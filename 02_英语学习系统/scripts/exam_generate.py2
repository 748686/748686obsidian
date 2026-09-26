#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
exam_generate.py V5.3

============================================================
核心架构
============================================================

V5.3：

    整张试卷
        ↓
    拆成最小稳定生成单元
        ↓
    每个单元独立 API
        ↓
    JSON 解析
        ↓
    独立验证
        ↓
    成功后进入下一个单元
        ↓
    Python 最后统一合并
        ↓
    完整试卷最终验证

============================================================
固定结构
============================================================

Listening A
    5题

Listening B
    5题

Listening C
    5题

Single Choice
    Batch 1：1～5
    Batch 2：6～10

Multiple Choice
    Batch 1：1～5
    Batch 2：6～10

Cloze
    Passage：单独生成
    Questions Batch 1：1～5
    Questions Batch 2：6～10

Reading
    5题

Translation
    Part A 汉译英：1～5
    Part B 英译汉：1～5

Writing
    1题

============================================================
V5.3 Listening 修复
============================================================

Listening A / B / C：

    必须统一输出：

    {
      "instruction": "string",
      "questions": [
        {
          "number": 1,
          "question": "string",
          "options": [
            "A. string",
            "B. string",
            "C. string",
            "D. string"
          ]
        }
      ]
    }

instruction：

    必须存在
    必须是非空字符串

============================================================
重要原则
============================================================

1. 不一次生成超大 JSON。

2. 每个批次最多5题。

3. 完形文章单独生成。

4. 完形第1～5题与第6～10题
   必须使用同一篇完形文章。

5. 每个模块独立重试。

6. 后一个模块失败，不影响前面的模块。

7. 最后 Python 自动合并。

8. 最终整卷再次验证。

9. 绝对不生成：

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

main.py 不需要修改。
"""

import json
import re
import time
from typing import Any

from common import CONFIG, env_required, request_json


# ============================================================
# 难度
# ============================================================

DIFFICULTIES = {
    1: {"star_name": "一星", "stars": "★☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆", "level": "小学1-4年级"},
    2: {"star_name": "二星", "stars": "★★☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆", "level": "小学高年级-初一"},
    3: {"star_name": "三星", "stars": "★★★☆☆☆☆☆☆☆☆☆☆☆☆☆☆", "level": "初二-初四"},
    4: {"star_name": "四星", "stars": "★★★★☆☆☆☆☆☆☆☆☆☆☆☆☆", "level": "高一"},
    5: {"star_name": "五星", "stars": "★★★★★☆☆☆☆☆☆☆☆☆☆☆☆", "level": "高二"},
    6: {"star_name": "六星", "stars": "★★★★★★☆☆☆☆☆☆☆☆☆☆☆", "level": "高三"},
    7: {"star_name": "七星", "stars": "★★★★★★★☆☆☆☆☆☆☆☆☆☆", "level": "大学"},
    8: {"star_name": "八星", "stars": "★★★★★★★★☆☆☆☆☆☆☆☆☆", "level": "四级"},
    9: {"star_name": "九星", "stars": "★★★★★★★★★☆☆☆☆☆☆☆☆", "level": "六级"},
    10: {"star_name": "十星", "stars": "★★★★★★★★★★☆☆☆☆☆☆☆", "level": "专四"},
    11: {"star_name": "十一星", "stars": "★★★★★★★★★★★☆☆☆☆☆☆", "level": "专六"},
    12: {"star_name": "十二星", "stars": "★★★★★★★★★★★★☆☆☆☆☆", "level": "专八"},
    13: {"star_name": "十三星", "stars": "★★★★★★★★★★★★★☆☆☆☆", "level": "考研"},
    14: {"star_name": "十四星", "stars": "★★★★★★★★★★★★★★☆☆☆", "level": "考博"},
    15: {"star_name": "十五星", "stars": "★★★★★★★★★★★★★★★☆☆", "level": "托福"},
    16: {"star_name": "十六星", "stars": "★★★★★★★★★★★★★★★★☆", "level": "雅思"},
    17: {"star_name": "十七星", "stars": "★★★★★★★★★★★★★★★★★", "level": "GRE"},
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

LISTENING_COUNT = 5

SINGLE_CHOICE_COUNT = 10
SINGLE_CHOICE_BATCH_SIZE = 5

MULTIPLE_CHOICE_COUNT = 10
MULTIPLE_CHOICE_BATCH_SIZE = 5

CLOZE_COUNT = 10
CLOZE_BATCH_SIZE = 5

READING_COUNT = 5

TRANSLATION_A_COUNT = 5
TRANSLATION_B_COUNT = 5

WRITING_COUNT = 1


# ============================================================
# 最大重试
# ============================================================

MODULE_RETRIES = 3


# ============================================================
# 每个模块独立 token
# ============================================================

MODULE_MAX_TOKENS = {
    "listening_a": 1800,
    "listening_b": 1800,
    "listening_c": 1800,

    "single_choice_1": 1800,
    "single_choice_2": 1800,

    "multiple_choice_1": 1800,
    "multiple_choice_2": 1800,

    "cloze_passage": 2600,
    "cloze_1": 1800,
    "cloze_2": 1800,

    "reading": 2000,

    "translation_a": 1200,
    "translation_b": 1200,

    "writing": 1000,
}


# ============================================================
# 禁止字段
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


# ============================================================
# 基础工具
# ============================================================

def _to_text(value: Any) -> str:

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, (int, float, bool)):
        return str(value).strip()

    return str(value).strip()


def _clean_text(value: Any) -> str:

    return re.sub(
        r"\s+",
        " ",
        _to_text(value),
    ).strip()


# ============================================================
# JSON 清理
# ============================================================

def clean_json_content(content: str) -> str:

    content = _to_text(content)

    if not content:
        raise ValueError("AI 返回内容为空")

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
        content = content[start:end + 1]

    return content.strip()


def parse_json_response(content: str) -> dict:

    cleaned = clean_json_content(content)

    try:
        data = json.loads(cleaned)

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"AI JSON 解析失败：{exc}"
        ) from exc

    if not isinstance(data, dict):

        raise ValueError(
            "AI JSON 顶层必须是 object"
        )

    return data


# ============================================================
# Agnes Response
# ============================================================

def extract_content(response: Any) -> str:

    if isinstance(response, str):
        return response

    if not isinstance(response, dict):
        raise ValueError("AI API 返回结构不是 dict")

    choices = response.get("choices")

    if not isinstance(choices, list) or not choices:
        raise ValueError("AI API 返回中没有 choices")

    first = choices[0]

    if not isinstance(first, dict):
        raise ValueError("AI API choices[0] 格式错误")

    message = first.get("message")

    if isinstance(message, dict):

        content = message.get("content")

        if isinstance(content, str):
            return content

        if isinstance(content, list):

            parts = []

            for item in content:

                if isinstance(item, dict):

                    text = item.get("text")

                    if text:
                        parts.append(_to_text(text))

            if parts:
                return "\n".join(parts)

    text = first.get("text")

    if isinstance(text, str):
        return text

    raise ValueError(
        "无法从 AI 返回结果中提取 content"
    )


def get_finish_reason(response: Any) -> str:

    if not isinstance(response, dict):
        return ""

    choices = response.get("choices")

    if not isinstance(choices, list) or not choices:
        return ""

    first = choices[0]

    if not isinstance(first, dict):
        return ""

    return _to_text(
        first.get("finish_reason")
    )


# ============================================================
# Article
# ============================================================

def _get_article_en(article: dict) -> str:

    if not isinstance(article, dict):
        raise ValueError("article 必须是 dict")

    value = _to_text(
        article.get("article_en")
    )

    if not value:
        raise ValueError("article_en 为空")

    return value


def _get_article_zh(article: dict) -> str:

    if not isinstance(article, dict):
        return ""

    return _to_text(
        article.get("article_zh")
    )


# ============================================================
# 题目工具
# ============================================================

def _question_text(question: Any) -> str:

    if not isinstance(question, dict):
        return ""

    for key in (
        "question",
        "stem",
        "text",
        "prompt",
        "sentence",
        "task",
    ):

        value = question.get(key)

        if value:
            return _to_text(value)

    return ""


def _option_text(option: Any) -> str:

    if isinstance(option, str):
        return option.strip()

    if isinstance(option, dict):

        for key in (
            "text",
            "option",
            "content",
            "value",
        ):

            value = option.get(key)

            if value:
                return _to_text(value)

    return ""


def _options(question: Any) -> list:

    if not isinstance(question, dict):
        return []

    options = question.get("options")

    if not isinstance(options, list):
        return []

    result = []

    for item in options:

        text = _option_text(item)

        if text:
            result.append(text)

    return result


# ============================================================
# 禁止答案字段检查
# ============================================================

def find_forbidden_fields(
    value: Any,
    path: str = "root",
) -> list[str]:

    found = []

    if isinstance(value, dict):

        for key, child in value.items():

            key_text = _to_text(key)

            if key_text.lower() in FORBIDDEN_FIELDS:

                found.append(
                    f"{path}.{key_text}"
                )

            found.extend(
                find_forbidden_fields(
                    child,
                    f"{path}.{key_text}",
                )
            )

    elif isinstance(value, list):

        for index, child in enumerate(value):

            found.extend(
                find_forbidden_fields(
                    child,
                    f"{path}[{index}]",
                )
            )

    return found


def check_forbidden_fields(data: dict) -> None:

    found = find_forbidden_fields(data)

    if found:

        raise ValueError(
            "试卷主体出现禁止字段："
            + ", ".join(found)
        )


# ============================================================
# 选择题验证
# ============================================================

def validate_choice_question(
    question: Any,
    section: str,
    index: int,
) -> None:

    if not isinstance(question, dict):

        raise ValueError(
            f"{section}第{index}题格式错误"
        )

    if not _question_text(question):

        raise ValueError(
            f"{section}第{index}题题干为空"
        )

    options = _options(question)

    if len(options) != 4:

        raise ValueError(
            f"{section}第{index}题必须有4个选项，"
            f"实际{len(options)}"
        )


def validate_question_batch(
    data: dict,
    field: str,
    expected_numbers: list[int],
    section: str,
) -> None:

    questions = data.get(field)

    if not isinstance(questions, list):

        raise ValueError(
            f"{section}：{field} 必须是 list"
        )

    if len(questions) != len(expected_numbers):

        raise ValueError(
            f"{section}必须{len(expected_numbers)}题，"
            f"实际{len(questions)}题"
        )

    actual_numbers = []

    for index, question in enumerate(
        questions,
        start=1,
    ):

        validate_choice_question(
            question,
            section,
            index,
        )

        try:

            number = int(
                question.get("number")
            )

        except Exception:

            raise ValueError(
                f"{section}存在非法编号"
            )

        actual_numbers.append(number)

    if actual_numbers != expected_numbers:

        raise ValueError(
            f"{section}编号错误："
            f"期望{expected_numbers}，"
            f"实际{actual_numbers}"
        )


# ============================================================
# Listening
# ============================================================

def validate_listening(
    data: dict,
    part: str,
) -> None:

    instruction = _to_text(
        data.get("instruction")
    )

    if not instruction:
        raise ValueError(
            f"Listening {part} 缺少 instruction"
        )

    validate_question_batch(
        data,
        "questions",
        [1, 2, 3, 4, 5],
        f"Listening {part}",
    )


# ============================================================
# 完形文章验证
# ============================================================

def _extract_cloze_numbers(
    passage: str,
) -> list[int]:

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

    return sorted(set(numbers))


def validate_cloze_passage(
    data: dict,
    article_en: str,
) -> None:

    passage = _to_text(
        data.get("passage")
    )

    if not passage:
        raise ValueError(
            "完形 passage 为空"
        )

    numbers = _extract_cloze_numbers(
        passage
    )

    if numbers != list(range(1, 11)):

        raise ValueError(
            "完形必须包含1～10号连续挖空，"
            f"实际检测到：{numbers}"
        )

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

    article_words = normalized_article.split()
    passage_words = normalized_passage.split()

    if not article_words:
        raise ValueError("article_en 为空")

    passage_set = {
        word.lower()
        for word in passage_words
    }

    matched = sum(
        1
        for word in article_words
        if word.lower() in passage_set
    )

    ratio = matched / len(article_words)

    if ratio < 0.85:

        raise ValueError(
            "完形没有保持 ARTICLE EN 原文，"
            f"原文重合率只有 {ratio:.1%}"
        )


def validate_cloze_batch(
    data: dict,
    expected_numbers: list[int],
) -> None:

    validate_question_batch(
        data,
        "questions",
        expected_numbers,
        "完形填空",
    )


# ============================================================
# 翻译验证
# ============================================================

def validate_translation_batch(
    data: dict,
    field: str,
    expected_count: int,
    section: str,
) -> None:

    questions = data.get(field)

    if not isinstance(questions, list):

        raise ValueError(
            f"{section}必须是list"
        )

    if len(questions) != expected_count:

        raise ValueError(
            f"{section}必须{expected_count}题，"
            f"实际{len(questions)}题"
        )

    expected_numbers = list(
        range(1, expected_count + 1)
    )

    actual_numbers = []

    for question in questions:

        if not isinstance(question, dict):

            raise ValueError(
                f"{section}题目格式错误"
            )

        sentence = _to_text(
            question.get("sentence")
        )

        if not sentence:

            raise ValueError(
                f"{section}存在空句子"
            )

        try:

            number = int(
                question.get("number")
            )

        except Exception:

            raise ValueError(
                f"{section}存在非法编号"
            )

        actual_numbers.append(number)

    if actual_numbers != expected_numbers:

        raise ValueError(
            f"{section}编号错误："
            f"{actual_numbers}"
        )


# ============================================================
# Writing
# ============================================================

def validate_writing(data: dict) -> None:

    questions = data.get("writing")

    if not isinstance(questions, list):

        raise ValueError(
            "writing 必须是 list"
        )

    if len(questions) != 1:

        raise ValueError(
            "writing 必须1题"
        )

    question = questions[0]

    if not isinstance(question, dict):

        raise ValueError(
            "writing 题目格式错误"
        )

    text = _to_text(
        question.get("question")
        or question.get("prompt")
        or question.get("task")
    )

    if not text:

        raise ValueError(
            "writing 缺少题目要求"
        )


# ============================================================
# API 请求
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

    url = f"{base_url}/chat/completions"

    max_tokens = MODULE_MAX_TOKENS.get(
        module,
        1800,
    )

    temperature = 0.15

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
        "temperature": temperature,
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

    print(
        f"       返回字符数：{len(content)}"
    )

    if finish_reason:

        print(
            f"       finish_reason："
            f"{finish_reason}"
        )

    if finish_reason == "length":

        raise ValueError(
            "AI 输出达到 max_tokens，"
            "JSON 可能被截断"
        )

    data = parse_json_response(
        content
    )

    return data, finish_reason


# ============================================================
# 公共 Context
# ============================================================

def build_common_context(
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> str:

    article_en = _get_article_en(article)
    article_zh = _get_article_zh(article)

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

    if not isinstance(source_words, list):
        source_words = words

    for item in source_words:

        if not isinstance(item, dict):
            continue

        word = _to_text(
            item.get("word")
        )

        meaning = _to_text(
            item.get("meaning")
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
# 公共 System Prompt
# ============================================================

def build_system_prompt() -> str:

    return """
你是748686英语学习系统的专业英语考试命题专家。

本次任务只负责生成指定的一个试卷模块。

只输出一个严格合法的 JSON object。

禁止：

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

绝对不要输出正确答案。

绝对不要输出解析。

绝对不要输出听力原文。

不要 Markdown。

不要 ```json。

不要 JSON 之外的任何文字。

严格遵守指定题量。

所有选择题 options 必须恰好4个。

JSON 必须完整闭合。
"""


# ============================================================
# Listening 公共 JSON 结构要求
# ============================================================

def build_listening_schema(
    instruction_example: str,
) -> str:

    return f"""
Listening 模块必须严格使用下面的 JSON 结构：

{{
  "instruction": "{instruction_example}",
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

强制要求：

1. instruction 字段必须存在。
2. instruction 必须是非空字符串。
3. questions 必须存在。
4. questions 必须正好5题。
5. number 必须依次为1、2、3、4、5。
6. 每题必须有 question。
7. 每题必须有4个 options。
8. 不得省略 instruction。
9. 不得增加答案字段。
10. 不得增加解析字段。

只输出 JSON object。
"""


# ============================================================
# Prompt
# ============================================================

def build_module_prompt(
    module: str,
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
    cloze_passage: str = "",
) -> tuple[str, str]:

    context = build_common_context(
        article,
        difficulty,
        article_type,
        words,
    )

    system = build_system_prompt()

    # --------------------------------------------------------
    # Listening A
    # --------------------------------------------------------

    if module == "listening_a":

        user = f"""
{context}

生成 Listening Part A。

严格5题。

主要考查：

- 简单听词
- 听短句
- 基本信息

不要生成听力原文。

每题4个选项。

instruction 必须存在且不能为空。

{build_listening_schema(
    "Listen carefully and choose the best answer."
)}

"""


    # --------------------------------------------------------
    # Listening B
    # --------------------------------------------------------

    elif module == "listening_b":

        user = f"""
{context}

生成 Listening Part B。

严格5题。

题型：

听短对话后回答问题。

但是：

1. JSON 中绝对不要生成对话原文。
2. 不要生成 listening_script。
3. 只生成 instruction 和 questions。
4. instruction 必须存在。
5. instruction 必须是非空字符串。
6. 每题必须有4个选项。
7. 必须正好5题。
8. 题号必须是1、2、3、4、5。

{build_listening_schema(
    "Listen to the short conversation and choose the best answer."
)}

"""


    # --------------------------------------------------------
    # Listening C
    # --------------------------------------------------------

    elif module == "listening_c":

        user = f"""
{context}

生成 Listening Part C。

严格5题。

题型：

根据 ARTICLE EN 的主要信息、细节、因果关系或主题设计听力理解题。

重要要求：

1. 所有题目必须围绕 ARTICLE EN。
2. 不要重新生成 ARTICLE EN。
3. 不要生成听力原文。
4. 不要生成 listening_script。
5. instruction 必须存在。
6. instruction 必须是非空字符串。
7. questions 必须正好5题。
8. 每题必须有4个选项。
9. 题号必须是1、2、3、4、5。

{build_listening_schema(
    "Listen carefully and choose the best answer."
)}

"""


    # --------------------------------------------------------
    # Single Choice 1
    # --------------------------------------------------------

    elif module == "single_choice_1":

        user = f"""
{context}

生成单项选择题第1～5题。

严格5题。

题号必须：

1
2
3
4
5

可以考查：

目标词汇、词义、语法、时态、句型、
文章内容、语言知识。

每题4个选项。

不要答案。

不要解析。

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

必须正好5题。
"""


    # --------------------------------------------------------
    # Single Choice 2
    # --------------------------------------------------------

    elif module == "single_choice_2":

        user = f"""
{context}

生成单项选择题第6～10题。

严格5题。

题号必须：

6
7
8
9
10

每题4个选项。

不要答案。

不要解析。

JSON：

{{
  "single_choice": [
    {{
      "number": 6,
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


    # --------------------------------------------------------
    # Multiple Choice 1
    # --------------------------------------------------------

    elif module == "multiple_choice_1":

        user = f"""
{context}

生成多项选择题第1～5题。

严格5题。

题号必须：

1
2
3
4
5

每题使用：

Choose all correct answers.

每题4个选项。

每题设计为至少两个正确答案，
但绝对不要输出正确答案。

question 必须简洁。

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
"""


    # --------------------------------------------------------
    # Multiple Choice 2
    # --------------------------------------------------------

    elif module == "multiple_choice_2":

        user = f"""
{context}

SECOND BATCH。

只生成多项选择题第6～10题。

严格5题。

题号只能是：

6
7
8
9
10

这是一个非常紧凑的 JSON 任务。

不要重复文章。

不要写长背景。

不要解释。

每题只包含：

number
question
answer_instruction
options

options 只能4个。

answer_instruction 固定：

Choose all correct answers.

绝对不要输出答案。

JSON 必须完整闭合。

JSON：

{{
  "multiple_choice": [
    {{
      "number": 6,
      "question": "short question",
      "answer_instruction": "Choose all correct answers.",
      "options": [
        "A. short",
        "B. short",
        "C. short",
        "D. short"
      ]
    }}
  ]
}}

必须正好5题：

6、7、8、9、10。
"""


    # --------------------------------------------------------
    # Cloze Passage
    # --------------------------------------------------------

    elif module == "cloze_passage":

        user = f"""
{context}

现在只生成完形填空文章。

非常重要：

必须直接使用 ARTICLE EN。

绝对不能重新写文章。

保持：

1. 原文全部句子。
2. 原文全部顺序。
3. 原文其他文字尽可能完全不改变。

只从原文中选择10个词挖空。

挖空格式必须严格：

____ (1) ____

____ (2) ____

……

____ (10) ____

只输出 passage。

不要生成题目。

不要生成选项。

不要生成答案。

JSON：

{{
  "passage": "ARTICLE EN，其中有1～10号挖空"
}}

JSON 必须完整闭合。
"""


    # --------------------------------------------------------
    # Cloze Questions 1
    # --------------------------------------------------------

    elif module == "cloze_1":

        user = f"""
{context}

下面是已经确定的完形文章：

{cloze_passage}

现在只生成完形填空第1～5题。

非常重要：

必须基于上面这篇文章。

不要修改文章。

不要重新生成文章。

题号：

1
2
3
4
5

每题4个选项。

题目应围绕对应挖空位置。

不要答案。

不要解析。

JSON：

{{
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


    # --------------------------------------------------------
    # Cloze Questions 2
    # --------------------------------------------------------

    elif module == "cloze_2":

        user = f"""
{context}

下面是已经确定的完形文章：

{cloze_passage}

现在只生成完形填空第6～10题。

非常重要：

必须基于同一篇文章。

不要修改文章。

不要重新生成文章。

题号：

6
7
8
9
10

每题4个选项。

题目应围绕对应挖空位置。

不要答案。

不要解析。

JSON：

{{
  "questions": [
    {{
      "number": 6,
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


    # --------------------------------------------------------
    # Reading
    # --------------------------------------------------------

    elif module == "reading":

        user = f"""
{context}

生成阅读理解。

严格5题。

阅读文章就是 ARTICLE EN。

不要重新生成阅读文章。

所有题目必须能够从 ARTICLE EN 找到依据。

每题4个选项。

不要答案。

不要解析。

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


    # --------------------------------------------------------
    # Translation A
    # --------------------------------------------------------

    elif module == "translation_a":

        user = f"""
{context}

生成汉译英。

严格5题。

题号：

1
2
3
4
5

题目围绕 ARTICLE ZH / ARTICLE EN。

只输出中文原句。

不要英文答案。

不要答案。

不要解析。

JSON：

{{
  "part_a": [
    {{
      "number": 1,
      "sentence": "中文句子"
    }}
  ]
}}

必须正好5题。
"""


    # --------------------------------------------------------
    # Translation B
    # --------------------------------------------------------

    elif module == "translation_b":

        user = f"""
{context}

生成英译汉。

严格5题。

题号：

1
2
3
4
5

英文句子必须来自 ARTICLE EN。

不要中文答案。

不要答案。

不要解析。

JSON：

{{
  "part_b": [
    {{
      "number": 1,
      "sentence": "English sentence"
    }}
  ]
}}

必须正好5题。
"""


    # --------------------------------------------------------
    # Writing
    # --------------------------------------------------------

    elif module == "writing":

        user = f"""
{context}

生成英语写作题。

严格1题。

必须：

- 与文章主题相关
- 与文章类型相关
- 符合当前考试难度
- 有明确任务
- 有明确要求

不要参考范文。

不要答案。

不要解析。

JSON：

{{
  "writing": [
    {{
      "number": 1,
      "question": "string"
    }}
  ]
}}

只能1题。
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

    if not isinstance(data, dict):

        raise ValueError(
            f"{module} 返回结果必须是 object"
        )

    check_forbidden_fields(data)

    if module == "listening_a":
        validate_listening(data, "A")

    elif module == "listening_b":
        validate_listening(data, "B")

    elif module == "listening_c":
        validate_listening(data, "C")

    elif module == "single_choice_1":

        validate_question_batch(
            data,
            "single_choice",
            [1, 2, 3, 4, 5],
            "单项选择第1～5题",
        )

    elif module == "single_choice_2":

        validate_question_batch(
            data,
            "single_choice",
            [6, 7, 8, 9, 10],
            "单项选择第6～10题",
        )

    elif module == "multiple_choice_1":

        validate_question_batch(
            data,
            "multiple_choice",
            [1, 2, 3, 4, 5],
            "多项选择第1～5题",
        )

        for question in data["multiple_choice"]:

            if not _to_text(
                question.get("answer_instruction")
            ):

                raise ValueError(
                    "多项选择第1～5题缺少 answer_instruction"
                )

    elif module == "multiple_choice_2":

        validate_question_batch(
            data,
            "multiple_choice",
            [6, 7, 8, 9, 10],
            "多项选择第6～10题",
        )

        for question in data["multiple_choice"]:

            if not _to_text(
                question.get("answer_instruction")
            ):

                raise ValueError(
                    "多项选择第6～10题缺少 answer_instruction"
                )

    elif module == "cloze_passage":

        validate_cloze_passage(
            data,
            _get_article_en(article),
        )

    elif module == "cloze_1":

        validate_cloze_batch(
            data,
            [1, 2, 3, 4, 5],
        )

    elif module == "cloze_2":

        validate_cloze_batch(
            data,
            [6, 7, 8, 9, 10],
        )

    elif module == "reading":

        validate_question_batch(
            data,
            "reading",
            [1, 2, 3, 4, 5],
            "阅读理解",
        )

    elif module == "translation_a":

        validate_translation_batch(
            data,
            "part_a",
            5,
            "汉译英",
        )

    elif module == "translation_b":

        validate_translation_batch(
            data,
            "part_b",
            5,
            "英译汉",
        )

    elif module == "writing":

        validate_writing(data)


# ============================================================
# 单模块生成
# ============================================================

def generate_module(
    module: str,
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
    api_key: str,
    cloze_passage: str = "",
) -> dict:

    system_prompt, user_prompt = (
        build_module_prompt(
            module,
            article,
            difficulty,
            article_type,
            words,
            cloze_passage,
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

            current_prompt = user_prompt

            if attempt == 2:

                current_prompt += """

SECOND ATTEMPT — STRICT JSON MODE

重新生成。

只输出完整 JSON object。

对于 Listening 模块：

必须包含：

"instruction": "非空字符串"

以及：

"questions": [5题]

不要 Markdown。

不要 ```。

不要解释。

不要答案。

不要解析。

保持指定题量。

JSON 必须完整闭合。
"""

            elif attempt == 3:

                current_prompt += """

THIRD ATTEMPT — ULTRA COMPACT JSON MODE

最后一次尝试。

请极度精简题干和选项。

严格按照要求的题号和题量输出。

对于 Listening A/B/C：

instruction 必须存在且不能为空。

questions 必须正好5题。

每题必须4个 options。

不要任何额外字段。

不要任何额外文字。

确保 JSON 最后完整闭合。
"""

            data, finish_reason = request_module(
                module,
                system_prompt,
                current_prompt,
                api_key,
            )

            if finish_reason == "length":

                raise ValueError(
                    "AI 输出达到长度限制"
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
# 合并5题批次
# ============================================================

def merge_batches(
    first: list,
    second: list,
    expected_count: int,
) -> list:

    if len(first) != expected_count // 2:
        raise ValueError(
            "第一批题目数量错误"
        )

    if len(second) != expected_count // 2:
        raise ValueError(
            "第二批题目数量错误"
        )

    merged = []

    for question in first + second:

        item = dict(question)

        item["number"] = len(merged) + 1

        merged.append(item)

    if len(merged) != expected_count:

        raise ValueError(
            f"批次合并后必须{expected_count}题"
        )

    return merged


# ============================================================
# 完形合并
# ============================================================

def merge_cloze(
    passage: dict,
    batch_1: dict,
    batch_2: dict,
) -> dict:

    questions_1 = batch_1.get(
        "questions"
    )

    questions_2 = batch_2.get(
        "questions"
    )

    merged_questions = merge_batches(
        questions_1,
        questions_2,
        CLOZE_COUNT,
    )

    return {
        "passage": passage["passage"],
        "questions": merged_questions,
    }


# ============================================================
# Multiple Choice
# ============================================================

def merge_multiple_choice(
    modules: dict,
) -> list:

    return merge_batches(
        modules["multiple_choice_1"][
            "multiple_choice"
        ],
        modules["multiple_choice_2"][
            "multiple_choice"
        ],
        MULTIPLE_CHOICE_COUNT,
    )


# ============================================================
# Single Choice
# ============================================================

def merge_single_choice(
    modules: dict,
) -> list:

    return merge_batches(
        modules["single_choice_1"][
            "single_choice"
        ],
        modules["single_choice_2"][
            "single_choice"
        ],
        SINGLE_CHOICE_COUNT,
    )


# ============================================================
# Translation
# ============================================================

def merge_translation(
    modules: dict,
) -> dict:

    return {
        "part_a": modules[
            "translation_a"
        ]["part_a"],

        "part_b": modules[
            "translation_b"
        ]["part_b"],
    }


# ============================================================
# Assemble
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

        "single_choice": merge_single_choice(
            modules
        ),

        "multiple_choice": merge_multiple_choice(
            modules
        ),

        "cloze": [
            merge_cloze(
                modules["cloze_passage"],
                modules["cloze_1"],
                modules["cloze_2"],
            )
        ],

        "reading": modules[
            "reading"
        ]["reading"],

        "translation": merge_translation(
            modules
        ),

        "writing": modules[
            "writing"
        ]["writing"],
    }

    return exam


# ============================================================
# 最终验证
# ============================================================

def validate_exam(
    exam: dict,
    article: dict,
    difficulty: int,
    article_type: str,
) -> None:

    if not isinstance(exam, dict):
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

    check_forbidden_fields(exam)

    # --------------------------------------------------------
    # Listening
    # --------------------------------------------------------

    listening = exam["listening"]

    if not isinstance(listening, list):
        raise ValueError(
            "listening 必须是 list"
        )

    if len(listening) != 3:
        raise ValueError(
            "listening 必须有 A/B/C"
        )

    parts = {
        _to_text(item.get("part")).upper(): item
        for item in listening
        if isinstance(item, dict)
    }

    for part in ("A", "B", "C"):

        if part not in parts:
            raise ValueError(
                f"缺少 Listening {part}"
            )

        instruction = _to_text(
            parts[part].get("instruction")
        )

        if not instruction:
            raise ValueError(
                f"Listening {part} 缺少 instruction"
            )

        validate_question_batch(
            parts[part],
            "questions",
            [1, 2, 3, 4, 5],
            f"Listening {part}",
        )

    # --------------------------------------------------------
    # Single
    # --------------------------------------------------------

    validate_question_batch(
        {
            "single_choice": exam[
                "single_choice"
            ]
        },
        "single_choice",
        list(range(1, 11)),
        "单项选择",
    )

    # --------------------------------------------------------
    # Multiple
    # --------------------------------------------------------

    validate_question_batch(
        {
            "multiple_choice": exam[
                "multiple_choice"
            ]
        },
        "multiple_choice",
        list(range(1, 11)),
        "多项选择",
    )

    # --------------------------------------------------------
    # Cloze
    # --------------------------------------------------------

    cloze = exam["cloze"]

    if not isinstance(cloze, list) or len(cloze) != 1:

        raise ValueError(
            "cloze 必须只有一个 passage"
        )

    validate_cloze_passage(
        cloze[0],
        _get_article_en(article),
    )

    validate_cloze_batch(
        {
            "questions": cloze[0]["questions"]
        },
        list(range(1, 11)),
    )

    # --------------------------------------------------------
    # Reading
    # --------------------------------------------------------

    validate_question_batch(
        {
            "reading": exam["reading"]
        },
        "reading",
        [1, 2, 3, 4, 5],
        "阅读理解",
    )

    # --------------------------------------------------------
    # Translation
    # --------------------------------------------------------

    validate_translation_batch(
        exam["translation"],
        "part_a",
        5,
        "汉译英",
    )

    validate_translation_batch(
        exam["translation"],
        "part_b",
        5,
        "英译汉",
    )

    # --------------------------------------------------------
    # Writing
    # --------------------------------------------------------

    validate_writing(exam)

    # --------------------------------------------------------
    # 最终输出
    # --------------------------------------------------------

    print()
    print("✓ 完整试卷最终验收通过")
    print("  ✓ Listening A = 5")
    print("  ✓ Listening B = 5")
    print("  ✓ Listening C = 5")
    print("  ✓ Single Choice = 10")
    print("      ├── 1～5")
    print("      └── 6～10")
    print("  ✓ Multiple Choice = 10")
    print("      ├── 1～5")
    print("      └── 6～10")
    print("  ✓ Cloze = 10")
    print("      ├── Passage")
    print("      ├── 1～5")
    print("      └── 6～10")
    print("  ✓ Reading = 5")
    print("  ✓ Translation A = 5")
    print("  ✓ Translation B = 5")
    print("  ✓ Writing = 1")
    print("  ✓ 没有 answers")
    print("  ✓ 没有 analysis")
    print("  ✓ 没有 listening_script")


# ============================================================
# Generate
# ============================================================

def generate(
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> dict:

    api_key_env = CONFIG["agnes"]["api_key_env"]

    api_key = env_required(api_key_env)

    print()
    print("=" * 60)
    print("EXAM GENERATION V5.3")
    print("=" * 60)

    print(
        f"✓ 难度："
        f"{DIFFICULTIES[difficulty]['star_name']} "
        f"{DIFFICULTIES[difficulty]['stars']}"
    )

    print(
        f"✓ 类型："
        f"{ARTICLE_TYPES.get(article_type, article_type)}"
    )

    article_en = _get_article_en(article)

    print(
        f"✓ 原文长度："
        f"{len(article_en.split())} words"
    )

    print()
    print("V5.3 最小批次独立生成模式：")
    print("  ✓ Listening A：5")
    print("  ✓ Listening B：5")
    print("  ✓ Listening C：5")
    print("  ✓ Single Choice：5 + 5")
    print("  ✓ Multiple Choice：5 + 5")
    print("  ✓ Cloze：Passage + 5 + 5")
    print("  ✓ Reading：5")
    print("  ✓ Translation：5 + 5")
    print("  ✓ Writing：1")

    print()
    print(
        "Listening A/B/C："
        "instruction + 5 questions + 4 options"
    )

    print(
        "每个生成单元独立 API → 验证 → 成功后进入下一单元。"
    )

    modules = {}

    # ========================================================
    # 1. Listening A
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 1")
    print("Listening A：5题")
    print("=" * 60)

    modules["listening_a"] = generate_module(
        "listening_a",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 2. Listening B
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 2")
    print("Listening B：5题")
    print("=" * 60)

    modules["listening_b"] = generate_module(
        "listening_b",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 3. Listening C
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 3")
    print("Listening C：5题")
    print("=" * 60)

    modules["listening_c"] = generate_module(
        "listening_c",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 4. Single Choice 1～5
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 4")
    print("Single Choice：1～5")
    print("=" * 60)

    modules["single_choice_1"] = generate_module(
        "single_choice_1",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 5. Single Choice 6～10
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 5")
    print("Single Choice：6～10")
    print("=" * 60)

    modules["single_choice_2"] = generate_module(
        "single_choice_2",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 6. Multiple Choice 1～5
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 6")
    print("Multiple Choice：1～5")
    print("=" * 60)

    modules["multiple_choice_1"] = generate_module(
        "multiple_choice_1",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 7. Multiple Choice 6～10
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 7")
    print("Multiple Choice：6～10")
    print("=" * 60)

    modules["multiple_choice_2"] = generate_module(
        "multiple_choice_2",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 8. Cloze Passage
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 8")
    print("Cloze Passage：生成完形文章")
    print("=" * 60)

    modules["cloze_passage"] = generate_module(
        "cloze_passage",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    cloze_passage = modules[
        "cloze_passage"
    ]["passage"]

    print()
    print("✓ 完形文章已经确定")
    print("✓ 后续第1～5题、第6～10题必须使用同一篇文章")

    # ========================================================
    # 9. Cloze 1～5
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 9")
    print("Cloze Questions：1～5")
    print("=" * 60)

    modules["cloze_1"] = generate_module(
        "cloze_1",
        article,
        difficulty,
        article_type,
        words,
        api_key,
        cloze_passage,
    )

    # ========================================================
    # 10. Cloze 6～10
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 10")
    print("Cloze Questions：6～10")
    print("=" * 60)

    modules["cloze_2"] = generate_module(
        "cloze_2",
        article,
        difficulty,
        article_type,
        words,
        api_key,
        cloze_passage,
    )

    # ========================================================
    # 11. Reading
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 11")
    print("Reading：5题")
    print("=" * 60)

    modules["reading"] = generate_module(
        "reading",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 12. Translation A
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 12")
    print("Translation A：汉译英 1～5")
    print("=" * 60)

    modules["translation_a"] = generate_module(
        "translation_a",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 13. Translation B
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 13")
    print("Translation B：英译汉 1～5")
    print("=" * 60)

    modules["translation_b"] = generate_module(
        "translation_b",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # 14. Writing
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM UNIT 14")
    print("Writing：1题")
    print("=" * 60)

    modules["writing"] = generate_module(
        "writing",
        article,
        difficulty,
        article_type,
        words,
        api_key,
    )

    # ========================================================
    # Python 合并
    # ========================================================

    print()
    print("=" * 60)
    print("ASSEMBLING COMPLETE EXAM")
    print("=" * 60)

    print("✓ 14个独立生成单元全部完成")

    exam = assemble_exam(
        modules,
        article,
        difficulty,
        article_type,
    )

    print("✓ Python 已合并完整试卷")

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
    print("=" * 60)
    print("EXAM GENERATION V5.3 COMPLETE")
    print("=" * 60)

    return exam


# ============================================================
# Markdown
# ============================================================

def _render_options(options: list) -> str:

    return "\n".join(
        f"- {_to_text(option)}"
        for option in options
    )


def _render_question(
    number: int,
    question: dict,
) -> str:

    qtext = _question_text(question)

    options = _options(question)

    lines = [
        f"### {number}. {qtext}",
        "",
    ]

    instruction = _to_text(
        question.get("answer_instruction")
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
            _render_options(options),
            "",
        ]
    )

    return "\n".join(lines)


# ============================================================
# Listening Render
# ============================================================

def _render_listening(exam: dict) -> str:

    parts = {
        _to_text(item.get("part")).upper(): item
        for item in exam["listening"]
    }

    lines = [
        "# 一、听力",
        "",
    ]

    for part in ("A", "B", "C"):

        item = parts[part]

        lines.append(
            f"## Part {part}"
        )

        lines.append("")

        instruction = _to_text(
            item.get("instruction")
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

    return "\n".join(lines)


# ============================================================
# Choice Render
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

        qtext = _question_text(question)

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
            question.get("answer_instruction")
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
                    _options(question)
                ),
                "",
            ]
        )

    return "\n".join(lines)


# ============================================================
# Cloze Render
# ============================================================

def _render_cloze(exam: dict) -> str:

    item = exam["cloze"][0]

    passage = _to_text(
        item.get("passage")
    )

    questions = item["questions"]

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

        qtext = _question_text(question)

        lines.extend(
            [
                f"### {index}. {qtext}",
                "",
                _render_options(
                    _options(question)
                ),
                "",
            ]
        )

    return "\n".join(lines)


# ============================================================
# Reading Render
# ============================================================

def _render_reading(exam: dict) -> str:

    lines = [
        "# 五、阅读理解",
        "",
        "请根据本文内容选择正确答案。",
        "",
    ]

    for index, question in enumerate(
        exam["reading"],
        start=1,
    ):

        lines.append(
            _render_question(
                index,
                question,
            )
        )

    return "\n".join(lines)


# ============================================================
# Translation Render
# ============================================================

def _translation_source(
    question: dict,
) -> str:

    return _to_text(
        question.get("sentence")
        or question.get("question")
        or question.get("source")
    )


def _render_translation(exam: dict) -> str:

    translation = exam["translation"]

    lines = [
        "# 六、翻译",
        "",
        "## Part A 汉译英",
        "",
    ]

    for index, question in enumerate(
        translation["part_a"],
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
        translation["part_b"],
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

    return "\n".join(lines)


# ============================================================
# Writing Render
# ============================================================

def _render_writing(exam: dict) -> str:

    item = exam["writing"][0]

    question = _to_text(
        item.get("question")
        or item.get("prompt")
        or item.get("task")
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
# Final Markdown Render
# ============================================================

def render(
    exam: dict,
    article_title: str,
    difficulty: int,
    article_type_name: str,
) -> str:

    title = _to_text(
        exam.get("title")
    )

    if not title:
        title = _to_text(article_title)

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
        _render_listening(exam)
    )

    lines.extend(
        [
            "",
            _render_choice_section(
                "二、单项选择",
                exam["single_choice"],
            ),
            "",
            _render_choice_section(
                "三、多选题",
                exam["multiple_choice"],
                show_answer_blank=True,
            ),
            "",
            _render_cloze(exam),
            "",
            _render_reading(exam),
            "",
            _render_translation(exam),
            "",
            _render_writing(exam),
        ]
    )

    return (
        "\n".join(lines).strip()
        + "\n"
    )
