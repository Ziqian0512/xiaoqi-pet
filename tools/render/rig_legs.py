import json, struct
p = r"E:\dsh-pet-projects\body\xiaoqi-rig.glb"
with open(p, "rb") as f:
    f.read(12); clen, ctype = struct.unpack("<II", f.read(8)); js = json.loads(f.read(clen))
nodes = js["nodes"]
joints = js["skins"][0]["joints"]
parent = {}
for idx, n in enumerate(nodes):
    for c in n.get("children", []):
        parent[c] = idx
names = {j: nodes[j].get("name") for j in joints}
# 腿链
kids = {}
for idx, n in enumerate(nodes):
    for c in n.get("children", []):
        kids.setdefault(idx, []).append(c)
hips = next(j for j in joints if nodes[j].get("name","").endswith("Hips"))
print("Hips 子节点:")
for c in kids.get(hips, []):
    print("  -", nodes[c].get("name"))
legs = [c for c in kids.get(hips, []) if "Leg" in nodes[c].get("name","") or "UpperLeg" in nodes[c].get("name","")]
print("\n腿根:", [nodes[c].get("name") for c in legs])
for leg in legs:
    def walk(i, d=0):
        print("  " * d + "└ " + nodes[i].get("name"))
        for c in kids.get(i, []):
            walk(c, d + 1)
    walk(leg)
# 有没有头发/裙子骨
extra = [nodes[j].get("name") for j in joints if not nodes[j].get("name","").startswith(("J_Bip","J_Adj","Root"))]
print("\n非标准骨（头发/裙/其他）:", extra)
