---
layout: default
title: "Horizon Summary: 2026-06-25 (ZH)"
date: 2026-06-25
lang: zh
---

> 从 31 条内容中筛选出 6 条重要资讯。

---

1. [OpenAI 携手博通推出首款自研 AI 芯片 Jalapeño](#item-1) ⭐️ 9.0/10
2. [Bunny DNS 免费推出，无查询限制](#item-2) ⭐️ 8.0/10
3. [GitHub 上的 PR 垃圾信息堪比 2000 年代初的邮件垃圾信息](#item-3) ⭐️ 8.0/10
4. [卡马克反思早期错误，称雷神之锤值得](#item-4) ⭐️ 8.0/10
5. [生成式 AI 可能降低中国学生考试成绩](#item-5) ⭐️ 8.0/10
6. [美光 26Q3 营收同比暴增 346%，净利润 282 亿美元](#item-6) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [OpenAI 携手博通推出首款自研 AI 芯片 Jalapeño](https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom/) ⭐️ 9.0/10

OpenAI 宣布推出其首款自研 AI 推理芯片 Jalapeño，由博通合作开发、台积电制造，开发过程借助 OpenAI 自身模型加速。 这标志着 OpenAI 在减少对外部芯片供应商依赖方面迈出重要一步，能够优化 AI 推理工作负载的成本和效率，可能影响 AI 硬件格局。 该芯片是一款专为推理优化的专用集成电路（ASIC），从设计到生产仅用时九个月，部分环节由 OpenAI 自身 AI 模型加速。

hackernews · jamdesk · 6月24日 17:47 · [社区讨论](https://news.ycombinator.com/item?id=48663324)

**背景**: AI 推理芯片是专门用于运行已训练好的 AI 模型进行预测的处理器，区别于训练芯片。ASIC 是为特定任务定制的芯片，比通用处理器效率更高。通过自研芯片，OpenAI 旨在降低推理成本并提升 ChatGPT 等服务的性能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Application-specific_integrated_circuit">Application-specific integrated circuit - Wikipedia</a></li>
<li><a href="https://aws.amazon.com/ai/machine-learning/inferentia/">AI Chip - Amazon Inferentia - AWS</a></li>

</ul>
</details>

**社区讨论**: 社区评论中，有用户对 AI 加速设计的说法表示怀疑，认为可能只是营销手段。其他人则指出台积电是制造商，并讨论了将权重固化到硅片等更专门化芯片的可能性，还提及了 Taalas 等类似项目。

**标签**: `#AI`, `#hardware`, `#chip design`, `#OpenAI`, `#inference`

---

<a id="item-2"></a>
## [Bunny DNS 免费推出，无查询限制](https://bunny.net/blog/were-making-bunny-dns-free/) ⭐️ 8.0/10

Bunny DNS 宣布现在完全免费，无查询次数限制，每个账户最多支持 500 个域名，并包含智能记录和健康监控等功能。 此举使 Bunny 成为 Cloudflare DNS 服务的强大欧洲替代品，可能通过降低开发者和企业寻求高性价比 DNS 托管服务的门槛来扰乱市场。 免费套餐包括最多 500 个域名的 DNS 托管，无查询限制，无按请求计费，并可使用脚本记录和健康监控等高级功能，这些功能在其他地方通常需要付费。

hackernews · dabinat · 6月24日 08:50 · [社区讨论](https://news.ycombinator.com/item?id=48657030)

**背景**: DNS（域名系统）是一项基础互联网技术，将人类可读的域名转换为 IP 地址。传统上，DNS 托管服务根据查询次数或域名数量收费。Bunny.net 是一家位于欧盟的内容交付网络和边缘服务提供商，此次推出免费 DNS 旨在通过取消 DNS 查询费用与 Cloudflare 等主要厂商竞争。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://bunny.net/dns/">Bunny DNS | The #1 Scriptable DNS Platform | bunny.net</a></li>

</ul>
</details>

**社区讨论**: 社区成员普遍欢迎这一举措，有些人称赞 Bunny 是 Cloudflare 的可行欧洲替代品。然而，也有人担心意外流量激增可能带来的隐性成本，以及考虑到 Bunny 融资轮次较小，其商业模式的可持续性。

**标签**: `#DNS`, `#hosting`, `#free-tier`, `#CDN`, `#Cloudflare-alternative`

---

<a id="item-3"></a>
## [GitHub 上的 PR 垃圾信息堪比 2000 年代初的邮件垃圾信息](https://www.greptile.com/blog/prs-on-openclaw) ⭐️ 8.0/10

Greptile 的一篇博文将当前 GitHub 上的拉取请求（PR）垃圾信息与 21 世纪初的电子邮件垃圾信息泛滥相提并论，引发了社区关于潜在缓解措施的讨论。 这种对比突显了开源维护者面临的一个日益严重的问题，即低质量或自动生成的 PR 数量不断增加，这可能会压垮项目并降低生产力。 博文指出，GitHub 最近为维护者引入了可配置的 PR 限制，但一些评论者认为，与电子邮件垃圾信息（发件人声誉与 IP 和域名挂钩）不同，PR 垃圾信息缺乏针对单个用户声誉的类似基础设施。

hackernews · dakshgupta · 6月24日 14:32 · [社区讨论](https://news.ycombinator.com/item?id=48660579)

**背景**: 拉取请求（PR）垃圾信息指未经请求或自动生成的 PR，通常包含琐碎的更改、广告链接或不相关的内容。Hacktoberfest 等活动加剧了这一问题，参与者为获取奖励而创建 PR，导致低质量贡献激增。与电子邮件垃圾信息的类比基于开放、去中心化平台中可扩展声誉和过滤机制的共同挑战。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/orgs/community/discussions/53233">What should I do about spam issues or pull requests ... - GitHub</a></li>
<li><a href="https://socket.dev/blog/express-js-spam-prs-commoditization-of-open-source">Express.js Spam PRs Incident Highlights the Commoditization ...</a></li>

</ul>
</details>

**社区讨论**: 评论者提出了多元化的观点：有人指出 GitHub 新的 PR 限制是一种部分解决方案；另一个人则强调了与电子邮件垃圾信息的结构性差异，即在电子邮件中由组织管理用户行为。一位维护者分享了要求首次贡献者进行非文字介绍的做法；还有人建议引入基于代币的捐赠系统，让维护者自行分配资源。

**标签**: `#open-source`, `#pull-request-spam`, `#community-management`, `#spam`, `#github`

---

<a id="item-4"></a>
## [卡马克反思早期错误，称雷神之锤值得](https://twitter.com/ID_AA_Carmack/status/2069799283369345247) ⭐️ 8.0/10

约翰·卡马克在推特上反思了他在 id Software 的早期错误，包括对员工施加过大压力，并得出结论：尽管《雷神之锤》的开发耗尽了公司，但绝对值得。 卡马克坦率的回顾为经典游戏开发的人力成本提供了罕见的洞察，他的结论——游戏比公司更重要——为行业提供了一个发人深省的视角。 卡马克特别提到，他没有意识到成熟公司需要更多宽松，而一直以初创公司的强度驱动员工会耗尽他们。他重申《雷神之锤》是游戏界的标志性巨作，因此付出的代价是值得的。

hackernews · shadowtree · 6月24日 15:56 · [社区讨论](https://news.ycombinator.com/item?id=48661825)

**背景**: 约翰·卡马克是传奇程序员，id Software 的联合创始人，以《毁灭战士》和《雷神之锤》等开创性游戏闻名。1996 年发布的《雷神之锤》是 3D 游戏的里程碑，但其开发据称给公司带来了压力，导致关键创意人员的离职。

**社区讨论**: 评论中提到了桑迪·彼得森对该代价的看法，并附有采访链接。一些人指出《雷神之锤 3：竞技场》仍充满活力，而另一些人同意卡马克的技术焦点有时掩盖了艺术成就，正如《毁灭战士 2》之后创意人员离开所体现的那样。

**标签**: `#game development`, `#leadership`, `#id Software`, `#John Carmack`, `#software engineering`

---

<a id="item-5"></a>
## [生成式 AI 可能降低中国学生考试成绩](https://cepr.org/publications/dp21577) ⭐️ 8.0/10

一项对 26,811 名中国 7-12 年级学生持续 30 个月的研究发现，生成式 AI 虽让作业成绩平均提高 18%、完成时间减少 30%，却导致闭卷月考成绩下降约 20%，中考、高考等高风险考试成绩降低 18%-24%。 这项大规模实证研究提供了有力证据，表明过度依赖生成式 AI 完成作业可能损害真正的学习，对全球教育政策和学校 AI 监管具有重要启示。 负面影响在社科科目中最大，其次是理工科和语言；低年级、高成就和男生受影响更明显。约 80%的 AI 用户表现出“作业外包”特征——作业时间极短但分数高，这类学生承担了主要损失。

telegram · zaihuapd · 6月24日 05:15

**背景**: 像 ChatGPT 这样的生成式 AI 工具能快速生成书面作业，导致部分学生将其用作捷径。这项研究跟踪学生 30 个月，以衡量对学习成果的长期影响。研究结果凸显了当 AI 被用作努力的替代品而非学习辅助工具时，可能削弱基础知识的风险。

**标签**: `#education`, `#generative AI`, `#academic performance`, `#China`, `#AI impact`

---

<a id="item-6"></a>
## [美光 26Q3 营收同比暴增 346%，净利润 282 亿美元](https://www.globenewswire.com/news-release/2026/06/24/3317151/14450/en/micron-technology-inc-reports-record-results-for-the-third-quarter-of-fiscal-2026.html) ⭐️ 8.0/10

美光科技发布 2026 财年第三季度财报，营收达 414.6 亿美元，同比增长 346%，净利润 282.4 亿美元，受 AI 基础设施对高带宽内存的需求驱动。 这一创纪录的业绩凸显了 AI 基础设施扩张对内存行业的巨大影响，美光的利润率和盈利能力达到前所未有的水平，标志着需求的结构性转变。 Non-GAAP 毛利率从去年同期的 39%飙升至 84.9%，公司预计下季度营收达 500 亿美元，毛利率升至 86%。美光已开始大规模量产 HBM4，并计划于 2027 年投产 HBM4E。

telegram · zaihuapd · 6月24日 22:22

**背景**: 高带宽内存（HBM）是一种 3D 堆叠 DRAM 技术，提供极宽的数据总线，对 AI 训练和推理工作负载至关重要。美光的 HBM4 及未来的 HBM4E 专为 NVIDIA Vera Rubin 平台等下一代 AI 加速器设计，旨在解决 AI 系统中的内存瓶颈问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/High_Bandwidth_Memory">High Bandwidth Memory - Wikipedia</a></li>
<li><a href="https://cloudnews.tech/micron-warns-ai-is-just-beginning-and-already-tightening-the-memory-market/">Micron Warns: AI Is Just Beginning and Already... | Cloud News</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#AI infrastructure`, `#memory`, `#earnings`, `#Micron`

---