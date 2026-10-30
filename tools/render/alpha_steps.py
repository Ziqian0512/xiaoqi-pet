from PIL import Image
for n in "abcd":
    p = r"E:\dsh-pet-projects\build\t_%s.png" % n
    im = Image.open(p)
    if im.mode != "RGBA":
        print(n, "模式", im.mode, "无 alpha"); continue
    h = im.getchannel("A").histogram(); total = im.width*im.height
    print(n, "%.1f%% 透明" % (100.0*h[0]/total))
