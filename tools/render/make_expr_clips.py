"""把 5 张 clean 表情做成「凑近」点击回应 clip（640x360，VP9 alpha）。

效果：从略远的胸像快速推到近景，停一下，再退回 —— 她一被戳就凑到镜头前。
"""

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

FFMPEG = Path(r"E:\dsh-pet-install\dsh-pet-standalone-webm-chat\_internal"
              r"\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe")
BODY = Path(r"E:\dsh-pet-projects\dspet-main\docs\body")
OUT_DIR = Path(r"E:\dsh-pet-projects\xiaoqi-pet\assets\characters\xiaoqi\videos\click")

W, H, FPS = 640, 360, 24
PAIRS = {
    "点击回应-生气": "xiaoqi-expr-angry-clean.png",
    "点击回应-委屈": "xiaoqi-expr-cry-clean.png",
    "点击回应-无语": "xiaoqi-expr-deadpan-clean.png",
    "点击回应-紧张": "xiaoqi-expr-nervous-clean.png",
    "点击回应-惊讶": "xiaoqi-expr-surprised-clean.png",
}

# 时间线（秒）：0 → 0.35 推近；0.35 → 1.1 停住；1.1 → 1.7 退回
PUSH, HOLD, BACK = 0.35, 1.1, 1.7


def key_white(img: Image.Image) -> Image.Image:
    from collections import deque

    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    seen = bytearray(w * h)
    q = deque()

    def is_bg(x, y):
        r, g, b, a = px[x, y]
        return a > 0 and r >= 238 and g >= 238 and b >= 238 and max(r, g, b) - min(r, g, b) <= 12

    for x in range(w):
        for y in (0, h - 1):
            if is_bg(x, y):
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(x, y):
                q.append((x, y))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        if not is_bg(x, y):
            continue
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                q.append((nx, ny))
    return img


def cover(img: Image.Image, zoom: float) -> Image.Image:
    """按 zoom 缩放到刚好装进 640x360（contain），居中偏上，保证猫耳和下巴都在画内。"""
    s = min(W / img.width, (H * 0.96) / img.height) * zoom
    nw, nh = max(1, int(img.width * s)), max(1, int(img.height * s))
    scaled = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = (W - nw) // 2
    y = max(0, int((H - nh) * 0.05))
    canvas.alpha_composite(scaled, (x, y))
    return canvas


def zoom_at(t: float) -> float:
    if t < PUSH:
        k = t / PUSH
        return 1.0 + 0.06 * (k ** 0.6)
    if t < HOLD:
        return 1.06
    if t < BACK:
        k = (t - HOLD) / (BACK - HOLD)
        return 1.06 - 0.06 * k
    return 1.0


def build(name: str, src: Path) -> None:
    raw = Image.open(src)
    # 底下有投影/渐变，先裁掉下缘，避免抠出灰边
    raw = raw.crop((0, 0, raw.width, int(raw.height * 0.86)))
    base = key_white(raw)
    n = int(FPS * BACK)
    tmp = Path(tempfile.mkdtemp(prefix="expr-"))
    for i in range(n):
        t = i / FPS
        frame = cover(base, zoom_at(t))
        frame.save(tmp / ("f_%04d.png" % i))
    out = OUT_DIR / (name + ".webm")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([str(FFMPEG), "-y", "-framerate", str(FPS),
                        "-i", str(tmp / "f_%04d.png"),
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
                        "-auto-alt-ref", "0", "-b:v", "0", "-crf", "30",
                        "-an", str(out)], capture_output=True)
    if r.returncode != 0:
        print((r.stderr or b"").decode("utf-8", "replace")[-500:])
        raise SystemExit("编码失败: " + name)
    print("%-24s %5.0f KB" % (name, out.stat().st_size / 1024))


if __name__ == "__main__":
    for nm, fn in PAIRS.items():
        p = BODY / fn
        if not p.is_file():
            print("缺图:", p)
            continue
        build(nm, p)
