---
layout: default
title: "Horizon Summary: 2026-05-21 (ZH)"
date: 2026-05-21
lang: zh
---

> From 47 items, 13 important content pieces were selected

---

1. [SpaceX S-1 文件披露与 Anthropic 的月均 12.5 亿美元 AI 计算协议](#item-1) ⭐️ 10.0/10
2. [OpenAI 模型推翻 Erdős 长期猜想](#item-2) ⭐️ 9.0/10
3. [GitHub 确认通过恶意 VSCode 扩展泄露 3800 个仓库](#item-3) ⭐️ 9.0/10
4. [Qwen3.7-Max：前沿智能体模型](#item-4) ⭐️ 9.0/10
5. [Google 的 AI 战略对网络流量生态系统宣战](#item-5) ⭐️ 8.0/10
6. [Railway 详述 GCP 账户停用，计划减少依赖](#item-6) ⭐️ 8.0/10
7. [Meta 封锁沙特和阿联酋的人权账号](#item-7) ⭐️ 8.0/10
8. [MGLRU 在 LSFMM+BPF 2026 上的集成挑战](#item-8) ⭐️ 8.0/10
9. [Qwen 3.6 35B GGUF：NTP 与 MTP 量化基准发布](#item-9) ⭐️ 8.0/10
10. [Cohere 发布 Command A+ 218B 稀疏 MoE 模型](#item-10) ⭐️ 8.0/10
11. [谷歌与 OpenAI 推出 AI 内容检测工具](#item-11) ⭐️ 8.0/10
12. [被控路由器用于钓鱼间谍活动](#item-12) ⭐️ 8.0/10
13. [研究：34%的 AI 模型测试出现数据造假](#item-13) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [SpaceX S-1 文件披露与 Anthropic 的月均 12.5 亿美元 AI 计算协议](https://simonwillison.net/2026/May/20/spacex-s1/#atom-everything) ⭐️ 10.0/10

SpaceX 向 SEC 提交的 S-1 文件披露了与 Anthropic 的云计算服务协议，Anthropic 将获得 COLOSSUS 和 COLOSSUS II 的计算能力，并同意每月支付 12.5 亿美元，协议持续至 2029 年 5 月。 这一巨额承诺标志着对 AI 计算基础设施前所未有的需求，并凸显了 AI 实验室与基础设施提供商之间战略合作的重要性，可能重塑云计算商业模式。 协议包含 2026 年 5 月和 6 月的容量爬坡期，期间费用较低，任何一方可提前 90 天通知终止。COLOSSUS I 拥有超过 22 万块 NVIDIA H100、H200 及其他 GPU。

rss · Simon Willison · May 20, 22:26

**背景**: SpaceX 运营着 COLOSSUS I 和 II，这些是用 NVIDIA GPU 构建的巨型 AI 超级计算机，最初用于训练 Grok。Anthropic 是一家专注于 AI 安全的公司，开发了 Claude 大语言模型。此次合作为 Anthropic 提供了训练和推理其模型的专用计算能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.servethehome.com/anthropic-signs-spacex-colossus-1-data-center-to-boost-capacity/">Anthropic Signs SpaceX Colossus 1 Data Center to... - ServeTheHome</a></li>
<li><a href="https://sourceryintel.com/reports/anthropic-spacex-partnership">Anthropic and SpaceX Compute Partnership — May 2026</a></li>

</ul>
</details>

**社区讨论**: 评论者对这笔交易的规模感到震惊，一些人质疑 SpaceX 整体的盈利能力，因为 2025 年净亏损 49 亿美元。另一些人则对空间数据中心的可行性表示怀疑，同时指出 Starlink 的盈利能力支撑了此类 AI 基础设施押注。

**标签**: `#AI`, `#cloud computing`, `#SpaceX`, `#Anthropic`, `#compute infrastructure`

---

<a id="item-2"></a>
## [OpenAI 模型推翻 Erdős 长期猜想](https://openai.com/index/model-disproves-discrete-geometry-conjecture/) ⭐️ 9.0/10

OpenAI 内部模型构建了一族无限的反例，推翻了离散几何中的一个核心猜想——Erdős 单位距离问题，该问题自 1946 年以来悬而未决。该证明已通过形式化验证，并得到外部数学家小组的认可。 这标志着 AI 模型首次推翻了一个长期悬而未决的重大猜想，展示了超越模式匹配的真正科学发现能力。它可能通过提供人类可能忽略的新颖见解和构造来加速数学研究。 该猜想由 Paul Erdős 于 1946 年提出，涉及平面中 n 个点之间同一距离出现次数的最大值。模型生成的反例将此前已知的下界做了多项式改进，证明中运用了代数数论的思想。

hackernews · tedsanders · May 20, 19:05 · [社区讨论](https://news.ycombinator.com/item?id=48212493)

**背景**: 离散几何研究点、线、圆等离散对象的组合性质。Erdős 单位距离问题问：给定平面中的 n 个点，相距恰好一个单位的点对最多有多少？几十年来，已知的上界和下界之间差距很大。OpenAI 模型搜索使单位距离最大化的构造方式，最终找到一族新的无限构造，推翻了 Erdős 的原始猜想。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openai.com/index/model-disproves-discrete-geometry-conjecture/">An OpenAI model has disproved a central conjecture in discrete geometry | OpenAI</a></li>
<li><a href="https://en.wikipedia.org/wiki/Discrete_geometry">Discrete geometry</a></li>

</ul>
</details>

**社区讨论**: 评论中既有兴奋也有哲学辩论：一些人认为这是 LLM 能发现真正新数学的证据，而另一些人指出通过反例证伪在理论深度上不如证明定理。几位评论者将其与象棋中专用 AI（如 Stockfish）相类比，预测未来 AI 数学家将变得常见。

**标签**: `#AI`, `#mathematics`, `#discrete geometry`, `#LLMs`, `#research`

---

<a id="item-3"></a>
## [GitHub 确认通过恶意 VSCode 扩展泄露 3800 个仓库](https://www.bleepingcomputer.com/news/security/github-confirms-breach-of-3-800-repos-via-malicious-vscode-extension/) ⭐️ 9.0/10

GitHub 确认一名员工的电脑因安装恶意 VSCode 扩展程序而被入侵，导致约 3800 个内部仓库遭到未授权访问。该公司已移除该恶意扩展、隔离终端并轮换关键密钥，调查仍在继续。 此事件凸显了通过 IDE 扩展进行供应链攻击的重大风险，尤其是在 GitHub 这样的平台上。它强调了在开发环境中对扩展安装和依赖管理实施更严格安全策略的必要性。 此次泄露影响了 GitHub 的内部仓库，但公司表示暂无证据表明客户代码或企业仓库受到影响。安全消息人士称，泄露内容可能包含 Copilot 和 CodeQL 等核心项目的源代码。

hackernews · Timofeibu · May 20, 13:43 · [社区讨论](https://news.ycombinator.com/item?id=48207660)

**背景**: 供应链攻击针对软件开发过程中安全性较弱的环节，例如第三方扩展或依赖项。VSCode 扩展虽然增强了功能，但如果执行恶意代码，可能会带来重大安全风险。虽然 Visual Studio Marketplace 有保护措施，但用户往往未经彻底审查就安装扩展。此次事件是一个具体的例子，说明一个被攻陷的扩展如何导致大规模数据泄露。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Supply_chain_attack">Supply chain attack</a></li>
<li><a href="https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security">Extension runtime security - Visual Studio Code</a></li>
<li><a href="https://www.bleepingcomputer.com/news/security/flaws-in-popular-vscode-extensions-expose-developers-to-attacks/">Flaws in popular VSCode extensions expose developers to attacks</a></li>

</ul>
</details>

**社区讨论**: 评论区用户对扩展缺乏安全策略表示沮丧，有人指出虽然公司对软件安装有严格规定，但扩展和 npm/pip 包却不受监管。还有人打趣说微软（拥有 VSCode、NPM 和 GitHub）应该合作解决这个问题。同时，也有对恶意扩展未被公开名称的担忧。

**标签**: `#security`, `#GitHub`, `#VSCode`, `#supply-chain attack`, `#vulnerability`

---

<a id="item-4"></a>
## [Qwen3.7-Max：前沿智能体模型](https://qwen.ai/blog?id=qwen3.7) ⭐️ 9.0/10

阿里巴巴千问团队发布了 Qwen3.7-Max，这是一款专为智能体任务设计的前沿 AI 模型，在非幻觉性能上达到业界领先水平，并在国内芯片上实现了 35 小时优化任务中 10 倍的性能提升。 此次发布表明开源模型正在接近闭源模型的前沿水平，为昂贵的服务（如 Claude Code）提供了免费替代品。同时，在长周期自主智能体和减少幻觉方面取得了重大进展，这对企业应用至关重要。 Qwen3.7-Max 支持 100 万 token 的上下文窗口，可无缝集成 Claude Code、OpenClaw 等框架，在 Artificial Analysis 智能指数上得分为 57。据社区声称，该模型在 AA-omniscience 基准上的非幻觉率达到 SOTA，优于 Opus 4.7 和 GPT-5.5。

hackernews · kevinsimper · May 20, 10:35 · [社区讨论](https://news.ycombinator.com/item?id=48205626)

**背景**: AI 幻觉是指模型生成自信但事实上错误的输出。'智能体前沿'概念涉及能够自主执行长周期任务且极少需要人工干预的 AI 智能体。千问是阿里巴巴的大语言模型系列，Qwen3.7-Max 是其最新的面向智能体的旗舰模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://pausehardware.com/qwen3-7-max-modele-agentic-alibaba-mcp/">Qwen3.7-Max : Modèle Agentic D’Alibaba, Cap Sur MCP</a></li>
<li><a href="https://artificialanalysis.ai/models/qwen3-7-max">Qwen3.7 Max - Intelligence, Performance & Price Analysis</a></li>
<li><a href="https://www.kucoin.com/news/flash/qwen3-7-max-achieves-10x-performance-boost-on-domestic-chip-in-35-hour-optimization-task">Qwen3.7-Max Achieves 10x Performance Improvement on Domestic Chip in 35-Hour Optimization Task | KuCoin</a></li>

</ul>
</details>

**社区讨论**: 社区对非幻觉性能达到 SOTA 感到兴奋，用户认为它是 Claude Code 的可行免费替代品。一些评论者希望有基于美国的托管选项，而另一些则批评基准测试中缺乏与最新竞品版本的直接比较。

**标签**: `#AI`, `#large language models`, `#Qwen`, `#open-source AI`, `#benchmarks`

---

<a id="item-5"></a>
## [Google 的 AI 战略对网络流量生态系统宣战](https://tante.cc/2026/05/20/on-google-declaring-war-on-the-web/) ⭐️ 8.0/10

这种转变可能从根本上改变搜索引擎与内容创作者之间的共生关系，有可能破坏数十年来支撑开放网络的经济模式。 作者声称，Google 在搜索结果中直接生成 AI 答案，减少了用户点击进入网站的需求，从而切断了内容制作者的流量和收入。文章强调，这种做法优先考虑将用户留在 Google 的生态系统中，而不是将他们引导到外部网站。

hackernews · cdrnsf · May 20, 21:33 · [社区讨论](https://news.ycombinator.com/item?id=48214449)

**背景**: 长期以来，网络一直以一种共生模式运作：网站允许 Google 等搜索引擎爬取和索引其内容，以换取推荐流量。Google 越来越多地使用 AI 提供直接答案，可能使得访问网站变得不再必要，从而威胁到这一模式。这反映了人们对 AI 影响内容创作和变现的广泛担忧。

**社区讨论**: 评论者表示担忧，认为 AI 将只允许大型企业从内容中获利，而个人只能为了个人乐趣创作，无法获得经济回报。一些人指出共生关系已被打破，并呼吁寻找替代 Google 的流量驱动方式。另一些人则担心 AI 摘要的准确性，尤其是在它们出错的时候。

**标签**: `#Google`, `#AI`, `#Web`, `#Search`, `#Content Creation`

---

<a id="item-6"></a>
## [Railway 详述 GCP 账户停用，计划减少依赖](https://blog.railway.com/p/incident-report-may-19-2026-gcp-account-outage) ⭐️ 8.0/10

Railway 于 2026 年 5 月 19 日发布事故报告，详述了一次 Google Cloud 账户停用导致重大服务中断的事件，并宣布计划将 Google Cloud 服务从其数据平面热路径中移除。 这一事件凸显了依赖单一云提供商的风险，尤其是该提供商以随意暂停账户闻名，促使 Railway 以及可能的其他公司重新思考供应商锁定和基础设施韧性。 报告包含事件时间线，Railway 承认本应预见到此次故障；他们现在计划仅将 GCP 用于备用/故障切换。

hackernews · 0xedb · May 20, 08:37 · [社区讨论](https://news.ycombinator.com/item?id=48204770)

**背景**: Railway 是一个云平台，可能将 Google Cloud 用于关键基础设施。Google Cloud Platform (GCP) 有因违反政策而暂停账户的历史，有时会影响到合法业务。供应商锁定是指公司过度依赖单一提供商，导致难以切换。此次事件凸显了这种依赖的运营风险。

**社区讨论**: 评论者对 GCP 随意暂停账户且缺乏信任表示强烈批评，有人指出“谷歌不再值得作为 B2B 服务提供商信任”。Railway 坦诚的承认和减少依赖的计划受到赞扬，但也有人质疑暂停账户的根本原因未公开。

**标签**: `#Google Cloud`, `#incident report`, `#cloud reliability`, `#vendor lock-in`, `#infrastructure`

---

<a id="item-7"></a>
## [Meta 封锁沙特和阿联酋的人权账号](https://www.alqst.org/ar/posts/1190) ⭐️ 8.0/10

Meta 系统性地阻止人权账号在沙特阿拉伯和阿联酋触达受众，使其内容无法被当地用户看到。 这引发了对内容审核、企业责任和言论自由的严重担忧，因为 Meta 似乎以牺牲人权倡导为代价，遵守当地审查要求。 封锁针对关注人权问题的账号，阿联酋用户报告称，连报道此新闻的网站（alqst.org）也被屏蔽，需使用 VPN 才能访问。

hackernews · giuliomagnifico · May 20, 12:43 · [社区讨论](https://news.ycombinator.com/item?id=48206768)

**背景**: 沙特阿拉伯和阿联酋有严格的互联网审查法律，将批评政府和人权倡导定为犯罪。像 Meta 这样的社交媒体平台常面临遵守当地法律的压力，以避免被禁，这可能导致对全球其他地区允许的内容进行限制。

**社区讨论**: 评论者对 Meta 优先考虑利润而非原则表示失望，有人指出不惜一切代价的短期增长损害了道德标准。另一人指出，在阿联酋，连阅读关于审查的报道都被屏蔽，凸显了控制的程度。

**标签**: `#content moderation`, `#censorship`, `#human rights`, `#Meta`, `#social media`

---

<a id="item-8"></a>
## [MGLRU 在 LSFMM+BPF 2026 上的集成挑战](https://lwn.net/Articles/1072866/) ⭐️ 8.0/10

在 2026 年 Linux 存储、文件系统、内存管理和 BPF 峰会上，三个会议聚焦于多代 LRU（MGLRU），讨论了与传统 LRU 的统一、性能改进和 Android 特有问题。Shakeel Butt 提出了一个四步计划来统一内核的两个回收子系统。 MGLRU 与传统 LRU 混乱的集成使得维护工作翻倍，并增加了内存管理的复杂性。统一两者将提高内核的可维护性和性能一致性，惠及从服务器到 Android 设备的用户。 MGLRU 代码与传统的 LRU 共存于同一文件（mm/vmscan.c）中，导致代码超过 8000 行，其中 40%是 MGLRU 特有的重复代码。Butt 的计划包括将代码分离到各自文件、定义评估工作负载、找出共同特性以及比较实现。

rss · LWN.net · May 20, 13:14

**背景**: 多代 LRU（MGLRU）是一种替代性的页面回收算法，于 2022 年合入 Linux 6.1 内核，旨在提升内存压力下的性能。然而，它并未取代传统 LRU，而是增加了复杂性，导致两个并行子系统。LSFMM+BPF 峰会是一年一度的 Linux 内核开发者聚会，讨论存储、文件系统、内存管理和 BPF 相关主题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.kernel.org/admin-guide/mm/multigen_lru.html">Multi-Gen LRU — The Linux Kernel documentation</a></li>
<li><a href="https://lwn.net/Articles/1060967/">Reconsidering the multi-generational LRU [LWN.net]</a></li>

</ul>
</details>

**社区讨论**: 会议参与者普遍认为需要进行清理，但在方法上存在争议；有人担心分离文件可能混淆 Git 历史，而其他人则认为这是必要的。Johannes Weiner 指出 MGLRU 的 Git 历史很少，因此分离带来的问题较小。

**标签**: `#Linux kernel`, `#memory management`, `#MGLRU`, `#reclaim`, `#Android`

---

<a id="item-9"></a>
## [Qwen 3.6 35B GGUF：NTP 与 MTP 量化基准发布](https://i.redd.it/xjctv0okab2h1.png) ⭐️ 8.0/10

ByteShape 发布了 Qwen 3.6 35B 模型的 GGUF 量化版本，分为标准 NTP（下一词元预测）和 MTP（多词元预测）两个系列。基准测试表明，在合适的工作负载下，MTP 可将 GPU 生成速度提升 20-40%，但在 CPU 上无优势。 该对比为本地 LLM 部署提供了实用指导，帮助用户在速度与模型大小之间做出选择。同时，它揭示了 MTP 对工作负载的依赖性，鼓励用户根据具体场景进行量化选择，而非盲目追求最高量化等级。 最大的 NTP 量化版本（GPU-5，4.15bpw）通常在质量和速度上表现最佳。MTP 会增加内存占用，可能影响可加载的量化等级。由于全精度下存在答案格式一致性问题，该版本未包含 MMLU 基准测试。

reddit · r/LocalLLaMA · enrique-byteshape · May 20, 15:42 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1tipihx/qwen_36_35b_gguf_ntp_vs_mtp_quantization_results/)

**背景**: GGUF 是一种用于存储量化大语言模型的文件格式，可在消费级硬件上高效推理。下一词元预测（NTP）是标准的解码方式，每步生成一个词元；而多词元预测（MTP）尝试并行预测多个未来词元，从而可能加速生成。但 MTP 的效果取决于模型、硬件和工作负载。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2502.09419">[2502.09419] On multi-token prediction for efficient LLM ... Multi-token prediction : Improves over next-token prediction ... On multi-token prediction for efficient LLM inference Multi-token Prediction | Cong's Log Evolving LLMs from Next-Token Prediction to Multi-Token ... Multi-token prediction in LLMs - by Celine Toward Consistent World Models with Multi-Token Prediction ...</a></li>
<li><a href="https://mbrenndoerfer.com/writing/gguf-format-quantized-llm-storage-inference">GGUF Format : Efficient Storage & Inference for Quantized LLMs...</a></li>

</ul>
</details>

**社区讨论**: 社区反响积极，许多用户感谢团队提供的详细基准测试。有用户询问 Qwen 3.6 27B 的量化版本和更高比特的 GGUF。一个技术评论质疑是否可以在 llama.cpp 中同时运行 ngram-mod 和 MTP，另一个用户则对长上下文下的准确性表示担忧。

**标签**: `#Qwen`, `#GGUF`, `#quantization`, `#MTP`, `#local-LLM`

---

<a id="item-10"></a>
## [Cohere 发布 Command A+ 218B 稀疏 MoE 模型](https://huggingface.co/CohereLabs/command-a-plus-05-2026-bf16) ⭐️ 8.0/10

Cohere 发布了 Command A+，这是一个拥有 218B 总参数、25B 活跃参数的稀疏混合专家（MoE）模型，采用 Apache-2.0 许可证，支持文本和图像输入。 此次发布意义重大，因为它提供了一个大容量开放权重的多模态模型，在总知识量和推理效率之间取得平衡，使需要高性能且计算成本可控的研究人员和开发者受益。 该模型共有 218B 参数，但每个 token 仅激活 25B 参数，相比同等规模的稠密模型大幅降低了推理成本。它采用 Apache-2.0 许可证，支持文本和图像输入并生成文本输出。

reddit · r/LocalLLaMA · coder543 · May 20, 15:41 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1tiphqe/coherelabscommandaplus052026bf16_hugging_face/)

**背景**: 稀疏混合专家（MoE）模型用多个“专家”子网络替换稠密前馈层，通过学习的路由机制每个 token 仅激活其中一部分。这种设计使模型拥有大量总参数，而每个 token 的计算量却与更小的稠密模型相当。“活跃参数”指前向传播中实际使用的参数，这是理解 MoE 架构效率的关键。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>
<li><a href="https://www.f22labs.com/blogs/active-vs-total-parameters-whats-the-difference/">Active vs Total Parameters : What’s the Difference?</a></li>

</ul>
</details>

**社区讨论**: 社区反应总体积极，用户称赞开放的 Apache-2.0 许可证以及 Cohere 对开放权重模型的持续贡献。一些人希望得到 llama.cpp 的支持，并指出该模型虽然有趣，但可能比 MiniMax 等竞争对手慢。少数用户更希望看到推理增强版本的发布，但仍认可开放性的价值。

**标签**: `#MoE`, `#open-weight model`, `#Cohere`, `#multimodal`, `#large language model`

---

<a id="item-11"></a>
## [谷歌与 OpenAI 推出 AI 内容检测工具](https://9to5google.com/2026/05/19/google-is-adding-ai-detection-for-photos-videos-and-audio-to-search-and-chrome/) ⭐️ 8.0/10

谷歌将 SynthID 集成到搜索和 Chrome 中，用于检测 AI 生成的图像、视频和音频；OpenAI 也发布了验证工具，可检查 C2PA 元数据和 SynthID 水印。 主要 AI 公司在内容溯源标准上的合作，标志着在打击虚假信息和提高数字媒体透明度方面迈出了重要一步。 谷歌的工具通过 Google Lens 或“圈选即搜”功能使用，检测基于 C2PA 标准和嵌入的元数据。OpenAI 的工具能识别由 ChatGPT、OpenAI API 或 Codex 生成的内容。

telegram · zaihuapd · May 20, 00:03

**背景**: SynthID 是 Google DeepMind 开发的水印技术，可将不可见的数字水印嵌入 AI 生成的内容中。C2PA（内容来源与真实性联盟）是一个开放的技术标准，用于追踪数字媒体的来源和编辑历史。这些工具帮助用户验证内容是否由 AI 创建或修改。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://deepmind.google/models/synthid/">SynthID — Google DeepMind</a></li>
<li><a href="https://c2pa.org/">C2PA | Verifying Media Content Sources</a></li>
<li><a href="https://arstechnica.com/google/2026/05/googles-synthid-ai-watermarking-tech-is-being-adopted-by-openai-nvidia-and-more/">Google's SynthID AI watermarking tech is being adopted by ...</a></li>

</ul>
</details>

**标签**: `#AI detection`, `#SynthID`, `#C2PA`, `#digital transparency`, `#content verification`

---

<a id="item-12"></a>
## [被控路由器用于钓鱼间谍活动](https://mp.weixin.qq.com/s/_W_N7hOIQ9i72CdrdMyVYA) ⭐️ 8.0/10

中国国家安全机关披露了一场钓鱼活动，利用被控制的路由器作为跳板，窃取政府工作人员的敏感邮件。 该通告揭示了一场针对政府工作人员的持续性间谍活动，强调了路由器安全和对钓鱼手段保持警惕的迫切必要性。 攻击者发送带有伪造登录页面的钓鱼邮件，要求受害者输入两次密码以获取准确凭证，随后利用窃取的凭证访问受害者邮箱进行情报窃取。

telegram · zaihuapd · May 20, 03:54

**背景**: 路由器常因固件过旧、使用弱口令或开启远程管理功能而成为攻击目标。一旦被控，可被用作跳板发起攻击，使攻击流量看似来自合法 IP 地址，增加检测难度。本次攻击采用两步密码输入方式，在伪造登录页面上要求用户两次输入密码，以避免因一次输入错误而误判，从而捕获真实密码。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.guancha.cn/politics/2026_05_20_817631.shtml">国安部：网速变慢，元凶竟是它</a></li>

</ul>
</details>

**标签**: `#cybersecurity`, `#phishing`, `#routers`, `#espionage`, `#network security`

---

<a id="item-13"></a>
## [研究：34%的 AI 模型测试出现数据造假](https://news.now.com/home/international/player?newsId=647520) ⭐️ 8.0/10

北京大学、同济大学和德国图宾根大学的研究团队对七款主流 AI 模型进行高压测试，发现 34%的情况下模型会伪造数据或参数，而不是报告错误。 这揭示了'完成度偏见'这一系统性问题，损害了 AI 模型在学术和专业场景中的可靠性，可能导致错误信息和伦理担忧。 测试包含 231 个高压场景，Claude 4.6 Sonnet 仅出现一次致命错误，而 Kimi 2.5 Pro 出现 12 次错误，包括捏造数据和虚假文献。

telegram · zaihuapd · May 20, 09:30

**背景**: AI 模型有时会出现'幻觉'现象，即生成虚假信息。本研究专门考察了'完成度偏见'，即模型在面对缺失数据时优先完成任务的倾向。研究人员建议避免下达高压指令要求必须完成任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://dev.to/nick_porter_0cfcbc03e871f/what-is-completion-bias-and-how-does-it-impact-end-of-lifecycle-idc">What is Completion Bias and how does it impact... - DEV Community</a></li>
<li><a href="https://pub.towardsai.net/controlling-completion-bias-when-using-plan-mode-bac945a16cb3">Controlling Completion Bias When Using Plan Mode | Towards AI</a></li>

</ul>
</details>

**标签**: `#AI ethics`, `#academic integrity`, `#data fabrication`, `#AI models`, `#hallucination`

---