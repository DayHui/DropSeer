"""生成品牌视觉提案总览页（自包含 HTML：SVG 内联 + PNG base64 嵌入）"""
import os, base64, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

PAL = [("黛青 teal", "#16404D", "主色 · 头像底 / 封面底 / 标题", "#FFFFFF"),
       ("琥珀 amber", "#B05A1F", "副色 · 风险信号 / 重点强调 / 特别期", "#FFFFFF"),
       ("雾白 paper", "#F4F6F4", "底色与反白字（不是白，是雾）", "#15191B"),
       ("墨 ink", "#15191B", "单色印刷 / 长文正文", "#FFFFFF"),
       ("水青 aqua", "#3E7C8F", "点缀 · 限量使用", "#FFFFFF")]


def inline_svg(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return f'<em>缺: {rel}</em>'
    with open(p, encoding="utf-8") as f:
        s = f.read()
    s = s.replace('<svg ', '<svg style="max-width:100%;height:auto;" ', 1)
    return s


def img64(rel, cap, style="max-width:100%;height:auto;"):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return f'<figure><em>缺: {rel}</em></figure>'
    b = base64.b64encode(open(p, "rb").read()).decode()
    return f'<figure><img src="data:image/png;base64,{b}" style="{style}"><figcaption>{cap}</figcaption></figure>'


def icon_card(rel, label, bg="#FFFFFF"):
    return f'<div class="cell" style="background:{bg}"><div class="art">{inline_svg(rel)}</div><div class="lbl">{label}</div></div>'


H = []
H.append('''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>水滴观测站 · 品牌视觉 v1</title>
<style>
:root{--teal:#16404D;--amber:#B05A1F;--paper:#F4F6F4;--ink:#15191B;--aqua:#3E7C8F;--line:#dfe4e3}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:"Noto Sans SC","Microsoft YaHei",-apple-system,sans-serif;
 -webkit-font-smoothing:antialiased;line-height:1.7}
.wrap{max-width:1180px;margin:0 auto;padding:64px 32px 96px}
h1{font-size:42px;letter-spacing:.14em;margin:0 0 8px;font-weight:900}
.sub{color:#5c6b70;letter-spacing:.22em;font-size:13px;margin-bottom:6px}
.lead{color:#42535a;max-width:760px;margin:20px 0 8px;font-size:15px}
h2{font-size:15px;letter-spacing:.28em;color:var(--teal);font-weight:900;
 margin:72px 0 6px;padding-top:22px;border-top:2px solid var(--teal)}
h2:first-of-type{margin-top:44px}
.note{color:#6b7a80;font-size:13px;margin:0 0 24px}
.grid{display:grid;gap:16px}
.g4{grid-template-columns:repeat(4,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
.cell{border:1px solid var(--line);border-radius:6px;padding:22px 16px 14px;
 background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center}
.cell .art{width:100%;max-width:190px}
.cell .lbl{font-size:12px;color:#6b7a80;letter-spacing:.1em;margin-top:14px;text-align:center}
figure{margin:0;border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff}
figure img{display:block;border-radius:4px;width:100%}
figcaption{font-size:12px;color:#6b7a80;letter-spacing:.08em;margin-top:10px;text-align:center}
.sw{border-radius:6px;overflow:hidden;border:1px solid var(--line)}
.sw .chip{height:96px;display:flex;align-items:flex-end;padding:10px 12px;font-size:12px;letter-spacing:.1em}
.sw .meta{background:#fff;padding:12px 14px}
.sw .meta b{display:block;font-size:13px;margin-bottom:4px}
.sw .meta span{font-size:12px;color:#6b7a80}
.row{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:center;
 border:1px solid var(--line);border-radius:8px;padding:20px;background:#fff}
.row.on-dark{background:var(--teal);border-color:var(--teal)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.tag{display:inline-block;font-size:12px;letter-spacing:.16em;color:var(--amber);
 border:1px solid var(--amber);border-radius:99px;padding:3px 12px;margin-bottom:10px}
table{border-collapse:collapse;width:100%;font-size:14px;background:#fff;
 border:1px solid var(--line);border-radius:8px;overflow:hidden}
th,td{border-bottom:1px solid var(--line);padding:11px 14px;text-align:left;vertical-align:top}
th{background:#eef1f0;font-size:12px;letter-spacing:.16em;color:var(--teal)}
tr:last-child td{border-bottom:none}
.bad{color:#a33} .good{color:var(--teal)}
footer{margin-top:80px;padding-top:24px;border-top:1px solid var(--line);
 color:#7b8a90;font-size:12px;letter-spacing:.1em}
</style></head><body><div class="wrap">''')

H.append(f'<div class="sub">DROPSEER &nbsp;·&nbsp; BRAND IDENTITY v1</div>')
H.append('<h1>水滴观测站 · 品牌视觉</h1>')
H.append('<p class="lead">主符号「<b>滴 · 测</b>」，辅符号「<b>盒 · 见</b>」。体系：亮底 + 单色 + 文字主导，'
         '脚本精确制图，等宽笔画。核心意象取自卷首语——<b>光滑的外壳，未必代表无懈可击</b>。</p>')

# 一、主符号
H.append('<h2>一 · 主符号 「滴 · 测」</h2>')
H.append('<p class="note">垂线自画面外探入（观测从黑盒之外开始）／ 空心水滴（光滑外壳之下）／ 中心点（风险就停在这一点上）／ 波纹弧（试探与回波）</p>')
H.append('<div class="grid g4">')
H.append(icon_card("01_图标/mark_drop_teal.svg", "全版 · 黛青"))
H.append(icon_card("01_图标/mark_drop_amber.svg", "全版 · 琥珀"))
H.append(icon_card("01_图标/mark_drop_ink.svg", "全版 · 墨"))
H.append(icon_card("01_图标/mark_drop_on_teal.svg", "全版 · 反白", "#16404D"))
H.append(icon_card("01_图标/mark_drop_simple_teal.svg", "简版（24–48px）· 黛青"))
H.append(icon_card("01_图标/mark_drop_simple_amber.svg", "简版 · 琥珀"))
H.append(icon_card("01_图标/mark_drop_simple_ink.svg", "简版 · 墨"))
H.append(icon_card("01_图标/mark_drop_simple_on_teal.svg", "简版 · 反白", "#16404D"))
H.append('</div>')

# 二、辅符号
H.append('<h2>二 · 辅符号 「盒 · 见」</h2>')
H.append('<p class="note">黑盒顶边开一道缝，里面的点由此显形——用于「黑盒 / 失效 / 风险」主题，不抢主标位置</p>')
H.append('<div class="grid g4">')
H.append(icon_card("01_图标/mark_box_teal.svg", "黛青"))
H.append(icon_card("01_图标/mark_box_amber.svg", "琥珀"))
H.append(icon_card("01_图标/mark_box_ink.svg", "墨"))
H.append(icon_card("01_图标/mark_box_on_teal.svg", "反白", "#16404D"))
H.append('</div>')

# 三、色彩
H.append('<h2>三 · 色彩系统</h2>')
H.append('<p class="note">一个画面只有一个主色；色块 + 反白字是最稳的形态；禁止渐变做主视觉；背景永远亮底</p>')
H.append('<div class="grid g4">')
for nm, hx, use, fg in PAL:
    H.append(f'<div class="sw"><div class="chip" style="background:{hx};color:{fg}">{hx}</div>'
             f'<div class="meta"><b>{nm}</b><span>{use}</span></div></div>')
H.append('</div>')

# 四、字标与组合
H.append('<h2>四 · 字标与组合</h2>')
H.append('<p class="note">中文思源黑体 Heavy（与《时空茶馆》的宋体刻意区分），字距 +10~12%；英文 Arial，字距 +40%；分隔线为「刻度尺」式，取代中心点</p>')
H.append('<div class="grid g2">')
H.append(f'<figure>{inline_svg("02_字标/wordmark_h.svg")}<figcaption>横排字标 · 黛青</figcaption></figure>')
H.append(f'<figure>{inline_svg("02_字标/wordmark_h_white.svg")}<figcaption>横排字标 · 反白</figcaption></figure>')
H.append('</div>')
H.append('<div class="grid g2" style="margin-top:16px">')
H.append(f'<figure>{inline_svg("03_组合/lockup_h.svg")}<figcaption>横排组合（符号左 + 字标右）</figcaption></figure>')
H.append(f'<figure>{inline_svg("03_组合/lockup_v.svg")}<figcaption>竖排组合（符号上 + 字标下）</figcaption></figure>')
H.append('</div>')

# 五、成品
H.append('<h2>五 · 成品（可直接上传）</h2>')
H.append('<div class="split">')
H.append(img64("04_成品/头像_黛青底_1200.png", "头像 · 黛青底 1200×1200（公众号 / 全平台）"))
H.append(img64("04_成品/头像_琥珀底_1200.png", "头像 · 琥珀底 1200×1200"))
H.append('</div>')
H.append('<div style="margin-top:18px">')
H.append(img64("04_成品/封面_公众号_900x383.png", "公众号封面 900×383（2.35:1 标准比例）"))
H.append('</div>')
H.append('<div class="split" style="margin-top:18px">')
H.append(img64("04_成品/封面_公众号_热点周报_900x383.png", "公众号封面 · 热点周报（系列名可变位）"))
H.append(img64("04_成品/封面_方形_3000.png", "方形封面 3000×3000"))
H.append('</div>')

# 六、系列插图
H.append('<h2>六 · 系列插图（六张一套）</h2>')
H.append('<p class="note">一条观测动线：<b>试探 → 回波 → 度量 → 链路 → 失效 → 复盘</b>。等宽笔画、几何化、单色，一次画好长期复用。</p>')
H.append(f'<figure style="padding:18px">{img64("06_系列插图/_系列插图_全览.png", "六张一览（3×2）")}</figure>')
H.append('<div class="grid g3" style="margin-top:18px">')
for k, lb in (("probe", "探 · 试探（技术实战 / 实测）"), ("wave", "波 · 回波（热点周报 / 动态）"),
              ("gauge", "度 · 度量（评测 / 横评）"), ("trace", "迹 · 链路（Agent / MCP 链路）"),
              ("fault", "罅 · 失效（失效分析 / 风险）"), ("log", "录 · 复盘（复盘 / 总结 / 案例）")):
    H.append(icon_card(f"06_系列插图/ill_{k}_teal.svg", lb))
H.append('</div>')
H.append('<div class="grid g3" style="margin-top:16px">')
for k in ("probe", "wave", "gauge"):
    H.append(icon_card(f"06_系列插图/ill_{k}_on_teal.svg", f"反白应用 · {k}", "#16404D"))
H.append('</div>')

# 七、与时空茶馆的边界
H.append('<h2>七 · 与《时空茶馆》的边界（刻意区分，防止品牌混同）</h2>')
H.append('''<table>
<tr><th>维度</th><th>水滴观测站</th><th>时空茶馆（对照）</th></tr>
<tr><td>主符号</td><td>滴 · 测（水滴 + 垂线 + 波纹）</td><td>晷 · 影（日晷圆盘 + 指针）</td></tr>
<tr><td>色彩</td><td>黛青 #16404D + 琥珀 #B05A1F</td><td>藏青 #14304F + 朱砂 #A8362A</td></tr>
<tr><td>中文字体</td><td>思源黑体 Heavy（现代仪器感）</td><td>思源宋体 Heavy（古典文气）</td></tr>
<tr><td>气质</td><td>冷静工程师 · 观测仪器</td><td>古意茶馆 · 时间容器</td></tr>
<tr><td>分隔线</td><td>线 + 三道刻度（量尺）</td><td>线 + 中心点</td></tr>
</table>''')

H.append('<footer>水滴观测站 · 品牌视觉 v1 &nbsp;|&nbsp; 由 _生成脚本/build_dropseer_assets.py 精确制图 &nbsp;|&nbsp; 改规格只需修改脚本顶部常量后重跑</footer>')
H.append('</div></body></html>')

out = os.path.join(ROOT, "提案_品牌视觉全览.html")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(H))
print("html:", out)
