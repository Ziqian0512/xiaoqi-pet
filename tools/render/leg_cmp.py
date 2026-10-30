from PIL import Image
import glob
a = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-zero\f_*.png"))[0]
b = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-stand\f_*.png"))[0]
sheet = Image.new("RGB", (2*440, 480))
for i, f in enumerate((a, b)):
    im = Image.open(f).convert("RGBA")
    w,h = im.size
    crop = im.crop((int(w*0.24), int(h*0.12), int(w*0.76), int(h*0.96))).resize((440, 480), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    sheet.paste(Image.alpha_composite(bg, crop).convert("RGB"), (i*440, 0))
sheet.save(r"E:\dsh-pet-projects\build\leg-compare.png")
print("ok")
