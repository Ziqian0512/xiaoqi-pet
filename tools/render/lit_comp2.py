from PIL import Image
import glob
files = sorted(glob.glob(r"E:\dsh-pet-projects\build\lit-test\f_*.png"))
im = Image.open(files[0]).convert("RGBA").resize((640, 360), Image.LANCZOS)
bg = Image.new("RGBA", im.size, (28, 32, 40, 255))
Image.alpha_composite(bg, im).convert("RGB").save(r"E:\dsh-pet-projects\build\lit-comp.png")
print("ok", Image.open(files[0]).size)
