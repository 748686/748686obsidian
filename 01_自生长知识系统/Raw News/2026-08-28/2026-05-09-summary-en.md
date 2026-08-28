---
layout: default
title: "Horizon Summary: 2026-05-09 (EN)"
date: 2026-05-09
lang: en
---

> From 48 items, 17 important content pieces were selected

---

1. [Google's reCAPTCHA Update Blocks De-Googled Android Users](#item-1) ⭐️ 8.0/10
2. [AI is breaking two vulnerability cultures](#item-2) ⭐️ 8.0/10
3. [Meshtastic: Off-Grid LoRa Mesh Messaging](#item-3) ⭐️ 8.0/10
4. [Mojo 1.0 Beta Released](#item-4) ⭐️ 8.0/10
5. [Real UUID v4 Collision Sparks Debate on Randomness Quality](#item-5) ⭐️ 8.0/10
6. [Using Claude Code: The Unreasonable Effectiveness of HTML](#item-6) ⭐️ 8.0/10
7. [Forgejo 'carrot disclosure' sparks security debate](#item-7) ⭐️ 8.0/10
8. [DAMON Subsystem Gets Major Update at LSFMM+BPF 2026](#item-8) ⭐️ 8.0/10
9. [AI2 Releases EMO: 1B-Active MoE with Document-Level Routing](#item-9) ⭐️ 8.0/10
10. [Z-lab releases DFlash speculator for Gemma 4 26B](#item-10) ⭐️ 8.0/10
11. [DeepSeek Reportedly Seeks $7.35B Funding, Plans V4.1 Release in June](#item-11) ⭐️ 8.0/10
12. [Canvas hacked by ShinyHunters, disrupting US schools finals week](#item-12) ⭐️ 8.0/10
13. [Cloudflare lays off 1100+ amid AI restructuring](#item-13) ⭐️ 8.0/10
14. [Anthropic eyes $100B+ funding, $1T valuation, overtaking OpenAI](#item-14) ⭐️ 8.0/10
15. [US suspects Nvidia chips smuggled to Alibaba via Thailand](#item-15) ⭐️ 8.0/10
16. [DeepSeek Reportedly Eyes $45B Valuation in First Funding Round](#item-16) ⭐️ 8.0/10
17. [Apple may end TSMC's exclusive chip manufacturing, eye Intel 18A](#item-17) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Google's reCAPTCHA Update Blocks De-Googled Android Users](https://reclaimthenet.org/google-broke-recaptcha-for-de-googled-android-users) ⭐️ 8.0/10

Google has updated its reCAPTCHA service to use remote attestation, causing it to fail on de-googled Android devices that lack Google Play Services and certified hardware. This effectively blocks users of custom ROMs like GrapheneOS from accessing websites that employ the new reCAPTCHA. This update significantly impacts privacy-focused users who choose de-googled Android, as it forces them to either accept hardware attestation tied to Google's servers or lose access to many websites. It echoes the controversial Web Environment Integrity (WEI) proposal, raising concerns about user autonomy and the future of open web access. The new reCAPTCHA relies on remote attestation, which uses hardware-bound keys (EK → AIK) to verify device integrity, potentially allowing Google to link attestations to specific devices. This breaks compatibility with custom ROMs and devices without Google's Trusted Execution Environment, such as those running LineageOS or CalyxOS.

hackernews · anonymousiam · May 8, 18:45 · [Discussion](https://news.ycombinator.com/item?id=48067119)

**Background**: De-googled Android refers to Android Open Source Project (AOSP) builds without Google services, often used for privacy. Remote attestation is a Trusted Computing technology that allows a remote party to verify a device's software and hardware state using secure enclaves and hardware keys. Previously, Google proposed Web Environment Integrity (WEI) to achieve similar goals on the web, but it was abandoned after widespread criticism. The new reCAPTCHA effectively implements a form of remote attestation, drawing parallels to WEI.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Remote_attestation">Remote attestation</a></li>
<li><a href="https://en.wikipedia.org/wiki/Web_Environment_Integrity">Web Environment Integrity</a></li>
<li><a href="https://itsfoss.com/android-distributions-roms/">5 De-Googled Android-based Operating Systems - It's FOSS I de-Googled my Android phone and actually liked it - How-To Geek I tried completely de-Googled Android — here's what happened 9 Best Degoogled Phones | True Stock Android Without Tracking e Foundation - deGoogled unGoogled smartphone operating ... Ultimate Guide to De-Googled Android Privacy Top DeGoogled Phones OS Compared - Efani</a></li>

</ul>
</details>

**Discussion**: Community members expressed strong opposition, with many vowing to avoid hardware attestation controlled by Google. Some commenters recommended alternative CAPTCHA services, while others described moving banks or self-hosting services to reduce dependence on Google. The technical discussion focused on how remote attestation could enable device tracking via the EK-AIK link.

**Tags**: `#reCAPTCHA`, `#Android`, `#privacy`, `#remote attestation`, `#degoogling`

---

<a id="item-2"></a>
## [AI is breaking two vulnerability cultures](https://www.jefftk.com/p/ai-is-breaking-two-vulnerability-cultures) ⭐️ 8.0/10

AI is accelerating the long-standing conflict between coordinated vulnerability disclosure (CVD) and full disclosure, a trend predicted before the rise of LLMs. This shift undermines the traditional CVD model, as AI can generate exploits faster than patches can be coordinated, increasing risk for organizations that cannot patch quickly and potentially shifting the security landscape toward full disclosure. The catalyst is software transparency: widespread open-source adoption and improved reversing tools have made closed-source software no longer effectively obscure. AI further lowers the barrier for exploit generation, making embargoed patches increasingly difficult to protect.

hackernews · speckx · May 8, 17:55 · [Discussion](https://news.ycombinator.com/item?id=48066524)

**Background**: In computer security, coordinated vulnerability disclosure (CVD) allows vendors time to patch before public disclosure, while full disclosure releases details immediately. The tension between these approaches has existed for decades, but AI's ability to rapidly analyze code and generate exploits is accelerating the conflict.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure">Coordinated vulnerability disclosure</a></li>
<li><a href="https://en.wikipedia.org/wiki/Full_disclosure_(computer_security)">Full disclosure (computer security) - Wikipedia</a></li>
<li><a href="https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html">Vulnerability Disclosure - OWASP Cheat Sheet Series</a></li>

</ul>
</details>

**Discussion**: Comments from experts like tptacek, freeqaz, and rikafurude21 note that the crackup was predicted long before LLMs, and cite examples like Log4Shell where patch commits were exploited before the official release. Animats warns that AI makes attacks faster, and the world is already at cyberwar. Overall, the community sees AI as amplifying existing vulnerabilities rather than creating a new problem.

**Tags**: `#AI`, `#vulnerability disclosure`, `#security`, `#open source`, `#LLMs`

---

<a id="item-3"></a>
## [Meshtastic: Off-Grid LoRa Mesh Messaging](https://meshtastic.org/docs/introduction/) ⭐️ 8.0/10

Meshtastic is an open-source project that enables low-power, long-range text messaging over a decentralized mesh network using LoRa radios, without requiring a license. This technology provides a resilient, off-grid communication alternative that operates independently of cellular or internet infrastructure, appealing to hobbyists, emergency preparedness, and privacy advocates. Meshtastic uses the 915 MHz (US) or 868 MHz (EU) ISM bands with a maximum transmit power of 100 mW (FCC) or 25 mW (ETSI), and supports encryption, GPS location sharing, and integration with MQTT for internet bridging.

hackernews · ColinWright · May 8, 11:22 · [Discussion](https://news.ycombinator.com/item?id=48061566)

**Background**: LoRa (Long Range) is a spread spectrum modulation technique that allows low-power devices to communicate over distances up to several kilometers in rural areas. Mesh networking enables devices to relay messages through intermediate nodes, extending coverage. Meshtastic builds on these concepts to create a decentralized text messaging system that does not rely on any central infrastructure.

<details><summary>References</summary>
<ul>
<li><a href="https://www.seeedstudio.com/blog/2025/07/10/meshtastic-off-grid-mesh-network/">What Is Meshtastic? Build Your Off-Grid Mesh Network in 2025</a></li>
<li><a href="https://en.wikipedia.org/wiki/LoRa">LoRa - Wikipedia</a></li>

</ul>
</details>

**Discussion**: The community is excited about Meshtastic, with users comparing it to the early internet and noting it encourages ham radio licensing. Some express surprise that off-grid mesh technology has not advanced beyond basic text messaging, while the Philadelphia mesh map example shows active local nodes.

**Tags**: `#mesh networking`, `#LoRa`, `#off-grid communication`, `#decentralization`, `#ham radio`

---

<a id="item-4"></a>
## [Mojo 1.0 Beta Released](https://mojolang.org/) ⭐️ 8.0/10

Modular Inc. released the Mojo 1.0 beta, a high-performance programming language combining Python-like syntax with Rust's ownership model and Zig's compile-time metaprogramming (comptime), targeting machine learning and systems programming. The company plans to open-source Mojo in Fall 2026. Mojo aims to bridge the gap between high-level usability and low-level performance, potentially attracting Python developers who need more speed without switching to C++ or Rust. Its unique use of LLVM and MLIR could set a new standard for domain-specific languages in AI and systems. Mojo's ownership model is similar to Rust's, ensuring memory safety without a garbage collector, while its comptime system is more powerful than Zig's, enabling extensive compile-time computation. It also features first-class SIMD support for vectorized operations.

hackernews · sbt567 · May 8, 02:49 · [Discussion](https://news.ycombinator.com/item?id=48057901)

**Background**: Ownership is a memory management concept where each value has a single owner, and the compiler enforces rules about borrowing and lifetimes, preventing memory errors without a garbage collector. Comptime (compile-time computation) allows code to be executed during compilation, enabling powerful metaprogramming and optimization. Mojo leverages these concepts to deliver high performance while retaining a Python-like syntax.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/coinmonks/understanding-ownership-in-rust-with-examples-73835ba931b1">Understanding Ownership in Rust with Examples | by Luis... | Medium</a></li>
<li><a href="https://zig.guide/language-basics/comptime/">Comptime | zig .guide</a></li>

</ul>
</details>

**Discussion**: Community reactions are generally positive, with users praising Mojo's ownership model, comptime, and SIMD support. However, some express skepticism about Python compatibility issues and the delay in open-sourcing until 2026. There are also concerns about competition from NVIDIA's CUDA Tile IR.

**Tags**: `#Mojo`, `#programming language`, `#ML`, `#performance`, `#open source`

---

<a id="item-5"></a>
## [Real UUID v4 Collision Sparks Debate on Randomness Quality](https://news.ycombinator.com/item?id=48060054) ⭐️ 8.0/10

A developer reported a genuine UUID v4 collision in production with only 15,000 records, using the npm uuid package on the backend. The collision occurred between a record from 2025 and a new insertion, producing the identical UUID b6133fd6-70fe-4fe3-bed6-8ca8fc9386cd. This event challenges the common assumption that UUID v4 collisions are practically impossible, highlighting the critical importance of high-quality entropy sources. It serves as a wake-up call for developers to audit their random number generation, especially in backend systems where collisions can have severe consequences. The database contained only about 15,000 records, making the collision statistically far beyond expected probabilities. The npm uuid package relies on the runtime's random number generator; on the backend, this typically uses cryptographic randomness, but a broken entropy source (e.g., insufficient seeding) could cause collisions.

hackernews · mittermayr · May 8, 07:57

**Background**: UUID version 4 (v4) generates random identifiers using 122 bits of randomness, yielding 5.3×10^36 possible values. The probability of a collision is minuscule only if the random number generator is properly seeded and has high entropy. Poor entropy sources, due to hardware defects, software bugs, or misconfiguration, can dramatically increase collision rates. The npm uuid package uses the Web Crypto API or Node.js crypto module, which should be robust, but failures still occur.

<details><summary>References</summary>
<ul>
<li><a href="https://softwareengineering.stackexchange.com/questions/130261/uuid-collisions">random - UUID collisions - Software Engineering Stack Exchange</a></li>
<li><a href="https://stackoverflow.com/questions/1155008/how-unique-is-uuid">guid - How unique is UUID? - Stack Overflow</a></li>
<li><a href="https://www.npmjs.com/package/uuid">uuid - npm</a></li>

</ul>
</details>

**Discussion**: Community comments highlighted that entropy source failures are surprisingly common: hardware defects, software bugs, and poor seeding can degrade randomness. Some noted that generating UUIDs on the frontend is fundamentally unreliable due to browser limits and potential collision attacks. Others referenced the Pro Git book's example on SHA-1 collision probability to contextualize the rarity of the event, yet reaffirmed that practical failures can occur.

**Tags**: `#UUID`, `#randomness`, `#entropy`, `#software engineering`, `#systems design`

---

<a id="item-6"></a>
## [Using Claude Code: The Unreasonable Effectiveness of HTML](https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/#atom-everything) ⭐️ 8.0/10

Anthropic's Thariq Shihipar published an article advocating for requesting HTML output from Claude instead of Markdown, providing concrete prompt examples and a collection site demonstrating richer explanations with SVG diagrams and interactive widgets. This challenges the common practice of defaulting to Markdown for LLM outputs, showing that HTML can significantly improve clarity and interactivity for explanations, code reviews, and technical documentation, potentially boosting developer productivity. The author suggests prompts like 'Create an HTML artifact that describes this PR', and Simon Willison experimented with GPT-5.5 to generate an interactive HTML explanation of a Linux exploit, demonstrating the approach's feasibility.

rss · Simon Willison · May 8, 21:00

**Background**: During the GPT-4 era, Markdown was preferred due to its token efficiency over HTML given the tight 8,192 token limit. However, with larger context windows, HTML's ability to embed SVG diagrams, interactive widgets, and in-page navigation makes it a superior format for rich explanations.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>

</ul>
</details>

**Tags**: `#Claude`, `#HTML`, `#Markdown`, `#LLM output`, `#prompt engineering`

---

<a id="item-7"></a>
## [Forgejo 'carrot disclosure' sparks security debate](https://lwn.net/Articles/1071499/) ⭐️ 8.0/10

Security researcher Julien Voisin used a controversial 'carrot disclosure' method to reveal alleged RCE vulnerabilities in Forgejo, bypassing the project's security policy. This incident highlights tensions between security researchers and open-source projects over disclosure norms, and could influence how projects handle future security reports. Voisin opened non-urgent pull requests for minor fixes rather than reporting the RCE privately, and only later published a blog post claiming a full RCE chain. He criticized Forgejo's security policy as overly formal.

rss · LWN.net · May 8, 16:30

**Background**: Forgejo is a software collaboration platform forked from Gitea in 2022, used by Codeberg and upcoming Fedora. 'Carrot disclosure' is a term coined by Voisin in 2024, where a researcher demonstrates exploitability by publishing redacted output, aiming to incentivize fixes without full disclosure.

<details><summary>References</summary>
<ul>
<li><a href="https://dustri.org/b/carrot-disclosure.html?ref=securitricks.com">Carrot disclosure | Personal blog of Julien (jvoisin) Voisin</a></li>

</ul>
</details>

**Tags**: `#Forgejo`, `#security`, `#RCE`, `#open-source`, `#disclosure`

---

<a id="item-8"></a>
## [DAMON Subsystem Gets Major Update at LSFMM+BPF 2026](https://lwn.net/Articles/1071256/) ⭐️ 8.0/10

SeongJae Park presented new DAMON capabilities including memory tiering via TPP-DAMON and NUMA-TPP-DAMON, data attributes monitoring, transparent huge pages support, and dynamic interleaving for CXL memory. These enhancements significantly improve Linux memory management efficiency, enabling better utilization of heterogeneous memory like CXL and providing user-space with finer-grained control. TPP-DAMON moved to a multiple-thread model due to single-thread slowness, and was merged for kernel 6.16 with control-group awareness in 6.19. Dynamic interleaving supports multiple destination nodes with weights but works only in virtual address spaces, merged in 6.17.

rss · LWN.net · May 8, 13:20

**Background**: DAMON (Data Access MONitor) is a Linux kernel subsystem that efficiently monitors memory access patterns and provides operations to manage memory accordingly. It spawns a kernel thread sampling accesses every 5ms, with results reported every 100ms, and imposes <0.1% overhead. Memory tiering refers to placing data across different memory types (e.g., RAM and CXL) based on access frequency.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.kernel.org/mm/damon/index.html">DAMON: Data Access MONitoring and Access-aware System Operations</a></li>
<li><a href="https://damonitor.github.io/">DAMON: Data Access Monitor | DAMON Project Website</a></li>
<li><a href="https://en.wikipedia.org/wiki/Memory_hierarchy">Memory hierarchy - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#Linux Kernel`, `#DAMON`, `#Memory Management`, `#LSFMM+BPF`

---

<a id="item-9"></a>
## [AI2 Releases EMO: 1B-Active MoE with Document-Level Routing](https://i.redd.it/zonmo2y79zzg1.png) ⭐️ 8.0/10

AI2 (Allen Institute for AI) has released EMO, a novel Mixture-of-Experts model with 1 billion active parameters out of 14 billion total, trained on 1 trillion tokens. The key innovation is document-level routing, where experts are clustered by domain (e.g., health, news) rather than by token-level surface patterns. This release demonstrates a promising direction in MoE design that could lead to more interpretable and domain-specialized models. If effective, it could enable efficient deployment by activating only relevant experts based on the input domain, potentially improving performance and reducing computation. EMO is an experimental model (not a final production model), having only undergone 1 trillion tokens of pretraining. The document-level routing mechanism clusters experts around domains like health and news, contrasting with typical MoE routing that learns token-level patterns.

reddit · r/LocalLLaMA · ghostderp · May 8, 20:57 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1t7kgy4/new_moe_from_ai2_emo/)

**Background**: Mixture of Experts (MoE) is a machine learning technique where multiple expert networks are each specialized in different parts of the data space; a gating network determines which experts to use per input. Traditional MoE routers operate at the token level, but document-level routing groups experts by domain, which could lead to more coherent expertise and easier interpretability.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>

</ul>
</details>

**Discussion**: The community reacted positively, with praise for AI2's consistent quality ('Allen AI does some great work') and excitement for the MoE direction hinted at earlier. Some noted it's an experimental model and wondered about its performance compared to others, with one user suggesting a smaller 200M active variant could be interesting.

**Tags**: `#MoE`, `#AI2`, `#EMO`, `#domain-specific routing`, `#LLM`

---

<a id="item-10"></a>
## [Z-lab releases DFlash speculator for Gemma 4 26B](https://huggingface.co/z-lab/gemma-4-26B-A4B-it-DFlash) ⭐️ 8.0/10

Z-lab released a DFlash speculator for the Gemma 4 26B model on Hugging Face, enabling faster speculative decoding via block diffusion drafting. DFlash promises better long-context performance than MTP due to its stateful design and parallel drafting, potentially benefiting users of large language models in inference serving. DFlash uses a lightweight block diffusion model for parallel token drafting, and it maintains persistent KV cache and RoPE offset state across iterations, which may degrade more gracefully than MTP in long contexts.

reddit · r/LocalLLaMA · PaceZealousideal6091 · May 8, 14:18 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1t79ayh/zlab_released_gemma426ba4bitdflash_anybody_tried/)

**Background**: Speculative decoding accelerates autoregressive generation by using a draft model to propose multiple tokens verified jointly by the target model. DFlash is a variant that generates drafts via block diffusion in a single forward pass, while MTP (Multi-Token Prediction) reuses the target model's KV cache but may suffer from ballooning cache in long contexts. The DFlash speculator is currently optimized for vLLM and may have higher memory requirements than MTP.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/z-lab/dflash">GitHub - z-lab/dflash: DFlash: Block Diffusion for Flash Speculative Decoding · GitHub</a></li>
<li><a href="https://arxiv.org/abs/2602.06036">[2602.06036] DFlash: Block Diffusion for Flash Speculative</a></li>

</ul>
</details>

**Discussion**: Community members corrected a misconception that MTP degrades faster in long contexts, pointing out that Gemma 4's MTP reuses the model's KV cache. Users reported mixed results: some saw high memory usage, others noted DFlash's stateful design is promising but limited to vLLM and small context sizes for now.

**Tags**: `#gemma-4`, `#dflash`, `#speculative decoding`, `#vLLM`, `#inference acceleration`

---

<a id="item-11"></a>
## [DeepSeek Reportedly Seeks $7.35B Funding, Plans V4.1 Release in June](https://www.reddit.com/r/LocalLLaMA/comments/1t7bfpw/reports_suggest_deepseek_is_seeking_735_billion/) ⭐️ 8.0/10

DeepSeek is reportedly seeking to raise approximately $7.35 billion (RMB 50 billion) in its first funding round, which would be the largest single fundraising round for a Chinese AI company. Additionally, the company plans to accelerate model iteration and release the V4.1 update of its V4 model in June. This massive funding round signals DeepSeek's aggressive push into commercialization and monetization, potentially reshaping the competitive landscape of AI model development. The accelerated release cadence also indicates a shift from pure research to product-driven innovation, which could impact open-source AI communities and the broader industry. The funding round is led by founder Liang Wenfeng who plans to contribute the maximum allowable amount. The company has informed some investors of plans to speed up model iteration, aligning with mainstream industry practices, and will launch V4.1 in June.

reddit · r/LocalLLaMA · External_Mood4719 · May 8, 15:34

**Background**: DeepSeek is a Chinese AI startup known for its large language models, such as DeepSeek V4, which features up to 1 trillion parameters and advanced reasoning capabilities. The V4 model was released in preview earlier this year with API pricing and a 1M context window. The company has previously focused on research but is now pivoting to commercialization with this significant funding.

<details><summary>References</summary>
<ul>
<li><a href="https://www.deepseek.com/en/">DeepSeek</a></li>
<li><a href="https://api-docs.deepseek.com/news/news260424">DeepSeek V 4 Preview Release | DeepSeek API Docs</a></li>

</ul>
</details>

**Discussion**: Community reactions are mixed: some express concern that such large funding will shift DeepSeek's focus from research to profit-making, potentially reducing open contributions. Others note inconsistencies in reported funding amounts (previously $300M) and caution that news should be verified from official sources.

**Tags**: `#AI`, `#funding`, `#DeepSeek`, `#AI models`, `#commercialization`

---

<a id="item-12"></a>
## [Canvas hacked by ShinyHunters, disrupting US schools finals week](https://www.cnn.com/2026/05/07/us/canvas-hack-strands-college-students-finals-week) ⭐️ 8.0/10

On May 7, 2026, the Canvas learning management system was hacked by the ShinyHunters group, causing widespread disruption during finals week at US schools. Instructure reported that Canvas was restored for most users later that evening after entering maintenance mode. This incident affects nearly 9,000 schools or organizations and leaked over 300 TB of data, including names, student IDs, and school emails. The timing during finals week directly disrupts student access to grades, assignments, and exams, highlighting vulnerabilities in critical educational infrastructure. ShinyHunters also claimed responsibility for an earlier incident on May 1, where usernames, email addresses, and student ID numbers were leaked. James Madison University had to postpone exams originally scheduled for Friday to Wednesday due to the outage.

telegram · zaihuapd · May 8, 04:30

**Background**: Canvas is a cloud-based learning management system (LMS) developed by Instructure, widely used by K-12, higher education, and corporate training. ShinyHunters is a notorious cybercrime group specializing in data breaches and extortion, active since 2020. Ransomware attacks often involve encrypting data and demanding payment, but in this case, the attackers displayed ransom notes on Canvas homepages.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Canvas_LMS">Canvas LMS</a></li>
<li><a href="https://en.wikipedia.org/wiki/ShinyHunters">ShinyHunters</a></li>

</ul>
</details>

**Tags**: `#网络安全`, `#数据泄露`, `#教育科技`, `#黑客事件`

---

<a id="item-13"></a>
## [Cloudflare lays off 1100+ amid AI restructuring](https://blog.cloudflare.com/building-for-the-future/) ⭐️ 8.0/10

Cloudflare announced on May 7, 2026, that it is laying off over 1,100 employees globally, citing massive internal AI adoption as the primary driver for organizational restructuring. This marks one of the most explicit links between AI expansion and large-scale workforce reduction at a major internet infrastructure company, signaling a broader industry trend where AI automation displaces human roles. The severance package includes full base salary through end of 2026, U.S. health insurance coverage through year-end, and extended equity vesting until August 15, 2026, with cliff period waived for employees under one year tenure.

telegram · zaihuapd · May 8, 08:15

**Background**: Cloudflare is a major content delivery network and internet security company. The company reported a 600% increase in internal AI usage across departments like engineering, HR, finance, and marketing in the past three months, with employees using AI agents for daily tasks. Enterprise AI agents are autonomous systems that can perceive environments, retain memory, and make independent decisions, increasingly adopted across industries.

<details><summary>References</summary>
<ul>
<li><a href="https://www.aeologic.com/blog/enterprise-ai-agent-architecture-guide/">Enterprise Agentic AI Architecture Guide 2026</a></li>
<li><a href="https://www.techtarget.com/searchenterpriseai/feature/AI-agents-increasingly-viable-for-enterprise-use">AI agents increasingly viable for enterprise use | TechTarget</a></li>

</ul>
</details>

**Tags**: `#Cloudflare`, `#Layoffs`, `#AI`, `#Tech Industry`, `#Restructuring`

---

<a id="item-14"></a>
## [Anthropic eyes $100B+ funding, $1T valuation, overtaking OpenAI](https://www.ft.com/content/a40cafcc-0fa4-4e70-9e24-90d826aea56d) ⭐️ 8.0/10

Anthropic is reportedly planning to raise hundreds of billions of dollars this summer to fund a major expansion of its AI computing infrastructure, with its valuation potentially reaching nearly $1 trillion and overtaking OpenAI. This marks a significant shift in the AI industry, as Anthropic's valuation would surpass OpenAI, reflecting investors' strong belief in its technology and growth trajectory, and could intensify competition for talent and compute resources. In the private secondary market on Forge Global, Anthropic's implied valuation has surged to between $1 trillion and $1.2 trillion, surpassing OpenAI's ~$880 billion valuation. Just this February, Anthropic raised $30 billion at a $380 billion valuation, meaning its expected valuation has more than doubled in a few months due to explosive enterprise customer growth.

telegram · zaihuapd · May 8, 11:15

**Background**: Forge Global is a marketplace for trading pre-IPO shares of private companies, and its secondary market valuations are often used as indicators of a private company's market value. Secondary market valuations reflect the price at which existing shares are traded among investors, and can differ from official fundraising valuations. They provide a real-time gauge of investor sentiment for private companies like Anthropic and OpenAI.

<details><summary>References</summary>
<ul>
<li><a href="https://forgeglobal.com/">Welcome To Forge - The Place To Buy And Sell Private Market</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Anthropic`, `#Funding`, `#Valuation`, `#OpenAI`

---

<a id="item-15"></a>
## [US suspects Nvidia chips smuggled to Alibaba via Thailand](https://www.bloomberg.com/news/articles/2026-05-08/us-said-to-suspect-nvidia-chips-smuggled-to-alibaba-via-thailand) ⭐️ 8.0/10

US prosecutors suspect Thai company OBON Corp. smuggled $2.5 billion worth of Super Micro servers containing advanced Nvidia chips to China, with Alibaba named as one of the end customers. This case could escalate US-China tech tensions, potentially tightening export controls and disrupting global AI supply chains, while also threatening Thailand's ambitions to become an AI hub. OBON was involved in creating Thailand's sovereign AI cloud Siam AI, which gained Nvidia partner status, but Alibaba denies any business relationship with Super Micro or OBON.

telegram · zaihuapd · May 8, 13:23

**Background**: Export controls restrict the sale of advanced Nvidia chips (such as H100 and H200) to China to prevent military use, driving smuggling routes through third countries like Thailand. A sovereign AI cloud is a government-operated AI infrastructure that ensures data sovereignty and compliance with local laws. Super Micro is a major server manufacturer known for high-performance systems used in AI and data centers.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Supermicro">Supermicro - Wikipedia</a></li>
<li><a href="https://www.microsoft.com/en-us/sovereignty">Discover Microsoft Sovereign Cloud | Microsoft</a></li>

</ul>
</details>

**Tags**: `#chip smuggling`, `#Nvidia`, `#Alibaba`, `#export controls`, `#geopolitics`

---

<a id="item-16"></a>
## [DeepSeek Reportedly Eyes $45B Valuation in First Funding Round](https://t.me/zaihuapd/41289) ⭐️ 8.0/10

DeepSeek is reportedly seeking its first external financing at a valuation of approximately $45 billion, with China's National Integrated Circuit Industry Investment Fund said to be in talks to lead the round. This would mark a significant state-backed investment in a leading Chinese AI company, signaling deeper government involvement in China's AI sector and potentially reshaping the competitive landscape. The $45 billion valuation would make DeepSeek one of the most valuable AI startups globally; this is its first large-scale external fundraising after previously relying on internal funding.

telegram · zaihuapd · May 8, 14:59

**Background**: DeepSeek is a Chinese AI company known for its large language models such as the V4 model. The National Integrated Circuit Industry Investment Fund, commonly known as the Big Fund, is a state-backed investment vehicle established in 2014 to support China's semiconductor industry. The fund has played a key role in boosting China's chip sector, with its first phase investing over 170 billion yuan.

<details><summary>References</summary>
<ul>
<li><a href="https://zh.wikipedia.org/wiki/国家大基金">国家大基金 - 维基百科，自由的百科全书</a></li>
<li><a href="https://baike.baidu.com/item/国家集成电路产业投资基金/15891498">国家集成电路产业投资基金_百度百科</a></li>
<li><a href="https://fortune.com/2026/04/24/deepseek-v4-ai-model-price-performance-china-open-source/">DeepSeek unveils V4 model, with rock-bottom prices ... - Fortune</a></li>

</ul>
</details>

**Tags**: `#DeepSeek`, `#AI`, `#China`, `#Funding`, `#Valuation`

---

<a id="item-17"></a>
## [Apple may end TSMC's exclusive chip manufacturing, eye Intel 18A](https://t.me/zaihuapd/41292) ⭐️ 8.0/10

According to The Wall Street Journal, Apple is considering ending TSMC's exclusive chip manufacturing relationship since 2014, potentially using Intel's 18A process for some mid-to-low-end chips as early as 2027. This move could significantly alter the semiconductor supply chain, reducing Apple's reliance on TSMC and boosting Intel's foundry business, while pressuring TSMC amid rising AI chip demand. Intel's role would be limited to manufacturing, not design, and the 18A process is a 1.8nm-class node that Intel claims offers competitive performance and efficiency. Apple's diversification aims to mitigate risk from TSMC's capacity constraints due to AI orders.

telegram · zaihuapd · May 8, 17:18

**Background**: Since 2014, Apple has relied exclusively on TSMC for manufacturing its A-series and M-series chips. Intel's 18A process is part of its foundry comeback, with production reportedly starting before TSMC's competing N2 node. Apple's move reflects a broader industry trend of diversifying chip sources.

<details><summary>References</summary>
<ul>
<li><a href="https://www.intel.com/content/www/us/en/foundry/process/18a.html">Intel 18A | See Our Biggest Process Innovation</a></li>
<li><a href="https://www.tomshardware.com/pc-components/cpus/intels-18a-production-starts-before-tsmcs-competing-n2-tech-heres-how-the-two-process-nodes-compare">Intel's 18A production starts before TSMC’s competing N2 tech ...</a></li>
<li><a href="https://www.tweaktown.com/news/111366/intels-new-18a-p-node-will-reportedly-provide-9-percent-higher-performance-and-18-percent-better-efficiency-than-18a/index.html">Intel's new 18A-P node will reportedly provide 9% higher ...</a></li>

</ul>
</details>

**Tags**: `#Apple`, `#Semiconductor`, `#TSMC`, `#Intel`, `#Supply Chain`

---