---
layout: default
title: "Horizon Summary: 2026-06-01 (EN)"
date: 2026-06-01
lang: en
---

> From 44 items, 9 important content pieces were selected

---

1. [Cloudflare Turnstile WebGL Fingerprinting Undermines Privacy](#item-1) ⭐️ 8.0/10
2. [1-Bit Bonsai Image 4B: Efficient Local Image Generation](#item-2) ⭐️ 8.0/10
3. [VideoLAN Unveils Dav2d: Open-Source AV2 Decoder](#item-3) ⭐️ 8.0/10
4. [Linux Restartable Sequences Explained](#item-4) ⭐️ 8.0/10
5. [Deflock reaches 100k mapped ALPRs in the US](#item-5) ⭐️ 8.0/10
6. [NVIDIA Parakeet Ported to ggml: Faster, Quantized, No Python](#item-6) ⭐️ 8.0/10
7. [Abliterated Gemma 4 E2B Variants Benchmarked](#item-7) ⭐️ 8.0/10
8. [FROST Attack Uses SSD Timing to Spy on Users](#item-8) ⭐️ 8.0/10
9. [AV2 Reference Encoder Reaches First 1.0.0 Release](#item-9) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Cloudflare Turnstile WebGL Fingerprinting Undermines Privacy](https://hacktivis.me/articles/cloudflare-turnstile-webgl-fingerprinting) ⭐️ 8.0/10

Cloudflare Turnstile now requires WebGL for fingerprinting, effectively bypassing privacy protections like Firefox's resistFingerprinting and disabling access for minority browsers that lack WebGL support. This practice undermines user privacy by enabling persistent tracking without consent, and it disproportionately affects users of minority or privacy-focused browsers, fragmenting the web. The issue was reported by a minority browser maintainer who noted that users started encountering Cloudflare challenges a few weeks ago. WebGL fingerprinting uses hardware and driver details to create a unique identifier.

hackernews · HypnoticOcelot · May 31, 14:13 · [Discussion](https://news.ycombinator.com/item?id=48345840)

**Background**: Browser fingerprinting collects device information (OS, browser type, screen resolution, etc.) to create a unique identifier, often used for tracking without cookies. WebGL fingerprinting specifically leverages the graphics card's capabilities, which vary greatly even between identical devices. Cloudflare Turnstile is a CAPTCHA alternative that aims to verify human users without manual puzzles, but its reliance on WebGL compromises privacy for non-standard browsers.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/Cloudflare_Turnstile">Cloudflare Turnstile</a></li>
<li><a href="https://browserleaks.com/webgl">WebGL Browser Report - WebGL Fingerprinting - BrowserLeaks</a></li>
<li><a href="https://en.wikipedia.org/wiki/Browser_fingerprinting">Browser fingerprinting</a></li>

</ul>
</details>

**Discussion**: Commenters raised concerns about the broader arms race between bot detection and circumvention, with some noting that fingerprinting is common even if ecologically costly. Others criticized Mozilla for not enabling resistFingerprinting by default, while a minority browser maintainer reported real user impact.

**Tags**: `#privacy`, `#fingerprinting`, `#Cloudflare`, `#WebGL`, `#browser`

---

<a id="item-2"></a>
## [1-Bit Bonsai Image 4B: Efficient Local Image Generation](https://prismml.com/news/bonsai-image-4b) ⭐️ 8.0/10

PrismML has released Bonsai Image 4B, a 4-billion parameter diffusion transformer that uses 1-bit weight quantization to reduce memory footprint by up to 8.3x, enabling on-device image generation on an iPhone. This marks a significant step toward democratizing high-quality image generation by making it feasible on consumer devices without requiring expensive cloud subscriptions. Users can now run sophisticated models locally, preserving privacy and enabling offline use. Bonsai Image 4B is based on FLUX.2 Klein 4B and is available in both 1-bit and ternary variants. While it achieves strong visual quality, some community members noted that it is marginally slower than the original small FLUX.2 model.

hackernews · modinfo · May 31, 15:04 · [Discussion](https://news.ycombinator.com/item?id=48346257)

**Background**: 1-bit quantization is a technique where each model weight is represented using only a single bit (or a small number of bits), dramatically reducing memory and computation requirements. Diffusion models are a class of generative models that create images by iteratively denoising random noise, and they typically require significant GPU memory. By applying extreme quantization, models like Bonsai Image 4B can run on devices with limited resources, such as smartphones.

<details><summary>References</summary>
<ul>
<li><a href="https://prismml.com/news/bonsai-image-4b">PrismML — Introducing 1-bit and Ternary Bonsai Image 4B: Image Generation for Local Devices</a></li>
<li><a href="https://www.prnewswire.com/news-releases/prismml-releases-bonsai-image-4b-302782354.html">PrismML Releases Bonsai Image 4B</a></li>
<li><a href="https://gigazine.net/gsc_news/en/20260527-bonsai-image-4b-image-generation-ai/">I tried out 'Bonsai Image 4B,' an image generation AI that runs locally on iPhones, and modified FLUX.2 Klein 4B into a 1-bit version, reducing memory usage to 1/8.3 of the original. - GIGAZINE</a></li>

</ul>
</details>

**Discussion**: Community comments were mixed: some users expressed excitement about local hardware upgrades as an alternative to subscriptions, while others questioned whether memory is the real bottleneck given that generation time remains slow. One user pointed out that Bonsai Image 4B is not truly the first to run on iPhone, as FLUX.2 itself runs via app with 8-bit or 6-bit quantization.

**Tags**: `#1-bit`, `#image generation`, `#model compression`, `#local AI`, `#diffusion models`

---

<a id="item-3"></a>
## [VideoLAN Unveils Dav2d: Open-Source AV2 Decoder](https://jbkempf.com/blog/2026/dav2d/) ⭐️ 8.0/10

VideoLAN has released dav2d, an open-source decoder for the AV2 video codec, marking the first major independent implementation of the standard. AV2 promises 25-30% bitrate reduction over AV1 but requires roughly five times more decoding complexity, making efficient software decoders crucial for adoption. Dav2d provides a production-ready, cross-platform decoder that can help hardware and software ecosystems prepare for AV2. The dav2d decoder is developed by the same team behind libavcodec and focuses on both speed and correctness. It is cross-platform and aims to serve as a reference for future hardware implementations.

hackernews · captain_bender · May 31, 11:44 · [Discussion](https://news.ycombinator.com/item?id=48344961)

**Background**: AV2 is the next-generation open, royalty-free video coding format from the Alliance for Open Media, succeeding AV1. It was formally released in May 2026 and offers about 30% better compression efficiency than AV1 at the cost of significantly higher computational complexity. VideoLAN is known for developing VLC media player and has a history of creating efficient decoders like dav1d for AV1.

<details><summary>References</summary>
<ul>
<li><a href="https://www.phoronix.com/news/Dav2d-Open-Source-AV2-Decode">VideoLAN Publishes Dav2d For Open-Source AV2 Decoder - Phoronix</a></li>
<li><a href="https://en.wikipedia.org/wiki/AV2_(video_coding_format)">AV2 (video coding format)</a></li>

</ul>
</details>

**Discussion**: Community comments express concern that AV2's decoding complexity is roughly five times that of AV1, potentially making existing AV1 hardware decoders obsolete. Some question whether a 25% size reduction justifies the cost of new hardware, though others note that software decoding may suffice for many use cases with optimization.

**Tags**: `#video codec`, `#AV2`, `#decoder`, `#performance`, `#open source`

---

<a id="item-4"></a>
## [Linux Restartable Sequences Explained](https://justine.lol/rseq/) ⭐️ 8.0/10

An article provides an in-depth technical explanation of Linux restartable sequences (rseq), a kernel feature enabling lock-free data structures without mutexes or atomic operations. This feature can significantly improve performance in multi-threaded applications by eliminating the overhead of traditional synchronization mechanisms, benefiting systems programmers working on high-concurrency code. Restartable sequences work by having the program mark critical sections; if the kernel preempts the thread within that section, it restarts the sequence from the beginning. The librseq library provides helpers for common use cases, so users often do not need to write assembly.

hackernews · grappler · May 31, 14:38 · [Discussion](https://news.ycombinator.com/item?id=48346019)

**Background**: Restartable sequences (rseq) are a Linux kernel mechanism that allows user-space code to perform per-CPU operations atomically without system calls. They were added in Linux kernel 4.18 and are used to efficiently implement reference counting, per-CPU counters, and other lock-free data structures. The kernel detects preemption or migration during a critical section and restarts the sequence, ensuring correctness without traditional locking.

<details><summary>References</summary>
<ul>
<li><a href="https://lwn.net/Articles/1033957/">The rseq() manual page [LWN.net]</a></li>
<li><a href="https://lwn.net/Articles/697539/">Kernel development [LWN.net]</a></li>

</ul>
</details>

**Discussion**: Community sentiment is largely positive, with users expressing excitement about using rseq in their projects. However, some commenters criticized the article's tone and lack of reference to the librseq library, noting that it provides easier-to-use helpers that avoid assembly.

**Tags**: `#linux`, `#kernel`, `#concurrency`, `#systems-programming`

---

<a id="item-5"></a>
## [Deflock reaches 100k mapped ALPRs in the US](https://deflock.org/) ⭐️ 8.0/10

The open-source project Deflock announced it has mapped over 100,000 automated license plate readers (ALPRs) across the United States. This milestone highlights the scale of surveillance infrastructure and empowers communities to challenge privacy abuses. It also sparks debate on how to counterbalance the benefits of security cameras with individual privacy rights. However, some community members note the data may be overcounted by a few percent due to duplication in OpenStreetMap. Additionally, the new map interface requires WebGL, causing accessibility issues for some users.

hackernews · pilingual · May 31, 17:04 · [Discussion](https://news.ycombinator.com/item?id=48347370)

**Background**: Automated License Plate Readers (ALPRs) are high-speed cameras that capture license plate data, often used by law enforcement and private companies. Deflock is a community-driven open-source project that maps these devices to increase transparency and accountability. The project uses OpenStreetMap data and encourages public contributions. As surveillance concerns grow, initiatives like Deflock help individuals understand where they are being watched.

<details><summary>References</summary>
<ul>
<li><a href="https://www.forbes.com/sites/larsdaniel/2024/11/26/think-youre-not-being-watched-deflock-says-think-again/">Think You’re Not Being Watched? DeFlock Says Think Again</a></li>
<li><a href="https://www.404media.co/the-open-source-project-deflock-is-mapping-license-plate-surveillance-cameras-all-over-the-world/">The Open Source Project DeFlock Is Mapping License Plate ...</a></li>
<li><a href="https://sls.eff.org/technologies/automated-license-plate-readers-alprs">Automated License Plate Readers</a></li>

</ul>
</details>

**Discussion**: Commenters expressed mixed feelings: some support the pushback against privacy abuses, while others raise concerns about data accuracy (e.g., ~2,500 duplicate entries) and technical limitations like WebGL requirements. A few suggest that companies like Flock could circumvent mapping by placing cameras on private property, advocating for stronger legislation instead.

**Tags**: `#privacy`, `#surveillance`, `#ALPR`, `#openstreetmap`, `#mapping`

---

<a id="item-6"></a>
## [NVIDIA Parakeet Ported to ggml: Faster, Quantized, No Python](https://www.reddit.com/r/LocalLLaMA/comments/1tt6oja/i_ported_nvidia_parakeet_speechtotext_to_ggml/) ⭐️ 8.0/10

A developer ported NVIDIA's Parakeet speech-to-text models to pure C++/ggml, achieving byte-identical output to NeMo with up to 5x speedup on GPU and 1.86x on CPU when quantized, and releasing GGUF quantized variants for efficient CPU/GPU inference. This makes high-quality NVIDIA speech-to-text models deployable without Python or PyTorch, enabling faster inference, lower memory usage, and easy embedding in applications, which benefits developers building local and edge ASR systems. The port supports FastConformer TDT/CTC/RNNT/hybrid models, runs on CPU and GPU (CUDA, HIP, Vulkan, Metal), and includes cache-aware streaming with word-level timestamps and confidence scores. The GGUF model file is self-contained with tokenizer baked in.

reddit · r/LocalLLaMA · /u/mudler_it · May 31, 20:35

**Background**: ggml is a tensor library for machine learning that enables large models on commodity hardware, used by llama.cpp and whisper.cpp. NVIDIA Parakeet is a family of state-of-the-art ASR models based on the FastConformer architecture. GGUF is a quantization format that reduces model size and speeds up inference on consumer hardware.

<details><summary>References</summary>
<ul>
<li><a href="https://ggml.ai/">ggml .ai</a></li>
<li><a href="https://developer.nvidia.com/blog/pushing-the-boundaries-of-speech-recognition-with-nemo-parakeet-asr-models/">Pushing the Boundaries of Speech Recognition with NVIDIA NeMo</a></li>
<li><a href="https://medium.com/@bnjmn_marie/gguf-quantization-for-fast-and-memory-efficient-inference-on-your-cpu-d10fbe58fbca">GGUF Quantization for Fast and Memory-Efficient Inference... | Medium</a></li>

</ul>
</details>

**Tags**: `#speech-to-text`, `#ggml`, `#NVIDIA Parakeet`, `#model optimization`, `#open source`

---

<a id="item-7"></a>
## [Abliterated Gemma 4 E2B Variants Benchmarked](https://www.reddit.com/r/LocalLLaMA/comments/1tsvs3j/13_abliterated_gemma_4_e2b_variants_44_gpu_hours/) ⭐️ 8.0/10

A Reddit user posted a comprehensive comparison of 13 abliterated variants of Google's Gemma 4 E2B model, using 44 GPU hours to evaluate safety removal (HarmBench ASR) and performance on 8 benchmarks, revealing which methods preserve capabilities. This work provides actionable insights for the AI safety community by identifying abliteration techniques that achieve high attack success rates without degrading performance, and it exposes discrepancies between claimed and actual capability preservation, which is critical for open-source model alignment. The best variant (coder3101) achieves 96% ASR and even outperforms the base model on GSM8K math, while aggressive methods cause significant perplexity increases (up to 7.35x) and token wastage; moreover, 5 of 13 models were missing safetensor keys due to shared KV projections.

reddit · r/LocalLLaMA · /u/nathandreamfast · May 31, 13:44

**Background**: Abliteration is a technique to remove safety alignment from large language models, often by ablating or modifying the refusal direction. Tools like Heretic automate this process. HarmBench is a standardized benchmark for evaluating the attack success rate (ASR) against harmful prompts, measuring how often a model refuses or complies.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/blog/mlabonne/abliteration">Uncensor any LLM with abliteration</a></li>
<li><a href="https://github.com/p-e-w/heretic">GitHub - p-e-w/heretic: Fully automatic censorship removal for</a></li>
<li><a href="https://arxiv.org/abs/2402.04249">[2402.04249] HarmBench: A Standardized Evaluation Framework for</a></li>

</ul>
</details>

**Tags**: `#abliteration`, `#Gemma 4`, `#model safety`, `#benchmark`, `#alignment`

---

<a id="item-8"></a>
## [FROST Attack Uses SSD Timing to Spy on Users](https://futurism.com/future-society/websites-spying-solid-state-drive) ⭐️ 8.0/10

Researchers disclosed the FROST (Fingerprinting Remotely using OPFS-based SSD Timing) attack, which allows malicious websites to infer user activities by measuring SSD read/write timing via the browser's Origin Private File System (OPFS) API, without any user interaction. This side-channel attack poses a significant privacy threat as it enables remote, passive surveillance of a user's browsing and application usage with high accuracy, using only standard browser APIs. It highlights a new class of vulnerabilities in modern web platform features. In experiments, the FROST attack achieved 88.95% accuracy in predicting visited websites and 95.83% accuracy in predicting opened applications. The attack was tested on macOS and Linux, but researchers claim Windows is also potentially vulnerable; closing browser tabs after use can reduce risk.

telegram · zaihuapd · May 31, 01:55

**Background**: SSD timing side-channel attacks exploit the measurable differences in read/write latency caused by contention for the SSD's internal resources. The Origin Private File System (OPFS) is a browser API that provides web apps with a private, sandboxed file system for storing files locally. FROST uses OPFS to generate controlled read/write operations and measures their completion time to detect other activity on the system, inferring which websites or applications are in use.

<details><summary>References</summary>
<ul>
<li><a href="https://cyberpress.org/sites-ssd-timing-side-channel-attacks/">Malicious Sites Track Users Through SSD Timing Side-Channel Attacks</a></li>
<li><a href="https://cybersecuritynews.com/malicious-websites-track-ssd-timing/">Malicious Websites Track Visitors by Analyzing their SSD ...</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system">Origin private file system - Web APIs | MDN</a></li>

</ul>
</details>

**Tags**: `#security`, `#side-channel attack`, `#SSD`, `#browser`, `#privacy`

---

<a id="item-9"></a>
## [AV2 Reference Encoder Reaches First 1.0.0 Release](https://videocardz.com/newz/aomedias-av2-encoder-gets-first-1-0-0-release) ⭐️ 8.0/10

AOMedia has tagged the first 1.0.0 release of the AV2 reference encoder in the AVM GitHub repository, marking an initial milestone for the next-generation royalty-free video codec. This release signifies progress toward a practical AV2 codec, which aims to deliver approximately 30% better compression than AV1, potentially reshaping video streaming, broadcasting, and real-time communications with higher efficiency. The current AVM software is a reference implementation for defining and testing the format, not an optimized production encoder; it still suffers from slow encoding speed and unresolved detail preservation issues, and the AV2 specification remains a draft.

telegram · zaihuapd · May 31, 14:08

**Background**: AV2 is an open, royalty-free video coding format developed by the Alliance for Open Media, succeeding the widely used AV1. Work began in 2020, and prototype implementations show around 30% bitrate reduction over AV1 at similar quality. AV2 is expected to compete with the royalty-based VVC (H.266) format in the market.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AV2_(video_coding_format)">AV2 (video coding format)</a></li>
<li><a href="https://www.phoronix.com/news/AV2-1.0-Specification-Released">AV 2 v1.0 Specification Released For Next-Gen Video Coding - Phoronix</a></li>
<li><a href="https://aomedia.org/press+releases/AOMedia-Announces-Year-End-Launch-of-Next-Generation-Video-Codec-AV2-on-10th-Anniversary/">AOMedia Announces Year-End Launch of Next Generation Video</a></li>

</ul>
</details>

**Tags**: `#AV2`, `#video codec`, `#AOMedia`, `#reference encoder`

---