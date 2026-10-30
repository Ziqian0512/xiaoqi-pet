from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\dance-skirt\f_*.png"))
pick = [frames[i] for i in (0, 40, 80, 120, 160, 200)]
ims = []
for f in pick:
    im = Image.open(f).convert("RGBA").resize((320, 180), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, (28, 32, 40, 255))
    ims.append(Image.alpha_composite(bg, im).convert("RGB"))
sheet = Image.new("RGB", (320*3, 180*2))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % 3)*320, (i // 3)*180))
sheet.save(r"E:\dsh-pet-projects\build\dance-skirt-sheet.png")
print("ok")
