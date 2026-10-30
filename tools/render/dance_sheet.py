from PIL import Image
ims = []
for n in (1, 40, 80, 120, 160, 200):
    im = Image.open(r"E:\dsh-pet-projects\build\dance-anim\f_%04d.png" % n).convert("RGBA")
    bg = Image.new("RGBA", im.size, (28, 32, 40, 255))
    ims.append(Image.alpha_composite(bg, im).convert("RGB").resize((320, 180)))
sheet = Image.new("RGB", (320*3, 180*2))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % 3)*320, (i // 3)*180))
sheet.save(r"E:\dsh-pet-projects\build\dance-sheet.png")
print("拼图 ok")
