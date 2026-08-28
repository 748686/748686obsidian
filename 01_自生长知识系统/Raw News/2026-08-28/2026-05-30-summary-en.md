---
layout: default
title: "Horizon Summary: 2026-05-30 (EN)"
date: 2026-05-30
lang: en
---

> From 53 items, 16 important content pieces were selected

---

1. [vLLM v0.22.0 Released with DeepSeek V4 Maturity and Rust Frontend](#item-1) ⭐️ 9.0/10
2. [Probe-Targeted Fine-Tuning Makes LLMs Express True Confidence](#item-2) ⭐️ 9.0/10
3. [Hacker finds critical flaws in CBSE online exam grading system](#item-3) ⭐️ 9.0/10
4. [California Assembly Passes 'Protect Our Games Act'](#item-4) ⭐️ 8.0/10
5. [Is AI repeating frontend's 'lost decade'?](#item-5) ⭐️ 8.0/10
6. [Anthropic run-rate revenue reaches $47 billion](#item-6) ⭐️ 8.0/10
7. [Loadable Crypto Module Proposed for FIPS Certification](#item-7) ⭐️ 8.0/10
8. [Protestware targets AI coding agents via jqwik library](#item-8) ⭐️ 8.0/10
9. [Monokernel achieves 3,300 tokens/s on AMD MI300X](#item-9) ⭐️ 8.0/10
10. [Qwen3.6-27B Quantization Benchmark by User](#item-10) ⭐️ 8.0/10
11. [Multi-Token Prediction speeds up inference up to 3.34x](#item-11) ⭐️ 8.0/10
12. [Nvidia teases N1X laptop chip with 20 ARM cores, 6144 CUDA cores for Computex](#item-12) ⭐️ 8.0/10
13. [StepFun Releases Step 3.7 Flash, a 196B MoE Model](#item-13) ⭐️ 8.0/10
14. [BYD offers one-year accident liability coverage for city NOA](#item-14) ⭐️ 8.0/10
15. [China Certifies Nine Domestic AI Chips for Gov Procurement](#item-15) ⭐️ 8.0/10
16. [Blue Origin's New Glenn Rocket Explodes in Static Fire Test](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [vLLM v0.22.0 Released with DeepSeek V4 Maturity and Rust Frontend](https://github.com/vllm-project/vllm/releases/tag/v0.22.0) ⭐️ 9.0/10

vLLM released version 0.22.0 with 459 commits from 230 contributors, featuring major hardening for DeepSeek V4, progress on Model Runner V2 toward default, and an experimental Rust frontend. Key improvements include NVFP4 fused MoE support, piecewise CUDA graphs, MTP speculative decoding, and multi-tier KV cache offloading. This release significantly enhances the inference efficiency and model support for DeepSeek V4, a state-of-the-art MoE model, while pushing Model Runner V2 towards broader adoption. The experimental Rust frontend also signals vLLM's exploration of performance-critical paths in a safer systems language. DeepSeek V4 now has a dedicated package, NVFP4 fused MoE, full and piecewise CUDA graph support, and MTP speculative decoding. Model Runner V2 gains an oracle to select it for Qwen3 dense models and automatic fallback to MRv1 when a KV connector is present.

github · khluu · May 29, 10:28

**Background**: vLLM is a high-throughput LLM inference engine with PagedAttention for efficient memory management. DeepSeek V4 is a Mixture-of-Experts (MoE) model that requires specialized kernel optimizations. NVFP4 fused MoE uses 4-bit floating point for faster expert computation, piecewise CUDA graphs reduce graph compilation overhead, and MTP speculative decoding uses Multi-Token Prediction drafters to speed up generation.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.vllm.ai/en/v0.15.0/api/vllm/model_executor/layers/fused_moe/oracle/nvfp4/">vllm.model_executor.layers. fused _ moe .oracle. nvfp4</a></li>
<li><a href="https://docs.sglang.io/docs/advanced_features/piecewise_cuda_graph">Piecewise CUDA Graph - SGLang Documentation</a></li>
<li><a href="https://njannasch.dev/blog/mtp-speculative-decoding-qwen-3-6-5060ti/">MTP Speculative Decoding Actually Works on MoE: 144 t/s on a</a></li>

</ul>
</details>

**Tags**: `#vllm`, `#LLM inference`, `#DeepSeek`, `#Rust`, `#open source`

---

<a id="item-2"></a>
## [Probe-Targeted Fine-Tuning Makes LLMs Express True Confidence](https://www.reddit.com/r/MachineLearning/comments/1tqrtkn/making_llms_tell_you_how_confident_they_really/) ⭐️ 9.0/10

Researchers developed probe-targeted fine-tuning (LoRA) that uses internal probe signals to teach LLMs to verbalize their actual confidence in answers, achieving causal shifts verified by activation patching. This addresses the key problem of LLM miscalibration where models often express overconfident responses (99% confidence) despite internally distinguishing correct from incorrect answers with high AUROC (0.76-0.88), providing a simple, efficient method to improve trustworthiness. The method uses LoRA fine-tuning with only a few hundred examples and trains in under 10 minutes on an M3 Ultra. Activation patching experiments show a correlation of ρ=0.976 between swapped hidden states at confidence positions and expressed confidence, confirming causality.

reddit · r/MachineLearning · /u/Synthium- · May 29, 05:15

**Background**: Large language models often suffer from poor calibration: they can internally detect whether they know an answer (probe AUROC up to 0.88), but their verbalized confidence is stuck at nearly 100% for all responses. Probe-targeted fine-tuning leverages this internal signal by using the probe's output as training targets for the model's own confidence output. Activation patching is a technique that swaps model activations between runs to test whether specific activations causally influence outputs.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AUROC">AUROC</a></li>
<li><a href="https://mbrenndoerfer.com/writing/activation-patching">Activation Patching : Causal Tracing in Neural Networks - Interactive</a></li>
<li><a href="https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)">Fine - tuning (deep learning) - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#confidence calibration`, `#fine-tuning`, `#probe`, `#LoRA`

---

<a id="item-3"></a>
## [Hacker finds critical flaws in CBSE online exam grading system](https://ni5arga.com/blog/posts/hacking-cbse/) ⭐️ 9.0/10

A researcher disclosed multiple critical security vulnerabilities in India's CBSE online exam grading system, including hardcoded master passwords, client-side OTP validation, and SQL injection, potentially allowing grade manipulation. These vulnerabilities affect a high-stakes national examination system used by millions of students, and if exploited, could allow unauthorized grade changes, undermining the integrity of the entire examination process. The researcher found that the system used a hardcoded master password, validated OTPs entirely on the client side, allowed bypassing login pages, and had an SQL injection vulnerability; he reported to CERT-In in February 2026 but CBSE initially denied the flaws.

telegram · zaihuapd · May 29, 05:52

**Background**: A hardcoded password is a fixed credential embedded in source code that attackers can easily extract and use to bypass authentication. Client-side OTP validation means the one-time password is verified in the user's browser, which can be bypassed using browser dev tools. SQL injection allows an attacker to execute arbitrary SQL commands on the database, potentially reading or modifying sensitive data.

<details><summary>References</summary>
<ul>
<li><a href="https://www.bleepingcomputer.com/news/security/hardcoded-password-found-in-cisco-software/">Hardcoded Password Found in Cisco Software</a></li>
<li><a href="https://security.stackexchange.com/questions/276635/what-security-risks-do-you-see-with-wrong-otps-appearing-in-application-logs">logging - What security risks do you see with wrong OTPs</a></li>
<li><a href="https://en.wikipedia.org/wiki/SQL_injection">SQL injection - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#security vulnerability`, `#CBSE`, `#online exam system`, `#India`, `#cybersecurity`

---

<a id="item-4"></a>
## [California Assembly Passes 'Protect Our Games Act'](https://www.invenglobal.com/articles/22330/stop-killing-games-movement-gains-momentum-california-assembly-passes-game-protection-bill) ⭐️ 8.0/10

The California State Assembly has passed the 'Protect Our Games Act', a bill that requires game publishers to keep digitally sold games functional or face penalties. The bill now moves to the State Senate for consideration. This legislation is a significant step for digital consumer rights and game preservation, potentially setting a precedent for other states and countries. It would force publishers to ensure that games remain playable even after server shutdowns, addressing a long-standing issue in the gaming industry. The bill excludes games provided via subscription services, free-to-play games, and games that are inherently playable offline indefinitely. It also prohibits the continued sale or distribution of games that have become unusable due to service termination.

hackernews · TechTechTech · May 29, 19:55 · [Discussion](https://news.ycombinator.com/item?id=48328365)

**Background**: Many modern games incorporate always-online DRM or require persistent server connections to function, even for single-player modes. When publishers decide to shut down these servers, the games become unplayable, leaving consumers with non-functional purchases. The Protect Our Games Act aims to require publishers to release patches or provide alternative means to keep games functional, such as removing server checks, thereby preserving consumer access.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Always-on_DRM">Always - on DRM - Wikipedia</a></li>
<li><a href="https://www.howtogeek.com/think-denuvo-is-bad-be-glad-we-dont-have-these-old-drm-solutions/">Think Denuvo Is Bad? Be Glad We Don't Have These 3 DRM Solutions...</a></li>

</ul>
</details>

**Discussion**: Commenters are generally supportive of the bill, but they raise concerns about potential loopholes such as publishers creating shell companies to avoid liability. Some worry that the exemptions for subscription and free-to-play games could incentivize a shift toward those models, while others wish the bill covered subscription games as well to ensure broader preservation.

**Tags**: `#gaming`, `#legislation`, `#consumer rights`, `#digital preservation`

---

<a id="item-5"></a>
## [Is AI repeating frontend's 'lost decade'?](https://mastrojs.github.io/blog/2026-05-23-is-AI-causing-a-repeat-of-frontends-lost-decade/) ⭐️ 8.0/10

A blog post argues that AI tools are causing a decline in frontend expertise and code quality, reminiscent of the 'lost decade' when frameworks like jQuery and React abstracted away fundamental web skills. This debate matters because it highlights a critical tension between AI-driven productivity gains and the erosion of deep frontend craftsmanship, potentially affecting web accessibility, performance, and overall software quality. The post references a past era where developers lost low-level skills to framework abstractions, and now AI code generation may accelerate that trend. Community comments counter that earlier shifts were largely beneficial and that AI similarly reduces accidental complexity.

hackernews · xyzal · May 29, 11:09 · [Discussion](https://news.ycombinator.com/item?id=48321631)

**Background**: The 'lost decade' in frontend development refers to the late 2000s when jQuery and then React, Vue, and Angular abstracted away direct DOM manipulation, leading to a generation of developers less familiar with vanilla HTML, CSS, and JavaScript. This pattern is now repeating with AI code assistants that generate entire components, further distancing developers from foundational knowledge.

<details><summary>References</summary>
<ul>
<li><a href="https://mastrojs.github.io/blog/2026-05-23-is-AI-causing-a-repeat-of-frontends-lost-decade/">Is AI causing a repeat of Frontend ’s Lost Decade ? | Mastro Blog</a></li>
<li><a href="https://en.m.wikipedia.org/wiki/Front-end_web_development">Front-end web development - Wikipedia</a></li>
<li><a href="https://aiespionage.net/tech-deep-dives/is-ai-causing-a-repeat-of-front-end-s-lost-decade/">Is AI causing a repeat of Front end 's Lost Decade ? - AI Espionage</a></li>

</ul>
</details>

**Discussion**: Comments show mixed sentiment: some agree that AI is lowering quality, while others argue that the previous era's 'expertise' was often dealing with unnecessary complexity. Several commenters note that the past industry was not filled with skilled artisans, and that tradeoffs are acceptable as long as more people can build things.

**Tags**: `#AI`, `#frontend development`, `#software engineering`, `#quality`, `#community debate`

---

<a id="item-6"></a>
## [Anthropic run-rate revenue reaches $47 billion](https://simonwillison.net/2026/May/29/anthropic/#atom-everything) ⭐️ 8.0/10

Anthropic disclosed in its $65 billion Series H funding announcement that its run-rate revenue crossed $47 billion earlier in May 2026, up from $9 billion at the end of 2025. This rapid revenue growth—from $9B to $47B in under six months—demonstrates extraordinary enterprise adoption of AI, positioning Anthropic as one of the fastest-scaling companies in any industry and surpassing OpenAI in valuation. The run-rate is an annualized projection based on the most recent month's revenue multiplied by 12, not to be confused with annual recurring revenue (ARR). Previous milestones include $14B in February 2026 and $30B in April 2026.

rss · Simon Willison · May 29, 01:23

**Background**: Run-rate revenue is a common metric for fast-growing startups, calculated by extrapolating recent monthly revenue to a full year. It gives a forward-looking estimate but can be volatile. Anthropic, the developer of the Claude AI model family, has been raising large funding rounds to scale compute, model training, and commercial expansion.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Revenue">Revenue - Wikipedia</a></li>
<li><a href="https://www.investopedia.com/terms/r/runrate.asp">investopedia.com/terms/r/runrate.asp</a></li>

</ul>
</details>

**Tags**: `#Anthropic`, `#AI industry`, `#revenue`, `#funding`, `#business milestone`

---

<a id="item-7"></a>
## [Loadable Crypto Module Proposed for FIPS Certification](https://lwn.net/Articles/1073759/) ⭐️ 8.0/10

A patch series by Amazon engineer Jay Wang proposes decoupling the Linux kernel crypto subsystem into a standalone loadable module, enabling a FIPS-certified module to be reused across multiple kernel versions without requiring full recertification. This proposal addresses a major pain point for organizations requiring FIPS compliance, as kernel updates currently invalidate certification and force lengthy recertification cycles, reducing the cost and delay of maintaining FIPS-certified Linux deployments. The proposal must overcome three obstacles: the build system cannot easily collect built-in objects into a module, the kernel's one-way symbol resolution prevents modules from exporting symbols to the main kernel, and the crypto subsystem must be available early in boot before the root filesystem is mounted.

rss · LWN.net · May 29, 14:29

**Background**: FIPS (Federal Information Processing Standards) 140-3 certification is a rigorous validation process for cryptographic modules required by US government agencies and regulated industries. The certification is tied to the exact binary, so any kernel change invalidates it. Currently, Linux crypto is built into the main kernel, causing lengthy recertification after every update. This proposal aims to isolate the crypto code into a loadable module that can be certified once and reused across kernel versions.

<details><summary>References</summary>
<ul>
<li><a href="https://www.corsec.com/fips-certification-process/">FIPS Certification Process - Corsec Security, Inc.</a></li>
<li><a href="https://ordr.net/blog/ordr-and-fips-certification">FIPS Certification and Why Its Important for the Public Sector - ORDR</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#crypto`, `#FIPS`, `#kernel modules`, `#security`

---

<a id="item-8"></a>
## [Protestware targets AI coding agents via jqwik library](https://lwn.net/Articles/1075315/) ⭐️ 8.0/10

On May 25, 2026, the jqwik property-based testing library version 1.10.0 was released with code that instructs AI coding agents to delete jqwik tests and source code, marking a novel protestware attack that evades traditional security scanners. This incident highlights a new class of supply-chain attack specifically targeting AI-assisted development workflows, where malicious instructions embedded in plain text can bypass current software composition analysis tools. It raises urgent concerns about trust in AI coding agents and the need for new detection mechanisms. The attack uses a simple System.out.print statement of 68 bytes of ASCII, making it invisible to scanners that look for install hooks, network calls, or filesystem writes. The change was committed and released by the legitimate maintainer through the normal build process, so it passes SLSA provenance checks.

rss · LWN.net · May 29, 14:09

**Background**: jqwik is a Java library for property-based testing, which automatically generates test cases based on properties the code should satisfy. Protestware refers to software that protests against a policy or action, often by introducing harmful behavior into the supply chain. Traditional supply-chain security tools focus on detecting network calls, file writes, or obfuscated code, but they are not designed to catch instructions embedded in plain ASCII text that target AI agents.

<details><summary>References</summary>
<ul>
<li><a href="https://jqwik.net/">jqwik : Property - Based Testing in Java</a></li>
<li><a href="https://socket.dev/blog/a-short-history-of-protestware">A Short History of Protestware - Socket</a></li>
<li><a href="https://www.baeldung.com/java-jqwik-property-based-testing">Property - Based Testing with jqwik | Baeldung</a></li>

</ul>
</details>

**Tags**: `#supply-chain security`, `#AI agents`, `#protestware`, `#Java`, `#vulnerability`

---

<a id="item-9"></a>
## [Monokernel achieves 3,300 tokens/s on AMD MI300X](https://www.reddit.com/r/MachineLearning/comments/1tqvuz9/building_a_monokernel_for_llm_inference_on_amd/) ⭐️ 8.0/10

Researchers built a monokernel that runs the entire LLM decode sequence as a single GPU program on AMD MI300X, achieving up to 3,300 output tokens per second per request without speculative decoding or quantization. This demonstrates that optimizing for hardware topology can dramatically reduce LLM inference latency on AMD GPUs, potentially closing the gap with NVIDIA H100 in low-latency serving. The work currently runs on a small 2B parameter coding model with batch size 1 on 8x MI300X GPUs, and the authors plan to extend it to large frontier mixture-of-experts (MoE) models.

reddit · r/MachineLearning · /u/averne_ · May 29, 08:54

**Background**: A monokernel is a single GPU kernel that fuses all operations of a model's forward pass, reducing launch overhead and improving memory efficiency. The AMD MI300X GPU has a unique chiplet architecture with I/O dies (IODs) that connect compute units; mapping memory access patterns to the physical die layout is key to achieving peak performance.

<details><summary>References</summary>
<ul>
<li><a href="https://rocm.docs.amd.com/en/develop/how-to/programming_guide.html">Programming guide — ROCm Documentation</a></li>
<li><a href="https://hazyresearch.stanford.edu/blog/2025-05-27-no-bubbles">Look Ma, No Bubbles! Designing a Low-Latency Megakernel for...</a></li>

</ul>
</details>

**Tags**: `#LLM inference`, `#GPU optimization`, `#AMD MI300X`, `#monokernel`, `#deep learning systems`

---

<a id="item-10"></a>
## [Qwen3.6-27B Quantization Benchmark by User](https://www.reddit.com/r/LocalLLaMA/comments/1tr9vzn/qwen3627b_quantization_benchmark/) ⭐️ 8.0/10

A user benchmarked multiple quantizations of the Qwen3.6-27B model using Kullback-Leibler Divergence (KLD) and Same Top P metrics, comparing Unsloth, mradermacher, and other quantized versions from Q8 down to Q2. This benchmark provides practical guidance for practitioners deploying Qwen3.6-27B locally, helping them choose quantization levels with optimal quality-VRAM trade-offs based on objective metrics rather than anecdotal reports. The tests used llama.cpp's llama-perplexity with a context length of 8192 tokens and KV cache quantized to q8_0 to fit the model in GPU. Results show Unsloth's Q4_K_XL offers a good quality compromise, while mradermacher's Q6_K outperforms Unsloth's Q6_K in KLD and token selection match.

reddit · r/LocalLLaMA · /u/bobaburger · May 29, 17:53

**Background**: Quantization reduces the precision of a model's weights to lower bit widths (e.g., from FP16 to 4-bit), decreasing memory usage and increasing inference speed at the cost of some accuracy. KLD measures how much the output probability distribution of a quantized model deviates from the original, while Same Top P tracks how often the quantized model chooses the same top token as the base model.

<details><summary>References</summary>
<ul>
<li><a href="https://fireworks.ai/blog/fireworks-quantization">How Fireworks evaluates quantization precisely and interpretably</a></li>
<li><a href="https://cosmo-edge.com/unsloth-dynamic-20-ggufs-llm-quantization/">Unsloth Dynamic 2.0 GGUFs: the new benchmark for LLM</a></li>
<li><a href="https://github.com/ssfdre38/gemma4-turbo">GitHub - ssfdre38/gemma4-turbo: IQ 4 _ XS quantization of Gemma...</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#quantization`, `#benchmark`, `#Qwen`, `#local LLM`

---

<a id="item-11"></a>
## [Multi-Token Prediction speeds up inference up to 3.34x](https://www.reddit.com/r/LocalLLaMA/comments/1trf0r0/i_tested_mtp_on_vllm_and_llamacpp_for_gemma_4/) ⭐️ 8.0/10

A Reddit user benchmarked Multi-Token Prediction (MTP) on Gemma 4 31B and Qwen 3.6 27B using vLLM and llama.cpp, achieving up to 132.52 tok/s (3.34x faster) on an RTX PRO 6000 Blackwell GPU. MTP is a speculative decoding technique that dramatically improves inference throughput without significant quality loss, making large dense models more practical for real-time applications and local deployment. The best result was vLLM with Gemma 4 at n=5 speculative tokens achieving 132.52 tok/s vs 39.69 tok/s baseline; llama.cpp with Qwen 3.6 peaked at 117.70 tok/s with n=3. The draft model is tiny (76M parameters for Gemma 4) and VRAM overhead appeared negligible.

reddit · r/LocalLLaMA · /u/FantasticNature7590 · May 29, 20:42

**Background**: Multi-Token Prediction (MTP) is a speculative decoding technique where a lightweight draft model predicts multiple future tokens, and the target model verifies them in a single forward pass. This amortizes memory bandwidth costs and speeds up autoregressive decoding. vLLM and llama.cpp are popular open-source inference engines that have recently added MTP support. GGUF is a quantization format for efficient local deployment.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/@bnjmn_marie/gguf-quantization-for-fast-and-memory-efficient-inference-on-your-cpu-d10fbe58fbca">GGUF Quantization for Fast and Memory-Efficient Inference... | Medium</a></li>
<li><a href="https://ggufloader.github.io/what-is-gguf.html">What is GGUF ? Complete Guide to GGUF Format & Quantization</a></li>

</ul>
</details>

**Tags**: `#Multi-Token Prediction`, `#vLLM`, `#llama.cpp`, `#LLM inference`, `#benchmarking`

---

<a id="item-12"></a>
## [Nvidia teases N1X laptop chip with 20 ARM cores, 6144 CUDA cores for Computex](https://www.reddit.com/r/LocalLLaMA/comments/1tracb5/nvidia_teases_new_pc_laptop_chip_to_be_announced/) ⭐️ 8.0/10

Nvidia has teased a new ARM-based laptop processor, the N1X, featuring 20 ARM cores and 6144 CUDA cores based on the Blackwell architecture. The chip is expected to be officially announced at Computex on June 2, 2026, and is essentially a lower-power version of the DGX Spark superchip. This marks Nvidia's major push into the PC laptop market with its own ARM CPU, potentially challenging AMD's Strix Halo and Qualcomm's Snapdragon X. The chip's high CUDA core count could make it exceptionally powerful for local LLM inference on laptops. The N1X is expected to be a variant of the GB10 Grace Blackwell Superchip used in the DGX Spark, but optimized for lower-power laptop systems. Early leaks suggest a heterogeneous 'big-little' architecture and support for up to 128GB of unified memory, though software support and pricing remain key concerns.

reddit · r/LocalLLaMA · /u/Terminator857 · May 29, 18:07

**Background**: Nvidia has traditionally focused on discrete GPUs for gaming and professional use, while leaving CPU design to partners like Intel and AMD. The N1X represents Nvidia's first serious attempt at creating its own Arm-based CPU for laptops, developed in collaboration with MediaTek. This follows similar efforts by Apple with its M-series chips and Qualcomm with the Snapdragon X series. The DGX Spark is a desktop AI supercomputer priced around $4,700, aimed at developers and researchers.

<details><summary>References</summary>
<ul>
<li><a href="https://www.tomsguide.com/computing/cpus/nvidia-n1x-cpu-everything-we-know-so-far">Nvidia N1X and N1 CPU: Everything we know so far - Tom's Guide</a></li>
<li><a href="https://www.digitalfoundry.net/news/2026/04/nvidia-is-making-laptops-now-n1n1x-leak-shows-a-128gb-monster-derived-from-their-dgx-spark-desktop-ai-workhorse">Nvidia Is Making Laptops Now: N1/ N1X Leak Shows a 128GB Monster...</a></li>
<li><a href="https://www.notebookcheck.net/Nvidia-N1X-leak-points-to-limited-2026-availability.1282855.0.html">Nvidia N1X leak points to limited 2026 availability</a></li>

</ul>
</details>

**Discussion**: Reddit commenters are excited about the hardware specs but remain skeptical about software support, especially for Windows on ARM and gaming compatibility. Many note that Nvidia must address the poor market reception of previous ARM laptop efforts by Microsoft and Qualcomm. Pricing is a major point of discussion, with hopes that the N1X laptops will be significantly cheaper than the $4,700 DGX Spark.

**Tags**: `#Nvidia`, `#ARM`, `#Laptop Chip`, `#LLM`, `#Computex`

---

<a id="item-13"></a>
## [StepFun Releases Step 3.7 Flash, a 196B MoE Model](https://www.reddit.com/r/LocalLLaMA/comments/1tqloii/stepfun_37_flash/) ⭐️ 8.0/10

StepFun has released Step 3.7 Flash, a multimodal Mixture-of-Experts model with 196B total parameters (11B active), capable of running locally on 128GB RAM and achieving strong benchmark results on coding and agentic tasks. This model provides a compelling local deployment option that rivals larger models on agentic and coding benchmarks, which is particularly relevant for the local LLM community and agent workflow development. The model includes a built-in 1.8B ViT for vision, and its benchmarks include SWE-Bench Pro 56.26% (beating DeepSeek V4 Flash and matching Gemini 3.5 Flash), DeepSearchQA F1 92.82%, and HLE with tools 47.2%. It is available on OpenRouter and NVIDIA NIM for those who prefer not to self-host.

reddit · r/LocalLLaMA · /u/Everlier · May 29, 00:32

**Background**: MoE (Mixture of Experts) models activate only a subset of parameters per token, enabling large total capacity with lower computational cost. SWE-Bench Pro is a challenging benchmark for real-world software engineering tasks, and DeepSearchQA evaluates multi-step information-seeking ability. StepFun is a Chinese AI company focused on developing efficient large language models.

<details><summary>References</summary>
<ul>
<li><a href="https://scaleapi.github.io/SWE-bench_Pro-os/">SWE-Bench Pro</a></li>
<li><a href="https://huggingface.co/datasets/google/deepsearchqa">google/ deepsearchqa · Datasets at Hugging Face</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#MoE`, `#Local LLM`, `#Multimodal`, `#Model Release`

---

<a id="item-14"></a>
## [BYD offers one-year accident liability coverage for city NOA](https://news.mydrivers.com/1/1125/1125729.htm) ⭐️ 8.0/10

BYD announced that it will provide one-year accident liability coverage for its City Navigation Assisted Driving (city NOA) system, covering all economic losses for the vehicle involved in accidents caused by assisted driving, with no upper limit. This policy could set a precedent in the automotive industry, boosting consumer confidence in assisted driving technology and potentially accelerating adoption of autonomous driving features. The coverage applies to new car buyers of DiPilot A and B systems for one year from delivery, and also to existing owners who upgrade to DiPilot 5.0. The DiPilot C system is priced at 12,000 yuan for new car selection.

telegram · zaihuapd · May 29, 01:03

**Background**: City Navigation Assisted Driving (city NOA) is an advanced driver-assistance system that enables autonomous navigation on urban roads, including lane changes, turns, and traffic light response. BYD's DiPilot (Tianshen Zhiyan) is its suite of assisted driving systems, with variants A, B, and C offering different levels of capability. Liability for accidents during assisted driving has been a key concern for consumers and regulators.

<details><summary>References</summary>
<ul>
<li><a href="https://ee.ofweek.com/2026-05/ART-8110-2801-30688887.html">智 驾 竞赛比亚迪丢王炸：兜底 城 市 NOA... - OFweek电子工程网</a></li>
<li><a href="https://aikahao.xcar.com.cn/video/3782133.html">aikahao.xcar.com.cn/video/3782133.html</a></li>

</ul>
</details>

**Tags**: `#Autonomous driving`, `#Automotive`, `#BYD`, `#Assisted driving`, `#Liability`

---

<a id="item-15"></a>
## [China Certifies Nine Domestic AI Chips for Gov Procurement](https://www.tomshardware.com/tech-industry/semiconductors/china-certifies-nine-domestic-ai-chips-for-government-procurement) ⭐️ 8.0/10

China's Information Security Evaluation Center for the first time added an 'AI training and inference chip' category to its security certification framework, certifying nine domestic AI processors for government procurement. The certified chips include products from Huawei (Ascend), Alibaba (Pingtouge Zhenwu), Biren Technology, and Hygon, while Cambricon and Baidu's Kunlun Core were not listed. This marks a significant policy shift by officially endorsing domestic AI chips for government use, potentially accelerating the replacement of foreign chips (like NVIDIA) in China's public sector and boosting the domestic AI hardware ecosystem. The certification is valid for three years and serves as the procurement basis for government agencies and state-owned enterprises. The nine chips cover a range of AI acceleration capabilities, but specific performance benchmarks were not disclosed.

telegram · zaihuapd · May 29, 08:41

**Background**: The 'Anke' security procurement catalog is a list of approved hardware and software for Chinese government use, focusing on information security and self-reliance. Previously, it mainly covered CPUs and other components; this is the first time AI accelerators have been included. Huawei's Ascend series, for example, is designed for AI training and inference using a proprietary architecture.

<details><summary>References</summary>
<ul>
<li><a href="https://www.bbc.com/zhongwen/articles/cgrp5krzp8qo/simp">bbc.com/zhongwen/articles/cgrp5krzp8qo/simp</a></li>
<li><a href="https://m.ebrun.com/669634.html">“死磕”鲲鹏 昇 腾 生态的极客们 要搞点大事情 - AI - 亿邦动力</a></li>

</ul>
</details>

**Tags**: `#AI chips`, `#China`, `#government procurement`, `#security certification`, `#technology policy`

---

<a id="item-16"></a>
## [Blue Origin's New Glenn Rocket Explodes in Static Fire Test](https://arstechnica.com/space/2026/05/blue-origins-new-glenn-rocket-just-exploded-during-a-static-fire-test/) ⭐️ 8.0/10

On May 28, 2026, Blue Origin's New Glenn rocket exploded during a static fire test at Cape Canaveral, destroying the vehicle and damaging launch infrastructure, with no injuries reported. This explosion severely delays Blue Origin's launch schedule and impacts NASA's Artemis lunar landing plans, as Blue Origin is contracted for lander and rover deliveries, and also disrupts Amazon's Project Kuiper satellite deployment. The explosion occurred during a static fire test of seven BE-4 methane engines on the first stage; the vehicle was lost and the launch pad's lightning protection tower collapsed. The NG-4 mission was to launch 48 Project Kuiper satellites.

telegram · zaihuapd · May 29, 11:08

**Background**: New Glenn is Blue Origin's heavy-lift reusable rocket powered by seven BE-4 engines burning liquid methane and oxygen. Static fire tests are routine pre-launch checks where engines are briefly ignited while the rocket is held down. This explosion is a major setback for Blue Origin, which has yet to achieve orbital flight with New Glenn.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/BE-4">BE-4 - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Project_Kuiper">Project Kuiper</a></li>

</ul>
</details>

**Tags**: `#space`, `#Blue Origin`, `#New Glenn`, `#NASA`, `#rocket explosion`

---