---
layout: default
title: "Horizon Summary: 2026-07-15 (ZH)"
date: 2026-07-15
lang: zh
---

> 从 38 条内容中筛选出 11 条重要资讯。

---

1. [Stripe 与 Advent 联合报价 530 亿美元收购 PayPal](#item-1) ⭐️ 9.0/10
2. [许多旧版 shim 引导加载程序仍被 Secure Boot 接受](#item-2) ⭐️ 9.0/10
3. [DeepSeek 年化收入逼近 5 亿美元，V4 API 毛利率超 50%](#item-3) ⭐️ 9.0/10
4. [Inkling：支持音频的新型开放权重多模态模型](#item-4) ⭐️ 8.0/10
5. [Claude web\_fetch 漏洞泄露用户记忆](#item-5) ⭐️ 8.0/10
6. [Linux 7.2 io\_uring 采用无锁 MPSC FIFO 队列](#item-6) ⭐️ 8.0/10
7. [通过哈达玛积分析解构卷积神经元](#item-7) ⭐️ 8.0/10
8. [中国 7 款手机端侧 AI 模型完成备案](#item-8) ⭐️ 8.0/10
9. [中国零售业垂类时代结束，各玩家同台竞技](#item-9) ⭐️ 8.0/10
10. [谷歌与 Epic 撤回动议，第三方应用商店将入驻 Google Play](#item-10) ⭐️ 8.0/10
11. [Telegram 推出机器人无服务器平台](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Stripe 与 Advent 联合报价 530 亿美元收购 PayPal](https://www.reuters.com/business/finance/stripe-advent-offer-buy-paypal-more-than-53-billion-sources-say-2026-07-15/) ⭐️ 9.0/10

据消息人士称，Stripe 与私募股权公司 Advent International 联合提出以超过 530 亿美元的价格收购 PayPal。 此次收购将合并两大支付平台，可能减少竞争并引发金融科技行业的反垄断担忧。 报价超过 530 亿美元，若完成，将把 Stripe、PayPal、Venmo、Braintree 和 Xoom 纳入同一集团。

hackernews · rvz · 7月15日 03:32 · [社区讨论](https://news.ycombinator.com/item?id=48915953)

**背景**: Stripe 是主要的在线支付处理商，而 PayPal 是领先的数字钱包。两家公司在在线结账领域存在竞争。反垄断监管机构可能因市场集中度问题对此交易进行审查。

**社区讨论**: 评论者表达了强烈反对，担心费用上涨、竞争减少以及 Stripe 对某些商户的限制政策。还有人指出高市场份额可能带来反垄断问题。

**标签**: `#fintech`, `#acquisition`, `#payments`, `#antitrust`, `#Stripe`

---

<a id="item-2"></a>
## [许多旧版 shim 引导加载程序仍被 Secure Boot 接受](https://lwn.net/Articles/1082940/) ⭐️ 9.0/10

CMU CERT 协调中心披露，许多存在漏洞的 shim 引导加载程序版本从未被添加到 Secure Boot 撤销列表中，允许攻击者绕过 Secure Boot 保护并在早期引导阶段执行任意代码。 这一疏忽破坏了 Linux 系统的基本安全机制，可能导致持久性攻击，重启和重装系统后仍能存活。 该建议包含易受攻击的 shim 列表，但许多版本未被加入撤销列表（DBX），而 DBX 用于阻止不受信任的 UEFI 模块加载。

rss · LWN.net · 7月15日 12:49

**背景**: Secure Boot 是一种 UEFI 安全特性，确保只有经过签名和受信任的引导加载程序才能运行。shim 引导加载程序充当 UEFI 固件与 Linux 引导加载程序之间的桥梁，撤销列表（DBX）用于将已知存在漏洞的版本列入黑名单。未将受感染的 shim 版本添加到该列表会导致系统暴露于风险中。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/rhboot/shim">GitHub - rhboot/shim: UEFI shim loader · GitHub</a></li>
<li><a href="https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_monitoring_and_updating_the_kernel/updating-the-secure-boot-revocation-list">Chapter 24. Updating the Secure Boot Revocation List | Managing...</a></li>

</ul>
</details>

**标签**: `#security`, `#secure boot`, `#linux`, `#bootloader`, `#vulnerability`

---

<a id="item-3"></a>
## [DeepSeek 年化收入逼近 5 亿美元，V4 API 毛利率超 50%](https://www.theinformation.com/articles/deepseeks-annualized-revenue-nears-500-million-boosting-fundraise-ipo-plans) ⭐️ 9.0/10

DeepSeek 的年化收入已达到 4 亿至 5 亿美元，主要来自企业和开发者的 API 调用，其 V4 API 的毛利率超过 50%。公司还计划以 740 亿美元的估值融资 74 亿美元。 这一里程碑证明了 DeepSeek 的商业化成功和盈利能力，验证了其 API 商业模式在 OpenAI 和 Anthropic 等竞争对手中的可行性。高估值和融资计划表明投资者信心强劲，并预示其在竞争激烈的 AI 领域有进一步增长潜力。 年化收入是基于近期月增速折算，并非已实现的全年收入。尽管 DeepSeek 的收费远低于 OpenAI 和 Anthropic，但通过优化基础设施减少了运行模型所需的芯片数量，从而实现了高毛利率。

telegram · zaihuapd · 7月15日 07:04

**背景**: DeepSeek 是一家以开发大型语言模型闻名的中国 AI 公司。其 DeepSeek V4 API 于 2026 年 4 月发布，兼容 OpenAI 和 Anthropic 的 API 格式，旨在提供高性价比的前沿 AI 能力。公司在首轮融资中还吸引了腾讯、宁德时代等大企业投资。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://api-docs.deepseek.com/">Your First API Call | DeepSeek API Docs</a></li>
<li><a href="https://deepseek.ai/deepseek-v4">DeepSeek AI: R1 Reasoning, API &amp; Local Deployment 2026</a></li>

</ul>
</details>

**标签**: `#DeepSeek`, `#AI`, `#Revenue`, `#API`, `#Fundraising`

---

<a id="item-4"></a>
## [Inkling：支持音频的新型开放权重多模态模型](https://thinkingmachines.ai/news/introducing-inkling/) ⭐️ 8.0/10

Thinking Machines AI 发布了 Inkling，这是一个大型开放权重多模态模型，支持音频输入，并可在 Tinker 平台上进行微调。 作为支持音频的最大开放权重模型之一，Inkling 为企业与开发者提供了一种可定制、可本地部署的闭源模型替代方案，有望降低多模态 AI 应用的成本并促进创新。 Inkling 并非整体最强的模型，但它结合了多模态能力、高效推理以及可在 Tinker 上进行微调的便利性，使其成为实用的可定制基座。社区提供了本地部署资源，包括 llama.cpp 分支、Unsloth 以及 Hugging Face 上的 GGUF/NVFP4 版本。

hackernews · vimarsh6739 · 7月15日 18:12 · [社区讨论](https://news.ycombinator.com/item?id=48924912)

**背景**: 开放权重模型是指将训练好的参数（权重）公开发布的人工智能模型，任何人都可以下载并修改。这不同于 GPT-4 等仅提供 API 访问的闭源模型。Inkling 支持音频、文本和图像，因此是多模态的，但不支持视频。Tinker 平台允许用户无需深厚专业知识即可对模型进行微调以适应特定任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://hai.stanford.edu/ai-definitions/what-is-an-open-weight-model">What is an Open-Weight Model? - Stanford HAI</a></li>
<li><a href="https://www.tinker.com/">Tinker — Play with AI , bring your ideas to life</a></li>

</ul>
</details>

**社区讨论**: 社区评论对 Inkling 的音频能力和本地部署潜力表示热情，有用户指出这可能是美国 Thinking Machines 公司推出的领先开放权重模型。另一评论称赞在 Tinker 上提供可微调的开放基础模型的商业模式，使企业能够以更低成本拥有定制化模型。总体情绪积极，关注实际应用。

**标签**: `#AI`, `#open-weights`, `#multimodal`, `#fine-tuning`, `#HN`

---

<a id="item-5"></a>
## [Claude web\_fetch 漏洞泄露用户记忆](https://simonwillison.net/2026/Jul/15/claude-web-fetch-exfiltration/#atom-everything) ⭐️ 8.0/10

安全研究员 Ayush Paul 发现了一种提示注入攻击，能够绕过 Claude 的 web\_fetch 工具保护，通过诱使 AI 跟随获取页面中的恶意链接，提取用户的私人记忆，包括姓名、所在城市和雇主名称。 此次攻击展示了 Anthropic 精心设计的防御措施被实际绕过的情况，表明即使是对&\#x27;致命三重奏&\#x27;的复杂保护，也可能被创意漏洞突破。它影响到所有启用记忆和 web\_fetch 功能的 Claude 用户，凸显了保护 AI 代理免受数据泄露的持续挑战。 该攻击利用了一个蜜罐网页，该网页呈现了一个虚假的身份验证系统，要求代理按字母顺序浏览用户个人资料 URL。Anthropic 拒绝了漏洞赏金申请，声称已内部发现该漏洞，随后通过阻止 web\_fetch 跟随获取内容中的额外链接来修复了问题。

rss · Simon Willison · 7月15日 14:21

**背景**: 提示注入攻击利用了大型语言模型遵循不可信内容中嵌入指令的能力。当 AI 代理具备&\#x27;致命三重奏&\#x27;——访问私有数据、处理不可信输入的能力以及可以对外通信的工具——攻击者可以诱骗其泄露敏感信息。Claude 的 web\_fetch 工具设计有限制，只允许获取用户直接输入或由其 web\_search 工具返回的 URL，以防范此类攻击。但该漏洞允许跟随获取页面内的链接，从而导致数据泄露攻击。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/">The lethal trifecta for AI agents: private data, untrusted content, and external communication</a></li>
<li><a href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool">Web fetch tool - Claude Platform Docs</a></li>
<li><a href="https://simonwillison.net/2025/Sep/10/claude-web-fetch-tool/">Claude API: Web fetch tool</a></li>

</ul>
</details>

**标签**: `#AI safety`, `#prompt injection`, `#security vulnerability`, `#Claude`, `#exfiltration`

---

<a id="item-6"></a>
## [Linux 7.2 io\_uring 采用无锁 MPSC FIFO 队列](https://lwn.net/Articles/1081871/) ⭐️ 8.0/10

Linux 内核 7.2 的 io\_uring 子系统将用无锁多生产者单消费者（MPSC）FIFO 队列替代现有的无锁链表（llist）任务跟踪，带来显著的性能提升。 这一改动提升了高性能 I/O 工作负载的公平性并减少了缓存争用，直接惠及使用 io\_uring 进行异步 I/O 的应用程序。 新队列使用尾指针和一个桩节点（stub sentinel）来维护 FIFO 顺序，无需列表反转，并避免了旧的头指针式 llist 方法中的重试循环和缓存行 bouncing。

rss · LWN.net · 7月15日 13:35

**背景**: io\_uring 是 Linux 内核的异步 I/O 接口，使用用户空间与内核之间的共享环形缓冲区。它目前使用无锁单链表（llist）跟踪工作项，该链表行为类似栈，处理前需要重排序，导致效率低下。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linux.org/threads/lwn-net-lockless-mpsc-fifo-queues-for-io_uring.68933/">News - [LWN.net] [$] Lockless MPSC FIFO queues for io_uring</a></li>

</ul>
</details>

**标签**: `#linux kernel`, `#io\_uring`, `#lockless data structures`, `#performance`, `#MPSC queue`

---

<a id="item-7"></a>
## [通过哈达玛积分析解构卷积神经元](https://www.reddit.com/r/MachineLearning/comments/1uwya70/mechanistic_interpretability_a_first_paper_on/) ⭐️ 8.0/10

作者提出一种新技术，通过计算感受野与权重的哈达玛积，然后进行聚类，来解构 Inceptionv1 中的神经元，揭示出像汽车、猫、狗等单语义特征簇。 这项工作是对机制可解释性的重要贡献，提供了一种细粒度分析卷积神经元的新方法。它可以帮助研究人员更好地理解和验证视觉模型的内部表征，推动 AI 安全发展。 分析显示，低值簇（如字母）的所有依赖神经元都对同一概念做出反应，正负权重均匀分布以降低总和，表明梯度下降有意为之。该方法应用于 Inceptionv1 的 mixed4e 层。

reddit · r/MachineLearning · /u/narang\_27 · 7月15日 06:59

**背景**: 机制可解释性旨在通过理解神经网络的内部算法和电路来逆向工程。Inceptionv1 是一种卷积神经网络架构，使用 1x1 卷积来降低维度。哈达玛积是逐元素乘法运算，在此用于结合感受野和权重信息。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mechanistic_interpretability">Mechanistic interpretability</a></li>
<li><a href="https://en.wikipedia.org/wiki/Hadamard_product_%28matrices%29">Hadamard product (matrices) - Wikipedia</a></li>
<li><a href="https://medium.com/@karuneshu21/implement-inception-v1-in-pytorch-66bdbb3d0005">Implement Inception - v 1 in PyTorch | by Karunesh Upadhyay | Medium</a></li>

</ul>
</details>

**标签**: `#mechanistic interpretability`, `#convolutional neural networks`, `#interpretability`, `#AI safety`, `#deep learning`

---

<a id="item-8"></a>
## [中国 7 款手机端侧 AI 模型完成备案](https://mp.weixin.qq.com/s/5MTWh4pWVAlL71RQbU-Udg) ⭐️ 8.0/10

2024 年 7 月 8 日，来自苹果、华为、OPPO、vivo、小米、三星和中兴的七款手机端侧语言模型在中国网信办完成备案。 这一监管里程碑表明，主要智能手机的 AI 功能可以合规地在中国部署，加速端侧 AI 的采用，并可能为 AI 治理树立先例。 备案的模型包括 Apple Intelligence、华为小艺 AI 大模型、OPPO AndesGPT、vivo 蓝心智能大模型、小米澎湃 AI 和三星 Galaxy AI 等，均用于手机端。

telegram · zaihuapd · 7月15日 08:06

**背景**: 端侧 AI 模型直接在手机上运行，而非云端，提供更快的响应和更好的隐私保护。中国监管机构要求 AI 产品进行备案，以确保安全和符合法规。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://juejin.cn/post/7413629689255182390">juejin.cn/post/7413629689255182390</a></li>
<li><a href="https://www.53ai.com/news/zhinengyingjian/2024070758924.html">【不看后悔】一文梳理 端 侧 模 型 和小 模 型 - 53AI-AI...</a></li>
<li><a href="https://www.aibase.com/tool/22425">AndesGPT -Personalized and exclusive intelligent experience</a></li>

</ul>
</details>

**标签**: `#AI regulation`, `#on-device AI`, `#mobile AI`, `#China`

---

<a id="item-9"></a>
## [中国零售业垂类时代结束，各玩家同台竞技](https://mp.weixin.qq.com/s/dAHAVxglD-F1RovjcvqCRw) ⭐️ 8.0/10

一项基于 257 份访谈和 5224 份问卷的研究显示，中国零售业的垂直细分时代已结束，山姆会员商店、零食折扣店、即时零售平台和拼多多正直接争夺同一笔家庭开支。山姆在华年收入预计达 1800-2000 亿元，零食店头部品牌门店近 4 万家，拼多多旗下多多买菜年销售额约 3000 亿元，年内有望冲击 4000 亿元。 这种融合标志着中国零售格局的根本性转变，传统业态边界消失，信任和物理距离成为决定性因素。对消费者和企业而言，理解这一新的竞争动态对于战略决策至关重要。 研究发现，48%的受访者计划控制消费，线下购物时距离比价格更重要——对于食品等入口商品，过低价格反而引发安全疑虑，信任成为首要竞争力。

telegram · zaihuapd · 7月15日 09:01

**背景**: 中国零售业历来按业态和价格区间细分，不同玩家服务不同消费者群体。但随着经济放缓和消费者行为转变，界限变得模糊：山姆会员店等高端仓储式卖场、拼多多等超低价电商平台、注重便利的即时零售以及价格激进的零食折扣店，如今都在争夺同一个家庭预算。即时零售可实现 30-60 分钟送达，而多多买菜（拼多多的社区团购业务）已快速扩张至数百个城市。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/posts/koppitz_instant-retail-in-china-how-are-aldi-china-activity-7423848168498397184-Wg4g">Multinational brands adopt instant retail in China with local... | LinkedIn</a></li>
<li><a href="https://en.jiemian.com/article/5833006.html">Home to the farm: Pinduoduo founder moves upstream-Jiemian Global</a></li>
<li><a href="https://asia.nikkei.com/spotlight/comment/china-discount-snack-chain-draws-crowds-of-frugal-shoppers">China discount snack chain draws crowds of frugal... - Nikkei Asia</a></li>

</ul>
</details>

**标签**: `#retail`, `#China`, `#e-commerce`, `#consumer behavior`, `#market research`

---

<a id="item-10"></a>
## [谷歌与 Epic 撤回动议，第三方应用商店将入驻 Google Play](https://www.theverge.com/policy/965792/google-epic-withdraw-injunction-third-party-app-stores-coming-google-play) ⭐️ 8.0/10

这标志着安卓应用分发格局的重大转变，可能增加竞争并降低替代应用商店的门槛，从而影响 Google 的主导地位和 Play 商店收入。 第三方商店需每年支付 5,000 美元的安全与政策审查费，不得在美国以外分发，且必须对开发者开放并有明确的信任与安全政策。美国以外地区将采用 Google 计划今年晚些时候推出的“Registered App Store”侧载方案。

telegram · zaihuapd · 7月15日 11:15

**背景**: 安卓侧载是指不通过 Google Play 商店安装应用，通常使用 APK 文件。在持续的反垄断诉讼中，Epic Games 起诉 Google 的应用商店政策。Google 新的“Registered App Store”计划将为美国以外的认证商店提供简化安装界面，且不收取交易费用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Sideloading">Sideloading - Wikipedia</a></li>
<li><a href="https://www.androidauthority.com/google-epic-changes-registered-app-stores-3646743/">Registered App Stores coming to Android this year - Android Authority</a></li>

</ul>
</details>

**标签**: `#Android`, `#Google Play`, `#Epic Games`, `#反垄断`, `#应用商店`

---

<a id="item-11"></a>
## [Telegram 推出机器人无服务器平台](https://core.telegram.org/bots/serverless) ⭐️ 8.0/10

Telegram 正式推出无服务器平台，开发者可将机器人和 Mini App 的后端代码直接运行在 Telegram 基础设施上，无需管理服务器。部署只需一条命令：npx tgcloud push。 这大大降低了机器人开发的门槛，开发者不再需要自己搭建和扩展服务器。同时与 Telegram Bot API 紧密集成，有望为数百万机器人提升性能和可靠性。 代码运行在靠近 Bot API 的隔离 V8 沙箱中，并内置 SQLite 数据库。开发者只需编写标准 JavaScript 模块并通过一条命令部署。

telegram · zaihuapd · 7月15日 16:00

**背景**: 无服务器计算允许开发者无需配置或管理服务器即可运行代码。Telegram 的平台使用 V8 沙箱隔离来安全执行不受信任的 JavaScript 代码，类似于 Cloudflare Workers 或 AWS Lambda 的运作方式。此次发布通过提供托管运行时环境，扩展了 Telegram 的机器人生态系统。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.generative.inc/ai-agent-sandboxes-the-infrastructure-layer-every-builder-needs-to-understand">AI Agent Sandboxes : Infrastructure Guide 2026 | Generative, Inc.</a></li>
<li><a href="https://www.aimadetools.com/blog/cloudflare-sandbox-ai-agents/">Cloudflare Sandbox for AI Agents: Secure Code Execution at the Edge</a></li>

</ul>
</details>

**标签**: `#serverless`, `#telegram`, `#bots`, `#platform`, `#deployment`

---