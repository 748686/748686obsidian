#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Word Image Bot V1.1

============================================================
功能
============================================================

飞书发送单词截图
        ↓
飞书机器人接收图片
        ↓
下载图片
        ↓
OCR：英文 + 中文
        ↓
识别英语 / 中文对应关系
        ↓
生成：

# 今日新词

1. beautiful — 美丽的
2. different — 不同的
3. healthy — 健康的

        ↓
把完整 Markdown 回传飞书


============================================================
当前版本原则
============================================================

1. 不上传 GitHub
2. 不修改现有 main.py
3. 不修改 exam_generate.py
4. 不修改 exam_answers.py
5. 不修改 grader
6. 不生成文章
7. 不生成试卷
8. 不生成音频
9. 不写入 input 文件夹
10. 只生成 Markdown 并回传飞书

后续 V1.2：
    用户确认
        ↓
    写入：
    02_英语学习系统/input/YYYY-MM-DD.md

后续 V2：
    写入后
        ↓
    上传 GitHub
"""


import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import requests
import pytesseract

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter

import lark_oapi as lark


# ============================================================
# 配置
# ============================================================

APP_ID = os.environ.get(
    "FEISHU_APP_ID",
    ""
).strip()

APP_SECRET = os.environ.get(
    "FEISHU_APP_SECRET",
    ""
).strip()

if not APP_ID:
    raise RuntimeError(
        "缺少环境变量 FEISHU_APP_ID"
    )

if not APP_SECRET:
    raise RuntimeError(
        "缺少环境变量 FEISHU_APP_SECRET"
    )


FEISHU_BASE = "https://open.feishu.cn"


# ============================================================
# 日志
# ============================================================

def log(message):
    print(
        f"[748686 FeishuWordBot] {message}",
        flush=True
    )


# ============================================================
# 获取 tenant_access_token
# ============================================================

def get_tenant_access_token():

    url = (
        f"{FEISHU_BASE}"
        "/open-apis/auth/v3/"
        "tenant_access_token/internal"
    )

    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    }

    response = requests.post(
        url,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != 0:

        raise RuntimeError(
            "获取 tenant_access_token 失败：\n"
            + json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            )
        )

    return data["tenant_access_token"]


# ============================================================
# 下载用户消息中的图片
# ============================================================

def download_message_image(
    token,
    message_id,
    image_key,
    output_path,
):
    """
    用户在飞书消息中发送的图片：

    GET
    /open-apis/im/v1/messages/
    {message_id}/resources/
    {image_key}?type=image
    """

    url = (
        f"{FEISHU_BASE}"
        "/open-apis/im/v1/messages/"
        f"{message_id}/resources/"
        f"{image_key}"
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    params = {
        "type": "image",
    }

    log("正在下载飞书图片...")

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=60,
    )

    if response.status_code != 200:

        raise RuntimeError(
            "下载飞书图片失败\n"
            f"HTTP: {response.status_code}\n"
            f"{response.text[:2000]}"
        )

    Path(output_path).write_bytes(
        response.content
    )

    file_size = Path(
        output_path
    ).stat().st_size

    log(
        f"图片下载完成："
        f"{file_size:,} bytes"
    )

    return output_path


# ============================================================
# 图片预处理
# ============================================================

def preprocess_image(image_path):

    image = Image.open(
        image_path
    )

    log(
        "原始图片："
        f"{image.width} × {image.height}"
    )

    if image.mode != "RGB":
        image = image.convert("RGB")

    # 放大两倍
    image = image.resize(
        (
            image.width * 2,
            image.height * 2,
        )
    )

    # 灰度
    image = image.convert("L")

    # 增强对比度
    image = ImageEnhance.Contrast(
        image
    ).enhance(1.5)

    # 轻度锐化
    image = image.filter(
        ImageFilter.SHARPEN
    )

    return image


# ============================================================
# OCR
# ============================================================

def run_ocr(image_path):

    log("开始 OCR...")

    image = preprocess_image(
        image_path
    )

    try:

        text = pytesseract.image_to_string(
            image,
            lang="eng+chi_sim",
            config="--psm 6",
        )

    except Exception as exc:

        raise RuntimeError(
            "Tesseract OCR 执行失败。\n"
            "请检查：\n"
            "1. tesseract 是否安装\n"
            "2. eng 是否安装\n"
            "3. chi_sim 是否安装\n\n"
            f"原始错误：{exc}"
        )

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    log("OCR 完成")

    print()
    print(
        "================ OCR 原始结果 ================"
    )
    print(text)
    print(
        "================================================"
    )
    print()

    return text


# ============================================================
# 清洗 OCR 行
# ============================================================

def clean_line(line):

    line = line.strip()

    if not line:
        return ""

    # 删除 OCR 常见项目符号噪声
    line = re.sub(
        r"^[|¦•·▪●○◆◇]+\s*",
        "",
        line,
    )

    # 合并连续空格
    line = re.sub(
        r"\s+",
        " ",
        line,
    )

    return line.strip()


# ============================================================
# 判断中文
# ============================================================

def has_chinese(text):

    return bool(
        re.search(
            r"[\u4e00-\u9fff]",
            text
        )
    )


# ============================================================
# 判断英文
# ============================================================

def has_english(text):

    return bool(
        re.search(
            r"[A-Za-z]",
            text
        )
    )


# ============================================================
# 判断是否像英语单词 / 英语短语
# ============================================================

def looks_like_english(text):

    if not has_english(text):
        return False

    # 去掉英语允许字符
    remaining = re.sub(
        r"[A-Za-z0-9\s'\-./]+",
        "",
        text,
    )

    # 剩余中文太多，不认为是纯英语
    chinese_count = len(
        re.findall(
            r"[\u4e00-\u9fff]",
            text
        )
    )

    english_count = len(
        re.findall(
            r"[A-Za-z]",
            text
        )
    )

    if chinese_count > english_count:
        return False

    # OCR 噪声过多
    if len(remaining) > 3:
        return False

    return True


# ============================================================
# 清理英语
# ============================================================

def clean_english(text):

    text = text.strip()

    # 去掉编号
    text = re.sub(
        r"^\d+[\s.)、-]+",
        "",
        text,
    )

    # 去掉常见 OCR 前缀
    text = re.sub(
        r"^[•·▪●○]+\s*",
        "",
        text,
    )

    return text.strip()


# ============================================================
# 清理中文
# ============================================================

def clean_chinese(text):

    text = text.strip()

    # 去掉编号
    text = re.sub(
        r"^\d+[\s.)、-]+",
        "",
        text,
    )

    return text.strip()


# ============================================================
# 处理单行：
#
# beautiful — 美丽的
# beautiful - 美丽的
# beautiful：美丽的
# ============================================================

def parse_inline_pair(line):

    patterns = [
        r"^([A-Za-z][A-Za-z0-9\s'\-./]+?)\s*[—–−-]\s*([\u4e00-\u9fff].*)$",

        r"^([A-Za-z][A-Za-z0-9\s'\-./]+?)\s*[：:]\s*([\u4e00-\u9fff].*)$",

        r"^([A-Za-z][A-Za-z0-9\s'\-./]+?)\s+([\u4e00-\u9fff].*)$",
    ]

    for pattern in patterns:

        match = re.match(
            pattern,
            line,
        )

        if not match:
            continue

        english = clean_english(
            match.group(1)
        )

        chinese = clean_chinese(
            match.group(2)
        )

        if not english:
            continue

        if not chinese:
            continue

        return {
            "english": english,
            "chinese": chinese,
        }

    return None


# ============================================================
# 解析 OCR
# ============================================================

def parse_word_pairs(raw_text):

    raw_lines = raw_text.splitlines()

    lines = []

    for raw_line in raw_lines:

        line = clean_line(
            raw_line
        )

        if line:
            lines.append(line)

    entries = []

    i = 0

    while i < len(lines):

        current = lines[i]

        # ----------------------------------------------------
        # 1. 先尝试：
        #
        # beautiful — 美丽的
        # ----------------------------------------------------

        inline = parse_inline_pair(
            current
        )

        if inline:

            entries.append(
                inline
            )

            i += 1
            continue

        # ----------------------------------------------------
        # 2. 再处理：
        #
        # beautiful
        # 美丽的
        # ----------------------------------------------------

        if looks_like_english(
            current
        ):

            english = clean_english(
                current
            )

            chinese_parts = []

            j = i + 1

            while j < len(lines):

                next_line = lines[j]

                # 如果下一个又是英语，
                # 说明没有中文解释
                if looks_like_english(
                    next_line
                ):
                    break

                if has_chinese(
                    next_line
                ):

                    chinese_parts.append(
                        clean_chinese(
                            next_line
                        )
                    )

                    j += 1
                    continue

                # 忽略词性
                if re.fullmatch(
                    r"(n|v|adj|adv|prep|conj|pron|"
                    r"vt|vi|aux|modal)\.?",
                    next_line,
                    flags=re.IGNORECASE,
                ):

                    j += 1
                    continue

                break

            if chinese_parts:

                chinese = " ".join(
                    chinese_parts
                )

                entries.append(
                    {
                        "english": english,
                        "chinese": chinese,
                    }
                )

                i = j
                continue

        i += 1

    return deduplicate_entries(
        entries
    )


# ============================================================
# 去重
# ============================================================

def deduplicate_entries(
    entries
):

    result = []

    seen = set()

    for item in entries:

        english = (
            item["english"]
            .strip()
        )

        chinese = (
            item["chinese"]
            .strip()
        )

        if not english:
            continue

        if not chinese:
            continue

        key = english.lower()

        if key in seen:
            continue

        seen.add(key)

        result.append(
            {
                "english": english,
                "chinese": chinese,
            }
        )

    return result


# ============================================================
# 生成最终 MD
# ============================================================

def build_markdown(
    entries
):

    if not entries:
        return None

    md = []

    md.append(
        "# 今日新词"
    )

    md.append("")

    for index, item in enumerate(
        entries,
        start=1,
    ):

        english = item[
            "english"
        ]

        chinese = item[
            "chinese"
        ]

        md.append(
            f"{index}. "
            f"{english} — {chinese}"
        )

    md.append("")

    return "\n".join(
        md
    )


# ============================================================
# OCR 无法配对时的备用 MD
# ============================================================

def build_fallback_markdown(
    raw_text
):

    md = []

    md.append(
        "# 今日新词"
    )

    md.append("")

    index = 1

    for raw_line in raw_text.splitlines():

        line = clean_line(
            raw_line
        )

        if not line:
            continue

        # 去掉原 OCR 编号
        line = re.sub(
            r"^\d+[\s.)、-]+",
            "",
            line,
        )

        md.append(
            f"{index}. {line}"
        )

        index += 1

    md.append("")

    return "\n".join(
        md
    )


# ============================================================
# 分割飞书长消息
# ============================================================

def split_message(
    text,
    max_chars=5000,
):

    if len(text) <= max_chars:
        return [text]

    chunks = []

    current = []

    length = 0

    for line in text.splitlines(
        keepends=True
    ):

        if (
            length + len(line)
            > max_chars
        ):

            if current:

                chunks.append(
                    "".join(
                        current
                    )
                )

            current = []
            length = 0

        current.append(
            line
        )

        length += len(line)

    if current:

        chunks.append(
            "".join(
                current
            )
        )

    return chunks


# ============================================================
# 发送飞书回复
# ============================================================

def reply_message(
    token,
    message_id,
    text,
):

    url = (
        f"{FEISHU_BASE}"
        "/open-apis/im/v1/messages/"
        f"{message_id}/reply"
    )

    headers = {
        "Authorization":
            f"Bearer {token}",

        "Content-Type":
            "application/json; charset=utf-8",
    }

    payload = {
        "msg_type": "text",
        "content": json.dumps(
            {
                "text": text
            },
            ensure_ascii=False,
        ),
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if response.status_code != 200:

        raise RuntimeError(
            "发送飞书回复失败：\n"
            f"HTTP {response.status_code}\n"
            f"{response.text[:2000]}"
        )

    data = response.json()

    if data.get("code") != 0:

        raise RuntimeError(
            "飞书回复 API 失败：\n"
            + json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )
        )


# ============================================================
# 处理图片消息
# ============================================================

def process_image_message(
    event_data
):

    message = (
        event_data.event.message
    )

    message_id = (
        message.message_id
    )

    message_type = (
        message.message_type
    )

    content = (
        message.content
    )

    log("=" * 70)
    log("收到飞书消息")
    log(f"message_id = {message_id}")
    log(f"message_type = {message_type}")
    log("=" * 70)

    # --------------------------------------------------------
    # 只处理图片
    # --------------------------------------------------------

    if message_type != "image":

        log(
            "不是图片消息，忽略。"
        )

        return

    # --------------------------------------------------------
    # 解析 content
    # --------------------------------------------------------

    try:

        content_data = json.loads(
            content
        )

    except Exception as exc:

        raise RuntimeError(
            "图片消息 content JSON "
            "解析失败："
            f"{exc}"
        )

    image_key = (
        content_data.get(
            "image_key"
        )
    )

    if not image_key:

        raise RuntimeError(
            "图片消息中没有找到 "
            "image_key。"
        )

    log(
        f"image_key = {image_key}"
    )

    # --------------------------------------------------------
    # Token
    # --------------------------------------------------------

    token = (
        get_tenant_access_token()
    )

    # --------------------------------------------------------
    # 临时目录
    # --------------------------------------------------------

    with tempfile.TemporaryDirectory(
        prefix="748686_word_"
    ) as temp_dir:

        image_path = (
            Path(temp_dir)
            / "word_image"
        )

        # ----------------------------------------------------
        # 下载
        # ----------------------------------------------------

        download_message_image(
            token=token,
            message_id=message_id,
            image_key=image_key,
            output_path=image_path,
        )

        # ----------------------------------------------------
        # OCR
        # ----------------------------------------------------

        raw_text = run_ocr(
            image_path
        )

        # ----------------------------------------------------
        # 解析
        # ----------------------------------------------------

        entries = parse_word_pairs(
            raw_text
        )

        log(
            f"识别并配对："
            f"{len(entries)} 个"
        )

        # ----------------------------------------------------
        # 生成 MD
        # ----------------------------------------------------

        markdown = build_markdown(
            entries
        )

        # ----------------------------------------------------
        # 如果没有可靠配对
        # ----------------------------------------------------

        if not markdown:

            log(
                "没有形成可靠的"
                "英语/中文配对。"
            )

            markdown = (
                build_fallback_markdown(
                    raw_text
                )
            )

        # ----------------------------------------------------
        # 打印 MD
        # ----------------------------------------------------

        print()
        print(
            "================ 生成 MD ================"
        )
        print(markdown)
        print(
            "=========================================="
        )
        print()

        # ----------------------------------------------------
        # 先回复处理结果
        # ----------------------------------------------------

        count = len(entries)

        if count > 0:

            status = (
                "✅ 图片识别完成\n\n"
                f"共识别 {count} 个单词/短语。\n\n"
                "下面是生成的 MD："
            )

        else:

            status = (
                "⚠️ 已读取图片，但暂时没有"
                "可靠识别出英语/中文配对。\n\n"
                "下面保留 OCR 结果生成的 MD："
            )

        reply_message(
            token=token,
            message_id=message_id,
            text=status,
        )

        # ----------------------------------------------------
        # 回传 Markdown
        # ----------------------------------------------------

        chunks = split_message(
            markdown
        )

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            if len(chunks) == 1:

                title = (
                    "📄 MD 内容\n\n"
                )

            else:

                title = (
                    f"📄 MD 内容 "
                    f"({index}/{len(chunks)})\n\n"
                )

            reply_message(
                token=token,
                message_id=message_id,
                text=(
                    title
                    + chunk
                ),
            )

    log(
        "图片 → MD → 飞书回传完成。"
    )


# ============================================================
# 消息事件处理
# ============================================================

def handle_message(
    data
):

    try:

        process_image_message(
            data
        )

    except Exception as exc:

        log(
            "处理图片失败："
            f"{type(exc).__name__}: "
            f"{exc}"
        )

        # 尝试回复错误
        try:

            token = (
                get_tenant_access_token()
            )

            message_id = (
                data.event.message.message_id
            )

            reply_message(
                token=token,
                message_id=message_id,
                text=(
                    "❌ 图片处理失败\n\n"
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
            )

        except Exception as reply_exc:

            log(
                "错误回复也失败："
                f"{reply_exc}"
            )


# ============================================================
# 主程序
# ============================================================

def main():

    log("=" * 70)
    log(
        "748686 飞书新学单词机器人 V1.1"
    )
    log("=" * 70)

    log(
        "当前模式："
        "图片 → MD → 飞书回传"
    )

    log(
        "当前不会写入 GitHub。"
    )

    log(
        "当前不会写入 input 文件夹。"
    )

    log(
        "FEISHU_APP_ID 已读取。"
    )

    log(
        "正在建立飞书长连接..."
    )

    # --------------------------------------------------------
    # 飞书事件分发器
    # --------------------------------------------------------

    event_handler = (
        lark.EventDispatcherHandler.builder(
            "",
            "",
            lark.LogLevel.INFO,
        )
        .register_p2_im_message_receive_v1(
            handle_message
        )
        .build()
    )

    # --------------------------------------------------------
    # WebSocket 长连接
    # --------------------------------------------------------

    ws_client = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        log_level=lark.LogLevel.INFO,
        event_handler=event_handler,
        auto_reconnect=True,
    )

    log("=" * 70)
    log(
        "机器人启动成功。"
    )
    log(
        "现在可以在飞书向机器人发送单词截图。"
    )
    log(
        "按 Ctrl+C 停止。"
    )
    log("=" * 70)

    ws_client.start()


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()

        log(
            "机器人已停止。"
        )

    except Exception as exc:

        log(
            "程序启动失败："
            f"{type(exc).__name__}: "
            f"{exc}"
        )

        sys.exit(1)
