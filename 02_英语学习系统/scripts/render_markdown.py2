#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
Markdown 渲染器 V4

======================================================================
职责
======================================================================

将 Agnes 返回的结构化英语学习文章 JSON
渲染成最终 Obsidian Markdown。

最终页面结构：

    英语短文注记 — X星难度（对应级别）1篇合集

    日期    文体    约XXX词    难度：XXX ★★★★★

    ┌──────────────────────────────┬──────────────────────┐
    │ 📖 English Article           │ 🎯 学习解析           │
    │                              │                      │
    │          英文文章标题        │ 目标词汇             │
    │      （居中、比正文大）      │ 新增词汇             │
    │                              │ 重点短语             │
    │ 英文正文                     │ 语法知识点           │
    │ 英文正文                     │ 重点句型             │
    │ 英文正文                     │ 文章结构             │
    │                              │                      │
    │          中文翻译标题        │                      │
    │      （居中、比正文大）      │                      │
    │                              │                      │
    │ 中文正文                     │                      │
    │ 中文正文                     │                      │
    └──────────────────────────────┴──────────────────────┘

======================================================================
V4 调整
======================================================================

1. 左栏始终顶部对齐。
2. 左栏正文全部左对齐。
3. 英文文章标题居中。
4. 英文文章标题比正文大。
5. 中文翻译标题居中。
6. 中文翻译标题比正文大。
7. 优先读取 Agnes 的 title_zh。
8. 如果没有 title_zh，则使用“中文翻译”作为现有兼容标题。
9. 目标词使用天蓝色文字 + 加粗。
10. 普通正文保持默认颜色。
11. 修复目标词替换过程中空格被吞掉的问题。
12. 使用独立英文单词边界，避免：
       sleep     -> sleeping
       strong    -> stronger
       exercise  -> exercises
13. 保留原始大小写。
14. HTML 特殊字符安全转义。
15. 支持 string / list / dict / 混合结构。
16. Agnes 新数据结构优先，旧数据结构自动兼容。
17. 不增加任何 AI 调用。
18. 不改变文章正文内容。
"""


import html
import re


# ======================================================================
# 目标词高亮颜色
# ======================================================================

TARGET_WORD_COLOR = "#38BDF8"


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
    从 target_vocabulary 中提取 word。

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

        if word and word.lower() not in {
            x.lower() for x in words
        }:

            words.append(word)

    # ------------------------------------------------------------------
    # 没有则使用 YML words
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

            if word and word.lower() not in {
                x.lower() for x in words
            }:

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

    目标词：

        beautiful

    输出：

        <span style="color:#38BDF8;"><strong>beautiful</strong></span>

    注意：

    1. 只改变目标词本身。
    2. 前后空格完全保留。
    3. 原始大小写完全保留。
    4. 不会把 sleep 匹配到 sleeping。
    5. 不会把 strong 匹配到 stronger。
    6. 多词目标短语也支持。
    """

    if not article_en:
        return ""

    text = str(
        article_en
    )

    valid_words = []

    seen = set()

    for word in target_words:

        word = str(
            word
        ).strip()

        if not word:
            continue

        key = word.lower()

        if key not in seen:

            valid_words.append(
                word
            )

            seen.add(key)

    if not valid_words:

        return _escape_text(
            text
        )

    # ------------------------------------------------------------------
    # 长词优先
    # ------------------------------------------------------------------

    valid_words.sort(
        key=len,
        reverse=True,
    )

    patterns = [
        re.escape(word)
        for word in valid_words
    ]

    combined = (
        r"(?<![A-Za-z])("
        + "|".join(patterns)
        + r")(?![A-Za-z])"
    )

    regex = re.compile(
        combined,
        flags=re.IGNORECASE,
    )

    parts = []

    last_end = 0

    for match in regex.finditer(text):

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

        matched_word = match.group(
            0
        )

        parts.append(
            '<span style="color:'
            + TARGET_WORD_COLOR
            + ';">'
            '<strong>'
            + _escape_text(
                matched_word
            )
            + '</strong>'
            '</span>'
        )

        last_end = match.end()

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

        beautiful — 美丽的
    """

    items = _to_items(
        vocabulary
    )

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
    新增词汇。
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
    重点短语。
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
                    + _escape_text(meaning)
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
    重点句型。
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
    文章结构。
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

    关键：
        vertical-align:top

    保证左右两栏永远从表格顶部开始。
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
# 获取中文标题
# ======================================================================

def _get_chinese_title(a):
    """
    中文翻译标题。

    优先级：

        1. title_zh
        2. chinese_title
        3. article_title_zh
        4. 中文翻译

    注意：

    当前 Agnes 如果没有中文标题字段，
    不进行任何 AI 调用。

    这样不会改变文章生成逻辑。
    """

    candidates = [
        "title_zh",
        "chinese_title",
        "article_title_zh",
    ]

    for key in candidates:

        value = _to_text(
            a.get(
                key,
                "",
            )
        )

        if value:

            return value

    return "中文翻译"


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
    # 英文文章标题
    # ==================================================================

    title = _to_text(
        a.get(
            "title",
            "",
        )
    )

    if not title:

        raise ValueError(
            "Agnes 返回的文章标题为空。"
            "文章必须由 AI 自动生成标题，"
            "不能使用固定默认标题。"
        )

    # ==================================================================
    # 中文文章标题
    # ==================================================================

    chinese_title = _get_chinese_title(
        a
    )

    # ==================================================================
    # 英文正文
    # ==================================================================

    article_en = _to_text(
        a.get(
            "article_en",
            "",
        )
    )

    if not article_en:

        raise ValueError(
            "Agnes 返回的 article_en 为空。"
        )

    # ==================================================================
    # 中文翻译
    # ==================================================================

    article_zh = _to_text(
        a.get(
            "article_zh",
            "",
        )
    )

    if not article_zh:

        raise ValueError(
            "Agnes 返回的 article_zh 为空。"
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
    # 标题
    # ==================================================================

    title_html = _escape_text(
        title
    )

    chinese_title_html = _escape_text(
        chinese_title
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
    #
    # 结构：
    #
    # 📖 English Article
    #
    #             英文标题
    #
    # 英文正文……
    #
    #             中文标题
    #
    # 中文正文……
    #
    # 注意：
    #
    # 标题居中。
    # 正文左对齐。
    # 整个左栏顶部对齐。
    # ==================================================================

    left_column = f"""
<div style="font-size:1.05em; line-height:1.75; text-align:left; vertical-align:top;">

<div style="font-size:1.15em; font-weight:700; margin-bottom:16px; text-align:left;">
📖 English Article
</div>

<div style="font-size:1.25em; font-weight:700; line-height:1.5; margin-bottom:20px; text-align:center;">
{title_html}
</div>

<div style="margin-bottom:28px; text-align:left; white-space:normal;">
{article_en_html}
</div>

<hr>

<div style="font-size:1.25em; font-weight:700; line-height:1.5; margin-top:22px; margin-bottom:18px; text-align:center;">
{chinese_title_html}
</div>

<div style="text-align:left; white-space:normal;">
{article_zh_html}
</div>

</div>
""".strip()

    # ==================================================================
    # 右栏
    # ==================================================================

    right_column = f"""
<div style="font-size:0.98em; line-height:1.65; text-align:left; vertical-align:top;">

<div style="font-size:1.15em; font-weight:700; margin-bottom:16px; text-align:left;">
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
