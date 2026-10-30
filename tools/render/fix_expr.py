import io
P = r"E:\dsh-pet-projects\tools\make_expr_clips.py"
s = io.open(P, encoding="utf-8").read()

s = s.replace('''    base = key_white(Image.open(src))''',
'''    raw = Image.open(src)
    # 底下有投影/渐变，先裁掉下缘，避免抠出灰边
    raw = raw.crop((0, 0, raw.width, int(raw.height * 0.72)))
    base = key_white(raw)''')

s = s.replace('''def cover(img: Image.Image, zoom: float) -> Image.Image:
    """按 zoom 缩放到刚好盖住 640x360，取上部（脸在画面上三分之一）。"""
    s = max(W / img.width, H / img.height) * zoom
    nw, nh = max(W, int(img.width * s)), max(H, int(img.height * s))
    scaled = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - W) // 2
    y = max(0, int((nh - H) * 0.30))
    return scaled.crop((x, y, x + W, y + H))''',
'''def cover(img: Image.Image, zoom: float) -> Image.Image:
    """按 zoom 缩放到刚好装进 640x360（contain），居中偏上，保证猫耳和下巴都在画内。"""
    s = min(W / img.width, H / img.height) * zoom
    nw, nh = max(1, int(img.width * s)), max(1, int(img.height * s))
    scaled = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = (W - nw) // 2
    y = max(0, int((H - nh) * 0.25))
    canvas.alpha_composite(scaled, (x, y))
    return canvas''')

s = s.replace("        canvas = Image.new(\"RGBA\", (W, H), (0, 0, 0, 0))\n        canvas.alpha_composite(frame)\n        canvas.save",
              "        frame.save")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("改 contain + 裁剪")
