#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import time

from common import CONFIG, env_required, request_json


# ============================================================
# 难度
# ============================================================

DIFFICULTIES = {
    i: f"{i}星"
    for i in range(1, 18)
}


# ============================================================
# 文体
# ============================================================

ARTICLE_TYPES = {
    "narration": "记叙文",
    "argumentation": "议论文",
    "exposition": "说明文",
    "description": "描写文",
    "letter": "应用文-书信",
    "diary": "应用文-日记",
    "notice": "应用文-通知",
    "poster": "应用文-海报",
    "speech": "应用文-演讲稿",
    "prose": "散文",
    "science": "科技文",
    "news": "新闻报道",
    "review": "评论文",
    "story": "故事",
    "comparison": "对比文",
    "fairy_tale": "童话故事",
    "interview": "采访",
}


# ============================================================
# JSON 最大重试次数
# ============================================================

JSON_RETRIES = 3


# ============================================================
# 清理模型返回内容
# ============================================================

def clean_json_content(content: str) -> str:
    """
    清理 Agnes 返回的 JSON 文本。

    处理：
        ```json
        {...}
        ```

    以及普通 ``` 包裹。

    同时去除 JSON 前后的说明文字。
    """

    if not isinstance(content, str):
        raise ValueError(
            f"模型返回内容不是字符串：{type(content).__name__}"
        )

    text = content.strip()

    # --------------------------------------------------------
    # 去除 Markdown JSON 代码围栏
    # --------------------------------------------------------

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    # --------------------------------------------------------
    # 如果模型前面加了说明文字，
    # 尝试从第一个 { 开始截取。
    # --------------------------------------------------------

    first_brace = text.find("{")

    if first_brace > 0:
        text = text[first_brace:]

    # --------------------------------------------------------
    # 如果后面有多余文字，
    # 从最后一个 } 截断。
    # --------------------------------------------------------

    last_brace = text.rfind("}")

    if last_brace >= 0:
        text = text[:last_brace + 1]

    return text.strip()


# ============================================================
# 尝试解析 JSON
# ============================================================

def parse_json_response(content: str):
    """
    稳健解析 Agnes 返回的 JSON。

    第一层：
        标准 json.loads

    第二层：
        提取 JSON 主体后再解析

    解析失败时抛出异常，
    由上层负责重新请求。
    """

    cleaned = clean_json_content(content)

    # --------------------------------------------------------
    # 第一种：直接解析
    # --------------------------------------------------------

    try:
        result = json.loads(cleaned)

        if not isinstance(result, dict):
            raise ValueError(
                "模型返回的 JSON 不是对象。"
            )

        return result

    except json.JSONDecodeError as first_error:

        # ----------------------------------------------------
        # 第二种：进一步提取最外层 JSON
        # ----------------------------------------------------

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start >= 0 and end > start:

            candidate = cleaned[
                start:end + 1
            ]

            try:

                result = json.loads(
                    candidate
                )

                if not isinstance(
                    result,
                    dict
                ):
                    raise ValueError(
                        "模型返回的 JSON 不是对象。"
                    )

                return result

            except Exception:

                pass

        # ----------------------------------------------------
        # 最终失败
        # ----------------------------------------------------

        raise ValueError(
            "Agnes 返回内容不是合法 JSON。\n"
            f"JSON 错误：{first_error}\n"
            f"返回内容：\n{content}"
        )


# ============================================================
# 构造 JSON 修复请求
# ============================================================

def build_repair_payload(
    original_content: str
):
    """
    当 Agnes 第一次返回的 JSON 无法解析时，
    请求 Agnes 修复 JSON。

    注意：
    不重新生成文章内容，
    只修复 JSON 格式。
    """

    return {

        "model": CONFIG["agnes"]["model"],

        "temperature": 0,

        "messages": [

            {
                "role": "system",

                "content": (
                    "你是JSON修复器。"
                    "只输出一个合法JSON对象。"
                    "不要Markdown。"
                    "不要```。"
                    "不要解释。"
                    "不要增加任何字段。"
                    "保持原始内容和字段完全不变，"
                    "只修复JSON语法错误。"
                ),
            },

            {

                "role": "user",

                "content": (
                    "下面是一个JSON生成结果，"
                    "它存在JSON语法错误。\n\n"
                    "请修复它，使其成为严格合法的JSON。\n\n"
                    "原始内容：\n"
                    f"{original_content}"
                ),

            },

        ],

    }


# ============================================================
# 请求 Agnes
# ============================================================

def request_article(
    key,
    url,
    payload
):
    """
    请求 Agnes 生成文章。
    """

    return request_json(
        "POST",
        url,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
    )


# ============================================================
# 主生成函数
# ============================================================

def generate(
    words,
    difficulty,
    article_type,
    length
):

    # ========================================================
    # 基础检查
    # ========================================================

    if article_type not in ARTICLE_TYPES:

        raise ValueError(
            f"未知文章类型：{article_type}"
        )

    if difficulty not in DIFFICULTIES:

        raise ValueError(
            f"未知难度：{difficulty}"
        )

    # ========================================================
    # API
    # ========================================================

    key = env_required(
        CONFIG["agnes"]["api_key_env"]
    )

    url = (
        CONFIG["agnes"]["base_url"]
        .rstrip("/")
        + "/chat/completions"
    )

    # ========================================================
    # 任务
    # ========================================================

    task = {

        "task": "生成英语学习短文",

        "difficulty": (
            DIFFICULTIES[difficulty]
        ),

        "article_type": (
            ARTICLE_TYPES[article_type]
        ),

        "target_length": length,

        "words": words,

        "requirements": [

            "所有目标词必须以原形出现在英文文章中",

            "文体必须符合指定类型",

            "难度必须真实改变句法、逻辑、结构和词汇",

            "提供完整中文翻译",

            "短文中的重点短语和语法知识点必须真实存在于文章中",

        ],

        "schema": {

            "title": "string",

            "article_en": "string",

            "article_zh": "string",

            "added_vocabulary": "array",

            "phrases": "array",

            "grammar_points": "array",

            "knowledge_structure": "array",

        },

    }

    # ========================================================
    # 第一次请求
    # ========================================================

    payload = {

        "model": CONFIG["agnes"]["model"],

        "temperature": 0.4,

        "messages": [

            {

                "role": "system",

                "content": (
                    "你是严格的英语教材生成器。"
                    "只输出一个合法JSON对象。"
                    "不要Markdown代码围栏。"
                    "不要解释。"
                    "不要在JSON前后添加任何文字。"
                ),

            },

            {

                "role": "user",

                "content": json.dumps(
                    task,
                    ensure_ascii=False
                ),

            },

        ],

    }

    # ========================================================
    # JSON 解析循环
    # ========================================================

    last_content = ""

    last_error = None

    for attempt in range(
        1,
        JSON_RETRIES + 1
    ):

        print(
            f"📝 Agnes 文章生成 / JSON解析 "
            f"{attempt}/{JSON_RETRIES}",
            flush=True
        )

        try:

            data = request_article(
                key,
                url,
                payload
            )

            # ------------------------------------------------
            # 检查 choices
            # ------------------------------------------------

            if not isinstance(
                data,
                dict
            ):

                raise ValueError(
                    "Agnes API 返回不是 JSON 对象。"
                )

            choices = data.get(
                "choices"
            )

            if not choices:

                raise ValueError(
                    f"Agnes 返回中没有 choices：{data}"
                )

            message = choices[0].get(
                "message",
                {}
            )

            content = message.get(
                "content",
                ""
            )

            if not content:

                raise ValueError(
                    "Agnes 返回的 message.content 为空。"
                )

            last_content = content

            # ------------------------------------------------
            # 尝试解析
            # ------------------------------------------------

            result = parse_json_response(
                content
            )

            # ------------------------------------------------
            # 基础结构检查
            # ------------------------------------------------

            required_fields = [

                "title",

                "article_en",

                "article_zh",

                "added_vocabulary",

                "phrases",

                "grammar_points",

                "knowledge_structure",

            ]

            missing = [

                field

                for field in required_fields

                if field not in result

            ]

            if missing:

                raise ValueError(
                    "Agnes JSON 缺少字段："
                    + ", ".join(missing)
                )

            # ------------------------------------------------
            # 成功
            # ------------------------------------------------

            print(
                "✓ Agnes 文章 JSON 解析成功",
                flush=True
            )

            return result

        except Exception as e:

            last_error = e

            print(
                "",
                flush=True
            )

            print(
                "⚠️ 文章 JSON 解析失败",
                flush=True
            )

            print(
                f"   {type(e).__name__}: {e}",
                flush=True
            )

            # ------------------------------------------------
            # 最后一次不再修复
            # ------------------------------------------------

            if attempt >= JSON_RETRIES:

                break

            # =================================================
            # 第二次：
            # 不重新生成，直接请求 Agnes 修复 JSON
            # =================================================

            if last_content:

                print(
                    "🔧 请求 Agnes 修复 JSON...",
                    flush=True
                )

                try:

                    repair_payload = (
                        build_repair_payload(
                            last_content
                        )
                    )

                    repair_data = request_article(
                        key,
                        url,
                        repair_payload
                    )

                    repair_choices = (
                        repair_data.get(
                            "choices"
                        )
                    )

                    if not repair_choices:

                        raise ValueError(
                            "JSON 修复请求没有返回 choices。"
                        )

                    repair_content = (
                        repair_choices[0]
                        .get("message", {})
                        .get("content", "")
                    )

                    if not repair_content:

                        raise ValueError(
                            "JSON 修复结果为空。"
                        )

                    result = parse_json_response(
                        repair_content
                    )

                    required_fields = [

                        "title",

                        "article_en",

                        "article_zh",

                        "added_vocabulary",

                        "phrases",

                        "grammar_points",

                        "knowledge_structure",

                    ]

                    missing = [

                        field

                        for field in required_fields

                        if field not in result

                    ]

                    if missing:

                        raise ValueError(
                            "修复后的 JSON 缺少字段："
                            + ", ".join(missing)
                        )

                    print(
                        "✓ Agnes JSON 修复成功",
                        flush=True
                    )

                    return result

                except Exception as repair_error:

                    print(
                        "⚠️ JSON 自动修复失败："
                        f"{type(repair_error).__name__}: "
                        f"{repair_error}",
                        flush=True
                    )

            # ------------------------------------------------
            # 等待后重新生成
            # ------------------------------------------------

            wait_seconds = (
                2 * attempt
            )

            print(
                f"⏳ {wait_seconds} 秒后重新请求 Agnes...",
                flush=True
            )

            time.sleep(
                wait_seconds
            )

    # ========================================================
    # 最终失败
    # ========================================================

    print(
        "",
        flush=True
    )

    print(
        "❌ Agnes 文章生成最终失败",
        flush=True
    )

    if last_error:

        print(
            f"错误：{last_error}",
            flush=True
        )

    # --------------------------------------------------------
    # 打印原始返回
    # --------------------------------------------------------

    if last_content:

        print(
            "",
            flush=True
        )

        print(
            "================ 原始 Agnes 返回 ================",
            flush=True
        )

        print(
            last_content,
            flush=True
        )

        print(
            "==================================================",
            flush=True
        )

    raise RuntimeError(
        "Agnes 文章 JSON 无法解析，"
        "已经达到最大重试次数。"
    )
