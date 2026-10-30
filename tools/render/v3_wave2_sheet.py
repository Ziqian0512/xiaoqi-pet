from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-wave2\f_*.png"))
ims=[]
for i in (0, 10, 20, 30, 40, 55):
    im = Image.open(frames[i]).convert("RGBA")
    w,h = im.size
    crop = im.crop((int(w*0.20), int(h*0.20), int(w*0.80), int(h*0.95))).resize((300, 430), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (300*6, 430))
for i, im in enumerate(ims): sheet.paste(im, (i*300,0))
sheet.save(r"E:\dsh-pet-projects\build\v3-wave2-sheet.png")
print("ok")
