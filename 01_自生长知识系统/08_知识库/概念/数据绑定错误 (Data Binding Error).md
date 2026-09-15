---
type: 概念
name: 数据绑定错误 (Data Binding Error)
status: active
importance: 3
confidence: 0.9
created_at: 2026-09-12
last_updated: 2026-09-12
---

# 数据绑定错误 (Data Binding Error)

## 核心定义

在自生长知识系统中，当源材料与事件主题不匹配或数据不完整时，会导致分析失败和知识入库拦截的故障现象。

## 新增事实

- 事件 EVT-20260912-000756 中，Article #421 (关于学校食堂健康) 被错误绑定到 Pomeranie 交通事故事件。
- 系统状态标记为 horizon_summary_only 和 unresolved，表明缺乏可信原文。
- 由于单一源限制和主题错位，该事件被标记为 Data_Error_Bound，禁止进入知识库正式层。

## 与其他知识的关系

- [[EVT-20260912-000756]]
- [[Article #421]]
- [[748686 自生长知识系统]]

## 来源事件

- EVT-20260912-000756

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-12

- 来源事件：EVT-20260912-000756
- 本次动作：CREATE
