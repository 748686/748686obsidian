---
layout: default
title: "Horizon Summary: 2026-06-23 (EN)"
date: 2026-06-23
lang: en
---

> From 25 items, 13 important content pieces were selected

---

1. [Valve's Steam Machine Officially Launches Today](#item-1) ⭐️ 9.0/10
2. [Free-threaded Python: past, present, and future](#item-2) ⭐️ 9.0/10
3. [Moebius: 0.2B image inpainting model with 10B-level performance](#item-3) ⭐️ 8.0/10
4. [Police Chiefs Stalking Women With Flock LPRs Shows Warrant Need](#item-4) ⭐️ 8.0/10
5. [Mitchell pledges $400k to Zig Software Foundation](#item-5) ⭐️ 8.0/10
6. [Deno Desktop Launches with Multi-Backend Webview Framework](#item-6) ⭐️ 8.0/10
7. [Claude Code 'Extended Thinking' Is a Lossy Reasoning Summary](#item-7) ⭐️ 8.0/10
8. [Nearly half of LG smart TV apps contain residential proxy SDKs](#item-8) ⭐️ 8.0/10
9. [Moebius image inpainting model ported to browser with Claude Code](#item-9) ⭐️ 8.0/10
10. [First preview of Xfce's Wayland compositor xfwl4](#item-10) ⭐️ 8.0/10
11. [OSPM 2026 Day One: Idle States, sched_ext, Lock-Holder Preemption](#item-11) ⭐️ 8.0/10
12. [Micron plans $200B expansion to ease AI memory shortage](#item-12) ⭐️ 8.0/10
13. [48 Chinese Developers Sue Apple Over China App Store Monopoly](#item-13) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Valve's Steam Machine Officially Launches Today](https://store.steampowered.com/news/group/45479024/view/685257114654870245) ⭐️ 9.0/10

Valve launched the Steam Machine, a new living room console powered by a custom AMD chip, with a fair reservation system that randomizes order instead of rewarding fastest signups. This launch marks Valve's first major console entry, challenging Sony and Microsoft in the living room while promoting open hardware and Linux gaming. The Steam Machine boasts over six times the horsepower of the Steam Deck and is capable of 4K gaming. It runs SteamOS but allows users to install other operating systems or apps.

hackernews · theschwa · Jun 22, 17:09 · [Discussion](https://news.ycombinator.com/item?id=48632884)

**Background**: Steam Machine is Valve's answer to traditional gaming consoles like PlayStation and Xbox. Unlike locked-down consoles, it is an open PC-like device that can run any software. Valve previously attempted a similar concept in 2015, but that line was discontinued. The new model leverages advancements from the Steam Deck.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Steam_Machine">Steam Machine - Wikipedia</a></li>
<li><a href="https://www.the-independent.com/extras/indybest/gadgets-tech/video-games-consoles/valve-steam-machine-release-date-b3000219.html">Valve’s Steam Machine launch could be just hours away | The Independent</a></li>
<li><a href="https://store.steampowered.com/hardware/steammachine">Steam Machine</a></li>

</ul>
</details>

**Discussion**: Community comments praised the fair reservation system, open nature, and relatable marketing footage. One user expressed support for Linux gaming, while others appreciated the freedom to install custom software.

**Tags**: `#steam-machine`, `#valve`, `#gaming-hardware`, `#pc-gaming`, `#launch`

---

<a id="item-2"></a>
## [Free-threaded Python: past, present, and future](https://lwn.net/Articles/1078367/) ⭐️ 9.0/10

Thomas Wouters, a CPython core developer and steering council member, presented a talk at PyCon US 2026 covering the motivation, history, current status, and future of free-threaded Python, which removes the Global Interpreter Lock (GIL). Removing the GIL is a groundbreaking change that enables true parallel execution of threads in Python, significantly improving performance on multi-core systems and expanding Python's suitability for CPU-bound and concurrent workloads. Wouters noted that the GIL was introduced long before multi-CPU systems were common, and its removal has been a long-standing goal; he also highlighted that free-threading is already available in recent Python releases and continues to evolve.

rss · LWN.net · Jun 22, 15:26

**Background**: The Global Interpreter Lock (GIL) is a mutex in CPython that protects access to Python objects and prevents multiple threads from executing Python bytecode simultaneously. While it simplifies memory management, it limits parallelism on multi-core systems. Free-threaded Python removes the GIL, allowing threads to run concurrently, which is crucial for performance improvements in modern hardware.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.python.org/3/howto/free-threading-python.html">Python support for free threading — Python 3.14.4</a></li>
<li><a href="https://github.com/python/steering-council">GitHub - python/steering-council: Communications from the ...</a></li>

</ul>
</details>

**Tags**: `#Python`, `#GIL`, `#free-threading`, `#concurrency`, `#CPython`

---

<a id="item-3"></a>
## [Moebius: 0.2B image inpainting model with 10B-level performance](https://hustvl.github.io/Moebius/) ⭐️ 8.0/10

Researchers released Moebius, a 0.2 billion parameter image inpainting model that achieves performance comparable to 10 billion parameter models. A community member demonstrated the model running entirely in a web browser via ONNX export. This breakthrough dramatically reduces computational requirements for high-quality image inpainting, enabling deployment on edge devices and in browsers. It challenges the assumption that large models are necessary for top-tier performance, potentially lowering costs and democratizing access to advanced image editing. Moebius outputs images at 512x512 resolution, and community tests indicate noticeable smoothing in inpainted areas compared to larger models, with weaker performance on novel objects. The model was successfully converted to ONNX and runs in-browser with approximately 1.3 GB download.

hackernews · DSemba · Jun 22, 13:53 · [Discussion](https://news.ycombinator.com/item?id=48630171)

**Background**: Image inpainting is the task of filling in missing or corrupted parts of an image. Large industrial models with billions of parameters achieve high quality but are computationally expensive. Moebius uses extreme structural compression to overcome the representation bottleneck, aiming for specialist-level quality with far fewer parameters. ONNX Runtime enables cross-platform inference, including in web browsers via WebAssembly and WebGPU.

<details><summary>References</summary>
<ul>
<li><a href="https://hustvl.github.io/Moebius/">Moebius: 0.2B Lightweight Image Inpainting Framework with 10B ...</a></li>
<li><a href="https://arxiv.org/abs/2606.19195">[2606.19195] Moebius: 0.2B Lightweight Image Inpainting ...</a></li>
<li><a href="https://huggingface.co/papers/2606.19195">Paper page - Moebius: 0.2B Lightweight Image Inpainting ...</a></li>

</ul>
</details>

**Discussion**: The community is impressed by the tiny model size and the browser demo, with some users successfully running it locally. However, skepticism exists about the claimed 10B-level performance, as tests reveal visible smoothing and resolution limitations (512x512). Users also express interest in specialized versions for manga translation and other domains.

**Tags**: `#image inpainting`, `#efficient ML`, `#model compression`, `#ONNX`, `#browser inference`

---

<a id="item-4"></a>
## [Police Chiefs Stalking Women With Flock LPRs Shows Warrant Need](https://ipvm.com/reports/police-chiefs-track) ⭐️ 8.0/10

A report documents that police chiefs have misused Flock Safety's automated license plate readers to stalk women, highlighting the urgent need for warrant requirements before such surveillance tools can be used for personal tracking. This abuse by law enforcement leaders themselves demonstrates the inherent risks of unchecked ALPR access, potentially eroding public trust and demanding stronger privacy safeguards. While Flock characterizes the abuse as rare, the report notes that tracking people known to officers is the most common form of misuse, revealing a contradiction in their stance.

hackernews · jhonovich · Jun 22, 19:13 · [Discussion](https://news.ycombinator.com/item?id=48634694)

**Background**: Automated License Plate Readers (ALPRs) like Flock Safety's use AI to capture license plates, vehicle make/model, and location data, enabling tracking of vehicles' movements over time. Police departments widely deploy these cameras, but without warrant requirements, officers can query the data for any reason, leading to privacy violations.

<details><summary>References</summary>
<ul>
<li><a href="https://www.jalopnik.com/1982690/police-flock-cameras-sued-for-tracking-man-526-times/">Police Used Flock Cameras To Track One Driver Over 500 Times.</a></li>
<li><a href="https://www.infosecinstitute.com/resources/general-security/privacy-implications-automatic-license-plate-recognition-technology/">Privacy Implications of Automatic License Plate Recognition...</a></li>
<li><a href="https://www.govtech.com/em/safety/despite-successes-alpr-tech-still-raises-privacy-concerns?_amp=true">Despite Successes, ALPR Tech Still Raises Privacy Concerns</a></li>

</ul>
</details>

**Discussion**: Commenters debate the tension between claims of rare abuse and the prevalence of officers tracking acquaintances. Some draw parallels to broader surveillance concerns, while others argue that without warrants, such systems invite misuse.

**Tags**: `#privacy`, `#surveillance`, `#police accountability`, `#civil liberties`, `#license plate readers`

---

<a id="item-5"></a>
## [Mitchell pledges $400k to Zig Software Foundation](https://mitchellh.com/writing/zig-donation-2026) ⭐️ 8.0/10

Mitchell Hashimoto announced a second pledge of $400,000 to the Zig Software Foundation, bringing his total support to $800,000, to fund the ongoing development of the Zig programming language. This substantial donation provides critical financial stability for the Zig Software Foundation, enabling faster development of the language, which aims to be a modern alternative to C for system programming. The pledge is for the year 2026, following a previous $400,000 donation in 2023; Mitchell Hashimoto is the creator of the Ghostty terminal emulator, written in Zig.

hackernews · tosh · Jun 22, 13:43 · [Discussion](https://news.ycombinator.com/item?id=48630020)

**Background**: Zig is a general-purpose system programming language designed to improve upon C, with a focus on safety, performance, and simplicity. It is maintained by the Zig Software Foundation (ZSF), a non-profit. Mitchell Hashimoto, co-founder of HashiCorp, is a prominent open-source developer and has been a major financial supporter of Zig.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Zig_(programming_language)">Zig (programming language)</a></li>
<li><a href="https://ziglang.org/">Home ⚡ Zig Programming Language</a></li>

</ul>
</details>

**Discussion**: The community reacted positively, with many praising Hashimoto's generosity and the impact on Zig development. Some commenters noted Ghostty's quality as a showcase for Zig, while others debated the language's stance against LLM-generated contributions.

**Tags**: `#zig`, `#programming-languages`, `#open-source`, `#funding`, `#donation`

---

<a id="item-6"></a>
## [Deno Desktop Launches with Multi-Backend Webview Framework](https://docs.deno.com/runtime/desktop/) ⭐️ 8.0/10

Deno has introduced Deno Desktop, a desktop application framework that supports multiple webview backends including CEF, Webview, and Raw, featuring a shared runtime to reduce binary sizes and a permission system for enhanced security. Deno Desktop offers a compelling alternative to Electron by potentially reducing app binary sizes to a few megabytes and improving security through its granular permission system, lowering the barrier for building cross-platform desktop apps with web technologies. The framework supports CEF, system Webview (WebKit on macOS/Linux, Edge WebView2 on Windows), and a Raw backend. A shared runtime is on the roadmap, promising to drop binary sizes to a few MB per app.

hackernews · GeneralMaximus · Jun 22, 05:38 · [Discussion](https://news.ycombinator.com/item?id=48626137)

**Background**: Desktop app frameworks like Electron bundle a full Chromium browser engine with each app, leading to large binary sizes (often 100+ MB). Webview backends use the system's native browser engine, reducing size. CEF allows embedding Chromium but is still large. Deno Desktop's shared runtime approach aims to share a single CEF copy across multiple apps, further reducing disk usage.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/webview/webview">GitHub - webview/webview: Tiny cross-platform webview library for C/C++. Uses WebKit (GTK/Cocoa) and Edge WebView2 (Windows). · GitHub</a></li>
<li><a href="https://en.wikipedia.org/wiki/Chromium_Embedded_Framework">Chromium Embedded Framework</a></li>

</ul>
</details>

**Discussion**: Commenters expressed interest in the shared CEF runtime and permission system integration. One user questioned how versioning would work for shared CEF across different apps. Another suggested adding a 'launch in browser' option similar to WebUI for better tradeoffs. Overall sentiment is positive, with many praising Deno's ecosystem maturity.

**Tags**: `#deno`, `#desktop-apps`, `#webview`, `#cef`, `#electron`

---

<a id="item-7"></a>
## [Claude Code 'Extended Thinking' Is a Lossy Reasoning Summary](https://patrickmccanna.net/the-text-in-claude-codes-extended-thinking-output-is-not-authentic/) ⭐️ 8.0/10

The article argues that Claude Code's 'Extended Thinking' feature produces a lossy summary of the model's reasoning rather than the actual chain-of-thought, highlighting issues of transparency and potential security risks. This matters because hidden reasoning undermines AI transparency, making it harder to audit models for safety and trustworthiness. It also enables potential prompt injection attacks where malicious instructions could be concealed in the reasoning chain. The article uses the analogy of JPEG vs. BMP to illustrate data loss: the compressed summary cannot be reversed to the original reasoning. Community comments note that companies like OpenAI and Google also obscure reasoning to protect competitive advantage.

hackernews · 0o_MrPatrick_o0 · Jun 22, 14:22 · [Discussion](https://news.ycombinator.com/item?id=48630535)

**Background**: Extended Thinking is a feature that gives Claude a 'scratchpad' to reason through complex problems before responding, providing step-by-step thought process. However, the output shown to users may be a summary rather than the full reasoning, which can lose detail and context. Lossy summarization intentionally drops some details for efficiency, but risks weakening accuracy.

<details><summary>References</summary>
<ul>
<li><a href="https://platform.claude.com/docs/en/build-with-claude/extended-thinking">Extended thinking - Claude API Docs</a></li>
<li><a href="https://zeromathai.com/en/lossy-lossless-summary-en/">Lossy Summary vs Lossless Summary — A Summarization ...</a></li>

</ul>
</details>

**Discussion**: Commenters generally agree that hidden reasoning is a known practice, citing competitive secrecy and safety concerns. Some warn about increased risk of prompt injection attacks, while others note that the reasoning blocks may not correspond to human reasoning at all, as per research on 'illegible reasoning.'

**Tags**: `#AI transparency`, `#reasoning`, `#safety`, `#Claude`, `#LLM`

---

<a id="item-8"></a>
## [Nearly half of LG smart TV apps contain residential proxy SDKs](https://spur.us/blog/smart-tv-apps-residential-proxy-sdks) ⭐️ 8.0/10

An investigation by Spur.us reveals that nearly half of LG smart TV apps from the LG Content Store include residential proxy SDKs, which covertly turn users' TVs into proxy nodes without consent. This poses a severe privacy violation as users' home networks are used for proxy traffic without their knowledge, potentially enabling malicious activities such as web scraping or circumvention of geo-blocks. The affected apps are third-party apps, not LG's first-party apps. The SDKs are supplied by third-party proxy service providers and are embedded in popular apps like streaming and utility apps.

hackernews · microcode · Jun 22, 20:48 · [Discussion](https://news.ycombinator.com/item?id=48635954)

**Background**: A residential proxy uses an IP address assigned by an Internet Service Provider (ISP) to a real household, making traffic appear to come from a legitimate home user rather than a data center. This is often used for web scraping, ad verification, or bypassing geo-restrictions. When embedded in smart TV apps without disclosure, it turns the TV into a node in a proxy network, consuming user bandwidth and potentially exposing their network to abuse.

<details><summary>References</summary>
<ul>
<li><a href="https://techreviewadvisor.com/what-is-a-residential-proxy/">What Is a Residential Proxy? How It Works - Tech Review Advisor</a></li>
<li><a href="https://www.fbi.gov/investigate/cyber/alerts/2026/evading-residential-proxy-networks-protecting-your-devices-from-becoming-a-tool-for-criminals">Evading Residential Proxy Networks: Protecting Your Devices ...</a></li>

</ul>
</details>

**Discussion**: Comments express strong concern and distrust toward smart TVs. Users recommend never connecting smart TVs to the network or isolating them on a firewalled VLAN. Some point out that the affected apps are third-party, not built-in, and discuss the rise of scraping from residential IPs.

**Tags**: `#privacy`, `#smart TV`, `#residential proxy`, `#security`, `#IoT`

---

<a id="item-9"></a>
## [Moebius image inpainting model ported to browser with Claude Code](https://simonwillison.net/2026/Jun/22/porting-moebius/#atom-everything) ⭐️ 8.0/10

Simon Willison successfully ported the Moebius 0.2B lightweight image inpainting model to run entirely in a web browser using WebGPU acceleration, with the help of the AI coding agent Claude Code. The demo is available at simonw.github.io/moebius-web/. This port demonstrates that state-of-the-art machine learning models can run efficiently in the browser, reducing reliance on server-side inference and enabling privacy-preserving, offline-capable applications. It lowers the barrier for developers to integrate advanced image editing capabilities into web applications. The port used ONNX Runtime Web with the WebGPU backend, avoiding the original PyTorch and CUDA dependencies. The model weights were converted to ONNX format, and Claude Code assisted with the implementation, including agentic research and code generation.

rss · Simon Willison · Jun 22, 23:43

**Background**: Moebius is a 0.2B parameter image inpainting model that achieves performance comparable to 10B-level models while being lightweight. WebGPU is a modern browser API that allows web applications to utilize the device's GPU for high-performance computation. Claude Code is an AI coding agent from Anthropic that can autonomously write, edit, and debug code across a project.

<details><summary>References</summary>
<ul>
<li><a href="https://hustvl.github.io/Moebius/">Moebius: 0.2B Lightweight Image Inpainting Framework with 10B ...</a></li>
<li><a href="https://github.com/mlc-ai/web-llm">GitHub - mlc-ai/web-llm: High-performance In-browser LLM Inference Engine · GitHub</a></li>
<li><a href="https://code.claude.com/docs/en/how-claude-code-works">How Claude Code works - Claude Code Docs</a></li>

</ul>
</details>

**Tags**: `#image inpainting`, `#WebGPU`, `#machine learning`, `#browser inference`, `#Claude Code`

---

<a id="item-10"></a>
## [First preview of Xfce's Wayland compositor xfwl4](https://lwn.net/Articles/1078942/) ⭐️ 8.0/10

Brian Tarricone announced the first preview release (alpha) of xfwl4, a Wayland compositor for the Xfce desktop environment, after nearly six months of development. This marks a significant milestone for Xfce's transition from X11 to Wayland, bringing modern display server features to the lightweight desktop environment and expanding Wayland adoption in the Linux ecosystem. The compositor is written in Rust and aims for feature parity with Xfwm4, though it is still missing many behaviors and settings, and users should expect bugs.

rss · LWN.net · Jun 22, 13:44

**Background**: Wayland is a protocol for display servers on Linux, designed to replace the older X Window System with improved security and simplicity. Xfce is a lightweight desktop environment that traditionally uses the Xfwm4 window manager on X11. The xfwl4 project, announced earlier in 2026, represents Xfce's investment in Wayland support, developed as a separate compositor rather than modifying Xfwm4.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wayland_compositor">Wayland compositor</a></li>
<li><a href="https://github.com/hanthor/xfwl4">GitHub - hanthor/xfwl4: xfwl4 Wayland compositor for XFCE</a></li>
<li><a href="https://www.phoronix.com/news/Xfce-Xfwl4-Wayland">Xfwl4 Being Developed As New Wayland Compositor For Xfce</a></li>

</ul>
</details>

**Tags**: `#Xfce`, `#Wayland`, `#Linux desktop`, `#compositor`

---

<a id="item-11"></a>
## [OSPM 2026 Day One: Idle States, sched_ext, Lock-Holder Preemption](https://lwn.net/Articles/1077759/) ⭐️ 8.0/10

Reports from the first day of the OSPM 2026 Linux kernel power management and scheduling summit cover discussions on CPU idle-state selection criteria, the sched_ext extensible scheduler class, and the issue of lock-holder preemption in virtualization. These topics are critical for improving Linux kernel efficiency in power management and scheduling, affecting both battery-powered devices and data center performance. The discussions may drive future kernel patches that optimize energy use and reduce latency. Rafael Wysocki, cpuidle maintainer, discussed success criteria for idle-state governors. Sessions also tackled sched_ext, which allows BPF-based schedulers, and lock-holder preemption, a problem where a virtual CPU holding a spinlock gets preempted, causing performance issues.

rss · LWN.net · Jun 22, 13:26

**Background**: The OSPM (OS-directed Power Management) summit is an annual gathering of Linux kernel developers focused on power management and scheduling. The cpuidle subsystem is responsible for putting idle CPUs into low-power states, with governors selecting the appropriate idle state based on predicted idle duration. sched_ext is a kernel feature that enables implementing schedulers as BPF programs, allowing rapid experimentation. Lock-holder preemption is a classic virtualization issue where the hypervisor preempts a vCPU holding a spinlock, causing wasted spinning on other vCPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/sched-ext/scx">GitHub - sched-ext/scx: sched_ext schedulers and tools Overview - sched_ext linux/tools/sched_ext/README.md at master · torvalds/linux sched-ext Tutorial | CachyOS sched_ext Linux 7.2 sched_ext Continues Working Toward Sub-Scheduler ...</a></li>
<li><a href="https://sched-ext.com/docs/OVERVIEW">Overview - sched_ext</a></li>
<li><a href="https://stackoverflow.com/questions/30780311/lock-holder-preemption">multithreading - Lock Holder Preemption - Stack Overflow</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#power management`, `#scheduling`, `#OSPM 2026`

---

<a id="item-12"></a>
## [Micron plans $200B expansion to ease AI memory shortage](https://t.me/zaihuapd/42101) ⭐️ 8.0/10

Micron Technology announced a plan to invest $200 billion to expand wafer fabrication plants in the U.S. and globally, aiming to alleviate the AI-driven memory chip supply bottleneck. A $50 billion investment in Idaho headquarters will build two factories, with the first expected to start production of DRAM chips for HBM in mid-2027. This massive investment signals the critical role of high-bandwidth memory (HBM) in AI hardware as demand surges, with DRAM prices rising over 170% in the past year and Micron's HBM3e and HBM4 capacity sold out through 2026. The expansion will help secure supply for AI accelerators and may influence global semiconductor supply chains. Micron's total investment of $200 billion is spread across multiple global sites, with the first Idaho factory alone costing $50 billion. The company's gross margin has reached 56% due to AI-driven demand, and HBM production involves complex 3D stacking of DRAM chips to achieve high bandwidth and low power consumption.

telegram · zaihuapd · Jun 22, 05:30

**Background**: High Bandwidth Memory (HBM) is a 3D-stacked DRAM technology that delivers ultra-high bandwidth and energy efficiency, essential for AI accelerators like GPUs. The AI boom has drastically increased demand for HBM, creating a supply crunch as traditional memory production cannot keep up. Micron, along with Samsung and SK Hynix, is one of the few manufacturers capable of producing HBM.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/High_Bandwidth_Memory">High Bandwidth Memory - Wikipedia</a></li>
<li><a href="https://www.techtarget.com/whatis/definition/high-bandwidth-memory">What is high-bandwidth memory (HBM)? - TechTarget High Bandwidth Memory (HBM): Everything You Need To Know High-Bandwidth Memory (HBM) - Semiconductor Engineering High Bandwidth Memory (HBM): Everything You Need to Know HBM (High Bandwidth Memory): Concept, Architecture, and ... High Bandwidth Memory (HBM) Explained</a></li>
<li><a href="https://semiengineering.com/high-bandwidth-memory-hbm-everything-you-need-to-know/">High Bandwidth Memory (HBM): Everything You Need To Know</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#HBM`, `#AI hardware`, `#memory chips`, `#investment`

---

<a id="item-13"></a>
## [48 Chinese Developers Sue Apple Over China App Store Monopoly](https://m.nbd.com.cn/articles/2026-06-22/4433380.html) ⭐️ 8.0/10

On June 22, 2026, 48 Chinese iOS developers filed a complaint with China's antitrust regulator, accusing Apple of abusing its monopoly in the Chinese market and failing to honor its promise that App Store commissions in China would not exceed those in other markets. They demand Apple open up third-party app distribution and payment channels in China. This complaint could escalate regulatory pressure on Apple in China, its second-largest iOS market, and potentially force changes to its App Store policies regarding commissions and third-party payment access, impacting global antitrust discussions. The developers also proposed establishing a 'global policy automatic alignment supervision mechanism' to ensure consistent commission rates and market openness. While Apple reduced commissions in China in March 2026, developers argue that without third-party distribution and payment options, the practical bargaining power has not improved.

telegram · zaihuapd · Jun 22, 14:57

**Background**: The 'Apple tax' refers to the 15-30% commission Apple charges on in-app purchases and paid app downloads. In China, Apple faces increasing antitrust scrutiny as regulators push for fair competition. Similar actions have occurred in other jurisdictions like the EU and South Korea, leading to forced changes such as allowing third-party payment systems.

**Tags**: `#Apple`, `#antitrust`, `#App Store`, `#China`, `#monopoly`

---