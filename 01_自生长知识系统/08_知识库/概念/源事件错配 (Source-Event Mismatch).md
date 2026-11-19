---
type: 概念
name: 源事件错配 (Source-Event Mismatch)
status: active
importance: 2
confidence: 0.9
created_at: 2026-10-23
last_updated: 2026-10-23
---

# 源事件错配 (Source-Event Mismatch)

## 核心定义

指自动化新闻聚合系统中，源文章内容与分配的事件主题完全不符的数据质量故障模式。本案例中英国零售主题被错误关联至中国政治和历史纪念新闻。

## 新增事实

- EVT-20261023-000072 是已记录的源事件错配案例，预期主题为英国零售，实际内容为梁振英活动和长征纪念邮票。

## 与其他知识的关系

- [[Global Merge Engine]]
- [[Data Quality Audit]]

## 来源事件

- EVT-20261023-000072

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-23

- 来源事件：EVT-20261023-000072
- 本次动作：CREATE


---

## 知识更新 · 2026-11-19

- 来源事件：EVT-20261119-000134
- 置信度：0.95
- 重要性：2

### 本次变化

系统在数据入库过程中出现的一次性技术故障，导致新闻源内容与事件主题完全无关。这反映了多层合并推理（First-layer merge reasoning）中对来源有效性验证的缺失。

### 新增事实

- 系统在处理 EVT-20261119-000134 时，将关于 GTA VI 巨脚怪目击的文章关联到了研究生融资主题的事件上。
- 该事件经历了 'First-layer merge reasoning' 流程但最终未能通过 fetched article 验证。

### 相关知识

- [[EVT-20261119-000134]]
- [[Article #168]]
