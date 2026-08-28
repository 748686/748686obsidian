---
layout: default
title: "Horizon Summary: 2026-08-03 (ZH)"
date: 2026-08-03
lang: zh
---

> 从 21 条内容中筛选出 5 条重要资讯。

---

**科技新闻**
1. [Kakehashi：在 Linux ARM 上运行 macOS 二进制的实验性用户态](#item-tech-news-1) ⭐️ 7.0/10
2. [eBay 安全团队骚扰批评者 判赔 5600 万美元](#item-tech-news-2) ⭐️ 7.0/10
3. [AI 公开信：企业支持开放权重，员工呼吁管控前沿](#item-tech-news-3) ⭐️ 7.0/10

**财经新闻**
1. [高盛交易业务有望创纪录，二季度股票交易收入激增 72%](#item-finance-news-1) ⭐️ 8.0/10
2. [公积金条例拟修订：灵活就业人员可缴存，装修物业费可提取](#item-finance-news-2) ⭐️ 7.0/10

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [Kakehashi：在 Linux ARM 上运行 macOS 二进制的实验性用户态](https://github.com/wie-project/kakehashi) ⭐️ 7.0/10

Kakehashi 是一个实验性用户态项目，目标是在 Linux ARM 机器上原生运行 macOS 命令行二进制。目前已有 7-Zip、curl 和 Xcode Git 的工作原型：7-Zip 通过 8k 文件树的多线程压缩测试，但比原生 Linux 执行慢约 5.2 倍；curl 的 200 多个命令和选项通过自动化 Docker 测试；Xcode Git 支持基本版本控制。项目处于早期阶段，尚未成熟，但开发者已规划优化方案以缩小性能差距。

hackernews · vlad\_kalinkin · 8月2日 16:26 · [社区讨论](https://news.ycombinator.com/item?id=49145937)

**「背景」** Kakehashi 是一个面向 Linux ARM64（aarch64）的 macOS 二进制翻译层，采用纯用户态方案，不依赖内核模块，也不使用 JIT。它加载 Darwin 平台的 Mach-O 可执行文件，在 Linux 进程中作为普通用户代码运行，并提供独立的 libSystem 实现和 BSD 系统调用翻译。另一个更广为人知的类似项目是 Darling，它旨在为 Linux 提供完整的 macOS 兼容层，但目前在 x86/x64 上支持较好，ARM64 支持仍在开发中；Kakehashi 则更专注于命令行工具，属于早期实验性项目。

**「影响」** 对 Linux ARM 用户而言，该项目提供了在本机运行部分 macOS 命令行工具（7-Zip、curl、Git）的实验性路径，但当前性能开销和成熟度仍不足以支撑生产环境。

**「社区讨论」** 评论区普遍表示期待，认为该方向类似 WINE/Proton 对 Windows 的价值；有评论询问是否与 Darling 项目及其 ARM64 PR 合作或目标不同，也有用户希望未来能实现类似 yabridge 的机制，在 Linux 上运行 macOS 音频单元（AU）插件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/wie-project/kakehashi">GitHub - wie - project / kakehashi : Userspace macOS translation layer...</a></li>
<li><a href="https://github.com/wie-project/kakehashi/blob/main/docs/architecture.md">kakehashi /docs/architecture.md at main · wie - project / kakehashi</a></li>
<li><a href="https://en.wikipedia.org/wiki/Darling_%28software%29">Darling (software) - Wikipedia</a></li>
<li><a href="https://github.com/darlinghq/darling">GitHub - darlinghq/darling: Darwin/macOS emulation layer for ... Architectures supported · darlinghq darling · Discussion ... Build instructions - Darling Docs Darling download | SourceForge.net Introduction - Darling Docs Darling (software) - Wikipedia</a></li>

</ul>
</details>

**标签**: `#macOS`, `#Linux`, `#ARM`, `#binary compatibility`, `#open source`

---

<a id="item-tech-news-2"></a>
### [eBay 安全团队骚扰批评者 判赔 5600 万美元](https://www.ft.com/content/06ec1b03-d4af-40cf-b12a-4ba5a410f6d2) ⭐️ 7.0/10

据英国《金融时报》报道，eBay 全球安全团队针对批评者发起骚扰和恐吓活动，最终导致 eBay 支付 5600 万美元和解金。前安全与安保高级总监 Jim Baugh 被判 57 个月监禁，前特别行动高级经理 Brian Gilbert 被判已服刑时间、一年监督释放并罚款 2 万美元，前全球恢复力总监 David Harville 也被判刑。美国检察官表示，七名团队成员（包括前警长）共同参与对受害者的骚扰和胁迫。该案成为科技公司安全部门滥用权力并被追究刑事责任的标志性法律案例。

hackernews · JumpCrisscross · 8月2日 19:19 · [社区讨论](https://news.ycombinator.com/item?id=49147435)

**「背景」** 2019 年，eBay 全球安全团队的高管（包括前高级安全主管吉姆·鲍等）针对批评该平台的马萨诸塞州夫妇伊娜和大卫·施泰纳发起了一场骚扰与恐吓行动，包括监视、跟踪以及寄送蟑螂、死猪和带血猪面具等物品。此后，eBay 与多名前高管在民事诉讼中同意支付近 5600 万美元和解，部分涉事前高管还在联邦刑事案件中被判入狱（例如吉姆·鲍被判处 57 个月监禁）。

**「影响」** 对美国科技企业及其内部安全团队而言，这一案件意味着针对批评者、记者或用户的报复性骚扰可能同时导致巨额民事赔偿和刑事起诉，从而显著提高此类行为的法律风险。

**「社区讨论」** 评论区有用户质疑调查是否仅限于这一对批评者，并希望检方进一步调查涉案前警长是否还有类似行为；另有用户引用 Scott Adams 关于无人监督时人会作恶的观点，认为企业应加强内部监督。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/news/story/ebay-settles-harassment-case-with-bloggers-for-nearly-56m-9082914/">EBay settles harassment case with bloggers for nearly $ 56 M | LinkedIn</a></li>
<li><a href="https://moneywise.com/news/top-stories/ebay-harassment-settlement-56-million">eBay execs who allegedly harassed journalists to pay $ 56 M</a></li>
<li><a href="https://dailycaller.com/2026/07/31/cockroaches-pig-mask-ebay-56-million-steiners-settlement-massachusetts-court/">Cockroaches, Bloody Pig Mask: eBay Forks Over $ 56 Million To...</a></li>

</ul>
</details>

**标签**: `#eBay`, `#tech industry`, `#corporate security`, `#legal`, `#ethics`

---

<a id="item-tech-news-3"></a>
### [AI 公开信：企业支持开放权重，员工呼吁管控前沿](https://simonwillison.net/2026/Aug/2/open-letters/#atom-everything) ⭐️ 7.0/10

微软于 7 月 24 日发布题为《开放权重与美国 AI 领导力》的公开信，截至目前已有 235 家 AI 相关公司签署，包括英伟达、亚马逊、Y Combinator、Linux 基金会及后来加入的 OpenAI，信中主张开放权重模型更安全、反对仅依赖封闭模型，并支持蒸馏作为合法的模型开发技术。Anthropic 未签署，三天后发布自己的立场文件，CEO Dario Amodei 呼吁打击工业化蒸馏运营，但同时表示从未主张禁止开放权重模型。7 月 28 日，1324 名前沿 AI 公司员工签署《Pacing the Frontier》公开信，呼吁美国政府支持国际努力，开发技术和治理工具以有意识地掌控自动化 AI 研发的推进节奏。信中还引用了 Anthropic 有 80%代码由 Claude Code 生成、OpenAI 的 Sol 将端到端服务成本降低 20%、Kimi K3 为基于自身架构的 nano 模型设计芯片等例证，说明自动化 AI 研究带来的竞争压力正在加剧。这些公开信是针对美国政府在安全担忧下可能限制开放权重模型的明确游说回应。

rss · Simon Willison · 8月2日 04:16

**「背景」** 开放权重模型指公开模型权重但可能限制使用或再分发，允许开发者检查行为、发现漏洞和构建改进；封闭模型则集中于少数供应商，难以外部审计。蒸馏是一种用其他模型输出训练或改进模型的通用技术，在行业中广泛使用，但也被指可能被大规模滥用。此前美国政府对 Claude Fable 5 的访问暂停事件，促使业界担心当局会以安全为由限制开放权重。

**「影响」** 对依赖开放权重模型和蒸馏技术的开发者、创业公司与研究机构而言，这些公开信显示美国政策可能走向收紧，同时也为支持开放路线的技术社区提供了被广泛引用的行业立场。但 Anthropic 与前沿实验室员工的立场表明，业界对如何管控前沿自动化研发仍存在明显分歧。

**标签**: `#AI policy`, `#open source`, `#AI industry`, `#technology news`

---

## 财经新闻

<a id="item-finance-news-1"></a>
### [高盛交易业务有望创纪录，二季度股票交易收入激增 72%](https://www.cnbc.com/2026/08/01/goldman-traders-are-on-pace-for-a-record-year-a-close-up-look-at-how-theyre-doing-it.html) ⭐️ 8.0/10

高盛第二季度股票交易收入同比飙升 72%，达到创纪录的 74.2 亿美元，超出分析师预期，使其交易业务有望创下全年纪录。

rss · CNBC Finance · 8月2日 13:52

**「背景」** 高盛近年来加大对股票业务的投入并调整全球银行与市场部门策略，通过投资银行和财富管理业务带动股票服务客户增长。

**标签**: `#Goldman Sachs`, `#equities trading`, `#investment banking`, `#earnings`, `#market volatility`

---

<a id="item-finance-news-2"></a>
### [公积金条例拟修订：灵活就业人员可缴存，装修物业费可提取](https://weibo.com/1642634100/RbwfKezfq) ⭐️ 7.0/10

住建部近日就《住房公积金管理条例（修订征求意见稿）》公开征求意见，拟允许个体工商户、外卖员、快递员、网约车司机等灵活就业人员自愿缴存住房公积金，并将自住住房装修、支付物业费纳入提取范围。该内容目前仍是征求意见稿，尚未正式实施。

telegram · zaihuapd · 8月2日 06:32

**「背景」** 现行《住房公积金管理条例》自 2002 年修订后沿用多年，此次是时隔七年再次启动修订。住建部发布的征求意见稿仍处于公开征求意见阶段，尚未正式生效；其核心导向是使公积金制度更好满足缴存人不同阶段的住房消费需求，并强化跨地区业务协同。

**「影响」** 如果修订最终落地，灵活就业人员可自愿建立公积金账户并获得相应住房支持，有自住住房的家庭也可申请提取公积金用于装修或缴纳物业费，相关规则将影响大量新市民、青年人和灵活就业群体。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://sfj.jcs.gov.cn/zwgk/zcwj/art/2026/art_5fb98ef143c845a3aaaed463b7ebf7b0.html">《住房公积金管理条例（修订征求意见稿）》公开征求意见</a></li>
<li><a href="https://news.cctv.cn/2026/06/05/ARTIQ5apQEKDzRBsMmZ0MWqv260605.shtml">住建部就《住房公积金管理条例（修订征求意见稿）》公开征求意见_新闻频道_央视网 (cctv.com)</a></li>

</ul>
</details>

**标签**: `#housing policy`, `#China`, `#provident fund`, `#flexible employment`, `#housing consumption`

---