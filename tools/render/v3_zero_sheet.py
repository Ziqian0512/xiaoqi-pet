from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-zero\f_*.png"))
ims=[]
for i in (0, 48):
    im = Image.open(frames[i]).convert("RGBA")
    w,h = im.size
    crop = im.crop((int(w*0.22), int(h*0.28), int(w*0.78), int(h*0.92))).resize((420, 460), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (420*2, 460))
for i, im in enumerate(ims): sheet.paste(im, (i*420,0))
sheet.save(r"E:\dsh-pet-projects\build\v3-zero-sheet.png")
print("ok")
