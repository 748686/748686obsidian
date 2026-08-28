---
layout: default
title: "Horizon Summary: 2026-07-08 (EN)"
date: 2026-07-08
lang: en
---

> From 40 items, 16 important content pieces were selected

---

1. [EU close to reviving message scanning rules](#item-1) ⭐️ 9.0/10
2. [Cloudflare Meerkat: Leaderless Async Consensus](#item-2) ⭐️ 9.0/10
3. [TypeScript 7.0 Announced with Up to 12x Speed Boost](#item-3) ⭐️ 9.0/10
4. [Critical Android remote root exploit chain disclosed](#item-4) ⭐️ 9.0/10
5. [Grok 4.5: xAI's New Model Claims High Efficiency but Faces Ethics Scrutiny](#item-5) ⭐️ 8.0/10
6. [Mistral Releases Robostral Navigate AI Model](#item-6) ⭐️ 8.0/10
7. [OpenAI Launches GPT-Live Voice Mode with GPT-5.5 Delegation](#item-7) ⭐️ 8.0/10
8. [OpenBSD use-after-free leads to local privilege escalation to root](#item-8) ⭐️ 8.0/10
9. [Anthropic's Fable Classifiers Too Zealous, Causing False Positives](#item-9) ⭐️ 8.0/10
10. [Modernizing Linux kernel cryptography API](#item-10) ⭐️ 8.0/10
11. [LingBot-Video: Sparse-MoE Video Diffusion Transformer with RL Post-Training](#item-11) ⭐️ 8.0/10
12. [Reducing drift in interactive world models with MoBA attention and self-rollout distillation](#item-12) ⭐️ 8.0/10
13. [MIIT Warns Claude Code Backdoor Exfiltrates User Data](#item-13) ⭐️ 8.0/10
14. [Top AI Companies Get Low Safety Ratings; Anthropic Leads at C+](#item-14) ⭐️ 8.0/10
15. [ByteDance releases Seedream 5.0 Pro with multilingual generation](#item-15) ⭐️ 8.0/10
16. [Researchers identify smartphone apps via EM signals with 99% accuracy](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [EU close to reviving message scanning rules](https://cyberinsider.com/eu-now-one-step-away-from-reviving-private-message-scanning-rules/) ⭐️ 9.0/10

The European Union is one step away from reviving proposed rules that would require scanning of private messages for child sexual abuse material, threatening the future of end-to-end encryption. If enacted, these rules could undermine privacy and encryption across the EU, affecting hundreds of millions of users and setting a dangerous precedent for mass surveillance. The proposal, known as Chat Control, has two versions: Chat Control 1.0 allows voluntary scanning by platforms, while Chat Control 2.0 mandates scanning and effectively bans end-to-end encryption.

hackernews · ggirelli · Jul 8, 16:53 · [Discussion](https://news.ycombinator.com/item?id=48834296)

**Background**: The EU's Chat Control regulation, formally the Child Sexual Abuse Regulation (CSAR), was proposed in May 2022 to combat child sexual abuse material. Critics argue that client-side scanning—checking content before encryption—would break encryption and enable mass surveillance of private communications.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chat_Control">Chat Control - Wikipedia</a></li>
<li><a href="https://edri.org/our-work/chat-control-what-is-actually-going-on/">Chat Control: What is actually going on? - European Digital Rights (EDRi)</a></li>
<li><a href="https://fightchatcontrol.eu/">Fight Chat Control - Protect Digital Privacy in the EU</a></li>

</ul>
</details>

**Discussion**: Community comments express strong concerns about the persistent nature of this legislation, with one user likening it to 'Terminator legislation' that will keep returning. Another user advises EU citizens to contact representatives via fightchatcontrol.eu, while others distinguish between voluntary and mandatory scanning versions.

**Tags**: `#privacy`, `#EU regulation`, `#surveillance`, `#encryption`, `#security`

---

<a id="item-2"></a>
## [Cloudflare Meerkat: Leaderless Async Consensus](https://blog.cloudflare.com/meerkat-introduction/) ⭐️ 9.0/10

Cloudflare Research introduced Meerkat, a global consensus service that uses the QuePaxa asynchronous consensus algorithm, designed for geographically distributed systems. Meerkat represents a novel production attempt at asynchronous consensus, which can make progress even under extreme network latency variability, potentially enabling strongly consistent services across global networks. The algorithm is leaderless and does not rely on timeouts, but requires global consensus for every operation, including reads, which may increase latency. It is currently an experiment and not yet in production.

hackernews · bobnamob · Jul 8, 13:18 · [Discussion](https://news.ycombinator.com/item?id=48831565)

**Background**: Traditional consensus algorithms like Paxos and Raft are partially synchronous and rely on timeouts to detect failures, which can behave poorly under high latency variability. Asynchronous consensus algorithms like QuePaxa avoid timeouts entirely, allowing progress under arbitrary message delays, but are historically difficult to implement efficiently in practice.

<details><summary>References</summary>
<ul>
<li><a href="https://blog.cloudflare.com/meerkat-introduction/">Introducing Meerkat: an experiment in global consensus</a></li>
<li><a href="https://news.ycombinator.com/item?id=48831565">Cloudflare Meerkat - Globally distributed consensus | Hacker News</a></li>

</ul>
</details>

**Discussion**: Commenters noted that comparing Meerkat to Raft is misleading since Raft is leader-based, and highlighted QuePaxa's asynchronous nature as the key innovation. Some expressed concern about the performance overhead of consensus on every read, while others saw value for challenging network conditions. There was skepticism about custom consensus implementations, but optimism that Cloudflare could succeed.

**Tags**: `#distributed consensus`, `#cloudflare`, `#meerkat`, `#asynchronous algorithms`, `#quepaxa`

---

<a id="item-3"></a>
## [TypeScript 7.0 Announced with Up to 12x Speed Boost](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) ⭐️ 9.0/10

Microsoft announced TypeScript 7.0, featuring a major compiler rewrite that delivers up to 12x faster build times across large codebases like VS Code, Sentry, and Playwright. This release dramatically reduces compilation time for TypeScript projects, which is critical for developer productivity in large-scale JavaScript/TypeScript applications. It also signals a new era of compiler performance for the ecosystem. Based on benchmarks, TypeScript 7.0 achieved 11.9x speedup on the VS Code codebase (from 125.7s to 10.6s), 8.9x on Sentry, and 8.7x on Playwright. The release also includes new language features, though details were not specified in the brief.

hackernews · DanRosenwasser · Jul 8, 16:06 · [Discussion](https://news.ycombinator.com/item?id=48833715)

**Background**: TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. The TypeScript compiler (tsc) is responsible for type checking and transpilation. Prior to version 7, the compiler had undergone incremental improvements, but this release represents a ground-up rewrite focusing on performance.

**Discussion**: The community praised the team for achieving massive speedups while maintaining compatibility. However, some users noted issues with ts-jest compatibility and called for better out-of-the-box integration with common tools. Others highlighted lingering pain points with tsconfig scoping in monorepos.

**Tags**: `#TypeScript`, `#compiler`, `#performance`, `#JavaScript`, `#Microsoft`

---

<a id="item-4"></a>
## [Critical Android remote root exploit chain disclosed](https://www.coolapk.com/feed/72700258?s=ZGQ2MTVlZjYxMDYyNTM3ZzZhNGUzOThjega1640) ⭐️ 9.0/10

Nebula Security disclosed a remote root exploit chain targeting all Android versions, combining a Firefox browser vulnerability (affecting version 151.0.2 and earlier) and a 15-year-old Linux kernel flaw (CVE-2026-43499, GhostLock), with proof-of-concept code released on GitHub. This exploit chain allows attackers to gain persistent root access on any Android device by simply tricking a user into clicking a malicious link, posing a severe security risk to billions of users and potentially leading to widespread exploitation. The attack leverages a remote code execution vulnerability in Mozilla Firefox and the GhostLock kernel flaw for privilege escalation, enabling attackers to execute arbitrary commands via ADB and implant files for persistent control.

telegram · zaihuapd · Jul 8, 13:01

**Background**: Android Debug Bridge (adb) is a command-line tool for debugging and managing Android devices, often used for development. A remote root exploit allows an attacker to gain superuser (root) access over a network. The GhostLock vulnerability is a local privilege escalation flaw in the Linux kernel that has remained undetected for 15 years.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Android_Debug_Bridge">Android Debug Bridge - Wikipedia</a></li>
<li><a href="https://thehackernews.com/2026/07/15-year-old-ghostlock-flaw-enables-root.html">15-Year-Old GhostLock Flaw Enables Root and Container Escape on Most Linux Distros</a></li>
<li><a href="https://www.hkcert.org/security-bulletin/mozilla-firefox-remote-code-execution-vulnerability_20250220">Mozilla Firefox Remote Code Execution Vulnerability</a></li>

</ul>
</details>

**Tags**: `#Android`, `#security`, `#vulnerability`, `#root`, `#exploit`

---

<a id="item-5"></a>
## [Grok 4.5: xAI's New Model Claims High Efficiency but Faces Ethics Scrutiny](https://x.ai/news/grok-4-5) ⭐️ 8.0/10

xAI has released Grok 4.5, a new AI model trained on trillions of tokens of Cursor coding data, claiming 4x better reasoning efficiency than Opus and competitive benchmark performance at a lower price. This release intensifies competition in the AI model market, especially for pricing and efficiency, but raises trust issues due to xAI's reported political bias and ethical concerns, potentially affecting enterprise adoption. Grok 4.5 is priced at $2/$6 per million tokens, compared to GPT-5.4 at $2.5/$15 and Opus 4.8 at $5/$25, and is benchmarked around Opus 4.7 level. Training included Cursor user interaction data.

hackernews · BoumTAC · Jul 8, 18:00 · [Discussion](https://news.ycombinator.com/item?id=48835111)

**Background**: Grok is an AI chatbot developed by xAI, Elon Musk's company. Previous versions include Grok 2.5 and Grok 3. The model aims for truth-seeking but has faced criticism over content moderation and political bias. The use of proprietary coding data from Cursor is a notable training approach.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Grok_(chatbot)">Grok (chatbot) - Wikipedia</a></li>
<li><a href="https://docs.x.ai/developers/models">Models | SpaceXAI Docs</a></li>

</ul>
</details>

**Discussion**: Commenters express skepticism about trusting xAI due to ethical issues like CSAM tolerance and political manipulation, though some acknowledge the model's efficiency and competitive pricing. Others question the economic viability of investing billions for the third-best model.

**Tags**: `#AI`, `#ethics`, `#Grok`, `#model release`, `#controversy`

---

<a id="item-6"></a>
## [Mistral Releases Robostral Navigate AI Model](https://mistral.ai/news/robostral-navigate/) ⭐️ 8.0/10

Mistral AI released Robostral Navigate, an 8B parameter model that enables robots to navigate complex environments using only a single RGB camera and language prompts, achieving 76.6% success on unseen R2R-CE benchmarks. This is significant because it demonstrates map-less navigation, solving the 'kidnapped robot' problem, and outperforms multi-sensor approaches with a simpler setup, potentially enabling wider adoption in hobbyist and commercial robotics. The model is not openly available; it uses only a single camera without pre-captured maps. It achieves state-of-the-art results on the R2R-CE benchmark.

hackernews · ottomengis · Jul 8, 14:09 · [Discussion](https://news.ycombinator.com/item?id=48832212)

**Background**: Map-less navigation is challenging because robots traditionally need a pre-built map to localize and navigate. The 'kidnapped robot' problem refers to a robot being placed in an unknown location without a map. Mistral's model uses deep learning to follow natural language directions from visual input alone.

<details><summary>References</summary>
<ul>
<li><a href="https://mistral.ai/news/robostral-navigate/">Robostral Navigate: single-camera AI navigation | Mistral AI</a></li>
<li><a href="https://www.bloomberg.com/news/articles/2026-07-08/mistral-ai-releases-robotics-model-to-support-physical-ai-push">Mistral AI Releases Robotics Model to Support Physical AI Push - Bloomberg</a></li>
<li><a href="https://news.ycombinator.com/item?id=48832212">Mistral's Robostral Navigate: a state of the art robotics navigation model | Hacker News</a></li>

</ul>
</details>

**Discussion**: Commenters are impressed by the map-less capability and discuss hobbyist applications like connecting it to OpenClaw for farm robots. Some note that while map-less outdoor navigation exists, indoor map-less navigation is relatively new. Privacy concerns are raised regarding geo-localization tech.

**Tags**: `#robotics`, `#navigation`, `#AI`, `#mistral`, `#deep learning`

---

<a id="item-7"></a>
## [OpenAI Launches GPT-Live Voice Mode with GPT-5.5 Delegation](https://openai.com/index/introducing-gpt-live/) ⭐️ 8.0/10

OpenAI has announced GPT-Live, a new voice mode that can delegate complex queries to GPT-5.5 for more advanced responses, as revealed in an official blog post. The feature aims to bridge the gap between voice assistants and frontier AI models. GPT-Live significantly enhances voice interactions by enabling real-time delegation to the latest model, making voice assistants far more capable. This could transform how users brainstorm, work, and communicate hands-free, potentially setting a new standard for AI voice interfaces. According to early access user simonw, GPT-Live allowed a full hour of conversation without restriction to an older voice model, though it had a bug where it interrupted and laughed at unintended cues. The delegation feature works in the background, so users are no longer limited to a voice model that is several years behind the frontier.

hackernews · logickkk1 · Jul 8, 17:03 · [Discussion](https://news.ycombinator.com/item?id=48834405)

**Background**: GPT-Live is a voice mode that lets users speak naturally and get responses from GPT-5.5, OpenAI's most advanced model. Previous voice modes used smaller, specialized models that lacked the full reasoning power of text-based GPT. This delegation approach combines low-latency speech recognition with the high intelligence of frontier models.

**Discussion**: Early access user simonw praised the feature for enabling long, productive conversations, but noted a bug involving unintended interruptions. Some commenters, like jonstaab, expressed ethical concerns about replacing human relationships, while artdigital criticized the lack of tool/connector support in voice mode across all frontier assistants.

**Tags**: `#AI`, `#voice mode`, `#OpenAI`, `#GPT-5.5`

---

<a id="item-8"></a>
## [OpenBSD use-after-free leads to local privilege escalation to root](https://nvd.nist.gov/vuln/detail/cve-2026-57589) ⭐️ 8.0/10

A use-after-free vulnerability (CVE-2026-57589) has been discovered in OpenBSD, allowing a local attacker to escalate privileges to root. This vulnerability is significant because OpenBSD is renowned for its security focus, and a local privilege escalation bug could undermine that reputation. It affects all systems running the vulnerable version. The vulnerability was discovered as part of the 'Patch The Planet' initiative by OpenAI and Trail of Bits. Details are currently limited; the OpenBSD security page does not yet list it.

hackernews · linggen · Jul 8, 13:24 · [Discussion](https://news.ycombinator.com/item?id=48831658)

**Background**: OpenBSD is a free, Unix-like operating system focused on security and correctness. Local privilege escalation is an attack where a user with limited access gains higher privileges, such as root, by exploiting a software flaw.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/OpenBSD">OpenBSD</a></li>
<li><a href="https://en.wikipedia.org/wiki/Local_privilege_escalation">Local privilege escalation</a></li>

</ul>
</details>

**Discussion**: Comments highlight that the bug was found via AI-assisted vulnerability hunting, praise OpenBSD's strong security record, and question why it's not yet on the official OpenBSD security page. Some express curiosity about how many more vulnerabilities might be discovered by similar projects.

**Tags**: `#openbsd`, `#security`, `#vulnerability`, `#CVE`, `#privilege-escalation`

---

<a id="item-9"></a>
## [Anthropic's Fable Classifiers Too Zealous, Causing False Positives](https://combine-lab.github.io/blog/2026/07/07/fable-is-not-a-useful-model.html) ⭐️ 8.0/10

Anthropic's safety classifiers for its Fable model are overly sensitive, frequently flagging benign requests as violations and downgrading them to a less capable model, causing frustration among users. This undermines the utility of Fable for legitimate tasks like code review or data analysis, and raises serious privacy concerns due to Anthropic's policy of retaining flagged inputs and outputs for up to two years. The classifiers seem to overreact to terms related to cybersecurity, biology, or jailbreaking, often passing requests to Opus 4.8 even for trivial topics; users report that even medical physics questions get waved off.

hackernews · karrot-kake · Jul 8, 20:41 · [Discussion](https://news.ycombinator.com/item?id=48837162)

**Background**: Fable is a powerful AI model from Anthropic, designed to be used with safety classifiers that aim to prevent misuse. However, these classifiers can flag benign requests, triggering data retention policies that keep user inputs and outputs for up to two years for safety analysis.

**Discussion**: Users share real-world examples: one asked for code review on a private repo and was flagged, another couldn't get medical physics questions answered. There's frustration that the classifiers are useless for genuine technical work, and concern about privacy with high false-positive rates.

**Tags**: `#AI safety`, `#classifiers`, `#censorship`, `#Anthropic`, `#Fable`

---

<a id="item-10"></a>
## [Modernizing Linux kernel cryptography API](https://lwn.net/Articles/1077427/) ⭐️ 8.0/10

At the 2026 Linux Security Summit North America, Eric Biggers presented ongoing efforts to replace the traditional Linux kernel crypto API with new library APIs that are safer and simpler to use. This modernization reduces complexity and potential security bugs in kernel cryptography, benefiting all kernel subsystems that rely on encryption, hashing, and authentication. The traditional crypto API, introduced in 2002, has become complex, slow, and poorly optimized for modern CPU-based acceleration, leading to maintenance and performance issues.

rss · LWN.net · Jul 8, 13:14

**Background**: The Linux kernel crypto API is a framework providing standardized interfaces for cryptographic algorithms such as ciphers, hashes, and message authentication codes. It has been part of the kernel since version 2.5.45 but its design has become outdated, prompting efforts to adopt library APIs for safer and more efficient crypto operations.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Linux_kernel_crypto_API">Linux kernel crypto API</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#cryptography`, `#security`, `#API design`, `#LSS NA`

---

<a id="item-11"></a>
## [LingBot-Video: Sparse-MoE Video Diffusion Transformer with RL Post-Training](https://www.reddit.com/r/MachineLearning/comments/1ur0bxq/lingbotvideo_sparsemoe_video_diffusion/) ⭐️ 8.0/10

LingBot-Video is a 13B parameter sparse-MoE video diffusion transformer (1.4B active) that has been post-trained with reinforcement learning using six rewards, including a physical-plausibility reward, and supports action-conditioned world model prediction for robot rollouts. This work advances video generation and world modeling by combining sparse MoE for efficiency, RL post-training for improved plausibility, and open release of weights and code, making it a strong candidate for robotics and video synthesis research. The model uses a DeepSeek-V3-style sparse MoE with 128 experts and top-8 routing, achieving top average performance on RBench but ranking second on general text-to-video. The physical-plausibility reward is judged by a VLM, which raises concerns about reward hacking despite adding real-video negatives.

reddit · r/MachineLearning · /u/Savings-Display5123 · Jul 8, 17:58

**Background**: Diffusion transformers (DiTs) replace convolutional U-Net backbones with transformer architectures for denoising in generative models. Sparse mixture of experts (MoE) activates only a subset of parameters per forward pass, enabling larger model capacity with lower computational cost. Reinforcement learning from reward models can fine-tune generative models for specific objectives, such as physical plausibility.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Sparse_mixture-of-experts">Sparse mixture-of-experts</a></li>
<li><a href="https://en.wikipedia.org/wiki/Diffusion_Transformer">Diffusion Transformer</a></li>
<li><a href="https://en.wikipedia.org/wiki/SGLang">SGLang</a></li>

</ul>
</details>

**Tags**: `#video generation`, `#world models`, `#sparse MoE`, `#diffusion transformers`, `#reinforcement learning`

---

<a id="item-12"></a>
## [Reducing drift in interactive world models with MoBA attention and self-rollout distillation](https://www.reddit.com/r/MachineLearning/comments/1ur4hkc/reducing_drift_in_interactive_worldmodel_rollouts/) ⭐️ 8.0/10

Researchers at LingBot World have released an open-weights interactive world model that uses a MoBA attention mask (mixing bidirectional and autoregressive attention) and post-training distillation over long self-rollout trajectories to significantly reduce drift, demonstrated by a continuous 60-minute stable rollout. This work addresses a critical challenge in interactive world models—drift accumulation during long rollouts—which has limited their practical usability. The combination of MoBA attention and long-rollout distillation could enable more stable and reliable interactive simulations for applications like video games, robotics, and virtual environments. The MoBA attention mask dynamically schedules KV-cache to keep long rollouts tractable, and the model uses Plücker embeddings plus AdaLN for camera control. A limitation is that persistence is only in appearance, not identity, meaning regions leaving the context window are regenerated on revisit, not recalled. The weights are released under CC-BY-NC-SA license.

reddit · r/MachineLearning · /u/Purple-Low-2779 · Jul 8, 20:23

**Background**: Interactive world models generate video frames conditioned on user input, essentially serving as a learned simulator. A common problem is drift: as the model autoregressively generates new frames based on its own previous outputs, small errors accumulate, causing the simulation to diverge from plausible reality over time. Existing methods often use teacher forcing during training, where the model sees ground-truth frames, but this does not translate to stable self-rollouts during inference.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/html/2604.03118v2">Self-Consistent Distribution Matching with Cache-Aware Training for Fast ...</a></li>
<li><a href="https://huggingface.co/papers/2604.03118">Self-Consistent Distribution Matching with Cache-Aware Training for Fast ...</a></li>

</ul>
</details>

**Tags**: `#world models`, `#drift reduction`, `#attention mechanisms`, `#distillation`, `#video generation`

---

<a id="item-13"></a>
## [MIIT Warns Claude Code Backdoor Exfiltrates User Data](https://nvdb.org.cn/publicAnnouncement/2074681830578630657) ⭐️ 8.0/10

China's Ministry of Industry and Information Technology (MIIT) issued a risk notice on July 8, 2025, warning that Claude Code versions 2.1.91 through 2.1.196 contain a backdoor that secretly transmits users' location and identity information to remote servers without consent. This is significant because Claude Code is a widely used AI coding tool, and the backdoor compromises the privacy and security of many developers. The authoritative warning from a government body like MIIT underscores the severity of the threat and may prompt organizations to reassess their use of AI tools in development pipelines. The affected versions span from 2.1.91 to 2.1.196, and the backdoor includes a built-in monitoring mechanism that exfiltrates sensitive data. Users are advised to immediately check, uninstall the vulnerable versions, or upgrade to the latest secure version that has removed the malicious code, and to strengthen outbound permission controls and traffic monitoring for development tools.

telegram · zaihuapd · Jul 8, 06:09

**Background**: Claude Code is an AI-assisted software development tool built by Anthropic, based on its Claude large language model family. It helps developers with coding tasks such as writing, debugging, and reviewing code. The tool is widely used in the industry, making the discovery of a backdoor that secretly sends user data particularly concerning.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>

</ul>
</details>

**Tags**: `#security`, `#claude-code`, `#backdoor`, `#ai-tools`, `#vulnerability`

---

<a id="item-14"></a>
## [Top AI Companies Get Low Safety Ratings; Anthropic Leads at C+](http://z.ai/) ⭐️ 8.0/10

The Future of Life Institute released a report rating nine top AI companies on safety, with none receiving an A grade. Anthropic earned the highest score of C+, while OpenAI and Google DeepMind received C, Meta got D+, and DeepSeek, xAI, and others received F. This report highlights a critical gap in AI safety governance as companies rapidly develop transformative AI without robust risk management plans. It underscores the need for stronger safety standards and transparency in the industry. The report notes that many companies have shifted from banning military use of their AI to actively seeking defense partnerships. Chinese companies Z.ai and Alibaba Cloud deny allegations of military ties, but were still rated low.

telegram · zaihuapd · Jul 8, 11:30

**Background**: The Future of Life Institute (FLI) is a nonprofit founded in 2014 to steer transformative technologies away from large-scale risks, focusing on existential AI risk. The institute's report evaluates companies on criteria such as risk assessment, transparency, and accountability. Z.ai is a Chinese AI company known for its GLM models and was blacklisted by the US in 2025. DeepSeek is a Chinese AI company founded in 2023, notable for low-cost, high-performance models like DeepSeek-R1.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Future_of_Life_Institute">Future of Life Institute</a></li>
<li><a href="https://en.wikipedia.org/wiki/Z.ai">Z.ai</a></li>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></li>

</ul>
</details>

**Tags**: `#AI safety`, `#AI ethics`, `#industry report`, `#AI governance`

---

<a id="item-15"></a>
## [ByteDance releases Seedream 5.0 Pro with multilingual generation](https://seed.bytedance.com/en/seedream5_0_pro) ⭐️ 8.0/10

ByteDance's Seed team released Seedream 5.0 Pro, a multimodal image generation model featuring high-density infographics, interactive editing, photorealistic quality, and native multilingual generation. This release advances AI image generation by combining precise editing with multilingual text support, enabling more practical applications in education, international marketing, and content creation. The model supports spatial annotation and hand-drawn sketch editing with layer separation, can generate text in over ten languages, and achieves photorealistic rendering of natural lighting, shadows, and skin textures.

telegram · zaihuapd · Jul 8, 15:11

**Background**: Multimodal image generation models create images from text prompts, often with the ability to include rendered text. Earlier models struggled with accurate multilingual text rendering and precise editing. Seedream 5.0 Pro improves on both fronts, targeting professional and international use cases.

**Tags**: `#ByteDance`, `#multimodal`, `#image generation`, `#AI`, `#Seedream`

---

<a id="item-16"></a>
## [Researchers identify smartphone apps via EM signals with 99% accuracy](https://www.scmp.com/news/china/science/article/3359688/chinese-researchers-find-peephole-any-smartphone-its-leaked-radio-signal) ⭐️ 8.0/10

Chinese researchers developed a non-contact forensic technique that identifies smartphone apps and operations by analyzing leaked low-frequency electromagnetic signals, achieving up to 99.07% accuracy on devices like iPhone 15 Pro, Xiaomi 15 Pro, and OPPO Reno 13. This attack method poses a serious privacy threat because it can work even when the phone is offline, in airplane mode, encrypted, or locked, without any access to the device's system or stored data. The technique analyzes low-frequency electromagnetic (EM) signals emitted by a running smartphone's components, and the researchers tested it on popular apps including TikTok, WeChat video calls, Baidu Maps, SMS, browser, camera, and cloud storage.

telegram · zaihuapd · Jul 8, 16:05

**Background**: All electronic devices emit electromagnetic radiation during operation, and these unintentional signals can reveal information about the device's activity. This is known as a side-channel attack, where an attacker exploits physical byproducts like EM leakage, power consumption, or sound. Previous side-channel attacks often required physical access or specialized equipment, but this new technique is non-contact and works over distance.

**Tags**: `#security`, `#privacy`, `#electromagnetic signals`, `#smartphone`, `#side-channel attack`

---