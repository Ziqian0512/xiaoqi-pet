import bpy
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\dsh-pet-projects\body\xiaoqi-rig.glb")
bpy.context.view_layer.update()

print("=== 对象 ===")
for ob in bpy.context.scene.objects:
    print(" ", ob.name, ob.type, "scale=", tuple(round(s, 3) for s in ob.scale),
          "parent=", ob.parent.name if ob.parent else None)

deps = bpy.context.evaluated_depsgraph_get()
for ob in bpy.context.scene.objects:
    if ob.type != "MESH":
        continue
    ev = ob.evaluated_get(deps)
    me = ev.to_mesh()
    mw = ev.matrix_world
    zs = [(mw @ v.co).z for v in me.vertices]
    xs = [(mw @ v.co).x for v in me.vertices]
    print("mesh", ob.name, "verts=", len(me.vertices))
    print("  world z: %.3f .. %.3f" % (min(zs), max(zs)))
    print("  world x: %.3f .. %.3f" % (min(xs), max(xs)))
    ev.to_mesh_clear()

arm = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"]
print("armature:", [a.name for a in arm])
