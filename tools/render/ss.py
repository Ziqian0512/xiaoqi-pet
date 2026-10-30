import io, os
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('''    sc.render.resolution_x = W * 2
    sc.render.resolution_y = H * 2''',
'''    ss = int(os.environ.get("XIAOQI_SUPERSAMPLE", "2"))
    sc.render.resolution_x = W * ss
    sc.render.resolution_y = H * ss''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("超采样可配")
