---
layout: default
title: "Horizon Summary: 2026-05-20 (ZH)"
date: 2026-05-20
lang: zh
---

> From 44 items, 11 important content pieces were selected

---

1. [Andrej Karpathy 加入 Anthropic 预训练团队](#item-1) ⭐️ 9.0/10
2. [CISA 承包商在 GitHub 上泄露 AWS GovCloud 密钥](#item-2) ⭐️ 9.0/10
3. [DeepSeek 漏洞：空对话输入'<think'泄露用户数据](#item-3) ⭐️ 9.0/10
4. [谷歌发布 Gemini Omni，支持对话式视频编辑](#item-4) ⭐️ 9.0/10
5. [谷歌重新设计搜索框，集成人工智能功能](#item-5) ⭐️ 8.0/10
6. [Forge 通过护栏将 8B 模型准确率从 53% 提升至 99%](#item-6) ⭐️ 8.0/10
7. [苹果发布搭载 Apple Intelligence 和代理式 AI 的新辅助功能](#item-7) ⭐️ 8.0/10
8. [Gemini 3.5 Flash 发布，价格更高，集成广泛](#item-8) ⭐️ 8.0/10
9. [提议重构 Linux this_cpu 操作以提升性能](#item-9) ⭐️ 8.0/10
10. [CXL 使内存管理问题恶化及未来发展方向](#item-10) ⭐️ 8.0/10
11. [砺算 7G100 显卡 5 月 20 日预售](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Andrej Karpathy 加入 Anthropic 预训练团队](https://twitter.com/karpathy/status/2056753169888334312) ⭐️ 9.0/10

Andrej Karpathy 在 X 平台宣布正式加入 Anthropic，将专注于预训练团队的工作，该团队负责训练 Claude 模型的核心知识与能力。 Karpathy 是极具影响力的 AI 研究者和教育家，他的加入表明 Anthropic 在前沿 AI 研究领域的实力增强，可能对模型开发和 AI 教育产生深远影响。 Karpathy 将负责 Anthropic 的预训练团队，该团队负责 Claude 的大规模训练任务。他此前创办了 AI 教育公司 Eureka Labs，并首创了“vibe coding”这一 AI 辅助编程术语。

hackernews · dmarcos · May 19, 15:07 · [社区讨论](https://news.ycombinator.com/item?id=48194352)

**背景**: 预训练是一种自监督学习技术，模型首先在大规模无标签数据上训练以学习通用表征，然后针对特定任务进行微调。Karpathy 是 OpenAI 联合创始人、前 Tesla AI 总监，以及知名教育家，以 nanoGPT 项目和 YouTube 频道著称。Anthropic 是一家领先的 AI 安全公司，开发了 Claude 模型系列。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Generative_pre-trained_transformer">Generative pre - trained transformer - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区对 Karpathy 加入 Anthropic 普遍表示兴奋，许多人希望他能在 NDA 限制下继续教育工作。部分用户担忧 Anthropic 成为吸收顶尖人才的行业巨头，而其他人则指出 Karpathy 在最近的采访中已暗示了这一动向。

**标签**: `#AI`, `#Anthropic`, `#Andrej Karpathy`, `#machine learning`, `#industry news`

---

<a id="item-2"></a>
## [CISA 承包商在 GitHub 上泄露 AWS GovCloud 密钥](https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/) ⭐️ 9.0/10

一名 CISA 承包商不慎在公共 GitHub 仓库中发布了 AWS GovCloud 访问密钥以及一个 CSV 文件，其中包含数十个 CISA 内部系统的明文用户名和密码。 此次泄露暴露了高度敏感的美国政府云基础设施和内部凭证，损害了国家安全，并突显了安全实践和事件响应方面的严重失误。 泄露的凭证包括 CISA Workspace 环境的 AWS GovCloud 密钥，以及一个名为“AWS-Workspace-Firefox-Passwords.csv”的文件，内含明文密码。该承包商在接到泄露通知后未能做出回应。

hackernews · LelouBil · May 19, 07:45 · [社区讨论](https://news.ycombinator.com/item?id=48190454)

**背景**: AWS GovCloud（美国）是一个合规的云环境，旨在为美国政府机构托管敏感和受控的非涉密信息，仅限美国人员访问。CISA（网络安全和基础设施安全局）是负责保护国家关键基础设施免受网络威胁的联邦机构。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://aws.amazon.com/govcloud-us/">AWS GovCloud (US) - Amazon Web Services</a></li>
<li><a href="https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/">AWS Services by Region</a></li>

</ul>
</details>

**社区讨论**: 评论者对缺乏回应和使用明文密码表示震惊，有人指出外国情报机构可能会将此事件误认为是蜜罐。其他人则讽刺地指出，AWS 提供了更安全的服务功能却未被使用。

**标签**: `#security`, `#breach`, `#CISA`, `#AWS`, `#GovCloud`

---

<a id="item-3"></a>
## [DeepSeek 漏洞：空对话输入'<think'泄露用户数据](https://t.me/zaihuapd/41461) ⭐️ 9.0/10

DeepSeek 的 Web 和 API 对话系统中发现了一个严重的会话隔离漏洞，攻击者在空对话中发送未闭合的'<think'字符串即可获取其他用户的对话历史，包括敏感信息。 该漏洞带来了严重的隐私风险，可能暴露 DeepSeek 用户的私人代码、API 密钥和个人对话，削弱了对 AI 聊天服务的信任，并凸显了多租户系统中建立强大会话隔离的必要性。 该漏洞由报告者 cancat2024 于 2026 年 5 月 11 日负责任地披露，影响 DeepSeek 的 Web 界面和 API；攻击者只需在新开的空对话中提交未闭合的'<think'字符串即可触发数据泄露。

telegram · zaihuapd · May 19, 11:33

**背景**: 会话隔离是一种安全机制，确保每个用户的聊天会话相互独立。'<think'令牌是某些 AI 模型用来指示推理或内部思考过程的特殊令牌。该漏洞表明 DeepSeek 在处理不完整的特殊令牌时存在缺陷，导致模型错误地检索其他会话中的数据。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/tajerek/deepseek-web-api-proxy">GitHub - tajerek/ deepseek -web-api-proxy: OpenAI-compatible API...</a></li>
<li><a href="https://arxiv.org/html/2405.08644v1">Thinking Tokens for Language Modeling - arXiv.org</a></li>
<li><a href="https://huggingface.co/papers/2405.08644">Paper page - Thinking Tokens for Language Modeling</a></li>

</ul>
</details>

**社区讨论**: 在 GitHub 上，社区成员指出第三方部署也存在同样行为，表明该问题可能源于模型中的幻觉效应，而非单纯的会话管理缺陷。

**标签**: `#security`, `#vulnerability`, `#DeepSeek`, `#data leakage`, `#AI`

---

<a id="item-4"></a>
## [谷歌发布 Gemini Omni，支持对话式视频编辑](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/) ⭐️ 9.0/10

谷歌发布了全新的多模态 AI 模型 Gemini Omni，用户可以通过自然语言对话编辑视频，具备物理规律理解、角色一致性保持和 SynthID 数字水印等能力。首个型号 Gemini Omni Flash 已向 Google AI Plus、Pro 和 Ultra 订阅用户开放，支持在 Gemini 应用、Google Flow、YouTube Shorts 和 YouTube Create App 中使用。 这标志着向直观的 AI 辅助视频创作迈出了重要一步，可能降低内容创作者的门槛，并支持更动态的实时编辑。SynthID 水印的加入也回应了人们对 AI 生成内容真实性的日益关注。 该模型具备对重力、流体力学等物理规律的直观理解，并能确保多次编辑中角色一致性。所有生成的视频都嵌入了 SynthID 数字水印以确保透明度，谷歌计划在未来几周内向开发者开放 API。

telegram · zaihuapd · May 19, 18:23

**背景**: 多模态 AI 模型能处理文本、图像和音频等多种数据类型。Gemini Omni 是谷歌最新的此类模型，将推理与创作能力融合，支持通过自然语言直接编辑视频。SynthID 由 Google DeepMind 开发，能在 AI 生成内容中嵌入人类无法感知的水印，并可通过专用工具检测，有助于区分 AI 内容与真实拍摄画面。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/">Introducing Gemini Omni</a></li>
<li><a href="https://deepmind.google/models/synthid/">SynthID — Google DeepMind</a></li>

</ul>
</details>

**社区讨论**: 社区评论持谨慎乐观态度，但对物理真实感提出批评。用户指出模型违反物理定律的具体例子（例如弹珠无故加速、积木塔砖块消失）。一些人认为其不如现有工具如 Seedance，另一些人指出视频生成在深层空间理解方面仍存在根本性问题。

**标签**: `#multimodal AI`, `#video generation`, `#Google Gemini`, `#AI model`, `#natural language processing`

---

<a id="item-5"></a>
## [谷歌重新设计搜索框，集成人工智能功能](https://blog.google/products-and-platforms/products/search/search-io-2026/) ⭐️ 8.0/10

在 2026 年 Google I/O 大会上，谷歌宣布对搜索框进行重大重新设计，集成了由 Gemini 大型语言模型提供支持的全新 AI 模式，直接提供综合答案，而不仅仅是链接。 这一转变可能根本改变用户与搜索的交互方式，减少对外部网站的流量，并引发对信息可靠性和网络出版未来的担忧。 新的搜索框放弃了经典的蓝色链接格式，呈现从多个来源提取但可能缺乏明确归属的 AI 生成摘要，用户可以选择进入“AI 模式”以获得对话式回答。

hackernews · berkeleyjunk · May 19, 18:34 · [社区讨论](https://news.ycombinator.com/item?id=48197370)

**背景**: 谷歌长期以来一直是占主导地位的搜索引擎，使用算法对网页进行排名。像 Gemini 这样的大型语言模型（LLM）可以通过基于训练数据预测单词来生成类似人类的文本，从而实现更直接的答案风格。在 2026 年 I/O 大会上，谷歌深化了对 AI 优先搜索的承诺。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Gemini">Google Gemini - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者表达了对 AI 生成答案的担忧，这些答案听起来权威，但可能汇总了不可靠的来源，以及“谷歌归零”导致原始网站流量枯竭的风险。一些用户不信任 LLM 输出的事实性，更倾向于主要来源。

**标签**: `#google`, `#search`, `#AI`, `#LLM`, `#UX`

---

<a id="item-6"></a>
## [Forge 通过护栏将 8B 模型准确率从 53% 提升至 99%](https://github.com/antoinezambelli/forge) ⭐️ 8.0/10

Antoine Zambelli 发布了 Forge，这是一个开源可靠性层，通过领域无关的护栏大幅提升本地 LLM 在多步代理任务上的准确率，使 8B 模型从 53% 提升至 99.3%。 Forge 将免费本地模型与昂贵前沿 API 之间的准确率差距缩小到 1 个百分点以内，使得无需云成本的实用自托管代理系统成为可能。它还揭示了基础设施因素（如服务后端选择）对性能的关键影响，这些因素在标准基准测试中常被忽略。 Forge 包含五个可独立开关的护栏层；根据消融研究，重试提示（retry nudges）和错误恢复（error recovery）影响最大。该系统引入了一个新的 ToolResolutionError 异常类，用于区分工具返回数据和返回空结果，防止静默数据污染。

hackernews · zambelli · May 19, 12:23 · [社区讨论](https://news.ycombinator.com/item?id=48192383)

**背景**: 代理工作流涉及多步骤任务，LLM 需迭代调用工具并进行推理。没有护栏时，单步错误会累积：90% 的单步准确率在 5 步后失败率约 40%。Forge 的护栏通过添加重试机制、错误恢复、步骤执行和针对消费级硬件优化的上下文管理来解决这一问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@prklipi/guardrails-in-llm-systems-building-safe-and-reliable-ai-applications-1b4780798720">Guardrails in LLM Systems: Building Safe and Reliable AI... | Medium</a></li>
<li><a href="https://www.ibm.com/think/topics/agentic-workflows">What are agentic workflows? - IBM</a></li>

</ul>
</details>

**社区讨论**: 社区成员普遍称赞 Forge，指出配备适当框架的小型本地模型可以表现出色。一位用户强调工具调用歧义（如 grep 返回退出码 1）是常见故障模式，而重试提示正好解决了这一问题。另一位用户分享了在前沿规模上的类似经验，以及适当规模解决方案的价值。

**标签**: `#LLM`, `#guardrails`, `#agentic tasks`, `#open-source`, `#reliability`

---

<a id="item-7"></a>
## [苹果发布搭载 Apple Intelligence 和代理式 AI 的新辅助功能](https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/) ⭐️ 8.0/10

苹果宣布了由 Apple Intelligence 驱动的新辅助功能，包括能够自主为残障用户执行任务的代理式 AI 能力。 这一整合将先进 AI 引入辅助功能领域，可能提升残障用户的独立性，并为代理式 AI 在消费产品中的应用树立先例。 这些功能利用设备和服务器端 AI 处理，与其他 Apple Intelligence 功能类似。代理式 AI 使系统能够根据上下文主动协助用户。

hackernews · interpol_p · May 19, 12:04 · [社区讨论](https://news.ycombinator.com/item?id=48192224)

**背景**: Apple Intelligence 是苹果于 2024 年发布的生成式 AI 系统，适用于搭载 A17 Pro 或 M1 及以上芯片的设备。代理式 AI 指能够自主行动以达成目标的 AI 系统，通常通过使用工具并在人类设定的约束内做出决策。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Apple_Intelligence">Apple Intelligence</a></li>
<li><a href="https://en.wikipedia.org/wiki/Agentic_AI">Agentic AI</a></li>

</ul>
</details>

**社区讨论**: 评论者赞扬了 LLM 在辅助功能中的实际应用，但批评苹果的语音转文字转录落后于竞争对手。一些人指出高速语音旁白演示实际上对盲人用户不可访问。

**标签**: `#accessibility`, `#Apple`, `#Apple Intelligence`, `#AI`, `#agentic AI`

---

<a id="item-8"></a>
## [Gemini 3.5 Flash 发布，价格更高，集成广泛](https://simonwillison.net/2026/May/19/gemini-35-flash/#atom-everything) ⭐️ 8.0/10

Google 在 Google I/O 大会上发布了 Gemini 3.5 Flash 模型，跳过预览阶段直接正式发布，并将其集成到 Gemini 应用、Google 搜索、Google Antigravity 和 Gemini API 等关键产品中。 此次发布标志着 Google 旗舰模型系列的重大更新，并立即广泛部署，但价格大幅上涨——是前代产品的 3 倍——表明 AI 实验室正在试探客户的价格接受度。 模型 ID 为 gemini-3.5-flash，知识截止日期为 2025 年 1 月，支持 1,048,576 个输入 token 和 65,536 个输出 token，但不支持计算机使用功能。定价为每百万输入 token 1.50 美元，每百万输出 token 9 美元，同时推出了新的 Interactions API（测试版），提供服务器端历史记录管理。

rss · Simon Willison · May 19, 22:40

**背景**: Gemini Flash 系列是 Google 面向高容量、低延迟任务设计的成本高效模型产品线。Google I/O 是公司年度开发者大会，期间发布重大产品。近期趋势显示，OpenAI 和 Anthropic 等其他 AI 实验室也在提高新模型版本的价格，表明行业正转向盈利化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Antigravity">Google Antigravity</a></li>
<li><a href="https://sourceforge.net/software/product/Gemini-Enterprise-Agent-Platform/">Gemini Enterprise Agent Platform Reviews in 2026</a></li>

</ul>
</details>

**标签**: `#Gemini`, `#Google I/O`, `#AI model`, `#machine learning`, `#release`

---

<a id="item-9"></a>
## [提议重构 Linux this_cpu 操作以提升性能](https://lwn.net/Articles/1073395/) ⭐️ 8.0/10

在 2026 年 LSFMM+BPF 峰会上，Yang Shi 提议使用每 CPU 页表重新实现 Linux 的 this_cpu 操作，让每个变量在每个 CPU 上拥有相同的地址，从而消除在 Arm 等架构上禁用抢占的需要。 这一改动能显著提升非 x86 架构的性能，通过减少多指令序列和禁用抢占的开销，可能惠及使用 Arm 及其他 CPU 的各类服务器和移动设备。 该提议需要对每 CPU 变量进行双重映射（一个全局映射用于初始化，一个每 CPU 映射用于访问），并面临 Linus Torvalds 因 TLB 管理难题而长期存在的反对意见。在 160 核 Arm 系统上的基准测试显示，内核构建的系统时间减少了 13-18%。

rss · LWN.net · May 19, 14:30

**背景**: 内核的 this_cpu 操作用于快速访问每 CPU 变量，这些变量是按 CPU 编号索引的数组，以避免加锁。在 x86 上，段寄存器实现了单指令原子访问；而在 Arm 等架构上，多指令序列需要禁用抢占，导致性能损失。该提议旨在通过每 CPU 页表使每 CPU 变量拥有统一地址，从而消除这一惩罚。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/v7.1-rc4/core-api/this_cpu_ops.html">this_cpu operations — The Linux Kernel documentation</a></li>
<li><a href="https://0xax.gitbooks.io/linux-insides/content/Concepts/linux-cpu-1.html">Per-CPU variables · Linux Inside</a></li>

</ul>
</details>

**标签**: `#kernel`, `#performance`, `#per-CPU`, `#LSFMM`, `#Linux`

---

<a id="item-10"></a>
## [CXL 使内存管理问题恶化及未来发展方向](https://lwn.net/Articles/1072858/) ⭐️ 8.0/10

Dan Williams 在 2026 年 Linux 存储、文件系统、内存管理和 BPF 峰会上介绍了 Compute Express Link (CXL)技术如何加剧 Linux 中的内存管理问题，并讨论了未来的发展。 随着 CXL 在数据中心越来越普及，内核必须解决热插拔内存、固件干扰和错误处理等挑战，以确保下一代系统的可靠和高效内存管理。 CXL 内存通过 PCIe 访问，延迟高于远程 NUMA 节点，其热插拔特性意味着部分 RAM 可能消失。内核正在采用“代码优先”策略记录硬件偏差，错误处理可能涉及内核崩溃。

rss · LWN.net · May 19, 14:15

**背景**: Compute Express Link (CXL)是一种开放标准互连，用于高速 CPU 到设备和 CPU 到内存的连接，面向高性能数据中心。它通过 PCIe 提供共享内存节点，但延迟高于本地内存。非一致性内存访问（NUMA）是一种内存设计，其中访问时间取决于内存相对于处理器的位置；远程 NUMA 节点比本地节点慢。CXL 内存的延迟通常比远程 NUMA 节点更差，对现有内存管理构成挑战。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Compute_Express_Link">Compute Express Link - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Non-uniform_memory_access">Non-uniform memory access - Wikipedia</a></li>

</ul>
</details>

**标签**: `#CXL`, `#memory management`, `#Linux kernel`, `#data center`, `#hardware architecture`

---

<a id="item-11"></a>
## [砺算 7G100 显卡 5 月 20 日预售](https://videocardz.com/newz/lisuan-confirms-7g100-preorder-launch-on-may-20-chinas-dx12-gaming-gpu-with-support-for-100-games) ⭐️ 8.0/10

砺算科技确认其 LX 7G100 游戏显卡将于 5 月 20 日晚 8 点在京东开启预售。该卡配备 12GB GDDR6 显存，支持 DirectX 12 和 Vulkan 1.3，官方声称性能达到 Nvidia RTX 4060 级别。 这对于国产 GPU 在消费级游戏市场是一个重要里程碑，因为这是少数几款完整支持 DX12 的国产显卡。如果实际性能与宣称相符，将有助于推动国产 GPU 生态发展，减少对外国硬件的依赖。 该卡已通过 WHQL 认证，并有超过 100 款游戏（包括《黑神话：悟空》和《赛博朋克 2077》）完成了兼容性测试。不过，声称的 RTX 4060 级别性能可能来自合成测试，实际游戏表现取决于驱动优化和游戏兼容性。

telegram · zaihuapd · May 19, 08:57

**背景**: 中国 GPU 厂商在消费级游戏领域传统上较为落后，此前推出的产品大多不支持 DirectX 12 等现代图形 API。砺算 7G100 尝试改变这一局面，通过支持 DX12 和 Vulkan 1.3，使其兼容众多主流 PC 游戏。WHQL 认证表明该卡已通过微软的 Windows 硬件质量实验室测试，确保驱动程序稳定性。

**标签**: `#国产GPU`, `#DX12`, `#游戏显卡`, `#硬件`, `#消费电子`

---