---
layout: default
title: "Horizon Summary: 2026-06-16 (EN)"
date: 2026-06-16
lang: en
---

> From 47 items, 17 important content pieces were selected

---

1. [US government forces Anthropic to block two AI models over national security](#item-1) ⭐️ 9.0/10
2. [Critical Path Traversal Vulnerability in Nezha Monitor (CVSS 9.1)](#item-2) ⭐️ 9.0/10
3. [vLLM v0.23.0 Enhances DeepSeek-V4 and Model Runner V2](#item-3) ⭐️ 8.0/10
4. [LinkedIn Job Offer Backdoor Targets Developers via npm](#item-4) ⭐️ 8.0/10
5. [Iroh 1.0: A Peer-to-Peer Networking Library for Applications](#item-5) ⭐️ 8.0/10
6. [Developers Replace Cloud AI Coding Assistants with Local Models](#item-6) ⭐️ 8.0/10
7. [Hetzner Price Adjustment](#item-7) ⭐️ 8.0/10
8. [Fox to Acquire Roku](#item-8) ⭐️ 8.0/10
9. [Salesforce Acquires Fin (formerly Intercom) for $3.6B](#item-9) ⭐️ 8.0/10
10. [Typst 0.15.0 Released with Multiple Bibliographies](#item-10) ⭐️ 8.0/10
11. [Linux 7.1 Kernel Sets Developer Record with 15,849 Commits](#item-11) ⭐️ 8.0/10
12. [curl declares 'summer of bliss', pauses vulnerability reports](#item-12) ⭐️ 8.0/10
13. [LLMs exhibit model-specific name biases](#item-13) ⭐️ 8.0/10
14. [Neocortical Learning Framework via Temporal Derivatives](#item-14) ⭐️ 8.0/10
15. [Cleo: A 2B Parameter Model for Unified Text-to-SQL](#item-15) ⭐️ 8.0/10
16. [ByteDance in Talks to Buy AI Chips from China's Iluvatar Corex](#item-16) ⭐️ 8.0/10
17. [Rio 3.5 Exposed as Wrapper of Open-Source Models Nex and Qwen](#item-17) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [US government forces Anthropic to block two AI models over national security](https://t.me/zaihuapd/41960) ⭐️ 9.0/10

The US government issued an export control directive to Anthropic under national security authority, requiring suspension of foreign citizen access to Fable 5 and Mythos 5. Anthropic has consequently closed access to both models for all customers, including foreign employees. This marks a significant escalation in government regulation of frontier AI models, directly intervening in model deployment due to security concerns. It sets a precedent for future export controls on powerful AI systems and impacts the entire AI industry's approach to model release and access. The Commerce Department action is linked to concerns about the models being jailbroken, potentially causing security risks. Only Fable 5 and Mythos 5 are affected; other Claude models remain accessible, and Anthropic is working to restore access as soon as possible.

telegram · zaihuapd · Jun 15, 08:55

**Background**: Fable 5 and Mythos 5 are advanced large language models developed by Anthropic. Mythos is designed for finding software vulnerabilities, and Fable 5 is a safety-tuned version of Mythos 5. Jailbreaking refers to techniques that bypass a model's safety guardrails, potentially enabling harmful outputs. The US government has increasingly used export controls to restrict access to sensitive technologies deemed national security risks.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mythos_(Anthropic)">Mythos (Anthropic)</a></li>
<li><a href="https://www.anthropic.com/news/claude-fable-5-mythos-5">Claude Fable 5 and Claude Mythos 5 \ Anthropic</a></li>
<li><a href="https://www.infoq.cn/article/SzLqxwcXt941I2eZclFK">Anthropic 祭出双旗舰 模 型 Fable 、Mythos... - InfoQ</a></li>
<li><a href="https://unwire.pro/2026/06/14/us-blocks-fable-5-ai/ai/">美國突然封殺 Fable 5 / Mythos 5 背後原因分析 企業要小心應對</a></li>
<li><a href="https://news.pedaily.cn/202606/565115.shtml">Fable 5 评测：强，贵，甚至能发现自己正在被检测_投资界</a></li>

</ul>
</details>

**Tags**: `#AI regulation`, `#export controls`, `#Anthropic`, `#national security`, `#government policy`

---

<a id="item-2"></a>
## [Critical Path Traversal Vulnerability in Nezha Monitor (CVSS 9.1)](https://github.com/nezhahq/nezha/security/advisories/GHSA-5c25-7vpj-9mqh) ⭐️ 9.0/10

A critical unauthenticated path traversal vulnerability (CVE-2026-53519, CVSS 9.1) has been disclosed in Nezha versions 2.0.13 and below, allowing attackers to read configuration files like config.yaml via crafted GET requests. This vulnerability enables unauthenticated attackers to extract JWT secrets from configuration files, potentially leading to full system compromise or unauthorized access to the monitoring dashboard, affecting all Nezha users who have not patched. The exploit uses a path traversal sequence (e.g., /dashboard../data/config.yaml) to bypass authentication. All versions up to and including v2.0.13 are affected; users must upgrade to v2.0.14 or later immediately.

telegram · zaihuapd · Jun 15, 09:25

**Background**: Nezha is an open-source, lightweight server monitoring and management tool composed of a dashboard and agent components. Configuration files typically store sensitive data such as JWT secrets and database credentials, which are exposed by this vulnerability. Path traversal attacks allow an attacker to read arbitrary files outside the web root by manipulating URL paths.

<details><summary>References</summary>
<ul>
<li><a href="https://blog.csdn.net/weixin_43748495/article/details/147731159">哪 吒 探 针 监 控 部署配置详细教程-CSDN博客</a></li>
<li><a href="https://zhichao.org/posts/4bba96">开源、轻量、易用的服务器实时 监 控 工具： 哪 吒 探 针 | ZhiChao's Blog</a></li>

</ul>
</details>

**Tags**: `#security`, `#vulnerability`, `#nezha`, `#path-traversal`, `#CVE`

---

<a id="item-3"></a>
## [vLLM v0.23.0 Enhances DeepSeek-V4 and Model Runner V2](https://github.com/vllm-project/vllm/releases/tag/v0.23.0) ⭐️ 8.0/10

vLLM v0.23.0 introduces major optimizations for DeepSeek-V4, including sparse MLA metadata decoupling, TRTLLM-gen attention kernel, and EPLB support for Mega-MoE, and expands Model Runner V2 by default to Llama and Mistral dense models. This release significantly improves inference performance and memory efficiency for state-of-the-art LLMs like DeepSeek-V4, benefiting developers deploying large models in production. The expansion of Model Runner V2 to more dense models further accelerates inference for widely-used model families. The release includes 408 commits from 200 contributors, with notable features like multi-tier KV cache offloading, a new object-store secondary tier, and unified parsing for reasoning and tool calls. Gemma 4 Unified encoder-free support and Transformers v5 compatibility are also added.

github · khluu · Jun 15, 05:27

**Background**: vLLM is a high-throughput, memory-efficient inference engine for large language models, widely used in AI/ML deployment. This release continues the project's rapid development pace, addressing performance bottlenecks and expanding model support.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.vllm.ai/en/latest/api/vllm/v1/attention/backends/mla/flashmla_sparse/">vllm.v1.attention.backends.mla.flashmla_sparse</a></li>
<li><a href="https://nvidia.github.io/TensorRT-LLM/advanced/gpt-attention.html">Multi-Head, Multi-Query, and Group-Query Attention — TensorRT- LLM</a></li>

</ul>
</details>

**Tags**: `#vLLM`, `#LLM inference`, `#release notes`, `#DeepSeek`, `#model optimization`

---

<a id="item-4"></a>
## [LinkedIn Job Offer Backdoor Targets Developers via npm](https://roman.pt/posts/linkedin-backdoor/) ⭐️ 8.0/10

A malicious job offer on LinkedIn directed a developer to a GitHub repository containing deprecated Node modules; running npm install automatically executed a backdoor via the prepare script. This attack demonstrates a sophisticated social engineering vector targeting developers, exploiting trust in recruitment processes and npm's automated lifecycle scripts. It underscores the growing threat of supply chain attacks and the need for heightened security awareness in job-related activities. The backdoor was hidden in deprecated npm packages and executed automatically when the victim ran npm install due to the prepare lifecycle script. The attacker posed as a recruiter from a small crypto startup and asked the victim to review a 'broken proof-of-concept' with deprecated modules.

hackernews · lwhsiao · Jun 15, 20:00 · [Discussion](https://news.ycombinator.com/item?id=48546294)

**Background**: npm install automatically runs lifecycle scripts like 'prepare', which can be abused to execute arbitrary code. Attackers often publish malicious packages under legitimate-seeming names or reuse deprecated package names to evade detection. Job scams targeting developers have become increasingly common, with attackers using fake offers to trick developers into running malware.

<details><summary>References</summary>
<ul>
<li><a href="https://dev.to/alien45/i-was-targeted-by-a-fake-employer-running-a-real-npm-supply-chain-attack-54i5">I Was Targeted by a Fake Employer Running a Real NPM Supply...</a></li>
<li><a href="https://www.linkedin.com/pulse/job-scams-targeting-developers-tech-professionals-hidden-yhspf">Job scams targeting developers and tech professionals: The ...</a></li>
<li><a href="https://cybersecuritynews.com/north-korean-hackers-attacking-developers/">North Korean Hackers Attacking Developers with 338 Malicious ...</a></li>

</ul>
</details>

**Discussion**: Commenters expressed frustration with LinkedIn's job posting quality, with some considering leaving the platform. Others called for a centralized cybercrime reporting system, noting that individuals have no easy way to report such attacks. Several observed that the attack is uncomfortably close to normal interview tasks, where developers might run npm install without suspicion.

**Tags**: `#security`, `#backdoor`, `#job scams`, `#Node.js`, `#LinkedIn`

---

<a id="item-5"></a>
## [Iroh 1.0: A Peer-to-Peer Networking Library for Applications](https://www.iroh.computer/blog/v1) ⭐️ 8.0/10

The n0-computer team has released Iroh 1.0, a Rust library for peer-to-peer connections with application-layer networking, providing hole-punching, relay, and custom transport support. Iroh 1.0 simplifies building decentralized applications by abstracting complex networking tasks, enabling developers to create peer-to-peer apps without managing infrastructure like Tailscale accounts. The library supports IPv4, IPv6, and relay transports out of the box, and allows custom transports via a plugin interface. It also includes a relay server implementation and opt-in observability tools.

hackernews · chadfowler · Jun 15, 15:13 · [Discussion](https://news.ycombinator.com/item?id=48542480)

**Background**: Application-layer networking means the library handles connection establishment and data transfer at the OSI model's Layer 7, abstracting away lower-level details like IP addresses. Iroh uses 'dial keys' (cryptographic keys) instead of IP addresses for identity, and relays assist with NAT traversal. This approach allows apps to connect peers directly without centralized servers.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/n0-computer/iroh">GitHub - n0-computer/iroh: IP addresses break, dial keys ...</a></li>
<li><a href="https://www.iroh.computer/">Iroh</a></li>
<li><a href="https://en.wikipedia.org/wiki/Application_layer">Application layer - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Community comments highlight various perspectives: some compare Iroh to Tailscale at the application layer, others ask about custom transports (e.g., WebRTC, BLE), and a few question the need for such a library given existing IP networking. Developers appreciate the custom transport interface and the potential for decentralized apps like a peer-to-peer messaging app.

**Tags**: `#networking`, `#p2p`, `#rust`, `#open-source`, `#library`

---

<a id="item-6"></a>
## [Developers Replace Cloud AI Coding Assistants with Local Models](https://news.ycombinator.com/item?id=48542100) ⭐️ 8.0/10

Several developers report successfully using local models like Qwen 3.6 35B and Gemma 4 26B to replace cloud-based coding assistants such as Claude and GPT, sharing hardware setups including Mac Studio with 128GB RAM and dual RTX3090s, achieving speeds up to 150 tokens per second. This shift demonstrates that local models are becoming viable for daily coding tasks, offering privacy, zero subscription costs, and comparable performance to frontier models from 8-12 months ago, potentially reducing reliance on expensive cloud APIs. Users employ toolchains like Pi coding harness, llama.cpp, and Semble with custom skills, and note that while local models are not as smart as the latest Claude or Codex, they are sufficient for most work. Hardware requirements include high-RAM Macs or multi-GPU setups.

hackernews · cloudking · Jun 15, 14:46

**Background**: Local large language models are AI models that run on a user's own hardware rather than on cloud servers. Qwen is a family of open-source LLMs developed by Alibaba Cloud, while Gemma is Google DeepMind's lightweight open-weight model series. Performance is often measured in tokens per second (tok/s), where higher speeds mean more responsive interaction; 150 tok/s is considered very fast for local inference.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Qwen">Qwen - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Gemma_(language_model)">Gemma ( language model ) - Wikipedia</a></li>
<li><a href="https://mljourney.com/how-many-tokens-per-second-is-good-for-local-llms/">How Many Tokens Per Second Is ‘Good’ for Local LLMs?</a></li>

</ul>
</details>

**Discussion**: The community is enthusiastic about the feasibility of local models, with users like Greenpants emphasizing privacy and speed, horsawlarway achieving 150 tok/s with dual RTX3090s, and pierotofy sharing a full setup guide. However, codinhood notes that opportunity cost of not using the latest models is a factor, and bluejay2387 mentions occasionally falling back to cloud models for hard tasks.

**Tags**: `#local LLMs`, `#AI-assisted coding`, `#hardware`, `#Qwen`, `#Gemma`

---

<a id="item-7"></a>
## [Hetzner Price Adjustment](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/#cloud-servers) ⭐️ 8.0/10

Hetzner has announced a significant price increase for its cloud servers, with some plans seeing up to a 3x hike. For example, the CPX11 plan rose from $6.99 to $20.49. This price adjustment reflects the AI boom's impact on hardware costs, particularly RAM and SSD scarcity. It may affect small developers and businesses that relied on Hetzner's affordability, and could signal broader price trends across the cloud hosting industry. The price increase is attributed to skyrocketing costs of RAM and SSDs, driven by AI-related demand. Hetzner has not introduced lower-cost alternatives to replace the previous affordable tiers.

hackernews · tuhtah · Jun 15, 13:19 · [Discussion](https://news.ycombinator.com/item?id=48540844)

**Background**: Hetzner is a German hosting provider known for offering affordable dedicated and cloud servers. The AI boom has caused a surge in demand for hardware components like RAM and SSDs, leading to shortages and price increases across the industry. This price adjustment by Hetzner is part of a larger trend affecting cloud providers.

**Discussion**: The community expressed mixed reactions, with some users frustrated by the 3x increase and questioning the justification. Others noted the broader hardware cost reality and wondered if larger hyperscalers like AWS and GCP can keep prices stable. Some users called for new lower-cost plans to match the old pricing.

**Tags**: `#cloud hosting`, `#pricing`, `#hardware scarcity`, `#AI boom`, `#Hetzner`

---

<a id="item-8"></a>
## [Fox to Acquire Roku](https://www.wsj.com/business/deals/fox-roku-deal-f6e564f9) ⭐️ 8.0/10

Fox Corporation is reportedly acquiring Roku, the popular streaming device and platform company, according to a Wall Street Journal report. This acquisition could give Fox direct access to Roku's massive user base, raising concerns about media consolidation and the potential for biased content placement on a widely used streaming platform. Roku has roughly 30-50% of American households using its hardware or software, and Fox's ownership could jeopardize Roku's service-agnostic architecture by prioritizing Fox content.

hackernews · thm · Jun 15, 12:50 · [Discussion](https://news.ycombinator.com/item?id=48540499)

**Background**: Roku is a leading streaming platform that offers hardware devices and a smart TV operating system. It has been criticized for increasing ads and content pushing, moving away from its original neutral hardware model. Fox is a major media conglomerate with news, sports, and entertainment properties.

**Discussion**: The community is largely pessimistic, with users concerned about Fox controlling Roku's platform and potentially pushing Fox News or other biased content. Many commenters express a desire to switch away from Roku, with some recommending alternatives like NVIDIA Shield with customized launchers.

**Tags**: `#acquisition`, `#Roku`, `#Fox`, `#media`, `#streaming`

---

<a id="item-9"></a>
## [Salesforce Acquires Fin (formerly Intercom) for $3.6B](https://www.salesforce.com/news/press-releases/2026/06/15/salesforce-signs-definitive-agreement-to-acquire-fin/?bc=HL) ⭐️ 8.0/10

On June 15, 2026, Salesforce announced a definitive agreement to acquire Fin, formerly known as Intercom, for $3.6 billion, marking a major move in AI customer service. This acquisition strengthens Salesforce's AI-powered customer support capabilities and directly positions it against rivals like Sierra, co-founded by ex-Salesforce co-CEO Bret Taylor. It signals the growing importance of AI agents in enterprise CRM. Fin's AI agent, used by over 12,000 brands, provides specialized roles for service and sales. The $3.6 billion deal comes shortly after Intercom's rebranding to Fin, highlighting the intense competition in the AI customer service space, with Sierra valued at $15.8 billion and Decagon at $4.5 billion.

hackernews · colesantiago · Jun 15, 12:08 · [Discussion](https://news.ycombinator.com/item?id=48540126)

**Background**: Intercom was originally a customer messaging platform that rebranded to Fin in 2026, pivoting to AI-powered customer agents. Salesforce is the world's leading CRM provider and has been aggressively integrating AI into its platform. The acquisition aims to fend off independent AI support agents that could become control points outside of CRM systems.

<details><summary>References</summary>
<ul>
<li><a href="https://www.salesforce.com/news/press-releases/2026/06/15/salesforce-signs-definitive-agreement-to-acquire-fin/">Salesforce Signs Definitive Agreement to Acquire Fin</a></li>
<li><a href="https://fin.ai/">Intercom - Fin. The highest performing Customer Agent</a></li>
<li><a href="https://www.intercom.com/help/en/articles/7120684-fin-ai-agent-explained">Fin AI Agent explained - Intercom Help</a></li>

</ul>
</details>

**Discussion**: Community sentiment is mixed: some praise effective AI support when done well, while others question the value of such platforms for non-enterprise customers, noting DIY alternatives like Hermes. There is also concern that Salesforce might degrade the product, and appreciation that Intercom exited before AI commoditization.

**Tags**: `#acquisition`, `#AI customer service`, `#enterprise software`, `#Salesforce`, `#Intercom`

---

<a id="item-10"></a>
## [Typst 0.15.0 Released with Multiple Bibliographies](https://typst.app/docs/changelog/0.15.0/) ⭐️ 8.0/10

Typst 0.15.0 introduces support for multiple bibliographies in a single document, improved HTML export with automatic MathML for equations, and various other enhancements. This release strengthens Typst as a viable LaTeX alternative for academic and technical writing, addressing a long-requested feature that improves document organization and cross-referencing. Multiple bibliographies allow separate reference lists per chapter or section; HTML export now includes MathML for better web visibility. The release also includes performance improvements and bug fixes.

hackernews · schu · Jun 15, 17:24 · [Discussion](https://news.ycombinator.com/item?id=48544396)

**Background**: Typst is a modern, markup-based typesetting system designed to be easier to learn than LaTeX while producing high-quality output. It compiles to PDF, PNG, and HTML. The project is open-source and has gained significant traction in academia and industry.

<details><summary>References</summary>
<ul>
<li><a href="https://typst.app/">Typst : The new foundation for documents</a></li>
<li><a href="https://github.com/typst/typst">GitHub - typst / typst : A markup-based typesetting system that is...</a></li>
<li><a href="https://grokipedia.com/page/Typst">Typst</a></li>

</ul>
</details>

**Discussion**: The community reaction is largely positive, with users praising the new features like multiple bibliographies and HTML/MathML support. However, some users note ongoing issues with footnotes, particularly for discursive footnotes with bibliography references, and hope for further improvements.

**Tags**: `#typst`, `#typesetting`, `#open-source`, `#version-release`

---

<a id="item-11"></a>
## [Linux 7.1 Kernel Sets Developer Record with 15,849 Commits](https://lwn.net/Articles/1077425/) ⭐️ 8.0/10

The Linux 7.1 kernel was released on June 14, 2026, with 15,849 non-merge changesets from 2,479 developers, making it one of the busiest cycles and setting a new record for the number of developers. This milestone highlights the growing and vibrant contributor base of the Linux kernel, reflecting the health of the open-source ecosystem and the increasing complexity of kernel development. Only four other releases (6.7, 5.8, 5.10, 5.13) have had more commits, with the 6.7 record driven by the inclusion of the bcachefs filesystem. The top contributor by changesets was Johan Hovold with 181 commits, while Jakub Kicinski changed the most lines (126,367).

rss · LWN.net · Jun 15, 16:36

**Background**: LWN.net is a respected publication covering Linux and free software development, often providing detailed analysis of kernel releases. Each Linux kernel development cycle lasts about two months, and the number of commits and developers are key metrics for community activity. The bcachefs filesystem, a copy-on-write filesystem merged in kernel 6.7, caused an unusually high number of commits.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/LWN.net">LWN.net - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Bcachefs">Bcachefs - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#development statistics`, `#kernel release`, `#LWN`, `#open source community`

---

<a id="item-12"></a>
## [curl declares 'summer of bliss', pauses vulnerability reports](https://lwn.net/Articles/1077946/) ⭐️ 8.0/10

From July 1 to August 3, 2026, curl will not accept vulnerability reports from submitters without a paid support contract. Maintainer Daniel Stenberg calls this period the 'curl summer of bliss' to allow the team to rest after intense pressure. This decision highlights the growing problem of maintainer burnout in open-source projects, especially critical infrastructure like curl that underpins countless systems. It may encourage other projects to prioritize maintainer well-being and spark discussions on sustainable security practices. The GitHub issue and pull-request trackers will remain open, but vulnerability reports will be ignored unless from paying support customers. The release of curl 8.22.0 has been delayed by two weeks to September 2, 2026.

rss · LWN.net · Jun 15, 13:32

**Background**: curl is a widely used command-line tool and library for transferring data with URLs, supporting protocols like HTTP, FTP, and many others. It is maintained primarily by Daniel Stenberg and a small team. The project has recently faced a surge in vulnerability reports, increasing pressure on the maintainers, leading to this temporary pause to prevent burnout.

**Tags**: `#curl`, `#security`, `#vulnerability reporting`, `#open source`, `#maintenance`

---

<a id="item-13"></a>
## [LLMs exhibit model-specific name biases](https://www.reddit.com/r/MachineLearning/comments/1u6mn3q/ai_language_models_have_favorite_names_and_we/) ⭐️ 8.0/10

Researchers discovered that large language models have strong, version-specific preferences for certain character names like Elena Vasquez and Marcus Chen, which appear consistently across diverse AI-generated content. This finding reveals systematic, model-specific biases in LLMs that have practical implications for AI-generated content detection and understanding model behavior. These biased names appear as correlated ensembles across dozens of websites, portraying characters as volcano experts, podcast hosts, and authors of thousands of papers. The research emerged as a side finding from a model diffing method called CDD.

reddit · r/MachineLearning · /u/CebulkaZapiekana · Jun 15, 17:07

**Background**: Large language models (LLMs) are AI systems trained on vast text data to generate human-like text. They can exhibit biases due to patterns in training data. The CDD (model diffing) method aims to compare model behaviors, and in this case, it uncovered name biases that are specific to each model version.

<details><summary>References</summary>
<ul>
<li><a href="https://transformer-circuits.pub/2024/model-diffing/">Stage-Wise Model Diffing</a></li>
<li><a href="https://medium.com/@dariussingh/ensemble-llms-with-llm-blender-bebb9eb0e6cf">Ensemble LLMs with LLM-Blender. LLM-Blender... | Medium</a></li>

</ul>
</details>

**Tags**: `#LLMs`, `#AI bias`, `#model behavior`, `#character names`, `#arXiv paper`

---

<a id="item-14"></a>
## [Neocortical Learning Framework via Temporal Derivatives](https://www.reddit.com/r/MachineLearning/comments/1u6x8al/how_the_brains_learn_r/) ⭐️ 8.0/10

A new paper proposes error-driven predictive learning via temporal derivatives as a complete framework for neocortical learning, implemented in the Axon simulation framework using spiking neurons. This framework claims to meet all criteria for neocortical learning, potentially surpassing backpropagation and improving training times, impacting both AI and neuroscience. The framework is driven by corticothalamic circuits and uses competitive kinase synaptic plasticity induction mechanisms. It has been demonstrated on cognitively motivated tasks.

reddit · r/MachineLearning · /u/Terminator857 · Jun 15, 23:39

**Background**: The neocortex is the brain's center for higher-order functions like perception and language. Backpropagation, the dominant learning algorithm in deep learning, is not biologically plausible. Predictive coding and error-driven learning are biologically inspired alternatives that approximate backpropagation.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Neuron_(software)">Neuron (software) - Wikipedia</a></li>
<li><a href="https://video.ucdavis.edu/media/Meeting+4-1-21A+Predictive+Error-Driven+Learning/1_irkap338/208414893">Meeting 4-1-21: Predictive Error - Driven Learning - University of...</a></li>
<li><a href="https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2021.721186/full">Frontiers | Corticothalamic Pathways in Auditory Processing: Recent...</a></li>

</ul>
</details>

**Tags**: `#neuroscience`, `#deep learning`, `#synaptic plasticity`, `#cortical learning`, `#spiking neural networks`

---

<a id="item-15"></a>
## [Cleo: A 2B Parameter Model for Unified Text-to-SQL](https://www.reddit.com/r/MachineLearning/comments/1u6udpb/cleo_trying_to_fit_full_analyst_behavior_in_a_2b/) ⭐️ 8.0/10

Cleo is a 2B parameter fine-tuned model based on Qwen3.5-2B-Base that uses a unified harness for gathering, repairing, and answering SQL queries, enabling live execution-based search and efficient resource usage. This demonstrates that small models can achieve competitive text-to-SQL performance when training, evaluation, and inference are tightly integrated, making it practical for resource-constrained deployments. Cleo includes a SQL safety layer, dialect handling, timeouts, and clarification behavior as part of its unified system, and the model, dataset, and harness are fully open-source.

reddit · r/MachineLearning · /u/Dreeseaw · Jun 15, 21:43

**Background**: Text-to-SQL involves converting natural language questions into SQL queries. Most industrial chatbots rely on either text-to-SQL or retrieval-augmented generation (RAG). Traditional approaches often use separate components for different stages, leading to inefficiencies.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/awslabs/unified-text2sql-benchmark">UNITE: A Unified Benchmark for Text-to-SQL Evaluation</a></li>
<li><a href="https://arxiv.org/abs/2305.16265v3">UNITE: A Unified Benchmark for Text-to-SQL Evaluation Unified Context-Intent Embeddings for Scalable Text-to-SQL Valid Text-to-SQL Generation with Unification-Based ... Bridging the gap between text-to-SQL research and real-world ... Natural Language to SQL Semantic Kernel Multi-Agent System ... UNITE: A Unified Benchmark for Text-to-SQL Evaluation - ADS</a></li>

</ul>
</details>

**Tags**: `#Text-to-SQL`, `#Small Language Models`, `#Open Source`, `#Fine Tuning`, `#NLP`

---

<a id="item-16"></a>
## [ByteDance in Talks to Buy AI Chips from China's Iluvatar Corex](https://www.reuters.com/world/china/bytedance-talks-with-chinas-iluvatar-corex-purchase-ai-chips-sources-say-2026-06-15/) ⭐️ 8.0/10

ByteDance is negotiating with Shanghai-based Iluvatar Corex to purchase AI chips for inference tasks, and is also considering Baidu's Kunlun chips as an additional supplier. If the deal goes through, Iluvatar Corex could become ByteDance's third major domestic GPU supplier, with at least 50,000 chips expected to be delivered this year. This move signals ByteDance's strategic shift to diversify its AI chip supply amid US export restrictions on advanced chips to China. It could significantly boost domestic chip companies like Iluvatar Corex and Baidu, and reshape the AI inference hardware landscape in China. The chips are primarily intended for AI inference workloads, not training. The news caused Iluvatar Corex's Hong Kong-listed stock to surge 12%.

telegram · zaihuapd · Jun 15, 06:53

**Background**: ByteDance, the parent company of TikTok, is one of China's largest consumers of AI chips for its recommendation algorithms and content moderation. Currently, its main domestic GPU suppliers are Huawei and Cambricon. US export controls have restricted ByteDance's access to Nvidia's high-end chips, prompting it to seek domestic alternatives. Iluvatar Corex develops GPGPUs for AI, and Baidu's Kunlun chips are another homegrown option.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Iluvatar_CoreX">Iluvatar CoreX - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Kunlunxin">Kunlunxin - Wikipedia</a></li>
<li><a href="https://www.cnbc.com/2025/11/28/baidu-is-major-ai-chip-player-in-china-to-fill-nvidia-gap.html">Baidu is major AI chip player in China to fill Nvidia gap - CNBC</a></li>

</ul>
</details>

**Tags**: `#AI chips`, `#ByteDance`, `#semiconductor`, `#China tech`, `#inference`

---

<a id="item-17"></a>
## [Rio 3.5 Exposed as Wrapper of Open-Source Models Nex and Qwen](https://mp.weixin.qq.com/s/0oYevRBT8PPxG5hudOXxug) ⭐️ 8.0/10

The Rio 3.5 model, previously celebrated as an open-source state-of-the-art, was revealed by the Nex team to be a wrapper combining Nex and Qwen models. Evidence showed a 79% probability it identifies as Nex and linear interpolation of weights with a mix ratio of 0.57:0.43. This incident severely undermines trust in the open-source AI community, highlighting the need for transparency and integrity in model releases. It also draws attention to recurring plagiarism issues in the Chinese AI ecosystem. Rio 3.5 was removed from Hugging Face after the exposure, with the team apologizing and claiming the uploaded version was an unrefined distillation error. The collinearity between Rio and the model pair exceeded 0.98, making independent training highly unlikely.

telegram · zaihuapd · Jun 15, 12:39

**Background**: Model distillation is a knowledge transfer technique where a smaller model learns from a larger teacher model, often used to reduce size and cost. However, 'wrapper' or 'sleeve' models directly combine or mimic existing models without proper attribution, amounting to plagiarism. Similar incidents include Cursor's Composer 2 being revealed as Kimi and Stanford's Llama3-V copying MiniCPM-Llama3-V 2.5.

<details><summary>References</summary>
<ul>
<li><a href="https://www.sii.edu.cn/2025/1120/c27a605/page.htm">NEX ：下一代能动性 模 型 体系与开源生态</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/1914629163857473685">模型蒸馏是什么？一文带你搞懂“模型蒸馏”看这篇就够了！ - 知乎</a></li>
<li><a href="https://cloud.tencent.com/developer/article/2517760">一文读懂到底什么是“模型蒸馏（Model Distillation）”技术？-腾讯云开...</a></li>

</ul>
</details>

**Tags**: `#open-source`, `#AI model`, `#controversy`, `#plagiarism`, `#community trust`

---