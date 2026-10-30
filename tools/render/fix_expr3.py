import io
P = r"E:\dsh-pet-projects\tools\make_expr_clips.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace("int(raw.height * 0.72)", "int(raw.height * 0.86)")
s = s.replace('s = min(W / img.width, (H * 0.98) / img.height) * zoom', 's = min(W / img.width, (H * 0.96) / img.height) * zoom')
s = s.replace("y = max(0, int((H - nh) * 0.12))", "y = max(0, int((H - nh) * 0.05))")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("裁剪 86%，contain 96%")
