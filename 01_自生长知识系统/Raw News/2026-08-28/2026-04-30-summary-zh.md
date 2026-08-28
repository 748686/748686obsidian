---
layout: default
title: "Horizon Summary: 2026-04-30 (ZH)"
date: 2026-04-30
lang: zh
---

> From 51 items, 26 important content pieces were selected

---

1. [Linux 内核严重零日漏洞 CVE-2026-31431 未修复](#item-1) ⭐️ 9.0/10
2. [Mistral 发布稠密 128B 参数模型，支持 256k 上下文](#item-2) ⭐️ 9.0/10
3. [美国下令停止向华虹供应芯片设备](#item-3) ⭐️ 9.0/10
4. [Zed 1.0 发布：快速、现代的代码编辑器](#item-4) ⭐️ 8.0/10
5. [Claude Code 漏洞导致 HERMES.md 触发额外计费](#item-5) ⭐️ 8.0/10
6. [爱思唯尔因引文卡特尔解雇第三名编辑](#item-6) ⭐️ 8.0/10
7. [京都樱花盛开时间创 1200 年来最早纪录](#item-7) ⭐️ 8.0/10
8. [锻造厂联邦提案](#item-8) ⭐️ 8.0/10
9. [LLM 0.32a0 重构为基于消息的架构](#item-9) ⭐️ 8.0/10
10. [Python 打包委员会通过 PEP 772 获批](#item-10) ⭐️ 8.0/10
11. [SUSE 安全审查发现 Plasma 登录管理器漏洞](#item-11) ⭐️ 8.0/10
12. [千万篇论文的交互式语义地图](#item-12) ⭐️ 8.0/10
13. [LLM 为何不在向量空间中推理：Reddit 热议](#item-13) ⭐️ 8.0/10
14. [Nous Research 关于 Hermes Agent 和本地大模型的 AMA](#item-14) ⭐️ 8.0/10
15. [Qwen 发布 FlashQLA，线性注意力加速 2-3 倍](#item-15) ⭐️ 8.0/10
16. [NVIDIA 发布 Nemotron 3 Super：1200 亿参数 MoE 模型，专为多智能体 AI 设计](#item-16) ⭐️ 8.0/10
17. [美国将 Anthropic 列入黑名单，国防承包商停用 Claude](#item-17) ⭐️ 8.0/10
18. [SpaceX 将马斯克薪酬与火星殖民挂钩](#item-18) ⭐️ 8.0/10
19. [最高法：订婚不等于性同意](#item-19) ⭐️ 8.0/10
20. [百度萝卜快跑事故后中国暂停新 L4 许可](#item-20) ⭐️ 8.0/10
21. [FastCGI 三十岁：仍是反向代理的优选协议](#item-21) ⭐️ 7.0/10
22. [开源 3D 打印听诊器成本仅 2.5-5 美元](#item-22) ⭐️ 7.0/10
23. [荷兰政府软启动开源代码平台](#item-23) ⭐️ 7.0/10
24. [在线年龄验证：隐私战场](#item-24) ⭐️ 7.0/10
25. [马里兰州禁止杂货店监控定价](#item-25) ⭐️ 7.0/10
26. [中国网暴信息治理规定定稿，8 月 1 日施行](#item-26) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Linux 内核严重零日漏洞 CVE-2026-31431 未修复](https://copy.fail/) ⭐️ 9.0/10

安全公司 Xint 披露了 Linux 内核 AF_ALG 套接字家族中的一个严重零日漏洞（CVE-2026-31431），允许非特权用户将权限提升至 root。目前，许多主要发行版尚未提供补丁。 该漏洞风险极高，可实现从用户空间到 root 的本地权限提升，影响大量 Linux 系统。补丁缺失以及部分厂商给出的低严重性评级引发了安全社区的担忧。 该漏洞位于 AF_ALG 套接字家族中，该家族提供了基于套接字的内核加密 API 接口。建议的缓解措施是通过 modprobe 配置禁用内核模块 `algif_aead`，但在某些系统（如 RHEL 9/10）上该模块是内置的，需要其他替代方案。

hackernews · unsnap_biceps · Apr 29, 18:13

**背景**: AF_ALG 是 Linux 特有的套接字家族，允许用户空间程序访问内核加密操作。它常被 GnuTLS 和 OpenVPN 等应用用于硬件加速加密。该漏洞由安全公司 Xint 发现，并随概念验证利用代码一同披露。

**社区讨论**: 社区对披露过程表示不满，指出 Red Hat 等厂商将该漏洞评为“中等”严重性并推迟修复。用户分享了缓解技术，包括禁用 `algif_aead` 模块或使用 systemd 阻止 AF_ALG 套接字。还有人强调了在受影响系统上以普通用户身份运行自主 AI 代理的风险。

**标签**: `#security`, `#linux kernel`, `#cve`, `#privilege escalation`, `#zero-day`

---

<a id="item-2"></a>
## [Mistral 发布稠密 128B 参数模型，支持 256k 上下文](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) ⭐️ 9.0/10

Mistral 发布了 Mistral Medium 3.5，这是一个稠密 128B 参数、支持 256k 上下文窗口的模型，将指令遵循、推理和编码能力统一到一组权重中。 该模型在 SWE-bench 上与 Sonnet 竞争，并提供可配置的推理努力，使其成为快速聊天和复杂代理任务的通用选择。其稠密架构与混合专家趋势形成对比，可能在某些工作负载上提供更好的性能。 该模型接受多模态输入（文本和图像），并支持函数调用。它取代了 Le Chat 中的 Mistral Medium 3.1 和 Magistral，以及编码代理 Vibe 中的 Devstral 2。

reddit · r/LocalLLaMA · jacek2023 · Apr 29, 15:14

**背景**: 稠密模型对每个 token 激活所有参数，而混合专家（MoE）模型仅激活子集。128B 稠密模型需要大量计算，但可以在任务间提供更一致的性能。可配置的推理努力允许模型根据请求复杂度调整测试时计算量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Reasoning_model">Reasoning model - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区对稠密 128B 架构感到兴奋，用户认为这是一个有趣的细分领域。一些人质疑它与 Qwen 3.5 Large 等 MoE 模型的比较，后者仅激活 17B 参数，速度更快。其他人对其 SWE-bench 性能印象深刻，并渴望在本地进行测试。

**标签**: `#LLM`, `#Mistral`, `#open-source`, `#model-release`, `#benchmark`

---

<a id="item-3"></a>
## [美国下令停止向华虹供应芯片设备](https://www.reuters.com/world/china/us-orders-chip-equipment-companies-halt-some-shipments-hua-hong-chinas-second-2026-04-28/) ⭐️ 9.0/10

美国商务部向 Lam Research、Applied Materials 和 KLA 等公司发函，要求停止向华虹集团旗下两座工厂（包括上海 Fab 6（28/22 纳米）和在建的 8a 厂）运送部分工具和材料，以限制其先进芯片发展。 此举直接针对中国第二大芯片代工厂及其向 7 纳米制造的进展，可能导致设备供应商损失数十亿美元销售额，并加剧中美技术紧张局势。 限制措施通过“被告知”信函实施，绕过了冗长的规则制定流程，涉及华虹的 Fab 6（28/22 纳米）和规划的 8a 厂。华虹此前已研发出 7 纳米工艺，并计划 2026 年底前在华力微电子实现初始产能。

telegram · zaihuapd · Apr 29, 05:39

**背景**: 美国一直在收紧对华半导体设备出口管制，以减缓其先进芯片制造能力的发展。华虹是中国第二大代工厂，一直在开发 7 纳米等先进节点。“被告知”信函是美国工业安全局（BIS）用来快速施加许可要求而无需正式修改规则的工具。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zhuanlan.zhihu.com/p/678352124">解读美国出口管制 - 知乎</a></li>
<li><a href="https://www.fsemi.tech/cms/xinwenkuaixun/5316.html">CSPT 2026 |华虹集团 7 纳米制程量产提速 - 未来半导体</a></li>

</ul>
</details>

**标签**: `#semiconductors`, `#US-China trade`, `#export controls`, `#chip manufacturing`, `#geopolitics`

---

<a id="item-4"></a>
## [Zed 1.0 发布：快速、现代的代码编辑器](https://zed.dev/blog/zed-1-0) ⭐️ 8.0/10

Zed 1.0 正式发布，这是一款用 Rust 构建的高性能多人代码编辑器，由前 Atom 团队创建，标志着该编辑器的一个重要里程碑。 Zed 1.0 以其对速度、协作和 AI 集成的关注，为 VS Code 和 Sublime Text 等编辑器提供了有吸引力的替代方案，可能重塑开发者工具的选择偏好。 该编辑器免费使用，但部分 AI 功能需要付费订阅。许可协议中包含一项条款，授予 Zed 广泛处理客户数据的权利，这引发了社区讨论。

hackernews · salkahfi · Apr 29, 14:34

**背景**: Zed 是一款用 Rust 编写的开源代码编辑器，专为高性能和多人协作而设计。它由 Atom 编辑器的联合创始人 Nathan Sobo 创建，并由 Zed Industries 开发。该编辑器支持 Linux、macOS 和 Windows。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Zed_(text_editor)">Zed (text editor) - Wikipedia</a></li>
<li><a href="https://zed.dev/">Zed — Your last next editor</a></li>
<li><a href="https://github.com/zed-industries/zed">GitHub - zed-industries/zed: Code at the speed of thought – Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.</a></li>

</ul>
</details>

**社区讨论**: 社区评论褒贬不一：许多人称赞 Zed 的速度和功能，称其为最好的现代编辑器，而另一些人则批评许可协议中的数据处理条款过于宽泛。一些用户对 AI 集成和订阅模式表示满意。

**标签**: `#code editor`, `#software release`, `#developer tools`, `#licensing`

---

<a id="item-5"></a>
## [Claude Code 漏洞导致 HERMES.md 触发额外计费](https://github.com/anthropics/claude-code/issues/53262) ⭐️ 8.0/10

Anthropic 的 Claude Code 中存在一个漏洞，导致包含 'HERMES.md' 的提交消息将请求路由到额外使用计费，给用户带来意外费用。Anthropic 最初拒绝为技术错误退款，但后来改变了立场，提供全额退款和额外积分。 此漏洞突显了广泛使用的 AI 编码工具中的严重计费问题，削弱了用户信任。公司最初拒绝为技术错误退款引发了社区反弹，但最终的逆转和补偿为处理类似事件树立了先例。 当提交消息包含 'HERMES.md' 时，该漏洞会被触发，导致请求被计为额外使用而非标准订阅。受影响的用户将获得全额退款以及相当于其月度订阅额的额外使用积分。

hackernews · homebrewer · Apr 29, 18:54

**背景**: Claude Code 是 Anthropic 开发的智能编码工具，帮助开发者理解代码库、编辑文件和运行命令。HERMES.md 是 Hermes Agent 项目管理方法使用的上下文文件。该漏洞可能将文件名误解为计费路由指令。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>
<li><a href="https://en.wikipedia.org/wiki/HERMES_method">HERMES method</a></li>

</ul>
</details>

**社区讨论**: 用户对 Anthropic 最初不退还技术错误的政策表示震惊，称其前所未有且令人担忧。在 Anthropic 改变立场后，一些用户分享了自己未解决的计费问题，表明客户支持存在更广泛的挑战。

**标签**: `#Claude Code`, `#billing bug`, `#Anthropic`, `#software bug`, `#customer support`

---

<a id="item-6"></a>
## [爱思唯尔因引文卡特尔解雇第三名编辑](https://www.chrisbrunet.com/p/third-editor-fired-in-elseviers-citation) ⭐️ 8.0/10

爱思唯尔因操纵引文解雇了第三名编辑，继续打击人为抬高引文指标的引文卡特尔行为。 这凸显了学术出版中持续存在的诚信问题以及引文指标的滥用，可能扭曲研究评估和资助决策。 该编辑参与了一个引文卡特尔，相互引用彼此论文，以提高 h 指数和发表数量。爱思唯尔在此丑闻中已解雇三名编辑。

hackernews · RigbyTaro · Apr 29, 15:45

**背景**: 引文卡特尔是一群作者相互串通引用彼此作品，人为增加引文数量。这种做法破坏了 h 指数等学术指标的诚信，而这些指标常用于终身教职和资助决策。爱思唯尔是一家大型学术出版商，因其在出版体系中的角色而受到批评。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Citation_cartel">Citation cartel - Wikipedia</a></li>
<li><a href="https://www.chronicle.com/article/the-dark-world-of-citation-cartels">The Dark World of ‘Citation Cartels’ - The Chronicle of ...</a></li>
<li><a href="https://retractionwatch.com/category/by-journal/elsevier/">elsevier – Retraction Watch</a></li>

</ul>
</details>

**社区讨论**: 评论者批评了 h 指数等虚荣指标，并呼吁改革，有人希望爱思唯尔及类似出版商倒闭。其他人指出该编辑的贪婪可能导致被发现，并好奇被删除的论文是否会被 LLM 遗忘。

**标签**: `#academic publishing`, `#citation cartel`, `#Elsevier`, `#research integrity`, `#vanity metrics`

---

<a id="item-7"></a>
## [京都樱花盛开时间创 1200 年来最早纪录](https://jivx.com/kyoto-bloom) ⭐️ 8.0/10

根据日本僧侣和科学家维护的独特历史数据集，京都的樱花盛开时间比过去 1200 年中的任何时期都要早。 这一趋势为气候变化对物候学的影响提供了明确证据，而长达 1200 年的数据集是世界上连续时间最长的气候记录之一，对气候研究具有不可估量的价值。 该数据集最初由日本僧侣和宫廷官员记录，他们记下了樱花节的具体日期；气候学家青野靖之（Yasuyuki Aono）在 2025 年去世前一直负责更新该数据。

hackernews · momentmaker · Apr 29, 19:32

**背景**: 物候学是研究生物事件（如开花、迁徙）时间与气候关系的学科。樱花对温度特别敏感，因此其盛开日期成为气候变化的一个可靠指标。京都的樱花记录跨越千年以上，为气候趋势提供了罕见的长期视角。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nytimes.com/2026/04/17/climate/japan-cherry-blossom-database-scientist.html">Japan’s Cherry Blossom Database, 1,200 Years Old, Has a New ...</a></li>
<li><a href="https://orennia.com/insights/1200-years-of-cherry-blossoms-reveal-what-climate-models-confirm">1,200 Years of Cherry Blossoms Reveal What Climate Models ...</a></li>
<li><a href="https://www.smithsonianmag.com/smart-news/in-japan-a-new-steward-for-1200-years-of-cherry-blossom-data-has-been-found-sustaining-a-climate-change-research-project-180988607/">In Japan, a New Steward for 1,200 Years of Cherry Blossom ...</a></li>

</ul>
</details>

**社区讨论**: 评论者对长达 1200 年的数据集表示敬畏，并对开花日期的快速变化表示担忧。一些人分享了个人观察到的提前开花现象，另一些人则质疑主流媒体为何没有更多报道此事。总体情绪是警觉和对历史记录的赞赏。

**标签**: `#climate change`, `#phenology`, `#historical data`, `#environmental science`, `#cherry blossoms`

---

<a id="item-8"></a>
## [锻造厂联邦提案](https://blog.tangled.org/federation/) ⭐️ 8.0/10

Tangled 博客上的一篇文章提议创建一个锻造厂联邦，以分散代码托管，减少对 GitHub 等中心化平台的依赖。 该提案可能通过实现不同代码锻造厂之间的互操作性来重塑开源协作，减少供应商锁定并促进竞争。 该联邦将使用 ForgeFed 等现有协议连接锻造厂，使用户能够跨平台处理问题、拉取请求和仓库。

hackernews · icy · Apr 29, 14:00

**背景**: Git 是去中心化的，但 GitHub 等代码托管平台是中心化的，造成了单点故障和控制。锻造厂联邦旨在将去中心化扩展到整个开发工作流程，类似于电子邮件或 Mastodon 的联邦方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.tangled.org/federation/">we need a federation of forges — tangled blog</a></li>
<li><a href="https://forgefed.org/">ForgeFed</a></li>
<li><a href="https://thecodersblog.com/federation-of-code-forges-2026">Federated Code Forges: The Blueprint for Interoperable ...</a></li>

</ul>
</details>

**社区讨论**: 评论褒贬不一：一些人将其与 Mastodon 的挑战（如去联邦化和审核争论）相比较，而另一些人则支持竞争并指出 ForgeFed 等现有项目。少数人建议使用 Fossil 等更丰富的 git 仓库作为替代方案。

**标签**: `#federation`, `#forge`, `#decentralization`, `#open source`, `#github alternative`

---

<a id="item-9"></a>
## [LLM 0.32a0 重构为基于消息的架构](https://simonwillison.net/2026/Apr/29/llm/#atom-everything) ⭐️ 8.0/10

LLM 0.32a0 是 LLM Python 库和 CLI 工具的 alpha 版本，它进行了一次重大的向后兼容重构，从提示-响应模型转向基于消息的架构，并支持带类型的响应片段。 这次重构使 LLM 能够更好地处理现代 LLM 的能力，如多模态输入、结构化输出、工具调用和推理，为开发者构建复杂 AI 应用提供了更高的灵活性。 新架构将输入建模为消息序列（类似聊天 API），输出建模为带类型的片段流，从而支持更丰富的交互。这些更改完全向后兼容，现有代码可以继续使用。

rss · Simon Willison · Apr 29, 19:01

**背景**: LLM 是一个开源 Python 库和 CLI 工具，通过插件为数百个 LLM 提供统一接口。最初设计用于简单的文本输入/文本输出提示，后来逐渐支持附件、模式和工具，但底层架构需要更新以跟上不断发展的模型能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/simonw/llm">GitHub - simonw/llm: Access large language models from the command-line · GitHub</a></li>
<li><a href="https://llm.datasette.io/">LLM: A CLI utility and Python library for interacting with Large Language Models</a></li>

</ul>
</details>

**标签**: `#LLM`, `#Python`, `#open-source`, `#refactor`, `#AI tools`

---

<a id="item-10"></a>
## [Python 打包委员会通过 PEP 772 获批](https://lwn.net/Articles/1068704/) ⭐️ 8.0/10

Python 打包社区现已拥有一个正式的治理委员会，该委员会通过 PEP 772 于 2026 年 4 月 16 日获批，选举预计在 2026 年 PyCon US 之后举行。 这建立了一个民主选举的机构，对打包标准、工具和实现拥有广泛权力，取代了之前的临时授权，让社区在打包决策中拥有更强的话语权。 该委员会将由五名当选成员组成，仿照 Python 指导委员会和类型委员会的模式。指导委员会将明确将其对相关 PEP 的决策权委托给打包委员会。

rss · LWN.net · Apr 29, 16:48

**背景**: Python 打包历来由 Python 打包管理局（PyPA，一个松散的项目组织）和 PSF 工作组管理，但两者都没有社区选举的机构。PEP 772 于 2025 年 2 月首次提出，经历了长时间的讨论，包括关于谁有资格成为投票社区成员的辩论，特别是针对 uv 等非 PyPA 项目。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://discuss.python.org/t/pep-772-packaging-council-governance-process-round-2/93904">PEP 772: Packaging Council governance process (Round 2) -</a></li>
<li><a href="https://discuss.python.org/t/pep-772-packaging-council-governance-process-round-3/100181">PEP 772: Packaging Council governance process (Round 3) -</a></li>
<li><a href="https://discuss.python.org/t/proposal-to-create-a-python-packaging-council/25469">Proposal to create a Python Packaging Council - Packaging -</a></li>

</ul>
</details>

**社区讨论**: 讨论凸显了定义投票社区的挑战，Charlie Marsh 指出 uv 开发者最初因非营利要求而不符合资格。该要求后来被移除，最终 PEP 采用了更具包容性的方式。

**标签**: `#Python`, `#packaging`, `#governance`, `#PEP`

---

<a id="item-11"></a>
## [SUSE 安全审查发现 Plasma 登录管理器漏洞](https://lwn.net/Articles/1070434/) ⭐️ 8.0/10

SUSE 安全团队发布了 Plasma Login Manager 6.6.2 的审查报告，指出其特权 D-Bus 助手 plasmaloginauthhelper 存在纵深防御安全问题，可能导致 plasmalogin 服务用户提升至 root 权限。 此事至关重要，因为 Plasma Login Manager 是处理用户身份验证的关键系统组件，这些漏洞实际上消除了服务用户与 root 之间的安全隔离，影响所有 KDE Plasma 用户。 问题出现在从 SDDM 分支出来的 6.6.2 版本中，该版本新增了特权助手。发布时上游尚未提供修复，但计划在 2026 年 5 月 12 日的下一个 Plasma 版本中修复。

rss · LWN.net · Apr 29, 14:20

**背景**: Plasma Login Manager 是 KDE Plasma 的显示管理器，从 SDDM（Simple Desktop Display Manager）分支而来。D-Bus 是 Linux 上的进程间通信系统；特权 D-Bus 助手以高权限运行以执行身份验证任务。纵深防御问题意味着多层安全防护薄弱，可能导致权限提升。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://security.opensuse.org/2026/04/27/plasma-login-manager.html">plasma-login-manager: Weaknesses in plasmaloginauthhelper ...</a></li>
<li><a href="https://lwn.net/Articles/1070434/">Security review of Plasma Login Manager (SUSE Security Team ...</a></li>
<li><a href="https://seclists.org/oss-sec/2026/q2/228">oss-sec: plasma-login-manager: Weaknesses in ...</a></li>

</ul>
</details>

**标签**: `#security`, `#Linux`, `#Plasma`, `#D-Bus`, `#KDE`

---

<a id="item-12"></a>
## [千万篇论文的交互式语义地图](https://www.reddit.com/gallery/1sz14mi) ⭐️ 8.0/10

一位开发者利用 SPECTER2 嵌入、UMAP 降维和 Voronoi 分区技术，构建了包含 1000 万篇科学论文的交互式语义地图，并在 Global Research Space 上免费开放使用。 该工具使研究人员能够直观地探索科学领域全景、发现相关研究，并分析机构或作者排名，有望加速文献综述和跨学科发现。 该地图使用论文标题和摘要的 SPECTER2 嵌入，通过 UMAP 进行二维投影，并在密度峰值上应用 Voronoi 分区以创建语义邻域。它支持关键词和语义查询，并包含用于排名机构、作者和主题的分析层。

reddit · r/MachineLearning · icannotchangethename · Apr 29, 14:53

**背景**: SPECTER2 是 Allen AI 开发的一系列面向科学任务的文档嵌入模型，能从论文标题和摘要生成特定任务的嵌入。UMAP（统一流形逼近与投影）是一种保留局部和全局结构的降维技术。Voronoi 分区根据到种子点的距离将平面划分为不同区域，从而创建独特的邻域。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/allenai/SPECTER2">GitHub - allenai/SPECTER2</a></li>
<li><a href="https://umap-learn.readthedocs.io/">UMAP : Uniform Manifold Approximation and Projection for Dimension...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Voronoi_diagram">Voronoi diagram - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区反应极为积极，用户称其“非常酷”，并将其与 ArXiv 机器学习景观图相提并论。一位用户询问了 Voronoi 分区过程的更多细节以及为何未使用 HDBSCAN，显示出技术上的好奇心。

**标签**: `#semantic mapping`, `#scientific literature`, `#visualization`, `#NLP`, `#machine learning`

---

<a id="item-13"></a>
## [LLM 为何不在向量空间中推理：Reddit 热议](https://www.reddit.com/r/MachineLearning/comments/1syjlc2/why_isnt_llm_reasoning_done_in_vector_space/) ⭐️ 8.0/10

Reddit 上的一场讨论探讨了为什么大型语言模型（LLM）不在潜在向量空间中进行推理，而是使用自然语言，并引用了循环 LLM 和扩散 LLM 等正在进行的研究。 这个问题触及了 LLM 推理中效率与可解释性之间的根本权衡，对未来模型架构和调试能力具有重要影响。 像 Coconut（连续思维链）和循环 LLM 这样的研究探索了潜在空间推理，但挑战包括失去可调试性以及在抽象向量空间中训练推理轨迹的困难。

reddit · r/MachineLearning · ZeusZCC · Apr 29, 00:46

**背景**: 当前的 LLM 以自然语言文本（思维链）生成推理，这具有可解释性但令牌效率低。模型内部在高维向量上运行，但中间推理并不直接在该空间中暴露。潜在空间推理旨在将推理保持在向量形式，可能更快、更紧凑，但以透明度为代价。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/dl1683/Latent-Space-Reasoning">GitHub - dl1683/ Latent - Space - Reasoning : Teaching LLMs to reason ...</a></li>
<li><a href="https://arxiv.org/html/2505.16782v1">Reasoning Beyond Language: A Comprehensive Survey on Latent ...</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍认为 LLM 内部已经在潜在空间中进行推理，语言输出只是一个痕迹。主要担忧是隐藏向量中的推理会降低可调试性和可控性，这对确定性任务来说是个问题。一些人指出扩散 LLM 是潜在推理的一个有前景的方向。

**标签**: `#LLM reasoning`, `#latent space`, `#chain-of-thought`, `#interpretability`, `#machine learning`

---

<a id="item-14"></a>
## [Nous Research 关于 Hermes Agent 和本地大模型的 AMA](https://www.reddit.com/r/LocalLLaMA/comments/1sz2y76/ama_with_nous_research_ask_us_anything/) ⭐️ 8.0/10

Nous Research 在 Reddit 上举办了一场 AMA，讨论他们的 Hermes Agent 框架——一个开源、能随时间学习和改进的自主智能体，以及他们在本地模型和自改进智能体系统方面的工作。 这场 AMA 直接揭示了最引人注目的开源智能体框架之一的开发内幕，该框架通过闭环学习和技能进化实现差异化，并回应了社区对能本地运行、实用的自主 AI 智能体日益增长的兴趣。 Hermes Agent 支持多种通信平台（Telegram、Discord、Slack 等），可在多种环境（本地、Docker、SSH）中运行，并具备带定期提醒的智能体管理记忆功能。团队成员包括联合创始人 emozilla 和 teknium、首席科学家 bloc97 以及核心开发者。

reddit · r/LocalLLaMA · emozilla · Apr 29, 15:57

**背景**: Nous Research 以 YaRN 方法闻名，该方法能高效扩展大语言模型的上下文窗口，并创建了 Hermes 系列模型。Hermes Agent 是他们最新的开源项目，设计为一个自主智能体，能从交互中学习并随时间改进技能，不同于传统的聊天机器人或编程助手。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/NousResearch/hermes-agent">GitHub - NousResearch/hermes-agent: The agent that grows with you · GitHub</a></li>
<li><a href="https://hermes-agent.nousresearch.com/">Hermes Agent — The Agent That Grows With You | Nous Research</a></li>
<li><a href="https://x.com/NousResearch/status/1698564523177779588?lang=ar-x-fm">Nous Research على X: "The YaRN method paper is now available on arxiv. Many congrats and thanks to our very own Bowen Peng (Bloc97) and @theemozilla, as well as @Void13950782 of @AiEleuther, and our dear friend @EnricoShippole. https://t.co/kTiUbKV0iW" / X</a></li>

</ul>
</details>

**社区讨论**: 社区成员对 Hermes Agent 的闭环学习和技能进化表示热情，但也提出了关于如何防止长期行为漂移以及与其他智能体框架差异化的问题。一些用户询问了实际用例以及与 Hermes 配合使用的最佳本地模型。

**标签**: `#AI Agents`, `#Local LLMs`, `#Hermes Agent`, `#Nous Research`, `#Open Source`

---

<a id="item-15"></a>
## [Qwen 发布 FlashQLA，线性注意力加速 2-3 倍](https://i.redd.it/7l3v03pbg4yg1.jpeg) ⭐️ 8.0/10

Qwen 发布了 FlashQLA，这是一个基于 TileLang 构建的高性能线性注意力内核库，在 SM90+ GPU 上实现了 2-3 倍的前向加速和 2 倍的反向加速。 FlashQLA 显著加速了个人设备上代理型 AI 的线性注意力，为长上下文任务和小模型提供了更快的推理和微调能力。 FlashQLA 采用门控驱动的自动卡内计算预加载和 16 阶段 warp 专用流水线来实现反向传播，但需要 SM90+ GPU（如 H100、Blackwell）和 CUDA 12.8+。

reddit · r/LocalLLaMA · ResearchCrafty1804 · Apr 29, 12:18

**背景**: 线性注意力内核优化了 Transformer 模型中的注意力机制，将计算复杂度从二次方降低到线性。FlashQLA 基于 TileLang（一种用于高效 AI 内核开发的平铺编程模型）构建，并针对 Qwen 模型中使用的门控 Delta 网络（GDN）架构。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/QwenLM/FlashQLA">QwenLM/ FlashQLA : high-performance linear attention kernel library...</a></li>
<li><a href="https://tradepoint.io/qwen-team-releases-flashqla-a-high-performance-linear-attention-kernel-library-that-achieves-up-to-3x-speedup-on-nvidia-hopper-gpus/">Qwen Team Releases FlashQLA : a High-Performance Linear ...</a></li>
<li><a href="https://arxiv.org/abs/2504.17577">[2504.17577] TileLang: A Composable Tiled Programming Model for</a></li>

</ul>
</details>

**社区讨论**: 社区对性能提升感到兴奋，但注意到需要 SM90+ GPU 的硬件要求，这限制了可访问性。一些用户质疑为何不支持 SM89（如 RTX 4090），并询问对现有 Qwen 模型的实际加速效果。

**标签**: `#FlashQLA`, `#linear attention`, `#AI kernels`, `#edge AI`, `#TileLang`

---

<a id="item-16"></a>
## [NVIDIA 发布 Nemotron 3 Super：1200 亿参数 MoE 模型，专为多智能体 AI 设计](https://t.me/zaihuapd/41118) ⭐️ 8.0/10

NVIDIA 发布了 Nemotron 3 Super，这是一款开源大语言模型，拥有 1200 亿总参数，每次推理仅激活 120 亿参数，采用混合专家（MoE）架构，融合了 Mamba 层与 Transformer 层。该模型支持 100 万 token 的上下文窗口，相比上一代 Nemotron Super 模型，吞吐量提升最高 5 倍，准确率提升最高 2 倍。 此次发布意义重大，因为它提供了一个专门为多智能体 AI 系统优化的强大开源权重模型，而多智能体 AI 是 AI 研究和工业中快速发展的领域。MoE、Mamba 和 Transformer 层的结合，加上 100 万 token 的上下文窗口，为开源大语言模型的效率和性能树立了新标杆。 该模型采用混合架构，将 Mamba 状态空间模型层与传统 Transformer 注意力层交错排列，实现了高效的长上下文处理。模型以宽松许可协议发布，权重开放，允许广泛使用和定制。

telegram · zaihuapd · Apr 29, 00:00

**背景**: 混合专家（MoE）是一种神经网络架构，每次输入只激活部分参数（专家），从而在不牺牲容量的情况下提高效率。Mamba 是一种状态空间模型，旨在比 Transformer 更高效地处理长序列，而 Transformer 则擅长通过注意力机制捕捉复杂依赖关系。多智能体 AI 系统由多个智能体协作解决问题，通常利用大语言模型进行协调。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.kdnuggets.com/why-the-newest-llms-use-a-moe-mixture-of-experts-architecture">Why the Newest LLMs use a MoE (Mixture of Experts) Architecture</a></li>
<li><a href="https://www.unite.ai/mamba-redefining-sequence-modeling-and-outforming-transformers-architecture/">Mamba: Redefining Sequence Modeling and Outforming Transformers</a></li>
<li><a href="https://en.wikipedia.org/wiki/Multi-agent_system">Multi-agent system</a></li>

</ul>
</details>

**标签**: `#NVIDIA`, `#LLM`, `#MoE`, `#open-source`, `#multi-agent`

---

<a id="item-17"></a>
## [美国将 Anthropic 列入黑名单，国防承包商停用 Claude](https://t.me/zaihuapd/41124) ⭐️ 8.0/10

特朗普政府将人工智能公司 Anthropic 指定为供应链风险，导致多家国防承包商要求员工停止使用其 Claude AI 模型，并切换至其他工具。 这一针对美国本土 AI 公司的前所未有的举措可能重塑硅谷与联邦政府的关系，可能抑制创新并改变国防领域对 AI 的采用。 Anthropic 是首家被指定为供应链风险的美国公司，而该标签传统上仅适用于外国对手；这一指定可能使 Anthropic 每年失去数十亿美元的国防部合同。

telegram · zaihuapd · Apr 29, 04:38

**背景**: 供应链风险指定通常用于将来自中国或俄罗斯等外国对手的供应商排除在美国国防合同之外。针对美国 AI 安全公司 Anthropic 的举动被视为重大政策转变，可能对 AI 行业和国家安全产生深远影响。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://news.northeastern.edu/2026/03/05/anthropic-supply-chain-risk/">What Does It Mean That Anthropic is a ‘ Supply Chain ’ Risk ?</a></li>
<li><a href="https://www.bbc.com/news/articles/cn5g3z3xe65o">Anthropic officially designated a supply chain risk by Pentagon</a></li>
<li><a href="https://vaidra.in/prepare/current-affairs/article/us-defence-secretary-hegseth-labels-anthropic-ai-as-supplychain-risk-tech-industry-pushes-back">US Defence Secretary Hegseth Labels Anthropic AI as Supply ‑ Chain ...</a></li>

</ul>
</details>

**标签**: `#AI policy`, `#national security`, `#Anthropic`, `#defense technology`, `#supply chain`

---

<a id="item-18"></a>
## [SpaceX 将马斯克薪酬与火星殖民挂钩](https://www.reuters.com/sustainability/boards-policy-regulation/spacex-ties-musk-compensation-mars-colonization-goal-2026-04-28/) ⭐️ 8.0/10

SpaceX 董事会批准了埃隆·马斯克的薪酬方案，将其奖励与实现火星殖民和运营太空数据中心挂钩，并计划于 2026 年 6 月左右进行 IPO。 该计划将马斯克的激励与 SpaceX 最雄心勃勃的长期目标对齐，可能加速太空探索和数据中心技术的进展，并为航天行业的高管薪酬树立先例。 如果 SpaceX 估值达到 7.5 万亿美元并建立至少 100 万人的永久火星殖民地，马斯克将获得 2 亿股超级投票权股票；若运营提供至少 100 太瓦计算能力的太空数据中心，可额外获得 6040 万股。未达估值目标则无奖励，且无时间限制。

telegram · zaihuapd · Apr 29, 06:51

**背景**: 超级投票权股票赋予创始人对公司决策不成比例的控制权，常被 Facebook 和 Google 等科技公司用于保持创始人影响力。太空数据中心是一种将计算设施置于轨道的概念，以利用太阳能并降低延迟，但 100 太瓦的目标比当前全球计算能力高出数个数量级。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://finance.sina.com.cn/wm/2026-04-29/doc-inhwefuz0960286.shtml">SpaceX披露马斯克天价薪酬方案，KPI...</a></li>
<li><a href="https://m.huxiu.com/article/428189.html">创始人怎样可以拥有更多投票权？-虎嗅网</a></li>

</ul>
</details>

**标签**: `#SpaceX`, `#Mars colonization`, `#executive compensation`, `#space data center`, `#IPO`

---

<a id="item-19"></a>
## [最高法：订婚不等于性同意](https://t.me/zaihuapd/41128) ⭐️ 8.0/10

最高人民法院将山西“订婚强奸案”列为参考案例，明确订婚不代表对性行为的默示同意，违背妇女意志发生性关系构成强奸罪。 这一法律先例明确了性自主权不受婚姻状态影响，纠正了公众的法律误解，强化了对中国女性权益的法律保护。 法院强调订婚不存在“默示性权利”，以暴力、胁迫等手段违背妇女意志发生性关系构成强奸罪。同时，泄露依法不公开审理案件信息的行为也将被追责。

telegram · zaihuapd · Apr 29, 07:43

**背景**: 在中国，传统观念有时会将订婚或婚姻等同于自动的性同意。此案源于山西大同一起备受关注的事件，一名女子在订婚后指控其未婚夫强奸。最高法将此案列为参考案例，旨在教育公众并指导下级法院。

**标签**: `#legal precedent`, `#sexual consent`, `#women's rights`, `#China`

---

<a id="item-20"></a>
## [百度萝卜快跑事故后中国暂停新 L4 许可](https://www.bloomberg.com/news/articles/2026-04-29/china-suspends-new-autonomous-driving-permits-after-baidu-outage) ⭐️ 8.0/10

2026 年 3 月底，百度萝卜快跑超百辆无人出租车在武汉集体故障，导致乘客滞留和交通中断，随后中国暂停发放新的 L4 级自动驾驶许可。工信部已要求地方自查并强化安全监测，百度在武汉的运营被暂停。 此次监管行动是第二次因百度事故暂停牌照发放，表明中国对自动驾驶安全的审查更加严格。这可能会减缓全国范围内 Robotaxi 服务的推广，并影响小马智行、文远知行等其他公司，尽管它们声称运营未受影响。 事故涉及百度萝卜快跑超百辆无人出租车在武汉同时故障，导致乘客滞留和交通拥堵。百度在武汉的运营被暂停，而小马智行和文远知行表示其在其他城市的服务正常进行。

telegram · zaihuapd · Apr 29, 08:53

**背景**: L4 级自动驾驶指车辆在特定条件下无需人类干预即可完成所有驾驶任务。百度萝卜快跑是中国最大的 Robotaxi 服务平台，在武汉拥有超 500 辆车，服务近 770 万市民。中国此前于 2025 年 7 月在五个城市开放 L4 商业化运营，取消了安全员强制随车的要求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zh.wikipedia.org/zh-hans/萝卜快跑">萝卜快跑 - 维基百科，自由的百科全书</a></li>
<li><a href="https://baike.baidu.com/item/L4级自动驾驶/64659260">L4级自动驾驶 - 百度百科</a></li>

</ul>
</details>

**标签**: `#autonomous driving`, `#regulation`, `#Baidu`, `#China`, `#L4 permits`

---

<a id="item-21"></a>
## [FastCGI 三十岁：仍是反向代理的优选协议](https://www.agwa.name/blog/post/fastcgi_is_the_better_protocol_for_reverse_proxies) ⭐️ 7.0/10

一篇技术文章指出，已满 30 岁的 FastCGI 协议在反向代理与后端服务器通信方面，技术上仍优于 HTTP，因其高效和简洁。 这挑战了广泛使用 HTTP 进行代理与后端通信的现状，可能促使后端工程师在性能关键系统中重新考虑协议选择。 FastCGI 采用二进制协议并支持多路复用连接，避免了 HTTP 的头部解析和连接管理等开销。但它缺乏原生 WebSocket 支持，且对复杂拓扑的灵活性较差。

hackernews · agwa · Apr 29, 16:16

**背景**: FastCGI 是 1990 年代中期设计的协议，旨在通过允许持久化进程和多路复用请求来改进 CGI。Nginx 和 Apache 等反向代理使用它与应用服务器通信。HTTP 虽然通用，但因其基于文本的特性和连接开销，在内部代理到后端通信时引入了低效。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.agwa.name/blog/post/fastcgi_is_the_better_protocol_for_reverse_proxies">FastCGI: 30 Years Old and Still the Better Protocol for ...</a></li>
<li><a href="https://thecodersblog.com/fastcgi-the-underestimated-protocol-for-modern-reverse-proxies-2026">FastCGI's Enduring Edge: Why the 30-Year-Old Protocol Still ...</a></li>
<li><a href="https://www.moltbook.com/post/c9c7c249-89f9-410c-a04e-27b9c06122d1">FastCGI at 30: why the 1996 binary protocol beats HTTP for ...</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍赞同文章观点，有人提到 Web Application Socket (WAS) 等替代协议可进一步改进。其他人回顾了 FastCGI、SCGI 和 HTTP 之间的历史争论，指出 HTTP 因简单和灵活而胜出。

**标签**: `#FastCGI`, `#reverse proxy`, `#protocols`, `#web servers`, `#HTTP`

---

<a id="item-22"></a>
## [开源 3D 打印听诊器成本仅 2.5-5 美元](https://github.com/GliaX/Stethoscope) ⭐️ 7.0/10

GliaX 听诊器是一款开源、3D 打印的医疗设备，生产成本仅为 2.5 至 5 美元，旨在让资源匮乏地区也能进行听诊检查。 与传统听诊器（30-100 美元以上）相比，成本大幅降低，有望使医疗诊断民主化，特别是在发展中国家和冲突地区，通过早期发现心肺疾病来挽救生命。 该设计在《PLOS One》研究中得到验证，声学性能可与 Littmann Cardiology III 媲美，但社区评论质疑其频率响应曲线，并指出市面上已有 7 美元的廉价金属听诊器。

hackernews · 0x54MUR41 · Apr 29, 14:47

**背景**: 听诊器是一种用于听取体内声音（听诊）的医疗仪器，主要用于心肺检查。传统声学听诊器依靠胸件、导管和耳件传输声音。GliaX 项目由 Tarek Loubani 博士领导，旨在利用 3D 打印和现成组件提供低成本、易复制的替代方案。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0193087">Validation of an effective, low cost, Free/open access 3D-printed stethoscope | PLOS One</a></li>
<li><a href="https://en.wikipedia.org/wiki/Stethoscope">Stethoscope - Wikipedia</a></li>
<li><a href="https://hackaday.com/tag/stethoscope/">stethoscope – Hackaday</a></li>

</ul>
</details>

**社区讨论**: 社区评论对其声学性能的说法表示怀疑，有用户对比频率响应图，质疑 3D 打印设备如何能与金标准听诊器匹敌。另一用户指出，7 美元即可买到廉价金属听诊器，削弱了成本优势的新颖性。不过，也有人认为该项目鼓舞人心，并呼吁开发开源超声设备。

**标签**: `#open-source`, `#medical devices`, `#3D printing`, `#healthcare`, `#DIY`

---

<a id="item-23"></a>
## [荷兰政府软启动开源代码平台](https://www.nldigitalgovernment.nl/news/soft-launch-for-government-open-source-code-platform/) ⭐️ 7.0/10

荷兰政府软启动了 code.overheid.nl，这是一个基于 Forgejo 的自托管开源代码平台，用于托管公共部门软件，其中包括一个名为 RegelRecht 的机器可读法律执行工具。 该举措通过减少对美国服务（如 GitHub 和 GitLab）的依赖来加强数字主权，并促进公共部门软件开发的透明度和协作。 该平台基于 Forgejo（GitLab 的一个免费分支）构建，并包含 RegelRecht，该工具将法律文本编码为结构化 YAML，并作为确定性决策逻辑运行，提供完整的解释轨迹。

hackernews · e12e · Apr 29, 09:14

**背景**: 数字主权问题促使政府寻求美国拥有的代码托管平台的替代方案。Forgejo 是一个社区驱动的自托管 Git 服务，允许组织完全控制其代码。该荷兰平台旨在成为公共部门开源开发的主权替代方案。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nldigitalgovernment.nl/news/soft-launch-for-government-open-source-code-platform/">Soft launch of open-source code platform for government</a></li>
<li><a href="https://www.opensourceforu.com/2026/04/dutch-government-backs-forgejo-for-sovereign-open-source-github-alternative/">Dutch Government Backs Forgejo For Sovereign Open Source ...</a></li>
<li><a href="https://abit.ee/en/artificial-intelligence/netherlands-open-source-forgejo-github-gitlab-digital-sovereignty-news-en">Netherlands Launches Forgejo-Based GitHub Alternative for ...</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了自豪和欣慰，认为荷兰政府终于拥抱开源，但也有人指出采用速度缓慢。此外，人们对 RegelRecht 工具感兴趣，并与德国类似举措（opencode.de）进行了比较。

**标签**: `#open source`, `#government`, `#Netherlands`, `#digital sovereignty`, `#public sector`

---

<a id="item-24"></a>
## [在线年龄验证：隐私战场](https://x.com/GlennMeder/status/2049088498163216560) ⭐️ 7.0/10

Glenn Meder 在 X（原 Twitter）上发起的一场讨论引发了关于强制性在线年龄验证的辩论，重点涉及隐私风险、身份欺诈以及家长与政府角色的冲突。 这场辩论意义重大，因为它触及互联网治理、公民自由和儿童安全等根本问题，可能影响未来的立法和技术设计。 讨论中提出了诸如服务器运营商使用 RTA 标头和匿名凭证系统等方案，但批评者认为大多数年龄验证方案会损害隐私并导致大规模身份欺诈。

hackernews · Cider9986 · Apr 29, 15:49

**背景**: 在线年龄验证是一种限制访问不适宜年龄内容的方法，通常要求用户提交个人身份信息。支持者认为这能保护未成年人，而反对者警告这会侵犯隐私并导致监控。随着世界各国政府考虑强制实施此类系统，辩论日益激烈。

**社区讨论**: 评论者强烈反对强制性年龄验证，指出隐私问题和身份欺诈的不可避免性。一些人提出了技术替代方案，如 RTA 标头或匿名凭证，但指出年龄验证的支持者并不关心保护隐私。

**标签**: `#privacy`, `#age verification`, `#internet governance`, `#parental controls`, `#identity fraud`

---

<a id="item-25"></a>
## [马里兰州禁止杂货店监控定价](https://www.theguardian.com/technology/2026/apr/29/maryland-grocery-stores-ban-surveillance-pricing) ⭐️ 7.0/10

马里兰州成为美国首个禁止杂货店监控定价的州，该法律禁止使用个人数据设定个性化价格。该法案于 2026 年 4 月签署。 这项立法为解决算法个性化定价问题开创了先例，随着零售商越来越多地使用 AI 和消费者数据来最大化利润，这一问题日益受到关注。它可能促使其他州采取类似的消费者保护措施。 该法律专门针对杂货店，禁止基于监控数据设定更高价格，但未涉及个性化折扣。批评者认为，商店可以提高基础价格，然后提供折扣，从而有效达到相同结果。

hackernews · 01-_- · Apr 29, 16:50

**背景**: 监控定价，也称为算法个性化定价，利用消费者的个人数据（如位置、浏览历史和购买习惯）为不同个体设定不同价格。这种做法不同于传统的动态定价，后者基于市场条件而非个人数据调整价格。该法律旨在防止基本商品中的价格歧视。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ici.radio-canada.ca/rci/en/news/2246515/are-you-paying-more-than-your-neighbour-it-could-be-surveillance-pricing">Are you paying more than your neighbour? It could be ’ surveillance ...</a></li>
<li><a href="https://www.aljazeera.com/features/2025/10/15/surveillance-pricing-why-you-might-be-paying-more-than-your-neighbour">‘ Surveillance pricing ’: Why you might be paying more... | Al Jazeera</a></li>
<li><a href="https://www.jdsupra.com/legalnews/surveillance-pricing-ai-pricing-tools-8489430/">Surveillance Pricing , AI Pricing Tools and the Push for... - JDSupra</a></li>

</ul>
</details>

**社区讨论**: 评论者对法律的有效性表示怀疑，指出商店可以通过提高基础价格并提供折扣来规避法律。一些人强调了对抗性定价的广泛趋势，以及消费者需要代理来寻找最佳交易。

**标签**: `#privacy`, `#legislation`, `#dynamic pricing`, `#surveillance`, `#consumer protection`

---

<a id="item-26"></a>
## [中国网暴信息治理规定定稿，8 月 1 日施行](https://t.me/zaihuapd/41135) ⭐️ 7.0/10

中国《网络暴力信息治理规定》定稿公布，自 2024 年 8 月 1 日起施行，新增公安、文旅、广电部门作为共同主管部门。 该规定为中国打击网络暴力提供了专门的法律框架，明确了定义和平台义务，将影响社交媒体平台和用户处理网络骚扰的方式。 与征求意见稿相比，定稿重新定义网暴为侮辱谩骂、造谣诽谤、煽动仇恨、威逼胁迫、侵犯隐私及贬低歧视等，删除了“道德绑架、恶意揣测”。同时放宽了对匿名账号的禁令，并将平台必须技术阻断网暴私信改为鼓励提供智能关键词屏蔽功能。

telegram · zaihuapd · Apr 29, 23:30

**背景**: 网络暴力，如在线骚扰和人肉搜索，在中国日益受到关注，促使政府起草专门法规。国家互联网信息办公室于 2023 年发布了征求意见稿，定稿吸收了反馈意见并增加了多个执法部门。

<details><summary>参考链接</summary>
<ul>
<li><a href="http://paper.people.com.cn/rmrb/images/2024-08/05/14/rmrb2024080514.pdf">ZZRMRB14B20240805C</a></li>
<li><a href="https://legal.gmw.cn/2024-06/17/content_37383564.htm">事后惩治→事前预警 治理网暴这些机制将派上用场 _光明网</a></li>
<li><a href="https://www.cac.gov.cn/2022-11/04/c_1669204414682178.htm">中央网信办印发《关于切实加强网络暴力治理的通知》_中央网络安全和信...</a></li>

</ul>
</details>

**标签**: `#cyber violence`, `#regulation`, `#China`, `#internet governance`, `#policy`

---