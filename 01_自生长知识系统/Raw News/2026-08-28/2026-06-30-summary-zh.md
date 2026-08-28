---
layout: default
title: "Horizon Summary: 2026-06-30 (ZH)"
date: 2026-06-30
lang: zh
---

> 从 45 条内容中筛选出 14 条重要资讯。

---

1. [vLLM v0.24.0：新增模型与重大优化](#item-1) ⭐️ 9.0/10
2. [谷歌 AI 同行评审处理顶会 1 万篇论文](#item-2) ⭐️ 9.0/10
3. [Qwen 3.6 27B：本地开发的最佳选择？](#item-3) ⭐️ 8.0/10
4. [提议 .self 顶级域名用于免费自托管](#item-4) ⭐️ 8.0/10
5. [Rocket Lab 收购铱星公司，达成战略交易](#item-5) ⭐️ 8.0/10
6. [美国最高法院裁定地理围栏搜查令需受第四修正案保护](#item-6) ⭐️ 8.0/10
7. [韩国计划投资 1 万亿美元于芯片和人形机器人](#item-7) ⭐️ 8.0/10
8. [WATaBoy：将 Game Boy 指令 JIT 编译为 WebAssembly，性能超越原生解释器](#item-8) ⭐️ 8.0/10
9. [CUDA 内核执行流程详解](#item-9) ⭐️ 8.0/10
10. [Ornith-1.0：自我支架式 LLM 用于智能编码](#item-10) ⭐️ 8.0/10
11. [Git 2.55.0 发布，新增 Linux fsmonitor 守护进程和历史命令改进](#item-11) ⭐️ 8.0/10
12. [EML 树被证明是通用逼近器](#item-12) ⭐️ 8.0/10
13. [长鑫存储与腾讯签署 30 亿美元 DRAM 供应协议](#item-13) ⭐️ 8.0/10
14. [特斯拉 FSD v14 Lite 让 HW3 车型获得 HW4 级智驾与自动泊车](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [vLLM v0.24.0：新增模型与重大优化](https://github.com/vllm-project/vllm/releases/tag/v0.24.0) ⭐️ 9.0/10

vLLM v0.24.0 版本发布，共有 571 次提交和 256 位贡献者，新增了对 MiniMax-M3 模型的支持，并对 DeepSeek-V4 进行了深度性能优化，包括 FlashInfer 稀疏索引缓存和集群协作 topK 内核。 该版本显著扩展了 vLLM 支持的模型范围，并展示了其作为高性能推理引擎在前沿大语言模型中的日益重要作用。针对 DeepSeek-V4 的优化提升了吞吐量和延迟，有益于大规模部署。 此版本引入了默认支持量化模型的 Model Runner V2 (MRv2)、新的流式解析引擎用于工具调用解析，以及用于专家并行性的 DeepEP v2 集成。此外，vLLM 不再内部设置 CUDA_VISIBLE_DEVICES，而是改用 device_ids 参数。

github · khluu · 6月29日 19:41

**背景**: vLLM 是一个开源的大语言模型推理引擎，专为高吞吐量和低延迟设计。它采用 PagedAttention 高效管理内存，并支持多种模型。此版本的优化利用了 FlashInfer 进行稀疏注意力、MXFP4 进行低精度计算等技术，对于处理 DeepSeek-V4 和 MiniMax-M3 等大型模型至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/flashinfer-ai/flashinfer">GitHub - flashinfer-ai/flashinfer: FlashInfer: Kernel Library for LLM Serving · GitHub</a></li>
<li><a href="https://en.wikipedia.org/wiki/MXFP4">MXFP4</a></li>

</ul>
</details>

**标签**: `#LLM`, `#inference`, `#vLLM`, `#open-source`, `#AI`

---

<a id="item-2"></a>
## [谷歌 AI 同行评审处理顶会 1 万篇论文](https://www.reddit.com/r/MachineLearning/comments/1uio9rb/googles_agentic_peerreviewer_handled_10k_papers/) ⭐️ 9.0/10

谷歌在 ICML 和 STOC 部署了一个代理式 AI 同行评审系统，以 30 分钟周转时间处理了约 10,000 篇论文。新研究论文显示，它比零样本提示多检测出 34%的数学错误。 这展示了一种可扩展的自动化科学同行评审方法，有望减少评审瓶颈并提高错误检测能力。它为会议规模下的 AI 辅助评审开创了先例，可能改变研究的评估方式。 该系统采用代理式框架，通过迭代推理结合检索和验证步骤来评审论文。它比基线零样本提示（即要求模型在没有额外指导的情况下进行评审）实现了 34%的改进。

reddit · r/MachineLearning · /u/Justgototheeffinmoon · 6月29日 10:05

**背景**: 像 ICML 和 STOC 这样的大型计算机科学会议的同行评审传统上需要数百名人类评审员，耗时数周。零样本提示是指使用大型语言模型在没有任务特定示例的情况下回答问题。代理式 AI 系统旨在自主规划和执行多步任务，例如获取论文详情、验证数学论断以及综合反馈。

**标签**: `#AI`, `#peer review`, `#conference`, `#automation`, `#machine learning`

---

<a id="item-3"></a>
## [Qwen 3.6 27B：本地开发的最佳选择？](https://quesma.com/blog/qwen-36-is-awesome/) ⭐️ 8.0/10

Quesma 的一篇博客文章认为 Qwen 3.6 27B 是本地开发的理想模型，声称它在性能和资源需求之间取得了良好平衡。 这一推荐具有重要意义，因为本地 LLM 部署可以增强隐私并降低延迟，但高昂的硬件成本（例如，128GB MacBook Pro 售价 6699 美元）以及缺乏真实代码库测试使得它对许多开发者来说不切实际。 Qwen 3.6 27B 密集模型在 Q4_K_M 量化下需要约 18GB VRAM，推荐使用 128GB MacBook Pro 来舒适运行，但社区评论指出，即使使用这样的硬件，在密集使用中仍会出现发热和噪音问题。

hackernews · stared · 6月29日 17:05 · [社区讨论](https://news.ycombinator.com/item?id=48721903)

**背景**: 本地 LLM 部署是指在个人硬件上运行大型语言模型，而非云服务器，提供隐私和离线能力，但需要大量的 GPU 内存和计算资源。Qwen 3.6 是阿里巴巴 Qwen 团队的最新模型系列，包括 27B 和 35B 参数版本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.runyard.dev/blog/qwen3-6-local-llm-guide-april-2026">Qwen3.6: The 27 B Model That Outperforms a 397- Billion - Parameter ...</a></li>
<li><a href="https://huggingface.co/Qwen/Qwen3.6-35B-A3B">Qwen/Qwen3.6-35B-A3B · Hugging Face</a></li>

</ul>
</details>

**社区讨论**: 社区评论对实际可行性表示怀疑，指出推荐的硬件非常昂贵（高达 6699 美元），而 OpenRouter 等云 API 可以更便宜地运行更大的模型。其他人指出，文章中的示例是新项目，不代表处理复杂的现有代码库。

**标签**: `#local LLM`, `#Qwen 3.6`, `#model deployment`, `#community discussion`

---

<a id="item-4"></a>
## [提议 .self 顶级域名用于免费自托管](https://hccf.onmy.cloud/2026/06/21/reclaiming-our-digital-selves-hccfs-vision-for-a-human-centered-top-level-domain/) ⭐️ 8.0/10

有人提议创建新的 .self 顶级域名，为个人提供免费域名用于自托管，旨在重获数字自主权。 如果实现，.self 可能降低自托管门槛并推动网络托管去中心化，但面临滥用防范、身份验证和可持续资金等重大挑战。 该提案包括每人一个免费域名，禁止停放、抢注和转售，但执行机制尚不明确，尤其是区分合法使用与滥用的方法。

hackernews · HumanCCF · 6月29日 19:49 · [社区讨论](https://news.ycombinator.com/item?id=48724230)

**背景**: 顶级域名是域名最后一部分，如 .com 或 .org。自托管是指运行自己的服务器来托管网站、电子邮件或其他服务，而非使用第三方提供商。.self 顶级域名将是专门为个人托管其数字存在而设计的通用顶级域名。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Top-level_domain">Top-level domain - Wikipedia</a></li>
<li><a href="https://blog.technitium.com/2022/06/how-to-self-host-your-own-domain-name.html">Technitium Blog: How To Self Host Your Own Domain Name</a></li>
<li><a href="https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains">List of Internet top-level domains - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区评论观点不一：有人回忆起免费 .tk 域名遭滥用的情况，有人建议采用基于声誉的系统或身份证明，还有许多人质疑经济可持续性和反抢注的执行力。

**标签**: `#TLD`, `#self-hosting`, `#domain names`, `#internet governance`, `#digital identity`

---

<a id="item-5"></a>
## [Rocket Lab 收购铱星公司，达成战略交易](https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-acquire-iridium-historic-deal-creating-fully) ⭐️ 8.0/10

Rocket Lab 宣布收购铱星公司（Iridium），获得其卫星星座和频谱权。这笔历史性交易巩固了 Rocket Lab 在航天行业的地位。 此次收购使 Rocket Lab 能够利用铱星现有的卫星网络和频谱，使其在卫星通信和发射服务方面成为更有力的竞争者。同时，这也提供了稳定的收入来源和发射需求，类似于 SpaceX 利用 Starlink 的模式。 交易包括铱星的卫星星座和关键的频谱权。Rocket Lab 还获得了铱星盈利的卫星业务以及一系列常规发射合同。

hackernews · everfrustrated · 6月29日 14:09 · [社区讨论](https://news.ycombinator.com/item?id=48719485)

**背景**: Rocket Lab 是一家航天发射和卫星制造公司，最初在新西兰创立，如今已归美国所有。铱星运营着一个由 66 颗低地球轨道卫星组成的星座，提供全球语音和数据通信。对于发射服务商来说，收购这样一个星座实属罕见。

**社区讨论**: 评论者认为此举是明智的战略举措，类似于 SpaceX 利用 Starlink 保证发射需求。有人对太空垃圾表示担忧，也有人注意到 Rocket Lab 从新西兰起源转向美国所有权的变化。

**标签**: `#space`, `#satellite`, `#acquisition`, `#Rocket Lab`, `#Iridium`

---

<a id="item-6"></a>
## [美国最高法院裁定地理围栏搜查令需受第四修正案保护](https://www.theguardian.com/us-news/2026/jun/29/supreme-court-geofence-warrants-case-decision) ⭐️ 8.0/10

美国最高法院裁定，执法部门利用地理围栏搜查令从谷歌获取手机位置数据的行为构成第四修正案下的搜查，需要具备可能原因并取得搜查令。该裁决涉及 2019 年弗吉尼亚州一起银行抢劫案。 这一里程碑式的裁决加强了数字隐私保护，要求执法部门在获取批量位置数据前必须满足宪法标准。它为法院如何处理反向位置搜查令设定了先例，并限制了对无辜旁观者的无证监控。 该地理围栏搜查令要求谷歌提供抢劫案发生前后 30 分钟内、银行周边 150 米范围内设备的位置数据。法院认为，获取这些汇总的位置历史侵犯了合理的隐私期待，驳回了公共场所数据不受保护的主张。

hackernews · cdrnsf · 6月29日 15:54 · [社区讨论](https://news.ycombinator.com/item?id=48720924)

**背景**: 地理围栏搜查令，又称反向位置搜查令，强制要求谷歌等公司识别在特定时间段内位于指定地理区域内的所有设备。谷歌的 Sensorvault 数据库存储着数百万用户的历史位置数据。第四修正案保护公民免受不合理的搜查和扣押；此前如 Riley 诉 California 案等裁决已承认手机包含高度私密信息。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Geofence_warrant">Geofence warrant</a></li>
<li><a href="https://www.scotusblog.com/2026/06/court-rules-that-law-enforcements-use-of-geofence-warrant-was-a-search/">Court rules that law enforcement’s use of “geofence warrant ...</a></li>
<li><a href="https://www.congress.gov/crs_external_products/LSB/PDF/LSB11274/LSB11274.4.pdf">Geofence Warrants and the Fourth Amendment - Congress.gov</a></li>

</ul>
</details>

**社区讨论**: 评论者指出该裁决对其他监控技术（如 Flock 摄像头）的影响，质疑访问其数据是否也需要搜查令。一些人赞赏法院在意见书中详细引用来源的做法，另一些人则将其与历史上的窃听先例相类比，突显执法工具与隐私权之间的持续张力。

**标签**: `#supreme-court`, `#geofence-warrants`, `#privacy`, `#law-enforcement`, `#fourth-amendment`

---

<a id="item-7"></a>
## [韩国计划投资 1 万亿美元于芯片和人形机器人](https://arstechnica.com/ai/2026/06/south-korea-to-spend-1t-on-more-memory-chip-production-and-humanoid-robots/) ⭐️ 8.0/10

韩国宣布了一项 1 万亿美元的投资计划，旨在扩大存储芯片生产并开发人形机器人，以推动其半导体和人工智能机器人产业的发展。 这一巨额政府投资标志着在商品化存储芯片和投机性人形机器人上的战略押注，可能重塑全球供应链并加速人形机器人的商业化。 该投资涵盖 DRAM 和 NAND 等存储芯片以及人形机器人开发，将两个看似不相关的领域结合在一起。这一宣布引发了不同的反应，一些人质疑将存储芯片生产与人形机器人联系起来的理由。

hackernews · jnord · 6月29日 22:21 · [社区讨论](https://news.ycombinator.com/item?id=48726102)

**背景**: 存储芯片是电子产品中的关键组件，韩国通过三星和 SK 海力士等公司主导全球市场。人形机器人是人工智能机器人领域的新兴方向，吸引了全球政府和公司的大量投资，但其实际外形仍存在争议。

**社区讨论**: 评论者对于将存储芯片和人形机器人结合表示怀疑，将其比作‘杂货和舞蹈课’。一些人质疑人形机器人的外形，认为存在更优设计，而另一些人则好奇为何全球都在匆忙投入人形机器人。

**标签**: `#semiconductors`, `#humanoid robots`, `#investment`, `#South Korea`, `#AI hardware`

---

<a id="item-8"></a>
## [WATaBoy：将 Game Boy 指令 JIT 编译为 WebAssembly，性能超越原生解释器](https://humphri.es/blog/WATaBoy/) ⭐️ 8.0/10

名为 WATaBoy 的项目证明，将 Game Boy CPU 指令 JIT 编译为 WebAssembly 可以获得比原生解释器更快的性能。该方法利用了 Web 浏览器已有的 WebAssembly JIT 编译基础架构。 这具有重要意义，因为它展示了一种新颖的方法来克服平台限制（例如 iOS 禁止 JIT 编译），即使用 WebAssembly 作为可移植的高性能目标。这有望在受限平台上实现更流畅的模拟，并启发其他复古系统的类似方案。 项目指出，原生解释器的开销大约为 1000%，而 WebAssembly JIT 的开销约为 20%，因此 JIT 方法更快。然而，在该工作负载下，Firefox 比 Chrome/Safari 慢约 25%。

hackernews · energeticbark · 6月29日 15:02 · [社区讨论](https://news.ycombinator.com/item?id=48720190)

**背景**: JIT（即时编译）在运行时将代码翻译为本地机器码以提高性能。WebAssembly（WASM）是一种低级二进制格式，旨在在 Web 浏览器中实现接近原生的速度。传统上，Game Boy 模拟器使用解释器或原生 JIT，但由于安全限制，这些方法在某些平台（如 iOS）上可能不被允许。WATaBoy 则从 Game Boy 指令生成 WASM，并依赖浏览器的 WASM JIT 引擎。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://wingolog.org/archives/2022/08/18/just-in-time-code-generation-within-webassembly">just-in-time code generation within webassembly — wingolog</a></li>

</ul>
</details>

**社区讨论**: 评论者称赞该项目是令人印象深刻的本科学位作品，并指出利用浏览器的 JIT 绕过 iOS 限制非常巧妙。有人指出 Firefox 的 WASM JIT 比 Chrome/Safari 慢。还有人评论道，鉴于开销差异，超越原生解释器是预料之中的事，但拥有一个基于 WASM 的 Game Boy JIT 运行时仍然很酷。

**标签**: `#JIT`, `#WebAssembly`, `#emulation`, `#Game Boy`, `#performance`

---

<a id="item-9"></a>
## [CUDA 内核执行流程详解](https://fergusfinn.com/blog/what-happens-when-you-run-a-gpu-kernel/) ⭐️ 8.0/10

这篇文章详细解析了启动 CUDA 内核时从 CPU 到 GPU 的路径，涵盖了驱动交互、硬件通信和 warp 调度。 这填补了知识空白，因为许多解释停留在内核/块/warp 层面，而本文将 CUDA 启动语法与实际 GPU 提交连接起来，对 GPU 计算和 HPC 从业者具有重要价值。 文章涉及门铃机制、队列管理描述符（QMD）和 warp 资格等主题；还解释了默认流中的信号量处理。

hackernews · mezark · 6月29日 13:11 · [社区讨论](https://news.ycombinator.com/item?id=48718863)

**背景**: CUDA 是一种并行计算平台，允许程序员使用 GPU 进行通用处理。启动 CUDA 内核涉及 CPU 通过驱动程序发出命令，驱动程序与 GPU 硬件进行通信。然后，GPU 调度器管理 warp（32 个线程的组）并在流多处理器上调度它们的执行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://stevengong.co/notes/Warp-Scheduling">Warp Scheduling (GPU Thread Scheduling) - stevengong.co</a></li>

</ul>
</details>

**社区讨论**: 评论表达了对文章深度的赞赏，特别是门铃和 QMD 的解释将 CUDA 语法与 GPU 硬件联系起来。一位读者指出 CUDA 默认流中的隐式同步比 Vulkan 的显式方法更简单。总体而言，读者认为这篇文章教育性很强，填补了现有资源的空白。

**标签**: `#CUDA`, `#GPU computing`, `#HPC`, `#kernel execution`, `#systems programming`

---

<a id="item-10"></a>
## [Ornith-1.0：自我支架式 LLM 用于智能编码](https://simonwillison.net/2026/Jun/29/ornith/#atom-everything) ⭐️ 8.0/10

DeepReinforce 发布了 Ornith-1.0 模型系列，采用 MIT 许可证开放权重，在编码基准测试中达到同类开源模型的最高性能，参数规模从 9B 到 397B 不等。 该发布推动了开源智能编码能力的发展，使开发者能够在本地运行强大的编码助手而无需锁定特定供应商，自我支架技术可能提高多步骤任务的可靠性。 模型基于预训练的 Gemma 4（Apache 2.0）和 Qwen 3.5（Apache 2.0）构建，确保许可证兼容性，包括密集和混合专家两种变体。作者测试了 35B 的 GGUF 量化模型，报告在智能编码任务上表现强劲。

rss · Simon Willison · 6月29日 16:17

**背景**: 自我支架（self-scaffolding）指的是 LLM 自主生成并遵循自己的推理步骤或工具使用计划的能力，无需外部提示即可提升复杂智能任务的性能。混合专家（MoE）是一种架构，每次只激活一部分参数，从而在较低计算成本下实现更大的有效模型规模。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://simonwillison.net/2026/Jun/29/ornith/">Ornith-1.0: Self-Scaffolding LLMs for Agentic Coding</a></li>
<li><a href="https://essamamdani.com/blog/ornith-1-0-self-scaffolding-llm-coding-2026">Ornith-1.0: The Self-Scaffolding LLM That Teaches Itself to ...</a></li>

</ul>
</details>

**标签**: `#LLM`, `#coding`, `#open-source`, `#agentic AI`, `#model release`

---

<a id="item-11"></a>
## [Git 2.55.0 发布，新增 Linux fsmonitor 守护进程和历史命令改进](https://lwn.net/Articles/1080188/) ⭐️ 8.0/10

Git 2.55.0 已发布，新增了实验性 'git history' 命令的功能，并为 Linux 系统添加了 fsmonitor 守护进程。此版本包含来自 100 位贡献者的非合并提交，其中 33 人是首次贡献者。 此次发布通过 fsmonitor 守护进程提升了 Linux 用户的性能，可显著加速 'git status' 等命令。增强后的 'git history' 命令提供了一种更交互式的方式来审查和修改提交历史，提高了开发者的效率。 fsmonitor 守护进程通过监视工作目录的文件变化来工作，使 Git 避免扫描整个目录树。'git history' 命令仍处于实验阶段；用户应注意其接口可能在未来版本中发生变化。

rss · LWN.net · 6月29日 20:22

**背景**: Git 是一个分布式版本控制系统，广泛应用于软件开发中跟踪源代码变化。fsmonitor（文件系统监视器）守护进程是一个长期运行的后台进程，它缓存文件系统变化，以提高需要检查工作树状态的命令的性能。'git history' 命令提供了一个交互式的、基于补丁的界面来审查和修改提交历史，补充了现有的 'git rebase -i' 等工具。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://git-scm.com/docs/git-fsmonitor--daemon">Git - git-fsmonitor--daemon Documentation</a></li>
<li><a href="https://git-scm.com/docs/git-history">Git - git-history Documentation</a></li>

</ul>
</details>

**标签**: `#Git`, `#Version Control`, `#Open Source`, `#Release`

---

<a id="item-12"></a>
## [EML 树被证明是通用逼近器](https://www.reddit.com/r/MachineLearning/comments/1uipl1t/eml_trees_are_universal_approximators_r/) ⭐️ 8.0/10

一篇新论文证明，由 EML（指数-减法-对数）初等函数组合而成的 EML 树是连续函数的通用逼近器。 这确立了 EML 树作为函数逼近的神经网络的理论基础替代方案，对可解释机器学习和符号计算具有潜在影响。 该证明构建了二元运算、多项式、双曲正切和单位划分的 EML 表示，并将它们用作类似乐高的积木。通过对数域的技术挑战通过基于符号的分解和仿射映射来解决。

reddit · r/MachineLearning · /u/JoeGermany · 6月29日 11:16

**背景**: EML 函数（指数-减法-对数）是一个单一的二元运算符，通过重复组合可以表达任何标准的实数初等函数。通用逼近意味着一个函数类可以在紧集上以任意精度逼近任何连续函数。这一结果与神经网络的通用逼近定理平行，但使用了不同的原语。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2606.23179">[2606.23179] EML Trees Are Universal Approximators</a></li>
<li><a href="https://www.stylewarning.com/posts/not-all-elementary/">Not all elementary functions can be expressed with exp-minus-log</a></li>

</ul>
</details>

**标签**: `#universal approximation`, `#function approximation`, `#EML trees`, `#machine learning theory`

---

<a id="item-13"></a>
## [长鑫存储与腾讯签署 30 亿美元 DRAM 供应协议](https://www.reuters.com/world/china/chinas-cxmt-wins-3-billion-memory-supply-deal-with-tencent-sources-say-2026-06-29/) ⭐️ 8.0/10

长鑫存储（CXMT）与腾讯签署了一项价值超过 200 亿元人民币（约 29.4 亿美元）的多年期 DRAM 供应协议，涵盖服务器内存芯片，协议期最长可达五年。 该协议增强了中国半导体自给能力，并为长鑫存储提供了重要客户，未来可能扩展至阿里云、字节跳动和小米等其他中国互联网公司。 据悉协议期限为 3 至 5 年，长鑫存储还在与阿里云、字节跳动和小米等公司洽谈类似协议。

telegram · zaihuapd · 6月29日 09:31

**背景**: DRAM（动态随机存取存储器）是一种易失性半导体存储器，广泛用于服务器和电脑中。长鑫存储是中国领先的 DRAM 制造商，在减少对三星、SK 海力士和美光等外国内存供应商依赖的努力中扮演关键角色。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Dynamic_random-access_memory">Dynamic random-access memory - Wikipedia</a></li>

</ul>
</details>

**标签**: `#DRAM`, `#半导体`, `#长鑫存储`, `#腾讯`, `#供应链`

---

<a id="item-14"></a>
## [特斯拉 FSD v14 Lite 让 HW3 车型获得 HW4 级智驾与自动泊车](https://x.com/Tesla_AI/status/2071592820889260101) ⭐️ 8.0/10

6 月 29 日，特斯拉发布了 FSD v14 Lite，将 HW4 级 V14 的智能提炼到 HW3 硬件上，使 HW3 车辆能够使用此前仅 HW4 拥有的强化学习和离线模型，并首次引入停车、出库和倒车功能。 此次更新通过将尖端智驾能力带给数百万无需硬件升级的现有车主，显著延长了老旧 HW3 车型的使用寿命。它展示了特斯拉在模型蒸馏方面的工程技术能力，并强化了其在跨硬件世代持续软件改进的承诺。 FSD v14 Lite 改进了导航处理、并线、行人交互、交通灯响应和车辆切入应对，同时减少了不必要的刹车，提升了转向平顺性和车道居中表现。更新还增加了全时段速度配置文件自定义，以个性化驾驶风格。

telegram · zaihuapd · 6月30日 02:26

**背景**: 模型蒸馏将知识从大型、强大的模型迁移到较小的模型，使较小模型能在性能更低的硬件上运行，同时保留大型模型的大部分性能。离线强化学习利用预先收集的数据集训练智能体，无需实时交互，从而更安全高效地更新模型。HW3 和 HW4 是指特斯拉定制的自动驾驶计算机硬件代次，HW4 提供更高的计算能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Knowledge_distillation">Knowledge distillation - Wikipedia</a></li>
<li><a href="https://openai.com/index/api-model-distillation/">Model Distillation in the API | OpenAI</a></li>

</ul>
</details>

**标签**: `#Tesla`, `#FSD`, `#autonomous driving`, `#reinforcement learning`, `#EV`

---