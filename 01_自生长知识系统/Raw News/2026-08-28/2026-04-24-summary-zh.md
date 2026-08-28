---
layout: default
title: "Horizon Summary: 2026-04-24 (ZH)"
date: 2026-04-24
lang: zh
---

> From 40 items, 26 important content pieces were selected

---

1. [OpenAI 发布前沿编程模型 GPT-5.5](#item-1) ⭐️ 9.0/10
2. [Bitwarden CLI 在 Checkmarx 供应链攻击中被入侵](#item-2) ⭐️ 9.0/10
3. [苹果 CEO 库克 2026 年卸任，特努斯接任](#item-3) ⭐️ 9.0/10
4. [vLLM v0.20.0：CUDA 13、PyTorch 2.11、FlashAttention 4、TurboQuant](#item-4) ⭐️ 8.0/10
5. [Anthropic 详解 Claude 健忘漏洞修复](#item-5) ⭐️ 8.0/10
6. [Tailscale 联合创始人批评云复杂性](#item-6) ⭐️ 8.0/10
7. [Ubuntu 26.04 LTS 'Resolute Raccoon' 发布](#item-7) ⭐️ 8.0/10
8. [Qwen 3.6 27B 在智能体指数上与 Sonnet 4.6 持平](#item-8) ⭐️ 8.0/10
9. [美国关于对抗性蒸馏的备忘录引发对开放模型的担忧](#item-9) ⭐️ 8.0/10
10. [单张 RTX 3090 实现 Qwen3.6-27B：85 TPS、125K 上下文、视觉能力](#item-10) ⭐️ 8.0/10
11. [腾讯发布 Hy3 预览版：295B MoE 模型，21B 激活参数](#item-11) ⭐️ 8.0/10
12. [DeepSeek 开源 DeepEP V2 和 TileKernels](#item-12) ⭐️ 8.0/10
13. [吹风机操控巴黎天气传感器，在 Polymarket 获利 3.4 万美元](#item-13) ⭐️ 8.0/10
14. [Google Cloud 默认安全缺陷导致巨额账单](#item-14) ⭐️ 8.0/10
15. [字节跳动发布 Seed3D 2.0，3D 生成迈向生产可用](#item-15) ⭐️ 8.0/10
16. [香港证监会与普华永道就恒大造假达成 10 亿港元和解](#item-16) ⭐️ 8.0/10
17. [中国三大运营商遭遇国际网络故障](#item-17) ⭐️ 8.0/10
18. [英国 NCSC 正式将通行密钥列为首选身份验证方式](#item-18) ⭐️ 8.0/10
19. [欧盟施压 Google 向对手开放 Android AI 助手权限](#item-19) ⭐️ 8.0/10
20. [MIT 科学家建立经典与量子物理的数学桥梁](#item-20) ⭐️ 8.0/10
21. [LiteParse 网页版：浏览器中的 PDF 文本提取](#item-21) ⭐️ 7.0/10
22. [Famfs 文件系统面临可能的 BPF 重构](#item-22) ⭐️ 7.0/10
23. [PI 编程助手搭配 Qwen3.6 35b 表现惊艳](#item-23) ⭐️ 7.0/10
24. [印度学生用 AI 制造虚假网红收割美国保守派](#item-24) ⭐️ 7.0/10
25. [OpenAI 的 macOS Chronicle 功能引发隐私与安全担忧](#item-25) ⭐️ 7.0/10
26. [台积电因成本推迟高数值孔径 EUV 导入至 2029 年](#item-26) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [OpenAI 发布前沿编程模型 GPT-5.5](https://openai.com/index/introducing-gpt-5-5/) ⭐️ 9.0/10

OpenAI 发布了 GPT-5.5，一款新的前沿编程模型，并开始向 Pro 和企业用户逐步推出。该模型在 CyberGym 基准测试中得分 82%，成为 AI 辅助编程领域的强劲竞争者。 GPT-5.5 代表了 AI 辅助软件工程的重大飞跃，可能改变开发者的生产力和工作流程。此次发布也重新引发了关于开发者对 AI 工具依赖性的讨论，社区评论中将失去访问权限比作失去肢体。 为确保服务稳定，模型将逐步推出，首先面向 Pro/企业用户，然后才覆盖 Plus 用户。API 访问尚未开放，但据报道通过 Codex API 的后门可获取 GPT-5.5。

hackernews · rd · Apr 23, 18:01

**背景**: 前沿编程模型是专门用于生成和理解代码的 AI 系统，开发者常用它们来自动化任务并提高生产力。OpenAI 的 GPT 系列已从通用语言模型演变为特定领域的工具，GPT-5.5 专注于编程性能。CyberGym 基准测试用于评估 AI 模型在网络安全和编程挑战方面的表现。

**社区讨论**: 社区情绪复杂：一些用户对日益增长的 AI 编程工具依赖性表示不安，将其比作成瘾。另一些用户则称赞模型性能，并认为 OpenAI 相比 Anthropic 的封闭式 Mythos 模型更加开放。少数用户注意到逐步推出和 API 后门访问等细节。

**标签**: `#AI`, `#GPT`, `#OpenAI`, `#coding`, `#machine learning`

---

<a id="item-2"></a>
## [Bitwarden CLI 在 Checkmarx 供应链攻击中被入侵](https://socket.dev/blog/bitwarden-cli-compromised) ⭐️ 9.0/10

Bitwarden CLI 在供应链攻击中通过被投毒的 npm 包遭到入侵，恶意版本 2026.4.0 被发布到 npm，窃取了受影响用户的凭证和机密信息。 此次攻击影响广泛使用的密码管理器 CLI，可能暴露开发者和组织的敏感凭证，并凸显了 npm 生态系统中持续存在的风险。 恶意包在检测前约 19 小时发布，仅有 334 名用户下载。在 .npmrc 中设置 min-release-age=7（npm 11.10+）即可阻止该包。

hackernews · tosh · Apr 23, 14:17

**背景**: 供应链攻击通过破坏受信任的依赖项来针对软件开发流程。在此案例中，攻击者投毒了 Bitwarden CLI 的 npm 包，该包被开发者用于通过命令行管理密码。Checkmarx 活动是一系列更广泛的 npm 供应链攻击。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://checkmarx.com/zero-post/npm-hit-by-shai-hulud-the-self-replicating-supply-chain-attack/">NPM Hit By Shai-Hulud, The Self-Replicating Supply Chain Attack</a></li>

</ul>
</details>

**社区讨论**: 社区评论建议使用 min-release-age 来缓解此类攻击、锁定依赖项，并考虑使用 Rust 替代方案如 rbw。一些用户对 CLI 以明文形式暴露所有数据表示担忧。

**标签**: `#supply chain security`, `#npm`, `#Bitwarden`, `#supply chain attack`, `#security`

---

<a id="item-3"></a>
## [苹果 CEO 库克 2026 年卸任，特努斯接任](https://t.me/zaihuapd/41030) ⭐️ 9.0/10

苹果宣布管理层交接：现任 CEO 蒂姆·库克将出任董事会执行董事长，硬件工程负责人约翰·特努斯将于 2026 年 9 月 1 日起担任新任 CEO。 这标志着苹果十多年来首次 CEO 更迭，预示着公司产品战略和企业方向进入新时代，对科技行业和投资者影响深远。 约翰·特努斯于 2001 年加入苹果，2013 年升任硬件工程副总裁，2021 年进入高管团队，负责 iPhone、Mac、iPad 和 AirPods 开发。现任董事长 Arthur Levinson 将于 2026 年 9 月 1 日转任首席独立董事。

telegram · zaihuapd · Apr 23, 13:46

**背景**: 蒂姆·库克自 2011 年接替史蒂夫·乔布斯担任苹果 CEO。在库克领导下，苹果营收和市值大幅增长，产品线如 iPhone、Apple Watch 和服务业务不断扩展。此次 CEO 交接对苹果而言是罕见事件，库克转任董事长以确保平稳过渡。

**标签**: `#Apple`, `#CEO transition`, `#leadership`, `#tech industry`

---

<a id="item-4"></a>
## [vLLM v0.20.0：CUDA 13、PyTorch 2.11、FlashAttention 4、TurboQuant](https://github.com/vllm-project/vllm/releases/tag/v0.20.0) ⭐️ 8.0/10

vLLM v0.20.0 是一个重大版本，包含来自 257 位贡献者的 546 次提交，默认使用 CUDA 13.0，升级至 PyTorch 2.11，将 FlashAttention 4 设为默认 MLA 预填充后端，并新增 TurboQuant 2-bit KV 缓存压缩。 此版本显著提升了大型语言模型的推理性能和内存效率，通过降低硬件需求并支持更大规模模型部署，惠及整个 AI/ML 社区。 FlashAttention 4 现在支持 SM90+ GPU 上的 head-dim 512 和 paged-KV，而 TurboQuant 通过 2-bit 压缩提供 4 倍 KV 缓存容量。升级至 PyTorch 2.11 对环境依赖有破坏性变更。

github · khluu · Apr 23, 21:02

**背景**: vLLM 是一个用于大型语言模型（LLM）的高吞吐量、内存高效的推理和服务引擎。它采用 PagedAttention 和连续批处理等技术来优化 GPU 内存和吞吐量。FlashAttention 是一种快速且内存高效的注意力算法，而 KV 缓存压缩可减少长上下文推理的内存占用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/vllm-project/vllm">GitHub - vllm-project/vllm: A high-throughput and memory-efficient inference and serving engine for LLMs · GitHub</a></li>
<li><a href="https://vllm.ai/">vLLM</a></li>

</ul>
</details>

**标签**: `#vLLM`, `#LLM inference`, `#CUDA`, `#PyTorch`, `#FlashAttention`

---

<a id="item-5"></a>
## [Anthropic 详解 Claude 健忘漏洞修复](https://www.anthropic.com/engineering/april-23-postmortem) ⭐️ 8.0/10

Anthropic 披露，3 月 26 日引入的一个漏洞导致 Claude 在每次对话轮次中清除旧思考内容（本应仅在会话空闲后执行一次），使其显得健忘和重复；该漏洞已于 4 月 10 日修复。 这种透明度有助于恢复用户信任，并凸显了在生产环境中保持 AI 行为一致性的挑战，尤其是在上下文保留至关重要的复杂编码任务中。 该漏洞影响 Claude Sonnet 4.6 和 Opus 4.6；此外，4 月 16 日 Anthropic 添加了系统提示指令以减少冗长输出，回应了社区的另一个投诉。

hackernews · mfiguiere · Apr 23, 17:48

**背景**: Claude Code 是一款 AI 编程助手，通过维护会话上下文来记住之前的交互。当会话空闲超过一小时后，清除旧思考内容可减少恢复时的延迟。该漏洞导致此清除操作在后续每一轮对话中重复执行，使模型显得健忘。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/engineering/april-23-postmortem">An update on recent Claude Code quality reports</a></li>
<li><a href="https://www.theregister.com/2026/04/13/claude_outage_quality_complaints/">Claude is getting worse, according to Claude • The Register</a></li>
<li><a href="https://github.com/anthropics/claude-code/issues/42796">[MODEL] Claude Code is unusable for complex engineering tasks with the Feb updates · Issue #42796 · anthropics/claude-code</a></li>

</ul>
</details>

**社区讨论**: 社区评论反应不一：有人赞赏这份诚实的故障报告，也有人对时间点表示怀疑，并质疑是否还有其他未披露的变更导致了感知到的质量下降。少数用户指出，GPT-5.4 等竞争模型已展现出改进。

**标签**: `#AI`, `#Claude`, `#bug`, `#transparency`, `#LLM`

---

<a id="item-6"></a>
## [Tailscale 联合创始人批评云复杂性](https://crawshaw.io/blog/building-a-cloud) ⭐️ 8.0/10

Tailscale 联合创始人 David Crawshaw 发表了一篇题为《我在构建一朵云》的博客文章，批评现代云基础设施和 Kubernetes 的复杂性，并提出一种更简单、更高效的云模型。 来自一位受人尊敬的行业人物的批评凸显了业界对云复杂性的日益不满，并可能影响云基础设施的设计方向，尤其是对于寻求简单性的小团队。 Crawshaw 认为 Kubernetes 存在根本性缺陷，且 VM 是错误抽象，因为其成本与 CPU/内存挂钩而非实际完成的工作。他主张一种默认高性能且简单的云模型。

hackernews · bumbledraven · Apr 23, 04:44

**背景**: 云计算通常提供 IaaS、PaaS 和 SaaS 模型。Kubernetes 已成为事实上的容器编排平台，但因其运维复杂性而受到广泛批评。许多企业在生产环境中使用 Kubernetes 时面临陡峭的学习曲线和额外开销。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://tfir.io/kubernetes-complexity-deal-with-it-there-is-no-way-around-rob-hirschfeld-rackn/">Kubernetes Complexity - Deal With It; There Is No Way Around |</a></li>
<li><a href="https://www.cncf.io/blog/2025/03/06/too-complex-its-not-kubernetes-its-what-it-does/">Too Complex: It’s Not Kubernetes, It’s What It Does | CNCF</a></li>
<li><a href="https://cloudnativenow.com/video-interviews/rethinking-kubernetes-complexity-in-the-enterprise-with-paul-turner/">Rethinking Kubernetes Complexity in the Enterprise with Paul</a></li>

</ul>
</details>

**社区讨论**: Hacker News 社区普遍认同 Crawshaw 的批评，许多人分享了关于 Kubernetes 复杂性的个人惨痛经历。一些人怀疑更简单的云模型能否避免同样的膨胀循环，而另一些人则欣赏这一愿景但担心盈利动机。

**标签**: `#cloud computing`, `#kubernetes`, `#infrastructure`, `#devops`

---

<a id="item-7"></a>
## [Ubuntu 26.04 LTS 'Resolute Raccoon' 发布](https://lwn.net/Articles/1069399/) ⭐️ 8.0/10

代号为 'Resolute Raccoon' 的 Ubuntu 26.04 LTS 已如期发布，引入了 TPM 支持的全盘加密、扩展的内存安全组件、改进的应用权限控制，以及对 Arm 系统的 Livepatch 支持。 此版本显著提升了 Ubuntu 用户在桌面、服务器和云环境中的安全性和弹性，TPM 支持的加密减少了对密码的依赖，而 Arm 上的 Livepatch 则最大限度地减少了基于 ARM 的系统的停机时间。 Ubuntu Desktop、Server、Cloud、WSL 和 Core 将获得 5 年的维护更新，而各风味版本将获得 3 年支持。此版本还包括 Edubuntu、Kubuntu 和 Xubuntu 等官方风味版本。

rss · LWN.net · Apr 23, 18:16

**背景**: TPM（可信平台模块）是一种硬件安全芯片，可安全存储加密密钥，从而在启动时无需密码即可实现全盘加密。Livepatch 允许在不重启的情况下应用内核安全更新，从而减少停机时间。内存安全组件使用 Rust 等语言编写，可防止常见的内存错误，从而提高安全性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ubuntu.com/blog/tpm-backed-full-disk-encryption-is-coming-to-ubuntu">TPM-backed Full Disk Encryption is coming to Ubuntu | Ubuntu</a></li>
<li><a href="https://lwn.net/Articles/943869/">Ubuntu to add TPM-backed full-disk encryption [LWN.net]</a></li>
<li><a href="https://www.reddit.com/r/Ubuntu/comments/15pnh0b/canonicallivepatch_coming_to_arm/">canonical-livepatch coming to ARM? : r/Ubuntu - Reddit</a></li>

</ul>
</details>

**标签**: `#Ubuntu`, `#Linux`, `#LTS`, `#security`, `#release`

---

<a id="item-8"></a>
## [Qwen 3.6 27B 在智能体指数上与 Sonnet 4.6 持平](https://www.reddit.com/gallery/1strodp) ⭐️ 8.0/10

Qwen 3.6 27B 这款仅 270 亿参数的小模型，在 Artificial Analysis 智能体指数上与 Sonnet 4.6 持平，超越了 Gemini 3.1 Pro Preview 和 GPT 5.2/5.3 等更大模型。 这表明小型、可本地运行的模型能够达到前沿级别的智能体性能，可能减少对昂贵 API 提供商的依赖，并加速设备端 AI 的部署。 该模型在所有三个子指数（编码、智能体、知识）上均有提升，但编码指数使用了 Terminal Bench Hard 和 SciCode，作者认为这些选择不太寻常。122B 版本预计将更加令人印象深刻。

reddit · r/LocalLLaMA · dionysio211 · Apr 23, 18:47

**背景**: Artificial Analysis 智能体指数使用包括 Terminal-Bench Hard 和 SciCode 在内的 10 个基准测试来评估 AI 模型的智能体能力。Terminal-Bench Hard 测试命令行任务执行，而 SciCode 评估科学编码。像 Qwen 3.6 27B 这样的小模型因硬件要求低而适合本地推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://artificialanalysis.ai/">AI Model & API Providers Analysis | Artificial Analysis</a></li>
<li><a href="https://www.tbench.ai/benchmarks/terminal-bench-2?difficulties=hard">Terminal - Bench</a></li>
<li><a href="https://scicode-bench.github.io/">SciCode - SciCode Benchmark</a></li>

</ul>
</details>

**社区讨论**: 社区情绪非常积极，用户报告在消费级 GPU（如 RTX 3090）上成功本地部署，并称赞其多步工具调用能力。部分人对基准有效性持怀疑态度，有评论者认为“刷榜”可能推高了分数，而另一人指出 Sonnet 在真实文件组织任务中仍表现更好。

**标签**: `#LLM`, `#benchmarks`, `#open-source`, `#agentic`, `#local-inference`

---

<a id="item-9"></a>
## [美国关于对抗性蒸馏的备忘录引发对开放模型的担忧](https://i.redd.it/jp8emg4cqywg1.jpeg) ⭐️ 8.0/10

美国科技政策办公室的一份政府备忘录对通过对抗性蒸馏大规模提取前沿模型能力表示担忧，这可能导致对开放模型实施更严格的管控。 这可能通过将模型权重视为战略资产来重塑开源 AI 的未来，在国家安全与创新及可及性之间寻求平衡。 该备忘录特别针对使用代理账户和越狱技术的工业化蒸馏，重点在于保护专有模型而非直接针对开源。

reddit · r/LocalLLaMA · MLExpert000 · Apr 23, 15:59

**背景**: 对抗性蒸馏是一种利用目标模型的输出来训练新模型以模仿其行为的技术，可能提取专有能力。前沿模型是具有显著能力的先进 AI 系统，若广泛可及可能带来国家安全风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.frontiermodelforum.org/issue-briefs/issue-brief-adversarial-distillation/">Adversarial Distillation - Frontier Model Forum</a></li>
<li><a href="https://www.justsecurity.org/134124/costs-china-ai-distillation/">The Case for Imposing Costs on China's AI Distillation Campaigns</a></li>
<li><a href="https://rejoicehub.com/blogs/adversarial-distillation-ai-model-security">Adversarial Distillation AI: How to Protect Your AI Models - Rejoicehub</a></li>

</ul>
</details>

**社区讨论**: 社区评论持怀疑态度，有人将此比作历史上寻找大规模杀伤性武器的过度反应，还有人指责 Anthropic 和 OpenAI 等 AI 公司游说监管以扼杀开放权重竞争。许多人认为这是限制中国模型并迫使美国用户支付更多费用的借口。

**标签**: `#AI regulation`, `#open source`, `#adversarial distillation`, `#national security`, `#frontier models`

---

<a id="item-10"></a>
## [单张 RTX 3090 实现 Qwen3.6-27B：85 TPS、125K 上下文、视觉能力](https://medium.com/@fzbcwvv/an-overnight-stack-for-qwen3-6-27b-85-tps-125k-context-vision-on-one-rtx-3090-0d95c6291914?postPublishedType=repub) ⭐️ 8.0/10

一篇指南声称通过自定义推理栈，在单张 RTX 3090 上为 Qwen3.6-27B 模型实现了 85 tokens/秒、125K 上下文长度和视觉能力，但关键的专有 CUDA 补丁尚未公开发布。 这展示了在消费级硬件上本地运行大型开放权重模型的潜力，可能使开发者和研究人员更容易获得强大的 LLM。但缺失的补丁引发了关于可复现性和透明度的担忧。 该栈据称在单张 RTX 3090（24GB 显存）上实现了 85 TPS、125K 上下文和视觉能力，但需要一个名为'patch_tolist_cudagraph.py'的文件，作者尚未发布。社区成员无法在没有该补丁的情况下复现结果。

reddit · r/LocalLLaMA · AmazingDrivers4u · Apr 23, 14:11

**背景**: Qwen3.6-27B 是阿里巴巴以 Apache 2.0 许可发布的稠密 270 亿参数开放权重模型，擅长编码任务。在本地运行此类大型模型通常需要多块高端 GPU 或大量优化。RTX 3090 拥有 24GB 显存，是本地 LLM 推理中流行的消费级 GPU，但在单卡上实现高吞吐量和长上下文具有挑战性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://simonwillison.net/2026/Apr/22/qwen36-27b/">Qwen3.6-27B: Flagship-Level Coding in a 27B Dense Model</a></li>
<li><a href="https://www.implicator.ai/alibaba-ships-qwen3-6-27b-an-open-weight-coding-model-that-beats-its-397b-moe/">Alibaba Qwen3.6-27B Dense Model Beats 397B Predecessor</a></li>

</ul>
</details>

**社区讨论**: 社区对性能声称（85 TPS）印象深刻，但对缺失的补丁感到沮丧，几位评论者称该帖子为点击诱饵或自我宣传。一些用户分享了自己的速度（例如，多 GPU 上 25 t/s，RTX 5090 上 30-40 t/s），并请求补丁或 Docker 镜像。

**标签**: `#LLM inference`, `#Qwen`, `#RTX 3090`, `#performance optimization`, `#local LLM`

---

<a id="item-11"></a>
## [腾讯发布 Hy3 预览版：295B MoE 模型，21B 激活参数](https://www.reddit.com/gallery/1stk2mz) ⭐️ 8.0/10

腾讯开源了 Hy3 预览版，这是一个总参数量达 2950 亿的混合专家模型（MoE），激活参数为 210 亿，支持 256K 上下文长度。该模型已在 Hugging Face 和 GitHub 上发布，腾讯云同步推出 API 及定价方案。 此次发布展示了一家中国大型科技公司在大规模开源 MoE 模型上的投入，可能加速复杂推理和智能体应用的 AI 发展。210 亿的激活参数理论上使其可在高端消费级硬件上运行，但实际部署仍具挑战。 该模型采用混合专家架构，总参数 2950 亿但每次仅激活 210 亿，从而实现高效推理。腾讯报告称，CodeBuddy 等产品的首 token 延迟降低了 54%，该模型已在元宝、腾讯文档、QQ 等内部产品上线。

reddit · r/LocalLLaMA · TKGaming_11 · Apr 23, 14:17

**背景**: 混合专家模型（MoE）是一种神经网络架构，将模型划分为多个专门的子网络（专家），每个输入仅激活其中一部分。这使得模型总参数量很大，但每个 token 的计算成本较低，类似于 Gemma 4 的 26B A4B 模型仅激活 40 亿参数。Hy3 预览版总参数 2950 亿、激活 210 亿的规模，理论上可在配备足够内存（如 256GB）的消费级硬件上运行，但实际使用可能需要量化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ai.google.dev/gemma/docs/core/model_card_4">Gemma 4 model card | Google AI for Developers</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained - Hugging Face</a></li>

</ul>
</details>

**社区讨论**: 社区反应不一：有人称赞模型规模及基础模型的发布，但许多人批评其许可证限制性强，称其为“权重可用”而非真正开源。其他人讨论硬件可行性，指出 AM5 主板上的 256GB 内存可运行该模型，并表示希望与 MiniMax 2.7 和 Qwen 3.5 等模型进行比较。

**标签**: `#LLM`, `#open-source`, `#MoE`, `#Tencent`, `#AI`

---

<a id="item-12"></a>
## [DeepSeek 开源 DeepEP V2 和 TileKernels](https://www.reddit.com/r/LocalLLaMA/comments/1ste9zs/deepseek_has_released_deepep_v2_and_tilekernels/) ⭐️ 8.0/10

DeepSeek 发布了 DeepEP V2（高效的专家并行通信库）和 TileKernels（基于 TileLang 的高性能 GPU 算子库），两者均已开源在 GitHub 上。 这些发布推进了大规模 AI 训练的并行化和 GPU 内核效率，可能实现线性扩展并支持 NVIDIA Blackwell GPU，从而加速未来模型的开发。 TileKernels 涵盖 MoE 路由、FP8/FP4 量化和融合算子，面向 NVIDIA SM90 和 SM100（Blackwell）架构，需要 CUDA 13.1 或更高版本。DeepEP V2 专注于专家并行通信优化。

reddit · r/LocalLLaMA · External_Mood4719 · Apr 23, 09:57

**背景**: DeepSeek 是一家以开源大语言模型闻名的中国 AI 公司。专家并行（EP）将模型专家分布到多个 GPU 上以提高训练效率，而 GPU 内核是加速计算的低级程序。TileLang 是一种用于编写高性能内核的领域特定语言。

**社区讨论**: 社区反应非常积极，称赞 DeepSeek 开源并推动研究。一些人推测线性扩展技术和 Blackwell 支持暗示了未来的模型（可能是 V4），并指出 DeepSeek 正在做 OpenAI 本应做的事情。

**标签**: `#DeepSeek`, `#open-source`, `#GPU kernels`, `#parallel computing`, `#AI infrastructure`

---

<a id="item-13"></a>
## [吹风机操控巴黎天气传感器，在 Polymarket 获利 3.4 万美元](https://fibo-crypto.fr/en/blog/polymarket-weather-sensor-manipulation-paris-meteo-france-2026/) ⭐️ 8.0/10

有人在 4 月 6 日和 15 日使用吹风机干扰巴黎戴高乐机场的法国气象局温度传感器，导致异常读数，从而在 Polymarket 的天气预测市场上触发获胜押注，获利超过 3.4 万美元。 这一事件凸显了预测市场所依赖的现实世界数据源的脆弱性，以及通过物理操纵获取经济收益的可能性，促使 Polymarket 更换数据源，并引发法律和安全方面的担忧。 4 月 6 日，传感器读数在数分钟内从接近 18°C 跃升至超过 21°C；4 月 15 日，22°C 区间的概率在 30 分钟内从 0.1%飙升至 95%。Polymarket 已将数据源切换至巴黎勒布尔热机场，但未撤销已结算的押注。

telegram · zaihuapd · Apr 23, 04:36

**背景**: Polymarket 是一个基于加密货币的预测市场，用户可以对现实世界事件的结果进行押注。天气预测市场允许对特定温度读数进行投注。法国气象局运营包括机场在内的官方气象站，这些站点通常被认为是可靠的数据源。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.theguardian.com/world/2026/apr/23/hairdryer-or-lighter-french-police-look-at-claim-of-sensor-tampering-to-win-weather-bets">‘ Hairdryer or lighter?’: French police look at claim of sensor ...</a></li>
<li><a href="https://www.aol.com/articles/police-investigate-claims-hair-dryer-150607773.html">Police investigate after claims ‘ hair dryer used to manipulate weather ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Polymarket">Polymarket - Wikipedia</a></li>

</ul>
</details>

**标签**: `#prediction markets`, `#weather manipulation`, `#Polymarket`, `#fraud`, `#sensor tampering`

---

<a id="item-14"></a>
## [Google Cloud 默认安全缺陷导致巨额账单](https://www.tomshardware.com/tech-industry/artificial-intelligence/google-cloud-customer-wakes-up-to-usd18-000-bill-despite-usd7-budget-thanks-to-forgotten-public-api-key-attacker-put-in-60-000-requests-and-blasted-through-usd1-400-spending-cap) ⭐️ 8.0/10

一名 AI 顾问尽管设置了 7 美元的预算上限，却因历史项目中的 API 密钥泄露，被攻击者利用发起 6 万次请求并绕过消费上限，导致 Google Cloud 账单超过 1.8 万美元。 此事件凸显了 Google Cloud 默认配置中的系统性安全缺陷：API 密钥可能静默获得对昂贵的 Gemini AI 端点的访问权限，且预算上限会在无通知情况下自动上调，使所有用户面临财务风险。 该漏洞源于 Google Cloud 的 Gemini API 密钥使用单一格式（“AIza”前缀）且安全设置默认关闭，导致任何暴露的密钥都能访问 Gemini 端点。此外，Google Cloud 会在触发阈值时自动上调信用额度且不通知用户。

telegram · zaihuapd · Apr 23, 05:21

**背景**: API 密钥是用于向云服务验证请求的凭证。在 Google Cloud 中，API 密钥传统上被认为对地图等低风险服务不敏感。但随着 Gemini AI 的引入，这些相同的密钥现在可以访问昂贵的 AI 端点，但许多用户并未意识到这一变化。Google Cloud 的预算警报仅为建议性质，不强制执行消费限制，且系统可自动增加信用额度，从而加剧了风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.tomshardware.com/tech-industry/artificial-intelligence/google-cloud-customer-wakes-up-to-usd18-000-bill-despite-usd7-budget-thanks-to-forgotten-public-api-key-attacker-put-in-60-000-requests-and-blasted-through-usd1-400-spending-cap">Google Cloud customer wakes up to $18,000+ bill despite $7 budget ...</a></li>
<li><a href="https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules">Google API Keys Weren't Secrets. But then Gemini Changed the ...</a></li>
<li><a href="https://thehackernews.com/2026/02/thousands-of-public-google-cloud-api.html">Thousands of Public Google Cloud API Keys Exposed with Gemini ...</a></li>

</ul>
</details>

**标签**: `#Google Cloud`, `#security`, `#API key`, `#cloud billing`, `#vulnerability`

---

<a id="item-15"></a>
## [字节跳动发布 Seed3D 2.0，3D 生成迈向生产可用](https://seed.bytedance.com/zh/blog/seed3d-2-0-released-higher-precision-and-greater-usability) ⭐️ 8.0/10

字节跳动于 2026 年 4 月 23 日发布了新一代 3D 生成大模型 Seed3D 2.0，在几何精度和纹理质量上取得行业领先（SOTA）水平，人类评测中相对主流模型的偏好率超过 69%。 这标志着 3D 生成从演示级向生产可用迈出关键一步，有望加速 AI 生成的 3D 内容在游戏、机器人和仿真等行业的应用。 Seed3D 2.0 还支持部件级生成和场景组合，输出带完整关节信息、兼容 URDF 等标准格式的内容，并可适配 NVIDIA Isaac Sim 等物理仿真引擎。

telegram · zaihuapd · Apr 23, 08:15

**背景**: 3D 生成模型旨在从文本或图像创建 3D 模型。以往的模型常产生低质量的几何或纹理，限制其仅用于原型或可视化。URDF 是一种用于机器人模型的标准 XML 格式，Isaac Sim 是 NVIDIA 的机器人仿真平台。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://news.aibase.com/news/27393">ByteDance Launches Seed3D 2.0: Geometry and Texture Dual SOTA ...</a></li>
<li><a href="https://github.com/aitools12/seed3d20">GitHub - aitools12/seed3d20: Seed3d 2.0 AI 3D model generator ...</a></li>
<li><a href="https://developer.nvidia.com/isaac/sim">Isaac Sim - Robotics Simulation and Synthetic Data Generation ...</a></li>

</ul>
</details>

**标签**: `#3D Generation`, `#ByteDance`, `#AI`, `#Computer Graphics`, `#Machine Learning`

---

<a id="item-16"></a>
## [香港证监会与普华永道就恒大造假达成 10 亿港元和解](https://apps.sfc.hk/edistributionWeb/gateway/TC/news-and-announcements/news/doc?refNo=26PR62) ⭐️ 8.0/10

香港证监会于 2026 年 4 月 23 日宣布，已与普华永道香港达成和解协议，要求普华永道预留 10 亿港元，用于赔偿中国恒大集团合资格独立少数股东因财务造假遭受的损失。 这是香港首次要求已倒闭公司的审计师向股东作出赔偿，为审计师责任和市场廉洁树立了里程碑式的先例，凸显监管机构追究看门人企业欺诈责任的决心。 香港证监会认定，恒大在 2019-2020 财年通过提前确认收入虚增收入 5641 亿元，将亏损变为虚假利润。普华永道被指严重违反专业责任，包括丧失审计独立性、缺乏专业怀疑态度，但在不承认法律责任的前提下达成和解。

telegram · zaihuapd · Apr 23, 12:07

**背景**: 中国恒大集团曾是国内最大房地产开发商之一，于 2021 年因巨额债务崩盘，引发房地产行业危机。香港证监会调查发现，恒大操纵财务报表以显示盈利，而普华永道作为审计师未能发现或报告欺诈行为。此次和解之前，中国监管机构已于 2024 年对普华永道处以合计 4.41 亿元罚款。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.thepaper.cn/newsDetail_forward_33037031">香港证监会、会财局同日出手 普华永道同意预留10亿港元赔偿恒大股东_...</a></li>
<li><a href="https://news.qq.com/rain/a/20260423A0741400">普华永道，赔偿10亿港元、被罚3亿港元_腾讯新闻</a></li>

</ul>
</details>

**标签**: `#finance`, `#regulation`, `#auditing`, `#fraud`, `#Evergrande`

---

<a id="item-17"></a>
## [中国三大运营商遭遇国际网络故障](https://t.me/zaihuapd/41029) ⭐️ 8.0/10

中国三大运营商——中国联通、中国电信和中国移动——均出现影响国际路由的广泛网络故障，特别是通往香港、日本和美国的方向，用户报告出现严重丢包和连接中断。 此次故障影响了依赖国际连接的数百万用户和企业，考虑到地缘政治背景，引发了对故障原因是技术问题还是主动策略调整的疑问。 中国电信通往香港和日本的路由受到影响，包括高级路由 CN2 和 9929 以及标准路由 163 和 4837；中国移动的海外手机流量也出现严重丢包，尤其是北京移动用户。

telegram · zaihuapd · Apr 23, 12:45

**背景**: 中国电信运营商使用不同的路由层级：CN2 是中国电信的高级国际路由，163 是标准公共路由；类似地，中国联通使用 9929（高级）和 4837（标准）。这些路由对国际连接至关重要，通常针对低延迟进行优化。BGP 路由泄漏或硬件故障可能导致大范围中断。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://gist.github.com/bgr24955/c05934370051d12d3677f2da4a260f32">VMRack VPS Review 2026: CN2 GIA Triple-Network Routes, Starting at ...</a></li>
<li><a href="https://www.explaintopic.com/networking/widespread-network-outage-across-china-telecom-infrastructur-1765803625.html">Widespread network outage across china telecom ... | ExplainTopic</a></li>
<li><a href="https://www.securityweek.com/china-telecom-routes-european-traffic-its-network-two-hours/">China Telecom Routes European Traffic to Its... - SecurityWeek</a></li>

</ul>
</details>

**社区讨论**: 新闻帖子邀请用户分享他们的经历，但内容中未提供具体评论。鉴于实时影响，预计讨论会很活跃。

**标签**: `#network outage`, `#China telecom`, `#internet censorship`, `#routing failure`, `#telecommunications`

---

<a id="item-18"></a>
## [英国 NCSC 正式将通行密钥列为首选身份验证方式](https://www.techradar.com/pro/security/uk-security-agency-officially-declares-passkeys-superior-to-passwords-passkeys-should-be-the-first-choice-for-authentication) ⭐️ 8.0/10

英国国家网络安全中心（NCSC）正式宣布通行密钥优于传统密码，并建议将其作为数字服务的首选登录方式，结束了此前的观望态度。 这一来自国家级网络安全机构的认可标志着重大政策转变，可能加速通行密钥的全球普及，减少对易受攻击密码的依赖，为数百万用户提升安全性。 英国超过 50%的 Google 活跃用户已注册通行密钥，eBay 和 PayPal 等主流平台也已适配。NCSC 指出，过去 12 个月的行业进展解决了核心实施难题。

telegram · zaihuapd · Apr 23, 14:47

**背景**: 通行密钥是存储在用户设备上的加密凭证，通常通过生物识别（指纹或面部识别）或 PIN 码解锁。它们取代传统密码，能抵御钓鱼攻击和凭证窃取。NCSC 此前因早期采用障碍而持谨慎态度，但现在认为该技术已足够成熟，可广泛使用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ncsc.gov.uk/blog-post/passkeys-not-perfect-getting-better">Passkeys : they're not perfect but they're getting better - NCSC .GOV.UK</a></li>
<li><a href="https://www.theregister.com/2026/04/23/ncsc_passkey_tech_now_reliable/">NCSC : Passkeys now good enough to be the default standard</a></li>
<li><a href="https://www.reddit.com/r/technology/comments/1stffrs/uk_security_agency_officially_declares_passkeys/">UK security agency officially declares passkeys superior to passwords</a></li>

</ul>
</details>

**社区讨论**: Reddit 上对该新闻的评论褒贬不一：一些用户欢迎此举，认为通行密钥更安全便捷；另一些人则担心设备锁定和丢失设备后的恢复问题。少数评论者指出，通行密钥在不同平台间仍存在可用性问题。

**标签**: `#cybersecurity`, `#authentication`, `#passkeys`, `#NCSC`, `#identity`

---

<a id="item-19"></a>
## [欧盟施压 Google 向对手开放 Android AI 助手权限](https://www.bloomberg.com/news/articles/2026-04-23/google-faces-eu-pressure-to-open-up-android-to-gemini-rivals) ⭐️ 8.0/10

欧盟正在起草法规，要求 Google 在 Android 系统上给予 ChatGPT、Claude 等竞争对手的 AI 助手与其自家 Gemini 相同的系统级权限。 这可能重塑移动 AI 助手市场的竞争格局，为用户提供更多选择，同时引发 Google 和 Android 用户对安全与隐私的重大担忧。 相关要求仍处于草案阶段，发布时间可能推迟。Google 担心这种开放要求可能影响用户安全和隐私。

telegram · zaihuapd · Apr 23, 15:31

**背景**: 欧盟此前已通过《数字市场法案》（DMA）对大型科技平台进行监管，包括要求 Google 提供浏览器和搜索引擎的选择屏幕。系统级权限允许 AI 助手深度与操作系统交互，例如读取通知或控制应用，目前 Google 在 Android 上仅将这一特权授予其自家的 Gemini 助手。

**标签**: `#EU regulation`, `#Android`, `#AI assistants`, `#Google`, `#antitrust`

---

<a id="item-20"></a>
## [MIT 科学家建立经典与量子物理的数学桥梁](https://www.newsy-today.com/new-study-bridges-the-worlds-of-classical-and-quantum-physics-mit-news/) ⭐️ 8.0/10

MIT 研究人员在经典 Hamilton-Jacobi 方程中引入密度项，得到了与薛定谔方程数学上等价的结果，从而为经典与量子物理之间建立了新的数学桥梁。 这项工作为量子行为提供了更简洁的数学描述，有望改进量子计算中量子比特行为的预测，并为量子力学与广义相对论的统一提供新线索。 新框架可以解释双缝实验和量子隧穿等量子现象。研究人员认为，它有望改进量子比特动力学的建模。

telegram · zaihuapd · Apr 23, 16:30

**背景**: Hamilton-Jacobi 方程是经典力学的一种表述，将粒子运动描述为波，因此被视为经典力学与量子力学的“最近途径”。薛定谔方程是非相对论量子力学的基本方程，支配量子系统的波函数。这项工作通过向 Hamilton-Jacobi 方程添加密度项，将两者联系起来。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Hamilton-Jacobi_equation">Hamilton-Jacobi equation</a></li>
<li><a href="https://en.wikipedia.org/wiki/Schrödinger_equation">Schrödinger equation</a></li>
<li><a href="https://en.wikipedia.org/wiki/Quantum_tunnelling">Quantum tunnelling</a></li>

</ul>
</details>

**标签**: `#quantum physics`, `#mathematical physics`, `#quantum computing`, `#research breakthrough`

---

<a id="item-21"></a>
## [LiteParse 网页版：浏览器中的 PDF 文本提取](https://simonwillison.net/2026/Apr/23/liteparse-for-the-web/#atom-everything) ⭐️ 7.0/10

Simon Willison 创建了 LlamaIndex 的 LiteParse 的浏览器版本，使得完全在浏览器中通过空间文本解析启发式方法提取 PDF 文本成为可能，无需 AI 模型。 该工具为 PDF 文本提取提供了一种保护隐私、可离线使用的替代方案，对于需要处理敏感文档且不希望将数据发送到服务器的 Web 开发者和 RAG 式问答系统尤其有用。 LiteParse 网页版使用与 Node.js CLI 版本相同的 PDF.js 和 Tesseract.js 库，并支持对扫描版 PDF 进行可选的 OCR 识别。它还提供了带边界框的可视化引用功能，以增强答案的可信度。

rss · Simon Willison · Apr 23, 21:54

**背景**: LiteParse 是 LlamaIndex 的一个开源项目，它使用空间文本解析启发式方法而非 AI 模型来提取 PDF 文本。它能处理多列布局，并以合理的线性顺序输出文本。原始版本是一个 Node.js CLI 工具；这个浏览器移植版使其无需安装即可使用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.marktechpost.com/2026/03/19/llamaindex-releases-liteparse-a-cli-and-typescript-native-library-for-spatial-pdf-parsing-in-ai-agent-workflows/">LlamaIndex Releases LiteParse: A CLI and TypeScript-Native</a></li>
<li><a href="https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/">Running OCR against PDFs and images directly in your browser</a></li>

</ul>
</details>

**标签**: `#PDF parsing`, `#browser`, `#open source`, `#text extraction`, `#LlamaIndex`

---

<a id="item-22"></a>
## [Famfs 文件系统面临可能的 BPF 重构](https://lwn.net/Articles/1068686/) ⭐️ 7.0/10

在 2026 年 LSFMM+BPF 峰会上，有人建议使用 BPF 重写 famfs 文件系统，而非当前基于 FUSE 的实现，这让维护者 John Groves 感到沮丧，因为他认为代码已接近合并主线。 这场争论可能显著延迟 famfs 的采用，这是一个针对 CXL 附加共享内存的专用文件系统，支持跨多个系统高效访问大型只读数据集。结果将影响未来内核文件系统在性能和可维护性之间的平衡。 Famfs 最初使用独立内核文件系统，后迁移到 FUSE 并引入两个新操作（GET_FMAP 和 GET_DAXDEV）以避免用户空间缺页开销。新提案建议将 famfs 特定逻辑移入 BPF 程序，这能进一步减少内核改动，但需要大量重写。

rss · LWN.net · Apr 23, 13:44

**背景**: Famfs（Fabric Attached Memory File System）专为存储在 CXL 附加共享内存中的大型只读数据集设计，允许多个主机通过 mmap()访问数据而无需系统调用。CXL（Compute Express Link）是一种互连技术，保持 CPU 与附加设备之间的内存一致性，实现资源池化。LSFMM+BPF 峰会是 Linux 内核开发者年度会议，专注于存储、文件系统、内存管理和 BPF。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/cxl-micron-reskit/famfs">GitHub - cxl-micron-reskit/famfs: This is the user space repo ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Compute_Express_Link">Compute Express Link - Wikipedia</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#filesystem`, `#CXL`, `#BPF`, `#memory management`

---

<a id="item-23"></a>
## [PI 编程助手搭配 Qwen3.6 35b 表现惊艳](https://www.reddit.com/r/LocalLLaMA/comments/1stjwg5/been_using_pi_coding_agent_with_local_qwen36_35b/) ⭐️ 7.0/10

一位 Reddit 用户分享了使用开源 PI 编程助手搭配本地 Qwen3.6 35b A3B 模型的积极体验，并重点介绍了一个自定义的“先计划”技能文件，该文件强制在编写任何代码之前进行逐步执行。 Qwen3.6 35b A3B 模型仅使用 3B 活跃参数，可在 MacBook Pro M4 Pro（48GB 内存）等消费级硬件上实现快速推理。先计划技能文件以 markdown 文件形式共享，强制实施包含分析、澄清、规划和执行阶段的结构化工作流程。

reddit · r/LocalLLaMA · SoAp9035 · Apr 23, 14:11

**背景**: PI 编程助手是由 Mario Zechner 开发的开源终端编程助手。Qwen3.6 35b A3B 是阿里巴巴最新发布的开源模型，采用混合专家架构，支持高达 262K 上下文 token。PI 中的技能文件类似于 Claude Code 的技能，允许用户定义自定义工作流程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Pi_Coding_Agent">Pi Coding Agent</a></li>
<li><a href="https://medium.com/data-science-in-your-pocket/qwen3-6-35b-a3b-the-tiny-active-open-model-that-thinks-codes-and-agents-like-a-much-bigger-one-486d535e372e">Qwen 3 . 6 – 35 B - A 3 B : The Tiny-Active Open Model That... | Medium</a></li>

</ul>
</details>

**社区讨论**: 社区成员证实了类似的成功，一位用户在改用 PI 搭配 Qwen3.6 35b 后取消了 IDE 和 Claude 订阅。其他人询问了与 OpenCode 计划模式的差异，以及是否值得从 Claude Code 迁移，总体情绪非常积极。

**标签**: `#local-llm`, `#coding-agent`, `#qwen`, `#open-source-ai`, `#skill-file`

---

<a id="item-24"></a>
## [印度学生用 AI 制造虚假网红收割美国保守派](https://www.indiatoday.in/india/story/indian-medical-students-fake-ai-influencer-instagram-us-republican-audience-jennifer-lawrence-syndey-sweeney-2899820-2026-04-22) ⭐️ 7.0/10

一名 22 岁的印度医学生 Sam 利用 Google Gemini 创建了名为 Emily Hart 的虚假保守派网红账号，在 Instagram 和 Fanvue 上从美国 MAGA 群体中获利数千美元。 此案例凸显了 AI 被滥用于制造令人信服的虚假身份以谋取政治和经济利益的现象，引发了对 misinformation、AI 伦理以及目标人群脆弱性的严重担忧。 Sam 最初发布普通美女照片但流量不佳；Gemini 建议他瞄准保守派受众以获得更高忠诚度和可支配收入。虚假账号发布冰钓、射击场等照片，并在 Fanvue 上销售 AI 生成的成人图片。

telegram · zaihuapd · Apr 23, 02:21

**背景**: Google Gemini 是 Google 开发的生成式 AI 聊天机器人和虚拟助手，能够提供建议和生成内容。Fanvue 是一个订阅制社交平台，允许创作者赚钱，并已成为 AI 生成内容的替代平台之一。MAGA 受众指支持唐纳德·特朗普“让美国再次伟大”运动的群体，通常具有保守价值观。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Gemini">Google Gemini - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Fanvue">Fanvue - Wikipedia</a></li>

</ul>
</details>

**标签**: `#AI`, `#misinformation`, `#social media`, `#ethics`, `#politics`

---

<a id="item-25"></a>
## [OpenAI 的 macOS Chronicle 功能引发隐私与安全担忧](https://www.theregister.com/2026/04/22/openai_chronicle_no_privacy_screenshot/) ⭐️ 7.0/10

OpenAI 为 macOS 版 Codex 应用推出了选择性加入的研究预览功能 Chronicle，该功能会定期截取屏幕并通过 OCR 提取文本作为持久记忆存储。安全研究人员指出，OCR 文本在本地以未加密形式存储，且容易受到提示注入攻击。 该功能与备受争议的微软 Recall 类似，给用户（尤其是处理敏感数据的开发者）带来了重大的隐私和安全风险。未加密的本地存储以及易受提示注入攻击的特性可能导致数据泄露和未授权访问。 Chronicle 目前仅限 macOS 上的 ChatGPT Pro 订阅用户使用，且未在欧盟、英国或瑞士推出。截屏数据仅在本地存储 6 小时，但 OCR 提取的文本以未加密形式无限期保存，并可被设备上的其他程序访问。

telegram · zaihuapd · Apr 23, 03:06

**背景**: Chronicle 是一种屏幕感知记忆功能，通过分析屏幕内容构建用户活动的持久记录。提示注入攻击利用 AI 模型的漏洞注入恶意提示，可能导致模型泄露数据或执行非预期操作。OCR（光学字符识别）技术将文本图像转换为机器可读的文本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://9to5mac.com/2026/04/20/codex-for-mac-gains-chronicle-for-enhancing-context-using-recent-screen-content/">OpenAI releases Codex ' Chronicle ' feature for enhancing... - 9to5 Mac</a></li>
<li><a href="https://www.neowin.net/news/openai-introduces-chronicle-for-codex-a-recall-like-memory-feature-for-developers-on-macos/">OpenAI introduces Chronicle for Codex, a Recall-like memory feature ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Prompt_injection_attack">Prompt injection attack</a></li>

</ul>
</details>

**标签**: `#AI`, `#privacy`, `#security`, `#OpenAI`, `#macOS`

---

<a id="item-26"></a>
## [台积电因成本推迟高数值孔径 EUV 导入至 2029 年](https://money.udn.com/money/story/5599/9458925?from=edn_newestlist_rank) ⭐️ 7.0/10

台积电在北美技术论坛上宣布，由于设备价格过高（单台超过 3.5 亿欧元），2029 年底前不会将 ASML 的高数值孔径 EUV 光刻机用于晶圆量产。公司同时披露 A13 制程将于 2029 年投产，并计划在 2029 年前于亚利桑那州建立 CoWoS 和 3D-IC 封装产能。 这一决定表明，全球领先的代工厂台积电认为现有 EUV 设备仍有潜力可挖，可能延缓高数值孔径 EUV 在整个行业的普及。同时，台积电在美国投资 CoWoS 和 3D-IC 封装，凸显了先进封装的重要性，并旨在完善其本土供应链。 高数值孔径 EUV（0.55 NA）可实现 8nm 分辨率，支持 2nm 以下制程的更小金属间距，但单台售价超过 3.5 亿欧元。台积电将继续优化现有 EUV 设备用于 A13 节点（可能为 2nm 或以下），并预计其亚利桑那州首座晶圆厂的良率将接近台湾工厂，第二座晶圆厂将于明年量产。

telegram · zaihuapd · Apr 23, 11:22

**背景**: 高数值孔径 EUV 光刻是 ASML 开发的下一代半导体制造技术，采用 0.55 数值孔径实现 8nm 分辨率，对 3nm 以下制程至关重要。CoWoS（基板上晶圆上芯片）和 3D-IC 是先进封装技术，通过垂直或水平集成多个芯片来提升性能并缩小尺寸。台积电的美国扩张旨在实现生产和封装本地化，以满足美国客户需求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zhuanlan.zhihu.com/p/688959589">High-NA EUV光刻机入场，究竟有多强？ - 知乎</a></li>
<li><a href="https://baike.baidu.com/item/High-NA+EUV/65485250">High-NA EUV - 百度百科</a></li>
<li><a href="https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm">CoWoS® - Taiwan Semiconductor Manufacturing Company Limited</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#TSMC`, `#ASML`, `#EUV lithography`, `#manufacturing`

---
