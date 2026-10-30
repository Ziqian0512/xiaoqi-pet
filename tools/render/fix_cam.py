import io, re
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

start = s.index("def setup_camera(")
end = s.index("def setup_render(")
new = '''def setup_camera(mins: Vector, maxs: Vector):
    """正交相机正对模特：脚落在 330/360 处，身高占 320px。"""
    height = maxs.z - mins.z
    width = maxs.x - mins.x
    S = height * (360.0 / 320.0)      # 画幅高度（世界单位）
    S = max(S, width * 1.15)          # 别裁到头发两侧
    cz = mins.z + (0.5 - 30.0 / 360.0) * S   # 脚离底边 30px
    cx = (mins.x + maxs.x) / 2

    cam_data = bpy.data.cameras.new("Cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = S
    cam = bpy.data.objects.new("Cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)

    depth = (maxs.y - mins.y)
    cam.location = Vector((cx, mins.y - max(depth, 1.0) * 2 - 1.0, cz))
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam
    return cam


'''
s = s[:start] + new + s[end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("相机重写")
