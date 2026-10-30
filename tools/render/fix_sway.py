import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('''    arm.animation_data.action = None      # 避免和动捕动作抢同一个 action\n''', '')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("不再清空动捕 action:", "arm.animation_data.action = None" not in s)
