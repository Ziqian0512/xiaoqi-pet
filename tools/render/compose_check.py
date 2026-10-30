from PIL import Image
im = Image.open(r"E:\dsh-pet-projects\build\mine-a2.png").convert("RGBA")
# 贴在深色格纹背景上，检查边缘和透明
bg = Image.new("RGBA", im.size, (40, 44, 52, 255))
for y in range(0, im.height, 32):
    for x in range(0, im.width, 32):
        if (x // 32 + y // 32) % 2 == 0:
            bg.paste((58, 62, 72, 255), (x, y, min(x+32, im.width), min(y+32, im.height)))
out = Image.alpha_composite(bg, im)
out.convert("RGB").save(r"E:\dsh-pet-projects\build\composite.png")
print("ok", out.size)
