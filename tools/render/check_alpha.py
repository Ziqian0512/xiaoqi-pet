from PIL import Image
im = Image.open(r"E:\dsh-pet-projects\build\check.png")
print("模式:", im.mode, "尺寸:", im.size)
if im.mode == "RGBA":
    a = im.getchannel("A")
    print("全透明像素占比: %.1f%%" % (100.0 * a.histogram()[0] / (im.width*im.height)))
else:
    print("没有 alpha 通道")
