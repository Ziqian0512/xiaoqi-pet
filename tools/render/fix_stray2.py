import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
start = s.index("def drop_strays(")
end = s.index("def import_model(")
new = '''def drop_strays():
    """只保留顶点最多的那个网格（Tripo 的 GLB 里偶尔混一个 Icosphere）。"""
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if len(meshes) <= 1:
        return
    meshes.sort(key=lambda o: len(o.data.vertices), reverse=True)
    keep = meshes[0]
    removed = []
    for ob in meshes[1:]:
        removed.append(ob.name)
        bpy.data.objects.remove(ob, do_unlink=True)
    if removed:
        print("删掉多余网格:", removed, "| 保留:", keep.name, len(keep.data.vertices), "顶点")


'''
s = s[:start] + new + s[end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("drop_strays 改为保留最大网格")
