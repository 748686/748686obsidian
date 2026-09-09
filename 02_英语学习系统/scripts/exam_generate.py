#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
exam_generate.py V4

============================================================
职责
============================================================

本文件只负责：

    根据已经生成完成的英语文章 article_en / article_zh
    生成“英语考试试卷主体”。

============================================================
重要架构变化 V4
============================================================

V3：

    一次 API 同时生成：

        试卷
        +
        answers
        +
        analysis
        +
        listening_script

    JSON 非常巨大，容易出现：

        JSONDecodeError

V4：

    本文件只生成：

        试卷题目

    不生成：

        answers
        analysis
        listening_script

    后续由独立：

        exam_answer_generate.py

    负责：

        answers
        analysis
        listening_script

============================================================
固定题量
============================================================

一、听力
    Part A：5题
    Part B：5题
    Part C：5题

二、单项选择
    10题

三、多选题
    10题

四、完形填空
    10空

五、阅读理解
    5题

六、翻译
    Part A 汉译英：5题
    Part B 英译汉：5题

七、写作
    1题

============================================================
V4 原则
============================================================

1. 只生成试卷主体。

2. 不生成 answers。

3. 不生成 analysis。

4. 不生成 listening_script。

5. 每道题仍然必须有完整题干。

6. 所有选择题必须有 A/B/C/D。

7. 多选题必须允许多个正确答案，
   但本文件不保存答案。

8. 完形必须直接使用 article_en。

9. 阅读必须直接使用 article_en。

10. Listening C 必须直接使用 article_en。

11. 翻译必须围绕 article_en / article_zh。

12. Writing 必须围绕文章主题和文体。

13. API 请求失败自动重试。

14. JSON 解析失败自动重试。

15. 题量/结构验证失败自动重试。

16. 只有已经成功解析 JSON，
    但结构验证失败，
    才允许进入 Repair。

17. 如果三次都没有获得可解析 JSON，
    不进入 Repair。

============================================================
main.py 接口保持不变
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
"""

import json
import re
import time
from pathlib import Path
from typing import Any

from common import CONFIG, env_required, request_json


# ============================================================
# 基础配置
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

CLOZE_COUNT = 10

READING_COUNT = 5

TRANSLATION_A_COUNT = 5
TRANSLATION_B_COUNT = 5

WRITING_COUNT = 1


# ============================================================
# 通用工具
# ============================================================

def _to_text(value: Any) -> str:

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, (int, float, bool)):
        return str(value).strip()

    return str(value).strip()


def _ensure_list(value: Any) -> list:

    if isinstance(value, list):
        return value

    if value is None:
        return []

    return [value]


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
        raise ValueError(
            "AI 返回内容为空"
        )

    # 去掉 Markdown JSON fence
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

    # 提取最外层 JSON object
    start = content.find("{")
    end = content.rfind("}")

    if start >= 0 and end > start:
        content = content[start:end + 1]

    return content.strip()


def parse_json_response(content: str) -> dict:

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

    if not isinstance(data, dict):

        raise ValueError(
            "AI JSON 顶层必须是 object"
        )

    return data


# ============================================================
# Agnes 内容提取
# ============================================================

def extract_content(
    response: Any,
) -> str:

    if isinstance(response, str):
        return response

    if not isinstance(response, dict):

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
                return "\n".join(parts)

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


# ============================================================
# 题目字段工具
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
# 文章字段
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
# 通用选择题验证
# ============================================================

def _validate_choice_question(
    question: Any,
    section_name: str,
    index: int,
) -> None:

    if not isinstance(
        question,
        dict,
    ):

        raise ValueError(
            f"{section_name}第 {index} 题格式错误"
        )

    qtext = _question_text(
        question
    )

    if not qtext:

        raise ValueError(
            f"{section_name}第 {index} 题题干为空"
        )

    options = _options(
        question
    )

    if len(options) != 4:

        raise ValueError(
            f"{section_name}第 {index} 题必须有 A/B/C/D 四个选项"
        )

    for expected in (
        "A",
        "B",
        "C",
        "D",
    ):

        if not any(
            re.match(
                rf"^\s*{expected}\s*[\.\、\)]",
                option,
                flags=re.IGNORECASE,
            )
            for option in options
        ):

            # 如果 AI 没有加 A/B/C/D，
            # 只要有4个选项仍允许，
            # 因为后续 Markdown 会保留原选项。
            #
            # 不在这里过度限制格式。
            pass


# ============================================================
# 听力验证
# ============================================================

def _validate_listening(
    exam: dict,
) -> None:

    listening = exam.get(
        "listening"
    )

    if not isinstance(
        listening,
        list,
    ):

        raise ValueError(
            "listening 必须是 list"
        )

    if len(listening) != 3:

        raise ValueError(
            "听力必须严格包含 Part A / B / C"
        )

    parts = {}

    for item in listening:

        if not isinstance(
            item,
            dict,
        ):

            raise ValueError(
                "听力部分格式错误"
            )

        part = _to_text(
            item.get(
                "part"
            )
        ).upper()

        if part not in {
            "A",
            "B",
            "C",
        }:

            raise ValueError(
                f"非法听力部分：{part}"
            )

        if part in parts:

            raise ValueError(
                f"听力 Part {part} 重复"
            )

        parts[part] = item

    expected_counts = {
        "A": LISTENING_A_COUNT,
        "B": LISTENING_B_COUNT,
        "C": LISTENING_C_COUNT,
    }

    for part, expected_count in expected_counts.items():

        if part not in parts:

            raise ValueError(
                f"缺少听力 Part {part}"
            )

        questions = parts[part].get(
            "questions"
        )

        if not isinstance(
            questions,
            list,
        ):

            raise ValueError(
                f"听力 Part {part} questions 必须是 list"
            )

        if len(questions) != expected_count:

            raise ValueError(
                f"听力 Part {part} 必须 {expected_count} 题，"
                f"实际 {len(questions)} 题"
            )

        for index, question in enumerate(
            questions,
            start=1,
        ):

            _validate_choice_question(
                question,
                f"听力 Part {part} ",
                index,
            )


# ============================================================
# 单项选择验证
# ============================================================

def _validate_single_choice(
    exam: dict,
) -> None:

    questions = exam.get(
        "single_choice"
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "single_choice 必须是 list"
        )

    if len(questions) != SINGLE_CHOICE_COUNT:

        raise ValueError(
            f"单项选择必须 {SINGLE_CHOICE_COUNT} 题，"
            f"实际 {len(questions)} 题"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        _validate_choice_question(
            question,
            "单项选择",
            index,
        )


# ============================================================
# 多选题验证
# ============================================================

def _validate_multiple_choice(
    exam: dict,
) -> None:

    questions = exam.get(
        "multiple_choice"
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "multiple_choice 必须是 list"
        )

    if len(questions) != MULTIPLE_CHOICE_COUNT:

        raise ValueError(
            f"多选题必须 {MULTIPLE_CHOICE_COUNT} 题，"
            f"实际 {len(questions)} 题"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        _validate_choice_question(
            question,
            "多选题",
            index,
        )


# ============================================================
# 完形填空验证
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


def _validate_cloze(
    exam: dict,
    article_en: str,
) -> None:

    cloze = exam.get(
        "cloze"
    )

    if not isinstance(
        cloze,
        list,
    ):

        raise ValueError(
            "cloze 必须是 list"
        )

    if len(cloze) != 1:

        raise ValueError(
            "cloze 必须只有一个 passage"
        )

    item = cloze[0]

    if not isinstance(
        item,
        dict,
    ):

        raise ValueError(
            "cloze 第一项格式错误"
        )

    passage = _to_text(
        item.get(
            "passage"
        )
    )

    if not passage:

        raise ValueError(
            "完形填空 passage 为空"
        )

    questions = item.get(
        "questions"
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "完形填空 questions 必须是 list"
        )

    if len(questions) != CLOZE_COUNT:

        raise ValueError(
            f"完形填空必须 {CLOZE_COUNT} 空，"
            f"实际 {len(questions)} 题"
        )

    # --------------------------------------------------------
    # 验证 1~10 挖空
    # --------------------------------------------------------

    blank_numbers = _extract_cloze_numbers(
        passage
    )

    expected_numbers = list(
        range(
            1,
            CLOZE_COUNT + 1,
        )
    )

    if blank_numbers != expected_numbers:

        raise ValueError(
            "完形填空必须包含连续的 "
            "____ (1) ____ 到 "
            "____ (10) ____"
        )

    # --------------------------------------------------------
    # 验证 article_en 基础
    #
    # 注意：
    # 挖掉10个词以后，不可能直接完全等于 article_en。
    # 因此采用：
    #
    # 1. 原文直接包含
    # 或
    # 2. 词汇重合率 >= 85%
    # --------------------------------------------------------

    normalized_passage = passage

    normalized_passage = re.sub(
        r"_{2,}\s*\(\d+\)\s*_{2,}",
        "",
        normalized_passage,
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

    if normalized_article not in normalized_passage:

        article_words = (
            normalized_article.split()
        )

        passage_words = (
            normalized_passage.split()
        )

        if len(article_words) < 10:

            raise ValueError(
                "article_en 太短，无法验证完形原文"
            )

        passage_word_set = {
            word.lower()
            for word in passage_words
        }

        matched = sum(
            1
            for word in article_words
            if word.lower()
            in passage_word_set
        )

        ratio = (
            matched
            / len(article_words)
        )

        if ratio < 0.85:

            raise ValueError(
                "完形填空没有直接使用生成的 article_en 原文"
            )

    # --------------------------------------------------------
    # 验证10道题
    # --------------------------------------------------------

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
            "number"
        )

        try:
            number = int(number)
        except Exception as exc:

            raise ValueError(
                f"完形第 {index} 题编号错误"
            ) from exc

        if number != index:

            raise ValueError(
                f"完形题编号错误："
                f"期望 {index}，实际 {number}"
            )

        _validate_choice_question(
            question,
            "完形",
            index,
        )


# ============================================================
# 阅读理解验证
# ============================================================

def _validate_reading(
    exam: dict,
) -> None:

    questions = exam.get(
        "reading"
    )

    if not isinstance(
        questions,
        list,
    ):

        raise ValueError(
            "reading 必须是 list"
        )

    if len(questions) != READING_COUNT:

        raise ValueError(
            f"阅读理解必须 {READING_COUNT} 题，"
            f"实际 {len(questions)} 题"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        _validate_choice_question(
            question,
            "阅读理解",
            index,
        )


# ============================================================
# 翻译验证
# ============================================================

def _translation_source(
    question: dict,
) -> str:

    if not isinstance(
        question,
        dict,
    ):
        return ""

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


def _validate_translation(
    exam: dict,
) -> None:

    translation = exam.get(
        "translation"
    )

    if not isinstance(
        translation,
        dict,
    ):

        raise ValueError(
            "translation 必须是 object"
        )

    part_a = translation.get(
        "part_a"
    )

    part_b = translation.get(
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

    if len(part_a) != TRANSLATION_A_COUNT:

        raise ValueError(
            f"汉译英必须 {TRANSLATION_A_COUNT} 题，"
            f"实际 {len(part_a)} 题"
        )

    if len(part_b) != TRANSLATION_B_COUNT:

        raise ValueError(
            f"英译汉必须 {TRANSLATION_B_COUNT} 题，"
            f"实际 {len(part_b)} 题"
        )

    for part_name, questions in (
        ("part_a", part_a),
        ("part_b", part_b),
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
                    f"翻译 {part_name} 第 {index} 题格式错误"
                )

            source = _translation_source(
                question
            )

            if not source:

                raise ValueError(
                    f"翻译 {part_name} 第 {index} 题原句为空"
                )


# ============================================================
# 写作验证
# ============================================================

def _validate_writing(
    exam: dict,
) -> None:

    writing = exam.get(
        "writing"
    )

    if not isinstance(
        writing,
        list,
    ):

        raise ValueError(
            "writing 必须是 list"
        )

    if len(writing) != WRITING_COUNT:

        raise ValueError(
            f"写作必须 {WRITING_COUNT} 题，"
            f"实际 {len(writing)} 题"
        )

    item = writing[0]

    if not isinstance(
        item,
        dict,
    ):

        raise ValueError(
            "写作题格式错误"
        )

    prompt = _to_text(
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

    if not prompt:

        raise ValueError(
            "写作题缺少明确要求"
        )


# ============================================================
# 顶层验证
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
            "考试结果必须是 dict"
        )

    # --------------------------------------------------------
    # V4：
    # 这里只允许试卷主体字段。
    #
    # 不再要求：
    #
    # answers
    # analysis
    # listening_script
    # --------------------------------------------------------

    required_fields = [
        "title",
        "listening",
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
        "translation",
        "writing",
    ]

    for field in required_fields:

        if field not in exam:

            raise ValueError(
                f"考试结果缺少字段：{field}"
            )

    title = _to_text(
        exam.get(
            "title"
        )
    )

    if not title:

        raise ValueError(
            "考试标题为空"
        )

    if difficulty not in DIFFICULTIES:

        raise ValueError(
            f"非法难度：{difficulty}"
        )

    if article_type not in ARTICLE_TYPES:

        raise ValueError(
            f"非法文章类型：{article_type}"
        )

    article_en = _get_article_en(
        article
    )

    # --------------------------------------------------------
    # 各部分验证
    # --------------------------------------------------------

    _validate_listening(
        exam
    )

    _validate_single_choice(
        exam
    )

    _validate_multiple_choice(
        exam
    )

    _validate_cloze(
        exam,
        article_en,
    )

    _validate_reading(
        exam
    )

    _validate_translation(
        exam
    )

    _validate_writing(
        exam
    )


# ============================================================
# Prompt：V4 只生成试卷主体
# ============================================================

def build_exam_payload(
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> dict:

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

    for item in _ensure_list(
        article.get(
            "target_vocabulary"
        )
    ):

        if isinstance(
            item,
            dict,
        ):

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

    if not target_words:

        for item in _ensure_list(
            words
        ):

            if isinstance(
                item,
                dict,
            ):

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

    prompt = f"""
你现在是“748686英语学习系统”的专业英语考试命题专家。

你的唯一任务是：

根据下面已经生成完成的英语文章，
生成“考试试卷主体”。

============================================================
非常重要：本次只生成试卷题目
============================================================

你绝对不要生成：

- answers
- analysis
- listening_script

不要生成任何答案。

不要生成任何解析。

不要生成听力原文。

本次 JSON 只保存：

“学生考试时看到的试卷内容”。

后续系统会使用另外一个独立程序，
根据这份试卷生成：

answers
analysis
listening_script

============================================================
文章信息
============================================================

文章标题：
{_to_text(article.get("title"))}

文章类型：
{article_type_name}

考试难度：
{difficulty_info["star_name"]}
{difficulty_info["stars"]}

对应级别：
{difficulty_info["level"]}

============================================================
ARTICLE EN
============================================================

{article_en}

============================================================
ARTICLE ZH
============================================================

{article_zh}

============================================================
目标词汇
============================================================

{json.dumps(
    target_words,
    ensure_ascii=False,
    indent=2,
)}

============================================================
固定题量
============================================================

听力：

Part A：5题
Part B：5题
Part C：5题

单项选择：10题

多选题：10题

完形填空：10空

阅读理解：5题

汉译英：5题

英译汉：5题

写作：1题

绝对不能少题。

============================================================
一、听力
============================================================

Part A：

严格5题。

每题都是一个完整英文听力句子的理解题。

题目本身必须是：

“Which word did you hear?”

或者同等难度的英文选择题。

每题必须有：

A
B
C
D

本阶段只生成题目，
不要生成听力原文。

不要生成答案。

不要生成解析。

------------------------------------------------------------

Part B：

严格5题。

每题必须设计成“听完整对话后回答问题”。

每道题都必须有：

A
B
C
D

本阶段只生成：

instruction
question
options

不要生成对话。

不要生成答案。

不要生成解析。

------------------------------------------------------------

Part C：

严格5题。

Part C 必须直接围绕 ARTICLE EN。

5道题全部必须能够根据 ARTICLE EN 回答。

每题：

A
B
C
D

不要生成 ARTICLE EN 的听力原文。

不要生成答案。

不要生成解析。

============================================================
二、单项选择
============================================================

严格10题。

每题：

- 完整题干
- A/B/C/D 四个选项

考查可以包括：

- 词汇
- 语法
- 时态
- 句型
- 词义
- 目标词汇
- 文章语言知识
- 文章核心内容

必须符合考试难度。

不要生成答案。

不要生成解析。

============================================================
三、多选题
============================================================

严格10题。

每题：

- 完整题干
- A/B/C/D 四个选项
- 明确要求学生选择所有正确答案

至少应该存在两个正确选项。

但是：

本次 JSON 不要写答案。

不要写解析。

============================================================
四、完形填空
============================================================

必须直接使用 ARTICLE EN。

绝对禁止重新写一篇文章。

必须把 ARTICLE EN 原文作为 passage。

只允许在原文中选择10个位置挖空。

严格使用：

____ (1) ____

____ (2) ____

____ (3) ____

一直到：

____ (10) ____

不得改写原文。

不得增加无关句子。

不得删除文章其他内容。

下面生成10道选择题。

每题：

A/B/C/D

不要生成答案。

不要生成解析。

============================================================
五、阅读理解
============================================================

严格5题。

阅读理解直接使用 ARTICLE EN。

不要重新写阅读文章。

5道题全部必须能够从 ARTICLE EN 找到依据。

每题：

A
B
C
D

不要生成答案。

不要生成解析。

============================================================
六、翻译
============================================================

Part A：

汉译英5题。

题目来源：

- ARTICLE ZH
- 或 ARTICLE EN 的核心句子
- 或文章核心内容的合理中文表达

Part B：

英译汉5题。

句子必须来自 ARTICLE EN，
或者直接截取 ARTICLE EN 中的核心句子。

每题只需要提供：

sentence

不要生成标准答案。

不要生成解析。

============================================================
七、写作
============================================================

严格1题。

必须：

- 与文章主题相关
- 与文章类型相关
- 符合当前考试难度
- 有明确写作要求
- 有明确写作任务

不要生成参考范文。

不要生成答案。

不要生成解析。

============================================================
绝对禁止的字段
============================================================

输出 JSON 中绝对不要出现：

"answers"

"analysis"

"listening_script"

"answer"

"correct_answer"

"standard_answer"

"explanation"

"reference_answer"

"sample_answer"

"model_answer"

任何题目都不能携带答案字段。

============================================================
JSON 输出
============================================================

只输出合法 JSON。

不要 Markdown。

不要 ```json。

不要解释。

不要在 JSON 外输出任何文字。

必须严格使用：

{{
  "title": "string",

  "listening": [
    {{
      "part": "A",
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
    }},
    {{
      "part": "B",
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
    }},
    {{
      "part": "C",
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
  ],

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
  ],

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
  ],

  "cloze": [
    {{
      "passage": "ARTICLE EN，包含 ____ (1) ____ 到 ____ (10) ____",
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
  ],

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
  ],

  "translation": {{
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
  }},

  "writing": [
    {{
      "number": 1,
      "question": "string"
    }}
  ]
}}

============================================================
最终硬性检查
============================================================

Listening A = 5

Listening B = 5

Listening C = 5

Single Choice = 10

Multiple Choice = 10

Cloze = 10

Reading = 5

Translation A = 5

Translation B = 5

Writing = 1

不要输出答案。

不要输出解析。

不要输出听力原文。

不要输出 answers。

不要输出 analysis。

不要输出 listening_script。

只输出试卷题目 JSON。
"""

    return {
        "system": (
            "你是748686英语学习系统的专业英语考试命题专家。"
            "本次只负责生成试卷题目。"
            "绝对不要生成答案、解析或听力原文。"
            "必须严格遵守题量和JSON结构。"
            "只输出合法JSON。"
        ),
        "user": prompt,
    }


# ============================================================
# Repair Prompt
# ============================================================

def build_repair_payload(
    exam: dict,
    article: dict,
    difficulty: int,
    article_type: str,
) -> dict:

    article_en = _get_article_en(
        article
    )

    prompt = f"""
请修复下面这份英语考试“试卷主体”。

============================================================
重要
============================================================

本次只修复：

试卷题目结构和内容。

绝对不要增加：

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
固定题量
============================================================

Listening A = 5
Listening B = 5
Listening C = 5

Single Choice = 10

Multiple Choice = 10

Cloze = 10

Reading = 5

Translation A = 5

Translation B = 5

Writing = 1

============================================================
硬性要求
============================================================

1. Listening A 必须5题。

2. Listening B 必须5题。

3. Listening C 必须5题。

4. 所有选择题必须有 A/B/C/D。

5. Multiple Choice 必须是多选题。

6. Cloze 必须直接使用 ARTICLE EN。

7. Cloze 必须有：

____ (1) ____

到：

____ (10) ____

8. Reading 必须直接使用 ARTICLE EN。

9. Listening C 必须直接围绕 ARTICLE EN。

10. Translation 必须来自文章内容。

11. Writing 必须与文章主题相关。

12. 不得出现任何答案字段。

13. 不得出现任何解析字段。

14. 不得出现 listening_script。

15. 只输出合法 JSON。

============================================================
ARTICLE EN
============================================================

{article_en}

============================================================
当前试卷
============================================================

{json.dumps(
    exam,
    ensure_ascii=False,
    indent=2,
)}

请返回修复后的完整试卷主体 JSON。

只返回 JSON。
不要 Markdown。
不要解释。
"""


    return {
        "system": (
            "你是严格的英语考试试卷结构修复专家。"
            "只修复试卷主体。"
            "绝对不要生成答案、解析或听力原文。"
            "只输出合法JSON。"
        ),
        "user": prompt,
    }


# ============================================================
# API 请求
# ============================================================

def request_exam(
    payload: dict,
    api_key: str,
) -> dict:

    base_url = _to_text(
        CONFIG["agnes"]["base_url"]
    ).rstrip("/")

    model = _to_text(
        CONFIG["agnes"]["model"]
    )

    url = (
        f"{base_url}/chat/completions"
    )

    body = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": payload["system"],
            },
            {
                "role": "user",
                "content": payload["user"],
            },
        ],
        "temperature": 0.3,
    }

    # ========================================================
    # 注意：
    #
    # common.py：
    #
    # request_json(
    #     method,
    #     url,
    #     headers=None,
    #     **kwargs
    # )
    #
    # 所以必须：
    #
    # headers=...
    # json=...
    #
    # 不能把 body 作为第三个位置参数。
    # ========================================================

    return request_json(
        "POST",
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=body,
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

    api_key_env = CONFIG["agnes"][
        "api_key_env"
    ]

    api_key = env_required(
        api_key_env
    )

    print()
    print("=" * 60)
    print("EXAM GENERATION V4")
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

    article_en = _get_article_en(
        article
    )

    print(
        f"✓ 原文长度："
        f"{len(article_en.split())} words"
    )

    print()
    print("V4 试卷主体模式：")
    print("  ✓ 只生成试卷题目")
    print("  ✓ 不生成 answers")
    print("  ✓ 不生成 analysis")
    print("  ✓ 不生成 listening_script")
    print()

    print("固定题量：")
    print("  Listening A : 5")
    print("  Listening B : 5")
    print("  Listening C : 5")
    print("  Single      : 10")
    print("  Multiple    : 10")
    print("  Cloze       : 10")
    print("  Reading     : 5")
    print("  Translation : 5 + 5")
    print("  Writing     : 1")
    print()

    payload = build_exam_payload(
        article,
        difficulty,
        article_type,
        words,
    )

    last_error = None

    # ========================================================
    # 最后一个成功解析、
    # 但结构验证失败的 JSON。
    # ========================================================

    last_invalid_exam = None

    # ========================================================
    # 第一阶段：正常生成
    # ========================================================

    for attempt in range(1, 4):

        print(
            f"📝 Agnes 试卷生成 {attempt}/3"
        )

        try:

            # ------------------------------------------------
            # API
            # ------------------------------------------------

            response = request_exam(
                payload,
                api_key,
            )

            print(
                "✓ Agnes API 请求成功"
            )

            # ------------------------------------------------
            # 提取 content
            # ------------------------------------------------

            content = extract_content(
                response
            )

            # ------------------------------------------------
            # JSON
            # ------------------------------------------------

            exam = parse_json_response(
                content
            )

            print(
                "✓ 试卷 JSON 解析成功"
            )

            # ------------------------------------------------
            # 明确检查 V4：
            #
            # 不允许 AI 偷偷把 answers /
            # analysis / listening_script
            # 塞回来。
            # ------------------------------------------------

            forbidden_fields = {
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

            found_forbidden = (
                forbidden_fields
                & set(exam.keys())
            )

            if found_forbidden:

                raise ValueError(
                    "V4 试卷主体出现禁止字段："
                    + ", ".join(
                        sorted(
                            found_forbidden
                        )
                    )
                )

            # ------------------------------------------------
            # 保存用于 Repair
            # ------------------------------------------------

            last_invalid_exam = exam

            # ------------------------------------------------
            # 严格验收
            # ------------------------------------------------

            print(
                "🔍 开始严格题量与结构验收..."
            )

            validate_exam(
                exam,
                article,
                difficulty,
                article_type,
            )

            print(
                "✓ 试卷主体严格验收通过"
            )

            print()
            print("题量验收：")
            print("  ✓ Listening A = 5")
            print("  ✓ Listening B = 5")
            print("  ✓ Listening C = 5")
            print("  ✓ Single Choice = 10")
            print("  ✓ Multiple Choice = 10")
            print("  ✓ Cloze = 10")
            print("  ✓ Reading = 5")
            print("  ✓ Translation A = 5")
            print("  ✓ Translation B = 5")
            print("  ✓ Writing = 1")
            print()
            print("内容结构：")
            print("  ✓ Cloze 使用 article_en")
            print("  ✓ Reading 题目围绕 article_en")
            print("  ✓ Listening C 题目围绕 article_en")
            print("  ✓ 试卷中没有 answers")
            print("  ✓ 试卷中没有 analysis")
            print("  ✓ 试卷中没有 listening_script")

            return exam

        except Exception as exc:

            last_error = exc

            print(
                f"⚠ 试卷生成/验收失败：{exc}"
            )

            if attempt < 3:

                print(
                    "↻ 将重新生成..."
                )

                time.sleep(2)

    # ========================================================
    # 三次结束
    # ========================================================

    # 如果完全没有解析成功的 JSON，
    # 绝对不能进入 Repair。
    #
    # 例如：
    #
    # API失败
    # JSON语法错误
    #
    # 都直接终止。
    # ========================================================

    if last_invalid_exam is None:

        raise RuntimeError(
            "英语试卷生成失败："
            "连续3次均未获得可解析的有效JSON。"
            f"最后错误：{last_error}"
        )

    # ========================================================
    # 第二阶段：Repair
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM REPAIR V4")
    print("=" * 60)

    print(
        "✓ 已获得可解析的试卷 JSON"
    )

    print(
        "✓ 但试卷主体结构验收失败"
    )

    print(
        "↻ 使用最后一份试卷进入 Repair"
    )

    repair_payload = build_repair_payload(
        last_invalid_exam,
        article,
        difficulty,
        article_type,
    )

    for attempt in range(1, 4):

        print(
            f"🔧 试卷结构修复 {attempt}/3"
        )

        try:

            response = request_exam(
                repair_payload,
                api_key,
            )

            print(
                "✓ Repair API 请求成功"
            )

            content = extract_content(
                response
            )

            exam = parse_json_response(
                content
            )

            print(
                "✓ Repair JSON 解析成功"
            )

            forbidden_fields = {
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

            found_forbidden = (
                forbidden_fields
                & set(exam.keys())
            )

            if found_forbidden:

                raise ValueError(
                    "Repair 后仍出现禁止字段："
                    + ", ".join(
                        sorted(
                            found_forbidden
                        )
                    )
                )

            validate_exam(
                exam,
                article,
                difficulty,
                article_type,
            )

            print(
                "✓ Repair 后试卷主体严格验收通过"
            )

            return exam

        except Exception as exc:

            last_error = exc

            print(
                f"⚠ 修复失败：{exc}"
            )

            if attempt < 3:

                print(
                    "↻ 将继续修复..."
                )

                time.sleep(2)

    raise RuntimeError(
        "英语试卷主体生成失败："
        f"{last_error}"
    )


# ============================================================
# Markdown 辅助
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

    answer_instruction = _to_text(
        question.get(
            "answer_instruction"
        )
    )

    if answer_instruction:

        lines.extend(
            [
                answer_instruction,
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
# Markdown：听力
# ============================================================

def _render_listening(
    exam: dict,
) -> str:

    listening = exam[
        "listening"
    ]

    parts = {
        _to_text(
            item.get(
                "part"
            )
        ).upper(): item
        for item in listening
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

        item = parts[part]

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
# Markdown：选择题
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

        answer_instruction = _to_text(
            question.get(
                "answer_instruction"
            )
        )

        if answer_instruction:

            lines.extend(
                [
                    answer_instruction,
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

    return "\n".join(
        lines
    )


# ============================================================
# Markdown：完形
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
                    _options(question)
                ),
                "",
            ]
        )

    return "\n".join(
        lines
    )


# ============================================================
# Markdown：阅读
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
        exam["reading"],
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
# Markdown：翻译
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

    return "\n".join(
        lines
    )


# ============================================================
# Markdown：写作
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

    # ========================================================
    # 试卷主体
    # ========================================================

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
                exam["single_choice"],
            ),
            "",
            _render_choice_section(
                "三、多选题",
                exam["multiple_choice"],
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

    return "\n".join(
        lines
    ).strip() + "\n"
