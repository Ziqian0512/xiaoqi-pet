"""量手的位置：哪个轴能把手臂推得更开。"""

import math
import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:]
SRC = ARGS[0]

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
import os
bpy.context.scene.frame_set(int(os.environ.get("PROBE_FRAME", "1")))
bpy.context.view_layer.update()

for name in ("J_Bip_L_Hand", "J_Bip_R_Hand"):
    pb = arm.pose.bones.get(name)
    if pb:
        w = arm.matrix_world @ pb.tail
        print("HAND %s  x=%.4f  z=%.4f" % (name, w.x, w.z))
