import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

if "def add_procedural_idle" not in s:
    s = s.replace("def main():", '''def add_procedural_idle(frames: int = 240, fps: int = 24):
    """临时的程序化待机：整体轻微起伏 + 微摆（等真动作素材到位就删掉）。"""
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None:
        print("没有骨架，跳过程序化动画")
        return
    import math as _m
    base_z = arm.location.z
    for f in range(1, frames + 1):
        t = (f - 1) / frames
        arm.location.z = base_z + 0.006 * _m.sin(2 * _m.pi * t)
        arm.rotation_euler.z = 0.008 * _m.sin(2 * _m.pi * t + 0.8)
        arm.keyframe_insert("location", frame=f)
        arm.keyframe_insert("rotation_euler", frame=f)


def main():''')

    s = s.replace('''    setup_light()
    setup_render()''',
'''    setup_light()
    setup_render()
    if os.environ.get("XIAOQI_ANIM") == "idle":
        add_procedural_idle(FRAMES if FRAMES > 1 else 240)''')
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了程序化待机")
