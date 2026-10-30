from PIL import Image
import glob
sheet = Image.new("RGB", (3*400, 300))
for i, ax in enumerate("xyz"):
    f = sorted(glob.glob(r"E:\dsh-pet-projects\build\arm-%s\f_*.png" % ax))[0]
    im = Image.open(f).convert("RGBA").resize((400, 300), Image.LANCZOS)
    # 只要人，缩到 300 高
    bg = Image.new("RGBA", im.size, (28,32,40,255))
    sheet.paste(Image.alpha_composite(bg, im).convert("RGB"), (i*400, 0))
sheet.save(r"E:\dsh-pet-projects\build\arm-axes.png")
print("ok")
