---
type: 概念
name: 来源-事件映射错误 (Source-Event Mismatch)
status: active
importance: 4
confidence: 0.9
created_at: 2026-09-13
last_updated: 2026-09-13
---

# 来源-事件映射错误 (Source-Event Mismatch)

## 核心定义

自动化知识系统中，事件标题与挂载源文章内容语义完全脱节的数据管道故障模式。本事件为典型负样本：电影奖项事件关联了德语礼仪文章。

## 新增事实

- EVT-20260913-000568 展示了标题（电影奖项）与来源内容（德语非正式称呼礼仪）完全正交的案例
- 此类错误在 Batch 3 至 Batch 43 中大量存在，被识别为最高优先级运维风险
- 来源状态通常为 unresolved, horizon_summary_only, 或 partial

## 与其他知识的关系

- [[748686 自生长知识系统]]
- [[数据治理]]

## 来源事件

- EVT-20260913-000568

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000568
- 本次动作：CREATE
