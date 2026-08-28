---
layout: default
title: "Horizon Summary: 2026-02-26 (EN)"
date: 2026-02-26
lang: en
---

> From 41 items, 14 important content pieces were selected

---

1. [vLLM v0.16.0 released with 30%+ throughput gains, Realtime API, and major XPU updates.](#item-1) ⭐️ 8.0/10
2. [Qwen 3.5 Struggles on Complex Coding Tasks in Comprehensive 70-Repo Benchmark](#item-2) ⭐️ 8.0/10
3. [Qwen 3 27B Model Creates Playable 3D Game Through Iterative Prompting](#item-3) ⭐️ 8.0/10
4. [Anthropic Abandons Its Core AI Safety Pledge Citing Competition](#item-4) ⭐️ 8.0/10
5. [Anthropic Reports Large-Scale Distillation Attacks on Claude by Chinese AI Labs](#item-5) ⭐️ 8.0/10
6. [SMIC's N+3 Process Used for Huawei Kirin 9030, Advancing Toward 5nm-Class Tech](#item-6) ⭐️ 8.0/10
7. [Chinese Academy of Sciences to stop paying APCs for over 30 high-cost journals like Nature Communications](#item-7) ⭐️ 8.0/10
8. [tldraw moves test suite to private repository over competitive concerns](#item-8) ⭐️ 7.0/10
9. [Claude Code Launches Remote Control Feature for Multi-Device Access](#item-9) ⭐️ 7.0/10
10. [Effort to Secure Network Time Protocol Gains Momentum with NTS Adoption Push](#item-10) ⭐️ 7.0/10
11. [Benchmark reveals Q4_K_M outperforms UD-Q4_K_XL for Qwen3.5-35B-A3B quantization on RTX 5080.](#item-11) ⭐️ 7.0/10
12. [OpenAI adds WebSocket support to Responses API, speeding up long-chain tasks by 40%](#item-12) ⭐️ 7.0/10
13. [Uber Employees Use AI Clone of CEO to Rehearse Presentations](#item-13) ⭐️ 7.0/10
14. [QingLong Panel Compromised by Cryptojacking Malware, CPU Usage Spikes to 800%](#item-14) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [vLLM v0.16.0 released with 30%+ throughput gains, Realtime API, and major XPU updates.](https://github.com/vllm-project/vllm/releases/tag/v0.16.0) ⭐️ 8.0/10

vLLM v0.16.0 introduces async scheduling with pipeline parallelism, delivering over 30% end-to-end throughput improvement, and launches a new WebSocket-based Realtime API for streaming audio interactions. The release also includes a major overhaul of its XPU platform, deprecating IPEX in favor of new vllm-xpu-kernels with expanded support for models like MoE and new data types. This release significantly boosts the efficiency and scalability of large language model inference, a critical bottleneck for AI applications, making high-volume, low-latency serving more cost-effective. The new Realtime API and expanded hardware support directly enable new interactive, voice-based applications and broaden the range of deployable hardware for AI workloads. The performance gains are quantified as a 30.8% end-to-end throughput improvement and a 31.8% improvement in tokens per output token (TPOT). The Realtime API builds on infrastructure from Mistral AI's Voxtral models, enabling sub-500ms latency streaming ASR. The XPU platform update adds support for mixed experts (MoE) models, MXFP4, WNA16, scaled matrix multiplication (scaled_mm), and FP8 data types.

github · khluu · Feb 25, 19:58

**Background**: vLLM is a high-throughput and memory-efficient inference and serving engine for large language models (LLMs). Pipeline parallelism is a technique to split a model across multiple GPUs to handle larger models or increase throughput. The term 'XPU' is an Intel abstraction for heterogeneous compute architectures that can map to CPUs, GPUs, FPGAs, or other accelerators. The Realtime API is designed for low-latency, streaming interactions, particularly for voice applications using models like Voxtral.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.vllm.ai/en/latest/examples/online_serving/openai_realtime_client/">OpenAI Realtime Client - vLLM</a></li>
<li><a href="https://ai.stackexchange.com/questions/28760/what-exactly-is-an-xpu">What exactly is an XPU? - Artificial Intelligence Stack Exchange</a></li>

</ul>
</details>

**Tags**: `#llm-inference`, `#model-serving`, `#performance-optimization`, `#parallel-computing`, `#hardware-acceleration`

---

<a id="item-2"></a>
## [Qwen 3.5 Struggles on Complex Coding Tasks in Comprehensive 70-Repo Benchmark](https://i.redd.it/5g4ostqlbnlg1.png) ⭐️ 8.0/10

A comprehensive benchmark test of coding LLMs, called APEX Testing, has been updated to include 70 real-world coding tasks and evaluated new models including all Qwen 3.5 variants and GPT-5.3 Codex. The results show GPT-5.3 Codex performing consistently well, while the large Qwen 3.5 397B model's performance "craters" on the most difficult "master" tasks that require coordination across many files. This benchmark provides crucial, practical data for developers and organizations choosing coding assistants, highlighting that raw model size does not guarantee performance on complex, multi-step software engineering tasks. The findings challenge perceptions of model rankings and emphasize the importance of task-specific evaluation beyond simple code completion. The benchmark now uses an agentic tool-use system for local models to ensure a fairer comparison with cloud-based agents, and it includes a focus on "anti-benchmaxxing" to prevent gaming the results. Notably, a quantized version of the GLM-4.7 model achieved the highest ELO score (1572) among the tested local models, outperforming all Qwen 3.5 variants.

reddit · r/LocalLLaMA · hauhau901 · Feb 25, 13:52

**Background**: APEX Testing is a custom benchmark designed to evaluate coding Large Language Models (LLMs) on real codebases with real problems, moving beyond synthetic tasks. Quantization is a technique to reduce the memory and computational footprint of LLMs by representing weights with lower precision, enabling them to run on local hardware via tools like LM Studio. ELO is a rating system borrowed from chess, used here to rank model performance relative to each other on the benchmark tasks.

<details><summary>References</summary>
<ul>
<li><a href="https://apidog.com/blog/qwen3-quantized-models-locally/">How to Use Qwen3 Quantized Models Locally: A Step-by-Step Guide</a></li>
<li><a href="https://huggingface.co/lmstudio-community?search_models=Gemma-3">lmstudio-community ( LM Studio Community)</a></li>

</ul>
</details>

**Discussion**: Community discussion raised questions about methodology, particularly whether the custom agentic framework used might disadvantage some open-source models, as performance can swing dramatically based on the framework. Concerns were also voiced about trusting results from models served via APIs like OpenRouter, where the specific quantization or optimizations used are unknown and could hinder performance. Some users shared anecdotal experiences aligning with the benchmark's findings regarding Qwen 3.5 model behavior.

**Tags**: `#LLM Benchmarking`, `#Code Generation`, `#AI Programming`, `#Model Evaluation`, `#Open Source AI`

---

<a id="item-3"></a>
## [Qwen 3 27B Model Creates Playable 3D Game Through Iterative Prompting](https://www.reddit.com/r/LocalLLaMA/comments/1refvmr/qwen_3_27b_is_impressive/) ⭐️ 8.0/10

A user demonstrated that the Qwen 3 27B parameter large language model successfully generated a functional, GTA-like 3D game with walking, driving, and basic physics through a series of five iterative prompts and feedback cycles. The model corrected issues like a backward-facing camera based on user feedback, resulting in a playable artifact. This demonstrates a significant leap in the practical coding and spatial reasoning capabilities of smaller, locally-runnable LLMs, challenging the notion that only massive models can handle complex, stateful tasks like game development. It highlights the potential for rapid prototyping and creative assistance using affordable, local AI, which could democratize aspects of game development and software creation. The demonstration used a quantized version of the model (likely Q4 quantization), which significantly reduces memory requirements while reportedly maintaining performance for this multi-step task. The success heavily relied on iterative prompting, where the user provided specific feedback like "camera is facing backward" to guide corrections, a technique where modern models show improved handling compared to a year ago.

reddit · r/LocalLLaMA · -dysangel- · Feb 25, 15:13

**Background**: Qwen 3 is a series of open-source large language models developed by Alibaba Cloud. The 27B version is a "dense" model with 27 billion parameters, designed to offer a strong balance between performance and resource requirements, making it suitable for local deployment on consumer hardware. Iterative prompting is a technique where a user provides an initial prompt, evaluates the AI's output, and then gives follow-up prompts with feedback or new instructions to progressively refine the result, which is particularly effective for complex code generation tasks.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/html/2505.09388v1">Qwen3 Technical Report - arXiv</a></li>
<li><a href="https://www.ibm.com/think/topics/iterative-prompting">What is iterative prompting? - IBM</a></li>
<li><a href="https://medium.com/@MikeTangoSierra/deploying-an-llm-locally-a-practical-guide-9372dec5fa7a">Deploying an LLM Locally: A Practical Guide | by Mark - Medium</a></li>

</ul>
</details>

**Discussion**: The community expressed excitement about the performance of a relatively small, quantized model, seeing it as a positive sign for the future of fast, local, and affordable AI inference that breaks potential monopolies. Discussions highlighted the critical role of iterative prompting and spatial feedback, noted the model's ability to maintain context across multiple prompts despite quantization, and compared Qwen's performance to other models like Gemma3.

**Tags**: `#local-llm`, `#code-generation`, `#qwen`, `#3d-gaming`, `#model-benchmarking`

---

<a id="item-4"></a>
## [Anthropic Abandons Its Core AI Safety Pledge Citing Competition](https://time.com/7380854/exclusive-anthropic-drops-flagship-safety-pledge/) ⭐️ 8.0/10

Anthropic, the AI company known for its safety-conscious stance, has officially dropped its flagship safety pledge. The company cited intense competitive pressures and the rapid pace of AI advancement as reasons for this unilateral policy shift. This move signals a major retreat from voluntary self-regulation by a leading AI safety advocate, potentially weakening industry-wide norms and accelerating a competitive 'race to the bottom' on safety standards. It reflects how commercial and geopolitical pressures are overriding earlier ethical commitments in the frontier AI sector. The decision was reportedly influenced by pressure from the Pentagon to allow AI use for surveillance and autonomous weapons, alongside competition from rivals like DeepSeek. While dropping its unilateral pledge, Anthropic continues to endorse external regulatory efforts like California's AI safety bill SB 53.

reddit · r/LocalLLaMA · HumanDrone8721 · Feb 25, 18:59

**Background**: Anthropic was founded with a strong focus on AI safety research and positioned itself as an ethical leader. Its flagship safety pledge was a voluntary commitment to responsible development, similar to pledges made by other tech giants following White House initiatives. These pledges were part of a broader, industry-wide effort to establish safety norms ahead of binding government regulations.

<details><summary>References</summary>
<ul>
<li><a href="https://time.com/7380854/exclusive-anthropic-drops-flagship-safety-pledge/">Anthropic Drops Flagship Safety Pledge | TIME</a></li>
<li><a href="https://forklog.com/en/anthropic-eases-ai-safety-rules-amid-pentagon-pressure/">Anthropic Eases AI Safety Rules Amid Pentagon Pressure | ForkLog</a></li>
<li><a href="https://www.eweek.com/news/california-ai-safety-bill-sb-53-anthropic-endorsement/">Anthropic Backs SB 53 – California's Landmark AI Safety Bill</a></li>

</ul>
</details>

**Discussion**: Community sentiment is largely cynical and critical, viewing the move as Anthropic 'selling its soul' under competitive and governmental pressure. Comments range from mocking the company's previous 'safety-conscious' branding to expressing concerns about degraded service quality and accelerated, less-safe development. Some users draw parallels to Google dropping its 'Don't be evil' motto.

**Tags**: `#AI Safety`, `#Anthropic`, `#AI Ethics`, `#Industry News`, `#Policy`

---

<a id="item-5"></a>
## [Anthropic Reports Large-Scale Distillation Attacks on Claude by Chinese AI Labs](https://t.me/zaihuapd/39851) ⭐️ 8.0/10

Anthropic published a report accusing three Chinese AI labs—DeepSeek, Moonshot AI, and MiniMax—of conducting large-scale 'distillation attacks' on its Claude model. The labs allegedly created over 24,000 fraudulent accounts and engaged in more than 16 million conversational interactions to extract Claude's capabilities for training their own models. This incident highlights a significant security and ethical challenge in the AI industry, where model capabilities and safety guardrails are being systematically extracted to bypass export controls and competitive barriers. It underscores the escalating tensions in global AI competition and raises questions about the effectiveness of current safeguards against industrial-scale intellectual property extraction. Anthropic stated that these attacks circumvented safety controls and export restrictions, and the company is now strengthening its defenses using techniques like behavioral fingerprinting. The scale of the operation—millions of interactions across tens of thousands of fake accounts—indicates a coordinated, industrial-level effort rather than isolated research attempts.

telegram · zaihuapd · Feb 25, 04:15

**Background**: Model distillation is a technique where a smaller or less capable model is trained on the outputs of a larger, more powerful model to replicate its capabilities. While knowledge distillation is a legitimate research method, it becomes an 'attack' or 'theft' when used at scale to systematically extract proprietary model intelligence, bypass terms of service, and evade safety filters. AI safety controls are measures implemented by companies like Anthropic to prevent their models from generating harmful, biased, or unsafe content, but techniques like multi-turn prompting can sometimes bypass these safeguards.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks">Detecting and preventing distillation attacks - Anthropic</a></li>
<li><a href="https://www.cnbc.com/2026/02/24/anthropic-openai-china-firms-distillation-deepseek.html">Anthropic joins OpenAI in flagging 'industrial-scale' distillation campaigns by Chinese AI firms - CNBC</a></li>
<li><a href="https://www.reddit.com/r/ClaudeCode/comments/1rcp658/anthropic_weve_identified_industrialscale/">Anthropic: "We've identified industrial-scale distillation attacks on our models by DeepSeek, Moonshot AI, and MiniMax." : r/ClaudeCode - Reddit</a></li>

</ul>
</details>

**Discussion**: The Reddit discussion reveals a debate within the technical community. Some users question why standard 'knowledge distillation' is suddenly being labeled as theft, suggesting a blurry line between legitimate research and malicious extraction. Others express concern about the industrial scale and coordinated nature of the attacks, viewing them as clear violations of terms of service and potential intellectual property infringement.

**Tags**: `#AI Security`, `#Model Distillation`, `#AI Ethics`, `#Anthropic`, `#Chinese AI Labs`

---

<a id="item-6"></a>
## [SMIC's N+3 Process Used for Huawei Kirin 9030, Advancing Toward 5nm-Class Tech](https://t.me/zaihuapd/39857) ⭐️ 8.0/10

TechInsights' analysis, published around December 11, 2025, confirms that Huawei's Kirin 9030 application processor is manufactured using SMIC's N+3 process. This process is a scaled evolution of SMIC's earlier 7nm-class N+2 technology. This represents a significant achievement for China's domestic semiconductor industry, demonstrating progress toward 5nm-class manufacturing capabilities despite international restrictions on acquiring advanced EUV lithography tools. It enables Huawei to source advanced smartphone processors domestically, reducing reliance on foreign foundries. The N+3 process achieves this scaling primarily through innovations in DUV-based patterning and DTCO (Design Technology Co-Optimization), but it still lags behind TSMC and Samsung's 5nm processes in absolute scaling. The process is expected to face significant yield challenges, particularly due to the aggressive scaling of metal pitches using DUV multi-patterning techniques.

telegram · zaihuapd · Feb 25, 08:00

**Background**: Semiconductor process nodes like 5nm are marketing terms for improved generations of chip technology. EUV (Extreme Ultraviolet) lithography is the standard tool for manufacturing leading-edge chips at 7nm and below, but its export to China is restricted. DUV (Deep Ultraviolet) lithography uses a longer wavelength, and achieving finer features requires complex multi-patterning techniques, which increase cost and can impact yield. DTCO is a methodology that co-optimizes chip design and manufacturing process to improve performance and reduce development time.

<details><summary>References</summary>
<ul>
<li><a href="https://www.techinsights.com/blog/smic-n3-confirmed-kirin-9030-analysis-reveals-how-close-smic-5nm">SMIC N+3 Confirmed: Kirin 9030 Analysis Reveals How Close SMIC Is to 5nm | TechInsights</a></li>
<li><a href="https://en.wikipedia.org/wiki/5_nm_process">5 nm process - Wikipedia</a></li>
<li><a href="https://www.tsmc.com/english/news-events/blog-article-20220615">What is DTCO ?: An Introduction to Design-Technology...</a></li>

</ul>
</details>

**Tags**: `#semiconductors`, `#manufacturing`, `#china-tech`, `#huawei`, `#process-technology`

---

<a id="item-7"></a>
## [Chinese Academy of Sciences to stop paying APCs for over 30 high-cost journals like Nature Communications](https://www.science.org/content/article/major-china-funder-plans-curtail-spending-pricey-open-access-fees) ⭐️ 8.0/10

The Chinese Academy of Sciences (CAS) plans to implement a new policy starting March 1, 2026, prohibiting its researchers from using academy funds to pay article processing charges (APCs) for over 30 high-cost international open access journals. The affected journals include Nature Communications, Cell Reports, and Science Advances, which charge APCs of at least $5,000 per article, far exceeding the global average of around $2,000. This represents a major policy shift by one of the world's largest research funders, which could significantly reshape the economics of open access publishing and journal selection patterns globally. The move signals a strategic effort to control escalating research costs and promote the development of domestic journals, potentially influencing the business models of prestigious international publishers. Under the new policy, CAS researchers who lack alternative funding sources will need to opt for the non-open access (subscription) route when publishing in hybrid journals like Nature to avoid fees. The policy specifically targets journals with APCs deemed excessively high, focusing on a list of over 30 titles where fees are more than double the global average.

telegram · zaihuapd · Feb 25, 10:15

**Background**: Article Processing Charges (APCs) are fees paid by authors or their institutions to make research articles freely available upon publication in open access journals. Hybrid journals are subscription-based journals that offer an open access option for individual articles upon payment of an APC, creating a dual revenue stream for publishers. The Chinese Academy of Sciences is a state-run complex of scientific research institutes and a major source of research funding in China.

<details><summary>References</summary>
<ul>
<li><a href="https://www.springernature.com/gp/open-science/journals-books/journal-pricing-faqs">Journal pricing FAQs | Open science - Springer Nature</a></li>
<li><a href="https://en.wikipedia.org/wiki/Hybrid_open-access_journal">Hybrid open-access journal - Wikipedia</a></li>
<li><a href="https://www.science.org/content/article/major-china-funder-plans-curtail-spending-pricey-open-access-fees">Major Chinese funder to stop paying fees for 30 pricey open-access journals | Science</a></li>

</ul>
</details>

**Tags**: `#academic-publishing`, `#open-access`, `#research-funding`, `#science-policy`, `#china-research`

---

<a id="item-8"></a>
## [tldraw moves test suite to private repository over competitive concerns](https://simonwillison.net/2026/Feb/25/closed-tests/#atom-everything) ⭐️ 7.0/10

The tldraw collaborative drawing library is moving its comprehensive test suite from its public GitHub repository to a private one. This decision was reportedly prompted by concerns that detailed tests could enable competitors or AI agents to rebuild the library's functionality from scratch, as demonstrated by Cloudflare's recent project to port Next.js using AI. This move highlights a growing tension for commercial open-source projects (COSS) between maintaining transparency and protecting their intellectual property and business viability. It raises fundamental questions about what core assets should remain open and could set a precedent for other companies to restrict access to tests, potentially altering open-source development practices. It's important to note that tldraw is not under a traditional open-source license; it uses a custom license that requires a commercial license for use in production environments. The team also filed a satirical issue about translating their code to Traditional Chinese to "defend intellectual property" from AI agents, highlighting the broader, often ironic, concerns in the AI era.

rss · Simon Willison · Feb 25, 21:06

**Background**: tldraw is a popular SDK for building infinite canvas and whiteboard applications with real-time collaboration features. Commercial Open Source Software (COSS) companies often release their core code publicly but rely on proprietary extensions, hosted services, or support for revenue. Build tools like Vite and Webpack are used to bundle and optimize web application code, and AI-assisted code generation is becoming increasingly capable of understanding and replicating software based on public artifacts like tests.

<details><summary>References</summary>
<ul>
<li><a href="https://tldraw.dev/">tldraw: Infinite Canvas SDK for React</a></li>
<li><a href="https://github.com/tldraw/tldraw">tldraw/tldraw: very good whiteboard infinite canvas SDK - GitHub</a></li>
<li><a href="https://en.wikipedia.org/wiki/Business_models_for_open-source_software">Business models for open-source software - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#open-source`, `#business-models`, `#testing`, `#intellectual-property`, `#software-engineering`

---

<a id="item-9"></a>
## [Claude Code Launches Remote Control Feature for Multi-Device Access](https://simonwillison.net/2026/Feb/25/claude-code-remote-control/#atom-everything) ⭐️ 7.0/10

Anthropic released a new 'Remote Control' feature for Claude Code yesterday, allowing users to run a session locally on their computer and then send prompts to it from Claude Code's web, iOS, or native desktop app interfaces. The feature is activated by running the `claude remote-control` command in the terminal. This feature significantly enhances the flexibility and accessibility of Claude Code, enabling developers to start a coding or automation task on one device (like a desktop) and continue or monitor it from another (like a phone). It represents a step towards making AI-powered development tools more seamlessly integrated into multi-device workflows, competing with similar offerings like OpenClaw. The initial release has some rough edges: users may encounter account permission errors, the `--dangerously-skip-permissions` flag appears ineffective, and API 500 errors can occur. Furthermore, only one remote session can run per machine, and sessions terminate ungracefully if the local program is restarted.

rss · Simon Willison · Feb 25, 17:33

**Background**: Claude Code is a developer tool from Anthropic that allows users to interact with AI models (like Claude Opus and Sonnet) through a terminal or desktop app to execute code, automate tasks, and control applications. It typically operates locally on a user's machine. The 'Claw category' of software, mentioned for comparison, refers to tools like OpenClaw that enable remote control and automation of personal computers, often featuring scheduled task execution.

<details><summary>References</summary>
<ul>
<li><a href="https://code.claude.com/docs/en/remote-control">Continue local sessions from any device with Remote Control - Claude Code Docs</a></li>
<li><a href="https://venturebeat.com/orchestration/anthropic-just-released-a-mobile-version-of-claude-code-called-remote">Anthropic just released a mobile version of Claude Code called Remote Control | VentureBeat</a></li>

</ul>
</details>

**Tags**: `#AI Development`, `#Claude Code`, `#Developer Tools`, `#Remote Control`

---

<a id="item-10"></a>
## [Effort to Secure Network Time Protocol Gains Momentum with NTS Adoption Push](https://lwn.net/Articles/1059200/) ⭐️ 7.0/10

At FOSDEM 2026, Ruben Nijveld from the Trifecta Tech Foundation presented work to accelerate the adoption of Network Time Security (NTS), the IETF's RFC-8915 standard for securing NTP traffic. The foundation, with additional funding from ICANN, is testing technologies to help major time servers like pool.ntp.org implement NTS more easily. NTP is a foundational internet protocol used universally for time synchronization, but it is fundamentally insecure and vulnerable to spoofing attacks. Securing it with NTS is critical because accurate, trusted time underpins countless systems, from authentication (Kerberos, TOTP) and distributed computing to cellular networks, financial trading, and power grids. NTS focuses on providing authentication and integrity for NTP packets rather than encrypting the time data itself, as the payload is public. The standard leverages Transport Layer Security (TLS) for initial key exchange and uses Authenticated Encryption with Associated Data (AEAD) to protect subsequent time synchronization exchanges.

rss · LWN.net · Feb 25, 14:26

**Background**: The Network Time Protocol (NTP), created in 1985, is used to synchronize computer clocks across the internet with Coordinated Universal Time (UTC), often referencing atomic clocks (Stratum 0 sources). It operates in a hierarchical client-server model but was designed without built-in security, making it susceptible to man-in-the-middle attacks where timestamps can be altered. Network Time Security (NTS) is a cryptographic mechanism defined in IETF RFC 8915 specifically to add authentication and integrity to NTP, addressing this long-standing vulnerability.

<details><summary>References</summary>
<ul>
<li><a href="https://datatracker.ietf.org/doc/html/rfc8915">RFC 8915: Network Time Security for the Network Time Protocol</a></li>
<li><a href="https://www.rfc-editor.org/info/rfc8915">Information on RFC 8915</a></li>

</ul>
</details>

**Tags**: `#network-security`, `#time-synchronization`, `#protocols`, `#infrastructure`

---

<a id="item-11"></a>
## [Benchmark reveals Q4_K_M outperforms UD-Q4_K_XL for Qwen3.5-35B-A3B quantization on RTX 5080.](https://www.reddit.com/r/LocalLLaMA/comments/1rei65v/qwen3535ba3b_quantization_quality_speed/) ⭐️ 7.0/10

A user ran detailed benchmarks on the Qwen3.5-35B-A3B model using llama.cpp on an RTX 5080 system, comparing the quality and speed of three quantization methods: Q8_0, Q4_K_M, and UD-Q4_K_XL. The results showed that the Unsloth Dynamic quant (UD-Q4_K_XL) performed significantly worse than the standard Q4_K_M, with nearly 10% higher perplexity and a larger file size. This benchmark provides crucial, practical guidance for the local LLM community on how to efficiently run large, state-of-the-art Mixture-of-Experts (MoE) models like Qwen3.5 on consumer hardware with limited VRAM. It highlights that not all advanced quantization techniques are universally beneficial, and choosing the wrong method can lead to significant performance degradation. The test used a CPU/GPU offloading setup over PCIe 5.0 because the full model didn't fit in the 16GB VRAM. The standard Q4_K_M quant achieved a perplexity of 6.6688 on WikiText-2 (only 2.1% worse than the Q8_0 baseline), while being nearly half the size. The author specifically recommends against using UD-Q4_K_XL for this MoE architecture, citing consistency with other reports.

reddit · r/LocalLLaMA · gaztrab · Feb 25, 16:35

**Background**: Quantization is a technique to reduce the memory and computational cost of large language models by representing their weights with fewer bits (e.g., 4-bit instead of 16-bit). llama.cpp is a popular framework for running LLMs locally, supporting various quantization formats like Q8_0 (8-bit) and Q4_K_M (a specific 4-bit method). Mixture-of-Experts (MoE) models, like Qwen3.5-35B-A3B, use a sparse architecture where only parts of the model are activated per input, making them more efficient but sometimes sensitive to quantization strategies.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF/discussions/6">unsloth/Qwen3-30B-A3B-GGUF · `UD-Q4_K_XL` or `Q4_K_M`?</a></li>
<li><a href="https://github.com/ggml-org/llama.cpp/discussions/2094">Difference in different quantization methods · ggml-org/llama.cpp · Discussion #2094</a></li>

</ul>
</details>

**Discussion**: The community engaged deeply with the technical findings. One user questioned how "free" the performance gain from using q8_0 for the KV cache really is, suggesting further tests. Another was grateful for the specific configuration tips, which drastically improved their own inference speed. Several comments debated the merits of perplexity versus KL Divergence as a quality metric and suggested alternative quants like Bartowski's Q4_K_L might offer better trade-offs.

**Tags**: `#quantization`, `#llama.cpp`, `#benchmarking`, `#local-llm`, `#hardware-performance`

---

<a id="item-12"></a>
## [OpenAI adds WebSocket support to Responses API, speeding up long-chain tasks by 40%](https://developers.openai.com/api/docs/guides/websocket-mode) ⭐️ 7.0/10

OpenAI has introduced a WebSocket mode for its Responses API, specifically optimized for complex workflows involving frequent tool calls. This mode, by establishing persistent connections and supporting incremental input, can improve the execution speed of long-chain tasks containing more than 20 tool calls by approximately 40%. This update significantly reduces latency for developers building agentic AI applications, such as coding assistants or orchestration loops, which require many model-tool interactions. It represents a meaningful performance enhancement for the growing ecosystem of complex, multi-step AI workflows. The WebSocket mode is compatible with Zero Data Retention (ZDR) specifications and supports low-latency context continuation using a `previous_response_id`. Currently, a single connection is limited to a duration of 60 minutes.

telegram · zaihuapd · Feb 25, 07:15

**Background**: The OpenAI Responses API is designed to simplify building AI agents by providing a chat-like format with built-in tool calling capabilities, such as web search, file search, and computer use. WebSocket is a communication protocol that provides full-duplex communication channels over a single TCP connection, allowing for persistent, low-latency data exchange between a client and server. Zero Data Retention (ZDR) is a policy where service providers do not store user data, which is important for handling confidential information in AI applications.

<details><summary>References</summary>
<ul>
<li><a href="https://developers.openai.com/api/docs/guides/websocket-mode">WebSocket Mode | OpenAI API</a></li>
<li><a href="https://www.panewslab.com/en/articles/019c93d3-d0f1-75fc-ae81-fdcdd120da63">OpenAI adds WebSocket support to the Responses API, speeding up long ...</a></li>
<li><a href="https://openrouter.ai/docs/guides/features/zdr">Zero Data Retention | How... | OpenRouter | Documentation</a></li>

</ul>
</details>

**Tags**: `#OpenAI`, `#API`, `#WebSocket`, `#Performance`, `#AI-Workflows`

---

<a id="item-13"></a>
## [Uber Employees Use AI Clone of CEO to Rehearse Presentations](https://www.businessinsider.com/uber-employees-use-ai-clone-ceo-prepare-meetings-presentations-2026-2) ⭐️ 7.0/10

Uber CEO Dara Khosrowshahi revealed that some teams have developed a digital clone called 'Dara AI' to help employees rehearse presentations before meeting with him in person. He also stated that approximately 30% of Uber's engineers are now AI power users, and the company may prioritize investing in GPU compute resources over expanding headcount if AI significantly boosts engineering efficiency. This demonstrates a novel, practical application of generative AI in corporate workflows, moving beyond content creation to simulating executive feedback for skill development. It signals a strategic shift in resource allocation for tech companies, where investment in computational power (GPUs) is being weighed against traditional human capital expansion, potentially reshaping future workforce planning. Khosrowshahi noted that while AI can process vast amounts of data, it still faces challenges in making decisions based on real-time, novel information and cannot fully replace executive functions. The 'Dara AI' tool is specifically used to help employees fine-tune slides and presentation details.

telegram · zaihuapd · Feb 25, 08:45

**Background**: Digital cloning is an emerging technology that uses deep-learning algorithms to create a digital replica of a person's communication style, voice, and knowledge. Graphics Processing Units (GPUs) are specialized processors ideal for parallel computation and have become the backbone of the AI economy, powering the training and running of complex AI models. In corporate strategy, 'headcount' refers to the total number of employees, and strategic planning often involves balancing human resources with technological investments.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Digital_cloning">Digital cloning - Wikipedia</a></li>
<li><a href="https://www.ensureias.com/blog/current-affairs/graphics-processing-units-gpus-from-gaming-hardware-to-the-backbone-of-the-ai-economy">Graphics Processing Units ( GPUs ): From Gaming Hardware to the...</a></li>
<li><a href="https://www.aihr.com/blog/fte-vs-headcount/">FTE vs . Headcount : The Key Differences HR Should Know - AIHR</a></li>

</ul>
</details>

**Tags**: `#AI Applications`, `#Corporate Strategy`, `#Future of Work`, `#Generative AI`, `#Business Automation`

---

<a id="item-14"></a>
## [QingLong Panel Compromised by Cryptojacking Malware, CPU Usage Spikes to 800%](https://qxhut.com/?id=52) ⭐️ 7.0/10

On February 7, 2026, multiple users reported that the QingLong Panel container management platform was compromised by a cryptocurrency mining malware named .fullgc, causing abnormal server CPU usage to spike to 800%. The malware achieves persistence by tampering with the config.sh configuration file and can automatically download malicious programs based on the system architecture. This incident is significant because QingLong Panel is a popular open-source tool for managing scheduled tasks and scripts, widely used by developers and DevOps teams for self-hosting. A successful cryptojacking attack on such a platform can silently hijack significant computing resources from numerous servers, leading to inflated cloud costs, degraded performance for legitimate services, and potential security breaches beyond just resource theft. Security analysis identifies the malware as part of the SusMiner family, which primarily connects to XMR (Monero) mining pools for illicit cryptocurrency mining. The primary attack targets are servers with their QingLong Panel management ports exposed to public IPv4 networks. Users are advised to check for hidden files in the `/ql/data/db/` directory.

telegram · zaihuapd · Feb 25, 14:24

**Background**: QingLong Panel is an open-source, Docker-based tool for managing and automating scheduled tasks (like JavaScript and Python scripts), commonly used for various online automation needs. Cryptojacking, or crypto-mining malware, is malicious software that hijacks a victim's computing resources to mine cryptocurrencies without their consent, often leading to high CPU/GPU usage and increased energy costs. Monero (XMR) is a privacy-focused cryptocurrency often targeted by such malware due to its mining algorithm being compatible with general-purpose CPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://lmntrix.com/blog/analysis-of-coin-miner-malware/">Analysis of Coin Miner Malware - LMNTRIX Blog</a></li>
<li><a href="https://miningpoolstats.stream/monero">Monero ( XMR ) RandomX | Mining Pools</a></li>

</ul>
</details>

**Tags**: `#security`, `#malware`, `#container-security`, `#cryptojacking`, `#devops`

---