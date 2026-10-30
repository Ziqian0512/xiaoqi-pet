import io
P = r"E:\dsh-pet-projects\dspet-main\relay\relay.py"
lines = io.open(P, encoding="utf-8").read().split("\n")
start = 2178
for i in range(start, min(start + 60, len(lines))):
    print(i + 1, lines[i][:120])
