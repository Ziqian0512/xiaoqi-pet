import json, struct
p = r"E:\dsh-pet-projects\body\xiaoqi-rig.glb"
with open(p, "rb") as f:
    magic, ver, total = struct.unpack("<III", f.read(12))
    clen, ctype = struct.unpack("<II", f.read(8))
    js = json.loads(f.read(clen))
print("meshes:", len(js.get("meshes", [])), "nodes:", len(js.get("nodes", [])),
      "skins:", len(js.get("skins", [])), "animations:", len(js.get("animations", [])))
nodes = js.get("nodes", [])
for si, sk in enumerate(js.get("skins", [])):
    joints = sk.get("joints", [])
    print("skin[%d] joints=%d" % (si, len(joints)))
    names = [nodes[j].get("name", "?") for j in joints[:8]]
    print("  前 8 个骨骼:", names)
    # 打印层级（从骨骼根开始）
    parent = {}
    for idx, n in enumerate(nodes):
        for c in n.get("children", []):
            parent[c] = idx
    roots = [j for j in joints if parent.get(j) not in joints]
    def walk(i, depth=0, limit=[0]):
        if limit[0] > 40: return
        limit[0] += 1
        print("  " * depth + "- " + str(nodes[i].get("name")))
        for c in nodes[i].get("children", []):
            walk(c, depth + 1, limit)
    for r in roots[:2]:
        walk(r)
if js.get("animations"):
    print("动画:", [(a.get("name"), len(a.get("channels", []))) for a in js["animations"]])
