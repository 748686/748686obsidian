---
layout: default
title: "Horizon Summary: 2026-05-18 (ZH)"
date: 2026-05-18
lang: zh
---

> From 31 items, 12 important content pieces were selected

---

1. [GDS 建议 NHS 保持开源仓库公开](#item-1) ⭐️ 9.0/10
2. [AI 不会加速软件开发过程](#item-2) ⭐️ 8.0/10
3. [原生应用仍需依赖 WebKit 进行文本渲染](#item-3) ⭐️ 8.0/10
4. [AI 是技术而非产品](#item-4) ⭐️ 8.0/10
5. [Mozilla 呼吁英国监管机构：不要削弱 VPN](#item-5) ⭐️ 8.0/10
6. [Linus Torvalds 谈 AI 漏洞泛滥：内核安全列表不堪重负](#item-6) ⭐️ 8.0/10
7. [计算机安全先驱 Peter G. Neumann 逝世](#item-7) ⭐️ 8.0/10
8. [付费项目误导高中生从事虚假机器学习研究](#item-8) ⭐️ 8.0/10
9. [M5、DGX Spark、Strix Halo 与 RTX 6000 AI 推理基准对比](#item-9) ⭐️ 8.0/10
10. [85 GPU 小时对比 Qwen3.6-27B 的 5 种 Abliteration 方法](#item-10) ⭐️ 8.0/10
11. [llama.cpp 双 GPU 加速修复量化 KV 缓存](#item-11) ⭐️ 8.0/10
12. [长鑫科技科创板 IPO，营收增长 719%](#item-12) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [GDS 建议 NHS 保持开源仓库公开](https://simonwillison.net/2026/May/17/gds-weighs-in/#atom-everything) ⭐️ 9.0/10

英国政府数字服务局（GDS）于 2026 年 5 月 14 日发布指导意见，建议公共部门组织默认保持开源仓库公开，直接反对了 NHS 在通过 Project Glasswing 报告安全漏洞后计划关闭其仓库的做法。 这次干预标志着英国政府内部的重大政策冲突，作为中央数字权威机构的 GDS 公开质疑 NHS 退出开源的做法，强调关闭仓库会增加成本并减少审查。结果可能为整个英国公共部门的开源实践树立先例。 GDS 的指导意见警告称，将所有内容设为私有会增加“交付和政策成本”，并减少复用和审查；而 NHS 的决定是由 Anthropic 的 Project Glasswing 网络安全倡议披露的漏洞引发的。Terence Eden 将 GDS 的声明解读为罕见的内部公务员分歧公开化。

rss · Simon Willison · May 17, 15:59

**背景**: 政府数字服务局（GDS）是英国政府负责数字化公共服务转型的部门。NHS（英国国家医疗服务体系）在 Project Glasswing 报告漏洞后计划关闭其开源仓库；Project Glasswing 是 Anthropic 发起的一项网络安全倡议，使用 AI 在关键开源软件中查找安全缺陷。开源软件是指公开可访问、可自由使用、修改和共享的代码，通常能带来更高的透明度和更快的创新，但也存在潜在的安全风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Government_Digital_Service">Government Digital Service - Wikipedia</a></li>
<li><a href="https://www.anthropic.com/glasswing">Project Glasswing: Securing critical software for the AI era</a></li>

</ul>
</details>

**标签**: `#open source`, `#government policy`, `#security`, `#NHS`, `#GDS`

---

<a id="item-2"></a>
## [AI 不会加速软件开发过程](https://frederickvanbrabant.com/blog/2026-05-15-i-dont-think-ai-will-make-your-processes-go-faster/) ⭐️ 8.0/10

一篇博文指出，AI（尤其是大语言模型）不会显著加快软件开发速度，因为主要瓶颈在于需求不明确，而非编码速度。 这种反主流观点挑战了 AI 提升整体生产力的普遍说法，促使重新审视软件工程中真正的低效环节。 作者强调，软件工程本质上就是澄清模糊需求的过程，而 AI 无法自动化这一任务，并指出模糊的功能需求长期是主要痛点。

hackernews · TheEdonian · May 17, 12:13 · [社区讨论](https://news.ycombinator.com/item?id=48168221)

**背景**: 软件开发涉及从需求到部署的多个阶段。虽然 GitHub Copilot 等 AI 工具可以加速编码，但最耗时的部分往往是理解要构建什么。文章认为，除非 AI 能帮助澄清需求，否则整体流程速度提升仍然有限。

**社区讨论**: 评论大多表示支持，用户分享了对模糊需求的经历，并认同瓶颈往往在开发前期。一些人认为 AI 可以在构思和文档等其他阶段提供帮助，但普遍共识是文章点出了一个关键事实。

**标签**: `#AI`, `#software engineering`, `#requirements`, `#productivity`, `#LLMs`

---

<a id="item-3"></a>
## [原生应用仍需依赖 WebKit 进行文本渲染](https://justsitandgrin.im/posts/native-all-the-way-until-you-need-text/) ⭐️ 8.0/10

一篇技术博文揭示了原生应用在渲染 Markdown 等富文本时经常回退到 WebKit，因为原生的 SwiftUI Text 组件在处理大文档时性能和特性不足。 这凸显了原生与 Web 之争中的一个务实权衡：即使性能敏感的原生应用也会在文本密集型视图中选择 WebKit，挑战了“原生总是性能更好”的假设。 作者对一个 Markdown 聊天视图进行了基准测试，发现 WebKit 渲染明显快于 SwiftUI 的 Text，TextKit 2 下每次按键重样式只需不到 8ms，而 WebKit 则受益于成熟的 GPU 加速引擎。

hackernews · dive · May 17, 11:49 · [社区讨论](https://news.ycombinator.com/item?id=48168058)

**背景**: Apple 平台上的原生应用开发使用 SwiftUI 和 UIKit 等框架，但它们的 Text 组件在处理大型或格式丰富的文档时可能很慢。WebKit（Safari 背后的引擎）在 macOS 和 iOS 上作为原生框架（WKWebView）提供，允许应用高效渲染 HTML 和 CSS。这篇文章探讨了性能权衡，并认为使用 WebKit 进行文本渲染是一种务实选择，而非原生开发的失败。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://webkit.org/blog/16301/webkit-features-in-safari-18-2/">WebKit Features in Safari 18.2 | WebKit</a></li>
<li><a href="https://fatbobman.com/en/posts/creating-stunning-dynamic-text-effects-with-textrender/">Creating Stunning Dynamic Text Effects with TextRenderer</a></li>
<li><a href="https://stackoverflow.com/questions/75922628/conditionally-rendering-text-view-with-a-large-string-causes-performance-issue">swiftui - Conditionally rendering Text view with a large string causes performance issue - Stack Overflow</a></li>

</ul>
</details>

**社区讨论**: 评论者分享了不同的体验：一位开发者称赞 TextKit 2 的快速按键重样式，另一位则指出浏览器引擎在性能上已超越 SwiftUI。一些人认为 WebKit 适合 Markdown 渲染，但反对方指出存在成熟的 SwiftUI Markdown 库（如 swift-markdown-ui）。总体而言，讨论集中在何时使用原生 vs Web 文本渲染，并提供了具体的性能数据。

**标签**: `#native vs web`, `#performance`, `#text rendering`, `#WebKit`, `#SwiftUI`

---

<a id="item-4"></a>
## [AI 是技术而非产品](https://daringfireball.net/2026/05/ai_is_technology_not_a_product) ⭐️ 8.0/10

一篇文章主张，人工智能应作为底层技术融入产品中，而非作为独立产品来营销。 这一观点挑战了当前 AI 产品化的趋势，强调真正的价值在于无缝融入用户体验，尤其是对于像苹果这样注重易用性的公司。 文章指出，成功的 AI 实现（例如让 Siri 可靠地完成日常任务）根本不需要让人感觉到 AI 的存在；它应当对用户不可见。

hackernews · ch_sm · May 17, 13:11 · [社区讨论](https://news.ycombinator.com/item?id=48168626)

**背景**: 许多科技公司目前将 AI 功能作为独立产品或升级来营销。然而，最有效的 AI 往往是不可见的，为智能推荐或语音助手等功能提供支持。苹果历来优先考虑无缝的用户体验，而非展示底层技术。

**社区讨论**: 评论者大多表示赞同，引用改善 Siri 而不让其感觉像 AI 的例子，并提及“Dropbox 是功能而非产品”的类比。一些人强调要从客户体验出发，正如史蒂夫·乔布斯所倡导的那样。

**标签**: `#AI`, `#product design`, `#Apple`, `#user experience`, `#technology strategy`

---

<a id="item-5"></a>
## [Mozilla 呼吁英国监管机构：不要削弱 VPN](https://blog.mozilla.org/netpolicy/2026/05/15/mozilla-to-uk-regulators-vpns-are-essential-privacy-and-security-tools-and-should-not-be-undermined/) ⭐️ 8.0/10

Mozilla 就英国政府关于在线年龄验证的咨询提交回应，认为 VPN 是隐私和安全所必需的，不应受到限制或削弱。 这很重要，因为它代表了一家知名科技公司反对可能限制 VPN 使用的法规，直接影响英国公民的隐私权和数字安全，并为其他国家树立先例。 该咨询是英国“在线上世界中成长”计划的一部分，包含一个关于年龄限制 VPN 的具体问题。Mozilla 强调监管机构应通过追究平台责任来处理在线伤害，而非针对 VPN。

hackernews · WithinReason · May 17, 06:17 · [社区讨论](https://news.ycombinator.com/item?id=48166459)

**背景**: VPN（虚拟专用网络）加密互联网流量并隐藏用户 IP 地址，提供隐私和安全。一些政府提议对 VPN 进行年龄限制，以防止未成年人绕过内容限制，但隐私倡导者认为这会削弱基本的隐私保护，并可能适得其反。

**社区讨论**: 评论者大多支持 Mozilla 的立场，有人指出澳大利亚政府出乎意料地推荐使用 VPN。其他人质疑平台如何在不使用 VPN 的情况下有效进行年龄验证，还有批评将英国的数字政策比作反乌托邦监控。

**标签**: `#VPN`, `#privacy`, `#Mozilla`, `#UK regulation`, `#digital rights`

---

<a id="item-6"></a>
## [Linus Torvalds 谈 AI 漏洞泛滥：内核安全列表不堪重负](https://lwn.net/Articles/1073193/) ⭐️ 8.0/10

Linus Torvalds 在 7.1-rc4 内核预补丁中宣布，Linux 内核安全列表被大量 AI 生成的漏洞报告淹没，并明确此类漏洞不应被视为秘密，也不应私下处理。 这一政策澄清解决了 AI 生成漏洞报告日益严重的问题，这些报告导致重复工作和精力浪费；它为内核社区如何处理自动提交设定了先例，有望提高效率和透明度。 该声明伴随着 Willy Tarreau 提交的一个拉取请求，其中包含定义什么构成安全漏洞以及使用 AI 发现漏洞的负责任方式的补丁，为社区提供了技术指南。

rss · LWN.net · May 17, 21:39

**背景**: Linux 内核安全列表是一个私人邮件列表，用于在公开披露之前讨论潜在的安全漏洞。内核预补丁（如-rc4）是下一个稳定内核版本的候选发布版，用于测试。AI 生成的漏洞报告不断增加，导致噪音和重复，因此需要政策调整。

**标签**: `#Linux kernel`, `#security`, `#AI-generated bugs`, `#kernel maintenance`, `#Linus Torvalds`

---

<a id="item-7"></a>
## [计算机安全先驱 Peter G. Neumann 逝世](https://lwn.net/Articles/1073186/) ⭐️ 8.0/10

著名计算机安全先驱、RISKS Digest 长期编辑 Peter G. Neumann 逝世。《纽约时报》于 2026 年 5 月 17 日发布了讣告。 Neumann 在 RISKS Digest 数十年的工作以及在 SRI 的研究塑造了计算机安全与风险分析领域。他的逝世是网络安全界的巨大损失。 Neumann 自 1985 年起主持 ACM 期刊 RISKS Digest，该期刊讨论计算机系统及公共政策中的风险。该消息通过 LWN.net 邮件列表发布。

rss · LWN.net · May 17, 19:36

**背景**: RISKS Digest（计算机及相关系统对公众风险的论坛）是一份经审核的在线期刊，专注于技术系统的安全性、可靠性和意外后果。由 Peter G. Neumann 创立，数十年来一直是系统管理员和安全专业人士的重要资源。Neumann 也是 SRI International 的研究员，是计算机安全领域的重要声音。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/RISKS_Digest">RISKS Digest</a></li>
<li><a href="https://catless.ncl.ac.uk/Risks/">RISKS-LIST: RISKS-FORUM Digest</a></li>

</ul>
</details>

**标签**: `#obituary`, `#computer security`, `#RISKS Digest`, `#Peter G. Neumann`

---

<a id="item-8"></a>
## [付费项目误导高中生从事虚假机器学习研究](https://www.reddit.com/r/MachineLearning/comments/1tfh2s9/program_misleading_high_school_students_into/) ⭐️ 8.0/10

一个名为 Algoverse AI Research 的付费项目被指控误导高中生发表有缺陷的机器学习论文，声称被 NeurIPS 研讨会接受，多篇论文存在明显错误，例如不同实验条件下结果完全相同。 这暴露了机器学习研究中严重的伦理问题，特别是针对高中生牟利，并损害了 NeurIPS 研讨会等知名会议的可信度。它引发了对同行评审过程公正性的担忧，以及对学生寻求大学申请资质的剥削。 该项目网站声称有 289 名学生被 NeurIPS 2025 录取，然而负责人 Kevin Zhu 有 158 篇论文和 468 位合著者，但没有博士学位或硕士学位。具体论文显示表格结果重复，且章节位置错乱，例如 Related Works 被放在 Results 部分内。

reddit · r/MachineLearning · Marisu_BG · May 17, 06:08

**背景**: NeurIPS 是顶级的机器学习会议，其研讨会虽有声望但比主会议严格性较低。OpenReview 是一个论文评审平台。Algoverse 将自己标榜为帮助高中生发表 AI 研究，但批评者称其利用该系统牟利。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://algoverseairesearch.org/">Algoverse AI Research</a></li>
<li><a href="https://openreview.net/about">About | OpenReview</a></li>
<li><a href="https://blog.neurips.cc/2025/04/12/guidance-for-neurips-workshop-proposals-2025/">Guidance for NeurIPS Workshop Proposals 2025 – NeurIPS</a></li>

</ul>
</details>

**社区讨论**: 评论指出 STEM 研究中类似剥削早已存在，有人称 Algoverse 是已知做法的规模化版本。其他人质疑错误是如何被发现的，一名评论者强调负责人缺乏高级学位。一条《卫报》文章链接被分享，证实了这一争议。

**标签**: `#academic misconduct`, `#ML research`, `#ethics`, `#high school`, `#NeurIPS`

---

<a id="item-9"></a>
## [M5、DGX Spark、Strix Halo 与 RTX 6000 AI 推理基准对比](https://i.redd.it/mk82wx765r1h1.jpeg) ⭐️ 8.0/10

经过三天的标准化基准测试，对比 M5、DGX Spark、Strix Halo 和 RTX 6000 在 AI 推理上的表现，结果显示 RTX 6000 在模型适配 VRAM 时性能最佳，而 M5 在模型超出 VRAM 时性能保持稳定。 此次对比为 AI 推理硬件选型提供了实际权衡，凸显了内存带宽和 VRAM 溢出惩罚的重要性，帮助开发者在统一内存（Apple）与独立 GPU 方案间做出选择。 RTX 6000 内存带宽约 1800 GB/s，M5 约 600 GB/s，DGX Spark 和 Strix Halo 约 256 GB/s。长时间运行时，M5 MacBook Pro 温度保持在 80°C 左右但噪音类似游戏本，而 EVO X2（Strix Halo）存在散热问题。

reddit · r/LocalLLaMA · Signal_Ad657 · May 17, 19:49 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1tfzsd6/m5_vs_dgx_spark_vs_strix_halo_vs_rtx_6000/)

**背景**: AI 推理性能严重依赖内存带宽，每秒生成的 token 数大致与带宽成正比。Apple M5 等统一内存架构无需担心 VRAM 溢出，而 RTX 6000 等独立 GPU 在模型超过显存时性能骤降。DGX Spark 是 NVIDIA 的紧凑型 AI 超级计算机，Strix Halo 是 AMD 面向迷你 PC 的高性能 APU。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nvidia.com/en-us/products/workstations/dgx-spark/">Personal AI Supercomputer Powered by Blackwell | NVIDIA DGX</a></li>
<li><a href="https://www.gmktec.com/products/amd-ryzen™-ai-max-395-evo-x2-ai-mini-pc">GMKtec EVO-X2 AI Mini PC AMD Ryzen™ AI Max+ 395</a></li>
<li><a href="https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/">NVIDIA DGX Spark: great hardware, early days for the ecosystem</a></li>

</ul>
</details>

**社区讨论**: 高赞评论指出 RTX 6000 在小模型上胜出，但 M5 因统一内存在大模型上表现稳定。其他评论讨论价格差异（M5 Max 128GB 售价 5500 美元 vs DGX Spark 3800 美元），批评 Apple 不可升级和生态封闭，并质疑 M5 在并行请求上的性能（与搭配 vLLM 的 4090 相比）。

**标签**: `#hardware comparison`, `#AI inference`, `#benchmarking`, `#LLM`, `#Apple M5`

---

<a id="item-10"></a>
## [85 GPU 小时对比 Qwen3.6-27B 的 5 种 Abliteration 方法](https://www.reddit.com/r/LocalLLaMA/comments/1tfmocw/85_gpuhours_comparing_5_abliteration_methods_on/) ⭐️ 8.0/10

作者发布了 Abliterlitics，一个开源工具包，通过 85 GPU 小时的基准测试、安全评估和权重级取证，系统比较了 Qwen3.6-27B 模型的五种 abliteration 技术。分析显示，Heretic 和 Huihui 变体在保留能力方面表现最佳，而所有方法均实现了近乎完全的安全移除。 这项工作提供了首次严谨、开源的 abliteration 方法比较，帮助 LLM 安全社区理解能力保留与拒绝抑制之间的权衡。它建立了一种可复现的基准测试方法，可指导未来的对齐研究和模型选择。 作者从 Q8_K_P GGUF 文件中恢复了 safetensors，并对六个模型（基础模型加五个 abliterated 变体）进行了 85 小时的基准测试，包括 HarmBench、KL 散度和权重取证。AEON 变体的“增强能力”声明与数据矛盾，而 Abliterix 的能力保留最差。

reddit · r/LocalLLaMA · nathandreamfast · May 17, 11:18

**背景**: Abliteration 是一种技术，通过识别并抑制导致 LLM 拒绝行为的单个潜在方向来“取消审查”模型。Safetensors 是一种安全的张量文件格式，可防止代码执行；GGUF 是一种量化格式，可减小模型大小。这项工作利用这些格式来恢复和比较模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/blog/mlabonne/abliteration">Uncensor any LLM with abliteration</a></li>
<li><a href="https://github.com/NousResearch/llm-abliteration/">GitHub - NousResearch/llm-abliteration: Make abliterated models with transformers, easy and fast · GitHub</a></li>

</ul>
</details>

**社区讨论**: 社区高度赞赏这项工作，评论称其为“高努力帖子”并感谢作者。一位用户提出了建设性的技术反馈，建议测量每个 token 位置的分布变化而非仅第一个，并提供了示例代码。几位用户请求更简单的总结和最佳用例。

**标签**: `#abliteration`, `#LLM safety`, `#model alignment`, `#benchmarking`, `#open source`

---

<a id="item-11"></a>
## [llama.cpp 双 GPU 加速修复量化 KV 缓存](https://www.reddit.com/r/LocalLLaMA/comments/1tflngz/dual_gpu_llamacpp_speedup/) ⭐️ 8.0/10

贡献者 RedToasty 修复了 llama.cpp 的张量并行模式，使其支持量化 KV 缓存，从而在无需非量化缓存内存开销的情况下实现更快的多 GPU 推理。基准测试显示速度显著提升，例如在双 GPU 设置上从约 31 tokens/s 提升到约 50 tokens/s。 此修复解决了长期存在的限制，即用户不得不在张量并行（快速）和量化 KV 缓存（节省内存）之间做出选择。它使 llama.cpp 的多 GPU 推理在实际工作负载中更加实用，可能减少对 vLLM 等替代引擎的需求。 该修复在一个名为 llama.cpp_qts 的分支中实现，与主线版本相比改动极小。它在张量并行模式下支持量化的 K 和 V 缓存（例如 Q8_0），但贡献者指出多次请求后存在不稳定性，建议使用 llama-swap 等自动重启工具。该功能尚未合并到主线。

reddit · r/LocalLLaMA · Legitimate-Dog5690 · May 17, 10:24

**背景**: 张量并行将模型层拆分到多个 GPU 上以并行计算，提高吞吐量。然而，llama.cpp 的实现此前要求非量化的 KV 缓存，这会消耗大量内存。量化 KV 缓存可减少内存使用，但与张量并行不兼容，迫使人们做出取舍。此修复解决了这一不兼容问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://rocm.blogs.amd.com/artificial-intelligence/tensor-parallelism/README.html">Analyzing the Impact of Tensor Parallelism Configurations on LLM Inference Performance — ROCm Blogs</a></li>
<li><a href="https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/">Quantized KV Cache - vLLM</a></li>

</ul>
</details>

**社区讨论**: 社区对此修复反响热烈，许多用户表示有意从 vLLM 转向 llama.cpp。但有人指出不稳定性，建议使用自动重启方案。还有人建议在实际上下文长度下进行基准测试，因为对于大的 KV 缓存，层拆分可能更有效。一位用户指出，原版 llama.cpp 已经支持非量化 KV 缓存的张量并行。

**标签**: `#llama.cpp`, `#tensor parallelism`, `#multi-GPU`, `#inference optimization`, `#KV cache`

---

<a id="item-12"></a>
## [长鑫科技科创板 IPO，营收增长 719%](https://api3.cls.cn/share/article/2373399?os=android&amp;sv=8.7.8&amp;app=cailianpress) ⭐️ 8.0/10

长鑫科技已在科创板提交 IPO 招股说明书，披露 2026 年一季度营收 508 亿元，同比增长 719.13%，净利润 330.1 亿元，扭亏为盈。 此次 IPO 为投资者提供了投资中国领先 DRAM 制造商的难得机会，正值全球存储芯片热潮之际，标志着中国在半导体存储器领域的自给自足能力增强，将吸引大量投资者关注。 公司预计 2026 年上半年营收 1100-1200 亿元（同比增长 612%-677%），扣非归母净利润 520-580 亿元。IPO 正值全球 DRAM 供应短缺导致价格大幅上涨，利好中国存储芯片制造商。

telegram · zaihuapd · May 17, 11:05

**背景**: DRAM（动态随机存取存储器）是计算机和服务器的内存核心。长鑫科技是中国少数 DRAM 生产商之一，对科技自主可控至关重要。科创板是上海证券交易所为高科技和成长型企业设立的板块，类似于纳斯达克。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Dynamic_random-access_memory">Dynamic random-access memory - Wikipedia</a></li>

</ul>
</details>

**标签**: `#IPO`, `#semiconductor`, `#DRAM`, `#Chinese tech`, `#finance`

---