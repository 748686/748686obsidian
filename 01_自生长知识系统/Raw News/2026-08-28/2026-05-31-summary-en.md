---
layout: default
title: "Horizon Summary: 2026-05-31 (EN)"
date: 2026-05-31
lang: en
---

> From 48 items, 14 important content pieces were selected

---

1. [Running Python ASGI Apps in Browser with Pyodide and Service Workers](#item-1) ⭐️ 9.0/10
2. [SpaceX Wins $4.16B US Military Satellite Missile Tracking Contract](#item-2) ⭐️ 9.0/10
3. [Accenture acquires Ookla for $1.2B](#item-3) ⭐️ 8.0/10
4. [Zig's ELF Linker Improvements Detailed in Devlog](#item-4) ⭐️ 8.0/10
5. [Voxel Space Tutorial Revives 1992 Comanche Graphics](#item-5) ⭐️ 8.0/10
6. [OpenRouter raises $113M Series B](#item-6) ⭐️ 8.0/10
7. [Openrsync: OpenBSD's reimplementation of rsync adopted in macOS](#item-7) ⭐️ 8.0/10
8. [Pope Leo's first encyclical criticizes technological messianism](#item-8) ⭐️ 8.0/10
9. [Anthropic details sandboxing techniques for Claude across products](#item-9) ⭐️ 8.0/10
10. [Debugger reveals training failures local to layers and steps](#item-10) ⭐️ 8.0/10
11. [NVIDIA NVFP4 Quantization of Qwen3.6-35B-A3B](#item-11) ⭐️ 8.0/10
12. [GPU Specs Comparison for Local LLM Inference Challenges Mac Recommendations](#item-12) ⭐️ 8.0/10
13. [Parallax: Parameterized Local Linear Attention for LLMs](#item-13) ⭐️ 8.0/10
14. [Huawei Proposes 'Tao Law' Using Temporal Scaling for Chips](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Running Python ASGI Apps in Browser with Pyodide and Service Workers](https://simonwillison.net/2026/May/30/pyodide-asgi-browser/#atom-everything) ⭐️ 9.0/10

Simon Willison demonstrated a method to run Python ASGI apps in the browser using Pyodide and Service Workers, enabling execution of JavaScript script tags that previously failed in Web Worker-based approaches. This was achieved via a Claude Code experiment and tested with Datasette Lite and a basic ASGI FastCGI demo. This breakthrough overcomes a key limitation of running Python apps in the browser, allowing proper execution of JavaScript-dependent plugins and dynamic content. It significantly enhances the capabilities of Python-in-browser tools like Datasette Lite and expands the potential for serverless Python applications. The demo uses Service Workers instead of Web Workers to intercept network requests and run Python ASGI apps within Pyodide, preserving script tag execution. Simon plans to upgrade Datasette Lite to adopt this approach after fully understanding the implementation.

rss · Simon Willison · May 30, 21:02

**Background**: Pyodide is a Python distribution for the browser based on WebAssembly, allowing Python to run entirely on the client side. ASGI (Asynchronous Server Gateway Interface) is a specification for asynchronous Python web servers and applications, enabling modern web frameworks like FastAPI and Starlette. Service Workers are scripts that run in the background of a web browser, capable of intercepting network requests and enabling offline experiences.

<details><summary>References</summary>
<ul>
<li><a href="https://pyodide.org/">Pyodide — Version 0.29.4</a></li>
<li><a href="https://github.com/pyodide/pyodide">GitHub - pyodide / pyodide : Pyodide is a Python distribution for...</a></li>

</ul>
</details>

**Tags**: `#Pyodide`, `#ASGI`, `#WebAssembly`, `#Datasette`, `#Service Workers`

---

<a id="item-2"></a>
## [SpaceX Wins $4.16B US Military Satellite Missile Tracking Contract](https://www.bloomberg.com/news/articles/2026-05-29/spacex-wins-4-billion-contract-for-us-golden-dome-satellites) ⭐️ 9.0/10

SpaceX has been awarded a $4.16 billion contract by the US Space Force to develop a space-based missile tracking constellation as part of the Golden Dome defense system. This contract marks a significant expansion of SpaceX's role in national security space, and the network aims to reduce blind spots in existing ground-based radar and airborne surveillance. It positions SpaceX at the core of a next-generation layered missile defense architecture. The constellation will integrate space-based sensors, communication systems, and ground processing capabilities to track foreign aircraft, missiles, and other aerial threats from orbit. SpaceX had previously contributed to Golden Dome's space-based interceptor prototype development and joined a multi-company consortium for the program's underlying software.

telegram · zaihuapd · May 30, 01:53

**Background**: The Golden Dome defense plan, announced by President Trump in May 2025, is a modern iteration of the Strategic Defense Initiative (SDI) from the 1980s, often called 'Star Wars'. It aims to create a layered homeland missile defense system using space-based sensors and interceptors to counter evolving threats from ballistic and hypersonic missiles. Similar concepts were revived in 2019 under the Space Development Agency's National Defense Space Architecture.

<details><summary>References</summary>
<ul>
<li><a href="https://www.nytimes.com/2025/05/20/us/politics/trump-golden-dome.html">Trump Unveils Plans for ‘Golden Dome’ Missile Defense</a></li>
<li><a href="https://en.wikipedia.org/wiki/Space-Based_Interceptor">Space-Based Interceptor</a></li>

</ul>
</details>

**Tags**: `#SpaceX`, `#defense`, `#satellite`, `#military`, `#space`

---

<a id="item-3"></a>
## [Accenture acquires Ookla for $1.2B](https://newsroom.accenture.com/news/2026/accenture-to-acquire-ookla-to-strengthen-network-intelligence-and-experience-with-data-and-ai-for-enterprises) ⭐️ 8.0/10

Accenture announced the acquisition of Ookla, the company behind Speedtest and Downdetector, for $1.2 billion to enhance network intelligence with data and AI for enterprises. This acquisition gives Accenture access to vast network performance data from millions of consumer tests, enabling it to offer deeper insights for telecoms and enterprises. It also raises concerns about data trust and potential conflicts of interest, as Accenture now owns tools that monitor outages of its consulting clients. The deal includes Ookla's data products such as Speedtest, Downdetector, Ekahau, and RootMetrics, with over 250 million consumer-initiated tests per month. Accenture plans to use this data to help communication service providers optimize Wi-Fi and 5G networks.

hackernews · Garbage · May 30, 16:28 · [Discussion](https://news.ycombinator.com/item?id=48337987)

**Background**: Ookla is best known for Speedtest.net, a widely used internet speed testing platform. Its data is highly valued by telecom operators for network planning and optimization. Accenture is a global professional services company specializing in IT services and consulting. The acquisition aligns with Accenture's strategy to integrate data and AI into enterprise network solutions.

**Discussion**: Community comments highlight that the real value of the deal lies in the data, not the consumer tools, with telcos paying six figures annually for insights. Some express distrust, fearing that Accenture could manipulate outage data to protect its consulting clients. A former employee confirms that the data business is highly lucrative and that Accenture was already a competitor through its Umlaut acquisition.

**Tags**: `#acquisition`, `#network intelligence`, `#data`, `#AI`, `#enterprise`

---

<a id="item-4"></a>
## [Zig's ELF Linker Improvements Detailed in Devlog](https://ziglang.org/devlog/2026/#2026-05-30) ⭐️ 8.0/10

A new devlog from the Zig team details improvements to its ELF linker, focusing on faster incremental compilation and linking for development iteration. These improvements could make Zig a more practical C replacement by drastically reducing compile-link-iterate times, especially for systems programming. It also enables better toolchain interoperability and could influence other languages like Raku to consider Zig as a backend target. The linker supports incremental linking, which is beneficial for development but may not be suitable for release builds due to potential incompatibility with link-time optimization. The devlog includes specific technical advancements that the community has been eagerly awaiting.

hackernews · kristoff_it · May 30, 17:29 · [Discussion](https://news.ycombinator.com/item?id=48338673)

**Background**: Zig is a modern systems programming language designed to improve upon C, with features like compile-time generics, manual memory management, and no hidden control flow. The ELF (Executable and Linkable Format) is the standard binary format on Linux and Unix-like systems, and a linker is a tool that combines object files into an executable. The Zig linker is a self-hosted component that handles linking for Zig and potentially other languages, making its performance crucial for developer productivity.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Zig_(programming_language)">Zig (programming language)</a></li>
<li><a href="https://en.wikipedia.org/wiki/ELF_file_format">ELF file format</a></li>
<li><a href="https://ziglang.org/">Home Zig Programming Language</a></li>

</ul>
</details>

**Discussion**: Comments express excitement about the linker progress, with users noting it could make Zig a true C replacement and enable rapid iteration similar to dynamic languages. Some discuss potential use cases like porting Raku's VM to Zig, while others raise questions about incremental linking's compatibility with release-mode optimizations.

**Tags**: `#Zig`, `#linker`, `#systems programming`, `#compilers`, `#performance`

---

<a id="item-5"></a>
## [Voxel Space Tutorial Revives 1992 Comanche Graphics](https://s-macke.github.io/VoxelSpace/) ⭐️ 8.0/10

An interactive tutorial has been published that explains the Voxel Space algorithm used in the 1992 game Comanche, demonstrating height-map-based terrain rendering with step-by-step visualization. This tutorial provides a rare deep dive into a groundbreaking retro-graphics technique, making it accessible to modern developers and enthusiasts, and preserving the history of real-time 3D rendering. The algorithm is technically a height-map renderer, not true voxel rendering, as it uses a 2D height array to create 3D terrain. The tutorial includes interactive demos and links to C++ and AGS ports.

hackernews · davikr · May 30, 14:25 · [Discussion](https://news.ycombinator.com/item?id=48336564)

**Background**: The Voxel Space algorithm was developed by NovaLogic for the 1992 helicopter combat game Comanche, achieving smooth terrain rendering on early PCs. Unlike true voxel methods that store data in a 3D grid, it uses a height map—a grayscale image where each pixel's brightness represents elevation—to efficiently render landscapes by projecting columns of prisms onto the screen.

<details><summary>References</summary>
<ul>
<li><a href="https://www.colinhoad.com/voxel-space-demo-bits-and-bytes-ep-4">Voxel Space Demo - Bits and Bytes (Ep. 4) | Colin Hoad</a></li>
<li><a href="https://en.wikipedia.org/wiki/Heightmap">Heightmap - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Commenters noted the technical distinction between height maps and true voxels, with one user sharing a personal anecdote about "oil tank holiday" tests in code testing. Several users contributed links to their own implementations in C++, AGS, and other platforms, highlighting the algorithm's lasting influence.

**Tags**: `#voxel-space`, `#terrain-rendering`, `#retro-graphics`, `#algorithm`, `#comanche`

---

<a id="item-6"></a>
## [OpenRouter raises $113M Series B](https://openrouter.ai/announcements/series-b) ⭐️ 8.0/10

OpenRouter, a unified LLM API proxy platform, has raised $113 million in Series B funding to expand its infrastructure and user base. This major funding round signals strong investor confidence in AI infrastructure intermediaries, as OpenRouter reduces friction for developers by aggregating over 300 models behind a single API, potentially accelerating adoption of diverse LLMs. OpenRouter charges a 5% surcharge on API usage, and claims over 250,000 apps and 4.2 million users globally. The company remains founder-led and founder-controlled post-funding.

hackernews · freeCandy · May 30, 17:27 · [Discussion](https://news.ycombinator.com/item?id=48338660)

**Background**: OpenRouter is an API proxy that provides a unified interface for accessing hundreds of LLMs, including models from OpenAI, Anthropic, and open-source alternatives. Developers can switch between models with minimal code changes, and the platform offers features like automatic routing and billing caps, which many providers lack. The service is compatible with the OpenAI SDK, making integration straightforward for many existing applications.

<details><summary>References</summary>
<ul>
<li><a href="https://apify.com/apify/openrouter">OpenRouter · Apify</a></li>
<li><a href="https://openrouter.ai/">OpenRouter</a></li>
<li><a href="https://www.morphllm.com/openrouter-alternative">OpenRouter Alternative: Intelligent Model Routing vs API Proxies</a></li>

</ul>
</details>

**Discussion**: Community comments on Hacker News reflect mixed views: while many praise OpenRouter for its low-friction model experimentation and billing caps, some question the long-term value given the 5% surcharge and the potential consolidation of the LLM market. The co-founder responded that the company remains founder-controlled and aims to build strong products for builders.

**Tags**: `#AI`, `#funding`, `#OpenRouter`, `#LLM`, `#API`

---

<a id="item-7"></a>
## [Openrsync: OpenBSD's reimplementation of rsync adopted in macOS](https://github.com/kristapsdz/openrsync) ⭐️ 8.0/10

The OpenBSD team has released Openrsync, a new implementation of the rsync file synchronization tool, which has already been adopted in macOS 15.0 as the default rsync. This reimplementation offers a more secure and maintainable codebase for the widely-used rsync protocol, reducing reliance on the original Samba-maintained version and improving integration in BSD and macOS ecosystems. Openrsync was initially developed as part of an RPKI validator project, and while it generally matches Samba rsync's functionality, some users have reported issues with the --rsync-path option when syncing directories.

hackernews · sph · May 30, 10:51 · [Discussion](https://news.ycombinator.com/item?id=48334854)

**Background**: rsync is a popular open-source utility for efficiently transferring and synchronizing files across systems, commonly used for backups and mirroring. The original implementation is maintained by the Samba team, but concerns about code complexity and security have led to alternative implementations like Openrsync.

**Discussion**: Community comments are generally positive, noting steady improvements and enthusiasm for exclusive use. However, one user pointed out a specific compatibility issue with the --rsync-path flag when syncing to a remote directory. Another comment highlighted a separate Go-based rsync implementation by the Gokrazy team, and one user mentioned that vibe-coded commits in the original rsync codebase make Openrsync a welcome alternative.

**Tags**: `#rsync`, `#openbsd`, `#implementation`, `#macos`, `#file-sync`

---

<a id="item-8"></a>
## [Pope Leo's first encyclical criticizes technological messianism](https://www.economist.com/europe/2026/05/28/leos-first-encyclical-attacks-technological-messianism) ⭐️ 8.0/10

Pope Leo has released his first encyclical, which sharply criticizes technological messianism—the belief that technology will solve all human problems—and warns against replacing humans with artificial intelligence. This encyclical marks a significant intervention by a major religious leader in debates about AI ethics and the societal control of technology, potentially shaping public discourse and policy. The encyclical reportedly acknowledges the Pope's own use of technology even as it condemns unchecked faith in AI, highlighting a tension between embracing and cautioning against technological progress.

hackernews · 1vuio0pswjnm7 · May 30, 10:30 · [Discussion](https://news.ycombinator.com/item?id=48334710)

**Background**: Technological messianism is the conviction that technology will inevitably lead to positive outcomes and solve all problems. A papal encyclical is a formal letter from the Pope that outlines the Catholic Church's official position on important issues, carrying significant moral authority for believers.

<details><summary>References</summary>
<ul>
<li><a href="https://www.economist.com/europe/2026/05/28/leos-first-encyclical-attacks-technological-messianism">Leo’s first encyclical attacks technological messianism</a></li>
<li><a href="https://en.wikipedia.org/wiki/Papal_encyclical">Papal encyclical</a></li>

</ul>
</details>

**Discussion**: Commenters debated who should control technology—technologists, users, governments, or religious institutions—with some expressing skepticism about AI hype. Others referenced Peter Thiel's views on the Antichrist and questioned whether AI CEOs suffer from 'AI psychosis.'

**Tags**: `#AI`, `#ethics`, `#technology`, `#religion`, `#society`

---

<a id="item-9"></a>
## [Anthropic details sandboxing techniques for Claude across products](https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything) ⭐️ 8.0/10

Anthropic published a detailed blog post explaining how they sandbox Claude across Claude.ai, Claude Code, and Cowork using gVisor, Seatbelt, and Bubblewrap respectively. This documentation addresses a common trust gap in AI sandboxing by providing thorough details on containment strategies, which helps users and developers assess security risks and build confidence in deploying agentic AI. Claude.ai uses gVisor; Claude Code on macOS uses Apple's Seatbelt framework and on Linux uses Bubblewrap; Claude Cowork runs in a full virtual machine (Apple Virtualization on macOS, HCS on Windows). The post also describes past risks like the api.anthropic.com/v1/files exfiltration vector.

rss · Simon Willison · May 30, 21:36

**Background**: Sandboxing is a security technique that isolates applications to prevent them from affecting the host system or accessing unauthorized data. gVisor is an open-source application kernel developed by Google that implements many Linux system calls in userspace for stronger isolation than traditional containers. Seatbelt is Apple's sandboxing framework on macOS, and Bubblewrap is a lightweight Linux sandbox used by tools like Flatpak. Understanding these methods helps readers appreciate the layered security approach Anthropic employs.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GVisor">gVisor - Wikipedia</a></li>
<li><a href="https://wiki.archlinux.org/title/Bubblewrap">Bubblewrap - ArchWiki</a></li>
<li><a href="https://nono.sh/docs/cli/internals/seatbelt">macOS Seatbelt - Nono Docs</a></li>

</ul>
</details>

**Tags**: `#AI safety`, `#Claude`, `#sandboxing`, `#security`, `#Anthropic`

---

<a id="item-10"></a>
## [Debugger reveals training failures local to layers and steps](https://www.reddit.com/r/MachineLearning/comments/1trui0b/what_i_learned_building_a_debugger_for_pytorch/) ⭐️ 8.0/10

A PyTorch debugger called NeuralDBG was open-sourced, which hooks into training loops to automatically detect and localize failures such as vanishing gradients, exploding gradients, and data anomalies by monitoring per-layer gradient norm transitions. This changes failure diagnosis from relying on global loss curves to focusing on specific layers and steps, enabling faster and more precise debugging for ML engineers, potentially saving hours of training time. The tool extracts semantic events like 'gradient norm transitions' and 'first occurrence tracking' rather than raw tensors, making the output compact and actionable; a simple code snippet for per-layer gradient norm monitoring is provided as a practical takeaway.

reddit · r/MachineLearning · /u/ProgrammerNo8287 · May 30, 08:48

**Background**: Training deep learning models often suffers from failures like vanishing or exploding gradients, which are typically diagnosed by monitoring the loss curve. However, the loss is a global aggregate that obscures the root cause. Per-layer gradient norms provide a more localized signal, but raw norms are noisy; detecting transitions from healthy to anomalous values is key.

**Tags**: `#PyTorch`, `#debugging`, `#training failures`, `#deep learning`, `#gradient analysis`

---

<a id="item-11"></a>
## [NVIDIA NVFP4 Quantization of Qwen3.6-35B-A3B](https://www.reddit.com/r/LocalLLaMA/comments/1ts6j6j/nvidiaqwen3635ba3bnvfp4_hugging_face/) ⭐️ 8.0/10

NVIDIA has released a quantized version of the Qwen3.6-35B-A3B model using the NVFP4 data type, achieving approximately 3.06x reduction in memory requirements while maintaining nearly identical accuracy across benchmarks. This enables efficient deployment of large mixture-of-experts models on limited hardware, significantly lowering the barrier for running advanced LLMs locally. The minimal accuracy loss (e.g., MMLU Pro from 85.6 to 85.0) makes NVFP4 a practical choice for production use. Only the weights and activations of linear operators in transformer blocks within MoE are quantized, reducing bits per parameter from 16 to 4. The model is quantized using NVIDIA's Model Optimizer and is ready for inference with the vLLM engine.

reddit · r/LocalLLaMA · /u/pmttyji · May 30, 17:49

**Background**: Quantization reduces numerical precision of model weights to lower memory usage and speed up inference. NVFP4 is a floating-point format with shared exponent and compact mantissa, offering higher dynamic range than uniform INT4. The Qwen3.6-35B-A3B is a 35-billion parameter mixture-of-experts (MoE) model, where only a subset of experts is active per token, making it efficient yet memory-intensive. vLLM is a high-throughput inference engine that supports various quantization formats.

<details><summary>References</summary>
<ul>
<li><a href="https://build.nvidia.com/spark/nvfp4-quantization">NVFP4 Quantization | DGX Spark</a></li>
<li><a href="https://github.com/vllm-project/vllm">GitHub - vllm -project/ vllm : A high-throughput and memory ...</a></li>
<li><a href="https://arxiv.org/abs/2507.11181">[2507.11181] Mixture of Experts in Large Language Models</a></li>

</ul>
</details>

**Tags**: `#quantization`, `#nvidia`, `#qwen`, `#efficient inference`, `#model optimization`

---

<a id="item-12"></a>
## [GPU Specs Comparison for Local LLM Inference Challenges Mac Recommendations](https://www.reddit.com/r/LocalLLaMA/comments/1trkze4/i_compared_all_specs_of_the_major_gpusmachines/) ⭐️ 8.0/10

A Reddit user published a comprehensive comparison of major GPUs (including RTX PRO 6000, Intel Arc Pro B70, Radeon MI50, RTX 5070 Ti, etc.) for local LLM inference, analyzing price, FP16 TFLOPS, VRAM, bandwidth, and derived metrics like $/TFLOP and $/GB, arguing that Macs are overpriced for this use case. This data-driven comparison helps the local LLM community make more informed hardware purchasing decisions beyond brand bias, especially for those prioritizing prefill speed and total cost of ownership. The author highlights that memory bandwidth is often the bottleneck for LLM inference, and that prefill performance is neglected by common word-generation benchmarks; the table includes Max-Q variants for power efficiency and notes that some GPUs support 2x-4x faster FP16/BF16 via tensor cores.

reddit · r/LocalLLaMA · /u/Ok_Top9254 · May 30, 00:44

**Background**: For local LLM inference, key GPU specs include FP16 TFLOPS (computational throughput for half-precision), VRAM capacity (how large a model can fit), and memory bandwidth (speed of transferring data, often the primary bottleneck after the first token). Max-Q is NVIDIA's technology to optimize power and performance in workstation GPUs. The author uses derived metrics like $/TFLOP and $/GB to evaluate cost efficiency.

<details><summary>References</summary>
<ul>
<li><a href="https://ozyphus.github.io/gpu-maths.html">GPU Mathematics for Machine Learning - Interactive Guide</a></li>
<li><a href="https://www.adaline.ai/blog/understanding-gpu-for-inference-in-llms">Understanding GPU for Inference in LLMs | Adaline</a></li>
<li><a href="https://www.nvidia.com/en-sg/geforce/gaming-laptops/max-q-technologies/">Max-Q Technologies for Laptops | NVIDIA</a></li>

</ul>
</details>

**Tags**: `#GPU`, `#LLM`, `#hardware comparison`, `#local inference`, `#performance`

---

<a id="item-13"></a>
## [Parallax: Parameterized Local Linear Attention for LLMs](https://www.reddit.com/r/LocalLLaMA/comments/1ts79rg/parallax_parameterized_local_linear_attention_for/) ⭐️ 8.0/10

Researchers propose Parallax, a parameterized local linear attention mechanism that scales for large language model pretraining by removing numerical solvers and adding a learnable query-like projector to probe the KV covariance. This work offers a theoretically grounded improvement over standard softmax attention with provably better bias-variance tradeoffs, and demonstrates consistent perplexity gains at 0.6B and 1.7B scales, marking the first architecture-optimizer codesign for attention mechanisms. Parallax uses a hardware-aware algorithm that increases arithmetic intensity over FlashAttention, and its prototype decode kernel matches or outperforms FlashAttention 2/3 across various batch sizes and context lengths. The advantage persists under both parameter-matched and compute-matched controls, and the Muon optimizer is found to unlock Parallax's capacity.

reddit · r/LocalLLaMA · /u/Thrumpwart · May 30, 18:18

**Background**: Standard Transformer attention uses softmax, which is a local constant estimate in the test-time regression framework. Local Linear Attention (LLA) upgrades this to a local linear estimate, improving bias-variance tradeoffs but facing scalability issues due to numerical solvers. Parallax introduces a parameterized version that removes these solvers and learns a projector to the KV covariance, enabling efficient pretraining.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2605.29157">[2605.29157] Parallax: Parameterized Local Linear Attention for...</a></li>
<li><a href="https://openreview.net/pdf?id=WGpzi489XY">L ATTENTION : AN OPTIMAL INTERPO L SOFTMAX ATTENTION FOR EST-T R</a></li>

</ul>
</details>

**Tags**: `#attention mechanism`, `#LLM`, `#efficient attention`, `#language modeling`, `#machine learning research`

---

<a id="item-14"></a>
## [Huawei Proposes 'Tao Law' Using Temporal Scaling for Chips](https://t.me/zaihuapd/41648) ⭐️ 8.0/10

Huawei officially introduced the 'Tao Law' at the 2026 International Symposium on Circuits and Systems (ISCAS 2026), proposing temporal scaling to replace geometric scaling for semiconductor advancement. The company has already designed and mass-produced 381 chips based on this law, and plans to release a new Kirin chip using logic folding technology in autumn 2026. The Tao Law offers a new path for semiconductor development beyond Moore's Law, potentially overcoming physical scaling limits and reshaping the global chip industry. It marks the first time China has proposed a guiding principle for worldwide semiconductor evolution, with significant strategic implications. The Tao Law reduces the time constant τ to achieve multi-level co-optimization across devices, circuits, chips, and systems, aiming for transistor density equivalent to 1.4nm process by 2031. The logic folding technology is a true 3D chip design approach that goes beyond traditional 2D and pseudo-3D designs by optimizing interconnections at the logic gate level.

telegram · zaihuapd · May 30, 02:18

**Background**: Moore's Law states that transistor density doubles approximately every two years, but it is now approaching physical limits as transistor sizes shrink to atomic scales. Huawei's Tao Law introduces temporal scaling — reducing signal propagation delay — as an alternative to shrinking dimensions, maintaining performance gains through system-level co-optimization rather than relying solely on process node advancements.

<details><summary>References</summary>
<ul>
<li><a href="https://baike.baidu.com/item/时间缩微/67842555">时间缩微 _百度百科</a></li>
<li><a href="https://zhichai.net/topic/177620770">华为"韬定律"深度解读：从几何 缩微 到 时间缩微 的范式跃迁</a></li>
<li><a href="https://k.sina.com.cn/article_5953189932_162d6782c06704cr5a.html?cre=tianyi&mod=pcpager_tech&loc=12&r=0&rfunc=24&tj=cxvertical_pc_pager_spt&tr=12">k.sina.com.cn/article_5953189932_162d6782c06704cr5a.html?cre...</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#Huawei`, `#chip design`, `#Moore's Law`, `#innovation`

---