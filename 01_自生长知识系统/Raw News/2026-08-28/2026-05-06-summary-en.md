---
layout: default
title: "Horizon Summary: 2026-05-06 (EN)"
date: 2026-05-06
lang: en
---

> From 48 items, 19 important content pieces were selected

---

1. [Gemma 4 Multi-Token Prediction Draft Models Released for 2x Speedup](#item-1) ⭐️ 9.0/10
2. [State Health Exchanges Leak Sensitive Data to Big Tech](#item-2) ⭐️ 9.0/10
3. [SGLang v0.5.11 Boosts Inference with CUDA 13 and Speculative Decoding](#item-3) ⭐️ 8.0/10
4. [DNSSEC Misconfiguration Causes Widespread .de Outage](#item-4) ⭐️ 8.0/10
5. [Computer Use: 45x More Expensive Than Structured APIs](#item-5) ⭐️ 8.0/10
6. [Anthropic Releases Financial Services Agent Templates](#item-6) ⭐️ 8.0/10
7. [Google Chrome Silently Installs 4 GB AI Model on Devices](#item-7) ⭐️ 8.0/10
8. [When Everyone Has AI and the Company Still Learns Nothing](#item-8) ⭐️ 8.0/10
9. [IBM objected to Microsoft using Tab for dialog navigation](#item-9) ⭐️ 8.0/10
10. [Zuckerberg Authorized Meta's Copyright Infringement for AI Training](#item-10) ⭐️ 8.0/10
11. [Heretic 1.3: Reproducible Uncensoring with Benchmarking and VRAM Reduction](#item-11) ⭐️ 8.0/10
12. [ProgramBench Tests AI Agents on Binary Reconstruction from Scratch](#item-12) ⭐️ 8.0/10
13. [DeepSeek V4 Pro matches GPT-5.2 on FoodTruck Bench at 17x lower cost](#item-13) ⭐️ 8.0/10
14. [Trump Administration Considers Pre-Release Review for AI Models](#item-14) ⭐️ 8.0/10
15. [Image Models Drive 6.5x More AI App Downloads Than Chatbot Updates](#item-15) ⭐️ 8.0/10
16. [GitHub Apologizes for Outages, Announces 30x Scaling Plan](#item-16) ⭐️ 8.0/10
17. [UK Online Safety Act Age Checks Bypassed with Fake Beards](#item-17) ⭐️ 8.0/10
18. [OpenAI's GPT-5.3 Instant Reduces Hallucinations by Up to 26.8%](#item-18) ⭐️ 8.0/10
19. [Microsoft Edge Stores Passwords in Cleartext in Memory](#item-19) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Gemma 4 Multi-Token Prediction Draft Models Released for 2x Speedup](https://www.reddit.com/r/LocalLLaMA/comments/1t4jq6h/gemma_4_mtp_released/) ⭐️ 9.0/10

Google has released multi-token prediction (MTP) draft models for Gemma 4 (31B, 26B-A4B, E4B, and E2B variants) on Hugging Face. These models enable up to 2x faster text generation through speculative decoding while guaranteeing identical quality to standard decoding. This release brings major efficiency gains to local and on-device AI applications, reducing latency without compromising accuracy. It also reinforces Google's commitment to open-source AI, offering developers a practical tool for more responsive and cost-effective inference. The MTP draft models are lightweight attachments; for example, the E2B draft model is only 78M parameters. They work by predicting multiple tokens ahead, which the target Gemma 4 model then verifies in parallel, achieving speedups up to 2x. Models are available on Hugging Face, and integration is expected in frameworks like llama.cpp and LM Studio.

reddit · r/LocalLLaMA · rerri · May 5, 16:01

**Background**: Multi-token prediction (MTP) is a technique where a model predicts several future tokens at once, improving inference efficiency. Speculative decoding uses a small draft model to propose tokens, which a larger target model verifies in a single pass, ensuring the output distribution exactly matches that of the target model. Google's implementation extends Gemma 4 with draft models specifically trained for MTP, enabling fast, accurate inference on resource-constrained devices.

<details><summary>References</summary>
<ul>
<li><a href="https://grokipedia.com/page/Multi-token_prediction">Multi-token prediction</a></li>
<li><a href="https://en.wikipedia.org/wiki/Speculative_decoding">Speculative decoding</a></li>

</ul>
</details>

**Discussion**: The community reacted with strong enthusiasm, highlighting the impressive speedups and tiny draft model sizes (e.g., the 78M E2B variant). Users shared visual guides and discussed integration with tools like LM Studio and llama.cpp. Some noted that Gemma models already tend to generate outputs using fewer tokens, which further amplifies the speed benefits. Overall sentiment is highly positive, with few reservations.

**Tags**: `#multi-token-prediction`, `#gemma-4`, `#speculative-decoding`, `#llm-efficiency`, `#google`

---

<a id="item-2"></a>
## [State Health Exchanges Leak Sensitive Data to Big Tech](https://www.bloomberg.com/features/2026-healthcare-advertising-trackers-privacy/) ⭐️ 9.0/10

A Bloomberg investigation found that nearly 20 US state health insurance exchanges embedded advertising tracking pixels, leaking race, gender, citizenship, zip codes, and other sensitive data of over 7 million users to Meta, TikTok, Google, and LinkedIn. This breach exposes highly sensitive health and demographic data, potentially violating HIPAA and state privacy laws, and eroding public trust; it also highlights the pervasive surveillance by ad-tech companies on government websites. Specific instances include Washington DC sending race and citizenship data to TikTok, Virginia transmitting zip codes to Meta for ad targeting, and New York sharing browsing history on family incarceration; other states leaked Medicaid application and non-citizen pregnancy benefit access to Google or Meta.

telegram · zaihuapd · May 5, 03:06

**Background**: Advertising tracking pixels are tiny, invisible images or scripts embedded in web pages that collect user behavior for targeted advertising. State health insurance exchanges are government-run marketplaces created under the Affordable Care Act, where individuals apply for health plans and must provide sensitive personal and financial information, making the presence of such trackers a severe privacy violation.

<details><summary>References</summary>
<ul>
<li><a href="https://kakunin-ip.click/zh/glossary/tracking-pixel">什么是追踪像素 - 工作原理、检测方法与防护措施 | IP确认酱</a></li>
<li><a href="https://yaoweibin.cn/pixel-tracking-explained/">在不到5分钟内解释像素追踪 - 姚伟斌</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#data-leak`, `#healthcare`, `#big-tech`, `#advertising-trackers`

---

<a id="item-3"></a>
## [SGLang v0.5.11 Boosts Inference with CUDA 13 and Speculative Decoding](https://github.com/sgl-project/sglang/releases/tag/v0.5.11) ⭐️ 8.0/10

SGLang v0.5.11 upgrades default CUDA to 13.0 and PyTorch to 2.11, enables speculative decoding V2 as default with overlap scheduling to reduce CPU overhead, adds decode-side radix cache for prefill/decode disaggregation, and introduces DFLASH kernel, FA3 community kernels, LoRA for DeepSeek-V3/Kimi-K2, and cookbook support for many new models including Gemma 4, GLM-5.1, and Qwen3.6. This release modernizes the inference stack with latest hardware support, reduces latency through default speculative decoding, and enables efficient disaggregated serving with radix cache, benefiting large-scale LLM deployments across text and diffusion models. Spec V2 overlap scheduling hides CPU overhead; decode radix cache recovers TTFT savings for shared prefixes; DFLASH kernel expanded to AMD ROCm; CP enhancements allow independent tuning of MoE and attention parallelism; FlashInfer CuteDSL MoE backend is provided for the FP4 path; new models are accompanied by cookbook recipes for tuned deployment.

github · Kangyan-Zhou · May 5, 21:28

**Background**: Speculative decoding accelerates LLM inference by using a draft model to propose multiple tokens verified by the target model in one pass. Prefill/decode disaggregation separates prompt processing (prefill) from token generation (decode) across instances for better resource use. RadixAttention in SGLang automatically reuses KV cache across requests, with radix cache storing shared prefixes as a tree for efficient lookup.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Speculative_decoding">Speculative decoding</a></li>
<li><a href="https://www.lmsys.org/blog/2024-01-17-sglang/">Fast and Expressive LLM Inference with RadixAttention and SGLang - LMSYS Blog | LMSYS Org</a></li>
<li><a href="https://bentoml.com/llm/inference-optimization/prefill-decode-disaggregation">Prefill-decode disaggregation | LLM Inference Handbook</a></li>

</ul>
</details>

**Tags**: `#sglang`, `#inference`, `#cuda`, `#speculative-decoding`, `#model-serving`

---

<a id="item-4"></a>
## [DNSSEC Misconfiguration Causes Widespread .de Outage](https://dnssec-analyzer.verisignlabs.com/nic.de) ⭐️ 8.0/10

DENIC, the registry for .de, published a malformed RRSIG signature over an NSEC3 record that failed validation against ZSK keytag 33834, causing all DNSSEC-validating resolvers to return SERVFAIL for .de domains. The zone data itself was intact, and non-validating resolvers were unaffected. This incident demonstrates the fragility of DNSSEC's centralized trust model, where a single registry-level misconfiguration can take down all domains under a TLD for validating users, affecting millions of German sites. It reignites debates over DNSSEC's security trade-offs and reliability. The malformed RRSIG was on the NSEC3 record for a0d5d1p51kijsevll74k523htmq406bk.de, associated with keytag 33834. The outage was intermittent due to anycast, as some DENIC nameserver nodes served the bad signature while others did not. Only validating resolvers were affected.

hackernews · warpspin · May 5, 20:16 · [Discussion](https://news.ycombinator.com/item?id=48027897)

**Background**: DNSSEC adds cryptographic signatures to DNS records, enabling resolvers to verify authenticity through a trust chain from the root zone to individual domains. DENIC, the .de registry, signs zone data with zone signing keys. A malformed RRSIG can cause validators to reject all records, effectively making domains unreachable for users behind those resolvers.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DNSSEC">DNSSEC</a></li>
<li><a href="https://www.cloudflare.com/learning/dns/dnssec/how-dnssec-works/">How Does DNSSEC Work? | Cloudflare</a></li>

</ul>
</details>

**Discussion**: Comments quickly identified the malformed RRSIG and keytag, with some humor about a DENIC party. Broader debate referenced Thomas Ptacek's critique of DNSSEC and concerns over the centralized point of failure it introduces, making the decentralized DNS more fragile. Historical DNSSEC outage lists were also mentioned, highlighting a pattern of similar incidents.

**Tags**: `#dnssec`, `#outage`, `#dns`, `#security`, `#infrastructure`

---

<a id="item-5"></a>
## [Computer Use: 45x More Expensive Than Structured APIs](https://reflex.dev/blog/computer-use-is-45x-more-expensive-than-structured-apis/) ⭐️ 8.0/10

A cost analysis reveals that using AI agents with computer vision to navigate UIs costs approximately 45 times more than relying on structured API calls, prompting discussion on mitigation strategies and alternative approaches. This cost disparity could severely limit the scalability of vision-based AI agents in production, pushing developers toward more efficient methods like accessibility APIs or UI pre-mapping, and reshaping AI automation economics. The cost stems from high token consumption of processing multiple screenshots per action, while structured APIs return only necessary data. Mitigation includes using accessibility APIs that expose a semantic UI tree or mapping the UI once into an API-like interface.

hackernews · palashawas · May 5, 16:34 · [Discussion](https://news.ycombinator.com/item?id=48024859)

**Background**: AI agents with 'computer use' capabilities (e.g., Anthropic's Claude, OpenAI's tools) interact with UIs by taking screenshots and simulating mouse and keyboard actions, consuming vision model tokens per step. Structured APIs return data in machine-readable formats with far fewer tokens. This cost comparison arises from the radical difference in token requirements.

<details><summary>References</summary>
<ul>
<li><a href="https://developers.openai.com/api/docs/guides/tools-computer-use">Computer use | OpenAI API</a></li>
<li><a href="https://grokipedia.com/page/OS_AI_Computer_Use">OS AI Computer Use</a></li>

</ul>
</details>

**Discussion**: Community comments suggest practical fixes: using accessibility APIs to cut costs, pre-mapping UIs for repeatable workflows, and minimizing visual tooling. Some note that existing SaaS obfuscation can make agents even costlier. A few express skepticism about security and privacy risks of granting agents full computer access.

**Tags**: `#AI agents`, `#computer vision`, `#API economics`, `#cost analysis`, `#developer tools`

---

<a id="item-6"></a>
## [Anthropic Releases Financial Services Agent Templates](https://www.anthropic.com/news/finance-agents) ⭐️ 8.0/10

Anthropic announced ten ready-to-run agent templates for financial services, deployable as plugins or cookbooks for tasks like pitch building, KYC screening, and reconciliation. This move intensifies the AI arms race in regulated finance, potentially accelerating automation but raising concerns over bias, regulatory risk, and market concentration. The templates do not grant agents control over lending or approval decisions, which may mitigate immediate risk but limits deployment scope; they are part of a broader push following a $1.5 billion joint venture with Wall Street firms.

hackernews · louiereederson · May 5, 15:05 · [Discussion](https://news.ycombinator.com/item?id=48023533)

**Background**: Anthropic is an AI safety company known for its Claude models. Financial services involve sensitive data and strict regulations. Agent templates are pre-built workflows that help automate complex tasks, often leveraging large language models. Cookbooks are instructional guides, and plugins extend platform capabilities.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/news/finance-agents">Agents for financial services and insurance \ Anthropic</a></li>
<li><a href="https://www.investmentnews.com/fintech/anthropic-rolls-out-financial-services-agents-as-arms-race-with-openai-heats-up/266445">Anthropic rolls out financial services agents as arms race ...</a></li>

</ul>
</details>

**Discussion**: Comments reflect skepticism about AI expertise in sensitive domains, concerns that templates are scattershot and could stifle startups, and reports of bias in Claude Opus 4.7; some question whether these tools are actually being used.

**Tags**: `#ai`, `#finance`, `#agents`, `#anthropic`, `#bias`

---

<a id="item-7"></a>
## [Google Chrome Silently Installs 4 GB AI Model on Devices](https://www.thatprivacyguy.com/blog/chrome-silent-nano-install/) ⭐️ 8.0/10

Google Chrome has started silently downloading a 4 GB on-device AI model (Gemini Nano) as part of a recent update, without explicit user consent or notification. This silent installation consumes significant disk space and bandwidth, particularly affecting users with limited resources and IT administrators managing shared environments. It also raises privacy and consent concerns about auto-updating software. The model file is named weights.bin and stored in the OptGuideOnDeviceModel directory. It is the Gemini Nano model, with CPU and GPU variants of ~2.7 GiB and ~4.0 GiB respectively. Users can disable it via chrome://flags by turning off 'Enables optimization guide on device' and 'Prompt API for Gemini Nano'. Google has since published a help page for managing on-device AI models.

hackernews · john-doe · May 5, 07:34 · [Discussion](https://news.ycombinator.com/item?id=48019219)

**Background**: Gemini Nano is an on-device large language model developed by Google, enabling AI tasks like text generation directly on the device without cloud processing. Chrome is integrating such models to offer features like the Prompt API for web developers. The file weights.bin contains the model's learned parameters. This move reflects a broader trend of browsers incorporating local AI to improve privacy and speed, but it also raises deployment and transparency challenges.

<details><summary>References</summary>
<ul>
<li><a href="https://cybernews.com/security/google-chrome-ai-model-device-no-consent/">Guy finds Google Chrome is quietly installing a 4GB AI model on our devices</a></li>
<li><a href="https://support.google.com/chrome/answer/16961953?hl=en">Manage on-device Generative AI models in Chrome - Google Chrome Help</a></li>
<li><a href="https://developer.chrome.com/docs/ai/built-in">Built-in AI | AI on Chrome | Chrome for Developers</a></li>

</ul>
</details>

**Discussion**: Community reactions are split. Some view it as a normal part of software updates, while others highlight severe practical impacts on shared IT systems (e.g., NFS home directories, lab machines) where repeated downloads cause storage bloat. Users have shared flags and scripts to disable the model, and there is call for a system-wide, single-copy installation to avoid redundancy.

**Tags**: `#chrome`, `#ai`, `#privacy`, `#disk-usage`, `#software-updates`

---

<a id="item-8"></a>
## [When Everyone Has AI and the Company Still Learns Nothing](https://www.robert-glaser.de/when-everyone-has-ai-and-the-company-still-learns-nothing/) ⭐️ 8.0/10

Despite widespread individual adoption of AI coding tools by developers, companies fail to capture organizational learning because rigid processes and misaligned incentives prevent knowledge sharing, according to a critical analysis. This matters because AI's productivity gains remain isolated to individuals, failing to improve enterprise efficiency unless companies address systemic bottlenecks and reward collaborative improvement. AI accelerates code production, but downstream processes like testing and deployment scheduling are bottlenecks that worsen as output increases; developers lack recognition for sharing their AI productivity techniques.

hackernews · youngbrioche · May 5, 09:30 · [Discussion](https://news.ycombinator.com/item?id=48020063)

**Background**: Organizational learning is the process by which a company adapts and improves its collective knowledge. In software development, AI tools like GitHub Copilot can drastically speed up coding, but enterprises often have multi-month release cycles requiring extensive testing, change management, and manual approvals. The 'messy middle' refers to the operational gap between a working prototype and production deployment, where most process friction occurs.

**Discussion**: Community comments broadly agree that individual AI productivity gains are not translating to organizational improvement. They highlight that bureaucratic processes are the real bottleneck, and there is no incentive for developers to share AI techniques, leading to fragmented, self-interested adoption. Some express concern that AI is being used to extract more work without proper compensation.

**Tags**: `#AI`, `#enterprise`, `#software development`, `#organizational learning`, `#productivity`

---

<a id="item-9"></a>
## [IBM objected to Microsoft using Tab for dialog navigation](https://devblogs.microsoft.com/oldnewthing/20260505-00/?p=112298) ⭐️ 8.0/10

A blog post reveals that IBM once objected to Microsoft using the Tab key to move between dialog fields, a decision that influenced early Windows UI conventions. This illustrates how corporate rivalries and legacy standards shaped modern interaction design, reminding us that even basic keyboard shortcuts were once contested. The story highlights that IBM had its own Tab usage on 3270 terminals, yet opposed Microsoft's implementation, possibly due to concerns over context-confusion between input and control characters.

hackernews · SeenNotHeard · May 5, 17:28 · [Discussion](https://news.ycombinator.com/item?id=48025687)

**Background**: In early graphical user interfaces, keyboard navigation for dialogs was not standardized. The Tab key, originally for tabulation in text, was repurposed to move focus between controls. IBM, a major keyboard manufacturer and mainframe vendor, had established usage patterns that Microsoft’s approach could disrupt.

**Discussion**: Comments reflect a mix of sentiments: one shares a story of IBM’s excessive bureaucracy, another notes IBM’s own Tab usage on 3270 terminals, while others discuss the inconvenience of the Tab key being hijacked by OS/UI behavior and question IBM’s exact reasoning.

**Tags**: `#history`, `#user-interface`, `#keyboard`, `#IBM`, `#Microsoft`

---

<a id="item-10"></a>
## [Zuckerberg Authorized Meta's Copyright Infringement for AI Training](https://variety.com/2026/digital/news/meta-ai-mark-zuckerberg-copyright-infringement-lawsuit-publishers-scott-turow-1236738383/) ⭐️ 8.0/10

A lawsuit alleges that Mark Zuckerberg personally authorized and encouraged Meta to use copyrighted materials without permission for training AI models, involving large-scale data scraping that ignored robots.txt directives. This case could establish personal liability for corporate executives in copyright infringement, potentially reshaping how tech companies source training data and setting a critical legal precedent for the AI industry. The allegations involve scraping millions of copyrighted works with direct involvement from Zuckerberg; previous Anthropic case gave $1.5 billion settlement for 500,000 pirated works, implying potentially huge damages given statutory minimums of $750 per infringement.

hackernews · spankibalt · May 5, 18:04 · [Discussion](https://news.ycombinator.com/item?id=48026207)

**Background**: AI training often relies on web-scraped data, sparking legal debates over copyright. The Anthropic settlement established that while training itself may be transformative, acquiring pirated works for that purpose is infringement. This case uniquely targets a CEO's personal authorization, challenging the corporate shield that typicallyprotects executives.

**Discussion**: Commenters overwhelmingly support personal liability, sharing experiences of Meta ignoring robots.txt and straining servers. Many hope for severe punishment to deter future infringement and set a precedent that would even allow open sharing by others. Some criticize the typical corporate avoidance of personal accountability.

**Tags**: `#artificial-intelligence`, `#copyright-infringement`, `#legal-precedent`, `#meta`, `#data-scraping`

---

<a id="item-11"></a>
## [Heretic 1.3: Reproducible Uncensoring with Benchmarking and VRAM Reduction](https://www.reddit.com/r/LocalLLaMA/comments/1t4hwup/heretic_13_released_reproducible_models/) ⭐️ 8.0/10

Heretic 1.3 introduces reproducible model runs, an integrated benchmarking system, reduced peak VRAM usage, and broader model support. It captures full environment details like PyTorch version and GPU driver to ensure reproducibility. Reproducible decensoring fosters trust and scientific rigor in open-source AI, while the integrated benchmarks streamline evaluation of decensored models. These improvements accelerate community-driven innovation and adoption. The release overcomes reproducibility challenges by recording all tensor operation dependencies, including GPU and driver specifics. It reduces VRAM usage and expands model support, though some models like Kimi k2.5/k2.6 are reported not yet compatible.

reddit · r/LocalLLaMA · -p-e-w- · May 5, 14:57

**Background**: Heretic is an open-source tool for automatically removing censorship from large language models (LLMs), a process known as abliteration. LLMs often contain refusal patterns for sensitive topics, and Heretic aims to eliminate these while preserving intelligence. Reproducibility is critical to verify that decensoring works consistently across different systems.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/p-e-w/heretic">GitHub - p-e-w/heretic: Fully automatic censorship removal for language models · GitHub</a></li>
<li><a href="https://aimultiple.com/reproducible-ai">Reproducible AI: Why it Matters & How to Improve it</a></li>

</ul>
</details>

**Discussion**: Community reception is overwhelmingly positive, with users calling Heretic the greatest OSS project for local LLMs. Discussions include questions about support for specific models like Kimi k2.5/k2.6 and upcoming MTP architecture, along with ongoing concerns about a competitor copying code.

**Tags**: `#LLM`, `#model-decensoring`, `#open-source`, `#benchmarking`, `#LocalLLaMA`

---

<a id="item-12"></a>
## [ProgramBench Tests AI Agents on Binary Reconstruction from Scratch](https://www.reddit.com/gallery/1t4j4s9) ⭐️ 8.0/10

Facebook Research introduced ProgramBench, a formal benchmark of 200 tasks that challenges AI agents to rebuild binaries from scratch with no internet, decompilation, or structural hints, using only black-box behavioral tests. It provides a rigorous, cheat-proof evaluation of AI agents' independent software engineering capabilities, highlighting current limitations and guiding future improvements in agentic coding systems. The benchmark used 6M lines of behavioral tests filtered to the best, and all models achieved 0% fully resolved tasks; best almost-resolved rate was 95% test pass. It is open-source and installable via pip.

reddit · r/LocalLLaMA · klieret · May 5, 15:40 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1t4j4s9/programbench_can_we_really_rebuild_huge_binaries/)

**Background**: In computing, a benchmark is a standardized test to evaluate performance. ProgramBench evaluates AI agents on reconstructing software binaries from scratch, meaning the agent must generate code that replicates the behavior of a given executable without access to its source code or implementation hints. Testing is performed via black-box behavioral tests, which verify only the external behavior of the generated program, not its internal structure, unlike typical coding benchmarks that provide function signatures or partial code.

<details><summary>References</summary>
<ul>
<li><a href="https://programbench.com/">ProgramBench</a></li>
<li><a href="https://benchlm.ai/benchmarks/programBench">ProgramBench Benchmark 2026: 9 model averages | BenchLM.ai</a></li>

</ul>
</details>

**Discussion**: Community reaction is mixed: some praise its rigor and potential for advancing AI coding, while others criticize its lack of real-world practicality, noting that even humans would struggle under the same restrictions. There is also interest in integrating it with custom harnesses and amusement at the website's vibecoded flaws.

**Tags**: `#benchmarks`, `#code-generation`, `#AI-agents`, `#LLM-evaluation`, `#software-engineering`

---

<a id="item-13"></a>
## [DeepSeek V4 Pro matches GPT-5.2 on FoodTruck Bench at 17x lower cost](https://i.redd.it/fx89f3w5n9zg1.png) ⭐️ 8.0/10

DeepSeek V4 Pro has become the first Chinese model to reach the frontier tier on FoodTruck Bench, a 30-day agentic simulation. It matched GPT-5.2's median outcome within 3% only ten weeks later, while costing ~17× less per API call. This result signals that the China–US frontier AI gap is closing rapidly, now measured in weeks rather than a year. The 17× cost efficiency could democratize access to top-tier agentic AI and shift market dynamics toward more affordable high-performance models. DeepSeek’s pricing is based on a promotional rate of $0.435/M input and $0.87/M output, but historically such promos become permanent. On consistency, DeepSeek outperformed Grok 4.3 with zero loans, 6× less food waste, and 30% more meals served, though Opus 4.6 still holds the highest peak performance.

reddit · r/LocalLLaMA · Disastrous_Theme5906 · May 5, 06:51 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1t47qbw/deepseek_v4_pro_matches_gpt52_on_foodtruck_bench/)

**Background**: FoodTruck Bench is an agentic AI benchmark that simulates running a food truck for 30 days using 34 tools (location, pricing, inventory, staff, weather, events) with persistent memory and daily reflection. Agentic AI refers to autonomous systems that plan, use tools, and adapt to achieve goals in complex environments, evolving beyond static chatbots.

<details><summary>References</summary>
<ul>
<li><a href="https://x.com/foodtruckbench/status/2051559134626218130">Leaderboard update on FoodTruck Bench, our agentic benchmark ...</a></li>
<li><a href="https://aiproductivity.ai/news/gemma-4-31b-foodtruck-bench-results/">Gemma 4 31B Takes 3rd on FoodTruck Bench, Beating Larger ...</a></li>
<li><a href="https://agentic.ai/what-is-agentic-ai">What Is Agentic AI? A Complete Guide for 2026</a></li>

</ul>
</details>

**Discussion**: Commenters expressed surprise at Gemma 4 31B’s strong performance, questioned the absence of models like GPT-5.5 and Qwen3.6, and noted that DeepSeek’s cost advantage is based on a promotional rate. Some called for deeper benchmarks tracking effort and review budget, not just final outcomes.

**Tags**: `#AI benchmarks`, `#large language models`, `#agentic AI`, `#cost efficiency`, `#DeepSeek`

---

<a id="item-14"></a>
## [Trump Administration Considers Pre-Release Review for AI Models](https://www.nytimes.com/2026/05/04/technology/trump-ai-models.html) ⭐️ 8.0/10

The Trump administration is considering a pre-release review process for new AI models, marking a shift from its previous deregulatory approach, after Anthropic’s Mythos model raised security concerns. The White House plans to establish an AI task force with tech executives and government officials to develop the regulatory procedure. This policy shift could reshape AI development and release practices, as leading companies may need government approval before launching models, potentially slowing innovation but enhancing security oversight. It also highlights the growing tension between technological advancement and national security in the AI race with China. The proposed review would grant the U.S. government priority access to evaluate new AI models before public release, with a focus on cybersecurity risks. The policy discussions were prompted in part by Anthropic's Mythos model, which demonstrated strong capabilities in identifying software vulnerabilities, alarming officials. The White House Chief of Staff and Treasury Secretary have taken over AI policy formulation, signaling the seriousness of the issue.

telegram · zaihuapd · May 5, 02:00

**Background**: Anthropic's Mythos is a powerful AI model that has not been publicly released due to safety concerns, particularly its ability to discover software vulnerabilities (CVEs) that could be exploited. The Trump administration initially favored minimal AI regulation, but the emergence of highly capable models like Mythos has prompted reconsideration. Pre-release review is a mechanism where government bodies evaluate AI systems for potential risks before they become widely available, similar to processes in other sensitive technologies.

<details><summary>References</summary>
<ul>
<li><a href="https://www.nytimes.com/2026/04/22/technology/anthropics-mythos-ai.html">Anthropic’s New Mythos A.I. Model Sets Off Global Alarms ...</a></li>
<li><a href="https://www.scientificamerican.com/article/what-is-mythos-and-why-are-experts-worried-about-anthropics-ai-model/">What is Mythos, Anthropic’s unreleased AI model, and how ...</a></li>

</ul>
</details>

**Tags**: `#AI regulation`, `#government policy`, `#AI safety`, `#Trump administration`, `#pre-release review`

---

<a id="item-15"></a>
## [Image Models Drive 6.5x More AI App Downloads Than Chatbot Updates](https://techcrunch.com/2026/05/04/image-ai-models-now-drive-app-growth-beating-chatbot-upgrades/) ⭐️ 8.0/10

According to Appfigures, image AI model releases now generate 6.5 times more app downloads than chatbot text model updates. For instance, Google Gemini's Nano Banana prompted over 22 million downloads in 28 days, and ChatGPT's GPT-4o image model added over 12 million, both far exceeding their text-only counterparts. This reveals that visual AI features are far more compelling for user acquisition than text-based improvements, but monetization remains uneven. Only ChatGPT successfully converted the surge into significant revenue (around $70 million), while Google and Meta saw negligible income, highlighting a market gap. In the same period, ChatGPT’s image model drove approximately $70 million in consumer spending, whereas Google's Nano Banana brought in only about $181,000, and Meta AI's Vibes video feature generated no meaningful revenue, demonstrating that downloads do not guarantee monetization.

telegram · zaihuapd · May 5, 09:49

**Background**: GPT-4o image generation, launched by OpenAI, excels at text rendering and prompt following. Google's Nano Banana (Gemini 2.5 Flash Image) is designed for high-volume, conversational image editing. Meta AI's Vibes is a short-form AI video generator and feed, akin to TikTok for AI videos. These releases represent the industry's shift toward multimodal AI experiences.

<details><summary>References</summary>
<ul>
<li><a href="https://openai.com/index/introducing-4o-image-generation/">Introducing 4o Image Generation | OpenAI</a></li>
<li><a href="https://gemini.google/overview/image-generation/">Nano Banana 2 - Gemini AI image generator & photo editor</a></li>
<li><a href="https://about.fb.com/news/2025/09/introducing-vibes-ai-videos/">Introducing Vibes: A New Way to Discover and Create AI Videos</a></li>

</ul>
</details>

**Tags**: `#AI apps`, `#image generation`, `#app market`, `#monetization`, `#tech news`

---

<a id="item-16"></a>
## [GitHub Apologizes for Outages, Announces 30x Scaling Plan](https://github.blog/news-insights/company-news/an-update-on-github-availability/) ⭐️ 8.0/10

GitHub CTO Vlad Fedorov apologized for two outages in April and revealed a 30x scaling initiative driven by AI agent workflows. Key changes include migrating performance-sensitive Ruby code to Go, offloading database workloads from MySQL, and moving from custom data centers to Azure and a multi-cloud architecture. This infrastructure overhaul aims to greatly enhance reliability and performance for the millions of developers who depend on GitHub daily. It also reflects a broader industry shift away from monolithic architectures and single-cloud lock-in toward microservices and multi-cloud resilience. The April 23 merge queue incident erroneously generated squash merges and reverted code across 658 repositories without data loss. The April 27 search outage stemmed from an Elasticsearch cluster overload, suspected to be an attack, but core Git operations remained unaffected.

telegram · zaihuapd · May 5, 11:42

**Background**: Elasticsearch is an open-source, distributed search and analytics engine built on Apache Lucene, commonly used for full-text search and log analysis. A merge queue is a CI/CD feature that automatically enqueues and tests pull requests in sequence to keep the main branch stable, especially useful for repositories with frequent merges.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.github.com/zh/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue">管理合并队列 - GitHub 文档</a></li>
<li><a href="https://baike.baidu.com/item/Elasticsearch/3411206">Elasticsearch_百度百科 什么是 Elasticsearch？- Elasticsearch 引擎简介 - AWS Elasticsearch基础（一）：Elasticsearch简介-腾讯云开发者社区-腾讯... 什么是Elasticsearch？它与其他搜索引擎相比有什么优势？ Elasticsearch简述_elasticsearch是什么-CSDN博客</a></li>

</ul>
</details>

**Tags**: `#GitHub`, `#scalability`, `#incident-report`, `#infrastructure`, `#architecture`

---

<a id="item-17"></a>
## [UK Online Safety Act Age Checks Bypassed with Fake Beards](https://www.theregister.com/2026/05/04/uk_online_safety_act_age_checks_subvert/) ⭐️ 8.0/10

A survey by Internet Matters shows that 46% of children find age checks very easy to bypass, and 32% have successfully done so using simple tricks like drawing fake beards or entering false birthdates. This reveals a critical flaw in the enforcement of the Online Safety Act, undermining its goal of protecting children from harmful content and prompting urgent calls for design-level safety measures. The survey also found that 49% of children still encountered harmful content, and 17% of parents had actively helped their child bypass checks, highlighting the system's ineffectiveness.

telegram · zaihuapd · May 5, 14:16

**Background**: The UK Online Safety Act mandates age verification to restrict minors' access to harmful online content. Age estimation technologies, such as AI-based facial analysis, are often used but can be fooled by simple spoofing. This news highlights the gap between regulatory intent and real-world effectiveness, as children easily circumvent these checks with minimal effort.

**Tags**: `#age verification`, `#online safety`, `#regulation`, `#security`, `#children`

---

<a id="item-18"></a>
## [OpenAI's GPT-5.3 Instant Reduces Hallucinations by Up to 26.8%](https://t.me/zaihuapd/41231) ⭐️ 8.0/10

OpenAI released GPT-5.3 Instant, an update to ChatGPT's conversation model that reduces hallucination rates by up to 26.8% in high-risk domains when using web search, alongside improvements in refusal handling and search quality. This update significantly enhances AI reliability in critical fields like medicine, law, and finance, reducing factual errors and making the model safer for professional use. Internal tests show a 26.8% hallucination drop with web search and 19.7% without; user feedback metrics show 22.5% and 9.6% improvements, respectively. The model is available to all ChatGPT users immediately.

telegram · zaihuapd · May 5, 17:06

**Background**: AI hallucination refers to a model generating plausible but factually incorrect text, a common issue in large language models like GPT. High-risk domains such as healthcare, law, and finance demand high factual accuracy. OpenAI has been working to reduce hallucinations through techniques like improved training and external knowledge retrieval, such as web search queries. This release integrates those improvements into a smaller, faster version called Instant.

**Tags**: `#OpenAI`, `#GPT-5.3`, `#AI hallucination`, `#language models`, `#AI safety`

---

<a id="item-19"></a>
## [Microsoft Edge Stores Passwords in Cleartext in Memory](https://cybernews.com/security/microsoft-edge-loads-cleartext-passwords-to-memory/) ⭐️ 8.0/10

Security researcher Tom Jøran Sønstebyseter Rønning discovered that Microsoft Edge loads all saved passwords into memory in cleartext at startup and keeps them decrypted throughout the session, unlike other Chromium browsers such as Chrome which use application-bound encryption and decrypt passwords only when needed. This design flaw exposes credentials even if the user never visits saved sites, allowing attackers with administrator privileges to extract passwords from Edge's process memory, including passwords of other logged-in users on terminal servers. It undermines the security model in multi-user environments and highlights a concerning 'by design' response from Microsoft. The vulnerability affects all saved passwords in Edge; the cleartext remains accessible throughout the browser session. By contrast, Google Chrome employs application-bound encryption, tying decryption keys to the specific application and decrypting credentials only on-demand. Microsoft has acknowledged the behavior and stated it is intentional, offering no immediate fix.

telegram · zaihuapd · May 5, 23:31

**Background**: Application-Bound Encryption (ABE) is a security mechanism that ties encryption keys to a specific application, preventing other processes from decrypting data. Chromium browsers, including Edge and Chrome, can implement ABE to protect saved passwords. Chrome uses ABE by default, while Edge currently lacks this enforcement, instead loading all passwords into memory in cleartext. This difference means Edge is more vulnerable to credential theft through memory scraping.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anoopcnair.com/application-bound-encryption-for-ms-edge-intune/">Enforce Application Bound Encryption For MS Edge Browser To</a></li>
<li><a href="https://www.anoopcnair.com/application-bound-encryption-in-ms-edge-browser/">Enable Or Disable Application Bound Encryption Policy In MS</a></li>

</ul>
</details>

**Tags**: `#security`, `#Microsoft Edge`, `#passwords`, `#vulnerability`, `#Chromium`

---