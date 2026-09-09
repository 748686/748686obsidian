#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
配套试卷生成器

功能：
1. 使用 Agnes 生成与文章配套的英语试卷
2. 自动清理 Markdown JSON 围栏
3. 自动提取最外层 JSON
4. JSON 解析失败自动请求 Agnes 修复
5. 最多重试 3 次
6. 校验试卷基本结构
7. 避免一次 JSON 异常直接导致整个 GitHub Action 失败
"""

import json
import sys

from common import CONFIG, env_required, request_json


JSON_RETRIES = 3


def clean_json_content(content):
    """
    清理 Agnes 返回内容，尽量提取纯 JSON。
    """

    if content is None:
        return ""

    content = str(content).strip()

    if not content:
        return ""

    # 去掉 Markdown JSON 围栏
    if content.startswith("```"):
        lines = content.splitlines()

        # 删除第一行 ```json / ```
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        # 删除最后一行 ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    # 再次处理可能存在的代码围栏
    content = content.replace("```json", "").replace("```JSON", "").replace("```", "").strip()

    # 如果前后存在解释文字，只提取最外层 JSON
    first_obj = content.find("{")
    last_obj = content.rfind("}")

    first_arr = content.find("[")
    last_arr = content.rfind("]")

    candidates = []

    if first_obj >= 0 and last_obj > first_obj:
        candidates.append(
            content[first_obj:last_obj + 1]
        )

    if first_arr >= 0 and last_arr > first_arr:
        candidates.append(
            content[first_arr:last_arr + 1]
        )

    if candidates:
        # 通常对象优先
        return candidates[0].strip()

    return content.strip()


def parse_json_response(content):
    """
    尝试将 Agnes 返回内容解析成 JSON。
    """

    cleaned = clean_json_content(content)

    if not cleaned:
        raise ValueError("Agnes 返回内容为空，无法解析 JSON")

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as first_error:

        # 再做一次更严格的最外层对象提取
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start >= 0 and end > start:
            candidate = cleaned[start:end + 1]

            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

        raise first_error


def validate_exam(exam):
    """
    验证试卷 JSON 的基本结构。

    注意：
    不把结构限制得过死，避免 Agnes 合法返回但字段略有差异时被误判。
    """

    if not isinstance(exam, dict):
        raise ValueError(
            f"试卷 JSON 顶层必须是 object，实际是 {type(exam).__name__}"
        )

    # 常见试卷字段
    possible_fields = [
        "title",
        "questions",
        "sections",
        "answer",
        "answers",
        "answer_key",
        "analysis",
    ]

    if not any(field in exam for field in possible_fields):
        raise ValueError(
            "试卷 JSON 缺少基本试卷字段，"
            f"当前字段：{list(exam.keys())}"
        )

    return True


def build_exam_payload(article, difficulty, article_type, words):
    """
    构造试卷生成请求。
    """

    article_title = article.get("title", "")
    article_en = article.get("article_en", "")
    article_zh = article.get("article_zh", "")

    return {
        "task": "根据英语学习文章生成配套试卷",

        "difficulty": f"{difficulty}星",

        "article_type": article_type,

        "target_words": words,

        "article": {
            "title": article_title,
            "article_en": article_en,
            "article_zh": article_zh,
        },

        "requirements": [
            "试卷必须严格围绕给定英语文章生成",
            "题目必须能够从文章内容中找到依据",
            "目标词汇应尽可能出现在题目或考查内容中",
            "难度必须与文章难度一致",
            "不要加入与文章无关的内容",
            "必须提供完整答案",
            "必须提供必要的解析",
            "只输出合法JSON",
            "不要输出Markdown代码围栏",
            "不要输出JSON之外的说明文字",
        ],

        "schema": {
            "title": "string",
            "questions": "array",
            "answers": "array",
            "analysis": "array"
        }
    }


def build_repair_payload(raw_content):
    """
    当 Agnes 第一次返回的 JSON 不合法时，
    请求 Agnes 只修复 JSON 语法，不改变试卷内容。
    """

    return {
        "task": "修复JSON格式",

        "instructions": [
            "下面是一份试卷生成结果",
            "它应该是JSON，但当前JSON语法不合法",
            "只修复JSON语法",
            "不要改变题目内容",
            "不要删除题目",
            "不要增加题目",
            "不要修改答案",
            "不要修改解析内容",
            "不要输出Markdown代码围栏",
            "只输出合法JSON对象"
        ],

        "broken_json": str(raw_content)
    }


def request_exam(key, url, payload):
    """
    请求 Agnes。
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


def extract_content(data):
    """
    从 Agnes Chat Completion 返回中提取 message.content。
    """

    try:
        choices = data["choices"]

        if not choices:
            raise ValueError("Agnes 返回 choices 为空")

        message = choices[0]["message"]

        content = message.get("content")

        if content is None:
            raise ValueError("Agnes 返回 message.content 不存在")

        return content

    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError(
            f"Agnes 返回结构异常：{data}"
        ) from exc


def generate(article, difficulty, article_type, words):
    """
    生成配套试卷。

    返回：
        dict
    """

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
                    "不要输出JSON之外的任何解释。"
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

    for attempt in range(1, JSON_RETRIES + 1):

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

                exam = parse_json_response(content)

                validate_exam(exam)

                print("✓ Agnes 配套试卷 JSON 解析成功")

                return exam

            except Exception as parse_error:

                print(
                    f"⚠ 配套试卷 JSON 解析失败："
                    f"{parse_error}"
                )

                # 如果还有机会，使用 Agnes 自己修复 JSON
                if attempt < JSON_RETRIES:

                    print("🔧 请求 Agnes 修复试卷 JSON...")

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
                f"⚠ 配套试卷请求失败："
                f"{request_error}"
            )

            if attempt >= JSON_RETRIES:
                break

    print("")
    print("=" * 60)
    print("❌ 配套试卷生成最终失败")
    print("=" * 60)

    if last_raw_content:
        print("Agnes 原始返回：")
        print(last_raw_content[:10000])

    print("=" * 60)

    # 这里仍然抛异常。
    # main.py 如果当前设计要求试卷必须成功，则会停止。
    # 但已经生成好的文章不会被删除。
    raise RuntimeError(
        "Agnes 配套试卷生成失败，"
        f"已尝试 {JSON_RETRIES} 次。"
    )


if __name__ == "__main__":
    print(
        "exam_generate.py 是模块文件，"
        "请通过 main.py 调用。"
    )
