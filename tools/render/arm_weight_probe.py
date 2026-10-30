"""查袖子/手臂的顶点主要绑在哪根骨上——判断"抬手不动"是不是权重问题。"""

import math

import bpy

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-staticarms.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()

mesh = next(o for o in bpy.context.scene.objects if o.type == "MESH" and len(o.data.vertices) > 100)
mw = mesh.matrix_world
gname = {g.index: g.name for g in mesh.vertex_groups}

from collections import Counter
counter = Counter()
samples = []
for v in mesh.data.vertices:
    p = mw @ v.co
    # 袖子/上臂区域：侧面、腰以上
    if abs(p.x) > 0.14 and 0.42 < p.z < 0.62:
        dom = ""
        best = 0.0
        for g in v.groups:
            if g.weight > best:
                best = g.weight
                dom = gname.get(g.group, "")
        counter[dom] += 1
        if len(samples) < 6:
            samples.append((round(p.x, 3), round(p.z, 3), dom, round(best, 2)))

print("手臂/袖口区域顶点主导骨分布：")
for name, n in counter.most_common(8):
    print("   %-24s %d" % (name, n))
print("样例:", samples)
