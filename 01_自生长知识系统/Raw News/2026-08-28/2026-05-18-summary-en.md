---
layout: default
title: "Horizon Summary: 2026-05-18 (EN)"
date: 2026-05-18
lang: en
---

> From 31 items, 12 important content pieces were selected

---

1. [GDS Advises NHS to Keep Open Source Repos Public](#item-1) ⭐️ 9.0/10
2. [AI Won't Speed Up Software Development](#item-2) ⭐️ 8.0/10
3. [Native Apps Still Rely on WebKit for Text Rendering](#item-3) ⭐️ 8.0/10
4. [AI is a technology, not a product](#item-4) ⭐️ 8.0/10
5. [Mozilla to UK Regulators: Do Not Undermine VPNs](#item-5) ⭐️ 8.0/10
6. [Linus Torvalds on AI Bug Flood: Kernel Security List Overwhelmed](#item-6) ⭐️ 8.0/10
7. [Computer Security Pioneer Peter G. Neumann Passes Away](#item-7) ⭐️ 8.0/10
8. [Paid program misleads high school students into fake ML research](#item-8) ⭐️ 8.0/10
9. [M5 vs DGX Spark vs Strix Halo vs RTX 6000 AI Benchmark](#item-9) ⭐️ 8.0/10
10. [85 GPU-Hour Comparison of 5 Abliteration Methods on Qwen3.6-27B](#item-10) ⭐️ 8.0/10
11. [Dual GPU llama.cpp speedup with quantized KV cache fix](#item-11) ⭐️ 8.0/10
12. [Changxin Technology Files for IPO on STAR Market with 719% Revenue Surge](#item-12) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [GDS Advises NHS to Keep Open Source Repos Public](https://simonwillison.net/2026/May/17/gds-weighs-in/#atom-everything) ⭐️ 9.0/10

The UK Government Digital Service (GDS) published guidance on May 14, 2026, recommending that public sector organizations keep open source repositories public by default, directly countering the NHS's plan to close its repos after security vulnerabilities were reported via Project Glasswing. This intervention signals a major policy conflict within the UK government, as GDS—the central digital authority—publicly challenges NHS's retreat from open source, emphasizing that closing repos increases costs and reduces scrutiny. The outcome could set a precedent for open source practices across the entire UK public sector. GDS's guidance warns that making everything private adds 'delivery and policy costs' and reduces reuse and scrutiny, while the NHS decision was triggered by vulnerabilities disclosed through Anthropic's Project Glasswing cybersecurity initiative. Terence Eden interprets GDS's statement as a rare public escalation of internal civil service disagreement.

rss · Simon Willison · May 17, 15:59

**Background**: The Government Digital Service (GDS) is a UK government unit responsible for transforming digital public services. The NHS (National Health Service) had planned to close its open source repositories after vulnerabilities were reported via Project Glasswing, a cybersecurity initiative by Anthropic that uses AI to find security flaws in critical open source software. Open source software is code that is publicly accessible and can be freely used, modified, and shared, often leading to greater transparency and faster innovation but also potential security risks.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Government_Digital_Service">Government Digital Service - Wikipedia</a></li>
<li><a href="https://www.anthropic.com/glasswing">Project Glasswing: Securing critical software for the AI era</a></li>

</ul>
</details>

**Tags**: `#open source`, `#government policy`, `#security`, `#NHS`, `#GDS`

---

<a id="item-2"></a>
## [AI Won't Speed Up Software Development](https://frederickvanbrabant.com/blog/2026-05-15-i-dont-think-ai-will-make-your-processes-go-faster/) ⭐️ 8.0/10

A blog post argues that AI, especially large language models, will not significantly speed up software development because the main bottleneck is unclear requirements, not coding speed. This contrarian perspective challenges the prevailing narrative that AI boosts overall productivity, forcing a reexamination of where true inefficiencies lie in software engineering. The author emphasizes that software engineering is fundamentally about clarifying ambiguous requirements, a task that AI cannot automate, and notes that vague feature requests have long been a major pain point.

hackernews · TheEdonian · May 17, 12:13 · [Discussion](https://news.ycombinator.com/item?id=48168221)

**Background**: Software development involves multiple phases, from requirements to deployment. While AI tools like GitHub Copilot can accelerate coding, the most time-consuming part often is understanding what to build. The article argues that unless AI helps with requirements clarification, overall process speed gains remain limited.

**Discussion**: Comments are largely supportive, with users sharing anecdotes of vague requirements and agreeing that the bottleneck is often pre-development. Some argue AI can assist in other phases like ideation and documentation, but there is broad consensus that the article highlights a key truth.

**Tags**: `#AI`, `#software engineering`, `#requirements`, `#productivity`, `#LLMs`

---

<a id="item-3"></a>
## [Native Apps Still Rely on WebKit for Text Rendering](https://justsitandgrin.im/posts/native-all-the-way-until-you-need-text/) ⭐️ 8.0/10

A technical blog post reveals that native apps often fall back to WebKit for rendering rich text like Markdown, because native SwiftUI Text components struggle with performance and features, especially for large documents. This highlights a pragmatic trade-off in the native vs web debate: even performance-critical native apps choose WebKit for text-heavy views, challenging the assumption that native always delivers better performance. The author benchmarks a Markdown chat view and finds WebKit rendering is significantly faster than SwiftUI's Text, with sub-8ms keystroke restyling in TextKit 2, while WebKit benefits from mature GPU-accelerated engines.

hackernews · dive · May 17, 11:49 · [Discussion](https://news.ycombinator.com/item?id=48168058)

**Background**: Native app development on Apple platforms uses frameworks like SwiftUI and UIKit, but their Text components can be slow for large or richly formatted documents. WebKit, the engine behind Safari, is available as a native framework (WKWebView) on macOS and iOS, allowing apps to render HTML and CSS efficiently. This post explores the performance trade-offs and argues that using WebKit for text rendering is a practical choice rather than a failure of native development.

<details><summary>References</summary>
<ul>
<li><a href="https://webkit.org/blog/16301/webkit-features-in-safari-18-2/">WebKit Features in Safari 18.2 | WebKit</a></li>
<li><a href="https://fatbobman.com/en/posts/creating-stunning-dynamic-text-effects-with-textrender/">Creating Stunning Dynamic Text Effects with TextRenderer</a></li>
<li><a href="https://stackoverflow.com/questions/75922628/conditionally-rendering-text-view-with-a-large-string-causes-performance-issue">swiftui - Conditionally rendering Text view with a large string causes performance issue - Stack Overflow</a></li>

</ul>
</details>

**Discussion**: Commenters shared mixed experiences: one developer praised TextKit 2 for fast keystroke restyling, while another noted that browser engines have outpaced SwiftUI in performance. Some agreed that WebKit is appropriate for Markdown rendering, but a counterargument pointed to mature SwiftUI Markdown libraries like swift-markdown-ui. Overall, the discussion centered on when to use native vs web text rendering, with concrete performance data.

**Tags**: `#native vs web`, `#performance`, `#text rendering`, `#WebKit`, `#SwiftUI`

---

<a id="item-4"></a>
## [AI is a technology, not a product](https://daringfireball.net/2026/05/ai_is_technology_not_a_product) ⭐️ 8.0/10

An article argues that artificial intelligence should be treated as an underlying technology integrated into products, rather than being marketed as a standalone product itself. This perspective challenges the current trend of AI productization, emphasizing that true value comes from seamless integration into user experiences, especially for companies like Apple focused on usability. The article highlights that successful AI implementation, such as making Siri work reliably for everyday tasks, does not need to feel like AI at all; it should be invisible to the user.

hackernews · ch_sm · May 17, 13:11 · [Discussion](https://news.ycombinator.com/item?id=48168626)

**Background**: Many tech companies currently market AI features as separate products or upgrades. However, the most effective AI is often invisible, powering features like smart recommendations or voice assistants. Apple has historically prioritized seamless user experience over showcasing underlying technology.

**Discussion**: Commenters largely agree, citing examples like improving Siri without making it feel like AI, and referencing the "Dropbox is a feature" analogy. Some emphasize working backward from customer experience, as Steve Jobs advocated.

**Tags**: `#AI`, `#product design`, `#Apple`, `#user experience`, `#technology strategy`

---

<a id="item-5"></a>
## [Mozilla to UK Regulators: Do Not Undermine VPNs](https://blog.mozilla.org/netpolicy/2026/05/15/mozilla-to-uk-regulators-vpns-are-essential-privacy-and-security-tools-and-should-not-be-undermined/) ⭐️ 8.0/10

Mozilla submitted a response to a UK government consultation on online age verification, arguing that VPNs are essential for privacy and security and should not be restricted or undermined. This matters because it represents a major pushback from a prominent tech company against potential regulations that could limit VPN usage, directly affecting privacy rights and digital security for UK citizens and setting a precedent for other countries. The UK consultation, part of the 'growing up in the online world' initiative, includes a specific question about age-gating VPNs. Mozilla emphasizes that regulators should address online harm by holding platforms accountable, rather than targeting VPNs.

hackernews · WithinReason · May 17, 06:17 · [Discussion](https://news.ycombinator.com/item?id=48166459)

**Background**: VPNs (Virtual Private Networks) encrypt internet traffic and hide users' IP addresses, providing privacy and security. Some governments propose age-gating VPNs to prevent minors from bypassing content restrictions, but privacy advocates argue this undermines fundamental privacy protections and could be counterproductive.

**Discussion**: Commenters largely support Mozilla's stance, with some noting that the Australian government surprisingly recommends VPN usage. Others question how platforms can effectively age-verify without VPNs, and there is criticism comparing UK digital policy to dystopian surveillance.

**Tags**: `#VPN`, `#privacy`, `#Mozilla`, `#UK regulation`, `#digital rights`

---

<a id="item-6"></a>
## [Linus Torvalds on AI Bug Flood: Kernel Security List Overwhelmed](https://lwn.net/Articles/1073193/) ⭐️ 8.0/10

Linus Torvalds announced in the 7.1-rc4 kernel prepatch that the Linux kernel security list is overwhelmed by a flood of AI-generated bug reports, and made it clear that such bugs are not considered secret and should not be handled privately. This policy clarification addresses the growing problem of AI-generated bug reports, which cause duplication and wasted effort; it sets a precedent for how the kernel community handles automated submissions, potentially improving efficiency and transparency. The announcement accompanied a pull request from Willy Tarreau with patches defining what constitutes a security bug and responsible ways to use AI for bug finding, providing technical guidelines for the community.

rss · LWN.net · May 17, 21:39

**Background**: The Linux kernel security list is a private mailing list used to discuss potential security vulnerabilities before public disclosure. Kernel prepatches (like -rc4) are release candidates for the next stable kernel version, used for testing. AI-generated bug reports have been increasing, causing noise and duplication, leading to the need for policy changes.

**Tags**: `#Linux kernel`, `#security`, `#AI-generated bugs`, `#kernel maintenance`, `#Linus Torvalds`

---

<a id="item-7"></a>
## [Computer Security Pioneer Peter G. Neumann Passes Away](https://lwn.net/Articles/1073186/) ⭐️ 8.0/10

Peter G. Neumann, the renowned computer security pioneer and longtime editor of the RISKS Digest, has passed away. The New York Times published an obituary on May 17, 2026. Neumann's decades-long work on RISKS Digest and his research at SRI shaped the field of computer security and risk analysis. His passing is a great loss to the cybersecurity community. Neumann moderated the RISKS Digest, an ACM periodical published since 1985 that discusses risks in computer systems and public policy. The announcement was made on the LWN.net mailing list.

rss · LWN.net · May 17, 19:36

**Background**: The RISKS Digest (Forum on Risks to the Public in Computers and Related Systems) is a moderated online periodical focused on security, safety, and unintended consequences of technological systems. Founded by Peter G. Neumann, it has been a key resource for system administrators and security professionals for decades. Neumann was also a researcher at SRI International and a prominent voice in computer security.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/RISKS_Digest">RISKS Digest</a></li>
<li><a href="https://catless.ncl.ac.uk/Risks/">RISKS-LIST: RISKS-FORUM Digest</a></li>

</ul>
</details>

**Tags**: `#obituary`, `#computer security`, `#RISKS Digest`, `#Peter G. Neumann`

---

<a id="item-8"></a>
## [Paid program misleads high school students into fake ML research](https://www.reddit.com/r/MachineLearning/comments/1tfh2s9/program_misleading_high_school_students_into/) ⭐️ 8.0/10

A paid program called Algoverse AI Research is accused of misleading high school students into publishing flawed machine learning papers by claiming acceptance to NeurIPS workshops, with multiple papers containing obvious errors such as identical results across different experimental conditions. This exposes a serious ethics breach in ML research, particularly targeting high school students for profit, and undermines the credibility of reputable venues like NeurIPS workshops. It raises concerns about the integrity of the peer review process and the exploitation of students seeking college application credentials. The program's website claims 289 students accepted to NeurIPS 2025, yet the director Kevin Zhu has 158 publications and 468 coauthors but no PhD or master's degree. Specific papers showed duplicated results in tables and misplaced sections like Related Works inside Results.

reddit · r/MachineLearning · Marisu_BG · May 17, 06:08

**Background**: NeurIPS is a top-tier machine learning conference, and its workshops are prestigious but less rigorous than the main conference. OpenReview is a platform for reviewing papers. Algoverse markets itself as helping high school students publish AI research, but critics say it exploits the system for profit.

<details><summary>References</summary>
<ul>
<li><a href="https://algoverseairesearch.org/">Algoverse AI Research</a></li>
<li><a href="https://openreview.net/about">About | OpenReview</a></li>
<li><a href="https://blog.neurips.cc/2025/04/12/guidance-for-neurips-workshop-proposals-2025/">Guidance for NeurIPS Workshop Proposals 2025 – NeurIPS</a></li>

</ul>
</details>

**Discussion**: Comments note that similar exploitation has existed in STEM research, with some calling Algoverse a scaled-up version of known practices. Others question how errors were found, and a commenter highlights the director's lack of advanced degrees. A Guardian article link is shared, confirming the controversy.

**Tags**: `#academic misconduct`, `#ML research`, `#ethics`, `#high school`, `#NeurIPS`

---

<a id="item-9"></a>
## [M5 vs DGX Spark vs Strix Halo vs RTX 6000 AI Benchmark](https://i.redd.it/mk82wx765r1h1.jpeg) ⭐️ 8.0/10

A standardized benchmark comparison of M5, DGX Spark, Strix Halo, and RTX 6000 for AI inference over three days reveals that the RTX 6000 outperforms for small models that fit in VRAM, while the M5 maintains consistent performance for larger models exceeding VRAM. This comparison provides practical trade-offs for AI inference hardware selection, highlighting the importance of memory bandwidth and VRAM overflow penalties. It helps developers decide between unified memory (Apple) and discrete GPU setups. The RTX 6000 has ~1800 GB/s memory bandwidth, M5 ~600 GB/s, and DGX Spark/Strix Halo ~256 GB/s. During extended runs, the M5 MacBook Pro maintained ~80°C but was noisy like a gaming laptop, while the EVO X2 (Strix Halo) had thermal issues.

reddit · r/LocalLLaMA · Signal_Ad657 · May 17, 19:49 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1tfzsd6/m5_vs_dgx_spark_vs_strix_halo_vs_rtx_6000/)

**Background**: AI inference performance heavily depends on memory bandwidth, as models generate tokens per second proportional to bandwidth. Unified memory architectures like Apple M5 allow large models to run without VRAM overflow penalties, while discrete GPUs like RTX 6000 suffer performance drops when model size exceeds VRAM. DGX Spark is NVIDIA's compact AI supercomputer, and Strix Halo is AMD's high-performance APU for mini PCs.

<details><summary>References</summary>
<ul>
<li><a href="https://www.nvidia.com/en-us/products/workstations/dgx-spark/">Personal AI Supercomputer Powered by Blackwell | NVIDIA DGX</a></li>
<li><a href="https://www.gmktec.com/products/amd-ryzen™-ai-max-395-evo-x2-ai-mini-pc">GMKtec EVO-X2 AI Mini PC AMD Ryzen™ AI Max+ 395</a></li>
<li><a href="https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/">NVIDIA DGX Spark: great hardware, early days for the ecosystem</a></li>

</ul>
</details>

**Discussion**: Top comment notes that RTX 6000 wins for small models but M5 holds steady for large models due to unified memory. Others discuss price differences ($5.5k for M5 Max 128GB vs $3.8k for DGX Spark), criticize Apple's non-upgradability and ecosystem lock-in, and question M5's parallel request performance compared to a 4090 with vLLM.

**Tags**: `#hardware comparison`, `#AI inference`, `#benchmarking`, `#LLM`, `#Apple M5`

---

<a id="item-10"></a>
## [85 GPU-Hour Comparison of 5 Abliteration Methods on Qwen3.6-27B](https://www.reddit.com/r/LocalLLaMA/comments/1tfmocw/85_gpuhours_comparing_5_abliteration_methods_on/) ⭐️ 8.0/10

The author released Abliterlitics, an open-source toolkit that systematically compares five abliteration techniques on the Qwen3.6-27B model using 85 GPU-hours of benchmarks, safety evaluations, and weight-level forensics. The analysis reveals that Heretic and Huihui variants best preserve capabilities, while all methods achieve near-complete safety removal. This work provides the first rigorous, open-source comparison of abliteration methods, helping the LLM safety community understand trade-offs between capability retention and refusal suppression. It establishes a reproducible benchmarking methodology that can guide future alignment research and model selection. The author recovered safetensors from a Q8_K_P GGUF file and ran 85 hours of benchmarks including HarmBench, KL divergence, and weight forensics across six models (base plus five abliterated). The AEON variant's claim of 'enhanced capabilities' is contradicted by the data, and Abliterix shows the worst capability preservation.

reddit · r/LocalLLaMA · nathandreamfast · May 17, 11:18

**Background**: Abliteration is a technique that identifies and suppresses a single latent direction responsible for refusal behavior in LLMs, effectively 'uncensoring' the model. Safetensors is a secure tensor file format that prevents code execution, and GGUF is a quantization format that reduces model size. This work uses these formats to recover and compare models.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/blog/mlabonne/abliteration">Uncensor any LLM with abliteration</a></li>
<li><a href="https://github.com/NousResearch/llm-abliteration/">GitHub - NousResearch/llm-abliteration: Make abliterated models with transformers, easy and fast · GitHub</a></li>

</ul>
</details>

**Discussion**: The community highly appreciates the effort, with comments calling it a 'high-effort post' and thanking the author. One user provided constructive technical feedback suggesting measuring distribution shifts at every token position rather than just the first, and offered example code. Several users asked for a simpler breakdown and best use cases.

**Tags**: `#abliteration`, `#LLM safety`, `#model alignment`, `#benchmarking`, `#open source`

---

<a id="item-11"></a>
## [Dual GPU llama.cpp speedup with quantized KV cache fix](https://www.reddit.com/r/LocalLLaMA/comments/1tflngz/dual_gpu_llamacpp_speedup/) ⭐️ 8.0/10

A contributor named RedToasty fixed llama.cpp's tensor parallelism mode to support quantized KV caches, enabling faster multi-GPU inference without the memory overhead of non-quantized caches. Benchmarks show a significant speedup, e.g., from ~31 to ~50 tokens/second on a dual-GPU setup. This fix addresses a long-standing limitation that forced users to choose between tensor parallelism (fast) and quantized KV cache (memory-efficient). It makes multi-GPU inference with llama.cpp more practical for real-world workloads, potentially reducing the need for alternative engines like vLLM for local inference. The fix is implemented in a fork called llama.cpp_qts with minimal changes from mainline. It supports quantized K and V caches (e.g., Q8_0) in tensor parallelism mode, but the contributor notes instability after many requests, recommending auto-restart tools like llama-swap. The feature is not yet merged into mainline.

reddit · r/LocalLLaMA · Legitimate-Dog5690 · May 17, 10:24

**Background**: Tensor parallelism splits a model's layers across multiple GPUs to parallelize computation, boosting throughput. However, llama.cpp's implementation previously required non-quantized KV caches, which consume significant memory. Quantizing the KV cache reduces memory usage but was incompatible with tensor parallelism, forcing a trade-off. This fix resolves that incompatibility.

<details><summary>References</summary>
<ul>
<li><a href="https://rocm.blogs.amd.com/artificial-intelligence/tensor-parallelism/README.html">Analyzing the Impact of Tensor Parallelism Configurations on LLM Inference Performance — ROCm Blogs</a></li>
<li><a href="https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/">Quantized KV Cache - vLLM</a></li>

</ul>
</details>

**Discussion**: The community is enthusiastic about the fix, with many users expressing interest in switching from vLLM to llama.cpp. However, some note instability and recommend using auto-restart solutions. There's also a suggestion to benchmark at actual context lengths because layer splitting can be more effective for large KV caches. One user pointed out that vanilla llama.cpp already supports tensor parallelism for non-quantized KV caches.

**Tags**: `#llama.cpp`, `#tensor parallelism`, `#multi-GPU`, `#inference optimization`, `#KV cache`

---

<a id="item-12"></a>
## [Changxin Technology Files for IPO on STAR Market with 719% Revenue Surge](https://api3.cls.cn/share/article/2373399?os=android&amp;sv=8.7.8&amp;app=cailianpress) ⭐️ 8.0/10

Changxin Technology (ChangXin Memory Technologies) has filed an IPO prospectus on Shanghai's STAR Market, disclosing Q1 2026 revenue of 50.8 billion RMB, a 719.13% year-over-year increase, and net profit of 33.01 billion RMB, reversing last year's losses. This IPO provides a rare public investment opportunity in a leading Chinese DRAM manufacturer amid a global memory chip boom, signaling China's growing self-sufficiency in semiconductor memory and attracting significant investor attention. The company expects H1 2026 revenue between 110 and 120 billion RMB (up 612-677% YoY) and non-GAAP net profit of 52-58 billion RMB. The IPO comes as global DRAM supply shortages drive massive price increases, benefiting Chinese memory makers.

telegram · zaihuapd · May 17, 11:05

**Background**: DRAM (Dynamic Random Access Memory) is the main memory used in computers and servers. Changxin Technology is one of China's few DRAM producers, crucial for national tech self-sufficiency. The STAR Market (科创板) is a Shanghai stock exchange board for high-tech and growth enterprises, similar to Nasdaq.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Dynamic_random-access_memory">Dynamic random-access memory - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#IPO`, `#semiconductor`, `#DRAM`, `#Chinese tech`, `#finance`

---