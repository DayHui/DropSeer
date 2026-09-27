#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
公众号封面高清版导出（补做）
============================
背景：微信图文封面官方推荐 900x383（2.35:1），但在手机上封面被拉伸到约 1080 物理像素宽，
      900px 源被放大 + 微信二次压缩 → 黑底 + 细银线这种高对比细线最容易发糊（实测反馈"不够清晰"）。

做法：不动设计、不改符号，只用同一套制图函数**按更高分辨率重新渲染**（PIL 直接矢量绘制，
      不是放大位图），并额外留出安全边距，让微信压缩后仍锐利。

用法：
    python gen_cover_hires.py
产出：
    04_成品/封面_公众号_高清_1800x767.png
    04_成品/封面_公众号_热点周报_高清_1800x767.png
    04_成品/封面_公众号_高清_1080x460.png
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_dropseer_assets as B  # noqa: E402

W, H = 1800, 767          # 2.347:1，与 900x383 同比例
W2, H2 = 1080, 460        # 微信实际展示宽度量级，作为备选

if __name__ == "__main__":
    # 主封面（通用）
    B.cover_wide(W, H, "void", "silver", "公众号_高清", series=B.TAGLINE, series_color="amber")
    B.cover_wide(W, H, "void", "silver", "公众号_热点周报_高清",
                 series="热点周报", series_color="amber")
    B.cover_wide(W2, H2, "void", "silver", "公众号_高清", series=B.TAGLINE, series_color="amber")
    print("done（原始 900x383 版本保留不动）")
