---
type: 概念
name: 数据摄入错配（Data Ingestion Mismatch）
status: active
importance: 2
confidence: 0.9
created_at: 2026-09-12
last_updated: 2026-09-12
---

# 数据摄入错配（Data Ingestion Mismatch）

## 核心定义

在自动知识系统中，事件ID/标题与实际源内容严重不符的技术缺陷。本案例中表现为军事/工业类事件ID关联了体育类源材料。

## 新增事实

- 事件 EVT-20260912-000618 的标题为韩华火箭炮出口，但源材料内容为法甲联赛雷恩胜马赛
- 该错误被系统识别为数据摄入错误、标签错配或源文件链接错误

## 与其他知识的关系

- [[748686 知识系统]]

## 来源事件

- EVT-20260912-000618

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-12

- 来源事件：EVT-20260912-000618
- 本次动作：CREATE
