import json, struct
p = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-rig.glb"
raw = open(p,"rb").read()
with open(p,"rb") as f:
    f.read(12); clen,_=struct.unpack("<II", f.read(8)); js=json.loads(f.read(clen))
print("MB:", round(len(raw)/1024/1024,2), "| skins:", len(js.get("skins",[])), "| anims:", len(js.get("animations",[])))
nodes=js.get("nodes",[])
for sk in js.get("skins",[]):
    j=sk.get("joints",[])
    print("joints:", len(j))
    print("前 10:", [nodes[x].get("name") for x in j[:10]])
    names=[nodes[x].get("name","") for x in j]
    print("有手指:", sum(1 for n in names if "Index" in n or "Thumb" in n or "Little" in n))
    print("头发/裙骨:", [n for n in names if "hair" in n.lower() or "skirt" in n.lower()][:6])
