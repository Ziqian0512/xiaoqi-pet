import io
P = r"E:\dsh-pet-projects\tools\v3_static_arms.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('"J_Bip_L_UpperArm": (math.radians(14), 0, math.radians(4)),', '"J_Bip_L_UpperArm": (0, 0, 0),')
s = s.replace('"J_Bip_R_UpperArm": (math.radians(14), 0, math.radians(-4)),', '"J_Bip_R_UpperArm": (0, 0, 0),')
s = s.replace('"J_Bip_L_LowerArm": (math.radians(-6), 0, 0),', '"J_Bip_L_LowerArm": (0, 0, 0),')
s = s.replace('"J_Bip_R_LowerArm": (math.radians(-6), 0, 0),', '"J_Bip_R_LowerArm": (0, 0, 0),')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("手臂全部归零（保持绑定姿态）")
