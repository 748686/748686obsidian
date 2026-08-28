---
layout: default
title: "Horizon Summary: 2026-05-11 (EN)"
date: 2026-05-11
lang: en
---

> From 28 items, 8 important content pieces were selected

---

1. [EU Digital Wallet Hardware Attestation Locks Identities to Duopoly](#item-1) ⭐️ 8.0/10
2. [Fictional Incident Report Highlights Rust Supply Chain Risks](#item-2) ⭐️ 8.0/10
3. [Linux Port of Space Cadet Pinball Delights Original Developers](#item-3) ⭐️ 8.0/10
4. [AI Coding Tools Induce Task Paralysis and Addiction](#item-4) ⭐️ 8.0/10
5. [Token speed visualization tool helps local LLM users feel performance](#item-5) ⭐️ 8.0/10
6. [MTP Speeds Coding But Slows Creative Writing](#item-6) ⭐️ 8.0/10
7. [Qwen3.6 35B A3B on 8GB VRAM at 40 tok/s](#item-7) ⭐️ 8.0/10
8. [NVIDIA Star Elastic: One Checkpoint, Three Models via Zero-Shot Slicing](#item-8) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [EU Digital Wallet Hardware Attestation Locks Identities to Duopoly](https://grapheneos.social/@GrapheneOS/116550899908879585) ⭐️ 8.0/10

The EU Digital Identity Wallet (EUDI) mandates hardware attestation from Google or Apple, effectively requiring all digital identities to be tied to devices approved by these American tech giants. This requirement undermines digital sovereignty and privacy by locking EU citizens into the Google/Apple duopoly, raising concerns about monopoly power and surveillance capabilities. Hardware attestation uses device-specific keys verified by Google or Apple, and the system lacks zero-knowledge proofs, meaning each attestation packet can link actions to a specific device.

hackernews · ChuckMcM · May 10, 17:54 · [Discussion](https://news.ycombinator.com/item?id=48086190)

**Background**: Hardware attestation is a security mechanism where a device's hardware proves its identity to a remote server, typically using a trusted platform module or secure enclave. The EU Digital Identity Wallet is a pan-European initiative to provide a unified digital identity for citizens. Requiring attestation only from Google or Apple effectively excludes devices without their approval, such as those with open-source operating systems.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/EU_Digital_Identity_Wallet">EU Digital Identity Wallet - Wikipedia</a></li>
<li><a href="https://commission.europa.eu/topics/digital-economy-and-society/european-digital-identity_en">European Digital Identity - European Commission</a></li>
<li><a href="https://developer.android.com/privacy-and-security/security-key-attestation">Verify hardware-backed key pairs with key attestation</a></li>

</ul>
</details>

**Discussion**: Commenters expressed strong opposition, noting that the requirement locks digital identities to the American duopoly and lacks privacy protections like zero-knowledge proofs. Some drew parallels to historical controversies such as Intel's CPU serial numbers and Windows 11's TPM requirements, arguing that this trend erodes user control and privacy.

**Tags**: `#hardware attestation`, `#digital identity`, `#monopoly`, `#EU digital wallet`, `#privacy`

---

<a id="item-2"></a>
## [Fictional Incident Report Highlights Rust Supply Chain Risks](https://nesbitt.io/2026/02/03/incident-report-cve-2024-yikes.html) ⭐️ 8.0/10

A detailed fictional incident report, CVE-2024-YIKES, illustrates a sophisticated supply chain attack on the Rust crate ecosystem, where a compromised transitive dependency (vulpine-lz4) with few stars is used to infiltrate the cargo build pipeline. This report highlights the real and growing threat of supply chain attacks in open-source ecosystems, particularly the Rust crate ecosystem, where small, obscure packages can have outsized influence due to transitive dependencies. The attack vector involves compromising credentials of a maintainer of a small library that is a transitive dependency of cargo itself, demonstrating how low-star packages can be used as entry points.

hackernews · miniBill · May 10, 17:43 · [Discussion](https://news.ycombinator.com/item?id=48086082)

**Background**: Software supply chain attacks target the development and distribution pipeline, inserting malicious code into legitimate software. In the Rust ecosystem, crates.io is the official package registry, and cargo relies on many dependencies, some of which may have minimal oversight. This fictional scenario mirrors real-world incidents like the SolarWinds attack and the ua-parser-js compromise.

<details><summary>References</summary>
<ul>
<li><a href="https://users.rust-lang.org/t/are-rust-crates-secure/18860">Are Rust crates secure? - The Rust Programming Language Forum</a></li>
<li><a href="https://users.rust-lang.org/t/regarding-the-security-safety-of-libraries-on-crates-io/66294">Regarding the Security / Safety of Libraries on Crates.io - The</a></li>
<li><a href="https://www.breachsense.com/blog/supply-chain-attack-examples/">10 Supply Chain Attack Examples and How to Detect Them</a></li>

</ul>
</details>

**Discussion**: Commenters recognized the story as fiction but praised its realism and technical accuracy. Some users pointed out specific crates that could be similarly exploited, while others reflected on the broader security challenges in the age of rapid development.

**Tags**: `#supply-chain`, `#security`, `#incident-response`, `#rust`, `#fictional-scenario`

---

<a id="item-3"></a>
## [Linux Port of Space Cadet Pinball Delights Original Developers](https://brennan.io/2026/05/09/pinball-and-escrow/) ⭐️ 8.0/10

A reverse-engineered port of the classic Space Cadet Pinball game has been released for Linux, developed entirely from decompiled executables without access to the original source code. This port preserves an iconic piece of gaming history that was bundled with Microsoft Windows for years, and its creation highlights the skill and dedication of the reverse-engineering community. The original developers' enthusiastic response underscores the emotional and historical value of such preservation efforts. The port was created solely by reverse engineering the original Windows executable, without reference to the source code, and is reported to be an extremely accurate recreation. The project has also been ported to multiple consoles and a browser-based version is available online.

hackernews · jandeboevrie · May 10, 11:22 · [Discussion](https://news.ycombinator.com/item?id=48082968)

**Background**: Space Cadet Pinball, originally part of the 1995 game Full Tilt! Pinball by Cinematronics, was licensed to Microsoft and included as 3D Pinball for Windows – Space Cadet in Windows Plus! and later Windows operating systems. Reverse engineering is a technique used to recreate software by analyzing its compiled binary, often to enable modern platform support or preservation.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Space_cadet_pinball">Space cadet pinball</a></li>
<li><a href="https://dos.zone/microsoft-3d-pinball-space-cadet/">Microsoft 3D Pinball: Space Cadet | DOS games in browser</a></li>
<li><a href="https://pinball.alula.me/">3D Pinball for Windows - Space Cadet</a></li>

</ul>
</details>

**Discussion**: Community response has been overwhelmingly positive, with the original author expressing delight and sharing the post with co-founders. Commenters praised the port's accuracy and noted that it was done 'blind' without original source code, comparing it to the classic pinball wizard quote.

**Tags**: `#reverse engineering`, `#game porting`, `#Linux`, `#preservation`, `#retro gaming`

---

<a id="item-4"></a>
## [AI Coding Tools Induce Task Paralysis and Addiction](https://g5t.de/articles/20260510-task-paralysis-and-ai/index.html) ⭐️ 8.0/10

A personal blog post and community discussion highlight that AI coding tools, initially seen as productivity boosters, are causing task paralysis, addiction, and a loss of joy in programming for many developers. This reflects a growing concern about the psychological impact of AI on developers, particularly those with ADHD, and challenges the narrative that AI is purely beneficial for productivity. Commenters describe a shift from deep technical engagement to managing AI agents, with recurring patterns of addiction like dopamine chasing and burnout, despite initial productivity gains.

hackernews · MrGilbert · May 10, 06:20 · [Discussion](https://news.ycombinator.com/item?id=48081469)

**Background**: Task paralysis is a psychological state where an individual feels unable to start or complete tasks due to overwhelm or indecision. AI coding tools like Claude Code generate code or plans quickly, which can initially reduce friction but may lead to dependency, reducing the developer's sense of ownership and deep focus. The phenomenon is particularly relevant for individuals with ADHD, who are more susceptible to dopamine-driven feedback loops.

**Discussion**: Commenters overwhelmingly agree with the article, sharing personal experiences of lost joy and addiction-like behaviors. Some express concern about the inability to stop using AI tools in a professional setting, while others describe a nostalgic longing for deeper technical problem-solving.

**Tags**: `#AI`, `#developer experience`, `#mental health`, `#productivity`, `#ADHD`

---

<a id="item-5"></a>
## [Token speed visualization tool helps local LLM users feel performance](https://www.reddit.com/r/LocalLLaMA/comments/1t99upf/getting_a_feel_for_how_fast_x_tokenssecond_really/) ⭐️ 8.0/10

A developer created a web-based tool called tokenspeed that simulates token generation at user-specified speeds to give a subjective feel for local LLM performance. It supports text, code, and reasoning + code modes. This tool addresses a common problem for the local LLM community: abstract tokens/second numbers are hard to interpret subjectively. It helps users make informed decisions about model and hardware choices by providing a visceral sense of speed. The tool is available as a web demo and also as a Python script for local execution. It includes a 'Think + Code' mode that simulates the thinking process of reasoning models like Qwen, though some users noted this mode may not fully replicate real behavior.

reddit · r/LocalLLaMA · MikeNonect · May 10, 15:23

**Background**: Tokens per second (tokens/s) is a common metric for LLM inference speed, but its subjective experience varies based on context such as chat versus coding. Local LLM enthusiasts often share performance numbers, but interpreting whether a speed is 'fast enough' is difficult without a point of reference. This tool provides a reference by simulating output at a given rate.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>
<li><a href="https://openllmbenchmarks.com/index.html">LLM Token Generation Speed Simulator & Benchmark | Compare</a></li>

</ul>
</details>

**Discussion**: The community overwhelmingly praised the tool as a brilliant and much-needed resource. Users discussed subjective speed thresholds and provided constructive feedback on the realism of the reasoning simulation, with some requesting a community showcase to prevent such projects from being buried.

**Tags**: `#local-llm`, `#tokens-per-second`, `#visualization`, `#performance`, `#tool`

---

<a id="item-6"></a>
## [MTP Speeds Coding But Slows Creative Writing](https://www.reddit.com/r/LocalLLaMA/comments/1t9gcar/mtp_benchmark_results_the_nature_of_the/) ⭐️ 8.0/10

Systematic benchmarks of Multi-Token Prediction (MTP) speculative inference on Qwen 3.6 27B reveal that task type determines performance: coding tasks nearly triple in speed at F16, while creative writing slows down at Q4_K_M quantization. This finding clarifies contradictory user reports and shows that speculative inference benefits are highly task-dependent, crucial for optimizing LLM deployment in coding assistants versus creative writing tools. The benchmarks tested five quantization levels (Q4_K_M, Q5_K_M, Q6_K, Q8_0, F16) and four task types (code, factual, analysis, creative), with temperature and MTP quantization having minimal impact. F16 + MTP tripled coding speed, while Q4_K_M + MTP slowed creative writing.

reddit · r/LocalLLaMA · ex-arman68 · May 10, 19:25

**Background**: Multi-Token Prediction (MTP) is a speculative decoding technique where a draft model predicts multiple tokens simultaneously, which are then verified by the main model. Quantization methods like Q4_K_M reduce model size and memory bandwidth at the cost of accuracy, commonly used for local LLM inference. The task dependency arises because coding tasks have more predictable token patterns, yielding higher acceptance rates, while creative writing has lower predictability.

<details><summary>References</summary>
<ul>
<li><a href="https://www.buildfastwithai.com/blogs/gemma-4-mtp-drafter-faster-inference">Gemma 4 MTP Drafter: Get 3x Faster Inference (2026 Guide)</a></li>
<li><a href="https://medium.com/@paul.ilvez/demystifying-llm-quantization-suffixes-what-q4-k-m-q8-0-and-q6-k-really-mean-0ec2770f17d3">Demystifying LLM Quantization Suffixes: What Q4_K_M, Q8_0 ...</a></li>
<li><a href="https://willitrunai.com/blog/quantization-guide-gguf-explained">Q4_K_M vs Q5_K_M vs Q8 — Which GGUF Quantization Should You ...</a></li>

</ul>
</details>

**Discussion**: Commenters noted that MoE models suffer more from MTP slowdown when partially offloaded, and that prompt processing speed can drop significantly (e.g., from 1400 t/s to 650 t/s) on some GPUs. Another user reported ~70% acceptance rate and 70–120 t/s on an RTX 5090 for coding tasks with Q6 quantization.

**Tags**: `#speculative inference`, `#MTP`, `#LLM inference`, `#benchmark`, `#coding vs creative`

---

<a id="item-7"></a>
## [Qwen3.6 35B A3B on 8GB VRAM at 40 tok/s](https://www.reddit.com/r/LocalLLaMA/comments/1t9eo83/running_qwen36_35b_a3b_on_8gb_vram_and_32gb_ram/) ⭐️ 8.0/10

A user shared a configuration to run Qwen3.6 35B A3B GGUF Q5 quant on an RTX 4060 with 8GB VRAM and 32GB RAM, achieving approximately 40 tokens per second with ~190k context. This shows that large mixture-of-experts (MoE) models can run efficiently on consumer hardware, making local LLM deployment more accessible to users with limited GPU memory. The setup uses llama-server with flags --ctx-size 192640, --n-gpu-layers 430, --n-cpu-moe 35, and flash-attention, achieving 40-43 tok/s on Q5_K_M quantized models. The model is a 35B parameter MoE with approximately 3B active parameters per token.

reddit · r/LocalLLaMA · Atul_Kumar_97 · May 10, 18:24

**Background**: Qwen3.6 35B A3B is a hybrid sparse mixture-of-experts model combining Gated DeltaNet linear attention with standard gated attention. The GGUF format allows running quantized models on CPU/GPU via llama.cpp. The --n-cpu-moe flag offloads expert layers to CPU to fit larger models within limited VRAM by using system RAM for MoE components.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/Qwen/Qwen3.6-35B-A3B">Qwen/Qwen3.6-35B-A3B · Hugging Face</a></li>
<li><a href="https://openrouter.ai/qwen/qwen3.6-35b-a3b">Qwen3.6 35B A3B - API Pricing & Benchmarks | OpenRouter</a></li>
<li><a href="https://huggingface.co/blog/Doctor-Shotgun/llamacpp-moe-offload-guide">Performant local mixture-of-experts CPU inference with GPU ...</a></li>

</ul>
</details>

**Discussion**: Some users felt the 35B model produces noticeably worse quality than the 27B variant, suggesting a 27B Q6 at 125k context as a sweet spot. Others praised the speed and shared optimization tips such as using --fit-on instead of manual offloading.

**Tags**: `#local-llm`, `#Qwen3.6`, `#llama.cpp`, `#model-optimization`, `#gguf`

---

<a id="item-8"></a>
## [NVIDIA Star Elastic: One Checkpoint, Three Models via Zero-Shot Slicing](https://www.reddit.com/r/LocalLLaMA/comments/1t8s83r/nvidia_ai_releases_star_elastic_one_checkpoint/) ⭐️ 8.0/10

NVIDIA AI has released Star Elastic, a post-training method that nests 23B and 12B submodels inside a 30B parent checkpoint, allowing zero-shot extraction of three reasoning models from a single file in BF16, FP8, and NVFP4 formats. This approach enables dynamic compute scaling without duplicating KV cache state, significantly reducing VRAM overhead and allowing inference engines to adapt model size per request, which is a breakthrough for efficient deployment of large language models. The nested submodels share a KV cache, so smaller models can be used for fast reasoning while larger models guide or evaluate, effectively creating a sliding scale of compute. The router learns the architecture rather than just the weights.

reddit · r/LocalLLaMA · phazei · May 10, 00:48

**Background**: Zero-shot slicing refers to extracting multiple model sizes from a single checkpoint without any additional training, analogous to scalable video coding where a single stream contains multiple resolutions. The KV cache is a memory structure in transformer models that stores key-value tensors from self-attention layers, reducing redundant computation. By sharing the KV cache across submodels, Star Elastic avoids duplicating cached states when switching between model sizes.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/html/2510.11106v1">Compositional Zero-Shot Learning: A Survey - arXiv</a></li>
<li><a href="https://peterchng.com/blog/2024/06/11/what-is-the-transformer-kv-cache/">What is the Transformer KV Cache?</a></li>

</ul>
</details>

**Discussion**: Community comments show mixed reactions: some are confused about why not always use the 30B model and whether smaller model thinking degrades larger model answers, while others highlight the shared KV cache as the most interesting part for deployment efficiency. The comparison to Qwen and Gemma E2B/E4B is also noted.

**Tags**: `#NVIDIA`, `#Star Elastic`, `#zero-shot slicing`, `#KV cache`, `#efficient deployment`

---