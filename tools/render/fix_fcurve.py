import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
if "def _iter_fcurves" not in s:
    s = s.replace("def add_procedural_idle(", '''def _iter_fcurves(act):
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


def add_procedural_idle(''')
    s = s.replace("            for fc in act.fcurves:", "            for fc in _iter_fcurves(act):")
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("兼容 5.x 的 fcurves")
