#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Word Highlight Test V3

本次测试：
- 使用飞书卡片原生 markdown / rich text 能力
- 不使用 HTML
- 不使用 <span>
- 不使用 <font>
- 不使用 <b>
- 不修改生产 Renderer

目标：
确认飞书原生卡片富文本到底支持哪些文字样式。
"""

import os
import sys
import requests


FEISHU_BASE = "https://open.feishu.cn"


def get_tenant_access_token(app_id, app_secret):
    url = f"{FEISHU_BASE}/open-apis/auth/v3/tenant_access_token/internal"

    response = requests.post(
        url,
        json={
            "app_id": app_id,
            "app_secret": app_secret,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != 0:
        raise RuntimeError(
            f"获取 tenant_access_token 失败：{data}"
        )

    token = data.get("tenant_access_token")

    if not token:
        raise RuntimeError(
            f"没有获取到 tenant_access_token：{data}"
        )

    return token


def send_card(webhook, card):
    payload = {
        "msg_type": "interactive",
        "card": card,
    }

    response = requests.post(
        webhook,
        json=payload,
        timeout=30,
    )

    print("HTTP 状态码：", response.status_code)
    print("飞书响应：", response.text)

    response.raise_for_status()

    data = response.json()

    if data.get("code", 0) != 0:
        raise RuntimeError(
            f"飞书发送失败：{data}"
        )


def build_card():

    content = (
        "## 748686｜原生富文本测试 V3\n\n"

        "正常文字：expand\n\n"

        "---\n\n"

        "### 测试 1｜Markdown 粗体\n"
        "**expand**\n\n"

        "### 测试 2｜Markdown 斜体\n"
        "*expand*\n\n"

        "### 测试 3｜Markdown 删除线\n"
        "~~expand~~\n\n"

        "### 测试 4｜颜色语法\n"
        "<font color='red'>expand</font>\n\n"

        "### 测试 5｜粗体 + 颜色\n"
        "**<font color='red'>expand</font>**\n\n"

        "---\n\n"

        "### 第二个单词\n\n"

        "**significant**\n\n"

        "*significant*\n\n"

        "~~significant~~\n\n"

        "<font color='red'>significant</font>\n\n"

        "**<font color='red'>significant</font>**\n\n"

        "---\n\n"

        "如果只有 Markdown 粗体生效，"
        "说明当前卡片文本解析器只接受 Markdown。\n\n"

        "如果颜色也生效，"
        "我们再继续测试背景效果。"
    )

    return {
        "config": {
            "wide_screen_mode": True
        },

        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": "748686｜原生富文本测试 V3"
            }
        },

        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            }
        ]
    }


def main():

    webhook = os.getenv("FEISHU_WEBHOOK", "").strip()
    app_id = os.getenv("APP_ID", "").strip()
    app_secret = os.getenv("APP_SECRET", "").strip()

    print()
    print("=" * 60)
    print("748686 FEISHU WORD HIGHLIGHT TEST V3")
    print("=" * 60)

    if not webhook:
        print("❌ FEISHU_WEBHOOK 未设置")
        sys.exit(1)

    if not app_id:
        print("❌ APP_ID 未设置")
        sys.exit(1)

    if not app_secret:
        print("❌ APP_SECRET 未设置")
        sys.exit(1)

    print("✓ FEISHU_WEBHOOK 已设置")
    print("✓ APP_ID 已设置")
    print("✓ APP_SECRET 已设置")

    print()
    print("验证飞书应用凭证...")

    get_tenant_access_token(
        app_id,
        app_secret,
    )

    print("✓ 飞书应用凭证正常")

    print()
    print("发送原生富文本测试卡片...")

    card = build_card()

    send_card(
        webhook,
        card,
    )

    print()
    print("=" * 60)
    print("✓ FEISHU WORD HIGHLIGHT TEST V3 SENT")
    print("=" * 60)


if __name__ == "__main__":
    main()
