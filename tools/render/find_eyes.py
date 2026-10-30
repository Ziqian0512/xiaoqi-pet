"""找眼睛和嘴的位置：用 UV 采样贴图颜色，红色虹膜 → 眼球中心。"""

import bpy

BLEND = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-staticarms.blend"
TEX = r"E:\dsh-pet-projects\body\v3\textures\03_anime_girl_3d_model_tripo_part_3_basecol.jpg"

bpy.ops.wm.open_mainfile(filepath=BLEND)
bpy.context.view_layer.update()

mesh = next(o for o in bpy.context.scene.objects if o.type == "MESH" and len(o.data.vertices) > 1000)
mw = mesh.matrix_world
img = bpy.data.images.load(TEX)
W, H = img.size
px = list(img.pixels)          # RGBA float, 0..1

uv_layer = mesh.data.uv_layers.active
if uv_layer is None:
    raise SystemExit("没有 UV")

def sample(u, v):
    x = int((u % 1.0) * (W - 1))
    y = int((v % 1.0) * (H - 1))
    i = (y * W + x) * 4
    return px[i], px[i + 1], px[i + 2]

# 每个顶点：用它的一个 loop 的 UV
loop_uv = {}
for poly in mesh.data.polygons:
    for li in poly.loop_indices:
        vi = mesh.data.loops[li].vertex_index
        if vi not in loop_uv:
            loop_uv[vi] = (uv_layer.data[li].uv[0], uv_layer.data[li].uv[1])

reds = []
for vi, (u, v) in loop_uv.items():
    r, g, b = sample(u, v)
    if r > 0.55 and g < 0.30 and b < 0.40 and r > g * 2.5:
        p = mw @ mesh.data.vertices[vi].co
        if 0.72 < p.z < 0.90 and p.y < -0.05:
            reds.append((p.x, p.y, p.z))

print("红色顶点数:", len(reds))
if reds:
    left = [p for p in reds if p[0] > 0]
    right = [p for p in reds if p[0] <= 0]
    for name, grp in (("左(视图右)", left), ("右", right)):
        if not grp:
            continue
        xs = [g[0] for g in grp]; ys = [g[1] for g in grp]; zs = [g[2] for g in grp]
        print("%s  n=%d  center=(%.3f, %.3f, %.3f)  z范围 %.3f..%.3f  x范围 %.3f..%.3f"
              % (name, len(grp), sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs),
                 min(zs), max(zs), min(xs), max(xs)))
