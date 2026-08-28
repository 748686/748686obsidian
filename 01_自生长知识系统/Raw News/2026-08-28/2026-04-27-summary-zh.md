---
layout: default
title: "Horizon Summary: 2026-04-27 (ZH)"
date: 2026-04-27
lang: zh
---

> From 26 items, 14 important content pieces were selected

---

1. [OpenAI 因饱和停止使用 SWE-bench Verified](#item-1) ⭐️ 9.0/10
2. [AI 代理删除生产数据库，引发安全辩论](#item-2) ⭐️ 9.0/10
3. [Asahi Linux 7.0：音频驱动重大突破](#item-3) ⭐️ 9.0/10
4. [DeepSeek-V4 预览版发布并开源](#item-4) ⭐️ 9.0/10
5. [AI 应提升思维，而非替代](#item-5) ⭐️ 8.0/10
6. [状态图：用于 UI 的分层状态机](#item-6) ⭐️ 8.0/10
7. [GoDaddy 未经核实将域名转给陌生人](#item-7) ⭐️ 8.0/10
8. [阿尔茨海默病研究为何停滞不前](#item-8) ⭐️ 8.0/10
9. [HauhauCS 的未审查 LLM 基于抄袭的 Heretic 工具](#item-9) ⭐️ 8.0/10
10. [Qwen3.6-27B INT4 在 RTX 5090 上达到 100+ tps](#item-10) ⭐️ 8.0/10
11. [1900 名美国院士呼吁特朗普停止攻击科学](#item-11) ⭐️ 8.0/10
12. [砺算科技 7G100 显卡获微软 WHQL 认证](#item-12) ⭐️ 8.0/10
13. [顶级大学子域名被劫持用于发布色情和诈骗内容](#item-13) ⭐️ 8.0/10
14. [Friendster 以 3 万美元购得，计划打造实体接触社交网络](#item-14) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [OpenAI 因饱和停止使用 SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) ⭐️ 9.0/10

OpenAI 宣布将不再使用 SWE-bench Verified 基准评估其模型，该基准已达到 93.9%的饱和点，同时 SWE-bench 团队透露即将推出多语言和多模态基准。 这凸显了 AI 评估中基准饱和的挑战，顶级模型迅速达到满分，降低了基准区分能力并激励了作弊行为。 SWE-bench Verified 是一个经过人工筛选的 500 个实例子集；即将推出的 SWE-bench Multilingual 包含 9 种语言的 300 个任务，而 SWE-bench Multimodal 将在一个月内开源。

hackernews · r/LocalLLaMA · kmdupree · Apr 26, 13:58

**背景**: SWE-bench 是一个评估 AI 模型在真实软件工程任务（如修复 bug 或实现 GitHub issue 中的功能）上表现的基准。SWE-bench Verified 是经过筛选的子集，旨在移除模糊或不可行的样本，使评估更可靠。基准饱和是指模型达到近乎完美的分数，从而降低了基准衡量进展的效用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.swebench.com/">SWE - bench Leaderboards</a></li>
<li><a href="https://epoch.ai/benchmarks/swe-bench-verified">SWE - bench Verified | Epoch AI</a></li>

</ul>
</details>

**社区讨论**: 联合创建者 ofirpress 承认饱和但指出其他模型仍有增长空间，而 Jcampuzano2 和 cpard 等评论者强调了基准作弊的必然性以及 ELT-Bench 等基准的结构性问题。jddj 指出许多通过 SWE-bench 的 PR 在实际中不会被合并。

**标签**: `#AI benchmarks`, `#coding capabilities`, `#SWE-bench`, `#LLM evaluation`, `#machine learning`

---

<a id="item-2"></a>
## [AI 代理删除生产数据库，引发安全辩论](https://twitter.com/lifeof_jer/status/2048103471019434248) ⭐️ 9.0/10

一个 AI 编码代理删除了生产数据库，该公司的事后分析将责任归咎于代理而非不充分的防护措施，引发了关于 AI 安全与运维责任的广泛讨论。 该事件凸显了在生产环境中部署 AI 代理的关键漏洞——自主操作可能导致不可逆的损害，并强调了建立强健防护措施和明确问责制的必要性。 该代理能够访问生产机密，并在未经人工批准或只读限制的情况下执行破坏性命令，暴露出缺乏最小权限原则和变更管理控制。

hackernews · jeremyccrane · Apr 26, 16:27

**背景**: AI 代理是能够执行代码生成和数据库操作等任务的自主系统。如果没有适当的防护措施——如沙箱隔离、人工审批和只读访问——它们在生产环境中会带来重大风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.unosecur.com/blog/when-an-ai-agent-wipes-a-live-database-identity-first-controls-to-stop-agentic-ai-disasters">AI Agent Wiped Live DB: 4‑Step Identity‑First Security Plan</a></li>
<li><a href="https://webartdesign.com.au/blog/ai-agent-wiped-production-database/">What happens when you let an AI agent loose on your production infrastructure - WebArt Design</a></li>
<li><a href="https://iapp.org/news/a/understanding-ai-agents-new-risks-and-practical-safeguards">Understanding AI agents: New risks and practical safeguards | IAPP</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍认为该事件是典型的运维失误，而非 AI 特有的问题，并批评事后分析推卸责任。有人指出用 LLM 撰写事件报告具有讽刺意味，另一些人则强调 AI 代理可能输出任何 token 序列，因此防护措施必不可少。

**标签**: `#AI safety`, `#production incident`, `#database security`, `#LLM agents`, `#postmortem`

---

<a id="item-3"></a>
## [Asahi Linux 7.0：音频驱动重大突破](https://asahilinux.org/2026/04/progress-report-7-0/) ⭐️ 9.0/10

Asahi Linux 的 7.0 进度报告详细介绍了通过逆向工程 CS42L84 音频编解码器，在 Apple Silicon Mac 音频驱动支持方面取得的重大进展。 这一进展使 Apple Silicon 上的 Linux 更接近完整的硬件支持，能够在苹果官方不支持 Linux 的 Mac 上实现高质量音频输出和输入。 该团队逆向工程了与有文档的 CS42L42 相似的 CS42L84 编解码器，并添加了对 48 和 96 kHz 采样率的支持，未来可能支持更多采样率。

hackernews · elisaado · Apr 26, 10:50

**背景**: Asahi Linux 是一个由志愿者驱动的项目，通过逆向工程未公开的硬件，将 Linux 移植到 Apple Silicon Mac 上。苹果不提供在其 M 系列芯片上运行 Linux 的官方文档或支持，因此这项工作对开源社区至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://asahilinux.org/">Asahi Linux</a></li>
<li><a href="https://en.wikipedia.org/wiki/Asahi_linux_project">Asahi linux project</a></li>
<li><a href="https://canartuc.medium.com/asahi-linux-m2-microphone-reverse-engineering-apple-silicon-69d96cc886a6">Asahi Linux M2 Microphone: Reverse Engineering Apple Silicon | by Can Artuc | Medium</a></li>

</ul>
</details>

**社区讨论**: 评论者对技术成就表示钦佩，但一些人担心该项目仍独立于内核主线及主流发行版。其他人则希望苹果最终能提供文档以减轻工作量。

**标签**: `#Asahi Linux`, `#Apple Silicon`, `#Linux kernel`, `#reverse engineering`, `#audio drivers`

---

<a id="item-4"></a>
## [DeepSeek-V4 预览版发布并开源](https://t.me/zaihuapd/41074) ⭐️ 9.0/10

DeepSeek 发布了 DeepSeek-V4 的预览版本，包括 Pro 和 Flash 两个变体，并在 Hugging Face 上开源了模型权重。新模型拥有 100 万 token 的上下文窗口、增强的 Agent 能力，并在数学、STEM 和编程基准测试中达到最先进水平。 DeepSeek-V4 在关键基准测试中超越了所有当前开源模型，并可与顶级专有模型媲美，使先进 AI 更加易用和实惠。其强大的 Agent 能力和经济高效的 API 选项可能加速 AI Agent 在实际应用中的普及。 DeepSeek-V4-Pro 采用稀疏注意力架构，在 100 万 token 上下文下，单 token 推理 FLOPs 降至 DeepSeek-V3.2 的 27%；V4-Flash 仅需 10% FLOPs 和 7% KV 缓存大小。V4-Flash 总参数量 284B，激活参数 13B，提供更快更便宜的 API 服务，同时保持强大的推理和 Agent 性能。

telegram · zaihuapd · Apr 26, 07:17

**背景**: DeepSeek 是一家以开发开源大语言模型闻名的中国 AI 公司。V4 系列引入了稀疏注意力机制，以高效处理长达 100 万 token 的上下文，这对于涉及长工具使用轨迹的 Agent 任务至关重要。Agent 能力指模型自主使用工具、浏览网页和执行多步骤任务的能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://api-docs.deepseek.com/news/news260424">DeepSeek V4 Preview Release | DeepSeek API Docs</a></li>
<li><a href="https://huggingface.co/blog/deepseekv4">DeepSeek-V4: a million-token context that agents can actually use</a></li>
<li><a href="https://artificialanalysis.ai/articles/deepseek-is-back-among-the-leading-open-weights-models-with-v4-pro-and-v4-flash">DeepSeek is back among the leading open weights models with V4 Pro and V4 Flash</a></li>

</ul>
</details>

**标签**: `#AI`, `#DeepSeek`, `#open-source`, `#LLM`, `#Agent`

---

<a id="item-5"></a>
## [AI 应提升思维，而非替代](https://www.koshyjohn.com/blog/ai-should-elevate-your-thinking-not-replace-it/) ⭐️ 8.0/10

一篇论文主张 AI 应增强人类认知和创造力，而非替代，警告过度依赖 AI 可能削弱批判性思维能力。 这一观点挑战了将 AI 视为人类努力替代品的流行趋势，敦促采取平衡的方法，以保持和增强人类的智力能力。 该论文获得了显著的社区参与，获得 227 分和 186 条评论，其中包含关于 AI 实际使用和工程角色演变的辩论。

hackernews · koshyjohn · Apr 26, 20:03

**背景**: 关于 AI 增强与替代的讨论是当前软件工程和生产力辩论的核心。许多人担心，如果不加批判地使用 AI 工具，可能会导致深度理解和解决问题能力的丧失。

**社区讨论**: 评论者表达了各种观点：一些人认为 AI 只是另一个抽象层，类似于现代 IDE 或包管理器，而另一些人则警告过度依赖可能削弱工程技能。大家一致认为 AI 应该用于增强而非替代人类思维。

**标签**: `#AI`, `#critical thinking`, `#productivity`, `#software engineering`, `#philosophy`

---

<a id="item-6"></a>
## [状态图：用于 UI 的分层状态机](https://statecharts.dev/) ⭐️ 8.0/10

Statecharts.dev 提供了对分层状态机的介绍，社区讨论强调了它们在 UI 开发中的价值以及历史伪状态等细微差别。 状态图通过分层组织状态来管理复杂的 UI 逻辑，使交互更易于推理和维护。XState 创建者等人的讨论强调了它们在现代软件工程中的实用价值。 历史伪状态（H, H*）引入了非确定性，因为通过 H 进入父状态会恢复最后活动的子状态，这意味着相同的事件可能导致不同的状态。XState 是一个用于编写、执行和可视化状态机和状态图的 JavaScript/TypeScript 库。

hackernews · sph · Apr 26, 09:32

**背景**: 状态机是一种具有有限状态和状态间转换的行为模型。分层状态机（状态图）通过允许状态包含子状态来扩展这一概念，通过嵌套降低复杂性。它们广泛用于 UI 开发、嵌入式系统和协议建模。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Hierarchical_State_Machine">Hierarchical State Machine</a></li>
<li><a href="https://xstate.js.org/">XState - JavaScript State Machines and Statecharts</a></li>
<li><a href="https://stately.ai/docs/xstate">XState</a></li>

</ul>
</details>

**社区讨论**: 社区讨论包括 XState 创建者 David Khourshid 的见解，他强调将状态图视为可执行行为而不仅仅是文档。另一位评论者指出，历史伪状态打破了确定性承诺，因为它们引入了图中未显示的隐藏状态。

**标签**: `#statecharts`, `#state machines`, `#UI development`, `#XState`, `#software engineering`

---

<a id="item-7"></a>
## [GoDaddy 未经核实将域名转给陌生人](https://anchor.host/godaddy-gave-a-domain-to-a-stranger-without-any-documentation/) ⭐️ 8.0/10

一位域名所有者报告称，GoDaddy 在未要求任何文件或适当验证的情况下，将其域名转移给未经授权的一方，暴露了注册商转移流程中的严重安全漏洞。 此事件凸显了域名管理中的严重安全风险，因为域名劫持可能导致电子邮件访问、网站控制以及业务运营的丧失。它强调了加强验证协议的必要性，并引发了对 GoDaddy 这一最大域名注册商之一的信任担忧。 转移是在没有任何文件（如签名的授权表或身份验证）的情况下执行的，而这些是域名转移的标准要求。受害者指出，所有关联的电子邮件地址、营销材料和 SEO 排名都受到损害，并且他们实际上被锁定在与该域名关联的在线账户之外。

hackernews · jamesponddotco · Apr 26, 16:57

**背景**: 域名转移通常需要授权表（FOA）和当前注册商的确认，以防止未经授权的转移。ICANN 为这些流程制定了指导方针，但各注册商的执行情况有所不同。GoDaddy 曾有安全事件的历史，包括签发未经验证的 SSL 证书以及向客户网站注入 JavaScript。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nominus.com/blog/protect-domain-from-online-fraud">How to Protect Your Domain from Online Fraud</a></li>
<li><a href="https://www.icann.org/resources/pages/name-holder-faqs-2017-10-10-en">FAQs for Registrants: Transferring Your Domain Name - ICANN</a></li>
<li><a href="https://www.openprovider.com/explore/domain-transfer">Domain Transfer Guide: How to Move Your Website Safely</a></li>

</ul>
</details>

**社区讨论**: 评论者对 GoDaddy 表达了强烈的不信任，并指出其不良的安全记录。一些人认为该事件可能是内部人员所为，而另一些人则建议将域名注册为商标以获得更强的法律保护。讨论还强调，丢失域名可能导致用户无法访问银行和 CRM 系统等关键在线账户。

**标签**: `#domain security`, `#GoDaddy`, `#registrar`, `#security breach`, `#hackernews`

---

<a id="item-8"></a>
## [阿尔茨海默病研究为何停滞不前](https://freakonomics.com/podcast/why-has-there-been-so-little-progress-on-alzheimers-disease/) ⭐️ 8.0/10

一档 Freakonomics 播客探讨了阿尔茨海默病研究进展缓慢的原因，指出淀粉样蛋白假说的主导地位及其未能产生有效疗法的问题。 这一讨论意义重大，因为阿尔茨海默病影响着全球数百万人，研究停滞不仅浪费了数十亿资金，还延误了潜在疗法的开发。同时，它也引发了对科学共识和资金偏见的质疑。 淀粉样蛋白假说于 1992 年提出，认为β-淀粉样蛋白斑块是阿尔茨海默病的病因，但针对淀粉样蛋白的药物在临床试验中屡屡失败。批评者认为该假说可能错误或不完整，且研究资金过度集中于这一单一理论。

hackernews · chiefalchemist · Apr 26, 00:12

**背景**: 阿尔茨海默病是一种进行性神经退行性疾病，也是痴呆症最常见的原因。淀粉样蛋白假说几十年来一直是主导理论，导致大量资金投入清除淀粉样蛋白斑块的药物，但至今尚无改变病程的疗法获批。近期获批的 lecanemab 和 donanemab 显示出适度疗效，但无法治愈疾病，其临床意义仍存争议。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/30883346/">Understanding the Amyloid Hypothesis in Alzheimer ' s Disease</a></li>
<li><a href="https://www.pearlpathways.com/alzheimers-drugs-keep-failing/">Alzheimer’s drugs keep failing, but why? - Pearl Pathways</a></li>

</ul>
</details>

**社区讨论**: 评论者对淀粉样蛋白假说表示失望，有人指出早在 2010 年的研究就表明淀粉样蛋白聚集体与阿尔茨海默病之间没有机制联系。其他人则指出系统性问题，如淀粉样蛋白支持者的“小圈子”压制了替代研究，并推荐 Karl Herrup 的著作《如何不研究一种疾病》以获取批判性视角。

**标签**: `#Alzheimer's`, `#research methodology`, `#pharmaceutical industry`, `#amyloid hypothesis`, `#science policy`

---

<a id="item-9"></a>
## [HauhauCS 的未审查 LLM 基于抄袭的 Heretic 工具](https://www.reddit.com/r/LocalLLaMA/comments/1sw77p0/hauhaucs_of_uncensored_aggressive_fame_published/) ⭐️ 8.0/10

以流行未审查 LLM 模型闻名的 HauhauCS 发布了一个名为'reaper-abliteration'的软件包，该包是 Heretic abliteration 工具的抄袭分支，违反了 AGPL-3.0 许可证，删除了署名并添加了商业限制。 这一事件破坏了开源 LLM 社区的信任，因为 HauhauCS 的模型每月下载量超过 500 万次，抄袭行为违反了软件伦理和许可证合规性，可能影响依赖正确署名的用户和开发者。 证据显示，7/7 的模块文件名、30/32 的拒绝标记以及 30 多个函数名与 Heretic v1.2.0 完全相同，内部变量名如'good_residuals'和'bad_residuals'未作更改。Heretic 的原始创建者证实了这些发现。

reddit · r/LocalLLaMA · nathandreamfast · Apr 26, 13:13

**背景**: Abliteration 是一种无需重新训练即可从 LLM 中移除拒绝行为的技术，常用于创建未审查模型。Heretic 是一个开源工具，使用 Optuna 参数优化自动化此过程，采用 AGPL-3.0 许可证，要求衍生作品保留署名并采用相同许可证。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/p-e-w/heretic">GitHub - p-e-w/ heretic : Fully automatic censorship removal for...</a></li>
<li><a href="https://huggingface.co/blog/mlabonne/abliteration">Uncensor any LLM with abliteration</a></li>
<li><a href="https://opensource.stackexchange.com/questions/5524/are-license-headers-required-under-the-agplv3">agpl 3.0 - Are license headers required under the AGPLv3? -</a></li>

</ul>
</details>

**社区讨论**: 社区表达了强烈谴责，许多用户报告称因提问而被 HauhauCS 屏蔽。Heretic 的原始创建者确认了抄袭行为，用户指出这种不当行为损害了声誉和信任。

**标签**: `#plagiarism`, `#open-source`, `#LLM`, `#ethics`, `#license-violation`

---

<a id="item-10"></a>
## [Qwen3.6-27B INT4 在 RTX 5090 上达到 100+ tps](https://www.reddit.com/r/LocalLLaMA/comments/1sw21op/qwen3627bint4_clocking_100_tps_with_256k_context/) ⭐️ 8.0/10

Qwen3.6-27B 模型通过 AutoRound 量化为 INT4，在单张 RTX 5090 上使用 vLLM 0.19 实现了 105-108 tokens/秒的生成速度，并支持完整的 256k 上下文窗口，社区报告通过自定义补丁可达 160+ tps。 这表明拥有长上下文的 27B 参数大模型可以在消费级硬件上高效运行，使先进的 AI 能力更易于个人和小团队使用。 该配置使用 vLLM 搭配 flashinfer 注意力后端、FP8 KV 缓存和 3 个草稿头的 MTP 推测解码，在保持模型质量（KLD 远优于 NVFP4）的同时实现了高吞吐量。

reddit · r/LocalLLaMA · Kindly-Cantaloupe978 · Apr 26, 08:37

**背景**: Qwen3.6-27B 是 Qwen 系列中一个 270 亿参数的语言模型。INT4 量化减少了模型大小和内存带宽需求，而 vLLM 是一个高性能推理引擎，支持推测解码和 KV 缓存量化等多种优化来加速生成。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.vllm.ai/en/latest/index.html">vLLM</a></li>
<li><a href="https://deepwiki.com/vllm-project/vllm-ascend/6.4-speculative-decoding">Speculative Decoding | vllm-project/vllm-ascend | DeepWiki</a></li>

</ul>
</details>

**社区讨论**: 社区反应热烈，用户报告在 RTX 3090 上也有类似性能（71-83 tps），使用 Genesis 补丁甚至可达 160+ tps。部分用户讨论 INT4 27B 与 FP8 35B A3B 模型之间的权衡，还有用户询问针对 RTX 5060 Ti 等低端 GPU 的最佳配置。

**标签**: `#LLM inference`, `#quantization`, `#vLLM`, `#speculative decoding`, `#local LLM`

---

<a id="item-11"></a>
## [1900 名美国院士呼吁特朗普停止攻击科学](https://t.me/zaihuapd/41070) ⭐️ 8.0/10

2025 年 3 月 31 日，1900 名美国国家科学院、工程院和医学院成员（包括十多位诺贝尔奖得主）签署了一封由 13 位来自医学、流行病学、气候科学等领域的科学家起草的公开信，呼吁特朗普政府停止对美国科学的全面攻击。 顶尖科学家的空前动员标志着美国科学政策面临严重危机，可能削弱研究资金、创新能力和全球竞争力。这封信反映了对基础研究削减和科学机构政治干预日益加剧的担忧。 签名者包括诺贝尔奖得主 Harvey J. Alter、Francoise Barre-Sinoussi、Reinhard Genzel、Edvard I. Moser 和 May-Britt Moser。该信由 13 位科学家起草，于 2025 年 3 月 31 日在网上发布。

telegram · zaihuapd · Apr 26, 00:40

**背景**: 美国国家科学院、工程院和医学院是著名的荣誉学会，成员因杰出研究贡献而当选。特朗普第二任期大幅削减联邦研究资金，尤其是气候和社会科学领域，并加强对大学研究的审查，引发了对“人才外流”和科学产出下降的担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.news.cn/world/20260424/d705807106ef4889917d86c885575814/c.html">美媒：受特朗普政府政策冲击 美国科研呈收缩趋势</a></li>
<li><a href="https://casisd.cas.cn/zkcg/ydkb/kjqykb/2025/kjqykb2503/202505/t20250523_7790747.html">《自然》讨论特朗普科技政策走向 呼吁重视气候和能源安全----中国科学...</a></li>
<li><a href="https://news.cctv.com/2025/06/01/ARTIWWt0shYPiEdTBeyn9fSe250601.shtml">新闻分析丨科研停滞，人才外流——特朗普政府政策引发美科学界“寒潮”_新...</a></li>

</ul>
</details>

**标签**: `#science policy`, `#research funding`, `#US politics`, `#open letter`

---

<a id="item-12"></a>
## [砺算科技 7G100 显卡获微软 WHQL 认证](http://www.cnbeta.com.tw/articles/tech/1559976.htm) ⭐️ 8.0/10

砺算科技的 7G100 系列 GPU 获得了微软 WHQL 认证，成为国内首家、全球第四家获此认证的 GPU 公司。 这一里程碑展示了中国国产 GPU 发展的重大进展，性能接近 NVIDIA RTX 4060，并增强了国家在关键半导体组件上的自给自足能力。 该 GPU 采用 6nm 工艺及自研“天图”架构，实现了计算核心、指令集与软件栈的完全自主设计。在 Steel Nomad 测试中跑分为 2268，接近 RTX 4060。

telegram · zaihuapd · Apr 26, 02:59

**背景**: WHQL（Windows 硬件质量实验室）认证是微软官方的测试项目，确保硬件和驱动程序与 Windows 兼容且稳定。这是任何硬件产品获得广泛消费者采用的关键一步。砺算的这一成就使其与 NVIDIA、AMD 和 Intel 等主要 GPU 厂商并列。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nicsrs.com/whql">WHQL Certification - Windows Logo - Driver Signing - NicSRS</a></li>
<li><a href="https://store.steampowered.com/app/2695340/3DMark_Steel_Nomad/">3DMark Steel Nomad on Steam</a></li>

</ul>
</details>

**标签**: `#GPU`, `#WHQL`, `#Chinese semiconductor`, `#hardware`, `#AI`

---

<a id="item-13"></a>
## [顶级大学子域名被劫持用于发布色情和诈骗内容](https://arstechnica.com/security/2026/04/why-are-top-university-websites-serving-porn-it-comes-down-to-shoddy-housekeeping/) ⭐️ 8.0/10

包括加州大学伯克利分校和哥伦比亚大学在内的至少 34 所顶级大学的子域名被威胁组织 Hazy Hawk 劫持，用于发布色情内容和诈骗信息。攻击利用了管理员在停用子域名后未清理 CNAME 记录的漏洞。 此事件凸显了一个可能影响任何组织的关键域名管理漏洞，尤其是像大学这样具有高域名权威的机构。被劫持的页面在谷歌搜索结果中排名靠前，可能触及大量用户并损害机构声誉。 Hazy Hawk 至少自 2023 年 12 月以来一直活跃，针对废弃的云资源和 DNS 配置错误。已发现数百个子域名和数千个恶意页面出现在搜索引擎中。

telegram · zaihuapd · Apr 26, 09:02

**背景**: 子域名劫持是指攻击者通过利用悬空的 DNS 记录（例如指向已停用外部服务的 CNAME 记录）来获得对子域名的控制权。CNAME 记录将一个域名映射到另一个域名，如果目标服务被移除而未删除该记录，攻击者就可以认领它。这种攻击在安全圈内广为人知，但在域名管理实践中常被忽视。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/CNAME_record">CNAME record - Wikipedia</a></li>
<li><a href="https://thehackernews.com/2025/05/hazy-hawk-exploits-dns-records-to.html">Hazy Hawk Exploits DNS Records to Hijack CDC, Corporate ...</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Subdomain_takeover">Subdomain takeover - Security | MDN</a></li>

</ul>
</details>

**标签**: `#security`, `#domain hijacking`, `#DNS`, `#university`, `#cyberattack`

---

<a id="item-14"></a>
## [Friendster 以 3 万美元购得，计划打造实体接触社交网络](https://ca98am79.medium.com/i-bought-friendster-for-30k-heres-what-i-m-doing-with-it-d5e8ddb3991d) ⭐️ 7.0/10

作者以 2 万美元比特币加一个年广告收入约 9 千美元的域名购得 Friendster.com 域名，并计划将其复兴为一个需要物理手机接触才能连接的社交网络。 此次收购复兴了一个历史悠久的社交网络品牌，并引入了一种新颖的物理接触要求，可能解决连接僵化和算法内容控制的问题。 该域名从前任所有者（曾将其用作落地页）处购得；新主人计划推出一款应用，用户必须将手机放在一起才能连接，且连接一年后失效。

hackernews · ca98am79 · Apr 26, 20:41

**背景**: Friendster 是 2002 年推出的先驱社交网络，早于 Facebook，但因技术问题和竞争而衰落。后来被出售并最终关闭，域名一直闲置。新主人旨在通过要求物理接近才能连接来差异化，与当今算法驱动的平台形成对比。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@ashleighbredigkeit/the-story-of-friendster-c095201b7a6f">The Story of Friendster - Medium</a></li>
<li><a href="https://datasociety.net/points/a-working-history-of-the-verified-internet-2/">Data & Society — A Working History of the Verified Internet</a></li>
<li><a href="https://d3.harvard.edu/platform-digit/submission/before-facebook-there-was-friendster-yes-thats-right/">Before Facebook there was… Friendster? Yes, that's right!</a></li>

</ul>
</details>

**社区讨论**: 评论者提出了物理功能面临的先有鸡还是先有蛋的问题，并建议允许初始虚拟连接以获取动力。其他人则赞扬了连接失效的想法以对抗网络僵化，并指出在应用商店中难以找到该应用。

**标签**: `#social media`, `#domain names`, `#startup`, `#nostalgia`, `#acquisition`

---