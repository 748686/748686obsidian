#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
配套试卷生成器 V2

============================================================
核心目标
============================================================

严格按照“英语短文注记配套试卷”完成版模板生成：

英语短文注记配套试卷 — {文章标题}
{星级难度}（{对应级别}） | 文体：{文体} | 满分：100分
文章标题：{文章标题}
（满分：100分    时间：60分钟）
姓名：__________    班级：__________    得分：__________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

一、听力
Part A 听句子，选出你所听到的单词
Part B 听对话，选择正确答案
Part C 听短文，选择正确答案

二、单项选择

三、多选题

四、完形填空

五、阅读理解

六、翻译
Part A 汉译英
Part B 英译汉

七、写作

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

参考答案与听力原文

听力原文
一、答案
二、答案
三、答案
四、答案
五、答案
六、答案
七、答案

============================================================
兼容 main.py
============================================================

main.py 继续使用：

    generate(...)
    render(...)

无需修改调用接口。
"""

import json
import re

from common import CONFIG, env_required, request_json


JSON_RETRIES = 3


# ==========================================================
# 17 星难度
# ==========================================================

DIFFICULTIES = {
    1: {
        "star_name": "一星",
        "level": "小学1-4年级",
        "label": "小学",
    },
    2: {
        "star_name": "二星",
        "level": "小学高年级-初一",
        "label": "小学高年级-初一",
    },
    3: {
        "star_name": "三星",
        "level": "初二-初四",
        "label": "初二-初四",
    },
    4: {
        "star_name": "四星",
        "level": "高一",
        "label": "高一",
    },
    5: {
        "star_name": "五星",
        "level": "高二",
        "label": "高二",
    },
    6: {
        "star_name": "六星",
        "level": "高三",
        "label": "高三",
    },
    7: {
        "star_name": "七星",
        "level": "大学",
        "label": "大学",
    },
    8: {
        "star_name": "八星",
        "level": "四级",
        "label": "四级",
    },
    9: {
        "star_name": "九星",
        "level": "六级",
        "label": "六级",
    },
    10: {
        "star_name": "十星",
        "level": "专四",
        "label": "专四",
    },
    11: {
        "star_name": "十一星",
        "level": "专六",
        "label": "专六",
    },
    12: {
        "star_name": "十二星",
        "level": "专八",
        "label": "专八",
    },
    13: {
        "star_name": "十三星",
        "level": "考研",
        "label": "考研",
    },
    14: {
        "star_name": "十四星",
        "level": "考博",
        "label": "考博",
    },
    15: {
        "star_name": "十五",
        "level": "托福",
        "label": "托福",
    },
    16: {
        "star_name": "十六星",
        "level": "雅思",
        "label": "雅思",
    },
    17: {
        "star_name": "十七星",
        "level": "GRE",
        "label": "GRE",
    },
}


# ==========================================================
# 17 种文章类型
# ==========================================================

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


# ==========================================================
# JSON 清理
# ==========================================================

def clean_json_content(content):
    if content is None:
        return ""

    content = str(content).strip()

    if not content:
        return ""

    # 去掉 Markdown JSON 围栏
    content = re.sub(
        r"^```(?:json|JSON)?\s*",
        "",
        content,
    )

    content = re.sub(
        r"\s*```\s*$",
        "",
        content,
    )

    content = content.strip()

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

        # 再尝试寻找 JSON 对象
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

        # 某些模型可能返回 content 数组
        if isinstance(content, list):

            texts = []

            for item in content:

                if isinstance(item, dict):

                    text = item.get(
                        "text",
                        item.get("content", "")
                    )

                    if text:
                        texts.append(str(text))

                elif isinstance(item, str):

                    texts.append(item)

            content = "\n".join(texts)

        return content

    except (KeyError, TypeError, IndexError) as exc:

        raise ValueError(
            f"Agnes 返回结构异常：{data}"
        ) from exc


# ==========================================================
# 通用工具
# ==========================================================

def _to_text(value):

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(
        value,
        (int, float, bool),
    ):
        return str(value)

    if isinstance(value, dict):

        preferred_keys = [
            "text",
            "question",
            "title",
            "name",
            "content",
            "answer",
            "analysis",
            "explanation",
            "meaning",
            "pattern",
            "prompt",
        ]

        parts = []

        for key in preferred_keys:

            if key not in value:
                continue

            text = _to_text(
                value[key]
            )

            if text:
                parts.append(text)

        if parts:
            return "；".join(parts)

        return "；".join(
            f"{key}: {_to_text(val)}"
            for key, val in value.items()
            if _to_text(val)
        )

    if isinstance(value, list):

        return "；".join(
            _to_text(item)
            for item in value
            if _to_text(item)
        )

    return str(value)


def _ensure_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


# ==========================================================
# 题目字段提取
# ==========================================================

def _question_text(question):

    if not isinstance(question, dict):
        return _to_text(question)

    for key in (
        "question",
        "text",
        "content",
        "prompt",
    ):

        value = question.get(key)

        if value:
            return _to_text(value)

    return ""


def _options(question):

    if not isinstance(question, dict):
        return []

    options = question.get(
        "options",
        []
    )

    return _ensure_list(options)


def _option_text(option):

    if isinstance(option, str):
        return option.strip()

    if isinstance(option, dict):

        # 优先支持：
        # {"label":"A","text":"xxx"}

        label = _to_text(
            option.get("label", "")
        )

        text = _to_text(
            option.get(
                "text",
                option.get(
                    "content",
                    option.get(
                        "option",
                        ""
                    )
                )
            )
        )

        if label and text:
            return f"{label}. {text}"

        if text:
            return text

        return _to_text(option)

    return _to_text(option)


# ==========================================================
# 试卷 JSON 结构验证
# ==========================================================

def validate_exam(exam):

    if not isinstance(exam, dict):

        raise ValueError(
            "试卷 JSON 顶层必须是 object"
        )

    required = [
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

    missing = [
        key
        for key in required
        if key not in exam
    ]

    if missing:

        raise ValueError(
            "试卷 JSON 缺少必要字段："
            + ", ".join(missing)
        )

    for key in required:

        if key == "listening_script":
            continue

        if not isinstance(
            exam[key],
            (list, dict, str),
        ):

            raise ValueError(
                f"字段 {key} 类型异常"
            )

    # 必须至少有一道正式题目
    question_fields = [
        "listening",
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
        "translation",
        "writing",
    ]

    total = 0

    for field in question_fields:

        value = exam.get(field)

        if isinstance(value, list):
            total += len(value)

        elif isinstance(value, dict):
            total += 1

    if total == 0:

        raise ValueError(
            "试卷没有任何题目"
        )

    return True


# ==========================================================
# 生成 Prompt
# ==========================================================

def build_exam_payload(
    article,
    difficulty,
    article_type,
    words,
):

    diff = DIFFICULTIES.get(
        difficulty,
        DIFFICULTIES[1],
    )

    target_words = []

    for item in words:

        if isinstance(item, dict):

            word = str(
                item.get("word", "")
            ).strip()

            meaning = str(
                item.get("meaning", "")
            ).strip()

            if word:
                target_words.append({
                    "word": word,
                    "meaning": meaning,
                })

        else:

            word = str(item).strip()

            if word:
                target_words.append({
                    "word": word,
                    "meaning": "",
                })

    return {

        "task":
            "根据给定英语学习文章生成完整配套试卷",

        "difficulty": {
            "number": difficulty,
            "star_name": diff["star_name"],
            "level": diff["level"],
            "label": diff["label"],
        },

        "article_type": {
            "id": article_type,
            "name": ARTICLE_TYPES.get(
                article_type,
                article_type,
            ),
        },

        "target_words": target_words,

        "article": {
            "title": article.get(
                "title",
                "",
            ),

            "article_en": article.get(
                "article_en",
                "",
            ),

            "article_zh": article.get(
                "article_zh",
                "",
            ),
        },

        "requirements": [

            # ------------------------------------------------
            # 总体要求
            # ------------------------------------------------

            "必须严格围绕给定文章命题",

            "所有题目必须能够从文章内容找到依据",

            "不得凭空加入文章之外的知识",

            "题目难度必须与指定星级一致",

            "必须生成完整试卷，不得只生成阅读理解题",

            "必须生成完整答案",

            "必须生成答案解析",

            # ------------------------------------------------
            # 七大题型
            # ------------------------------------------------

            "试卷必须包含七个部分",

            "第一部分必须是听力",

            "第二部分必须是单项选择",

            "第三部分必须是多选题",

            "第四部分必须是完形填空",

            "第五部分必须是阅读理解",

            "第六部分必须是翻译",

            "第七部分必须是写作",

            # ------------------------------------------------
            # 听力
            # ------------------------------------------------

            "听力必须包含 Part A、Part B、Part C",

            "Part A 为听句子，选出你所听到的单词",

            "Part B 为听对话，选择正确答案",

            "Part C 为听短文，选择正确答案",

            "必须提供完整听力原文",

            "听力原文必须与听力题目严格对应",

            "听力原文不能依赖文章之外的内容",

            # ------------------------------------------------
            # 单项选择
            # ------------------------------------------------

            "单项选择每题必须有 A、B、C、D 四个选项",

            "每题只有一个正确答案",

            # ------------------------------------------------
            # 多选题
            # ------------------------------------------------

            "多选题每题必须有 A、B、C、D 四个选项",

            "多选题可以有两个或多个正确答案",

            # ------------------------------------------------
            # 完形填空
            # ------------------------------------------------

            "完形填空必须提供完整短文",

            "空格必须使用明确的编号",

            "每个空必须提供 A、B、C、D 四个选项",

            # ------------------------------------------------
            # 阅读理解
            # ------------------------------------------------

            "阅读理解必须围绕给定文章",

            "必须提供题目和选项",

            # ------------------------------------------------
            # 翻译
            # ------------------------------------------------

            "翻译必须包含 Part A 汉译英",

            "翻译必须包含 Part B 英译汉",

            "翻译内容必须来自文章核心内容",

            # ------------------------------------------------
            # 写作
            # ------------------------------------------------

            "写作必须与文章主题相关",

            "必须给出明确写作要求",

            # ------------------------------------------------
            # 目标词
            # ------------------------------------------------

            "尽可能考查给定目标词汇",

            "目标词可以出现在单选、多选、完形、阅读、翻译等题型中",

            # ------------------------------------------------
            # JSON
            # ------------------------------------------------

            "只输出合法 JSON",

            "不要输出 Markdown 代码围栏",

            "不要输出 JSON 之外的说明",

        ],

        "score_structure": {

            "total_score": 100,

            "sections": [
                "listening",
                "single_choice",
                "multiple_choice",
                "cloze",
                "reading",
                "translation",
                "writing",
            ],
        },

        "schema": {

            "title":
                "string",

            "listening": [
                {
                    "part": "A",
                    "instruction": "string",
                    "score": 10,
                    "questions": [
                        {
                            "question": "string",
                            "options": [
                                "A. string",
                                "B. string",
                                "C. string",
                                "D. string",
                            ],
                            "answer": "A",
                            "analysis": "string",
                        }
                    ],
                }
            ],

            "single_choice": [
                {
                    "question": "string",
                    "options": [
                        "A. string",
                        "B. string",
                        "C. string",
                        "D. string",
                    ],
                    "answer": "A",
                    "analysis": "string",
                }
            ],

            "multiple_choice": [
                {
                    "question": "string",
                    "options": [
                        "A. string",
                        "B. string",
                        "C. string",
                        "D. string",
                    ],
                    "answer": ["A", "C"],
                    "analysis": "string",
                }
            ],

            "cloze": [
                {
                    "passage": "string",
                    "questions": [
                        {
                            "number": 1,
                            "options": [
                                "A. string",
                                "B. string",
                                "C. string",
                                "D. string",
                            ],
                            "answer": "A",
                            "analysis": "string",
                        }
                    ],
                }
            ],

            "reading": [
                {
                    "question": "string",
                    "options": [
                        "A. string",
                        "B. string",
                        "C. string",
                        "D. string",
                    ],
                    "answer": "A",
                    "analysis": "string",
                }
            ],

            "translation": {
                "part_a": [
                    {
                        "question": "中文句子",
                        "answer": "English answer",
                        "analysis": "string",
                    }
                ],
                "part_b": [
                    {
                        "question": "English sentence",
                        "answer": "中文答案",
                        "analysis": "string",
                    }
                ],
            },

            "writing": [
                {
                    "prompt": "string",
                    "requirements": [
                        "string"
                    ],
                    "reference_answer": "string",
                    "analysis": "string",
                }
            ],

            "listening_script": {
                "part_a": "string",
                "part_b": "string",
                "part_c": "string",
            },

            "answers": {
                "listening": [],
                "single_choice": [],
                "multiple_choice": [],
                "cloze": [],
                "reading": [],
                "translation": {},
                "writing": [],
            },

            "analysis": {
                "general": "string",
            },
        },
    }


# ==========================================================
# JSON 修复
# ==========================================================

def build_repair_payload(raw_content):

    return {

        "task":
            "修复配套试卷 JSON",

        "instructions": [

            "当前内容应该是 JSON",

            "只修复 JSON 语法或结构格式问题",

            "不要删除任何题目",

            "不要增加新的题目",

            "不要修改题目内容",

            "不要修改答案",

            "不要修改解析",

            "必须保留七大题型",

            "必须保留听力原文",

            "不要输出 Markdown",

            "不要解释",

            "只输出合法 JSON 对象",

        ],

        "required_structure": [
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
        ],

        "broken_json": str(
            raw_content
        ),
    }


# ==========================================================
# Agnes 请求
# ==========================================================

def request_exam(
    key,
    url,
    payload,
):

    return request_json(
        "POST",
        url,
        headers={
            "Authorization":
                f"Bearer {key}",

            "Content-Type":
                "application/json",
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
    words,
):

    key = env_required(
        CONFIG["agnes"]["api_key_env"]
    )

    url = (
        CONFIG["agnes"]["base_url"].rstrip("/")
        + "/chat/completions"
    )

    payload = build_exam_payload(
        article,
        difficulty,
        article_type,
        words,
    )

    request_payload = {

        "model":
            CONFIG["agnes"]["model"],

        "temperature":
            0.3,

        "messages": [

            {
                "role": "system",

                "content": (
                    "你是一名严格的英语考试命题专家。"
                    "你的任务是根据给定英语学习文章，"
                    "生成完整配套试卷。"
                    "必须严格按照用户提供的七大题型结构。"
                    "必须只输出合法JSON。"
                    "禁止输出Markdown代码围栏。"
                    "禁止输出JSON之外的任何文字。"
                ),
            },

            {
                "role": "user",

                "content": json.dumps(
                    payload,
                    ensure_ascii=False,
                ),
            },

        ],
    }

    last_raw_content = ""

    for attempt in range(
        1,
        JSON_RETRIES + 1,
    ):

        print(
            f"📝 Agnes 配套试卷生成 "
            f"{attempt}/{JSON_RETRIES}"
        )

        try:

            data = request_exam(
                key,
                url,
                request_payload,
            )

            content = extract_content(
                data
            )

            last_raw_content = content

            try:

                exam = parse_json_response(
                    content
                )

                validate_exam(
                    exam
                )

                print(
                    "✓ Agnes 完整配套试卷 "
                    "JSON 解析成功"
                )

                return exam

            except Exception as parse_error:

                print(
                    "⚠ 配套试卷 JSON "
                    f"解析/验证失败：{parse_error}"
                )

                if attempt < JSON_RETRIES:

                    print(
                        "🔧 请求 Agnes 修复 "
                        "配套试卷 JSON..."
                    )

                    repair_payload = {

                        "model":
                            CONFIG["agnes"]["model"],

                        "temperature":
                            0.0,

                        "messages": [

                            {
                                "role":
                                    "system",

                                "content": (
                                    "你是严格的JSON修复器。"
                                    "只输出合法JSON。"
                                    "不得解释。"
                                    "不得输出Markdown。"
                                ),
                            },

                            {
                                "role":
                                    "user",

                                "content":
                                    json.dumps(
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

                        repair_content = (
                            extract_content(
                                repair_data
                            )
                        )

                        repaired_exam = (
                            parse_json_response(
                                repair_content
                            )
                        )

                        validate_exam(
                            repaired_exam
                        )

                        print(
                            "✓ Agnes 配套试卷 "
                            "JSON 修复成功"
                        )

                        return repaired_exam

                    except Exception as repair_error:

                        print(
                            "⚠ 配套试卷 JSON "
                            f"修复失败：{repair_error}"
                        )

        except Exception as request_error:

            print(
                "⚠ 配套试卷请求失败："
                f"{request_error}"
            )

    print("")
    print("=" * 70)
    print("❌ 配套试卷生成最终失败")
    print("=" * 70)

    if last_raw_content:

        print(
            "Agnes 原始返回："
        )

        print(
            str(last_raw_content)[:12000]
        )

    print("=" * 70)

    raise RuntimeError(
        "Agnes 配套试卷生成失败，"
        f"已尝试 {JSON_RETRIES} 次。"
    )


# ==========================================================
# Markdown：星星
# ==========================================================

def _stars(difficulty):

    difficulty = max(
        1,
        min(17, int(difficulty)),
    )

    return (
        "★" * difficulty
        +
        "☆" * (17 - difficulty)
    )


# ==========================================================
# Markdown：题目渲染
# ==========================================================

def _render_options(options):

    lines = []

    for option in _ensure_list(options):

        text = _option_text(option)

        if text:
            lines.append(
                f"   {text}"
            )

    return "\n".join(lines)


def _render_question(
    number,
    question,
    include_analysis=False,
):

    lines = []

    text = _question_text(
        question
    )

    if text:

        lines.append(
            f"{number}. {text}"
        )

    options = _options(
        question
    )

    if options:

        lines.append(
            _render_options(
                options
            )
        )

    if include_analysis:

        answer = _to_text(
            question.get(
                "answer",
                ""
            )
            if isinstance(
                question,
                dict
            )
            else ""
        )

        analysis = _to_text(
            question.get(
                "analysis",
                ""
            )
            if isinstance(
                question,
                dict
            )
            else ""
        )

        if answer:
            lines.append(
                f"答案：{answer}"
            )

        if analysis:
            lines.append(
                f"解析：{analysis}"
            )

    return "\n\n".join(
        line
        for line in lines
        if line
    )


# ==========================================================
# Part A / B / C
# ==========================================================

def _find_part(
    listening,
    letter,
):

    for part in _ensure_list(
        listening
    ):

        if not isinstance(
            part,
            dict
        ):
            continue

        value = str(
            part.get(
                "part",
                ""
            )
        ).strip().upper()

        if value == letter:
            return part

    return {}


def _render_listening(
    listening
):

    blocks = []

    for letter, default_instruction, default_score in [

        (
            "A",
            "听句子，选出你所听到的单词。",
            10,
        ),

        (
            "B",
            "听对话，选择正确答案。",
            10,
        ),

        (
            "C",
            "听短文，选择正确答案。",
            10,
        ),

    ]:

        part = _find_part(
            listening,
            letter,
        )

        instruction = _to_text(
            part.get(
                "instruction",
                default_instruction,
            )
        )

        score = part.get(
            "score",
            default_score,
        )

        blocks.append(
            f"Part {letter} "
            f"{instruction}（{score}分）"
        )

        questions = part.get(
            "questions",
            []
        )

        for index, question in enumerate(
            _ensure_list(questions),
            start=1,
        ):

            rendered = _render_question(
                index,
                question,
            )

            if rendered:
                blocks.append(
                    rendered
                )

    return "\n\n".join(
        blocks
    )


# ==========================================================
# 普通选择题
# ==========================================================

def _render_choice_section(
    questions
):

    blocks = []

    for index, question in enumerate(
        _ensure_list(questions),
        start=1,
    ):

        rendered = _render_question(
            index,
            question,
        )

        if rendered:
            blocks.append(
                rendered
            )

    return "\n\n".join(
        blocks
    )


# ==========================================================
# 完形填空
# ==========================================================

def _render_cloze(
    cloze
):

    blocks = []

    for item in _ensure_list(
        cloze
    ):

        if not isinstance(
            item,
            dict
        ):
            text = _to_text(item)

            if text:
                blocks.append(text)

            continue

        passage = _to_text(
            item.get(
                "passage",
                ""
            )
        )

        if passage:
            blocks.append(
                passage
            )

        questions = item.get(
            "questions",
            []
        )

        for index, question in enumerate(
            _ensure_list(questions),
            start=1,
        ):

            if isinstance(
                question,
                dict
            ):

                number = question.get(
                    "number",
                    index,
                )

            else:

                number = index

            rendered = _render_question(
                number,
                question,
            )

            if rendered:
                blocks.append(
                    rendered
                )

    return "\n\n".join(
        blocks
    )


# ==========================================================
# 翻译
# ==========================================================

def _render_translation(
    translation
):

    if not isinstance(
        translation,
        dict
    ):

        return _to_text(
            translation
        )

    blocks = []

    part_a = translation.get(
        "part_a",
        []
    )

    blocks.append(
        "Part A 汉译英（5分）"
    )

    for index, item in enumerate(
        _ensure_list(part_a),
        start=1,
    ):

        if isinstance(
            item,
            dict
        ):

            question = _to_text(
                item.get(
                    "question",
                    ""
                )
            )

        else:

            question = _to_text(
                item
            )

        if question:

            blocks.append(
                f"{index}. {question}"
            )

    part_b = translation.get(
        "part_b",
        []
    )

    blocks.append(
        "Part B 英译汉（5分）"
    )

    for index, item in enumerate(
        _ensure_list(part_b),
        start=1,
    ):

        if isinstance(
            item,
            dict
        ):

            question = _to_text(
                item.get(
                    "question",
                    ""
                )
            )

        else:

            question = _to_text(
                item
            )

        if question:

            blocks.append(
                f"{index}. {question}"
            )

    return "\n\n".join(
        blocks
    )


# ==========================================================
# 写作
# ==========================================================

def _render_writing(
    writing
):

    blocks = []

    for index, item in enumerate(
        _ensure_list(writing),
        start=1,
    ):

        if isinstance(
            item,
            dict
        ):

            prompt = _to_text(
                item.get(
                    "prompt",
                    item.get(
                        "question",
                        ""
                    )
                )
            )

            requirements = item.get(
                "requirements",
                []
            )

        else:

            prompt = _to_text(item)
            requirements = []

        if prompt:

            blocks.append(
                f"{index}. {prompt}"
            )

        req_lines = []

        for req in _ensure_list(
            requirements
        ):

            text = _to_text(req)

            if text:
                req_lines.append(
                    f"- {text}"
                )

        if req_lines:

            blocks.append(
                "\n".join(req_lines)
            )

    return "\n\n".join(
        blocks
    )


# ==========================================================
# 听力原文
# ==========================================================

def _render_listening_script(
    script
):

    if not isinstance(
        script,
        dict
    ):

        return _to_text(
            script
        )

    blocks = []

    mapping = [
        (
            "part_a",
            "Part A",
        ),
        (
            "part_b",
            "Part B",
        ),
        (
            "part_c",
            "Part C",
        ),
    ]

    for key, label in mapping:

        text = _to_text(
            script.get(
                key,
                ""
            )
        )

        if text:

            blocks.append(
                f"{label}\n\n{text}"
            )

    return "\n\n".join(
        blocks
    )


# ==========================================================
# 答案
# ==========================================================

def _render_answer_list(
    values
):

    lines = []

    for index, value in enumerate(
        _ensure_list(values),
        start=1,
    ):

        if isinstance(
            value,
            dict
        ):

            answer = _to_text(
                value.get(
                    "answer",
                    value.get(
                        "correct_answer",
                        ""
                    )
                )
            )

        else:

            answer = _to_text(
                value
            )

        if answer:

            lines.append(
                f"{index}. {answer}"
            )

    return "\n".join(
        lines
    )


def _render_answers(
    answers
):

    if not isinstance(
        answers,
        dict
    ):

        text = _to_text(
            answers
        )

        return text or "—"

    blocks = []

    mapping = [
        (
            "listening",
            "一、答案",
        ),
        (
            "single_choice",
            "二、答案",
        ),
        (
            "multiple_choice",
            "三、答案",
        ),
        (
            "cloze",
            "四、答案",
        ),
        (
            "reading",
            "五、答案",
        ),
        (
            "translation",
            "六、答案",
        ),
        (
            "writing",
            "七、答案",
        ),
    ]

    for key, label in mapping:

        blocks.append(
            label
        )

        value = answers.get(
            key,
            []
        )

        if isinstance(
            value,
            dict
        ):

            # 翻译等结构化答案
            text_parts = []

            for sub_key, sub_value in value.items():

                text = _to_text(
                    sub_value
                )

                if text:

                    text_parts.append(
                        f"{sub_key}: {text}"
                    )

            answer_text = "\n".join(
                text_parts
            )

        else:

            answer_text = (
                _render_answer_list(
                    value
                )
            )

        blocks.append(
            answer_text or "—"
        )

    return "\n\n".join(
        blocks
    )


# ==========================================================
# 答案解析
# ==========================================================

def _render_analysis(
    analysis,
    exam,
):

    blocks = []

    if isinstance(
        analysis,
        dict
    ):

        general = _to_text(
            analysis.get(
                "general",
                ""
            )
        )

        if general:
            blocks.append(
                general
            )

    elif analysis:

        blocks.append(
            _to_text(
                analysis
            )
        )

    # 如果题目本身携带解析，
    # 这里统一汇总出来。
    section_map = [
        (
            "single_choice",
            "单项选择",
        ),
        (
            "multiple_choice",
            "多选题",
        ),
        (
            "cloze",
            "完形填空",
        ),
        (
            "reading",
            "阅读理解",
        ),
    ]

    for field, label in section_map:

        questions = exam.get(
            field,
            []
        )

        section_lines = []

        for index, question in enumerate(
            _ensure_list(questions),
            start=1,
        ):

            if not isinstance(
                question,
                dict
            ):
                continue

            explanation = _to_text(
                question.get(
                    "analysis",
                    question.get(
                        "explanation",
                        ""
                    )
                )
            )

            if explanation:

                section_lines.append(
                    f"{index}. {explanation}"
                )

        if section_lines:

            blocks.append(
                f"{label}\n\n"
                + "\n".join(
                    section_lines
                )
            )

    return "\n\n".join(
        blocks
    ) or "—"


# ==========================================================
# 最终 Markdown
# ==========================================================

def render(
    e,
    title,
    difficulty,
    article_type,
):

    """
    将完整试卷 JSON
    渲染为 Obsidian Markdown。

    main.py 调用方式保持不变：

        render(
            e,
            title,
            difficulty,
            article_type,
        )
    """

    difficulty = int(
        difficulty
    )

    diff = DIFFICULTIES.get(
        difficulty,
        DIFFICULTIES[1],
    )

    article_type_name = ARTICLE_TYPES.get(
        article_type,
        article_type,
    )

    exam_title = _to_text(
        e.get(
            "title",
            f"{title} 配套试卷",
        )
    )

    if not exam_title:
        exam_title = (
            f"{title} 配套试卷"
        )

    listening_text = _render_listening(
        e.get(
            "listening",
            []
        )
    )

    single_choice_text = (
        _render_choice_section(
            e.get(
                "single_choice",
                []
            )
        )
    )

    multiple_choice_text = (
        _render_choice_section(
            e.get(
                "multiple_choice",
                []
            )
        )
    )

    cloze_text = _render_cloze(
        e.get(
            "cloze",
            []
        )
    )

    reading_text = (
        _render_choice_section(
            e.get(
                "reading",
                []
            )
        )
    )

    translation_text = (
        _render_translation(
            e.get(
                "translation",
                {}
            )
        )
    )

    writing_text = _render_writing(
        e.get(
            "writing",
            []
        )
    )

    listening_script_text = (
        _render_listening_script(
            e.get(
                "listening_script",
                {}
            )
        )
    )

    answers_text = _render_answers(
        e.get(
            "answers",
            {}
        )
    )

    analysis_text = _render_analysis(
        e.get(
            "analysis",
            {}
        ),
        e,
    )

    # ------------------------------------------------------
    # 最终文档
    # ------------------------------------------------------

    return f"""---
difficulty: {difficulty}星
difficulty_level: {diff["level"]}
article_type: {article_type_name}
source_article: {title}
---

英语短文注记配套试卷 — {exam_title}
{diff["star_name"]}难度（{diff["level"]}）  |  文体：{article_type_name}  |  满分：100分
文章标题：{title}
（满分：100分    时间：60分钟）
姓名：__________    班级：__________    得分：__________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

一、听力（共20分）

（注：听力原文不印在试卷上，请听老师朗读后作答）

{listening_text or "—"}

二、单项选择（共10分）

{single_choice_text or "—"}

三、多选题（共10分）

{multiple_choice_text or "—"}

四、完形填空（共10分）

{cloze_text or "—"}

五、阅读理解（共10分）

{reading_text or "—"}

六、翻译（共10分）

{translation_text or "—"}

七、写作（共10分）

{writing_text or "—"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

参考答案与听力原文

听力原文

{listening_script_text or "—"}

{answers_text}

答案解析

{analysis_text}

"""
    

# ==========================================================
# 直接运行保护
# ==========================================================

if __name__ == "__main__":

    print(
        "exam_generate.py 是模块文件，"
        "请通过 main.py 调用。"
    )
