import json, io, os
base = r"E:\dsh-pet-projects\pet-src-data\dsh-pet-standalone"
for name in ("config.json", "config-slot-0.json"):
    p = os.path.join(base, name)
    if not os.path.exists(p):
        print(name, "不存在"); continue
    d = json.load(io.open(p, encoding="utf-8"))
    chat = d.get("chat") or {}
    prov = (chat.get("providers") or {}).get(chat.get("active_provider") or "", {})
    print(name, "| chat.enabled=", chat.get("enabled"),
          "| provider=", chat.get("active_provider"),
          "| base_url=", prov.get("base_url"), "| model=", prov.get("model"),
          "| key?", bool(prov.get("api_key")))
