"""修 v3 的蒙皮串味：裙摆顶点不许受手臂/手骨影响。

做法：
1. 读出骨架里所有 arm/hand/forearm/shoulder 骨的名字
2. 找出裙摆区域顶点（胯高 ~ 裙摆下沿，半径较大）
3. 从这些顶点上移除上述骨的权重，统一给 Hips
"""

import math

import bpy

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-idle-rt3.blend"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-fixskin.blend"

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()

arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
print("网格:", [m.name for m in meshes])

arm_bones = {b.name for b in arm.data.bones
             if any(k in b.name for k in ("Shoulder", "UpperArm", "LowerArm", "Hand", "Thumb",
                                          "Index", "Middle", "Ring", "Little"))}
print("手臂相关骨:", len(arm_bones))

hips = arm.data.bones.get("J_Bip_C_Hips")
hips_z = (arm.matrix_world @ hips.head_local).z
print("Hips z:", round(hips_z, 3))

for mesh in meshes:
    mw = mesh.matrix_world
    gname = {g.index: g.name for g in mesh.vertex_groups}
    fixed = 0
    for v in mesh.data.vertices:
        p = mw @ v.co
        r = math.hypot(p.x, p.y)
        # 裙摆：胯部以下、裙摆上、半径大（腿在 r<0.08，裙摆在 r>0.10）
        if not (hips_z - 0.30 <= p.z <= hips_z + 0.04 and r > 0.095):
            continue
        touched = False
        for g in list(v.groups):
            name = gname.get(g.group, "")
            if name in arm_bones:
                mesh.vertex_groups[g.group].remove([v.index])
                touched = True
        if touched:
            vg = mesh.vertex_groups.get("J_Bip_C_Hips") or mesh.vertex_groups.new(name="J_Bip_C_Hips")
            vg.add([v.index], 1.0, "REPLACE")
            fixed += 1
    if fixed:
        print("  %s: 修了 %d 个裙摆顶点" % (mesh.name, fixed))

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT)
