"""从一张已抠像的 PNG 生成桌宠 clip（640x360，VP9 alpha，24fps）。

用法：
  python make_clip.py <输入png> <输出webm> <预设> [时长秒]

预设：
  idle   微呼吸（横 4px + 纵 3px 慢漂移）
  bounce 被戳一下：快速放大 4% 再回落
  shake  摇头：左右 8px 抖动
  tilt   歪头：轻微旋转（用 ffmpeg rotate）
  slide  横向滑入滑出（做"走过来"的占位）

真动作（跳舞/吃饭）以后由 AI 图生视频出 mp4，再走同一条编码命令。
"""

import subprocess
import sys
from pathlib import Path

FFMPEG = Path(r"E:\dsh-pet-install\dsh-pet-standalone-webm-chat\_internal"
              r"\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe")

W, H = 640, 360


def build(src: str, out: str, preset: str, seconds: float = 10.0) -> None:
    if preset == "idle":
        big = f"scale={W + 20}:{H + 11}:flags=lanczos"
        crop = f"crop={W}:{H}:x='10+4*sin(2*PI*t/6)':y='5+3*sin(2*PI*t/9)'"
        vf = f"{big},format=yuva420p,{crop}"
    elif preset == "bounce":
        # 0.6 秒：放大到 1.04 再回来
        vf = (f"scale={W}:{H}:flags=lanczos,format=yuva420p,"
              f"scale=w='{W}*(1+0.04*sin(PI*t/0.6))':h='{H}*(1+0.04*sin(PI*t/0.6))'"
              f":eval=frame,crop={W}:{H}")
    elif preset == "shake":
        big = f"scale={W + 24}:{H + 8}:flags=lanczos"
        crop = f"crop={W}:{H}:x='12+8*sin(2*PI*t/0.35)':y='4'"
        vf = f"{big},format=yuva420p,{crop}"
    elif preset == "tilt":
        vf = (f"scale={W}:{H}:flags=lanczos,format=yuva420p,"
              f"rotate='0.035*sin(2*PI*t/2.2)':c=black@0:ow={W}:oh={H}")
    elif preset == "slide":
        big = f"scale={W + 80}:{H}:flags=lanczos"
        crop = f"crop={W}:{H}:x='40-30*sin(2*PI*t/4)':y='0'"
        vf = f"{big},format=yuva420p,{crop}"
    else:
        raise SystemExit("未知预设: " + preset)

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(FFMPEG), "-y", "-loop", "1", "-framerate", "24", "-i", src,
           "-vf", vf, "-t", str(seconds),
           "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-auto-alt-ref", "0",
           "-b:v", "0", "-crf", "30", "-an", out]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print((r.stderr or b"").decode("utf-8", "replace")[-800:])
        raise SystemExit("编码失败")
    print("%-40s %6.0f KB  %s" % (Path(out).name, Path(out).stat().st_size / 1024, preset))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    build(sys.argv[1], sys.argv[2], sys.argv[3],
          float(sys.argv[4]) if len(sys.argv) > 4 else 10.0)
