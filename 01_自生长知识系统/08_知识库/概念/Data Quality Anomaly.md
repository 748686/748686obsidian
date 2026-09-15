---
type: 概念
name: Data Quality Anomaly
status: active
importance: 4
confidence: 0.9
created_at: 2026-09-13
last_updated: 2026-09-13
---

# Data Quality Anomaly

## 核心定义

指知识系统在处理新闻事件时出现的来源与主题不匹配、正文缺失或状态未解决等系统性数据质量问题，导致事实无法核查。

## 新增事实

- 在 EVT-20260913-000528 中，事件标题指向网球体育领域，但唯一关联信源 ARTICLE #238 内容为法国参议院选举政治分析，属于严重的信源错位。
- 该信源状态标记为 source_status: unresolved 且 content_status: horizon_summary_only，表明缺乏原始可信文本。
- 此类异常被归类为数据管道系统性故障的表现之一，伴随高比例的 Source-Event Mismatch。

## 与其他知识的关系

- [[748686 自生长知识系统]]

## 来源事件

- EVT-20260913-000528

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000528
- 本次动作：CREATE
