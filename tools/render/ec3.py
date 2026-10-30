from PIL import Image
im = Image.open(r"E:\dsh-pet-projects\build\expr-frame3.png").convert("RGBA")
bg = Image.new("RGBA", im.size, (30, 33, 40, 255))
Image.alpha_composite(bg, im).convert("RGB").save(r"E:\dsh-pet-projects\build\expr-comp3.png")
print("ok")
