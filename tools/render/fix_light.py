import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

s = s.replace('''    light_data.energy = 400''', '''    light_data.energy = 120''')
s = s.replace('''    fill_data.energy = 120''', '''    fill_data.energy = 40''')
s = s.replace('''        bg.inputs[1].default_value = 0.5''', '''        bg.inputs[1].default_value = 0.25''')

if "view_settings.view_transform" not in s:
    s = s.replace('''    sc.render.fps = 24''',
'''    sc.render.fps = 24
    try:
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
    except TypeError:
        pass''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("曝光调整")
