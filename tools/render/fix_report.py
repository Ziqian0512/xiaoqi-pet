import io
P = r"E:\dsh-pet-projects\tools\v3_report.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('print("%-22s %8s  x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]" % ("name", "tris", 0, 0, 0, 0, 0, 0))', '')
s = s.replace('print("%-22s %8d  x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]" % r)',
              'print("PART %-22s %8d x[%.2f,%.2f] y[%.2f,%.2f] z[%.2f,%.2f]" % r)')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
