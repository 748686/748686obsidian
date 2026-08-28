---
layout: default
title: "Horizon Summary: 2026-06-19 (ZH)"
date: 2026-06-19
lang: zh
---

> 从 40 条内容中筛选出 6 条重要资讯。

---

1. [Transformer 共同作者 Noam Shazeer 离开谷歌加入 OpenAI](#item-1) ⭐️ 9.0/10
2. [发现 10,000 个 GitHub 仓库分发木马恶意软件](#item-2) ⭐️ 8.0/10
3. [医院和大学以更低成本重新利用药物](#item-3) ⭐️ 8.0/10
4. [驳斥 2026 年美国数据中心容量取消的夸大说法](#item-4) ⭐️ 8.0/10
5. [SFC 发布面向 FOSS 的 LLM 生成式 AI 最佳实践建议](#item-5) ⭐️ 8.0/10
6. [苹果与英特尔达成初步芯片代工协议](#item-6) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Transformer 共同作者 Noam Shazeer 离开谷歌加入 OpenAI](https://twitter.com/NoamShazeer/status/2067400851438932297) ⭐️ 9.0/10

此举标志着 AI 领域的一次重大人才流动，Shazeer 是奠定现代大语言模型基础的 Transformer 架构的关键贡献者，他的加入可能加速 OpenAI 在下一代 AI 模型上的研发。 Shazeer 最初于 2021 年离开谷歌，联合创立了 Character.AI，随后在 2024 年通过一项价值约 27 亿美元的许可和人才协议回归。他担任 Gemini 联合负责人仅数月便再次离职。

hackernews · lukasgross · 6月18日 00:26 · [社区讨论](https://news.ycombinator.com/item?id=48578913)

**背景**: Transformer 架构由 2017 年发表的论文《Attention Is All You Need》提出，通过用注意力机制取代循环层和卷积层，彻底革新了自然语言处理。它是 GPT、BERT 和 Gemini 等模型的基础。Shazeer 是该论文的八位共同作者之一，并在谷歌担任工程师长达二十余年。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/1706.03762">Abstract page for arXiv paper 1706.03762: Attention Is All You Need</a></li>
<li><a href="https://research.google/pubs/attention-is-all-you-need/">Attention is All You Need</a></li>

</ul>
</details>

**社区讨论**: 社区反响热烈，许多人提供了 Shazeer 从谷歌到 Character.AI 再回归的职业轨迹信息。一些人对他回归后迅速离职感到惊讶，另一些人则猜测此举背后有政治或战略原因。总体情绪是这对 OpenAI 来说是一次重大胜利。

**标签**: `#AI`, `#transformers`, `#Noam Shazeer`, `#OpenAI`, `#Google`

---

<a id="item-2"></a>
## [发现 10,000 个 GitHub 仓库分发木马恶意软件](https://orchidfiles.com/github-repositories-distributing-malware/) ⭐️ 8.0/10

一名安全研究人员发现约 10,000 个 GitHub 仓库正在主动分发木马恶意软件，利用该平台的信任来感染毫无戒心的用户。 这一发现凸显了开源软件中严重的供应链风险，恶意代码可以通过自动依赖管理器和自动化代理轻松传播，可能影响无数下游项目及用户。 这些恶意仓库通常是热门项目的克隆并稍作修改，而且它们不断推送新提交以出现在搜索结果或“最近更新”列表的顶部，目标是自动化代理而非人类用户。

hackernews · theorchid · 6月18日 11:45 · [社区讨论](https://news.ycombinator.com/item?id=48583928)

**背景**: GitHub 是一个广泛用于托管开源代码的平台，许多软件项目会自动从 GitHub 仓库拉取依赖项。攻击者通过创建模仿合法仓库的虚假仓库来利用这一点，嵌入恶意软件，在持续集成或开发者克隆代码时执行。

**社区讨论**: 社区成员分享了类似经历，一位用户报告其 GitHub 名称被附加到未知项目上，另一位详细描述了一起迪士尼工程师下载恶意 AI 工具的事件。评论者指出这些仓库针对自动化代理，持续更新以保持活跃，并提到了过去此类供应链攻击的案例。

**标签**: `#security`, `#malware`, `#github`, `#supply-chain`, `#open-source`

---

<a id="item-3"></a>
## [医院和大学以更低成本重新利用药物](https://www.kcl.ac.uk/news/hospitals-and-universities-repurposing-drugs-at-90-lower-cost) ⭐️ 8.0/10

医院和大学正在将现有药物重新用于新适应症，大幅降低治疗成本。例如，使用抗癌药物 Avastin 替代 Lucentis 治疗黄斑变性，单次剂量成本从 1500 美元降至 50 美元。 这种做法挑战了高昂的药品价格，可能使治疗更加可负担，尤其对于制药公司缺乏研发动力的罕见病。同时揭示了医疗定价和监管中的系统性问题。 Avastin（贝伐珠单抗）和 Lucentis（雷珠单抗）源于同一母体抗体，但 Avastin 每剂成本约低 30 倍。然而，Avastin 并未按眼内注射包装，需要重新分装并进行超说明书使用。

hackernews · giuliomagnifico · 6月18日 10:33 · [社区讨论](https://news.ycombinator.com/item?id=48583386)

**背景**: 药物重新利用是指将已获批药物用于新的医疗适应症，这比开发新药更快、更便宜。许多现有药物具有新用途的潜力，但监管和商业障碍往往阻碍其应用。例如，Avastin 是一种最初获批用于癌症的 VEGF 抑制剂，也能阻止眼中异常血管生长——湿性黄斑变性的病因。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Avastin">Avastin</a></li>
<li><a href="https://en.wikipedia.org/wiki/Lucentis">Lucentis</a></li>

</ul>
</details>

**社区讨论**: 社区评论赞扬了重新利用的努力，并提供了具体案例，如 Avastin 用于眼病和艾司氯胺酮的争议。用户指出药品定价中的激励扭曲，呼吁建立促进超说明书使用的监管途径。有人指出重新利用可惠及罕见病，但面临制造商的抵制。

**标签**: `#drug repurposing`, `#healthcare costs`, `#pharmaceuticals`, `#innovation`

---

<a id="item-4"></a>
## [驳斥 2026 年美国数据中心容量取消的夸大说法](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter) ⭐️ 8.0/10

SemiAnalysis 的一项新分析指出，关于 2026 年美国数据中心容量一半被取消的说法被严重夸大，并呼吁人们审查具体申报文件而非依赖模糊估计。 这很重要，因为不准确的数据中心容量取消估计可能会误导人工智能基础设施投资和行业规划，可能导致不必要的市场恐慌或政策误判。 该分析强调，标记为'vibecoded'（指基于松散提示由 AI 生成的代码）的估计不可靠，并主张逐一审查每个数据中心的申报文件以评估真实的取消率。

rss · Semianalysis · 6月18日 15:54

**背景**: 近期，一些报告称 2026 年美国计划的数据中心容量中近一半已被取消，引发了对人工智能基础设施供应过剩的担忧。'Vibe coding'是一种软件开发实践，AI 根据描述生成代码；在此语境中，它指代那些同样基于无严格验证的估计。SemiAnalysis 认为这些估计缺乏具体事实依据。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter">Stop Saying Half of 2026 US Datacenter Capacity Is Canceled</a></li>
<li><a href="https://en.wikipedia.org/wiki/Vibe_coding">Vibe coding - Wikipedia</a></li>

</ul>
</details>

**标签**: `#datacenter`, `#infrastructure`, `#AI`, `#industry analysis`, `#capacity planning`

---

<a id="item-5"></a>
## [SFC 发布面向 FOSS 的 LLM 生成式 AI 最佳实践建议](https://lwn.net/Articles/1078521/) ⭐️ 8.0/10

软件自由保护组织 (SFC) 发布了关于在自由和开源软件 (FOSS) 贡献中使用 LLM 生成式 AI 系统的最佳实践建议，该建议由 SFC 和社区志愿者共同制定。 这些建议为面临专有 LLM 生成式 AI 带来的伦理和法律困境的 FOSS 贡献者提供了实用指导，有助于在使用或拒绝这些工具时最大限度地减少对软件自由的损害。 该建议明确被定位为最佳实践而非强制性要求，SFC 后续还将提供文件、教程、公开问答和播客等支持材料以进一步协助社区。

rss · LWN.net · 6月18日 16:00

**背景**: 软件自由保护组织是一个推广软件自由并为 FOSS 项目提供法律和行政支持的非营利组织。LLM 生成式 AI 系统（如 ChatGPT）因训练数据来源不确定且可能生成法律条款不明确的代码，引发了关于许可、归属和伦理使用的担忧。

**标签**: `#open source`, `#LLM`, `#generative AI`, `#software freedom`, `#FOSS`

---

<a id="item-6"></a>
## [苹果与英特尔达成初步芯片代工协议](https://t.me/zaihuapd/42031) ⭐️ 8.0/10

苹果与英特尔签署了一项初步协议，由英特尔为部分苹果设备代工芯片。该协议历经一年多谈判，并在美国政府的强力推动下最终敲定。 这项协议是英特尔代工业务的一项重大胜利，赢得了苹果这样的顶级客户，同时重塑了半导体供应链，减少了苹果对台积电的依赖。这也凸显了美国政府对芯片制造战略日益增强的影响力。 目前尚不清楚苹果哪些产品（iPhone、iPad 或 Mac）将使用英特尔制造的芯片。通过此次协议，英特尔现与英伟达、SpaceX 和苹果三家建立了代工合作伙伴关系。

telegram · zaihuapd · 6月18日 09:19

**背景**: 芯片代工厂是指为其他公司制造集成电路的半导体制造工厂。在代工模式下，像苹果这样的无晶圆厂公司设计芯片，但将生产外包给台积电等纯代工厂，或者越来越多地外包给英特尔这类提供代工服务的整合器件制造商。该协议将苹果的部分生产从台积电转移到英特尔，实现了供应链多元化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chip_foundry">Chip foundry</a></li>

</ul>
</details>

**标签**: `#Apple`, `#Intel`, `#chip manufacturing`, `#foundry`, `#semiconductor`

---