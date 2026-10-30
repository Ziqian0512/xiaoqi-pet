import io, re
P = r"E:\dsh-pet-projects\dspet-main\relay\relay.py"
s = io.open(P, encoding="utf-8").read()
for m in re.finditer(r"stream", s):
    i = m.start()
    line_start = s.rfind("\n", 0, i) + 1
    line_end = s.find("\n", i)
    print(s.count("\n", 0, line_start) + 1, "|", s[line_start:line_end].strip()[:110])
