"""给上臂加固定外展（绕本地 X 轴 +12°），烘进动作的所有帧。"""

import math

import bpy
from mathutils import Quaternion

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-fixskin.blend"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-arms.blend"
DEG = 12.0

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
sc = bpy.context.scene

pairs = [("J_Bip_L_UpperArm", 1.0), ("J_Bip_R_UpperArm", -1.0)]
for name, sign in pairs:
    pb = arm.pose.bones.get(name)
    if pb is None:
        continue
    q = Quaternion((1, 0, 0), math.radians(DEG) * sign)
    mode = pb.rotation_mode
    for f in range(sc.frame_start, sc.frame_end + 1):
        sc.frame_set(f)
        if mode == "QUATERNION":
            pb.rotation_quaternion = pb.rotation_quaternion @ q
            pb.keyframe_insert("rotation_quaternion", frame=f)
        else:
            pb.rotation_euler.x += math.radians(DEG) * sign
            pb.keyframe_insert("rotation_euler", frame=f)

sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT)
