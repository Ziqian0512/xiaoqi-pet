import bpy
import bmesh
from mathutils import Vector

SRC = r"E:\dsh-pet-projects\body\anims\anim5\tripo_convert_50935b14-2895-451b-b3bb-6925135e1347.fbx"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
bpy.context.view_layer.update()

mesh_ob = next(o for o in bpy.context.scene.objects if o.type == "MESH")
mw = mesh_ob.matrix_world
me = mesh_ob.data
bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table()

seen = set()
islands = []
for v in bm.verts:
    if v.index in seen:
        continue
    stack = [v]
    comp = []
    seen.add(v.index)
    while stack:
        cur = stack.pop()
        comp.append(cur.index)
        for e in cur.link_edges:
            other = e.other_vert(cur)
            if other.index not in seen:
                seen.add(other.index)
                stack.append(other)
    islands.append(comp)

print("连通块数量:", len(islands))
islands.sort(key=len, reverse=True)
for i, comp in enumerate(islands[:12]):
    co = [mw @ bm.verts[j].co for j in comp]
    xs = [c.x for c in co]; ys = [c.y for c in co]; zs = [c.z for c in co]
    print("  #%d 顶点=%5d  x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]"
          % (i, len(comp), min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
bm.free()
