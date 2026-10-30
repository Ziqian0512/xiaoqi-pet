from PIL import Image
import glob
f = sorted(glob.glob(r"E:\dsh-pet-projects\build\v3-stand-anim\f_*.png"))[0]
im = Image.open(f).convert("RGBA")
w,h = im.size
# 头部区域
crop = im.crop((int(w*0.38), int(h*0.10), int(w*0.62), int(h*0.36)))
bg = Image.new("RGBA", crop.size, (28,32,40,255))
comp = Image.alpha_composite(bg, crop).convert("RGB")
comp = comp.resize((comp.width*3, comp.height*3), Image.LANCZOS)
comp.save(r"E:\dsh-pet-projects\build\v3-head-zoom.png")
print(comp.size)
