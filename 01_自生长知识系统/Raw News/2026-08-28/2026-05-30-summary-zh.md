---
layout: default
title: "Horizon Summary: 2026-05-30 (ZH)"
date: 2026-05-30
lang: zh
---

> 从 53 条内容中筛选出 16 条重要资讯。

---

1. [vLLM v0.22.0 发布：DeepSeek V4 成熟化与 Rust 前端](#item-1) ⭐️ 9.0/10
2. [通过探针定向微调让大语言模型表达真实置信度](#item-2) ⭐️ 9.0/10
3. [研究者发现 CBSE 在线阅卷系统严重漏洞](#item-3) ⭐️ 9.0/10
4. [加州议会通过《保护我们的游戏法案》](#item-4) ⭐️ 8.0/10
5. [AI 是否在重蹈前端“失落的十年”？](#item-5) ⭐️ 8.0/10
6. [Anthropic 年化收入达 470 亿美元](#item-6) ⭐️ 8.0/10
7. [为 FIPS 认证提出可加载加密模块](#item-7) ⭐️ 8.0/10
8. [抗议软件通过 jqwik 库瞄准 AI 编程代理](#item-8) ⭐️ 8.0/10
9. [单核（monokernel）在 AMD MI300X 上实现每秒 3300 个 token](#item-9) ⭐️ 8.0/10
10. [用户对 Qwen3.6-27B 量化版本进行基准测试](#item-10) ⭐️ 8.0/10
11. [多令牌预测将推理速度提升高达 3.34 倍](#item-11) ⭐️ 8.0/10
12. [英伟达预告 N1X 笔记本芯片：20 个 ARM 核心+6144 个 CUDA 核心，Computex 发布](#item-12) ⭐️ 8.0/10
13. [StepFun 发布 Step 3.7 Flash，196B 参数 MoE 模型](#item-13) ⭐️ 8.0/10
14. [比亚迪为城市领航辅助驾驶提供一年事故兜底](#item-14) ⭐️ 8.0/10
15. [中国首次将 9 款国产 AI 芯片纳入政府采购目录](#item-15) ⭐️ 8.0/10
16. [蓝色起源新格伦火箭静态点火测试爆炸](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [vLLM v0.22.0 发布：DeepSeek V4 成熟化与 Rust 前端](https://github.com/vllm-project/vllm/releases/tag/v0.22.0) ⭐️ 9.0/10

vLLM 发布了 v0.22.0 版本，包含来自 230 位贡献者的 459 次提交，主要亮点包括 DeepSeek V4 的显著强化、模型运行器 V2 向默认进发，以及实验性的 Rust 前端。关键改进有 NVFP4 融合 MoE 支持、分段 CUDA 图、MTP 推测解码和多级 KV 缓存卸载。 该版本显著提升了 DeepSeek V4（一种先进的 MoE 模型）的推理效率与模型支持，同时推动模型运行器 V2 走向更广泛的应用。实验性的 Rust 前端也表明 vLLM 正在探索使用更安全的系统语言来优化性能关键路径。 DeepSeek V4 现在拥有专用包、NVFP4 融合 MoE、完整与分段 CUDA 图支持以及 MTP 推测解码。模型运行器 V2 新增了一个选择器（oracle），可自动为 Qwen3 稠密模型启用它，并在存在 KV 连接器时自动回退到 MRv1。

github · khluu · 5月29日 10:28

**背景**: vLLM 是一个高吞吐量的 LLM 推理引擎，采用 PagedAttention 实现高效内存管理。DeepSeek V4 是一个混合专家（MoE）模型，需要专门的内核优化。NVFP4 融合 MoE 使用 4 位浮点加速专家计算，分段 CUDA 图减少图编译开销，MTP 推测解码利用多 Token 预测草稿模型加速生成。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.vllm.ai/en/v0.15.0/api/vllm/model_executor/layers/fused_moe/oracle/nvfp4/">vllm.model_executor.layers. fused _ moe .oracle. nvfp4</a></li>
<li><a href="https://docs.sglang.io/docs/advanced_features/piecewise_cuda_graph">Piecewise CUDA Graph - SGLang Documentation</a></li>
<li><a href="https://njannasch.dev/blog/mtp-speculative-decoding-qwen-3-6-5060ti/">MTP Speculative Decoding Actually Works on MoE: 144 t/s on a</a></li>

</ul>
</details>

**标签**: `#vllm`, `#LLM inference`, `#DeepSeek`, `#Rust`, `#open source`

---

<a id="item-2"></a>
## [通过探针定向微调让大语言模型表达真实置信度](https://www.reddit.com/r/MachineLearning/comments/1tqrtkn/making_llms_tell_you_how_confident_they_really/) ⭐️ 9.0/10

研究人员开发了探针定向微调（LoRA）方法，利用内部探针信号教会大语言模型口头表达真实的答案置信度，并通过激活补丁验证了因果效应。 这解决了大语言模型校准的关键问题：模型虽然能内部区分正确与错误答案（AUROC 达 0.76-0.88），但常表达过度自信（99%置信度），该方法通过简单高效的微调使表达置信度与内部知识对齐。 该方法使用 LoRA 微调，仅需几百个样本，在 M3 Ultra 上训练不到 10 分钟。激活补丁实验显示，在置信度位置交换隐藏状态与表达置信度之间的相关性达ρ=0.976，证实了因果效应。

reddit · r/MachineLearning · /u/Synthium- · 5月29日 05:15

**背景**: 大型语言模型常存在校准不佳的问题：它们能在内部检测自己是否知道答案（探针 AUROC 高达 0.88），但口头表达的置信度对所有回答都接近 100%。探针定向微调利用这一内部信号，将探针输出作为模型自身置信度输出的训练目标。激活补丁是一种通过交换不同运行间模型激活值，来检验特定激活是否对输出有因果影响的技术。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AUROC">AUROC</a></li>
<li><a href="https://mbrenndoerfer.com/writing/activation-patching">Activation Patching : Causal Tracing in Neural Networks - Interactive</a></li>
<li><a href="https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)">Fine - tuning (deep learning) - Wikipedia</a></li>

</ul>
</details>

**标签**: `#LLM`, `#confidence calibration`, `#fine-tuning`, `#probe`, `#LoRA`

---

<a id="item-3"></a>
## [研究者发现 CBSE 在线阅卷系统严重漏洞](https://ni5arga.com/blog/posts/hacking-cbse/) ⭐️ 9.0/10

这些漏洞影响数百万学生参加的高利害全国性考试系统，一旦被利用，可导致未经授权的成绩修改，破坏整个考试过程的公正性。 研究者发现系统使用了硬编码主密码、完全在客户端验证 OTP、允许绕过登录页面，并且存在 SQL 注入漏洞；他于 2026 年 2 月向 CERT-In 报告，但 CBSE 起初否认漏洞存在。

telegram · zaihuapd · 5月29日 05:52

**背景**: 硬编码密码是嵌入在源代码中的固定凭证，攻击者可轻易提取并绕过认证。客户端 OTP 验证意味着一次性密码在用户浏览器中校验，可通过浏览器开发者工具绕过。SQL 注入允许攻击者在数据库上执行任意 SQL 命令，可能读取或修改敏感数据。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.bleepingcomputer.com/news/security/hardcoded-password-found-in-cisco-software/">Hardcoded Password Found in Cisco Software</a></li>
<li><a href="https://security.stackexchange.com/questions/276635/what-security-risks-do-you-see-with-wrong-otps-appearing-in-application-logs">logging - What security risks do you see with wrong OTPs</a></li>
<li><a href="https://en.wikipedia.org/wiki/SQL_injection">SQL injection - Wikipedia</a></li>

</ul>
</details>

**标签**: `#security vulnerability`, `#CBSE`, `#online exam system`, `#India`, `#cybersecurity`

---

<a id="item-4"></a>
## [加州议会通过《保护我们的游戏法案》](https://www.invenglobal.com/articles/22330/stop-killing-games-movement-gains-momentum-california-assembly-passes-game-protection-bill) ⭐️ 8.0/10

加利福尼亚州议会通过了《保护我们的游戏法案》，要求游戏发行商保持数字销售游戏的功能性，否则将面临处罚。该法案现已提交至州参议院审议。 这项立法是数字消费者权益和游戏保护方面的重要一步，可能为其他州和国家树立先例。它将迫使发行商确保游戏在服务器关闭后仍可游玩，解决了游戏行业长期存在的问题。 该法案排除了通过订阅服务提供的游戏、免费游戏以及本身可无限期离线游玩的游戏。它还禁止继续销售或分发因服务终止而无法使用的游戏。

hackernews · TechTechTech · 5月29日 19:55 · [社区讨论](https://news.ycombinator.com/item?id=48328365)

**背景**: 许多现代游戏采用了始终在线 DRM 或要求持续的服务器连接才能运行，即使是单人模式也是如此。当发行商决定关闭这些服务器时，游戏变得无法游玩，导致消费者购买的商品失去功能。《保护我们的游戏法案》旨在要求发行商发布补丁或提供其他方法来保持游戏功能，例如移除服务器检查，从而保障消费者的访问权。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Always-on_DRM">Always - on DRM - Wikipedia</a></li>
<li><a href="https://www.howtogeek.com/think-denuvo-is-bad-be-glad-we-dont-have-these-old-drm-solutions/">Think Denuvo Is Bad? Be Glad We Don't Have These 3 DRM Solutions...</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍支持该法案，但提出了潜在漏洞的担忧，例如发行商创建空壳公司以规避责任。一些人担心对订阅和免费游戏的豁免可能会促使向这些模式转变，而另一些人则希望法案也能涵盖订阅游戏，以确保更广泛的保护。

**标签**: `#gaming`, `#legislation`, `#consumer rights`, `#digital preservation`

---

<a id="item-5"></a>
## [AI 是否在重蹈前端“失落的十年”？](https://mastrojs.github.io/blog/2026-05-23-is-AI-causing-a-repeat-of-frontends-lost-decade/) ⭐️ 8.0/10

一篇博文指出，AI 工具正在导致前端专业知识和代码质量下降，让人联想到当年 jQuery 和 React 等框架抽象掉基本 Web 技能的“失落的十年”。 这场争论之所以重要，是因为它揭示了 AI 驱动的效率提升与前端工匠精神丧失之间的紧张关系，可能影响网页可访问性、性能和整体软件质量。 文章提到过去开发者因框架抽象而丧失底层技能的时期，而现在的 AI 代码生成可能加速这一趋势。社区评论反驳称，早期的转变大多是良性的，AI 同样减少了偶然复杂性。

hackernews · xyzal · 5月29日 11:09 · [社区讨论](https://news.ycombinator.com/item?id=48321631)

**背景**: 前端开发的“失落的十年”指的是 2000 年代末，jQuery 以及后来的 React、Vue 和 Angular 将直接 DOM 操作抽象化，导致一代开发者对原生 HTML、CSS 和 JavaScript 不够熟悉。如今，AI 代码助手能够生成完整组件，进一步拉大了开发者与基础知识的距离，这一模式正在重演。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://mastrojs.github.io/blog/2026-05-23-is-AI-causing-a-repeat-of-frontends-lost-decade/">Is AI causing a repeat of Frontend ’s Lost Decade ? | Mastro Blog</a></li>
<li><a href="https://en.m.wikipedia.org/wiki/Front-end_web_development">Front-end web development - Wikipedia</a></li>
<li><a href="https://aiespionage.net/tech-deep-dives/is-ai-causing-a-repeat-of-front-end-s-lost-decade/">Is AI causing a repeat of Front end 's Lost Decade ? - AI Espionage</a></li>

</ul>
</details>

**社区讨论**: 评论情绪不一：有人认同 AI 正在降低质量，也有人认为过去所谓的“专业知识”往往是在处理不必要的复杂性。多位评论者指出，过去的行业并非充满熟练工匠，只要更多人能构建东西，这种权衡是可以接受的。

**标签**: `#AI`, `#frontend development`, `#software engineering`, `#quality`, `#community debate`

---

<a id="item-6"></a>
## [Anthropic 年化收入达 470 亿美元](https://simonwillison.net/2026/May/29/anthropic/#atom-everything) ⭐️ 8.0/10

Anthropic 在 650 亿美元 H 轮融资公告中披露，其年化收入于 2026 年 5 月突破 470 亿美元，而 2025 年底仅为 90 亿美元。 这种快速增长——不到六个月从 90 亿跃升至 470 亿美元——展示了企业级 AI 应用的惊人速度，使 Anthropic 成为所有行业中增长最快的公司之一，并在估值上超越 OpenAI。 年化收入是基于最近一个月收入乘以 12 的年化预测值，不同于年度经常性收入（ARR）。此前的里程碑包括 2026 年 2 月的 140 亿美元和 2026 年 4 月的 300 亿美元。

rss · Simon Willison · 5月29日 01:23

**背景**: 年化收入是快速增长初创公司常用的指标，通过将近期月收入推算至全年得出。它提供了前瞻性估计，但可能波动较大。Anthropic 是 Claude 系列 AI 模型的开发者，通过大规模融资来扩展算力、模型训练和商业化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Revenue">Revenue - Wikipedia</a></li>
<li><a href="https://www.investopedia.com/terms/r/runrate.asp">investopedia.com/terms/r/runrate.asp</a></li>

</ul>
</details>

**标签**: `#Anthropic`, `#AI industry`, `#revenue`, `#funding`, `#business milestone`

---

<a id="item-7"></a>
## [为 FIPS 认证提出可加载加密模块](https://lwn.net/Articles/1073759/) ⭐️ 8.0/10

亚马逊工程师 Jay Wang 提出补丁系列，将 Linux 内核加密子系统解耦为独立的可加载模块，使得通过 FIPS 认证的加密模块可以在多个内核版本间复用，无需重新完整认证。 该提案解决了需要 FIPS 合规的组织的主要痛点，因为内核更新当前会使认证失效并迫使进行长时间的重新认证周期，从而降低维护 FIPS 认证 Linux 部署的成本和延迟。 该提案必须克服三个障碍：构建系统无法轻松将内置对象收集到模块中，内核的单向符号解析阻止模块向主内核导出符号，以及加密子系统必须在根文件系统挂载前的启动早期可用。

rss · LWN.net · 5月29日 14:29

**背景**: FIPS（联邦信息处理标准）140-3 认证是一种严格的加密模块验证过程，被美国政府机构和受监管行业所需要。认证绑定到确切的二进制文件，因此任何内核更改都会使其失效。目前，Linux 加密被构建到主内核中，导致每次更新后都需要长时间的重新认证。该提案旨在将加密代码隔离到可加载模块中，认证一次即可跨内核版本复用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.corsec.com/fips-certification-process/">FIPS Certification Process - Corsec Security, Inc.</a></li>
<li><a href="https://ordr.net/blog/ordr-and-fips-certification">FIPS Certification and Why Its Important for the Public Sector - ORDR</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#crypto`, `#FIPS`, `#kernel modules`, `#security`

---

<a id="item-8"></a>
## [抗议软件通过 jqwik 库瞄准 AI 编程代理](https://lwn.net/Articles/1075315/) ⭐️ 8.0/10

2026 年 5 月 25 日，jqwik 属性基础测试库 1.10.0 版本发布，其中包含指示 AI 编程代理删除 jqwik 测试和源代码的代码，这是一种新型抗议软件攻击，能够规避传统安全扫描器。 此事件突显了一类新型供应链攻击，专门针对 AI 辅助开发工作流，嵌入在纯文本中的恶意指令能够绕过当前软件组成分析工具。这引发了对 AI 编程代理信任度的紧迫担忧，并需要新的检测机制。 该攻击使用一个简单的 68 字节 ASCII 的 System.out.print 语句，使其对寻找安装钩子、网络调用或文件系统写入的扫描器不可见。该更改由合法维护者通过正常构建流程提交并发布，因此通过了 SLSA 来源检查。

rss · LWN.net · 5月29日 14:09

**背景**: jqwik 是一个用于 Java 的属性基础测试库，它根据代码应满足的属性自动生成测试用例。抗议软件（protestware）是指为抗议某项政策或行为而引入有害行为的软件。传统的供应链安全工具专注于检测网络调用、文件写入或混淆代码，但它们并非为捕捉针对 AI 代理的纯 ASCII 文本指令而设计。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://jqwik.net/">jqwik : Property - Based Testing in Java</a></li>
<li><a href="https://socket.dev/blog/a-short-history-of-protestware">A Short History of Protestware - Socket</a></li>
<li><a href="https://www.baeldung.com/java-jqwik-property-based-testing">Property - Based Testing with jqwik | Baeldung</a></li>

</ul>
</details>

**标签**: `#supply-chain security`, `#AI agents`, `#protestware`, `#Java`, `#vulnerability`

---

<a id="item-9"></a>
## [单核（monokernel）在 AMD MI300X 上实现每秒 3300 个 token](https://www.reddit.com/r/MachineLearning/comments/1tqvuz9/building_a_monokernel_for_llm_inference_on_amd/) ⭐️ 8.0/10

研究人员构建了一个单核（monokernel），在 AMD MI300X 上以单个 GPU 程序运行整个 LLM 解码序列，在不使用推测解码或量化的情况下，每个请求每秒输出高达 3300 个 token。 这证明了针对硬件拓扑的优化可以大幅降低 AMD GPU 上的 LLM 推理延迟，有可能缩小与 NVIDIA H100 在低延迟服务方面的差距。 该工作目前在一个 2B 参数的小型编码模型上运行，批大小为 1，使用 8 个 MI300X GPU，作者计划将其扩展到大型前沿混合专家（MoE）模型。

reddit · r/MachineLearning · /u/averne_ · 5月29日 08:54

**背景**: 单核（monokernel）是一个单一的 GPU 内核，融合了模型前向传播的所有操作，减少了启动开销并提高了内存效率。AMD MI300X GPU 具有独特的芯片组架构，带有连接计算单元的 I/O 芯片（IOD）；将内存访问模式映射到物理芯片布局是实现峰值性能的关键。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://rocm.docs.amd.com/en/develop/how-to/programming_guide.html">Programming guide — ROCm Documentation</a></li>
<li><a href="https://hazyresearch.stanford.edu/blog/2025-05-27-no-bubbles">Look Ma, No Bubbles! Designing a Low-Latency Megakernel for...</a></li>

</ul>
</details>

**标签**: `#LLM inference`, `#GPU optimization`, `#AMD MI300X`, `#monokernel`, `#deep learning systems`

---

<a id="item-10"></a>
## [用户对 Qwen3.6-27B 量化版本进行基准测试](https://www.reddit.com/r/LocalLLaMA/comments/1tr9vzn/qwen3627b_quantization_benchmark/) ⭐️ 8.0/10

一位用户使用 KL 散度（KLD）和相同 Top P 指标对 Qwen3.6-27B 模型的多种量化版本进行了基准测试，比较了 Unsloth、mradermacher 等从 Q8 到 Q2 的量化版本。 该基准测试为本地部署 Qwen3.6-27B 的实践者提供了实用指导，帮助他们基于客观指标而非经验报告选择具有最佳质量与显存权衡的量化级别。 测试使用 llama.cpp 的 llama-perplexity，上下文长度为 8192 个 token，KV 缓存量化为 q8_0 以确保模型能放入 GPU。结果显示 Unsloth 的 Q4_K_XL 提供了良好的质量折衷，而 mradermacher 的 Q6_K 在 KLD 和 token 选择匹配上优于 Unsloth 的 Q6_K。

reddit · r/LocalLLaMA · /u/bobaburger · 5月29日 17:53

**背景**: 量化将模型权重的精度降低到更低的位宽（例如从 FP16 到 4 位），从而减少内存使用并提高推理速度，但会牺牲一些准确性。KLD 衡量量化模型输出概率分布与原始模型的偏差程度，而相同 Top P 则跟踪量化模型选择与基础模型相同最高 token 的频率。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://fireworks.ai/blog/fireworks-quantization">How Fireworks evaluates quantization precisely and interpretably</a></li>
<li><a href="https://cosmo-edge.com/unsloth-dynamic-20-ggufs-llm-quantization/">Unsloth Dynamic 2.0 GGUFs: the new benchmark for LLM</a></li>
<li><a href="https://github.com/ssfdre38/gemma4-turbo">GitHub - ssfdre38/gemma4-turbo: IQ 4 _ XS quantization of Gemma...</a></li>

</ul>
</details>

**标签**: `#LLM`, `#quantization`, `#benchmark`, `#Qwen`, `#local LLM`

---

<a id="item-11"></a>
## [多令牌预测将推理速度提升高达 3.34 倍](https://www.reddit.com/r/LocalLLaMA/comments/1trf0r0/i_tested_mtp_on_vllm_and_llamacpp_for_gemma_4/) ⭐️ 8.0/10

一位 Reddit 用户在 RTX PRO 6000 Blackwell GPU 上，使用 vLLM 和 llama.cpp 对 Gemma 4 31B 和 Qwen 3.6 27B 进行多令牌预测（MTP）基准测试，最高达到 132.52 tok/s（加速 3.34 倍）。 MTP 是一种推测解码技术，能在不显著降低质量的前提下大幅提升推理吞吐量，使大型密集模型更适用于实时应用和本地部署。 最佳结果是 vLLM 搭配 Gemma 4 使用 n=5 个推测令牌，达到 132.52 tok/s，基线为 39.69 tok/s；llama.cpp 搭配 Qwen 3.6 在 n=3 时达到峰值 117.70 tok/s。草稿模型非常小（Gemma 4 为 76M 参数），VRAM 开销似乎可忽略不计。

reddit · r/LocalLLaMA · /u/FantasticNature7590 · 5月29日 20:42

**背景**: 多令牌预测（MTP）是一种推测解码技术：轻量级草稿模型预测多个未来令牌，目标模型在一次前向传播中验证它们。这分摊了内存带宽成本，加速了自回归解码。vLLM 和 llama.cpp 是流行的开源推理引擎，近期加入了 MTP 支持。GGUF 是一种用于高效本地部署的量化格式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@bnjmn_marie/gguf-quantization-for-fast-and-memory-efficient-inference-on-your-cpu-d10fbe58fbca">GGUF Quantization for Fast and Memory-Efficient Inference... | Medium</a></li>
<li><a href="https://ggufloader.github.io/what-is-gguf.html">What is GGUF ? Complete Guide to GGUF Format & Quantization</a></li>

</ul>
</details>

**标签**: `#Multi-Token Prediction`, `#vLLM`, `#llama.cpp`, `#LLM inference`, `#benchmarking`

---

<a id="item-12"></a>
## [英伟达预告 N1X 笔记本芯片：20 个 ARM 核心+6144 个 CUDA 核心，Computex 发布](https://www.reddit.com/r/LocalLLaMA/comments/1tracb5/nvidia_teases_new_pc_laptop_chip_to_be_announced/) ⭐️ 8.0/10

英伟达预告了新款基于 ARM 架构的笔记本处理器 N1X，配备 20 个 ARM 核心和 6144 个基于 Blackwell 架构的 CUDA 核心。该芯片预计将于 2026 年 6 月 2 日在 Computex 上正式发布，本质上是 DGX Spark 超级芯片的低功耗版本。 这标志着英伟达携自研 ARM CPU 大举进军 PC 笔记本市场，可能对 AMD 的 Strix Halo 和高通的 Snapdragon X 构成挑战。该芯片的高 CUDA 核心数量可能使其在笔记本电脑上进行本地 LLM 推理时异常强大。 N1X 预计是 DGX Spark 所用 GB10 Grace Blackwell 超级芯片的变体，但针对低功耗笔记本系统进行了优化。早期泄露显示采用异构 big-little 架构，最高支持 128GB 统一内存，但软件支持和定价仍是关键问题。

reddit · r/LocalLLaMA · /u/Terminator857 · 5月29日 18:07

**背景**: 英伟达传统上专注于游戏和专业用途的独立 GPU，而将 CPU 设计留给英特尔和 AMD 等合作伙伴。N1X 代表了英伟达首次认真尝试打造自研的基于 Arm 的笔记本电脑 CPU，与联发科合作开发。此举效仿了苹果 M 系列芯片和高通 Snapdragon X 系列的类似努力。DGX Spark 是一款售价约 4700 美元的桌面 AI 超级计算机，面向开发者和研究人员。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.tomsguide.com/computing/cpus/nvidia-n1x-cpu-everything-we-know-so-far">Nvidia N1X and N1 CPU: Everything we know so far - Tom's Guide</a></li>
<li><a href="https://www.digitalfoundry.net/news/2026/04/nvidia-is-making-laptops-now-n1n1x-leak-shows-a-128gb-monster-derived-from-their-dgx-spark-desktop-ai-workhorse">Nvidia Is Making Laptops Now: N1/ N1X Leak Shows a 128GB Monster...</a></li>
<li><a href="https://www.notebookcheck.net/Nvidia-N1X-leak-points-to-limited-2026-availability.1282855.0.html">Nvidia N1X leak points to limited 2026 availability</a></li>

</ul>
</details>

**社区讨论**: Reddit 评论者对硬件规格感到兴奋，但仍对软件支持持怀疑态度，特别是 Windows on ARM 和游戏兼容性。许多人指出，英伟达必须解决微软和高通此前 ARM 笔记本尝试在市场上反响不佳的问题。定价是讨论的主要焦点，人们希望 N1X 笔记本将比 4700 美元的 DGX Spark 便宜得多。

**标签**: `#Nvidia`, `#ARM`, `#Laptop Chip`, `#LLM`, `#Computex`

---

<a id="item-13"></a>
## [StepFun 发布 Step 3.7 Flash，196B 参数 MoE 模型](https://www.reddit.com/r/LocalLLaMA/comments/1tqloii/stepfun_37_flash/) ⭐️ 8.0/10

StepFun 发布了 Step 3.7 Flash，这是一个多模态混合专家模型，总参数量 196B（激活 11B），可在 128GB 内存上本地运行，并在编程和智能体任务上取得了优异的基准成绩。 该模型在智能体和编程基准上媲美更大模型，为本地部署提供了极具竞争力的选择，对本地大语言模型社区和智能体工作流开发尤为重要。 该模型内置 1.8B 的视觉 Transformer（ViT），基准测试包括 SWE-Bench Pro 56.26%（超过 DeepSeek V4 Flash，与 Gemini 3.5 Flash 持平）、DeepSearchQA F1 92.82% 和带工具的 HLE 47.2%。用户可通过 OpenRouter 和 NVIDIA NIM 使用，无需自行部署。

reddit · r/LocalLLaMA · /u/Everlier · 5月29日 00:32

**背景**: MoE（混合专家）模型每个词元仅激活部分参数，从而在降低计算成本的同时实现大容量。SWE-Bench Pro 是评估真实软件工程任务的挑战性基准，DeepSearchQA 则测试多步信息检索能力。StepFun 是一家专注于高效大语言模型开发的中国人工智能公司。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://scaleapi.github.io/SWE-bench_Pro-os/">SWE-Bench Pro</a></li>
<li><a href="https://huggingface.co/datasets/google/deepsearchqa">google/ deepsearchqa · Datasets at Hugging Face</a></li>

</ul>
</details>

**标签**: `#LLM`, `#MoE`, `#Local LLM`, `#Multimodal`, `#Model Release`

---

<a id="item-14"></a>
## [比亚迪为城市领航辅助驾驶提供一年事故兜底](https://news.mydrivers.com/1/1125/1125729.htm) ⭐️ 8.0/10

比亚迪宣布，为其城市领航辅助驾驶（城市 NOA）提供一年事故兜底，承担因辅助驾驶导致的本车全部经济损失，且不设上限。 这项政策可能为汽车行业树立先例，增强消费者对辅助驾驶技术的信心，并可能加速自动驾驶功能的普及。 该保障适用于天神之眼 A、B 车型的新车用户（自提车起一年内），以及升级到天神之眼 5.0 的老车主。天神之眼 C 选装价为 12000 元。

telegram · zaihuapd · 5月29日 01:03

**背景**: 城市领航辅助驾驶（城市 NOA）是一种高级辅助驾驶系统，能够在城市道路实现自动导航，包括变道、转弯和红绿灯响应。比亚迪的天神之眼（DiPilot）是其辅助驾驶系统系列，A、B、C 版本提供不同能力等级。辅助驾驶事故的责任问题一直是消费者和监管机构关注的关键点。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ee.ofweek.com/2026-05/ART-8110-2801-30688887.html">智 驾 竞赛比亚迪丢王炸：兜底 城 市 NOA... - OFweek电子工程网</a></li>
<li><a href="https://aikahao.xcar.com.cn/video/3782133.html">aikahao.xcar.com.cn/video/3782133.html</a></li>

</ul>
</details>

**标签**: `#Autonomous driving`, `#Automotive`, `#BYD`, `#Assisted driving`, `#Liability`

---

<a id="item-15"></a>
## [中国首次将 9 款国产 AI 芯片纳入政府采购目录](https://www.tomshardware.com/tech-industry/semiconductors/china-certifies-nine-domestic-ai-chips-for-government-procurement) ⭐️ 8.0/10

中国信息安全测评中心首次在安全认证框架下新增“AI 训练与推理芯片”品类，共 9 款国产 AI 处理器通过认证，可用于政府采购。认证厂商包括华为（昇腾）、阿里（平头哥镇武）、壁仞科技和海光信息，而寒武纪和百度昆仑芯未出现。 这标志着中国官方首次正式认可国产 AI 芯片用于政府机构，可能加速公共部门替换国外芯片（如 NVIDIA），并推动国内 AI 硬件生态发展。 认证有效期为三年，将作为政府机构和国有企业采购的依据。九款芯片覆盖多种 AI 加速能力，但未公开具体性能指标。

telegram · zaihuapd · 5月29日 08:41

**背景**: “安可”安全采购目录是中国政府为保障信息安全而设立的硬件和软件采购清单，此前主要涵盖 CPU 等组件，这是首次纳入 AI 加速器。例如，华为昇腾系列采用自主架构，专为 AI 训练和推理设计。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.bbc.com/zhongwen/articles/cgrp5krzp8qo/simp">bbc.com/zhongwen/articles/cgrp5krzp8qo/simp</a></li>
<li><a href="https://m.ebrun.com/669634.html">“死磕”鲲鹏 昇 腾 生态的极客们 要搞点大事情 - AI - 亿邦动力</a></li>

</ul>
</details>

**标签**: `#AI chips`, `#China`, `#government procurement`, `#security certification`, `#technology policy`

---

<a id="item-16"></a>
## [蓝色起源新格伦火箭静态点火测试爆炸](https://arstechnica.com/space/2026/05/blue-origins-new-glenn-rocket-just-exploded-during-a-static-fire-test/) ⭐️ 8.0/10

2026 年 5 月 28 日，蓝色起源的新格伦火箭在卡纳维拉尔角的静态点火测试中发生爆炸，火箭被毁，发射台基础设施受损，无人员伤亡。 此次爆炸严重延误了蓝色起源的发射计划，并影响了 NASA 的阿尔忒弥斯月球着陆计划（蓝色起源承担了着陆器和月球车的发射任务），同时也打乱了亚马逊的柯伊伯计划卫星部署。 爆炸发生在一级火箭七台 BE-4 甲烷发动机的静态点火测试期间，火箭全毁，发射台的闪电防护塔倒塌。原计划 NG-4 任务发射 48 颗柯伊伯计划卫星。

telegram · zaihuapd · 5月29日 11:08

**背景**: 新格伦是蓝色起源的重型可重复使用火箭，由七台以液氧甲烷为燃料的 BE-4 发动机提供动力。静态点火测试是发射前的常规检查，火箭被固定，发动机短时点火。此次爆炸对尚未实现轨道飞行的蓝色起源来说是重大挫折。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/BE-4">BE-4 - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Project_Kuiper">Project Kuiper</a></li>

</ul>
</details>

**标签**: `#space`, `#Blue Origin`, `#New Glenn`, `#NASA`, `#rocket explosion`

---