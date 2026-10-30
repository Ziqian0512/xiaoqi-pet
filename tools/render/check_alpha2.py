from PIL import Image
im = Image.open(r"E:\dsh-pet-projects\build\check2.png")
print("模式:", im.mode, "尺寸:", im.size)
a = im.getchannel("A")
h = a.histogram()
print("全透明: %.1f%%  不透明: %.1f%%" % (100.0*h[0]/(im.width*im.height), 100.0*h[255]/(im.width*im.height)))
im2 = im.convert("RGBA")
im2.save(r"E:\dsh-pet-projects\build\check2-vis.png")
