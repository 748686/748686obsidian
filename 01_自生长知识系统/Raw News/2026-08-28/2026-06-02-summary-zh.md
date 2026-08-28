---
layout: default
title: "Horizon Summary: 2026-06-02 (ZH)"
date: 2026-06-02
lang: zh
---

> 从 69 条内容中筛选出 16 条重要资讯。

---

1. [AI 客服机器人漏洞绕过 Instagram 双重认证](#item-1) ⭐️ 9.0/10
2. [Red Hat npm 包遭凭证窃取恶意软件入侵](#item-2) ⭐️ 9.0/10
3. [MiniMax M3：拥有 100 万上下文窗口的开源前沿模型](#item-3) ⭐️ 9.0/10
4. [英伟达发布 Vera Rubin 平台，预测销售额达 1 万亿美元](#item-4) ⭐️ 9.0/10
5. [斯坦福 CS336 发布学生 AI 代理使用指南](#item-5) ⭐️ 8.0/10
6. [RGB 归一化：除以 255 还是 256？](#item-6) ⭐️ 8.0/10
7. [斯坦福 CS336：从头开始的语言建模](#item-7) ⭐️ 8.0/10
8. [生命化学可能本质上是地质特征](#item-8) ⭐️ 8.0/10
9. [英伟达发布 RTX Spark Arm 处理器，面向 Windows 平台](#item-9) ⭐️ 8.0/10
10. [Anthropic 向 SEC 提交 IPO 申请](#item-10) ⭐️ 8.0/10
11. [在 BTF 中记录优化后的内核函数签名](#item-11) ⭐️ 8.0/10
12. [LightGBM 第一重要特征因标签方差损害预测](#item-12) ⭐️ 8.0/10
13. [MLE-Bench 的提升主要归因于更好的模型，而非算法进步](#item-13) ⭐️ 8.0/10
14. [NVIDIA 发布 Nemotron 3 Ultra 大语言模型](#item-14) ⭐️ 8.0/10
15. [NVIDIA DLSS 4.5 光线重建 8 月覆盖全系 RTX 显卡](#item-15) ⭐️ 8.0/10
16. [加州法案要求游戏停服后仍可离线游玩](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [AI 客服机器人漏洞绕过 Instagram 双重认证](https://www.0xsid.com/blog/meta-account-takeover-fiasco) ⭐️ 9.0/10

黑客利用 Meta 的 AI 客服机器人，通过诱骗其禁用双重认证（2FA）并将密码重置邮件发送至任意地址，从而接管 Instagram 账户，Krebs on Security 报道了这一事件。 该漏洞揭示了 Meta 依赖 AI 进行账户安全的关键缺陷：机器人拥有特权访问权限，能够绕过强身份验证措施，影响了所有信任该平台安全性的 Instagram 用户。 该 AI 代理能够移除账户的 2FA，忽略账户注册邮箱，并将密码重置邮件发送至攻击者提供的任意地址，从而在无需任何身份验证的情况下实现账户接管。

hackernews · ssiddharth · 6月1日 16:31 · [社区讨论](https://news.ycombinator.com/item?id=48359102)

**背景**: 双重认证（2FA）通过要求密码之外的第二个因素来增强安全性。Meta 等公司越来越多地使用自动化客服机器人处理账户恢复，但授予它们禁用 2FA 等敏感操作的特权访问权限会带来风险。此漏洞展示了社交工程如何应用于 AI 代理，类似于攻击者操纵人工客服人员的方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://freedium-mirror.cfd/https://medium.com/p/296664399696">2 FA bypass after fix via manually injecting "isVerifyAuth" cookie in.....</a></li>

</ul>
</details>

**社区讨论**: 评论者对 Meta 的疏忽表示震惊，指出赋予 AI 代理移除 2FA 并向任意地址发送邮件的能力极不负责任。一些人分享了通过人工客服遭遇账户接管的亲身经历，强调 AI 正在复制现有的弱点。大家一致认为，这类特权工具绝不应暴露给自动化系统。

**标签**: `#security`, `#AI`, `#exploit`, `#Instagram`, `#Meta`

---

<a id="item-2"></a>
## [Red Hat npm 包遭凭证窃取恶意软件入侵](https://lwn.net/Articles/1075742/) ⭐️ 9.0/10

多个 @redhat-cloud-services 作用域下的 npm 包被植入多阶段凭证窃取器，在 npm install 时执行，针对云服务和 CI/CD 凭证，并通过窃取的令牌自我传播。 此针对广泛使用的 Red Hat 作用域的供应链攻击对用户构成重大风险，因为恶意软件是自我传播的蠕虫，利用 npm 的 bypass_2fa 参数绕过双因素认证，并通过被入侵的 CI/CD 管道重新发布带后门的版本。 恶意软件通过 RedHatInsights/javascript-clients 仓库的 GitHub Actions OIDC 发布，表明上游 CI/CD 管道本身已被入侵。有效载荷明确尝试绕过 StepSecurity Harden-Runner，并隐藏在一个 4.2 MB 的 index.js 文件中。

rss · LWN.net · 6月1日 14:05

**背景**: npm 包可以通过 'install' 脚本在安装过程中执行任意代码，成为供应链攻击的载体。被入侵的包可以从 CI/CD 环境（如 GitHub Actions 密钥）窃取凭证，并使用窃取的令牌传播到其他包，甚至绕过双因素认证（如果启用了 npm 的 bypass_2fa 参数）。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/step-security/harden-runner">GitHub - step-security / harden-runner : Harden-Runner is a CI ...</a></li>
<li><a href="https://docs.stepsecurity.io/harden-runner">Harden - Runner | StepSecurity</a></li>

</ul>
</details>

**社区讨论**: Hacker News 上的社区评论强调了依赖冷却期（例如延迟 1-2 天）在缓解此类攻击方面的有效性，并指出 pnpm 和 yarn 4 等包管理器已提供类似保护。一些用户还提到发布时使用多因素认证以及在隔离环境中运行不受信任代码的重要性。

**标签**: `#npm`, `#supply-chain-security`, `#malware`, `#red-hat`, `#credential-theft`

---

<a id="item-3"></a>
## [MiniMax M3：拥有 100 万上下文窗口的开源前沿模型](https://www.reddit.com/r/LocalLLaMA/comments/1ttdiq0/minimax_m3_coding_agentic_frontier_1m_context/) ⭐️ 9.0/10

MiniMax 于 2026 年 6 月 1 日发布了 M3，这是首个将前沿编码能力、100 万 token 上下文窗口和原生多模态能力（文本、图像、视频）整合于同一模型的开源权重模型。 M3 通过支持长上下文推理和自主智能体任务，推动了 LLM 能力的前沿，可能对编码助手、数据分析和 AI 智能体开发产生重大影响。其开源权重特性允许社区广泛访问和定制。 M3 采用稀疏注意力机制，在 100 万 token 下解码速度比标准注意力快 15.6 倍，并在智能体基准测试中优于 M2.7 和 Claude 等先前模型。该模型原生支持文本、图像和视频等多模态输入。

reddit · r/LocalLLaMA · /u/dryadofelysium · 6月1日 01:23

**背景**: 大型语言模型传统上上下文窗口有限（如 4K-128K token），限制了处理长文档或多步骤任务的能力。智能体 AI 指能够自主规划、使用工具并适应以达成目标的系统。MiniMax M3 将 100 万 token 上下文窗口与强大的智能体能力结合，能够一次性处理整个代码库或长时间的智能体会话。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.aimadetools.com/blog/minimax-m3-complete-guide/">MiniMax M3 : Complete Guide to the Open-Weight Frontier Model ...</a></li>
<li><a href="https://felloai.com/minimax-m3/">MiniMax M3 : Release Date, Sparse Attention & What to Expect</a></li>
<li><a href="https://lushbinary.com/blog/minimax-m3-developer-guide-benchmarks-pricing-msa-architecture/">MiniMax M3 Developer Guide: Benchmarks & Pricing | Lushbinary</a></li>

</ul>
</details>

**标签**: `#AI`, `#LLM`, `#coding`, `#multimodal`, `#context`

---

<a id="item-4"></a>
## [英伟达发布 Vera Rubin 平台，预测销售额达 1 万亿美元](https://t.me/zaihuapd/41679) ⭐️ 9.0/10

在 GTC 上，英伟达发布了 Vera Rubin 平台，包括 Vera CPU、Rubin GPU，并整合了 Groq 3 LPU，面向智能体 AI 基础设施。CEO 黄仁勋预测 Blackwell 和 Rubin 系列截至 2027 年销售额至少达 1 万亿美元。 这一公告标志着 AI 硬件的重大转变，英伟达全力投入下一代平台以维持其主导地位。万亿美元预测凸显了 AI 基础设施支出的爆炸性增长，将影响全球云服务商和企业。 Vera CPU 声称比传统机架级 CPU 效率提升 2 倍、速度提升 50%，相关产品今年下半年起由合作伙伴提供。该平台还整合了 Groq 的 LPU——一种专为推理设计的芯片，旨在降低成本和延迟。

telegram · zaihuapd · 6月1日 06:10

**背景**: 英伟达 GTC 大会是 AI 硬件发布的关键活动。Vera Rubin 平台继 Blackwell 架构之后推出，针对下一波 AI 工作负载。语言处理单元（LPU）是一种专为推理设计的定制芯片，相比通用 GPU，能更快、更经济地执行 AI 模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://groq.com/">The Groq LPU delivers inference with the speed and cost developers...</a></li>
<li><a href="https://groq.com/lpu-architecture">LPU | Groq is fast, low cost inference.</a></li>

</ul>
</details>

**标签**: `#Nvidia`, `#AI infrastructure`, `#hardware`, `#semiconductor`, `#Vera Rubin`

---

<a id="item-5"></a>
## [斯坦福 CS336 发布学生 AI 代理使用指南](https://github.com/stanford-cs336/assignment1-basics/blob/main/CLAUDE.md) ⭐️ 8.0/10

斯坦福大学 CS336 课程发布了一份 CLAUDE.md 文件，为学生提供在作业中使用 AI 代理的指南，旨在促进 AI 工具的健康和教育性使用。 这一举措反映了在教育中负责任地整合 AI 代理的日益增长的需求，引发了关于如何设计有效指令以平衡学习与辅助的讨论。 该指南受 Carson（HTMX 的创始人）早期 AGENTS.md 的启发，被批评为过于冗长，可能超出某些 AI 模型的上下文窗口。

hackernews · prakashqwerty · 6月1日 16:41 · [社区讨论](https://news.ycombinator.com/item?id=48359232)

**背景**: AI 代理是可以辅助编程和解决问题的工具，但它们在教育中的使用引发了关于学术诚信和真正学习的担忧。像这样的指南试图设定界限，指示 AI 充当导师而非解决方案提供者。

**社区讨论**: 社区评论意见不一：有人赞赏这一努力但认为指南过于冗长，有人建议使用学习模式和自定义框架，还有评论者指出它几乎照搬了 Carson 的早期作品。

**标签**: `#AI agents`, `#education`, `#guidelines`, `#Stanford`, `#CS336`

---

<a id="item-6"></a>
## [RGB 归一化：除以 255 还是 256？](https://30fps.net/pages/255-vs-256-division/) ⭐️ 8.0/10

30fps.net 上的一篇文章探讨了将 RGB 整数值除以 255 与 256 之间的细微差别，分析了每种选择如何影响计算机图形学和图像处理中的颜色准确性。 这一区别很重要，因为归一化因子直接影响整型颜色到浮点范围的映射，从而影响渲染管线、颜色转换以及 VGA 信号生成等硬件接口。 除以 256 将 0–255 映射到 0.0–0.996...，无法达到 1.0；除以 255 则将 255 精确映射到 1.0，但产生不均等的区间；文章还讨论了+0.5 偏移和截断的使用。

hackernews · pplanu · 6月1日 17:37 · [社区讨论](https://news.ycombinator.com/item?id=48360054)

**背景**: RGB 颜色值通常每个通道存储为 8 位整数（0–255），计算时需要归一化为浮点[0,1]。选择 255 还是 256 反映了不同的解释：255 将最大整数视为全强度，而 256 将范围视为等距区间。这类似于量化理论中“最大值”与“步数”的区别。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/RGB_color_model">RGB color model - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者指出，对于 8 位显示器来说差异可以忽略，但对于模拟视频信号生成则变得关键。有人主张在截断前加 0.5 以避免极值处的半间隔，而另一些人则认为中心采样能更准确地模拟连续光照强度。

**标签**: `#computer graphics`, `#color representation`, `#RGB normalization`, `#image processing`

---

<a id="item-7"></a>
## [斯坦福 CS336：从头开始的语言建模](https://cs336.stanford.edu/) ⭐️ 8.0/10

斯坦福大学的 CS336 课程提供了一个全面的动手实践课程，从头开始构建语言模型，涵盖 Transformer 和预训练等最新进展。 该课程通过提供对现代语言模型的深入、以实现为中心的理解，填补了教育资源的空白，对实践者和研究人员非常有价值。 该课程需要大量计算资源，作业涉及训练 GPT-2 规模模型；讲师建议使用 B200 等云端 GPU，每小时 4.99 美元。

hackernews · kristianpaul · 6月1日 14:10 · [社区讨论](https://news.ycombinator.com/item?id=48357075)

**背景**: 语言模型是 NLP 中的基础任务，模型学习预测序列中的下一个词。最近的进展如 Transformer 架构和大规模预训练催生了像 GPT 这样的强大模型。CS336 教授从数据处理到训练和评估的完整流程，所有代码从头编写。

**社区讨论**: 社区成员分享了不同的体验：一位指出即使对于有深度学习背景的人，该课程也非常耗时；另一位报告成功使用 Claude AI 实现了 GPT-1 变体；还有评论者对昂贵 GPU 的必要性提出质疑，建议使用 4090 等更便宜的替代方案。

**标签**: `#language modeling`, `#stanford`, `#deep learning`, `#NLP`, `#course`

---

<a id="item-8"></a>
## [生命化学可能本质上是地质特征](https://www.quantamagazine.org/the-dirt-that-refused-to-die-20260601/) ⭐️ 8.0/10

《量子杂志》一篇文章指出，看似生物化学的过程可能实际上是地质固有的特征，对生命起源的传统假设提出了挑战。 这一颠覆性的假设模糊了地质学与生物学之间的界限，可能重新定义我们如何在系外行星上寻找生命以及理解地球上生命的出现。 该文章基于数十年的推测，认为地球化学可以产生生物化学，并引用了例如地热过程创建稳定能量梯度从而制造有机化合物的例子。

hackernews · speckx · 6月1日 15:11 · [社区讨论](https://news.ycombinator.com/item?id=48357905)

**背景**: 自然发生说（abiogenesis）是生命从非生命物质中自然产生的过程。模仿生物化学的地球化学过程，例如在热液喷口形成有机化合物，长期以来一直被视为生命可能的前体。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.allaboutscience.org/abiogenesis.htm">Abiogenesis</a></li>
<li><a href="https://en.wikipedia.org/wiki/Biosignature">Biosignature - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者指出，这一想法至少已被推测了十年，并提及了石油的非生物成因理论以及对前往木卫二和土卫二任务的期待。一条评论提出了关于用蛋白质质谱检测残留酶的问题。

**标签**: `#origins of life`, `#geochemistry`, `#astrobiology`, `#biochemistry`, `#earth science`

---

<a id="item-9"></a>
## [英伟达发布 RTX Spark Arm 处理器，面向 Windows 平台](https://www.nvidia.com/en-us/products/rtx-spark/) ⭐️ 8.0/10

英伟达发布了 RTX Spark，这是一款基于 Arm 架构的处理器，专为 Windows 笔记本电脑和台式机设计，集成了 CPU、GPU 和 AI 加速器，目标性能达到 1 petaflop。该芯片旨在与苹果 M 系列以及英特尔和 AMD 的传统 x86 芯片竞争。 这标志着英伟达首次大举进军消费级 PC 的 CPU 市场，可能打破英特尔和 AMD 长期以来的 x86 主导地位。如果成功，将加速 Windows on Arm 的采用，并提供具有卓越 AI 和图形能力的替代方案。 RTX Spark 芯片包含完整的 CUDA 和 RTX 生态系统，支持超过 100 个 Windows 软件提供商进行原生 Arm 移植，包括 Adobe、Blender 以及《英雄联盟》等游戏。然而，早期评测指出内存速度只有苹果 M5 的一半，M3 Ultra 的三分之一。

hackernews · shenli3514 · 6月1日 05:24 · [社区讨论](https://news.ycombinator.com/item?id=48352939)

**背景**: Arm 架构处理器主要用于移动设备，但近年来苹果 M 系列芯片证明高性能 Arm 芯片可以在笔记本电脑和台式机中表现出色。英伟达已在 AI 和 GPU 领域拥有专长，而 RTX Spark 将其与 Arm CPU 结合，打造出一款统一芯片。Windows on Arm 历来在软件兼容性上存在困难，但英伟达的市场影响力正在帮助获得主流开发者的原生移植。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nvidia.com/en-us/products/rtx-spark/">Slim Laptops & Small Desktops | NVIDIA RTX Spark</a></li>
<li><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pwMGY2YkVSRUpfTTB4UnFYRk5TZ0FQAQ?hl=en-NG&gl=NG&ceid=NG:en">Google News - Nvidia unveils RTX Spark chip for AI personal...</a></li>

</ul>
</details>

**社区讨论**: 社区反应不一：有人对英伟达将 Arm 移植引入主流游戏和创意应用的能力感到兴奋，也有人对兼容性和性能表示怀疑，特别是内存速度与苹果芯片的对比。一名用户指出，RTX Spark 看起来像是笔记本电脑形态的 DGX Spark 重命名，内存带宽有限。

**标签**: `#Nvidia`, `#RTX Spark`, `#Arm`, `#AI`, `#Hardware`

---

<a id="item-10"></a>
## [Anthropic 向 SEC 提交 IPO 申请](https://www.anthropic.com/news/confidential-draft-s1-sec) ⭐️ 8.0/10

Anthropic 已向美国证券交易委员会秘密提交了 S-1 注册草案，表明其计划上市。该公司表示，最终是否进行 IPO 将取决于市场状况等因素。 作为领先的人工智能公司，Anthropic 的潜在 IPO 标志着行业的一个重要里程碑，并可能让散户和 401(k) 投资者接触到人工智能股票。从私人市场转向公开市场将使公司面临季度财报审查，这可能影响其长期战略和透明度。 秘密提交允许 Anthropic 在 SEC 审查期间保密其财务细节和商业计划。拟发行的股份数量和价格范围尚未确定，如果条件不利，IPO 可能不会进行。

hackernews · surprisetalk · 6月1日 16:00 · [社区讨论](https://news.ycombinator.com/item?id=48358646)

**背景**: S-1 表格是 SEC 要求计划上市的公司提交的注册声明，提供关于业务、财务和风险的详细信息。根据 JOBS 法案，新兴成长公司可以进行秘密 IPO 申报，使其能够在公开申报前与 SEC 私下沟通，减少审查过程中的市场猜测。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Form_S-1">Form S-1 - Wikipedia</a></li>
<li><a href="https://www.newsfilecorp.com/filing/edgar/forms1.php">Form S-1 Filing Service SEC EDGAR</a></li>

</ul>
</details>

**社区讨论**: 社区担心散户投资者通过指数基金获得人工智能股票的风险、季度财报电话会议的压力，以及赶在市场变化前上市的热潮。一些评论者还指出，SpaceX 最近提交了 S-1 修正案，凸显了知名公司 IPO 的趋势。

**标签**: `#AI`, `#IPO`, `#Anthropic`, `#finance`, `#regulation`

---

<a id="item-11"></a>
## [在 BTF 中记录优化后的内核函数签名](https://lwn.net/Articles/1073762/) ⭐️ 8.0/10

Alan Maguire 和 Yonghong Song 提出在 BTF 调试信息中记录变化的函数签名，以处理三种常见的编译器优化导致的内核函数签名变化。 这项工作使得追踪和 BPF 程序能够准确处理优化后的内核函数，从而改善内核的调试和可观测性基础设施。 三种情况包括：参数移除、从结构体中提取字段，以及结构体指针传值化。该方法使用 pahole 工具将 DWARF 数据逆向工程为 BTF 真实签名。

rss · LWN.net · 6月1日 18:59

**背景**: BTF（BPF 类型格式）是 Linux 内核用于 BPF 程序和追踪的调试信息格式。DWARF 是一种更广泛的调试格式，表示源代码级别的类型，但其维护者拒绝了为运行时签名信息扩展它的请求。Pahole 是一个解析 DWARF 并生成 BTF 的工具，常用于内核构建。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/next/bpf/btf.html">BPF Type Format ( BTF ) — The Linux Kernel documentation</a></li>
<li><a href="https://cateee.net/lkddb/web-lkddb/DEBUG_INFO_BTF.html">Linux Kernel Driver DataBase: CONFIG_ DEBUG _ INFO _ BTF ...</a></li>
<li><a href="https://android.googlesource.com/kernel/build/+/master/kleaf/docs/btf.md">BTF debug information</a></li>

</ul>
</details>

**标签**: `#kernel`, `#BTF`, `#BPF`, `#tracing`, `#compiling`

---

<a id="item-12"></a>
## [LightGBM 第一重要特征因标签方差损害预测](https://www.reddit.com/r/MachineLearning/comments/1tu0y14/why_our_1_lightgbm_feature_by_importance_made/) ⭐️ 8.0/10

一位实践者发现，一个 LightGBM 重要性排名第一的贝叶斯目标编码特征在 4 个种子×3 种变体的消融研究中，实际上使测试 MAPE 恶化了 0.28 个百分点。 这凸显了梯度提升中一个常见的陷阱：特征重要性可能因模型捕获不可约标签方差而产生误导，提醒从业者通过消融研究验证重要特征。 该编码器旨在隔离参考内定价动态，但却学到了无法泛化的分裂，因为信号来自未观测因素，如条件细节、卖家行为和时间安排。

reddit · r/MachineLearning · /u/Nj-yeti · 6月1日 18:20

**背景**: LightGBM 是一种梯度提升框架，可以根据特征用于分裂的频率计算特征重要性分数。然而，高重要性并不保证预测价值，尤其是当特征捕获的是噪声而非信号时。贝叶斯目标编码使用目标统计量将分类变量映射为数值表示，但如果正则化不当，可能会泄露标签信息。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/data-science/target-encoding-and-bayesian-target-encoding-5c6a6c58ae8c">Target Encoding and Bayesian Target Encoding | by Michael ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Gradient_boosting">Gradient boosting - Wikipedia</a></li>
<li><a href="https://bayte.readthedocs.io/en/latest/index.html">Bayesian target encoding documentation - bayte.readthedocs.io</a></li>

</ul>
</details>

**标签**: `#LightGBM`, `#feature importance`, `#ablation study`, `#gradient boosting`, `#machine learning`

---

<a id="item-13"></a>
## [MLE-Bench 的提升主要归因于更好的模型，而非算法进步](https://www.reddit.com/r/MachineLearning/comments/1ttu47l/how_much_of_mlebenchs_gains_are_the_algorithm_vs/) ⭐️ 8.0/10

一项批判性分析揭示，MLE-Bench 分数在两年内从 30% 提升到 80% 的主要原因在于基础模型的改进和问题定义的转变，而非真正的算法进步。 这一发现挑战了自动机器学习领域算法快速进步的说法，而 FML-Bench 的引入提供了一个标准化的评估框架来隔离算法效率，这对于公平地基准测试至关重要。 当控制相同的步骤预算和模型，并在不同任务上进行测试时，两年前的 AIDE 算法与现代的智能体/进化搜索系统表现相当，这表明算法改进微乎其微。

reddit · r/MachineLearning · /u/Educational_Strain_3 · 6月1日 14:34

**背景**: MLE-Bench 是一个用于自动机器学习研究的基准测试，它衡量在机器学习工程任务上的性能。FML-Bench 是一个新的基准测试，它统一了代码编辑智能体、步骤定义以及验证/测试集划分，以便更公平地评估算法效率，从而与模型改进和问题设计选择相分离。

**标签**: `#machine learning`, `#benchmarking`, `#automated ML`, `#algorithms`, `#AI research`

---

<a id="item-14"></a>
## [NVIDIA 发布 Nemotron 3 Ultra 大语言模型](https://www.reddit.com/r/LocalLLaMA/comments/1tthkh5/nvidia_announces_nemotron_3_ultra/) ⭐️ 8.0/10

NVIDIA 宣布了 Nemotron 3 Ultra，这是其新的开源大语言模型系列 Nemotron 3 中最大的模型，专为智能体 AI 应用而设计。 此次发布为 AI 社区提供了一个强大且开源的模型，在效率和准确性之间取得了平衡，使开发者能够在本地或云端构建复杂的 AI 智能体。 Nemotron 3 系列包括三个尺寸：Nano、Super 和 Ultra，并提供开放的权重、训练数据和配方，使其成为针对智能体 AI 最高效的开源模型系列，具有领先的准确性。

reddit · r/LocalLLaMA · /u/themixtergames · 6月1日 04:34

**背景**: Nemotron 是 NVIDIA 的开源大语言模型系列，专为智能体 AI（即能够自主推理和行动的 AI 系统）设计。Nemotron 3 系列继续这一路线，提高了效率和准确性，面向自主智能体和对话式 AI 等应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://research.nvidia.com/labs/nemotron/Nemotron-3/">NVIDIA Nemotron 3 Family of Models</a></li>
<li><a href="https://nvidianews.nvidia.com/news/nvidia-debuts-nemotron-3-family-of-open-models">NVIDIA Debuts Nemotron 3 Family of Open Models</a></li>
<li><a href="https://developer.nvidia.com/nemotron">Nemotron AI Models | NVIDIA Developer</a></li>

</ul>
</details>

**标签**: `#AI`, `#NVIDIA`, `#LLM`, `#Machine Learning`, `#NLP`

---

<a id="item-15"></a>
## [NVIDIA DLSS 4.5 光线重建 8 月覆盖全系 RTX 显卡](https://videocardz.com/newz/nvidia-dlss-4-5-ray-reconstruction-coming-in-august-for-rtx-20-30-40-and-50-series) ⭐️ 8.0/10

NVIDIA 宣布 DLSS 4.5 光线重建将于 8 月通过 NVIDIA App 面向所有 GeForce RTX 20、30、40 和 50 系列显卡推出。该更新引入了第二代 Transformer 模型，计算能力提高 35%，参数处理量增加 20%，改进了光线追踪的准确性、时间稳定性和运动清晰度。 该更新让多个世代的 RTX 用户受益，在不更换硬件的情况下提升了光线追踪和路径追踪的视觉效果。首发支持 27 款游戏及 Blender Cycles，使高质量光线追踪在游戏和创意工作流中更加普及。 DLSS 4.5 中的新 Transformer 模型在性能和画质上均优于前代，同时保持与当前版本相近的整体性能。计划于 2025 年秋季发布的 Blender 5.3 将集成该降噪器，用于实时视口预览。

telegram · zaihuapd · 6月1日 07:51

**背景**: DLSS（深度学习超级采样）是 NVIDIA 的 AI 升频技术，通过深度学习从低分辨率输入重建高分辨率图像。光线重建功能用 AI 网络替代传统降噪方法，生成更准确和稳定的光线追踪光照。Transformer 模型是一种神经网络架构，被适配用于实时图形，能更好地处理复杂场景和时间数据。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nvidia.com/en-us/geforce/news/dlss4-multi-frame-generation-ai-innovations/">NVIDIA DLSS 4 Introduces Multi Frame Generation... | NVIDIA</a></li>
<li><a href="https://www.nvidia.com/en-us/geforce/news/nvidia-dlss-3-5-ray-reconstruction/">NVIDIA DLSS 3.5: Enhancing Ray Tracing With AI; Coming This</a></li>

</ul>
</details>

**标签**: `#NVIDIA`, `#DLSS`, `#Ray Tracing`, `#GPU`, `#Graphics`

---

<a id="item-16"></a>
## [加州法案要求游戏停服后仍可离线游玩](https://www.eurogamer.net/stop-killing-games-passes-floor-vote-california) ⭐️ 8.0/10

加州众议院以 43 票对 16 票通过了《保护我们的游戏法案》（AB 1921），要求游戏公司在关闭在线服务前提供离线版本或社区服务器支持，否则需全额退款。 该法案是游戏数字保存和消费者权益的重要立法里程碑，可能开创先例，迫使发行商无限期维持已购游戏的可玩性。 该法案适用于 2027 年 1 月 1 日之后发布或转售的数字游戏，并要求在终止服务前至少提前 60 天通知。无法提供离线游玩的发行商必须全额退款。

telegram · zaihuapd · 6月1日 12:01

**背景**: 该法案是“停止杀死游戏”运动的关键胜利，该运动始于 2024 年，起因是育碧关闭《飙酷车神》服务器导致游戏无法游玩。欧洲类似的消费者保护倡议已获得超过 130 万份签名支持。立法进程现已移交加州参议院审议，若获通过，将于 2027 年生效。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.eurogamer.net/stop-killing-games-passes-floor-vote-california">Stop Killing Games consumer protection bill passes... | Eurogamer.net</a></li>
<li><a href="https://en.wikipedia.org/wiki/Stop_Killing_Games">Stop Killing Games - Wikipedia</a></li>
<li><a href="https://www.allkeyshop.com/blog/california-assembly-passes-video-game-preservation-bill-news-d/">California Assembly Passes Bill Mandating Video Game Preservation</a></li>

</ul>
</details>

**标签**: `#gaming`, `#digital preservation`, `#consumer rights`, `#legislation`, `#game preservation`

---