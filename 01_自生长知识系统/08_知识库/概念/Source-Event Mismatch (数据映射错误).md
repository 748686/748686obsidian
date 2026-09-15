---
type: 概念
name: Source-Event Mismatch (数据映射错误)
status: active
importance: 3
confidence: 0.9
created_at: 2026-09-13
last_updated: 2026-09-13
---

# Source-Event Mismatch (数据映射错误)

## 核心定义

知识系统中的一种数据质量缺陷，表现为事件元数据（标题/主题）与挂载的来源文章内容完全无关。在EVT-20260913-000211中表现为足球赛事件挂载了科技商业新闻。日报显示此问题在Batch 3-43中占比高达80-90%，是系统性运维风险。

## 新增事实

- EVT-20260913-000211是Source-Event Mismatch的具体案例，足球事件挂载OpenAI新闻。
- 该错误导致事件无法进行有效的事实核查和交叉验证。
- 日报指出Batch 3至Batch 43中约80-90%的事件存在此类映射错误。

## 与其他知识的关系

- [[748686自生长知识系统]]
- [[Global Merge]]

## 来源事件

- EVT-20260913-000211

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000211
- 本次动作：CREATE
