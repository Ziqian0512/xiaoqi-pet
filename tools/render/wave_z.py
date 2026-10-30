import io
P = r"E:\dsh-pet-projects\tools\v3_wave.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('up.rotation_euler = (lift, 0.0, 0.0)', 'up.rotation_euler = (0.0, 0.0, lift)')
s = s.replace('fore.rotation_euler = (0.25 + swing, 0.0, 0.0)', 'fore.rotation_euler = (0.0, 0.0, 0.20 + swing)')
s = s.replace('hand.rotation_euler = (0.0, swing * 0.6, 0.0)', 'hand.rotation_euler = (0.0, 0.0, swing * 0.5)')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("挥手改用 Z 轴")
