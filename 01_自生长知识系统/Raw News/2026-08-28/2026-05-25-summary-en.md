---
layout: default
title: "Horizon Summary: 2026-05-25 (EN)"
date: 2026-05-25
lang: en
---

> From 28 items, 6 important content pieces were selected

---

1. [Spyware Backdoor Found in Telegram on APKPure](#item-1) ⭐️ 9.0/10
2. [Memory now accounts for 63% of AI chip costs](#item-2) ⭐️ 8.0/10
3. [LLM Agents Show Constraint Decay in Backend Code Generation](#item-3) ⭐️ 8.0/10
4. [Microsoft open-sources earliest DOS source code](#item-4) ⭐️ 8.0/10
5. [AMD Removes Linux Support from Free Vivado Tier](#item-5) ⭐️ 8.0/10
6. [Armin Ronacher: AI-Generated Bug Reports Are Inaccurate](#item-6) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Spyware Backdoor Found in Telegram on APKPure](https://x.com/EricParker/status/2058411298195661221) ⭐️ 9.0/10

A repackaged version of Telegram 12.6.5 on APKPure was found to contain the DataCollector spyware framework (classes3.dex, over 3000 lines of code), which can steal chat history, contacts, photos, documents, GPS location, and SIM card data, encrypted via AES-GCM and exfiltrated to C2 server 38.190.225.166. This highlights the security risks of downloading apps from third-party stores, as even official-looking packages can contain powerful spyware. Millions of users who downloaded Telegram from APKPure may have had their private communications and sensitive data compromised. The backdoor is embedded in a repackaged APK signed with a different certificate, and the DataCollector spyware uses AES-GCM encryption to evade detection. The C2 server IP (38.190.225.166) may be used for further analysis.

telegram · zaihuapd · May 24, 11:38

**Background**: APKPure is a third-party Android app store that distributes APK files outside of Google Play. While it offers apps that may not be available in official stores, its vetting process is less rigorous, making it a target for malware injection. Telegram is a widely used encrypted messaging app; modifying its official build grants the spyware access to all user data.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/APKPure">APKPure</a></li>
<li><a href="https://apkpure.com/how-to/is-apkpure-safe-to-download-apps-and-games">Is APKPure Safe to Download Apps and Games?</a></li>

</ul>
</details>

**Tags**: `#security`, `#malware`, `#Telegram`, `#APKPure`, `#spyware`

---

<a id="item-2"></a>
## [Memory now accounts for 63% of AI chip costs](https://epoch.ai/data-insights/ai-chip-component-cost-shares) ⭐️ 8.0/10

According to Epoch AI, memory's share of AI chip component costs rose from 52% in early 2024 to 63% by late 2025, driven primarily by high-bandwidth memory (HBM) demand. This shift makes memory the dominant cost component, surpassing packaging and auxiliary components. This trend implies that AI inference and training hardware costs could see significant reduction without technical breakthroughs, simply by waiting for DRAM supply to catch up with demand. It also highlights a supply chain bottleneck that could affect AI chip pricing and availability for consumers and enterprises. Over the period, packaging costs fell from 19% to 15%, auxiliary components from 15% to 9%, while logic die costs remained stable at 13–14%. The rising memory cost is largely due to HBM, which consumes about three times the wafer capacity of DDR5 per gigabyte.

hackernews · intelkishan · May 24, 16:31 · [Discussion](https://news.ycombinator.com/item?id=48258684)

**Background**: High-Bandwidth Memory (HBM) is a type of DRAM stacked vertically to save space and power, commonly used in AI accelerators like NVIDIA GPUs. As AI model sizes grow, demand for HBM has surged, diverting wafer and packaging capacity from consumer DRAM like DDR5. This has led to price increases in both AI and consumer memory markets.

<details><summary>References</summary>
<ul>
<li><a href="https://epoch.ai/data-insights/ai-chip-component-cost-shares">AI Chip Component Costs: Memory at 63% | Epoch AI | Epoch AI</a></li>
<li><a href="https://en.wikipedia.org/wiki/High_Bandwidth_Memory">High Bandwidth Memory - Wikipedia</a></li>
<li><a href="https://www.tomshardware.com/pc-components/ram/hbm-is-eating-your-ram">Here's why HBM is coming for your PC's RAM — HBM consumes around three times the wafer capacity of DDR5 per gigabyte, as AI supercharges demand for chips and advanced packaging | Tom's Hardware</a></li>

</ul>
</details>

**Discussion**: Commenters noted that DRAM supply growth at 20-25% annually may not keep pace with AI demand, suggesting persistent high memory costs. Some expressed frustration over rising RAM prices for consumers, with one user reporting a 96GB kit price jumping from $250 to $1200. Others saw an opportunity for software-level memory optimization to reduce dependency.

**Tags**: `#AI`, `#hardware costs`, `#memory`, `#semiconductor`, `#DRAM`

---

<a id="item-3"></a>
## [LLM Agents Show Constraint Decay in Backend Code Generation](https://arxiv.org/abs/2605.06445) ⭐️ 8.0/10

A new research paper introduces 'constraint decay,' a phenomenon where LLM-based coding agents excel at unconstrained code generation but significantly underperform when forced to follow explicit architectural rules. This finding underscores that current LLM agents are unreliable for production-grade backend development, where adherence to specific constraints is critical, and highlights a key challenge for deploying AI coding assistants in real-world software engineering. The study did not fully test frontier models (e.g., GPT-4, Claude 3.5) due to cost constraints, so the specific performance numbers may differ for state-of-the-art systems. The paper also notes that jointly satisfying functional and structural requirements remains an open problem.

hackernews · wek · May 24, 12:55 · [Discussion](https://news.ycombinator.com/item?id=48256912)

**Background**: LLM-based coding agents use large language models to generate code from natural language prompts. While they can produce functional code quickly, their reliability under complex architectural constraints—such as specific design patterns or coding standards—has been less studied. Constraint decay refers to the observed drop in performance when agents must navigate explicit rules.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2605.06445">[2605.06445] Constraint Decay: The Fragility of LLM Agents in Backend Code Generation</a></li>
<li><a href="https://arxiv.org/html/2605.06445">Constraint decay: The Fragility of LLM Agents in Backend Code Generation</a></li>

</ul>
</details>

**Discussion**: Community comments draw parallels to other studies on long-horizon tasks and 'calcification' patterns. Some developers are building external orchestrators to enforce constraints, noting that multiple review-and-fix rounds are often required to match specifications.

**Tags**: `#LLM agents`, `#code generation`, `#constraint decay`, `#backend development`, `#research`

---

<a id="item-4"></a>
## [Microsoft open-sources earliest DOS source code](https://arstechnica.com/gadgets/2026/04/microsoft-open-sources-the-earliest-dos-source-code-discovered-to-date/) ⭐️ 8.0/10

Microsoft released the earliest known source code of MS-DOS, recovered through OCR from paper printouts by a dedicated team of historians and preservationists. This release marks a significant contribution to computing history, allowing developers and historians to study the foundational code that helped launch the PC revolution. The source code was preserved through OCR and manual transcription from paper printouts provided by Tim Paterson, the original author of DOS, and modern OCR software struggled with the print quality.

hackernews · DamnInteresting · May 24, 01:21 · [Discussion](https://news.ycombinator.com/item?id=48253386)

**Background**: MS-DOS was the operating system that powered the early IBM PC and its clones, establishing Microsoft's dominance in the PC software market. The code is written in assembly language and represents a pivotal artifact from the early days of personal computing.

**Discussion**: Commenters expressed gratitude for the preservation effort, with many noting the historical significance. Some highlighted the simplicity of the code compared to modern systems, while others pointed out the important role of Microsoft's BASIC interpreter alongside DOS.

**Tags**: `#open-source`, `#microsoft`, `#dos`, `#computing-history`, `#preservation`

---

<a id="item-5"></a>
## [AMD Removes Linux Support from Free Vivado Tier](https://adaptivesupport.amd.com/s/question/0D5Pd00001YQLdMKAX/why-is-vivado-20261-dropping-linux-support-for-free-tier-?language=en_US) ⭐️ 8.0/10

AMD's Vivado 2026.1 drops Linux support for the free (Basic/WebPACK) tier, while retaining it for paid editions. This change has sparked widespread backlash in the FPGA developer community. This decision alienates students, hobbyists, and developers who rely on Linux, potentially shrinking the FPGA ecosystem and driving users to competitors like Lattice or Intel. It undermines community goodwill that Xilinx had built before the AMD acquisition. The free Vivado tier (formerly WebPACK) is permanently free for supported devices, but version 2026.1 restricts it to Windows only. Paid editions (Standard, Enterprise) continue to support Linux.

hackernews · zdw · May 24, 04:14 · [Discussion](https://news.ycombinator.com/item?id=48254309)

**Background**: Vivado is AMD's FPGA design suite, offering free and paid tiers. The free WebPACK edition has long been a gateway for students and hobbyists to learn and develop on AMD FPGAs. Linux support is critical for many developers, especially in academic and open-source environments. Removing it from the free tier threatens accessibility and community growth.

<details><summary>References</summary>
<ul>
<li><a href="https://ebics.net/vivado-fpga/">Design Smarter FPGAs with the Vivado FPGA Design Suite –</a></li>
<li><a href="https://pcbsync.com/xilinx-vivado-editions/">Vivado WebPACK vs Standard vs Enterprise: Which Edition Do ...</a></li>
<li><a href="https://adaptivesupport.amd.com/s/question/0D52E00006hpVwQSAU/vivado-webpack-download?language=en_US">Vivado WebPack Download</a></li>

</ul>
</details>

**Discussion**: Community sentiment is overwhelmingly negative. Users express frustration that AMD ignores the real issue—Linux removal—while answering unasked questions. Long-time AMD users and educators plan to switch to competitors like Lattice. Some note parallels to Intel's acquisition of Altera, which also shuttered community forums.

**Tags**: `#FPGA`, `#AMD/Xilinx`, `#Vivado`, `#Linux`, `#Community backlash`

---

<a id="item-6"></a>
## [Armin Ronacher: AI-Generated Bug Reports Are Inaccurate](https://simonwillison.net/2026/May/24/armin-ronacher/#atom-everything) ⭐️ 8.0/10

Armin Ronacher, creator of Flask and Jinja2, highlighted the growing problem of AI-generated bug reports that are confident but inaccurate. He advocates for issue reports to be condensed to only human observations: what command was run, expected behavior, actual behavior, and exact error/log. This issue affects open-source maintainers who waste time deciphering inaccurate AI-generated reports, leading to burnout and reduced productivity. It underscores the need for better AI usage in software development, especially in bug reporting. Ronacher calls the AI rewriting 'a clanker' — a derogatory term for AI — and notes that poorly prompted AI often produces fake-minimal repros, wrong root cause guesses, and irrelevant error lists. He recommends a simple four-point template for human observations.

rss · Simon Willison · May 24, 18:46

**Background**: Bug reports are essential for open-source maintenance, but AI tools like LLMs are increasingly used to generate or refine them. A 'minimal reproduction' (minimal repro) is a code snippet that reliably reproduces a bug with minimal context. Armin Ronacher is a well-known developer who created Flask, Jinja2, and Werkzeug.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Clanker">Clanker - Wikipedia</a></li>
<li><a href="https://repro.fyi/">repro.fyi — The Art of the Minimal Reproduction</a></li>

</ul>
</details>

**Tags**: `#open source`, `#bug reporting`, `#AI misuse`, `#software maintenance`, `#LLM`

---