---
layout: default
title: "Horizon Summary: 2026-08-24 (ZH)"
date: 2026-08-24
lang: zh
---

> 从 26 条内容中筛选出 11 条重要资讯。

---

**科技新闻**
1. [《复杂系统如何失败》经典文章引发韧性工程讨论](#item-tech-news-1) ⭐️ 8.0/10
2. [英伟达斥 60 亿美元授权 Poolside 技术，打造 Nemotron 开源模型](#item-tech-news-2) ⭐️ 8.0/10
3. [什么是 Harness？LLM 智能体的概念框架](#item-tech-news-3) ⭐️ 7.0/10
4. [安卓车载主机固件遭恶意软件供应链攻击](#item-tech-news-4) ⭐️ 7.0/10
5. [Wi-Fi 8 不再追逐速度，转向可靠性](#item-tech-news-5) ⭐️ 7.0/10
6. [Fable 高成本促使团队重新分配编码模型](#item-tech-news-6) ⭐️ 7.0/10
7. [乌兰察布成中国 AI 算力热土，承诺容量 12.5 吉瓦](#item-tech-news-7) ⭐️ 7.0/10
8. [苹果折叠 iPhone 9 月发布售价超 2000 美元](#item-tech-news-8) ⭐️ 7.0/10

**财经新闻**
1. [英伟达通知大客户 AI 服务器涨价，涨幅普遍超 15%](#item-finance-news-1) ⭐️ 8.0/10
2. [三大运营商上半年净利润集体下滑，日均少赚约 0.61 亿元](#item-finance-news-2) ⭐️ 8.0/10
3. [阿里拟配售 800 亿港元新股，净额将全部投入 AI 建设](#item-finance-news-3) ⭐️ 8.0/10

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [《复杂系统如何失败》经典文章引发韧性工程讨论](https://how.complexsystems.fail/) ⭐️ 8.0/10

Hacker News 用户 shortcrct 提交了 Richard Cook 于 1998 年撰写的经典文章《How Complex Systems Fail》。文章指出所有有趣系统本质上都具有危险性，故障不可避免，并认为对复杂系统进行“根本原因分析”常常是徒劳的；系统依靠冗余和人的持续应对才能继续运行。社区讨论将这篇文章与现代韧性工程和混沌工程实践联系起来，例如有评论者称“无故障运行需要故障经验”正是混沌工程产生的原因。该提交并非新闻，而是一篇被广泛引用且对分布式系统、运维和可靠性工程仍有深远影响的基础文献。

hackernews · shortcrct · 8月23日 15:13 · [社区讨论](https://news.ycombinator.com/item?id=49409473)

**「背景」** 《How Complex Systems Fail》是安全研究者 Richard I. Cook 于 1998 年发表的经典论文，文中归纳了复杂系统失效模式的十八个特征。Cook 指出，复杂系统内始终存在多种潜在缺陷，系统无法在没有缺陷的状态下运行；这些缺陷单独不足以造成失败，因此往往被视为次要因素，但系统失效通常是复杂性、潜在缺陷与日常工作相互作用的结果，而非单一“根本原因”所致。该文后来被收入《Web Operations》和《Hindsight》杂志等出版物，成为理解复杂系统安全性、故障归因与系统韧性研究的重要参考文献。

**「影响」** 对于从事分布式系统、运维和可靠性工程的从业者，这篇文章提供了理解复杂系统故障动态和“根本原因分析”局限性的概念框架，并常被用来论证混沌工程等主动故障注入实践的价值。

**「社区讨论」** 多位评论者强调这篇文章的重要性，有评论者认为只有经历过复杂系统实际故障的人才能充分理解它，而“根本原因分析”在复杂系统中是徒劳的；也有评论者将文章与混沌工程直接关联，指出持续主动制造故障是为了让系统始终防御故障并获取临界点数据。另有评论者推荐 John Gall 的 Systemantics 相关著作，并对原文中“THE own nature”的写法提出疑问。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Richard_Cook_%28safety_researcher%29">Richard Cook (safety researcher) - Wikipedia</a></li>
<li><a href="https://skybrary.aero/sites/default/files/bookshelf/5926.pdf">HOW COMPLEX SYSTEMS FAIL - SKYbrary Aviation Safety</a></li>
<li><a href="https://how.complexsystems.fail/">How Complex Systems Fail</a></li>

</ul>
</details>

**标签**: `#complex systems`, `#failure analysis`, `#resilience engineering`, `#chaos engineering`, `#systems thinking`

---

<a id="item-tech-news-2"></a>
### [英伟达斥 60 亿美元授权 Poolside 技术，打造 Nemotron 开源模型](https://www.wsj.com/tech/ai/nvidia-is-spending-6-billion-to-build-a-powerful-u-s-alternative-to-chinese-ai-c51c38cc) ⭐️ 8.0/10

英伟达本周与 AI 初创公司 Poolside 达成协议，按 120 亿美元投前估值投资 10 亿美元，并另支付 60 亿美元获得其技术授权、吸纳大部分工程师，逾百名员工将加入英伟达参与开源权重模型项目 Nemotron 的研发。知情人士称，英伟达计划借此打造全球最强开源权重模型之一，与 DeepSeek、Kimi K3 等中国模型竞争，也将直接挑战 OpenAI、Anthropic 等美国闭源模型公司。该交易反映了英伟达从芯片供应商进一步深入 AI 模型层，并以开源权重路线对抗中美闭源与开源阵营的竞争格局。该报道来自《华尔街日报》，目前无更多官方细节或独立验证。

telegram · zaihuapd · 8月23日 04:20

**「背景」** Nemotron 是英伟达开发的开放权重基础模型系列，主要包括大语言模型及相关推理模型，并扩展至数据集、训练配方和开发者工具。Poolside 是一家人工智能初创公司，专注于 AI 模型构建；英伟达此次以结构化方式向其支付 60 亿美元获取技术授权，并投资 10 亿美元，这是英伟达为规避监管审查而采用的第三笔类似交易。该交易旨在强化英伟达在开源权重 AI 领域的布局，与 DeepSeek、Kimi K3 等中国模型抗衡。

**「影响」** 这项总计约 70 亿美元的交易将使英伟达直接进入开源权重模型竞赛，并目标在一年内打造全球最强开源权重模型之一，直接挑战 DeepSeek、Kimi 等中国模型，同时加剧与 OpenAI、Anthropic 等美国闭源模型公司的竞争。对依赖开源模型的开发者与 AI 生态而言，这可能带来一个由英伟达主导的高性能新选项，并进一步推动美国科技公司在该领域的军备竞赛。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Nemotron">Nemotron - Wikipedia</a></li>
<li><a href="https://www.telesurenglish.net/nvidia-ai-investment/">7 Strategic Moves in Nvidia AI Investment to... - teleSUR English</a></li>
<li><a href="https://finance.biggo.com/news/55f0389a-5b54-450a-89c2-bee817a26a4f">Nvidia Spends $7 Billion to Enter the Open-Weight Model Race, Taking Direct Aim at DeepSeek and OpenAI — BigGo Finance</a></li>
<li><a href="https://usaherald.com/poolside-deal-with-nvidia-strengthens-us-in-open-weight-ai-race/">Poolside Deal With Nvidia Strengthens US In Open-Weight AI Race - USA Herald</a></li>

</ul>
</details>

**标签**: `#Nvidia`, `#AI models`, `#open weight`, `#strategic investment`, `#competition`

---

<a id="item-tech-news-3"></a>
### [什么是 Harness？LLM 智能体的概念框架](https://earendil.com/posts/what-is-a-harness/) ⭐️ 7.0/10

《What Is a Harness?》是一篇面向非黑客读者的概念文章，探讨 LLM 智能体系统中的“harness”一词，试图为智能体工程中缺乏术语的编排与控制层建立清晰定义。文章提出的类比是：harness=底盘、模型=引擎、token=燃料、智能体=整车，强调 harness 是让模型与工具、CLI、扩展和交接流程衔接的中间层。该文并非突破性技术成果，但回应了智能体开发中术语缺口，具有实用心智模型价值。

hackernews · tosh · 8月23日 14:24 · [社区讨论](https://news.ycombinator.com/item?id=49409092)

**「背景」** 在 LLM 智能体系统中，harness（常译为“装置”或“控制层”）是一种为 AI 模型提供运行环境的软件，与模型本身不同，终端用户或软件工程师可以直接拥有并与之交互。它决定模型能看到什么、能调用哪些工具（如内部 CLI、技能/扩展），并在此意义上形成“Agent = Model + Harness”的框架。Earendil 团队在相关文章中强调这一框架过于简化，同时也在用 Pi 和 Lefos 等工具实践这一概念。

**「影响」** 对正在构建 LLM 智能体系统的开发者而言，采用“harness”这一概念有助于区分模型、接口和工具编排层，从而改善系统设计与团队沟通。

**「社区讨论」** 社区评论中，有开发者分享了为会计智能体构建内部 CLI 作为 harness 的正面经验，认为内部 CLI 对智能体极为有用；也有人询问支持跨终端/WebUI、跨成员、跨模型或跨提供方“交接”的 harness 是否存在。作者现身回应称文章面向非黑客读者，并补充了“底盘/引擎/燃料/整车”的类比；另有评论将 LLM 比作电力、harness 比作电子技术，称 Pi 因扩展系统而被认为是最好的 harness，但也有人指出工程师对工具定义无法达成一致，说明该术语仍是愿望的占位符。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://earendil.com/posts/what-is-a-harness/">What is a Harness? | EARENDIL</a></li>
<li><a href="https://earendil.com/">Welcome | EARENDIL</a></li>
<li><a href="https://harnessindex.ai/">Harness Index</a></li>

</ul>
</details>

**标签**: `#harness`, `#LLM`, `#AI agents`, `#software engineering`, `#conceptual`

---

<a id="item-tech-news-4"></a>
### [安卓车载主机固件遭恶意软件供应链攻击](https://securelist.com/android-head-unit-malware/121106/) ⭐️ 7.0/10

卡巴斯基 Securelist 发布报告称，一种恶意软件通过官方 OTA 更新进入基于 Android 的汽车车载主机固件，形成新的供应链攻击向量。该恶意软件主要影响廉价的中国后市场车载主机，而非 Android Auto，因为 Android Auto 本质上是屏幕镜像协议，主要软件运行在连接的手机上。报告指出，这类攻击无法自行传播到其他安卓车载主机，但可能被用于组建僵尸网络或作为横向移动的入口。目前攻击的具体规模、传播范围以及是否已造成实际损害尚无完整公开数据。

hackernews · campuscodi · 8月23日 13:05 · [社区讨论](https://news.ycombinator.com/item?id=49408550)

**「背景」** Android 汽车车机（head unit）是安装在车辆中控台上的嵌入式设备，通常运行完整版 Android 系统，并可能通过蓝牙、Wi-Fi 或 CAN 总线与车辆其他系统通信。卡巴斯基研究人员发现，一种名为 zhima（又名 JarService）的恶意软件通过 DoFun 等廉价后装车机厂商的官方 OTA 固件更新渠道分发，利用一个名为 installNotExists 的布尔参数安装本不存在的恶意应用，形成多阶段感染链，最终将车机纳入用于广告欺诈和代理流量的僵尸网络（可能与 BadBox 有关）。这类攻击并非通过 Android Auto 或 CarPlay 传播，因为后者仅是屏幕镜像协议，主要软件运行在连接的手机上。

**「影响」** 使用廉价安卓后装车载主机的用户即使不自行安装应用，也可能通过官方 OTA 更新渠道感染恶意软件；若车机接入 CAN 总线，还可能进一步影响车辆系统安全。

**「社区讨论」** 评论者澄清该恶意软件来自特定后装厂商的第一方 OTA 更新，不具备自我传播能力，也不影响 Android Auto；同时有人担忧车机与手机配对或连接 CAN 总线后可能成为横向移动的入口。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.technadu.com/kaspersky-finds-first-documented-android-car-head-unit-malware-using-firmware-update-mechanism-possible-links-to-badbox-botnet/633738/">Android Car Head - Unit Malware Linked to BadBox Uses... - TechNadu</a></li>
<li><a href="https://dev.to/anoymask/jarservice-zhima-malware-entering-via-insecure-android-car-head-unit-update-paths-221l">JarService / zhima Malware Entering via Insecure Android Car Head ...</a></li>
<li><a href="https://pasqualepillitteri.it/en/news/12333/first-malware-connected-cars-botnet-android-head-units">First Malware for Connected Cars Found: The Hidden Botnet Inside...</a></li>

</ul>
</details>

**标签**: `#security`, `#malware`, `#android`, `#automotive`, `#iot`

---

<a id="item-tech-news-5"></a>
### [Wi-Fi 8 不再追逐速度，转向可靠性](https://www.xda-developers.com/wi-fi-8-first-wireless-upgrade-years-isnt-chasing-speed-home-networks-need-it/) ⭐️ 7.0/10

Wi-Fi 8 被描述为多年来首个不以速度为主要卖点的无线升级，重点转向可靠性和真实网络体验，尤其针对家庭网络的痛点。文章认为这一代标准不再追求理论峰值速率，而更关注实际使用中的稳定性和连接质量。评论中则提到 Wi-Fi 8 预计在 2028 年左右落地，但客户端设备支持仍是普及的关键限制。整体来看，这次升级的意义在于让无线网络更贴近真实世界的需求，而非继续堆叠纸面速度。

hackernews · taubek · 8月23日 06:41 · [社区讨论](https://news.ycombinator.com/item?id=49406539)

**「背景」** Wi-Fi 8（即 IEEE 802.11bn）预计将在 2028 年完成最终标准化，首批产品可能在 2027 年出现。与以往几代 Wi-Fi 主要追逐峰值速率提升不同，Wi-Fi 8 把超高可靠性作为核心目标，特别适合稳定性比极限吞吐量更重要的环境。Wi-Fi 联盟和相关厂商（如高通）正在推动该标准，它被视为 5G 蜂窝网络的补充而非替代，尤其有助于改善家庭和室内场景的真实网络体验。

**「影响」** 对家庭用户来说，即使换用 Wi-Fi 7/8 路由器，如果客户端设备仍以 2.4GHz 和 5GHz 为主，实际带宽提升可能很小；真正受益的是需要稳定漫游和多设备连接的场景。

**「社区讨论」** 评论者普遍认同单纯提升理论速度意义有限：一位用户从 Wi-Fi 5 升到 Wi-Fi 7 后带宽零提升，原因是距离和墙体；另一名用户指出在 40 多台设备的家庭网络中，只有两台支持 Wi-Fi 7，约半数设备仍停留在 2.4GHz。也有用户质疑是否应直接用 5G/6G 取代 Wi-Fi，但实际部署中客户端兼容性和接入点位置仍是主要制约。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wi-Fi_8">Wi-Fi 8 - Wikipedia</a></li>
<li><a href="https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Qualcomm-Wi-Fi-8-Advancing-wireless-through-ultra-high-reliability-Part-1-white-paper.pdf">Wi-Fi 8: Advancing wireless through ultra-high reliability</a></li>
<li><a href="https://wca.org/wi-fi-8-standard/">Wi-Fi 8 Standard Stays on Track for 2028 - wca.org</a></li>

</ul>
</details>

**标签**: `#wifi`, `#networking`, `#wireless standards`, `#hardware`, `#reliability`

---

<a id="item-tech-news-6"></a>
### [Fable 高成本促使团队重新分配编码模型](https://simonwillison.net/2026/Aug/23/drew-breunig/) ⭐️ 7.0/10

Drew Breunig 在文章中表示，Anthropic 的新模型 Fable 虽然能力出色，但成本高昂，而 Opus、5.6、K3 以及 GLM 等模型在大多数编码任务上已经“足够好”。在 Fable 出现之前，团队不太需要花时间优化编码工具链或上下文策略，因为新一代模型往往以同等或更低价格解决这些问题。Fable 的出现改变了这一经济性，促使团队开始思考哪些工作该交给哪个模型，以在性能与成本之间取得平衡。Simon Willison 引用了这一观点，并标注了 Anthropic、Claude 等相关标签。

rss · Simon Willison · 8月23日 19:55

**「背景」** 本条目引用 Drew Breunig 的文章，讨论 Anthropic 新推出的前沿模型 Fable 虽然能力极强，但使用成本显著高于其他模型，这改变了团队对 AI 编程工具投入精力的态度。此前，模型迭代通常以相近或更低的价格带来性能提升，类似“摩尔定律”式的免费午餐，因此优化编码工具链（harness）或上下文策略显得不那么重要；而 Fable 的高成本促使团队开始按任务选择合适的模型，例如在大多数编码工作中使用“足够好”的 Claude Opus、5.6、K3 甚至 GLM。

**「影响」** 对开发者的直接启示是，编码工作流不再是单一“最强模型”包办，而是需要根据任务复杂度和成本，在前沿模型与低成本替代模型之间进行路由，并重新投入精力优化上下文策略和工具链。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.dbreunig.com/2026/08/23/fable-the-end-of-moore-s-law.html">Fable &amp; The End of the Free Lunch</a></li>

</ul>
</details>

**标签**: `#AI models`, `#software engineering`, `#model economics`, `#coding tools`, `#Anthropic`

---

<a id="item-tech-news-7"></a>
### [乌兰察布成中国 AI 算力热土，承诺容量 12.5 吉瓦](https://www.wired.com/story/the-unlikely-place-at-the-center-of-chinas-ai-boom/) ⭐️ 7.0/10

内蒙古乌兰察布已发展成为中国 AI 算力中心：高盛报告显示，自 2016 年以来当地已开业或开工近 100 个数据中心，中国企业承诺的总容量达 12.5 吉瓦，其中超过七成是在过去一年宣布的，规模超过 OpenAI 星际之门项目规划的 10 吉瓦。DeepSeek、字节跳动、阿里和小红书均在此自建 AI 数据中心。当地的高寒气候、低电价和邻近北京是主要吸引力，但水资源短缺成为隐忧：年降水量仅约 14 英寸，上月当地水厂被迫每晚停水 7 小时；目前约 37%的电力仍来自煤电。

telegram · zaihuapd · 8月23日 00:55

**「背景」** 数据中心选址通常看重气候、电价、网络和土地成本。乌兰察布地处内蒙古，高寒气候利于自然散热，且靠近京津冀电网枢纽，成为近年国内 AI 算力扩张的重点区域之一；全球范围内，OpenAI 与微软的星际之门项目也计划建设约 10 吉瓦的数据中心容量。

**「影响」** 乌兰察布大规模算力扩张的直接后果是当地水资源压力加剧（水厂已限时停水）和煤电占比仍高（约 37%），这可能限制后续项目落地速度。不过，这些承诺容量未必全部按时投运，实际建设进度仍有变数。

**标签**: `#AI infrastructure`, `#data centers`, `#China tech`, `#energy`, `#cloud computing`

---

<a id="item-tech-news-8"></a>
### [苹果折叠 iPhone 9 月发布售价超 2000 美元](https://www.bloomberg.com/news/newsletters/2026-08-23/apple-s-foldable-iphone-details-retail-store-changes-for-new-home-products-mt5vjf61) ⭐️ 7.0/10

彭博社 Mark Gurman 报道，苹果首款折叠 iPhone 将于 9 月 9 日前后发布，售价超过 2000 美元，但缺少长焦摄像头，并改用 Touch ID 解锁，被视为苹果近几年最令人期待的产品。苹果还计划下月对更新款 iPhone 涨价，其中 iPhone 18 Pro 可能上涨 100 美元至 1199 美元。零售店将在今秋调整布局，为带屏幕的智能家居中枢等新品腾出空间。

telegram · zaihuapd · 8月23日 14:29

**「背景」** 苹果首款折叠屏 iPhone 是多年传闻中的重磅新品，此前爆料多指向 2026 年 9 月发布，可能的命名包括 iPhone Fold、iPhone Ultra 或 iPhone Flip。不过，供应链消息对其是否因生产问题延期说法不一，有的称仍会按计划在 9 月推出，有的则暗示可能推迟。

**「影响」** 对苹果用户和高端智能手机市场而言，折叠 iPhone 的超高定价与配置取舍将直接影响新机购买决策，并可能带动 iPhone 18 Pro 等既有产品线价格进一步上调。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.macrumors.com/roundup/iphone-fold/">iPhone Fold: Everything We Know | MacRumors</a></li>
<li><a href="https://www.cnet.com/tech/mobile/iphone-fold-what-we-know-so-far-about-apples-2026-foldable/">Apple&#x27;s Foldable iPhone Ultra: Release Date, Price, and Leaks</a></li>
<li><a href="https://mobilityarena.com/apple-iphone-fold-may-not-be-shipped-in-september-2026-as-we-thought/">iPhone Fold (iPhone Ultra) 2026: Release Date, Price, Specs ...</a></li>

</ul>
</details>

**标签**: `#Apple`, `#iPhone`, `#foldable smartphone`, `#hardware`, `#consumer tech`

---

## 财经新闻

<a id="item-finance-news-1"></a>
### [英伟达通知大客户 AI 服务器涨价，涨幅普遍超 15%](https://www.bloomberg.com/news/articles/2026-08-22/nvidia-customers-notified-about-ai-related-price-hikes-above-15) ⭐️ 8.0/10

据知情人士称，英伟达已通知部分最大客户，搭载其 AI 芯片的服务器价格多数将上涨超过 15%，原因是内存芯片成本飙升；涨价适用于明年初发货的系统，涉及旗舰 Vera Rubin 和 Grace Blackwell 芯片。

telegram · zaihuapd · 8月23日 01:45

**「背景」** 英伟达已通知部分最大客户，由于内存芯片（DRAM）成本飙升，搭载其 AI 芯片的服务器价格将普遍上涨超过 15%，涨价适用于明年初发货的系统，涉及旗舰 Vera Rubin 和 Grace Blackwell 芯片。内存芯片主要由三星、SK 海力士和美光供应，供不应求使其议价能力增强。

**「影响」** 此次涨价将推高微软、谷歌、甲骨文等云服务商的 AI 服务器采购成本，并可能促使它们向企业客户转嫁算力或云服务价格。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://biz.chosun.com/en/en-international/2026/08/23/55BZNNM5HZD5VGEP5YW43LOL7E/?outputType=amp">Nvidia lifts AI server prices 15% amid memory chip squeeze - CHOSUNBIZ</a></li>
<li><a href="https://thenextweb.com/news/nvidia-ai-server-price-increase-memory-costs">Nvidia AI server prices are rising more than 15% from early next year</a></li>
<li><a href="https://finance.biggo.com/news/451a4604-e731-4952-b459-579778eca018">Nvidia AI Server Prices to Jump More Than 15% Early Next Year as Memory Chip Costs Surge — BigGo Finance</a></li>
<li><a href="https://www.financialexpress.com/market/global-markets/nvidia-ai-servers-may-get-15-costlier-what-it-signals-for-the-industry/4323644/">Nvidia AI servers may get 15% costlier — What it signals for ...</a></li>
<li><a href="https://247wallst.com/investing/2026/08/23/nvidias-15-price-hike-reveals-the-hidden-cost-of-the-ai-boom/">Nvidia&#x27;s 15% Price Hike Reveals the Hidden Cost of the AI ...</a></li>
<li><a href="https://www.chosun.com/english/industry-en/2026/08/23/AAB5QRDDVRFHNLXSUYXCT6WQ5U/">NVIDIA Raises AI Server Prices 15% Amid Memory Shortage</a></li>

</ul>
</details>

**标签**: `#Nvidia`, `#AI servers`, `#memory chips`, `#price hikes`, `#supply chain`

---

<a id="item-finance-news-2"></a>
### [三大运营商上半年净利润集体下滑，日均少赚约 0.61 亿元](https://www.guancha.cn/economy/2026_08_21_828161.shtml) ⭐️ 8.0/10

据观察者网报道，中国移动、中国电信、中国联通 2026 年上半年归属于母公司股东的净利润分别同比下降 6.3%、14.9%和 34.8%；三家合计日均盈利从去年同期的 6.28 亿元降至 5.67 亿元，相当于每天少赚约 0.61 亿元。中国联通降幅最大、接近腰斩，公司解释称受增值税政策调整和人工成本投入节奏影响；三家运营商的算力服务与智能服务等新兴业务均高速增长。

telegram · zaihuapd · 8月23日 07:34

**「背景」** 此前 2026 年一季度中国联通净利润已同比下滑 18%，并出现低价套餐调整、代理佣金削减等成本控制动作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://post.smzdm.com/p/aggd2qg6/">联 通 Q1 利 润 下 滑 18%，代理佣金被砍40...</a></li>

</ul>
</details>

**标签**: `#China telecom`, `#earnings`, `#profit decline`, `#China Mobile`, `#China Unicom`

---

<a id="item-finance-news-3"></a>
### [阿里拟配售 800 亿港元新股，净额将全部投入 AI 建设](https://www.jwview.com/jingwei/html/m/08-23/684731.shtml) ⭐️ 8.0/10

阿里巴巴 8 月 23 日宣布，拟向美国境外的非美国人士配售总额 800 亿港元的新股，这是其 2019 年港股上市以来首次启动新股配售；公司称，配售所得款项净额将全部用于投资全栈 AI 能力，并加强 AI 基础设施建设。

telegram · zaihuapd · 8月23日 08:19

**「背景」** 阿里巴巴 2019 年在香港二次上市，此次是其上市以来首次新股配售，配售对象为美国境外的非美国人士。

**「影响」** 此次配售可能摊薄现有股东持股；市场对阿里巴巴盈利下滑（据报净利下跌 75%）已有负面反应，且该交易若完成将成为香港上市企业最大规模的后续发行，或影响港股投资者情绪。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://finance.biggo.com/news/c1d0d164-9aad-4fee-9781-a3d6c750a1a9">Alibaba Launches First Share Placement Since Hong Kong Listing, Raising HK$80 Billion to Boost AI Infrastructure — BigGo Finance</a></li>
<li><a href="https://www.aol.com/articles/alibaba-proposes-hong-kong-share-044723000.html">Alibaba plans $10 billion Hong Kong share placement to fund AI spending - AOL</a></li>
<li><a href="https://www.scmp.com/tech/big-tech/article/3364957/alibaba-issue-hk80-billion-new-shares-global-ai-push">Developing | Alibaba to issue HK$80 billion in new shares for global AI push | South China Morning Post</a></li>
<li><a href="https://btw.co/node/12054819/alibaba-profit/">Alibaba Profit Trending #30 - Break The Web</a></li>
<li><a href="https://nypost.com/2026/08/23/business/alibaba-launches-10b-hong-kong-share-placement-to-fund-ai-spending/">Alibaba launches $10B Hong Kong share placement to fund AI...</a></li>

</ul>
</details>

**标签**: `#Alibaba`, `#share placement`, `#AI infrastructure`, `#Hong Kong market`, `#capital raising`

---