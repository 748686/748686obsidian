#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 Feishu Long Connection Test V1.0

用途：
- 测试飞书官方 SDK 长连接是否成功
- 接收飞书卡片交互回调
- 暂时不连接英语学习系统
- 暂时不连接 Cloudflare
- 暂时不修改 GitHub 文件
"""

import os
import json
import lark_oapi as lark
from lark_oapi.api.card.v1 import *


APP_ID = os.environ.get("FEISHU_APP_ID")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET")


def handle_card_action(data):
    print()
    print("=" * 70)
    print("748686 FEISHU CARD ACTION RECEIVED")
    print("=" * 70)

    try:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception:
        print(data)

    print("=" * 70)

    # 尝试提取最重要的数据
    try:
        event = data.event
        action = event.action

        print()
        print("QUESTION ID:", getattr(action, "value", None))
        print("ACTION:", getattr(action, "tag", None))

    except Exception as e:
        print("解析 action 时出现异常：", repr(e))

    print()
    print(">>> 飞书长连接已经收到卡片交互 <<<")
    print()


def main():
    if not APP_ID:
        raise RuntimeError("缺少环境变量 FEISHU_APP_ID")

    if not APP_SECRET:
        raise RuntimeError("缺少环境变量 FEISHU_APP_SECRET")

    print("=" * 70)
    print("748686 FEISHU LONG CONNECTION TEST V1.0")
    print("=" * 70)
    print()
    print("APP_ID:", APP_ID)
    print("APP_SECRET: 已读取")
    print()
    print("正在建立飞书长连接……")
    print("请保持这个程序持续运行。")
    print()

    event_handler = (
        lark.EventDispatcherHandler.builder(
            "",
            "",
        )
        .register_p2_card_action_trigger(handle_card_action)
        .build()
    )

    client = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.INFO,
    )

    print("正在启动 WebSocket 长连接……")
    print()

    client.start()


if __name__ == "__main__":
    main()
