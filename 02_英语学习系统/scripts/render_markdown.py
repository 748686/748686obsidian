#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
Markdown 渲染器

作用：
1. 将 Agnes 返回的文章 JSON 渲染成 Obsidian Markdown
2. 兼容：
   - string
   - list[string]
   - list[dict]
   - 混合结构
3. 不要求 Agnes 严格改变知识结构的数据格式
4. 避免 dict / list 导致 Markdown 渲染阶段崩溃
"""

import json


def _to_text(value):
    """
    将任意常见 JSON 值安全转换成 Markdown 可显示文本。
    """

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, (int, float, bool)):
        return str(value)

    if isinstance(value, dict):
        # 常见字段优先
        preferred_keys = [
            "title",
            "name",
            "point",
            "content",
            "description",
            "explanation",
            "example",
            "text",
            "detail",
        ]

        parts = []

        # 优先输出常见语义字段
        used = set()

        for key in preferred_keys:
            if key in value:
                text = _to_text(value[key])
                if text:
                    parts.append(text)
                    used.add(key)

        # 如果没有任何常见字段，则安全序列化
        if not parts:
            for key, val in value.items():
                text = _to_text(val)
                if text:
                    parts.append(f"{key}: {text}")

        return "；".join(parts)

    if isinstance(value, list):
        return "；".join(
            text
            for item in value
            if (text := _to_text(item))
        )

    return str(value)


def _to_lines(value):
    """
    将列表结构转换成 Markdown 多行文本。
    """

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


def _render_list(value, empty="—"):
    """
    将数组渲染成 Markdown 列表。
    """

    lines = _to_lines(value)

    if not lines:
        return empty

    return "\n".join(
        f"- {line}"
        for line in lines
    )


def _render_inline(value, empty="—"):
    """
    将内容渲染成单行 HTML <br> 格式。
    """

    lines = _to_lines(value)

    if not lines:
        return empty

    return "<br>".join(lines)


def render(a, words, difficulty, article_type, date):
    """
    将 Agnes 文章 JSON 渲染成 Markdown。

    参数：
        a              Agnes 返回的文章 JSON
        words          本次目标词汇
        difficulty     难度星级
        article_type   中文文章类型
        date           日期
    """

    title = _to_text(a.get("title", "英语学习文章"))

    article_en = _to_text(
        a.get("article_en", "")
    )

    article_zh = _to_text(
        a.get("article_zh", "")
    )

    vocabulary = a.get(
        "added_vocabulary",
        []
    )

    phrases = a.get(
        "phrases",
        []
    )

    grammar = a.get(
        "grammar_points",
        []
    )

    knowledge_structure = a.get(
        "knowledge_structure",
        []
    )

    target_words = _render_list(
        words,
        empty="—"
    )

    vocabulary_text = _render_inline(
        vocabulary,
        empty="—"
    )

    phrases_text = _render_inline(
        phrases,
        empty="—"
    )

    grammar_text = _render_inline(
        grammar,
        empty="—"
    )

    knowledge_text = _render_inline(
        knowledge_structure,
        empty="—"
    )

    markdown = f"""---
date: {date}
difficulty: {difficulty}星
article_type: {article_type}
---

# {title}

## English Article

{article_en}

---

## 中文翻译

{article_zh}

---

## 目标词汇

{target_words}

---

## 学习重点

**添加的词汇**  
{vocabulary_text}

**重点短语**  
{phrases_text}

**语法知识点**  
{grammar_text}

**知识结构**  
{knowledge_text}

---

## 学习信息

- 难度：{difficulty}星
- 文体：{article_type}
- 日期：{date}
"""

    return markdown
