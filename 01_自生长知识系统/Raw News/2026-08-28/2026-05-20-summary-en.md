---
layout: default
title: "Horizon Summary: 2026-05-20 (EN)"
date: 2026-05-20
lang: en
---

> From 44 items, 11 important content pieces were selected

---

1. [Andrej Karpathy Joins Anthropic's Pre-Training Team](#item-1) ⭐️ 9.0/10
2. [CISA contractor leaks AWS GovCloud keys on GitHub](#item-2) ⭐️ 9.0/10
3. [DeepSeek Vulnerability: Empty Chat '<think' Leaks User Data](#item-3) ⭐️ 9.0/10
4. [Google Unveils Gemini Omni for Conversational Video Editing](#item-4) ⭐️ 9.0/10
5. [Google Redesigns Search Box with AI Integration](#item-5) ⭐️ 8.0/10
6. [Forge boosts 8B model accuracy from 53% to 99% with guardrails](#item-6) ⭐️ 8.0/10
7. [Apple unveils new accessibility features with Apple Intelligence and agentic AI](#item-7) ⭐️ 8.0/10
8. [Gemini 3.5 Flash Launches with Higher Price, Wide Integration](#item-8) ⭐️ 8.0/10
9. [Proposal to rework Linux this_cpu ops for speed](#item-9) ⭐️ 8.0/10
10. [CXL Worsens Memory Management, Future Directions](#item-10) ⭐️ 8.0/10
11. [Lisuan 7G100: China's DX12 Gaming GPU Preorder on May 20](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Andrej Karpathy Joins Anthropic's Pre-Training Team](https://twitter.com/karpathy/status/2056753169888334312) ⭐️ 9.0/10

Andrej Karpathy announced on X that he has joined Anthropic, specifically working on the pre-training team responsible for the massive training runs that give Claude its core knowledge and capabilities. Karpathy is a highly influential AI researcher and educator, and his move to Anthropic signals the lab's growing strength in frontier AI research and may impact both model development and AI education. Karpathy will work on Anthropic's pre-training team, which handles large-scale training runs for Claude. He previously founded Eureka Labs and coined the term 'vibe coding' for AI-assisted programming.

hackernews · dmarcos · May 19, 15:07 · [Discussion](https://news.ycombinator.com/item?id=48194352)

**Background**: Pre-training is a self-supervised learning technique where a model is first trained on a large, unlabeled dataset to learn general representations, then fine-tuned for specific tasks. Karpathy is a co-founder of OpenAI, former Tesla AI Director, and a prominent educator known for projects like nanoGPT and his YouTube channel. Anthropic is a leading AI safety company, creator of the Claude model series.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Generative_pre-trained_transformer">Generative pre - trained transformer - Wikipedia</a></li>

</ul>
</details>

**Discussion**: The community largely expressed excitement about Karpathy joining Anthropic, with many hoping he continues his educational work despite potential NDA restrictions. Some users voiced concern about Anthropic becoming a dominant force that absorbs top talent, while others noted Karpathy had foreshadowed this move in a recent interview.

**Tags**: `#AI`, `#Anthropic`, `#Andrej Karpathy`, `#machine learning`, `#industry news`

---

<a id="item-2"></a>
## [CISA contractor leaks AWS GovCloud keys on GitHub](https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/) ⭐️ 9.0/10

A CISA contractor accidentally published AWS GovCloud access keys and a CSV file containing plaintext usernames and passwords for dozens of internal CISA systems on a public GitHub repository. This breach exposes highly sensitive U.S. government cloud infrastructure and internal credentials, undermining national security and highlighting severe lapses in security practices and incident response. The leaked credentials included AWS GovCloud keys for a CISA Workspace environment and a file named “AWS-Workspace-Firefox-Passwords.csv” with plaintext passwords. The contractor failed to respond when notified about the exposure.

hackernews · LelouBil · May 19, 07:45 · [Discussion](https://news.ycombinator.com/item?id=48190454)

**Background**: AWS GovCloud (US) is a compliant cloud environment designed to host sensitive and controlled unclassified information for U.S. government agencies, with restricted access to U.S. persons. CISA (Cybersecurity and Infrastructure Security Agency) is a federal agency responsible for protecting the nation's critical infrastructure from cyber threats.

<details><summary>References</summary>
<ul>
<li><a href="https://aws.amazon.com/govcloud-us/">AWS GovCloud (US) - Amazon Web Services</a></li>
<li><a href="https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/">AWS Services by Region</a></li>

</ul>
</details>

**Discussion**: Commenters expressed shock at the lack of response and the use of plaintext passwords, with some suggesting that the incident could be mistaken for a honeypot by foreign intelligence. Others highlighted the irony of using AWS services that offer better security features.

**Tags**: `#security`, `#breach`, `#CISA`, `#AWS`, `#GovCloud`

---

<a id="item-3"></a>
## [DeepSeek Vulnerability: Empty Chat '<think' Leaks User Data](https://t.me/zaihuapd/41461) ⭐️ 9.0/10

A critical session isolation vulnerability has been discovered in DeepSeek's Web and API dialogue systems, where an attacker can send an unclosed '<think' string in an empty conversation to retrieve other users' conversation histories, including sensitive data. This vulnerability poses a severe privacy risk, potentially exposing private code, API keys, and personal conversations of DeepSeek users, undermining trust in AI chat services and highlighting the need for robust session isolation in multi-tenant systems. The vulnerability was responsibly disclosed by reporter cancat2024 on May 11, 2026, and affects both the DeepSeek Web interface and API; the attacker only needs to submit an incomplete '<think' string in a fresh empty chat session to trigger data leakage.

telegram · zaihuapd · May 19, 11:33

**Background**: Session isolation is a security mechanism that ensures each user's chat sessions are kept separate from others. The '<think' token is a special token used by some AI models to indicate reasoning or internal thought processes. This vulnerability suggests a flaw in how DeepSeek handles incomplete special tokens, causing the model to incorrectly retrieve data from other sessions.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/tajerek/deepseek-web-api-proxy">GitHub - tajerek/ deepseek -web-api-proxy: OpenAI-compatible API...</a></li>
<li><a href="https://arxiv.org/html/2405.08644v1">Thinking Tokens for Language Modeling - arXiv.org</a></li>
<li><a href="https://huggingface.co/papers/2405.08644">Paper page - Thinking Tokens for Language Modeling</a></li>

</ul>
</details>

**Discussion**: On GitHub, community members noted that third-party deployments also exhibit the same behavior, suggesting the issue may stem from a hallucination-like effect in the model rather than a pure session management bug.

**Tags**: `#security`, `#vulnerability`, `#DeepSeek`, `#data leakage`, `#AI`

---

<a id="item-4"></a>
## [Google Unveils Gemini Omni for Conversational Video Editing](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/) ⭐️ 9.0/10

Google has announced Gemini Omni, a new multimodal AI model that allows users to edit videos through natural language conversation, with capabilities including physics understanding, character consistency, and SynthID digital watermarking. The first model, Gemini Omni Flash, is now available to Google AI Plus, Pro, and Ultra subscribers through the Gemini app, Google Flow, YouTube Shorts, and YouTube Create App. This marks a major step toward intuitive, AI-assisted video creation, potentially lowering the barrier for content creators and enabling more dynamic, real-time edits. The inclusion of SynthID watermarking also addresses growing concerns over AI-generated content authenticity. The model demonstrates inherent understanding of physics like gravity and fluid dynamics, and maintains character consistency across multiple edit iterations. All generated videos are embedded with SynthID digital watermarks for transparency, and Google plans to open the API to developers in the coming weeks.

telegram · zaihuapd · May 19, 18:23

**Background**: Multimodal AI models process multiple data types like text, images, and audio. Gemini Omni is Google's latest such model, bridging reasoning and creation to enable direct video editing via natural language. SynthID, developed by Google DeepMind, embeds imperceptible watermarks into AI-generated content that can be detected by specialized tools, helping to distinguish AI-made content from real footage.

<details><summary>References</summary>
<ul>
<li><a href="https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/">Introducing Gemini Omni</a></li>
<li><a href="https://deepmind.google/models/synthid/">SynthID — Google DeepMind</a></li>

</ul>
</details>

**Discussion**: Community comments are cautiously positive but critical of physics realism. Users point out specific examples where the model violates physics (e.g., a marble speeding up without energy source, Jenga brick tower bricks disappearing). Some compare it unfavorably to existing tools like Seedance, while others note fundamental issues with deep spatial understanding in video generation.

**Tags**: `#multimodal AI`, `#video generation`, `#Google Gemini`, `#AI model`, `#natural language processing`

---

<a id="item-5"></a>
## [Google Redesigns Search Box with AI Integration](https://blog.google/products-and-platforms/products/search/search-io-2026/) ⭐️ 8.0/10

At Google I/O 2026, Google announced a major redesign of its search box, integrating a new AI mode powered by Gemini, its large language model, to provide direct, synthesized answers rather than just links. This shift could fundamentally change how users interact with search, reducing traffic to external websites and raising concerns about information reliability and the future of web publishing. The new search box moves away from the classic blue link format, presenting AI-generated summaries that pull from multiple sources but may lack clear attribution, and users can opt into 'AI Mode' to get conversational answers.

hackernews · berkeleyjunk · May 19, 18:34 · [Discussion](https://news.ycombinator.com/item?id=48197370)

**Background**: Google has long been the dominant search engine, using algorithms to rank web pages. Large language models (LLMs) like Gemini can generate human-like text by predicting words based on training data, enabling a more direct answer style. At I/O 2026, Google deepens its commitment to AI-first search.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Gemini">Google Gemini - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Commenters expressed concerns about AI-generated answers sounding authoritative but potentially aggregating unreliable sources, and the risk of 'Google Zero' where traffic to original sites dries up. Some users distrust LLM outputs for factual queries and prefer primary sources.

**Tags**: `#google`, `#search`, `#AI`, `#LLM`, `#UX`

---

<a id="item-6"></a>
## [Forge boosts 8B model accuracy from 53% to 99% with guardrails](https://github.com/antoinezambelli/forge) ⭐️ 8.0/10

Antoine Zambelli released Forge, an open-source reliability layer that uses domain-agnostic guardrails to dramatically improve local LLM accuracy on multi-step agentic tasks, achieving 99.3% on an 8B model compared to 53% without. Forge narrows the accuracy gap between free local models and costly frontier APIs to less than 1 percentage point, enabling practical self-hosted agentic systems without cloud costs. It also reveals critical infrastructure factors (e.g., serving backend choice) that standard benchmarks ignore. Forge consists of five independently toggleable guardrail layers; retry nudges and error recovery are most impactful per ablation studies. The system includes a novel ToolResolutionError exception class to distinguish between a tool returning data and returning nothing, preventing silent data corruption.

hackernews · zambelli · May 19, 12:23 · [Discussion](https://news.ycombinator.com/item?id=48192383)

**Background**: Agentic workflows involve multi-step tasks where an LLM calls tools and reasons iteratively. Without guardrails, per-step errors compound: 90% per-step accuracy yields ~40% failure rate over 5 steps. Forge’s guardrails address this by adding retry mechanisms, error recovery, step enforcement, and context management optimized for consumer hardware.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/@prklipi/guardrails-in-llm-systems-building-safe-and-reliable-ai-applications-1b4780798720">Guardrails in LLM Systems: Building Safe and Reliable AI... | Medium</a></li>
<li><a href="https://www.ibm.com/think/topics/agentic-workflows">What are agentic workflows? - IBM</a></li>

</ul>
</details>

**Discussion**: Community members largely praised Forge, noting that small local models with a proper harness can perform excellently. One user highlighted the tool-call ambiguity (e.g., grep returning exit code 1) as a common failure mode that retry nudges address. Another shared parallel experiences with frontier scale and the value of appropriately scaled solutions.

**Tags**: `#LLM`, `#guardrails`, `#agentic tasks`, `#open-source`, `#reliability`

---

<a id="item-7"></a>
## [Apple unveils new accessibility features with Apple Intelligence and agentic AI](https://www.apple.com/newsroom/2026/05/apple-unveils-new-accessibility-features-and-updates-with-apple-intelligence/) ⭐️ 8.0/10

Apple announced new accessibility features powered by Apple Intelligence, including agentic AI capabilities that can autonomously perform tasks for users with disabilities. This integration brings advanced AI to accessibility, potentially improving independence for disabled users and setting a precedent for agentic AI in consumer products. The features leverage on-device and server AI processing, similar to other Apple Intelligence functions. Agentic AI allows the system to proactively assist users based on context.

hackernews · interpol_p · May 19, 12:04 · [Discussion](https://news.ycombinator.com/item?id=48192224)

**Background**: Apple Intelligence is Apple's generative AI system announced in 2024, available on devices with A17 Pro or M1+ chips. Agentic AI refers to AI systems that can act autonomously to achieve goals, often by using tools and making decisions within human-defined constraints.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Apple_Intelligence">Apple Intelligence</a></li>
<li><a href="https://en.wikipedia.org/wiki/Agentic_AI">Agentic AI</a></li>

</ul>
</details>

**Discussion**: Commenters praised the practical application of LLMs for accessibility but criticized Apple's speech-to-text transcription as behind competitors. Some noted the high-speed voiceover demonstration was actually inaccessible to blind users.

**Tags**: `#accessibility`, `#Apple`, `#Apple Intelligence`, `#AI`, `#agentic AI`

---

<a id="item-8"></a>
## [Gemini 3.5 Flash Launches with Higher Price, Wide Integration](https://simonwillison.net/2026/May/19/gemini-35-flash/#atom-everything) ⭐️ 8.0/10

Google released Gemini 3.5 Flash as a generally available model at Google I/O, skipping the preview phase, and integrated it into key products including the Gemini app, Google Search, Google Antigravity, and Gemini API. This release marks a major update to Google's flagship model family with immediate broad deployment, but the significant price increase—3x that of its predecessor—signals a trend among AI labs testing customer price tolerance. The model ID is gemini-3.5-flash, with a knowledge cut-off of January 2025, supporting 1,048,576 input tokens and 65,536 output tokens, but lacking computer use capability. Pricing is $1.50 per million input tokens and $9 per million output tokens, and a new Interactions API (beta) offers server-side history management.

rss · Simon Willison · May 19, 22:40

**Background**: The Gemini Flash series is Google's cost-efficient model line designed for high-volume, low-latency tasks. Google I/O is the company's annual developer conference where major product announcements are made. Recent trends show other AI labs like OpenAI and Anthropic also raising prices on newer model versions, indicating a shift toward monetization.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Antigravity">Google Antigravity</a></li>
<li><a href="https://sourceforge.net/software/product/Gemini-Enterprise-Agent-Platform/">Gemini Enterprise Agent Platform Reviews in 2026</a></li>

</ul>
</details>

**Tags**: `#Gemini`, `#Google I/O`, `#AI model`, `#machine learning`, `#release`

---

<a id="item-9"></a>
## [Proposal to rework Linux this_cpu ops for speed](https://lwn.net/Articles/1073395/) ⭐️ 8.0/10

At the 2026 LSFMM+BPF Summit, Yang Shi proposed reimplementing Linux's this_cpu operations using per-CPU page tables to give each variable the same address on every CPU, eliminating the need to disable preemption on architectures like Arm. This change could significantly improve performance on non-x86 architectures by reducing overhead from multi-instruction sequences and preemption disabling, potentially benefiting a wide range of server and mobile devices that use Arm and other CPUs. The proposal requires double-mapping per-CPU variables (one global mapping for initialization, one per-CPU mapping for access), and faces historical opposition from Linus Torvalds due to TLB management challenges. Benchmarks on a 160-core Arm system showed 13-18% reduction in kernel-build system time.

rss · LWN.net · May 19, 14:30

**Background**: The kernel's this_cpu operations provide fast access to per-CPU variables, which are arrays indexed by CPU number to avoid locking. On x86, segment registers enable single-instruction atomic access; on architectures like Arm, multi-instruction sequences require preemption to be disabled, causing performance loss. The proposal aims to eliminate that penalty by making per-CPU variables have uniform addresses via per-CPU page tables.

<details><summary>References</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/v7.1-rc4/core-api/this_cpu_ops.html">this_cpu operations — The Linux Kernel documentation</a></li>
<li><a href="https://0xax.gitbooks.io/linux-insides/content/Concepts/linux-cpu-1.html">Per-CPU variables · Linux Inside</a></li>

</ul>
</details>

**Tags**: `#kernel`, `#performance`, `#per-CPU`, `#LSFMM`, `#Linux`

---

<a id="item-10"></a>
## [CXL Worsens Memory Management, Future Directions](https://lwn.net/Articles/1072858/) ⭐️ 8.0/10

Dan Williams presented an overview of how Compute Express Link (CXL) technology is exacerbating memory-management problems in Linux and discussed upcoming developments at the 2026 Linux Storage, Filesystem, Memory Management, and BPF Summit. As CXL becomes more prevalent in data centers, the kernel must address challenges like hot-plug memory, firmware interference, and error handling to ensure reliable and efficient memory management for next-generation systems. CXL memory is accessed over PCIe with higher latency than remote NUMA nodes, and its hot-plug nature means portions of RAM can disappear. The kernel is adopting a 'code-first' policy to document hardware deviations, and error handling may involve kernel panics.

rss · LWN.net · May 19, 14:15

**Background**: Compute Express Link (CXL) is an open standard interconnect for high-speed CPU-to-device and CPU-to-memory connections, aimed at high-performance data centers. It provides shared memory nodes over PCIe, but with higher latency than local memory. Non-Uniform Memory Access (NUMA) is a memory design where access time depends on memory location relative to a processor; remote NUMA nodes are slower than local ones. CXL memory typically has worse latency than even remote NUMA nodes, challenging existing memory management.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Compute_Express_Link">Compute Express Link - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Non-uniform_memory_access">Non-uniform memory access - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#CXL`, `#memory management`, `#Linux kernel`, `#data center`, `#hardware architecture`

---

<a id="item-11"></a>
## [Lisuan 7G100: China's DX12 Gaming GPU Preorder on May 20](https://videocardz.com/newz/lisuan-confirms-7g100-preorder-launch-on-may-20-chinas-dx12-gaming-gpu-with-support-for-100-games) ⭐️ 8.0/10

Lisuan Technology confirms the LX 7G100 gaming GPU will begin preorder on May 20 at 8 PM on JD.com. It features 12GB GDDR6, supports DirectX 12 and Vulkan 1.3, and claims performance comparable to the Nvidia RTX 4060. This is a significant milestone for domestic Chinese GPUs in the consumer gaming market, as it is one of the few Chinese-made graphics cards with full DX12 support. If real-world performance matches claims, it could boost the domestic GPU ecosystem and reduce reliance on foreign hardware. The card has passed WHQL certification and over 100 games, including Black Myth: Wukong and Cyberpunk 2077, have been tested for compatibility. However, the claimed RTX 4060-level performance may come from synthetic benchmarks, and real gaming performance depends on driver optimization and game compatibility.

telegram · zaihuapd · May 19, 08:57

**Background**: Chinese GPU makers have traditionally lagged in the consumer gaming segment, with most previous offerings lacking support for modern graphics APIs like DirectX 12. The Lisuan 7G100 aims to change that by supporting DX12 and Vulkan 1.3, making it compatible with a wide range of mainstream PC games. WHQL certification indicates it has passed Microsoft's Windows Hardware Quality Labs testing, ensuring driver stability.

**Tags**: `#国产GPU`, `#DX12`, `#游戏显卡`, `#硬件`, `#消费电子`

---