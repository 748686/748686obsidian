---
type: 概念
name: 数据管道来源错配 (Data Mapping Error)
status: active
importance: 3
confidence: 0.9
created_at: 2026-09-13
last_updated: 2026-09-13
---

# 数据管道来源错配 (Data Mapping Error)

## 核心定义

在2026-09-13的系统运行中，约80-90%的事件出现了来源内容与事件标签严重不匹配的情况（如体育事件关联政治新闻）。这是系统当前最大的运维风险，可能导致知识库被大量未验证的“幽灵事件”污染。

## 新增事实

- 2026-09-13 Batch 3至Batch 43中绝大多数事件存在来源-事件映射错误
- 错误表现包括标题与文章无关、来源状态为unresolved或horizon_summary_only
- 此问题导致日报中有效新闻占比极低，无法进行事实核查

## 与其他知识的关系

- [[748686 自生长知识系统]]
- [[Event Router]]
- [[Global Merge 算法]]

## 来源事件

- EVT-20260913-000189

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000189
- 本次动作：CREATE
