---
type: 概念
name: 数据管道来源映射错误 (Source-Event Mismatch)
status: active
importance: 3
confidence: 0.95
created_at: 2026-09-13
last_updated: 2026-09-13
---

# 数据管道来源映射错误 (Source-Event Mismatch)

## 核心定义

748686系统当前存在系统性故障，导致大量事件节点挂载了不相关的新闻源（如将国际政治新闻关联至宠物/文化事件），造成'幽灵事件'污染知识库。

## 新增事实

- 在Batch 3至Batch 43中，约80-90%的事件存在严重的来源与事件映射错误。
- 具体表现包括事件标题与挂载文章内容完全无关（如'熊猫宝宝'关联'BRICS声明'）。
- 来源状态普遍为unresolved, horizon_summary_only, partial，缺乏原文URL和正文。

## 与其他知识的关系

- [[748686 自生长知识系统]]
- [[Router/Global Merge 算法]]

## 来源事件

- EVT-20260913-000354

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000354
- 本次动作：CREATE
