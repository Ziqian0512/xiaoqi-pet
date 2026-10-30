from PIL import Image
import glob
f = sorted(glob.glob(r"E:\dsh-pet-projects\build\v2-static\f_*.png"))[0]
im = Image.open(f).convert("RGBA").resize((320,180), Image.LANCZOS)
bg = Image.new("RGBA", im.size, (28,32,40,255))
Image.alpha_composite(bg, im).convert("RGB").resize((640,360)).save(r"E:\dsh-pet-projects\build\v2-static-comp.png")
print("ok")
