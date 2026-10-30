from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\sway-test\f_*.png"))
print("帧数", len(frames))
pick = [frames[i] for i in (0, 30, 60, 90)]
ims = []
for f in pick:
    im = Image.open(f).convert("RGBA")
    crop = im.crop((180, 0, 460, 200))   # 头部区域
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (280*4, 200))
for i, im in enumerate(ims):
    sheet.paste(im, (i*280, 0))
sheet.save(r"E:\dsh-pet-projects\build\sway-sheet.png")
print("ok")
