---
layout: default
title: "Horizon Summary: 2026-05-27 (EN)"
date: 2026-05-27
lang: en
---

> From 52 items, 13 important content pieces were selected

---

1. [Netherlands blocks US acquisition of Solvinity over sovereignty concerns](#item-1) ⭐️ 9.0/10
2. [Microsoft Copilot Cowork Data Exfiltration Vulnerability](#item-2) ⭐️ 9.0/10
3. [WAVE: A Portable GPU ISA for Cross-Vendor Kernel Deployment](#item-3) ⭐️ 9.0/10
4. [PrismML Releases Binary and Ternary Bonsai Image 4B Model](#item-4) ⭐️ 9.0/10
5. [Outsourcing plus local AI will soon become more economical than frontier labs](#item-5) ⭐️ 8.0/10
6. [Curl maintainers overwhelmed by AI-generated security reports](#item-6) ⭐️ 8.0/10
7. [EAMS: Equivariant Mesh Networks for Robust Anatomical Segmentation](#item-7) ⭐️ 8.0/10
8. [China Restricts Overseas Travel for AI Talent at Alibaba, DeepSeek](#item-8) ⭐️ 8.0/10
9. [Cactus Hybrid Router: 65k model matches frontier AI performance](#item-9) ⭐️ 8.0/10
10. [SkillOpt: Treating Markdown Skill Files as Trainable Parameters](#item-10) ⭐️ 8.0/10
11. [Iran Plans Permanent Internet Disconnect, Government-Only Access](#item-11) ⭐️ 8.0/10
12. [China Blocks Founders' Travel in Meta's Manus Acquisition Review](#item-12) ⭐️ 8.0/10
13. [Alipay Unveils Token Pay and AI Wallet](#item-13) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Netherlands blocks US acquisition of Solvinity over sovereignty concerns](https://www.politico.eu/article/netherlands-blocks-us-takeover-vital-digital-supplier/) ⭐️ 9.0/10

The Dutch government blocked Kyndryl's €100 million takeover of cloud provider Solvinity, which hosts the national digital identity system DigiD, citing public interest concerns after advice from intelligence agencies. This decision protects the privacy and digital sovereignty of Dutch citizens by preventing a US company from controlling critical infrastructure that handles sensitive identity data. It sets a precedent for other nations evaluating foreign ownership of essential digital services. The deal, valued at €100 million ($113 million), involved Kyndryl, a US-based IT infrastructure services provider spun off from IBM. The Dutch Ministry of Economic Affairs blocked the takeover following a recommendation from the country's intelligence agency, citing risks to national security and data protection.

hackernews · vrganj · May 26, 11:46 · [Discussion](https://news.ycombinator.com/item?id=48278406)

**Background**: DigiD is the Netherlands' official digital identity system, used by 16.5 million citizens for accessing government services such as tax filing and healthcare. Solvinity provides secure managed cloud services that host DigiD's infrastructure. Concerns arose because a US owner could be compelled by US laws like the CLOUD Act to hand over data, undermining Dutch data protection laws.

<details><summary>References</summary>
<ul>
<li><a href="https://www.reuters.com/technology/dutch-government-block-takeover-cloud-services-company-solvinity-by-us-based-2026-05-26/">Dutch block US takeover of Solvinity as against public ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/DigiD">DigiD</a></li>
<li><a href="https://www.solvinity.com/">Secure Managed Cloud | Solvinity</a></li>

</ul>
</details>

**Discussion**: Commenters expressed relief and approval, noting that the government's move was long overdue after parliament voted to end Solvinity's contract. There was debate about the need for cryptographic sovereignty where vendors cannot access data even under legal compulsion, and some questioned why the Netherlands cannot self-host an open-source identity solution for 20 million users.

**Tags**: `#cybersecurity`, `#digital sovereignty`, `#national security`, `#identity management`, `#privacy`

---

<a id="item-2"></a>
## [Microsoft Copilot Cowork Data Exfiltration Vulnerability](https://simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files/#atom-everything) ⭐️ 9.0/10

A prompt injection vulnerability in Microsoft Copilot Cowork allows attackers to exfiltrate files by sending emails with external images that trigger network requests, leveraging pre-authenticated OneDrive download links. This was discovered by PromptArmor and reported on May 26, 2026. This vulnerability highlights a critical design flaw in agentic AI systems, where autonomous agents can be tricked into leaking sensitive data. It underscores the ongoing challenge of securing LLM-based agents against prompt injection attacks, especially in widely-deployed enterprise products like Microsoft 365. The attack works because Copilot Cowork can send emails to the user's inbox without approval, and those emails can contain external images that make network requests. Additionally, OneDrive pre-authenticated links can be included in the email, allowing an attacker who obtains the link to download files directly.

rss · Simon Willison · May 26, 15:36

**Background**: Prompt injection is a security exploit where malicious inputs cause LLMs to behave unintendedly, often overriding system instructions. Agentic systems, like Copilot Cowork, are AI architectures that can operate autonomously by combining memory, planning, and tool use. Pre-authenticated links (PAR) are URLs that grant access to resources without requiring additional authentication, often used for sharing files. This combination creates a 'lethal trifecta' for data exfiltration.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Prompt_injection">Prompt injection - Wikipedia</a></li>
<li><a href="https://owasp.org/www-community/attacks/PromptInjection">Prompt Injection | OWASP Foundation</a></li>

</ul>
</details>

**Tags**: `#security`, `#AI`, `#Microsoft`, `#prompt injection`, `#data exfiltration`

---

<a id="item-3"></a>
## [WAVE: A Portable GPU ISA for Cross-Vendor Kernel Deployment](https://www.reddit.com/r/MachineLearning/comments/1to76tv/p_built_a_portable_gpu_isa_after_reading_too_many/) ⭐️ 9.0/10

A developer has open-sourced WAVE, a portable GPU instruction set architecture (ISA) and toolchain that allows a single GPU kernel to run on NVIDIA, AMD, Apple, and Intel GPUs. The project includes a compiler, thin backends for Metal, PTX, HIP, and SYCL, and PyTorch integration verified to produce identical training results across all backends. WAVE addresses the long-standing fragmentation in GPU programming by providing a single abstraction that works across major vendors, potentially reducing engineering overhead for ML and HPC applications. If widely adopted, it could simplify multi-GPU development and lower the barrier to entry for GPU computing. WAVE distills 11 hardware-invariant primitives from over 5,000 pages of vendor ISA documentation across 16 microarchitectures. The toolchain compiles kernels to a portable binary, and thin backends translate it to vendor-specific ISAs; the project has been verified on Apple M4 Pro, NVIDIA T4, and AMD MI300X GPUs.

reddit · r/MachineLearning · /u/not-your-typical-cs · May 26, 13:36

**Background**: GPU programming traditionally requires vendor-specific languages and toolchains, such as NVIDIA's CUDA and PTX, AMD's HIP, and Apple's Metal, making it difficult to write portable code. A GPU ISA defines the low-level instructions that a GPU executes, and a portable ISA can abstract away hardware differences. WAVE builds on this concept by creating a universal ISA that all major GPU vendors can target via thin backends.

<details><summary>References</summary>
<ul>
<li><a href="https://wave.ojima.me/">WAVE - The Universal GPU ISA | WAVE</a></li>
<li><a href="https://en.wikipedia.org/wiki/ROCm">ROCm - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#GPU`, `#ISA`, `#portability`, `#deep learning`, `#toolchain`

---

<a id="item-4"></a>
## [PrismML Releases Binary and Ternary Bonsai Image 4B Model](https://www.reddit.com/r/LocalLLaMA/comments/1togflk/prismml_just_released_binary_and_ternary_bonsai/) ⭐️ 9.0/10

PrismML released binary and ternary quantized versions of the Bonsai Image 4B text-to-image diffusion transformer, achieving a model size of only ~3GB and enabling fully local inference in the browser via WebGPU. This breakthrough democratizes AI image generation by allowing powerful text-to-image models to run on consumer hardware without requiring expensive GPUs or cloud services, significantly lowering the barrier to entry and preserving user privacy. The binary and ternary quantization reduces model weights to 1 bit and ~1.58 bits per parameter respectively, compressing a 4B parameter model from ~16GB to ~3GB. The models are released under the Apache-2.0 license and include official implementations for WebGPU inference.

reddit · r/LocalLLaMA · /u/xenovatech · May 26, 18:53

**Background**: Traditional diffusion models like FLUX use U-Net architectures, but recent innovations like Diffusion Transformers (DiTs) replace the U-Net with transformer backbones for better scalability. Extreme quantization techniques like binary and ternary quantization reduce model size by representing weights with very low bit-widths (1 or 1.58 bits), making models feasible for devices with limited memory. WebGPU is a modern browser API that allows web applications to leverage the GPU for accelerated computation, enabling local inference without server-side processing.

<details><summary>References</summary>
<ul>
<li><a href="https://ieeexplore.ieee.org/document/11250544">A Survey on Binary and Ternary Neural Networks and Their Realization in ...</a></li>
<li><a href="https://encord.com/blog/diffusion-models-with-transformers/">Scalability of Diffusion Models with Transformer Backbone | Encord</a></li>
<li><a href="https://dl.acm.org/doi/10.1145/3696410.3714553">WeInfer: Unleashing the Power of WebGPU on LLM Inference in Web Browsers | Proceedings of the ACM on Web Conference 2025</a></li>

</ul>
</details>

**Tags**: `#quantization`, `#diffusion`, `#text-to-image`, `#webgpu`, `#local-ai`

---

<a id="item-5"></a>
## [Outsourcing plus local AI will soon become more economical than frontier labs](https://www.signalbloom.ai/posts/outsourcing-plus-localai-will-soon-become-more-economical-vs-frontier-labs/) ⭐️ 8.0/10

A recent article argues that combining outsourcing with local or smaller AI models will soon be more cost-effective than using frontier model APIs from major AI labs like OpenAI and Anthropic. If accurate, this shift could reduce dependence on expensive frontier APIs, enabling smaller companies to access advanced AI capabilities and potentially transforming the software development and AI consulting industries. The article is speculative and based on trends in LLM pricing, noting that subscription-based access to models like Claude can be 10x-40x cheaper than API pricing, while developer skill and management remain critical factors.

hackernews · GodelNumbering · May 26, 12:08 · [Discussion](https://news.ycombinator.com/item?id=48278610)

**Background**: Frontier AI labs such as OpenAI, DeepMind, and Anthropic develop large, powerful models accessed via expensive APIs. Outsourcing involves hiring developers in lower-wage countries. The article suggests that combining smaller, local AI models with outsourced talent can match or exceed frontier model performance at lower cost, challenging the current API-centric model.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/Most_prestigious_AI_research_labs">Most prestigious AI research labs</a></li>
<li><a href="https://x.ai/api">API : Frontier Models for Reasoning & Enterprise | xAI</a></li>
<li><a href="https://openai.com/api/">Our API platform offers our latest models and guides for safety best...</a></li>

</ul>
</details>

**Discussion**: Commenters largely agree that developer quality and management are crucial, with some drawing parallels between working with LLMs and offshore developers. There is skepticism that weaker developers with weaker AI can outperform strong developers with frontier AI. One commenter reports a company replacing Eastern European teams with US programmers plus AI, suggesting increased productivity.

**Tags**: `#AI economics`, `#LLMs`, `#software engineering`, `#outsourcing`, `#developer productivity`

---

<a id="item-6"></a>
## [Curl maintainers overwhelmed by AI-generated security reports](https://simonwillison.net/2026/May/26/the-pressure/#atom-everything) ⭐️ 8.0/10

Daniel Stenberg, the lead maintainer of the curl project, reports that the team is facing an unprecedented deluge of credible AI-assisted security reports, with incoming reports now exceeding one per day—a 4-5x increase over 2024 and double the rate of 2025. This highlights a systemic issue where AI tools are dramatically increasing the volume and quality of security reports, straining maintainers of critical open-source projects and threatening project sustainability. Despite the surge, the vulnerabilities found are mostly LOW or MEDIUM severity; the last HIGH severity CVE was in October 2023. The project has already confirmed 12 vulnerabilities in the current release cycle, a new record, and is on track to publish at least 30 CVEs in 2026 by mid-year.

rss · Simon Willison · May 26, 23:48

**Background**: curl is a widely used open-source command-line tool and library for transferring data with URLs, installed on billions of devices. The project's security team processes vulnerability reports and publishes CVEs (Common Vulnerabilities and Exposures). Recently, AI-assisted security research tools have enabled more thorough and automated vulnerability discovery, leading to a surge in detailed reports.

**Tags**: `#curl`, `#security`, `#open source`, `#AI`, `#vulnerability management`

---

<a id="item-7"></a>
## [EAMS: Equivariant Mesh Networks for Robust Anatomical Segmentation](https://www.reddit.com/r/MachineLearning/comments/1tobtmu/augmented_equivariant_mesh_networks_for/) ⭐️ 8.0/10

The paper presents EAMS (Equivariant Anatomical Mesh Segmentor), a unified framework built on Equivariant Mesh Neural Networks (EMNN) that incorporates intrinsic mesh descriptors and anatomy-aware priors, achieving robust segmentation across four clinical tasks with less than 2 million parameters. EAMS demonstrates that a single lightweight equivariant architecture can handle diverse anatomical segmentation tasks without task-specific customization, while remaining stable under geometric perturbations like pose and mesh resolution changes, which is critical for clinical reliability. The model uses heat kernel signatures (HKS) and area-weighted PCA-derived frames as anatomy-aware priors, and augments message passing with lightweight global context. Experiments show strict equivariance can hurt on subtle asymmetric features (e.g., liver landmarks), motivating future work on soft equivariance.

reddit · r/MachineLearning · /u/m0ronovich · May 26, 16:18

**Background**: Anatomical mesh segmentation involves labeling vertices, edges, or faces on 3D surface meshes from medical scans. Traditional methods are often task-specific and non-equivariant, leading to performance drops under rotations or resolution changes. Equivariant neural networks, such as EMNN, enforce roto-translational symmetry to improve generalization, but may struggle with asymmetric anatomical cues.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2402.04821">[2402.04821] E(3)-Equivariant Mesh Neural Networks</a></li>
<li><a href="https://github.com/HySonLab/EquiMesh">GitHub - HySonLab/EquiMesh: E(3)-Equivariant Mesh Neural Networks (AISTATS 2024)</a></li>
<li><a href="https://arxiv.org/abs/2505.21572">[2505.21572] Thickness-aware E(3)-Equivariant 3D Mesh Neural Networks</a></li>

</ul>
</details>

**Discussion**: The author shared the work as a solo project, expressing excitement about the ICML workshop acceptance and noting the trade-off between equivariance and performance on asymmetric features. They invited feedback and mentioned plans to explore soft equivariance via learned canonicalization and frame averaging.

**Tags**: `#machine learning`, `#mesh segmentation`, `#equivariant neural networks`, `#medical imaging`, `#ICML`

---

<a id="item-8"></a>
## [China Restricts Overseas Travel for AI Talent at Alibaba, DeepSeek](https://www.reddit.com/r/LocalLLaMA/comments/1to5fj5/china_clamps_down_on_overseas_travel_for_ai/) ⭐️ 8.0/10

China has imposed restrictions on overseas travel for AI researchers at Alibaba and DeepSeek, as reported by sources familiar with the matter. This move potentially hampers the exchange of ideas and collaboration with international AI communities. This restriction could significantly slow down AI research and open-source model development in China, affecting the global AI landscape. It may also disrupt talent flow and model releases, impacting companies like DeepSeek that have been actively releasing open-source models. The restrictions specifically target AI talent at Alibaba and DeepSeek, two leading Chinese AI entities. DeepSeek, founded in 2023 by Liang Wenfeng and backed by High-Flyer, has released several open-source models including DeepSeek-LLM and DeepSeek-Coder.

reddit · r/LocalLLaMA · /u/kaggleqrdl · May 26, 12:26

**Background**: DeepSeek is a Chinese AI company based in Hangzhou, known for developing open-source large language models using self-built training frameworks and massive computing resources. The company has gained attention for quickly releasing competitive models. China's tightened control on AI talent movement reflects ongoing geopolitical tensions and concerns about technology transfer.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>
<li><a href="https://www.deepseek.com/">DeepSeek | 深度求索</a></li>

</ul>
</details>

**Discussion**: The Reddit community expressed concern, with one comment stating 'Big, if true. Doesn't bode well for research / OS models out of China.' Overall sentiment suggests anxiety over the potential negative impact on open-source AI development from China.

**Tags**: `#AI`, `#China`, `#Talent`, `#Open Source`, `#Geopolitics`

---

<a id="item-9"></a>
## [Cactus Hybrid Router: 65k model matches frontier AI performance](https://www.reddit.com/r/LocalLLaMA/comments/1tom98y/cactus_hybrid_router_gemma42b_can_match/) ⭐️ 8.0/10

Cactus Compute released the Cactus Hybrid Router, a 65k-parameter model that decides whether to process a task locally using a quantized edge model (e.g., Gemma4-2B) or route it to a cloud frontier model (e.g., Gemini-3.1-Flash-Lite), achieving equivalent performance while routing 15-55% of tasks to the cloud. This innovation significantly reduces inference cost and cloud infrastructure pressure by running simple queries locally, making AI deployment more efficient and scalable for real-time applications like coding assistants and live AI. The router uses only 65k parameters and works with text-only, vision, and audio prompts; it supports an adjustable edge-cloud ratio and maintains robust performance even when the edge model is quantized to 4-bit using Cactus Quants.

reddit · r/LocalLLaMA · /u/Henrie_the_dreamer · May 26, 22:20

**Background**: Hybrid routing uses a small, fast model to evaluate query complexity and decide whether a lightweight local model suffices or a powerful cloud model is needed, balancing latency, cost, and accuracy. Quantization compresses model size with minimal quality loss, enabling efficient on-device inference.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/quotentiroler/CactusRoute">CactusRoute — 7-Layer Adaptive Edge/Cloud Hybrid Router</a></li>
<li><a href="https://betterstack.com/community/guides/ai/cactus-ai/">Cactus: Low-Latency AI Inference for Mobile with Zero-Copy ...</a></li>
<li><a href="https://cactuscompute.com/docs/v1.6">Overview | Cactus</a></li>

</ul>
</details>

**Tags**: `#AI inference`, `#edge computing`, `#model routing`, `#hybrid models`, `#LLM optimization`

---

<a id="item-10"></a>
## [SkillOpt: Treating Markdown Skill Files as Trainable Parameters](https://www.reddit.com/r/LocalLLaMA/comments/1to1mey/skillopt_treats_markdown_skill_files_as_trainable/) ⭐️ 8.0/10

SkillOpt introduces a systematic optimization framework for LLM agent skill files written in Markdown, using bounded edits and validation gating to iteratively improve skill descriptions. This formalizes a previously ad hoc practice in agent building, enabling automatic skill improvement that transfers across models and benchmarks, potentially reducing manual prompt engineering effort. Best skills converge with 1 to 4 accepted edits out of many proposals, an edit budget of 4 to 8 per step works best, and the median final skill is around 920 tokens. A skill optimized on Codex transferred to Claude Code with zero modification, gaining +59.7 on SpreadsheetBench.

reddit · r/LocalLLaMA · /u/agentic-doc · May 26, 09:20

**Background**: LLM agents often rely on Markdown skill files that describe how to perform tasks, but these files are typically handcrafted. SkillOpt treats these skill files as trainable parameters, using an optimizer model to propose bounded edits (add, delete, replace) and a validation set to gate acceptance, akin to gradient descent in text space.

<details><summary>References</summary>
<ul>
<li><a href="https://www.emergentmind.com/topics/skillopt">SkillOpt : Optimizing LLM Agent Skills</a></li>
<li><a href="https://huggingface.co/papers/2605.23904">Paper page - SkillOpt : Executive Strategy for Self-Evolving Agent Skills</a></li>
<li><a href="https://digg.com/ai/gulp2jzs">Microsoft Research releases SkillOpt , an optimization method that...</a></li>

</ul>
</details>

**Tags**: `#LLM agents`, `#skill optimization`, `#markdown`, `#code generation`, `#AI research`

---

<a id="item-11"></a>
## [Iran Plans Permanent Internet Disconnect, Government-Only Access](https://t.me/zaihuapd/41574) ⭐️ 8.0/10

Digital rights activists report that Iran is planning a permanent disconnection from the global internet, allowing only government-approved individuals to access a filtered version. The plan, dubbed a 'government privilege', would replace the current internet with a domestic intranet for most citizens. If implemented, this would represent one of the most extreme forms of internet censorship globally, isolating Iran from the digital world and severely restricting information flow. It could set a precedent for other authoritarian regimes and has significant implications for digital rights, freedom of expression, and geopolitical tensions. The plan reportedly stems from the National Information Network (NIN), a domestic intranet Iran has been developing since 2005 to tighten control. According to Filterwatch, the current internet shutdown that began on January 8, 2026, is a precursor to this permanent system, which would require security clearance for global access.

telegram · zaihuapd · May 26, 06:36

**Background**: Iran has long practiced internet censorship, blocking social media and websites considered harmful. The National Information Network is a state-controlled intranet aimed at replacing the global internet for domestic users. In early 2026, Iran experienced a total internet blackout following protests, leading to a 'Filternet Plus' configuration that replaced the global internet with a domestic intranet. This new plan would make such restrictions permanent and selective.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/filterwatch/filterwatch-has-a-new-home-df8ca19e37f2">Filterwatch Has A New Home! - Medium</a></li>
<li><a href="https://en.wikipedia.org/wiki/National_Information_Network">National Information Network - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Internet_censorship_in_Iran">Internet censorship in Iran - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#internet censorship`, `#Iran`, `#digital rights`, `#network sovereignty`

---

<a id="item-12"></a>
## [China Blocks Founders' Travel in Meta's Manus Acquisition Review](https://t.me/zaihuapd/41577) ⭐️ 8.0/10

Chinese regulators are investigating Meta's acquisition of AI startup Manus for potential investment violations, and have restricted the travel of co-founders Xiao Hong and Ji Yichao while the review is ongoing. This marks a significant escalation in cross-border tech acquisitions scrutiny, and could set a precedent for future AI deals involving Chinese-founded startups and US tech giants. It also highlights the growing tension between US and China over AI talent and technology. Meta announced the acquisition of Manus in December 2024 for an undisclosed amount, though reports suggest around $2 billion. The founders were told not to leave China after meeting with the National Development and Reform Commission this month, but are allowed to travel domestically.

telegram · zaihuapd · May 26, 09:56

**Background**: Manus is a general-purpose AI agent developed by Butterfly Effect, a company founded in China but based in Singapore. It is designed to autonomously execute complex tasks using tools and reasoning. The acquisition by Meta represents a major move to enhance its AI capabilities, but Chinese regulators are now reviewing whether the deal violates investment rules, likely due to concerns about technology transfer and national security.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Manus_(AI_agent)">Manus ( AI agent) - Wikipedia</a></li>
<li><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lCOTdxakVCR2FRVHVzSFJ3dm1pZ0FQAQ?hl=en-NG&gl=NG&ceid=NG:en">Google News - News about Manus • AI • Meta - Overview</a></li>

</ul>
</details>

**Tags**: `#AI regulation`, `#Meta`, `#Manus`, `#China tech`, `#acquisition`

---

<a id="item-13"></a>
## [Alipay Unveils Token Pay and AI Wallet](https://finance.sina.com.cn/jjxw/2026-05-26/doc-inhzffss1524895.shtml) ⭐️ 8.0/10

On May 26, 2026, Alipay launched Token Pay, a payment solution for AI companies, and an AI Wallet for individual users to manage AI agent payments. The services are now available for trial. This marks the first integrated AI-native payment system from a major fintech platform, bridging AI services with global subscription and token-based payments. It could accelerate the monetization of AI applications and set a new standard for AI commerce. Token Pay supports global user subscriptions and in-app token top-ups for large model companies. Already, MiniMax and StepFun have partnered with Alipay to adopt the payment solution for their AI products.

telegram · zaihuapd · May 26, 12:31

**Background**: Alipay had previously launched AI Pay and AI Receive services, and now completes the full-stack AI payment system with Token Pay and AI Wallet. The AI Pay service has already processed 300 million transactions and supports 95% of common AI agent frameworks, making it the first large-scale commercial AI-native payment infrastructure globally. Token Pay is designed to handle the unique needs of AI services, such as token-based billing and recurring subscriptions.

<details><summary>References</summary>
<ul>
<li><a href="https://news.qq.com/rain/a/20260526A06WSA00">支付宝发布全球首个Token Pay服务和AI钱包产品，即日起就可体验</a></li>
<li><a href="https://finance.sina.com.cn/tech/roll/2026-05-26/doc-inhzffsk2851978.shtml">全新发布AI钱包和Token Pay 支付宝全栈AI支付产品矩阵亮相_新浪科技_...</a></li>
<li><a href="https://www.163.com/dy/article/KTSBC55005198UNI.html">支付宝：已完成3亿笔AI支付 全新发布AI钱包及Token Pay</a></li>

</ul>
</details>

**Tags**: `#支付宝`, `#Token Pay`, `#AI钱包`, `#支付`, `#金融科技`

---