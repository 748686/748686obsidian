---
layout: default
title: "Horizon Summary: 2026-05-22 (EN)"
date: 2026-05-22
lang: en
---

> From 41 items, 11 important content pieces were selected

---

1. [Nvidia CEO: Nvidia Has Essentially Abandoned China AI Chip Market](#item-1) ⭐️ 9.0/10
2. [New Freenet Redesign Uses WebAssembly for Decentralized Apps](#item-2) ⭐️ 8.0/10
3. [Google Tests AI-Powered Ad Formats, Expands Direct Offers](#item-3) ⭐️ 8.0/10
4. [Indexing a Year of Video Locally with Gemma4-31B on MacBook](#item-4) ⭐️ 8.0/10
5. [Google's Antigravity IDE Bait-and-Switch](#item-5) ⭐️ 8.0/10
6. [Vivaldi 8.0 Released with New Features and Improvements](#item-6) ⭐️ 8.0/10
7. [GCC BPF support nears feature parity with LLVM](#item-7) ⭐️ 8.0/10
8. [Proposal: Private Memory Nodes for Linux Kernel](#item-8) ⭐️ 8.0/10
9. [Tesla Supervised FSD Launches in China](#item-9) ⭐️ 8.0/10
10. [OpenAI Plans IPO Filing as Early as This Week](#item-10) ⭐️ 8.0/10
11. [Tencent Launches OS-Level AI Assistant Marvis](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Nvidia CEO: Nvidia Has Essentially Abandoned China AI Chip Market](https://www.cnbc.com/2026/05/21/nvidia-jensen-huang-china-ai-chip-market-huawei.html) ⭐️ 9.0/10

Nvidia CEO Jensen Huang announced that the company has effectively abandoned the Chinese AI chip market due to US export restrictions, ceding the market to domestic competitors like Huawei. This marks a major shift in the global AI chip supply chain, as Nvidia's exit from China could accelerate Chinese self-sufficiency and reshape the competitive landscape for AI hardware. Huang stated that Nvidia has told investors not to expect licenses to sell advanced chips in China, and noted that Huawei's local chip ecosystem is very strong. Nvidia is now focusing on supporting supply chain expansion and has announced an $80 billion stock buyback.

telegram · zaihuapd · May 21, 05:52

**Background**: US export controls restrict the sale of advanced AI chips like Nvidia's H100 to China. Nvidia's H100 is a data center GPU based on the Hopper architecture, featuring Tensor Cores and Transformer Engine for AI training and inference. Meanwhile, Huawei has developed its Ascend AI chips, such as the Ascend 950 series, which are competitive with Nvidia's offerings in the Chinese market.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Nvidia_H100_GPU">Nvidia H100 GPU</a></li>
<li><a href="https://tech-insider.org/huawei-ascend-950pr-ai-chip-nvidia-china-2026/">Huawei Ascend 950PR: The 1.56 PFLOP AI Chip vs Nvidia [2026]</a></li>
<li><a href="https://www.huaweicentral.com/huawei-ascend-950-ai-chips-demand-surges/">Huawei Ascend 950 AI chips demand surges after DeepSeek V4 ...</a></li>

</ul>
</details>

**Tags**: `#Nvidia`, `#AI chips`, `#China`, `#export controls`, `#Huawei`

---

<a id="item-2"></a>
## [New Freenet Redesign Uses WebAssembly for Decentralized Apps](https://freenet.org/) ⭐️ 8.0/10

The original Freenet (now Hyphanet) has been completely redesigned and relaunched with a global decentralized key-value store where keys are WebAssembly contracts that define valid state, mutation rules, and a commutative merge operation for consistency. This approach offers a novel solution to the consistency problem in decentralized systems without requiring consensus protocols like blockchain, enabling fast state propagation (seconds) and allowing apps to be downloaded and run in browsers like single-page applications. Every contract must define a commutative merge operation, enabling state updates to spread like a virus and typically achieving global consistency in seconds. Early applications include River (group chat) and Delta (CMS), both available for desktop but not yet mobile.

hackernews · sanity · May 21, 14:34 · [Discussion](https://news.ycombinator.com/item?id=48223362)

**Background**: Freenet is a peer-to-peer file-sharing network originally launched in 2000, now renamed Hyphanet. WebAssembly (WASM) is a binary instruction format that runs in browsers and is used here for smart contracts. The commutative merge operation is a CRDT-like technique that ensures consistency without central coordination.

<details><summary>References</summary>
<ul>
<li><a href="https://interjectedfuture.com/a-simple-way-to-understand-crdts/">A simple way to understand CRDTs</a></li>
<li><a href="https://interjectedfuture.com/trade-offs-between-different-crdts/">Trade-offs between Different CRDTs</a></li>
<li><a href="https://gitplanet.com/label/p2p">Top p2p open source projects - GitPlanet</a></li>

</ul>
</details>

**Discussion**: The community expressed mixed reactions: some criticized the governance decision to force a rewrite without consulting the original team, while others engaged in technical debate about the merge function and suggested using update logs as an alternative. Concerns were also raised about 'ghost keys' relying on donations to Freenet rather than burning cryptocurrency.

**Tags**: `#p2p`, `#decentralized-apps`, `#webassembly`, `#blockchain-alternative`, `#freenet`

---

<a id="item-3"></a>
## [Google Tests AI-Powered Ad Formats, Expands Direct Offers](https://blog.google/products/ads-commerce/google-marketing-live-search-ads/) ⭐️ 8.0/10

Google announced at Google Marketing Live 2026 that it is integrating its Gemini AI into Search to create new conversational ad formats, including Conversational Discovery ads and AI-powered Shopping ads, and is expanding its Direct Offers pilot to more brands and users. These AI-generated ads could significantly alter the user experience by making ads more personalized and persuasive, raising ethical concerns about manipulation and the degradation of search utility as users may find it harder to distinguish organic results from sponsored content. The new formats leverage Gemini to write custom explainers for products based on user queries, and Direct Offers allows advertisers to surface real-time deals directly in search results; the pilot has been running since January 2026 with brands like Chewy, Gap, and L'Oreal.

hackernews · sofumel · May 21, 09:49 · [Discussion](https://news.ycombinator.com/item?id=48220105)

**Background**: Google Search has long displayed advertisements alongside organic results, but the introduction of generative AI (Gemini) marks a shift toward more conversational and context-aware ad experiences. Direct Offers is Google's first agentic ad format, aiming to bridge product research and purchase decisions automatically.

<details><summary>References</summary>
<ul>
<li><a href="https://blog.google/products/ads-commerce/google-marketing-live-search-ads/">New ad formats built with Gemini coming to Google Search</a></li>
<li><a href="https://www.luzern.co/direct-offers-googles-first-agentic-ad-format/">Direct Offers : Google ’s First Agentic Ad Format – Luzern</a></li>
<li><a href="https://searchengineland.com/google-tests-new-conversational-ad-formats-in-ai-mode-and-search-478115">Google tests new conversational ad formats in AI Mode and Search</a></li>

</ul>
</details>

**Discussion**: Community comments express strong concern that AI-generated ads will manipulate users more effectively, with one user calling it 'the essence of the evil of AI ads.' Others worry about Google gathering training data to influence people even when they know they are being influenced, and some predict search will become essentially useless.

**Tags**: `#ads`, `#Google Search`, `#AI`, `#privacy`, `#SEO`

---

<a id="item-4"></a>
## [Indexing a Year of Video Locally with Gemma4-31B on MacBook](https://blog.simbastack.com/indexed-a-year-of-video-locally/) ⭐️ 8.0/10

A developer successfully indexed one year's worth of personal video footage on a 2021 MacBook by running Gemma4-31B, a 31-billion-parameter multimodal model, entirely locally using 50GB of swap memory. This demonstrates that powerful local LLMs can handle practical, memory-intensive tasks like video indexing without cloud dependency, paving the way for private, offline personal archiving tools. The model runs at 4-bit quantization, requiring about 19 GiB for weights, but the author reports 28.4 GiB usage due to context and other apps; SSD wear is a concern due to heavy swap usage.

hackernews · asenna · May 21, 14:01 · [Discussion](https://news.ycombinator.com/item?id=48222733)

**Background**: Gemma4-31B is an open multimodal model from Google DeepMind that can process video as sequences of frames. Local LLM video indexing involves extracting frames, generating descriptions with the model, and building a searchable index. A MacBook with limited RAM uses swap (disk space as virtual memory) to accommodate large models, which can accelerate SSD wear.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/google/gemma-4-31B">google/gemma-4-31B · Hugging Face</a></li>
<li><a href="https://medium.com/@bSharpML/use-llamaindex-and-a-local-llm-to-summarize-youtube-videos-29817440e671">Use LlamaIndex and a Local LLM to Summarize YouTube Videos</a></li>

</ul>
</details>

**Discussion**: Commenters discussed sharing the skill files and a GitHub repo (framedex) for the project. Concerns were raised about SSD wear from heavy swapping, and suggestions were made to reduce memory usage via quantization and freeing other apps. Some users shared their own experiences running similar models on older hardware with upgraded memory.

**Tags**: `#local LLM`, `#video indexing`, `#Gemma4`, `#memory management`, `#personal archiving`

---

<a id="item-5"></a>
## [Google's Antigravity IDE Bait-and-Switch](https://www.0xsid.com/blog/antigravity-bait-n-switch) ⭐️ 8.0/10

Google replaced the original VSCode-based Antigravity IDE with a different agent-first platform in a controversial update, confusing existing users who were not adequately informed. This bait-and-switch undermines developer trust and highlights Google's inconsistent product strategy, potentially pushing users to more reliable competitors in the AI-assisted coding market. The original Antigravity was a lightweight VSCode reskin with AI features, whereas the 2.0 update replaced it with a standalone agentic platform, breaking existing workflows and integrations.

hackernews · ssiddharth · May 21, 13:50 · [Discussion](https://news.ycombinator.com/item?id=48222529)

**Background**: Google Antigravity is an AI-powered IDE focused on agentic development. The 'bait-and-switch' refers to a product update that fundamentally changed the IDE's nature without clear communication, causing backlash from users who relied on the original tool. Such shifts damage user trust and reflect poorly on Google's long-term commitment to developer tools.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Antigravity">Google Antigravity - Wikipedia</a></li>
<li><a href="https://antigravity.google/">Google Antigravity</a></li>

</ul>
</details>

**Discussion**: Users expressed frustration, with some providing workarounds to restore old functionality. Others criticized Google's lack of focus and compared it unfavorably to other AI labs that maintain clearer product identities.

**Tags**: `#Google`, `#Antigravity`, `#IDE`, `#developer tools`, `#bait-and-switch`

---

<a id="item-6"></a>
## [Vivaldi 8.0 Released with New Features and Improvements](https://vivaldi.com/blog/vivaldi-on-desktop-8-0/) ⭐️ 8.0/10

Vivaldi 8.0 has been released for desktop, introducing new features and improvements such as enhanced Workspaces, no bundled AI, and a major version bump. As a popular alternative browser, Vivaldi 8.0 continues to attract users seeking privacy and customization, sparking debate about its partially closed-source model versus usability advantages. Approximately 92% of Vivaldi's code is open-source from Chromium, 3% is open-source from Vivaldi, and only 5% (the UI) is closed-source, which can be modified via CSS. The 8.0 release does not include AI features, a relief for some users.

hackernews · OuterVale · May 21, 07:21 · [Discussion](https://news.ycombinator.com/item?id=48219060)

**Background**: Vivaldi is a web browser based on Chromium, known for its high customizability and built-in features like tab stacking and workspaces. It is free to use but unlike many Chromium-based browsers, its user interface is partially closed-source, which has drawn criticism from open-source advocates.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Vivaldi_(web_browser)">Vivaldi (web browser) - Wikipedia</a></li>
<li><a href="https://vivaldi.com/blog/technology/why-isnt-vivaldi-browser-open-source/">Why isn’t Vivaldi browser open-source? | Vivaldi Browser</a></li>

</ul>
</details>

**Discussion**: The community discussion highlights mixed views: some praise Vivaldi's superior UX (e.g., workspaces hiding tabs until needed) and print functionality, while others express concern over data collection or the closed-source model, preferring alternatives like Brave or Firefox. One long-time user expressed relief that no AI was added.

**Tags**: `#Vivaldi`, `#Browser`, `#Privacy`, `#Open Source`, `#Web Browsers`

---

<a id="item-7"></a>
## [GCC BPF support nears feature parity with LLVM](https://lwn.net/Articles/1071973/) ⭐️ 8.0/10

At the 2026 LSFMM+BPF Summit, GCC BPF developers reported that GCC 16.1, released on April 30, 2026, now passes 601 out of 713 kernel BPF self-tests, approaching feature parity with LLVM. The GNU toolchain now includes BPF support across GCC, binutils, DejaGNU, GNU poke, and GDB, though some components like GDB's simulator are outdated. This milestone reduces the kernel's dependency on LLVM for BPF compilation, promoting toolchain diversity and freedom for Linux distributions. It also strengthens the GNU toolchain's relevance for eBPF development, which is critical for modern Linux networking, observability, and security. A small set of remaining fixes is needed for GCC to pass all kernel BPF self-tests; most failing tests share common root causes. GCC also has work-in-progress support for Solana's BPF variant, which includes 64-bit product, quotient, and remainder instructions that could benefit upstream BPF.

rss · LWN.net · May 21, 14:52

**Background**: BPF (Berkeley Packet Filter), specifically its extended version eBPF, allows running sandboxed programs in the Linux kernel without changing kernel source code, used for networking, tracing, and security. LLVM has historically been the primary compiler for BPF; GCC's BPF backend aims to provide a mature alternative, reducing reliance on a single toolchain. The LSFMM+BPF Summit is an annual invitation-only event where kernel developers discuss storage, filesystem, memory management, and BPF topics.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Berkeley_Packet_Filter">Berkeley Packet Filter - Wikipedia</a></li>
<li><a href="https://gcc.gnu.org/wiki/BPFBackEnd">BPFBackEnd - GCC Wiki</a></li>
<li><a href="https://events.linuxfoundation.org/lsfmmbpf/">Linux Storage, Filesystem, MM & BPF Summit | LF Events</a></li>

</ul>
</details>

**Tags**: `#GCC`, `#BPF`, `#Linux kernel`, `#LLVM`, `#toolchain`

---

<a id="item-8"></a>
## [Proposal: Private Memory Nodes for Linux Kernel](https://lwn.net/Articles/1072881/) ⭐️ 8.0/10

Gregory Price proposed making NUMA memory nodes private to specific processes at the 2026 Linux Storage, Filesystem, Memory Management, and BPF Summit, aiming to restrict access to device-attached memory such as compressed RAM. This feature would enable more efficient use of specialized memory devices (e.g., accelerators, smart NICs) by preventing the kernel's buddy allocator from falling back to them, potentially improving performance and security. It also addresses a growing challenge as heterogeneous memory architectures proliferate. Price's preferred solution adds a __GFP_PRIVATE allocation flag, allowing fallback to ordinary RAM if private node memory is unavailable. However, he noted that existing kernel code using for_each_online_node() loops can still accidentally allocate from private nodes, making the approach fragile.

rss · LWN.net · May 21, 13:22

**Background**: NUMA (Non-Uniform Memory Access) systems categorize memory into nodes based on access latency; typically, any process can allocate from any node. Devices like CXL memory expanders or compressed RAM (zram) attach large memory pools, but the kernel's buddy allocator may treat them as general-purpose RAM, causing unwanted usage. Private memory nodes would restrict allocation to only explicitly authorized processes.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Non-uniform_memory_access">Non-uniform memory access - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Zram">zram - Wikipedia</a></li>

</ul>
</details>

**Discussion**: David Hildenbrand questioned the correctness of the for_each_online_node() pattern, while John Hubbard noted that the code was correct when written but the world has changed. Kiryl Shutsemau argued that fixing broken allocation patterns would be better than adding a new flag, but Price countered that fixing all such patterns could take years.

**Tags**: `#Linux kernel`, `#memory management`, `#NUMA`, `#LSFMM+BPF`, `#private memory nodes`

---

<a id="item-9"></a>
## [Tesla Supervised FSD Launches in China](https://x.com/i/status/2057226337010745348) ⭐️ 8.0/10

Tesla announced on X that its supervised Full Self-Driving (FSD) system is now available in China. This marks a significant expansion of Tesla's autonomous driving technology into the world's largest automotive market, potentially accelerating FSD adoption globally. The announcement lacks technical specifics such as regulatory approvals or feature differences from the US version. FSD (Supervised) still requires constant driver attention.

telegram · zaihuapd · May 21, 01:34

**Background**: Tesla's Full Self-Driving (Supervised) is an advanced driver-assistance system that handles many driving tasks but requires an attentive driver ready to intervene. It includes navigation on most roads, self-parking, and summon features. The system has been available in North America and is now expanding to China.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Tesla_Autopilot">Tesla Autopilot - Wikipedia</a></li>
<li><a href="https://www.tesla.com/support/fsd">Full Self-Driving (Supervised) | Tesla Support</a></li>

</ul>
</details>

**Tags**: `#autonomous driving`, `#Tesla`, `#FSD`, `#China`

---

<a id="item-10"></a>
## [OpenAI Plans IPO Filing as Early as This Week](https://www.wsj.com/tech/ai/openai-is-preparing-to-file-for-an-ipo-very-soon-0ec95af5) ⭐️ 8.0/10

OpenAI is preparing to confidentially file for an IPO as early as this week, targeting a September listing, and has hired Goldman Sachs and Morgan Stanley to draft the prospectus. An OpenAI IPO would be a landmark event for the AI industry, signaling the transition of leading AI companies from private to public markets and potentially reshaping investment in artificial intelligence. The company recently won a legal dispute with Elon Musk, removing a key obstacle to going public, but still faces challenges such as high data center costs and competition from Anthropic. Musk plans to appeal, so the timeline remains uncertain.

telegram · zaihuapd · May 21, 04:08

**Background**: A confidential IPO filing allows companies to submit their draft registration statement to the SEC without public disclosure, giving them flexibility to test market reception. Anthropic, founded by former OpenAI employees, is a key competitor in the AI safety space and develops the Claude model family. OpenAI's potential IPO comes amid a rapid AI arms race with massive capital expenditures.

<details><summary>References</summary>
<ul>
<li><a href="https://www.valuethemarkets.com/education/what-is-a-confidential-ipo-filing">What is a Confidential IPO Filing? | Confidential IPOs</a></li>
<li><a href="https://en.wikipedia.org/wiki/Anthropic">Anthropic - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#OpenAI`, `#IPO`, `#AI`, `#Business`

---

<a id="item-11"></a>
## [Tencent Launches OS-Level AI Assistant Marvis](https://finance.sina.com.cn/jjxw/2026-05-21/doc-inhyrmmu5949795.shtml) ⭐️ 8.0/10

On May 21, Tencent officially launched Marvis, a system-level AI assistant that integrates with Windows, Mac, and Android. It is available for free with 10 million daily tokens and requires no invitation code. This launch represents a significant step in embedding AI deeply into operating systems, potentially transforming how users interact with their devices. The local privacy mode addresses growing concerns about data security and could set a new standard for AI assistants. Marvis features a six-agent team led by a main agent that coordinates specialized sub-agents for parallel task execution. The privacy mode uses an on-device large language model, ensuring all data processing stays local and works even offline.

telegram · zaihuapd · May 21, 10:00

**Background**: AI middleware serves as an abstraction layer between applications and system resources, enabling seamless AI integration. On-device large language models (LLMs) are lightweight models that run locally on devices, offering privacy benefits but typically with limited capabilities compared to cloud models. Tencent's Marvis combines these concepts to create an OS-level AI assistant.

<details><summary>References</summary>
<ul>
<li><a href="https://news.aibase.com/news/28191">Tencent Marvis Launches Officially: System-Level AI Assistant , Six...</a></li>
<li><a href="https://kr-asia.com/pulses/162131">Tencent launches Marvis AI assistant</a></li>
<li><a href="https://grokipedia.com/page/On-device_large_language_model">On-device large language model</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Operating System`, `#Tencent`, `#Privacy`, `#Multi-Agent`

---