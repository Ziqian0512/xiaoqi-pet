from PIL import Image
im = Image.open(r"E:\dsh-pet-projects\build\check-final.png")
h = im.getchannel("A").histogram(); total = im.width*im.height
print(im.size, "透明 %.1f%%" % (100.0*h[0]/total))
