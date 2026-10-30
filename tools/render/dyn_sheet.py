from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\sway-skirt\f_*.png"))
pick = [frames[i] for i in (0, 30, 60, 90)]
ims = []
for f in pick:
    im = Image.open(f).convert("RGBA").resize((320,180), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, im).convert("RGB"))
sheet = Image.new("RGB", (320*4, 180))
for i, im in enumerate(ims):
    sheet.paste(im, (i*320, 0))
sheet.save(r"E:\dsh-pet-projects\build\dynamics-sheet.png")
print("ok")
