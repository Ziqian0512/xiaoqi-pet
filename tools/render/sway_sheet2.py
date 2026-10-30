from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\sway-test\f_*.png"))
pick = [frames[i] for i in (0, 30, 60, 90)]
ims = []
for f in pick:
    im = Image.open(f).convert("RGBA")
    print(f, im.size)
    crop = im.crop((520, 0, 820, 240))
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (300*4, 240))
for i, im in enumerate(ims):
    sheet.paste(im, (i*300, 0))
sheet.save(r"E:\dsh-pet-projects\build\sway-sheet2.png")
print("ok")
