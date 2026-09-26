"""《水滴观测站 / DropSeer》品牌视觉 v1 —— 主符号「滴·测」+ 辅符号「盒·见」
自包含：图标 / 字标 / 组合 SVG + 各平台成品 PNG + 六张系列插图
工艺基准对齐《时空茶馆》定案 v9：等宽笔画、亮底单色、脚本精确制图。
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

HEX = {"teal": "#16404D", "amber": "#B05A1F", "paper": "#F4F6F4",
       "ink": "#15191B", "aqua": "#3E7C8F", "white": "#FFFFFF"}
RGB = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in HEX.items()}

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
for sub in ("01_图标", "02_字标", "03_组合", "04_成品", "06_系列插图"):
    os.makedirs(os.path.join(ROOT, sub), exist_ok=True)

# ---------------- 全局制图常量（改规格只动这里） ----------------
S = 200          # 主符号画布
W = 13           # 主笔画厚度
SW = 8           # 次笔画厚度（刻度 / 波纹）
IS = 240         # 插图画布
MW, SW2 = 8, 5   # 插图主 / 次笔画

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
TAGLINE = "黑盒之外 · 冷静观测"


def arc_pts(cx, cy, r, a0, a1, n=48):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]


# ---------------- 主符号「滴·测」 ----------------
APEX = (100.0, 52.0)     # 水滴尖端
DC = (100.0, 114.0)      # 水滴圆心
DR = 44.0                # 水滴半径
LINE_TOP = 14.0          # 垂线起点（几乎触到画布上缘：从画面外探入）


def _tangent_points():
    """过 APEX 作圆的两条切线的切点"""
    dx, dy = APEX[0] - DC[0], APEX[1] - DC[1]
    d = math.hypot(dx, dy)
    a = math.degrees(math.acos(DR / d))
    base = math.degrees(math.atan2(dy, dx))
    out = []
    for sgn in (-1, 1):
        th = math.radians(base + sgn * a)
        out.append((DC[0] + DR * math.cos(th), DC[1] + DR * math.sin(th)))
    return out


T1, T2 = _tangent_points()


def mark_drop(ripple=True):
    """滴·测（全）：垂线 + 空心水滴（圆 + 两切线）+ 中心点 + 波纹弧"""
    p = [("line", APEX[0], LINE_TOP, APEX[1], 0.0, W)]  # placeholder, replaced below
    p = [("line", DC[0], LINE_TOP, DC[0], APEX[1], W)]
    p.append(("circle", DC[0], DC[1], DR, W))
    p.append(("line", APEX[0], APEX[1], T1[0], T1[1], W))
    p.append(("line", APEX[0], APEX[1], T2[0], T2[1], W))
    if ripple:
        p.append(("arc", DC[0], DC[1], 62.0, 40.0, 140.0, SW))
        p.append(("arc", DC[0], DC[1], 78.0, 40.0, 140.0, SW))
    p.append(("dot", DC[0], DC[1], 11.0))
    return p


def mark_box():
    """盒·见（辅）：黑盒顶边开一道缝，里面的点由此显形"""
    return [
        ("line", 58.0, 58.0, 84.0, 58.0, W),
        ("line", 116.0, 58.0, 142.0, 58.0, W),
        ("line", 142.0, 58.0, 142.0, 142.0, W),
        ("line", 142.0, 142.0, 58.0, 142.0, W),
        ("line", 58.0, 142.0, 58.0, 58.0, W),
        ("dot", 100.0, 78.0, 10.0),
    ]


MARK = mark_drop(True)
MARK_SIMPLE = mark_drop(False)
MARK_BOX = mark_box()


# ---------------- 渲染层 ----------------
def svg_for(prims, color, bg=None, size=S):
    out = []
    if bg:
        out.append(f'<rect width="{size}" height="{size}" fill="{HEX[bg]}"/>')
    for p in prims:
        k = p[0]
        if k == "circle":
            out.append(f'<circle cx="{p[1]}" cy="{p[2]}" r="{p[3]}" fill="none" stroke="{HEX[color]}" stroke-width="{p[4]}"/>')
        elif k == "dot":
            out.append(f'<circle cx="{p[1]}" cy="{p[2]}" r="{p[3]}" fill="{HEX[color]}"/>')
        elif k == "line":
            out.append(f'<line x1="{p[1]:.1f}" y1="{p[2]:.1f}" x2="{p[3]:.1f}" y2="{p[4]:.1f}" stroke="{HEX[color]}" stroke-width="{p[5]}" stroke-linecap="round"/>')
        elif k == "arc":
            pts = arc_pts(p[1], p[2], p[3], p[4], p[5])
            d = f'M {pts[0][0]:.1f} {pts[0][1]:.1f} ' + ' '.join(f'L {x:.1f} {y:.1f}' for x, y in pts[1:])
            out.append(f'<path d="{d}" fill="none" stroke="{HEX[color]}" stroke-width="{p[6]}" stroke-linecap="round" stroke-linejoin="round"/>')
        elif k == "poly":
            pts = p[1]
            d = f'M {pts[0][0]:.1f} {pts[0][1]:.1f} ' + ' '.join(f'L {x:.1f} {y:.1f}' for x, y in pts[1:]) + ' Z'
            out.append(f'<path d="{d}" fill="{HEX[color]}"/>')
    return "\n  ".join(out)


def render(im, prims, center, size_px, color, canvas=None):
    d = ImageDraw.Draw(im)
    cs = canvas or S
    sc = size_px / cs
    ox, oy = center[0] - size_px / 2, center[1] - size_px / 2
    c = RGB[color]
    for p in prims:
        k = p[0]
        if k == "circle":
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
        elif k == "poly":
            d.polygon([(ox + x * sc, oy + y * sc) for x, y in p[1]], fill=c)


def write_svg(path, body, vb):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb[0]} {vb[1]}">\n  {body}\n</svg>\n')
    print("svg:", os.path.relpath(path, ROOT))


def divider_svg(x1, x2, y, color, k=1.0):
    """刻度尺式分隔线：一条细线 + 三道短刻度（区别于时空茶馆的「线 + 中心点」）"""
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
def wordmark_h(color="teal", bg=None):
    b = f'<rect width="620" height="196" fill="{HEX[bg]}"/>' if bg else ""
    return f'''{b}
  <text x="310" y="104" text-anchor="middle" font-family="{FONT_CN_STACK}" font-weight="900" font-size="58" letter-spacing="7" fill="{HEX[color]}">{CN_NAME}</text>
  {divider_svg(190, 430, 134, color)}
  <text x="310" y="162" text-anchor="middle" font-family="{FONT_EN_STACK}" font-size="12.6" letter-spacing="5.4" fill="{HEX[color]}" opacity="0.75">{EN_NAME}</text>''', (620, 196)


def lockup_h(color="teal", bg=None):
    b = f'<rect width="620" height="200" fill="{HEX[bg]}"/>' if bg else ""
    return f'''{b}
  <g transform="translate(6,6) scale(0.94)">{svg_for(MARK, color)}</g>
  <text x="212" y="108" font-family="{FONT_CN_STACK}" font-weight="900" font-size="58" letter-spacing="6" fill="{HEX[color]}">{CN_NAME}</text>
  {divider_svg(216, 420, 132, color)}
  <text x="216" y="158" font-family="{FONT_EN_STACK}" font-size="12.5" letter-spacing="4.6" fill="{HEX[color]}" opacity="0.75">{EN_NAME}</text>''', (620, 200)


def lockup_v(color="teal", bg=None):
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
    k = px / 3000.0
    im = Image.new("RGB", (px, px), RGB[bg])
    d = ImageDraw.Draw(im)
    render(im, prims or MARK, (px / 2, px * 0.29), px * 0.23, fg)
    spaced(d, CN_NAME, ImageFont.truetype(SANS_CN, int(px * 0.120)), px * 0.485, fg, int(px * 0.024), px / 2)
    divider_px(d, px * 0.325, px * 0.675, px * 0.605, fg, k * 2.4)
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


# ---------------- 系列插图（240×240，等宽笔画，几何化） ----------------
def ill_probe():
    """探 · 试探：一根探针逼近靶环"""
    return [("line", 68.0, 34.0, 126.0, 128.0, MW),
            ("circle", 150.0, 158.0, 34.0, MW),
            ("dot", 150.0, 158.0, 7.0)]


def ill_wave():
    """波 · 回波：声呐式的探测波纹"""
    p = [("dot", 120.0, 158.0, 9.0)]
    for r in (34.0, 58.0, 82.0):
        p.append(("arc", 120.0, 158.0, r, 200.0, 340.0, SW2))
    return p


def ill_gauge():
    """度 · 度量：一块只剩半边的刻度盘 + 指针"""
    p = [("arc", 120.0, 150.0, 70.0, 180.0, 360.0, MW)]
    for ang in (180.0, 270.0, 360.0):
        a = math.radians(ang)
        p.append(("line", 120 + 56 * math.cos(a), 150 + 56 * math.sin(a),
                  120 + 66 * math.cos(a), 150 + 66 * math.sin(a), SW2))
    p.append(("line", 120.0, 150.0, 165.9, 117.9, MW))
    p.append(("dot", 120.0, 150.0, 7.0))
    return p


def ill_trace():
    """迹 · 链路：一条带节点的观测轨迹，末节点是空的（待核验）"""
    return [("line", 40.0, 166.0, 90.0, 166.0, SW2),
            ("line", 90.0, 166.0, 120.0, 112.0, SW2),
            ("line", 120.0, 112.0, 156.0, 112.0, SW2),
            ("line", 156.0, 112.0, 196.0, 166.0, SW2),
            ("dot", 40.0, 166.0, 7.0),
            ("dot", 120.0, 112.0, 7.0),
            ("dot", 156.0, 112.0, 7.0),
            ("circle", 196.0, 166.0, 10.0, SW2)]


def ill_fault():
    """罅 · 失效：黑盒裂开一道贯穿的缝"""
    return [("line", 66.0, 66.0, 174.0, 66.0, MW),
            ("line", 174.0, 66.0, 174.0, 174.0, MW),
            ("line", 174.0, 174.0, 66.0, 174.0, MW),
            ("line", 66.0, 174.0, 66.0, 66.0, MW),
            ("line", 120.0, 66.0, 106.0, 104.0, MW),
            ("line", 106.0, 104.0, 134.0, 132.0, MW),
            ("line", 134.0, 132.0, 116.0, 174.0, MW)]


def ill_log():
    """录 · 复盘：三条观测记录，其中一条短一截"""
    return [("dot", 46.0, 92.0, 5.0), ("line", 62.0, 92.0, 190.0, 92.0, SW2),
            ("dot", 46.0, 126.0, 5.0), ("line", 62.0, 126.0, 150.0, 126.0, SW2),
            ("dot", 46.0, 160.0, 5.0), ("line", 62.0, 160.0, 190.0, 160.0, SW2)]


ILLS = [("probe", "探 · 试探", ill_probe), ("wave", "波 · 回波", ill_wave),
        ("gauge", "度 · 度量", ill_gauge), ("trace", "迹 · 链路", ill_trace),
        ("fault", "罅 · 失效", ill_fault), ("log", "录 · 复盘", ill_log)]


def contact_sheet(cell=380, cols=3, pad=20, bg="paper"):
    rows = (len(ILLS) + cols - 1) // cols
    Wd, Ht = cols * cell + 2 * pad, rows * cell + 2 * pad
    im = Image.new("RGB", (Wd, Ht), RGB[bg])
    d = ImageDraw.Draw(im)
    for i, (key, label, fn) in enumerate(ILLS):
        cx = pad + (i % cols) * cell + cell / 2
        cy = pad + (i // cols) * cell + cell / 2
        render(im, fn(), (cx, cy - 8), cell * 0.56, "teal", canvas=IS)
        f = ImageFont.truetype(SANS_CN, 15)
        spaced(d, label, f, cy + cell * 0.30, "teal", 3, cx)
    p = os.path.join(ROOT, "06_系列插图", "_系列插图_全览.png")
    im.save(p)
    print("png:", os.path.basename(p))


# ---------------- 主程序 ----------------
if __name__ == "__main__":
    ICON_DIR = os.path.join(ROOT, "01_图标")
    for nm, pr in (("drop", MARK), ("drop_simple", MARK_SIMPLE), ("box", MARK_BOX)):
        for c in ("teal", "amber", "white", "ink"):
            write_svg(os.path.join(ICON_DIR, f"mark_{nm}_{c}.svg"), svg_for(pr, c), (S, S))
        write_svg(os.path.join(ICON_DIR, f"mark_{nm}_on_teal.svg"), svg_for(pr, "paper", bg="teal"), (S, S))
        write_svg(os.path.join(ICON_DIR, f"mark_{nm}_on_amber.svg"), svg_for(pr, "paper", bg="amber"), (S, S))

    for c, fn in (("teal", "wordmark_h.svg"), ("white", "wordmark_h_white.svg"), ("ink", "wordmark_h_ink.svg")):
        b, vb = wordmark_h(c)
        write_svg(os.path.join(ROOT, "02_字标", fn), b, vb)

    for c, fn in (("teal", "lockup_h.svg"), ("white", "lockup_h_white.svg")):
        b, vb = lockup_h(c)
        write_svg(os.path.join(ROOT, "03_组合", fn), b, vb)
    for c, fn in (("teal", "lockup_v.svg"), ("white", "lockup_v_white.svg")):
        b, vb = lockup_v(c)
        write_svg(os.path.join(ROOT, "03_组合", fn), b, vb)

    avatar(1200, "teal", "paper", "黛青底")
    avatar(800, "teal", "paper", "黛青底")
    avatar(1200, "amber", "paper", "琥珀底")
    cover_sq(3000, "teal", "paper", "方形", series=TAGLINE, series_color="amber")
    cover_sq(3000, "amber", "paper", "特别期", series=TAGLINE, series_color="paper")
    cover_wide(900, 383, "teal", "paper", "公众号", series=TAGLINE, series_color="amber")
    cover_wide(900, 383, "teal", "paper", "公众号_热点周报", series="热点周报", series_color="amber")
    cover_wide(1920, 1080, "teal", "paper", "16x9", series=TAGLINE, series_color="amber")

    ILL_DIR = os.path.join(ROOT, "06_系列插图")
    for key, label, fn in ILLS:
        for c in ("teal", "amber", "white", "ink"):
            write_svg(os.path.join(ILL_DIR, f"ill_{key}_{c}.svg"), svg_for(fn(), c, size=IS), (IS, IS))
        write_svg(os.path.join(ILL_DIR, f"ill_{key}_on_teal.svg"), svg_for(fn(), "paper", bg="teal", size=IS), (IS, IS))
    contact_sheet()

    print("\n完成 ->", ROOT)
