---
layout: default
title: "Horizon Summary: 2026-04-18 (ZH)"
date: 2026-04-18
lang: zh
---

> From 30 items, 16 important content pieces were selected

---

1. [Shor 算法新实现将攻击 256 位椭圆曲线密码的内存需求降低 20 倍](#item-1) ⭐️ 9.0/10
2. [我国科学家首次人工制造出球状闪电，证实其本质为电磁孤子](#item-2) ⭐️ 9.0/10
3. [《自然》刊发大规模古 DNA 研究：过去万年人类经历广泛定向选择](#item-3) ⭐️ 9.0/10
4. [Anthropic 发布 Claude Design，一款通过提示词生成 UI 设计的 AI 工具](#item-4) ⭐️ 8.0/10
5. [Smol machines 项目发布便携式虚拟机，实现亚秒级冷启动，融合容器易用性与虚拟机隔离性。](#item-5) ⭐️ 8.0/10
6. [360 漏洞挖掘智能体发现两项全球高危漏洞，影响逾 10 亿用户](#item-6) ⭐️ 8.0/10
7. [硅谷精英被指将公共科研科学家转化为低薪 AI 零工](#item-7) ⭐️ 8.0/10
8. [谷歌拟向五角大楼机密环境部署 TPU 芯片，加速 Gemini 在国防领域的落地。](#item-8) ⭐️ 8.0/10
9. [以太坊 ETH Rangers 项目结项：追回 580 万美元并识别百名朝鲜 IT 员工](#item-9) ⭐️ 8.0/10
10. [分析显示 Claude 4.7 分词器导致成本增加 20-45%](#item-10) ⭐️ 7.0/10
11. [Linux 7.0 懒惰抢占调度器变更引发 PostgreSQL 性能回归调查](#item-11) ⭐️ 7.0/10
12. [翻译巨头 DeepL 进军语音领域，推出实时语音翻译套件与 API](#item-12) ⭐️ 7.0/10
13. [Perplexity 发布 Personal Computer 软件，将 Mac 转化为 AI 助手](#item-13) ⭐️ 7.0/10
14. [星链故障中断美海军无人艇测试，暴露五角大楼依赖风险](#item-14) ⭐️ 7.0/10
15. [中国半导体设备厂商 2025 年营收创纪录，美系设备经东南亚转运进口量激增](#item-15) ⭐️ 7.0/10
16. [DeepSeek 拟以 100 亿美元估值融资至少 3 亿美元](#item-16) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Shor 算法新实现将攻击 256 位椭圆曲线密码的内存需求降低 20 倍](https://lwn.net/Articles/1066156/) ⭐️ 9.0/10

2026 年 4 月 17 日，来自谷歌、加州大学伯克利分校、以太坊基金会和斯坦福大学的研究人员发表了一篇论文，提出了一种更高效的 Shor 算法实现，将攻击 256 位椭圆曲线密码所需的内存减少了 20 倍。研究人员发布了一个零知识证明，证明他们拥有实现这些改进的量子电路，但没有公开电路细节。 这一突破显著提高了量子攻击对广泛使用的密码系统（如椭圆曲线密码）的实用性，这些系统保护着许多互联网协议和区块链技术。它突显了后量子密码学采用的时间线正在加速，并强调了在关键基础设施中采用抗量子算法的必要性。 新的量子电路使用少于 1,200 个逻辑量子比特和 9,000 万个量子门，根据架构不同，对应约 50 万个物理量子比特，而 IBM 的 Condor 量子计算机只有 1,121 个物理量子比特。然而，研究人员没有公开具体电路，而是使用了零知识证明，且实际应用仍需要比当前量子计算机多约 500 倍的内存。

rss · LWN.net · Apr 17, 15:53

**背景**: Shor 算法是一种量子算法，能高效分解大数，威胁到 RSA 和椭圆曲线密码等经典密码系统。椭圆曲线密码（ECC）广泛用于安全通信，256 位 ECC 提供约 128 位安全性，但易受 Shor 算法的量子攻击。量子计算机使用量子比特和量子电路，但实际挑战包括噪声和纠错，逻辑量子比特由多个物理量子比特构建以提高可靠性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Elliptic-curve_cryptography">Elliptic-curve cryptography - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Zero-knowledge_proof">Zero-knowledge proof - Wikipedia</a></li>

</ul>
</details>

**标签**: `#quantum-computing`, `#cryptography`, `#algorithms`, `#research`, `#security`

---

<a id="item-2"></a>
## [我国科学家首次人工制造出球状闪电，证实其本质为电磁孤子](https://www.news.cn/tech/20260416/b487a8967b70495f8fc00364844225d6/c.html) ⭐️ 9.0/10

中国科学院上海光学精密机械研究所的研究团队首次在世界上以人工方式成功激发并捕获了与自然界球状闪电高度相似的球形发光体，相关研究成果于 4 月 16 日发表在《自然·光子学》期刊上。该实验证实了球状闪电的本质为电磁孤子，为这一长期缺乏实验验证的科学悬案提供了关键证据。 这一突破揭示了极端电磁能量约束的基础物理机制，为聚变能源及高能量密度物理等领域的研究提供了新参考。这是等离子体物理学理解的重要进展，可能为未来能源技术发展提供重要启示。 研究团队利用强激光驱动太赫兹波在局域实现相对论级场强，将氩气电离为等离子体，通过光波辐射压与热压的力学平衡将能量囚禁，形成直径约百微米、寿命达百纳秒的能量球。经物理标度变换，该能量球可对应自然界中直径数十厘米、持续数秒的球状闪电。

telegram · zaihuapd · Apr 17, 09:00

**背景**: 球状闪电是一种罕见的大气现象，涉及雷暴期间出现的球形发光物体，由于观测数据有限，其本质几个世纪以来一直存在争议。电磁孤子是自增强的波包，在传播过程中保持其形状，这是由于介质中非线性和色散效应之间的平衡所致。太赫兹波位于微波和红外光之间的电磁频谱，相对论级场强指的是足以将带电粒子加速到接近光速的强电场。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Soliton">Soliton - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Terahertz_radiation">Terahertz radiation - Wikipedia</a></li>

</ul>
</details>

**标签**: `#physics`, `#scientific breakthrough`, `#energy research`, `#plasma physics`, `#optics`

---

<a id="item-3"></a>
## [《自然》刊发大规模古 DNA 研究：过去万年人类经历广泛定向选择](https://www.nature.com/articles/s41586-026-10358-1) ⭐️ 9.0/10

哈佛医学院等机构的研究人员在《自然》杂志发表研究，通过对 15,836 个古代西欧亚人基因组（含 10,016 个新样本）的深度分析，证实定向选择在过去一万年间的人类演化中极为普遍。研究发现数百个等位基因受到强烈选择，这些基因频率的变化影响了现代人的复杂性状，具体表现为预测体脂率和精神分裂症患病风险的下降，以及认知表现相关指标的提升。 这项研究挑战了此前认为“有利突变驱动的定向选择在人类近期演化中十分罕见”的传统观点，为理解达尔文自然选择如何塑造人类复杂性状的遗传结构提供了重要证据。这些发现对于理解人类生物学、进化遗传学以及认知和新陈代谢等影响现代人群的性状的遗传基础具有重要意义。 研究团队估算了 970 万个变异位点的选择系数，量化了自然选择对特定遗传变异的作用强度。该研究特别关注西欧亚人群，这可能限制了研究结果对其他地理区域和人群的普适性。

telegram · zaihuapd · Apr 17, 18:00

**背景**: 古 DNA 分析涉及从考古遗骸中提取和测序 DNA，以研究过去人群的遗传变异。在群体遗传学中，选择系数衡量了自然选择相对于群体中最适应类型对特定基因型的作用强度。等位基因频率在繁殖群体中随时间的变化代表了生物进化的基本机制，因为进化过程既依赖于遗传变异性的变化，也依赖于等位基因频率的变化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.researchgate.net/publication/227850816_Ancient_DNA_analysis_of_human_populations">(PDF) Ancient DNA analysis of human populations</a></li>
<li><a href="https://www.britannica.com/science/selection-coefficient">Selection coefficient | Mutation, Natural & Evolution | Britannica</a></li>
<li><a href="https://scienceoxygen.com/how-does-allele-frequency-contribute-to-evolution/">How does allele frequency contribute to evolution?</a></li>

</ul>
</details>

**标签**: `#genetics`, `#evolution`, `#ancient DNA`, `#human biology`, `#scientific research`

---

<a id="item-4"></a>
## [Anthropic 发布 Claude Design，一款通过提示词生成 UI 设计的 AI 工具](https://www.anthropic.com/news/claude-design-anthropic-labs) ⭐️ 8.0/10

Anthropic 发布了 Claude Design，这是一款 AI 驱动的工具，可将文本提示词转换为交互式 UI 原型，与其 Claude Opus 4.7 模型一同推出。该工具被定位为对现有设计平台（如 Canva）的补充，而非直接替代品。 这标志着 Anthropic 从 AI 研究实验室向全栈提供商的重要扩展，直接挑战了 Figma 等成熟设计工具。它可以通过快速可视化想法来加速早期设计工作流程，可能降低非设计人员创建功能原型的门槛。 Claude Design 于 2026 年 4 月 17 日发布，包含 AI 驱动的模板、智能布局系统和调色板生成器等功能。该工具专为需要快速将想法转化为视觉呈现、且不从现有设计平台开始的用户而构建。

hackernews · meetpateltech · Apr 17, 15:04

**背景**: Anthropic 是一家美国 AI 公司，以开发 Claude 系列大语言模型（LLM）而闻名。UI 设计自动化工具利用 AI 从文本描述生成用户界面布局、组件和原型，代表了从手动设计工作向意图驱动生成的转变。Figma 是一个广泛用于 UI/UX 设计的流行协作设计平台。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://venturebeat.com/technology/anthropic-just-launched-claude-design-an-ai-tool-that-turns-prompts-into-prototypes-and-challenges-figma">Anthropic just launched Claude Design, an AI tool that turns prompts into prototypes and challenges Figma | VentureBeat</a></li>
<li><a href="https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/">Anthropic launches Claude Design, a new product for creating quick visuals | TechCrunch</a></li>
<li><a href="https://en.wikipedia.org/wiki/Anthropic">Anthropic - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了不同观点：一些人认为它是一个有用的沟通工具，不会取代专业设计师，而另一些人则担心它可能使设计同质化并贬低原创性。几位评论者指出了它对 Figma 的潜在竞争影响，其中一人观察到其股价在公告发布时下跌。

**标签**: `#AI`, `#UI Design`, `#Anthropic`, `#Productivity Tools`, `#Design Automation`

---

<a id="item-5"></a>
## [Smol machines 项目发布便携式虚拟机，实现亚秒级冷启动，融合容器易用性与虚拟机隔离性。](https://github.com/smol-machines/smolvm) ⭐️ 8.0/10

Smol machines 项目由前 AWS 工程师开发，推出了便携式虚拟机，实现亚秒级冷启动，旨在替代 Docker 容器，融合容器的易用性和虚拟机的强隔离性。该项目采用混合方法，通过精简不必要的 Linux 内核模块来优化启动时间。 这一创新解决了 Docker 和 Firecracker 等现有技术的性能差距，通过在不牺牲安全性的情况下提供更快的启动时间，可能提升云计算和微服务的效率。它可能影响寻求轻量级、隔离环境进行应用部署和扩展的开发者和组织。 该项目包含一个 CLI 工具，可以创建自包含的二进制文件，例如用于 Python 应用，无需使用 pyenv 或 venv 等环境管理器。但根据社区反馈，它目前依赖 Alpine 等特定基础镜像，可能缺少内存或 CPU 热调整等功能。

hackernews · binsquare · Apr 17, 17:18

**背景**: 虚拟机通过模拟完整操作系统提供强隔离性，但与容器相比，通常具有更高的资源开销和更慢的启动时间。Docker 容器轻量且便携，提供高效的资源利用，但隔离性较弱，因为它们共享主机内核。Firecracker 等技术旨在通过提供轻量级虚拟机来弥合这一差距，但它们可能针对 AWS 基础设施等特定用例进行优化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://aws.amazon.com/compare/the-difference-between-docker-vm/">Docker vs VM - Difference Between Application Deployment Technologies - AWS</a></li>
<li><a href="https://medium.com/@ravipatel.it/understanding-virtual-machines-vs-docker-containers-a-technical-comparison-241f370b2076">Understanding Virtual Machines vs Docker Containers: A Technical Comparison | by Ravi Patel | Medium</a></li>
<li><a href="https://www.redhat.com/en/topics/containers/containers-vs-vms">Containers vs. VMs: Similarities, differences, and combined ...</a></li>

</ul>
</details>

**社区讨论**: 社区讨论呈现多样化观点，包括赞扬自包含二进制功能作为 GraalVM Native 的更简单替代方案，询问类似 Singularity 的数字签名安全功能，以及请求自动资源分配和支持 Ubuntu 等更多基础镜像的功能。总体情绪积极，对单客户单后端基础设施等用例表现出兴趣。

**标签**: `#virtualization`, `#containers`, `#performance`, `#open-source`, `#cloud-computing`

---

<a id="item-6"></a>
## [360 漏洞挖掘智能体发现两项全球高危漏洞，影响逾 10 亿用户](https://finance.sina.com.cn/tech/2026-04-17/doc-inhuupth6598363.shtml) ⭐️ 8.0/10

360 集团自主研发的漏洞挖掘智能体近日发现两项潜伏多年的重大安全漏洞，分别为 Windows 内核提权漏洞和 Office 远程代码执行漏洞，目前已上报国家漏洞库并完成修复。这是我国首次公开披露智能体规模化发现基础软件核心漏洞的能力成果。 这一突破展示了 AI 在网络安全中日益重要的作用，推动行业从人工防御转向自动化机器对抗，有望提升全球软件漏洞的威胁检测能力和响应速度。它强调了组织采用 AI 驱动安全工具的必要性，以应对 Windows 和 Office 等关键系统中不断演变的威胁。 这些漏洞影响全球超过 10 亿 Windows 及 Office 用户，波及个人终端、政企办公系统及关键基础设施。该智能体体系目前已累计挖掘近千个漏洞，其中高危漏洞超过 50 项，显示了其在大规模安全审计中的可扩展性和有效性。

telegram · zaihuapd · Apr 17, 05:06

**背景**: 漏洞检测系统使用自动化工具识别软件中的安全缺陷，AI 通过分析代码模式和行为来增强此能力，以发现隐藏问题。Windows 内核提权漏洞允许攻击者获取更高系统权限，可能危及整个系统，而 Office 远程代码执行漏洞则使恶意代码能通过文档远程运行，带来广泛风险。传统网络安全依赖人工分析和基于签名的检测，但像 360 系统这样的 AI 驱动方法旨在自动化和扩展此过程，以实现更快响应。

<details><summary>参考链接</summary>
<ul>
<li><a href="http://news.cnfol.com/chanyejingji/20260417/32150992.shtml">覆盖10亿用户！ 360...</a></li>
<li><a href="https://www.freebuf.com/articles/system/456703.html">Windows 内核 0Day 漏洞遭野外利用提权（CVE-2025-62215） - FreeBuf...</a></li>
<li><a href="https://www.ichunqiu.com/course/58915">Office 远 程 代 码 执 行 漏 洞 _视频教 程 _i春秋_培育数字时 代 的安全感</a></li>

</ul>
</details>

**标签**: `#Cybersecurity`, `#AI`, `#Vulnerability Detection`, `#Windows`, `#Office`

---

<a id="item-7"></a>
## [硅谷精英被指将公共科研科学家转化为低薪 AI 零工](https://www.thenation.com/article/society/ai-silicon-valley-andreesen-thiel-stem/) ⭐️ 8.0/10

硅谷精英，包括彼得·蒂尔和马克·安德里森，被指控游说削减 NSF 和 NIH 等机构的公共科研经费，导致去年超过 1 万名 STEM 博士联邦雇员离职，并迫使大学实验室关闭。这些失业的科学家现在在 Mercor 和 ScaleAI 等平台上从事时薪制的 AI 模型训练工作，尽管处理高难度学术问题，但有效薪酬较低。 这一趋势通过将人才从长期科学探究转向短期商业 AI 项目，威胁公共科研基础，可能削弱 AI 开发的创新和伦理标准。它凸显了科技行业的系统性劳动剥削，高技能研究人员面临不稳定的零工工作，引发了对公平性和 STEM 职业未来的担忧。 像 Mercor 这样的平台提供专业任务，时薪高达 150 美元，但与其他平台相比，薪酬差距可达 30 倍，表明 AI 零工经济中存在显著的工资不平等。经费削减，如 NIH 拟议的 180 亿美元削减，占其预算近 40%，直接影响癌症研究和其他关键领域。

telegram · zaihuapd · Apr 17, 05:51

**背景**: 美国的公共科研经费主要由国家科学基金会（NSF）和国立卫生研究院（NIH）等机构管理，支持 STEM（科学、技术、工程和数学）项目和职业。AI 训练平台，如 Mercor 和 ScaleAI，连接 AI 实验室与领域专家，为模型训练生成高质量数据，常以灵活零工为卖点。对这些机构的预算削减可能导致实验室关闭和失业，迫使研究人员在私营部门寻找替代工作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://gigdrift.io/ai-training-platforms-compared/">AI Training Platforms Compared: Which One Actually Pays... - GigDrift</a></li>
<li><a href="https://www.mercor.com/">Mercor | Defining the future of work</a></li>
<li><a href="https://www.nbcnews.com/science/science-news/trumps-nih-budget-cuts-threaten-research-stirring-panic-rcna191744">Trump's NIH budget cuts threaten ‘entire fields of research ,’ stirring...</a></li>

</ul>
</details>

**标签**: `#AI Ethics`, `#Public Policy`, `#Labor Issues`, `#Silicon Valley`, `#Research Funding`

---

<a id="item-8"></a>
## [谷歌拟向五角大楼机密环境部署 TPU 芯片，加速 Gemini 在国防领域的落地。](https://www.tomshardware.com/tech-industry/artificial-intelligence/google-and-pentagon-in-talks-to-run-tpus-inside-classified-environments) ⭐️ 8.0/10

谷歌正与美国国防部谈判，计划首次在获准的机密环境中部署其自研的 TPU 芯片及 GPU 机架，以支持 Gemini 人工智能模型在大规模机密任务中的运行。拟议的合同条款包含禁止用于国内大规模监控和全自动武器的限制，这与 OpenAI 此前的协议类似。 此举有助于谷歌缩小与 AWS 和微软在机密云市场的差距，预计到 2027 年其国防领域收入可达 20 亿美元。它还突显了先进 AI 硬件在国家安全基础设施中的日益融合，对国防 AI 应用的伦理和战略影响提出了新问题。 谷歌分布式云已获得处理秘密级数据的 IL6 授权，但机密边界内仍缺乏支撑大规模工作负载的基础设施。谷歌公职部门的目标是在 2025 至 2027 年间实现约 60 亿美元的预订额，其中 20 亿美元预计来自国防领域。

telegram · zaihuapd · Apr 17, 15:03

**背景**: TPU 是谷歌自主研发的专用集成电路，专为机器学习工作负载优化，相比传统 GPU 能显著提升性能。DoD IL6 是 FedRAMP 和国防部框架内针对处理秘密级数据的云环境的最高授权，确保严格的安全控制。Gemini 是谷歌最强大的通用基础 AI 模型，具备多模态能力，可用于视觉语言处理和高级推理等任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Tensor_Processing_Unit">Tensor Processing Unit - Wikipedia</a></li>
<li><a href="https://www.schellman.com/blog/federal-compliance/dod-il6-explained">DoD IL6: What It Is and Why It Matters | Schellman</a></li>
<li><a href="https://ai.google.dev/gemini-api/docs">Gemini API | Google AI for Developers</a></li>

</ul>
</details>

**标签**: `#Artificial Intelligence`, `#Defense Technology`, `#Cloud Computing`, `#Hardware`, `#Ethics in AI`

---

<a id="item-9"></a>
## [以太坊 ETH Rangers 项目结项：追回 580 万美元并识别百名朝鲜 IT 员工](https://blog.ethereum.org/2026/04/16/eth-rangers-recap) ⭐️ 8.0/10

以太坊基金会的 ETH Rangers 安全资助计划完成了首期六个月的工作，追回或冻结了 580 万美元资金，处理了 36 起以上事件响应，并报告了 785 项漏洞及客户端错误。该项目识别出约 100 名渗透至 Web3 组织的朝鲜 IT 从业者，涉及约 53 个加密项目，并在 Geth、Besu 等主流执行客户端中发现了 14 个拒绝服务漏洞。 这很重要，因为它展示了去中心化安全倡议在保护以太坊生态系统免受财务损失和复杂威胁（如国家支持的渗透和可能破坏网络稳定性的关键漏洞）方面的有效性。它突显了区块链中主动安全措施对于保护用户资产和维护去中心化技术信任的日益重要性。 该计划涉及 Secureum、The Red Guild 和 SEAL 等顶级安全团队，参与者每人获得 25,000 美元津贴。发现的拒绝服务漏洞可能导致执行客户端节点崩溃或 CPU 异常消耗，如果被利用，可能影响以太坊的网络性能。

telegram · zaihuapd · Apr 17, 15:57

**背景**: ETH Rangers 是以太坊基金会于 2024 年底启动的去中心化安全倡议，旨在加强网络对抗智能合约漏洞利用和社会工程攻击的能力。以太坊执行客户端，如 Geth（用 Go 编写）和 Besu（用 Java 编写），是运行节点以处理以太坊网络上交易和智能合约的软件。Web3 中的拒绝服务漏洞可通过过量请求淹没系统来中断服务，导致崩溃或资源耗尽。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://coinalertnews.com/news/2026/04/17/ethereum-foundation-rangers-security-report">Ethereum Foundation Concludes 'Ethereum Rangers' Security ...</a></li>
<li><a href="https://blog.ethereum.org/2024/12/02/ethrangers-public-goods">The ETH Rangers Program | Ethereum Foundation Blog</a></li>
<li><a href="https://blog.web3labs.com/a-comparison-of-ethereum-clients/">A comparison of Ethereum clients - Web3 Labs Ethereum Clients Comparison: Best Ethereum Client 2024 Besu - Infrastructure Tools - Alchemy Step 3: Installing execution client - CoinCashew Ethereum Clients Comparison: Best Ethereum Client 2024 Ethereum Clients Comparison: Best Ethereum Client 2024 Ethereum Clients Comparison: Best Ethereum Client 2024 Ethereum Clients Comparison: Best Ethereum Client 2024 Execution clients - EthStaker Knowledge Base</a></li>

</ul>
</details>

**标签**: `#Blockchain Security`, `#Ethereum`, `#Cybersecurity`, `#Decentralized Collaboration`, `#Vulnerability Research`

---

<a id="item-10"></a>
## [分析显示 Claude 4.7 分词器导致成本增加 20-45%](https://www.claudecodecamp.com/p/i-measured-claude-4-7-s-new-tokenizer-here-s-what-it-costs-you) ⭐️ 7.0/10

对 Claude Opus 4.7 更新版分词器的技术分析显示，与 4.6 版本相比，其分词数量增加了 1.0-1.45 倍，导致某些工作负载的成本增加 20-45%。分词器的变更还会使之前版本的提示缓存失效，增加了冷启动成本。 这很重要，因为分词成本直接影响 AI 应用的经济性，20-45%的增长可能显著影响规模化使用大语言模型的企业。该分析揭示了在竞争激烈的 AI 领域中，模型性能提升与运营成本之间的权衡关系。 分词器变更不会直接导致缓存失效，但会使冷启动成本更高，因为缓存前缀需要用多出 1.3-1.45 倍的分词重新写入。Anthropic 在 Claude 4.7 中引入了'effort'参数，允许用户在智能水平和分词消耗之间进行权衡。

hackernews · aray07 · Apr 17, 15:29

**背景**: 分词是大语言模型将文本分解为称为分词的小单元进行处理的过程，成本通常按每百万分词计算。Claude 是 Anthropic 的大语言模型系列，其中 Opus 是其能力最强的版本。提示缓存是一种通过重用先前处理的文本前缀来减少分词使用的技术，但在切换不兼容的模型版本时会发生缓存失效。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.claudecodecamp.com/p/i-measured-claude-4-7-s-new-tokenizer-here-s-what-it-costs-you">I Measured Claude 4.7's New Tokenizer. Here's What It Costs You.</a></li>
<li><a href="https://venturebeat.com/technology/anthropic-releases-claude-opus-4-7-narrowly-retaking-lead-for-most-powerful-generally-available-llm">Anthropic releases Claude Opus 4.7, narrowly retaking lead for most powerful generally available LLM | VentureBeat</a></li>
<li><a href="https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7">What's new in Claude Opus 4.7 - Claude API Docs</a></li>

</ul>
</details>

**社区讨论**: 社区评论揭示了关于成本与性能权衡的不同观点，一些用户质疑性能提升是否值得增加的成本，而另一些人则认为对于商业应用来说，AI 成本相比人力成本仍然微不足道。几位评论者指出，实际每任务成本影响可能与简单的分词数量增加不同，建议需要进行更全面的分析。

**标签**: `#AI`, `#Machine Learning`, `#Cost Analysis`, `#LLM`, `#Anthropic`

---

<a id="item-11"></a>
## [Linux 7.0 懒惰抢占调度器变更引发 PostgreSQL 性能回归调查](https://lwn.net/Articles/1067029/) ⭐️ 7.0/10

Linux 内核 7.0 默认启用懒惰抢占调度器模式后，有报告称 PostgreSQL 性能出现 50% 的回归，但调查发现实际情况没有最初报告的那么严重。调查显示，回归是由于 PostgreSQL 的用户空间自旋锁在新的调度器模式下更频繁地被抢占，导致锁争用增加。 这很重要，因为它突显了数据库工作负载对内核调度器变更的敏感性，可能影响许多生产系统。该事件还说明了内核开发者在简化调度器配置的同时，为不同工作负载平衡延迟和吞吐量所面临的持续挑战。 Linux 7.0 中的时间片扩展功能可以通过允许进程在关键部分请求临时抢占保护来缓解此问题，但 PostgreSQL 开发者指出这需要大量代码更改，且对旧内核版本无帮助。懒惰抢占模式会延迟抢占直到任务时间片用完或调度器时钟滴答发生，这与立即响应的完全抢占模式不同。

rss · LWN.net · Apr 17, 13:34

**背景**: CPU 调度器抢占决定了何时将正在运行的进程从 CPU 中移除以允许另一个进程运行，从而在延迟（快速响应）和吞吐量（系统效率）之间取得平衡。Linux 提供了多种抢占模式（如 PREEMPT_NONE、PREEMPT_VOLUNTARY 和实时模式）以适应不同的工作负载，懒惰抢占是一种较新的模式，旨在同时服务于延迟敏感型和吞吐量驱动型应用。PostgreSQL 使用用户空间自旋锁进行并发控制，如果锁持有者在释放锁之前被抢占，可能会导致性能问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lwn.net/Articles/994322/">The long road to lazy preemption - lwn.net</a></li>
<li><a href="https://www.phoronix.com/news/Linux-6.13-Sched-Lazy-Preempt">Lazy Preemption Merged Along With Other Scheduler ... - Phoronix</a></li>
<li><a href="https://en.wikipedia.org/wiki/Preemption_(computing)">Preemption (computing) - Wikipedia</a></li>

</ul>
</details>

**标签**: `#linux-kernel`, `#cpu-scheduler`, `#performance`, `#postgresql`, `#kernel-development`

---

<a id="item-12"></a>
## [翻译巨头 DeepL 进军语音领域，推出实时语音翻译套件与 API](https://techcrunch.com/2026/04/16/deepl-known-for-text-translation-now-wants-to-translate-your-voice/) ⭐️ 7.0/10

4 月 16 日，DeepL 正式推出了实时语音翻译套件 DeepL Voice，支持 Zoom 和 Microsoft Teams 等会议平台，用户可在会议中实时收听翻译音频或查看屏幕字幕。同时，DeepL 发布了相关 API，允许企业将该技术集成至呼叫中心等自定义场景，并支持通过 QR 码快速加入多人的线下或远程群聊翻译。 此举标志着 DeepL 从文本翻译拓展至实时语音翻译领域，有望提升全球商业和远程协作中的沟通效率。它可能加剧与其它 AI 翻译服务的竞争，并推动语音处理技术的创新。 当前系统采用“语音-文本-语音”的转换架构，以平衡翻译延迟与准确度，并计划未来开发端到端的直接语音翻译模型。该技术还具备学习行业术语及专有名词的能力，以提升专业场景下的翻译质量，目前处于早期访问阶段，并开放了企业候补名单申请。

telegram · zaihuapd · Apr 17, 03:04

**背景**: DeepL 是一家德国公司，以其高质量的在线文本翻译服务而闻名，因其准确性和多语言支持而广受欢迎。实时语音翻译通常涉及将语音转换为文本、翻译文本，然后将翻译后的文本合成为目标语言语音，这一过程被称为“语音-文本-语音”转换。端到端的直接语音翻译模型旨在通过直接将语音翻译为语音，无需中间文本步骤，来简化这一过程，从而可能降低延迟和错误传播。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://techcrunch.com/2024/11/13/deepl-launches-deepl-voice-real-time-text-based-translations-from-voices-and-videos/">DeepL launches DeepL Voice, real-time, text-based translations</a></li>
<li><a href="https://arxiv.org/html/2503.04799v1">Direct Speech to Speech Translation: A Review - arXiv.org</a></li>

</ul>
</details>

**标签**: `#AI/ML`, `#Translation Technology`, `#Real-time Systems`, `#API Development`, `#Speech Processing`

---

<a id="item-13"></a>
## [Perplexity 发布 Personal Computer 软件，将 Mac 转化为 AI 助手](https://www.cultofmac.com/news/perplexity-personal-computer) ⭐️ 7.0/10

Perplexity 发布了 Personal Computer 软件，面向 Perplexity Max 订阅者和候补名单用户开放，该软件将 Mac 转化为 AI 助手，能够自主管理 Gmail、Slack 和 Salesforce 等应用中的任务。该系统以目标为导向，将复杂目标分解为子任务，并协调 AI 工具完成工作。 这一发布代表了 AI 生产力工具的重大进步，通过实现跨多个平台的自主任务自动化，可能提升个人和企业用户的效率。它符合将 AI 深度集成到日常工作流程的趋势，提供了更无缝和智能的助手体验。 该软件深度集成于 Mac 应用，可访问本地文件和原生程序，并包含企业功能，如 SOC 2 合规性、审计日志和沙盒执行以增强安全性。然而，由于数据处理依赖云端服务器而非纯本地运行，尽管有用户审批和“一键关闭”等安全机制，隐私安全仍是关注焦点。

telegram · zaihuapd · Apr 17, 03:34

**背景**: Perplexity 是一家 AI 搜索引擎公司，Perplexity Max 是其最高级的订阅层级，提供对最新 AI 模型和文件创建等功能的访问。SOC 2 合规性是软件中数据安全的标准，确保对敏感信息的控制，而沙盒执行则隔离代码以防止 AI 应用中的系统风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.perplexity.ai/help-center/en/articles/11680686-perplexity-max">Perplexity Max | Perplexity Help Center</a></li>
<li><a href="https://www.planetcompliance.com/soc-2/best-soc-2-compliance-software/">The Best SOC 2 Compliance Software & Tools</a></li>
<li><a href="https://blog.cloudflare.com/dynamic-workers/">Sandboxing AI agents, 100x faster</a></li>

</ul>
</details>

**标签**: `#AI`, `#Productivity`, `#Software Release`, `#Mac`, `#Automation`

---

<a id="item-14"></a>
## [星链故障中断美海军无人艇测试，暴露五角大楼依赖风险](https://www.reuters.com/business/media-telecom/starlink-outage-hit-drone-tests-exposing-pentagons-growing-reliance-spacex-2026-04-16/) ⭐️ 7.0/10

内部文件显示，SpaceX 的星链卫星网络故障曾多次导致美国海军无人艇测试中断，包括 2025 年 8 月的一次全球性断网，使 24 艘无人艇在加州海岸失去通信并滞留近一小时。同年 4 月的测试也表明，星链在多设备高负载环境下存在连接瓶颈，难以稳定支撑复杂无人系统操作。 这很重要，因为星链凭借其成本优势和近 1 万颗卫星的规模，已成为美军无人机控制和导弹追踪等任务的关键支撑，其可靠性关乎国家安全。对单一商业供应商的深度依赖可能演变为单点故障，增加了国防基础设施的脆弱性。 故障发生在 2025 年的特定测试中，其中 8 月的事件涉及全球网络中断，同时影响了多艘无人艇。限制包括高负载场景下的连接瓶颈，这对复杂军事系统的稳定运行构成挑战。

telegram · zaihuapd · Apr 17, 04:19

**背景**: 星链是由 SpaceX 运营的卫星互联网星座，由数千颗低地球轨道卫星组成，提供全球宽带覆盖。军用无人机通常依赖 MAVLink 等通信协议进行控制和数据传输，卫星网络是远程操作的核心支撑。单点故障指的是系统中一旦失效就会导致广泛中断的组件，突显了集中依赖的风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.rfwireless-world.com/articles/spacex-starlink-network-architecture">SpaceX Starlink Network Architecture and System Elements | RF</a></li>
<li><a href="https://www.flyeye.io/drone-technology-communication/">Drone Communication Systems - Fly Eye</a></li>
<li><a href="http://scriptorum.imagicity.com/tag/single-point-of-failure/">single point of failure | THE SCRIPTORVM</a></li>

</ul>
</details>

**标签**: `#satellite-communications`, `#military-technology`, `#cybersecurity`, `#spacex`, `#drones`

---

<a id="item-15"></a>
## [中国半导体设备厂商 2025 年营收创纪录，美系设备经东南亚转运进口量激增](https://www.tomshardware.com/tech-industry/chinese-chip-tool-makers-booked-record-2025-revenues) ⭐️ 7.0/10

北方华创、中微公司、盛美上海和拓荆科技等中国半导体设备厂商在 2025 年均创下营收纪录，其中北方华创前三季度营收达 271.4 亿元。同时，中国晶圆厂通过新加坡和马来西亚大量进口美系设备，从这两地的进口额分别增至 57 亿和 34 亿美元，而从美国的直接进口额降至 20 亿美元，为 2017 年以来最低。 这凸显了在地缘政治紧张和美国出口管制背景下，中国本土半导体设备产业的韧性和增长，同时也揭示了全球供应链中的战略规避路径。美国提出的 MATCH 法案可能进一步收紧限制，影响长鑫存储、中芯国际等企业，并重塑半导体领域的国际贸易格局。 尽管营收增长强劲，但受国内市场激烈竞争和价格战影响，本土供应商的利润率正面临下滑压力。应用材料、泛林集团和科磊在 2025 财年的在华销售额合计近 190 亿美元，中国市场营收占比均超过 30%。

telegram · zaihuapd · Apr 17, 10:37

**背景**: 半导体设备用于制造芯片，关键类型包括刻蚀和沉积设备。美国出口管制限制了向中国销售先进半导体设备，以遏制其技术进步，这导致中国增加了对本土生产和替代进口路径的依赖。北方华创和拓荆科技是该领域的主要中国厂商，专注于 PECVD 和 ALD 等设备。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.naura.com/">NAURA - 首页 - 北方华创</a></li>
<li><a href="https://stockpage.10jqka.com.cn/688072/">拓 荆 科 技 (688072)个股资金流向查询_个股行情_同花顺财经</a></li>

</ul>
</details>

**标签**: `#semiconductors`, `#geopolitics`, `#trade`, `#manufacturing`, `#regulations`

---

<a id="item-16"></a>
## [DeepSeek 拟以 100 亿美元估值融资至少 3 亿美元](https://www.reuters.com/world/china/chinas-deepseek-is-raising-funds-10-billion-valuation-information-reports-2026-04-17/) ⭐️ 7.0/10

中国人工智能初创公司 DeepSeek 计划以 100 亿美元估值开展新一轮融资，目标筹集至少 3 亿美元资金。该公司此前曾多次拒绝中国顶级风投及科技巨头的入股邀约，此次融资将支持其开发先进推理模型，应对日益增长的算力与研发资本需求。 此次融资表明投资者对 DeepSeek 在全球 AI 竞争中保持竞争力的信心，尽管面临美国芯片出口管制。100 亿美元的估值使 DeepSeek 成为中国 AI 生态系统中的重要参与者，并展示了中国 AI 公司如何通过低成本模型开发等策略适应地缘政治限制。 DeepSeek 曾利用英伟达高性能芯片完成模型训练，但当前面临美国对先进半导体的出口管制挑战。该公司通过低成本模型策略维持竞争地位，这有助于减轻硬件限制和 AI 开发成本上升的影响。

telegram · zaihuapd · Apr 17, 15:14

**背景**: 先进推理模型是专为复杂思考、问题解决和逻辑分析设计的 AI 系统，代表了超越基本模式识别的 AI 发展关键前沿。美国自 2018 年以来实施的 AI 芯片和半导体出口管制，旨在限制中国获取用于 AI 应用的先进计算硬件。对于面临资源限制的 AI 初创公司而言，低成本模型策略变得尤为重要，因为它们需要在性能提升与不断上升的开发成本之间取得平衡。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.labellerr.com/blog/compare-reasoning-models/">5 Best AI Reasoning Models of 2026: Ranked! - labellerr.com</a></li>
<li><a href="https://en.wikipedia.org/wiki/United_States_export_controls_on_AI_chips_and_semiconductors">United States export controls on AI chips and semiconductors</a></li>
<li><a href="https://stratejos.ai/ai-for-startups-competing-with-limited-resources-in-2026/">AI for Startups: Competing with Limited Resources in 2026</a></li>

</ul>
</details>

**标签**: `#AI`, `#Funding`, `#Startups`, `#China`, `#Chip Restrictions`

---