import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
start = s.index("def drop_strays(")
end = s.index("def import_model(")
new = '''def drop_strays():
    """只删掉垃圾网格（顶点极少），分件模型一律保留。"""
    removed = []
    for ob in list(bpy.context.scene.objects):
        if ob.type == "MESH" and len(ob.data.vertices) < 20:
            removed.append(ob.name)
            bpy.data.objects.remove(ob, do_unlink=True)
    if removed:
        print("删掉垃圾网格:", removed)


'''
s = s[:start] + new + s[end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("drop_strays 改为只删极小网格")
