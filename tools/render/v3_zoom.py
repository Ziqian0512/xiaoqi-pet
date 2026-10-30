from PIL import Image
import glob
frames = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-fix\f_*.png"))
im = Image.open(frames[0]).convert("RGBA")
print("size", im.size)
# 腰部区域放大
w,h = im.size
crop = im.crop((int(w*0.30), int(h*0.42), int(w*0.70), int(h*0.78)))
bg = Image.new("RGBA", crop.size, (28,32,40,255))
comp = Image.alpha_composite(bg, crop).convert("RGB")
comp = comp.resize((comp.width*2, comp.height*2), Image.LANCZOS)
comp.save(r"E:\dsh-pet-projects\build\v3-waist-zoom.png")
print("ok", comp.size)
