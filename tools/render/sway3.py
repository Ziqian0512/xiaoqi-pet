from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\sway2\f_*.png"))
pick = [frames[i] for i in (0, 30, 60, 90)]
ims = []
for f in pick:
    im = Image.open(f).convert("RGBA").crop((520, 0, 820, 240))
    bg = Image.new("RGBA", im.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, im).convert("RGB"))
sheet = Image.new("RGB", (300*4, 240))
for i, im in enumerate(ims):
    sheet.paste(im, (i*300, 0))
sheet.save(r"E:\dsh-pet-projects\build\sway3.png")
print("ok")
