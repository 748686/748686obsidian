#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
配套试卷生成器

功能：
1. 使用 Agnes 生成配套试卷
2. 自动清理 Markdown JSON 围栏
3. 自动提取 JSON
4. JSON 解析失败自动修复
5. 保留 main.py 所需要的：
       generate()
       render()
6. 尽量兼容 Agnes 返回的不同 JSON 结构
"""

import json

from common import CONFIG, env_required, request_json


JSON_RETRIES = 3


# ==========================================================
# JSON 清理
# ==========================================================

def clean_json_content(content):
    if content is None:
        return ""

    content = str(content).strip()

    if not content:
        return ""

    # 去掉 Markdown 代码围栏
    if content.startswith("```"):
        lines = content.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    content = (
        content
        .replace("```json", "")
        .replace("```JSON", "")
        .replace("```", "")
        .strip()
    )

    # 提取最外层 JSON 对象
    first_obj = content.find("{")
    last_obj = content.rfind("}")

    if first_obj >= 0 and last_obj > first_obj:
        return content[first_obj:last_obj + 1].strip()

    return content


def parse_json_response(content):
    cleaned = clean_json_content(content)

    if not cleaned:
        raise ValueError(
            "Agnes 返回内容为空，无法解析 JSON"
        )

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError as first_error:

        # 再次尝试提取最外层对象
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start >= 0 and end > start:

            candidate = cleaned[start:end + 1]

            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

        raise first_error


# ==========================================================
# Agnes 返回结构
# ==========================================================

def extract_content(data):

    try:
        choices = data["choices"]

        if not choices:
            raise ValueError(
                "Agnes 返回 choices 为空"
            )

        message = choices[0]["message"]

        content = message.get("content")

        if content is None:
            raise ValueError(
                "Agnes 返回 message.content 不存在"
            )

        return content

    except (KeyError, TypeError, IndexError) as exc:

        raise ValueError(
            f"Agnes 返回结构异常：{data}"
        ) from exc


# ==========================================================
# 试卷结构检查
# ==========================================================

def validate_exam(exam):

    if not isinstance(exam, dict):
        raise ValueError(
            "试卷 JSON 顶层必须是 object"
        )

    possible_fields = [
        "title",
        "questions",
        "sections",
        "answer",
        "answers",
        "answer_key",
        "analysis",
    ]

    if not any(
        field in exam
        for field in possible_fields
    ):
        raise ValueError(
            "试卷 JSON 缺少基本字段，"
            f"当前字段：{list(exam.keys())}"
        )

    return True


# ==========================================================
# 试卷请求内容
# ==========================================================

def build_exam_payload(
    article,
    difficulty,
    article_type,
    words
):

    return {
        "task": "根据英语学习文章生成配套试卷",

        "difficulty": f"{difficulty}星",

        "article_type": article_type,

        "target_words": words,

        "article": {
            "title": article.get(
                "title",
                ""
            ),

            "article_en": article.get(
                "article_en",
                ""
            ),

            "article_zh": article.get(
                "article_zh",
                ""
            ),
        },

        "requirements": [
            "试卷必须严格围绕给定英语文章生成",
            "题目必须能够从文章内容中找到依据",
            "目标词汇应尽可能进入考查范围",
            "难度必须与文章难度一致",
            "不要加入与文章无关的内容",
            "必须提供完整答案",
            "必须提供必要解析",
            "只输出合法JSON",
            "不要输出Markdown代码围栏",
            "不要输出JSON之外的说明文字",
        ],

        "schema": {
            "title": "string",
            "questions": "array",
            "answers": "array",
            "analysis": "array",
        },
    }


# ==========================================================
# JSON 修复
# ==========================================================

def build_repair_payload(raw_content):

    return {
        "task": "修复JSON格式",

        "instructions": [
            "下面是一份试卷生成结果",
            "当前内容应该是JSON，但JSON语法不合法",
            "只修复JSON语法",
            "不要改变题目内容",
            "不要删除题目",
            "不要增加题目",
            "不要修改答案",
            "不要修改解析",
            "不要输出Markdown代码围栏",
            "只输出合法JSON对象",
        ],

        "broken_json": str(raw_content),
    }


# ==========================================================
# Agnes 请求
# ==========================================================

def request_exam(
    key,
    url,
    payload
):

    return request_json(
        "POST",
        url,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
    )


# ==========================================================
# 主生成函数
# ==========================================================

def generate(
    article,
    difficulty,
    article_type,
    words
):

    key = env_required(
        CONFIG["agnes"]["api_key_env"]
    )

    url = (
        CONFIG["agnes"]["base_url"].rstrip("/")
        + "/chat/completions"
    )

    payload = {
        "model": CONFIG["agnes"]["model"],

        "temperature": 0.3,

        "messages": [
            {
                "role": "system",
                "content": (
                    "你是严格的英语考试试卷生成器。"
                    "只输出合法JSON。"
                    "不要输出Markdown代码围栏。"
                    "不要输出JSON之外的任何说明。"
                ),
            },

            {
                "role": "user",
                "content": json.dumps(
                    build_exam_payload(
                        article,
                        difficulty,
                        article_type,
                        words,
                    ),
                    ensure_ascii=False,
                ),
            },
        ],
    }

    last_raw_content = ""

    for attempt in range(
        1,
        JSON_RETRIES + 1
    ):

        print(
            f"📝 Agnes 配套试卷生成 / JSON解析 "
            f"{attempt}/{JSON_RETRIES}"
        )

        try:

            data = request_exam(
                key,
                url,
                payload,
            )

            content = extract_content(data)

            last_raw_content = content

            try:

                exam = parse_json_response(
                    content
                )

                validate_exam(exam)

                print(
                    "✓ Agnes 配套试卷 JSON 解析成功"
                )

                return exam

            except Exception as parse_error:

                print(
                    "⚠ 配套试卷 JSON 解析失败："
                    f"{parse_error}"
                )

                # --------------------------------------------------
                # JSON 解析失败 → Agnes 修复
                # --------------------------------------------------

                if attempt < JSON_RETRIES:

                    print(
                        "🔧 请求 Agnes 修复试卷 JSON..."
                    )

                    repair_payload = {
                        "model": CONFIG["agnes"]["model"],

                        "temperature": 0.0,

                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "你是JSON修复器。"
                                    "只输出合法JSON。"
                                    "不要Markdown。"
                                    "不要解释。"
                                ),
                            },

                            {
                                "role": "user",
                                "content": json.dumps(
                                    build_repair_payload(
                                        last_raw_content
                                    ),
                                    ensure_ascii=False,
                                ),
                            },
                        ],
                    }

                    try:

                        repair_data = request_exam(
                            key,
                            url,
                            repair_payload,
                        )

                        repair_content = extract_content(
                            repair_data
                        )

                        repaired_exam = parse_json_response(
                            repair_content
                        )

                        validate_exam(
                            repaired_exam
                        )

                        print(
                            "✓ Agnes 配套试卷 JSON 修复成功"
                        )

                        return repaired_exam

                    except Exception as repair_error:

                        print(
                            "⚠ 配套试卷 JSON 修复失败："
                            f"{repair_error}"
                        )

        except Exception as request_error:

            print(
                "⚠ 配套试卷请求失败："
                f"{request_error}"
            )

    print("")
    print("=" * 60)
    print("❌ 配套试卷生成最终失败")
    print("=" * 60)

    if last_raw_content:
        print("Agnes 原始返回：")
        print(
            str(last_raw_content)[:10000]
        )

    print("=" * 60)

    raise RuntimeError(
        "Agnes 配套试卷生成失败，"
        f"已尝试 {JSON_RETRIES} 次。"
    )


# ==========================================================
# 通用 Markdown 文本转换
# ==========================================================

def _to_text(value):

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(
        value,
        (int, float, bool)
    ):
        return str(value)

    if isinstance(value, dict):

        parts = []

        preferred_keys = [
            "question",
            "title",
            "name",
            "text",
            "content",
            "answer",
            "analysis",
            "explanation",
            "option",
            "options",
            "description",
        ]

        used = set()

        for key in preferred_keys:

            if key in value:

                text = _to_text(
                    value[key]
                )

                if text:

                    if isinstance(
                        value[key],
                        (dict, list)
                    ):
                        parts.append(text)
                    else:
                        parts.append(
                            f"{key}: {text}"
                        )

                    used.add(key)

        # 如果没有常见字段
        if not parts:

            for key, val in value.items():

                text = _to_text(val)

                if text:

                    parts.append(
                        f"{key}: {text}"
                    )

        return "；".join(parts)

    if isinstance(value, list):

        return "；".join(
            text
            for item in value
            if (
                text := _to_text(item)
            )
        )

    return str(value)


def _to_lines(value):

    if value is None:
        return []

    if isinstance(value, list):

        result = []

        for item in value:

            text = _to_text(item)

            if text:
                result.append(text)

        return result

    text = _to_text(value)

    if text:
        return [text]

    return []


# ==========================================================
# 试卷 Markdown 渲染
# ==========================================================

def render(
    e,
    title,
    difficulty,
    article_type
):

    """
    将 Agnes 返回的试卷 JSON
    转换为 Obsidian Markdown。

    这个函数必须存在，因为 main.py 使用：

        from exam_generate import generate, render
    """

    exam_title = _to_text(
        e.get(
            "title",
            f"{title} 配套试卷"
        )
    )

    questions = e.get(
        "questions",
        []
    )

    sections = e.get(
        "sections",
        []
    )

    answers = e.get(
        "answers",
        e.get(
            "answer_key",
            e.get(
                "answer",
                []
            )
        )
    )

    analysis = e.get(
        "analysis",
        []
    )

    # ------------------------------------------------------
    # 题目
    # ------------------------------------------------------

    question_lines = []

    if questions:

        for index, question in enumerate(
            questions,
            start=1
        ):

            if isinstance(
                question,
                dict
            ):

                q_text = (
                    question.get(
                        "question",
                        question.get(
                            "text",
                            question.get(
                                "content",
                                ""
                            )
                        )
                    )
                )

                q_text = _to_text(
                    q_text
                )

                if q_text:
                    question_lines.append(
                        f"### {index}. {q_text}"
                    )

                options = question.get(
                    "options",
                    []
                )

                if options:

                    option_lines = _to_lines(
                        options
                    )

                    question_lines.extend(
                        f"- {x}"
                        for x in option_lines
                    )

            else:

                q_text = _to_text(
                    question
                )

                if q_text:

                    question_lines.append(
                        f"### {index}. {q_text}"
                    )

    elif sections:

        for section in sections:

            text = _to_text(
                section
            )

            if text:
                question_lines.append(
                    text
                )

    else:

        question_lines.append(
            "—"
        )

    question_text = "\n\n".join(
        question_lines
    )


    # ------------------------------------------------------
    # 答案
    # ------------------------------------------------------

    answer_lines = _to_lines(
        answers
    )

    if answer_lines:

        answer_text = "\n".join(
            f"{i}. {text}"
            for i, text in enumerate(
                answer_lines,
                start=1
            )
        )

    else:

        answer_text = "—"


    # ------------------------------------------------------
    # 解析
    # ------------------------------------------------------

    analysis_lines = _to_lines(
        analysis
    )

    if analysis_lines:

        analysis_text = "\n".join(
            f"- {text}"
            for text in analysis_lines
        )

    else:

        analysis_text = "—"


    # ------------------------------------------------------
    # Markdown
    # ------------------------------------------------------

    return f"""---
difficulty: {difficulty}星
article_type: {article_type}
source_article: {title}
---

# {exam_title}

> 配套文章：{title}

> 难度：{difficulty}星  
> 文体：{article_type}

---

## 一、试题

{question_text}

---

## 二、参考答案

{answer_text}

---

## 三、答案解析

{analysis_text}

---

## 学习建议

完成试卷后，建议重新阅读原文，并重点检查：

- 目标词汇
- 重点短语
- 语法结构
- 文章逻辑
- 阅读理解能力

"""
    

# ==========================================================
# 直接运行保护
# ==========================================================

if __name__ == "__main__":

    print(
        "exam_generate.py 是模块文件，"
        "请通过 main.py 调用。"
    )
