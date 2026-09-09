#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
数据验证器

职责
======================================================================
1. 验证 Agnes 生成的英语文章 JSON
2. 验证文章基础字段
3. 验证结构化学习解析字段
4. 验证目标词汇
5. 验证目标词确实以原形出现在英文正文
6. 验证 YML / 输入目标词全部进入 target_vocabulary
7. 验证重点短语、语法、句型、知识结构的数据结构
8. 验证配套试卷总分
"""

import re

from common import normalize


# ======================================================================
# 基础工具
# ======================================================================

def _require_non_empty_string(value, field):
    """
    要求字段必须是非空字符串。
    """

    if not isinstance(value, str):
        raise ValueError(
            f"字段 {field} 必须是字符串，"
            f"实际类型：{type(value).__name__}"
        )

    if not value.strip():
        raise ValueError(
            f"字段 {field} 不能为空"
        )


def _require_list(value, field):
    """
    要求字段必须是数组。
    """

    if not isinstance(value, list):
        raise ValueError(
            f"字段 {field} 必须是数组，"
            f"实际类型：{type(value).__name__}"
        )


# ======================================================================
# 严格检查英文单词是否以独立单词形式出现
# ======================================================================

def _word_exists_as_original_form(article_en, word):
    """
    检查目标词是否作为独立英文单词出现在正文中。

    例如：

        sleep      → 可以匹配 sleep
        sleeping   → 不应该被 sleep 匹配
        sleeps     → 不应该被 sleep 匹配
        asleep     → 不应该被 sleep 匹配

    同时忽略大小写。
    """

    if not isinstance(article_en, str):
        return False

    if not isinstance(word, str):
        return False

    word = word.strip()

    if not word:
        return False

    pattern = (
        r"(?<![A-Za-z])"
        + re.escape(word)
        + r"(?![A-Za-z])"
    )

    return re.search(
        pattern,
        article_en,
        flags=re.IGNORECASE,
    ) is not None


# ======================================================================
# 验证目标词输入
# ======================================================================

def _validate_input_words(words):
    """
    验证 main.py / YML 传入的目标词。

    当前系统允许：

        ["beautiful", "protect"]

    或：

        [
            {"word": "beautiful", "meaning": "美丽的"},
            {"word": "protect", "meaning": "保护"}
        ]
    """

    if words is None:
        return []

    if not isinstance(words, list):
        raise ValueError(
            f"目标词列表必须是数组，"
            f"实际类型：{type(words).__name__}"
        )

    result = []

    for item in words:

        if isinstance(item, dict):

            word = str(
                item.get("word", "")
            ).strip()

        else:

            word = str(item).strip()

        if word:
            result.append(word)

    return result


# ======================================================================
# 验证目标词汇
# ======================================================================

def _validate_target_vocabulary(
    article_en,
    target_vocabulary,
    words,
):
    """
    验证：

    1. target_vocabulary 必须是数组
    2. 每个项目必须是 dict
    3. 必须有 word
    4. 必须有 meaning
    5. word 必须出现在 article_en
    6. YML 输入目标词必须全部进入 target_vocabulary
    """

    _require_list(
        target_vocabulary,
        "target_vocabulary",
    )

    vocabulary_words = []

    for index, item in enumerate(
        target_vocabulary,
        start=1,
    ):

        if not isinstance(item, dict):

            raise ValueError(
                "target_vocabulary "
                f"第 {index} 项必须是对象"
            )

        word = str(
            item.get("word", "")
        ).strip()

        meaning = str(
            item.get("meaning", "")
        ).strip()

        if not word:

            raise ValueError(
                "target_vocabulary "
                f"第 {index} 项缺少 word"
            )

        if not meaning:

            raise ValueError(
                f"目标词 {word} 缺少 meaning"
            )

        # --------------------------------------------------------------
        # 原形独立单词检查
        # --------------------------------------------------------------

        if not _word_exists_as_original_form(
            article_en,
            word,
        ):

            raise ValueError(
                "目标词未在英文正文中以原形出现："
                + word
            )

        vocabulary_words.append(
            word.lower()
        )

    # ==================================================================
    # 检查 YML 输入目标词
    # ==================================================================

    input_words = _validate_input_words(words)

    missing = []

    for word in input_words:

        if word.lower() not in vocabulary_words:

            missing.append(word)

    if missing:

        raise ValueError(
            "YML目标词未全部进入 target_vocabulary："
            + ", ".join(missing)
        )


# ======================================================================
# 验证新增词汇
# ======================================================================

def _validate_added_vocabulary(value):
    """
    added_vocabulary:

    [
        {
            "word": "...",
            "meaning": "..."
        }
    ]
    """

    _require_list(
        value,
        "added_vocabulary",
    )

    for index, item in enumerate(
        value,
        start=1,
    ):

        if not isinstance(item, dict):

            raise ValueError(
                "added_vocabulary "
                f"第 {index} 项必须是对象"
            )

        word = str(
            item.get("word", "")
        ).strip()

        meaning = str(
            item.get("meaning", "")
        ).strip()

        if not word:

            raise ValueError(
                "added_vocabulary "
                f"第 {index} 项缺少 word"
            )

        if not meaning:

            raise ValueError(
                f"新增词汇 {word} 缺少 meaning"
            )


# ======================================================================
# 验证重点短语
# ======================================================================

def _validate_phrases(
    article_en,
    value,
):
    """
    phrases:

    [
        {
            "phrase": "...",
            "meaning": "..."
        }
    ]

    同时要求 phrase 真实出现在 article_en。
    """

    _require_list(
        value,
        "phrases",
    )

    for index, item in enumerate(
        value,
        start=1,
    ):

        if not isinstance(item, dict):

            raise ValueError(
                "phrases "
                f"第 {index} 项必须是对象"
            )

        phrase = str(
            item.get("phrase", "")
        ).strip()

        meaning = str(
            item.get("meaning", "")
        ).strip()

        if not phrase:

            raise ValueError(
                "phrases "
                f"第 {index} 项缺少 phrase"
            )

        if not meaning:

            raise ValueError(
                f"重点短语 {phrase} 缺少 meaning"
            )

        # --------------------------------------------------------------
        # 短语必须真实出现在正文
        # --------------------------------------------------------------

        normalized_article = normalize(
            article_en
        )

        normalized_phrase = normalize(
            phrase
        )

        if normalized_phrase not in normalized_article:

            raise ValueError(
                f"重点短语未在英文正文中出现：{phrase}"
            )


# ======================================================================
# 验证语法知识点
# ======================================================================

def _validate_grammar_points(value):
    """
    grammar_points:

    [
        {
            "name": "...",
            "explanation": "...",
            "example": "..."
        }
    ]
    """

    _require_list(
        value,
        "grammar_points",
    )

    for index, item in enumerate(
        value,
        start=1,
    ):

        if not isinstance(item, dict):

            raise ValueError(
                "grammar_points "
                f"第 {index} 项必须是对象"
            )

        name = str(
            item.get("name", "")
        ).strip()

        explanation = str(
            item.get("explanation", "")
        ).strip()

        example = str(
            item.get("example", "")
        ).strip()

        if not name:

            raise ValueError(
                "grammar_points "
                f"第 {index} 项缺少 name"
            )

        if not explanation:

            raise ValueError(
                f"语法知识点 {name} 缺少 explanation"
            )

        if not example:

            raise ValueError(
                f"语法知识点 {name} 缺少 example"
            )


# ======================================================================
# 验证重点句型
# ======================================================================

def _validate_sentence_patterns(value):
    """
    sentence_patterns:

    [
        {
            "pattern": "...",
            "meaning": "...",
            "example": "..."
        }
    ]
    """

    _require_list(
        value,
        "sentence_patterns",
    )

    for index, item in enumerate(
        value,
        start=1,
    ):

        if not isinstance(item, dict):

            raise ValueError(
                "sentence_patterns "
                f"第 {index} 项必须是对象"
            )

        pattern = str(
            item.get("pattern", "")
        ).strip()

        meaning = str(
            item.get("meaning", "")
        ).strip()

        example = str(
            item.get("example", "")
        ).strip()

        if not pattern:

            raise ValueError(
                "sentence_patterns "
                f"第 {index} 项缺少 pattern"
            )

        if not meaning:

            raise ValueError(
                f"重点句型 {pattern} 缺少 meaning"
            )

        if not example:

            raise ValueError(
                f"重点句型 {pattern} 缺少 example"
            )


# ======================================================================
# 验证文章结构
# ======================================================================

def _validate_knowledge_structure(value):
    """
    knowledge_structure:

    [
        {
            "title": "...",
            "content": "..."
        }
    ]
    """

    _require_list(
        value,
        "knowledge_structure",
    )

    for index, item in enumerate(
        value,
        start=1,
    ):

        if not isinstance(item, dict):

            raise ValueError(
                "knowledge_structure "
                f"第 {index} 项必须是对象"
            )

        title = str(
            item.get("title", "")
        ).strip()

        content = str(
            item.get("content", "")
        ).strip()

        if not title:

            raise ValueError(
                "knowledge_structure "
                f"第 {index} 项缺少 title"
            )

        if not content:

            raise ValueError(
                f"文章结构 {title} 缺少 content"
            )


# ======================================================================
# 验证文章
# ======================================================================

def article(a, words):
    """
    验证 Agnes 生成的完整文章。

    成功：
        正常返回 None

    失败：
        raise ValueError
    """

    if not isinstance(a, dict):

        raise ValueError(
            "文章结果必须是 JSON 对象"
        )

    # ==================================================================
    # 基础字段
    # ==================================================================

    required_fields = [
        "title",
        "article_en",
        "article_zh",
        "target_vocabulary",
        "added_vocabulary",
        "phrases",
        "grammar_points",
        "sentence_patterns",
        "knowledge_structure",
    ]

    missing = [
        field
        for field in required_fields
        if field not in a
    ]

    if missing:

        raise ValueError(
            "文章缺少字段："
            + ", ".join(missing)
        )

    # ==================================================================
    # 基础字符串
    # ==================================================================

    _require_non_empty_string(
        a["title"],
        "title",
    )

    _require_non_empty_string(
        a["article_en"],
        "article_en",
    )

    _require_non_empty_string(
        a["article_zh"],
        "article_zh",
    )

    article_en = a["article_en"]

    # ==================================================================
    # 目标词汇
    # ==================================================================

    _validate_target_vocabulary(
        article_en,
        a["target_vocabulary"],
        words,
    )

    # ==================================================================
    # 新增词汇
    # ==================================================================

    _validate_added_vocabulary(
        a["added_vocabulary"]
    )

    # ==================================================================
    # 重点短语
    # ==================================================================

    _validate_phrases(
        article_en,
        a["phrases"],
    )

    # ==================================================================
    # 语法
    # ==================================================================

    _validate_grammar_points(
        a["grammar_points"]
    )

    # ==================================================================
    # 重点句型
    # ==================================================================

    _validate_sentence_patterns(
        a["sentence_patterns"]
    )

    # ==================================================================
    # 知识结构
    # ==================================================================

    _validate_knowledge_structure(
        a["knowledge_structure"]
    )

    # ==================================================================
    # 成功
    # ==================================================================

    print("✓ 文章数据验证通过")

    print(
        f"✓ 目标词汇："
        f"{len(a['target_vocabulary'])}"
    )

    print(
        f"✓ 新增词汇："
        f"{len(a['added_vocabulary'])}"
    )

    print(
        f"✓ 重点短语："
        f"{len(a['phrases'])}"
    )

    print(
        f"✓ 语法知识点："
        f"{len(a['grammar_points'])}"
    )

    print(
        f"✓ 重点句型："
        f"{len(a['sentence_patterns'])}"
    )

    print(
        f"✓ 文章结构："
        f"{len(a['knowledge_structure'])}"
    )


# ======================================================================
# 验证试卷
# ======================================================================

def exam(e):
    """
    验证配套试卷。
    """

    if not isinstance(e, dict):

        raise ValueError(
            "试卷结果必须是 JSON 对象"
        )

    if e.get("total_score") != 100:

        raise ValueError(
            "试卷总分必须为100"
        )
