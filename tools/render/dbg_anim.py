import bpy

SRC = r"E:\dsh-pet-projects\body\anims\anim5\tripo_convert_50935b14-2895-451b-b3bb-6925135e1347.fbx"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC, automatic_bone_orientation=True)
bpy.context.view_layer.update()

print("=== 对象 ===")
for ob in bpy.context.scene.objects:
    print(" ", ob.name, ob.type, "parent=", ob.parent.name if ob.parent else None)

print("=== Actions ===")
for act in bpy.data.actions:
    fr = act.frame_range
    print("  %-30s frames %.0f..%.0f  (%.1f 秒 @24fps)"
          % (act.name, fr[0], fr[1], (fr[1] - fr[0]) / 24.0))

arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
print("armature:", arm.name if arm else None)
if arm:
    print("骨骼数:", len(arm.data.bones))
    print("动画数据:", arm.animation_data.action.name if arm.animation_data and arm.animation_data.action else "无")
