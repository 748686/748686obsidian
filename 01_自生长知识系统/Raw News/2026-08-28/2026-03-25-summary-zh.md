---
layout: default
title: "Horizon Summary: 2026-03-25 (ZH)"
date: 2026-03-25
lang: zh
---

> From 45 items, 19 important content pieces were selected

---

1. [LiteLLM PyPI 版本 1.82.7 和 1.82.8 被恶意代码入侵](#item-1) ⭐️ 9.0/10
2. [LiteLLM 1.82.8 中的恶意 litellm_init.pth 文件在安装时窃取凭证](#item-2) ⭐️ 9.0/10
3. [LiteLLM 1.82.7 和 1.82.8 版本通过恶意 .pth 文件漏洞被入侵](#item-3) ⭐️ 9.0/10
4. [Wine 11 通过内核级重写大幅提升 Linux 运行 Windows 游戏的速度](#item-4) ⭐️ 8.0/10
5. [专家权重流式加载技术让万亿参数 MoE 模型在消费级硬件上运行成为可能](#item-5) ⭐️ 8.0/10
6. [美国联邦通信委员会以安全风险为由全面禁止外国制造的新型消费级路由器](#item-6) ⭐️ 8.0/10
7. [英伟达利用现金储备投资 AI 初创公司，引发反垄断担忧](#item-7) ⭐️ 8.0/10
8. [阿里达摩院发布玄铁 C950 RISC-V CPU，刷新全球性能纪录](#item-8) ⭐️ 8.0/10
9. [我国日均词元调用量两年增长超千倍，今年 3 月突破 140 万亿](#item-9) ⭐️ 8.0/10
10. [DarkSword iOS 漏洞链披露：通过 Safari 恶意网页感染，已在多国被利用](#item-10) ⭐️ 8.0/10
11. [Google 推出基于 Gemini 的暗网情报 AI 代理，已开放预览](#item-11) ⭐️ 8.0/10
12. [苹果推出 Apple Business，一个面向各种规模企业的全合一平台。](#item-12) ⭐️ 7.0/10
13. [OpenAI 关闭其 Sora AI 视频生成应用。](#item-13) ⭐️ 7.0/10
14. [包管理器实施依赖冷却期以应对供应链攻击](#item-14) ⭐️ 7.0/10
15. [PHP 提议用 BSD 三条款许可证替换双重许可证，社区投票开放至 2026 年 4 月 4 日。](#item-15) ⭐️ 7.0/10
16. [Chris Down 澄清 Linux 内核 zswap 与 zram 子系统的常见误解](#item-16) ⭐️ 7.0/10
17. [LM Studio 恶意软件恐慌确认为 Windows Defender 误报](#item-17) ⭐️ 7.0/10
18. [SillyTavern 扩展利用本地 AI 模型为任意游戏中的 NPC 注入生命](#item-18) ⭐️ 7.0/10
19. [OpenCode 源代码审计揭示 7 个外部域名连接与隐私问题](#item-19) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [LiteLLM PyPI 版本 1.82.7 和 1.82.8 被恶意代码入侵](https://github.com/BerriAI/litellm/issues/24512) ⭐️ 9.0/10

PyPI 上的 LiteLLM Python 包版本 1.82.7 和 1.82.8 被发现包含恶意代码，该代码执行了 forkbomb 攻击，导致系统内存耗尽。维护者确认入侵源于其 CI/CD 管道中使用 trivy 工具的漏洞，PyPI 已隔离受影响的包。 这一事件突显了广泛使用的 AI/ML 库中关键供应链漏洞，可能影响数百万次下载，使用户面临凭证窃取和拒绝服务攻击的风险。它强调了在开源生态系统中改进安全实践的紧迫性，特别是对于支撑现代 AI 应用的依赖项。 恶意代码以 base64 编码形式添加到 proxy_server.py 中，解码并执行另一个文件，导致 forkbomb 迅速消耗系统资源。此次攻击与 TeamPCP 黑客组织持续的供应链活动有关，虽然代理 Docker 版本因固定依赖而未受影响，但 PyPI 包的下载量已超过 9500 万次。

hackernews · dot_treo · Mar 24, 12:06

**背景**: LiteLLM 是一个流行的 Python 库，为调用 OpenAI 和 Anthropic 等提供商的各种大语言模型（LLM）提供统一接口。PyPI（Python 包索引）是 Python 包的官方存储库，开发者在此发布和安装软件依赖项。供应链攻击涉及入侵受信任的软件源以分发恶意软件，通常针对广泛使用的包以最大化影响。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.bleepingcomputer.com/news/security/popular-litellm-pypi-package-compromised-in-teampcp-supply-chain-attack/">Popular LiteLLM PyPI package compromised in TeamPCP supply ...</a></li>
<li><a href="https://github.com/BerriAI/litellm/issues/24512">LiteLLM Python package compromised by supply-chain attack</a></li>

</ul>
</details>

**社区讨论**: 社区讨论包括维护者详细说明 CI/CD 漏洞、呼吁在开发环境中实现更好的沙箱和隔离，以及像 canary 这样的工具用于检测未经授权的包访问。整体情绪反映了对依赖信任的担忧以及在软件供应链中需要更强大安全措施的需求。

**标签**: `#security`, `#ai-ml`, `#python`, `#supply-chain`, `#devops`

---

<a id="item-2"></a>
## [LiteLLM 1.82.8 中的恶意 litellm_init.pth 文件在安装时窃取凭证](https://simonwillison.net/2026/Mar/24/malicious-litellm/#atom-everything) ⭐️ 9.0/10

PyPI 上的 LiteLLM v1.82.8 软件包被植入了一个隐藏在 litellm_init.pth 文件中的凭证窃取器，该文件在安装时自动执行，无需导入软件包。PyPI 已隔离该软件包，将暴露时间窗口限制在几小时内。 这一事件是一次严重的供应链攻击，直接影响 AI/ML 社区，因为 LiteLLM 被广泛用于管理大型语言模型 API。它暴露了软件分发平台的关键漏洞，并强调了在开源生态系统中加强安全措施的必要性。 恶意文件通过扫描用户目录，针对广泛的敏感数据，包括 SSH 密钥、AWS 凭证和加密货币钱包。此次攻击与之前 Trivy 安全扫描器的漏洞有关，该漏洞可能导致 PyPI 凭证被盗，用于上传恶意软件包。

rss · Simon Willison · Mar 24, 15:07

**背景**: LiteLLM 是一个开源 Python 库，通过提供统一的 API 来简化与各种大型语言模型的交互。PyPI（Python 包索引）是 Python 软件包的官方仓库，开发者在此发布和分发软件。供应链攻击涉及在软件源头或分发点进行破坏，以感染下游用户，通常通过恶意更新或依赖项实现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/BerriAI/litellm/issues/24512">[Security]: CRITICAL: Malicious litellm_init.pth in litellm 1 ...</a></li>
<li><a href="https://futuresearch.ai/blog/litellm-pypi-supply-chain-attack/">Supply Chain Attack in litellm 1.82.8 on PyPI</a></li>
<li><a href="https://www.microsoft.com/en-us/security/blog/threat-intelligence/supply-chain-attacks/">Supply chain attacks | Latest Threats | Microsoft Security Blog</a></li>

</ul>
</details>

**标签**: `#security`, `#supply-chain-attack`, `#ai-ml`, `#python`, `#pypi`

---

<a id="item-3"></a>
## [LiteLLM 1.82.7 和 1.82.8 版本通过恶意 .pth 文件漏洞被入侵](https://www.reddit.com/r/LocalLLaMA/comments/1s2fch0/developing_situation_litellm_compromised/) ⭐️ 9.0/10

LiteLLM Python 库的 1.82.7 和 1.82.8 版本通过恶意 .pth 文件漏洞被入侵，该漏洞会在 Python 解释器启动时自动执行窃取凭证的代码。这一安全漏洞已在 GitHub issue 中报告，影响了从 PyPI 安装这些特定版本的用户。 这一事件构成了严重的安全风险，因为 LiteLLM 被广泛用于在生产 AI/ML 系统中访问超过 100 个 LLM API，可能暴露敏感凭证并引发供应链攻击。.pth 文件漏洞的隐蔽性绕过了标准安全检查，使得受影响的用户必须立即进行凭证轮换和版本降级。 受感染包中的恶意文件 'litellm_init.pth'（34,628 字节）会在 Python 解释器启动时自动执行，无需导入 LiteLLM，因此对标准代码审查不可见。根据社区验证，仅 1.82.7 和 1.82.8 版本确认受影响，较早版本如 1.82.6 和 1.82.3 仍安全。

reddit · r/LocalLLaMA · OrganizationWinter99 · Mar 24, 14:28

**背景**: LiteLLM 是一个开源 Python 库，提供统一接口，使用 OpenAI API 格式调用来自 OpenAI、Anthropic 和 Azure 等提供商的超过 100 个大语言模型（LLM）。.pth 文件是 Python 路径配置文件，可以在 Python 解释器启动时自动执行任意代码，这是 Python 问题跟踪器中记录的一个已知安全风险。该库由 BerriAI 开发，可在 PyPI 上获取，其中 1.82.7 和 1.82.8 版本是受感染的发布版本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/BerriAI/litellm/issues/24512">[Security]: CRITICAL: Malicious litellm_init.pth in litellm 1.82.8 — credential stealer · Issue #24512 · BerriAI/litellm</a></li>
<li><a href="https://github.com/python/cpython/issues/113659">Security risk of hidden pth files · Issue #113659 · python/cpython</a></li>
<li><a href="https://docs.litellm.ai/docs/">Getting Started | liteLLM</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调了 .pth 文件漏洞的隐蔽性，指出它绕过了基于导入的检测，并使得受影响系统必须进行凭证轮换。用户讨论了实用的缓解措施，如使用 Docker 进行隔离、检查其 LiteLLM 版本，并表达了对依赖 LiteLLM 的其他工具可能遭受供应链攻击的担忧。讨论氛围紧迫且具有教育意义，许多人分享了技术见解和对安全版本的验证。

**标签**: `#security`, `#AI/ML`, `#software-engineering`, `#open-source`, `#incident-response`

---

<a id="item-4"></a>
## [Wine 11 通过内核级重写大幅提升 Linux 运行 Windows 游戏的速度](https://www.xda-developers.com/wine-11-rewrites-linux-runs-windows-games-speed-gains/) ⭐️ 8.0/10

Wine 11 已发布，通过内核级重写显著提升了在 Linux 上运行 Windows 游戏的性能，基准测试显示《尘埃 3》的帧率从 110.6 提升至 860.7，《生化危机 2》等游戏也实现了类似的巨大性能提升。 这代表了兼容层技术的重大进步，可能显著改善 Linux 游戏体验，使 Linux 成为依赖 Windows 独占游戏的玩家更可行的平台，并加强开源游戏生态系统。 基准测试中显示的极端性能提升是将 Wine 11 与未启用 fsync 的原始 Wine 进行比较的结果，而已在使用 fsync 的用户将看到更温和的改进；ntsync 实现提供了最显著的加速效果，但可能不会对所有游戏产生同等影响。

hackernews · felineflock · Mar 24, 18:34

**背景**: Wine 是一个兼容层，允许 Windows 应用程序和游戏在 Linux 等类 Unix 操作系统上运行，无需模拟或虚拟化，而是将 Windows API 调用转换为 POSIX 调用。该项目通过数十年来对 Windows 文档化和未文档化行为的逆向工程而开发。Valve 基于 Wine 构建的 Proton 通过 Steam 平台在将 Windows 游戏引入 Linux 方面发挥了关键作用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wine_(software)">Wine (software) - Wikipedia</a></li>
<li><a href="https://wiki.archlinux.org/title/Wine">Wine - ArchWiki</a></li>
<li><a href="https://en.wikipedia.org/wiki/Windows_API">Windows API - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区成员表达了对 Wine 技术成就的赞赏，同时指出基准测试比较可能夸大了已在使用 fsync 等性能优化用户的真实收益。一些人强调了 Valve 对该项目的资金贡献，另一些人则讨论了底层 Windows 兼容性工作涉及的技术复杂性。

**标签**: `#Wine`, `#Linux Gaming`, `#Compatibility Layer`, `#Performance Optimization`, `#Open Source`

---

<a id="item-5"></a>
## [专家权重流式加载技术让万亿参数 MoE 模型在消费级硬件上运行成为可能](https://simonwillison.net/2026/Mar/24/streaming-experts/#atom-everything) ⭐️ 8.0/10

开发者们展示了通过从存储设备流式加载专家权重，可以在内存有限的消费级硬件上运行大规模混合专家模型，包括在 MacBook Pro 上运行 1 万亿参数的 Kimi K2.5 模型和在 iPhone 上运行 397B 参数的 Qwen3.5 模型。这些实验进展迅速，性能从最初的测试提升到新实现中达到约每秒 1.7 个 token。 这一突破显著降低了在本地运行最先进大语言模型的门槛，使得边缘 AI 应用成为可能，并让更多人无需昂贵云基础设施即可使用先进 AI 技术。它可能加速设备端 AI 助手、隐私保护工具以及跨行业更高效模型部署的发展。 Kimi K2.5 模型拥有 1 万亿总参数，但每次仅激活 32B 权重，在配备 96GB RAM 的 M2 Max MacBook Pro 上运行，而 Qwen3.5-397B-A17B 模型在 iPhone 上达到每秒 0.6 个 token。这些实现依赖于为每个 token 从 SSD 流式加载必要的专家权重，通过条件计算绕过内存限制。

rss · Simon Willison · Mar 24, 05:09

**背景**: 混合专家模型是一种大语言模型，它使用条件计算为每个输入仅激活一部分'专家'神经网络，使其比密集模型更高效。专家权重流式加载是指在推理过程中从 SSD 等存储设备加载这些激活的权重，而不是将整个模型保留在 RAM 中，从而降低内存需求。该技术建立在稀疏模型架构基础上，例如 Mistral AI 的 Mixtral 8x7B 和阿里巴巴的 Qwen3.5 系列所使用的架构。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ibm.com/think/topics/mixture-of-experts">What is mixture of experts? | IBM</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>
<li><a href="https://mistral.ai/news/mixtral-of-experts">Mixtral of experts | Mistral AI</a></li>

</ul>
</details>

**标签**: `#Mixture-of-Experts`, `#LLM Optimization`, `#Hardware Efficiency`, `#Streaming Inference`, `#Edge AI`

---

<a id="item-6"></a>
## [美国联邦通信委员会以安全风险为由全面禁止外国制造的新型消费级路由器](https://www.bloomberg.com/news/articles/2026-03-23/fcc-bans-all-foreign-made-routers-citing-security-risks?embedded-checkout=true) ⭐️ 8.0/10

美国联邦通信委员会（FCC）正式宣布，出于对网络安全和供应链漏洞的担忧，全面禁止所有在外国制造的新型消费级路由器进口至美国市场。该禁令遵循'新老划断'原则，仅针对未获认证的新型号，已在使用或先前已获批准的现有设备不受影响。 这项政策对全球硬件供应链和电信设备市场产生重大影响，可能重塑网络设备的制造和贸易模式。它反映了美国政府对外国制造技术构成网络安全威胁的日益担忧，可能导致其他国家采取类似的监管行动。 外国生产的家用网络设备已被列入 FCC 的'受管辖实体名单'，制造商必须获得设备授权才能在美国销售。虽然可以申请豁免，但必须通过向美国国防部等机构提交申请并获得批准，这表明了严格的安全审查流程。

telegram · zaihuapd · Mar 24, 01:17

**背景**: 美国联邦通信委员会（FCC）是一个独立的美国政府机构，负责监管州际和国际通信。FCC 的'受管辖实体名单'用于识别被认为对国家安全构成不可接受风险的通信设备和服务。消费级路由器是基本的网络设备，用于在家庭和小型企业中引导网络和设备之间的互联网流量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Federal_Communications_Commission">Federal Communications Commission - Wikipedia</a></li>
<li><a href="https://t.me/s/zaihuapd/40474">科技圈 在花频道– Telegram</a></li>

</ul>
</details>

**标签**: `#Cybersecurity`, `#Regulation`, `#Hardware`, `#Supply Chain`, `#Telecommunications`

---

<a id="item-7"></a>
## [英伟达利用现金储备投资 AI 初创公司，引发反垄断担忧](https://www.wsj.com/tech/nvidia-ai-market-competition-9db60e4c) ⭐️ 8.0/10

自 2022 年以来，英伟达已向 OpenAI、CoreWeave 和 Reflection 等 AI 初创公司投资数十亿美元，通过供应商、投资者和债权人的多重身份将客户锁定在其生态系统中。该公司还与芯片初创公司 Groq 达成 200 亿美元的授权协议并挖走其核心团队，美国参议员已致函质疑此类交易是否旨在规避反垄断审查。 这一策略可能通过增加客户转向 AMD 等竞争对手的难度，巩固英伟达在 AI 硬件市场的统治地位，从而抑制创新和竞争。日益增长的监管审查反映了对科技巨头利用金融力量控制新兴产业的广泛担忧。 这些投资覆盖了 AI 产业链的多个环节，从云基础设施（CoreWeave）到前沿 AI 研究（Reflection）。与 Groq 的交易被设计为非排他性授权协议而非直接收购，这可能有助于规避监管障碍，同时仍能获取关键技术和人才。

telegram · zaihuapd · Mar 24, 03:02

**背景**: 由于 AI 热潮，英伟达已成为 AI 芯片（GPU）的主要供应商，通过销售 H100 及更新的 Blackwell 架构芯片积累了巨额现金储备。CoreWeave 是一家专注于 AI 工作负载的专业云提供商，最初是一家加密货币挖矿公司。Groq 是一家以推理加速技术闻名的芯片初创公司，与英伟达的 TensorRT 和 Triton 推理平台存在竞争关系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/CoreWeave">CoreWeave - Wikipedia</a></li>
<li><a href="https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html">Nvidia buying AI chip startup Groq's assets for about $20 billion in its largest deal on record</a></li>

</ul>
</details>

**标签**: `#AI`, `#Nvidia`, `#Antitrust`, `#Investment`, `#Tech Industry`

---

<a id="item-8"></a>
## [阿里达摩院发布玄铁 C950 RISC-V CPU，刷新全球性能纪录](https://mp.weixin.qq.com/s/TTnqm8qm3Dxshj_0bxwtkw) ⭐️ 8.0/10

2026 年 3 月 24 日，在上海举办的玄铁 RISC-V 生态大会上，阿里巴巴达摩院发布了基于开源 RISC-V 架构的新一代旗舰 CPU 玄铁 C950。该芯片在 Specint2006 单核测试中得分超过 70 分，创下公开 RISC-V 处理器的性能新高，并集成了自研 AI 加速引擎，可原生运行 Qwen3、DeepSeek V3 等千亿参数级大模型。 这一突破表明 RISC-V 架构已能在高性能计算领域与 ARM、x86 等专有指令集架构竞争，有助于减少对西方芯片技术的依赖。专门针对大语言模型优化的集成 AI 加速能力，使该芯片能够满足新一代云计算、生成式人工智能、高端机器人和边缘计算等对高效 AI 推理至关重要的应用场景需求。 玄铁 C950 面向云计算、生成式人工智能、高端机器人和边缘计算等领域，达摩院表示将用于新一代高端算力场景。虽然 Specint2006 得分超过 70 分是一项重要成就，但其在实际应用中的性能表现，以及与竞争架构在完整系统实现中的对比，仍有待全面评估。

telegram · zaihuapd · Mar 24, 06:01

**背景**: RISC-V 是一种基于精简指令集计算机原则的免费开放标准指令集架构，最初于 2010 年在加州大学伯克利分校开发，现由 RISC-V International 维护。与 x86 和 ARM 等专有指令集架构不同，RISC-V 规范在宽松的开源许可下发布，无需支付版税即可实现。SPECint2006（CPU2006）是用于测试现代服务器系统 CPU 性能的标准化基准测试套件，其中 CINT2006 测量整数计算性能。Qwen3 是阿里云开发的 Qwen 系列大语言模型的最新版本，以 Apache-2.0 许可下的开放权重模型形式分发。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/RISC-V_architecture">RISC-V architecture</a></li>
<li><a href="https://en.wikipedia.org/wiki/SPECint">SPECint - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Qwen">Qwen - Wikipedia</a></li>

</ul>
</details>

**标签**: `#RISC-V`, `#CPU`, `#AI Acceleration`, `#Cloud Computing`, `#Edge Computing`

---

<a id="item-9"></a>
## [我国日均词元调用量两年增长超千倍，今年 3 月突破 140 万亿](http://paper.people.com.cn/rmrb/pc/content/202603/24/content_30147015.html) ⭐️ 8.0/10

国家数据局披露，我国日均词元调用量已在今年 3 月突破 140 万亿，从 2024 年初的 1000 亿增长到 2025 年底的 100 万亿，两年内增幅超过千倍。 这一爆发式增长表明中国人工智能发展已进入快速商业化阶段，基于词元的价值体系正在加速形成高质量数据供给链，并推动数据要素市场化配置改革。 增长轨迹呈现指数级加速，日均词元调用量在不到两年内从 1000 亿增至 100 万亿，随后在 2025 年 12 月至 2026 年 3 月的三个月内又增加了 40 万亿。

telegram · zaihuapd · Mar 24, 07:22

**背景**: 词元是大语言模型处理信息的最小单元，具有可计量、可定价、可交易的特征。自 2014 年以来，中国积极推动数据要素市场化，建立数据交易平台以创建标准化的数据资源市场。词元使用量的快速增长反映了通过基于词元的调用、分发和结算系统实现人工智能技术商业化的进程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.yicaiglobal.com/news/chinas-daily-token-usage-jumps-40-in-three-months">China's Daily Token Usage Jumps 40% in Three Months - Yicai Global</a></li>
<li><a href="https://letsdatascience.com/news/china-sees-ai-token-use-increase-1000-fold-0bd0d3e4">China Sees AI Token Use Increase 1,000-Fold | Let's Data Science</a></li>
<li><a href="https://www.sciencedirect.com/science/article/pii/S1057521925004168">Data element marketization and corporate investment efficiency</a></li>

</ul>
</details>

**标签**: `#AI`, `#Tokenization`, `#Data Market`, `#China Tech`, `#Large Language Models`

---

<a id="item-10"></a>
## [DarkSword iOS 漏洞链披露：通过 Safari 恶意网页感染，已在多国被利用](https://t.me/zaihuapd/40482) ⭐️ 8.0/10

安全研究人员披露了 DarkSword 漏洞利用链，该漏洞链通过恶意网页针对 iOS 18.4 至 18.7 版本的 Safari 浏览器，利用包括 CVE-2025-43529 在内的六个漏洞来部署 GHOSTBLADE 等恶意载荷。自 2025 年 11 月起，该漏洞已被多类攻击者用于针对沙特阿拉伯、土耳其、马来西亚和乌克兰的攻击行动，所有相关漏洞已在 iOS 26.3 中完成修补。 此次披露揭示了一个复杂的现实世界漏洞利用链，它绕过了 iOS 的安全防护，仅通过简单的网页浏览即可实现设备完全控制，影响了多个国家的用户。不同威胁行为者广泛采用该漏洞链，表明此类漏洞利用工具包能够在网络犯罪生态系统中迅速扩散，对移动设备安全构成重大风险。 该漏洞链利用了 iOS 软件栈中的六个漏洞，其中三个在发现时是零日漏洞，并且几乎完全用 JavaScript 编写以实现简化部署。值得注意的是，虽然所有漏洞都在 iOS 26.3 中修补，但其中许多实际上在更早的增量更新（如 iOS 18.7.3 和 26.2）中就已修复，这凸显了及时进行安全更新的重要性。

telegram · zaihuapd · Mar 24, 11:45

**背景**: DarkSword 是一个完整的 iOS 漏洞利用工具包，通过 Safari 漏洞针对设备实现远程代码执行。GHOSTBLADE 载荷是一个数据窃取组件，能够从受感染设备中提取敏感信息，包括加密货币钱包数据、Wi-Fi 密码、短信和聊天记录。CVE-2025-43529 是 WebKit（Safari 浏览器引擎）中的一个释放后使用漏洞，是该漏洞链中串联的六个漏洞之一。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cloud.google.com/blog/topics/threat-intelligence/darksword-ios-exploit-chain">The Proliferation of DarkSword: iOS Exploit Chain Adopted by ...</a></li>
<li><a href="https://thehackernews.com/2026/03/darksword-ios-exploit-kit-uses-6-flaws.html">DarkSword iOS Exploit Kit Uses 6 Flaws, 3 Zero-Days for Full ...</a></li>
<li><a href="https://nvd.nist.gov/vuln/detail/CVE-2025-43529">NVD - CVE - 2025 - 43529</a></li>

</ul>
</details>

**标签**: `#cybersecurity`, `#vulnerability-disclosure`, `#iOS-security`, `#Safari`, `#exploit-chain`

---

<a id="item-11"></a>
## [Google 推出基于 Gemini 的暗网情报 AI 代理，已开放预览](https://www.theregister.com/2026/03/23/google_dark_web_ai/) ⭐️ 8.0/10

Google 推出了一个基于 Gemini 的暗网情报与安全运营 AI 代理，并已接入 Google Threat Intelligence 开放预览。该服务每天分析约 800 万至 1000 万条暗网帖子，以识别初始访问中介活动、数据泄露和内部威胁等组织风险，内部测试显示准确率达 98%。 这一发布之所以重要，是因为它利用 Google 的先进 AI 技术来自动化和扩展暗网监控，通过提供近实时的威胁情报，可能提升组织的网络安全水平。这反映了 AI 驱动安全解决方案的趋势，能够处理海量数据以预先识别新兴威胁。 该 AI 代理首先为客户建立组织画像，然后筛查暗网帖子中的相关风险，专注于高容量分析并报告高准确率。目前处于公开预览阶段，表明它可能仍在开发中或会根据用户反馈进行调整。

telegram · zaihuapd · Mar 24, 13:15

**背景**: Gemini 是 Google DeepMind 开发的多模态大语言模型系列，是 LaMDA 和 PaLM 2 等模型的继任者，为包括聊天机器人在内的多种 AI 应用提供支持。暗网监控涉及持续扫描 TOR 和加密频道等隐藏互联网部分，以收集关于数据泄露和初始访问中介等网络威胁的情报，这些中介将未经授权的网络访问权出售给其他威胁行为者。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Gemini_(AI_model)">Gemini (AI model)</a></li>
<li><a href="https://www.crowdstrike.com/en-us/cybersecurity-101/threat-intelligence/dark-web-monitoring/">What is Dark Web Monitoring? [Beginner's Guide] | CrowdStrike</a></li>
<li><a href="https://en.wikipedia.org/wiki/Initial_access_broker">Initial access broker - Wikipedia</a></li>

</ul>
</details>

**标签**: `#AI`, `#Cybersecurity`, `#Dark Web`, `#Google`, `#Threat Intelligence`

---

<a id="item-12"></a>
## [苹果推出 Apple Business，一个面向各种规模企业的全合一平台。](https://www.apple.com/newsroom/2026/03/introducing-apple-business-a-new-all-in-one-platform-for-businesses-of-all-sizes/) ⭐️ 7.0/10

苹果推出了 Apple Business，这是一个面向各种规模企业的新全合一平台，提供商务邮箱、日历、带自定义域名的目录服务以及集成的 AppleCare 等功能。该公告于 2026 年 3 月在苹果新闻室发布。 此举可能对商务软件市场产生重大影响，通过提供精简的、苹果集成的解决方案，可能吸引中小型企业，潜在挑战微软 365 和 Intune 等竞争对手。这反映了苹果进军企业 IT 管理的努力，旨在简化工作流程并提升各行业的生产力。 该平台免费提供，但按用户存储升级收费，社区反馈强调了严重的可用性问题，例如有缺陷的域名锁定流程和糟糕的“自带设备”支持。此外，它还包括企业版 MacBook 预装软件以及 Apple Store 和 iCloud 的用户组等功能。

hackernews · soheilpro · Mar 24, 15:29

**背景**: Apple Business 建立在苹果现有的企业产品基础上，例如 Apple Business Manager，它帮助企业管理设备和应用。IT 管理软件常面临集成困难和可用性问题等挑战，行业报告中有提及。苹果的平台旨在通过在其生态系统（包括 iOS、iPadOS、macOS、watchOS 和 tvOS）中提供统一解决方案来解决这些问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.apple.com/business/enterprise/">Enterprise - Business - Apple</a></li>
<li><a href="https://rootcode.io/blog/ux-for-b2b-products">UX for B2B Products: Why most Enterprise Software face ...</a></li>
<li><a href="https://www.cisco.com/c/dam/en/us/products/collateral/software/top-5-enteprise-software-challenges.pdf">Solving the Top 5 Enterprise IT Infrastructure Software Management ...</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了复杂情绪，用户批评该平台流程有缺陷、可用性差以及免费定价限制改进等战略问题，而其他人则因集成功能和低成本 MacBook 看到其对小型企业的潜力。显著观点包括对域名锁定问题的沮丧以及对吸引 50 人以下新企业的赞赏。

**标签**: `#Apple`, `#Business Software`, `#IT Management`, `#Product Announcement`, `#User Experience`

---

<a id="item-13"></a>
## [OpenAI 关闭其 Sora AI 视频生成应用。](https://twitter.com/soraofficialapp/status/2036532795984715896) ⭐️ 7.0/10

OpenAI 宣布关闭其 Sora AI 视频生成应用，包括消费者应用和面向专业人士的网络服务，这一消息已得到近期新闻报道的证实。该决定于 2026 年 3 月 24 日通过 Sora 官方 X 账号的帖子公布。 此次关闭表明 AI 视频生成市场可能面临挑战，因为它引发了对此类技术可持续性和成本效益的质疑，即使是像 OpenAI 这样的领先公司也不例外。它可能通过突显 AI 开发中的战略转变和资源限制，影响用户、开发者和更广泛的行业。 此次关闭包括面向消费者的 Sora 应用和专业的网络服务，OpenAI 将高成本和向机器人技术的战略转向列为关闭原因。值得注意的是，该公告是在 OpenAI 发布 Sora 安全指南后不久发布的，这表明可能存在内部不一致或决策仓促的情况。

hackernews · mikeocool · Mar 24, 20:01

**背景**: Sora 是 OpenAI 开发的 AI 视频生成工具，允许用户根据文本提示或上传的图像创建逼真的视频，支持电影感和照片写实等多种风格。它作为 OpenAI 推进生成式 AI 技术的一部分推出，具有视频混音和可定制信息流等功能。AI 视频生成涉及合成视觉内容的算法，一直是快速发展的领域，在娱乐、教育和商业中都有应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nytimes.com/2026/03/24/technology/openai-shutting-down-sora.html">OpenAI Is Shutting Down Sora, Its A.I. Video Generator</a></li>
<li><a href="https://openai.com/sora/">Sora | OpenAI</a></li>

</ul>
</details>

**社区讨论**: 社区情绪复杂，一些用户对 Sora 的创意潜力表示怀念，但指出其新鲜感很快消失，而另一些用户则批评此次关闭是战略失误或成本问题。关键观点包括对应用缺乏持续参与度的担忧、与更广泛社交媒体平台相比的冗余性，以及对 AI 视频技术未来的怀疑。

**标签**: `#AI`, `#OpenAI`, `#Video Generation`, `#Industry News`, `#Product Shutdown`

---

<a id="item-14"></a>
## [包管理器实施依赖冷却期以应对供应链攻击](https://simonwillison.net/2026/Mar/24/package-managers-need-to-cool-down/#atom-everything) ⭐️ 7.0/10

包括 pnpm、Yarn、Bun、Deno、uv、pip 和 npm 在内的主要包管理器最近都实现了依赖冷却期功能，这些功能可将新发布包的安装延迟一段可配置的时间，通常为数天到数周。这些功能在 2025 年 9 月至 2026 年 2 月期间陆续添加，其中 pnpm 10.16 于 2025 年 9 月引入了 minimumReleaseAge 设置，而 npm 11.10.0 则在 2026 年 2 月添加了 min-release-age 功能。 这很重要，因为依赖冷却期通过创建一个缓冲期来提供对抗供应链攻击的实际防御手段，在此期间社区可以在恶意更新被广泛采用之前检测到它们。根据 Sonatype 的研究，软件供应链攻击在 2023 年增加了 200%，这些安全措施有助于保护数百万开发者和组织免受受损依赖的影响。 不同的包管理器以不同的配置实现冷却期：pnpm 使用 minimumReleaseAge 配合 minimumReleaseAgeExclude 来排除受信任的包，Yarn 具有 npmMinimalAgeGate（以分钟为单位）配合 npmPreapprovedPackages，Bun 通过 bunfig.toml 配置 minimumReleaseAge，而 pip 26.0 目前仅支持使用--uploaded-prior-to 的绝对时间戳而非相对时长。大多数工具允许对受信任的包进行豁免，并且 Seth Larson 为 pip 的限制提供了一个使用 cron 作业更新绝对日期的变通方案。

rss · Simon Willison · Mar 24, 21:11

**背景**: 依赖冷却期是一种安全措施，它在软件包发布后和可安装前创建一个等待期，为社区检测潜在的恶意更新留出时间。软件供应链攻击发生在恶意行为者破坏开发流水线中的依赖时，这种情况变得越来越普遍，2023 年攻击增加了 200%。包管理器是自动化开发项目中软件依赖的安装、更新和管理过程的工具。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.yossarian.net/2025/11/21/We-should-all-be-using-dependency-cooldowns">We should all be using dependency cooldowns</a></li>
<li><a href="https://www.techrepublic.com/article/sonatype-state-software-supply-chain-security/">Software Supply Chain Attacks Up 200%: New Sonatype Research</a></li>
<li><a href="https://pnpm.io/settings">Settings ( pnpm -workspace.yaml) | pnpm</a></li>

</ul>
</details>

**标签**: `#package-management`, `#security`, `#supply-chain-attacks`, `#software-engineering`, `#dependency-management`

---

<a id="item-15"></a>
## [PHP 提议用 BSD 三条款许可证替换双重许可证，社区投票开放至 2026 年 4 月 4 日。](https://lwn.net/Articles/1063993/) ⭐️ 7.0/10

PHP 项目在 Ben Ramsey 的带领下，提议将其当前的双重许可证（大部分代码使用 PHP v3.01，Zend 目录使用 Zend v2.0）替换为 BSD 三条款许可证，社区正在就此许可证更新 RFC 进行投票，截止日期为 2026 年 4 月 4 日。 这一变化很重要，因为它简化了 PHP 的许可证，减少了依赖 PHP 的开发者和项目的困惑，并符合开源领域向 BSD 等宽松许可证发展的趋势，这可能促进 PHP 的采用和与其他软件的集成。 该提案旨在弃用自定义的 PHP 和 Zend 许可证，转而采用 BSD 三条款许可证，后者是 OSI 批准的，并与 GPLv2 等主要 copyleft 许可证兼容，但这一变更需要通过正在进行的社区投票获得批准。

rss · LWN.net · Mar 24, 16:00

**背景**: PHP 是一种广泛用于 Web 开发的开源脚本语言，最初由 Rasmus Lerdorf 创建。自 2006 年以来，PHP 一直使用双重许可证方案：大部分代码使用 PHP v3.01，Zend Engine 目录使用 Zend v2.0，其中 Zend 许可证源于 Zend Technologies 的商业化努力。BSD 三条款许可证是一种宽松的开源许可证，允许在最小限制下自由使用、修改和分发，常用于简化许可证并提高兼容性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://wiki.php.net/rfc/php_license_update">PHP: rfc:php_license_update</a></li>
<li><a href="https://opensource.org/license/bsd-3-clause">The 3- Clause BSD License - Open Source Initiative</a></li>
<li><a href="https://fossa.com/blog/open-source-software-licenses-101-bsd-3-clause-license/">Open Source Software Licenses 101: The BSD 3- Clause License</a></li>

</ul>
</details>

**标签**: `#PHP`, `#Open Source`, `#Licensing`, `#Software Development`, `#Community Governance`

---

<a id="item-16"></a>
## [Chris Down 澄清 Linux 内核 zswap 与 zram 子系统的常见误解](https://lwn.net/Articles/1064478/) ⭐️ 7.0/10

Chris Down 发表了一篇详细分析，解释了 Linux 内核中 zswap 和 zram 子系统的根本区别，这两者常被误认为是类似的压缩交换解决方案。文章提供了关于何时使用每个子系统以优化内存管理并避免性能下降的实用指导。 这一澄清很重要，因为在内存压力下误用 zswap 或 zram 可能会恶化系统性能，影响在资源受限环境中工作的系统管理员和开发者。理解它们的区别有助于优化 Linux 系统，提高内存管理的效率和可靠性。 zswap 作为交换页面的压缩 RAM 缓存，使用 zsmalloc 进行内存池管理，而 zram 则在 RAM 中创建一个压缩块设备用于交换存储。分析强调，根据内核的内存压力处理策略，选择错误的子系统可能比完全没有交换更糟糕。

rss · LWN.net · Mar 24, 13:34

**背景**: zswap 和 zram 是 Linux 内核功能，旨在通过压缩原本会交换到磁盘的数据来提高内存效率。zswap 在 RAM 中为交换页面提供压缩缓存，而 zram 则在 RAM 中创建一个虚拟压缩块设备用于交换存储。两者都旨在减少磁盘 I/O 并提升性能，但它们在内存压力和分配方面基于不同的假设。理解这些子系统对于在 Linux 环境中进行有效的系统调优至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.kernel.org/admin-guide/mm/zswap.html">zswap — The Linux Kernel documentation</a></li>
<li><a href="https://wiki.archlinux.org/title/Zswap">zswap - ArchWiki</a></li>
<li><a href="https://en.wikipedia.org/wiki/Zram">zram - Wikipedia</a></li>

</ul>
</details>

**标签**: `#linux-kernel`, `#memory-management`, `#systems-programming`, `#performance-optimization`, `#operating-systems`

---

<a id="item-17"></a>
## [LM Studio 恶意软件恐慌确认为 Windows Defender 误报](https://i.redd.it/kmwwgv6bmzqg1.jpeg) ⭐️ 7.0/10

一位 Reddit 用户报告 Windows Defender 将 LM Studio 标记为恶意软件，但 LM Studio 开发团队调查后确认这是误报，微软迅速更新了检测规则以解决问题。该事件发生在 2024 年底，影响了包括 0.3.5 和 0.4.7 在内的多个版本。 这一事件凸显了在快速发展的本地 AI 工具生态系统中，安全警惕与误报之间的紧张关系，用户在这些工具上运行敏感模型。它展示了安全担忧如何在 AI 社区中迅速传播，以及开发团队透明回应对维护信任的重要性。 Windows Defender 具体将其标记为 'Trojan:Win32/Cinjo.O!cl'，在 VirusTotal 上 60 多个杀毒引擎中只有 1 个将其识别为恶意。事件时间恰逢最近的 LiteLLM PyPI 供应链攻击，这最初引发了担忧，但已确认无关，因为 LM Studio 不使用 LiteLLM。

reddit · r/LocalLLaMA · mooncatx3 · Mar 24, 12:39

**背景**: LM Studio 是一款流行的桌面应用程序，允许用户在本地计算机上私密运行大型语言模型（如 Llama 和 Mistral），无需依赖云端。误报是指安全软件错误地将合法文件识别为恶意软件，这可能干扰用户工作流程并削弱对软件工具的信任。Windows Defender 是微软内置的防病毒保护工具，用于扫描并清除 Windows 系统中的恶意软件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lmstudio.ai/">LM Studio</a></li>
<li><a href="https://learn.microsoft.com/en-us/troubleshoot/sharepoint/security/false-positive-malware-detections">Resolve False Positive Malware Detections ... | Microsoft Learn</a></li>

</ul>
</details>

**社区讨论**: 社区讨论最初表现出担忧和怀疑，用户分享了技术证据和个人经历，但在开发团队确认后整体情绪转向宽慰。关键观点包括对 VirusTotal 结果的分析、与以往误报的比较，以及关于供应链攻击风险的讨论，不过大多数人在证据支持下接受了误报的解释。

**标签**: `#security`, `#AI-tools`, `#false-positive`, `#community-discussion`, `#malware-detection`

---

<a id="item-18"></a>
## [SillyTavern 扩展利用本地 AI 模型为任意游戏中的 NPC 注入生命](https://v.redd.it/9ju2tp2gezqg1) ⭐️ 7.0/10

开发者创建了一个 SillyTavern 扩展，通过整合游戏维基获取背景故事、克隆游戏文件中的语音，并利用本地 AI 模型（Cydonia 用于角色扮演，Qwen 3.5 0.8B 作为游戏管理员），为任意游戏中的 NPC 实现动态交互。该系统完全在本地运行，仅需一个小型模组连接游戏与 SillyTavern 后端。 这代表了 AI 增强游戏领域的重要进展，使复杂的 NPC 交互无需云服务即可应用于任何游戏，可能彻底改变玩家体验单机和角色扮演游戏的方式。它展示了本地大语言模型在游戏中的实际应用，解决了延迟和隐私问题，同时实现了更丰富、更沉浸的叙事体验。 该系统使用 Cydonia（一个针对角色扮演优化的模型）生成叙事，并利用具有结构化输出的 Qwen 3.5 0.8B 将响应映射到游戏内动作，由于本地执行而实现了低延迟。当前限制包括需要手动整合维基和从游戏文件克隆语音，且性能取决于本地硬件能力。

reddit · r/LocalLLaMA · goodive123 · Mar 24, 12:34

**背景**: SillyTavern 是一个本地安装的用户界面，为与各种大语言模型 API 交互提供统一前端，常用于 AI 角色扮演和聊天应用。Cydonia 是 Hugging Face 等平台上可用的专业角色扮演模型，针对叙事和角色交互任务进行了优化。Qwen 3.5 0.8B 是阿里巴巴 Qwen 系列中的小型开源多模态模型，专为在消费级硬件上高效本地部署而设计。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.sillytavern.app/">What is SillyTavern? | docs.ST.app</a></li>
<li><a href="https://huggingface.co/SuperbEmphasis">SuperbEmphasis (Superb Emphasis)</a></li>
<li><a href="https://huggingface.co/Qwen/Qwen3.5-0.8B">Qwen/Qwen3.5-0.8B - Hugging Face</a></li>

</ul>
</details>

**社区讨论**: 社区评论对该项目革新游戏行业的潜力表现出高度热情，并将其与《上古卷轴 5：天际》的 Mantella 等项目进行比较。主要讨论集中在开源可用性、实时空间感知和硬件要求等实施挑战，以及在反 AI 情绪背景下游戏集成 AI 的争议。

**标签**: `#AI in Gaming`, `#Local LLM`, `#SillyTavern`, `#NPC Interaction`, `#Voice Cloning`

---

<a id="item-19"></a>
## [OpenCode 源代码审计揭示 7 个外部域名连接与隐私问题](https://www.reddit.com/r/LocalLLaMA/comments/1s2q4et/opencode_source_code_audit_7_external_domains/) ⭐️ 7.0/10

对智能编码工具 OpenCode 的详细源代码审计发现其连接到 7 个外部域名，包括 app.opencode.ai、api.opencode.ai 和 models.dev 等，其中部分连接缺乏明确的用户同意机制或禁用选项。审计还发现该工具在没有网络连接时启动会卡住，表明其对外部服务存在硬性依赖。 这很重要，因为它揭示了 AI 开发工具中'开源'声明与实际本地功能之间日益扩大的差距，对那些期望真正本地化操作的开发者构成了显著的隐私担忧。这些发现可能影响人们对类似工具的信任，这些工具虽然以本地化为卖点，却默认嵌入了遥测或外部依赖。 审计特别指出，虽然大多数外部连接都有禁用选项或用户同意机制，但实验性的 Web UI 代理目前缺少禁用标志，不过开发者计划将其打包到二进制文件中。此外，通过用户测试证实了该工具启动时对网络连接的依赖，在没有网络访问的情况下无法启动。

reddit · r/LocalLLaMA · Spotty_Weldah · Mar 24, 20:53

**背景**: OpenCode 是一款智能编码工具，利用 AI 辅助软件开发工作流，提供文本用户界面（TUI）和实验性的 Web UI。源代码审计是对应用程序源代码的系统性分析，旨在发现安全漏洞、合规性问题或隐藏功能，通常用于验证隐私和安全声明。在'本地化'AI 工具的背景下，用户通常期望极少或没有外部网络连接，以保护数据隐私并确保离线功能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.vaadata.com/blog/understanding-source-code-audit-methodology-and-process/">Source Code Audit: Understanding the Methodology & Process</a></li>
<li><a href="https://www.datacamp.com/blog/best-agentic-ide">The 13 Best Agentic IDEs in 2026 - DataCamp</a></li>
<li><a href="https://www.linuxlinks.com/100-awesome-must-have-tui-linux-apps/">100 Awesome and Must-Have TUI Linux Apps - LinuxLinks</a></li>

</ul>
</details>

**社区讨论**: 社区讨论表达了对'本地化'工具默认启用遥测这一模式的担忧，用户指出像 Mistral Vibe 这样的工具在隐私对比中表现更好。几位用户分享了解决方案，包括注重隐私的分支版本如 kilocode 和替代工具如 Code Puppy，而其他人则批评 OpenCode 启动时对网络的依赖，认为这证明它并非真正的本地工具。

**标签**: `#privacy`, `#open-source`, `#AI-tools`, `#telemetry`, `#code-audit`

---