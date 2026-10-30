from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-face2\f_*.png"))
ims=[]
for i in (0, 2, 4, 40):
    im = Image.open(frames[i]).convert("RGBA")
    w,h = im.size
    crop = im.crop((int(w*0.40), int(h*0.10), int(w*0.60), int(h*0.30))).resize((310, 310), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    ims.append(Image.alpha_composite(bg, crop).convert("RGB"))
sheet = Image.new("RGB", (310*4, 310))
for i, im in enumerate(ims): sheet.paste(im, (i*310,0))
sheet.save(r"E:\dsh-pet-projects\build\v3-face2-sheet.png")
print("ok")
