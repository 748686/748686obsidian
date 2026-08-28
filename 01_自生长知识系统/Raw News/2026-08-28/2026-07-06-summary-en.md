---
layout: default
title: "Horizon Summary: 2026-07-06 (EN)"
date: 2026-07-06
lang: en
---

> From 38 items, 12 important content pieces were selected

---

1. [LingBot-Vision: Masked Boundary Modeling for Self-Supervised Pretraining](#item-1) ⭐️ 9.0/10
2. [Tencent Open-Sources Hy3 Preview: 295B MoE with 256K Context](#item-2) ⭐️ 9.0/10
3. [OpenWrt One: Open-Source Hardware Router with WiFi 7 Successor in Development](#item-3) ⭐️ 8.0/10
4. [Anthropic Discovers a Global Workspace in Language Models](#item-4) ⭐️ 8.0/10
5. [Microsoft Resets Xbox Division Amid Profitability Concerns](#item-5) ⭐️ 8.0/10
6. [Nvidia GPU Debt Backstop Fuels $7T AI Infrastructure Boom](#item-6) ⭐️ 8.0/10
7. [OpenSSH 10.4 released with post-quantum signatures and sandbox hardening](#item-7) ⭐️ 8.0/10
8. [Exploring the Linux Kernel's iomap Layer](#item-8) ⭐️ 8.0/10
9. [TRACE: Open-Source Hierarchical Memory for LLM Agents Achieves 82.5% F1 on EventQA](#item-9) ⭐️ 8.0/10
10. [China to Reduce SCI Publication Incentives to Prevent Tech Leaks](#item-10) ⭐️ 8.0/10
11. [Bilibili Sends Legal Letter to BiliRoaming Open-Source Project](#item-11) ⭐️ 8.0/10
12. [Microsoft EU Filing Shows 40% Profit in Ireland, Only 3% Staff](#item-12) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [LingBot-Vision: Masked Boundary Modeling for Self-Supervised Pretraining](https://www.reddit.com/r/MachineLearning/comments/1up4cjh/lingbotvision_masked_boundary_modeling_for/) ⭐️ 9.0/10

LingBot-Vision introduces masked boundary modeling, where the teacher network generates boundary tokens for the student to reconstruct, achieving a state-of-the-art NYUv2 linear-probe RMSE of 0.296 at 1.1B parameters, outperforming DINOv3-7B's 0.309. This novel self-supervised pretraining method significantly improves depth estimation performance with less data (161M images vs. DINOv3's ~500M), potentially reducing the need for labeled data and large-scale pretraining in computer vision. The method uses a teacher-student framework where boundary tokens are derived from the teacher's own predictions, avoiding external edge detectors; masked regions force reconstruction of boundary-bearing areas. The model comes in four sizes, with weights released under Apache-2.0 license.

reddit · r/MachineLearning · /u/StillThese3747 · Jul 6, 17:37

**Background**: Self-supervised learning aims to learn useful representations from unlabeled data. Masked modeling, like BERT in NLP, predicts masked parts of input. Boundary detection identifies object edges. LingBot-Vision combines these: it masks boundary tokens predicted by the teacher, so the student must learn to reconstruct structural boundaries.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2401.00897">[2401.00897] Masked Modeling for Self-supervised ... - arXiv.org</a></li>

</ul>
</details>

**Discussion**: The Reddit community discusses the evaluation rigor, noting that a 0.013 RMSE difference could be due to probe hyperparameters, and the lack of ablation against hard-masking baselines like ADIOS/AttMask. Some question whether the comparison with DINOv3 is settled, as Gram anchoring is still used.

**Tags**: `#self-supervised learning`, `#computer vision`, `#masked modeling`, `#boundary detection`, `#pretraining`

---

<a id="item-2"></a>
## [Tencent Open-Sources Hy3 Preview: 295B MoE with 256K Context](https://t.me/zaihuapd/42385) ⭐️ 9.0/10

Tencent has released and open-sourced the Hunyuan Hy3 preview, a Mixture-of-Experts (MoE) language model with 295 billion total parameters and 21 billion active parameters, supporting a 256K token context length. This release significantly enriches the open-source LLM ecosystem with a large-scale MoE model focused on complex reasoning and agent tasks, potentially accelerating development in AI-powered coding and scientific applications. The model achieves a 54% reduction in first-token latency for products like CodeBuddy, thanks to deep co-optimization of model architecture and inference framework. It targets enhanced performance in math, science, and code generation.

telegram · zaihuapd · Jul 6, 10:09

**Background**: Mixture-of-Experts (MoE) is an architecture that uses multiple specialized sub-networks (experts) and a router to activate only a subset of parameters per token, enabling large model capacity with lower computational cost. First-token latency is the time it takes for a model to start generating its first output token, critical for real-time interactive applications. Tencent's Hunyuan Hy3 leverages these techniques to balance scale and efficiency.

<details><summary>References</summary>
<ul>
<li><a href="https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mixture-of-experts">A Visual Guide to Mixture of Experts ( MoE )</a></li>
<li><a href="https://www.codeant.ai/blogs/ai-first-token-latency">Why Faster First Tokens Matter More Than Total Response Time</a></li>

</ul>
</details>

**Tags**: `#AI`, `#MoE`, `#open-source`, `#LLM`, `#Tencent`

---

<a id="item-3"></a>
## [OpenWrt One: Open-Source Hardware Router with WiFi 7 Successor in Development](https://openwrt.org/toh/openwrt/one) ⭐️ 8.0/10

OpenWrt One is an open hardware router fully supported by OpenWrt firmware, now available for purchase. The community is already discussing the upcoming OpenWrt Two, which will feature WiFi 7 support. This release represents a milestone for open-source networking hardware, offering a reliable, customizable alternative to commercial routers. The planned WiFi 7 successor indicates ongoing innovation in the OpenWrt ecosystem. Priced at $106 with case and antennas or $84 without, the OpenWrt One includes 1GB RAM, which some users note as limited for data center use. The OpenWrt Two is being developed to support WiFi 7 (802.11be) for higher throughput.

hackernews · peter_d_sherman · Jul 6, 18:23 · [Discussion](https://news.ycombinator.com/item?id=48808482)

**Background**: OpenWrt is a Linux-based open-source firmware for embedded devices like routers, known for extending device life and adding advanced features beyond manufacturer support. WiFi 7 (IEEE 802.11be) is the latest wireless standard offering theoretical speeds up to 23 Gbit/s, with final standard published in July 2025.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/WiFi_7">WiFi 7</a></li>
<li><a href="https://github.com/openwrt/firmware-selector-openwrt-org">GitHub - openwrt/firmware-selector-openwrt-org: The OpenWrt Firmware Selector! Quickly find firmware for your device and build custom ones online! · GitHub</a></li>
<li><a href="https://openwrt.org/toh/views/toh_fwdownload">[OpenWrt Wiki] Table of Hardware: Firmware downloads</a></li>

</ul>
</details>

**Discussion**: Overall sentiment is positive, with users praising the affordable price and open-source nature. Some compare it to alternatives like OPNSense, noting OpenWrt's learning curve and scattered documentation. A user mentions recent purchase, indicating active demand.

**Tags**: `#openwrt`, `#open hardware`, `#router`, `#networking`, `#embedded systems`

---

<a id="item-4"></a>
## [Anthropic Discovers a Global Workspace in Language Models](https://www.anthropic.com/research/global-workspace) ⭐️ 8.0/10

Anthropic researchers have identified a 'global workspace' in large language models (LLMs), where information is integrated across layers, analogous to the Global Neuronal Workspace theory of consciousness. This finding provides a new framework for understanding how LLMs combine information across layers, potentially leading to improved model interpretability and alignment. The work defines a 'J-space' based on the expected change to final logits from perturbations at each layer, revealing a shared subspace across contexts.

hackernews · in-silico · Jul 6, 17:44 · [Discussion](https://news.ycombinator.com/item?id=48808002)

**Background**: Global Workspace Theory (GWT) is a leading scientific account of consciousness, proposing that information becomes globally available for reasoning and action when broadcast across a neural workspace. In transformer-based LLMs, information flows through multiple layers of self-attention and feedforward networks, allowing integration across tokens. This research adapts GWT to artificial neural networks, suggesting a similar integrative mechanism exists in LLMs.

<details><summary>References</summary>
<ul>
<li><a href="https://fmt.matthiasgruber.com/basics/global-neuronal-workspace/">Global Neuronal Workspace Theory - The Standard Model of...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)">Transformer (deep learning architecture)</a></li>
<li><a href="https://www.datacamp.com/tutorial/how-transformers-work">How Transformers Work: A Detailed Exploration of Transformer Architecture | DataCamp</a></li>

</ul>
</details>

**Discussion**: Community comments show mixed reactions: some appreciate the conceptual connection to consciousness, while others (like snaking0776) caution against overstating the analogy, noting that the J-space is more about a shared reasoning subspace. Several commenters recall related experiments, such as duplicating layers to improve math ability, and Neel Nanda's independent replication.

**Tags**: `#AI`, `#language models`, `#interpretability`, `#Anthropic`, `#deep learning`

---

<a id="item-5"></a>
## [Microsoft Resets Xbox Division Amid Profitability Concerns](https://news.xbox.com/en-us/2026/07/06/resetting-xbox/) ⭐️ 8.0/10

Microsoft announced a major reset of its Xbox division, citing thin and non-growing profit margins despite $5 billion in quarterly revenue, leading to layoffs and studio independence. This restructuring signals a strategic shift in Microsoft's gaming approach, potentially affecting the industry's hardware, subscription, and acquisition strategies, and impacting thousands of developers. The reset includes trimming operations to return to growth, with CEO Asha acknowledging corporate management failures and allowing studios to go independent, while Xbox continues to generate significant revenue.

hackernews · dijksterhuis · Jul 6, 14:18 · [Discussion](https://news.ycombinator.com/item?id=48804993)

**Background**: Xbox is Microsoft's gaming division, which has been competing with Sony's PlayStation and Nintendo. Despite high revenue, the division has struggled with profitability due to high costs from acquisitions and Game Pass investments. The reset aims to address these financial challenges.

**Discussion**: Commenters expressed mixed reactions: some see the reset as necessary but blame past leadership, while others criticize Microsoft's inability to manage gaming as an art form. There is sympathy for laid-off workers and skepticism about the return to growth narrative.

**Tags**: `#Xbox`, `#gaming`, `#Microsoft`, `#business strategy`, `#industry analysis`

---

<a id="item-6"></a>
## [Nvidia GPU Debt Backstop Fuels $7T AI Infrastructure Boom](https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes) ⭐️ 8.0/10

Nvidia has launched a debt backstop mechanism that guarantees to rent back unused GPUs at a fixed rate, de-risking loans for neoclouds. This is projected to drive $7 trillion in AI debt by 2029, enabling massive expansion of AI compute capacity. This financial innovation unlocks capital for smaller cloud operators, broadening access to AI compute beyond hyperscalers. It transforms Nvidia from a chip supplier into a financial catalyst for the entire AI infrastructure ecosystem. The backstop works by Nvidia agreeing to repurchase or rent unused GPUs at a predetermined price, making lenders willing to finance GPU clusters. The 'trinity' required for neoclouds includes capital, offtake agreements, and datacenters, with Nvidia's backstop addressing the capital component.

rss · Semianalysis · Jul 6, 21:53

**Background**: Neoclouds are specialized cloud providers focused exclusively on GPU-as-a-Service for AI workloads. An offtake agreement is a long-term commitment by a customer to rent GPU capacity, which lenders require to secure financing. Nvidia's backstop effectively substitutes for an offtake agreement, enabling capital-constrained startups to build large GPU clusters.

<details><summary>References</summary>
<ul>
<li><a href="https://mlq.ai/news/nvidia-launches-gpu-backstop-financing-model-takes-cut-of-cloud-revenue-from-neocloud-partners/">Nvidia Launches GPU Backstop Financing Model, Takes Cut of Cloud Revenue From Neocloud Partners | MLQ News</a></li>
<li><a href="https://www.globaldatacenterhub.com/p/in-ai-infrastructure-the-offtake">In AI Infrastructure, the Offtake Agreement Is the Asset</a></li>

</ul>
</details>

**Tags**: `#AI Infrastructure`, `#Nvidia`, `#Cloud Computing`, `#AI Financing`, `#Debt Markets`

---

<a id="item-7"></a>
## [OpenSSH 10.4 released with post-quantum signatures and sandbox hardening](https://lwn.net/Articles/1081536/) ⭐️ 8.0/10

OpenSSH 10.4 was released, adding experimental support for a composite post-quantum signature scheme combining ML-DSA 44 and Ed25519. Additionally, on Linux, sshd will now refuse to start if SECCOMP or NO_NEW_PRIVS sandbox features are not enabled. This is significant because SSH is a critical infrastructure tool used for secure remote access worldwide; post-quantum signature support future-proofs SSH against potential quantum computer attacks. The stricter sandbox enforcement improves security by ensuring sshd runs in a confined environment, reducing the impact of potential vulnerabilities. The post-quantum signature scheme follows an IETF draft and combines ML-DSA 44 (a NIST-standardized lattice-based algorithm) with Ed25519. On Linux, if sshd is compiled with sandbox support and the system lacks SECCOMP or NO_NEW_PRIVS, the daemon will now fail to start instead of merely logging an error.

rss · LWN.net · Jul 6, 16:13

**Background**: OpenSSH is the most widely used implementation of the SSH protocol for secure remote login and file transfer. Post-quantum cryptography aims to develop cryptographic systems that are secure against both classical and quantum computers; ML-DSA (formerly Dilithium) is a lattice-based digital signature scheme standardized by NIST. SECCOMP (secure computing mode) and NO_NEW_PRIVS are Linux kernel features that help restrict the capabilities of processes, making them essential for sandboxing.

<details><summary>References</summary>
<ul>
<li><a href="https://www.encryptionconsulting.com/ml-dsa-and-pq-signing/">ML-DSA and PQ Signing: What You Need to Know | Encryption Consulting</a></li>
<li><a href="https://en.wikipedia.org/wiki/Seccomp">seccomp - Wikipedia</a></li>
<li><a href="https://www.kernel.org/doc/html/latest/userspace-api/no_new_privs.html">No New Privileges Flag — The Linux Kernel documentation</a></li>

</ul>
</details>

**Tags**: `#security`, `#cryptography`, `#post-quantum`, `#SSH`, `#software release`

---

<a id="item-8"></a>
## [Exploring the Linux Kernel's iomap Layer](https://lwn.net/Articles/1079415/) ⭐️ 8.0/10

Jonathan Corbet published an in-depth article on LWN explaining the iomap layer in the Linux kernel, which handles mapping between filesystem space and storage space, introduced in kernel 4.8 by Christoph Hellwig. This article fills a knowledge gap about a core filesystem component, enabling kernel developers to better understand and use iomap for efficient I/O and reducing boilerplate code in filesystem implementations. The iomap structure uses a single struct to represent large extents, replacing the older buffer-head mechanism, and supports both block devices and DAX persistent memory. It consists of a low-level mapping layer and a higher-level operation layer.

rss · LWN.net · Jul 6, 14:37

**Background**: Before iomap, the Linux kernel used buffer heads to map between disk blocks and memory, which were inefficient for large files and extent-based filesystems. iomap was initially derived from XFS's existing implementation and has since been adopted by many filesystems like ext4 and btrfs for direct I/O. It provides a unified interface for both buffered and direct I/O operations.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.kernel.org/filesystems/iomap/design.html">1. Library Design — The Linux Kernel documentation</a></li>
<li><a href="https://kernelnewbies.org/KernelProjects/iomap">KernelProjects/iomap - Linux Kernel Newbies linux/Documentation/filesystems/iomap/design.rst at master ... iomap: Buffered I/O and Direct I/O Mapping | torvalds/linux ... News [LWN.net] [$] The kernel's iomap layer - Linux.org Filesystems and iomap - LWN.net</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#filesystem`, `#iomap`, `#storage`, `#XFS`

---

<a id="item-9"></a>
## [TRACE: Open-Source Hierarchical Memory for LLM Agents Achieves 82.5% F1 on EventQA](https://www.reddit.com/r/MachineLearning/comments/1uoz5jo/trace_opensource_hierarchical_memory_for_llm/) ⭐️ 8.0/10

TRACE is a new open-source hierarchical memory system that organizes conversation history into a topic tree. It achieved 82.5% F1 on the MemoryAgentBench EventQA task using the gpt-oss-20B model. This work addresses a key limitation in LLM agents—flat memory retrieval—by introducing hierarchical topic trees, leading to significantly better performance than existing methods like Mem0 and MemGPT. The open-source release enables wider adoption and further research. The benchmark comparison is not apples-to-apples because TRACE used gpt-oss-20B while Mem0 and MemGPT used GPT-4o-mini; TRACE’s gpt-oss-120B version achieved 83.8% F1. The author noted issues with running Mem0 on gpt-oss due to JSON parsing constraints.

reddit · r/MachineLearning · /u/PsychologicalDot7749 · Jul 6, 14:35

**Background**: LLM agents require memory systems to retain and retrieve information across long conversations. Traditional approaches use flat retrieval-augmented generation (RAG) that treats all history as equal chunks, which can lose contextual hierarchy. TRACE organizes memory into a topic tree with branches and summaries, allowing agents to navigate historical context more effectively. MemoryAgentBench is a benchmark from ICLR 2026 designed to evaluate memory capabilities in LLM agents.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/pdf/2507.05257">Published as a conference paper at ICLR 2026</a></li>
<li><a href="https://github.com/HUST-AI-HYZ/MemoryAgentBench">GitHub - HUST-AI-HYZ/MemoryAgentBench: Open source code for ICLR 2026 Paper: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions · GitHub</a></li>
<li><a href="https://openai.com/index/introducing-gpt-oss/">Introducing gpt-oss - OpenAI</a></li>

</ul>
</details>

**Tags**: `#LLM agents`, `#hierarchical memory`, `#open-source`, `#benchmark`, `#memory systems`

---

<a id="item-10"></a>
## [China to Reduce SCI Publication Incentives to Prevent Tech Leaks](https://www.ft.com/content/64a811f1-b132-4211-8a8c-2252cf964039?syn-25a6b1a6=1) ⭐️ 8.0/10

Chinese policymakers are discussing reducing incentives for researchers to publish in international journals, including lowering the weight of SCI publications in academic promotion and tenure decisions, citing national security concerns over technology leaks. This shift could reshape China's academic evaluation system, reduce international research collaboration, and impact global scientific publishing by potentially diverting high-quality research to domestic Chinese-language journals. The National Natural Science Foundation of China now requires at least 20% of representative papers from funded projects to be published in Chinese-language journals. A materials scientist reported stopping submissions to foreign journals due to vague and tightening security review standards.

telegram · zaihuapd · Jul 6, 01:03

**Background**: SCI (Science Citation Index) has long been a key metric for academic evaluation in Chinese universities, heavily influencing hiring, promotion, and funding decisions. In recent years, China has strengthened national security reviews of academic publications, especially after a case where a researcher allegedly leaked sensitive data while trying to get published in an international journal.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Science_Citation_Index_Expanded">Science Citation Index Expanded - Wikipedia</a></li>
<li><a href="https://link.springer.com/article/10.1007/s10734-026-01691-5">Shifting dual promotion pressures and research trade-offs ...</a></li>
<li><a href="https://www.sixthtone.com/news/1015445">Up or Out: The Ruthless Tenure Race for Young Chinese Scholars</a></li>

</ul>
</details>

**Discussion**: One community commenter noted that this policy might be intended to combat academic fraud, suggesting that reducing pressure to publish in high-impact international journals could lower incentives for misconduct.

**Tags**: `#China`, `#academic publishing`, `#national security`, `#SCI`, `#research policy`

---

<a id="item-11"></a>
## [Bilibili Sends Legal Letter to BiliRoaming Open-Source Project](https://github.com/yujincheng08/BiliRoaming) ⭐️ 8.0/10

Bilibili sent a legal letter to the BiliRoaming open-source project, demanding it stop reverse engineering its non-public APIs, authentication, and paid content protection mechanisms, and delete or revert related code within 2 days. This rare legal action against a reverse-engineering project highlights the escalating tension between platform protection and open-source modifications; it could set a precedent affecting developers and users who rely on such tools. The letter specifically cites actions like hooking playback authentication, rewriting paid bangumi to be viewable, bypassing secure transmission locks, and modifying CDN origin fallback; BiliRoaming is an Xposed module that unblocks Bilibili's regional restrictions for anime shows.

telegram · zaihuapd · Jul 6, 08:21

**Background**: BiliRoaming is an open-source Xposed module for Android that allows users to bypass Bilibili's regional restrictions on anime content and enables other minor features. Xposed is a framework that lets users modify the behavior of apps on rooted Android devices without altering APK files. Reverse engineering like this often violates a platform's terms of service and may be subject to legal challenges under copyright or anti-circumvention laws.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/yujincheng08/BiliRoaming/releases">Releases · yujincheng08/BiliRoaming - GitHub</a></li>
<li><a href="https://github.com/enyto/biliroaming">GitHub - enyto/biliroaming: 哔哩漫游，解除B站客户端番剧区域限制的...</a></li>
<li><a href="https://sourceforge.net/projects/biliroaming.mirror/">BiliRoaming download | SourceForge.net</a></li>

</ul>
</details>

**Tags**: `#开源`, `#逆向工程`, `#法律`, `#B站`, `#BiliRoaming`

---

<a id="item-12"></a>
## [Microsoft EU Filing Shows 40% Profit in Ireland, Only 3% Staff](https://www.techspot.com/news/113001-microsoft-new-eu-disclosure-shows-exactly-how-tech.html) ⭐️ 8.0/10

Microsoft's latest EU regulatory disclosure reveals that nearly 40% of its global pre-tax profit for the fiscal year ending June 2025 is attributed to Ireland, despite only 3% of its workforce being located there. This highlights the company's ongoing profit shifting to low-tax jurisdictions. This disclosure sheds light on significant corporate tax avoidance practices by Microsoft, with implications for tax policy debates and the effectiveness of EU transparency rules. It may increase pressure on governments to close loopholes and reconsider how multinational profits are taxed. In the filing, Germany's reported profit share was less than 0.5% despite being a major market, while Luxembourg's 34 employees generated $283 million in pre-tax income (a 142% profit margin). Microsoft cites accounting differences and states that tax is not the sole measure of contribution.

telegram · zaihuapd · Jul 6, 09:19

**Background**: Profit shifting is a strategy where multinational companies move profits from high-tax to low-tax jurisdictions, often using internal pricing of intellectual property. The EU's 2021 public country-by-country reporting rules require large companies to disclose revenue and taxes per country, increasing transparency. This disclosure comes as the US IRS seeks $29 billion in back taxes from Microsoft for past profit shifting.

<details><summary>References</summary>
<ul>
<li><a href="https://doorm.ai/跨国公司的税务布局策略/">跨 国 公 司 的 税 务布局 策 略 – Doorm AI</a></li>
<li><a href="https://zh.wikipedia.org/wiki/欧洲联盟">欧 洲联 盟 - 维基百科，自由的百科全书</a></li>

</ul>
</details>

**Tags**: `#Microsoft`, `#tax avoidance`, `#corporate taxation`, `#EU transparency`, `#profit shifting`

---