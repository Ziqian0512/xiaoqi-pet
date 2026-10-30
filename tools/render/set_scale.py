import json, io, os
p = r"E:\dsh-pet-projects\pet-src-data\dsh-pet-standalone\config-slot-0.json"
d = json.load(io.open(p, encoding="utf-8"))
d["scale"] = 0.9          # 窗口 1152×648，人物约 576px 高
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
print("scale =", d["scale"])
