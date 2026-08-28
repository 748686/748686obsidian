---
layout: default
title: "Horizon Summary: 2026-06-18 (EN)"
date: 2026-06-18
lang: en
---

> From 50 items, 15 important content pieces were selected

---

1. [U.S. Science in Crisis as Funding and Policy Collapse](#item-1) ⭐️ 9.0/10
2. [Android 17 Released: Mandatory Large-Screen Support, AI Integration](#item-2) ⭐️ 9.0/10
3. [Nezha Monitoring v2.0.13 and Below Has Critical Path Traversal (CVSS 9.1)](#item-3) ⭐️ 9.0/10
4. [Epic Games Open-Sources Lore VCS for Game Dev](#item-4) ⭐️ 8.0/10
5. [US Delays Blacklisting DeepSeek, Adds 100+ Chinese Firms to Security List](#item-5) ⭐️ 8.0/10
6. [Leaked Docs Show OpenAI Losing Billions Annually](#item-6) ⭐️ 8.0/10
7. [GLM-5.2 tops open-weights models on Artificial Analysis](#item-7) ⭐️ 8.0/10
8. [RFC 10008 defines HTTP QUERY method for safe, idempotent requests with body](#item-8) ⭐️ 8.0/10
9. [Volkswagen blocks GrapheneOS users via Play Protect requirement](#item-9) ⭐️ 8.0/10
10. [Charity Majors: AI Code Is Disposable, Demands More Discipline](#item-10) ⭐️ 8.0/10
11. [Next-Latent Prediction: Transformers Learn Compact World Models](#item-11) ⭐️ 8.0/10
12. [Seeking Theory for Probe Strength in Transformer Circuits](#item-12) ⭐️ 8.0/10
13. [Contrastive Targeted SFT for Causal Dependency Graphs in LLMs](#item-13) ⭐️ 8.0/10
14. [STAR Market Fifth Standard Expands to AI](#item-14) ⭐️ 8.0/10
15. [Anthropic surpasses OpenAI in enterprise AI market share](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [U.S. Science in Crisis as Funding and Policy Collapse](https://www.scientificamerican.com/article/americas-compact-between-science-and-politics-is-broken/) ⭐️ 9.0/10

A Scientific American article and extensive community discussion reveal that severe funding cuts and visa restrictions are driving U.S. scientists to leave the country or abandon research altogether. This breakdown threatens U.S. leadership in science and innovation, potentially causing a long-term brain drain and loss of critical research capabilities. Specific testimonies include a researcher whose R01 grant was not renewed, forcing staff to part-time, and a scientist whose wife operates an optical trap—a rare skill held by only about 2,000 people worldwide—who is moving abroad.

hackernews · presspot · Jun 17, 09:54 · [Discussion](https://news.ycombinator.com/item?id=48568058)

**Background**: The U.S. research enterprise has long relied on a compact between science and politics, where government funding supports basic research through agencies like NIH. However, recent political turmoil, budget constraints, and immigration restrictions have disrupted this compact, leading to a crisis in academic labs and national labs.

**Discussion**: Commenters express deep frustration and despair, with many sharing personal stories of leaving the U.S. or science. Some note that while the situation is chaotic, it also forces adaptation and new opportunities, though the overall sentiment is one of loss and uncertainty.

**Tags**: `#science policy`, `#research funding`, `#US politics`, `#academia crisis`, `#brain drain`

---

<a id="item-2"></a>
## [Android 17 Released: Mandatory Large-Screen Support, AI Integration](https://android-developers.googleblog.com/2026/06/Android-17.html) ⭐️ 9.0/10

Google has released Android 17 to Pixel devices and opened the source code, introducing mandatory large-screen support, AI integration via AppFunctions for Gemini, and a full shift to Jetpack Compose. This update fundamentally changes Android development by requiring apps to support large screens and by enabling AI to directly invoke app functions, which will affect all developers and enhance user experiences on foldables, tablets, and other form factors. Android 17 removes the developer opt-out for orientation and resizability restrictions on large screens (sw > 600 dp), enforces strict memory limits based on total device RAM, and introduces temporary permissions and a contact picker for privacy.

telegram · zaihuapd · Jun 17, 01:02

**Background**: Android 17 focuses on making Android a 'smart system' by integrating AI assistants like Google Gemini through the new AppFunctions API, which allows apps to expose functions that can be invoked by AI. It also mandates adaptive large-screen support, continuing the trend from Android 12L and later versions. Jetpack Compose, a modern declarative UI toolkit, becomes the default for new development, with the traditional View system moving to maintenance mode.

<details><summary>References</summary>
<ul>
<li><a href="https://android-developers.googleblog.com/2026/06/Android-17.html">Android Developers Blog: Android 17 is here</a></li>
<li><a href="https://developer.android.com/about/versions/17/changes/ff-restrictions-ignored">Restrictions on orientation and resizability are ignored | Android Developers</a></li>
<li><a href="https://en.wikipedia.org/wiki/Jetpack_Compose">Jetpack Compose</a></li>
<li><a href="https://developer.android.com/reference/android/app/appfunctions/AppFunctionService">AppFunctionService | API reference |</a></li>

</ul>
</details>

**Tags**: `#Android`, `#mobile development`, `#AI integration`, `#privacy`, `#Jetpack Compose`

---

<a id="item-3"></a>
## [Nezha Monitoring v2.0.13 and Below Has Critical Path Traversal (CVSS 9.1)](https://t.me/zaihuapd/42001) ⭐️ 9.0/10

A severe unauthenticated path traversal vulnerability (CVE-2026-53519) has been disclosed in Nezha Monitoring versions below v2.0.13, with a CVSS score of 9.1. Attackers can read arbitrary files, such as the config.yaml, to extract JWT secrets by crafting a GET request like /dashboard../data/config.yaml. Nezha Monitoring is a widely used self-hosted server monitoring tool; the vulnerability allows unauthorized access to sensitive JWT keys, enabling attackers to forge sessions and compromise entire server fleets. Immediate upgrade is critical for all users. The vulnerability resides in the dashboard component and affects all versions prior to v2.0.13. The exploit requires no authentication and can be triggered over HTTP, making it remotely exploitable with low complexity.

telegram · zaihuapd · Jun 17, 01:25

**Background**: Path traversal (or directory traversal) attacks allow an attacker to read files outside the intended directory by using sequences like '../' in file paths. Nezha Monitoring is an open-source, self-hosted monitoring and operation tool that supports multiple servers and websites, making such a vulnerability particularly dangerous for infrastructure security.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/nezhahq/nezha">GitHub - nezhahq/nezha: :trollface: Self-hosted, lightweight ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Path_traversal_vulnerability">Path traversal vulnerability</a></li>
<li><a href="https://owasp.org/www-community/attacks/Path_Traversal">Path Traversal | OWASP Foundation</a></li>

</ul>
</details>

**Tags**: `#网络安全`, `#漏洞`, `#哪吒监控`, `#路径穿越`, `#CVSS`

---

<a id="item-4"></a>
## [Epic Games Open-Sources Lore VCS for Game Dev](https://lore.org/) ⭐️ 8.0/10

Epic Games has open-sourced Lore, a version control system originally built for Fortnite, designed to handle large binary assets and replace Perforce in game development. Lore addresses Git's poor handling of non-text files like textures and 3D models, providing a scalable alternative for game studios. It could disrupt the proprietary Perforce dominance in game development. Lore, formerly Unreal Revision Control, is already used internally at Epic and in Unreal Editor for Fortnite. It supports file locking, permissions, and large-scale collaboration for big projects.

hackernews · regnerba · Jun 17, 14:30 · [Discussion](https://news.ycombinator.com/item?id=48571081)

**Background**: Version control systems like Git track changes in code files but struggle with large binary assets common in game development. Perforce has been the industry standard for game dev due to its file locking and scalability, but it's proprietary and expensive. Lore aims to offer an open-source alternative with similar capabilities.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/EpicGames/lore">Lore is a next-generation, open source revision control system</a></li>
<li><a href="https://www.phoronix.com/news/Epic-Games-Lore-VCS">Epic Games Announces Lore Open-Source Version Control System</a></li>

</ul>
</details>

**Discussion**: The Hacker News community largely views Lore as a promising challenger to Perforce for game development. Some users highlight Git's poor user experience and lack of file locking, while others note Lore's pedigree as an internal Epic tool. There is curiosity about its performance compared to Perforce.

**Tags**: `#version control`, `#game development`, `#open source`, `#scalability`, `#perforce`

---

<a id="item-5"></a>
## [US Delays Blacklisting DeepSeek, Adds 100+ Chinese Firms to Security List](https://www.reuters.com/world/china/us-holds-off-blacklisting-chinas-deepseek-more-than-100-firms-deemed-security-2026-06-17/) ⭐️ 8.0/10

The United States has temporarily declined to blacklist the Chinese AI company DeepSeek, but added over 100 other Chinese firms to its trade security risk list. This decision signals a nuanced approach in US-China tech competition, potentially affecting global AI supply chains and the availability of advanced AI models. DeepSeek, known for its efficient large language models, remains unlisted, but the broader expansion of the blacklist targets entities deemed security risks, including those involved in advanced computing and AI.

hackernews · giuliomagnifico · Jun 17, 03:55 · [Discussion](https://news.ycombinator.com/item?id=48565498)

**Background**: The US Entity List restricts American companies from exporting certain goods and technologies to listed entities. DeepSeek is a Chinese AI startup that developed cost-effective models, gaining attention for competitive performance despite export controls on advanced GPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Comments show mixed reactions: some users appreciate DeepSeek's affordability and utility for coding tasks, while others criticize US government actions as hypocritical or hard to enforce. Some note that many Chinese AI companies already rely little on US goods, limiting the impact.

**Tags**: `#geopolitics`, `#AI`, `#DeepSeek`, `#US-China`, `#regulation`

---

<a id="item-6"></a>
## [Leaked Docs Show OpenAI Losing Billions Annually](https://arstechnica.com/ai/2026/06/leaked-financial-docs-show-openai-is-losing-billions-of-dollars-a-year/) ⭐️ 8.0/10

Leaked financial documents reveal that OpenAI incurred billions of dollars in losses in 2025 despite generating $13 billion in revenue, with research and development costs being the primary expense. This raises critical questions about the long-term financial sustainability of leading AI companies and the economics of frontier AI development, affecting investors, competitors, and the broader tech industry. The company reported $13 billion in gross revenue in 2025 with a cost of revenue of $7.5 billion, and research and development costs accounted for the largest share of expenses. OpenAI has over 900 million weekly active ChatGPT users but only about 50 million paid subscribers.

hackernews · greenchair · Jun 17, 21:31 · [Discussion](https://news.ycombinator.com/item?id=48577208)

**Background**: OpenAI is a leading artificial intelligence research and deployment company known for developing advanced models like GPT-4 and ChatGPT. The company started as a non-profit but later created a for-profit subsidiary to raise capital, though its governance structure remains complex. Large language model development requires enormous computing resources and talent, leading to high operational costs.

**Discussion**: Commenters debated the sustainability of OpenAI's business model, with some noting that R&D costs dominate and questioning whether the focus should shift to inference cost reduction. Others pointed out the challenge of converting free users to paid subscribers given many free alternatives like DeepSeek.

**Tags**: `#OpenAI`, `#AI business`, `#financial analysis`, `#AI startups`

---

<a id="item-7"></a>
## [GLM-5.2 tops open-weights models on Artificial Analysis](https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index) ⭐️ 8.0/10

GLM-5.2 has been ranked as the leading open-weights model on the Artificial Analysis Intelligence Index, achieving near-frontier performance at drastically reduced prices compared to closed models. This development shows that open-weights models can rival top closed models like GPT-5.5 and Opus, potentially democratizing access to high-quality AI at much lower cost and challenging the dominance of proprietary providers. The model achieves close-to-frontier scores on coding and agent benchmarks, with community reports noting API pricing 10x cheaper than Anthropic's Opus, though some users observed high token consumption during reasoning tasks.

hackernews · himata4113 · Jun 17, 09:12 · [Discussion](https://news.ycombinator.com/item?id=48567759)

**Background**: Open-weights models allow anyone to download, inspect, and fine-tune the trained weights, unlike fully closed models. Artificial Analysis is an independent platform that benchmarks AI models on quality, price, and speed, providing transparent comparisons for developers.

<details><summary>References</summary>
<ul>
<li><a href="https://artificialanalysis.ai/">AI Model & API Providers Analysis | Artificial Analysis</a></li>
<li><a href="https://huggingface.co/blog/daya-shankar/open-source-llms">Best Open -Source LLM Models in 2026: Coding, Local, Agentic AI ...</a></li>
<li><a href="https://www.linkedin.com/pulse/openais-open-weight-model-what-means-developers-ai-industry-tsi9f">OpenAI’s Open - Weight Model : What It Means for Developers and the...</a></li>

</ul>
</details>

**Discussion**: Community members largely celebrated GLM-5.2 for offering near-frontier quality at very low prices, with some calling it a 'massive win for the rest of the world' against closed providers. However, a user noted that its reasoning efficiency could be improved, citing a 15-minute reasoning task consuming 45k tokens.

**Tags**: `#AI`, `#open-weights`, `#GLM`, `#model comparison`

---

<a id="item-8"></a>
## [RFC 10008 defines HTTP QUERY method for safe, idempotent requests with body](https://www.rfc-editor.org/info/rfc10008/) ⭐️ 8.0/10

RFC 10008 has been published, standardizing the HTTP QUERY method as a new HTTP request method that is safe and idempotent and allows a request body, providing a standardized alternative to GET with a body. This addresses a long-standing gap in HTTP: GET cannot carry a body, yet many applications require complex queries with bodies. QUERY enables caching, automatic retries, and safer interactions for APIs, HTML forms, and complex data retrieval. The QUERY method is similar to POST but must be safe and idempotent, meaning the same request produces the same result without side effects. Caching can use the request body as part of the cache key, though this raises concerns about unbounded key sizes.

hackernews · schappim · Jun 17, 10:51 · [Discussion](https://news.ycombinator.com/item?id=48568502)

**Background**: HTTP GET is idempotent and cacheable but historically cannot include a request body. POST supports a body but is not required to be idempotent, causing issues with retries and caching. The IETF considered allowing GET with body but chose a new method due to interoperability concerns with existing implementations.

<details><summary>References</summary>
<ul>
<li><a href="https://www.rfc-editor.org/info/rfc10008/">RFC 10008 : The HTTP QUERY Method | RFC Editor</a></li>
<li><a href="https://httpwg.org/http-extensions/draft-ietf-httpbis-safe-method-w-body.html">The HTTP QUERY Method</a></li>
<li><a href="https://horovits.medium.com/http-s-new-method-for-data-apis-http-query-1ff71e6f73f3">HTTP‘s New Method For Data APIs: HTTP QUERY | by Horovits | Medium</a></li>

</ul>
</details>

**Discussion**: Community comments discuss cache key implementation challenges, the possibility of HTML forms supporting QUERY to avoid POST resubmission warnings, and the historical workaround of sending bodies with GET. The discussion is generally supportive but raises valid technical concerns.

**Tags**: `#HTTP`, `#RFC`, `#web standards`, `#API design`, `#protocol`

---

<a id="item-9"></a>
## [Volkswagen blocks GrapheneOS users via Play Protect requirement](https://discuss.grapheneos.org/d/35949-volkswagen-app?page=3) ⭐️ 8.0/10

Volkswagen has locked its API to require Play Protect certification, effectively blocking GrapheneOS users from accessing car features via the official app. This disables community-driven integrations and forces users to rely on an advertisement-heavy official app. This move by a major automaker sets a precedent for restricting device freedom and privacy-focused OS users from accessing connected car features. It highlights growing tensions between Google's certification ecosystem and custom Android ROMs like GrapheneOS, which prioritize privacy over Google services. The API lock affects not only GrapheneOS but any device without Play Protect certification, including those using community projects like Home Assistant for automation. The official VW app is reported to be 60% advertisements and 30% features, making it less functional than previous community alternatives.

hackernews · microtonal · Jun 17, 15:04 · [Discussion](https://news.ycombinator.com/item?id=48571526)

**Background**: GrapheneOS is a security-hardened, open-source Android-based operating system that focuses on privacy and often runs without Google Play Services. Google's Play Protect certification is required for devices to access Google apps and certain APIs, and it relies on Google's proprietary compatibility tests. GrapheneOS users typically avoid Google services to minimize data collection, making Play Protect certification incompatible with their privacy goals.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GrapheneOS">GrapheneOS</a></li>
<li><a href="https://www.android.com/certified/">Android – Certified</a></li>
<li><a href="https://grapheneos.org/">GrapheneOS: the private and secure mobile OS</a></li>

</ul>
</details>

**Discussion**: Community comments express frustration and disappointment, with users highlighting that Volkswagen previously turned off API access for community integrations and now blocks GrapheneOS outright. Some users lament the loss of useful features like Home Assistant automations, and others criticize the official app's heavy advertising. There is also concern that this trend could spread to other VW brands and potentially align with broader restrictions on privacy tools.

**Tags**: `#privacy`, `#GrapheneOS`, `#Android`, `#automotive`, `#Volkswagen`

---

<a id="item-10"></a>
## [Charity Majors: AI Code Is Disposable, Demands More Discipline](https://simonwillison.net/2026/Jun/17/charity-majors/#atom-everything) ⭐️ 8.0/10

Charity Majors argues that AI has turned the economics of code production upside down, making code generation effectively free and instant, and shifting code from treasured to disposable. This fundamental shift demands more engineering discipline as the focus moves from writing code to curating and validating it, affecting how software teams prioritize architecture, testing, and system design. Majors notes that lines of code went from being carefully curated to disposable and regenerable practically overnight, highlighting a dramatic change in developer mindset.

rss · Simon Willison · Jun 17, 17:12

**Background**: Traditionally, software development involved high costs for writing and maintaining code, making reuse and careful curation essential. With AI-assisted programming, generating large amounts of code becomes cheap and fast, reducing the marginal cost of new code. This economic shift requires engineers to invest more effort in system-level thinking and quality assurance rather than manual coding.

**Tags**: `#ai`, `#ai-assisted-programming`, `#software-engineering`, `#economics-of-code`, `#charity-majors`

---

<a id="item-11"></a>
## [Next-Latent Prediction: Transformers Learn Compact World Models](https://www.reddit.com/r/MachineLearning/comments/1u84mio/nextlatent_prediction_transformers_r/) ⭐️ 8.0/10

Microsoft Research introduces Next-Latent Prediction (NextLat), a self-supervised method that trains transformers to predict their own next latent state given the current latent and next token, achieving better world models and up to 3.3x faster inference via self-speculative decoding. NextLat improves data efficiency and representation learning over standard next-token prediction, offering a principled way to compress history into compact belief states. This could lead to more capable and faster autoregressive models for reasoning and planning tasks. The method provably converges to belief states—compressed information necessary to predict the future. Self-speculative decoding enables multi-step lookahead, resulting in lossless acceleration up to 3.3x without sacrificing output quality.

reddit · r/MachineLearning · /u/jayden_teoh_ · Jun 17, 08:44

**Background**: Standard transformers are trained via next-token prediction, which provides sparse supervision per token. NextLat adds an auxiliary task: predicting the next latent representation, which compresses the sequence history. Self-speculative decoding is a technique where the same model drafts and verifies token blocks, reducing sequential generation steps.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2511.05963">[2511.05963] Next-Latent Prediction Transformers Learn Compact World Models</a></li>
<li><a href="https://neurips.cc/virtual/2025/132811">NeurIPS Keynote #7 Next-Latent Prediction Transformers Learn Compact World Models</a></li>

</ul>
</details>

**Tags**: `#transformers`, `#self-supervised learning`, `#representation learning`, `#efficient inference`, `#Microsoft Research`

---

<a id="item-12"></a>
## [Seeking Theory for Probe Strength in Transformer Circuits](https://www.reddit.com/r/MachineLearning/comments/1u8lo60/how_do_you_analyze_the_relative_strength_of/) ⭐️ 8.0/10

A Reddit user posted a detailed question seeking theoretical grounding for comparing the strength of probes in transformer circuits, specifically focusing on the trade-off between probe capacity and underlying network complexity. This question addresses a fundamental gap in mechanistic interpretability: how to rigorously evaluate what probes can reveal about model internals. Resolving it could lead to more reliable circuit analyses and better guarantees for model safety and factuality. The user cites an old study that trained a logistic regression probe to detect word positions and notes problems such as very small vocabulary sizes leading to unrepresentative performance. They also share a real failure case where Google Gemini incorrectly counted letters in 'Google', undermining the claim that models inherently learn token positions.

reddit · r/MachineLearning · /u/RepresentativeBee600 · Jun 17, 20:29

**Background**: In mechanistic interpretability, probing involves training simple classifiers (probes) on model activations to test if certain features are encoded. However, the theoretical foundations for comparing probe strength are underdeveloped, with questions about overfitting and sample complexity remaining open. The Nyquist sampling theorem is mentioned as a potential analogy for determining if enough data has been seen to guarantee reliable detection of patterns.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2509.17665">[2509.17665] Mechanistic Interpretability with SAEs: Probing</a></li>

</ul>
</details>

**Tags**: `#mechanistic interpretability`, `#probing`, `#circuit analysis`, `#transformer models`, `#ML theory`

---

<a id="item-13"></a>
## [Contrastive Targeted SFT for Causal Dependency Graphs in LLMs](https://www.reddit.com/r/MachineLearning/comments/1u8if6l/contrastive_targeted_sft_as_a_mechinterp_method/) ⭐️ 8.0/10

A researcher proposes using contrastive targeted supervised fine-tuning (SFT) to discover causal dependency graphs between capability dimensions in large language models, by training pairs of checkpoints that differ in a specific dimension, then ablating identified circuits and measuring downstream degradation in other dimensions. This methodology could enable systematic understanding of how different capabilities interact inside LLMs, potentially improving training order and targeted behavior control, which is a key goal in mechanistic interpretability and model steering. The contrastive approach creates pairs of checkpoints from the same base model—one with a dimension deeply represented, the other shallowly—then uses patch differences to locate circuits and ablates them to map causal dependencies. The researcher also plans to test compositionality via prompting requiring causal chaining and use activation steering as a diagnostic tool.

reddit · r/MachineLearning · /u/Substantial_Diver469 · Jun 17, 18:31

**Background**: Mechanistic interpretability aims to reverse-engineer the internal components (circuits) of neural networks that implement specific behaviors. Supervised fine-tuning (SFT) adapts pre-trained models to specific tasks using labeled data. Contrastive learning techniques compare positive and negative examples to learn representations. This post combines these ideas to map causal dependencies between capability dimensions in LLMs, a novel approach not yet explored in existing literature.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2304.14997">[2304.14997] Towards Automated Circuit Discovery for Mechanistic Interpretability</a></li>
<li><a href="https://arxiv.org/html/2402.11068v2">Large Language Models for Causal Discovery: Current Landscape ...</a></li>

</ul>
</details>

**Tags**: `#mechanistic interpretability`, `#SFT`, `#causal dependencies`, `#LLMs`, `#circuit discovery`

---

<a id="item-14"></a>
## [STAR Market Fifth Standard Expands to AI](https://mp.weixin.qq.com/s/ywLPXkSlqY9S5Vwp8G5saA) ⭐️ 8.0/10

CSRC Chairman Wu Qing announced at the 2026 Lujiazui Forum that the STAR Market's fifth set of listing standards will be expanded to cover AI companies, including quantum tech, biomanufacturing, and embodied AI. The regulator also plans to introduce shelf registration for refinancing and four policies to support Shanghai as an international financial hub. This policy shift provides a crucial financing channel for unprofitable AI and hard-tech startups in China, potentially accelerating their growth and IPO process. It signals strong government support for the AI sector and may reshape the landscape of China's tech capital markets. The fifth set of standards originally allowed pre-revenue companies in biotech and other hard-tech sectors to list. The expansion now explicitly includes AI large-model companies, embodied AI, quantum tech, and biomanufacturing. Additionally, the CSRC will strictly crack down on fake tech hype and issue guidance on AI regulation in capital markets.

telegram · zaihuapd · Jun 17, 08:30

**Background**: The STAR Market (科创板) is China's Nasdaq-style board for tech companies, launched in 2019. Its fifth set of listing standards permits companies without profits to go public if they meet certain R&D and market cap thresholds. Shelf registration (储架发行) is a mechanism where issuers can register securities once and issue them in tranches over time, streamlining refinancing. Embodied AI refers to AI systems that interact with the physical world, such as humanoid robots.

<details><summary>References</summary>
<ul>
<li><a href="http://www.ce.cn/xwzx/gnsz/gdxw/202606/t20260618_3038347.shtml">科创板第五套标准扩围至大模型企业 智谱、MiniMax“回A”有望提速科创板...</a></li>
<li><a href="https://paper.cnstock.com/html/2026-06/18/content_2233003.htm">科创板第五套标准扩围至大模型企业 智谱、MiniMax“回A”有望提速</a></li>
<li><a href="https://baike.baidu.com/item/储架发行制度/1648322">储架发行制度_百度百科</a></li>

</ul>
</details>

**Tags**: `#AI`, `#regulation`, `#China`, `#stock market`, `#technology`

---

<a id="item-15"></a>
## [Anthropic surpasses OpenAI in enterprise AI market share](https://techcrunch.com/2026/06/16/anthropics-latest-feud-with-the-trump-admin-may-actually-help-it-sales-data-suggests/) ⭐️ 8.0/10

In May 2026, Anthropic's enterprise AI market share surpassed OpenAI for the first time, with Ramp data showing Anthropic capturing 41% of enterprise subscription spending versus OpenAI's 39.5%, despite the Trump administration ordering Anthropic to remove its latest models due to export controls. This milestone signals a shift in enterprise AI adoption, where safety-focused Anthropic is gaining trust over OpenAI despite regulatory headwinds. It may also reshape the competitive landscape and investor sentiment ahead of potential IPOs. The models affected are Claude Fable 5 and Claude Mythos 5, which were released in June 2026 and then promptly ordered offline. However, most enterprise customers still use the publicly available Claude Opus series, mitigating immediate revenue impact.

telegram · zaihuapd · Jun 17, 09:30

**Background**: Anthropic is an AI safety company founded by former OpenAI employees, known for its Claude models. In June 2026, it released its most powerful models, Fable 5 and Mythos 5, but the U.S. government ordered them removed citing national security concerns about foreign access. Enterprise AI market share is tracked by companies like Ramp, which analyzes corporate spending on AI subscriptions.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/news/claude-fable-5-mythos-5">Claude Fable 5 and Claude Mythos 5 \ Anthropic</a></li>
<li><a href="https://www.cnbc.com/2026/06/09/anthropic-mythos-claude-fable-5.html">Anthropic releases Mythos-like AI model to the public, Claude Fable 5</a></li>

</ul>
</details>

**Tags**: `#AI industry`, `#enterprise AI`, `#market competition`, `#regulation`, `#Anthropic`

---