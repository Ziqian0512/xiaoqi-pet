"""把裙子拆成独立物体 + 布料模拟（腰部钉住，跟着身体动、下摆自然垂）。

输入：xiaoqi-rigged-hair.blend（已有裙骨和发束骨）
输出：xiaoqi-dynamics.blend
"""

import math

import bpy
from mathutils import Vector

BLEND_IN = r"E:\dsh-pet-projects\body\xiaoqi-rigged-hair.blend"
BLEND_OUT = r"E:\dsh-pet-projects\body\xiaoqi-dynamics.blend"

TOP_Z = 0.552
HEM_Z = 0.372
WAIST_R = 0.075

bpy.ops.wm.open_mainfile(filepath=BLEND_IN)
bpy.context.view_layer.update()

body = next(o for o in bpy.context.scene.objects if o.type == "MESH")
mw = body.matrix_world

# ---- 1. 选裙摆顶点 ----
bpy.context.view_layer.objects.active = body
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="DESELECT")
bpy.ops.object.mode_set(mode="OBJECT")

hips = [(v.index) for v in body.data.vertices
        if HEM_Z - 0.02 <= (mw @ v.co).z <= TOP_Z + 0.01
        and math.hypot((mw @ v.co).x, (mw @ v.co).y) > WAIST_R]
print("裙摆顶点:", len(hips))
if not hips:
    raise SystemExit("没选到裙摆顶点")

for i in hips:
    body.data.vertices[i].select = True
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.separate(type="SELECTED")
bpy.ops.object.mode_set(mode="OBJECT")

skirt = None
for ob in bpy.context.scene.objects:
    if ob.type == "MESH" and ob is not body:
        skirt = ob
        break
print("裙子物体:", skirt.name if skirt else None, "顶点:", len(skirt.data.vertices) if skirt else 0)

# ---- 2. 钉住腰部 ----
pin = skirt.vertex_groups.new(name="pin")
smw = skirt.matrix_world
for v in skirt.data.vertices:
    z = (smw @ v.co).z
    if z > TOP_Z - 0.03:
        pin.add([v.index], 1.0, "REPLACE")

# ---- 3. 布料 ----
cl = skirt.modifiers.new("Cloth", "CLOTH")
settings = cl.settings
settings.quality = 8
settings.mass = 0.25
settings.air_damping = 1.0
settings.tension_stiffness = 25
settings.compression_stiffness = 25
settings.shear_stiffness = 8
settings.bending_stiffness = 1.2
settings.vertex_group_mass = "pin"
settings.pin_stiffness = 1.0
try:
    settings.use_pressure = False
except AttributeError:
    pass
cl.point_cache.frame_start = 1
cl.point_cache.frame_end = 260

# 身体当碰撞体
body.modifiers.new("Collision", "COLLISION")
col = body.collision
col.thickness_outer = 0.012
col.cloth_friction = 5

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print("已保存:", BLEND_OUT)
