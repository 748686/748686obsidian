---
layout: default
title: "Horizon Summary: 2026-07-20 (ZH)"
date: 2026-07-20
lang: zh
---

> 从 41 条内容中筛选出 14 条重要资讯。

---

1. [AI 在寻找反例上超越数学家](#item-1) ⭐️ 9.0/10
2. [黑客清除罗马尼亚土地登记数据库](#item-2) ⭐️ 9.0/10
3. [Fastjson 1.x 高危无 Gadget RCE 漏洞](#item-3) ⭐️ 9.0/10
4. [中国开放权重 AI 策略正在胜出](#item-4) ⭐️ 8.0/10
5. [arXiv 上 AI 写作激增的测量揭示了检测缺陷](#item-5) ⭐️ 8.0/10
6. [软件中的完美与过度工程](#item-6) ⭐️ 8.0/10
7. [Kimi K3、Qwen 3.8 与 Anthropic 潜在解体](#item-7) ⭐️ 8.0/10
8. [谷歌的声音](#item-8) ⭐️ 8.0/10
9. [本·汤普森提议美国立法以增强开放 AI 模型对抗中国](#item-9) ⭐️ 8.0/10
10. [山姆·奥特曼披露 OpenAI 本地 GPT-3 计划](#item-10) ⭐️ 8.0/10
11. [Hugging Face 披露 AI 智能体驱动的安全事件](#item-11) ⭐️ 8.0/10
12. [美政府被曝拟限制使用中国开放权重 AI 模型](#item-12) ⭐️ 8.0/10
13. [研究发现在美军应用中发现中俄代码](#item-13) ⭐️ 8.0/10
14. [智谱建成国产芯片大型数据中心](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [AI 在寻找反例上超越数学家](https://xenaproject.wordpress.com/2026/07/20/human-mathematicians-are-being-outcounterexampled/) ⭐️ 9.0/10

一篇博客文章指出，AI 工具越来越多地能够为数学猜想提供反例，从而节省数学家的时间并改变研究方向。 这一发展代表了 AI 主动参与数学发现的范式转变，可能加速研究进程，并避免在错误猜想上浪费精力。 文章强调，包括大语言模型和 Lean 等形式化证明助手在内的 AI，现在能够发现人类可能忽略的反例，甚至针对长期存在的猜想。

hackernews · artninja1988 · 7月20日 19:03 · [社区讨论](https://news.ycombinator.com/item?id=48983382)

**背景**: 数学猜想是指被认为正确但尚未证明的命题。找到反例可以推翻猜想，这历来需要人类的洞察力。AI 现在能够利用机器学习和自动推理，系统地搜索数学空间以寻找此类反例。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2306.07277">[2306.07277] Mathematical conjecture generation using machine intelligence</a></li>
<li><a href="https://www.math.harvard.edu/event/workshop-on-machine-learning-and-mathematical-conjecture/">Workshop on Machine Learning and Mathematical Conjecture - Harvard Math</a></li>

</ul>
</details>

**社区讨论**: 评论普遍欢迎这一趋势，指出这能避免研究人员在错误猜想上浪费时间，如张益唐的轶事所示。有人诗意地反思人类主导地位的丧失，引用《约翰·亨利之歌》，而另一些人则希望自己求学时就有基于 LLM 的形式化工具来检测错误。

**标签**: `#AI`, `#mathematics`, `#counterexamples`, `#machine learning`, `#research`

---

<a id="item-2"></a>
## [黑客清除罗马尼亚土地登记数据库](https://news.risky.biz/risky-bulletin-hacker-wipes-romanias-entire-land-registry-database/) ⭐️ 9.0/10

一名黑客清除了罗马尼亚整个土地登记数据库，但官方声称离线备份可能保存了关键数据。 此事件可能破坏土地所有权证明和房地产交易，如果备份失败，将影响数百万罗马尼亚人。 黑客疑似来自阿尔及利亚的 Zakaria Mahdjoub。该机构正在将其应用程序迁移到罗马尼亚政府云，由特别电信服务局（STS）协调。

hackernews · speckx · 7月20日 13:28 · [社区讨论](https://news.ycombinator.com/item?id=48978605)

**背景**: 土地登记数据库包含土地所有权、边界和交易的法律记录。丢失此类数据可能导致法律混乱和经济混乱。罗马尼亚的离线备份可能防止最坏情况发生。

**社区讨论**: 评论指出政府 IT 合同中的腐败可能导致安全性差。一些人对存在离线备份表示庆幸，另一些人则注意到其他地方类似事件，如韩国数据中心火灾。

**标签**: `#cybersecurity`, `#database`, `#government infrastructure`, `#incident response`, `#Romania`

---

<a id="item-3"></a>
## [Fastjson 1.x 高危无 Gadget RCE 漏洞](https://x.com/k_firsov/status/2078872293745570032) ⭐️ 9.0/10

Fastjson 1.2.68 至 1.2.83 版本被披露存在一个严重的远程代码执行漏洞，该漏洞无需开启 autoType，也无需任何 classpath gadget 链，可在 JDK 8、17 和 21 上利用。 该漏洞极其严重，因为 Fastjson 在 Java 应用中广泛使用，特别是在中国技术生态中，而 1.x 分支已停止维护且无官方补丁，用户必须升级到 Fastjson2 或启用 SafeMode 才能缓解风险。 该漏洞不需要 autoType 支持，也不依赖 classpath 中的任何特定 gadget，大大降低了利用门槛；唯一的缓解措施是升级到 Fastjson2，或通过 JVM 参数或配置文件启用 SafeMode。

telegram · zaihuapd · 7月20日 14:32

**背景**: Fastjson 是阿里巴巴开发的 Java 高性能 JSON 库。反序列化漏洞通常依赖于“gadget 链”——即 classpath 中可利用的类序列，在反序列化时被触发来执行任意代码。Fastjson 1.x 的 autoType 功能可能被滥用，而 SafeMode（自 1.2.68 引入）则完全禁用 autoType 以防止此类攻击。1.x 分支自 2024 年 10 月起已停止维护。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://snyk.io/blog/serialization-and-deserialization-in-java/">Serialization and deserialization in Java | Snyk Blog | Snyk</a></li>
<li><a href="https://github.com/alibaba/fastjson/wiki/fastjson_safemode_en">fastjson _ safemode _en · alibaba/ fastjson Wiki · GitHub</a></li>
<li><a href="https://www.huaweicloud.com/eu/notice/20220523153626935.html">Fastjson &lt;= 1.2.80 Deserialization Remote Code Execution...</a></li>

</ul>
</details>

**标签**: `#Fastjson`, `#RCE`, `#Security`, `#Vulnerability`, `#JSON`

---

<a id="item-4"></a>
## [中国开放权重 AI 策略正在胜出](https://werd.io/american-ai-is-locked-down-and-proprietary-its-losing/) ⭐️ 8.0/10

一篇文章指出，中国开放权重的 AI 模型凭借更低的成本和更广泛的采用，正在击败美国的专有模型，挑战 OpenAI 的 GPT 等闭源 AI 的主导地位。 这一趋势可能使先进 AI 的获取民主化，让初创公司和研究人员无需巨额预算即可创新，并可能将全球 AI 平衡从美国科技巨头手中转移。 开放权重模型并非完全开源；它们允许用户下载和修改训练后的权重，但许可条款各异。社区评论中对“80%初创公司使用中国模型”的说法存在争议。

hackernews · benwerd · 7月20日 14:21 · [社区讨论](https://news.ycombinator.com/item?id=48979269)

**背景**: 开放权重 AI 模型是指其训练后的神经网络权重公开可下载和改编，与仅通过 API 访问的专有模型相对。这降低了开发者针对特定任务微调模型的门槛。中国已发布了众多此类模型，包括阿里巴巴的 Qwen 和百度的 ERNIE，与 Meta 的 Llama 等美国开放权重模型竞争。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ai21.com/glossary/open-weights-model/">What is an Open - Weights Model ? | AI 21</a></li>
<li><a href="https://www.linkedin.com/top-content/innovation/open-innovation-models/open-weights-and-their-impact-on-innovation/">Open Weights and Their Impact on Innovation</a></li>

</ul>
</details>

**社区讨论**: 评论者指出历史模式显示免费/低端产品最终占据主导，如个人电脑击败小型机、Linux 击败 Unix。一些人对 80%的数据表示怀疑，称他们接触的初创公司主要使用美国模型。其他人澄清开放权重不等于开源，但能显著降低成本。

**标签**: `#AI`, `#open-weights`, `#China`, `#open-source`, `#AI strategy`

---

<a id="item-5"></a>
## [arXiv 上 AI 写作激增的测量揭示了检测缺陷](https://unslop.run/blog/measuring-ai-writing-on-arxiv) ⭐️ 8.0/10

该研究分析了 2021 年至 2026 年间 arXiv 上的 12,750 篇论文，发现到 2026 年 1 月，39%的论文被标记为 AI 撰写，其中计算机科学领域高达 65%。检测器经过调校以最小化误报，显示了 ChatGPT 发布后的激增。 这引发了关于学术诚信和 AI 检测工具可靠性的严重担忧，因为该研究本身承认检测存在偏差，甚至对 LLM 时代之前的人类撰写文本也可能产生误报。 该检测器结合了三种评分方法，但未发布源代码，导致难以复现。社区使用 2011 年前的论文进行测试显示高误报率，例如一篇 2011 年的论文被标记为 27%机器撰写，2012 年的博士论文被标记为 40%。

hackernews · dopamine\_daddy · 7月20日 16:36 · [社区讨论](https://news.ycombinator.com/item?id=48981206)

**背景**: AI 文本检测器通常分析词汇重复、均匀性等模式，并与已知 AI 输出进行对比。然而，这些方法可能对非母语者或正式学术写作存在偏见，近期研究表明检测器常将人类文本误判为 AI 生成（误报）。arXiv 研究强调了这些局限性，尤其是应用于结构化和客观的科学论文时。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing">Wikipedia:Signs of AI writing - Wikipedia</a></li>
<li><a href="https://www.grammarly.com/blog/ai/how-do-ai-detectors-work/">How Do AI Detectors Work? Key Methods and Limitations | Grammarly</a></li>
<li><a href="https://machinelearningmastery.com/bias-detection-in-llm-outputs-statistical-approaches/">Bias Detection in LLM Outputs: Statistical Approaches - MachineLearningMastery.com</a></li>

</ul>
</details>

**社区讨论**: 评论者对检测准确性表示怀疑，有人上传了 LLM 时代之前的论文却得到高机器撰写分数，表明存在偏见。其他人指出缺乏开源代码，并讨论了企业中使用 LLM 的博弈论动态，质疑检测到的增长是否反映了真实的 AI 写作，还是写作风格为规避检测而改变。

**标签**: `#AI`, `#arXiv`, `#academic integrity`, `#LLM detection`, `#machine learning`

---

<a id="item-6"></a>
## [软件中的完美与过度工程](https://var0.xyz/posts/perfection-is-not-over-engineering.html) ⭐️ 8.0/10

一篇文章认为，在软件中追求完美与过度工程是两回事，挑战了‘完美是好的敌人’这一常见说法，引发了关于工程文化的细致讨论。 这一讨论意义重大，因为它重新定义了工程师和产品团队评估质量权衡的方式，可能减少对完美主义的污名化，并鼓励更深思熟虑的工程决策。 该文章获得了 183 分和 83 条评论，社区成员就完美主义是否会导致过度工程，或是高质量软件的必要追求展开了辩论。评论者区分了解决错误问题（过度工程）和优化真实约束（完美）之间的差异。

hackernews · var0xyz · 7月20日 14:10 · [社区讨论](https://news.ycombinator.com/item?id=48979120)

**背景**: 在软件工程中，‘完美是好的敌人’是一句常见的格言，警告过度精化会延迟交付。过度工程指的是添加当前需求不需要的复杂性或功能。这篇文章挑战了这一二分法，认为完美主义可以是一种对卓越的纪律性追求，而非浪费精力，特别是在需求严格的情况下。

**社区讨论**: 社区意见分歧：一些人支持反对将完美视为过度工程，指出‘完美是好的敌人’常被用作低质量的借口。另一些人则警告说，完美主义可能导致对琐事的过度争论和情感负担，且这句话常被用来回应那些纠结于罕见边缘情况的工程师。一个关键见解是区分解决错误问题（过度工程）和优化真实约束（完美）。

**标签**: `#software-engineering`, `#perfectionism`, `#over-engineering`, `#engineering-culture`, `#product-development`

---

<a id="item-7"></a>
## [Kimi K3、Qwen 3.8 与 Anthropic 潜在解体](https://www.emergingtrajectories.com/lh/frontier-lab-economics/) ⭐️ 8.0/10

一篇分析文章聚焦 Kimi K3 和 Qwen 3.8 的发布，同时指出 Anthropic 的首席产品官 Mike Krieger 在 Claude Design 发布前从 Figma 董事会辞职，引发利益冲突担忧。 这些事件凸显了 AI 模型开发领域日益激烈的竞争、开源权重模型日益增长的重要性，以及前沿实验室的伦理治理问题，这些问题可能影响行业信任和监管。 社区讨论表明，对类似 K3 的模型进行 ASIC 优化可能成为决定性因素，而 Anthropic 与 Figma 的事件则引发了对专有战略信息和合作伙伴背叛的质疑。

hackernews · cl42 · 7月20日 15:13 · [社区讨论](https://news.ycombinator.com/item?id=48980019)

**背景**: 专用集成电路（ASIC）是为特定任务定制的芯片，常用于 AI 加速器。开源权重模型公开训练好的神经网络参数，允许透明评估和微调。最近发布的 Kimi K3 和 Qwen 3.8 代表了向更开放 AI 生态系统的转变。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.linkedin.com/advice/0/how-ai-machine-learning-impact-asic">AI and ML: How They Will Impact the ASIC Market</a></li>
<li><a href="https://medium.com/@kimanited73/open-weight-models-f504be677b1c">Open Weight Models . What are they, and why should you... | Medium</a></li>
<li><a href="https://www.emergentmind.com/topics/open-weight-models">Open - Weight Neural Models</a></li>

</ul>
</details>

**社区讨论**: LarsDu88 认为最终赢家将是能最快将模型优化到 ASIC 上的公司，overgard 则强调了 Figma 的利益冲突问题。bko 认为风险被夸大，port3000 观察到炒作周期缩短，暗示可能存在平台期。

**标签**: `#AI models`, `#frontier labs`, `#industry analysis`, `#open-weight models`, `#ethics`

---

<a id="item-8"></a>
## [谷歌的声音](https://www.newyorker.com/culture/the-weekend-essay/the-voice-of-google) ⭐️ 8.0/10

《纽约客》发表了一篇由前谷歌员工克莱尔·斯台普顿撰写的文章，详细描述了她在谷歌内部经历异议以及员工声音被压制的情况。 这篇文章揭示了谷歌企业文化从开放对话转向压制异议的转变，反映了大型科技公司中员工激进主义与企业控制之间的广泛紧张关系。 克莱尔·斯台普顿（Claire Stapleton），曾创建著名的“TGIF”邮件摘要，描述了她在就多样性、工会化等问题发声后如何遭到反击并最终被边缘化。

hackernews · littlexsparkee · 7月20日 15:15 · [社区讨论](https://news.ycombinator.com/item?id=48980053)

**背景**: 谷歌曾以其独特的文化和“不作恶”的信条而备受赞誉，但随着公司发展，它在军事合同、多样性和劳工权利等问题上面临内部冲突。这篇文章是关于大型科技公司中企业异议演变这一更广泛讨论的一部分。

**社区讨论**: 评论显示了各种观点：一些人支持斯台普顿关于异议被压制的叙述，而另一些人则认为她因谷歌超越了她的理想而变得怨恨。一条评论指出，这一经历促使了 Alphabet 工会的成立。

**标签**: `#Google`, `#tech culture`, `#dissent`, `#corporate culture`, `#essay`

---

<a id="item-9"></a>
## [本·汤普森提议美国立法以增强开放 AI 模型对抗中国](https://simonwillison.net/2026/Jul/20/afraid-of-chinese-models/#atom-everything) ⭐️ 8.0/10

该提案解决了 AI 实验室在未授权数据上训练却禁止蒸馏的虚伪问题，并可能为美国开放模型在与日益强大的中国开放权重模型（如 Qwen 3.8 Max）的竞争中创造公平环境。 汤普森还推测，阿里巴巴决定以开放权重形式发布 2.4 万亿参数的 Qwen 3.8 Max，可能受到了习近平最近鼓励开源讲话的影响。该模型的大小接近 Kimi K3 的 2.8 万亿参数。

rss · Simon Willison · 7月20日 17:09

**背景**: 模型蒸馏是一种将知识从大模型转移到小模型的技术，通常通过 API 查询实现，也可能被非法用于提取模型能力。开放权重模型公开其训练参数，有助于进一步创新但也可能被滥用。版权合理使用允许在未经许可的情况下使用受版权保护的材料用于研究等目的，但其对 AI 训练数据的适用性在法律上存在争议。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Model_distillation">Model distillation</a></li>
<li><a href="https://opensource.org/ai/open-weights">Open Weights: not quite what you’ve been told</a></li>

</ul>
</details>

**标签**: `#AI policy`, `#open source`, `#model distillation`, `#Chinese AI`, `#copyright`

---

<a id="item-10"></a>
## [山姆·奥特曼披露 OpenAI 本地 GPT-3 计划](https://simonwillison.net/2026/Jul/20/sam-altman/#atom-everything) ⭐️ 8.0/10

一份山姆·奥特曼在 2022 年 10 月 1 日发给 OpenAI 董事会的邮件被泄露，并在 2026 年马斯克诉奥特曼案中曝光，邮件详细说明了 OpenAI 计划发布一个能力接近 GPT-3 级别、可在消费硬件上本地运行的语言模型。 这一披露提供了对 OpenAI 在开源竞争方面战略思考的罕见洞察，显示该公司曾考虑发布本地模型，专门用于抢先于 Stability AI 等竞争对手，并抑制新项目的融资。 该模型的能力将接近 GPT-3，并可在消费硬件上运行，无需依赖云端。奥特曼表示目标是尽快发布，抢在 Stability AI 或其他公司推出类似模型之前。

rss · Simon Willison · 7月20日 03:47

**背景**: GPT-3 是一个拥有 1750 亿参数的大型语言模型，以其强大的文本生成能力而闻名，但通常需要强大的云端基础设施。要在消费设备上本地运行这样的模型，需要进行大量优化，如量化或蒸馏。Stability AI 是一家英国公司，以开源图像生成模型 Stable Diffusion 闻名，并已扩展到其他 AI 领域，使其成为开源 AI 模型的竞争对手。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Stability_AI">Stability AI</a></li>
<li><a href="https://huggingface.co/openai/gpt-oss-20b">openai/ gpt -oss-20b · Hugging Face</a></li>
<li><a href="https://medium.com/ai-by-johannes/easily-create-your-own-local-gpt-for-free-81f5323e9b3a">Easily Create Your Own Local GPT for Free | by Johannes... | Medium</a></li>

</ul>
</details>

**标签**: `#ai-ethics`, `#sam-altman`, `#generative-ai`, `#open-source-strategy`

---

<a id="item-11"></a>
## [Hugging Face 披露 AI 智能体驱动的安全事件](https://huggingface.co/blog/security-incident-july-2026) ⭐️ 8.0/10

Hugging Face 披露了 2026 年 7 月的一次安全事件，一个自主 AI 智能体框架利用其数据集处理流程中的两处代码执行漏洞，窃取了内部凭证和数据。公司指出，商业大模型 API 因安全护栏最初拒绝协助取证日志分析，团队转而使用本地部署的 GLM 5.2 模型分析了超过 1.7 万条攻击记录。 这起事件意义重大，因为它展示了一种由自主 AI 智能体驱动的新型攻击手段，凸显了不断演变的威胁态势。同时，它也暴露了商业大模型 API 的一个关键局限——安全护栏可能阻碍合法的安全调查，强调了在事件响应中需要平衡安全与可用性的模型。 攻击发生在周末期间，执行了数万次操作，并在多个内部集群间横向移动。Hugging Face 确认面向公众的模型、数据集及 Spaces 未被篡改，软件供应链经核查无异常。

telegram · zaihuapd · 7月20日 10:41

**背景**: Hugging Face 是一个流行的机器学习模型、数据集和演示应用（Spaces）托管平台。AI 智能体是一种能够自主规划并执行任务以实现目标的系统，在此次事件中被用于实施攻击。LLM 安全护栏是商业模型中内置的机制，旨在防止滥用，但也可能像此次事件那样阻止合法的取证查询。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GLM_5.2">GLM 5.2</a></li>
<li><a href="https://huggingface.co/zai-org/GLM-5.2">zai-org/GLM-5.2 · Hugging Face</a></li>
<li><a href="https://www.testwo.com/article/2125">全 面 LLM 安 全 指南：解读 AI 法规与 LLM 安 全 最佳实践</a></li>

</ul>
</details>

**标签**: `#安全事件`, `#AI安全`, `#Hugging Face`, `#智能体攻击`, `#漏洞利用`

---

<a id="item-12"></a>
## [美政府被曝拟限制使用中国开放权重 AI 模型](https://www.axios.com/2026/07/20/ai-us-china-open-source-kimi) ⭐️ 8.0/10

据 Axios 报道，特朗普政府正考虑通过采购规则、实体清单威胁等软性措施，阻止美国企业使用物美价廉的中国开放权重 AI 模型，尤其是在 Kimi K3 表现强劲之后。 这一举措可能重塑全球 AI 竞争格局，可能切断美国企业获取性价比高的中国模型的途径，而这些模型正日益具有竞争力。它也凸显了开源与闭源 AI 之间日益紧张的局势，批评者认为美国闭源公司正借助政府干预来扼杀竞争。 报道指出，政府可能不会实施硬性封禁，而是依靠采购规则、实体清单威胁和舆论压力等繁文缛节式的&\#x27;软限制&\#x27;。白宫 AI 顾问 David Sacks 批评 OpenAI 和 Anthropic 试图借助政府力量消灭开源竞争。

telegram · zaihuapd · 7月20日 11:49

**背景**: 开放权重模型是指其预训练参数公开发布的人工智能模型，允许开发者微调和部署，但不一定完全开源。Kimi K3 是中国公司月之暗面（Moonshot AI）开发的大语言模型，拥有 2.8 万亿参数，采用名为 KDA 的混合线性注意力机制。它于 2026 年 7 月发布，表现出色，在某些基准测试中已接近或匹配美国模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Kimi_K3">Kimi K3</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/2000352647211929923">kimi-K3架构提前曝光! - 知乎</a></li>

</ul>
</details>

**标签**: `#AI policy`, `#open source`, `#geopolitics`, `#Kimi K3`, `#regulation`

---

<a id="item-13"></a>
## [研究发现在美军应用中发现中俄代码](https://www.wired.com/story/apps-marketed-to-us-troops-are-shipping-chinese-and-russian-code/) ⭐️ 8.0/10

普渡大学研究人员发现，面向美军推广的 220 多款应用中近三分之二嵌入了来自中国、俄罗斯等国的第三方代码，包括华为 SDK。 第三方代码可远程更新为间谍软件，可能危及美军人员敏感数据和位置信息，构成国家安全风险。 在至少一个案例中，华为 SDK 作为依赖项被偷偷嵌入，开发人员不知情。尽管未观察到数据传输至华为服务器，但代码可被远程激活。

telegram · zaihuapd · 7月20日 13:42

**背景**: 移动应用常集成第三方 SDK 用于分析等功能，但来自敌对国家的 SDK 可能引入供应链风险。美国国防部此前曾报告利用商业位置数据进行监视的情况。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.wired.com/story/apps-marketed-to-us-troops-are-shipping-chinese-and-russian-code/">Apps Marketed to US Troops Are Shipping Chinese and Russian Code | WIRED</a></li>
<li><a href="https://www.supplychainbrain.com/blogs/1-think-tank/post/44053-five-supply-chain-security-risks-hiding-inside-your-mobile-apps">Five Supply Chain Security Risks Hiding Inside Your Mobile Apps | SupplyChainBrain</a></li>
<li><a href="https://www.corellium.com/blog/mobile-app-supply-chain-security">Mobile App Security Risks: The Hidden Supply Chain Threat</a></li>

</ul>
</details>

**标签**: `#mobile security`, `#supply chain risk`, `#national security`, `#third-party code`, `#surveillance`

---

<a id="item-14"></a>
## [智谱建成国产芯片大型数据中心](https://www.bloomberg.com/news/articles/2026-07-20/z-ai-completes-giant-data-center-with-chinese-chips-to-train-ai) ⭐️ 8.0/10

智谱 AI 完成了一座全部采用国产芯片的 1 吉瓦数据中心建设，目前已部分运营，将用于支持其 GLM 大语言模型系列的开发。 这一里程碑表明中国有能力在不依赖外国芯片（如受美国出口管制的英伟达 GPU）的情况下建设大规模 AI 基础设施，减少对进口的依赖，增强中国在 AI 领域的自给自足能力，并可能加速国产芯片生态系统的发展。 该数据中心功率达 1 吉瓦，足以同时为约 75 万户家庭供电，是中国 AI 实验室建造的最大规模设施之一。智谱已运营多个各拥有超万枚芯片的计算集群。

telegram · zaihuapd · 7月20日 15:43

**背景**: 中国面临美国出口管制，限制获取英伟达 H100 等先进外国 AI 芯片。作为回应，中国 AI 实验室正加速采用来自华为昇腾、寒武纪等公司的国产芯片。智谱 AI 的 GLM 是知名的开源大语言模型系列，GLM-5 采用了 745B 参数的 MoE 架构。该数据中心标志着中国在 AI 自给自足方面迈出了关键一步。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Z.ai">Z.ai - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/GLM_%28AI%29">GLM (AI) - Wikipedia</a></li>
<li><a href="https://www.blackridgeresearch.com/blog/latest-list-top-largest-data-center-projects-china">Top 5 Data Center Projects in China 2026: ByteDance, Alibaba &amp; NDRC</a></li>

</ul>
</details>

**标签**: `#AI`, `#Data Center`, `#Chinese Chips`, `#Infrastructure`, `#GLM`

---