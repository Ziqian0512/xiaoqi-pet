"""被戳一下：用 PIL 逐帧缩放（ffmpeg 的 scale 不支持时间表达式，这条最稳）。

0.7 秒 = 17 帧：1.00 → 1.05 → 1.00，带一点回弹。
"""

import io
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

FFMPEG = Path(r"E:\dsh-pet-install\dsh-pet-standalone-webm-chat\_internal"
              r"\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe")
W, H = 640, 360
FPS = 24
DUR = 0.7


def ease(i: int, n: int) -> float:
    import math

    x = i / max(1, n - 1)
    # 0 → 1 → 0，前快后慢
    return math.sin(math.pi * x) ** 0.8


def build(src: str, out: str, peak: float = 0.05) -> None:
    img = Image.open(src).convert("RGBA")
    n = max(2, int(FPS * DUR))
    tmp = Path(tempfile.mkdtemp(prefix="bounce-"))
    for i in range(n):
        s = 1.0 + peak * ease(i, n)
        w, h = int(W * s), int(H * s)
        scaled = img.resize((w, h), Image.LANCZOS)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.alpha_composite(scaled, ((W - w) // 2, H - h))
        canvas.save(tmp / ("f_%04d.png" % i))
    cmd = [str(FFMPEG), "-y", "-framerate", str(FPS), "-i", str(tmp / "f_%04d.png"),
           "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-auto-alt-ref", "0",
           "-b:v", "0", "-crf", "28", "-an", out]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print((r.stderr or b"").decode("utf-8", "replace")[-600:])
        raise SystemExit("编码失败")
    print("%-40s %6.0f KB  bounce(%d 帧)" % (Path(out).name,
                                             Path(out).stat().st_size / 1024, n))


if __name__ == "__main__":
    import sys

    build(sys.argv[1], sys.argv[2])
