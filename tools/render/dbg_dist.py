import bpy
import bmesh
import math
from mathutils import Vector

SRC = r"E:\dsh-pet-projects\body\anims\anim5\tripo_convert_50935b14-2895-451b-b3bb-6925135e1347.fbx"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
bpy.context.view_layer.update()

arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
mesh_ob = next(o for o in bpy.context.scene.objects if o.type == "MESH")
mw = mesh_ob.matrix_world

segs = []
for b in arm.data.bones:
    h = arm.matrix_world @ b.head_local
    t = arm.matrix_world @ b.tail_local
    if (t - h).length < 1e-5:
        continue
    segs.append((h, t))
print("骨段数:", len(segs))


def dist_to_skel(p: Vector) -> float:
    best = 1e9
    for h, t in segs:
        d = t - h
        L2 = d.dot(d)
        if L2 < 1e-9:
            best = min(best, (p - h).length)
            continue
        u = max(0.0, min(1.0, (p - h).dot(d) / L2))
        proj = h + d * u
        best = min(best, (p - proj).length)
    return best


bm = bmesh.new()
bm.from_mesh(mesh_ob.data)
bm.verts.ensure_lookup_table()

bands = {}
for v in bm.verts:
    p = mw @ v.co
    d = dist_to_skel(p)
    band = int(p.z * 10) / 10.0
    bands.setdefault(band, []).append((d, abs(p.x), p.z))
bm.free()

print("=== 各高度带的\"离骨架距离\"分布 ===")
for z in sorted(bands):
    ds = sorted(x[0] for x in bands[z])
    n = len(ds)
    p50 = ds[n // 2]
    p90 = ds[int(n * 0.9)]
    far = sum(1 for d in ds if d > 0.06)
    print("  z=%.1f  n=%5d  中位=%.3f  p90=%.3f  >6cm 的顶点=%d" % (z, n, p50, p90, far))
