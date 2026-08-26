# 01_自生长知识系统

> 本目录属于 GitHub 私有仓库 `748686obsidian`，不会把系统文件散落到仓库根目录。

## 运行链路

GitHub Actions → Horizon → 全球 RSS → 去重/评分/摘要 → 27 Skills → 日报/周报 → 知识库 → Obsidian → 飞书

## 第一次配置

1. 把你已有的 27 个 Skill `.md` 文件放入 `Skills/` 对应分类目录。
2. 打开 `00_System/rss_sources.json`，把你之前整理好的全球 RSS 地址填进去。
3. GitHub 仓库 `Settings → Secrets and variables → Actions → New repository secret` 添加：
   - `AI_API_KEY`
   - `AI_BASE_URL`
   - `AI_MODEL`
   - `FEISHU_WEBHOOK`（暂时没有飞书可不加）
4. 打开 `Actions` → `01 自生长知识系统 - 每日运行` → `Run workflow` 手动测试。
5. 测试成功后，GitHub Actions 会按 workflow 中的 cron 自动运行。

## API 配置例子

如果使用 OpenAI-compatible API：

- `AI_BASE_URL`: 例如 `https://api.openai.com/v1`
- `AI_MODEL`: 你实际可调用的模型名
- `AI_API_KEY`: 你的 API Key

如果使用其他兼容 OpenAI API 的中转服务，只需要把 `AI_BASE_URL` 和 `AI_MODEL` 改成对应值。

## 安全

API Key 只放 GitHub Actions Secrets，不写进仓库文件。
