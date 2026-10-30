from PIL import Image
import glob
files = sorted(glob.glob(r"E:\dsh-pet-projects\build\lit-test\f_*.png"))
print("帧数:", len(files))
im = Image.open(files[20]).convert("RGBA").resize((640, 360), Image.LANCZOS)
bg = Image.new("RGBA", im.size, (28, 32, 40, 255))
Image.alpha_composite(bg, im).convert("RGB").save(r"E:\dsh-pet-projects\build\lit-comp.png")
print(im.size)
