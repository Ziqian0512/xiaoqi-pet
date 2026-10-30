import json, io, os
base = r"E:\dsh-pet-projects\pet-src-data\dsh-pet-standalone"
for name in ("config.json", "config-slot-0.json"):
    p = os.path.join(base, name)
    if not os.path.exists(p):
        continue
    d = json.load(io.open(p, encoding="utf-8"))
    keep = {k: d.get(k) for k in ("scale", "pet_scale", "dpi_scale", "character") if k in d}
    print(name, keep if keep else "（无 scale 键 → 用默认）")
    print("   所有顶层键:", list(d.keys())[:14])
