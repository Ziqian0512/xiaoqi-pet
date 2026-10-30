"""检查 GLB 的蒙皮权重质量：有没有没绑的顶点、权重是否集中、每顶点骨骼数。"""

import json
import struct

import numpy as np

P = r"E:\dsh-pet-projects\body\xiaoqi-rig.glb"

with open(P, "rb") as f:
    f.read(12)
    clen, _ = struct.unpack("<II", f.read(8))
    js = json.loads(f.read(clen))
    blen, _ = struct.unpack("<II", f.read(8))
    bin_chunk = f.read(blen)

acc = js["accessors"]
views = js["bufferViews"]


def read_accessor(i: int) -> np.ndarray:
    a = acc[i]
    bv = views[a["bufferView"]]
    comp = {5120: np.int8, 5121: np.uint8, 5122: np.int16,
            5123: np.uint16, 5125: np.uint32, 5126: np.float32}[a["componentType"]]
    ncomp = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}[a["type"]]
    count = a["count"]
    offset = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    stride = bv.get("byteStride") or (np.dtype(comp).itemsize * ncomp)
    raw = np.frombuffer(bin_chunk, dtype=np.uint8,
                        count=stride * count, offset=offset).reshape(count, stride)
    data = raw[:, :np.dtype(comp).itemsize * ncomp].copy().view(comp).reshape(count, ncomp)
    return data.astype(np.float64) if comp is np.float32 else data


prim = js["meshes"][0]["primitives"][0]
attrs = prim["attributes"]
print("顶点数:", acc[attrs["POSITION"]]["count"])
print("有 JOINTS_0:", "JOINTS_0" in attrs, "| WEIGHTS_0:", "WEIGHTS_0" in attrs)

if "WEIGHTS_0" in attrs:
    w = read_accessor(attrs["WEIGHTS_0"])
    s = w.sum(axis=1)
    print("权重和：min=%.3f  max=%.3f" % (s.min(), s.max()))
    print("权重和 <0.99 的顶点: %d (%.2f%%)" % ((s < 0.99).sum(), 100 * (s < 0.99).mean()))
    print("权重和 ~0 的顶点（完全没绑）: %d" % (s < 0.01).sum())
    mx = w.max(axis=1)
    print("最大权重 <0.5（大概率糊）: %d (%.2f%%)" % ((mx < 0.5).sum(), 100 * (mx < 0.5).mean()))
    nz = (w > 0.001).sum(axis=1)
    print("每顶点参与骨骼数：平均 %.2f，最大 %d" % (nz.mean(), nz.max()))

if "JOINTS_0" in attrs:
    j = read_accessor(attrs["JOINTS_0"])
    used = np.unique(j[w > 0.001]) if "WEIGHTS_0" in attrs else np.unique(j)
    print("实际被用到的骨索引数:", len(used), "/", len(js["skins"][0]["joints"]))
