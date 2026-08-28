---
layout: default
title: "Horizon Summary: 2026-07-25 (ZH)"
date: 2026-07-25
lang: zh
---

> 从 31 条内容中筛选出 8 条重要资讯。

---

1. [vLLM v0.26.0 发布，支持 Inkling 模型并优化 DeepSeek-V4](#item-1) ⭐️ 9.0/10
2. [SGLang v0.5.16 新增 DSpark 投机解码和 Inkling 支持](#item-2) ⭐️ 9.0/10
3. [开放权重 AI：机器学习领域的 Kubernetes？](#item-3) ⭐️ 9.0/10
4. [Anthropic 发布 Claude Opus 5，成本仅为前沿 AI 的一半](#item-4) ⭐️ 9.0/10
5. [安卓或限制设备内 ADB，引发开发者争论](#item-5) ⭐️ 8.0/10
6. [Ruff v0.16.0 默认启用 413 条规则，导致 CI 管道出错](#item-6) ⭐️ 8.0/10
7. [AMD 挑战 NVIDIA CUDA 护城河：软件与生产瓶颈](#item-7) ⭐️ 8.0/10
8. [GNU C 库 2.44 发布，引入系统级可调参数配置](#item-8) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [vLLM v0.26.0 发布，支持 Inkling 模型并优化 DeepSeek-V4](https://github.com/vllm-project/vllm/releases/tag/v0.26.0) ⭐️ 9.0/10

vLLM v0.26.0 正式发布，包含 212 位贡献者的 411 次提交，新增对 Inkling 模型系列的全面支持、DeepSeek-V4 的性能优化、fp32 lm\_head 支持、灵活的后端注意力机制以及 KV 卸载增强。 该版本通过支持 Inkling 等前沿模型并为 DeepSeek-V4 带来显著性能提升，巩固了 vLLM 作为领先 LLM 推理引擎的地位，对大规模 AI 部署至关重要。 Inkling 系列支持分段 CUDA 图、Hopper FA4 相对注意力、MTP 投机解码（每步 1 个草稿 token）、LoRA 和 ModelOpt NVFP4 量化。DeepSeek-V4 优化包括专用路由内核（端到端 TPOT 提升 2.94%）和 fused\_topk\_bias（内核加速 1.5–2 倍），fp32 lm\_head 现可通过 head\_dtype 选项用于生成模型。

github · khluu · 7月25日 10:38

**背景**: vLLM 是一个用于高吞吐、低延迟 LLM 推理的开源库。Inkling 模型是 Thinking Machines Lab 开发的万亿参数多模态混合专家 Transformer，支持文本、图像和音频输入，上下文窗口达 100 万 token。DeepSeek-V4 是一个大型语言模型，通过高效路由和注意力内核获得性能提升。投机解码技术如 MTP（多 token 预测）通过每步预测多个 token 来加速生成。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://vllm.ai/blog/2026-07-15-inkling">TML Inkling on vLLM: Day-0 Support with Optimized Performance | vLLM Blog</a></li>
<li><a href="https://arxiv.org/html/2603.05451v1">FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling</a></li>
<li><a href="https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp/">MTP (Multi-Token Prediction) - vLLM</a></li>

</ul>
</details>

**标签**: `#vLLM`, `#LLM inference`, `#release`, `#DeepSeek`, `#optimization`

---

<a id="item-2"></a>
## [SGLang v0.5.16 新增 DSpark 投机解码和 Inkling 支持](https://github.com/sgl-project/sglang/releases/tag/v0.5.16) ⭐️ 9.0/10

SGLang v0.5.16 引入了 DSpark，一种基于置信度的投机解码算法，在 DeepSeek-V4-Pro 上达到 383.7 tok/s，并新增了对 Inkling 的支持，这是一个拥有 975B 参数、1M token 上下文的多模态 MoE 模型。 DSpark 无需重新训练即可显著提升 LLM 推理吞吐量，使 DeepSeek-V4 等大型模型速度提升高达 85%，而 Inkling 支持则能够部署具有超长上下文的尖端多模态 MoE 模型，惠及实际应用。 DSpark 使用半自回归草稿和基于置信度的验证窗口大小调整，而 Inkling 采用混合注意力机制（滑动窗口、全注意力和 Mamba2）以及 NVFP4 MoE。该版本还移除了实验性的 QServe 和 FBGEMM FP8 量化路径。

github · Qiaolin-Yu · 7月25日 00:13

**背景**: 投机解码通过使用较小的草稿模型生成多个 token，再由目标模型验证，从而加速 LLM 推理。混合专家模型（MoE）每个 token 仅激活部分参数，提高了效率。NVFP4 是一种 4 位浮点格式，专为 NVIDIA Blackwell GPU 上的高效推理而设计。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2607.05147">[2607.05147] DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation</a></li>
<li><a href="https://www.techtimes.com/articles/319236/20260628/deepseek-releases-dspark-speculative-decoding-makes-v4-85-percent-faster.htm">DeepSeek Releases DSpark: Speculative Decoding Makes V4 Up to 85 Percent Faster</a></li>
<li><a href="https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/">Introducing NVFP4 for Efficient and Accurate Low-Precision Inference | NVIDIA Technical Blog</a></li>

</ul>
</details>

**标签**: `#LLM inference`, `#speculative decoding`, `#MoE`, `#multimodal`, `#SGLang`

---

<a id="item-3"></a>
## [开放权重 AI：机器学习领域的 Kubernetes？](https://tobi.knaup.me/2026-07-25-open-weight-ai-is-having-its-kubernetes-moment/) ⭐️ 9.0/10

一篇新文章将开放权重 AI 模型与 Kubernetes 进行了引人注目的类比，指出开放模型正成为 AI 基础设施的标准平台，就像 Kubernetes 成为容器编排的标准一样。 这一比较突显了一种潜在的范式转变：开放权重模型可能主导 AI 部署，实现更广泛的访问、更低的成本和更大的社区协作，类似 Kubernetes 改变云原生计算的方式。 文章指出，美国实验室需要以宽松许可证发布前沿级别的开放权重模型，供初创企业在此基础上构建，这呼应了 Kubernetes 成功的路径。然而，在治理、安全性以及围绕模型来源的地缘政治紧张方面仍存在挑战。

hackernews · tknaup · 7月25日 14:49 · [社区讨论](https://news.ycombinator.com/item?id=49048034)

**背景**: 开放权重 AI 指的是训练参数（权重）公开的模型，任何人都可以下载、微调并在自己的硬件上部署。Kubernetes 是一个用于自动化容器化应用程序部署、扩展和管理的开源系统，由 Google 捐赠给云原生计算基金会后成为行业标准。这一类比表明，开放权重模型可能遵循类似的发展轨迹，成为 AI 的默认基础设施层。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/pulse/open-weight-ai-what-we-finally-opened-bonnet-nicolas-pistorio-n3ulf">Open - weight AI : what if we finally opened the bonnet ?</a></li>
<li><a href="https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/">Open Weights and American AI Leadership</a></li>
<li><a href="https://asibiont.com/en/blog/pochemu-strategiya-otkrytykh-vesov-kitaya-pobezhdaet-v-gonke-ii">China&#x27;s Open - Weights AI Strategy Is Winning: What... — ASI Biont Blog</a></li>

</ul>
</details>

**社区讨论**: 评论者就按来源禁止中国模型的可行性展开辩论，指出权重只是数字，无法按地理分类。其他人讨论了 tokenomics，希望开放权重模型能稳定推理定价。还有人呼吁像 Linux 一样进行协作模型开发，公司共同贡献于一个开放的共享模型。

**标签**: `#open-weight`, `#AI`, `#Kubernetes`, `#open source`, `#machine learning`

---

<a id="item-4"></a>
## [Anthropic 发布 Claude Opus 5，成本仅为前沿 AI 的一半](https://simonwillison.net/2026/Jul/24/introducing-claude-opus-5/#atom-everything) ⭐️ 9.0/10

Anthropic 发布了新模型 Claude Opus 5，其性能接近前沿智能水平，价格仅为 Claude Fable 5 的一半。该模型目前在 Artificial Analysis 排行榜上位居首位，甚至超过了 Fable 5。 此次发布大幅降低了高端 AI 能力的成本，使更多用户能够使用前沿级别的性能。同时证明，专注于安全的训练可以在不牺牲通用智能的情况下限制有害能力。 Claude Opus 5 的定价与 Opus 4.8 相同，并提供价格翻倍的快速模式。它在网络安全漏洞发现方面有改进，但刻意避免在利用漏洞方面进行训练，因此在该领域仍落后于 Mythos 5。

rss · Simon Willison · 7月24日 23:48

**背景**: 前沿智能（Frontier Intelligence）指在能力上达到最前沿水平的 AI 模型，通常通过大规模模型和高计算成本实现。Anthropic 的 Claude 模型系列包含多个层级：Opus 是旗舰型号，而 Fable 是能力更强但价格更高的变体，专为前沿任务设计。新发布的 Opus 5 旨在平衡成本与性能，并延续 Anthropic 对安全的重视，刻意限制其网络利用能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@eng.fadishaar/gemma-4-frontier-ai-intelligence-that-runs-on-your-laptop-633990c9dd68">Gemma 4: Frontier AI Intelligence That Runs on Your Laptop | Medium</a></li>
<li><a href="https://artificialanalysis.ai/leaderboards/models">LLM Leaderboard - Comparison of AI models from OpenAI, Anthropic...</a></li>

</ul>
</details>

**社区讨论**: 早期社区反响积极，该模型在 Artificial Analysis 排行榜上领先。作者还注意到其主动行为，例如模型在无法直接查看图纸的情况下，自主构建计算机视觉管线来解析图像。

**标签**: `#AI`, `#Anthropic`, `#Claude`, `#language models`

---

<a id="item-5"></a>
## [安卓或限制设备内 ADB，引发开发者争论](https://kitsumed.github.io/blog/posts/android-may-soon-restrict-on-device-adb/) ⭐️ 8.0/10

安卓可能很快限制设备内 ADB 访问，限制开发者直接在设备上运行 ADB 命令的能力。该提议正在讨论中，引发了关于安全性与开发者灵活性的辩论。 这一变化可能严重影响依赖设备内 ADB 进行调试和自动化的开发者。它反映了谷歌安全强化与开发者社区需求之间的持续紧张关系。 限制似乎针对的是网络暴露的 ADB，而不仅仅是 USB。社区成员指出，利用此向量需要同时启用开发者选项和远程 ADB，对典型用户来说不太可能。

hackernews · shscs911 · 7月25日 06:57 · [社区讨论](https://news.ycombinator.com/item?id=49045159)

**背景**: Android Debug Bridge \(ADB\) 是一个用于调试安卓设备的命令行工具。设备内 ADB 允许通过终端或自动化应用直接在设备上运行命令。虽然功能强大，但 ADB 暴露时可能被恶意软件利用，促使谷歌考虑限制。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Android_Debug_Bridge">Android Debug Bridge</a></li>
<li><a href="https://www.androidpolice.com/use-wireless-adb-android-phone/">How to use wireless ADB on your Android phone or tablet</a></li>

</ul>
</details>

**社区讨论**: 社区反应不一：一些人认为该限制不必要，因为攻击向量不现实；另一些人则认为这是合理的安全步骤。一个显著的建议是允许将 ADB 限制在 VPN 等特定接口。

**标签**: `#Android`, `#ADB`, `#security`, `#developer tools`, `#privacy`

---

<a id="item-6"></a>
## [Ruff v0.16.0 默认启用 413 条规则，导致 CI 管道出错](https://simonwillison.net/2026/Jul/25/ruff/#atom-everything) ⭐️ 8.0/10

Ruff v0.16.0 于 2026 年 7 月 23 日发布，将其默认启用的规则从 59 条大幅增加到 413 条，导致使用未固定 Ruff 依赖的项目出现 CI 失败。 这一变化显著提高了 Python 代码质量的门槛，自动捕获许多严重问题，但也可能破坏那些依赖先前默认规则集且未显式配置的团队现有工作流程。 自 v0.1.0 以来，Ruff 的总规则数从 708 条增加到 968 条，新的默认规则包括检测语法错误和即时运行时错误的规则。Simon Willison 报告在 sqlite-utils 中发现了 1618 个错误，其中 1538 个通过 --unsafe-fixes 自动修复。

rss · Simon Willison · 7月25日 22:44

**背景**: Ruff 是由 Astral 开发的高性能 Python 代码检查工具，比 Pylint 和 Black 等传统工具快 10 到 100 倍。它用一个快速工具替代了多个依赖项。工具的默认规则集很重要，因为它决定了在没有用户配置的情况下自动运行哪些检查。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://astral.sh/ruff">Ruff , an extremely fast Python linter | Astral</a></li>
<li><a href="https://github.com/astral-sh/ruff">GitHub - astral-sh/ ruff : An extremely fast Python linter and code...</a></li>

</ul>
</details>

**标签**: `#Python`, `#linting`, `#Ruff`, `#AST`, `#developer tools`

---

<a id="item-7"></a>
## [AMD 挑战 NVIDIA CUDA 护城河：软件与生产瓶颈](https://newsletter.semianalysis.com/p/can-amd-break-the-cuda-moat-amd-advancing) ⭐️ 8.0/10

一份详细分析揭示了 AMD 在竞争 NVIDIA CUDA 生态系统中的内部困境，包括不稳定的开发集群、用于软件质量的代理内核生成、Helios MI455X 系统的生产爬坡问题，以及通过财务工程提供高达 105%折扣以激励采用的策略。 如果 AMD 无法提升软件质量和生产可扩展性，它可能无法撼动 NVIDIA 的 CUDA 主导地位，而这对于竞争 AI 硬件至关重要。代理内核生成的成功可能是缩小软件差距的关键差异化因素。 代理内核生成使用自主 LLM 代理在迭代循环中自动化内核创建和优化。Helios MI455X 系统集成了 72 个 GPU，互连带宽为 896 GB/s，远低于 NVIDIA NVLink 6 的 3.6 TB/s，并且 AMD 通过财务工程提供了超过 100%的折扣。

rss · Semianalysis · 7月25日 00:33

**背景**: NVIDIA 的 CUDA 平台为 AI 开发者创造了强大的生态系统锁定，而 AMD 的竞争平台 ROCm 在软件成熟度和开发工具方面历史上一直落后。代理内核生成是一种新兴方法，利用大型语言模型自动生成高性能计算内核，可能帮助 AMD 缩小软件质量差距。Helios MI455X 是 AMD 最新的 AI 服务器架构，旨在挑战 NVIDIA 在数据中心 AI 领域的主导地位。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.emergentmind.com/topics/agentic-kernel-generation">Agentic Kernel Generation</a></li>
<li><a href="https://arxiv.org/html/2601.15727">Towards Automated Kernel Generation in the Era of LLMs</a></li>
<li><a href="https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026">AMD Helios Challenges NVIDIA: The MI 455 X and the... | Introl Blog</a></li>

</ul>
</details>

**标签**: `#AMD`, `#CUDA`, `#AI`, `#GPU`, `#software`

---

<a id="item-8"></a>
## [GNU C 库 2.44 发布，引入系统级可调参数配置](https://lwn.net/Articles/1085030/) ⭐️ 8.0/10

GNU C 库（glibc）2.44 版本已发布，新增 /etc/tunables.conf 文件用于系统级可调参数配置，增加了控制只读可执行段透明大页的新选项，并包含多项数学函数改进和安全修复。 此版本显著增强了系统管理员调整 glibc 行为的能力，无需仅依赖环境变量，同时透明大页控制可提升可执行段的性能与安全性。由于 glibc 是几乎所有 Linux 系统的基础组件，这些变更对系统稳定性和效率具有广泛影响。 /etc/tunables.conf 文件允许每行指定一个可调参数，可通过可选前缀修饰符控制 GLIBC\_TUNABLES 环境变量的覆盖权限，并支持通过 \[proc:\*\] 语法实现按进程或按用户的规则。新增的透明大页可调参数（glibc.tune.thp\_for\_ro\_exec）允许管理员为只读可执行段启用或禁用 THP，有助于减少内存碎片和 TLB 未命中。

rss · LWN.net · 7月25日 13:44

**背景**: GNU C 库（glibc）是大多数 Linux 发行版使用的核心 C 库，为程序提供系统调用和基本功能。可调参数（tunables）是 glibc 的一项特性，允许调整运行时行为，之前只能通过 GLIBC\_TUNABLES 环境变量配置。透明大页（THP）是 Linux 内核的一项特性，可自动使用大内存页（通常 2MB）以减少 TLB 开销，但若配置不当可能造成内存膨胀。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.phoronix.com/news/Glibc-System-Tunables">Glibc Introduces /etc/tunables.conf For System-Wide Tunables - Phoronix</a></li>
<li><a href="https://www.sourceware.org/glibc/manual/2.39/html_node/Tunables.html">Tunables (The GNU C Library)</a></li>

</ul>
</details>

**标签**: `#glibc`, `#C library`, `#system programming`, `#security`, `#performance`

---