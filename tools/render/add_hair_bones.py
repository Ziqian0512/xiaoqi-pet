"""给双马尾加骨骼链（挂 Head 下），并按区域刷权重。

几何依据（来自实测）：
- 头部骨 head z≈0.828，头顶 0.946
- 双马尾：|x| 0.10–0.22，z 0.55–0.95，y 0 ~ 0.13（在脑后/两侧）
- 手臂：|x| 0.15–0.22，但 y≈-0.13（身前）→ 用 y > -0.05 排除手臂
"""

import math

import bpy
from mathutils import Vector

BLEND_IN = r"E:\dsh-pet-projects\body\xiaoqi-rigged-skirt.blend"
BLEND_OUT = r"E:\dsh-pet-projects\body\xiaoqi-rigged-hair.blend"

SEGMENTS = 3


def side_of(p):
    return "L" if p.x > 0 else "R"


bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
bpy.context.view_layer.update()

arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
mesh_ob = next(o for o in bpy.context.scene.objects if o.type == "MESH")
mw = mesh_ob.matrix_world

head_bone = arm.data.bones["mixamorig:Head"]
head_world = arm.matrix_world @ head_bone.head_local
print("Head 骨:", tuple(round(v, 3) for v in head_world))

# ---- 1. 造发束骨：两侧各 3 节，从头顶侧面往下 ----
chains = {}
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones
for side in ("L", "R"):
    sign = 1 if side == "L" else -1
    base = Vector((head_world.x + sign * 0.10, head_world.y + 0.03, head_world.z + 0.06))
    prev = None
    for i in range(SEGMENTS):
        b = eb.new("hair_%s_%d" % (side, i))
        b.head = base + Vector((0, 0, -0.10 * i))
        b.tail = base + Vector((sign * 0.01 * i, 0.005 * i, -0.10 * (i + 1)))
        if prev is None:
            b.parent = eb[head_bone.name]
            b.use_connect = False
        else:
            b.parent = prev
            b.use_connect = True
        prev = b
    chains[side] = ["hair_%s_%d" % (side, i) for i in range(SEGMENTS)]
bpy.ops.object.mode_set(mode="OBJECT")
print("发束骨:", sum(len(v) for v in chains.values()))

# ---- 2. 选中头发顶点 ----
hair_verts = []
for v in mesh_ob.data.vertices:
    p = mw @ v.co
    r = math.hypot(p.x, p.y)
    if p.z < 0.52 or p.z > 0.98:
        continue
    if abs(p.x) < 0.095:
        continue          # 太靠中线，是脸/脖子
    if p.y < -0.05:
        continue          # 身前，是手臂
    if r < 0.10:
        continue
    hair_verts.append((v.index, p))
print("头发候选顶点:", len(hair_verts))

for side, names in chains.items():
    for n in names:
        if n not in mesh_ob.vertex_groups:
            mesh_ob.vertex_groups.new(name=n)

# 先从这些顶点的原有组里抠掉一部分权重，避免和头骨打架
head_group = mesh_ob.vertex_groups.get("mixamorig:Head")
for idx, _p in hair_verts:
    try:
        if head_group:
            head_group.add([idx], 0.25, "REPLACE")
    except RuntimeError:
        pass

# 按高度分段给骨链权重（上→下）
for idx, p in hair_verts:
    side = side_of(p)
    names = chains[side]
    t = max(0.0, min(1.0, (0.94 - p.z) / 0.36))     # 0=高 1=低
    seg = min(SEGMENTS - 1, int(t * SEGMENTS))
    w = 0.75 / max(1, SEGMENTS)
    # 相邻两节平滑过渡
    frac = t * SEGMENTS - seg
    mesh_ob.vertex_groups[names[seg]].add([idx], w * (1.0 - frac) + 0.25, "REPLACE")
    if seg + 1 < SEGMENTS:
        mesh_ob.vertex_groups[names[seg + 1]].add([idx], w * frac, "REPLACE")

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print("已保存:", BLEND_OUT)
