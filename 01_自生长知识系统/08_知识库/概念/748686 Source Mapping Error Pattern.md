---
type: 概念
name: 748686 Source Mapping Error Pattern
status: active
importance: 2
confidence: 0.9
created_at: 2026-09-13
last_updated: 2026-09-13
---

# 748686 Source Mapping Error Pattern

## 核心定义

A recurring data quality issue in the 748686 system where Global Merge logic incorrectly associates event titles with unrelated source articles, resulting in 'ghost events' and analysis failure.

## 新增事实

- EVT-20260913-000374 is an example of a source mapping error where 'AfD and Deportation' was linked to 'Marthaler beim Lausitz Festival'.
- The source status for the linked article was marked as 'unresolved' and 'horizon_summary_only'.
- The daily report indicates that 80-90% of events in Batch 3 to 43 suffer from similar mapping errors.

## 与其他知识的关系

- [[748686 Self-Growing Knowledge System]]
- [[Global Merge Algorithm]]

## 来源事件

- EVT-20260913-000374

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000374
- 本次动作：CREATE
