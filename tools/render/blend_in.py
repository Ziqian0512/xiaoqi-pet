import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
if "open_mainfile" not in s:
    s = s.replace('''def import_model(path: str):
    if path.lower().endswith((".glb", ".gltf")):''',
'''def import_model(path: str):
    if path.lower().endswith(".blend"):
        bpy.ops.wm.open_mainfile(filepath=path)
        return
    if path.lower().endswith((".glb", ".gltf")):''')
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("支持 .blend 输入")
