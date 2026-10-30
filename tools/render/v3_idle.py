"""v3 没有骨架，用父级空物体做"整体呼吸"（起伏 + 轻微缩放），供渲染用。"""

import math

import bpy

SRC = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-low.blend"
OUT = r"E:\dsh-pet-projects\body\v3\xiaoqi-v3-idle.blend"
FRAMES = 96

bpy.ops.wm.open_mainfile(filepath=SRC)
bpy.context.view_layer.update()

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
root = bpy.data.objects.new("root", None)
bpy.context.scene.collection.objects.link(root)
for ob in meshes:
    ob.parent = root
    ob.matrix_parent_inverse = root.matrix_world.inverted()

for f in range(1, FRAMES + 1):
    t = (f - 1) / FRAMES
    root.location.z = 0.004 * math.sin(2 * math.pi * t)
    s = 1.0 + 0.004 * math.sin(2 * math.pi * t)
    root.scale = (s, s, 1.0 + 0.006 * math.sin(2 * math.pi * t))
    root.keyframe_insert("location", frame=f)
    root.keyframe_insert("scale", frame=f)

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = FRAMES
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved:", OUT, "| meshes:", len(meshes))
