---
layout: default
title: "Horizon Summary: 2026-04-26 (EN)"
date: 2026-04-26
lang: en
---

> From 25 items, 14 important content pieces were selected

---

1. [Trump Fires All 24 Members of National Science Board](#item-1) ⭐️ 9.0/10
2. [Google Plans Up to $40B Investment in Anthropic](#item-2) ⭐️ 9.0/10
3. [Qwen3.6-27B runs at 80 tps on single RTX 5090 with vLLM](#item-3) ⭐️ 8.0/10
4. [GLM-5.1 Runs Locally at 40 tps, 2000+ pp/s](#item-4) ⭐️ 8.0/10
5. [DeepSeek V4 Update Sparks Community Debate](#item-5) ⭐️ 8.0/10
6. [TeamViewer 13/14 to End Public Internet Connections by 2026](#item-6) ⭐️ 8.0/10
7. [China's Q1 2026 GDP Growth Masks Rising Youth and Migrant Unemployment](#item-7) ⭐️ 8.0/10
8. [OpenAI Launches GPT-5.5 Biosecurity Bug Bounty Program](#item-8) ⭐️ 8.0/10
9. [New 10GbE USB Adapters: Smaller, Cooler, Cheaper](#item-9) ⭐️ 7.0/10
10. [OpenAI Confirms No Separate GPT-5.5 Codex Model](#item-10) ⭐️ 7.0/10
11. [OpenAI Releases GPT-5.5 Prompting Guide](#item-11) ⭐️ 7.0/10
12. [Xiaomi MiMo V2.5 Pro Debuts on AI Index, Weights Coming](#item-12) ⭐️ 7.0/10
13. [FCC Expands Router Ban to Mobile Hotspots and CPE Devices](#item-13) ⭐️ 7.0/10
14. [China Regulates Online Financial Product Marketing](#item-14) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Trump Fires All 24 Members of National Science Board](https://www.science.org/content/article/trump-fires-nsf-s-oversight-board) ⭐️ 9.0/10

President Trump has fired all 24 members of the National Science Board, the oversight body of the National Science Foundation (NSF), effectively removing the entire board that sets NSF policies and advises the president and Congress on science and engineering issues. This unprecedented move raises serious concerns about political interference in science, as the National Science Board plays a critical role in ensuring the independence and integrity of NSF's research funding decisions. The firing could disrupt NSF operations and undermine trust in U.S. science policy. The National Science Board consists of 24 presidentially appointed members plus the NSF director as an ex officio member; all 24 appointed members have been terminated. The board has statutory responsibilities including policy oversight of NSF and advisory duties to the president and Congress.

hackernews · skullone · Apr 25, 22:39

**Background**: The National Science Foundation (NSF) is a major U.S. government agency that funds fundamental research and education in science and engineering. The National Science Board, established by the NSF Act of 1950, provides independent oversight and policy guidance to NSF, and also serves as an advisory body to the president and Congress. Board members are typically distinguished scientists and engineers appointed to staggered six-year terms.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/National_Science_Board">National Science Board - Wikipedia</a></li>
<li><a href="https://www.nsf.gov/">NSF - U.S. National Science Foundation</a></li>

</ul>
</details>

**Discussion**: Commenters expressed shock and concern, with many viewing the firing as a move to undermine scientific integrity. Some questioned the board's importance, while others speculated about future appointments of political allies. A few sought a silver lining, hoping a future administration could rebuild the system better.

**Tags**: `#NSF`, `#science policy`, `#US politics`, `#research funding`

---

<a id="item-2"></a>
## [Google Plans Up to $40B Investment in Anthropic](https://www.bloomberg.com/news/articles/2026-04-24/google-plans-to-invest-up-to-40-billion-in-anthropic) ⭐️ 9.0/10

Google plans to invest up to $40 billion in AI company Anthropic, including $10 billion in cash at a $350 billion valuation and up to $30 billion more based on performance targets, plus 5 gigawatts of compute capacity via Google Cloud over five years. This massive investment underscores Google's strategic bet on Anthropic as a key AI partner, potentially reshaping the competitive landscape against rivals like OpenAI and Microsoft, and signals the growing importance of compute resources in AI development. Anthropic, which develops the Claude AI model and the Claude Code coding tool, is considering an IPO as early as October. Amazon recently added another $5 billion to its investment in Anthropic.

telegram · zaihuapd · Apr 25, 11:02

**Background**: Anthropic is an AI safety and research company founded by former OpenAI employees, known for its Claude series of large language models. Google has been a prior investor, and this new deal includes significant cloud computing resources using Google's custom TPU chips, which are specialized for AI workloads.

<details><summary>References</summary>
<ul>
<li><a href="https://www.linkedin.com/company/anthropicresearch">Anthropic | LinkedIn</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>

</ul>
</details>

**Tags**: `#AI`, `#investment`, `#Anthropic`, `#Google`, `#cloud computing`

---

<a id="item-3"></a>
## [Qwen3.6-27B runs at 80 tps on single RTX 5090 with vLLM](https://www.reddit.com/r/LocalLLaMA/comments/1sv8eua/qwen3627b_at_80_tps_with_218k_context_window_on/) ⭐️ 8.0/10

A Reddit user demonstrated running the Qwen3.6-27B model at approximately 80 tokens per second with a 218k context window on a single RTX 5090 GPU using vLLM 0.19.1rc1, and shared a detailed recipe for reproducing the setup. This achievement shows that large 27B-parameter models can now run efficiently on consumer-grade hardware, making advanced LLM inference more accessible to individuals and small teams without expensive server infrastructure. The model uses NVFP4 quantization and Multi-Token Prediction (MTP) to reduce memory and improve throughput. The recipe is based on a previous post for Qwen3.5-27B, which achieved 77 tps on the same hardware.

reddit · r/LocalLLaMA · Kindly-Cantaloupe978 · Apr 25, 10:21

**Background**: NVFP4 is a 4-bit floating-point quantization format that preserves dynamic range better than integer quantization. Multi-Token Prediction (MTP) is a training strategy where the model learns to predict multiple future tokens simultaneously, which can be combined with speculative decoding to speed up inference. vLLM is an open-source high-throughput inference engine that supports various optimizations for LLM serving.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2601.20088">[2601.20088] Quantization-Aware Distillation for NVFP4</a></li>
<li><a href="https://arxiv.org/abs/2512.02010">[2512.02010] Four Over Six: More Accurate NVFP4 Quantization</a></li>
<li><a href="https://github.com/vllm-project/vllm">vllm -project/ vllm : A high-throughput and memory-efficient inference ...</a></li>

</ul>
</details>

**Discussion**: The post received high engagement (266 upvotes, 97% ratio), indicating strong community interest. Comments likely discuss the impressive performance and the practicality of running large models on consumer GPUs.

**Tags**: `#LLM`, `#vLLM`, `#RTX 5090`, `#Qwen`, `#local inference`

---

<a id="item-4"></a>
## [GLM-5.1 Runs Locally at 40 tps, 2000+ pp/s](https://www.reddit.com/r/LocalLLaMA/comments/1svgtlh/glm_51_locally_40tps_2000_pps/) ⭐️ 8.0/10

A user achieved 40 tokens/sec generation and over 2000 prefilled tokens/sec running the 478B-parameter GLM-5.1 model locally on 4 NVIDIA RTX 6000 Pro GPUs using REAP-NVFP4 quantization and custom SGLang patches. This demonstrates that very large open-source models (478B parameters) can be run efficiently on consumer-grade hardware, potentially democratizing access to frontier-level LLMs for local inference and development. The setup uses 4 RTX 6000 Pro GPUs (limited to 350W each) with REAP-NVFP4 quantization (which prunes experts from 256 to 154) and two small patches to SGLang for Blackwell architecture support. Throughput degrades gracefully with context depth, from 2229 pp/s at 0 prefilled to 863 pp/s at 64K context.

reddit · r/LocalLLaMA · val_in_tech · Apr 25, 16:31

**Background**: GLM-5.1 is a large language model with 478 billion parameters, making it one of the largest open-weight models. REAP-NVFP4 is a quantization technique that combines expert pruning (REAP) with NVIDIA's FP4 format to reduce model size and memory bandwidth requirements. SGLang is a high-performance serving framework for LLMs, and the RTX 6000 Pro is NVIDIA's Blackwell-architecture workstation GPU with 96 GB of memory.

<details><summary>References</summary>
<ul>
<li><a href="https://developers.redhat.com/articles/2026/02/04/accelerating-large-language-models-nvfp4-quantization">Accelerating large language models with NVFP4 quantization</a></li>

</ul>
</details>

**Discussion**: The Reddit community reacted positively (92% upvote ratio), with users impressed by the throughput and asking about further optimization and concurrency settings. The author noted that inference software is still under-optimized for these cards and expects true potential to unfold soon.

**Tags**: `#LLM inference`, `#local LLM`, `#quantization`, `#hardware optimization`, `#GLM`

---

<a id="item-5"></a>
## [DeepSeek V4 Update Sparks Community Debate](https://i.redd.it/he3eoyzr9bxg1.png) ⭐️ 8.0/10

DeepSeek has released an update to its V4 model, continuing its tradition of open-weight releases and detailed research papers, while competitors like Kimi, GLM, and Qwen have moved toward more closed practices. DeepSeek 对开放性的承诺对 AI 社区至关重要，它提供了可访问的高性能模型和透明的研究，推动了创新，与行业向封闭模型发展的趋势形成对比。 The V4 Pro model is approximately 2.5x larger than V3.2 (1.6T vs 0.67T parameters), and some users report that it uses significantly more tokens for generation, suggesting a decrease in intelligence density compared to competitors like GPT-5.4 and GPT-5.5.

reddit · r/LocalLLaMA · techlatest_net · Apr 25, 10:10

**Background**: Open-weight models release the trained neural network parameters, allowing others to run and fine-tune the model. Base models are pre-trained on large text corpora and can be further fine-tuned for specific tasks. DeepSeek has been a leader in open-weight LLMs, consistently publishing research and releasing models promptly.

<details><summary>References</summary>
<ul>
<li><a href="https://openweight.org/">Open Weight Definition (OWD)</a></li>
<li><a href="https://www.analyticsvidhya.com/blog/2025/04/open-weight-models/">What are Open Source and Open Weight Models?</a></li>
<li><a href="https://toloka.ai/blog/base-llm-vs-instruction-tuned-llm/">Base LLM vs. instruction-tuned LLM - toloka.ai</a></li>

</ul>
</details>

**Discussion**: The community is divided: some praise DeepSeek for maintaining openness while others criticize the V4 Pro's increased token usage and lower intelligence density compared to GPT-5.4 and GPT-5.5, noting that DeepSeek requires roughly 10x more tokens for similar performance.

**Tags**: `#DeepSeek`, `#LLM`, `#AI`, `#Open Source`, `#Model Update`

---

<a id="item-6"></a>
## [TeamViewer 13/14 to End Public Internet Connections by 2026](https://www.landiannews.com/archives/112799.html) ⭐️ 8.0/10

TeamViewer announced that versions 13 and 14 will reach end of life on October 31, 2026, after which they will no longer support public internet connections via official servers, only local network functionality. This forces users who purchased perpetual licenses for these versions to switch to a subscription model to continue using remote access over the internet, raising concerns about vendor lock-in and the devaluation of perpetual licenses. Perpetual license holders cannot upgrade to newer versions for free; TeamViewer offers migration discounts but does not provide a free path. The company cites security improvements as the reason for the change.

telegram · zaihuapd · Apr 25, 05:43

**Background**: TeamViewer is a popular remote desktop software that historically offered perpetual licenses. In recent years, the company has shifted to a subscription-only model, and older versions have been phased out. Version 12 support ended earlier, and now versions 13 and 14 are being deprecated.

<details><summary>References</summary>
<ul>
<li><a href="https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-classic/licensing/subscription/teamviewer-product-lifecycle-policies/">TeamViewer Product Lifecycle Policies</a></li>
<li><a href="https://community.teamviewer.com/English/kb/articles/49188-teamviewer-product-lifecycle-policies">TeamViewer Product Lifecycle Policies - TeamViewer Support</a></li>
<li><a href="https://community.spiceworks.com/t/teamviewer-accountability/1165153">TeamViewer Accountability - Water Cooler - Spiceworks Community</a></li>

</ul>
</details>

**Discussion**: Community discussions on Spiceworks and TeamViewer forums express frustration, with users criticizing the forced migration and high subscription costs. Some suggest alternatives like AnyDesk or RustDesk.

**Tags**: `#TeamViewer`, `#software licensing`, `#remote desktop`, `#EOL`

---

<a id="item-7"></a>
## [China's Q1 2026 GDP Growth Masks Rising Youth and Migrant Unemployment](https://m.caixin.com/m/2026-04-24/102437308.html) ⭐️ 8.0/10

China's Q1 2026 GDP grew 5% year-on-year, but the surveyed urban unemployment rate for ages 25-29 rose to 7.7% (highest since data release in Dec 2023) and for migrant agricultural workers to 5.7% (highest since COVID-19 ended), according to the National Bureau of Statistics. This structural disconnect between GDP growth and job creation signals that China's economic recovery is not translating into sufficient employment, especially for youth and migrant workers, which could fuel social instability and force policy adjustments. The 25-29 age group's unemployment rose from 6.8% to 7.7% over Q1, reflecting structural deterioration as these workers are more experienced and have higher labor force participation. Meanwhile, migrant worker unemployment hit a near-three-year high due to weakness in construction, manufacturing, and services.

telegram · zaihuapd · Apr 25, 14:45

**Background**: China's surveyed urban unemployment rate is a key labor market indicator calculated by the National Bureau of Statistics based on sample surveys. The employment elasticity of GDP measures how much employment increases per percentage point of GDP growth; capital-intensive industries like infrastructure and high-end manufacturing have low elasticity, meaning they create fewer jobs per unit of output.

<details><summary>References</summary>
<ul>
<li><a href="https://www.stats.gov.cn/zs/tjwh/tjkw/tjqk/zgxxb/202603/P020260302324455449803.pdf">01B20260302C</a></li>
<li><a href="http://www.niehuihua.com/uploads/soft/190213/1-1Z2131KT9.pdf">题目《哪类企 业 和行 业 更能吸纳 就 业 》</a></li>

</ul>
</details>

**Discussion**: The editor's note expresses disagreement with the expert view that GDP growth is driven by capital-intensive sectors with low employment elasticity, but retains the original text for readers' deep thinking. No other community comments are provided.

**Tags**: `#China economy`, `#unemployment`, `#labor market`, `#structural issues`, `#youth employment`

---

<a id="item-8"></a>
## [OpenAI Launches GPT-5.5 Biosecurity Bug Bounty Program](https://openai.com/zh-Hans-CN/index/gpt-5-5-bio-bug-bounty/) ⭐️ 8.0/10

OpenAI has launched a biosecurity bug bounty program for GPT-5.5, offering a $25,000 reward for the first universal jailbreak that bypasses five biosecurity challenges without triggering safeguards. The program is invitation-only, with applications open from April 23 to June 22, 2026, and testing from April 28 to July 27, 2026. This program highlights the growing concern over AI models being misused for biosecurity threats, such as generating instructions for harmful biological agents. By incentivizing researchers to find vulnerabilities, OpenAI aims to strengthen safety measures before broader deployment, setting a precedent for responsible AI release practices. The bounty specifically targets GPT-5.5 running in Codex Desktop, and requires a universal jailbreak that works across all five biosecurity challenges. Participants must sign a non-disclosure agreement and conduct evaluations on a dedicated platform.

telegram · zaihuapd · Apr 25, 16:36

**Background**: GPT-5.5 is OpenAI's latest large language model, emphasizing speed, accuracy, and real-world use. A universal jailbreak is a consistent attack strategy that bypasses safety guardrails across multiple queries, posing significant risks for enabling real-world harm. Biosecurity bug bounties are part of broader efforts to test and improve safeguards against misuse of advanced AI.

<details><summary>References</summary>
<ul>
<li><a href="https://indianexpress.com/article/technology/artificial-intelligence/openai-rolls-out-gpt-5-5-highlights-speed-accuracy-and-real-world-use-10653022/">OpenAI rolls out GPT - 5 . 5 , highlights speed... - The Indian Express</a></li>
<li><a href="https://deploymentsafety.openai.com/gpt-5-5">GPT - 5 . 5 System Card - OpenAI Deployment Safety Hub</a></li>
<li><a href="https://anonhaven.com/news/openai-zapustila-bug-bounty-dlya-gpt-55-25-000-za-universalnyj-jailbreak-v-biobezopasnosti/">OpenAI запустила GPT - 5 . 5 Bio Bug Bounty с призом $25 000</a></li>

</ul>
</details>

**Tags**: `#AI Safety`, `#Bug Bounty`, `#OpenAI`, `#Biosecurity`, `#GPT-5.5`

---

<a id="item-9"></a>
## [New 10GbE USB Adapters: Smaller, Cooler, Cheaper](https://www.jeffgeerling.com/blog/2026/new-10-gbe-usb-adapters-cooler-smaller-cheaper/) ⭐️ 7.0/10

New 10GbE USB adapters based on the Realtek RTL8159 chip are now available, offering smaller size, lower heat, and lower cost compared to previous Thunderbolt-based solutions. However, performance varies significantly depending on the host's USB standard support and interrupt handling capabilities. This makes 10GbE networking more accessible to a wider range of users, especially those with newer USB4 or Thunderbolt 4 ports, potentially accelerating adoption of high-speed wired networking in home and small office environments. The adapters use the Realtek RTL8159 chip and support USB 3.2 Gen 2x2 (20 Gbps) for full 10GbE speeds, but many hosts lack this standard, resulting in a downgrade to 10 Gbps USB 3.2 Gen 2. Additionally, interrupt rates on lower-powered devices like MacBook Neo can limit throughput, and iperf3 is single-threaded by default, which may underreport performance.

hackernews · calcifer · Apr 25, 05:56

**Background**: 10GbE (10 Gigabit Ethernet) is a high-speed networking standard offering 10 Gbps data transfer, commonly used in data centers and professional workflows. Traditionally, 10GbE adapters for laptops used Thunderbolt 3/4, which are expensive and bulky. Newer USB-based adapters leverage the USB4 and USB 3.2 Gen 2x2 standards to provide similar speeds at lower cost, but compatibility and performance depend on the host hardware.

<details><summary>References</summary>
<ul>
<li><a href="https://www.qnap.com/en-us/product/qna-uc10g1sf">QNA-UC10G1SF | USB 4 Type-C to 10GbE SFP+ Network Adapter, Compatible with USB 4 and Thunderbolt™ 3/4 Ports | QNAP (US)</a></li>
<li><a href="https://nascompares.com/2024/07/05/iocrest-usb4-to-10gbe-adapter-review/">IOCREST USB4 to 10GbE Adapter Review – NAS Compares</a></li>
<li><a href="https://superuser.com/questions/1284506/is-there-a-technical-reason-no-10gbe-usb-3-1-gen-2-adapters-exist-yet">networking - Is there a technical reason no 10GbE USB 3.1 Gen 2</a></li>

</ul>
</details>

**Discussion**: The community discussion highlights technical nuances: one commenter notes that iperf3 is single-threaded by default and suggests using -P 4 for multi-threaded testing to better measure performance. Another expresses confusion over USB version naming, while a third points out that Apple hardware lacks USB 3.2 Gen 2x2 support, so adapters downgrade to 10 Gbps. A link to a Framework expansion card is also shared.

**Tags**: `#networking`, `#hardware`, `#USB`, `#10GbE`, `#benchmark`

---

<a id="item-10"></a>
## [OpenAI Confirms No Separate GPT-5.5 Codex Model](https://simonwillison.net/2026/Apr/25/romain-huet/#atom-everything) ⭐️ 7.0/10

OpenAI's Romain Huet confirmed that GPT-5.5 will not have a separate Codex model, as coding capabilities have been unified into the main model since GPT-5.4. This unification simplifies OpenAI's product lineup and signals a strategic shift toward integrated multimodal and agentic capabilities, potentially improving developer experience and model efficiency. GPT-5.5 shows strong gains in agentic coding, computer use, and any task on a computer, building on the unification started in GPT-5.4.

rss · Simon Willison · Apr 25, 12:06

**Background**: OpenAI Codex was a specialized model for translating natural language into code, used in tools like GitHub Copilot. Agentic coding refers to AI agents that autonomously perform software development tasks. By merging Codex into the main GPT model, OpenAI aims to provide a single model capable of both general reasoning and code generation.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/OpenAI_Codex_(language_model)">OpenAI Codex (language model ) - Wikipedia</a></li>
<li><a href="https://openai.com/codex/">Codex | AI Coding Partner from OpenAI | OpenAI</a></li>
<li><a href="https://en.wikipedia.org/wiki/Agentic_coding">Agentic coding</a></li>

</ul>
</details>

**Tags**: `#openai`, `#gpt`, `#ai`, `#llms`, `#generative-ai`

---

<a id="item-11"></a>
## [OpenAI Releases GPT-5.5 Prompting Guide](https://simonwillison.net/2026/Apr/25/gpt-5-5-prompting-guide/#atom-everything) ⭐️ 7.0/10

OpenAI has released an official prompting guide for GPT-5.5, now available in the API, with tips including sending short user-visible updates during multi-step tasks to improve perceived responsiveness. This guide helps developers optimize prompts for GPT-5.5, which OpenAI recommends treating as a new model family rather than a drop-in replacement, potentially improving application performance and user experience. OpenAI advises starting with a fresh baseline prompt instead of migrating existing prompts from older models, and suggests using the Codex app with the command '$openai-docs migrate this project to gpt-5.5' to upgrade code.

rss · Simon Willison · Apr 25, 04:13

**Background**: GPT-5.5 is the latest large language model from OpenAI, succeeding GPT-5.2 and GPT-5.4. Prompting guides provide best practices for interacting with AI models to achieve desired outputs, and are crucial for developers building applications on top of these models.

<details><summary>References</summary>
<ul>
<li><a href="https://developers.openai.com/api/docs/models/gpt-5.5">GPT - 5 . 5 Model | OpenAI API</a></li>
<li><a href="https://apidog.com/blog/how-to-use-gpt-5-5-api/">How to Use the GPT - 5 . 5 API</a></li>

</ul>
</details>

**Tags**: `#GPT-5.5`, `#prompting`, `#OpenAI`, `#API`, `#LLM`

---

<a id="item-12"></a>
## [Xiaomi MiMo V2.5 Pro Debuts on AI Index, Weights Coming](https://www.reddit.com/gallery/1sv9q8f) ⭐️ 7.0/10

Xiaomi's MiMo V2.5 Pro model has been ranked 54th on the Artificial Analysis Intelligence Index, and the company hinted that model weights will be released soon. This marks Xiaomi's entry into the competitive AI leaderboard with a 1-trillion-parameter MoE model, and the potential open-weight release could significantly impact the local LLM community by enabling self-hosting and fine-tuning. MiMo V2.5 Pro is a multimodal, agentic LLM with 1 million context length, designed for complex software engineering and long-horizon tasks. It entered public beta on April 2026.

reddit · r/LocalLLaMA · Nunki08 · Apr 25, 11:33

**Background**: The Artificial Analysis Intelligence Index is a composite benchmark that aggregates ten challenging evaluations to measure AI capabilities across mathematics, science, coding, and reasoning. Xiaomi's MiMo series is a family of large language models developed by the Chinese electronics giant, with the V2.5 Pro being its most capable model to date.

<details><summary>References</summary>
<ul>
<li><a href="https://mimo.xiaomi.com/mimo-v2-5-pro">MiMo-V2.5-Pro | Xiaomi</a></li>
<li><a href="https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index">Artificial Analysis Intelligence Index</a></li>
<li><a href="https://tosea.ai/blog/mimo-v2-5-pro-complete-guide">How to Use MiMo-V2.5-Pro: Complete Guide to Xiaomi's New 1T ...</a></li>

</ul>
</details>

**Discussion**: The Reddit community showed high engagement with 342 upvotes and a 96% upvote ratio, expressing excitement about the potential open-weight release. Many users discussed the implications for self-hosting and competition with other open-weight models.

**Tags**: `#Xiaomi`, `#MiMo`, `#AI model`, `#open weights`, `#LLM`

---

<a id="item-13"></a>
## [FCC Expands Router Ban to Mobile Hotspots and CPE Devices](https://www.androidauthority.com/router-ban-expands-to-hotspots-3660505/) ⭐️ 7.0/10

The FCC has updated its ban on foreign-made Wi-Fi routers to now include consumer mobile hotspots (MiFi) and residential LTE/5G CPE devices. The ban applies only to new equipment applications, and some models are exempted until October 1, 2027. This expansion tightens supply chain restrictions on networking equipment, potentially affecting availability and pricing of mobile hotspots and fixed wireless access devices in the US. Consumers and businesses relying on these devices may face limited choices or higher costs. The ban does not affect existing approved models, smartphones with hotspot capabilities, or enterprise-grade equipment. The FCC has granted conditional exemptions to some manufacturers like Netgear, allowing sales of certain products until October 1, 2027.

telegram · zaihuapd · Apr 25, 09:32

**Background**: The FCC's Covered List identifies communications equipment that poses a national security risk, banning its authorization for use in the US. The original ban targeted foreign-made routers, and this update extends to mobile hotspots and CPE (Customer Premises Equipment) like LTE/5G fixed wireless terminals. CPE refers to devices at the customer's location that connect to a service provider's network, such as modems, routers, and gateways.

<details><summary>References</summary>
<ul>
<li><a href="https://www.fcc.gov/faqs-recent-updates-fcc-covered-list-regarding-routers-produced-foreign-countries">FAQs on Recent Updates to FCC Covered List Regarding Routers ...</a></li>
<li><a href="https://www.cnet.com/home/internet/fccs-foreign-made-router-ban-one-popular-brand-just-got-the-first-exemption/">FCC's Foreign-Made Router Ban: One Popular Brand Just Got the ...</a></li>
<li><a href="https://www.pcmag.com/news/why-is-fcc-banning-foreign-made-wi-fi-routers-what-you-need-to-know">Why Is the FCC Banning Foreign-Made Wi-Fi Routers ... - PCMag</a></li>

</ul>
</details>

**Tags**: `#FCC`, `#regulation`, `#routers`, `#hotspots`, `#CPE`

---

<a id="item-14"></a>
## [China Regulates Online Financial Product Marketing](https://finance.sina.cn/stock/jdts/2026-04-25/detail-inhvsuve3987870.d.html) ⭐️ 7.0/10

Eight Chinese government departments issued the 'Measures for the Administration of Online Marketing of Financial Products,' effective September 30, 2026, requiring payment tools to be displayed separately from loan products and banning misleading marketing language. This regulation directly impacts major credit payment products like Huabei, Baitiao, and Yuefu, potentially reshaping how fintech companies market and integrate financial services in e-commerce and daily payment scenarios. Non-bank payment institutions must no longer list loan products as payment options; checkout interfaces must prioritize payment tools. The rules also prohibit phrases like 'low threshold,' 'instant approval,' and 'low interest rate' in loan marketing.

telegram · zaihuapd · Apr 25, 10:03

**Background**: Huabei (Ant Group), Baitiao (JD Finance), and Yuefu (Meituan) are popular 'credit payment' products that allow users to pay later or in installments. Previously, these products were often displayed alongside payment tools like bank cards or Alipay balance, blurring the line between payment and credit. The new regulation aims to protect consumers by ensuring clear distinction and preventing misleading marketing.

<details><summary>References</summary>
<ul>
<li><a href="https://www.gov.cn/zhengce/zhengceku/202604/content_7066927.htm">金融产品网络营销管理办法_国务院部门文件_中国政府网</a></li>
<li><a href="https://www.news.cn/politics/20260424/615d283daaf54ceeb6f2a0c6a4f33b4c/c.html">金融产品网络营销管理办法 - 新华网</a></li>
<li><a href="https://www.pai.com.cn/p/01kq20v6n641978kfhhv08qh4g">网络金融新规出台： 花 呗 、 白 条 等将迎重大调整 - 电商派</a></li>

</ul>
</details>

**Discussion**: One commenter noted that Huabei can be forcibly closed by contacting Alipay customer service, after which it will no longer appear. This suggests some users prefer to opt out of such credit products.

**Tags**: `#fintech`, `#regulation`, `#China`, `#payments`, `#consumer finance`

---