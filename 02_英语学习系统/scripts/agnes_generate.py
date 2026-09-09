#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
Agnes 英语短文生成器 V2

职责
======================================================================
1. 根据难度生成英语学习短文
2. 根据指定文章类型生成对应文体
3. 强制目标词汇以原形出现在英文正文
4. 为每篇文章自动生成与内容匹配的英文标题
5. 生成中文翻译
6. 生成结构化学习解析
7. 为 render_markdown.py 提供稳定 JSON 数据
8. Agnes 返回 JSON 异常时自动修复 / 重试

输出数据结构
======================================================================

{
    "title": "...",
    "article_en": "...",
    "article_zh": "...",

    "target_vocabulary": [
        {
            "word": "...",
            "meaning": "..."
        }
    ],

    "added_vocabulary": [
        {
            "word": "...",
            "meaning": "..."
        }
    ],

    "phrases": [
        {
            "phrase": "...",
            "meaning": "..."
        }
    ],

    "grammar_points": [
        {
            "name": "...",
            "explanation": "...",
            "example": "..."
        }
    ],

    "sentence_patterns": [
        {
            "pattern": "...",
            "meaning": "...",
            "example": "..."
        }
    ],

    "knowledge_structure": [
        {
            "title": "...",
            "content": "..."
        }
    ]
}
"""

import json
import re
import time

from common import CONFIG, env_required, request_json


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
# 文体特点
# ======================================================================

ARTICLE_TYPE_RULES = {
    "narration": (
        "叙述事件或故事。必须具有清晰的时间、地点、人物、事件经过和结果。"
    ),

    "argumentation": (
        "表达明确观点并进行论证。需要有观点、理由、例子或解释以及结论。"
    ),

    "exposition": (
        "解释说明事物或现象，以客观说明为主，不应写成议论文。"
    ),

    "description": (
        "重点描写人物、景物、场所或事物的外貌、特征、环境和感受。"
    ),

    "letter": (
        "书信形式。需要有自然的称呼、正文、结尾和署名感。"
    ),

    "diary": (
        "日记形式。以第一人称记录当天经历、事件和感受。"
    ),

    "notice": (
        "通知形式。信息简洁明确，应包含必要的时间、地点、对象和事项。"
    ),

    "poster": (
        "海报形式。用于宣传活动或事项，语言简洁、有吸引力和号召力。"
    ),

    "speech": (
        "演讲稿形式。面向听众讲话，应有自然的开场、主体和结束语。"
    ),

    "prose": (
        "散文形式。自由表达个人感受、观察或感悟，语言自然、有一定文学性。"
    ),

    "science": (
        "科技科普形式。解释科学、自然、技术或科技产品，强调准确、清晰。"
    ),

    "news": (
        "新闻报道形式。重点交代 who、what、when、where、why，语言客观。"
    ),

    "review": (
        "评论形式。对书籍、电影、餐厅、活动等进行评价，并说明理由。"
    ),

    "story": (
        "故事形式。具有角色、情节、冲突或变化以及相对完整的结尾。"
    ),

    "comparison": (
        "对比两个事物、人物、方法或观点，清楚说明相同点和不同点。"
    ),

    "fairy_tale": (
        "童话故事形式。可以使用魔法、精灵、会说话的动物等奇幻元素，并具有寓意。"
    ),

    "interview": (
        "采访形式。使用一问一答结构，围绕人物经历、观点或事件展开。"
    ),
}


# ======================================================================
# JSON 最大重试次数
# ======================================================================

JSON_RETRIES = 3


# ======================================================================
# 标题禁止列表
#
# 这些标题属于明显的占位标题，
# 不允许 Agnes 返回。
# ======================================================================

FORBIDDEN_TITLES = {
    "article",
    "english article",
    "english learning article",
    "my article",
    "untitled",
    "a story",
    "an article",
    "the article",
    "a short article",
    "english short article",
    "英语学习文章",
    "英语短文",
    "文章",
    "标题",
}


# ======================================================================
# 目标词标准化
# ======================================================================

def normalize_target_words(words):

    result = []

    if words is None:
        return result

    # ------------------------------------------------------------------
    # 单个字符串
    # ------------------------------------------------------------------

    if isinstance(words, str):

        for item in words.split(","):

            word = item.strip()

            if word:

                result.append({
                    "word": word,
                    "meaning": "",
                })

        return result

    # ------------------------------------------------------------------
    # 列表
    # ------------------------------------------------------------------

    if not isinstance(words, (list, tuple)):

        raise ValueError(
            f"目标词汇必须是字符串或数组，"
            f"实际类型：{type(words).__name__}"
        )

    for item in words:

        # --------------------------------------------------------------
        # 标准结构
        # --------------------------------------------------------------

        if isinstance(item, dict):

            word = str(
                item.get("word", "")
            ).strip()

            meaning = str(
                item.get("meaning", "")
            ).strip()

            if word:

                result.append({
                    "word": word,
                    "meaning": meaning,
                })

            continue

        # --------------------------------------------------------------
        # 兼容纯字符串
        # --------------------------------------------------------------

        word = str(item).strip()

        if word:

            result.append({
                "word": word,
                "meaning": "",
            })

    return result


# ======================================================================
# 目标词名称列表
# ======================================================================

def target_word_names(words):

    return [
        item["word"]
        for item in normalize_target_words(words)
        if item.get("word")
    ]


# ======================================================================
# 清理模型返回内容
# ======================================================================

def clean_json_content(content: str):

    if not isinstance(content, str):

        raise ValueError(
            f"模型返回内容不是字符串：{type(content).__name__}"
        )

    text = content.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.strip()

    first_brace = text.find("{")

    if first_brace > 0:

        text = text[first_brace:]

    last_brace = text.rfind("}")

    if last_brace >= 0:

        text = text[:last_brace + 1]

    return text.strip()


# ======================================================================
# JSON 解析
# ======================================================================

def parse_json_response(content: str):

    cleaned = clean_json_content(content)

    try:

        result = json.loads(cleaned)

        if not isinstance(result, dict):

            raise ValueError(
                "模型返回的 JSON 不是对象。"
            )

        return result

    except json.JSONDecodeError as first_error:

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start >= 0 and end > start:

            candidate = cleaned[
                start:end + 1
            ]

            try:

                result = json.loads(candidate)

                if not isinstance(result, dict):

                    raise ValueError(
                        "模型返回的 JSON 不是对象。"
                    )

                return result

            except Exception:

                pass

        raise ValueError(
            "Agnes 返回内容不是合法 JSON。\n"
            f"JSON 错误：{first_error}\n"
            f"返回内容：\n{content}"
        )


# ======================================================================
# 构造 JSON 修复请求
# ======================================================================

def build_repair_payload(original_content: str):

    return {

        "model": CONFIG["agnes"]["model"],

        "temperature": 0,

        "messages": [

            {
                "role": "system",

                "content": (
                    "你是严格的JSON修复器。"
                    "只输出一个合法JSON对象。"
                    "不要Markdown。"
                    "不要```。"
                    "不要解释。"
                    "不要增加字段。"
                    "不要删除字段。"
                    "不要修改文章内容。"
                    "只修复JSON语法错误。"
                ),
            },

            {
                "role": "user",

                "content": (
                    "下面的内容本来应该是一个JSON对象，"
                    "但存在JSON语法错误。\n\n"
                    "请修复为严格合法的JSON。\n\n"
                    "原始内容：\n"
                    f"{original_content}"
                ),
            },

        ],

    }


# ======================================================================
# 请求 Agnes
# ======================================================================

def request_article(
    key,
    url,
    payload,
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


# ======================================================================
# 从 Agnes message 中提取 content
# ======================================================================

def extract_message_content(message):

    if not isinstance(message, dict):

        return ""

    content = message.get(
        "content",
        "",
    )

    # ------------------------------------------------------------------
    # 最常见情况：
    #
    # "content": "......"
    # ------------------------------------------------------------------

    if isinstance(content, str):

        return content.strip()

    # ------------------------------------------------------------------
    # 某些 API 可能返回：
    #
    # "content": [
    #     {"type": "text", "text": "..."}
    # ]
    # ------------------------------------------------------------------

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):

                text_parts.append(item)

                continue

            if not isinstance(item, dict):

                continue

            text = item.get(
                "text",
                "",
            )

            if isinstance(text, str) and text.strip():

                text_parts.append(
                    text.strip()
                )

        return "\n".join(
            text_parts
        ).strip()

    return ""


# ======================================================================
# 验证数组
# ======================================================================

def ensure_list(
    result,
    field,
):

    value = result.get(field)

    if value is None:

        raise ValueError(
            f"Agnes JSON 缺少字段：{field}"
        )

    if not isinstance(value, list):

        raise ValueError(
            f"Agnes 字段 {field} 必须是数组，"
            f"实际类型：{type(value).__name__}"
        )

    return value


# ======================================================================
# 验证文章标题
# ======================================================================

def validate_title(title):
    """
    严格验证 AI 自动生成的文章标题。

    要求：

    1. 必须是字符串。
    2. 不能为空。
    3. 不能使用明显的占位标题。
    4. 不允许把 Title: / 标题：当成标题内容。
    """

    if not isinstance(
        title,
        str,
    ):

        raise ValueError(
            "字段 title 必须是字符串。"
        )

    title = title.strip()

    if not title:

        raise ValueError(
            "字段 title 不能为空。"
        )

    # ------------------------------------------------------------------
    # 禁止 "Title: xxx"
    # ------------------------------------------------------------------

    if re.match(
        r"^(title|标题)\s*[:：]",
        title,
        flags=re.IGNORECASE,
    ):

        raise ValueError(
            f"title 不应包含 Title:/标题：前缀：{title}"
        )

    # ------------------------------------------------------------------
    # 禁止占位标题
    # ------------------------------------------------------------------

    normalized = re.sub(
        r"\s+",
        " ",
        title,
    ).strip().lower()

    if normalized in FORBIDDEN_TITLES:

        raise ValueError(
            f"title 不能使用泛化或占位标题：{title}"
        )

    return title


# ======================================================================
# 验证文章结果
# ======================================================================

def validate_result(
    result,
    words,
):

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

    # ------------------------------------------------------------------
    # 字段存在
    # ------------------------------------------------------------------

    missing = [

        field

        for field in required_fields

        if field not in result

    ]

    if missing:

        raise ValueError(
            "Agnes JSON 缺少字段："
            + ", ".join(missing)
        )

    # ------------------------------------------------------------------
    # 字符串字段
    # ------------------------------------------------------------------

    for field in [
        "title",
        "article_en",
        "article_zh",
    ]:

        if not isinstance(
            result[field],
            str,
        ):

            raise ValueError(
                f"字段 {field} 必须是字符串。"
            )

        if not result[field].strip():

            raise ValueError(
                f"字段 {field} 不能为空。"
            )

    # ------------------------------------------------------------------
    # 标题质量验证
    # ------------------------------------------------------------------

    result["title"] = validate_title(
        result["title"]
    )

    # ------------------------------------------------------------------
    # 数组字段
    # ------------------------------------------------------------------

    for field in [
        "target_vocabulary",
        "added_vocabulary",
        "phrases",
        "grammar_points",
        "sentence_patterns",
        "knowledge_structure",
    ]:

        ensure_list(
            result,
            field,
        )

    # ------------------------------------------------------------------
    # 目标词汇验证
    # ------------------------------------------------------------------

    article_en = result["article_en"]

    target_vocabulary = result[
        "target_vocabulary"
    ]

    target_vocab_words = set()

    for item in target_vocabulary:

        if not isinstance(item, dict):

            raise ValueError(
                "target_vocabulary 中的项目必须是对象。"
            )

        word = str(
            item.get("word", "")
        ).strip()

        meaning = str(
            item.get("meaning", "")
        ).strip()

        if not word:

            raise ValueError(
                "target_vocabulary 中存在空 word。"
            )

        if not meaning:

            raise ValueError(
                f"目标词 {word} 缺少 meaning。"
            )

        target_vocab_words.add(
            word.lower()
        )

        # --------------------------------------------------------------
        # 目标词必须以独立原形出现在文章中
        # --------------------------------------------------------------

        pattern = (
            r"(?<![A-Za-z])"
            + re.escape(word)
            + r"(?![A-Za-z])"
        )

        if not re.search(
            pattern,
            article_en,
            flags=re.IGNORECASE,
        ):

            raise ValueError(
                f"目标词未在英文正文中以原形出现：{word}"
            )

    # ------------------------------------------------------------------
    # YML 目标词验证
    # ------------------------------------------------------------------

    normalized_words = normalize_target_words(
        words
    )

    required_word_names = {

        item["word"].strip().lower()

        for item in normalized_words

        if item.get("word")
    }

    if not required_word_names:

        raise ValueError(
            "YML 没有提供有效目标词汇。"
        )

    missing_yml_words = [

        item["word"]

        for item in normalized_words

        if item.get("word")
        and item["word"].strip().lower()
        not in target_vocab_words
    ]

    if missing_yml_words:

        raise ValueError(
            "YML目标词未进入 target_vocabulary："
            + ", ".join(missing_yml_words)
        )

    # ------------------------------------------------------------------
    # YML目标词必须真实出现在 article_en
    # ------------------------------------------------------------------

    missing_in_article = []

    for item in normalized_words:

        word = item.get(
            "word",
            "",
        ).strip()

        if not word:

            continue

        pattern = (
            r"(?<![A-Za-z])"
            + re.escape(word)
            + r"(?![A-Za-z])"
        )

        if not re.search(
            pattern,
            article_en,
            flags=re.IGNORECASE,
        ):

            missing_in_article.append(
                word
            )

    if missing_in_article:

        raise ValueError(
            "YML目标词未以原形出现在 article_en："
            + ", ".join(missing_in_article)
        )

    # ------------------------------------------------------------------
    # 验证重点短语
    # ------------------------------------------------------------------

    for item in result["phrases"]:

        if not isinstance(item, dict):

            raise ValueError(
                "phrases 中的项目必须是对象。"
            )

        phrase = str(
            item.get("phrase", "")
        ).strip()

        meaning = str(
            item.get("meaning", "")
        ).strip()

        if not phrase:

            raise ValueError(
                "phrases 中存在空 phrase。"
            )

        if not meaning:

            raise ValueError(
                f"重点短语 {phrase} 缺少 meaning。"
            )

        if not re.search(
            re.escape(phrase),
            article_en,
            flags=re.IGNORECASE,
        ):

            raise ValueError(
                f"重点短语未出现在 article_en：{phrase}"
            )

    # ------------------------------------------------------------------
    # 验证新增词汇
    # ------------------------------------------------------------------

    for item in result["added_vocabulary"]:

        if not isinstance(item, dict):

            raise ValueError(
                "added_vocabulary 中的项目必须是对象。"
            )

        word = str(
            item.get("word", "")
        ).strip()

        meaning = str(
            item.get("meaning", "")
        ).strip()

        if not word:

            raise ValueError(
                "added_vocabulary 中存在空 word。"
            )

        if not meaning:

            raise ValueError(
                f"新增词汇 {word} 缺少 meaning。"
            )

    # ------------------------------------------------------------------
    # 验证语法知识点
    # ------------------------------------------------------------------

    for item in result["grammar_points"]:

        if not isinstance(item, dict):

            raise ValueError(
                "grammar_points 中的项目必须是对象。"
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
                "grammar_points 中存在空 name。"
            )

        if not explanation:

            raise ValueError(
                f"语法知识点 {name} 缺少 explanation。"
            )

        if not example:

            raise ValueError(
                f"语法知识点 {name} 缺少 example。"
            )

    # ------------------------------------------------------------------
    # 验证重点句型
    # ------------------------------------------------------------------

    for item in result["sentence_patterns"]:

        if not isinstance(item, dict):

            raise ValueError(
                "sentence_patterns 中的项目必须是对象。"
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
                "sentence_patterns 中存在空 pattern。"
            )

        if not meaning:

            raise ValueError(
                f"重点句型 {pattern} 缺少 meaning。"
            )

        if not example:

            raise ValueError(
                f"重点句型 {pattern} 缺少 example。"
            )

    # ------------------------------------------------------------------
    # 验证知识结构
    # ------------------------------------------------------------------

    for item in result["knowledge_structure"]:

        if not isinstance(item, dict):

            raise ValueError(
                "knowledge_structure 中的项目必须是对象。"
            )

        title = str(
            item.get("title", "")
        ).strip()

        content = str(
            item.get("content", "")
        ).strip()

        if not title:

            raise ValueError(
                "knowledge_structure 中存在空 title。"
            )

        if not content:

            raise ValueError(
                f"知识结构 {title} 缺少 content。"
            )

    return result


# ======================================================================
# 主生成函数
# ======================================================================

def generate(
    words,
    difficulty,
    article_type,
    length,
):

    # ==================================================================
    # 基础检查
    # ==================================================================

    if article_type not in ARTICLE_TYPES:

        raise ValueError(
            f"未知文章类型：{article_type}"
        )

    if difficulty not in DIFFICULTIES:

        raise ValueError(
            f"未知难度：{difficulty}"
        )

    # ==================================================================
    # 难度信息
    # ==================================================================

    difficulty_info = DIFFICULTIES[
        difficulty
    ]

    # ==================================================================
    # 文体信息
    # ==================================================================

    article_type_name = ARTICLE_TYPES[
        article_type
    ]

    article_type_rule = ARTICLE_TYPE_RULES[
        article_type
    ]

    # ==================================================================
    # API
    # ==================================================================

    key = env_required(
        CONFIG["agnes"]["api_key_env"]
    )

    url = (
        CONFIG["agnes"]["base_url"]
        .rstrip("/")
        + "/chat/completions"
    )

    # ==================================================================
    # 目标词标准化
    # ==================================================================

    words = normalize_target_words(words)

    print(
        f"✓ 目标词标准化完成：{len(words)} 个",
        flush=True,
    )

    for item in words:

        print(
            f"  - {item['word']}："
            f"{item.get('meaning', '')}",
            flush=True,
        )

    # ==================================================================
    # 提取真正给 Agnes 的目标词名称
    # ==================================================================

    target_word_list = target_word_names(
        words
    )

    if not target_word_list:

        raise ValueError(
            "没有有效目标词汇，无法生成英语短文。"
        )

    # ==================================================================
    # 任务定义
    # ==================================================================

    task = {

        "task": "生成英语学习短文",

        "difficulty": {

            "stars": difficulty,

            "star_name": difficulty_info["star"],

            "level": difficulty_info["level"],

            "display_label": difficulty_info["label"],

        },

        "article_type": {

            "id": article_type,

            "name": article_type_name,

            "rule": article_type_rule,

        },

        "target_length": length,

        "target_words": target_word_list,

        "target_word_details": words,

        "requirements": [

            # ----------------------------------------------------------
            # 标题
            # ----------------------------------------------------------

            "必须根据文章实际内容自行生成一个英文文章标题。",

            "标题必须与 article_en 的实际主题和内容高度相关。",

            "标题必须符合指定文章类型、指定难度和文章主题。",

            "标题应该自然、简洁、像真实英语文章的标题。",

            "每篇文章必须重新根据实际内容命名，禁止使用固定标题模板。",

            "禁止使用 Article、English Article、English Learning Article、My Article、Untitled、A Story、An Article 等泛化或占位标题。",

            "title 字段必须是非空字符串。",

            "title 字段中不要加入 Title:、标题：等前缀。",

            # ----------------------------------------------------------
            # 目标词
            # ----------------------------------------------------------

            "所有 target_words 必须进入 target_vocabulary。",

            "所有目标词必须以原形出现在 article_en 中。",

            "目标词必须自然地融入文章，不得机械堆砌。",

            # ----------------------------------------------------------
            # 文章
            # ----------------------------------------------------------

            "article_en 必须是一篇完整、自然、连贯的英语短文。",

            "article_zh 必须完整准确地翻译 article_en。",

            "英文文章实际内容必须符合指定文章类型。",

            # ----------------------------------------------------------
            # 难度
            # ----------------------------------------------------------

            "难度必须真实改变词汇、句法、句子长度、逻辑复杂度和文章结构。",

            "不得仅通过增加生僻词来伪造高难度。",

            # ----------------------------------------------------------
            # 学习解析
            # ----------------------------------------------------------

            "phrases 中的重点短语必须真实存在于 article_en 中。",

            "grammar_points 必须分析 article_en 中真实出现的语法。",

            "sentence_patterns 必须来自 article_en 中真实出现的句型。",

            "knowledge_structure 必须总结 article_en 的真实结构。",

            # ----------------------------------------------------------
            # JSON
            # ----------------------------------------------------------

            "所有字段必须严格按照 schema 返回。",

            "只返回合法JSON对象。",

            "不要Markdown。",

            "不要```。",

            "不要JSON之外的任何文字。",
        ],

        # ==================================================================
        # JSON Schema
        # ==================================================================

        "schema": {

            "title": "string",

            "article_en": "string",

            "article_zh": "string",

            "target_vocabulary": [

                {
                    "word": "string",
                    "meaning": "string",
                }

            ],

            "added_vocabulary": [

                {
                    "word": "string",
                    "meaning": "string",
                }

            ],

            "phrases": [

                {
                    "phrase": "string",
                    "meaning": "string",
                }

            ],

            "grammar_points": [

                {
                    "name": "string",
                    "explanation": "string",
                    "example": "string",
                }

            ],

            "sentence_patterns": [

                {
                    "pattern": "string",
                    "meaning": "string",
                    "example": "string",
                }

            ],

            "knowledge_structure": [

                {
                    "title": "string",
                    "content": "string",
                }

            ],

        },

    }

    # ==================================================================
    # Agnes Prompt
    # ==================================================================

    payload = {

        "model": CONFIG["agnes"]["model"],

        "temperature": 0.4,

        "messages": [

            {

                "role": "system",

                "content": (

                    "你是748686英语学习系统的专业英语教材生成器。"

                    "你必须严格按照用户提供的难度、文章类型、目标词汇和长度生成文章。"

                    "你必须为每一篇文章自行生成一个与文章实际内容匹配的英文标题。"

                    "标题必须具体、自然、简洁，并且真实反映文章主题。"

                    "禁止使用Article、English Article、English Learning Article、"
                    "My Article、Untitled、A Story、An Article等泛化或占位标题。"

                    "禁止使用固定标题模板。"

                    "不要在title中加入Title:或标题：前缀。"

                    "你不是普通聊天助手。"

                    "你的输出将被Python程序直接解析。"

                    "因此只能输出一个严格合法的JSON对象。"

                    "禁止Markdown。"

                    "禁止代码围栏。"

                    "禁止解释。"

                    "禁止JSON前后添加任何文字。"

                ),

            },

            {

                "role": "user",

                "content": json.dumps(
                    task,
                    ensure_ascii=False,
                    indent=2,
                ),

            },

        ],

    }

    # ==================================================================
    # JSON 解析循环
    # ==================================================================

    last_content = ""

    last_error = None

    for attempt in range(
        1,
        JSON_RETRIES + 1,
    ):

        print(
            f"📝 Agnes 文章生成 / JSON解析 "
            f"{attempt}/{JSON_RETRIES}",
            flush=True,
        )

        try:

            # ----------------------------------------------------------
            # 请求 Agnes
            # ----------------------------------------------------------

            data = request_article(
                key,
                url,
                payload,
            )

            # ----------------------------------------------------------
            # API 返回检查
            # ----------------------------------------------------------

            if not isinstance(
                data,
                dict,
            ):

                raise ValueError(
                    "Agnes API 返回不是 JSON 对象。"
                )

            choices = data.get(
                "choices"
            )

            if not choices:

                raise ValueError(
                    "Agnes 返回中没有 choices："
                    + json.dumps(
                        data,
                        ensure_ascii=False,
                    )
                )

            if not isinstance(
                choices,
                list,
            ):

                raise ValueError(
                    "Agnes 返回的 choices 不是数组。"
                )

            if not isinstance(
                choices[0],
                dict,
            ):

                raise ValueError(
                    "Agnes 返回的 choices[0] 不是对象。"
                )

            # ----------------------------------------------------------
            # 获取 message
            # ----------------------------------------------------------

            message = choices[0].get(
                "message",
                {},
            )

            if not isinstance(
                message,
                dict,
            ):

                raise ValueError(
                    "Agnes 返回的 message 不是对象。"
                )

            # ----------------------------------------------------------
            # 提取 content
            # ----------------------------------------------------------

            content = extract_message_content(
                message
            )

            # ==========================================================
            # Agnes 返回诊断
            # ==========================================================

            if not content:

                print(
                    "",
                    flush=True,
                )

                print(
                    "================ Agnes API 原始 choices[0] ================",
                    flush=True,
                )

                print(
                    json.dumps(
                        choices[0],
                        ensure_ascii=False,
                        indent=2,
                    ),
                    flush=True,
                )

                print(
                    "============================================================",
                    flush=True,
                )

                print(
                    "",
                    flush=True,
                )

                print(
                    "================ Agnes API 原始 message ================",
                    flush=True,
                )

                print(
                    json.dumps(
                        message,
                        ensure_ascii=False,
                        indent=2,
                    ),
                    flush=True,
                )

                print(
                    "=========================================================",
                    flush=True,
                )

                raise ValueError(
                    "Agnes 返回的 message.content 为空。"
                )

            # ----------------------------------------------------------
            # 保存原始内容
            # ----------------------------------------------------------

            last_content = content

            # ----------------------------------------------------------
            # JSON 解析
            # ----------------------------------------------------------

            result = parse_json_response(
                content
            )

            # ----------------------------------------------------------
            # 数据契约验证
            # ----------------------------------------------------------

            result = validate_result(
                result,
                words,
            )

            # ----------------------------------------------------------
            # 成功
            # ----------------------------------------------------------

            print(
                "✓ Agnes 文章 JSON 解析成功",
                flush=True,
            )

            print(
                f"✓ 文章标题：{result['title']}",
                flush=True,
            )

            print(
                f"✓ 文体：{article_type_name}",
                flush=True,
            )

            print(
                f"✓ 难度："
                f"{difficulty_info['star']} "
                f"({difficulty_info['level']})",
                flush=True,
            )

            print(
                f"✓ 目标词汇："
                f"{len(result['target_vocabulary'])}",
                flush=True,
            )

            print(
                f"✓ 新增词汇："
                f"{len(result['added_vocabulary'])}",
                flush=True,
            )

            print(
                f"✓ 重点短语："
                f"{len(result['phrases'])}",
                flush=True,
            )

            print(
                f"✓ 语法知识点："
                f"{len(result['grammar_points'])}",
                flush=True,
            )

            print(
                f"✓ 重点句型："
                f"{len(result['sentence_patterns'])}",
                flush=True,
            )

            print(
                f"✓ 知识结构："
                f"{len(result['knowledge_structure'])}",
                flush=True,
            )

            return result

        except Exception as e:

            # ==========================================================
            # 统一错误处理
            # ==========================================================

            last_error = e

            print(
                "",
                flush=True,
            )

            print(
                "⚠️ 文章 JSON / 数据验证失败",
                flush=True,
            )

            print(
                f"   {type(e).__name__}: {e}",
                flush=True,
            )

            # ----------------------------------------------------------
            # 最后一次
            # ----------------------------------------------------------

            if attempt >= JSON_RETRIES:

                break

            # ==========================================================
            # JSON 修复
            # ==========================================================

            if last_content:

                print(
                    "🔧 请求 Agnes 修复 JSON...",
                    flush=True,
                )

                try:

                    repair_payload = (
                        build_repair_payload(
                            last_content
                        )
                    )

                    repair_data = request_article(
                        key,
                        url,
                        repair_payload,
                    )

                    if not isinstance(
                        repair_data,
                        dict,
                    ):

                        raise ValueError(
                            "JSON 修复请求返回不是 JSON 对象。"
                        )

                    repair_choices = (
                        repair_data.get(
                            "choices"
                        )
                    )

                    if not repair_choices:

                        raise ValueError(
                            "JSON 修复请求没有返回 choices。"
                        )

                    if not isinstance(
                        repair_choices[0],
                        dict,
                    ):

                        raise ValueError(
                            "JSON 修复请求的 choices[0] 不是对象。"
                        )

                    repair_message = (
                        repair_choices[0].get(
                            "message",
                            {},
                        )
                    )

                    repair_content = (
                        extract_message_content(
                            repair_message
                        )
                    )

                    if not repair_content:

                        print(
                            "",
                            flush=True,
                        )

                        print(
                            "============= Agnes JSON修复原始 choices[0] =============",
                            flush=True,
                        )

                        print(
                            json.dumps(
                                repair_choices[0],
                                ensure_ascii=False,
                                indent=2,
                            ),
                            flush=True,
                        )

                        print(
                            "=========================================================",
                            flush=True,
                        )

                        raise ValueError(
                            "JSON 修复结果为空。"
                        )

                    result = parse_json_response(
                        repair_content
                    )

                    result = validate_result(
                        result,
                        words,
                    )

                    print(
                        "✓ Agnes JSON 修复成功",
                        flush=True,
                    )

                    print(
                        f"✓ 文章标题：{result['title']}",
                        flush=True,
                    )

                    return result

                except Exception as repair_error:

                    print(
                        "⚠️ JSON 自动修复失败："
                        f"{type(repair_error).__name__}: "
                        f"{repair_error}",
                        flush=True,
                    )

            # ----------------------------------------------------------
            # 等待后重新请求
            # ----------------------------------------------------------

            wait_seconds = 2 * attempt

            print(
                f"⏳ {wait_seconds} 秒后重新请求 Agnes...",
                flush=True,
            )

            time.sleep(
                wait_seconds
            )

    # ==================================================================
    # 最终失败
    # ==================================================================

    print(
        "",
        flush=True,
    )

    print(
        "❌ Agnes 文章生成最终失败",
        flush=True,
    )

    if last_error:

        print(
            f"错误：{last_error}",
            flush=True,
        )

    if last_content:

        print(
            "",
            flush=True,
        )

        print(
            "================ 原始 Agnes 返回 ================",
            flush=True,
        )

        print(
            last_content,
            flush=True,
        )

        print(
            "==================================================",
            flush=True,
        )

    raise RuntimeError(
        "Agnes 文章 JSON / 数据验证失败，"
        "已经达到最大重试次数。"
    )
