from PIL import Image
import glob
f = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-face\f_*.png"))[0]
im = Image.open(f).convert("RGBA").resize((640,360), Image.LANCZOS)
bg = Image.new("RGBA", im.size, (28,32,40,255))
Image.alpha_composite(bg, im).convert("RGB").save(r"E:\dsh-pet-projects\build\v3-face-full.png")
print("ok")
