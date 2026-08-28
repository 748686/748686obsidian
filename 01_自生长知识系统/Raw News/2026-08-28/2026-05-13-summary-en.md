---
layout: default
title: "Horizon Summary: 2026-05-13 (EN)"
date: 2026-05-13
lang: en
---

> From 47 items, 16 important content pieces were selected

---

1. [Six serious CVEs in dnsmasq prompt security debate](#item-1) ⭐️ 9.0/10
2. [Instructure Pays Ransom After Canvas Hack](#item-2) ⭐️ 9.0/10
3. [Googlebook: New AI-Powered Laptops from Google](#item-3) ⭐️ 8.0/10
4. [Needle: 26M Model Distilled from Gemini for Tool Calling](#item-4) ⭐️ 8.0/10
5. [DuckDB Unveils Quack Protocol for Client-Server Mode](#item-5) ⭐️ 8.0/10
6. [Deep Dive on Rendering Realistic Sky and Sunsets](#item-6) ⭐️ 8.0/10
7. [Obsidian Unveils New Plugin Review System and Community Site](#item-7) ⭐️ 8.0/10
8. [Guide to Learning Software Architecture Sparks Debate](#item-8) ⭐️ 8.0/10
9. [Bambu Lab faces backlash over user agent restrictions and open source abuse](#item-9) ⭐️ 8.0/10
10. [Canada's Bill C-22 Revives Surveillance and Encryption Backdoors](#item-10) ⭐️ 8.0/10
11. [Scaling transparent huge pages to 1GB](#item-11) ⭐️ 8.0/10
12. [Transformer LLM Runs on Unmodified Game Boy Color](#item-12) ⭐️ 8.0/10
13. [MagicQuant v2.0: Hybrid GGUF Quantization Pipeline](#item-13) ⭐️ 8.0/10
14. [llama-eval Adds Local Benchmarking to llama.cpp](#item-14) ⭐️ 8.0/10
15. [TanStack hit by 20-minute npm supply chain attack](#item-15) ⭐️ 8.0/10
16. [SpaceX, Google in Talks for Orbital Data Centers](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Six serious CVEs in dnsmasq prompt security debate](https://lists.thekelleys.org.uk/pipermail/dnsmasq-discuss/2026q2/018471.html) ⭐️ 9.0/10

CERT has released six CVEs for serious security vulnerabilities in dnsmasq, a widely used DNS forwarder and DHCP server, prompting urgent patching calls. These vulnerabilities affect millions of devices, including home routers, Android phones, and Linux systems, potentially allowing remote code execution or denial of service, making the need for memory-safe languages more urgent. The CVEs cover memory safety issues like buffer overflows and use-after-free, typical in C codebases. Patches are available in the latest dnsmasq release, but coordination with distributions like Debian and OpenWRT is ongoing.

hackernews · chizhik-pyzhik · May 12, 18:12 · [Discussion](https://news.ycombinator.com/item?id=48112042)

**Background**: Dnsmasq is a lightweight, open-source software providing DNS caching, DHCP, TFTP, and network boot for small networks. It runs on Linux, BSDs, Android, and macOS, and is embedded in many home routers and IoT devices. Because it is written in C, it is susceptible to memory safety bugs, which have been a recurring source of vulnerabilities.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Dnsmasq">Dnsmasq</a></li>
<li><a href="https://en.wikipedia.org/wiki/Memory_safety">Memory safety</a></li>
<li><a href="https://thekelleys.org.uk/dnsmasq/doc.html">Dnsmasq - network services for small networks.</a></li>

</ul>
</details>

**Discussion**: Commenters debate the urgency of moving to memory-safe languages like Rust, with some advocating for replacing dnsmasq entirely. Others criticize Debian for shipping an outdated version and discuss OpenWRT's patching progress. Some express a preference for separate tools over dnsmasq's all-in-one approach.

**Tags**: `#security`, `#dnsmasq`, `#CVE`, `#memory safety`, `#networking`

---

<a id="item-2"></a>
## [Instructure Pays Ransom After Canvas Hack](https://www.insidehighered.com/news/tech-innovation/administrative-tech/2026/05/11/instructure-pays-ransom-canvas-hackers) ⭐️ 9.0/10

Instructure, the company behind the Canvas learning platform, confirmed it paid a ransom to hackers who breached its systems in May 2026, receiving digital confirmation of data destruction. This incident sparks debate on whether ransom payments encourage more attacks, especially given Canvas's widespread adoption in education; it also raises questions about data security practices for sensitive student information. Instructure stated it received shred logs as proof of data deletion, but critics argue such logs can be falsified. The breach affected student and institutional data, though specific details remain limited.

hackernews · Cider9986 · May 12, 02:56 · [Discussion](https://news.ycombinator.com/item?id=48103668)

**Background**: Canvas is a learning management system used by thousands of schools worldwide. Ransomware attacks involve hackers encrypting or stealing data and demanding payment for its release or destruction. Paying ransoms is controversial because it funds criminal activity and may not guarantee data safety.

**Discussion**: Commenters expressed skepticism about the payment, with some comparing it to kidnapping ransoms and others noting that paying rewards ransomware groups. A user highlighted the irony that ransomware groups must appear 'credible' to stay in business, while another called the confirmation of data destruction 'shockingly naive.'

**Tags**: `#security`, `#ransomware`, `#education`, `#canvas`, `#cybersecurity`

---

<a id="item-3"></a>
## [Googlebook: New AI-Powered Laptops from Google](https://googlebook.google/) ⭐️ 8.0/10

Google announced Googlebook, a new category of laptops built on Android and integrated with Gemini AI, set to launch later this year in partnership with Acer, ASUS, Dell, HP, and Lenovo. This marks Google's attempt to redefine the laptop market with deep AI integration, but community skepticism about Google's product longevity and AI marketing could hinder adoption. Googlebook replaces Chromebooks, featuring deep Android integration and AI-powered features like shopping assistance, but initial reactions criticize Google's history of killing products and poor AI marketing.

hackernews · tambourine_man · May 12, 17:37 · [Discussion](https://news.ycombinator.com/item?id=48111545)

**Background**: Chromebooks were Google's previous laptop initiative, running Chrome OS and popular in education. Google has a reputation for discontinuing products (e.g., Google+, Stadia). The new Googlebook aims to leverage Google's Gemini AI, but the community remains skeptical based on past experiences.

<details><summary>References</summary>
<ul>
<li><a href="https://www.thurrott.com/google/335949/the-first-googlebook-laptops-with-gemini-intelligence-are-coming-later-this-year">The First ‘Googlebook’ Laptops With Gemini Intelligence Are</a></li>
<li><a href="https://timesfeatured.com/googlebook-is-googles-new-ai-powered-laptop-platform-built-on-android/">Googlebook Is Google’s New AI-Powered Laptop Platform Built</a></li>
<li><a href="https://stampedandsolotravel.com/article/googlebook-the-future-of-laptops-chromebook-successor-with-ai">Googlebook: The Future of Laptops? Chromebook Successor with</a></li>

</ul>
</details>

**Discussion**: Comments are overwhelmingly negative, citing Google's history of killing products and poor AI marketing. Users express reluctance to invest in a Google laptop due to fears of discontinuation, and criticize the initial demo focusing on AI shopping as out of touch.

**Tags**: `#Google`, `#laptops`, `#AI`, `#product launch`, `#community skepticism`

---

<a id="item-4"></a>
## [Needle: 26M Model Distilled from Gemini for Tool Calling](https://github.com/cactus-compute/needle) ⭐️ 8.0/10

Cactus Compute released Needle, a 26M parameter model distilled from Gemini for efficient single-shot function calling. It runs at 6000 tok/s prefill and 1200 tok/s decode on consumer devices. This demonstrates that large models are overkill for tool calling, enabling on-device agentic experiences on budget phones. It challenges the assumption that reasoning-heavy models are needed for structured output tasks. The model uses Simple Attention Networks (only attention and gating, no MLPs) and was pretrained on 200B tokens. It beats several larger models like FunctionGemma-270M but is limited to single-shot function calling, not conversational settings.

hackernews · HenryNdubuaku · May 12, 18:03 · [Discussion](https://news.ycombinator.com/item?id=48111896)

**Background**: Tool calling or function calling allows LLMs to interact with external APIs and tools. Distillation is a technique to create smaller, faster student models that mimic larger teacher models. Needle is an example of a highly specialized small model for a specific task.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/@aevalone/clarifying-function-calling-tool-use-in-llms-6511af510f99">Clarifying Function Calling / Tool Use in LLMs | Medium</a></li>
<li><a href="https://dev.to/apideck/an-introduction-to-function-calling-and-tool-use-in-llms-9kl">An introduction to function calling and tool use in LLMs</a></li>
<li><a href="https://medium.com/@piyushkashyap045/llm-distillation-the-key-to-efficient-ai-models-cb4026a655bf">LLM Distillation : The Key to Efficient AI Models | by Piyush... | Medium</a></li>

</ul>
</details>

**Discussion**: Community comments show interest in browser deployment, feasibility for CLI tools, and appreciation for tiny models. Suggestions include publishing a live demo and clarifying model size notation. Overall sentiment is positive, with excitement about on-device agents.

**Tags**: `#distillation`, `#tool-calling`, `#small-models`, `#on-device-AI`, `#attention-networks`

---

<a id="item-5"></a>
## [DuckDB Unveils Quack Protocol for Client-Server Mode](https://duckdb.org/2026/05/12/quack-remote-protocol) ⭐️ 8.0/10

On May 12, 2026, DuckDB Labs announced Quack, an HTTP-based client-server protocol that enables remote query execution and horizontal scaling for DuckDB, allowing it to run as a server with multiple concurrent writers for the first time. This addresses DuckDB's historical limitation as an embedded database without a server mode, making it suitable for shared team servers and small-ball internal analytics. The protocol claims to be 32x faster than PostgreSQL for bulk analytics workloads. Quack is implemented as an extension called 'duckdb-quack' available on GitHub. It uses HTTP as the transport layer and supports multiple concurrent writers, a significant improvement over the previous single-user embedded model.

hackernews · aduffy · May 12, 17:54 · [Discussion](https://news.ycombinator.com/item?id=48111765)

**Background**: DuckDB is an in-process SQL OLAP database that traditionally runs embedded within applications and does not have a client-server interface. This means it was limited to single-user scenarios without remote access. Quack changes that by adding a network protocol, enabling DuckDB to be used as a lightweight analytics server.

<details><summary>References</summary>
<ul>
<li><a href="https://motherduck.com/blog/first-variant/duckdb-client-server/">If It Quacks Like a Duck: DuckDB Gets a Client-Server Protocol</a></li>
<li><a href="https://byteiota.com/quack-protocol-duckdb-client-server-32x-faster/">Quack Protocol: DuckDB Client-Server 32x Faster | byteiota</a></li>
<li><a href="https://github.com/duckdb/duckdb-quack">GitHub - duckdb/duckdb-quack · GitHub</a></li>

</ul>
</details>

**Discussion**: The community is excited, with users seeing Quack as a solution for horizontal scaling in internal apps and small team servers. One user considered using it via SSH for remote queries, while another questioned its suitability for multi-user read/write scenarios with low performance requirements compared to SQLite. Overall, sentiment is positive and curious about practical applications.

**Tags**: `#DuckDB`, `#database`, `#client-server`, `#scalability`, `#analytics`

---

<a id="item-6"></a>
## [Deep Dive on Rendering Realistic Sky and Sunsets](https://blog.maximeheckel.com/posts/on-rendering-the-sky-sunsets-and-planets/) ⭐️ 8.0/10

Maxime Heckel published a detailed blog post on rendering realistic sky, sunsets, and planets using atmospheric scattering models, with interactive WebGL demos. This post fills a gap in accessible, hands-on tutorials for atmospheric scattering in real-time graphics, benefiting WebGL developers and hobbyists interested in procedural sky rendering. The implementation uses Rayleigh and Mie scattering, along with transmittance and single scattering approximations, but the demo's sunset model incorrectly turns the sky black immediately after the sun sets, as noted by a commenter.

hackernews · ibobev · May 12, 13:26 · [Discussion](https://news.ycombinator.com/item?id=48107997)

**Background**: Atmospheric scattering explains why the sky is blue and sunsets are red. In computer graphics, Rayleigh scattering simulates light scattering by small particles (air molecules), while Mie scattering handles larger particles like dust. Real-time rendering often simplifies these physical models to achieve performance on GPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://developer.nvidia.com/gpugems/gpugems2/part-ii-shading-lighting-and-shadows/chapter-16-accurate-atmospheric-scattering">Chapter 16. Accurate Atmospheric Scattering | NVIDIA Developer</a></li>
<li><a href="https://en.wikipedia.org/wiki/Rayleigh_scattering">Rayleigh scattering - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Commenters praise the write-up and share related works, such as Sebastian Lague's video on planetary atmospheres. A notable critique points out that the sunset model fails to maintain twilight glow after sunset, a limitation acknowledged as difficult to fix.

**Tags**: `#computer graphics`, `#atmospheric scattering`, `#rendering`, `#shaders`

---

<a id="item-7"></a>
## [Obsidian Unveils New Plugin Review System and Community Site](https://obsidian.md/blog/future-of-plugins/) ⭐️ 8.0/10

Obsidian announced a new community site and automated review system to handle the plugin submission backlog and reduce developer frustration, after nearly a year of development. This resolves a critical scaling bottleneck for Obsidian's plugin ecosystem, reducing developer frustration and preventing team burnout, while improving plugin quality and potential security. The automated system aims to assess plugins for security and functionality, but community members expressed skepticism about reliably detecting malicious code, and concerns about iOS code execution restrictions remain.

hackernews · xz18r · May 12, 15:45 · [Discussion](https://news.ycombinator.com/item?id=48109970)

**Background**: Obsidian is a popular note-taking app that supports a large ecosystem of community plugins. Previously, all plugins required manual review by a small team (only seven people), leading to a significant backlog and developer frustration. The new system introduces automated checks to streamline submissions.

**Discussion**: CEO kepano expressed excitement and acknowledged the challenges, while dtkav praised the solution for relieving the scaling bottleneck. Others like varun_ch doubted the effectiveness of automated security checks, and ydj questioned how plugins comply with iOS restrictions on downloaded code.

**Tags**: `#obsidian`, `#plugins`, `#community`, `#review-system`, `#automation`

---

<a id="item-8"></a>
## [Guide to Learning Software Architecture Sparks Debate](https://matklad.github.io/2026/05/12/software-architecture.html) ⭐️ 8.0/10

An article on fundamental software architecture principles was published on matklad.github.io, generating extensive community discussion and shared insights. This article and its discussion highlight the practical importance of software architecture for engineers, offering valuable recommendations and sparking debate on best practices. The article scored 8.0/10 with high community engagement of 514 points and 103 comments, indicating broad relevance.

hackernews · surprisetalk · May 12, 09:30 · [Discussion](https://news.ycombinator.com/item?id=48106024)

**Background**: Software architecture refers to the high-level structures of a software system and the discipline of creating such structures. It involves making fundamental design decisions that affect the system's quality attributes like performance, maintainability, and scalability. Learning architecture often involves studying principles, patterns, and real-world examples.

**Discussion**: Comments recommended classic texts like 'A Philosophy of Software Design' and 'Software Architecture: Perspectives on an Emerging Discipline'. Some argued that true architecture learning comes from maintaining large projects, and suggested the 'Architecture of Open Source Applications' series as a practical resource.

**Tags**: `#software-architecture`, `#best-practices`, `#design-principles`, `#engineering-culture`

---

<a id="item-9"></a>
## [Bambu Lab faces backlash over user agent restrictions and open source abuse](https://www.jeffgeerling.com/blog/2026/bambu-lab-abusing-open-source-social-contract/) ⭐️ 8.0/10

Bambu Lab has implemented user agent restrictions on its 3D printer ecosystem, blocking third-party tools by relying on client-supplied metadata, and is facing criticism for violating the open source social contract. This controversy highlights ongoing tensions between closed ecosystems and open source values in the 3D printing community, potentially eroding trust in Bambu Lab and influencing consumer choices. The company's justification—that restrictions prevent service outages from unauthorized traffic spikes—is widely dismissed as weak, as user agent strings can be easily spoofed.

hackernews · rubenbe · May 12, 14:54 · [Discussion](https://news.ycombinator.com/item?id=48109224)

**Background**: The open source social contract in 3D printing implies that users have freedom to control their hardware and software. User agent strings are metadata sent by clients to identify themselves; blocking based solely on this is not effective security. Bambu Lab previously faced backlash over LAN mode restrictions and changed course after community outrage.

<details><summary>References</summary>
<ul>
<li><a href="https://chromewebstore.google.com/detail/random-user-agent-switche/einpaelgookohagofgnnkcfjbkkgepnp">Random User - Agent (Switcher) - Chrome Web Store</a></li>
<li><a href="https://docs.wpvip.com/security-controls/user-agent-restrictions/">User Agent Restrictions · WordPress VIP Documentation</a></li>

</ul>
</details>

**Discussion**: Commenters widely criticize Bambu Lab's excuses, noting that user agent spoofing is trivial and that the company previously reversed course on LAN mode after similar outrage. One commenter speculates about geopolitical motives related to wartime use in Ukraine.

**Tags**: `#open source`, `#3D printing`, `#Bambu Lab`, `#community backlash`, `#tech ethics`

---

<a id="item-10"></a>
## [Canada's Bill C-22 Revives Surveillance and Encryption Backdoors](https://www.eff.org/deeplinks/2026/05/canadas-bill-c-22-repackaged-version-last-years-surveillance-nightmare) ⭐️ 8.0/10

Canada's government has introduced Bill C-22, the Lawful Access Act, which would mandate data retention and encryption backdoors, threatening end-to-end encrypted services like Signal and WhatsApp. If passed, Bill C-22 could force encrypted messaging providers to block Canadian users or weaken their security, undermining global digital rights and setting a dangerous precedent for surveillance legislation. Bill C-22 is a rebranded version of last year's failed Bill C-2, and includes requirements for mandatory data retention and exceptional access to encrypted communications, according to the EFF.

hackernews · Brajeshwar · May 12, 17:35 · [Discussion](https://news.ycombinator.com/item?id=48111531)

**Background**: Encryption backdoors are deliberate vulnerabilities in cryptographic systems designed to allow government access to encrypted data. Data retention laws require service providers to store user communications and metadata for potential law enforcement access. Both practices are highly controversial as they can weaken overall security and infringe on privacy.

<details><summary>References</summary>
<ul>
<li><a href="https://www.eff.org/deeplinks/2026/05/canadas-bill-c-22-repackaged-version-last-years-surveillance-nightmare">Canada’s Bill C-22 Is a Repackaged Version of Last Year’s ...</a></li>
<li><a href="https://www.parl.ca/DocumentViewer/en/45-1/bill/C-22/first-reading">Government Bill (House of Commons) C-22 (45-1) - First ...</a></li>
<li><a href="https://www.internetsociety.org/blog/2025/05/what-is-an-encryption-backdoor/">What Is an Encryption Backdoor? - Internet Society</a></li>

</ul>
</details>

**Discussion**: Commenters expressed strong opposition, with one user noting the bill would force encrypted services to block Canadians, and another criticizing the persistent reintroduction of such legislation. A user also requested a French translation of the EFF article to aid advocacy.

**Tags**: `#surveillance`, `#encryption`, `#Canada`, `#digital rights`, `#legislation`

---

<a id="item-11"></a>
## [Scaling transparent huge pages to 1GB](https://lwn.net/Articles/1071716/) ⭐️ 8.0/10

Usama Arif proposed extending transparent huge pages (THP) to support 1GB pages at the 2026 Linux Storage, Filesystem, Memory Management, and BPF Summit. This could significantly improve performance and scalability for large-memory systems with terabytes of RAM, reducing management overhead. It makes 1GB pages available transparently without manual hugetlbfs configuration. The RFC patch set was surprisingly small and less invasive than expected. Key discussion points included whether to preallocate page-table pages for splitting (deposit) – currently 2MB per 1GB THP – or to avoid it entirely.

rss · LWN.net · May 12, 13:24

**Background**: Transparent Huge Pages (THP) is a Linux kernel feature that automatically uses 2MB (PMD-level) pages to reduce TLB misses. Currently, 1GB (PUD-level) huge pages are only available via hugetlbfs, which requires static pre-allocation at boot time. The proposal aims to make 1GB pages transparently available to applications, providing dynamic fallback when huge page allocation fails.

<details><summary>References</summary>
<ul>
<li><a href="https://oneuptime.com/blog/post/2026-03-02-how-to-configure-transparent-huge-pages-on-ubuntu/view">How to Configure Transparent Huge Pages on Ubuntu</a></li>
<li><a href="https://stackoverflow.com/questions/59123308/why-linux-has-4-layers-of-page-tables-and-how-it-works-exactly">memory - Why Linux has 4 layers of "page tables" and how it ...</a></li>
<li><a href="https://joelsiks.com/posts/linux-huge-pages/">Huge Pages on Linux</a></li>

</ul>
</details>

**Discussion**: David Hildenbrand argued that splitting 1GB THPs indicates something wrong and questioned the need for preallocating page-table pages. Kiryl Shutsemau suggested that processes could request 1GB THPs via the madvise system call.

**Tags**: `#Linux`, `#Kernel`, `#Memory Management`, `#Huge Pages`, `#THP`

---

<a id="item-12"></a>
## [Transformer LLM Runs on Unmodified Game Boy Color](https://i.redd.it/1hl9id7ghs0h1.jpeg) ⭐️ 8.0/10

A transformer language model (TinyStories-260K) has been successfully run locally on a stock Game Boy Color, using fixed-point arithmetic and bank-switched cartridge ROM to store model weights. This demonstrates that even severely constrained 8-bit hardware can run modern transformer models, pushing the boundaries of edge inference and showing potential for low-power offline AI applications. The model is Andrej Karpathy's TinyStories-260K, converted to INT8 weights and using a custom kernel with fixed-point math. The KV cache is stored in cartridge SRAM, and prompt entry is done via the Game Boy's D-pad and buttons.

reddit · r/LocalLLaMA · maddiedreese · May 12, 23:15 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1tbi2n3/i_got_a_real_transformer_language_model_running/)

**Background**: The Game Boy Color has an 8-bit CPU at about 8 MHz, with 32 KB of work RAM and limited cartridge ROM/RAM. TinyStories-260K is a minimal transformer trained on simple stories, with only 260K parameters. Fixed-point arithmetic avoids floating-point hardware, and MBC5 bank switching allows accessing up to 8 MB of ROM by swapping banks.

<details><summary>References</summary>
<ul>
<li><a href="https://hackaday.io/project/205074-on-chip-lm-tinystories-260k-on-cortex-m7">On-Chip LM: TinyStories 260K on Cortex-M7 - Hackaday.io</a></li>
<li><a href="https://arxiv.org/abs/2203.12758">Mokey: Enabling Narrow Fixed-Point Inference for Out-of-the ...</a></li>
<li><a href="https://gbdk.org/docs/api/docs_rombanking_mbcs.html">GBDK 2020 Docs: ROM/RAM Banking and MBCs</a></li>

</ul>
</details>

**Discussion**: The community expressed strong admiration and excitement, with comments like 'Wow just wow' and 'Extremely impressive, well done!'. Some users joked about running models on other retro consoles like the N64, and referenced similar projects.

**Tags**: `#transformer`, `#Game Boy`, `#edge inference`, `#quantization`, `#hobbyist`

---

<a id="item-13"></a>
## [MagicQuant v2.0: Hybrid GGUF Quantization Pipeline](https://www.reddit.com/r/LocalLLaMA/comments/1tb3sja/magicquant_v20_hybrid_mixed_gguf_models_unsloth/) ⭐️ 8.0/10

MagicQuant v2.0 introduces a pipeline that creates hybrid mixed GGUF quant models by learning per-tensor quantization assignments from Unsloth and other sources, and produces benchmark tables identifying optimal configurations per VRAM budget. This project addresses the need for layer-specific quantization optimization in LLMs, improving efficiency and quality for local deployment, and provides systematic benchmarks to guide users. MagicQuant uses per-tensor Kullback-Leibler divergence to detect layer-specific quantization sensitivities, handles non-monotonic KLD curves with collapse logic, and integrates Unsloth's learned configurations for improved accuracy.

reddit · r/LocalLLaMA · crossivejoker · May 12, 14:46

**Background**: GGUF is a binary format for storing quantized large language models, used by llama.cpp for efficient inference. Quantization reduces model size by lowering the precision of weights, but can degrade performance. Hybrid (mixed-precision) quantization assigns different bit widths to different layers to balance size and quality. Unsloth is an open-source library that provides fast fine-tuning and quantization, including dynamic learned quant configurations.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/@bnjmn_marie/gguf-quantization-for-fast-and-memory-efficient-inference-on-your-cpu-d10fbe58fbca">GGUF Quantization for Fast and Memory-Efficient Inference... | Medium</a></li>
<li><a href="https://unsloth.ai/docs">Unsloth Docs | Unsloth Documentation</a></li>
<li><a href="https://quark.docs.amd.com/release-0.5.1/onnx/tutorial_mix_precision.html">Tutorial: Mixed Precision — Quark 0.5.1 documentation</a></li>

</ul>
</details>

**Discussion**: Commenters praised the concept and commitment, noting the importance of per-tensor KLD tracking. One user inquired about handling non-monotonic KLD curves, while another suggested adding balloon graphs similar to Unsloth's benchmarks.

**Tags**: `#quantization`, `#GGUF`, `#Unsloth`, `#local LLM`, `#optimization`

---

<a id="item-14"></a>
## [llama-eval Adds Local Benchmarking to llama.cpp](https://github.com/ggml-org/llama.cpp/pull/21152) ⭐️ 8.0/10

A new pull request adds the `llama-eval` tool to llama.cpp, enabling local evaluation of LLMs on standard benchmarks including AIME, GSM8K, and GPQA. This addresses a common pain point for the local LLM community by providing a standardized evaluation tool directly within llama.cpp, making it easy to compare different quantizations and finetunes without external dependencies. The tool supports three datasets: AIME (math olympiad-level reasoning), GSM8K (grade school math), and GPQA (graduate-level science multiple-choice). Users can run evaluations with adjustable parallelism and context length.

reddit · r/LocalLLaMA · jacek2023 · May 12, 12:57 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1tb0uln/examples_add_llamaeval_by_ggerganov_pull_request/)

**Background**: llama.cpp is a popular open-source project for running large language models locally on consumer hardware, supporting quantization for efficiency. Standard benchmarks like AIME, GSM8K, and GPQA are widely used to evaluate LLM performance on math and science reasoning.

<details><summary>References</summary>
<ul>
<li><a href="https://www.emergentmind.com/topics/aime-benchmarks">AIME Benchmarks : Math & AI Evaluation</a></li>
<li><a href="https://www.oxen.ai/datasets/GSM8K">datasets/GSM8K | Datasets at Oxen.ai</a></li>
<li><a href="https://arxiv.org/abs/2311.12022">GPQA: A Graduate-Level Google-Proof Q&A Benchmark GPQA Benchmark 2026: 50 LLM scores | BenchLM.ai GPQA Leaderboard | Kaggle GPQA-Diamond Benchmark: Scores, Leaderboard & How AI Models ... AI Benchmarks 2026 - MMLU, GPQA, SWE-bench | LM Market Cap</a></li>

</ul>
</details>

**Discussion**: The community response is overwhelmingly positive, with users praising the convenience and standardization. Comments highlight that previous attempts to benchmark locally were cumbersome, requiring external tools or API keys. Some users note the high resource requirements for certain evaluations, but overall see this as a valuable addition.

**Tags**: `#llama.cpp`, `#LLM evaluation`, `#benchmarking`, `#quantization`, `#local LLM`

---

<a id="item-15"></a>
## [TanStack hit by 20-minute npm supply chain attack](https://tanstack.com/blog/npm-supply-chain-compromise-postmortem) ⭐️ 8.0/10

On May 11, 2026, between 19:20 and 19:26 UTC, attackers published 84 malicious versions across 42 TanStack npm packages using a sophisticated chain of pull_request_target, GitHub Actions cache poisoning, and OIDC token extraction. This attack demonstrates a new level of sophistication in npm supply chain attacks, combining multiple GitHub Actions vulnerabilities to achieve valid SLSA Build Level 3 attestations, potentially affecting thousands of downstream projects. The attacker exploited pull_request_target to run code in the repository context, poisoned the build cache to inject malicious code, and extracted OIDC tokens from runner memory to sign attestations; the malicious versions were detected and deprecated within 20 minutes.

telegram · zaihuapd · May 12, 03:00

**Background**: GitHub Actions workflows using pull_request_target run in the context of the target repository, which can be exploited if the workflow checks out and executes code from the pull request. Cache poisoning allows attackers to inject malicious content into the build cache, which later gets used in subsequent builds. OIDC tokens are short-lived credentials used for authentication with cloud providers; extracting them from runner memory enables an attacker to sign artifacts with valid SLSA attestations.

<details><summary>References</summary>
<ul>
<li><a href="https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure Part 1: Preventing...</a></li>
<li><a href="https://aviii.hashnode.dev/the-pwn-request">The Pwn - Request : Securing CI/CD from pull _ request _ target Attacks</a></li>
<li><a href="https://snyk.io/blog/tanstack-npm-packages-compromised/">TanStack npm Packages Hit by Mini Shai-Hulud | Snyk</a></li>

</ul>
</details>

**Tags**: `#npm`, `#supply-chain-attack`, `#GitHub Actions`, `#dependency security`, `#OIDC`

---

<a id="item-16"></a>
## [SpaceX, Google in Talks for Orbital Data Centers](https://www.wsj.com/tech/spacex-google-in-talks-to-explore-data-centers-in-orbit-7b7799e2) ⭐️ 8.0/10

Google is in discussions with SpaceX for rocket launch agreements to support its Project Suncatcher, with a goal of launching a prototype orbital data center by 2027. This partnership could revolutionize cloud computing by enabling data processing in space, reducing reliance on terrestrial energy and latency for space-based applications, and marks a strategic shift by two industry giants toward orbital infrastructure. Google's Project Suncatcher involves solar-powered satellites equipped with custom Tensor Processing Units (TPUs), networked via free-space optical links. SpaceX is emphasizing orbital data centers as a key selling point for its upcoming IPO, and recently struck a ground-based compute deal with Anthropic for 300 MW of compute and over 220,000 Nvidia GPUs.

telegram · zaihuapd · May 12, 16:28

**Background**: Orbital data centers are a concept where computing resources are placed in space, offering advantages such as unlimited solar energy and low latency for satellite data processing. Google announced Project Suncatcher in November 2025, and the idea has been explored in academic research, including a peer-reviewed paper in Nature Electronics. SpaceX's Starship is a potential launch vehicle for such infrastructure.

<details><summary>References</summary>
<ul>
<li><a href="https://money.usnews.com/investing/news/articles/2026-05-12/google-spacex-in-talks-to-explore-data-centers-in-orbit-wsj-reports">Google in Talks With SpaceX for Suncatcher Orbital Data ...</a></li>
<li><a href="https://arstechnica.com/google/2025/11/meet-project-suncatcher-googles-plan-to-put-ai-data-centers-in-space/">Meet Project Suncatcher, Google’s plan to put AI data centers ...</a></li>
<li><a href="https://www.forbes.com/sites/anishasircar/2025/11/11/google-unveils-project-suncatcher-to-run-ai-on-solar-satellites-in-orbit/">Google Plans To Run AI Data Centers In Space With Project ...</a></li>

</ul>
</details>

**Tags**: `#Space`, `#Data Centers`, `#Cloud Computing`, `#SpaceX`, `#Google`

---