import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace("W, H = 640, 360", "W, H = 1280, 720")
s = s.replace('ss = int(os.environ.get("XIAOQI_SUPERSAMPLE", "2"))', 'ss = int(os.environ.get("XIAOQI_SUPERSAMPLE", "1"))')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("渲染改 1280x720, 超采样默认 1")
