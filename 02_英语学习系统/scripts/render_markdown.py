#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
Markdown 渲染器 V2

======================================================================
职责
======================================================================

将 Agnes 返回的结构化英语学习文章 JSON
渲染成最终 Obsidian Markdown。

最终页面结构：

    英语短文注记 — X星难度（对应级别）1篇合集
    日期    文体    约XXX词    难度：XXX ★★★★★

    ┌──────────────────────────────┬──────────────────────┐
    │ 📖 英语文章                  │ 🎯 学习解析           │
    │                              │                      │
    │ English Article              │ 目标词汇             │
    │ 英文正文                     │ 新增词汇             │
    │ 目标词蓝色高亮               │ 重点短语             │
    │                              │ 语法知识点           │
    │ 中文翻译                     │ 重点句型             │
    │                              │ 文章结构             │
    └──────────────────────────────┴──────────────────────┘

======================================================================
重要规则
======================================================================

1. 不再使用文章标题作为 Markdown 一级标题。
2. 页面第一行直接使用“英语短文注记”抬头。
3. 主体使用两列表格。
4. 英文正文中的目标词自动蓝色高亮。
5. 高亮由 Python 完成，不依赖 Agnes 输出 HTML。
6. 目标词使用单词边界匹配，避免误伤其他单词。
7. 支持 string / list / dict / 混合结构。
8. Agnes 新数据结构优先，旧数据结构自动兼容。
"""

import html
import re


# ======================================================================
# 17 星难度体系
# ======================================================================

DIFFICULTIES = {
    1: {
        "star": "一星",
        "level": "小学1-4年级",
        "label": "小学",
    },

    2: {
        "star": "二星",
        "level": "小学高年级-初一",
        "label": "小学高年级-初一",
    },

    3: {
        "star": "三星",
        "level": "初二-初四",
        "label": "初二-初四",
    },

    4: {
        "star": "四星",
        "level": "高一",
        "label": "高一",
    },

    5: {
        "star": "五星",
        "level": "高二",
        "label": "高二",
    },

    6: {
        "star": "六星",
        "level": "高三",
        "label": "高三",
    },

    7: {
        "star": "七星",
        "level": "大学",
        "label": "大学",
    },

    8: {
        "star": "八星",
        "level": "四级",
        "label": "四级",
    },

    9: {
        "star": "九星",
        "level": "六级",
        "label": "六级",
    },

    10: {
        "star": "十星",
        "level": "专四",
        "label": "专四",
    },

    11: {
        "star": "十一星",
        "level": "专六",
        "label": "专六",
    },

    12: {
        "star": "十二星",
        "level": "专八",
        "label": "专八",
    },

    13: {
        "star": "十三星",
        "level": "考研",
        "label": "考研",
    },

    14: {
        "star": "十四星",
        "level": "考博",
        "label": "考博",
    },

    15: {
        "star": "十五星",
        "level": "托福",
        "label": "托福",
    },

    16: {
        "star": "十六星",
        "level": "雅思",
        "label": "雅思",
    },

    17: {
        "star": "十七星",
        "level": "GRE",
        "label": "GRE",
    },
}


# ======================================================================
# 17 种文章类型
# ======================================================================

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


# ======================================================================
# 安全转换成文字
# ======================================================================

def _to_text(value):
    """
    将常见 JSON 数据安全转换成字符串。

    支持：
        string
        number
        bool
        dict
        list
    """

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, (int, float, bool)):
        return str(value)

    if isinstance(value, dict):

        preferred_keys = [
            "word",
            "meaning",
            "phrase",
            "name",
            "title",
            "pattern",
            "explanation",
            "example",
            "content",
            "description",
            "point",
            "text",
            "detail",
        ]

        parts = []

        used = set()

        for key in preferred_keys:

            if key not in value:
                continue

            text = _to_text(
                value[key]
            )

            if text:

                parts.append(text)
                used.add(key)

        # 如果没有识别到常见字段
        if not parts:

            for key, val in value.items():

                text = _to_text(val)

                if text:

                    parts.append(
                        f"{key}: {text}"
                    )

        return "；".join(parts)

    if isinstance(value, list):

        parts = []

        for item in value:

            text = _to_text(item)

            if text:

                parts.append(text)

        return "；".join(parts)

    return str(value)


# ======================================================================
# 转换成数组
# ======================================================================

def _to_items(value):
    """
    将任意结构统一转换成 list。
    """

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, str):

        text = value.strip()

        if not text:
            return []

        return [text]

    return [value]


# ======================================================================
# HTML 安全转义
# ======================================================================

def _escape_text(value):
    """
    HTML 表格中使用。

    保留普通文字内容，
    防止文章中的特殊字符破坏 HTML。
    """

    return html.escape(
        _to_text(value),
        quote=False,
    )


# ======================================================================
# 获取难度信息
# ======================================================================

def _get_difficulty_info(difficulty):
    """
    difficulty 可能是：

        1
        "1"
        "1星"

    统一转换成 1~17。
    """

    try:

        if isinstance(
            difficulty,
            str,
        ):

            match = re.search(
                r"\d+",
                difficulty,
            )

            if not match:

                raise ValueError

            difficulty = int(
                match.group()
            )

        else:

            difficulty = int(
                difficulty
            )

    except Exception:

        raise ValueError(
            f"无法识别难度：{difficulty}"
        )

    if difficulty not in DIFFICULTIES:

        raise ValueError(
            f"难度必须为 1~17，实际：{difficulty}"
        )

    return (
        difficulty,
        DIFFICULTIES[difficulty],
    )


# ======================================================================
# 生成星星
# ======================================================================

def _render_stars(difficulty):
    """
    总共 17 个位置。

    例如：

    1星：
    ★☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

    8星：
    ★★★★★★★★☆☆☆☆☆☆☆☆☆

    17星：
    ★★★★★★★★★★★★★★★★★
    """

    filled = "★" * difficulty
    empty = "☆" * (17 - difficulty)

    return filled + empty


# ======================================================================
# 获取文章类型名称
# ======================================================================

def _get_article_type_name(
    article_type,
):
    """
    支持：

        argumentation
        议论文
    """

    if article_type in ARTICLE_TYPES:

        return ARTICLE_TYPES[
            article_type
        ]

    if article_type in ARTICLE_TYPES.values():

        return article_type

    return str(
        article_type
    )


# ======================================================================
# 从目标词数据中提取 word
# ======================================================================

def _extract_target_words(
    vocabulary,
    fallback_words=None,
):
    """
    从：

        target_vocabulary

    中提取：

        word

    如果没有 target_vocabulary，
    则回退到 YML 传入的 words。
    """

    words = []

    # ------------------------------------------------------------------
    # 优先使用 Agnes 返回的 target_vocabulary
    # ------------------------------------------------------------------

    for item in _to_items(
        vocabulary
    ):

        if isinstance(
            item,
            dict,
        ):

            word = item.get(
                "word",
                "",
            )

        else:

            word = item

        word = _to_text(
            word
        ).strip()

        if word and word not in words:

            words.append(word)

    # ------------------------------------------------------------------
    # 没有则使用 words
    # ------------------------------------------------------------------

    if not words:

        for item in _to_items(
            fallback_words
        ):

            if isinstance(
                item,
                dict,
            ):

                word = item.get(
                    "word",
                    "",
                )

            else:

                word = item

            word = _to_text(
                word
            ).strip()

            if word and word not in words:

                words.append(word)

    return words


# ======================================================================
# 英文正文目标词高亮
# ======================================================================

def _highlight_target_words(
    article_en,
    target_words,
):
    """
    将英文正文中的目标词自动高亮。

    例如：

        beautiful

    变成：

        <span style="color:#3498db;"><strong>beautiful</strong></span>

    使用单词边界，避免：

        sleep

    错误匹配：

        sleeping

    同时保留原始大小写。
    """

    if not article_en:

        return ""

    text = str(
        article_en
    )

    valid_words = []

    for word in target_words:

        word = str(
            word
        ).strip()

        if not word:
            continue

        if word not in valid_words:

            valid_words.append(word)

    if not valid_words:

        return _escape_text(
            text
        )

    # ------------------------------------------------------------------
    # 按长度从长到短
    #
    # 防止：
    #
    # "important"
    # "more important"
    #
    # 等情况下短词先匹配。
    # ------------------------------------------------------------------

    valid_words.sort(
        key=len,
        reverse=True,
    )

    # ------------------------------------------------------------------
    # 构造正则
    # ------------------------------------------------------------------

    patterns = []

    for word in valid_words:

        patterns.append(
            re.escape(word)
        )

    combined = (
        r"(?<![A-Za-z])("
        + "|".join(patterns)
        + r")(?![A-Za-z])"
    )

    regex = re.compile(
        combined,
        flags=re.IGNORECASE,
    )

    # ------------------------------------------------------------------
    # 逐段处理
    # ------------------------------------------------------------------

    parts = []

    last_end = 0

    for match in regex.finditer(
        text
    ):

        # 普通文字
        before = text[
            last_end:
            match.start()
        ]

        if before:

            parts.append(
                _escape_text(
                    before
                )
            )

        # 目标词
        matched_word = match.group(
            0
        )

        parts.append(
            '<span style="color:#3498db;">'
            '<strong>'
            + _escape_text(
                matched_word
            )
            + "</strong></span>"
        )

        last_end = match.end()

    # ------------------------------------------------------------------
    # 最后一段
    # ------------------------------------------------------------------

    tail = text[
        last_end:
    ]

    if tail:

        parts.append(
            _escape_text(
                tail
            )
        )

    return "".join(
        parts
    )


# ======================================================================
# 渲染目标词汇
# ======================================================================

def _render_target_vocabulary(
    vocabulary,
    fallback_words=None,
):
    """
    右栏：

        目标词汇

    格式：

        <strong>beautiful</strong> — 美丽的
    """

    items = _to_items(
        vocabulary
    )

    # 如果 Agnes 没返回 target_vocabulary
    # 则用 words 构造
    if not items:

        items = _to_items(
            fallback_words
        )

    if not items:

        return "—"

    lines = []

    for item in items:

        if isinstance(
            item,
            dict,
        ):

            word = _to_text(
                item.get(
                    "word",
                    "",
                )
            )

            meaning = _to_text(
                item.get(
                    "meaning",
                    "",
                )
            )

            if word and meaning:

                lines.append(
                    "<strong>"
                    + _escape_text(word)
                    + "</strong> — "
                    + _escape_text(meaning)
                )

            elif word:

                lines.append(
                    "<strong>"
                    + _escape_text(word)
                    + "</strong>"
                )

        else:

            text = _to_text(
                item
            )

            if text:

                lines.append(
                    _escape_text(text)
                )

    if not lines:

        return "—"

    return "<br>".join(
        lines
    )


# ======================================================================
# 渲染新增词汇
# ======================================================================

def _render_added_vocabulary(
    vocabulary,
):
    """
    新增词汇：

        <strong>disagree</strong> — 不同意
    """

    items = _to_items(
        vocabulary
    )

    if not items:

        return "—"

    lines = []

    for item in items:

        if isinstance(
            item,
            dict,
        ):

            word = _to_text(
                item.get(
                    "word",
                    "",
                )
            )

            meaning = _to_text(
                item.get(
                    "meaning",
                    "",
                )
            )

            if word and meaning:

                lines.append(
                    "<strong>"
                    + _escape_text(word)
                    + "</strong> — "
                    + _escape_text(meaning)
                )

            elif word:

                lines.append(
                    "<strong>"
                    + _escape_text(word)
                    + "</strong>"
                )

        else:

            text = _to_text(
                item
            )

            if text:

                lines.append(
                    _escape_text(text)
                )

    if not lines:

        return "—"

    return "<br>".join(
        lines
    )


# ======================================================================
# 渲染重点短语
# ======================================================================

def _render_phrases(
    phrases,
):
    """
    重点短语：

        <strong>make a big difference</strong>
        — 产生巨大不同
    """

    items = _to_items(
        phrases
    )

    if not items:

        return "—"

    lines = []

    for item in items:

        if isinstance(
            item,
            dict,
        ):

            phrase = _to_text(
                item.get(
                    "phrase",
                    "",
                )
            )

            meaning = _to_text(
                item.get(
                    "meaning",
                    "",
                )
            )

            if phrase and meaning:

                lines.append(
                    "<strong>"
                    + _escape_text(
                        phrase
                    )
                    + "</strong> — "
                    + _escape_text(
                        meaning
                    )
                )

            elif phrase:

                lines.append(
                    "<strong>"
                    + _escape_text(
                        phrase
                    )
                    + "</strong>"
                )

        else:

            text = _to_text(
                item
            )

            if text:

                lines.append(
                    _escape_text(
                        text
                    )
                )

    if not lines:

        return "—"

    return "<br>".join(
        lines
    )


# ======================================================================
# 渲染语法知识点
# ======================================================================

def _render_grammar(
    grammar,
):
    """
    语法：

        语法名称
        解释
        例句
    """

    items = _to_items(
        grammar
    )

    if not items:

        return "—"

    blocks = []

    for item in items:

        if isinstance(
            item,
            dict,
        ):

            name = _to_text(
                item.get(
                    "name",
                    ""
                )
            )

            explanation = _to_text(
                item.get(
                    "explanation",
                    ""
                )
            )

            example = _to_text(
                item.get(
                    "example",
                    ""
                )
            )

            parts = []

            if name:

                parts.append(
                    "<strong>"
                    + _escape_text(name)
                    + "</strong>"
                )

            if explanation:

                parts.append(
                    _escape_text(
                        explanation
                    )
                )

            if example:

                parts.append(
                    "<em>例："
                    + _escape_text(
                        example
                    )
                    + "</em>"
                )

            if parts:

                blocks.append(
                    "<br>".join(parts)
                )

        else:

            text = _to_text(
                item
            )

            if text:

                blocks.append(
                    _escape_text(
                        text
                    )
                )

    if not blocks:

        return "—"

    return "<br><br>".join(
        blocks
    )


# ======================================================================
# 渲染重点句型
# ======================================================================

def _render_sentence_patterns(
    patterns,
):
    """
    重点句型：

        句型
        含义
        原文例句
    """

    items = _to_items(
        patterns
    )

    if not items:

        return "—"

    blocks = []

    for item in items:

        if isinstance(
            item,
            dict,
        ):

            pattern = _to_text(
                item.get(
                    "pattern",
                    ""
                )
            )

            meaning = _to_text(
                item.get(
                    "meaning",
                    ""
                )
            )

            example = _to_text(
                item.get(
                    "example",
                    ""
                )
            )

            parts = []

            if pattern:

                parts.append(
                    "<strong>"
                    + _escape_text(
                        pattern
                    )
                    + "</strong>"
                )

            if meaning:

                parts.append(
                    _escape_text(
                        meaning
                    )
                )

            if example:

                parts.append(
                    "<em>原文："
                    + _escape_text(
                        example
                    )
                    + "</em>"
                )

            if parts:

                blocks.append(
                    "<br>".join(parts)
                )

        else:

            text = _to_text(
                item
            )

            if text:

                blocks.append(
                    _escape_text(
                        text
                    )
                )

    if not blocks:

        return "—"

    return "<br><br>".join(
        blocks
    )


# ======================================================================
# 渲染文章结构
# ======================================================================

def _render_knowledge_structure(
    structure,
):
    """
    文章结构：

        标题 — 内容
    """

    items = _to_items(
        structure
    )

    if not items:

        return "—"

    blocks = []

    for item in items:

        if isinstance(
            item,
            dict,
        ):

            title = _to_text(
                item.get(
                    "title",
                    ""
                )
            )

            content = _to_text(
                item.get(
                    "content",
                    ""
                )
            )

            if title and content:

                blocks.append(
                    "<strong>"
                    + _escape_text(title)
                    + "</strong><br>"
                    + _escape_text(content)
                )

            elif title:

                blocks.append(
                    "<strong>"
                    + _escape_text(title)
                    + "</strong>"
                )

            elif content:

                blocks.append(
                    _escape_text(
                        content
                    )
                )

        else:

            text = _to_text(
                item
            )

            if text:

                blocks.append(
                    _escape_text(
                        text
                    )
                )

    if not blocks:

        return "—"

    return "<br><br>".join(
        blocks
    )


# ======================================================================
# HTML 表格单元格
# ======================================================================

def _cell(
    content,
):
    """
    统一生成 HTML table 单元格。
    """

    return (
        '<td style="'
        'width:50%;'
        'vertical-align:top;'
        'padding:18px;'
        'border:1px solid var(--background-modifier-border);'
        '">'
        + content
        + "</td>"
    )


# ======================================================================
# 主渲染函数
# ======================================================================

def render(
    a,
    words,
    difficulty,
    article_type,
    date,
    length=None,
):
    """
    将 Agnes 文章 JSON 渲染成最终 Obsidian Markdown。

    参数：
        a              Agnes 返回的文章 JSON
        words          YML 目标词汇
        difficulty     1~17
        article_type   中文文章类型 / 英文 ID
        date           日期
        length         YML 指定文章长度
    """

    if not isinstance(
        a,
        dict,
    ):

        raise ValueError(
            "Agnes 文章数据必须是 dict。"
        )

    # ==================================================================
    # 难度
    # ==================================================================

    difficulty_number, difficulty_info = (
        _get_difficulty_info(
            difficulty
        )
    )

    star_name = difficulty_info[
        "star"
    ]

    level_name = difficulty_info[
        "level"
    ]

    difficulty_label = difficulty_info[
        "label"
    ]

    stars = _render_stars(
        difficulty_number
    )

    # ==================================================================
    # 文体
    # ==================================================================

    article_type_name = (
        _get_article_type_name(
            article_type
        )
    )

    # ==================================================================
    # 文章内容
    # ==================================================================

    title = _to_text(
        a.get(
            "title",
            "英语学习文章",
        )
    )

    article_en = _to_text(
        a.get(
            "article_en",
            "",
        )
    )

    article_zh = _to_text(
        a.get(
            "article_zh",
            "",
        )
    )

    # ==================================================================
    # 学习数据
    # ==================================================================

    target_vocabulary = a.get(
        "target_vocabulary",
        [],
    )

    added_vocabulary = a.get(
        "added_vocabulary",
        [],
    )

    phrases = a.get(
        "phrases",
        [],
    )

    grammar = a.get(
        "grammar_points",
        [],
    )

    sentence_patterns = a.get(
        "sentence_patterns",
        [],
    )

    knowledge_structure = a.get(
        "knowledge_structure",
        [],
    )

    # ==================================================================
    # 目标词
    # ==================================================================

    target_words = _extract_target_words(
        target_vocabulary,
        words,
    )

    # ==================================================================
    # 英文正文高亮
    # ==================================================================

    article_en_html = (
        _highlight_target_words(
            article_en,
            target_words,
        )
    )

    # ==================================================================
    # 中文正文
    # ==================================================================

    article_zh_html = _escape_text(
        article_zh
    )

    # ==================================================================
    # 右栏内容
    # ==================================================================

    target_vocabulary_html = (
        _render_target_vocabulary(
            target_vocabulary,
            words,
        )
    )

    added_vocabulary_html = (
        _render_added_vocabulary(
            added_vocabulary
        )
    )

    phrases_html = (
        _render_phrases(
            phrases
        )
    )

    grammar_html = (
        _render_grammar(
            grammar
        )
    )

    sentence_patterns_html = (
        _render_sentence_patterns(
            sentence_patterns
        )
    )

    knowledge_structure_html = (
        _render_knowledge_structure(
            knowledge_structure
        )
    )

    # ==================================================================
    # 文章长度
    # ==================================================================

    if length is not None:

        length_text = str(
            length
        )

    else:

        # 如果 main.py 没有传 length，
        # 尝试简单计算英文单词数量。
        length_text = str(
            len(
                re.findall(
                    r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b",
                    article_en,
                )
            )
        )

    # ==================================================================
    # 左栏
    # ==================================================================

    left_column = f"""
<div style="font-size:1.05em; line-height:1.75;">

<div style="font-size:1.15em; font-weight:700; margin-bottom:12px;">
📖 English Article
</div>

<div style="margin-bottom:24px;">
{article_en_html}
</div>

<hr>

<div style="font-size:1.15em; font-weight:700; margin-top:20px; margin-bottom:12px;">
中文翻译
</div>

<div>
{article_zh_html}
</div>

</div>
""".strip()

    # ==================================================================
    # 右栏
    # ==================================================================

    right_column = f"""
<div style="font-size:0.98em; line-height:1.65;">

<div style="font-size:1.15em; font-weight:700; margin-bottom:16px;">
🎯 学习解析
</div>

<div style="font-weight:700; margin-top:12px;">
目标词汇
</div>

<div style="margin-top:6px; margin-bottom:18px;">
{target_vocabulary_html}
</div>

<div style="font-weight:700; margin-top:12px;">
新增词汇
</div>

<div style="margin-top:6px; margin-bottom:18px;">
{added_vocabulary_html}
</div>

<div style="font-weight:700; margin-top:12px;">
重点短语
</div>

<div style="margin-top:6px; margin-bottom:18px;">
{phrases_html}
</div>

<div style="font-weight:700; margin-top:12px;">
语法知识点
</div>

<div style="margin-top:6px; margin-bottom:18px;">
{grammar_html}
</div>

<div style="font-weight:700; margin-top:12px;">
重点句型
</div>

<div style="margin-top:6px; margin-bottom:18px;">
{sentence_patterns_html}
</div>

<div style="font-weight:700; margin-top:12px;">
文章结构
</div>

<div style="margin-top:6px;">
{knowledge_structure_html}
</div>

</div>
""".strip()

    # ==================================================================
    # 两列表格
    # ==================================================================

    table = f"""
<table>
<tr>
{_cell(left_column)}
{_cell(right_column)}
</tr>
</table>
""".strip()

    # ==================================================================
    # 最终 Markdown
    # ==================================================================

    markdown = f"""---
date: {date}
difficulty: {difficulty_number}星
article_type: {article_type_name}
---

英语短文注记 — {star_name}难度（{level_name}）1篇合集

{date}    {article_type_name}    约{length_text}词    难度：{difficulty_label} {stars}

{table}
"""

    return markdown
