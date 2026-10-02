#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 Feishu Word Highlight Test V1.0

用途：
------------------------------------------------------------
独立测试飞书卡片中：

    浅蓝色背景
    +
    深蓝色粗体文字

是否能够真正包住单词本身。

测试单词：
    expand
    significant

注意：
------------------------------------------------------------
本脚本完全独立：
- 不读取英语学习系统
- 不修改任何 Markdown
- 不修改 main.py
- 不修改 Feishu Renderer V2.1
- 只发送一张测试卡片
"""

from __future__ import annotations

import json
import os
import sys

import requests


# ============================================================
# Feishu
# ============================================================

FEISHU_BASE = "https://open.feishu.cn"

TOKEN_URL = (
    f"{FEISHU_BASE}/open-apis/auth/v3/"
    "tenant_access_token/internal"
)


# ============================================================
# 日志
# ============================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    raise RuntimeError(message)


# ============================================================
# 获取 Token
# ============================================================

def get_tenant_access_token(
    app_id: str,
    app_secret: str,
) -> str:

    response = requests.post(
        TOKEN_URL,
        json={
            "app_id": app_id,
            "app_secret": app_secret,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != 0:
        fail(
            "获取 Feishu Token 失败：\n"
            + json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )
        )

    token = data.get(
        "tenant_access_token"
    )

    if not token:
        fail(
            "Feishu 返回结果没有 "
            "tenant_access_token"
        )

    return token


# ============================================================
# 测试卡片
# ============================================================

def make_test_card() -> dict:

    # --------------------------------------------------------
    # 这里就是我们要测试的重点
    #
    # 方案：
    # 让单词本身拥有浅蓝色背景 + 深蓝色粗体
    #
    # 如果飞书 lark_md 不支持 background，
    # 飞书会直接显示实际解析效果。
    # --------------------------------------------------------

    test_word_1 = (
        "<span style="
        "\"background-color:#DCEEFF;"
        "color:#0B3B82;"
        "font-weight:bold;"
        "padding:2px 5px;\""
        ">expand</span>"
    )

    test_word_2 = (
        "<span style="
        "\"background-color:#DCEEFF;"
        "color:#0B3B82;"
        "font-weight:bold;"
        "padding:2px 5px;\""
        ">significant</span>"
    )

    paragraph = (
        "The company decided to "
        f"{test_word_1} "
        "its business because the market "
        "showed "
        f"{test_word_2} "
        "growth."
    )

    return {

        "config": {
            "wide_screen_mode": True,
            "enable_forward": True,
        },

        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": (
                    "🧪 飞书单词高亮测试"
                ),
            },
        },

        "elements": [

            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "# English Word Highlight Test\n\n"
                        "测试目标："
                        "浅蓝色背景 + 深蓝色粗体\n\n"
                    ),
                },
            },

            {
                "tag": "hr",
            },

            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": paragraph,
                },
            },

            {
                "tag": "hr",
            },

            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "**测试单词**\n\n"
                        f"{test_word_1}　expand = 扩大；扩展\n\n"
                        f"{test_word_2}　significant = "
                        "重要的；显著的"
                    ),
                },
            },

            {
                "tag": "hr",
            },

            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "如果上面的两个单词显示为：\n\n"
                        "浅蓝色底 + 深蓝色粗体\n\n"
                        "说明这种方式可以继续接入你的 "
                        "English Renderer。"
                    ),
                },
            },
        ],
    }


# ============================================================
# 发送
# ============================================================

def send_card(
    webhook: str,
    card: dict,
) -> dict:

    response = requests.post(
        webhook,
        headers={
            "Content-Type":
                "application/json; charset=utf-8"
        },
        json={
            "msg_type": "interactive",
            "card": card,
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != 0:
        fail(
            "Feishu Webhook 发送失败：\n"
            + json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )
        )

    return data


# ============================================================
# Main
# ============================================================

def main() -> None:

    webhook = os.getenv(
        "FEISHU_WEBHOOK",
        "",
    ).strip()

    app_id = os.getenv(
        "APP_ID",
        "",
    ).strip()

    app_secret = os.getenv(
        "APP_SECRET",
        "",
    ).strip()

    if not webhook:
        fail(
            "缺少环境变量 FEISHU_WEBHOOK"
        )

    if not app_id:
        fail(
            "缺少环境变量 APP_ID"
        )

    if not app_secret:
        fail(
            "缺少环境变量 APP_SECRET"
        )

    log()
    log("=" * 70)
    log("748686 Feishu Word Highlight Test V1.0")
    log("=" * 70)

    log()
    log("测试单词：")
    log("  expand")
    log("  significant")

    log()
    log("目标效果：")
    log("  浅蓝色背景")
    log("  深蓝色文字")
    log("  粗体")
    log("  背景直接包住单词本身")

    log()
    log("→ 获取 Feishu Token")

    token = get_tenant_access_token(
        app_id,
        app_secret,
    )

    log("✓ Token 获取成功")

    # Token 在这里主要用于确认 APP_ID / APP_SECRET 正常。
    # 实际发送仍然使用现有 Webhook。

    _ = token

    log()
    log("→ 创建测试卡片")

    card = make_test_card()

    log("✓ 测试卡片创建完成")

    log()
    log("→ 发送到飞书")

    result = send_card(
        webhook,
        card,
    )

    log("✓ 飞书发送成功")

    log()
    log(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )

    log()
    log("=" * 70)
    log("✓ 测试完成")
    log("=" * 70)


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        log("用户中断")
        sys.exit(130)

    except Exception as exc:

        log()
        log("=" * 70)
        log("❌ 测试失败")
        log("=" * 70)
        log(str(exc))
        sys.exit(1)
