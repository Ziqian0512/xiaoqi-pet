"""试验：给上臂骨加固定外展偏移，看哪个轴能把手臂推开。

用法：blender -b -P arm_out_test.py -- <blend> <输出目录> <轴x|y|z> <角度度>
"""

import math
import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT, AXIS = ARGS[0], ARGS[1], ARGS[2]
DEG = float(ARGS[3]) if len(ARGS) > 3 else 12.0

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")

for name in ("J_Bip_R_UpperArm",):
    pb = arm.pose.bones.get(name)
    if not pb:
        continue
    pb.rotation_mode = "XYZ"
    sign = 1.0
    ang = math.radians(DEG) * sign
    cur = list(pb.rotation_euler)
    idx = {"x": 0, "y": 1, "z": 2}[AXIS]
    cur[idx] += ang
    pb.rotation_euler = cur

bpy.context.scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved:", OUT, "| axis", AXIS, DEG)
