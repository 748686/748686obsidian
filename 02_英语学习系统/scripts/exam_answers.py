#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Exam Answers / Analysis Generator V1.0

======================================================================
职责
======================================================================

本文件只负责：

    1. 根据已经生成好的英语试卷生成答案
    2. 生成每一道题的详细解析
    3. 生成听力原文
    4. 生成总体学习分析

======================================================================
重要架构
======================================================================

试卷文件：
    exam_generate.py

负责：

    listening
    single_choice
    multiple_choice
    cloze
    reading
    translation
    writing

本文件：

    exam_answers.py

只负责：

    answers
    question_analysis
    listening_script
    general_analysis

======================================================================
绝对禁止
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

MAX_GENERATE_ATTEMPTS = 3
MAX_REPAIR_ATTEMPTS = 2

TEMPERATURE = 0.2

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
# 工具函数
# ======================================================================

def _clean_json_text(text: str) -> str:
    """
    清理 Agnes 返回的 Markdown JSON。
    """

    if not isinstance(text, str):
        raise ValueError("AI 返回内容不是字符串")

    text = text.strip()

    # 去掉 ```json ... ```
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    text = text.strip()

    # 如果前后还有杂讯，尝试截取最外层 JSON
    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        text = text[start:end + 1]

    return text.strip()


def _parse_json(text: str) -> dict:
    """
    解析 JSON。
    """

    cleaned = _clean_json_text(text)

    try:
        obj = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"AI JSON 解析失败：{e}"
        ) from e

    if not isinstance(obj, dict):
        raise ValueError("AI JSON 顶层必须是 object")

    return obj


def _api_config():
    """
    获取 Agnes API 配置。
    """

    agnes = CONFIG["agnes"]

    base_url = agnes["base_url"].rstrip("/")
    model = agnes["model"]
    api_key_env = agnes["api_key_env"]

    api_key = env_required(api_key_env)

    return base_url, model, api_key


def _extract_response_text(response: dict) -> str:
    """
    从 OpenAI-compatible API 返回中提取文本。
    """

    try:
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(
            f"无法从 Agnes API 响应中提取文本：{response}"
        ) from e


# ======================================================================
# 文章读取
# ======================================================================

def _get_article_en(article: Any) -> str:
    if isinstance(article, dict):
        value = article.get("article_en")

        if isinstance(value, str) and value.strip():
            return value.strip()

    raise ValueError("文章缺少 article_en")


def _get_article_zh(article: Any) -> str:
    if isinstance(article, dict):
        value = article.get("article_zh")

        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def _get_article_title(article: Any) -> str:
    if isinstance(article, dict):
        value = article.get("title")

        if isinstance(value, str) and value.strip():
            return value.strip()

    return "英语文章"


def _get_target_words(article: Any, words: Any) -> list:
    """
    优先使用 main.py 传入的 words。
    """

    if isinstance(words, list):
        return [
            str(x).strip()
            for x in words
            if str(x).strip()
        ]

    if isinstance(article, dict):
        value = article.get("target_vocabulary")

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
    """
    获取试卷各部分题目数量。

    不要求固定值写死在 AI 中，
    直接以实际试卷为准。
    """

    listening = exam.get("listening", [])

    if not isinstance(listening, list):
        listening = []

    single = exam.get("single_choice", [])

    if not isinstance(single, list):
        single = []

    multiple = exam.get("multiple_choice", [])

    if not isinstance(multiple, list):
        multiple = []

    cloze = exam.get("cloze", [])

    cloze_count = 0

    if isinstance(cloze, list):
        for item in cloze:
            if isinstance(item, dict):
                qs = item.get("questions", [])

                if isinstance(qs, list):
                    cloze_count += len(qs)

    reading = exam.get("reading", [])

    if not isinstance(reading, list):
        reading = []

    translation = exam.get("translation", {})

    part_a_count = 0
    part_b_count = 0

    if isinstance(translation, dict):

        part_a = translation.get("part_a", [])
        part_b = translation.get("part_b", [])

        if isinstance(part_a, list):
            part_a_count = len(part_a)

        if isinstance(part_b, list):
            part_b_count = len(part_b)

    writing = exam.get("writing", [])

    if not isinstance(writing, list):
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
# Prompt
# ======================================================================

def build_payload(
    exam: dict,
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
) -> dict:

    article_en = _get_article_en(article)
    article_zh = _get_article_zh(article)
    article_title = _get_article_title(article)

    difficulty_name = DIFFICULTY_NAMES.get(
        difficulty,
        str(difficulty),
    )

    article_type_name = ARTICLE_TYPES.get(
        article_type,
        article_type,
    )

    counts = _count_exam(exam)

    system_prompt = f"""
你是“{SYSTEM_NAME}”的英语试卷答案与解析专家。

你的任务不是生成试卷。

你收到的是一份已经确定的英语试卷。

你只能为现有试题生成：

1. 标准答案
2. 每一道题的详细解析
3. 听力原文
4. 总体学习分析

============================================================
绝对规则
============================================================

严禁修改题目。

严禁重新生成题目。

严禁增加题目。

严禁删除题目。

严禁修改题干。

严禁修改选项。

严禁重新生成阅读文章。

严禁重新生成完形文章。

试卷中的题目编号必须保持完全一致。

所有答案必须对应已经存在的题目。

============================================================
语言
============================================================

说明和解析使用中文。

听力原文使用英文。

英文答案保持英文。

============================================================
难度
============================================================

难度：
{difficulty} 星

对应：
{difficulty_name}

文章类型：
{article_type_name}

============================================================
输出要求
============================================================

只输出合法 JSON。

不要输出 Markdown。

不要输出 ```json。

不要输出任何 JSON 之外的解释文字。

============================================================
答案规则
============================================================

单选题：

answer 必须是 A/B/C/D 之一。

多选题：

answer 必须是由多个选项组成的数组，例如：

["A", "C"]

至少两个正确选项。

完形填空：

answer 必须是正确选项字母。

阅读：

answer 必须对应现有选项。

翻译：

给出标准参考译文。

写作：

给出参考范文。

============================================================
解析规则
============================================================

每一道题必须有独立解析。

解析至少说明：

1. 为什么这个答案正确
2. 为什么其他选项不正确（选择题）
3. 涉及的核心词汇 / 语法 / 阅读依据
4. 必要时指出文章中的依据

不要写空泛解析。

============================================================
听力规则
============================================================

Listening Part A：

生成与现有5道题一一对应的短听力原文。

Listening Part B：

生成与现有5道题一一对应的听力原文。

Listening Part C：

必须直接以 ARTICLE EN 为听力原文。

不得改写 ARTICLE EN。

不得增加内容。

不得删除内容。

============================================================
"""

    user_prompt = f"""
下面是已经生成好的试卷。

==============================
文章标题
==============================

{article_title}

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

{json.dumps(words, ensure_ascii=False)}

==============================
试卷
==============================

{json.dumps(exam, ensure_ascii=False, indent=2)}

==============================
试卷题目数量
==============================

{json.dumps(counts, ensure_ascii=False)}

==============================
请输出 JSON
==============================

输出结构必须严格为：

{{
  "listening_script": {{
    "part_a": [],
    "part_b": [],
    "part_c": "ARTICLE EN 原文"
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

  "question_analysis": {{
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

  "general_analysis": {{
    "summary": "",
    "grammar": [],
    "vocabulary": [],
    "reading": [],
    "listening": [],
    "translation": [],
    "writing": [],
    "study_advice": []
  }}
}}

============================================================
非常重要
============================================================

不要在 answers 中复制题目。

不要在 question_analysis 中复制完整题目。

每个答案对象只保存题号和答案。

例如：

{{
  "question": 1,
  "answer": "B"
}}

解析例如：

{{
  "question": 1,
  "answer": "B",
  "analysis": "这里考查……"
}}

翻译例如：

{{
  "question": 1,
  "answer": "参考译文……"
}}

写作例如：

{{
  "question": 1,
  "answer": "参考范文……"
}}

听力 Part A / B：

每个对象必须包含：

{{
  "question": 1,
  "script": "..."
}}

Listening Part C：

必须：

"part_c": ARTICLE EN

不能改写。
"""

    return {
        "system_prompt": system_prompt.strip(),
        "user_prompt": user_prompt.strip(),
    }


# ======================================================================
# Repair Prompt
# ======================================================================

def build_repair_payload(
    exam: dict,
    article: dict,
    difficulty: int,
    article_type: str,
    words: list,
    invalid_result: dict,
    error_message: str,
) -> dict:

    payload = build_payload(
        exam,
        article,
        difficulty,
        article_type,
        words,
    )

    repair_system = payload["system_prompt"] + """

============================================================
REPAIR MODE
============================================================

你上一次生成的答案解析 JSON 没有通过程序验收。

你现在必须修复它。

不要修改试卷。

不要修改题目。

不要增加或删除题目。

只修复答案、解析、听力原文和总体分析。

必须输出完整 JSON。

不要输出 Markdown。
"""

    repair_user = payload["user_prompt"] + f"""

============================================================
上一次错误
============================================================

{error_message}

============================================================
上一次 AI 输出
============================================================

{json.dumps(invalid_result, ensure_ascii=False, indent=2)}

请重新输出完整、合法、可验收的 JSON。
"""

    return {
        "system_prompt": repair_system,
        "user_prompt": repair_user,
    }


# ======================================================================
# API
# ======================================================================

def request_answers(payload: dict) -> dict:

    base_url, model, api_key = _api_config()

    url = f"{base_url}/chat/completions"

    body = {
        "model": model,
        "temperature": TEMPERATURE,
        "messages": [
            {
                "role": "system",
                "content": payload["system_prompt"],
            },
            {
                "role": "user",
                "content": payload["user_prompt"],
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

    text = _extract_response_text(response)

    return _parse_json(text)


# ======================================================================
# 验收工具
# ======================================================================

def _is_question_number(value: Any) -> bool:
    return isinstance(value, int) and value >= 1


def _validate_numbered_list(
    value: Any,
    expected_count: int,
    name: str,
):
    if not isinstance(value, list):
        raise ValueError(f"{name} 必须是 list")

    if len(value) != expected_count:
        raise ValueError(
            f"{name} 数量错误："
            f"期望 {expected_count}，实际 {len(value)}"
        )

    expected_numbers = list(range(1, expected_count + 1))

    actual_numbers = []

    for item in value:

        if not isinstance(item, dict):
            raise ValueError(
                f"{name} 存在非 object 项"
            )

        q = item.get("question")

        if not _is_question_number(q):
            raise ValueError(
                f"{name} 存在非法 question 编号：{q}"
            )

        actual_numbers.append(q)

    if sorted(actual_numbers) != expected_numbers:
        raise ValueError(
            f"{name} question 编号错误："
            f"{actual_numbers}"
        )


def _validate_answer_value(
    value: Any,
    name: str,
):
    if isinstance(value, str):
        if not value.strip():
            raise ValueError(
                f"{name} answer 不能为空"
            )
        return

    if isinstance(value, list):

        if len(value) < 2:
            raise ValueError(
                f"{name} 多选答案至少需要两个选项"
            )

        for item in value:

            if not isinstance(item, str):
                raise ValueError(
                    f"{name} 多选答案包含非法选项"
                )

            if item not in ("A", "B", "C", "D"):
                raise ValueError(
                    f"{name} 存在非法选项：{item}"
                )

        if len(set(value)) != len(value):
            raise ValueError(
                f"{name} 多选答案存在重复选项"
            )

        return

    raise ValueError(
        f"{name} answer 类型错误"
    )


def validate_result(
    result: dict,
    exam: dict,
    article: dict,
) -> None:

    if not isinstance(result, dict):
        raise ValueError(
            "答案解析结果必须是 object"
        )

    required_top = {
        "listening_script",
        "answers",
        "question_analysis",
        "general_analysis",
    }

    missing = required_top - set(result.keys())

    if missing:
        raise ValueError(
            f"答案解析缺少字段：{sorted(missing)}"
        )

    # --------------------------------------------------------------
    # 听力原文
    # --------------------------------------------------------------

    scripts = result["listening_script"]

    if not isinstance(scripts, dict):
        raise ValueError(
            "listening_script 必须是 object"
        )

    part_a = scripts.get("part_a")

    part_b = scripts.get("part_b")

    part_c = scripts.get("part_c")

    _validate_numbered_list(
        part_a,
        5,
        "listening_script.part_a",
    )

    _validate_numbered_list(
        part_b,
        5,
        "listening_script.part_b",
    )

    article_en = _get_article_en(article)

    if not isinstance(part_c, str):
        raise ValueError(
            "listening_script.part_c 必须是字符串"
        )

    if part_c.strip() != article_en.strip():
        raise ValueError(
            "Listening Part C 原文必须与 ARTICLE EN 完全一致"
        )

    # --------------------------------------------------------------
    # 答案
    # --------------------------------------------------------------

    answers = result["answers"]

    if not isinstance(answers, dict):
        raise ValueError(
            "answers 必须是 object"
        )

    counts = _count_exam(exam)

    answer_sections = [
        ("listening", counts["listening"]),
        ("single_choice", counts["single_choice"]),
        ("multiple_choice", counts["multiple_choice"]),
        ("cloze", counts["cloze"]),
        ("reading", counts["reading"]),
    ]

    for section, count in answer_sections:

        value = answers.get(section)

        _validate_numbered_list(
            value,
            count,
            f"answers.{section}",
        )

        for item in value:
            _validate_answer_value(
                item.get("answer"),
                f"answers.{section}[{item['question']}]",
            )

    translation = answers.get("translation")

    if not isinstance(translation, dict):
        raise ValueError(
            "answers.translation 必须是 object"
        )

    _validate_numbered_list(
        translation.get("part_a"),
        counts["translation_a"],
        "answers.translation.part_a",
    )

    _validate_numbered_list(
        translation.get("part_b"),
        counts["translation_b"],
        "answers.translation.part_b",
    )

    for item in translation["part_a"]:

        answer = item.get("answer")

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError(
                f"translation.part_a "
                f"{item['question']} 缺少参考译文"
            )

    for item in translation["part_b"]:

        answer = item.get("answer")

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError(
                f"translation.part_b "
                f"{item['question']} 缺少参考译文"
            )

    # --------------------------------------------------------------
    # Writing
    # --------------------------------------------------------------

    writing_answers = answers.get("writing")

    _validate_numbered_list(
        writing_answers,
        counts["writing"],
        "answers.writing",
    )

    for item in writing_answers:

        answer = item.get("answer")

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError(
                f"writing {item['question']} 缺少参考范文"
            )

    # --------------------------------------------------------------
    # 每道题解析
    # --------------------------------------------------------------

    analysis = result["question_analysis"]

    if not isinstance(analysis, dict):
        raise ValueError(
            "question_analysis 必须是 object"
        )

    analysis_sections = [
        ("listening", counts["listening"]),
        ("single_choice", counts["single_choice"]),
        ("multiple_choice", counts["multiple_choice"]),
        ("cloze", counts["cloze"]),
        ("reading", counts["reading"]),
    ]

    for section, count in analysis_sections:

        value = analysis.get(section)

        _validate_numbered_list(
            value,
            count,
            f"question_analysis.{section}",
        )

        for item in value:

            text = item.get("analysis")

            if not isinstance(text, str) or not text.strip():
                raise ValueError(
                    f"{section} "
                    f"{item['question']} 缺少解析"
                )

    translation_analysis = analysis.get(
        "translation"
    )

    if not isinstance(translation_analysis, dict):
        raise ValueError(
            "question_analysis.translation 必须是 object"
        )

    _validate_numbered_list(
        translation_analysis.get("part_a"),
        counts["translation_a"],
        "question_analysis.translation.part_a",
    )

    _validate_numbered_list(
        translation_analysis.get("part_b"),
        counts["translation_b"],
        "question_analysis.translation.part_b",
    )

    for section in ("part_a", "part_b"):

        for item in translation_analysis[section]:

            text = item.get("analysis")

            if not isinstance(text, str) or not text.strip():
                raise ValueError(
                    f"translation {section} "
                    f"{item['question']} 缺少解析"
                )

    writing_analysis = analysis.get("writing")

    _validate_numbered_list(
        writing_analysis,
        counts["writing"],
        "question_analysis.writing",
    )

    for item in writing_analysis:

        text = item.get("analysis")

        if not isinstance(text, str) or not text.strip():
            raise ValueError(
                f"writing {item['question']} 缺少解析"
            )

    # --------------------------------------------------------------
    # 总体分析
    # --------------------------------------------------------------

    general = result["general_analysis"]

    if not isinstance(general, dict):
        raise ValueError(
            "general_analysis 必须是 object"
        )

    if not isinstance(
        general.get("summary"),
        str,
    ) or not general["summary"].strip():

        raise ValueError(
            "general_analysis.summary 不能为空"
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

    if not isinstance(exam, dict):
        raise ValueError("exam 必须是 dict")

    if not isinstance(article, dict):
        raise ValueError("article 必须是 dict")

    # --------------------------------------------------------------
    # 第一次生成
    # --------------------------------------------------------------

    last_invalid = None
    last_error = None

    payload = build_payload(
        exam,
        article,
        difficulty,
        article_type,
        words,
    )

    for attempt in range(
        1,
        MAX_GENERATE_ATTEMPTS + 1,
    ):

        print()
        print(
            f"📝 Agnes 答案解析生成 "
            f"{attempt}/{MAX_GENERATE_ATTEMPTS}"
        )

        try:

            result = request_answers(payload)

            print("✓ Agnes API 请求成功")

            validate_result(
                result,
                exam,
                article,
            )

            print("✓ 答案解析验收通过")

            return result

        except Exception as e:

            last_error = str(e)

            print(
                f"⚠ 答案解析生成/验收失败："
                f"{last_error}"
            )

            # ------------------------------------------------------
            # API / JSON 解析失败
            # ------------------------------------------------------

            if "JSON 解析失败" in last_error:

                last_invalid = None

            else:

                try:
                    last_invalid = result
                except Exception:
                    last_invalid = None

            if attempt < MAX_GENERATE_ATTEMPTS:

                time.sleep(2)

    # ==================================================================
    # Repair
    # ==================================================================

    if last_invalid is None:

        raise RuntimeError(
            "英语试卷答案解析生成失败："
            f"连续 {MAX_GENERATE_ATTEMPTS} 次均未获得"
            "可用于 Repair 的有效 JSON。\n"
            f"最后错误：{last_error}"
        )

    print()
    print("=" * 60)
    print("进入答案解析 Repair")
    print("=" * 60)

    repair_payload = build_repair_payload(
        exam,
        article,
        difficulty,
        article_type,
        words,
        last_invalid,
        last_error or "未知错误",
    )

    repair_error = None

    for attempt in range(
        1,
        MAX_REPAIR_ATTEMPTS + 1,
    ):

        print()
        print(
            f"🔧 Agnes 答案解析 Repair "
            f"{attempt}/{MAX_REPAIR_ATTEMPTS}"
        )

        try:

            result = request_answers(
                repair_payload
            )

            print("✓ Repair API 请求成功")

            validate_result(
                result,
                exam,
                article,
            )

            print("✓ Repair 验收通过")

            return result

        except Exception as e:

            repair_error = str(e)

            print(
                f"⚠ Repair 失败："
                f"{repair_error}"
            )

            time.sleep(2)

    raise RuntimeError(
        "英语试卷答案解析 Repair 失败。\n"
        f"最后错误：{repair_error}"
    )


# ======================================================================
# Markdown 渲染
# ======================================================================

def _answer_text(answer: Any) -> str:

    if isinstance(answer, list):
        return ", ".join(answer)

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
        f"> 文章类型：{article_type_name}"
    )

    lines.append("")

    # ==================================================================
    # 一、听力原文
    # ==================================================================

    lines.append("## 一、听力原文")
    lines.append("")

    scripts = result["listening_script"]

    lines.append("### Part A")
    lines.append("")

    for item in scripts["part_a"]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['script']}"
        )

        lines.append("")

    lines.append("### Part B")
    lines.append("")

    for item in scripts["part_b"]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['script']}"
        )

        lines.append("")

    lines.append("### Part C")
    lines.append("")

    lines.append(
        scripts["part_c"]
    )

    lines.append("")

    # ==================================================================
    # 二、答案
    # ==================================================================

    lines.append("## 二、标准答案")
    lines.append("")

    answers = result["answers"]

    answer_sections = [
        ("listening", "听力"),
        ("single_choice", "单项选择"),
        ("multiple_choice", "多项选择"),
        ("cloze", "完形填空"),
        ("reading", "阅读理解"),
    ]

    for key, title in answer_sections:

        lines.append(f"### {title}")
        lines.append("")

        for item in answers[key]:

            lines.append(
                f"{item['question']}. "
                f"{_answer_text(item['answer'])}"
            )

        lines.append("")

    # ==================================================================
    # 翻译
    # ==================================================================

    translation = answers["translation"]

    lines.append("### 翻译 A：中译英")
    lines.append("")

    for item in translation["part_a"]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['answer']}"
        )

        lines.append("")

    lines.append("### 翻译 B：英译中")
    lines.append("")

    for item in translation["part_b"]:

        lines.append(
            f"**{item['question']}.** "
            f"{item['answer']}"
        )

        lines.append("")

    # ==================================================================
    # 写作
    # ==================================================================

    lines.append("### 写作参考范文")
    lines.append("")

    for item in answers["writing"]:

        lines.append(
            f"**{item['question']}.**"
        )

        lines.append("")

        lines.append(
            item["answer"]
        )

        lines.append("")

    # ==================================================================
    # 三、逐题解析
    # ==================================================================

    lines.append("## 三、逐题解析")
    lines.append("")

    analysis = result["question_analysis"]

    analysis_sections = [
        ("listening", "听力"),
        ("single_choice", "单项选择"),
        ("multiple_choice", "多项选择"),
        ("cloze", "完形填空"),
        ("reading", "阅读理解"),
    ]

    for key, title in analysis_sections:

        lines.append(f"### {title}")
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

    # ==================================================================
    # 翻译解析
    # ==================================================================

    trans_analysis = analysis["translation"]

    lines.append("### 翻译 A：中译英")
    lines.append("")

    for item in trans_analysis["part_a"]:

        lines.append(
            f"**第 {item['question']} 题**"
        )

        lines.append("")

        lines.append(
            item["analysis"]
        )

        lines.append("")

    lines.append("### 翻译 B：英译中")
    lines.append("")

    for item in trans_analysis["part_b"]:

        lines.append(
            f"**第 {item['question']} 题**"
        )

        lines.append("")

        lines.append(
            item["analysis"]
        )

        lines.append("")

    # ==================================================================
    # 写作解析
    # ==================================================================

    lines.append("### 写作")
    lines.append("")

    for item in analysis["writing"]:

        lines.append(
            f"**第 {item['question']} 题**"
        )

        lines.append("")

        lines.append(
            item["analysis"]
        )

        lines.append("")

    # ==================================================================
    # 四、总体学习分析
    # ==================================================================

    general = result["general_analysis"]

    lines.append("## 四、总体学习分析")
    lines.append("")

    lines.append("### 总结")
    lines.append("")

    lines.append(
        general["summary"]
    )

    lines.append("")

    for key, title in [
        ("grammar", "语法"),
        ("vocabulary", "词汇"),
        ("reading", "阅读"),
        ("listening", "听力"),
        ("translation", "翻译"),
        ("writing", "写作"),
        ("study_advice", "学习建议"),
    ]:

        values = general.get(key, [])

        if not isinstance(values, list):
            values = [str(values)]

        lines.append(
            f"### {title}"
        )

        lines.append("")

        for value in values:

            lines.append(
                f"- {value}"
            )

        lines.append("")

    return "\n".join(lines).strip() + "\n"


# ======================================================================
# 独立测试入口
# ======================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("748686 英语学习系统")
    print("exam_answers.py")
    print("=" * 70)
    print()
    print("本文件是答案 / 解析生成模块。")
    print()
    print("正常情况下由 main.py 调用：")
    print()
    print("generate(exam, article, difficulty, article_type, words)")
    print()
