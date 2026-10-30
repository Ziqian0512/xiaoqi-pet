"""测"抬手"该绕哪个轴：把右臂在三个轴上各转 90°，烘焙成关键帧后渲一帧对比。

（直接摆姿势会被已有动作覆盖，所以必须写成关键帧。）
"""

import math
import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT, AXIS = ARGS[0], ARGS[1], ARGS[2]

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
sc = bpy.context.scene

pb = arm.pose.bones.get("J_Bip_R_UpperArm")
pb.rotation_mode = "XYZ"
idx = {"x": 0, "y": 1, "z": 2}[AXIS]

for f in range(sc.frame_start, sc.frame_end + 1):
    sc.frame_set(f)
    rot = list(pb.rotation_euler)
    rot[idx] = math.radians(90)
    pb.rotation_euler = rot
    pb.keyframe_insert("rotation_euler", frame=f)

sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved:", OUT, AXIS)
