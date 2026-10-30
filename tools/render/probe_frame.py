import io
P = r"E:\dsh-pet-projects\tools\hand_probe.py"
s = io.open(P, encoding="utf-8").read()
if "frame_set" in s and "FRAME" not in s:
    s = s.replace('bpy.context.scene.frame_set(1)', 'import os\nbpy.context.scene.frame_set(int(os.environ.get("PROBE_FRAME", "1")))')
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
