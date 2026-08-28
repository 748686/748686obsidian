---
layout: default
title: "Horizon Summary: 2026-06-15 (EN)"
date: 2026-06-15
lang: en
---

> From 26 items, 10 important content pieces were selected

---

1. [Linux 7.1 kernel released with major subsystem improvements](#item-1) ⭐️ 9.0/10
2. [Huawei Open-Sources Pangu 2.0, Aims for World No.1](#item-2) ⭐️ 9.0/10
3. [US Government Forces Anthropic to Restrict Two AI Models](#item-3) ⭐️ 9.0/10
4. [Formal Methods and the Future of Programming](#item-4) ⭐️ 8.0/10
5. [JavaScript's Evolution into a Compilation Target](#item-5) ⭐️ 8.0/10
6. [How to Earn a Billion Dollars Through Startups](#item-6) ⭐️ 8.0/10
7. [SMIC N+3 Metal Pitch Compared to Intel 18A](#item-7) ⭐️ 8.0/10
8. [Coherent Context Can Silently Shift LLMs Into Different Internal Regimes](#item-8) ⭐️ 8.0/10
9. [Verifier Tax: Horizon-Dependent Safety–Success Tradeoff for LLM Agents](#item-9) ⭐️ 8.0/10
10. [75 US data center projects worth $130B blocked in Q1 2026](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Linux 7.1 kernel released with major subsystem improvements](https://lwn.net/Articles/1077758/) ⭐️ 9.0/10

Linus Torvalds has released the Linux 7.1 kernel, featuring new clone() flags, BPF support for io_uring, zero-copy I/O for ublk, initial sched_ext sub-scheduler support, swapping improvements, and a completely rewritten NTFS implementation. This release integrates long-anticipated features like BPF with io_uring and extensible scheduling via sched_ext, which will enhance I/O performance and process management flexibility. The rewritten NTFS driver also improves filesystem compatibility. The sched_ext sub-scheduler support is described as initial and incomplete, while the NTFS driver is fully rewritten. The kernel also drops support for old 486-based architectures.

rss · LWN.net · Jun 14, 18:47

**Background**: The Linux kernel is the core of the operating system, managing hardware and system resources. io_uring is a modern asynchronous I/O interface for efficient file and network operations. sched_ext allows scheduling policies to be written in BPF and loaded dynamically. ublk is a user-space block device driver that provides safety and flexibility. NTFS is a filesystem used by Microsoft Windows.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Io_uring">io_uring - Wikipedia</a></li>
<li><a href="https://github.com/sched-ext/scx">GitHub - sched-ext/scx: sched_ext schedulers and tools · GitHub</a></li>
<li><a href="https://www.kernel.org/doc/html/latest/block/ublk.html">Userspace block device driver (ublk driver) — The Linux ...</a></li>

</ul>
</details>

**Tags**: `#Linux`, `#kernel`, `#BPF`, `#io_uring`, `#NTFS`

---

<a id="item-2"></a>
## [Huawei Open-Sources Pangu 2.0, Aims for World No.1](https://t.me/zaihuapd/41948) ⭐️ 9.0/10

At HDC 2026, Huawei announced openPangu 2.0, an open-source large language model with a 505B-parameter Pro variant and a 92B-parameter Flash variant, supporting 512K context length. The company plans to release seven major components including pre-training code starting June 30. This release is a major open-source contribution from a leading tech giant, potentially shifting the AI landscape by providing a very large, accessible model optimized for Ascend hardware and HarmonyOS. It strengthens Huawei's position in the global AI race, especially within the Chinese ecosystem. The model is tailored for Ascend AI computing and HarmonyOS, with 512K context length enabling long-document processing. Full open-sourcing will start from June 30, covering seven components such as pre-training code and possibly weights.

telegram · zaihuapd · Jun 14, 08:05

**Background**: Huawei's Ascend computing platform is a full-stack AI infrastructure combining Ascend AI processors with base software, supporting training and inference across cloud, edge, and device. HarmonyOS is Huawei's distributed operating system. Yu Chengdong noted that while Huawei's computing power is limited due to supporting domestic enterprises, the company has been developing Pangu since before the concept of large models became popular.

<details><summary>References</summary>
<ul>
<li><a href="https://e.huawei.com/cn/products/computing/ascend">昇腾计算-华为Ascend-AI计算-华为企业业务</a></li>
<li><a href="https://www.huaweicloud.com/product/ecs/ascend.html">昇腾AI云服务器_ECS-华为云</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/1952064479069188801">AI算力新纪元：华为昇腾超节点战略与英伟达H100/H200的深度对决</a></li>

</ul>
</details>

**Tags**: `#Huawei`, `#open-source`, `#large language model`, `#AI`, `#Pangu`

---

<a id="item-3"></a>
## [US Government Forces Anthropic to Restrict Two AI Models](https://t.me/zaihuapd/41949) ⭐️ 9.0/10

The US government issued an export control directive to Anthropic, requiring the company to block all access to its Claude Fable 5 and Claude Mythos 5 models for any foreign national, including its own foreign employees, citing national security risks from potential jailbreaking. This unprecedented government intervention signals escalating regulatory tensions around powerful AI models and could set a precedent for export controls on AI capabilities, impacting how companies deploy advanced models globally. Anthropic complied by shutting down access to both models for all customers; other Claude models remain unaffected. The company is working to restore access as soon as possible while ensuring compliance.

telegram · zaihuapd · Jun 14, 09:06

**Background**: Jailbreaking refers to bypassing built-in safety mechanisms in AI models to elicit unintended or harmful outputs. Claude Fable 5 and Claude Mythos 5 are advanced AI models developed by Anthropic; Mythos-class models are capable of identifying and exploiting zero-day vulnerabilities in major software, raising significant security concerns.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/news/claude-fable-5-mythos-5">Claude Fable 5 and Claude Mythos 5 \ Anthropic</a></li>
<li><a href="https://red.anthropic.com/2026/mythos-preview/">Claude Mythos Preview \ red.anthropic.com</a></li>
<li><a href="https://www.lakera.ai/blog/jailbreaking-large-language-models-guide">Jailbreaking Large Language Models: Techniques, Examples ...</a></li>

</ul>
</details>

**Tags**: `#AI regulation`, `#Anthropic`, `#national security`, `#export control`, `#AI safety`

---

<a id="item-4"></a>
## [Formal Methods and the Future of Programming](https://blog.janestreet.com/formal-methods-at-jane-street-index/?from_theconsensus=1) ⭐️ 8.0/10

Jane Street's blog post examines formal methods, including historical proof automation, and argues they could play a key role in verifying AI-generated code. As AI generates increasing amounts of code, formal verification becomes crucial to ensure correctness and safety, shifting human effort from writing code to verifying it. The discussion traces proof automation from early SAT solvers like Oppen-Nelson to the Boyer-Moore prover, highlighting the continued need for human guidance in suggesting lemmas. Formal methods require writing specifications that can themselves contain bugs, but they provide a different kind of rigor than traditional testing.

hackernews · eatonphil · Jun 14, 12:35 · [Discussion](https://news.ycombinator.com/item?id=48526633)

**Background**: Formal methods are mathematically rigorous techniques for specifying, developing, and verifying software and hardware systems. They use formal logic to prove that a system satisfies its specification, offering higher assurance than testing alone. Automated theorem proving (ATP) and proof assistants are key tools, with proof automation aiming to reduce the manual effort involved.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Formal_methods">Formal methods - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Automated_theorem_proving">Automated theorem proving - Wikipedia</a></li>
<li><a href="https://web.mit.edu/16.35/www/lecturenotes/FormalMethods.pdf">Introducing Formal Methods - MIT</a></li>

</ul>
</details>

**Discussion**: Commenters share personal experiences with formal methods: one former proof of correctness worker notes that early proof automation was more advanced than many later systems, while another uses expressive types in Scala 3 to enforce compile-time proofs. A non-English speaker highlights the challenge of learning programming through translation and suggests AI should shift human value toward verification. One commenter questions whether formal specs are just 'tests written differently' and can suffer from the same bugs.

**Tags**: `#formal methods`, `#proof automation`, `#AI verification`, `#programming languages`, `#Jane Street`

---

<a id="item-5"></a>
## [JavaScript's Evolution into a Compilation Target](https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript) ⭐️ 8.0/10

Gary Bernhardt's 2014 talk humorously predicted that JavaScript would become a compilation target, a prophecy that has largely come true with the rise of WebAssembly and Electron. This talk accurately foresaw the trajectory of web development, where languages like TypeScript compile to JavaScript and desktop apps are built with web technologies via Electron, affecting how developers today approach cross-platform development. The talk referenced asm.js, a precursor to WebAssembly, which was later deprecated in favor of WebAssembly. Electron, another prediction, enables desktop applications using web technologies.

hackernews · subset · Jun 14, 12:38 · [Discussion](https://news.ycombinator.com/item?id=48526661)

**Background**: JavaScript was originally designed as a scripting language for web browsers, but over time it became the only language natively supported by all browsers. To improve performance and enable other languages to run on the web, asm.js (a strict subset of JavaScript) was introduced in 2013, followed by WebAssembly (a binary format) in 2015. Electron, released in 2013, allows developers to build desktop applications using web technologies like JavaScript, HTML, and CSS.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/WebAssembly">WebAssembly</a></li>
<li><a href="https://en.wikipedia.org/wiki/Electron_(software_framework)">Electron (software framework)</a></li>

</ul>
</details>

**Discussion**: Commenters largely agree that Bernhardt's predictions were accurate, noting that JavaScript has become a compilation target and that Electron brought web technologies to desktop apps. Some point out that WebAssembly still lacks direct DOM manipulation, requiring JavaScript as glue code.

**Tags**: `#JavaScript`, `#WebAssembly`, `#TypeScript`, `#Programming Languages`, `#History`

---

<a id="item-6"></a>
## [How to Earn a Billion Dollars Through Startups](https://paulgraham.com/earn.html) ⭐️ 8.0/10

Paul Graham published an essay arguing that one can legitimately earn a billion dollars by creating value through startups, challenging criticisms that equate wealth with exploitation. This essay sparks significant debate about the ethics of wealth creation in the startup ecosystem, influencing how entrepreneurs and investors justify large fortunes. Graham distinguishes between being given a billion dollars and earning it through creating something of equivalent value, and argues that the process of creative destruction often involves moral entanglement.

hackernews · kingstoned · Jun 14, 11:50 · [Discussion](https://news.ycombinator.com/item?id=48526360)

**Background**: Paul Graham is the co-founder of Y Combinator, a prominent startup accelerator. His essays on startups and wealth are widely read. The concept of 'earning' wealth through startups is central to tech culture, often contrasted with criticisms of wealth inequality.

**Discussion**: Comments are polarized: some praise Graham's perspective and lament negativity, while others critique his use of 'earn' and argue that billion-dollar fortunes inevitably involve exploitation or destruction that isn't accounted for.

**Tags**: `#startups`, `#wealth`, `#entrepreneurship`, `#Paul Graham`, `#economics`

---

<a id="item-7"></a>
## [SMIC N+3 Metal Pitch Compared to Intel 18A](https://newsletter.semianalysis.com/p/steel-smic-n3-teardown) ⭐️ 8.0/10

SemiAnalysis published a detailed teardown analysis comparing SMIC's N+3 node metal pitch to Intel 18A and other competitors, providing original measurement data. This comparison is significant because it reveals how SMIC's advanced node, fabricated without EUV lithography, stacks up against Intel's leading-edge node, with implications for the semiconductor race and geopolitical tensions. Metal pitch is the distance between centers of adjacent metal interconnect lines; smaller pitch typically indicates higher transistor density. SMIC N+3 is a scaled evolution of its 7nm-class process, approaching 5nm-equivalent density without using EUV.

rss · Semianalysis · Jun 14, 19:14

**Background**: In semiconductor manufacturing, node names like '5nm' are often marketing terms rather than physical dimensions; metal pitch is a key metric for density. SMIC is constrained by US sanctions and cannot access EUV lithography, yet has advanced to N+3 using multiple patterning with DUV. Intel 18A is Intel's most advanced node, featuring RibbonFET gate-all-around transistors and PowerVia backside power delivery.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Semiconductor_Manufacturing_International_Corporation">Semiconductor Manufacturing International Corporation - Wikipedia</a></li>
<li><a href="https://techlevated.com/evolution-of-metal-pitch-in-semiconductor-transistors/">Evolution of Metal Pitch in Semiconductor Transistors</a></li>
<li><a href="https://en.wikipedia.org/wiki/5_nm_process">5 nm process - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#semiconductors`, `#SMIC`, `#Intel 18A`, `#process technology`, `#teardown`

---

<a id="item-8"></a>
## [Coherent Context Can Silently Shift LLMs Into Different Internal Regimes](https://www.reddit.com/r/MachineLearning/comments/1u5xnxg/coherent_context_can_silently_shift_llms_into_a/) ⭐️ 8.0/10

Independent researcher PresentSituation8736 discovered that a strong, coherent context can shift an LLM's internal representation space before output generation, causing safety mechanisms like RLHF and output filters to remain blind to the change. This finding reveals a fundamental blind spot in current LLM safety approaches, which only inspect final outputs, implying that sophisticated adversaries could bypass safeguards without triggering any surface-level alarms. The researcher measured hidden-state geometry, residual stream trajectories, and used sparse autoencoder (SAE) readouts on open models like Gemma-3-12B-IT, using coherent target texts that are not explicit jailbreak prompts.

reddit · r/MachineLearning · /u/PresentSituation8736 · Jun 14, 21:42

**Background**: LLMs are neural networks that process text by transforming token embeddings through a series of layers. The residual stream is a core component that accumulates information across layers, acting as a shared representation space. Mechanistic interpretability aims to reverse-engineer the internal algorithms of these models.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>
<li><a href="https://arxiv.org/html/2312.12141v1">Exploring the Residual Stream of Transformers - arXiv.org</a></li>
<li><a href="https://seantrott.substack.com/p/mechanistic-interpretability-for">" Mechanistic interpretability " for LLMs, explained</a></li>

</ul>
</details>

**Tags**: `#AI safety`, `#mechanistic interpretability`, `#LLM`, `#alignment`, `#internal state`

---

<a id="item-9"></a>
## [Verifier Tax: Horizon-Dependent Safety–Success Tradeoff for LLM Agents](https://www.reddit.com/r/MachineLearning/comments/1u58mkq/the_verifier_tax_horizondependent_safetysuccess/) ⭐️ 8.0/10

A new paper presented at ACM CAIS 2026 introduces the Verifier Tax, a horizon-dependent safety–success tradeoff in tool-using LLM agents, and proposes a two-tier verification architecture combining deterministic checks with an LLM-based verifier. This work highlights that current evaluation practices focusing solely on success rate can hide unsafe completions, and the Verifier Tax reveals a critical tension between safety and task completion as tasks lengthen, impacting the safe deployment of LLM agents in real-world applications. The study uses τ-bench tool-use scenarios and decomposes outcomes into safe success, unsafe success, and failure; it finds that verification reduces unsafe success but also reduces task completion as the horizon increases, with model-dependent interaction horizons of 15–30 turns.

reddit · r/MachineLearning · /u/AccomplishedLeg1508 · Jun 14, 02:09

**Background**: LLM agents are increasingly used with external tools (e.g., APIs) to complete multi-step tasks. However, an agent may achieve a task objective while violating safety or policy rules, leading to 'unsafe success'. The Verifier Tax concept emerges from the observation that adding verification to catch such violations can inadvertently reduce the agent's ability to complete long-horizon tasks.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2603.19328">[2603.19328] The Verifier Tax: Horizon Dependent Safety Success ...</a></li>
<li><a href="https://github.com/sierra-research/tau2-bench">GitHub - sierra-research/tau2-bench: τ-Bench: A Benchmark for ...</a></li>
<li><a href="https://www.harrisburgu.edu/news/2026-06-05-ai-agent-safety-doctoral-research/">HU Student's Doctoral Research on AI Agent Safety Featured at...</a></li>

</ul>
</details>

**Tags**: `#LLM agents`, `#AI safety`, `#verification`, `#tool use`, `#evaluation`

---

<a id="item-10"></a>
## [75 US data center projects worth $130B blocked in Q1 2026](https://www.tomshardware.com/tech-industry/artificial-intelligence/more-than-75-data-center-build-outs-worth-usd130-billion-have-been-successfully-blocked-in-the-first-four-months-of-2026-bipartisan-opposition-mounts-nationwide-over-fears-of-soaring-power-and-water-costs) ⭐️ 8.0/10

In the first quarter of 2026, over 75 data center construction projects valued at approximately $130 billion were blocked or delayed across the United States, matching the total number for all of 2025. Bipartisan opposition and grassroots activism over energy consumption and environmental impact have intensified sharply. This marks a major shift in data center infrastructure deployment, potentially slowing AI and cloud computing growth. The rapid rise in opposition—from 396 to 833 grassroots groups in three months across 49 states—signals that energy and environmental constraints could become a critical bottleneck for the tech industry. The blocked projects represent about $130 billion in total value, matching the entire 2025 tally in just one quarter. State legislatures have introduced numerous regulatory bills, and some federal lawmakers have proposed legislation to pause data center construction.

telegram · zaihuapd · Jun 14, 03:03

**Background**: Data centers consume enormous amounts of electricity and water, raising concerns about grid strain and environmental impact. As AI workloads surge, demand for new data centers has skyrocketed, leading to conflicts with local communities over resource allocation. The bipartisan nature of the opposition highlights that this is not a partisan issue but a broad-based environmental and economic concern.

**Tags**: `#data centers`, `#energy regulation`, `#AI infrastructure`, `#US policy`, `#environmental impact`

---