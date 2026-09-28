#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""水滴观测站 · 发布版装配器（assemble_publish.py）

把「初稿」装配成「可推送公众号草稿箱的发布版」。
之所以做成脚本：装配动作里有同一个锚点重复插图的坑，已手工犯过两次，
从此不再手写一次性脚本。

用法
----
python assemble_publish.py \
    --src  03_稿件/001-Agent的四种死法/001-初稿-v0.7.md \
    --plan 03_稿件/001-Agent的四种死法/001-配图挂载.json \
    --out  03_稿件/001-Agent的四种死法/001-发布版.md \
    --note "（发布版预览 · 未定稿）……"

配图挂载表（JSON，可省略）
------------------------
{
  "title": "Agent 的四层失效",
  "cover": "../../04_素材与配图/品牌视觉/最终版/04_成品/封面_公众号_高清_1800x767.png",
  "images": [
    {"position": "after",  "anchor": "锚点原文（必须唯一）", "path": "相对本 md 的图片路径", "alt": "一句话说明"},
    {"position": "before", "anchor": "……", "path": "……", "alt": "……"}
  ]
}

装配动作（顺序固定）
------------------
1. 去掉正文首行大标题（公众号标题在后台单独填，正文再来一遍是硬伤）
2. 去掉元信息引用块与 [注入位] 引用块（构造场景声明保留）
3. 截掉「## 本版改了什么」及其后的内部附录与出处表
4. 二级标题统一带序号（中文数字 + 青绿着色）—— 排版规范硬要求
5. 按配图挂载表插图（显式 before/after；锚点缺失或不唯一即报错退出）
6. 统一中文引号、压缩多余空行
7. 写入 frontmatter（title + cover）

自检输出：章节数、标题去重、插图数、正文字数、残留风险项。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

ACCENT = "#1DA69A"
CN_DIGITS = "一二三四五六七八九十"

# 元信息/注入位引用块的前缀（这些不进发布版）
META_PREFIXES = (
    "> 【注入位",
    "> 水滴观测站 · 正刊",
    "> 关键词：",
    "> **本稿含",
    "> 相对 v0.2",
    "> （发布版预览",
    "> （精简版预览",
    "> （极简版预览",
)

# 附录起点（其后全部截掉）
APPENDIX_MARK = re.compile(r"^##\s*本版改了什么")
NUM_RE = re.compile(r"^(?:[一二三四五六七八九十]+|\d{1,2})\s*[、.．]\s*")


def cn_num(n: int) -> str:
    if n <= 10:
        return CN_DIGITS[n - 1]
    if n < 20:
        return "十" + CN_DIGITS[n - 11]
    tens, ones = divmod(n, 10)
    return CN_DIGITS[tens - 1] + "十" + (CN_DIGITS[ones - 1] if ones else "")


def number_headings(text: str) -> tuple[str, list[str]]:
    """给所有 `## ` 标题加序号（先剥旧序号，再重编，幂等）。"""
    out, titles, n = [], [], 0
    for line in text.splitlines():
        m = re.match(r"^(##\s+)(\S.*)$", line)
        if m:
            n += 1
            body = NUM_RE.sub("", m.group(2)).strip()
            titles.append(body)
            line = f'{m.group(1)}<span style="color:{ACCENT}">{cn_num(n)}</span>、{body}'
        out.append(line)
    return "\n".join(out), titles


def fix_quotes(text: str) -> str:
    """半角双引号 -> 中文弯引号（跳过代码围栏与行内代码）。"""
    out, in_fence, open_q = [], False, True
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or '"' not in line:
            out.append(line)
            continue
        parts = line.split("`")
        for i, seg in enumerate(parts):
            if i % 2 == 1:  # 行内代码，保持原样
                continue
            buf = []
            for ch in seg:
                if ch == '"':
                    buf.append("“" if open_q else "”")
                    open_q = not open_q
                else:
                    buf.append(ch)
            parts[i] = "".join(buf)
        out.append("`".join(parts))
    return "\n".join(out)


def insert_images(text: str, images: list[dict]) -> tuple[str, int]:
    for i, spec in enumerate(images, 1):
        anchor, pos = spec["anchor"], spec.get("position", "after")
        cnt = text.count(anchor)
        if cnt == 0:
            raise SystemExit(f"[FAIL] 第 {i} 张图锚点未找到：{anchor[:40]}…")
        if cnt > 1:
            raise SystemExit(f"[FAIL] 第 {i} 张图锚点不唯一（命中 {cnt} 次）：{anchor[:40]}…")
        block = f'![{spec.get("alt", "")}]({spec["path"]})'
        text = text.replace(
            anchor, f"{anchor}\n\n{block}" if pos == "after" else f"{block}\n\n{anchor}", 1
        )
    return text, len(images)


def strip_scaffold(lines: list[str]) -> list[str]:
    """去大标题 / 元信息与注入位引用块 / 附录。"""
    out, seen_h1 = [], False
    for line in lines:
        s = line.strip()
        if APPENDIX_MARK.match(s):
            break
        if s.startswith("# ") and not seen_h1:  # 只去掉第一个大标题
            seen_h1 = True
            continue
        if s.startswith(META_PREFIXES):
            continue
        out.append(line)
    return out


def body_word_count(text: str) -> int:
    t = re.sub(r"^>.*$", "", text, flags=re.M)
    t = re.sub(r"^!\[.*$", "", t, flags=re.M)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[#*|>\-\s]", "", t)
    return len(t)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="初稿 md")
    ap.add_argument("--plan", default="", help="配图挂载表 JSON（可省略）")
    ap.add_argument("--out", required=True, help="输出发布版 md")
    ap.add_argument("--title", default="", help="不填则取自 plan")
    ap.add_argument("--cover", default="", help="不填则取自 plan")
    ap.add_argument("--note", default="", help="文首说明行（可省略）")
    args = ap.parse_args()

    src = open(args.src, encoding="utf-8").read()
    plan = {}
    if args.plan and os.path.exists(args.plan):
        plan = json.load(open(args.plan, encoding="utf-8"))

    title = args.title or plan.get("title")
    cover = args.cover or plan.get("cover")
    if not title or not cover:
        print("[FAIL] 缺 title 或 cover（frontmatter 缺一，wenyan 直接报错）")
        return 1

    text = "\n".join(strip_scaffold(src.splitlines()))
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # 顺序要紧：引号修正必须排在加序号之前，否则会把手写进去的
    # <span style="..."> 里的引号也换成中文引号，直接废掉 HTML（已踩过）。
    text = fix_quotes(text)
    text, n_img = insert_images(text, plan.get("images", []))
    text, titles = number_headings(text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    note = f"> {args.note}\n\n" if args.note else ""
    final = f"---\ntitle: {title}\ncover: {cover}\n---\n\n{note}{text}\n"
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    open(args.out, "w", encoding="utf-8").write(final)

    # ---- 自检 ----
    print(f"[OK] 已写出 {args.out}")
    print(f"  章节数   : {len(titles)}（去重后 {len(set(titles))}）")
    for i, t in enumerate(titles, 1):
        print(f"    {cn_num(i)}、{t}")
    print(f"  插图数   : {n_img}")
    print(f"  正文字数 : 约 {body_word_count(text)}")
    risks = []
    if len(titles) != len(set(titles)):
        risks.append("章节标题有重复")
    if n_img != len(plan.get("images", [])):
        risks.append("插图数与挂载表不符")
    no_tag = re.sub(r"<[^>]+>", "", text)  # 属性里的引号不算正文残留
    if '"' in no_tag:
        risks.append(f"仍残留半角引号 {no_tag.count(chr(34))} 个")
    if re.search(r"<[a-z]+ [^>]*[“”]", text):
        risks.append("HTML 属性里的引号被误换成中文引号（废掉样式，查 fix_quotes 顺序）")
    if "**" in text and text.count("**") % 2:
        risks.append("加粗标记未闭合")
    print(f"  自检风险 : {'、'.join(risks) if risks else '无'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
