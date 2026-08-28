---
layout: default
title: "Horizon Summary: 2026-06-18 (ZH)"
date: 2026-06-18
lang: zh
---

> 从 50 条内容中筛选出 15 条重要资讯。

---

1. [美国科学因资金和政策崩溃陷入危机](#item-1) ⭐️ 9.0/10
2. [Android 17 正式发布：强制大屏适配，集成 AI 功能](#item-2) ⭐️ 9.0/10
3. [哪吒监控 v2.0.13 以下版本存在高危路径穿越漏洞 (CVSS 9.1)](#item-3) ⭐️ 9.0/10
4. [Epic Games 开源游戏开发版本控制系统 Lore](#item-4) ⭐️ 8.0/10
5. [美国暂缓封杀 DeepSeek，新增百余家中国公司入安全名单](#item-5) ⭐️ 8.0/10
6. [泄露文件显示 OpenAI 每年亏损数十亿美元](#item-6) ⭐️ 8.0/10
7. [GLM-5.2 在 Artificial Analysis 上成为领先的开放权重模型](#item-7) ⭐️ 8.0/10
8. [RFC 10008 定义 HTTP QUERY 方法，用于安全、幂等的带体请求](#item-8) ⭐️ 8.0/10
9. [大众汽车通过 Play Protect 要求屏蔽 GrapheneOS 用户](#item-9) ⭐️ 8.0/10
10. [Charity Majors: AI 代码可丢弃，需更多工程纪律](#item-10) ⭐️ 8.0/10
11. [下一潜在状态预测：变压器学习紧凑世界模型](#item-11) ⭐️ 8.0/10
12. [探寻 Transformer 电路中探针强度的理论基础](#item-12) ⭐️ 8.0/10
13. [对比目标 SFT 绘制 LLM 因果依赖图](#item-13) ⭐️ 8.0/10
14. [科创板第五套标准扩至人工智能](#item-14) ⭐️ 8.0/10
15. [Anthropic 企业 AI 市场份额首超 OpenAI](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [美国科学因资金和政策崩溃陷入危机](https://www.scientificamerican.com/article/americas-compact-between-science-and-politics-is-broken/) ⭐️ 9.0/10

《科学美国人》的一篇文章及大量社区讨论揭示，严重的资金削减和签证限制正迫使美国科学家离开国家或彻底放弃研究。 这种崩溃威胁到美国在科学和创新领域的领导地位，可能导致长期的人才流失和关键研究能力的丧失。 具体证词包括一位研究人员的 R01 资助未续期，导致员工转为兼职；以及一位科学家，其妻子操作光学陷阱（全球仅约 2000 人掌握的稀有技能），他们正计划移居国外。

hackernews · presspot · 6月17日 09:54 · [社区讨论](https://news.ycombinator.com/item?id=48568058)

**背景**: 美国科研事业长期以来依赖于科学与政治之间的契约，政府通过 NIH 等机构资助基础研究。然而，近期的政治动荡、预算限制和移民政策限制破坏了这一契约，导致学术实验室和国家实验室陷入危机。

**社区讨论**: 评论者表达了深深的沮丧和绝望，许多人分享了离开美国或科学的个人故事。一些人指出，尽管形势混乱，但也迫使人们适应并寻找新机会，但整体情绪仍是失落和不确定性。

**标签**: `#science policy`, `#research funding`, `#US politics`, `#academia crisis`, `#brain drain`

---

<a id="item-2"></a>
## [Android 17 正式发布：强制大屏适配，集成 AI 功能](https://android-developers.googleblog.com/2026/06/Android-17.html) ⭐️ 9.0/10

Google 已向 Pixel 设备推送 Android 17 并开放源代码，引入强制大屏适配、通过 AppFunctions 集成 Gemini AI 助手，以及全面转向 Jetpack Compose。 此更新从根本上改变了 Android 开发，要求应用支持大屏，并允许 AI 直接调用应用功能，这将影响所有开发者，并提升折叠屏、平板等设备上的用户体验。 Android 17 移除了开发者对大屏设备（sw > 600 dp）方向与可调整大小的限制的免除选项，根据设备总内存强制执行严格的内存限制，并引入了临时权限和联系人选择器以增强隐私。

telegram · zaihuapd · 6月17日 01:02

**背景**: Android 17 通过新的 AppFunctions API 集成 Google Gemini 等 AI 助手，使应用能够暴露可供 AI 调用的功能，从而将 Android 打造成一个“智能系统”。它还强制要求大屏自适应支持，延续了自 Android 12L 以来的趋势。Jetpack Compose 作为现代声明式 UI 工具包，成为新开发的默认选择，传统 View 系统进入维护模式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://android-developers.googleblog.com/2026/06/Android-17.html">Android Developers Blog: Android 17 is here</a></li>
<li><a href="https://developer.android.com/about/versions/17/changes/ff-restrictions-ignored">Restrictions on orientation and resizability are ignored | Android Developers</a></li>
<li><a href="https://en.wikipedia.org/wiki/Jetpack_Compose">Jetpack Compose</a></li>
<li><a href="https://developer.android.com/reference/android/app/appfunctions/AppFunctionService">AppFunctionService | API reference |</a></li>

</ul>
</details>

**标签**: `#Android`, `#mobile development`, `#AI integration`, `#privacy`, `#Jetpack Compose`

---

<a id="item-3"></a>
## [哪吒监控 v2.0.13 以下版本存在高危路径穿越漏洞 (CVSS 9.1)](https://t.me/zaihuapd/42001) ⭐️ 9.0/10

哪吒监控 v2.0.13 以下版本被披露存在一个严重的未授权路径穿越漏洞 (CVE-2026-53519)，CVSS 评分为 9.1。攻击者可通过构造类似 /dashboard../data/config.yaml 的 GET 请求读取任意文件，从而提取 JWT 密钥。 哪吒监控是一款广泛使用的自托管服务器监控工具，该漏洞允许未授权访问敏感的 JWT 密钥，攻击者可伪造会话并危及整个服务器集群。所有用户应立即升级。 该漏洞位于仪表板组件中，影响 v2.0.13 之前的所有版本。利用过程无需认证，可通过 HTTP 触发，远程利用且复杂度低。

telegram · zaihuapd · 6月17日 01:25

**背景**: 路径穿越（目录遍历）攻击允许攻击者通过在文件路径中使用 '../' 等序列来读取预期目录之外的文件。哪吒监控是一款开源、自托管的监控运维工具，支持多服务器和网站，因此这类漏洞对基础设施安全尤为危险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/nezhahq/nezha">GitHub - nezhahq/nezha: :trollface: Self-hosted, lightweight ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Path_traversal_vulnerability">Path traversal vulnerability</a></li>
<li><a href="https://owasp.org/www-community/attacks/Path_Traversal">Path Traversal | OWASP Foundation</a></li>

</ul>
</details>

**标签**: `#网络安全`, `#漏洞`, `#哪吒监控`, `#路径穿越`, `#CVSS`

---

<a id="item-4"></a>
## [Epic Games 开源游戏开发版本控制系统 Lore](https://lore.org/) ⭐️ 8.0/10

Epic Games 将其原本为 Fortnite 构建的版本控制系统 Lore 开源，该系统旨在处理大型二进制资产，并替代 Perforce 在游戏开发中的地位。 Lore 解决了 Git 对纹理、3D 模型等非文本文件处理不佳的问题，为游戏工作室提供了可扩展的替代方案。它可能撼动 Perforce 在游戏开发中的专有统治地位。 Lore 原名 Unreal Revision Control，已在 Epic 内部和 Unreal Editor for Fortnite 中使用。它支持文件锁定、权限管理和大型项目的协作。

hackernews · regnerba · 6月17日 14:30 · [社区讨论](https://news.ycombinator.com/item?id=48571081)

**背景**: 像 Git 这样的版本控制系统可以跟踪代码文件的变化，但难以处理游戏开发中常见的大型二进制资产。Perforce 因其文件锁定和可扩展性而成为游戏开发行业标准，但它是专有且昂贵的。Lore 旨在提供具有类似功能的开源替代方案。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/EpicGames/lore">Lore is a next-generation, open source revision control system</a></li>
<li><a href="https://www.phoronix.com/news/Epic-Games-Lore-VCS">Epic Games Announces Lore Open-Source Version Control System</a></li>

</ul>
</details>

**社区讨论**: Hacker News 社区普遍认为 Lore 是 Perforce 在游戏开发领域的有力挑战者。一些用户强调 Git 用户体验差且缺乏文件锁定，另一些用户则指出 Lore 作为 Epic 内部工具的背景。人们对其与 Perforce 的性能对比充满好奇。

**标签**: `#version control`, `#game development`, `#open source`, `#scalability`, `#perforce`

---

<a id="item-5"></a>
## [美国暂缓封杀 DeepSeek，新增百余家中国公司入安全名单](https://www.reuters.com/world/china/us-holds-off-blacklisting-chinas-deepseek-more-than-100-firms-deemed-security-2026-06-17/) ⭐️ 8.0/10

美国暂时未将中国人工智能公司 DeepSeek 列入黑名单，但已将超过 100 家其他中国企业纳入贸易安全风险清单。 这一决定表明美中科技竞争的微妙态度，可能影响全球 AI 供应链和先进 AI 模型的可获取性。 以高效大语言模型闻名的 DeepSeek 未被列入名单，但黑名单的扩大针对被视为安全风险的实体，包括涉及先进计算和 AI 的企业。

hackernews · giuliomagnifico · 6月17日 03:55 · [社区讨论](https://news.ycombinator.com/item?id=48565498)

**背景**: 美国实体清单限制美国公司向列入清单的实体出口特定商品和技术。DeepSeek 是一家中国 AI 初创公司，开发了高性价比的模型，尽管面临先进 GPU 的出口管制，仍以具竞争力的性能获得关注。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论反应不一：一些用户赞赏 DeepSeek 的实惠性和编程任务的实用性，另一些批评美国政府的行为虚伪或难以执行。有人指出许多中国 AI 公司几乎不依赖美国商品，限制了影响。

**标签**: `#geopolitics`, `#AI`, `#DeepSeek`, `#US-China`, `#regulation`

---

<a id="item-6"></a>
## [泄露文件显示 OpenAI 每年亏损数十亿美元](https://arstechnica.com/ai/2026/06/leaked-financial-docs-show-openai-is-losing-billions-of-dollars-a-year/) ⭐️ 8.0/10

泄露的财务文件显示，OpenAI 在 2025 年尽管收入达到 130 亿美元，但仍亏损数十亿美元，研发成本是主要支出。 这引发了关于领先 AI 公司长期财务可持续性以及前沿 AI 开发经济学的关键问题，影响投资者、竞争对手和更广泛的科技行业。 该公司 2025 年总收入为 130 亿美元，营收成本为 75 亿美元，研发支出占费用最大部分。OpenAI 每周有超过 9 亿 ChatGPT 活跃用户，但只有约 5000 万付费用户。

hackernews · greenchair · 6月17日 21:31 · [社区讨论](https://news.ycombinator.com/item?id=48577208)

**背景**: OpenAI 是一家领先的人工智能研究和部署公司，以开发 GPT-4 和 ChatGPT 等先进模型而闻名。该公司最初是非营利组织，后来创建了营利性子公司以筹集资金，但其治理结构仍然复杂。大型语言模型的开发需要巨大的计算资源和人才，导致高昂的运营成本。

**社区讨论**: 评论者讨论了 OpenAI 商业模式的可持续性，一些人指出研发成本占主导地位，并质疑是否应该将重点转向降低推理成本。其他人则指出，鉴于存在 DeepSeek 等许多免费替代品，将免费用户转化为付费用户面临挑战。

**标签**: `#OpenAI`, `#AI business`, `#financial analysis`, `#AI startups`

---

<a id="item-7"></a>
## [GLM-5.2 在 Artificial Analysis 上成为领先的开放权重模型](https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index) ⭐️ 8.0/10

GLM-5.2 在 Artificial Analysis 智能指数上被评为领先的开放权重模型，以大幅低于闭源模型的价格实现了接近前沿的性能。 这一进展表明，开放权重模型可以媲美 GPT-5.5 和 Opus 等顶级闭源模型，有可能以更低的成本普及高质量 AI，并挑战专有提供商的统治地位。 该模型在编程和智能体基准测试上取得接近前沿的分数，社区报告称其 API 价格比 Anthropic 的 Opus 便宜 10 倍，但一些用户观察到推理任务中 token 消耗较高。

hackernews · himata4113 · 6月17日 09:12 · [社区讨论](https://news.ycombinator.com/item?id=48567759)

**背景**: 开放权重模型允许任何人下载、检查和微调训练后的权重，而不是像完全闭源模型那样。Artificial Analysis 是一个独立平台，对 AI 模型的质量、价格和速度进行基准测试，为开发者提供透明的比较。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://artificialanalysis.ai/">AI Model & API Providers Analysis | Artificial Analysis</a></li>
<li><a href="https://huggingface.co/blog/daya-shankar/open-source-llms">Best Open -Source LLM Models in 2026: Coding, Local, Agentic AI ...</a></li>
<li><a href="https://www.linkedin.com/pulse/openais-open-weight-model-what-means-developers-ai-industry-tsi9f">OpenAI’s Open - Weight Model : What It Means for Developers and the...</a></li>

</ul>
</details>

**社区讨论**: 社区成员普遍庆祝 GLM-5.2 以极低的价格提供接近前沿的质量，有人称其是'对闭源提供商的巨大胜利'。然而，有用户指出其推理效率有待提高，并举例说明一次推理任务耗时 15 分钟、消耗 45k token。

**标签**: `#AI`, `#open-weights`, `#GLM`, `#model comparison`

---

<a id="item-8"></a>
## [RFC 10008 定义 HTTP QUERY 方法，用于安全、幂等的带体请求](https://www.rfc-editor.org/info/rfc10008/) ⭐️ 8.0/10

RFC 10008 已正式发布，标准化了 HTTP QUERY 方法作为新的 HTTP 请求方法，该方法安全且幂等，并允许请求体，为 GET 带体请求提供了标准化替代方案。 这解决了 HTTP 中长期存在的空白：GET 不能携带请求体，但许多应用需要带体的复杂查询。QUERY 支持缓存、自动重试以及更安全的 API、HTML 表单和复杂数据检索交互。 QUERY 方法类似于 POST，但必须安全且幂等，即相同请求产生相同结果且无副作用。缓存可以使用请求体作为缓存键的一部分，但这引发了关于键大小无限制的担忧。

hackernews · schappim · 6月17日 10:51 · [社区讨论](https://news.ycombinator.com/item?id=48568502)

**背景**: HTTP GET 是幂等且可缓存的，但历史上不能包含请求体。POST 支持请求体，但不要求幂等，导致重试和缓存问题。IETF 曾考虑允许 GET 带体，但由于现有实现的互操作性问题，最终选择了新方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.rfc-editor.org/info/rfc10008/">RFC 10008 : The HTTP QUERY Method | RFC Editor</a></li>
<li><a href="https://httpwg.org/http-extensions/draft-ietf-httpbis-safe-method-w-body.html">The HTTP QUERY Method</a></li>
<li><a href="https://horovits.medium.com/http-s-new-method-for-data-apis-http-query-1ff71e6f73f3">HTTP‘s New Method For Data APIs: HTTP QUERY | by Horovits | Medium</a></li>

</ul>
</details>

**社区讨论**: 社区评论讨论了缓存键实现挑战、HTML 表单支持 QUERY 以避免 POST 重新提交警告的可能性，以及历史上发送 GET 带体的变通方法。讨论总体上表示支持，但也提出了合理的技术担忧。

**标签**: `#HTTP`, `#RFC`, `#web standards`, `#API design`, `#protocol`

---

<a id="item-9"></a>
## [大众汽车通过 Play Protect 要求屏蔽 GrapheneOS 用户](https://discuss.grapheneos.org/d/35949-volkswagen-app?page=3) ⭐️ 8.0/10

大众汽车已锁定其 API，要求通过 Play Protect 认证，从而有效阻止 GrapheneOS 用户通过官方应用访问车辆功能。此举禁用了社区驱动的集成，迫使用户依赖广告繁多的官方应用。 一家主要汽车制造商的此举开创了先例，限制设备自由和注重隐私的操作系统用户访问联网汽车功能。这凸显了 Google 认证生态系统与 GrapheneOS 等优先考虑隐私而非 Google 服务的自定义 Android ROM 之间日益紧张的局势。 API 锁定不仅影响 GrapheneOS，也影响任何没有 Play Protect 认证的设备，包括使用 Home Assistant 等社区项目进行自动化的设备。据报道，官方大众应用 60%是广告，30%是功能，使其比以前社区替代方案功能更差。

hackernews · microtonal · 6月17日 15:04 · [社区讨论](https://news.ycombinator.com/item?id=48571526)

**背景**: GrapheneOS 是一个经过安全加固、基于 Android 的开源操作系统，专注于隐私，通常不运行 Google Play 服务。Google 的 Play Protect 认证是设备访问 Google 应用和某些 API 所必需的，它依赖于 Google 的专有兼容性测试。GrapheneOS 用户通常避免使用 Google 服务以最小化数据收集，这使得 Play Protect 认证与其隐私目标不兼容。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GrapheneOS">GrapheneOS</a></li>
<li><a href="https://www.android.com/certified/">Android – Certified</a></li>
<li><a href="https://grapheneos.org/">GrapheneOS: the private and secure mobile OS</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了沮丧和失望，用户指出大众此前已关闭了社区集成的 API 访问，现在又彻底屏蔽 GrapheneOS。一些用户对失去 Home Assistant 自动化等有用功能感到惋惜，另一些用户批评官方应用广告过多。还有人担心这一趋势可能蔓延至大众其他品牌，并可能与更广泛的隐私工具限制相呼应。

**标签**: `#privacy`, `#GrapheneOS`, `#Android`, `#automotive`, `#Volkswagen`

---

<a id="item-10"></a>
## [Charity Majors: AI 代码可丢弃，需更多工程纪律](https://simonwillison.net/2026/Jun/17/charity-majors/#atom-everything) ⭐️ 8.0/10

Charity Majors 认为，AI 彻底颠覆了代码生产的经济学，使代码生成变得几乎免费且即时，代码从被珍视变为可丢弃。 这一根本性转变要求更强的工程纪律，因为重点从编写代码转向 curation 和验证，影响软件团队对架构、测试和系统设计的优先级安排。 Majors 指出，代码行几乎一夜之间从精心策划变为可丢弃和可重新生成，突显了开发者心态的巨大变化。

rss · Simon Willison · 6月17日 17:12

**背景**: 传统上，软件开发中编写和维护代码成本高昂，使得重用和精心策划至关重要。借助 AI 辅助编程，生成大量代码变得廉价且快速，降低了新代码的边际成本。这一经济转变要求工程师在系统级思维和质量保证上投入更多精力，而非手工编码。

**标签**: `#ai`, `#ai-assisted-programming`, `#software-engineering`, `#economics-of-code`, `#charity-majors`

---

<a id="item-11"></a>
## [下一潜在状态预测：变压器学习紧凑世界模型](https://www.reddit.com/r/MachineLearning/comments/1u84mio/nextlatent_prediction_transformers_r/) ⭐️ 8.0/10

微软研究院提出下一潜在状态预测（NextLat），一种自监督方法，训练变压器在给定当前潜在状态和下一词元的情况下预测自身的下一潜在状态，从而构建更好的世界模型，并通过自推测解码实现高达 3.3 倍的推理加速。 NextLat 相较于标准下一词元预测，提升了数据效率和表示学习，提供了一种将历史压缩为紧凑信念状态的原则性方法。这有望带来更强大、更快的自回归模型，用于推理和规划任务。 该方法理论上收敛到信念状态——预测未来所需的压缩信息。自推测解码支持多步前瞻，在不牺牲输出质量的情况下实现高达 3.3 倍的无损加速。

reddit · r/MachineLearning · /u/jayden_teoh_ · 6月17日 08:44

**背景**: 标准变压器通过下一词元预测进行训练，每个词元提供稀疏的监督。NextLat 增加了一个辅助任务：预测下一个潜在表示，从而压缩序列历史。自推测解码是一种技术，同一模型同时起草和验证词元块，减少顺序生成步骤。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2511.05963">[2511.05963] Next-Latent Prediction Transformers Learn Compact World Models</a></li>
<li><a href="https://neurips.cc/virtual/2025/132811">NeurIPS Keynote #7 Next-Latent Prediction Transformers Learn Compact World Models</a></li>

</ul>
</details>

**标签**: `#transformers`, `#self-supervised learning`, `#representation learning`, `#efficient inference`, `#Microsoft Research`

---

<a id="item-12"></a>
## [探寻 Transformer 电路中探针强度的理论基础](https://www.reddit.com/r/MachineLearning/comments/1u8lo60/how_do_you_analyze_the_relative_strength_of/) ⭐️ 8.0/10

一位 Reddit 用户发布了一个详细的问题，寻求在 Transformer 电路中比较探针强度的理论基础，特别关注探针容量与底层网络复杂度之间的权衡。 这个问题触及了机制可解释性中的一个根本性空白：如何严格评估探针能揭示模型内部机制的哪些信息。解决这一问题可能带来更可靠的电路分析，并为模型安全性和事实性提供更好的保障。 该用户引用了一项旧研究，该研究训练了逻辑回归探针来检测单词位置，并指出词汇量极小会导致性能不具代表性等问题。他们还分享了一个真实失败案例：Google Gemini 错误地数出了 'Google' 中的字母数，这削弱了模型天生学会 token 位置的说法。

reddit · r/MachineLearning · /u/RepresentativeBee600 · 6月17日 20:29

**背景**: 在机制可解释性中，探针技术涉及在模型激活上训练简单分类器（探针），以测试某些特征是否被编码。然而，比较探针强度的理论基础尚不完善，关于过拟合和样本复杂度的问题仍未解决。奈奎斯特采样定理被提及作为一种可能的类比，用于判断是否已经看到足够的数据来保证可靠地检测模式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2509.17665">[2509.17665] Mechanistic Interpretability with SAEs: Probing</a></li>

</ul>
</details>

**标签**: `#mechanistic interpretability`, `#probing`, `#circuit analysis`, `#transformer models`, `#ML theory`

---

<a id="item-13"></a>
## [对比目标 SFT 绘制 LLM 因果依赖图](https://www.reddit.com/r/MachineLearning/comments/1u8if6l/contrastive_targeted_sft_as_a_mechinterp_method/) ⭐️ 8.0/10

一位研究者提出使用对比目标监督微调（SFT）来发现大型语言模型中不同能力维度之间的因果依赖图，通过训练一对仅在某一维度上有差异的检查点，然后消融识别出的电路并测量其他维度的性能下降。 该方法有望系统性地理解 LLM 内部不同能力如何相互作用，可能优化训练顺序和定向行为控制，这是机械可解释性和模型操控的关键目标。 对比方法从同一基础模型创建一对检查点——一个维度深度代表，另一个浅层代表——然后通过差异补丁定位电路并消融它们以映射因果依赖。研究者还计划通过需要因果链的提示测试组合性，并使用激活引导作为诊断工具。

reddit · r/MachineLearning · /u/Substantial_Diver469 · 6月17日 18:31

**背景**: 机械可解释性旨在逆向工程神经网络中实现特定行为的内部组件（电路）。监督微调（SFT）使用标注数据使预训练模型适应特定任务。对比学习技术通过比较正负样本来学习表示。该帖子将这些思想结合起来，以映射 LLM 中能力维度之间的因果依赖，这是一种尚未在现有文献中探索的新方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2304.14997">[2304.14997] Towards Automated Circuit Discovery for Mechanistic Interpretability</a></li>
<li><a href="https://arxiv.org/html/2402.11068v2">Large Language Models for Causal Discovery: Current Landscape ...</a></li>

</ul>
</details>

**标签**: `#mechanistic interpretability`, `#SFT`, `#causal dependencies`, `#LLMs`, `#circuit discovery`

---

<a id="item-14"></a>
## [科创板第五套标准扩至人工智能](https://mp.weixin.qq.com/s/ywLPXkSlqY9S5Vwp8G5saA) ⭐️ 8.0/10

中国证监会主席吴清在 2026 陆家嘴论坛上宣布，科创板第五套上市标准的适用范围将扩大至人工智能领域，涵盖量子科技、生物制造、具身智能等硬科技企业。此外，证监会还将推出储架发行等再融资改革措施，并宣布支持上海国际金融中心建设的四项政策。 这一政策调整为尚未盈利的人工智能及硬科技初创企业提供了关键的融资渠道，可能加速其成长和 IPO 进程。这表明政府对人工智能领域的大力支持，并可能重塑中国科技资本市场的格局。 第五套标准原先允许生物医药等硬科技领域的未盈利企业上市，此次扩围明确将人工智能大模型、具身智能、量子科技、生物制造等企业纳入。此外，证监会将严查借科技之名蹭热点、炒概念等违法违规行为，并适时发布规范资本市场人工智能的指导意见。

telegram · zaihuapd · 6月17日 08:30

**背景**: 科创板是中国 2019 年推出的、对标纳斯达克的科技板块，其第五套上市标准允许未盈利但研发投入和市值达标的公司上市。储架发行是一种“一次核准、多次发行”的再融资机制，可简化流程、降低融资成本。具身智能指能通过与物理环境交互实现智能增长的 AI 系统，例如人形机器人。

<details><summary>参考链接</summary>
<ul>
<li><a href="http://www.ce.cn/xwzx/gnsz/gdxw/202606/t20260618_3038347.shtml">科创板第五套标准扩围至大模型企业 智谱、MiniMax“回A”有望提速科创板...</a></li>
<li><a href="https://paper.cnstock.com/html/2026-06/18/content_2233003.htm">科创板第五套标准扩围至大模型企业 智谱、MiniMax“回A”有望提速</a></li>
<li><a href="https://baike.baidu.com/item/储架发行制度/1648322">储架发行制度_百度百科</a></li>

</ul>
</details>

**标签**: `#AI`, `#regulation`, `#China`, `#stock market`, `#technology`

---

<a id="item-15"></a>
## [Anthropic 企业 AI 市场份额首超 OpenAI](https://techcrunch.com/2026/06/16/anthropics-latest-feud-with-the-trump-admin-may-actually-help-it-sales-data-suggests/) ⭐️ 8.0/10

2026 年 5 月，Anthropic 在企业 AI 市场份额首次超过 OpenAI，Ramp 数据显示其企业订阅占比达 41%，OpenAI 为 39.5%，尽管特朗普政府以出口管制为由要求 Anthropic 下架其最新模型。 这一里程碑标志着企业 AI 采用格局的转变，尽管面临监管阻碍，注重安全的 Anthropic 正在赢得更多信任。这也可能在潜在 IPO 前重塑竞争态势和投资者情绪。 受影响的模型是 2026 年 6 月发布后被迅速要求下架的 Claude Fable 5 和 Claude Mythos 5。然而，大多数企业客户仍在使用公开的 Claude Opus 系列，从而缓解了直接的收入影响。

telegram · zaihuapd · 6月17日 09:30

**背景**: Anthropic 是一家由前 OpenAI 员工创立的 AI 安全公司，以其 Claude 模型闻名。2026 年 6 月，它发布了最强大的模型 Fable 5 和 Mythos 5，但美国政府以国家安全为由要求撤下，担心外国访问。企业 AI 市场份额由 Ramp 等公司追踪，分析企业在 AI 订阅上的支出。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/news/claude-fable-5-mythos-5">Claude Fable 5 and Claude Mythos 5 \ Anthropic</a></li>
<li><a href="https://www.cnbc.com/2026/06/09/anthropic-mythos-claude-fable-5.html">Anthropic releases Mythos-like AI model to the public, Claude Fable 5</a></li>

</ul>
</details>

**标签**: `#AI industry`, `#enterprise AI`, `#market competition`, `#regulation`, `#Anthropic`

---