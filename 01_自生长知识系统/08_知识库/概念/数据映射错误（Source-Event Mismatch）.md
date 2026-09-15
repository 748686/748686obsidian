---
type: 概念
name: 数据映射错误（Source-Event Mismatch）
status: active
importance: 3
confidence: 0.9
created_at: 2026-09-13
last_updated: 2026-09-13
---

# 数据映射错误（Source-Event Mismatch）

## 核心定义

在748686知识系统中，事件标题与挂载的源文章内容主题完全不一致，导致无法构建有效事实网络。此案例作为系统数据质量问题的典型示例被记录。

## 新增事实

- 事件EVT-20260913-000513的标题‘英国地基沉降索赔激增’与源文章ARTICLE #223‘朝鲜在三国演习结束一天后发射多枚导弹’主题无关。
- 由于源文章正文缺失且主题错配，关于‘英国地基沉降’的事实被标记为Unverified（未证实）。

## 与其他知识的关系

- [[ARTICLE #223]]
- [[EVT-20260913-000513]]

## 来源事件

- EVT-20260913-000513

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-13

- 来源事件：EVT-20260913-000513
- 本次动作：CREATE
