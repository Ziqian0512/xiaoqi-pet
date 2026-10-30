import io
P = r"E:\dsh-pet-projects\tools\make_clip.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('''    cmd = [str(FFMPEG)''', '''    Path(out).parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(FFMPEG)''')
s = s.replace('''    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:])''', '''    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print((r.stderr or b"").decode("utf-8", "replace")[-800:])''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("修好目录与解码")
