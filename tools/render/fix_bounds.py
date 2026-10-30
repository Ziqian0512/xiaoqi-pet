import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
start = s.index("def bounds_of_meshes(")
end = s.index("def setup_camera(")
new = '''def bounds_of_meshes():
    """用实际顶点（world 空间）算包围盒——skinned mesh 的 bound_box 不可靠。"""
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    mins = Vector((1e9, 1e9, 1e9))
    maxs = Vector((-1e9, -1e9, -1e9))
    found = False
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH":
            continue
        ev = ob.evaluated_get(deps)
        me = ev.to_mesh()
        mw = ev.matrix_world
        for v in me.vertices:
            w = mw @ v.co
            mins = Vector((min(mins.x, w.x), min(mins.y, w.y), min(mins.z, w.z)))
            maxs = Vector((max(maxs.x, w.x), max(maxs.y, w.y), max(maxs.z, w.z)))
            found = True
        ev.to_mesh_clear()
    if not found:
        raise RuntimeError("场景里没有网格")
    return mins, maxs


'''
s = s[:start] + new + s[end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("包围盒改为逐顶点")
