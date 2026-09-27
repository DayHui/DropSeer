"""《水滴观测站》文章插图 —— 基于「水银悬滴」风格的公众号正文配图
风格纪律：宇宙黑底 + 实心水银银 + 一道镜面高光 + 琥珀仅作风险/异常标记；极简、留白大。
复用主符号的悬滴轮廓（drop_ring），保证形状与品牌符号一致。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import build_dropseer_assets as B

VOID = B.RGB["void"]; SILVER = B.RGB["silver"]; WHITE = B.RGB["white"]
AMBER = B.RGB["amber"]; INK = B.RGB["ink"]
BOX = (19, 26, 34)          # 黑盒（比宇宙黑略亮一档）
SILVER_DIM = (150, 162, 174)  # 弱化水银（次要线）

OUT = os.path.join(B.ROOT, "07_文章插图")
os.makedirs(OUT, exist_ok=True)

_RING = B.drop_ring(B.APEX_Y, B.DC[1], B.DRX, B.DRY, B.K1, B.K2)
_RX = [p[0] for p in _RING]; _RY = [p[1] for p in _RING]
_OX, _OY, _OW, _OH = min(_RX), min(_RY), max(_RX) - min(_RX), max(_RY) - min(_RY)
_GLOSS = B.mark_drop("silver", "white", True)[1][1]  # 高光弧点（同坐标系）


def drop_pts(cx, cy, w, h):
    return [((p[0] - _OX) / _OW * w + (cx - w / 2), (p[1] - _OY) / _OH * h + (cy - h / 2)) for p in _RING]


def draw_drop(im, cx, cy, w, h, fill=SILVER, gloss=True, gloss_color=WHITE):
    d = ImageDraw.Draw(im)
    d.polygon(drop_pts(cx, cy, w, h), fill=fill)
    if gloss:
        gp = [((p[0] - _OX) / _OW * w + (cx - w / 2), (p[1] - _OY) / _OH * h + (cy - h / 2)) for p in _GLOSS]
        gw = max(1, int(round(6.0 * w / 80)))
        d.line(gp, fill=gloss_color, width=gw, joint="curve")


def arc_pts(cx, cy, r, a0, a1, n=60):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]


def canvas(w, h):
    im = Image.new("RGB", (w, h), VOID)
    return im, ImageDraw.Draw(im)


# ============ 场景 1：黑盒 ============
def scene_blackbox(w, h):
    im, d = canvas(w, h)
    cx, cy = w / 2, h / 2
    bw, bh = 320, 220
    x0, y0 = cx - bw / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=18, fill=BOX, outline=SILVER, width=2)
    # 顶部镜面反光边
    d.line([(x0 + 26, y0 + 3), (x0 + bw - 26, y0 + 3)], fill=WHITE, width=2)
    # 琥珀裂缝
    crack = [(cx, y0 + 4), (cx - 26, y0 + 74), (cx + 18, y0 + 112), (cx - 8, y0 + bh - 4)]
    d.line(crack, fill=AMBER, width=3, joint="curve")
    d.ellipse([cx - 8 - 6, y0 + bh - 4 - 6, cx - 8 + 6, y0 + bh - 4 + 6], fill=AMBER)
    return im


# ============ 场景 2：水滴入黑盒 ============
def scene_drop_into_box(w, h):
    im, d = canvas(w, h)
    cx = w / 2
    draw_drop(im, cx, h * 0.42, 120, 220)
    bw, bh = 300, 180
    x0, y0 = cx - bw / 2, h * 0.68
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=14, fill=BOX, outline=SILVER, width=2)
    # 顶部开口缝
    d.line([(x0 + bw * 0.32, y0 + 2), (x0 + bw * 0.68, y0 + 2)], fill=AMBER, width=3)
    return im


# ============ 场景 3：Agent 链路 ============
def scene_chain(w, h):
    im, d = canvas(w, h)
    n = 5
    xs = [w * (0.18 + 0.16 * i) for i in range(n)]
    cy = h * 0.5
    dw, dh = 92, 165
    for i, x in enumerate(xs):
        fill = AMBER if i == 2 else SILVER
        draw_drop(im, x, cy, dw, dh, fill=fill)
    # 连接线（滴之间）
    for i in range(n - 1):
        x1 = xs[i] + dw / 2 - 2
        x2 = xs[i + 1] - dw / 2 + 2
        if i == 2:  # 第 3→4 之间断裂
            d.line([(x1, cy - dh * 0.2), (x1 + (x2 - x1) * 0.4, cy - dh * 0.2)], fill=SILVER, width=2)
            d.ellipse([x2 - 5, cy - dh * 0.2 - 5, x2 + 5, cy - dh * 0.2 + 5], fill=AMBER)
        else:
            d.line([(x1, cy - dh * 0.2), (x2, cy - dh * 0.2)], fill=SILVER, width=2)
    return im


# ============ 场景 4：评测仪表 ============
def scene_gauge(w, h):
    im, d = canvas(w, h)
    cx, cy, r = w / 2, h * 0.58, 200
    d.line(arc_pts(cx, cy, r, 180, 360), fill=SILVER, width=3, joint="curve")
    d.line(arc_pts(cx, cy, r, 306, 360), fill=AMBER, width=3, joint="curve")
    for a in (180, 225, 270, 315, 360):
        rad = math.radians(a)
        d.line([(cx + (r - 16) * math.cos(rad), cy + (r - 16) * math.sin(rad)),
                (cx + (r - 30) * math.cos(rad), cy + (r - 30) * math.sin(rad))], fill=SILVER_DIM, width=2)
    # 指针指向 45°（危险区方向）
    pr = r * 0.78
    d.line([(cx, cy), (cx + pr * 0.707, cy - pr * 0.707)], fill=SILVER, width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=SILVER)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=AMBER)
    return im


# ============ 场景 5：四类失效 ============
def scene_four_faults(w, h):
    im, d = canvas(w, h)
    cxs = [w * (0.14 + 0.24 * i) for i in range(4)]
    cy, rr = h * 0.46, 88
    for x in cxs:
        d.ellipse([x - rr, cy - rr, x + rr, cy + rr], outline=SILVER, width=2)
        draw_drop(im, x, cy, 62, 110)
    my = h * 0.82
    # 幻觉：实心点
    d.ellipse([cxs[0] - 7, my - 7, cxs[0] + 7, my + 7], fill=AMBER)
    # 工具调用：交叉
    for sx in (-1, 1):
        d.line([(cxs[1] - 12, my - 12 * sx), (cxs[1] + 12, my + 12 * sx)], fill=AMBER, width=3)
    # 规划失效：分叉
    d.line([(cxs[2], my - 14), (cxs[2], my)], fill=AMBER, width=3)
    d.line([(cxs[2], my), (cxs[2] - 12, my + 13)], fill=AMBER, width=3)
    d.line([(cxs[2], my), (cxs[2] + 12, my + 13)], fill=AMBER, width=3)
    # 版本退化：下降箭头
    d.line([(cxs[3] - 14, my - 10), (cxs[3] + 14, my + 10)], fill=AMBER, width=3)
    d.line([(cxs[3] + 14, my + 10), (cxs[3] + 2, my + 4)], fill=AMBER, width=3)
    d.line([(cxs[3] + 14, my + 10), (cxs[3] + 10, my + 22)], fill=AMBER, width=3)
    return im


# ============ 场景 6：观测 ============
def scene_observe(w, h):
    im, d = canvas(w, h)
    cx, cy = w / 2, h * 0.5
    for r, wd in ((190, 2), (140, 2), (90, 2)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=SILVER, width=wd)
    d.line([(cx - 230, cy), (cx + 230, cy)], fill=SILVER_DIM, width=1)
    d.line([(cx, cy - 230), (cx, cy + 230)], fill=SILVER_DIM, width=1)
    draw_drop(im, cx, cy, 78, 140)
    # 探测点（45° 外环上）
    a = math.radians(45)
    px, py = cx + 190 * math.cos(a), cy - 190 * math.sin(a)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=AMBER)
    return im


# ============ 场景 7：信号波形 ============
def scene_wave(w, h):
    im, d = canvas(w, h)
    cy = h * 0.5
    pts = []
    for i in range(140):
        x = w * 0.12 + (w * 0.76) * i / 139
        y = cy + 78 * math.sin(i * 0.22)
        pts.append((x, y))
    # 从中段断裂
    break_a, break_b = 48, 92
    d.line(pts[:break_a], fill=SILVER, width=3, joint="curve")
    d.line(pts[break_b:], fill=SILVER, width=3, joint="curve")
    gx = (pts[break_a - 1][0] + pts[break_b][0]) / 2
    d.line([(pts[break_a - 1][0], cy - 60), (pts[break_b][0], cy + 60)], fill=AMBER, width=3)
    d.ellipse([gx - 7, cy - 7, gx + 7, cy + 7], fill=AMBER)
    return im


# ============ 场景 8：编队 ============
def scene_team(w, h):
    im, d = canvas(w, h)
    bx, by = w / 2, h * 0.56
    draw_drop(im, bx, by, 132, 240)
    smalls = [(w * 0.26, h * 0.62), (w * 0.37, h * 0.30), (w * 0.63, h * 0.30),
              (w * 0.74, h * 0.62), (w * 0.50, h * 0.16)]
    for sx, sy in smalls:
        d.line([(bx - 10, by - 40), (sx, sy + 20)], fill=SILVER_DIM, width=1)
        draw_drop(im, sx, sy, 52, 94, gloss=False)
    return im


# ============ 场景 9：分隔符 ============
def scene_divider(w, h):
    im, d = canvas(w, h)
    cx, cy = w / 2, h / 2
    draw_drop(im, cx, cy, 40, 72)
    d.line([(cx - 90, cy), (cx - 48, cy)], fill=SILVER_DIM, width=2)
    d.line([(cx + 48, cy), (cx + 90, cy)], fill=SILVER_DIM, width=2)
    return im


SCENES = [
    ("文章插图_黑盒", scene_blackbox, (1200, 675)),
    ("文章插图_水滴入黑盒", scene_drop_into_box, (1200, 675)),
    ("文章插图_Agent链路", scene_chain, (1200, 675)),
    ("文章插图_评测仪表", scene_gauge, (1200, 675)),
    ("文章插图_四类失效", scene_four_faults, (1200, 675)),
    ("文章插图_观测", scene_observe, (1200, 675)),
    ("文章插图_信号波形", scene_wave, (1200, 675)),
    ("文章插图_编队", scene_team, (1200, 675)),
    ("文章插图_分隔符", scene_divider, (480, 200)),
]


def contact():
    th = 240
    cell = 360
    cols = 3
    rows = (len(SCENES) + cols - 1) // cols
    im = Image.new("RGB", (cols * cell + 60, rows * (th + 40) + 60), VOID)
    for i, (name, fn, (sw, sh)) in enumerate(SCENES):
        s = fn(sw, sh)
        s = s.resize((cell, int(cell * sh / sw)), Image.LANCZOS)
        x = 30 + (i % cols) * cell
        y = 30 + (i // cols) * (th + 40)
        im.paste(s, (x, y))
    p = os.path.join(OUT, "_文章插图_全览.png")
    im.save(p)
    print("png:", os.path.basename(p))


if __name__ == "__main__":
    for name, fn, (sw, sh) in SCENES:
        im = fn(sw, sh)
        p = os.path.join(OUT, name + ".png")
        im.save(p)
        print("png:", name)
    contact()
    print("\n完成 ->", OUT)
