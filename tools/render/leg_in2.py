"""腿内收（左右分别给角度，做成对称站姿）。"""

import math
import sys

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = ARGS[0], ARGS[1]
DEG_L = float(ARGS[2]) if len(ARGS) > 2 else 4.5
DEG_R = float(ARGS[3]) if len(ARGS) > 3 else 2.2

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
sc = bpy.context.scene

for name, deg, sign in (("J_Bip_L_UpperLeg", DEG_L, -1.0), ("J_Bip_R_UpperLeg", DEG_R, 1.0)):
    pb = arm.pose.bones.get(name)
    if pb is None:
        continue
    pb.rotation_mode = "XYZ"
    for f in range(sc.frame_start, sc.frame_end + 1):
        sc.frame_set(f)
        rot = list(pb.rotation_euler)
        rot[0] = math.radians(deg) * sign
        pb.rotation_euler = rot
        pb.keyframe_insert("rotation_euler", frame=f)

sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
for name in ("J_Bip_L_Foot", "J_Bip_R_Foot"):
    pb = arm.pose.bones.get(name)
    if pb:
        w = arm.matrix_world @ pb.tail
        print("FOOT %s x=%.4f" % (name, w.x))
print("saved:", OUT)
