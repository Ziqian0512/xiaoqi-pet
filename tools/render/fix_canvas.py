import io
P = r"E:\dsh-pet-projects\tools\key_anchor.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('CANVAS = (640, 960)', 'CANVAS = (640, 360)')
s = s.replace('FEET_MARGIN = 8          # 脚底离画布底部多少像素', 'FEET_Y = 330             # 与 catalog.FEET_Y 对齐')
s = s.replace('TOP_MARGIN = 12', 'TOP_MARGIN = 8')
s = s.replace('''    max_w = cw - 24
    max_h = ch - TOP_MARGIN - FEET_MARGIN''', '''    max_w = cw - 24
    max_h = FEET_Y - TOP_MARGIN''')
s = s.replace('''    x = (cw - new[0]) // 2
    y = ch - FEET_MARGIN - new[1]''', '''    x = (cw - new[0]) // 2
    y = FEET_Y - new[1]''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("改画布 640x360, 脚 y=330")
