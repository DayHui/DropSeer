"""生成品牌视觉提案总览页（深空暗色主题，自包含：SVG 内联 + PNG base64）"""
import os, base64

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

PAL = [("宇宙黑 void", "#0A0F14", "主背景 —— 黑盒 / 深空", "#D2DBE4"),
       ("水银银 silver", "#D2DBE4", "水滴主体 / 反白字", "#0A0F14"),
       ("镜面白 white", "#FFFFFF", "高光（全反射镜面）", "#0A0F14"),
       ("琥珀 amber", "#B05A1F", "风险信号（唯一暖色）", "#FFFFFF"),
       ("墨 ink", "#0E1418", "单色印刷 / 亮底反白", "#D2DBE4")]


def inline_svg(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return f'<em>缺: {rel}</em>'
    with open(p, encoding="utf-8") as f:
        s = f.read()
    return s.replace('<svg ', '<svg style="max-width:100%;height:auto;" ', 1)


def img64(rel, cap):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return f'<figure><em>缺: {rel}</em></figure>'
    b = base64.b64encode(open(p, "rb").read()).decode()
    return f'<figure><img src="data:image/png;base64,{b}" style="width:100%;height:auto;display:block;border-radius:4px"><figcaption>{cap}</figcaption></figure>'


def card(rel, label, bg="#0A0F14"):
    return f'<div class="cell" style="background:{bg}"><div class="art">{inline_svg(rel)}</div><div class="lbl">{label}</div></div>'


H = []
H.append('''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>水滴观测站 · 品牌视觉 v2</title>
<style>
:root{--void:#0A0F14;--card:#111821;--card2:#141D28;--silver:#D2DBE4;--dim:#7E8A94;
 --faint:#56636E;--amber:#B05A1F;--line:#223140;--white:#FFFFFF}
*{box-sizing:border-box}
body{margin:0;background:var(--void);color:var(--silver);
 font-family:"Noto Sans SC","Microsoft YaHei",-apple-system,sans-serif;
 -webkit-font-smoothing:antialiased;line-height:1.75}
.wrap{max-width:1180px;margin:0 auto;padding:72px 32px 110px}
.sub{color:var(--dim);letter-spacing:.3em;font-size:12px;margin-bottom:8px}
h1{font-size:44px;letter-spacing:.12em;margin:0 0 18px;font-weight:900;color:var(--white)}
.quote{color:var(--silver);background:var(--card);border-left:2px solid var(--amber);
 padding:18px 22px;border-radius:0 8px 8px 0;font-size:14px;line-height:1.9;margin:0 0 8px}
.quote .who{color:var(--dim);font-size:12px;letter-spacing:.12em}
.lead{color:var(--silver);max-width:780px;margin:16px 0 4px;font-size:15px;opacity:.9}
h2{font-size:15px;letter-spacing:.3em;color:var(--amber);font-weight:900;
 margin:76px 0 8px;padding-top:24px;border-top:1px solid var(--line)}
h2:first-of-type{margin-top:40px}
.note{color:var(--dim);font-size:13px;margin:0 0 26px}
.grid{display:grid;gap:18px}
.g4{grid-template-columns:repeat(4,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
.cell{border:1px solid var(--line);border-radius:8px;padding:26px 18px 16px;
 background:var(--card);display:flex;flex-direction:column;align-items:center;justify-content:center}
.cell .art{width:100%;max-width:180px}
.cell .lbl{font-size:12px;color:var(--dim);letter-spacing:.08em;margin-top:16px;text-align:center}
figure{margin:0;border:1px solid var(--line);border-radius:8px;padding:14px;background:var(--card)}
figcaption{font-size:12px;color:var(--dim);letter-spacing:.08em;margin-top:12px;text-align:center}
.sw{border-radius:8px;overflow:hidden;border:1px solid var(--line)}
.sw .chip{height:90px;display:flex;align-items:flex-end;padding:10px 13px;font-size:12px;letter-spacing:.12em}
.sw .meta{background:var(--card);padding:12px 14px}
.sw .meta b{display:block;font-size:13px;margin-bottom:4px;color:var(--silver)}
.sw .meta span{font-size:12px;color:var(--dim)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:22px}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card);
 border:1px solid var(--line);border-radius:8px;overflow:hidden}
th,td{border-bottom:1px solid var(--line);padding:12px 15px;text-align:left;vertical-align:top}
th{background:var(--card2);font-size:12px;letter-spacing:.16em;color:var(--amber)}
tr:last-child td{border-bottom:none}
footer{margin-top:90px;padding-top:26px;border-top:1px solid var(--line);color:var(--faint);font-size:12px;letter-spacing:.1em}
</style></head><body><div class="wrap">''')

H.append('<div class="sub">DROPSEER &nbsp;·&nbsp; BRAND IDENTITY v2</div>')
H.append('<h1>水滴观测站 · 品牌视觉</h1>')
H.append('<blockquote class="quote">“它是那么美，就像一滴圣母的眼泪……它的表面完全光滑。放大一千万倍，这时已经可以看到大分子了，但水滴仍然完全光滑。”<br>'
         '<span class="who">——《三体II·黑暗森林》 末日之战</span></blockquote>')
H.append('<p class="lead">主符号「<b>水银悬滴</b>」。极致的美（一滴完美水银 / 全反射镜面）+ 极致的简（绝对光滑，所以符号上<b>没有任何多余零件</b>）。宇宙黑背景里，一滴银，一道光。</p>')

# 一、主符号
H.append('<h2>一 · 主符号 「水银悬滴」</h2>')
H.append('<p class="note">实心水银滴 + 一道镜面高光。尖端朝上（水滴将落未落，观测从黑盒之外开始）；高光 = 全反射镜面映出的光纹；无颈、无波纹、无杂线——放大一千万倍依然光滑。</p>')
H.append('<div class="grid g4">')
H.append(card("01_图标/mark_drop.svg", "全版（银滴 + 高光）"))
H.append(card("01_图标/mark_drop_simple.svg", "简版（无高光，小尺寸）"))
H.append(card("01_图标/mark_drop_ink.svg", "墨版（亮底 / 单色）", "#F7F9FA"))
H.append(card("01_图标/mark_drop_on_void.svg", "带宇宙黑底"))
H.append('</div>')

# 二、辅符号
H.append('<h2>二 · 辅符号 「盒 · 见」</h2>')
H.append('<p class="note">黑盒顶边开一道缝，内部的点由此显形——用于黑盒 / 失效 / 风险主题，不抢主标位置</p>')
H.append('<div class="grid g4">')
H.append(card("01_图标/mark_box_silver.svg", "水银银"))
H.append(card("01_图标/mark_box_amber.svg", "琥珀（风险）"))
H.append(card("01_图标/mark_box_ink.svg", "墨", "#F7F9FA"))
H.append(card("01_图标/mark_box_on_void.svg", "带宇宙黑底"))
H.append('</div>')

# 三、配色
H.append('<h2>三 · 色彩系统</h2>')
H.append('<p class="note">一个画面只有一个主色；银滴 + 高光是最核心的形态；禁止渐变 / 发光 / 立体感；背景为宇宙黑（黑盒），非特殊说明不用亮底</p>')
H.append('<div class="grid g4">')
for nm, hx, use, fg in PAL:
    H.append(f'<div class="sw"><div class="chip" style="background:{hx};color:{fg}">{hx}</div>'
             f'<div class="meta"><b>{nm}</b><span>{use}</span></div></div>')
H.append('</div>')

# 四、字标与组合
H.append('<h2>四 · 字标与组合</h2>')
H.append('<p class="note">中文思源黑体 Heavy，字距 +10~12%；英文 Arial，字距 +40%；分隔线为刻度尺式。反白（水银银）用于深底。</p>')
H.append('<div class="grid g2">')
H.append(f'<figure>{inline_svg("02_字标/wordmark_h.svg")}<figcaption>横排字标 · 水银银</figcaption></figure>')
H.append(f'<figure>{inline_svg("02_字标/wordmark_h_ink.svg")}<figcaption>横排字标 · 墨（亮底）</figcaption></figure>')
H.append('</div>')
H.append('<div class="grid g2" style="margin-top:18px">')
H.append(f'<figure>{inline_svg("03_组合/lockup_h.svg")}<figcaption>横排组合（符号左 + 字标右）</figcaption></figure>')
H.append(f'<figure>{inline_svg("03_组合/lockup_v.svg")}<figcaption>竖排组合（符号上 + 字标下）</figcaption></figure>')
H.append('</div>')

# 五、成品
H.append('<h2>五 · 成品（可直接上传）</h2>')
H.append('<div class="split">')
H.append(img64("04_成品/头像_宇宙黑底_1200.png", "头像 · 宇宙黑底 1200×1200（公众号 / 全平台）"))
H.append(img64("04_成品/头像_水银底_1200.png", "头像 · 水银底（特别期 / 反转）"))
H.append('</div>')
H.append('<div style="margin-top:20px">')
H.append(img64("04_成品/封面_公众号_900x383.png", "公众号封面 900×383（2.35:1）"))
H.append('</div>')
H.append('<div class="split" style="margin-top:20px">')
H.append(img64("04_成品/封面_公众号_热点周报_900x383.png", "公众号封面 · 热点周报（系列名可变位）"))
H.append(img64("04_成品/封面_方形_3000.png", "方形封面 3000×3000"))
H.append('</div>')

# 六、系列插图
H.append('<h2>六 · 系列插图（六张一套）</h2>')
H.append('<p class="note">一条观测动线：试探 → 回波 → 度量 → 链路 → 失效 → 复盘。几何化、单色（水银银用于深底）。</p>')
H.append(f'<figure style="padding:18px">{img64("06_系列插图/_系列插图_全览.png", "六张一览（3×2，宇宙黑底反白）")}</figure>')
H.append('<div class="grid g3" style="margin-top:20px">')
for k, lb in (("probe", "探 · 试探（技术实战 / 实测）"), ("wave", "波 · 回波（热点周报 / 动态）"),
              ("gauge", "度 · 度量（评测 / 横评）"), ("trace", "迹 · 链路（Agent / MCP 链路）"),
              ("fault", "罅 · 失效（失效分析 / 风险）"), ("log", "录 · 复盘（复盘 / 总结 / 案例）")):
    H.append(card(f"06_系列插图/ill_{k}_silver.svg", lb))
H.append('</div>')

# 七、与茶馆边界
H.append('<h2>七 · 与《时空茶馆》的边界（防止品牌混同）</h2>')
H.append('''<table>
<tr><th>维度</th><th>水滴观测站</th><th>时空茶馆（对照）</th></tr>
<tr><td>主符号</td><td>水银悬滴（实心银滴 + 镜面高光）</td><td>晷 · 影（日晷圆盘 + 指针）</td></tr>
<tr><td>体系</td><td>宇宙黑底（黑盒 / 深空）+ 水银反白</td><td>亮底宣纸 + 藏青单色</td></tr>
<tr><td>主色</td><td>宇宙黑 #0A0F14 + 水银 #D2DBE4</td><td>藏青 #14304F + 朱砂 #A8362A</td></tr>
<tr><td>气质</td><td>冷静工程师 · 黑盒观测 · 三体美学</td><td>古意茶馆 · 时间容器</td></tr>
</table>''')

H.append('<footer>水滴观测站 · 品牌视觉 v2 &nbsp;|&nbsp; 由 _生成脚本/build_dropseer_assets.py 精确制图 &nbsp;|&nbsp; 意象源自《三体II》水滴</footer>')
H.append('</div></body></html>')

out = os.path.join(ROOT, "提案_品牌视觉全览.html")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(H))
print("html:", out)
