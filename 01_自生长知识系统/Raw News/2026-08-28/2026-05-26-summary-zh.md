---
layout: default
title: "Horizon Summary: 2026-05-26 (ZH)"
date: 2026-05-26
lang: zh
---

> 从 28 条内容中筛选出 9 条重要资讯。

---

1. [教宗良十四世发布人工智能伦理通谕](#item-1) ⭐️ 9.0/10
2. [用人工智能更慢地写出更好的代码](#item-2) ⭐️ 8.0/10
3. [Mullvad 推出针对 VPN 出口 IP 指纹识别的缓解措施](#item-3) ⭐️ 8.0/10
4. [加州提议豁免 Linux 于年龄验证法](#item-4) ⭐️ 8.0/10
5. [LSFMM+BPF 峰会讨论基于 LLM 的内核补丁审查](#item-5) ⭐️ 8.0/10
6. [SFC 回应 Bambu 违反 AGPLv3 协议](#item-6) ⭐️ 8.0/10
7. [半存活人脑用于药物测试](#item-7) ⭐️ 8.0/10
8. [欧盟初步调查：谷歌违反《数字市场法》](#item-8) ⭐️ 8.0/10
9. [马斯克：xAI 将于 2026 年底开源 0.5T 参数模型](#item-9) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [教宗良十四世发布人工智能伦理通谕](https://simonwillison.net/2026/May/25/encyclical-on-ai/#atom-everything) ⭐️ 9.0/10

梵蒂冈发布了教宗良十四世题为《崇高人性》的通谕，专门针对人工智能时代保护人类的伦理问题。该文件因其异常的清晰和深度而受到赞扬。 这是首个专门论述人工智能的教宗通谕，标志着天主教会介入现代科技伦理。它提供了易于理解的伦理指引，可能影响全球关于人工智能监管和人类尊严的讨论。 该通谕强调了大语言模型的可解释性问题，将人工智能系统描述为更多是“培育”而非“建造”。它还强调真正的发展必须以人为中心，而不是财富积累。

rss · Simon Willison · 5月25日 23:58

**背景**: 教宗通谕是教宗就重要问题发表的正式信函。教宗良十四世选择此名以纪念良十三世，后者在《新事》通谕中论述了工业革命的劳工问题。本通谕将这一社会训导更新到人工智能时代。

**标签**: `#AI ethics`, `#Vatican`, `#papal encyclical`, `#technology ethics`, `#society`

---

<a id="item-2"></a>
## [用人工智能更慢地写出更好的代码](https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/) ⭐️ 8.0/10

Nolan Lawson 的博客文章主张，对 AI 辅助编码采用深思熟虑、迭代的方法，可以产生比通常注重速度的做法更高质量的代码，这挑战了 AI 编码工具的主流叙事。 这一观点意义重大，因为它鼓励开发者重新思考他们在工作流程中使用 AI 的方式，可能会带来更好的代码质量和更可持续的软件工程实践。 作者描述了一个涉及多个 AI 模型的工作流程，用于设计、实现和审查，强调迭代和彻底性而非原始速度，并指出像 Claude 和 Codex 这样的工具可以串联使用以捕获边界情况。

hackernews · signa11 · 5月25日 23:16 · [社区讨论](https://news.ycombinator.com/item?id=48272984)

**背景**: AI 编码助手（如 ChatGPT、Claude 和 GitHub Copilot）因能快速生成代码而变得流行，但输出质量可能差异很大。本文提出了一种更慢、更审慎的过程，利用 AI 进行设计和审查，同时辅以人工监督。

**社区讨论**: 评论揭示了不同的体验：一些人发现 AI 辅助的工作流程会变成漫长的反复过程，甚至可能超过手动编码的时间；而另一些人则看重针对不同阶段（设计、实现、审查）使用多个 LLM 的价值，并认为在审慎使用的情况下 AI 可以生成高质量代码。少数评论者出于伦理原因对 AI 持怀疑态度，但发现代码审查用例问题较少。

**标签**: `#AI`, `#coding`, `#software engineering`, `#productivity`, `#code quality`

---

<a id="item-3"></a>
## [Mullvad 推出针对 VPN 出口 IP 指纹识别的缓解措施](https://mullvad.net/en/help/exit-ip-vpn-servers-mitigation-rollout) ⭐️ 8.0/10

Mullvad VPN 宣布推出缓解措施，防止出口 IP 指纹识别，该技术可通过 VPN 服务器的唯一 IP 地址识别用户。 这很重要，因为出口 IP 指纹识别允许网站跨会话关联用户，从而破坏 VPN 隐私。Mullvad 的积极响应为 VPN 行业树立了良好榜样。 缓解措施包括更改出口服务器配置以减少唯一性。用户可能会感受到轻微的性能变化，但无需任何操作。

hackernews · Cider9986 · 5月25日 17:45 · [社区讨论](https://news.ycombinator.com/item?id=48269580)

**背景**: VPN 出口 IP 指纹识别是一种隐私攻击，网站通过出口 IP 地址识别用户的 VPN 提供商和特定服务器，可用于跨网站或会话追踪用户。Mullvad 此前曾发布关于该漏洞的研究。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://discuss.privacyguides.net/t/mullvad-exit-ips-as-a-fingerprinting-vector/37910">Mullvad exit IPs as a fingerprinting vector - General - Privacy</a></li>
<li><a href="https://tmctmt.com/posts/mullvad-exit-ips-as-a-fingerprinting-vector/">Mullvad exit IPs as a fingerprinting vector | tmctmt</a></li>
<li><a href="https://cacm.acm.org/research/openvpn-is-open-to-vpn-fingerprinting/">OpenVPN Is Open to VPN Fingerprinting – Communications of the ACM</a></li>

</ul>
</details>

**社区讨论**: 用户对快速响应表示惊讶和赞赏，一些人建议进一步改进，如集成浏览器反指纹识别功能。有评论者指出，Mullvad 浏览器已通过使用代理而非 WireGuard 避免了此问题。

**标签**: `#privacy`, `#VPN`, `#fingerprinting`, `#security`, `#Mullvad`

---

<a id="item-4"></a>
## [加州提议豁免 Linux 于年龄验证法](https://www.tomshardware.com/software/linux/california-moves-to-exempt-linux-from-its-upcoming-age-verification-law-after-backlash-over-forcing-operating-systems-to-collect-users-ages-amendment-proposed-by-the-same-lawmaker-who-wrote-the-original-law) ⭐️ 8.0/10

加州提出对其年龄验证法进行修订，明确豁免 Linux 操作系统，此前该法要求操作系统收集用户年龄引发了强烈反对。 此举避免了 Linux 采用和开源软件可能面临的灾难，因为原法律将对缺乏集中用户账户的操作系统施加不可能的负担。 该修正案由原法律的同一立法者提出，表明认识到意外后果。豁免明确涵盖非主要用于访问商业内容的操作系统。

hackernews · rbanffy · 5月25日 18:19 · [社区讨论](https://news.ycombinator.com/item?id=48269961)

**背景**: 加州旨在保护未成年人在线安全的年龄验证法原本要求所有操作系统验证用户年龄。这引发了 Linux 和开源社区的强烈反对，因为 Linux 发行版通常没有集中式用户账户或轻松验证年龄的能力。拟议修正案豁免了非主要用于访问商业内容的操作系统。

**社区讨论**: 社区评论对该法律的必要性表示怀疑，并强调对开源系统应用年龄验证的不切实际。一些评论者批评立法过程未咨询相关专家，而另一些则指出该法律会加重消费者负担，而非有效监管企业。

**标签**: `#Linux`, `#California`, `#age-verification`, `#internet regulation`, `#open source`

---

<a id="item-5"></a>
## [LSFMM+BPF 峰会讨论基于 LLM 的内核补丁审查](https://lwn.net/Articles/1073583/) ⭐️ 8.0/10

在 2026 年 Linux 存储、文件系统、内存管理和 BPF 峰会上，由 Roman Gushchin 等人主持的全体会议讨论了使用大型语言模型（LLM）进行 Linux 内核补丁审查，重点关注 Sashiko 工具。 此次讨论表明 AI 辅助代码审查在 Linux 内核中日益受到关注，有望减轻人类维护者的工作负担并提高补丁质量，尤其对于首次贡献者。 Sashiko 在分析的 1500 个邮件线程中达到 10% 的误报率和 85% 的真阳性率，关键和高严重性问题的准确率接近 97%。自 3 月中旬推出以来，该工具已被提及在 140 条内核提交信息中。

rss · LWN.net · 5月25日 21:27

**背景**: Linux 内核开发过程严重依赖人工审查者来评估补丁。大型语言模型是一种概率性 AI 系统，可以分析代码并提供审查意见。Sashiko 是一个自动审查内核补丁的工具，介于静态分析和人工审查之间。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://events.linuxfoundation.org/lsfmmbpf/">Linux Storage, Filesystem, MM & BPF Summit | LF Events</a></li>
<li><a href="https://ebpf.foundation/event/linux-storage-filesystem-memory-management-bpf-summit/">Linux Storage, Filesystem, Memory Management & BPF Summit</a></li>

</ul>
</details>

**标签**: `#LLM`, `#Linux kernel`, `#patch review`, `#AI-assisted development`

---

<a id="item-6"></a>
## [SFC 回应 Bambu 违反 AGPLv3 协议](https://lwn.net/Articles/1074286/) ⭐️ 8.0/10

软件自由保护协会（SFC）于 5 月 18 日发布回应，详细说明了 Bambu Lab 违反 AGPLv3 许可的行为，包括未能提供对 GPL 许可切片机修改的源代码，并威胁一位分支创建者。SFC 启动了 baltobu 逆向工程项目，并托管一个合规的 Orca Slicer 分支。 此举突显了开源许可在 3D 打印行业的执行，保护了开发者的权利和用户的自由。它为追究商业实体在 AGPLv3 合规方面的责任树立了先例，尤其是在维修权方面。 Bambu Lab 就 AGPLv3 要求发表了虚假公开声明，并威胁了 Paweł Jarczak，后者创建了 Orca Slicer 的分支以实现与其 Bambu 打印机的互操作。SFC 的 baltobu 项目旨在逆向工程 Bambu 的专有代码，以确保合规并支持消费者。

rss · LWN.net · 5月25日 16:48

**背景**: AGPLv3 是一种强 copyleft 许可证，要求在网络上使用修改版软件时，必须向用户提供其源代码。3D 打印机切片机将 3D 模型转换为打印机指令（G-code）。Orca Slicer 是一个开源切片机，源自 Bambu Studio，而 Bambu Studio 本身基于 AGPLv3 许可的代码。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GNU_Affero_General_Public_License">GNU Affero General Public License - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Slicer_(3D_printing)">Slicer (3D printing) - Wikipedia</a></li>

</ul>
</details>

**标签**: `#open source`, `#AGPLv3`, `#license enforcement`, `#3D printing`, `#software freedom`

---

<a id="item-7"></a>
## [半存活人脑用于药物测试](https://www.science.org/content/article/not-alive-not-dead-disembodied-human-brains-used-drug-testing) ⭐️ 8.0/10

一项研究利用 BrainEx 灌流系统，在死亡数小时后恢复了人类大脑的部分代谢和细胞活动，从而能够测试阿尔茨海默病和帕金森病等神经疾病的药物。 这一突破挑战了传统的死亡定义，引发了关于意识和人类尊严的深刻伦理问题，同时可能通过提供比动物试验更准确的人脑模型，彻底改变神经药物开发。 这些来自捐赠者的大脑并未恢复意识或完整的神经活动；该技术由美国生物科技公司 Bexorg 开发。该研究引发了关于器官捐赠知情同意和维持生命技术边界的争论。

telegram · zaihuapd · 5月25日 14:57

**背景**: BrainEx 系统是一种灌流技术，在死后向脑组织输送氧气和营养物质，维持细胞完整性。传统上，脑死亡被视为不可逆，但该系统可以在无意识状态下部分恢复细胞功能。这项工作建立在早期动物研究基础上，但首次报道用于人类大脑的药物测试。

**标签**: `#neuroscience`, `#bioethics`, `#drug testing`, `#brain research`, `#ethics`

---

<a id="item-8"></a>
## [欧盟初步调查：谷歌违反《数字市场法》](https://t.me/zaihuapd/41566) ⭐️ 8.0/10

欧盟委员会初步认定 Alphabet（谷歌）违反《数字市场法》，通过在搜索结果中自我偏好以及在 Play 商店限制应用开发者。 这是《数字市场法》下的重大执法行动，表明欧盟认真遏制大型科技公司反竞争行为，可能导致重大罚款或强制改变谷歌在欧洲的商业模式。 具体而言，谷歌搜索结果被指控优先展示其购物、航班和酒店等服务，而 Play 商店限制开发者引导用户使用替代支付或分发渠道。欧盟委员会认为谷歌的合规措施不足。

telegram · zaihuapd · 5月26日 00:27

**背景**: 《数字市场法》（DMA）是欧盟法规，指定大型在线平台为“守门人”并施加义务以确保公平竞争。自我偏好（平台偏袒自身服务而非竞争者）是 DMA 禁止的关键行为。谷歌的搜索服务和 Play 商店已被指定为受这些规则约束的核心平台服务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://element.io/blog/the-digital-markets-act-explained-in-15-questions/">The Digital Markets Act explained in 15 questions</a></li>
<li><a href="https://laweconcenter.org/resources/antitrust-unchained-the-eus-case-against-self-preferencing/">Antitrust Unchained: The EU’s Case Against Self-Preferencing</a></li>
<li><a href="https://digital-markets-act.ec.europa.eu/developer-portal/app-distribution_en">App distribution - Digital Markets Act (DMA) - European ...</a></li>

</ul>
</details>

**标签**: `#antitrust`, `#DMA`, `#Google`, `#EU`, `#regulation`

---

<a id="item-9"></a>
## [马斯克：xAI 将于 2026 年底开源 0.5T 参数模型](https://x.com/i/status/2058796067592736866) ⭐️ 8.0/10

埃隆·马斯克宣布，xAI 将在 2026 年底前开源一个 0.5 万亿参数模型，外界广泛推测该模型为 Grok 4.2 基座模型。 开源如此大规模的模型将延续 xAI 对透明度的承诺，并为 AI 社区提供一个强大的免费语言模型，可能加速研究和应用。 该模型拥有 0.5 万亿参数，xAI 此前已以 Apache 2.0 许可证开源了 Grok-1（3140 亿参数）。新模型预计是当前的基座模型 Grok 4.2。

telegram · zaihuapd · 5月26日 02:46

**背景**: 像 Grok 这样的大型语言模型采用混合专家（MoE）架构，将模型分为多个子网络以提高效率。xAI 有开源模型的历史，始于 2024 年开源 Grok-1。开源使社区能够无限制地研究、微调和部署模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nextbigfuture.com/2026/04/anthropic-and-xai-model-parameter-counts.html">Anthropic and xAI Model Parameter Counts | NextBigFuture.com</a></li>
<li><a href="https://en.wikipedia.org/wiki/Grok_(chatbot)">Grok (chatbot) - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区情绪似乎褒贬不一，有用户不屑地质疑是否真的会有人使用该模型，并将其贬低为‘豆包’，暗示其没有用处。

**标签**: `#AI`, `#open-source`, `#xAI`, `#Grok`, `#large language models`

---