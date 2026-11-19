---
type: 概念
name: Data_Mismatch_Pattern
status: active
importance: 2
confidence: 0.9
created_at: 2026-11-19
last_updated: 2026-11-19
---

# Data_Mismatch_Pattern

## 核心定义

在自动化新闻聚合系统中，元数据（标题/事件摘要）与正文信源不匹配的已知模式。本事件是该模式的典型案例，提示需建立交叉验证机制。

## 新增事实

- EVT-20261119-000186 的元数据声称美国防长赫格塞斯宣称捕获委内瑞拉总统马杜罗。
- EVT-20261119-000186 的唯一信源 Article #230 实际内容为英国制裁以色列官员导致约旦河西岸建合同延期。
- Article #230 中零出现 Hegseth、Maduro、Venezuela、US Military、Capture 等关键词。

## 与其他知识的关系

- [[Pete Hegseth]]
- [[Nicolás Maduro]]
- [[Article #230]]

## 来源事件

- EVT-20261119-000186

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-11-19

- 来源事件：EVT-20261119-000186
- 本次动作：CREATE
