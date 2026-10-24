---
type: 概念
name: Source-Event Mismatch Data Quality Issue
status: active
importance: 3
confidence: 0.95
created_at: 2026-10-23
last_updated: 2026-10-23
---

# Source-Event Mismatch Data Quality Issue

## 核心定义

在自动化知识采集管道中，高频出现源文章与目标事件主题无关（如移民政策文章关联王室新闻）且正文内容缺失（partial）的系统性质量问题。

## 新增事实

- 数据管道存在元数据映射错误，导致不相关的新闻文章被错误关联至特定事件。
- 部分抓取的源文章内容不完整（status: partial），正文缺失，仅保留描述性元数据。
- 此类错误可能导致基于未经验证来源的事件实体创建产生虚假知识。

## 与其他知识的关系

- [[ARTICLE #256]]
- [[Graham Norton Show]]
- [[William, Prince of Wales]]

## 来源事件

- EVT-20261023-000517

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-10-23

- 来源事件：EVT-20261023-000517
- 本次动作：CREATE
