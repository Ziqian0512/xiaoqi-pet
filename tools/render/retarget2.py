"""重定向 v2：用 Copy Rotation 约束（世界空间）+ 烘焙，只复制旋转，不动位移。"""

import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:]
RIG, MOCAP, OUT = ARGS[0], ARGS[1], ARGS[2]
ACTION_KEY = ARGS[3] if len(ARGS) > 3 else "idle"
FRAMES = int(ARGS[4]) if len(ARGS) > 4 else 96

MAP = {
    "Hips": "J_Bip_C_Hips", "Spine": "J_Bip_C_Spine", "Spine1": "J_Bip_C_Chest",
    "Spine2": "J_Bip_C_UpperChest", "Neck": "J_Bip_C_Neck", "Head": "J_Bip_C_Head",
    "LeftShoulder": "J_Bip_L_Shoulder", "LeftArm": "J_Bip_L_UpperArm",
    "LeftForeArm": "J_Bip_L_LowerArm", "LeftHand": "J_Bip_L_Hand",
    "RightShoulder": "J_Bip_R_Shoulder", "RightArm": "J_Bip_R_UpperArm",
    "RightForeArm": "J_Bip_R_LowerArm", "RightHand": "J_Bip_R_Hand",
    "LeftUpLeg": "J_Bip_L_UpperLeg", "LeftLeg": "J_Bip_L_LowerLeg",
    "LeftFoot": "J_Bip_L_Foot", "LeftToeBase": "J_Bip_L_ToeBase",
    "RightUpLeg": "J_Bip_R_UpperLeg", "RightLeg": "J_Bip_R_LowerLeg",
    "RightFoot": "J_Bip_R_Foot", "RightToeBase": "J_Bip_R_ToeBase",
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
tgt = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
tgt_name = tgt.name

bpy.ops.import_scene.fbx(filepath=MOCAP)
bpy.context.view_layer.update()
src = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE" and o.name != tgt_name)

acts = [a for a in bpy.data.actions if ACTION_KEY.lower() in a.name.lower()]
if not acts:
    raise SystemExit("找不到动作 " + ACTION_KEY)
act = acts[0]
print("动作:", act.name)
if src.animation_data is None:
    src.animation_data_create()
src.animation_data.action = act

# 只保留目标骨架 + 它的网格，删掉源骨架的网格
for ob in list(bpy.context.scene.objects):
    if ob.type == "MESH" and ob.parent and ob.parent.name == src.name:
        bpy.data.objects.remove(ob, do_unlink=True)

n = 0
for s_name, t_name in MAP.items():
    s_full = "mixamorig:" + s_name
    if s_full not in src.pose.bones or t_name not in tgt.pose.bones:
        continue
    pb = tgt.pose.bones[t_name]
    for c in list(pb.constraints):
        pb.constraints.remove(c)
    con = pb.constraints.new("COPY_ROTATION")
    con.target = src
    con.subtarget = s_full
    con.target_space = "LOCAL"
    con.owner_space = "LOCAL"
    con.mix_mode = "REPLACE"
    n += 1
print("约束个数:", n)

bpy.context.view_layer.objects.active = tgt
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.select_all(action="SELECT")
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = FRAMES
bpy.ops.nla.bake(frame_start=1, frame_end=FRAMES, only_selected=False,
                 visual_keying=True, clear_constraints=True, clear_parents=False,
                 use_current_action=False, bake_types={"POSE"})
bpy.ops.object.mode_set(mode="OBJECT")

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT)
