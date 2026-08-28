---
layout: default
title: "Horizon Summary: 2026-05-29 (EN)"
date: 2026-05-29
lang: en
---

> From 30 items, 9 important content pieces were selected

---

1. [Anthropic raises $65B in Series H at $965B valuation](#item-1) ⭐️ 10.0/10
2. [Linux kernel to replace struct page with memory descriptors](#item-2) ⭐️ 9.0/10
3. [NVIDIA pledges $150B annual investment in Taiwan as AI hub](#item-3) ⭐️ 9.0/10
4. [LLM Writing Smells Collection Sparks Debate](#item-4) ⭐️ 8.0/10
5. [Postgres as the Foundation for Durable Workflows](#item-5) ⭐️ 8.0/10
6. [IBM Launches $5B Project Lightwell for Open Source Security](#item-6) ⭐️ 8.0/10
7. [Nvidia Essentially Abandons Chinese AI Chip Market](#item-7) ⭐️ 8.0/10
8. [Qualcomm and ByteDance Partner on Custom AI ASICs](#item-8) ⭐️ 8.0/10
9. [BYD Unveils 4nm Autonomous Driving Chip 'Xuanji A3'](#item-9) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Anthropic raises $65B in Series H at $965B valuation](https://www.anthropic.com/news/series-h) ⭐️ 10.0/10

Anthropic announced a $65 billion Series H funding round at a $965 billion post-money valuation, surpassing OpenAI in both revenue and valuation. This marks a major shift in the AI industry, as Anthropic now leads over OpenAI, potentially reshaping competitive dynamics and investor confidence. Anthropic reported a run-rate revenue of $47 billion as of early May, up from $30 billion in February, and the Series H follows their Series G earlier this year.

hackernews · meetpateltech · May 28, 18:09 · [Discussion](https://news.ycombinator.com/item?id=48313048)

**Background**: Series H is a late-stage funding round, and post-money valuation includes the new capital. Run-rate revenue extrapolates recent revenue to estimate annual figures, showing rapid growth. Anthropic's ascent past OpenAI signals a changing landscape in generative AI.

**Discussion**: Comments discussed the distinction between run-rate and classic revenue, noted Anthropic surpassing OpenAI as a bigger headline, and coined the term 'kilocorn' for $1 trillion valuation.

**Tags**: `#Anthropic`, `#funding`, `#AI`, `#valuation`, `#OpenAI`

---

<a id="item-2"></a>
## [Linux kernel to replace struct page with memory descriptors](https://lwn.net/Articles/1073425/) ⭐️ 9.0/10

Vishal Moola presented the current state and future plans for replacing struct page with memory descriptors at the LSFMM+BPF 2026 summit. This fundamental change to Linux memory management reduces memory overhead and complexity, potentially improving performance and maintainability across the kernel. The memory descriptors are intended to be only 8 bytes, with types such as folio, slab, ptdesc, zsmalloc, and netmem. The transition involves a double-allocation cost and a proposed CONFIG_MEMDESC option, initially disabled by default.

rss · LWN.net · May 28, 13:09

**Background**: The struct page has been a core part of Linux memory management since 1995, but it has grown to 64 bytes and is cluttered with unions to support different page types, leading to inefficiencies. Memory descriptors aim to separate type-specific information, making the structure smaller and more maintainable by only storing a pointer to a type-specific descriptor.

<details><summary>References</summary>
<ul>
<li><a href="https://blogs.oracle.com/linux/introducing-memdesc">Introducing Memdesc | linux</a></li>
<li><a href="https://lwn.net/Articles/1015320/">The state of the page in 2025 [LWN.net]</a></li>
<li><a href="https://lore.kernel.org/linux-mm/5a55874d-80b9-b622-ec98-1bfdf3b251bf@redhat.com/T/">Dynamically allocated memory descriptors</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#memory management`, `#memory descriptors`, `#struct page`, `#LSFMM`

---

<a id="item-3"></a>
## [NVIDIA pledges $150B annual investment in Taiwan as AI hub](https://arstechnica.com/tech-policy/2026/05/nvidia-ceo-wants-taiwan-to-be-center-of-ai-revolution-not-us/) ⭐️ 9.0/10

NVIDIA CEO Jensen Huang announced plans to invest approximately $150 billion annually in Taiwan, calling it the center of the AI revolution. The investment covers AI chip production, system manufacturing, and supply chain partnerships with TSMC, Foxconn, and others. This unprecedented annual commitment signals a strategic shift for NVIDIA, cementing Taiwan as the core of AI hardware development. It could reshape global AI supply chains and intensify geopolitical discussions around semiconductor independence. The new Taipei headquarters is expected to break ground this year and open by 2030, housing 4,000 employees. Prior annual investments were in the range of $10-15 billion, making the $150 billion figure a tenfold increase.

telegram · zaihuapd · May 28, 07:33

**Background**: NVIDIA designs GPUs and AI accelerators that rely heavily on advanced semiconductor manufacturing, primarily by TSMC in Taiwan. Taiwan's ecosystem, including Foxconn, Wistron, and Quanta, provides critical assembly and supply chain services for NVIDIA's AI systems. The island has long been a focal point in global tech geopolitics due to its semiconductor dominance.

**Tags**: `#NVIDIA`, `#AI`, `#Taiwan`, `#semiconductors`, `#investment`

---

<a id="item-4"></a>
## [LLM Writing Smells Collection Sparks Debate](https://shvbsle.in/various-llm-smells/) ⭐️ 8.0/10

A blog post titled 'Various LLM Smells' catalogs recurring linguistic patterns that indicate LLM-generated text, such as phrases like 'the honest caveat:' and 'load bearing'. This resource helps readers identify and avoid the homogenized style of LLM output, preserving individuality in writing while still leveraging AI assistance. The article lists specific patterns like contrastive negation ('It’s not X, it’s Y') and overuse of 'The' in headings, as noted by commenters including Claude users.

hackernews · speckx · May 28, 19:02 · [Discussion](https://news.ycombinator.com/item?id=48313810)

**Background**: LLM 'smells' are analogous to code smells in software engineering — patterns that suggest the output was generated by a language model rather than a human. These linguistic tics arise from training data biases and model tendencies, making AI text detectable even without formal detectors.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2605.22976">LLM Code Smells: A Taxonomy and Detection Approach</a></li>

</ul>
</details>

**Discussion**: Commenters shared additional smells (e.g., 'blast radius' when not referring to explosives) and debated whether LLMs should be used directly or only for critique. Some argued that LLM sameness is beneficial in web design but detrimental to personal writing style.

**Tags**: `#LLM`, `#writing`, `#text generation`, `#AI detection`, `#style`

---

<a id="item-5"></a>
## [Postgres as the Foundation for Durable Workflows](https://www.dbos.dev/blog/postgres-is-all-you-need-for-durable-execution) ⭐️ 8.0/10

DBOS published a blog arguing that Postgres alone is sufficient for building durable workflow execution, proposing it as a simpler alternative to dedicated workflow engines like Temporal. This proposal could simplify system architectures by reducing dependencies, but raises questions about scalability and feature parity with mature platforms. Engineers evaluating workflow solutions must weigh the trade-offs between a database-centric approach and specialized services. DBOS relies on a paid component called Conductor for scaling and recovery, which some community members view as a limitation. Alternatives like Armin Ronacher's absurd and River also exist, each with their own trade-offs such as missing DLQ support in the free version of River.

hackernews · KraftyOne · May 28, 18:41 · [Discussion](https://news.ycombinator.com/item?id=48313530)

**Background**: Durable workflows ensure that long-running processes survive failures by persisting their state. Specialized workflow engines like Temporal provide these capabilities but introduce additional infrastructure complexity. The DBOS blog argues that Postgres, already widely used for data storage, can serve as the single source of truth for both data and workflow state, eliminating the need for a separate engine.

<details><summary>References</summary>
<ul>
<li><a href="https://temporal.io/">Durable Execution Solutions | Temporal</a></li>

</ul>
</details>

**Discussion**: Commenters pointed out DBOS's reliance on the paid Conductor component as a deal-breaker. Some shared their own lightweight implementations using Postgres and other backends, while others debated the trade-offs between DBOS, Temporal, absurd, and River, highlighting issues like payload size limits and missing features.

**Tags**: `#durable workflows`, `#Postgres`, `#database`, `#engineering`, `#temporal`

---

<a id="item-6"></a>
## [IBM Launches $5B Project Lightwell for Open Source Security](https://lwn.net/Articles/1075065/) ⭐️ 8.0/10

IBM and Red Hat announced Project Lightwell, a $5 billion initiative to create an AI-powered vulnerability clearinghouse for open source software, backed by over 20,000 engineers. This marks one of the largest corporate investments in open source security, potentially transforming how enterprises handle vulnerabilities at scale and strengthening supply chain security across the industry. The clearinghouse will use advanced AI to validate and test fixes, offered via commercial subscriptions for enterprise integration, while also sharing vulnerability information with upstream projects.

rss · LWN.net · May 28, 13:30

**Background**: Open source software relies on thousands of projects that often lack dedicated security resources. A vulnerability clearinghouse acts as a central hub to identify, verify, and distribute fixes, helping enterprises manage risks in their software supply chains efficiently.

<details><summary>References</summary>
<ul>
<li><a href="https://newsroom.ibm.com/2026-05-28-ibm-and-red-hat-commit-5-billion-to-redefine-the-future-of-open-source-in-the-ai-era">IBM and Red Hat Commit $5 Billion to Redefine the Future of Open Source in the AI Era</a></li>
<li><a href="https://www.redhat.com/en/about/press-releases/project-lightwell-secure-open-source">IBM and Red Hat Commit $5 Billion to Redefine the Future of Open Source in the AI Era</a></li>
<li><a href="https://linuxiac.com/ibm-and-red-hat-launch-5b-open-source-security-project/">IBM and Red Hat Launch $5B Open Source Security Project</a></li>

</ul>
</details>

**Tags**: `#open source security`, `#AI`, `#vulnerability management`, `#IBM`, `#Project Lightwell`

---

<a id="item-7"></a>
## [Nvidia Essentially Abandons Chinese AI Chip Market](https://t.me/zaihuapd/41609) ⭐️ 8.0/10

Nvidia CEO Jensen Huang stated that due to US export restrictions, the company has essentially given up on the Chinese AI chip market, ceding it to local competitors like Huawei. He advised investors not to expect any licenses to sell advanced chips to China. This marks a significant shift in the global AI chip landscape, with China becoming increasingly reliant on domestic suppliers like Huawei. It underscores the growing impact of US-China tech decoupling and could accelerate China's self-sufficiency in semiconductors. The Chinese market previously represented at least one-fifth of Nvidia's data center revenue. Nvidia is now focusing on expanding its supply chain and announced an $80 billion stock buyback program.

telegram · zaihuapd · May 28, 03:03

**Background**: US export controls, implemented by the Trump administration in April, require licenses for exporting advanced chips to China. These controls aim to restrict China's access to cutting-edge AI technology. Nvidia's GPUs are widely used for AI training and inference, and losing the Chinese market forces the company to redirect investments to other regions.

**Tags**: `#Nvidia`, `#AI chips`, `#export controls`, `#China`, `#semiconductor`

---

<a id="item-8"></a>
## [Qualcomm and ByteDance Partner on Custom AI ASICs](https://t.me/zaihuapd/41616) ⭐️ 8.0/10

Qualcomm has formed a partnership with ByteDance to produce custom AI ASICs, with ByteDance ordering millions of chips for AI inference workloads. This deal positions Qualcomm as a key supplier in the custom AI chip market and provides ByteDance with high-volume, optimized hardware to power its AI services, potentially shifting the competitive landscape for AI inference hardware. ByteDance will also leverage Qualcomm's manufacturing expertise to convert its internal chip designs into mass-produced semiconductors. This follows Qualcomm's earlier announcement in late April to deliver its first ASIC to a hyperscale cloud provider.

telegram · zaihuapd · May 28, 07:09

**Background**: An application-specific integrated circuit (ASIC) is a chip customized for a particular use, offering higher efficiency than general-purpose CPUs or GPUs for specific tasks like AI inference. AI inference workloads refer to the computational resources needed when a pre-trained model processes new data to make predictions. Hyperscalers like ByteDance increasingly adopt custom ASICs to optimize performance and reduce costs for large-scale AI services.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ASIC">ASIC</a></li>
<li><a href="https://www.naddod.com/ai-insights/what-are-ai-inference-workloads-why-ai-inference-workloads-are-growing-rapidly">Introduction of AI Inference Workloads - NADDOD Blog</a></li>

</ul>
</details>

**Tags**: `#AI chips`, `#Qualcomm`, `#ByteDance`, `#ASIC`, `#hardware`

---

<a id="item-9"></a>
## [BYD Unveils 4nm Autonomous Driving Chip 'Xuanji A3'](https://finance.sina.com.cn/roll/2026-05-28/doc-inhznenn1371824.shtml) ⭐️ 8.0/10

On May 28, BYD announced the mass production of its self-developed 4nm autonomous driving chip, Xuanji A3, which supports L3 and L4 autonomous driving. Three chips together deliver over 2100 TOPS of computing power. This marks a significant move by a major automaker to vertically integrate chip design for autonomous driving, potentially reducing reliance on external suppliers. The high TOPS and 4nm process indicate competitiveness with leading AI chips. BYD claims that the chip, combined with proprietary algorithm optimization, doubles computing power utilization. The company also noted it has developed over 2000 chip products and operates five wafer fabrication plants.

telegram · zaihuapd · May 28, 13:01

**Background**: Autonomous driving chips are specialized processors designed to handle the massive sensor data and real-time decision-making required for self-driving cars. The shift to 4nm node—a leading semiconductor manufacturing process—enables higher performance and energy efficiency. BYD's move into chip production is part of a broader trend of automakers building in-house silicon.

**Discussion**: No community comments available.

**Tags**: `#autonomous driving`, `#BYD`, `#4nm chip`, `#automotive`, `#AI`

---