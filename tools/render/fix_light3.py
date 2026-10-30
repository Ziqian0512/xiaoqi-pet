import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('''        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Medium High Contrast"''',
'''        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
        sc.view_settings.exposure = -0.15''')
s = s.replace('''    area("Key", (1.6, -2.2, 2.2), (math.radians(50), 0, math.radians(35)), 90, 2.5)''',
'''    area("Key", (1.6, -2.2, 2.2), (math.radians(50), 0, math.radians(35)), 150, 2.0)''')
s = s.replace('''        bg.inputs[1].default_value = 0.10''', '''        bg.inputs[1].default_value = 0.06''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("改 Standard + 更硬的主光")
