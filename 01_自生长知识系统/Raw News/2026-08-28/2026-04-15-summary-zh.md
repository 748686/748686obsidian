---
layout: default
title: "Horizon Summary: 2026-04-15 (ZH)"
date: 2026-04-15
lang: zh
---

> From 34 items, 15 important content pieces were selected

---

1. [OpenSSL 4.0.0 发布，引入新加密算法和破坏性变更](#item-1) ⭐️ 9.0/10
2. [OpenAI 发布 GPT-5.4-Cyber 并扩展网络安全可信访问计划](#item-2) ⭐️ 8.0/10
3. [AI 将网络安全转变为工作量证明经济模型](#item-3) ⭐️ 8.0/10
4. [HALO-Loss 让神经网络能够通过数学定义的“我不知道”类别来拒绝预测。](#item-4) ⭐️ 8.0/10
5. [MiniMax M2.7 GGUF 调查揭示 llama.cpp 中普遍存在的 NaN 问题](#item-5) ⭐️ 8.0/10
6. [将超过 1000 亿参数的大模型蒸馏至 40 亿参数以下的技术](#item-6) ⭐️ 8.0/10
7. [斯坦福大学 2026 年 AI 指数报告显示中美 AI 性能差距基本消失，AI 加速全球普及。](#item-7) ⭐️ 8.0/10
8. [Anthropic 推出 Claude Code Routines，实现 LLM 工作流自动化](#item-8) ⭐️ 7.0/10
9. [小米 12 Pro 被改造成 24/7 无头 AI 服务器，通过 Ollama 运行 Gemma4](#item-9) ⭐️ 7.0/10
10. [基于 KL 散度的 Qwen3.5-9B 量化方法更新对比](#item-10) ⭐️ 7.0/10
11. [百度在 Hugging Face 上发布 ERNIE-Image 多模态 AI 模型，供公众访问使用。](#item-11) ⭐️ 7.0/10
12. [大语言模型自主调优 llama.cpp 参数，实现最高 54% 的生成速度提升](#item-12) ⭐️ 7.0/10
13. [多家主流媒体因 AI 训练担忧屏蔽互联网档案馆爬虫，记者联名支持数字保存](#item-13) ⭐️ 7.0/10
14. [亚马逊发布机载卫星天线 Leo Aviation Antenna，与星链竞争机上 Wi-Fi 市场](#item-14) ⭐️ 7.0/10
15. [谷歌搜索更新反垃圾政策，打击后退按钮劫持行为，违规站点将面临降权。](#item-15) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [OpenSSL 4.0.0 发布，引入新加密算法和破坏性变更](https://lwn.net/Articles/1067622/) ⭐️ 9.0/10

OpenSSL 4.0.0 于 2026 年 4 月 14 日发布，增加了对新加密算法的支持，并引入了多项不兼容的变更，例如移除 SSLv3 支持和标准化十六进制转储宽度。此主要版本更新将支持到 2027 年 5 月 14 日。 此版本具有重要意义，因为 OpenSSL 是一个广泛使用的加密库，支撑着许多系统和应用程序的安全通信，其破坏性变更可能需要更新依赖软件以保持兼容性和安全性。移除 SSLv3 等过时协议通过消除漏洞增强了安全性，但可能影响仍依赖这些协议的遗留系统。 值得注意的变更包括移除自 2015 年起已弃用的 SSLv2 Client Hello 和 SSLv3 支持，以及默认禁用 TLS 中已弃用的椭圆曲线，除非显式启用。此版本还将十六进制转储宽度标准化为签名 24 字节和其他数据 16 字节，以保持在 80 字符限制内。

rss · LWN.net · Apr 14, 15:36

**背景**: OpenSSL 是一个开源软件库，为网络上的安全通信提供加密功能，广泛用于 Web 服务器和操作系统等应用程序。它支持 TLS、DTLS 和 QUIC 等协议，并包含一个可独立使用的通用加密库（libcrypto）。像 4.0.0 这样的主要版本发布通常会引入破坏性变更以增强安全性和现代化代码库，要求用户调整其集成方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/OpenSSL">OpenSSL - Wikipedia</a></li>
<li><a href="https://openssl-communities.org/d/HKTgiLuU/openssl-4-0-page-needed">OpenSSL 4.0 page needed</a></li>

</ul>
</details>

**标签**: `#OpenSSL`, `#Cryptography`, `#Security`, `#Software Updates`, `#Libraries`

---

<a id="item-2"></a>
## [OpenAI 发布 GPT-5.4-Cyber 并扩展网络安全可信访问计划](https://simonwillison.net/2026/Apr/14/trusted-access-openai/#atom-everything) ⭐️ 8.0/10

OpenAI 推出了 GPT-5.4-Cyber，这是其 GPT-5.4 模型的微调版本，专门针对防御性网络安全用例设计，同时正在扩展其网络安全可信访问计划，允许经过验证的用户以更少限制的方式访问这些模型。 这代表了 OpenAI 对网络安全专用 AI 领域日益激烈竞争的战略回应，特别是在 Anthropic 最近发布 Claude Mythos 之后，此举可能加速 AI 驱动的防御工具的采用，同时也引发了关于访问控制和行业动态的讨论。 GPT-5.4-Cyber 被描述为具有'网络许可'特性，比标准模型具有更少的能力限制，但访问需要通过 Persona 的身份验证或针对高级工具的额外申请流程，形成了一个分层访问系统。

rss · Simon Willison · Apr 14, 21:23

**背景**: 像 GPT-5.4 这样的大型语言模型是在海量文本数据上训练的 AI 系统，能够生成类似人类的响应。微调涉及在专门数据集上进行额外训练，使这些通用模型适应网络安全等特定领域。像 Persona 这样的身份验证服务通过文档处理帮助组织验证用户身份，同时满足监管要求。网络安全 AI 领域竞争日益激烈，各公司都在开发用于防御应用的专用模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.reuters.com/technology/openai-unveils-gpt-54-cyber-week-after-rivals-announcement-ai-model-2026-04-14/">OpenAI unveils GPT-5.4-Cyber a week after rival's announcement of AI model | Reuters</a></li>
<li><a href="https://openai.com/index/scaling-trusted-access-for-cyber-defense/">Trusted access for the next era of cyber defense | OpenAI</a></li>
<li><a href="https://en.wikipedia.org/wiki/Persona_(identity_verification_service)">Persona (identity verification service) - Wikipedia</a></li>

</ul>
</details>

**标签**: `#AI`, `#Cybersecurity`, `#OpenAI`, `#Machine Learning`

---

<a id="item-3"></a>
## [AI 将网络安全转变为工作量证明经济模型](https://simonwillison.net/2026/Apr/14/cybersecurity-proof-of-work/#atom-everything) ⭐️ 8.0/10

英国 AI 安全研究所对 Anthropic 的 Claude Mythos AI 模型的评估证实了其卓越的漏洞检测能力，随着投入更多计算代币（和资金），性能会提升，从而将网络安全构建为一个工作量证明模型，其中安全性与经济投入成正比。 这一转变可能从根本上改变网络安全的经济学，为组织大力投资 AI 驱动的安全审查创造强烈激励，可能使系统更具韧性，但也增加了成本，并将安全工作集中在强大的 AI 模型周围。 分析强调，在此模型下，开源库变得更有价值，因为对其的安全投资可以被所有用户共享，这抵制了可能削弱开源项目的低成本'氛围编码'替代趋势。

rss · Simon Willison · Apr 14, 19:41

**背景**: 工作量证明（PoW）是一个最初为防止网络滥用（如垃圾邮件）而提出的概念，要求服务请求者付出计算努力；它在比特币等区块链系统中广为人知，矿工通过解决谜题来验证交易。Claude Mythos 是 Anthropic 的高级 AI 模型，设计用于包括网络安全在内的高性能任务，其能力已由英国 AI 安全研究所独立评估，以评估其对安全实践的影响。英国 AI 安全研究所对 AI 模型进行部署前评估，以了解其风险和益处，重点关注网络安全和交互危害等领域。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Proof_of_work">Proof of work - Wikipedia</a></li>
<li><a href="https://em360tech.com/tech-articles/what-claude-mythos-everything-you-need-know-about-anthropics-most-powerful-ai-model">What is Claude Mythos? | Anthropic’s “Most Powerful” AI</a></li>
<li><a href="https://www.aisi.gov.uk/blog/pre-deployment-evaluation-of-openais-o1-model">Pre-Deployment evaluation of OpenAI’s o1 model | AISI Work</a></li>

</ul>
</details>

**标签**: `#AI Security`, `#Cybersecurity`, `#Proof of Work`, `#Claude Mythos`, `#Economic Incentives`

---

<a id="item-4"></a>
## [HALO-Loss 让神经网络能够通过数学定义的“我不知道”类别来拒绝预测。](https://www.reddit.com/r/MachineLearning/comments/1skzuhd/i_dont_know_teaching_neural_networks_to_abstain/) ⭐️ 8.0/10

研究人员开源了 HALO-Loss，这是一种新颖的损失函数，可替代交叉熵，通过在潜在空间中创建一个数学定义的“我不知道”类别，使神经网络能够拒绝预测。这种即插即用的替代方案使用欧几里得距离而非无约束的点积，将最大置信度限制在距离学习原型的有限范围内。 这解决了神经网络中的一个基本安全问题，即模型在面对垃圾数据或分布外数据时会自信地产生幻觉，有望提升医疗和自动驾驶等关键应用中的 AI 安全性。该方法消除了分布外检测与基础准确性之间的典型权衡，使安全增强更加实用。 在 CIFAR-10/100 上的测试显示，基础准确性没有下降（在 CIFAR-10 上甚至提高了 0.23%），校准误差（ECE）从约 8% 降至 1.5%，远分布外数据的误报率（FPR@95）减少了一半以上（例如，在 SVHN 上从 22.08% 降至 10.27%）。零参数的“拒绝类别”直接固定在潜在空间的原点，无需额外的架构更改。

reddit · r/MachineLearning · 4rtemi5 · Apr 14, 05:45

**背景**: 交叉熵损失是机器学习中的标准函数，用于衡量预测概率分布与真实分布之间的差异，但它迫使模型将特征无限推离原点以实现零损失，从而产生一个锯齿状的潜在空间，没有数学上合理的位置来处理不确定的预测。潜在空间指的是数据的压缩表示，其中保留了基本特征，使模型能够发现模式和关系。分布外（OOD）检测涉及识别与训练分布不同的数据，这对 AI 安全至关重要，但通常以降低基础准确性为代价。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Cross-entropy">Cross-entropy - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Latent_space">Latent space - Wikipedia</a></li>

</ul>
</details>

**标签**: `#machine-learning`, `#neural-networks`, `#ai-safety`, `#loss-functions`, `#out-of-distribution-detection`

---

<a id="item-5"></a>
## [MiniMax M2.7 GGUF 调查揭示 llama.cpp 中普遍存在的 NaN 问题](https://www.reddit.com/r/LocalLLaMA/comments/1slk4di/minimax_m27_gguf_investigation_fixes_benchmarks/) ⭐️ 8.0/10

一项技术调查发现，Hugging Face 上 21%-38% 的 GGUF 模型存在 NaN（非数字）问题，根本原因在于 llama.cpp 在困惑度评估时发生溢出。研究人员确定了特定的问题量化类型（Q5_K 和 Q4_K）和块（32 和 311），而较小的 I 量化类型如 IQ4_XS 和 IQ3_XXS 则未受影响。 这一发现非常重要，因为它揭示了一个影响 Hugging Face 上大量量化模型的普遍错误，可能损害这些模型在本地 AI 部署中的可靠性。它强调了开源 LLM 生态系统中严格测试的重要性，并可能推动 llama.cpp 等支持许多本地 AI 应用的流行工具的修复。 该问题特别影响困惑度评估期间的 Q5_K 和 Q4_K 量化类型，其中块 32 和块 311 被确定为问题区域。有趣的是，较低比特的量化如 Q2_K_XL 未产生 NaN，而中等大小的量化如 Q4_K_XL 却产生了，这表明量化大小与溢出错误之间存在非线性关系。

reddit · r/LocalLLaMA · danielhanchen · Apr 14, 20:12

**背景**: GGUF（GPT 生成统一格式）是由 llama.cpp 团队创建的二进制文件格式，用于将大型语言模型存储在单个优化文件中，以实现高效的本地部署。量化通过降低权重的精度来减小模型大小，其中 Q4_K 和 Q5_K 等类型代表平衡大小和准确性的特定量化方法。llama.cpp 是一个用于本地运行 LLM 的开源 C++ 实现，广泛用于 GGUF 模型的推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://imthadhahamed0205.medium.com/what-is-gguf-the-format-powering-local-ai-models-like-llama-and-mistral-9bfb23be7612">What is GGUF ? The Format Powering Local AI Models like... | Medium</a></li>
<li><a href="https://gerfficient.com/en/home/model-quantization">LLM Model Formats, Conversion and Quantization | Gerfficient</a></li>

</ul>
</details>

**标签**: `#quantization`, `#llama.cpp`, `#model-debugging`, `#hugging-face`, `#perplexity`

---

<a id="item-6"></a>
## [将超过 1000 亿参数的大模型蒸馏至 40 亿参数以下的技术](https://i.redd.it/ytl9389gp4vg1.png) ⭐️ 8.0/10

近期进展使得能够将超过 1000 亿参数的大型语言模型蒸馏至 40 亿参数以下的小型模型，重点关注效率和可访问性。例如，TRL 现在支持使用 1000 亿以上参数的教师模型进行策略蒸馏，训练速度提升高达 40 倍。 这很重要，因为它通过降低计算和内存需求，使先进 AI 能力更易于获取，能够在消费级硬件和资源受限的环境中部署。这符合 AI 效率和民主化的增长趋势，可能降低成本并扩展实际应用。 关键细节包括使用知识蒸馏，即较小的学生模型模仿较大的教师模型的输出或特征，以及如策略蒸馏等加速训练的技术。局限性可能涉及性能权衡，因为蒸馏后的模型可能无法在所有任务中完全匹配教师的准确性。

reddit · r/LocalLLaMA · cmpatino_ · Apr 14, 10:01

**背景**: 知识蒸馏是一种模型压缩技术，其中较小的学生模型被训练来复制较大的教师模型的行为，使用更少的计算和内存。大型语言模型（LLMs）是拥有数十亿参数的 AI 模型，用于文本生成和理解等任务。参数减少方法，如蒸馏，旨在使这些模型更高效，并能在有限硬件上部署。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Knowledge_distillation">Knowledge distillation - Wikipedia</a></li>
<li><a href="https://huggingface.co/spaces/HuggingFaceTB/trl-distillation-trainer">Distilling 100B+ Models 40x Faster with TRL - Hugging Face</a></li>
<li><a href="https://www.reddit.com/r/LocalLLM/comments/1q4brqd/poll_whats_your_favorite_local_model_parameter/">Poll - what's your favorite local model parameter count? : r/LocalLLM</a></li>

</ul>
</details>

**社区讨论**: 社区讨论强调了对实际应用和挑战的兴趣，用户辩论大多数现实世界用例是否需要巨大模型，并表达了对训练大模型的 GPU 成本的担忧。还有关于偏好本地模型参数数量的投票参与，反映了对效率和可访问性的关注。

**标签**: `#model-distillation`, `#AI-efficiency`, `#large-language-models`, `#machine-learning`, `#parameter-reduction`

---

<a id="item-7"></a>
## [斯坦福大学 2026 年 AI 指数报告显示中美 AI 性能差距基本消失，AI 加速全球普及。](https://hai.stanford.edu/ai-index/2026-ai-index-report) ⭐️ 8.0/10

斯坦福大学发布《2026 年 AI 指数报告》，指出中美 AI 模型性能差距已基本消失，美国 Anthropic 的领先优势仅剩 2.7%。中国在 AI 领域表现强劲，在论文发表、专利产出、工业机器人装机量及公共 AI 超算数量上均位居全球第一，且职场 AI 使用率超过 80%，远高于 58%的全球平均水平。 这份报告揭示了全球 AI 格局的重大转变，中国的快速进步挑战了美国的领先地位，可能重塑技术政策、经济竞争力和国际 AI 治理。AI 的加速普及和投资增长突显了其对全球产业和就业的变革性影响。 报告显示，全球超 90%的顶尖模型在多项人类竞赛中表现优异，但呈现出“锯齿前沿”的能力不均现象，同时全球 AI 算力三年增长 30 倍，企业投资翻倍至 5817 亿美元。然而，AI 对就业的冲击已显现，22 至 25 岁软件开发者岗位自 2024 年起下滑 20%，且进入美国的 AI 研究人员数量在过去一年骤降 80%。

telegram · zaihuapd · Apr 14, 05:09

**背景**: AI 指数报告是斯坦福大学以人为本人工智能研究所（HAI）的年度出版物，追踪并可视化人工智能趋势数据，包括模型性能、研究成果和经济影响。Anthropic 是一家美国 AI 安全公司，以开发 Claude 系列大语言模型而闻名，而 DeepSeek 是一家成立于 2023 年的中国 AI 公司，凭借 DeepSeek-R1 等模型崭露头角。这些报告为比较各国和各领域的 AI 进展提供了基准。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_(language_model)">Claude (language model) - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>
<li><a href="https://hai.stanford.edu/ai-index/2025-ai-index-report">The 2025 AI Index Report | Stanford HAI</a></li>

</ul>
</details>

**标签**: `#AI Research`, `#Global AI Trends`, `#Technology Policy`, `#Economic Impact`, `#Machine Learning`

---

<a id="item-8"></a>
## [Anthropic 推出 Claude Code Routines，实现 LLM 工作流自动化](https://code.claude.com/docs/en/routines) ⭐️ 7.0/10

Anthropic 推出了 Claude Code Routines 功能，目前处于研究预览阶段，允许开发者使用大语言模型创建可重复的自动化工作流。这些例程可以按计划触发、通过 API 调用触发，或响应 GitHub 活动等事件触发。 这标志着大语言模型向生产工作流实用化迈出了重要一步，从一次性交互转向计划性和事件驱动的自动化。通过减少重复编码任务中的人工干预，该功能可能加速 AI 在软件开发中的采用。 该功能目前处于研究预览阶段，可与 Claude Code 订阅配合使用，但用户注意到文档与实现之间存在关于可用 GitHub 触发器的差异。社区讨论强调了性能可靠性问题以及对第三方集成的服务条款解释的担忧。

hackernews · matthieu_bl · Apr 14, 16:54

**背景**: Claude Code 是 Anthropic 的 AI 驱动编码助手，帮助开发者完成代码生成、调试和文档编写等任务。LLM 工作流自动化指的是将大语言模型任务嵌入自动化流程，这代表了从机器人流程自动化向代理流程自动化的转变，即由 LLM 编排工作流。Anthropic 的服务条款区分了消费者服务和商业服务，API 使用通常属于商业条款范畴。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://9to5mac.com/2026/04/14/anthropic-adds-repeatable-routines-feature-to-claude-code-heres-how-it-works/">Anthropic adds routines to redesigned Claude Code, here's how it works - 9to5Mac</a></li>
<li><a href="https://arxiv.org/abs/2411.05451">[2411.05451] WorkflowLLM: Enhancing Workflow Orchestration ... GitHub - Skyvern-AI/skyvern: Automate browser based workflows ... LLM4Workflow: An LLM-based Automated Workflow Model ... LLM Automation: Top 7 Tools & 8 Case Studies How to Build Workflows with Prefect and LLM Frameworks ...</a></li>
<li><a href="https://privacy.claude.com/en/articles/9190861-terms-of-service-updates">Terms of Service Updates | Anthropic Privacy Center</a></li>

</ul>
</details>

**社区讨论**: 社区情绪复杂，用户对 LLM 提供商功能持久性和性能一致性的信任表示担忧。具体讨论集中在第三方集成的服务条款解释、Claude 模型近期性能下降问题，以及文档记载与实际可用的 GitHub 事件触发器之间的差异。

**标签**: `#AI`, `#LLM`, `#Automation`, `#Developer Tools`, `#Anthropic`

---

<a id="item-9"></a>
## [小米 12 Pro 被改造成 24/7 无头 AI 服务器，通过 Ollama 运行 Gemma4](https://i.redd.it/fo3jf5vk85vg1.jpeg) ⭐️ 7.0/10

一位用户成功将小米 12 Pro 智能手机改造成专用本地 AI 服务器，通过刷入 LineageOS 移除 Android 界面冗余，实现自定义散热管理和电池保护系统，并通过 Ollama 部署 Gemma4 作为局域网可访问的 API。该设置包括在 45°C 触发外部冷却的自定义守护进程，以及将充电限制在 80%以支持 24/7 运行的脚本。 这展示了搭载骁龙 8 Gen 1 等强大芯片的消费级移动硬件如何被重新用于边缘 AI 计算，可能降低本地 LLM 部署的门槛，并支持注重隐私的应用。它展示了在移动硬件连续运行中散热管理和电池寿命的实用解决方案，可能激发边缘 AI 生态系统中类似项目的灵感。 该设置通过移除 Android 界面组件，为 LLM 计算实现了约 9GB 的可用内存，并通过手动编译的 wpa_supplicant 在无头模式下保持网络连接。外部冷却模块通过 Wi-Fi 智能插座控制，而电池保护脚本有助于防止在连续运行期间的电池退化。

reddit · r/LocalLLaMA · Aromatic_Ad_7557 · Apr 14, 11:44

**背景**: Ollama 是一个简化本地运行大型语言模型的开源工具，支持无需云依赖的隐私优先 AI 应用。Gemma4 是 Google 于 2026 年 4 月发布的最新开源 LLM 系列，提供文本和图像输入的多模态能力。wpa_supplicant 是一个处理 WPA/WPA2 无线认证的 Linux 守护进程，常用于无头系统中的命令行网络连接。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://learn.microsoft.com/en-us/agent-framework/agents/providers/ollama">Ollama | Microsoft Learn</a></li>
<li><a href="https://en.wikipedia.org/wiki/Gemma_(language_model)">Gemma (language model)</a></li>
<li><a href="https://thelinuxcode.com/how-to-use-wpa-supplicant/">How to Use WPA_Supplicant: An In-Depth Guide - TheLinuxCode</a></li>

</ul>
</details>

**标签**: `#Local AI`, `#Hardware Hacking`, `#Ollama`, `#Mobile Computing`, `#Edge Computing`

---

<a id="item-10"></a>
## [基于 KL 散度的 Qwen3.5-9B 量化方法更新对比](https://www.reddit.com/r/LocalLLaMA/comments/1sl59qq/updated_qwen359b_quantization_comparison/) ⭐️ 7.0/10

一篇 Reddit 帖子发布了针对 Qwen3.5-9B 模型的社区 GGUF 量化方法的定量对比，使用 KL 散度（KLD）来评估量化版本相对于原始 BF16 基准的忠实度。该分析根据 KLD 分数对量化方法（如 eaddario/Qwen3.5-9B-Q8_0 和 unsloth/Qwen3.5-9B-UD-Q8_K_XL）进行排名，分数越低表示保真度越高。 这很重要，因为它为选择量化方法提供了数据驱动的依据，帮助用户选择能最小化信息损失的文件，而不是依赖可用性或猜测。这支持了在消费级硬件上优化大型语言模型以提高效率的广泛趋势，有利于在本地部署模型的开发者和研究人员。 该对比使用 KL 散度作为忠实度的度量指标，它比困惑度（PPL）更稳定，因为它依赖于基准分布而非数据集。KLD 分数低于 0.01 的量化方法（如 eaddario/Qwen3.5-9B-Q8_0，KLD 为 0.001198）被突出显示为最忠实的，但该分析仅限于 Qwen3.5-9B 模型，可能不适用于其他模型。

reddit · r/LocalLLaMA · TitwitMuffbiscuit · Apr 14, 10:55

**背景**: 量化是一种降低模型权重精度（例如从 32 位降至 8 位）的技术，以减少内存使用并加速推理，但通常以轻微精度损失为代价。GGUF 是一种存储量化模型的统一格式，支持如 Q8_0 等量化级别，以平衡大小和性能。KL 散度衡量量化模型的概率分布与原始模型的差异，值越低表示信息损失越少。BF16 是一种 16 位浮点格式，在此上下文中用作高精度比较的基准。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ggufloader.github.io/what-is-gguf.html">What is GGUF? Complete Guide to GGUF Format & Quantization (2025)</a></li>
<li><a href="https://encord.com/blog/kl-divergence-in-machine-learning/">KL Divergence in Machine Learning | Encord</a></li>
<li><a href="https://www.emergentmind.com/topics/bf16-precision">BF 16 Precision in AI Training</a></li>

</ul>
</details>

**标签**: `#quantization`, `#model-evaluation`, `#Qwen`, `#LLM-optimization`, `#machine-learning`

---

<a id="item-11"></a>
## [百度在 Hugging Face 上发布 ERNIE-Image 多模态 AI 模型，供公众访问使用。](https://huggingface.co/baidu/ERNIE-Image) ⭐️ 7.0/10

百度已将其 ERNIE-Image 多模态 AI 模型发布在 Hugging Face 平台上，使其可供公众使用和实验。此次发布发生在近期，由模型在 Hugging Face 上的可用性表明，但内容中未提供具体版本或日期。 此次发布具有重要意义，因为它提高了先进多模态 AI 技术的可访问性，可能加速计算机视觉和自然语言处理等领域的研究与开发。这也反映了百度等主要 AI 公司日益增长的趋势，即将其模型在开放平台上提供，促进全球 AI 社区的协作与创新。 该模型托管在 Hugging Face 上，这是一个分享 AI 模型的流行平台，允许用户通过 API 访问或下载供本地使用。然而，给定内容中未提供具体技术细节，如模型大小、性能基准或限制，因此用户可能需要参考 Hugging Face 页面或百度的文档以获取更多信息。

reddit · r/LocalLLaMA · adefa · Apr 14, 15:23

**背景**: 多模态 AI 模型整合了多种类型的数据，如图像和文本，以执行视觉问答或图像生成等任务，增强了 AI 理解和与世界交互的能力。Hugging Face 是一个广泛使用的平台，提供分享和部署机器学习模型的工具和社区，使开发者更容易访问和使用先进的 AI 技术。百度的 ERNIE 系列包括多种 AI 模型，ERNIE-Image 是其多模态产品的一部分，基于大语言模型和计算机视觉的进展构建。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ernie.baidu.com/blog/posts/ernie-4.5-vl-28b-a3b-thinking/">ERNIE-4.5-VL-28B-A3B-Thinking: A Breakthrough in Multimodal AI</a></li>
<li><a href="https://en.wikipedia.org/wiki/Hugging_Face">Hugging Face - Wikipedia</a></li>
<li><a href="https://blog.roboflow.com/multimodal-models/">Multimodal Models and Computer Vision: A Deep Dive</a></li>

</ul>
</details>

**标签**: `#AI`, `#multimodal-models`, `#computer-vision`, `#hugging-face`, `#deep-learning`

---

<a id="item-12"></a>
## [大语言模型自主调优 llama.cpp 参数，实现最高 54% 的生成速度提升](https://www.reddit.com/r/LocalLLaMA/comments/1sl85r5/the_llm_tunes_its_own_llamacpp_flags_54_toks_on/) ⭐️ 7.0/10

开发者发布了 llm-server 的第二版，引入了 --ai-tune 参数，使大语言模型能够在循环中自主优化 llama.cpp 的配置参数，并缓存找到的最快配置。该方法在 Qwen3.5-27B Q4_K_M 等模型上实现了最高 54% 的生成速度提升，从每秒 25.94 个 token 提高到 40.05 个。 这代表了一种新颖的 AI 优化方法，即模型自身调优其运行时参数，有望实现本地大语言模型部署的性能调优自动化。它可以显著减少在不同硬件和模型组合中手动优化推理设置的工作量，使高性能本地大语言模型的使用更加便捷。 该系统通过将 llama-server --help 的输出作为上下文输入到大语言模型调优循环中，自动整合来自 llama.cpp 更新的新参数。性能提升因模型而异，Qwen3.5-27B 显示出最大的改进，而 gemma-4-31B 的提升较为有限，表明其效果取决于具体的模型特性。

reddit · r/LocalLLaMA · raketenkater · Apr 14, 13:05

**背景**: llama.cpp 是一个用于本地运行大语言模型的开源 C++ 实现，提供多种参数以在不同硬件上优化性能。量化后缀如 Q4_K_M 指的是特定的 4 位量化方法，可在保持精度的同时减小模型大小。像 llama-optimus 这样的工具使用贝叶斯优化来自动调优 llama.cpp 参数，但这种新方法使用大语言模型自身作为调优器。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/ggml-org/llama.cpp/discussions/14191">Optimizing llama.cpp flags for max performance; tuning with ML Optuna-library (llama‑optimus) · ggml-org/llama.cpp · Discussion #14191</a></li>
<li><a href="https://pypi.org/project/llama-optimus/">llama-optimus · PyPI</a></li>
<li><a href="https://medium.com/@paul.ilvez/demystifying-llm-quantization-suffixes-what-q4-k-m-q8-0-and-q6-k-really-mean-0ec2770f17d3">Demystifying LLM Quantization Suffixes: What Q4_K_M, Q8_0 ...</a></li>

</ul>
</details>

**标签**: `#AI Optimization`, `#LLM Performance`, `#llama.cpp`, `#Local LLM`, `#Automated Tuning`

---

<a id="item-13"></a>
## [多家主流媒体因 AI 训练担忧屏蔽互联网档案馆爬虫，记者联名支持数字保存](https://www.wired.com/story/the-internets-most-powerful-archiving-tool-is-in-mortal-peril/) ⭐️ 7.0/10

包括《纽约时报》、USA Today 母公司 Gannett 和 Reddit 在内的 23 家主流新闻网站和社交平台已屏蔽互联网档案馆的爬虫工具 ia_archiverbot，担心其内容被 AI 公司用于模型训练。作为回应，电子前哨基金会（EFF）组织 100 多名记者签署公开信，支持互联网档案馆的保存工作，强调其在事实核查和历史记录保存中的关键作用。 这一事件加剧了版权保护与公众获取数字信息之间的紧张关系，可能削弱未来世代存档和验证在线内容的能力。它反映了 AI 伦理方面的更广泛行业冲突，媒体机构试图控制其知识产权，而数字保存倡导者则警告这会削弱历史问责制。 屏蔽行动基于 AI 检测初创公司 Originality AI 的分析，该公司识别出这些网站限制了 ia_archiverbot 爬虫；部分媒体如《卫报》则限制了 API 访问而非完全屏蔽。互联网档案馆正与相关媒体进行沟通，警告称此类限制可能严重影响社会了解历史和现实的能力。

telegram · zaihuapd · Apr 14, 00:12

**背景**: 互联网档案馆的网站时光机（Wayback Machine）是一个于 2001 年推出的数字存档工具，用于保存网页的历史版本，允许用户查看网站的过去状态；截至 2025 年，它已存档超过 1 万亿个页面。电子前哨基金会（EFF）是一个成立于 1990 年的非营利数字权利组织，倡导互联网公民自由并支持数字保存等倡议。AI 训练涉及使用从网络抓取的大型数据集来训练机器学习模型，这在媒体和科技行业引发了版权和伦理担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Internet_Archive_Wayback_Machine">Internet Archive Wayback Machine</a></li>
<li><a href="https://en.wikipedia.org/wiki/Electronic_Frontier_Foundation">Electronic Frontier Foundation - Wikipedia</a></li>

</ul>
</details>

**标签**: `#Internet Archive`, `#AI Ethics`, `#Digital Preservation`, `#Copyright`, `#Media`

---

<a id="item-14"></a>
## [亚马逊发布机载卫星天线 Leo Aviation Antenna，与星链竞争机上 Wi-Fi 市场](https://www.pcmag.com/news/amazon-leo-shows-off-in-flight-wi-fi-antenna-that-will-take-on-starlink) ⭐️ 7.0/10

亚马逊发布了面向商用飞机的机载卫星天线 Leo Aviation Antenna，采用全双工相控阵方案，无机械运动部件，支持最高 1 Gbps 下载和 400 Mbps 上传速度，并称可在一天内完成安装。该产品已与两家航空公司达成合作，其中一项计划在 2028 年前覆盖 500 架飞机。 这一进展意义重大，因为它使亚马逊成为星链在快速增长的机上 Wi-Fi 市场中的直接竞争对手，可能推动创新并降低航空公司和乘客的成本。它有望提升航班上的连接体验，支持流媒体和视频会议等高带宽应用。 该天线采用全双工相控阵技术，无需机械部件即可同时进行发送和接收，提高了可靠性和速度。但公告中未提供关于延迟、覆盖区域或定价的具体细节。

telegram · zaihuapd · Apr 14, 01:10

**背景**: 机上 Wi-Fi 系统通常依赖卫星通信，其中低地球轨道（LEO）卫星相比传统地球静止轨道卫星具有更低的延迟。全双工相控阵天线使用电子波束赋形来追踪卫星，无需机械部件，可实现更快、更稳定的连接。星链等公司已率先提供基于 LEO 的服务，推动了该领域的竞争。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.cnblogs.com/aguai1992/p/6718763.html">关于网络和带宽（ 全 双 工 与半 双 工 带宽区别） - 阿怪123 - 博客园</a></li>
<li><a href="https://www.researching.cn/ArticlePdf/m00078/2024/22/9/9.pdf">Journal of Terahertz Science and Electronic Information Technology</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/714411449">天线测试与安装的步骤详解 - 知乎</a></li>

</ul>
</details>

**标签**: `#satellite-communications`, `#aerospace-technology`, `#in-flight-connectivity`, `#amazon`, `#starlink-competition`

---

<a id="item-15"></a>
## [谷歌搜索更新反垃圾政策，打击后退按钮劫持行为，违规站点将面临降权。](https://9to5google.com/2026/04/13/google-search-back-button-hijacking/) ⭐️ 7.0/10

谷歌搜索近日更新反垃圾内容政策，将后退按钮劫持列为恶意违规行为，该政策将于 2026 年 6 月 15 日起正式实施。此政策针对那些通过脚本干扰浏览器功能、阻止用户返回上一页并重定向至广告或未经请求页面的网站。 这一更新很重要，因为它针对日益增长的欺骗性行为，这些行为损害了用户体验和信任，有望提升网页导航标准。它将影响 SEO 和网页开发，对违规站点进行人工处置或自动降权，从而推动整个行业采用更清洁、用户友好的设计。 谷歌已观察到后退按钮劫持行为呈上升趋势，并为网站所有者提供两个月的整改期，要求其自查并移除涉及劫持的代码、库或广告平台配置。处罚措施可能包括人工处置或自动降权，这可能会严重影响网站在搜索结果中的可见度。

telegram · zaihuapd · Apr 14, 08:48

**背景**: 后退按钮劫持是一种技术，网站通过 JavaScript 脚本操纵浏览器的历史 API，例如添加条目或改变对后退命令的响应，阻止用户返回上一页。这通常会将用户重定向至广告或不需要的页面，利用浏览器功能进行垃圾信息或欺骗性目的。由于其对用户体验和信任的负面影响，这种做法已成为网页开发和 SEO 领域的一个关注点。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developers.google.com/search/blog/2026/04/back-button-hijacking">Introducing a new spam policy for "back button hijacking" | Google Search Central Blog | Google for Developers</a></li>
<li><a href="https://wolf-of-seo.de/en/what-is/back-button-hijack/">What is Back Button Hijack? A glossary entry about online risks</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/API/History_API">History API - Web APIs | MDN</a></li>

</ul>
</details>

**标签**: `#Google Search`, `#Web Development`, `#SEO`, `#User Experience`, `#Anti-Spam`

---