#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
主程序 V2.1

流程：

1. 读取 input/{date}.md
2. 提取目标词汇
3. 提取图片中的词汇
4. 目标词汇去重
5. Agnes 生成英语短文
6. 验证文章
7. 渲染最终 Obsidian Markdown
8. 如果 --exam=yes：
      8.1 生成英语试卷
      8.2 试卷立即独立落盘
      8.3 再独立生成答案
      8.4 生成每道题解析
      8.5 生成听力原文
      8.6 生成总体学习分析
      8.7 答案解析独立落盘
9. 写入 manifest.json

======================================================================
重要架构
======================================================================

英语短文：

    output/{date}/英语短文注记/

试卷：

    output/{date}/配套试卷/
        └── {difficulty}星_{article_type}_试卷.md

答案解析：

    output/{date}/配套试卷/
        └── {difficulty}星_{article_type}_答案解析.md

======================================================================
重要原则
======================================================================

试卷和答案解析完全分离。

试卷生成成功后立即写入磁盘。

即使答案解析生成失败：

    试卷仍然保留。

答案解析不会影响已经落盘的试卷。

======================================================================
音频参数
======================================================================

--audio：

    yes / no

--audio-format：

    mp3 / m4a / wav

例如：

    --audio "yes"
    --audio-format "mp3"

======================================================================
"""

import argparse
import json
import sys
from pathlib import Path


# ======================================================================
# 当前 scripts 目录加入 Python 路径
# ======================================================================

sys.path.insert(
    0,
    str(Path(__file__).parent),
)


# ======================================================================
# 系统模块
# ======================================================================

from common import ROOT, CONFIG

from input_parser import parse

from vision_extract import extract

from agnes_generate import (
    generate as gen_article,
    ARTICLE_TYPES,
)

from validate import article

from render_markdown import render

from exam_generate import (
    generate as gen_exam,
    render as render_exam,
)

from exam_answers import (
    generate as gen_answers,
    render as render_answers,
)


# ======================================================================
# 主程序
# ======================================================================

def main():

    # ==================================================================
    # 命令行参数
    # ==================================================================

    parser = argparse.ArgumentParser(
        description="02_英语学习系统"
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    parser.add_argument(
        "--difficulty",
        type=int,
        choices=range(1, 18),
        required=True,
    )

    parser.add_argument(
        "--article-type",
        choices=ARTICLE_TYPES,
        required=True,
    )

    parser.add_argument(
        "--length",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--exam",
        choices=["yes", "no"],
        default="no",
    )

    parser.add_argument(
        "--image",
        choices=["yes", "no"],
        default="no",
    )

    # ==================================================================
    # 注意：
    #
    # --audio 表示是否生成音频
    #
    # 所以这里必须是：
    #
    #     yes / no
    #
    # 不能写成：
    #
    #     mp3 / m4a / wav
    #
    # 音频格式由下面的 --audio-format 单独控制。
    # ==================================================================

    parser.add_argument(
        "--audio",
        choices=["yes", "no"],
        default="no",
    )

    parser.add_argument(
        "--audio-format",
        choices=["mp3", "m4a", "wav"],
        default="mp3",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
    )

    args = parser.parse_args()

    # ==================================================================
    # 基础信息
    # ==================================================================

    date = args.date

    difficulty = args.difficulty

    article_type = args.article_type

    article_type_name = ARTICLE_TYPES[
        article_type
    ]

    length = args.length

    print(
        "============================================================"
    )

    print(
        "02_英语学习系统"
    )

    print(
        "============================================================"
    )

    print(
        f"日期：{date}"
    )

    print(
        f"难度：{difficulty}星"
    )

    print(
        f"文章类型：{article_type_name}"
    )

    print(
        f"英文类型：{article_type}"
    )

    print(
        f"目标长度：约 {length} 词"
    )

    print(
        f"配套试卷：{args.exam}"
    )

    print(
        f"图片处理：{args.image}"
    )

    print(
        f"音频生成：{args.audio}"
    )

    print(
        f"音频格式：{args.audio_format}"
    )

    print(
        f"音频速度：{args.speed}"
    )

    print(
        "============================================================"
    )

    # ==================================================================
    # 输入文件
    # ==================================================================

    input_file = (
        ROOT
        / "input"
        / f"{date}.md"
    )

    if not input_file.exists():

        raise FileNotFoundError(
            f"输入文件不存在：{input_file}"
        )

    print(
        f"读取输入：{input_file}"
    )

    # ==================================================================
    # 读取目标词汇和图片
    # ==================================================================

    words, images = parse(
        input_file,
        CONFIG["limits"]["max_words"],
    )

    print(
        f"原始目标词汇：{len(words)}"
    )

    print(
        f"图片数量：{len(images)}"
    )

    # ==================================================================
    # OCR / Vision 提取图片中的词汇
    # ==================================================================

    if images:

        print(
            "开始处理图片中的目标词汇..."
        )

    for image in images:

        extracted_words = extract(
            image
        )

        if extracted_words:

            print(
                f"图片新增词汇：{len(extracted_words)}"
            )

            words.extend(
                extracted_words
            )

    # ==================================================================
    # 目标词汇去重
    # ==================================================================

    unique_words = {}

    for word in words:

        if not isinstance(
            word,
            dict,
        ):

            continue

        value = word.get(
            "word",
            "",
        )

        if not value:

            continue

        key = str(
            value
        ).strip().lower()

        if not key:

            continue

        if key not in unique_words:

            unique_words[key] = word

    words = list(
        unique_words.values()
    )

    print(
        f"最终目标词汇：{len(words)}"
    )

    if words:

        print(
            "目标词汇："
        )

        for item in words:

            word = item.get(
                "word",
                "",
            )

            meaning = item.get(
                "meaning",
                "",
            )

            if meaning:

                print(
                    f"  - {word}：{meaning}"
                )

            else:

                print(
                    f"  - {word}"
                )

    # ==================================================================
    # 输出目录
    # ==================================================================

    output_dir = (
        ROOT
        / "output"
        / date
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ==================================================================
    # Agnes 生成文章
    # ==================================================================

    print()
    print(
        "============================================================"
    )

    print(
        "ARTICLE GENERATION"
    )

    print(
        "============================================================"
    )

    art = gen_article(
        words,
        difficulty,
        article_type,
        length,
    )

    print(
        f"文章标题：{art.get('title', '')}"
    )

    # ==================================================================
    # 文章验证
    # ==================================================================

    print()
    print(
        "ARTICLE VALIDATION"
    )

    article(
        art,
        words,
    )

    print(
        "✓ 文章验证通过"
    )

    # ==================================================================
    # 英语短文注记
    # ==================================================================

    note_dir = (
        output_dir
        / "英语短文注记"
    )

    note_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    note = render(
        art,
        words,
        difficulty,
        article_type_name,
        date,
        length,
    )

    note_file = (
        note_dir
        / f"{difficulty}星_{article_type_name}.md"
    )

    note_file.write_text(
        note,
        encoding="utf-8",
    )

    print(
        f"✓ 英语短文注记已保存：{note_file}"
    )

    # ==================================================================
    # 配套试卷
    # ==================================================================

    if args.exam == "yes":

        exam_dir = (
            output_dir
            / "配套试卷"
        )

        exam_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ==============================================================
        # 第一阶段：
        #
        # 只生成试卷
        #
        # 不生成答案
        # 不生成解析
        # 不生成听力原文
        # 不生成总体分析
        # ==============================================================

        print()
        print(
            "============================================================"
        )

        print(
            "EXAM PAPER GENERATION"
        )

        print(
            "============================================================"
        )

        print(
            "现在只生成考生试卷。"
        )

        print(
            "答案、解析、听力原文不会在本阶段生成。"
        )

        exam = gen_exam(
            art,
            difficulty,
            article_type,
            words,
        )

        # ==============================================================
        # 试卷立即渲染
        # ==============================================================

        exam_markdown = render_exam(
            exam,
            art["title"],
            difficulty,
            article_type_name,
        )

        exam_file = (
            exam_dir
            / f"{difficulty}星_{article_type_name}_试卷.md"
        )

        # ==============================================================
        # 非常重要：
        #
        # 试卷在这里立即写入磁盘。
        #
        # 后面的答案解析如果失败：
        #
        #     试卷不会消失
        #
        #     试卷不会被覆盖
        #
        #     试卷已经成为独立文件
        # ==============================================================

        exam_file.write_text(
            exam_markdown,
            encoding="utf-8",
        )

        print()
        print(
            "✓ 配套试卷已立即落盘："
        )

        print(
            f"  {exam_file}"
        )

        # ==============================================================
        # 第二阶段：
        #
        # 独立生成答案 / 解析
        # ==============================================================

        print()
        print(
            "============================================================"
        )

        print(
            "EXAM ANSWERS / ANALYSIS GENERATION"
        )

        print(
            "============================================================"
        )

        print(
            "现在开始独立生成："
        )

        print(
            "  1. 答案"
        )

        print(
            "  2. 每道题解析"
        )

        print(
            "  3. 听力原文"
        )

        print(
            "  4. 总体学习分析"
        )

        print()

        # ==============================================================
        # 生成答案 / 解析
        #
        # 注意：
        #
        # 这里读取的是刚刚已经生成成功的 exam。
        #
        # 如果这里失败：
        #
        #     上面的 exam_file 仍然存在。
        # ==============================================================

        answer_result = gen_answers(
            exam,
            art,
            difficulty,
            article_type,
            words,
        )

        # ==============================================================
        # 答案解析 Markdown
        # ==============================================================

        answer_markdown = render_answers(
            answer_result,
            art["title"],
            difficulty,
            article_type_name,
        )

        answer_file = (
            exam_dir
            / f"{difficulty}星_{article_type_name}_答案解析.md"
        )

        answer_file.write_text(
            answer_markdown,
            encoding="utf-8",
        )

        print()
        print(
            "✓ 答案解析已保存："
        )

        print(
            f"  {answer_file}"
        )

        # ==============================================================
        # 考试系统完成
        # ==============================================================

        print()
        print(
            "============================================================"
        )

        print(
            "EXAM COMPLETE"
        )

        print(
            "============================================================"
        )

        print(
            f"✓ 试卷：{exam_file}"
        )

        print(
            f"✓ 答案解析：{answer_file}"
        )

    # ==================================================================
    # Manifest
    # ==================================================================

    manifest = {

        "date": date,

        "difficulty": difficulty,

        "article_type": article_type_name,

        "article_type_en": article_type,

        "length": length,

        "exam": args.exam,

        "image": args.image,

        # ==============================================================
        # 正确记录：
        #
        # audio = yes/no
        # audio_format = mp3/m4a/wav
        # ==============================================================

        "audio": args.audio,

        "audio_format": args.audio_format,

        "speed": args.speed,

        "target_words": words,

        "article_title": art.get(
            "title",
            "",
        ),

    }

    manifest_file = (
        output_dir
        / "manifest.json"
    )

    manifest_file.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"✓ manifest 已保存：{manifest_file}"
    )

    # ==================================================================
    # 完成
    # ==================================================================

    print()
    print(
        "============================================================"
    )

    print(
        f"完成：{output_dir}"
    )

    print(
        "============================================================"
    )


# ======================================================================
# 程序入口
# ======================================================================

if __name__ == "__main__":

    main()
