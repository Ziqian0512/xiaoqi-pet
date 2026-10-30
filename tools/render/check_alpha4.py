from PIL import Image
for name, p in (("shenshen", r"E:\dsh-pet-projects\build\shen-a2.png"),
                ("mine", r"E:\dsh-pet-projects\build\mine-a2.png")):
    im = Image.open(p)
    print(name, im.mode, im.size, end="  ")
    if im.mode == "RGBA":
        h = im.getchannel("A").histogram(); total = im.width*im.height
        print("%.1f%% 透明" % (100.0*h[0]/total))
    else:
        print("无 alpha")
