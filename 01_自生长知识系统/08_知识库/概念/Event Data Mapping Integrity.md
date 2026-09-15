---
type: 概念
name: Event Data Mapping Integrity
status: active
importance: 3
confidence: 0.9
created_at: 2026-09-12
last_updated: 2026-09-12
---

# Event Data Mapping Integrity

## 核心定义

事件-文章映射一致性是知识库有效性的前置条件，语义不匹配（如体育人物vs政治人事）会导致知识构建失败。

## 新增事实

- EVT-20260912-000244因标题（Mbappé）与来源（Merz/Stumpp）语义互斥被标记为无效状态
- 单一未解析来源（horizon_summary_only）无法支持跨源验证
- 数据管道需在第一层Global Merge阶段增加语义相似度校验以防止实体错误合并

## 与其他知识的关系

- [[748686 Knowledge System]]
- [[EVT-20260912-000244]]

## 来源事件

- EVT-20260912-000244

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-12

- 来源事件：EVT-20260912-000244
- 本次动作：CREATE
