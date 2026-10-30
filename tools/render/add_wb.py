import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

# 用 Workbench 平光试一版：颜色直接取贴图，不参与 PBR 打光
old_start = s.index("def setup_render(")
old_end = s.index("def setup_light(")
new = '''def setup_render():
    sc = bpy.context.scene
    engine = os.environ.get("XIAOQI_ENGINE", "eevee")
    if engine == "workbench":
        sc.render.engine = "BLENDER_WORKBENCH"
        sh = sc.display.shading
        sh.light = "FLAT"
        sh.color_type = "TEXTURE"
        sh.show_object_outline = False
        sh.show_specular_highlight = False
    else:
        for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                sc.render.engine = eng
                break
            except TypeError:
                continue
    sc.render.resolution_x = W * 2
    sc.render.resolution_y = H * 2
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.fps = 24
    try:
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
        sc.view_settings.exposure = 0.0
    except TypeError:
        pass


'''
s = s[:old_start] + new + s[old_end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了 workbench 模式")
