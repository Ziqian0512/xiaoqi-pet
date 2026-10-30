import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('sh.light = "FLAT"', 'sh.light = os.environ.get("XIAOQI_WB_LIGHT", "FLAT")')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("光源可切换")
