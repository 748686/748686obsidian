---
type: 概念
name: 置信度评分模型 (Confidence Scoring Model)
status: active
importance: 5
confidence: 0.85
created_at: 2026-10-23
last_updated: 2026-10-23
---

# 置信度评分模型 (Confidence Scoring Model)

## 核心定义

一种用于评估Event Unit质量的机制，基于来源权威性、内容完整度、元数据一致性和多源佐证四个维度计算0-1的分数，以决定数据是否进入正式知识库。

## 新增事实

- 低于阈值的Event Unit应被转入沙盒区，不参与正式合卷生成。
- 当正文缺失但标签与标题冲突时，置信度应接近0。

## 与其他知识的关系

- [[自生长知识系统]]
- [[多源信息融合]]

## 来源事件

- EVT-20261023-000678

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-23

- 来源事件：EVT-20261023-000678
- 本次动作：CREATE
