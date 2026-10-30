import bpy
import bmesh
import math
from mathutils import Vector

SRC = r"E:\dsh-pet-projects\body\anims\anim5\tripo_convert_50935b14-2895-451b-b3bb-6925135e1347.fbx"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
bpy.context.view_layer.update()
mesh_ob = next(o for o in bpy.context.scene.objects if o.type == "MESH")
mw = mesh_ob.matrix_world

bm = bmesh.new()
bm.from_mesh(mesh_ob.data)
bm.verts.ensure_lookup_table()

print("=== 裙子候选带 z 0.38–0.60：半径分布 ===")
for z0 in (0.38, 0.42, 0.46, 0.50, 0.54, 0.58):
    rs = []
    for v in bm.verts:
        p = mw @ v.co
        if z0 <= p.z < z0 + 0.04:
            rs.append(math.sqrt(p.x ** 2 + p.y ** 2))
    if not rs:
        continue
    rs.sort()
    n = len(rs)
    print("  z=%.2f n=%4d  r: min=%.3f p50=%.3f p90=%.3f max=%.3f"
          % (z0, n, rs[0], rs[n // 2], rs[int(n * 0.9)], rs[-1]))

print("\n=== 头发候选（z>0.62 且半径>0.10）：y 分布 ===")
ys = []
for v in bm.verts:
    p = mw @ v.co
    if p.z > 0.62 and math.sqrt(p.x ** 2 + p.y ** 2) > 0.10:
        ys.append(p.y)
if ys:
    ys.sort()
    n = len(ys)
    print("  n=%d  y: min=%.3f p50=%.3f max=%.3f" % (n, ys[0], ys[n // 2], ys[-1]))
bm.free()
