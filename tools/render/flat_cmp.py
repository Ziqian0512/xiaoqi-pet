from PIL import Image
import glob
def comp(src, out, n):
    f = sorted(glob.glob(src + r"\f_*.png"))[n]
    im = Image.open(f).convert("RGBA").resize((320,180), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, (28,32,40,255))
    Image.alpha_composite(bg, im).convert("RGB").save(out)
comp(r"E:\dsh-pet-projects\build\dance-flat", r"E:\dsh-pet-projects\build\d-flat.png", 100)
comp(r"E:\dsh-pet-projects\build\idle2-flat", r"E:\dsh-pet-projects\build\i2-flat.png", 40)
sheet = Image.new("RGB", (640,180))
sheet.paste(Image.open(r"E:\dsh-pet-projects\build\d-flat.png"), (0,0))
sheet.paste(Image.open(r"E:\dsh-pet-projects\build\i2-flat.png"), (320,0))
sheet.save(r"E:\dsh-pet-projects\build\flat-compare.png")
print("ok")
