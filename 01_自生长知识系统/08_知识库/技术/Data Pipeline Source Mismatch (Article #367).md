---
type: 技术
name: Data Pipeline Source Mismatch (Article #367)
status: active
importance: 2
confidence: 0.95
created_at: 2026-10-24
last_updated: 2026-10-24
---

# Data Pipeline Source Mismatch (Article #367)

## 核心定义

发现一例数据管道错误：Article #367 被错误关联至ECB货币政策事件，其实际内容应为德国足球乙级联赛（沃尔夫斯堡）相关的体育新闻，且原文状态为未解决。

## 新增事实

- Article #367 的标题为 '2. Liga: Wolfsburg lässt Punkte liegen, Kohfeldt unter Druck'（德乙：沃尔夫斯堡丢分，科费尔被施压）。
- Article #367 的内容状态为 'horizon_summary_only'，源状态为 'unresolved'。
- Article #367 与 ECB Interest Rate Decision 事件存在元数据层面的严重错配。

## 与其他知识的关系

- [[Wolfsburg]]
- [[Niko Kohfeldt]]

## 来源事件

- EVT-20261024-000273

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-24

- 来源事件：EVT-20261024-000273
- 本次动作：CREATE
