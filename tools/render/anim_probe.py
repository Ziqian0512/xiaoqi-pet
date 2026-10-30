import re, glob, os
for p in sorted(glob.glob(r"E:\dsh-pet-projects\body\anims\anim*\*.fbx")):
    data = open(p, "rb").read()
    ver = int.from_bytes(data[23:27], "little") if data.startswith(b"Kaydara FBX Binary") else 0
    has_bones = b"J_Bip" in data or b"mixamorig" in data or b"Bip01" in data
    has_anim = b"AnimationStack" in data or b"AnimCurveNode" in data
    print(os.path.basename(os.path.dirname(p)), "| %.1f MB" % (len(data)/1024/1024),
          "| v%d" % ver, "| 骨骼:", has_bones, "| 动画:", has_anim)
