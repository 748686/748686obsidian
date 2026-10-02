#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu English Renderer V2.3

V2.3 修复：
1. 读取当天 input/日期.md 中的新学单词。
2. 支持 input、Input、输入等常见目录。
3. 不要求文章 Markdown 预先使用 **单词**。
4. 新学单词在飞书英文正文中显示为蓝色 + 粗体。
5. 使用已验证格式：**<font color='blue'>word</font>**
6. 输出识别到的新词、正文命中次数和最终正文。
7. 文章卡片末尾暂时附加高亮诊断信息。
8. 保留原有文章、配图、试卷、答案、听力及按钮流程。
9. 不修改 main.py、试卷生成、答案解析、图片生成或音频生成。
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
TOKEN_URL = f"{FEISHU_BASE}/open-apis/auth/v3/tenant_access_token/internal"
IMAGE_UPLOAD_URL = f"{FEISHU_BASE}/open-apis/im/v1/images"


# ============================================================
# 通用工具
# ============================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def file_exists(path: Path) -> bool:
    return path.is_file()


def compact(text: str, max_length: int = 900) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text if len(text) <= max_length else text[:max_length].rstrip() + "\n..."


def markdown_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if not match:
        return "English Learning"

    title = match.group(1).strip()
    for suffix in ("｜答案与解析", "｜答案", "｜试卷", "｜文章"):
        title = title.replace(suffix, "")
    return title.strip()


def extract_meta(text: str, key: str) -> str:
    patterns = {
        "difficulty": [r"难度：([^｜\n]+)", r"难度：([^\n]+)"],
        "level": [r"级别：([^｜\n]+)", r"(小学[^\n]+年级)"],
        "article_type": [r"文章类型：([^｜\n]+)", r"文体：([^｜\n]+)"],
        "score": [r"总分：([^\n]+)"],
    }

    for pattern in patterns.get(key, []):
        match = re.search(pattern, text)
        if match and match.lastindex:
            return match.group(1).strip()

    return ""


# ============================================================
# GitHub 链接
# ============================================================

def github_file_url(path: Path) -> str | None:
    server = os.getenv("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
    repository = os.getenv("GITHUB_REPOSITORY", "").strip()
    ref = os.getenv("GITHUB_REF_NAME", "main").strip()

    if not repository:
        return None

    try:
        relative = path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        return None

    relative_url = "/".join(part.replace(" ", "%20") for part in relative.parts)
    return f"{server}/{repository}/blob/{ref}/{relative_url}"


def make_url_button(
    text: str,
    url: str | None,
    button_type: str = "default",
) -> dict[str, Any] | None:
    if not url:
        return None

    return {
        "tag": "button",
        "text": {"tag": "plain_text", "content": text},
        "type": button_type,
        "url": url,
    }


# ============================================================
# Feishu Client
# ============================================================

class FeishuClient:

    def __init__(self, app_id: str, app_secret: str, webhook: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.webhook = webhook
        self.session = requests.Session()
        self._token: str | None = None

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
            fail("获取 Feishu tenant_access_token 失败：" +
                 json.dumps(data, ensure_ascii=False))

        token = data.get("tenant_access_token")
        if not token:
            fail("Feishu 返回结果中没有 tenant_access_token")

        self._token = token
        return token

    def upload_image(self, path: Path) -> str:
        log(f"   ↑ 上传图片：{path.name}")

        with path.open("rb") as fp:
            response = self.session.post(
                IMAGE_UPLOAD_URL,
                headers={
                    "Authorization": f"Bearer {self.tenant_access_token()}"
                },
                data={"image_type": "message"},
                files={"image": (path.name, fp, "image/png")},
                timeout=120,
            )

        response.raise_for_status()
        data = response.json()

        if data.get("code") != 0:
            fail("上传 Feishu 图片失败：" +
                 json.dumps(data, ensure_ascii=False))

        image_key = data.get("data", {}).get("image_key")
        if not image_key:
            fail("Feishu 图片上传成功，但没有返回 image_key")

        log(f"   ✓ image_key: {image_key}")
        return image_key

    def send_card(self, card: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(
            self.webhook,
            headers={"Content-Type": "application/json; charset=utf-8"},
            json={"msg_type": "interactive", "card": card},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("code") != 0:
            fail("Feishu Webhook 发送卡片失败：" +
                 json.dumps(data, ensure_ascii=False))

        return data


# ============================================================
# 试卷题量统计
# ============================================================

def count_questions(exam_text: str) -> dict[str, int]:
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
        "听力": [r"听力"],
        "单项选择": [r"单项选择"],
        "多项选择": [r"多项选择", r"多选题"],
        "完形填空": [r"完形填空"],
        "阅读理解": [r"阅读理解"],
        "翻译": [r"翻译"],
        "写作": [r"写作"],
    }

    listening_match = re.search(
        r"(?:^|\n)#{1,6}\s*[^#\n]*听力[^#\n]*\n"
        r"([\s\S]*?)(?=\n#{1,6}\s|\Z)",
        exam_text,
        re.MULTILINE,
    )

    if listening_match:
        listening_body = listening_match.group(1)
        part_counts = []

        for part in ("A", "B", "C"):
            part_match = re.search(
                rf"Part\s*{part}[\s\S]*?(?=Part\s*[ABC]|\Z)",
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
                part_counts.append(len(numbers))

        sections["听力"] = sum(part_counts)

    for section, patterns in section_patterns.items():
        if section == "听力":
            continue

        body = None
        for section_pattern in patterns:
            match = re.search(
                rf"(?:^|\n)#{1,6}\s*[^#\n]*{section_pattern[0]}[^#\n]*\n"
                rf"([\s\S]*?)(?=\n#{1,6}\s|\Z)",
                exam_text,
                re.IGNORECASE,
            )
            if match:
                body = match.group(1)
                break

        if not body:
            continue

        numbers = re.findall(r"^###?\s*(\d+)\.", body, re.MULTILINE)
        if not numbers:
            numbers = re.findall(r"^\s*(\d+)[\.\、]", body, re.MULTILINE)

        if numbers:
            sections[section] = len(numbers)

    if sections["多项选择"] == 0:
        sections["多项选择"] = sections["多选题"]

    del sections["多选题"]
    return sections


# ============================================================
# 文章解析
# ============================================================

def extract_article_body(article_text: str) -> str:
    text = article_text.strip()

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2].strip()

    text = re.sub(r"^#\s+.+$\n?", "", text, count=1, flags=re.MULTILINE)
    return text.strip()


def normalize_section_name(heading: str) -> str:
    value = re.sub(r"^[#\s]+", "", heading.strip())
    value = re.sub(r"[：:]+$", "", value)
    lower = value.lower()

    if lower in {
        "english", "english article", "article",
        "英文", "英文原文", "英语原文", "英语文章",
    }:
        return "english"

    if (
        "中文翻译" in value or "中文译文" in value
        or value == "翻译" or "translation" in lower
        or lower == "chinese"
    ):
        return "translation"

    if (
        "重点词汇" in value or "重点单词" in value
        or "核心词汇" in value or "核心单词" in value
        or value == "词汇" or "vocabulary" in lower or "vocab" in lower
    ):
        return "vocabulary"

    if "重点短语" in value or "核心短语" in value or value == "短语" or "phrase" in lower:
        return "phrases"

    if (
        "语法难点" in value or "语法重点" in value
        or "语法解析" in value or "grammar" in lower
    ):
        return "grammar"

    if (
        "学习建议" in value or "学习提示" in value
        or "学习要点" in value or "learning notes" in lower
        or "learning tips" in lower or lower == "notes"
    ):
        return "notes"

    return "other"


def split_markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {
        key: [] for key in
        ("english", "translation", "vocabulary", "phrases", "grammar", "notes", "other")
    }
    current = "english"

    for line in text.splitlines():
        heading = re.match(r"^\s{0,3}(#{2,6})\s+(.+?)\s*$", line)
        if heading:
            current = normalize_section_name(heading.group(2))
            continue
        sections[current].append(line)

    return {key: "\n".join(value).strip() for key, value in sections.items()}


def clean_markdown(text: str) -> str:
    text = text.strip()
    text = re.sub(r"<span[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</span>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    return text.strip()


def paragraph_list(text: str) -> list[str]:
    text = clean_markdown(text)
    return [
        part.strip()
        for part in re.split(r"\n\s*\n+", text)
        if part.strip()
    ]


def extract_highlight_words(text: str) -> list[str]:
    words: list[str] = []

    for pattern in (r"\*\*([^*\n]+?)\*\*", r"__([^_\n]+?)__"):
        for value in re.findall(pattern, text):
            value = value.strip()
            if value and len(value) <= 80 and value not in words:
                words.append(value)

    return words


def extract_vocabulary_items(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        line = re.sub(r"^[-*•]\s*", "", line)
        line = re.sub(r"^\d+[.)、]\s*", "", line)

        match = re.match(r"^\*\*(.+?)\*\*\s*[-—:：]\s*(.+)$", line)
        if match:
            items.append({
                "word": match.group(1).strip(),
                "meaning": match.group(2).strip(),
            })
            continue

        match = re.match(
            r"^([A-Za-z][A-Za-z0-9' -]{1,60})\s*[：:]\s*(.+)$",
            line,
        )
        if match:
            items.append({
                "word": match.group(1).strip(),
                "meaning": match.group(2).strip(),
            })
            continue

        match = re.match(
            r"^([A-Za-z][A-Za-z0-9' -]{1,60})\s+[-—]\s+(.+)$",
            line,
        )
        if match:
            items.append({
                "word": match.group(1).strip(),
                "meaning": match.group(2).strip(),
            })

    return items


# ============================================================
# 读取当天 Input 文件中的新学单词
# ============================================================

def find_input_file(root: Path, date: str) -> Path | None:
    """
    支持以下位置：
    02_英语学习系统/input/YYYY-MM-DD.md
    02_英语学习系统/Input/YYYY-MM-DD.md
    02_英语学习系统/INPUT/YYYY-MM-DD.md
    02_英语学习系统/输入/YYYY-MM-DD.md
    仓库根目录下的 input/Input/INPUT/输入 目录
    """

    directories = [
        root / "02_英语学习系统" / "input",
        root / "02_英语学习系统" / "Input",
        root / "02_英语学习系统" / "INPUT",
        root / "02_英语学习系统" / "输入",
        root / "input",
        root / "Input",
        root / "INPUT",
        root / "输入",
    ]

    for directory in directories:
        candidate = directory / f"{date}.md"
        if candidate.is_file():
            return candidate

        # 同一天的 txt 输入也兼容
        candidate_txt = directory / f"{date}.txt"
        if candidate_txt.is_file():
            return candidate_txt

    return None


def extract_input_words(text: str) -> list[str]:
    """
    从日期输入文件中提取新学单词。

    支持示例：
      expand
      - expand
      1. expand
      expand: 扩大
      expand — 扩大
      **expand** - 扩大
      adapt (v.) 适应
      look forward to — 期待

    按行读取，尽量避免把说明性句子里的普通英文全部当成新词。
    """

    words: list[str] = []

    ignored_lines = {
        "新学单词", "今日单词", "重点单词", "学习单词",
        "单词", "词汇", "今日新词", "新单词",
        "words", "vocabulary", "new words", "today's words",
    }

    for original_line in text.splitlines():
        line = original_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            line = re.sub(r"^#+\s*", "", line).strip()

        line = re.sub(r"^\s*[-*+•]\s*", "", line)
        line = re.sub(r"^\s*\d+\s*[.)、]\s*", "", line)
        line = re.sub(r"^\s*\[\s*[xX ]\s*\]\s*", "", line)
        line = line.strip(" \t|")

        if not line:
            continue

        if line.lower().strip(" :：") in ignored_lines:
            continue

        # 去掉单词外侧的 Markdown 粗体符号
        line = re.sub(r"^\*\*(.*?)\*\*$", r"\1", line).strip()
        line = re.sub(r"^__(.*?)__$", r"\1", line).strip()

        # 表格行：优先取第一列
        if "|" in line:
            columns = [c.strip() for c in line.strip("|").split("|")]
            if columns:
                line = columns[0]

        # 去掉编号之后，优先读取分隔符前的英文词或短语
        # 分隔符包括中英文冒号、长横线、制表符、等号。
        left = re.split(r"\s*(?:：|:|—|–|=|\t)\s*", line, maxsplit=1)[0].strip()

        # “word - 中文释义”格式
        if left == line:
            match = re.match(
                r"^([A-Za-z][A-Za-z'’-]*(?:\s+[A-Za-z][A-Za-z'’-]*){0,4})"
                r"\s+-\s+.+$",
                line,
            )
            if match:
                left = match.group(1).strip()

        # “word (n.) 中文释义”格式
        if left == line:
            match = re.match(
                r"^([A-Za-z][A-Za-z'’-]*(?:\s+[A-Za-z][A-Za-z'’-]*){0,4})"
                r"\s+\((?:n|v|adj|adv|prep|phr|conj|pron|num|art)[^)]*\)"
                r"(?:\s+.*)?$",
                line,
                re.IGNORECASE,
            )
            if match:
                left = match.group(1).strip()

        # 只接受英文单词/短语，避免把中文或整句误识别为新词
        left = left.strip(" \t`*_\"'“”‘’.,，。;；()（）[]{}")

        if not re.fullmatch(
            r"[A-Za-z][A-Za-z'’-]*(?:\s+[A-Za-z][A-Za-z'’-]*){0,4}",
            left,
        ):
            # 纯单词行后面跟中文释义、词性时，再尝试提取行首英文短语
            match = re.match(
                r"^([A-Za-z][A-Za-z'’-]*(?:\s+[A-Za-z][A-Za-z'’-]*){0,4})",
                line,
            )
            if not match:
                continue
            left = match.group(1).strip()

        if left.lower() in ignored_lines:
            continue

        if left and left.casefold() not in {w.casefold() for w in words}:
            words.append(left)

    return words


# ============================================================
# 英文正文高亮
# ============================================================

def highlight_markdown_words(text: str, highlight_words: list[str]) -> str:
    """
    输出格式：
    **<font color='blue'>word</font>**

    先保护已有 HTML 高亮和 Markdown 粗体，避免重复套标签。
    """

    if not text:
        return text

    placeholders: dict[str, str] = {}

    def save_placeholder(value: str) -> str:
        key = f"ZZFEISHUHL{len(placeholders)}ZZ"
        placeholders[key] = value
        return key

    # 已经有的 font 格式先保护，防止重复套标签
    text = re.sub(
        r"\*\*<font\b[^>]*>.*?</font>\*\*|<font\b[^>]*>.*?</font>",
        lambda m: save_placeholder(m.group(0)),
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # 已有 Markdown 粗体转为蓝色粗体并保护
    text = re.sub(
        r"\*\*([^*\n]+?)\*\*",
        lambda m: save_placeholder(
            f"**<font color='blue'>{m.group(1)}</font>**"
        ),
        text,
    )
    text = re.sub(
        r"__([^_\n]+?)__",
        lambda m: save_placeholder(
            f"**<font color='blue'>{m.group(1)}</font>**"
        ),
        text,
    )

    # 长短语优先，避免先匹配短词破坏长短语
    unique_words = sorted(
        {w.strip() for w in highlight_words if w.strip()},
        key=len,
        reverse=True,
    )

    for word in unique_words:
        pattern = re.compile(
            rf"(?<![A-Za-z0-9_])({re.escape(word)})(?![A-Za-z0-9_])",
            re.IGNORECASE,
        )

        text = pattern.sub(
            lambda m: save_placeholder(
                f"**<font color='blue'>{m.group(1)}</font>**"
            ),
            text,
        )

    # 恢复所有保护内容
    for key, value in placeholders.items():
        text = text.replace(key, value)

    return text


def count_word_occurrences(text: str, words: list[str]) -> dict[str, int]:
    results: dict[str, int] = {}

    for word in words:
        word = word.strip()
        if not word:
            continue

        pattern = re.compile(
            rf"(?<![A-Za-z0-9_]){re.escape(word)}(?![A-Za-z0-9_])",
            re.IGNORECASE,
        )
        count = len(pattern.findall(text))

        if count:
            results[word] = count

    return results


def make_article_paragraph(
    text: str,
    highlight_words: list[str],
) -> dict[str, Any]:
    content = highlight_markdown_words(text, highlight_words)

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
    content = f"**{icon} {title}**"
    if subtitle:
        content += f"\n{subtitle}"

    return {
        "tag": "div",
        "text": {"tag": "lark_md", "content": content},
    }


def make_highlight_word_card(words: list[str]) -> dict[str, Any] | None:
    if not words:
        return None

    display = [
        f"**<font color='blue'>{word}</font>**"
        for word in words[:20]
    ]

    content = "**🔵 今日重点表达**\n\n" + "　　".join(display)

    return {
        "tag": "div",
        "text": {"tag": "lark_md", "content": content},
    }


def make_vocabulary_card(
    vocabulary: list[dict[str, str]],
) -> dict[str, Any] | None:
    if not vocabulary:
        return None

    lines = ["**🔵 重点词汇**", ""]

    for item in vocabulary[:15]:
        word = item.get("word", "").strip()
        meaning = item.get("meaning", "").strip()

        if not word:
            continue

        styled_word = f"**<font color='blue'>{word}</font>**"
        lines.append(f"{styled_word}　{meaning}" if meaning else styled_word)

    if len(lines) <= 2:
        return None

    return {
        "tag": "div",
        "text": {"tag": "lark_md", "content": "\n".join(lines)},
    }


def make_text_section(
    icon: str,
    title: str,
    text: str,
) -> list[dict[str, Any]]:
    elements: list[dict[str, Any]] = []

    if not text:
        return elements

    elements.append(make_section_title(icon, title))
    elements.append({"tag": "hr"})

    for paragraph in paragraph_list(text):
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": paragraph},
        })

    return elements


# ============================================================
# 文章卡片
# ============================================================

def make_article_card(
    title: str,
    article_body: str,
    image_key: str | None,
    difficulty: str,
    article_type: str,
    article_url: str | None,
    input_words: list[str] | None = None,
) -> dict[str, Any]:

    sections = split_markdown_sections(article_body)

    english = sections.get("english", "") or article_body
    translation = sections.get("translation", "")
    vocabulary_text = sections.get("vocabulary", "")
    phrases = sections.get("phrases", "")
    grammar = sections.get("grammar", "")
    notes = sections.get("notes", "")

    highlight_words = extract_highlight_words(english)
    vocabulary_items = extract_vocabulary_items(vocabulary_text)

    for item in vocabulary_items:
        word = item.get("word", "").strip()
        if word and word.casefold() not in {w.casefold() for w in highlight_words}:
            highlight_words.append(word)

    # 把当天 Input 文件中的新学单词加入正文高亮名单
    for word in (input_words or []):
        if word and word.casefold() not in {w.casefold() for w in highlight_words}:
            highlight_words.append(word)

    elements: list[dict[str, Any]] = []

    if image_key:
        elements.append({
            "tag": "img",
            "img_key": image_key,
            "alt": {"tag": "plain_text", "content": title},
            "mode": "fit_horizontal",
        })

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"# {title}\n\n"
                f"⭐ {difficulty or '—'}　·　📖 {article_type or '—'}\n\n"
                "✨ **English Reading · 精读学习**"
            ),
        },
    })
    elements.append({"tag": "hr"})

    elements.append(make_section_title("🇬🇧", "English Article", "英文原文"))
    elements.append({"tag": "hr"})

    english_paragraphs = paragraph_list(english)
    final_english_paragraphs: list[str] = []

    for paragraph in english_paragraphs:
        final_content = highlight_markdown_words(paragraph, highlight_words)
        final_english_paragraphs.append(final_content)
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": final_content},
        })

    # 今日重点表达
    highlight_card = make_highlight_word_card(highlight_words)
    if highlight_card:
        elements.append({"tag": "hr"})
        elements.append(highlight_card)

    # 中文翻译
    if translation:
        elements.append({"tag": "hr"})
        elements.extend(make_text_section("🇨🇳", "中文翻译", translation))

    # 重点词汇
    vocabulary_card = make_vocabulary_card(vocabulary_items)
    if vocabulary_card:
        elements.append({"tag": "hr"})
        elements.append(vocabulary_card)

    # 重点短语
    if phrases:
        elements.append({"tag": "hr"})
        elements.extend(make_text_section("💬", "重点短语", phrases))

    # 语法难点
    if grammar:
        elements.append({"tag": "hr"})
        elements.extend(make_text_section("🧠", "语法难点", grammar))

    # 学习提示
    if notes:
        elements.append({"tag": "hr"})
        elements.extend(make_text_section("💡", "学习提示", notes))

    elements.append({"tag": "hr"})
    elements.append({
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
    })

    if article_url:
        elements.append({"tag": "hr"})
        button = make_url_button("📄 在 GitHub 打开完整文章", article_url, "primary")
        if button:
            elements.append({"tag": "action", "actions": [button]})

    # 临时诊断：显示在飞书文章卡片末尾，确认实际生成的 Markdown
    raw_final_english = "\n\n".join(final_english_paragraphs)
    occurrence_counts = count_word_occurrences(english, input_words or [])

    diagnostic_lines = [
        "**🔧 临时高亮诊断**",
        "",
        f"Input 新学单词数：{len(input_words or [])}",
        f"正文实际命中单词种类：{len(occurrence_counts)}",
        "",
        "**Input 识别结果：**",
        ", ".join(input_words or []) if input_words else "未识别到新学单词",
        "",
        "**正文命中次数：**",
    ]

    if occurrence_counts:
        diagnostic_lines.extend(
            f"- {word}: {count} 次"
            for word, count in occurrence_counts.items()
        )
    else:
        diagnostic_lines.append("没有匹配到当天 Input 中的单词。")

    diagnostic_lines.extend([
        "",
        "**最终发送的英文正文 Markdown（原始格式）：**",
        "```text",
        compact(raw_final_english, 3500),
        "```",
    ])

    elements.append({"tag": "hr"})
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": "\n".join(diagnostic_lines),
        },
    })

    return {
        "config": {
            "wide_screen_mode": True,
            "enable_forward": True,
        },
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": "📖 English Reading",
            },
        },
        "elements": elements,
    }


# ============================================================
# 学习中心卡片
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

    total_questions = sum(question_counts.values())
    elements: list[dict[str, Any]] = []

    if image_key:
        elements.append({
            "tag": "img",
            "img_key": image_key,
            "alt": {"tag": "plain_text", "content": title},
            "mode": "fit_horizontal",
        })

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**📚 {title}**\n\n"
                f"⭐ **难度：** {difficulty or '—'}\n"
                f"👦 **级别：** {level or '—'}\n"
                f"📖 **文体：** {article_type or '—'}\n"
                f"📝 **题目：** {total_questions} 项"
            ),
        },
    })
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                "**今天的学习内容**\n\n"
                "📖 精读文章\n📝 综合试卷\n🎧 听力训练\n"
                "💡 词汇、语法与阅读分析\n\n"
                "建议顺序：**阅读 → 答题 → 听力 → 查看解析**"
            ),
        },
    })

    buttons = []
    for label, url, kind in (
        ("📖 查看文章", article_url, "primary"),
        ("📝 查看试卷", exam_url, "default"),
    ):
        button = make_url_button(label, url, kind)
        if button:
            buttons.append(button)

    if buttons:
        elements.append({"tag": "action", "actions": buttons})

    if answers_url:
        button = make_url_button("💡 查看答案与解析", answers_url)
        if button:
            elements.append({"tag": "action", "actions": [button]})

    return {
        "config": {"wide_screen_mode": True, "enable_forward": True},
        "header": {
            "template": "turquoise",
            "title": {
                "tag": "plain_text",
                "content": "📚 748686 English Learning",
            },
        },
        "elements": elements,
    }


# ============================================================
# 试卷卡片
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
        count = counts.get(name, 0)
        if count:
            rows.append(f"{icon} **{name}：** {count}题")

    content = (
        f"**{title}**\n\n📝 **综合英语试卷**\n\n"
        + "\n".join(rows)
        + "\n\n📌 建议先独立完成试卷，再查看答案与解析。\n"
        "本阶段飞书卡片为展示入口，不会在答题过程中提前显示答案。"
    )

    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": content}},
        {"tag": "hr"},
    ]

    buttons = []
    for label, url, kind in (
        ("📝 打开试卷", exam_url, "primary"),
        ("💡 查看答案", answers_url, "default"),
    ):
        button = make_url_button(label, url, kind)
        if button:
            buttons.append(button)

    if buttons:
        elements.append({"tag": "action", "actions": buttons})

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "orange",
            "title": {"tag": "plain_text", "content": "📝 综合英语试卷"},
        },
        "elements": elements,
    }


# ============================================================
# 听力卡片
# ============================================================

def make_listening_card(title: str, audio_files: list[Path]) -> dict[str, Any]:
    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**{title}**\n\n"
                    "🎧 听力训练文件已经生成。\n\n"
                    "建议按照：**Part A → Part B → Part C** 完成训练。"
                ),
            },
        },
        {"tag": "hr"},
    ]

    for path in audio_files:
        url = github_file_url(path)

        if url:
            button = make_url_button(f"🎧 {path.stem}", url)
            if button:
                elements.append({"tag": "action", "actions": [button]})
        else:
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": f"🎧 **{path.name}**"},
            })

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "purple",
            "title": {"tag": "plain_text", "content": "🎧 Listening"},
        },
        "elements": elements,
    }


# ============================================================
# 文件路径
# ============================================================

def build_paths(
    root: Path,
    date: str,
    difficulty: str,
    article_type: str,
) -> dict[str, Path]:

    base = root / "02_英语学习系统" / "output" / date

    return {
        "base": base,
        "article": base / "文章" / f"{difficulty}星_{article_type}_文章.md",
        "exam": base / "配套试卷" / f"{difficulty}星_{article_type}_试卷.md",
        "answers": base / "配套试卷" / f"{difficulty}星_{article_type}_答案与解析.md",
        "image": base / "配图" / "文章配图.png",
        "listening_dir": base / "配套试卷" / "听力",
    }


def discover_audio_files(listening_dir: Path) -> list[Path]:
    if not listening_dir.is_dir():
        return []

    allowed = {".mp3", ".m4a", ".wav", ".aac", ".flac"}
    files = [
        path for path in listening_dir.iterdir()
        if path.is_file() and path.suffix.lower() in allowed
    ]

    priority = {
        "Listening_A": 1,
        "Listening_B": 2,
        "Listening_C": 3,
        "Listening_总音频": 4,
    }

    files.sort(key=lambda p: (priority.get(p.stem, 99), p.name))
    return files


# ============================================================
# 主流程
# ============================================================

def run(args: argparse.Namespace) -> None:
    root = Path(args.repo_root).resolve()

    webhook = os.getenv("FEISHU_WEBHOOK", "").strip()
    app_id = os.getenv("APP_ID", "").strip()
    app_secret = os.getenv("APP_SECRET", "").strip()

    if not webhook:
        fail("缺少环境变量 FEISHU_WEBHOOK")
    if not app_id:
        fail("缺少环境变量 APP_ID")
    if not app_secret:
        fail("缺少环境变量 APP_SECRET")

    paths = build_paths(root, args.date, args.difficulty, args.article_type)

    log()
    log("=" * 70)
    log("748686 English Learning System")
    log("Feishu English Renderer V2.3")
    log("=" * 70)
    log(f"日期：{args.date}")
    log(f"难度：{args.difficulty}星")
    log(f"文体：{args.article_type}")
    log()

    if not paths["base"].is_dir():
        log(f"⚠️ 输出目录不存在：{paths['base']}")
        log("ℹ️ 当前日期没有英语学习输出")
        log("ℹ️ Feishu SKIP")
        return

    if not file_exists(paths["article"]):
        log(f"⚠️ 文章不存在：{paths['article']}")
        log("ℹ️ 当前日期无法发送英语学习内容")
        log("ℹ️ Feishu SKIP")
        return

    article_text = read_text(paths["article"])
    title = markdown_title(article_text)
    difficulty = extract_meta(article_text, "difficulty")
    level = extract_meta(article_text, "level")
    article_type = extract_meta(article_text, "article_type")
    article_body = extract_article_body(article_text)

    log(f"✓ 文章：{paths['article'].name}")

    article_sections = split_markdown_sections(article_body)
    english = article_sections.get("english", "") or article_body

    highlight_words = extract_highlight_words(english)
    vocabulary_items = extract_vocabulary_items(
        article_sections.get("vocabulary", "")
    )

    for item in vocabulary_items:
        word = item.get("word", "").strip()
        if word and word.casefold() not in {w.casefold() for w in highlight_words}:
            highlight_words.append(word)

    # 读取本次指定日期的新学单词，而不是依赖运行当天的系统日期
    input_file = find_input_file(root, args.date)
    input_words: list[str] = []

    if input_file:
        try:
            input_words = extract_input_words(read_text(input_file))
            log(f"✓ 当天新学单词文件：{input_file}")
            log(f"✓ Input 识别到新学单词：{len(input_words)} 个")
            log("   " + (", ".join(input_words) if input_words else "未识别到单词"))
        except Exception as exc:
            log(f"⚠️ 读取新学单词文件失败：{input_file}")
            log(f"   原因：{exc}")
    else:
        log("⚠️ 没有找到当天 Input 文件。已检查 input/Input/INPUT/输入 目录。")
        log(f"   目标日期：{args.date}")

    all_highlight_words = list(highlight_words)
    for word in input_words:
        if word.casefold() not in {w.casefold() for w in all_highlight_words}:
            all_highlight_words.append(word)

    occurrences = count_word_occurrences(english, input_words)

    log(f"✓ 英文正文段落：{len(paragraph_list(english))}")
    log(f"✓ 中文翻译：{'有' if article_sections.get('translation') else '无'}")
    log(f"✓ 重点词汇：{len(vocabulary_items)}")
    log(f"✓ 原文章重点高亮词：{len(highlight_words)}")
    log(f"✓ 合并后的高亮词：{len(all_highlight_words)}")
    log(f"✓ Input 新学单词在正文中的命中种类：{len(occurrences)}")

    if occurrences:
        for word, count in occurrences.items():
            log(f"   命中：{word} × {count}")
    elif input_words:
        log("⚠️ Input 单词未在英文正文中匹配到；请核对单词拼写和文章内容。")

    exam_text = ""
    question_counts: dict[str, int] = {}

    if file_exists(paths["exam"]):
        exam_text = read_text(paths["exam"])
        question_counts = count_questions(exam_text)
        log(f"✓ 试卷：{paths['exam'].name}")
    else:
        log("ℹ️ 没有试卷")

    answers_exists = file_exists(paths["answers"])
    log(f"✓ 答案解析：{paths['answers'].name}" if answers_exists else "ℹ️ 没有答案与解析")

    image_path: Path | None = paths["image"] if paths["image"].is_file() else None
    log(f"✓ 配图：{image_path.name}" if image_path else "ℹ️ 没有配图")

    audio_files = discover_audio_files(paths["listening_dir"])
    log(f"✓ 音频：{len(audio_files)} 个" if audio_files else "ℹ️ 没有听力文件")

    article_url = github_file_url(paths["article"])
    exam_url = github_file_url(paths["exam"]) if paths["exam"].is_file() else None
    answers_url = github_file_url(paths["answers"]) if answers_exists else None

    client = FeishuClient(app_id, app_secret, webhook)

    image_key = client.upload_image(image_path) if image_path else None

    log()
    log("→ 发送英语学习中心")

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
    client.send_card(home_card)
    log("✓ 学习中心已发送")

    log("→ 生成精读文章卡片 V2.3")

    article_card = make_article_card(
        title=title,
        article_body=article_body,
        image_key=image_key,
        difficulty=difficulty,
        article_type=article_type,
        article_url=article_url,
        input_words=input_words,
    )

    # 控制台打印最终卡片中实际发送的英文正文 Markdown
    log()
    log("=" * 70)
    log("FINAL ENGLISH ARTICLE MARKDOWN")
    log("=" * 70)

    for element in article_card.get("elements", []):
        if element.get("tag") != "div":
            continue

        text_obj = element.get("text", {})
        content = text_obj.get("content", "")
        if not content:
            continue

        if "English Article" in content:
            continue

        # 打印文章正文的段落；诊断区也会在卡片中显示
        if "<font color='blue'>" in content:
            log(content)
    log("=" * 70)
    log()

    client.send_card(article_card)
    log("✓ 精读文章 V2.3 已发送")

    if paths["exam"].is_file():
        log("→ 发送考试卡片")
        client.send_card(
            make_exam_card(title, question_counts, exam_url, answers_url)
        )
        log("✓ 考试卡片已发送")
    else:
        log("ℹ️ 没有试卷，跳过考试卡片")

    if audio_files:
        log("→ 发送听力卡片")
        client.send_card(make_listening_card(title, audio_files))
        log("✓ 听力卡片已发送")
    else:
        log("ℹ️ 没有听力，跳过听力卡片")

    log()
    log("=" * 70)
    log("✓ Feishu English Renderer V2.3 完成")
    log("✓ Input 新学单词已接入正文高亮流程")
    log("✓ 新学单词格式：**<font color='blue'>word</font>**")
    log("✓ 保留文章、配图、试卷、答案、听力和原文按钮")
    log("=" * 70)


# ============================================================
# 参数
# ============================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="748686 English Learning Feishu Renderer V2.3"
    )
    parser.add_argument("--date", required=True, help="目标日期，例如 2026-10-02")
    parser.add_argument("--difficulty", required=True, help="难度，例如 1")
    parser.add_argument("--article-type", required=True, help="文章类型，例如 议论文")
    parser.add_argument("--repo-root", default=".", help="仓库根目录")
    return parser.parse_args()


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":
    try:
        run(parse_args())
    except KeyboardInterrupt:
        log("用户中断")
        sys.exit(130)
    except Exception as exc:
        log()
        log("=" * 70)
        log("❌ Feishu English Renderer FAILED")
        log("=" * 70)
        log(str(exc))
        sys.exit(1)
