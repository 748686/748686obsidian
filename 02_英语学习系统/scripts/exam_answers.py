#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Exam Answers / Analysis Generator V2.4

======================================================================
职责
======================================================================

本文件只负责：

    1. 根据已经生成好的英语试卷生成答案
    2. 生成每一道题的详细解析
    3. 生成听力原文
    4. 生成总体学习分析

======================================================================
V2.4 修复
======================================================================

1. 修复多选题答案被强制要求至少两个选项的问题

   原 V2.3：
       多选题必须至少有两个正确答案

   V2.4：
       多选题答案数量完全依据原题实际内容判断。

       可以是：

           ["A"]

       也可以是：

           ["A", "C"]

           ["A", "B", "D"]

       不允许为了满足“多选题”而强行增加错误选项。

2. 多选题答案仍然必须：

       - 是数组
       - 至少包含一个答案
       - 只能使用 A / B / C / D
       - 不允许重复

3. 保留 V2.2 对旧版答案文件的兼容逻辑

4. 保留 14 个独立模块

5. 保留分块生成 + 独立重试机制

6. 保留已经成功生成的模块，不因为后续模块失败而重新生成

7. 不修改试卷本身

8. 不修改 Stage 2 Markdown → exam_data 恢复逻辑

======================================================================
"""

import json
import os
import re
import sys
import time
import random
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# 基础路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_DIR = SCRIPT_DIR.parent

PROJECT_ROOT = SYSTEM_DIR.parent


# ======================================================================
# 配置
# ======================================================================

SETTINGS_FILE = SYSTEM_DIR / "settings.json"

DEFAULT_API_BASE_URL = "https://api.agnes-ai.cn/v1"
DEFAULT_MODEL = "agnes-3.0-flash"

AI_TIMEOUT = 180

MAX_BLOCK_ATTEMPTS = 3

RETRY_BASE_SECONDS = 2

THROTTLE_SECONDS = 1.5


# ======================================================================
# 工具函数
# ======================================================================

def load_settings():

    if not SETTINGS_FILE.exists():
        return {}

    try:

        with SETTINGS_FILE.open(
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

            if isinstance(data, dict):
                return data

    except Exception as e:

        print(
            f"⚠ 无法读取 settings.json：{e}"
        )

    return {}


SETTINGS = load_settings()


def _get_setting(name, default=None):

    value = SETTINGS.get(name)

    if value is not None:
        return value

    return default


def _get_api_key():

    key = os.environ.get("AGNES_API_KEY")

    if key:
        return key

    key = os.environ.get("AI_API_KEY")

    if key:
        return key

    key = _get_setting("AGNES_API_KEY")

    if key:
        return key

    key = _get_setting("AI_API_KEY")

    if key:
        return key

    return None


def _get_base_url():

    return (
        os.environ.get("AI_BASE_URL")
        or os.environ.get("AGNES_API_BASE_URL")
        or _get_setting(
            "AI_BASE_URL",
            DEFAULT_API_BASE_URL,
        )
        or DEFAULT_API_BASE_URL
    ).rstrip("/")


def _get_model():

    return (
        os.environ.get("AI_MODEL")
        or _get_setting(
            "AI_MODEL",
            DEFAULT_MODEL,
        )
        or DEFAULT_MODEL
    )


def _sleep_throttle():

    time.sleep(THROTTLE_SECONDS)


# ======================================================================
# AI 调用
# ======================================================================

def call_ai(
    messages,
    temperature=0.2,
    max_tokens=4000,
):

    api_key = _get_api_key()

    if not api_key:

        raise RuntimeError(
            "未找到 AI API Key。"
            "请设置 AGNES_API_KEY 或 AI_API_KEY。"
        )

    base_url = _get_base_url()

    model = _get_model()

    url = f"{base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    body = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    request = Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    last_error = None

    for attempt in range(5):

        try:

            with urlopen(
                request,
                timeout=AI_TIMEOUT,
            ) as response:

                raw = response.read()

                data = json.loads(
                    raw.decode("utf-8")
                )

                choices = data.get("choices")

                if not choices:

                    raise RuntimeError(
                        "AI 返回结果中没有 choices"
                    )

                content = (
                    choices[0]
                    .get("message", {})
                    .get("content", "")
                )

                if not content:

                    raise RuntimeError(
                        "AI 返回内容为空"
                    )

                return content

        except HTTPError as e:

            last_error = e

            try:
                error_body = e.read().decode(
                    "utf-8",
                    errors="ignore",
                )
            except Exception:
                error_body = ""

            print(
                f"⚠ AI HTTP 错误 "
                f"{e.code}：{error_body[:500]}"
            )

            retry_after = e.headers.get(
                "Retry-After"
            )

            if retry_after:

                try:
                    wait_seconds = float(
                        retry_after
                    )
                except Exception:
                    wait_seconds = (
                        RETRY_BASE_SECONDS
                        * (2 ** attempt)
                    )

            else:

                wait_seconds = (
                    RETRY_BASE_SECONDS
                    * (2 ** attempt)
                )

            wait_seconds += random.uniform(
                0,
                1,
            )

            if attempt < 4:

                print(
                    f"→ {wait_seconds:.1f}s 后重试"
                )

                time.sleep(
                    min(wait_seconds, 180)
                )

        except (
            URLError,
            TimeoutError,
            ConnectionError,
        ) as e:

            last_error = e

            wait_seconds = (
                RETRY_BASE_SECONDS
                * (2 ** attempt)
            )

            wait_seconds += random.uniform(
                0,
                1,
            )

            print(
                f"⚠ AI 网络错误：{e}"
            )

            if attempt < 4:

                print(
                    f"→ {wait_seconds:.1f}s 后重试"
                )

                time.sleep(
                    min(wait_seconds, 180)
                )

        except Exception as e:

            last_error = e

            print(
                f"⚠ AI 调用失败：{e}"
            )

            if attempt < 4:

                wait_seconds = (
                    RETRY_BASE_SECONDS
                    * (2 ** attempt)
                )

                time.sleep(
                    min(wait_seconds, 180)
                )

    raise RuntimeError(
        f"AI 调用连续失败：{last_error}"
    )


# ======================================================================
# JSON 提取
# ======================================================================

def _extract_json(text):

    if not text:

        raise ValueError(
            "AI 返回内容为空"
        )

    text = text.strip()

    # --------------------------------------------------------------
    # 直接 JSON
    # --------------------------------------------------------------

    try:

        return json.loads(text)

    except Exception:
        pass

    # --------------------------------------------------------------
    # Markdown JSON code block
    # --------------------------------------------------------------

    match = re.search(
        r"```(?:json)?\s*(.*?)\s*```",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if match:

        candidate = match.group(1).strip()

        try:

            return json.loads(candidate)

        except Exception:
            pass

    # --------------------------------------------------------------
    # 从第一个 { 到最后一个 } 尝试
    # --------------------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:

        candidate = text[
            start:end + 1
        ]

        try:

            return json.loads(candidate)

        except Exception as e:

            raise ValueError(
                "无法解析 AI 返回的 JSON："
                f"{e}"
            )

    raise ValueError(
        "AI 返回内容中没有找到 JSON 对象"
    )


# ======================================================================
# 基础答案验证
# ======================================================================

def _validate_answer_items(
    result,
    expected_questions,
    block_name,
):

    if not isinstance(result, dict):

        raise ValueError(
            f"{block_name} 返回结果必须是对象"
        )

    answers = result.get("answers")

    if not isinstance(answers, list):

        raise ValueError(
            f"{block_name} 缺少 answers 数组"
        )

    expected = [
        int(x)
        for x in expected_questions
    ]

    actual = []

    for item in answers:

        if not isinstance(item, dict):

            raise ValueError(
                f"{block_name} 存在非法题目对象"
            )

        if "question" not in item:

            raise ValueError(
                f"{block_name} 某题缺少 question"
            )

        try:

            question = int(
                item["question"]
            )

        except Exception:

            raise ValueError(
                f"{block_name} "
                f"题号非法："
                f"{item.get('question')}"
            )

        actual.append(question)

        if "answer" not in item:

            raise ValueError(
                f"{block_name} "
                f"第 {question} 题缺少 answer"
            )

        answer = item.get("answer")

        # ----------------------------------------------------------
        # 单项选择
        # ----------------------------------------------------------

        if isinstance(answer, str):

            if answer not in (
                "A",
                "B",
                "C",
                "D",
            ):

                raise ValueError(
                    f"{block_name} "
                    f"第 {question} 题存在非法选项："
                    f"{answer}"
                )

        # ----------------------------------------------------------
        # 多项选择
        #
        # V2.4：
        # 不再强制至少两个。
        #
        # 允许：
        #
        # ["A"]
        # ["A", "C"]
        # ["A", "B", "D"]
        #
        # 但不能为空。
        # ----------------------------------------------------------

        elif isinstance(answer, list):

            if not answer:

                raise ValueError(
                    f"{block_name} "
                    f"第 {question} 题 "
                    f"answer 不能为空数组"
                )

            for option in answer:

                if option not in (
                    "A",
                    "B",
                    "C",
                    "D",
                ):

                    raise ValueError(
                        f"{block_name} "
                        f"第 {question} 题 "
                        f"存在非法选项："
                        f"{option}"
                    )

        else:

            raise ValueError(
                f"{block_name} "
                f"第 {question} 题 answer "
                f"必须是字符串或数组"
            )

    if actual != expected:

        raise ValueError(
            f"{block_name} 题号不匹配。"
            f"期望：{expected}；"
            f"实际：{actual}"
        )


# ======================================================================
# 单项选择验证
# ======================================================================

def _validate_single_choice_answers(
    result,
    expected_questions,
    block_name,
):

    _validate_answer_items(
        result,
        expected_questions,
        block_name,
    )

    for item in result["answers"]:

        answer = item.get("answer")

        if not isinstance(answer, str):

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题"
                f"单选答案必须是字符串"
            )


# ======================================================================
# 多项选择验证
# ======================================================================

def _validate_multiple_choice_answers(
    result,
    expected_questions,
    block_name,
):

    _validate_answer_items(
        result,
        expected_questions,
        block_name,
    )

    for item in result["answers"]:

        answer = item.get("answer")

        if not isinstance(answer, list):

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题"
                f"多选答案必须是数组"
            )

        # ----------------------------------------------------------
        # V2.4
        #
        # 多选题可以只有一个正确答案。
        #
        # 因此删除：
        #
        # if len(answer) < 2:
        #
        # 但仍然禁止空数组。
        # ----------------------------------------------------------

        if not answer:

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题"
                f"多选答案不能为空"
            )

        if len(set(answer)) != len(answer):

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题"
                f"答案存在重复选项"
            )


# ======================================================================
# 完形填空验证
# ======================================================================

def _validate_cloze_answers(
    result,
    expected_questions,
    block_name,
):

    _validate_answer_items(
        result,
        expected_questions,
        block_name,
    )


# ======================================================================
# 阅读理解验证
# ======================================================================

def _validate_reading_answers(
    result,
    expected_questions,
    block_name,
):

    _validate_answer_items(
        result,
        expected_questions,
        block_name,
    )

    for item in result["answers"]:

        answer = item.get("answer")

        if not isinstance(answer, str):

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题"
                f"阅读答案必须是字符串"
            )


# ======================================================================
# 翻译验证
# ======================================================================

def _validate_translation_answers(
    result,
    expected_questions,
    block_name,
):

    if not isinstance(result, dict):

        raise ValueError(
            f"{block_name} 返回结果必须是对象"
        )

    answers = result.get("answers")

    if not isinstance(answers, list):

        raise ValueError(
            f"{block_name} 缺少 answers 数组"
        )

    expected = [
        int(x)
        for x in expected_questions
    ]

    actual = []

    for item in answers:

        if not isinstance(item, dict):

            raise ValueError(
                f"{block_name} 存在非法题目对象"
            )

        question = item.get("question")

        try:

            question = int(question)

        except Exception:

            raise ValueError(
                f"{block_name} "
                f"题号非法：{question}"
            )

        actual.append(question)

        if not item.get("answer"):

            raise ValueError(
                f"{block_name} "
                f"第 {question} 题答案为空"
            )

        if not isinstance(
            item.get("answer"),
            str,
        ):

            raise ValueError(
                f"{block_name} "
                f"第 {question} 题答案必须是字符串"
            )

    if actual != expected:

        raise ValueError(
            f"{block_name} 题号不匹配。"
            f"期望：{expected}；"
            f"实际：{actual}"
        )


# ======================================================================
# 写作验证
# ======================================================================

def _validate_writing_answer(
    result,
    expected_questions,
    block_name,
):

    if not isinstance(result, dict):

        raise ValueError(
            f"{block_name} 返回结果必须是对象"
        )

    answers = result.get("answers")

    if not isinstance(answers, list):

        raise ValueError(
            f"{block_name} 缺少 answers 数组"
        )

    expected = [
        int(x)
        for x in expected_questions
    ]

    actual = []

    for item in answers:

        if not isinstance(item, dict):

            raise ValueError(
                f"{block_name} 存在非法题目对象"
            )

        try:

            question = int(
                item["question"]
            )

        except Exception:

            raise ValueError(
                f"{block_name} 题号非法"
            )

        actual.append(question)

        answer = item.get("answer")

        if not isinstance(
            answer,
            str,
        ) or not answer.strip():

            raise ValueError(
                f"{block_name} "
                f"第 {question} 题答案为空"
            )

    if actual != expected:

        raise ValueError(
            f"{block_name} 题号不匹配。"
            f"期望：{expected}；"
            f"实际：{actual}"
        )


# ======================================================================
# Prompt
# ======================================================================

def _build_question_payload(
    questions,
):

    payload = []

    for q in questions:

        item = {
            "question": q.get(
                "question"
            ),
            "question_text": q.get(
                "question_text",
                q.get(
                    "question",
                    "",
                ),
            ),
        }

        if "options" in q:

            item["options"] = q[
                "options"
            ]

        if "passage" in q:

            item["passage"] = q[
                "passage"
            ]

        if "translation" in q:

            item["translation"] = q[
                "translation"
            ]

        if "sentence" in q:

            item["sentence"] = q[
                "sentence"
            ]

        payload.append(item)

    return payload


def _build_system_prompt():

    return """
你是英语学习系统的专业试卷答案解析专家。

你的任务是：

1. 根据原题判断正确答案
2. 为每道题提供详细、准确、适合学习者理解的解析
3. 严格按照要求返回 JSON
4. 不得修改原题
5. 不得修改选项
6. 不得遗漏任何题目
7. 不得增加不存在的题目
8. 不得改变题号

============================================================
选择题答案规则
============================================================

单项选择题：

answer 必须是字符串，只能是：

"A"
"B"
"C"
"D"

多项选择题：

answer 必须是数组，只能包含：

"A"
"B"
"C"
"D"

例如：

["A"]

["A", "C"]

["A", "B", "D"]

多选题的正确答案数量必须以原题实际内容为准。

不要为了满足“多选题”而强行增加错误选项。

如果根据原题判断只有一个选项正确，
必须如实返回一个选项，例如：

["B"]

绝对禁止为了凑够两个答案而编造错误选项。

============================================================
JSON 格式规则
============================================================

必须返回合法 JSON。

不要返回 Markdown。

不要返回 ```json。

不要在 JSON 字符串中直接放置未转义的双引号。

如果解析中需要引用英文单词或短语，
优先使用中文引号“ ”，
不要使用未经转义的英文双引号。

============================================================
答案解析
============================================================

每道题都必须包含：

question
answer
analysis

analysis 必须说明：

- 为什么这个答案正确
- 其他选项为什么不正确（如果适用）
- 涉及的词汇、语法或阅读理解点
- 适合英语学习者理解

============================================================
绝对禁止
============================================================

不得：

- 修改原题
- 修改选项
- 编造原文不存在的信息
- 编造答案
- 为多选题强行增加错误选项
- 遗漏题目
- 修改题号
"""


def _build_user_prompt(
    block_name,
    questions,
):

    question_payload = (
        _build_question_payload(
            questions
        )
    )

    payload_text = json.dumps(
        question_payload,
        ensure_ascii=False,
        indent=2,
    )

    return f"""
现在处理：

{block_name}

原题数据如下：

{payload_text}

请根据原题逐题判断正确答案，并生成详细解析。

严格按照以下 JSON 结构返回：

{{
  "answers": [
    {{
      "question": 1,
      "answer": "A",
      "analysis": "解析内容"
    }}
  ]
}}

如果是多项选择题：

{{
  "answers": [
    {{
      "question": 1,
      "answer": ["A", "C"],
      "analysis": "解析内容"
    }}
  ]
}}

注意：

多选题答案数量必须以实际题目为准。

如果只有一个选项正确，就返回：

["A"]

不能为了满足“多选题”而强行增加第二个错误选项。

必须覆盖本模块全部题目。
"""


# ======================================================================
# Block 生成
# ======================================================================

def _run_block(
    block_name,
    questions,
    validator,
):

    expected_questions = [
        q.get("question")
        for q in questions
    ]

    last_error = None

    for attempt in range(
        1,
        MAX_BLOCK_ATTEMPTS + 1,
    ):

        print(
            f"      → 尝试 {attempt}/"
            f"{MAX_BLOCK_ATTEMPTS}"
        )

        try:

            messages = [
                {
                    "role": "system",
                    "content": (
                        _build_system_prompt()
                    ),
                },
                {
                    "role": "user",
                    "content": _build_user_prompt(
                        block_name,
                        questions,
                    ),
                },
            ]

            _sleep_throttle()

            raw = call_ai(
                messages,
                temperature=0.2,
                max_tokens=5000,
            )

            print(
                f"      → AI 返回 "
                f"{len(raw)} 字符"
            )

            result = _extract_json(
                raw
            )

            validator(
                result,
                expected_questions,
                block_name,
            )

            print(
                f"      ✓ {block_name} "
                f"验证通过"
            )

            return result

        except Exception as e:

            last_error = e

            print(
                f"      ✗ {block_name} "
                f"失败：{e}"
            )

            if attempt < MAX_BLOCK_ATTEMPTS:

                wait_seconds = (
                    2 ** attempt
                ) + random.uniform(
                    0,
                    1,
                )

                print(
                    f"      → "
                    f"{wait_seconds:.1f}s 后重试"
                )

                time.sleep(
                    wait_seconds
                )

    raise RuntimeError(
        f"{block_name} 连续 "
        f"{MAX_BLOCK_ATTEMPTS} 次失败："
        f"{last_error}"
    )


# ======================================================================
# 最终结果验证
# ======================================================================

def _validate_final_result(
    result,
    exam_data,
):

    if not isinstance(
        result,
        dict,
    ):

        raise ValueError(
            "最终答案结果必须是对象"
        )

    if "blocks" not in result:

        raise ValueError(
            "最终结果缺少 blocks"
        )

    if not isinstance(
        result["blocks"],
        list,
    ):

        raise ValueError(
            "blocks 必须是数组"
        )

    if "overall_analysis" not in result:

        raise ValueError(
            "最终结果缺少 overall_analysis"
        )

    if not isinstance(
        result["overall_analysis"],
        str,
    ):

        raise ValueError(
            "overall_analysis 必须是字符串"
        )


# ======================================================================
# 总体分析
# ======================================================================

def _build_overall_analysis(
    exam_data,
    blocks,
):

    summary = []

    for block in blocks:

        if not isinstance(
            block,
            dict,
        ):
            continue

        block_name = block.get(
            "block_name",
            "",
        )

        answers = block.get(
            "answers",
            [],
        )

        summary.append(
            {
                "block_name": block_name,
                "answers": answers,
            }
        )

    summary_text = json.dumps(
        summary,
        ensure_ascii=False,
        indent=2,
    )

    messages = [
        {
            "role": "system",
            "content": """
你是英语学习分析专家。

请根据整套英语试卷的答案和解析，
生成一份总体学习分析。

分析重点：

1. 学习者可能掌握较好的内容
2. 可能存在的薄弱点
3. 词汇问题
4. 语法问题
5. 阅读理解问题
6. 听力问题
7. 翻译问题
8. 写作问题
9. 后续学习建议

必须返回合法 JSON：

{
  "overall_analysis": "完整分析"
}

不要返回 Markdown。
不要返回 ```json。
""",
        },
        {
            "role": "user",
            "content": f"""
整套试卷答案与解析：

{summary_text}

请生成总体学习分析。
""",
        },
    ]

    _sleep_throttle()

    raw = call_ai(
        messages,
        temperature=0.2,
        max_tokens=5000,
    )

    result = _extract_json(
        raw
    )

    analysis = result.get(
        "overall_analysis"
    )

    if not isinstance(
        analysis,
        str,
    ) or not analysis.strip():

        raise ValueError(
            "总体学习分析为空"
        )

    return analysis


# ======================================================================
# 主生成函数
# ======================================================================

def generate(
    exam_data,
    output_path=None,
):

    print(
        "============================================================"
    )

    print(
        "EXAM ANSWERS / ANALYSIS GENERATION V2.4"
    )

    print(
        "============================================================"
    )

    if not isinstance(
        exam_data,
        dict,
    ):

        raise ValueError(
            "exam_data 必须是 dict"
        )

    # ==============================================================
    # 读取试卷结构
    # ==============================================================

    listening = exam_data.get(
        "listening",
        {},
    )

    single_choice = exam_data.get(
        "single_choice",
        [],
    )

    multiple_choice = exam_data.get(
        "multiple_choice",
        [],
    )

    cloze = exam_data.get(
        "cloze",
        [],
    )

    reading = exam_data.get(
        "reading",
        [],
    )

    translation = exam_data.get(
        "translation",
        {},
    )

    writing = exam_data.get(
        "writing",
        [],
    )

    # ==============================================================
    # 构建 14 个模块
    # ==============================================================

    blocks = []

    # --------------------------------------------------------------
    # Listening A
    # --------------------------------------------------------------

    listening_a = listening.get(
        "A",
        [],
    )

    if listening_a:

        blocks.append(
            {
                "block_name":
                    "Listening A",
                "questions":
                    listening_a,
                "validator":
                    _validate_single_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Listening B
    # --------------------------------------------------------------

    listening_b = listening.get(
        "B",
        [],
    )

    if listening_b:

        blocks.append(
            {
                "block_name":
                    "Listening B",
                "questions":
                    listening_b,
                "validator":
                    _validate_single_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Listening C
    # --------------------------------------------------------------

    listening_c = listening.get(
        "C",
        [],
    )

    if listening_c:

        blocks.append(
            {
                "block_name":
                    "Listening C",
                "questions":
                    listening_c,
                "validator":
                    _validate_single_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Single Choice 1
    # --------------------------------------------------------------

    if len(single_choice) > 0:

        blocks.append(
            {
                "block_name":
                    "Single Choice 1",
                "questions":
                    single_choice[:5],
                "validator":
                    _validate_single_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Single Choice 2
    # --------------------------------------------------------------

    if len(single_choice) > 5:

        blocks.append(
            {
                "block_name":
                    "Single Choice 2",
                "questions":
                    single_choice[5:],
                "validator":
                    _validate_single_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Multiple Choice 1
    # --------------------------------------------------------------

    if len(multiple_choice) > 0:

        blocks.append(
            {
                "block_name":
                    "Multiple Choice 1",
                "questions":
                    multiple_choice[:5],
                "validator":
                    _validate_multiple_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Multiple Choice 2
    # --------------------------------------------------------------

    if len(multiple_choice) > 5:

        blocks.append(
            {
                "block_name":
                    "Multiple Choice 2",
                "questions":
                    multiple_choice[5:],
                "validator":
                    _validate_multiple_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Cloze
    # --------------------------------------------------------------

    if cloze:

        blocks.append(
            {
                "block_name":
                    "Cloze",
                "questions":
                    cloze,
                "validator":
                    _validate_single_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Reading
    # --------------------------------------------------------------

    if reading:

        blocks.append(
            {
                "block_name":
                    "Reading",
                "questions":
                    reading,
                "validator":
                    _validate_single_choice_answers,
            }
        )

    # --------------------------------------------------------------
    # Translation A
    # --------------------------------------------------------------

    translation_a = (
        translation.get(
            "A",
            [],
        )
        if isinstance(
            translation,
            dict,
        )
        else []
    )

    if translation_a:

        blocks.append(
            {
                "block_name":
                    "Translation A",
                "questions":
                    translation_a,
                "validator":
                    _validate_translation_answers,
            }
        )

    # --------------------------------------------------------------
    # Translation B
    # --------------------------------------------------------------

    translation_b = (
        translation.get(
            "B",
            [],
        )
        if isinstance(
            translation,
            dict,
        )
        else []
    )

    if translation_b:

        blocks.append(
            {
                "block_name":
                    "Translation B",
                "questions":
                    translation_b,
                "validator":
                    _validate_translation_answers,
            }
        )

    # --------------------------------------------------------------
    # Writing
    # --------------------------------------------------------------

    if writing:

        blocks.append(
            {
                "block_name":
                    "Writing",
                "questions":
                    writing,
                "validator":
                    _validate_writing_answer,
            }
        )

    # ==============================================================
    # 逐模块生成
    # ==============================================================

    generated_blocks = []

    total_blocks = len(blocks)

    for index, block in enumerate(
        blocks,
        start=1,
    ):

        block_name = block[
            "block_name"
        ]

        questions = block[
            "questions"
        ]

        validator = block[
            "validator"
        ]

        first_question = (
            questions[0].get(
                "question"
            )
            if questions
            else ""
        )

        last_question = (
            questions[-1].get(
                "question"
            )
            if questions
            else ""
        )

        print(
            f"[{index}/{total_blocks}] "
            f"{block_name}｜"
            f"{len(questions)}题"
            f"｜{first_question}-"
            f"{last_question}"
        )

        result = _run_block(
            block_name,
            questions,
            validator,
        )

        generated_blocks.append(
            {
                "block_name":
                    block_name,
                "answers":
                    result["answers"],
            }
        )

        print(
            f"      ✓ {block_name} 完成"
        )

    # ==============================================================
    # 总体分析
    # ==============================================================

    print()
    print(
        "→ 正在生成总体学习分析"
    )

    overall_analysis = (
        _build_overall_analysis(
            exam_data,
            generated_blocks,
        )
    )

    print(
        "✓ 总体学习分析完成"
    )

    # ==============================================================
    # 最终结果
    # ==============================================================

    final_result = {
        "blocks":
            generated_blocks,
        "overall_analysis":
            overall_analysis,
    }

    _validate_final_result(
        final_result,
        exam_data,
    )

    # ==============================================================
    # 保存
    # ==============================================================

    if output_path:

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                final_result,
                f,
                ensure_ascii=False,
                indent=2,
            )

        print()
        print(
            f"✓ 答案解析已保存："
            f"{output_path}"
        )

    print()
    print(
        "============================================================"
    )

    print(
        "答案与详细解析生成完成"
    )

    print(
        "============================================================"
    )

    return final_result


# ======================================================================
# Markdown 渲染
# ======================================================================

def render(
    result,
    output_path,
    article_title="",
    difficulty="",
    article_type="",
):

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = []

    lines.append(
        "# 英语综合试卷答案与详细解析"
    )

    lines.append("")

    if article_title:

        lines.append(
            f"文章：{article_title}"
        )

        lines.append("")

    if difficulty:

        lines.append(
            f"难度：{difficulty}"
        )

        lines.append("")

    if article_type:

        lines.append(
            f"文章类型：{article_type}"
        )

        lines.append("")

    lines.append("---")
    lines.append("")

    for block in result.get(
        "blocks",
        [],
    ):

        block_name = block.get(
            "block_name",
            "",
        )

        lines.append(
            f"## {block_name}"
        )

        lines.append("")

        for item in block.get(
            "answers",
            [],
        ):

            question = item.get(
                "question",
                "",
            )

            answer = item.get(
                "answer",
                "",
            )

            analysis = item.get(
                "analysis",
                "",
            )

            if isinstance(
                answer,
                list,
            ):

                answer_text = ", ".join(
                    answer
                )

            else:

                answer_text = str(
                    answer
                )

            lines.append(
                f"### {question}. "
                f"答案：{answer_text}"
            )

            lines.append("")

            if analysis:

                lines.append(
                    analysis
                )

                lines.append("")

        lines.append("---")
        lines.append("")

    lines.append(
        "## 总体学习分析"
    )

    lines.append("")

    lines.append(
        result.get(
            "overall_analysis",
            "",
        )
    )

    lines.append("")

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            "\n".join(lines)
        )

    print(
        f"✓ Markdown 已保存："
        f"{output_path}"
    )

    return output_path


# ======================================================================
# CLI
# ======================================================================

if __name__ == "__main__":

    print(
        "============================================================"
    )

    print(
        "exam_answers.py V2.4"
    )

    print(
        "============================================================"
    )

    if len(sys.argv) < 2:

        print(
            "用法："
        )

        print(
            "python exam_answers.py "
            "<exam_data.json> "
            "[output.json]"
        )

        sys.exit(1)

    exam_data_path = Path(
        sys.argv[1]
    )

    if not exam_data_path.exists():

        print(
            f"错误：文件不存在："
            f"{exam_data_path}"
        )

        sys.exit(1)

    try:

        with exam_data_path.open(
            "r",
            encoding="utf-8",
        ) as f:

            exam_data = json.load(f)

    except Exception as e:

        print(
            f"错误：无法读取 exam_data："
            f"{e}"
        )

        sys.exit(1)

    output_path = None

    if len(sys.argv) >= 3:

        output_path = Path(
            sys.argv[2]
        )

    try:

        generate(
            exam_data,
            output_path,
        )

    except Exception as e:

        print()
        print(
            "✗ 答案解析生成失败"
        )

        print(
            f"错误：{e}"
        )

        sys.exit(1)
