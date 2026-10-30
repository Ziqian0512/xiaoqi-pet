import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

# 1) 2 倍分辨率渲染再缩小（抗锯齿）
s = s.replace('''    sc.render.resolution_x = W
    sc.render.resolution_y = H''',
'''    sc.render.resolution_x = W * 2
    sc.render.resolution_y = H * 2''')

# 2) 重新打光：弱环境 + 主光 + 侧补光 + 轮廓光
start = s.index("def setup_light(")
end = s.index("def add_procedural_idle(")
new = '''def setup_light():
    """三点光：主光偏左前、补光右侧弱、轮廓光在后上方；环境光压低。"""
    def area(name, loc, rot, energy, size):
        d = bpy.data.lights.new(name, type="AREA")
        d.energy = energy
        d.size = size
        ob = bpy.data.objects.new(name, d)
        ob.location = loc
        ob.rotation_euler = rot
        bpy.context.scene.collection.objects.link(ob)
        return ob

    area("Key", (1.6, -2.2, 2.2), (math.radians(50), 0, math.radians(35)), 90, 2.5)
    area("Fill", (-2.0, -1.6, 1.2), (math.radians(70), 0, math.radians(-55)), 25, 3.0)
    area("Rim", (0.4, 1.8, 2.6), (math.radians(120), 0, math.radians(200)), 70, 2.0)

    world = bpy.data.worlds.new("W")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.55, 0.6, 0.7, 1)
        bg.inputs[1].default_value = 0.10
    bpy.context.scene.world = world

    sc = bpy.context.scene
    try:
        sc.eevee.use_gtao = True          # 环境光遮蔽：让褶皱有层次
    except AttributeError:
        pass
    try:
        sc.eevee.taa_render_samples = 32
    except AttributeError:
        pass


'''
s = s[:start] + new + s[end:]

# 3) 色彩管理：AgX + 轻微提对比
s = s.replace('''        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"''',
'''        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Medium High Contrast"''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("光照 + 分辨率 + 色彩管理都改了")
