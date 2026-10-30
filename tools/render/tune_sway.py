import io
P = r"E:\dsh-pet-projects\tools\render_clip.py"
s = io.open(P, encoding="utf-8").read()
s = s.replace('def hair_sway(frames: int = 240, amp: float = 0.10):', 'def hair_sway(frames: int = 240, amp: float = 0.022):')
s = s.replace('def skirt_sway(frames: int = 240, amp: float = 0.035):', 'def skirt_sway(frames: int = 240, amp: float = 0.018):')
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("幅度调小: hair 0.022 / skirt 0.018")
