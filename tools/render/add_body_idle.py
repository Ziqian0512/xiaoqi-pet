import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

# 让 sway 在"没有动画数据"的模型上也能工作
s = s.replace('''    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None or not arm.animation_data:
        return''',
'''    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None:
        return
    if arm.animation_data is None:
        arm.animation_data_create()''')

if "def body_idle" not in s:
    s = s.replace("def main():", '''def body_idle(frames: int = 240, amp: float = 0.006):
    """没有动捕时，给整体加一点呼吸起伏（Hips 上下 + 轻微左右）。"""
    import math as _m
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None:
        return
    if arm.animation_data is None:
        arm.animation_data_create()
    pb = arm.pose.bones.get("J_Bip_C_Hips") or arm.pose.bones.get("mixamorig:Hips")
    if pb is None:
        return
    base = pb.location.copy()
    for f in range(1, frames + 1):
        t = (f - 1) / frames
        pb.location = (base.x + amp * 0.4 * _m.sin(2 * _m.pi * t),
                       base.y,
                       base.z + amp * _m.sin(2 * _m.pi * t))
        pb.keyframe_insert("location", frame=f)


def main():''')
    s = s.replace('''    if os.environ.get("XIAOQI_SKIRT_SWAY") == "1":''',
'''    if os.environ.get("XIAOQI_BODY_IDLE") == "1":
        body_idle(FRAMES if FRAMES > 1 else 240)

    if os.environ.get("XIAOQI_SKIRT_SWAY") == "1":''')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了 body_idle + 兼容无动画模型")
