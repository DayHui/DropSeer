"""底色 / 主色 候选对比样张 —— 供定色用"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_dropseer_assets as B

OUT = os.path.join(B.ROOT, "对比_底色与主色.png")
SANS = B.SANS_CN
NEUTRAL = (255, 255, 255)
INK = (60, 68, 72)
MUTE = (120, 132, 138)
LINE = (222, 226, 228)

PRIMARY = [
    ("A", "现用 · 黛青", "#16404D", "色相 192°，偏黄绿，屏幕发闷"),
    ("B", "深海蓝", "#123D52", "色相 203°，冷青蓝，清冷干净 ★推荐"),
    ("C", "数码墨蓝", "#1C2B38", "色相 208°，低饱和炭蓝，极简高级"),
    ("D", "蓝黑墨", "#12242E", "色相 196°，近黑最沉，仪器感最强"),
]
GROUND = [
    ("1", "现用 · 雾白", "#F4F6F4", "绿分量最高，发灰发脏"),
    ("2", "纯白", "#FFFFFF", "最干净，但偏冷硬"),
    ("3", "冷雾白", "#F7F9FA", "微冷蓝，与水感一致，干净 ★推荐"),
    ("4", "浅灰白", "#EFF2F3", "灰阶明显，卡片层次感强"),
]

CW, GAP, MG = 250, 42, 56
TOPL, ROWH = 108, 388
Wd = MG * 2 + 4 * CW + 3 * GAP
Ht = TOPL + ROWH * 2 + 40


def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


im = Image.new("RGB", (Wd, Ht), NEUTRAL)
d = ImageDraw.Draw(im)

d.text((MG, 30), "水滴观测站 · 定色对比", font=ImageFont.truetype(SANS, 30), fill=(22, 40, 50))
d.text((MG, 72), "上排：主色（头像 / 封面底色）    下排：底色（页面 / 纸面）", font=ImageFont.truetype(SANS, 15), fill=MUTE)


def block_row(items, y0, kind):
    d.text((MG, y0 - 30), "① 主色候选" if kind == "primary" else "② 底色候选",
           font=ImageFont.truetype(SANS, 18), fill=(22, 40, 50))
    for i, (tag, name, hexv, desc) in enumerate(items):
        x = MG + i * (CW + GAP)
        rgb = hex2rgb(hexv)
        d.rectangle([x, y0, x + CW, y0 + CW], fill=rgb, outline=LINE)
        if kind == "primary":
            # 主色块内画反白简版符号 + 反白标题
            B.render(im, B.MARK_SIMPLE, (x + CW / 2, y0 + CW * 0.40), CW * 0.46, "paper", canvas=B.S)
            f = ImageFont.truetype(SANS, 17)
            B.spaced(d, "水滴观测站", f, y0 + CW * 0.63, "paper", 3, x + CW / 2)
        else:
            # 底色块内画主色（用 B 组深海蓝）简版符号 + 主色标题
            B.render(im, B.MARK_SIMPLE, (x + CW / 2, y0 + CW * 0.40), CW * 0.46, "teal", canvas=B.S)
            # 覆盖成候选底色底，再重画
            d.rectangle([x + 1, y0 + 1, x + CW - 1, y0 + CW - 1], fill=rgb)
            B.render(im, B.MARK_SIMPLE, (x + CW / 2, y0 + CW * 0.40), CW * 0.46, "teal", canvas=B.S)
            f = ImageFont.truetype(SANS, 17)
            B.spaced(d, "水滴观测站", f, y0 + CW * 0.63, "teal", 3, x + CW / 2)
        # 标注
        ty = y0 + CW + 14
        d.text((x, ty), f"{tag}  {name}", font=ImageFont.truetype(SANS, 18), fill=(22, 40, 50))
        d.text((x, ty + 28), hexv, font=ImageFont.truetype(SANS, 14), fill=(176, 90, 31))
        d.text((x, ty + 52), desc, font=ImageFont.truetype(SANS, 13), fill=MUTE)


block_row(PRIMARY, TOPL, "primary")
block_row(GROUND, TOPL + ROWH, "ground")

im.save(OUT)
print("png:", OUT)
