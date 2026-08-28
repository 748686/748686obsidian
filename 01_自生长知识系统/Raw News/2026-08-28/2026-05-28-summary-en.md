---
layout: default
title: "Horizon Summary: 2026-05-28 (EN)"
date: 2026-05-28
lang: en
---

> From 39 items, 11 important content pieces were selected

---

1. [Critical 7-Zip Heap Overflow Allows Arbitrary Code Execution](#item-1) ⭐️ 9.0/10
2. [Anthropic and OpenAI Achieve Product-Market Fit, Argues Simon Willison](#item-2) ⭐️ 8.0/10
3. [Canada to buy Swedish GlobalEye planes, shifting from US suppliers](#item-3) ⭐️ 8.0/10
4. [GitHub Major Outage Disrupts Core Development Workflows](#item-4) ⭐️ 8.0/10
5. [Go to Support Generic Methods](#item-5) ⭐️ 8.0/10
6. [SQLite Adds AGENTS.md to Define AI Contribution Policy](#item-6) ⭐️ 8.0/10
7. [MOT Tool Fights Openwashing in AI Models](#item-7) ⭐️ 8.0/10
8. [LWN Rescues Andrew Morton's 2004 OLS Keynote](#item-8) ⭐️ 8.0/10
9. [Progress on removing Linux page mapcount field](#item-9) ⭐️ 8.0/10
10. [Huawei Proposes Tau Scaling Law for Semiconductor Advance](#item-10) ⭐️ 8.0/10
11. [CXMT Gets STAR Market IPO Approval, Plans to Raise 29.5B Yuan](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Critical 7-Zip Heap Overflow Allows Arbitrary Code Execution](https://socprime.com/blog/cve-2026-48095-7-zip-heap-overflow-flaw/) ⭐️ 9.0/10

A critical heap buffer overflow vulnerability (CVE-2026-48095) has been disclosed in 7-Zip version 26.00, affecting the NTFS archive handler. The flaw allows attackers to execute arbitrary code or cause application crashes by tricking users into opening a specially crafted archive file. 7-Zip is one of the most widely used file archivers globally, and this vulnerability exposes millions of users to remote code execution risks. The signature-based fallback logic in 7-Zip expands the attack surface, as malicious files with common extensions like .7z, .zip, or .rar can be rerouted to the vulnerable NTFS handler. The vulnerability is a heap buffer write overflow triggered by an under-allocation in the NTFS compressed stream buffer (GetCuSize shift UB), enabling vtable hijack for arbitrary code execution. The issue was fixed in 7-Zip version 26.01 released on April 27, 2026.

telegram · zaihuapd · May 27, 08:01

**Background**: 7-Zip is a free, open-source file archiver widely used for compressing and decompressing files. The NTFS archive handler is a module that processes NTFS volumes embedded within archives. A heap buffer overflow occurs when a program writes more data to a heap memory buffer than it can hold, potentially leading to code execution. The signature-based fallback logic allows 7-Zip to try different handlers based on file signatures, but it inadvertently routes crafted files to the vulnerable NTFS handler even when the file extension suggests a different format.

<details><summary>References</summary>
<ul>
<li><a href="https://cybersecuritynews.com/7-zip-vulnerabilities-code-execution/">New 7-Zip Vulnerabilities Let Attackers Execute Arbitrary ...</a></li>
<li><a href="https://thecybersecguru.com/exploits/cve-2026-48095-7-zip-heap-buffer-overflow/">CVE-2026-48095: 7-Zip Heap Buffer Overflow Vulnerability ...</a></li>
<li><a href="https://securitylab.github.com/advisories/GHSL-2026-140_7-Zip/">GHSL-2026-140: Heap Buffer Write Overflow in 7-Zip</a></li>

</ul>
</details>

**Tags**: `#安全漏洞`, `#7-Zip`, `#CVE-2026-48095`, `#任意代码执行`, `#压缩软件`

---

<a id="item-2"></a>
## [Anthropic and OpenAI Achieve Product-Market Fit, Argues Simon Willison](https://simonwillison.net/2026/May/27/product-market-fit/#atom-everything) ⭐️ 8.0/10

Simon Willison argues that Anthropic and OpenAI have found product-market fit, based on rumors of Anthropic's first profitable quarter and enterprise customers paying API prices for coding agents like Claude Code and OpenAI Codex. This signals a shift from free or subsidized AI usage to sustainable revenue models, with enterprise spending on LLMs potentially reaching trillions, impacting how companies budget for AI tools. Anthropic's Enterprise plan reportedly switched to $20/seat/month plus API pricing in November 2025, and OpenAI made a similar change for Codex in April 2026. Willison estimated he would have spent $2,180 on API tokens in 30 days vs. his $200 subscription.

rss · Simon Willison · May 27, 16:38 · [Discussion](https://news.ycombinator.com/item?id=48296794)

**Background**: Product-market fit refers to a product meeting strong market demand, leading to profitability. LLM companies have invested heavily in compute and infrastructure, and recent pricing changes for enterprise seats indicate they are monetizing usage. Similar moves by OpenAI and Anthropic suggest they are consolidating their market position.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>
<li><a href="https://claude.com/product/claude-code">Claude Code by Anthropic | AI Coding Agent, Terminal, IDE</a></li>

</ul>
</details>

**Discussion**: Commenters expressed mixed views: some questioned the distinction between product-market fit and profitability, while others raised concerns about high costs and potential astroturfing. One commenter noted that open-source models like GLM-5.1 could undercut pricing, challenging the business model.

**Tags**: `#AI industry`, `#product-market fit`, `#LLMs`, `#enterprise AI`, `#market analysis`

---

<a id="item-3"></a>
## [Canada to buy Swedish GlobalEye planes, shifting from US suppliers](https://www.theguardian.com/world/2026/may/27/canada-sweden-saab-globaleye-aircraft) ⭐️ 8.0/10

Canada has announced plans to purchase Saab GlobalEye surveillance aircraft from Sweden, marking a shift away from traditional US defense suppliers due to production backlogs and geopolitical tensions. This decision signals a broader trend among US allies to diversify defense procurement, potentially reducing US dominance in the defense industry and boosting European competitors like Saab. The GlobalEye is built on the Bombardier Global 6000/6500 business jet, which is manufactured in Canada, and features the Erieye ER radar system with S-band technology for jamming resistance.

hackernews · tosh · May 27, 16:53 · [Discussion](https://news.ycombinator.com/item?id=48296994)

**Background**: The Saab GlobalEye is a multi-domain airborne early warning and control (AEW&C) platform that entered service in 2020. It combines active and passive sensors for long-range detection of air, sea, and land targets, and has been operational in conflicts such as in Ukraine.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GlobalEye">GlobalEye - Wikipedia</a></li>
<li><a href="https://www.saab.com/products/globaleye">GlobalEye AEW&C | Saab</a></li>
<li><a href="https://thedefensepost.com/2025/12/05/globaleye-saab-guide/">A Quick Guide Into Saab’s GlobalEye Surveillance Plane</a></li>

</ul>
</details>

**Discussion**: Commenters noted that the US lacks a direct comparable aircraft, making this a practical procurement rather than purely political. Some linked the shift to US threats against allies, while others highlighted the Canadian production base and prior commitments to Sweden.

**Tags**: `#geopolitics`, `#defense`, `#procurement`, `#Canada`, `#Sweden`

---

<a id="item-4"></a>
## [GitHub Major Outage Disrupts Core Development Workflows](https://www.githubstatus.com/incidents/xy1tt3hs572m) ⭐️ 8.0/10

GitHub suffered a significant incident on an unspecified date, impacting pull requests, issues, git operations, and API requests, with users reporting that recent outages have been frequent. This outage disrupts critical development workflows for millions of developers, raising concerns about GitHub's reliability as a central platform for software collaboration. The incident specifically affected pull requests on both web UI and API, which were not reflecting all commits or branch changes consistently, increasing the risk of merging incomplete code.

hackernews · maxnoe · May 27, 12:15 · [Discussion](https://news.ycombinator.com/item?id=48293080)

**Background**: GitHub is a widely-used platform for version control and collaboration, hosting millions of repositories. Frequent outages can severely impact developer productivity and trust. The recent pattern of incidents has led to community frustration.

**Discussion**: Community comments express frustration with the recurring outages, with one user noting that pull request diffs were inconsistent, making it easy to merge without full review. Another user compared reliability issues to other services like Supabase and Cloudflare since AI coding became common.

**Tags**: `#GitHub`, `#incident`, `#outage`, `#reliability`, `#developer tools`

---

<a id="item-5"></a>
## [Go to Support Generic Methods](https://github.com/golang/go/issues/77273) ⭐️ 8.0/10

The Go team is implementing support for generic methods, allowing methods on types to have their own type parameters, as proposed in GitHub issue #77273. This feature fills a major gap in Go's generics, enabling more expressive and reusable code, particularly for design patterns like monads or data access layers. The implementation is incremental; generic methods were initially deferred from the original generics proposal as a "not now" item, but the team is now moving forward with careful design.

hackernews · f311a · May 27, 09:02 · [Discussion](https://news.ycombinator.com/item?id=48291575)

**Background**: Go introduced generics in version 1.18, allowing functions and types to have type parameters. However, methods on generic types could not define additional type parameters, limiting certain patterns. This proposal addresses that limitation, bringing Go closer to the flexibility of languages like Java or C#.

<details><summary>References</summary>
<ul>
<li><a href="https://stackoverflow.com/questions/77546447/go-how-to-specify-a-type-constraint-in-which-a-methods-argument-type-is-the-sa">generics - Go: How to specify a type constraint in which a</a></li>
<li><a href="https://stackoverflow.com/questions/70668236/how-to-create-generic-method-in-go-method-must-have-no-type-parameters">How to create generic method in Go? (method must have no type</a></li>

</ul>
</details>

**Discussion**: Community comments are overwhelmingly positive, with users expressing excitement about potential patterns like monad libraries and noting that this feature resolves a significant gap for those coming from other languages.

**Tags**: `#Go`, `#generics`, `#programming languages`, `#type parameters`

---

<a id="item-6"></a>
## [SQLite Adds AGENTS.md to Define AI Contribution Policy](https://simonwillison.net/2026/May/27/sqlite-agents/#atom-everything) ⭐️ 8.0/10

SQLite has added an AGENTS.md file that explicitly states the project does not accept agentic code (code written autonomously by AI agents), but welcomes agentic bug reports with reproducible test cases and documentation-oriented patches. Additionally, the SQLite forum has been split to create a dedicated Bug Forum for AI-generated bug reports due to a flood of such submissions. This policy sets a precedent for how critical open-source projects can balance the benefits of AI assistance with the need to maintain code quality and legal clarity. It will influence other projects grappling with AI-generated contributions, and highlights the challenge of differentiating human-written and agentic work in open-source ecosystems. The AGENTS.md file was committed five days ago, and a subsequent commit removed the word '(currently)' to strengthen the rejection of agentic code. SQLite does not accept pull requests without prior agreement and legal paperwork placing them in the public domain, though human developers may review concise pull requests as proof-of-concept before reimplementing.

rss · Simon Willison · May 27, 23:44

**Background**: AGENTS.md is a file that projects can use to specify policies for AI coding agents, analogous to README.md for human contributors. 'Agentic code' refers to code autonomously generated by AI agents that plan, write, test, and deploy code end-to-end. SQLite is a widely-used embedded SQL database known for its strict quality standards and conservative contribution model, typically requiring contributors to sign legal documents. The project's creator, D. Richard Hipp, has been actively fixing issues on the new Bug Forum.

<details><summary>References</summary>
<ul>
<li><a href="https://agents.md/">AGENTS . md</a></li>
<li><a href="https://tms-outsource.com/blog/posts/what-is-agentic-coding/">What Is Agentic Coding ? The Next AI Dev Workflow</a></li>

</ul>
</details>

**Tags**: `#sqlite`, `#AI agents`, `#open source`, `#contribution policies`, `#software engineering`

---

<a id="item-7"></a>
## [MOT Tool Fights Openwashing in AI Models](https://lwn.net/Articles/1073420/) ⭐️ 8.0/10

Arnaud Le Hors introduced the Model Openness Tool (MOT) at Open Source Summit North America 2026 to evaluate the true openness of large language models. The tool helps users identify openwashing, where models are marketed as open source but fail to meet standard openness criteria, promoting transparency and informed decision-making. MOT is based on the Model Openness Framework (MOF) and evaluates models against specific criteria like license, data, and training code availability.

rss · LWN.net · May 27, 15:52

**Background**: Many AI models described as open source are actually 'open weight' or have restrictive licenses, a practice called openwashing. The Open Source Initiative (OSI) has a strict definition of open source, but many models do not comply.

<details><summary>References</summary>
<ul>
<li><a href="https://mot.isitopen.ai/">Models | Model Openness Tool</a></li>
<li><a href="https://github.com/lfai/model_openness_tool">GitHub - lfai/ model _ openness _ tool : Model Openness Tool</a></li>

</ul>
</details>

**Tags**: `#open source`, `#AI`, `#openwashing`, `#large language models`, `#transparency`

---

<a id="item-8"></a>
## [LWN Rescues Andrew Morton's 2004 OLS Keynote](https://lwn.net/Articles/1070746/) ⭐️ 8.0/10

LWN.net has published a rescued transcript of Andrew Morton's keynote at the 2004 Ottawa Linux Symposium, which had been replaced by crypto spam on Groklaw. This transcript preserves a historically significant speech that documents a pivotal change in the Linux kernel development model, offering invaluable insight into the project's evolution. The transcript was recovered via the Wayback Machine after the original Groklaw page was overrun with crypto spam, and none of the original links remain functional.

rss · LWN.net · May 27, 14:35

**Background**: Groklaw was a legal blog founded by paralegal Pamela Jones in 2003 to cover the SCO–Linux litigation. The Ottawa Linux Symposium (OLS) was a premier technical conference for Linux kernel developers. Andrew Morton's 2004 keynote followed a Kernel Summit session that decided to fundamentally change the kernel's development model, moving toward a more inclusive process.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Groklaw">Groklaw - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Linux_Symposium">Linux Symposium - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#linux`, `#kernel development`, `#history`, `#open source`, `#preservation`

---

<a id="item-9"></a>
## [Progress on removing Linux page mapcount field](https://lwn.net/Articles/1073418/) ⭐️ 8.0/10

David Hildenbrand reported nearing completion of removing the expensive 'mapcount' field from Linux's struct page at the 2026 LSFMM+BPF Summit, with a new patch set that introduces a 'folio->_total_pages_mapped' field. This change reduces kernel memory management overhead, simplifies code, and enables better support for large folios, potentially improving performance and maintainability for the entire Linux kernel. The new 'NO_PAGE_MAPCOUNT' config option (since 6.15) is still experimental; the latest patch set also adds support for mapping large folios as arbitrary combinations of page sizes, but makes some accounting statistics imprecise.

rss · LWN.net · May 27, 13:16

**Background**: The mapcount field in struct page tracks how many page-table entries reference a given page, and a zero mapcount indicates the page can be reclaimed. Maintaining this field has become increasingly complex and expensive as memory management evolves, motivating efforts to eliminate it.

<details><summary>References</summary>
<ul>
<li><a href="https://blogs.oracle.com/linux/struct-page-the-linux-physical-page-frame-data-structure">struct page, the Linux physical page frame data structure | linux</a></li>
<li><a href="https://lwn.net/Articles/1013649/">Looking forward to mapcount madness 2025 [LWN.net]</a></li>
<li><a href="https://events.linuxfoundation.org/lsfmmbpf/">Linux Storage, Filesystem, MM & BPF Summit | LF Events</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#memory management`, `#struct page`, `#mapcount`, `#LSFMM+BPF`

---

<a id="item-10"></a>
## [Huawei Proposes Tau Scaling Law for Semiconductor Advance](https://t.me/zaihuapd/41597) ⭐️ 8.0/10

At the 2026 IEEE International Symposium on Circuits and Systems in Shanghai, Huawei officially introduced the Tau (τ) Scaling Law, advocating for time scaling instead of traditional geometric scaling. The company claims to have designed and mass-produced 381 chips under this principle and plans to launch a new Kirin smartphone chip this autumn featuring logic folding technology. This could represent a paradigm shift in semiconductor scaling, potentially extending performance gains beyond Moore's Law's physical limits. If validated, it may offer an alternative path for chip advancement, especially for companies facing restrictions on advanced manufacturing equipment. The Tau Scaling Law reduces the time constant (τ) to achieve multi-level co-optimization from devices to systems. Huawei targets transistor density equivalent to 1.4nm process by 2031 using this approach, and the upcoming Kirin chip will be the first to fully implement logic folding technology.

telegram · zaihuapd · May 27, 09:00

**Background**: Moore's Law, which predicted transistor density doubling every two years, is slowing as geometric scaling approaches physical atomic limits. The semiconductor industry has been exploring alternative scaling methods, such as advanced packaging and new materials. Huawei's Tau Scaling Law proposes time-domain optimization as a new dimension, leveraging faster switching and reduced latency rather than shrinking transistor dimensions.

<details><summary>References</summary>
<ul>
<li><a href="https://www.huawei.com/en/news/2026/5/ieee-iscas-tau-scaling">HUAWEI Presents the Tau (τ) Scaling Law, Enabling ...</a></li>
<li><a href="https://www.trendforce.com/news/2026/05/26/news-huawei-unveils-new-semiconductor-principle-tau-τ-scaling-law/">[News] Huawei Unveils New Semiconductor Principle – Tau (τ ...</a></li>
<li><a href="https://www.guru3d.com/story/huawei-targets-14nmequivalent-chip-density-without-advanced-euv-tools/">Huawei Targets 1.4nm-Equivalent Chip Density Without Advanced</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#Moore's Law`, `#Huawei`, `#chip design`, `#innovation`

---

<a id="item-11"></a>
## [CXMT Gets STAR Market IPO Approval, Plans to Raise 29.5B Yuan](https://static.sse.com.cn/stock/disclosure/announcement/c/202605/000001_20260527_SPLE.pdf) ⭐️ 8.0/10

ChangXin Memory Technologies (CXMT) received approval from the Shanghai Stock Exchange for its IPO on the STAR Market, planning to raise 29.5 billion yuan to fund DRAM technology upgrades and wafer fabrication expansion. This IPO marks a milestone for China's domestic memory chip industry, as CXMT is a leading DRAM manufacturer and the funds will bolster its competitiveness against global players like Samsung and SK Hynix, supporting national semiconductor self-sufficiency goals. The proposed 29.5 billion yuan offering would be the second-largest IPO on the STAR Market since its inception, with proceeds allocated to memory wafer manufacturing, DRAM technology upgrades, and forward-looking R&D projects.

telegram · zaihuapd · May 27, 09:12

**Background**: DRAM (Dynamic Random Access Memory) is a type of volatile memory widely used in computers, servers, and mobile devices. The STAR Market is China's Nasdaq-style board for tech companies with relaxed listing requirements. CXMT, founded in 2016 and based in Hefei, is the country's primary DRAM producer, having achieved mass production of DDR4 and LPDDR4 chips.

<details><summary>References</summary>
<ul>
<li><a href="https://baike.baidu.com/item/长鑫科技集团股份有限公司/64261783">长鑫科技集团股份有限公司_百度百科</a></li>
<li><a href="https://finance.eastmoney.com/a/202605183739821249.html">日赚近4亿！存储龙头长鑫科技IPO有新进展 核心受益股一览</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#DRAM`, `#IPO`, `#China`, `#memory`

---