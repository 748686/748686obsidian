---
type: 概念
name: 匹配失效 (Matching Failure)
status: active
importance: 3
confidence: 0.8
created_at: 2026-09-14
last_updated: 2026-09-14
---

# 匹配失效 (Matching Failure)

## 核心定义

指在自生长知识系统中，检索阶段将不相关的源文档错误关联到目标事件或主题的现象，通常由语义相似度阈值过低或向量空间歧义引起。

## 新增事实

- 匹配失效通常发生在 Global Merge 层
- 匹配失效会导致合成过程产生无效知识或空结果
- 匹配失效与内容缺失不同，匹配失效意味着主题标签冲突，而内容缺失意味着标签一致但正文不全

## 与其他知识的关系

- [[内容缺失 (Content Absence)]]
- [[语义检索]]

## 来源事件

- EVT-20260914-000405

## 来源文件

- Task 4 Event Analysis

## 更新记录

### 2026-09-14

- 来源事件：EVT-20260914-000405
- 本次动作：CREATE
