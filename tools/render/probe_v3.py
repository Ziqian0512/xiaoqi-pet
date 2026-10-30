import json, struct
p = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-parts.glb"
raw = open(p, "rb").read()
with open(p, "rb") as f:
    f.read(12); clen,_ = struct.unpack("<II", f.read(8)); js = json.loads(f.read(clen))
print("MB:", round(len(raw)/1024/1024, 2))
print("meshes:", len(js.get("meshes", [])), "| nodes:", len(js.get("nodes", [])), "| materials:", len(js.get("materials", [])))
print("images:", [(i.get("mimeType")) for i in js.get("images", [])][:8])
acc = js["accessors"]
for i, m in enumerate(js.get("meshes", [])[:12]):
    tris = 0
    for pr in m.get("primitives", []):
        idx = pr.get("indices")
        if idx is not None:
            tris += acc[idx]["count"] // 3
    print("  mesh[%d] %-18s tris=%d" % (i, str(m.get("name"))[:18], tris))
