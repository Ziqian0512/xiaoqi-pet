import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

s = s.replace('''def import_model(path: str):''',
'''def drop_strays():
    """删掉不属于角色的多余网格（Tripo 的 GLB 里混了一个 Icosphere）。"""
    keep = set()
    for ob in bpy.context.scene.objects:
        if ob.type == "MESH" and ob.parent and ob.parent.type == "ARMATURE":
            keep.add(ob.name)
        elif ob.type == "MESH":
            has_arm_mod = any(m.type == "ARMATURE" for m in ob.modifiers)
            if has_arm_mod:
                keep.add(ob.name)
    removed = []
    for ob in list(bpy.context.scene.objects):
        if ob.type == "MESH" and ob.name not in keep:
            removed.append(ob.name)
            bpy.data.objects.remove(ob, do_unlink=True)
    if removed:
        print("删掉多余网格:", removed)


def import_model(path: str):''')

s = s.replace('''    import_model(SRC)
    mins, maxs = bounds_of_meshes()''',
'''    import_model(SRC)
    drop_strays()
    mins, maxs = bounds_of_meshes()''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了清理多余网格")
