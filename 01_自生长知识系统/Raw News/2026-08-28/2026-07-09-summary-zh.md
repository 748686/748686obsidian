---
layout: default
title: "Horizon Summary: 2026-07-09 (ZH)"
date: 2026-07-09
lang: zh
---

> 从 43 条内容中筛选出 15 条重要资讯。

---

1. [OpenAI 发布 GPT-5.6 系列及 Sol 模型](#item-1) ⭐️ 10.0/10
2. [TypeScript 7.0 发布：Go 重写带来高达 12 倍速度提升](#item-2) ⭐️ 10.0/10
3. [欧盟议会批准聊天控制 1.0 大规模扫描](#item-3) ⭐️ 9.0/10
4. [用 Rust 重写的 Postgres 通过所有回归测试](#item-4) ⭐️ 9.0/10
5. [蚂蚁集团开源 LingBot-Video，首个 MoE 具身视频基模](#item-5) ⭐️ 9.0/10
6. [郑州超算互联网核心节点上线，提供超 10 万张国产 AI 算力卡](#item-6) ⭐️ 9.0/10
7. [Meta 发布 Muse Spark 1.1 代理式 AI 模型](#item-7) ⭐️ 8.0/10
8. [Bun 从 Zig 重写为 Rust](#item-8) ⭐️ 8.0/10
9. [OpenAI 推出 GPT-Live 语音模型，可委托 GPT-5.5 执行复杂任务](#item-9) ⭐️ 8.0/10
10. [Meta 超级智能进展：大规模计算与 RL 初创公司](#item-10) ⭐️ 8.0/10
11. [Rust 1.97.0 发布，新符号混淆方案与 Cargo 警告拒绝](#item-11) ⭐️ 8.0/10
12. [IMGNet：通过符号模式匹配进行人脸验证](#item-12) ⭐️ 8.0/10
13. [大疆 EV50 无人机飞越珠峰创 8861 米纪录](#item-13) ⭐️ 8.0/10
14. [Meta 自研 AI 芯片 Iris 9 月量产，明年算力翻倍](#item-14) ⭐️ 8.0/10
15. [OpenAI 发布国家安全原则，禁止自主武器](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [OpenAI 发布 GPT-5.6 系列及 Sol 模型](https://openai.com/index/gpt-5-6/) ⭐️ 10.0/10

OpenAI 发布了 GPT-5.6 系列，包含三个模型：旗舰 Sol、均衡 Terra 和低成本 Luna。旗舰 Sol 模型在 ARC-AGI-3 基准测试中取得 7.8% 的 SOTA 分数，成为首个经验证在 ARC-AGI-3 游戏中获胜的前沿模型。 此次发布标志着 AI 推理和代理能力的重大飞跃，尤其是在衡量交互式推理与适应的挑战性 ARC-AGI-3 基准上。GPT-5.6 系列增强了 OpenAI 相对于 Anthropic 的 Fable 5 等竞争对手的竞争地位，而 max/ultra 推理、多智能体协作和 Programmatic Tool Calling 的引入使得复杂任务执行更加高效。 GPT-5.6 系列包括 Sol、Terra 和 Luna 模型，其中 Sol 最为强大。GPT-5.6 Sol 使用最大推理努力在 ARC-AGI-3 上取得了 7.8% 的 SOTA，并在编码、科学和网络安全任务上提升了性能。开发者指南强调了改进的意图理解和图像细节保留，而 GPT-5.4 计划于 7 月 23 日下线。

hackernews · logickkk1 · 7月9日 17:04 · [社区讨论](https://news.ycombinator.com/item?id=48849066)

**背景**: ARC-AGI-3 是一个基准测试，通过交互式回合制环境评估流体适应效率和代理智能。与衡量被动推理的前代 ARC-AGI-1 和 2 不同，ARC-AGI-3 要求智能体在没有明确指令的情况下探索、推断目标并规划行动。GPT-5.6 系列基于 OpenAI 之前的模型，引入三个层级以平衡能力、成本和速度，并包含多智能体协作和编程工具调用等功能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arcprize.org/arc-agi/3">ARC-AGI-3</a></li>
<li><a href="https://openai.com/index/previewing-gpt-5-6-sol/">Previewing GPT-5.6 Sol: a next-generation model | OpenAI</a></li>
<li><a href="https://www.axios.com/2026/07/08/gpt-sol-ultra-openai-anthropic-grok">GPT-5.6 buzz builds. Here's what to know about OpenAI's new Sol model</a></li>

</ul>
</details>

**社区讨论**: 社区评论聚焦于开发者指南中使用 GPT-5.6 的技巧、ARC-AGI-3 的 SOTA 结果以及与其他模型的比较。一位用户指出该模型首次在 ARC-AGI-3 游戏中获胜，另一位用户质疑 Codex 能否取代 Claude Code。还有用户注意到，OpenAI 在特定基准测试中排除 Fable 5 的比较，因为它拒绝回答许多生物学问题。

**标签**: `#GPT-5.6`, `#OpenAI`, `#Language Models`, `#AI Safety`, `#Benchmarks`

---

<a id="item-2"></a>
## [TypeScript 7.0 发布：Go 重写带来高达 12 倍速度提升](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) ⭐️ 10.0/10

微软发布了 TypeScript 7.0，这是一个用 Go 重写的原生版本，相比旧版构建速度提升 8 到 12 倍，并支持共享内存多线程。用户可通过 npm 安装，支持 LSP 的编辑器可使用新语言服务器。 这次重写代表了 TypeScript（一种广泛使用的语言）编译器性能的范式转变，大幅减少了大型项目的构建时间。它也展示了使用 Go 等系统语言优化工具性能的增长趋势。 新增实验性参数 --checkers 和 --builders，可微调类型检查和项目引用构建的并行度。但 Vue、Svelte 等嵌入式语言工具链尚未就绪，这些项目仍需使用旧版 TypeScript。

telegram · zaihuapd · 7月9日 04:01

**背景**: TypeScript 是 JavaScript 的静态类型超集，编译为普通 JavaScript。原编译器由 TypeScript 自身编写，在大代码库中性能受限。语言服务器协议（LSP）是一种标准化协议，使编辑器能够提供代码补全和错误检查等语言功能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/">Announcing TypeScript 7.0 - TypeScript</a></li>
<li><a href="https://en.wikipedia.org/wiki/Language_Server_Protocol">Language Server Protocol - Wikipedia</a></li>
<li><a href="https://microsoft.github.io/language-server-protocol/">Official page for Language Server Protocol</a></li>

</ul>
</details>

**标签**: `#TypeScript`, `#Go`, `#Compiler`, `#Performance`, `#Microsoft`

---

<a id="item-3"></a>
## [欧盟议会批准聊天控制 1.0 大规模扫描](https://www.patrick-breyer.de/en/eu-parliament-greenlights-chat-control-1-0-breyer-our-children-lose-out/) ⭐️ 9.0/10

2026 年 7 月 8 日，欧洲议会投票允许对私人信息进行大规模扫描，直至 2028 年 4 月 3 日，尽管多数议员反对此项措施。 这一决定代表着欧盟数字隐私的重大挫折，因为它允许在 Gmail、Snapchat 和 Skype 等平台上对私人通信进行无证扫描，为大规模监控开创了先例。 否决该扫描法律的动议未能通过，因为它需要所有 705 名议员中的绝对多数（361 票），而不仅仅是出席的议员；只有 314 票反对，276 票赞成，17 票弃权，113 人缺席。

hackernews · rapnie · 7月9日 11:03 · [社区讨论](https://news.ycombinator.com/item?id=48843923)

**背景**: 聊天控制是指旨在检测在线通信中儿童性虐待材料的一系列欧盟法规。2022 年的原始提案（聊天控制 1.0）允许科技公司自愿扫描。尽管此前被否决，但由于程序上的漏洞——需要绝对多数才能阻止该立法——在暑假前的最后一天，许多议员已经离开的情况下，该法案得以通过。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chat_Control">Chat Control - Wikipedia</a></li>
<li><a href="https://fightchatcontrol.eu/chat-control-overview">Chat Control 1.0 vs 2.0 - Fight Chat Control</a></li>
<li><a href="https://www.techtimes.com/articles/320010/20260709/eu-parliament-passes-chat-control-default-314-meps-couldnt-block-scanning-law.htm">EU Parliament Passes Chat Control by Default: 314 MEPs Couldn't Block Scanning Law</a></li>

</ul>
</details>

**社区讨论**: 评论者对这一程序性操作表示愤怒，称其反民主且威胁隐私。有人指出投票被安排在暑假前以减少出席人数，并讽刺欧盟在声称保护儿童的同时变得“极权”。

**标签**: `#privacy`, `#surveillance`, `#EU law`, `#Chat Control`, `#democracy`

---

<a id="item-4"></a>
## [用 Rust 重写的 Postgres 通过所有回归测试](https://github.com/malisper/pgrust) ⭐️ 9.0/10

一个名为 pgrust 的项目使用大型语言模型 (LLM) 将 PostgreSQL 完全用 Rust 重写，目前已通过官方 PostgreSQL 回归测试的 100%。 这证明了使用 AI 重写关键基础设施软件（如数据库）的可行性，可能带来更快的创新和更安全的内存管理，同时也引发了关于许可证、代码审查以及对 AI 生成代码信任度的辩论。 该重写项目使用 LLM 生成代码，在不到一个月内产生了超过 7,000 次提交，使得传统代码审查变得不切实际。项目采用 AGPL 许可证，这与 PostgreSQL 的宽松许可证不同。

hackernews · SweetSoftPillow · 7月9日 06:18 · [社区讨论](https://news.ycombinator.com/item?id=48841676)

**背景**: PostgreSQL 回归测试是一套全面的测试套件，用于验证 SQL 实现和扩展功能。基于 LLM 的代码生成是一种新兴技术，利用大型语言模型生成源代码，可以加速开发，但引发了关于正确性、安全性和可维护性的担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.postgresql.org/docs/current/regress.html">PostgreSQL: Documentation: 18: Chapter 31. Regression Tests</a></li>
<li><a href="https://arxiv.org/abs/2508.00083">A Survey on Code Generation with LLM-based Agents</a></li>

</ul>
</details>

**社区讨论**: 作者解释该项目是使用 LLM 构建更好 Postgres 的实验，并正在开发新版本。评论者因大量提交日志而担忧 AI 生成代码的审查问题，并讨论了从 PostgreSQL 许可证改为 AGPL 的争议。有人建议通过镜像流量来比较实际负载下的行为。

**标签**: `#postgres`, `#rust`, `#llm`, `#database`, `#ai`

---

<a id="item-5"></a>
## [蚂蚁集团开源 LingBot-Video，首个 MoE 具身视频基模](https://www.qbitai.com/2026/07/446458.html) ⭐️ 9.0/10

蚂蚁集团开源了 LingBot-Video，这是全球首个基于混合专家（MoE）架构的具身智能视频生成基础模型，在 RBench 评测基准上取得 0.620 的 SOTA 分数，并在 GitHub 以 Apache 2.0 许可证发布。 该开源发布显著降低了具身 AI 研究门槛，其高效的 MoE 架构仅激活 30B 总参数中的 3B，推理效率是同等规模密集模型的 3 倍，可加速机器人动作预测、仿真数据生成和世界模型开发等方向。 LingBot-Video 在架构（DiT+MoE 平衡容量与成本）、数据（7 万小时具身数据，覆盖灵巧操作、机器人移动和第一视角交互）和训练（多维强化学习奖励，关注物理合理性和任务完成度）三方面创新，采用扩散变换器（DiT）骨干网络。

telegram · zaihuapd · 7月9日 04:30

**背景**: 混合专家（MoE）是一种 AI 架构，使用多个专用子网络（专家）和门控机制，每个输入仅激活部分专家，提升效率。扩散变换器（DiT）在扩散模型中用变换器替代传统 U-Net 骨干，实现更好的可扩展性和性能。LingBot-Video 结合这些技术用于具身视频生成，即学习生成机器人执行任务的视频，对机器人学习和仿真有用。RBench 是评估机器人操作视频生成的基准。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>
<li><a href="https://www.nvidia.com/en-us/glossary/mixture-of-experts/">What Is Mixture of Experts (MoE) and How It Works?</a></li>
<li><a href="https://arxiv.org/abs/2212.09748">[2212.09748] Scalable Diffusion Models with Transformers</a></li>

</ul>
</details>

**标签**: `#Embodied AI`, `#Video Generation`, `#MoE`, `#Open Source`, `#Robotics`

---

<a id="item-6"></a>
## [郑州超算互联网核心节点上线，提供超 10 万张国产 AI 算力卡](https://36kr.com/newsflashes/3887797387344387) ⭐️ 9.0/10

2026 年 7 月 9 日，国家超算互联网核心节点在郑州正式上线运行，可对外提供超过 10 万张国产人工智能加速卡作为算力资源池。 这一里程碑标志着接入国家超算互联网的最大单体国产 AI 算力资源池，显著提升了中国自主 AI 计算能力，减少对外部硬件的依赖。 该节点承担运营管理、资源调度等核心功能，并整合供需对接、产业孵化等综合服务，旨在构建覆盖全国的计算资源统筹调度体系。

telegram · zaihuapd · 7月9日 07:00

**背景**: 中国国家超算互联网平台于 2024 年 4 月启动，旨在连接全国超算中心形成一体化网络。国产 AI 加速卡（如华为、中科曙光的产品）正越来越多地部署在大型集群中。"万卡俱乐部"表明国产 AI 芯片基于性能和稳定性正获得市场认可。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Supercomputing_in_China">Supercomputing in China - Wikipedia</a></li>
<li><a href="https://www.akingump.com/en/insights/ai-law-and-regulation-tracker/China's-National-Supercomputing-Internet-Platform">China's National Supercomputing Internet Platform | Akin</a></li>
<li><a href="https://english.www.gov.cn/news/202404/12/content_WS66187785c6d0868f4e8e5f5c.html">China launches national supercomputing network to boost digital economy</a></li>

</ul>
</details>

**标签**: `#supercomputing`, `#AI infrastructure`, `#China`, `#domestic compute`, `#national supercomputing internet`

---

<a id="item-7"></a>
## [Meta 发布 Muse Spark 1.1 代理式 AI 模型](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/) ⭐️ 8.0/10

Meta 于 2026 年 7 月 9 日公开发布 Muse Spark 1.1，这是一个专为代理式编程设计的多模态 AI 模型，可通过 Meta 开发者平台获取 API 访问。 此次发布将 Meta 定位为 OpenAI 和 Anthropic 在 AI 编程助手领域的主要竞争对手，以每百万输入令牌 1.25 美元的激进定价，可能通过将编程模型商品化来颠覆市场。 该模型在 Terminal-Bench 2.1 上进行了评估，但社区分析指出资源限制（6 个 CPU 核心、8GB 内存）被覆盖，这可能使结果无效。定价为每百万令牌输入 1.25 美元、输出 4.5 美元，缓存输入为 0.15 美元。

hackernews · ot · 7月9日 14:10 · [社区讨论](https://news.ycombinator.com/item?id=48846184)

**背景**: Muse Spark 是 Meta 最强大的 AI 模型，最初于 2026 年 4 月发布，作为更广泛规模化计划的一部分。代理式 AI 系统能够自主追求目标、使用工具并采取行动，超越了传统的文本生成。1.1 版本专门针对具备代理能力的编程任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://techcrunch.com/2026/07/09/meta-enters-the-crowded-ai-coding-battle-with-muse-spark-1-1/">Meta enters the crowded AI coding battle with Muse Spark 1 ...</a></li>
<li><a href="https://ai.meta.com/blog/introducing-muse-spark-msl/">Introducing Muse Spark: Scaling Towards Personal ...</a></li>

</ul>
</details>

**社区讨论**: 社区成员对基准测试的有效性持怀疑态度；GodelNumbering 指出覆盖 Terminal-Bench 2.1 中的资源上限会使结果无效。Simon Willison 分享了一个用于 LLM 的实用集成工具，其他人则讨论战略影响和定价，一些用户指出 Meta 的低价可能使编程模型商品化。

**标签**: `#AI`, `#Meta`, `#Muse Spark`, `#LLM`, `#benchmarks`

---

<a id="item-8"></a>
## [Bun 从 Zig 重写为 Rust](https://simonwillison.net/2026/Jul/8/rewriting-bun-in-rust/#atom-everything) ⭐️ 8.0/10

Jarred Sumner 宣布成功将 Bun JavaScript 运行时从 Zig 重写为 Rust，该过程使用了 Claude 进行密集的代理工程，耗时 11 天，API 令牌成本约为 16.5 万美元。 此次重写表明现代 AI 编码代理使大规模重写成为可能，挑战了长期以来的“永不重写”智慧。同时展示了 Rust 的内存安全性如何消除困扰 Zig 手动内存管理的常见错误（如释放后使用）。 Bun 的测试套件（用 TypeScript 编写）充当了验证移植的合规套件。基于 Rust 的新 Bun 自 2026 年 6 月 17 日起已在 Claude Code 中运行，Linux 上启动速度提升 10%，用户未察觉到变化。

rss · Simon Willison · 7月8日 23:57

**背景**: Bun 是一个快速的全能型 JavaScript 运行时、包管理器和测试运行器，最初用 Zig 编写。Zig 是一种需要手动管理内存的系统编程语言，这导致 Bun 中出现释放后使用和双重释放错误。Rust 通过其所有权模型和 Drop trait 提供了内存安全性保证，在编译时防止此类错误。代理工程是指使用能够规划、使用工具并在人工监督下自主完成任务的人工智能代理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Bun_(software)">Bun (software) - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Zig_(programming_language)">Zig (programming language)</a></li>
<li><a href="https://www.ibm.com/think/topics/agentic-engineering">What is agentic engineering? - IBM</a></li>

</ul>
</details>

**标签**: `#Bun`, `#Rust`, `#Zig`, `#systems programming`, `#engineering`

---

<a id="item-9"></a>
## [OpenAI 推出 GPT-Live 语音模型，可委托 GPT-5.5 执行复杂任务](https://simonwillison.net/2026/Jul/8/introducing-gptlive/#atom-everything) ⭐️ 8.0/10

OpenAI 推出了 GPT-Live，这是一系列新的 ChatGPT 语音模型，支持全双工对话，并能将复杂任务委托给 GPT-5.5。两个版本可用：面向付费用户的 GPT-Live-1 和作为所有用户默认选项的 GPT-Live-1 mini，后者取代了高级语音模式。 此次升级通过使用更强大的模型和无缝的任务委托，显著提升了 ChatGPT 语音模式的用户体验，尤其适用于复杂查询。这展示了对话式 AI 的实用进展，使语音助手在头脑风暴和多步骤任务中更加有用。 GPT-Live 采用全双工架构，可同时听和说，保持自然对话流畅。它将网页搜索、深度推理等复杂工作委托给 OpenAI 最新前沿模型 GPT-5.5，且 OpenAI 将持续更新后台模型。较大的 GPT-Live-1 模型面向付费用户，而 GPT-Live-1 mini 免费可用。

rss · Simon Willison · 7月8日 23:20

**背景**: ChatGPT 之前的语音模式基于较老的 GPT-4o 时代模型，知识截止于 2024 年，限制了其实用性。GPT-Live 利用了 2026 年 4 月发布的 GPT-5.5 前沿模型，该模型专为编码和研究等复杂任务设计。全双工语音允许双方同时说话和收听，实现更自然的交互。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.explainx.ai/blog/gpt-live-openai-chatgpt-voice-july-2026">GPT-Live: OpenAI Full-Duplex ChatGPT Voice | explainx.ai Blog</a></li>
<li><a href="https://help.openai.com/en/articles/8400625-voice-mode">ChatGPT Voice - OpenAI Help Center</a></li>
<li><a href="https://tech.yahoo.com/ai/chatgpt/articles/openai-launches-gpt-live-voice-130906310.html">OpenAI launches GPT-Live voice models for real-time conversations</a></li>

</ul>
</details>

**标签**: `#OpenAI`, `#GPT-Live`, `#voice mode`, `#GPT-5.5`, `#AI assistants`

---

<a id="item-10"></a>
## [Meta 超级智能进展：大规模计算与 RL 初创公司](https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence) ⭐️ 8.0/10

Meta 的超级智能部门发布了一年进展更新，强调了前所未有的大规模计算扩展，包括超过 2000 公里的跨数据中心基础设施，以及一个顶级强化学习环境初创公司的出现。 这标志着 AI 基础设施竞赛的加速，Meta 的激进投资可能重塑超级智能领域。RL 环境初创公司填补了训练高级 AI 代理的关键空白。 计算扩展涉及超过 2000 公里的“跨数据中心”网络，使多个数据中心像一台超级计算机一样工作。RL 环境初创公司被描述为“凭空出现”，表明这是一个突然的新竞争者。

rss · Semianalysis · 7月9日 19:16

**背景**: Meta 超级智能实验室（MSL）是 Meta 旗下专注于实现人工超级智能的部门。传统计算扩展通常限于单个数据中心，但“跨数据中心”技术连接分布式站点以克服电力和空间限制。强化学习环境提供模拟或真实世界设置，RL 代理通过试错在其中进行训练。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Meta_Superintelligence_Labs">Meta Superintelligence Labs - Wikipedia</a></li>
<li><a href="https://www.naddod.com/blog/a-complete-guide-to-scale-across-the-third-pillar-of-ai-computing">What Is Scale-Across? A Complete Guide to the “Third Pillar ...</a></li>
<li><a href="https://www.patronus.ai/guide-to-rl-environments">RL Environments: Tutorial & Examples</a></li>

</ul>
</details>

**标签**: `#AI`, `#Meta`, `#Superintelligence`, `#Compute`, `#Reinforcement Learning`

---

<a id="item-11"></a>
## [Rust 1.97.0 发布，新符号混淆方案与 Cargo 警告拒绝](https://lwn.net/Articles/1082032/) ⭐️ 8.0/10

Rust 1.97.0 引入了新的默认符号混淆方案，支持通过新标志拒绝 Cargo 警告，并且在成功构建后不再隐藏链接器输出。 这些更改提高了 Rust 开发者的构建可靠性和调试体验。拒绝警告有助于在 CI 管道中强制执行代码质量，而新的混淆方案提供了更稳定的符号名称。 新的符号混淆方案可跨 Rust 版本生成更一致的符号名称。Cargo 警告拒绝功能允许将警告视为错误，类似于 rustc 中的`-D warnings`。移除隐藏链接器输出意味着所有链接器消息现在都可见。

rss · LWN.net · 7月9日 13:19

**背景**: 符号混淆用于为链接器使用的符号编码唯一名称。Rust 之前的混淆方案在不同版本间可能变化，导致不稳定。拒绝 Cargo 警告是长期请求的功能，用于强制执行更严格的构建策略。之前成功构建后默认隐藏链接器输出，这可能会隐藏有用的诊断信息。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://doc.rust-lang.org/stable/rustc/symbol-mangling/index.html">Symbol Mangling - The rustc book - Learn Rust</a></li>
<li><a href="https://github.com/rust-lang/cargo/issues/8424">Add `--deny-warnings` functionality for all commands. · Issue ...</a></li>

</ul>
</details>

**标签**: `#Rust`, `#release`, `#programming language`, `#tooling`, `#build system`

---

<a id="item-12"></a>
## [IMGNet：通过符号模式匹配进行人脸验证](https://www.reddit.com/r/MachineLearning/comments/1urxvxh/i_built_imgnet_a_face_verification_model_that/) ⭐️ 8.0/10

IMGNet 提出了一种人脸验证模型，用滑动窗口符号模式匹配取代余弦相似度，在 LFW 上达到 96.27% 的准确率，模型大小仅 10.58 MB，在 CASIA-WebFace 上训练。 这种新颖的方法可能实现更高效、更紧凑的人脸验证系统，而符号模式匹配无需重新训练即可提升 ArcFace 嵌入的发现，表明这是良好训练的人脸嵌入的基本属性。 该模型使用 SW Block 替代标准卷积，采用多尺度关系操作；定义了纯基于符号模式一致性的 IMG Sign MSE Loss；以及结合三种度量的投票系统。在无需重新训练的情况下应用于 ArcFace (buffalo_l)，IMG Sign Score 在 LFW 上达到 99.58%，仅比 ArcFace+Cosine 低 0.24%。

reddit · r/MachineLearning · /u/img-_- · 7月9日 18:00

**背景**: 人脸验证通常使用余弦相似度比较嵌入向量，以判断两张脸是否属于同一个人。IMGNet 则比较嵌入向量在滑动窗口上的局部关系符号模式，其灵感来自语言学中表面形式不同但意义相同的例子。该模型在包含 49 万张图像的 CASIA-WebFace 数据集上训练。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/imamgh11/imgnet">GitHub - imamgh11/imgnet: NEW ERA OF AI</a></li>
<li><a href="https://github.com/imamgh11/imgnet/blob/main/README.md">imgnet/README.md at main · imamgh11/imgnet · GitHub</a></li>

</ul>
</details>

**标签**: `#face verification`, `#machine learning`, `#computer vision`, `#representation learning`, `#embedding similarity`

---

<a id="item-13"></a>
## [大疆 EV50 无人机飞越珠峰创 8861 米纪录](https://www.163.com/dy/article/L1CUCV940514R9OJ.html) ⭐️ 8.0/10

大疆未发布的 EV50 垂直起降运载无人机在珠穆朗玛峰上空飞行至 8861 米，创造了公开测试中电动垂直起降（eVTOL）无人机的最高飞行升限纪录。 这一成就证明了使用 VTOL 运载无人机在极端环境下进行高海拔物流和科学研究的可行性，可能改变偏远山区物资运输的方式。 在为期 12 天的任务中，EV50 完成 32 架次起降，连续爬升 3730 米，返程时仍剩 30%电量。它搭载了北京大学研究人员的臭氧测量设备。

telegram · zaihuapd · 7月9日 06:00

**背景**: EV50 是一款复合翼 VTOL 无人机，可以像多旋翼一样垂直起降，然后过渡到固定翼飞行以实现高效长距离巡航。这种混合设计结合了垂直操作的灵活性和固定翼飞机的续航能力，适用于需要精确悬停和远距离飞行的任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://dronexl.co/2026/07/09/dji-ev50-evtol-delivery-drone-everest/">DJI EV50 Debuts As Company's First EVTOL Delivery Drone With ...</a></li>
<li><a href="https://pandaily.com/dji-ev50-everest-vtol-cargo-drone-jul2026">DJI Unreleased EV50 VTOL Cargo Drone Flies Above Everest ...</a></li>
<li><a href="https://www.ecns.cn/cns-wire/2026-07-09/detail-ihfhemcv3615461.shtml">DJI unveils EV50 drone after setting Everest altitude record</a></li>

</ul>
</details>

**标签**: `#drone`, `#VTOL`, `#DJI`, `#high-altitude`, `#logistics`

---

<a id="item-14"></a>
## [Meta 自研 AI 芯片 Iris 9 月量产，明年算力翻倍](https://www.reuters.com/world/asia-pacific/meta-put-ai-chip-into-production-september-it-looks-double-computing-capacity-2026-07-09/) ⭐️ 8.0/10

Meta 计划于 2026 年 9 月启动自研 AI 芯片“Iris”的量产，目标是在 2027 年将整体 AI 算力翻倍至 14 吉瓦。 此举降低了 Meta 对英伟达和 AMD 等外部供应商的依赖，可能重塑 AI 硬件市场，并降低大规模 AI 训练和推理的成本。 该芯片属于 MTIA（Meta 训练和推理加速器）第四代项目，由博通协助设计、台积电制造，仅用六周完成测试，未发现重大问题。

telegram · zaihuapd · 7月9日 12:37

**背景**: Meta 一直在大力投资 AI 基础设施，计划今年部署 7 吉瓦算力，AI 基础设施投入高达 1450 亿美元。MTIA 芯片系列是 Meta 定制的 ASIC，专为优化推荐算法、内容排名等 AI 工作负载而设计，比通用 GPU 具有更高效率。通过自研芯片，Meta 旨在减少对英伟达等主导供应商的依赖并控制成本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ithome.com/0/974/723.htm">消息称 Meta 计划 9 月量产自研 AI 芯片 Iris，目标明年 AI 算力翻倍...</a></li>
<li><a href="https://news.qq.com/rain/a/20260709A0A17L00">报道：Meta自研AI芯片“Iris”计划9月量产，2027年算力拟翻倍至14吉瓦</a></li>

</ul>
</details>

**标签**: `#AI`, `#hardware`, `#Meta`, `#chips`, `#infrastructure`

---

<a id="item-15"></a>
## [OpenAI 发布国家安全原则，禁止自主武器](https://openai.com/index/government-national-security-partnerships/) ⭐️ 8.0/10

OpenAI 公布了一套国家安全原则，明确禁止将其技术用于自主武器、大规模监控以及高风险自动化决策。该公司还通过 Daybreak 网络防御计划扩大了与美国盟友的防御合作，包括与澳大利亚、加拿大、日本和欧盟机构的合作。 这为国家安全领域的 AI 治理树立了明确先例，在道德边界与防御应用之间取得平衡。可能会影响全球其他 AI 公司和政府政策，尤其是在 AI 的军事用途方面。 这些原则严格禁止大规模国内监控、自主武器系统和高风险自动化决策。Daybreak 计划为经过验证的防御者提供高级 AI 工具，将更宽松的功能与更强的监督和范围控制相结合。

telegram · zaihuapd · 7月9日 13:22

**背景**: OpenAI 长期面临其技术在军事领域的伦理问题。此前，公司使用政策禁止任何军事应用，但近期国家安全合作有所增加。这些新原则正式界定了允许的防御用途，同时划定了明确的红线。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openai.com/daybreak/">Daybreak | OpenAI for cybersecurity</a></li>
<li><a href="https://openai.com/index/daybreak-securing-the-world/">Daybreak: Tools for securing every organization in the world</a></li>

</ul>
</details>

**标签**: `#AI safety`, `#AI governance`, `#OpenAI`, `#national security`, `#autonomous weapons`

---