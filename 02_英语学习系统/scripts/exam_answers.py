#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Exam Answers / Analysis Generator V2.5

======================================================================
职责
======================================================================

本文件只负责：

    1. 根据已经生成好的英语试卷 exam_data 生成答案
    2. 生成每一道题的详细解析
    3. 生成听力原文
    4. 生成总体学习分析

======================================================================
重要数据结构契约
======================================================================

Stage 2 exam_data 中：

    question = 题目文字
    number   = 数字题号
    options  = 选项

例如：

    {
        "number": 1,
        "question": "What word do you hear?",
        "options": [
            "A. run",
            "B. swim",
            "C. jump",
            "D. dance"
        ]
    }

绝对禁止：

    int(question)

必须使用：

    number

======================================================================
兼容当前 main.py
======================================================================

generate(
    exam_data,
    article_title="",
    difficulty="",
    article_type="",
    words=0,
)

======================================================================
规则
======================================================================

1. 不修改试卷
2. 不修改 exam_data
3. 每个模块独立调用 AI
4. 单个模块失败最多重试 3 次
5. 已经成功的模块可复用
6. 多选题允许 1～4 个正确答案
7. 多选题绝不强制至少两个答案
8. 所有答案必须来自 A/B/C/D
9. JSON 必须合法
10. 保持题目原始 number
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# ======================================================================
# 配置
# ======================================================================

DEFAULT_API_BASE_URL = "https://api.agnes-ai.cn/v1"
DEFAULT_MODEL = "agnes-3.0-flash"

REQUEST_TIMEOUT = 180
MAX_AI_RETRIES = 5
MAX_BLOCK_ATTEMPTS = 3

RETRY_BASE_SECONDS = 2.0
THROTTLE_SECONDS = 1.5


# ======================================================================
# 基础工具
# ======================================================================

def _get_api_key() -> str:
    api_key = (
        os.environ.get("AGNES_API_KEY")
        or os.environ.get("AI_API_KEY")
        or ""
    ).strip()

    if not api_key:
        raise RuntimeError(
            "未找到 AGNES_API_KEY 或 AI_API_KEY 环境变量"
        )

    return api_key


def _get_base_url() -> str:
    return (
        os.environ.get("AI_BASE_URL")
        or DEFAULT_API_BASE_URL
    ).rstrip("/")


def _get_model() -> str:
    return (
        os.environ.get("AI_MODEL")
        or DEFAULT_MODEL
    ).strip()


# ======================================================================
# AI 调用
# ======================================================================

def call_ai(
    system_prompt: str,
    user_prompt: str,
) -> str:

    api_key = _get_api_key()
    base_url = _get_base_url()
    model = _get_model()

    url = f"{base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "temperature": 0.2,
    }

    data = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = None

    for attempt in range(1, MAX_AI_RETRIES + 1):

        try:
            request = Request(
                url,
                data=data,
                headers=headers,
                method="POST",
            )

            with urlopen(
                request,
                timeout=REQUEST_TIMEOUT,
            ) as response:

                raw = response.read().decode("utf-8")

            result = json.loads(raw)

            content = (
                result.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if not content:
                raise RuntimeError(
                    "AI 返回内容为空"
                )

            time.sleep(THROTTLE_SECONDS)

            return content

        except HTTPError as exc:

            last_error = exc

            retry_after = exc.headers.get("Retry-After")

            if retry_after:
                try:
                    delay = float(retry_after)
                except ValueError:
                    delay = RETRY_BASE_SECONDS * (2 ** (attempt - 1))
            else:
                delay = RETRY_BASE_SECONDS * (2 ** (attempt - 1))

            delay = min(delay, 180)

            if attempt >= MAX_AI_RETRIES:
                break

            jitter = random.uniform(0, 0.5)

            print(
                f"      → AI 请求失败 HTTP {exc.code}，"
                f"{delay + jitter:.1f}s 后重试"
            )

            time.sleep(delay + jitter)

        except (URLError, TimeoutError, json.JSONDecodeError) as exc:

            last_error = exc

            if attempt >= MAX_AI_RETRIES:
                break

            delay = min(
                RETRY_BASE_SECONDS * (2 ** (attempt - 1)),
                180,
            )

            jitter = random.uniform(0, 0.5)

            print(
                f"      → AI 请求异常：{exc}"
            )
            print(
                f"      → {delay + jitter:.1f}s 后重试"
            )

            time.sleep(delay + jitter)

        except Exception as exc:

            last_error = exc

            if attempt >= MAX_AI_RETRIES:
                break

            delay = min(
                RETRY_BASE_SECONDS * (2 ** (attempt - 1)),
                180,
            )

            jitter = random.uniform(0, 0.5)

            print(
                f"      → AI 请求异常：{exc}"
            )
            time.sleep(delay + jitter)

    raise RuntimeError(
        f"AI 调用连续 {MAX_AI_RETRIES} 次失败：{last_error}"
    )


# ======================================================================
# JSON 提取
# ======================================================================

def _extract_json(text: str):

    text = text.strip()

    # --------------------------------------------------------------
    # 1. 直接 JSON
    # --------------------------------------------------------------

    try:
        return json.loads(text)
    except Exception:
        pass

    # --------------------------------------------------------------
    # 2. Markdown JSON code block
    # --------------------------------------------------------------

    fenced = re.findall(
        r"```(?:json)?\s*(.*?)\s*```",
        text,
        flags=re.S | re.I,
    )

    for candidate in fenced:
        try:
            return json.loads(candidate)
        except Exception:
            continue

    # --------------------------------------------------------------
    # 3. 从文本中寻找 JSON 对象
    # --------------------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        candidate = text[start:end + 1]

        try:
            return json.loads(candidate)
        except Exception:
            pass

    # --------------------------------------------------------------
    # 4. 从文本中寻找 JSON 数组
    # --------------------------------------------------------------

    start = text.find("[")
    end = text.rfind("]")

    if start >= 0 and end > start:
        candidate = text[start:end + 1]

        try:
            return json.loads(candidate)
        except Exception:
            pass

    raise ValueError(
        "AI 返回内容无法解析为合法 JSON"
    )


# ======================================================================
# 数据结构标准化
# ======================================================================

def _prepare_question(
    question: dict,
    fallback_number: int,
) -> dict:

    if not isinstance(question, dict):
        raise ValueError(
            f"题目不是对象：{question!r}"
        )

    item = dict(question)

    # --------------------------------------------------------------
    # 真正的题号来自 number
    # --------------------------------------------------------------

    number = item.get("number")

    if number is None:
        number = fallback_number

    try:
        number = int(number)
    except Exception:
        raise ValueError(
            f"题目 number 无法转换为整数：{number!r}"
        )

    item["_answer_question_number"] = number

    # --------------------------------------------------------------
    # 保留原始 question 文本
    # --------------------------------------------------------------

    question_text = item.get("question", "")

    if not isinstance(question_text, str):
        question_text = str(question_text)

    item["_answer_question_text"] = question_text

    return item


def _prepare_question_list(
    questions,
    section_name: str,
) -> list:

    if questions is None:
        return []

    if not isinstance(questions, list):
        raise ValueError(
            f"{section_name} 必须是列表，"
            f"实际类型：{type(questions).__name__}"
        )

    result = []

    for index, question in enumerate(
        questions,
        start=1,
    ):
        result.append(
            _prepare_question(
                question,
                index,
            )
        )

    return result


def _prepare_listening(
    listening,
) -> list:

    if listening is None:
        return []

    if not isinstance(listening, list):
        raise ValueError(
            "listening 必须是列表"
        )

    result = []

    for part_data in listening:

        if not isinstance(part_data, dict):
            raise ValueError(
                "listening part 必须是对象"
            )

        part = str(
            part_data.get("part", "")
        ).strip()

        questions = _prepare_question_list(
            part_data.get("questions", []),
            f"Listening {part}",
        )

        result.append(
            {
                "part": part,
                "instruction": part_data.get(
                    "instruction",
                    "",
                ),
                "questions": questions,
            }
        )

    return result


# ======================================================================
# Question Payload
# ======================================================================

def _build_question_payload(
    questions: list,
) -> list:

    payload = []

    for q in questions:

        item = {
            "question": q["_answer_question_number"],
            "question_text": q["_answer_question_text"],
        }

        if "options" in q:
            item["options"] = q["options"]

        if "answer_instruction" in q:
            item["answer_instruction"] = q[
                "answer_instruction"
            ]

        if "sentence" in q:
            item["sentence"] = q["sentence"]

        payload.append(item)

    return payload


# ======================================================================
# Validator
# ======================================================================

def _validate_answer_items(
    result,
    expected_questions,
    module_name,
):

    if not isinstance(result, list):
        raise ValueError(
            f"{module_name} 返回结果必须是数组"
        )

    expected = [
        int(x)
        for x in expected_questions
    ]

    actual = []

    for item in result:

        if not isinstance(item, dict):
            raise ValueError(
                f"{module_name} 存在非对象答案项"
            )

        if "question" not in item:
            raise ValueError(
                f"{module_name} 答案缺少 question"
            )

        try:
            number = int(item["question"])
        except Exception:
            raise ValueError(
                f"{module_name} question 必须是数字："
                f"{item['question']!r}"
            )

        actual.append(number)

        if "answer" not in item:
            raise ValueError(
                f"{module_name} 第 {number} 题缺少 answer"
            )

        answer = item["answer"]

        if isinstance(answer, str):

            answer = answer.strip().upper()

            if answer not in {
                "A",
                "B",
                "C",
                "D",
            }:
                raise ValueError(
                    f"{module_name} 第 {number} 题答案非法："
                    f"{answer}"
                )

        elif isinstance(answer, list):

            if not answer:
                raise ValueError(
                    f"{module_name} 第 {number} 题答案不能为空"
                )

            normalized = []

            for option in answer:

                if not isinstance(
                    option,
                    str,
                ):
                    raise ValueError(
                        f"{module_name} 第 {number} 题"
                        "答案必须是 A/B/C/D"
                    )

                option = option.strip().upper()

                if option not in {
                    "A",
                    "B",
                    "C",
                    "D",
                }:
                    raise ValueError(
                        f"{module_name} 第 {number} 题"
                        f"答案非法：{option}"
                    )

                if option in normalized:
                    raise ValueError(
                        f"{module_name} 第 {number} 题"
                        f"答案重复：{option}"
                    )

                normalized.append(option)

        else:
            raise ValueError(
                f"{module_name} 第 {number} 题"
                " answer 类型非法"
            )

    if sorted(actual) != sorted(expected):
        raise ValueError(
            f"{module_name} 题号不完整或错误。"
            f"期望：{expected}，"
            f"实际：{actual}"
        )

    if len(actual) != len(set(actual)):
        raise ValueError(
            f"{module_name} 存在重复题号"
        )

    return result


def _validate_single_choice_answers(
    result,
    expected_questions,
    module_name,
):

    result = _validate_answer_items(
        result,
        expected_questions,
        module_name,
    )

    for item in result:

        answer = item["answer"]

        if not isinstance(answer, str):
            raise ValueError(
                f"{module_name} 第 "
                f"{item['question']} 题"
                "单选答案必须是单个字母"
            )

        if answer.strip().upper() not in {
            "A",
            "B",
            "C",
            "D",
        }:
            raise ValueError(
                f"{module_name} 第 "
                f"{item['question']} 题"
                "单选答案非法"
            )

    return result


def _validate_multiple_choice_answers(
    result,
    expected_questions,
    module_name,
):

    result = _validate_answer_items(
        result,
        expected_questions,
        module_name,
    )

    # --------------------------------------------------------------
    # 多选题：
    # 允许 1～4 个答案
    #
    # 绝不强制至少两个答案。
    # --------------------------------------------------------------

    for item in result:

        answer = item["answer"]

        if not isinstance(answer, list):
            raise ValueError(
                f"{module_name} 第 "
                f"{item['question']} 题"
                "多选答案必须是数组"
            )

        if len(answer) < 1:
            raise ValueError(
                f"{module_name} 第 "
                f"{item['question']} 题"
                "多选答案不能为空"
            )

        if len(answer) > 4:
            raise ValueError(
                f"{module_name} 第 "
                f"{item['question']} 题"
                "多选答案最多 4 个"
            )

    return result


def _validate_cloze_answers(
    result,
    expected_questions,
    module_name,
):

    return _validate_single_choice_answers(
        result,
        expected_questions,
        module_name,
    )


def _validate_reading_answers(
    result,
    expected_questions,
    module_name,
):

    return _validate_single_choice_answers(
        result,
        expected_questions,
        module_name,
    )


def _validate_translation_answers(
    result,
    expected_questions,
    module_name,
):

    if not isinstance(result, list):
        raise ValueError(
            f"{module_name} 必须返回数组"
        )

    expected = [
        int(x)
        for x in expected_questions
    ]

    actual = []

    for item in result:

        if not isinstance(item, dict):
            raise ValueError(
                f"{module_name} 存在非法答案项"
            )

        number = item.get("question")

        try:
            number = int(number)
        except Exception:
            raise ValueError(
                f"{module_name} question 非数字"
            )

        actual.append(number)

        answer = item.get("answer", "")

        if not isinstance(answer, str):
            raise ValueError(
                f"{module_name} 第 {number} 题"
                " answer 必须是字符串"
            )

        if not answer.strip():
            raise ValueError(
                f"{module_name} 第 {number} 题"
                " answer 不能为空"
            )

        if not item.get("analysis"):
            raise ValueError(
                f"{module_name} 第 {number} 题"
                " 缺少 analysis"
            )

    if sorted(actual) != sorted(expected):
        raise ValueError(
            f"{module_name} 题号错误。"
            f"期望：{expected}，"
            f"实际：{actual}"
        )

    if len(actual) != len(set(actual)):
        raise ValueError(
            f"{module_name} 存在重复题号"
        )

    return result


def _validate_writing_answers(
    result,
    expected_questions,
    module_name,
):

    if not isinstance(result, list):
        raise ValueError(
            f"{module_name} 必须返回数组"
        )

    expected = [
        int(x)
        for x in expected_questions
    ]

    actual = []

    for item in result:

        if not isinstance(item, dict):
            raise ValueError(
                f"{module_name} 存在非法答案项"
            )

        try:
            number = int(item["question"])
        except Exception:
            raise ValueError(
                f"{module_name} question 非数字"
            )

        actual.append(number)

        if not item.get("answer"):
            raise ValueError(
                f"{module_name} 第 {number} 题"
                " 缺少 answer"
            )

        if not item.get("analysis"):
            raise ValueError(
                f"{module_name} 第 {number} 题"
                " 缺少 analysis"
            )

    if sorted(actual) != sorted(expected):
        raise ValueError(
            f"{module_name} 题号错误。"
            f"期望：{expected}，"
            f"实际：{actual}"
        )

    if len(actual) != len(set(actual)):
        raise ValueError(
            f"{module_name} 存在重复题号"
        )

    return result


# ======================================================================
# Prompt
# ======================================================================

SYSTEM_PROMPT = """
你是 748686 英语学习系统的试卷答案与解析专家。

你的任务是根据给出的真实试卷题目，生成标准答案和详细解析。

必须严格遵守以下规则：

1. 只能根据题目、选项和文章内容判断答案。
2. 不得修改题目。
3. 不得修改选项。
4. 不得创造题目中不存在的信息。
5. 返回严格合法的 JSON。
6. 不要使用 Markdown。
7. 不要输出 JSON 之外的任何内容。
8. JSON 字符串内部如果需要引用英文，请避免使用未经转义的英文双引号。
9. 可以使用中文引号“”。

答案格式：

[
  {
    "question": 1,
    "answer": "B",
    "analysis": "详细解释为什么选择 B，并说明其他选项为什么不正确。"
  }
]

多选题格式：

[
  {
    "question": 1,
    "answer": ["A", "C"],
    "analysis": "详细解释所有正确答案。"
  }
]

特别重要：

多选题的正确答案数量必须根据题目真实内容判断。

允许：

["A"]

也允许：

["A", "C"]

也允许：

["A", "B", "C"]

最多：

["A", "B", "C", "D"]

绝对不要因为题目写着“多选题”就强行添加第二个错误答案。

如果实际上只有一个正确答案，就必须返回：

["B"]

不能为了满足“多选”而制造错误答案。
"""


# ======================================================================
# 单模块运行
# ======================================================================

def _run_block(
    module_name: str,
    questions: list,
    validator,
) -> dict:

    if not questions:
        return {
            "module": module_name,
            "answers": [],
        }

    expected_questions = [
        q["_answer_question_number"]
        for q in questions
    ]

    first_question = expected_questions[0]
    last_question = expected_questions[-1]

    print(
        f"[MODULE] {module_name}｜"
        f"{len(questions)}题｜"
        f"{first_question}-{last_question}"
    )

    payload = _build_question_payload(
        questions
    )

    user_prompt = f"""
请为下面的试卷题目生成标准答案和详细解析。

模块：

{module_name}

题目：

{json.dumps(
    payload,
    ensure_ascii=False,
    indent=2,
)}

必须返回：

[
  {{
    "question": 题号,
    "answer": "A/B/C/D 或 [\"A\", \"C\"]",
    "analysis": "详细解析"
  }}
]

要求：

- question 必须使用题目中的 number
- 必须覆盖全部题目
- 不得遗漏
- 不得增加题目
- 单选题只能一个字母
- 多选题允许 1～4 个字母
- 答案必须来自 A/B/C/D
"""

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

            raw = call_ai(
                SYSTEM_PROMPT,
                user_prompt,
            )

            print(
                f"      → AI 返回 "
                f"{len(raw)} 字符"
            )

            parsed = _extract_json(raw)

            validated = validator(
                parsed,
                expected_questions,
                module_name,
            )

            print(
                f"      ✓ {module_name} "
                f"通过验证"
            )

            return {
                "module": module_name,
                "answers": validated,
            }

        except Exception as exc:

            last_error = exc

            print(
                f"      ✗ {module_name} "
                f"失败：{exc}"
            )

            if attempt < MAX_BLOCK_ATTEMPTS:

                time.sleep(
                    RETRY_BASE_SECONDS
                )

    raise RuntimeError(
        f"{module_name} 连续 "
        f"{MAX_BLOCK_ATTEMPTS} 次失败："
        f"{last_error}"
    )


# ======================================================================
# Generate
# ======================================================================

def generate(
    exam_data,
    article_title="",
    difficulty="",
    article_type="",
    words=0,
):

    print("=" * 60)
    print(
        "EXAM ANSWERS / ANALYSIS GENERATION V2.5"
    )
    print("=" * 60)

    if not isinstance(exam_data, dict):
        raise ValueError(
            "exam_data 必须是 dict"
        )

    # --------------------------------------------------------------
    # Stage 2 原始结构
    # --------------------------------------------------------------

    listening = _prepare_listening(
        exam_data.get("listening", [])
    )

    single_choice = _prepare_question_list(
        exam_data.get("single_choice", []),
        "Single Choice",
    )

    multiple_choice = _prepare_question_list(
        exam_data.get("multiple_choice", []),
        "Multiple Choice",
    )

    cloze_data = exam_data.get(
        "cloze",
        [],
    )

    cloze = []

    if cloze_data:

        if not isinstance(
            cloze_data,
            list,
        ):
            raise ValueError(
                "cloze 必须是列表"
            )

        for index, block in enumerate(
            cloze_data,
            start=1,
        ):

            if not isinstance(
                block,
                dict,
            ):
                raise ValueError(
                    "cloze block 必须是对象"
                )

            questions = _prepare_question_list(
                block.get(
                    "questions",
                    [],
                ),
                f"Cloze {index}",
            )

            cloze.append(
                {
                    "passage": block.get(
                        "passage",
                        "",
                    ),
                    "questions": questions,
                }
            )

    reading = _prepare_question_list(
        exam_data.get("reading", []),
        "Reading",
    )

    translation_data = exam_data.get(
        "translation",
        {},
    )

    translation_a = _prepare_question_list(
        translation_data.get(
            "part_a",
            [],
        )
        if isinstance(
            translation_data,
            dict,
        )
        else [],
        "Translation A",
    )

    translation_b = _prepare_question_list(
        translation_data.get(
            "part_b",
            [],
        )
        if isinstance(
            translation_data,
            dict,
        )
        else [],
        "Translation B",
    )

    writing = _prepare_question_list(
        exam_data.get("writing", []),
        "Writing",
    )

    # --------------------------------------------------------------
    # 构建模块
    # --------------------------------------------------------------

    blocks = []

    # Listening A/B/C
    for part_data in listening:

        part = part_data["part"]

        if part_data["questions"]:

            blocks.append(
                (
                    f"Listening {part}",
                    part_data["questions"],
                    _validate_single_choice_answers,
                )
            )

    # Single Choice 1 / 2
    if single_choice:

        blocks.append(
            (
                "Single Choice 1",
                single_choice[:5],
                _validate_single_choice_answers,
            )
        )

        if len(single_choice) > 5:

            blocks.append(
                (
                    "Single Choice 2",
                    single_choice[5:],
                    _validate_single_choice_answers,
                )
            )

    # Multiple Choice 1 / 2
    if multiple_choice:

        blocks.append(
            (
                "Multiple Choice 1",
                multiple_choice[:5],
                _validate_multiple_choice_answers,
            )
        )

        if len(multiple_choice) > 5:

            blocks.append(
                (
                    "Multiple Choice 2",
                    multiple_choice[5:],
                    _validate_multiple_choice_answers,
                )
            )

    # Cloze
    for index, block in enumerate(
        cloze,
        start=1,
    ):

        if block["questions"]:

            blocks.append(
                (
                    f"Cloze {index}",
                    block["questions"],
                    _validate_cloze_answers,
                )
            )

    # Reading
    if reading:

        blocks.append(
            (
                "Reading",
                reading,
                _validate_reading_answers,
            )
        )

    # Translation A
    if translation_a:

        blocks.append(
            (
                "Translation A",
                translation_a,
                _validate_translation_answers,
            )
        )

    # Translation B
    if translation_b:

        blocks.append(
            (
                "Translation B",
                translation_b,
                _validate_translation_answers,
            )
        )

    # Writing
    if writing:

        blocks.append(
            (
                "Writing",
                writing,
                _validate_writing_answers,
            )
        )

    print(
        f"✓ 已构建 {len(blocks)} 个答案解析模块"
    )

    # --------------------------------------------------------------
    # 执行模块
    # --------------------------------------------------------------

    result = {
        "title": article_title
        or exam_data.get("title", ""),
        "difficulty": difficulty,
        "article_type": article_type,
        "words": words,
        "modules": [],
    }

    for index, (
        module_name,
        questions,
        validator,
    ) in enumerate(
        blocks,
        start=1,
    ):

        print(
            f"[{index}/{len(blocks)}] "
            f"{module_name}"
        )

        block_result = _run_block(
            module_name,
            questions,
            validator,
        )

        result["modules"].append(
            block_result
        )

    print("=" * 60)
    print(
        f"✓ 答案解析生成完成："
        f"{len(result['modules'])} 个模块"
    )
    print("=" * 60)

    return result


# ======================================================================
# Render
# ======================================================================

def render(
    result,
    article_title="",
    difficulty="",
    article_type="",
):

    lines = []

    title = (
        article_title
        or result.get("title")
        or "英语综合试卷"
    )

    lines.append(
        f"# {title}｜答案与详细解析"
    )
    lines.append("")

    if difficulty:
        lines.append(
            f"- 难度：{difficulty}"
        )

    if article_type:
        lines.append(
            f"- 文章类型：{article_type}"
        )

    lines.append("")

    for module in result.get(
        "modules",
        [],
    ):

        module_name = module.get(
            "module",
            "",
        )

        lines.append(
            f"## {module_name}"
        )
        lines.append("")

        for item in module.get(
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
                answer_text = str(answer)

            lines.append(
                f"### 第 {question} 题"
            )
            lines.append("")
            lines.append(
                f"**答案：{answer_text}**"
            )
            lines.append("")

            if analysis:
                lines.append(
                    f"**解析：** {analysis}"
                )
                lines.append("")

    return "\n".join(lines)


# ======================================================================
# CLI
# ======================================================================

def main():

    if len(sys.argv) < 2:

        print(
            "用法："
            "python exam_answers.py "
            "<exam_data.json>"
        )

        return 1

    input_path = Path(
        sys.argv[1]
    )

    if not input_path.exists():

        print(
            f"文件不存在：{input_path}"
        )

        return 1

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as f:

        exam_data = json.load(f)

    result = generate(
        exam_data
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
