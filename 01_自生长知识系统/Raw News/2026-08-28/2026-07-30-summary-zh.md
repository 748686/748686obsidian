---
layout: default
title: "Horizon Summary: 2026-07-30 (ZH)"
date: 2026-07-30
lang: zh
---

> 从 41 条内容中筛选出 15 条重要资讯。

---

1. [GitHub Stacked PRs 现已公开预览](#item-1) ⭐️ 9.0/10
2. [OpenAI GPT-5.6 Luna 降价 80%](#item-2) ⭐️ 9.0/10
3. [Kimi K3 开源权重模型以新颖架构达到前沿水平](#item-3) ⭐️ 9.0/10
4. [Claude AI 在 60 小时内发现 NIST 后量子候选算法 HAWK 弱点](#item-4) ⭐️ 9.0/10
5. [DeepMind 解散 AlphaFold 团队，核心成员跳槽 Anthropic](#item-5) ⭐️ 9.0/10
6. [Gemini Robotics 2 实现机器人全身智能](#item-6) ⭐️ 8.0/10
7. [欧足联及 55 个成员协会抵制 FIFA 赛事](#item-7) ⭐️ 8.0/10
8. [缪子谜题破解，旧结果不再吻合](#item-8) ⭐️ 8.0/10
9. [重构的经济效益分析](#item-9) ⭐️ 8.0/10
10. [GCC 指导委员会宣布 AI 政策](#item-10) ⭐️ 8.0/10
11. [教授因同行评审流程失去三位潜在博士生](#item-11) ⭐️ 8.0/10
12. [字节重组 To B：飞书并入豆包和火山引擎](#item-12) ⭐️ 8.0/10
13. [美委员会代表团访华遭华为、DeepSeek 等拒见](#item-13) ⭐️ 8.0/10
14. [澳大利亚起诉 Telegram 涉恐内容，面临 5460 万澳元罚款](#item-14) ⭐️ 8.0/10
15. [欧盟启动 AI 超级工厂招标 拟撬动 3000 亿欧元投资](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [GitHub Stacked PRs 现已公开预览](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/) ⭐️ 9.0/10

GitHub 已推出 Stacked PRs 公开预览版，让开发者能够将大型变更拆分为小型、可审查的拉取请求，并以堆栈形式组织。 这是 GitHub 工作流程的重大变革，支持增量开发和审查，可提升代码质量和开发者效率。它让更多开发者接触到堆栈式工作流，有望改变大型功能的上线方式。 Stacked PRs 是一系列有序的拉取请求，每个代表变更的一个聚焦层，支持 CLI \(gh-stack\) 和 UI。但用户反馈合并整个堆栈存在漏洞，且在需要审查时使用 squash-and-merge 需重新批准。

hackernews · tomzorz · 7月30日 16:26 · [社区讨论](https://news.ycombinator.com/item?id=49112232)

**背景**: 传统上，拉取请求是整体式的，大型变更难以审查。Stacked PRs 允许将大型功能拆分为小型、相互依赖的 PR，可增量审查和合并。这种工作流在一些开源社区中很流行，但此前 GitHub 缺乏原生支持。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/">Stacked pull requests are now in public preview - GitHub Changelog</a></li>
<li><a href="https://github.github.com/gh-stack/">GitHub Stacked PRs | GitHub Stacked PRs</a></li>
<li><a href="https://www.reddit.com/r/programming/comments/1sl4erj/github_stacked_prs/">r/programming on Reddit: GitHub Stacked PRs</a></li>

</ul>
</details>

**社区讨论**: 社区反应不一：知名开发者 steveklabnik 称赞这是 GitHub 的最大变革之一，而用户 matharmin 报告了堆栈合并破坏等漏洞。GitHub 团队承认问题并邀请反馈，承诺尽快修复。

**标签**: `#github`, `#pull-requests`, `#developer-tools`, `#workflow`, `#version-control`

---

<a id="item-2"></a>
## [OpenAI GPT-5.6 Luna 降价 80%](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) ⭐️ 9.0/10

OpenAI 宣布将其最快最便宜的模型 GPT-5.6 Luna 降价 80%，同时通过内核优化和实验提升 15%的效率。 这一大幅降价重塑了 AI 模型的经济性，使高质量推理成本仅为以前的一小部分，并标志着在一年涨价后进入了价格下降的新阶段。 降价 80%意味着 Luna 现在便宜了 5 倍，这是通过内核工作将服务成本降低 20%以及 token 生成效率提升 15%以上实现的。此举适用于 API 和消费者使用。

hackernews · tedsanders · 7月30日 17:15 · [社区讨论](https://news.ycombinator.com/item?id=49112867)

**背景**: GPT-5.6 是 OpenAI 于 2026 年 7 月发布的模型系列，包含三个变体：Luna（最便宜）、Terra（平衡型）和 Sol（旗舰型）。Luna 本身已经能力很强且价格实惠；此次更新进一步大幅降低成本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GPT-5.6">GPT-5.6 - Wikipedia</a></li>
<li><a href="https://openai.com/index/gpt-5-6/">GPT‑5.6: Frontier intelligence that scales with ... - OpenAI</a></li>
<li><a href="https://developers.openai.com/api/docs/models/gpt-5.6-luna">GPT-5.6 Luna Model | OpenAI API</a></li>

</ul>
</details>

**社区讨论**: 社区表达了震惊和兴奋，评论指出这一转变感觉像拨号上网到宽带，并推测推理提供商每月可节省数十亿美元。一些人强调了优化选择模型的难度。

**标签**: `#GPT-5.6`, `#OpenAI`, `#AI cost reduction`, `#language models`, `#price-performance`

---

<a id="item-3"></a>
## [Kimi K3 开源权重模型以新颖架构达到前沿水平](https://www.reddit.com/r/MachineLearning/comments/1vaysjf/how_kimi_k3_engineered_its_way_to_the_frontier_r/) ⭐️ 9.0/10

月之暗面科技（Moonshot AI）发布了 Kimi K3，这是一个开源权重的大语言模型，在 580 个模型中排名第四，仅次于 Claude Opus 5、Fable 5 和 GPT-5.6 Sol。它引入了三项关键创新：Kimi Delta Attention（用每个头 128×128 的矩阵替代 KV 缓存）、Quantile Balancing（用于平衡每层 896 个专家的负载）以及 AgentENV（一个用于强化学习训练的 Firecracker 微虚拟机运行时）。 Kimi K3 证明了开源权重模型能够与最好的专有前沿模型竞争，可能加速 AI 研究和部署。其架构创新——尤其是内存高效的注意力机制和无超参数的负载均衡——可能会影响整个行业的未来模型设计。 Kimi K3 在 93 层中的 69 层使用了 Kimi Delta Attention，将 100 万 token 上下文的显存占用从 104.6 GiB 降低到 27.2 GiB。Quantile Balancing 直接从单次批次的路由器分数边距计算偏置，避免了 DeepSeek-V3 使用的固定步长偏置调整。AgentENV 在 RL 训练期间创建了 5100 万个沙箱，检查点耗时 133 毫秒，恢复耗时 49 毫秒。

reddit · r/MachineLearning · /u/noninertialframe96 · 7月30日 16:37

**背景**: 大语言模型通常使用 KV 缓存来存储注意力键值对，其大小随上下文长度线性增长，限制了长上下文性能。混合专家（MoE）模型使用多个专门的子网络（专家）按 token 激活，需要负载均衡以确保所有专家被均匀利用。基于人类反馈的强化学习（RLHF）或代理强化学习通过与环境交互来训练模型，传统上需要专用基础设施，成本高且速度慢。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://jianyuh.github.io/attention/2025/12/13/KDA.html">Linear Attention : Kimi Delta Attention | Jianyu Huang’s Blog</a></li>
<li><a href="https://openathena.ai/blog/quantile-balancing/">Mixture of Experts Quantile Balancing: Validated at 32B-A5B (1e22 FLOPs) Scale | Open Athena</a></li>
<li><a href="https://github.com/kvcache-ai/AgentENV">GitHub - kvcache-ai/AgentENV: AgentENV (AENV) is a ...</a></li>

</ul>
</details>

**标签**: `#attention mechanisms`, `#mixture of experts`, `#large language models`, `#model efficiency`, `#open-source`

---

<a id="item-4"></a>
## [Claude AI 在 60 小时内发现 NIST 后量子候选算法 HAWK 弱点](https://startupfortune.com/claude-mythos-broke-hawk-and-the-nist-post-quantum-timeline-may-not-survive-it/) ⭐️ 9.0/10

Anthropic 的 Claude Mythos Preview 模型发现 NIST 后量子数字签名算法 HAWK 的严重弱点，将其有效密钥强度减半。攻击耗时约 60 小时，耗费 10 万美元 API 费用，而人类专家此前两年未能发现。 这表明 AI 在发现后量子密码候选算法漏洞方面可超越人类密码分析员，可能重塑 NIST 标准化进程。它强调了密码敏捷性的必要性，以及应依赖经证明的标准而非等待完美算法。 该攻击针对 HAWK-256，将其安全性从 2^64 降至 2^38 次操作，但攻击并非多项式时间，因此更大密钥仍安全。此外，该模型改进了对七轮 AES-128 的最优攻击，但完整 AES-128（10 轮）不受影响。

telegram · zaihuapd · 7月30日 05:47

**背景**: HAWK 是一种基于格的数字签名方案，是 NIST 后量子密码&\#x27;附加数字签名&\#x27;阶段第三轮中唯一的格基候选算法。根据 2026 年行政令，NIST 正在标准化抗量子攻击的算法，要求联邦机构在 2030-2031 年前迁移至抗量子密码体系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.techtimes.com/articles/321876/20260728/ai-cracks-post-quantum-cipher-60-hours-after-two-years-human-review-failed.htm">AI Cracks Post-Quantum Cipher in 60 Hours After Two Years of Human Review Failed</a></li>
<li><a href="https://www.csoonline.com/article/4202920/mythos-takes-its-first-shot-at-post-quantum-cryptography.html">Anthropic finds weakness in Hawk post-quantum digital signature algorithm | CSO Online</a></li>
<li><a href="https://en.wikipedia.org/wiki/NIST_Post-Quantum_Cryptography_Standardization">NIST Post-Quantum Cryptography Standardization</a></li>

</ul>
</details>

**标签**: `#AI`, `#密码学`, `#后量子密码学`, `#NIST`, `#HAWK`

---

<a id="item-5"></a>
## [DeepMind 解散 AlphaFold 团队，核心成员跳槽 Anthropic](https://www.ft.com/content/61b2953d-ee0d-45de-af6e-a9c1cf524b33?syn-25a6b1a6=1) ⭐️ 9.0/10

谷歌 DeepMind 解散了曾获诺贝尔奖的 AlphaFold 蛋白质结构预测研究团队，核心成员 John Jumper、Jonas Adler 和 Alexander Pritzel 跳槽至竞争对手 Anthropic。 此举标志着 AI 研究领域人才争夺战加剧，DeepMind 将资源转向大语言模型等项目，而 Anthropic 则获得了顶尖的结构生物学人才。 AlphaFold 原论文的近四分之一作者已完全离开公司，其他成员被重新分配到 Gemini、酶设计、核聚变及 Isomorphic Labs 等项目。

telegram · zaihuapd · 7月30日 07:45

**背景**: AlphaFold 是谷歌 DeepMind 开发的 AI 系统，能高精度预测蛋白质结构，并于 2024 年获得诺贝尔化学奖。它是计算生物学的突破，使得快速理解蛋白质折叠成为可能。DeepMind 的新研究策略聚焦于大语言模型和其他前沿 AI 应用，而 Isomorphic Labs 是 Alphabet 旗下专注于 AI 药物研发的子公司。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AlphaFold">AlphaFold - Wikipedia</a></li>
<li><a href="https://deepmind.google/science/alphafold/">AlphaFold — Google DeepMind</a></li>
<li><a href="https://en.wikipedia.org/wiki/Isomorphic_Labs">Isomorphic Labs - Wikipedia</a></li>

</ul>
</details>

**标签**: `#AlphaFold`, `#DeepMind`, `#Anthropic`, `#AI Research`, `#Talent Movement`

---

<a id="item-6"></a>
## [Gemini Robotics 2 实现机器人全身智能](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) ⭐️ 8.0/10

2026 年 7 月 30 日，谷歌 DeepMind 发布了 Gemini Robotics 2，这是一组三个视觉-语言-动作模型，能够实现对完整人形机器人的全身智能控制、精细灵巧操作以及多机器人协作。 此次发布将机器人技术从桌面操作推进到全身协调，是迈向能够在现实环境中运行的通用人形机器人的重要一步。它展示了大模型与物理行动的结合，可能加速机器人在家庭和工作场所的部署。 Gemini Robotics 2 基于 Gemini 2.0，以三个独立模型形式发布，访问权限受限，目前仅向波士顿动力等受信任的测试者开放。这些模型将视觉和语言输入转化为电机指令，可完成行走、操作和团队协作等全身任务。

hackernews · ai2027 · 7月30日 15:15 · [社区讨论](https://news.ycombinator.com/item?id=49111237)

**背景**: 视觉-语言-动作模型是一种人工智能系统，能处理视觉和文本输入并直接输出机器人动作。此前的机器人模型常专注于抓取或导航等孤立技能。Gemini Robotics 2 将这种能力扩展到全身控制，即机器人使用整个身体（腿、躯干、手臂、手）执行协调任务。之前的版本 Gemini Robotics 于 2025 年 3 月发布，专注于桌面操作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/">Gemini Robotics 2 brings whole body intelligence to robots</a></li>
<li><a href="https://en.wikipedia.org/wiki/Gemini_Robotics">Gemini Robotics</a></li>
<li><a href="https://www.marktechpost.com/2026/07/30/google-deepmind-gemini-robotics-2-whole-body-control-dexterity-multi-robot-collaboration/">Google DeepMind Ships Three Physical AI Models For Whole Body ...</a></li>

</ul>
</details>

**社区讨论**: 社区评论对谷歌 DeepMind 广泛的 AI 组合以及快速进步的潜力表示兴奋，但也对当前机器人速度和执行器质量表示怀疑。一些用户请求对现实世界能力进行诚实评估，其他人则将其与早期大语言模型相比，认为起步缓慢但前景光明。

**标签**: `#AI`, `#Robotics`, `#DeepMind`, `#Multimodal AI`, `#Gemini`

---

<a id="item-7"></a>
## [欧足联及 55 个成员协会抵制 FIFA 赛事](https://www.uefa.com/news-media/news/02a7-213a92896eb0-54dfbf454e3b-1000--statement-on-behalf-of-uefa-and-its-55-national-associations/) ⭐️ 8.0/10

欧足联及其 55 个国家协会宣布将不参加 FIFA 赛事，理由是对治理问题和投资者影响的担忧。 这代表了国际足球治理中的重大裂痕，可能导致竞争性赛事，并重塑这项运动的全球结构。 抵制源于 FIFA 计划将世界杯扩大到 48 甚至 64 支球队，并允许外部投资者获得赛事所有权。

hackernews · dickfickling · 7月30日 18:40 · [社区讨论](https://news.ycombinator.com/item?id=49113929)

**背景**: FIFA 是足球运动的全球管理机构，而欧足联管理欧洲足球。历史上，欧足联一直是 FIFA 内部的强大集团。FIFA 最近的提议引发了对腐败和商业过度扩张的担忧。

**社区讨论**: Hacker News 社区强烈支持欧足联的立场，许多人呼吁罢免 FIFA 主席因凡蒂诺。评论者担心外部投资会将足球变成纯粹的商业。

**标签**: `#sports`, `#governance`, `#FIFA`, `#UEFA`, `#corruption`

---

<a id="item-8"></a>
## [缪子谜题破解，旧结果不再吻合](https://www.quantamagazine.org/physicists-solve-a-muon-mystery-now-old-results-dont-add-up-20260729/) ⭐️ 8.0/10

物理学家通过格点 QCD 计算使理论预测与 Fermilab 实验测量一致，解决了存在数十年的缪子 g-2 反常。但这一解决却使布鲁克海文实验的旧结果失效，现在显示出显著偏差。 这一解决加强了粒子物理标准模型——此前该模型曾因明显的反常而受到挑战。同时，它也迫使人们重新评估先前的实验结果，可能改变对基本粒子性质的理解。 关键突破来自改进的格点 QCD 计算，它降低了理论不确定性，使缪子反常磁矩（g-2）的预测值与 Fermilab 结果一致。布鲁克海文测量曾被视为新物理的先兆，如今却与理论-实验联合共识偏离 4.2 个标准差。

hackernews · ibobev · 7月30日 15:22 · [社区讨论](https://news.ycombinator.com/item?id=49111305)

**背景**: 缪子是一种与电子相似但质量约 200 倍的粒子。其磁矩可极高精度测量，任何与标准模型预测的偏差都可能预示新粒子。Fermilab 的缪子 g-2 实验以 0.14 ppm 的精度测量了缪子反常磁矩。多年来，实验值与理论计算不符，激发了新物理的希望。最近的格点 QCD 计算修正了理论值，消除了这一偏差。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Muon_g-2">Muon g-2 - Wikipedia</a></li>
<li><a href="https://muon-g-2.fnal.gov/">Fermilab | Muon g-2</a></li>
<li><a href="https://news.fnal.gov/2025/06/muon-g-2-most-precise-measurement-of-muon-magnetic-anomaly/">Muon g-2 announces most precise measurement of the magnetic ...</a></li>

</ul>
</details>

**社区讨论**: 评论包括对科学范式的哲学反思，也有对未知系统误差的质疑。有人庆幸自己没有在该问题上投入多年，还有一条幽默评论认为平行宇宙或许能调和旧结果。

**标签**: `#physics`, `#muon`, `#particle physics`, `#quantum mechanics`

---

<a id="item-9"></a>
## [重构的经济效益分析](https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html) ⭐️ 8.0/10

Martin Fowler 的文章定量分析了重构的经济效益，特别是在 AI 工具辅助下，通过实际测量展示了成本节约和质量改进。 该分析将 AI 辅助软件工程置于具体数据之上，超越了模糊的评论，为考虑采用 AI 的开发者和组织提供了可操作的见解。 该文章可能比较了重构前后的 token 消耗等指标，证明 AI 辅助重构可以降低成本并提高代码质量。

hackernews · javaeeeee · 7月30日 15:10 · [社区讨论](https://news.ycombinator.com/item?id=49111176)

**背景**: 重构是指在保持外部行为不变的情况下重组现有代码，以改善内部结构。随着 GitHub Copilot 等 AI 编程助手的兴起，理解重构的经济影响对采用这些工具的团队至关重要。

**社区讨论**: 评论者赞赏其基于实际、量化的方法，与模糊的 AI 评论形成对比。有人指出，人类开发者的最佳实践正在被 AI 重新发现，另一些人则强调在自主重构中需要人类监督。

**标签**: `#refactoring`, `#software engineering`, `#economics`, `#AI-assisted development`, `#best practices`

---

<a id="item-10"></a>
## [GCC 指导委员会宣布 AI 政策](https://lwn.net/Articles/1086041/) ⭐️ 8.0/10

GCC 指导委员会宣布了一项政策，限制 AI 生成的贡献，理由是版权和开源伦理问题。 该政策为大型开源项目处理 AI 贡献树立了先例，可能影响更广泛的自由软件生态。 该政策明确针对大语言模型的贡献，指出此类输出可能不受版权保护，这与 GPL 对版权的依赖相冲突。

hackernews · arto · 7月30日 11:45 · [社区讨论](https://news.ycombinator.com/item?id=49108685)

**背景**: GCC（GNU 编译器套件）是 GNU 项目的核心组件，采用 GPL 许可，该许可利用版权来强制执行 copyleft 原则。如果 AI 生成的代码不受版权保护，则无法使用 GPL 许可，这可能动摇自由软件的法律基础。

**社区讨论**: 社区评论表达了支持与担忧的混合态度。一些人赞赏该政策对贡献者的指导，而另一些人则辩论其对自由软件的版权影响，有评论引用道：“AI 的真正目的是让财富获得技能，而不让技能获得财富。”

**标签**: `#GCC`, `#AI Policy`, `#Open Source`, `#GNU`, `#Contributions`

---

<a id="item-11"></a>
## [教授因同行评审流程失去三位潜在博士生](https://www.reddit.com/r/MachineLearning/comments/1vawwb8/i_have_lost_three_and_a_half_potential_phd/) ⭐️ 8.0/10

一名早期职业助理教授报告称，由于会议评审流程让才华横溢的本科生对研究职业望而却步，他失去了三位半潜在博士生。这些学生参与撰写了评价很高但仍被拒绝的论文，陷入无尽的重新提交循环。 这凸显了机器学习学术出版中的系统性问题，即评审流程可能阻碍有才华的新人进入该领域。它强调了改革同行评审、减少随机性和偏见的必要性，因为当前体系可能正在损害研究的未来。 该教授在顶级会议上拥有超过 10 年经验，并认为这些论文远高于录取标准。其中一篇论文获得了四个一致“弱接收”但被拒绝，导致无尽重新提交，每次解决之前的问题后只会招致更多随机的批评。

reddit · r/MachineLearning · /u/AffectionateLife5693 · 7月30日 15:30

**背景**: “三大”机器学习会议通常指 NeurIPS、ICML 和 ICLR，它们竞争极其激烈，对 ML 学术界职业有重大影响。这些会议的同行评审过程以嘈杂和有时任意性著称，论文往往需要多次重新提交。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/khairulislam/ML-conferences">GitHub - khairulislam/ML-conferences: List of ML conferences ...</a></li>
<li><a href="https://conferencedatabase.com/blog/machine-learning-conferences">Top 7 Machine Learning Conferences for 2025-2026</a></li>
<li><a href="https://www.datacamp.com/blog/top-machine-learning-conferences">Top 11 Machine Learning Conferences for 2026 - DataCamp</a></li>

</ul>
</details>

**标签**: `#peer review`, `#academic publishing`, `#machine learning`, `#PhD students`

---

<a id="item-12"></a>
## [字节重组 To B：飞书并入豆包和火山引擎](https://news.qq.com/rain/a/20260730A03CAP00) ⭐️ 8.0/10

字节跳动重组企业业务，将飞书产品团队与豆包产品团队合并，成立新的‘豆包产品团队’，由赵祺负责；飞书的市场、销售及客户服务团队与火山引擎整合，成立‘创造力服务平台’，由谭待负责。 这是字节跳动成立以来最大规模的 To B 重组，表明其将消费端 AI 领先优势（豆包拥有 3.3 亿用户）向企业生产力场景商业化的重要战略。通过将协作工具、AI 助手和云服务紧密结合，可能重塑中国企业软件和 AI 市场。 现有飞书产品和服务保持不变，双方共同开发的豆包企业版已在部分飞书客户中内测。重组后，飞书负责人谢欣在产品方面向赵祺汇报，而市场、销售和客服职能则纳入谭待领导的创造力服务平台。

telegram · zaihuapd · 7月30日 02:55

**背景**: 飞书是字节跳动旗下的企业协作平台（国际版名为 Lark），豆包是字节跳动于 2023 年 8 月推出的 AI 聊天机器人，截至 2024 年 11 月已成为中国最受欢迎的 AI 助手，月活跃用户约 6000 万，到 2026 年 5 月用户数达 3.3 亿。火山引擎是字节跳动的云和 AI 服务平台，为企业提供 AI 模型训练和部署的基础设施。此次重组旨在更好地整合这些资源，以在企业 AI 市场竞争。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.eastisread.com/p/bytedance-folds-feishu-teams-into">ByteDance folds Feishu teams into Doubao, Volcano Engine in enterprise AI push</a></li>
<li><a href="https://technode.com/2026/07/30/bytedance-restructures-ai-business-merging-doubao-and-feishu-product-teams/">ByteDance restructures AI business, merging Doubao and Feishu ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Doubao">Doubao - Wikipedia</a></li>

</ul>
</details>

**标签**: `#ByteDance`, `#AI Business`, `#Enterprise Software`, `#Organizational Change`, `#Feishu`

---

<a id="item-13"></a>
## [美委员会代表团访华遭华为、DeepSeek 等拒见](https://tech.ifeng.com/c/8v7fL2j6ajG) ⭐️ 8.0/10

2026 年 7 月下旬，美国美中经济与安全审查委员会（USCC）代表团访问北京、杭州和上海，但被华为、腾讯、阿里巴巴、百度和 DeepSeek 等中国头部科技企业集体拒绝会面或实地考察。 此次拒绝凸显了中美科技领域日益紧张的局势和不信任，可能影响未来关于 AI 和半导体的政策建议及出口管制。它突显了在关键技术上双边接触日益困难。 USCC 成立于 2000 年，是一个独立的立法机构委员会，历史上一直推动对华芯片制裁、扩大实体清单和 AI 技术出口限制。这是其自 2019 年以来首次正式访华。

telegram · zaihuapd · 7月30日 03:40

**背景**: USCC 负责监测美中经济关系的国家安全影响并向国会报告。DeepSeek 是一家 2023 年成立的中国 AI 公司，开发了成本低廉、开源权重的大型语言模型，颠覆了 AI 行业并面临出口限制。华为是中国领先的电信和科技公司，长期受到美国制裁。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/US-China_Economic_and_Security_Review_Commission">US-China Economic and Security Review Commission</a></li>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></li>
<li><a href="https://www.uscc.gov/">Homepage | U.S.- CHINA | ECONOMIC and SECURITY REVIEW COMMISSION</a></li>

</ul>
</details>

**标签**: `#US-China relations`, `#tech policy`, `#Huawei`, `#DeepSeek`, `#security review`

---

<a id="item-14"></a>
## [澳大利亚起诉 Telegram 涉恐内容，面临 5460 万澳元罚款](https://www.reuters.com/world/asia-pacific/australia-begins-legal-action-against-telegram-over-alleged-pro-terror-material-2026-07-30/) ⭐️ 8.0/10

澳大利亚 eSafety 专员办公室对 Telegram 提起法律诉讼，指控其未按要求删除宣扬恐怖主义的内容，包括基督城和布法罗恐袭视频，最高可能面临 5460 万澳元的民事罚款。 此案凸显了加密消息平台在内容审核方面面临的日益增长的监管压力，可能为各国政府追究科技公司对用户生成极端内容的责任树立先例。 法院文件显示，2025 年 7 月至 10 月间，澳大利亚用户曾就 12 条涉恐帖文投诉，但 Telegram 未删除其中 10 条，也未封禁相关账号。

telegram · zaihuapd · 7月30日 03:45

**背景**: Telegram 是一款以强加密和极少内容审核而闻名的流行消息应用。eSafety 专员是澳大利亚的在线安全监管机构，有权发出通知要求删除非法内容。如果被判违规，Telegram 的罚款将是澳大利亚 2021 年《在线安全法》下有史以来最大的之一。

**标签**: `#platform regulation`, `#content moderation`, `#Telegram`, `#Australia`, `#terrorism`

---

<a id="item-15"></a>
## [欧盟启动 AI 超级工厂招标 拟撬动 3000 亿欧元投资](https://www.wsj.com/world/europe/eu-opens-call-for-creation-of-local-ai-gigafactories-c286213d) ⭐️ 8.0/10

欧盟委员会正式启动最多七座 AI 超级工厂的招标，旨在撬动约 3000 亿欧元投资，其中 1000 亿欧元来自欧盟层面资金和参与成员国。 此举标志着欧盟为打造自主 AI 基础设施、与美国和中国等全球领先者竞争的战略性举措，可能重塑欧洲科技生态系统并吸引大量私人资本。 招标支持最多七座 AI 设施，分为选址和扩建两个阶段。投标截止日期为 2024 年 11 月 12 日，中标结果预计 2027 年 7 月公布，设施必须在签约后 18 个月内投入运营。

telegram · zaihuapd · 7月30日 11:50

**背景**: AI 超级工厂是用于训练和运行先进 AI 模型的大规模计算设施。欧盟旨在减少对非欧洲云和计算提供商的依赖，并培育有竞争力的本地 AI 生态系统，类似于美国的《芯片法案》和中国的 AI 基础设施投资。

**标签**: `#AI`, `#Europe`, `#supercomputing`, `#investment`, `#policy`

---