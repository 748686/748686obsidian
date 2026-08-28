---
layout: default
title: "Horizon Summary: 2026-04-02 (ZH)"
date: 2026-04-02
lang: zh
---

> From 38 items, 13 important content pieces were selected

---

1. [axios npm 维护者账号遭劫持，恶意版本注入远程控制木马](#item-1) ⭐️ 9.0/10
2. [NASA“阿尔忒弥斯 2 号”载人绕月任务进入发射倒计时，时隔 50 年重返月球轨道](#item-2) ⭐️ 9.0/10
3. [Artemis II 成功发射，四名宇航员开启为期 10 天的月球任务。](#item-3) ⭐️ 8.0/10
4. [EmDash：基于 TypeScript 的无服务器 CMS，通过沙盒插件成为 WordPress 的继任者](#item-4) ⭐️ 8.0/10
5. [Bonsai 1-bit 模型在极端压缩下仍保持出色质量](#item-5) ⭐️ 8.0/10
6. [Arcee AI 发布 Trinity-Large-Thinking：3980 亿参数稀疏专家混合模型，130 亿激活参数，采用 Apache 2.0 许可证](#item-6) ⭐️ 8.0/10
7. [attn-rot KV 缓存优化技术已集成到 llama.cpp，显著提升量化效率](#item-7) ⭐️ 8.0/10
8. [四肢瘫痪者通过脑机接口植入物用意念创作音乐](#item-8) ⭐️ 8.0/10
9. [DRAM 价格上涨威胁爱好者单板计算机市场的可负担性](#item-9) ⭐️ 7.0/10
10. [研究人员在 Transformer 中用基于 RBF 的注意力机制替代点积注意力，以解决幅度偏差问题。](#item-10) ⭐️ 7.0/10
11. [TurboQuant 被应用于模型权重压缩：Qwen3.5-27B 实现接近 Q4_0 的质量，体积减小 10%](#item-11) ⭐️ 7.0/10
12. [Falcon-OCR 与 Falcon-Perception：面向 OCR 与分割任务的轻量级视觉模型](#item-12) ⭐️ 7.0/10
13. [GitHub 出现非官方仓库，通过 npm 包的 source map 还原 Claude Code 2.1.88 的 4756 个 TypeScript 文件。](#item-13) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [axios npm 维护者账号遭劫持，恶意版本注入远程控制木马](https://t.me/zaihuapd/40637) ⭐️ 9.0/10

2026 年 3 月 31 日，安全机构 StepSecurity 发现主流 JavaScript 库 axios 的 npm 维护者账号遭劫持，攻击者手动发布了恶意版本 axios@1.14.1 和 axios@0.30.4。这些版本通过注入虚假依赖 plain-crypto-js 触发恶意脚本，针对 Windows、macOS 和 Linux 系统植入远程访问木马（RAT）。 这一事件凸显了对一个拥有数百万依赖项的广泛使用库的重大供应链攻击，可能危及全球无数应用程序和系统。它暴露了 npm 账户安全漏洞以及绕过 GitHub Actions 等自动化 CI/CD 流程的风险，可能导致恶意软件广泛传播。 攻击者绕过了正常的 GitHub Actions CI/CD 流程手动发布恶意版本，通过连接到特定命令与控制服务器针对多种操作系统。虚假依赖 plain-crypto-js 在攻击前几分钟才发布，表明这是一次有组织的规避检测行为。

telegram · zaihuapd · Apr 1, 05:25

**背景**: Axios 是一个流行的 JavaScript 库，用于在 Web 和 Node.js 应用程序中发起 HTTP 请求，通常通过 npm（Node 包管理器）集成。npm 账户劫持涉及攻击者通过域名接管或社会工程等方法未经授权访问维护者账户，以发布恶意软件包。GitHub Actions 是一个自动化软件工作流程的 CI/CD 工具，绕过它可能让攻击者无需标准安全检查即可注入代码。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://socket.dev/blog/axios-npm-package-compromised">Supply Chain Attack on Axios Pulls Malicious Dependency from...</a></li>
<li><a href="https://www.endorlabs.com/learn/npm-account-takeovers-are-a-growing-malware-trend">npm Account Takeovers are a Growing Malware Trend | Blog |</a></li>
<li><a href="https://inventivehq.com/blog/github-actions-cicd-guide">GitHub Actions CI / CD : Complete Guide to Workflows, Runners, and...</a></li>

</ul>
</details>

**标签**: `#security`, `#supply-chain-attack`, `#npm`, `#javascript`, `#axios`

---

<a id="item-2"></a>
## [NASA“阿尔忒弥斯 2 号”载人绕月任务进入发射倒计时，时隔 50 年重返月球轨道](https://www.nasa.gov/) ⭐️ 9.0/10

NASA 的“阿尔忒弥斯 2 号”任务计划于 2026 年 4 月 1 日美国东部时间 18:24 从肯尼迪航天中心发射，使用太空发射系统（SLS）火箭和猎户座飞船将四名宇航员送入太空进行为期 10 天的绕月飞行。这是自 1972 年阿波罗 17 号以来，人类时隔半个多世纪首次重返月球轨道的载人任务，此前因技术故障导致发射窗口多次推迟。 这次任务标志着太空探索的历史性里程碑，在时隔五十多年后重新建立人类在月球轨道的存在，为 NASA 阿尔忒弥斯计划下的可持续月球探索铺平道路。它展示了国际社会在深空载人任务方面重新获得的能力，并为未来的月球着陆和潜在的火星任务奠定了基础。 该任务因技术问题多次推迟，包括 2026 年 2 月和 3 月测试中出现的液氢泄漏和氦气流中断，导致火箭被迫撤回装配大楼进行紧急检修。目前 SLS 火箭已屹立于发射台，预计全球超过一千万观众将通过官方频道观看这一历史时刻。

telegram · zaihuapd · Apr 1, 22:01

**背景**: 阿尔忒弥斯计划是 NASA 旨在让人类重返月球并建立可持续探索的倡议，它建立在先前计划（如星座计划）的组件基础上。太空发射系统（SLS）是 NASA 专门为阿尔忒弥斯任务设计的超重型运载火箭，能够单次发射就将猎户座飞船直接送往月球。猎户座是一种部分可重复使用的载人航天器，由洛克希德·马丁制造的乘员舱和欧洲服务舱组成，是将宇航员送往月球轨道并返回地球的主要载具。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Space_Launch_System">Space Launch System - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Orion_(spacecraft)">Orion (spacecraft) - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Artemis_program">Artemis program - Wikipedia</a></li>

</ul>
</details>

**标签**: `#space-exploration`, `#NASA`, `#Artemis-program`, `#rocket-launch`, `#lunar-mission`

---

<a id="item-3"></a>
## [Artemis II 成功发射，四名宇航员开启为期 10 天的月球任务。](https://www.theguardian.com/science/live/2026/apr/01/artemis-ii-launch-nasa-orion-moon-trip-live-updates) ⭐️ 8.0/10

Artemis II 成功发射，四名宇航员执行为期 10 天的任务，包括月球飞越和返回地球，这是 50 多年来的首次载人月球任务。该任务使用 NASA 的太空发射系统火箭和猎户座飞船，以测试深空能力。 这次任务是 NASA 阿尔忒弥斯计划的关键一步，为未来的月球着陆和最终的人类火星任务铺平道路。它展示了美国在太空探索中的重新领导地位，并推进了长期深空旅行的技术。 任务剖面包括多次地月转移注入和从月球的自由返回轨道，关键事件包括 4 月 6 日的月球飞越和 4 月 10 日的溅落。社区讨论中强调了再入过程中隔热罩安全性的担忧。

hackernews · Philpax · Apr 1, 22:38

**背景**: 阿尔忒弥斯计划是 NASA 重返月球并建立可持续存在的倡议，Artemis II 是其首次载人任务。它基于 2022 年无人测试任务 Artemis I，并使用太空发射系统（一种超重型运载火箭）和猎户座飞船，后者比阿波罗飞船更大，专为深空任务设计。该计划旨在实现未来的月球着陆和火星探索。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Artemis_II">Artemis II - Wikipedia</a></li>
<li><a href="https://www.nasa.gov/mission/artemis-ii/">Artemis II: NASA’s First Crewed Lunar Flyby in 50 Years - NASA</a></li>
<li><a href="https://en.wikipedia.org/wiki/Orion_(spacecraft)">Orion (spacecraft) - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区情绪复杂，既有对任务里程碑的兴奋和对发射速度的惊叹，也有对隔热罩安全性和未来时间表的担忧。评论强调了发射的情感反应、速度和时间表等技术细节，以及关于政府能力和项目效率的辩论。

**标签**: `#space-exploration`, `#NASA`, `#Artemis-program`, `#rocket-science`, `#aerospace`

---

<a id="item-4"></a>
## [EmDash：基于 TypeScript 的无服务器 CMS，通过沙盒插件成为 WordPress 的继任者](https://blog.cloudflare.com/emdash-wordpress/) ⭐️ 8.0/10

Cloudflare 推出了 EmDash，这是一个基于 TypeScript 的无服务器 CMS，被设计为 WordPress 的精神继任者，它使用 Dynamic Workers 来安全地沙盒化插件，解决了 WordPress 插件系统中的根本性安全和架构问题。该 CMS 基于 Astro 框架构建，可以在包括自托管硬件在内的任何平台上部署。 这很重要，因为 WordPress 为超过 40%的网站提供支持，但一直存在插件安全漏洞和架构限制问题，而 EmDash 的沙盒化插件方法可以显著降低安全风险，改善数百万网站的开发工作流程。基于 TypeScript 的无服务器架构也符合现代 Web 开发向类型安全和可扩展云基础设施发展的趋势。 EmDash 插件被实现为 TypeScript 模块，而不是 WordPress 基于文件的方法，它们在隔离的 Dynamic Workers 中运行，提供毫秒级启动时间，并防止插件访问敏感系统资源。该 CMS 基于 Astro 框架构建，该框架针对内容驱动型网站进行了优化，虽然设计上是无服务器的，但可以部署在任何基础设施上，包括自托管服务器。

hackernews · elithrar · Apr 1, 16:14

**背景**: WordPress 是一个广泛使用的内容管理系统，严重依赖插件来实现功能，但其插件架构存在安全漏洞，恶意插件可以访问数据库和环境变量。Dynamic Workers 是 Cloudflare 的新隔离技术，可以在安全、轻量级的隔离环境中执行不受信任的代码，启动时间仅为毫秒级，是传统容器的替代方案。TypeScript 是一种编程语言，为 JavaScript 添加了静态类型，有助于在开发过程中捕获错误，并提高大型应用程序的代码可维护性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developers.cloudflare.com/dynamic-workers/">Dynamic Workers · Cloudflare Dynamic Workers docs</a></li>
<li><a href="https://blog.cloudflare.com/dynamic-workers/">Sandboxing AI agents, 100x faster</a></li>
<li><a href="https://en.wikipedia.org/wiki/TypeScript">TypeScript - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调了开发者对 EmDash 的 TypeScript 基础和沙盒化插件架构的赞赏，指出它解决了 WordPress 的安全和 CI/CD 挑战。一些用户对其是否能克服 WordPress 的网络效应表示怀疑，而其他人则强调了实际好处，例如将插件视为代码模块而非内容文件。

**标签**: `#CMS`, `#WordPress`, `#TypeScript`, `#Security`, `#Serverless`

---

<a id="item-5"></a>
## [Bonsai 1-bit 模型在极端压缩下仍保持出色质量](https://v.redd.it/1o2k0u2innsg1) ⭐️ 8.0/10

PrismML 发布了 Bonsai 1-bit 量化模型，包括一个 80 亿参数的版本，相比标准模型实现了 14 倍的大小缩减，同时在聊天和文档摘要等实际任务中保持了令人惊讶的良好性能。由于独特的 1-bit 量化方法，这些模型需要使用专门的 llama.cpp 分支进行推理。 这一突破使大语言模型在消费级硬件上变得更加可行，有望在笔记本电脑、移动设备和边缘计算平台上实现本地部署，而无需昂贵的高内存系统。这种极端压缩可以降低 AI 能力的使用门槛，同时减少计算成本和能源消耗。 Bonsai 8B 模型仅有 1GB 大小，需要使用定制的 llama.cpp 分支进行推理，因为标准 llama.cpp 不支持专门的 1-bit 操作。尽管在尺寸方面令人印象深刻，早期测试显示在代码生成任务中存在局限性，并且在超过 4k tokens 的较长上下文中可能出现质量下降。

reddit · r/LocalLLaMA · tcarambat · Apr 1, 22:40

**背景**: 1-bit 量化将模型权重减少为二进制值（通常为-1 和 1），相比标准的 16-bit 或 8-bit 量化，能显著缩小模型大小和内存需求。GGUF 是一种为在消费级硬件上高效加载和运行大语言模型而优化的文件格式，通常与 llama.cpp 一起使用。MLX 是苹果公司为在 Apple Silicon 芯片上进行高效机器学习而开发的框架，尽管提到的 Bonsai 测试并未专门使用 MLX。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2202.05292">[2202.05292] On One-Bit Quantization</a></li>
<li><a href="https://huggingface.co/docs/hub/gguf">GGUF · Hugging Face</a></li>
<li><a href="https://mlx-framework.org/">MLX</a></li>

</ul>
</details>

**社区讨论**: 社区成员对模型的质量与尺寸比表示兴奋，一些人指出在某些任务中它的表现可与更高位数的模型相媲美。有人对代码生成的局限性以及在较长上下文中的潜在质量下降表示担忧，而其他人则强调了在树莓派等低端设备上部署的潜力。几位用户要求与其他模型（如 Qwen 3.5）进行比较，并表示对更大 Bonsai 变体的兴趣。

**标签**: `#quantization`, `#local-llms`, `#model-compression`, `#machine-learning`, `#efficiency`

---

<a id="item-6"></a>
## [Arcee AI 发布 Trinity-Large-Thinking：3980 亿参数稀疏专家混合模型，130 亿激活参数，采用 Apache 2.0 许可证](https://i.redd.it/k8o0rrfoulsg1.png) ⭐️ 8.0/10

Arcee AI 在 Hugging Face 上发布了 Trinity-Large-Thinking 模型，这是一个 3980 亿参数的稀疏专家混合模型，拥有约 130 亿激活参数，采用 Apache 2.0 许可证。该模型在 GPQA（76 分）和 MMLU-Pro 等基准测试中表现出色，同时保持了高稀疏性。 此次发布代表了开源大语言模型的重要进展，将大规模参数与高效的稀疏激活相结合，降低了计算成本。宽松的 Apache 2.0 许可证允许广泛的商业和研究用途，可能加速需要高推理能力的 AI 应用创新。 该模型的稀疏架构意味着在推理过程中仅激活约 3.3%的总参数（3980 亿中的 130 亿），显著降低了内存和计算需求。然而，其庞大尺寸仍带来实际部署挑战，有评论指出它对于四块 RTX 6000 PRO GPU 来说太大，无法以 FP8 精度运行。

reddit · r/LocalLLaMA · TKGaming_11 · Apr 1, 16:24

**背景**: 专家混合架构通过为每个输入仅激活专门的参数子集，使大规模模型能够降低计算成本。稀疏激活指的是消除模型输出中贡献较弱元素的技术，有利于计算加速等应用。Apache 2.0 许可证是一种宽松的开源许可证，为 AI 项目提供广泛的使用权和专利保护。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>
<li><a href="https://openreview.net/forum?id=B9XP2R9LtG">Sparsing Law: Towards Large Language Models with Greater Activation Sparsity | OpenReview</a></li>
<li><a href="https://local-ai-zone.github.io/guides/ai-model-licensing-complete-legal-guide-2025.html">LLM License Types Guide 2025: Complete Legal Compliance & Usage Rights for AI Models - Local AI Zone</a></li>

</ul>
</details>

**社区讨论**: 社区成员对该模型令人印象深刻的稀疏性和性能表示兴奋，有人指出尽管 GPQA 分数相对一般，但其基准测试结果仍具竞争力。多条评论强调了实际部署挑战，包括运行如此大型模型的硬件限制，而其他人则欢迎开放权重发布和 GGUF 格式的可用性，这使推理更加容易。

**标签**: `#large-language-models`, `#open-source`, `#mixture-of-experts`, `#hugging-face`, `#ai-inference`

---

<a id="item-7"></a>
## [attn-rot KV 缓存优化技术已集成到 llama.cpp，显著提升量化效率](https://github.com/ggml-org/llama.cpp/pull/21038#issue-4146294463) ⭐️ 8.0/10

attn-rot 技术（一种类似 TurboQuant 的 KV 缓存优化）已通过拉取请求#21038 合并到 llama.cpp 代码库，实现了 TurboQuant 约 80%的优势且几乎没有缺点，使 Q8 量化性能接近 F16。 该集成通过优化 KV 缓存量化，显著提升了大语言模型的内存效率和推理速度，使高性能量化更易实现，并降低了运行 Llama 和 Qwen 等模型的硬件需求。 该技术涉及将 KV 缓存转换为加权和以平滑异常值，而非极坐标投影，且已在 exllama 和 ik_llama.cpp 等其他实现中使用。它使 Q8 量化性能接近 F16，可能在不显著损失精度的情况下减少 KV 缓存的内存使用。

reddit · r/LocalLLaMA · Dany0 · Apr 1, 15:27

**背景**: KV 缓存是基于 Transformer 的大语言模型中的内存组件，用于存储先前令牌的键值对以加速推理，但在长上下文生成中可能消耗大量内存。量化通过降低这些值的精度（例如从 16 位降至 8 位或更低）来节省内存，TurboQuant 等技术可将 KV 缓存压缩至低至 3 位而不损失精度。Llama.cpp 是一个开源推理引擎，用于在各种硬件上高效运行大语言模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ai-manual.ru/article/attn-rot-turboquant-lite-v-llamacpp-razbor-novogo-metoda-kvantovaniya-kv-kesha-i-benchmarki-dlya-qwen35/">Attn - rot в llama.cpp: новый метод квантования KV-кэша... | AiManual</a></li>
<li><a href="https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/">TurboQuant: Redefining AI efficiency with extreme compression</a></li>
<li><a href="https://medium.com/@tejaswi_kashyap/memory-optimization-in-llms-leveraging-kv-cache-quantization-for-efficient-inference-94bc3df5faef">Memory Optimization in LLMs: Leveraging KV Cache Quantization for...</a></li>

</ul>
</details>

**社区讨论**: 社区讨论显示出复杂情绪，一些用户指出 attn-rot 是已在 exllama 和 ik_llama.cpp 中使用的成熟技术，而其他人则对量化效率提升表示兴奋。关键观点包括关于集成到发布版本的问题、与 TurboQuant 的内存减少比较以及 Q8 版本的实际测试，部分用户计划默认采用 Q8。

**标签**: `#llama.cpp`, `#KV Cache`, `#Quantization`, `#Machine Learning Optimization`, `#Open Source`

---

<a id="item-8"></a>
## [四肢瘫痪者通过脑机接口植入物用意念创作音乐](https://www.wired.com/story/meet-the-man-making-music-with-his-brain-implant/) ⭐️ 8.0/10

2024 年，69 岁的四肢瘫痪者 Galen Buckwalter 接受了开颅手术，植入了六枚 Blackrock Neurotech 芯片，使他能够用意念操作电脑、恢复部分手指感觉，并在研究团队开发的算法帮助下直接用神经信号生成音调。他将实验中创作的音轨用于自己乐队 Siggy 的歌曲《Wirehead》，该曲收录于 3 月 15 日发行的同名专辑中。 这一进展表明，脑机接口技术不仅能用于基本沟通和运动恢复，还能实现音乐创作等创造性表达，突显了其提升残障人士生活质量和个人满足感的潜力。它强调了神经技术向以用户为中心的设计转变，注重与用户兴趣结合以实现长期采用和社会影响。 该植入物使用 Blackrock Neurotech 芯片，具有 96 个阵列来读取和刺激电信号，音乐生成涉及将神经信号转换为音调的算法，使 Buckwalter 能同时控制两路声音。一个关键限制是该技术需要侵入性手术，仍处于研究阶段，长期可用性和可及性面临挑战。

telegram · zaihuapd · Apr 1, 07:34

**背景**: 脑机接口是使大脑与外部设备直接通信的系统，常用于通过恢复运动或沟通能力来帮助瘫痪或神经系统疾病患者。Blackrock Neurotech 是神经植入物的领先开发者，以其能读取和刺激大脑信号的微芯片而闻名，应用于治疗瘫痪等病症。神经信号音乐生成涉及解释大脑活动以创建或控制声音的算法，是辅助和创意技术中的一个新兴领域。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.dailymail.co.uk/sciencetech/article-12007025/The-company-implanted-dozens-chips-peoples-brains.html">The company which has implanted dozens of chips in people's ...</a></li>
<li><a href="https://inews.co.uk/news/technology/blackrock-neurotech-rival-elon-musk-neuralink-2880658">What is Blackrock Neurotech? The rival to Elon Musk's ...</a></li>

</ul>
</details>

**标签**: `#brain-computer interface`, `#neurotechnology`, `#assistive technology`, `#music technology`, `#human-computer interaction`

---

<a id="item-9"></a>
## [DRAM 价格上涨威胁爱好者单板计算机市场的可负担性](https://www.jeffgeerling.com/blog/2026/dram-pricing-is-killing-the-hobbyist-sbc-market/) ⭐️ 7.0/10

Hacker News 讨论显示，DRAM 价格上涨正在对爱好者单板计算机市场产生负面影响，行业预测显示 2026 年第二季度 DRAM 合约价格可能环比上涨 58-63%。社区评论表明这种价格压力不仅限于 SBC 市场，还影响了包括智能手机和通用计算硬件在内的多个技术领域。 这很重要，因为 DRAM 是大多数计算设备的关键组件，价格上涨直接影响消费电子市场的产品可负担性和可用性。对于依赖可访问、低成本硬件进行教育和项目开发的爱好者 SBC 社区来说，这些价格压力可能会限制技术创新和技术开发的参与度。 TrendForce 预测，2026 年第二季度常规 DRAM 合约价格将环比上涨 58-63%，而 NAND 闪存价格同期可能上涨 70-75%。全球单板计算机市场在 2023 年估值约为 31.7 亿美元，考虑到该市场对可负担性的重视，使其特别容易受到组件价格波动的影响。

hackernews · ingve · Apr 1, 21:36

**背景**: DRAM（动态随机存取存储器）是一种用于计算机和电子设备中临时数据存储的易失性存储器。单板计算机是在单个电路板上构建的完整计算机，在爱好者和教育工作者中很受欢迎，用于类似树莓派这样的项目。SBC 市场在 COVID-19 大流行期间曾面临供应链挑战，组件短缺影响了整个技术领域的可用性和定价。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.tomshardware.com/pc-components/dram/dram-and-nand-contract-prices-to-climb-again-in-q2">DRAM prices predicted to jump 63% in Q2, NAND up to 75% ...</a></li>
<li><a href="https://www.zionmarketresearch.com/report/single-board-computer-market">Single Board Computer Market Industry Insights, Growth, Trends,</a></li>
<li><a href="https://www.tomshardware.com/tech-industry/pc-makers-report-surging-prices-across-different-components-increasing-costs-are-going-beyond-memory-chip-and-processors-now-affecting-pcbs-plastic-materials-and-more">PC makers report surging prices across different... | Tom's Hardware</a></li>

</ul>
</details>

**社区讨论**: 社区情绪表达了对广泛市场影响的担忧，评论指出 DRAM 定价正在影响从智能手机到工业机器的"一切"。一些用户强调，除了内存组件之外的供应链问题正在导致价格上涨，而其他人则认为这可能会出于成本原因将某些应用推回微控制器。几位评论者将其与大流行期间先前的组件短缺相提并论，表明这代表了更广泛供应链挑战的延续。

**标签**: `#hardware`, `#economics`, `#supply-chain`, `#single-board-computers`, `#DRAM`

---

<a id="item-10"></a>
## [研究人员在 Transformer 中用基于 RBF 的注意力机制替代点积注意力，以解决幅度偏差问题。](https://www.reddit.com/r/MachineLearning/comments/1s9cdq0/p_i_replaced_dotproduct_attention_with/) ⭐️ 7.0/10

一位研究人员进行了一项技术实验，在 Transformer 中用基于距离的度量（使用径向基函数（RBF）核）替代了标准的缩放点积注意力（SDPA），具体实现了 RBF 注意力机制，根据查询和键之间的平方欧几里得距离计算注意力分数。这一改变旨在缓解'幅度欺凌'问题，即大振幅的键向量无论对齐如何都会主导 softmax。 这一探索具有重要意义，因为它挑战了现代 Transformer 架构的一个基本组成部分，可能催生更鲁棒的注意力机制，减少对向量幅度的敏感性，并可能在某些任务中提升模型的可解释性或性能。它还突显了点积操作在机器学习堆栈中的深度集成，引发了关于硬件优化权衡和更广泛 AI 社区中替代注意力公式的讨论。 该实现需要克服实际挑战，例如朴素成对欧几里得距离计算导致的内存问题，通过代数展开平方距离公式来避免生成完整距离矩阵得以解决。然而，由于硬件优化偏向点积操作，该实验面临局限性，研究人员指出行业解决方案如查询-键归一化（QK-Norm）已在不改变核心操作的情况下解决了幅度偏差问题。

reddit · r/MachineLearning · 4rtemi5 · Apr 1, 06:14

**背景**: 点积注意力是 Transformer 中的核心机制，注意力分数通过查询和键向量的缩放点积计算，使模型能够关注输入序列的相关部分。RBF 核是一种基于距离的函数，常用于支持向量机等核方法中，基于欧几里得距离而非点积来衡量相似性。在 Transformer 中，幅度偏差指大振幅向量不成比例地影响注意力分数的趋势，这可能影响模型行为，先前工作已通过归一化等技术解决了此问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/4rtemi5/rbf_attention">GitHub - 4rtemi5/rbf_attention: Experiment on replacing the ...</a></li>
<li><a href="https://arxiv.org/abs/2006.06147">[2006.06147] Implicit Kernel Attention - arXiv.org Attention is Kernel Trick Reloaded - GitHub Pages Radial basis function kernel - Wikipedia Replacing Dot-Product Attention with RBF-Attention: Technical ... EcoFormer: Energy-Saving Attention with Linear Complexity A novel approach to attention mechanism using kernel ... - PubMed</a></li>
<li><a href="https://arxiv.org/abs/2302.08626">[2302.08626] Role of Bias Terms in Dot-Product Attention ROLE OF BIAS TERMS IN DOT-PRODUCT ATTENTION Role of Bias Terms in Dot-Product Attention - IEEE Xplore Scaled Dot-Product Attention Explained! - by Nikita Prasad Role of Bias Terms in Dot-Product Attention | Request PDF arXiv:2302.08626v1 [cs.NE] 16 Feb 2023 jax.nn.dot_product_attention — JAX documentation</a></li>

</ul>
</details>

**社区讨论**: 社区评论反映了不同的观点，一些用户赞扬这一创新并分享了基于核的注意力的相关工作，而另一些用户则辩论幅度偏差是缺陷还是特性，指出大振幅可以帮助模型打包更多信息。有人提出需要与标准点积注意力进行彻底比较评估，以及硬件优化挑战，因为 GPU 高度优化了点积操作，使得替代方案在实践中效率较低。

**标签**: `#attention-mechanisms`, `#transformers`, `#machine-learning`, `#optimization`, `#neural-networks`

---

<a id="item-11"></a>
## [TurboQuant 被应用于模型权重压缩：Qwen3.5-27B 实现接近 Q4_0 的质量，体积减小 10%](https://i.redd.it/118nngfciksg1.png) ⭐️ 7.0/10

一位开发者创建了一个 llama.cpp 分支，实现了一种名为 TQ3_1S 的新型 3.5 位权重量化格式，应用了受 TurboQuant 启发的技术来压缩 Qwen3.5-27B 模型。这使其困惑度与 Q4_0 量化相比仅差 0.19%，同时模型体积减小约 10%，从而能在 16GB RTX 5060 Ti GPU 上运行。 这展示了如何将先进的量化研究实际应用于解决现实硬件限制，使更大的语言模型能在消费级 GPU 上本地部署，更具可及性。它表明，最初为 KV 缓存设计的基于变换的量化技术，可以有效地适配到权重压缩中，可能影响未来的模型优化方法。 TQ3_1S 格式使用了 Walsh-Hadamard 旋转、8 中心点量化和双半块缩放，并在 llama.cpp 中支持 CUDA 运行时。虽然实现了接近 Q4_0 的困惑度（在 wiki.test.raw 上为 7.2570 对比 7.2431），但一些社区成员指出，Q4_0 被视为一种过时的量化方法，且仅用困惑度可能无法完全捕捉量化损失，相比使用相对于 bf16 基线的 KLD 度量。

reddit · r/LocalLLaMA · pmttyji · Apr 1, 11:58

**背景**: 量化通过用更少的位数（例如 4 位而非 16 位）表示权重来减小模型体积，使更大的模型能在有限的 GPU 内存上运行。TurboQuant 是近期的一种研究技术，旨在优化 Transformer 模型中的 KV（键值）缓存压缩，以减少推理时的内存使用。Q4_0 指的是 GGUF 生态系统中的一种特定 4 位量化格式，不过像 Q4_K_M 这样的新方法通常在相似位宽下能提供更好的质量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://techinformed.com/google-publishes-turboquant-to-ease-ai-memory-strain/">Google publishes TurboQuant to ease AI memory strain -</a></li>
<li><a href="https://simonwillison.net/2024/Nov/23/quantization-matters/">Quantization matters</a></li>
<li><a href="https://pytorch.org/blog/hadacore/">HadaCore: Tensor Core Accelerated Hadamard Transform Kernel</a></li>

</ul>
</details>

**社区讨论**: 社区反应不一，一些人赞扬这种实用的创新和解决现实问题的能力，而另一些人则批评其与过时的 Q4_0 进行比较以及使用困惑度作为度量标准。建议包括与更新的量化方法（如 unsloth Q3_K_S）进行比较，并使用相对于 bf16 基线的 KLD 来进行更准确的质量评估。

**标签**: `#quantization`, `#local-ai`, `#model-compression`, `#gpu-optimization`, `#turboquant`

---

<a id="item-12"></a>
## [Falcon-OCR 与 Falcon-Perception：面向 OCR 与分割任务的轻量级视觉模型](https://v.redd.it/i9vlaiol9ksg1) ⭐️ 7.0/10

技术创新研究院（TII）发布了 Falcon-OCR 和 Falcon-Perception 两款专用视觉模型，分别用于光学字符识别（OCR）和图像分割任务。这些模型具有显著的轻量化特性，并且正在为开源推理库 llama.cpp 开发集成支持。 这些模型为大型多模态模型提供了高效、专用的替代方案，使得文档处理和对象分割等专用视觉任务能够在消费级硬件上以更低的计算成本运行。这符合计算机视觉和人工智能生态系统中模型优化和部署效率的发展趋势。 Falcon-Perception 是一个专注于分割任务的 30 亿参数模型，而 Falcon-OCR 则处理 OCR 任务；两者均设计为紧凑型，据报道 Falcon-Perception 大小约为 7.5 MB。社区讨论强调了其在 GIS 分析和文档处理流程等领域的实际应用，不过一些用户指出了在设置方面的挑战，以及缺乏与 GLM-OCR 等其他 OCR 模型的直接比较。

reddit · r/LocalLLaMA · Automatic_Truth_6666 · Apr 1, 11:05

**背景**: 光学字符识别（OCR）是一种将文本图像转换为机器编码文本的技术，而图像分割则涉及将图像分割成多个部分以简化分析。Llama.cpp 是一个开源软件库，能够在各种硬件上高效运行大型语言模型的推理，常用于优化模型部署。此类轻量级视觉模型旨在降低计算需求，同时保持特定任务的性能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Llama.cpp">Llama.cpp</a></li>
<li><a href="https://sanaazahra.medium.com/ocr-segmentation-with-python-code-f3251114ee48">OCR Segmentation with Python Code | by Sana'a Zahra | Medium</a></li>

</ul>
</details>

**社区讨论**: 社区表现出浓厚兴趣，评论赞扬了对 llama.cpp 支持的努力和模型的小巧尺寸，不过也有人幽默地提到了带宽担忧。讨论了实际应用，例如在 GIS 中使用 Falcon-Perception 进行树木分割，而其他人则对模型在低质量文档上的性能（与 PaddleOCR 等工具相比）表示好奇。批评意见包括缺乏与 GLM-OCR 的比较，以及报告了如 PyTorch 错误等设置问题。

**标签**: `#computer-vision`, `#OCR`, `#machine-learning`, `#open-source`, `#model-optimization`

---

<a id="item-13"></a>
## [GitHub 出现非官方仓库，通过 npm 包的 source map 还原 Claude Code 2.1.88 的 4756 个 TypeScript 文件。](https://t.me/zaihuapd/40641) ⭐️ 7.0/10

一个名为 'claude-code-sourcemap' 的非官方 GitHub 仓库通过公开 npm 包 @anthropic-ai/claude-code 附带的 source map 文件 cli.js.map 中的 sourcesContent 字段，还原出 Claude Code 2.1.88 的 TypeScript 源码，共 4756 个文件，其中包括 1884 个 .ts 和 .tsx 文件。 这一事件凸显了软件发布中的重大安全疏忽，因为 source map 可能无意中暴露专有代码，可能影响 Anthropic 等公司的 AI 工具透明度和知识产权保护。 还原过程利用了 source map 中的 sourcesContent 字段，该字段嵌入了原始源代码，使得无需访问原始仓库即可重建代码；这是 npm 包构建中常见但常被忽视的问题。

telegram · zaihuapd · Apr 1, 08:07

**背景**: Source map 是将压缩或打包的 JavaScript 代码映射回原始源代码的文件，用于辅助调试；它们通常包含 sourcesContent 字段，该字段包含完整的源代码文本，如果包含在生产包中，可能导致代码意外暴露。Claude Code 是 Anthropic 开发的 AI 编码助手，而 npm 是 JavaScript 的包管理器，托管公共和私有代码库。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://alan-west.hashnode.dev/your-npm-package-is-leaking-source-code-heres-how-to-fix-it">Your NPM Package Is Leaking Source Code (Here's How to Fix It)</a></li>
<li><a href="https://dev.to/gabrielanhaia/claude-codes-entire-source-code-was-just-leaked-via-npm-source-maps-heres-whats-inside-cjo">Claude Code's Entire Source Code Was Just Leaked via npm ...</a></li>

</ul>
</details>

**标签**: `#reverse-engineering`, `#source-maps`, `#claude-code`, `#npm`, `#typescript`

---