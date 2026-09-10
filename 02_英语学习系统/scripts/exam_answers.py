#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Exam Answers / Analysis Generator V2.0

======================================================================
职责
======================================================================

本文件只负责：

    1. 根据已经生成好的英语试卷生成答案
    2. 生成每一道题的详细解析
    3. 生成听力原文
    4. 生成总体学习分析

======================================================================
绝对规则
======================================================================

本文件不得重新生成：

    listening questions
    single_choice questions
    multiple_choice questions
    cloze questions
    reading questions
    translation questions
    writing questions

也不得修改原试卷。

======================================================================
核心架构
======================================================================

旧版本：

    一次 AI 请求
        ↓
    超大 JSON
        ↓
    全部答案
        +
    全部解析
        +
    全部听力原文
        +
    总体分析

新版本：

    01 Listening A
        ↓
    02 Listening B
        ↓
    03 Listening C
        ↓
    04 Single Choice 1
        ↓
    05 Single Choice 2
        ↓
    06 Multiple Choice 1
        ↓
    07 Multiple Choice 2
        ↓
    08 Cloze 1
        ↓
    09 Cloze 2
        ↓
    10 Reading
        ↓
    11 Translation A
        ↓
    12 Translation B
        ↓
    13 Writing
        ↓
    14 General Analysis
        ↓
    Python 合并
        ↓
    render()

每一个模块独立请求、独立验证、独立重试。

======================================================================
公开接口
======================================================================

generate(exam, article, difficulty, article_type, words)

render(result, article_title, difficulty, article_type_name)

======================================================================
"""

import json
import re
import time
from typing import Any

from common import CONFIG, env_required, request_json


# ======================================================================
# 基础配置
# ======================================================================

SYSTEM_NAME = "748686 英语学习系统"

MAX_BLOCK_ATTEMPTS = 3
TEMPERATURE = 0.2

# 每个小块很小，不再需要以前 12000 token 的超大空间。
MAX_OUTPUT_TOKENS = 3500


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


DIFFICULTY_NAMES = {
    1: "小学1-4年级",
    2: "小学高年级-初一",
    3: "初二-初四",
    4: "高一",
    5: "高二",
    6: "高三",
    7: "大学",
    8: "四级",
    9: "六级",
    10: "专四",
    11: "专六",
    12: "专八",
    13: "考研",
    14: "考博",
    15: "托福",
    16: "雅思",
    17: "GRE",
}


# ======================================================================
# JSON 工具
# ======================================================================

def _clean_json_text(text: str) -> str:
    """清理 AI 返回的 JSON。"""

    if not isinstance(text, str):
        raise ValueError("AI 返回内容不是字符串")

    text = text.strip()

    if not text:
        raise ValueError("AI 返回内容为空")

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        text = text[start:end + 1]

    if not text:
        raise ValueError(
            "AI 返回内容中没有找到 JSON object"
        )

    return text


def _parse_json(text: str) -> dict:

    cleaned = _clean_json_text(text)

    try:
        obj = json.loads(cleaned)

    except json.JSONDecodeError as e:

        preview = cleaned[:500].replace(
            "\n",
            "\\n",
        )

        raise ValueError(
            "AI JSON 解析失败："
            f"{e}\n"
            f"返回内容前500字符：{preview}"
        ) from e

    if not isinstance(obj, dict):
        raise ValueError(
            "AI JSON 顶层必须是 object"
        )

    return obj


# ======================================================================
# API 配置
# ======================================================================

def _api_config():

    agnes = CONFIG["agnes"]

    base_url = agnes["base_url"].rstrip("/")
    model = agnes["model"]
    api_key_env = agnes["api_key_env"]

    api_key = env_required(api_key_env)

    return base_url, model, api_key


# ======================================================================
# API 响应提取
# ======================================================================

def _extract_response_text(response: dict) -> str:

    if not isinstance(response, dict):
        raise ValueError(
            "Agnes API 返回不是 object"
        )

    choices = response.get("choices")

    if not isinstance(choices, list) or not choices:
        raise ValueError(
            "Agnes API 返回缺少 choices"
        )

    choice = choices[0]

    if not isinstance(choice, dict):
        raise ValueError(
            "Agnes API choices[0] 不是 object"
        )

    finish_reason = choice.get(
        "finish_reason"
    )

    print(
        f"    finish_reason：{finish_reason}"
    )

    message = choice.get("message")

    if not isinstance(message, dict):
        raise ValueError(
            "Agnes API 返回缺少 message"
        )

    content = message.get("content")

    if isinstance(content, str):

        text = content.strip()

        print(
            f"    AI 返回字符数：{len(text)}"
        )

        if not text:
            raise ValueError(
                "AI 返回内容为空"
            )

        return text

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, str):

                parts.append(item)

            elif isinstance(item, dict):

                text_value = item.get("text")

                if isinstance(
                    text_value,
                    str,
                ):
                    parts.append(text_value)

        text = "".join(parts).strip()

        print(
            f"    AI 返回字符数：{len(text)}"
        )

        if not text:
            raise ValueError(
                "AI content parts 为空"
            )

        return text

    raise ValueError(
        "无法从 Agnes API 响应中提取文本："
        f"content 类型={type(content).__name__}"
    )


# ======================================================================
# 文章读取
# ======================================================================

def _get_article_en(article: Any) -> str:

    if isinstance(article, dict):

        value = article.get(
            "article_en"
        )

        if isinstance(
            value,
            str,
        ) and value.strip():

            return value.strip()

    raise ValueError(
        "文章缺少 article_en"
    )


def _get_article_zh(article: Any) -> str:

    if isinstance(article, dict):

        value = article.get(
            "article_zh"
        )

        if isinstance(
            value,
            str,
        ) and value.strip():

            return value.strip()

    return ""


def _get_article_title(article: Any) -> str:

    if isinstance(article, dict):

        value = article.get(
            "title"
        )

        if isinstance(
            value,
            str,
        ) and value.strip():

            return value.strip()

    return "英语文章"


def _get_target_words(
    article: Any,
    words: Any,
) -> list:

    if isinstance(words, list):

        return [
            str(x).strip()
            for x in words
            if str(x).strip()
        ]

    if isinstance(article, dict):

        value = article.get(
            "target_vocabulary"
        )

        if isinstance(value, list):

            return [
                str(x).strip()
                for x in value
                if str(x).strip()
            ]

    return []


# ======================================================================
# 试卷计数
# ======================================================================

def _count_exam(exam: dict) -> dict:

    listening = exam.get(
        "listening",
        [],
    )

    if not isinstance(
        listening,
        list,
    ):
        listening = []

    single = exam.get(
        "single_choice",
        [],
    )

    if not isinstance(
        single,
        list,
    ):
        single = []

    multiple = exam.get(
        "multiple_choice",
        [],
    )

    if not isinstance(
        multiple,
        list,
    ):
        multiple = []

    cloze = exam.get(
        "cloze",
        [],
    )

    cloze_count = 0

    if isinstance(
        cloze,
        list,
    ):

        for item in cloze:

            if isinstance(
                item,
                dict,
            ):

                qs = item.get(
                    "questions",
                    [],
                )

                if isinstance(
                    qs,
                    list,
                ):

                    cloze_count += len(qs)

    reading = exam.get(
        "reading",
        [],
    )

    if not isinstance(
        reading,
        list,
    ):
        reading = []

    translation = exam.get(
        "translation",
        {},
    )

    part_a_count = 0
    part_b_count = 0

    if isinstance(
        translation,
        dict,
    ):

        part_a = translation.get(
            "part_a",
            [],
        )

        part_b = translation.get(
            "part_b",
            [],
        )

        if isinstance(
            part_a,
            list,
        ):
            part_a_count = len(part_a)

        if isinstance(
            part_b,
            list,
        ):
            part_b_count = len(part_b)

    writing = exam.get(
        "writing",
        [],
    )

    if not isinstance(
        writing,
        list,
    ):
        writing = []

    return {
        "listening": len(listening),
        "single_choice": len(single),
        "multiple_choice": len(multiple),
        "cloze": cloze_count,
        "reading": len(reading),
        "translation_a": part_a_count,
        "translation_b": part_b_count,
        "writing": len(writing),
    }


# ======================================================================
# 通用题目工具
# ======================================================================

def _question_number(item: dict) -> int:

    value = item.get("question")

    if isinstance(value, int):
        return value

    if isinstance(value, str):

        match = re.search(
            r"\d+",
            value,
        )

        if match:
            return int(match.group())

    raise ValueError(
        f"试卷题目缺少合法 question 编号：{item}"
    )


def _copy_questions(
    questions: list,
) -> list:

    if not isinstance(
        questions,
        list,
    ):
        raise ValueError(
            "题目集合必须是 list"
        )

    result = []

    for item in questions:

        if not isinstance(
            item,
            dict,
        ):
            raise ValueError(
                "试卷中存在非 object 题目"
            )

        result.append(
            item
        )

    return result


def _split_five(
    questions: list,
    name: str,
) -> tuple[list, list]:

    questions = _copy_questions(
        questions
    )

    if len(questions) != 10:

        raise ValueError(
            f"{name} 必须正好有10题，"
            f"实际 {len(questions)}"
        )

    return (
        questions[:5],
        questions[5:],
    )


def _split_cloze(
    exam: dict,
) -> tuple[list, list]:

    cloze = exam.get(
        "cloze",
        [],
    )

    if not isinstance(
        cloze,
        list,
    ):
        raise ValueError(
            "exam.cloze 必须是 list"
        )

    all_questions = []

    for passage in cloze:

        if not isinstance(
            passage,
            dict,
        ):
            continue

        questions = passage.get(
            "questions",
            [],
        )

        if isinstance(
            questions,
            list,
        ):
            all_questions.extend(
                questions
            )

    if len(all_questions) != 10:

        raise ValueError(
            "完形填空必须正好有10题，"
            f"实际 {len(all_questions)}"
        )

    return (
        all_questions[:5],
        all_questions[5:],
    )


# ======================================================================
# API 请求
# ======================================================================

def _request_block(
    block_name: str,
    system_prompt: str,
    user_prompt: str,
) -> dict:

    base_url, model, api_key = _api_config()

    url = f"{base_url}/chat/completions"

    body = {
        "model": model,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_OUTPUT_TOKENS,
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
    }

    response = request_json(
        "POST",
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=body,
    )

    return _parse_json(
        _extract_response_text(
            response
        )
    )


# ======================================================================
# 通用 Prompt
# ======================================================================

def _base_system_prompt(
    difficulty: int,
    article_type: str,
) -> str:

    difficulty_name = DIFFICULTY_NAMES.get(
        difficulty,
        str(difficulty),
    )

    article_type_name = ARTICLE_TYPES.get(
        article_type,
        article_type,
    )

    return f"""
你是“{SYSTEM_NAME}”的英语试卷答案解析专家。

现在你处理的是已经生成完成的正式试卷。

你的任务只有：

1. 根据现有题目给出标准答案
2. 给出每道题的详细解析

绝对禁止：

- 重新出题
- 修改题目
- 修改选项
- 增加题目
- 删除题目
- 改写题目
- 改变题号

难度：
{difficulty}星

难度名称：
{difficulty_name}

文章类型：
{article_type_name}

说明和解析使用中文。

只输出合法 JSON。

不得输出 Markdown。

不得输出 ```json。

不得输出 JSON 之外的任何文字。
""".strip()


# ======================================================================
# Listening Block
# ======================================================================

def _build_listening_payload(
    part_name: str,
    questions: list,
    article_en: str,
    difficulty: int,
    article_type: str,
) -> tuple[str, str]:

    system_prompt = _base_system_prompt(
        difficulty,
        article_type,
    )

    if part_name in (
        "Listening A",
        "Listening B",
    ):

        system_prompt += """

============================================================
听力原文规则
============================================================

本模块除了答案和解析之外，还必须生成听力原文。

每一道题必须对应一个 script。

script 必须能够支持该题的正确答案。

不得修改题目。

不得把多个题目合并成一个 script。

每一道题必须单独一个对象。
"""

        user_prompt = f"""
现在处理：

{part_name}

这一部分只有以下题目：

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2,
)}

请根据这些已经存在的题目生成答案、解析和听力原文。

严格返回：

{{
  "answers": [
    {{
      "question": 1,
      "answer": "A"
    }}
  ],
  "analysis": [
    {{
      "question": 1,
      "analysis": "详细解析"
    }}
  ],
  "scripts": [
    {{
      "question": 1,
      "script": "英文听力原文"
    }}
  ]
}}

要求：

answers 数量必须等于题目数量。

analysis 数量必须等于题目数量。

scripts 数量必须等于题目数量。

question 编号必须与原题完全一致。

只输出 JSON。
"""

        return system_prompt, user_prompt

    # --------------------------------------------------------------
    # Listening C
    # --------------------------------------------------------------

    system_prompt += """

============================================================
Listening Part C 特殊规则
============================================================

Listening Part C 的听力原文不能由你重新生成。

Python 会直接使用 ARTICLE EN 作为 Part C 原文。

因此：

你只需要生成答案和解析。

不得生成 script。

不得修改 ARTICLE EN。
"""

    user_prompt = f"""
现在处理：

Listening Part C

以下是 ARTICLE EN：

==============================
ARTICLE EN
==============================

{article_en}

==============================
现有 Listening Part C 题目
==============================

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2,
)}

严格返回：

{{
  "answers": [
    {{
      "question": 1,
      "answer": "A"
    }}
  ],
  "analysis": [
    {{
      "question": 1,
      "analysis": "详细解析"
    }}
  ]
}}

要求：

answers 数量必须等于题目数量。

analysis 数量必须等于题目数量。

question 编号必须与原题完全一致。

只输出 JSON。
"""

    return system_prompt, user_prompt


# ======================================================================
# 普通选择题 / 阅读 / 完形
# ======================================================================

def _build_question_payload(
    section_name: str,
    questions: list,
    difficulty: int,
    article_type: str,
    article_en: str,
    article_zh: str,
) -> tuple[str, str]:

    system_prompt = _base_system_prompt(
        difficulty,
        article_type,
    )

    user_prompt = f"""
现在处理：

{section_name}

以下是已经存在的正式试题：

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2,
)}

ARTICLE EN：

{article_en}

ARTICLE ZH：

{article_zh}

请严格根据现有试题给出：

1. 标准答案
2. 每一道题的详细解析

严格返回：

{{
  "answers": [
    {{
      "question": 1,
      "answer": "A"
    }}
  ],
  "analysis": [
    {{
      "question": 1,
      "analysis": "详细解析"
    }}
  ]
}}

要求：

answers 数量必须等于输入题目数量。

analysis 数量必须等于输入题目数量。

question 编号必须完全对应原题。

选择题答案只能使用：

A
B
C
D

多项选择题 answer 必须是数组，例如：

["A", "C"]

至少两个正确选项。

每一道题都必须有详细解析。

不得省略。

不得写“同上”。

不得写“见上”。

不得写“略”。

只输出 JSON。
"""

    return system_prompt, user_prompt


# ======================================================================
# Translation
# ======================================================================

def _build_translation_payload(
    part_name: str,
    questions: list,
    difficulty: int,
    article_type: str,
) -> tuple[str, str]:

    system_prompt = _base_system_prompt(
        difficulty,
        article_type,
    )

    if part_name == "Translation A":

        direction = "中译英"

        answer_instruction = """
answer 必须是高质量标准英文参考答案。
"""

    else:

        direction = "英译中"

        answer_instruction = """
answer 必须是准确、自然的中文参考译文。
"""

    user_prompt = f"""
现在处理：

{part_name}

翻译方向：

{direction}

以下是已经存在的正式试题：

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2,
)}

请不要修改原题。

只生成参考答案和逐题解析。

{answer_instruction}

严格返回：

{{
  "answers": [
    {{
      "question": 1,
      "answer": "参考答案"
    }}
  ],
  "analysis": [
    {{
      "question": 1,
      "analysis": "详细解析"
    }}
  ]
}}

要求：

answers 数量必须等于输入题目数量。

analysis 数量必须等于输入题目数量。

question 编号必须完全对应原题。

不得省略任何题目。

只输出 JSON。
"""

    return system_prompt, user_prompt


# ======================================================================
# Writing
# ======================================================================

def _build_writing_payload(
    questions: list,
    difficulty: int,
    article_type: str,
) -> tuple[str, str]:

    system_prompt = _base_system_prompt(
        difficulty,
        article_type,
    )

    user_prompt = f"""
现在处理：

Writing

以下是已经存在的正式写作题：

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2,
)}

不得修改题目。

请为现有写作题生成：

1. 参考范文
2. 写作解析

严格返回：

{{
  "answers": [
    {{
      "question": 1,
      "answer": "完整参考范文"
    }}
  ],
  "analysis": [
    {{
      "question": 1,
      "analysis": "详细写作解析"
    }}
  ]
}}

要求：

answers 数量必须等于题目数量。

analysis 数量必须等于题目数量。

参考范文必须完整。

解析至少包括：

- 写作思路
- 文章结构
- 关键表达
- 语法注意点
- 如何满足题目要求

只输出 JSON。
"""

    return system_prompt, user_prompt


# ======================================================================
# General Analysis
# ======================================================================

def _build_general_payload(
    exam: dict,
    article: dict,
    all_result: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> tuple[str, str]:

    system_prompt = _base_system_prompt(
        difficulty,
        article_type,
    )

    article_en = _get_article_en(
        article
    )

    article_zh = _get_article_zh(
        article
    )

    user_prompt = f"""
现在进入：

General Analysis

前面的所有答案和逐题解析已经由独立模块完成。

你现在不能重新计算题目答案。

你只能根据已经完成的结果进行总体学习分析。

==============================
ARTICLE EN
==============================

{article_en}

==============================
ARTICLE ZH
==============================

{article_zh}

==============================
目标词汇
==============================

{json.dumps(
    words,
    ensure_ascii=False,
)}

==============================
已经完成的答案与解析
==============================

{json.dumps(
    all_result,
    ensure_ascii=False,
    indent=2,
)}

严格返回：

{{
  "summary": "本套试卷总体学习情况总结",
  "grammar": [
    "语法分析"
  ],
  "vocabulary": [
    "词汇分析"
  ],
  "reading": [
    "阅读能力分析"
  ],
  "listening": [
    "听力能力分析"
  ],
  "translation": [
    "翻译能力分析"
  ],
  "writing": [
    "写作能力分析"
  ],
  "study_advice": [
    "具体学习建议"
  ]
}}

要求：

summary 必须非空。

所有数组必须是 list。

内容必须具体。

不能只写空泛的“加强练习”。

必须结合本套文章、题型和答案情况。

只输出 JSON。
"""

    return system_prompt, user_prompt


# ======================================================================
# Block Validators
# ======================================================================

def _validate_question_numbers(
    actual: list,
    expected: list,
    name: str,
):

    if not isinstance(
        actual,
        list,
    ):
        raise ValueError(
            f"{name} 必须是 list"
        )

    if len(actual) != len(expected):

        raise ValueError(
            f"{name} 数量错误："
            f"期望 {len(expected)}，"
            f"实际 {len(actual)}"
        )

    actual_numbers = []

    for item in actual:

        if not isinstance(
            item,
            dict,
        ):
            raise ValueError(
                f"{name} 存在非 object"
            )

        q = item.get(
            "question"
        )

        if not isinstance(
            q,
            int,
        ):
            raise ValueError(
                f"{name} 存在非法 question：{q}"
            )

        actual_numbers.append(q)

    if actual_numbers != expected:

        raise ValueError(
            f"{name} question 编号错误："
            f"期望 {expected}，"
            f"实际 {actual_numbers}"
        )


def _validate_answer_items(
    result: dict,
    expected_questions: list,
    block_name: str,
):

    if not isinstance(
        result,
        dict,
    ):
        raise ValueError(
            f"{block_name} 返回必须是 object"
        )

    answers = result.get(
        "answers"
    )

    analysis = result.get(
        "analysis"
    )

    expected_numbers = [
        _question_number(x)
        for x in expected_questions
    ]

    _validate_question_numbers(
        answers,
        expected_numbers,
        f"{block_name}.answers",
    )

    _validate_question_numbers(
        analysis,
        expected_numbers,
        f"{block_name}.analysis",
    )

    for item in answers:

        answer = item.get(
            "answer"
        )

        if isinstance(
            answer,
            str,
        ):

            if not answer.strip():

                raise ValueError(
                    f"{block_name} "
                    f"第 {item['question']} 题 answer 为空"
                )

        elif isinstance(
            answer,
            list,
        ):

            if len(answer) < 2:

                raise ValueError(
                    f"{block_name} "
                    f"第 {item['question']} 题多选答案不足两个"
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
                        f"第 {item['question']} 题存在非法选项："
                        f"{option}"
                    )

        else:

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题 answer 类型错误"
            )

    for item in analysis:

        text = item.get(
            "analysis"
        )

        if (
            not isinstance(
                text,
                str,
            )
            or not text.strip()
        ):

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题缺少解析"
            )


def _validate_listening_block(
    result: dict,
    expected_questions: list,
    block_name: str,
    require_scripts: bool,
):

    _validate_answer_items(
        result,
        expected_questions,
        block_name,
    )

    if not require_scripts:
        return

    scripts = result.get(
        "scripts"
    )

    expected_numbers = [
        _question_number(x)
        for x in expected_questions
    ]

    _validate_question_numbers(
        scripts,
        expected_numbers,
        f"{block_name}.scripts",
    )

    for item in scripts:

        script = item.get(
            "script"
        )

        if (
            not isinstance(
                script,
                str,
            )
            or not script.strip()
        ):

            raise ValueError(
                f"{block_name} "
                f"第 {item['question']} 题缺少 script"
            )


def _validate_general(
    result: dict,
):

    if not isinstance(
        result,
        dict,
    ):
        raise ValueError(
            "General Analysis 必须是 object"
        )

    summary = result.get(
        "summary"
    )

    if (
        not isinstance(
            summary,
            str,
        )
        or not summary.strip()
    ):

        raise ValueError(
            "general_analysis.summary 不能为空"
        )

    for key in (
        "grammar",
        "vocabulary",
        "reading",
        "listening",
        "translation",
        "writing",
        "study_advice",
    ):

        value = result.get(
            key
        )

        if not isinstance(
            value,
            list,
        ):

            raise ValueError(
                f"general_analysis.{key} 必须是 list"
            )


# ======================================================================
# 单个 Block 执行器
# ======================================================================

def _run_block(
    index: int,
    total: int,
    block_name: str,
    system_prompt: str,
    user_prompt: str,
    validator,
) -> dict:

    print()
    print(
        "------------------------------------------------------------"
    )

    print(
        f"[{index}/{total}] {block_name}"
    )

    print(
        "------------------------------------------------------------"
    )

    last_error = None

    for attempt in range(
        1,
        MAX_BLOCK_ATTEMPTS + 1,
    ):

        print(
            f"  📝 生成尝试 "
            f"{attempt}/{MAX_BLOCK_ATTEMPTS}"
        )

        try:

            result = _request_block(
                block_name,
                system_prompt,
                user_prompt,
            )

            print(
                "  ✓ API 请求成功"
            )

            validator(
                result
            )

            print(
                "  ✓ 模块验收通过"
            )

            return result

        except Exception as e:

            last_error = str(e)

            print(
                f"  ⚠ 模块失败：{last_error}"
            )

            if attempt < MAX_BLOCK_ATTEMPTS:

                time.sleep(
                    2 + attempt
                )

    raise RuntimeError(
        f"{block_name} 连续 "
        f"{MAX_BLOCK_ATTEMPTS} 次失败："
        f"{last_error}"
    )


# ======================================================================
# 生成主函数
# ======================================================================

def generate(
    exam: dict,
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> dict:

    if not isinstance(
        exam,
        dict,
    ):
        raise ValueError(
            "exam 必须是 dict"
        )

    if not isinstance(
        article,
        dict,
    ):
        raise ValueError(
            "article 必须是 dict"
        )

    article_en = _get_article_en(
        article
    )

    article_zh = _get_article_zh(
        article
    )

    # ==============================================================
    # 检查试卷
    # ==============================================================

    counts = _count_exam(
        exam
    )

    print()
    print(
        "=" * 60
    )

    print(
        "STAGE 3 / 3"
    )

    print(
        "EXAM ANSWERS / ANALYSIS GENERATION V2.0"
    )

    print(
        "=" * 60
    )

    print()
    print(
        "本阶段采用独立模块生成。"
    )

    print(
        "任何一个模块失败，只重试当前模块。"
    )

    print()
    print(
        "试卷题目数量："
    )

    print(
        json.dumps(
            counts,
            ensure_ascii=False,
        )
    )

    # ==============================================================
    # 提取 Listening
    # ==============================================================

    listening = _copy_questions(
        exam.get(
            "listening",
            [],
        )
    )

    if len(listening) != 15:

        raise ValueError(
            "Listening 必须正好有15题，"
            f"实际 {len(listening)}"
        )

    listening_a = listening[:5]
    listening_b = listening[5:10]
    listening_c = listening[10:15]

    # ==============================================================
    # Single Choice
    # ==============================================================

    single = _copy_questions(
        exam.get(
            "single_choice",
            [],
        )
    )

    single_1, single_2 = _split_five(
        single,
        "Single Choice",
    )

    # ==============================================================
    # Multiple Choice
    # ==============================================================

    multiple = _copy_questions(
        exam.get(
            "multiple_choice",
            [],
        )
    )

    multiple_1, multiple_2 = _split_five(
        multiple,
        "Multiple Choice",
    )

    # ==============================================================
    # Cloze
    # ==============================================================

    cloze_1, cloze_2 = _split_cloze(
        exam
    )

    # ==============================================================
    # Reading
    # ==============================================================

    reading = _copy_questions(
        exam.get(
            "reading",
            [],
        )
    )

    if len(reading) != 5:

        raise ValueError(
            "Reading 必须正好有5题，"
            f"实际 {len(reading)}"
        )

    # ==============================================================
    # Translation
    # ==============================================================

    translation = exam.get(
        "translation",
        {},
    )

    if not isinstance(
        translation,
        dict,
    ):
        raise ValueError(
            "exam.translation 必须是 object"
        )

    translation_a = _copy_questions(
        translation.get(
            "part_a",
            [],
        )
    )

    translation_b = _copy_questions(
        translation.get(
            "part_b",
            [],
        )
    )

    # ==============================================================
    # Writing
    # ==============================================================

    writing = _copy_questions(
        exam.get(
            "writing",
            [],
        )
    )

    if len(writing) != 1:

        raise ValueError(
            "Writing 当前必须正好有1题，"
            f"实际 {len(writing)}"
        )

    # ==============================================================
    # 最终结果容器
    # ==============================================================

    result = {
        "listening_script": {
            "part_a": [],
            "part_b": [],
            "part_c": article_en,
        },

        "answers": {
            "listening": [],
            "single_choice": [],
            "multiple_choice": [],
            "cloze": [],
            "reading": [],
            "translation": {
                "part_a": [],
                "part_b": [],
            },
            "writing": [],
        },

        "question_analysis": {
            "listening": [],
            "single_choice": [],
            "multiple_choice": [],
            "cloze": [],
            "reading": [],
            "translation": {
                "part_a": [],
                "part_b": [],
            },
            "writing": [],
        },

        "general_analysis": {
            "summary": "",
            "grammar": [],
            "vocabulary": [],
            "reading": [],
            "listening": [],
            "translation": [],
            "writing": [],
            "study_advice": [],
        },
    }

    # ==============================================================
    # Block 1
    # ==============================================================

    system_prompt, user_prompt = _build_listening_payload(
        "Listening A",
        listening_a,
        article_en,
        difficulty,
        article_type,
    )

    block = _run_block(
        1,
        14,
        "Listening A｜5题",
        system_prompt,
        user_prompt,
        lambda x: _validate_listening_block(
            x,
            listening_a,
            "Listening A",
            True,
        ),
    )

    result["answers"]["listening"].extend(
        block["answers"]
    )

    result["question_analysis"]["listening"].extend(
        block["analysis"]
    )

    result["listening_script"]["part_a"] = (
        block["scripts"]
    )

    # ==============================================================
    # Block 2
    # ==============================================================

    system_prompt, user_prompt = _build_listening_payload(
        "Listening B",
        listening_b,
        article_en,
        difficulty,
        article_type,
    )

    block = _run_block(
        2,
        14,
        "Listening B｜5题",
        system_prompt,
        user_prompt,
        lambda x: _validate_listening_block(
            x,
            listening_b,
            "Listening B",
            True,
        ),
    )

    result["answers"]["listening"].extend(
        block["answers"]
    )

    result["question_analysis"]["listening"].extend(
        block["analysis"]
    )

    result["listening_script"]["part_b"] = (
        block["scripts"]
    )

    # ==============================================================
    # Block 3
    # ==============================================================

    system_prompt, user_prompt = _build_listening_payload(
        "Listening C",
        listening_c,
        article_en,
        difficulty,
        article_type,
    )

    block = _run_block(
        3,
        14,
        "Listening C｜5题",
        system_prompt,
        user_prompt,
        lambda x: _validate_listening_block(
            x,
            listening_c,
            "Listening C",
            False,
        ),
    )

    result["answers"]["listening"].extend(
        block["answers"]
    )

    result["question_analysis"]["listening"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 4
    # ==============================================================

    system_prompt, user_prompt = _build_question_payload(
        "Single Choice 1｜第1-5题",
        single_1,
        difficulty,
        article_type,
        article_en,
        article_zh,
    )

    block = _run_block(
        4,
        14,
        "Single Choice 1｜1-5",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            single_1,
            "Single Choice 1",
        ),
    )

    result["answers"]["single_choice"].extend(
        block["answers"]
    )

    result["question_analysis"]["single_choice"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 5
    # ==============================================================

    system_prompt, user_prompt = _build_question_payload(
        "Single Choice 2｜第6-10题",
        single_2,
        difficulty,
        article_type,
        article_en,
        article_zh,
    )

    block = _run_block(
        5,
        14,
        "Single Choice 2｜6-10",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            single_2,
            "Single Choice 2",
        ),
    )

    result["answers"]["single_choice"].extend(
        block["answers"]
    )

    result["question_analysis"]["single_choice"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 6
    # ==============================================================

    system_prompt, user_prompt = _build_question_payload(
        "Multiple Choice 1｜第1-5题",
        multiple_1,
        difficulty,
        article_type,
        article_en,
        article_zh,
    )

    block = _run_block(
        6,
        14,
        "Multiple Choice 1｜1-5",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            multiple_1,
            "Multiple Choice 1",
        ),
    )

    result["answers"]["multiple_choice"].extend(
        block["answers"]
    )

    result["question_analysis"]["multiple_choice"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 7
    # ==============================================================

    system_prompt, user_prompt = _build_question_payload(
        "Multiple Choice 2｜第6-10题",
        multiple_2,
        difficulty,
        article_type,
        article_en,
        article_zh,
    )

    block = _run_block(
        7,
        14,
        "Multiple Choice 2｜6-10",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            multiple_2,
            "Multiple Choice 2",
        ),
    )

    result["answers"]["multiple_choice"].extend(
        block["answers"]
    )

    result["question_analysis"]["multiple_choice"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 8
    # ==============================================================

    system_prompt, user_prompt = _build_question_payload(
        "Cloze 1｜第1-5题",
        cloze_1,
        difficulty,
        article_type,
        article_en,
        article_zh,
    )

    block = _run_block(
        8,
        14,
        "Cloze 1｜1-5",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            cloze_1,
            "Cloze 1",
        ),
    )

    result["answers"]["cloze"].extend(
        block["answers"]
    )

    result["question_analysis"]["cloze"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 9
    # ==============================================================

    system_prompt, user_prompt = _build_question_payload(
        "Cloze 2｜第6-10题",
        cloze_2,
        difficulty,
        article_type,
        article_en,
        article_zh,
    )

    block = _run_block(
        9,
        14,
        "Cloze 2｜6-10",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            cloze_2,
            "Cloze 2",
        ),
    )

    result["answers"]["cloze"].extend(
        block["answers"]
    )

    result["question_analysis"]["cloze"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 10
    # ==============================================================

    system_prompt, user_prompt = _build_question_payload(
        "Reading",
        reading,
        difficulty,
        article_type,
        article_en,
        article_zh,
    )

    block = _run_block(
        10,
        14,
        "Reading｜5题",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            reading,
            "Reading",
        ),
    )

    result["answers"]["reading"].extend(
        block["answers"]
    )

    result["question_analysis"]["reading"].extend(
        block["analysis"]
    )

    # ==============================================================
    # Block 11
    # ==============================================================

    system_prompt, user_prompt = _build_translation_payload(
        "Translation A",
        translation_a,
        difficulty,
        article_type,
    )

    block = _run_block(
        11,
        14,
        "Translation A｜中译英",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            translation_a,
            "Translation A",
        ),
    )

    result["answers"]["translation"]["part_a"] = (
        block["answers"]
    )

    result["question_analysis"]["translation"]["part_a"] = (
        block["analysis"]
    )

    # ==============================================================
    # Block 12
    # ==============================================================

    system_prompt, user_prompt = _build_translation_payload(
        "Translation B",
        translation_b,
        difficulty,
        article_type,
    )

    block = _run_block(
        12,
        14,
        "Translation B｜英译中",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            translation_b,
            "Translation B",
        ),
    )

    result["answers"]["translation"]["part_b"] = (
        block["answers"]
    )

    result["question_analysis"]["translation"]["part_b"] = (
        block["analysis"]
    )

    # ==============================================================
    # Block 13
    # ==============================================================

    system_prompt, user_prompt = _build_writing_payload(
        writing,
        difficulty,
        article_type,
    )

    block = _run_block(
        13,
        14,
        "Writing｜1题",
        system_prompt,
        user_prompt,
        lambda x: _validate_answer_items(
            x,
            writing,
            "Writing",
        ),
    )

    result["answers"]["writing"] = (
        block["answers"]
    )

    result["question_analysis"]["writing"] = (
        block["analysis"]
    )

    # ==============================================================
    # Block 14
    # ==============================================================

    system_prompt, user_prompt = _build_general_payload(
        exam,
        article,
        result,
        difficulty,
        article_type,
        words,
    )

    block = _run_block(
        14,
        14,
        "General Analysis｜总体学习分析",
        system_prompt,
        user_prompt,
        _validate_general,
    )

    result["general_analysis"] = block

    # ==============================================================
    # 最终完整性检查
    # ==============================================================

    _validate_final_result(
        result,
        exam,
        article,
    )

    print()
    print(
        "=" * 60
    )

    print(
        "✓ STAGE 3 ANSWERS / ANALYSIS 全部完成"
    )

    print(
        "✓ 14 个独立模块全部通过验收"
    )

    print(
        "=" * 60
    )

    return result


# ======================================================================
# 最终完整性检查
# ======================================================================

def _validate_final_result(
    result: dict,
    exam: dict,
    article: dict,
) -> None:

    if not isinstance(
        result,
        dict,
    ):
        raise ValueError(
            "最终答案解析结果必须是 object"
        )

    required = {
        "listening_script",
        "answers",
        "question_analysis",
        "general_analysis",
    }

    missing = required - set(
        result.keys()
    )

    if missing:

        raise ValueError(
            f"最终结果缺少字段：{sorted(missing)}"
        )

    counts = _count_exam(
        exam
    )

    # --------------------------------------------------------------
    # Listening
    # --------------------------------------------------------------

    listening_answers = result[
        "answers"
    ]["listening"]

    if len(
        listening_answers
    ) != counts["listening"]:

        raise ValueError(
            "最终 listening 答案数量错误："
            f"期望 {counts['listening']}，"
            f"实际 {len(listening_answers)}"
        )

    listening_analysis = result[
        "question_analysis"
    ]["listening"]

    if len(
        listening_analysis
    ) != counts["listening"]:

        raise ValueError(
            "最终 listening 解析数量错误"
        )

    scripts = result[
        "listening_script"
    ]

    if len(
        scripts["part_a"]
    ) != 5:

        raise ValueError(
            "最终 Listening A 原文必须5条"
        )

    if len(
        scripts["part_b"]
    ) != 5:

        raise ValueError(
            "最终 Listening B 原文必须5条"
        )

    article_en = _get_article_en(
        article
    )

    if scripts[
        "part_c"
    ].strip() != article_en.strip():

        raise ValueError(
            "最终 Listening C 必须与 ARTICLE EN 完全一致"
        )

    # --------------------------------------------------------------
    # 普通题型
    # --------------------------------------------------------------

    for key in (
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
    ):

        answer_count = len(
            result["answers"][key]
        )

        expected_count = counts[key]

        if answer_count != expected_count:

            raise ValueError(
                f"最终 {key} 答案数量错误："
                f"期望 {expected_count}，"
                f"实际 {answer_count}"
            )

        analysis_count = len(
            result[
                "question_analysis"
            ][key]
        )

        if analysis_count != expected_count:

            raise ValueError(
                f"最终 {key} 解析数量错误"
            )

    # --------------------------------------------------------------
    # Translation
    # --------------------------------------------------------------

    translation_answers = result[
        "answers"
    ]["translation"]

    if len(
        translation_answers["part_a"]
    ) != counts["translation_a"]:

        raise ValueError(
            "最终 Translation A 数量错误"
        )

    if len(
        translation_answers["part_b"]
    ) != counts["translation_b"]:

        raise ValueError(
            "最终 Translation B 数量错误"
        )

    # --------------------------------------------------------------
    # Writing
    # --------------------------------------------------------------

    if len(
        result["answers"]["writing"]
    ) != counts["writing"]:

        raise ValueError(
            "最终 Writing 答案数量错误"
        )

    if len(
        result["question_analysis"]["writing"]
    ) != counts["writing"]:

        raise ValueError(
            "最终 Writing 解析数量错误"
        )

    # --------------------------------------------------------------
    # General
    # --------------------------------------------------------------

    _validate_general(
        result["general_analysis"]
    )


# ======================================================================
# Markdown 渲染
# ======================================================================

def _answer_text(
    answer: Any,
) -> str:

    if isinstance(
        answer,
        list,
    ):

        return ", ".join(
            answer
        )

    return str(answer)


def render(
    result: dict,
    article_title: str,
    difficulty: int,
    article_type_name: str,
) -> str:

    difficulty_name = DIFFICULTY_NAMES.get(
        difficulty,
        str(difficulty),
    )

    lines = []

    lines.append(
        f"# {article_title}｜答案与解析"
    )

    lines.append("")

    lines.append(
        f"> 难度：{difficulty}星｜"
        f"{difficulty_name}"
    )

    lines.append(
        f"> 文章类型："
        f"{article_type_name}"
    )

    lines.append("")

    # ==============================================================
    # 一、听力原文
    # ==============================================================

    lines.append(
        "## 一、听力原文"
    )

    lines.append("")

    scripts = result[
        "listening_script"
    ]

    lines.append(
        "### Part A"
    )

    lines.append("")

    for item in scripts[
        "part_a"
    ]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['script']}"
        )

        lines.append("")

    lines.append(
        "### Part B"
    )

    lines.append("")

    for item in scripts[
        "part_b"
    ]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['script']}"
        )

        lines.append("")

    lines.append(
        "### Part C"
    )

    lines.append("")

    lines.append(
        scripts["part_c"]
    )

    lines.append("")

    # ==============================================================
    # 二、答案
    # ==============================================================

    lines.append(
        "## 二、标准答案"
    )

    lines.append("")

    answers = result[
        "answers"
    ]

    answer_sections = [
        (
            "listening",
            "听力",
        ),
        (
            "single_choice",
            "单项选择",
        ),
        (
            "multiple_choice",
            "多项选择",
        ),
        (
            "cloze",
            "完形填空",
        ),
        (
            "reading",
            "阅读理解",
        ),
    ]

    for key, title in answer_sections:

        lines.append(
            f"### {title}"
        )

        lines.append("")

        for item in answers[key]:

            lines.append(
                f"{item['question']}. "
                f"{_answer_text(item['answer'])}"
            )

        lines.append("")

    # ==============================================================
    # 翻译
    # ==============================================================

    translation = answers[
        "translation"
    ]

    lines.append(
        "### 翻译 A：中译英"
    )

    lines.append("")

    for item in translation[
        "part_a"
    ]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['answer']}"
        )

        lines.append("")

    lines.append(
        "### 翻译 B：英译中"
    )

    lines.append("")

    for item in translation[
        "part_b"
    ]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['answer']}"
        )

        lines.append("")

    # ==============================================================
    # 写作
    # ==============================================================

    lines.append(
        "### 写作参考范文"
    )

    lines.append("")

    for item in answers[
        "writing"
    ]:

        lines.append(
            f"**{item['question']}.**"
        )

        lines.append("")

        lines.append(
            item["answer"]
        )

        lines.append("")

    # ==============================================================
    # 三、逐题解析
    # ==============================================================

    lines.append(
        "## 三、逐题解析"
    )

    lines.append("")

    analysis = result[
        "question_analysis"
    ]

    analysis_sections = [
        (
            "listening",
            "听力",
        ),
        (
            "single_choice",
            "单项选择",
        ),
        (
            "multiple_choice",
            "多项选择",
        ),
        (
            "cloze",
            "完形填空",
        ),
        (
            "reading",
            "阅读理解",
        ),
    ]

    for key, title in analysis_sections:

        lines.append(
            f"### {title}"
        )

        lines.append("")

        for item in analysis[key]:

            lines.append(
                f"**第 {item['question']} 题**"
            )

            lines.append("")

            lines.append(
                item["analysis"]
            )

            lines.append("")

    # ==============================================================
    # 翻译解析
    # ==============================================================

    trans_analysis = analysis[
        "translation"
    ]

    lines.append(
        "### 翻译 A：中译英"
    )

    lines.append("")

    for item in trans_analysis[
        "part_a"
    ]:

        lines.append(
            f"**第 {item['question']} 题**"
        )

        lines.append("")

        lines.append(
            item["analysis"]
        )

        lines.append("")

    lines.append(
        "### 翻译 B：英译中"
    )

    lines.append("")

    for item in trans_analysis[
        "part_b"
    ]:

        lines.append(
            f"**第 {item['question']} 题**"
        )

        lines.append("")

        lines.append(
            item["analysis"]
        )

        lines.append("")

    # ==============================================================
    # 写作解析
    # ==============================================================

    lines.append(
        "### 写作"
    )

    lines.append("")

    for item in analysis[
        "writing"
    ]:

        lines.append(
            f"**第 {item['question']} 题**"
        )

        lines.append("")

        lines.append(
            item["analysis"]
        )

        lines.append("")

    # ==============================================================
    # 四、总体学习分析
    # ==============================================================

    general = result[
        "general_analysis"
    ]

    lines.append(
        "## 四、总体学习分析"
    )

    lines.append("")

    lines.append(
        "### 总结"
    )

    lines.append("")

    lines.append(
        general["summary"]
    )

    lines.append("")

    for key, title in [
        (
            "grammar",
            "语法",
        ),
        (
            "vocabulary",
            "词汇",
        ),
        (
            "reading",
            "阅读",
        ),
        (
            "listening",
            "听力",
        ),
        (
            "translation",
            "翻译",
        ),
        (
            "writing",
            "写作",
        ),
        (
            "study_advice",
            "学习建议",
        ),
    ]:

        values = general.get(
            key,
            [],
        )

        if not isinstance(
            values,
            list,
        ):

            values = [
                str(values)
            ]

        lines.append(
            f"### {title}"
        )

        lines.append("")

        for value in values:

            lines.append(
                f"- {value}"
            )

        lines.append("")

    return (
        "\n".join(lines)
        .strip()
        + "\n"
    )


# ======================================================================
# 独立测试入口
# ======================================================================

if __name__ == "__main__":

    print(
        "=" * 70
    )

    print(
        "748686 英语学习系统"
    )

    print(
        "exam_answers.py V2.0"
    )

    print(
        "=" * 70
    )

    print()

    print(
        "本文件是答案 / 解析生成模块。"
    )

    print()

    print(
        "现在采用 14 个独立 AI 模块："
    )

    print()

    modules = [
        "01 Listening A",
        "02 Listening B",
        "03 Listening C",
        "04 Single Choice 1",
        "05 Single Choice 2",
        "06 Multiple Choice 1",
        "07 Multiple Choice 2",
        "08 Cloze 1",
        "09 Cloze 2",
        "10 Reading",
        "11 Translation A",
        "12 Translation B",
        "13 Writing",
        "14 General Analysis",
    ]

    for module in modules:

        print(
            f"  {module}"
        )

    print()

    print(
        "正常情况下由 main.py 调用："
    )

    print()

    print(
        "generate("
        "exam, "
        "article, "
        "difficulty, "
        "article_type, "
        "words"
        ")"
    )
