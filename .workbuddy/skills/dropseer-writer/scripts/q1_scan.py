#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Q1 语言质检扫描器（dropseer-writer skill 配套）
================================================
用法：
    python q1_scan.py <稿件.md>

扫描前会**排除**：标题行（#）、引用块（> ，即 [注入位] 编辑标记）、表格（|）、
代码块（``` 之间）、以及文末「本版改了什么」等附录（以 `## 本版` 开头的章节）。
即：只扫正文。

输出：禁用词命中（带行号）、标点统计（冒号/破折号/引号/加粗）、
独立成段的短句数量（节奏指标）、正文字数。
"""

import re
import sys

BANNED = [
    "说白了", "意味着什么", "这意味着", "本质上", "换句话说", "不可否认",
    "综上所述", "总的来说", "值得注意的是", "不难发现", "让我们来看看",
    "接下来让我们", "在这个", "随着技术", "随着人工智能", "深度解析",
    "全面解读", "重磅", "赋能", "抓手", "闭环", "震惊", "杀疯",
    "AI工具", "某个模型", "相关技术", "某大厂",
]

LIMITS = {
    "破折号": (5, "全篇不超过 5 处"),
    "加粗": (3, "金句加粗 2–3 处"),
    "冒号": (None, "一段里不超过 1 处为宜"),
    "半角引号": (0, "中文正文一律用 “ ” 或「」，不用半角 \""),
    "情绪标点(。。。)": (0, "不学上游的情绪标点口吻"),
    "情绪标点(？？？)": (0, "不学上游的情绪标点口吻"),
}


def body_lines(text):
    """返回 [(行号, 正文行)]，已排除标题/引用块/表格/代码块/附录。"""
    out, in_code, in_appendix = [], False, False
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if s.startswith("## 本版"):
            in_appendix = True
        if in_appendix:
            continue
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("|"):
            continue
        out.append((i, line))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = body_lines(text)
    body = "\n".join(l for _, l in lines)

    print("=" * 66)
    print(f"Q1 语言质检 · {path}")
    print("=" * 66)

    print("\n[1] 禁用词命中")
    hit = 0
    for w in BANNED:
        for no, line in lines:
            if w in line:
                hit += 1
                print(f"    L{no:4d}  「{w}」  {line.strip()[:52]}")
    print("    零命中 ✅" if not hit else f"    共 {hit} 处，逐处改写")

    print("\n[2] 标点统计（仅正文）")
    counts = {
        "冒号": body.count("："),
        "破折号": body.count("——"),
        "加粗": len(re.findall(r"\*\*", body)) // 2,
        "中文引号“”": body.count("\u201c") + body.count("\u201d"),
        "中文引号「」": body.count("「"),
        "半角引号": body.count('"'),
        "情绪标点(。。。)": body.count("。。。"),
        "情绪标点(？？？)": body.count("？？？"),
    }
    for k, v in counts.items():
        lim = LIMITS.get(k)
        flag = ""
        if lim and lim[0] is not None:
            flag = "  ← 超限！" if v > lim[0] else "  ✅"
            flag += f"（上限 {lim[0]}，{lim[1]}）"
        print(f"    {k:14s} {v:3d}{flag}")

    print("\n[3] 节奏指标")
    paras = [l.strip() for l in body.splitlines() if l.strip()]
    shorts = [p for p in paras if 4 <= len(p) <= 30]
    print(f"    独立成段的短句：{len(shorts)} 处（要求 ≥3）"
          + ("  ✅" if len(shorts) >= 3 else "  ← 不足，节奏可能呆板"))
    for s in shorts[:8]:
        print(f"      · {s[:40]}")

    chars = len(re.sub(r"\s", "", body))
    print(f"\n[4] 正文字数：约 {chars} 字（长文建议 3000–6000，框架篇可短）")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
