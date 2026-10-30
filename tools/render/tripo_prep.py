from PIL import Image
src = r"E:\dsh-pet-projects\dspet-main\docs\body\xiaoqi-main-v3-final.png"
im = Image.open(src)
print("原始:", im.mode, im.size)
rgba = im.convert("RGBA")
bbox = rgba.split()[3].getbbox() if im.mode == "RGBA" else None
print("alpha bbox:", bbox)
# 白底 + 裁掉多余留白（Tripo 更喜欢单一物体、贴边近）
flat = Image.new("RGB", rgba.size, (255, 255, 255))
flat.paste(rgba, mask=rgba.split()[3])
if bbox:
    pad = 24
    box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad),
           min(rgba.width, bbox[2]+pad), min(rgba.height, bbox[3]+pad))
    flat = flat.crop(box)
out = r"E:\dsh-pet-projects\build\tripo-in-white.png"
flat.save(out)
print("输出:", out, flat.size)
