---
type: 概念
name: 数据管道源-事件映射错误（Source-Event Mismatch）
status: active
importance: 2
confidence: 0.9
created_at: 2026-09-12
last_updated: 2026-09-12
---

# 数据管道源-事件映射错误（Source-Event Mismatch）

## 核心定义

一种自生长知识系统的数据完整性故障模式，表现为事件元数据主题与关联来源内容严重脱节（如地质符号事件关联金融新闻），导致无法构建有效事实，需通过完整性审查拦截。

## 新增事实

- EVT-20260912-000340 展示了该故障模式：标题指向纳斯卡线条，但唯一来源 ARTICLE #432 内容为美国学生贷款支付问题。
- 当来源状态为 unresolved 且仅含摘要（horizon_summary_only）时，跨源验证失败，事件被标记为异常样本而非有效知识。

## 与其他知识的关系

- [[748686自生长知识系统]]
- [[ARTICLE #432]]

## 来源事件

- EVT-20260912-000340

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-12

- 来源事件：EVT-20260912-000340
- 本次动作：CREATE
