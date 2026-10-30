import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
start = s.index("def setup_camera(")
end = s.index("def setup_render(")
new = '''def setup_camera(mins: Vector, maxs: Vector):
    """正交相机正对模特。

    Blender 的 ortho_scale 说的是**较长边**（这里 640 宽），
    所以竖直可见高度 = ortho_scale * (H/W)。
    """
    height = maxs.z - mins.z
    width = maxs.x - mins.x

    vspan = height * (360.0 / 320.0)          # 竖直可见范围（身高占 320px）
    S = vspan * (W / H)                       # 换算成 ortho_scale（横向）
    if width * 1.15 > S * (H / W) * 0 + S:    # 横向太宽就放大画幅
        S = max(S, width * 1.15 * (W / H))

    cz = mins.z + (0.5 - 30.0 / 360.0) * vspan
    cx = (mins.x + maxs.x) / 2

    cam_data = bpy.data.cameras.new("Cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = S
    cam = bpy.data.objects.new("Cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)

    depth = max(maxs.y - mins.y, 0.2)
    cam.location = Vector((cx, mins.y - depth * 3 - 1.0, cz))
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam
    return cam


'''
s = s[:start] + new + s[end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("相机按长边重新算")
