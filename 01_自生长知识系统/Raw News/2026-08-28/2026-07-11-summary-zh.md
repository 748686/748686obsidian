---
layout: default
title: "Horizon Summary: 2026-07-11 (ZH)"
date: 2026-07-11
lang: zh
---

> 从 29 条内容中筛选出 10 条重要资讯。

---

1. [人形机器人完成全球首例活猪胆囊手术](#item-1) ⭐️ 9.0/10
2. [U-Boot FIT 签名验证发现六项严重漏洞](#item-2) ⭐️ 9.0/10
3. [vLLM v0.25.0 默认启用 Model Runner V2](#item-3) ⭐️ 8.0/10
4. [SGLang v0.5.15 在 Blackwell 上大幅提升 LLM 推理性能](#item-4) ⭐️ 8.0/10
5. [ClickHouse 将 PgBouncer 吞吐量提升至 4 倍](#item-5) ⭐️ 8.0/10
6. [优先使用 SQLite 的 STRICT 表](#item-6) ⭐️ 8.0/10
7. [VultronRetriever 模型登顶 MTEB，存储节省 16 倍](#item-7) ⭐️ 8.0/10
8. [SK 海力士 CEO 预警 2027 年最严重内存短缺](#item-8) ⭐️ 8.0/10
9. [苹果起诉 OpenAI 窃取硬件商业机密](#item-9) ⭐️ 8.0/10
10. [特朗普政府力推英特尔复兴，苹果将采用其芯片](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [人形机器人完成全球首例活猪胆囊手术](https://arstechnica.com/ai/2026/07/humanoid-robots-controlled-by-surgeons-did-world-first-operation-on-live-pigs/) ⭐️ 9.0/10

外科医生远程操控宇树 G1 人形机器人，在活猪上成功完成两例腹腔镜胆囊切除手术，这是首次将通用人形机器人用于活体手术，结果发表在《自然》期刊。 这表明了低成本替代专用手术机器人（如达芬奇系统）的可能性，有望将先进手术服务扩展到偏远地区、战场甚至太空等资源有限的环境，从而推动手术护理的普及。 宇树 G1 基础款售价 13,500 美元，配备灵巧手后约 67,000 美元，远低于专用手术机器人 50 万美元以上的价格。该机器人高 1.5 米，重 27 公斤。

telegram · zaihuapd · 7月11日 02:29

**背景**: 人形机器人旨在模仿人类形态和运动，但很少用于手术。传统手术机器人如达芬奇系统价格昂贵且需要专用硬件。这项研究表明，低成本通用人形机器人可通过远程控制适应精确的手术任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.unitree.com/g1/">Humanoid robot G 1 _ Humanoid Robot ... | Unitree Robotics</a></li>

</ul>
</details>

**标签**: `#robotics`, `#surgery`, `#humanoid robot`, `#medical technology`, `#AI in healthcare`

---

<a id="item-2"></a>
## [U-Boot FIT 签名验证发现六项严重漏洞](https://www.bleepingcomputer.com/news/security/new-u-boot-flaws-could-enable-stealthy-firmware-attacks/) ⭐️ 9.0/10

Binarly 披露了 U-Boot 的 FIT 签名验证代码中的六个漏洞，其中两个可导致任意代码执行，四个可造成拒绝服务。这些漏洞影响自 2013.07 版本以来的 50 多个稳定版本及大量下游分支。 攻击者可在操作系统启动前执行恶意代码，绕过所有安全措施，甚至植入持久性固件恶意软件。对于支持远程固件更新的 BMC 等系统，利用这些漏洞无需物理接触，对嵌入式及服务器生态系统构成严重威胁。 这些漏洞存在于签名验证完成前处理不可信 FIT 镜像的过程中。通过恶意固件更新可实现远程利用；尽管补丁已被 U-Boot 接受，但各硬件厂商需自行集成并分发修复，老旧设备可能永远无法获得更新。

telegram · zaihuapd · 7月11日 08:32

**背景**: U-Boot 是嵌入式系统中广泛使用的开源引导程序。FIT（Flattened Image Tree）是其标准启动镜像打包格式，签名验证用于确保镜像真实性。BMC（基板管理控制器）可远程管理服务器固件更新。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cybersecuritynews.com/u-boot-fit-signature-verification/">Six U-Boot FIT Signature Verification Flaws Enable Code Execution and DoS Attacks</a></li>
<li><a href="https://docs.u-boot.org/en/latest/usage/fit/signature.html">U-Boot FIT Signature Verification — Das U-Boot unknown version documentation</a></li>

</ul>
</details>

**标签**: `#security`, `#vulnerability`, `#u-boot`, `#firmware`, `#bootloader`

---

<a id="item-3"></a>
## [vLLM v0.25.0 默认启用 Model Runner V2](https://github.com/vllm-project/vllm/releases/tag/v0.25.0) ⭐️ 8.0/10

vLLM v0.25.0 将 Model Runner V2 设为所有稠密模型的默认运行路径，移除了旧版 PagedAttention 实现，并使 Transformers 建模后端的性能与原生 vLLM 持平。 此次发布是一次重大的架构改革，简化了代码库，消除了技术债务，并扩展了模型支持，以更高的性能和兼容性惠及 LLM 推理社区。 该版本包含来自 232 位贡献者的 558 次提交，新增了 LLaVA-OneVision-2 和 GLM-5 等模型，并引入了用于工具调用/推理解析的全新流式解析引擎。

github · khluu · 7月11日 20:06

**背景**: vLLM 是一个开源的高吞吐量 LLM 推理引擎。Model Runner V2 采用模块化设计和 GPU 原生内核重建了执行核心，取代了旧的 V1 后端。PagedAttention 曾是一项关键的内存管理优化技术，但已被 V2 的改进所取代。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://vllm.ai/blog/2026-03-24-mrv2">Model Runner V2: A Modular and Faster Core for vLLM | vLLM Blog</a></li>
<li><a href="https://docs.vllm.ai/en/v0.22.1/design/model_runner_v2/">Model Runner V2 Design Document - vLLM</a></li>

</ul>
</details>

**标签**: `#LLM`, `#vLLM`, `#inference`, `#open-source`, `#AI`

---

<a id="item-4"></a>
## [SGLang v0.5.15 在 Blackwell 上大幅提升 LLM 推理性能](https://github.com/sgl-project/sglang/releases/tag/v0.5.15) ⭐️ 8.0/10

SGLang v0.5.15 引入了具有零开销调度的推测解码 V2，实现了端到端每秒 token 数量增加 11%，以及 IndexShare 多 token 预测（MTP），在长上下文场景下将草稿步骤成本降低高达 1.9 倍。此外，在 Blackwell GPU 上使用 NVFP4 量化后的 GLM-5.2 模型，在 8 卡 B300 上每用户每秒 token 数超过 500。 这些优化显著降低了生产环境中 LLM 服务的推理延迟和成本，尤其是在 NVIDIA 最新的 Blackwell 架构上。推测解码和量化方面的性能提升使得像 GLM-5.2、DeepSeek-V4 等大型模型的高吞吐、低延迟服务更加可行。 主要改进包括 Spec V2 的 CUDA 可图化草稿扩展与融合元数据操作、IndexShare MTP 跨步骤复用索引器 top-k、TopK V2 融合 top-k 与页表变换，以及针对 Blackwell 的 GEMM 形状专用 JIT 路由器。该版本还默认启用了可中断 CUDA Graph，并新增了线性注意力内核（KDA/GDN）以支持替代注意力机制。

github · Fridge003 · 7月10日 22:58

**背景**: 推测解码是一种推理优化技术，其中一个小型草稿模型生成多个候选 token，然后一个更大的目标模型并行验证它们，从而降低延迟。NVFP4 是伴随 NVIDIA Blackwell 推出的 4 位浮点格式，通过分层缩放提高超低精度下的准确性。SGLang 是一个面向 LLM 的开源推理引擎，专注于高性能和生产就绪。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/">Introducing NVFP4 for Efficient and Accurate Low-Precision Inference | NVIDIA Technical Blog</a></li>
<li><a href="https://en.wikipedia.org/wiki/Speculative_decoding">Speculative decoding</a></li>
<li><a href="https://verda.com/blog/nvfp4-nvidia-blackwell-intro">NVFP4 Explained: How NVIDIA Blackwell Unlocks Low-Precision Floating Point</a></li>

</ul>
</details>

**标签**: `#SGLang`, `#LLM Inference`, `#GPU Optimization`, `#Speculative Decoding`, `#NVFP4`

---

<a id="item-5"></a>
## [ClickHouse 将 PgBouncer 吞吐量提升至 4 倍](https://clickhouse.com/blog/pgbouncer-clickhouse-managed-postgres) ⭐️ 8.0/10

ClickHouse 发表了一篇博客文章，描述了他们如何通过启用 SO_REUSEPORT 并实现进程间的 peering，将流行的 PostgreSQL 连接池工具 PgBouncer 的吞吐量提升至原来的 4 倍。 PgBouncer 在 PostgreSQL 部署中被广泛使用，这项性能提升将惠及众多依赖其进行连接池管理的用户。所使用的技术也可为其他网络服务的类似优化提供参考。 SO_REUSEPORT 允许多个进程绑定到同一个 TCP 端口，均匀分配传入的连接。Peering 机制将取消请求转发到正确的进程，消除了瓶颈并提高了可扩展性。

hackernews · saisrirampur · 7月11日 15:28 · [社区讨论](https://news.ycombinator.com/item?id=48872874)

**背景**: PgBouncer 是 PostgreSQL 的轻量级连接池工具，通过管理数据库连接来提升性能。传统上它以单进程运行，在多核系统上存在吞吐量瓶颈。SO_REUSEPORT 是一种 Linux 套接字选项，允许多个进程在同一端口上接受连接。PgBouncer 的 Peering 机制使不同进程能够协调并转发取消请求，解决了因取消请求发错进程而导致的问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lwn.net/Articles/542629/">The SO_REUSEPORT socket option [LWN.net]</a></li>
<li><a href="https://medium.com/high-performance-network-programming/performance-optimisation-using-so-reuseport-c0fe4f2d3f88">Performance Optimisation using SO_REUSEPORT | by Marten Gartner | High Performance Network Programming | Medium</a></li>
<li><a href="https://www.pgbouncer.org/config.html">PgBouncer config</a></li>

</ul>
</details>

**社区讨论**: 社区成员推荐了 Odyssey 和 pgdog 等替代方案，并询问了 peering 设置的简便性。其他人分享了在 Kubernetes 或多台机器上运行多个 PgBouncer 进程的经验。

**标签**: `#PostgreSQL`, `#PgBouncer`, `#performance`, `#connection pooling`, `#scalability`

---

<a id="item-6"></a>
## [优先使用 SQLite 的 STRICT 表](https://evanhahn.com/prefer-strict-tables-in-sqlite/) ⭐️ 8.0/10

一篇文章推荐使用 SQLite 3.37.0 版本（2021 年 11 月 27 日）引入的 STRICT 表，以强制数据类型约束，提高数据库可靠性，特别是在多个应用共享同一个数据库时。 这个建议解决了 SQLite 动态类型（dynamic typing）的常见批评，使其在多应用场景中更可靠，并鼓励更安全的数据库实践。它可能会推动 STRICT 表的采用，并可能影响未来的默认设置。 STRICT 表强制执行精确的数据类型，禁止类型强制转换，但不支持 DATE 等某些类型。每个表必须显式声明为 STRICT。

hackernews · ingve · 7月11日 17:33 · [社区讨论](https://news.ycombinator.com/item?id=48873940)

**背景**: SQLite 传统上使用动态类型（灵活类型），列可以存储任何数据类型，无论声明的类型如何，这可能导致意外的类型不匹配。自 SQLite 3.37.0 起可用的 STRICT 表改变了这一点，它强制进行严格的类型检查，确保插入的数据与声明的列类型匹配。当数据库被多个应用共享或需要更强的类型安全时，这尤其有益。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.sqlite.org/stricttables.html">STRICT Tables</a></li>
<li><a href="https://www.sqlitetutorial.net/sqlite-strict-tables/">SQLite Strict Tables</a></li>

</ul>
</details>

**社区讨论**: 评论普遍欢迎这一功能，一些用户希望 STRICT 成为默认设置。担忧包括缺少 DATE 等数据类型，以及关于 SQLite 作为嵌入式数据库与共享数据库的不同用例的辩论。讨论反映了对更强类型安全的渴望，同时也承认 SQLite 的灵活性。

**标签**: `#SQLite`, `#databases`, `#type safety`, `#software engineering`

---

<a id="item-7"></a>
## [VultronRetriever 模型登顶 MTEB，存储节省 16 倍](https://www.reddit.com/r/MachineLearning/comments/1utmxq8/vultronretriever_family_of_models_released_on/) ⭐️ 8.0/10

VultronRetriever 模型家族已在 HuggingFace 发布，在 MTEB 排行榜上取得第一名，索引存储缩小达 16 倍，吞吐量提高 12 倍，超越之前的 9B 级领先模型。 这一突破使得在 iPhone 等边缘设备上完全离线进行高质量检索和嵌入成为可能，将 AI 应用扩展到隐私敏感和资源受限的环境，同时降低基础设施成本。 该系列包括三个模型：Prime-8B（全球第一）、Core-4.5B（性能超越其两倍大小的模型）和 Flash-0.8B（性能超越其五倍大小的模型）。所有模型均在无污染数据集上训练，采用 Hydra 架构实现延迟交互检索，内存占用仅为同类模型的一半。

reddit · r/MachineLearning · /u/madkimchi · 7月11日 15:22

**背景**: MTEB 是一个全面的嵌入模型基准，涵盖检索、分类和聚类等任务。Hydra 架构将晚期交互检索（类似于 ColBERT）和自回归生成统一到单个视觉语言模型中，提高了效率并减少了内存占用。VultronRetriever 模型针对视觉文档检索进行了优化，支持在边缘设备上进行离线问答和文档索引。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blogs.vultr.com/vultronretriever">VultronRetriever : Open Visual Document Retrieval Models Built for...</a></li>
<li><a href="https://huggingface.co/vultr/VultronRetrieverCore-Qwen3.5-4.5B">vultr/VultronRetrieverCore-Qwen3.5-4.5B · Hugging Face</a></li>

</ul>
</details>

**标签**: `#Information Retrieval`, `#Embedding Models`, `#HuggingFace`, `#Edge AI`, `#MTEB`

---

<a id="item-8"></a>
## [SK 海力士 CEO 预警 2027 年最严重内存短缺](https://www.reuters.com/world/asia-pacific/sk-hynix-ceo-sees-worst-ever-memory-supply-shortage-2027-says-demand-outstrip-2026-07-10/) ⭐️ 8.0/10

SK 海力士 CEO 郭鲁正警告称，2027 年全球内存行业将面临史上最严重的供应短缺，即使扩产，2030 年后客户需求仍将超过供应能力。该预警发布于公司在纳斯达克上市首日，当日股价收涨 13.3%至 168.85 美元。 作为主要内存制造商，SK 海力士的这一预测表明 AI 和计算需求将导致内存长期供应紧张，可能推高硬件成本并影响整个科技行业。该预警对供应链规划具有重要参考价值。 SK 海力士 2025 年营业利润创纪录达 47 万亿韩元（约 310 亿美元），2026 年第二季度预计进一步增至 65.5 万亿韩元。公司正考虑在美国、日本或东南亚建设海外晶圆厂，优先选择土地、电力和人力成本最具优势的地区。

telegram · zaihuapd · 7月11日 00:45

**背景**: 内存芯片包括 DRAM 和 NAND 闪存，是计算机和电子设备的关键部件。晶圆厂是半导体制造工厂，在硅晶圆上制造电路后切割成独立芯片。随着人工智能和云计算需求爆发，新建晶圆厂需要数年时间，导致供需失衡；CEO 警告这种失衡可能在 2027 年达到顶峰。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://m.elecfans.com/article/253435.html">晶 圆 _ 晶 圆 是 什 么 -电子发烧友网</a></li>
<li><a href="https://today.line.me/tw/v3/article/Gg53n35">AI熱潮引發記憶體短缺！ 三星與 SK ... | LINE TODAY</a></li>

</ul>
</details>

**标签**: `#memory shortage`, `#semiconductor industry`, `#SK Hynix`, `#hardware`, `#supply chain`

---

<a id="item-9"></a>
## [苹果起诉 OpenAI 窃取硬件商业机密](https://www.cnbc.com/2026/07/10/apple-openai-lawsuit-trade-secrets.html) ⭐️ 8.0/10

苹果于 2026 年 7 月 10 日在美国加州北区联邦法院起诉 OpenAI、两名前员工及 io Products，指控其系统性窃取苹果的产品设计、制造工艺及供应链机密，以加快消费级硬件业务发展。 此案可能为 AI 公司如何与科技巨头在硬件领域竞争树立重要先例，并可能影响 OpenAI 的硬件计划及整个行业的知识产权保护方式。 苹果指控前员工刘畅离职后仍下载数十份硬件文件，硬件负责人陈友堂将供应商信息发送至个人邮箱，并鼓励求职者携带苹果零件参加面试。苹果还称目前有超过 400 名前员工在 OpenAI 工作。

telegram · zaihuapd · 7月11日 03:14

**背景**: OpenAI 正拓展消费硬件业务，据报道开发智能音箱等 AI 驱动设备。苹果声称 OpenAI 的硬件业务建立在窃取的商业机密之上，包括未发布产品的设计和制造工艺。由苹果前设计总监 Jony Ive 联合创立的 io Products 也被列为被告。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.macrumors.com/2026/07/10/apple-sues-openai/">Apple Sues OpenAI for Stealing Trade Secrets to Build AI Hardware</a></li>
<li><a href="https://www.engadget.com/2212759/apple-calls-openais-hardware-business-rotten-to-its-core-in-trade-secret-theft-lawsuit/">Apple Calls OpenAI 's Hardware Business 'Rotten To Its Core' In...</a></li>
<li><a href="https://fortune.com/2026/07/10/apple-openai-lawsuit-trade-secrets-theft-allegations/">Apple accuses OpenAI, and former design star Jony Ive's io Products firm, of stealing hardware trade secrets in blockbuster lawsuit | Fortune</a></li>

</ul>
</details>

**标签**: `#Apple`, `#OpenAI`, `#lawsuit`, `#trade secrets`, `#AI hardware`

---

<a id="item-10"></a>
## [特朗普政府力推英特尔复兴，苹果将采用其芯片](https://www.wsj.com/tech/the-white-house-intel-trump-apple-84fe833e) ⭐️ 8.0/10

苹果已同意在其部分芯片中使用英特尔的制造工厂，这是在特朗普政府的施压下实现的。美国政府将 90 亿美元的联邦拨款转为英特尔 10%的股份，成为其最大股东，并促成了英伟达和 SpaceX 等公司与英特尔签约。 这标志着政府对半导体产业的重大干预，可能重塑全球芯片制造格局，增强美国供应链韧性。在中美地缘政治紧张背景下，重振国内芯片生产具有战略意义。 这 90 亿美元的资金来自《芯片与科学法案》，英特尔新任 CEO 陈立武每月与商务部官员会面。自 2025 年 3 月以来，英特尔股价翻了三倍，其代工服务已获得英伟达和 SpaceX 等重要客户。

telegram · zaihuapd · 7月11日 05:54

**背景**: 2022 年的《芯片与科学法案》拨款 527 亿美元用于提升国内半导体制造和研究。英特尔曾是主导芯片制造商，但在先进制造上落后于台积电。其代工服务部门于 2021 年成立，旨在向外部客户提供英特尔的制造技术。特朗普政府的行动延续了两党保障美国芯片供应链的努力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Intel_Foundry_Services">Intel Foundry Services</a></li>
<li><a href="https://en.wikipedia.org/wiki/CHIPS_Act">CHIPS Act</a></li>

</ul>
</details>

**标签**: `#半导体`, `#产业政策`, `#英特尔`, `#苹果`, `#地缘政治`

---