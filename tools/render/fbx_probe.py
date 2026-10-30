import re
p = r"E:\dsh-pet-projects\body\tripo-fbx\tripo_convert_eae502a6-29fe-4f36-8b6f-b6fa354db956.fbx"
data = open(p, "rb").read()
print("大小 MB:", round(len(data)/1024/1024, 2))
head = data[:64]
print("头部:", head[:24])
# FBX 头部（可能是压缩的）
if head.startswith(b"Kaydara FBX Binary"):
    import struct
    ver = struct.unpack("<I", data[23:27])[0]
    print("FBX binary 版本:", ver)
    # 粗查骨骼名
    names = set(re.findall(rb"(mixamorig[:_][A-Za-z_]+|J_Bip_[CRL]_\w+|Root|Hips|Spine)", data[:2000000]))
    print("骨骼名样本:", [n.decode() for n in list(names)[:8]])
    print("含 Mixamorig:", b"mixamorig" in data.lower(), "| 含 J_Bip:", b"J_Bip" in data)
else:
    print("不是标准 FBX 二进制头，可能是 ASCII 或压缩")
