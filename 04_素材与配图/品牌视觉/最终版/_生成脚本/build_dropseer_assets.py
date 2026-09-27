"""《水滴观测站 / DropSeer》品牌视觉 v2 —— 主符号「水银悬滴」
意象来源：《三体II》水滴（强互作用力宇宙探测器）。
核心美学：极致的美（一滴完美水银 / 全反射镜面 / 圣母的眼泪）+ 极致的简（绝对光滑，
放大一千万倍依然光滑——所以符号上**没有任何多余零件**）。
工艺：脚本精确制图；曲率连续贝塞尔；等宽笔画；无渐变、无发光、无立体感。
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

HEX = {
    "void":   "#0A0F14",  # 宇宙黑（主背景 —— 黑盒 / 深空）
    "silver": "#D2DBE4",  # 水银银（水滴主体 / 反白字）
    "paper":  "#F7F9FA",  # 冷雾白（亮底 / 反白字）
    "ink":    "#0E1418",  # 墨（单色 / 亮底反白）
    "amber":  "#B05A1F",  # 琥珀（风险信号，唯一暖色）
    "white":  "#FFFFFF",  # 镜面白（高光）
}
RGB = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in HEX.items()}

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
for sub in ("01_图标", "02_字标", "03_组合", "04_成品", "06_系列插图"):
    os.makedirs(os.path.join(ROOT, sub), exist_ok=True)

# ---------------- 全局制图常量 ----------------
S = 200            # 主符号画布
GLOSS_W = 6.0      # 镜面高光宽度
IS = 240           # 插图画布
MW, SW2 = 8, 5     # 插图主 / 次笔画
N = 30             # 贝塞尔 / 圆弧采样段数

FONT_CN_STACK = "'Noto Sans SC','Source Han Sans SC','Microsoft YaHei',sans-serif"
FONT_EN_STACK = "'Helvetica Neue',Arial,sans-serif"
SANS_CN = "C:/Windows/Fonts/msyhbd.ttc"
if not os.path.exists(SANS_CN):
    SANS_CN = "C:/Windows/Fonts/simhei.ttf"
SANS_EN = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(SANS_EN):
    SANS_EN = "C:/Windows/Fonts/arial.ttf"

CN_NAME = "水滴观测站"
EN_NAME = "DROPSEER"
TAGLINE = "知其白，守其黑"


def arc_pts(cx, cy, r, a0, a1, n=N):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]


def cubic(p0, c1, c2, p3, n=N):
    out = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        a, b, c, d = mt ** 3, 3 * mt * mt * t, 3 * mt * t * t, t ** 3
        out.append((a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0],
                    a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1]))
    return out


# ---------------- 主符号「水银悬滴」 ----------------
# 头部（底部）浑圆、尾部（尖端）极尖；曲率连续，尖端为真尖点
APEX_Y = 20.0             # 尖端（尾部）
DC = (100.0, 140.0)       # 底部椭圆中心
DRX, DRY = 40.0, 32.0     # 底部椭圆横/纵半径（最宽 80；ry<rx → 底部收尖不鼓；高 152，高宽比 1.90）
K1, K2 = 52.0, 24.0       # 上贝塞尔两控制点距离
GLOSS_S = 0.82            # 高光弧的轮廓缩放比（锚点=底部椭圆中心）
GLOSS_T0, GLOSS_T1 = 0.16, 0.62   # 高光弧覆盖的贝塞尔参数区间


def ellipse_pts(cx, cy, rx, ry, a0, a1, n=N):
    """椭圆弧采样（ry<rx 时为扁椭圆，底部收得更急、不鼓）"""
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]


def drop_ring(apex_y, cy, rx, ry, k1, k2, n=N):
    """悬滴闭合轮廓：尖端 → 左贝塞尔 → 底部椭圆弧 → 右贝塞尔 → 回尖端"""
    cx = DC[0]
    apex = (cx, apex_y)
    left = cubic(apex, (cx, apex_y + k1), (cx - rx, cy - k2), (cx - rx, cy), n)
    bottom = ellipse_pts(cx, cy, rx, ry, 180, 0, n)   # 180°→0°（经 90°=最低点）为椭圆下半
    right = cubic((cx + rx, cy), (cx + rx, cy - k2), (cx, apex_y + k1), apex, n)
    return left + bottom[1:] + right[1:]


def mark_drop(fill="silver", gloss_color="white", gloss=True):
    """水银悬滴：实心银滴 + 一道镜面高光（唯一细节，模拟全反射镜面）"""
    outer = drop_ring(APEX_Y, DC[1], DRX, DRY, K1, K2)
    prims = [("fillring", outer, fill)]
    if gloss:
        ga = DC[1] + (APEX_Y - DC[1]) * GLOSS_S
        gr = drop_ring(ga, DC[1], DRX * GLOSS_S, DRY * GLOSS_S, K1 * GLOSS_S, K2 * GLOSS_S)
        i0, i1 = int(GLOSS_T0 * N), int(GLOSS_T1 * N)
        prims.append(("curve", gr[i0:i1 + 1], GLOSS_W, gloss_color))
    return prims


def mark_box():
    """盒 · 见（辅）：黑盒顶边开一道缝，内部的点由此显形（用于黑盒/失效/风险主题）"""
    return [
        ("line", 58.0, 58.0, 84.0, 58.0, 13),
        ("line", 116.0, 58.0, 142.0, 58.0, 13),
        ("line", 142.0, 58.0, 142.0, 142.0, 13),
        ("line", 142.0, 142.0, 58.0, 142.0, 13),
        ("line", 58.0, 142.0, 58.0, 58.0, 13),
        ("dot", 100.0, 78.0, 10.0),
    ]


MARK = mark_drop("silver", "white", True)        # 全版：银滴 + 高光
MARK_SIMPLE = mark_drop("silver", None, False)   # 简版：银滴无高光（小尺寸）
MARK_INK = mark_drop("ink", None, False)         # 墨版：亮底 / 单色印刷
MARK_INK_GLOSS = mark_drop("ink", "white", True)  # 墨版：银底反转（黑曜石质感，保留高光）


# ---------------- 渲染层 ----------------
def _path(pts, close=False):
    d = f'M {pts[0][0]:.1f} {pts[0][1]:.1f} ' + ' '.join(f'L {x:.1f} {y:.1f}' for x, y in pts[1:])
    return d + (' Z' if close else '')


def svg_for(prims, color, bg=None, size=S):
    out = []
    if bg:
        out.append(f'<rect width="{size}" height="{size}" fill="{HEX[bg]}"/>')
    for p in prims:
        k = p[0]
        if k == "fillring":
            out.append(f'<path d="{_path(p[1], True)}" fill="{HEX[p[2]]}"/>')
        elif k == "curve":
            out.append(f'<path d="{_path(p[1])}" fill="none" stroke="{HEX[p[3]]}" stroke-width="{p[2]}" stroke-linecap="round" stroke-linejoin="round"/>')
        elif k == "circle":
            out.append(f'<circle cx="{p[1]}" cy="{p[2]}" r="{p[3]}" fill="none" stroke="{HEX[color]}" stroke-width="{p[4]}"/>')
        elif k == "dot":
            out.append(f'<circle cx="{p[1]}" cy="{p[2]}" r="{p[3]}" fill="{HEX[color]}"/>')
        elif k == "line":
            out.append(f'<line x1="{p[1]:.1f}" y1="{p[2]:.1f}" x2="{p[3]:.1f}" y2="{p[4]:.1f}" stroke="{HEX[color]}" stroke-width="{p[5]}" stroke-linecap="round"/>')
        elif k == "arc":
            out.append(f'<path d="{_path(arc_pts(p[1], p[2], p[3], p[4], p[5]))}" fill="none" stroke="{HEX[color]}" stroke-width="{p[6]}" stroke-linecap="round" stroke-linejoin="round"/>')
    return "\n  ".join(out)


def render(im, prims, center, size_px, color, canvas=None):
    d = ImageDraw.Draw(im)
    cs = canvas or S
    sc = size_px / cs
    ox, oy = center[0] - size_px / 2, center[1] - size_px / 2
    c = RGB[color]
    for p in prims:
        k = p[0]
        if k == "fillring":
            d.polygon([(ox + x * sc, oy + y * sc) for x, y in p[1]], fill=RGB[p[2]])
        elif k == "curve":
            pts = [(ox + x * sc, oy + y * sc) for x, y in p[1]]
            d.line(pts, fill=RGB[p[3]], width=max(1, int(round(p[2] * sc))), joint="curve")
        elif k == "circle":
            r, w = p[3] * sc, p[4] * sc
            d.ellipse([ox + p[1] * sc - r - w / 2, oy + p[2] * sc - r - w / 2,
                       ox + p[1] * sc + r + w / 2, oy + p[2] * sc + r + w / 2],
                      outline=c, width=max(1, int(round(w))))
        elif k == "dot":
            r = p[3] * sc
            x, y = ox + p[1] * sc, oy + p[2] * sc
            d.ellipse([x - r, y - r, x + r, y + r], fill=c)
        elif k == "line":
            d.line([(ox + p[1] * sc, oy + p[2] * sc), (ox + p[3] * sc, oy + p[4] * sc)],
                   fill=c, width=max(1, int(round(p[5] * sc))), joint="curve")
        elif k == "arc":
            pts = [(ox + x * sc, oy + y * sc) for x, y in arc_pts(p[1], p[2], p[3], p[4], p[5])]
            d.line(pts, fill=c, width=max(1, int(round(p[6] * sc))), joint="curve")


def write_svg(path, body, vb):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb[0]} {vb[1]}">\n  {body}\n</svg>\n')
    print("svg:", os.path.relpath(path, ROOT))


def divider_svg(x1, x2, y, color, k=1.0):
    s = [f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{HEX[color]}" stroke-width="{1.1*k:.2f}" opacity="0.85"/>']
    for i in range(3):
        tx = x1 + (x2 - x1) * i / 2
        s.append(f'<line x1="{tx:.1f}" y1="{y-4.5*k:.1f}" x2="{tx:.1f}" y2="{y+4.5*k:.1f}" stroke="{HEX[color]}" stroke-width="{1.1*k:.2f}" opacity="0.85"/>')
    return "".join(s)


def divider_px(d, x1, x2, y, color, k=1.0):
    c = RGB[color]
    wd = max(1, int(round(1.2 * k)))
    d.line([(x1, y), (x2, y)], fill=c, width=wd)
    for i in range(3):
        tx = x1 + (x2 - x1) * i / 2
        d.line([(tx, y - 4.5 * k), (tx, y + 4.5 * k)], fill=c, width=wd)


def spaced(d, text, font, y, color, spacing, center_x):
    ws = [d.textlength(ch, font=font) for ch in text]
    total = sum(ws) + spacing * (len(text) - 1)
    x = center_x - total / 2
    for ch, w in zip(text, ws):
        d.text((x, y), ch, font=font, fill=RGB[color])
        x += w + spacing


def spaced_at(d, text, font, x0, y, color, spacing):
    x = x0
    for ch in text:
        d.text((x, y), ch, font=font, fill=RGB[color])
        x += d.textlength(ch, font=font) + spacing


# ---------------- 字标 / 组合 ----------------
def wordmark_h(color="silver", bg=None):
    b = f'<rect width="620" height="196" fill="{HEX[bg]}"/>' if bg else ""
    return f'''{b}
  <text x="310" y="104" text-anchor="middle" font-family="{FONT_CN_STACK}" font-weight="900" font-size="58" letter-spacing="7" fill="{HEX[color]}">{CN_NAME}</text>
  {divider_svg(190, 430, 134, color)}
  <text x="310" y="162" text-anchor="middle" font-family="{FONT_EN_STACK}" font-size="12.6" letter-spacing="5.4" fill="{HEX[color]}" opacity="0.75">{EN_NAME}</text>''', (620, 196)


def lockup_h(color="silver", bg=None):
    b = f'<rect width="620" height="200" fill="{HEX[bg]}"/>' if bg else ""
    return f'''{b}
  <g transform="translate(6,6) scale(0.94)">{svg_for(MARK, color)}</g>
  <text x="212" y="108" font-family="{FONT_CN_STACK}" font-weight="900" font-size="58" letter-spacing="6" fill="{HEX[color]}">{CN_NAME}</text>
  {divider_svg(216, 420, 132, color)}
  <text x="216" y="158" font-family="{FONT_EN_STACK}" font-size="12.5" letter-spacing="4.6" fill="{HEX[color]}" opacity="0.75">{EN_NAME}</text>''', (620, 200)


def lockup_v(color="silver", bg=None):
    b = f'<rect width="380" height="480" fill="{HEX[bg]}"/>' if bg else ""
    return f'''{b}
  <g transform="translate(90,6)">{svg_for(MARK, color)}</g>
  <text x="190" y="296" text-anchor="middle" font-family="{FONT_CN_STACK}" font-weight="900" font-size="58" letter-spacing="6" fill="{HEX[color]}">{CN_NAME}</text>
  {divider_svg(95, 285, 324, color)}
  <text x="190" y="352" text-anchor="middle" font-family="{FONT_EN_STACK}" font-size="12.4" letter-spacing="5" fill="{HEX[color]}" opacity="0.75">{EN_NAME}</text>''', (380, 480)


# ---------------- 成品 ----------------
def avatar(px, bg, fg, tag, prims=None, with_en=True):
    im = Image.new("RGB", (px, px), RGB[bg])
    d = ImageDraw.Draw(im)
    render(im, prims or MARK, (px / 2, px * 0.40), px * 0.44, fg)
    spaced(d, CN_NAME, ImageFont.truetype(SANS_CN, int(px * 0.088)), px * 0.655, fg, int(px * 0.018), px / 2)
    if with_en:
        spaced(d, EN_NAME, ImageFont.truetype(SANS_EN, int(px * 0.023)), px * 0.775, fg, int(px * 0.0065), px / 2)
    p = os.path.join(ROOT, "04_成品", f"头像_{tag}_{px}.png")
    im.save(p)
    print("png:", os.path.basename(p))


def cover_sq(px, bg, fg, tag, series=TAGLINE, series_color=None, prims=None):
    sc_c = series_color or fg
    im = Image.new("RGB", (px, px), RGB[bg])
    d = ImageDraw.Draw(im)
    render(im, prims or MARK, (px / 2, px * 0.29), px * 0.23, fg)
    spaced(d, CN_NAME, ImageFont.truetype(SANS_CN, int(px * 0.120)), px * 0.485, fg, int(px * 0.024), px / 2)
    divider_px(d, px * 0.325, px * 0.675, px * 0.605, fg, px / 3000 * 2.4)
    spaced(d, EN_NAME, ImageFont.truetype(SANS_EN, int(px * 0.024)), px * 0.655, fg, int(px * 0.0075), px / 2)
    spaced(d, series, ImageFont.truetype(SANS_CN, int(px * 0.044)), px * 0.775, sc_c, int(px * 0.013), px / 2)
    p = os.path.join(ROOT, "04_成品", f"封面_{tag}_{px}.png")
    im.save(p, quality=94)
    print("png:", os.path.basename(p))


def cover_wide(w, h, bg, fg, tag, series=TAGLINE, series_color=None, prims=None):
    sc_c = series_color or fg
    k = h / 383.0
    im = Image.new("RGB", (w, h), RGB[bg])
    d = ImageDraw.Draw(im)
    render(im, prims or MARK, (w * 0.155, h * 0.47), h * 0.52, fg)
    tx = w * 0.335
    avail = w * 0.96 - tx
    fs_cn = min(h * 0.195, avail / 5.45)
    sp = fs_cn * 0.10
    f = ImageFont.truetype(SANS_CN, int(fs_cn))
    spaced_at(d, CN_NAME, f, tx, h * 0.245, fg, sp)
    divider_px(d, tx, tx + avail * 0.44, h * 0.585, fg, k * 1.6)
    fe = ImageFont.truetype(SANS_EN, int(h * 0.042))
    spaced_at(d, EN_NAME, fe, tx, h * 0.632, fg, h * 0.015)
    fs = ImageFont.truetype(SANS_CN, int(h * 0.066))
    spaced_at(d, series, fs, tx, h * 0.752, sc_c, h * 0.021)
    p = os.path.join(ROOT, "04_成品", f"封面_{tag}_{w}x{h}.png")
    im.save(p, quality=94)
    print("png:", os.path.basename(p))


# ---------------- 系列插图（几何化，暗底用反白银 / 亮底用墨） ----------------
def ill_probe():
    return [("line", 68.0, 34.0, 126.0, 128.0, MW),
            ("circle", 150.0, 158.0, 34.0, MW),
            ("dot", 150.0, 158.0, 7.0)]


def ill_wave():
    p = [("dot", 120.0, 158.0, 9.0)]
    for r in (34.0, 58.0, 82.0):
        p.append(("arc", 120.0, 158.0, r, 200.0, 340.0, SW2))
    return p


def ill_gauge():
    p = [("arc", 120.0, 150.0, 70.0, 180.0, 360.0, MW)]
    for ang in (180.0, 270.0, 360.0):
        a = math.radians(ang)
        p.append(("line", 120 + 56 * math.cos(a), 150 + 56 * math.sin(a),
                  120 + 66 * math.cos(a), 150 + 66 * math.sin(a), SW2))
    p.append(("line", 120.0, 150.0, 165.9, 117.9, MW))
    p.append(("dot", 120.0, 150.0, 7.0))
    return p


def ill_trace():
    return [("line", 40.0, 166.0, 90.0, 166.0, SW2),
            ("line", 90.0, 166.0, 120.0, 112.0, SW2),
            ("line", 120.0, 112.0, 156.0, 112.0, SW2),
            ("line", 156.0, 112.0, 196.0, 166.0, SW2),
            ("dot", 40.0, 166.0, 7.0),
            ("dot", 120.0, 112.0, 7.0),
            ("dot", 156.0, 112.0, 7.0),
            ("circle", 196.0, 166.0, 10.0, SW2)]


def ill_fault():
    return [("line", 66.0, 66.0, 174.0, 66.0, MW),
            ("line", 174.0, 66.0, 174.0, 174.0, MW),
            ("line", 174.0, 174.0, 66.0, 174.0, MW),
            ("line", 66.0, 174.0, 66.0, 66.0, MW),
            ("line", 120.0, 66.0, 106.0, 104.0, MW),
            ("line", 106.0, 104.0, 134.0, 132.0, MW),
            ("line", 134.0, 132.0, 116.0, 174.0, MW)]


def ill_log():
    return [("dot", 46.0, 92.0, 5.0), ("line", 62.0, 92.0, 190.0, 92.0, SW2),
            ("dot", 46.0, 126.0, 5.0), ("line", 62.0, 126.0, 150.0, 126.0, SW2),
            ("dot", 46.0, 160.0, 5.0), ("line", 62.0, 160.0, 190.0, 160.0, SW2)]


ILLS = [("probe", "探 · 试探", ill_probe), ("wave", "波 · 回波", ill_wave),
        ("gauge", "度 · 度量", ill_gauge), ("trace", "迹 · 链路", ill_trace),
        ("fault", "罅 · 失效", ill_fault), ("log", "录 · 复盘", ill_log)]


def contact_sheet(cell=380, cols=3, pad=20, bg="void", fg="silver"):
    rows = (len(ILLS) + cols - 1) // cols
    Wd, Ht = cols * cell + 2 * pad, rows * cell + 2 * pad
    im = Image.new("RGB", (Wd, Ht), RGB[bg])
    d = ImageDraw.Draw(im)
    for i, (key, label, fn) in enumerate(ILLS):
        cx = pad + (i % cols) * cell + cell / 2
        cy = pad + (i // cols) * cell + cell / 2
        render(im, fn(), (cx, cy - 8), cell * 0.56, fg, canvas=IS)
        f = ImageFont.truetype(SANS_CN, 15)
        spaced(d, label, f, cy + cell * 0.30, fg, 3, cx)
    p = os.path.join(ROOT, "06_系列插图", "_系列插图_全览.png")
    im.save(p)
    print("png:", os.path.basename(p))


# ---------------- 主程序 ----------------
if __name__ == "__main__":
    ICON = os.path.join(ROOT, "01_图标")
    write_svg(os.path.join(ICON, "mark_drop.svg"), svg_for(MARK, "silver"), (S, S))
    write_svg(os.path.join(ICON, "mark_drop_simple.svg"), svg_for(MARK_SIMPLE, "silver"), (S, S))
    write_svg(os.path.join(ICON, "mark_drop_ink.svg"), svg_for(MARK_INK, "ink"), (S, S))
    write_svg(os.path.join(ICON, "mark_drop_on_void.svg"), svg_for(MARK, "silver", bg="void"), (S, S))
    for c, tag in (("silver", "silver"), ("ink", "ink"), ("amber", "amber")):
        write_svg(os.path.join(ICON, f"mark_box_{tag}.svg"), svg_for(mark_box(), c), (S, S))
    write_svg(os.path.join(ICON, "mark_box_on_void.svg"), svg_for(mark_box(), "silver", bg="void"), (S, S))

    for c, fn in (("silver", "wordmark_h.svg"), ("white", "wordmark_h_white.svg"), ("ink", "wordmark_h_ink.svg")):
        b, vb = wordmark_h(c)
        write_svg(os.path.join(ROOT, "02_字标", fn), b, vb)

    for c, fn in (("silver", "lockup_h.svg"), ("white", "lockup_h_white.svg")):
        b, vb = lockup_h(c)
        write_svg(os.path.join(ROOT, "03_组合", fn), b, vb)
    for c, fn in (("silver", "lockup_v.svg"), ("white", "lockup_v_white.svg")):
        b, vb = lockup_v(c)
        write_svg(os.path.join(ROOT, "03_组合", fn), b, vb)

    avatar(1200, "void", "silver", "宇宙黑底")
    avatar(800, "void", "silver", "宇宙黑底")
    avatar(1200, "silver", "ink", "水银底", prims=MARK_INK_GLOSS)
    cover_sq(3000, "void", "silver", "方形", series=TAGLINE, series_color="amber")
    cover_sq(3000, "silver", "ink", "特别期", series=TAGLINE, series_color="amber", prims=MARK_INK_GLOSS)
    cover_wide(900, 383, "void", "silver", "公众号", series=TAGLINE, series_color="amber")
    cover_wide(900, 383, "void", "silver", "公众号_热点周报", series="热点周报", series_color="amber")
    cover_wide(1920, 1080, "void", "silver", "16x9", series=TAGLINE, series_color="amber")

    ILLD = os.path.join(ROOT, "06_系列插图")
    for key, label, fn in ILLS:
        for c, tag in (("silver", "silver"), ("amber", "amber"), ("white", "white"), ("ink", "ink")):
            write_svg(os.path.join(ILLD, f"ill_{key}_{tag}.svg"), svg_for(fn(), c, size=IS), (IS, IS))
        write_svg(os.path.join(ILLD, f"ill_{key}_on_void.svg"), svg_for(fn(), "silver", bg="void", size=IS), (IS, IS))
    contact_sheet()

    print("\n完成 ->", ROOT)
