#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Word Highlight Test V2

目的：
- 独立测试飞书 lark_md 对颜色和粗体的支持
- 不修改生产 Renderer
- 不读取真实英语学习数据
- 不修改任何生产文件

测试单词：
expand
significant

测试方式：
1. Markdown 粗体
2. <font color>
3. <font color> + <b>
4. Markdown 粗体 + <font color>
"""

import os
import sys
import requests


FEISHU_BASE = "https://open.feishu.cn"


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
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
            f"响应中没有 tenant_access_token：{data}"
        )

    return token


def send_card(webhook: str, card: dict):
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
    print("响应：", response.text)

    response.raise_for_status()

    data = response.json()

    if data.get("code", 0) != 0:
        raise RuntimeError(
            f"飞书发送失败：{data}"
        )

    return data


def build_card():
    return {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": "748686｜飞书文字效果测试 V2"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "## 测试文章\n\n"
                        "The company decided to expand its business because "
                        "the market showed significant growth.\n\n"
                        "---\n\n"

                        "### 测试 1｜Markdown 粗体\n"
                        "**expand**\n\n"

                        "### 测试 2｜font 颜色\n"
                        "<font color='blue'>expand</font>\n\n"

                        "### 测试 3｜font + b\n"
                        "<font color='blue'><b>expand</b></font>\n\n"

                        "### 测试 4｜Markdown + font\n"
                        "**<font color='blue'>expand</font>**\n\n"

                        "---\n\n"

                        "### 第二个单词\n"
                        "**significant**\n\n"
                        "<font color='blue'>significant</font>\n\n"
                        "<font color='blue'><b>significant</b></font>\n\n"
                        "**<font color='blue'>significant</font>**\n\n"

                        "---\n\n"
                        "请观察：\n"
                        "- 哪一种会变粗？\n"
                        "- 哪一种会变蓝？\n"
                        "- 哪一种仍然是黑色普通字体？"
                    )
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
    print("748686 FEISHU WORD HIGHLIGHT TEST V2")
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
    print("检查飞书应用凭证...")

    token = get_tenant_access_token(
        app_id,
        app_secret,
    )

    if token:
        print("✓ 飞书应用凭证正常")

    print()
    print("准备发送测试卡片...")

    card = build_card()

    send_card(
        webhook,
        card,
    )

    print()
    print("=" * 60)
    print("✓ FEISHU WORD HIGHLIGHT TEST V2 SENT")
    print("=" * 60)
    print()
    print("请打开飞书查看测试卡片。")


if __name__ == "__main__":
    main()
