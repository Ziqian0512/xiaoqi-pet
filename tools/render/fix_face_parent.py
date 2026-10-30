import io
P = r"E:\dsh-pet-projects\tools\v3_face_hack.py"
s = io.open(P, encoding="utf-8").read()

s = s.replace('''    lid.location = (sign * EYE_X, EYE_Y - 0.004, EYE_Z + EYE_R * 0.55)
    lid.parent = arm
    lid.parent_type = "BONE"
    lid.parent_bone = "J_Bip_C_Head"
    pieces.append(("lid", side, lid))''',
'''    pos = Vector((sign * EYE_X, EYE_Y - 0.004, EYE_Z + EYE_R * 0.55))
    lid.parent = arm
    lid.parent_type = "BONE"
    lid.parent_bone = "J_Bip_C_Head"
    bpy.context.view_layer.update()
    lid.matrix_world = Matrix.Translation(pos)
    pieces.append(("lid", side, lid))''')

s = s.replace('''mouth.location = (0.0, EYE_Y - 0.006, MOUTH_Z)
mouth.parent = arm
mouth.parent_type = "BONE"
mouth.parent_bone = "J_Bip_C_Head"''',
'''mpos = Vector((0.0, EYE_Y - 0.006, MOUTH_Z))
mouth.parent = arm
mouth.parent_type = "BONE"
mouth.parent_bone = "J_Bip_C_Head"
bpy.context.view_layer.update()
mouth.matrix_world = Matrix.Translation(mpos)''')

s = s.replace("from mathutils import Vector", "from mathutils import Matrix, Vector")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("父级坐标修正")
