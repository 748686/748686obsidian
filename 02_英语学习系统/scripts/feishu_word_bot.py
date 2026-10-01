#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Word Image Bot V2.0

流程：
飞书图片 -> 立即回执 -> 下载 -> OCR -> 英中配对
-> 合并当天 input/YYYY-MM-DD.md -> git commit/push
-> 飞书报告结果

边界：
1. 只处理目标群 748686知识系统 的图片消息。
2. 只写入 02_英语学习系统/input/。
3. 不修改考试解析器、评分器、试卷生成器、文章生成器。
4. 使用 GitHub Actions 自带的 GITHUB_TOKEN 推送当前仓库。
5. 日期以 GitHub Actions Runner 的 UTC 日期为准。
6. 只有 push 成功，才回复“已录入正式仓库”。
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

# 单条消息的内存去重。仅用于同一次运行期间。
_processed_message_ids = set()
_processing_message_ids = set()
_message_lock = threading.Lock()

# Token 缓存
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
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[748686 FeishuWordBot V2.0] [{now}] {message}", flush=True)


# ============================================================
# 飞书 API
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
            json={"app_id": APP_ID, "app_secret": APP_SECRET},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("code") != 0 or not data.get("tenant_access_token"):
            raise RuntimeError(
                "获取飞书 Token 失败：" +
                json.dumps(data, ensure_ascii=False)[:2000]
            )

        _cached_token = data["tenant_access_token"]
        # Token 通常有较长有效期，提前 5 分钟刷新。
        _token_expiry = time.time() + max(
            60, int(data.get("expire", 7200)) - 300
        )

        return _cached_token


def find_target_chat(token):
    log(f"正在查找目标群：{TARGET_CHAT_NAME}")

    url = f"{FEISHU_BASE}/open-apis/im/v1/chats"
    headers = {"Authorization": f"Bearer {token}"}
    page_token = ""

    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token

        response = requests.get(
            url, headers=headers, params=params, timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if data.get("code") != 0:
            raise RuntimeError(
                "查询群列表失败：" +
                json.dumps(data, ensure_ascii=False)[:2000]
            )

        result = data.get("data", {})
        for chat in result.get("items", []):
            if chat.get("name") == TARGET_CHAT_NAME:
                chat_id = chat.get("chat_id")
                if not chat_id:
                    raise RuntimeError("找到目标群，但 chat_id 为空。")
                log(f"目标群已找到：{TARGET_CHAT_NAME}")
                return chat_id

        if not result.get("has_more"):
            break

        page_token = result.get("page_token", "")
        if not page_token:
            break

    raise RuntimeError(
        f"没有找到目标群「{TARGET_CHAT_NAME}」。"
        "请确认机器人已加入该群，并有读取群信息的权限。"
    )


def send_group_text(token, chat_id, text):
    """向目标群发送独立消息，避免依赖原消息的回复权限。"""
    url = f"{FEISHU_BASE}/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
    }

    response = requests.post(
        url,
        headers=headers,
        params={"receive_id_type": "chat_id"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != 0:
        raise RuntimeError(
            "发送群消息失败：" +
            json.dumps(data, ensure_ascii=False)[:2000]
        )


def reply_message(token, message_id, text):
    """优先回复原消息。"""
    url = f"{FEISHU_BASE}/open-apis/im/v1/messages/{message_id}/reply"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
    }

    response = requests.post(
        url, headers=headers, json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != 0:
        raise RuntimeError(
            "回复原消息失败：" +
            json.dumps(data, ensure_ascii=False)[:2000]
        )


def notify(message_id, chat_id, text):
    """优先回复原消息；回复失败时，尝试向目标群发消息。"""
    try:
        token = get_tenant_access_token()
        if message_id:
            reply_message(token, message_id, text)
        else:
            send_group_text(token, chat_id, text)
        log("飞书通知发送成功。")
        return True
    except Exception as exc:
        log(f"原消息回复失败：{type(exc).__name__}: {exc}")

    try:
        token = get_tenant_access_token(force_refresh=True)
        send_group_text(token, chat_id, text)
        log("已通过群消息方式发送通知。")
        return True
    except Exception as exc:
        log(f"群消息备用通知也失败：{type(exc).__name__}: {exc}")
        return False


def send_connection_card(token, chat_id):
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "green",
            "title": {
                "tag": "plain_text",
                "content": "🟢 748686 英语单词录入系统 V2.0",
            },
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "**飞书长连接已启动**\n\n"
                        "发送单词图片后，系统会立即回执，随后识别英文与中文，"
                        "追加到当天的 `02_英语学习系统/input/YYYY-MM-DD.md`，"
                        "并尝试提交、推送到 GitHub。\n\n"
                        "**只有 GitHub push 成功，才会报告录入成功。**"
                    ),
                },
            },
            {"tag": "hr"},
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": f"目标群：{TARGET_CHAT_NAME}",
                    }
                ],
            },
        ],
    }

    url = f"{FEISHU_BASE}/open-apis/im/v1/messages"
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        params={"receive_id_type": "chat_id"},
        json={
            "receive_id": chat_id,
            "msg_type": "interactive",
            "content": json.dumps(card, ensure_ascii=False),
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != 0:
        raise RuntimeError(
            "连接卡片发送失败：" +
            json.dumps(data, ensure_ascii=False)[:2000]
        )

    log("连接成功卡片已发送。")


def download_message_image(token, message_id, image_key, output_path):
    url = (
        f"{FEISHU_BASE}/open-apis/im/v1/messages/"
        f"{message_id}/resources/{image_key}"
    )
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params={"type": "image"},
        timeout=60,
    )
    response.raise_for_status()

    if not response.content:
        raise RuntimeError("飞书图片下载结果为空。")

    Path(output_path).write_bytes(response.content)
    log(f"图片下载完成：{Path(output_path).stat().st_size:,} bytes")


# ============================================================
# OCR
# ============================================================

def preprocess_image(image_path):
    with Image.open(image_path) as source:
        image = source.convert("RGB")

    log(f"原始图片尺寸：{image.width} × {image.height}")

    # 控制最大边，避免超大图片占用过多内存。
    max_side = 2600
    scale = min(2.0, max_side / max(image.width, image.height))
    if scale > 1:
        image = image.resize(
            (int(image.width * scale), int(image.height * scale))
        )

    image = image.convert("L")
    image = ImageEnhance.Contrast(image).enhance(1.5)
    return image.filter(ImageFilter.SHARPEN)


def run_ocr(image_path):
    log("开始执行 Tesseract OCR。")
    image = preprocess_image(image_path)

    text = pytesseract.image_to_string(
        image,
        lang="eng+chi_sim",
        config="--psm 6",
    )
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    log("OCR 执行完成。")
    log("========== OCR 原始结果开始 ==========")
    print(text, flush=True)
    log("========== OCR 原始结果结束 ==========")

    if not text.strip():
        raise RuntimeError(
            "OCR 没有提取到可读文字。请发送清晰、完整、文字未被遮挡的图片。"
        )

    return text


# ============================================================
# 英文与中文配对
# ============================================================

def clean_line(line):
    line = line.strip()
    line = re.sub(r"^[|¦•·▪●○◆◇]+\s*", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def has_chinese(text):
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def has_english(text):
    return bool(re.search(r"[A-Za-z]", text))


def looks_like_english(text):
    if not has_english(text):
        return False

    # 英文词条可以含空格、连字符、撇号、数字和常见标点。
    remaining = re.sub(r"[A-Za-z0-9\s'\-./()]+", "", text)
    if len(remaining) > 2:
        return False

    letters = len(re.findall(r"[A-Za-z]", text))
    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    return letters > 0 and chinese == 0


def clean_english(text):
    text = re.sub(r"^\s*\d+\s*[.)、-]\s*", "", text.strip())
    return text.strip(" \t:：—–-")


def clean_chinese(text):
    text = re.sub(r"^\s*\d+\s*[.)、-]\s*", "", text.strip())
    return text.strip(" \t:：—–-")


def parse_inline_pair(line):
    patterns = [
        r"^\s*\d*\s*[.)、-]?\s*"
        r"([A-Za-z][A-Za-z0-9\s'\-./()]*?)"
        r"\s*[—–−-]\s*([\u4e00-\u9fff].*)$",
        r"^\s*\d*\s*[.)、-]?\s*"
        r"([A-Za-z][A-Za-z0-9\s'\-./()]*?)"
        r"\s*[：:]\s*([\u4e00-\u9fff].*)$",
    ]

    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            english = clean_english(match.group(1))
            chinese = clean_chinese(match.group(2))
            if english and chinese:
                return {"english": english, "chinese": chinese}

    return None


def deduplicate_entries(entries):
    result = []
    seen = set()

    for item in entries:
        english = clean_english(item.get("english", ""))
        chinese = clean_chinese(item.get("chinese", ""))

        if not english or not chinese:
            continue
        if not has_english(english) or has_chinese(english):
            continue
        if not has_chinese(chinese):
            continue

        key = re.sub(r"\s+", " ", english).casefold()
        if key in seen:
            continue

        seen.add(key)
        result.append({"english": english, "chinese": chinese})

    return result


def parse_word_pairs(raw_text):
    lines = [clean_line(x) for x in raw_text.splitlines()]
    lines = [x for x in lines if x]
    entries = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 格式一：beautiful — 美丽的
        pair = parse_inline_pair(line)
        if pair:
            entries.append(pair)
            i += 1
            continue

        # 格式二：
        # beautiful
        # 美丽的
        if looks_like_english(line):
            english = clean_english(line)
            j = i + 1
            chinese_parts = []

            while j < len(lines):
                next_line = lines[j]

                if looks_like_english(next_line):
                    break

                if has_chinese(next_line):
                    # 不把混合大量英文的下一行直接当作中文释义。
                    if len(re.findall(r"[A-Za-z]", next_line)) > 4:
                        break
                    chinese_parts.append(clean_chinese(next_line))
                    j += 1
                    continue

                if re.fullmatch(
                    r"(n|v|adj|adv|prep|conj|pron|vt|vi|aux|modal)\.?",
                    next_line,
                    flags=re.IGNORECASE,
                ):
                    j += 1
                    continue

                break

            if chinese_parts:
                entries.append({
                    "english": english,
                    "chinese": " ".join(chinese_parts),
                })
                i = j
                continue

        i += 1

    return deduplicate_entries(entries)


# ============================================================
# Markdown：保留原文件，安全追加和去重
# ============================================================

def utc_date_string():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def parse_existing_entries(text):
    entries = []
    pattern = re.compile(
        r"^\s*\d+\.\s*(.+?)\s*[—–-]\s*([\u4e00-\u9fff].*?)\s*$"
    )

    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            english = clean_english(match.group(1))
            chinese = clean_chinese(match.group(2))
            if english and chinese:
                entries.append({
                    "english": english,
                    "chinese": chinese,
                })

    return entries


def build_daily_markdown(date_string, new_entries):
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = INPUT_DIR / f"{date_string}.md"

    if output_path.exists():
        old_text = output_path.read_text(encoding="utf-8")
        old_entries = parse_existing_entries(old_text)
        log(f"当天文件已存在，读取原有词条：{len(old_entries)} 个")
    else:
        old_text = ""
        old_entries = []
        log("当天文件不存在，将创建新文件。")

    merged = list(old_entries)
    seen = {
        re.sub(r"\s+", " ", item["english"]).casefold()
        for item in old_entries
    }

    added = []
    for item in new_entries:
        key = re.sub(r"\s+", " ", item["english"]).casefold()
        if key in seen:
            log(f"跳过当天已存在的单词：{item['english']}")
            continue
        seen.add(key)
        merged.append(item)
        added.append(item)

    # 维持原系统约定的简单格式。
    lines = ["# 今日新词", ""]
    for index, item in enumerate(merged, start=1):
        lines.append(f"{index}. {item['english']} — {item['chinese']}")
    lines.append("")

    new_text = "\n".join(lines)

    if new_text != old_text:
        output_path.write_text(new_text, encoding="utf-8")
        log(f"Markdown 已写入：{output_path}")
    else:
        log("文件内容没有变化，无需改写。")

    return output_path, merged, added


# ============================================================
# GitHub commit / push
# ============================================================

def run_git(args, check=True):
    command = ["git"] + list(args)
    log("$ " + " ".join(command))

    result = subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if result.stdout:
        print(result.stdout, flush=True)

    if check and result.returncode != 0:
        raise RuntimeError(
            f"Git 命令失败（退出码 {result.returncode}）："
            + " ".join(command)
        )

    return result


def git_commit_and_push(output_path):
    if not GITHUB_REPOSITORY:
        raise RuntimeError(
            "缺少 GITHUB_REPOSITORY，无法确认当前仓库。"
        )

    branch = GITHUB_REF_NAME
    if not branch:
        raise RuntimeError(
            "缺少 GITHUB_REF_NAME。请从仓库默认分支手动启动工作流。"
        )

    relative_path = output_path.relative_to(REPO_ROOT).as_posix()

    run_git(["config", "user.name", "github-actions[bot]"])
    run_git([
        "config", "user.email",
        "41898282+github-actions[bot]@users.noreply.github.com",
    ])

    run_git(["add", "--", relative_path])

    staged = run_git(["diff", "--cached", "--quiet"], check=False)
    if staged.returncode == 0:
        log("没有新的 Git 变更，无需提交。")
        return False

    if staged.returncode != 1:
        raise RuntimeError("无法检查暂存区状态。")

    run_git([
        "commit",
        "-m",
        f"Add daily English vocabulary {output_path.stem}",
    ])

    # 如果远端有并发更新，先尝试 rebase，避免直接覆盖远端提交。
    last_error = None
    for attempt in range(1, 4):
        log(f"准备推送 GitHub（第 {attempt}/3 次）。")

        pull = run_git(
            ["pull", "--rebase", "origin", branch],
            check=False,
        )
        if pull.returncode != 0:
            run_git(["rebase", "--abort"], check=False)
            last_error = "git pull --rebase 失败，可能存在同一文件并发冲突。"
            log(last_error)
            break

        push = run_git(["push", "origin", f"HEAD:{branch}"], check=False)
        if push.returncode == 0:
            log("GitHub push 成功。")
            return True

        last_error = "git push 失败。"
        log(last_error)

    raise RuntimeError(
        (last_error or "GitHub 推送失败。")
        + "请检查 Actions 的 contents: write 权限、分支保护规则和并发提交冲突。"
    )


# ============================================================
# 图片处理
# ============================================================

def get_message_field(message, field, default=None):
    """兼容 SDK 对象字段缺失或字段值为空的情况。"""
    try:
        value = getattr(message, field)
        return default if value is None else value
    except Exception:
        return default


def process_image_message(event_data, target_chat_id):
    event = getattr(event_data, "event", None)
    message = getattr(event, "message", None) if event else None

    if message is None:
        log("收到事件，但没有 event.message。")
        return

    message_id = get_message_field(message, "message_id", "")
    message_type = get_message_field(message, "message_type", "")
    chat_id = get_message_field(message, "chat_id", "")
    content = get_message_field(message, "content", "{}")

    log("=" * 65)
    log(f"收到消息事件：message_id={message_id}")
    log(f"message_type={message_type}, chat_id={chat_id}")
    log("=" * 65)

    if not message_id:
        log("消息没有 message_id，无法处理。")
        return

    # 只处理目标群，避免处理其他群的消息。
    if chat_id and target_chat_id and chat_id != target_chat_id:
        log("消息来自非目标群，忽略。")
        return

    if message_type != "image":
        log("收到非图片消息，忽略。")
        return

    with _message_lock:
        if message_id in _processed_message_ids:
            log("检测到重复消息，跳过。")
            return
        if message_id in _processing_message_ids:
            log("该图片正在处理中，跳过重复事件。")
            return
        _processing_message_ids.add(message_id)

    # 先发回执，避免用户等待期间没有反馈。
    notify(
        message_id,
        target_chat_id,
        "📥 已收到单词图片，正在下载并识别英文和中文，请稍候……",
    )

    try:
        try:
            content_data = json.loads(content or "{}")
        except Exception as exc:
            raise RuntimeError(f"图片消息 content 不是有效 JSON：{exc}")

        image_key = content_data.get("image_key")
        if not image_key:
            raise RuntimeError("图片消息中没有 image_key。")

        token = get_tenant_access_token()

        with tempfile.TemporaryDirectory(prefix="748686_word_") as temp_dir:
            image_path = Path(temp_dir) / "word_image.png"

            download_message_image(
                token=token,
                message_id=message_id,
                image_key=image_key,
                output_path=image_path,
            )

            raw_text = run_ocr(image_path)
            entries = parse_word_pairs(raw_text)

            log(f"OCR 成功配对：{len(entries)} 个词条。")

            if not entries:
                raise RuntimeError(
                    "图片中没有识别出可靠的英文—中文配对。"
                    "没有写入文件，也没有推送 GitHub。"
                    "请发送更清晰的图片，最好每行一个“英文 — 中文”。"
                )

            date_string = utc_date_string()
            output_path, merged, added = build_daily_markdown(
                date_string, entries
            )

            if not added:
                # 当天词条均已存在，不做空提交。
                log("本次没有新增词条。")
                notify(
                    message_id,
                    target_chat_id,
                    f"ℹ️ 图片识别完成，但没有新增单词。\n"
                    f"本次识别 {len(entries)} 个词条，全部已存在于 "
                    f"`input/{date_string}.md`，没有重复录入。",
                )
                _processed_message_ids.add(message_id)
                return

            log("开始提交并推送 GitHub。")
            git_commit_and_push(output_path)

            # push 成功之后才发送成功消息。
            preview = "\n".join(
                f"{i}. {item['english']} — {item['chinese']}"
                for i, item in enumerate(added, start=1)
            )

            success_text = (
                f"✅ 单词图片已处理并成功推送到 GitHub！\n\n"
                f"日期：{date_string}（UTC）\n"
                f"文件：`02_英语学习系统/input/{date_string}.md`\n"
                f"本次新增：{len(added)} 个单词\n"
                f"当天累计：{len(merged)} 个单词\n\n"
                f"新增词条：\n{preview}\n\n"
                f"现在可以启动英语学习系统学习今天的新词了。"
            )

            notify(message_id, target_chat_id, success_text)
            _processed_message_ids.add(message_id)

    except Exception as exc:
        log(f"图片处理失败：{type(exc).__name__}: {exc}")
        notify(
            message_id,
            target_chat_id,
            "❌ 图片处理未完成。\n\n"
            f"失败阶段或原因：{type(exc).__name__}: {exc}\n\n"
            "系统没有报告本次录入成功。请查看 GitHub Actions 日志。",
        )

    finally:
        with _message_lock:
            _processing_message_ids.discard(message_id)


# ============================================================
# 飞书事件回调
# ============================================================

def make_handler(target_chat_id):
    def handle_message(data):
        try:
            process_image_message(data, target_chat_id)
        except Exception as exc:
            log(f"事件回调异常：{type(exc).__name__}: {exc}")
    return handle_message


# ============================================================
# 主程序
# ============================================================

def main():
    log("=" * 65)
    log("748686 飞书新学单词机器人 V2.0")
    log("模式：长连接 -> 图片 -> OCR -> 日期 MD -> GitHub push")
    log(f"目标群：{TARGET_CHAT_NAME}")
    log(f"仓库根目录：{REPO_ROOT}")
    log(f"输入目录：{INPUT_DIR}")
    log(f"GitHub 仓库：{GITHUB_REPOSITORY or '(未设置)'}")
    log(f"GitHub 分支：{GITHUB_REF_NAME or '(未设置)'}")
    log("=" * 65)

    if not GITHUB_REPOSITORY:
        raise RuntimeError(
            "GITHUB_REPOSITORY 未设置。请从 GitHub Actions 工作流运行。"
        )
    if not GITHUB_REF_NAME:
        raise RuntimeError(
            "GITHUB_REF_NAME 未设置。请从仓库分支手动启动工作流。"
        )

    token = get_tenant_access_token()
    log("tenant_access_token 获取成功。")

    target_chat_id = find_target_chat(token)
    send_connection_card(token, target_chat_id)

    event_handler = (
        lark.EventDispatcherHandler.builder("", "", lark.LogLevel.INFO)
        .register_p2_im_message_receive_v1(
            make_handler(target_chat_id)
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

    log("🟢 准备启动飞书 WebSocket 长连接。")
    log("收到任何消息事件时，日志会出现“收到消息事件”。")
    log("📷 现在可以在目标群发送单词图片。")
    ws_client.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("机器人收到停止信号。")
    except Exception as exc:
        log(f"程序启动失败：{type(exc).__name__}: {exc}")
        sys.exit(1)
