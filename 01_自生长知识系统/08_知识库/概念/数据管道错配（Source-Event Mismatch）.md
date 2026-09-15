---
type: 概念
name: 数据管道错配（Source-Event Mismatch）
status: active
importance: 2
confidence: 0.95
created_at: 2026-09-12
last_updated: 2026-09-12
---

# 数据管道错配（Source-Event Mismatch）

## 核心定义

描述一种系统故障模式，即检索到的源材料与目标事件主题不匹配（如德国政治标题对应美国能源新闻），且正文缺失，导致知识合成失败。

## 新增事实

- EVT-20260912-000561 中，标题指向 AfD 州议员背景，但源材料 ARTICLE #203 指向美国柴油价格与伊朗冲击。
- 该错配导致系统判定为 'Error: Data Mismatch'，并建议剔除关联以避免污染知识图谱。

## 与其他知识的关系

- [[748686 自生长知识系统]]
- [[ARTICLE #203]]

## 来源事件

- EVT-20260912-000561

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-12

- 来源事件：EVT-20260912-000561
- 本次动作：CREATE
