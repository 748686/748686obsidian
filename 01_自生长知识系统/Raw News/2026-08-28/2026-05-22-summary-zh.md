---
layout: default
title: "Horizon Summary: 2026-05-22 (ZH)"
date: 2026-05-22
lang: zh
---

> From 41 items, 11 important content pieces were selected

---

1. [黄仁勋：英伟达已基本放弃中国 AI 芯片市场](#item-1) ⭐️ 9.0/10
2. [全新 Freenet 采用 WebAssembly 实现去中心化应用](#item-2) ⭐️ 8.0/10
3. [谷歌测试 AI 驱动广告格式，扩大直接优惠试点](#item-3) ⭐️ 8.0/10
4. [在 MacBook 上用 Gemma4-31B 本地索引一年视频](#item-4) ⭐️ 8.0/10
5. [谷歌 Antigravity IDE 的诱饵调包策略](#item-5) ⭐️ 8.0/10
6. [Vivaldi 8.0 发布，带来新功能和改进](#item-6) ⭐️ 8.0/10
7. [GCC 的 BPF 支持接近与 LLVM 功能对等](#item-7) ⭐️ 8.0/10
8. [提议为 Linux 内核添加私有内存节点](#item-8) ⭐️ 8.0/10
9. [特斯拉监督版 FSD 在华推出](#item-9) ⭐️ 8.0/10
10. [OpenAI 计划最快本周提交 IPO 申请](#item-10) ⭐️ 8.0/10
11. [腾讯发布操作系统级 AI 助手 Marvis](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [黄仁勋：英伟达已基本放弃中国 AI 芯片市场](https://www.cnbc.com/2026/05/21/nvidia-jensen-huang-china-ai-chip-market-huawei.html) ⭐️ 9.0/10

英伟达 CEO 黄仁勋宣布，由于美国出口管制，公司已基本放弃中国 AI 芯片市场，将其让给华为等本土竞争对手。 这标志着全球 AI 芯片供应链的重大转变，英伟达退出中国可能加速中国自主可控进程，并重塑 AI 硬件竞争格局。 黄仁勋表示，英伟达已告知投资者不要期望获得在华销售先进芯片的许可，并指出华为本土芯片生态系统非常强劲。英伟达目前正将资金用于支持供应链扩张，并宣布了 800 亿美元的股票回购计划。

telegram · zaihuapd · May 21, 05:52

**背景**: 美国出口管制限制了英伟达 H100 等先进 AI 芯片对华销售。英伟达 H100 是基于 Hopper 架构的数据中心 GPU，配备 Tensor Core 和 Transformer 引擎，专为 AI 训练和推理设计。与此同时，华为开发了昇腾 AI 芯片（如昇腾 950 系列），在中国市场与英伟达产品竞争。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Nvidia_H100_GPU">Nvidia H100 GPU</a></li>
<li><a href="https://tech-insider.org/huawei-ascend-950pr-ai-chip-nvidia-china-2026/">Huawei Ascend 950PR: The 1.56 PFLOP AI Chip vs Nvidia [2026]</a></li>
<li><a href="https://www.huaweicentral.com/huawei-ascend-950-ai-chips-demand-surges/">Huawei Ascend 950 AI chips demand surges after DeepSeek V4 ...</a></li>

</ul>
</details>

**标签**: `#Nvidia`, `#AI chips`, `#China`, `#export controls`, `#Huawei`

---

<a id="item-2"></a>
## [全新 Freenet 采用 WebAssembly 实现去中心化应用](https://freenet.org/) ⭐️ 8.0/10

原始 Freenet（现更名为 Hyphanet）已被彻底重新设计并重新发布，采用全局去中心化键值存储，其中键是 WebAssembly 合约，用于定义有效状态、变更规则以及用于一致性的可交换合并操作。 该方法为去中心化系统中的一致性问题提供了新颖解决方案，无需区块链等共识协议，可实现快速状态传播（数秒内），并允许应用像单页应用一样在浏览器中下载和运行。 每个合约必须定义可交换的合并操作，使得状态更新像病毒一样传播，通常能在数秒内达成全局一致。早期应用包括 River（群聊）和 Delta（CMS），目前仅支持桌面端，尚无移动版本。

hackernews · sanity · May 21, 14:34 · [社区讨论](https://news.ycombinator.com/item?id=48223362)

**背景**: Freenet 最初于 2000 年发布，是一个点对点文件共享网络，现已更名为 Hyphanet。WebAssembly（WASM）是一种在浏览器中运行的二进制指令格式，在此用于智能合约。可交换合并操作是一种类似 CRDT 的技术，无需中央协调即可确保一致性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://interjectedfuture.com/a-simple-way-to-understand-crdts/">A simple way to understand CRDTs</a></li>
<li><a href="https://interjectedfuture.com/trade-offs-between-different-crdts/">Trade-offs between Different CRDTs</a></li>
<li><a href="https://gitplanet.com/label/p2p">Top p2p open source projects - GitPlanet</a></li>

</ul>
</details>

**社区讨论**: 社区反应不一：有人批评治理决策在未咨询原团队的情况下强制重写，而另一些人则就合并功能展开技术辩论，建议使用更新日志作为替代方案。还有人担心“幽灵键”依赖向 Freenet 捐款而非销毁加密货币。

**标签**: `#p2p`, `#decentralized-apps`, `#webassembly`, `#blockchain-alternative`, `#freenet`

---

<a id="item-3"></a>
## [谷歌测试 AI 驱动广告格式，扩大直接优惠试点](https://blog.google/products/ads-commerce/google-marketing-live-search-ads/) ⭐️ 8.0/10

谷歌在 2026 年 Google Marketing Live 上宣布，将 Gemini AI 整合到搜索中，创建新的对话式广告格式，包括对话发现广告和 AI 驱动的购物广告，并正在向更多品牌和用户扩展其直接优惠试点。 这些 AI 生成的广告可能通过使广告更加个性化和有说服力，显著改变用户体验，引发关于操纵和搜索效用下降的伦理担忧，因为用户可能更难区分自然结果和赞助内容。 新格式利用 Gemini 根据用户查询为产品编写自定义解释，而直接优惠允许广告商在搜索结果中直接展示实时优惠；该试点自 2026 年 1 月开始运行，已有 Chewy、Gap 和 L'Oreal 等品牌参与。

hackernews · sofumel · May 21, 09:49 · [社区讨论](https://news.ycombinator.com/item?id=48220105)

**背景**: 谷歌搜索长期以来一直将广告与自然结果并列显示，但生成式 AI（Gemini）的引入标志着向更对话式和上下文感知的广告体验的转变。直接优惠是谷歌首个代理式广告格式，旨在自动连接产品研究和购买决策。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.google/products/ads-commerce/google-marketing-live-search-ads/">New ad formats built with Gemini coming to Google Search</a></li>
<li><a href="https://www.luzern.co/direct-offers-googles-first-agentic-ad-format/">Direct Offers : Google ’s First Agentic Ad Format – Luzern</a></li>
<li><a href="https://searchengineland.com/google-tests-new-conversational-ad-formats-in-ai-mode-and-search-478115">Google tests new conversational ad formats in AI Mode and Search</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了对 AI 生成广告将更有效操纵用户的强烈担忧，有用户称其为'AI 广告邪恶本质的精髓'。其他人担心谷歌收集训练数据以在人们明知被影响时仍能影响他们，一些人预测搜索将变得基本无用。

**标签**: `#ads`, `#Google Search`, `#AI`, `#privacy`, `#SEO`

---

<a id="item-4"></a>
## [在 MacBook 上用 Gemma4-31B 本地索引一年视频](https://blog.simbastack.com/indexed-a-year-of-video-locally/) ⭐️ 8.0/10

一位开发者通过在 2021 款 MacBook 上完全本地运行 310 亿参数的多模态模型 Gemma4-31B，并使用 50GB 交换内存，成功索引了一年的个人视频素材。 这表明强大的本地 LLM 可以处理视频索引等实际的内存密集型任务，而无需依赖云服务，为私密、离线的个人存档工具铺平了道路。 模型以 4 位量化运行，权重约需 19 GiB，但作者报告由于上下文和其他应用，实际使用达 28.4 GiB；大量交换内存使用导致 SSD 磨损问题。

hackernews · asenna · May 21, 14:01 · [社区讨论](https://news.ycombinator.com/item?id=48222733)

**背景**: Gemma4-31B 是 Google DeepMind 推出的开放多模态模型，可以将视频作为帧序列处理。本地 LLM 视频索引涉及提取帧、用模型生成描述并构建可搜索的索引。内存有限的 MacBook 使用交换内存（将磁盘空间当作虚拟内存）来容纳大模型，这可能会加速 SSD 磨损。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/google/gemma-4-31B">google/gemma-4-31B · Hugging Face</a></li>
<li><a href="https://medium.com/@bSharpML/use-llamaindex-and-a-local-llm-to-summarize-youtube-videos-29817440e671">Use LlamaIndex and a Local LLM to Summarize YouTube Videos</a></li>

</ul>
</details>

**社区讨论**: 评论者讨论了分享技能文件以及项目的 GitHub 仓库（framedex）。有人担心大量交换内存导致 SSD 磨损，并建议通过量化和关闭其他应用来减少内存使用。一些用户分享了他们在老旧但内存升级的硬件上运行类似模型的经验。

**标签**: `#local LLM`, `#video indexing`, `#Gemma4`, `#memory management`, `#personal archiving`

---

<a id="item-5"></a>
## [谷歌 Antigravity IDE 的诱饵调包策略](https://www.0xsid.com/blog/antigravity-bait-n-switch) ⭐️ 8.0/10

谷歌在一次有争议的更新中，将原本基于 VSCode 的 Antigravity IDE 替换为一个不同的、以智能体为先的平台，这让未得到充分告知的现有用户感到困惑。 这种诱饵调包行为损害了开发者信任，并凸显了谷歌不一致的产品策略，可能促使用户转向 AI 辅助编程市场上更可靠的竞争对手。 原有的 Antigravity 是带有 AI 功能的轻量级 VSCode 重制版，而 2.0 更新将其替换为一个独立的智能体平台，破坏了现有的工作流和集成。

hackernews · ssiddharth · May 21, 13:50 · [社区讨论](https://news.ycombinator.com/item?id=48222529)

**背景**: Google Antigravity 是一个以 AI 为核心的 IDE，专注于智能体开发。所谓的“诱饵调包”是指一次产品更新在未明确沟通的情况下根本性地改变了 IDE 的性质，引发了依赖原工具的用户强烈不满。这种转变损害了用户信任，并反映了谷歌对开发者工具长期投入的糟糕态度。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Antigravity">Google Antigravity - Wikipedia</a></li>
<li><a href="https://antigravity.google/">Google Antigravity</a></li>

</ul>
</details>

**社区讨论**: 用户表达了不满，有人提供了恢复旧功能的方法。其他人批评谷歌缺乏专注，并与其他 AI 实验室进行了不利对比，认为那些实验室保持了更清晰的产品定位。

**标签**: `#Google`, `#Antigravity`, `#IDE`, `#developer tools`, `#bait-and-switch`

---

<a id="item-6"></a>
## [Vivaldi 8.0 发布，带来新功能和改进](https://vivaldi.com/blog/vivaldi-on-desktop-8-0/) ⭐️ 8.0/10

Vivaldi 8.0 桌面版已发布，带来了强化的工作区、不捆绑 AI 等新功能和改进，并进行了一次大版本更新。 作为一款流行的替代浏览器，Vivaldi 8.0 继续吸引注重隐私和自定义的用户，同时其部分闭源模式与可用性优势引发了讨论。 Vivaldi 约 92%的代码来自开源的 Chromium，3%来自 Vivaldi 开源部分，仅 5%（用户界面）为闭源，但可通过 CSS 修改。8.0 版本未加入 AI 功能，这让部分用户感到放心。

hackernews · OuterVale · May 21, 07:21 · [社区讨论](https://news.ycombinator.com/item?id=48219060)

**背景**: Vivaldi 是一款基于 Chromium 的网页浏览器，以高度可定制性和内置功能（如标签页堆叠和工作区）而闻名。它免费使用，但与许多基于 Chromium 的浏览器不同，其用户界面部分闭源，这一点受到开源倡导者的批评。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Vivaldi_(web_browser)">Vivaldi (web browser) - Wikipedia</a></li>
<li><a href="https://vivaldi.com/blog/technology/why-isnt-vivaldi-browser-open-source/">Why isn’t Vivaldi browser open-source? | Vivaldi Browser</a></li>

</ul>
</details>

**社区讨论**: 社区讨论反应不一：有人称赞 Vivaldi 卓越的用户体验（例如工作区可以隐藏标签页直到需要时才显示）和打印功能，也有人担心数据收集或闭源模式，倾向于使用 Brave 或 Firefox 等替代方案。一位长期用户对没有添加 AI 感到欣慰。

**标签**: `#Vivaldi`, `#Browser`, `#Privacy`, `#Open Source`, `#Web Browsers`

---

<a id="item-7"></a>
## [GCC 的 BPF 支持接近与 LLVM 功能对等](https://lwn.net/Articles/1071973/) ⭐️ 8.0/10

在 2026 年 LSFMM+BPF 峰会上，GCC BPF 开发者报告称，2026 年 4 月 30 日发布的 GCC 16.1 现已通过 713 项内核 BPF 自测试中的 601 项，接近与 LLVM 的功能对等。GNU 工具链现在包括对 GCC、binutils、DejaGNU、GNU poke 和 GDB 的 BPF 支持，但某些组件如 GDB 的模拟器已过时。 这一里程碑减少了对 LLVM 用于 BPF 编译的内核依赖，促进了工具链多样性和 Linux 发行版的自由。它还增强了 GNU 工具链在 eBPF 开发中的相关性，而 eBPF 对于现代 Linux 网络、可观测性和安全性至关重要。 GCC 要完全通过内核 BPF 自测试，只需修复一小批问题；多数失败测试有共同的根本原因。GCC 还对 Solana 的 BPF 变体进行了初步支持，该变体包含 64 位乘积、商和余数指令，可能对上游 BPF 有益。

rss · LWN.net · May 21, 14:52

**背景**: BPF（伯克利包过滤器），特别是其扩展版本 eBPF，允许在不更改内核源代码的情况下在 Linux 内核中运行沙箱程序，用于网络、跟踪和安全。迄今为止，LLVM 是 BPF 的主要编译器；GCC 的 BPF 后端旨在提供成熟的替代方案，减少对单一工具链的依赖。LSFMM+BPF 峰会是年度仅限受邀者参加的活动，内核开发者在此讨论存储、文件系统、内存管理和 BPF 主题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Berkeley_Packet_Filter">Berkeley Packet Filter - Wikipedia</a></li>
<li><a href="https://gcc.gnu.org/wiki/BPFBackEnd">BPFBackEnd - GCC Wiki</a></li>
<li><a href="https://events.linuxfoundation.org/lsfmmbpf/">Linux Storage, Filesystem, MM & BPF Summit | LF Events</a></li>

</ul>
</details>

**标签**: `#GCC`, `#BPF`, `#Linux kernel`, `#LLVM`, `#toolchain`

---

<a id="item-8"></a>
## [提议为 Linux 内核添加私有内存节点](https://lwn.net/Articles/1072881/) ⭐️ 8.0/10

Gregory Price 在 2026 年 Linux 存储、文件系统、内存管理和 BPF 峰会上提议将 NUMA 内存节点设为特定进程私有，以限制对设备附加内存（如压缩 RAM）的访问。 该特性将通过防止内核伙伴分配器回退到专用内存设备，使得更高效地利用这些设备（例如加速器、智能网卡），从而可能提升性能和安全性。随着异构内存架构的普及，它解决了日益增长的挑战。 Price 的首选方案是添加 __GFP_PRIVATE 分配标志，允许在私有节点内存不可用时回退到普通 RAM。但他指出，现有内核代码中使用的 for_each_online_node() 循环仍可能意外地从私有节点分配内存，这使得该方法存在脆弱性。

rss · LWN.net · May 21, 13:22

**背景**: NUMA（非统一内存访问）系统根据访问延迟将内存划分为节点；通常，任何进程都可以从任何节点分配内存。像 CXL 内存扩展器或压缩 RAM（zram）这样的设备会附加大型内存池，但内核的伙伴分配器可能将它们视为通用 RAM，导致非预期的使用。私有内存节点将限制分配仅允许明确授权的进程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Non-uniform_memory_access">Non-uniform memory access - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Zram">zram - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: David Hildenbrand 质疑 for_each_online_node() 模式的正确性，John Hubbard 指出代码在编写时是正确的，但世界已经改变了。Kiryl Shutsemau 认为修复有问题的分配模式比添加新标志更好，但 Price 反驳说修复所有此类模式可能需要数年时间。

**标签**: `#Linux kernel`, `#memory management`, `#NUMA`, `#LSFMM+BPF`, `#private memory nodes`

---

<a id="item-9"></a>
## [特斯拉监督版 FSD 在华推出](https://x.com/i/status/2057226337010745348) ⭐️ 8.0/10

特斯拉在 X 平台宣布，其监督版全自动驾驶（FSD）系统现已在中国可用。 这标志着特斯拉自动驾驶技术进入全球最大汽车市场，可能会加速 FSD 在全球的采用。 该公告缺乏技术细节，比如监管批准或与美国版本的功能差异。FSD（监督版）仍需要驾驶员持续关注。

telegram · zaihuapd · May 21, 01:34

**背景**: 特斯拉的全自动驾驶（监督版）是一种先进的驾驶辅助系统，可处理许多驾驶任务，但需要驾驶员保持专注并随时准备接管。它包括在大多数道路上导航、自动泊车和召唤功能。该系统已在北美可用，现正扩展到中国。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Tesla_Autopilot">Tesla Autopilot - Wikipedia</a></li>
<li><a href="https://www.tesla.com/support/fsd">Full Self-Driving (Supervised) | Tesla Support</a></li>

</ul>
</details>

**标签**: `#autonomous driving`, `#Tesla`, `#FSD`, `#China`

---

<a id="item-10"></a>
## [OpenAI 计划最快本周提交 IPO 申请](https://www.wsj.com/tech/ai/openai-is-preparing-to-file-for-an-ipo-very-soon-0ec95af5) ⭐️ 8.0/10

OpenAI 正筹备最早于本周秘密提交 IPO 申请，目标在 9 月上市，并已聘请高盛和摩根士丹利起草招股书。 OpenAI 上市将成为 AI 行业的里程碑事件，标志着领先 AI 公司从私有转向公开市场，可能重塑人工智能领域的投资格局。 该公司最近在与埃隆·马斯克的法律诉讼中胜诉，扫清了上市的一大障碍，但仍面临数据中心高昂成本以及 Anthropic 等竞争对手追赶的挑战。马斯克计划上诉，因此上市时间仍不确定。

telegram · zaihuapd · May 21, 04:08

**背景**: 秘密 IPO 申请允许公司向 SEC 提交注册声明草案而不公开披露，使其能够灵活测试市场反应。Anthropic 由前 OpenAI 员工创立，是 AI 安全领域的核心竞争对手，开发了 Claude 模型系列。OpenAI 的潜在上市正值 AI 军备竞赛激烈、资本开支巨大的时期。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.valuethemarkets.com/education/what-is-a-confidential-ipo-filing">What is a Confidential IPO Filing? | Confidential IPOs</a></li>
<li><a href="https://en.wikipedia.org/wiki/Anthropic">Anthropic - Wikipedia</a></li>

</ul>
</details>

**标签**: `#OpenAI`, `#IPO`, `#AI`, `#Business`

---

<a id="item-11"></a>
## [腾讯发布操作系统级 AI 助手 Marvis](https://finance.sina.com.cn/jjxw/2026-05-21/doc-inhyrmmu5949795.shtml) ⭐️ 8.0/10

5 月 21 日，腾讯正式推出系统级 AI 助手 Marvis，支持 Windows、Mac 和 Android 平台，免费使用且无需邀请码，每日提供 1000 万 Token。 此次发布标志着 AI 深度嵌入操作系统的重大进展，可能改变用户与设备的交互方式。本地隐私模式回应了日益增长的数据安全担忧，有望成为 AI 助手的新标准。 Marvis 内置由主 Agent 统筹六个专项 Agent 并行执行任务的“AI 团队”。隐私模式采用端侧大模型，所有数据处理均在本地完成，断网也可使用。

telegram · zaihuapd · May 21, 10:00

**背景**: AI 中间件作为应用与系统资源之间的抽象层，可实现 AI 的无缝集成。端侧大模型是轻量级模型，在本地设备上运行，提供隐私优势但能力通常弱于云端模型。腾讯 Marvis 结合了这些概念，打造出操作系统级的 AI 助手。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://news.aibase.com/news/28191">Tencent Marvis Launches Officially: System-Level AI Assistant , Six...</a></li>
<li><a href="https://kr-asia.com/pulses/162131">Tencent launches Marvis AI assistant</a></li>
<li><a href="https://grokipedia.com/page/On-device_large_language_model">On-device large language model</a></li>

</ul>
</details>

**标签**: `#AI`, `#Operating System`, `#Tencent`, `#Privacy`, `#Multi-Agent`

---