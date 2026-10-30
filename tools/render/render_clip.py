"""Blender 无头渲染：GLB/FBX → 透明 640×360 PNG 序列。

用法（命令行）：
  blender -b --factory-startup -P render_clip.py -- <输入模型> <输出目录> [帧数] [起点帧]

先跑 1 帧验证构图：帧数传 1。
"""

import os
import sys
import math

import bpy
from mathutils import Vector

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SRC = ARGS[0]
OUT = ARGS[1]
FRAMES = int(ARGS[2]) if len(ARGS) > 2 else 1
START = int(ARGS[3]) if len(ARGS) > 3 else 1

W, H = 1280, 720


def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def drop_strays():
    """删掉不属于角色的网格（Tripo 偶尔塞一个 Icosphere）。

    规则：有骨架修改器、或父级是骨架、或顶点数 > 200 且不是球状杂物 → 保留。
    简单可靠：保留「有 Armature 修改器」或「父级为 ARMATURE」的网格；
    若一个都没有（未绑定模型），则保留顶点最多的那个。
    """
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    keep = set()
    if arm is not None:
        for ob in meshes:
            if ob.parent is arm or any(m.type == "ARMATURE" for m in ob.modifiers):
                keep.add(ob.name)
    if not keep and meshes:
        meshes.sort(key=lambda o: len(o.data.vertices), reverse=True)
        keep.add(meshes[0].name)
    removed = []
    for ob in meshes:
        if ob.name not in keep:
            removed.append(ob.name)
            bpy.data.objects.remove(ob, do_unlink=True)
    if removed:
        print("删掉非角色网格:", removed, "| 保留", len(keep), "个")


def import_model(path: str):
    if path.lower().endswith(".blend"):
        bpy.ops.wm.open_mainfile(filepath=path)
        return
    if path.lower().endswith((".glb", ".gltf")):
        bpy.ops.import_scene.gltf(filepath=path)
    else:
        bpy.ops.import_scene.fbx(filepath=path)


def bounds_of_meshes():
    """用实际顶点（world 空间）算包围盒——skinned mesh 的 bound_box 不可靠。"""
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    mins = Vector((1e9, 1e9, 1e9))
    maxs = Vector((-1e9, -1e9, -1e9))
    found = False
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH":
            continue
        ev = ob.evaluated_get(deps)
        me = ev.to_mesh()
        mw = ev.matrix_world
        for v in me.vertices:
            w = mw @ v.co
            mins = Vector((min(mins.x, w.x), min(mins.y, w.y), min(mins.z, w.z)))
            maxs = Vector((max(maxs.x, w.x), max(maxs.y, w.y), max(maxs.z, w.z)))
            found = True
        ev.to_mesh_clear()
    if not found:
        raise RuntimeError("场景里没有网格")
    return mins, maxs


def setup_camera(mins: Vector, maxs: Vector):
    """正交相机正对模特。

    Blender 的 ortho_scale 说的是**较长边**（这里 640 宽），
    所以竖直可见高度 = ortho_scale * (H/W)。
    """
    height = maxs.z - mins.z
    width = maxs.x - mins.x

    vspan = height * (360.0 / 320.0)          # 竖直可见范围（身高占 320px）
    S = vspan * (W / H)                       # 换算成 ortho_scale（横向）
    if width * 1.15 > S * (H / W) * 0 + S:    # 横向太宽就放大画幅
        S = max(S, width * 1.15 * (W / H))

    cz = mins.z + (0.5 - 30.0 / 360.0) * vspan
    cx = (mins.x + maxs.x) / 2

    cam_data = bpy.data.cameras.new("Cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = S
    cam = bpy.data.objects.new("Cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)

    depth = max(maxs.y - mins.y, 0.2)
    cam.location = Vector((cx, mins.y - depth * 3 - 1.0, cz))
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam
    return cam


def setup_render():
    sc = bpy.context.scene
    engine = os.environ.get("XIAOQI_ENGINE", "eevee")
    if engine == "workbench":
        sc.render.engine = "BLENDER_WORKBENCH"
        sh = sc.display.shading
        sh.light = os.environ.get("XIAOQI_WB_LIGHT", "FLAT")
        sh.color_type = "TEXTURE"
        sh.show_object_outline = False
        sh.show_specular_highlight = False
    else:
        for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                sc.render.engine = eng
                break
            except TypeError:
                continue
    ss = int(os.environ.get("XIAOQI_SUPERSAMPLE", "1"))
    sc.render.resolution_x = W * ss
    sc.render.resolution_y = H * ss
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.fps = 24
    try:
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
        sc.view_settings.exposure = 0.0
    except TypeError:
        pass


def setup_light():
    """三点光：主光偏左前、补光右侧弱、轮廓光在后上方；环境光压低。"""
    def area(name, loc, rot, energy, size):
        d = bpy.data.lights.new(name, type="AREA")
        d.energy = energy
        d.size = size
        ob = bpy.data.objects.new(name, d)
        ob.location = loc
        ob.rotation_euler = rot
        bpy.context.scene.collection.objects.link(ob)
        return ob

    area("Key", (1.6, -2.2, 2.2), (math.radians(50), 0, math.radians(35)), 150, 2.0)
    area("Fill", (-2.0, -1.6, 1.2), (math.radians(70), 0, math.radians(-55)), 25, 3.0)
    area("Rim", (0.4, 1.8, 2.6), (math.radians(120), 0, math.radians(200)), 70, 2.0)

    world = bpy.data.worlds.new("W")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.55, 0.6, 0.7, 1)
        bg.inputs[1].default_value = 0.06
    bpy.context.scene.world = world

    sc = bpy.context.scene
    try:
        sc.eevee.use_gtao = True          # 环境光遮蔽：让褶皱有层次
    except AttributeError:
        pass
    try:
        sc.eevee.taa_render_samples = 32
    except AttributeError:
        pass


def _iter_fcurves(act):
    """Blender 5.x 的 Action 没有 .fcurves 了（slotted actions）。"""
    try:
        return list(act.fcurves)
    except AttributeError:
        curves = []
        for layer in getattr(act, "layers", []):
            for strip in getattr(layer, "strips", []):
                for cb in getattr(strip, "channelbags", []):
                    curves.extend(cb.fcurves)
        return curves


def add_procedural_idle(frames: int = 240, fps: int = 24):
    """临时的程序化待机：整体轻微起伏 + 微摆（等真动作素材到位就删掉）。"""
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None:
        print("没有骨架，跳过程序化动画")
        return
    import math as _m
    base_z = arm.location.z
    for f in range(1, frames + 1):
        t = (f - 1) / frames
        arm.location.z = base_z + 0.006 * _m.sin(2 * _m.pi * t)
        arm.rotation_euler.z = 0.008 * _m.sin(2 * _m.pi * t + 0.8)
        arm.keyframe_insert("location", frame=f)
        arm.keyframe_insert("rotation_euler", frame=f)


def hair_sway(frames: int = 240, fps: int = 24, amp: float = 0.10):
    """给发束骨加滞后摆动（近似惯性），没有布料/物理也能看出"头发跟着动"。"""
    import math as _m
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None:
        return
    if arm.animation_data is None:
        arm.animation_data_create()
    for pb in arm.pose.bones:
        if not pb.name.startswith("hair_"):
            continue
        seg = int(pb.name.rsplit("_", 1)[-1])
        swing = amp * (0.4 + 0.35 * seg)      # 越靠发梢幅度越大
        pb.rotation_mode = "XYZ"
        for f in range(1, frames + 1):
            t = (f - 1) / frames
            pb.rotation_euler = (
                swing * _m.sin(2 * _m.pi * t + 0.9 * seg),
                0.0,
                swing * 0.35 * _m.cos(2 * _m.pi * t + 0.5 * seg),
            )
            pb.keyframe_insert("rotation_euler", frame=f)


def skirt_sway(frames: int = 240, amp: float = 0.018):
    """裙摆摆动：给裙骨加小幅滞后摆动（比布料稳定，320px 下够看）。"""
    import math as _m
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None:
        return
    if arm.animation_data is None:
        arm.animation_data_create()
    for pb in arm.pose.bones:
        if not pb.name.startswith("skirt_"):
            continue
        seg = 1 if pb.name.endswith("_b") else 0
        swing = amp * (0.5 + 0.5 * seg)
        pb.rotation_mode = "XYZ"
        for f in range(1, frames + 1):
            t = (f - 1) / frames
            phase = 0.7 * (hash(pb.name) % 7)
            pb.rotation_euler = (
                swing * _m.sin(2 * _m.pi * t + phase),
                0.0,
                swing * 0.6 * _m.cos(2 * _m.pi * t + phase * 0.5),
            )
            pb.keyframe_insert("rotation_euler", frame=f)


def body_idle(frames: int = 240, amp: float = 0.006):
    """没有动捕时，给整体加一点呼吸起伏（Hips 上下 + 轻微左右）。"""
    import math as _m
    arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
    if arm is None:
        return
    if arm.animation_data is None:
        arm.animation_data_create()
    pb = arm.pose.bones.get("J_Bip_C_Hips") or arm.pose.bones.get("mixamorig:Hips")
    if pb is None:
        return
    base = pb.location.copy()
    for f in range(1, frames + 1):
        t = (f - 1) / frames
        pb.location = (base.x + amp * 0.4 * _m.sin(2 * _m.pi * t),
                       base.y,
                       base.z + amp * _m.sin(2 * _m.pi * t))
        pb.keyframe_insert("location", frame=f)


def main():
    clean_scene()
    import_model(SRC)
    drop_strays()
    mins, maxs = bounds_of_meshes()
    print("模型包围盒 min=%s max=%s" % (tuple(round(v, 3) for v in mins),
                                      tuple(round(v, 3) for v in maxs)))
    setup_camera(mins, maxs)
    setup_light()
    setup_render()
    want = os.environ.get("XIAOQI_ACTION", "")
    if want:
        arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
        acts = [a for a in bpy.data.actions if want.lower() in a.name.lower()]
        if arm and acts:
            act = acts[0]
            if not arm.animation_data:
                arm.animation_data_create()
            arm.animation_data.action = act
            fr = act.frame_range
            sc = bpy.context.scene
            sc.frame_start = int(fr[0])
            end = int(fr[0]) + FRAMES - 1 if FRAMES > 1 else int(fr[1])
            sc.frame_end = min(end, int(fr[1]))
            # 锁住水平位移（桌宠窗口跟不了她走），只保留上下起伏
            for fc in _iter_fcurves(act):
                if fc.data_path.endswith("location") and ("Root" in fc.data_path or "Hips" in fc.data_path):
                    if fc.array_index in (0, 1):
                        for kp in fc.keyframe_points:
                            kp.co[1] = 0.0
                            kp.handle_left[1] = 0.0
                            kp.handle_right[1] = 0.0
            print("动作:", act.name, "帧", sc.frame_start, "..", sc.frame_end,
                  "（已锁水平位移）")

    if os.environ.get("XIAOQI_BODY_IDLE") == "1":
        body_idle(FRAMES if FRAMES > 1 else 240)

    if os.environ.get("XIAOQI_SKIRT_SWAY") == "1":
        skirt_sway(FRAMES if FRAMES > 1 else 240)

    if os.environ.get("XIAOQI_HAIR_SWAY") == "1":
        hair_sway(FRAMES if FRAMES > 1 else 240)

    if os.environ.get("XIAOQI_ANIM") == "idle":
        add_procedural_idle(FRAMES if FRAMES > 1 else 240)

    os.makedirs(OUT, exist_ok=True)
    sc = bpy.context.scene
    sc.frame_start = START
    sc.frame_end = START + FRAMES - 1
    sc.render.filepath = os.path.join(OUT, "f_")
    bpy.ops.render.render(animation=True)
    print("渲染完成 →", OUT)


main()
