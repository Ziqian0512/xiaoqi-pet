"""在 v3 的 VRM 骨上直接写"程序化待机"：呼吸 + 轻微转头 + 手臂微摆。

不依赖任何动捕，幅度可控、必定不会拧成一团。
"""

import math

import bpy

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-rig.glb"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-proc-idle.blend"
FRAMES = 120

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
bpy.context.view_layer.update()

arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
if arm.animation_data is None:
    arm.animation_data_create()
act = bpy.data.actions.new("proc_idle")
arm.animation_data.action = act

SWAY = {
    "J_Bip_C_Hips": (0.012, 0.0, 0.0),
    "J_Bip_C_Spine": (0.020, 0.0, 0.010),
    "J_Bip_C_Chest": (0.014, 0.0, 0.008),
    "J_Bip_C_Neck": (0.010, 0.030, 0.0),
    "J_Bip_C_Head": (0.014, 0.045, 0.012),
    "J_Bip_L_Shoulder": (0.0, 0.0, 0.012),
    "J_Bip_R_Shoulder": (0.0, 0.0, -0.012),
    "J_Bip_L_UpperArm": (0.010, 0.0, 0.035),
    "J_Bip_R_UpperArm": (0.010, 0.0, -0.035),
}


def wave(t, phase, amp):
    return amp * math.sin(2 * math.pi * t + phase)


bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for pb in arm.pose.bones:
    pb.rotation_mode = "XYZ"

for f in range(1, FRAMES + 1):
    t = (f - 1) / FRAMES
    for pb in arm.pose.bones:
        name = pb.name
        if name in SWAY:
            ax, ay, az = SWAY[name]
            pb.rotation_euler = (
                wave(t, 0.0, ax),
                wave(t, 0.7, ay),
                wave(t, 1.4, az),
            )
            pb.keyframe_insert("rotation_euler", frame=f)
    hips = arm.pose.bones.get("J_Bip_C_Hips")
    if hips:
        hips.location = (0.0, 0.0, 0.006 * math.sin(2 * math.pi * t))
        hips.keyframe_insert("location", frame=f)
bpy.ops.object.mode_set(mode="OBJECT")

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = FRAMES
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT)
