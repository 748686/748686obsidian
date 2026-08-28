---
layout: default
title: "Horizon Summary: 2026-05-24 (EN)"
date: 2026-05-24
lang: en
---

> From 22 items, 6 important content pieces were selected

---

1. [Apple Open-Sources corecrypto with Formal Proofs for Quantum-Safe Algorithms](#item-1) ⭐️ 9.0/10
2. [80386 Microcode Disassembled in Detail](#item-2) ⭐️ 8.0/10
3. [Anthropic's Project Glasswing AI Finds 10,000+ Critical Vulnerabilities](#item-3) ⭐️ 8.0/10
4. [Microsoft pushes Claude Code to key teams](#item-4) ⭐️ 8.0/10
5. [Microsoft's Report Reveals OpenAI's $11.5 Billion Quarterly Loss](#item-5) ⭐️ 8.0/10
6. [China Fines Futu, Tiger Brokers Over Cross-Border Securities](#item-6) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Apple Open-Sources corecrypto with Formal Proofs for Quantum-Safe Algorithms](https://security.apple.com/blog/formal-verification-corecrypto/) ⭐️ 9.0/10

Apple has open-sourced its corecrypto cryptographic library, including formally verified implementations of the quantum-safe algorithms ML-KEM and ML-DSA, and released end-to-end mathematical proofs using the Isabelle theorem prover to ensure correctness against NIST standards. This sets a new benchmark for cryptographic security assurance by combining real-world deployment on billions of devices with rigorous formal verification, and it encourages broader adoption of post-quantum cryptography in the industry. The open-source release includes the corecrypto C code and hand-optimized ARM64 assembly, along with custom verification tools and Isabelle theory libraries for independent review; the verified algorithms are already used in iMessage and VPN products.

telegram · zaihuapd · May 23, 04:49

**Background**: corecrypto is Apple's low-level cryptographic library powering encryption on over 2.5 billion active devices. Formal verification uses mathematical proofs to show that code exactly matches a specification, eliminating entire classes of bugs. ML-KEM (formerly Kyber) and ML-DSA (formerly Dilithium) are NIST-standardized post-quantum algorithms resistant to attacks from future quantum computers.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ML-KEM">ML-KEM</a></li>
<li><a href="https://en.wikipedia.org/wiki/ML-DSA">ML-DSA</a></li>
<li><a href="https://en.wikipedia.org/wiki/Isabelle_theorem_prover">Isabelle theorem prover</a></li>

</ul>
</details>

**Tags**: `#cryptography`, `#formal verification`, `#apple`, `#quantum-safe`, `#open source`

---

<a id="item-2"></a>
## [80386 Microcode Disassembled in Detail](https://www.reenigne.org/blog/80386-microcode-disassembled/) ⭐️ 8.0/10

A detailed disassembly of the Intel 80386's microcode has been published, revealing the internal control logic of this classic 32-bit processor. This reverse engineering achievement provides unprecedented insight into the design of a foundational CPU, benefiting retrocomputing enthusiasts and computer architecture researchers alike. The disassembly likely involved analyzing high-resolution die photographs and reconstructing the microcode ROM contents; the 80386 uses microprogramming to implement its x86 instruction set.

hackernews · nand2mario · May 23, 12:11 · [Discussion](https://news.ycombinator.com/item?id=48247004)

**Background**: Microcode is a low-level layer of instructions that controls a CPU's internal operations, acting as an interpreter for machine code. The Intel 80386, released in 1985, was the first 32-bit processor in the x86 line and a cornerstone of modern computing. Disassembling its microcode is a highly complex reverse engineering task that requires deep knowledge of the chip's layout and logic.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Microcode">Microcode - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Intel_80386">Intel 80386</a></li>

</ul>
</details>

**Discussion**: Commenters expressed admiration for the reverse engineering effort, with some asking about the technical process of extracting microcode from die images. Related projects like z386, an open-source 80386 built around original microcode, were also mentioned.

**Tags**: `#reverse engineering`, `#CPU microcode`, `#80386`, `#computer architecture`, `#retrocomputing`

---

<a id="item-3"></a>
## [Anthropic's Project Glasswing AI Finds 10,000+ Critical Vulnerabilities](https://www.anthropic.com/research/glasswing-initial-update) ⭐️ 8.0/10

Anthropic's Project Glasswing, using the Claude Mythos Preview model, discovered over 10,000 high-risk vulnerabilities across critical software and open-source projects within a month, with a 90.6% true positive rate across reviewed submissions. This breakthrough demonstrates that AI can dramatically accelerate vulnerability discovery, but also exposes a critical patching bottleneck that the software industry must address to keep pace. Partners such as Cloudflare report vulnerability discovery speeds increased by over tenfold. Of 1,752 reviewed vulnerabilities, 90.6% were true positives, and Anthropic has open-sourced the Claude Security tool to help enterprises with remediation.

telegram · zaihuapd · May 23, 03:16

**Background**: Project Glasswing is a cybersecurity initiative by Anthropic that brings together over 45 organizations, including Apple and Google, to use the unreleased Claude Mythos Preview model for vulnerability discovery. The model is described as a new frontier-tier model above Opus. The project highlights that while AI can find vulnerabilities faster than humans, the manual process of verification, disclosure, and patching remains a bottleneck.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/research/glasswing-initial-update">Project Glasswing: An initial update \ Anthropic</a></li>
<li><a href="https://www.wired.com/story/anthropic-mythos-preview-project-glasswing/">Anthropic Teams Up With Its Rivals to Keep AI From Hacking ...</a></li>
<li><a href="https://www.forbes.com/sites/paulocarvao/2026/04/08/five-reasons-anthropic-kept-its-cybersecurity-breakthrough-invite-only/">Five Reasons Anthropic Kept Its Cybersecurity Breakthrough ...</a></li>

</ul>
</details>

**Tags**: `#AI`, `#cybersecurity`, `#vulnerability discovery`, `#Anthropic`, `#software security`

---

<a id="item-4"></a>
## [Microsoft pushes Claude Code to key teams](https://t.me/zaihuapd/41535) ⭐️ 8.0/10

Microsoft is internally promoting Anthropic's Claude Code across major engineering teams, including non-technical employees, and requiring developers to use both Claude Code and GitHub Copilot for comparison. This move signals Microsoft's pragmatic adoption of a competitor's AI coding tool, potentially reshaping enterprise AI workflows and intensifying the rivalry between Claude Code and GitHub Copilot. Teams affected include CoreAI, Windows, Microsoft 365, and Outlook; non-technical staff are encouraged to use Claude Code for prototyping.

telegram · zaihuapd · May 23, 06:05

**Background**: Claude Code is an AI coding agent developed by Anthropic, integrated with GitHub, GitLab, and command-line tools. It uses constitutional AI for safety. Microsoft also develops GitHub Copilot, a competing AI pair-programming tool. The internal comparison suggests Microsoft is evaluating which tool better suits its engineering needs.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>
<li><a href="https://claude.com/product/claude-code">Claude Code by Anthropic | AI Coding Agent, Terminal, IDE</a></li>

</ul>
</details>

**Tags**: `#AI coding`, `#Claude Code`, `#Microsoft`, `#GitHub Copilot`, `#enterprise AI`

---

<a id="item-5"></a>
## [Microsoft's Report Reveals OpenAI's $11.5 Billion Quarterly Loss](https://t.me/zaihuapd/41537) ⭐️ 8.0/10

Microsoft's latest earnings report disclosed that its equity method investment in OpenAI reduced its quarterly net profit by $3.1 billion, implying OpenAI suffered a net loss of approximately $11.5 billion in the quarter based on Microsoft's roughly 27% stake. This disclosure highlights the enormous cash burn rate in AI development, with OpenAI's quarterly loss nearly three times its $4.3 billion revenue in the first half of the year, underscoring the financial risks and high costs of leading AI research. Microsoft has invested $11.6 billion of its committed $13 billion in OpenAI; if pre-tax loss and actual stake of 32.5% are used, the loss could exceed $12 billion.

telegram · zaihuapd · May 23, 07:40

**Background**: Equity method accounting is used when an investor has significant influence (typically 20-50% ownership) over an investee, recording its share of the investee's profit or loss as investment income. OpenAI is a private company developing advanced AI models like GPT, requiring vast computing resources and talent, leading to high operating costs. This accounting treatment allowed Microsoft's earnings to reflect OpenAI's financial performance.

<details><summary>References</summary>
<ul>
<li><a href="https://www.dongao.com/zjzcgl/zjkjsw/201905131026788.shtml">权 益 法 下可辨认净 资 产公允价值与账面价值怎么调整_东奥会计在线</a></li>
<li><a href="http://www.canet.com.cn/acc/zzjq/200807/19-36934.html">canet.com.cn/acc/zzjq/200807/19-36934.html</a></li>

</ul>
</details>

**Tags**: `#OpenAI`, `#Microsoft`, `#AI industry`, `#financial losses`, `#equity method accounting`

---

<a id="item-6"></a>
## [China Fines Futu, Tiger Brokers Over Cross-Border Securities](https://t.me/zaihuapd/41539) ⭐️ 8.0/10

Chinese regulators proposed fines of 18.5 billion yuan for Futu Holdings and 4.11 billion yuan for Tiger Brokers subsidiaries for conducting unauthorized cross-border securities, mutual fund sales, and futures businesses in mainland China. This marks a significant regulatory crackdown on fintech brokerages operating across borders, signaling stricter enforcement of China's securities laws and potentially reshaping the landscape for cross-border investment platforms. Futu Holdings was also ordered to rectify operations, and its CEO Li Hua faces a personal fine of 1.25 million yuan. The penalties are subject to further proceedings and final decisions.

telegram · zaihuapd · May 23, 10:58

**Background**: Futu Holdings and Tiger Brokers are major online brokerages based in Hong Kong that offer securities trading services to mainland Chinese investors. Chinese law requires firms providing securities services in China to hold appropriate licenses. These fines target their alleged unlicensed cross-border activities, which have been a focus of regulatory concern amid efforts to control capital outflows and maintain market order.

**Tags**: `#regulation`, `#fintech`, `#China`, `#securities`, `#enforcement`

---