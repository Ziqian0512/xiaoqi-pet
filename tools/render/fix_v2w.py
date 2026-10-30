import io
P = r"E:\dsh-pet-projects\tools\v2_bones.py"
s = io.open(P, encoding="utf-8").read()

start = s.index("# ---------- 刷权重 ----------")
end = s.index('bpy.ops.wm.save_as_mainfile(filepath=OUT)')
new = '''# ---------- 刷权重（按骨架主导骨判定头发，避免抓到手臂）----------
def vg(name):
    return mesh.vertex_groups.get(name) or mesh.vertex_groups.new(name=name)


for names in hair_names.values():
    for n in names:
        vg(n)
for _i, a, c in skirt_names:
    vg(a)
    vg(c)

gidx = {g.index: g.name for g in mesh.vertex_groups}
head_vg = mesh.vertex_groups.get("J_Bip_C_Head")
hips_vg = mesh.vertex_groups.get("J_Bip_C_Hips")

face_w = 0.105            # 脸的半宽
top_z = head_h.z + 0.08   # 头顶以上
hair_n = skirt_n = 0
for v in mesh.data.vertices:
    p = mw @ v.co
    r = math.hypot(p.x, p.y)

    # 主导骨
    dom, dom_w = "", 0.0
    for g in v.groups:
        if g.weight > dom_w:
            dom_w = g.weight
            dom = gidx.get(g.group, "")

    # 头发：主导骨是 Head，且不在脸中央（两侧或头顶）
    if dom == "J_Bip_C_Head" and (abs(p.x) > face_w or p.z > top_z):
        side = "L" if p.x > 0 else "R"
        names = hair_names[side]
        t = max(0.0, min(1.0, (zmax - p.z) / (zmax - head_h.z)))
        seg = min(HAIR_SEG - 1, int(t * HAIR_SEG))
        frac = t * HAIR_SEG - seg
        vg(names[seg]).add([v.index], 0.7 * (1 - frac) + 0.3, "REPLACE")
        if seg + 1 < HAIR_SEG:
            vg(names[seg + 1]).add([v.index], 0.7 * frac, "REPLACE")
        hair_n += 1
        continue

    # 裙子：主导骨是腿或胯，且半径大、高度在胯到裙摆之间
    if dom in ("J_Bip_L_UpperLeg", "J_Bip_R_UpperLeg", "J_Bip_C_Hips") and r > 0.09 \\
            and HEM - 0.02 <= p.z <= TOP:
        ang = math.atan2(p.y - hips_h.y, p.x - hips_h.x) % (2 * math.pi)
        k = int(round(ang / (2 * math.pi / SK_CH))) % SK_CH
        _i, a, c = skirt_names[k]
        t = max(0.0, min(1.0, (TOP - p.z) / (TOP - HEM)))
        if hips_vg:
            hips_vg.add([v.index], max(0.0, 1.0 - t * 2.0), "REPLACE")
        vg(a).add([v.index], (1 - t) * 0.8, "REPLACE")
        vg(c).add([v.index], t * 0.8, "REPLACE")
        skirt_n += 1

print("刷了头发顶点:", hair_n, "| 裙摆顶点:", skirt_n)
'''
s = s[:start] + new + s[end:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("权重逻辑改为按主导骨")
