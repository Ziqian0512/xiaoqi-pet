"""给 v3 加眼睛开合和嘴片（几何 hack）。

- 眼睑：半圆片，挂在头骨上，绕上边缘旋转 → 闭合时盖住眼球
- 嘴：小椭圆片，缩放表示开合
"""

import math

import bmesh
import bpy
from mathutils import Matrix, Vector

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-staticarms.blend"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-face.blend"
FRAMES = 96

EYE_X = 0.065
EYE_Y = -0.099
EYE_Z = 0.772
EYE_R = 0.032
MOUTH_Z = 0.735
SKIN = (0.98, 0.86, 0.82, 1.0)
LIP = (0.55, 0.28, 0.30, 1.0)

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()

arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
head_bone = arm.pose.bones["J_Bip_C_Head"]
head_world = arm.matrix_world @ head_bone.head


def make_mat(name, rgba):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = 0.7
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.2
    return m


skin_mat = make_mat("lid_skin", SKIN)
lip_mat = make_mat("lip", LIP)


def half_disc(name, radius, mat, segments=16):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    center = bm.verts.new((0, 0, 0))
    verts = [center]
    for i in range(segments + 1):
        ang = math.pi * i / segments          # 半圆（0..180°）
        verts.append(bm.verts.new((math.cos(ang) * radius, 0, math.sin(ang) * radius)))
    for i in range(segments):
        bm.faces.new((verts[0], verts[i + 1], verts[i + 2]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def ellipse(name, rx, rz, mat, segments=20):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    center = bm.verts.new((0, 0, 0))
    ring = [bm.verts.new((math.cos(2 * math.pi * i / segments) * rx, 0,
                          math.sin(2 * math.pi * i / segments) * rz))
            for i in range(segments)]
    for i in range(segments):
        bm.faces.new((center, ring[i], ring[(i + 1) % segments]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(ob)
    return ob


pieces = []
for side, sign in (("L", 1), ("R", -1)):
    lid = half_disc("lid_" + side, EYE_R * 1.25, skin_mat)
    pos = Vector((sign * EYE_X, EYE_Y - 0.030, EYE_Z + EYE_R * 0.30))
    lid.parent = arm
    lid.parent_type = "BONE"
    lid.parent_bone = "J_Bip_C_Head"
    bpy.context.view_layer.update()
    lid.matrix_world = Matrix.Translation(pos)
    pieces.append(("lid", side, lid))

mouth = ellipse("mouth", 0.018, 0.007, lip_mat)
mpos = Vector((0.0, EYE_Y - 0.035, MOUTH_Z))
mouth.parent = arm
mouth.parent_type = "BONE"
mouth.parent_bone = "J_Bip_C_Head"
bpy.context.view_layer.update()
mouth.matrix_world = Matrix.Translation(mpos)
pieces.append(("mouth", "C", mouth))

sc = bpy.context.scene
sc.frame_start = 1
sc.frame_end = FRAMES

for kind, side, ob in pieces:
    if kind == "lid":
        for f in range(1, FRAMES + 1):
            t = (f - 1) / FRAMES
            # 每 2 秒眨一次：0.06 秒闭合
            phase = (t * 2.0) % 1.0
            closed = 1.0 if phase > 0.96 else 0.0
            ob.rotation_euler = (math.radians(-95) * closed, 0, 0)
            ob.keyframe_insert("rotation_euler", frame=f)
    else:
        for f in range(1, FRAMES + 1):
            ob.scale = (1.0, 1.0, 0.6)
            ob.keyframe_insert("scale", frame=f)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("已保存:", OUT, "| head bone z=%.3f" % head_world.z)
