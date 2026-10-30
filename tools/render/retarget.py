"""把 v1 的动捕（mixamorig）重定向到 v3 的 VRM 骨架（J_Bip_*）。

原理：按"静止姿态的差"换算。对每根骨：
    target_pose = rest_target @ (rest_source⁻¹ @ source_pose)
同时把根骨的位移压平（桌宠窗口跟不了她走），只保留上下起伏。

用法（Blender 无头）：
    blender -b -P retarget.py -- <rigged.glb> <mocap.fbx> <输出.blend> <动作名关键字> <帧数>
"""

import math
import sys

import bpy
from mathutils import Matrix

ARGS = sys.argv[sys.argv.index("--") + 1:]
RIG, MOCAP, OUT = ARGS[0], ARGS[1], ARGS[2]
ACTION_KEY = ARGS[3] if len(ARGS) > 3 else "idle"
FRAMES = int(ARGS[4]) if len(ARGS) > 4 else 96

# mixamorig → J_Bip
MAP = {
    "Hips": "J_Bip_C_Hips",
    "Spine": "J_Bip_C_Spine",
    "Spine1": "J_Bip_C_Chest",
    "Spine2": "J_Bip_C_UpperChest",
    "Neck": "J_Bip_C_Neck",
    "Head": "J_Bip_C_Head",
    "LeftShoulder": "J_Bip_L_Shoulder",
    "LeftArm": "J_Bip_L_UpperArm",
    "LeftForeArm": "J_Bip_L_LowerArm",
    "LeftHand": "J_Bip_L_Hand",
    "RightShoulder": "J_Bip_R_Shoulder",
    "RightArm": "J_Bip_R_UpperArm",
    "RightForeArm": "J_Bip_R_LowerArm",
    "RightHand": "J_Bip_R_Hand",
    "LeftUpLeg": "J_Bip_L_UpperLeg",
    "LeftLeg": "J_Bip_L_LowerLeg",
    "LeftFoot": "J_Bip_L_Foot",
    "LeftToeBase": "J_Bip_L_ToeBase",
    "RightUpLeg": "J_Bip_R_UpperLeg",
    "RightLeg": "J_Bip_R_LowerLeg",
    "RightFoot": "J_Bip_R_Foot",
    "RightToeBase": "J_Bip_R_ToeBase",
}
for f, j in (("Thumb", "Thumb"), ("Index", "Index"), ("Middle", "Middle"),
             ("Ring", "Ring"), ("Little", "Little")):
    for side in ("Left", "Right"):
        for seg in (1, 2, 3):
            MAP["%sHand%s%d" % (side, f, seg)] = "J_Bip_%s_%s%d" % (
                "L" if side == "Left" else "R", j, seg)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=RIG)
bpy.context.view_layer.update()
tgt_arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
tgt_name = tgt_arm.name
print("目标骨架:", tgt_name, "| 骨数:", len(tgt_arm.data.bones))

bpy.ops.import_scene.fbx(filepath=MOCAP)
bpy.context.view_layer.update()
src_arm = next(o for o in bpy.context.scene.objects
               if o.type == "ARMATURE" and o.name != tgt_name)
print("源骨架:", src_arm.name, "| 骨数:", len(src_arm.data.bones))

# 选动作
acts = [a for a in bpy.data.actions if ACTION_KEY.lower() in a.name.lower()]
if not acts:
    print("找不到动作:", ACTION_KEY, "| 现有:", [a.name for a in bpy.data.actions])
    raise SystemExit(1)
act = acts[0]
print("动作:", act.name)


def iter_fcurves(a):
    try:
        return list(a.fcurves)
    except AttributeError:
        out = []
        for layer in getattr(a, "layers", []):
            for strip in getattr(layer, "strips", []):
                for cb in getattr(strip, "channelbags", []):
                    out.extend(cb.fcurves)
        return out


if src_arm.animation_data is None:
    src_arm.animation_data_create()
src_arm.animation_data.action = act

for pb in tgt_arm.pose.bones:
    pb.rotation_mode = "QUATERNION"

rest_s = {b.name: b.matrix_local.copy() for b in src_arm.data.bones}
rest_t = {b.name: b.matrix_local.copy() for b in tgt_arm.data.bones}

pairs = []
for s_name, t_name in MAP.items():
    s_full = "mixamorig:" + s_name
    if s_full in src_arm.pose.bones and t_name in tgt_arm.pose.bones:
        pairs.append((s_full, t_name))
print("可映射骨骼:", len(pairs))

# 按层级排序（父先子后）
depth = {}
for b in tgt_arm.data.bones:
    d, p = 0, b.parent
    while p:
        d += 1
        p = p.parent
    depth[b.name] = d
pairs.sort(key=lambda pr: depth.get(pr[1], 0))

bpy.context.view_layer.objects.active = tgt_arm
if tgt_arm.animation_data is None:
    tgt_arm.animation_data_create()
new_act = bpy.data.actions.new("retarget_" + ACTION_KEY)
tgt_arm.animation_data.action = new_act

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = FRAMES

for f in range(1, FRAMES + 1):
    bpy.context.scene.frame_set(f)
    bpy.context.view_layer.update()
    for s_full, t_name in pairs:
        sp = src_arm.pose.bones[s_full]
        tp = tgt_arm.pose.bones[t_name]
        delta = rest_s[s_full].inverted() @ sp.matrix
        want = rest_t[t_name] @ delta
        # 根骨：压掉水平位移
        if t_name == "J_Bip_C_Hips":
            want.translation = tp.matrix.translation.copy()
            want.translation.z = rest_t[t_name].translation.z + (sp.matrix.translation.z - rest_s[s_full].translation.z)
        tp.matrix = want
        tp.keyframe_insert("rotation_quaternion", frame=f)
        if t_name == "J_Bip_C_Hips":
            tp.keyframe_insert("location", frame=f)

for fc in iter_fcurves(new_act):
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"

bpy.context.scene.frame_end = FRAMES
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT)
