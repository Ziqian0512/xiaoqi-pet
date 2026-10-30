import io
P = r"E:\dsh-pet-projects\tools\v3_face_hack.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace("EYE_R = 0.030", "EYE_R = 0.032")
s = s.replace("Vector((sign * EYE_X, EYE_Y - 0.004, EYE_Z + EYE_R * 0.55))",
              "Vector((sign * EYE_X, EYE_Y - 0.030, EYE_Z + EYE_R * 0.30))")
s = s.replace("Vector((0.0, EYE_Y - 0.006, MOUTH_Z))",
              "Vector((0.0, EYE_Y - 0.035, MOUTH_Z))")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("眼睑前移 3cm")
