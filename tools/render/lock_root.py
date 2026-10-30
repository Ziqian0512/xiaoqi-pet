import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
if "锁住位移" not in s:
    s = s.replace('''            print("动作:", act.name, "帧", sc.frame_start, "..", sc.frame_end)''',
'''            # 锁住水平位移（桌宠窗口跟不了她走），只保留上下起伏
            for fc in act.fcurves:
                if fc.data_path.endswith("location") and ("Root" in fc.data_path or "Hips" in fc.data_path):
                    if fc.array_index in (0, 1):
                        for kp in fc.keyframe_points:
                            kp.co[1] = 0.0
                            kp.handle_left[1] = 0.0
                            kp.handle_right[1] = 0.0
            print("动作:", act.name, "帧", sc.frame_start, "..", sc.frame_end,
                  "（已锁水平位移）")''')
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了位移锁")
