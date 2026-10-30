from PIL import Image
import glob, os
f = sorted(glob.glob(r"E:\dsh-pet-projects\build\v2-test\f_*.png"))[0]
im = Image.open(f).convert("RGBA").resize((640,360), Image.LANCZOS)
bg = Image.new("RGBA", im.size, (28,32,40,255))
Image.alpha_composite(bg, im).convert("RGB").save(r"E:\dsh-pet-projects\build\v2-desktop.png")
# 源图缩到同样身高（320px）并排放
src = Image.open(r"E:\dsh-pet-projects\body\v2\..\v2\..\v2\xiaoqi-v2-raw.glb") if False else None
print("ok")
