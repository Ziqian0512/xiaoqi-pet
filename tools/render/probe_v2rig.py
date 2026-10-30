import json, struct
p = r"E:\dsh-pet-projects\body\v2\xiaoqi-v2-rig.glb"
with open(p, "rb") as f:
    f.read(12); clen,_ = struct.unpack("<II", f.read(8)); js = json.loads(f.read(clen))
print("MB:", round(len(open(p,"rb").read())/1024/1024, 2))
print("meshes:", len(js.get("meshes", [])), "| skins:", len(js.get("skins", [])), "| anims:", len(js.get("animations", [])))
nodes = js.get("nodes", [])
for sk in js.get("skins", []):
    js_ = sk.get("joints", [])
    print("joints:", len(js_), "| 前 6:", [nodes[x].get("name") for x in js_[:6]])
