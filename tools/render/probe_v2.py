import json, struct
p = r"E:\dsh-pet-projects\body\v2\xiaoqi-v2-raw.glb"
with open(p, "rb") as f:
    f.read(12); clen,_ = struct.unpack("<II", f.read(8)); js = json.loads(f.read(clen))
print("meshes:", len(js.get("meshes", [])), "| nodes:", len(js.get("nodes", [])),
      "| skins:", len(js.get("skins", [])), "| animations:", len(js.get("animations", [])))
print("materials:", [m.get("name") for m in js.get("materials", [])])
print("images:", [(i.get("mimeType"), i.get("name","")) for i in js.get("images", [])][:6])
tot = 0
for m in js.get("meshes", []):
    for pr in m.get("primitives", []):
        idx = pr.get("indices")
        if idx is not None:
            tot += js["accessors"][idx]["count"] // 3
print("三角面总数:", tot)
