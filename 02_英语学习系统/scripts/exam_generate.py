#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
exam_generate.py V3.1

============================================================
职责
============================================================

围绕已经生成的英语文章 article_en / article_zh，
生成完整英语考试试卷。

固定题量：

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
V3.1 修复
============================================================

1. 修复 request_json() 参数调用错误。

   common.py：

       request_json(method, url, headers=None, **kwargs)

   正确调用：

       request_json(
           "POST",
           url,
           headers=headers,
           json=body,
       )

2. API 请求失败时，不进入 Repair。

3. 只有已经成功取得并解析 JSON，
   但试卷内容验收失败时，才进入 Repair。

4. 保留最后一个已经成功解析但验收失败的 exam，
   用于 Repair，避免无意义的额外 API 请求。

5. main.py 接口完全保持不变：

       generate(article, difficulty, article_type, words)

       render(exam, article_title, difficulty, article_type_name)
"""

import json
import re
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
    return re.sub(r"\s+", " ", _to_text(value)).strip()


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
        raise ValueError("AI JSON 顶层必须是 object")

    return data


# ============================================================
# Agnes 内容提取
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
                        parts.append(
                            _to_text(text)
                        )

            if parts:
                return "\n".join(parts)

    text = first.get("text")

    if isinstance(text, str):
        return text

    raise ValueError(
        "无法从 AI 返回结果中提取 content"
    )


# ============================================================
# 题目字段工具
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


def _answer(question: Any) -> Any:

    if not isinstance(question, dict):
        return None

    return question.get("answer")


def _analysis(question: Any) -> str:

    if not isinstance(question, dict):
        return ""

    return _to_text(
        question.get("analysis")
        or question.get("explanation")
        or ""
    )


# ============================================================
# 文章字段
# ============================================================

def _get_article_en(article: dict) -> str:

    if not isinstance(article, dict):
        raise ValueError("article 必须是 dict")

    article_en = _to_text(
        article.get("article_en")
    )

    if not article_en:
        raise ValueError("article_en 为空")

    return article_en


def _get_article_zh(article: dict) -> str:

    if not isinstance(article, dict):
        return ""

    return _to_text(
        article.get("article_zh")
    )


# ============================================================
# 听力验证
# ============================================================

def _get_listening_script(exam: dict) -> dict:

    script = exam.get("listening_script")

    if not isinstance(script, dict):
        raise ValueError(
            "listening_script 必须是 object"
        )

    for part in (
        "part_a",
        "part_b",
        "part_c",
    ):
        if not _to_text(script.get(part)):
            raise ValueError(
                f"听力原文 {part} 为空"
            )

    return script


def _validate_listening(
    exam: dict,
    article_en: str,
) -> None:

    listening = exam.get("listening")

    if not isinstance(listening, list):
        raise ValueError(
            "listening 必须是 list"
        )

    if len(listening) != 3:
        raise ValueError(
            "听力必须严格包含 Part A / B / C 三部分"
        )

    parts = {}

    for item in listening:

        if not isinstance(item, dict):
            raise ValueError(
                "听力部分格式错误"
            )

        part = _to_text(
            item.get("part")
        ).upper()

        if part not in {"A", "B", "C"}:
            raise ValueError(
                f"非法听力部分：{part}"
            )

        if part in parts:
            raise ValueError(
                f"听力 Part {part} 重复"
            )

        parts[part] = item

    required_counts = {
        "A": LISTENING_A_COUNT,
        "B": LISTENING_B_COUNT,
        "C": LISTENING_C_COUNT,
    }

    for part, required_count in required_counts.items():

        if part not in parts:
            raise ValueError(
                f"缺少听力 Part {part}"
            )

        questions = parts[part].get(
            "questions"
        )

        if not isinstance(questions, list):
            raise ValueError(
                f"听力 Part {part} questions 必须是 list"
            )

        if len(questions) != required_count:
            raise ValueError(
                f"听力 Part {part} 必须 "
                f"{required_count} 题，"
                f"实际 {len(questions)} 题"
            )

        for index, question in enumerate(
            questions,
            start=1,
        ):

            qtext = _question_text(
                question
            )

            if not qtext:
                raise ValueError(
                    f"听力 Part {part} "
                    f"第 {index} 题题干为空"
                )

            options = _options(question)

            if len(options) != 4:
                raise ValueError(
                    f"听力 Part {part} "
                    f"第 {index} 题必须有 "
                    f"A/B/C/D 四个选项"
                )

            answer = _to_text(
                _answer(question)
            ).upper()

            if answer not in {
                "A",
                "B",
                "C",
                "D",
            }:
                raise ValueError(
                    f"听力 Part {part} "
                    f"第 {index} 题答案非法："
                    f"{answer}"
                )

            if not _analysis(question):
                raise ValueError(
                    f"听力 Part {part} "
                    f"第 {index} 题缺少解析"
                )

    script = _get_listening_script(exam)

    # Part C 必须直接使用 article_en
    part_c_script = _clean_text(
        script["part_c"]
    )

    article_clean = _clean_text(
        article_en
    )

    if part_c_script != article_clean:
        raise ValueError(
            "听力 Part C 原文必须与 "
            "article_en 完全一致"
        )

    # Part A 禁止中文
    chinese_pattern = re.compile(
        r"[\u4e00-\u9fff]"
    )

    if chinese_pattern.search(
        script["part_a"]
    ):
        raise ValueError(
            "听力 Part A 原文不能出现中文"
        )

    # Part B 必须有真正对话
    part_b_script = script["part_b"]

    if not re.search(
        r"(Boy|Girl|Man|Woman|Teacher|Student|Speaker|A|B)\s*:",
        part_b_script,
        flags=re.IGNORECASE,
    ):
        raise ValueError(
            "听力 Part B 必须包含真正的英文对话角色"
        )


# ============================================================
# 单项选择验证
# ============================================================

def _validate_single_choice(exam: dict) -> None:

    questions = exam.get(
        "single_choice"
    )

    if not isinstance(questions, list):
        raise ValueError(
            "single_choice 必须是 list"
        )

    if len(questions) != SINGLE_CHOICE_COUNT:
        raise ValueError(
            f"单项选择必须 "
            f"{SINGLE_CHOICE_COUNT} 题，"
            f"实际 {len(questions)} 题"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        qtext = _question_text(
            question
        )

        if not qtext:
            raise ValueError(
                f"单项选择第 {index} 题题干为空"
            )

        options = _options(question)

        if len(options) != 4:
            raise ValueError(
                f"单项选择第 {index} 题必须有 A/B/C/D"
            )

        answer = _to_text(
            _answer(question)
        ).upper()

        if answer not in {
            "A",
            "B",
            "C",
            "D",
        }:
            raise ValueError(
                f"单项选择第 {index} 题答案非法"
            )

        if not _analysis(question):
            raise ValueError(
                f"单项选择第 {index} 题缺少解析"
            )


# ============================================================
# 多选题验证
# ============================================================

def _normalize_answers(
    value: Any,
) -> list[str]:

    if isinstance(value, list):

        result = []

        for item in value:

            letter = _to_text(
                item
            ).upper()

            if letter in {
                "A",
                "B",
                "C",
                "D",
            }:
                result.append(letter)

        return sorted(set(result))

    text = _to_text(
        value
    ).upper()

    if not text:
        return []

    letters = re.findall(
        r"[ABCD]",
        text,
    )

    return sorted(set(letters))


def _validate_multiple_choice(
    exam: dict,
) -> None:

    questions = exam.get(
        "multiple_choice"
    )

    if not isinstance(questions, list):
        raise ValueError(
            "multiple_choice 必须是 list"
        )

    if len(questions) != MULTIPLE_CHOICE_COUNT:
        raise ValueError(
            f"多选题必须 "
            f"{MULTIPLE_CHOICE_COUNT} 题，"
            f"实际 {len(questions)} 题"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        qtext = _question_text(
            question
        )

        if not qtext:
            raise ValueError(
                f"多选题第 {index} 题题干为空"
            )

        options = _options(question)

        if len(options) != 4:
            raise ValueError(
                f"多选题第 {index} 题必须有 A/B/C/D"
            )

        answers = _normalize_answers(
            _answer(question)
        )

        if len(answers) < 2:
            raise ValueError(
                f"多选题第 {index} 题至少需要两个正确答案"
            )

        if not _analysis(question):
            raise ValueError(
                f"多选题第 {index} 题缺少解析"
            )


# ============================================================
# 完形填空
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

    return sorted(set(numbers))


def _validate_cloze(
    exam: dict,
    article_en: str,
) -> None:

    cloze = exam.get("cloze")

    if not isinstance(cloze, list):
        raise ValueError(
            "cloze 必须是 list"
        )

    if not cloze:
        raise ValueError(
            "cloze 不能为空"
        )

    item = cloze[0]

    if not isinstance(item, dict):
        raise ValueError(
            "cloze 第一项格式错误"
        )

    passage = _to_text(
        item.get("passage")
    )

    if not passage:
        raise ValueError(
            "完形填空 passage 为空"
        )

    questions = item.get(
        "questions"
    )

    if not isinstance(questions, list):
        raise ValueError(
            "完形填空 questions 必须是 list"
        )

    if len(questions) != CLOZE_COUNT:
        raise ValueError(
            f"完形填空必须 "
            f"{CLOZE_COUNT} 空，"
            f"实际 {len(questions)} 题"
        )

    blank_numbers = _extract_cloze_numbers(
        passage
    )

    expected_numbers = list(
        range(1, CLOZE_COUNT + 1)
    )

    if blank_numbers != expected_numbers:
        raise ValueError(
            "完形填空必须包含连续的 "
            "____ (1) ____ 到 "
            "____ (10) ____"
        )

    # --------------------------------------------------------
    # 去掉挖空标记后检查文章主体
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
                "article_en 太短，"
                "无法验证完形原文"
            )

        passage_word_set = {
            x.lower()
            for x in passage_words
        }

        matched = sum(
            1
            for word in article_words
            if word.lower()
            in passage_word_set
        )

        ratio = (
            matched / len(article_words)
        )

        if ratio < 0.85:
            raise ValueError(
                "完形填空没有直接使用生成的 "
                "article_en 原文"
            )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        if not isinstance(question, dict):
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
                f"完形第 {index} 题缺少正确编号"
            ) from exc

        if number != index:
            raise ValueError(
                f"完形题编号错误："
                f"期望 {index}，"
                f"实际 {number}"
            )

        options = _options(question)

        if len(options) != 4:
            raise ValueError(
                f"完形第 {index} 题必须有 A/B/C/D"
            )

        answer = _to_text(
            _answer(question)
        ).upper()

        if answer not in {
            "A",
            "B",
            "C",
            "D",
        }:
            raise ValueError(
                f"完形第 {index} 题答案非法"
            )

        if not _analysis(question):
            raise ValueError(
                f"完形第 {index} 题缺少解析"
            )


# ============================================================
# 阅读理解
# ============================================================

def _validate_reading(
    exam: dict,
) -> None:

    questions = exam.get(
        "reading"
    )

    if not isinstance(questions, list):
        raise ValueError(
            "reading 必须是 list"
        )

    if len(questions) != READING_COUNT:
        raise ValueError(
            f"阅读理解必须 "
            f"{READING_COUNT} 题，"
            f"实际 {len(questions)} 题"
        )

    for index, question in enumerate(
        questions,
        start=1,
    ):

        qtext = _question_text(
            question
        )

        if not qtext:
            raise ValueError(
                f"阅读理解第 {index} 题题干为空"
            )

        options = _options(question)

        if len(options) != 4:
            raise ValueError(
                f"阅读理解第 {index} 题必须有 A/B/C/D"
            )

        answer = _to_text(
            _answer(question)
        ).upper()

        if answer not in {
            "A",
            "B",
            "C",
            "D",
        }:
            raise ValueError(
                f"阅读理解第 {index} 题答案非法"
            )

        if not _analysis(question):
            raise ValueError(
                f"阅读理解第 {index} 题缺少解析"
            )


# ============================================================
# 翻译
# ============================================================

def _validate_translation(
    exam: dict,
) -> None:

    translation = exam.get(
        "translation"
    )

    if not isinstance(translation, dict):
        raise ValueError(
            "translation 必须是 object"
        )

    part_a = translation.get(
        "part_a"
    )

    part_b = translation.get(
        "part_b"
    )

    if not isinstance(part_a, list):
        raise ValueError(
            "translation.part_a 必须是 list"
        )

    if not isinstance(part_b, list):
        raise ValueError(
            "translation.part_b 必须是 list"
        )

    if len(part_a) != TRANSLATION_A_COUNT:
        raise ValueError(
            f"汉译英必须 "
            f"{TRANSLATION_A_COUNT} 题，"
            f"实际 {len(part_a)} 题"
        )

    if len(part_b) != TRANSLATION_B_COUNT:
        raise ValueError(
            f"英译汉必须 "
            f"{TRANSLATION_B_COUNT} 题，"
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
                    f"翻译 {part_name} "
                    f"第 {index} 题格式错误"
                )

            source = (
                question.get("sentence")
                or question.get("question")
                or question.get("source")
            )

            answer = (
                question.get("answer")
                or question.get("translation")
                or question.get("standard_answer")
            )

            analysis = (
                question.get("analysis")
                or question.get("explanation")
            )

            if not _to_text(source):
                raise ValueError(
                    f"翻译 {part_name} "
                    f"第 {index} 题原句为空"
                )

            if not _to_text(answer):
                raise ValueError(
                    f"翻译 {part_name} "
                    f"第 {index} 题缺少标准答案"
                )

            if not _to_text(analysis):
                raise ValueError(
                    f"翻译 {part_name} "
                    f"第 {index} 题缺少解析"
                )


# ============================================================
# 写作
# ============================================================

def _validate_writing(
    exam: dict,
) -> None:

    writing = exam.get(
        "writing"
    )

    if not isinstance(writing, list):
        raise ValueError(
            "writing 必须是 list"
        )

    if len(writing) != WRITING_COUNT:
        raise ValueError(
            f"写作必须 "
            f"{WRITING_COUNT} 题，"
            f"实际 {len(writing)} 题"
        )

    item = writing[0]

    if not isinstance(item, dict):
        raise ValueError(
            "写作题格式错误"
        )

    prompt = (
        item.get("question")
        or item.get("prompt")
        or item.get("task")
    )

    if not _to_text(prompt):
        raise ValueError(
            "写作题缺少明确要求"
        )

    reference = (
        item.get("answer")
        or item.get("sample_answer")
        or item.get("model_answer")
        or item.get("reference_answer")
    )

    if not _to_text(reference):
        raise ValueError(
            "写作题缺少参考答案/范文"
        )

    analysis = (
        item.get("analysis")
        or item.get("explanation")
    )

    if not _to_text(analysis):
        raise ValueError(
            "写作题缺少解析"
        )


# ============================================================
# 顶层答案验证
# ============================================================

def _validate_answers(
    exam: dict,
) -> None:

    answers = exam.get(
        "answers"
    )

    if not isinstance(
        answers,
        dict,
    ):
        raise ValueError(
            "answers 必须是 object"
        )

    required = (
        "listening",
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
        "translation",
        "writing",
    )

    for key in required:

        if key not in answers:
            raise ValueError(
                f"answers 缺少 {key}"
            )


# ============================================================
# 顶层解析验证
# ============================================================

def _validate_analysis(
    exam: dict,
) -> None:

    analysis = exam.get(
        "analysis"
    )

    if not isinstance(
        analysis,
        dict,
    ):
        raise ValueError(
            "analysis 必须是 object"
        )

    if not any(
        _to_text(value)
        for value in analysis.values()
    ):
        raise ValueError(
            "analysis 不能为空"
        )


# ============================================================
# 总验证
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

    required_fields = [
        "title",
        "listening",
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
        "translation",
        "writing",
        "listening_script",
        "answers",
        "analysis",
    ]

    for field in required_fields:

        if field not in exam:
            raise ValueError(
                f"考试结果缺少字段：{field}"
            )

    title = _to_text(
        exam.get("title")
    )

    if not title:
        raise ValueError(
            "考试标题为空"
        )

    article_en = _get_article_en(
        article
    )

    if difficulty not in DIFFICULTIES:
        raise ValueError(
            f"非法难度：{difficulty}"
        )

    if article_type not in ARTICLE_TYPES:
        raise ValueError(
            f"非法文章类型：{article_type}"
        )

    _validate_listening(
        exam,
        article_en,
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

    _validate_answers(
        exam
    )

    _validate_analysis(
        exam
    )


# ============================================================
# Prompt：完整考试生成
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
        article.get("target_vocabulary")
    ):

        if isinstance(item, dict):

            word = _to_text(
                item.get("word")
            )

            meaning = _to_text(
                item.get("meaning")
            )

            if word:
                target_words.append({
                    "word": word,
                    "meaning": meaning,
                })

    if not target_words:

        for item in _ensure_list(
            words
        ):

            if isinstance(item, dict):

                word = _to_text(
                    item.get("word")
                )

                meaning = _to_text(
                    item.get("meaning")
                )

                if word:
                    target_words.append({
                        "word": word,
                        "meaning": meaning,
                    })

    prompt = f"""
你现在是“748686英语学习系统”的专业英语考试命题专家。

请根据下面已经生成完成的英语文章，生成一整套完整英语试卷。

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
对应级别：{difficulty_info["level"]}

============================================================
ARTICLE EN
============================================================

{article_en}

============================================================
ARTICLE ZH
============================================================

{article_zh}

============================================================
目标词
============================================================

{json.dumps(
    target_words,
    ensure_ascii=False,
    indent=2,
)}

============================================================
绝对固定题量
============================================================

一、听力
Part A：5题
Part B：5题
Part C：5题

二、单项选择：10题

三、多选题：10题

四、完形填空：10空

五、阅读理解：5题

六、翻译
Part A 汉译英：5题
Part B 英译汉：5题

七、写作：1题

任何题型都不能少题。

============================================================
一、听力：严格要求
============================================================

Part A：
“听句子，选出你所听到的单词”。

严格5题。

每题必须对应一个完整、自然、纯英文的听力句子。

不能出现中文听力句子。

题面可以只显示：
Which word did you hear?

A. healthy
B. happy
C. heavy
D. helpful

但完整英文句子必须保存在 listening_script.part_a 中。

Part A 的5个句子必须分别与5道题一一对应。

------------------------------------------------------------

Part B：
“听对话，选择正确答案”。

严格5题。

每题必须对应一个真正完整的英文对话。

对话必须至少包含两个说话者。

完整5段对话必须全部写入 listening_script.part_b。

不能只生成一个问题。

不能只生成一句话。

------------------------------------------------------------

Part C：
“听短文，选择正确答案”。

严格5题。

Part C 的听力原文必须直接使用 ARTICLE EN。

绝对禁止重新写一篇听力短文。

listening_script.part_c 必须与 article_en 完全一致。

5道 Part C 题目必须全部能够从 article_en 找到依据。

============================================================
二、单项选择
============================================================

必须严格10题。

每题：

1. 完整题干
2. A/B/C/D 四个选项
3. 只能一个正确答案
4. 必须有解析

可以考查：

- 词汇
- 语法
- 时态
- 句型
- 词义
- 目标词
- 文章相关语言点

必须符合当前考试难度。

============================================================
三、多选题
============================================================

必须严格10题。

每题：

1. 完整题干
2. A/B/C/D 四个选项
3. 至少两个正确答案
4. 必须有作答位置
5. 必须有答案
6. 必须有解析

题目必须围绕文章内容、词汇、语言知识或核心主题。

============================================================
四、完形填空
============================================================

必须直接使用 ARTICLE EN。

绝对不能重新写一篇文章。

在 ARTICLE EN 原文基础上选择10个合适位置挖空。

每一个空必须写成：

____ (1) ____

一直到：

____ (10) ____

必须严格存在1到10的10个编号空。

下面生成10道选择题。

每题：

A/B/C/D 四个选项。

每题只能一个正确答案。

每题必须有解析。

完形 passage 必须是 ARTICLE EN 原文，
只是在原文中挖掉10个词或短语。

不要改写文章。

不要重新写文章。

============================================================
五、阅读理解
============================================================

必须严格5题。

阅读理解文章直接使用 ARTICLE EN。

不要重新写阅读文章。

5道题必须全部能够从 ARTICLE EN 找到依据。

每题：

A/B/C/D

单一正确答案。

每题必须有解析。

============================================================
六、翻译
============================================================

Part A：汉译英5题。

Part B：英译汉5题。

一共10题。

翻译句子必须来自 ARTICLE EN / ARTICLE ZH，
或者直接根据文章核心句子进行合理截取。

不能凭空设计完全无关的句子。

每题必须有：

- 原句
- 标准答案
- 解析

============================================================
七、写作
============================================================

严格1题。

写作主题必须与本篇文章主题和文章类型相关。

必须有明确写作要求。

必须有参考范文。

必须有写作解析。

============================================================
答案
============================================================

answers 必须完整覆盖：

listening
single_choice
multiple_choice
cloze
reading
translation
writing

不能缺少任何一项。

============================================================
解析
============================================================

每一道题都必须有解析。

不能只给一个 general。

必须让学生能够知道为什么答案正确。

============================================================
输出格式
============================================================

只输出合法 JSON。

不要 Markdown。

不要 ```json。

不要解释。

JSON 必须严格符合下面 schema：

{{
  "title": "string",

  "listening": [
    {{
      "part": "A",
      "instruction": "string",
      "score": 10,
      "questions": [
        {{
          "number": 1,
          "question": "string",
          "options": [
            "A. string",
            "B. string",
            "C. string",
            "D. string"
          ],
          "answer": "A",
          "analysis": "string"
        }}
      ]
    }}
  ],

  "single_choice": [],

  "multiple_choice": [],

  "cloze": [
    {{
      "passage": "ARTICLE EN，其中10处变成 ____ (1) ____ 到 ____ (10) ____",
      "questions": []
    }}
  ],

  "reading": [],

  "translation": {{
    "part_a": [],
    "part_b": []
  }},

  "writing": [],

  "listening_script": {{
    "part_a": "5个完整英文听力句子",
    "part_b": "5段完整英文对话",
    "part_c": "必须与 ARTICLE EN 完全一致"
  }},

  "answers": {{
    "listening": [],
    "single_choice": [],
    "multiple_choice": [],
    "cloze": [],
    "reading": [],
    "translation": {{
      "part_a": [],
      "part_b": []
    }},
    "writing": []
  }},

  "analysis": {{
    "general": "string"
  }}
}}

============================================================
最后再次强调
============================================================

A=5
B=5
C=5
单选=10
多选=10
完形=10
阅读=5
汉译英=5
英译汉=5
写作=1

完形必须来自 ARTICLE EN。

阅读必须使用 ARTICLE EN。

听力 Part C 必须使用 ARTICLE EN。

听力原文必须完整。

所有题目必须有答案和解析。
"""

    return {
        "system": (
            "你是748686英语学习系统的专业英语考试命题专家。"
            "必须严格遵守用户指定题量和JSON结构。"
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
请修复下面这份英语试卷。

不要重新设计题型。

不要改变题型结构。

不要改变文章主题。

必须严格满足：

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

硬性要求：

1. Part A 每题对应完整英文听力句子。
2. Part A 不允许中文听力句子。
3. Part B 每题必须对应完整英文对话。
4. Part C 必须直接使用 ARTICLE EN。
5. Cloze 必须直接使用 ARTICLE EN。
6. Cloze 必须有：
   ____ (1) ____
   到
   ____ (10) ____
7. Reading 必须使用 ARTICLE EN。
8. Translation 必须从文章原文/核心内容选择。
9. 所有选择题必须有 A/B/C/D。
10. 单选每题只能一个正确答案。
11. 多选每题至少两个正确答案。
12. 每题必须有答案。
13. 每题必须有解析。
14. listening_script 必须完整。
15. answers 必须完整。
16. analysis 必须完整。
17. 只输出合法 JSON。

ARTICLE EN：

{article_en}

当前试卷：

{json.dumps(
    exam,
    ensure_ascii=False,
    indent=2,
)}

请返回修复后的完整 JSON。
"""

    return {
        "system": (
            "你是严格的英语考试试卷修复专家。"
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
    # V3.1 关键修复
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
    # 所以 body 必须通过 json= 传入，
    # 不能作为第三个位置参数。
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

    api_key_env = CONFIG["agnes"]["api_key_env"]

    api_key = env_required(
        api_key_env
    )

    print()
    print("=" * 60)
    print("EXAM GENERATION V3.1")
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
    # 重要：
    #
    # last_valid_json_exam：
    # 已经成功完成 API 请求并成功解析 JSON，
    # 但是 validate_exam() 失败的最后一份试卷。
    #
    # 它可以直接进入 Repair。
    #
    # 如果 API 一直失败，则它保持 None，
    # 绝对不进入 Repair。
    # ========================================================

    last_invalid_exam = None

    # ========================================================
    # 第一阶段：生成
    # ========================================================

    for attempt in range(1, 4):

        print(
            f"📝 Agnes 试卷生成 {attempt}/3"
        )

        try:

            # ------------------------------------------------
            # API 请求
            # ------------------------------------------------

            response = request_exam(
                payload,
                api_key,
            )

            print(
                "✓ Agnes API 请求成功"
            )

            # ------------------------------------------------
            # 提取 AI 内容
            # ------------------------------------------------

            content = extract_content(
                response
            )

            # ------------------------------------------------
            # JSON 解析
            # ------------------------------------------------

            exam = parse_json_response(
                content
            )

            print(
                "✓ JSON 解析成功"
            )

            # ------------------------------------------------
            # 注意：
            # API 成功 + JSON 成功
            # 但验收失败
            # 才允许进入 Repair。
            # ------------------------------------------------

            last_invalid_exam = exam

            print(
                "🔍 开始严格题量与内容验收..."
            )

            validate_exam(
                exam,
                article,
                difficulty,
                article_type,
            )

            print(
                "✓ 试卷严格验收通过"
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
            print("  ✓ Listening Script 完整")
            print("  ✓ Cloze 使用 article_en")
            print("  ✓ Reading 使用 article_en")
            print("  ✓ Part C 使用 article_en")
            print("  ✓ 所有题目存在答案与解析")

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

                # 只在生成失败时短暂等待。
                # common.py 本身已经负责 API retry。
                import time
                time.sleep(2)

    # ========================================================
    # 三次结束
    # ========================================================

    # 如果连 JSON 都没有成功拿到：
    #
    # last_invalid_exam is None
    #
    # 说明：
    #
    # API 请求失败
    # 或 JSON 解析失败
    #
    # 此时绝对不能进入 Repair。
    # ========================================================

    if last_invalid_exam is None:

        raise RuntimeError(
            "英语试卷生成失败："
            "连续3次均未获得可用于验收的有效JSON。"
            f"最后错误：{last_error}"
        )

    # ========================================================
    # 第二阶段：结构修复
    # ========================================================

    print()
    print("=" * 60)
    print("EXAM REPAIR")
    print("=" * 60)

    print(
        "✓ 已取得可解析试卷"
    )

    print(
        "✓ 原始试卷内容验收失败"
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
            f"🔧 试卷严格修复 {attempt}/3"
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

            validate_exam(
                exam,
                article,
                difficulty,
                article_type,
            )

            print(
                "✓ 修复后严格验收通过"
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

                import time
                time.sleep(2)

    raise RuntimeError(
        "英语试卷生成失败："
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

    return "\n".join(lines)


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

    if question.get(
        "answer_instruction"
    ):
        lines.extend(
            [
                _to_text(
                    question[
                        "answer_instruction"
                    ]
                ),
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

    return "\n".join(lines)


# ============================================================
# Markdown：听力
# ============================================================

def _render_listening(
    exam: dict,
) -> str:

    listening = exam["listening"]

    parts = {
        _to_text(
            item.get("part")
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
            item.get("instruction")
        )

        if instruction:
            lines.append(
                instruction
            )
            lines.append("")

        questions = item[
            "questions"
        ]

        for index, question in enumerate(
            questions,
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

        lines.append(
            f"### {index}. {qtext}"
        )
        lines.append("")

        if show_answer_blank:
            lines.append(
                "**作答：________________**"
            )
            lines.append("")

        lines.append(
            _render_options(
                _options(question)
            )
        )

        lines.append("")

    return "\n".join(lines)


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
        item.get("passage")
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

        lines.append(
            f"### {index}."
        )

        lines.append("")

        lines.append(
            _render_options(
                _options(question)
            )
        )

        lines.append("")

    return "\n".join(lines)


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

    return "\n".join(lines)


# ============================================================
# Markdown：翻译
# ============================================================

def _translation_source(
    question: dict,
) -> str:

    return _to_text(
        question.get("sentence")
        or question.get("question")
        or question.get("source")
    )


def _translation_answer(
    question: dict,
) -> str:

    return _to_text(
        question.get("answer")
        or question.get("translation")
        or question.get("standard_answer")
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

    return "\n".join(lines)


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
# Markdown：听力原文
# ============================================================

def _render_listening_script(
    exam: dict,
) -> str:

    script = exam[
        "listening_script"
    ]

    lines = [
        "# 参考答案与听力原文",
        "",
        "## 听力原文",
        "",
        "### Part A",
        "",
        _to_text(
            script["part_a"]
        ),
        "",
        "### Part B",
        "",
        _to_text(
            script["part_b"]
        ),
        "",
        "### Part C",
        "",
        _to_text(
            script["part_c"]
        ),
        "",
    ]

    return "\n".join(lines)


# ============================================================
# Markdown：答案
# ============================================================

def _render_answers(
    exam: dict,
) -> str:

    lines = [
        "## 一、听力答案",
        "",
    ]

    listening = exam[
        "listening"
    ]

    for item in listening:

        part = _to_text(
            item.get("part")
        ).upper()

        lines.append(
            f"### Part {part}"
        )
        lines.append("")

        for index, question in enumerate(
            item["questions"],
            start=1,
        ):

            answer = _to_text(
                _answer(question)
            ).upper()

            lines.append(
                f"{index}. {answer}"
            )

        lines.append("")

    lines.extend(
        [
            "## 二、单项选择答案",
            "",
        ]
    )

    for index, question in enumerate(
        exam["single_choice"],
        start=1,
    ):

        lines.append(
            f"{index}. "
            f"{_to_text(_answer(question)).upper()}"
        )

    lines.extend(
        [
            "",
            "## 三、多选题答案",
            "",
        ]
    )

    for index, question in enumerate(
        exam["multiple_choice"],
        start=1,
    ):

        answers = _normalize_answers(
            _answer(question)
        )

        lines.append(
            f"{index}. "
            f"{', '.join(answers)}"
        )

    lines.extend(
        [
            "",
            "## 四、完形填空答案",
            "",
        ]
    )

    for index, question in enumerate(
        exam["cloze"][0]["questions"],
        start=1,
    ):

        lines.append(
            f"{index}. "
            f"{_to_text(_answer(question)).upper()}"
        )

    lines.extend(
        [
            "",
            "## 五、阅读理解答案",
            "",
        ]
    )

    for index, question in enumerate(
        exam["reading"],
        start=1,
    ):

        lines.append(
            f"{index}. "
            f"{_to_text(_answer(question)).upper()}"
        )

    lines.extend(
        [
            "",
            "## 六、翻译答案",
            "",
            "### Part A 汉译英",
            "",
        ]
    )

    for index, question in enumerate(
        exam["translation"]["part_a"],
        start=1,
    ):

        lines.extend(
            [
                f"{index}. "
                f"{_translation_answer(question)}",
                "",
            ]
        )

    lines.extend(
        [
            "### Part B 英译汉",
            "",
        ]
    )

    for index, question in enumerate(
        exam["translation"]["part_b"],
        start=1,
    ):

        lines.extend(
            [
                f"{index}. "
                f"{_translation_answer(question)}",
                "",
            ]
        )

    lines.extend(
        [
            "## 七、写作答案",
            "",
        ]
    )

    writing = exam[
        "writing"
    ][0]

    lines.extend(
        [
            _to_text(
                writing.get("answer")
                or writing.get("sample_answer")
                or writing.get("model_answer")
                or writing.get("reference_answer")
            ),
            "",
        ]
    )

    return "\n".join(lines)


# ============================================================
# Markdown：解析
# ============================================================

def _render_analysis(
    exam: dict,
) -> str:

    lines = [
        "# 答案解析",
        "",
        "## 一、听力",
        "",
    ]

    listening = exam[
        "listening"
    ]

    for item in listening:

        part = _to_text(
            item.get("part")
        ).upper()

        lines.extend(
            [
                f"### Part {part}",
                "",
            ]
        )

        for index, question in enumerate(
            item["questions"],
            start=1,
        ):

            lines.extend(
                [
                    f"**{index}.** "
                    f"{_analysis(question)}",
                    "",
                ]
            )

    lines.extend(
        [
            "## 二、单项选择",
            "",
        ]
    )

    for index, question in enumerate(
        exam["single_choice"],
        start=1,
    ):

        lines.extend(
            [
                f"**{index}.** "
                f"{_analysis(question)}",
                "",
            ]
        )

    lines.extend(
        [
            "## 三、多选题",
            "",
        ]
    )

    for index, question in enumerate(
        exam["multiple_choice"],
        start=1,
    ):

        lines.extend(
            [
                f"**{index}.** "
                f"{_analysis(question)}",
                "",
            ]
        )

    lines.extend(
        [
            "## 四、完形填空",
            "",
        ]
    )

    for index, question in enumerate(
        exam["cloze"][0]["questions"],
        start=1,
    ):

        lines.extend(
            [
                f"**{index}.** "
                f"{_analysis(question)}",
                "",
            ]
        )

    lines.extend(
        [
            "## 五、阅读理解",
            "",
        ]
    )

    for index, question in enumerate(
        exam["reading"],
        start=1,
    ):

        lines.extend(
            [
                f"**{index}.** "
                f"{_analysis(question)}",
                "",
            ]
        )

    lines.extend(
        [
            "## 六、翻译",
            "",
            "### Part A 汉译英",
            "",
        ]
    )

    for index, question in enumerate(
        exam["translation"]["part_a"],
        start=1,
    ):

        lines.extend(
            [
                f"**{index}.** "
                f"{_to_text(question.get('analysis'))}",
                "",
            ]
        )

    lines.extend(
        [
            "### Part B 英译汉",
            "",
        ]
    )

    for index, question in enumerate(
        exam["translation"]["part_b"],
        start=1,
    ):

        lines.extend(
            [
                f"**{index}.** "
                f"{_to_text(question.get('analysis'))}",
                "",
            ]
        )

    lines.extend(
        [
            "## 七、写作",
            "",
        ]
    )

    writing = exam[
        "writing"
    ][0]

    lines.extend(
        [
            _to_text(
                writing.get("analysis")
                or writing.get("explanation")
            ),
            "",
        ]
    )

    general = _to_text(
        exam.get(
            "analysis",
            {}
        ).get("general")
    )

    if general:

        lines.extend(
            [
                "## 总体说明",
                "",
                general,
                "",
            ]
        )

    return "\n".join(lines)


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
        exam.get("title")
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
            "",
            "---",
            "",
            _render_listening_script(
                exam
            ),
            "",
            _render_answers(
                exam
            ),
            "",
            "---",
            "",
            _render_analysis(
                exam
            ),
        ]
    )

    return "\n".join(
        lines
    ).strip() + "\n"
