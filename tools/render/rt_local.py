import io
P = r"E:\dsh-pet-projects\tools\retarget2.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('con.target_space = "WORLD"', 'con.target_space = "LOCAL"')
s = s.replace('con.owner_space = "WORLD"', 'con.owner_space = "LOCAL"')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("改成 LOCAL 空间")
