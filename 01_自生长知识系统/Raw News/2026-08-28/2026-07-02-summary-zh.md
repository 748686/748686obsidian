---
layout: default
title: "Horizon Summary: 2026-07-02 (ZH)"
date: 2026-07-02
lang: zh
---

> 从 43 条内容中筛选出 15 条重要资讯。

---

1. [鸡蛋价格操纵者获利远超罚款千倍](#item-1) ⭐️ 9.0/10
2. [Linux 6.9 LUKS 挂起回归导致加密密钥保留在内存中](#item-2) ⭐️ 8.0/10
3. [Podman 6.0.0 发布，带来网络和 Quadlet 升级](#item-3) ⭐️ 8.0/10
4. [PeerTube：去中心化视频平台引发关注](#item-4) ⭐️ 8.0/10
5. [F-Droid：Android 开发者验证是特洛伊木马](#item-5) ⭐️ 8.0/10
6. [日本最高法院裁定 AI 不能列为专利发明人](#item-6) ⭐️ 8.0/10
7. [定理证明经济的衰落](#item-7) ⭐️ 8.0/10
8. [Geoffrey Litt 的 '理解以参与' 理念](#item-8) ⭐️ 8.0/10
9. [ECTC 2026 综述：EMIB-T、HBM4、光子互连等](#item-9) ⭐️ 8.0/10
10. [LLM 辅助的内存管理补丁集被评估](#item-10) ⭐️ 8.0/10
11. [苹果协助 FBI 溯源 iCloud 匿名邮箱用户](#item-11) ⭐️ 8.0/10
12. [Meta 拟出售富余 AI 算力，进军云计算市场](#item-12) ⭐️ 8.0/10
13. [Cloudflare 9 月起默认拦截混合用途 AI 爬虫，点名谷歌](#item-13) ⭐️ 8.0/10
14. [企业因 AI 成本飙升限制使用](#item-14) ⭐️ 8.0/10
15. [Anthropic 与三星洽谈代工自研 AI 芯片](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [鸡蛋价格操纵者获利远超罚款千倍](https://www.thebignewsletter.com/p/crime-pays-the-egg-bandits-made-a) ⭐️ 9.0/10

调查显示，鸡蛋生产商通过价格操纵获得的利润远高于被处以的罚款，暴露出监管的不足。 这很重要，因为它表明当前的反垄断处罚力度不足以威慑非法串通行为，最终损害了支付高价的消费者。 支付的罚款仅为非法利润的一小部分，标题称操纵者获利是罚款的“一千倍”。具体金额未给出，但差距凸显了执法不力。

hackernews · toomuchtodo · 7月2日 13:25 · [社区讨论](https://news.ycombinator.com/item?id=48761229)

**背景**: 价格操纵是指竞争对手之间非法达成协议，人为抬高价格，削弱竞争并损害消费者利益。反垄断法律旨在防止此类串通行为，但罚款通常基于收入或损失计算，可能远低于实际获利。在本案中，鸡蛋生产商被指控在高蛋价时期合谋，同时将原因归咎于禽流感和通货膨胀，却暗中操纵价格。

**社区讨论**: 评论者对缺乏企业追责表示不满，有人指出个人责任缺失且企业资金被视为言论。还有人称许多人被误导，以为高蛋价是由于通货膨胀和禽流感，实际上价格操纵是主要因素。讨论还提到市场集中度是根本原因。

**标签**: `#price fixing`, `#antitrust`, `#corporations`, `#economics`, `#consumer protection`

---

<a id="item-2"></a>
## [Linux 6.9 LUKS 挂起回归导致加密密钥保留在内存中](https://mathstodon.xyz/@iblech/116769502749142438) ⭐️ 8.0/10

从 Linux 6.9 开始，`cryptsetup luksSuspend` 命令在挂起期间不再从内存中清除磁盘加密密钥，导致密钥保留在 RAM 中。 这一回归削弱了 LUKS 加密设备的安全性，因为拥有物理访问权限的攻击者可以从挂起系统的内存中提取主密钥，无需密码即可解密磁盘。 该问题影响 Linux 6.9 及更高版本的内核，但并非所有发行版都受影响，因为 `luksSuspend` 并非官方 cryptsetup 规范的一部分，它最初是 Debian 的扩展。

hackernews · IngoBlechschmid · 7月2日 15:25 · [社区讨论](https://news.ycombinator.com/item?id=48763035)

**背景**: LUKS（Linux 统一密钥设置）是一种磁盘加密规范，使用主密钥对分区上的数据进行加密。在正常操作期间，该主密钥保存在内核内存中以便即时解密。当系统挂起到 RAM 时，密钥仍留在内存中，但 `luksSuspend` 设计用于清除密钥以防止冷启动或物理攻击。这一回归意味着密钥不再被清除，从而使其容易受到攻击。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup">Linux Unified Key Setup - Wikipedia</a></li>
<li><a href="https://sesamedisk.com/linux-luks-suspend-regression-security/">Linux LUKS Suspend Regression: Keys Stay - Sesame Disk</a></li>
<li><a href="https://news.ycombinator.com/item?id=48763035">Since Linux 6.9, LUKS suspend stopped wiping disk-encryption ...</a></li>

</ul>
</details>

**社区讨论**: 社区评论显示了不同的反应：一些人认为 `luksSuspend` 并非官方支持，仅影响 Debian，而另一些人则强调此类安全回归很容易被忽视，因为一切仍然正常。少数用户低估了风险，指出如果挂起后不需要重新输入密码，加密密钥本来就应保留在内存中，磁盘加密主要保护的是驱动器被移除时的数据盗窃。

**标签**: `#Linux`, `#kernel`, `#security`, `#encryption`, `#regression`

---

<a id="item-3"></a>
## [Podman 6.0.0 发布，带来网络和 Quadlet 升级](https://blog.podman.io/2026/07/introducing-podman-v6-0-0/) ⭐️ 8.0/10

Podman v6.0.0 引入了新的网络功能，并对 Quadlet（一种将容器作为 systemd 服务运行的工具）进行了重大增强。 此重要版本巩固了 Podman 作为 Docker 领先替代品的地位，尤其对依赖 systemd 集成和强大网络功能的系统管理员和 DevOps 人员意义重大。 该版本包括网络配置和管理的改进，以及 Quadlet 从容器定义生成 systemd 单元文件的能力。建议用户查看变更日志以了解可能的不兼容变更。

hackernews · soheilpro · 7月2日 14:23 · [社区讨论](https://news.ycombinator.com/item?id=48762098)

**背景**: Podman 是由 Red Hat 开发的无守护进程容器引擎，提供与 Docker 兼容的命令行接口。Quadlet 允许用户通过简单的配置文件定义容器，并自动生成 systemd 服务来管理它们。这种方法简化了在 Linux 系统上的容器生命周期管理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.redhat.com/en/blog/quadlet-podman">Make systemd better for Podman with Quadlet</a></li>
<li><a href="https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html">podman -systemd.unit — Podman documentation</a></li>

</ul>
</details>

**社区讨论**: 社区反应不一：一些用户称赞 Podman 的改进和 Quadlet 的便利性，而另一些用户则指出与 Docker 的细微不兼容性可能会给期望完全兼容的项目带来问题。一位 macOS 用户将 Podman 的速度与 OrbStack 进行了不利比较。

**标签**: `#podman`, `#containers`, `#devops`, `#linux`

---

<a id="item-4"></a>
## [PeerTube：去中心化视频平台引发关注](https://github.com/Chocobozzz/PeerTube) ⭐️ 8.0/10

PeerTube，一个基于 ActivityPub 协议的开源去中心化视频平台，引发了社区广泛关注，讨论焦点集中在其盈利模式挑战和采用障碍上。 PeerTube 代表着向去中心化视频托管的一种潜在转变，赋予用户和创作者更多控制权，但其成功取决于解决盈利和内容发现等问题。 PeerTube 利用 P2P 技术降低服务器负载，并使用 ActivityPub 协议与其他实例互联，但目前缺乏内置的盈利机制，内容库也远小于 YouTube。

hackernews · doener · 7月2日 11:17 · [社区讨论](https://news.ycombinator.com/item?id=48759634)

**背景**: PeerTube 是 Fediverse（联邦宇宙）的一部分，Fediverse 是一个使用 ActivityPub 协议互联社交平台网络。与 YouTube 等中心化服务不同（由一家公司控制所有服务器），PeerTube 允许任何人托管一个‘pod’（服务器），该服务器可以与其他服务器通信，从而实现去中心化视频托管。该平台还使用点对点技术，让观看者之间共享带宽，从而在视频走红时减少服务器压力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/PeerTube">PeerTube - Wikipedia</a></li>
<li><a href="https://github.com/Chocobozzz/PeerTube">GitHub - Chocobozzz/PeerTube: ActivityPub- federated video ...</a></li>
<li><a href="https://docs.joinpeertube.org/contribute/architecture">Architecture | PeerTube documentation</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调盈利是专业 YouTube 创作者的最大障碍，一位用户指出制作成本高昂。一些创作者欣赏 PeerTube 适合开源项目，但感叹平台缺乏受众和内容。其他人则因为被 YouTube 封禁而转投 PeerTube。总体情绪谨慎乐观，但承认存在显著的采用障碍。

**标签**: `#decentralized`, `#video hosting`, `#open source`, `#federation`, `#PeerTube`

---

<a id="item-5"></a>
## [F-Droid：Android 开发者验证是特洛伊木马](https://f-droid.org/2026/07/01/adv-malware.html) ⭐️ 8.0/10

F-Droid 发布文章称，Google 从 2026 年 9 月开始要求验证开发者身份并注册包名的 Android 开发者验证，实际上是一种伪装成保护的威胁，尤其危害开源应用分发。 此验证可能限制在认证 Android 设备上安装来自 F-Droid 等第三方商店的应用，损害用户自由和开源生态。这代表了平台控制的更广泛趋势，影响依赖替代应用来源的开发者与用户。 Google 的开发者验证要求开发者验证身份并注册包名，从 2026 年 9 月起，在特定地区，只有已验证开发者的应用才能安装在认证 Android 设备上。F-Droid 声称这给了 Google 对应用分发的控制权，如同特洛伊木马。

hackernews · drewfax · 7月2日 03:00 · [社区讨论](https://news.ycombinator.com/item?id=48755965)

**背景**: F-Droid 是 Android 的免费开源应用仓库，提供无用户跟踪或非自由依赖的应用。Google Play 商店长期以来要求开发者注册，但从其他来源侧载通常被允许。新的验证将这一要求扩展到认证设备上的所有应用，可能阻止所有来源的未验证应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/F-Droid">F-Droid</a></li>
<li><a href="https://developer.android.com/developer-verification">Android developer verification | Android Developers</a></li>
<li><a href="https://f-droid.org/">F-Droid - Free and Open Source Android App Repository</a></li>

</ul>
</details>

**社区讨论**: 社区评论反应不一：一些人支持 F-Droid 的立场并建议切换到 GrapheneOS 等替代操作系统，另一些人则批评文章基调幼稚且适得其反。有评论指出恐慌情绪可能损害 F-Droid 的可信度。

**标签**: `#Android`, `#F-Droid`, `#developer verification`, `#open source`, `#privacy`

---

<a id="item-6"></a>
## [日本最高法院裁定 AI 不能列为专利发明人](https://japannews.yomiuri.co.jp/science-nature/technology/20260306-314930/) ⭐️ 8.0/10

日本最高法院裁定，人工智能不能列为专利申请的发明人，只有人类才能被列为发明人。 这一裁决在重要司法管辖区确立了法律先例，明确 AI 生成的发明必须有人类发明人，影响使用 AI 进行研发的公司的专利策略。 该裁决与美国和欧洲的类似立场一致，这些地区的专利局也认为 AI 系统不能作为发明人。裁决不禁止在发明过程中使用 AI，但要求有人的贡献和控制。

hackernews · mushstory · 7月2日 13:43 · [社区讨论](https://news.ycombinator.com/item?id=48761536)

**背景**: 专利法传统上要求发明人是构思发明的自然人。随着 AI 系统越来越能够生成新颖产出，世界各地的法院和专利局都在纠结 AI 是否可被视为发明人。日本的裁决强化了以人类为中心的发明人观点。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.uspto.gov/subscription-center/2025/revised-inventorship-guidance-ai-assisted-inventions">Revised inventorship guidance for AI-assisted inventions</a></li>

</ul>
</details>

**社区讨论**: 社区评论普遍支持该裁决，指出 AI 缺乏责任能力，不应拥有利益。其他人质疑实际漏洞，例如发明人在使用 AI 时只需将自己列为发明人。一些评论者引用了反对专利本身的经济学论点。

**标签**: `#AI`, `#patents`, `#intellectual property`, `#Japan`, `#legal ruling`

---

<a id="item-7"></a>
## [定理证明经济的衰落](https://davidbessis.substack.com/p/the-fall-of-the-theorem-economy) ⭐️ 8.0/10

David Bessis 认为，随着自动化证明助手和形式化的兴起，传统的定理证明经济正在衰落，数学正转向直觉和可视化。文章批评了系统对定理证明优先权的病态痴迷，而真正的进步往往发生在这一循环之外。 这很重要，因为它标志着数学实践和评估方式的转变，AI 和形式化工具正在挑战学术数学的核心激励结构。它可能将优先权重塑为洞察和理解，而非纯粹的生产定理。 Bessis 指出，在 Lean 等系统中 AI 编写的证明往往无法传达有用的人类洞察，但它们正被越来越多地使用。他主张，从证明过程中获得的直觉比证明本身更有价值。

hackernews · varjag · 7月2日 08:01 · [社区讨论](https://news.ycombinator.com/item?id=48758048)

**背景**: 证明助手是一种软件工具，通过人机协作帮助人类开发形式化证明。形式化验证使用数学方法证明系统的正确性。'定理经济'一词指的是将证明新定理作为数学成就主要货币的学术文化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Proof_assistant">Proof assistant - Wikipedia</a></li>
<li><a href="https://davidbessis.substack.com/p/the-fall-of-the-theorem-economy">The fall of the theorem economy - David Bessis</a></li>
<li><a href="https://en.wikipedia.org/wiki/Formal_verification">Formal verification - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论引用了 Greg Egan 小说《Diaspora》中的'真理挖掘'概念，预见形式化之后数学将演变为可视化和洞察。另一条评论将其与软件测试类比，认为数学家可能采用'经过实战检验'的信心文化而非形式化证明。有些人注意到该文章之前在 Hacker News 上的提交记录。

**标签**: `#mathematics`, `#formal verification`, `#theorem proving`, `#AI`, `#philosophy of mathematics`

---

<a id="item-8"></a>
## [Geoffrey Litt 的 '理解以参与' 理念](https://simonwillison.net/2026/Jul/2/understand-to-participate/#atom-everything) ⭐️ 8.0/10

Geoffrey Litt 在 AIE 会议上提出了“理解以参与”的概念，强调开发者必须深入理解 AI 生成的代码，以避免认知债务并有效与编码代理协作。 这一概念突显了 AI 辅助开发中的一个关键挑战：随着编码代理生成更多代码，开发者面临积累认知债务的风险，这可能会削弱他们指导和改进软件的能力。它将讨论从单纯的生产力转向可持续的理解。 该演讲是 AIE World's Fair 2026 的一部分，所有 300 多场录播将在三周内陆续发布。Litt 还在 Twitter 上发布了演讲的线程版本。

rss · Simon Willison · 7月2日 17:07

**背景**: 认知债务指的是开发者对代码的理解与实际代码工作方式之间日益扩大的差距，尤其是在代码由 AI 生成的情况下。在 AI 辅助开发中，开发者常常在不完全理解的情况下接受 AI 生成的代码，导致心理负担增加，并降低做出明智更改的能力。“理解以参与”理念认为，为了与编码代理有效协作，开发者必须保持足够深入的理解，以主动塑造项目。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://x.com/geoffreylitt/status/2072522267414901109">That's where another answer comes in: we can understand to ...</a></li>
<li><a href="https://dev.to/bala_paranj_059d338e44e7e/six-contradictions-behind-cognitive-debt-in-ai-assisted-development-30no">Six Contradictions Behind Cognitive Debt in AI Assisted Development</a></li>

</ul>
</details>

**标签**: `#AI-assisted development`, `#coding agents`, `#cognitive debt`, `#software engineering`

---

<a id="item-9"></a>
## [ECTC 2026 综述：EMIB-T、HBM4、光子互连等](https://newsletter.semianalysis.com/p/ectc2026) ⭐️ 8.0/10

在 ECTC 2026 上，Intel 推出了 EMIB-T，这是一种支持更大芯片尺寸和 HBM4 的先进封装技术，同时台积电、SK 海力士、三星、美光、Marvell、Lightmatter 和微软展示了定制 HBM、微流体冷却和光子互连方面的进展。 这些进展对于扩展 AI 硬件和芯片架构至关重要，因为先进封装直接影响性能、带宽和热管理。 EMIB-T 支持最大 120x180mm 的封装尺寸、超过 38 个桥接以及超过 12 个光罩尺寸的芯片。光子互连旨在用电光通路替代电气 I/O，以降低功耗并增加带宽。

rss · Semianalysis · 7月2日 17:25

**背景**: 先进半导体封装将多个芯片（小芯片）集成到一个封装中，以提高性能并降低成本。EMIB（嵌入式多芯片互连桥）是 Intel 用于高密度芯片间连接的技术。光子互连使用光进行数据传输，比电气互连提供更高的带宽和更低的功耗。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.tomshardware.com/pc-components/cpus/intel-details-new-advanced-packaging-breakthroughs-emib-t-paves-the-way-for-hbm4-and-increased-ucie-bandwidth">Intel details new advanced packaging breakthroughs — EMIB - T paves...</a></li>
<li><a href="https://lightmatter.co/knowledge-hub/how-do-photonic-interconnects-work/">How Do Photonic Interconnects Work? - lightmatter.co</a></li>

</ul>
</details>

**标签**: `#semiconductor packaging`, `#HBM`, `#photonic interconnects`, `#ECTC`, `#advanced cooling`

---

<a id="item-10"></a>
## [LLM 辅助的内存管理补丁集被评估](https://lwn.net/Articles/1080162/) ⭐️ 8.0/10

两个由资深内核开发者借助 LLM 开发的大型内存管理补丁集正在被 Linux 内核社区评估。 这标志着 AI 生成贡献被接受的方式的转变，来自受尊敬开发者的补丁被认真对待，可能为未来的 LLM 辅助工作树立先例。 其中一套由 Rik van Riel 提出的补丁引入了“超级页块”，旨在无需依赖不灵活的 hugetlbfs 预留系统即可可靠分配 1GB 大页，解决内存碎片化挑战。

rss · LWN.net · 7月2日 14:06

**背景**: 长期运行的 Linux 系统中内存碎片化使得大块连续内存分配变得困难。内核使用页块（如 4MB）来管理碎片，但 1GB 分配在没有 hugetlbfs 的情况下不可靠，而 hugetlbfs 在启动时预留内存。超级页块旨在为分配决策提供新的可见性层次。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.pingcap.com/blog/linux-kernel-vs-memory-fragmentation-1/">Memory Fragmentation in Linux: Causes, Fixes & Tools</a></li>
<li><a href="https://www.alibabacloud.com/help/en/alinux/support/solutions-to-memory-fragmentation-in-linux-operating-systems">Fix performance issues due to Linux memory fragmentation - Alibaba Cloud Linux - Alibaba Cloud</a></li>

</ul>
</details>

**社区讨论**: 文章指出，来自未知开发者的 LLM 贡献曾受到质疑，但来自资深开发者的补丁得到了更认真的评估，凸显了贡献者声誉的重要性。

**标签**: `#Linux kernel`, `#LLM`, `#memory management`, `#patch sets`, `#open source`

---

<a id="item-11"></a>
## [苹果协助 FBI 溯源 iCloud 匿名邮箱用户](https://t.me/zaihuapd/42302) ⭐️ 8.0/10

苹果向 FBI 提供了与一个用于发送威胁信息的“隐藏邮箱地址”相关联的真实 iCloud 账户信息，导致嫌疑人 Alden Ruml 被识别并承认发送威胁邮件。 此案表明，苹果宣传为隐私保护工具的“隐藏邮箱地址”功能并非完全匿名，在执法调查中可追溯到用户身份，这动摇了用户对苹果隐私承诺的信任。 嫌疑人 Alden Ruml 通过“隐藏邮箱地址”功能创建了 134 个匿名邮箱地址，并承认向 FBI 局长 Kash Patel 的女友 Alexis Wilkins 发送了威胁信息。

telegram · zaihuapd · 7月2日 01:03

**背景**: iCloud+的“隐藏邮箱地址”功能允许付费订阅用户生成唯一的随机邮箱地址，这些地址会转发到用户的个人收件箱，旨在注册服务时保护隐私。然而，苹果保留了匿名地址与用户真实 iCloud 账户之间的映射关系，并可在有效执法请求时提供此信息。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.landian.news/archives/112374.html">iCloud+ 隐 藏 邮 件 地 址 可不 能 乱用：苹果帮助FBI... | 蓝点网</a></li>
<li><a href="https://www.ithome.com/0/934/278.htm">苹果被指向美执法部门披露使用隐私邮箱用户的真实身份 - IT之家</a></li>
<li><a href="https://www.sohu.com/a/1003418999_362225">苹果“隐藏我的邮箱”功能遭挑战：向美执法部门披露用户真实信息</a></li>

</ul>
</details>

**标签**: `#privacy`, `#Apple`, `#law enforcement`, `#iCloud`, `#anonymity`

---

<a id="item-12"></a>
## [Meta 拟出售富余 AI 算力，进军云计算市场](https://www.bloomberg.com/news/articles/2026-07-02/south-korean-stocks-tumble-6-as-ai-jitters-hurt-chipmakers) ⭐️ 8.0/10

Meta 正计划向外部客户出售多余的 AI 算力和模型服务，此举标志着其可能进军云计算市场。同时，苹果正洽谈向中国存储芯片厂商 YMTC 和 CXMT 采购芯片，这两则消息导致三星电子和 SK 海力士等韩国芯片股大幅下跌。 这一进展引发市场担忧大型科技公司可能放缓 AI 基础设施投资，从而导致 AI 芯片和存储组件供应过剩。同时，苹果向中国供应商多元化采购，威胁到韩国存储龙头企业的市场主导地位。 2026 年 7 月 2 日，韩国 Kospi 指数一度下跌 7%，三星电子和 SK 海力士跌幅至少 8%，导致韩国交易所暂停了 Kospi 期货的程序化卖出。据报道，苹果正与 YMTC（NAND 闪存）和 CXMT（DRAM）洽谈，为其在中国市场销售的设备采购芯片。

telegram · zaihuapd · 7月2日 02:29

**背景**: Meta 一直在大力投资 AI 基础设施，建设大规模计算集群用于训练和推理。现在其考虑将富余算力对外销售，类似于亚马逊 AWS 源于其内部基础设施。与此同时，中国存储厂商 YMTC 和 CXMT 已能生产具有竞争力的 NAND 和 DRAM 产品，对韩国老牌厂商构成挑战。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/YMTC">YMTC</a></li>
<li><a href="https://en.wikipedia.org/wiki/CXMT">CXMT</a></li>

</ul>
</details>

**标签**: `#AI`, `#Meta`, `#Cloud Computing`, `#Semiconductors`, `#Market`

---

<a id="item-13"></a>
## [Cloudflare 9 月起默认拦截混合用途 AI 爬虫，点名谷歌](https://techcrunch.com/2026/07/01/cloudflares-new-policy-pushes-ai-companies-to-pay-for-publishers-content/) ⭐️ 8.0/10

Cloudflare 宣布，自 2026 年 9 月 15 日起，将默认拦截同时用于搜索索引和 AI 训练的“混合用途”AI 爬虫，被阻止的页面将包括带有广告的网页。该公司特别批评谷歌利用了一个漏洞：许多发布商阻止了 AI 爬虫但允许谷歌搜索爬虫，而谷歌却将抓取的内容用于 AI 训练。 这项政策迫使 AI 公司要么按功能区分爬虫，要么为内容使用付费，可能改变网络发布商与 AI 开发者之间的经济平衡。它可能为其他互联网基础设施服务商树立先例，并赋予发布商更多对其内容如何用于 AI 训练的控制权。 默认拦截适用于新注册的 Cloudflare 网站和现有免费套餐用户，付费用户可自行选择开启或关闭。此外，Cloudflare 与 Ceramic.ai 和 You.com 合作，推出了按使用付费的收入模式，允许 AI 公司根据实际使用情况向发布商支付补偿。

telegram · zaihuapd · 7月2日 05:37

**背景**: Cloudflare 是一家主要的互联网基础设施公司，为大量网站提供安全与性能服务。AI 爬虫是自动程序，用于抓取网站内容以训练大型语言模型。发布商面临两难：他们希望允许搜索引擎爬虫收录内容以提升可见度，但又不希望 AI 公司未经补偿就抓取内容用于训练。谷歌被指控忽视发布商的退出设置，并利用其搜索爬虫数据训练 AI，尽管声称其 Google-Extended 爬虫允许选择退出。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.chatai.com/posts/cloudflare-changes-ai-crawling-rules-blocking-mixed-use-ai-bots-by-default">Cloudflare Changes AI Crawling Rules, Blocking Mixed - Use ... | ChatAI</a></li>
<li><a href="https://www.wired.com/story/cloudflare-blocks-ai-crawlers-default/">Cloudflare Is Blocking AI Crawlers by Default | WIRED</a></li>
<li><a href="https://www.newsbytesapp.com/news/science/google-reveals-ai-training-loophole-in-court-testimony/story">Google can train AI using web content despite publisher opt-out</a></li>

</ul>
</details>

**标签**: `#Cloudflare`, `#AI crawlers`, `#web scraping`, `#Google`, `#publisher rights`

---

<a id="item-14"></a>
## [企业因 AI 成本飙升限制使用](https://www.404media.co/companies-are-throttling-employees-ai-use-because-its-too-expensive/) ⭐️ 8.0/10

花旗银行、Atlassian 和 Adobe 等公司正限制员工使用 GPT-5.5 和 Claude Opus 4.6 等高级 AI 模型，原因在于按用量计费模式下成本不可控地飙升。Atlassian 的月度 AI 支出从 2025 年 8 月的 500 万美元增至 2026 年 5 月的逾 1500 万美元。 这揭示了企业 AI 应用面临的具体财务挑战，与无限 AI 整合的叙事相矛盾。企业可能需要采取成本管理策略，可能减缓 AI 在业务流程中的部署。 花旗银行于 2026 年 6 月 24 日禁止了 GPT-5.5 和 Claude Opus 4.6，原因是这些模型消耗的 AI 积分过高。Atlassian 推出了成本追踪面板并终止了无限使用，Adobe 则未续签将于 2026 年 6 月 30 日到期的无限 Claude 合同。

telegram · zaihuapd · 7月2日 13:59

**背景**: GPT-5.5 是 OpenAI 于 2026 年 4 月 23 日发布的大型语言模型，以高基准分数和曾倾向于提及地精（后已修正）而闻名。Claude Opus 4.6 是 Anthropic 于 2026 年 2 月 5 日发布的旗舰模型。这些模型通过 API 以按用量计费的形式提供，企业按处理的 token 数付费，在员工大规模使用时会导致不可预测的成本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GPT-5.5">GPT-5.5</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_Opus_4.6">Claude Opus 4.6</a></li>
<li><a href="https://openai.com/index/introducing-gpt-5-5/">Introducing GPT‑5.5 - OpenAI</a></li>

</ul>
</details>

**标签**: `#AI cost`, `#enterprise AI`, `#cost management`, `#AI adoption`, `#technology news`

---

<a id="item-15"></a>
## [Anthropic 与三星洽谈代工自研 AI 芯片](https://www.theinformation.com/articles/anthropic-talks-samsung-manufacture-custom-ai-chip) ⭐️ 8.0/10

Anthropic 已启动自研 AI 芯片的开发工作，并与三星电子就潜在制造合作进行早期洽谈，旨在加强对 Claude 模型算力基础设施的控制。 此举表明 Anthropic 正战略性地向 AI 硬件垂直整合迈进，减少对谷歌和亚马逊等外部芯片供应商的依赖。若成功，有望提升 Claude 的性能和成本效率，与 OpenAI 的芯片计划类似。 该项目仍处于早期阶段，Anthropic 最终也可能决定仅购买 AI 芯片而非自研。自研 AI 芯片成本极高，研发投入可能超过 5 亿美元。

telegram · zaihuapd · 7月2日 15:57

**背景**: Meta、OpenAI 和谷歌等主要 AI 公司越来越多地自研定制芯片，以减少对英伟达 GPU 的依赖并针对自身工作负载优化。三星的晶圆代工业务近期开始有选择性地接受新客户，市场正发生变化。Anthropic 目前严重依赖谷歌 TPU 和亚马逊自研芯片来满足 Claude 的算力需求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://finance.sina.com.cn/stock/usstock/c/2026-07-02/doc-inifmrtq5832255.shtml">知情人士：Anthropic正与三星洽谈定制AI芯片代工合作_新浪财经_新浪网</a></li>
<li><a href="https://www.tradingkey.com/zh-hans/analysis/stocks/us-stock/261770244-from-openai-to-anthropic-in-house-chip-development-tradingkey">从OpenAI到Anthropic： AI巨头算力自主战打响，芯片自研成必选项？</a></li>
<li><a href="https://www.ithome.com/0/971/836.htm">现在是供方时间：消息称三星晶圆代工已开始选择性接受新客户订单 - IT...</a></li>

</ul>
</details>

**标签**: `#Anthropic`, `#AI chips`, `#semiconductor`, `#Samsung`, `#AI infrastructure`

---