import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

s = s.replace('''    sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [
        e.bl_rna.identifier for e in bpy.types.RenderEngine.__subclasses__()
    ] or hasattr(bpy.types, "RenderEngine") else "BLENDER_EEVEE"
    try:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        sc.render.engine = "BLENDER_EEVEE"''',
'''    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue''')

s = s.replace('''def bounds_of_meshes():
    mins = Vector((1e9, 1e9, 1e9))''',
'''def bounds_of_meshes():
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    mins = Vector((1e9, 1e9, 1e9))''')

s = s.replace('''        for corner in ob.bound_box:
            world = ob.matrix_world @ Vector(corner)''',
'''        ev = ob.evaluated_get(deps)
        for corner in ev.bound_box:
            world = ev.matrix_world @ Vector(corner)''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
