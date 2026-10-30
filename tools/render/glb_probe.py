import json, struct, sys
p = r"E:\Chrome_Download\xiaoqi.glb"
with open(p, "rb") as f:
    magic, ver, total = struct.unpack("<III", f.read(12))
    print("magic:", magic.to_bytes(4,"little"), "version:", ver, "size:", total)
    clen, ctype = struct.unpack("<II", f.read(8))
    js = json.loads(f.read(clen))
print("meshes:", len(js.get("meshes", [])), "| nodes:", len(js.get("nodes", [])),
      "| materials:", len(js.get("materials", [])), "| textures:", len(js.get("textures", [])))
print("skins:", len(js.get("skins", [])), "| animations:", len(js.get("animations", [])))
print("images:", [ (i.get("mimeType"), i.get("name","")) for i in js.get("images", []) ][:6])
print("mesh names:", [m.get("name") for m in js.get("meshes", [])][:10])
print("材质名:", [m.get("name") for m in js.get("materials", [])][:10])
if js.get("animations"):
    print("动画名:", [a.get("name") for a in js["animations"]][:10])
