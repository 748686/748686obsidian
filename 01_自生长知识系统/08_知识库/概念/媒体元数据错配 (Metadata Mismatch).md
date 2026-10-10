---
type: 概念
name: 媒体元数据错配 (Metadata Mismatch)
status: active
importance: 2
confidence: 0.9
created_at: 2026-10-10
last_updated: 2026-10-10
---

# 媒体元数据错配 (Metadata Mismatch)

## 核心定义

指在新闻聚合或数据库索引过程中，源文章的实际内容主题与关联的标题、摘要或标签发生语义冲突的现象。本案例中，AP关于艺术家的报道被错误索引至时政评论标题下。

## 新增事实

- EVT-20261010-000300 事件中，AP关于格哈德·里希特的报道与中文标题“求新唯实 发展重质”（时政评论）发生元数据错配。
- 当来源状态为 unresolved 或 horizon_summary_only 时，定性标签（如“最重要艺术家”）仅能作为“媒体声称”而非事实保存。

## 与其他知识的关系

- [[Gerhard Richter]]
- [[美联社]]
- [[人民日报]]

## 来源事件

- EVT-20261010-000300

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-10

- 来源事件：EVT-20261010-000300
- 本次动作：CREATE
