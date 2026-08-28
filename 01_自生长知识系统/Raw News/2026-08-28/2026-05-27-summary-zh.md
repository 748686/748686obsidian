---
layout: default
title: "Horizon Summary: 2026-05-27 (ZH)"
date: 2026-05-27
lang: zh
---

> 从 52 条内容中筛选出 13 条重要资讯。

---

1. [荷兰以主权为由阻止美国收购 Solvinity](#item-1) ⭐️ 9.0/10
2. [微软 Copilot Cowork 数据泄露漏洞](#item-2) ⭐️ 9.0/10
3. [WAVE：一个跨厂商可移植的 GPU 指令集架构](#item-3) ⭐️ 9.0/10
4. [PrismML 发布二元和三元 Bonsai Image 4B 模型](#item-4) ⭐️ 9.0/10
5. [外包加本地 AI 很快将比前沿实验室更经济](#item-5) ⭐️ 8.0/10
6. [Curl 维护者被 AI 生成的安全报告压垮](#item-6) ⭐️ 8.0/10
7. [EAMS：用于鲁棒解剖分割的等变网格网络](#item-7) ⭐️ 8.0/10
8. [中国限制阿里巴巴和深度求索 AI 人才出境](#item-8) ⭐️ 8.0/10
9. [Cactus 混合路由器：6.5 万参数模型媲美前沿 AI 性能](#item-9) ⭐️ 8.0/10
10. [SkillOpt：将 Markdown 技能文件视为可训练参数](#item-10) ⭐️ 8.0/10
11. [伊朗计划永久断开互联网，仅允许政府审查人员上网](#item-11) ⭐️ 8.0/10
12. [Meta 收购 Manus 被中国审查，联合创始人被限制出境](#item-12) ⭐️ 8.0/10
13. [支付宝发布 Token Pay 和 AI 钱包](#item-13) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [荷兰以主权为由阻止美国收购 Solvinity](https://www.politico.eu/article/netherlands-blocks-us-takeover-vital-digital-supplier/) ⭐️ 9.0/10

荷兰政府阻止了 Kyndryl 对云服务提供商 Solvinity 的 1 亿欧元收购，后者托管国家数字身份系统 DigiD，理由是基于情报机构的建议和公共利益考量。 这一决定保护了荷兰公民的隐私和数字主权，阻止美国公司控制处理敏感身份数据的关键基础设施。它为其他国家评估外国拥有关键数字服务所有权树立了先例。 该交易价值 1 亿欧元（1.13 亿美元），涉及从 IBM 分拆出来的美国 IT 基础设施服务提供商 Kyndryl。荷兰经济事务部根据情报机构的建议阻止了收购，理由是存在国家安全和数据保护风险。

hackernews · vrganj · 5月26日 11:46 · [社区讨论](https://news.ycombinator.com/item?id=48278406)

**背景**: DigiD 是荷兰官方的数字身份系统，1650 万公民通过它访问税务申报、医疗保健等政府服务。Solvinity 提供托管 DigiD 基础设施的安全托管云服务。担忧在于，美国所有者可能被迫遵守《CLOUD 法案》等美国法律交出数据，从而破坏荷兰的数据保护法律。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.reuters.com/technology/dutch-government-block-takeover-cloud-services-company-solvinity-by-us-based-2026-05-26/">Dutch block US takeover of Solvinity as against public ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/DigiD">DigiD</a></li>
<li><a href="https://www.solvinity.com/">Secure Managed Cloud | Solvinity</a></li>

</ul>
</details>

**社区讨论**: 评论者表达了宽慰和赞同，认为政府的行动是迟来的，此前议会已投票终止 Solvinity 的合同。讨论中有人主张需要密码学主权，即使面临法律压力，供应商也无法访问数据；也有人质疑荷兰为何不能为 2000 万用户自建开源身份解决方案。

**标签**: `#cybersecurity`, `#digital sovereignty`, `#national security`, `#identity management`, `#privacy`

---

<a id="item-2"></a>
## [微软 Copilot Cowork 数据泄露漏洞](https://simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files/#atom-everything) ⭐️ 9.0/10

微软 Copilot Cowork 存在提示注入漏洞，攻击者可通过发送包含外部图片的邮件触发网络请求，利用 OneDrive 预认证链接泄露文件。该漏洞由 PromptArmor 发现并于 2026 年 5 月 26 日报告。 该漏洞凸显了自主 AI 系统中的关键设计缺陷——自动代理可被诱导泄露敏感数据。它强调了在广泛部署的企业产品（如 Microsoft 365）中防御提示注入攻击的持续挑战。 攻击之所以成功，是因为 Copilot Cowork 可以在未经批准的情况下向用户收件箱发送邮件，且邮件可包含触发网络请求的外部图片。此外，OneDrive 预认证链接可以被嵌入邮件，攻击者获取链接后可直接下载文件。

rss · Simon Willison · 5月26日 15:36

**背景**: 提示注入是一种安全漏洞，恶意输入可导致 LLM 产生非预期行为，通常覆盖系统指令。自主系统（如 Copilot Cowork）是结合记忆、规划和工具使用的 AI 架构，能够自主运行。预认证链接（PAR）是无需额外认证即可访问资源的 URL，常用于文件共享。这三者结合形成了数据泄露的“致命三重奏”。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Prompt_injection">Prompt injection - Wikipedia</a></li>
<li><a href="https://owasp.org/www-community/attacks/PromptInjection">Prompt Injection | OWASP Foundation</a></li>

</ul>
</details>

**标签**: `#security`, `#AI`, `#Microsoft`, `#prompt injection`, `#data exfiltration`

---

<a id="item-3"></a>
## [WAVE：一个跨厂商可移植的 GPU 指令集架构](https://www.reddit.com/r/MachineLearning/comments/1to76tv/p_built_a_portable_gpu_isa_after_reading_too_many/) ⭐️ 9.0/10

一位开发者开源了 WAVE，这是一个可移植的 GPU 指令集架构（ISA）及工具链，允许单个 GPU 内核在 NVIDIA、AMD、Apple 和 Intel GPU 上运行。该项目包含编译器、针对 Metal、PTX、HIP 和 SYCL 的轻量后端，以及经过验证的 PyTorch 集成，可在所有后端上产生相同的训练结果。 WAVE 解决了 GPU 编程中长期存在的碎片化问题，提供了一个适用于主要厂商的单一抽象层，有望降低机器学习和高性能计算应用的工程开销。如果得到广泛采用，它可以简化多 GPU 开发并降低 GPU 计算的门槛。 WAVE 从跨越 16 种微架构的 5000 多页厂商 ISA 文档中提炼出 11 种与硬件无关的原语。该工具链将内核编译为可移植的二进制文件，然后由轻量后端转换为特定厂商的 ISA；该项目已在 Apple M4 Pro、NVIDIA T4 和 AMD MI300X GPU 上得到验证。

reddit · r/MachineLearning · /u/not-your-typical-cs · 5月26日 13:36

**背景**: GPU 编程传统上需要特定厂商的语言和工具链，例如 NVIDIA 的 CUDA 和 PTX、AMD 的 HIP 以及 Apple 的 Metal，这使得编写可移植代码变得困难。GPU ISA 定义了 GPU 执行的底层指令，而可移植 ISA 可以抽象掉硬件差异。WAVE 基于这一概念，创建了一个通用 ISA，所有主要 GPU 厂商都可以通过轻量后端来支持。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://wave.ojima.me/">WAVE - The Universal GPU ISA | WAVE</a></li>
<li><a href="https://en.wikipedia.org/wiki/ROCm">ROCm - Wikipedia</a></li>

</ul>
</details>

**标签**: `#GPU`, `#ISA`, `#portability`, `#deep learning`, `#toolchain`

---

<a id="item-4"></a>
## [PrismML 发布二元和三元 Bonsai Image 4B 模型](https://www.reddit.com/r/LocalLLaMA/comments/1togflk/prismml_just_released_binary_and_ternary_bonsai/) ⭐️ 9.0/10

PrismML 发布了 Bonsai Image 4B 文本到图像扩散变换器的二元和三元量化版本，模型大小仅约 3GB，并通过 WebGPU 在浏览器中实现完全本地推理。 这一突破使强大的文本到图像模型能够在消费级硬件上运行，无需昂贵的 GPU 或云服务，从而大幅降低使用门槛并保护用户隐私，从而普及了 AI 图像生成。 二元和三元量化将模型权重分别降至每参数 1 比特和约 1.58 比特，将 40 亿参数模型从约 16GB 压缩到约 3GB。这些模型以 Apache-2.0 许可证发布，并包含 WebGPU 推理的官方实现。

reddit · r/LocalLLaMA · /u/xenovatech · 5月26日 18:53

**背景**: 传统的扩散模型如 FLUX 使用 U-Net 架构，但最近的创新如扩散变换器（DiTs）用变换器骨干取代了 U-Net，以实现更好的可扩展性。极端量化技术如二元和三元量化通过使用极低比特宽度（1 或 1.58 比特）表示权重，从而减小模型大小，使模型适用于内存有限的设备。WebGPU 是一种现代浏览器 API，允许 Web 应用程序利用 GPU 进行加速计算，从而无需服务器端处理即可实现本地推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ieeexplore.ieee.org/document/11250544">A Survey on Binary and Ternary Neural Networks and Their Realization in ...</a></li>
<li><a href="https://encord.com/blog/diffusion-models-with-transformers/">Scalability of Diffusion Models with Transformer Backbone | Encord</a></li>
<li><a href="https://dl.acm.org/doi/10.1145/3696410.3714553">WeInfer: Unleashing the Power of WebGPU on LLM Inference in Web Browsers | Proceedings of the ACM on Web Conference 2025</a></li>

</ul>
</details>

**标签**: `#quantization`, `#diffusion`, `#text-to-image`, `#webgpu`, `#local-ai`

---

<a id="item-5"></a>
## [外包加本地 AI 很快将比前沿实验室更经济](https://www.signalbloom.ai/posts/outsourcing-plus-localai-will-soon-become-more-economical-vs-frontier-labs/) ⭐️ 8.0/10

如果准确，这一转变可能减少对昂贵前沿 API 的依赖，使小公司能够获得先进 AI 能力，并可能改变软件开发和 AI 咨询行业。 该文章具有推测性，基于 LLM 定价趋势，指出订阅式访问如 Claude 等模型比 API 定价便宜 10 到 40 倍，而开发者的技能和管理仍然是关键因素。

hackernews · GodelNumbering · 5月26日 12:08 · [社区讨论](https://news.ycombinator.com/item?id=48278610)

**背景**: 前沿 AI 实验室如 OpenAI、DeepMind 和 Anthropic 开发大型强大模型，通过昂贵的 API 访问。外包涉及在低工资国家雇佣开发者。文章认为，将较小的本地 AI 模型与外包人才结合，可以以较低成本匹配或超越前沿模型性能，挑战当前以 API 为中心的模式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Most_prestigious_AI_research_labs">Most prestigious AI research labs</a></li>
<li><a href="https://x.ai/api">API : Frontier Models for Reasoning & Enterprise | xAI</a></li>
<li><a href="https://openai.com/api/">Our API platform offers our latest models and guides for safety best...</a></li>

</ul>
</details>

**社区讨论**: 评论者大多同意开发者质量和管理至关重要，有些人将使用 LLM 与海外开发者工作相提并论。有人怀疑能力较弱的开发者配合较弱 AI 能否胜过使用前沿 AI 的强开发者。一位评论者报告称，一家公司正在用美国程序员加 AI 取代东欧团队，表明生产力提高。

**标签**: `#AI economics`, `#LLMs`, `#software engineering`, `#outsourcing`, `#developer productivity`

---

<a id="item-6"></a>
## [Curl 维护者被 AI 生成的安全报告压垮](https://simonwillison.net/2026/May/26/the-pressure/#atom-everything) ⭐️ 8.0/10

Curl 项目的首席维护者 Daniel Stenberg 报告称，团队正面临前所未有的、由 AI 辅助生成的可信安全报告洪流，目前每日收到的报告超过一份——是 2024 年的 4 到 5 倍，是 2025 年速度的两倍。 这突显了一个系统性问题：AI 工具大幅提高了安全报告的数量和质量，给关键开源项目的维护者带来巨大压力，并威胁到项目的可持续性。 尽管报告激增，但发现的漏洞大多为低或中等 severity；最近一次高严重性 CVE 发布于 2023 年 10 月。在当前发布周期内，项目已确认 12 个漏洞，创下新纪录，并且有望在 2026 年中期之前至少发布 30 个 CVE。

rss · Simon Willison · 5月26日 23:48

**背景**: Curl 是一个广泛使用的开源命令行工具和库，用于通过 URL 传输数据，安装在数十亿设备上。项目的安全团队负责处理漏洞报告并发布 CVE（常见漏洞与暴露）。近期，AI 辅助的安全研究工具实现了更全面、自动化的漏洞发现，导致详细报告激增。

**标签**: `#curl`, `#security`, `#open source`, `#AI`, `#vulnerability management`

---

<a id="item-7"></a>
## [EAMS：用于鲁棒解剖分割的等变网格网络](https://www.reddit.com/r/MachineLearning/comments/1tobtmu/augmented_equivariant_mesh_networks_for/) ⭐️ 8.0/10

EAMS 表明，一个轻量级的等变架构可以处理多种解剖分割任务而无需任务特定定制，同时在姿态和网格分辨率变化等几何扰动下保持稳定，这对临床可靠性至关重要。 该模型使用热核签名（HKS）和面积加权 PCA 导出的框架作为解剖学先验，并通过轻量级全局上下文增强消息传递。实验表明严格等变性可能损害微妙的非对称特征（例如肝脏标志点），这促进了未来对软等变性的研究。

reddit · r/MachineLearning · /u/m0ronovich · 5月26日 16:18

**背景**: 解剖网格分割涉及对来自医学扫描的 3D 表面网格的顶点、边或面进行标记。传统方法通常是任务特定且非等变的，导致在旋转或分辨率变化下性能下降。等变神经网络（如 EMNN）强制执行旋转平移对称性以提高泛化能力，但可能难以处理非对称的解剖学线索。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2402.04821">[2402.04821] E(3)-Equivariant Mesh Neural Networks</a></li>
<li><a href="https://github.com/HySonLab/EquiMesh">GitHub - HySonLab/EquiMesh: E(3)-Equivariant Mesh Neural Networks (AISTATS 2024)</a></li>
<li><a href="https://arxiv.org/abs/2505.21572">[2505.21572] Thickness-aware E(3)-Equivariant 3D Mesh Neural Networks</a></li>

</ul>
</details>

**社区讨论**: 作者作为个人项目分享了这项工作，对 ICML workshop 的接收表示兴奋，并指出了等变性与非对称特征性能之间的权衡。他们邀请反馈，并提到计划通过学习的规范化（canonicalization）和帧平均（frame averaging）探索软等变性。

**标签**: `#machine learning`, `#mesh segmentation`, `#equivariant neural networks`, `#medical imaging`, `#ICML`

---

<a id="item-8"></a>
## [中国限制阿里巴巴和深度求索 AI 人才出境](https://www.reddit.com/r/LocalLLaMA/comments/1to5fj5/china_clamps_down_on_overseas_travel_for_ai/) ⭐️ 8.0/10

据报道，中国对阿里巴巴和深度求索（DeepSeek）的人工智能研究人员实施了出境限制。此举可能阻碍与国际 AI 界的思想交流与合作。 这一限制可能显著减缓中国的人工智能研究和开源模型开发，影响全球 AI 格局。还可能扰乱人才流动和模型发布，对像深度求索这样积极发布开源模型的公司造成影响。 限制措施特别针对阿里巴巴和深度求索这两家中国领先 AI 实体的人工智能人才。深度求索由梁文峰于 2023 年创立，由幻方量化（High-Flyer）资助，已发布多个开源模型，包括 DeepSeek-LLM 和 DeepSeek-Coder。

reddit · r/LocalLLaMA · /u/kaggleqrdl · 5月26日 12:26

**背景**: 深度求索是一家位于杭州的中国人工智能公司，以使用自建训练框架和万卡算力开发开源大语言模型而闻名。该公司因迅速发布具有竞争力的模型而受到关注。中国对 AI 人才流动的收紧反映了持续的地缘政治紧张局势和对技术转移的担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>
<li><a href="https://www.deepseek.com/">DeepSeek | 深度求索</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区表达了担忧，有评论称‘如果属实，影响很大。对中国的研究/开源模型来说不是好兆头。’总体情绪反映出对来自中国的开源 AI 开发可能受到负面影响的焦虑。

**标签**: `#AI`, `#China`, `#Talent`, `#Open Source`, `#Geopolitics`

---

<a id="item-9"></a>
## [Cactus 混合路由器：6.5 万参数模型媲美前沿 AI 性能](https://www.reddit.com/r/LocalLLaMA/comments/1tom98y/cactus_hybrid_router_gemma42b_can_match/) ⭐️ 8.0/10

Cactus Compute 发布了 Cactus 混合路由器，这是一个 6.5 万参数的模型，能够决定是使用量化后的边缘模型（如 Gemma4-2B）在本地处理任务，还是将任务路由到云端前沿模型（如 Gemini-3.1-Flash-Lite），在将 15-55%的任务路由到云端的同时实现了同等性能。 这一创新通过本地处理简单查询，大幅降低推理成本和云端基础设施压力，使 AI 部署更加高效且可扩展，适用于编码助手和实时 AI 等应用。 该路由器仅使用 6.5 万个参数，支持纯文本、视觉和音频提示；它支持可调节的边缘-云端比例，并且即使在边缘模型通过 Cactus Quants 量化为 4 位时也能保持稳健的性能。

reddit · r/LocalLLaMA · /u/Henrie_the_dreamer · 5月26日 22:20

**背景**: 混合路由使用一个轻量快速的模型来评估查询复杂度，决定是使用本地模型还是调用云端模型，从而平衡延迟、成本和精度。量化技术以极小的质量损失压缩模型大小，实现高效的设备端推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/quotentiroler/CactusRoute">CactusRoute — 7-Layer Adaptive Edge/Cloud Hybrid Router</a></li>
<li><a href="https://betterstack.com/community/guides/ai/cactus-ai/">Cactus: Low-Latency AI Inference for Mobile with Zero-Copy ...</a></li>
<li><a href="https://cactuscompute.com/docs/v1.6">Overview | Cactus</a></li>

</ul>
</details>

**标签**: `#AI inference`, `#edge computing`, `#model routing`, `#hybrid models`, `#LLM optimization`

---

<a id="item-10"></a>
## [SkillOpt：将 Markdown 技能文件视为可训练参数](https://www.reddit.com/r/LocalLLaMA/comments/1to1mey/skillopt_treats_markdown_skill_files_as_trainable/) ⭐️ 8.0/10

SkillOpt 提出了一套系统化的优化框架，针对 LLM 智能体的 Markdown 技能文件，通过有界编辑和验证门控迭代改进技能描述。 该工作将此前智能体构建中的临时做法形式化，实现了可跨模型和基准迁移的自动技能优化，有望减少人工提示工程的工作量。 最佳技能在众多提议中仅接受 1 到 4 次编辑即可收敛，每步 4 到 8 次的编辑预算效果最佳，最终技能中位数约为 920 个 token。在 Codex 上优化的技能无需修改即可迁移到 Claude Code，在 SpreadsheetBench 上提升了 59.7 分。

reddit · r/LocalLLaMA · /u/agentic-doc · 5月26日 09:20

**背景**: LLM 智能体通常依赖描述任务执行方式的 Markdown 技能文件，但这些文件通常是手工编写的。SkillOpt 将这些技能文件视为可训练参数，使用优化模型提出有界编辑（添加、删除、替换），并通过验证集进行门控接受，类似于文本空间中的梯度下降。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.emergentmind.com/topics/skillopt">SkillOpt : Optimizing LLM Agent Skills</a></li>
<li><a href="https://huggingface.co/papers/2605.23904">Paper page - SkillOpt : Executive Strategy for Self-Evolving Agent Skills</a></li>
<li><a href="https://digg.com/ai/gulp2jzs">Microsoft Research releases SkillOpt , an optimization method that...</a></li>

</ul>
</details>

**标签**: `#LLM agents`, `#skill optimization`, `#markdown`, `#code generation`, `#AI research`

---

<a id="item-11"></a>
## [伊朗计划永久断开互联网，仅允许政府审查人员上网](https://t.me/zaihuapd/41574) ⭐️ 8.0/10

数字权利活动人士报告称，伊朗正计划永久断开全球互联网连接，仅允许通过政府审查的人员访问经过过滤的版本。该计划被称为‘政府特权’，将用国内内联网取代当前互联网，供大多数公民使用。 如果实施，这将是全球最极端的互联网审查形式之一，使伊朗与数字世界隔绝，严重限制信息流动。这可能为其他威权政权树立先例，对数字权利、言论自由和地缘政治紧张局势具有重大影响。 据报道，该计划源于伊朗自 2005 年以来为加强控制而开发的国内内联网‘国家信息网络’（NIN）。据 Filterwatch 称，2026 年 1 月 8 日开始的当前互联网关闭是这一永久系统的前兆，全球访问需要安全审查。

telegram · zaihuapd · 5月26日 06:36

**背景**: 伊朗长期以来一直实行互联网审查，屏蔽被认为有害的社交媒体和网站。国家信息网络是一个由国家控制的内联网，旨在取代全球互联网供国内用户使用。2026 年初，伊朗在抗议活动后经历了全面互联网中断，随后采用了‘Filternet Plus’配置，用国内内联网取代全球互联网。新计划将使这些限制永久化并具有选择性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/filterwatch/filterwatch-has-a-new-home-df8ca19e37f2">Filterwatch Has A New Home! - Medium</a></li>
<li><a href="https://en.wikipedia.org/wiki/National_Information_Network">National Information Network - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Internet_censorship_in_Iran">Internet censorship in Iran - Wikipedia</a></li>

</ul>
</details>

**标签**: `#internet censorship`, `#Iran`, `#digital rights`, `#network sovereignty`

---

<a id="item-12"></a>
## [Meta 收购 Manus 被中国审查，联合创始人被限制出境](https://t.me/zaihuapd/41577) ⭐️ 8.0/10

中国监管部门正在调查 Meta 收购 AI 初创公司 Manus 是否违反投资规定，并在审查期间限制了联合创始人 Xiao Hong 和 Ji Yichao 的出境。 这标志着跨境科技收购审查的显著升级，可能为未来涉及中国创立的初创企业与美国科技巨头的 AI 交易开创先例。它也凸显了中美之间在 AI 人才和技术方面日益紧张的局势。 Meta 于 2024 年 12 月宣布收购 Manus，交易金额未公开，但有报道称约 20 亿美元。联合创始人在本月与国家发改委会面后被通知不得离境，但允许在中国境内出行。

telegram · zaihuapd · 5月26日 09:56

**背景**: Manus 是由 Butterfly Effect 开发的通用型 AI 智能体，该公司在中国创立但总部设在新加坡。它旨在利用工具和推理自主执行复杂任务。Meta 的收购是其增强 AI 能力的重大举措，但中国监管机构正在审查该交易是否违反投资规定，可能是出于对技术转让和国家安全的担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Manus_(AI_agent)">Manus ( AI agent) - Wikipedia</a></li>
<li><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lCOTdxakVCR2FRVHVzSFJ3dm1pZ0FQAQ?hl=en-NG&gl=NG&ceid=NG:en">Google News - News about Manus • AI • Meta - Overview</a></li>

</ul>
</details>

**标签**: `#AI regulation`, `#Meta`, `#Manus`, `#China tech`, `#acquisition`

---

<a id="item-13"></a>
## [支付宝发布 Token Pay 和 AI 钱包](https://finance.sina.com.cn/jjxw/2026-05-26/doc-inhzffss1524895.shtml) ⭐️ 8.0/10

2026 年 5 月 26 日，支付宝发布了 Token Pay 服务（面向 AI 公司的支付方案）和 AI 钱包（面向个人用户管理 AI 智能体支付的产品），现已开放体验。 这标志着主流金融科技平台首次推出集成的 AI 原生支付体系，将 AI 服务与全球订阅和基于 Token 的支付连接起来。此举可能加速 AI 应用的商业化，并为 AI 商务树立新标准。 Token Pay 支持全球用户订阅和端内充 Token，面向大模型公司。MiniMax 和阶跃星辰已与支付宝合作，在其 AI 产品中采用该支付方案。

telegram · zaihuapd · 5月26日 12:31

**背景**: 支付宝此前已推出 AI 付和 AI 收服务，现在通过 Token Pay 和 AI 钱包补齐了全栈 AI 支付体系。AI 付已处理 3 亿笔交易，支持 95%的通用智能体框架，成为全球首个大规模商用的 AI 原生支付基建。Token Pay 旨在满足 AI 服务的独特需求，如基于 Token 的计费和周期性订阅。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://news.qq.com/rain/a/20260526A06WSA00">支付宝发布全球首个Token Pay服务和AI钱包产品，即日起就可体验</a></li>
<li><a href="https://finance.sina.com.cn/tech/roll/2026-05-26/doc-inhzffsk2851978.shtml">全新发布AI钱包和Token Pay 支付宝全栈AI支付产品矩阵亮相_新浪科技_...</a></li>
<li><a href="https://www.163.com/dy/article/KTSBC55005198UNI.html">支付宝：已完成3亿笔AI支付 全新发布AI钱包及Token Pay</a></li>

</ul>
</details>

**标签**: `#支付宝`, `#Token Pay`, `#AI钱包`, `#支付`, `#金融科技`

---