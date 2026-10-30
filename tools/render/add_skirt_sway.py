import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
if "def skirt_sway" not in s:
    s = s.replace("def main():", '''def skirt_sway(frames: int = 240, amp: float = 0.035):
    """裙摆摆动：给裙骨加小幅滞后摆动（比布料稳定，320px 下够看）。"""
    import math as _m
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None or not arm.animation_data:
        return
    for pb in arm.pose.bones:
        if not pb.name.startswith("skirt_"):
            continue
        seg = 1 if pb.name.endswith("_b") else 0
        swing = amp * (0.5 + 0.5 * seg)
        pb.rotation_mode = "XYZ"
        for f in range(1, frames + 1):
            t = (f - 1) / frames
            phase = 0.7 * (hash(pb.name) % 7)
            pb.rotation_euler = (
                swing * _m.sin(2 * _m.pi * t + phase),
                0.0,
                swing * 0.6 * _m.cos(2 * _m.pi * t + phase * 0.5),
            )
            pb.keyframe_insert("rotation_euler", frame=f)


def main():''')
    s = s.replace('''    if os.environ.get("XIAOQI_HAIR_SWAY") == "1":''',
'''    if os.environ.get("XIAOQI_SKIRT_SWAY") == "1":
        skirt_sway(FRAMES if FRAMES > 1 else 240)

    if os.environ.get("XIAOQI_HAIR_SWAY") == "1":''')
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了裙摆摆动")
