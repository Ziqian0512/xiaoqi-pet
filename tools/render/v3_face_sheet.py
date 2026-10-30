from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-face\f_*.png"))
ims=[]
for i in (0, 3, 6, 30):
    im = Image.open(frames[i]).convert("RGBA")
    w,h = im.size
    crop = im.crop((int(w*0.40), int(h*0.12), int(w*0.60), int(h*0.30))).resize((300, 270), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (300*4, 270))
for i, im in enumerate(ims): sheet.paste(im, (i*300,0))
sheet.save(r"E:\dsh-pet-projects\build\v3-face-sheet.png")
print("ok")
