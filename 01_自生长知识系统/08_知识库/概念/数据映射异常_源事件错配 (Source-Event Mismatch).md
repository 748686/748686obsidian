---
type: 概念
name: 数据映射异常/源事件错配 (Source-Event Mismatch)
status: active
importance: 3
confidence: 0.9
created_at: 2026-09-12
last_updated: 2026-09-12
---

# 数据映射异常/源事件错配 (Source-Event Mismatch)

## 核心定义

一种数据管道故障，指单一来源的主题与关联事件的主题存在根本性逻辑冲突（如AI资源列表对应军事动员），导致事件分析缺乏事实基础。识别此类异常是保证知识库“宁缺毋滥”的关键防御机制。

## 新增事实

- 该异常表现为来源状态为未解决（unresolved）且仅有摘要（horizon_summary_only）时，主题仍被强行关联至无关事件。
- 此类错误会导致“单源谬误”被放大，因为缺乏交叉验证，且底层证据与顶层结论断裂。
- 处理原则包括将事件标记为 Invalid_Mapping 或 Pending_Correction，禁止生成最终知识节点。

## 与其他知识的关系

- [[Article #417]]
- [[748686 自生长知识系统]]

## 来源事件

- EVT-20260912-000755

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-12

- 来源事件：EVT-20260912-000755
- 本次动作：CREATE
