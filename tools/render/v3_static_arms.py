"""把手臂改成静态自然姿态：上臂微外展、肘部微弯，不再跟动捕走。

Q 版手臂短，动捕的手臂角度会让肘部翻折。待机不需要手臂摆动。
"""

import math

import bpy
from mathutils import Euler

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-fixskin.blend"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-staticarms.blend"

# 每根骨固定角度（度）：(x, y, z)，本地空间
POSE = {
    "J_Bip_L_Shoulder": (0, 0, 0),
    "J_Bip_R_Shoulder": (0, 0, 0),
    "J_Bip_L_UpperArm": (0, 0, 0),
    "J_Bip_R_UpperArm": (0, 0, 0),
    "J_Bip_L_LowerArm": (0, 0, 0),
    "J_Bip_R_LowerArm": (0, 0, 0),
    "J_Bip_L_Hand": (0, 0, 0),
    "J_Bip_R_Hand": (0, 0, 0),
}

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
sc = bpy.context.scene

# 手指一律归零
finger = [b.name for b in arm.data.bones
          if any(k in b.name for k in ("Thumb", "Index", "Middle", "Ring", "Little"))]
for name in finger:
    POSE[name] = (0, 0, 0)

for pb in arm.pose.bones:
    if pb.name in POSE:
        pb.rotation_mode = "XYZ"

for f in range(sc.frame_start, sc.frame_end + 1):
    sc.frame_set(f)
    for name, rot in POSE.items():
        pb = arm.pose.bones.get(name)
        if pb is None:
            continue
        pb.rotation_euler = Euler(rot, "XYZ")
        pb.keyframe_insert("rotation_euler", frame=f)

sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT, "| 固定姿态骨:", len(POSE))
