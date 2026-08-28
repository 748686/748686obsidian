---
layout: default
title: "Horizon Summary: 2026-05-29 (ZH)"
date: 2026-05-29
lang: zh
---

> 从 30 条内容中筛选出 9 条重要资讯。

---

1. [Anthropic H 轮融资 650 亿美元，估值 9650 亿](#item-1) ⭐️ 10.0/10
2. [Linux 内核用内存描述符替代 struct page](#item-2) ⭐️ 9.0/10
3. [英伟达承诺每年在台湾投资 1500 亿美元，将其作为 AI 中心](#item-3) ⭐️ 9.0/10
4. [LLM 写作气味合集引发热议](#item-4) ⭐️ 8.0/10
5. [以 Postgres 为基础构建持久化工作流](#item-5) ⭐️ 8.0/10
6. [IBM 启动 50 亿美元 Project Lightwell 保障开源安全](#item-6) ⭐️ 8.0/10
7. [英伟达基本放弃中国 AI 芯片市场](#item-7) ⭐️ 8.0/10
8. [高通与字节跳动合作 AI 定制 ASIC 芯片](#item-8) ⭐️ 8.0/10
9. [比亚迪发布 4nm 智驾芯片'璇玑 A3'](#item-9) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Anthropic H 轮融资 650 亿美元，估值 9650 亿](https://www.anthropic.com/news/series-h) ⭐️ 10.0/10

Anthropic 宣布完成 650 亿美元的 H 轮融资，投后估值达 9650 亿美元，在收入和估值上均超越 OpenAI。 这标志着 AI 行业的重大转变，Anthropic 现已领先 OpenAI，可能重塑竞争格局和投资者信心。 Anthropic 报告称，截至 5 月初，其年化收入已达 470 亿美元，高于 2 月份的 300 亿美元，此次 H 轮融资紧随今年早些时候的 G 轮之后。

hackernews · meetpateltech · 5月28日 18:09 · [社区讨论](https://news.ycombinator.com/item?id=48313048)

**背景**: H 轮是后期融资轮次，投后估值包含新注入资本。年化收入通过近期收入推算年度数据，显示快速增长。Anthropic 超越 OpenAI 标志着生成式 AI 格局的变化。

**社区讨论**: 评论讨论了年化收入与传统收入的区别，指出 Anthropic 超越 OpenAI 是更大的新闻，并创造了'千角兽'一词来指代万亿美元估值。

**标签**: `#Anthropic`, `#funding`, `#AI`, `#valuation`, `#OpenAI`

---

<a id="item-2"></a>
## [Linux 内核用内存描述符替代 struct page](https://lwn.net/Articles/1073425/) ⭐️ 9.0/10

Vishal Moola 在 LSFMM+BPF 2026 峰会上介绍了用内存描述符替代 struct page 的现状和未来计划。 这是 Linux 内存管理的根本性变革，可减少内存开销和复杂性，有望提高内核的性能和可维护性。 内存描述符计划仅占 8 字节，已有 folio、slab、ptdesc、zsmalloc、netmem 等类型。转换涉及双分配开销，并提出了默认禁用的 CONFIG_MEMDESC 选项。

rss · LWN.net · 5月28日 13:09

**背景**: struct page 自 1995 年以来一直是 Linux 内存管理的核心，但它已增长到 64 字节，并因支持不同页面类型而堆满了联合体，导致效率低下。内存描述符旨在分离类型特定信息，仅存储指向类型特定描述符的指针，从而使结构更小、更易维护。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blogs.oracle.com/linux/introducing-memdesc">Introducing Memdesc | linux</a></li>
<li><a href="https://lwn.net/Articles/1015320/">The state of the page in 2025 [LWN.net]</a></li>
<li><a href="https://lore.kernel.org/linux-mm/5a55874d-80b9-b622-ec98-1bfdf3b251bf@redhat.com/T/">Dynamically allocated memory descriptors</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#memory management`, `#memory descriptors`, `#struct page`, `#LSFMM`

---

<a id="item-3"></a>
## [英伟达承诺每年在台湾投资 1500 亿美元，将其作为 AI 中心](https://arstechnica.com/tech-policy/2026/05/nvidia-ceo-wants-taiwan-to-be-center-of-ai-revolution-not-us/) ⭐️ 9.0/10

英伟达 CEO 黄仁勋宣布计划每年在台湾投入约 1500 亿美元，称台湾是 AI 革命中心。这笔投资涵盖 AI 芯片生产、系统制造以及与台积电、鸿海等公司的供应链合作。 这一史无前例的年度承诺标志着英伟达的战略转向，将台湾确立为 AI 硬件开发的核心。它可能重塑全球 AI 供应链，并加剧围绕半导体自主的地缘政治讨论。 新台北总部预计今年动工、2030 年启用，容纳 4000 名员工。此前年度投资规模约为 100 亿至 150 亿美元，而 1500 亿美元的数字是之前的十倍。

telegram · zaihuapd · 5月28日 07:33

**背景**: 英伟达设计的 GPU 和 AI 加速器高度依赖先进半导体制造，主要来自台积电（位于台湾）。台湾的生态系统，包括鸿海、纬创和广达，为英伟达的 AI 系统提供关键的组装和供应链服务。由于其在半导体领域的统治地位，台湾长期以来一直是全球科技地缘政治的焦点。

**标签**: `#NVIDIA`, `#AI`, `#Taiwan`, `#semiconductors`, `#investment`

---

<a id="item-4"></a>
## [LLM 写作气味合集引发热议](https://shvbsle.in/various-llm-smells/) ⭐️ 8.0/10

一篇名为《Various LLM Smells》的博客文章汇总了表明文本由 LLM 生成的常见语言模式，例如“the honest caveat:”和“load bearing”等短语。 该资源帮助读者识别并避免 LLM 输出的同质化风格，在借助 AI 辅助的同时保持写作个性。 文章列出了一些具体模式，如对比否定（“不是 X，而是 Y”）以及在标题中过度使用“The”，这些模式也被包括 Claude 用户在内的评论者注意到。

hackernews · speckx · 5月28日 19:02 · [社区讨论](https://news.ycombinator.com/item?id=48313810)

**背景**: LLM“气味”类似于软件工程中的代码异味——这些模式暗示输出是由语言模型而非人类生成的。这些语言习惯源于训练数据偏差和模型倾向，使得即使没有正式检测器也能识别 AI 文本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2605.22976">LLM Code Smells: A Taxonomy and Detection Approach</a></li>

</ul>
</details>

**社区讨论**: 评论者分享了更多气味（例如非爆炸场景下的“blast radius”），并辩论是否应直接使用 LLM 输出还是仅用于批判。有人认为 LLM 的同质化在网页设计中有利，但对个人写作风格有害。

**标签**: `#LLM`, `#writing`, `#text generation`, `#AI detection`, `#style`

---

<a id="item-5"></a>
## [以 Postgres 为基础构建持久化工作流](https://www.dbos.dev/blog/postgres-is-all-you-need-for-durable-execution) ⭐️ 8.0/10

DBOS 发布了一篇博客，主张仅用 Postgres 就能构建持久化工作流执行，将其作为 Temporal 等专用工作流引擎的更简单替代方案。 这一提议可能通过减少依赖来简化系统架构，但也引发了关于可扩展性与成熟平台功能对等性的疑问。评估工作流解决方案的工程师必须权衡以数据库为中心的方法与专用服务之间的利弊。 DBOS 依赖一个名为 Conductor 的付费组件来实现扩展和恢复，一些社区成员认为这是一个限制。还存在 Armin Ronacher 的 absurd 和 River 等替代方案，每个方案都有自己的权衡，例如 River 的免费版本缺少死信队列支持。

hackernews · KraftyOne · 5月28日 18:41 · [社区讨论](https://news.ycombinator.com/item?id=48313530)

**背景**: 持久化工作流通过持久化状态确保长时间运行的过程在故障后仍能继续。像 Temporal 这样的专用工作流引擎提供了这些能力，但增加了基础设施的复杂性。DBOS 的博客认为，已经广泛用于数据存储的 Postgres 可以作为数据和工作流状态的单一事实来源，从而消除对单独引擎的需求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://temporal.io/">Durable Execution Solutions | Temporal</a></li>

</ul>
</details>

**社区讨论**: 评论者指出 DBOS 依赖付费的 Conductor 组件是阻碍因素。一些人分享了他们自己使用 Postgres 和其他后端实现的轻量级方案，而另一些人则讨论了 DBOS、Temporal、absurd 和 River 之间的权衡，突出了诸如负载大小限制和缺失功能等问题。

**标签**: `#durable workflows`, `#Postgres`, `#database`, `#engineering`, `#temporal`

---

<a id="item-6"></a>
## [IBM 启动 50 亿美元 Project Lightwell 保障开源安全](https://lwn.net/Articles/1075065/) ⭐️ 8.0/10

IBM 和 Red Hat 宣布 Project Lightwell，这是一项耗资 50 亿美元的计划，旨在建立一个由 AI 驱动的开源软件漏洞信息中心，并得到超过 2 万名工程师的支持。 这是企业在开源安全领域最大规模的投资之一，可能彻底改变企业大规模处理漏洞的方式，并加强整个行业的供应链安全性。 该信息中心将利用先进 AI 验证和测试补丁，通过商业订阅向企业提供集成服务，同时也会与上游项目共享漏洞信息。

rss · LWN.net · 5月28日 13:30

**背景**: 开源软件依赖成千上万的项目，这些项目往往缺乏专门的安全资源。漏洞信息中心作为一个中央枢纽，用于识别、验证和分发补丁，帮助企业高效管理其软件供应链中的风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://newsroom.ibm.com/2026-05-28-ibm-and-red-hat-commit-5-billion-to-redefine-the-future-of-open-source-in-the-ai-era">IBM and Red Hat Commit $5 Billion to Redefine the Future of Open Source in the AI Era</a></li>
<li><a href="https://www.redhat.com/en/about/press-releases/project-lightwell-secure-open-source">IBM and Red Hat Commit $5 Billion to Redefine the Future of Open Source in the AI Era</a></li>
<li><a href="https://linuxiac.com/ibm-and-red-hat-launch-5b-open-source-security-project/">IBM and Red Hat Launch $5B Open Source Security Project</a></li>

</ul>
</details>

**标签**: `#open source security`, `#AI`, `#vulnerability management`, `#IBM`, `#Project Lightwell`

---

<a id="item-7"></a>
## [英伟达基本放弃中国 AI 芯片市场](https://t.me/zaihuapd/41609) ⭐️ 8.0/10

英伟达 CEO 黄仁勋表示，由于美国出口限制，公司已基本放弃中国 AI 芯片市场，将其让给华为等本土竞争对手。他建议投资者不要期望获得向中国销售先进芯片的许可。 这标志着全球 AI 芯片格局的重大转变，中国将越来越依赖华为等国内供应商。它凸显了中美技术脱钩日益加剧的影响，并可能加速中国在半导体领域的自给自足。 中国市场此前至少占英伟达数据中心收入的五分之一。英伟达现在正专注于扩大供应链，并宣布了 800 亿美元的股票回购计划。

telegram · zaihuapd · 5月28日 03:03

**背景**: 美国出口管制措施于今年 4 月由特朗普政府实施，要求向中国出口先进芯片必须获得许可。这些管制旨在限制中国获取尖端 AI 技术。英伟达的 GPU 被广泛用于 AI 训练和推理，失去中国市场迫使公司将投资转向其他地区。

**标签**: `#Nvidia`, `#AI chips`, `#export controls`, `#China`, `#semiconductor`

---

<a id="item-8"></a>
## [高通与字节跳动合作 AI 定制 ASIC 芯片](https://t.me/zaihuapd/41616) ⭐️ 8.0/10

高通已与字节跳动达成合作，将为其生产定制 AI ASIC 芯片，字节跳动将采购数百万颗用于 AI 推理工作负载的芯片。 该合作使高通成为定制 AI 芯片市场的重要供应商，并为字节跳动提供了大规模、优化的硬件以支撑其 AI 服务，可能改变 AI 推理硬件的竞争格局。 字节跳动还将借助高通的制造经验，将其内部芯片设计转化为可量产的半导体产品。此前高通在 4 月底宣布，将于今年向某超大规模云服务商交付首款 ASIC。

telegram · zaihuapd · 5月28日 07:09

**背景**: 专用集成电路（ASIC）是为特定用途定制的芯片，在 AI 推理等特定任务上比通用 CPU 或 GPU 效率更高。AI 推理工作负载指的是预训练模型处理新数据以进行预测时所需的计算资源。字节跳动等超大规模云服务商越来越多地采用定制 ASIC，以优化性能并降低大规模 AI 服务的成本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ASIC">ASIC</a></li>
<li><a href="https://www.naddod.com/ai-insights/what-are-ai-inference-workloads-why-ai-inference-workloads-are-growing-rapidly">Introduction of AI Inference Workloads - NADDOD Blog</a></li>

</ul>
</details>

**标签**: `#AI chips`, `#Qualcomm`, `#ByteDance`, `#ASIC`, `#hardware`

---

<a id="item-9"></a>
## [比亚迪发布 4nm 智驾芯片'璇玑 A3'](https://finance.sina.com.cn/roll/2026-05-28/doc-inhznenn1371824.shtml) ⭐️ 8.0/10

5 月 28 日，比亚迪宣布其自研的 4 纳米智驾芯片“璇玑 A3”进入规模化量产，支持 L3、L4 级别自动驾驶，三颗芯片总算力超过 2100 TOPS。 这标志着主流车企在智能驾驶芯片设计上实现垂直整合的重要一步，有望降低对外部供应商的依赖。高算力和 4 纳米工艺表明该芯片具有与顶级 AI 芯片竞争的能力。 比亚迪声称该芯片结合自研算法优化，算力利用率提升 100%。公司还表示已推出 2000 多款芯片产品，并拥有 5 座晶圆工厂。

telegram · zaihuapd · 5月28日 13:01

**背景**: 自动驾驶芯片是专门用于处理自动驾驶汽车海量传感器数据和实时决策的处理器。采用 4 纳米制程——这是领先的半导体制造工艺——能够实现更高的性能和能效。比亚迪进入芯片生产是汽车制造商自研芯片这一更广泛趋势的一部分。

**社区讨论**: 无社区评论。

**标签**: `#autonomous driving`, `#BYD`, `#4nm chip`, `#automotive`, `#AI`

---