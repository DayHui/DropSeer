"""文章插图全览页（深空暗色主题，PNG base64 内嵌）"""
import os, base64

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IL = os.path.join(ROOT, "07_文章插图")

ITEMS = [
    ("文章插图_黑盒", "黑盒 · 光滑外壳下的风险", "开篇立意 / 四大支柱总述 / 失效分析。一道琥珀裂缝，呼应「光滑的外壳未必无懈可击」。"),
    ("文章插图_水滴入黑盒", "水滴入黑盒", "卷首语、账号门面、公众号头图。主符号的场景化：水滴将落未落，落入黑盒。"),
    ("文章插图_Agent链路", "Agent / MCP 链路", "技术实战 · 链路实测。五个水银节点，中间一个琥珀失效节点 + 链路断裂。"),
    ("文章插图_评测仪表", "评测仪表", "评测工具横评 / 质量度量。指针指向琥珀危险区。"),
    ("文章插图_四类失效", "四类失效", "洞察思考 · 四层失效分类学（账号核心锚点图）：幻觉 / 工具调用 / 规划 / 退化。"),
    ("文章插图_观测", "观测", "账号人设「冷静的观测者」/ 热点周报。雷达对准一滴水银，探测点锁定。"),
    ("文章插图_信号波形", "信号波形", "E2E 测试实战 / 通信测试。一条信号中段断裂，琥珀标记异常。"),
    ("文章插图_编队", "超级工程师 + Agent 编队", "团队转型。一颗大水银滴带一群小滴。"),
    ("文章插图_分隔符", "章节分隔符", "文章内章节切换的视觉停顿。"),
]


def b64(p):
    return "data:image/png;base64," + base64.b64encode(open(os.path.join(IL, p), "rb").read()).decode()


H = ['''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>水滴观测站 · 文章插图</title>
<style>
:root{--void:#0A0F14;--card:#111821;--silver:#D2DBE4;--dim:#7E8A94;--amber:#B05A1F;--line:#223140;--white:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--void);color:var(--silver);font-family:"Noto Sans SC","Microsoft YaHei",sans-serif;line-height:1.7}
.wrap{max-width:1080px;margin:0 auto;padding:64px 32px 100px}
.sub{color:var(--dim);letter-spacing:.3em;font-size:12px;margin-bottom:8px}
h1{font-size:36px;letter-spacing:.1em;margin:0 0 14px;color:var(--white)}
.lead{color:var(--dim);font-size:14px;max-width:720px}
.sec{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:18px;margin-top:34px}
.sec img{width:100%;height:auto;display:block;border-radius:6px}
.sec h2{font-size:16px;margin:14px 0 4px;color:var(--amber);letter-spacing:.06em}
.sec p{font-size:13px;color:var(--dim);margin:0}
</style></head><body><div class="wrap">
<div class="sub">DROPSEER · ARTICLE ILLUSTRATIONS</div>
<h1>水滴观测站 · 文章插图</h1>
<p class="lead">基于「水银悬滴」风格：宇宙黑底 + 实心水银 + 镜面高光 + 琥珀仅作风险标记。9 张，覆盖公众号文章高频场景。源脚本 <code>_生成脚本/build_articles.py</code>。</p>''']

for name, title, desc in ITEMS:
    H.append(f'<div class="sec"><img src="{b64(name + ".png")}"><h2>{title}</h2><p>{desc}</p></div>')

H.append('</div></body></html>')

out = os.path.join(ROOT, "文章插图_全览.html")
open(out, "w", encoding="utf-8").write("\n".join(H))
print("html:", out)
