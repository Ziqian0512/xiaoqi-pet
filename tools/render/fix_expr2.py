import io
P = r"E:\dsh-pet-projects\tools\make_expr_clips.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace("return 1.0 + 0.12 * (k ** 0.6)", "return 1.0 + 0.06 * (k ** 0.6)")
s = s.replace("        return 1.12\n", "        return 1.06\n")
s = s.replace("return 1.12 - 0.12 * k", "return 1.06 - 0.06 * k")
s = s.replace("y = max(0, int((H - nh) * 0.25))", "y = max(0, int((H - nh) * 0.12))")
s = s.replace('s = min(W / img.width, H / img.height) * zoom', 's = min(W / img.width, (H * 0.98) / img.height) * zoom')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("zoom 峰值降到 1.06")
