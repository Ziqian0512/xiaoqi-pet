"""给小祈 v2（VRM 骨架）加发束骨和裙骨，并按几何刷权重。

v2 骨架是 J_Bip_*（VRM 命名），高度约 1.0。
"""

import math

import bpy
from mathutils import Vector

SRC = r"E:\dsh-pet-projects\body\v2\xiaoqi-v2-rig.glb"
OUT = r"E:\dsh-pet-projects\body\v2\xiaoqi-v2-dynamics.blend"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
bpy.context.view_layer.update()

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
meshes.sort(key=lambda o: len(o.data.vertices), reverse=True)
for ob in meshes[1:]:
    bpy.data.objects.remove(ob, do_unlink=True)
mesh = meshes[0]
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
mw = mesh.matrix_world

b = arm.data.bones
hips = b.get("J_Bip_C_Hips")
head = b.get("J_Bip_C_Head")
hips_h = arm.matrix_world @ hips.head_local
head_h = arm.matrix_world @ head.head_local
print("Hips:", tuple(round(v, 3) for v in hips_h), "Head:", tuple(round(v, 3) for v in head_h))

zs = [(mw @ v.co).z for v in mesh.data.vertices]
zmin, zmax = min(zs), max(zs)
print("网格 z:", round(zmin, 3), "-", round(zmax, 3), "顶点:", len(mesh.data.vertices))

# ---------- 发束骨 ----------
HAIR_SEG = 3
hair_names = {}
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones
for side in ("L", "R"):
    sign = 1 if side == "L" else -1
    base = Vector((head_h.x + sign * 0.12, head_h.y + 0.04, head_h.z + 0.04))
    prev = None
    for i in range(HAIR_SEG):
        nb = eb.new("hair_%s_%d" % (side, i))
        nb.head = base + Vector((0, 0, -0.11 * i))
        nb.tail = base + Vector((sign * 0.012 * i, 0.004 * i, -0.11 * (i + 1)))
        if prev is None:
            nb.parent = eb[head.name]
            nb.use_connect = False
        else:
            nb.parent = prev
            nb.use_connect = True
        prev = nb
    hair_names[side] = ["hair_%s_%d" % (side, i) for i in range(HAIR_SEG)]

# ---------- 裙骨 ----------
SK_CH = 6
TOP = hips_h.z + 0.05
HEM = zmin + (zmax - zmin) * 0.34
skirt_names = []
for i in range(SK_CH):
    ang = 2 * math.pi * i / SK_CH
    dx, dy = math.cos(ang), math.sin(ang)
    a = eb.new("skirt_%d_a" % i)
    a.head = Vector((hips_h.x + 0.05 * dx, hips_h.y + 0.05 * dy, TOP))
    a.tail = Vector((hips_h.x + 0.09 * dx, hips_h.y + 0.09 * dy, (TOP + HEM) / 2))
    a.parent = eb[hips.name]
    a.use_connect = False
    c = eb.new("skirt_%d_b" % i)
    c.head = a.tail
    c.tail = Vector((hips_h.x + 0.13 * dx, hips_h.y + 0.13 * dy, HEM))
    c.parent = a
    c.use_connect = True
    skirt_names.append((i, a.name, c.name))
bpy.ops.object.mode_set(mode="OBJECT")
print("新增骨:", sum(len(v) for v in hair_names.values()) + SK_CH * 2)

# ---------- 刷权重（按骨架主导骨判定头发，避免抓到手臂）----------
def vg(name):
    return mesh.vertex_groups.get(name) or mesh.vertex_groups.new(name=name)


for names in hair_names.values():
    for n in names:
        vg(n)
for _i, a, c in skirt_names:
    vg(a)
    vg(c)

gidx = {g.index: g.name for g in mesh.vertex_groups}
head_vg = mesh.vertex_groups.get("J_Bip_C_Head")
hips_vg = mesh.vertex_groups.get("J_Bip_C_Hips")

face_w = 0.105            # 脸的半宽
top_z = head_h.z + 0.08   # 头顶以上
hair_n = skirt_n = 0
for v in mesh.data.vertices:
    p = mw @ v.co
    r = math.hypot(p.x, p.y)

    # 主导骨
    dom, dom_w = "", 0.0
    for g in v.groups:
        if g.weight > dom_w:
            dom_w = g.weight
            dom = gidx.get(g.group, "")

    # 头发：主导骨是 Head，且不在脸中央（两侧或头顶）
    if dom == "J_Bip_C_Head" and (abs(p.x) > face_w or p.z > top_z):
        side = "L" if p.x > 0 else "R"
        names = hair_names[side]
        t = max(0.0, min(1.0, (zmax - p.z) / (zmax - head_h.z)))
        seg = min(HAIR_SEG - 1, int(t * HAIR_SEG))
        frac = t * HAIR_SEG - seg
        vg(names[seg]).add([v.index], 0.7 * (1 - frac) + 0.3, "REPLACE")
        if seg + 1 < HAIR_SEG:
            vg(names[seg + 1]).add([v.index], 0.7 * frac, "REPLACE")
        hair_n += 1
        continue

    # 裙子：主导骨是腿或胯，且半径大、高度在胯到裙摆之间
    if dom in ("J_Bip_L_UpperLeg", "J_Bip_R_UpperLeg", "J_Bip_C_Hips") and r > 0.09 \
            and HEM - 0.02 <= p.z <= TOP:
        ang = math.atan2(p.y - hips_h.y, p.x - hips_h.x) % (2 * math.pi)
        k = int(round(ang / (2 * math.pi / SK_CH))) % SK_CH
        _i, a, c = skirt_names[k]
        t = max(0.0, min(1.0, (TOP - p.z) / (TOP - HEM)))
        if hips_vg:
            hips_vg.add([v.index], max(0.0, 1.0 - t * 2.0), "REPLACE")
        vg(a).add([v.index], (1 - t) * 0.8, "REPLACE")
        vg(c).add([v.index], t * 0.8, "REPLACE")
        skirt_n += 1

print("刷了头发顶点:", hair_n, "| 裙摆顶点:", skirt_n)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT)
