from PIL import Image
import glob
sheet = Image.new("RGB", (3*380, 300))
for i, ax in enumerate("xyz"):
    f = sorted(glob.glob(r"E:\dsh-pet-projects\build\raise-%s\f_*.png" % ax))[0]
    im = Image.open(f).convert("RGBA").resize((380, 300), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, (28,32,40,255))
    sheet.paste(Image.alpha_composite(bg, im).convert("RGB"), (i*380, 0))
sheet.save(r"E:\dsh-pet-projects\build\raise-axes.png")
print("ok")
