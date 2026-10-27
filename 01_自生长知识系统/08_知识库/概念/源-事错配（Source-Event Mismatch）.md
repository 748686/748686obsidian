---
type: 概念
name: 源-事错配（Source-Event Mismatch）
status: active
importance: 3
confidence: 0.9
created_at: 2026-10-26
last_updated: 2026-10-26
---

# 源-事错配（Source-Event Mismatch）

## 核心定义

指自动化新闻聚合系统中，事件分类标签与实际关联的新闻文章内容严重不符的现象。本事件展示了该现象如何导致分析结论崩塌，并揭示了低质量源（缺失URL、含事实错误的摘要）被错误关联的风险。

## 新增事实

- 事件EVT-20261026-000200在英文分析中被归类为巴西总统大选，但唯一关联源Article #377实际报道的是保加利亚大选。
- 事件EVT-20261026-000200在中文分析中被归类为布拉格媒体改革抗议，但唯一关联源ARTICLE #320实际报道的是伊朗革命卫队攻击伊拉克库尔德立场。
- 关联源Article #377存在事实错误，将保加利亚现任总统标记为“Jotowa”，与已知事实（Rumen Radev）冲突。
- 两个语言维度的分析均显示关联源状态为unresolved/horizon_summary_only，缺乏原始URL和正文。

## 与其他知识的关系

- [[748686自生长知识系统]]
- [[Article #377]]
- [[ARTICLE #320]]

## 来源事件

- EVT-20261026-000200

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-26

- 来源事件：EVT-20261026-000200
- 本次动作：CREATE
