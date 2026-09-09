#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
主程序

流程：

1. 读取 input/{date}.md
2. 提取目标词汇
3. 提取图片中的词汇
4. 目标词汇去重
5. Agnes 生成英语短文
6. 验证文章
7. 渲染最终 Obsidian Markdown
8. 可选生成配套试卷
9. 写入 manifest.json

注意：
文章只负责生成一篇。
图片、音频等后续功能保持独立，不影响文章落盘。
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

    # ------------------------------------------------------------------
    # 这里是本次非常重要的修改：
    #
    # 把 length 传给 render()
    #
    # 这样最终抬头才能准确显示：
    #
    # 约80词
    # 约100词
    # 约120词
    # 约150词
    # ...
    # ------------------------------------------------------------------

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

        print()
        print(
            "============================================================"
        )

        print(
            "EXAM GENERATION"
        )

        print(
            "============================================================"
        )

        exam = gen_exam(
            art,
            difficulty,
            article_type,
            words,
        )

        exam_dir = (
            output_dir
            / "配套试卷"
        )

        exam_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

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

        exam_file.write_text(
            exam_markdown,
            encoding="utf-8",
        )

        print(
            f"✓ 配套试卷已保存：{exam_file}"
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
