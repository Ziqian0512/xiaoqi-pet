from PIL import Image
im = Image.open(r"E:\dsh-pet-projects\build\idle3d-check.png")
a = im.getchannel("A"); h = a.histogram(); t = im.width*im.height
print(im.size, "透明 %.1f%%" % (100.0*h[0]/t))
bg = Image.new("RGBA", im.size, (28, 32, 40, 255))
Image.alpha_composite(bg, im).convert("RGB").save(r"E:\dsh-pet-projects\build\idle3d-comp.png")
