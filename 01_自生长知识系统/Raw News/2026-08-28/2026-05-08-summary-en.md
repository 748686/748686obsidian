---
layout: default
title: "Horizon Summary: 2026-05-08 (EN)"
date: 2026-05-08
lang: en
---

> From 47 items, 18 important content pieces were selected

---

1. [Dirtyfrag: Universal Linux LPE Vulnerability Disclosed](#item-1) ⭐️ 9.0/10
2. [Anthropic Releases Natural Language Autoencoders for Model Interpretability](#item-2) ⭐️ 9.0/10
3. [Mozilla Uses Claude Mythos to Harden Firefox](#item-3) ⭐️ 9.0/10
4. [Andrew Morton to Step Down from Linux Memory Management](#item-4) ⭐️ 9.0/10
5. [Open-OSS/privacy-filter malware on Hugging Face with 244k downloads](#item-5) ⭐️ 9.0/10
6. [Triton v3.7.0 Released with New Operations and Backend Enhancements](#item-6) ⭐️ 8.0/10
7. [AI Agents Need Control Flow, Not More Prompts](#item-7) ⭐️ 8.0/10
8. [Cloudflare Lays Off 20% of Workforce in Restructuring](#item-8) ⭐️ 8.0/10
9. [DeepSeek 4 Flash: Local Inference on Apple Metal](#item-9) ⭐️ 8.0/10
10. [AI slop is killing online communities](#item-10) ⭐️ 8.0/10
11. [Chrome removes claim that on-device AI doesn't send data to Google](#item-11) ⭐️ 8.0/10
12. [MiMo V2.5 310B MoE Model Added to llama.cpp](#item-12) ⭐️ 8.0/10
13. [Moonshot AI Hits $10B Valuation, Kimi Revenue Surges](#item-13) ⭐️ 8.0/10
14. [Apple R&D Spending Tops 10% for First Time in 30 Years, Pivots to AI](#item-14) ⭐️ 8.0/10
15. [Tencent Hy3 preview sees 10x adoption over Hy2 in two weeks](#item-15) ⭐️ 8.0/10
16. [Anthropic Partners with SpaceX for GPU Compute, Boosts Claude Limits](#item-16) ⭐️ 8.0/10
17. [Google Cloud Evolves reCAPTCHA into Fraud Defense with QR Verification](#item-17) ⭐️ 8.0/10
18. [Xiaomi Open-Sources OmniVoice: 646-Language Voice Cloning TTS](#item-18) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Dirtyfrag: Universal Linux LPE Vulnerability Disclosed](https://www.openwall.com/lists/oss-security/2026/05/07/8) ⭐️ 9.0/10

A universal Linux local privilege escalation vulnerability named Dirtyfrag has been disclosed via a public GitHub repository, affecting all major distributions. The vulnerability, similar in root cause to the earlier Copy Fail, exploits the net/xfrm and RxRPC subsystems and currently has no patches or CVEs. This vulnerability poses a critical threat to Linux system security, enabling unprivileged users to gain root access on any major distribution. Its disclosure without patches forces administrators to urgently mitigate risk by disabling affected kernel modules or applying workarounds. Dirtyfrag consists of two related issues: one in the xfrm-ESP page-cache write (same sink as Copy Fail) and another in the RxRPC protocol. The researcher, Hyunwoo Kim, noted that while Copy Fail was the motivation, the RxRPC issue is unrelated.

hackernews · flipped · May 7, 19:21 · [Discussion](https://news.ycombinator.com/item?id=48053623)

**Background**: Linux LPE (Local Privilege Escalation) vulnerabilities allow a local user with limited privileges to gain root access. Copy Fail (CVE-2026-31431) was a recent high-severity Linux kernel vulnerability in the crypto subsystem's algif_aead module. Dirtyfrag targets the net/xfrm (IPsec) and RxRPC (AFS filesystem protocol) subsystems, both of which are optional but often enabled by default in distributions.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/V4bel/dirtyfrag">GitHub - V4bel/ dirtyfrag · GitHub</a></li>
<li><a href="https://stacker.news/items/1486126">dirtyfrag : Universal Linux LPE - V4bel \ stacker news</a></li>
<li><a href="https://news.lavx.hu/article/dirty-frag-linux-vulnerability-enables-root-access-across-major-distributions-no-patches-available">Dirty Frag Linux Vulnerability Enables Root Access... | LavX News</a></li>

</ul>
</details>

**Discussion**: The community comments highlight the similarity to Copy Fail and express frustration with kernel maintainers for enabling seldom-used functionality by default. A commenter notes that algif_aead received flak for Copy Fail, but the real issue was the authencesn module, which remains unfixed.

**Tags**: `#linux`, `#kernel`, `#security`, `#vulnerability`, `#lpe`

---

<a id="item-2"></a>
## [Anthropic Releases Natural Language Autoencoders for Model Interpretability](https://www.anthropic.com/research/natural-language-autoencoders) ⭐️ 9.0/10

Anthropic has open-sourced Natural Language Autoencoders (NLAs) that translate internal model activations into human-readable text, releasing weights for Qwen 2.5 (7B), Gemma 3 (12B, 27B), and Llama 3.3 (70B). This breakthrough in interpretability allows researchers to directly read what a language model is 'thinking' during inference, enabling safer and more transparent AI systems. By releasing open-weight models, Anthropic empowers the broader community to probe proprietary and open models alike. The NLA method uses an activation verbalizer to generate text describing a specific layer's activation, then reconstructs the activation to verify fidelity. The released models are built on top of existing architectures and are available on Hugging Face.

hackernews · instagraham · May 7, 17:54 · [Discussion](https://news.ycombinator.com/item?id=48052537)

**Background**: Autoencoders are neural networks that learn efficient data representations by compressing input and reconstructing it. In large language models (LLMs), 'activations' are numerical vectors representing internal states. NLAs extend autoencoders to produce natural language descriptions, making model internals interpretable.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/research/natural-language-autoencoders">Natural Language Autoencoders: Turning Claude’s thoughts into text</a></li>

</ul>
</details>

**Discussion**: Community members praised the open-weight release and engagement with Hugging Face, calling it 'huge news'. Some noted the approach's reliance on specific layers and questioned how clean training data can be obtained given circulating discussions. Experts recommended reading the detailed explainer on Transformer Circuits.

**Tags**: `#interpretability`, `#LLMs`, `#autoencoders`, `#Anthropic`, `#open-source`

---

<a id="item-3"></a>
## [Mozilla Uses Claude Mythos to Harden Firefox](https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything) ⭐️ 9.0/10

Mozilla used the Claude Mythos Preview AI model to find and fix hundreds of security vulnerabilities in Firefox, with the number of monthly fixes jumping from ~20-30 to 423 in April 2026. This breakthrough demonstrates that AI-assisted vulnerability detection has become highly effective, shifting from low-quality reports to high-signal bug discovery that can dramatically accelerate software security hardening. Mozilla ran Claude Code with Mythos Preview in an isolated container, prompting it to proactively find vulnerabilities; this approach uncovered a 20-year-old XSLT bug and a 15-year-old legend element bug. Many attempts were blocked by Firefox's existing defense-in-depth measures.

rss · Simon Willison · May 7, 17:56

**Background**: Claude Mythos Preview is Anthropic's most powerful large language model, released in private preview in 2026 to select companies. Prior to this, AI-generated security bug reports were often considered low-quality noise that imposed costs on maintainers. Mozilla combined improved model capabilities with better prompting and filtering techniques to harness AI effectively.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Mythos_Preview">Claude Mythos Preview</a></li>
<li><a href="https://red.anthropic.com/2026/mythos-preview/">Claude Mythos Preview \ red.anthropic.com</a></li>

</ul>
</details>

**Tags**: `#AI`, `#security`, `#Firefox`, `#vulnerability detection`, `#Mozilla`

---

<a id="item-4"></a>
## [Andrew Morton to Step Down from Linux Memory Management](https://lwn.net/Articles/1070994/) ⭐️ 9.0/10

On April 21, 2026, Andrew Morton announced his intention to step down as maintainer of the Linux kernel's memory-management subsystem, a role he has held for decades. The future of maintainership was discussed at the 2026 LSFMM+BPF Summit, with David Hildenbrand set to take over the integration tree. This transition marks a generational shift in leadership for one of the kernel's most critical subsystems, impacting the entire Linux ecosystem. The community must reorganize to ensure continued high-quality maintenance and review. Morton noted that the memory-management code is heavily interlinked, making it difficult to split the subsystem into separate parts. David Hildenbrand will handle the catch-all integration tree, but many details about future maintainership remain unresolved.

rss · LWN.net · May 7, 14:42

**Background**: The memory-management subsystem handles virtual memory, page allocation, and other core functions in the Linux kernel. Andrew Morton has been its maintainer since before it became a separate subsystem, and the LSFMM+BPF Summit is an annual conference where kernel developers discuss storage, filesystem, memory management, and BPF topics.

<details><summary>References</summary>
<ul>
<li><a href="https://lwn.net/Articles/lsfmmbpf2023/">The 2023 LSFMM+BPF Summit [LWN.net]</a></li>

</ul>
</details>

**Tags**: `#linux kernel`, `#memory management`, `#maintainership`, `#open source`, `#community`

---

<a id="item-5"></a>
## [Open-OSS/privacy-filter malware on Hugging Face with 244k downloads](https://www.reddit.com/r/LocalLLaMA/comments/1t6febk/warning_openossprivacyfilter_malware/) ⭐️ 9.0/10

A fake AI model named Open-OSS/privacy-filter on Hugging Face has been identified as infostealer malware, using a Python-based dropper to execute malicious PowerShell commands and download a Windows executable. Over 244k downloads have been recorded, and the repository has been reported to Hugging Face and Microsoft. This incident highlights the growing threat of malware disguised as AI models on popular platforms like Hugging Face, potentially compromising many users' sensitive data. It underscores the need for better security vetting in open-source AI repositories. The malware targets Windows systems; Linux users are unaffected. The malicious payload includes a Rust-compiled program that steals data from Chrome, WinSCP, and other applications, and is persisted via Task Scheduler. The attack chain involves multiple layers of base64-encoded commands.

reddit · r/LocalLLaMA · charles25565 · May 7, 16:20

**Background**: Infostealer malware is a type of malicious software designed to steal sensitive data from victims' devices. Python droppers are often used as initial payloads to download and execute further malware. Tria.ge is an online sandbox used for behavioral analysis of suspicious files, and the provided link shows the malware's behavior.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/infostealer-malware">Infostealer malware</a></li>
<li><a href="https://github.com/topics/dropper?l=python">dropper · GitHub Topics · GitHub</a></li>
<li><a href="https://sandbox.recordedfuture.com/docs/">Home - Triage</a></li>

</ul>
</details>

**Discussion**: The community expressed shock at the 244k downloads and noted the obvious red flags, such as the organization name 'Open open source software'. One user provided technical details of the attack chain, while another pointed out that the accounts that liked the model may indicate multiple malware campaigns. Sarcasm about Linux immunity and a humorous comment about GGUF were also present.

**Tags**: `#security`, `#malware`, `#huggingface`, `#AI safety`

---

<a id="item-6"></a>
## [Triton v3.7.0 Released with New Operations and Backend Enhancements](https://github.com/triton-lang/triton/releases/tag/v3.7.0) ⭐️ 8.0/10

Triton v3.7.0 introduces tl.squeeze/tl.unsqueeze operations, scaled batched matmul, FP8 constant support, and several backend improvements including 2CTA mode and TMA multicast. The release also includes LLVM updates, bug fixes, and performance optimizations for the JIT compiler. This release enhances Triton's expressiveness and performance for GPU kernel development, directly benefiting AI/ML practitioners who rely on Triton for high-performance deep learning workloads. Scaled batched matmul and FP8 constants are particularly relevant for modern LLM inference and training. The scaled batched matmul feature supports efficiently multiplying multiple matrices with scaling, while FP8 constants allow direct creation of 8-bit floating-point constants in Triton kernels. Backend improvements include 2CTA (multi-CTA) mode for better GPU utilization and TMA (Tensor Memory Accelerator) multicast support.

github · atalman · May 7, 22:19

<details><summary>References</summary>
<ul>
<li><a href="https://docs.pytorch.org/docs/stable/generated/torch.matmul.html">torch.matmul — PyTorch 2.11 documentation</a></li>
<li><a href="https://github.com/parca-dev/proton">GitHub - parca-dev/ proton</a></li>

</ul>
</details>

**Tags**: `#triton`, `#gpu`, `#compiler`, `#deep learning`, `#release`

---

<a id="item-7"></a>
## [AI Agents Need Control Flow, Not More Prompts](https://bsuh.bearblog.dev/agents-need-control-flow/) ⭐️ 8.0/10

The article argues that building reliable AI agents requires explicit control flow constructs like loops and conditionals, rather than solely relying on improving prompts. This challenges the predominant prompt-engineering approach in AI agent development. This insight is significant because current AI agent development heavily emphasizes prompt engineering, which often leads to unreliable behavior in complex real-world tasks. Shifting focus to control flow could lead to more robust and deterministic agents, improving their practical utility. The article highlights that without explicit control flow, agents struggle with tasks requiring iteration or conditional logic, such as processing multiple files in a session. The community discussion suggests that LLMs may be better used for writing deterministic code rather than handling tasks at runtime.

hackernews · bsuh · May 7, 16:43 · [Discussion](https://news.ycombinator.com/item?id=48051562)

**Background**: AI agents are software systems that leverage large language models (LLMs) to autonomously perform tasks. Control flow refers to the order in which individual statements, instructions, or function calls are executed or evaluated, including constructs like loops and conditionals. Prompt engineering involves crafting input prompts to guide LLM behavior, but this approach has limitations in handling multi-step, stateful tasks.

**Discussion**: The community strongly agrees with the article's thesis. One commenter criticizes the advice to 'build for future models' and provides a concrete example of a QA agent failing due to lack of control flow. Others suggest that LLMs should be used to write deterministic code instead of handling tasks at runtime, and some humorously note that this is essentially reinventing programming.

**Tags**: `#AI agents`, `#control flow`, `#prompt engineering`, `#LLM`, `#software design`

---

<a id="item-8"></a>
## [Cloudflare Lays Off 20% of Workforce in Restructuring](https://blog.cloudflare.com/building-for-the-future/) ⭐️ 8.0/10

Cloudflare announced a layoff of approximately 1,100 employees, representing 20% of its workforce, as part of a strategic restructuring aimed at 'building for the future.' This significant reduction at a major tech company highlights the tension between long-term AI investments and short-term cost pressures, affecting over a thousand employees and sparking debate about corporate messaging. Departing employees will receive full base pay through end of 2026, U.S. healthcare coverage through year-end, and equity vesting through August 15th, with cliffs waived.

hackernews · PriorityLeft · May 7, 20:23 · [Discussion](https://news.ycombinator.com/item?id=48054423)

**Background**: Cloudflare is a major content delivery network and cloud security company. The layoff comes after a period of rapid hiring, including a large intern program in September 2025. The company and others in tech have increased spending on AI technologies, which has not yet translated into equivalent revenue gains, leading to cost-cutting measures.

**Discussion**: Community comments criticized the euphemistic title, with one user noting the contradiction between hiring 1,111 interns in 2025 and now laying off 1,100. Another affected employee posted looking for a new job. Some speculated the layoffs are due to high AI costs without offsetting revenue.

**Tags**: `#cloudflare`, `#layoffs`, `#tech-industry`, `#corporate-strategy`, `#ai-economics`

---

<a id="item-9"></a>
## [DeepSeek 4 Flash: Local Inference on Apple Metal](https://github.com/antirez/ds4) ⭐️ 8.0/10

Antirez released DeepSeek 4 Flash (DS4), a local inference engine optimized for DeepSeek models using Apple's Metal API, enabling efficient on-device LLM inference on Mac hardware. This project addresses the practical need for optimized local inference on Apple hardware, potentially narrowing the gap between frontier and open-source models through focused optimization on a single model architecture. DS4 handles large initial prompts (e.g., 25k tokens) with significant prefill time (~4 minutes) but uses disk-based KV caching to speed up subsequent interactions, and peaks at 50W power usage on an M3 Max MacBook Pro.

hackernews · tamnd · May 7, 15:40 · [Discussion](https://news.ycombinator.com/item?id=48050751)

**Background**: DeepSeek is a Chinese AI company developing large language models. Apple's Metal API provides low-level GPU access for graphics and compute on Apple hardware, enabling efficient inference. Local inference engines like llama.cpp and ollama allow running LLMs on personal devices, but few are specifically optimized for Apple's Metal backend and DeepSeek models.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Metal_(API)">Metal (API) - Wikipedia</a></li>
<li><a href="https://www.skool.com/open-source-ai-builders-club/best-local-llm-inference-engines-in-2025-from-everyday-laptops-to-enterprise">Best Local LLM Inference Engines in 2025: From Everyday Laptops to ...</a></li>

</ul>
</details>

**Discussion**: The community praised DS4 for its focused optimization and educational value, with commenters noting the potential for iterative improvement. Some expressed concern about the long prefill time for large inputs, while the author clarified that caching makes it practical for regular use. Energy efficiency was highlighted as a positive aspect.

**Tags**: `#deepseek`, `#local-inference`, `#metal`, `#apple`, `#llm`

---

<a id="item-10"></a>
## [AI slop is killing online communities](https://rmoff.net/2026/05/06/ai-slop-is-killing-online-communities/) ⭐️ 8.0/10

A new blog post argues that AI-generated content is flooding online communities, degrading authentic human interactions and overwhelming moderators. Community managers report banning hundreds of bot accounts monthly and fear losing the battle against inauthentic content. This trend threatens the very foundation of online communities—trust and authenticity—potentially driving users away from platforms. The widespread adoption of AI raises critical questions about how to preserve genuine human connection in digital spaces. Specific examples include a user who had an LLM agent karma-farm on Reddit without detection, and a niche community that bans 600 AI content accounts monthly. Moderation costs have increased significantly, with smaller communities bearing an unfair burden.

hackernews · thm · May 7, 18:46 · [Discussion](https://news.ycombinator.com/item?id=48053203)

**Background**: AI slop refers to low-quality, often irrelevant or misleading content generated by large language models (LLMs) and other AI tools, designed to mimic human posts. Online communities rely on authentic interactions, but bots and automated content erode trust, requiring manual moderation. As AI generation becomes cheaper and more accessible, the volume of such content has exploded, threatening community sustainability.

**Discussion**: Community commenters share firsthand experiences: one user successfully karmafarmed on Reddit using an AI agent, while a community organizer bans 600 AI accounts monthly and fears losing the battle. Others suggest that smaller, more insular communities may be the solution, and some even argue that AI pollution might push humans back to real-world interactions.

**Tags**: `#AI`, `#online communities`, `#content moderation`, `#bots`, `#authenticity`

---

<a id="item-11"></a>
## [Chrome removes claim that on-device AI doesn't send data to Google](https://old.reddit.com/r/chrome/comments/1t5qayz/chrome_removes_claim_of_ondevice_al_not_sending/) ⭐️ 8.0/10

Google Chrome has removed a statement from its on-device AI features page that previously claimed the AI does not send data to Google servers, raising privacy concerns. This change undermines user trust in Google's privacy promises and suggests that on-device AI may not be as private as advertised, potentially affecting millions of Chrome users who rely on its integrated AI features. The removal was noticed on the Chrome AI innovations page, and community members suspect it may indicate data transmission. Google's enterprise policy states data may be sent to Google for AI features to work, but not used to improve models or for ads.

hackernews · newsoftheday · May 7, 15:56 · [Discussion](https://news.ycombinator.com/item?id=48050964)

**Background**: On-device AI refers to AI models that run locally on a user's device, theoretically processing data without sending it to external servers. Chrome has been introducing such features, including a 4GB AI model that downloads silently, which has already sparked privacy and consent debates.

<details><summary>References</summary>
<ul>
<li><a href="https://www.google.com/chrome/ai-innovations/">AI in Chrome: help right where you need it</a></li>
<li><a href="https://support.google.com/chrome/answer/16961953?hl=en">Manage on-device Generative AI models in Chrome - Google Chrome Help</a></li>
<li><a href="https://www.tomsguide.com/ai/check-your-storage-chrome-may-be-downloading-a-4gb-ai-model-heres-what-we-know">'No clear consent flow for this download': Google Chrome is silently stashing a 4GB AI model on your device — and Google just responded | Tom's Guide</a></li>

</ul>
</details>

**Discussion**: The Reddit and Hacker News communities express strong skepticism, with many believing the AI features are primarily for data collection. Some commenters suggest the wording change might be for brevity, but most view it as confirmation of data being sent to Google, potentially violating GDPR.

**Tags**: `#privacy`, `#Chrome`, `#AI`, `#Google`, `#data collection`

---

<a id="item-12"></a>
## [MiMo V2.5 310B MoE Model Added to llama.cpp](https://github.com/ggml-org/llama.cpp/pull/22493) ⭐️ 8.0/10

A pull request (#22493) by AesSedai adds support for Xiaomi's MiMo V2.5 model to llama.cpp, a 310B total / 15B activated sparse Mixture-of-Experts (MoE) model with 1M token context and multimodal capabilities (text, image, video, audio). This enables local inference of a state-of-the-art multimodal MoE model on consumer-grade hardware with 128GB RAM (e.g., DGX Spark), making powerful AI accessible to developers and researchers. The addition of Multi-Token Prediction (MTP) support is also anticipated, further improving generation efficiency. The model uses a 729M-parameter ViT vision encoder and a 261M-parameter Audio Transformer as modality adapters, plus a 3-layer MTP head with 329M parameters. While the initial merge supports text and image modalities, audio and video support are not yet included in this pull request.

reddit · r/LocalLLaMA · jacek2023 · May 7, 11:23 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1t67lvx/feat_add_mimo_v25_model_support_by_aessedai_pull/)

**Background**: Sparse Mixture of Experts (MoE) is a model architecture that activates only a subset of expert sub-networks for each input token, allowing larger total parameter counts with lower computational cost per token. Multi-Token Prediction (MTP) is a training technique where the model predicts multiple future tokens simultaneously, improving sample efficiency and generation speed. llama.cpp is a popular open-source project that enables efficient inference of large language models on CPU and GPU. MiMo V2.5, developed by Xiaomi, is a 310B sparse MoE model optimized for multimodal understanding and long context.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Sparse_mixture-of-experts">Sparse mixture-of-experts</a></li>
<li><a href="https://arxiv.org/abs/2505.10518">[2505.10518] Multi-Token Prediction Needs Registers</a></li>

</ul>
</details>

**Discussion**: Community members expressed excitement about running MiMo V2.5 on 128GB systems, with one tester reporting 60 tokens/sec on a dual-GPU setup. Some users noted that audio/video support is missing and that the initial GGUF quantization may not be optimal, advising to wait for future versions. One user reported that the model loops constantly even on the official web UI, calling it a 'broken model.'

**Tags**: `#llama.cpp`, `#MiMo`, `#MoE`, `#multimodal`, `#open-source`

---

<a id="item-13"></a>
## [Moonshot AI Hits $10B Valuation, Kimi Revenue Surges](https://t.me/zaihuapd/41251) ⭐️ 8.0/10

Moonshot AI completed a new funding round of over $700 million, pushing its valuation above $10 billion and making it a decacorn in just over two years. Additionally, its Kimi product generated more revenue in the last 20 days than it did in all of 2025, with overseas revenue now exceeding domestic revenue. This milestone highlights the rapid scaling of Chinese AI startups and strong investor confidence, especially from major tech firms like Alibaba and Tencent. The exceptional revenue growth of Kimi signals a significant shift in AI adoption, with global demand driving higher usage and monetization. The funding round was co-led by Alibaba, Tencent, Wuyuan, Jiuan, and other investors, bringing Moonshot AI's total funding to over $1.2 billion. The Kimi product's revenue surge is attributed to growth in global paid users and API calls, with overseas markets now outperforming domestic ones.

telegram · zaihuapd · May 7, 00:30

**Background**: Moonshot AI is a Chinese startup specializing in large language models (LLMs), known for its Kimi product family. The company recently released Kimi K2.5, an open-source multimodal model that can handle text, code, and visual content. A "decacorn" refers to a private startup valued at $10 billion or more, a rare achievement in the startup world. The news also mentions OpenRouter, a unified API platform that allows developers to access various AI models through a single interface.

<details><summary>References</summary>
<ul>
<li><a href="https://www.dugainadvisors.com/post/decacorn-hectocorn-valuations-what-s-next">Decacorn & Hectocorn Valuations: What's Next?</a></li>
<li><a href="https://www.kimi.com/ai-models/kimi-k2-5">Kimi K2.5 | Open Visual Agentic Model for Real Work</a></li>
<li><a href="https://www.codecademy.com/article/what-is-openrouter">What is OpenRouter? A Guide with Practical Examples - Codecademy</a></li>

</ul>
</details>

**Tags**: `#AI`, `#startup`, `#funding`, `#LLM`, `#valuation`

---

<a id="item-14"></a>
## [Apple R&D Spending Tops 10% for First Time in 30 Years, Pivots to AI](https://www.cnbc.com/2026/05/06/apples-rd-spending-climbs-to-10percent-of-revenue-on-ai-investments.html) ⭐️ 8.0/10

Apple's R&D spending reached 10.3% of revenue in the March 2026 quarter, the first time above 10% in three decades, with a 34% year-over-year increase in R&D investment. This marks a strategic pivot toward integrating AI across its hardware platform, including on-device LLMs, private cloud computing, and custom AI chips. This financial milestone signals Apple's determination to compete in the AI race, potentially reshaping its product ecosystem as it did during the iPod era. The move could accelerate the integration of generative AI into everyday devices like iPhones, AirPods, and AR glasses, affecting millions of users and the broader consumer tech landscape. The R&D surge comes as CEO Tim Cook prepares to step down in September 2026, with Apple focusing on on-device AI with a ~3 billion parameter model, a larger server-based model via Private Cloud Compute, and custom chips like the M5 series. Apple is also reportedly developing AI glasses and AirPods with cameras.

telegram · zaihuapd · May 7, 01:00

**Background**: Apple has historically kept R&D spending around 6-8% of revenue, but the rise to over 10% reflects a major strategic shift. The company is investing in on-device AI to differentiate on privacy, using Private Cloud Compute to securely handle complex workloads. Custom silicon like the M-series chips enables tight integration of AI capabilities across devices, a strategy that previously fueled the iPhone's success.

<details><summary>References</summary>
<ul>
<li><a href="https://machinelearning.apple.com/research/introducing-apple-foundation-models">Introducing Apple’s On-Device and Server Foundation Models -</a></li>
<li><a href="https://security.apple.com/blog/private-cloud-compute/">Private Cloud Compute: A new frontier for AI privacy in the cloud - Apple Security Research</a></li>
<li><a href="https://www.fastcompany.com/91047728/apple-ai-applegpt-generative-siri-m3-macbook-air-cloud-device">Apple hinted at big AI plans. Here's what AppleGPT might entail</a></li>

</ul>
</details>

**Tags**: `#Apple`, `#AI`, `#R&D`, `#Hardware`, `#Strategy`

---

<a id="item-15"></a>
## [Tencent Hy3 preview sees 10x adoption over Hy2 in two weeks](https://finance.sina.com.cn/tech/shenji/2026-05-07/doc-inhwzrtp8521239.shtml) ⭐️ 8.0/10

Tencent's Hy3 preview model achieved token usage 10 times that of its predecessor Hy2 within two weeks of launch, and ranked first on OpenRouter's weekly leaderboard in both overall usage and market share. This rapid adoption signals strong market validation for Tencent's latest model and intensifies competition in the AI model landscape, especially in agent and tool-calling scenarios where Hy3 preview excelled. Hy3 preview is a 295-billion parameter Mixture-of-Experts (MoE) model with 21 billion active parameters, supporting a 256K token context window and integrating both fast and slow thinking capabilities.

telegram · zaihuapd · May 7, 05:34

**Background**: Hy3 preview is the first model trained on Tencent's rebuilt AI infrastructure, using a Mixture-of-Experts architecture that activates only a subset of parameters per token to balance performance and efficiency. OpenRouter is a platform providing access to over 300 AI models through a single API, often used for benchmarking model adoption. The model also showed significant growth in coding and agent-related applications, with a 16.5x increase in usage across Tencent's own tools like WorkBuddy and Codebuddy.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/tencent/Hy3-preview">tencent/Hy3-preview · Hugging Face</a></li>
<li><a href="https://www.tencent.com/en-us/articles/2202320.html">Tencent Unveils Hy3 preview; Model Enhances Agent Capabilities and Real-World Usability - Tencent 腾讯</a></li>
<li><a href="https://github.com/Tencent-Hunyuan/Hy3-preview">GitHub - Tencent-Hunyuan/Hy3-preview: Hy3 preview (295B A21B), a leading reasoning and agent model in its size, with great cost efficiency · GitHub</a></li>

</ul>
</details>

**Tags**: `#AI`, `#LLM`, `#Tencent`, `#Model Performance`, `#Industry News`

---

<a id="item-16"></a>
## [Anthropic Partners with SpaceX for GPU Compute, Boosts Claude Limits](https://t.me/zaihuapd/41259) ⭐️ 8.0/10

Anthropic has partnered with SpaceX to use the entire compute capacity of xAI's Colossus 1 data center, gaining access to over 220,000 Nvidia GPUs and more than 300 megawatts of power within a month. As a result, Claude Code rate limits have doubled and peak-hour restrictions for Pro/Max users have been removed, while Claude Opus API rate limits have also been significantly increased. This partnership massively expands Anthropic's computational resources, enabling faster model training and higher API throughput for Claude customers. It signals a deepening collaboration between AI companies and large-scale infrastructure providers, potentially accelerating the development of advanced AI models. Colossus 1, built in a record 122 days in Memphis, Tennessee, is one of the largest AI data centers, originally used to train xAI's Grok model. Anthropic will utilize the entire facility, including over 220,000 Nvidia GPUs and 300 MW of capacity.

telegram · zaihuapd · May 7, 08:19

**Background**: Anthropic develops the Claude family of large language models, used for tasks like software development via Claude Code. To train and serve these models at scale, massive computational clusters with thousands of GPUs are required. The Colossus data center, operated by xAI under SpaceX ownership, provides such infrastructure.

<details><summary>References</summary>
<ul>
<li><a href="https://www.datacenterdynamics.com/en/news/anthropic-to-use-all-of-spacex-xais-colossus-1-data-center-compute/">Anthropic to use all of SpaceX-xAI's Colossus 1 data center compute</a></li>
<li><a href="https://claude.com/product/claude-code">Claude Code by Anthropic | AI Coding Agent, Terminal, IDE</a></li>

</ul>
</details>

**Tags**: `#算力合作`, `#AI基础设施`, `#NVIDIA GPU`, `#Claude`

---

<a id="item-17"></a>
## [Google Cloud Evolves reCAPTCHA into Fraud Defense with QR Verification](https://support.google.com/recaptcha/answer/16609652?hl=en) ⭐️ 8.0/10

Google Cloud launched Fraud Defense as the next evolution of reCAPTCHA, introducing a QR code-based mobile verification challenge to counter AI-powered bots. This marks a significant shift from traditional CAPTCHA to a fraud prevention platform, essential for securing the agentic web against sophisticated automated attacks. The QR verification requires users to scan a code with their phone to prove human presence. Compatibility requires Android Google Play Services 25.41.30+ or iOS 15.0+.

telegram · zaihuapd · May 7, 09:18

**Background**: reCAPTCHA has been a widely used service by Google to distinguish human users from bots. With the rise of AI agents, traditional challenges are becoming less effective. Fraud Defense extends reCAPTCHA's capabilities to include fraud and abuse prevention across the agentic web, integrating with Cloud Armor and Apigee for multi-layered protection.

<details><summary>References</summary>
<ul>
<li><a href="https://cloud.google.com/blog/products/identity-security/introducing-google-cloud-fraud-defense-the-next-evolution-of-recaptcha/">Introducing Google Cloud Fraud Defense, the next evolution of reCAPTCHA | Google Cloud Blog</a></li>
<li><a href="https://docs.cloud.google.com/recaptcha/docs">Google Cloud Fraud Defense documentation | Google Cloud Documentation</a></li>
<li><a href="https://cloud.google.com/security/products/fraud-defense">Fraud Defense | Google Cloud</a></li>

</ul>
</details>

**Tags**: `#security`, `#captcha`, `#fraud prevention`, `#google cloud`, `#QR code`

---

<a id="item-18"></a>
## [Xiaomi Open-Sources OmniVoice: 646-Language Voice Cloning TTS](https://mp.weixin.qq.com/s/TCS_Sd10g_rvf1cszw673A) ⭐️ 8.0/10

Xiaomi has open-sourced OmniVoice, a massively multilingual zero-shot TTS model supporting over 600 languages, with a minimal bidirectional Transformer architecture that achieves a training speed of 100,000 hours per day and PyTorch inference at 40x real-time. This release democratizes high-quality multilingual voice cloning, surpassing commercial systems in 24-language tests and approaching natural speech in 102 languages, enabling cross-lingual customization and noisy environment adaptation for developers worldwide. OmniVoice is trained on 580,000 hours of speech data across 646 languages from 50 open-source datasets, using full-codebook random masking and LLM pre-trained parameters to enhance efficiency and intelligibility.

telegram · zaihuapd · May 7, 10:06

**Background**: Text-to-speech (TTS) converts written text into spoken audio, and voice cloning aims to replicate a target speaker's voice characteristics. OmniVoice uses a bidirectional Transformer architecture (similar to BERT) with a codebook for discrete audio representations, and leverages pre-trained LLM parameters to bootstrap training. Full-codebook random masking is a training technique where all codebook entries are randomly masked during training to improve robustness.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/k2-fsa/OmniVoice">GitHub - k2-fsa/OmniVoice: High-Quality Voice Cloning TTS for 600+ Languages · GitHub</a></li>
<li><a href="https://huggingface.co/k2-fsa/OmniVoice">k2-fsa/OmniVoice · Hugging Face</a></li>

</ul>
</details>

**Tags**: `#TTS`, `#voice cloning`, `#open-source`, `#multilingual`, `#Xiaomi`

---