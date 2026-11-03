---
type: 概念
name: 源数据错位（Source-Metadata Mismatch）
status: active
importance: 2
confidence: 0.95
created_at: 2026-10-31
last_updated: 2026-10-31
---

# 源数据错位（Source-Metadata Mismatch）

## 核心定义

在新闻摄入管道中，事件ID的元数据标签与捕获的有效源文本内容不一致的现象。例如本事件标记为'UK weather forecast'但内容为俄罗斯媒体审查报道。

## 新增事实

- EVT-20261031-000468 记录了一次典型的元数据与内容错位，名义主题为英国天气预报，实际源文本为美联社关于俄罗斯报纸关闭的报道。

## 与其他知识的关系

- 暂无

## 来源事件

- EVT-20261031-000468

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-31

- 来源事件：EVT-20261031-000468
- 本次动作：CREATE
