"""把 v3 减面后的 12 个部件合并成一个网格，导出 GLB（带贴图），用于上传 Tripo 绑骨。"""

import bpy

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-low.blend"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-merge.glb"

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
print("合并前:", len(meshes), "个网格")

bpy.ops.object.select_all(action="DESELECT")
for ob in meshes:
    ob.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.join()

merged = bpy.context.view_layer.objects.active
tris = sum(len(p.vertices) - 2 for p in merged.data.polygons)
print("合并后:", merged.name, "| 顶点", len(merged.data.vertices), "| 三角面", tris,
      "| 材质", len(merged.data.materials))

bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format="GLB",
    use_selection=True,
    export_apply=True,
    export_texcoords=True,
    export_normals=True,
    export_materials="EXPORT",
)
print("导出:", OUT)
