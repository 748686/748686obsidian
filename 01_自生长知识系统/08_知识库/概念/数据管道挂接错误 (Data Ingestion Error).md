---
type: 概念
name: 数据管道挂接错误 (Data Ingestion Error)
status: active
importance: 2
confidence: 0.9
created_at: 2026-09-13
last_updated: 2026-09-13
---

# 数据管道挂接错误 (Data Ingestion Error)

## 核心定义

指自动化新闻摄入系统中，事件元数据（如标题、分类）与挂载的来源文章实体之间发生主题性或ID映射错误的故障模式。该错误会导致事实核查失败和知识库污染。

## 新增事实

- EVT-20260913-000277 是一个典型的挂接错误样本：事件声称是哈萨克斯坦vs白俄罗斯网球赛，但来源Article #334实为德国AfD政党抗议活动。
- 此类错误通常源于爬虫或RSS解析阶段的ID映射失败，或Google News等聚合链接未正确解析到对应条目。
- 当来源内容标记为 'partial' 且主题与事件完全背离时，应判定为 'invalid_source_mismatch' 并隔离。

## 与其他知识的关系

- [[748686 自生长知识系统]]

## 来源事件

- EVT-20260913-000277

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000277
- 本次动作：CREATE
