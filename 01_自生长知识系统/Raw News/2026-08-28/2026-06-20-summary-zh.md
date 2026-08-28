---
layout: default
title: "Horizon Summary: 2026-06-20 (ZH)"
date: 2026-06-20
lang: zh
---

> 从 34 条内容中筛选出 14 条重要资讯。

---

1. [Project Valhalla 值类型在 JDK 28 中到来](#item-1) ⭐️ 9.0/10
2. [挪威禁止小学生使用 AI，允许青少年在监督下使用](#item-2) ⭐️ 8.0/10
3. [ATProto 没有像 Mastodon 那样的实例](#item-3) ⭐️ 8.0/10
4. [现代汽车全面收购波士顿动力](#item-4) ⭐️ 8.0/10
5. [EFF：法院记录应免费，取消 PACER 费用](#item-5) ⭐️ 8.0/10
6. [业余研究者或利用 AI 破解线形文字 A](#item-6) ⭐️ 8.0/10
7. [Systemd v261 发布，新增云实例元数据服务、启动密钥和实时更新支持](#item-7) ⭐️ 8.0/10
8. [BPF 协程允许程序挂起与恢复](#item-8) ⭐️ 8.0/10
9. [AUR 遭持续攻击：利用遗弃软件包植入恶意软件](#item-9) ⭐️ 8.0/10
10. [中国网信办就分布式数字身份监管征求意见](#item-10) ⭐️ 8.0/10
11. [智谱创始人称旗下模型或可在 2027 年一季度前达到‘Mythos’级别](#item-11) ⭐️ 8.0/10
12. [美国施压 ASML，担忧 EUV 光刻机流入中国](#item-12) ⭐️ 8.0/10
13. [Google 对侧载未验证应用设置 24 小时等待](#item-13) ⭐️ 8.0/10
14. [法院文件披露 SpaceX 向中国投资者售股](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Project Valhalla 值类型在 JDK 28 中到来](https://www.jvm-weekly.com/p/project-valhalla-explained-how-a) ⭐️ 9.0/10

经过十年的开发，Project Valhalla 的值类型最终将在 JDK 28 中到来，从根本上改变 JVM 处理对象内存布局的方式。 这显著提升了 Java 应用程序的性能和内存效率，特别是对于数据密集型工作负载，因为值类型支持密集存储，无需对象头或指针。 值类型允许对象数组连续存储且每个元素无头部开销，但堆扁平化仅限于表示不超过 64 位的对象；更大的对象仍需要间接访问。

hackernews · philonoist · 6月19日 06:35 · [社区讨论](https://news.ycombinator.com/item?id=48595511)

**背景**: Project Valhalla 是 2014 年启动的 OpenJDK 项目，旨在为 Java 引入值类型。值类型是用户定义的类型，行为类似于基本类型，没有身份标识且内存布局紧凑。这是 Java 对象模型的重大演进，旨在结合基本类型的性能与对象的抽象性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Project_Valhalla_(Java_language)">Project Valhalla (Java language)</a></li>
<li><a href="https://openjdk.org:443/projects/valhalla/">Project Valhalla</a></li>

</ul>
</details>

**社区讨论**: 社区讨论中既有对辛勤工作的赞赏，也有批评，特别是围绕空安全模型的复杂性和更大对象堆扁平化的限制。一些评论者为 Java 的演进辩护，指出 Java 自早期以来已显著改进。

**标签**: `#Java`, `#Project Valhalla`, `#JVM`, `#value types`, `#performance`

---

<a id="item-2"></a>
## [挪威禁止小学生使用 AI，允许青少年在监督下使用](https://www.reuters.com/technology/norway-imposes-near-ban-ai-elementary-school-2026-06-19/) ⭐️ 8.0/10

挪威政府宣布，几乎全面禁止 6 至 13 岁的小学生使用人工智能，同时允许 14 至 16 岁的初中生在监督下有限度地使用 AI。 这一政策为监管教育中的人工智能树立了重要先例，突显了生成式 AI 可能阻碍阅读和写作等基础学习技能的担忧。它引发了关于如何平衡 AI 潜在益处与儿童发展风险之间的讨论。 该禁令适用于一年级至七年级的学生，一般规则是禁止使用 AI，而年龄较大的学生可以在教师监督下谨慎使用 AI 工具。政府指出，儿童需要先发展核心能力，然后才能接触 AI。

hackernews · ilreb · 6月19日 16:03 · [社区讨论](https://news.ycombinator.com/item?id=48600093)

**背景**: 生成式人工智能（如 ChatGPT）可以生成类似人类的文本，引发人们担忧学生可能用它来作弊完成作业，或绕过批判性思维和写作技能的学习。许多教育工作者认为，在早期教育中禁止或严格限制 AI 是必要的，以保护基础学习，类似于在学生理解算术之前不允许使用计算器。

**社区讨论**: 评论普遍支持这项禁令，simonw 认为 13 岁以下的儿童需要在不使用 AI 的情况下学习读写。nunez 指出 AI 对学生成绩有害，禁止它需要大幅增加教师工作量。baq 建议，在适当的保障措施下，AI 可以作为辅导工具对低年级学生有用。

**标签**: `#AI in Education`, `#Regulation`, `#Norway`, `#Policy`, `#K-12`

---

<a id="item-3"></a>
## [ATProto 没有像 Mastodon 那样的实例](https://overreacted.io/there-are-no-instances-in-atproto/) ⭐️ 8.0/10

Dan Abramov 的博客文章澄清了 ATProto 不采用像 Mastodon 那样的“实例”概念，而是将功能拆分为中继（relay）、应用视图（app view）和个人数据服务器（PDS）。 这一解释消除了开发者和用户中常见的误解，突显了 ATProto 在去中心化和可扩展性方面独特的架构思路。 在 ATProto 中，中继（relay）在服务之间传输数据而不解释内容，使应用视图可以独立扩展。这种分离与 ActivityPub 基于实例的模型形成对比，后者每个服务器需处理所有功能。

hackernews · danabramov · 6月19日 15:10 · [社区讨论](https://news.ycombinator.com/item?id=48599515)

**背景**: 基于 ActivityPub 的平台（如 Mastodon）使用“实例”——独立服务器，负责承载用户账户、内容并进行联邦。ATProto 将这些角色解耦为三个独立服务：中继负责数据分发，应用视图负责用户体验，PDS 负责个人数据存储。这种设计旨在提高灵活性并降低小型运营者的运营成本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AT_Protocol">AT Protocol - Wikipedia</a></li>
<li><a href="https://atproto.com/guides/overview">Protocol Overview - AT Protocol</a></li>
<li><a href="https://docs.bsky.app/docs/advanced-guides/atproto">The AT Protocol | Bluesky</a></li>

</ul>
</details>

**社区讨论**: 评论者指出，尽管协议层面是去中心化的，但 Bluesky 公司仍运行主应用并托管大多数用户数据，导致实际上的中心化。其他人赞赏了架构的清晰性，但也对中继的成本和独立自托管的难度提出了担忧。

**标签**: `#ATProto`, `#Bluesky`, `#decentralized protocols`, `#ActivityPub`, `#social media architecture`

---

<a id="item-4"></a>
## [现代汽车全面收购波士顿动力](https://startupfortune.com/hyundai-takes-full-control-of-boston-dynamics-as-softbank-exits-for-325-million/) ⭐️ 8.0/10

现代汽车集团行使看跌期权，从软银手中收购波士顿动力剩余股份，实现对这家机器人公司的完全控股。 此举巩固了现代汽车对机器人领域的投入，可能加速像 Atlas 这样的人形机器人的商业化，以应对韩国劳动年龄人口减少的趋势。 2020 年 12 月，现代汽车最初以 8.8 亿美元收购了 80%的股份，对波士顿动力的估值为 11 亿美元。协议中包含一项看跌期权，软银现已行使该期权出售其剩余的约 9%股份。

hackernews · ck2 · 6月19日 16:28 · [社区讨论](https://news.ycombinator.com/item?id=48600312)

**背景**: 波士顿动力以先进机器人闻名，如人形机器人 Atlas 和四足机器人 Spot。软银于 2017 年从谷歌母公司 Alphabet 手中收购了它。现代汽车作为大型汽车制造商，计划将机器人技术应用于制造及其他领域，尤其是韩国预计到 2040 年劳动年龄人口将减少 25%。

**社区讨论**: 评论者就人形机器人 vs 专用机器人展开了辩论，有人认为人形机器人对制造业并非最优。另一些人将此次收购与韩国人口结构下降联系起来，认为通用机器人可以解决劳动力短缺问题。也有人对 Atlas 在汽车工厂中的直接实用性表示怀疑。

**标签**: `#robotics`, `#acquisitions`, `#Boston Dynamics`, `#Hyundai`, `#SoftBank`

---

<a id="item-5"></a>
## [EFF：法院记录应免费，取消 PACER 费用](https://www.eff.org/deeplinks/2026/06/court-records-should-be-free) ⭐️ 8.0/10

电子前哨基金会（EFF）发表文章，主张公众应免费获取法院记录，并强调 PACER 按页收费带来的经济负担。 这一点很重要，因为法院记录的高额费用阻碍了公众获取司法信息、透明度以及公民和记者监督司法系统的能力。 PACER 对联邦法院文件每页收费 1 美元，而一些州法院收费更高（例如爱达荷州每页 10 美元）。CourtListener 和 Recap 插件等工具可帮助免费分享已购买的文件。

hackernews · hn_acker · 6月19日 17:34 · [社区讨论](https://news.ycombinator.com/item?id=48600946)

**背景**: PACER（公共法院电子记录访问系统）是一个提供联邦法院文件公共访问的电子系统，但要求用户按页付费。批评者认为，既然纳税人资助法院，记录应该免费获取。EFF 长期以来一直倡导免费访问，像 CourtListener 这样的项目旨在通过众包已购买文件来绕过付费墙。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/PACER_(law)">PACER (law) - Wikipedia</a></li>
<li><a href="https://pacer.uscourts.gov/">Public Access to Court Electronic Records | PACER: Federal ...</a></li>
<li><a href="https://www.uscourts.gov/court-records/find-a-case-pacer">Find a Case (PACER) - United States Courts</a></li>

</ul>
</details>

**社区讨论**: 评论者指出了州法院更高的费用，赞扬了 CourtListener 和 Recap 填补了关键空白，并认为政府故意限制公民获取权利。有人建议应让大型律所和数据收集者等经批准的合作伙伴免费访问，而另一些人则强调法院裁决就是法律，应可免费阅读。

**标签**: `#legal tech`, `#open data`, `#access to justice`, `#PACER`, `#public records`

---

<a id="item-6"></a>
## [业余研究者或利用 AI 破解线形文字 A](https://aiclambake.com/clamtakes/linear-a/) ⭐️ 8.0/10

业余研究者汤姆·迪米诺利用 Claude Code 构建了分析线形文字 A 语料的 Python 脚本，声称已翻译超过 300 个单词。其研究成果目前正由罗格斯大学和剑桥大学的语言学专家评审。 若经证实，这将是线形文字 A 首次被破译——该文字体系一个多世纪以来一直未能被解读。同时，这也展示了 AI 工具如何在复杂的密码学和语言学研究中发挥作用。 研究者使用 Claude Code 创建了一套 Python 脚本，用于查询、交叉引用和整理来自 GORILA 和 SigLA 数据库的数字化线形文字 A 语料。该语料总共只有约 7500 个字符，分布在约 1500 条铭文中，使得系统性分析极其困难。

hackernews · Kosturdistan · 6月19日 16:04 · [社区讨论](https://news.ycombinator.com/item?id=48600107)

**背景**: 线形文字 A 是克里特岛米诺斯文明在公元前 1800 年至 1450 年间使用的文字系统。自 1900 年被重新发现以来一直未能破译，而其后继文字线形文字 B 已于 20 世纪 50 年代被破译，代表迈锡尼希腊语。语料规模小以及缺乏双语对照文本是主要障碍。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Linear_A_script">Linear A script</a></li>
<li><a href="https://www.worldhistory.org/Linear_A_Script/">Linear A Script - World History Encyclopedia</a></li>

</ul>
</details>

**社区讨论**: 评论者表达了谨慎的乐观态度，指出该研究者的工作正在接受专家评审，且其方法产生了切实成果（翻译了 300 多个单词）。一些人强调语料规模极小（7500 个字符）并提醒注意虚假声称，但使用 AI 工具被视为一种有前景的研究方法。

**标签**: `#Linear A`, `#cryptography`, `#AI-assisted research`, `#ancient scripts`, `#linguistics`

---

<a id="item-7"></a>
## [Systemd v261 发布，新增云实例元数据服务、启动密钥和实时更新支持](https://lwn.net/Articles/1078708/) ⭐️ 8.0/10

Systemd v261 引入了新的云实例元数据服务（IMDS）子系统、面向无 TPM 系统的“启动密钥”机制，以及对内核实时更新编排（LUO）和 Kexec Handover（KHO）的支持。 这些新增功能显著增强了 systemd 在云和安全场景下的能力，实现了更可靠的实例元数据获取、非 TPM 硬件上的加密密钥，以及无缝的内核实时更新，对系统管理和云编排工作流产生影响。 IMDS 守护进程提供基于 Varlink 的接口，并包含可供 cloud-init 等工具使用的 CLI 命令；启动密钥功能允许在没有物理 TPM 的情况下将密钥绑定到启动阶段。LUO/KHO 支持可在基于 kexec 的内核更新中保留有状态的文件描述符。

rss · LWN.net · 6月19日 18:56

**背景**: Systemd 是大多数主流 Linux 发行版使用的初始化系统和服务管理器。IMDS 是一种云功能，提供关于运行中实例的元数据（如 IP 地址、主机名），通常通过 HTTP 访问；将其集成到 systemd 中可标准化访问。启动密钥允许加密绑定到启动过程的敏感数据，传统上依赖 TPM（可信平台模块）芯片。实时更新编排和 Kexec Handover 是内核就地更新机制，无需完全重启即可保留关键状态。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lwn.net/Articles/1033364/">Kexec handover and the live update orchestrator [LWN.net]</a></li>
<li><a href="https://lwn.net/Articles/1001730/">Systemd takes steps toward a more secure boot process [LWN.net]</a></li>
<li><a href="https://github.com/systemd/systemd/issues/40763">Instance Metadata Service (IMDS) daemon integrated into systemd ...</a></li>

</ul>
</details>

**标签**: `#systemd`, `#linux`, `#system-administration`, `#cloud`, `#init-system`

---

<a id="item-8"></a>
## [BPF 协程允许程序挂起与恢复](https://lwn.net/Articles/1076210/) ⭐️ 8.0/10

Kumar Kartikeya Dwivedi 在 LSFMM+BPF 2026 上提出一种设计，允许将 BPF 程序表达为协程，从而实现挂起与恢复。 这一变化简化了编写长时间运行的 BPF 任务（如堆栈跟踪收集或用户空间网络）的方式，避免了手动拆分为回调，使内核扩展更易于开发。 该设计使用无栈协程，类似于 Rust 的 async 或 C++ 协程，编译器重写代码以实现挂起/恢复，BPF 验证器将恢复视为间接函数调用。

rss · LWN.net · 6月19日 15:55

**背景**: BPF（伯克利包过滤器）程序传统上在同一上下文中运行至完成。为了处理多步骤任务，开发者必须将逻辑拆分为独立的钩子并手动管理状态。协程允许单个函数暂停并在之后恢复，这对于长时间运行或延迟操作至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://bpfconf.ebpf.io/bpfconf2026/bpfconf2026_material/Coroutines+in+BPF+-+LSF_MM_BPF+May+2026.pdf">Coroutines in BPF - LSF/MM/BPF May 2026 - bpfconf.ebpf.io</a></li>

</ul>
</details>

**标签**: `#BPF`, `#Linux kernel`, `#coroutines`, `#LSFMM`, `#kernel development`

---

<a id="item-9"></a>
## [AUR 遭持续攻击：利用遗弃软件包植入恶意软件](https://lwn.net/Articles/1077619/) ⭐️ 8.0/10

Arch 用户仓库（AUR）正遭受持续攻击，恶意行为者通过认领遗弃软件包来推送恶意软件。AUR 团队已于 2026 年 6 月 19 日暂时关闭新用户注册，以阻止攻击者账号涌入。 此次攻击削弱了用户对 AUR 的信任，而 AUR 是 Arch Linux 用户获取官方仓库之外软件的关键社区仓库。该事件暴露了 AUR 信任模型中的根本性安全缺陷，可能促使其治理结构发生重大变革。 AUR 托管超过 107,000 个软件包，其中近 14,000 个为遗弃软件包，任何注册用户均可无需审核直接认领。攻击者创建新账号认领遗弃软件包，然后推送包含恶意代码的 PKGBUILD 文件来安装恶意软件。

rss · LWN.net · 6月19日 14:40

**背景**: Arch 用户仓库（AUR）是一个由社区驱动的 Arch Linux 软件仓库，用户在此共享用于从源码构建软件的 PKGBUILD 脚本。与官方仓库不同，AUR 软件包在发布或更新前无需经过正式审核。遗弃软件包是指没有维护者的软件包，任何注册用户均可自由认领。许多 Arch Linux 用户依赖 yay 或 paru 等 AUR 辅助工具来管理 AUR 软件包。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Arch_User_Repository">Arch User Repository</a></li>
<li><a href="https://wiki.archlinux.org/title/Arch_User_Repository">Arch User Repository - ArchWiki</a></li>

</ul>
</details>

**标签**: `#security`, `#Arch Linux`, `#AUR`, `#attacks`, `#open source`

---

<a id="item-10"></a>
## [中国网信办就分布式数字身份监管征求意见](https://www.cac.gov.cn/2026-06/18/c_1783525605384124.htm) ⭐️ 8.0/10

国家网信办于 2026 年 6 月 18 日发布《促进分布式数字身份互通互认应用规定（征求意见稿）》，向社会公开征求意见，截至 7 月 18 日。 若正式实施，该规定将为中国建立分布式数字身份的国家框架，可能实现金融、交通、海关、数字人民币等领域的跨平台身份互通互认，并为政府支持的区块链身份系统树立先例。 征求意见稿将分布式数字身份定义为由标识符、密钥、可验证凭证和可验证声明构成，并提议依托国家区块链网络建设身份链，实现跨平台互认。

telegram · zaihuapd · 6月19日 01:39

**背景**: 分布式数字身份（DDID）允许用户自主控制身份数据，无需依赖中央权威机构，利用区块链实现防篡改记录。可验证凭证（VC）是遵循 W3C 标准的数字文档，支持对声明的加密验证。该规定与全球走向自主主权身份（SSI）的趋势一致。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Verifiable_credentials">Verifiable credentials</a></li>
<li><a href="https://chain.link/education-hub/blockchain-identity">Digital Identity on the Blockchain With Chainlink | Chainlink</a></li>
<li><a href="https://www.dock.io/post/blockchain-identity-management">Blockchain Identity Management: Beginner's Guide 2026</a></li>

</ul>
</details>

**标签**: `#decentralized identity`, `#blockchain`, `#regulation`, `#digital identity`, `#China`

---

<a id="item-11"></a>
## [智谱创始人称旗下模型或可在 2027 年一季度前达到‘Mythos’级别](https://x.com/jietang/status/2067580270078030088) ⭐️ 8.0/10

智谱 AI 创始人唐杰反驳了一位用户关于中国 AI 实验室需到 2026 年底才能达到 Anthropic 的 Mythos 级别模型的评估，公开表示其公司进展会更快，可能在 2027 年第一季度前达到该里程碑。埃隆·马斯克也参与了讨论，认同 2027 年第一季度的预测。 这一交流凸显了中美 AI 实验室之间日益激烈的竞争，高层人物公开争论前沿模型能力的时间线。其结果可能影响投资者信心、研究优先级以及对全球 AI 竞赛的看法。 原始用户评估认为智谱的 GLM-5.2 模型大约相当于 Claude Opus 4.7–4.8 的水平，暗示中美模型差距约 7 个月。Anthropic 的 Mythos（也称 Fable）是一款前沿 AI 模型，于 2026 年 4 月预览，以强大的代理编程和推理能力著称。

telegram · zaihuapd · 6月19日 02:24

**背景**: Anthropic 的 Mythos 是一款下一代大语言模型，因其先进的代理编程和推理能力而备受瞩目，代表了超越 Claude Opus 系列的重大飞跃。智谱 AI 的 GLM-5.2 于 2026 年 6 月发布，拥有 1M token 的上下文窗口，专为长代理任务和编程设计。Claude Opus 系列（如 Opus 4.7）是 Anthropic 的旗舰推理模型，常被用作比较模型性能的基准。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://techcrunch.com/2026/04/07/anthropic-mythos-ai-model-preview-security/">Anthropic debuts preview of powerful new AI model Mythos in new</a></li>
<li><a href="https://forklog.com/en/zhipu-ai-launches-glm-5-2-with-1-million-token-context/">Zhipu AI Launches GLM-5.2 with 1 Million Token Context | ForkLog</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude (language model ) - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 埃隆·马斯克回复‘Probably Q1’，被解读为 2027 年第一季度；唐杰则直接回应‘won’t take that long’，声称进展更快。讨论显示了中美双方人物的乐观态度和竞争动力。

**标签**: `#AI`, `#LLM`, `#ZhiPu`, `#model comparison`, `#China AI`

---

<a id="item-12"></a>
## [美国施压 ASML，担忧 EUV 光刻机流入中国](https://www.bloomberg.com/news/articles/2026-06-19/us-tells-asml-it-s-concerned-china-may-have-top-chip-tool) ⭐️ 8.0/10

美国商务部长卢特尼克近日向 ASML 高管表示，怀疑一台 EUV 光刻机可能已非法流入中国，违反出口管制。ASML 坚决否认，称从未向中国出口完整的 EUV 系统，全球 314 台运行中的设备均不在中国。 这一指控可能加剧美欧在半导体出口管制上的紧张关系，并影响美国国会正在推动的更严格对华限制法案。它还可能威胁全球芯片供应链的稳定以及人工智能和机器学习所需先进硬件的供应。 美方官员声称掌握 ASML 未善意行事的证据，包括对华出口 EUV 相关运输设备，但拒绝出示。ASML 已散发文件自证清白，并反驳称从未出口任何 EUV 专用组件。

telegram · zaihuapd · 6月19日 03:09

**背景**: 极紫外（EUV）光刻是当前最先进的半导体制造技术，对生产 7 纳米以下的尖端芯片至关重要。由于其战略重要性，EUV 系统受到严格的出口管制，美国主导阻止中国获取这些设备。荷兰的 ASML 是 EUV 光刻机的唯一制造商。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.elecfans.com/article/89/2023/202310302282517.html">什么是 EUV 光 刻 ？ EUV 与DUV 光 刻 的区别 - 制造/封装 - 电子发烧友网</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#export control`, `#EUV lithography`, `#US-China tech war`, `#chip supply chain`

---

<a id="item-13"></a>
## [Google 对侧载未验证应用设置 24 小时等待](https://t.me/zaihuapd/42054) ⭐️ 8.0/10

Google 在 Android 上推出了新的侧载流程，要求用户在安装未验证开发者应用前等待 24 小时并完成多项验证步骤。 这一变化通过增加步骤来阻止恶意侧载应用和诈骗，提高了 Android 用户的安全性，同时也改变了长期以来开放的侧载生态。 新流程包括开启开发者模式、确认并非被诱导、重启设备、一次性的 24 小时冷静期，以及安装前的指纹、面容或 PIN 验证。

telegram · zaihuapd · 6月19日 07:59

**背景**: 侧载允许用户在 Google Play 官方商店之外安装应用，提供了灵活性但也带来安全风险。Google 一直在加强侧载限制以打击诈骗，这一新的高摩擦流程旨在让诈骗者更难诱骗用户安装恶意应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.androidauthority.com/google-android-sideloading-unverified-apps-new-rules-3650343/">Android's new sideloading rules are here, and they come with ...</a></li>
<li><a href="https://www.zdnet.com/article/how-google-android-sideloading-crackdown-works-limits/">Google's big Android sideloading crackdown has a 24-hour ...</a></li>

</ul>
</details>

**标签**: `#Android`, `#sideloading`, `#security`, `#Google`, `#app installation`

---

<a id="item-14"></a>
## [法院文件披露 SpaceX 向中国投资者售股](https://www.propublica.org/article/spacex-elon-musk-ipo-foreign-investors-china) ⭐️ 8.0/10

ProPublica 获得的法院文件显示，SpaceX 在近期 IPO 前，通过中间商 Tomales Bay Capital，在 2018 年至 2021 年间向至少十几名位于中国大陆、香港和俄罗斯的投资者出售股份，而 IPO 时却禁止此类投资者参与。 此事引发对美国国家安全法规合规性的严重担忧，因为 SpaceX 承担敏感军事项目，可能危及政府合同和声誉。 投资者包括与中国军工承包商有关联的商界人士及卡塔尔王室关联实体，单笔投资额从 80 万到 4000 万美元不等；SpaceX 估值从 2019 年的 333 亿美元飙升至 2.7 万亿美元，早期投资获得巨额回报。

telegram · zaihuapd · 6月19日 12:00

**背景**: SpaceX 是美国领先的航空航天公司，拥有包括军事发射在内的敏感政府合同。美国法律限制外国投资国防相关企业。该公司 IPO 招股说明书以监管与合规风险为由禁止中国和香港投资者参与。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/company/tomales-bay-capital">Tomales Bay Capital | LinkedIn</a></li>
<li><a href="https://raizer.app/investor/tomales-bay-capital">Tomales Bay Capital – VC Investor Profile & Insights</a></li>

</ul>
</details>

**标签**: `#SpaceX`, `#IPO`, `#compliance`, `#national security`, `#foreign investment`

---