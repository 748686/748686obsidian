#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V6.5.3
...
（文件头注释保持不变，略）
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time

from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from zoneinfo import ZoneInfo


# ============================================================
# PATH
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

SYSTEM = ROOT / "00_System"
SKILLS = ROOT / "Skills"
RAW_NEWS = ROOT / "Raw News"
REPORTS = ROOT / "05_日报"
WEEKLY = ROOT / "06_周报"
TOPICS = ROOT / "07_专题报告"
KNOWLEDGE = ROOT / "08_知识库"
LOGS = SYSTEM / "运行日志"

ROUTES_FILE = SYSTEM / "skill_routes.json"


# ============================================================
# CONSTANTS
# ============================================================

EVENT_UNITS_SUFFIX = "EventUnit"

EVENT_INDEX_FILE = "_event_index.json"

EVENT_UNITS_COMPLETE_FILE = "_EVENT_UNITS_COMPLETE"

SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"

GLOBAL_MERGE_CHECKPOINT_FILE = "_global_merge_checkpoint.json"

GLOBAL_CLUSTER_REGISTRY_FILE = "_global_cluster_registry.json"


AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"

AGNES_MODEL = "agnes-2.5-flash"

AGNES_API_KEY_ENV = "AGNES_API_KEY"


DEFAULT_TEMPERATURE = 0.3

AI_TIMEOUT = 180

AI_REQUEST_THROTTLE_SECONDS = 1.5

AI_MAX_429_RETRIES = 5

AI_429_BACKOFF_BASE = 10

AI_429_BACKOFF_MAX = 180

AI_429_JITTER_MAX = 3

_LAST_AI_REQUEST_TIME = 0.0


AGGREGATION_BATCH_SIZE = 30

GLOBAL_MERGE_WINDOW_SIZE = 30

GLOBAL_MERGE_OVERLAP = 15

MAX_ARTICLES_PER_EVENT_CONTEXT = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

CLUSTER_REPAIR_ATTEMPTS = 2


RECOVERY_BATCH_SIZES = (
    30,
    15,
    8,
    4,
    2,
    1,
)


BEIJING_TZ = ZoneInfo("Asia/Shanghai")


CURRENT_LANGUAGE = None

SUPPORTED_LANGUAGES = (
    "EN",
    "ZH",
)


# ============================================================
# TIME
# ============================================================

def now():
    return datetime.now(BEIJING_TZ)


# ============================================================
# PROCESSING UNIT PATH
# ============================================================

def event_units_root(date):
    return RAW_NEWS / f"{date}-EventUnit"


def language_dir(date, language=None):
    lang = language or CURRENT_LANGUAGE
    if lang not in SUPPORTED_LANGUAGES:
        raise RuntimeError(f"❌ 未设置合法语言批次：{lang}")
    return event_units_root(date) / lang


def event_units_dir(date, language=None):
    return language_dir(date, language) / "event_units"


def conflict_log_path(date, language=None):
    lang = language or CURRENT_LANGUAGE
    return LOGS / f"{date}_{lang}_event_aggregation_conflicts.log"


def global_merge_checkpoint_path(date, language=None):
    return event_units_dir(date, language) / GLOBAL_MERGE_CHECKPOINT_FILE


def global_cluster_registry_path(date, language=None):
    return event_units_dir(date, language) / GLOBAL_CLUSTER_REGISTRY_FILE


# ============================================================
# LOGGING
# ============================================================

def log_conflict(date, stage, message, details=None):
    LOGS.mkdir(parents=True, exist_ok=True)
    lines = [
        "",
        "=" * 80,
        f"TIME: {now().isoformat()}",
        f"DATE: {date}",
        f"LANGUAGE: {CURRENT_LANGUAGE}",
        f"STAGE: {stage}",
        f"MESSAGE: {message}",
    ]
    if details is not None:
        try:
            detail = details if isinstance(details, str) else json.dumps(details, ensure_ascii=False, indent=2)
        except Exception:
            detail = str(details)
        lines += ["DETAILS:", detail]
    lines += ["=" * 80, ""]
    path = conflict_log_path(date)
    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"⚠️ {message}")
    print(f" Conflict log: {path}")


# ============================================================
# JSON
# ============================================================

def read_json(path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise RuntimeError(f"❌ JSON读取失败：{path}\n{e}") from e


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_json_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        payload = json.dumps(data, ensure_ascii=False, indent=2)
        tmp.write_text(payload, encoding="utf-8")
        json.loads(tmp.read_text(encoding="utf-8"))
        with tmp.open("rb") as f:
            os.fsync(f.fileno())
        tmp.replace(path)
    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass
        raise


# ============================================================
# AI JSON
# ============================================================

def parse_ai_json(result, context):
    text = str(result).strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            candidate = text[start:end + 1]
            try:
                return json.loads(candidate)
            except Exception:
                pass
        raise RuntimeError(f"❌ AI JSON解析失败：{context}\n\n{text[:5000]}")


# ============================================================
# SAFE NAME
# ============================================================

def safe_name(text):
    text = re.sub(r'[\\/:*?"<>|]', "_", str(text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:120] or "未命名"


# ============================================================
# FRONT MATTER
# ============================================================

def parse_front_matter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    data = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data, parts[2].lstrip()


# ============================================================
# AI THROTTLE
# ============================================================

def wait_for_ai_throttle():
    global _LAST_AI_REQUEST_TIME
    elapsed = time.monotonic() - _LAST_AI_REQUEST_TIME
    remaining = AI_REQUEST_THROTTLE_SECONDS - elapsed
    if remaining > 0:
        print(f" ⏳ AI请求节流等待 {remaining:.1f}s")
        time.sleep(remaining)
    _LAST_AI_REQUEST_TIME = time.monotonic()


def parse_retry_after(headers):
    if headers is None:
        return None
    value = headers.get("Retry-After")
    if value is None:
        return None
    try:
        seconds = float(str(value).strip())
        return seconds if seconds >= 0 else None
    except ValueError:
        return None


def calculate_429_backoff(retry_number):
    base = min(AI_429_BACKOFF_BASE * (2 ** (retry_number - 1)), AI_429_BACKOFF_MAX)
    return min(base + random.uniform(0, AI_429_JITTER_MAX), AI_429_BACKOFF_MAX)


# ============================================================
# AI CALL
# ============================================================

def call_ai(prompt, system_prompt=None, temperature=DEFAULT_TEMPERATURE):
    key = os.getenv(AGNES_API_KEY_ENV, "").strip()
    if not key:
        raise RuntimeError("❌ 缺少 AGNES_API_KEY")
    if not system_prompt:
        system_prompt = "你是748686自生长知识系统的知识工程师。严格依据输入内容，不得编造事实。"
    payload = json.dumps({
        "model": AGNES_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }, ensure_ascii=False).encode()
    req = Request(
        AGNES_BASE_URL + "/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "748686-Knowledge-Pipeline/6.5.3"
        },
        method="POST"
    )
    for attempt in range(AI_MAX_429_RETRIES + 1):
        wait_for_ai_throttle()
        try:
            with urlopen(req, timeout=AI_TIMEOUT) as r:
                raw = r.read().decode("utf-8")
            try:
                data = json.loads(raw)
            except Exception as e:
                raise RuntimeError("❌ AGNES.ai 返回不是合法JSON\n" + raw[:3000]) from e
            try:
                result = data["choices"][0]["message"]["content"]
            except Exception as e:
                raise RuntimeError("❌ AGNES.ai 返回格式异常\n" + json.dumps(data, ensure_ascii=False)[:5000]) from e
            if not str(result).strip():
                raise RuntimeError("❌ AGNES.ai 返回空内容")
            return str(result).strip()
        except HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            if e.code == 429:
                if attempt >= AI_MAX_429_RETRIES:
                    print("❌ AGNES.ai HTTP 429 — 已达到最大自动重试次数")
                    raise RuntimeError("❌ AGNES.ai HTTP 429：自动重试次数耗尽") from e
                retry_number = attempt + 1
                retry_after = parse_retry_after(e.headers)
                if retry_after is not None:
                    wait_seconds = min(retry_after, AI_429_BACKOFF_MAX)
                    source = "Retry-After"
                else:
                    wait_seconds = calculate_429_backoff(retry_number)
                    source = "指数退避"
                print(f"⚠️ AGNES.ai HTTP 429 — Retry {retry_number}/{AI_MAX_429_RETRIES}, Wait {wait_seconds:.1f}s, Source={source}")
                if body:
                    print(" Response:", re.sub(r"\s+", " ", body).strip()[:1000])
                time.sleep(wait_seconds)
                continue
            raise RuntimeError(f"❌ AGNES.ai HTTP错误 {e.code}\n{body[:3000]}") from e
        except URLError as e:
            raise RuntimeError("❌ AGNES.ai 网络连接失败\n" + str(e.reason)) from e
        except TimeoutError as e:
            raise RuntimeError("❌ AGNES.ai 请求超时") from e
        except Exception as e:
            raise RuntimeError(f"❌ AGNES.ai 请求失败：{e}") from e
    raise RuntimeError("❌ AGNES.ai 请求异常结束")


# ============================================================
# SKILLS (省略，同之前)
# ============================================================

def load_skills():
    if not SKILLS.exists():
        raise RuntimeError(f"Skills目录不存在：{SKILLS}")
    out = {}
    for p in sorted(SKILLS.rglob("*.md")):
        out[p.name] = {
            "name": p.name,
            "path": str(p),
            "content": p.read_text(encoding="utf-8", errors="replace"),
        }
    return out


def load_routes():
    routes = read_json(ROUTES_FILE, {})
    if not routes:
        raise RuntimeError("skill_routes.json为空或不存在")
    return routes


# ============================================================
# ENRICHED NEWS (同之前)
# ============================================================

def get_enriched_files(date, language):
    root = RAW_NEWS / f"{date}-Enriched" / language.lower()
    if not root.exists():
        raise FileNotFoundError(f"没有找到 {date} / {language} Enriched目录：{root}")
    return sorted(root.rglob("*.md"))


def load_news_file(path):
    content = path.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_front_matter(content)
    return {"path": path, "metadata": meta, "body": body, "content": content}


def load_all_enriched_news(date, language):
    files = get_enriched_files(date, language)
    print(f"Enriched files: {len(files)}")
    if not files:
        raise RuntimeError(f"❌ {date} / {language} 没有Enriched新闻")
    items = [load_news_file(p) for p in files]
    items = [x for x in items if x["metadata"].get("title", "").strip()]
    if not items:
        raise RuntimeError(f"❌ {date} / {language} 没有有效新闻")
    def score(x):
        try:
            return float(x["metadata"].get("horizon_score", 0))
        except Exception:
            return 0
    items.sort(key=score, reverse=True)
    print(f"Valid news: {len(items)}")
    return items


def build_article_digest(item, index):
    m = item["metadata"]
    return f"""
[ARTICLE {index}]
标题：{m.get("title", "Untitled")}
来源：{m.get("source", "Unknown")}
原文链接：{m.get("source_url", "")}
来源状态：{m.get("source_status", "")}
内容状态：{m.get("content_status", "")}
内容：
{item["body"][:ARTICLE_CLUSTER_CONTENT_LIMIT]}
""".strip()


# ============================================================
# CLUSTER VALIDATION (同之前)
# ============================================================

def inspect_cluster_assignment(clusters, expected_indexes):
    expected = set(map(int, expected_indexes))
    occ = {}
    malformed = []
    for pos, c in enumerate(clusters, 1):
        if not isinstance(c, dict):
            malformed.append(f"cluster[{pos}]不是对象")
            continue
        ids = c.get("article_indexes")
        if not isinstance(ids, list):
            malformed.append(f"cluster[{pos}] article_indexes不是数组")
            continue
        if not ids:
            malformed.append(f"cluster[{pos}]为空Cluster")
            continue
        for v in ids:
            try:
                i = int(v)
            except Exception:
                malformed.append(f"cluster[{pos}]非法ARTICLE ID：{v}")
                continue
            occ.setdefault(i, []).append(pos)
    duplicate = {i: p for i, p in occ.items() if len(p) > 1}
    actual = set(occ)
    return {
        "duplicate": duplicate,
        "missing": sorted(expected - actual),
        "extra": sorted(actual - expected),
        "malformed": malformed,
    }


def valid_issues(issues):
    return not any([issues["duplicate"], issues["missing"], issues["extra"], issues["malformed"]])


def normalize_clusters(clusters):
    out = []
    for c in clusters:
        if not isinstance(c, dict):
            out.append(c)
            continue
        d = dict(c)
        ids = d.get("article_indexes", [])
        if isinstance(ids, list):
            d["article_indexes"] = [
                int(x) if str(x).lstrip("-").isdigit() else x
                for x in ids
            ]
        out.append(d)
    return out


# ============================================================
# FIRST AI CLUSTERING (同之前)
# ============================================================

def cluster_news_batch(date, items, indexes):
    expected = [int(x) for x in indexes]
    joined = "\n\n".join(build_article_digest(item, expected[i]) for i, item in enumerate(items))
    prompt = f"""
你正在执行748686自生长知识系统V6.5.3第一层事件聚类。

日期：{date}
语言：{CURRENT_LANGUAGE}

{joined}

任务：

识别哪些新闻属于同一个现实世界的具体事件。

支持：
- 跨来源
- 跨语言
- 同一具体现实事件的不同报道

不要因为：
- 公司相同
- 国家相同
- 人物相同
- 行业相同
- 关键词相同

就强行合并。

无法确定时宁可分开。

绝对覆盖ARTICLE编号：

{json.dumps(expected)}

每篇必须且只能属于一个cluster。

无法与其他文章合并的文章必须单独成为cluster。

重要输出限制：

1. cluster_id只能是Local Cluster ID，例如C001、C002。
2. 不得生成EVT-/REC-/GM-等Global ID。
3. Global ID由Python Global Registry生成。
4. event_title尽量短。
5. event_reason尽量短。
6. 不得复制文章正文。
7. 只输出JSON。
8. 不要Markdown。
9. 不要解释。

格式：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "统一事件名称",
      "event_reason": "一句话判断"
    }}
  ]
}}
"""
    result = call_ai(prompt, "你是全球新闻事件聚类专家。每篇ARTICLE必须且只能属于一个cluster。只输出合法JSON。", 0)
    data = parse_ai_json(result, f"{date} {CURRENT_LANGUAGE} 第一轮新闻聚类")
    clusters = data.get("clusters")
    if not isinstance(clusters, list):
        raise RuntimeError("❌ 第一轮聚类结果缺少clusters")
    return normalize_clusters(clusters)


def repair_cluster_news_batch(date, items, indexes, broken, issues, attempt):
    expected = [int(x) for x in indexes]
    joined = "\n\n".join(build_article_digest(item, expected[i]) for i, item in enumerate(items))
    prompt = f"""
修复748686 V6.5.3 ARTICLE覆盖冲突。

日期：{date}
语言：{CURRENT_LANGUAGE}
第{attempt}次修复

真实ARTICLE：

{json.dumps(expected)}

文章：

{joined}

上次结果：

{json.dumps(broken, ensure_ascii=False, indent=2)}

检测问题：

{json.dumps(issues, ensure_ascii=False, indent=2)}

重新判断全部文章。

要求：

1. cluster_id只能是Local Cluster ID。
2. 例如C001。
3. 不得生成EVT-/REC-/GM-。
4. 同一现实事件合并。
5. 不同事件分开。
6. 每篇ARTICLE恰好一次。
7. Missing=0。
8. Duplicate=0。
9. Extra=0。
10. 不得遗漏。
11. 只输出JSON。
12. 不要解释。

格式：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "事件",
      "event_reason": "原因"
    }}
  ]
}}
"""
    result = call_ai(prompt, "你是新闻事件聚类冲突修复专家。必须完整覆盖输入ARTICLE。", 0)
    data = parse_ai_json(result, f"{date} {CURRENT_LANGUAGE} 聚类冲突修复 #{attempt}")
    clusters = data.get("clusters")
    if not isinstance(clusters, list):
        raise RuntimeError("❌ 聚类修复结果缺少clusters")
    return normalize_clusters(clusters)


def _safe_covered_indexes(clusters, expected_indexes):
    issues = inspect_cluster_assignment(clusters, expected_indexes)
    if issues["duplicate"] or issues["extra"] or issues["malformed"]:
        return []
    expected = {int(x) for x in expected_indexes}
    actual = set()
    for cluster in clusters:
        for value in cluster.get("article_indexes", []):
            actual.add(int(value))
    return sorted(actual & expected)


def cluster_news_batch_with_repair(date, items, indexes, batch_label):
    expected = [int(x) for x in indexes]
    clusters = None
    try:
        clusters = cluster_news_batch(date, items, expected)
        issues = inspect_cluster_assignment(clusters, expected)
        if valid_issues(issues):
            return "complete", clusters, []
        log_conflict(date, f"STAGE 1A / {batch_label}", "AI第一次聚类返回非法ARTICLE归属，启动自动修复。", {"issues": issues, "clusters": clusters})
        for attempt in range(1, CLUSTER_REPAIR_ATTEMPTS + 1):
            try:
                clusters = repair_cluster_news_batch(date, items, expected, clusters, issues, attempt)
                issues = inspect_cluster_assignment(clusters, expected)
                if valid_issues(issues):
                    print(" ✅ Cluster conflict repaired successfully.")
                    return "complete", clusters, []
                log_conflict(date, f"STAGE 1A / {batch_label}", f"第{attempt}次聚类冲突修复仍然失败。", {"issues": issues, "clusters": clusters})
            except Exception as repair_error:
                log_conflict(date, f"STAGE 1A / {batch_label}", f"第{attempt}次聚类修复请求/解析失败。", str(repair_error))
        final_issues = inspect_cluster_assignment(clusters or [], expected)
        if final_issues["missing"] and not final_issues["duplicate"] and not final_issues["extra"] and not final_issues["malformed"]:
            safe = _safe_covered_indexes(clusters, expected)
            unresolved = sorted(set(expected) - set(safe))
            if safe and unresolved:
                print(f" 🟡 Missing-only：安全保留{len(safe)}篇，隔离{len(unresolved)}篇：{unresolved}")
                log_conflict(date, f"STAGE 1A / {batch_label}", "修复失败，但仅存在Missing；安全覆盖部分保留，Missing进入Recovery Queue。", {"safe_covered": safe, "recovery_queue": unresolved, "issues": final_issues})
                return "partial", clusters, unresolved
        print(f" 🔴 Batch结果不安全，整批进入Recovery Queue：{expected}")
        log_conflict(date, f"STAGE 1A / {batch_label}", "自动修复失败；整批隔离。", {"issues": final_issues, "recovery_queue": expected})
        return "failed", [], expected
    except Exception as e:
        log_conflict(date, f"STAGE 1A / {batch_label}", "本批AI异常；整批隔离进入Recovery Queue。", str(e))
        print(f" 🔴 AI exception isolated into Recovery Queue: {expected}")
        return "failed", [], expected


# ============================================================
# GLOBAL REGISTRY (同之前，已修复日期格式)
# ============================================================

def create_global_cluster_registry(date, language):
    return {
        "version": "6.5.3",
        "date": str(date),
        "language": str(language),
        "next_sequence": 1,
        "registered": [],
    }


def persist_global_cluster_registry(date, registry):
    path = global_cluster_registry_path(date)
    write_json_atomic(path, {
        "version": "6.5.3",
        "date": registry["date"],
        "language": registry["language"],
        "next_sequence": int(registry["next_sequence"]),
        "registered": registry["registered"],
        "saved_at": now().isoformat(),
    })


def load_or_create_global_registry(date, language):
    path = global_cluster_registry_path(date, language)
    if path.exists():
        registry = read_json(path, None)
        if not isinstance(registry, dict):
            raise RuntimeError(f"❌ {date}/{language} Global Cluster Registry异常")
        if str(registry.get("date")) != str(date):
            raise RuntimeError("❌ Registry日期不一致")
        if str(registry.get("language")).upper() != str(language).upper():
            raise RuntimeError("❌ Registry语言不一致")
        if not isinstance(registry.get("registered"), list):
            raise RuntimeError("❌ Registry registered异常")
        print(f"♻️ 使用已有 Global Registry：{path}")
        return registry
    registry = create_global_cluster_registry(date, language)
    persist_global_cluster_registry(date, registry)
    print(f"🆕 创建 Global Registry：{path}")
    return registry


def register_global_cluster_ids(date, clusters, registry, source):
    out = []
    for c in clusters:
        d = dict(c)
        local_id = str(d.get("local_cluster_id") or d.get("cluster_id") or "").strip()
        if not local_id:
            raise RuntimeError("❌ Global Registry收到空Local Cluster ID")
        if not re.fullmatch(r"C\d+", local_id):
            raise RuntimeError(f"❌ AI Local Cluster ID非法：{local_id}")
        seq = int(registry["next_sequence"])
        date_compact = str(date).replace("-", "")
        global_id = f"EVT-{date_compact}-{seq:06d}"
        registry["next_sequence"] = seq + 1
        d["local_cluster_id"] = local_id
        d["cluster_id"] = global_id
        d["member_cluster_ids"] = [global_id]
        d["global_id_source"] = "python_global_registry"
        d["global_registry_source"] = source
        registry["registered"].append({
            "global_cluster_id": global_id,
            "local_cluster_id": local_id,
            "source": source,
            "article_indexes": sorted(set(int(x) for x in d.get("article_indexes", []))),
        })
        out.append(d)
    persist_global_cluster_registry(date, registry)
    return out


def _make_cluster_records(batch_identifier, clusters):
    out = []
    for c in clusters:
        indexes = sorted(set(int(x) for x in c.get("article_indexes", [])))
        if not indexes:
            continue
        local_id = str(c.get("cluster_id", "C001")).strip()
        out.append({
            "cluster_id": local_id,
            "local_cluster_id": local_id,
            "event_title": c.get("event_title", "未命名事件"),
            "event_reason": c.get("event_reason", ""),
            "article_indexes": indexes,
            "batch_identifier": batch_identifier,
        })
    return out


# ============================================================
# RECOVERY (同之前)
# ============================================================

def _recovery_pass(date, news, indexes, recovery_pass_no, batch_size):
    indexes = sorted(set(int(x) for x in indexes))
    sub_batches = [indexes[i:i + batch_size] for i in range(0, len(indexes), batch_size)]
    recovered = []
    pending = []
    print(f"\n🛠️ RECOVERY PASS {recovery_pass_no} | Articles={len(indexes)} | BatchSize={batch_size} | SubBatches={len(sub_batches)}")
    for sub_no, sub_indexes in enumerate(sub_batches, 1):
        items = [news[index - 1] for index in sub_indexes]
        label = f"RECOVERY {recovery_pass_no} / BATCH {sub_no}"
        print(f" 🔹 {label}: {sub_indexes}")
        if len(sub_indexes) == 1:
            index = sub_indexes[0]
            title = news[index - 1]["metadata"].get("title", "未命名事件").strip()
            recovered.append({
                "cluster_id": f"C{index:03d}",
                "article_indexes": [index],
                "event_title": title[:120] if title else "未命名事件",
                "event_reason": "该文章在恢复阶段作为独立事件单元保留。",
            })
            print(f" 🟢 Singleton安全保留：ARTICLE {index}")
            continue
        status, clusters, unresolved = cluster_news_batch_with_repair(date, items, sub_indexes, label)
        if status == "complete":
            recovered.extend(clusters)
        elif status == "partial":
            safe = _safe_covered_indexes(clusters, sub_indexes)
            safe_set = set(safe)
            safe_clusters = []
            for cluster in clusters:
                ids = [int(x) for x in cluster.get("article_indexes", []) if int(x) in safe_set]
                if ids:
                    item = dict(cluster)
                    item["article_indexes"] = sorted(set(ids))
                    safe_clusters.append(item)
            if safe_clusters:
                recovered.extend(safe_clusters)
            pending.extend(unresolved)
        else:
            pending.extend(sub_indexes)
    return recovered, sorted(set(pending))


def build_initial_clusters(date, news, registry):
    allc = []
    total = len(news)
    print("\n" + "=" * 70)
    print("STAGE 1A — AI EVENT CLUSTERING V6.5.3")
    print("=" * 70)
    print(f"Processing Unit: {date} / {CURRENT_LANGUAGE}")
    print(f"Input Enriched News: {total}")
    print(f"Normal Batch Size: {AGGREGATION_BATCH_SIZE}")
    print("Recovery: 30/15/8/4/2/1")
    pending = []
    normal_batch_no = 0
    for start in range(0, total, AGGREGATION_BATCH_SIZE):
        normal_batch_no += 1
        end = min(start + AGGREGATION_BATCH_SIZE, total)
        indexes = list(range(start + 1, end + 1))
        items = news[start:end]
        print(f"\n🔹 Cluster Batch {normal_batch_no}: {indexes[0]}-{indexes[-1]}/{total}")
        status, clusters, unresolved = cluster_news_batch_with_repair(date, items, indexes, f"CLUSTER BATCH {normal_batch_no}")
        if status == "complete":
            local_records = _make_cluster_records(normal_batch_no, clusters)
            allc.extend(register_global_cluster_ids(date, local_records, registry, f"Batch {normal_batch_no}"))
            print(f" Clusters generated: {len(clusters)}")
        elif status == "partial":
            safe = _safe_covered_indexes(clusters, indexes)
            safe_set = set(safe)
            safe_clusters = []
            for cluster in clusters:
                ids = [int(x) for x in cluster.get("article_indexes", []) if int(x) in safe_set]
                if ids:
                    item = dict(cluster)
                    item["article_indexes"] = sorted(set(ids))
                    safe_clusters.append(item)
            if safe_clusters:
                local_records = _make_cluster_records(normal_batch_no, safe_clusters)
                allc.extend(register_global_cluster_ids(date, local_records, registry, f"Batch {normal_batch_no} SAFE PART"))
            pending.extend(unresolved)
            print(f" 🟡 Safe clusters kept={len(safe_clusters)} | Pending={len(pending)}")
        else:
            pending.extend(unresolved)
            print(f" 🔴 Entire batch isolated | Pending={len(pending)}")
    for pass_no, batch_size in enumerate(RECOVERY_BATCH_SIZES, 1):
        if not pending:
            break
        current_pending = sorted(set(pending))
        pending = []
        recovered, unresolved = _recovery_pass(date, news, current_pending, pass_no, batch_size)
        local_records = _make_cluster_records(f"RECOVERY PASS {pass_no}", recovered)
        allc.extend(register_global_cluster_ids(date, local_records, registry, f"Recovery Pass {pass_no}"))
        pending.extend(unresolved)
        print(f" Recovery Pass {pass_no}: recovered={len(recovered)} | still_pending={len(pending)}")
    if pending:
        log_conflict(date, "STAGE 1A / FINAL RECOVERY", "Recovery Queue仍有未处理ARTICLE，禁止进入Global Merge。", {"pending_articles": sorted(set(pending))})
        raise RuntimeError("❌ V6.5.3 Stage 1A最终仍有未处理ARTICLE：" + str(sorted(set(pending))))
    validate_cluster_coverage(allc, range(1, total + 1), f"{date}/{CURRENT_LANGUAGE} Stage 1A GLOBAL", date)
    validate_global_cluster_membership(date, allc, "STAGE 1A INITIAL")
    print(f"\n✅ Initial Clusters: {len(allc)}")
    print(f"✅ ARTICLE Coverage: {total}/{total}")
    return allc


# ============================================================
# CLUSTER COVERAGE
# ============================================================

def validate_cluster_coverage(clusters, expected, context, date=None):
    issues = inspect_cluster_assignment(clusters, expected)
    if valid_issues(issues):
        return
    if date:
        log_conflict(date, context, "聚类覆盖验证失败。", issues)
    raise RuntimeError(f"❌ {context} 聚类覆盖失败：{issues}")


# ============================================================
# MERGE WINDOWS
# ============================================================

def build_merge_windows(clusters):
    if len(clusters) <= GLOBAL_MERGE_WINDOW_SIZE:
        return [clusters]
    step = GLOBAL_MERGE_WINDOW_SIZE - GLOBAL_MERGE_OVERLAP
    if step <= 0:
        raise RuntimeError("❌ Window Size必须大于Overlap")
    return _windows(clusters, step)


def _windows(clusters, step):
    out = []
    s = 0
    while s < len(clusters):
        e = min(s + GLOBAL_MERGE_WINDOW_SIZE, len(clusters))
        out.append(clusters[s:e])
        if e >= len(clusters):
            break
        s += step
    return out


# ============================================================
# GLOBAL MERGE AI (修改后的核心函数)
# ============================================================

def merge_cluster_window(date, window, round_no, window_no):
    blocks = []
    for i, c in enumerate(window, 1):
        blocks.append(f"""
[CLUSTER {i}]
Cluster ID：
{c["cluster_id"]}

原始Cluster成员：
{json.dumps(c.get("member_cluster_ids", []), ensure_ascii=False)}

事件名称：
{c.get("event_title", "未命名事件")}

事件判断：
{c.get("event_reason", "")}

文章数量：
{len(c.get("article_indexes", []))}

文章编号：
{json.dumps(c.get("article_indexes", []))}
""".strip())
    expected = list(range(1, len(window) + 1))
    base_prompt = f"""
你正在执行748686自生长知识系统V6.5.3全局事件归并。

日期：{date}
语言：{CURRENT_LANGUAGE}
轮次：{round_no}
窗口：{window_no}

{chr(10).join(blocks)}

判断这些Cluster是否属于同一个“具体现实世界事件”。

可以合并：
- 同一政策发布
- 同一公司重大动作
- 同一事故
- 同一产品发布
- 同一具体现实事件
- 同一正在持续发展的单一现实事件

不得合并：
- 同公司不同事件
- 同人物不同事件
- 同国家不同事件
- 同产业不同事件
- 同趋势不同具体事件
- 仅关键词相同
- 仅主题相同

无法确认时宁可分开。

要求：
1. 每个输入Cluster必须且只能进入一个group。
2. 不得遗漏。
3. 不得重复。
4. 不得创造Cluster编号。
5. 一个group可以只有一个Cluster。
6. Cluster ID已经由Python注册。
7. 必须原样引用Global ID。
8. 不得修改Global ID。
9. 不得生成REC-/GM-替代ID。
10. 不需要返回文章编号。
11. 只根据当前窗口判断。
12. 只输出JSON。

输入Cluster编号：
{json.dumps(expected)}

格式：
{{
  "groups": [
    {{
      "group_id": "G001",
      "cluster_indexes": [1,4],
      "event_title": "统一事件名称",
      "reason": "为什么属于同一现实事件"
    }}
  ]
}}
"""
    # 第一次尝试
    try:
        data = parse_ai_json(
            call_ai(base_prompt, "你是全球新闻事件归并专家。必须覆盖全部输入Cluster，每个恰好一次。这是具体事件合并，不是主题分类。", 0),
            f"{date} {CURRENT_LANGUAGE} Global Merge Round {round_no} Window {window_no}"
        )
        groups = data.get("groups")
        if not isinstance(groups, list):
            raise RuntimeError("❌ Global Merge缺少groups")
        # 验证覆盖
        actual = []
        malformed = []
        for p, g in enumerate(groups, 1):
            if not isinstance(g, dict):
                malformed.append(f"group[{p}]不是对象")
                continue
            ids = g.get("cluster_indexes")
            if not isinstance(ids, list) or not ids:
                malformed.append(f"group[{p}]cluster_indexes无效")
                continue
            for x in ids:
                try:
                    actual.append(int(x))
                except Exception:
                    malformed.append(f"group[{p}]非法编号：{x}")
        dup = sorted({x for x in actual if actual.count(x) > 1})
        miss = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if not (dup or miss or extra or malformed):
            return groups
        # 记录第一次失败
        log_conflict(date, f"STAGE 1B / ROUND {round_no} / WINDOW {window_no}", "Global Merge窗口AI输出覆盖异常，尝试修复。", {"duplicate": dup, "missing": miss, "extra": extra, "malformed": malformed, "groups": groups})
    except Exception as e:
        log_conflict(date, f"STAGE 1B / ROUND {round_no} / WINDOW {window_no}", "Global Merge窗口AI调用失败，尝试修复。", str(e))
        groups = []  # 确保后续修复提示有效

    # 第二次尝试：修复提示
    repair_prompt = f"""
你之前处理 Global Merge 窗口时，输出结果不完整。

请重新处理该窗口，必须完整覆盖所有 Cluster 编号。

原始窗口内容：
{chr(10).join(blocks)}

缺失的 Cluster 编号：
{json.dumps(miss if 'miss' in locals() else [])}

重复的 Cluster 编号：
{json.dumps(dup if 'dup' in locals() else [])}

额外的 Cluster 编号：
{json.dumps(extra if 'extra' in locals() else [])}

请输出完整的 groups，确保每个 Cluster 恰好出现一次。

格式：
{{
  "groups": [
    {{
      "group_id": "G001",
      "cluster_indexes": [1,4],
      "event_title": "统一事件名称",
      "reason": "为什么属于同一现实事件"
    }}
  ]
}}
"""
    try:
        data = parse_ai_json(
            call_ai(repair_prompt, "你是全球新闻事件归并专家。必须完整覆盖所有Cluster编号，每个恰好一次。", 0),
            f"{date} {CURRENT_LANGUAGE} Global Merge Repair Round {round_no} Window {window_no}"
        )
        groups = data.get("groups")
        if not isinstance(groups, list):
            raise RuntimeError("❌ 修复后Global Merge缺少groups")
        # 再次验证
        actual = []
        malformed = []
        for p, g in enumerate(groups, 1):
            if not isinstance(g, dict):
                malformed.append(f"group[{p}]不是对象")
                continue
            ids = g.get("cluster_indexes")
            if not isinstance(ids, list) or not ids:
                malformed.append(f"group[{p}]cluster_indexes无效")
                continue
            for x in ids:
                try:
                    actual.append(int(x))
                except Exception:
                    malformed.append(f"group[{p}]非法编号：{x}")
        dup = sorted({x for x in actual if actual.count(x) > 1})
        miss = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if not (dup or miss or extra or malformed):
            print(f" ✅ Global Merge Window {window_no} 修复成功")
            return groups
        # 仍失败，自动补全缺失Cluster
        log_conflict(date, f"STAGE 1B / ROUND {round_no} / WINDOW {window_no}", "Global Merge修复仍失败，自动为缺失Cluster创建单组。", {"duplicate": dup, "missing": miss, "extra": extra, "malformed": malformed})
        # 创建缺失组
        for idx in miss:
            groups.append({
                "group_id": f"G{len(groups)+1:03d}",
                "cluster_indexes": [idx],
                "event_title": window[idx-1].get("event_title", "未命名事件"),
                "reason": "自动补全：该Cluster未在AI输出中覆盖，单独成组。"
            })
        # 如果存在重复或extra，由于不确定如何处理，仅记录日志，但尝试返回当前groups（可能仍有问题，但至少不会中断）
        if dup or extra or malformed:
            log_conflict(date, f"STAGE 1B / ROUND {round_no} / WINDOW {window_no}", "自动补全后仍存在重复或异常，请人工检查。", {"duplicate": dup, "missing": miss, "extra": extra, "malformed": malformed})
        # 返回可能不完美的groups，后续Union-Find将忽略无效组
        return groups
    except Exception as e:
        log_conflict(date, f"STAGE 1B / ROUND {round_no} / WINDOW {window_no}", "Global Merge修复调用失败，自动为所有Cluster创建单组。", str(e))
        # 全部自动补全
        groups = []
        for i in range(1, len(window)+1):
            groups.append({
                "group_id": f"G{i:03d}",
                "cluster_indexes": [i],
                "event_title": window[i-1].get("event_title", "未命名事件"),
                "reason": "自动补全：修复调用失败，全部单独成组。"
            })
        return groups


# ============================================================
# UNION FIND (同之前)
# ============================================================

class UnionFind:
    # ...（省略，与之前完全相同）
    pass


def apply_window_groups(uf, window, groups, round_no, window_no):
    # ...（省略，与之前完全相同）
    pass


def merge_metadata_histories(history, records, uf):
    # ...（省略，与之前完全相同）
    pass


def choose_component_metadata(member_ids, by_id, history, uf):
    # ...（省略，与之前完全相同）
    pass


def rebuild_global_clusters(current, uf, metadata_history):
    # ...（省略，与之前完全相同）
    pass


# ============================================================
# GLOBAL MEMBERSHIP VALIDATION (同之前)
# ============================================================

def validate_global_cluster_membership(date, clusters, context, expected_original_ids=None):
    # ...（省略，与之前完全相同）
    pass


def validate_global_article_coverage(date, clusters, news_count, context):
    # ...（省略，与之前完全相同）
    pass


# ============================================================
# CHECKPOINT (同之前)
# ============================================================

def save_global_merge_checkpoint(date, round_no, current, original_cluster_ids, completed_windows=None, status="running", uf=None, window_count=None, metadata_history=None):
    # ...（省略，与之前完全相同）
    pass


def load_global_merge_checkpoint(date):
    # ...（省略，与之前完全相同）
    pass


def remove_global_merge_checkpoint(date):
    # ...（省略，与之前完全相同）
    pass


def validate_checkpoint(date, checkpoint, expected_original_ids, news_count):
    # ...（省略，与之前完全相同）
    pass


# ============================================================
# GLOBAL MERGE (同之前)
# ============================================================

def merge_all_clusters(date, clusters, news_count):
    # ...（保持不变，但调用了修改后的merge_cluster_window）
    pass


# ============================================================
# EVENT UNIT (同之前)
# ============================================================

# ... 以下所有函数与之前提供的完整代码相同，不再重复列出


# ============================================================
# MAIN (同之前)
# ============================================================

def main():
    # ...（保持不变）
    pass


if __name__ == "__main__":
    sys.exit(main())
