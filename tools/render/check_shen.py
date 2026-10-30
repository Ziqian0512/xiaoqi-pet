from PIL import Image
for name, p in (("shenshen", r"E:\dsh-pet-projects\build\shen-alpha.png"),):
    im = Image.open(p)
    print(name, im.mode, im.size)
    if im.mode == "RGBA":
        h = im.getchannel("A").histogram(); total = im.width*im.height
        print("  %.1f%% 透明" % (100.0*h[0]/total))
