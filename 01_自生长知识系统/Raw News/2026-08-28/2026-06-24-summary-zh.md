---
layout: default
title: "Horizon Summary: 2026-06-24 (ZH)"
date: 2026-06-24
lang: zh
---

> 从 34 条内容中筛选出 10 条重要资讯。

---

1. [Unlimited OCR：一次处理长文档的恒定 KV 缓存 OCR 方法](#item-1) ⭐️ 9.0/10
2. [CXMT 通过 IPO 和 HBM 推进挑战 DRAM 巨头](#item-2) ⭐️ 9.0/10
3. [中国'灵晟'超算以 2.198 ExaFLOPS 登顶 TOP500](#item-3) ⭐️ 9.0/10
4. [TikZ 编辑器：LaTeX 图形的所见即所得工具](#item-4) ⭐️ 8.0/10
5. [AI 编程中不可避免的规范循环](#item-5) ⭐️ 8.0/10
6. [BPF JIT 编译器支持 KASAN](#item-6) ⭐️ 8.0/10
7. [近半数 LG 智能电视应用含住宅代理 SDK](#item-7) ⭐️ 8.0/10
8. [OpenAI 用 GPT-5 打造 AI 动画电影《Critterz》](#item-8) ⭐️ 8.0/10
9. [美国人形机器人关键部件依赖中国供应链](#item-9) ⭐️ 8.0/10
10. [FFmpeg 严重漏洞可通过视频文件远程执行代码](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Unlimited OCR：一次处理长文档的恒定 KV 缓存 OCR 方法](https://github.com/baidu/Unlimited-OCR) ⭐️ 9.0/10

百度研究人员推出了 Unlimited OCR，该方法使用巧妙的架构技巧（R-SWA）在长文档解析过程中保持 KV 缓存大小固定，从而能够一次性处理数百页而不会耗尽内存。 这克服了长文档 OCR 中的根本内存瓶颈，无需昂贵硬件即可支持更长的上下文窗口，可能显著改进文档数字化、RAG 和自动数据提取等应用。 关键创新是 R-SWA（受限滑动窗口注意力），它限制注意力在滑动窗口内，并使用特殊的预填充策略来保持 KV 缓存大小恒定，与输入长度无关。该模型可以在单次前向传播中处理数十到数百页，并从头到尾连续解析，无需增长内存。

hackernews · ingve · 6月23日 11:35 · [社区讨论](https://news.ycombinator.com/item?id=48643426)

**背景**: 传统 OCR 系统独立处理文档页面，丢失跨页上下文。基于 Transformer 的模型使用 KV 缓存存储先前计算的注意力键值对，随着输入长度线性增长，导致长文档内存溢出。这一限制迫使开发者将文档分块，牺牲了上下文理解。Unlimited OCR 提出一种保持固定大小 KV 缓存的架构，实现了真正的长文档一次性解析。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/baidu/Unlimited-OCR">GitHub - baidu/Unlimited-OCR: Unlimited OCR Works: Welcome the Era of One-shot Long-horizon Parsing. · GitHub</a></li>
<li><a href="https://arxiv.org/pdf/2606.23050">Unlimited OCR Works Welcome the Era of One-shot Long-horizon Parsing Baidu Inc.</a></li>
<li><a href="https://news.ycombinator.com/item?id=48643426">Unlimited OCR: One-Shot Long-Horizon Parsing | Hacker News</a></li>

</ul>
</details>

**社区讨论**: 社区反应非常积极，许多评论称赞这一巧妙的架构技巧。评论者指出了对长文档处理的实际意义，有人分享了在乐谱扫描和本地 OCR 方面的相关经验。对先前工作（Deepseek-OCR、PaddleOCR）的致谢也受到赞赏。

**标签**: `#OCR`, `#deep learning`, `#memory optimization`, `#natural language processing`, `#document analysis`

---

<a id="item-2"></a>
## [CXMT 通过 IPO 和 HBM 推进挑战 DRAM 巨头](https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram) ⭐️ 9.0/10

中国的长鑫存储技术（CXMT）正准备进行 IPO，并在 DRAM 市场尤其是高带宽内存（HBM）和晶圆产能扩张方面，加大与三星、SK 海力士和美光的竞争。 此举可能重塑全球 DRAM 格局，减少中国对外国内存芯片的依赖，并影响依赖 HBM 的 AI 硬件供应链。 据报告，CXMT 内存收入达 80 亿美元，正在进行 HBM3 生产，但与现有竞争对手相比仍存在制程节点差距。

rss · Semianalysis · 6月23日 14:51

**背景**: DRAM 是一种用于计算机和服务器的易失性存储器。HBM 是一种高性能 3D 堆叠 DRAM 技术，对 NVIDIA GPU 等 AI 加速器至关重要。目前，三星、SK 海力士和美光主导 DRAM 市场，CXMT 是崛起的中国挑战者。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ChangXin_Memory_Technologies">ChangXin Memory Technologies - Wikipedia</a></li>
<li><a href="https://www.abhs.in/blog/china-cxmt-memory-chip-8-billion-revenue-hbm3-samsung-micron-2026">China's CXMT Hit $8 Billion in Memory Revenue — HBM3 Production...</a></li>

</ul>
</details>

**标签**: `#DRAM`, `#semiconductor`, `#China`, `#memory`, `#geopolitics`

---

<a id="item-3"></a>
## [中国'灵晟'超算以 2.198 ExaFLOPS 登顶 TOP500](https://news.mydrivers.com/1/1131/1131573.htm) ⭐️ 9.0/10

2026 年 6 月 23 日公布的 TOP500 榜单中，中国'灵晟'超算以 2.198 ExaFLOPS 的 HPL 性能位居榜首，成为全球首台纯 CPU 设计突破 2 ExaFLOPS 的系统。 这标志着中国时隔八年重回超算榜首，预示着高性能计算领域向纯 CPU 百亿亿次架构的转变，减少了对 GPU 加速器的依赖。 该系统由 20,480 个节点构成，每个节点配备两颗 LX2 处理器（ARMv9 架构，每颗 304 核心），总计近 1400 万 CPU 核心，功耗约 42.2 MW，能效为 52.07 GigaFLOPS/W。

telegram · zaihuapd · 6月23日 15:30

**背景**: TOP500 榜单根据 HPL 基准测试对全球最强超算进行排名。ExaFLOPS（每秒百亿亿次浮点运算）是百亿亿次计算的门槛。近年来多数百亿亿次系统依赖 GPU 加速器，而灵晟仅凭 CPU 达到了这一水平。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://x.com/Compute_King/status/2069348374609080753">更多的资料： LineShine超级计算机由深圳国家超级计算中心（NSCC-SZ）...</a></li>
<li><a href="https://tech.ifeng.com/c/8tCEPugIDxu">245万个CPU核心，中国超算“灵晟”突破2EFlops_凤凰网</a></li>

</ul>
</details>

**标签**: `#supercomputing`, `#TOP500`, `#HPC`, `#China`, `#exascale`

---

<a id="item-4"></a>
## [TikZ 编辑器：LaTeX 图形的所见即所得工具](https://tikz.dev/editor/) ⭐️ 8.0/10

一款开源的所见即所得 TikZ 图形编辑器已发布，允许用户通过拖拽和调整大小来可视化编辑 TikZ 源代码，同时保持源代码和渲染图形同步。 该编辑器大大简化了创建和修改 TikZ 图形的过程，传统上需要手动调整坐标并重新编译，为大量使用 LaTeX 的研究人员和学者节省了时间。 该编辑器通过解析 TikZ 代码并跟踪对象的精确源位置来工作，当元素移动时仅覆盖数值。它主要使用 Codex AI 编码代理构建，花费约 500 美元的 ChatGPT 订阅费。

hackernews · DominikPeters · 6月23日 14:24 · [社区讨论](https://news.ycombinator.com/item?id=48645437)

**背景**: TikZ 是一个强大的 LaTeX 包，用于创建矢量图形，常用于学术论文。传统上，用户手动编写 TikZ 代码并重新编译查看结果，这可能很繁琐。该编辑器提供实时视觉反馈和双向编辑。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://tikz.org/">LaTeX Graphics with TikZ</a></li>

</ul>
</details>

**社区讨论**: 社区称赞该项目的界面和概念，但批评生成的 TikZ 代码大量使用绝对坐标，这不符合 TikZ 的典型用法。有人推荐了 quiver.app 等专业绘图替代工具，还有评论者提到使用 AI 代币的高昂成本。

**标签**: `#TikZ`, `#LaTeX`, `#editor`, `#WYSIWYG`, `#open-source`

---

<a id="item-5"></a>
## [AI 编程中不可避免的规范循环](https://lucumr.pocoo.org/2026/6/23/the-coming-loop/) ⭐️ 8.0/10

作者提出了“即将到来的循环”这一概念，即使用 AI 编程代理时不可避免的规格说明迭代澄清过程，将软件开发转向以规范为驱动的模式。 这一洞察揭示了范式的转变：开发者从编码者转变为规范制定者和审查者，深刻影响了 AI 代理时代的生产力和软件设计的本质。 核心瓶颈变成了规格说明的清晰度而非代码生成；循环过程需要对规范进行反复细化，直到 AI 代理能够准确实现，通常需要多次迭代。

hackernews · ingve · 6月23日 11:06 · [社区讨论](https://news.ycombinator.com/item?id=48643180)

**背景**: AI 编程代理是能够根据自然语言提示自主编写、修改和调试代码的工具。规范驱动开发（SDD）是一种 2026 年的方法论，其中可执行的规范成为事实来源，AI 据此生成代码。“即将到来的循环”描述了模糊规范导致反复来回反馈的循环，使得编写规范成为关键技能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://agentic.ai/best/coding-agents">18 Best AI Coding Agents in 2026 — Agentic.ai</a></li>
<li><a href="https://thebcms.com/blog/spec-driven-development">Spec-Driven Development (SDD): The Definitive 2026 Guide</a></li>
<li><a href="https://developer.microsoft.com/blog/spec-driven-development-spec-kit">Diving Into Spec-Driven Development With GitHub Spec Kit What is Spec-Driven Development? | Spec Kit Documentation spec-kit/spec-driven.md at main · github/spec-kit · GitHub Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl Spec-Driven Development: A Spec-First Approach to AI-Native ... Spec-Driven Development</a></li>

</ul>
</details>

**社区讨论**: 评论者一致认为规范循环是真实存在的，且常常成为瓶颈。有人指出，清晰度需要前期思考，AI 无法加速这一过程。另一人将此视为将软件视为生命系统的转变。第三人表示，编写清晰的规范是主要挑战，当规范良好时，代理表现出色。

**标签**: `#AI agents`, `#software development`, `#paradigm shift`, `#spec-driven development`, `#LLM tools`

---

<a id="item-6"></a>
## [BPF JIT 编译器支持 KASAN](https://lwn.net/Articles/1077740/) ⭐️ 8.0/10

Alexis Lothoré 正在为 BPF 即时编译 (JIT) 编译器添加内核地址消毒器 (KASAN) 支持，用于检测 JIT 生成代码中的释放后使用和越界错误。他于 2026 年 Linux 存储、文件系统、内存管理与 BPF 峰会上展示了这一工作。 这通过让 KASAN 能够捕获 BPF JIT 代码中的内存错误提升了内核安全性，此前这些代码绕过了检测。对内核测试和可靠性意义重大，因为 BPF 广泛应用于网络、跟踪和安全领域。 目前，该补丁仅针对 x86 上的 LDX 和 STX BPF 指令（加载和存储），忽略了栈访问。由于寄存器保存和恢复，开销很大，一条指令变成十二条，但正在考虑通过内联 __asan*() 函数等优化方式来降低开销。

rss · LWN.net · 6月23日 15:53

**背景**: KASAN 是 Linux 内核中的一个动态内存错误检测器，通过软件或硬件内存标记来识别释放后使用和越界访问。BPF JIT 编译器将 BPF 字节码转换为本地机器码以提高性能；此前，它直接发出指针解引用，不进行 KASAN 检查。向 JIT 添加 KASAN 检测可确保 JIT 生成的代码也受到监控。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.kernel.org/dev-tools/kasan.html">Kernel Address Sanitizer (KASAN) — The Linux Kernel</a></li>
<li><a href="https://sysctl-explorer.net/net/core/bpf_jit_enable/">bpf_jit_enable | sysctl-explorer.net</a></li>

</ul>
</details>

**社区讨论**: 在演讲中，听众建议内联 __asan*() 函数可以减少寄存器保存和恢复的开销，但 Lothoré 指出简单的内联可能更糟。还有人问为什么不在编译器或验证器中加入检测，Lothoré 解释这需要稳定的 KASAN API 并会使测试复杂化。目前尚未发现任何错误，因为补丁尚未经过广泛测试。

**标签**: `#kernel`, `#BPF`, `#KASAN`, `#JIT`, `#memory safety`

---

<a id="item-7"></a>
## [近半数 LG 智能电视应用含住宅代理 SDK](https://spur.us/blog/smart-tv-apps-residential-proxy-sdks) ⭐️ 8.0/10

一项安全扫描发现，在抽样的 6038 款 LG 和三星智能电视应用中，有 2058 款包含住宅代理 SDK，其中 LG 平台占比接近一半。这些应用如屏保、小游戏等在用户关闭后仍可继续运行代理功能。 这暴露了一个广泛的隐私风险：家庭 IP 地址可能在用户不知情的情况下被劫持用于代理网络，从而可能为欺诈或内容抓取等恶意活动提供便利。该事件突显了主要电视制造商尚未解决的关键物联网安全漏洞。 受影响的应用包括屏保、时钟和小游戏；部分应用在关闭后仍然活跃。亚马逊和 Roku 已在其平台上禁止此类 SDK，但 LG 和三星尚未公开实施同等限制。

telegram · zaihuapd · 6月23日 02:26

**背景**: 住宅代理是指互联网服务提供商分配给真实家庭用户的 IP 地址，常用于匿名或绕过地理限制。嵌入智能电视应用的住宅代理 SDK 可以将电视变成代理网络中的一个节点，允许第三方通过家庭 IP 路由流量。这可能使用户面临因 IP 被用于非法活动而承担法律责任的风险，并降低网络性能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://segmentfault.com/a/1190000047344538">什么是住宅代理（Residential Proxy）？详解原理、优势与应用场景</a></li>
<li><a href="https://blog.csdn.net/2303_78381320/article/details/161290563">住宅IP代理详解：工作原理、类型与使用场景选型指南（2026）-CSDN博客</a></li>

</ul>
</details>

**标签**: `#smart-tv`, `#security`, `#privacy`, `#IoT`, `#residential-proxy`

---

<a id="item-8"></a>
## [OpenAI 用 GPT-5 打造 AI 动画电影《Critterz》](https://t.me/zaihuapd/42125) ⭐️ 8.0/10

OpenAI 正在支持制作一部名为《Critterz》的动画长片，该片主要使用包括 GPT-5 在内的 OpenAI 自有 AI 工具完成，制作预算不到 3000 万美元，制作周期仅 9 个月。 该项目展示了 AI 大幅降低动画长片制作成本和时间的能力，可能颠覆传统动画行业，并为独立创作者带来新的可能性。 该片计划在戛纳电影节首映，并于 2026 年全球上映。其预算和制作周期远低于传统动画电影——后者通常耗资超过 1 亿美元、耗时 3 至 5 年。

telegram · zaihuapd · 6月23日 03:11

**背景**: GPT-5 是 OpenAI 于 2025 年 8 月发布的第五代多模态大语言模型，能够处理文本、图像等多种数据类型。AI 动画是指利用机器学习技术自动完成动作生成、角色一致性、场景渲染等任务，而这些任务传统上需要大量人力。OpenAI 对《Critterz》的支持展示了一条端到端的 AI 驱动制作流程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GPT-5">GPT-5 - Wikipedia</a></li>
<li><a href="https://www.neolemon.com/blog/ai-storyboard-to-animation-pipeline-workflow/">AI Storyboard To Animation Pipeline: Complete Workflow GitHub - calesthio/OpenMontage: World's first open-source ... AI Animation in Blender: Complete Guide (2026) | 3D-Agent AI in Animation: Tools, Uses & Future Trends Animation pipeline: key steps, challenges and tools | LucidLink Where AI Fits in an Animation Pipeline: Pre-Production ... How Pixar’s Animation Pipeline Has Evolved with AI</a></li>

</ul>
</details>

**标签**: `#OpenAI`, `#AI film`, `#GPT-5`, `#animation`, `#creative AI`

---

<a id="item-9"></a>
## [美国人形机器人关键部件依赖中国供应链](https://t.me/zaihuapd/42129) ⭐️ 8.0/10

这种依赖性凸显了美国机器人行业日益增长的战略脆弱性——摩根士丹利估算中国供应链可将制造成本压低三分之二，可能改变竞争格局，并促使美国议员考虑立法评估相关风险。 迪士尼的“奥拉夫”机器人使用了中国宇树科技的部件，特斯拉正与中国供应商合作推进 Optimus 量产准备。2025 年 2 月美国两党议员提出法案，拟评估美国机器人竞争力及供应链风险。

telegram · zaihuapd · 6月23日 07:47

**背景**: 人形机器人旨在模仿人类外观和动作，需要精密电机、关节、磁体和传感器来实现灵巧操作。美国和中国是该新兴领域的主要竞争者，中国凭借其成熟的电子和制造供应链实现更低成本和更快迭代。

**标签**: `#robotics`, `#supply chain`, `#US-China relations`, `#humanoid robots`, `#technology competition`

---

<a id="item-10"></a>
## [FFmpeg 严重漏洞可通过视频文件远程执行代码](https://cybernews.com/security/critical-ffmpeg-vulnerability-enables-complete-compromise/) ⭐️ 8.0/10

FFmpeg 公开了一个致命漏洞（CVE-2026-8461，代号 PixelSmash），位于 MagicYUV 解码器中，通过构造视频文件可实现远程代码执行。该漏洞已在紧急发布的 8.1.2 版本中得到修复。 FFmpeg 被嵌入无数播放器、服务器和物联网设备，未修补的系统可能因看似无害的视频文件而完全沦陷。这一高危漏洞（CVSS 8.8）要求生态系统立即更新。 该漏洞是 FFmpeg 的 libavcodec 组件中的一个堆越界写入问题，由特制的 MagicYUV 编码视频触发。攻击者不仅可通过直接播放利用，还可通过缩略图生成或媒体库扫描触发，且痕迹极少。

telegram · zaihuapd · 6月23日 15:00

**背景**: FFmpeg 是一个被广泛使用的开源多媒体库，为 VLC、Jellyfin、Kodi、OBS 等应用提供视频处理能力。MagicYUV 解码器用于处理一种无损视频编码。堆越界写入是指数据被写入分配内存区域之外，可能导致代码执行或系统崩溃。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.securityweek.com/ffmpeg-pixelsmash-flaw-allows-rce-on-video-players-media-servers-nas-appliances/">FFmpeg PixelSmash Flaw Allows RCE on Video Players, Media ...</a></li>
<li><a href="https://undercodenews.com/pixelsmash-exposes-a-hidden-threat-how-one-ffmpeg-flaw-could-turn-everyday-video-files-into-remote-attack-weapons/">PixelSmash Exposes a Hidden Threat: How One FFmpeg Flaw Could ...</a></li>
<li><a href="https://cybersecuritynews.com/ffmpeg-vulnerability-weaponize-media-files/">Critical FFmpeg Vulnerability Allows Attackers to Weaponize ...</a></li>

</ul>
</details>

**标签**: `#FFmpeg`, `#security vulnerability`, `#remote code execution`, `#CVE`, `#multimedia`

---