---
layout: default
title: "Horizon Summary: 2026-07-17 (EN)"
date: 2026-07-17
lang: en
---

> From 43 items, 8 important content pieces were selected

---

1. [Bonsai 27B runs locally on iPhone with 1-bit quantization](#item-1) ⭐️ 9.0/10
2. [Huawei Ascend 950 Supernode Debuts, Claims 6.7x Compute vs Nvidia](#item-2) ⭐️ 9.0/10
3. [AWS Billing Glitch Shows $1.7B Estimated Charges](#item-3) ⭐️ 8.0/10
4. [JWST Detects Atmosphere on Rocky Exoplanet LHS 1140b](#item-4) ⭐️ 8.0/10
5. [Mozilla Report: Open Source AI Models Surge in Market Share](#item-5) ⭐️ 8.0/10
6. [Kaggle competition reveals AI submission and judge inconsistencies](#item-6) ⭐️ 8.0/10
7. [DeepSeek V4 Flash on RTX 5090 with 1M Context in llama.cpp](#item-7) ⭐️ 8.0/10
8. [Kimi K3: Open-Source 2.8T Model Tops Frontend Code Arena](#item-8) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Bonsai 27B runs locally on iPhone with 1-bit quantization](https://www.reddit.com/r/LocalLLaMA/comments/1uyz9n2/bonsai_27b_runs_locally_on_an_iphone_a_27b_model/) ⭐️ 9.0/10

PrismML released Bonsai 27B, a 1-bit quantized version of Qwen3.6-27B, that runs locally on an iPhone with only 3.9GB memory footprint and retains approximately 90% of the FP16 benchmark performance. This breakthrough demonstrates that large language models with 27 billion parameters can now run on consumer mobile devices, drastically reducing the barrier to private, on-device AI inference. It also showcases the viability of extreme quantization techniques for practical deployment. The model uses binary g128 quantization, where each weight is a single sign bit and groups of 128 weights share one FP16 scale, achieving ~1.125 bits per weight without high-precision escape hatches. Even embeddings, attention/MLP projections, and the LM head are binarized, which is unusual for 1-bit schemes.

reddit · r/LocalLLaMA · /u/ElmBark · Jul 17, 13:08

**Background**: Quantization reduces the precision of model weights to lower bits, trading a small accuracy loss for large reductions in memory and compute. Standard 16-bit \(FP16\) 27B models require ~54GB, far exceeding phone memory. 1-bit quantization pushes compression to the extreme, representing each weight as either +1 or -1 with a shared scale, making on-device deployment feasible.

<details><summary>References</summary>
<ul>
<li><a href="https://prismml.com/news/prismml-releases-bonsai-27b">PrismML — PrismML Announces 1-bit Bonsai 27B - The First 27B Model to ...</a></li>
<li><a href="https://prismml.com/news/bonsai-27b">PrismML — Announcing Bonsai 27B: The First 27B-Class Model to ...</a></li>
<li><a href="https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit">prism-ml/Bonsai-27B-mlx-1bit · Hugging Face</a></li>

</ul>
</details>

**Tags**: `#quantization`, `#mobile inference`, `#LLM compression`, `#binary weights`, `#local LLM`

---

<a id="item-2"></a>
## [Huawei Ascend 950 Supernode Debuts, Claims 6.7x Compute vs Nvidia](https://www.ithome.com/0/978/019.htm) ⭐️ 9.0/10

At WAIC 2026, Huawei publicly demonstrated the Ascend 950 supernode \(Atlas 950 SuperPoD\), based on its proprietary Lingqu interconnect protocol and supernode architecture, scaling to 1,024 cards and delivering 1 EFLOPS FP8 and 2 EFLOPS FP4 compute with 256 TB unified memory. According to a BOC International report, its total compute is 6.7 times that of Nvidia&\#x27;s equivalent NVL144 system. This announcement signals Huawei&\#x27;s continued push to challenge Nvidia&\#x27;s dominance in AI computing hardware, particularly for large-scale training and inference. If verified, the 6.7x performance claim could reshape the competitive landscape and accelerate adoption of domestic AI chips in China. The Ascend 950 supernode uses Huawei&\#x27;s self-developed Lingqu \(UnifiedBus\) interconnect protocol, which replaces PCIe, NVLink, and RDMA with a five-layer protocol stack supporting up to 8,192 cards without convergence. The system also features FP8 and FP4 precision formats, commonly used for efficient AI inference and low-precision training.

telegram · zaihuapd · Jul 17, 10:27

**Background**: Huawei&\#x27;s Lingqu \(UnifiedBus\) interconnect protocol was officially released in September 2025 at HUAWEI CONNECT 2025, aiming to solve the interconnect challenges of large-scale computing resources. FP8 and FP4 are low-precision floating-point formats widely used in AI workloads to reduce memory bandwidth and accelerate computation while maintaining acceptable accuracy. The Ascend 950 is the latest in Huawei&\#x27;s supernode series, following the Ascend 384 which has already been deployed in over 750 commercial systems across internet, telecom, and finance sectors.

<details><summary>References</summary>
<ul>
<li><a href="https://baike.baidu.com/item/%E7%81%B5%E8%A1%A2/66774401">灵衢 - 百度百科</a></li>
<li><a href="https://www.toutiao.com/article/7551352889764020755/">华为全联接大会 2025：发布灵衢互联协议与多系列超节点产品，引领 AI ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Minifloat">Minifloat - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#Huawei`, `#Ascend 950`, `#AI Hardware`, `#Supercomputer`, `#Compute`

---

<a id="item-3"></a>
## [AWS Billing Glitch Shows $1.7B Estimated Charges](https://news.ycombinator.com/item?id=48945241) ⭐️ 8.0/10

On July 16, 2026, a bug in AWS Cost Explorer caused unit pricing errors, displaying estimated bills as high as $1.7 billion for some customers whose normal usage is under $5. This high-profile billing error erodes customer trust and highlights the critical importance of accurate metering and pricing in cloud services, affecting potentially millions of AWS users. The root cause was a unit conversion error where AWS billed per byte instead of per gigabyte, inflating charges by roughly 1 billion times; actual invoices and Cost and Usage Reports remained accurate.

hackernews · nprateem · Jul 17, 09:42

**Background**: AWS Cost Explorer uses estimated billing data based on metered usage. Cloud providers typically charge per gigabyte \(GB\) for storage and data transfer. A confusion between decimal prefixes \(GB = 10^9 bytes\) and binary prefixes \(GiB = 2^30 bytes\) or a simple unit miss can cause massive errors. In this case, a pricing plan defaulted to bytes instead of GB.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Binary_prefix">Binary prefix - Wikipedia</a></li>
<li><a href="https://thenextweb.com/news/aws-billing-bug-billion-dollar-estimates">An AWS billing bug sent users estimated charges of up to $2.5 ... - TNW</a></li>
<li><a href="https://techcrunch.com/2026/07/17/amazon-fixing-bug-that-billed-some-aws-customers-billions-of-dollars/">Amazon fixing bug that billed some AWS customers billions of ...</a></li>

</ul>
</details>

**Discussion**: An ex-AWS engineer shared firsthand experience from a past similar error, confirming it was a unit mismatch. Many users reported shock and adrenaline rushes upon seeing astronomical bills, while others noted that the actual charges were never affected and that AWS responded quickly.

**Tags**: `#AWS`, `#billing`, `#cloud computing`, `#bug`, `#outage`

---

<a id="item-4"></a>
## [JWST Detects Atmosphere on Rocky Exoplanet LHS 1140b](https://www.bbc.com/news/articles/cy4kdd1e0ejo) ⭐️ 8.0/10

NASA&\#x27;s James Webb Space Telescope has detected an atmosphere on the rocky exoplanet LHS 1140b, which orbits in the habitable zone of its red dwarf star, ruling out the previous mini-Neptune classification. This is the first confirmed atmosphere on a potentially habitable Earth-like planet, marking a major milestone in exoplanet research and bringing us closer to identifying signs of life beyond Earth. LHS 1140b is about 5.6 times Earth&\#x27;s mass and 70% larger in radius, located 48 light-years away. The detection was made using JWST&\#x27;s emission spectroscopy as the planet passed behind its star.

hackernews · neversaydie · Jul 17, 14:06 · [Discussion](https://news.ycombinator.com/item?id=48947560)

**Background**: LHS 1140b was discovered in 2017 by the MEarth Project and orbits a red dwarf star. Red dwarfs are cooler and have closer habitable zones, often subjecting planets to intense stellar radiation. Mini-Neptunes are exoplanets with a thick atmosphere and a rocky core, unlike rocky Earth-like planets. JWST&\#x27;s spectroscopy can distinguish between these types by analyzing the planet&\#x27;s atmospheric composition.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/LHS_1140_b">LHS 1140 b - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/LHS_1140">LHS 1140 - Wikipedia</a></li>
<li><a href="https://science.nasa.gov/exoplanet-catalog/lhs-1140-b/">LHS 1140 b - Science@NASA</a></li>

</ul>
</details>

**Discussion**: Commenters expressed initial skepticism about a rocky planet retaining atmosphere around a red dwarf, but later acknowledged that JWST data ruled out the mini-Neptune hypothesis. Some discussed the Fermi paradox and the need for a solar lens telescope, while others noted that 48 light-years is relatively close and speculated about near-light-speed propulsion.

**Tags**: `#exoplanet`, `#atmosphere`, `#JWST`, `#astronomy`, `#habitable-zone`

---

<a id="item-5"></a>
## [Mozilla Report: Open Source AI Models Surge in Market Share](https://stateofopensource.ai/) ⭐️ 8.0/10

Mozilla published a presentation analyzing the state of open source AI, showing that open models now account for 63% of tokens processed on OpenRouter, a shift from 40% just four months ago. This rapid growth indicates that open source models are challenging the dominance of closed-source leaders like Anthropic and OpenAI, potentially reshaping the AI industry&\#x27;s competitive landscape. The presentation has been criticized for its low-quality, LLM-generated prose, but the underlying data highlights a fivefold increase in open model token processing over four months.

hackernews · rellem · Jul 17, 14:31 · [Discussion](https://news.ycombinator.com/item?id=48947825)

**Background**: Open source AI models, such as Llama and Mistral, are freely available for use and modification, unlike closed models like GPT-4. The shift towards open models could lower costs and accelerate innovation, as companies like Apple can optimize them for on-device use.

**Discussion**: Community comments express mixed sentiments: some celebrate the rise of open models as a threat to closed-source companies, while others criticize the presentation&\#x27;s AI-generated content as low-quality and note that the debate itself elevates the topic&\#x27;s importance.

**Tags**: `#open source AI`, `#community discussion`, `#model market share`, `#LLM trends`

---

<a id="item-6"></a>
## [Kaggle competition reveals AI submission and judge inconsistencies](https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/724918#3498423) ⭐️ 8.0/10

A Kaggle community discussion has highlighted that in the &\#x27;Measuring AGI&\#x27; competition, submissions and evaluations are being handled by AI, leading to inconsistencies and prompt injection attacks where competitors can trick AI judges into declaring them winners. This raises serious concerns about the integrity of AI-driven competitions and evaluations, as AI judges can be easily manipulated and lack common sense, potentially undermining trust in automated assessment systems across industries. Specifically, community members report that AI judges can be prompt injected to award wins, and that submissions are often generated entirely by AI with minimal human input, shifting focus from human skill to idea execution or insider advantage.

hackernews · twerkmeister · Jul 17, 11:30 · [Discussion](https://news.ycombinator.com/item?id=48946010)

**Background**: Prompt injection is a security exploit where crafted inputs cause AI models to behave unexpectedly, bypassing safeguards. LLM-as-a-Judge systems are known to exhibit biases and can be unreliable. Kaggle is a data science competition platform that traditionally involved human skill, but recent events show increasing reliance on AI for both submissions and judging.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Prompt_injection_attack">Prompt injection attack</a></li>
<li><a href="https://arxiv.org/abs/2604.23178">[2604.23178] Judging the Judges: A Systematic Evaluation of Bias ...</a></li>
<li><a href="https://www.techtimes.com/articles/318360/20260614/when-ai-grades-ai-why-smarter-models-are-not-fairer-judges-their-own-work.htm">When AI Grades AI: Why Smarter Models Are Not Fairer Judges of Their ...</a></li>

</ul>
</details>

**Discussion**: Commenters express frustration that AI has &\#x27;killed&\#x27; fair hackathons, with one noting that prompt injection allows winners to be declared artificially. Others argue that Kaggle has always had issues with black-box models and brute-force methods, so this is not entirely new.

**Tags**: `#AI ethics`, `#Kaggle`, `#competition integrity`, `#prompt injection`, `#AI evaluation`

---

<a id="item-7"></a>
## [DeepSeek V4 Flash on RTX 5090 with 1M Context in llama.cpp](https://www.reddit.com/r/LocalLLaMA/comments/1uz5w3y/deepseek_v4_flash_on_5090_in_llamacpp_with_1/) ⭐️ 8.0/10

A user shared benchmarks and configuration for running DeepSeek V4 Flash, a 284B-parameter mixture-of-experts model, on an RTX 5090 with a full 1 million token context window using llama.cpp, achieving prefill speeds of ~650–700 tokens/s and decode speeds of ~17 tokens/s. This demonstrates that large MoE models with 1M context are now practically usable on high-end consumer hardware, opening up local inference for long-context tasks like document analysis and code generation without relying on cloud APIs. The user used a Q8\_K\_XL quantized GGUF model from Unsloth and reported a loading time of 32 seconds; they noted that speed is not yet as impressive as Qwen models but there is room for further optimization in llama.cpp.

reddit · r/LocalLLaMA · /u/Shoddy\_Bed3240 · Jul 17, 17:14

**Background**: DeepSeek V4 Flash is a preview model in the DeepSeek V4 series, a Mixture-of-Experts \(MoE\) architecture with 284B total parameters but only 13B activated per token, making it efficient for inference. It supports a 1M token context window. llama.cpp is an open-source inference engine that runs LLMs locally on consumer hardware using the GGUF format, which optimizes model loading and quantization.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash">deepseek -ai/ DeepSeek - V 4 - Flash · Hugging Face</a></li>
<li><a href="https://en.wikipedia.org/wiki/Llama.cpp">Llama.cpp</a></li>
<li><a href="https://en.wikipedia.org/wiki/GGUF">GGUF - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#deepseek`, `#llama.cpp`, `#local-llm`, `#inference`, `#benchmark`

---

<a id="item-8"></a>
## [Kimi K3: Open-Source 2.8T Model Tops Frontend Code Arena](https://www.kimi.com/blog/kimi-k3) ⭐️ 8.0/10

Moonshot AI released Kimi K3, the world&\#x27;s first open-source 2.8 trillion parameter model, which tops the Frontend Code Arena leaderboard with a score of 1679, surpassing Claude Fable 5 in frontend coding tasks. This release marks a significant milestone for open-source AI, demonstrating that a model with novel architecture \(Kimi Delta Attention and Attention Residuals\) can rival top proprietary models on specific benchmarks, potentially accelerating adoption and innovation in the open-source community. Kimi K3 is a sparse Mixture-of-Experts model with 2.8 trillion parameters, built on Kimi Delta Attention \(a hybrid linear attention mechanism\) and Attention Residuals, featuring native vision and a 1 million token context window; API pricing is $0.30 per million tokens for cache hits, $3.00 for cache misses, and $15.00 for output, with full model weights to be released in July 2026.

telegram · zaihuapd · Jul 17, 00:02

**Background**: Kimi Delta Attention \(KDA\) is a linear attention mechanism that improves upon Gated DeltaNet with per-channel diagonal gating, enabling more efficient memory management than traditional full attention. Attention Residuals \(AttnRes\) allow each transformer layer to selectively aggregate information from all previous layers, enhancing long-range dependencies. The model uses a sparse MoE structure to achieve 2.8T parameters with lower computational cost than a dense model of similar size.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2510.26692">[2510.26692] Kimi Linear: An Expressive, Efficient Attention ... GitHub - MoonshotAI/Kimi-Linear Kimi K3 - Kimi API Platform Kimi Linear: An Expressive, Efficient Attention Architecture Moonshot AI Releases Kimi K3: A 2.8 Trillion Parameter Open ... GitHub - hwilner/kimi-delta-attention: Educational ... Kimi K3 (Moonshot AI) - Cloudflare Docs</a></li>
<li><a href="https://github.com/MoonshotAI/Kimi-Linear">GitHub - MoonshotAI/Kimi-Linear</a></li>
<li><a href="https://arena.ai/leaderboard/code/html">HTML Code AI Leaderboard - Best AI Models for HTML Generation</a></li>

</ul>
</details>

**Tags**: `#open-source`, `#large language model`, `#AI`, `#deep learning`, `#model architecture`

---