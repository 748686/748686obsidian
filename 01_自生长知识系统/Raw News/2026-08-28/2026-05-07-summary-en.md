---
layout: default
title: "Horizon Summary: 2026-05-07 (EN)"
date: 2026-05-07
lang: en
---

> From 41 items, 14 important content pieces were selected

---

1. [Qwen 3.6 27B gets 2.5x faster inference via MTP in llama.cpp](#item-1) ⭐️ 9.0/10
2. [Apple to Open iOS 27 to Third-Party AI Models](#item-2) ⭐️ 9.0/10
3. [NVIDIA, OpenAI, Microsoft Release Open MRC Protocol](#item-3) ⭐️ 9.0/10
4. [Critique of Productivity Theater in Modern Workplaces](#item-4) ⭐️ 8.0/10
5. [Vibe coding and agentic engineering blur in practice](#item-5) ⭐️ 8.0/10
6. [Incus 7.0 LTS released with backup API and S3 support](#item-6) ⭐️ 8.0/10
7. [ZAYA1-8B: Efficient 8B model trained on AMD hardware](#item-7) ⭐️ 8.0/10
8. [Qwen 3.6 27B Quantization Quality Comparison via Chess SVG](#item-8) ⭐️ 8.0/10
9. [Qwen3-27B gets 2.5x speed with MTP graft on Unsloth UD XL GGUF](#item-9) ⭐️ 8.0/10
10. [Running Qwen3.6 27B NVFP4 with MTP on RTX 5090 at 200k Context](#item-10) ⭐️ 8.0/10
11. [Anthropic Commits $200 Billion to Google Cloud Over 5 Years](#item-11) ⭐️ 8.0/10
12. [DeepSeek Reportedly in Talks for $45B Valuation Funding](#item-12) ⭐️ 8.0/10
13. [Google Chrome silently downloads 4GB AI model without consent](#item-13) ⭐️ 8.0/10
14. [EU Plans Mandatory Removal of Huawei, ZTE Equipment from Telecom Networks](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Qwen 3.6 27B gets 2.5x faster inference via MTP in llama.cpp](https://www.reddit.com/r/LocalLLaMA/comments/1t57xuu/25x_faster_inference_with_qwen_36_27b_using_mtp/) ⭐️ 9.0/10

A recent pull request adds Multi-Token Prediction (MTP) support to llama.cpp for Qwen 3.6 27B, achieving up to 2.5x faster token generation on consumer hardware like M2 Max and RTX 3090. This makes local agentic coding viable on 48GB devices with up to 262k context, bridging the gap between cloud and local LLM inference for practical applications. The MTP feature uses the model's built-in tensor layers for speculative decoding, requiring a custom build of llama.cpp from the open PR. Converted GGUF quants with fixed Jinja chat templates are available on Hugging Face.

reddit · r/LocalLLaMA · ex-arman68 · May 6, 09:35

**Background**: Speculative decoding accelerates LLM inference by using a smaller draft model to predict multiple tokens, which are then verified by the main model in parallel. The GGUF format enables efficient quantization and deployment of models on consumer hardware. llama.cpp is a popular C/C++ inference engine that supports a wide range of models and optimizations.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/ggml-org/llama.cpp/pull/22673">llama + spec: MTP Support by am17an · Pull Request #22673 · ggml-org/llama.cpp</a></li>
<li><a href="https://research.google/blog/looking-back-at-speculative-decoding/">Looking back at speculative decoding</a></li>
<li><a href="https://dasroot.net/posts/2026/05/llama-cpp-performance-surge-beta-mtp-support/">Llama.cpp Performance Surge: Bridging the Gap with Beta MTP Support · Technical news about AI, coding and all</a></li>

</ul>
</details>

**Discussion**: The community is highly enthusiastic, with users reporting 2-3x speedups on various hardware. A user on RTX 3090 achieved 100 tok/s with 256k context on IQ4_XS quantization. Some users noted the rapid pace of progress can be overwhelming but appreciated the practical improvements.

**Tags**: `#inference-speedup`, `#local-llm`, `#llama.cpp`, `#speculative-decoding`, `#Qwen`

---

<a id="item-2"></a>
## [Apple to Open iOS 27 to Third-Party AI Models](https://www.bloomberg.com/news/articles/2026-05-05/ios-27-features-apple-plans-to-let-users-swap-models-across-apple-intelligence) ⭐️ 9.0/10

Apple plans to let users choose third-party AI models for system functions like Siri, Writing Tools, and Image Playground in iOS 27, iPadOS 27, and macOS 27, breaking ChatGPT's current exclusivity. This marks a groundbreaking shift in Apple's AI strategy, turning Apple Intelligence into an open platform that could reshape the AI assistant market by fostering competition among providers like Google and Anthropic. The feature, internally called Extensions, will be available in Settings and allow users to swap models for text generation, image generation, and editing, while Apple continues to offer its own models.

telegram · zaihuapd · May 6, 05:38

**Background**: Apple Intelligence is Apple's generative AI system, first announced at WWDC 2024, combining on-device and server processing. It initially integrated ChatGPT as the exclusive third-party model for features like Siri and Image Playground. This new plan expands third-party options dramatically.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Apple_Intelligence">Apple Intelligence</a></li>
<li><a href="https://www.apple.com/apple-intelligence/">Apple Intelligence - Apple</a></li>

</ul>
</details>

**Tags**: `#Apple`, `#AI`, `#iOS`, `#ChatGPT`, `#third-party models`

---

<a id="item-3"></a>
## [NVIDIA, OpenAI, Microsoft Release Open MRC Protocol](https://blogs.nvidia.com/blog/spectrum-x-ethernet-mrc/) ⭐️ 9.0/10

NVIDIA, OpenAI, and Microsoft, along with other partners, jointly released and open-sourced the Multipath Reliable Connection (MRC) protocol, an RDMA transport that uses packet spraying for concurrent multi-path transmission and microsecond-level failure rerouting. This collaboration among major AI players targets network bottlenecks in large-scale AI training, improving throughput and stability for gigascale clusters. As an open standard contributed to OCP, MRC aims to reduce industry fragmentation and accelerate future AI infrastructure like Stargate. MRC is already deployed on NVIDIA Spectrum-X platforms and Blackwell architecture, powering systems like Microsoft Fairwater and OCI Abilene, and is used for training models such as GPT-5.5. The protocol is an open specification under the Open Compute Project (OCP).

telegram · zaihuapd · May 6, 14:39

**Background**: RDMA (Remote Direct Memory Access) enables direct data transfer between computers without OS intervention, achieving high throughput and low latency. Traditional networks face congestion and single-path failures in large AI clusters. MRC combines packet spraying (sending data across multiple paths) with rapid failover to keep GPUs fed and reduce idle time.

<details><summary>References</summary>
<ul>
<li><a href="https://blogs.nvidia.com/blog/spectrum-x-ethernet-mrc/">NVIDIA Spectrum-X — the Open, AI-Native Ethernet Fabric ...</a></li>
<li><a href="https://www.firecat-web.com/daily-news/7869">OpenAI联合多家厂商推出MRC协议，破解大规模AI训练网络瓶颈</a></li>
<li><a href="https://news.qq.com/rain/a/20260507A00RCF00">OpenAI携手五巨头开源革命性超算协议：一举解决超大集群LLM训练不稳定...</a></li>

</ul>
</details>

**Tags**: `#AI基础设施`, `#网络协议`, `#NVIDIA`, `#MRC协议`, `#高算力集群`

---

<a id="item-4"></a>
## [Critique of Productivity Theater in Modern Workplaces](https://nooneshappy.com/article/appearing-productive-in-the-workplace/) ⭐️ 8.0/10

An opinion piece published on No One's Happy analyzes how modern workplaces, especially in tech, prioritize appearing productive over actual output through elongated documents, AI-generated over-engineering, and performative artifacts. The article resonates deeply with engineers and managers who experience inefficiency from productivity theater, highlighting how AI tools can exacerbate rather than solve workplace bloat. The author notes that requirements documents have grown from one page to twelve, status updates have become bulleted summaries of summaries, and AI-generated over-engineering is praised by non-technical managers while masking inefficiency.

hackernews · diebillionaires · May 6, 16:18 · [Discussion](https://news.ycombinator.com/item?id=48038001)

**Background**: Productivity theater refers to activities that give the illusion of productivity without delivering real value, such as excessive documentation and over-engineered solutions. In software engineering, this has been amplified by generative AI tools like LLMs, which can produce large volumes of code and text that look impressive but may lack substance.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/@olabodeoyeneye/documentation-bloat-at-workplace-perspectives-on-its-avoidance-c0f32b82a277">Documentation Bloat at Workplace: Perspectives on its Avoidance | by 'Bode Oyeneye | Medium</a></li>
<li><a href="https://www.forbes.com/sites/timkeary/2026/04/27/is-software-engineering-cooked-the-future-of-development-post-ai/">Is Software Engineering ‘Cooked’? The Future Of Development ...</a></li>
<li><a href="https://www.acm.org/media-center/2026/april/techbrief-vibe-coding">AI “Vibe Coding” Could Reshape Software Development but Lacks ...</a></li>

</ul>
</details>

**Discussion**: Commenters widely agree with the critique, sharing personal experiences of over-engineered AI architectures and documentation bloat. Some argue that software engineering enables this uniquely due to a culture of non-technical management and tool misuse.

**Tags**: `#workplace culture`, `#software engineering`, `#productivity`, `#management`, `#AI`

---

<a id="item-5"></a>
## [Vibe coding and agentic engineering blur in practice](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/#atom-everything) ⭐️ 8.0/10

Simon Willison reveals in a podcast that vibe coding and agentic engineering, which he once considered distinct, are increasingly overlapping in his own work, causing him unease about code quality and responsibility. This convergence challenges the responsible use of AI in software development, as even experienced engineers may skip code review when AI agents become reliable, potentially compromising production software quality and security. Willison notes that for routine tasks like generating a JSON API endpoint, he trusts Claude Code to produce correct code without reviewing every line, but he questions whether this is responsible for production systems.

rss · Simon Willison · May 6, 14:24 · [Discussion](https://news.ycombinator.com/item?id=48037128)

**Background**: Vibe coding, coined by Andrej Karpathy in 2025, is an AI-assisted approach where programmers accept generated code without deep review. Agentic engineering, also coined by Karpathy, refers to using AI agents as tools within a professional engineering workflow, emphasizing oversight and quality. Willison had previously argued that vibe coding is fine for personal tools but irresponsible for production software, while agentic engineering maintains high standards.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Vibe_coding">Vibe coding</a></li>
<li><a href="https://www.ibm.com/think/topics/agentic-engineering">What is agentic engineering? - IBM</a></li>

</ul>
</details>

**Discussion**: Commenters express skepticism about AI trustworthiness, noting that errors become more subtle and harder to detect, with one pointing out that using lines of code as a metric is problematic. Another highlights that undisciplined engineering practices existed before AI, which are now accelerated.

**Tags**: `#vibe coding`, `#agentic engineering`, `#AI coding tools`, `#software engineering`, `#LLMs`

---

<a id="item-6"></a>
## [Incus 7.0 LTS released with backup API and S3 support](https://lwn.net/Articles/1071469/) ⭐️ 8.0/10

Incus 7.0 LTS has been released, introducing a low-level backup API, built-in S3 operations (replacing MinIO), and removing support for cgroups v1 and xtables. This long-term support release ensures stability for container and VM management through 2031, and the removal of outdated dependencies like cgroups v1 and xtables modernizes the platform. The first two years include bug fixes and minor improvements via point releases, followed by security-only maintenance for the remaining five years. A total of 204 individuals contributed to this release.

rss · LWN.net · May 6, 13:53

**Background**: Incus is a container and virtual-machine manager, forked from LXC/LXD. cgroups v1 is an older kernel resource control mechanism that has been superseded by cgroups v2. xtables (iptables, ip6tables, ebtables) is a legacy firewall framework now replaced by nftables. This release aligns Incus with modern Linux kernel features.

<details><summary>References</summary>
<ul>
<li><a href="https://diveinto.com/blog/cgroups-v1-to-v2">Understanding cgroups: From v1 to v2 and Why It Matters for ...</a></li>
<li><a href="https://dashdash.io/8/xtables-nft">xtables-nft(8): iptables using nftables | Linux Man Page</a></li>

</ul>
</details>

**Tags**: `#Incus`, `#containers`, `#virtual-machines`, `#LTS`, `#open-source`

---

<a id="item-7"></a>
## [ZAYA1-8B: Efficient 8B model trained on AMD hardware](https://www.zyphra.com/post/zaya1-8b) ⭐️ 8.0/10

Zyphra released ZAYA1-8B, an 8-billion-parameter language model pretrained entirely on a cluster of 1,024 AMD MI300x nodes with Pensando Pollara interconnect, using a novel Markovian RSA architecture that achieves performance competitive with models over 100B parameters. This demonstrates that frontier-quality small language models can be trained on non-NVIDIA hardware, reducing dependency on a single vendor and potentially lowering costs for AI research and local deployment. The model uses MoE++ architecture, reasoning-first pretraining, reasoning RL cascade, and a test-time compute method called Markovian RSA. It is designed for local deployment on GPUs with 24-32GB VRAM, with a VLLM fork available.

reddit · r/LocalLLaMA · carbocation · May 6, 19:43 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1t5nll0/zaya18b_frontier_intelligence_density_trained_on/)

**Background**: Training large language models typically requires expensive NVIDIA hardware due to CUDA ecosystem dominance. AMD has been developing its ROCm software stack to support AI workloads, but large-scale pretraining on AMD infrastructure remains rare. Markovian RSA is a novel test-time compute technique that iteratively refines reasoning traces, potentially improving inference quality without increasing model size.

<details><summary>References</summary>
<ul>
<li><a href="https://x.com/ZyphraAI/status/2052103623904309618">Zyphra on X: "Maximum intelligence per parameter was the target. ZAYA1-8B's performance reflects innovations across the full stack: Zyphra’s MoE++ architecture, reasoning-first pretraining, a reasoning RL cascade methodology, and a novel test-time compute method called Markovian RSA. https://t.co/LjNnbkniwj" / X</a></li>
<li><a href="https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/pretrain/setup_tutorial.html">Pretraining with Megatron-LM — Tutorials for AI developers 12.0</a></li>
<li><a href="https://medium.com/@RaajasSode/training-large-language-models-with-an-amd-gpu-85e53616b20c">Training Large Language Models with an AMD GPU - Medium</a></li>

</ul>
</details>

**Discussion**: The community is excited about AMD-based training but skeptical of benchmark comparisons. Some users question the 'frontier' comparisons, while others welcome the innovation and hope for local deployment support. There is also concern about limited compatibility with inference engines like llama.cpp.

**Tags**: `#AMD`, `#small language models`, `#model training`, `#novel architecture`, `#local deployment`

---

<a id="item-8"></a>
## [Qwen 3.6 27B Quantization Quality Comparison via Chess SVG](https://www.reddit.com/r/LocalLLaMA/comments/1t53dhp/quality_comparison_between_qwen_36_27b/) ⭐️ 8.0/10

A Reddit user empirically compared quality degradation across multiple quantizations (BF16, Q8_0, Q6_K, Q5_K_XL, Q4_K_XL, IQ4_XS, IQ3_XXS) of Qwen 3.6 27B using a chessboard SVG generation task with random moves. This comparison provides practical guidance for selecting the best quantization for local LLM deployment on limited VRAM (16 GB), highlighting trade-offs between model size, speed, and output correctness. The task required tracking board state after 7 random moves (half-moves) and generating correct SVG with piece positions and last move highlight, testing both reasoning and code generation abilities.

reddit · r/LocalLLaMA · bobaburger · May 6, 05:10

**Background**: Quantization reduces model weight precision to fit larger models into fewer GPU resources, at the cost of output quality. Common methods include Q8_0 (8-bit), Q6_K (6-bit), and IQ (improved quantization) variants like IQ4_XS and IQ3_XXS, with lower bits meaning more compression but more degradation.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/localmodels/Llama-2-7B-ggml">localmodels/Llama-2-7B-ggml · Hugging Face</a></li>
<li><a href="https://gist.github.com/Artefact2/b5f810600771265fc1e39442288e8ec9">GGUF quantizations overview · GitHub</a></li>
<li><a href="https://tonisagrista.com/blog/2026/quantization/">GGUF quantization guide - Langur Monkey</a></li>

</ul>
</details>

**Discussion**: Commenters praised the thoroughness and visual clarity, but raised concerns about single-run results being affected by statistical noise. Suggestions included testing with multiple runs, trying AWQ quantizations, and using a fork of llama.cpp for better context handling.

**Tags**: `#quantization`, `#Qwen3.6`, `#local LLM`, `#benchmark`, `#SVG generation`

---

<a id="item-9"></a>
## [Qwen3-27B gets 2.5x speed with MTP graft on Unsloth UD XL GGUF](https://www.reddit.com/r/LocalLLaMA/comments/1t5ageq/qwen3627b_with_mtp_grafted_on_unsloth_ud_xl_25x/) ⭐️ 8.0/10

A user grafted Multi-Token Prediction (MTP) draft heads onto a quantized Qwen3-27B GGUF model using Unsloth's UD XL quantization and a custom build of llama.cpp that includes the unmerged PR #22673, achieving 2-2.5x token throughput improvement. This optimization significantly speeds up local LLM inference for the 27B parameter model, making it practical for users with limited hardware like partial CPU offload setups, and demonstrates a viable way to enable MTP on quantized models before official support lands in llama.cpp. The base model uses Unsloth's UD XL quantization (e.g., Q4_K_XL) while the three MTP layers are kept at Q8_0 to preserve speculative accuracy; all GGUF files and a conversion script are shared on Hugging Face for replication.

reddit · r/LocalLLaMA · havenoammo · May 6, 11:45

**Background**: Multi-Token Prediction (MTP) is a training technique where a language model predicts multiple future tokens simultaneously, improving inference efficiency through speculative decoding. GGUF is a binary format optimized for running quantized models locally with executors like llama.cpp. Unsloth's UD XL quantization reduces model size while maintaining quality. The PR #22673 in llama.cpp adds MTP support but has not yet been merged into the main branch.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2404.19737">[2404.19737] Better & Faster Large Language Models via Multi-token Prediction</a></li>
<li><a href="https://huggingface.co/docs/hub/gguf">GGUF · Hugging Face</a></li>
<li><a href="https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs">Unsloth Dynamic 2.0 GGUFs | Unsloth Documentation</a></li>

</ul>
</details>

**Discussion**: Comments were overwhelmingly positive, with users reporting 2-2.5x speedups on various hardware including RTX Pro 6000 and AMD ROCm (RDNA 3.5). Some users noted the benefit for partial CPU offload scenarios and appreciated the shared conversion script for grafting MTP onto other models.

**Tags**: `#LLM inference`, `#Multi-Token Prediction`, `#GGUF quantization`, `#llama.cpp`, `#optimization`

---

<a id="item-10"></a>
## [Running Qwen3.6 27B NVFP4 with MTP on RTX 5090 at 200k Context](https://www.reddit.com/r/LocalLLaMA/comments/1t5dya8/qwen36_27b_nvfp4_mtp_on_a_single_rtx_5090_200k/) ⭐️ 8.0/10

A user successfully runs the Qwen3.6-27B-NVFP4 model with Multi-Token Prediction (MTP) speculative decoding on a single RTX 5090 GPU, achieving 200k context length using vLLM with flashinfer attention backend. This demonstration shows that large language models with 27B parameters can run on consumer hardware with high context lengths and decent performance, making advanced AI more accessible and practical for local deployment. The configuration uses NVFP4 quantization (compressed-tensors), KV cache dtype fp8_e4m3, MTP with 3 speculative tokens, and max-model-len set to 230400. The user only validated up to 200k context, not the full 262k.

reddit · r/LocalLLaMA · Maheidem · May 6, 14:05

**Background**: NVFP4 is a 4-bit floating-point quantization format from NVIDIA that preserves higher dynamic range than integer quantization. Multi-Token Prediction (MTP) is a speculative decoding method where the target model itself predicts multiple future tokens, eliminating the need for a separate draft model and potentially doubling or tripling inference throughput. FlashInfer is a high-performance CUDA kernel library for attention operations, used in vLLM to accelerate prefill and decode phases. vLLM is an open-source LLM serving framework that supports various quantization and decoding optimizations.

<details><summary>References</summary>
<ul>
<li><a href="https://build.nvidia.com/spark/nvfp4-quantization">NVFP4 Quantization | DGX Spark</a></li>
<li><a href="https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp/">MTP (Multi-Token Prediction) - vLLM</a></li>
<li><a href="https://github.com/flashinfer-ai/flashinfer">GitHub - flashinfer-ai/flashinfer: FlashInfer: Kernel Library ... Attention Backend Feature Support - vLLM FlashAttention and FlashInfer | vllm-project/vllm | DeepWiki FlashInfer on ROCm: High‑Throughput Prefill Attention via ... FlashInfer: Efficient and Customizable Attention Engine for ... FlashInfer Attention Backend | NVIDIA/TensorRT-LLM | DeepWiki</a></li>

</ul>
</details>

**Discussion**: Commenters praised the performance, with one noting that running ~30B dense models at Q4 with 128k+ context on consumer hardware is a revolution. Another user reported similar settings on a 5090 achieving 75-130 t/s with thinking enabled. There was also debate about disabling thinking and whether the setup constitutes 'AI slop'.

**Tags**: `#LLM`, `#vLLM`, `#quantization`, `#RTX5090`, `#MTP`

---

<a id="item-11"></a>
## [Anthropic Commits $200 Billion to Google Cloud Over 5 Years](https://www.theinformation.com/articles/anthropic-commits-spending-200-billion-googles-cloud-chips?utm_source=chatgpt.com) ⭐️ 8.0/10

Anthropic has committed to spending $200 billion on Google Cloud over the next five years, a commitment that represents more than 40% of Google Cloud's disclosed backlog. This was revealed by The Information and caused Alphabet's stock to rise about 2% after hours. This massive commitment signals a deep strategic alliance between Anthropic and Google, solidifying Google Cloud's position in AI infrastructure and intensifying competition with other cloud providers like AWS and Microsoft Azure. It also underscores the enormous capital requirements for training and deploying advanced AI models. In April 2026, the two companies also signed an agreement with Broadcom to secure multiple gigawatts of TPU computing power, expected to come online from 2027. Additionally, Alphabet plans to invest up to $40 billion in Anthropic at a valuation of $350 billion, further deepening their partnership.

telegram · zaihuapd · May 6, 03:53

**Background**: Anthropic is an AI research and safety company best known for its Claude series of large language models. Google Cloud's TPUs (Tensor Processing Units) are custom-designed AI accelerator chips that optimize performance for training and inference. A cloud provider's backlog refers to committed customer spending that has not yet been recognized as revenue, and this commitment represents a significant portion of Google Cloud's future revenue.

<details><summary>References</summary>
<ul>
<li><a href="https://cloud.google.com/tpu">Tensor Processing Units (TPUs) | Google Cloud</a></li>

</ul>
</details>

**Tags**: `#Anthropic`, `#Google Cloud`, `#AI Infrastructure`, `#Cloud Computing`, `#Business Strategy`

---

<a id="item-12"></a>
## [DeepSeek Reportedly in Talks for $45B Valuation Funding](https://www.bloomberg.com/news/articles/2026-05-06/china-chip-fund-in-talks-to-lead-mega-deepseek-funding-ft-says) ⭐️ 8.0/10

DeepSeek is reportedly in talks for its first major external funding round led by China's National Integrated Circuit Industry Investment Fund, with a valuation of approximately $45 billion. This funding would mark a significant state-backed investment in Chinese AI, demonstrating deepening government involvement in core AI companies and potentially accelerating DeepSeek's development amid US chip export restrictions. The funding round is led by the National Integrated Circuit Industry Investment Fund (also known as the Big Fund), and this is DeepSeek's first major external capital raise. The $45 billion valuation reflects DeepSeek's rapid rise since its founding in 2023.

telegram · zaihuapd · May 6, 06:28

**Background**: DeepSeek is a Chinese AI company founded in 2023 by Liang Wenfeng, originally funded by hedge fund High-Flyer. It gained global attention in early 2025 with its R1 model, which achieved performance comparable to GPT-4 at a fraction of the training cost. The National Integrated Circuit Industry Investment Fund is a state-backed fund aimed at boosting China's semiconductor self-sufficiency. This potential investment signals China's strategic push to strengthen its AI capabilities despite US technology restrictions.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></li>
<li><a href="https://en.wikipedia.org/wiki/National_Integrated_Circuit_Industry_Investment_Fund">National Integrated Circuit Industry Investment Fund</a></li>

</ul>
</details>

**Tags**: `#DeepSeek`, `#AI funding`, `#China`, `#semiconductor`, `#venture capital`

---

<a id="item-13"></a>
## [Google Chrome silently downloads 4GB AI model without consent](https://www.tomshardware.com/tech-industry/cyber-security/google-chrome-silently-downloads-4gb-ai-model-to-your-device-without-permission-report-claims-researcher-says-practice-may-violate-eu-law-waste-thousands-of-kilowatts-of-energy) ⭐️ 8.0/10

Security researcher Alexander Hanff reported that Google Chrome silently downloads a 4GB Gemini Nano AI model (weights.bin) to compatible devices without user permission, and the file reappears even after manual deletion. This practice could violate EU GDPR and other privacy laws, and may waste significant energy and bandwidth, potentially affecting billions of users. It highlights the broader trend of tech companies forcefully deploying AI features without user consent. The model file is approximately 4GB, and the researcher estimates that distributing it to 1 billion users could generate up to 60,000 tonnes of carbon emissions. Similar behavior was also reported for Anthropic's Claude app.

telegram · zaihuapd · May 6, 11:15

**Background**: Gemini Nano is a lightweight AI model developed by Google DeepMind, designed to run on-device for tasks like summarization and smart replies. Chrome has been integrating AI features, but this silent download raises concerns about user control and data privacy. The file 'weights.bin' contains the trained neural network parameters.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">Gemini (language model) - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#google-chrome`, `#AI`, `#GDPR`, `#security`

---

<a id="item-14"></a>
## [EU Plans Mandatory Removal of Huawei, ZTE Equipment from Telecom Networks](https://t.me/zaihuapd/41247) ⭐️ 8.0/10

The European Commission is considering new regulations that would mandate all EU member states to phase out Huawei and ZTE equipment from their telecom and broadband infrastructure, upgrading previous non-binding recommendations to legally enforceable requirements. This marks a significant escalation in EU cybersecurity policy, potentially reshaping telecom supply chains in Europe and affecting global geopolitics. If enacted, it could force operators to replace existing infrastructure, impacting costs and network operations, while also influencing other regions' approaches to high-risk vendors. The new rules would also tighten external infrastructure funding by stopping loans to non-EU countries using Huawei equipment. Non-compliant member states could face investigations and financial penalties if they fail to remove designated equipment on time.

telegram · zaihuapd · May 6, 14:00

**Background**: In 2020, the EU adopted the 5G Cybersecurity Toolbox, a set of non-binding measures to address risks from high-risk vendors like Huawei and ZTE. The toolbox included recommendations to restrict or exclude such vendors from 5G networks, but implementation varied across member states. The proposed regulation aims to create a uniform, binding approach across the EU.

<details><summary>References</summary>
<ul>
<li><a href="https://digital-strategy.ec.europa.eu/en/library/eu-toolbox-5g-security">The EU toolbox for 5G security - Shaping Europe’s digital ...</a></li>
<li><a href="https://www.telecomrevieweurope.com/articles/reports-and-coverage/how-the-eus-5g-toolbox-shapes-secure-connectivity/">How the EU’s 5G Toolbox Shapes Secure Connectivity</a></li>
<li><a href="https://eutechloop.com/eus-plans-to-reduce/">EU’s plans to reduce dependency on high-risk vendors</a></li>

</ul>
</details>

**Tags**: `#Huawei`, `#EU`, `#telecom regulation`, `#cybersecurity`, `#geopolitics`

---