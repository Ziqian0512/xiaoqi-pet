"""做一个挥手动作：抬起右臂 + 摆小臂，用来验证"手臂动时裙子不动"。

基于手臂已归零的那版（xiaoqi-v3-staticarms.blend）。
"""

import math

import bpy

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-staticarms.blend"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-wave.blend"
FRAMES = 72          # 3 秒 @24fps

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
sc = bpy.context.scene

up = arm.pose.bones.get("J_Bip_R_UpperArm")
fore = arm.pose.bones.get("J_Bip_R_LowerArm")
hand = arm.pose.bones.get("J_Bip_R_Hand")
for pb in (up, fore, hand):
    if pb:
        pb.rotation_mode = "XYZ"

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")

for f in range(1, FRAMES + 1):
    t = (f - 1) / FRAMES
    # 0-0.25 抬臂；0.25-0.75 摆动；0.75-1 放下
    if t < 0.25:
        k = t / 0.25
        lift = 1.15 * k
        swing = 0.0
    elif t < 0.75:
        lift = 1.15
        swing = 0.45 * math.sin(2 * math.pi * (t - 0.25) / 0.5 * 2)
    else:
        k = (1.0 - t) / 0.25
        lift = 1.15 * k
        swing = 0.0

    if up:
        up.rotation_euler = (0.0, 0.0, lift)
        up.keyframe_insert("rotation_euler", frame=f)
    if fore:
        fore.rotation_euler = (0.0, 0.0, 0.20 + swing)
        fore.keyframe_insert("rotation_euler", frame=f)
    if hand:
        hand.rotation_euler = (0.0, 0.0, swing * 0.5)
        hand.keyframe_insert("rotation_euler", frame=f)

bpy.ops.object.mode_set(mode="OBJECT")
sc.frame_start = 1
sc.frame_end = FRAMES
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT, "| 帧数", FRAMES)
