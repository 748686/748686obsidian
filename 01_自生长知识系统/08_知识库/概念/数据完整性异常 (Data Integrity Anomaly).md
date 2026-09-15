---
type: 概念
name: 数据完整性异常 (Data Integrity Anomaly)
status: active
importance: 2
confidence: 0.8
created_at: 2026-09-14
last_updated: 2026-09-14
---

# 数据完整性异常 (Data Integrity Anomaly)

## 核心定义

指事件元数据与来源内容主题严重不匹配，且来源可靠性不足（如仅存摘要无原文），导致无法进行有效知识生成的系统状态。

## 新增事实

- EVT-20260914-000195 被标记为无效数据包，因 Event Title (Fingal's Cave) 与 Source Article (Irish Whiskey Tariffs) 主题脱节。
- 该事件来源 #230 状态为 'unresolved' 和 'horizon_summary_only'，表明系统未能找到可信原始链接。

## 与其他知识的关系

- [[EVT-20260914-000195]]

## 来源事件

- EVT-20260914-000195

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-14

- 来源事件：EVT-20260914-000195
- 本次动作：CREATE
