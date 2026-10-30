import io, json
p = r"E:\dsh-pet-projects\xiaoqi-pet\assets\characters\xiaoqi\manifest.json"
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(
    {"name": "小祈", "body_box": [253, 8, 387, 330]}, ensure_ascii=False, indent=2))
print("ok")
