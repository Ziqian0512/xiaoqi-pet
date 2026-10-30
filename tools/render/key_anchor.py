"""把锚点图的白底抠成透明，并摆到 640x960 画布上（脚贴底、居中）。

不用 colorkey —— 她的头发和白丝都接近白色，色键会把人也抠掉。
用"从边缘漫水填充"只去掉与画布边界连通的白色。
"""

import os
import sys
from collections import deque

from PIL import Image, ImageFilter

SRC = r"E:\dsh-pet-projects\dspet-main\docs\body\xiaoqi-main-v3-final.png"
OUT = r"E:\dsh-pet-projects\build\idle-keyed.png"
CANVAS = (640, 360)
FEET_Y = 330             # 与 catalog.FEET_Y 对齐
TOP_MARGIN = 8


def key_white(img: Image.Image) -> Image.Image:
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
        r, g, b, _a = px[x, y]
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                q.append((nx, ny))

    # 边缘羽化：alpha 轻微模糊，压掉锯齿
    alpha = img.getchannel("A").filter(ImageFilter.GaussianBlur(0.8))
    img.putalpha(alpha)
    return img


def place(img: Image.Image, canvas=CANVAS) -> Image.Image:
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    cw, ch = canvas
    max_w = cw - 24
    max_h = FEET_Y - TOP_MARGIN
    scale = min(max_w / img.width, max_h / img.height)
    new = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
    img = img.resize(new, Image.LANCZOS)
    out = Image.new("RGBA", canvas, (0, 0, 0, 0))
    x = (cw - new[0]) // 2
    y = FEET_Y - new[1]
    out.alpha_composite(img, (x, y))
    return out


def main() -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    src = Image.open(SRC)
    keyed = key_white(src)
    final = place(keyed)
    final.save(OUT)
    bbox = final.getbbox()
    print("输出:", OUT, final.size, "内容 bbox:", bbox)
    alpha = final.getchannel("A")
    hist = alpha.histogram()
    print("透明像素占比: %.1f%%" % (100.0 * hist[0] / (final.width * final.height)))


if __name__ == "__main__":
    main()
