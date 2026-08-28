---
layout: default
title: "Horizon Summary: 2026-08-15 (ZH)"
date: 2026-08-15
lang: zh
---

> 从 35 条内容中筛选出 15 条重要资讯。

---

**科技新闻**
1. [Qwen 3.8 27B 发布：开源模型本地推理获社区好评](#item-tech-news-1) ⭐️ 8.0/10
2. [Firefox 成为最后仍支持 uBlock Origin 的主流浏览器](#item-tech-news-2) ⭐️ 8.0/10
3. [GLM-5.3 发布：前沿编程与新兴网络能力引热议](#item-tech-news-3) ⭐️ 8.0/10
4. [AI 机器人实验室年测 300 万人体组织，挑战动物测试](#item-tech-news-4) ⭐️ 8.0/10
5. [小红书开源 dots3-note，280B MoE 仅 16B 激活](#item-tech-news-5) ⭐️ 8.0/10
6. [Opus 5 为何用起来更差：转向智能体导向的输出](#item-tech-news-6) ⭐️ 7.0/10
7. [RustDesk 在 Wayland 上实现真正无人值守远程访问](#item-tech-news-7) ⭐️ 7.0/10
8. [AI by Hand：动手理解 AI 模型数学原理](#item-tech-news-8) ⭐️ 7.0/10
9. [不分类，靠幻觉：用嵌入匹配 LLM 生成的假设标签](#item-tech-news-9) ⭐️ 7.0/10
10. [谷歌被令一周内取消第三方应用商店安装障碍](#item-tech-news-10) ⭐️ 7.0/10
11. [PostgreSQL 修复 to\_char 高危漏洞，可致任意代码执行](#item-tech-news-11) ⭐️ 7.0/10
12. [苹果联手阿里为中国训练专属 AI 大模型，有望成首个获批外企](#item-tech-news-12) ⭐️ 7.0/10

**财经新闻**
1. [伯克希尔二季度增持 Alphabet 至第三大重仓，并结束连续净卖出](#item-finance-news-1) ⭐️ 8.0/10
2. [高盛参与英伟达、英特尔和 Alphabet 的大型 AI 融资交易](#item-finance-news-2) ⭐️ 8.0/10
3. [苹果提交 App Store 外部购买抽成方案：最高 15%](#item-finance-news-3) ⭐️ 8.0/10

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [Qwen 3.8 27B 发布：开源模型本地推理获社区好评](https://huggingface.co/Qwen/Qwen3.8-27B-FP8) ⭐️ 8.0/10

Qwen 3.8 27B 是一款新发布的开源权重语言模型，凭借较强的推理能力和本地运行表现引发广泛讨论。其提供 FP8 量化版本并支持 MTP（多 token 预测），有助于降低部署门槛。在社区测试中，该模型能通过某些私人推理基准，但处理同一任务消耗的 token 数约为对比模型的 5 倍，耗时较长；实际速度受硬件和推理引擎影响，例如在 RTX 5090 上搭配 ninfer 引擎可达约 138 tokens/s。虽然并非范式级突破，但它为本地模型生态提供了一个高价值的新选择。

hackernews · erdaltoprak · 8月14日 15:00 · [社区讨论](https://news.ycombinator.com/item?id=49299605)

**「背景」** Qwen 3.8 是阿里巴巴开源大语言模型家族的最新一代，官方称其为迄今最强的 Qwen 开放模型系列；Qwen3.8-27B 于 2026 年 8 月 3 日随 Qwen 3.8-Max 一同公布，并承诺开放权重。Hugging Face 页面显示该模型提供 FP8 量化版本，但服务尚在准备中。此前 Qwen3.5 和 Qwen3.6 系列已被社区广泛采用，因此这次 27B 模型的发布被视为本地部署场景的重要进展。

**「影响」** 对需要本地部署开源模型的开发者而言，Qwen 3.8 27B 提供了一个兼具推理能力和量化/多 token 预测支持的新选项，并在特定硬件与推理引擎组合下可实现较高吞吐。不过，由于社区反馈基于个人基准和具体硬件，实际性能表现会因环境配置而有差异。

**「社区讨论」** 社区普遍认可其推理能力：有用户称它是继 Gemma 4 之后第二个能通过其私有基准的本地模型，也有评论者展示了在笔记本上生成的高质量 SVG 示例。与此同时，一些用户指出其 VRAM 使用效率不如 Gemma 4，思考轨迹风格的改变可能影响 MTP 预测，还有人报告通过 ninfer 引擎可显著提升生成速度。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@rosgluk/qwen-3-8-27b-is-coming-and-it-could-be-the-most-important-local-ai-release-of-2026-c1cf381d5292">Qwen 3.8 27B Is Coming - and It Could Be the Most Important Local AI Release of 2026 | by Rost Glukhov | Aug, 2026 | Medium</a></li>
<li><a href="https://www.yottalabs.ai/post/qwen-3-8-27b-specs-hardware-requirements-how-to-run-2026">Qwen 3.8 27B: Specs, Hardware Requirements, and How to Run It (2026) | Yotta Labs</a></li>
<li><a href="https://huggingface.co/Qwen/Qwen3.8-27B">Qwen/Qwen3.8-27B · Hugging Face</a></li>

</ul>
</details>

**标签**: `#Qwen`, `#large language models`, `#open source AI`, `#local inference`, `#model release`

---

<a id="item-tech-news-2"></a>
### [Firefox 成为最后仍支持 uBlock Origin 的主流浏览器](https://www.pcworld.com/article/3212428/firefox-is-now-the-last-major-browser-that-still-supports-ublock-origin.html) ⭐️ 8.0/10

随着基于 Chromium 的浏览器逐步因 Manifest V3 限制扩展能力，Firefox 现已成为唯一仍完整支持 uBlock Origin 的主流浏览器。这一变化标志着广告拦截生态的重要转折：uBlock Origin 这类依赖强大 WebRequest API 的扩展，在 Chrome、Edge 等浏览器上已无法以原有方式运行。Firefox 因此成为仍希望使用完整版 uBlock Origin 用户的主要选择，同时也凸显了浏览器厂商在隐私、广告过滤和扩展开放性上的分歧。

hackernews · DemiGuru · 8月14日 19:03 · [社区讨论](https://news.ycombinator.com/item?id=49303202)

**「背景信息」** Chrome 等 Chromium 系浏览器正在转向 Manifest V3，这一扩展规范限制了对网络请求的拦截能力，因此不再支持依赖完整拦截能力的 uBlock Origin（原版），而只允许功能受限的 uBlock Origin Lite。Mozilla 则明确表示 Firefox 会同时支持 Manifest V2 和 V3，并继续保留 webRequestBlocking 能力，使 uBlock Origin 在 Firefox 中继续可用。由于 Safari 和 DuckDuckGo 等其他主要非 Chromium 浏览器也不支持 uBlock Origin，Firefox 因此成为唯一仍支持这款扩展的主要浏览器。

**「影响」** Firefox 成为坚持使用完整版 uBlock Origin 的用户唯一的主要浏览器选择；继续使用其他主流浏览器则需改用 uBlock Origin Lite 等替代方案。

**「社区讨论」** 评论中有人称赞 Firefox 会人工审查 uBlock Origin 的每次更新，也有用户批评 Google 借 Manifest V3 削弱扩展自由度并质疑使用广告公司浏览器的做法；还有人询问 uBlock Origin Lite 的拦截效果是否足够。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.pcworld.com/article/3212428/firefox-is-now-the-last-major-browser-that-still-supports-ublock-origin.html">Firefox is now the last major browser that still supports uBlock Origin | PCWorld</a></li>
<li><a href="https://blog.mozilla.org/en/firefox/firefox-manifest-v3-adblockers/">Mozilla’s approach to Manifest V3: What’s different and why it matters for extension users | The Mozilla Blog</a></li>
<li><a href="https://www.neowin.net/news/firefox-gives-latest-update-on-ublock-origin-support-as-chrome-and-microsoft-edge-end-it/">Firefox gives latest update on uBlock Origin support as Chrome and Microsoft Edge end it - Neowin</a></li>

</ul>
</details>

**标签**: `#Firefox`, `#uBlock Origin`, `#privacy`, `#ad-blocking`, `#web browsers`

---

<a id="item-tech-news-3"></a>
### [GLM-5.3 发布：前沿编程与新兴网络能力引热议](https://z.ai/blog/glm-5.3) ⭐️ 8.0/10

Z.ai 发布 GLM-5.3，宣称具备前沿编程与新兴网络能力，并引发显著社区讨论。用户报告称，通过 Claude Code 等工具接入后，该模型可执行红队任务，包括 WordPress 插件 0-day、RCE 与 6.8 内核漏洞利用适配等。Z.ai 还疑似以规模化方式扫描开源与流行软件，并通过 cvd.z.ai 披露大量处于 embargo 状态的关键或高危 CVE。评论者认为其表现已接近 Sol 和 Fable，但本质上仍是 GLM 5.2 加后训练，权重预计约两周后发布。

hackernews · pella · 8月14日 05:19 · [社区讨论](https://news.ycombinator.com/item?id=49294997)

**「背景」** GLM-5.3 是 Z.ai 于 2026 年 8 月 14 日发布的大语言模型更新。它沿用了 GLM-5.2 的底座模型，官方称所有能力提升均来自扩展后的后训练（post-training），而非更换基础架构。该模型在编程任务上较 GLM-5.2 提升约 50%，并在 Terminal-Bench 3.0 和 Agents’ Last Exam \(CLI\) 等基准上达到开源最优水平，同时新增了网络空间攻防等“涌现”能力，并通过 ZCode 和 GLM Coding Plan 提供分阶段访问。

**「影响」** 根据 Z.ai 的披露，GLM-5.3 的后训练意外产生了利用链推理能力，并在 Linux、WebKit、FreeBSD 中发现了 1,097 个关键漏洞，同时在 269 个开源项目中发现了 2,436 个漏洞；因此，受影响项目的维护者与下游用户需要立即查看 Z.ai 的实时 CVE 清单并修补暴露的代码。Z.ai 将模型权重在发布后保留两周，也意味着希望在本地下游或微调该模型的团队需要等待更长时间。

**「社区讨论」** 社区整体认可模型能力，尤其对自动红队与漏洞挖掘效果感到惊讶；但也有观点质疑大规模扫描披露 CVE 的成本与必要性，并认为这仍是 GLM 5.2 的后训练变体，距离领先模型仅一步之遥。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.unite.ai/z-ai-launches-glm-5-3-with-frontier-coding-and-a-cyber-capability-that-outgrew-its-training/">Z.ai Launches GLM-5.3 With Frontier Coding and a Cyber ...</a></li>
<li><a href="https://kylon.io/blog/glm-5-3-launch-aug-2026">Z.ai launches GLM-5.3 for coding and cyber defense</a></li>
<li><a href="https://docs.z.ai/guides/llm/glm-5.3">GLM-5.3 - Overview - Z.AI DEVELOPER DOCUMENT</a></li>
<li><a href="https://www.techtimes.com/articles/324426/20260814/glm-53-post-training-produced-exploit-chains-zai-never-planned-finds-1097-critical-bugs.htm">GLM-5.3: Post-Training Produced Exploit Chains Z.ai Never ...</a></li>
<li><a href="https://venturebeat.com/technology/glm-5-3-is-here-with-advanced-cyber-capabilities-and-reportedly-already-found-a-serious-vulnerability-in-cursor">GLM-5.3 is here with advanced cyber capabilities — and ...</a></li>
<li><a href="https://moclaw.ai/blog/glm-5-3-vulnerability-discovery">GLM-5.3 Found 2,436 Real Vulnerabilities | MoClaw Blog</a></li>

</ul>
</details>

**标签**: `#AI`, `#large language models`, `#cyber security`, `#coding`, `#GLM`

---

<a id="item-tech-news-4"></a>
### [AI 机器人实验室年测 300 万人体组织，挑战动物测试](https://www.fastcompany.com/91589344/the-worlds-largest-biological-datacenter-could-help-make-animal-testing-obsolete) ⭐️ 8.0/10

据 Fast Company 报道，Vivodyne 在旧金山南部部署了 12 个“蜂巢”机器人实验室，利用 AI 设计实验并规模化培养人体组织，每年可对 300 多万个人体组织开展受控试验，宣传容量是美国全部临床试验总和的两倍。目前约 90% 的临床试验在通过动物测试后仍告失败，而该系统旨在用更接近人体、由 AI 驱动的组织测试来更好地预测新药疗效与安全性。这一规模尚属行业首次，但其能否真正替代动物测试仍有待独立验证。

telegram · zaihuapd · 8月14日 01:48

**「背景」** 药物研发的传统路径是先通过动物测试评估安全性和有效性，但动物与人体差异巨大，约 90%至 95%的临床试验即使在动物测试通过后仍会失败。Vivodyne 是一家利用机器人和 AI 规模化培养并测试人体组织的生物技术公司，于 2025 年 5 月获得 4000 万美元 A 轮融资，旨在用人体组织测试取代动物测试，以降低临床试验的高失败率。

**「影响」** 对药物研发企业而言，若验证成立，这种高通量人体组织测试可显著降低临床前阶段的失败风险，并减少对动物实验的依赖；但监管接受度和预测能力仍需进一步证据支持。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.vivodyne.com/">Vivodyne | Make biology computable</a></li>
<li><a href="https://www.businesswire.com/news/home/20250528498236/en/Vivodyne-to-Replace-Animal-Testing-With-$40-Million-Funding-to-Reverse-95-Clinical-Trial-Failure-Rate">Vivodyne to Replace Animal Testing With $40 Million Funding to Reverse 95% Clinical Trial Failure Rate</a></li>

</ul>
</details>

**标签**: `#AI`, `#biotech`, `#robotics`, `#drug testing`, `#human tissue`

---

<a id="item-tech-news-5"></a>
### [小红书开源 dots3-note，280B MoE 仅 16B 激活](https://x.com/dotsstudioai/status/2088083314855018521) ⭐️ 8.0/10

小红书 dots 实验室开源了 dots3-note preview，这是 dots3 系列首个开放权重模型。模型总参数量达 280B，采用 MoE 架构，每次推理仅激活 16B 参数，支持 512K 上下文，并能处理文字、图片、视频和音频等多模态数据。该模型引入新的 TEMPO 强化学习方法，通过自批判和测试时价值估计训练长程智能体，已在 Hugging Face 上开放权重。官方还同步发布了 VibeSearchBench 和 VibeLifeBench 两个真实场景智能体基准，便于社区评估。

telegram · zaihuapd · 8月14日 08:27

**「背景」** 小红书（RedNote）dots 实验室开源的 dots3-note preview 是 dots3 系列首个开放权重模型，采用 Mixture-of-Experts（MoE）架构，总参数 280B，每次推理仅激活 16B 参数，支持最高 512K token 上下文，并可处理文本、图片、视频和音频。模型引入新的强化学习方法 TEMPO，通过自批判和测试时价值估计来训练长程智能体；同步发布的 VibeSearchBench 和 VibeLifeBench 是两个真实场景智能体基准，用于评估此类能力。

**「影响」** 开发者现可直接从 Hugging Face 下载 dots3-note preview 的开放权重，并在 vLLM main 上获得原生支持，以约 16B 激活参数低成本部署 280B 参数的多模态模型，处理长达 512K 上下文及文字、图片、视频和音频输入。同步发布的 TEMPO 强化学习方法和 VibeSearchBench、VibeLifeBench 基准，为长程智能体训练与真实场景评测提供了可复用的公开工具；不过官方尚未公布详细性能数据，实际收益仍需开发者自行验证。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/studio-dots-ai/dots3-note-prev">GitHub - studio-dots-ai/dots3-note-prev: dots3 note preview</a></li>
<li><a href="https://huggingnews.com/ai/rednote-open-sources-280b-dots3-note-model-first-open-weight-release-in-48810470">RedNote Open Sources 280B dots3-note Model, First Open Weight ...</a></li>
<li><a href="https://www.bannedbook.org/bnews/itnews/20260814/2348931.html">小红书开源 dots3-note，280B MoE 仅 16B 激活参数 - 禁闻网</a></li>
<li><a href="https://www.163.com/dy/article/L4A41D5M0511AQHO.html">刚刚，小红书开源dots3-note！IMO 42分满分同系列模型来了|调用|知名企业_网易订阅</a></li>
<li><a href="https://huggingface.co/dots-studio/dots3-note-prev">dots-studio/dots3-note-prev · Hugging Face</a></li>

</ul>
</details>

**标签**: `#open-source`, `#MoE`, `#multimodal`, `#reinforcement-learning`, `#benchmarks`

---

<a id="item-tech-news-6"></a>
### [Opus 5 为何用起来更差：转向智能体导向的输出](https://mun-logadan.github.io/why-does-opus-5-feel-worse/) ⭐️ 7.0/10

一位开发者撰文分析为何 Opus 5 的使用体验变差，认为模型在训练上越来越以智能体而非人类为目标，导致输出变成“智能体语言”，缺乏人类可读的优雅。社区讨论中，多位用户抱怨 Opus 5 写作过于省略、抽象，以及过度“诚实”和“忏悔”式的表达，令人疲惫。有用户因沟通成本转向 OpenAI 的 Sol，并称其“好相处得多”。该分析虽属主观体验，但引发关于大模型沟通风格和智能体化趋势的广泛讨论。

hackernews · numeri · 8月14日 10:12 · [社区讨论](https://news.ycombinator.com/item?id=49296740)

**「背景」** Claude Opus 5 是 Anthropic 于 2026 年 7 月发布的最新旗舰模型，官方称其在生命科学、金融研究等领域的基准表现优于 Opus 4.8。同时，官方提示词文档也明确指出，该模型在响应冗长度、代理式叙述、子代理委派和自我纠错等方面存在显著的行为差异，这为用户关于其沟通风格“更差”的讨论提供了背景。

**「影响」** 对日常使用 Opus 5 的开发者而言，其省略且抽象的表达风格可能降低协作效率；评论中已有用户因此转向 OpenAI 产品。

**「社区讨论」** 评论者普遍认可作者的判断，认为 Opus 5 的写作“过于省略”且偏向“智能体语言”，并举例称其句子“围绕观点绕圈后突然落地”。也有用户反馈 OpenAI Sol 更“好相处”，并担忧若 Anthropic 不及时调整，可能引发企业客户流失。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/news/claude-opus-5">Introducing Claude Opus 5 \ Anthropic</a></li>
<li><a href="https://www.anthropic.com/claude/opus">Claude Opus \ Anthropic</a></li>
<li><a href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5">Prompting Claude Opus 5 - Claude Platform Docs</a></li>

</ul>
</details>

**标签**: `#Opus 5`, `#LLM communication`, `#AI agents`, `#developer experience`, `#AI analysis`

---

<a id="item-tech-news-7"></a>
### [RustDesk 在 Wayland 上实现真正无人值守远程访问](https://rustdesk.com/blog/unattended-remote-access-wayland/) ⭐️ 7.0/10

RustDesk 现已支持在 Wayland 上实现真正的无人值守远程访问，改善了 Linux 用户的远程桌面体验。该更新解决了 Wayland 会话中无人值守访问此前较难实现的限制，对使用 Wayland 的用户而言是高价值改进。这属于增量更新而非突破性变化，但社区有实际需求，例如有用户表示两天前刚遇到相关问题。需要留意的是，RustDesk 自托管时仍不支持加密连接，这是一个已知限制。

hackernews · rustdesk · 8月14日 16:12 · [社区讨论](https://news.ycombinator.com/item?id=49300759)

**「背景」** Wayland 协议出于安全和隐私考虑，对屏幕捕获和输入注入设置了严格限制，这使得许多远程桌面工具在 Wayland 会话中难以实现无人值守访问，通常需要现场用户逐次确认。RustDesk 此前也受此限制，无法在没有人工批准的情况下远程连接 Wayland 桌面。此次更新让 RustDesk 能够提供真正的无人值守远程访问，无需远程机器上有人在场批准每次会话；不过图形登录界面仍是特殊情况，因为它出现在用户 Wayland 会话启动之前。

**「影响」** RustDesk 用户现在可以在 Wayland 上获得无人值守远程访问能力，简化了远程管理与支持流程。不过，自托管用户仍无法使用加密连接，这限制了其在安全敏感环境中的使用。

**「社区讨论」** 社区成员对此次更新表示欢迎，有用户提到两天前刚遇到此问题并很高兴看到解决。也有用户指出 RustDesk 自托管时仍不支持加密连接（GitHub issue \#3714），另有用户询问 RustDesk 与 VNC、Remmina over SSH/Tailscale 等方案的比较。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://rustdesk.com/blog/unattended-remote-access-wayland/">Unattended Remote Access on Wayland with RustDesk — RustDesk</a></li>
<li><a href="https://github.com/rustdesk/rustdesk/discussions/10016">Wayland: Select the screen to be shared (Operate on the peer ...</a></li>

</ul>
</details>

**标签**: `#remote desktop`, `#Wayland`, `#RustDesk`, `#open source`, `#Linux`

---

<a id="item-tech-news-8"></a>
### [AI by Hand：动手理解 AI 模型数学原理](https://www.byhand.ai/) ⭐️ 7.0/10

AI by Hand 是 By Hand Research 的研究出版物，由 Tom Yeh 教授创办，通过“动手算”练习从数学和算法层面解释 AI 模型，帮助读者理解模型的可解释性与内部机制。该出版物提供免费文章并举办直播研讨会，订阅者可免费获取新文章，会员则可访问完整研究资料库。它不同于常见的工具使用教程，而是聚焦于模型底层原理，适合希望深入理解 AI 基础的学习者和研究者。社区讨论中，它也被推荐为从零构建 LLM 的相关阅读材料。

hackernews · sans\_souse · 8月14日 15:58 · [社区讨论](https://news.ycombinator.com/item?id=49300568)

**「背景」** AI by Hand 是 Tom Yeh 教授创立的研究出版物，隶属于 By Hand Research，旨在从数学和算法层面研究模型的可解释性与可解释性。Tom Yeh 是科罗拉多大学博尔德分校计算机科学系的教授，其研究致力于通过方法、系统和交互技术让现代 AI 模型更加可解释、可控和可用。该出版物为订阅者提供免费的新文章，并举办直播研讨会。

**「影响」** 对机器学习学习者和模型可解释性研究者而言，这是一个由学术研究者维护、可免费获取的系统性学习资源，有助于弥补概念式讲解与数学/算法底层原理之间的空白。

**「社区讨论」** 有评论者将其与“Train your own LLM”“Deep Learning \(No Starch Press\)”等从零构建和可视化入门资源并列推荐，也有人分享了受 micrograd 启发的类似项目 ml-by-hand；同时有用户表示不清楚网站内容，因为越过订阅页后只看到文章描述链接，需要成为订阅者才能阅读。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.byhand.ai/about">About - AI by Hand ✍️</a></li>
<li><a href="https://www.colorado.edu/cs/tom-yeh">Tom Yeh | Computer Science | University of Colorado Boulder</a></li>

</ul>
</details>

**标签**: `#AI`, `#machine learning`, `#model interpretability`, `#education`, `#research`

---

<a id="item-tech-news-9"></a>
### [不分类，靠幻觉：用嵌入匹配 LLM 生成的假设标签](https://simonwillison.net/2026/Aug/14/dont-classify-hallucinate/) ⭐️ 7.0/10

Simon Willison 在 2026 年 8 月 14 日介绍了 Doug Turnbull 提出的“不要分类，要幻觉”方法，用来给自己博客里大量未打标签的旧文章补标签。Simon 的博客共有 1,856 个标签，数量太大，无法一次性全部提交给 LLM 并让它判断哪些标签匹配内容。该方法的要点是先让 LLM 在不看到现有标签表的情况下自由生成“从未见过”的假设分类，再用向量嵌入把这些假设分类映射到现有语料中最接近的具体标签。Doug 的示例提示还会给出标签的层级形状，例如“家具 / 客厅家具 / 咖啡桌与茶几 / 咖啡桌”，帮助模型生成更贴近实际体系的猜测。这样可以避免把完整标签表塞进提示词，同时保留已有标签体系。

rss · Simon Willison · 8月14日 21:54

**「背景」** 传统的 LLM 分类通常需要把候选标签列表放进提示词，让模型从中选择；当标签表很大时，这会消耗大量上下文窗口，甚至超出模型限制。向量嵌入可以把文本映射成语义向量，通过向量距离或相似度找到语义相近的内容。Doug Turnbull 的方法正是把这两者结合：先生成假设标签，再在向量空间里检索最接近的既有标签。

**「影响」** 这一技巧让拥有大型或异构标签体系的维护者能够用很小的提示词完成 LLM 标注，同时保持与现有标签体系的一致性；实际效果仍取决于嵌入模型的质量和标签表在语义空间中的覆盖程度。

**标签**: `#LLM`, `#embeddings`, `#tagging`, `#search`, `#AI`

---

<a id="item-tech-news-10"></a>
### [谷歌被令一周内取消第三方应用商店安装障碍](https://www.androidauthority.com/google-play-store-remove-third-party-app-store-friction-3698697/) ⭐️ 7.0/10

美国加州北区联邦地区法院法官 James Donato 在 Epic 诉谷歌反垄断案中下令，谷歌必须在一周内删除 Play Store 中安装第三方安卓应用商店前的多余步骤和警告弹窗，使安装过程与普通安卓应用一样直接。法院认为这些“查看”后才出现“安装”按钮等设计是蓄意的反竞争摩擦，意在吓退普通用户；此前陪审团已裁定谷歌在安卓应用分发上构成非法垄断。该命令直接影响 Google Play 对竞品应用商店的分发控制，是案件救济阶段的重要措施。

telegram · zaihuapd · 8月14日 09:55

**「背景」** Epic Games 对谷歌提起的反垄断诉讼指控谷歌在安卓应用分发市场存在非法垄断行为。2024 年 10 月，美国地区法官 James Donato 发布永久禁令，要求谷歌降低第三方安卓应用商店的安装门槛；2025 年 7 月，第九巡回上诉法院在 147 F.4th 917 号判决中维持了这一裁定。此次要求谷歌在一周内删除安装第三方商店时的多余警告步骤，属于该禁令后续合规监督的一部分。

**「影响」** 对安卓用户和第三方应用商店开发者而言，安装竞品商店的门槛将显著降低，Google Play 当前通过警告和多步操作维持的分发壁垒至少在这一救济措施中被移除。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Epic_Games_v._Google">Epic Games v. Google - Wikipedia</a></li>
<li><a href="https://www.techtimes.com/articles/324467/20260814/google-buried-rival-app-stores-play-store-search-judge-gives-week-fix.htm">Google Buried Rival App Stores in Play Store Search: Judge Gives Week to Fix</a></li>

</ul>
</details>

**标签**: `#antitrust`, `#google`, `#android`, `#app stores`, `#epic games`

---

<a id="item-tech-news-11"></a>
### [PostgreSQL 修复 to\_char 高危漏洞，可致任意代码执行](https://www.postgresql.org/support/security/CVE-2026-14669/) ⭐️ 7.0/10

PostgreSQL 项目披露高危漏洞 CVE-2026-14669，该漏洞存在于 to\_char\(timestamptz\) 函数处理超长 POSIX 时区缩写的过程中，可引发堆缓冲区溢出，使能够设置时区的低权限数据库用户以 PostgreSQL 服务进程的操作系统权限执行任意代码，CVSS 评分为 8.8。受影响版本包括 18.5、17.11、16.15、15.19 和 14.24 之前的所有版本；由于 18.5 因回归问题未正式发布，18 系列用户应直接升级至 18.6，其他用户应分别升级至 17.11、16.15、15.19 或 14.24。此次修复属于小版本安全更新，不需要转储数据库或运行 pg\_upgrade，只需更新程序文件并重启服务即可。

telegram · zaihuapd · 8月14日 14:35

**「背景」** to\_char\(timestamptz\) 是 PostgreSQL 中用于将带时区的时间戳格式化为字符串的函数，在处理 POSIX 时区缩写时需要解析长度不受限的用户输入。此类格式化函数若缺少对超长输入的边界检查，就可能在内存中写出越界数据，进而被利用来破坏内存并在服务进程中植入恶意代码。

**「影响」** 使用受影响 PostgreSQL 版本且允许低权限数据库账户设置时区的部署应尽快应用安全更新，否则攻击者可能以数据库服务进程的权限执行任意代码，直接威胁数据库的机密性、完整性和可用性。

**标签**: `#postgresql`, `#security`, `#vulnerability`, `#cve`, `#database`

---

<a id="item-tech-news-12"></a>
### [苹果联手阿里为中国训练专属 AI 大模型，有望成首个获批外企](https://www.reuters.com/business/retail-consumer/apple-trains-its-own-ai-model-china-market-with-alibabas-support-sources-say-2026-08-14/) ⭐️ 7.0/10

知情人士称，苹果已专门为中国市场训练一款大语言模型，并获阿里巴巴支持，改变此前依赖第三方模型的策略。Apple Intelligence 预计将在未来数月内随 iOS 更新在中国上线。中国网信办已于上月备案苹果的生成式 AI 服务，若落地苹果将成为首个获北京批准在华提供自有 AI 模型的外国公司。报道基于未具名消息源，缺乏技术细节。

telegram · zaihuapd · 8月14日 14:47

**「背景」** 苹果此前在中国市场并未直接提供自有的生成式 AI 服务，而是依赖与本地第三方模型合作来满足合规要求。据报道，苹果现正与阿里巴巴合作，为中国市场专门训练大语言模型，并已获得阿里巴巴的技术支持；相关生成式 AI 服务也已向中国网信办备案。中国对生成式 AI 服务实行备案和审批管理，外国公司若想直接向中国用户提供自有 AI 模型，需通过这一监管程序。

**「影响」** 若落地，苹果将成为首家获北京批准在华提供自有 AI 模型的外国公司，这会显著改变其在华智能手机市场的竞争态势，并可能为其他美国科技公司与中方合作提供范例。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://global.chinadaily.com.cn/a/202502/14/WS67ae9fd8a310c240449d5324.html">Partnership with Apple recognition of Alibaba&#x27;s AI ...</a></li>
<li><a href="https://finance.yahoo.com/technology/ai/articles/exclusive-apple-trains-own-ai-042135013.html?fr=sycsrp_catchall">Exclusive-Apple trains its own AI model for China market with ...</a></li>
<li><a href="https://finance.yahoo.com/technology/ai/articles/apple-trains-china-specific-ai-140316517.html?fr=sycsrp_catchall">Apple trains China-specific AI model with Alibaba&#x27;s help</a></li>
<li><a href="https://www.macrumors.com/2026/08/14/apple-trained-own-ai-model-for-china/">Apple Trained Own AI Model for China Market With Help From ...</a></li>
<li><a href="https://www.reuters.com/business/retail-consumer/apple-trains-its-own-ai-model-china-market-with-alibabas-support-sources-say-2026-08-14/">EXCLUSIVE: Apple trains its own AI model for China market ...</a></li>

</ul>
</details>

**标签**: `#Apple`, `#AI`, `#China`, `#Alibaba`, `#LLM`

---

## 财经新闻

<a id="item-finance-news-1"></a>
### [伯克希尔二季度增持 Alphabet 至第三大重仓，并结束连续净卖出](https://www.cnbc.com/2026/08/14/berkshire-hathaway-boosts-alphabet-to-a-top-three-holding-ups-delta-and-housing-bets.html) ⭐️ 8.0/10

伯克希尔哈撒韦的二季度监管文件显示，公司大幅增持 Alphabet，使其成为第三大美股持仓，同时增持达美航空和房屋建筑商。截至 6 月底，Alphabet 持仓约 1.06 亿股、市值 379 亿美元，环比增加 83%；伯克希尔还结束连续 14 个季度净卖出，二季度净买入近 200 亿美元股票。

rss · CNBC Finance · 8月14日 21:06

**「背景」** 这次增持中很大一部分来自 6 月初 Alphabet 为 AI 基础设施融资而发行的 100 亿美元私募股票；伯克希尔此前已连续 14 个季度净卖出，并在疫情期间清仓航空股。

**标签**: `#Berkshire Hathaway`, `#Alphabet`, `#Delta Air Lines`, `#Homebuilders`, `#Portfolio Management`

---

<a id="item-finance-news-2"></a>
### [高盛参与英伟达、英特尔和 Alphabet 的大型 AI 融资交易](https://www.cnbc.com/2026/08/14/goldmans-latest-cash-cow-is-all-about-funding-the-ai-infrastructure-boom.html) ⭐️ 8.0/10

高盛参与了三项大型 AI 融资安排：英伟达宣布由高盛等六家机构合力筹集 5000 亿美元用于 AI 基础设施建设，英特尔将 20 亿美元增发（最初为 15 亿美元）由高盛担任联席账簿管理人，Alphabet 的 850 亿美元增发（最初为 80 亿美元）也由高盛协助。除英特尔和 Alphabet 的增发为已公布的实际交易外，英伟达融资目前只有不具约束力的谅解备忘录，高盛的具体出资额和客户等细节尚未披露。

rss · CNBC Finance · 8月14日 20:05

**「背景」** 在股票增发中，银行通常以折扣价从发行人处买入股票，再以公开发行价卖给机构客户，差价形成承销费；因此大型科技公司的 AI 资本开支热潮能为高盛等头部投行带来可观收入。

**标签**: `#Goldman Sachs`, `#AI infrastructure`, `#equity offerings`, `#capital markets`, `#investment banking`

---

<a id="item-finance-news-3"></a>
### [苹果提交 App Store 外部购买抽成方案：最高 15%](https://9to5mac.com/2026/08/13/apple-proposes-commissions-of-up-to-15-for-off-app-store-purchases-in-the-us/) ⭐️ 8.0/10

苹果已向美国法院提交 App Store 外部购买抽成方案，费率最高为 15%：标准应用抽成 15%，视频、新闻等合作项目及订阅续费抽成 10%，小型企业计划应用抽成 5%。目前这仍是提案，还需等待 Epic 的回应及法院后续审理。

telegram · zaihuapd · 8月14日 02:33

**「背景」** 此方案源于苹果与《堡垒之夜》开发商 Epic Games 的反垄断诉讼。此前联邦法官认定苹果“故意”未遵守法院命令，最高法院已受理相关争议。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://applemagazine.com/apple-app-store-fees-external-purchases/">Apple Proposes 15% App Store Fees for External Purchases</a></li>
<li><a href="https://www.courthousenews.com/supreme-court-takes-apple-contempt-fight-over-app-store-fees-on-third-party-payments/">Supreme Court takes Apple contempt fight over App Store fees ...</a></li>

</ul>
</details>

**标签**: `#Apple`, `#App Store`, `#antitrust`, `#commissions`, `#Epic Games`

---