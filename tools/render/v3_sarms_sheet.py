from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-sarms\f_*.png"))
ims=[]
for i in (0, 24, 48, 72):
    im = Image.open(frames[i]).convert("RGBA")
    w,h = im.size
    crop = im.crop((int(w*0.22), int(h*0.30), int(w*0.78), int(h*0.90))).resize((360, 400), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (360*4, 400))
for i, im in enumerate(ims): sheet.paste(im, (i*360,0))
sheet.save(r"E:\dsh-pet-projects\build\v3-sarms-sheet.png")
print("ok")
