import json, io, os
base = r"E:\dsh-pet-projects\pet-src-data\dsh-pet-standalone"
chat = {
    "enabled": True,
    "active_provider": "relay",
    "providers": {
        "relay": {
            "name": "小祈（服务器）",
            "base_url": "http://100.117.93.31:8787",
            "chat_path": "/v1/chat/completions",
            "model": "dspet",
            "api_key": "",
            "timeout": 120.0,
            "temperature": 0.7,
            "max_tokens": 2048,
        }
    },
    "history_message_limit": 40,
    "history_char_limit": 24000,
}
for name in ("config.json", "config-slot-0.json"):
    p = os.path.join(base, name)
    d = {}
    if os.path.exists(p):
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except ValueError:
            d = {}
    d["chat"] = chat
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
    print("写入", name, "| chat.active_provider=relay")
