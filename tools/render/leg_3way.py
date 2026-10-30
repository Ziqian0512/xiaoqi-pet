from PIL import Image
import glob
files = [sorted(glob.glob(r"E:\dsh-pet-projects\build\%s\f_*.png" % d))[0] for d in ("v3-zero","v3-stand-mid","v3-stand")]
labels = ["原样(分开)","中(3°)","并拢(4.5°)"]
sheet = Image.new("RGB", (3*400, 470))
for i, f in enumerate(files):
    im = Image.open(f).convert("RGBA")
    w,h = im.size
    crop = im.crop((int(w*0.26), int(h*0.14), int(w*0.74), int(h*0.96))).resize((400, 470), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (28,32,40,255))
    sheet.paste(Image.alpha_composite(bg, crop).convert("RGB"), (i*400, 0))
sheet.save(r"E:\dsh-pet-projects\build\leg-3way.png")
print("ok")
