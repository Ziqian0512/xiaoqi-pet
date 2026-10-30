"""v3 分件减面：按部件类型给不同目标面数，保留 UV/贴图，存成可渲染的 blend。

目标总量 ~6 万面（桌宠 720p 足够），头发和裙子保留更多面。
"""

import bpy

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-parts.glb"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-low.blend"

# 部件 → 目标三角面数
TARGETS = {
    "tripo_part_0": 14000,   # 头发
    "tripo_part_1": 22000,   # 身体+上衣
    "tripo_part_3": 8000,    # 头/脸
    "tripo_part_2": 4000,    # 腿
    "tripo_part_5": 4000,
    "tripo_part_7": 3000,    # 裙
    "tripo_part_8": 2500,
    "tripo_part_9": 2500,
    "tripo_part_10": 800,    # 吊带
    "tripo_part_11": 800,
    "tripo_part_4": 1200,    # 鞋
    "tripo_part_6": 1200,
}
DROP = {"tripo_part_12"}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
bpy.context.view_layer.update()

removed, kept = [], []
for ob in list(bpy.context.scene.objects):
    if ob.type != "MESH":
        continue
    if ob.name in DROP:
        removed.append(ob.name)
        bpy.data.objects.remove(ob, do_unlink=True)
        continue
    tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
    target = TARGETS.get(ob.name)
    if target and tris > target * 1.1:
        mod = ob.modifiers.new("Decimate", "DECIMATE")
        mod.decimate_type = "COLLAPSE"
        mod.ratio = max(0.02, target / tris)
        mod.use_collapse_triangulate = True
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=mod.name)
        new_tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
        kept.append((ob.name, tris, new_tris))
    else:
        kept.append((ob.name, tris, tris))

total = 0
for name, before, after in sorted(kept, key=lambda r: -r[2]):
    total += after
    print("PART %-16s %7d -> %7d" % (name, before, after))
print("总计面数:", total, "| 删掉:", removed)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved:", OUT)
