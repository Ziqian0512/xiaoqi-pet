from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-fix\f_*.png"))
idx = [0, 20, 40, 60, 80]
ims = []
for i in idx:
    im = Image.open(frames[i]).convert("RGBA")
    w, h = im.size
    crop = im.crop((int(w*0.28), int(h*0.40), int(w*0.72), int(h*0.80))).resize((360, 330), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (360*5, 330))
for i, im in enumerate(ims):
    sheet.paste(im, (i*360, 0))
sheet.save(r"E:\dsh-pet-projects\build\v3-arm-frames.png")
print("ok")
