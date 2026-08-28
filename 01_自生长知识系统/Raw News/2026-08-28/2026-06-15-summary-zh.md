---
layout: default
title: "Horizon Summary: 2026-06-15 (ZH)"
date: 2026-06-15
lang: zh
---

> 从 26 条内容中筛选出 10 条重要资讯。

---

1. [Linux 7.1 内核发布，带来重大子系统改进](#item-1) ⭐️ 9.0/10
2. [华为开源盘古 2.0，目标世界第一](#item-2) ⭐️ 9.0/10
3. [美国政府迫使 Anthropic 限制两款 AI 模型](#item-3) ⭐️ 9.0/10
4. [形式化方法与编程的未来](#item-4) ⭐️ 8.0/10
5. [JavaScript 演变为编译目标](#item-5) ⭐️ 8.0/10
6. [如何通过创业赚取十亿美元](#item-6) ⭐️ 8.0/10
7. [中芯国际 N+3 金属间距对比英特尔 18A](#item-7) ⭐️ 8.0/10
8. [连贯上下文能悄无声息地将 LLM 切换到不同内部状态](#item-8) ⭐️ 8.0/10
9. [验证税：LLM 代理中与任务时长相关的安全-成功权衡](#item-9) ⭐️ 8.0/10
10. [2026 年一季度美国 75 个数据中心项目被阻，总值 1300 亿美元](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Linux 7.1 内核发布，带来重大子系统改进](https://lwn.net/Articles/1077758/) ⭐️ 9.0/10

Linus Torvalds 发布了 Linux 7.1 内核，包含新的 clone() 标志、对 io_uring 的 BPF 支持、ublk 的零拷贝 I/O、初始 sched_ext 子调度器支持、交换改进以及完全重写的 NTFS 实现。 此版本集成了期待已久的功能，如 BPF 与 io_uring 的结合以及通过 sched_ext 实现的可扩展调度，这将增强 I/O 性能和进程管理灵活性。重写的 NTFS 驱动程序也改善了文件系统兼容性。 sched_ext 子调度器支持被描述为初始且不完整，而 NTFS 驱动程序则完全重写。内核还移除了对旧有的 486 架构的支持。

rss · LWN.net · 6月14日 18:47

**背景**: Linux 内核是操作系统的核心，管理硬件和系统资源。io_uring 是一种现代异步 I/O 接口，用于高效的文件和网络操作。sched_ext 允许在 BPF 中编写调度策略并动态加载。ublk 是一种用户空间块设备驱动程序，提供安全性和灵活性。NTFS 是 Microsoft Windows 使用的文件系统。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Io_uring">io_uring - Wikipedia</a></li>
<li><a href="https://github.com/sched-ext/scx">GitHub - sched-ext/scx: sched_ext schedulers and tools · GitHub</a></li>
<li><a href="https://www.kernel.org/doc/html/latest/block/ublk.html">Userspace block device driver (ublk driver) — The Linux ...</a></li>

</ul>
</details>

**标签**: `#Linux`, `#kernel`, `#BPF`, `#io_uring`, `#NTFS`

---

<a id="item-2"></a>
## [华为开源盘古 2.0，目标世界第一](https://t.me/zaihuapd/41948) ⭐️ 9.0/10

在华为开发者大会 2026 上，华为发布了开源盘古 openPangu 2.0 模型，包含 505B 参数的 Pro 版和 92B 参数的 Flash 版，支持 512K 上下文。计划从 6 月 30 日起陆续开源预训练代码等 7 大组件。 此次发布是科技巨头的一项重大开源贡献，通过提供一个针对昇腾硬件和鸿蒙系统优化的超大可访问模型，可能改变 AI 格局。它巩固了华为在全球 AI 竞赛中的地位，尤其在中国生态内。 该模型针对昇腾 AI 计算和鸿蒙系统进行了优化，512K 上下文长度支持长文档处理。完整开源将从 6 月 30 日开始，涵盖预训练代码等 7 个组件，可能包括模型权重。

telegram · zaihuapd · 6月14日 08:05

**背景**: 华为的昇腾计算平台是结合昇腾 AI 处理器和基础软件的全栈 AI 基础设施，支持云端、边缘和设备的训练与推理。鸿蒙是华为的分布式操作系统。余承东提到，虽然华为的算力因支持国内企业而有限，但公司在大模型概念流行之前就已开始研发盘古。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://e.huawei.com/cn/products/computing/ascend">昇腾计算-华为Ascend-AI计算-华为企业业务</a></li>
<li><a href="https://www.huaweicloud.com/product/ecs/ascend.html">昇腾AI云服务器_ECS-华为云</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/1952064479069188801">AI算力新纪元：华为昇腾超节点战略与英伟达H100/H200的深度对决</a></li>

</ul>
</details>

**标签**: `#Huawei`, `#open-source`, `#large language model`, `#AI`, `#Pangu`

---

<a id="item-3"></a>
## [美国政府迫使 Anthropic 限制两款 AI 模型](https://t.me/zaihuapd/41949) ⭐️ 9.0/10

美国政府以国家安全为由，向 Anthropic 发出出口管制指令，要求阻止任何外国公民（包括公司内部的外籍员工）访问 Claude Fable 5 和 Claude Mythos 5 模型，原因是担心模型可能被越狱带来安全风险。 这一前所未有的政府干预表明围绕强大 AI 模型的监管紧张局势正在升级，可能为 AI 能力的出口管制树立先例，影响全球公司部署先进模型的方式。 Anthropic 已经关闭这两款模型对所有客户的访问，其他 Claude 模型不受影响。公司正在努力尽快恢复访问，同时确保合规。

telegram · zaihuapd · 6月14日 09:06

**背景**: 越狱（jailbreaking）是指绕过 AI 模型内置的安全机制，引发意外或有害输出。Claude Fable 5 和 Claude Mythos 5 是 Anthropic 开发的先进 AI 模型；Mythos 类模型能够识别并利用主要软件中的零日漏洞，引发了重大安全担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/news/claude-fable-5-mythos-5">Claude Fable 5 and Claude Mythos 5 \ Anthropic</a></li>
<li><a href="https://red.anthropic.com/2026/mythos-preview/">Claude Mythos Preview \ red.anthropic.com</a></li>
<li><a href="https://www.lakera.ai/blog/jailbreaking-large-language-models-guide">Jailbreaking Large Language Models: Techniques, Examples ...</a></li>

</ul>
</details>

**标签**: `#AI regulation`, `#Anthropic`, `#national security`, `#export control`, `#AI safety`

---

<a id="item-4"></a>
## [形式化方法与编程的未来](https://blog.janestreet.com/formal-methods-at-jane-street-index/?from_theconsensus=1) ⭐️ 8.0/10

Jane Street 的博客文章探讨了形式化方法，包括历史上的证明自动化，并认为它们可能在验证 AI 生成的代码中发挥关键作用。 随着 AI 生成越来越多的代码，形式化验证对于确保正确性和安全性变得至关重要，将人力从编写代码转向验证代码。 讨论追溯了从早期的 Oppen-Nelson SAT 求解器到 Boyer-Moore 证明器的证明自动化历程，强调了在建议引理方面仍需人类指导。形式化方法需要编写本身可能包含错误的规范，但它们提供了与传统测试不同的严谨性。

hackernews · eatonphil · 6月14日 12:35 · [社区讨论](https://news.ycombinator.com/item?id=48526633)

**背景**: 形式化方法是用于规范、开发和验证软件及硬件系统的数学严格化技术。它们使用形式逻辑来证明系统满足其规范，提供比单独测试更高的保证。自动定理证明（ATP）和证明助手是关键工具，而证明自动化旨在减少涉及的人工工作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Formal_methods">Formal methods - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Automated_theorem_proving">Automated theorem proving - Wikipedia</a></li>
<li><a href="https://web.mit.edu/16.35/www/lecturenotes/FormalMethods.pdf">Introducing Formal Methods - MIT</a></li>

</ul>
</details>

**社区讨论**: 评论者分享了个人使用形式化方法的经验：一位前正确性证明工作者指出早期的证明自动化比许多后来的系统更先进；另一位则在 Scala 3 中使用表达性类型来强制编译时证明。一位非英语母语者强调了通过翻译学习编程的挑战，并建议 AI 应将人类价值转向验证。一位评论者质疑形式化规范是否只是'以不同方式编写的测试'，并可能遭受相同的错误。

**标签**: `#formal methods`, `#proof automation`, `#AI verification`, `#programming languages`, `#Jane Street`

---

<a id="item-5"></a>
## [JavaScript 演变为编译目标](https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript) ⭐️ 8.0/10

Gary Bernhardt 在 2014 年的演讲中幽默地预言 JavaScript 将成为编译目标，这一预言随着 WebAssembly 和 Electron 的兴起已基本成为现实。 该演讲准确预见了 Web 开发的发展轨迹，例如 TypeScript 等语言编译为 JavaScript，以及通过 Electron 使用 Web 技术构建桌面应用，影响了当今开发者处理跨平台开发的方式。 演讲提到了 asm.js（WebAssembly 的前身），后来被 WebAssembly 取代。另一个预言 Electron 使得使用 Web 技术构建桌面应用成为可能。

hackernews · subset · 6月14日 12:38 · [社区讨论](https://news.ycombinator.com/item?id=48526661)

**背景**: JavaScript 最初是作为网页浏览器的脚本语言设计的，但后来成为所有浏览器原生支持的唯一语言。为了提升性能并让其他语言也能在 Web 上运行，2013 年引入了 asm.js（JavaScript 的严格子集），随后在 2015 年推出了 WebAssembly（一种二进制格式）。Electron 于 2013 年发布，允许开发者使用 JavaScript、HTML 和 CSS 等 Web 技术构建桌面应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/WebAssembly">WebAssembly</a></li>
<li><a href="https://en.wikipedia.org/wiki/Electron_(software_framework)">Electron (software framework)</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍认为 Bernhardt 的预言很准确，指出 JavaScript 已成为编译目标，Electron 将 Web 技术带到了桌面应用。一些人指出 WebAssembly 仍然缺乏直接操作 DOM 的能力，需要 JavaScript 作为胶水代码。

**标签**: `#JavaScript`, `#WebAssembly`, `#TypeScript`, `#Programming Languages`, `#History`

---

<a id="item-6"></a>
## [如何通过创业赚取十亿美元](https://paulgraham.com/earn.html) ⭐️ 8.0/10

保罗·格雷厄姆发表了一篇文章，认为通过创办创新企业创造价值，可以合法赚取十亿美元，并反驳了将财富等同于剥削的批评。 这篇文章引发了关于创业生态系统中财富创造伦理的重要辩论，影响了企业家和投资者如何为巨额财富辩护。 格雷厄姆区分了被给予十亿美元和通过创造同等价值来赚取十亿美元，并指出创造性破坏的过程往往涉及道德纠缠。

hackernews · kingstoned · 6月14日 11:50 · [社区讨论](https://news.ycombinator.com/item?id=48526360)

**背景**: 保罗·格雷厄姆是著名创业加速器 Y Combinator 的联合创始人。他关于创业和财富的文章广为流传。通过创业‘赚取’财富的概念是科技文化的核心，常与对财富不平等的批评形成对比。

**社区讨论**: 评论呈现两极分化：一些人赞扬格雷厄姆的观点并对负面评论感到遗憾，而另一些人则批评他对‘赚取’一词的使用，认为十亿美元财富不可避免地涉及未被考虑的剥削或破坏。

**标签**: `#startups`, `#wealth`, `#entrepreneurship`, `#Paul Graham`, `#economics`

---

<a id="item-7"></a>
## [中芯国际 N+3 金属间距对比英特尔 18A](https://newsletter.semianalysis.com/p/steel-smic-n3-teardown) ⭐️ 8.0/10

SemiAnalysis 发布了详细的拆解分析，对比了中芯国际 N+3 节点的金属间距与英特尔 18A 等竞品，并提供了原创测量数据。 这一对比至关重要，因为它揭示了中芯国际在无 EUV 光刻条件下制造的先进节点如何与英特尔前沿节点竞争，对半导体竞赛和地缘政治具有启示意义。 金属间距是相邻金属互连线中心之间的距离；间距越小通常代表晶体管密度越高。中芯国际 N+3 是其 7nm 级工艺的缩放演进，在未使用 EUV 的情况下接近 5nm 等效密度。

rss · Semianalysis · 6月14日 19:14

**背景**: 在半导体制造中，'5nm'等节点名称常是营销术语而非物理尺寸；金属间距是密度的关键指标。中芯国际受美国制裁限制，无法获得 EUV 光刻机，但仍通过多次图案化技术利用 DUV 推进至 N+3。英特尔 18A 是英特尔最先进的节点，采用 RibbonFET 环绕栅极晶体管和 PowerVia 背面供电技术。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Semiconductor_Manufacturing_International_Corporation">Semiconductor Manufacturing International Corporation - Wikipedia</a></li>
<li><a href="https://techlevated.com/evolution-of-metal-pitch-in-semiconductor-transistors/">Evolution of Metal Pitch in Semiconductor Transistors</a></li>
<li><a href="https://en.wikipedia.org/wiki/5_nm_process">5 nm process - Wikipedia</a></li>

</ul>
</details>

**标签**: `#semiconductors`, `#SMIC`, `#Intel 18A`, `#process technology`, `#teardown`

---

<a id="item-8"></a>
## [连贯上下文能悄无声息地将 LLM 切换到不同内部状态](https://www.reddit.com/r/MachineLearning/comments/1u5xnxg/coherent_context_can_silently_shift_llms_into_a/) ⭐️ 8.0/10

独立研究者 PresentSituation8736 发现，强大的连贯上下文可以在输出生成之前改变 LLM 的内部表征空间，使得 RLHF 和输出过滤器等安全机制对变化视而不见。 这一发现揭示了当前 LLM 安全方法的一个根本性盲点——它们只检查最终输出，意味着精心构造的对手可以在不触发任何表层警报的情况下绕过安全防护。 研究者测量了隐藏状态几何结构、残差流轨迹，并在 Gemma-3-12B-IT 等开放模型上使用了稀疏自编码器（SAE）读数，使用的目标文本是连贯的文本而非直接的越狱提示。

reddit · r/MachineLearning · /u/PresentSituation8736 · 6月14日 21:42

**背景**: LLM 是通过一系列层变换词元嵌入来处理文本的神经网络。残差流是一个核心组件，它在各层之间累积信息，充当共享的表征空间。机械可解释性旨在逆向工程这些模型的内部算法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>
<li><a href="https://arxiv.org/html/2312.12141v1">Exploring the Residual Stream of Transformers - arXiv.org</a></li>
<li><a href="https://seantrott.substack.com/p/mechanistic-interpretability-for">" Mechanistic interpretability " for LLMs, explained</a></li>

</ul>
</details>

**标签**: `#AI safety`, `#mechanistic interpretability`, `#LLM`, `#alignment`, `#internal state`

---

<a id="item-9"></a>
## [验证税：LLM 代理中与任务时长相关的安全-成功权衡](https://www.reddit.com/r/MachineLearning/comments/1u58mkq/the_verifier_tax_horizondependent_safetysuccess/) ⭐️ 8.0/10

一篇在 ACM CAIS 2026 上发表的新论文提出了“验证税”概念，即工具使用型 LLM 代理中与任务时长相关的安全-成功权衡，并提出了一个结合确定性检查与基于 LLM 的验证器的两层验证架构。 这项工作表明，当前仅关注成功率的评估方法可能掩盖不安全完成的情况，而验证税揭示了随着任务变长，安全性与任务完成之间的关键张力，影响 LLM 代理在实际应用中的安全部署。 该研究使用τ-bench 工具使用场景，将结果分解为安全成功、不安全成功和失败；发现验证减少了不安全成功，但随着任务时长增加也降低了任务完成率，且存在模型相关的交互时长（15–30 轮）。

reddit · r/MachineLearning · /u/AccomplishedLeg1508 · 6月14日 02:09

**背景**: LLM 代理越来越多地与外部工具（如 API）结合使用来完成多步骤任务。然而，代理可能在违反安全或策略规则的情况下达成任务目标，导致“不安全成功”。验证税概念源于这样的观察：添加验证来捕捉此类违规行为可能会无意中降低代理完成长周期任务的能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2603.19328">[2603.19328] The Verifier Tax: Horizon Dependent Safety Success ...</a></li>
<li><a href="https://github.com/sierra-research/tau2-bench">GitHub - sierra-research/tau2-bench: τ-Bench: A Benchmark for ...</a></li>
<li><a href="https://www.harrisburgu.edu/news/2026-06-05-ai-agent-safety-doctoral-research/">HU Student's Doctoral Research on AI Agent Safety Featured at...</a></li>

</ul>
</details>

**标签**: `#LLM agents`, `#AI safety`, `#verification`, `#tool use`, `#evaluation`

---

<a id="item-10"></a>
## [2026 年一季度美国 75 个数据中心项目被阻，总值 1300 亿美元](https://www.tomshardware.com/tech-industry/artificial-intelligence/more-than-75-data-center-build-outs-worth-usd130-billion-have-been-successfully-blocked-in-the-first-four-months-of-2026-bipartisan-opposition-mounts-nationwide-over-fears-of-soaring-power-and-water-costs) ⭐️ 8.0/10

2026 年第一季度，美国全国至少有 75 个数据中心建设项目被阻止或推迟，总价值约 1300 亿美元，数量已与 2025 年全年持平。社区及跨党派政治人物对能源消耗与环境影响的担忧显著升温。 这标志着数据中心基础设施部署的重大转折，可能减缓 AI 和云计算的发展。草根反对组织在三个月内从 396 个激增至 833 个，遍布 49 个州，表明能源和环境制约可能成为科技行业的关键瓶颈。 被阻项目总值约 1300 亿美元，仅一个季度就与 2025 年全年持平。各州议会提出了大量监管法案，部分联邦议员也推动暂停数据中心建设的立法提案。

telegram · zaihuapd · 6月14日 03:03

**背景**: 数据中心消耗大量电力和水资源，引发对电网压力和环境影响的担忧。随着 AI 工作负载激增，对新数据中心的需求急剧上升，导致与当地社区在资源分配上的冲突。跨党派的反对表明这并非党派问题，而是广泛的环境和经济关切。

**标签**: `#data centers`, `#energy regulation`, `#AI infrastructure`, `#US policy`, `#environmental impact`

---