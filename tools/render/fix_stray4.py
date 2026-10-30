import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
start = s.index("def drop_strays(")
end = s.index("def import_model(")
new = '''def drop_strays():
    """删掉不属于角色的网格（Tripo 偶尔塞一个 Icosphere）。

    规则：有骨架修改器、或父级是骨架、或顶点数 > 200 且不是球状杂物 → 保留。
    简单可靠：保留「有 Armature 修改器」或「父级为 ARMATURE」的网格；
    若一个都没有（未绑定模型），则保留顶点最多的那个。
    """
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    keep = set()
    if arm is not None:
        for ob in meshes:
            if ob.parent is arm or any(m.type == "ARMATURE" for m in ob.modifiers):
                keep.add(ob.name)
    if not keep and meshes:
        meshes.sort(key=lambda o: len(o.data.vertices), reverse=True)
        keep.add(meshes[0].name)
    removed = []
    for ob in meshes:
        if ob.name not in keep:
            removed.append(ob.name)
            bpy.data.objects.remove(ob, do_unlink=True)
    if removed:
        print("删掉非角色网格:", removed, "| 保留", len(keep), "个")


'''
s = s[:start] + new + s[end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("取景逻辑修好")
