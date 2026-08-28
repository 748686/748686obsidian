---
layout: default
title: "Horizon Summary: 2026-03-24 (EN)"
date: 2026-03-24
lang: en
---

> From 28 items, 6 important content pieces were selected

---

1. [iPhone 17 Pro Demonstrated Running a 400B Parameter LLM](#item-1) ⭐️ 8.0/10
2. [Blog explores using LLM agents for automated research on an old idea](#item-2) ⭐️ 7.0/10
3. [Linux kernel patch allows BPF programs to transition between sleepable and atomic contexts](#item-3) ⭐️ 7.0/10
4. [MiniMax upgrades Coding Plan to Token Plan with multimodal support and announces MiniMax 2.7 open-source weights release](#item-4) ⭐️ 7.0/10
5. [Tech Companies Evaluate Employees Based on LLM Token Consumption](#item-5) ⭐️ 7.0/10
6. [OpenAI recommends UK include AI chatbots in Google search choice page](#item-6) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [iPhone 17 Pro Demonstrated Running a 400B Parameter LLM](https://twitter.com/anemll/status/2035901335984611412) ⭐️ 8.0/10

A demonstration shows an iPhone 17 Pro running a 400 billion parameter large language model, utilizing techniques like quantization and Mixture of Experts architecture to enable this on mobile hardware. This demonstration is significant as it pushes the boundaries of on-device AI, potentially enabling advanced language models to run locally on smartphones without constant cloud connectivity, which could revolutionize mobile applications and privacy. The model uses Mixture of Experts architecture, which activates only a subset of parameters at a time, and quantization to reduce precision, lowering memory and computational requirements; however, practical limitations like thermal throttling and reduced accuracy due to quantization are noted.

hackernews · anemll · Mar 23, 14:30

**Background**: Large language models (LLMs) are AI systems trained on vast text data to generate human-like text; parameters measure model size, with higher counts typically requiring more computational resources. Quantization is a technique that reduces the precision of model weights (e.g., from 32-bit to 8-bit) to decrease memory usage and speed up inference while maintaining accuracy. Mixture of Experts (MoE) is an architecture where a model consists of multiple specialized sub-models (experts), with a routing mechanism selecting only a few experts per input, making large models more efficient by not using all parameters simultaneously.

<details><summary>References</summary>
<ul>
<li><a href="https://www.geeksforgeeks.org/deep-learning/quantization-in-deep-learning/">What is Quantization - GeeksforGeeks</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>
<li><a href="https://www.mayhemcode.com/2025/12/the-complete-guide-to-local-llm.html">The Complete Guide to Local LLM Hardware: Specs for Running AI Models on Consumer Hardware</a></li>

</ul>
</details>

**Discussion**: Community discussion includes skepticism about the headline's omission of MoE details and quantization's impact on model performance, with users noting that quantization can make models behave like smaller ones and that thermal throttling on devices like iPads limits practical use. Some comments also reference technical papers and express concerns about hardware limitations.

**Tags**: `#LLM`, `#Mobile AI`, `#Hardware`, `#Quantization`, `#Mixture of Experts`

---

<a id="item-2"></a>
## [Blog explores using LLM agents for automated research on an old idea](https://ykumar.me/blog/eclip-autoresearch/) ⭐️ 7.0/10

A blog post detailed an experiment using LLM agents to automate research on an old idea, with the agent acting like a hyperparameter optimization algorithm with basic reasoning. The system, based on a simple loop in a program.md file, iteratively improves training code, runs experiments, and records results. This approach demonstrates how LLM agents can accelerate research by automating tedious tasks like hyperparameter tuning and code iteration, potentially reducing human effort and enabling large-scale experimentation. It aligns with broader trends in AI automation, where agents are being developed to handle complex workflows in scientific and technical domains. The core of the system is a simple loop in program.md that favors simplicity, while other files include an arbitrary ML model for training. However, limitations include high costs if agents try all LLM recommendations and reliance on potentially niche or poorly maintained libraries.

hackernews · ykumards · Mar 23, 18:40

**Background**: LLM agents are AI systems that combine large language models with modules like planning and memory to execute complex tasks autonomously. Autoresearch systems, such as those popularized by Karpathy, use agents to run multiple experiments overnight, automating parts of the research process. These systems aim to reduce costs and accelerate discovery by handling iterative tasks like code optimization and evaluation.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2501.04227">Agent Laboratory: Using LLM Agents as Research Assistants</a></li>
<li><a href="https://datasciencedojo.com/blog/karpathy-autoresearch-explained/">Karpathy Autoresearch Explained: 100 Experiments Overnight</a></li>
<li><a href="https://www.promptingguide.ai/research/llm-agents">LLM Agents | Prompt Engineering Guide</a></li>

</ul>
</details>

**Discussion**: Community comments highlight practical applications, such as using LLMs for prior art exploration with mixed success, and concerns about cost efficiency and data bottlenecks. Some users note that similar iterative approaches with feedback loops are common in complex LLM deployments, while others question whether autoresearch offers advantages over traditional hyperparameter optimization methods.

**Tags**: `#AI Research`, `#LLM Agents`, `#Automated Systems`, `#Machine Learning`, `#Hacker News`

---

<a id="item-3"></a>
## [Linux kernel patch allows BPF programs to transition between sleepable and atomic contexts](https://lwn.net/Articles/1062868/) ⭐️ 7.0/10

Puranjay Mohan has proposed a patch set that enables BPF programs running in sleepable contexts to temporarily acquire locks and transition to atomic contexts, addressing a current limitation where such transitions were prohibited. The implementation introduces a new KF_FORBID_FAULT marker that allows the BPF verifier to track sleep permissions on an instruction-by-instruction basis rather than globally for the entire program. This development is significant because it allows more BPF programs to be marked as sleepable, enabling them to copy data from user space—a common operation that requires the ability to sleep. By providing finer-grained context tracking, the patch set enhances the flexibility and performance of BPF programs in the Linux kernel, potentially expanding their use cases in areas like memory management and concurrency control. The patch set adds a KF_FORBID_FAULT marker that can only be used on kfuncs already marked with KF_ACQUIRE, temporarily preventing the program from sleeping while holding the acquired resource. However, BPF maintainer Alexei Starovoitov has raised objections to parts of the implementation, meaning acceptance depends on whether Mohan can address these concerns.

rss · LWN.net · Mar 23, 16:00

**Background**: BPF (Berkeley Packet Filter) programs in the Linux kernel can run in either sleepable or atomic (non-sleepable) contexts. Atomic contexts forbid operations that could delay kernel execution, such as waiting for I/O or handling page faults. Sleepable BPF programs, introduced in 2020, allow copying from user space but were restricted from calling many existing BPF interfaces that assumed atomic contexts. Kfuncs are kernel functions accessible to BPF programs, with markers like KF_ACQUIRE and KF_RELEASE helping the verifier track resource management.

<details><summary>References</summary>
<ul>
<li><a href="https://lwn.net/Articles/825415/">Sleepable BPF programs [LWN.net]</a></li>
<li><a href="https://docs.kernel.org/bpf/kfuncs.html">BPF Kernel Functions (kfuncs) — The Linux Kernel documentation</a></li>
<li><a href="https://lwn.net/Articles/779120/">Concurrency management in BPF [LWN.net]</a></li>

</ul>
</details>

**Tags**: `#Linux Kernel`, `#BPF`, `#Kernel Programming`, `#Concurrency`, `#Patch Development`

---

<a id="item-4"></a>
## [MiniMax upgrades Coding Plan to Token Plan with multimodal support and announces MiniMax 2.7 open-source weights release](https://mp.weixin.qq.com/s/o4KGGgtp32vRMecOYCbVmA) ⭐️ 7.0/10

MiniMax has upgraded its Coding Plan to Token Plan, providing Plus and higher-tier users with additional credits for video, audio, music, and image multimodal model calls while maintaining their original programming model usage. The company also announced that MiniMax 2.7 open-source weights will be released in approximately two weeks, following recent performance improvements on the OpenClaw benchmark. This upgrade makes MiniMax's platform more versatile by integrating multimodal AI capabilities into a single subscription, potentially reducing costs and complexity for developers working with diverse AI models. The upcoming open-source release of MiniMax 2.7 weights will enable broader community access to their latest coding-focused model, fostering innovation and adoption in AI-assisted development tools. To ensure service stability during peak hours, MiniMax will implement dynamic rate limiting on weekday afternoons (3:00-5:30 PM), with weekly call limits set at 10 times the original programming model's 5-hour usage allowance. The MiniMax 2.7 model has shown significant performance improvements on the OpenClaw benchmark, which specifically tests AI agent tool-calling capabilities.

telegram · zaihuapd · Mar 23, 02:09

**Background**: MiniMax's Coding Plan is a subscription service that provides access to their coding-focused AI models, with usage limits that refresh periodically. The platform has previously offered models like MiniMax-M2, which is designed for coding and agentic workflows with efficient inference speeds. OpenClaw is a benchmark that evaluates LLM performance in real-world tool-calling scenarios for AI agents, going beyond traditional isolated capability tests.

<details><summary>References</summary>
<ul>
<li><a href="https://platform.minimax.io/subscribe/coding-plan">Token Plan - MiniMax API Platform</a></li>
<li><a href="https://github.com/MiniMax-AI/MiniMax-M2">GitHub - MiniMax-AI/MiniMax-M2: MiniMax-M2, a model built for ...</a></li>
<li><a href="https://github.com/Shad107/openclaw-benchmark">GitHub - Shad107/ openclaw - benchmark : Real-world LLM benchmark ...</a></li>

</ul>
</details>

**Tags**: `#AI/ML`, `#multimodal models`, `#open-source`, `#software engineering`, `#API services`

---

<a id="item-5"></a>
## [Tech Companies Evaluate Employees Based on LLM Token Consumption](https://gizmodo.com/tech-employees-are-reportedly-being-evaluated-by-how-fast-they-burn-through-llm-tokens-2000736627) ⭐️ 7.0/10

According to reports, tech companies including Meta and OpenAI are evaluating employee performance based on their consumption of LLM tokens, with high usage being rewarded and low usage penalized. An OpenAI engineer reportedly consumed 210 billion tokens cumulatively, and OpenAI president Greg Brockman stated that GPT-5.4 processed 5 trillion tokens daily within a week of its launch. This represents a significant shift in workplace performance metrics, potentially creating incentives for excessive AI usage rather than focusing on quality outcomes. It raises important questions about how AI adoption should be measured in professional settings and could influence broader industry trends in productivity evaluation. The practice has reportedly created internal leaderboards where employees compete on token usage, with companies like Meta and Shopify explicitly incorporating AI usage metrics into performance reviews. This approach focuses on quantitative consumption rather than qualitative outcomes or innovation impact.

telegram · zaihuapd · Mar 23, 08:42

**Background**: LLM tokens are the basic units of text processing in large language models, with token counts directly correlating to computational costs and API pricing. GPT-5.4 is OpenAI's latest frontier model released in March 2026, featuring advanced capabilities and a 1M-token context window. Performance metrics in tech companies traditionally focus on outputs like code quality, project delivery, and business impact rather than input consumption.

<details><summary>References</summary>
<ul>
<li><a href="https://winder.ai/calculating-token-counts-llm-context-windows-practical-guide/">Calculating LLM Token Counts: A Practical Guide</a></li>
<li><a href="https://en.wikipedia.org/wiki/GPT-5.4">GPT-5.4 - Wikipedia</a></li>
<li><a href="https://careeraheadonline.com/tech-workers-embrace-tokenmaxxing-a-new-ai-rivalry/">Tech Workers Embrace Tokenmaxxing: A New AI Rivalry</a></li>

</ul>
</details>

**Tags**: `#AI Ethics`, `#Workplace Culture`, `#LLM Usage`, `#Performance Metrics`, `#Tech Industry`

---

<a id="item-6"></a>
## [OpenAI recommends UK include AI chatbots in Google search choice page](https://assets.publishing.service.gov.uk/media/69b970dcc06ba9576435ab5a/OpenAI.pdf) ⭐️ 7.0/10

On March 6, OpenAI submitted a public consultation response to the UK Competition and Markets Authority (CMA), recommending that Google's search choice page eligibility criteria explicitly include AI chatbots with search capabilities, allowing services like ChatGPT to be selected as default search options on Android devices and Chrome. OpenAI also proposed using transparent, dynamic popularity metrics to determine inclusion and expanding the choice page to voice, visual, and AI-assisted search entry points. This recommendation could ensure fair competition by allowing emerging AI services like ChatGPT to compete directly with established search engines such as Google, potentially reshaping market dynamics and increasing user access to innovative AI-driven search tools. It highlights a novel regulatory approach for integrating advanced technologies into existing frameworks, which may influence global policies on digital market competition and AI accessibility. OpenAI argues that ChatGPT and similar services perform broad information discovery through conversational or multimodal methods, functionally akin to Google Search's AI Overviews and AI Mode, and that current draft rules focused on traditional search could exclude these new services. The proposal targets the UK's CMA as part of its digital market regulation efforts, with Google's search choice page being a key compliance mechanism under the Digital Markets Act in Europe.

telegram · zaihuapd · Mar 23, 14:50

**Background**: The Google search choice page is a feature introduced to comply with regulations like the EU's Digital Markets Act, allowing users in certain regions to select their default search engine and browser during device setup on Android. The UK Competition and Markets Authority (CMA) is a regulatory body that promotes competition and protects consumers, currently reviewing digital market rules that could designate major platforms like Google and Apple with 'strategic market status'. AI Overviews and AI Mode are Google Search features that use AI to generate summaries and provide advanced reasoning capabilities, representing the integration of AI into traditional search functions.

<details><summary>References</summary>
<ul>
<li><a href="https://www.neowin.net/news/google-will-add-new-search-and-browser-choice-screens-for-android-phones-in-europe/">Google will add new search and browser choice screens for... - Neowin</a></li>
<li><a href="https://www.gov.uk/government/organisations/competition-and-markets-authority">Competition and Markets Authority - GOV. UK</a></li>
<li><a href="https://en.wikipedia.org/wiki/AI_Overviews">AI Overviews - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#AI Regulation`, `#Search Engines`, `#Competition Policy`, `#OpenAI`, `#UK CMA`

---