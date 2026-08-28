---
layout: default
title: "Horizon Summary: 2026-06-09 (EN)"
date: 2026-06-09
lang: en
---

> From 62 items, 15 important content pieces were selected

---

1. [OpenAI Submits S-1 Draft to SEC](#item-1) ⭐️ 9.0/10
2. [Signal condemns UK surveillance proposals as threat to privacy](#item-2) ⭐️ 9.0/10
3. [Xiaomi MiMo v2.5 Pro UltraSpeed: 1000 tokens/sec on 1T model](#item-3) ⭐️ 9.0/10
4. [Luce Spark Enables 35B MoE on 16GB GPU Without Offload Tax](#item-4) ⭐️ 9.0/10
5. [Apple Unveils Core AI Framework for On-Device AI](#item-5) ⭐️ 8.0/10
6. [Social media shifts from friends to fads](#item-6) ⭐️ 8.0/10
7. [xAI's GPU Rental Business Resembles Data Center REIT](#item-7) ⭐️ 8.0/10
8. [Apple reveals new AI architecture with Google Gemini models](#item-8) ⭐️ 8.0/10
9. [AI progress is slowing and revenue demands are unsustainable](#item-9) ⭐️ 8.0/10
10. [Massachusetts bans sale of precise location data](#item-10) ⭐️ 8.0/10
11. [Thermo Fisher antibody data manipulation investigation](#item-11) ⭐️ 8.0/10
12. [BM25 outperforms semantic embeddings for tool selection in agents](#item-12) ⭐️ 8.0/10
13. [Indie Dev Embeds Local LLM in Unity for Unscripted NPC Chat](#item-13) ⭐️ 8.0/10
14. [GGerganov's PR Optimizes KV Cache for Gemma-4 MTP](#item-14) ⭐️ 8.0/10
15. [llama.cpp adds video input support via mtmd](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [OpenAI Submits S-1 Draft to SEC](https://openai.com/index/openai-submits-confidential-s-1/) ⭐️ 9.0/10

OpenAI has confidentially submitted a draft S-1 registration statement to the SEC as a preliminary step toward an initial public offering. This marks a major milestone in OpenAI's transition from a non-profit to a public company, which could democratize access to AI investments and influence the broader AI industry landscape. The confidential filing under the JOBS Act allows OpenAI to keep financial details private until closer to the IPO, and the SEC typically completes its review of a draft S-1 within about two weeks.

hackernews · hackerBanana · Jun 8, 21:22 · [Discussion](https://news.ycombinator.com/item?id=48452317)

**Background**: An S-1 registration statement is a form required by the SEC for companies planning to go public in the U.S., containing detailed financial and business information. The JOBS Act of 2012 allows emerging growth companies to file draft registration statements confidentially for nonpublic review, reducing market speculation during the preparation phase.

<details><summary>References</summary>
<ul>
<li><a href="https://www.sec.gov/about/divisions-offices/division-corporation-finance/draft-registration-statement-processing-procedures-expanded">SEC.gov | Enhanced Accommodations for Issuers Submitting ...</a></li>
<li><a href="https://www.sec.gov/Archives/edgar/data/1326801/000119312512034517/d287954ds1.htm">Registration Statement on Form S-1</a></li>

</ul>
</details>

**Discussion**: Community comments express skepticism about OpenAI's transition from non-profit to public company, with some questioning the point of non-profits that can IPO. Others humorously compare the announcement to a brief slack message and speculate on retail investor frenzy and market impact.

**Tags**: `#OpenAI`, `#IPO`, `#AI industry`, `#corporate finance`

---

<a id="item-2"></a>
## [Signal condemns UK surveillance proposals as threat to privacy](https://signal.org/blog/pdfs/2026-06-08-uk-surveillance-is-not-safety.pdf) ⭐️ 9.0/10

Signal published a statement (PDF) arguing against the UK government's surveillance proposals, warning that client-side scanning and remote attestation would undermine end-to-end encryption and user privacy. This matters because it highlights the escalating conflict between government surveillance ambitions and the fundamental right to private communication; if adopted, such measures could set a global precedent for weakening encryption. The statement specifically criticizes proposed client-side scanning (CSS) and remote attestation, which would force devices to scan messages locally and verify compliance, effectively breaking end-to-end encryption without technically breaking it.

hackernews · g0xA52A2A · Jun 8, 19:42 · [Discussion](https://news.ycombinator.com/item?id=48450646)

**Background**: The UK's Online Safety Bill and related proposals have sparked widespread concern among privacy advocates. Client-side scanning (CSS) is a technique where a user's device scans content before encryption, allowing authorities to detect illegal material without directly accessing encrypted data, but critics argue it enables mass surveillance and weakens security for all users.

<details><summary>References</summary>
<ul>
<li><a href="https://techcrunch.com/2022/11/24/uk-online-safety-bill-css-e2ee/">Surveillance powers in UK's Online Safety Bill are risk to</a></li>
<li><a href="https://www.internetsociety.org/resources/doc/2020/fact-sheet-client-side-scanning/">Fact Sheet: Client - Side Scanning - Internet Society</a></li>

</ul>
</details>

**Discussion**: Community commenters express strong opposition, with some noting the slippery slope from device DRM to government surveillance (michaelt) and others warning of a gradual expansion: camera-based age verification, then AI nudity detection on all devices (big85). There is also frustration with political leaders and a sense of inevitability about the 'ratchet' of surveillance measures (budududuroiu).

**Tags**: `#privacy`, `#surveillance`, `#encryption`, `#UK policy`, `#Signal`

---

<a id="item-3"></a>
## [Xiaomi MiMo v2.5 Pro UltraSpeed: 1000 tokens/sec on 1T model](https://mimo.xiaomi.com/blog/mimo-tilert-1000tps) ⭐️ 9.0/10

Xiaomi released MiMo-v2.5-Pro-UltraSpeed, achieving up to 1200 tokens per second inference speed on a 1.02 trillion parameter Mixture-of-Experts model. This breakthrough could dramatically reduce AI inference costs and latency, potentially democratizing access to trillion-parameter models for real-time applications. The model has 42 billion active parameters due to MoE sparsity, uses hybrid attention and multi-token prediction, and supports up to 1 million token context with pricing at $0.14 per million input tokens and $0.28 per million output tokens.

hackernews · gainsurier · Jun 8, 15:27 · [Discussion](https://news.ycombinator.com/item?id=48446639)

**Background**: MiMo is an open-source Mixture-of-Experts (MoE) model developed by Xiaomi. MiMo-v2.5-Pro has 1.02 trillion total parameters but only 42 billion active per token, making it efficient. The UltraSpeed variant uses optimized inference to achieve extremely high throughput.

<details><summary>References</summary>
<ul>
<li><a href="https://mimo.xiaomi.com/blog/mimo-tilert-1000tps">Xiaomi MiMo , Explore and Love</a></li>
<li><a href="https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro-Base">XiaomiMiMo/ MiMo - V 2 . 5 - Pro -Base · Hugging Face</a></li>
<li><a href="https://openrouter.ai/xiaomi/mimo-v2.5">MiMo - V 2 . 5 - API Pricing & Benchmarks | OpenRouter</a></li>

</ul>
</details>

**Discussion**: Commenters expressed mixed feelings: some find the speed exciting but unsettling for workflow, others question productivity gains given fixed work hours. There is also commentary on price competition between Chinese and American providers, with MiMo's fast mode being very competitive.

**Tags**: `#AI`, `#LLM`, `#inference`, `#performance`, `#Xiaomi`

---

<a id="item-4"></a>
## [Luce Spark Enables 35B MoE on 16GB GPU Without Offload Tax](https://www.reddit.com/r/LocalLLaMA/comments/1u0b3cu/luce_spark_a_35b_moe_on_a_16_gb_gpu_without_the/) ⭐️ 9.0/10

Luce Spark introduces a dynamic caching technique that keeps only active experts on the GPU, allowing 35B MoE models to run on 16 GB VRAM with minimal offload overhead. It uses self-tuning calibration to learn expert placement from live routing, and a fused graph to eliminate per-layer graph overhead. This breakthrough makes large MoE models accessible on consumer-grade GPUs, drastically lowering the hardware barrier for local LLM inference. It could enable developers and enthusiasts to run state-of-the-art models like Qwen3.6 35B-A3B on affordable 16 GB cards. The system achieves ~100 tok/s at 60% GPU residency, compared to 66 tok/s with naive offload, and 119 tok/s on a full 24 GB GPU. It is implemented in the open-source dflash_server tool and supports both Laguna and Qwen MoE models in GGUF format.

reddit · r/LocalLLaMA · /u/sandropuppo · Jun 8, 15:24

**Background**: Mixture-of-Experts (MoE) models use multiple specialized sub-networks (experts) and activate only a subset per token, which allows larger parameter counts with lower computational cost. However, loading all experts into GPU memory is often impossible, and offloading to CPU introduces significant latency. Luce Spark addresses this by caching only the most frequently used experts on the GPU and swapping others on-demand.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/html/2512.03927v1">OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed</a></li>
<li><a href="https://arxiv.org/html/2412.00099v2">Mixture of Cache-Conditional Experts for Efficient Mobile</a></li>
<li><a href="https://arxiv.org/html/2509.02408v1">Cache Management for Mixture-of-Experts LLMs – extended</a></li>

</ul>
</details>

**Tags**: `#MoE`, `#local LLM`, `#GPU optimization`, `#model inference`, `#caching`

---

<a id="item-5"></a>
## [Apple Unveils Core AI Framework for On-Device AI](https://developer.apple.com/documentation/coreai/) ⭐️ 8.0/10

Apple introduced Core AI, a new framework for running AI models on-device, with tools to convert PyTorch models into the .aimodel format and optimize them for Apple silicon's CPU, GPU, and Neural Engine. Core AI could replace the older CoreML framework, enabling developers to deploy full-scale large language models locally, which may reduce reliance on cloud AI services and accelerate on-device intelligence across the Apple ecosystem. The framework includes Core AI Optimization for model preparation and Core AI PyTorch Extensions for model conversion, and is highlighted in WWDC 2026 sessions. It supports both CPU/GPU and the Neural Engine.

hackernews · hmokiguess · Jun 8, 18:47 · [Discussion](https://news.ycombinator.com/item?id=48449665)

**Background**: Apple previously provided CoreML for on-device machine learning, but it was limited in handling large, complex models like LLMs. Core AI is designed to leverage Apple's unified memory architecture and Neural Engine to run full-scale AI models locally, offering better performance and privacy.

<details><summary>References</summary>
<ul>
<li><a href="https://www.apple.com/newsroom/2026/06/apple-aids-app-development-with-new-intelligence-frameworks-and-advanced-tools/">Apple aids app development with new intelligence frameworks and ...</a></li>

</ul>
</details>

**Discussion**: Developers are excited about on-device AI's potential to disrupt cloud AI companies, as one commenter noted AI companies are rushing to IPO before the shift. Another pointed to a related Foundation model update and WWDC 2026 videos. A common question is whether Core AI completely replaces CoreML, with some viewing it as a direct successor.

**Tags**: `#Apple`, `#Core AI`, `#on-device AI`, `#PyTorch`, `#CoreML`

---

<a id="item-6"></a>
## [Social media shifts from friends to fads](https://www.bbc.com/worklife/article/20260520-how-social-media-ceased-to-be-social) ⭐️ 8.0/10

A BBC article argues that social media platforms like Facebook and Instagram have evolved from tools for connecting with friends into algorithm-driven content discovery feeds, reducing genuine social interaction. This shift reflects a broader trend in technology where user engagement is prioritized over authentic connection, impacting how people interact online and raising concerns about mental health and manipulation. The article notes that users now primarily consume content from strangers rather than friends, and that algorithms curate feeds based on engagement metrics rather than social relationships.

hackernews · 1vuio0pswjnm7 · Jun 8, 11:58 · [Discussion](https://news.ycombinator.com/item?id=48444228)

**Background**: Social media originally centered on connecting with friends and family through updates and photos. Over time, platforms introduced algorithmic feeds to increase engagement, showing popular content from non-friends. This shift has been criticized for reducing genuine social interaction and promoting addictive behaviors.

**Discussion**: Commenters express frustration, with one stating social media now manipulates users like cable TV but worse. Another notes that removing non-friend content leaves feeds nearly empty, revealing how little actual social content exists. Some debate whether platforms like Hacker News are also social media.

**Tags**: `#social media`, `#algorithms`, `#technology criticism`, `#online culture`, `#engagement`

---

<a id="item-7"></a>
## [xAI's GPU Rental Business Resembles Data Center REIT](https://martinalderson.com/posts/xais-new-rental-business/) ⭐️ 8.0/10

xAI's primary business appears to be renting GPUs to companies like Google and Anthropic, generating an estimated $26 billion in annual revenue, rather than leading AI research. This makes xAI resemble a data center REIT more than a frontier AI lab. This critique challenges the perception of xAI as a cutting-edge AI lab and highlights circular financial deals involving SpaceX and Google that may inflate valuations. It raises concerns about the sustainability of such business models in the AI industry. xAI's Colossus cluster runs on on-site gas turbines with fuel costs of only about $90 million per year. However, the quality of xAI's LLM suggests it is not at the frontier of AI research.

hackernews · martinald · Jun 8, 15:13 · [Discussion](https://news.ycombinator.com/item?id=48446428)

**Background**: A REIT (Real Estate Investment Trust) is a company that owns and operates income-producing real estate. Data center REITs profit from increasing data usage and AI growth by leasing data center space. xAI's model of renting GPU capacity essentially turns it into a similar income-generating entity rather than a research lab.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Real_estate_investment_trust">Real estate investment trust - Wikipedia</a></li>
<li><a href="https://www.reit.com/what-reit/reit-sectors/data-center">Discover Data Center REITs | Investing Tips, Data and More REITs</a></li>

</ul>
</details>

**Discussion**: Commenters are skeptical of the circular deals between xAI, Google, and SpaceX, with one noting that Google's stake in SpaceX could incentivize inflated valuations. Others point out that the article echoes a previous HN comment, raising questions about originality. There is also debate about whether xAI's revenue model justifies its valuation given its model quality.

**Tags**: `#xAI`, `#AI industry`, `#business model`, `#GPU renting`, `#data center`

---

<a id="item-8"></a>
## [Apple reveals new AI architecture with Google Gemini models](https://www.macrumors.com/2026/06/08/apple-reveals-new-ai-architecture/) ⭐️ 8.0/10

Apple announced a new AI architecture that integrates Google Gemini models, emphasizing privacy through on-device processing and Private Cloud Compute. This partnership positions Apple to leverage Google's advanced AI while maintaining its strong privacy stance, potentially setting a new standard for on-device AI and challenging competitors like OpenAI and Anthropic. The architecture uses on-device processing and Private Cloud Compute, with Apple guaranteeing that user data is used only for the immediate request and is not accessible to Apple or third parties; outside experts can verify these privacy guarantees at any time.

hackernews · unclefuzzy · Jun 8, 19:14 · [Discussion](https://news.ycombinator.com/item?id=48450142)

**Background**: Apple Intelligence is Apple's suite of AI features that prioritize on-device processing to protect user privacy. Private Cloud Compute extends this by processing more complex requests in Apple's own cloud infrastructure without storing data. Google Gemini is a family of large language models developed by Google DeepMind, known for advanced reasoning and multimodal capabilities.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">Gemini (language model) - Wikipedia</a></li>
<li><a href="https://deepmind.google/models/gemini/pro/">Gemini 3.1 Pro — Google DeepMind</a></li>

</ul>
</details>

**Discussion**: Commenters had mixed reactions: luk212 called it a 'very Apple-ish approach' of wrapping external tools in a privacy architecture, while microflash noted the lack of EU launch as concerning. NorwegianDude questioned the feasibility of Apple's privacy claims, and bensyverson requested more technical details about model integration. dejawu wondered why Apple chose Google over Anthropic or OpenAI, risking less differentiation.

**Tags**: `#Apple`, `#Google Gemini`, `#AI architecture`, `#privacy`, `#on-device AI`

---

<a id="item-9"></a>
## [AI progress is slowing and revenue demands are unsustainable](https://www.wheresyoured.at/ai-is-slowing-down/) ⭐️ 8.0/10

An article by Ed Zitron argues that artificial intelligence progress is decelerating and that the industry requires over $3 trillion in revenue by the end of 2030 to maintain its existence, highlighting a financial sustainability crisis. This challenges the prevailing narrative of unbounded AI growth and raises critical questions about the economic viability of massive AI investments, affecting venture capital, corporate strategy, and public expectations. The article claims that despite enormous capital expenditure, AI companies are far from generating sufficient revenue, and scaling laws may be yielding diminishing returns. It also points to high operational costs and competition among cloud providers.

hackernews · crescit_eundo · Jun 8, 15:46 · [Discussion](https://news.ycombinator.com/item?id=48446893)

**Background**: AI scaling laws describe the empirical relationship between model performance and factors like compute, data, and parameters. The Chinchilla scaling law, introduced by DeepMind in 2022, emphasizes compute-optimal training by balancing model size and data. However, recent observations suggest that simply scaling up may be hitting limits, leading to debates about the future of AI progress and the economic models supporting it.

<details><summary>References</summary>
<ul>
<li><a href="https://www.remio.ai/post/ai-scaling-laws-are-rewriting-the-rules-of-innovation-why-bigger-models-don-t-just-mean-better-resu">AI scaling laws are rewriting the rules of innovation: why</a></li>
<li><a href="https://en.wikipedia.org/wiki/Neural_scaling_law">Neural scaling law - Wikipedia</a></li>
<li><a href="https://arxiv.org/abs/2203.15556">[2203.15556] Training Compute-Optimal Large Language Models Chinchilla Scaling Laws: Compute-Optimal Training and ... Chinchilla Scaling Laws - GeeksforGeeks Chinchilla scaling laws - AI Wiki Neural scaling law - Wikipedia Images Chinchilla data-optimal scaling laws: In plain English Chinchilla Scaling Laws for Large Language Models (LLMs)</a></li>

</ul>
</details>

**Discussion**: Comments are divided: some agree with the financial analysis, noting the huge revenue gap, while others argue that the article underestimates real-world productivity gains and the potential for new applications. One commenter suggests that Apple's low-cost licensing deal with Google shows consumer AI can be profitable, countering the narrative of unprofitability.

**Tags**: `#AI`, `#economics`, `#industry analysis`, `#scaling`, `#sustainability`

---

<a id="item-10"></a>
## [Massachusetts bans sale of precise location data](https://techcrunch.com/2026/06/08/massachusetts-votes-to-pass-new-privacy-rights-bill-that-bans-sale-of-precise-location-data/) ⭐️ 8.0/10

Massachusetts has passed a new privacy rights bill that explicitly bans the sale of precise location data, marking a significant legislative move to protect consumer privacy. This bill sets a precedent for other states and could lead to a nationwide shift in how location data is handled, impacting companies that rely on selling such data for revenue. The bill specifically targets the 'sale' of location data, which some commenters note may leave loopholes for data exchange or transfer that isn't classified as a sale.

hackernews · 01-_- · Jun 8, 17:07 · [Discussion](https://news.ycombinator.com/item?id=48448012)

**Background**: Precise location data is highly sensitive as it can reveal individuals' movements, habits, and associations. Many apps and services collect this data, often sharing or selling it to third parties without explicit user consent. This bill is part of a broader privacy movement, following similar actions in California and fines against companies like General Motors for unauthorized data sharing.

**Discussion**: Community comments express cautious optimism, with some pointing out potential loopholes like using 'exchange' instead of 'sale'. Others raise concerns about vehicle data and argue that the harm occurs at data collection, not just sale, urging stronger protections.

**Tags**: `#privacy`, `#location data`, `#legislation`, `#data rights`

---

<a id="item-11"></a>
## [Thermo Fisher antibody data manipulation investigation](https://reeserichardson.blog/2026/05/28/how-much-of-thermo-fishers-antibody-data-has-been-manipulated/) ⭐️ 8.0/10

An investigation by Sholto David has uncovered potential large-scale data manipulation in Thermo Fisher Scientific's antibody products, suggesting systematic fraud in their validation data. This matters because Thermo Fisher is a major global antibody supplier, and falsified data can waste researchers' time and money while undermining the reproducibility of biomedical research. The investigation was led by whistleblower Sholto David, who previously uncovered fraud at Dana-Farber Cancer Institute. The blog post examines multiple cases of suspicious western blot images in Thermo Fisher's antibody validation data.

hackernews · mhrmsn · Jun 8, 06:56 · [Discussion](https://news.ycombinator.com/item?id=48442075)

**Background**: Antibodies are essential tools in biomedical research used to detect specific proteins. Data manipulation in antibody validation can lead to irreproducible results, contributing to the ongoing reproducibility crisis in science. Thermo Fisher is one of the largest suppliers of research antibodies globally.

**Discussion**: Commenters expressed strong suspicion of systematic fraud, with one noting they had observed faked data years ago for Ikaros antibodies and subsequently avoided Thermo Fisher. Others praised Sholto David's investigative work and highlighted the financial and practical impact on labs, while noting that serious researchers already validate antibodies themselves.

**Tags**: `#scientific fraud`, `#antibody research`, `#biotech`, `#reproducibility crisis`, `#data manipulation`

---

<a id="item-12"></a>
## [BM25 outperforms semantic embeddings for tool selection in agents](https://www.reddit.com/r/MachineLearning/comments/1u07tlm/why_i_stopped_using_semantic_embeddings_for_tool/) ⭐️ 8.0/10

A Reddit user reports that after testing three retrieval strategies on 200 query-tool pairs, BM25 achieved 81% top-1 accuracy for tool selection, outperforming semantic embeddings (64%) and a hybrid approach (78%). The author switched back to BM25 for a production agent system exposing 140 MCP tools. This challenges the common assumption that hybrid retrieval (semantic + BM25) always wins, showing that for tool selection—where descriptions are short and keyword-dependent—BM25 alone is more effective. Practitioners building agent gateways may need to reevaluate their retrieval strategies. The BM25 index included tool name, description, and a walk of input/output schema properties, which added discriminative keywords. Hybrid (0.7 semantic + 0.3 BM25) performed worse than BM25 alone because semantic noise diluted the clean BM25 signal. The author adopted Ratel's indexing approach documented in ADR-0004.

reddit · r/MachineLearning · /u/AbjectBug5885 · Jun 8, 13:24

**Background**: The Model Context Protocol (MCP) is an open standard for connecting AI applications to external tools and data sources. Tool descriptions in MCP are typically short (under 50 tokens) and structurally similar, with discriminative information often contained in a single keyword. BM25 is a classic information retrieval algorithm that ranks documents based on keyword frequency and term importance, making it well-suited for such sparse, keyword-driven queries.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Model_Context_Protocol">Model Context Protocol - Wikipedia</a></li>
<li><a href="https://modelcontextprotocol.io/docs/getting-started/intro">What is the Model Context Protocol (MCP)? - Model Context</a></li>

</ul>
</details>

**Tags**: `#tool selection`, `#semantic embeddings`, `#BM25`, `#agents`, `#information retrieval`

---

<a id="item-13"></a>
## [Indie Dev Embeds Local LLM in Unity for Unscripted NPC Chat](https://www.reddit.com/r/LocalLLaMA/comments/1u0cpbm/i_bundled_a_fully_local_llm_inside_my_unity_game/) ⭐️ 8.0/10

A developer created 'Simulation Simulator', a Unity game that runs a fully local LLM for unscripted NPC conversations, achieving five distinct endings based on natural language interactions without any internet or cloud dependency. This demonstrates a significant step beyond scripted dialogues, proving that local LLMs can create truly dynamic and replayable game narratives. It opens possibilities for immersive, evolving NPCs in indie games and highlights the potential for privacy-preserving AI in gaming. The game currently cannot include real-time text-to-speech or translation due to processing time adding 10-20 seconds per exchange. A demo of 'Simulation Simulator' is available on Steam for players to experience the local LLM-driven dialogue.

reddit · r/LocalLLaMA · /u/MorphLand · Jun 8, 16:21

**Background**: Local LLMs like those offered by Ollama or LM Studio allow AI models to run entirely on a user's machine without sending data to external servers. Tools such as LLMUnity provide Unity SDKs to integrate these models directly into game engines, enabling NPC dialogue generation that adapts to player input in real-time. Traditionally, game NPCs rely on pre-written dialogue trees or cloud-based AI services, which limit dynamism or require internet access.

<details><summary>References</summary>
<ul>
<li><a href="https://neocortex.link/blog/03-17-25_run_llms_locally_with_unity">Neocortex Blog | Use Large Language Models (LLMs) in Unity Locally!</a></li>
<li><a href="https://github.com/undreamai/LLMUnity">GitHub - undreamai/LLMUnity: Create characters in Unity with LLMs! · GitHub</a></li>
<li><a href="https://www.goodai.com/ai-people-now-with-local-llm/">AI People: Now with Local LLM | GoodAI</a></li>

</ul>
</details>

**Tags**: `#local-llm`, `#game-development`, `#unity`, `#NPC`, `#AI-integration`

---

<a id="item-14"></a>
## [GGerganov's PR Optimizes KV Cache for Gemma-4 MTP](https://www.reddit.com/r/LocalLLaMA/comments/1u06jel/kvcache_avoid_kv_cells_copies_by_ggerganov_pull/) ⭐️ 8.0/10

A pull request by ggerganov has been merged into llama.cpp that eliminates unnecessary KV cache copies, improving multi-token prediction (MTP) performance for Gemma-4 models. The change is available in llama.cpp version b9551 and later. This optimization reduces inference latency and memory overhead for multi-token prediction, a technique that predicts several future tokens simultaneously. It makes Gemma-4 inference more efficient, benefiting applications like real-time language generation and decoding. The PR specifically avoids copying KV cells during inference, which is a frequent bottleneck in transformer-based LLMs. The merge was quick, indicating high community consensus on the improvement's value.

reddit · r/LocalLLaMA · /u/pmttyji · Jun 8, 12:31

**Background**: KV caching is a technique that stores past key-value pairs in the attention mechanism to avoid recomputation, speeding up LLM inference. Multi-token prediction (MTP) extends the traditional next-token prediction by forecasting multiple future tokens at once, which can improve throughput and reduce decoding steps. This PR targets the intersection of these two optimizations for the Gemma-4 model family running on llama.cpp.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/blog/not-lain/kv-caching">KV Caching Explained: Optimizing Transformer Inference Efficiency</a></li>
<li><a href="https://sebastianraschka.com/llm-architecture-gallery/mtp/">Multi-Token Prediction (MTP) | Sebastian Raschka, PhD</a></li>
<li><a href="https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms">Understanding and Coding the KV Cache in LLMs from Scratch</a></li>

</ul>
</details>

**Tags**: `#llama.cpp`, `#KV-cache`, `#performance optimization`, `#LLM inference`, `#MTP`

---

<a id="item-15"></a>
## [llama.cpp adds video input support via mtmd](https://www.reddit.com/r/LocalLLaMA/comments/1u08j3q/mtmd_add_video_input_support_by_ngxson_pull/) ⭐️ 8.0/10

Pull request #24269 by ngxson adds video input support to llama.cpp using the mtmd tool, allowing multimodal models like Gemma and Qwen to process video content directly on local hardware. This extends llama.cpp's multimodal capabilities from images to video, significantly broadening the range of local AI applications such as video captioning, question answering, and analysis without cloud dependency. The mtmd tool, designed for multimodal processing, now accepts video files as input, likely converting frames to tokens for the underlying LLM. This integration follows the earlier addition of image support and aligns with models like Gemma 4 that natively support video understanding.

reddit · r/LocalLLaMA · /u/jacek2023 · Jun 8, 13:51

**Background**: llama.cpp is a popular open-source library for running large language models locally on consumer hardware, written in C/C++. It has recently added multimodal support for image inputs through tools like llava and mtmd. The mtmd tool specifically handles multiple modalities and now extends to video, enabling users to feed video files directly into compatible models for inference.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md">llama . cpp /docs/ multimodal .md at master · ggml-org/ llama . cpp · GitHub</a></li>
<li><a href="https://simonwillison.net/2025/May/10/llama-cpp-vision/">Trying out llama.cpp’s new vision support</a></li>
<li><a href="https://huggingface.co/blog/gemma4">Welcome Gemma 4: Frontier multimodal intelligence on device</a></li>

</ul>
</details>

**Tags**: `#llama.cpp`, `#multimodal`, `#video`, `#AI inference`

---