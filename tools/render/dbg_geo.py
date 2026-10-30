import bpy
from mathutils import Vector

SRC = r"E:\dsh-pet-projects\body\anims\anim5\tripo_convert_50935b14-2895-451b-b3bb-6925135e1347.fbx"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
bpy.context.view_layer.update()

arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
print("=== 关键骨骼（world 坐标）===")
for name in ("mixamorig:Hips", "mixamorig:Spine", "mixamorig:Spine1", "mixamorig:Spine2",
             "mixamorig:Neck", "mixamorig:Head", "mixamorig:HeadTop_End",
             "mixamorig:LeftUpLeg", "mixamorig:RightUpLeg",
             "mixamorig:LeftLeg", "mixamorig:RightLeg"):
    b = arm.data.bones.get(name)
    if not b:
        continue
    head = arm.matrix_world @ b.head_local
    tail = arm.matrix_world @ b.tail_local
    print("  %-26s head=(%.3f, %.3f, %.3f)  tail_z=%.3f" %
          (name, head.x, head.y, head.z, tail.z))

mesh_ob = next(o for o in bpy.context.scene.objects if o.type == "MESH")
me = mesh_ob.data
mw = mesh_ob.matrix_world
zs = [(mw @ v.co).z for v in me.vertices]
print("\n=== 网格 z 分布 ===")
print("  min=%.3f max=%.3f" % (min(zs), max(zs)))
import collections
hist = collections.Counter(int(z * 20) for z in zs)
for k in sorted(hist):
    print("  z=%.2f-%.2f : %d" % (k / 20, (k + 1) / 20, hist[k]))
