import os, re, json
root = r"E:\dsh-pet\resources\app.asar.unpacked"
hits = []
for dirpath, dirs, files in os.walk(root):
    if len(hits) > 40: break
    for f in files:
        if f.endswith((".js", ".mjs", ".json")) and "image" in (dirpath + f).lower():
            hits.append(os.path.join(dirpath, f))
print("候选文件:", len(hits))
for h in hits[:12]:
    print(" ", h.replace(root, "..."))
