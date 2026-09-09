#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
exam_generate.py V5.1

============================================================
核心架构
============================================================

V4：

    Agnes 一次生成整张试卷
        ↓
    一个超大 JSON
        ↓
    容易 JSON 截断

V5：

    Agnes 分块生成试卷
        ↓
    每个模块独立 JSON
        ↓
    Python 自动合并
        ↓
    完整结构验证

V5.1：

    在 V5 基础上进一步拆分 Multiple Choice：

        Multiple Choice 1
            ↓
        1～5题

        Multiple Choice 2
            ↓
        6～10题

        Python 自动合并
            ↓
        Multiple Choice 1～10

============================================================
本文件只生成：
============================================================

    试卷主体

绝对不生成：

    answers
    analysis
    listening_script

============================================================
固定题量
============================================================

Listening A       5
Listening B       5
Listening C       5

Single Choice    10

Multiple Choice  10
    ├── Batch 1：1～5
    └── Batch 2：6～10

Cloze            10

Reading           5

Translation A     5
Translation B     5

Writing           1

============================================================
生成策略
============================================================

每个模块独立调用 Agnes。

模块：

1. listening_a
2. listening_b
3. listening_c
4. single_choice
5. multiple_choice_1
6. multiple_choice_2
7. cloze
8. reading
9. translation
10. writing

每个模块：

    API 请求
        ↓
    JSON 解析
        ↓
    结构验证
        ↓
    成功
        ↓
    保存到 Python 内存

失败：

    自动重新生成

每个模块最多3次。

============================================================
V5.1 重要保护
============================================================

1. Multiple Choice 拆成两个5题模块。

2. 每个模块独立 max_tokens。

3. 记录 finish_reason。

4. 如果 finish_reason == length：
       明确认为输出达到长度限制。

5. 递归检查禁止答案字段。

6. 所有模块完成以后：
       Python 自动合并。

7. 最终整卷再次验证。

8. 只有完整试卷验证通过：
       才返回 exam。

============================================================
兼容接口
============================================================

generate(
    article,
    difficulty,
    article_type,
    words,
)

render(
    exam,
    article_title,
    difficulty,
    article_type_name,
)

保持不变。

main.py 不需要修改。
"""


import json
import re
import time
from pathlib import Path
from typing import Any

from common import CONFIG, env_required, request_json


# ============================================================
# 基础
# ============================================================

ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# 难度
# ============================================================

DIFFICULTIES = {
    1: {
        "star_name": "一星",
        "stars": "★☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆",
        "level": "小学1-4年级",
    },
    2: {
        "star_name": "二星",
        "stars": "★★☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆",
        "level": "小学高年级-初一",
    },
    3: {
        "star_name": "三星",
        "stars": "★★★☆☆☆☆☆☆☆☆☆☆☆☆☆☆",
        "level": "初二-初四",
    },
    4: {
        "star_name": "四星",
        "stars": "★★★★☆☆☆☆☆☆☆☆☆☆☆☆☆",
        "level": "高一",
    },
    5: {
        "star_name": "五星",
        "stars": "★★★★★☆☆☆☆☆☆☆☆☆☆☆☆",
        "level": "高二",
    },
    6: {
        "star_name": "六星",
        "stars": "★★★★★★☆☆☆☆☆☆☆☆☆☆☆",
        "level": "高三",
    },
    7: {
        "star_name": "七星",
        "stars": "★★★★★★★☆☆☆☆☆☆☆☆☆☆",
        "level": "大学",
    },
    8: {
        "star_name": "八星",
        "stars": "★★★★★★★★☆☆☆☆☆☆☆☆☆",
        "level": "四级",
    },
    9: {
        "star_name": "九星",
        "stars": "★★★★★★★★★☆☆☆☆☆☆☆☆",
        "level": "六级",
    },
    10: {
        "star_name": "十星",
        "stars": "★★★★★★★★★★☆☆☆☆☆☆☆",
        "level": "专四",
    },
    11: {
        "star_name": "十一星",
        "stars": "★★★★★★★★★★★☆☆☆☆☆☆",
        "level": "专六",
    },
    12: {
        "star_name": "十二星",
        "stars": "★★★★★★★★★★★★☆☆☆☆☆",
        "level": "专八",
    },
    13: {
        "star_name": "十三星",
        "stars": "★★★★★★★★★★★★★☆☆☆☆",
        "level": "考研",
    },
    14: {
        "star_name": "十四星",
        "stars": "★★★★★★★★★★★★★★☆☆☆",
        "level": "考博",
    },
    15: {
        "star_name": "十五星",
        "stars": "★★★★★★★★★★★★★★★☆☆",
        "level": "托福",
    },
    16: {
        "star_name": "十六星",
        "stars": "★★★★★★★★★★★★★★★★☆",
        "level": "雅思",
    },
    17: {
        "star_name": "十七星",
        "stars": "★★★★★★★★★★★★★★★★★",
        "level": "GRE",
    },
}


# ============================================================
# 文章类型
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
# 固定题量
# ============================================================

LISTENING_A_COUNT = 5
LISTENING_B_COUNT = 5
LISTENING_C_COUNT = 5

SINGLE_CHOICE_COUNT = 10
MULTIPLE_CHOICE_COUNT = 10
MULTIPLE_CHOICE_BATCH_SIZE = 5

CLOZE_COUNT = 10

READING_COUNT = 5

TRANSLATION_A_COUNT = 5
TRANSLATION_B_COUNT = 5

WRITING_COUNT = 1


# ============================================================
# V5.1 模块
# ============================================================

MODULES = (
    "listening_a",
    "listening_b",
    "listening_c",
    "single_choice",
    "multiple_choice_1",
    "multiple_choice_2",
    "cloze",
    "reading",
    "translation",
    "writing",
)

MODULE_RETRIES = 3


# ============================================================
# 每个模块独立 token 上限
# ============================================================

MODULE_MAX_TOKENS = {
    "listening_a": 2200,
    "listening_b": 2200,
    "listening_c": 2200,
    "single_choice": 3200,
    "multiple_choice_1": 2200,
    "multiple_choice_2": 2200,
    "cloze": 4000,
    "reading": 2200,
    "translation": 2200,
    "writing": 1200,
}


# ============================================================
# 通用工具
# ============================================================

def _to_text(value: Any) -> str:

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(
        value,
        (int, float, bool),
    ):
        return str(value).strip()

    return str(value).strip()


def _clean_text(value: Any) -> str:

    return re.sub(
        r"\s+",
        " ",
        _to_text(value),
    ).strip()


def _ensure_list(value: Any) -> list:

    if isinstance(value, list):
        return value

    if value is None:
        return []

    return [value]


# ============================================================
# JSON
# ============================================================

def clean_json_content(
    content: str,
) -> str:

    content = _to_text(
        content
    )

    if not content:

        raise ValueError(
            "AI 返回内容为空"
        )

    content = re.sub(
        r"^```(?:json)?\s*",
        "",
        content,
        flags=re.IGNORECASE,
    )

    content = re.sub(
        r"\s*```$",
        "",
        content,
        flags=re.IGNORECASE,
    )

    content = content.strip()

    start = content.find("{")
    end = content.rfind("}")

    if start >= 0 and end > start:

        content = content[
            start:end + 1
        ]

    return content.strip()


def parse_json_response(
    content: str,
) -> dict:

    cleaned = clean_json_content(
        content
    )

    try:

        data = json.loads(
            cleaned
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"AI JSON 解析失败：{exc}"
        ) from exc

    if not isinstance(
        data,
        dict,
    ):

        raise ValueError(
            "AI JSON 顶层必须是 object"
        )

    return data


# ============================================================
# Agnes Response
# ============================================================

def extract_content(
    response: Any,
) -> str:

    if isinstance(
        response,
        str,
    ):
        return response

    if not isinstance(
        response,
        dict,
    ):

        raise ValueError(
            "AI API 返回结构不是 dict"
        )

    choices = response.get(
        "choices"
    )

    if not isinstance(
        choices,
        list,
    ) or not choices:

        raise ValueError(
            "AI API 返回中没有 choices"
        )

    first = choices[0]

    if not isinstance(
        first,
        dict,
    ):

        raise ValueError(
            "AI API choices[0] 格式错误"
        )

    message = first.get(
        "message"
    )

    if isinstance(
        message,
        dict,
    ):

        content = message.get(
            "content"
        )

        if isinstance(
            content,
            str,
        ):

            return content

        if isinstance(
            content,
            list,
        ):

            parts = []

            for item in content:

                if isinstance(
                    item,
                    dict,
                ):

                    text = item.get(
                        "text"
                    )

                    if text:

                        parts.append(
                            _to_text(text)
                        )

            if parts:

                return "\n".join(
                    parts
                )

    text = first.get(
        "text"
    )

    if isinstance(
        text,
        str,
    ):

        return text

    raise ValueError(
        "无法从 AI 返回结果中提取 content"
    )


def get_finish_reason(
    response: Any,
) -> str:

    if not isinstance(
        response,
        dict,
    ):

        return ""

    choices = response.get(
        "choices"
    )

    if not isinstance(
        choices,
        list,
    ) or not choices:

        return ""

    first = choices[0]

    if not isinstance(
        first,
        dict,
    ):

        return ""

    return _to_text(
        first.get(
            "finish_reason"
        )
    )


# ============================================================
# 文章
# ============================================================

def _get_article_en(
    article: dict,
) -> str:

    if not isinstance(
        article,
        dict,
    ):

        raise ValueError(
            "article 必须是 dict"
        )

    article_en = _to_text(
        article.get(
            "article_en"
        )
    )

    if not article_en:

        raise ValueError(
            "article_en 为空"
        )

    return article_en


def _get_article_zh(
    article: dict,
) -> str:

    if not isinstance(
        article,
        dict,
    ):
        return ""

    return _to_text(
        article.get(
            "article_zh"
        )
    )


# ============================================================
# 选项
# ============================================================

def _question_text(
    question: Any,
) -> str:

    if not isinstance(
        question,
        dict,
    ):
        return ""

    for key in (
        "question",
        "stem",
        "text",
        "prompt",
        "sentence",
    ):

        value = question.get(
            key
        )

        if value:

            return _to_text(
                value
            )

    return ""


def _option_text(
    option: Any,
) -> str:

    if isinstance(
        option,
        str,
    ):

        return option.strip()

    if isinstance(
        option,
        dict,
    ):

        for key in (
            "text",
            "option",
            "content",
            "value",
        ):

            value = option.get(
                key
            )

            if value:

                return _to_text(
                    value
                )

    return ""


def _options(
    question: Any,
) -> list:

    if not isinstance(
        question,
        dict,
    ):

        return []

    options = question.get(
        "options"
    )

    if not isinstance(
        options,
        list,
    ):

        return []

    result = []

    for item in options:

        text = _option_text(
            item
        )

        if text:

            result.append(
                text
            )

    return result


# ============================================================
# 禁止答案字段
# ============================================================

FORBIDDEN_FIELDS = {
    "answers",
    "analysis",
    "listening_script",
    "answer",
    "correct_answer",
    "standard_answer",
    "explanation",
    "reference_answer",
    "sample_answer",
    "model_answer",
}


def find_forbidden_fields(
    value: Any,
    path: str = "root",
) -> list[str]:

    found = []

    if isinstance(
        value,
        dict,
    ):

        for key, child in value.items():

            key_text = _to_text(
                key
            )

            if (
                key_text.lower()
                in FORBIDDEN_FIELDS
            ):

                found.append(
                    f"{path}.{key_text}"
                )

            found.extend(
                find_forbidden_fields(
                    child,
                    f"{path}.{key_text}",
                )
            )

    elif isinstance(
        value,
        list,
    ):

        for index, child in enumerate(
            value
        ):

            found.extend(
                find_forbidden_fields(
                    child,
                    f"{path}[{index}]",
                )
            )

    return found


def check_forbidden_fields(
    data: dict,
) -> None:

    found = find_forbidden_fields(
        data
    )

    if found:

        raise ValueError(
            "试卷主体出现禁止字段："
            + ", ".join(found)
        )


# ============================================================
# 通用选择题验证
# ============================================================

def validate_choice_question(
    question: Any,
    section: str,
    index: int,
) -> None:

    if not isinstance(
        question,
        dict,
    ):

        raise ValueError(
            f"{section}第 {index} 题格式错误"
        )

    if not _question_text(
        question
    ):

        raise ValueError(
            f"{section}第 {index} 题题干为空"
        )

    options = _options(
        question
    )

    if len(options) != 4:

        raise ValueError(
            f"{section}第 {index} 题必须有4个选项"
        )


# ============================================================
# 听力模块验证
# ============================================================

def validate_listening_module(
    data: dict,
    part: str,
) -> None:

    if part not in {
        "A",
        "B",
        "C",
    }:

        raise ValueError(
            f"非法听力 Part：{part}"
        )

    instruction = _to_text(
        data.get(
            "instruction"
        )
    )

    if not instruction:

        raise ValueError(
            f"Listening {part} 缺少 instruction"
        )

    questions = data.get(
        "questions"
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            f"Listening {part} questions 必须是 list"
        )

    if len(questions) != 5:

        raise ValueError(
            f"Listening {part} 必须5题，"
            f"实际 {len(questions)}"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        validate_choice_question(
            question,
            f"Listening {part}",
            index,
        )


# ============================================================
# 普通选择题模块验证
# ============================================================

def validate_choice_list(
    data: dict,
    field: str,
    count: int,
    name: str,
) -> None:

    questions = data.get(
        field
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            f"{field} 必须是 list"
        )

    if len(questions) != count:

        raise ValueError(
            f"{name}必须 {count} 题，"
            f"实际 {len(questions)}"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        validate_choice_question(
            question,
            name,
            index,
        )


# ============================================================
# 完形
# ============================================================

def _extract_cloze_numbers(
    passage: str,
) -> list[int]:

    if not passage:
        return []

    patterns = [
        r"_{2,}\s*\((\d+)\)\s*_{2,}",
        r"_{2,}\s*(\d+)\s*_{2,}",
        r"\(\s*(\d+)\s*\)\s*_{2,}",
    ]

    numbers = []

    for pattern in patterns:

        found = re.findall(
            pattern,
            passage,
        )

        if found:

            numbers.extend(
                int(x)
                for x in found
            )

    return sorted(
        set(numbers)
    )


def validate_cloze(
    data: dict,
    article_en: str,
) -> None:

    passage = _to_text(
        data.get(
            "passage"
        )
    )

    if not passage:

        raise ValueError(
            "完形 passage 为空"
        )

    questions = data.get(
        "questions"
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "完形 questions 必须是 list"
        )

    if len(questions) != 10:

        raise ValueError(
            f"完形必须10题，实际{len(questions)}"
        )

    numbers = _extract_cloze_numbers(
        passage
    )

    if numbers != list(
        range(
            1,
            11,
        )
    ):

        raise ValueError(
            "完形必须包含1到10号连续挖空"
        )

    # --------------------------------------------------------
    # 去掉挖空以后检查与原文重合度
    # --------------------------------------------------------

    normalized_passage = re.sub(
        r"_{2,}\s*\(\d+\)\s*_{2,}",
        "",
        passage,
    )

    normalized_passage = re.sub(
        r"\(\s*\d+\s*\)\s*_{2,}",
        "",
        normalized_passage,
    )

    normalized_passage = re.sub(
        r"\s+",
        " ",
        normalized_passage,
    ).strip()

    normalized_article = re.sub(
        r"\s+",
        " ",
        article_en,
    ).strip()

    article_words = (
        normalized_article.split()
    )

    passage_words = (
        normalized_passage.split()
    )

    if not article_words:

        raise ValueError(
            "article_en 为空"
        )

    passage_set = {
        word.lower()
        for word in passage_words
    }

    matched = sum(
        1
        for word in article_words
        if word.lower()
        in passage_set
    )

    ratio = (
        matched
        / len(article_words)
    )

    if ratio < 0.85:

        raise ValueError(
            "完形没有保持 article_en 原文，"
            f"原文重合率只有 {ratio:.1%}"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        if not isinstance(
            question,
            dict,
        ):

            raise ValueError(
                f"完形第 {index} 题格式错误"
            )

        number = question.get(
            "number",
            index,
        )

        try:

            number = int(
                number
            )

        except Exception:

            raise ValueError(
                f"完形第 {index} 题编号错误"
            )

        if number != index:

            raise ValueError(
                f"完形编号错误："
                f"期望{index}，实际{number}"
            )

        validate_choice_question(
            question,
            "完形",
            index,
        )


# ============================================================
# 翻译
# ============================================================

def validate_translation(
    data: dict,
) -> None:

    part_a = data.get(
        "part_a"
    )

    part_b = data.get(
        "part_b"
    )

    if not isinstance(
        part_a,
        list,
    ):

        raise ValueError(
            "translation.part_a 必须是 list"
        )

    if not isinstance(
        part_b,
        list,
    ):

        raise ValueError(
            "translation.part_b 必须是 list"
        )

    if len(part_a) != 5:

        raise ValueError(
            "汉译英必须5题"
        )

    if len(part_b) != 5:

        raise ValueError(
            "英译汉必须5题"
        )

    for name, questions in (
        ("汉译英", part_a),
        ("英译汉", part_b),
    ):

        for index, question in enumerate(
            questions,
            start=1,
        ):

            if not isinstance(
                question,
                dict,
            ):

                raise ValueError(
                    f"{name}第{index}题格式错误"
                )

            sentence = _to_text(
                question.get(
                    "sentence"
                )
            )

            if not sentence:

                raise ValueError(
                    f"{name}第{index}题句子为空"
                )


# ============================================================
# 写作
# ============================================================

def validate_writing(
    data: dict,
) -> None:

    questions = data.get(
        "writing"
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "writing 必须是 list"
        )

    if len(questions) != 1:

        raise ValueError(
            "writing 必须1题"
        )

    question = questions[0]

    if not isinstance(
        question,
        dict,
    ):

        raise ValueError(
            "writing 题目格式错误"
        )

    text = _to_text(
        question.get(
            "question"
        )
        or question.get(
            "prompt"
        )
        or question.get(
            "task"
        )
    )

    if not text:

        raise ValueError(
            "writing 缺少题目要求"
        )


# ============================================================
# API
# ============================================================

def request_module(
    module: str,
    system_prompt: str,
    user_prompt: str,
    api_key: str,
) -> tuple[dict, str]:

    base_url = _to_text(
        CONFIG["agnes"]["base_url"]
    ).rstrip("/")

    model = _to_text(
        CONFIG["agnes"]["model"]
    )

    url = (
        f"{base_url}/chat/completions"
    )

    max_tokens = MODULE_MAX_TOKENS.get(
        module,
        3000,
    )

    body = {
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

        "temperature": 0.25,

        "max_tokens": max_tokens,
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

    finish_reason = get_finish_reason(
        response
    )

    content = extract_content(
        response
    )

    data = parse_json_response(
        content
    )

    return data, finish_reason


# ============================================================
# Prompt 基础
# ============================================================

def build_common_context(
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> str:

    article_en = _get_article_en(
        article
    )

    article_zh = _get_article_zh(
        article
    )

    difficulty_info = DIFFICULTIES[
        difficulty
    ]

    article_type_name = ARTICLE_TYPES.get(
        article_type,
        article_type,
    )

    target_words = []

    source_words = article.get(
        "target_vocabulary"
    )

    if not isinstance(
        source_words,
        list,
    ):

        source_words = words

    for item in source_words:

        if not isinstance(
            item,
            dict,
        ):

            continue

        word = _to_text(
            item.get(
                "word"
            )
        )

        meaning = _to_text(
            item.get(
                "meaning"
            )
        )

        if word:

            target_words.append(
                {
                    "word": word,
                    "meaning": meaning,
                }
            )

    return f"""
文章标题：
{_to_text(article.get("title"))}

文章类型：
{article_type_name}

考试难度：
{difficulty_info["star_name"]}

对应级别：
{difficulty_info["level"]}

ARTICLE EN：

{article_en}

ARTICLE ZH：

{article_zh}

目标词汇：

{json.dumps(
    target_words,
    ensure_ascii=False,
)}
"""


# ============================================================
# 模块 Prompt
# ============================================================

def build_module_prompt(
    module: str,
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> tuple[str, str]:

    context = build_common_context(
        article,
        difficulty,
        article_type,
        words,
    )

    system = """
你是748686英语学习系统的专业英语考试命题专家。

本次任务只负责生成指定的一个试卷模块。

绝对不要生成：

answers
analysis
listening_script
answer
correct_answer
standard_answer
explanation
reference_answer
sample_answer
model_answer

不要生成任何答案。

不要生成任何解析。

只输出一个严格合法的 JSON object。

不要 Markdown。

不要 ```json。

不要解释。

不要在 JSON 外输出文字。

严格遵守题量。

所有 options 必须恰好4个。
"""


    # ========================================================
    # Listening A
    # ========================================================

    if module == "listening_a":

        user = f"""
{context}

现在只生成：

Listening Part A

严格5题。

Part A 主要考查简单听词、听短句、听基本信息。

每题必须有：

question
options

options 严格4个：

A. ...
B. ...
C. ...
D. ...

不要生成听力原文。

不要生成答案。

不要生成解析。

JSON：

{{
  "instruction": "string",
  "questions": [
    {{
      "number": 1,
      "question": "string",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好5题。
"""


    # ========================================================
    # Listening B
    # ========================================================

    elif module == "listening_b":

        user = f"""
{context}

现在只生成：

Listening Part B

严格5题。

设计为：

“听一段简短对话后回答问题”。

但是：

本 JSON 绝对不能生成对话原文。

只生成：

instruction
question
options

每题必须4个选项：

A
B
C
D

不要生成答案。

不要生成解析。

JSON：

{{
  "instruction": "string",
  "questions": [
    {{
      "number": 1,
      "question": "string",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好5题。
"""


    # ========================================================
    # Listening C
    # ========================================================

    elif module == "listening_c":

        user = f"""
{context}

现在只生成：

Listening Part C

严格5题。

非常重要：

所有题目必须直接围绕 ARTICLE EN。

5题都必须能够根据 ARTICLE EN 回答。

不要重新写文章。

不要生成听力原文。

不要生成答案。

不要生成解析。

每题必须：

A
B
C
D

JSON：

{{
  "instruction": "string",
  "questions": [
    {{
      "number": 1,
      "question": "string",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好5题。
"""


    # ========================================================
    # Single Choice
    # ========================================================

    elif module == "single_choice":

        user = f"""
{context}

现在只生成：

单项选择题。

严格10题。

题目可以考查：

- 目标词汇
- 词义
- 基础语法
- 时态
- 句型
- 文章内容
- 文章语言知识

必须符合当前考试难度。

每题：

question
options

options 严格4个：

A
B
C
D

不要生成答案。

不要生成解析。

JSON：

{{
  "single_choice": [
    {{
      "number": 1,
      "question": "string",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好10题。
"""


    # ========================================================
    # Multiple Choice Batch 1
    # ========================================================

    elif module == "multiple_choice_1":

        user = f"""
{context}

现在只生成：

多项选择题第1～5题。

严格5题。

这是整个多项选择模块的第一批。

题号必须是：

1
2
3
4
5

每题必须：

question
answer_instruction
options

options 严格4个：

A
B
C
D

每题设计为：

Choose all correct answers.

每题应该存在至少两个正确答案。

但是绝对不能输出正确答案。

不要输出解析。

JSON：

{{
  "multiple_choice": [
    {{
      "number": 1,
      "question": "string",
      "answer_instruction": "Choose all correct answers.",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好5题。

只生成1～5题。
"""


    # ========================================================
    # Multiple Choice Batch 2
    # ========================================================

    elif module == "multiple_choice_2":

        user = f"""
{context}

现在只生成：

多项选择题第6～10题。

严格5题。

这是整个多项选择模块的第二批。

题号必须是：

6
7
8
9
10

每题必须：

question
answer_instruction
options

options 严格4个：

A
B
C
D

每题设计为：

Choose all correct answers.

每题应该存在至少两个正确答案。

但是绝对不能输出正确答案。

不要输出解析。

JSON：

{{
  "multiple_choice": [
    {{
      "number": 6,
      "question": "string",
      "answer_instruction": "Choose all correct answers.",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好5题。

只生成6～10题。
"""


    # ========================================================
    # Cloze
    # ========================================================

    elif module == "cloze":

        user = f"""
{context}

现在只生成：

完形填空。

非常重要：

必须直接使用下面的 ARTICLE EN。

绝对不能重新写文章。

ARTICLE EN：

{_get_article_en(article)}

必须保持：

1. 原文全部句子。
2. 原文全部顺序。
3. 原文其他文字不改变。

只允许从原文中选择10个词进行挖空。

严格使用：

____ (1) ____

____ (2) ____

一直到：

____ (10) ____

然后为10个空分别生成选择题。

每题：

A
B
C
D

不要生成答案。

不要生成解析。

JSON：

{{
  "passage": "完整ARTICLE EN，其中有10个挖空",
  "questions": [
    {{
      "number": 1,
      "question": "string",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好10题。
"""


    # ========================================================
    # Reading
    # ========================================================

    elif module == "reading":

        user = f"""
{context}

现在只生成：

阅读理解5题。

非常重要：

不要重新生成阅读文章。

阅读文章就是：

ARTICLE EN

5道题必须全部能够从 ARTICLE EN 找到依据。

每题：

A
B
C
D

不要生成答案。

不要生成解析。

JSON：

{{
  "reading": [
    {{
      "number": 1,
      "question": "string",
      "options": [
        "A. string",
        "B. string",
        "C. string",
        "D. string"
      ]
    }}
  ]
}}

必须正好5题。
"""


    # ========================================================
    # Translation
    # ========================================================

    elif module == "translation":

        user = f"""
{context}

现在只生成：

翻译题。

Part A：

汉译英5题。

Part B：

英译汉5题。

题目必须围绕 ARTICLE EN / ARTICLE ZH。

Part B 的英文句子必须来自 ARTICLE EN。

Part A 的中文句子应该来自 ARTICLE ZH，
或者是 ARTICLE EN 核心句子的自然中文表达。

每题只输出：

number
sentence

绝对不要输出答案。

不要输出解析。

JSON：

{{
  "part_a": [
    {{
      "number": 1,
      "sentence": "中文句子"
    }}
  ],
  "part_b": [
    {{
      "number": 1,
      "sentence": "English sentence"
    }}
  ]
}}

Part A 必须5题。

Part B 必须5题。
"""


    # ========================================================
    # Writing
    # ========================================================

    elif module == "writing":

        user = f"""
{context}

现在只生成：

英语写作题。

严格1题。

写作题必须：

- 与文章主题相关
- 与文章类型相关
- 符合当前考试难度
- 有明确写作任务
- 有明确要求

不要生成参考范文。

不要生成答案。

不要生成解析。

JSON：

{{
  "writing": [
    {{
      "number": 1,
      "question": "string"
    }}
  ]
}}

只能有1题。
"""


    else:

        raise ValueError(
            f"未知试卷模块：{module}"
        )

    return system, user


# ============================================================
# 模块验证
# ============================================================

def validate_module(
    module: str,
    data: dict,
    article: dict,
) -> None:

    if not isinstance(
        data,
        dict,
    ):

        raise ValueError(
            f"{module} 返回结果必须是 object"
        )

    check_forbidden_fields(
        data
    )

    # --------------------------------------------------------
    # Listening
    # --------------------------------------------------------

    if module == "listening_a":

        validate_listening_module(
            data,
            "A",
        )

    elif module == "listening_b":

        validate_listening_module(
            data,
            "B",
        )

    elif module == "listening_c":

        validate_listening_module(
            data,
            "C",
        )

    # --------------------------------------------------------
    # Single
    # --------------------------------------------------------

    elif module == "single_choice":

        validate_choice_list(
            data,
            "single_choice",
            SINGLE_CHOICE_COUNT,
            "单项选择",
        )

    # --------------------------------------------------------
    # Multiple Choice Batch 1
    # --------------------------------------------------------

    elif module == "multiple_choice_1":

        validate_choice_list(
            data,
            "multiple_choice",
            MULTIPLE_CHOICE_BATCH_SIZE,
            "多选题第1～5题",
        )

        questions = data[
            "multiple_choice"
        ]

        expected_numbers = [
            1,
            2,
            3,
            4,
            5,
        ]

        actual_numbers = []

        for question in questions:

            try:

                number = int(
                    question.get(
                        "number"
                    )
                )

            except Exception:

                raise ValueError(
                    "多选题第1～5题存在非法编号"
                )

            actual_numbers.append(
                number
            )

            instruction = _to_text(
                question.get(
                    "answer_instruction"
                )
            )

            if not instruction:

                raise ValueError(
                    "多选题缺少 answer_instruction"
                )

        if actual_numbers != expected_numbers:

            raise ValueError(
                "多选题第一批编号必须为1～5，"
                f"实际为 {actual_numbers}"
            )

    # --------------------------------------------------------
    # Multiple Choice Batch 2
    # --------------------------------------------------------

    elif module == "multiple_choice_2":

        validate_choice_list(
            data,
            "multiple_choice",
            MULTIPLE_CHOICE_BATCH_SIZE,
            "多选题第6～10题",
        )

        questions = data[
            "multiple_choice"
        ]

        expected_numbers = [
            6,
            7,
            8,
            9,
            10,
        ]

        actual_numbers = []

        for question in questions:

            try:

                number = int(
                    question.get(
                        "number"
                    )
                )

            except Exception:

                raise ValueError(
                    "多选题第6～10题存在非法编号"
                )

            actual_numbers.append(
                number
            )

            instruction = _to_text(
                question.get(
                    "answer_instruction"
                )
            )

            if not instruction:

                raise ValueError(
                    "多选题缺少 answer_instruction"
                )

        if actual_numbers != expected_numbers:

            raise ValueError(
                "多选题第二批编号必须为6～10，"
                f"实际为 {actual_numbers}"
            )

    # --------------------------------------------------------
    # Cloze
    # --------------------------------------------------------

    elif module == "cloze":

        validate_cloze(
            data,
            _get_article_en(article),
        )

    # --------------------------------------------------------
    # Reading
    # --------------------------------------------------------

    elif module == "reading":

        validate_choice_list(
            data,
            "reading",
            READING_COUNT,
            "阅读理解",
        )

    # --------------------------------------------------------
    # Translation
    # --------------------------------------------------------

    elif module == "translation":

        validate_translation(
            data
        )

    # --------------------------------------------------------
    # Writing
    # --------------------------------------------------------

    elif module == "writing":

        validate_writing(
            data
        )


# ============================================================
# 单个模块生成
# ============================================================

def generate_module(
    module: str,
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
    api_key: str,
) -> dict:

    system_prompt, user_prompt = (
        build_module_prompt(
            module,
            article,
            difficulty,
            article_type,
            words,
        )
    )

    last_error = None

    for attempt in range(
        1,
        MODULE_RETRIES + 1,
    ):

        print(
            f"    📝 {module} "
            f"{attempt}/{MODULE_RETRIES}"
        )

        try:

            data, finish_reason = (
                request_module(
                    module,
                    system_prompt,
                    user_prompt,
                    api_key,
                )
            )

            if finish_reason:

                print(
                    f"       finish_reason："
                    f"{finish_reason}"
                )

            if finish_reason == "length":

                raise ValueError(
                    "AI 输出达到长度限制，"
                    "JSON 可能被截断"
                )

            validate_module(
                module,
                data,
                article,
            )

            print(
                f"    ✓ {module} "
                "生成并验证成功"
            )

            return data

        except Exception as exc:

            last_error = exc

            print(
                f"    ⚠ {module} 失败：{exc}"
            )

            if attempt < MODULE_RETRIES:

                print(
                    f"    ↻ {module} "
                    "将重新生成..."
                )

                time.sleep(
                    2 * attempt
                )

    raise RuntimeError(
        f"试卷模块 {module} 连续 "
        f"{MODULE_RETRIES} 次失败："
        f"{last_error}"
    )


# ============================================================
# Multiple Choice 合并
# ============================================================

def merge_multiple_choice(
    modules: dict,
) -> list:

    batch_1 = modules[
        "multiple_choice_1"
    ].get(
        "multiple_choice"
    )

    batch_2 = modules[
        "multiple_choice_2"
    ].get(
        "multiple_choice"
    )

    if not isinstance(
        batch_1,
        list,
    ):

        raise ValueError(
            "Multiple Choice 第一批不是 list"
        )

    if not isinstance(
        batch_2,
        list,
    ):

        raise ValueError(
            "Multiple Choice 第二批不是 list"
        )

    if len(batch_1) != 5:

        raise ValueError(
            "Multiple Choice 第一批必须5题"
        )

    if len(batch_2) != 5:

        raise ValueError(
            "Multiple Choice 第二批必须5题"
        )

    merged = []

    for question in batch_1:

        item = dict(
            question
        )

        item["number"] = len(
            merged
        ) + 1

        merged.append(
            item
        )

    for question in batch_2:

        item = dict(
            question
        )

        item["number"] = len(
            merged
        ) + 1

        merged.append(
            item
        )

    if len(merged) != 10:

        raise ValueError(
            "Multiple Choice 合并后不是10题"
        )

    for index, question in enumerate(
        merged,
        start=1,
    ):

        if int(
            question.get(
                "number"
            )
        ) != index:

            raise ValueError(
                f"Multiple Choice 合并后编号错误："
                f"第{index}题"
            )

    return merged


# ============================================================
# 完整试卷合并
# ============================================================

def assemble_exam(
    modules: dict,
    article: dict,
    difficulty: int,
    article_type: str,
) -> dict:

    title = (
        f"{DIFFICULTIES[difficulty]['star_name']}"
        f"·{ARTICLE_TYPES.get(article_type, article_type)}"
        f"英语综合试卷"
    )

    multiple_choice = (
        merge_multiple_choice(
            modules
        )
    )

    exam = {
        "title": title,

        "listening": [
            {
                "part": "A",
                "instruction": modules[
                    "listening_a"
                ]["instruction"],
                "questions": modules[
                    "listening_a"
                ]["questions"],
            },
            {
                "part": "B",
                "instruction": modules[
                    "listening_b"
                ]["instruction"],
                "questions": modules[
                    "listening_b"
                ]["questions"],
            },
            {
                "part": "C",
                "instruction": modules[
                    "listening_c"
                ]["instruction"],
                "questions": modules[
                    "listening_c"
                ]["questions"],
            },
        ],

        "single_choice": modules[
            "single_choice"
        ]["single_choice"],

        "multiple_choice": multiple_choice,

        "cloze": [
            {
                "passage": modules[
                    "cloze"
                ]["passage"],
                "questions": modules[
                    "cloze"
                ]["questions"],
            }
        ],

        "reading": modules[
            "reading"
        ]["reading"],

        "translation": {
            "part_a": modules[
                "translation"
            ]["part_a"],
            "part_b": modules[
                "translation"
            ]["part_b"],
        },

        "writing": modules[
            "writing"
        ]["writing"],
    }

    return exam


# ============================================================
# 完整试卷最终验证
# ============================================================

def validate_exam(
    exam: dict,
    article: dict,
    difficulty: int,
    article_type: str,
) -> None:

    if not isinstance(
        exam,
        dict,
    ):

        raise ValueError(
            "完整试卷必须是 dict"
        )

    required = [
        "title",
        "listening",
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
        "translation",
        "writing",
    ]

    for field in required:

        if field not in exam:

            raise ValueError(
                f"完整试卷缺少字段：{field}"
            )

    check_forbidden_fields(
        exam
    )

    title = _to_text(
        exam.get(
            "title"
        )
    )

    if not title:

        raise ValueError(
            "试卷标题为空"
        )

    # --------------------------------------------------------
    # Listening
    # --------------------------------------------------------

    listening = exam[
        "listening"
    ]

    if not isinstance(
        listening,
        list,
    ):

        raise ValueError(
            "listening 必须是 list"
        )

    if len(listening) != 3:

        raise ValueError(
            "listening 必须有 A/B/C 三部分"
        )

    parts = {
        _to_text(
            item.get(
                "part"
            )
        ).upper(): item
        for item in listening
        if isinstance(item, dict)
    }

    for part in (
        "A",
        "B",
        "C",
    ):

        if part not in parts:

            raise ValueError(
                f"缺少 Listening {part}"
            )

        questions = parts[
            part
        ].get(
            "questions"
        )

        if not isinstance(
            questions,
            list,
        ):

            raise ValueError(
                f"Listening {part} questions 错误"
            )

        if len(questions) != 5:

            raise ValueError(
                f"Listening {part} 必须5题"
            )

        for index, question in enumerate(
            questions,
            start=1,
        ):

            validate_choice_question(
                question,
                f"Listening {part}",
                index,
            )

    # --------------------------------------------------------
    # Single
    # --------------------------------------------------------

    validate_choice_list(
        exam,
        "single_choice",
        SINGLE_CHOICE_COUNT,
        "单项选择",
    )

    # --------------------------------------------------------
    # Multiple
    # --------------------------------------------------------

    validate_choice_list(
        exam,
        "multiple_choice",
        MULTIPLE_CHOICE_COUNT,
        "多选题",
    )

    multiple_questions = exam[
        "multiple_choice"
    ]

    expected_numbers = list(
        range(
            1,
            MULTIPLE_CHOICE_COUNT + 1,
        )
    )

    actual_numbers = []

    for question in multiple_questions:

        try:

            number = int(
                question.get(
                    "number"
                )
            )

        except Exception:

            raise ValueError(
                "多选题存在非法编号"
            )

        actual_numbers.append(
            number
        )

        instruction = _to_text(
            question.get(
                "answer_instruction"
            )
        )

        if not instruction:

            raise ValueError(
                "多选题缺少 answer_instruction"
            )

    if actual_numbers != expected_numbers:

        raise ValueError(
            "完整多选题编号错误："
            f"{actual_numbers}"
        )

    # --------------------------------------------------------
    # Cloze
    # --------------------------------------------------------

    cloze = exam[
        "cloze"
    ]

    if not isinstance(
        cloze,
        list,
    ) or len(cloze) != 1:

        raise ValueError(
            "cloze 必须包含一个 passage"
        )

    validate_cloze(
        cloze[0],
        _get_article_en(article),
    )

    # --------------------------------------------------------
    # Reading
    # --------------------------------------------------------

    validate_choice_list(
        exam,
        "reading",
        READING_COUNT,
        "阅读理解",
    )

    # --------------------------------------------------------
    # Translation
    # --------------------------------------------------------

    validate_translation(
        exam["translation"]
    )

    # --------------------------------------------------------
    # Writing
    # --------------------------------------------------------

    validate_writing(
        exam
    )

    # --------------------------------------------------------
    # 最终题量
    # --------------------------------------------------------

    print()
    print(
        "✓ 完整试卷最终验收通过"
    )

    print(
        "  ✓ Listening A = 5"
    )

    print(
        "  ✓ Listening B = 5"
    )

    print(
        "  ✓ Listening C = 5"
    )

    print(
        "  ✓ Single Choice = 10"
    )

    print(
        "  ✓ Multiple Choice = 10"
    )

    print(
        "  ✓ Cloze = 10"
    )

    print(
        "  ✓ Reading = 5"
    )

    print(
        "  ✓ Translation A = 5"
    )

    print(
        "  ✓ Translation B = 5"
    )

    print(
        "  ✓ Writing = 1"
    )

    print(
        "  ✓ 没有 answers"
    )

    print(
        "  ✓ 没有 analysis"
    )

    print(
        "  ✓ 没有 listening_script"
    )


# ============================================================
# Generate
# ============================================================

def generate(
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> dict:

    api_key_env = CONFIG[
        "agnes"
    ][
        "api_key_env"
    ]

    api_key = env_required(
        api_key_env
    )

    print()
    print(
        "=" * 60
    )

    print(
        "EXAM GENERATION V5.1"
    )

    print(
        "=" * 60
    )

    print(
        f"✓ 难度："
        f"{DIFFICULTIES[difficulty]['star_name']} "
        f"{DIFFICULTIES[difficulty]['stars']}"
    )

    print(
        f"✓ 类型："
        f"{ARTICLE_TYPES.get(article_type, article_type)}"
    )

    article_en = _get_article_en(
        article
    )

    print(
        f"✓ 原文长度："
        f"{len(article_en.split())} words"
    )

    print()
    print(
        "V5.1 分块试卷生成模式："
    )

    print(
        "  ✓ Listening A：5"
    )

    print(
        "  ✓ Listening B：5"
    )

    print(
        "  ✓ Listening C：5"
    )

    print(
        "  ✓ Single Choice：10"
    )

    print(
        "  ✓ Multiple Choice：10"
    )

    print(
        "      ├── Batch 1：1～5"
    )

    print(
        "      └── Batch 2：6～10"
    )

    print(
        "  ✓ Cloze：10"
    )

    print(
        "  ✓ Reading：5"
    )

    print(
        "  ✓ Translation：5 + 5"
    )

    print(
        "  ✓ Writing：1"
    )

    print()
    print(
        "每个模块独立调用 Agnes。"
    )

    print(
        "Multiple Choice 进一步拆成两个5题模块。"
    )

    print(
        "Python 最后自动合并完整试卷。"
    )

    print()

    modules = {}

    total = len(
        MODULES
    )

    # ========================================================
    # 分块生成
    # ========================================================

    for index, module in enumerate(
        MODULES,
        start=1,
    ):

        print()
        print(
            "------------------------------------------------------------"
        )

        print(
            f"EXAM MODULE {index}/{total}"
        )

        print(
            f"MODULE：{module}"
        )

        print(
            "------------------------------------------------------------"
        )

        modules[module] = (
            generate_module(
                module,
                article,
                difficulty,
                article_type,
                words,
                api_key,
            )
        )

        print(
            f"✓ 模块 {module} 已完成"
        )

    # ========================================================
    # Multiple Choice 合并
    # ========================================================

    print()
    print(
        "------------------------------------------------------------"
    )

    print(
        "MERGING MULTIPLE CHOICE"
    )

    print(
        "------------------------------------------------------------"
    )

    multiple_choice = (
        merge_multiple_choice(
            modules
        )
    )

    print(
        "✓ Multiple Choice 第一批：1～5"
    )

    print(
        "✓ Multiple Choice 第二批：6～10"
    )

    print(
        "✓ Multiple Choice 已合并为10题"
    )

    # ========================================================
    # Python 合并完整试卷
    # ========================================================

    print()
    print(
        "=" * 60
    )

    print(
        "ASSEMBLING COMPLETE EXAM"
    )

    print(
        "=" * 60
    )

    exam = assemble_exam(
        modules,
        article,
        difficulty,
        article_type,
    )

    print(
        "✓ 所有模块已经由 Python 合并"
    )

    # ========================================================
    # 最终验证
    # ========================================================

    validate_exam(
        exam,
        article,
        difficulty,
        article_type,
    )

    print()
    print(
        "=" * 60
    )

    print(
        "EXAM GENERATION V5.1 COMPLETE"
    )

    print(
        "=" * 60
    )

    return exam


# ============================================================
# Markdown 工具
# ============================================================

def _render_options(
    options: list,
) -> str:

    lines = []

    for option in options:

        lines.append(
            f"- {_to_text(option)}"
        )

    return "\n".join(
        lines
    )


def _render_question(
    number: int,
    question: dict,
) -> str:

    qtext = _question_text(
        question
    )

    options = _options(
        question
    )

    lines = [
        f"### {number}. {qtext}",
        "",
    ]

    instruction = _to_text(
        question.get(
            "answer_instruction"
        )
    )

    if instruction:

        lines.extend(
            [
                instruction,
                "",
            ]
        )

    lines.extend(
        [
            _render_options(
                options
            ),
            "",
        ]
    )

    return "\n".join(
        lines
    )


# ============================================================
# 听力 Render
# ============================================================

def _render_listening(
    exam: dict,
) -> str:

    parts = {
        _to_text(
            item.get(
                "part"
            )
        ).upper(): item
        for item in exam[
            "listening"
        ]
    }

    lines = [
        "# 一、听力",
        "",
    ]

    for part in (
        "A",
        "B",
        "C",
    ):

        item = parts[
            part
        ]

        lines.append(
            f"## Part {part}"
        )

        lines.append("")

        instruction = _to_text(
            item.get(
                "instruction"
            )
        )

        if instruction:

            lines.extend(
                [
                    instruction,
                    "",
                ]
            )

        for index, question in enumerate(
            item["questions"],
            start=1,
        ):

            lines.append(
                _render_question(
                    index,
                    question,
                )
            )

    return "\n".join(
        lines
    )


# ============================================================
# 选择题 Render
# ============================================================

def _render_choice_section(
    title: str,
    questions: list,
    show_answer_blank: bool = False,
) -> str:

    lines = [
        f"# {title}",
        "",
    ]

    for index, question in enumerate(
        questions,
        start=1,
    ):

        qtext = _question_text(
            question
        )

        lines.extend(
            [
                f"### {index}. {qtext}",
                "",
            ]
        )

        if show_answer_blank:

            lines.extend(
                [
                    "**作答：________________**",
                    "",
                ]
            )

        instruction = _to_text(
            question.get(
                "answer_instruction"
            )
        )

        if instruction:

            lines.extend(
                [
                    instruction,
                    "",
                ]
            )

        lines.extend(
            [
                _render_options(
                    _options(
                        question
                    )
                ),
                "",
            ]
        )

    return "\n".join(
        lines
    )


# ============================================================
# 完形 Render
# ============================================================

def _render_cloze(
    exam: dict,
) -> str:

    item = exam[
        "cloze"
    ][0]

    passage = _to_text(
        item.get(
            "passage"
        )
    )

    questions = item[
        "questions"
    ]

    lines = [
        "# 四、完形填空",
        "",
        passage,
        "",
        "## 选择题",
        "",
    ]

    for index, question in enumerate(
        questions,
        start=1,
    ):

        lines.extend(
            [
                f"### {index}.",
                "",
                _render_options(
                    _options(
                        question
                    )
                ),
                "",
            ]
        )

    return "\n".join(
        lines
    )


# ============================================================
# 阅读 Render
# ============================================================

def _render_reading(
    exam: dict,
) -> str:

    lines = [
        "# 五、阅读理解",
        "",
        "请根据本文内容选择正确答案。",
        "",
    ]

    for index, question in enumerate(
        exam[
            "reading"
        ],
        start=1,
    ):

        lines.append(
            _render_question(
                index,
                question,
            )
        )

    return "\n".join(
        lines
    )


# ============================================================
# 翻译 Render
# ============================================================

def _translation_source(
    question: dict,
) -> str:

    return _to_text(
        question.get(
            "sentence"
        )
        or question.get(
            "question"
        )
        or question.get(
            "source"
        )
    )


def _render_translation(
    exam: dict,
) -> str:

    translation = exam[
        "translation"
    ]

    lines = [
        "# 六、翻译",
        "",
        "## Part A 汉译英",
        "",
    ]

    for index, question in enumerate(
        translation[
            "part_a"
        ],
        start=1,
    ):

        lines.extend(
            [
                f"### {index}. "
                f"{_translation_source(question)}",
                "",
                "翻译：____________________________",
                "",
            ]
        )

    lines.extend(
        [
            "## Part B 英译汉",
            "",
        ]
    )

    for index, question in enumerate(
        translation[
            "part_b"
        ],
        start=1,
    ):

        lines.extend(
            [
                f"### {index}. "
                f"{_translation_source(question)}",
                "",
                "翻译：____________________________",
                "",
            ]
        )

    return "\n".join(
        lines
    )


# ============================================================
# 写作 Render
# ============================================================

def _render_writing(
    exam: dict,
) -> str:

    item = exam[
        "writing"
    ][0]

    question = _to_text(
        item.get(
            "question"
        )
        or item.get(
            "prompt"
        )
        or item.get(
            "task"
        )
    )

    return "\n".join(
        [
            "# 七、写作",
            "",
            "### 1.",
            "",
            question,
            "",
            "作文：",
            "",
            "__________________________________________________",
            "",
            "__________________________________________________",
            "",
            "__________________________________________________",
            "",
        ]
    )


# ============================================================
# Markdown Render
# ============================================================

def render(
    exam: dict,
    article_title: str,
    difficulty: int,
    article_type_name: str,
) -> str:

    title = _to_text(
        exam.get(
            "title"
        )
    )

    if not title:

        title = _to_text(
            article_title
        )

    lines = [
        f"# {title}",
        "",
        f"> 难度："
        f"{DIFFICULTIES[difficulty]['star_name']} "
        f"{DIFFICULTIES[difficulty]['stars']}",
        "",
        f"> 级别："
        f"{DIFFICULTIES[difficulty]['level']}",
        "",
        f"> 文体：{article_type_name}",
        "",
        "> 总分：100分",
        "",
        "---",
        "",
    ]

    lines.append(
        _render_listening(
            exam
        )
    )

    lines.extend(
        [
            "",
            _render_choice_section(
                "二、单项选择",
                exam[
                    "single_choice"
                ],
            ),
            "",
            _render_choice_section(
                "三、多选题",
                exam[
                    "multiple_choice"
                ],
                show_answer_blank=True,
            ),
            "",
            _render_cloze(
                exam
            ),
            "",
            _render_reading(
                exam
            ),
            "",
            _render_translation(
                exam
            ),
            "",
            _render_writing(
                exam
            ),
        ]
    )

    return (
        "\n".join(
            lines
        ).strip()
        + "\n"
    )
