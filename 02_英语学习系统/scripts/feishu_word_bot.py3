#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Word Bot V3.0

功能：
1. 飞书文字消息 -> 自动整理 -> GitHub
2. 飞书图片消息 -> OCR -> 自动整理 -> GitHub
3. 图片和文字最终使用同一个词条解析器
4. 不限制每天单词数量
5. 自动删除软件界面无用文字
6. 自动提取：
      英文单词
      词性
      中文释义
7. 当天已有单词自动去重
8. 如果当天已有旧的错误词条，而本次重新发送了正确词条，
   使用新识别结果覆盖旧结果
9. 只有 GitHub push 成功后，才报告成功
10. 只写入：
      02_英语学习系统/input/YYYY-MM-DD.md

不修改：
- exam_generate.py
- exam_answers.py
- exam_parser.py
- exam_grader.py
- main.py
- 其他英语学习系统核心程序

日期：
- GitHub Actions Runner UTC
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import lark_oapi as lark


# ============================================================
# 配置
# ============================================================

APP_ID = os.environ.get("FEISHU_APP_ID", "").strip()
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "").strip()

TARGET_CHAT_NAME = "748686知识系统"
FEISHU_BASE = "https://open.feishu.cn"

REPO_ROOT = Path(
    os.environ.get("GITHUB_WORKSPACE", os.getcwd())
).resolve()

INPUT_DIR = REPO_ROOT / "02_英语学习系统" / "input"

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "").strip()
GITHUB_REF_NAME = os.environ.get("GITHUB_REF_NAME", "").strip()


# ============================================================
# 运行期间消息去重
# ============================================================

_processed_message_ids = set()
_processing_message_ids = set()
_message_lock = threading.Lock()


# ============================================================
# Token 缓存
# ============================================================

_token_lock = threading.Lock()
_cached_token = None
_token_expiry = 0


if not APP_ID:
    raise RuntimeError("缺少环境变量 FEISHU_APP_ID")

if not APP_SECRET:
    raise RuntimeError("缺少环境变量 FEISHU_APP_SECRET")


# ============================================================
# 日志
# ============================================================

def log(message):
    now = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
    print(
        f"[748686 FeishuWordBot V3.0] "
        f"[{now}] {message}",
        flush=True,
    )


# ============================================================
# 飞书 Token
# ============================================================

def get_tenant_access_token(force_refresh=False):
    global _cached_token, _token_expiry

    with _token_lock:
        if (
            not force_refresh
            and _cached_token
            and time.time() < _token_expiry
        ):
            return _cached_token

        url = (
            f"{FEISHU_BASE}/open-apis/auth/v3/"
            "tenant_access_token/internal"
        )

        response = requests.post(
            url,
            json={
                "app_id": APP_ID,
                "app_secret": APP_SECRET,
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        if (
            data.get("code") != 0
            or not data.get("tenant_access_token")
        ):
            raise RuntimeError(
                "获取飞书 Token 失败："
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )[:2000]
            )

        _cached_token = data["tenant_access_token"]

        _token_expiry = time.time() + max(
            60,
            int(data.get("expire", 7200)) - 300,
        )

        return _cached_token


# ============================================================
# 查找目标群
# ============================================================

def find_target_chat(token):
    log(f"正在查找目标群：{TARGET_CHAT_NAME}")

    url = f"{FEISHU_BASE}/open-apis/im/v1/chats"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    page_token = ""

    while True:
        params = {
            "page_size": 100
        }

        if page_token:
            params["page_token"] = page_token

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        if data.get("code") != 0:
            raise RuntimeError(
                "查询群列表失败："
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )[:2000]
            )

        result = data.get("data", {})

        for chat in result.get("items", []):
            if chat.get("name") == TARGET_CHAT_NAME:
                chat_id = chat.get("chat_id")

                if not chat_id:
                    raise RuntimeError(
                        "找到目标群，但 chat_id 为空。"
                    )

                log(
                    f"目标群已找到：{TARGET_CHAT_NAME}"
                )

                return chat_id

        if not result.get("has_more"):
            break

        page_token = result.get("page_token", "")

        if not page_token:
            break

    raise RuntimeError(
        f"没有找到目标群「{TARGET_CHAT_NAME}」。"
        "请确认机器人已经加入该群。"
    )


# ============================================================
# 飞书消息
# ============================================================

def send_group_text(token, chat_id, text):
    url = (
        f"{FEISHU_BASE}/open-apis/im/v1/messages"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }

    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps(
            {"text": text},
            ensure_ascii=False,
        ),
    }

    response = requests.post(
        url,
        headers=headers,
        params={
            "receive_id_type": "chat_id"
        },
        json=payload,
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    if data.get("code") != 0:
        raise RuntimeError(
            "发送群消息失败："
            + json.dumps(
                data,
                ensure_ascii=False,
            )[:2000]
        )


def reply_message(token, message_id, text):
    url = (
        f"{FEISHU_BASE}/open-apis/im/v1/messages/"
        f"{message_id}/reply"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }

    payload = {
        "msg_type": "text",
        "content": json.dumps(
            {"text": text},
            ensure_ascii=False,
        ),
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    if data.get("code") != 0:
        raise RuntimeError(
            "回复原消息失败："
            + json.dumps(
                data,
                ensure_ascii=False,
            )[:2000]
        )


def notify(message_id, chat_id, text):
    """
    优先回复原消息。
    回复失败后，通过群消息发送。
    """

    try:
        token = get_tenant_access_token()

        if message_id:
            reply_message(
                token,
                message_id,
                text,
            )
        else:
            send_group_text(
                token,
                chat_id,
                text,
            )

        log("飞书通知发送成功。")
        return True

    except Exception as exc:
        log(
            f"原消息回复失败："
            f"{type(exc).__name__}: {exc}"
        )

    try:
        token = get_tenant_access_token(
            force_refresh=True
        )

        send_group_text(
            token,
            chat_id,
            text,
        )

        log("已通过群消息方式发送通知。")
        return True

    except Exception as exc:
        log(
            f"群消息备用通知失败："
            f"{type(exc).__name__}: {exc}"
        )

        return False


# ============================================================
# 启动卡片
# ============================================================

def send_connection_card(token, chat_id):
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "green",
            "title": {
                "tag": "plain_text",
                "content":
                    "🟢 748686 英语单词录入系统 V3.0",
            },
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "**飞书长连接已启动**\n\n"
                        "现在支持两种方式：\n\n"
                        "📝 **直接粘贴单词文字**\n"
                        "系统自动整理并写入 GitHub。\n\n"
                        "📷 **发送单词图片**\n"
                        "系统自动 OCR，再进行整理并写入 GitHub。\n\n"
                        "**单词数量不限。图片或文字里有多少个有效单词，"
                        "就处理多少个。**\n\n"
                        "只有 GitHub push 成功后，才会报告录入成功。"
                    ),
                },
            },
            {
                "tag": "hr"
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content":
                            f"目标群：{TARGET_CHAT_NAME}",
                    }
                ],
            },
        ],
    }

    url = (
        f"{FEISHU_BASE}/open-apis/im/v1/messages"
    )

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type":
                "application/json; charset=utf-8",
        },
        params={
            "receive_id_type": "chat_id"
        },
        json={
            "receive_id": chat_id,
            "msg_type": "interactive",
            "content": json.dumps(
                card,
                ensure_ascii=False,
            ),
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    if data.get("code") != 0:
        raise RuntimeError(
            "连接卡片发送失败："
            + json.dumps(
                data,
                ensure_ascii=False,
            )[:2000]
        )

    log("连接成功卡片已发送。")


# ============================================================
# 图片下载
# ============================================================

def download_message_image(
    token,
    message_id,
    image_key,
    output_path,
):
    url = (
        f"{FEISHU_BASE}/open-apis/im/v1/messages/"
        f"{message_id}/resources/{image_key}"
    )

    response = requests.get(
        url,
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        params={
            "type": "image"
        },
        timeout=60,
    )

    response.raise_for_status()

    if not response.content:
        raise RuntimeError(
            "飞书图片下载结果为空。"
        )

    Path(output_path).write_bytes(
        response.content
    )

    log(
        "图片下载完成："
        f"{Path(output_path).stat().st_size:,} bytes"
    )


# ============================================================
# OCR
# ============================================================

def preprocess_image(image_path):
    with Image.open(image_path) as source:
        image = source.convert("RGB")

    log(
        f"原始图片尺寸："
        f"{image.width} × {image.height}"
    )

    max_side = 2600

    scale = min(
        2.0,
        max_side /
        max(image.width, image.height),
    )

    if scale > 1:
        image = image.resize(
            (
                int(image.width * scale),
                int(image.height * scale),
            )
        )

    image = image.convert("L")

    image = ImageEnhance.Contrast(
        image
    ).enhance(1.5)

    image = image.filter(
        ImageFilter.SHARPEN
    )

    return image


def run_ocr(image_path):
    log("开始执行 Tesseract OCR。")

    image = preprocess_image(
        image_path
    )

    text = pytesseract.image_to_string(
        image,
        lang="eng+chi_sim",
        config="--psm 6",
    )

    text = (
        text
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    log("OCR 执行完成。")

    log(
        "========== OCR 原始结果开始 =========="
    )

    print(
        text,
        flush=True,
    )

    log(
        "========== OCR 原始结果结束 =========="
    )

    if not text.strip():
        raise RuntimeError(
            "OCR 没有提取到可读文字。"
        )

    return text


# ============================================================
# 通用文字清洗
# ============================================================

def normalize_spaces(text):
    text = text.replace(
        "\u3000",
        " ",
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    return text.strip()


def clean_line(line):
    line = line.strip()

    # 去掉 OCR 常见的列表符号
    line = re.sub(
        r"^[|¦•·▪●○◆◇◎]+\s*",
        "",
        line,
    )

    # 去掉常见序号
    line = re.sub(
        r"^\s*\d+\s*[.)、．]\s*",
        "",
        line,
    )

    line = normalize_spaces(line)

    return line.strip()


# ============================================================
# 无用界面文字
# ============================================================

NOISE_PATTERNS = [
    r"^今日新词$",
    r"^今日新词[（(]\d+[）)]$",
    r"^今日复习$",
    r"^今日复习[（(]\d+[）)]$",
    r"^今日学习$",
    r"^今日学习[（(]\d+[）)]$",
    r"^学习单词$",
    r"^复习单词$",
    r"^今日单词$",
    r"^单词学习$",
    r"^单词复习$",
    r"^V$",
    r"^v$",
]


def is_noise_line(line):
    line = normalize_spaces(line)

    if not line:
        return True

    for pattern in NOISE_PATTERNS:
        if re.fullmatch(
            pattern,
            line,
            flags=re.IGNORECASE,
        ):
            return True

    return False


# ============================================================
# 中文判断
# ============================================================

def has_chinese(text):
    return bool(
        re.search(
            r"[\u4e00-\u9fff]",
            text,
        )
    )


def has_english(text):
    return bool(
        re.search(
            r"[A-Za-z]",
            text,
        )
    )


# ============================================================
# 英文单词判断
# ============================================================

def clean_english(text):
    text = text.strip()

    text = re.sub(
        r"^[^\wA-Za-z]+",
        "",
        text,
    )

    text = re.sub(
        r"[^A-Za-z0-9][^\w]*$",
        "",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def looks_like_english_word(line):
    """
    判断一行是否像一个真正的英文单词/短语。

    允许：
    - beautiful
    - grandparent
    - well
    - ice cream
    - mother-in-law
    - don't

    不允许：
    - 今日新词
    - 今日复习
    - n.
    - adj.
    - adv.
    - num.
    - 普通包含大量中文的行
    """

    line = clean_line(line)

    if not line:
        return False

    if is_noise_line(line):
        return False

    if has_chinese(line):
        return False

    # 词性不能作为单词
    if re.fullmatch(
        r"(n|v|adj|adv|prep|conj|pron|"
        r"vt|vi|aux|modal|num|art|det|"
        r"abbr)\.?",
        line,
        flags=re.IGNORECASE,
    ):
        return False

    # 常见界面文字
    if re.search(
        r"(今日|学习|复习|单词|词汇)",
        line,
    ):
        return False

    # 必须以英文字母开头
    if not re.match(
        r"^[A-Za-z]",
        line,
    ):
        return False

    # 允许的英文词条字符
    if not re.fullmatch(
        r"[A-Za-z][A-Za-z0-9'./\- ]*",
        line,
    ):
        return False

    letters = len(
        re.findall(
            r"[A-Za-z]",
            line,
        )
    )

    if letters < 1:
        return False

    # 过长的一整句话通常不是词条
    if len(line) > 80:
        return False

    return True


# ============================================================
# 中文释义清洗
# ============================================================

def clean_definition(text):
    text = text.strip()

    # 删除列表序号
    text = re.sub(
        r"^\s*\d+\s*[.)、．]\s*",
        "",
        text,
    )

    # 统一空格
    text = normalize_spaces(text)

    # 修复常见 OCR 分隔
    text = re.sub(
        r"\s*([；;：:，,。])\s*",
        r"\1",
        text,
    )

    text = re.sub(
        r"\s*([（）()])\s*",
        r"\1",
        text,
    )

    # 去掉行首多余符号
    text = re.sub(
        r"^[|¦•·▪●○◆◇◎]+\s*",
        "",
        text,
    )

    return text.strip(
        " \t-—–"
    )


# ============================================================
# 词性行判断
# ============================================================

POS_PATTERN = re.compile(
    r"^(?:"
    r"n|v|adj|adv|prep|conj|pron|"
    r"vt|vi|aux|modal|num|art|det|"
    r"abbr"
    r")\.?",
    re.IGNORECASE,
)


def looks_like_definition(line):
    if not line:
        return False

    if has_chinese(line):
        return True

    # 极少数软件会把词性单独放一行
    if POS_PATTERN.match(line):
        return True

    return False


# ============================================================
# 行内词条
# ============================================================

def parse_inline_pair(line):
    patterns = [
        r"^\s*(?:\d+[.)、．]\s*)?"
        r"([A-Za-z][A-Za-z0-9'./\- ]*?)"
        r"\s*[—–−-]\s*"
        r"(.+)$",

        r"^\s*(?:\d+[.)、．]\s*)?"
        r"([A-Za-z][A-Za-z0-9'./\- ]*?)"
        r"\s*[：:]\s*"
        r"(.+)$",
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

        definition = clean_definition(
            match.group(2)
        )

        if (
            looks_like_english_word(
                english
            )
            and definition
            and (
                has_chinese(definition)
                or POS_PATTERN.match(
                    definition
                )
            )
        ):
            return {
                "english": english,
                "chinese": definition,
            }

    return None


# ============================================================
# 主要词条解析器
# ============================================================

def parse_word_entries(raw_text):
    """
    核心规则：

    1. 不限制词条数量。
    2. 找到一个英文单词后，继续收集它下面的定义。
    3. 遇到下一个英文单词时结束当前词条。
    4. 自动跳过：
         今日新词
         今日复习
         数量
         软件 UI
    5. 图片 OCR 和直接粘贴文字共用。
    """

    raw_lines = (
        raw_text
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .split("\n")
    )

    lines = []

    for raw_line in raw_lines:
        line = clean_line(raw_line)

        if not line:
            continue

        if is_noise_line(line):
            continue

        lines.append(line)

    entries = []

    current_word = None
    current_definitions = []

    def flush_current():
        nonlocal current_word
        nonlocal current_definitions

        if not current_word:
            return

        definitions = []

        for definition in current_definitions:
            definition = clean_definition(
                definition
            )

            if not definition:
                continue

            definitions.append(
                definition
            )

        if definitions:
            entries.append(
                {
                    "english":
                        current_word,
                    "chinese":
                        "；".join(
                            definitions
                        ),
                }
            )

        current_word = None
        current_definitions = []

    for line in lines:

        # ----------------------------------------------------
        # 先判断是否为完整的：
        # word — definition
        # ----------------------------------------------------

        inline = parse_inline_pair(line)

        if inline:
            flush_current()

            entries.append(
                inline
            )

            continue

        # ----------------------------------------------------
        # 新英文单词
        # ----------------------------------------------------

        if looks_like_english_word(line):

            flush_current()

            current_word = clean_english(
                line
            )

            current_definitions = []

            continue

        # ----------------------------------------------------
        # 当前单词的释义
        # ----------------------------------------------------

        if current_word:

            if looks_like_definition(line):

                current_definitions.append(
                    clean_definition(line)
                )

                continue

            # 不认识的行：
            # 如果包含中文，也尽量保留为定义。
            if has_chinese(line):

                current_definitions.append(
                    clean_definition(line)
                )

                continue

    flush_current()

    return normalize_entries(
        entries
    )


# ============================================================
# 词条最终标准化
# ============================================================

def normalize_entries(entries):
    result = []
    index_by_word = {}

    for item in entries:

        english = clean_english(
            item.get(
                "english",
                "",
            )
        )

        chinese = clean_definition(
            item.get(
                "chinese",
                "",
            )
        )

        if not english:
            continue

        if not looks_like_english_word(
            english
        ):
            continue

        # 没有中文释义时暂时不写入。
        if not chinese or not has_chinese(
            chinese
        ):
            continue

        key = re.sub(
            r"\s+",
            " ",
            english,
        ).casefold()

        normalized = {
            "english": english,
            "chinese": chinese,
        }

        # 如果同一个词再次出现：
        # 后面的更完整内容覆盖前面的内容。
        if key in index_by_word:
            result[
                index_by_word[key]
            ] = normalized
        else:
            index_by_word[key] = len(
                result
            )
            result.append(
                normalized
            )

    return result


# ============================================================
# Markdown 解析
# ============================================================

def parse_existing_entries(text):
    """
    读取当天旧 MD。

    同时允许新词覆盖旧的错误 OCR 结果。
    """

    entries = []

    pattern = re.compile(
        r"^\s*\d+\.\s*"
        r"(.+?)"
        r"\s*[—–-]\s*"
        r"(.+?)"
        r"\s*$"
    )

    for line in text.splitlines():

        match = pattern.match(line)

        if not match:
            continue

        english = clean_english(
            match.group(1)
        )

        chinese = clean_definition(
            match.group(2)
        )

        if not english:
            continue

        if not chinese:
            continue

        # 只保留合理的英文词条
        if not looks_like_english_word(
            english
        ):
            continue

        entries.append(
            {
                "english": english,
                "chinese": chinese,
            }
        )

    return normalize_entries(
        entries
    )


# ============================================================
# Markdown 构建
# ============================================================

def utc_date_string():
    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d"
    )


def build_daily_markdown(
    date_string,
    new_entries,
):
    INPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        INPUT_DIR /
        f"{date_string}.md"
    )

    if output_path.exists():

        old_text = output_path.read_text(
            encoding="utf-8"
        )

        old_entries = parse_existing_entries(
            old_text
        )

        log(
            f"当天文件已存在，"
            f"读取有效词条："
            f"{len(old_entries)} 个"
        )

    else:

        old_text = ""
        old_entries = []

        log(
            "当天文件不存在，将创建新文件。"
        )

    # --------------------------------------------------------
    # 建立已有词典
    # --------------------------------------------------------

    merged = []
    index_by_word = {}

    for item in old_entries:

        key = re.sub(
            r"\s+",
            " ",
            item["english"],
        ).casefold()

        index_by_word[key] = len(
            merged
        )

        merged.append(item)

    added = []
    updated = []

    # --------------------------------------------------------
    # 新词条
    # --------------------------------------------------------

    for item in new_entries:

        key = re.sub(
            r"\s+",
            " ",
            item["english"],
        ).casefold()

        if key in index_by_word:

            old_item = merged[
                index_by_word[key]
            ]

            # 如果重新发送的内容不同，
            # 直接使用新内容覆盖。
            if (
                old_item["chinese"]
                != item["chinese"]
            ):
                merged[
                    index_by_word[key]
                ] = item

                updated.append(
                    item
                )

                log(
                    "更新当天已有词条："
                    f"{item['english']}"
                )

            else:

                log(
                    "跳过完全重复单词："
                    f"{item['english']}"
                )

        else:

            index_by_word[key] = len(
                merged
            )

            merged.append(item)
            added.append(item)

    # --------------------------------------------------------
    # 重新生成标准 Markdown
    # --------------------------------------------------------

    lines = [
        "# 今日新词",
        "",
    ]

    for index, item in enumerate(
        merged,
        start=1,
    ):
        lines.append(
            f"{index}. "
            f"{item['english']} — "
            f"{item['chinese']}"
        )

    lines.append("")

    new_text = "\n".join(lines)

    if new_text != old_text:

        output_path.write_text(
            new_text,
            encoding="utf-8",
        )

        log(
            f"Markdown 已写入："
            f"{output_path}"
        )

    else:

        log(
            "文件内容没有变化。"
        )

    return (
        output_path,
        merged,
        added,
        updated,
    )


# ============================================================
# Git
# ============================================================

def run_git(
    args,
    check=True,
):
    command = [
        "git"
    ] + list(args)

    log(
        "$ "
        + " ".join(command)
    )

    result = subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if result.stdout:
        print(
            result.stdout,
            flush=True,
        )

    if (
        check
        and result.returncode != 0
    ):
        raise RuntimeError(
            "Git 命令失败："
            f"{' '.join(command)}"
        )

    return result


def git_commit_and_push(
    output_path
):
    if not GITHUB_REPOSITORY:
        raise RuntimeError(
            "缺少 GITHUB_REPOSITORY。"
        )

    branch = GITHUB_REF_NAME

    if not branch:
        raise RuntimeError(
            "缺少 GITHUB_REF_NAME。"
        )

    relative_path = (
        output_path
        .relative_to(REPO_ROOT)
        .as_posix()
    )

    run_git([
        "config",
        "user.name",
        "github-actions[bot]",
    ])

    run_git([
        "config",
        "user.email",
        "41898282+github-actions[bot]"
        "@users.noreply.github.com",
    ])

    run_git([
        "add",
        "--",
        relative_path,
    ])

    staged = run_git(
        [
            "diff",
            "--cached",
            "--quiet",
        ],
        check=False,
    )

    if staged.returncode == 0:

        log(
            "没有新的 Git 变更。"
        )

        return False

    if staged.returncode != 1:
        raise RuntimeError(
            "无法检查 Git 暂存区。"
        )

    run_git([
        "commit",
        "-m",
        f"Update daily English vocabulary "
        f"{output_path.stem}",
    ])

    last_error = None

    for attempt in range(1, 4):

        log(
            f"准备推送 GitHub："
            f"第 {attempt}/3 次"
        )

        pull = run_git(
            [
                "pull",
                "--rebase",
                "origin",
                branch,
            ],
            check=False,
        )

        if pull.returncode != 0:

            run_git(
                [
                    "rebase",
                    "--abort",
                ],
                check=False,
            )

            last_error = (
                "git pull --rebase 失败。"
            )

            break

        push = run_git(
            [
                "push",
                "origin",
                f"HEAD:{branch}",
            ],
            check=False,
        )

        if push.returncode == 0:

            log(
                "GitHub push 成功。"
            )

            return True

        last_error = (
            "git push 失败。"
        )

    raise RuntimeError(
        (
            last_error
            or "GitHub 推送失败。"
        )
        + "请检查 Actions 的 "
        "contents: write 权限、"
        "分支保护和并发提交。"
    )


# ============================================================
# SDK 消息字段
# ============================================================

def get_message_field(
    message,
    field,
    default=None,
):
    try:

        value = getattr(
            message,
            field,
        )

        if value is None:
            return default

        return value

    except Exception:

        return default


# ============================================================
# 从飞书 text message 获取文字
# ============================================================

def extract_text_message(content):
    """
    飞书 text 消息 content 通常是：

    {
        "text": "..."
    }

    兼容部分异常情况。
    """

    if not content:
        return ""

    try:

        data = json.loads(
            content
        )

        if isinstance(
            data,
            dict,
        ):
            text = data.get(
                "text",
                "",
            )

            if text:
                return str(text)

    except Exception:

        pass

    return str(content)


# ============================================================
# 统一处理：文字
# ============================================================

def process_text_message(
    event_data,
    target_chat_id,
):
    event = getattr(
        event_data,
        "event",
        None,
    )

    message = (
        getattr(
            event,
            "message",
            None,
        )
        if event
        else None
    )

    if message is None:
        log(
            "文字事件没有 event.message。"
        )
        return

    message_id = get_message_field(
        message,
        "message_id",
        "",
    )

    chat_id = get_message_field(
        message,
        "chat_id",
        "",
    )

    content = get_message_field(
        message,
        "content",
        "{}",
    )

    log("=" * 65)
    log(
        f"收到文字消息："
        f"message_id={message_id}"
    )
    log(
        f"message_type=text, "
        f"chat_id={chat_id}"
    )
    log("=" * 65)

    if not message_id:
        log(
            "文字消息没有 message_id。"
        )
        return

    if (
        chat_id
        and target_chat_id
        and chat_id != target_chat_id
    ):
        log(
            "文字消息来自非目标群，忽略。"
        )
        return

    with _message_lock:

        if message_id in (
            _processed_message_ids
        ):
            log(
                "检测到重复文字消息，跳过。"
            )
            return

        if message_id in (
            _processing_message_ids
        ):
            log(
                "该文字消息正在处理中。"
            )
            return

        _processing_message_ids.add(
            message_id
        )

    notify(
        message_id,
        target_chat_id,
        "📝 已收到单词文字，正在整理单词、词性和中文释义，请稍候……",
    )

    try:

        raw_text = extract_text_message(
            content
        )

        log(
            "========== 飞书原始文字开始 =========="
        )

        print(
            raw_text,
            flush=True,
        )

        log(
            "========== 飞书原始文字结束 =========="
        )

        if not raw_text.strip():
            raise RuntimeError(
                "收到的文字为空。"
            )

        entries = parse_word_entries(
            raw_text
        )

        log(
            f"文字整理完成："
            f"识别到 {len(entries)} 个词条。"
        )

        if not entries:
            raise RuntimeError(
                "没有识别出可靠的英文词条。"
                "请直接粘贴包含英文单词和中文释义的内容。"
            )

        date_string = utc_date_string()

        (
            output_path,
            merged,
            added,
            updated,
        ) = build_daily_markdown(
            date_string,
            entries,
        )

        # ----------------------------------------------------
        # 没有新增、没有更新
        # ----------------------------------------------------

        if (
            not added
            and not updated
        ):

            notify(
                message_id,
                target_chat_id,
                f"ℹ️ 文字整理完成。\n\n"
                f"本次识别：{len(entries)} 个单词\n"
                f"当天累计：{len(merged)} 个单词\n"
                f"没有新增或修改内容，因此没有产生 GitHub 提交。",
            )

            _processed_message_ids.add(
                message_id
            )

            return

        # ----------------------------------------------------
        # GitHub
        # ----------------------------------------------------

        log(
            "开始提交并推送 GitHub。"
        )

        git_commit_and_push(
            output_path
        )

        # ----------------------------------------------------
        # 成功消息
        # ----------------------------------------------------

        result_lines = []

        for item in added:

            result_lines.append(
                f"+ {item['english']} — "
                f"{item['chinese']}"
            )

        for item in updated:

            result_lines.append(
                f"↻ {item['english']} — "
                f"{item['chinese']}"
            )

        preview = "\n".join(
            result_lines
        )

        success_text = (
            "✅ 单词文字已整理并成功推送到 GitHub！\n\n"
            f"日期：{date_string}（UTC）\n"
            f"文件：`02_英语学习系统/input/{date_string}.md`\n"
            f"本次识别：{len(entries)} 个单词\n"
            f"新增：{len(added)} 个\n"
            f"更新：{len(updated)} 个\n"
            f"当天累计：{len(merged)} 个\n\n"
            f"本次处理：\n{preview}\n\n"
            "现在可以启动英语学习系统学习今天的单词了。"
        )

        notify(
            message_id,
            target_chat_id,
            success_text,
        )

        _processed_message_ids.add(
            message_id
        )

    except Exception as exc:

        log(
            f"文字处理失败："
            f"{type(exc).__name__}: {exc}"
        )

        notify(
            message_id,
            target_chat_id,
            "❌ 单词文字处理未完成。\n\n"
            f"原因：{type(exc).__name__}: {exc}\n\n"
            "系统没有报告本次录入成功。",
        )

    finally:

        with _message_lock:
            _processing_message_ids.discard(
                message_id
            )


# ============================================================
# 统一处理：图片
# ============================================================

def process_image_message(
    event_data,
    target_chat_id,
):
    event = getattr(
        event_data,
        "event",
        None,
    )

    message = (
        getattr(
            event,
            "message",
            None,
        )
        if event
        else None
    )

    if message is None:
        log(
            "图片事件没有 event.message。"
        )
        return

    message_id = get_message_field(
        message,
        "message_id",
        "",
    )

    message_type = get_message_field(
        message,
        "message_type",
        "",
    )

    chat_id = get_message_field(
        message,
        "chat_id",
        "",
    )

    content = get_message_field(
        message,
        "content",
        "{}",
    )

    log("=" * 65)
    log(
        f"收到图片消息："
        f"message_id={message_id}"
    )
    log(
        f"message_type={message_type}, "
        f"chat_id={chat_id}"
    )
    log("=" * 65)

    if not message_id:
        return

    if (
        chat_id
        and target_chat_id
        and chat_id != target_chat_id
    ):
        log(
            "图片来自非目标群，忽略。"
        )
        return

    with _message_lock:

        if message_id in (
            _processed_message_ids
        ):
            log(
                "检测到重复图片消息，跳过。"
            )
            return

        if message_id in (
            _processing_message_ids
        ):
            log(
                "该图片正在处理中。"
            )
            return

        _processing_message_ids.add(
            message_id
        )

    notify(
        message_id,
        target_chat_id,
        "📷 已收到单词图片，正在 OCR 识别并整理，请稍候……",
    )

    try:

        try:

            content_data = json.loads(
                content or "{}"
            )

        except Exception as exc:

            raise RuntimeError(
                "图片消息 content "
                f"不是有效 JSON：{exc}"
            )

        image_key = content_data.get(
            "image_key"
        )

        if not image_key:
            raise RuntimeError(
                "图片消息中没有 image_key。"
            )

        token = get_tenant_access_token()

        with tempfile.TemporaryDirectory(
            prefix="748686_word_"
        ) as temp_dir:

            image_path = (
                Path(temp_dir)
                / "word_image.png"
            )

            download_message_image(
                token=token,
                message_id=message_id,
                image_key=image_key,
                output_path=image_path,
            )

            # --------------------------------------------
            # OCR
            # --------------------------------------------

            raw_text = run_ocr(
                image_path
            )

            # --------------------------------------------
            # OCR 后进入和文字完全相同的解析器
            # --------------------------------------------

            entries = parse_word_entries(
                raw_text
            )

            log(
                f"OCR 整理完成："
                f"识别到 {len(entries)} 个词条。"
            )

            if not entries:
                raise RuntimeError(
                    "图片 OCR 没有识别出可靠的英文词条。"
                    "没有写入 GitHub。"
                )

            date_string = utc_date_string()

            (
                output_path,
                merged,
                added,
                updated,
            ) = build_daily_markdown(
                date_string,
                entries,
            )

            if (
                not added
                and not updated
            ):

                notify(
                    message_id,
                    target_chat_id,
                    f"ℹ️ 图片 OCR 整理完成。\n\n"
                    f"本次识别：{len(entries)} 个单词\n"
                    f"当天累计：{len(merged)} 个单词\n"
                    "全部已经存在，没有产生新的 GitHub 提交。",
                )

                _processed_message_ids.add(
                    message_id
                )

                return

            # --------------------------------------------
            # GitHub
            # --------------------------------------------

            log(
                "开始提交并推送 GitHub。"
            )

            git_commit_and_push(
                output_path
            )

            result_lines = []

            for item in added:

                result_lines.append(
                    f"+ {item['english']} — "
                    f"{item['chinese']}"
                )

            for item in updated:

                result_lines.append(
                    f"↻ {item['english']} — "
                    f"{item['chinese']}"
                )

            preview = "\n".join(
                result_lines
            )

            success_text = (
                "✅ 单词图片已识别、整理并成功推送到 GitHub！\n\n"
                f"日期：{date_string}（UTC）\n"
                f"文件：`02_英语学习系统/input/{date_string}.md`\n"
                f"本次识别：{len(entries)} 个单词\n"
                f"新增：{len(added)} 个\n"
                f"更新：{len(updated)} 个\n"
                f"当天累计：{len(merged)} 个\n\n"
                f"本次处理：\n{preview}\n\n"
                "现在可以启动英语学习系统学习今天的单词了。"
            )

            notify(
                message_id,
                target_chat_id,
                success_text,
            )

            _processed_message_ids.add(
                message_id
            )

    except Exception as exc:

        log(
            f"图片处理失败："
            f"{type(exc).__name__}: {exc}"
        )

        notify(
            message_id,
            target_chat_id,
            "❌ 图片处理未完成。\n\n"
            f"原因：{type(exc).__name__}: {exc}\n\n"
            "系统没有报告本次录入成功。",
        )

    finally:

        with _message_lock:
            _processing_message_ids.discard(
                message_id
            )


# ============================================================
# 飞书事件回调
# ============================================================

def make_handler(target_chat_id):

    def handle_message(data):

        try:

            event = getattr(
                data,
                "event",
                None,
            )

            message = (
                getattr(
                    event,
                    "message",
                    None,
                )
                if event
                else None
            )

            if message is None:

                log(
                    "收到消息事件，但没有 message。"
                )

                return

            message_type = get_message_field(
                message,
                "message_type",
                "",
            )

            log(
                "收到消息事件："
                f"message_type={message_type}"
            )

            # --------------------------------------------
            # 文字
            # --------------------------------------------

            if message_type == "text":

                process_text_message(
                    data,
                    target_chat_id,
                )

                return

            # --------------------------------------------
            # 图片
            # --------------------------------------------

            if message_type == "image":

                process_image_message(
                    data,
                    target_chat_id,
                )

                return

            # --------------------------------------------
            # 其他
            # --------------------------------------------

            log(
                f"收到暂不处理的消息类型："
                f"{message_type}"
            )

        except Exception as exc:

            log(
                f"事件回调异常："
                f"{type(exc).__name__}: {exc}"
            )

    return handle_message


# ============================================================
# 主程序
# ============================================================

def main():

    log("=" * 65)
    log(
        "748686 飞书新学单词机器人 V3.0"
    )
    log(
        "模式："
        "文字/图片 -> 整理 -> 日期 MD -> GitHub push"
    )
    log(
        "支持：直接粘贴文字 + 图片 OCR"
    )
    log(
        "单词数量：动态，不设固定数量"
    )
    log(
        f"目标群：{TARGET_CHAT_NAME}"
    )
    log(
        f"仓库根目录：{REPO_ROOT}"
    )
    log(
        f"输入目录：{INPUT_DIR}"
    )
    log(
        f"GitHub 仓库："
        f"{GITHUB_REPOSITORY or '(未设置)'}"
    )
    log(
        f"GitHub 分支："
        f"{GITHUB_REF_NAME or '(未设置)'}"
    )
    log("=" * 65)

    if not GITHUB_REPOSITORY:

        raise RuntimeError(
            "GITHUB_REPOSITORY 未设置。"
            "请从 GitHub Actions 工作流运行。"
        )

    if not GITHUB_REF_NAME:

        raise RuntimeError(
            "GITHUB_REF_NAME 未设置。"
            "请从仓库分支手动启动工作流。"
        )

    token = get_tenant_access_token()

    log(
        "tenant_access_token 获取成功。"
    )

    target_chat_id = find_target_chat(
        token
    )

    send_connection_card(
        token,
        target_chat_id,
    )

    # --------------------------------------------------------
    # 保留已经验证能够工作的 WebSocket 机制
    # --------------------------------------------------------

    event_handler = (
        lark.EventDispatcherHandler
        .builder(
            "",
            "",
            lark.LogLevel.INFO,
        )
        .register_p2_im_message_receive_v1(
            make_handler(
                target_chat_id
            )
        )
        .build()
    )

    ws_client = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        log_level=lark.LogLevel.INFO,
        event_handler=event_handler,
        auto_reconnect=True,
    )

    log(
        "🟢 准备启动飞书 WebSocket 长连接。"
    )

    log(
        "现在支持："
        "文字消息 + 图片消息"
    )

    log(
        "文字：直接粘贴背单词软件内容即可。"
    )

    log(
        "图片：发送截图即可自动 OCR。"
    )

    log(
        "单词数量不限。"
    )

    ws_client.start()


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        log(
            "机器人收到停止信号。"
        )

    except Exception as exc:

        log(
            f"程序启动失败："
            f"{type(exc).__name__}: {exc}"
        )

        sys.exit(1)
