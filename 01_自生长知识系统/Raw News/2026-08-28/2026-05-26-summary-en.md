---
layout: default
title: "Horizon Summary: 2026-05-26 (EN)"
date: 2026-05-26
lang: en
---

> From 28 items, 9 important content pieces were selected

---

1. [Pope Leo XIV Issues Encyclical on AI Ethics](#item-1) ⭐️ 9.0/10
2. [Using AI to write better code more slowly](#item-2) ⭐️ 8.0/10
3. [Mullvad Rolls Out Mitigation for VPN Exit IP Fingerprinting](#item-3) ⭐️ 8.0/10
4. [California Proposes Exempting Linux from Age-Verification Law](#item-4) ⭐️ 8.0/10
5. [LLM-based kernel patch review debated at LSFMM+BPF](#item-5) ⭐️ 8.0/10
6. [SFC Responds to Bambu's AGPLv3 Violations](#item-6) ⭐️ 8.0/10
7. [Semi-Alive Human Brains Used for Drug Testing](#item-7) ⭐️ 8.0/10
8. [EU Preliminary Investigation Finds Google Violated DMA](#item-8) ⭐️ 8.0/10
9. [Musk: xAI to Open-Source 0.5T Parameter Model by End of 2026](#item-9) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Pope Leo XIV Issues Encyclical on AI Ethics](https://simonwillison.net/2026/May/25/encyclical-on-ai/#atom-everything) ⭐️ 9.0/10

The Vatican released an encyclical titled 'Magnifica Humanitas' by Pope Leo XIV, specifically addressing ethical safeguards for humanity in the age of artificial intelligence. The document is praised for its exceptional clarity and depth. This is the first papal encyclical dedicated solely to AI, signaling the Catholic Church's engagement with modern technology ethics. It offers accessible ethical guidance that could influence global discussions on AI regulation and human dignity. The encyclical highlights the interpretability problem of large language models, describing AI systems as more 'cultivated' than 'built'. It also emphasizes that true development must place people at the center, not wealth accumulation.

rss · Simon Willison · May 25, 23:58

**Background**: A papal encyclical is a formal letter from the Pope addressing important issues. Pope Leo XIV chose his name in honor of Pope Leo XIII, who addressed industrial revolution labor issues in 'Rerum Novarum'. This encyclical updates that social teaching for the AI era.

**Tags**: `#AI ethics`, `#Vatican`, `#papal encyclical`, `#technology ethics`, `#society`

---

<a id="item-2"></a>
## [Using AI to write better code more slowly](https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/) ⭐️ 8.0/10

Nolan Lawson's blog post argues that a deliberate, iterative approach to AI-assisted coding can produce higher quality code than the typical focus on speed, challenging the dominant narrative of AI coding tools. This perspective is significant because it encourages developers to rethink how they use AI in their workflows, potentially leading to better code quality and more sustainable practices in software engineering. The author describes a workflow involving multiple AI models for design, implementation, and review, emphasizing iteration and thoroughness over raw speed, and notes that tools like Claude and Codex can be used in a chain to catch corner cases.

hackernews · signa11 · May 25, 23:16 · [Discussion](https://news.ycombinator.com/item?id=48272984)

**Background**: AI coding assistants, such as ChatGPT, Claude, and GitHub Copilot, have become popular for generating code quickly, but the quality of the output can vary significantly. This article proposes a slower, more deliberate process that leverages AI for design and review alongside human oversight.

**Discussion**: Comments reveal mixed experiences: some find that AI-assisted workflows become long back-and-forth processes that can exceed manual coding time, while others see value in using multiple LLMs for different stages (design, implementation, review) and believe AI can produce high-quality code when used deliberately. A few commenters express AI skepticism on ethical grounds but find code review use cases less problematic.

**Tags**: `#AI`, `#coding`, `#software engineering`, `#productivity`, `#code quality`

---

<a id="item-3"></a>
## [Mullvad Rolls Out Mitigation for VPN Exit IP Fingerprinting](https://mullvad.net/en/help/exit-ip-vpn-servers-mitigation-rollout) ⭐️ 8.0/10

Mullvad VPN has announced the rollout of mitigation measures to prevent exit IP fingerprinting, a technique that could identify users through their VPN server's unique IP address. This is significant because exit IP fingerprinting undermines VPN privacy by allowing websites to correlate users across sessions. Mullvad's proactive response sets a positive example for the VPN industry. The mitigation involves changes to exit server configurations to reduce uniqueness. Users may experience minor performance changes but no action is required.

hackernews · Cider9986 · May 25, 17:45 · [Discussion](https://news.ycombinator.com/item?id=48269580)

**Background**: VPN exit IP fingerprinting is a privacy attack where a website identifies a user's VPN provider and specific server based on the exit IP address. This can be used to track users across different sites or sessions. Mullvad had previously published research on this vulnerability.

<details><summary>References</summary>
<ul>
<li><a href="https://discuss.privacyguides.net/t/mullvad-exit-ips-as-a-fingerprinting-vector/37910">Mullvad exit IPs as a fingerprinting vector - General - Privacy</a></li>
<li><a href="https://tmctmt.com/posts/mullvad-exit-ips-as-a-fingerprinting-vector/">Mullvad exit IPs as a fingerprinting vector | tmctmt</a></li>
<li><a href="https://cacm.acm.org/research/openvpn-is-open-to-vpn-fingerprinting/">OpenVPN Is Open to VPN Fingerprinting – Communications of the ACM</a></li>

</ul>
</details>

**Discussion**: Users expressed surprise and appreciation for the quick response, with some suggesting further improvements like browser integration of anti-fingerprinting features. One commenter noted that Mullvad Browser already avoids this issue by using proxies instead of WireGuard.

**Tags**: `#privacy`, `#VPN`, `#fingerprinting`, `#security`, `#Mullvad`

---

<a id="item-4"></a>
## [California Proposes Exempting Linux from Age-Verification Law](https://www.tomshardware.com/software/linux/california-moves-to-exempt-linux-from-its-upcoming-age-verification-law-after-backlash-over-forcing-operating-systems-to-collect-users-ages-amendment-proposed-by-the-same-lawmaker-who-wrote-the-original-law) ⭐️ 8.0/10

California has proposed an amendment to its age-verification law to explicitly exempt Linux operating systems after backlash over requiring them to collect user ages. This move prevents a potential disaster for Linux adoption and open source software, as the original law would have placed an impossible burden on operating systems that lack centralized user accounts. The amendment was proposed by the same lawmaker who wrote the original law, indicating a recognition of the unintended consequences. The exemption specifically covers operating systems that are not primarily used for accessing commercial content.

hackernews · rbanffy · May 25, 18:19 · [Discussion](https://news.ycombinator.com/item?id=48269961)

**Background**: California's age-verification law, aimed at protecting minors online, originally required all operating systems to verify user ages. This sparked backlash from the Linux and open source communities, as Linux distributions often don't have centralized user accounts or the ability to easily verify ages. The proposed amendment exempts operating systems that are not primarily used for commercial content access.

**Discussion**: Community comments expressed skepticism about the law's necessity and highlighted the impracticality of applying age verification to open source systems. Some commenters criticized the legislative process for not consulting relevant experts, while others noted that the law would burden consumers rather than regulate companies effectively.

**Tags**: `#Linux`, `#California`, `#age-verification`, `#internet regulation`, `#open source`

---

<a id="item-5"></a>
## [LLM-based kernel patch review debated at LSFMM+BPF](https://lwn.net/Articles/1073583/) ⭐️ 8.0/10

At the 2026 Linux Storage, Filesystem, Memory Management & BPF Summit, a plenary session led by Roman Gushchin and others discussed using large language models (LLMs) for Linux kernel patch review, with a focus on the Sashiko tool. This discussion signals growing interest in AI-assisted code review for the Linux kernel, potentially easing the workload on human maintainers and improving patch quality, especially for first-time contributors. Sashiko achieved a 10% false-positive rate and 85% true-positive rate across 1500 analyzed email threads, with critical and high-severity accuracy near 97%. The tool has been mentioned in 140 kernel commit messages since its mid-March launch.

rss · LWN.net · May 25, 21:27

**Background**: The Linux kernel development process relies heavily on human reviewers to evaluate patches. Large language models are probabilistic AI systems that can analyze code and provide review comments. Sashiko is a tool designed to automatically review kernel patches, sitting between static analysis and human review.

<details><summary>References</summary>
<ul>
<li><a href="https://events.linuxfoundation.org/lsfmmbpf/">Linux Storage, Filesystem, MM & BPF Summit | LF Events</a></li>
<li><a href="https://ebpf.foundation/event/linux-storage-filesystem-memory-management-bpf-summit/">Linux Storage, Filesystem, Memory Management & BPF Summit</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#Linux kernel`, `#patch review`, `#AI-assisted development`

---

<a id="item-6"></a>
## [SFC Responds to Bambu's AGPLv3 Violations](https://lwn.net/Articles/1074286/) ⭐️ 8.0/10

The Software Freedom Conservancy (SFC) published a response on May 18 detailing Bambu Lab's violations of the AGPLv3 license, including failure to provide source code for modifications to a GPL-licensed slicer and threatening a fork creator. SFC launched the baltobu reverse-engineering project and is hosting a compliant fork of Orca Slicer. This action highlights the enforcement of open-source licenses in the 3D printing industry, protecting developer rights and user freedoms. It sets a precedent for holding commercial entities accountable for AGPLv3 compliance, especially in the right-to-repair context. Bambu Lab has made false public statements about AGPLv3 requirements and threatened Paweł Jarczak, who created a fork of Orca Slicer to interoperate with Bambu printers. SFC's baltobu project aims to reverse-engineer Bambu's proprietary code to ensure compliance and support consumers.

rss · LWN.net · May 25, 16:48

**Background**: The AGPLv3 is a strong copyleft license requiring that modified versions of the software, when used over a network, must have their source code made available to users. A 3D printer slicer converts 3D models into printer instructions (G-code). Orca Slicer is an open-source slicer derived from Bambu Studio, itself based on AGPLv3-licensed code.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GNU_Affero_General_Public_License">GNU Affero General Public License - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Slicer_(3D_printing)">Slicer (3D printing) - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#open source`, `#AGPLv3`, `#license enforcement`, `#3D printing`, `#software freedom`

---

<a id="item-7"></a>
## [Semi-Alive Human Brains Used for Drug Testing](https://www.science.org/content/article/not-alive-not-dead-disembodied-human-brains-used-drug-testing) ⭐️ 8.0/10

A study using the BrainEx perfusion system has restored partial metabolic and cellular activity in human brains hours after death, enabling drug testing for neurological diseases like Alzheimer's and Parkinson's. This breakthrough challenges the traditional definition of death and raises profound ethical questions about consciousness and human dignity, while potentially revolutionizing neurological drug development by providing a more accurate human model than animal tests. The brains, obtained from donors, did not regain consciousness or full neural activity; the technology is developed by Bexorg, a U.S. biotech company. The study has sparked debate over informed consent for organ donation and the boundaries of life-sustaining technology.

telegram · zaihuapd · May 25, 14:57

**Background**: The BrainEx system is a perfusion technology that delivers oxygen and nutrients to brain tissue post-mortem, maintaining cellular integrity. Traditionally, brain death is considered irreversible, but this system can partially revive cellular functions without consciousness. This work builds on earlier animal studies but is the first reported use with human brains for drug testing.

**Tags**: `#neuroscience`, `#bioethics`, `#drug testing`, `#brain research`, `#ethics`

---

<a id="item-8"></a>
## [EU Preliminary Investigation Finds Google Violated DMA](https://t.me/zaihuapd/41566) ⭐️ 8.0/10

The European Commission preliminarily found that Alphabet (Google) violated the Digital Markets Act (DMA) through self-preferencing in search results and by restricting app developers in the Play Store. This is a major enforcement action under the DMA, signaling that the EU is serious about curbing Big Tech anti-competitive practices and could lead to significant fines or forced changes to Google's business model in Europe. Specifically, Google's search results allegedly favor its own shopping, flights, and hotel services, while the Play Store restricts developers from directing users to alternative payment or distribution channels. The Commission deemed Google's compliance measures insufficient.

telegram · zaihuapd · May 26, 00:27

**Background**: The Digital Markets Act (DMA) is an EU regulation that designates large online platforms as 'gatekeepers' and imposes obligations to ensure fair competition. Self-preferencing, where a platform favors its own services over competitors, is a key prohibited practice under the DMA. Google's search service and Play Store have been designated as core platform services subject to these rules.

<details><summary>References</summary>
<ul>
<li><a href="https://element.io/blog/the-digital-markets-act-explained-in-15-questions/">The Digital Markets Act explained in 15 questions</a></li>
<li><a href="https://laweconcenter.org/resources/antitrust-unchained-the-eus-case-against-self-preferencing/">Antitrust Unchained: The EU’s Case Against Self-Preferencing</a></li>
<li><a href="https://digital-markets-act.ec.europa.eu/developer-portal/app-distribution_en">App distribution - Digital Markets Act (DMA) - European ...</a></li>

</ul>
</details>

**Tags**: `#antitrust`, `#DMA`, `#Google`, `#EU`, `#regulation`

---

<a id="item-9"></a>
## [Musk: xAI to Open-Source 0.5T Parameter Model by End of 2026](https://x.com/i/status/2058796067592736866) ⭐️ 8.0/10

Elon Musk announced that xAI will open-source a 0.5 trillion parameter model by the end of 2026, widely speculated to be the Grok 4.2 base model. Open-sourcing such a large model would continue xAI's commitment to transparency and could provide the AI community with a powerful, freely available language model, potentially accelerating research and applications. The model has 0.5 trillion parameters, and xAI previously open-sourced Grok-1 (314B parameters) under the Apache 2.0 license. The new model is expected to be the active base model Grok 4.2.

telegram · zaihuapd · May 26, 02:46

**Background**: Large language models like Grok use a Mixture-of-Experts (MoE) architecture, which divides the model into multiple subnetworks to improve efficiency. xAI has a history of open-sourcing its models, starting with Grok-1 in 2024. Open-sourcing allows the community to study, fine-tune, and deploy the model without restrictions.

<details><summary>References</summary>
<ul>
<li><a href="https://www.nextbigfuture.com/2026/04/anthropic-and-xai-model-parameter-counts.html">Anthropic and xAI Model Parameter Counts | NextBigFuture.com</a></li>
<li><a href="https://en.wikipedia.org/wiki/Grok_(chatbot)">Grok (chatbot) - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Community sentiment appears mixed, with one user dismissively questioning whether anyone would actually use the model, comparing it unfavorably to a Chinese term 'doubao' (bean bag), implying it is not useful.

**Tags**: `#AI`, `#open-source`, `#xAI`, `#Grok`, `#large language models`

---