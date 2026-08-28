---
layout: default
title: "Horizon Summary: 2026-07-02 (EN)"
date: 2026-07-02
lang: en
---

> From 43 items, 15 important content pieces were selected

---

1. [Egg Price Fixers Profited Thousands Times More Than Fines](#item-1) ⭐️ 9.0/10
2. [Linux 6.9 LUKS Suspend Regression Keeps Encryption Keys in Memory](#item-2) ⭐️ 8.0/10
3. [Podman 6.0.0 Released with Networking and Quadlet Upgrades](#item-3) ⭐️ 8.0/10
4. [PeerTube: Decentralized Video Platform Gains Attention](#item-4) ⭐️ 8.0/10
5. [F-Droid: Android developer verification is a Trojan horse](#item-5) ⭐️ 8.0/10
6. [Japan Top Court Rules AI Cannot Be Named as Inventor](#item-6) ⭐️ 8.0/10
7. [The Decline of Theorem-Proving Economy](#item-7) ⭐️ 8.0/10
8. [Geoffrey Litt's 'Understand to Participate' Concept](#item-8) ⭐️ 8.0/10
9. [ECTC 2026 Roundup: EMIB-T, HBM4, Photonic Interconnects, More](#item-9) ⭐️ 8.0/10
10. [LLM-Assisted Memory Management Patches Evaluated](#item-10) ⭐️ 8.0/10
11. [Apple Helps FBI Identify Anonymous iCloud Email User](#item-11) ⭐️ 8.0/10
12. [Meta to Sell Surplus AI Compute, Enter Cloud Market](#item-12) ⭐️ 8.0/10
13. [Cloudflare to Default-Block Mixed-Use AI Crawlers, Calls Out Google](#item-13) ⭐️ 8.0/10
14. [Companies Restrict AI Use as Costs Skyrocket](#item-14) ⭐️ 8.0/10
15. [Anthropic in talks with Samsung to manufacture custom AI chips](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Egg Price Fixers Profited Thousands Times More Than Fines](https://www.thebignewsletter.com/p/crime-pays-the-egg-bandits-made-a) ⭐️ 9.0/10

An investigation reveals that egg producers made far more from price fixing than the fines imposed, highlighting regulatory inadequacy. This matters because it shows that current antitrust penalties are too weak to deter illegal collusion, ultimately hurting consumers who pay inflated prices. The fine paid was only a fraction of the illicit profits, with the title stating the bandits made 'a thousand times' the fine. The specific amounts are not given, but the disparity underscores enforcement failures.

hackernews · toomuchtodo · Jul 2, 13:25 · [Discussion](https://news.ycombinator.com/item?id=48761229)

**Background**: Price fixing is an illegal agreement among competitors to set prices artificially high, reducing competition and harming consumers. Antitrust laws are designed to prevent such collusion, but fines are often calculated based on revenue or damages, which may be far less than actual profits gained. In this case, the egg producers allegedly colluded during a period of high egg prices, blaming avian flu and inflation while secretly fixing prices.

**Discussion**: Commenters express frustration with the lack of consequences for corporations, with one noting that individual liability is absent and corporate money is treated as speech. Another mentions that many people were misled into thinking high egg prices were due to inflation and avian flu, when in fact price fixing was a major factor. The discussion also touches on market concentration as a root cause.

**Tags**: `#price fixing`, `#antitrust`, `#corporations`, `#economics`, `#consumer protection`

---

<a id="item-2"></a>
## [Linux 6.9 LUKS Suspend Regression Keeps Encryption Keys in Memory](https://mathstodon.xyz/@iblech/116769502749142438) ⭐️ 8.0/10

Since Linux 6.9, the `cryptsetup luksSuspend` command no longer wipes disk-encryption keys from memory during suspend, leaving them accessible in RAM. This regression undermines the security of LUKS-encrypted devices because an attacker with physical access to a suspended system could extract the master key from memory and decrypt the disk without needing the passphrase. The issue affects Linux kernels from 6.9 onward, but not all distributions are impacted because `luksSuspend` is not part of the official cryptsetup specification; it originated as a Debian extension.

hackernews · IngoBlechschmid · Jul 2, 15:25 · [Discussion](https://news.ycombinator.com/item?id=48763035)

**Background**: LUKS (Linux Unified Key Setup) is a disk encryption specification that uses a master key to encrypt data on a partition. During normal operation, this master key is held in kernel memory to allow decryption on the fly. When a system is suspended to RAM, the key remains in memory, but `luksSuspend` was designed to wipe the key to protect against cold boot or physical attacks. The regression means the key is no longer wiped, leaving it vulnerable.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup">Linux Unified Key Setup - Wikipedia</a></li>
<li><a href="https://sesamedisk.com/linux-luks-suspend-regression-security/">Linux LUKS Suspend Regression: Keys Stay - Sesame Disk</a></li>
<li><a href="https://news.ycombinator.com/item?id=48763035">Since Linux 6.9, LUKS suspend stopped wiping disk-encryption ...</a></li>

</ul>
</details>

**Discussion**: Community comments highlight mixed reactions: some argue that `luksSuspend` is not officially supported and only affects Debian, while others emphasize that security regressions like this are easy to miss because everything still works. A few users downplay the risk, noting that after suspend, the encryption key is expected to be in memory anyway if no passphrase re-entry is required, and that disk encryption mainly protects against data theft when the drive is removed.

**Tags**: `#Linux`, `#kernel`, `#security`, `#encryption`, `#regression`

---

<a id="item-3"></a>
## [Podman 6.0.0 Released with Networking and Quadlet Upgrades](https://blog.podman.io/2026/07/introducing-podman-v6-0-0/) ⭐️ 8.0/10

Podman v6.0.0 introduces new networking features and significant enhancements to Quadlet, a tool for running containers as systemd services. This major release strengthens Podman's position as a leading Docker alternative, especially for system administrators and DevOps who rely on systemd integration and robust networking. The release includes improvements to network configuration and management, as well as Quadlet's ability to generate systemd unit files from container definitions. Users are advised to review the changelog for breaking changes.

hackernews · soheilpro · Jul 2, 14:23 · [Discussion](https://news.ycombinator.com/item?id=48762098)

**Background**: Podman is a daemonless container engine developed by Red Hat, offering a Docker-compatible command-line interface. Quadlet allows users to define containers in simple configuration files and automatically generates systemd services to manage them. This approach simplifies container lifecycle management on Linux systems.

<details><summary>References</summary>
<ul>
<li><a href="https://www.redhat.com/en/blog/quadlet-podman">Make systemd better for Podman with Quadlet</a></li>
<li><a href="https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html">podman -systemd.unit — Podman documentation</a></li>

</ul>
</details>

**Discussion**: Community reactions are mixed: some users praise Podman's improvements and Quadlet's convenience, while others note that minor incompatibilities with Docker can cause issues for projects expecting full compatibility. A user from macOS compares Podman unfavorably to OrbStack in terms of speed.

**Tags**: `#podman`, `#containers`, `#devops`, `#linux`

---

<a id="item-4"></a>
## [PeerTube: Decentralized Video Platform Gains Attention](https://github.com/Chocobozzz/PeerTube) ⭐️ 8.0/10

PeerTube, an open-source, decentralized video platform using ActivityPub federation, has gained significant community attention, with discussions focusing on its monetization challenges and adoption hurdles. PeerTube represents a potential shift towards decentralized video hosting, empowering users and creators with greater control, but its success hinges on solving monetization and content discovery issues. PeerTube leverages P2P technology to reduce server load and uses the ActivityPub protocol to federate with other instances, but currently lacks built-in monetization mechanisms and has a smaller content library compared to YouTube.

hackernews · doener · Jul 2, 11:17 · [Discussion](https://news.ycombinator.com/item?id=48759634)

**Background**: PeerTube is part of the Fediverse, a network of interconnected social platforms using the ActivityPub protocol. Unlike centralized services like YouTube, where one company controls all servers, PeerTube allows anyone to host a 'pod' (server) that can communicate with others, enabling decentralized video hosting. The platform also uses peer-to-peer technology to share bandwidth among viewers, reducing server strain when videos go viral.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/PeerTube">PeerTube - Wikipedia</a></li>
<li><a href="https://github.com/Chocobozzz/PeerTube">GitHub - Chocobozzz/PeerTube: ActivityPub- federated video ...</a></li>
<li><a href="https://docs.joinpeertube.org/contribute/architecture">Architecture | PeerTube documentation</a></li>

</ul>
</details>

**Discussion**: Community comments highlight monetization as the biggest obstacle for professional YouTubers, with one user noting the high production costs. Some creators appreciate PeerTube for open-source projects but lament the lack of audience and content on the platform. Others turn to it after being banned from YouTube. Overall, sentiment is cautiously optimistic but acknowledges significant adoption hurdles.

**Tags**: `#decentralized`, `#video hosting`, `#open source`, `#federation`, `#PeerTube`

---

<a id="item-5"></a>
## [F-Droid: Android developer verification is a Trojan horse](https://f-droid.org/2026/07/01/adv-malware.html) ⭐️ 8.0/10

F-Droid published an article arguing that Google's new Android developer verification, which requires identity verification and package name registration starting September 2026, is actually a threat disguised as protection, especially for open-source app distribution. This verification could restrict installation of apps from third-party stores like F-Droid on certified Android devices, undermining user freedom and the open-source ecosystem. It represents a broader trend of platform control that affects developers and users who rely on alternative app sources. Google's developer verification requires developers to verify their identity and register their package names, and starting September 2026, only apps from verified developers can be installed on certified Android devices in select regions. F-Droid claims this gives Google a chokehold over app distribution, akin to a Trojan horse.

hackernews · drewfax · Jul 2, 03:00 · [Discussion](https://news.ycombinator.com/item?id=48755965)

**Background**: F-Droid is a free and open-source (FOSS) app repository for Android, offering apps without user tracking or non-free dependencies. Google's Play Store has long required developer registration, but sideloading from other sources was generally allowed. The new verification extends this requirement to all apps on certified devices, potentially blocking unverified apps regardless of source.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/F-Droid">F-Droid</a></li>
<li><a href="https://developer.android.com/developer-verification">Android developer verification | Android Developers</a></li>
<li><a href="https://f-droid.org/">F-Droid - Free and Open Source Android App Repository</a></li>

</ul>
</details>

**Discussion**: Community comments show mixed reactions: some support F-Droid's stance and suggest switching to alternative OSes like GrapheneOS, while others criticize the article's tone as childish and counterproductive. One comment notes that the fearmongering could discredit F-Droid's message.

**Tags**: `#Android`, `#F-Droid`, `#developer verification`, `#open source`, `#privacy`

---

<a id="item-6"></a>
## [Japan Top Court Rules AI Cannot Be Named as Inventor](https://japannews.yomiuri.co.jp/science-nature/technology/20260306-314930/) ⭐️ 8.0/10

Japan's Supreme Court has ruled that artificial intelligence cannot be listed as an inventor on patent applications, requiring that only a human can be named as the inventor. This decision sets a legal precedent in a major jurisdiction, clarifying that AI-generated inventions must have a human inventor, which affects patent strategies for companies using AI in research and development. The ruling aligns with similar positions in the U.S. and Europe, where patent offices have also held that AI systems cannot be inventors. It does not prohibit using AI in the invention process but requires human contribution and control.

hackernews · mushstory · Jul 2, 13:43 · [Discussion](https://news.ycombinator.com/item?id=48761536)

**Background**: Patent law traditionally requires an inventor to be a natural person who conceives the invention. As AI systems become more capable of generating novel outputs, courts and patent offices worldwide are grappling with whether AI can be considered an inventor. Japan's ruling reinforces the human-centric view of inventorship.

<details><summary>References</summary>
<ul>
<li><a href="https://www.uspto.gov/subscription-center/2025/revised-inventorship-guidance-ai-assisted-inventions">Revised inventorship guidance for AI-assisted inventions</a></li>

</ul>
</details>

**Discussion**: Community comments were largely supportive, noting that AI lacks accountability and should not own benefits. Others questioned practical loopholes, such as inventors simply listing themselves when AI was used. Some referenced economic arguments against patents altogether.

**Tags**: `#AI`, `#patents`, `#intellectual property`, `#Japan`, `#legal ruling`

---

<a id="item-7"></a>
## [The Decline of Theorem-Proving Economy](https://davidbessis.substack.com/p/the-fall-of-the-theorem-economy) ⭐️ 8.0/10

David Bessis argues that the traditional theorem-proving economy is declining as automated proof assistants and formalization shift mathematics toward intuition and visualization. This essay critiques the system's obsession with theorem-proving priority while real progress often occurs outside that loop. This matters because it signals a transformation in how mathematics is practiced and valued, with AI and formal tools challenging the core incentive structure of academic mathematics. It could reshape priorities toward insight and understanding rather than pure theorem production. Bessis highlights that AI-written proofs in systems like Lean often fail to convey useful human insights, yet they are increasingly used. He contends that the intuitions gained from proving are more valuable than the proof itself.

hackernews · varjag · Jul 2, 08:01 · [Discussion](https://news.ycombinator.com/item?id=48758048)

**Background**: A proof assistant is a software tool that helps humans develop formal proofs through human-machine collaboration. Formal verification uses mathematical methods to prove correctness of systems. The term 'theorem economy' refers to the academic culture that prioritizes proving new theorems as the primary currency of mathematical achievement.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Proof_assistant">Proof assistant - Wikipedia</a></li>
<li><a href="https://davidbessis.substack.com/p/the-fall-of-the-theorem-economy">The fall of the theorem economy - David Bessis</a></li>
<li><a href="https://en.wikipedia.org/wiki/Formal_verification">Formal verification - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Comments reference Greg Egan's 'truth mining' concept from the novel Diaspora, foreseeing mathematics evolving into visualization and insight after formalization. Another comment draws parallels to software testing, suggesting that mathematicians may adopt a culture of 'battle-tested' confidence rather than formal proof. Some note the article's prior submissions on Hacker News.

**Tags**: `#mathematics`, `#formal verification`, `#theorem proving`, `#AI`, `#philosophy of mathematics`

---

<a id="item-8"></a>
## [Geoffrey Litt's 'Understand to Participate' Concept](https://simonwillison.net/2026/Jul/2/understand-to-participate/#atom-everything) ⭐️ 8.0/10

Geoffrey Litt introduced the concept of 'Understand to participate' at the AIE conference, emphasizing that developers must deeply understand AI-generated code to avoid cognitive debt and actively collaborate with coding agents. This concept highlights a critical challenge in AI-assisted development: as coding agents produce more code, developers risk accruing cognitive debt, which can undermine their ability to guide and improve the software. It shifts the conversation from mere productivity to sustainable understanding. The talk was part of the AIE World's Fair 2026, and all 300+ recordings will be released over three weeks. Litt also published a thread version of his talk on Twitter.

rss · Simon Willison · Jul 2, 17:07

**Background**: Cognitive debt refers to the growing gap between a developer's understanding of code and how it actually works, especially when code is generated by AI. In AI-assisted development, developers often accept AI-generated code without full comprehension, leading to mental overhead and reduced ability to make informed changes. The 'understand to participate' philosophy argues that to collaborate effectively with coding agents, developers must maintain a deep enough understanding to actively shape the project.

<details><summary>References</summary>
<ul>
<li><a href="https://x.com/geoffreylitt/status/2072522267414901109">That's where another answer comes in: we can understand to ...</a></li>
<li><a href="https://dev.to/bala_paranj_059d338e44e7e/six-contradictions-behind-cognitive-debt-in-ai-assisted-development-30no">Six Contradictions Behind Cognitive Debt in AI Assisted Development</a></li>

</ul>
</details>

**Tags**: `#AI-assisted development`, `#coding agents`, `#cognitive debt`, `#software engineering`

---

<a id="item-9"></a>
## [ECTC 2026 Roundup: EMIB-T, HBM4, Photonic Interconnects, More](https://newsletter.semianalysis.com/p/ectc2026) ⭐️ 8.0/10

At ECTC 2026, Intel introduced EMIB-T, an advanced packaging technology supporting larger chip sizes and HBM4, while TSMC, SK Hynix, Samsung, Micron, Marvell, Lightmatter, and Microsoft presented progress in custom HBM, microfluidic cooling, and photonic interconnects. These developments are critical for scaling AI hardware and chiplet architectures, as advanced packaging directly impacts performance, bandwidth, and thermal management. EMIB-T supports package sizes up to 120x180mm, over 38 bridges, and more than 12 reticle-sized dies. Photonic interconnects aim to replace electrical I/O with optical pathways to reduce power and increase bandwidth.

rss · Semianalysis · Jul 2, 17:25

**Background**: Advanced semiconductor packaging integrates multiple chips (chiplets) into a single package to improve performance and reduce cost. EMIB (Embedded Multi-die Interconnect Bridge) is Intel's technology for high-density chip-to-chip connections. Photonic interconnects use light for data transmission, offering higher bandwidth and lower power than electrical interconnects.

<details><summary>References</summary>
<ul>
<li><a href="https://www.tomshardware.com/pc-components/cpus/intel-details-new-advanced-packaging-breakthroughs-emib-t-paves-the-way-for-hbm4-and-increased-ucie-bandwidth">Intel details new advanced packaging breakthroughs — EMIB - T paves...</a></li>
<li><a href="https://lightmatter.co/knowledge-hub/how-do-photonic-interconnects-work/">How Do Photonic Interconnects Work? - lightmatter.co</a></li>

</ul>
</details>

**Tags**: `#semiconductor packaging`, `#HBM`, `#photonic interconnects`, `#ECTC`, `#advanced cooling`

---

<a id="item-10"></a>
## [LLM-Assisted Memory Management Patches Evaluated](https://lwn.net/Articles/1080162/) ⭐️ 8.0/10

Two large memory-management patch sets, developed with LLM assistance by established kernel developers, are being reviewed by the Linux kernel community. This marks a shift in how AI-generated contributions are received, as patches from respected developers are taken seriously, potentially setting a precedent for future LLM-assisted work. One patch set by Rik van Riel introduces 'super page blocks' to reliably allocate 1GB huge pages without the inflexible hugetlbfs reservation system, addressing memory fragmentation challenges.

rss · LWN.net · Jul 2, 14:06

**Background**: Memory fragmentation in long-running Linux systems makes large contiguous allocations difficult. The kernel uses page blocks (e.g., 4MB) to manage fragmentation, but 1GB allocations are unreliable without hugetlbfs, which reserves memory at boot time. Super page blocks aim to provide a new visibility level for allocation decisions.

<details><summary>References</summary>
<ul>
<li><a href="https://www.pingcap.com/blog/linux-kernel-vs-memory-fragmentation-1/">Memory Fragmentation in Linux: Causes, Fixes & Tools</a></li>
<li><a href="https://www.alibabacloud.com/help/en/alinux/support/solutions-to-memory-fragmentation-in-linux-operating-systems">Fix performance issues due to Linux memory fragmentation - Alibaba Cloud Linux - Alibaba Cloud</a></li>

</ul>
</details>

**Discussion**: The article notes that LLM contributions from unknown developers have faced skepticism, but those from established developers receive more serious evaluation, highlighting the importance of contributor reputation.

**Tags**: `#Linux kernel`, `#LLM`, `#memory management`, `#patch sets`, `#open source`

---

<a id="item-11"></a>
## [Apple Helps FBI Identify Anonymous iCloud Email User](https://t.me/zaihuapd/42302) ⭐️ 8.0/10

Apple provided the FBI with the real iCloud account details linked to a 'Hide My Email' address used to send threatening messages, leading to the identification and confession of the suspect, Alden Ruml. This case shows that Apple's 'Hide My Email' feature, marketed as a privacy tool, is not fully anonymous and can be traced back to users in law enforcement investigations, challenging user trust in Apple's privacy promises. The suspect, Alden Ruml, had created 134 anonymous email addresses through the 'Hide My Email' feature and admitted to sending threats to Alexis Wilkins, the girlfriend of FBI Director Kash Patel.

telegram · zaihuapd · Jul 2, 01:03

**Background**: iCloud+'s 'Hide My Email' feature allows paid subscribers to generate unique, random email addresses that forward to their personal inbox, intended to protect privacy when signing up for services. However, Apple retains the mapping between the anonymous address and the user's real iCloud account, and can provide this information in response to valid law enforcement requests.

<details><summary>References</summary>
<ul>
<li><a href="https://www.landian.news/archives/112374.html">iCloud+ 隐 藏 邮 件 地 址 可不 能 乱用：苹果帮助FBI... | 蓝点网</a></li>
<li><a href="https://www.ithome.com/0/934/278.htm">苹果被指向美执法部门披露使用隐私邮箱用户的真实身份 - IT之家</a></li>
<li><a href="https://www.sohu.com/a/1003418999_362225">苹果“隐藏我的邮箱”功能遭挑战：向美执法部门披露用户真实信息</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#Apple`, `#law enforcement`, `#iCloud`, `#anonymity`

---

<a id="item-12"></a>
## [Meta to Sell Surplus AI Compute, Enter Cloud Market](https://www.bloomberg.com/news/articles/2026-07-02/south-korean-stocks-tumble-6-as-ai-jitters-hurt-chipmakers) ⭐️ 8.0/10

Meta is planning to sell excess AI computing capacity and model services to external customers, signaling a potential entry into the cloud computing market. This news, combined with Apple's discussions to source chips from Chinese memory suppliers YMTC and CXMT, triggered a sharp sell-off in South Korean chipmakers like Samsung and SK Hynix. This development raises concerns about a potential slowdown in AI infrastructure investment by big tech, which could lead to oversupply of AI chips and memory components. It also threatens the dominance of South Korean memory leaders as Apple diversifies its supply chain to Chinese alternatives. The Kospi index fell up to 7% on July 2, 2026, with Samsung and SK Hynix dropping at least 8%, prompting a temporary halt in programmatic selling of Kospi futures. Apple is reportedly in talks with YMTC (NAND flash) and CXMT (DRAM) for chips used in devices sold in China.

telegram · zaihuapd · Jul 2, 02:29

**Background**: Meta has been heavily investing in AI infrastructure, building massive compute clusters for training and inference. Surplus compute capacity is now being considered for external sale, similar to how Amazon Web Services (AWS) originated from Amazon's internal infrastructure. Meanwhile, Chinese memory manufacturers YMTC and CXMT have advanced to produce competitive NAND and DRAM, challenging South Korean incumbents.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/YMTC">YMTC</a></li>
<li><a href="https://en.wikipedia.org/wiki/CXMT">CXMT</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Meta`, `#Cloud Computing`, `#Semiconductors`, `#Market`

---

<a id="item-13"></a>
## [Cloudflare to Default-Block Mixed-Use AI Crawlers, Calls Out Google](https://techcrunch.com/2026/07/01/cloudflares-new-policy-pushes-ai-companies-to-pay-for-publishers-content/) ⭐️ 8.0/10

Cloudflare announced that starting September 15, 2026, it will default-block mixed-use AI crawlers—those that simultaneously scrape for search indexing and AI training—on ad-supported pages. The company specifically criticized Google for exploiting a loophole where publishers block AI crawlers but allow Google's search bot, which Google then uses to train its AI models. This policy shift forces AI companies to either separate their crawlers by function or pay for content usage, potentially altering the economic balance between web publishers and AI developers. It could set a precedent for other internet infrastructure providers and empower publishers to control how their content is used for AI training. The default block applies to new Cloudflare websites and existing free-tier customers, while paid customers can opt in or out. Cloudflare also partnered with Ceramic.ai and You.com to enable a pay-per-use revenue model, allowing AI companies to compensate publishers based on actual usage.

telegram · zaihuapd · Jul 2, 05:37

**Background**: Cloudflare is a major internet infrastructure company that powers a significant portion of the web, providing security and performance services. AI crawlers are automated programs that scrape website content to train large language models. Publishers have faced a dilemma: they want to allow search engine crawlers to index their content for visibility, but they want to prevent AI companies from scraping their content for training without compensation. Google has been accused of ignoring publisher opt-outs and using its search crawler data to train AI, despite claims that its Google-Extended crawler allows opting out.

<details><summary>References</summary>
<ul>
<li><a href="https://www.chatai.com/posts/cloudflare-changes-ai-crawling-rules-blocking-mixed-use-ai-bots-by-default">Cloudflare Changes AI Crawling Rules, Blocking Mixed - Use ... | ChatAI</a></li>
<li><a href="https://www.wired.com/story/cloudflare-blocks-ai-crawlers-default/">Cloudflare Is Blocking AI Crawlers by Default | WIRED</a></li>
<li><a href="https://www.newsbytesapp.com/news/science/google-reveals-ai-training-loophole-in-court-testimony/story">Google can train AI using web content despite publisher opt-out</a></li>

</ul>
</details>

**Tags**: `#Cloudflare`, `#AI crawlers`, `#web scraping`, `#Google`, `#publisher rights`

---

<a id="item-14"></a>
## [Companies Restrict AI Use as Costs Skyrocket](https://www.404media.co/companies-are-throttling-employees-ai-use-because-its-too-expensive/) ⭐️ 8.0/10

Citibank, Atlassian, and Adobe are restricting employee use of advanced AI models like GPT-5.5 and Claude Opus 4.6 due to unsustainable cost increases from usage-based pricing. Atlassian's monthly AI spending tripled from $5 million in August 2025 to over $15 million in May 2026. This reveals concrete financial challenges in enterprise AI adoption, contradicting the narrative of unlimited AI integration. Companies may need to adopt cost management strategies, potentially slowing AI deployment in business workflows. Citibank banned GPT-5.5 and Claude Opus 4.6 on June 24, 2026, due to excessive AI credit consumption. Atlassian implemented cost-tracking dashboards and ended unlimited usage, while Adobe did not renew its unlimited Claude contract expiring June 30, 2026.

telegram · zaihuapd · Jul 2, 13:59

**Background**: GPT-5.5 is a large language model by OpenAI released April 23, 2026, known for high benchmark scores and a tendency to mention goblins that was later corrected. Claude Opus 4.6 is Anthropic's flagship model released February 5, 2026. These models are offered via API with usage-based pricing, meaning companies pay per token processed, which can lead to unpredictable costs when scaled across employees.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GPT-5.5">GPT-5.5</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_Opus_4.6">Claude Opus 4.6</a></li>
<li><a href="https://openai.com/index/introducing-gpt-5-5/">Introducing GPT‑5.5 - OpenAI</a></li>

</ul>
</details>

**Tags**: `#AI cost`, `#enterprise AI`, `#cost management`, `#AI adoption`, `#technology news`

---

<a id="item-15"></a>
## [Anthropic in talks with Samsung to manufacture custom AI chips](https://www.theinformation.com/articles/anthropic-talks-samsung-manufacture-custom-ai-chip) ⭐️ 8.0/10

Anthropic has started developing its own AI chips and is in early negotiations with Samsung Electronics for manufacturing, aiming to gain more control over the compute infrastructure for its Claude model. This move signals Anthropic's strategic push toward vertical integration in AI hardware, reducing reliance on external chip suppliers like Google and Amazon. If successful, it could enhance performance and cost-efficiency for Claude, similar to OpenAI's chip efforts. The project is still in early stages, and Anthropic may ultimately decide to only purchase AI chips instead. Custom AI chip development is extremely costly, with R&D potentially exceeding $500 million.

telegram · zaihuapd · Jul 2, 15:57

**Background**: Major AI companies like Meta, OpenAI, and Google are increasingly developing custom chips to reduce dependence on Nvidia GPUs and optimize for their specific workloads. Samsung's foundry business has recently begun selectively accepting new customers as the market shifts. Anthropic currently relies heavily on Google's TPUs and Amazon's custom chips for Claude's compute needs.

<details><summary>References</summary>
<ul>
<li><a href="https://finance.sina.com.cn/stock/usstock/c/2026-07-02/doc-inifmrtq5832255.shtml">知情人士：Anthropic正与三星洽谈定制AI芯片代工合作_新浪财经_新浪网</a></li>
<li><a href="https://www.tradingkey.com/zh-hans/analysis/stocks/us-stock/261770244-from-openai-to-anthropic-in-house-chip-development-tradingkey">从OpenAI到Anthropic： AI巨头算力自主战打响，芯片自研成必选项？</a></li>
<li><a href="https://www.ithome.com/0/971/836.htm">现在是供方时间：消息称三星晶圆代工已开始选择性接受新客户订单 - IT...</a></li>

</ul>
</details>

**Tags**: `#Anthropic`, `#AI chips`, `#semiconductor`, `#Samsung`, `#AI infrastructure`

---