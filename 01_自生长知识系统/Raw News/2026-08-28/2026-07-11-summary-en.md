---
layout: default
title: "Horizon Summary: 2026-07-11 (EN)"
date: 2026-07-11
lang: en
---

> From 29 items, 10 important content pieces were selected

---

1. [Humanoid robot performs world's first live pig gallbladder surgery](#item-1) ⭐️ 9.0/10
2. [Six Critical U-Boot FIT Signature Verification Vulnerabilities Discovered](#item-2) ⭐️ 9.0/10
3. [vLLM v0.25.0 ships Model Runner V2 as default](#item-3) ⭐️ 8.0/10
4. [SGLang v0.5.15 Boosts LLM Inference on Blackwell](#item-4) ⭐️ 8.0/10
5. [ClickHouse scales PgBouncer to 4x throughput](#item-5) ⭐️ 8.0/10
6. [Prefer STRICT Tables in SQLite](#item-6) ⭐️ 8.0/10
7. [VultronRetriever models top MTEB, cut storage 16x](#item-7) ⭐️ 8.0/10
8. [SK Hynix CEO warns of worst memory shortage by 2027](#item-8) ⭐️ 8.0/10
9. [Apple Sues OpenAI for Stealing Trade Secrets for Hardware](#item-9) ⭐️ 8.0/10
10. [Trump Administration Drives Intel Revival, Apple to Use Chips](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Humanoid robot performs world's first live pig gallbladder surgery](https://arstechnica.com/ai/2026/07/humanoid-robots-controlled-by-surgeons-did-world-first-operation-on-live-pigs/) ⭐️ 9.0/10

Surgeons remotely controlled a Unitree G1 humanoid robot to perform two laparoscopic gallbladder removal surgeries on live pigs, marking the first use of a general-purpose humanoid robot for live surgery. The results were published in Nature. This demonstrates a low-cost alternative to specialized surgical robots like the da Vinci system, potentially expanding access to remote and resource-limited settings such as rural areas, battlefields, or space. It could democratize advanced surgical care. The Unitree G1 base model costs $13,500, and with dexterous hands it costs about $67,000, far less than the $500,000+ for dedicated surgical robots. The robot is 1.5m tall and weighs 27kg.

telegram · zaihuapd · Jul 11, 02:29

**Background**: Humanoid robots are designed to mimic human form and movement, but are rarely used in surgery. Traditional surgical robots like the da Vinci system are expensive and require dedicated hardware. This research shows that a low-cost, general-purpose humanoid robot can be adapted for precise surgical tasks via remote control.

<details><summary>References</summary>
<ul>
<li><a href="https://www.unitree.com/g1/">Humanoid robot G 1 _ Humanoid Robot ... | Unitree Robotics</a></li>

</ul>
</details>

**Tags**: `#robotics`, `#surgery`, `#humanoid robot`, `#medical technology`, `#AI in healthcare`

---

<a id="item-2"></a>
## [Six Critical U-Boot FIT Signature Verification Vulnerabilities Discovered](https://www.bleepingcomputer.com/news/security/new-u-boot-flaws-could-enable-stealthy-firmware-attacks/) ⭐️ 9.0/10

Binarly disclosed six vulnerabilities in U-Boot's FIT signature verification code, two enabling arbitrary code execution and four causing denial of service. The flaws affect over 50 stable versions dating back to 2013.07 and numerous downstream branches. Attackers can execute malicious code before the operating system boots, bypassing all security measures and potentially installing persistent firmware malware. For systems with remote firmware update capabilities like BMCs, exploitation requires no physical access, posing a severe threat to embedded and server ecosystems. The vulnerabilities reside in how untrusted FIT images are processed before signature validation completes. Remote exploitation is possible via malicious firmware updates, and while patches have been accepted into U-Boot, each hardware vendor must integrate and distribute them—legacy devices may never receive fixes.

telegram · zaihuapd · Jul 11, 08:32

**Background**: U-Boot is a widely used open-source bootloader for embedded systems. FIT (Flattened Image Tree) is its standard packaging format for boot images, and signature verification ensures image authenticity. BMCs (Baseboard Management Controllers) manage server firmware updates remotely.

<details><summary>References</summary>
<ul>
<li><a href="https://cybersecuritynews.com/u-boot-fit-signature-verification/">Six U-Boot FIT Signature Verification Flaws Enable Code Execution and DoS Attacks</a></li>
<li><a href="https://docs.u-boot.org/en/latest/usage/fit/signature.html">U-Boot FIT Signature Verification — Das U-Boot unknown version documentation</a></li>

</ul>
</details>

**Tags**: `#security`, `#vulnerability`, `#u-boot`, `#firmware`, `#bootloader`

---

<a id="item-3"></a>
## [vLLM v0.25.0 ships Model Runner V2 as default](https://github.com/vllm-project/vllm/releases/tag/v0.25.0) ⭐️ 8.0/10

vLLM v0.25.0 makes Model Runner V2 the default for all dense models, removes the legacy PagedAttention implementation, and achieves performance parity between the Transformers modeling backend and native vLLM. This release is a major architectural overhaul that simplifies the codebase, eliminates technical debt, and broadens model support, benefiting the LLM inference community with improved performance and compatibility. The release includes 558 commits from 232 contributors, adds new models like LLaVA-OneVision-2 and GLM-5, and introduces a new Streaming Parser Engine for tool-call/reasoning parsing.

github · khluu · Jul 11, 20:06

**Background**: vLLM is an open-source high-throughput LLM inference engine. Model Runner V2 rebuilds the execution core with modular design and GPU-native kernels, replacing the older V1 backend. PagedAttention was a key optimization for memory management but has been superseded by V2's improvements.

<details><summary>References</summary>
<ul>
<li><a href="https://vllm.ai/blog/2026-03-24-mrv2">Model Runner V2: A Modular and Faster Core for vLLM | vLLM Blog</a></li>
<li><a href="https://docs.vllm.ai/en/v0.22.1/design/model_runner_v2/">Model Runner V2 Design Document - vLLM</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#vLLM`, `#inference`, `#open-source`, `#AI`

---

<a id="item-4"></a>
## [SGLang v0.5.15 Boosts LLM Inference on Blackwell](https://github.com/sgl-project/sglang/releases/tag/v0.5.15) ⭐️ 8.0/10

SGLang v0.5.15 introduces Speculative Decoding V2 with zero-overhead scheduling, achieving +11% end-to-end tokens per second, and IndexShare Multi-Token Prediction (MTP) that reduces draft-step cost by up to 1.9x on long contexts. Additionally, GLM-5.2 with NVFP4 quantization on Blackwell GPUs now serves over 500 tokens per second per user on 8x B300. These optimizations significantly reduce inference latency and cost for production LLM serving, especially on NVIDIA's latest Blackwell architecture. The performance gains in speculative decoding and quantization make high-throughput, low-latency serving more accessible for large models like GLM-5.2, DeepSeek-V4, and others. Key improvements include Spec V2's CUDA-graphable draft-extend with fused metadata ops, IndexShare MTP reusing indexer top-k across steps, TopK V2 fusing top-k with page-table transform, and GEMM shape-specialized JIT routers for Blackwell. The release also enables breakable CUDA Graph by default and adds linear-attention kernels (KDA/GDN) for alternative attention mechanisms.

github · Fridge003 · Jul 10, 22:58

**Background**: Speculative decoding is an inference optimization where a smaller draft model generates multiple candidate tokens, and a larger target model verifies them in parallel, reducing latency. NVFP4 is a 4-bit floating-point format introduced with NVIDIA Blackwell that uses hierarchical scaling for improved accuracy at ultra-low precision. SGLang is an open-source inference engine for LLMs that focuses on high performance and production readiness.

<details><summary>References</summary>
<ul>
<li><a href="https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/">Introducing NVFP4 for Efficient and Accurate Low-Precision Inference | NVIDIA Technical Blog</a></li>
<li><a href="https://en.wikipedia.org/wiki/Speculative_decoding">Speculative decoding</a></li>
<li><a href="https://verda.com/blog/nvfp4-nvidia-blackwell-intro">NVFP4 Explained: How NVIDIA Blackwell Unlocks Low-Precision Floating Point</a></li>

</ul>
</details>

**Tags**: `#SGLang`, `#LLM Inference`, `#GPU Optimization`, `#Speculative Decoding`, `#NVFP4`

---

<a id="item-5"></a>
## [ClickHouse scales PgBouncer to 4x throughput](https://clickhouse.com/blog/pgbouncer-clickhouse-managed-postgres) ⭐️ 8.0/10

ClickHouse published a blog post describing how they scaled PgBouncer, a popular PostgreSQL connection pooler, to 4x its original throughput by enabling SO_REUSEPORT and implementing peering between processes. PgBouncer is widely used in PostgreSQL deployments, and this performance improvement benefits many users who rely on it for connection pooling. The techniques used can inspire similar optimizations in other network services. SO_REUSEPORT allows multiple processes to bind to the same TCP port, distributing incoming connections evenly. Peering forwards cancellation requests to the correct process, eliminating bottlenecks and improving scalability.

hackernews · saisrirampur · Jul 11, 15:28 · [Discussion](https://news.ycombinator.com/item?id=48872874)

**Background**: PgBouncer is a lightweight connection pooler for PostgreSQL that manages database connections to improve performance. Traditionally, it runs as a single process, limiting throughput on multi-core systems. SO_REUSEPORT is a Linux socket option that enables multiple processes to accept connections on the same port. Peering in PgBouncer allows separate processes to coordinate and forward cancellation requests, which historically caused issues when a cancellation landed on the wrong process.

<details><summary>References</summary>
<ul>
<li><a href="https://lwn.net/Articles/542629/">The SO_REUSEPORT socket option [LWN.net]</a></li>
<li><a href="https://medium.com/high-performance-network-programming/performance-optimisation-using-so-reuseport-c0fe4f2d3f88">Performance Optimisation using SO_REUSEPORT | by Marten Gartner | High Performance Network Programming | Medium</a></li>
<li><a href="https://www.pgbouncer.org/config.html">PgBouncer config</a></li>

</ul>
</details>

**Discussion**: Community members suggested alternatives like Odyssey and pgdog, and asked about the simplicity of setting up peering. Others shared experiences running multiple PgBouncer processes on Kubernetes or in multi-machine setups.

**Tags**: `#PostgreSQL`, `#PgBouncer`, `#performance`, `#connection pooling`, `#scalability`

---

<a id="item-6"></a>
## [Prefer STRICT Tables in SQLite](https://evanhahn.com/prefer-strict-tables-in-sqlite/) ⭐️ 8.0/10

An article recommends using STRICT tables in SQLite, introduced in version 3.37.0 (2021-11-27), to enforce data type constraints and improve database reliability, especially when multiple applications share the same database. This tip addresses a common criticism of SQLite's dynamic typing, making it more robust for multi-application scenarios and encouraging safer database practices. It could drive adoption of STRICT tables and potentially influence future defaults. STRICT tables enforce exact data types and disallow type coercion, but they do not support some types like DATE. Each table must be explicitly declared as STRICT.

hackernews · ingve · Jul 11, 17:33 · [Discussion](https://news.ycombinator.com/item?id=48873940)

**Background**: SQLite traditionally uses dynamic typing (flexible typing), where columns can store any data type regardless of the declared type, which can lead to accidental type mismatches. STRICT tables, available since SQLite 3.37.0, change this by enforcing strict type checking, ensuring that inserted data matches the declared column type. This is particularly beneficial when a database is shared across multiple applications or when stronger type safety is desired.

<details><summary>References</summary>
<ul>
<li><a href="https://www.sqlite.org/stricttables.html">STRICT Tables</a></li>
<li><a href="https://www.sqlitetutorial.net/sqlite-strict-tables/">SQLite Strict Tables</a></li>

</ul>
</details>

**Discussion**: Comments generally welcome the feature, with some users wishing STRICT were the default. Concerns include missing data types like DATE and debates about SQLite's use case as an embedded database versus shared databases. The discussion reflects a desire for more type safety while acknowledging SQLite's flexibility.

**Tags**: `#SQLite`, `#databases`, `#type safety`, `#software engineering`

---

<a id="item-7"></a>
## [VultronRetriever models top MTEB, cut storage 16x](https://www.reddit.com/r/MachineLearning/comments/1utmxq8/vultronretriever_family_of_models_released_on/) ⭐️ 8.0/10

The VultronRetriever family of models has been released on HuggingFace, achieving #1 on the MTEB leaderboard with up to 16x smaller index storage and 12x higher throughput compared to previous 9B-class leaders. This breakthrough enables high-quality retrieval and embedding on edge devices like iPhones entirely offline, expanding AI applications to privacy-sensitive and resource-constrained environments while reducing infrastructure costs. The family includes three models: Prime-8B (global #1), Core-4.5B (outperforming models twice its size), and Flash-0.8B (outperforming models up to 5x its size). All models are trained on contamination-free datasets and leverage the Hydra architecture for late interaction retrieval with up to half the memory of comparable models.

reddit · r/MachineLearning · /u/madkimchi · Jul 11, 15:22

**Background**: MTEB is a comprehensive benchmark for embedding models, covering tasks like retrieval, classification, and clustering. The Hydra architecture unifies late interaction retrieval (similar to ColBERT) and autoregressive generation in a single vision-language model, improving efficiency and reducing memory footprint. The VultronRetriever models are optimized for visual document retrieval, enabling offline Q&A and document indexing on edge devices.

<details><summary>References</summary>
<ul>
<li><a href="https://blogs.vultr.com/vultronretriever">VultronRetriever : Open Visual Document Retrieval Models Built for...</a></li>
<li><a href="https://huggingface.co/vultr/VultronRetrieverCore-Qwen3.5-4.5B">vultr/VultronRetrieverCore-Qwen3.5-4.5B · Hugging Face</a></li>

</ul>
</details>

**Tags**: `#Information Retrieval`, `#Embedding Models`, `#HuggingFace`, `#Edge AI`, `#MTEB`

---

<a id="item-8"></a>
## [SK Hynix CEO warns of worst memory shortage by 2027](https://www.reuters.com/world/asia-pacific/sk-hynix-ceo-sees-worst-ever-memory-supply-shortage-2027-says-demand-outstrip-2026-07-10/) ⭐️ 8.0/10

SK Hynix CEO Kwak Noh-Jung warned that the global memory industry will face the worst supply shortage in history by 2027, with demand outstripping supply even after capacity expansion beyond 2030. The warning came on the company's Nasdaq debut day, where shares closed up 13.3% at $168.85. This forecast from a major memory maker signals that AI and computing demand will drive long-term memory tightness, potentially raising hardware costs and impacting the entire tech industry. As a leading player, SK Hynix's outlook carries significant weight for supply chain planning. SK Hynix reported a record operating profit of 47 trillion won ($31 billion) in 2025, with Q2 2026 expected to rise further to 65.5 trillion won. The company is considering overseas fab locations in the US, Japan, or Southeast Asia, prioritizing regions with cost advantages in land, power, and labor.

telegram · zaihuapd · Jul 11, 00:45

**Background**: Memory chips, including DRAM and NAND flash, are critical components in computers and electronic devices. Fabs (fabrication plants) produce these chips on silicon wafers, which are then cut into individual dies. With surging demand from AI and cloud computing, new fab construction takes years, leading to potential supply-demand imbalances that the CEO warns could peak in 2027.

<details><summary>References</summary>
<ul>
<li><a href="https://m.elecfans.com/article/253435.html">晶 圆 _ 晶 圆 是 什 么 -电子发烧友网</a></li>
<li><a href="https://today.line.me/tw/v3/article/Gg53n35">AI熱潮引發記憶體短缺！ 三星與 SK ... | LINE TODAY</a></li>

</ul>
</details>

**Tags**: `#memory shortage`, `#semiconductor industry`, `#SK Hynix`, `#hardware`, `#supply chain`

---

<a id="item-9"></a>
## [Apple Sues OpenAI for Stealing Trade Secrets for Hardware](https://www.cnbc.com/2026/07/10/apple-openai-lawsuit-trade-secrets.html) ⭐️ 8.0/10

Apple filed a lawsuit on July 10, 2026, in the U.S. District Court for the Northern District of California against OpenAI, two former employees, and io Products, accusing them of systematically stealing trade secrets related to product design, manufacturing processes, and supply chain to accelerate OpenAI's consumer hardware business. This lawsuit could set a significant precedent for how AI companies compete with established tech giants in hardware, potentially impacting OpenAI's hardware ambitions and the broader industry's approach to intellectual property protection. Apple alleges former employee Chang Liu downloaded dozens of hardware files after leaving the company, and hardware head Tang Yew Tan sent supplier information to his personal email and encouraged job candidates to bring Apple parts to interviews. Apple also claims over 400 former employees now work at OpenAI.

telegram · zaihuapd · Jul 11, 03:14

**Background**: OpenAI has been expanding into consumer hardware, reportedly developing smart speakers and other AI-powered devices. Apple claims OpenAI's hardware business is built on misappropriated trade secrets, including unreleased product designs and manufacturing processes. Io Products, co-founded by former Apple design chief Jony Ive, is also named as a defendant in the lawsuit.

<details><summary>References</summary>
<ul>
<li><a href="https://www.macrumors.com/2026/07/10/apple-sues-openai/">Apple Sues OpenAI for Stealing Trade Secrets to Build AI Hardware</a></li>
<li><a href="https://www.engadget.com/2212759/apple-calls-openais-hardware-business-rotten-to-its-core-in-trade-secret-theft-lawsuit/">Apple Calls OpenAI 's Hardware Business 'Rotten To Its Core' In...</a></li>
<li><a href="https://fortune.com/2026/07/10/apple-openai-lawsuit-trade-secrets-theft-allegations/">Apple accuses OpenAI, and former design star Jony Ive's io Products firm, of stealing hardware trade secrets in blockbuster lawsuit | Fortune</a></li>

</ul>
</details>

**Tags**: `#Apple`, `#OpenAI`, `#lawsuit`, `#trade secrets`, `#AI hardware`

---

<a id="item-10"></a>
## [Trump Administration Drives Intel Revival, Apple to Use Chips](https://www.wsj.com/tech/the-white-house-intel-trump-apple-84fe833e) ⭐️ 8.0/10

Apple has agreed to use Intel's manufacturing facilities for some of its chips, following pressure from the Trump administration. The U.S. government converted $9 billion in federal grants into a 10% stake in Intel, becoming its largest shareholder, and facilitated deals with Nvidia and SpaceX. This marks a significant government intervention in the semiconductor industry, potentially reshaping global chip manufacturing dynamics and strengthening U.S. supply chain resilience. It also highlights the strategic importance of reviving domestic chip production amid geopolitical tensions with China. The $9 billion conversion came from CHIPS Act funds, and Intel's new CEO Lip-Bu Tan meets monthly with Commerce officials. Intel's stock has tripled since March 2025, and the company's foundry services have secured major customers like Nvidia and SpaceX.

telegram · zaihuapd · Jul 11, 05:54

**Background**: The CHIPS and Science Act of 2022 allocated $52.7 billion to boost domestic semiconductor manufacturing and research. Intel, once a dominant chipmaker, has struggled to keep pace with TSMC in advanced manufacturing. Its foundry services unit, launched in 2021, aims to offer external customers access to Intel's fabrication technology. The Trump administration's actions continue bipartisan efforts to secure U.S. chip supply chains.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Intel_Foundry_Services">Intel Foundry Services</a></li>
<li><a href="https://en.wikipedia.org/wiki/CHIPS_Act">CHIPS Act</a></li>

</ul>
</details>

**Tags**: `#半导体`, `#产业政策`, `#英特尔`, `#苹果`, `#地缘政治`

---