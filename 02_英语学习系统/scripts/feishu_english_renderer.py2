#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu English Renderer V2.1

职责：
1. 读取指定日期的英语学习输出
2. 读取文章
3. 读取配图
4. 读取试卷
5. 读取答案与解析
6. 读取听力文件
7. 使用 APP_ID / APP_SECRET 上传图片
8. 使用 FEISHU_WEBHOOK 发送卡片
9. 与 748686 自生长知识系统使用同一个飞书群入口

V2.1 升级：
------------------------------------------------------------
重点升级 Article Card：

1. 英语文章独立展示
2. 中文翻译独立展示
3. 重点单词独立展示
4. 重点短语独立展示
5. 语法难点独立展示
6. 学习提示独立展示
7. 自动识别文章中的 **重点单词**
8. 重点词在正文中使用深蓝色高亮
9. 重点词汇使用浅蓝色视觉卡片
10. 文章按段落展示，不再一次性压缩成一大段
11. 自动识别多种 Markdown 标题格式
12. 保留文章配图
13. 保留 GitHub 原文按钮
14. 不修改 main.py
15. 不修改 exam_generate.py
16. 不修改 exam_answers.py
17. 不修改 knowledge_image.py
18. 不修改 audio_generate.py

原则：
------------------------------------------------------------
本程序只负责 Feishu 展示层。
不修改英语学习系统原始输出。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import requests


# ============================================================
# Feishu
# ============================================================

FEISHU_BASE = "https://open.feishu.cn"

TOKEN_URL = (
    f"{FEISHU_BASE}/open-apis/auth/v3/"
    "tenant_access_token/internal"
)

IMAGE_UPLOAD_URL = (
    f"{FEISHU_BASE}/open-apis/im/v1/images"
)


# ============================================================
# 工具
# ============================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_exists(path: Path) -> bool:
    return path.is_file()


def compact(text: str, max_length: int = 900) -> str:

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    text = text.strip()

    if len(text) <= max_length:
        return text

    return (
        text[:max_length].rstrip()
        + "\n..."
    )


def markdown_title(text: str) -> str:

    match = re.search(
        r"^#\s+(.+)$",
        text,
        re.MULTILINE,
    )

    if match:

        title = match.group(1).strip()

        title = title.replace(
            "｜答案与解析",
            "",
        )

        title = title.replace(
            "｜答案",
            "",
        )

        title = title.replace(
            "｜试卷",
            "",
        )

        title = title.replace(
            "｜文章",
            "",
        )

        return title.strip()

    return "English Learning"


def extract_meta(
    text: str,
    key: str,
) -> str:

    patterns = {

        "difficulty": [
            r"难度：([^｜\n]+)",
            r"难度：([^\n]+)",
        ],

        "level": [
            r"级别：([^｜\n]+)",
            r"(小学[^\n]+年级)",
        ],

        "article_type": [
            r"文章类型：([^｜\n]+)",
            r"文体：([^｜\n]+)",
        ],

        "score": [
            r"总分：([^\n]+)",
        ],
    }

    for pattern in patterns.get(
        key,
        [],
    ):

        match = re.search(
            pattern,
            text,
        )

        if match and match.lastindex:

            return match.group(1).strip()

    return ""


# ============================================================
# GitHub 文件链接
# ============================================================

def github_file_url(
    path: Path,
) -> str | None:

    server = os.getenv(
        "GITHUB_SERVER_URL",
        "https://github.com",
    ).rstrip("/")

    repository = os.getenv(
        "GITHUB_REPOSITORY",
        "",
    ).strip()

    ref = os.getenv(
        "GITHUB_REF_NAME",
        "main",
    ).strip()

    if not repository:
        return None

    try:

        relative = path.resolve().relative_to(
            Path.cwd().resolve()
        )

    except ValueError:

        return None

    relative_url = "/".join(
        part.replace(" ", "%20")
        for part in relative.parts
    )

    return (
        f"{server}/{repository}/blob/"
        f"{ref}/{relative_url}"
    )


# ============================================================
# Feishu Client
# ============================================================

class FeishuClient:

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        webhook: str,
    ):

        self.app_id = app_id
        self.app_secret = app_secret
        self.webhook = webhook

        self.session = requests.Session()

        self._token: str | None = None

    # --------------------------------------------------------
    # Tenant Access Token
    # --------------------------------------------------------

    def tenant_access_token(self) -> str:

        if self._token:
            return self._token

        response = self.session.post(
            TOKEN_URL,
            json={
                "app_id": self.app_id,
                "app_secret": self.app_secret,
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:

            fail(
                "获取 Feishu tenant_access_token 失败："
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )

        token = data.get(
            "tenant_access_token"
        )

        if not token:

            fail(
                "Feishu 返回结果中没有 "
                "tenant_access_token"
            )

        self._token = token

        return token

    def auth_headers(self) -> dict[str, str]:

        return {
            "Authorization": (
                f"Bearer "
                f"{self.tenant_access_token()}"
            ),
            "Content-Type": "application/json",
        }

    # --------------------------------------------------------
    # 上传图片
    # --------------------------------------------------------

    def upload_image(
        self,
        path: Path,
    ) -> str:

        log(
            f"   ↑ 上传图片：{path.name}"
        )

        with path.open("rb") as fp:

            response = self.session.post(
                IMAGE_UPLOAD_URL,
                headers={
                    "Authorization": (
                        f"Bearer "
                        f"{self.tenant_access_token()}"
                    )
                },
                data={
                    "image_type": "message",
                },
                files={
                    "image": (
                        path.name,
                        fp,
                        "image/png",
                    )
                },
                timeout=120,
            )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:

            fail(
                "上传 Feishu 图片失败："
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )

        image_key = (
            data
            .get("data", {})
            .get("image_key")
        )

        if not image_key:

            fail(
                "Feishu 图片上传成功，"
                "但没有返回 image_key"
            )

        log(
            f"   ✓ image_key: {image_key}"
        )

        return image_key

    # --------------------------------------------------------
    # Webhook
    # --------------------------------------------------------

    def send_card(
        self,
        card: dict[str, Any],
    ) -> dict[str, Any]:

        payload = {
            "msg_type": "interactive",
            "card": card,
        }

        response = self.session.post(
            self.webhook,
            headers={
                "Content-Type": (
                    "application/json; charset=utf-8"
                )
            },
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:

            fail(
                "Feishu Webhook 发送卡片失败："
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )

        return data


# ============================================================
# Markdown / 内容
# ============================================================

def count_questions(
    exam_text: str,
) -> dict[str, int]:

    sections = {
        "听力": 0,
        "单项选择": 0,
        "多项选择": 0,
        "多选题": 0,
        "完形填空": 0,
        "阅读理解": 0,
        "翻译": 0,
        "写作": 0,
    }

    section_patterns = {

        "听力": [
            r"听力",
        ],

        "单项选择": [
            r"单项选择",
        ],

        "多项选择": [
            r"多项选择",
            r"多选题",
        ],

        "完形填空": [
            r"完形填空",
        ],

        "阅读理解": [
            r"阅读理解",
        ],

        "翻译": [
            r"翻译",
        ],

        "写作": [
            r"写作",
        ],
    }

    # --------------------------------------------------------
    # 听力
    # --------------------------------------------------------

    listening_match = re.search(
        r"(?:^|\n)#{1,6}\s*[^#\n]*听力[^#\n]*\n"
        r"([\s\S]*?)"
        r"(?=\n#{1,6}\s|\Z)",
        exam_text,
        re.MULTILINE,
    )

    if listening_match:

        listening_body = (
            listening_match.group(1)
        )

        part_counts = []

        for part in ("A", "B", "C"):

            part_match = re.search(
                rf"Part\s*{part}"
                rf"[\s\S]*?"
                rf"(?=Part\s*[ABC]|\Z)",
                listening_body,
                re.IGNORECASE,
            )

            if not part_match:
                continue

            numbers = re.findall(
                r"^###?\s*(\d+)\.",
                part_match.group(0),
                re.MULTILINE,
            )

            if not numbers:

                numbers = re.findall(
                    r"^\s*(\d+)[\.\、]",
                    part_match.group(0),
                    re.MULTILINE,
                )

            if numbers:
                part_counts.append(
                    len(numbers)
                )

        sections["听力"] = sum(
            part_counts
        )

    # --------------------------------------------------------
    # 普通章节
    # --------------------------------------------------------

    for section, patterns in section_patterns.items():

        if section == "听力":
            continue

        body = None

        for section_pattern in patterns:

            match = re.search(
                rf"(?:^|\n)#{1,6}\s*"
                rf"[^#\n]*{section_pattern}"
                rf"[^#\n]*\n"
                rf"([\s\S]*?)"
                rf"(?=\n#{1,6}\s|\Z)",
                exam_text,
                re.IGNORECASE,
            )

            if match:

                body = match.group(1)

                break

        if not body:
            continue

        numbers = re.findall(
            r"^###?\s*(\d+)\.",
            body,
            re.MULTILINE,
        )

        if not numbers:

            numbers = re.findall(
                r"^\s*(\d+)[\.\、]",
                body,
                re.MULTILINE,
            )

        if numbers:

            sections[section] = len(
                numbers
            )

    if sections["多项选择"] == 0:

        sections["多项选择"] = (
            sections["多选题"]
        )

    del sections["多选题"]

    return sections


def extract_article_body(
    article_text: str,
) -> str:

    text = article_text.strip()

    if text.startswith("---"):

        parts = text.split(
            "---",
            2,
        )

        if len(parts) == 3:

            text = parts[2].strip()

    text = re.sub(
        r"^#\s+.+$\n?",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    return text.strip()


# ============================================================
# Article V2.1 Parser
# ============================================================

def normalize_section_name(
    heading: str,
) -> str:

    value = heading.strip()

    value = re.sub(
        r"^[#\s]+",
        "",
        value,
    )

    value = re.sub(
        r"[：:]+$",
        "",
        value,
    )

    lower = value.lower()

    # English
    if (
        lower in {
            "english",
            "english article",
            "article",
            "英文",
            "英文原文",
            "英语原文",
            "英语文章",
        }
    ):
        return "english"

    # Translation
    if (
        "中文翻译" in value
        or "中文译文" in value
        or "翻译" == value
        or "translation" in lower
        or lower == "chinese"
    ):
        return "translation"

    # Vocabulary
    if (
        "重点词汇" in value
        or "重点单词" in value
        or "核心词汇" in value
        or "核心单词" in value
        or "词汇" == value
        or "vocabulary" in lower
        or "vocab" in lower
    ):
        return "vocabulary"

    # Phrases
    if (
        "重点短语" in value
        or "核心短语" in value
        or "短语" == value
        or "phrase" in lower
    ):
        return "phrases"

    # Grammar
    if (
        "语法难点" in value
        or "语法重点" in value
        or "语法解析" in value
        or "grammar" in lower
    ):
        return "grammar"

    # Learning
    if (
        "学习建议" in value
        or "学习提示" in value
        or "学习要点" in value
        or "learning notes" in lower
        or "learning tips" in lower
        or "notes" == lower
    ):
        return "notes"

    return "other"


def split_markdown_sections(
    text: str,
) -> dict[str, str]:

    sections: dict[str, list[str]] = {
        "english": [],
        "translation": [],
        "vocabulary": [],
        "phrases": [],
        "grammar": [],
        "notes": [],
        "other": [],
    }

    current = "english"

    for line in text.splitlines():

        heading = re.match(
            r"^\s{0,3}(#{2,6})\s+(.+?)\s*$",
            line,
        )

        if heading:

            name = normalize_section_name(
                heading.group(2)
            )

            current = name

            continue

        sections[current].append(
            line
        )

    return {
        key: "\n".join(value).strip()
        for key, value in sections.items()
    }


def clean_markdown(
    text: str,
) -> str:

    text = text.strip()

    # 删除 HTML span，但保留里面的文字
    text = re.sub(
        r"<span[^>]*>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"</span>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # 图片
    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text,
    )

    return text.strip()


def extract_highlight_words(
    text: str,
) -> list[str]:

    words: list[str] = []

    # **word**
    for match in re.findall(
        r"\*\*([^*\n]+?)\*\*",
        text,
    ):

        value = match.strip()

        if not value:
            continue

        if len(value) > 80:
            continue

        if value not in words:
            words.append(value)

    # __word__
    for match in re.findall(
        r"__([^_\n]+?)__",
        text,
    ):

        value = match.strip()

        if not value:
            continue

        if len(value) > 80:
            continue

        if value not in words:
            words.append(value)

    return words


def extract_vocabulary_items(
    text: str,
) -> list[dict[str, str]]:

    items: list[dict[str, str]] = []

    if not text:
        return items

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines:

        line = re.sub(
            r"^[-*•]\s*",
            "",
            line,
        )

        line = re.sub(
            r"^\d+[.)、]\s*",
            "",
            line,
        )

        # word — meaning
        match = re.match(
            r"^\*\*(.+?)\*\*\s*"
            r"(?:[-—:：]\s*)"
            r"(.+)$",
            line,
        )

        if match:

            items.append(
                {
                    "word": match.group(1).strip(),
                    "meaning": match.group(2).strip(),
                }
            )

            continue

        # word：meaning
        match = re.match(
            r"^([A-Za-z][A-Za-z0-9' -]{1,60})"
            r"\s*[：:]\s*(.+)$",
            line,
        )

        if match:

            items.append(
                {
                    "word": match.group(1).strip(),
                    "meaning": match.group(2).strip(),
                }
            )

            continue

        # word - meaning
        match = re.match(
            r"^([A-Za-z][A-Za-z0-9' -]{1,60})"
            r"\s+[-—]\s+(.+)$",
            line,
        )

        if match:

            items.append(
                {
                    "word": match.group(1).strip(),
                    "meaning": match.group(2).strip(),
                }
            )

    return items


def paragraph_list(
    text: str,
) -> list[str]:

    text = clean_markdown(text)

    paragraphs = re.split(
        r"\n\s*\n+",
        text,
    )

    result = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        result.append(
            paragraph
        )

    return result


# ============================================================
# Feishu Article Formatting
# ============================================================

def escape_lark_text(
    text: str,
) -> str:

    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def highlight_markdown_words(
    text: str,
    highlight_words: list[str],
) -> str:

    if not highlight_words:
        return text

    # 先保护 Markdown 粗体
    placeholders: dict[str, str] = {}

    def protect(
        match: re.Match,
    ) -> str:

        key = (
            f"__HL_{len(placeholders)}__"
        )

        placeholders[key] = match.group(0)

        return key

    protected = re.sub(
        r"\*\*[^*\n]+?\*\*",
        protect,
        text,
    )

    # 按长度倒序，避免短词先匹配
    for word in sorted(
        highlight_words,
        key=len,
        reverse=True,
    ):

        word = word.strip()

        if not word:
            continue

        escaped_word = re.escape(
            word
        )

        protected = re.sub(
            rf"(?<![\w])"
            rf"({escaped_word})"
            rf"(?![\w])",
            (
                r"<font color='#0B3B82'>"
                r"<b>\1</b>"
                r"</font>"
            ),
            protected,
            flags=re.IGNORECASE,
        )

    # 恢复 Markdown 粗体
    for key, value in placeholders.items():

        protected = protected.replace(
            key,
            value,
        )

    # 对原始 **word** 再进行颜色处理
    def bold_replacer(
        match: re.Match,
    ) -> str:

        word = match.group(1)

        return (
            "<font color='#0B3B82'>"
            f"<b>{word}</b>"
            "</font>"
        )

    protected = re.sub(
        r"\*\*([^*\n]+?)\*\*",
        bold_replacer,
        protected,
    )

    return protected


def make_article_paragraph(
    text: str,
    highlight_words: list[str],
) -> dict[str, Any]:

    content = highlight_markdown_words(
        text,
        highlight_words,
    )

    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": content,
        },
    }


def make_section_title(
    icon: str,
    title: str,
    subtitle: str = "",
) -> dict[str, Any]:

    content = (
        f"**{icon} {title}**"
    )

    if subtitle:
        content += (
            f"\n{subtitle}"
        )

    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": content,
        },
    }


def make_highlight_word_card(
    words: list[str],
) -> dict[str, Any] | None:

    if not words:
        return None

    display = []

    for word in words[:20]:

        display.append(
            f"🔹 **{word}**"
        )

    content = (
        "**🔵 今日重点表达**\n\n"
        + "　　".join(display)
    )

    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": content,
        },
    }


def make_vocabulary_card(
    vocabulary: list[dict[str, str]],
) -> dict[str, Any] | None:

    if not vocabulary:
        return None

    lines = [
        "**🔵 重点词汇**",
        "",
    ]

    for item in vocabulary[:15]:

        word = item.get(
            "word",
            "",
        ).strip()

        meaning = item.get(
            "meaning",
            "",
        ).strip()

        if not word:
            continue

        if meaning:

            lines.append(
                f"**{word}**　"
                f"{meaning}"
            )

        else:

            lines.append(
                f"**{word}**"
            )

    if len(lines) <= 2:
        return None

    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": "\n".join(lines),
        },
    }


def make_text_section(
    icon: str,
    title: str,
    text: str,
) -> list[dict[str, Any]]:

    elements: list[dict[str, Any]] = []

    if not text:
        return elements

    elements.append(
        make_section_title(
            icon,
            title,
        )
    )

    elements.append(
        {
            "tag": "hr",
        }
    )

    paragraphs = paragraph_list(
        text
    )

    for paragraph in paragraphs:

        elements.append(
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": paragraph,
                },
            }
        )

    return elements


# ============================================================
# Article Card V2.1
# ============================================================

def make_article_card(
    title: str,
    article_body: str,
    image_key: str | None,
    difficulty: str,
    article_type: str,
    article_url: str | None,
) -> dict[str, Any]:

    # --------------------------------------------------------
    # 解析文章结构
    # --------------------------------------------------------

    sections = split_markdown_sections(
        article_body
    )

    english = sections.get(
        "english",
        "",
    )

    translation = sections.get(
        "translation",
        "",
    )

    vocabulary_text = sections.get(
        "vocabulary",
        "",
    )

    phrases = sections.get(
        "phrases",
        "",
    )

    grammar = sections.get(
        "grammar",
        "",
    )

    notes = sections.get(
        "notes",
        "",
    )

    # --------------------------------------------------------
    # 如果没有明确 English 标题
    # 就把原始正文作为英文正文
    # --------------------------------------------------------

    if not english:

        english = article_body

    # --------------------------------------------------------
    # 自动识别重点词
    #
    # 来源：
    # 1. English 中的 **word**
    # 2. Vocabulary 中的 **word**
    # --------------------------------------------------------

    highlight_words = extract_highlight_words(
        english
    )

    vocabulary_items = extract_vocabulary_items(
        vocabulary_text
    )

    for item in vocabulary_items:

        word = item.get(
            "word",
            "",
        ).strip()

        if word and word not in highlight_words:

            highlight_words.append(
                word
            )

    # --------------------------------------------------------
    # 卡片元素
    # --------------------------------------------------------

    elements: list[dict[str, Any]] = []

    # --------------------------------------------------------
    # 1. 顶部文章配图
    # --------------------------------------------------------

    if image_key:

        elements.append(
            {
                "tag": "img",
                "img_key": image_key,
                "alt": {
                    "tag": "plain_text",
                    "content": title,
                },
                "mode": "fit_horizontal",
            }
        )

    # --------------------------------------------------------
    # 2. 文章标题区
    # --------------------------------------------------------

    meta_line = (
        f"⭐ {difficulty or '—'}"
        f"　·　"
        f"📖 {article_type or '—'}"
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"# {title}\n\n"
                    f"{meta_line}\n\n"
                    "✨ **English Reading · "
                    "精读学习**"
                ),
            },
        }
    )

    elements.append(
        {
            "tag": "hr",
        }
    )

    # --------------------------------------------------------
    # 3. 英文原文
    # --------------------------------------------------------

    elements.append(
        make_section_title(
            "🇬🇧",
            "English Article",
            "英文原文",
        )
    )

    elements.append(
        {
            "tag": "hr",
        }
    )

    english_paragraphs = paragraph_list(
        english
    )

    for paragraph in english_paragraphs:

        elements.append(
            make_article_paragraph(
                paragraph,
                highlight_words,
            )
        )

    # --------------------------------------------------------
    # 4. 今日重点词
    # --------------------------------------------------------

    highlight_card = (
        make_highlight_word_card(
            highlight_words
        )
    )

    if highlight_card:

        elements.append(
            {
                "tag": "hr",
            }
        )

        elements.append(
            highlight_card
        )

    # --------------------------------------------------------
    # 5. 中文翻译
    # --------------------------------------------------------

    if translation:

        elements.append(
            {
                "tag": "hr",
            }
        )

        elements.extend(
            make_text_section(
                "🇨🇳",
                "中文翻译",
                translation,
            )
        )

    # --------------------------------------------------------
    # 6. 重点词汇
    # --------------------------------------------------------

    vocabulary_card = (
        make_vocabulary_card(
            vocabulary_items
        )
    )

    if vocabulary_card:

        elements.append(
            {
                "tag": "hr",
            }
        )

        elements.append(
            vocabulary_card
        )

    # --------------------------------------------------------
    # 7. 重点短语
    # --------------------------------------------------------

    if phrases:

        elements.append(
            {
                "tag": "hr",
            }
        )

        elements.extend(
            make_text_section(
                "💬",
                "重点短语",
                phrases,
            )
        )

    # --------------------------------------------------------
    # 8. 语法难点
    # --------------------------------------------------------

    if grammar:

        elements.append(
            {
                "tag": "hr",
            }
        )

        elements.extend(
            make_text_section(
                "🧠",
                "语法难点",
                grammar,
            )
        )

    # --------------------------------------------------------
    # 9. 学习提示
    # --------------------------------------------------------

    if notes:

        elements.append(
            {
                "tag": "hr",
            }
        )

        elements.extend(
            make_text_section(
                "💡",
                "学习提示",
                notes,
            )
        )

    # --------------------------------------------------------
    # 10. 学习方法提示
    # --------------------------------------------------------

    elements.append(
        {
            "tag": "hr",
        }
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "**🎯 建议这样学习**\n\n"
                    "① 先通读英文原文\n"
                    "② 注意蓝色高亮的重点表达\n"
                    "③ 对照中文翻译检查理解\n"
                    "④ 记忆重点词汇与短语\n"
                    "⑤ 最后回看语法难点\n\n"
                    "📌 **不要只背单词，要结合文章语境理解。**"
                ),
            },
        }
    )

    # --------------------------------------------------------
    # 11. 原文按钮
    # --------------------------------------------------------

    if article_url:

        elements.append(
            {
                "tag": "hr",
            }
        )

        elements.append(
            {
                "tag": "action",
                "actions": [
                    make_url_button(
                        "📄 在 GitHub 打开完整文章",
                        article_url,
                        "primary",
                    )
                ],
            }
        )

    # --------------------------------------------------------
    # Card
    # --------------------------------------------------------

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
                    "📖 English Reading"
                ),
            },
        },

        "elements": elements,
    }


# ============================================================
# 卡片按钮
# ============================================================

def make_url_button(
    text: str,
    url: str | None,
    button_type: str = "default",
) -> dict[str, Any] | None:

    if not url:
        return None

    return {
        "tag": "button",
        "text": {
            "tag": "plain_text",
            "content": text,
        },
        "type": button_type,
        "url": url,
    }


# ============================================================
# 学习中心
# ============================================================

def make_home_card(
    title: str,
    difficulty: str,
    level: str,
    article_type: str,
    image_key: str | None,
    question_counts: dict[str, int],
    article_url: str | None,
    exam_url: str | None,
    answers_url: str | None,
) -> dict[str, Any]:

    total_questions = sum(
        question_counts.values()
    )

    elements: list[dict[str, Any]] = []

    if image_key:

        elements.append(
            {
                "tag": "img",
                "img_key": image_key,
                "alt": {
                    "tag": "plain_text",
                    "content": title,
                },
                "mode": "fit_horizontal",
            }
        )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**📚 {title}**\n\n"
                    f"⭐ **难度：** "
                    f"{difficulty or '—'}\n"
                    f"👦 **级别：** "
                    f"{level or '—'}\n"
                    f"📖 **文体：** "
                    f"{article_type or '—'}\n"
                    f"📝 **题目：** "
                    f"{total_questions} 项"
                ),
            },
        }
    )

    elements.append(
        {
            "tag": "hr",
        }
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "**今天的学习内容**\n\n"
                    "📖 精读文章\n"
                    "📝 综合试卷\n"
                    "🎧 听力训练\n"
                    "💡 词汇、语法与阅读分析\n\n"
                    "建议顺序："
                    "**阅读 → 答题 → 听力 → 查看解析**"
                ),
            },
        }
    )

    buttons = []

    button = make_url_button(
        "📖 查看文章",
        article_url,
        "primary",
    )

    if button:
        buttons.append(button)

    button = make_url_button(
        "📝 查看试卷",
        exam_url,
    )

    if button:
        buttons.append(button)

    if buttons:

        elements.append(
            {
                "tag": "action",
                "actions": buttons,
            }
        )

    if answers_url:

        elements.append(
            {
                "tag": "action",
                "actions": [
                    make_url_button(
                        "💡 查看答案与解析",
                        answers_url,
                    )
                ],
            }
        )

    return {
        "config": {
            "wide_screen_mode": True,
            "enable_forward": True,
        },
        "header": {
            "template": "turquoise",
            "title": {
                "tag": "plain_text",
                "content": (
                    "📚 748686 English Learning"
                ),
            },
        },
        "elements": elements,
    }


# ============================================================
# Exam Card
# ============================================================

def make_exam_card(
    title: str,
    counts: dict[str, int],
    exam_url: str | None,
    answers_url: str | None,
) -> dict[str, Any]:

    rows = []

    display_names = [
        ("听力", "🎧"),
        ("单项选择", "🔤"),
        ("多项选择", "☑️"),
        ("完形填空", "🧩"),
        ("阅读理解", "📖"),
        ("翻译", "🌐"),
        ("写作", "✍️"),
    ]

    for name, icon in display_names:

        count = counts.get(
            name,
            0,
        )

        if count:

            rows.append(
                f"{icon} **{name}：** "
                f"{count}题"
            )

    content = (
        f"**{title}**\n\n"
        "📝 **综合英语试卷**\n\n"
        + "\n".join(rows)
        + "\n\n"
        "📌 建议先独立完成试卷，"
        "再查看答案与解析。\n"
        "本阶段飞书卡片为展示入口，"
        "不会在答题过程中提前显示答案。"
    )

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": content,
            },
        },
        {
            "tag": "hr",
        },
    ]

    buttons = []

    exam_button = make_url_button(
        "📝 打开试卷",
        exam_url,
        "primary",
    )

    if exam_button:
        buttons.append(exam_button)

    answers_button = make_url_button(
        "💡 查看答案",
        answers_url,
    )

    if answers_button:
        buttons.append(answers_button)

    if buttons:

        elements.append(
            {
                "tag": "action",
                "actions": buttons,
            }
        )

    return {
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "template": "orange",
            "title": {
                "tag": "plain_text",
                "content": "📝 综合英语试卷",
            },
        },
        "elements": elements,
    }


# ============================================================
# Listening Card
# ============================================================

def make_listening_card(
    title: str,
    audio_files: list[Path],
) -> dict[str, Any]:

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**{title}**\n\n"
                    "🎧 听力训练文件已经生成。\n\n"
                    "建议按照："
                    "**Part A → Part B → Part C** "
                    "完成训练。"
                ),
            },
        },
        {
            "tag": "hr",
        },
    ]

    for path in audio_files:

        url = github_file_url(
            path
        )

        if url:

            button = make_url_button(
                f"🎧 {path.stem}",
                url,
            )

            if button:

                elements.append(
                    {
                        "tag": "action",
                        "actions": [
                            button,
                        ],
                    }
                )

        else:

            elements.append(
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"🎧 **{path.name}**"
                        ),
                    },
                }
            )

    return {
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "template": "purple",
            "title": {
                "tag": "plain_text",
                "content": "🎧 Listening",
            },
        },
        "elements": elements,
    }


# ============================================================
# 文件发现
# ============================================================

def build_paths(
    root: Path,
    date: str,
    difficulty: str,
    article_type: str,
) -> dict[str, Path]:

    base = (
        root
        / "02_英语学习系统"
        / "output"
        / date
    )

    return {

        "base": base,

        "article": (
            base
            / "文章"
            / f"{difficulty}星_"
              f"{article_type}_文章.md"
        ),

        "exam": (
            base
            / "配套试卷"
            / f"{difficulty}星_"
              f"{article_type}_试卷.md"
        ),

        "answers": (
            base
            / "配套试卷"
            / f"{difficulty}星_"
              f"{article_type}_答案与解析.md"
        ),

        "image": (
            base
            / "配图"
            / "文章配图.png"
        ),

        "listening_dir": (
            base
            / "配套试卷"
            / "听力"
        ),
    }


def discover_audio_files(
    listening_dir: Path,
) -> list[Path]:

    if not listening_dir.is_dir():
        return []

    allowed = {
        ".mp3",
        ".m4a",
        ".wav",
        ".aac",
        ".flac",
    }

    files = [
        path
        for path in listening_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in allowed
    ]

    priority = {
        "Listening_A": 1,
        "Listening_B": 2,
        "Listening_C": 3,
        "Listening_总音频": 4,
    }

    files.sort(
        key=lambda p: (
            priority.get(
                p.stem,
                99,
            ),
            p.name,
        )
    )

    return files


# ============================================================
# 主流程
# ============================================================

def run(
    args: argparse.Namespace,
) -> None:

    root = Path(
        args.repo_root
    ).resolve()

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

    paths = build_paths(
        root=root,
        date=args.date,
        difficulty=args.difficulty,
        article_type=args.article_type,
    )

    log()
    log("=" * 70)
    log("748686 English Learning System")
    log("Feishu English Renderer V2.1")
    log("=" * 70)

    log(
        f"日期：{args.date}"
    )

    log(
        f"难度：{args.difficulty}星"
    )

    log(
        f"文体：{args.article_type}"
    )

    log()

    # --------------------------------------------------------
    # 输出目录
    # --------------------------------------------------------

    if not paths["base"].is_dir():

        log(
            f"⚠️ 输出目录不存在："
            f"{paths['base']}"
        )

        log(
            "⚠️ 当前日期没有英语学习输出"
        )

        log(
            "ℹ️ Feishu SKIP"
        )

        return

    # --------------------------------------------------------
    # 文章
    # --------------------------------------------------------

    if not file_exists(
        paths["article"]
    ):

        log(
            f"⚠️ 文章不存在："
            f"{paths['article']}"
        )

        log(
            "ℹ️ 当前日期无法发送英语学习内容"
        )

        log(
            "ℹ️ Feishu SKIP"
        )

        return

    article_text = read_text(
        paths["article"]
    )

    title = markdown_title(
        article_text
    )

    difficulty = extract_meta(
        article_text,
        "difficulty",
    )

    level = extract_meta(
        article_text,
        "level",
    )

    article_type = extract_meta(
        article_text,
        "article_type",
    )

    article_body = extract_article_body(
        article_text
    )

    log(
        f"✓ 文章："
        f"{paths['article'].name}"
    )

    # --------------------------------------------------------
    # V2.1 Article Parser Debug
    # --------------------------------------------------------

    article_sections = split_markdown_sections(
        article_body
    )

    highlight_words = extract_highlight_words(
        article_sections.get(
            "english",
            article_body,
        )
    )

    vocabulary_items = extract_vocabulary_items(
        article_sections.get(
            "vocabulary",
            "",
        )
    )

    for item in vocabulary_items:

        word = item.get(
            "word",
            "",
        ).strip()

        if word and word not in highlight_words:

            highlight_words.append(
                word
            )

    log(
        f"✓ 英文正文段落："
        f"{len(paragraph_list(article_sections.get('english', article_body)))}"
    )

    log(
        f"✓ 中文翻译："
        f"{'有' if article_sections.get('translation') else '无'}"
    )

    log(
        f"✓ 重点词汇："
        f"{len(vocabulary_items)}"
    )

    log(
        f"✓ 重点高亮词："
        f"{len(highlight_words)}"
    )

    log(
        f"✓ 重点短语："
        f"{'有' if article_sections.get('phrases') else '无'}"
    )

    log(
        f"✓ 语法难点："
        f"{'有' if article_sections.get('grammar') else '无'}"
    )

    # --------------------------------------------------------
    # 试卷
    # --------------------------------------------------------

    exam_text = ""
    question_counts = {}

    if file_exists(
        paths["exam"]
    ):

        exam_text = read_text(
            paths["exam"]
        )

        question_counts = count_questions(
            exam_text
        )

        log(
            f"✓ 试卷："
            f"{paths['exam'].name}"
        )

    else:

        log(
            "ℹ️ 没有试卷"
        )

    # --------------------------------------------------------
    # 答案
    # --------------------------------------------------------

    answers_exists = file_exists(
        paths["answers"]
    )

    if answers_exists:

        log(
            f"✓ 答案解析："
            f"{paths['answers'].name}"
        )

    else:

        log(
            "ℹ️ 没有答案与解析"
        )

    # --------------------------------------------------------
    # 图片
    # --------------------------------------------------------

    image_path = paths["image"]

    if image_path.is_file():

        log(
            f"✓ 配图："
            f"{image_path.name}"
        )

    else:

        image_path = None

        log(
            "ℹ️ 没有配图"
        )

    # --------------------------------------------------------
    # 音频
    # --------------------------------------------------------

    audio_files = discover_audio_files(
        paths["listening_dir"]
    )

    if audio_files:

        log(
            f"✓ 音频："
            f"{len(audio_files)} 个"
        )

    else:

        log(
            "ℹ️ 没有听力文件"
        )

    # --------------------------------------------------------
    # GitHub links
    # --------------------------------------------------------

    article_url = github_file_url(
        paths["article"]
    )

    exam_url = (
        github_file_url(
            paths["exam"]
        )
        if paths["exam"].is_file()
        else None
    )

    answers_url = (
        github_file_url(
            paths["answers"]
        )
        if answers_exists
        else None
    )

    # --------------------------------------------------------
    # Feishu client
    # --------------------------------------------------------

    client = FeishuClient(
        app_id=app_id,
        app_secret=app_secret,
        webhook=webhook,
    )

    # --------------------------------------------------------
    # 图片上传
    # --------------------------------------------------------

    image_key = None

    if image_path:

        image_key = client.upload_image(
            image_path
        )

    # --------------------------------------------------------
    # 1. 学习中心
    # --------------------------------------------------------

    log()
    log(
        "→ 发送英语学习中心"
    )

    home_card = make_home_card(
        title=title,
        difficulty=difficulty,
        level=level,
        article_type=article_type,
        image_key=image_key,
        question_counts=question_counts,
        article_url=article_url,
        exam_url=exam_url,
        answers_url=answers_url,
    )

    client.send_card(
        home_card
    )

    log(
        "✓ 学习中心已发送"
    )

    # --------------------------------------------------------
    # 2. 文章 V2.1
    # --------------------------------------------------------

    log(
        "→ 发送精读文章 V2.1"
    )

    article_card = make_article_card(
        title=title,
        article_body=article_body,
        image_key=image_key,
        difficulty=difficulty,
        article_type=article_type,
        article_url=article_url,
    )

    client.send_card(
        article_card
    )

    log(
        "✓ 精读文章 V2.1 已发送"
    )

    # --------------------------------------------------------
    # 3. 考试
    # --------------------------------------------------------

    if paths["exam"].is_file():

        log(
            "→ 发送考试卡片"
        )

        exam_card = make_exam_card(
            title=title,
            counts=question_counts,
            exam_url=exam_url,
            answers_url=answers_url,
        )

        client.send_card(
            exam_card
        )

        log(
            "✓ 考试卡片已发送"
        )

    else:

        log(
            "ℹ️ 没有试卷，跳过考试卡片"
        )

    # --------------------------------------------------------
    # 4. 听力
    # --------------------------------------------------------

    if audio_files:

        log(
            "→ 发送听力卡片"
        )

        listening_card = make_listening_card(
            title=title,
            audio_files=audio_files,
        )

        client.send_card(
            listening_card
        )

        log(
            "✓ 听力卡片已发送"
        )

    else:

        log(
            "ℹ️ 没有听力，跳过听力卡片"
        )

    # --------------------------------------------------------
    # 结束
    # --------------------------------------------------------

    log()

    log("=" * 70)

    log(
        "✓ Feishu English Renderer V2.1 完成"
    )

    log(
        "✓ Article Card 已升级为英语精读学习卡"
    )

    log(
        "✓ English / 中文 / 词汇 / 短语 / 语法 / 学习提示"
    )

    log(
        "✓ 使用 FEISHU_WEBHOOK"
    )

    log(
        "✓ 使用同一个 748686知识系统 飞书群"
    )

    log("=" * 70)


# ============================================================
# 参数
# ============================================================

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "748686 English Learning "
            "Feishu Renderer V2.1"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
        help="UTC 日期，例如 2026-09-27",
    )

    parser.add_argument(
        "--difficulty",
        required=True,
        help="难度，例如 1",
    )

    parser.add_argument(
        "--article-type",
        required=True,
        help="文章类型，例如 议论文",
    )

    parser.add_argument(
        "--repo-root",
        default=".",
        help="仓库根目录",
    )

    return parser.parse_args()


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":

    try:

        run(
            parse_args()
        )

    except KeyboardInterrupt:

        log(
            "用户中断"
        )

        sys.exit(130)

    except Exception as exc:

        log()

        log("=" * 70)

        log(
            "❌ Feishu English Renderer FAILED"
        )

        log("=" * 70)

        log(
            str(exc)
        )

        sys.exit(1)
