import io
P = r"E:\dsh-pet-projects\tools\find_eyes.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace("        reds.append((p.x, p.y, p.z))",
              "        if p.z > 0.70 and p.y < 0.02:\n            reds.append((p.x, p.y, p.z))")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("只保留头部区域")
