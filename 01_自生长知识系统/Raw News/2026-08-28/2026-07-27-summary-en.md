---
layout: default
title: "Horizon Summary: 2026-07-27 (EN)"
date: 2026-07-27
lang: en
---

> From 32 items, 10 important content pieces were selected

---

1. [Moonshot AI Opens Kimi K3: First 2.8 Trillion Parameter Open Model](#item-1) ⭐️ 10.0/10
2. [vLLM v0.26.0: Major Release with Inkling Model and DeepSeek-V4 Tuning](#item-2) ⭐️ 9.0/10
3. [Anthropic calls for mandatory safety testing of capable AI models](#item-3) ⭐️ 9.0/10
4. [Google teases Gemini 4 as most ambitious pre-training yet](#item-4) ⭐️ 9.0/10
5. [Unpatched RCE Vulnerability in Fastjson2 Affects All Versions](#item-5) ⭐️ 9.0/10
6. [Judge Rejects Google&\#x27;s DMCA Defense Against Scraping](#item-6) ⭐️ 8.0/10
7. [Hazard Pointers Proposed for Linux Kernel](#item-7) ⭐️ 8.0/10
8. [Solo Evaluation Finds Left-Leaning Bias in Six Frontier LLMs](#item-8) ⭐️ 8.0/10
9. [Changxin Memory surges 471% on STAR Market debut](#item-9) ⭐️ 8.0/10
10. [China Begins Mass Production of Domestic DUV Lithography Tools](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Moonshot AI Opens Kimi K3: First 2.8 Trillion Parameter Open Model](https://huggingface.co/moonshotai/Kimi-K3) ⭐️ 10.0/10

Moonshot AI has open-sourced Kimi K3, a 2.8 trillion parameter model with 104 billion active parameters, making it the first openly available model at the 3-trillion scale. It introduces Kimi Delta Attention \(KDA\), Attention Residuals \(AttnRes\), and Stable LatentMoE, supporting multi-modal inputs and a 1 million token context window. Kimi K3&\#x27;s open release marks a milestone in AI by providing a frontier-scale model to the community, potentially accelerating research and applications in long-context reasoning, multimodal understanding, and agentic tasks. Its efficient architecture \(2.5x improvement over K2\) demonstrates that massive models can be both powerful and practical. The model uses 896 experts with 16 activated per token under the Stable LatentMoE framework, and supports MXFP4 quantization for efficient inference. Benchmarks like GPQA Diamond, BrowseComp, and DeepSWE show it competes with proprietary models such as GPT-5.6 Sol and Claude Fable 5.

telegram · zaihuapd · Jul 27, 15:15

**Background**: Large language models often use Mixture-of-Experts \(MoE\) to scale parameters while keeping computation manageable. Kimi K3&\#x27;s KDA is a linear attention mechanism that improves memory efficiency, and Stable LatentMoE further reduces routing and expert compute costs by projecting to a lower-dimensional latent space. MXFP4 is a 4-bit floating-point quantization format that balances accuracy and speed.

<details><summary>References</summary>
<ul>
<li><a href="https://jianyuh.github.io/attention/2025/12/13/KDA.html">Linear Attention : Kimi Delta Attention | Jianyu Huang’s Blog</a></li>
<li><a href="https://arxiv.org/abs/2601.18089">[2601.18089] LatentMoE: Toward Optimal Accuracy per FLOP and Parameter in Mixture of Experts</a></li>
<li><a href="https://huggingface.co/blog/RakshitAralimatti/learn-ai-with-me">What’s MXFP4? The 4-Bit Secret Powering OpenAI’s GPT‑OSS Models on Modest Hardware</a></li>

</ul>
</details>

**Tags**: `#人工智能`, `#大语言模型`, `#开源`, `#MoonshotAI`, `#Kimi K3`

---

<a id="item-2"></a>
## [vLLM v0.26.0: Major Release with Inkling Model and DeepSeek-V4 Tuning](https://github.com/vllm-project/vllm/releases/tag/v0.26.0) ⭐️ 9.0/10

vLLM v0.26.0 introduces the Inkling model family with full support \(base modeling, CUDA graphs, attention, speculative decoding, LoRA, and quantization\), delivers DeepSeek-V4 performance optimizations including a specialized routing kernel and fused topk bias, adds fp32 lm\_head via head\_dtype, and enables flexible attention backends per KV-cache group. This release significantly enhances LLM inference flexibility and performance, particularly for hybrid models and large-scale deployments. The Inkling model support and DeepSeek-V4 optimizations impact a broad range of users, from researchers to production engineers, by reducing latency and improving accuracy. The release includes 411 commits from 212 contributors, with notable technical additions like Hopper FA4 relative attention, piecewise CUDA graph support, and a Rust frontend for multimodal video and audio. KV offloading and tiered secondary storage have matured, and Transformers 5.13 migration adds several new model backends.

github · khluu · Jul 27, 01:06

**Background**: vLLM is an open-source high-throughput LLM inference engine. The Inkling model is a 975B-parameter multimodal MoE model from Thinking Machines Lab with 41B active parameters and 256k context length. FlashAttention-4 \(FA4\) is a recent attention algorithm optimized for NVIDIA Hopper and Blackwell GPUs, improving memory efficiency and speed.

<details><summary>References</summary>
<ul>
<li><a href="https://inkling-model.com/">Inkling Model : Architecture, Capabilities, Context &amp; Access</a></li>
<li><a href="https://docs.vllm.ai/en/latest/api/vllm/model_executor/layers/fused_moe/router/fused_topk_bias_router/">fused_topk_bias_router - vLLM</a></li>
<li><a href="https://modal.com/blog/reverse-engineer-flash-attention-4">We reverse-engineered Flash Attention 4</a></li>

</ul>
</details>

**Tags**: `#vLLM`, `#LLM Inference`, `#DeepSeek`, `#Performance Optimization`, `#CUDA`

---

<a id="item-3"></a>
## [Anthropic calls for mandatory safety testing of capable AI models](https://www.anthropic.com/news/position-open-weights-models) ⭐️ 9.0/10

Anthropic published a policy statement supporting mandatory safety testing for all sufficiently capable AI models, including open-weights models, which critics argue effectively bans open-weights releases. This stance could influence AI regulation and potentially restrict the development and distribution of open-weights models, impacting open-source AI communities and smaller developers. Anthropic claims it does not advocate for a ban on open-weights models, but requires mandatory safety testing. Critics question who administers the tests, the cost, and potential for refusal, comparing it to de facto bans used historically.

hackernews · surprisetalk · Jul 27, 22:03 · [Discussion](https://news.ycombinator.com/item?id=49076057)

**Background**: Open-weights models are AI models whose core components are publicly released, allowing anyone to download, inspect, modify, and run them on their own infrastructure. Anthropic is a leading AI company focused on safety, and its policy positions often carry weight in regulatory debates. The debate centers on balancing innovation and openness with safety concerns about misuse of powerful AI.

<details><summary>References</summary>
<ul>
<li><a href="https://hai.stanford.edu/ai-definitions/what-is-an-open-weight-model">What is an Open-Weight Model? - Stanford HAI</a></li>
<li><a href="https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/">Open Weights and American AI Leadership</a></li>

</ul>
</details>

**Discussion**: Community comments express strong skepticism and accusations that Anthropic uses safety as a pretext to protect its proprietary models. Some point out inconsistencies in Anthropic&\#x27;s support for hardware bans while opposing model restrictions, and others see the policy as a competitive move against open-weights alternatives like DeepSeek.

**Tags**: `#AI safety`, `#open-weights models`, `#regulation`, `#Anthropic`, `#policy debate`

---

<a id="item-4"></a>
## [Google teases Gemini 4 as most ambitious pre-training yet](https://9to5google.com/2026/07/26/google-gemini-4-teases/) ⭐️ 9.0/10

Google CEO Sundar Pichai announced that Gemini 4 is currently in training, describing it as the company&\#x27;s most ambitious pre-training project to date, with an expected launch by the end of 2026. This signals Google&\#x27;s continued commitment to frontier AI development, potentially pushing the capabilities of large language models significantly forward and intensifying competition in the AI industry. Pichai emphasized that Google will prioritize compute allocation for frontier AGI research, and Gemini 3.x Flash series will maintain near-monthly updates focusing on coding intelligence.

telegram · zaihuapd · Jul 27, 04:06

**Background**: Large language models like Gemini undergo a pre-training phase where they learn from vast amounts of text data. Google&\#x27;s Gemini series has been competing with models like OpenAI&\#x27;s GPT and Anthropic&\#x27;s Claude. This latest iteration aims to be a major leap forward.

**Tags**: `#AI`, `#Gemini 4`, `#Google`, `#large language models`, `#pre-training`

---

<a id="item-5"></a>
## [Unpatched RCE Vulnerability in Fastjson2 Affects All Versions](https://mp.weixin.qq.com/s/LJaul1jNjK9pXRAkoUiMEA) ⭐️ 9.0/10

On July 27, security firm Chaitin Technology disclosed a remote code execution \(RCE\) vulnerability in Alibaba&\#x27;s Fastjson2 Java JSON library, affecting all versions up to 2.0.62. The vulnerability allows attackers to bypass AutoType type checking via malicious JSON data and execute arbitrary code. No official patch has been released yet. This is the second critical vulnerability in the Fastjson family within a month, highlighting ongoing security risks in widely-used Java JSON processing libraries. Many applications rely on Fastjson2, so unpatched systems are at high risk of remote compromise. The maintainer has confirmed the issue, but the fix branch \(PR \#7695\) was closed and not merged into the main branch. Complete vulnerability details and exploit code have not been publicly disclosed. Until an official fix is available, users are advised to completely disable AutoType in configurations.

telegram · zaihuapd · Jul 27, 10:31

**Background**: Fastjson2 is a high-performance JSON library for Java developed by Alibaba. It supports features like automatic type deserialization via AutoType, which can be exploited if not properly secured. Previous versions of Fastjson have also had similar RCE vulnerabilities, making this a recurring issue for the library.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/alibaba/fastjson2">GitHub - alibaba/fastjson2: FASTJSON2 is a Java JSON library with ...</a></li>
<li><a href="https://alibaba.github.io/fastjson2/">FASTJSON 2.0介绍 | fastjson2</a></li>

</ul>
</details>

**Tags**: `#security`, `#vulnerability`, `#fastjson2`, `#rce`, `#java`

---

<a id="item-6"></a>
## [Judge Rejects Google&\#x27;s DMCA Defense Against Scraping](https://www.techdirt.com/2026/07/27/judge-rejects-googles-attempt-to-dmca-its-way-out-of-being-scraped/) ⭐️ 8.0/10

A U.S. judge ruled that Google cannot use the Digital Millennium Copyright Act \(DMCA\) to prevent third-party scraping of its search results, rejecting Google&\#x27;s argument that scraping constitutes copyright infringement. This ruling sets an important legal precedent upholding the legality of scraping publicly available data on the web, which is critical for competitors, researchers, and transparency advocates who rely on web scraping for innovation and accountability. Google had argued that its search results are compiled with creative selection and arrangement, warranting copyright protection, but the judge found insufficient originality. The case involved Google suing SerpAPI, a third-party service that scrapes Google&\#x27;s search results.

hackernews · cdrnsf · Jul 27, 18:15 · [Discussion](https://news.ycombinator.com/item?id=49073513)

**Background**: Web scraping is the automated extraction of data from websites, often used for data analysis, market research, or creating alternative user interfaces. The DMCA is a U.S. copyright law that prohibits circumvention of technological protection measures and can be used to enforce copyright claims. This case highlights the tension between copyright law and the open web.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Web_scraping">Web scraping - Wikipedia</a></li>
<li><a href="https://www.linkedin.com/pulse/what-dmca-why-does-matter-website-owners-qumere-alam-siddiqui-get6c">What is DMCA and Why Does It Matter for Website Owners 2026?</a></li>
<li><a href="https://www.dmca.com/">Content Protection and Takedown Company Since 2006 | DMCA .com</a></li>

</ul>
</details>

**Discussion**: Commenters noted the irony that Google&\#x27;s own success was built on crawling the web, and criticized Google for deprecating its affordable API while suing third parties that fill the gap. Some highlighted the public interest in scraping search results to expose advertising scams.

**Tags**: `#DMCA`, `#Web Scraping`, `#Google`, `#Copyright`, `#Tech Law`

---

<a id="item-7"></a>
## [Hazard Pointers Proposed for Linux Kernel](https://lwn.net/Articles/1084015/) ⭐️ 8.0/10

The Linux kernel community is evaluating a hazard pointer implementation proposed by Mathieu Desnoyers and Paul McKenney as an alternative to read-copy-update \(RCU\) for lockless data updates. Hazard pointers can reduce memory usage and cleanup delays compared to RCU, offering better performance in certain scenarios, which is significant for the kernel&\#x27;s scalability and real-time capabilities. The proposed API requires allocating a hazptr\_ctx for each concurrent pointer, with hazptr\_acquire\(\) to protect an object and hazptr\_release\(\) to release it; hazptr\_synchronize\(\) waits until all references are gone. The implementation uses a per-CPU array with four slots.

rss · LWN.net · Jul 27, 16:51

**Background**: Read-copy-update \(RCU\) is a synchronization mechanism that allows concurrent reads and updates without locks, but it can delay memory reclamation. Hazard pointers are an alternative safe memory reclamation technique that tracks active references explicitly, often leading to lower overhead for short-lived references.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Read-copy-update">Read - copy - update - Wikipedia</a></li>
<li><a href="https://www.linkedin.com/pulse/lock-free-stack-hazard-pointer-implementation-explained-rainer-grimm-0nsze?tl=en">A Lock-Free Stack: A Hazard Pointer Implementation Explained I</a></li>

</ul>
</details>

**Tags**: `#linux-kernel`, `#hazard-pointers`, `#RCU`, `#memory-management`, `#concurrency`

---

<a id="item-8"></a>
## [Solo Evaluation Finds Left-Leaning Bias in Six Frontier LLMs](https://www.reddit.com/r/MachineLearning/comments/1v8fnzw/evaluated_6_frontier_llms_gpt54_claude_sonnet_46/) ⭐️ 8.0/10

A solo evaluation of six frontier LLMs \(GPT-5.4, Claude Sonnet 4.6, Claude Opus 4.7, Gemini Pro, Gemini Flash, and Grok 4.3\) across 8 bias benchmarks \(~20,600 examples\) found that all models exhibit left-leaning political bias, and show high refusal rates on race-related questions, with GPT-5.4 refusing 20.3% of such questions. This study provides empirical evidence of systematic political bias across leading AI systems, which could affect trust and fairness in applications like content moderation and decision support. The high refusal rates on race questions also raise concerns about model utility and potential avoidance behavior on sensitive topics. Notably, Grok 4.3, which self-reports as right-leaning, actually behaves in a left-leaning manner when classifying content or answering policy questions. Refusal rates on BBQ race questions varied widely: GPT-5.4 refused 20.3%, Claude Opus 4.7 refused 13.8%, Grok 9.5%, and Claude Sonnet 4.6 and Gemini Pro around 5%.

reddit · r/MachineLearning · /u/marggggggggg · Jul 27, 22:37

**Background**: Bias evaluation benchmarks like WinoBias, BBQ, and SeeGULL are designed to measure social biases \(gender, race, political orientation\) in language models. WinoBias tests gender bias in coreference resolution, BBQ assesses bias in question answering across nine social dimensions, and SeeGULL covers stereotypes across geo-cultural groups. This study used eight such benchmarks to compare six state-of-the-art LLMs on political, gender, and racial bias.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2110.08193">[2110.08193] BBQ: A Hand-Built Bias Benchmark for Question Answering</a></li>
<li><a href="https://www.emergentmind.com/topics/winobias">WinoBias : Gender Bias in Coreference Benchmark</a></li>
<li><a href="https://github.com/google-research-datasets/seegull">GitHub - google-research-datasets/seegull: SeeGULL is a broad-coverage stereotype dataset in English containing stereotypes about identity groups spanning 178 countries across 8 different geo-political regions across 6 continents, as well as state-level identities within the US and India. · GitHub</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#bias`, `#evaluation`, `#fairness`

---

<a id="item-9"></a>
## [Changxin Memory surges 471% on STAR Market debut](https://www.stcn.com/article/detail/4042119.html) ⭐️ 8.0/10

Changxin Memory Technologies \(688825.SH\) debuted on the Shanghai Stock Exchange STAR Market on July 27, opening at 49.5 yuan per share, a 471.59% increase from its IPO price of 8.66 yuan. This IPO is the largest in STAR Market history, with total funds raised of approximately 57.919 billion yuan, surpassing SMIC&\#x27;s 2020 record. It marks a significant milestone for China&\#x27;s domestic DRAM industry and the broader semiconductor self-sufficiency drive. If the over-allotment option is fully exercised, total funds raised could reach about 66.607 billion yuan. The company expects net profit attributable to parent of 50-57 billion yuan for the first half of 2026, a sharp turnaround from losses.

telegram · zaihuapd · Jul 27, 01:29

**Background**: Changxin Memory is China&\#x27;s leading DRAM manufacturer and a key player in the national push for semiconductor self-sufficiency. The STAR Market, established in 2019, is China&\#x27;s Nasdaq-style board for tech and innovative companies, with an IPO system based on registration.

<details><summary>References</summary>
<ul>
<li><a href="https://cfi.net.cn/p20260716000463.html">长 鑫 科 技 上市在即，A股投资风向转变了吗？ - CFi.CN 中财网</a></li>
<li><a href="https://en.wikipedia.org/wiki/Shanghai_Stock_Exchange_STAR_Market">Shanghai Stock Exchange STAR Market - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#半导体`, `#IPO`, `#存储芯片`, `#科创板`, `#国产替代`

---

<a id="item-10"></a>
## [China Begins Mass Production of Domestic DUV Lithography Tools](https://www.theinformation.com/articles/china-starts-mass-producing-homegrown-duv-chipmaking-tools-advance-local-chip-industry) ⭐️ 8.0/10

China has started mass-producing domestically developed immersion deep ultraviolet \(DUV\) lithography machines, with a target of approximately 5 units in 2025 and 20 units by 2027, to be delivered to domestic chipmakers like SMIC and Hua Hong Semiconductor. This marks a strategic step in China&\#x27;s effort to reduce reliance on foreign lithography equipment, potentially challenging ASML&\#x27;s dominance in the Chinese market, especially if Western export controls tighten further. The domestically produced tools still lag behind ASML&\#x27;s offerings in performance and reliability, and chipmakers will need months to test precision and compatibility before they can be used in mass production lines.

telegram · zaihuapd · Jul 27, 14:10

**Background**: Deep ultraviolet \(DUV\) lithography uses light \(typically 193 nm or 248 nm\) to pattern integrated circuits on silicon wafers. Immersion lithography replaces the air gap between the lens and wafer with water, enhancing resolution to produce features below 45 nm. ASML currently dominates the high-end lithography market, making China&\#x27;s push for self-sufficiency significant.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DUV_lithography">DUV lithography</a></li>
<li><a href="https://en.wikipedia.org/wiki/Immersion_lithography">Immersion lithography</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#lithography`, `#China`, `#ASML`, `#chip manufacturing`

---