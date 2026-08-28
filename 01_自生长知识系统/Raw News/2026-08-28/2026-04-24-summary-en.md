---
layout: default
title: "Horizon Summary: 2026-04-24 (EN)"
date: 2026-04-24
lang: en
---

> From 40 items, 26 important content pieces were selected

---

1. [OpenAI Releases GPT-5.5, a Frontier Coding Model](#item-1) ⭐️ 9.0/10
2. [Bitwarden CLI compromised in Checkmarx supply chain attack](#item-2) ⭐️ 9.0/10
3. [Apple CEO Tim Cook to Step Down in 2026, John Ternus to Succeed](#item-3) ⭐️ 9.0/10
4. [vLLM v0.20.0: CUDA 13, PyTorch 2.11, FlashAttention 4, TurboQuant](#item-4) ⭐️ 8.0/10
5. [Anthropic details Claude forgetfulness bug fix](#item-5) ⭐️ 8.0/10
6. [Tailscale Co-founder Critiques Cloud Complexity](#item-6) ⭐️ 8.0/10
7. [Ubuntu 26.04 LTS 'Resolute Raccoon' Released](#item-7) ⭐️ 8.0/10
8. [Qwen 3.6 27B Ties Sonnet 4.6 on Agentic Index](#item-8) ⭐️ 8.0/10
9. [US Memo on Adversarial Distillation Raises Open Model Concerns](#item-9) ⭐️ 8.0/10
10. [85 TPS, 125K Context, Vision for Qwen3.6-27B on Single RTX 3090](#item-10) ⭐️ 8.0/10
11. [Tencent Releases Hy3 Preview: 295B MoE with 21B Active](#item-11) ⭐️ 8.0/10
12. [DeepSeek Open-Sources DeepEP V2 and TileKernels](#item-12) ⭐️ 8.0/10
13. [Hairdryer used to rig Paris weather sensor, netting $34K on Polymarket](#item-13) ⭐️ 8.0/10
14. [Google Cloud Default Security Flaw Causes Massive Bills](#item-14) ⭐️ 8.0/10
15. [ByteDance Releases Seed3D 2.0, 3D Generation Goes Production-Ready](#item-15) ⭐️ 8.0/10
16. [SFC and PwC Reach HK$1 Billion Settlement for Evergrande Fraud](#item-16) ⭐️ 8.0/10
17. [China's Three Major Telecoms Suffer International Network Outage](#item-17) ⭐️ 8.0/10
18. [UK NCSC Officially Endorses Passkeys as Primary Authentication](#item-18) ⭐️ 8.0/10
19. [EU Pressures Google to Open Android to Rival AI Assistants](#item-19) ⭐️ 8.0/10
20. [MIT Researchers Build Math Bridge Between Classical and Quantum Physics](#item-20) ⭐️ 8.0/10
21. [LiteParse for the Web: Browser-Based PDF Text Extraction](#item-21) ⭐️ 7.0/10
22. [Famfs Filesystem Faces Potential BPF Redesign](#item-22) ⭐️ 7.0/10
23. [PI Coding Agent with Qwen3.6 35b Impresses Users](#item-23) ⭐️ 7.0/10
24. [Indian student uses AI to create fake influencer targeting US conservatives](#item-24) ⭐️ 7.0/10
25. [OpenAI's macOS Chronicle Feature Sparks Privacy and Security Concerns](#item-25) ⭐️ 7.0/10
26. [TSMC Delays High-NA EUV Adoption Until 2029 Due to Cost](#item-26) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [OpenAI Releases GPT-5.5, a Frontier Coding Model](https://openai.com/index/introducing-gpt-5-5/) ⭐️ 9.0/10

OpenAI has released GPT-5.5, a new frontier coding model, with a gradual rollout starting with Pro and Enterprise accounts. The model scores 82% on the CyberGym benchmark, positioning it as a strong competitor in AI-assisted coding. GPT-5.5 represents a major leap in AI-assisted software engineering, potentially transforming developer productivity and workflow. The release also reignites debate about developer dependency on AI tools, as highlighted by community comments comparing losing access to losing a limb. The rollout is gradual over many hours to ensure service stability, starting with Pro/Enterprise accounts before reaching Plus users. API access is not yet available, but a backdoor via Codex API reportedly provides access to GPT-5.5.

hackernews · rd · Apr 23, 18:01

**Background**: Frontier coding models are AI systems specialized in generating and understanding code, often used by developers to automate tasks and boost productivity. OpenAI's GPT series has evolved from general-purpose language models to domain-specific tools, with GPT-5.5 focusing on coding performance. The CyberGym benchmark evaluates AI models on cybersecurity and coding challenges.

**Discussion**: Community sentiment is mixed: some users express unease about growing dependency on AI coding tools, comparing it to an addiction. Others praise the model's performance and OpenAI's more open approach compared to Anthropic's gated Mythos model. A few users note the gradual rollout and backdoor API access as notable details.

**Tags**: `#AI`, `#GPT`, `#OpenAI`, `#coding`, `#machine learning`

---

<a id="item-2"></a>
## [Bitwarden CLI compromised in Checkmarx supply chain attack](https://socket.dev/blog/bitwarden-cli-compromised) ⭐️ 9.0/10

Bitwarden CLI was compromised in a supply chain attack via a poisoned npm package, with a malicious version 2026.4.0 published to npm that exfiltrated credentials and secrets from affected users. This attack affects a widely-used password manager CLI, potentially exposing sensitive credentials of developers and organizations, and highlights the ongoing risks in the npm ecosystem. The malicious package was published approximately 19 hours before detection, and only 334 users downloaded it. Setting min-release-age=7 in .npmrc (npm 11.10+) would have blocked it.

hackernews · tosh · Apr 23, 14:17

**Background**: Supply chain attacks target the software development pipeline by compromising trusted dependencies. In this case, the attacker poisoned the Bitwarden CLI npm package, which is used by developers to manage passwords from the command line. The Checkmarx campaign is a broader series of npm supply chain attacks.

<details><summary>References</summary>
<ul>
<li><a href="https://checkmarx.com/zero-post/npm-hit-by-shai-hulud-the-self-replicating-supply-chain-attack/">NPM Hit By Shai-Hulud, The Self-Replicating Supply Chain Attack</a></li>

</ul>
</details>

**Discussion**: Community comments suggest using min-release-age to mitigate such attacks, pinning dependencies, and considering Rust alternatives like rbw. Some users expressed concerns about the CLI exposing all data in plaintext.

**Tags**: `#supply chain security`, `#npm`, `#Bitwarden`, `#supply chain attack`, `#security`

---

<a id="item-3"></a>
## [Apple CEO Tim Cook to Step Down in 2026, John Ternus to Succeed](https://t.me/zaihuapd/41030) ⭐️ 9.0/10

Apple announced a leadership transition: current CEO Tim Cook will become Executive Chairman of the Board, and hardware engineering head John Ternus will become CEO effective September 1, 2026. This marks the first CEO change at Apple in over a decade, signaling a new era for the company's product strategy and corporate direction, with significant implications for the tech industry and investors. John Ternus joined Apple in 2001, became hardware engineering VP in 2013, and entered the executive team in 2021, overseeing iPhone, Mac, iPad, and AirPods development. Current Chairman Arthur Levinson will become Lead Independent Director on September 1, 2026.

telegram · zaihuapd · Apr 23, 13:46

**Background**: Tim Cook has been Apple's CEO since 2011, succeeding Steve Jobs. Under Cook, Apple's revenue and market capitalization grew dramatically, with product lines like iPhone, Apple Watch, and services expanding. The CEO transition is a rare event for the company, with Cook moving to a chairman role to ensure continuity.

**Tags**: `#Apple`, `#CEO transition`, `#leadership`, `#tech industry`

---

<a id="item-4"></a>
## [vLLM v0.20.0: CUDA 13, PyTorch 2.11, FlashAttention 4, TurboQuant](https://github.com/vllm-project/vllm/releases/tag/v0.20.0) ⭐️ 8.0/10

vLLM v0.20.0 is a major release with 546 commits from 257 contributors, introducing CUDA 13.0 as the default, upgrading to PyTorch 2.11, enabling FlashAttention 4 as the default MLA prefill backend, and adding TurboQuant 2-bit KV cache compression. This release significantly improves inference performance and memory efficiency for large language models, benefiting the entire AI/ML community by reducing hardware requirements and enabling larger model deployments. FlashAttention 4 now supports head-dim 512 and paged-KV on SM90+ GPUs, while TurboQuant delivers 4× KV cache capacity with 2-bit compression. The upgrade to PyTorch 2.11 is a breaking change for environment dependencies.

github · khluu · Apr 23, 21:02

**Background**: vLLM is a high-throughput, memory-efficient inference and serving engine for large language models (LLMs). It uses techniques like PagedAttention and continuous batching to optimize GPU memory and throughput. FlashAttention is a fast and memory-efficient attention algorithm, and KV cache compression reduces memory usage for long-context inference.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/vllm-project/vllm">GitHub - vllm-project/vllm: A high-throughput and memory-efficient inference and serving engine for LLMs · GitHub</a></li>
<li><a href="https://vllm.ai/">vLLM</a></li>

</ul>
</details>

**Tags**: `#vLLM`, `#LLM inference`, `#CUDA`, `#PyTorch`, `#FlashAttention`

---

<a id="item-5"></a>
## [Anthropic details Claude forgetfulness bug fix](https://www.anthropic.com/engineering/april-23-postmortem) ⭐️ 8.0/10

Anthropic disclosed that a bug introduced on March 26 caused Claude to appear forgetful and repetitive by clearing older thinking every turn instead of only once after idle sessions; the fix was deployed on April 10. This transparency helps restore user trust and highlights the challenges of maintaining consistent AI behavior in production, especially for complex coding tasks where context retention is critical. The bug affected Claude Sonnet 4.6 and Opus 4.6; additionally, on April 16, Anthropic added a system prompt instruction to reduce verbosity, addressing another community complaint.

hackernews · mfiguiere · Apr 23, 17:48

**Background**: Claude Code is an AI coding assistant that maintains a session context to remember previous interactions. When a session is idle for over an hour, clearing older thinking reduces latency upon resumption. The bug caused this clearing to repeat on every subsequent turn, making the model seem forgetful.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/engineering/april-23-postmortem">An update on recent Claude Code quality reports</a></li>
<li><a href="https://www.theregister.com/2026/04/13/claude_outage_quality_complaints/">Claude is getting worse, according to Claude • The Register</a></li>
<li><a href="https://github.com/anthropics/claude-code/issues/42796">[MODEL] Claude Code is unusable for complex engineering tasks with the Feb updates · Issue #42796 · anthropics/claude-code</a></li>

</ul>
</details>

**Discussion**: Community comments show mixed reactions: some appreciate the honest postmortem, while others remain skeptical about the timing and question whether other undisclosed changes also contributed to perceived quality drops. A few users note that competing models like GPT-5.4 have shown improvements.

**Tags**: `#AI`, `#Claude`, `#bug`, `#transparency`, `#LLM`

---

<a id="item-6"></a>
## [Tailscale Co-founder Critiques Cloud Complexity](https://crawshaw.io/blog/building-a-cloud) ⭐️ 8.0/10

Tailscale co-founder David Crawshaw published a blog post titled 'I am building a cloud,' criticizing the complexity of modern cloud infrastructure and Kubernetes, and proposing a simpler, more efficient cloud model. This critique from a respected industry figure highlights growing frustration with cloud complexity and could influence the direction of cloud infrastructure design, especially for smaller teams seeking simplicity. Crawshaw argues that Kubernetes is fundamentally flawed and that VMs are the wrong abstraction because they tie cost to CPU/memory rather than actual work done. He advocates for a cloud model that defaults to high performance and simplicity.

hackernews · bumbledraven · Apr 23, 04:44

**Background**: Cloud computing typically offers IaaS, PaaS, and SaaS models. Kubernetes has become the de facto container orchestration platform but is widely criticized for its operational complexity. Many enterprises struggle with Kubernetes in production due to its steep learning curve and overhead.

<details><summary>References</summary>
<ul>
<li><a href="https://tfir.io/kubernetes-complexity-deal-with-it-there-is-no-way-around-rob-hirschfeld-rackn/">Kubernetes Complexity - Deal With It; There Is No Way Around |</a></li>
<li><a href="https://www.cncf.io/blog/2025/03/06/too-complex-its-not-kubernetes-its-what-it-does/">Too Complex: It’s Not Kubernetes, It’s What It Does | CNCF</a></li>
<li><a href="https://cloudnativenow.com/video-interviews/rethinking-kubernetes-complexity-in-the-enterprise-with-paul-turner/">Rethinking Kubernetes Complexity in the Enterprise with Paul</a></li>

</ul>
</details>

**Discussion**: The Hacker News community largely agrees with Crawshaw's critique, with many sharing personal horror stories about Kubernetes complexity. Some express skepticism that a simpler cloud model can avoid the same bloat cycle, while others admire the vision but worry about profit motives.

**Tags**: `#cloud computing`, `#kubernetes`, `#infrastructure`, `#devops`

---

<a id="item-7"></a>
## [Ubuntu 26.04 LTS 'Resolute Raccoon' Released](https://lwn.net/Articles/1069399/) ⭐️ 8.0/10

Ubuntu 26.04 LTS, codenamed 'Resolute Raccoon', has been released on schedule, introducing TPM-backed full-disk encryption, expanded memory-safe components, improved application permission controls, and Livepatch support for Arm systems. This release significantly enhances security and resilience for Ubuntu users across desktop, server, and cloud, with TPM-backed encryption reducing reliance on passphrases and Livepatch for Arm minimizing downtime on ARM-based systems. Maintenance updates will be provided for 5 years for Ubuntu Desktop, Server, Cloud, WSL, and Core, while flavors will be supported for 3 years. The release also includes official flavors like Edubuntu, Kubuntu, and Xubuntu.

rss · LWN.net · Apr 23, 18:16

**Background**: TPM (Trusted Platform Module) is a hardware security chip that stores encryption keys securely, enabling full-disk encryption without requiring a passphrase at boot. Livepatch allows kernel security updates to be applied without rebooting, reducing downtime. Memory-safe components are written in languages like Rust that prevent common memory bugs, improving security.

<details><summary>References</summary>
<ul>
<li><a href="https://ubuntu.com/blog/tpm-backed-full-disk-encryption-is-coming-to-ubuntu">TPM-backed Full Disk Encryption is coming to Ubuntu | Ubuntu</a></li>
<li><a href="https://lwn.net/Articles/943869/">Ubuntu to add TPM-backed full-disk encryption [LWN.net]</a></li>
<li><a href="https://www.reddit.com/r/Ubuntu/comments/15pnh0b/canonicallivepatch_coming_to_arm/">canonical-livepatch coming to ARM? : r/Ubuntu - Reddit</a></li>

</ul>
</details>

**Tags**: `#Ubuntu`, `#Linux`, `#LTS`, `#security`, `#release`

---

<a id="item-8"></a>
## [Qwen 3.6 27B Ties Sonnet 4.6 on Agentic Index](https://www.reddit.com/gallery/1strodp) ⭐️ 8.0/10

Qwen 3.6 27B, a small 27-billion-parameter model, has matched Sonnet 4.6 on the Artificial Analysis Agentic Index, surpassing larger models like Gemini 3.1 Pro Preview and GPT 5.2/5.3. This demonstrates that small, locally-runnable models can achieve frontier-level agentic performance, potentially reducing reliance on expensive API providers and accelerating on-device AI deployment. The model made gains across all three sub-indices (Coding, Agentic, Knowledge), though the Coding Index uses Terminal Bench Hard and SciCode, which the author considers unusual choices. The 122B version is anticipated to be even more impressive.

reddit · r/LocalLLaMA · dionysio211 · Apr 23, 18:47

**Background**: The Artificial Analysis Agentic Index evaluates AI models on agentic capabilities using 10 benchmarks including Terminal-Bench Hard and SciCode. Terminal-Bench Hard tests command-line task execution, while SciCode assesses scientific coding. Small models like Qwen 3.6 27B are attractive for local inference due to lower hardware requirements.

<details><summary>References</summary>
<ul>
<li><a href="https://artificialanalysis.ai/">AI Model & API Providers Analysis | Artificial Analysis</a></li>
<li><a href="https://www.tbench.ai/benchmarks/terminal-bench-2?difficulties=hard">Terminal - Bench</a></li>
<li><a href="https://scicode-bench.github.io/">SciCode - SciCode Benchmark</a></li>

</ul>
</details>

**Discussion**: Community sentiment is highly positive, with users reporting successful local deployment on consumer GPUs (e.g., RTX 3090) and praising its multi-step tool-calling ability. Some skepticism exists about benchmark validity, with one commenter suggesting 'benchmaxxing' may inflate scores, while another noted that Sonnet still outperformed in a real-world file organization task.

**Tags**: `#LLM`, `#benchmarks`, `#open-source`, `#agentic`, `#local-inference`

---

<a id="item-9"></a>
## [US Memo on Adversarial Distillation Raises Open Model Concerns](https://i.redd.it/jp8emg4cqywg1.jpeg) ⭐️ 8.0/10

A US government memo from the Office of Science and Technology Policy expresses concern about large-scale extraction of frontier model capabilities through adversarial distillation, potentially leading to tighter controls on open models. This could reshape the future of open-source AI by treating model weights as strategic assets, balancing national security against innovation and accessibility. The memo specifically targets industrialized distillation using proxy accounts and jailbreak techniques, focusing on protecting proprietary models rather than open-source directly.

reddit · r/LocalLLaMA · MLExpert000 · Apr 23, 15:59

**Background**: Adversarial distillation is a technique where a target model's outputs are used to train a new model that mimics its behavior, potentially extracting proprietary capabilities. Frontier models are advanced AI systems with significant capabilities that could pose national security risks if widely accessible.

<details><summary>References</summary>
<ul>
<li><a href="https://www.frontiermodelforum.org/issue-briefs/issue-brief-adversarial-distillation/">Adversarial Distillation - Frontier Model Forum</a></li>
<li><a href="https://www.justsecurity.org/134124/costs-china-ai-distillation/">The Case for Imposing Costs on China's AI Distillation Campaigns</a></li>
<li><a href="https://rejoicehub.com/blogs/adversarial-distillation-ai-model-security">Adversarial Distillation AI: How to Protect Your AI Models - Rejoicehub</a></li>

</ul>
</details>

**Discussion**: Community comments are skeptical, with some comparing the move to historical overreactions like the search for WMDs, and others accusing AI companies like Anthropic and OpenAI of lobbying for regulation to stifle open-weight competition. Many see it as a pretext to restrict Chinese models and force US users to pay more.

**Tags**: `#AI regulation`, `#open source`, `#adversarial distillation`, `#national security`, `#frontier models`

---

<a id="item-10"></a>
## [85 TPS, 125K Context, Vision for Qwen3.6-27B on Single RTX 3090](https://medium.com/@fzbcwvv/an-overnight-stack-for-qwen3-6-27b-85-tps-125k-context-vision-on-one-rtx-3090-0d95c6291914?postPublishedType=repub) ⭐️ 8.0/10

A guide claims to achieve 85 tokens/second, 125K context length, and vision capabilities for the Qwen3.6-27B model on a single RTX 3090 using a custom inference stack, but a critical proprietary CUDA patch is not publicly released. This demonstrates the potential for running large open-weight models locally on consumer hardware, which could democratize access to powerful LLMs for developers and researchers. However, the missing patch raises concerns about reproducibility and transparency. The stack reportedly achieves 85 TPS with 125K context and vision on a single RTX 3090 (24GB VRAM), but requires a file named 'patch_tolist_cudagraph.py' that the author has not released. Community members have been unable to replicate the results without this patch.

reddit · r/LocalLLaMA · AmazingDrivers4u · Apr 23, 14:11

**Background**: Qwen3.6-27B is a dense 27-billion-parameter open-weight model released by Alibaba under Apache 2.0, excelling at coding tasks. Running such large models locally typically requires multiple high-end GPUs or significant optimization. The RTX 3090, with 24GB VRAM, is a popular consumer GPU for local LLM inference, but achieving high throughput and long context on a single card is challenging.

<details><summary>References</summary>
<ul>
<li><a href="https://simonwillison.net/2026/Apr/22/qwen36-27b/">Qwen3.6-27B: Flagship-Level Coding in a 27B Dense Model</a></li>
<li><a href="https://www.implicator.ai/alibaba-ships-qwen3-6-27b-an-open-weight-coding-model-that-beats-its-397b-moe/">Alibaba Qwen3.6-27B Dense Model Beats 397B Predecessor</a></li>

</ul>
</details>

**Discussion**: The community is impressed by the performance claims (85 TPS) but frustrated by the missing patch, with several commenters calling the post clickbait or self-promotion. Some users shared their own speeds (e.g., 25 t/s on multi-GPU, 30-40 t/s on RTX 5090) and requested the patch or a Docker image.

**Tags**: `#LLM inference`, `#Qwen`, `#RTX 3090`, `#performance optimization`, `#local LLM`

---

<a id="item-11"></a>
## [Tencent Releases Hy3 Preview: 295B MoE with 21B Active](https://www.reddit.com/gallery/1stk2mz) ⭐️ 8.0/10

Tencent has open-sourced the Hy3-preview, a 295-billion-parameter Mixture-of-Experts (MoE) language model with 21 billion active parameters, supporting a 256K context length. The model is available on Hugging Face and GitHub, with accompanying API and pricing plans from Tencent Cloud. This release demonstrates a major Chinese tech company's push into large-scale open-source MoE models, potentially accelerating AI development in complex reasoning and agent applications. The 21B active parameter count makes it theoretically feasible to run on high-end consumer hardware, though practical deployment remains challenging. The model uses a Mixture-of-Experts architecture with 295B total parameters but only 21B active per token, enabling efficient inference. Tencent reports a 54% reduction in first-token latency for products like CodeBuddy, and the model is already deployed in internal products such as Yuanbao, Tencent Docs, and QQ.

reddit · r/LocalLLaMA · TKGaming_11 · Apr 23, 14:17

**Background**: Mixture-of-Experts (MoE) is a neural network architecture that divides the model into multiple specialized sub-networks (experts) and activates only a subset for each input. This allows models to have a large total parameter count while keeping computational cost per token low, similar to how Gemma 4's 26B A4B model activates only 4B parameters. The 295B total with 21B active places Hy3-preview in a size class that could theoretically run on consumer hardware with sufficient RAM (e.g., 256GB), but practical use may require quantization.

<details><summary>References</summary>
<ul>
<li><a href="https://ai.google.dev/gemma/docs/core/model_card_4">Gemma 4 model card | Google AI for Developers</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained - Hugging Face</a></li>

</ul>
</details>

**Discussion**: Community sentiment is mixed: some praise the model's size and the release of a base model, but many criticize the license as restrictive, calling it 'weights available' rather than truly open-source. Others discuss hardware feasibility, noting that 256GB RAM on AM5 boards could run it, and express interest in comparisons with models like MiniMax 2.7 and Qwen 3.5.

**Tags**: `#LLM`, `#open-source`, `#MoE`, `#Tencent`, `#AI`

---

<a id="item-12"></a>
## [DeepSeek Open-Sources DeepEP V2 and TileKernels](https://www.reddit.com/r/LocalLLaMA/comments/1ste9zs/deepseek_has_released_deepep_v2_and_tilekernels/) ⭐️ 8.0/10

DeepSeek has released DeepEP V2, an efficient expert-parallel communication library, and TileKernels, a high-performance GPU kernel library written in TileLang, both open-source on GitHub. These releases advance parallelization and GPU kernel efficiency for large-scale AI training, potentially enabling linear scaling and supporting NVIDIA Blackwell GPUs, which could accelerate future model development. TileKernels covers MoE routing, FP8/FP4 quantization, and fused operators, targeting NVIDIA SM90 and SM100 (Blackwell) architectures, requiring CUDA 13.1 or later. DeepEP V2 focuses on expert-parallel communication optimization.

reddit · r/LocalLLaMA · External_Mood4719 · Apr 23, 09:57

**Background**: DeepSeek is a Chinese AI company known for its open-source large language models. Expert parallelism (EP) distributes model experts across GPUs to improve training efficiency, while GPU kernels are low-level programs that accelerate computations. TileLang is a domain-specific language for writing high-performance kernels.

**Discussion**: The community is highly positive, praising DeepSeek for open-sourcing and advancing research. Some speculate that the linear scaling technique and Blackwell support hint at a future model (possibly V4), and note that DeepSeek is doing what OpenAI was expected to do.

**Tags**: `#DeepSeek`, `#open-source`, `#GPU kernels`, `#parallel computing`, `#AI infrastructure`

---

<a id="item-13"></a>
## [Hairdryer used to rig Paris weather sensor, netting $34K on Polymarket](https://fibo-crypto.fr/en/blog/polymarket-weather-sensor-manipulation-paris-meteo-france-2026/) ⭐️ 8.0/10

A person manipulated a Météo-France temperature sensor at Paris Charles de Gaulle Airport using a hairdryer on April 6 and 15, causing abnormal readings that triggered winning bets on Polymarket's weather prediction market, earning over $34,000. This incident highlights the vulnerability of real-world data sources used by prediction markets and the potential for physical manipulation to generate financial gains, prompting Polymarket to switch data sources and raising legal and security concerns. On April 6, the sensor reading jumped from near 18°C to over 21°C within minutes; on April 15, the probability of the 22°C range surged from 0.1% to 95% in 30 minutes. Polymarket has switched its data source to Paris Le Bourget Airport but did not void the settled bets.

telegram · zaihuapd · Apr 23, 04:36

**Background**: Polymarket is a cryptocurrency-based prediction market where users bet on outcomes of real-world events. Weather prediction markets allow bets on specific temperature readings. Météo-France operates official weather stations, including at airports, which are typically considered reliable data sources.

<details><summary>References</summary>
<ul>
<li><a href="https://www.theguardian.com/world/2026/apr/23/hairdryer-or-lighter-french-police-look-at-claim-of-sensor-tampering-to-win-weather-bets">‘ Hairdryer or lighter?’: French police look at claim of sensor ...</a></li>
<li><a href="https://www.aol.com/articles/police-investigate-claims-hair-dryer-150607773.html">Police investigate after claims ‘ hair dryer used to manipulate weather ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Polymarket">Polymarket - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#prediction markets`, `#weather manipulation`, `#Polymarket`, `#fraud`, `#sensor tampering`

---

<a id="item-14"></a>
## [Google Cloud Default Security Flaw Causes Massive Bills](https://www.tomshardware.com/tech-industry/artificial-intelligence/google-cloud-customer-wakes-up-to-usd18-000-bill-despite-usd7-budget-thanks-to-forgotten-public-api-key-attacker-put-in-60-000-requests-and-blasted-through-usd1-400-spending-cap) ⭐️ 8.0/10

An AI consultant faced a $18,000+ Google Cloud bill despite setting a $7 budget, due to a leaked API key from a past project that attackers exploited to make 60,000 requests, bypassing spending caps. This incident highlights a systemic security flaw in Google Cloud's default configuration, where API keys can silently gain access to expensive Gemini AI endpoints, and budget caps are automatically raised without notification, putting all users at financial risk. The vulnerability stems from Google Cloud's Gemini API keys using a single format ("AIza" prefix) and security settings being disabled by default, allowing any exposed key to access Gemini endpoints. Additionally, Google Cloud automatically raises credit limits when thresholds are triggered without informing the user.

telegram · zaihuapd · Apr 23, 05:21

**Background**: API keys are credentials used to authenticate requests to cloud services. In Google Cloud, API keys were traditionally considered non-sensitive for low-risk services like Maps. However, with the introduction of Gemini AI, these same keys can now access expensive AI endpoints, but many users are unaware of this change. Google Cloud's budget alerts are advisory and do not enforce spending limits, and the system can automatically increase credit limits, exacerbating the risk.

<details><summary>References</summary>
<ul>
<li><a href="https://www.tomshardware.com/tech-industry/artificial-intelligence/google-cloud-customer-wakes-up-to-usd18-000-bill-despite-usd7-budget-thanks-to-forgotten-public-api-key-attacker-put-in-60-000-requests-and-blasted-through-usd1-400-spending-cap">Google Cloud customer wakes up to $18,000+ bill despite $7 budget ...</a></li>
<li><a href="https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules">Google API Keys Weren't Secrets. But then Gemini Changed the ...</a></li>
<li><a href="https://thehackernews.com/2026/02/thousands-of-public-google-cloud-api.html">Thousands of Public Google Cloud API Keys Exposed with Gemini ...</a></li>

</ul>
</details>

**Tags**: `#Google Cloud`, `#security`, `#API key`, `#cloud billing`, `#vulnerability`

---

<a id="item-15"></a>
## [ByteDance Releases Seed3D 2.0, 3D Generation Goes Production-Ready](https://seed.bytedance.com/zh/blog/seed3d-2-0-released-higher-precision-and-greater-usability) ⭐️ 8.0/10

ByteDance launched Seed3D 2.0 on April 23, 2026, a new generation 3D generation model that achieves state-of-the-art (SOTA) results in geometry and texture quality, with a human evaluation preference rate over 69% compared to mainstream models. This marks a significant step from demo-level 3D generation to production-ready assets, potentially accelerating the adoption of AI-generated 3D content in gaming, robotics, and simulation industries. Seed3D 2.0 also supports part-level generation and scene composition, outputting assets with complete joint information compatible with standard formats like URDF and physics simulation engines like NVIDIA Isaac Sim.

telegram · zaihuapd · Apr 23, 08:15

**Background**: 3D generation models aim to create 3D models from text or images. Previous models often produced low-quality geometry or textures, limiting their use to prototypes or visualizations. URDF is a standard XML format for robot models, and Isaac Sim is a robotics simulation platform from NVIDIA.

<details><summary>References</summary>
<ul>
<li><a href="https://news.aibase.com/news/27393">ByteDance Launches Seed3D 2.0: Geometry and Texture Dual SOTA ...</a></li>
<li><a href="https://github.com/aitools12/seed3d20">GitHub - aitools12/seed3d20: Seed3d 2.0 AI 3D model generator ...</a></li>
<li><a href="https://developer.nvidia.com/isaac/sim">Isaac Sim - Robotics Simulation and Synthetic Data Generation ...</a></li>

</ul>
</details>

**Tags**: `#3D Generation`, `#ByteDance`, `#AI`, `#Computer Graphics`, `#Machine Learning`

---

<a id="item-16"></a>
## [SFC and PwC Reach HK$1 Billion Settlement for Evergrande Fraud](https://apps.sfc.hk/edistributionWeb/gateway/TC/news-and-announcements/news/doc?refNo=26PR62) ⭐️ 8.0/10

The Hong Kong Securities and Futures Commission (SFC) announced on April 23, 2026, that it has reached a settlement with PwC Hong Kong, requiring PwC to set aside HK$1 billion to compensate eligible independent minority shareholders of China Evergrande Group for losses caused by financial fraud. This is the first time in Hong Kong that an auditor of a collapsed company has been required to compensate shareholders, setting a landmark precedent for auditor accountability and market integrity. It underscores the regulatory push to hold gatekeepers responsible for corporate fraud. The SFC found that Evergrande inflated revenue by 564.1 billion yuan over 2019-2020 through premature revenue recognition, turning losses into fictitious profits. PwC was found to have seriously breached professional duties, including loss of audit independence and lack of professional skepticism, but settled without admitting liability.

telegram · zaihuapd · Apr 23, 12:07

**Background**: China Evergrande Group, once one of China's largest property developers, collapsed in 2021 under massive debt, triggering a crisis in the real estate sector. The SFC investigation revealed that Evergrande manipulated financial statements to appear profitable, and PwC, as its auditor, failed to detect or report the fraud. This settlement follows previous penalties by Chinese regulators, including a combined fine of 441 million yuan against PwC in 2024.

<details><summary>References</summary>
<ul>
<li><a href="https://www.thepaper.cn/newsDetail_forward_33037031">香港证监会、会财局同日出手 普华永道同意预留10亿港元赔偿恒大股东_...</a></li>
<li><a href="https://news.qq.com/rain/a/20260423A0741400">普华永道，赔偿10亿港元、被罚3亿港元_腾讯新闻</a></li>

</ul>
</details>

**Tags**: `#finance`, `#regulation`, `#auditing`, `#fraud`, `#Evergrande`

---

<a id="item-17"></a>
## [China's Three Major Telecoms Suffer International Network Outage](https://t.me/zaihuapd/41029) ⭐️ 8.0/10

All three major Chinese telecom operators—China Unicom, China Telecom, and China Mobile—are experiencing widespread network failures affecting international routes, particularly to Hong Kong, Japan, and the US, with reports of severe packet loss and connection interruptions. This outage impacts millions of users and businesses relying on international connectivity, and given the geopolitical context, it raises questions about whether the cause is a technical failure or deliberate policy change. China Telecom's routes to Hong Kong and Japan, including premium CN2 and 9929 routes as well as standard 163 and 4837 routes, are affected; China Mobile's mobile data to overseas destinations also shows severe packet loss, especially for users in Beijing.

telegram · zaihuapd · Apr 23, 12:45

**Background**: Chinese telecom operators use different routing tiers: CN2 (ChinaNet Next Carrying Network) is China Telecom's premium international route, while 163 is the standard public route. Similarly, China Unicom uses 9929 (premium) and 4837 (standard). These routes are critical for international connectivity and are often optimized for low latency. BGP route leaks or hardware failures can cause widespread disruptions.

<details><summary>References</summary>
<ul>
<li><a href="https://gist.github.com/bgr24955/c05934370051d12d3677f2da4a260f32">VMRack VPS Review 2026: CN2 GIA Triple-Network Routes, Starting at ...</a></li>
<li><a href="https://www.explaintopic.com/networking/widespread-network-outage-across-china-telecom-infrastructur-1765803625.html">Widespread network outage across china telecom ... | ExplainTopic</a></li>
<li><a href="https://www.securityweek.com/china-telecom-routes-european-traffic-its-network-two-hours/">China Telecom Routes European Traffic to Its... - SecurityWeek</a></li>

</ul>
</details>

**Discussion**: The news post invites users to share their experiences, but no specific comments are provided in the content. The discussion is expected to be active given the real-time impact.

**Tags**: `#network outage`, `#China telecom`, `#internet censorship`, `#routing failure`, `#telecommunications`

---

<a id="item-18"></a>
## [UK NCSC Officially Endorses Passkeys as Primary Authentication](https://www.techradar.com/pro/security/uk-security-agency-officially-declares-passkeys-superior-to-passwords-passkeys-should-be-the-first-choice-for-authentication) ⭐️ 8.0/10

The UK National Cyber Security Centre (NCSC) has officially declared passkeys superior to traditional passwords and recommends them as the primary authentication method for digital services, ending its previous cautious stance. This endorsement from a major national cybersecurity authority signals a significant policy shift that could accelerate global adoption of passkeys, reducing reliance on vulnerable passwords and improving security for millions of users. Over 50% of active Google users in the UK have already registered passkeys, and major platforms like eBay and PayPal have adopted the technology. The NCSC noted that industry progress over the past 12 months resolved key implementation challenges.

telegram · zaihuapd · Apr 23, 14:47

**Background**: Passkeys are cryptographic credentials stored on a user's device, typically unlocked via biometrics (fingerprint or face recognition) or a PIN. They replace traditional passwords and are resistant to phishing and credential theft. The NCSC had previously been cautious due to early adoption hurdles but now considers the technology mature enough for widespread use.

<details><summary>References</summary>
<ul>
<li><a href="https://www.ncsc.gov.uk/blog-post/passkeys-not-perfect-getting-better">Passkeys : they're not perfect but they're getting better - NCSC .GOV.UK</a></li>
<li><a href="https://www.theregister.com/2026/04/23/ncsc_passkey_tech_now_reliable/">NCSC : Passkeys now good enough to be the default standard</a></li>
<li><a href="https://www.reddit.com/r/technology/comments/1stffrs/uk_security_agency_officially_declares_passkeys/">UK security agency officially declares passkeys superior to passwords</a></li>

</ul>
</details>

**Discussion**: Reddit comments on the news are mixed: some users welcome the move, noting passkeys are more secure and convenient, while others express concerns about device lock-in and recovery options if a device is lost. A few commenters point out that passkeys still have usability issues across different platforms.

**Tags**: `#cybersecurity`, `#authentication`, `#passkeys`, `#NCSC`, `#identity`

---

<a id="item-19"></a>
## [EU Pressures Google to Open Android to Rival AI Assistants](https://www.bloomberg.com/news/articles/2026-04-23/google-faces-eu-pressure-to-open-up-android-to-gemini-rivals) ⭐️ 8.0/10

The European Union is drafting regulations that would require Google to grant rival AI assistants, such as ChatGPT and Claude, the same system-level access on Android as its own Gemini assistant. This could reshape competition in the mobile AI assistant market, potentially giving users more choice while raising significant security and privacy concerns for Google and Android users. The requirements are still in draft stage and may be delayed. Google has expressed concerns that such openness could compromise user security and privacy.

telegram · zaihuapd · Apr 23, 15:31

**Background**: The EU has previously used the Digital Markets Act (DMA) to regulate big tech platforms, including requiring Google to offer choice screens for browsers and search engines. System-level access allows an AI assistant to interact deeply with the operating system, such as reading notifications or controlling apps, which is currently a privilege Google grants only to its own Gemini assistant on Android.

**Tags**: `#EU regulation`, `#Android`, `#AI assistants`, `#Google`, `#antitrust`

---

<a id="item-20"></a>
## [MIT Researchers Build Math Bridge Between Classical and Quantum Physics](https://www.newsy-today.com/new-study-bridges-the-worlds-of-classical-and-quantum-physics-mit-news/) ⭐️ 8.0/10

MIT researchers introduced a density term into the classical Hamilton-Jacobi equation, yielding results mathematically equivalent to the Schrödinger equation, thus providing a novel mathematical bridge between classical and quantum physics. This work offers a more concise mathematical description of quantum behavior, potentially improving predictions for qubit behavior in quantum computing and providing new insights toward unifying quantum mechanics with general relativity. The new framework can explain quantum phenomena such as the double-slit experiment and quantum tunneling. The researchers believe it could lead to better modeling of qubit dynamics.

telegram · zaihuapd · Apr 23, 16:30

**Background**: The Hamilton-Jacobi equation is a formulation of classical mechanics that describes particle motion as a wave, making it the 'closest approach' of classical mechanics to quantum mechanics. The Schrödinger equation is the fundamental equation of non-relativistic quantum mechanics, governing the wave function of a quantum system. This work bridges the two by adding a density term to the Hamilton-Jacobi equation.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Hamilton-Jacobi_equation">Hamilton-Jacobi equation</a></li>
<li><a href="https://en.wikipedia.org/wiki/Schrödinger_equation">Schrödinger equation</a></li>
<li><a href="https://en.wikipedia.org/wiki/Quantum_tunnelling">Quantum tunnelling</a></li>

</ul>
</details>

**Tags**: `#quantum physics`, `#mathematical physics`, `#quantum computing`, `#research breakthrough`

---

<a id="item-21"></a>
## [LiteParse for the Web: Browser-Based PDF Text Extraction](https://simonwillison.net/2026/Apr/23/liteparse-for-the-web/#atom-everything) ⭐️ 7.0/10

Simon Willison created a browser-based version of LlamaIndex's LiteParse, enabling PDF text extraction entirely in the browser using spatial text parsing heuristics without AI models. This tool provides a privacy-preserving, offline-capable alternative for PDF text extraction, which is especially useful for web developers and RAG-style Q&A systems that need to handle sensitive documents without sending data to servers. LiteParse for the web uses PDF.js and Tesseract.js, the same libraries as the Node.js CLI version, and supports optional OCR for scanned PDFs. It also offers a visual citations feature with bounding boxes to enhance answer credibility.

rss · Simon Willison · Apr 23, 21:54

**Background**: LiteParse is an open-source project from LlamaIndex that extracts text from PDFs using spatial text parsing heuristics rather than AI models. It handles multi-column layouts and outputs text in a sensible linear order. The original version was a Node.js CLI tool; this browser port makes it accessible without installation.

<details><summary>References</summary>
<ul>
<li><a href="https://www.marktechpost.com/2026/03/19/llamaindex-releases-liteparse-a-cli-and-typescript-native-library-for-spatial-pdf-parsing-in-ai-agent-workflows/">LlamaIndex Releases LiteParse: A CLI and TypeScript-Native</a></li>
<li><a href="https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/">Running OCR against PDFs and images directly in your browser</a></li>

</ul>
</details>

**Tags**: `#PDF parsing`, `#browser`, `#open source`, `#text extraction`, `#LlamaIndex`

---

<a id="item-22"></a>
## [Famfs Filesystem Faces Potential BPF Redesign](https://lwn.net/Articles/1068686/) ⭐️ 7.0/10

At the 2026 LSFMM+BPF summit, a suggestion emerged to rewrite the famfs filesystem using BPF instead of its current FUSE-based implementation, causing frustration for maintainer John Groves who believed the code was nearly ready for mainline merging. This debate could significantly delay the adoption of famfs, a specialized filesystem for CXL-attached shared memory that enables efficient access to large read-mostly datasets across multiple systems. The outcome will influence how future kernel filesystems balance performance and maintainability. Famfs originally used a standalone kernel filesystem, then moved to FUSE with two new operations (GET_FMAP and GET_DAXDEV) to avoid user-space page fault overhead. The new proposal suggests moving famfs-specific logic into BPF programs, which could further reduce kernel changes but requires significant rework.

rss · LWN.net · Apr 23, 13:44

**Background**: Famfs (Fabric Attached Memory File System) is designed for large read-mostly datasets stored in CXL-attached shared memory, allowing multiple hosts to access data via mmap() without system calls. CXL (Compute Express Link) is an interconnect that maintains memory coherency between CPUs and attached devices, enabling resource pooling. The LSFMM+BPF summit is an annual gathering of Linux kernel developers focused on storage, filesystems, memory management, and BPF.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/cxl-micron-reskit/famfs">GitHub - cxl-micron-reskit/famfs: This is the user space repo ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Compute_Express_Link">Compute Express Link - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#filesystem`, `#CXL`, `#BPF`, `#memory management`

---

<a id="item-23"></a>
## [PI Coding Agent with Qwen3.6 35b Impresses Users](https://www.reddit.com/r/LocalLLaMA/comments/1stjwg5/been_using_pi_coding_agent_with_local_qwen36_35b/) ⭐️ 7.0/10

A Reddit user shared a positive experience using the open-source PI Coding Agent with the local Qwen3.6 35b A3B model, highlighting a custom 'plan-first' skill file that enforces step-by-step execution before writing any code. 这表明本地开源编程助手现在可以媲美 Claude Code 等基于云的订阅服务，在保持实际项目高性能的同时，可能为用户节省大量成本。 The Qwen3.6 35b A3B model uses only 3B active parameters, enabling fast inference on consumer hardware like a MacBook Pro M4 Pro with 48GB RAM. The plan-first skill file is shared as a markdown file that enforces a structured workflow with phases for analysis, clarification, planning, and execution.

reddit · r/LocalLLaMA · SoAp9035 · Apr 23, 14:11

**Background**: PI Coding Agent is an open-source terminal-based coding assistant developed by Mario Zechner. Qwen3.6 35b A3B is Alibaba's latest open-source model with a mixture-of-experts architecture, supporting up to 262K context tokens. Skill files in PI are similar to Claude Code's skills, allowing users to define custom workflows.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/Pi_Coding_Agent">Pi Coding Agent</a></li>
<li><a href="https://medium.com/data-science-in-your-pocket/qwen3-6-35b-a3b-the-tiny-active-open-model-that-thinks-codes-and-agents-like-a-much-bigger-one-486d535e372e">Qwen 3 . 6 – 35 B - A 3 B : The Tiny-Active Open Model That... | Medium</a></li>

</ul>
</details>

**Discussion**: Community members confirmed similar success, with one user canceling both IDE and Claude subscriptions after switching to PI with Qwen3.6 35b. Others asked about differences from OpenCode's plan mode and whether PI is worth moving from Claude Code, with overall sentiment being very positive.

**Tags**: `#local-llm`, `#coding-agent`, `#qwen`, `#open-source-ai`, `#skill-file`

---

<a id="item-24"></a>
## [Indian student uses AI to create fake influencer targeting US conservatives](https://www.indiatoday.in/india/story/indian-medical-students-fake-ai-influencer-instagram-us-republican-audience-jennifer-lawrence-syndey-sweeney-2899820-2026-04-22) ⭐️ 7.0/10

A 22-year-old Indian medical student named Sam used Google Gemini to create a fake conservative influencer persona, Emily Hart, on Instagram and Fanvue, earning thousands of dollars from US MAGA audiences. This case highlights the growing misuse of AI to create convincing fake personas for political and financial gain, raising serious concerns about misinformation, AI ethics, and the vulnerability of targeted demographics. Sam initially posted generic attractive photos but got low engagement; Gemini advised targeting conservative audiences for higher loyalty and disposable income. The fake persona posted content like ice fishing and shooting range photos, and sold AI-generated adult images on Fanvue.

telegram · zaihuapd · Apr 23, 02:21

**Background**: Google Gemini is a generative AI chatbot and virtual assistant developed by Google, capable of providing advice and generating content. Fanvue is a subscription social platform that allows creators to earn money, and it has gained traction as an alternative for AI-generated content. The MAGA audience refers to supporters of Donald Trump's 'Make America Great Again' movement, often characterized by conservative values.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Google_Gemini">Google Gemini - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Fanvue">Fanvue - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#AI`, `#misinformation`, `#social media`, `#ethics`, `#politics`

---

<a id="item-25"></a>
## [OpenAI's macOS Chronicle Feature Sparks Privacy and Security Concerns](https://www.theregister.com/2026/04/22/openai_chronicle_no_privacy_screenshot/) ⭐️ 7.0/10

OpenAI released Chronicle, an opt-in research preview for the Codex app on macOS, which periodically captures screenshots and uses OCR to store extracted text as persistent memory. Security researchers have flagged that the OCR text is stored unencrypted locally and is vulnerable to prompt injection attacks. This feature mirrors the controversial Microsoft Recall, raising significant privacy and security risks for users, especially developers who may handle sensitive data. The unencrypted local storage and susceptibility to prompt injection could lead to data leaks and unauthorized access. Chronicle is currently limited to ChatGPT Pro subscribers on macOS and is not available in the EU, UK, or Switzerland. Screenshot data is stored locally for only 6 hours, but OCR-extracted text is kept indefinitely in unencrypted form and can be accessed by other programs on the device.

telegram · zaihuapd · Apr 23, 03:06

**Background**: Chronicle is a screen-aware memory feature that builds a persistent record of user activity by analyzing screen content. Prompt injection attacks exploit vulnerabilities in AI models by injecting malicious prompts, potentially causing the model to leak data or perform unintended actions. OCR (Optical Character Recognition) technology converts images of text into machine-readable text.

<details><summary>References</summary>
<ul>
<li><a href="https://9to5mac.com/2026/04/20/codex-for-mac-gains-chronicle-for-enhancing-context-using-recent-screen-content/">OpenAI releases Codex ' Chronicle ' feature for enhancing... - 9to5 Mac</a></li>
<li><a href="https://www.neowin.net/news/openai-introduces-chronicle-for-codex-a-recall-like-memory-feature-for-developers-on-macos/">OpenAI introduces Chronicle for Codex, a Recall-like memory feature ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Prompt_injection_attack">Prompt injection attack</a></li>

</ul>
</details>

**Tags**: `#AI`, `#privacy`, `#security`, `#OpenAI`, `#macOS`

---

<a id="item-26"></a>
## [TSMC Delays High-NA EUV Adoption Until 2029 Due to Cost](https://money.udn.com/money/story/5599/9458925?from=edn_newestlist_rank) ⭐️ 7.0/10

TSMC announced at its North America Technology Forum that it will not use ASML's high-NA EUV lithography for mass production until at least 2029, citing the equipment's high cost—over €350 million per unit. The company also revealed that its A13 process will start production in 2029 and outlined plans to build CoWoS and 3D-IC packaging capacity in Arizona by that year. This decision signals that TSMC, the world's leading foundry, believes current EUV tools can be extended further, potentially slowing the adoption of high-NA EUV across the industry. It also highlights the growing importance of advanced packaging, as TSMC invests in US-based CoWoS and 3D-IC to complete its domestic supply chain. High-NA EUV (0.55 NA) offers 8nm resolution, enabling smaller metal pitches for sub-2nm nodes, but costs over €350 million per system. TSMC will continue to optimize its existing EUV tools for the A13 node (likely 2nm or below) and expects its first Arizona fab's yield to approach that of its Taiwan fabs, with the second fab starting mass production next year.

telegram · zaihuapd · Apr 23, 11:22

**Background**: High-NA EUV lithography is a next-generation semiconductor manufacturing technology developed by ASML, using a 0.55 numerical aperture to achieve 8nm resolution, critical for nodes below 3nm. CoWoS (Chip-on-Wafer-on-Substrate) and 3D-IC are advanced packaging technologies that integrate multiple chips vertically or horizontally, improving performance and reducing footprint. TSMC's US expansion aims to localize production and packaging to meet demand from American customers.

<details><summary>References</summary>
<ul>
<li><a href="https://zhuanlan.zhihu.com/p/688959589">High-NA EUV光刻机入场，究竟有多强？ - 知乎</a></li>
<li><a href="https://baike.baidu.com/item/High-NA+EUV/65485250">High-NA EUV - 百度百科</a></li>
<li><a href="https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm">CoWoS® - Taiwan Semiconductor Manufacturing Company Limited</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#TSMC`, `#ASML`, `#EUV lithography`, `#manufacturing`

---
