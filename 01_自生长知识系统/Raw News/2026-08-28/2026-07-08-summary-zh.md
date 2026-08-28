---
layout: default
title: "Horizon Summary: 2026-07-08 (ZH)"
date: 2026-07-08
lang: zh
---

> 从 40 条内容中筛选出 16 条重要资讯。

---

1. [欧盟即将重启消息扫描规则](#item-1) ⭐️ 9.0/10
2. [Cloudflare Meerkat：无领导者异步共识算法](#item-2) ⭐️ 9.0/10
3. [TypeScript 7.0 发布，速度提升高达 12 倍](#item-3) ⭐️ 9.0/10
4. [安卓全版本远程 Root 攻击链曝光](#item-4) ⭐️ 9.0/10
5. [Grok 4.5：xAI 新模型宣称高效率但面临伦理质疑](#item-5) ⭐️ 8.0/10
6. [Mistral 发布 Robostral Navigate AI 模型](#item-6) ⭐️ 8.0/10
7. [OpenAI 推出可委托 GPT-5.5 的 GPT-Live 语音模式](#item-7) ⭐️ 8.0/10
8. [OpenBSD 释放后使用漏洞导致本地权限提升至 root](#item-8) ⭐️ 8.0/10
9. [Anthropic 的 Fable 分类器过于敏感，导致误报](#item-9) ⭐️ 8.0/10
10. [Linux 内核密码学 API 现代化](#item-10) ⭐️ 8.0/10
11. [LingBot-Video：经强化学习后训练的稀疏 MoE 视频扩散 Transformer](#item-11) ⭐️ 8.0/10
12. [交互世界模型漂移减少：MoBA 与自滚动蒸馏](#item-12) ⭐️ 8.0/10
13. [工信部警告 Claude Code 后门泄露用户数据](#item-13) ⭐️ 8.0/10
14. [顶尖 AI 企业安全评级低，Anthropic 以 C+领先](#item-14) ⭐️ 8.0/10
15. [字节跳动发布 Seedream 5.0 Pro，支持多语言生成](#item-15) ⭐️ 8.0/10
16. [研究人员通过电磁信号识别手机应用，准确率达 99%](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [欧盟即将重启消息扫描规则](https://cyberinsider.com/eu-now-one-step-away-from-reviving-private-message-scanning-rules/) ⭐️ 9.0/10

欧盟距离重启一项要求扫描私人消息以查找儿童性虐待素材的提案仅一步之遥，这对端到端加密的未来构成威胁。 如果该规则得以实施，可能会破坏整个欧盟的隐私和加密保护，影响数亿用户，并为大规模监控树立危险先例。 该提案被称为“聊天控制”，包含两个版本：聊天控制 1.0 允许平台自愿扫描，而聊天控制 2.0 强制要求扫描并实际上禁止端到端加密。

hackernews · ggirelli · 7月8日 16:53 · [社区讨论](https://news.ycombinator.com/item?id=48834296)

**背景**: 欧盟的“聊天控制”法规，正式名称为《儿童性虐待法规》（CSAR），于 2022 年 5 月提出，旨在打击儿童性虐待素材。批评者认为，客户端扫描（在加密前检查内容）将破坏加密，并使得对私人通信进行大规模监控成为可能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Chat_Control">Chat Control - Wikipedia</a></li>
<li><a href="https://edri.org/our-work/chat-control-what-is-actually-going-on/">Chat Control: What is actually going on? - European Digital Rights (EDRi)</a></li>
<li><a href="https://fightchatcontrol.eu/">Fight Chat Control - Protect Digital Privacy in the EU</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了对该立法持续存在的强烈担忧，有用户将其比作会不断卷土重来的“终结者式立法”。另一名用户建议欧盟公民通过 fightchatcontrol.eu 联系代表，还有用户区分了自愿扫描和强制扫描的不同版本。

**标签**: `#privacy`, `#EU regulation`, `#surveillance`, `#encryption`, `#security`

---

<a id="item-2"></a>
## [Cloudflare Meerkat：无领导者异步共识算法](https://blog.cloudflare.com/meerkat-introduction/) ⭐️ 9.0/10

Cloudflare Research 推出了 Meerkat，这是一个全球共识服务，采用 QuePaxa 异步共识算法，专为地理分布式系统设计。 Meerkat 代表了异步共识在生产环境中的一次全新尝试，即使在极端网络延迟波动下也能取得进展，有望在全球网络中实现强一致性的服务。 该算法无领导者且不依赖超时，但每个操作（包括读取）都需要全局共识，这可能增加延迟。目前它仍是一个实验，尚未投入生产。

hackernews · bobnamob · 7月8日 13:18 · [社区讨论](https://news.ycombinator.com/item?id=48831565)

**背景**: 传统的共识算法如 Paxos 和 Raft 是部分同步的，依赖超时来检测故障，在高延迟波动下表现不佳。像 QuePaxa 这样的异步共识算法完全避免使用超时，允许在任意消息延迟下取得进展，但历来在实际中难以高效实现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.cloudflare.com/meerkat-introduction/">Introducing Meerkat: an experiment in global consensus</a></li>
<li><a href="https://news.ycombinator.com/item?id=48831565">Cloudflare Meerkat - Globally distributed consensus | Hacker News</a></li>

</ul>
</details>

**社区讨论**: 评论者指出，将 Meerkat 与 Raft 比较具有误导性，因为 Raft 是基于领导者的，并强调 QuePaxa 的异步特性是核心创新。一些人担心每次读取都需共识的性能开销，而另一些人则认为在挑战性网络条件下具有价值。人们对自定义共识实现持怀疑态度，但对 Cloudflare 能够成功持乐观态度。

**标签**: `#distributed consensus`, `#cloudflare`, `#meerkat`, `#asynchronous algorithms`, `#quepaxa`

---

<a id="item-3"></a>
## [TypeScript 7.0 发布，速度提升高达 12 倍](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) ⭐️ 9.0/10

微软发布了 TypeScript 7.0，其编译器经过重大重写，在 VS Code、Sentry 和 Playwright 等大型代码库上实现了高达 12 倍的构建速度提升。 此版本大幅减少了 TypeScript 项目的编译时间，对于大型 JavaScript/TypeScript 应用程序的开发者生产力至关重要。这也标志着 TypeScript 生态系统编译器性能的新时代。 根据基准测试，TypeScript 7.0 在 VS Code 代码库上实现了 11.9 倍加速（从 125.7 秒降至 10.6 秒），在 Sentry 上达到 8.9 倍，在 Playwright 上达到 8.7 倍。该版本还包含新的语言功能，但未在摘要中详细说明。

hackernews · DanRosenwasser · 7月8日 16:06 · [社区讨论](https://news.ycombinator.com/item?id=48833715)

**背景**: TypeScript 是 JavaScript 的类型化超集，编译为纯 JavaScript。TypeScript 编译器（tsc）负责类型检查和转译。在 7.0 版本之前，编译器经历了渐进式改进，但此版本代表了专注于性能的从头重写。

**社区讨论**: 社区赞扬团队在保持兼容性的同时实现了巨大的速度提升。然而，一些用户指出与 ts-jest 的兼容性问题，并呼吁更好地与常用工具开箱即用集成。其他用户则强调了 monorepo 中 tsconfig 作用域配置的老大难问题。

**标签**: `#TypeScript`, `#compiler`, `#performance`, `#JavaScript`, `#Microsoft`

---

<a id="item-4"></a>
## [安卓全版本远程 Root 攻击链曝光](https://www.coolapk.com/feed/72700258?s=ZGQ2MTVlZjYxMDYyNTM3ZzZhNGUzOThjega1640) ⭐️ 9.0/10

Nebula Security 曝光了一条针对所有安卓版本的远程 Root 攻击链，该链结合了 Firefox 浏览器漏洞（影响 151.0.2 及更早版本）和一个存在 15 年的 Linux 内核漏洞（CVE-2026-43499，GhostLock），概念验证代码已发布在 GitHub 上。 该攻击链只需诱骗用户点击恶意链接即可在任何安卓设备上获得持久 Root 权限，对数十亿用户构成严重安全风险，可能导致大规模利用。 该攻击利用 Mozilla Firefox 中的远程代码执行漏洞和 GhostLock 内核提权漏洞，使攻击者能够通过 ADB 执行任意命令并植入文件以实现持久控制。

telegram · zaihuapd · 7月8日 13:01

**背景**: Android Debug Bridge (adb) 是一种用于调试和管理安卓设备的命令行工具，常用于开发。远程 Root 漏洞使攻击者能通过网络获得超级用户（Root）权限。GhostLock 漏洞是 Linux 内核中的一个本地提权漏洞，已潜伏 15 年未被发现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Android_Debug_Bridge">Android Debug Bridge - Wikipedia</a></li>
<li><a href="https://thehackernews.com/2026/07/15-year-old-ghostlock-flaw-enables-root.html">15-Year-Old GhostLock Flaw Enables Root and Container Escape on Most Linux Distros</a></li>
<li><a href="https://www.hkcert.org/security-bulletin/mozilla-firefox-remote-code-execution-vulnerability_20250220">Mozilla Firefox Remote Code Execution Vulnerability</a></li>

</ul>
</details>

**标签**: `#Android`, `#security`, `#vulnerability`, `#root`, `#exploit`

---

<a id="item-5"></a>
## [Grok 4.5：xAI 新模型宣称高效率但面临伦理质疑](https://x.ai/news/grok-4-5) ⭐️ 8.0/10

xAI 发布了新 AI 模型 Grok 4.5，该模型使用来自 Cursor 的万亿级 token 编码数据训练，声称推理效率比 Opus 高 4 倍，且基准测试表现具有竞争力，价格更低。 此发布加剧了 AI 模型市场的竞争，特别是在定价和效率方面，但由于 xAI 被报道的政治偏见和伦理问题，引发了信任危机，可能影响企业采用。 Grok 4.5 的定价为每百万 token $2/$6，相比之下 GPT-5.4 为$2.5/$15，Opus 4.8 为$5/$25，基准测试水平约为 Opus 4.7。训练数据包含了 Cursor 用户交互数据。

hackernews · BoumTAC · 7月8日 18:00 · [社区讨论](https://news.ycombinator.com/item?id=48835111)

**背景**: Grok 是 xAI（埃隆·马斯克的公司）开发的 AI 聊天机器人。先前版本包括 Grok 2.5 和 Grok 3。该模型旨在追求真相，但因其内容审核和政治偏见问题受到批评。使用来自 Cursor 的专有编码数据进行训练是一种值得注意的训练方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Grok_(chatbot)">Grok (chatbot) - Wikipedia</a></li>
<li><a href="https://docs.x.ai/developers/models">Models | SpaceXAI Docs</a></li>

</ul>
</details>

**社区讨论**: 评论者因 CSAM 容忍和政治操纵等伦理问题对信任 xAI 表示怀疑，尽管一些人承认该模型的效率和具有竞争力的定价。还有人对投入数十亿美元打造第三佳模型的经济可行性提出质疑。

**标签**: `#AI`, `#ethics`, `#Grok`, `#model release`, `#controversy`

---

<a id="item-6"></a>
## [Mistral 发布 Robostral Navigate AI 模型](https://mistral.ai/news/robostral-navigate/) ⭐️ 8.0/10

Mistral AI 发布了 Robostral Navigate，这是一个 8B 参数的模型，仅使用单颗 RGB 摄像头和语言指令就能让机器人在复杂环境中导航，在未见过的 R2R-CE 基准测试中达到 76.6% 的成功率。 这很重要，因为它展示了无地图导航能力，解决了“绑架机器人”问题，并以更简单的设置超越了多传感器方法，有望在爱好者和商业机器人领域得到更广泛的应用。 该模型未公开可用；它仅使用单个摄像头，无需预先获取地图。它在 R2R-CE 基准测试上达到了最先进的结果。

hackernews · ottomengis · 7月8日 14:09 · [社区讨论](https://news.ycombinator.com/item?id=48832212)

**背景**: 无地图导航很具挑战性，因为传统上机器人需要预先构建的地图来定位和导航。“绑架机器人”问题指的是机器人被放置在没有地图的未知位置。Mistral 的模型仅通过视觉输入，利用深度学习来遵循自然语言指令。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://mistral.ai/news/robostral-navigate/">Robostral Navigate: single-camera AI navigation | Mistral AI</a></li>
<li><a href="https://www.bloomberg.com/news/articles/2026-07-08/mistral-ai-releases-robotics-model-to-support-physical-ai-push">Mistral AI Releases Robotics Model to Support Physical AI Push - Bloomberg</a></li>
<li><a href="https://news.ycombinator.com/item?id=48832212">Mistral's Robostral Navigate: a state of the art robotics navigation model | Hacker News</a></li>

</ul>
</details>

**社区讨论**: 评论者对无地图能力印象深刻，并讨论了将其连接到 OpenClaw 用于农场机器人等爱好者应用。一些人指出，虽然室外无地图导航已经存在，但室内无地图导航相对较新。还提出了关于地理定位技术的隐私担忧。

**标签**: `#robotics`, `#navigation`, `#AI`, `#mistral`, `#deep learning`

---

<a id="item-7"></a>
## [OpenAI 推出可委托 GPT-5.5 的 GPT-Live 语音模式](https://openai.com/index/introducing-gpt-live/) ⭐️ 8.0/10

OpenAI 宣布推出 GPT-Live 新语音模式，该模式可将复杂查询委托给 GPT-5.5 以获得更先进的回复，官方博客文章已公布。此功能旨在弥合语音助手与前沿 AI 模型之间的差距。 GPT-Live 通过实时委托给最新模型，显著增强了语音交互能力，使语音助手更加强大。这可能会改变用户免提进行头脑风暴、工作和交流的方式，有望为 AI 语音界面树立新标准。 据早期访问用户 simonw 称，GPT-Live 支持长达一小时的对话，不再受限于老旧的语音模型，但存在一个 bug，即会打断用户并对非预期的提示发笑。委托功能在后台运行，用户不再受限于落后前沿数年的语音模型。

hackernews · logickkk1 · 7月8日 17:03 · [社区讨论](https://news.ycombinator.com/item?id=48834405)

**背景**: GPT-Live 是一种语音模式，允许用户自然说话并从 GPT-5.5（OpenAI 最先进的模型）获得回复。之前的语音模式使用较小的专用模型，缺乏基于文本的 GPT 的全部推理能力。这种委托方法结合了低延迟语音识别与前沿模型的高智能。

**社区讨论**: 早期访问用户 simonw 称赞该功能支持长时间的生产性对话，但指出存在意外打断的 bug。一些评论者如 jonstaab 表达了对替代人际关系的伦理担忧，而 artdigital 则批评所有前沿助手在语音模式中缺乏工具/连接器支持。

**标签**: `#AI`, `#voice mode`, `#OpenAI`, `#GPT-5.5`

---

<a id="item-8"></a>
## [OpenBSD 释放后使用漏洞导致本地权限提升至 root](https://nvd.nist.gov/vuln/detail/cve-2026-57589) ⭐️ 8.0/10

在 OpenBSD 中发现了一个释放后使用漏洞（CVE-2026-57589），允许本地攻击者将权限提升至 root。 该漏洞意义重大，因为 OpenBSD 以其安全特性著称，本地权限提升漏洞可能损害其声誉。所有运行受影响版本的系统都会受到影响。 该漏洞是由 OpenAI 和 Trail of Bits 发起的 'Patch The Planet' 项目发现的。目前细节有限，OpenBSD 安全页面尚未列出该漏洞。

hackernews · linggen · 7月8日 13:24 · [社区讨论](https://news.ycombinator.com/item?id=48831658)

**背景**: OpenBSD 是一个注重安全性和正确性的自由类 Unix 操作系统。本地权限提升是指拥有有限访问权限的用户通过利用软件缺陷获得更高权限（如 root）的攻击方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/OpenBSD">OpenBSD</a></li>
<li><a href="https://en.wikipedia.org/wiki/Local_privilege_escalation">Local privilege escalation</a></li>

</ul>
</details>

**社区讨论**: 评论指出该漏洞是通过人工智能辅助的漏洞挖掘发现的，赞扬了 OpenBSD 良好的安全记录，并质疑为何该漏洞尚未出现在官方安全页面。一些人好奇类似项目还可能发现多少漏洞。

**标签**: `#openbsd`, `#security`, `#vulnerability`, `#CVE`, `#privilege-escalation`

---

<a id="item-9"></a>
## [Anthropic 的 Fable 分类器过于敏感，导致误报](https://combine-lab.github.io/blog/2026/07/07/fable-is-not-a-useful-model.html) ⭐️ 8.0/10

这削弱了 Fable 在代码审查或数据分析等合法任务中的实用性，并且由于 Anthropic 对被标记的输入输出保留长达两年的政策，引发了严重的隐私担忧。 分类器似乎对涉及网络安全、生物学或越狱的术语反应过度，即使是微不足道的话题也常常将请求传递给 Opus 4.8；用户报告称，甚至医学物理问题也被拒绝。

hackernews · karrot-kake · 7月8日 20:41 · [社区讨论](https://news.ycombinator.com/item?id=48837162)

**背景**: Fable 是 Anthropic 开发的一款强大 AI 模型，其设计配合了旨在防止滥用的安全分类器。然而，这些分类器可能标记良性请求，从而触发数据保留政策，将用户的输入和输出保留长达两年以供安全分析。

**社区讨论**: 用户分享了真实案例：有人请求审查私有代码仓库却被标记，另有人无法回答医学物理问题。用户对分类器在真正技术工作中毫无用处感到沮丧，并对高误报率下的隐私问题表示担忧。

**标签**: `#AI safety`, `#classifiers`, `#censorship`, `#Anthropic`, `#Fable`

---

<a id="item-10"></a>
## [Linux 内核密码学 API 现代化](https://lwn.net/Articles/1077427/) ⭐️ 8.0/10

在 2026 年北美 Linux 安全峰会上，Eric Biggers 介绍了正在进行的将传统 Linux 内核密码学 API 替换为更安全、更易使用的新库 API 的工作。 这一现代化改造降低了内核密码学的复杂性和潜在安全漏洞，惠及所有依赖加密、哈希和认证的内核子系统。 自 2002 年引入的传统密码学 API 已变得复杂、缓慢，且未能针对现代基于 CPU 的加速进行优化，导致维护和性能问题。

rss · LWN.net · 7月8日 13:14

**背景**: Linux 内核密码学 API 是一个为加密算法（如密码、哈希和消息认证码）提供标准化接口的框架。自内核 2.5.45 版本以来一直存在，但其设计已过时，因此推动了采用库 API 以实现更安全、更高效的密码学操作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Linux_kernel_crypto_API">Linux kernel crypto API</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#cryptography`, `#security`, `#API design`, `#LSS NA`

---

<a id="item-11"></a>
## [LingBot-Video：经强化学习后训练的稀疏 MoE 视频扩散 Transformer](https://www.reddit.com/r/MachineLearning/comments/1ur0bxq/lingbotvideo_sparsemoe_video_diffusion/) ⭐️ 8.0/10

LingBot-Video 是一个 13B 参数的稀疏 MoE 视频扩散 Transformer（活跃参数 1.4B），通过包含物理合理性奖励在内的六项奖励进行了强化学习后训练，并支持基于动作条件的机器人 rollout 预测即世界模型。 该工作通过结合稀疏 MoE 提升效率、强化学习后训练增强合理性，并开源权重与代码，推动了视频生成和世界建模的发展，是机器人与视频合成研究的有力候选。 该模型采用 DeepSeek-V3 风格的稀疏 MoE，拥有 128 个专家和 Top-8 路由，在 RBench 上取得平均最高分，但通用文生视频排名第二。物理合理性奖励由 VLM 评判，尽管加入了真实视频负样本，仍引发对奖励破解的担忧。

reddit · r/MachineLearning · /u/Savings-Display5123 · 7月8日 17:58

**背景**: 扩散 Transformer（DiT）用 Transformer 架构取代了卷积 U-Net 主干，用于生成模型中的去噪过程。稀疏混合专家（MoE）每次前向传播仅激活部分参数，从而以较低计算成本实现更大模型容量。基于奖励模型的强化学习可以针对特定目标（如物理合理性）微调生成模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Sparse_mixture-of-experts">Sparse mixture-of-experts</a></li>
<li><a href="https://en.wikipedia.org/wiki/Diffusion_Transformer">Diffusion Transformer</a></li>
<li><a href="https://en.wikipedia.org/wiki/SGLang">SGLang</a></li>

</ul>
</details>

**标签**: `#video generation`, `#world models`, `#sparse MoE`, `#diffusion transformers`, `#reinforcement learning`

---

<a id="item-12"></a>
## [交互世界模型漂移减少：MoBA 与自滚动蒸馏](https://www.reddit.com/r/MachineLearning/comments/1ur4hkc/reducing_drift_in_interactive_worldmodel_rollouts/) ⭐️ 8.0/10

LingBot World 的研究人员发布了一个开源权重的交互式世界模型，该模型使用 MoBA 注意力掩码（混合双向和自回归注意力）以及基于长自滚动轨迹的蒸馏后训练，显著减少了漂移，并通过连续 60 分钟的稳定滚动展示了效果。 这项工作解决了交互式世界模型中的一个关键挑战——长滚动过程中的漂移积累——这限制了它们的实际可用性。MoBA 注意力与长滚动蒸馏的结合有望为视频游戏、机器人技术和虚拟环境等应用提供更稳定可靠的交互式模拟。 MoBA 注意力掩码通过动态调度 KV 缓存使得长滚动在计算上可行，模型使用 Plücker 嵌入和 AdaLN 进行相机控制。一个局限性是持久性仅在外观层面，而非身份层面，这意味着离开上下文窗口的区域在重新访问时会被重新生成，而非召回。权重以 CC-BY-NC-SA 许可证发布。

reddit · r/MachineLearning · /u/Purple-Low-2779 · 7月8日 20:23

**背景**: 交互式世界模型根据用户输入生成视频帧，本质上作为一个学习到的模拟器。一个常见问题是漂移：当模型基于自身之前的输出自回归地生成新帧时，小误差会累积，导致模拟随时间偏离合理的现实。现有方法通常在训练中使用教师强制，即模型看到真实帧，但这并不能在推理过程中转化为稳定的自滚动。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2604.03118v2">Self-Consistent Distribution Matching with Cache-Aware Training for Fast ...</a></li>
<li><a href="https://huggingface.co/papers/2604.03118">Self-Consistent Distribution Matching with Cache-Aware Training for Fast ...</a></li>

</ul>
</details>

**标签**: `#world models`, `#drift reduction`, `#attention mechanisms`, `#distillation`, `#video generation`

---

<a id="item-13"></a>
## [工信部警告 Claude Code 后门泄露用户数据](https://nvdb.org.cn/publicAnnouncement/2074681830578630657) ⭐️ 8.0/10

中国工业和信息化部于 2025 年 7 月 8 日发布风险提示，指出 Claude Code 2.1.91 至 2.1.196 版本存在安全后门，可以在未经用户同意的情况下，将用户的地域和身份标识等敏感信息传输到远程服务器。 此事意义重大，因为 Claude Code 是一款广泛使用的 AI 编程工具，此次后门事件危及大量开发者的隐私和安全。作为政府权威机构的工信部发出警告，凸显了威胁的严重性，并可能促使各机构重新评估在开发流程中使用 AI 工具的安全性。 受影响版本为 2.1.91 至 2.1.196，后门内置监控机制，会外传敏感数据。建议用户立即排查，卸载受影响版本或升级到已清除恶意代码的最新安全版本，同时加强开发工具的外联权限管控和流量监测。

telegram · zaihuapd · 7月8日 06:09

**背景**: Claude Code 是 Anthropic 公司基于其 Claude 大语言模型系列开发的一款 AI 辅助软件开发工具，可帮助开发者完成编码、调试和代码审查等任务。该工具在行业中广泛使用，因此发现其存在秘密发送用户数据的后门尤为令人担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>

</ul>
</details>

**标签**: `#security`, `#claude-code`, `#backdoor`, `#ai-tools`, `#vulnerability`

---

<a id="item-14"></a>
## [顶尖 AI 企业安全评级低，Anthropic 以 C+领先](http://z.ai/) ⭐️ 8.0/10

生命未来研究所发布了一份报告，对九家顶尖人工智能公司的安全表现进行评级，没有一家获得 A 评级。Anthropic 以 C+位居榜首，OpenAI 和谷歌 DeepMind 得 C，Meta 得 D+，而 DeepSeek、xAI 等公司则获得 F 评级。 该报告凸显了人工智能安全治理方面的关键差距，因为企业正在快速开发变革性人工智能，却没有制定可靠的风险管理计划。这强调了行业需要更严格的安全标准和透明度。 报告指出，许多公司已从禁止将人工智能用于军事领域转向积极寻求防务伙伴关系。中国公司 Z.ai 和阿里云否认与军方有关联的指控，但评级仍然很低。

telegram · zaihuapd · 7月8日 11:30

**背景**: 生命未来研究所（FLI）是一个成立于 2014 年的非营利组织，旨在引导变革性技术远离大规模风险，重点关注人工智能的生存风险。该报告从风险评估、透明度和问责制等维度评估企业。Z.ai 是一家中国人工智能公司，以其 GLM 模型闻名，并于 2025 年被美国列入实体清单。DeepSeek 是一家成立于 2023 年的中国人工智能公司，以低成本高性能模型如 DeepSeek-R1 著称。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Future_of_Life_Institute">Future of Life Institute</a></li>
<li><a href="https://en.wikipedia.org/wiki/Z.ai">Z.ai</a></li>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></li>

</ul>
</details>

**标签**: `#AI safety`, `#AI ethics`, `#industry report`, `#AI governance`

---

<a id="item-15"></a>
## [字节跳动发布 Seedream 5.0 Pro，支持多语言生成](https://seed.bytedance.com/en/seedream5_0_pro) ⭐️ 8.0/10

字节跳动 Seed 团队发布了多模态图像生成模型 Seedream 5.0 Pro，具备高密度信息图、交互式编辑、摄影级画质和原生多语言生成等能力。 此次发布将精准编辑与多语言文字支持结合，推动了 AI 图像生成在教育、国际营销和内容创作等领域的实际应用。 该模型支持空间标注和手绘草图编辑并实现图层分离，可生成十余种语言的文字，并在自然光影、阴影和皮肤纹理等方面达到摄影级真实感。

telegram · zaihuapd · 7月8日 15:11

**背景**: 多模态图像生成模型能够根据文本提示生成图像，通常包含渲染文字的能力。早期模型在多语言文字准确生成和精准编辑方面存在困难。Seedream 5.0 Pro 在这两方面进行了改进，面向专业和国际应用场景。

**标签**: `#ByteDance`, `#multimodal`, `#image generation`, `#AI`, `#Seedream`

---

<a id="item-16"></a>
## [研究人员通过电磁信号识别手机应用，准确率达 99%](https://www.scmp.com/news/china/science/article/3359688/chinese-researchers-find-peephole-any-smartphone-its-leaked-radio-signal) ⭐️ 8.0/10

中国研究人员开发出一种非接触式取证技术，通过分析泄漏的低频电磁信号来识别智能手机正在使用的应用及操作，在 iPhone 15 Pro、小米 15 Pro 和 OPPO Reno 13 等设备上准确率高达 99.07%。 这种攻击方法即使手机处于离线、飞行模式、加密或锁定状态也能工作，无需访问设备系统或存储数据，因此构成了严重的隐私威胁。 该技术分析了运行中智能手机组件发出的低频电磁（EM）信号，研究人员在抖音、微信视频通话、百度地图、短信、浏览器、相机和云存储等流行应用上进行了测试。

telegram · zaihuapd · 7月8日 16:05

**背景**: 所有电子设备在运行时都会发出电磁辐射，这些无意的信号可能泄露设备的活动信息。这被称为侧信道攻击，攻击者利用电磁泄漏、功耗或声音等物理副产品进行攻击。以往的侧信道攻击通常需要物理接触或专用设备，而这项新技术是非接触式的，可在一定距离内工作。

**标签**: `#security`, `#privacy`, `#electromagnetic signals`, `#smartphone`, `#side-channel attack`

---