---
type: 概念
name: 信息验证失败（Information Verification Failure）
status: active
importance: 3
confidence: 0.9
created_at: 2026-09-20
last_updated: 2026-09-20
---

# 信息验证失败（Information Verification Failure）

## 核心定义

在一个知识单元中，声明的主题与实际引用的来源内容之间缺乏逻辑一致性或事实支持，导致无法生成有效的结论或综述。这是自动化知识系统中常见的数据质量问题，需通过语义一致性校验来预防。

## 新增事实

- 当唯一来源无效时，应明确列出缺失的关键信息维度，并将单元标记为incomplete或unverified。
- 区分“无信息”和“矛盾信息”至关重要：前者需要更多搜索，后者需要仲裁逻辑。

## 与其他知识的关系

- [[数据质量]]
- [[知识图谱]]

## 来源事件

- EVT-20260920-000346

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-20

- 来源事件：EVT-20260920-000346
- 本次动作：CREATE
