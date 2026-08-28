---
layout: default
title: "Horizon Summary: 2026-03-24 (ZH)"
date: 2026-03-24
lang: zh
---

> From 28 items, 6 important content pieces were selected

---

1. [iPhone 17 Pro 演示运行 4000 亿参数大语言模型](#item-1) ⭐️ 8.0/10
2. [博客探讨使用 LLM 智能体对旧研究思路进行自动化研究](#item-2) ⭐️ 7.0/10
3. [Linux 内核补丁允许 BPF 程序在可休眠与原子上下文之间切换](#item-3) ⭐️ 7.0/10
4. [MiniMax 升级 Coding Plan 为 Token Plan 支持全模态模型，并宣布即将发布 MiniMax 2.7 开源权重](#item-4) ⭐️ 7.0/10
5. [科技企业将员工 LLM token 消耗量纳入绩效考核](#item-5) ⭐️ 7.0/10
6. [OpenAI 建议英国将 AI 聊天机器人纳入 Google 搜索选择页](#item-6) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [iPhone 17 Pro 演示运行 4000 亿参数大语言模型](https://twitter.com/anemll/status/2035901335984611412) ⭐️ 8.0/10

一项演示展示了 iPhone 17 Pro 运行一个 4000 亿参数的大语言模型，通过量化和混合专家架构等技术在移动硬件上实现。 这一演示意义重大，因为它突破了设备端 AI 的极限，可能使先进的语言模型无需持续云端连接即可在智能手机上本地运行，从而可能革新移动应用和隐私保护。 该模型采用混合专家架构，每次仅激活部分参数，并通过量化降低精度以减少内存和计算需求；但实际限制如热节流和量化导致的精度下降也被指出。

hackernews · anemll · Mar 23, 14:30

**背景**: 大语言模型是基于海量文本数据训练的 AI 系统，用于生成类人文本；参数衡量模型大小，参数越多通常需要更多计算资源。量化是一种技术，通过降低模型权重的精度（例如从 32 位降至 8 位）来减少内存使用并加速推理，同时保持准确性。混合专家架构中，模型由多个专业化子模型（专家）组成，通过路由机制为每个输入选择少数专家，从而避免同时使用所有参数，提高大型模型的效率。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.geeksforgeeks.org/deep-learning/quantization-in-deep-learning/">What is Quantization - GeeksforGeeks</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>
<li><a href="https://www.mayhemcode.com/2025/12/the-complete-guide-to-local-llm.html">The Complete Guide to Local LLM Hardware: Specs for Running AI Models on Consumer Hardware</a></li>

</ul>
</details>

**社区讨论**: 社区讨论包括对标题未提及 MoE 细节和量化对模型性能影响的质疑，用户指出量化可能使模型表现类似较小模型，且 iPad 等设备上的热节流限制了实际使用。一些评论还引用了技术论文并表达了对硬件限制的担忧。

**标签**: `#LLM`, `#Mobile AI`, `#Hardware`, `#Quantization`, `#Mixture of Experts`

---

<a id="item-2"></a>
## [博客探讨使用 LLM 智能体对旧研究思路进行自动化研究](https://ykumar.me/blog/eclip-autoresearch/) ⭐️ 7.0/10

一篇博客文章详细介绍了使用 LLM 智能体对旧研究思路进行自动化研究的实验，该智能体类似于一个带有基本推理的超参数优化算法。该系统基于 program.md 文件中的一个简单循环，迭代地改进训练代码、运行实验并记录结果。 这种方法展示了 LLM 智能体如何通过自动化超参数调整和代码迭代等繁琐任务来加速研究，可能减少人力投入并实现大规模实验。它符合 AI 自动化的更广泛趋势，即开发智能体来处理科学和技术领域的复杂工作流程。 该系统的核心是 program.md 中的一个简单循环，强调简洁性，而其他文件包含用于训练的任意机器学习模型。然而，局限性包括如果智能体尝试所有 LLM 建议会产生高成本，以及依赖可能小众或维护不善的库。

hackernews · ykumards · Mar 23, 18:40

**背景**: LLM 智能体是将大型语言模型与规划和记忆等模块结合以自主执行复杂任务的 AI 系统。自动化研究系统，例如由 Karpathy 推广的系统，使用智能体在一夜之间运行多个实验，自动化研究过程的某些部分。这些系统旨在通过处理代码优化和评估等迭代任务来降低成本并加速发现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2501.04227">Agent Laboratory: Using LLM Agents as Research Assistants</a></li>
<li><a href="https://datasciencedojo.com/blog/karpathy-autoresearch-explained/">Karpathy Autoresearch Explained: 100 Experiments Overnight</a></li>
<li><a href="https://www.promptingguide.ai/research/llm-agents">LLM Agents | Prompt Engineering Guide</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调了实际应用，例如使用 LLM 进行现有技术探索但效果不一，以及对成本效率和数据瓶颈的担忧。一些用户指出，带有反馈循环的类似迭代方法在复杂 LLM 部署中很常见，而其他人则质疑自动化研究是否比传统的超参数优化方法更有优势。

**标签**: `#AI Research`, `#LLM Agents`, `#Automated Systems`, `#Machine Learning`, `#Hacker News`

---

<a id="item-3"></a>
## [Linux 内核补丁允许 BPF 程序在可休眠与原子上下文之间切换](https://lwn.net/Articles/1062868/) ⭐️ 7.0/10

Puranjay Mohan 提出了一套补丁集，允许在可休眠上下文中运行的 BPF 程序临时获取锁并切换到原子上下文，解决了当前此类切换被禁止的限制。该实现引入了一个新的 KF_FORBID_FAULT 标记，使 BPF 验证器能够以指令为单位跟踪休眠权限，而不是对整个程序进行全局限制。 这一进展意义重大，因为它允许更多 BPF 程序被标记为可休眠，从而使它们能够从用户空间复制数据——这是一种需要休眠能力的常见操作。通过提供更细粒度的上下文跟踪，该补丁集增强了 Linux 内核中 BPF 程序的灵活性和性能，可能扩展其在内存管理和并发控制等领域的应用场景。 该补丁集添加了一个 KF_FORBID_FAULT 标记，该标记只能用于已标记为 KF_ACQUIRE 的 kfuncs，在持有获取的资源时暂时阻止程序休眠。然而，BPF 维护者 Alexei Starovoitov 对部分实现提出了异议，这意味着补丁的接受取决于 Mohan 能否解决这些问题。

rss · LWN.net · Mar 23, 16:00

**背景**: Linux 内核中的 BPF（Berkeley Packet Filter）程序可以在可休眠或原子（不可休眠）上下文中运行。原子上下文禁止可能延迟内核执行的操作，例如等待 I/O 或处理页面错误。2020 年引入的可休眠 BPF 程序允许从用户空间复制数据，但被限制调用许多假定原子上下文的现有 BPF 接口。Kfuncs 是 BPF 程序可访问的内核函数，KF_ACQUIRE 和 KF_RELEASE 等标记帮助验证器跟踪资源管理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lwn.net/Articles/825415/">Sleepable BPF programs [LWN.net]</a></li>
<li><a href="https://docs.kernel.org/bpf/kfuncs.html">BPF Kernel Functions (kfuncs) — The Linux Kernel documentation</a></li>
<li><a href="https://lwn.net/Articles/779120/">Concurrency management in BPF [LWN.net]</a></li>

</ul>
</details>

**标签**: `#Linux Kernel`, `#BPF`, `#Kernel Programming`, `#Concurrency`, `#Patch Development`

---

<a id="item-4"></a>
## [MiniMax 升级 Coding Plan 为 Token Plan 支持全模态模型，并宣布即将发布 MiniMax 2.7 开源权重](https://mp.weixin.qq.com/s/o4KGGgtp32vRMecOYCbVmA) ⭐️ 7.0/10

MiniMax 将其 Coding Plan 升级为 Token Plan，Plus 及以上套餐用户在保留原编程模型用量的基础上，额外获得视频、语音、音乐、图像等多模态模型的调用额度。同时，MiniMax 宣布 MiniMax 2.7 的开源权重将在约两周内发布，该模型在 OpenClaw 基准测试中表现有明显提升。 此次升级通过将多模态 AI 能力集成到单一订阅中，使 MiniMax 平台更加多功能化，可能降低开发者使用多样化 AI 模型的成本和复杂性。即将发布的 MiniMax 2.7 开源权重将使更广泛的社区能够访问其最新的编程专用模型，促进 AI 辅助开发工具的创新和采用。 为确保服务稳定性，MiniMax 将在工作日下午高峰时间（15:00-17:30）实施动态限流，单周调用上限为原编程模型 5 小时用量的 10 倍。MiniMax 2.7 模型在 OpenClaw 基准测试中表现有明显提升，该测试专门评估 AI 智能体的工具调用能力。

telegram · zaihuapd · Mar 23, 02:09

**背景**: MiniMax 的 Coding Plan 是一项订阅服务，提供对其编程专用 AI 模型的访问权限，使用限制会定期刷新。该平台此前已提供如 MiniMax-M2 等模型，专为编码和智能体工作流程设计，具有高效的推理速度。OpenClaw 是一个基准测试，用于评估大语言模型在 AI 智能体实际工具调用场景中的性能，超越了传统的孤立能力测试。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://platform.minimax.io/subscribe/coding-plan">Token Plan - MiniMax API Platform</a></li>
<li><a href="https://github.com/MiniMax-AI/MiniMax-M2">GitHub - MiniMax-AI/MiniMax-M2: MiniMax-M2, a model built for ...</a></li>
<li><a href="https://github.com/Shad107/openclaw-benchmark">GitHub - Shad107/ openclaw - benchmark : Real-world LLM benchmark ...</a></li>

</ul>
</details>

**标签**: `#AI/ML`, `#multimodal models`, `#open-source`, `#software engineering`, `#API services`

---

<a id="item-5"></a>
## [科技企业将员工 LLM token 消耗量纳入绩效考核](https://gizmodo.com/tech-employees-are-reportedly-being-evaluated-by-how-fast-they-burn-through-llm-tokens-2000736627) ⭐️ 7.0/10

据报道，Meta 和 OpenAI 等科技公司正在根据员工消耗的 LLM token 数量来评估绩效，高使用量者获得奖励，低使用量者面临压力。一名 OpenAI 工程师累计消耗了 2100 亿 token，而 OpenAI 总裁 Greg Brockman 表示，GPT-5.4 上线一周后日处理量已达 5 万亿 token。 这标志着职场绩效评估方式的重大转变，可能激励员工过度使用 AI 而非关注工作质量。它引发了关于如何在专业环境中衡量 AI 采用效果的重要问题，并可能影响整个行业的生产力评估趋势。 据报道，这种做法催生了内部排行榜，员工在 token 使用量上相互竞争，Meta 和 Shopify 等公司明确将 AI 使用指标纳入绩效评估。这种方法侧重于量化消耗而非工作质量或创新影响。

telegram · zaihuapd · Mar 23, 08:42

**背景**: LLM token 是大型语言模型中文本处理的基本单位，token 数量直接关系到计算成本和 API 定价。GPT-5.4 是 OpenAI 于 2026 年 3 月发布的最新前沿模型，具备先进能力并支持 100 万 token 的上下文窗口。科技公司的传统绩效指标通常关注代码质量、项目交付和业务影响等产出，而非输入消耗。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://winder.ai/calculating-token-counts-llm-context-windows-practical-guide/">Calculating LLM Token Counts: A Practical Guide</a></li>
<li><a href="https://en.wikipedia.org/wiki/GPT-5.4">GPT-5.4 - Wikipedia</a></li>
<li><a href="https://careeraheadonline.com/tech-workers-embrace-tokenmaxxing-a-new-ai-rivalry/">Tech Workers Embrace Tokenmaxxing: A New AI Rivalry</a></li>

</ul>
</details>

**标签**: `#AI Ethics`, `#Workplace Culture`, `#LLM Usage`, `#Performance Metrics`, `#Tech Industry`

---

<a id="item-6"></a>
## [OpenAI 建议英国将 AI 聊天机器人纳入 Google 搜索选择页](https://assets.publishing.service.gov.uk/media/69b970dcc06ba9576435ab5a/OpenAI.pdf) ⭐️ 7.0/10

3 月 6 日，OpenAI 向英国竞争与市场管理局（CMA）提交了一份公开咨询意见，建议 Google 搜索选择页的资格标准应明确纳入具备搜索功能的 AI 聊天机器人，使 ChatGPT 等服务能在 Android 设备和 Chrome 等入口被用户选为默认搜索服务。OpenAI 还建议以透明、动态的流行度标准决定入选服务，并将选择页扩展到语音、视觉和 AI 辅助搜索等入口。 这一建议通过让 ChatGPT 等新兴 AI 服务与 Google 等成熟搜索引擎直接竞争，可确保公平竞争，可能重塑市场格局并增加用户对创新 AI 驱动搜索工具的访问。它展示了一种将先进技术融入现有监管框架的新方法，可能影响全球关于数字市场竞争和 AI 可及性的政策。 OpenAI 认为，ChatGPT 等服务通过对话式或多模态方式完成广泛信息发现，功能上与 Google Search 的 AI Overviews 和 AI Mode 相近，而当前围绕传统搜索设计的草案可能排除这类新型服务。该建议针对英国 CMA 的数字市场监管工作，Google 搜索选择页是欧洲《数字市场法案》下的关键合规机制。

telegram · zaihuapd · Mar 23, 14:50

**背景**: Google 搜索选择页是为遵守欧盟《数字市场法案》等法规而推出的功能，允许特定地区用户在 Android 设备设置期间选择默认搜索引擎和浏览器。英国竞争与市场管理局（CMA）是一个促进竞争和保护消费者的监管机构，目前正在审查可能将 Google 和 Apple 等主要平台指定为“战略市场地位”的数字市场规则。AI Overviews 和 AI Mode 是 Google Search 的功能，利用 AI 生成摘要并提供高级推理能力，代表了 AI 与传统搜索功能的融合。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.neowin.net/news/google-will-add-new-search-and-browser-choice-screens-for-android-phones-in-europe/">Google will add new search and browser choice screens for... - Neowin</a></li>
<li><a href="https://www.gov.uk/government/organisations/competition-and-markets-authority">Competition and Markets Authority - GOV. UK</a></li>
<li><a href="https://en.wikipedia.org/wiki/AI_Overviews">AI Overviews - Wikipedia</a></li>

</ul>
</details>

**标签**: `#AI Regulation`, `#Search Engines`, `#Competition Policy`, `#OpenAI`, `#UK CMA`

---