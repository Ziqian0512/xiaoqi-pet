import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()

if "XIAOQI_ACTION" not in s:
    s = s.replace('''    if os.environ.get("XIAOQI_ANIM") == "idle":''',
'''    want = os.environ.get("XIAOQI_ACTION", "")
    if want:
        arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
        acts = [a for a in bpy.data.actions if want.lower() in a.name.lower()]
        if arm and acts:
            act = acts[0]
            if not arm.animation_data:
                arm.animation_data_create()
            arm.animation_data.action = act
            fr = act.frame_range
            sc = bpy.context.scene
            sc.frame_start = int(fr[0])
            end = int(fr[0]) + FRAMES - 1 if FRAMES > 1 else int(fr[1])
            sc.frame_end = min(end, int(fr[1]))
            print("动作:", act.name, "帧", sc.frame_start, "..", sc.frame_end)

    if os.environ.get("XIAOQI_ANIM") == "idle":''')
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("支持选动作")
