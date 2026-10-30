from PIL import Image
p = r"E:\dsh-pet-projects\dspet-main\docs\body\xiaoqi-expr-angry-clean.png"
im = Image.open(p).convert("RGBA")
w, h = im.size
px = im.load()
print("尺寸", im.size)
for (x, y) in [(2,2),(w-3,2),(2,h-3),(w-3,h-3),(w//2,3)]:
    print((x,y), px[x,y])
