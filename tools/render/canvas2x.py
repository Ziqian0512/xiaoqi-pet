import io
P = r"E:\dsh-pet-projects\xiaoqi-pet\pet\catalog.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('''CANVAS_W = 640
CANVAS_H = 360

# 脚底在画布内的 y 坐标（与母版一致：640×360 画布脚底 y=330）
FEET_Y = 330 / 360 * CANVAS_H  # = 330''',
'''# 画布提到 1280×720（2 倍），这样放大显示时不会先糊 —— 2026-10-31
CANVAS_W = 1280
CANVAS_H = 720

# 脚底在画布内的 y 坐标（保持原来的 330/360 比例）
FEET_Y = 330 / 360 * CANVAS_H  # = 660''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("画布改为 1280x720:", "CANVAS_W = 1280" in io.open(P, encoding="utf-8").read())
