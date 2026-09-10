#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
主程序 V2.3

======================================================================
核心流程
======================================================================

整个系统严格采用：

    三阶段
    +
    每阶段独立落盘
    +
    每阶段独立 Git commit
    +
    每阶段独立 Git push

======================================================================
第一阶段
======================================================================

生成英语短文
    ↓
验证文章
    ↓
渲染 Markdown
    ↓
立即落盘
    ↓
确认文件存在
    ↓
Git add
    ↓
Git commit
    ↓
Git push
    ↓
文章安全进入 GitHub
    ↓
才允许进入第二阶段

======================================================================
第二阶段
======================================================================

生成配套试卷
    ↓
渲染试卷
    ↓
立即落盘
    ↓
确认文件存在
    ↓
Git add
    ↓
Git commit
    ↓
Git push
    ↓
试卷安全进入 GitHub
    ↓
才允许进入第三阶段

======================================================================
第三阶段
======================================================================

生成答案解析
    ↓
渲染答案解析
    ↓
立即落盘
    ↓
确认文件存在
    ↓
Git add
    ↓
Git commit
    ↓
Git push

======================================================================
Manifest
======================================================================

所有业务阶段完成后：

    生成 manifest.json
    ↓
    落盘
    ↓
    Git add
    ↓
    Git commit
    ↓
    Git push

======================================================================
重要原则
======================================================================

文章、试卷、答案解析完全独立。

例如：

    文章        ✅
    试卷        ❌
    答案解析    不执行

则：

    文章已经存在 GitHub
    试卷不存在
    答案解析不会执行

绝不会因为后续阶段失败而丢失前面已经成功的阶段。

======================================================================
目录结构
======================================================================

output/{date}/
│
├── 英语短文注记/
│   └── {difficulty}星_{article_type}.md
│
├── 配套试卷/
│   ├── {difficulty}星_{article_type}_试卷.md
│   └── {difficulty}星_{article_type}_答案解析.md
│
└── manifest.json

======================================================================
Git 保存原则
======================================================================

每一个成功阶段都立即：

    git add
    git commit
    git push

不会等整个程序结束后才统一 push。

这样可以保证：

    后续阶段失败
        ↓
    前面阶段已经进入 GitHub
        ↓
    前面内容不会丢失
"""

import argparse
import json
import subprocess
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
# Git 工具
# ======================================================================

def run_git(
    args: list[str],
    label: str,
):
    """
    执行 Git 命令。

    任何 Git 命令失败都会直接抛出异常。

    这样可以防止程序以为已经保存，
    实际上 GitHub 并没有收到文件。
    """

    print()
    print(
        f"▶ Git：{label}"
    )

    print(
        "  git "
        + " ".join(args)
    )

    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if result.stdout.strip():

        print(
            result.stdout.strip()
        )

    if result.returncode != 0:

        if result.stderr.strip():

            print(
                result.stderr.strip()
            )

        raise RuntimeError(
            f"Git 操作失败：{label}"
        )

    return result


# ======================================================================
# Git 用户身份初始化
# ======================================================================

def ensure_git_identity():
    """
    确保 GitHub Actions Runner 有 Git 提交身份。

    GitHub Actions 中 checkout 通常已经具备 Git，
    但提交身份不一定存在。

    因此这里显式设置。
    """

    print()
    print(
        "============================================================"
    )

    print(
        "GIT INITIALIZATION"
    )

    print(
        "============================================================"
    )

    # ------------------------------------------------------------------
    # 检查当前是否已经存在 user.name
    # ------------------------------------------------------------------

    name_result = subprocess.run(
        [
            "git",
            "config",
            "user.name",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if name_result.returncode != 0 or not name_result.stdout.strip():

        run_git(
            [
                "config",
                "user.name",
                "github-actions[bot]",
            ],
            "设置 Git 用户名",
        )

    else:

        print(
            f"✓ Git 用户名：{name_result.stdout.strip()}"
        )

    # ------------------------------------------------------------------
    # 检查当前是否已经存在 user.email
    # ------------------------------------------------------------------

    email_result = subprocess.run(
        [
            "git",
            "config",
            "user.email",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if email_result.returncode != 0 or not email_result.stdout.strip():

        run_git(
            [
                "config",
                "user.email",
                "41898282+github-actions[bot]@users.noreply.github.com",
            ],
            "设置 Git 邮箱",
        )

    else:

        print(
            f"✓ Git 邮箱：{email_result.stdout.strip()}"
        )


# ======================================================================
# Git 阶段提交
# ======================================================================

def git_save_stage(
    paths: list[Path],
    message: str,
    label: str,
):
    """
    将指定阶段产生的文件立即提交并推送到 GitHub。

    参数：

        paths：
            本阶段新增 / 修改的文件

        message：
            Git commit message

        label：
            日志显示名称
    """

    print()
    print(
        "============================================================"
    )

    print(
        f"GIT SAVE / {label}"
    )

    print(
        "============================================================"
    )

    # ------------------------------------------------------------------
    # 确认所有文件存在
    # ------------------------------------------------------------------

    for path in paths:

        if not path.exists():

            raise RuntimeError(
                f"准备 Git 保存时发现文件不存在：{path}"
            )

        if path.stat().st_size <= 0:

            raise RuntimeError(
                f"准备 Git 保存时发现空文件：{path}"
            )

        print(
            f"✓ 待保存：{path}"
        )

    # ------------------------------------------------------------------
    # git add
    # ------------------------------------------------------------------

    relative_paths = []

    for path in paths:

        try:

            relative = path.relative_to(ROOT)

        except ValueError:

            raise RuntimeError(
                f"文件不属于 Git 根目录：{path}"
            )

        relative_paths.append(
            str(relative)
        )

    run_git(
        [
            "add",
            "--",
            *relative_paths,
        ],
        "git add",
    )

    # ------------------------------------------------------------------
    # 检查 staged 内容
    # ------------------------------------------------------------------

    staged = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--name-only",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if staged.returncode != 0:

        raise RuntimeError(
            "无法检查 Git staged 文件"
        )

    if not staged.stdout.strip():

        print(
            "ℹ 本阶段没有新的 Git 变更。"
        )

        return

    print()
    print(
        "✓ Git staged 文件："
    )

    print(
        staged.stdout.strip()
    )

    # ------------------------------------------------------------------
    # git commit
    # ------------------------------------------------------------------

    run_git(
        [
            "commit",
            "-m",
            message,
        ],
        "git commit",
    )

    # ------------------------------------------------------------------
    # git push
    # ------------------------------------------------------------------

    run_git(
        [
            "push",
        ],
        "git push",
    )

    print()
    print(
        f"✓ {label}已经成功保存到 GitHub"
    )


# ======================================================================
# 文件写入 + 文件确认
# ======================================================================

def write_and_confirm(
    file_path: Path,
    content: str,
    label: str,
):
    """
    写入文件，并立即确认文件确实存在。

    只有确认成功，函数才返回。
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    if not file_path.exists():

        raise RuntimeError(
            f"{label}已经执行写入，但文件确认不存在："
            f"{file_path}"
        )

    if file_path.stat().st_size <= 0:

        raise RuntimeError(
            f"{label}文件存在，但是文件大小为 0："
            f"{file_path}"
        )

    print()
    print(
        f"✓ {label}已落盘："
    )

    print(
        f"  {file_path}"
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
        "02_英语学习系统 V2.3"
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
    # Git 初始化
    # ==================================================================

    ensure_git_identity()

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
    # OCR / Vision
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

    # ##################################################################
    #
    # 第一阶段
    #
    # ARTICLE
    #
    # ##################################################################

    print()
    print(
        "============================================================"
    )

    print(
        "STAGE 1 / 3"
    )

    print(
        "ARTICLE GENERATION"
    )

    print(
        "============================================================"
    )

    print(
        "现在只生成英语短文。"
    )

    print(
        "试卷和答案解析不会在本阶段生成。"
    )

    # ------------------------------------------------------------------
    # Agnes 生成文章
    # ------------------------------------------------------------------

    art = gen_article(
        words,
        difficulty,
        article_type,
        length,
    )

    print()
    print(
        f"文章标题：{art.get('title', '')}"
    )

    # ------------------------------------------------------------------
    # 文章验证
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # 渲染文章
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # 第一阶段独立落盘
    # ------------------------------------------------------------------

    write_and_confirm(
        note_file,
        note,
        "英语短文注记",
    )

    # ------------------------------------------------------------------
    # 第一阶段立即 Git 保存
    # ------------------------------------------------------------------

    git_save_stage(
        [note_file],
        (
            f"02英语学习系统："
            f"{date} "
            f"{difficulty}星 "
            f"{article_type_name} "
            f"英语短文"
        ),
        "第一阶段文章",
    )

    print()
    print(
        "✓ 第一阶段完成"
    )

    print(
        "✓ 文章已经独立落盘"
    )

    print(
        "✓ 文章已经独立提交到 GitHub"
    )

    print(
        "✓ 现在才允许进入试卷阶段"
    )

    # ##################################################################
    #
    # 第二阶段
    #
    # EXAM PAPER
    #
    # ##################################################################

    exam_file = None
    answer_file = None

    if args.exam == "yes":

        exam_dir = (
            output_dir
            / "配套试卷"
        )

        exam_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        print()
        print(
            "============================================================"
        )

        print(
            "STAGE 2 / 3"
        )

        print(
            "EXAM PAPER GENERATION"
        )

        print(
            "============================================================"
        )

        print(
            "文章已经成功保存到 GitHub。"
        )

        print(
            "现在开始独立生成考生试卷。"
        )

        print(
            "答案解析不会在本阶段生成。"
        )

        # ------------------------------------------------------------------
        # 生成试卷
        # ------------------------------------------------------------------

        exam = gen_exam(
            art,
            difficulty,
            article_type,
            words,
        )

        # ------------------------------------------------------------------
        # 渲染试卷
        # ------------------------------------------------------------------

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

        # ------------------------------------------------------------------
        # 第二阶段独立落盘
        # ------------------------------------------------------------------

        write_and_confirm(
            exam_file,
            exam_markdown,
            "配套试卷",
        )

        # ------------------------------------------------------------------
        # 第二阶段立即 Git 保存
        # ------------------------------------------------------------------

        git_save_stage(
            [exam_file],
            (
                f"02英语学习系统："
                f"{date} "
                f"{difficulty}星 "
                f"{article_type_name} "
                f"配套试卷"
            ),
            "第二阶段试卷",
        )

        print()
        print(
            "✓ 第二阶段完成"
        )

        print(
            "✓ 试卷已经独立落盘"
        )

        print(
            "✓ 试卷已经独立提交到 GitHub"
        )

        print(
            "✓ 现在才允许进入答案解析阶段"
        )

        # ##################################################################
        #
        # 第三阶段
        #
        # ANSWERS / ANALYSIS
        #
        # ##################################################################

        print()
        print(
            "============================================================"
        )

        print(
            "STAGE 3 / 3"
        )

        print(
            "EXAM ANSWERS / ANALYSIS GENERATION"
        )

        print(
            "============================================================"
        )

        print(
            "文章：已保存"
        )

        print(
            "试卷：已保存"
        )

        print(
            "现在开始独立生成答案解析。"
        )

        print(
            "本阶段失败不会影响前面的文章和试卷。"
        )

        print()

        print(
            "将生成："
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

        # ------------------------------------------------------------------
        # 生成答案 / 解析
        # ------------------------------------------------------------------

        answer_result = gen_answers(
            exam,
            art,
            difficulty,
            article_type,
            words,
        )

        # ------------------------------------------------------------------
        # 渲染答案解析
        # ------------------------------------------------------------------

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

        # ------------------------------------------------------------------
        # 第三阶段独立落盘
        # ------------------------------------------------------------------

        write_and_confirm(
            answer_file,
            answer_markdown,
            "答案解析",
        )

        # ------------------------------------------------------------------
        # 第三阶段立即 Git 保存
        # ------------------------------------------------------------------

        git_save_stage(
            [answer_file],
            (
                f"02英语学习系统："
                f"{date} "
                f"{difficulty}星 "
                f"{article_type_name} "
                f"答案解析"
            ),
            "第三阶段答案解析",
        )

        print()
        print(
            "✓ 第三阶段完成"
        )

        print(
            "✓ 答案解析已经独立落盘"
        )

        print(
            "✓ 答案解析已经独立提交到 GitHub"
        )

        # ------------------------------------------------------------------
        # 三阶段完成
        # ------------------------------------------------------------------

        print()
        print(
            "============================================================"
        )

        print(
            "ALL THREE STAGES COMPLETE"
        )

        print(
            "============================================================"
        )

        print(
            f"✓ 文章：{note_file}"
        )

        print(
            f"✓ 试卷：{exam_file}"
        )

        print(
            f"✓ 答案解析：{answer_file}"
        )

    else:

        print()
        print(
            "============================================================"
        )

        print(
            "EXAM SKIPPED"
        )

        print(
            "============================================================"
        )

        print(
            "配套试卷：no"
        )

        print(
            "文章已经独立落盘。"
        )

    # ==================================================================
    # Manifest
    #
    # Manifest 永远最后生成。
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

    write_and_confirm(
        manifest_file,
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        "manifest",
    )

    # ------------------------------------------------------------------
    # Manifest 最后单独 Git 保存
    # ------------------------------------------------------------------

    git_save_stage(
        [manifest_file],
        (
            f"02英语学习系统："
            f"{date} "
            f"manifest"
        ),
        "最终 Manifest",
    )

    # ==================================================================
    # 最终完成
    # ==================================================================

    print()
    print(
        "============================================================"
    )

    print(
        "02_英语学习系统 COMPLETE"
    )

    print(
        "============================================================"
    )

    print(
        f"输出目录：{output_dir}"
    )

    print(
        "============================================================"
    )

    print(
        "✓ 文章已经保存到 GitHub"
    )

    if args.exam == "yes":

        print(
            "✓ 试卷已经保存到 GitHub"
        )

        print(
            "✓ 答案解析已经保存到 GitHub"
        )

    print(
        "✓ Manifest 已经保存到 GitHub"
    )

    print(
        "============================================================"
    )


# ======================================================================
# 程序入口
# ======================================================================

if __name__ == "__main__":

    main()
