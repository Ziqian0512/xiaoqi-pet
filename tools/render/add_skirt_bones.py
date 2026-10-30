"""给裙子加骨骼并重刷权重，解决"腿一张开裙子炸成一片"。

做法：
1. 在 Hips 下挂 6 组裙骨（每组 2 节，从腰到裙摆）
2. 裙摆顶点（z 0.34–0.58 且半径 > 0.075）重新分配权重：
   - 上缘 → Hips（跟着骨盆走）
   - 下缘 → 对应角度的裙骨
   - 原来的腿骨/身体权重清掉，避免双重拉扯
3. 保存成 .blend，供渲染脚本使用
"""

import math

import bpy
from mathutils import Vector

SRC = r"E:\dsh-pet-projects\body\anims\anim5\tripo_convert_50935b14-2895-451b-b3bb-6925135e1347.fbx"
OUT_BLEND = r"E:\dsh-pet-projects\body\xiaoqi-rigged-skirt.blend"

CHAINS = 6
TOP_Z = 0.552
MID_Z = 0.462
HEM_Z = 0.372
WAIST_R = 0.075
HEM_R = 0.175

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
bpy.context.view_layer.update()

arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
mesh_ob = next(o for o in bpy.context.scene.objects if o.type == "MESH")
mw = mesh_ob.matrix_world

hips = arm.data.bones["mixamorig:Hips"]
hips_head = arm.matrix_world @ hips.head_local
cx, cy = hips_head.x, hips_head.y
print("Hips:", (round(cx, 3), round(cy, 3), round(hips_head.z, 3)))

# ---- 1. 造裙骨 ----
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones
names = []
for i in range(CHAINS):
    ang = 2 * math.pi * i / CHAINS
    dx, dy = math.cos(ang), math.sin(ang)
    a = eb.new("skirt_%d_a" % i)
    a.head = Vector((cx + WAIST_R * 0.6 * dx, cy + WAIST_R * 0.6 * dy, TOP_Z))
    a.tail = Vector((cx + WAIST_R * 1.6 * dx, cy + WAIST_R * 1.6 * dy, MID_Z))
    a.parent = eb[hips.name]
    a.use_connect = False
    b = eb.new("skirt_%d_b" % i)
    b.head = a.tail
    b.tail = Vector((cx + HEM_R * 0.8 * dx, cy + HEM_R * 0.8 * dy, HEM_Z))
    b.parent = a
    b.use_connect = True
    names.append((i, a.name, b.name))
bpy.ops.object.mode_set(mode="OBJECT")
print("新增裙骨:", len(names) * 2)

# ---- 2. 重刷权重 ----
for _, a_name, b_name in names:
    for g in (a_name, b_name):
        if g not in mesh_ob.vertex_groups:
            mesh_ob.vertex_groups.new(name=g)
vg_hips = mesh_ob.vertex_groups.get("mixamorig:Hips") or mesh_ob.vertex_groups.new(name="mixamorig:Hips")

# 先清掉这些顶点在所有组里的旧权重
skirt_verts = []
for v in mesh_ob.data.vertices:
    p = mw @ v.co
    r = math.hypot(p.x - cx, p.y - cy)
    if HEM_Z - 0.02 <= p.z <= TOP_Z + 0.01 and r > WAIST_R:
        skirt_verts.append((v.index, p, r))
print("裙摆顶点:", len(skirt_verts))

all_groups = [g.index for g in mesh_ob.vertex_groups]
for idx, _p, _r in skirt_verts:
    for gi in all_groups:
        try:
            mesh_ob.vertex_groups[gi].remove([idx])
        except RuntimeError:
            pass

for idx, p, r in skirt_verts:
    ang = math.atan2(p.y - cy, p.x - cx) % (2 * math.pi)
    k = int(round(ang / (2 * math.pi / CHAINS))) % CHAINS
    _i, a_name, b_name = names[k]
    t = (TOP_Z - p.z) / (TOP_Z - HEM_Z)          # 0=腰 1=裙摆
    t = max(0.0, min(1.0, t))
    w_hips = max(0.0, 1.0 - t * 2.2)             # 上缘主要跟骨盆
    w_a = (1.0 - w_hips) * (1.0 - t) * 1.6
    w_b = (1.0 - w_hips) * t * 1.6
    tot = w_hips + w_a + w_b
    if tot <= 0:
        w_hips, w_a, w_b, tot = 1.0, 0.0, 0.0, 1.0
    vg_hips.add([idx], w_hips / tot, "REPLACE")
    mesh_ob.vertex_groups[a_name].add([idx], w_a / tot, "REPLACE")
    mesh_ob.vertex_groups[b_name].add([idx], w_b / tot, "REPLACE")

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("已保存:", OUT_BLEND)
