import bpy

SRC = r"E:\dsh-pet-projects\body\anims\anim5\tripo_convert_50935b14-2895-451b-b3bb-6925135e1347.fbx"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
bpy.context.view_layer.update()

for mat in bpy.data.materials:
    print("=== 材质:", mat.name, "use_nodes=", mat.use_nodes)
    if not mat.use_nodes:
        continue
    for n in mat.node_tree.nodes:
        if n.type == "TEX_IMAGE":
            img = n.image
            print("  贴图节点:", n.name, "| 文件:", (img.filepath if img else "无"),
                  "| 颜色空间:", (img.colorspace_settings.name if img else "-"),
                  "| 尺寸:", (tuple(img.size) if img else "-"))
        elif n.type == "BSDF_PRINCIPLED":
            base = n.inputs.get("Base Color")
            rough = n.inputs.get("Roughness")
            metal = n.inputs.get("Metallic")
            print("  BSDF base_color linked:", base.is_linked,
                  "| roughness:", (rough.default_value if not rough.is_linked else "linked"),
                  "| metallic:", (metal.default_value if not metal.is_linked else "linked"))
