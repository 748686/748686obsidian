# 02_英语学习系统

一个基于 GitHub Actions + Python + Agnes.ai 的英语学习自动化系统初始版。

## 工作流

`input/YYYY-MM-DD.md` → 解析词汇/图片 → AI 生成短文 → 校验 → 固定两栏注记 → 可选试卷 → 可选图片 → 可选听力 → `output/YYYY-MM-DD/`

## 使用

1. 在 `input/` 放当天词汇文件。
2. GitHub Actions 手动运行 `02_英语学习系统`。
3. 设置 `AGNES_API_KEY`；启用图片/视觉/听力时设置 `OPENAI_API_KEY`。
4. 选择日期、难度、文体、长度以及试卷/图片/音频选项。

本版本是完整可运行骨架；API 的模型与多媒体接口集中在 `config/settings.json`，后续可以按你提供的具体接口要求调整。
