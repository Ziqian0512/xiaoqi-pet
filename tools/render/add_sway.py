import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
if "hair_sway" not in s:
    s = s.replace("def main():", '''def hair_sway(frames: int = 240, fps: int = 24, amp: float = 0.10):
    """给发束骨加滞后摆动（近似惯性），没有布料/物理也能看出"头发跟着动"。"""
    import math as _m
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None or not arm.animation_data:
        return
    arm.animation_data.action = None      # 避免和动捕动作抢同一个 action
    for pb in arm.pose.bones:
        if not pb.name.startswith("hair_"):
            continue
        seg = int(pb.name.rsplit("_", 1)[-1])
        swing = amp * (0.4 + 0.35 * seg)      # 越靠发梢幅度越大
        pb.rotation_mode = "XYZ"
        for f in range(1, frames + 1):
            t = (f - 1) / frames
            pb.rotation_euler = (
                swing * _m.sin(2 * _m.pi * t + 0.9 * seg),
                0.0,
                swing * 0.35 * _m.cos(2 * _m.pi * t + 0.5 * seg),
            )
            pb.keyframe_insert("rotation_euler", frame=f)


def main():''')
    s = s.replace('''    if os.environ.get("XIAOQI_ANIM") == "idle":''',
'''    if os.environ.get("XIAOQI_HAIR_SWAY") == "1":
        hair_sway(FRAMES if FRAMES > 1 else 240)

    if os.environ.get("XIAOQI_ANIM") == "idle":''')
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了发束摆动")
