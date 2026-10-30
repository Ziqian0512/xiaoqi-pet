from PIL import Image
import glob
f = sorted(glob.glob(r"E:\dsh-pet-projects\build\v2-test\f_*.png"))[0]
im = Image.open(f).convert("RGBA").resize((640,360), Image.LANCZOS)
bg = Image.new("RGBA", im.size, (28,32,40,255))
comp = Image.alpha_composite(bg, im).convert("RGB")
comp.save(r"E:\dsh-pet-projects\build\v2-desktop.png")
# 对比：源图缩到 320px 高
src = Image.open(r"C:\Users\10943\.dsh\attachments\v1\objects\1e\1e3ca55ea3e65c0be4201faea4b833ebf017e798dafa2eeef963e81b989613fe")
h = 320
w = int(src.width * h / src.height)
src_small = src.convert("RGB").resize((w, h), Image.LANCZOS)
sheet = Image.new("RGB", (640 + w + 20, 360), (28,32,40))
sheet.paste(comp, (0,0))
sheet.paste(src_small, (660, 20))
sheet.save(r"E:\dsh-pet-projects\build\v2-vs-src.png")
print("ok", im.size, src_small.size)
