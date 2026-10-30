from PIL import Image
src = r"E:\dsh-pet-projects\dspet-main\docs\body\xiaoqi-main-v3-final.png"
im = Image.open(src).convert("RGB")
w, h = im.size
px = im.load()
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(0, h, 2):
    for x in range(0, w, 2):
        r, g, b = px[x, y]
        if max(abs(255-r), abs(255-g), abs(255-b)) > 12:
            if x < minx: minx = x
            if y < miny: miny = y
            if x > maxx: maxx = x
            if y > maxy: maxy = y
print("内容框:", (minx, miny, maxx, maxy), im.size)
pad = 20
box = (max(0, minx-pad), max(0, miny-pad), min(w, maxx+pad), min(h, maxy+pad))
crop = im.crop(box)
out = r"E:\dsh-pet-projects\build\tripo-in-white.png"
crop.save(out)
print("输出:", out, crop.size)
