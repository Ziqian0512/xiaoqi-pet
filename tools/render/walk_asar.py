import os
root = r"E:\dsh-pet\resources\app.asar.unpacked"
n = 0
for dirpath, dirs, files in os.walk(root):
    for f in files:
        n += 1
print("文件总数:", n)
# 列出前两层目录
for dirpath, dirs, files in os.walk(root):
    depth = dirpath[len(root):].count(os.sep)
    if depth <= 2:
        print(dirpath.replace(root, "."), "| dirs:", dirs[:6], "| files:", files[:4])
    if depth >= 2:
        dirs[:] = []
