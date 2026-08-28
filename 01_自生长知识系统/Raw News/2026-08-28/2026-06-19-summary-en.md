---
layout: default
title: "Horizon Summary: 2026-06-19 (EN)"
date: 2026-06-19
lang: en
---

> From 40 items, 6 important content pieces were selected

---

1. [Noam Shazeer, Transformer Co-Author, Leaves Google for OpenAI](#item-1) ⭐️ 9.0/10
2. [10K GitHub Repos Found Distributing Trojan Malware](#item-2) ⭐️ 8.0/10
3. [Hospitals and Universities Repurposing Drugs at Lower Cost](#item-3) ⭐️ 8.0/10
4. [Debunking Cancellation Claims for 2026 US Datacenter Capacity](#item-4) ⭐️ 8.0/10
5. [SFC Releases Best-Practice Recommendations for LLM AI in FOSS](#item-5) ⭐️ 8.0/10
6. [Apple and Intel Reach Preliminary Chip Foundry Deal](#item-6) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Noam Shazeer, Transformer Co-Author, Leaves Google for OpenAI](https://twitter.com/NoamShazeer/status/2067400851438932297) ⭐️ 9.0/10

Noam Shazeer, co-author of the seminal 'Attention Is All You Need' paper and former Gemini co-lead at Google, has announced he is leaving Google to join OpenAI. This move signals a significant talent shift in AI, as Shazeer was instrumental in creating the transformer architecture that underpins modern large language models. His expertise could accelerate OpenAI's efforts in next-generation AI models. Shazeer originally left Google in 2021 to co-found Character.AI, then returned in 2024 via a licensing and talent deal valued around $2.7 billion. His stint as Gemini co-lead lasted only a few months before this departure.

hackernews · lukasgross · Jun 18, 00:26 · [Discussion](https://news.ycombinator.com/item?id=48578913)

**Background**: The transformer architecture, introduced in the 2017 paper 'Attention Is All You Need,' revolutionized natural language processing by replacing recurrent and convolutional layers with attention mechanisms. It is the foundation for models like GPT, BERT, and Gemini. Shazeer was one of the eight co-authors of that paper and a key engineer at Google for over two decades.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/1706.03762">Abstract page for arXiv paper 1706.03762: Attention Is All You Need</a></li>
<li><a href="https://research.google/pubs/attention-is-all-you-need/">Attention is All You Need</a></li>

</ul>
</details>

**Discussion**: The community is highly engaged, with many providing context on Shazeer's career arc from Google to Character.AI and back. Some express surprise at his quick departure after returning, while others speculate about political or strategic reasons behind the move. Overall sentiment is that this is a major win for OpenAI.

**Tags**: `#AI`, `#transformers`, `#Noam Shazeer`, `#OpenAI`, `#Google`

---

<a id="item-2"></a>
## [10K GitHub Repos Found Distributing Trojan Malware](https://orchidfiles.com/github-repositories-distributing-malware/) ⭐️ 8.0/10

A security researcher discovered approximately 10,000 GitHub repositories that are actively distributing Trojan malware, exploiting the platform's trust to infect unsuspecting users. This discovery highlights a severe supply chain risk in open-source software, as malicious code can easily propagate through automated dependency managers and automated agents, potentially affecting countless downstream projects and users. The malicious repositories are often clones of popular projects with slight modifications, and they continually push new commits to appear at the top of search results or the 'Last Updated' list, targeting automated agents rather than humans.

hackernews · theorchid · Jun 18, 11:45 · [Discussion](https://news.ycombinator.com/item?id=48583928)

**Background**: GitHub is a widely used platform for hosting open-source code, and many software projects automatically pull dependencies from GitHub repositories. Attackers exploit this by creating fake repositories that mimic legitimate ones, embedding malware that gets executed during continuous integration or when developers clone the code.

**Discussion**: Community members shared similar experiences, with one user reporting their GitHub name being attached to unknown projects, and another detailing a case where a Disney engineer downloaded a malicious AI tool. Commenters noted that the repositories target automated agents, constantly updating to stay relevant, and linked to past incidents of such supply-chain attacks.

**Tags**: `#security`, `#malware`, `#github`, `#supply-chain`, `#open-source`

---

<a id="item-3"></a>
## [Hospitals and Universities Repurposing Drugs at Lower Cost](https://www.kcl.ac.uk/news/hospitals-and-universities-repurposing-drugs-at-90-lower-cost) ⭐️ 8.0/10

Hospitals and universities are repurposing existing drugs for new uses, dramatically lowering treatment costs. For example, using the cancer drug Avastin instead of Lucentis for macular degeneration cuts costs from $1,500 to $50 per dose. This approach challenges high drug prices and could make treatments more affordable, especially for rare diseases where pharmaceutical companies lack incentives. It also highlights systemic issues in healthcare pricing and regulation. Avastin (bevacizumab) and Lucentis (ranibizumab) share the same parent antibody, but Avastin costs roughly 30 times less per dose. However, Avastin is not packaged for intraocular use, requiring repackaging and off-label use.

hackernews · giuliomagnifico · Jun 18, 10:33 · [Discussion](https://news.ycombinator.com/item?id=48583386)

**Background**: Drug repurposing involves using an approved drug for a new medical indication, which can be faster and cheaper than developing a new drug. Many existing drugs have potential for new uses, but regulatory and commercial barriers often hinder adoption. For instance, Avastin is a VEGF inhibitor originally approved for cancer that also blocks abnormal blood vessel growth in the eye, the cause of wet macular degeneration.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Avastin">Avastin</a></li>
<li><a href="https://en.wikipedia.org/wiki/Lucentis">Lucentis</a></li>

</ul>
</details>

**Discussion**: Community comments praise repurposing efforts, providing concrete examples like Avastin for eye disease and esketamine controversy. Users highlight broken incentives in drug pricing and call for regulatory pathways to facilitate off-label use. Some note that repurposing can benefit rare diseases but faces manufacturer resistance.

**Tags**: `#drug repurposing`, `#healthcare costs`, `#pharmaceuticals`, `#innovation`

---

<a id="item-4"></a>
## [Debunking Cancellation Claims for 2026 US Datacenter Capacity](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter) ⭐️ 8.0/10

A new analysis by SemiAnalysis argues that claims of half of 2026 US datacenter capacity being canceled are greatly exaggerated, urging people to review individual filings rather than rely on vague estimates. This matters because inaccurate capacity cancellation estimates could misguide AI infrastructure investments and industry planning, potentially causing unnecessary market panic or policy miscalculations. The analysis emphasizes that estimates labeled as 'vibecoded'—a term for AI-generated code based on loose prompts—are unreliable, and instead advocates for examining each individual datacenter filing to assess true cancellation rates.

rss · Semianalysis · Jun 18, 15:54

**Background**: Recently, some reports suggested that nearly half of planned US datacenter capacity for 2026 had been canceled, sparking concerns about AI infrastructure oversupply. 'Vibe coding' is a software development practice where AI generates code based on a description; in this context, it refers to estimates that are similarly generated without rigorous verification. SemiAnalysis argues that such estimates are not grounded in detailed facts.

<details><summary>References</summary>
<ul>
<li><a href="https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter">Stop Saying Half of 2026 US Datacenter Capacity Is Canceled</a></li>
<li><a href="https://en.wikipedia.org/wiki/Vibe_coding">Vibe coding - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#datacenter`, `#infrastructure`, `#AI`, `#industry analysis`, `#capacity planning`

---

<a id="item-5"></a>
## [SFC Releases Best-Practice Recommendations for LLM AI in FOSS](https://lwn.net/Articles/1078521/) ⭐️ 8.0/10

The Software Freedom Conservancy (SFC) has announced the release of its best-practice recommendations for using LLM-backed generative AI systems in free and open source software (FOSS) contributions, created by the SFC and volunteers from the community. These recommendations provide practical guidance to FOSS contributors navigating the ethical and legal dilemmas posed by proprietary LLM-backed AI, helping to minimize damage to software freedom whether one chooses to use or reject these tools. The recommendations are explicitly framed as best practices rather than requirements, and SFC will follow up with supporting materials such as documents, tutorials, public Q&As, and podcasts to further assist the community.

rss · LWN.net · Jun 18, 16:00

**Background**: The Software Freedom Conservancy is a nonprofit organization that promotes software freedom and provides legal and administrative support to FOSS projects. LLM-backed generative AI systems, such as ChatGPT, raise concerns about licensing, attribution, and ethical use because they are often trained on and may generate code under uncertain legal terms.

**Tags**: `#open source`, `#LLM`, `#generative AI`, `#software freedom`, `#FOSS`

---

<a id="item-6"></a>
## [Apple and Intel Reach Preliminary Chip Foundry Deal](https://t.me/zaihuapd/42031) ⭐️ 8.0/10

Apple and Intel have signed a preliminary agreement for Intel to manufacture chips for some Apple devices, following over a year of negotiations and with strong encouragement from the U.S. government. This deal marks a major win for Intel's foundry business, securing a top-tier customer like Apple, and it reshapes the semiconductor supply chain by reducing Apple's reliance on TSMC. It also underscores growing U.S. government influence in chip manufacturing strategy. The specific Apple products (iPhone, iPad, or Mac) that will use Intel-manufactured chips remain unclear. With this deal, Intel now has foundry partnerships with Nvidia, SpaceX, and Apple.

telegram · zaihuapd · Jun 18, 09:19

**Background**: A chip foundry is a semiconductor fabrication plant (fab) that manufactures integrated circuits for other companies. In the foundry model, fabless companies like Apple design chips but outsource production to pure-play foundries like TSMC or increasingly to integrated device manufacturers (IDMs) like Intel that offer foundry services. The deal shifts some of Apple's production from TSMC to Intel, diversifying its supply chain.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chip_foundry">Chip foundry</a></li>

</ul>
</details>

**Tags**: `#Apple`, `#Intel`, `#chip manufacturing`, `#foundry`, `#semiconductor`

---