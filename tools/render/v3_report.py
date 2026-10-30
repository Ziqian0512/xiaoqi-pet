"""导入 v3 分件 GLB，报告每件的包围盒/面数，并按位置猜名字。"""

import bpy
from mathutils import Vector

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-parts.glb"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-report.blend"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
bpy.context.view_layer.update()

objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
print("网格数:", len(objs))

rows = []
for o in objs:
    mw = o.matrix_world
    zs, xs, ys = [], [], []
    for v in o.data.vertices:
        p = mw @ v.co
        xs.append(p.x); ys.append(p.y); zs.append(p.z)
    tris = sum(len(pl.vertices) - 2 for pl in o.data.polygons)
    rows.append((o.name, tris, min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))

rows.sort(key=lambda r: -r[1])

for r in rows:
    print("PART %-22s %8d x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]" % r)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved:", OUT)
