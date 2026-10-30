"""从 v3 GLB 里导出所有贴图，并找出"脸"那张（head 材质）。"""

import json
import struct

import os

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-parts.glb"
OUT = r"E:\dsh-pet-projects\body\v3\textures"
os.makedirs(OUT, exist_ok=True)

with open(SRC, "rb") as f:
    f.read(12)
    clen, _ = struct.unpack("<II", f.read(8))
    js = json.loads(f.read(clen))
    blen, _ = struct.unpack("<II", f.read(8))
    blob = f.read(blen)

images = js.get("images", [])
views = js["bufferViews"]
print("images:", len(images))

# 材质 → baseColor 贴图索引
mat_tex = {}
for m in js.get("materials", []):
    pbr = m.get("pbrMetallicRoughness") or {}
    bct = pbr.get("baseColorTexture") or {}
    idx = bct.get("index")
    if idx is not None:
        tex = js["textures"][idx]
        mat_tex[m.get("name", "?")] = tex.get("source")

for i, img in enumerate(images):
    bv = views[img["bufferView"]]
    start = bv.get("byteOffset", 0)
    length = bv["byteLength"]
    ext = "jpg" if "jpeg" in (img.get("mimeType") or "") else "png"
    name = img.get("name") or ("img%d" % i)
    path = os.path.join(OUT, "%02d_%s.%s" % (i, name.replace("/", "_")[:40], ext))
    with open(path, "wb") as fo:
        fo.write(blob[start:start + length])
    print("  %02d %-46s %.0f KB  <- 材质 %s" %
          (i, name, length / 1024,
           [mn for mn, ti in mat_tex.items() if ti == i][:2]))
