---
layout: default
title: "Horizon Summary: 2026-06-07 (EN)"
date: 2026-06-07
lang: en
---

> From 45 items, 15 important content pieces were selected

---

1. [First Invasive BCI Restores Vision to Patient Blind for 20 Years](#item-1) ⭐️ 9.0/10
2. [Meta confirms AI chatbot bug led to Instagram account hacks](#item-2) ⭐️ 8.0/10
3. [Moving beyond fork() + exec()](#item-3) ⭐️ 8.0/10
4. [Zeroserve: A zero-config web server with eBPF scripting](#item-4) ⭐️ 8.0/10
5. [Nvidia Proposes High-Performance CPU for Windows PCs](#item-5) ⭐️ 8.0/10
6. [HN User Questions Anti-AI Sentiment in Community](#item-6) ⭐️ 8.0/10
7. [MicroPython compiled to WebAssembly for Python sandboxing](#item-7) ⭐️ 8.0/10
8. [Cohere Offers Early Access to Unreleased Coding Model with Efficient Architecture](#item-8) ⭐️ 8.0/10
9. [1-Click Admin Takeover Flaw Found in PewDiePie's Odysseus AI Tool](#item-9) ⭐️ 8.0/10
10. [120 tok/s on 12GB VRAM with Gemma 4 12B QAT MTP](#item-10) ⭐️ 8.0/10
11. [KVarN KV Cache Quant Achieves Higher-Bit Precision at Lower Memory](#item-11) ⭐️ 8.0/10
12. [Custom CUDA/C++ Inference Engine for NVIDIA's DVLT 3D Transformer](#item-12) ⭐️ 8.0/10
13. [DeepSeek V4 Flash Support in llama.cpp WIP PR Shows Promise](#item-13) ⭐️ 8.0/10
14. [MoQ and GSQ: Boosting Low-Bit GGUF Quantization](#item-14) ⭐️ 8.0/10
15. [Gemma 4 QAT Benchmarks on Strix Halo APU](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [First Invasive BCI Restores Vision to Patient Blind for 20 Years](https://www.ithome.com/0/960/883.htm) ⭐️ 9.0/10

Chinese surgeons at Xiangya Hospital successfully implanted the IMIE intelligent retinal system into a 61-year-old patient blind for 20 years due to retinitis pigmentosa, enabling her to discern objects and navigate doorways with restored vision of 0.03. This marks China's first successful clinical trial of an invasive BCI for vision restoration, using a 256-channel flexible electrode array with four times the channel count of foreign counterparts, demonstrating significant progress in neural engineering and medical technology. The IMIE system uses an external camera to capture images, which are processed into electrical signals that directly stimulate the optic nerve, bypassing damaged photoreceptors. The patient continues to undergo rehabilitation training to improve visual perception.

telegram · zaihuapd · Jun 6, 07:30

**Background**: Invasive brain-computer interfaces (BCIs) involve surgically implanting electrodes into the brain or nervous system to directly interact with neural circuits. The IMIE (Intelligent Medical Implant for Eye) system is a type of retinal prosthesis that electrically stimulates the optic nerve. The 256-channel flexible electrode array used in this trial is thinner and more biocompatible, allowing for higher resolution stimulation. Similar developments in flexible electrode technology, such as Tsinghua University's 9-micron-thick organic flexible electrode array, are advancing the field.

<details><summary>References</summary>
<ul>
<li><a href="https://www.ithome.com/0/960/883.htm">全国首例：侵入式脑机接口让失明 20 年患者重见光明 - IT之家</a></li>
<li><a href="https://sputniknews.cn/20260606/1071733984.html">中国首例！ 盲人凭脑机接口复明成功 - 2026年6月6日, 俄罗斯卫星通讯社</a></li>
<li><a href="https://www.tsinghua.edu.cn/info/1182/126137.htm">厚度仅9微米！清华打造脑机接口超柔性“神经纽带”-清华大学</a></li>

</ul>
</details>

**Tags**: `#脑机接口`, `#医疗科技`, `#神经工程`, `#生物医学工程`, `#侵入式BCI`

---

<a id="item-2"></a>
## [Meta confirms AI chatbot bug led to Instagram account hacks](https://this.weekinsecurity.com/meta-confirms-thousands-of-instagram-accounts-were-hacked-by-abusing-its-ai-chatbot/) ⭐️ 8.0/10

Meta confirmed that attackers exploited a bug in its AI chatbot's account recovery process to bypass email verification and hijack thousands of Instagram accounts, beginning around April 17 and lasting for several weeks. This incident underscores critical security risks in AI-powered customer support and account recovery systems, affecting over 20,000 users and potentially eroding trust in Meta's platform security. The hackers gained full control of hijacked accounts, including access to direct messages, posts, and linked accounts. Meta notified at least 20,225 affected individuals, and the vulnerability existed from April 17 until it was fixed.

hackernews · speckx · Jun 6, 18:35 · [Discussion](https://news.ycombinator.com/item?id=48427643)

**Background**: AI chatbots are increasingly used by companies like Meta for automated account recovery to streamline user support. However, this incident shows that when identity verification mechanisms are flawed, these AI systems can be manipulated to bypass security checks, enabling account takeovers without proper authorization.

<details><summary>References</summary>
<ul>
<li><a href="https://cybersecuritynews.com/instagram-meta-ai-vulnerability/">Instagram Meta AI Vulnerability Allegedly Enables Password ...</a></li>
<li><a href="https://blog.checkpoint.com/ai-security/the-meta-ai-account-recovery-incident-wasnt-just-a-chatbot-problem/">The Meta AI Account Recovery Incident Wasn’t Just a Chatbot ...</a></li>

</ul>
</details>

**Discussion**: Commenters criticized Meta's description that the tool 'worked properly,' arguing the bug represents a severe security failure. Some expressed frustration with Meta's automated systems while others hope this incident accelerates the decline of Meta's platforms.

**Tags**: `#security`, `#Instagram`, `#AI chatbot`, `#account hijacking`, `#Meta`

---

<a id="item-3"></a>
## [Moving beyond fork() + exec()](https://lwn.net/SubscriberLink/1076018/16f01bbbb8e0d1f0/) ⭐️ 8.0/10

The article discusses the historical rationale for Unix's fork()+exec() process creation model and argues that it is now outdated, proposing alternatives like posix_spawn and vfork. This matters because fork()+exec() is a fundamental OS primitive; rethinking it could simplify systems programming and improve performance, affecting many applications and developers. Key details include the overhead of fork() even with copy-on-write, and that posix_spawn provides a combined process creation and execution call that avoids unnecessary copying.

hackernews · jwilk · Jun 6, 14:34 · [Discussion](https://news.ycombinator.com/item?id=48425528)

**Background**: In Unix, fork() creates a child process that is an almost exact copy of the parent, while exec() replaces the child's memory with a new program. This two-step process was elegant for its time but incurs overhead. Alternatives like vfork() (which suspends the parent) and posix_spawn() (a combined call) exist but are less used. The debate is about whether the elegance justifies the performance cost.

<details><summary>References</summary>
<ul>
<li><a href="https://www.man7.org/linux/man-pages/man3/posix_spawn.3.html">posix_spawn(3) - Linux manual page</a></li>
<li><a href="https://en.wikipedia.org/wiki/Fork_(system_call)">Fork (system call) - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Comments highlight both sides: some argue fork()+exec() is elegant and extensible, while others lament its complexity and performance issues, citing personal bug experiences. There is reference to a Microsoft Research paper "A fork() in the road" that criticizes fork.

**Tags**: `#systems programming`, `#unix`, `#process creation`, `#fork`, `#exec`

---

<a id="item-4"></a>
## [Zeroserve: A zero-config web server with eBPF scripting](https://su3.io/posts/introducing-zeroserve) ⭐️ 8.0/10

Zeroserve is introduced as a zero-configuration web server that uses eBPF for scripting, offering an alternative to traditional servers like nginx and Caddy. It is built in Rust and allows users to write eBPF programs in C to handle HTTP requests. This approach shifts web server configuration from declarative languages to programmable eBPF, enabling high-performance, flexible request handling. It could simplify deployment and open new possibilities for low-latency web serving, though it may have a steeper learning curve. Zeroserve is single-threaded and focuses on static file serving, with community suggestions to explore multi-threading via SO_REUSEPORT and integration with other eBPF program types like XDP. The project's design bet is on configuration paradigm rather than performance alone.

hackernews · losfair · Jun 6, 14:59 · [Discussion](https://news.ycombinator.com/item?id=48425723)

**Background**: eBPF (extended Berkeley Packet Filter) is a Linux kernel technology that allows running sandboxed programs in kernel space, traditionally used for networking, observability, and security. Web servers like nginx and Caddy use declarative config files, whereas Zeroserve uses eBPF programs (written in C) to define request handling logic, potentially allowing direct kernel interaction for performance gains.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/EBPF">eBPF - Wikipedia</a></li>
<li><a href="https://ebpf.io/what-is-ebpf/">What is eBPF? An Introduction and Deep Dive into the eBPF ...</a></li>

</ul>
</details>

**Discussion**: Commenters expressed interest in the concept, with some noting the missed opportunity for a Rust-based eBPF script interface. Others highlighted the impressive performance of nginx and questioned the focus on static files given modern trends. There was also discussion about the potential for kernel-accelerated web serving using eBPF, though the current implementation is userspace.

**Tags**: `#eBPF`, `#web server`, `#zero-config`, `#Rust`, `#networking`

---

<a id="item-5"></a>
## [Nvidia Proposes High-Performance CPU for Windows PCs](https://twitter.com/lemire/status/2062880075117113739) ⭐️ 8.0/10

Nvidia has proposed a powerful CPU system for Windows PCs that leverages unified memory architecture, potentially integrating high-performance Arm-based cores with its GPU technology for local AI workloads. This proposal could redefine PC architecture by bringing unified memory to Windows, similar to Apple Silicon, enabling more efficient local AI processing and potentially challenging Intel and AMD in the CPU market. The system reportedly shares a unified memory pool between CPU and GPU, similar to Nvidia's Grace CPU for data centers, but optimized for consumer Windows PCs with a focus on local AI inference.

hackernews · tosh · Jun 6, 12:52 · [Discussion](https://news.ycombinator.com/item?id=48424605)

**Background**: Unified memory architecture allows CPU and GPU to access the same memory pool without copying data, reducing latency and simplifying programming. Nvidia has previously developed the Arm-based Grace CPU for servers, and this proposal adapts similar technology for consumer PCs to enable seamless local AI execution.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Unified_memory_architecture">Unified memory architecture</a></li>
<li><a href="https://grokipedia.com/page/Nvidia_Grace">Nvidia Grace</a></li>
<li><a href="https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/unified-memory.html">4.1. Unified Memory — CUDA Programming Guide</a></li>

</ul>
</details>

**Discussion**: Commenters debated the benefits of unified memory for gaming and AI, with some questioning performance claims and comparing to existing solutions like AMD Ryzen AI Max and Qualcomm Snapdragon X2. Others expressed skepticism about the niche appeal of local AI for average consumers.

**Tags**: `#Nvidia`, `#CPU`, `#Windows`, `#AI`, `#Unified Memory`

---

<a id="item-6"></a>
## [HN User Questions Anti-AI Sentiment in Community](https://news.ycombinator.com/item?id=48420827) ⭐️ 8.0/10

A Hacker News user questioned the perceived anti-AI sentiment on the platform, sparking a discussion with over 600 comments including moderator dang's observation that the community is divided on AI. This discussion highlights the ongoing tension in the software industry between AI-assisted development and traditional coding, which influences tool adoption and community dynamics on influential tech forums. The original poster argues that code is a means to an end and that AI-assisted versions can ship faster; comments range from fears about job loss to concerns about proprietary non-deterministic databases.

hackernews · Ekami · Jun 6, 02:31

**Background**: AI coding assistants like Claude Code and GitHub Copilot use large language models to generate code from natural language prompts. They have sparked debates about code quality, developer productivity, and the future of software engineering. Hacker News, a tech-focused social news site, often hosts polarized discussions on such topics.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>

</ul>
</details>

**Discussion**: The comments reveal a divided community: some defend AI for accelerating development, while others value the craft of coding and fear AI threatens their livelihood. Detractors also raise concerns about proprietary lock-in and non-deterministic outputs. Moderator dang notes that HN is not uniformly anti-AI, but both sides perceive bias.

**Tags**: `#AI`, `#software engineering`, `#Hacker News`, `#meta`, `#community`

---

<a id="item-7"></a>
## [MicroPython compiled to WebAssembly for Python sandboxing](https://simonwillison.net/2026/Jun/6/micropython-in-a-sandbox/#atom-everything) ⭐️ 8.0/10

Simon Willison released an alpha package called micropython-wasm that compiles MicroPython to WebAssembly, allowing Python code to run safely in a sandbox within Python applications like Datasette. He also created a plugin, datasette-agent-micropython, for Datasette Agent to leverage this sandbox. This provides a practical solution for executing untrusted Python code securely, addressing a long-standing challenge for plugin systems and applications. By leveraging WebAssembly's sandboxing properties, it enforces memory and CPU limits, making it suitable for AI agents and other use cases. The package compiles MicroPython using Emscripten to produce a WebAssembly module that runs in an isolated environment, preventing access to the host filesystem, network, or other resources. It is currently alpha software and not recommended for production use.

rss · Simon Willison · Jun 6, 03:53

**Background**: MicroPython is a lean implementation of Python 3 optimized for microcontrollers but can also run on other platforms. WebAssembly (WASM) is a binary instruction format that executes in a virtual machine with built-in sandboxing. Combining them allows running Python in an isolated environment with resource limits.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/MicroPython">MicroPython</a></li>
<li><a href="https://micropython.org/">MicroPython - Python for microcontrollers</a></li>
<li><a href="https://agent.datasette.io/">Datasette Agent: an AI assistant for Datasette to help ...</a></li>

</ul>
</details>

**Tags**: `#sandbox`, `#micropython`, `#webassembly`, `#python`, `#security`

---

<a id="item-8"></a>
## [Cohere Offers Early Access to Unreleased Coding Model with Efficient Architecture](https://www.reddit.com/r/LocalLLaMA/comments/1tylzy2/coheres_unreleased_coding_model_early_access_for/) ⭐️ 8.0/10

Cohere has released an early access version of its first coding model, a 30B parameter model with only 3B active parameters, for community testing on Hugging Face before official launch. This marks Cohere's entry into the coding model space and demonstrates a focus on local deployment efficiency through sparse activation, potentially setting a new standard for developer-friendly AI tools. The model has 30B total parameters but only 3B active, suggesting a Mixture-of-Experts (MoE) architecture that enables fast inference on consumer hardware. Cohere is seeking community feedback to improve the model before its public release.

reddit · r/LocalLLaMA · /u/nick_frosst · Jun 6, 16:36

**Background**: In AI models, parameters are the internal weights learned during training that determine output. A Mixture-of-Experts (MoE) architecture uses multiple specialized sub-networks (experts) and a gating mechanism to activate only a subset for each input, drastically reducing computational cost. For example, a 30B MoE model with 3B active parameters can run on a single GPU, making local deployment feasible.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained - Hugging Face</a></li>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#Cohere`, `#coding model`, `#local LLM`, `#early access`, `#AI`

---

<a id="item-9"></a>
## [1-Click Admin Takeover Flaw Found in PewDiePie's Odysseus AI Tool](https://www.reddit.com/r/LocalLLaMA/comments/1tys1wj/another_1click_admin_account_takeover_in/) ⭐️ 8.0/10

A security researcher disclosed a 1-click admin account takeover vulnerability in PewDiePie's self-hosted AI tool Odysseus, allowing attackers to gain full admin control with a single click. This vulnerability is critical because Odysseus is promoted as a private, self-hosted AI workspace, and a full admin takeover undermines user trust and data security. The recurring nature of such flaws indicates a need for more rigorous security audits in popular AI tools. The vulnerability allows a 1-click admin takeover without user interaction, similar to other recent 1-click account takeover issues in ZITADEL and Microsoft 365 Android apps. No patch has been confirmed at the time of disclosure.

reddit · r/LocalLLaMA · /u/theonejvo · Jun 6, 20:32

**Background**: PewDiePie released Odysseus, a self-hosted AI workspace for running open-source models locally, emphasizing privacy and user control. The tool is built on existing web UIs like Claude and ChatGPT's interfaces, but self-hosted. A 1-click admin takeover vulnerability is a severe security issue that could expose all user data and allow full system control.

<details><summary>References</summary>
<ul>
<li><a href="https://www.tomshardware.com/tech-industry/artificial-intelligence/pewdiepie-goes-all-in-on-self-hosting-ai-using-modded-gpus-with-plans-to-build-own-model-soon-youtuber-pits-multiple-sentient-chatbots-against-each-other-to-find-the-best-answers">PewDiePie goes all-in on self-hosting AI using... | Tom's Hardware</a></li>
<li><a href="https://80.lv/articles/pewdiepie-releases-his-own-self-hosted-ai-workspace-available-for-free">PewDiePie Releases His Own Self-Hosted AI Workspace for Free</a></li>

</ul>
</details>

**Tags**: `#security`, `#vulnerability`, `#AI`, `#LLM`, `#PewDiePie`

---

<a id="item-10"></a>
## [120 tok/s on 12GB VRAM with Gemma 4 12B QAT MTP](https://www.reddit.com/r/LocalLLaMA/comments/1typjmc/120_toks_on_12gb_vram_with_gemma_4_12b_qat_mtp/) ⭐️ 8.0/10

A user achieved 120 tokens per second inference speed on a 12GB NVIDIA RTX 4070 Super GPU using Gemma 4 12B QAT (Quantization-Aware Training) model with Multi-Token Prediction (MTP) speculative decoding via a patched llama.cpp. This demonstrates a remarkable breakthrough in running large language models locally on consumer hardware, making high-speed inference accessible on mid-range GPUs (12GB VRAM) without sacrificing quality, which could accelerate adoption of local LLMs. The setup uses Unsloth's 4-bit quantized GGUF of Gemma 4 12B QAT and a separate Q8_0 quantized draft model for MTP, achieving about 2x speedup over non-MTP inference (from ~60 tok/s to ~120 tok/s). However, it requires the GPU to be set as secondary to free up VRAM, and Windows users may lose ~500MB+ VRAM due to driver overhead.

reddit · r/LocalLLaMA · /u/janvitos · Jun 6, 18:53

**Background**: Quantization-Aware Training (QAT) integrates quantization into the training process, allowing models to adapt to low-precision inference and thus maintain accuracy even after aggressive quantization. Multi-Token Prediction (MTP) is a speculative decoding technique where a lightweight draft head predicts several tokens ahead in parallel, and the main model verifies them, increasing throughput. Gemma 4 is Google's latest open model family, and the QAT variant is specifically designed for efficient inference.

<details><summary>References</summary>
<ul>
<li><a href="https://www.ibm.com/think/topics/quantization-aware-training">What is Quantization Aware Training ? | IBM</a></li>
<li><a href="https://docs.llamatik.com/guides/multi-token-prediction/">Multi - Token Prediction ( MTP ) • Llamatik Documentation</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#quantization`, `#inference speed`, `#Gemma 4`, `#speculative decoding`

---

<a id="item-11"></a>
## [KVarN KV Cache Quant Achieves Higher-Bit Precision at Lower Memory](https://www.reddit.com/r/LocalLLaMA/comments/1tyockn/kv_cache_quant_benchmarks_kvarn_6bit_matches_q8_0/) ⭐️ 8.0/10

KVarN quantization benchmarks show that 6-bit KVarN matches the precision of q8_0, and 4-bit KVarN matches q5_0, enabling significant memory savings without quality loss in LLM inference. This breakthrough allows VRAM-constrained users to run larger contexts or models, as KVarN offers one-bit-higher precision at the same memory cost, potentially democratizing long-context LLM inference on consumer hardware. The benchmarks were conducted on Qwen 3.6 27B with 64k context using a fork of llama.cpp (BeeLlama). Prompt processing is currently slower, but the method is expected to be optimized further.

reddit · r/LocalLLaMA · /u/Anbeeld · Jun 6, 18:06

**Background**: KV cache quantization reduces memory usage by storing keys and values in lower precision. Standard formats like q8_0 use 8-bit, while KVarN uses variance normalization and Hadamard rotation to maintain high quality at lower bit-widths. This research is from Huawei and is implemented in vLLM as well.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/huawei-csl/KVarN">GitHub - huawei-csl/KVarN: KVarN is a native vLLM KV-cache ...</a></li>
<li><a href="https://arxiv.org/pdf/2606.03458">KVarN: Variance-Normalized KV-Cache Quantization Mitigates ...</a></li>
<li><a href="https://insiderllm.com/guides/llm-quantization-explained/">Quantization Explained: What It Means for Local AI | InsiderLLM</a></li>

</ul>
</details>

**Tags**: `#KV cache`, `#quantization`, `#LLM inference`, `#KVarN`, `#llama.cpp`

---

<a id="item-12"></a>
## [Custom CUDA/C++ Inference Engine for NVIDIA's DVLT 3D Transformer](https://www.reddit.com/r/LocalLLaMA/comments/1tyu79c/dvltcu_inference_engine_written_from_scratch_in/) ⭐️ 8.0/10

A developer released dvlt.cu, a lightweight inference engine for NVIDIA's Déjà View (DVLT) 3D transformer model, implemented entirely in CUDA/C++ as a single 5MB binary with minimal dependencies (only cuBLASLt and the CuTe header library from CUTLASS). This demonstrates that a large, sophisticated transformer model can be served with a tiny, dependency-free binary, potentially enabling efficient 3D reconstruction on edge devices or in resource-constrained environments without the overhead of Python or deep learning frameworks. The engine uses mmap'd bf16 weights, bulk GPU upload, static dimensions, and a one-shot arena for deterministic memory allocation; weights (117M parameters) are NVIDIA's non-commercial release fetched separately.

reddit · r/LocalLLaMA · /u/yassa9 · Jun 6, 22:04

**Background**: Déjà View (DVLT) is a recurrent transformer for multi-view 3D reconstruction that loops a shared block of attention with discrete depth indexing, outputting per-pixel rays, depth, confidence, and camera poses from unordered images. With only 117M parameters, it competes with larger models. cuTLASS (CUTLASS) is NVIDIA's CUDA template library for high-performance matrix operations, and its CuTe component provides tensor abstractions.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/nv-tlabs/dvlt">GitHub - nv-tlabs/dvlt: Official implementation of Déjà View ...</a></li>
<li><a href="https://github.com/NVIDIA/cutlass">GitHub - NVIDIA/cutlass: CUDA Templates and Python DSLs for ...</a></li>

</ul>
</details>

**Tags**: `#CUDA`, `#inference engine`, `#3D reconstruction`, `#transformer`, `#HPC`

---

<a id="item-13"></a>
## [DeepSeek V4 Flash Support in llama.cpp WIP PR Shows Promise](https://www.reddit.com/r/LocalLLaMA/comments/1tyb3np/deepseek_v4_flash_is_amazing_wip_llamacpp_pr_24162/) ⭐️ 8.0/10

A work-in-progress pull request (#24162) has added support for DeepSeek V4 Flash to llama.cpp, enabling local inference with custom quantization. DeepSeek V4 Flash is a 284B-parameter MoE model that delivers frontier-level intelligence at a local scale, and this PR brings it to the open-source llama.cpp ecosystem, potentially dominating the 80-140GB model space. The PR is early-stage with slow inference (5-6 tps) and incomplete GPU/Flash Attention support, but the model's native FP4-FP8 hybrid quantization helps it tolerate aggressive quantization better than competitors, and the MoE architecture uses only 13B activated parameters per token.

reddit · r/LocalLLaMA · /u/Lowkey_LokiSN · Jun 6, 07:56

**Background**: DeepSeek V4 Flash is a Mixture-of-Experts (MoE) model with 284B total parameters but only 13B activated per input, supporting a 1M-token context window. It uses a hybrid FP4-FP8 quantization scheme that reduces memory footprint while retaining quality. llama.cpp is a popular open-source library for running LLMs locally on consumer hardware. Quantization, such as the custom 3-bit version mentioned in the post, compresses models to fit within available VRAM.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash">deepseek -ai/ DeepSeek - V 4 - Flash · Hugging Face</a></li>
<li><a href="https://build.nvidia.com/deepseek-ai/deepseek-v4-flash">deepseek - v 4 - flash Model by Deepseek -ai | NVIDIA NIM</a></li>
<li><a href="https://openrouter.ai/deepseek/deepseek-v4-flash:free">DeepSeek V 4 Flash - API Pricing & Benchmarks | OpenRouter</a></li>

</ul>
</details>

**Tags**: `#deepseek`, `#llama.cpp`, `#local-llm`, `#quantization`, `#open-source`

---

<a id="item-14"></a>
## [MoQ and GSQ: Boosting Low-Bit GGUF Quantization](https://www.reddit.com/r/LocalLLaMA/comments/1tyjkfh/moq_ggufs_and_gsq_lowbit_ggufs_are_about_to_get/) ⭐️ 8.0/10

Two new quantization methods, MoQ (Mixture-of-Quantization) and GSQ (Gumbel-Softmax Quantization), are set to significantly improve the performance of low-bit GGUF models, enabling more efficient local LLM deployment. This advancement could make high-quality LLMs more accessible on consumer hardware by reducing memory and computational requirements without sacrificing accuracy, benefiting the local LLM community and edge deployment scenarios. MoQ schedules various data precisions during quantization-aware training, while GSQ is a scalar post-training quantization method that achieves near-lossless compression at 2-bit for trillion-parameter models. Both are designed to be compatible with existing inference frameworks.

reddit · r/LocalLLaMA · /u/beneath_steel_sky · Jun 6, 15:01

**Background**: GGUF is a binary file format for storing machine learning models, optimized for fast loading and inference with GGML. Quantization reduces model precision (e.g., from 16-bit to 4-bit or 2-bit) to lower memory usage and speed up computation, which is crucial for deploying LLMs on devices with limited resources. MoQ and GSQ represent state-of-the-art techniques to minimize accuracy loss during this compression.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GGUF">GGUF - Wikipedia</a></li>
<li><a href="https://www.deepspeed.ai/tutorials/MoQ-tutorial/">DeepSpeed Mixture-of- Quantization ( MoQ ) - DeepSpeed</a></li>
<li><a href="https://arxiv.org/html/2604.18556">GSQ : Highly-Accurate Low-Precision Scalar Quantization for LLMs via...</a></li>

</ul>
</details>

**Tags**: `#quantization`, `#GGUF`, `#LLM`, `#inference optimization`, `#local deployment`

---

<a id="item-15"></a>
## [Gemma 4 QAT Benchmarks on Strix Halo APU](https://www.reddit.com/r/LocalLLaMA/comments/1tyilv7/gemma_4_qat_q4_0_bench_on_strix_halo/) ⭐️ 8.0/10

A user benchmarked Google's official Gemma 4 QAT Q4_0 GGUF models on an AMD Strix Halo APU (Ryzen AI Max+ 395) using llama.cpp with Vulkan backend, including multi-token prediction (MTP) assistant heads. The 26B-A4B QAT model achieved up to 71.4 tokens per second decode with 91.8% draft acceptance. This benchmark shows the practical performance of quantization-aware training (QAT) for large language models on a cutting-edge consumer APU, demonstrating that high-quality local inference is feasible with models like Gemma 4. The results help users understand the trade-offs between model size, quantization, and inference speed for local LLM deployment. The test system used 128 GB unified LPDDR5X memory, Linux Mint with kernel 6.17, and Mesa 25.2.8. The 26B-A4B QAT model with QAT-matched MTP and Q8 KV cache delivered 71.4 tok/s decode, while plain Vulkan without MTP reached 59 tok/s. The 12B and 31B models showed lower performance, with 31B only achieving about 19 tok/s.

reddit · r/LocalLLaMA · /u/westsunset · Jun 6, 14:22

**Background**: GGUF is a file format for efficient LLM storage and inference, created by the llama.cpp project. Strix Halo is AMD's high-performance APU combining Zen 5 cores and a large RDNA 3.5 iGPU. Quantization-aware training (QAT) simulates low-precision arithmetic during training to reduce accuracy loss compared to post-training quantization.

<details><summary>References</summary>
<ul>
<li><a href="https://ggufloader.github.io/what-is-gguf.html">What is GGUF? Complete Guide to GGUF Format & Quantization</a></li>
<li><a href="https://d33gy59ovltp76.cloudfront.net/news/amd-s-game-changing-strix-halo-apu-formally-known-as-the-ryzen-ai-max-poses-for-new-die-shots-and-gets-annotated">AMD's game-changing Strix Halo APU , formally known as</a></li>
<li><a href="https://www.ibm.com/think/topics/quantization-aware-training">What is quantization aware training? - IBM</a></li>

</ul>
</details>

**Tags**: `#Gemma 4`, `#QAT`, `#Quantization`, `#Local LLM`, `#Strix Halo`

---