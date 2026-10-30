"""测腿内收：把左右大腿骨在某轴转 deg（向内），量脚的位置。"""

import math
import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT, AXIS, DEG = ARGS[0], ARGS[1], ARGS[2], float(ARGS[3])

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
sc = bpy.context.scene
idx = {"x": 0, "y": 1, "z": 2}[AXIS]

for name, sign in (("J_Bip_L_UpperLeg", -1.0), ("J_Bip_R_UpperLeg", 1.0)):
    pb = arm.pose.bones.get(name)
    if pb is None:
        continue
    pb.rotation_mode = "XYZ"
    for f in range(sc.frame_start, sc.frame_end + 1):
        sc.frame_set(f)
        rot = list(pb.rotation_euler)
        rot[idx] = math.radians(DEG) * sign
        pb.rotation_euler = rot
        pb.keyframe_insert("rotation_euler", frame=f)

sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)

for name in ("J_Bip_L_Foot", "J_Bip_R_Foot"):
    pb = arm.pose.bones.get(name)
    if pb:
        w = arm.matrix_world @ pb.tail
        print("FOOT %s x=%.4f z=%.4f" % (name, w.x, w.z))
print("saved:", OUT, AXIS, DEG)
