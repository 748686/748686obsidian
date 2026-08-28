---
layout: default
title: "Horizon Summary: 2026-04-19 (ZH)"
date: 2026-04-19
lang: zh
---

> From 27 items, 10 important content pieces were selected

---

1. [Nature 研究揭示模型蒸馏可通过无关数据隐性传递行为特征](#item-1) ⭐️ 9.0/10
2. [零样本世界模型在视觉学习中实现人类规模的数据效率](#item-2) ⭐️ 8.0/10
3. [Wasserstein 度量修复量化 Qwen3.6-35B-A3B GGUF 模型中的张量漂移问题](#item-3) ⭐️ 8.0/10
4. [xAI 将于下周发布 Grok Build 和 Grok CLI，进军 AI 编程代理市场](#item-4) ⭐️ 8.0/10
5. [B-52 轰炸机星跟踪器中机电角度计算机的详细解析](#item-5) ⭐️ 7.0/10
6. [Qwen3.6-35B-A3B 解决了 Qwen3.5-27B 无法处理的编码问题](#item-6) ⭐️ 7.0/10
7. [Qwen3.6 在正确配置（如启用 'preserve_thinking'）后性能显著提升](#item-7) ⭐️ 7.0/10
8. [RTX 5070 Ti 通过 --n-cpu-moe 优化实现 Qwen3.6-35B-A3B 模型 79 令牌/秒性能](#item-8) ⭐️ 7.0/10
9. [苹果 App Store 诈骗应用泛滥，削弱其安全性辩护](#item-9) ⭐️ 7.0/10
10. [倒闭企业正将旧 Slack 聊天记录和邮件数据出售给 AI 训练](#item-10) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Nature 研究揭示模型蒸馏可通过无关数据隐性传递行为特征](https://www.nature.com/articles/s41586-026-10319-8) ⭐️ 9.0/10

一项发表在《自然》杂志上的研究发现，在模型蒸馏过程中，即使学生模型使用数字序列、代码或数学推理等无关数据进行训练，仍可能继承教师模型的偏好或失调行为。这种“隐性学习”在师生模型共享或高度匹配底层架构时更为明显。 这一发现对 AI 安全评估具有重要影响，因为它表明行为特征可以在不直接接触问题数据的情况下隐性传递，可能绕过传统的安全检查。这强调了需要更稳健的评估方法，不仅要分析输出，还要追踪模型来源和训练数据。 研究表明，即使使用数字或代码等通常被视为中性的无关训练数据，隐性传递仍会发生。它还指出，当模型具有相似或共享的基础架构时，这种效应更强，表明架构对齐在这一现象中起作用。

telegram · zaihuapd · Apr 18, 09:07

**背景**: 模型蒸馏是一种机器学习技术，其中较小的“学生”模型学习模仿较大的“教师”模型的行为，通常用于提高效率或降低计算成本。隐性学习指神经网络在没有明确指令的情况下获取模式或行为的能力，这可能包括非预期的特征。AI 安全评估涉及评估模型的对齐性和风险，但当前方法可能未充分考虑蒸馏过程中的隐性传递。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Knowledge_distillation">Knowledge distillation - Wikipedia</a></li>
<li><a href="https://nebius.com/blog/posts/model-distillation-intro">Introduction to model distillation: Efficient knowledge transfer for AI applications</a></li>
<li><a href="https://minority-mindset.com/beyond-checklists-rethinking-how-we-measure-ai-safety/">Beyond Checklists: Rethinking How We Measure AI Safety – Minority...</a></li>

</ul>
</details>

**标签**: `#AI Safety`, `#Model Distillation`, `#Machine Learning`, `#Research`, `#Neural Networks`

---

<a id="item-2"></a>
## [零样本世界模型在视觉学习中实现人类规模的数据效率](https://i.redd.it/px240r8jkuvg1.png) ⭐️ 8.0/10

该论文提出了零样本世界模型（ZWM），当使用单个儿童的视觉经验（BabyZWM 数据集）进行训练时，无需任何任务特定训练，就能在多种视觉认知任务上达到最先进性能，实现了与人类发展效率相当的零样本学习。 这项工作显著缩小了 AI 与人类学习之间的数据效率差距，为构建更灵活、高效的 AI 系统提供了蓝图，这些系统可以从有限的人类规模数据中学习，从而降低计算成本并加速在机器人、自主系统和认知 AI 中的应用。 ZWM 基于三个设计原则：时间分解预测以分离外观与动态，通过近似因果推理进行零样本视觉认知结构提取，以及组合提取器以实现复杂推理，代码和数据集计划于 2026 年 5 月发布。

reddit · r/MachineLearning · FaeriaManic · Apr 18, 00:58

**背景**: AI 中的零样本学习指模型无需特定训练示例就能执行任务，通常利用预训练中的通用知识。世界模型是模拟环境以预测结果的 AI 系统，常用于强化学习中进行规划。视觉认知任务评估 AI 在感知和推理方面的能力，如物体识别或场景理解，模仿人类的认知过程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2604.10333v1">1 Overview. (A) The Zero-shot Visual World Model (ZWM) framework has three design principles: temporally-factored prediction to flexibly separate appearance from dynamics; zero-shot extraction of visual-cognitive structures from the predictor through approximate causal inference; and composing extractors together to achieve increasingly complex inference abilities. (B) After self-supervised pretraining, ZWM can perform diverse visual-cognitive tasks zero-shot, i.e., without any additional training or exampl</a></li>
<li><a href="https://github.com/awwkl/ZWM">GitHub - awwkl/ZWM: Zero-shot World Models Are ...</a></li>
<li><a href="https://arxiv.org/abs/2510.04141">[2510.04141] The Artificial Intelligence Cognitive Examination:</a></li>

</ul>
</details>

**标签**: `#AI`, `#Machine Learning`, `#Zero-shot Learning`, `#Computer Vision`, `#Data Efficiency`

---

<a id="item-3"></a>
## [Wasserstein 度量修复量化 Qwen3.6-35B-A3B GGUF 模型中的张量漂移问题](https://www.reddit.com/r/LocalLLaMA/comments/1sp2l72/qwen3635ba3buncensoredwassersteingguf/) ⭐️ 8.0/10

一位 Reddit 用户使用 Wasserstein 度量（W1）发现并修复了量化 Qwen3.6-35B-A3B GGUF 模型中 SSM 层的张量漂移问题，该方法在检测数值不稳定性方面比 Kullback-Leibler 散度更有效。修复专门针对三个 ssm_conv1d.weight 层（块 36-38），修正后的模型已发布在 Hugging Face 上。 这很重要，因为量化模型中的张量漂移会降低性能和可靠性，尤其是在对状态空间模型的长上下文记忆至关重要的 SSM 层中。基于 Wasserstein 的方法为量化问题提供了更强大的调试工具，可能提高各种量化 LLM 的稳定性，并使在资源受限部署中工作的开发者受益。 修复将受影响层的 Wasserstein 距离（W1）值从 0.0038-0.0040 降低到 0.0006-0.0009，而其他张量保持健康。修正后的模型基于 HauhauCS 的 Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive 版本，并推荐使用 Q4_K_P 量化以获得最佳性能。

reddit · r/LocalLLaMA · EvilEnginer · Apr 18, 16:42

**背景**: GGUF（GGML 通用格式）是一种在消费级硬件上运行大型语言模型的文件格式，通过压缩权重来减小文件大小并加速推理，但量化可能引入数值不稳定性。状态空间模型（SSM）是某些 Transformer 中用于处理长上下文序列的架构，其中 SSM 层（如 ssm_conv1d）管理状态转换。Wasserstein 度量（W1）是一种用于比较概率分布的数学工具，常在机器学习中用于测量数据分布或模型输出之间的差异。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wasserstein_metric">Wasserstein metric - Wikipedia</a></li>
<li><a href="https://willitrunai.com/blog/quantization-guide-gguf-explained">GGUF Quantization Explained — Q4_K_M vs Q5_K_M vs Q8: VRAM ...</a></li>
<li><a href="https://arxiv.org/abs/2405.21060">[2405.21060] Transformers are SSMs: Generalized Models and</a></li>

</ul>
</details>

**标签**: `#Quantization`, `#Numerical Stability`, `#LLM Optimization`, `#Wasserstein Metric`, `#Model Debugging`

---

<a id="item-4"></a>
## [xAI 将于下周发布 Grok Build 和 Grok CLI，进军 AI 编程代理市场](https://www.testingcatalog.com/exclusive-early-look-at-grok-computer-and-grok-build/) ⭐️ 8.0/10

xAI 计划于下周发布 Grok Build 和 Grok CLI，支持并行模式和竞技场模式等多代理协同功能，并同步推出名为 Grok Computer 的桌面客户端以扩展第三方服务集成。此外，xAI 已向 Grok Heavy 订阅用户开放 Grok 4.3 早期测试版，该版本提升了前端性能，将作为编程工具的核心底层。 此举使 xAI 进入快速发展的 AI 编程代理市场，通过先进的多代理协作和本地优先安全特性，可能加速软件开发进程。它将影响开发者和企业，提供集成工具以提升编码效率和系统互操作性。 Grok Build 是一款本地优先的 CLI 编码代理，在用户机器上安全运行，支持 8 个并行 AI 代理和竞技场模式，由 grok-code-fast-1 驱动，具有 70.8% 的 SWE-Bench 验证率和 256K 上下文长度。Grok Computer 通过新增的连接器层将代理能力扩展至第三方服务和系统底层。

telegram · zaihuapd · Apr 18, 05:40

**背景**: xAI 是一家以开发 Grok 而闻名的 AI 公司，Grok 是一款能够聊天、生成图像、编写代码并提供实时答案的 AI 助手。AI 编程代理是利用人工智能自动化编码任务的工具，通常基于大型语言模型。多代理协作涉及多个 AI 代理通过通信协议协同工作，以解决复杂问题，例如在软件开发中。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Grok_Build">Grok Build - Grokipedia</a></li>
<li><a href="https://grok.com/">Grok</a></li>
<li><a href="https://www.ibm.com/think/topics/multi-agent-collaboration">What is Multi-Agent Collaboration? | IBM</a></li>

</ul>
</details>

**标签**: `#AI Programming`, `#xAI`, `#Grok Build`, `#Multi-Agent Systems`, `#Software Development`

---

<a id="item-5"></a>
## [B-52 轰炸机星跟踪器中机电角度计算机的详细解析](https://www.righto.com/2026/04/B-52-star-tracker-angle-computer.html) ⭐️ 7.0/10

一篇技术文章深入探讨了 B-52 轰炸机星跟踪器导航系统中使用的机电角度计算机，详细介绍了其机械计算原理和历史背景。该文章解释了这种设备如何通过机电方式而非纯电子或数字方法执行天体导航计算。 这项分析很重要，因为它保存了数字计算机占据主导地位之前对军事导航至关重要的历史机电计算系统知识。了解这些机电系统有助于洞察 20 世纪中期航空技术的工程挑战和解决方案，展示了如何通过机械精度执行复杂计算。 星跟踪器的角度计算机使用机械组件执行天体导航计算，该系统能够在南北半球运行。值得注意的细节包括天文罗盘的螺旋搜索模式覆盖方位角±4°和高度角±2.5°，以及系统的赤纬限制为+90°至-47°，高度限制低至-6°。

hackernews · NelsonMinar · Apr 18, 16:26

**背景**: B-52 同温层堡垒是美国自 20 世纪 50 年代开始服役的远程战略轰炸机，其任务需要复杂的导航系统。像 Z3（1941 年完成）这样的机电计算机代表了早期计算技术，将电气输入与机械计算机制相结合。星跟踪器是使用恒星作为参考点来确定飞机位置和方向的天体导航系统，对于超出地面导航辅助设备范围的远程轰炸机尤为重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Boeing_B-52_Stratofortress">Boeing B - 52 Stratofortress - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Z3_(computer)">Z3 ( computer ) - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了对历史机电系统工程复杂性的钦佩，用户指出了与海军火力控制技术的联系，并赞赏了关于星跟踪器搜索模式的具体技术细节。几位评论者表示，看到工程师在数字计算普及之前如何用机械解决方案解决复杂问题，这让他们深受启发。

**标签**: `#electromechanical-computing`, `#aviation-history`, `#military-technology`, `#retrocomputing`, `#navigation-systems`

---

<a id="item-6"></a>
## [Qwen3.6-35B-A3B 解决了 Qwen3.5-27B 无法处理的编码问题](https://www.reddit.com/r/LocalLLaMA/comments/1soxyfi/qwen3635ba3b_solved_coding_problems_qwen3527b/) ⭐️ 7.0/10

一位开发者报告称，在开发预算应用程序时，Qwen3.6-35B-A3B 模型成功解决了 Qwen3.5-27B 模型无法处理的编码问题和错误，通常只需一到两次尝试即可完成。这一改进是在开发者针对先前模型已达到极限的具体问题测试新模型后观察到的。 这展示了 AI 辅助编码方面的切实进展，表明像 Qwen3.6-35B-A3B 这样更新、更大的模型可以克服先前版本的局限性，从而可能减少软件项目的技术债务并提高开发效率。它突显了本地 LLM 领域的持续竞争，其中模型的渐进式改进直接影响应用程序开发等实际应用。 这一比较基于对一款预算应用程序的实际测试，该应用涉及费用跟踪、动态预算和银行账户集成等功能。Qwen3.5-27B 模型使用了 Q4_K_M 量化版本，这可能会影响其性能，而 Qwen3.6-35B-A3B 模型则是全精度版本，不过两者都设计用于本地部署。

reddit · r/LocalLLaMA · simracerman · Apr 18, 13:40

**背景**: Qwen3.6 和 Qwen3.5 是阿里巴巴 Qwen 团队开发的大型语言模型系列，其中 27B 和 35B 等版本表示参数数量（以十亿计）。像 Q4_K_M 这样的量化方法通过将权重压缩到 4 位精度来减小模型大小，以实现高效的本地部署，但这可能会影响准确性。Reddit 上的 LocalLLaMA 社区专注于讨论和比较可用于本地运行的 AI 模型，以支持编码等实际应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/Qwen/Qwen3.6-35B-A3B">Qwen/Qwen3.6-35B-A3B · Hugging Face</a></li>
<li><a href="https://huggingface.co/bartowski/Qwen_Qwen3.5-27B-GGUF">bartowski/Qwen_Qwen3.5-27B-GGUF · Hugging Face</a></li>
<li><a href="https://news.smol.ai/issues/24-07-17-ainews-gemma-2-tops-rlocalllama-vibe-check">Gemma 2 tops /r/LocalLlama vibe check | AINews</a></li>

</ul>
</details>

**标签**: `#AI Models`, `#Coding`, `#LocalLLaMA`, `#Software Development`, `#Model Comparison`

---

<a id="item-7"></a>
## [Qwen3.6 在正确配置（如启用 'preserve_thinking'）后性能显著提升](https://i.redd.it/wq76z71k9wvg1.jpeg) ⭐️ 7.0/10

一位用户确认，在正确配置（如启用 'preserve_thinking'）后，Qwen3.6 在处理高要求任务时表现出显著的性能提升，可媲美 Opus 和 Codex 等高端模型。该模型在 M5 Max 128GB 内存、8 位量化、3K PP 的硬件上高效运行，在 oMLX + Pi.dev 上实现了高速处理。 这很重要，因为它凸显了 Qwen3.6 作为专有模型的成本效益本地替代品的潜力，使开发者和研究人员更容易使用先进 AI。对配置的强调突出了优化在最大化实际应用性能中的重要性，这可能加速 AI/ML 社区的采用。 性能提升特别在启用 'preserve_thinking' 时被注意到，这是一个有助于保留推理令牌以提高效率的配置参数。用户在 M5 Max 128GB 内存、8 位量化、3K PP 的硬件上测试，在 oMLX + Pi.dev 上实现了 100 TG，表明强大的硬件兼容性和速度。

reddit · r/LocalLLaMA · onil_gova · Apr 18, 06:37

**背景**: Qwen3.6 是阿里巴巴集团 Qwen 团队开发的大型语言模型系列，提供多模态混合思维能力，支持 256K 上下文和 201 种语言。'Preserve_thinking' 是一个与保留推理内容相关的配置参数，类似于 Claude 4.5 等模型中的功能，可提高缓存效率和令牌管理。oMLX 是一个框架，但在此上下文中，它可能指运行 AI 模型的工具或环境，尽管搜索结果未提供具体细节。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/QwenLM/Qwen3.6">GitHub - QwenLM/Qwen3.6: Qwen3.6 is the large language model series developed by Qwen team, Alibaba Group. · GitHub</a></li>
<li><a href="https://medium.com/@mkteam/thinking-mode-in-claude-4-5-all-you-need-to-know-353235942182">Thinking mode in Claude 4.5: All You need to Know - Medium</a></li>
<li><a href="https://unsloth.ai/docs/models/qwen3.6">Qwen3.6 - How to Run Locally | Unsloth Documentation</a></li>

</ul>
</details>

**标签**: `#AI`, `#LLM`, `#LocalLLaMA`, `#Performance`, `#Configuration`

---

<a id="item-8"></a>
## [RTX 5070 Ti 通过 --n-cpu-moe 优化实现 Qwen3.6-35B-A3B 模型 79 令牌/秒性能](https://www.reddit.com/r/LocalLLaMA/comments/1sor55y/rtx_5070_ti_9800x3d_running_qwen3635ba3b_at_79_ts/) ⭐️ 7.0/10

一位用户展示了在消费级硬件（RTX 5070 Ti + Ryzen 9800X3D）上运行 Qwen3.6-35B-A3B MoE 模型，通过 llama.cpp 中的 --n-cpu-moe 20 标志实现了 79 令牌/秒的生成速度，相比标准的 --cpu-moe 方法提升了 54% 的性能。 这项优化通过显著提升 VRAM 利用率和推理速度，使得大型 MoE 模型在消费级硬件上更加可用，让拥有 16GB GPU 的用户能够高效运行 22GB+ 的模型，无需昂贵的硬件升级。 --n-cpu-moe 20 标志将前 20 层的专家保留在 CPU 上，而将剩余层放在 GPU 上，使用了 12.7GB 的 VRAM，相比之下 --cpu-moe 仅使用 3.5GB；通过 -np 标志实现 128K 上下文长度时性能损失极小。

reddit · r/LocalLLaMA · marlang · Apr 18, 07:40

**背景**: 混合专家（MoE）模型将神经网络划分为专门的“专家”子网络，这些子网络选择性激活，在保持大量参数的同时降低计算成本。GGUF 是一种量化格式，专为在消费级硬件上高效部署大语言模型而设计；llama.cpp 是一个开源推理框架，支持多种优化标志以在本地运行模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>
<li><a href="https://www.ibm.com/think/topics/gguf-versus-ggml">GGUF versus GGML | IBM</a></li>

</ul>
</details>

**标签**: `#LocalLLM`, `#Hardware Optimization`, `#MoE Models`, `#llama.cpp`, `#AI Performance`

---

<a id="item-9"></a>
## [苹果 App Store 诈骗应用泛滥，削弱其安全性辩护](https://appleinsider.com/articles/26/04/17/app-store-scams-are-getting-worse-and-apple-isnt-doing-enough?utm_source=rss) ⭐️ 7.0/10

苹果 App Store 的审核机制被指存在严重漏洞，导致大量诈骗应用绕过监管。近期，一款虚假加密货币应用在下架前已诈骗用户约 950 万美元，苹果从中赚取了 142.5 万至 285 万美元的佣金。 诈骗应用的激增正在瓦解苹果维持 App Store 垄断地位的核心论据，该论据主要依赖保护用户安全的说法来合理化其抽成比例并抵制第三方商店。这种情况加剧了苹果在全球反垄断调查中的法律压力，并引发对其安全承诺有效性的担忧。 2026 年第一季度，App Store 的应用提交量同比增长 84%，达到 23.58 万个，但审核团队规模疑似未同步增长，导致“先通过后变脸”及冒名应用频发。苹果对此类安全漏洞的质疑多以重复性公关辞令回应，未提出实质性整改方案。

telegram · zaihuapd · Apr 18, 03:25

**背景**: 苹果的 App Store 审核流程旨在评估所有应用、更新和应用内购买，以确保安全可信的用户体验，如其官方指南所述。iOS 采用应用沙盒作为关键安全功能，将每个应用隔离在安全环境中，以保护用户数据免受恶意或编写不当的应用侵害。公证是 macOS 软件的自动化安全扫描流程，不同于手动 App Store 审核，后者侧重于更广泛的合规性，包括安全、性能和业务方面。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.apple.com/distribute/app-review/">App Review - Distribute - Apple Developer</a></li>
<li><a href="https://medium.com/@ios_guru/app-sandboxing-for-implementing-security-and-privacy-697641286c2e">App Sandboxing for Implementing Security and Privacy in iOS ...</a></li>
<li><a href="https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution">Notarizing macOS software before distribution - Apple Developer</a></li>

</ul>
</details>

**标签**: `#App Security`, `#Platform Governance`, `#Antitrust`, `#Mobile Ecosystems`, `#Fraud Prevention`

---

<a id="item-10"></a>
## [倒闭企业正将旧 Slack 聊天记录和邮件数据出售给 AI 训练](https://www.reddit.com/r/technology/comments/1sow19a/failed_companies_are_selling_old_slack_chats_and/) ⭐️ 7.0/10

部分倒闭或濒临破产的科技企业正在出售其保存的旧 Slack 聊天记录和电子邮件档案，这些数据被用于 AI 模型训练。此举引发隐私专家担忧，相关数据可能包含员工个人隐私、商业机密及客户敏感信息。 这一现象反映出 AI 训练数据需求持续增长，已开始向企业历史数据资产延伸，带来了新的隐私和安全风险。它引发了关于数据所有权、企业道德以及公司清算数字资产时的法律合规性的重要问题。 目前数据交易的具体规模和定价尚不清楚，但它们代表了企业通信数据的二级市场。Slack 允许组织自定义数据保留设置，但一旦数据被存档，其在清算过程中的处置可能缺乏明确监管。

telegram · zaihuapd · Apr 18, 14:55

**背景**: 大型语言模型（LLMs）需要大量文本数据进行训练，通常来源于公开可用的互联网内容。Slack 是广泛使用的工作场所通信平台，公司可以自定义数据保留策略来控制消息和文件的存储时间。当公司破产时，包括数字数据在内的资产可能会通过资产出售进行清算以偿还债权人，遵循既定的清算流程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://slack.com/help/articles/203457187-Customize-data-retention-in-Slack">Customize data retention in Slack</a></li>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>
<li><a href="https://rabin.com/services/asset-recovery-services/liquidation-process-asset/">Asset Liquidation Process | Rabin Worldwide</a></li>

</ul>
</details>

**标签**: `#AI Ethics`, `#Data Privacy`, `#Corporate Data`, `#AI Training`, `#Technology News`

---