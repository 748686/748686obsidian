---
layout: default
title: "Horizon Summary: 2026-02-26 (ZH)"
date: 2026-02-26
lang: zh
---

> From 41 items, 14 important content pieces were selected

---

1. [vLLM v0.16.0 发布，吞吐量提升超 30%，新增实时 API 并大幅更新 XPU 平台。](#item-1) ⭐️ 8.0/10
2. [Qwen 3.5 在复杂编码任务上表现不佳，70 个真实代码库基准测试揭示性能差异](#item-2) ⭐️ 8.0/10
3. [Qwen 3 27B 模型通过迭代提示创建可玩的 3D 游戏](#item-3) ⭐️ 8.0/10
4. [Anthropic 放弃其核心 AI 安全承诺，称因竞争压力](#item-4) ⭐️ 8.0/10
5. [Anthropic 披露多家中国 AI 实验室对 Claude 发起大规模蒸馏攻击](#item-5) ⭐️ 8.0/10
6. [中芯国际 N+3 工艺制造麒麟 9030 芯片，向 5nm 级技术迈进](#item-6) ⭐️ 8.0/10
7. [中国科学院将停止支付 Nature Communications 等 30 余种高价期刊的论文处理费](#item-7) ⭐️ 8.0/10
8. [tldraw 因竞争担忧将测试套件移至私有仓库](#item-8) ⭐️ 7.0/10
9. [Claude Code 推出远程控制功能，支持多设备访问](#item-9) ⭐️ 7.0/10
10. [推动 NTS 采用，为网络时间协议（NTP）安全化注入新动力](#item-10) ⭐️ 7.0/10
11. [基准测试显示，在 RTX 5080 上，Qwen3.5-35B-A3B 的 Q4_K_M 量化方法优于 UD-Q4_K_XL。](#item-11) ⭐️ 7.0/10
12. [OpenAI 为 Responses API 增加 WebSocket 支持，长链条任务提速 40%](#item-12) ⭐️ 7.0/10
13. [Uber 员工使用 CEO 的 AI 克隆进行汇报预演](#item-13) ⭐️ 7.0/10
14. [青龙面板遭挖矿木马植入，导致 CPU 占用率飙升至 800%](#item-14) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [vLLM v0.16.0 发布，吞吐量提升超 30%，新增实时 API 并大幅更新 XPU 平台。](https://github.com/vllm-project/vllm/releases/tag/v0.16.0) ⭐️ 8.0/10

vLLM v0.16.0 引入了异步调度与流水线并行，实现了超过 30% 的端到端吞吐量提升，并推出了一个基于 WebSocket 的实时 API，用于流式音频交互。该版本还对 XPU 平台进行了重大重构，弃用 IPEX 转而采用新的 vllm-xpu-kernels，并扩展了对 MoE 等模型和新数据类型的支持。 此次发布显著提升了大规模语言模型推理的效率和可扩展性，这是 AI 应用的关键瓶颈，使得高吞吐、低延迟的服务更具成本效益。新的实时 API 和扩展的硬件支持直接赋能了新的交互式、基于语音的应用，并拓宽了 AI 工作负载的可部署硬件范围。 性能提升被量化为 30.8% 的端到端吞吐量提升和 31.8% 的每输出令牌效率（TPOT）提升。实时 API 基于 Mistral AI 的 Voxtral 模型基础设施构建，可实现亚 500 毫秒延迟的流式自动语音识别。XPU 平台更新增加了对混合专家模型、MXFP4、WNA16、缩放矩阵乘法以及 FP8 数据类型的支持。

github · khluu · Feb 25, 19:58

**背景**: vLLM 是一个用于大规模语言模型的高吞吐、内存高效的推理和服务引擎。流水线并行是一种将模型拆分到多个 GPU 上以处理更大模型或提高吞吐量的技术。'XPU' 是英特尔对异构计算架构的抽象，可以映射到 CPU、GPU、FPGA 或其他加速器。实时 API 专为低延迟、流式交互设计，特别适用于使用 Voxtral 等模型的语音应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.vllm.ai/en/latest/examples/online_serving/openai_realtime_client/">OpenAI Realtime Client - vLLM</a></li>
<li><a href="https://ai.stackexchange.com/questions/28760/what-exactly-is-an-xpu">What exactly is an XPU? - Artificial Intelligence Stack Exchange</a></li>

</ul>
</details>

**标签**: `#llm-inference`, `#model-serving`, `#performance-optimization`, `#parallel-computing`, `#hardware-acceleration`

---

<a id="item-2"></a>
## [Qwen 3.5 在复杂编码任务上表现不佳，70 个真实代码库基准测试揭示性能差异](https://i.redd.it/5g4ostqlbnlg1.png) ⭐️ 8.0/10

名为 APEX Testing 的编码大语言模型综合基准测试已更新，包含 70 个真实世界编码任务，并评估了包括所有 Qwen 3.5 变体和 GPT-5.3 Codex 在内的新模型。结果显示 GPT-5.3 Codex 表现稳定出色，而大型 Qwen 3.5 397B 模型在需要跨多个文件协调的最困难 "master" 任务上表现 "崩溃"。 该基准测试为开发者和组织选择编码助手提供了关键且实用的数据，表明原始模型规模并不能保证在复杂、多步骤的软件工程任务上的性能。这些发现挑战了模型排名的普遍认知，并强调了超越简单代码补全的、针对特定任务的评估的重要性。 该基准测试现在为本地模型使用了智能体工具调用系统，以确保与基于云的智能体进行更公平的比较，并且它侧重于 "反基准测试作弊" 以防止结果被操纵。值得注意的是，GLM-4.7 模型的量化版本在测试的本地模型中获得了最高的 ELO 分数（1572），超过了所有 Qwen 3.5 变体。

reddit · r/LocalLLaMA · hauhau901 · Feb 25, 13:52

**背景**: APEX Testing 是一个自定义基准测试，旨在通过真实的代码库和问题来评估编码大语言模型，超越了合成任务。量化是一种通过使用更低精度表示权重来减少大语言模型内存和计算占用的技术，使其能够通过 LM Studio 等工具在本地硬件上运行。ELO 是一个从国际象棋借鉴的评分系统，在这里用于根据模型在基准任务上的表现进行相对排名。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://apidog.com/blog/qwen3-quantized-models-locally/">How to Use Qwen3 Quantized Models Locally: A Step-by-Step Guide</a></li>
<li><a href="https://huggingface.co/lmstudio-community?search_models=Gemma-3">lmstudio-community ( LM Studio Community)</a></li>

</ul>
</details>

**社区讨论**: 社区讨论对方法论提出了质疑，特别是所使用的自定义智能体框架是否可能对某些开源模型不利，因为性能可能因框架不同而剧烈波动。社区也对通过 OpenRouter 等 API 服务的模型结果的可信度表示担忧，因为所使用的具体量化或优化方式未知，可能会影响性能。一些用户分享了与基准测试中关于 Qwen 3.5 模型行为的发现相符的经验性观察。

**标签**: `#LLM Benchmarking`, `#Code Generation`, `#AI Programming`, `#Model Evaluation`, `#Open Source AI`

---

<a id="item-3"></a>
## [Qwen 3 27B 模型通过迭代提示创建可玩的 3D 游戏](https://www.reddit.com/r/LocalLLaMA/comments/1refvmr/qwen_3_27b_is_impressive/) ⭐️ 8.0/10

一位用户展示，Qwen 3 270 亿参数大语言模型通过五轮迭代提示和反馈，成功生成了一个功能性的、类似 GTA 的 3D 游戏，包含行走、驾驶和基础物理效果。模型根据用户反馈修正了诸如摄像机朝向错误等问题，最终产出了一个可玩的成果。 这展示了较小规模、可在本地运行的大语言模型在实践编码和空间推理能力上的重大飞跃，挑战了只有巨型模型才能处理游戏开发这类复杂、有状态任务的观念。它凸显了使用经济实惠的本地 AI 进行快速原型设计和创意辅助的潜力，这可能推动游戏开发和软件创作的民主化。 该演示使用了模型的量化版本（很可能是 Q4 量化），这大幅降低了内存需求，但据报道在此多步骤任务中仍保持了性能。成功很大程度上依赖于迭代提示，用户提供了诸如“摄像机面朝后方”等具体反馈来引导修正，现代模型处理此类技术的能力相比一年前已有显著提升。

reddit · r/LocalLLaMA · -dysangel- · Feb 25, 15:13

**背景**: Qwen 3 是阿里巴巴云开发的一系列开源大语言模型。270 亿参数版本是一个“稠密”模型，旨在性能和资源需求之间取得良好平衡，使其适合在消费级硬件上本地部署。迭代提示是一种技术，用户提供初始提示，评估 AI 的输出，然后给出包含反馈或新指令的后续提示，以逐步完善结果，这对于复杂的代码生成任务特别有效。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/html/2505.09388v1">Qwen3 Technical Report - arXiv</a></li>
<li><a href="https://www.ibm.com/think/topics/iterative-prompting">What is iterative prompting? - IBM</a></li>
<li><a href="https://medium.com/@MikeTangoSierra/deploying-an-llm-locally-a-practical-guide-9372dec5fa7a">Deploying an LLM Locally: A Practical Guide | by Mark - Medium</a></li>

</ul>
</details>

**社区讨论**: 社区对这款相对较小、经过量化的模型的性能感到兴奋，认为这是未来快速、本地化、经济实惠的 AI 推理的一个积极信号，有助于打破潜在垄断。讨论强调了迭代提示和空间反馈的关键作用，注意到模型尽管经过量化仍能在多个提示中保持上下文，并将 Qwen 的性能与 Gemma3 等其他模型进行了比较。

**标签**: `#local-llm`, `#code-generation`, `#qwen`, `#3d-gaming`, `#model-benchmarking`

---

<a id="item-4"></a>
## [Anthropic 放弃其核心 AI 安全承诺，称因竞争压力](https://time.com/7380854/exclusive-anthropic-drops-flagship-safety-pledge/) ⭐️ 8.0/10

以注重安全著称的 AI 公司 Anthropic 已正式放弃其旗舰安全承诺。该公司将激烈的竞争压力和 AI 技术的快速发展作为其单方面政策转变的理由。 此举标志着一家领先的 AI 安全倡导者在自愿自我监管方面的重大退却，可能削弱全行业的规范，并加速安全标准上的“竞次”竞争。这反映了在尖端 AI 领域，商业和地缘政治压力正在压倒早期的伦理承诺。 据报道，这一决定受到了来自美国国防部的压力（要求允许将 AI 用于监视和自主武器）以及来自 DeepSeek 等竞争对手的影响。在放弃单方面承诺的同时，Anthropic 仍继续支持外部监管努力，如加利福尼亚州的 AI 安全法案 SB 53。

reddit · r/LocalLLaMA · HumanDrone8721 · Feb 25, 18:59

**背景**: Anthropic 成立之初就高度重视 AI 安全研究，并将自身定位为伦理领导者。其旗舰安全承诺是一项负责任开发的自愿承诺，类似于其他科技巨头在白宫倡议后所做的承诺。这些承诺是在具有约束力的政府法规出台之前，建立安全规范的更广泛的全行业努力的一部分。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://time.com/7380854/exclusive-anthropic-drops-flagship-safety-pledge/">Anthropic Drops Flagship Safety Pledge | TIME</a></li>
<li><a href="https://forklog.com/en/anthropic-eases-ai-safety-rules-amid-pentagon-pressure/">Anthropic Eases AI Safety Rules Amid Pentagon Pressure | ForkLog</a></li>
<li><a href="https://www.eweek.com/news/california-ai-safety-bill-sb-53-anthropic-endorsement/">Anthropic Backs SB 53 – California's Landmark AI Safety Bill</a></li>

</ul>
</details>

**社区讨论**: 社区情绪主要是嘲讽和批评，认为此举是 Anthropic 在竞争和政府压力下“出卖了灵魂”。评论内容从嘲讽该公司先前“注重安全”的品牌形象，到对服务质量下降和加速、安全性降低的开发表示担忧。一些用户将此与 Google 放弃“不作恶”信条相提并论。

**标签**: `#AI Safety`, `#Anthropic`, `#AI Ethics`, `#Industry News`, `#Policy`

---

<a id="item-5"></a>
## [Anthropic 披露多家中国 AI 实验室对 Claude 发起大规模蒸馏攻击](https://t.me/zaihuapd/39851) ⭐️ 8.0/10

Anthropic 近日发布报告，指控三家中国 AI 实验室——DeepSeek、月之暗面（Moonshot AI）和 MiniMax——对其 Claude 模型发起大规模“蒸馏攻击”。据称，这些实验室创建了超过 24,000 个虚假账号，并进行了超过 1600 万次对话交互，以提取 Claude 的能力用于训练他们自己的模型。 这一事件凸显了 AI 行业面临的一个重大安全与伦理挑战，即模型能力和安全护栏正被系统性提取，以规避出口管制和竞争壁垒。它反映了全球 AI 竞争不断升级的紧张局势，并对当前针对工业规模知识产权提取的防护措施的有效性提出了质疑。 Anthropic 指出，这些攻击规避了安全监管与出口管制，该公司正通过行为指纹识别等技术加强防御。此次行动的规模——跨越数万个虚假账号的数百万次交互——表明这是一次有组织的、工业级别的努力，而非孤立的研究尝试。

telegram · zaihuapd · Feb 25, 04:15

**背景**: 模型蒸馏是一种技术，通过使用更强大模型的输出来训练一个较小或能力较弱的模型，以复制其能力。虽然知识蒸馏是一种合法的研究方法，但当它被大规模用于系统性提取专有模型智能、违反服务条款并规避安全过滤器时，就成为一种“攻击”或“盗窃”。AI 安全控制是 Anthropic 等公司实施的措施，旨在防止其模型生成有害、有偏见或不安全的内容，但像多轮提示这样的技术有时可以绕过这些防护措施。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks">Detecting and preventing distillation attacks - Anthropic</a></li>
<li><a href="https://www.cnbc.com/2026/02/24/anthropic-openai-china-firms-distillation-deepseek.html">Anthropic joins OpenAI in flagging 'industrial-scale' distillation campaigns by Chinese AI firms - CNBC</a></li>
<li><a href="https://www.reddit.com/r/ClaudeCode/comments/1rcp658/anthropic_weve_identified_industrialscale/">Anthropic: "We've identified industrial-scale distillation attacks on our models by DeepSeek, Moonshot AI, and MiniMax." : r/ClaudeCode - Reddit</a></li>

</ul>
</details>

**社区讨论**: Reddit 上的讨论揭示了技术社区内部的争论。一些用户质疑为什么标准的“知识蒸馏”突然被标记为盗窃，这表明合法研究和恶意提取之间的界限变得模糊。其他人则对攻击的工业规模和协调性表示担忧，认为这明显违反了服务条款，并可能构成知识产权侵权。

**标签**: `#AI Security`, `#Model Distillation`, `#AI Ethics`, `#Anthropic`, `#Chinese AI Labs`

---

<a id="item-6"></a>
## [中芯国际 N+3 工艺制造麒麟 9030 芯片，向 5nm 级技术迈进](https://t.me/zaihuapd/39857) ⭐️ 8.0/10

TechInsights 于 2025 年 12 月 11 日左右发布的最新分析证实，华为麒麟 9030 应用处理器采用中芯国际（SMIC）的 N+3 工艺制造。该工艺是中芯国际早期 7nm 级 N+2 技术的缩放演进版本。 这标志着中国本土半导体产业的一项重大成就，展示了在无法获取先进 EUV 光刻机的情况下，向 5nm 级制造能力迈进的进展。这使得华为能够在国内采购先进的智能手机处理器，减少对外部代工厂的依赖。 N+3 工艺主要通过基于 DUV 的光刻技术和 DTCO（设计工艺协同优化）方面的创新实现技术缩放，但在绝对缩放水平上仍落后于台积电和三星的 5nm 工艺。该工艺预计将面临重大良率挑战，尤其是在使用 DUV 多重图案化技术激进缩放金属间距方面。

telegram · zaihuapd · Feb 25, 08:00

**背景**: 5nm 等半导体工艺节点是用于指代新一代改进型芯片技术的营销术语。EUV（极紫外）光刻是制造 7nm 及以下尖端芯片的标准工具，但其对华出口受到限制。DUV（深紫外）光刻使用更长的波长，要实现更精细的特征需要复杂的多重图案化技术，这会增加成本并可能影响良率。DTCO（设计工艺协同优化）是一种协同优化芯片设计和制造工艺以提高性能并缩短开发时间的方法论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.techinsights.com/blog/smic-n3-confirmed-kirin-9030-analysis-reveals-how-close-smic-5nm">SMIC N+3 Confirmed: Kirin 9030 Analysis Reveals How Close SMIC Is to 5nm | TechInsights</a></li>
<li><a href="https://en.wikipedia.org/wiki/5_nm_process">5 nm process - Wikipedia</a></li>
<li><a href="https://www.tsmc.com/english/news-events/blog-article-20220615">What is DTCO ?: An Introduction to Design-Technology...</a></li>

</ul>
</details>

**标签**: `#semiconductors`, `#manufacturing`, `#china-tech`, `#huawei`, `#process-technology`

---

<a id="item-7"></a>
## [中国科学院将停止支付 Nature Communications 等 30 余种高价期刊的论文处理费](https://www.science.org/content/article/major-china-funder-plans-curtail-spending-pricey-open-access-fees) ⭐️ 8.0/10

中国科学院计划于 2026 年 3 月 1 日起实施新规，禁止院内科研人员使用科学院经费支付 30 多种高收费国际开放获取期刊的论文处理费。受影响的期刊包括 Nature Communications、Cell Reports 和 Science Advances 等，其单篇 APC 均不低于 5000 美元，远超约 2000 美元的全球均价。 这是全球主要科研资助机构之一的重大政策转变，可能显著重塑开放获取出版的经济模式以及全球的期刊选择格局。此举旨在控制不断攀升的科研成本并推动本土期刊发展，可能会对知名国际出版商的商业模式产生影响。 根据新规，若无其他资金来源，中国科学院的研究人员在 Nature 等混合期刊发表论文时，将需要选择非开放获取（订阅）模式以避免费用。该政策专门针对被认为收费过高的期刊，聚焦于一个包含 30 多种刊物的名单，这些刊物的费用是全球平均水平的两倍以上。

telegram · zaihuapd · Feb 25, 10:15

**背景**: 论文处理费是作者或其机构为使研究文章在开放获取期刊上发表后能免费获取而支付的费用。混合期刊是基于订阅的期刊，但为单篇文章提供开放获取选项（需支付 APC），这为出版商创造了双重收入流。中国科学院是一个国家级的综合性科研机构，也是中国重要的科研经费来源。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.springernature.com/gp/open-science/journals-books/journal-pricing-faqs">Journal pricing FAQs | Open science - Springer Nature</a></li>
<li><a href="https://en.wikipedia.org/wiki/Hybrid_open-access_journal">Hybrid open-access journal - Wikipedia</a></li>
<li><a href="https://www.science.org/content/article/major-china-funder-plans-curtail-spending-pricey-open-access-fees">Major Chinese funder to stop paying fees for 30 pricey open-access journals | Science</a></li>

</ul>
</details>

**标签**: `#academic-publishing`, `#open-access`, `#research-funding`, `#science-policy`, `#china-research`

---

<a id="item-8"></a>
## [tldraw 因竞争担忧将测试套件移至私有仓库](https://simonwillison.net/2026/Feb/25/closed-tests/#atom-everything) ⭐️ 7.0/10

协作绘图库 tldraw 正将其全面的测试套件从其公共 GitHub 仓库转移至私有仓库。据报道，这一决定是由于担心详细的测试可能使竞争对手或 AI 代理能够从头开始重建该库的功能，Cloudflare 最近使用 AI 移植 Next.js 的项目就证明了这一点。 此举突显了商业开源项目（COSS）在保持透明度和保护其知识产权与商业可行性之间日益加剧的紧张关系。它引发了关于哪些核心资产应保持开放的根本性问题，并可能为其他公司限制测试访问开创先例，从而可能改变开源开发实践。 值得注意的是，tldraw 并未采用传统的开源许可证；它使用自定义许可证，要求在生产环境中使用需获得商业许可。该团队还提交了一个讽刺性的议题，讨论将代码翻译成繁体中文以“保护知识产权”免受 AI 代理侵害，这突显了 AI 时代更广泛且常带有讽刺意味的担忧。

rss · Simon Willison · Feb 25, 21:06

**背景**: tldraw 是一个流行的 SDK，用于构建具有实时协作功能的无限画布和白板应用程序。商业开源软件（COSS）公司通常会公开其核心代码，但依赖专有扩展、托管服务或技术支持来获得收入。Vite 和 Webpack 等构建工具用于打包和优化 Web 应用程序代码，而 AI 辅助代码生成正变得越来越能够基于测试等公共工件来理解和复制软件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://tldraw.dev/">tldraw: Infinite Canvas SDK for React</a></li>
<li><a href="https://github.com/tldraw/tldraw">tldraw/tldraw: very good whiteboard infinite canvas SDK - GitHub</a></li>
<li><a href="https://en.wikipedia.org/wiki/Business_models_for_open-source_software">Business models for open-source software - Wikipedia</a></li>

</ul>
</details>

**标签**: `#open-source`, `#business-models`, `#testing`, `#intellectual-property`, `#software-engineering`

---

<a id="item-9"></a>
## [Claude Code 推出远程控制功能，支持多设备访问](https://simonwillison.net/2026/Feb/25/claude-code-remote-control/#atom-everything) ⭐️ 7.0/10

Anthropic 昨日为 Claude Code 发布了一项新的“远程控制”功能，允许用户在本地计算机上运行一个会话，然后通过 Claude Code 的网页版、iOS 版或原生桌面应用界面向其发送提示。该功能通过在终端中运行 `claude remote-control` 命令来激活。 该功能显著增强了 Claude Code 的灵活性和可访问性，使开发者能够在一台设备（如台式机）上启动编码或自动化任务，并从另一台设备（如手机）继续或监控它。这标志着 AI 驱动的开发工具向更无缝地融入多设备工作流程迈出了一步，与 OpenClaw 等类似产品形成竞争。 该功能的初始版本存在一些不完善之处：用户可能会遇到账户权限错误，`--dangerously-skip-permissions` 标志似乎无效，并且可能出现 API 500 错误。此外，每台机器只能运行一个远程会话，如果本地程序重启，会话会异常终止。

rss · Simon Willison · Feb 25, 17:33

**背景**: Claude Code 是 Anthropic 推出的一款开发者工具，允许用户通过终端或桌面应用与 AI 模型（如 Claude Opus 和 Sonnet）交互，以执行代码、自动化任务和控制应用程序。它通常在用户的本地机器上运行。文中用于对比的“Claw 类”软件，指的是像 OpenClaw 这样能够远程控制和自动化个人计算机的工具，通常具备定时任务执行功能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://code.claude.com/docs/en/remote-control">Continue local sessions from any device with Remote Control - Claude Code Docs</a></li>
<li><a href="https://venturebeat.com/orchestration/anthropic-just-released-a-mobile-version-of-claude-code-called-remote">Anthropic just released a mobile version of Claude Code called Remote Control | VentureBeat</a></li>

</ul>
</details>

**标签**: `#AI Development`, `#Claude Code`, `#Developer Tools`, `#Remote Control`

---

<a id="item-10"></a>
## [推动 NTS 采用，为网络时间协议（NTP）安全化注入新动力](https://lwn.net/Articles/1059200/) ⭐️ 7.0/10

在 FOSDEM 2026 上，Trifecta Tech 基金会的 Ruben Nijveld 介绍了加速采用网络时间安全（NTS）标准的工作，该标准是 IETF 的 RFC-8915，旨在保护 NTP 流量。该基金会获得了 ICANN 等机构的额外资助，正在测试相关技术，以帮助 pool.ntp.org 等大型时间服务器更轻松地部署 NTS。 NTP 是用于时间同步的基础性互联网协议，但其本身存在根本性的安全缺陷，易受欺骗攻击。用 NTS 对其进行保护至关重要，因为准确、可信的时间是无数系统的基石，从身份验证（Kerberos、TOTP）、分布式计算到蜂窝网络、金融交易和电网都依赖于此。 NTS 的重点是为 NTP 数据包提供身份验证和完整性保护，而非加密时间数据本身，因为时间载荷是公开的。该标准利用传输层安全（TLS）进行初始密钥交换，并使用关联数据认证加密（AEAD）来保护后续的时间同步交换。

rss · LWN.net · Feb 25, 14:26

**背景**: 网络时间协议（NTP）创建于 1985 年，用于将互联网上的计算机时钟与协调世界时（UTC）同步，通常参考原子钟（Stratum 0 源）。它采用分层客户端-服务器模型运行，但设计时未内置安全机制，因此容易受到中间人攻击，导致时间戳被篡改。网络时间安全（NTS）是 IETF RFC 8915 中定义的一种加密机制，专门用于为 NTP 添加身份验证和完整性保护，以解决这一长期存在的安全漏洞。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://datatracker.ietf.org/doc/html/rfc8915">RFC 8915: Network Time Security for the Network Time Protocol</a></li>
<li><a href="https://www.rfc-editor.org/info/rfc8915">Information on RFC 8915</a></li>

</ul>
</details>

**标签**: `#network-security`, `#time-synchronization`, `#protocols`, `#infrastructure`

---

<a id="item-11"></a>
## [基准测试显示，在 RTX 5080 上，Qwen3.5-35B-A3B 的 Q4_K_M 量化方法优于 UD-Q4_K_XL。](https://www.reddit.com/r/LocalLLaMA/comments/1rei65v/qwen3535ba3b_quantization_quality_speed/) ⭐️ 7.0/10

一位用户在 RTX 5080 系统上使用 llama.cpp 对 Qwen3.5-35B-A3B 模型进行了详细的基准测试，比较了 Q8_0、Q4_K_M 和 UD-Q4_K_XL 三种量化方法的质量和速度。结果显示，Unsloth Dynamic 量化（UD-Q4_K_XL）的表现明显逊于标准的 Q4_K_M，其困惑度高出近 10%，且文件体积更大。 这项基准测试为本地 LLM 社区提供了关键的实践指导，帮助他们如何在 VRAM 有限的消费级硬件上高效运行像 Qwen3.5 这样的大型、先进的混合专家模型。它强调并非所有先进的量化技术都普遍有益，选择错误的方法可能导致显著的性能下降。 由于完整模型无法放入 16GB 的 VRAM，测试使用了通过 PCIe 5.0 进行的 CPU/GPU 卸载设置。标准的 Q4_K_M 量化在 WikiText-2 上达到了 6.6688 的困惑度（仅比 Q8_0 基线差 2.1%），而其文件大小几乎只有一半。作者特别建议不要对这种 MoE 架构使用 UD-Q4_K_XL，并指出这与其它报告的结果一致。

reddit · r/LocalLLaMA · gaztrab · Feb 25, 16:35

**背景**: 量化是一种通过使用更少的比特（例如，用 4 位而非 16 位）来表示大语言模型的权重，从而降低其内存和计算成本的技术。llama.cpp 是一个流行的本地运行 LLM 的框架，支持多种量化格式，如 Q8_0（8 位）和 Q4_K_M（一种特定的 4 位方法）。混合专家模型，如 Qwen3.5-35B-A3B，采用稀疏架构，每次输入仅激活模型的一部分，这使其更高效，但有时对量化策略更敏感。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF/discussions/6">unsloth/Qwen3-30B-A3B-GGUF · `UD-Q4_K_XL` or `Q4_K_M`?</a></li>
<li><a href="https://github.com/ggml-org/llama.cpp/discussions/2094">Difference in different quantization methods · ggml-org/llama.cpp · Discussion #2094</a></li>

</ul>
</details>

**社区讨论**: 社区对技术发现进行了深入探讨。一位用户质疑使用 q8_0 作为 KV 缓存带来的性能提升是否真的“免费”，建议进行更多测试。另一位用户则对具体的配置建议表示感谢，这些建议极大提升了他自己的推理速度。一些评论还就困惑度与 KL 散度作为质量指标的优劣进行了辩论，并建议像 Bartowski 的 Q4_K_L 这样的替代量化方法可能提供更好的权衡。

**标签**: `#quantization`, `#llama.cpp`, `#benchmarking`, `#local-llm`, `#hardware-performance`

---

<a id="item-12"></a>
## [OpenAI 为 Responses API 增加 WebSocket 支持，长链条任务提速 40%](https://developers.openai.com/api/docs/guides/websocket-mode) ⭐️ 7.0/10

OpenAI 宣布为其 Responses API 引入 WebSocket 模式，专门针对涉及频繁工具调用的复杂工作流进行优化。该模式通过建立持久连接并支持增量输入，可将包含 20 次以上工具调用的长链条任务执行速度提升约 40%。 这一更新显著降低了构建智能体 AI 应用（如编码助手或编排循环）的开发者的延迟，这些应用需要大量的模型与工具交互。对于日益增长的复杂、多步骤 AI 工作流生态系统而言，这是一次有意义的性能增强。 WebSocket 模式兼容零数据保留（ZDR）规范，并支持利用 `previous_response_id` 实现低延迟的上下文续接。目前，单次连接的时长限制在 60 分钟以内。

telegram · zaihuapd · Feb 25, 07:15

**背景**: OpenAI Responses API 旨在通过提供类似聊天的格式和内置的工具调用能力（如网络搜索、文件搜索和计算机使用）来简化 AI 智能体的构建。WebSocket 是一种通信协议，可在单个 TCP 连接上提供全双工通信通道，允许客户端和服务器之间进行持久、低延迟的数据交换。零数据保留（ZDR）是一项服务提供商不存储用户数据的政策，对于在 AI 应用中处理机密信息非常重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developers.openai.com/api/docs/guides/websocket-mode">WebSocket Mode | OpenAI API</a></li>
<li><a href="https://www.panewslab.com/en/articles/019c93d3-d0f1-75fc-ae81-fdcdd120da63">OpenAI adds WebSocket support to the Responses API, speeding up long ...</a></li>
<li><a href="https://openrouter.ai/docs/guides/features/zdr">Zero Data Retention | How... | OpenRouter | Documentation</a></li>

</ul>
</details>

**标签**: `#OpenAI`, `#API`, `#WebSocket`, `#Performance`, `#AI-Workflows`

---

<a id="item-13"></a>
## [Uber 员工使用 CEO 的 AI 克隆进行汇报预演](https://www.businessinsider.com/uber-employees-use-ai-clone-ceo-prepare-meetings-presentations-2026-2) ⭐️ 7.0/10

Uber 首席执行官 Dara Khosrowshahi 透露，公司部分团队开发了一个名为“Dara AI”的数字克隆，用于帮助员工在与他本人正式会面前进行演示预演。他还指出，目前 Uber 约 30% 的工程师已成为 AI 深度用户，并且如果 AI 能显著提升工程效率，公司未来可能会优先增加 GPU 等算力资源投入，而非单纯扩张工程师员额。 这展示了生成式 AI 在企业工作流程中的一种新颖且实用的应用，超越了内容创作，进入了模拟高管反馈以提升员工技能的领域。它标志着科技公司资源分配的战略性转变，即对计算能力（GPU）的投资正被置于与传统人力资本扩张同等重要的位置，这可能重塑未来的劳动力规划。 Khosrowshahi 指出，虽然 AI 能处理海量数据，但在基于实时新信息进行决策方面仍面临挑战，目前尚无法完全取代高管职能。“Dara AI”工具的具体用途是协助员工微调幻灯片及演讲细节。

telegram · zaihuapd · Feb 25, 08:45

**背景**: 数字克隆是一项新兴技术，它利用深度学习算法来创建一个人沟通风格、声音和知识的数字副本。图形处理器（GPU）是专为并行计算设计的处理器，已成为 AI 经济的支柱，为复杂 AI 模型的训练和运行提供算力。在企业战略中，“headcount”（员额）指的是员工总数，战略规划通常涉及在人力资源与技术投资之间取得平衡。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Digital_cloning">Digital cloning - Wikipedia</a></li>
<li><a href="https://www.ensureias.com/blog/current-affairs/graphics-processing-units-gpus-from-gaming-hardware-to-the-backbone-of-the-ai-economy">Graphics Processing Units ( GPUs ): From Gaming Hardware to the...</a></li>
<li><a href="https://www.aihr.com/blog/fte-vs-headcount/">FTE vs . Headcount : The Key Differences HR Should Know - AIHR</a></li>

</ul>
</details>

**标签**: `#AI Applications`, `#Corporate Strategy`, `#Future of Work`, `#Generative AI`, `#Business Automation`

---

<a id="item-14"></a>
## [青龙面板遭挖矿木马植入，导致 CPU 占用率飙升至 800%](https://qxhut.com/?id=52) ⭐️ 7.0/10

2026 年 2 月 7 日，多名用户发现青龙面板（QingLong Panel）容器管理平台被名为 .fullgc 的挖矿木马植入，导致服务器 CPU 占用率异常升至 800%。该木马通过篡改 config.sh 配置文件实现持久化，并能根据系统架构自动下载恶意程序。 此事影响重大，因为青龙面板是一个用于管理定时任务和脚本的流行开源工具，被开发者和运维团队广泛用于自托管环境。对此类平台的成功加密劫持攻击，可以悄无声息地窃取大量服务器的计算资源，导致云成本激增、合法服务性能下降，并可能引发超越资源盗窃本身的安全漏洞。 安全分析判定该恶意程序属于 SusMiner 家族，主要通过连接 XMR（门罗币）矿池进行非法挖矿。主要攻击目标是管理端口暴露在公网 IPv4 环境下的服务器。建议用户检查 `/ql/data/db/` 路径下的隐藏文件。

telegram · zaihuapd · Feb 25, 14:24

**背景**: 青龙面板是一个基于 Docker 的开源工具，用于管理和自动化定时任务（如 JavaScript 和 Python 脚本），常用于各种网络自动化需求。加密劫持（Cryptojacking）或加密货币挖矿木马，是一种在未经用户同意的情况下劫持其计算资源来挖掘加密货币的恶意软件，通常会导致 CPU/GPU 使用率飙升和能源成本增加。门罗币（XMR）是一种注重隐私的加密货币，由于其挖矿算法与通用 CPU 兼容，常成为此类恶意软件的目标。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lmntrix.com/blog/analysis-of-coin-miner-malware/">Analysis of Coin Miner Malware - LMNTRIX Blog</a></li>
<li><a href="https://miningpoolstats.stream/monero">Monero ( XMR ) RandomX | Mining Pools</a></li>

</ul>
</details>

**标签**: `#security`, `#malware`, `#container-security`, `#cryptojacking`, `#devops`

---