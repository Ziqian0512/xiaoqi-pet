import io
P = r"E:\dsh-pet-projects\tools\find_eyes.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace("if r > 0.45 and r > g * 2.2 and r > b * 1.8:", "if r > 0.55 and g < 0.30 and b < 0.40 and r > g * 2.5:")
s = s.replace("if p.z > 0.70 and p.y < 0.02:", "if 0.72 < p.z < 0.90 and p.y < -0.05:")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("更严格的虹膜判定")
