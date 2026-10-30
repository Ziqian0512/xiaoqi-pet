import io
P = r"E:\dsh-pet-projects\xiaoqi-pet\pet\xiaoqi_link.py"
s = io.open(P, encoding="utf-8").read()
old = '''        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        return os.path.join(base, "dsh-pet-standalone-webm-chat", "xiaoqi.json")'''
new = '''        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        # 装好的版本是 dsh-pet-standalone-webm-chat；源码跑是 dsh-pet-standalone
        for name in ("dsh-pet-standalone-webm-chat", "dsh-pet-standalone"):
            path = os.path.join(base, name, "xiaoqi.json")
            if os.path.isfile(path):
                return path
        return os.path.join(base, "dsh-pet-standalone-webm-chat", "xiaoqi.json")'''
if old in s:
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("多目录查找:", "for name in (" in io.open(P, encoding="utf-8").read())
