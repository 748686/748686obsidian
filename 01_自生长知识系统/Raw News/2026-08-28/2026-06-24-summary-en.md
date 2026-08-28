---
layout: default
title: "Horizon Summary: 2026-06-24 (EN)"
date: 2026-06-24
lang: en
---

> From 34 items, 10 important content pieces were selected

---

1. [Unlimited OCR: One-shot Long-horizon Parsing with Constant KV Cache](#item-1) ⭐️ 9.0/10
2. [CXMT Set to Challenge DRAM Leaders with IPO and HBM Push](#item-2) ⭐️ 9.0/10
3. [China's 'LineShine' Supercomputer Tops TOP500 with 2.198 ExaFLOPS](#item-3) ⭐️ 9.0/10
4. [TikZ Editor: WYSIWYG Tool for LaTeX Figures](#item-4) ⭐️ 8.0/10
5. [The Inevitable Spec Loop in AI Coding](#item-5) ⭐️ 8.0/10
6. [KASAN Support for BPF JIT Compiler](#item-6) ⭐️ 8.0/10
7. [Nearly Half of LG Smart TV Apps Contain Residential Proxy SDKs](#item-7) ⭐️ 8.0/10
8. [OpenAI Produces AI Animated Film 'Critterz' with GPT-5](#item-8) ⭐️ 8.0/10
9. [US humanoid robots rely on Chinese supply chain for key parts](#item-9) ⭐️ 8.0/10
10. [Critical FFmpeg Bug Allows Remote Code Execution via Video Files](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Unlimited OCR: One-shot Long-horizon Parsing with Constant KV Cache](https://github.com/baidu/Unlimited-OCR) ⭐️ 9.0/10

Baidu researchers introduced Unlimited OCR, a method that uses a clever architectural trick (R-SWA) to keep the KV cache size fixed during long document parsing, enabling one-shot processing of hundreds of pages without running out of memory. This overcomes the fundamental memory bottleneck in long-document OCR, enabling much longer context windows without expensive hardware, which could significantly improve applications like document digitization, RAG, and automated data extraction. The key innovation is R-SWA (Restricted Sliding Window Attention), which restricts attention to a sliding window and uses a special prefill strategy to maintain a constant KV cache size, regardless of input length. The model can process tens to hundreds of pages in a single forward pass and parse continuously from first page to last without growing memory.

hackernews · ingve · Jun 23, 11:35 · [Discussion](https://news.ycombinator.com/item?id=48643426)

**Background**: Traditional OCR systems process document pages independently, losing cross-page context. Transformer-based models use a KV cache to store previously computed key-value pairs for attention, which grows linearly with input length, causing out-of-memory errors for long documents. This limitation forces developers to chunk documents into small pieces, compromising contextual understanding. Unlimited OCR proposes an architecture that maintains a fixed-size KV cache, enabling true one-shot parsing of long documents.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/baidu/Unlimited-OCR">GitHub - baidu/Unlimited-OCR: Unlimited OCR Works: Welcome the Era of One-shot Long-horizon Parsing. · GitHub</a></li>
<li><a href="https://arxiv.org/pdf/2606.23050">Unlimited OCR Works Welcome the Era of One-shot Long-horizon Parsing Baidu Inc.</a></li>
<li><a href="https://news.ycombinator.com/item?id=48643426">Unlimited OCR: One-Shot Long-Horizon Parsing | Hacker News</a></li>

</ul>
</details>

**Discussion**: The community response is highly positive, with many praising the clever architectural hack. Commenters note the practical significance for long-document processing, with some sharing related experiences in music scanning and local OCR. The acknowledgment of prior work (Deepseek-OCR, PaddleOCR) is also appreciated.

**Tags**: `#OCR`, `#deep learning`, `#memory optimization`, `#natural language processing`, `#document analysis`

---

<a id="item-2"></a>
## [CXMT Set to Challenge DRAM Leaders with IPO and HBM Push](https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram) ⭐️ 9.0/10

China's ChangXin Memory Technologies (CXMT) is preparing for an IPO and ramping up competition with Samsung, SK Hynix, and Micron in the DRAM market, particularly in High Bandwidth Memory (HBM) and wafer capacity expansion. This move could reshape the global DRAM landscape, reduce China's reliance on foreign memory chips, and impact AI hardware supply chains that depend on HBM. CXMT reportedly generated $8 billion in memory revenue and is working on HBM3 production, while facing a process node deficit compared to established rivals.

rss · Semianalysis · Jun 23, 14:51

**Background**: DRAM is a type of volatile memory used in computers and servers. HBM is a high-performance 3D-stacked DRAM technology critical for AI accelerators like NVIDIA GPUs. Currently, Samsung, SK Hynix, and Micron dominate the DRAM market, with CXMT as a rising Chinese challenger.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ChangXin_Memory_Technologies">ChangXin Memory Technologies - Wikipedia</a></li>
<li><a href="https://www.abhs.in/blog/china-cxmt-memory-chip-8-billion-revenue-hbm3-samsung-micron-2026">China's CXMT Hit $8 Billion in Memory Revenue — HBM3 Production...</a></li>

</ul>
</details>

**Tags**: `#DRAM`, `#semiconductor`, `#China`, `#memory`, `#geopolitics`

---

<a id="item-3"></a>
## [China's 'LineShine' Supercomputer Tops TOP500 with 2.198 ExaFLOPS](https://news.mydrivers.com/1/1131/1131573.htm) ⭐️ 9.0/10

On June 23, 2026, the TOP500 list placed China's 'LineShine' supercomputer at number one with 2.198 ExaFLOPS HPL performance, making it the first pure-CPU system to exceed 2 ExaFLOPS. This marks China's return to the top supercomputing spot after eight years, signaling a shift toward pure-CPU exascale architecture and reducing reliance on GPU accelerators for high-performance computing. The system uses 20,480 nodes, each with two LX2 processors (ARMv9, 304 cores each), totaling nearly 14 million CPU cores, with a power consumption of 42.2 MW and an efficiency of 52.07 GigaFLOPS/W.

telegram · zaihuapd · Jun 23, 15:30

**Background**: The TOP500 list ranks the world's most powerful supercomputers by their performance on the HPL benchmark. ExaFLOPS (10^18 floating-point operations per second) is a milestone for exascale computing. Most recent exascale systems rely on GPU accelerators, but LineShine achieves it with only CPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://x.com/Compute_King/status/2069348374609080753">更多的资料： LineShine超级计算机由深圳国家超级计算中心（NSCC-SZ）...</a></li>
<li><a href="https://tech.ifeng.com/c/8tCEPugIDxu">245万个CPU核心，中国超算“灵晟”突破2EFlops_凤凰网</a></li>

</ul>
</details>

**Tags**: `#supercomputing`, `#TOP500`, `#HPC`, `#China`, `#exascale`

---

<a id="item-4"></a>
## [TikZ Editor: WYSIWYG Tool for LaTeX Figures](https://tikz.dev/editor/) ⭐️ 8.0/10

An open-source WYSIWYG editor for TikZ figures has been released, allowing users to visually edit TikZ source code by dragging and resizing elements while keeping the source code and rendered figure in sync. This editor significantly simplifies the process of creating and modifying TikZ figures, which is traditionally done by manually tweaking coordinates and recompiling, saving time for researchers and academics who use LaTeX extensively. The editor works by parsing TikZ code and tracking exact source locations of objects, allowing it to override only numeric values when elements are moved. It was built primarily using the Codex AI coding agent, costing around $500 in ChatGPT subscription fees.

hackernews · DominikPeters · Jun 23, 14:24 · [Discussion](https://news.ycombinator.com/item?id=48645437)

**Background**: TikZ is a powerful LaTeX package for creating vector graphics, commonly used in academic papers. Traditionally, users write TikZ code manually and recompile to see results, which can be tedious. This editor provides real-time visual feedback and bidirectional editing.

<details><summary>References</summary>
<ul>
<li><a href="https://tikz.org/">LaTeX Graphics with TikZ</a></li>

</ul>
</details>

**Discussion**: The community praised the project's UI and concept but criticized that the generated TikZ code relies heavily on absolute coordinates, which is atypical for TikZ. Some suggested alternatives like quiver.app for specialized diagrams, and one commenter noted the high cost of AI tokens used.

**Tags**: `#TikZ`, `#LaTeX`, `#editor`, `#WYSIWYG`, `#open-source`

---

<a id="item-5"></a>
## [The Inevitable Spec Loop in AI Coding](https://lucumr.pocoo.org/2026/6/23/the-coming-loop/) ⭐️ 8.0/10

The author introduces the concept of 'The Coming Loop', an inevitable iterative process of clarifying specifications when using AI coding agents, shifting software development towards a spec-driven model. This insight highlights a paradigm shift where developers transition from coders to spec architects and reviewers, significantly impacting productivity and the nature of software design in the age of AI agents. The core bottleneck becomes specification clarity, not code generation; the loop involves repeated refinement of specs until they are precise enough for AI agents to implement correctly, often requiring multiple iterations.

hackernews · ingve · Jun 23, 11:06 · [Discussion](https://news.ycombinator.com/item?id=48643180)

**Background**: AI coding agents are tools that autonomously write, modify, and debug code from natural language prompts. Spec-driven development (SDD) is a 2026 methodology where executable specifications become the source of truth, with AI generating code from them. The 'coming loop' describes the feedback cycle where ambiguous specs cause repeated back-and-forth, making spec writing the critical skill.

<details><summary>References</summary>
<ul>
<li><a href="https://agentic.ai/best/coding-agents">18 Best AI Coding Agents in 2026 — Agentic.ai</a></li>
<li><a href="https://thebcms.com/blog/spec-driven-development">Spec-Driven Development (SDD): The Definitive 2026 Guide</a></li>
<li><a href="https://developer.microsoft.com/blog/spec-driven-development-spec-kit">Diving Into Spec-Driven Development With GitHub Spec Kit What is Spec-Driven Development? | Spec Kit Documentation spec-kit/spec-driven.md at main · github/spec-kit · GitHub Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl Spec-Driven Development: A Spec-First Approach to AI-Native ... Spec-Driven Development</a></li>

</ul>
</details>

**Discussion**: Commenters agree that the spec loop is real and often a bottleneck. One notes that clarity requires upfront thinking that cannot be accelerated by AI. Another sees this as a shift toward treating software like a living system. A third states that writing clear specs is the main challenge, with agents performing well when specs are good.

**Tags**: `#AI agents`, `#software development`, `#paradigm shift`, `#spec-driven development`, `#LLM tools`

---

<a id="item-6"></a>
## [KASAN Support for BPF JIT Compiler](https://lwn.net/Articles/1077740/) ⭐️ 8.0/10

Alexis Lothoré is adding Kernel Address Sanitizer (KASAN) support to the BPF just-in-time (JIT) compiler to detect use-after-free and out-of-bounds errors in JIT-generated code. He presented the work at the 2026 Linux Storage, Filesystem, Memory-Management, and BPF Summit. This improves kernel security by enabling KASAN to catch memory bugs in BPF JIT code, which previously bypassed instrumentation. It is significant for kernel testing and reliability, as BPF is widely used for networking, tracing, and security. Currently, the patch targets only the LDX and STX BPF instructions (loads and stores) on x86, ignoring stack accesses. The overhead is substantial, turning one instruction into twelve due to register save/restore, but optimizations like inlining __asan*() functions are being considered.

rss · LWN.net · Jun 23, 15:53

**Background**: KASAN is a dynamic memory error detector in the Linux kernel that identifies use-after-free and out-of-bounds accesses using software or hardware memory tagging. The BPF JIT compiler translates BPF bytecode into native machine code for performance; previously, it emitted direct pointer dereferences without KASAN checks. Adding KASAN instrumentation to the JIT ensures that JIT-generated code is also monitored.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.kernel.org/dev-tools/kasan.html">Kernel Address Sanitizer (KASAN) — The Linux Kernel</a></li>
<li><a href="https://sysctl-explorer.net/net/core/bpf_jit_enable/">bpf_jit_enable | sysctl-explorer.net</a></li>

</ul>
</details>

**Discussion**: During the talk, audience members suggested that inlining __asan*() functions could reduce overhead from register save/restore, but Lothoré noted that naive inlining might be worse. Others asked why not instrument the compiler or verifier, which Lothoré explained would require a stable KASAN API and complicate testing. No bugs have been found yet because the patch hasn't been widely tested.

**Tags**: `#kernel`, `#BPF`, `#KASAN`, `#JIT`, `#memory safety`

---

<a id="item-7"></a>
## [Nearly Half of LG Smart TV Apps Contain Residential Proxy SDKs](https://spur.us/blog/smart-tv-apps-residential-proxy-sdks) ⭐️ 8.0/10

A security scan found that 2,058 out of 6,038 sampled LG and Samsung smart TV apps include residential proxy SDKs, with LG accounting for nearly half. These apps, such as screensavers and games, can continue running proxy functions even after being closed. This exposes a widespread privacy risk where home IP addresses can be hijacked for proxy networks without user consent, potentially enabling malicious activities like fraud or content scraping. It highlights a critical IoT security gap that major TV manufacturers have not yet addressed. The affected apps include screensavers, clocks, and casual games; some remain active after closure. Amazon and Roku have already banned such SDKs on their platforms, while LG and Samsung have not publicly implemented equivalent restrictions.

telegram · zaihuapd · Jun 23, 02:26

**Background**: A residential proxy is an IP address assigned by an internet service provider to a real household, often used for anonymity or bypassing geographic restrictions. Residential proxy SDKs embedded in smart TV apps can turn the TV into a node in a proxy network, allowing third parties to route traffic through the home IP. This potentially exposes users to legal liability if the IP is used for illegal activities, and degrades network performance.

<details><summary>References</summary>
<ul>
<li><a href="https://segmentfault.com/a/1190000047344538">什么是住宅代理（Residential Proxy）？详解原理、优势与应用场景</a></li>
<li><a href="https://blog.csdn.net/2303_78381320/article/details/161290563">住宅IP代理详解：工作原理、类型与使用场景选型指南（2026）-CSDN博客</a></li>

</ul>
</details>

**Tags**: `#smart-tv`, `#security`, `#privacy`, `#IoT`, `#residential-proxy`

---

<a id="item-8"></a>
## [OpenAI Produces AI Animated Film 'Critterz' with GPT-5](https://t.me/zaihuapd/42125) ⭐️ 8.0/10

OpenAI is supporting the production of an animated feature film titled 'Critterz', primarily using its own AI tools including GPT-5, with a budget of under $30 million and a production timeline of just 9 months. This project demonstrates the potential of AI to dramatically reduce the cost and time required for feature-length animation, potentially disrupting the traditional animation industry and opening new possibilities for independent creators. The film is scheduled to premiere at the Cannes Film Festival and will be released globally in 2026. The budget and timeline are significantly lower than traditional animated films, which often cost over $100 million and take 3-5 years.

telegram · zaihuapd · Jun 23, 03:11

**Background**: GPT-5 is the fifth-generation multimodal large language model from OpenAI, launched in August 2025, capable of processing text, images, and more. AI in animation involves using machine learning to automate tasks like motion generation, character consistency, and scene rendering, which traditionally require extensive manual labor. OpenAI's support for 'Critterz' showcases an end-to-end AI-driven production pipeline.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GPT-5">GPT-5 - Wikipedia</a></li>
<li><a href="https://www.neolemon.com/blog/ai-storyboard-to-animation-pipeline-workflow/">AI Storyboard To Animation Pipeline: Complete Workflow GitHub - calesthio/OpenMontage: World's first open-source ... AI Animation in Blender: Complete Guide (2026) | 3D-Agent AI in Animation: Tools, Uses & Future Trends Animation pipeline: key steps, challenges and tools | LucidLink Where AI Fits in an Animation Pipeline: Pre-Production ... How Pixar’s Animation Pipeline Has Evolved with AI</a></li>

</ul>
</details>

**Tags**: `#OpenAI`, `#AI film`, `#GPT-5`, `#animation`, `#creative AI`

---

<a id="item-9"></a>
## [US humanoid robots rely on Chinese supply chain for key parts](https://t.me/zaihuapd/42129) ⭐️ 8.0/10

The Wall Street Journal reported that US humanoid robot manufacturers are increasingly dependent on Chinese suppliers for critical components such as motors, joints, magnets, and sensors, and that China produced 28 new humanoid robot models in 2025, nearly three times the number of US firms. This dependency underscores a growing strategic vulnerability for the US robotics industry, as China's cost advantages (estimated by Morgan Stanley to reduce manufacturing costs by up to two-thirds) could shift competitive dynamics and prompt US lawmakers to consider legislative measures to assess risks. Disney's 'Olaf' robots use components from China's Unitree Robotics and Tesla is cooperating with Chinese suppliers to prepare for mass production of Optimus. A bipartisan bill introduced in February 2025 aims to evaluate US robotics competitiveness and supply chain risks.

telegram · zaihuapd · Jun 23, 07:47

**Background**: Humanoid robots are designed to resemble and mimic human movements, requiring precision motors, joints, magnets, and sensors for dexterity. The US and China are key competitors in this emerging field, with China leveraging its established electronics and manufacturing supply chains to achieve lower costs and faster iteration.

**Tags**: `#robotics`, `#supply chain`, `#US-China relations`, `#humanoid robots`, `#technology competition`

---

<a id="item-10"></a>
## [Critical FFmpeg Bug Allows Remote Code Execution via Video Files](https://cybernews.com/security/critical-ffmpeg-vulnerability-enables-complete-compromise/) ⭐️ 8.0/10

FFmpeg disclosed a critical vulnerability (CVE-2026-8461, codenamed PixelSmash) in the MagicYUV decoder, enabling remote code execution via crafted video files. The flaw is fixed in version 8.1.2 released urgently. With FFmpeg embedded in countless media players, servers, and IoT devices, unpatched systems are at risk of complete compromise through seemingly innocuous video files. This high-severity flaw (CVSS 8.8) demands immediate updates across the ecosystem. The vulnerability is a heap out-of-bounds write in FFmpeg's libavcodec component, triggered by maliciously crafted MagicYUV-encoded videos. Attackers can exploit it not only via direct playback but also through thumbnail generation or media library scanning, with minimal traces.

telegram · zaihuapd · Jun 23, 15:00

**Background**: FFmpeg is a widely used open-source multimedia library that powers video processing in applications like VLC, Jellyfin, Kodi, and OBS. The MagicYUV decoder handles a lossless video codec. A heap out-of-bounds write occurs when data is written outside the allocated memory region, potentially allowing code execution or system crashes.

<details><summary>References</summary>
<ul>
<li><a href="https://www.securityweek.com/ffmpeg-pixelsmash-flaw-allows-rce-on-video-players-media-servers-nas-appliances/">FFmpeg PixelSmash Flaw Allows RCE on Video Players, Media ...</a></li>
<li><a href="https://undercodenews.com/pixelsmash-exposes-a-hidden-threat-how-one-ffmpeg-flaw-could-turn-everyday-video-files-into-remote-attack-weapons/">PixelSmash Exposes a Hidden Threat: How One FFmpeg Flaw Could ...</a></li>
<li><a href="https://cybersecuritynews.com/ffmpeg-vulnerability-weaponize-media-files/">Critical FFmpeg Vulnerability Allows Attackers to Weaponize ...</a></li>

</ul>
</details>

**Tags**: `#FFmpeg`, `#security vulnerability`, `#remote code execution`, `#CVE`, `#multimedia`

---