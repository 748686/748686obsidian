---
layout: default
title: "Horizon Summary: 2026-07-27 (ZH)"
date: 2026-07-27
lang: zh
---

> 从 32 条内容中筛选出 10 条重要资讯。

---

1. [月之暗面开源 Kimi K3：首个 2.8 万亿参数开放模型](#item-1) ⭐️ 10.0/10
2. [vLLM v0.26.0 发布：新增 Inkling 模型系列和 DeepSeek-V4 优化](#item-2) ⭐️ 9.0/10
3. [Anthropic 呼吁对强大 AI 模型进行强制安全测试](#item-3) ⭐️ 9.0/10
4. [谷歌透露 Gemini 4 为迄今最雄心预训练](#item-4) ⭐️ 9.0/10
5. [Fastjson2 未修复的远程代码执行漏洞影响所有版本](#item-5) ⭐️ 9.0/10
6. [法官驳回谷歌以 DMCA 抗辩抓取案](#item-6) ⭐️ 8.0/10
7. [Linux 内核提出危险指针方案](#item-7) ⭐️ 8.0/10
8. [单人评测发现六款前沿大模型存在左倾偏见](#item-8) ⭐️ 8.0/10
9. [长鑫科技科创板首日暴涨 471%](#item-9) ⭐️ 8.0/10
10. [中国开始量产国产 DUV 光刻机](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [月之暗面开源 Kimi K3：首个 2.8 万亿参数开放模型](https://huggingface.co/moonshotai/Kimi-K3) ⭐️ 10.0/10

月之暗面开源了 Kimi K3，该模型总参数量达 2.8 万亿，激活参数为 1040 亿，成为首个开放的 3T 级别模型。它引入了 Kimi Delta Attention \(KDA\)、Attention Residuals \(AttnRes\) 和 Stable LatentMoE 架构，支持多模态输入和百万 token 上下文窗口。 Kimi K3 的开源是人工智能领域的里程碑，为社区提供了一个前沿规模的模型，可能加速长上下文推理、多模态理解和智能体任务的研究与应用。其高效架构（相对 K2 提升 2.5 倍）表明，大规模模型可以既强大又实用。 该模型在 Stable LatentMoE 框架下使用 896 个专家，每个 token 激活 16 个，并支持 MXFP4 量化以实现高效推理。在 GPQA Diamond、BrowseComp 和 DeepSWE 等基准测试中，它与 GPT-5.6 Sol 和 Claude Fable 5 等专有模型互有胜负。

telegram · zaihuapd · 7月27日 15:15

**背景**: 大语言模型常采用混合专家 \(MoE\) 架构，在控制计算量的同时扩大参数量。Kimi K3 的 KDA 是一种线性注意力机制，可提升内存效率；Stable LatentMoE 通过将路由和专家计算投影到更低维度的潜在空间，进一步降低成本。MXFP4 是一种 4 位浮点量化格式，可在准确性与速度之间取得平衡。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://jianyuh.github.io/attention/2025/12/13/KDA.html">Linear Attention : Kimi Delta Attention | Jianyu Huang’s Blog</a></li>
<li><a href="https://arxiv.org/abs/2601.18089">[2601.18089] LatentMoE: Toward Optimal Accuracy per FLOP and Parameter in Mixture of Experts</a></li>
<li><a href="https://huggingface.co/blog/RakshitAralimatti/learn-ai-with-me">What’s MXFP4? The 4-Bit Secret Powering OpenAI’s GPT‑OSS Models on Modest Hardware</a></li>

</ul>
</details>

**标签**: `#人工智能`, `#大语言模型`, `#开源`, `#MoonshotAI`, `#Kimi K3`

---

<a id="item-2"></a>
## [vLLM v0.26.0 发布：新增 Inkling 模型系列和 DeepSeek-V4 优化](https://github.com/vllm-project/vllm/releases/tag/v0.26.0) ⭐️ 9.0/10

vLLM v0.26.0 引入了 Inkling 模型系列，提供完整支持（基础建模、CUDA 图、注意力机制、推测解码、LoRA 和量化），实现了 DeepSeek-V4 性能优化，包括专用路由内核和 fused topk bias，通过 head\_dtype 增加了 fp32 lm\_head，并允许按 KV-cache 组选择注意力后端。 此次发布显著提升了 LLM 推理的灵活性和性能，尤其适用于混合模型和大规模部署。Inkling 模型支持和 DeepSeek-V4 优化通过降低延迟和提高准确性，影响了从研究人员到生产工程师的广泛用户。 该版本包含来自 212 位贡献者的 411 次提交，重要技术新增包括 Hopper FA4 相对注意力、分段 CUDA 图支持以及用于多模态视频和音频的 Rust 前端。KV 卸载和分层二级存储已成熟，Transformers 5.13 迁移增加了多个新模型后端。

github · khluu · 7月27日 01:06

**背景**: vLLM 是一个开源的高吞吐量 LLM 推理引擎。Inkling 模型是 Thinking Machines Lab 推出的 975B 参数多模态 MoE 模型，具有 41B 活跃参数和 256k 上下文长度。FlashAttention-4 \(FA4\) 是一种最新的注意力算法，针对 NVIDIA Hopper 和 Blackwell GPU 进行了优化，提高了内存效率和速度。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://inkling-model.com/">Inkling Model : Architecture, Capabilities, Context &amp; Access</a></li>
<li><a href="https://docs.vllm.ai/en/latest/api/vllm/model_executor/layers/fused_moe/router/fused_topk_bias_router/">fused_topk_bias_router - vLLM</a></li>
<li><a href="https://modal.com/blog/reverse-engineer-flash-attention-4">We reverse-engineered Flash Attention 4</a></li>

</ul>
</details>

**标签**: `#vLLM`, `#LLM Inference`, `#DeepSeek`, `#Performance Optimization`, `#CUDA`

---

<a id="item-3"></a>
## [Anthropic 呼吁对强大 AI 模型进行强制安全测试](https://www.anthropic.com/news/position-open-weights-models) ⭐️ 9.0/10

Anthropic 发布政策声明，支持对所有足够强大的 AI 模型（包括开放权重模型）进行强制安全测试，批评者认为这实际上等同于禁止开放权重模型的发布。 这一立场可能影响 AI 监管，并可能限制开放权重模型的开发和分发，对开源 AI 社区和小型开发者产生重大影响。 Anthropic 声称其不主张禁止开放权重模型，但要求强制安全测试。批评者质疑测试由谁管理、成本以及可能的拒绝，并认为这类似于历史上事实上的禁令。

hackernews · surprisetalk · 7月27日 22:03 · [社区讨论](https://news.ycombinator.com/item?id=49076057)

**背景**: 开放权重模型是核心组件公开发布的 AI 模型，允许任何人下载、检查、修改并在自己的基础设施上运行。Anthropic 是一家专注于安全的领先 AI 公司，其政策立场在监管辩论中经常具有分量。争论的核心在于平衡创新和开放性与对强大 AI 被滥用的安全担忧。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://hai.stanford.edu/ai-definitions/what-is-an-open-weight-model">What is an Open-Weight Model? - Stanford HAI</a></li>
<li><a href="https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/">Open Weights and American AI Leadership</a></li>

</ul>
</details>

**社区讨论**: 社区评论表达了强烈的怀疑，指责 Anthropic 以安全为借口保护其专有模型。一些人指出 Anthropic 支持硬件禁令却反对模型限制的矛盾，另一些人则认为该政策是针对 DeepSeek 等开放权重替代品的竞争策略。

**标签**: `#AI safety`, `#open-weights models`, `#regulation`, `#Anthropic`, `#policy debate`

---

<a id="item-4"></a>
## [谷歌透露 Gemini 4 为迄今最雄心预训练](https://9to5google.com/2026/07/26/google-gemini-4-teases/) ⭐️ 9.0/10

谷歌 CEO Sundar Pichai 宣布 Gemini 4 已投入训练，称其为公司迄今最具雄心的预训练项目，预计 2026 年底发布。 这表明谷歌持续投入前沿 AI 研发，可能大幅提升大语言模型能力，并加剧 AI 行业的竞争。 Pichai 强调谷歌会优先将算力分配给前沿 AGI 研究，而 Gemini 3.x Flash 系列将保持近每月一次的更新频率，重点提升智能编码能力。

telegram · zaihuapd · 7月27日 04:06

**背景**: 像 Gemini 这样的大语言模型会经历预训练阶段，在海量文本数据中学习。谷歌的 Gemini 系列一直与 OpenAI 的 GPT 和 Anthropic 的 Claude 等模型竞争，最新版本旨在实现重大飞跃。

**标签**: `#AI`, `#Gemini 4`, `#Google`, `#large language models`, `#pre-training`

---

<a id="item-5"></a>
## [Fastjson2 未修复的远程代码执行漏洞影响所有版本](https://mp.weixin.qq.com/s/LJaul1jNjK9pXRAkoUiMEA) ⭐️ 9.0/10

7 月 27 日，长亭科技披露了阿里巴巴 Fastjson2 Java JSON 库中的一个远程代码执行（RCE）漏洞，影响 2.0.62 及之前的所有版本。攻击者可通过恶意 JSON 数据绕过 AutoType 类型检查并执行任意代码。目前尚未发布官方补丁。 这是一个月内 Fastjson 系列第二个严重漏洞，突显了广泛使用的 Java JSON 处理库中的持续安全风险。许多应用程序依赖 Fastjson2，未打补丁的系统面临远程攻击的高风险。 项目维护者已确认此问题，但修复分支（PR \#7695）已关闭且未合并到主分支。完整漏洞细节和利用代码尚未公开。在官方修复版推出前，建议用户完全禁用 AutoType。

telegram · zaihuapd · 7月27日 10:31

**背景**: Fastjson2 是阿里巴巴开发的高性能 Java JSON 库。它支持通过 AutoType 进行自动类型反序列化，如果保护不当可能被利用。此前 Fastjson 的早期版本也曾出现类似的 RCE 漏洞，这一问题在该库中反复出现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/alibaba/fastjson2">GitHub - alibaba/fastjson2: FASTJSON2 is a Java JSON library with ...</a></li>
<li><a href="https://alibaba.github.io/fastjson2/">FASTJSON 2.0介绍 | fastjson2</a></li>

</ul>
</details>

**标签**: `#security`, `#vulnerability`, `#fastjson2`, `#rce`, `#java`

---

<a id="item-6"></a>
## [法官驳回谷歌以 DMCA 抗辩抓取案](https://www.techdirt.com/2026/07/27/judge-rejects-googles-attempt-to-dmca-its-way-out-of-being-scraped/) ⭐️ 8.0/10

美国一名法官裁定，谷歌不能利用《数字千年版权法案》（DMCA）来阻止第三方抓取其搜索结果，驳回了谷歌关于抓取构成版权侵权的论点。 这一裁决确立了重要法律先例，维护了网络上公开数据抓取的合法性，对于依赖抓取进行创新和问责的竞争对手、研究人员和透明度倡导者至关重要。 谷歌曾辩称其搜索结果经过创造性筛选和编排，应受版权保护，但法官认为缺乏足够的原创性。该案涉及谷歌起诉第三方服务 SerpAPI，该服务抓取谷歌搜索结果。

hackernews · cdrnsf · 7月27日 18:15 · [社区讨论](https://news.ycombinator.com/item?id=49073513)

**背景**: 网页抓取是从网站自动提取数据的行为，常用于数据分析、市场研究或创建替代用户界面。DMCA 是美国版权法，禁止规避技术保护措施，并可用于执行版权主张。此案凸显了版权法与开放网络之间的紧张关系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Web_scraping">Web scraping - Wikipedia</a></li>
<li><a href="https://www.linkedin.com/pulse/what-dmca-why-does-matter-website-owners-qumere-alam-siddiqui-get6c">What is DMCA and Why Does It Matter for Website Owners 2026?</a></li>
<li><a href="https://www.dmca.com/">Content Protection and Takedown Company Since 2006 | DMCA .com</a></li>

</ul>
</details>

**社区讨论**: 评论者指出，谷歌自身的成功正是建立在爬取网络的基础之上，具有讽刺意味；同时批评谷歌取消了价格合理的 API，却起诉填补空白的三方服务。还有评论强调了抓取搜索结果以揭露广告骗局的公共利益。

**标签**: `#DMCA`, `#Web Scraping`, `#Google`, `#Copyright`, `#Tech Law`

---

<a id="item-7"></a>
## [Linux 内核提出危险指针方案](https://lwn.net/Articles/1084015/) ⭐️ 8.0/10

Linux 内核社区正在评估由 Mathieu Desnoyers 和 Paul McKenney 提出的危险指针（hazard pointer）实现，作为读-复制-更新（RCU）的替代方案，用于无锁数据更新。 与 RCU 相比，危险指针可以减少内存使用和清理延迟，在某些场景下提供更好的性能，这对内核的可扩展性和实时能力具有重要意义。 提议的 API 要求为每个并发指针分配一个 hazptr\_ctx，使用 hazptr\_acquire\(\) 保护对象，hazptr\_release\(\) 释放对象；hazptr\_synchronize\(\) 等待所有引用消失。实现使用每 CPU 的数组，包含四个槽位。

rss · LWN.net · 7月27日 16:51

**背景**: 读-复制-更新（RCU）是一种允许并发读取和更新而无需锁的同步机制，但可能延迟内存回收。危险指针是一种替代的安全内存回收技术，显式跟踪活动引用，通常对短期引用具有较低的开销。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Read-copy-update">Read - copy - update - Wikipedia</a></li>
<li><a href="https://www.linkedin.com/pulse/lock-free-stack-hazard-pointer-implementation-explained-rainer-grimm-0nsze?tl=en">A Lock-Free Stack: A Hazard Pointer Implementation Explained I</a></li>

</ul>
</details>

**标签**: `#linux-kernel`, `#hazard-pointers`, `#RCU`, `#memory-management`, `#concurrency`

---

<a id="item-8"></a>
## [单人评测发现六款前沿大模型存在左倾偏见](https://www.reddit.com/r/MachineLearning/comments/1v8fnzw/evaluated_6_frontier_llms_gpt54_claude_sonnet_46/) ⭐️ 8.0/10

一项对六款前沿大模型（GPT-5.4、Claude Sonnet 4.6、Claude Opus 4.7、Gemini Pro、Gemini Flash 和 Grok 4.3）的独立评测，使用 8 个偏见基准（约 20,600 个样本）发现，所有模型都表现出左倾政治偏见，并且在涉及种族的问题上拒绝率较高，其中 GPT-5.4 的拒绝率达到 20.3%。 这项研究为领先 AI 系统存在的系统性政治偏见提供了实证证据，可能影响内容审核和决策支持等应用中的信任与公平性。种族问题上的高拒绝率也引发了对模型实用性和敏感话题回避行为的担忧。 值得注意的是，自称右倾的 Grok 4.3 在内容分类或政策问题回答时实际表现出左倾行为。在 BBQ 种族问题上的拒绝率差异很大：GPT-5.4 拒绝 20.3%，Claude Opus 4.7 拒绝 13.8%，Grok 9.5%，而 Claude Sonnet 4.6 和 Gemini Pro 约为 5%。

reddit · r/MachineLearning · /u/marggggggggg · 7月27日 22:37

**背景**: 偏见评估基准如 WinoBias、BBQ 和 SeeGULL 旨在测量语言模型中的社会偏见（性别、种族、政治倾向）。WinoBias 测试指代消解中的性别偏见，BBQ 评估问答系统在九个社会维度上的偏见，SeeGULL 则涵盖跨地理文化群体的刻板印象。本研究使用了其中八个基准来比较六款最先进大模型在政治、性别和种族偏见方面的表现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2110.08193">[2110.08193] BBQ: A Hand-Built Bias Benchmark for Question Answering</a></li>
<li><a href="https://www.emergentmind.com/topics/winobias">WinoBias : Gender Bias in Coreference Benchmark</a></li>
<li><a href="https://github.com/google-research-datasets/seegull">GitHub - google-research-datasets/seegull: SeeGULL is a broad-coverage stereotype dataset in English containing stereotypes about identity groups spanning 178 countries across 8 different geo-political regions across 6 continents, as well as state-level identities within the US and India. · GitHub</a></li>

</ul>
</details>

**标签**: `#LLM`, `#bias`, `#evaluation`, `#fairness`

---

<a id="item-9"></a>
## [长鑫科技科创板首日暴涨 471%](https://www.stcn.com/article/detail/4042119.html) ⭐️ 8.0/10

长鑫科技（688825.SH）于 7 月 27 日在上海证券交易所科创板上市，开盘报 49.5 元/股，较发行价 8.66 元/股上涨 471.59%。 此次 IPO 是科创板史上最大规模，实际募资总额约 579.19 亿元，超过中芯国际 2020 年的纪录。这标志着中国国产 DRAM 产业及半导体自主化进程的重大里程碑。 若超额配售选择权全额行使，预计募资总额约 666.07 亿元。公司预计 2026 年上半年归母净利润 500 至 570 亿元，同比大幅扭亏。

telegram · zaihuapd · 7月27日 01:29

**背景**: 长鑫科技是中国领先的 DRAM 制造商，是国家半导体自主化战略的关键企业。科创板于 2019 年设立，是中国纳斯达克风格的科技和创新企业板块，实行注册制 IPO。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cfi.net.cn/p20260716000463.html">长 鑫 科 技 上市在即，A股投资风向转变了吗？ - CFi.CN 中财网</a></li>
<li><a href="https://en.wikipedia.org/wiki/Shanghai_Stock_Exchange_STAR_Market">Shanghai Stock Exchange STAR Market - Wikipedia</a></li>

</ul>
</details>

**标签**: `#半导体`, `#IPO`, `#存储芯片`, `#科创板`, `#国产替代`

---

<a id="item-10"></a>
## [中国开始量产国产 DUV 光刻机](https://www.theinformation.com/articles/china-starts-mass-producing-homegrown-duv-chipmaking-tools-advance-local-chip-industry) ⭐️ 8.0/10

中国已开始大规模生产自主研发的浸没式深紫外（DUV）光刻机，计划 2025 年生产约 5 台，2027 年约 20 台，并将交付给中芯国际、华虹半导体等国内芯片制造商。 这标志着中国在减少对外国光刻设备依赖方面迈出了战略性一步，可能会挑战 ASML 在中国市场的主导地位，尤其是在西方进一步收紧出口管制的情况下。 国产设备在性能和可靠性上仍落后于 ASML 的产品，芯片制造商需要数月时间测试其精度和兼容性，才能将其用于量产产线。

telegram · zaihuapd · 7月27日 14:10

**背景**: 深紫外（DUV）光刻利用光（通常为 193 纳米或 248 纳米波长）在硅晶圆上刻印集成电路图案。浸没式光刻用纯水代替透镜与晶圆之间的空气间隙，提高分辨率，可制造 45 纳米以下的特征尺寸。ASML 目前主导高端光刻市场，因此中国追求自给自足意义重大。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DUV_lithography">DUV lithography</a></li>
<li><a href="https://en.wikipedia.org/wiki/Immersion_lithography">Immersion lithography</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#lithography`, `#China`, `#ASML`, `#chip manufacturing`

---