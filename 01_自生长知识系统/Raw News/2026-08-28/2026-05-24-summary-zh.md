---
layout: default
title: "Horizon Summary: 2026-05-24 (ZH)"
date: 2026-05-24
lang: zh
---

> From 22 items, 6 important content pieces were selected

---

1. [苹果开源 corecrypto，附带量子安全算法形式化证明](#item-1) ⭐️ 9.0/10
2. [80386 微码逆向工程解析](#item-2) ⭐️ 8.0/10
3. [Anthropic 的 Project Glasswing 用 AI 发现逾万高危漏洞](#item-3) ⭐️ 8.0/10
4. [微软在核心团队推广 Claude Code](#item-4) ⭐️ 8.0/10
5. [微软财报披露 OpenAI 季度亏损 115 亿美元](#item-5) ⭐️ 8.0/10
6. [富途和老虎证券因跨境证券业务被罚](#item-6) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [苹果开源 corecrypto，附带量子安全算法形式化证明](https://security.apple.com/blog/formal-verification-corecrypto/) ⭐️ 9.0/10

苹果公司开源了其 corecrypto 密码库，包含经过形式化验证的量子安全算法 ML-KEM 和 ML-DSA 实现，并使用 Isabelle 定理证明器发布了端到端的数学证明，以确保与 NIST 标准的一致性。 此举结合了数十亿设备上的实际部署与严格的形式化验证，为密码学安全保障设立了新标杆，并鼓励行业更广泛地采用后量子密码学。 开源发布包括 corecrypto 的 C 代码和手工优化的 ARM64 汇编，以及供独立审查的定制验证工具和 Isabelle 理论库；已验证的算法已用于 iMessage 和 VPN 产品中。

telegram · zaihuapd · May 23, 04:49

**背景**: corecrypto 是苹果的低层密码学库，为超过 25 亿台活跃设备提供加密支持。形式化验证通过数学证明来确保代码与规范完全一致，从而消除整类错误。ML-KEM（原 Kyber）和 ML-DSA（原 Dilithium）是 NIST 标准化的后量子算法，能够抵御未来量子计算机的攻击。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ML-KEM">ML-KEM</a></li>
<li><a href="https://en.wikipedia.org/wiki/ML-DSA">ML-DSA</a></li>
<li><a href="https://en.wikipedia.org/wiki/Isabelle_theorem_prover">Isabelle theorem prover</a></li>

</ul>
</details>

**标签**: `#cryptography`, `#formal verification`, `#apple`, `#quantum-safe`, `#open source`

---

<a id="item-2"></a>
## [80386 微码逆向工程解析](https://www.reenigne.org/blog/80386-microcode-disassembled/) ⭐️ 8.0/10

一篇关于 Intel 80386 微码的详细反汇编报告已发布，揭示了这款经典 32 位处理器的内部控制逻辑。 这一逆向工程成果为基础 CPU 的设计提供了前所未有的洞察，惠及复古计算爱好者和计算机架构研究人员。 反汇编可能涉及分析高分辨率芯片显微照片并重建微码 ROM 内容；80386 使用微程序设计来实现其 x86 指令集。

hackernews · nand2mario · May 23, 12:11 · [社区讨论](https://news.ycombinator.com/item?id=48247004)

**背景**: 微码是一层低级指令，控制 CPU 的内部操作，充当机器码的解释器。Intel 80386 于 1985 年发布，是 x86 系列中首款 32 位处理器，也是现代计算的基石。反汇编其微码是一项高度复杂的逆向工程任务，需要对芯片布局和逻辑有深入了解。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Microcode">Microcode - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Intel_80386">Intel 80386</a></li>

</ul>
</details>

**社区讨论**: 评论者对逆向工程工作表示钦佩，有些人询问从芯片图像中提取微码的技术过程。还提到了相关项目如 z386，一个基于原始微码构建的开源 80386。

**标签**: `#reverse engineering`, `#CPU microcode`, `#80386`, `#computer architecture`, `#retrocomputing`

---

<a id="item-3"></a>
## [Anthropic 的 Project Glasswing 用 AI 发现逾万高危漏洞](https://www.anthropic.com/research/glasswing-initial-update) ⭐️ 8.0/10

Anthropic 的 Project Glasswing 项目利用 Claude Mythos Preview 模型，在一个月内从关键软件和开源项目中发现了超过一万个高危漏洞，经审查的漏洞中真阳性率达到 90.6%。 这一突破表明 AI 可以大幅加速漏洞发现，但也暴露了关键的补丁修复瓶颈，软件行业必须解决这一问题以跟上步伐。 包括 Cloudflare 在内的合作伙伴报告漏洞发现速度提高了十倍以上。在 1,752 个经审查的漏洞中，90.6% 为真阳性，Anthropic 已开源 Claude Security 工具以帮助企业修复漏洞。

telegram · zaihuapd · May 23, 03:16

**背景**: Project Glasswing 是 Anthropic 的一项网络安全计划，联合了包括苹果和谷歌在内的超过 45 个组织，使用未发布的 Claude Mythos Preview 模型进行漏洞发现。该模型被描述为超越 Opus 的新一代前沿模型。该项目强调，虽然 AI 可以比人类更快地发现漏洞，但验证、披露和打补丁的人工过程仍然是瓶颈。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/research/glasswing-initial-update">Project Glasswing: An initial update \ Anthropic</a></li>
<li><a href="https://www.wired.com/story/anthropic-mythos-preview-project-glasswing/">Anthropic Teams Up With Its Rivals to Keep AI From Hacking ...</a></li>
<li><a href="https://www.forbes.com/sites/paulocarvao/2026/04/08/five-reasons-anthropic-kept-its-cybersecurity-breakthrough-invite-only/">Five Reasons Anthropic Kept Its Cybersecurity Breakthrough ...</a></li>

</ul>
</details>

**标签**: `#AI`, `#cybersecurity`, `#vulnerability discovery`, `#Anthropic`, `#software security`

---

<a id="item-4"></a>
## [微软在核心团队推广 Claude Code](https://t.me/zaihuapd/41535) ⭐️ 8.0/10

微软正在其重要工程团队中内部推广 Anthropic 的 Claude Code，甚至鼓励没有编程经验的员工使用，并要求开发者同时使用 Claude Code 和 GitHub Copilot 并反馈对比。 此举表明微软务实采纳竞争对手的 AI 编程工具，可能重塑企业 AI 工作流程，并加剧 Claude Code 与 GitHub Copilot 之间的竞争。 受影响的团队包括 CoreAI、Windows、Microsoft 365 和 Outlook 团队；非技术人员被鼓励使用 Claude Code 进行原型设计。

telegram · zaihuapd · May 23, 06:05

**背景**: Claude Code 是 Anthropic 开发的 AI 编程代理，可与 GitHub、GitLab 和命令行工具集成，采用宪法 AI 技术确保安全。微软同时开发了 GitHub Copilot 作为竞争性 AI 结对编程工具。内部对比表明微软正在评估哪种工具更符合其工程需求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>
<li><a href="https://claude.com/product/claude-code">Claude Code by Anthropic | AI Coding Agent, Terminal, IDE</a></li>

</ul>
</details>

**标签**: `#AI coding`, `#Claude Code`, `#Microsoft`, `#GitHub Copilot`, `#enterprise AI`

---

<a id="item-5"></a>
## [微软财报披露 OpenAI 季度亏损 115 亿美元](https://t.me/zaihuapd/41537) ⭐️ 8.0/10

微软最新财报显示，其对 OpenAI 的权益法投资导致单季度净利润减少 31 亿美元，基于微软持有约 27%股权计算，OpenAI 该季度净亏损约 115 亿美元。 这一披露凸显了人工智能开发中巨大的资金消耗速度，OpenAI 单季度亏损几乎是其今年上半年 43 亿美元营收的近三倍，强调了领先 AI 研究的财务风险和高成本。 微软已向 OpenAI 投入 116 亿美元，占其 130 亿美元承诺投资的绝大部分；若按税前损失和实际持股比例 32.5%计算，亏损可能超 120 亿美元。

telegram · zaihuapd · May 23, 07:40

**背景**: 权益法核算用于投资者对被投资单位具有重大影响（通常持股 20%-50%）的情况，投资者按其持股比例分享被投资单位的净利润或净亏损，计入投资收益。OpenAI 是一家开发 GPT 等先进 AI 模型的私人公司，需要大量计算资源和人才，导致运营成本高昂。这种会计处理方法使微软的收益反映了 OpenAI 的财务表现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.dongao.com/zjzcgl/zjkjsw/201905131026788.shtml">权 益 法 下可辨认净 资 产公允价值与账面价值怎么调整_东奥会计在线</a></li>
<li><a href="http://www.canet.com.cn/acc/zzjq/200807/19-36934.html">canet.com.cn/acc/zzjq/200807/19-36934.html</a></li>

</ul>
</details>

**标签**: `#OpenAI`, `#Microsoft`, `#AI industry`, `#financial losses`, `#equity method accounting`

---

<a id="item-6"></a>
## [富途和老虎证券因跨境证券业务被罚](https://t.me/zaihuapd/41539) ⭐️ 8.0/10

中国监管机构拟对富途控股罚款 185 亿元，对老虎证券子公司罚没约 41.1 亿元，原因是它们未经授权在中国内地开展跨境证券、公募基金销售和期货业务。 这标志着对跨境经营的金融科技券商的一次重大监管打击，表明中国将更严格地执行证券法，并可能重塑跨境投资平台的格局。 富途控股还被责令整改，其创始人兼首席执行官李华面临个人罚款 125 万元。这些处罚尚需经过后续程序并等待最终决定。

telegram · zaihuapd · May 23, 10:58

**背景**: 富途控股和老虎证券是总部位于香港的主要在线券商，向中国大陆投资者提供证券交易服务。中国法律要求在中国境内提供证券服务的公司持有相应的许可证。这些罚款针对的是它们涉嫌无牌跨境业务，在控制资本外流和维护市场秩序的努力中，这一直是监管关注的焦点。

**标签**: `#regulation`, `#fintech`, `#China`, `#securities`, `#enforcement`

---