---
type: 概念
name: 数据源-事件映射错误 (Source-Event Mismatch)
status: active
importance: 3
confidence: 0.95
created_at: 2026-09-12
last_updated: 2026-09-12
---

# 数据源-事件映射错误 (Source-Event Mismatch)

## 核心定义

748686系统数据管道中出现的系统性故障模式，表现为将足球等特定事件ID错误绑定至无关的新闻列表（如啤酒节、胡塞民兵相关条目）。该模式导致有效信息密度降低，需通过多批次交叉验证及高置信度锚点策略进行拦截。

## 新增事实

- ARTICLE #313 被识别为典型的 Source-Event Mismatch 案例，其中事件标题涉及兰斯足球，但来源内容涉及 Wiesn-Kartell 和 Huthi-Miliz 等无关主题。
- 748686系统 2026-09-12 日报显示约 80% 的原始 Batch 数据存在源-事件映射错误，系统采取了‘宁缺毋滥’原则拦截此类低置信度信息入库。

## 与其他知识的关系

- [[748686 自生长知识系统]]
- [[ARTICLE #313]]
- [[EVT-20260912-000657]]

## 来源事件

- EVT-20260912-000657

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-12

- 来源事件：EVT-20260912-000657
- 本次动作：CREATE
