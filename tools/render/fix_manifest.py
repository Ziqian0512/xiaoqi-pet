import json, io
p = r"E:\dsh-pet-projects\xiaoqi-pet\assets\characters\xiaoqi\manifest.json"
data = {"name": "小祈", "body_box": [123, 12, 516, 952]}
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))
print(open(p, encoding="utf-8").read())
