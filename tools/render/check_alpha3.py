from PIL import Image
im = Image.open(r"E:\dsh-pet-projects\build\check3.png")
a = im.getchannel("A"); h = a.histogram()
total = im.width*im.height
print("模式:", im.mode, im.size)
print("全透明: %.1f%%  不透明: %.1f%%" % (100.0*h[0]/total, 100.0*h[255]/total))
