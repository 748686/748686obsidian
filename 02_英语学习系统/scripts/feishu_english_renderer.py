#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu English Renderer V1.0

职责：
1. 读取指定日期的英语学习输出
2. 读取文章
3. 读取配图
4. 读取试卷
5. 读取答案与解析
6. 读取听力文件
7. 上传图片 / 文件到飞书
8. 发送精美英语学习中心卡片

注意：
- 不修改 main.py
- 不修改 exam_generate.py
- 不修改 exam_answers.py
- 不修改 knowledge_image.py
- 不修改 audio_generate.py
- 本程序只负责 Feishu 展示层
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
from pathlib import Path
from typing import Any

import requests


# ============================================================
# 常量
# ============================================================

FEISHU_BASE = "https://open.feishu.cn"

TOKEN_URL = (
    f"{FEISHU_BASE}/open-apis/auth/v3/"
    "tenant_access_token/internal"
)

MESSAGE_URL = (
    f"{FEISHU_BASE}/open-apis/im/v1/messages"
)

IMAGE_UPLOAD_URL = (
    f"{FEISHU_BASE}/open-apis/im/v1/images"
)

FILE_UPLOAD_URL = (
    f"{FEISHU_BASE}/open-apis/im/v1/files"
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
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    if len(text) <= max_length:
        return text

    return text[:max_length].rstrip() + "\n..."


def markdown_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)

    if match:
        title = match.group(1).strip()

        title = title.replace("｜答案与解析", "")
        title = title.replace("｜答案", "")
        title = title.replace("｜试卷", "")

        return title.strip()

    return "English Learning"


def extract_meta(text: str, key: str) -> str:
    patterns = {
        "difficulty": [
            r"难度：([^｜\n]+)",
            r"难度：([^\n]+)",
        ],
        "level": [
            r"级别：([^｜\n]+)",
            r"小学[^\n]+年级",
        ],
        "article_type": [
            r"文章类型：([^｜\n]+)",
            r"文体：([^｜\n]+)",
        ],
        "score": [
            r"总分：([^\n]+)",
        ],
    }

    for pattern in patterns.get(key, []):
        match = re.search(pattern, text)

        if match:
            return match.group(1).strip()

    return ""


# ============================================================
# Feishu API
# ============================================================

class FeishuClient:

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        chat_id: str,
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.chat_id = chat_id
        self.session = requests.Session()
        self._token: str | None = None

    # --------------------------------------------------------
    # Token
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
                + json.dumps(data, ensure_ascii=False)
            )

        token = data.get("tenant_access_token")

        if not token:
            fail("Feishu 返回结果中没有 tenant_access_token")

        self._token = token

        return token

    def headers(self) -> dict[str, str]:
        return {
            "Authorization": (
                f"Bearer {self.tenant_access_token()}"
            )
        }

    # --------------------------------------------------------
    # 上传图片
    # --------------------------------------------------------

    def upload_image(self, path: Path) -> str:

        log(f"   ↑ 上传图片：{path.name}")

        with path.open("rb") as fp:

            response = self.session.post(
                IMAGE_UPLOAD_URL,
                headers=self.headers(),
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
                + json.dumps(data, ensure_ascii=False)
            )

        image_key = data.get("data", {}).get("image_key")

        if not image_key:
            fail("Feishu 图片上传成功，但没有返回 image_key")

        log(f"   ✓ image_key: {image_key}")

        return image_key

    # --------------------------------------------------------
    # 上传文件
    # --------------------------------------------------------

    def upload_file(self, path: Path) -> str:

        log(f"   ↑ 上传文件：{path.name}")

        file_type = self._detect_file_type(path)

        mime_type = (
            mimetypes.guess_type(path.name)[0]
            or "application/octet-stream"
        )

        with path.open("rb") as fp:

            response = self.session.post(
                FILE_UPLOAD_URL,
                headers=self.headers(),
                data={
                    "file_type": file_type,
                    "file_name": path.name,
                },
                files={
                    "file": (
                        path.name,
                        fp,
                        mime_type,
                    )
                },
                timeout=180,
            )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:
            fail(
                "上传 Feishu 文件失败："
                + json.dumps(data, ensure_ascii=False)
            )

        file_key = data.get("data", {}).get("file_key")

        if not file_key:
            fail("Feishu 文件上传成功，但没有返回 file_key")

        log(f"   ✓ file_key: {file_key}")

        return file_key

    @staticmethod
    def _detect_file_type(path: Path) -> str:

        suffix = path.suffix.lower()

        if suffix in {".mp3", ".wav", ".m4a", ".aac", ".flac"}:
            return "mp3" if suffix == ".mp3" else suffix.lstrip(".")

        if suffix in {".pdf"}:
            return "pdf"

        if suffix in {".doc", ".docx"}:
            return "doc"

        if suffix in {".xls", ".xlsx"}:
            return "xls"

        if suffix in {".ppt", ".pptx"}:
            return "ppt"

        if suffix in {".txt", ".md"}:
            return "txt"

        if suffix in {".zip"}:
            return "zip"

        return "stream"

    # --------------------------------------------------------
    # 发送消息
    # --------------------------------------------------------

    def send_message(
        self,
        msg_type: str,
        content: dict[str, Any],
    ) -> dict[str, Any]:

        params = {
            "receive_id_type": "chat_id",
        }

        payload = {
            "receive_id": self.chat_id,
            "msg_type": msg_type,
            "content": json.dumps(
                content,
                ensure_ascii=False,
            ),
        }

        response = self.session.post(
            MESSAGE_URL,
            params=params,
            headers={
                **self.headers(),
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:
            fail(
                "发送 Feishu 消息失败："
                + json.dumps(data, ensure_ascii=False)
            )

        return data

    def send_card(
        self,
        card: dict[str, Any],
    ) -> dict[str, Any]:

        return self.send_message(
            "interactive",
            card,
        )

    def send_file_message(
        self,
        file_key: str,
    ) -> dict[str, Any]:

        return self.send_message(
            "file",
            {
                "file_key": file_key,
            },
        )

    def send_audio_message(
        self,
        file_key: str,
    ) -> dict[str, Any]:

        return self.send_message(
            "audio",
            {
                "file_key": file_key,
            },
        )


# ============================================================
# Markdown / 内容分析
# ============================================================

def count_questions(
    exam_text: str,
) -> dict[str, int]:

    sections = {
        "听力": 0,
        "单项选择": 0,
        "多选题": 0,
        "完形填空": 0,
        "阅读理解": 0,
        "翻译": 0,
        "写作": 0,
    }

    for section in sections:

        match = re.search(
            rf"#{1,6}\s*[^#\n]*{re.escape(section)}[^#\n]*\n"
            rf"([\s\S]*?)(?=\n#{1,6}\s|\Z)",
            exam_text,
            re.IGNORECASE,
        )

        if not match:
            continue

        body = match.group(1)

        numbers = re.findall(
            r"^###?\s*(\d+)\.",
            body,
            re.MULTILINE,
        )

        if numbers:
            sections[section] = len(set(numbers))

    return sections


def extract_article_body(
    article_text: str,
) -> str:

    text = article_text.strip()

    # 删除 YAML front matter
    if text.startswith("---"):
        parts = text.split("---", 2)

        if len(parts) == 3:
            text = parts[2].strip()

    # 删除一级标题
    text = re.sub(
        r"^#\s+.+$\n?",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    return text.strip()


# ============================================================
# 卡片生成
# ============================================================

def make_button(
    text: str,
    value: str,
    button_type: str = "default",
) -> dict[str, Any]:

    return {
        "tag": "button",
        "text": {
            "tag": "plain_text",
            "content": text,
        },
        "type": button_type,
        "value": {
            "action": value,
        },
    }


def make_home_card(
    title: str,
    difficulty: str,
    level: str,
    article_type: str,
    image_key: str | None,
    question_counts: dict[str, int],
) -> dict[str, Any]:

    total_questions = sum(question_counts.values())

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

    elements.extend(
        [
            {
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
            },
            {
                "tag": "hr",
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "**今天的学习内容**\n\n"
                        "📖 精读文章\n"
                        "📝 综合试卷\n"
                        "🎧 听力训练\n"
                        "💡 词汇、语法与阅读分析"
                    ),
                },
            },
            {
                "tag": "action",
                "actions": [
                    make_button(
                        "📖 开始阅读",
                        "read_article",
                        "primary",
                    ),
                    make_button(
                        "📝 开始答题",
                        "start_exam",
                    ),
                ],
            },
            {
                "tag": "action",
                "actions": [
                    make_button(
                        "🎧 听力训练",
                        "listening",
                    ),
                    make_button(
                        "📎 学习文件",
                        "files",
                    ),
                ],
            },
        ]
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
                "content": "📚 748686 English Learning",
            },
        },
        "elements": elements,
    }


def make_article_card(
    title: str,
    article_body: str,
    image_key: str | None,
    difficulty: str,
    article_type: str,
) -> dict[str, Any]:

    preview = compact(
        article_body,
        3500,
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

    elements.extend(
        [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        f"**{title}**\n\n"
                        f"⭐ {difficulty or '—'}　"
                        f"📖 {article_type or '—'}"
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
                    "content": preview,
                },
            },
            {
                "tag": "hr",
            },
            {
                "tag": "action",
                "actions": [
                    make_button(
                        "📝 开始答题",
                        "start_exam",
                        "primary",
                    ),
                    make_button(
                        "🎧 听力训练",
                        "listening",
                    ),
                ],
            },
        ]
    )

    return {
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "template": "blue",
            "title": {
                "tag": "plain_text",
                "content": "📖 Article",
            },
        },
        "elements": elements,
    }


def make_exam_card(
    title: str,
    counts: dict[str, int],
) -> dict[str, Any]:

    rows = []

    display_names = [
        ("听力", "🎧"),
        ("单项选择", "🔤"),
        ("多选题", "☑️"),
        ("完形填空", "🧩"),
        ("阅读理解", "📖"),
        ("翻译", "🌐"),
        ("写作", "✍️"),
    ]

    for name, icon in display_names:

        count = counts.get(name, 0)

        if count:
            rows.append(
                f"{icon} **{name}：** {count}题"
            )

    content = (
        f"**{title}**\n\n"
        "📝 **综合英语试卷**\n\n"
        + "\n".join(rows)
        + "\n\n"
        "⚠️ 答题过程中不会显示正确答案。\n"
        "提交整张试卷后统一评分并查看解析。"
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
        "elements": [
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
            {
                "tag": "action",
                "actions": [
                    make_button(
                        "📝 开始考试",
                        "start_exam",
                        "primary",
                    ),
                ],
            },
        ],
    }


def make_listening_card(
    title: str,
    audio_files: list[tuple[str, str]],
) -> dict[str, Any]:

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**{title}**\n\n"
                    "🎧 请按 Part A → Part B → Part C "
                    "完成听力训练。"
                ),
            },
        },
        {
            "tag": "hr",
        },
    ]

    for label, filename in audio_files:

        elements.append(
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"🎧 **{label}**\n`{filename}`",
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
# 主流程
# ============================================================

def find_first(
    directory: Path,
    patterns: list[str],
) -> Path | None:

    for pattern in patterns:

        matches = sorted(
            directory.glob(pattern)
        )

        if matches:
            return matches[0]

    return None


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
            / f"{difficulty}星_{article_type}_文章.md"
        ),

        "exam": (
            base
            / "配套试卷"
            / f"{difficulty}星_{article_type}_试卷.md"
        ),

        "answers": (
            base
            / "配套试卷"
            / f"{difficulty}星_{article_type}_答案与解析.md"
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


def run(args: argparse.Namespace) -> None:

    root = Path(args.repo_root).resolve()

    app_id = os.getenv("FEISHU_APP_ID", "").strip()
    app_secret = os.getenv("FEISHU_APP_SECRET", "").strip()
    chat_id = os.getenv("FEISHU_CHAT_ID", "").strip()

    if not app_id:
        fail("缺少环境变量 FEISHU_APP_ID")

    if not app_secret:
        fail("缺少环境变量 FEISHU_APP_SECRET")

    if not chat_id:
        fail(
            "缺少环境变量 FEISHU_CHAT_ID。"
            "请填写目标飞书群的 chat_id。"
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
    log("Feishu English Renderer V1.0")
    log("=" * 70)
    log(f"日期：{args.date}")
    log(f"难度：{args.difficulty}星")
    log(f"文体：{args.article_type}")
    log()

    if not paths["base"].is_dir():
        fail(
            f"输出目录不存在：{paths['base']}"
        )

    # --------------------------------------------------------
    # 读取文章
    # --------------------------------------------------------

    if not file_exists(paths["article"]):
        fail(
            f"文章不存在：{paths['article']}"
        )

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

    log(f"✓ 文章：{paths['article'].name}")

    # --------------------------------------------------------
    # 试卷
    # --------------------------------------------------------

    if not file_exists(paths["exam"]):
        fail(
            f"试卷不存在：{paths['exam']}"
        )

    exam_text = read_text(
        paths["exam"]
    )

    question_counts = count_questions(
        exam_text
    )

    log(f"✓ 试卷：{paths['exam'].name}")

    # --------------------------------------------------------
    # 答案
    # --------------------------------------------------------

    if not file_exists(paths["answers"]):
        fail(
            f"答案与解析不存在：{paths['answers']}"
        )

    log(
        f"✓ 答案解析："
        f"{paths['answers'].name}"
    )

    # --------------------------------------------------------
    # 图片
    # --------------------------------------------------------

    image_path = paths["image"]

    if image_path.is_file():
        log(f"✓ 配图：{image_path.name}")
    else:
        image_path = None
        log("⚠️ 配图不存在，将发送无图版本")

    # --------------------------------------------------------
    # 音频
    # --------------------------------------------------------

    audio_files = discover_audio_files(
        paths["listening_dir"]
    )

    if audio_files:
        log(
            f"✓ 音频：{len(audio_files)} 个"
        )
    else:
        log("⚠️ 未找到听力文件")

    # --------------------------------------------------------
    # Feishu
    # --------------------------------------------------------

    client = FeishuClient(
        app_id=app_id,
        app_secret=app_secret,
        chat_id=chat_id,
    )

    image_key = None

    if image_path:
        image_key = client.upload_image(
            image_path
        )

    # --------------------------------------------------------
    # 发送学习中心
    # --------------------------------------------------------

    log()
    log("→ 发送学习中心卡片")

    home_card = make_home_card(
        title=title,
        difficulty=difficulty,
        level=level,
        article_type=article_type,
        image_key=image_key,
        question_counts=question_counts,
    )

    client.send_card(
        home_card
    )

    log("✓ 学习中心已发送")

    # --------------------------------------------------------
    # 发送文章卡片
    # --------------------------------------------------------

    log("→ 发送文章卡片")

    article_card = make_article_card(
        title=title,
        article_body=article_body,
        image_key=image_key,
        difficulty=difficulty,
        article_type=article_type,
    )

    client.send_card(
        article_card
    )

    log("✓ 文章卡片已发送")

    # --------------------------------------------------------
    # 发送考试卡片
    # --------------------------------------------------------

    log("→ 发送考试卡片")

    exam_card = make_exam_card(
        title=title,
        counts=question_counts,
    )

    client.send_card(
        exam_card
    )

    log("✓ 考试卡片已发送")

    # --------------------------------------------------------
    # 上传原始文件
    # --------------------------------------------------------

    log()
    log("→ 上传原始学习文件")

    upload_files = [
        paths["article"],
        paths["exam"],
        paths["answers"],
    ]

    if image_path:
        upload_files.append(
            image_path
        )

    upload_files.extend(
        audio_files
    )

    uploaded_count = 0

    for path in upload_files:

        try:

            file_key = client.upload_file(
                path
            )

            client.send_file_message(
                file_key
            )

            uploaded_count += 1

        except Exception as exc:

            log(
                f"⚠️ 文件发送失败："
                f"{path.name} | {exc}"
            )

    # --------------------------------------------------------
    # 结束
    # --------------------------------------------------------

    log()
    log("=" * 70)
    log("✓ Feishu English Renderer 完成")
    log(f"   文件发送：{uploaded_count}/{len(upload_files)}")
    log("=" * 70)


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "748686 English Learning "
            "Feishu Renderer"
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


if __name__ == "__main__":

    try:
        run(
            parse_args()
        )

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
