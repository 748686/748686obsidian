#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Word Highlight Test V4

目的：
只测试飞书 lark_md 中可能实现“单词背景/标签效果”的写法。

目标视觉：

浅蓝色背景
深蓝色粗体
expand

注意：
- 不修改生产 Renderer
- 不读取真实文章
- 不修改任何生产文件
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
        "## 748686｜单词背景效果测试 V4\n\n"

        "下面每一行都是独立测试。\n\n"

        "---\n\n"

        "### A｜已经确认可用：蓝色 + 粗体\n\n"
        "**<font color='blue'>expand</font>**\n\n"

        "---\n\n"

        "### B｜测试：blue 标签\n\n"
        "<font color='blue'>[expand]</font>\n\n"

        "---\n\n"

        "### C｜测试：蓝色粗体 + 方括号\n\n"
        "**<font color='blue'>[expand]</font>**\n\n"

        "---\n\n"

        "### D｜测试：代码样式\n\n"
        "`expand`\n\n"

        "---\n\n"

        "### E｜测试：代码样式 + 蓝色粗体\n\n"
        "**<font color='blue'>`expand`</font>**\n\n"

        "---\n\n"

        "### F｜测试：HTML 背景（对照组）\n\n"
        "<span style='background-color:#DCEEFF;color:#0B3B82;font-weight:bold;'>expand</span>\n\n"

        "---\n\n"

        "### G｜测试：背景色 + 蓝色粗体（对照组）\n\n"
        "<span style='background:#DCEEFF;'><font color='blue'><b>expand</b></font></span>\n\n"

        "---\n\n"

        "### H｜目标效果参考\n\n"
        "🟦 **<font color='blue'>expand</font>**\n\n"

        "注意：H 只是视觉参考，不是最终方案。\n\n"

        "---\n\n"

        "第二个单词：\n\n"

        "**<font color='blue'>significant</font>**\n\n"

        "`significant`\n\n"

        "<span style='background-color:#DCEEFF;color:#0B3B82;font-weight:bold;'>significant</span>"
    )

    return {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": "748686｜单词背景效果测试 V4"
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
    print("748686 FEISHU WORD HIGHLIGHT TEST V4")
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
        app_secret
    )

    print("✓ 飞书应用凭证正常")

    print()
    print("发送 V4 测试卡片...")

    card = build_card()

    send_card(
        webhook,
        card
    )

    print()
    print("=" * 60)
    print("✓ FEISHU WORD HIGHLIGHT TEST V4 SENT")
    print("=" * 60)


if __name__ == "__main__":
    main()
