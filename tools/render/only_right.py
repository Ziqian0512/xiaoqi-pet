import io
P = r"E:\dsh-pet-projects\tools\arm_out_test.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('for name in ("J_Bip_L_UpperArm", "J_Bip_R_UpperArm"):', 'for name in ("J_Bip_R_UpperArm",):')
s = s.replace('sign = 1 if name.startswith("J_Bip_L") else -1', 'sign = 1.0')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("只测右臂")
