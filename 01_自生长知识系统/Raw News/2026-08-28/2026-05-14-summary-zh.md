---
layout: default
title: "Horizon Summary: 2026-05-14 (ZH)"
date: 2026-05-14
lang: zh
---

> From 40 items, 12 important content pieces were selected

---

1. [TextGen 以原生桌面应用形式发布，开源替代 LM Studio](#item-1) ⭐️ 9.0/10
2. [LLM 推动个人软件开发：软件的 Emacs 化](#item-2) ⭐️ 8.0/10
3. [告别 GitHub，迁移至 Forgejo](#item-3) ⭐️ 8.0/10
4. [ProPublica 揭露医保算法拒赔系统](#item-4) ⭐️ 8.0/10
5. [CSP 许可列表实验](#item-5) ⭐️ 8.0/10
6. [Fragnesia：Linux 内核新本地提权漏洞](#item-6) ⭐️ 8.0/10
7. [重新审视 mshare：Linux 共享内存的页表共享](#item-7) ⭐️ 8.0/10
8. [德国主权技术基金向 KDE 投资超 100 万欧元](#item-8) ⭐️ 8.0/10
9. [谷歌关闭免费搜索，Cloudflare 拦截 AI 爬虫：社区寻找替代方案](#item-9) ⭐️ 8.0/10
10. [DramaBox：基于 LTX 2.3 的开源 expressive 语音模型](#item-10) ⭐️ 8.0/10
11. [三星工会罢工致芯片产出骤降，供应链面临风险](#item-11) ⭐️ 8.0/10
12. [小米开源 OneVL：自动驾驶一步潜空间推理框架](#item-12) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [TextGen 以原生桌面应用形式发布，开源替代 LM Studio](https://www.reddit.com/r/LocalLLaMA/comments/1tbyyee/textgen_is_now_a_native_desktop_app_opensource/) ⭐️ 9.0/10

TextGen（原 text-generation-webui）已从 Web 界面转变为免安装、可移植的桌面应用，支持 Windows、Linux 和 macOS，采用精美的 Electron 界面，且无任何出站请求。 此次更新填补了开源本地大模型生态中的一个重要空白，提供了一个免费、私密且完全开源的替代方案，与流行的专有软件 LM Studio 形成竞争，让用户拥有更多控制权。 TextGen 提供 CUDA、Vulkan、纯 CPU、Apple Silicon/Intel 和 ROCm 的便携构建；它使用 ik_llama.cpp，提供了 LM Studio 和 Ollama 所用的原生 llama.cpp 所没有的新量化类型。

reddit · r/LocalLLaMA · oobabooga4 · May 13, 13:00

**背景**: TextGen 由 oobabooga 于 2022 年 12 月创建，早于 Llama 和 llama.cpp，是最早流行的本地大语言模型 Web 界面之一。LM Studio 作为主要替代方案，同样是 Electron 应用，但属于专有软件且会收集系统信息。Electron 是一个使用 Web 技术构建跨平台桌面应用的框架。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/LM_Studio">LM Studio</a></li>
<li><a href="https://mljourney.com/lm-studio-complete-setup-and-usage-guide/">LM Studio: Complete Setup and Usage Guide - ML Journey</a></li>
<li><a href="https://www.electronjs.org/">Build cross-platform desktop apps with JavaScript, HTML, and CSS | Electron</a></li>

</ul>
</details>

**社区讨论**: 社区反应极为积极，用户对拥有一个私密且开源的 LM Studio 替代方案感到兴奋。许多人回忆起最初使用该项目的时光，并赞赏其持续改进；部分用户询问技术细节，如升级到 Gradio 6 或安装最新 llama.cpp。

**标签**: `#LLM`, `#open-source`, `#desktop app`, `#local AI`, `#TextGen`

---

<a id="item-2"></a>
## [LLM 推动个人软件开发：软件的 Emacs 化](https://sockpuppet.org/blog/2026/05/12/emacsification/) ⭐️ 8.0/10

一篇博客文章指出，LLM 让个人软件开发变得极其容易，软件正演变为每个用户高度个性化、可定制的“Emacs 配置文件”，从预包装工具转向个人定制工具。 这标志着软件创作可能走向民主化，用户能轻松定制应用以满足精确需求，减少对通用产品的依赖，重燃 1960 年代个人计算的原始理念。 知名安全研究员 tptacek 和 dang 赞同这一观点，tptacek 列举了多个应用类别（如播客应用、笔记应用），LLM 生成的解决方案已能超越商业产品。“Emacs 化”一词源自将整个 GNU 系统变得像 Emacs 一样可扩展的愿景。

hackernews · rdslw · May 13, 07:06 · [社区讨论](https://news.ycombinator.com/item?id=48118727)

**背景**: Emacs 是一款高度可扩展的文本编辑器，用户可通过 Lisp 代码几乎自定义一切。“Emacs 化”概念源于 Guile 项目文档，设想未来程序像 Emacs 扩展一样在 Guile（一种 Lisp 解释器）内运行。本篇新闻将此概念扩展到 LLM，认为 AI 现使非程序员也能轻松构建定制软件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://wingolog.org/archives/2009/01/07/a-brief-history-of-guile">a brief history of guile — wingolog</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍赞同：tptacek 列出了 LLM 构建工具已超越商业替代品的具体应用类别；dang 表示他一直在倡导这一观点；SoftTalker 提醒个人软件本是家庭计算的最初愿景。但 shaokind 指出 Emacs 本身教的是脆弱的定制方法，而非顺畅的个人软件开发。

**标签**: `#software development`, `#AI`, `#LLMs`, `#personal software`, `#customization`

---

<a id="item-3"></a>
## [告别 GitHub，迁移至 Forgejo](https://jorijn.com/en/blog/leaving-github-for-forgejo/) ⭐️ 8.0/10

一位开发者记录了从 GitHub 迁移到自托管的 Forgejo 平台的过程，强调了去中心化和控制权的好处，同时指出了失去社交图谱这一取舍。 这一故事反映了开发者中日益增长的远离 GitHub 等中心化平台的趋势，背后的驱动力是对控制权、隐私以及对公司基础设施依赖的担忧。它突出了采用去中心化替代方案时的实际考虑和挑战。 该作者在自己的硬件上自托管 Forgejo，获得了完全控制权，但失去了 GitHub 的社交图谱功能，如星标、关注者和贡献记录。他们指出 GitSocial 等工具有助于保留和重建部分社交连接。

hackernews · jorijn · May 13, 12:54 · [社区讨论](https://news.ycombinator.com/item?id=48121266)

**背景**: Forgejo 是一个自托管的轻量级软件锻炉，使用 Go 语言编写，基于 GPLv3 许可，提供 Git 仓库托管、问题跟踪和协作功能。它源自 Gitea 的分支，强调社区治理。与 GitHub 这种中心化服务不同，Forgejo 允许个人和组织托管自己的实例，促进去中心化。Codeberg 等项目提供公共 Forgejo 实例，并且联邦支持正在开发中，以实现不同锻炉之间的互联。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Forgejo">Forgejo</a></li>
<li><a href="https://forgejo.org/">Forgejo – Beyond coding. We forge.</a></li>

</ul>
</details>

**社区讨论**: 评论表达了对去中心化的热情，一些用户已经自托管或向 Forgejo 和 Codeberg 捐款以支持联邦功能。其他人则提醒要维护 GitHub 镜像以保证可见性，并讨论了 GitSocial 等工具用于跨锻炉协作。还有关于 AI 爬虫以及 GitHub 因 AI 驱动使用量增加而面临的扩展问题的担忧。

**标签**: `#Git`, `#self-hosting`, `#decentralization`, `#Forgejo`, `#open source`

---

<a id="item-4"></a>
## [ProPublica 揭露医保算法拒赔系统](https://www.propublica.org/article/evicore-health-insurance-denials-cigna-unitedhealthcare-aetna-prior-authorizations) ⭐️ 8.0/10

ProPublica 发布调查，详细说明了 Cigna、UnitedHealthcare 和 Aetna 等健康保险公司如何使用算法和非医生审核员系统性地拒绝承保，常常将程序标记为“非医疗必需”。 这种做法引发了关于 AI 在医疗领域应用的深刻伦理担忧，因为算法拒绝可能绕过个体化临床判断，导致不当拒赔和患者伤害，影响数百万美国参保人。 根据报道，算法标记潜在问题并将请求发送给内部护士和医生审查，但只有医生才能做出最终拒绝；2022 年与 Carelon 的 1300 万美元和解凸显了诸如将传真机设置为仅接收 5-10 页等策略。

hackernews · ceejayoz · May 13, 19:01 · [社区讨论](https://news.ycombinator.com/item?id=48126000)

**背景**: 预授权是常见的保险流程，需要医疗服务的预先批准。对算法偏见和此类决策缺乏透明度的担忧日益增加，Medicare Advantage 计划中也存在类似问题。2024 年提出的解决 AI 偏见的联邦法规未能最终确定，政府正在通过试点项目在传统 Medicare 中测试 AI。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.kff.org/patient-consumer-protections/regulation-of-ai-in-prior-authorization-and-claims-review-a-look-at-federal-and-state-consumer-protections/">Regulation of AI in Prior Authorization and Claims Review: A Look at Federal and State Consumer Protections | KFF</a></li>
<li><a href="https://www.pbs.org/newshour/show/how-algorithms-are-being-used-to-deny-health-insurance-claims-in-bulk">How algorithms are being used to deny health insurance claims</a></li>
<li><a href="https://councils.forbes.com/blog/how-ai-is-reshaping-prior-authorization-in-health-insurance">How AI Is Reshaping Prior Authorization in Health Insurance</a></li>

</ul>
</details>

**社区讨论**: 医生评论者对非医生“同行”进行拒赔审查表示沮丧，其他人批评美国人均医疗支出高昂以及使用算法控制成本。一位评论者强调了一起诉讼，揭露了通过限制传真页数来阻碍承保请求的策略。

**标签**: `#healthcare`, `#AI ethics`, `#insurance`, `#algorithm bias`, `#investigative journalism`

---

<a id="item-5"></a>
## [CSP 许可列表实验](https://simonwillison.net/2026/May/13/csp-allow/#atom-everything) ⭐️ 8.0/10

Simon Willison 发布了一个工具，展示了如何通过拦截 fetch 错误，在受 CSP 保护的沙箱 iframe 中动态允许域名。父窗口会提示用户将被阻止的源添加到许可列表中并刷新页面。 这种方法提供了一种实用的方式来处理沙箱 iframe 中的 CSP 限制，而无需全面放宽安全策略。它使 Web 安全从业者能够构建用户控制的许可列表，在保持强大安全性的同时提高可用性。 该工具在沙箱 iframe 内使用自定义的 fetch() 函数来捕获 CSP 违规，然后将违规信息传递给父窗口。父窗口可以提示用户将阻止的域名添加到 connect-src 许可列表，之后刷新页面以应用新策略。

rss · Simon Willison · May 13, 04:50

**背景**: 内容安全策略（CSP）是一种安全标准，用于限制网页可以加载的资源。沙箱 iframe 隔离了嵌入式内容，但可能过于严格，特别是对于需要动态域名的 API。通常，CSP 许可列表是静态的，需要手动更新。这个实验通过拦截 fetch 错误展示了一种动态替代方案。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://simonwillison.net/2026/May/13/csp-allow/">Tool: CSP Allow-list Experiment | Simon Willison’s Weblog</a></li>

</ul>
</details>

**标签**: `#CSP`, `#security`, `#web development`, `#sandbox`, `#iframe`

---

<a id="item-6"></a>
## [Fragnesia：Linux 内核新本地提权漏洞](https://lwn.net/Articles/1072647/) ⭐️ 8.0/10

新发现了一个名为 Fragnesia 的本地提权漏洞，影响 Linux 内核的 XFRM ESP 子系统。该漏洞无需竞态条件即可实现向只读文件内核页缓存的任意字节写入。 该漏洞构成严重安全风险，允许非特权用户在受影响的 Linux 系统上提升至 root 权限。它属于与近期披露的 Dirty Frag 漏洞相同的类别，扩大了攻击面。 该漏洞利用无需竞态条件，且概念验证代码已公开。补丁已提出但尚未合并到 Linus Torvalds 的主线或任何稳定内核分支。

rss · LWN.net · May 13, 15:26

**背景**: Linux 内核中的 XFRM（转换）子系统负责处理 IPsec 数据包的转换，包括加密和认证。ESP（封装安全载荷）是 IPsec 中的一种协议，提供机密性和数据完整性。Fragnesia 是 ESP-over-TCP 处理代码中的一个逻辑漏洞，允许对只读文件页缓存进行任意写入，从而实现权限提升。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.cilium.io/en/latest/reference-guides/xfrm/index.html">XFRM Reference Guide — Cilium 1.20.0-dev documentation</a></li>
<li><a href="https://en.wikipedia.org/wiki/IPsec">IPsec - Wikipedia</a></li>
<li><a href="https://www.tenable.com/blog/dirty-frag-cve-2026-43284-cve-2026-43500-frequently-asked-questions-linux-kernel-lpe">Dirty Frag (CVE-2026-43284,CVE-2026-43500): Linux Kernel ...</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#security`, `#vulnerability`, `#LPE`, `#privilege escalation`

---

<a id="item-7"></a>
## [重新审视 mshare：Linux 共享内存的页表共享](https://lwn.net/Articles/1072333/) ⭐️ 8.0/10

在 2026 年 LSFMM+BPF 峰会上，Anthony Yznaga 展示了更新的 mshare 补丁集，引入了一套基于系统调用的新 API（如 mshare_create、mshare_attach 等），用于在共享内存的无关进程之间共享页表，取代了之前基于 msharefs 文件系统的方法。 这项工作直接解决了页表开销可能超过共享内存本身的可扩展性问题，影响数据库和虚拟化等工作负载。如果合并，mshare 将大幅减少内存消耗并提升 Linux 中多进程共享内存应用的性能。 新 API 包括返回文件描述符的 mshare_create()，通过 ftruncate()设置区域大小，以及 mshare_attach()映射区域。其他调用如 mshare_map()、mshare_advise()和 mshare_protect()处理映射、建议和保护更改。

rss · LWN.net · May 13, 13:19

**背景**: 在 Linux 中，共享内存的进程各自维护自己的页表副本，当许多进程共享大区域时会导致显著开销。页表是 CPU 用于将虚拟地址转换为物理地址的数据结构。mshare 旨在允许无关进程共享同一物理内存的单一页表集，减少重复和内存压力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lwn.net/Articles/895217/">Sharing page tables with mshare () - LWN.net</a></li>
<li><a href="https://blogs.oracle.com/linux/mshare">Introduction to mshare | linux - Oracle Blogs</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#memory management`, `#page tables`, `#mshare`, `#LSFMM+BPF`

---

<a id="item-8"></a>
## [德国主权技术基金向 KDE 投资超 100 万欧元](https://lwn.net/Articles/1072565/) ⭐️ 8.0/10

主权技术基金向 KDE 项目授予超过 100 万欧元，用于加强其核心基础设施（包括 Plasma、KDE Linux 和通信框架）的安全性和可靠性。 德国政府支持基金的这笔重大投资凸显了开源桌面环境作为关键数字基础设施日益受到认可，将通过改善安全性和稳定性直接惠及全球数百万 KDE 用户。 这笔投资将专注于 KDE 核心组件的结构性改进，例如 Plasma 桌面、KDE Linux（基于 Arch 的不可变发行版）以及通信服务的基础框架。

rss · LWN.net · May 13, 13:09

**背景**: 主权技术基金（STF）是德国联邦经济事务和气候行动部下属的公共倡议，旨在资助关键开源软件基础设施的维护、开发和安全性。KDE 是最大的自由桌面环境项目之一，为 Linux 及其他类 Unix 系统提供图形界面。KDE Linux 是一个目前处于 alpha 阶段的不可变发行版，使用 Arch Linux 软件包并通过 Flatpak 分发应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Sovereign_Tech_Fund">Sovereign Tech Fund</a></li>
<li><a href="https://en.wikipedia.org/wiki/KDE_Linux">KDE Linux</a></li>

</ul>
</details>

**标签**: `#KDE`, `#open source`, `#funding`, `#desktop environment`, `#security`

---

<a id="item-9"></a>
## [谷歌关闭免费搜索，Cloudflare 拦截 AI 爬虫：社区寻找替代方案](https://www.reddit.com/r/LocalLLaMA/comments/1tcaboi/websearch_is_coming_to_a_screeching_performance/) ⭐️ 8.0/10

谷歌将其免费搜索层级限制为仅 50 个域名用于站内查询，并计划于 2027 年 1 月 1 日前完全关闭，高级搜索暂无公开定价。Cloudflare 现已默认拦截所有 AI 爬虫对其网络的数据抓取，最近还与 GoDaddy 达成合作覆盖其域名。 这些变化威胁到 AI 模型训练和运行所需的网络数据获取，尤其依赖实时网络抓取的本地模型。社区可能需转向去中心化搜索替代方案，这将重塑开源 AI 生态。 谷歌免费搜索索引的限制和关闭时间表影响站点特定搜索，而 Cloudflare 默认拦截 AI 爬虫波及大量网站。社区讨论中提到现有替代方案如 YaCy、SearXNG、Brave Search API 和 Common Crawl。

reddit · r/LocalLLaMA · NetTechMan · May 13, 19:35

**背景**: 网络爬虫对于训练大语言模型和为 AI 系统提供实时信息至关重要。谷歌的免费搜索 API 一直是关键资源，而 Cloudflare 保护大量网站免受不必要的流量。这些变化造成了一个缺口，去中心化或开源搜索项目可能填补。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.cloudflare.com/declaring-your-aindependence-block-ai-bots-scrapers-and-crawlers-with-a-single-click/">Declare your AIndependence: block AI bots , scrapers and crawlers...</a></li>
<li><a href="https://sproutscape.io/is-your-website-invisible-to-ai-search-cloudflares-new-default-could-be-blocking-you/">Cloudflare AI Bot Blocking – Make Sure Your Website Ranks in AI ...</a></li>
<li><a href="https://www.zdnet.com/article/google-search-alternatives-no-ai/">Sick of AI in Search ? These 7 Google alternatives still put... | ZDNET</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区普遍认为这些变化标志着搜索付费墙和对机器人流量进行货币化的趋势。许多人主张使用 YaCy 和 P2P 网络等去中心化替代方案，也有人建议一次性抓取数据并通过 P2P 共享，或最终采用微支付以消除广告。

**标签**: `#web scraping`, `#AI`, `#search engines`, `#decentralization`, `#Cloudflare`

---

<a id="item-10"></a>
## [DramaBox：基于 LTX 2.3 的开源 expressive 语音模型](https://v.redd.it/5zdi52w4rx0h1) ⭐️ 8.0/10

Resemble AI 发布了 DramaBox，这是一个基于 LTX-2.3 的开源 expressive 文本转语音模型。它能够通过单一提示生成高度 expressive 的语音表现，包括情绪、笑声、叹息和呼吸。 这一开源发布使先进的 expressive 文本转语音技术对开发者和研究人员更易获取，可用于独立游戏开发、为无障碍目的进行声音克隆以及创意内容制作。它代表了让 AI 语音听起来更自然、更像人类的一步。 DramaBox 在 LTX-2.3 音频分支上训练，遵循 LTX-2 社区许可证，并支持声音克隆。但一些用户报告说，虽然 expressive 性很高，但音频质量仍可能听起来机械或低沉。

reddit · r/LocalLLaMA · manmaynakhashi · May 13, 17:06 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1tc5wx1/dramabox_most_expressive_voice_model_ever_based/)

**背景**: LTX-2.3 是 Lightricks 开发的一款 AI 视频模型，包含音频生成能力以进行音视频联合生成。文本转语音（TTS）将文本转换为语音，而 expressive TTS 则添加情绪和韵律变化以使其更自然。Resemble AI 在 LTX-2.3 的音频组件之上构建了 DramaBox，以增强表 expressive。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/resemble-ai/DramaBox">GitHub - resemble-ai/DramaBox: super expressive prompting model based on ltx2.3 · GitHub</a></li>
<li><a href="https://www.resemble.ai/learn/models/dramabox">DramaBox: Expressive Text to Speech Model | Resemble AI</a></li>
<li><a href="https://ltx.io/model/ltx-2-3">LTX-2.3: Introducing LTX's Latest AI Video Model | LTX Model</a></li>

</ul>
</details>

**社区讨论**: 社区评论总体正面，赞扬其开源发布以及用于独立游戏和声音克隆的潜力。然而，一些用户指出，尽管 expressive 性很高，但音频质量仍显得机械或保真度低，如同“隔着管道说话”。还有人询问商业化用途及特定应用场景。

**标签**: `#TTS`, `#voice synthesis`, `#open-source`, `#expressive voice`, `#AI`

---

<a id="item-11"></a>
## [三星工会罢工致芯片产出骤降，供应链面临风险](https://t.me/zaihuapd/41355) ⭐️ 8.0/10

三星电子最大工会报告称，因大批员工离岗参与加薪抗议集会，周四夜班期间，其代工芯片和存储芯片产出分别大幅下降 58%和 18%。工会威胁称，若加薪和取消奖金上限的诉求得不到满足，将从 5 月 21 日起举行为期 18 天的全面罢工。 此次抗议可能扰乱全球半导体供应链，因为三星是领先的存储芯片制造商和重要的代工厂商。全面罢工可能严重冲击依赖三星芯片的行业，包括人工智能、汽车和消费电子。 产量下降发生在周四晚上 10 点至周五早上 6 点的夜班期间，代工芯片下降 58%，存储芯片下降 18%。从 5 月 21 日起可能举行的 18 天全面罢工将是三星电子首次全面罢工，将影响其在韩国和全球的业务。

telegram · zaihuapd · May 13, 01:11

**背景**: 三星电子是全球最大的存储芯片制造商和顶级代工厂商，与台积电（TSMC）竞争。该工会代表约 28,000 名工人，要求提高基本工资并取消绩效奖金上限。此前谈判破裂，导致此次抗议。代工芯片是为特斯拉等客户定制的，而存储芯片用于各种设备。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.sammobile.com/news/samsung-bags-massive-16-5-billion-deal-make-2nm-ai-chips-tesla/">Samsung bags massive $16.5 billion deal to make 2nm AI chips for...</a></li>
<li><a href="https://www.reuters.com/technology/samsung-raises-non-memory-chip-investment-target-skorea-announces-bigger-tax-2021-05-13/">Samsung boosts non-memory chip investment to $151 bln as</a></li>

</ul>
</details>

**标签**: `#semiconductors`, `#labor dispute`, `#Samsung`, `#supply chain`, `#chip production`

---

<a id="item-12"></a>
## [小米开源 OneVL：自动驾驶一步潜空间推理框架](https://mp.weixin.qq.com/s/7po3r6YtmuXm8Xny1bw61Q) ⭐️ 8.0/10

小米开源了 OneVL，这是一种一步式潜空间推理框架，首次将视觉-语言-行动（VLA）模型与世界模型统一到自动驾驶中，在包括 NAVSIM 在内的多项基准上达到最先进性能，PDM 得分为 88.84。 这是首个将 VLA 与世界模型统一到单步潜推理范式中的框架，性能超越显式自回归思维链方法，同时延迟降低超过 94%，对实时自动驾驶系统具有重要影响。 OneVL 采用潜空间思维链，用视觉潜令牌编码物理因果关系、语言潜令牌编码驾驶意图，推理时移除双辅助解码器。其 MLP 回归头变体延迟仅为 0.24 秒，是典型 VLA 自回归推理的 5.4%。

telegram · zaihuapd · May 13, 10:33

**背景**: 视觉-语言-行动（VLA）模型整合视觉感知和语言推理以生成驾驶动作，世界模型则通过模拟未来场景进行规划。传统方法通常以多步自回归方式结合两者，计算成本高。OneVL 的潜空间推理将两个过程压缩为单次前向传播，实现高效的实时运行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2501.11260">[2501.11260] A Survey of World Models for Autonomous Driving The Waymo World Model: A New Frontier For Autonomous Driving ... Awesome World Models for Autonomous Driving - GitHub DriveDreamer: Towards Real-world-driven World Models for ... Research on World Models for Connected Automated Driving ... [PDF] A Survey of World Models for Autonomous Driving ... World models for autonomous driving</a></li>
<li><a href="https://github.com/LMD0311/Awesome-World-Model">Awesome World Models for Autonomous Driving - GitHub DriveDreamer: Towards Real-world-driven World Models for ... Research on World Models for Connected Automated Driving ... [PDF] A Survey of World Models for Autonomous Driving ... World models for autonomous driving</a></li>
<li><a href="https://arxiv.org/abs/2509.25239">[2509.25239] A Formal Comparison Between Chain of Thought and</a></li>

</ul>
</details>

**标签**: `#VLA`, `#autonomous driving`, `#latent space reasoning`, `#world model`, `#Xiaomi`

---