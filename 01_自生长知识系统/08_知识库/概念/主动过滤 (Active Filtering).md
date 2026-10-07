---
type: 概念
name: 主动过滤 (Active Filtering)
status: active
importance: 2
confidence: 0.9
created_at: 2026-10-07
last_updated: 2026-10-07
---

# 主动过滤 (Active Filtering)

## 核心定义

在事件分析引擎中，严格筛选输入信息，只保留高度相关且质量可信的数据，拒绝无关噪声的处理策略。相比被动合并，能显著降低AI幻觉风险，适用于事实核查等高精度场景。

## 新增事实

- 主动过滤策略要求检查来源的source_status和content_status，标记为unresolved或内容缺失的来源应被排除。
- 主动过滤通过前置语义围栏，在深度推理前剔除明显不相关的噪音数据。

## 与其他知识的关系

- 暂无

## 来源事件

- EVT-20261007-000604

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-07

- 来源事件：EVT-20261007-000604
- 本次动作：CREATE
