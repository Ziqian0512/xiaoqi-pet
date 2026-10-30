import glob, os
for p in glob.glob(r"E:\dsh-pet-projects\body\anims\anim5\**\*.fbx", recursive=True) + glob.glob(r"E:\dsh-pet-projects\body\anims\anim5\**\*.glb", recursive=True):
    data = open(p, "rb").read()
    print(os.path.basename(p), "| %.1f MB" % (len(data)/1024/1024))
    for kw in (b"AnimationStack", b"AnimCurveNode", b"J_Bip", b"mixamorig", b"Take", b"Armature"):
        if kw in data:
            print("   含有:", kw.decode())
