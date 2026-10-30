import io
P = r"E:\dsh-pet-projects\xiaoqi-pet\pet\xiaoqi_link.py"
s = io.open(P, encoding="utf-8").read()
if "\nimport logging\n" not in s:
    s = s.replace("import json\nimport time", "import json\nimport logging\nimport time", 1)
if "log = logging.getLogger" not in s:
    s = s.replace("DEFAULT_BASE = ", "log = logging.getLogger(__name__)\n\nDEFAULT_BASE = ", 1)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("logging:", "log = logging.getLogger" in io.open(P, encoding="utf-8").read())
