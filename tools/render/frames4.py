from PIL import Image
for n in (1, 30, 60, 90):
    im = Image.open(r"E:\dsh-pet-projects\build\idle-anim\f_%04d.png" % n).convert("RGBA")
    bg = Image.new("RGBA", im.size, (28, 32, 40, 255))
    Image.alpha_composite(bg, im).convert("RGB").save(r"E:\dsh-pet-projects\build\anim-f%d.png" % n)
print("拼了 4 帧对比")
