---
layout: default
title: "Horizon Summary: 2026-06-20 (EN)"
date: 2026-06-20
lang: en
---

> From 34 items, 14 important content pieces were selected

---

1. [Project Valhalla's value types arrive in JDK 28](#item-1) ⭐️ 9.0/10
2. [Norway Bans AI for Elementary Students, Allows Supervised Use for Teens](#item-2) ⭐️ 8.0/10
3. [ATProto Has No Instances Like Mastodon](#item-3) ⭐️ 8.0/10
4. [Hyundai completes full acquisition of Boston Dynamics](#item-4) ⭐️ 8.0/10
5. [EFF: Court Records Should Be Free, End PACER Fees](#item-5) ⭐️ 8.0/10
6. [Amateur May Have Cracked Linear A Using AI](#item-6) ⭐️ 8.0/10
7. [Systemd v261 released with IMDS, boot secrets, and live update support](#item-7) ⭐️ 8.0/10
8. [BPF coroutines enable suspend/resume of programs](#item-8) ⭐️ 8.0/10
9. [AUR under sustained attack: orphaned packages used to push malware](#item-9) ⭐️ 8.0/10
10. [China Proposes Regulation for Decentralized Digital Identity](#item-10) ⭐️ 8.0/10
11. [ZhiPu Founder Claims Model Could Reach 'Mythos' Level by Q1 2027](#item-11) ⭐️ 8.0/10
12. [US pressures ASML over possible EUV tool reaching China](#item-12) ⭐️ 8.0/10
13. [Google Imposes 24-Hour Wait for Sideloading Unverified Apps](#item-13) ⭐️ 8.0/10
14. [Court docs: SpaceX sold shares to Chinese investors before IPO](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Project Valhalla's value types arrive in JDK 28](https://www.jvm-weekly.com/p/project-valhalla-explained-how-a) ⭐️ 9.0/10

After a decade of development, Project Valhalla's value types are finally arriving in JDK 28, fundamentally changing how the JVM handles memory layout for objects. This significantly improves performance and memory efficiency for Java applications, especially for data-intensive workloads, by enabling dense storage of values without object headers or pointers. Value types allow arrays of objects to be stored contiguously with no per-element headers, but heap flattening is limited to objects with representations up to 64 bits; larger objects still incur indirection.

hackernews · philonoist · Jun 19, 06:35 · [Discussion](https://news.ycombinator.com/item?id=48595511)

**Background**: Project Valhalla is an OpenJDK project started in 2014 to introduce value types to Java. Value types are user-defined types that behave like primitives, with no identity and compact memory layout. This is a major evolution of the Java object model, aiming to combine the performance of primitives with the abstraction of objects.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Project_Valhalla_(Java_language)">Project Valhalla (Java language)</a></li>
<li><a href="https://openjdk.org:443/projects/valhalla/">Project Valhalla</a></li>

</ul>
</details>

**Discussion**: The community discussion shows a mix of appreciation for the hard work and criticism, particularly around the complexity of the null safety model and the limitations of heap flattening for larger objects. Some commenters defend Java's evolution, noting that Java has improved significantly since its early days.

**Tags**: `#Java`, `#Project Valhalla`, `#JVM`, `#value types`, `#performance`

---

<a id="item-2"></a>
## [Norway Bans AI for Elementary Students, Allows Supervised Use for Teens](https://www.reuters.com/technology/norway-imposes-near-ban-ai-elementary-school-2026-06-19/) ⭐️ 8.0/10

The Norwegian government announced a near-total ban on AI use for students aged 6 to 13 in elementary schools, while allowing limited, supervised AI use for students aged 14 to 16 in lower secondary school. This policy sets a significant precedent for regulating AI in education, highlighting concerns that generative AI may hinder foundational learning skills like reading and writing. It sparks debate on how to balance AI's potential benefits with risks to child development. The ban applies to students in first through seventh grade, with a general rule against AI use, while older students can use AI tools cautiously under teacher supervision. The government cited the need for children to first develop core competencies before engaging with AI.

hackernews · ilreb · Jun 19, 16:03 · [Discussion](https://news.ycombinator.com/item?id=48600093)

**Background**: Generative AI, like ChatGPT, can produce human-like text, raising concerns that students may use it to cheat on assignments or bypass learning critical thinking and writing skills. Many educators argue that banning or strictly limiting AI in early education is necessary to preserve foundational learning, similar to not allowing calculators before students understand arithmetic.

**Discussion**: Comments generally support the ban, with simonw agreeing that kids under 13 need to learn reading and writing without AI. nunez points out that AI has been detrimental to student outcomes and that banning it requires substantial teacher workload. baq suggests AI could be useful in tutor mode with proper safeguards for younger students.

**Tags**: `#AI in Education`, `#Regulation`, `#Norway`, `#Policy`, `#K-12`

---

<a id="item-3"></a>
## [ATProto Has No Instances Like Mastodon](https://overreacted.io/there-are-no-instances-in-atproto/) ⭐️ 8.0/10

Dan Abramov's blog post clarifies that ATProto does not use 'instances' like Mastodon; instead, it separates functionality into relays, app views, and personal data servers (PDS). This explanation resolves a common misconception among developers and users, highlighting ATProto's distinct architectural approach to decentralization and scalability. In ATProto, relays shuttle data between services without interpreting content, allowing app views to scale independently. This separation contrasts with ActivityPub's instance-based model where each server handles all functions.

hackernews · danabramov · Jun 19, 15:10 · [Discussion](https://news.ycombinator.com/item?id=48599515)

**Background**: ActivityPub-based platforms like Mastodon use 'instances'——independent servers that host user accounts, content, and handle federation. ATProto decouples these roles into three distinct services: relays for data distribution, app views for user experience, and PDS for personal data storage. This design aims to improve flexibility and reduce operational costs for smaller operators.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AT_Protocol">AT Protocol - Wikipedia</a></li>
<li><a href="https://atproto.com/guides/overview">Protocol Overview - AT Protocol</a></li>
<li><a href="https://docs.bsky.app/docs/advanced-guides/atproto">The AT Protocol | Bluesky</a></li>

</ul>
</details>

**Discussion**: Commenters pointed out that despite protocol-level decentralization, Bluesky the corporation runs the main app and hosts most user data, leading to effective centralization. Others praised the architectural clarity but raised concerns about relay costs and the difficulty of self-hosting independently.

**Tags**: `#ATProto`, `#Bluesky`, `#decentralized protocols`, `#ActivityPub`, `#social media architecture`

---

<a id="item-4"></a>
## [Hyundai completes full acquisition of Boston Dynamics](https://startupfortune.com/hyundai-takes-full-control-of-boston-dynamics-as-softbank-exits-for-325-million/) ⭐️ 8.0/10

Hyundai Motor Group has exercised its put option to acquire the remaining stake in Boston Dynamics from SoftBank, taking full ownership of the robotics company. This move solidifies Hyundai's commitment to robotics, potentially accelerating the commercialization of humanoid robots like Atlas amid South Korea's shrinking working-age population. In December 2020, Hyundai initially purchased an 80% stake for $880 million, valuing Boston Dynamics at $1.1 billion. The agreement included a put option that SoftBank has now exercised to sell its remaining approximately 9% stake.

hackernews · ck2 · Jun 19, 16:28 · [Discussion](https://news.ycombinator.com/item?id=48600312)

**Background**: Boston Dynamics is known for advanced robots like Atlas (humanoid) and Spot (quadruped). SoftBank acquired it from Google's parent Alphabet in 2017. Hyundai, a major automaker, aims to apply robotics in manufacturing and beyond, especially as South Korea faces a projected 25% decline in working-age population by 2040.

**Discussion**: Commenters debated the merits of humanoid vs. purpose-built robots, with some arguing humanoids are suboptimal for manufacturing. Others linked the acquisition to South Korea's demographic decline, suggesting general-purpose robotics could address labor shortages. There was also skepticism about Atlas's immediate utility in car factories.

**Tags**: `#robotics`, `#acquisitions`, `#Boston Dynamics`, `#Hyundai`, `#SoftBank`

---

<a id="item-5"></a>
## [EFF: Court Records Should Be Free, End PACER Fees](https://www.eff.org/deeplinks/2026/06/court-records-should-be-free) ⭐️ 8.0/10

The Electronic Frontier Foundation (EFF) published an article arguing that public access to court records should be free, highlighting the financial burden of PACER's per-page fees. This matters because high fees on court records hinder public access to justice, transparency, and the ability of citizens and journalists to monitor the judicial system. PACER charges $1 per page for federal court documents, while some state courts charge even more (e.g., $10 per page in Idaho). Tools like CourtListener and the Recap plugin help share purchased documents for free.

hackernews · hn_acker · Jun 19, 17:34 · [Discussion](https://news.ycombinator.com/item?id=48600946)

**Background**: PACER (Public Access to Court Electronic Records) is an electronic system that provides public access to federal court documents, but requires users to pay per-page fees. Critics argue that since taxpayers fund the courts, records should be freely accessible. The EFF has long advocated for free access, and projects like CourtListener aim to circumvent the paywall by crowdsourcing purchased documents.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/PACER_(law)">PACER (law) - Wikipedia</a></li>
<li><a href="https://pacer.uscourts.gov/">Public Access to Court Electronic Records | PACER: Federal ...</a></li>
<li><a href="https://www.uscourts.gov/court-records/find-a-case-pacer">Find a Case (PACER) - United States Courts</a></li>

</ul>
</details>

**Discussion**: Commenters highlighted the even higher fees in state courts, praised CourtListener and Recap for filling a vital gap, and argued that the government intentionally limits access to rights. Some suggested that access should be free for approved partners like law firms and data collectors, while others emphasized that court decisions are the law and should be freely readable.

**Tags**: `#legal tech`, `#open data`, `#access to justice`, `#PACER`, `#public records`

---

<a id="item-6"></a>
## [Amateur May Have Cracked Linear A Using AI](https://aiclambake.com/clamtakes/linear-a/) ⭐️ 8.0/10

An amateur researcher, Tom Di Mino, has used Claude Code to build Python scripts that analyze the Linear A corpus, claiming to have translated over 300 words. His work is currently under review by linguistics experts at Rutgers and Cambridge. If validated, this would be the first decipherment of Linear A, a script that has remained undeciphered for over a century. It also showcases how AI tools can assist in complex cryptographic and linguistic research. The researcher used Claude Code to create a suite of Python scripts that query, cross-reference, and organize the digitized Linear A corpus from the GORILA and SigLA databases. The total corpus contains only about 7500 characters across roughly 1500 inscriptions, making systematic analysis extremely challenging.

hackernews · Kosturdistan · Jun 19, 16:04 · [Discussion](https://news.ycombinator.com/item?id=48600107)

**Background**: Linear A is a writing system used by the Minoan civilization of Crete from 1800 to 1450 BC. It has not been deciphered since its rediscovery in 1900, unlike its descendant Linear B, which was deciphered in the 1950s and represents Mycenaean Greek. The small corpus size and the lack of a bilingual text have been major obstacles.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Linear_A_script">Linear A script</a></li>
<li><a href="https://www.worldhistory.org/Linear_A_Script/">Linear A Script - World History Encyclopedia</a></li>

</ul>
</details>

**Discussion**: Commenters express cautious optimism, noting that the researcher's work is being reviewed by experts and that his approach produces tangible results (over 300 translated words). Some highlight the extremely small corpus size (7500 characters) and caution against false claims, but the use of AI tools is seen as a promising methodology.

**Tags**: `#Linear A`, `#cryptography`, `#AI-assisted research`, `#ancient scripts`, `#linguistics`

---

<a id="item-7"></a>
## [Systemd v261 released with IMDS, boot secrets, and live update support](https://lwn.net/Articles/1078708/) ⭐️ 8.0/10

Systemd v261 introduces a new cloud Instance Metadata Service (IMDS) subsystem, a 'boot secret' mechanism for systems without a TPM, and support for the kernel's Live Update Orchestration (LUO) and Kexec Handover (KHO). These additions significantly enhance systemd's capabilities in cloud and security contexts, enabling more robust instance metadata retrieval, encrypted secrets on non-TPM hardware, and seamless kernel live updates, which impact system administration and cloud orchestration workflows. The IMDS daemon provides a Varlink-based interface with CLI commands usable by tools like cloud-init, while the boot secret feature allows binding secrets to boot phases without a physical TPM. LUO/KHO support enables preserving stateful file descriptors across kexec-based kernel updates.

rss · LWN.net · Jun 19, 18:56

**Background**: Systemd is the init system and service manager used by most major Linux distributions. IMDS is a cloud feature that provides metadata about the running instance (like IP addresses, hostname) typically accessed over HTTP; integrating it into systemd standardizes access. Boot secrets allow encryption of sensitive data tied to the boot process, traditionally relying on a TPM (Trusted Platform Module) chip. Live Update Orchestration and Kexec Handover are kernel mechanisms for updating the kernel in place without a full reboot, preserving critical state.

<details><summary>References</summary>
<ul>
<li><a href="https://lwn.net/Articles/1033364/">Kexec handover and the live update orchestrator [LWN.net]</a></li>
<li><a href="https://lwn.net/Articles/1001730/">Systemd takes steps toward a more secure boot process [LWN.net]</a></li>
<li><a href="https://github.com/systemd/systemd/issues/40763">Instance Metadata Service (IMDS) daemon integrated into systemd ...</a></li>

</ul>
</details>

**Tags**: `#systemd`, `#linux`, `#system-administration`, `#cloud`, `#init-system`

---

<a id="item-8"></a>
## [BPF coroutines enable suspend/resume of programs](https://lwn.net/Articles/1076210/) ⭐️ 8.0/10

Kumar Kartikeya Dwivedi proposed a design to allow BPF programs to be expressed as coroutines, enabling suspension and resumption at LSFMM+BPF 2026. This change simplifies writing long-running BPF tasks like stack trace collection or user-space networking by avoiding manual splitting into callbacks, making kernel extensions easier to develop. The design uses stackless coroutines, akin to Rust's async or C++ coroutines, where the compiler rewrites code for suspension/resume, and the BPF verifier sees resumption as an indirect function call.

rss · LWN.net · Jun 19, 15:55

**Background**: BPF (Berkeley Packet Filter) programs traditionally run to completion in the same context. To handle multi-step tasks, developers had to break logic into separate hooks and manage state manually. Coroutines allow a single function to pause and resume later, which is critical for long-running or deferred operations.

<details><summary>References</summary>
<ul>
<li><a href="https://bpfconf.ebpf.io/bpfconf2026/bpfconf2026_material/Coroutines+in+BPF+-+LSF_MM_BPF+May+2026.pdf">Coroutines in BPF - LSF/MM/BPF May 2026 - bpfconf.ebpf.io</a></li>

</ul>
</details>

**Tags**: `#BPF`, `#Linux kernel`, `#coroutines`, `#LSFMM`, `#kernel development`

---

<a id="item-9"></a>
## [AUR under sustained attack: orphaned packages used to push malware](https://lwn.net/Articles/1077619/) ⭐️ 8.0/10

A sustained attack on the Arch User Repository (AUR) has been ongoing, where malicious actors adopt orphaned packages to push malware. The AUR team temporarily suspended new-user registration on June 19, 2026, to stem the influx of attacker accounts. This attack undermines trust in the AUR, a critical community repository for Arch Linux users seeking software not in official repositories. The incident highlights fundamental security flaws in the AUR's trust model and may drive major changes to its governance. The AUR hosts over 107,000 packages, including nearly 14,000 orphaned ones that any registered user can adopt without review. Attackers created new accounts to take over orphaned packages and push malicious PKGBUILD files that install malware.

rss · LWN.net · Jun 19, 14:40

**Background**: The Arch User Repository (AUR) is a community-driven repository for Arch Linux where users share PKGBUILD scripts to build software from source. Unlike official repositories, AUR packages undergo no formal review before publication or updates. Orphaned packages are those without a maintainer and are free for any registered user to adopt. Many Arch Linux users rely on AUR helpers like yay or paru to manage AUR packages.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Arch_User_Repository">Arch User Repository</a></li>
<li><a href="https://wiki.archlinux.org/title/Arch_User_Repository">Arch User Repository - ArchWiki</a></li>

</ul>
</details>

**Tags**: `#security`, `#Arch Linux`, `#AUR`, `#attacks`, `#open source`

---

<a id="item-10"></a>
## [China Proposes Regulation for Decentralized Digital Identity](https://www.cac.gov.cn/2026-06/18/c_1783525605384124.htm) ⭐️ 8.0/10

China's Cyberspace Administration (CAC) published a draft regulation on June 18, 2026, seeking public comments on promoting interoperability and mutual recognition of decentralized digital identities using blockchain. If enacted, this regulation would establish a national framework for decentralized digital identity in China, potentially enabling cross-platform identity verification across finance, transportation, customs, and digital yuan, and setting a precedent for government-backed blockchain identity systems. The draft defines decentralized digital identity as consisting of identifiers, keys, verifiable credentials (VCs), and verifiable declarations, and proposes to build an 'identity chain' on the national blockchain network to enable interoperability.

telegram · zaihuapd · Jun 19, 01:39

**Background**: Decentralized digital identity (DDID) allows users to control their own identity data without relying on a central authority, using blockchain for tamper-proof records. Verifiable credentials (VCs) are digital documents that follow W3C standards, enabling cryptographic verification of claims. This regulation aligns with global trends toward self-sovereign identity (SSI).

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Verifiable_credentials">Verifiable credentials</a></li>
<li><a href="https://chain.link/education-hub/blockchain-identity">Digital Identity on the Blockchain With Chainlink | Chainlink</a></li>
<li><a href="https://www.dock.io/post/blockchain-identity-management">Blockchain Identity Management: Beginner's Guide 2026</a></li>

</ul>
</details>

**Tags**: `#decentralized identity`, `#blockchain`, `#regulation`, `#digital identity`, `#China`

---

<a id="item-11"></a>
## [ZhiPu Founder Claims Model Could Reach 'Mythos' Level by Q1 2027](https://x.com/jietang/status/2067580270078030088) ⭐️ 8.0/10

ZhiPu AI founder Tang Jie disputed a user's estimate that Chinese AI labs would reach Anthropic's Mythos-level model by late 2026, stating publicly that his company's progress would be faster and could achieve the milestone by Q1 2027. Elon Musk also weighed in, agreeing with a Q1 2027 timeline. This exchange highlights the intensifying competition between Chinese and US AI labs, with top figures publicly debating timelines for frontier model capabilities. The outcome could influence investor confidence, research priorities, and perceptions of the global AI race. The original user assessment estimated ZhiPu's GLM-5.2 model to be at roughly Claude Opus 4.7–4.8 level, implying a 7-month gap between Chinese and US models. Anthropic's Mythos (also called Fable) is a frontier AI model previewed in April 2026, known for strong agentic coding and reasoning skills.

telegram · zaihuapd · Jun 19, 02:24

**Background**: Anthropic's Mythos is a next-generation large language model that has been previewed for its advanced agentic coding and reasoning capabilities, representing a significant leap beyond the Claude Opus series. ZhiPu AI's GLM-5.2, released in June 2026, features a 1M-token context window and is designed for long agent tasks and programming. The Claude Opus line (e.g., Opus 4.7) is Anthropic's flagship reasoning model, often used as a benchmark for comparing model performance.

<details><summary>References</summary>
<ul>
<li><a href="https://techcrunch.com/2026/04/07/anthropic-mythos-ai-model-preview-security/">Anthropic debuts preview of powerful new AI model Mythos in new</a></li>
<li><a href="https://forklog.com/en/zhipu-ai-launches-glm-5-2-with-1-million-token-context/">Zhipu AI Launches GLM-5.2 with 1 Million Token Context | ForkLog</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude (language model ) - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Elon Musk replied with 'Probably Q1', interpreted as Q1 2027, while Tang Jie directly responded 'won’t take that long', asserting faster progress. The discussion shows optimism and competitive drive from both Chinese and US figures.

**Tags**: `#AI`, `#LLM`, `#ZhiPu`, `#model comparison`, `#China AI`

---

<a id="item-12"></a>
## [US pressures ASML over possible EUV tool reaching China](https://www.bloomberg.com/news/articles/2026-06-19/us-tells-asml-it-s-concerned-china-may-have-top-chip-tool) ⭐️ 8.0/10

US Commerce Secretary Lutnick recently expressed concern to ASML executives that an EUV lithography machine may have illegally reached China, violating export controls. ASML firmly denies this, stating it has never exported a complete EUV system to China and none of the 314 operational units worldwide are located there. This allegation could escalate US-EU tensions over semiconductor export controls and impact ongoing Congressional efforts to tighten restrictions on China. It also threatens the stability of global chip supply chains and the availability of advanced hardware for AI and machine learning. US officials claim to have evidence of ASML not acting in good faith, including export of EUV-related transport equipment to China, but have refused to show it. ASML has circulated documents to prove its compliance and replied that it never exported any EUV-specific components.

telegram · zaihuapd · Jun 19, 03:09

**Background**: Extreme Ultraviolet (EUV) lithography is the most advanced semiconductor manufacturing technology, essential for producing cutting-edge chips below 7nm. Due to its strategic importance, EUV systems are subject to strict export controls, with the US leading efforts to prevent China from acquiring them. The Netherlands-based ASML is the sole manufacturer of EUV lithography machines.

<details><summary>References</summary>
<ul>
<li><a href="https://www.elecfans.com/article/89/2023/202310302282517.html">什么是 EUV 光 刻 ？ EUV 与DUV 光 刻 的区别 - 制造/封装 - 电子发烧友网</a></li>

</ul>
</details>

**Tags**: `#semiconductor`, `#export control`, `#EUV lithography`, `#US-China tech war`, `#chip supply chain`

---

<a id="item-13"></a>
## [Google Imposes 24-Hour Wait for Sideloading Unverified Apps](https://t.me/zaihuapd/42054) ⭐️ 8.0/10

Google has introduced a new sideloading flow on Android requiring a 24-hour waiting period and multiple verification steps before installing apps from unverified developers. This change enhances security for Android users by adding friction to deter malicious sideloaded apps and fraud, altering the traditionally open sideloading ecosystem. The new process includes enabling developer mode, confirming the user is not coerced, restarting the device, a one-time 24-hour cooling-off period, and biometric or PIN verification before installation.

telegram · zaihuapd · Jun 19, 07:59

**Background**: Sideloading allows installing apps outside the official Google Play Store, offering flexibility but also security risks. Google has been tightening sideloading to combat fraud, and this new high-friction process aims to make it harder for scammers to trick users into installing malicious apps.

<details><summary>References</summary>
<ul>
<li><a href="https://www.androidauthority.com/google-android-sideloading-unverified-apps-new-rules-3650343/">Android's new sideloading rules are here, and they come with ...</a></li>
<li><a href="https://www.zdnet.com/article/how-google-android-sideloading-crackdown-works-limits/">Google's big Android sideloading crackdown has a 24-hour ...</a></li>

</ul>
</details>

**Tags**: `#Android`, `#sideloading`, `#security`, `#Google`, `#app installation`

---

<a id="item-14"></a>
## [Court docs: SpaceX sold shares to Chinese investors before IPO](https://www.propublica.org/article/spacex-elon-musk-ipo-foreign-investors-china) ⭐️ 8.0/10

Court documents released by ProPublica reveal that SpaceX sold shares to at least a dozen investors based in mainland China, Hong Kong, and Russia through intermediary Tomales Bay Capital between 2018 and 2021, before its recent IPO where it banned such investors. This raises serious compliance concerns with U.S. national security regulations, as SpaceX handles sensitive military projects, and could jeopardize its government contracts and reputation. Investors included businesspeople linked to Chinese military contractors and Qatari royal entities, with individual investments ranging from $800,000 to $40 million; SpaceX's valuation surged from $33.3 billion in 2019 to $2.7 trillion, yielding massive returns on early investments.

telegram · zaihuapd · Jun 19, 12:00

**Background**: SpaceX is a leading U.S. aerospace company with sensitive government contracts, including military launches. U.S. laws restrict foreign investment in defense-related firms. The company's IPO prospectus cited regulatory and compliance risks as the reason for banning Chinese and Hong Kong investors.

<details><summary>References</summary>
<ul>
<li><a href="https://www.linkedin.com/company/tomales-bay-capital">Tomales Bay Capital | LinkedIn</a></li>
<li><a href="https://raizer.app/investor/tomales-bay-capital">Tomales Bay Capital – VC Investor Profile & Insights</a></li>

</ul>
</details>

**Tags**: `#SpaceX`, `#IPO`, `#compliance`, `#national security`, `#foreign investment`

---