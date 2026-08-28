---
layout: default
title: "Horizon Summary: 2026-05-08 (ZH)"
date: 2026-05-08
lang: zh
---

> From 47 items, 18 important content pieces were selected

---

1. [Dirtyfrag：通用 Linux 本地提权漏洞公开](#item-1) ⭐️ 9.0/10
2. [Anthropic 发布自然语言自动编码器用于模型可解释性](#item-2) ⭐️ 9.0/10
3. [Mozilla 用 Claude Mythos 强化 Firefox 安全](#item-3) ⭐️ 9.0/10
4. [Andrew Morton 将卸任 Linux 内存管理维护者](#item-4) ⭐️ 9.0/10
5. [Hugging Face 上的 Open-OSS/privacy-filter 恶意软件，下载量达 24.4 万](#item-5) ⭐️ 9.0/10
6. [Triton v3.7.0 发布，新增操作和后端增强](#item-6) ⭐️ 8.0/10
7. [AI 代理需要控制流，而非更多提示](#item-7) ⭐️ 8.0/10
8. [Cloudflare 裁员 20%进行战略重组](#item-8) ⭐️ 8.0/10
9. [DeepSeek 4 Flash：在 Apple Metal 上的本地推理引擎](#item-9) ⭐️ 8.0/10
10. [AI 垃圾内容正在扼杀在线社区](#item-10) ⭐️ 8.0/10
11. [Chrome 删除“设备端 AI 不向 Google 发送数据”声明](#item-11) ⭐️ 8.0/10
12. [llama.cpp 新增 MiMo V2.5 310B MoE 模型支持](#item-12) ⭐️ 8.0/10
13. [月之暗面估值突破 100 亿美元，Kimi 收入激增](#item-13) ⭐️ 8.0/10
14. [苹果研发支出 30 年来首超营收 10%，全力转向 AI](#item-14) ⭐️ 8.0/10
15. [腾讯 Hy3 preview 两周调用量达 Hy2 十倍](#item-15) ⭐️ 8.0/10
16. [Anthropic 与 SpaceX 达成 GPU 算力合作，提升 Claude 使用限制](#item-16) ⭐️ 8.0/10
17. [Google Cloud 将 reCAPTCHA 升级为 Fraud Defense，加入二维码验证](#item-17) ⭐️ 8.0/10
18. [小米开源 OmniVoice：646 语种语音克隆 TTS](#item-18) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Dirtyfrag：通用 Linux 本地提权漏洞公开](https://www.openwall.com/lists/oss-security/2026/05/07/8) ⭐️ 9.0/10

名为 Dirtyfrag 的通用 Linux 本地提权漏洞已通过公开 GitHub 仓库披露，影响所有主流发行版。该漏洞在根因上与之前的 Copy Fail 类似，利用 net/xfrm 和 RxRPC 子系统，目前尚无补丁或 CVE 编号。 该漏洞对 Linux 系统安全构成严重威胁，允许非特权用户在任意主流发行版上获得 root 权限。由于在无补丁的情况下公开，管理员必须紧急缓解风险，例如禁用受影响的内核模块或应用临时措施。 Dirtyfrag 包含两个相关子问题：一个在 xfrm-ESP 页缓存写入（与 Copy Fail 相同的数据出口），另一个在 RxRPC 协议中。研究员 Hyunwoo Kim 指出，虽然 Copy Fail 是研究动机，但 RxRPC 问题与之无关。

hackernews · flipped · May 7, 19:21 · [社区讨论](https://news.ycombinator.com/item?id=48053623)

**背景**: Linux 本地提权（LPE）漏洞允许具有有限权限的本地用户获得 root 访问权限。Copy Fail（CVE-2026-31431）是近期一个高严重性的 Linux 内核漏洞，位于加密子系统的 algif_aead 模块中。Dirtyfrag 针对 net/xfrm（IPsec）和 RxRPC（AFS 文件系统协议）子系统，两者均为可选功能，但常在发行版中默认启用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/V4bel/dirtyfrag">GitHub - V4bel/ dirtyfrag · GitHub</a></li>
<li><a href="https://stacker.news/items/1486126">dirtyfrag : Universal Linux LPE - V4bel \ stacker news</a></li>
<li><a href="https://news.lavx.hu/article/dirty-frag-linux-vulnerability-enables-root-access-across-major-distributions-no-patches-available">Dirty Frag Linux Vulnerability Enables Root Access... | LavX News</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调该漏洞与 Copy Fail 的相似性，并对内核维护者默认启用极少使用的功能表示不满。有评论者指出，Copy Fail 中 algif_aead 受到指责，但实际问题是 authencesn 模块，该模块至今未修复。

**标签**: `#linux`, `#kernel`, `#security`, `#vulnerability`, `#lpe`

---

<a id="item-2"></a>
## [Anthropic 发布自然语言自动编码器用于模型可解释性](https://www.anthropic.com/research/natural-language-autoencoders) ⭐️ 9.0/10

Anthropic 开源了自然语言自动编码器（NLA），能将模型内部激活转化为人类可读的文本，并发布了针对 Qwen 2.5（7B）、Gemma 3（12B、27B）和 Llama 3.3（70B）的权重。 这一可解释性突破使研究者能直接读取语言模型在推理时的“想法”，有助于构建更安全、更透明的 AI 系统。通过发布开放权重模型，Anthropic 赋予了更广泛社区探索专有和开源模型的能力。 NLA 方法使用“激活言词化器”生成描述特定层激活的文本，然后重建激活以验证保真度。发布的模型基于现有架构构建，可在 Hugging Face 上获取。

hackernews · instagraham · May 7, 17:54 · [社区讨论](https://news.ycombinator.com/item?id=48052537)

**背景**: 自动编码器是一种神经网络，通过学习压缩输入并重建来获取高效的数据表示。在大语言模型（LLM）中，“激活”是表示内部状态的数值向量。NLA 将自动编码器扩展到产生自然语言描述，从而使模型内部变得可解释。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/research/natural-language-autoencoders">Natural Language Autoencoders: Turning Claude’s thoughts into text</a></li>

</ul>
</details>

**社区讨论**: 社区成员赞扬了开放权重发布以及与 Hugging Face 的互动，称之为“重大新闻”。有人指出该方法依赖于特定层，并质疑在大量讨论流传的背景下如何获得干净的训练数据。专家建议阅读 Transformer Circuits 上的详细解释。

**标签**: `#interpretability`, `#LLMs`, `#autoencoders`, `#Anthropic`, `#open-source`

---

<a id="item-3"></a>
## [Mozilla 用 Claude Mythos 强化 Firefox 安全](https://simonwillison.net/2026/May/7/firefox-claude-mythos/#atom-everything) ⭐️ 9.0/10

Mozilla 利用 Claude Mythos 预览版 AI 模型在 Firefox 中查找并修复了数百个安全漏洞，每月修复数量从约 20-30 个跃升至 2026 年 4 月的 423 个。 这一突破表明 AI 辅助的漏洞检测已变得非常有效，从低质量报告转变为高信号漏洞发现，可大幅加速软件安全加固。 Mozilla 在隔离容器中运行 Claude Code 及 Mythos 预览版，提示它主动寻找漏洞；该方法发现了一个 20 年历史的 XSLT 漏洞和一个 15 年历史的 legend 元素漏洞。许多尝试被 Firefox 现有的纵深防御措施阻挡。

rss · Simon Willison · May 7, 17:56

**背景**: Claude Mythos 预览版是 Anthropic 于 2026 年向特定公司私有发布的最强大语言模型。此前，AI 生成的安全漏洞报告常被视为低质量噪音，给维护者带来成本。Mozilla 结合改进的模型能力和更好的提示与过滤技术，有效利用了 AI。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Mythos_Preview">Claude Mythos Preview</a></li>
<li><a href="https://red.anthropic.com/2026/mythos-preview/">Claude Mythos Preview \ red.anthropic.com</a></li>

</ul>
</details>

**标签**: `#AI`, `#security`, `#Firefox`, `#vulnerability detection`, `#Mozilla`

---

<a id="item-4"></a>
## [Andrew Morton 将卸任 Linux 内存管理维护者](https://lwn.net/Articles/1070994/) ⭐️ 9.0/10

2026 年 4 月 21 日，Andrew Morton 宣布计划卸任 Linux 内核内存管理子系统的维护者职务，他已担任此角色数十年。在 2026 年 LSFMM+BPF 峰会上讨论了未来维护工作，David Hildenbrand 将接管整合树。 这一交接标志着内核最关键子系统之一的领导层代际更迭，影响整个 Linux 生态系统。社区必须重组以确保持续高质量的维护和审查工作。 Morton 指出，内存管理代码高度相互关联，难以将子系统拆分为独立部分。David Hildenbrand 将负责整合树，但未来维护工作的许多细节尚未解决。

rss · LWN.net · May 7, 14:42

**背景**: 内存管理子系统负责 Linux 内核中的虚拟内存、页面分配等核心功能。Andrew Morton 自该子系统成为独立子系统之前就一直担任维护者。LSFMM+BPF 峰会是内核开发者每年讨论存储、文件系统、内存管理和 BPF 主题的会议。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lwn.net/Articles/lsfmmbpf2023/">The 2023 LSFMM+BPF Summit [LWN.net]</a></li>

</ul>
</details>

**标签**: `#linux kernel`, `#memory management`, `#maintainership`, `#open source`, `#community`

---

<a id="item-5"></a>
## [Hugging Face 上的 Open-OSS/privacy-filter 恶意软件，下载量达 24.4 万](https://www.reddit.com/r/LocalLLaMA/comments/1t6febk/warning_openossprivacyfilter_malware/) ⭐️ 9.0/10

Hugging Face 上名为 Open-OSS/privacy-filter 的虚假 AI 模型被确认为信息窃取恶意软件，使用基于 Python 的 dropper 执行恶意 PowerShell 命令并下载 Windows 可执行文件。该模型已被下载超过 24.4 万次，相关仓库已向 Hugging Face 和微软举报。 此事件凸显了在 Hugging Face 等流行平台上伪装成 AI 模型的恶意软件日益增长的威胁，可能危及大量用户的敏感数据。它强调了在开源 AI 仓库中加强安全审查的必要性。 该恶意软件针对 Windows 系统；Linux 用户不受影响。恶意负载包括一个用 Rust 编译的程序，用于从 Chrome、WinSCP 等应用程序窃取数据，并通过任务计划程序持久化。攻击链涉及多层 base64 编码的命令。

reddit · r/LocalLLaMA · charles25565 · May 7, 16:20

**背景**: 信息窃取恶意软件是一种旨在从受害者设备窃取敏感数据的恶意软件。Python dropper 通常用作初始载荷，用于下载和执行进一步的恶意软件。Tria.ge 是一个用于可疑文件行为分析的在线沙箱，提供的链接显示了该恶意软件的行为。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/infostealer-malware">Infostealer malware</a></li>
<li><a href="https://github.com/topics/dropper?l=python">dropper · GitHub Topics · GitHub</a></li>
<li><a href="https://sandbox.recordedfuture.com/docs/">Home - Triage</a></li>

</ul>
</details>

**社区讨论**: 社区对 24.4 万次下载量表示震惊，并指出明显的危险信号，例如组织名称'Open open source software'。一位用户提供了攻击链的技术细节，另一位指出点赞该模型的账户可能表明存在多个恶意活动。还有对 Linux 免疫力的讽刺以及关于 GGUF 的幽默评论。

**标签**: `#security`, `#malware`, `#huggingface`, `#AI safety`

---

<a id="item-6"></a>
## [Triton v3.7.0 发布，新增操作和后端增强](https://github.com/triton-lang/triton/releases/tag/v3.7.0) ⭐️ 8.0/10

Triton v3.7.0 新增 tl.squeeze/tl.unsqueeze 操作、缩放批次矩阵乘法、FP8 常量支持，以及包括 2CTA 模式和 TMA 多播在内的后端改进。该版本还包括 LLVM 更新、错误修复和 JIT 编译器的性能优化。 此版本增强了 Triton 在 GPU 内核开发中的表达能力和性能，直接惠及依赖 Triton 进行高性能深度学习工作负载的 AI/ML 从业者。缩放批次矩阵乘法和 FP8 常量对现代 LLM 推理和训练尤为重要。 缩放批次矩阵乘法功能支持高效地批量缩放矩阵乘法，而 FP8 常量允许在 Triton 内核中直接创建 8 位浮点常量。后端改进包括更好的 GPU 利用率的 2CTA（多 CTA）模式和 TMA（张量内存加速器）多播支持。

github · atalman · May 7, 22:19

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.pytorch.org/docs/stable/generated/torch.matmul.html">torch.matmul — PyTorch 2.11 documentation</a></li>
<li><a href="https://github.com/parca-dev/proton">GitHub - parca-dev/ proton</a></li>

</ul>
</details>

**标签**: `#triton`, `#gpu`, `#compiler`, `#deep learning`, `#release`

---

<a id="item-7"></a>
## [AI 代理需要控制流，而非更多提示](https://bsuh.bearblog.dev/agents-need-control-flow/) ⭐️ 8.0/10

文章认为，构建可靠的 AI 代理需要显式的控制流结构（如循环和条件判断），而不是仅仅依赖改进提示。这挑战了当前 AI 代理开发中主流的提示工程方法。 这一见解意义重大，因为当前 AI 代理的开发过度强调提示工程，这往往导致复杂现实任务中的不可靠行为。将重点转向控制流可以带来更健壮和确定性的代理，提升其实用价值。 文章指出，没有显式的控制流，代理在处理需要迭代或条件逻辑的任务时（例如在会话中处理多个文件）会变得困难。社区讨论建议，LLM 或许更适合用于编写确定性代码，而非在运行时处理任务。

hackernews · bsuh · May 7, 16:43 · [社区讨论](https://news.ycombinator.com/item?id=48051562)

**背景**: AI 代理是利用大型语言模型（LLM）自主执行任务的软件系统。控制流指的是单个语句、指令或函数调用被执行或求值的顺序，包括循环和条件等结构。提示工程涉及编写输入提示以引导 LLM 行为，但这种方法在处理多步骤、有状态的任务时存在局限性。

**社区讨论**: 社区强烈赞同文章的论点。一位评论者批评了“为未来模型构建”的建议，并举了一个由于缺乏控制流而失败的质量保证（QA）代理的具体例子。其他人建议 LLM 应该用于编写确定性代码，而不是在运行时处理任务，有些人幽默地指出这本质上是在重新发明编程。

**标签**: `#AI agents`, `#control flow`, `#prompt engineering`, `#LLM`, `#software design`

---

<a id="item-8"></a>
## [Cloudflare 裁员 20%进行战略重组](https://blog.cloudflare.com/building-for-the-future/) ⭐️ 8.0/10

Cloudflare 宣布裁员约 1100 人，占员工总数的 20%，这是旨在'为未来建设'的战略重组的一部分。 一家主要科技公司如此大规模的裁员凸显了长期 AI 投资与短期成本压力之间的紧张关系，影响了一千多名员工，并引发了对企业信息传递的讨论。 被裁员工将获得截至 2026 年底的全额基本工资、美国员工的年度医保，以及截至 8 月 15 日的股权归属，且悬崖条款被豁免。

hackernews · PriorityLeft · May 7, 20:23 · [社区讨论](https://news.ycombinator.com/item?id=48054423)

**背景**: Cloudflare 是一家主要的 CDN 和云安全公司。此次裁员发生在前一段快速招聘期之后，包括 2025 年 9 月的大型实习生项目。该公司和其他科技公司增加了对 AI 技术的投入，但尚未转化为同等的收入增长，因此采取了削减成本的措施。

**社区讨论**: 社区评论批评了委婉的标题，一位用户指出 2025 年招聘 1111 名实习生与现在裁员 1100 人之间的矛盾。另一名受影响的员工发帖寻找新工作。一些人猜测裁员是由于高昂的 AI 成本而没有相应的收入来抵消。

**标签**: `#cloudflare`, `#layoffs`, `#tech-industry`, `#corporate-strategy`, `#ai-economics`

---

<a id="item-9"></a>
## [DeepSeek 4 Flash：在 Apple Metal 上的本地推理引擎](https://github.com/antirez/ds4) ⭐️ 8.0/10

Antirez 发布了 DeepSeek 4 Flash（DS4），这是一个针对 DeepSeek 模型优化的本地推理引擎，利用 Apple 的 Metal API 在 Mac 硬件上实现高效设备端大语言模型推理。 该项目满足了在 Apple 硬件上进行优化本地推理的实际需求，通过专注于单一模型架构的优化，可能缩小前沿模型与开源模型之间的差距。 DS4 处理大型初始提示（例如 25k tokens）时预填充时间较长（约 4 分钟），但利用基于磁盘的 KV 缓存加速后续交互，在 M3 Max MacBook Pro 上峰值功耗为 50W。

hackernews · tamnd · May 7, 15:40 · [社区讨论](https://news.ycombinator.com/item?id=48050751)

**背景**: DeepSeek 是一家中国人工智能公司，开发大型语言模型。Apple 的 Metal API 提供底层 GPU 接口，用于 Apple 硬件上的图形和计算，从而实现高效推理。像 llama.cpp 和 ollama 这样的本地推理引擎允许在个人设备上运行大语言模型，但很少有专门针对 Apple 的 Metal 后端和 DeepSeek 模型进行优化的。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Metal_(API)">Metal (API) - Wikipedia</a></li>
<li><a href="https://www.skool.com/open-source-ai-builders-club/best-local-llm-inference-engines-in-2025-from-everyday-laptops-to-enterprise">Best Local LLM Inference Engines in 2025: From Everyday Laptops to ...</a></li>

</ul>
</details>

**社区讨论**: 社区称赞 DS4 的针对性优化和教育价值，评论者指出了迭代改进的潜力。一些人对大型输入的长预填充时间表示担忧，而作者澄清说缓存使其在常规使用中具有实用性。能效被强调为一个积极方面。

**标签**: `#deepseek`, `#local-inference`, `#metal`, `#apple`, `#llm`

---

<a id="item-10"></a>
## [AI 垃圾内容正在扼杀在线社区](https://rmoff.net/2026/05/06/ai-slop-is-killing-online-communities/) ⭐️ 8.0/10

一篇新的博客文章指出，AI 生成的内容正在淹没在线社区，破坏真实的人际互动并压垮版主。社区管理者报告称每月封禁数百个机器人账号，担心在与虚假内容的斗争中失败。 这一趋势威胁着在线社区的根本——信任与真实性，可能驱使用户离开平台。AI 的广泛采用引发了一个关键问题：如何在数字空间中维护真正的人际连接。 具体案例包括：一位用户让 LLM 代理在 Reddit 上刷分未被察觉，以及一个小众社区每月封禁 600 个 AI 内容账号。版主的工作量显著增加，小社区负担尤为沉重。

hackernews · thm · May 7, 18:46 · [社区讨论](https://news.ycombinator.com/item?id=48053203)

**背景**: AI 垃圾内容指由大型语言模型（LLM）等 AI 工具生成的低质量、常无关或误导性内容，旨在模仿人类发帖。在线社区依赖真实的互动，但机器人和自动化内容侵蚀了信任，需要人工审核。随着 AI 生成成本降低且更易获取，此类内容数量激增，威胁社区可持续性。

**社区讨论**: 社区评论者分享亲身经历：一位用户用 AI 代理在 Reddit 成功刷分，而一位社区组织者每月封禁 600 个 AI 账号并担心失败。其他人认为小规模、更封闭的社区可能是解决方案，甚至有人提出 AI 污染可能促使人类回归现实世界互动。

**标签**: `#AI`, `#online communities`, `#content moderation`, `#bots`, `#authenticity`

---

<a id="item-11"></a>
## [Chrome 删除“设备端 AI 不向 Google 发送数据”声明](https://old.reddit.com/r/chrome/comments/1t5qayz/chrome_removes_claim_of_ondevice_al_not_sending/) ⭐️ 8.0/10

谷歌 Chrome 从其设备端 AI 功能页面删除了一项声明，该声明此前声称 AI 不会向 Google 服务器发送数据，引发了隐私担忧。 这一变化破坏了用户对谷歌隐私承诺的信任，并暗示设备端 AI 可能并不像宣传的那样保护隐私，可能影响依赖其集成 AI 功能的数百万 Chrome 用户。 删除行为在 Chrome AI 创新页面上被注意到，社区成员怀疑这可能表明数据传输。谷歌的企业政策声明，数据可能被发送到谷歌以使 AI 功能正常工作，但不会用于改进模型或广告。

hackernews · newsoftheday · May 7, 15:56 · [社区讨论](https://news.ycombinator.com/item?id=48050964)

**背景**: 设备端 AI 是指在用户本地设备上运行的 AI 模型，理论上处理数据无需发送到外部服务器。Chrome 一直在引入此类功能，包括一个静默下载的 4GB AI 模型，这已经引发了隐私和同意方面的争论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.google.com/chrome/ai-innovations/">AI in Chrome: help right where you need it</a></li>
<li><a href="https://support.google.com/chrome/answer/16961953?hl=en">Manage on-device Generative AI models in Chrome - Google Chrome Help</a></li>
<li><a href="https://www.tomsguide.com/ai/check-your-storage-chrome-may-be-downloading-a-4gb-ai-model-heres-what-we-know">'No clear consent flow for this download': Google Chrome is silently stashing a 4GB AI model on your device — and Google just responded | Tom's Guide</a></li>

</ul>
</details>

**社区讨论**: Reddit 和 Hacker News 社区表达了强烈的怀疑，许多人认为 AI 功能主要用于数据收集。一些评论者认为措辞更改可能只是为了简洁，但大多数人认为这确认了数据被发送到谷歌，可能违反 GDPR。

**标签**: `#privacy`, `#Chrome`, `#AI`, `#Google`, `#data collection`

---

<a id="item-12"></a>
## [llama.cpp 新增 MiMo V2.5 310B MoE 模型支持](https://github.com/ggml-org/llama.cpp/pull/22493) ⭐️ 8.0/10

AesSedai 提交的拉取请求 (#22493) 为 llama.cpp 添加了对小米 MiMo V2.5 模型的支持，该模型是一个 310B 总参数 / 15B 激活的稀疏混合专家 (MoE) 模型，支持 1M 令牌上下文和多模态（文本、图像、视频、音频）。 这使得能够在配备 128GB 内存的消费级硬件（如 DGX Spark）上本地运行最先进的多模态 MoE 模型，从而让开发者和研究人员能够使用强大的 AI。此外，多令牌预测 (MTP) 支持也备受期待，可进一步提高生成效率。 该模型使用 729M 参数的 ViT 视觉编码器和 261M 参数的音频 Transformer 作为模态适配器，以及一个 3 层、329M 参数的 MTP 头。初始合并支持文本和图像模态，但音频和视频支持尚未包含在此拉取请求中。

reddit · r/LocalLLaMA · jacek2023 · May 7, 11:23 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1t67lvx/feat_add_mimo_v25_model_support_by_aessedai_pull/)

**背景**: 稀疏混合专家 (MoE) 是一种模型架构，只为每个输入令牌激活一部分专家子网络，从而在保持较低每令牌计算成本的同时实现更大的总参数量。多令牌预测 (MTP) 是一种训练技术，模型同时预测多个未来令牌，从而提高样本效率和生成速度。llama.cpp 是一个流行的开源项目，可在 CPU 和 GPU 上高效推理大型语言模型。小米开发的 MiMo V2.5 是一个 310B 稀疏 MoE 模型，针对多模态理解和长上下文进行了优化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Sparse_mixture-of-experts">Sparse mixture-of-experts</a></li>
<li><a href="https://arxiv.org/abs/2505.10518">[2505.10518] Multi-Token Prediction Needs Registers</a></li>

</ul>
</details>

**社区讨论**: 社区成员对在 128GB 系统上运行 MiMo V2.5 表示兴奋，一位测试者在双 GPU 设置上报告了 60 tok/s 的速度。一些用户指出缺少音频/视频支持，并且初始 GGUF 量化可能不是最优的，建议等待未来版本。一位用户报告称该模型即使在官方网页界面上也不断循环，将其称为‘有问题的模型’。

**标签**: `#llama.cpp`, `#MiMo`, `#MoE`, `#multimodal`, `#open-source`

---

<a id="item-13"></a>
## [月之暗面估值突破 100 亿美元，Kimi 收入激增](https://t.me/zaihuapd/41251) ⭐️ 8.0/10

这一里程碑突显了中国人工智能初创公司的快速扩张以及投资者（尤其是阿里巴巴和腾讯等科技巨头）的强烈信心。Kimi 收入的异常增长标志着人工智能采用率的重大转变，全球需求推动了更高的使用率和商业化。 本轮融资由阿里、腾讯、五源、九安等联合领投，月之暗面累计融资额已超 12 亿美元。Kimi 产品收入激增得益于全球付费用户和 API 调用量的增长，海外市场现已超越国内市场。

telegram · zaihuapd · May 7, 00:30

**背景**: 月之暗面是一家专注于大语言模型的中国初创公司，以其 Kimi 产品系列闻名。该公司最近发布了 Kimi K2.5，这是一个开源的、能够处理文本、代码和视觉内容的多模态模型。“十角兽”指估值达到或超过 100 亿美元的私营初创公司，这是创业界罕见的成就。新闻中还提到了 OpenRouter，这是一个统一的 API 平台，允许开发者通过单一接口访问多种 AI 模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.dugainadvisors.com/post/decacorn-hectocorn-valuations-what-s-next">Decacorn & Hectocorn Valuations: What's Next?</a></li>
<li><a href="https://www.kimi.com/ai-models/kimi-k2-5">Kimi K2.5 | Open Visual Agentic Model for Real Work</a></li>
<li><a href="https://www.codecademy.com/article/what-is-openrouter">What is OpenRouter? A Guide with Practical Examples - Codecademy</a></li>

</ul>
</details>

**标签**: `#AI`, `#startup`, `#funding`, `#LLM`, `#valuation`

---

<a id="item-14"></a>
## [苹果研发支出 30 年来首超营收 10%，全力转向 AI](https://www.cnbc.com/2026/05/06/apples-rd-spending-climbs-to-10percent-of-revenue-on-ai-investments.html) ⭐️ 8.0/10

苹果 2026 年 3 月财季研发支出占营收比例升至 10.3%，为 30 年来首次突破 10%，研发投入同比增长 34%。这标志着苹果战略转向将 AI 整合到其硬件平台，包括端侧大语言模型、私有云计算和自研 AI 芯片。 这一财务里程碑表明苹果决心在 AI 竞赛中竞争，有可能像 iPod 时代那样重塑其产品生态系统。此举可能加速生成式 AI 融入 iPhone、AirPods、AR 眼镜等日常设备，影响数百万用户和整个消费科技领域。 研发激增之际，CEO 蒂姆·库克准备于 2026 年 9 月卸任，苹果正专注于端侧 AI（约 30 亿参数模型）、通过私有云计算运行的更大服务器端模型，以及 M5 系列等自研芯片。苹果还被曝正开发 AI 眼镜和带摄像头的 AirPods。

telegram · zaihuapd · May 7, 01:00

**背景**: 苹果历史上研发支出占营收比例维持在 6-8%左右，此次突破 10%反映了重大战略转变。公司正投资端侧 AI 以在隐私方面形成差异化，并通过私有云计算安全处理复杂工作负载。M 系列等自研芯片使得 AI 能力在设备间紧密整合，这一策略此前曾推动 iPhone 的成功。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://machinelearning.apple.com/research/introducing-apple-foundation-models">Introducing Apple’s On-Device and Server Foundation Models -</a></li>
<li><a href="https://security.apple.com/blog/private-cloud-compute/">Private Cloud Compute: A new frontier for AI privacy in the cloud - Apple Security Research</a></li>
<li><a href="https://www.fastcompany.com/91047728/apple-ai-applegpt-generative-siri-m3-macbook-air-cloud-device">Apple hinted at big AI plans. Here's what AppleGPT might entail</a></li>

</ul>
</details>

**标签**: `#Apple`, `#AI`, `#R&D`, `#Hardware`, `#Strategy`

---

<a id="item-15"></a>
## [腾讯 Hy3 preview 两周调用量达 Hy2 十倍](https://finance.sina.com.cn/tech/shenji/2026-05-07/doc-inhwzrtp8521239.shtml) ⭐️ 8.0/10

腾讯混元 Hy3 preview 模型上线两周内，Token 调用总量达到前代 Hy2 的 10 倍，并在 OpenRouter 周榜总榜和市场占有率上均排名第一。 这一快速采用表明腾讯最新模型获得了强烈的市场认可，并加剧了 AI 模型领域的竞争，尤其是在 Hy3 preview 表现出色的智能体和工具调用场景中。 Hy3 preview 是一个 2950 亿参数的混合专家（MoE）模型，激活参数 210 亿，支持 256K token 上下文窗口，并集成了快思考和慢思考能力。

telegram · zaihuapd · May 7, 05:34

**背景**: Hy3 preview 是腾讯在重建的 AI 基础设施上训练的首个模型，采用混合专家（MoE）架构，每个 token 只激活部分参数以平衡性能与效率。OpenRouter 是一个通过单一 API 提供 300 多个 AI 模型访问的平台，常用于衡量模型采用情况。该模型在编程和智能体相关应用中增长显著，在腾讯 WorkBuddy、Codebuddy 等工具中的使用量增长了 16.5 倍。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/tencent/Hy3-preview">tencent/Hy3-preview · Hugging Face</a></li>
<li><a href="https://www.tencent.com/en-us/articles/2202320.html">Tencent Unveils Hy3 preview; Model Enhances Agent Capabilities and Real-World Usability - Tencent 腾讯</a></li>
<li><a href="https://github.com/Tencent-Hunyuan/Hy3-preview">GitHub - Tencent-Hunyuan/Hy3-preview: Hy3 preview (295B A21B), a leading reasoning and agent model in its size, with great cost efficiency · GitHub</a></li>

</ul>
</details>

**标签**: `#AI`, `#LLM`, `#Tencent`, `#Model Performance`, `#Industry News`

---

<a id="item-16"></a>
## [Anthropic 与 SpaceX 达成 GPU 算力合作，提升 Claude 使用限制](https://t.me/zaihuapd/41259) ⭐️ 8.0/10

Anthropic 与 SpaceX 达成合作，使用 xAI 旗下 Colossus 1 数据中心的全部算力，在一个月内获得超过 22 万块 NVIDIA GPU 和 300 兆瓦电力。由此，Claude Code 的速率限制翻倍，Pro/Max 用户的高峰期限制被取消，Claude Opus API 的速率限制也显著提升。 此次合作大幅扩充了 Anthropic 的计算资源，加快了模型训练速度，并提高了 Claude API 的吞吐量。这标志着 AI 公司与大型基础设施提供商之间的合作进一步深化，可能加速先进 AI 模型的开发。 Colossus 1 数据中心位于田纳西州孟菲斯市，创纪录地在 122 天内建成，是最大的 AI 数据中心之一，最初用于训练 xAI 的 Grok 模型。Anthropic 将使用该设施的全部算力，包括超过 22 万块 NVIDIA GPU 和 300 兆瓦容量。

telegram · zaihuapd · May 7, 08:19

**背景**: Anthropic 开发了 Claude 系列大语言模型，通过 Claude Code 等工具用于软件开发等任务。要大规模训练和提供服务，需要配备数千块 GPU 的巨型计算集群。由 SpaceX 旗下 xAI 运营的 Colossus 数据中心正好提供了这样的基础设施。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.datacenterdynamics.com/en/news/anthropic-to-use-all-of-spacex-xais-colossus-1-data-center-compute/">Anthropic to use all of SpaceX-xAI's Colossus 1 data center compute</a></li>
<li><a href="https://claude.com/product/claude-code">Claude Code by Anthropic | AI Coding Agent, Terminal, IDE</a></li>

</ul>
</details>

**标签**: `#算力合作`, `#AI基础设施`, `#NVIDIA GPU`, `#Claude`

---

<a id="item-17"></a>
## [Google Cloud 将 reCAPTCHA 升级为 Fraud Defense，加入二维码验证](https://support.google.com/recaptcha/answer/16609652?hl=en) ⭐️ 8.0/10

Google Cloud 推出了 Fraud Defense，作为 reCAPTCHA 的下一代演进，加入了二维码手机验证挑战以对抗 AI 驱动的机器人。 这标志着从传统验证码到欺诈预防平台的重大转变，对于保护代理化网络免受复杂自动化攻击至关重要。 二维码验证要求用户用手机扫描代码以证明人类身份。兼容性需要 Android Google Play Services 25.41.30+ 或 iOS 15.0+。

telegram · zaihuapd · May 7, 09:18

**背景**: reCAPTCHA 一直是 Google 广泛用于区分人类用户和机器人的服务。随着 AI 智能体的兴起，传统挑战效果减弱。Fraud Defense 扩展了 reCAPTCHA 的能力，涵盖代理化网络上的欺诈和滥用预防，并与 Cloud Armor 和 Apigee 集成以提供多层防护。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cloud.google.com/blog/products/identity-security/introducing-google-cloud-fraud-defense-the-next-evolution-of-recaptcha/">Introducing Google Cloud Fraud Defense, the next evolution of reCAPTCHA | Google Cloud Blog</a></li>
<li><a href="https://docs.cloud.google.com/recaptcha/docs">Google Cloud Fraud Defense documentation | Google Cloud Documentation</a></li>
<li><a href="https://cloud.google.com/security/products/fraud-defense">Fraud Defense | Google Cloud</a></li>

</ul>
</details>

**标签**: `#security`, `#captcha`, `#fraud prevention`, `#google cloud`, `#QR code`

---

<a id="item-18"></a>
## [小米开源 OmniVoice：646 语种语音克隆 TTS](https://mp.weixin.qq.com/s/TCS_Sd10g_rvf1cszw673A) ⭐️ 8.0/10

小米开源了 OmniVoice，这是一个支持 600 多种语言的极简双向 Transformer 架构的多语言零样本 TTS 模型，训练速度达到每天 10 万小时，PyTorch 推理速度达到 40 倍实时。 此次开源将高质量多语言语音克隆技术普及化，在 24 种语言的测试中超越商业系统，在 102 种语言中逼近真实语音，为全球开发者提供了跨语言定制、带噪适配等能力。 OmniVoice 基于 50 个开源数据集构建了 58 万小时、646 种语言的训练集，采用全码本随机掩蔽和大语言模型预训练参数来提升效率和可懂度。

telegram · zaihuapd · May 7, 10:06

**背景**: 文本转语音（TTS）是将书面文字转换为语音音频，语音克隆则是复制目标说话人的声音特征。OmniVoice 使用双向 Transformer 架构（类似 BERT）和码本表示离散音频，并利用预训练大语言模型参数来加速训练。全码本随机掩蔽是一种训练技术，在训练时随机掩蔽所有码本条目，以提升鲁棒性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/k2-fsa/OmniVoice">GitHub - k2-fsa/OmniVoice: High-Quality Voice Cloning TTS for 600+ Languages · GitHub</a></li>
<li><a href="https://huggingface.co/k2-fsa/OmniVoice">k2-fsa/OmniVoice · Hugging Face</a></li>

</ul>
</details>

**标签**: `#TTS`, `#voice cloning`, `#open-source`, `#multilingual`, `#Xiaomi`

---