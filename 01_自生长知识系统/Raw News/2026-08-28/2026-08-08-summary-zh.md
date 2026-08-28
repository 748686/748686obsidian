---
layout: default
title: "Horizon Summary: 2026-08-08 (ZH)"
date: 2026-08-08
lang: zh
---

> 从 36 条内容中筛选出 23 条重要资讯。

---

**科技新闻**
1. [让 Postgres 分析查询提速数百倍：pgrust 的批处理、算子融合与 SIMD](#item-tech-news-1) ⭐️ 8.0/10
2. [Cloudflare Kitesurf：跑在 V8 隔离中的智能体优先浏览器](#item-tech-news-2) ⭐️ 8.0/10
3. [OpenAI 称 Astra 或达关键网络攻击能力，安全测试或推迟发布](#item-tech-news-3) ⭐️ 8.0/10
4. [DeepSeek V4 Flash 0731 发布：更快更便宜](#item-tech-news-4) ⭐️ 7.0/10
5. [科技从业者集体失去职业信心会怎样](#item-tech-news-5) ⭐️ 7.0/10
6. [Oracle 禁止 OpenJDK 使用 AI 生成代码](#item-tech-news-6) ⭐️ 7.0/10
7. [2027 年内存产能据报道已被预订一空](#item-tech-news-7) ⭐️ 7.0/10
8. [与爬虫搏斗一年：150 万页网站的成本与对策](#item-tech-news-8) ⭐️ 7.0/10
9. [Meta 在儿童心理健康案中被判巨额赔偿](#item-tech-news-9) ⭐️ 7.0/10
10. [Wyzer：面向分布式安全的新编程语言](#item-tech-news-10) ⭐️ 7.0/10
11. [Codex 与 GPT-5.6 Sol Ultra 生成的《Moonlight &amp; Mayhem》胜过 Claude Fable 5](#item-tech-news-11) ⭐️ 7.0/10
12. [Token 末日：企业正急于控制 AI Token 成本](#item-tech-news-12) ⭐️ 7.0/10
13. [shadow-utils 4.20.0 移除密码过期与旧散列功能](#item-tech-news-13) ⭐️ 7.0/10
14. [SK 海力士确认 V10 NAND：375 层堆叠并首次采用晶圆键合](#item-tech-news-14) ⭐️ 7.0/10
15. [sub2api 曝 OAuth 高危漏洞，仅凭邮箱即可接管账户](#item-tech-news-15) ⭐️ 7.0/10
16. [亚马逊 AWS 严查内部 CPU 浪费，智能体 AI 推高算力需求](#item-tech-news-16) ⭐️ 7.0/10

**科技博客**
1. [SpaceX 2027 年 10GW 与微软最大承购展望](#item-tech-blog-1) ⭐️ 1.0/10
2. [Gemini 长期失利，GCP 短期受益](#item-tech-blog-2) ⭐️ 1.0/10

**财经新闻**
1. [纳斯达克 23 小时交易制获 SEC 批准，12 月 6 日上线](#item-finance-news-1) ⭐️ 9.0/10
2. [7 月非农意外减少后，市场大幅下调美联储 9 月加息概率](#item-finance-news-2) ⭐️ 8.0/10
3. [特朗普再签行政令限制美国出生公民权](#item-finance-news-3) ⭐️ 8.0/10
4. [美国审查中国 AI 企业海外获取英伟达芯片渠道](#item-finance-news-4) ⭐️ 8.0/10
5. [北京非京籍购房社保年限下调至 1 年，公积金贷款额度同步提高](#item-finance-news-5) ⭐️ 8.0/10

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [让 Postgres 分析查询提速数百倍：pgrust 的批处理、算子融合与 SIMD](https://malisper.me/how-we-made-postgres-hundreds-of-times-faster-the-query-engine/) ⭐️ 8.0/10

pgrust 项目通过批处理（batching）、算子融合（operator fusion）和 SIMD 等技术，宣称能让 Postgres 的分析查询速度提升数百倍，并引入了自适应规划能力。该项目目前尚未达到生产就绪状态，作者表示当前最优先事项是正确性，已通过形式化验证和差分模糊测试证明超过 1000 个面向用户函数在 pgrust 与 Postgres 中逻辑完全一致。社区讨论既关注这些优化能否回馈到 Postgres 本身，也质疑这类替代实现能否获得足够信任。

hackernews · poly2it · 8月7日 11:00 · [社区讨论](https://news.ycombinator.com/item?id=49208535)

**「背景」** PostgreSQL 传统上以行式存储和处理为主，对于需要扫描大量数据的分析型查询往往效率不高。pgrust 是一个用 Rust 重写 PostgreSQL 的实验性项目，通过批量处理（batching）、算子融合（operator fusion）和 SIMD 指令来优化查询引擎，从而显著加速分析查询。该项目还引入了自适应规划（adaptive planning），这是社区长期期待但在 PostgreSQL 核心中尚未实现的技术。这些优化属于数据库查询引擎领域的常见技术，但应用在 PostgreSQL 上仍属新颖尝试。

**「影响」** 对于希望提升 Postgres 分析性能的开发者，pgrust 提供了值得关注的原型验证，但在项目成熟并获得社区信任之前，生产环境普遍采用的现实可能性仍然很低。

**「社区讨论」** 作者回应称正确性是首要目标，并已对大量函数做了验证；部分评论者询问优化能否反向移植到 Postgres，也有人认为即使技术上更优，用户仍会因信任和长期维护问题而选择原生 Postgres。另有评论者赞赏自适应规划方向的探索，并询问 IO 调度与线程调度等更细架构是否已得到处理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://malisper.me/how-we-made-postgres-hundreds-of-times-faster-the-query-engine/">Rebuilding Postgres for 300x faster analytics: batching, operator fusion, and SIMD - malisper.me</a></li>

</ul>
</details>

**标签**: `#postgres`, `#query-engine`, `#simd`, `#operator-fusion`, `#analytics`

---

<a id="item-tech-news-2"></a>
### [Cloudflare Kitesurf：跑在 V8 隔离中的智能体优先浏览器](https://blog.cloudflare.com/kitesurf/) ⭐️ 8.0/10

Cloudflare 发布了 Kitesurf，一个基于 Blitz 引擎、运行在 V8 隔离中的智能体优先浏览器。它旨在让浏览器自动化和 AI 智能体交互以更轻量、安全且可扩展的方式执行。与传统需要启动完整浏览器实例的方案不同，Kitesurf 将浏览器运行时封装进 V8 隔离，降低资源开销并提高同一主机上可运行的自动化任务密度。该技术可用于网页抓取、自动化测试、内容生成等场景，属于 Cloudflare 向智能体友好型平台演进的一部分。这一发布把模块化开源浏览器引擎 Blitz 带到了云基础设施的核心场景中。

hackernews · m3h · 8月7日 10:42 · [社区讨论](https://news.ycombinator.com/item?id=49208393)

**「背景」** 传统浏览器自动化需要为每个并发任务启动独立浏览器进程，资源开销高。V8 隔离是 JavaScript 引擎的轻量沙箱，能让多个独立实例共享底层进程。Cloudflare 的 Workers 已在函数计算中广泛使用 V8 隔离，Kitesurf 则将这一模型延伸到基于模块化开源引擎 Blitz 的完整浏览器运行时。

**「影响」** 对开发者而言，Kitesurf 将浏览器自动化负载封装成可在 V8 隔离中缩放运行的单元，有望降低抓取、测试和智能体应用的部署成本与密度限制。

**「社区讨论」** 社区讨论集中在 Cloudflare 的双重角色上：一些长期用户担忧 CDN/安全业务与智能体抓取服务之间存在潜在利益冲突，而另一些人则质疑 agent 在浏览器中的实际落地场景。Blitz 引擎作者补充说，Kitesurf 计划开源并回馈上游，这在一定程度上缓解了部分人对引擎封闭化的疑虑。

**标签**: `#browser automation`, `#AI agents`, `#Cloudflare`, `#browser engine`, `#web scraping`

---

<a id="item-tech-news-3"></a>
### [OpenAI 称 Astra 或达关键网络攻击能力，安全测试或推迟发布](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities/) ⭐️ 8.0/10

OpenAI 于 2026 年 8 月 7 日披露，其即将推出的模型 Astra 在内部评估中显示出代理编码与网络安全方面的重大进展，初步结果强到无法排除达到「关键」网络能力阈值的可能性；此前 GPT-5.6-Sol 等模型在该评估中仅被评为「高」。根据 OpenAI 的预备框架，达到关键阈值意味着模型可在无需人工干预的情况下，自主发现并利用加固真实系统的零日漏洞，或仅凭高层目标策划和执行端到端的新型网络攻击。公司已暂停不符合强化安全要求的 Astra 相关内部活动，实施隔离测试环境、加密增强、通用监控等措施，并将与政府机构和 AI 安全组织合作开展第三方测试。这些扩大后的安全测试可能导致 Astra 的发布推迟。

telegram · zaihuapd · 8月7日 16:44

**「背景」** OpenAI 的预备框架是一套用于评估前沿模型在网络安全等领域风险等级的机制，结果通常分为低、中、高、关键等层级。达到「关键」意味着模型具备自主实施复杂真实世界网络攻击的能力，因此会触发更严格的安全审查和发布决策。

**「影响」** 对依赖 OpenAI 前沿模型的企业和安全团队而言，Astra 若确认达到关键阈值，其发布可能延后，并伴随第三方审计与更严格的使用限制；由于评估尚未最终确认，具体的发布时间和能力边界仍存在不确定性。

**标签**: `#OpenAI`, `#AI safety`, `#cybersecurity`, `#frontier models`, `#model release`

---

<a id="item-tech-news-4"></a>
### [DeepSeek V4 Flash 0731 发布：更快更便宜](https://arcprize.org/results/deepseek-v4-flash-0731) ⭐️ 7.0/10

DeepSeek V4 Flash 0731 是 DeepSeek 于 7 月 31 日发布的新版模型，相比此前的 preview 版本，用户在质量上认为它“整整高了一个档次”，尤其擅长调试和解析上传的文档与数据。其本地部署速度突出：在 2 块 RTX Pro 6000 Blackwell 上，prefill 速度约为 8k tok/s，单流生成约 250 tok/s。成本也极低，有用户在 Oh My Pi 上同时运行 5-6 个会话（约 12 条流），每天花费难以超过 5 美元；OpenCode Go 临时提供双倍限额，10 美元实际可获得约 140 美元的 token。不过官方已预告“显著提价”，且一些用户反映新版本在 agent 场景中会出现无限循环、不执行工具调用而浪费 token 的问题。

hackernews · tosh · 8月7日 17:56 · [社区讨论](https://news.ycombinator.com/item?id=49214008)

**「背景」** DeepSeek V4 Flash 0731 是 DeepSeek 于 2026 年 7 月 31 日发布的 Flash 效率型模型正式版，取代了此前的“预览”（preview）版本。官方称其激活参数量远小于 V4 Pro（Preview），但在多项基准测试中表现更优，并与最强的专有模型基本持平。该模型沿用 V4 Flash-DSpark 的结构，加入推测解码模块以提升推理速度，提供 100 万 token 的上下文长度，并支持本地部署和 API 使用。

**「影响」** 对依赖 DeepSeek V4 Flash 的低成本编码与代理工作流，当前版本提供了更强的推理质量与更高吞吐，但官方即将上调价格，用户应关注定价变化并评估本地部署或替代方案。

**「社区讨论」** 社区普遍认可其速度与性价比，LaurensBER 称它“几乎什么事都能用，且便宜到成本无关紧要”；但 nylonstrung 对比上一版 Flash 时报告了 agent 无限循环、不执行工具调用的问题，ak\_t 则强调这是 07/31 版本而非几月前的 preview，并表示本地运行一周后感觉整体高了一个档次。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731">deepseek -ai/ DeepSeek - V 4 - Flash - 0731 · Hugging Face</a></li>
<li><a href="https://featherless.ai/models/deepseek-ai/DeepSeek-V4-Flash-0731">Run DeepSeek - V 4 - Flash - 0731 API (Easy Deployment &amp; Flat-Rate...)</a></li>
<li><a href="https://hokai.io/hub/models/deepseek-v4-flash-0731">DeepSeek - V 4 - Flash - 0731 : 1M Context &amp; GPQA 88.1 (2026) | HokAI</a></li>

</ul>
</details>

**标签**: `#deepseek`, `#large-language-models`, `#benchmark`, `#ai-inference`, `#open-source-ai`

---

<a id="item-tech-news-5"></a>
### [科技从业者集体失去职业信心会怎样](https://www.noemamag.com/why-is-everyone-in-tech-so-sad/) ⭐️ 7.0/10

这篇发表于 Noema 杂志的文章《Why Is Everyone in Tech So Sad?》探讨了为何越来越多科技从业者对职业生涯失去信心，并分析这一现象可能对整个行业产生的影响。文章被视为对科技行业幻灭与职业倦怠的深刻剖析，聚焦软件工程职业的文化转变，而非技术突破。作者认为，这种普遍的情绪不仅关乎个人心理健康，也可能威胁行业的可持续性。文中还涉及科技行业令人疲惫的工作环境、网络环境的毒性，以及从业者对职业意义的重新审视。

hackernews · RickJWagner · 8月7日 12:42 · [社区讨论](https://news.ycombinator.com/item?id=49209539)

**「背景」** 这篇文章发表于《Noema》杂志，题为《为什么科技行业里的每个人都这么悲伤？》。其核心观点是，许多人正在意识到知识工作大多是徒劳的，而人工智能或许会让我们有机会看到，当整个职业阶层对自身职业丧失信心时会发生什么。《Noema》是一本跨学科的长篇新闻杂志，覆盖哲学、治理、地缘政治、经济、技术和文化等领域。

**「影响」** 这篇文章可能促使科技行业更认真地反思从业者的职业倦怠与心理健康问题，尤其是在软件工程等核心岗位中持续存在的文化压力。

**「社区讨论」** Hacker News 评论中，有人将科技从业者的处境与历史上排字工的衰落相比，认为整个职业可能逐渐消失；也有人指出当今网络环境的毒性是导致从业者倦怠的重要根源。另一位有 20 年经验的从业者表示自己已对工作失去热情，甚至幻想流浪生活；而一位非程序员则认为文章中的幸灾乐祸令人不适，但承认这引发了对社会共同处境的思考。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.noemamag.com/why-is-everyone-in-tech-so-sad/">Why Is Everyone In Tech So Sad? | NOEMA</a></li>
<li><a href="https://www.noemamag.com/">NOEMA | Noema Magazine</a></li>

</ul>
</details>

**标签**: `#tech-industry`, `#burnout`, `#mental-health`, `#software-engineering`, `#career-satisfaction`

---

<a id="item-tech-news-6"></a>
### [Oracle 禁止 OpenJDK 使用 AI 生成代码](https://app.dealroom.co/news/feed/oracle-bans-ai-generated-code-from-openjdk-despite-ellison-s-claim-oracle-isn-t-writing-its-own-code) ⭐️ 7.0/10

Oracle 已对 OpenJDK 实施一项临时政策，禁止接受 AI 生成的代码贡献。此举主要反映法律与审查负担方面的担忧：AI 生成的内容可能带来版权溯源问题，也会加重本就有限的人力审查资源。OpenJDK 是许多企业依赖的开源 Java 实现，由 Oracle 主导开发，因此该限制对开源协作与 AI 辅助编程实践都有显著影响。

hackernews · delduca · 8月7日 17:36 · [社区讨论](https://news.ycombinator.com/item?id=49213754)

**「背景」** OpenJDK 是由 Oracle 作为企业赞助方支持的开源 Java 实现社区，长期由维护者和企业贡献者共同维护。2026 年 4 月，OpenJDK 发布了《OpenJDK Interim Policy on Generative AI》，在正式政策出台前对生成式 AI 产出的代码贡献作出限制，理由是此类贡献会增加人工审阅负担，并带来安全与知识产权风险。该临时政策已获 OpenJDK 管理委员会批准，Oracle 正在起草完整政策，后续规范将如何落地仍有待观察。

**「影响」** OpenJDK 贡献者目前必须避免提交由生成式 AI 工具编写的代码，否则相关补丁可能不被接受。由于正式政策仍在制定中，这一限制的实际执行尺度仍存在不确定性。

**「社区讨论」** 评论普遍认为这一禁令在版权风险和审查负担上可以理解，但有人指出 Oracle 自身大举投入 AI，与其限制贡献的做法存在讽刺之处；也有人预期最终政策不会比临时版本更好。另有评论者澄清 OpenJDK 并非社区独立实现，而是由 Oracle 主导的项目。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openjdk.org/legal/ai">OpenJDK Interim Policy on Generative AI</a></li>
<li><a href="https://mail.openjdk.org/archives/list/announce@openjdk.org/thread/NPTV4NGSIN2IOMVESWUVN7Y3ERMUBKH2/">OpenJDK Interim Policy on Generative AI - announce - openjdk.org</a></li>
<li><a href="https://www.infoq.com/news/2026/06/oracle-genai-policies/">Oracle&#x27;s OpenJDK Bans Generative AI Contributions While ...</a></li>

</ul>
</details>

**标签**: `#OpenJDK`, `#Oracle`, `#AI-generated code`, `#open source policy`, `#copyright`

---

<a id="item-tech-news-7"></a>
### [2027 年内存产能据报道已被预订一空](https://www.ign.com/articles/ramageddon-continues-another-year-as-2027-memory-capacity-is-reportedly-sold-out) ⭐️ 7.0/10

据报道，2027 年的内存产能已经被完全预订，这凸显了 AI 驱动的 HBM 需求正在挤压 DRAM 供应。由于 HBM3E 在生产相同比特数时消耗的晶圆供应量约为 DDR5 的三倍，HBM 产能的快速提升将限制非 HBM 产品的行业供应增长。这一状况可能对 DRAM 价格和可用性产生直接压力，并波及消费电子产品。

hackernews · inigyou · 8月7日 07:58 · [社区讨论](https://news.ycombinator.com/item?id=49207236)

**「背景」** 据报道，三星、SK 海力士和美光等主要内存厂商 2027 年的 DRAM 和 HBM 产能已被全部预订售罄，且没有计划增加额外供应。这一局面源于 AI 对高带宽内存（HBM）的强劲需求，而 HBM 的生产需要占用约三倍于普通 DRAM 的晶圆产能，因而挤压了传统内存供应。Digitimes 的报道指出，这可能导致 2027 年面向 PC、笔记本和智能手机等消费设备的 DRAM 供应相比 2026 年显著减少。

**「影响」** 2027 年内存产能据报已被预订一空，显示 AI 对 HBM 的需求正持续挤占传统 DRAM（如 DDR5）的晶圆产能，可能使消费级 PC、手机、笔记本电脑等产品的内存供应继续紧张，并推高 DRAM 现货价格。由于该消息仅为行业报道，实际产能分配与价格影响仍存在不确定性。

**「社区讨论」** 评论者指出，一个单元的 HBM 容量大约消耗相当于三个单元 DDR5 的晶圆产能，因为 HBM 芯片需要更大尺寸；其他人则担忧这会对消费产品价格产生通胀压力，并有人建议建立类似 USB 的内存条通用标准以复用旧内存，还有开发者表示正在考虑囤积微控制器。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.tweaktown.com/news/113004/memory-capacity-for-all-of-2027-has-reportedly-been-booked-and-sold-with-no-more-dram-or-hbm-available/index.html">Memory capacity for all of 2027 has reportedly been booked and sold, with no more DRAM or HBM available</a></li>
<li><a href="https://www.ign.com/articles/ramageddon-continues-another-year-as-2027-memory-capacity-is-reportedly-sold-out">Now That 2027 RAM Manufacturing Capacity Has Reportedly Been Sold Through, It&#x27;s Hard To Imagine the RAMageddon Ending Any Time Soon</a></li>
<li><a href="https://famiboards.com/threads/memory-capacity-for-all-of-2027-has-reportedly-been-booked-and-sold-with-no-more-dram-or-hbm-available-digitimes-report.18266/">Memory capacity for all of 2027 has reportedly been booked and sold, with no more DRAM or HBM available (Digitimes report) | Famiboards</a></li>
<li><a href="https://en.wikipedia.org/wiki/2025%E2%80%93present_global_memory_supply_shortage">2025–present global memory supply shortage - Wikipedia</a></li>
<li><a href="https://intuitionlabs.ai/articles/ram-shortage-2025-ai-demand">RAM Shortage 2025: How AI Demand is Raising DRAM Prices | IntuitionLabs</a></li>
<li><a href="https://medium.com/@Elongated_musk/memory-supercycle-how-ais-hbm-hunger-is-squeezing-dram-and-what-to-own-79c316f89586">Memory Supercycle: How AI’s HBM Hunger Is Squeezing DRAM (and What to Own) | by elongated_musk | Medium</a></li>

</ul>
</details>

**标签**: `#memory`, `#HBM`, `#hardware`, `#semiconductors`, `#AI infrastructure`

---

<a id="item-tech-news-8"></a>
### [与爬虫搏斗一年：150 万页网站的成本与对策](https://patronview.com/news/99-percent-of-my-website-traffic-is-bots/) ⭐️ 7.0/10

一位网站运营者分享了其在拥有 150 万页面的站点上对抗爬虫与机器人流量一整年的经历，重点记录了检测手段、Cloudflare 等防护方案以及成本冲击：正常月成本约 90 美元，在一次糟糕的高峰月份账单上涨约 500%。评论者补充了具体案例，例如 Claude 的搜索爬虫在 72 小时内抓取约 20.5 万页、仅带来 1 次推荐，说明高抓取量并不等于真实用户收益。该话题还牵出开放网络担忧：把“谁能访问网站”的判断外包给大型公司可能让用户无声失去访问权。整体上，这是一次具体运营挑战，而非技术突破。

hackernews · petercooper · 8月7日 14:51 · [社区讨论](https://news.ycombinator.com/item?id=49211386)

**「背景」** PatronView 是一个关于慈善捐赠者数据的网站，其运营者记录了过去一年与爬虫和机器人流量斗争的经验。网站规模约 150 万页，曾有一天收到来自中国机器人的 360 万次请求，Cloudflare 报告称其网站与 Anthropic 爬虫的访问量比约为每带来一位访客就有 35,000 次抓取。这类问题在依赖公共数据并希望向真实用户提供免费信息的站点中尤为突出，典型的应对手段包括使用 Cloudflare 等托管防护、基于工作量证明的浏览器验证（如 Anubis），以及通过分析用户代理和行为特征识别爬虫。

**「影响」** 运营内容型网站并公开数据的开发者会面临类似成本风险；采用静态站点或工作量证明方案可能降低负担，但依赖 Cloudflare 等第三方会引发可访问性控制的担忧。

**「社区讨论」** 评论者普遍认同机器人流量问题的严重性，但存在分歧：一些人担心将访问控制外包给 Cloudflare 违背开放网络理念，另一些人推荐 Anubis 的工作量证明方案作为非 Cloudflare 站点的有效缓解手段；还有人引用自家站点被 Claude 搜索爬虫抓取 20.5 万页却仅带来 1 次引荐，并点出“抓取者抱怨被抓取”的讽刺。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://patronview.com/news/99-percent-of-my-website-traffic-is-bots/">99% of My Website Traffic Is Bots | PatronView</a></li>

</ul>
</details>

**标签**: `#web scraping`, `#bot detection`, `#Cloudflare`, `#website infrastructure`, `#operations`

---

<a id="item-tech-news-9"></a>
### [Meta 在儿童心理健康案中被判巨额赔偿](https://www.theguardian.com/technology/2026/aug/06/new-mexico-court-meta) ⭐️ 7.0/10

2026 年 8 月 6 日，美国新墨西哥州法院裁定 Meta 因其社交平台对儿童心理健康的伤害承担责任，多家媒体报道的金额口径不一：Guardian 和 Reuters 称 Meta 需支付 5.67 亿美元用于青少年心理健康基金，而 WSJ 的标题则写为 9.42 亿美元。裁决依据是新墨西哥州公共妨害法（NMSA 1978 § 30-8-1），认定 Meta 的行为危害公共健康、安全或福利，并要求其为未成年用户做出产品变更。这是美国州法院针对大型平台算法与未成年人心理健康关系作出的重大追责裁决，可能影响未来对社交媒体公司的监管与诉讼。

hackernews · boplicity · 8月7日 00:06 · [社区讨论](https://news.ycombinator.com/item?id=49204352)

**「背景」** 美国新墨西哥州法院在一起具有里程碑意义的诉讼中，认定 Meta 旗下 Instagram 和 Facebook 等平台助长了青少年的心理健康危机。陪审团裁定 Meta 故意违反该州的《不公平做法法》，法官随后要求 Meta 支付 5.67 亿美元，设立一项“治理基金”，用于补救其平台对青少年造成的伤害，包括为受影响的年轻人提供治疗。此案是该诉讼第二阶段的结果，此前新墨西哥州总检察长依据该州公共妨害法起诉 Meta，指控其平台通过算法向青少年推送有害内容。

**「影响」** 对 Meta 而言，这笔款项虽可能只占其全球营收的一小部分，但按新墨西哥州约 200 万人口折算，属于金额极高的判决；Meta 需要为该州未成年用户调整产品设计并承担财务成本，其他州也可能借鉴此案推动类似诉讼。

**「社区讨论」** 评论者一方面认为 5.67 亿或 9.42 亿美元对 Meta 全球营收只是“经营成本”，另一方面指出新墨西哥州人口仅约 200 万，因此这笔判决按人均计算非常重。还有人分享了对 Instagram Reels 和 TikTok 成瘾性滚动的亲身经历，并担忧各国若继续限制未成年人使用社交媒体，Meta 未来的收入增长和股价可能承压。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.pbs.org/newshour/nation/new-mexico-court-orders-meta-to-pay-567-million-over-mental-health-harms-to-kids-online">New Mexico court orders Meta to pay $567 million over mental health harms to kids online | PBS News</a></li>
<li><a href="https://www.cnbc.com/2026/08/06/meta-to-pay-into-567-million-fund-after-child-harms-case-new-mexico.html">Meta ordered to pay $567 million into abatement fund as remedy to child harms case in New Mexico</a></li>
<li><a href="https://www.nytimes.com/2026/08/06/technology/meta-new-mexico-child-safety.html">Meta Ordered to Pay $567 Million Fine by New Mexico Judge - The New York Times</a></li>

</ul>
</details>

**标签**: `#legal`, `#social media`, `#meta`, `#mental health`, `#regulation`

---

<a id="item-tech-news-10"></a>
### [Wyzer：面向分布式安全的新编程语言](https://github.com/Wyzer-Lang/wyzer) ⭐️ 7.0/10

Wyzer 是一种静态类型、编译型、面向资源的编程语言，旨在通过编舞编程（choreographic programming）和 Perceus 内存管理实现分布式安全，弥补 Rust 安全保证中的空白。作者因 Rust 无法防止分布式死锁、跨服务协议不匹配和正确性问题而启动该项目。Wyzer 使用线性/仿射类型和引用计数而不是借用检查器和生命周期，这使得语言服务器协议（LSP）在计算上更容易理解。经过 5 个月的研究和数周的开发，作者即将发布 0.1.0 版本，并欢迎社区贡献。

hackernews · v0id\_isgood · 8月7日 12:28 · [社区讨论](https://news.ycombinator.com/item?id=49209385)

**「背景」** 编舞编程是一种编程范式，它从全局视角描述分布式节点之间的交互，然后编译为各节点的本地实现，从而能够在编译期静态检查无死锁和协议一致性。Perceus 是一种基于引用计数并支持内存复用的内存管理技术，可以在不引入借用检查器的情况下实现内存安全。

**「影响」** 对于分布式系统和编程语言设计领域的研究者及开发者，Wyzer 提供了一种早期尝试，将编舞编程引入实用编译语言，可能有助于减少分布式死锁问题；但由于 0.1.0 尚未正式发布，其实际可行性和性能表现仍需验证。

**「社区讨论」** 评论者赞赏该项目的雄心和不同于主流语言的创新方向，同时建议在文档中增加更多示例并重点解释新概念。也有人对如何保证分布式无死锁表示怀疑，并关注内部函数调用与外部函数调用的区分以及超时处理等实际问题。

**标签**: `#programming-language`, `#distributed-systems`, `#choreographic-programming`, `#memory-safety`, `#rust`

---

<a id="item-tech-news-11"></a>
### [Codex 与 GPT-5.6 Sol Ultra 生成的《Moonlight &amp; Mayhem》胜过 Claude Fable 5](https://simonwillison.net/2026/Aug/7/moonlight-mayhem/#atom-everything) ⭐️ 7.0/10

西蒙·威利森使用完全相同的提示词，将 Codex Desktop 搭配 GPT-5.6 Sol Ultra 的“激进子代理”模式与 Claude Fable 5 进行对比，结果 Codex 生成了更好的游戏《Moonlight &amp; Mayhem》。该游戏设定在一座博物馆中，玩家需要营救两只浣熊队友并叠罗汉取出金色沙丁鱼，而 Claude Fable 5 的版本只是单只浣熊在后院收集硬币和鱼。Codex 初次生成时存在一个明显 bug，每只浣熊头顶都有一个巨大黑色球体眼球，且 Codex 在开发中查看截图时未能发现，最终通过追问“为什么浣熊身上有巨大黑色球体”并指示“修复它”解决。Codex 总计耗时 52 分钟；根据 AgentsView 估算，若按 API 全价计费，该会话成本约为 23.28 美元，涉及 70.07 万输入 token、3250 万缓存 token 和 14.8 万输出 token。完整 Codex 转录和修复提交已公开在 GitHub 仓库中。

rss · Simon Willison · 8月7日 19:18

**「背景」** 西蒙·威利森此前使用 Claude Fable 5 依据一个由 GPT-3 和 DALL-E 在四年前生成的创意一次性构建出完整可玩的《Raccoon Heist》游戏。本次对比中，他使用同一提示词测试 Codex Desktop 的 GPT-5.6 Sol Ultra 模式，该模式会大量使用子代理来并行处理开发任务。

**「影响」** 对评估 AI 编程工具的开发者来说，这次对比提供了具体证据：Codex 的子代理模式在复杂游戏生成上能产出更完整、更具主题性的结果，但初版仍存在视觉 bug，说明自动化代理也需要人工审查和后续修复；用户可以直接试玩游戏并查看公开的代码仓库与完整对话记录。

**标签**: `#AI code generation`, `#LLM comparison`, `#Claude`, `#Codex`, `#GPT-5.6`

---

<a id="item-tech-news-12"></a>
### [Token 末日：企业正急于控制 AI Token 成本](https://simonwillison.net/2026/Aug/7/pdfs-are-terrible/#atom-everything) ⭐️ 7.0/10

404 Media 于 6 月 24 日报道，随着 AI Token 消耗激增，企业正竞相削减 AI 支出。据泄露的埃森哲会议录音，埃森哲 agentic AI 战略负责人 Justice Kwak 表示，内部数据显示 Token 消耗主要来自非工程师，而非工程师；客户团队负责人 Stuart Henderson 则提到，将 PDF 转换为 markdown 是“最大的 Token 消耗者之一”，Kwak 确认这与公司数据一致。Simon Willison 评论道，如果埃森哲能认识到 PDF 不是传达信息的理想媒介，或许能向商业世界推广这一教训。该报道基于泄露的内部讨论，反映企业 AI 成本压力正从工程师扩展到更广泛的非技术用户行为。

rss · Simon Willison · 8月7日 16:18

**「背景」** 大型语言模型按“词元”（token）计费，模型会将文本切分为词元后再处理，因此像把 PDF 转换成 Markdown 这类需要读取整份文档并重新生成文本的任务会消耗大量词元，从而推高企业的 AI 使用费用。根据 404 Media 获得的埃森哲（Accenture）泄露会议录音，非工程师员工的日常 AI 操作（例如把 PDF 转成幻灯片）正成为“词元消耗大户”，埃森哲内部也出现“token 支出飙升”并考虑限制员工的 AI 使用。404 Media 将这一现象称为“Tokenpocalypse”的开端。

**「影响」** 对依赖 PDF 等非结构化文档的 AI 企业客户而言，非工程人员大量进行 PDF 到 markdown 转换会显著推高 Token 成本，促使企业加速实施成本控制措施；但该结论基于埃森哲内部泄露讨论，缺乏公开数据支撑。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.404media.co/the-tokenpocalypse-is-here-companies-are-scrambling-to-stop-spending-so-much-on-ai/">The Tokenpocalypse Is Here: Companies Are Scrambling To Stop ...</a></li>
<li><a href="https://finance.yahoo.com/technology/ai/articles/tokenpocalypse-companies-quietly-throttle-ai-180600952.html?fr=sycsrp_catchall">The &#x27;Tokenpocalypse&#x27; is here: Companies quietly throttle AI ...</a></li>
<li><a href="https://www.newsbreak.com/the-cool-down-314855763/4739709234465-the-tokenpocalypse-is-here-companies-quietly-throttle-ai-as-token-bills-pile-up">The &#x27;Tokenpocalypse&#x27; is here: Companies quietly throttle AI ...</a></li>

</ul>
</details>

**标签**: `#AI costs`, `#token usage`, `#PDF conversion`, `#enterprise AI`, `#cost optimization`

---

<a id="item-tech-news-13"></a>
### [shadow-utils 4.20.0 移除密码过期与旧散列功能](https://lwn.net/Articles/1086949/) ⭐️ 7.0/10

shadow-utils 4.20.0 按计划移除了多项与定期密码过期相关的功能：expiry 命令被删除，/etc/shadow 第四字段（最小密码年龄）被忽略并在出现时移除；同时删除了 groupmems、logoutd，并移除 DES 和 MD5 密码散列算法支持，默认散列改为 SHA512（除非 login.defs 中定义 ENCRYPT\_METHOD）。这些移除从 4.19.0（2025 年 12 月）开始弃用，目的是配合 NIST 800-63B 不再强制要求、甚至禁止验证系统强制定期改密的新规范。仍可通过 passwd -e 或 getent 等命令处理部分密码过期场景，但依赖强制定期改密的组织应准备在未来几年内完全失去这些功能。

rss · LWN.net · 8月7日 15:54

**「背景」** shadow-utils 是 Linux 上管理 /etc/shadow、/etc/passwd 等用户与组数据库的工具集，密码过期功能至少可追溯到 1996 年。过去为防止未授权访问，系统常强制用户定期更换密码；但 2015 年研究认为其安全收益很小，NIST 800-63B 也从不再推荐改为在 2025 年修订版中明确禁止验证方强制要求定期改密，这成为本次移除的动因。

**「影响」** 依赖强制定期密码过期策略或旧密码散列算法的组织与管理员需要调整审计、合规或认证流程，不能再直接使用 expiry、最小密码年龄或 DES/MD5 散列；受影响系统应显式设置 login.defs 中的 ENCRYPT\_METHOD，并改用 passwd -e 等方式处理密码失效。

**标签**: `#shadow-utils`, `#Linux`, `#password-expiration`, `#security`, `#system-administration`

---

<a id="item-tech-news-14"></a>
### [SK 海力士确认 V10 NAND：375 层堆叠并首次采用晶圆键合](https://www.gelonghui.com/live/2599953) ⭐️ 7.0/10

SK 海力士在 FMS 2026 峰会新闻稿中确认，其新一代 V10 NAND 闪存采用 375 层堆叠设计，是继 321 层 V9“4D NAND”之后的产品。这也是 SK 海力士首款采用晶圆键合技术的 NAND 产品。官方宣称，V10 NAND 实现上代产品 2.5 倍的每瓦性能，专为需要兼顾能效和性能的 AI 基础设施环境优化。

telegram · zaihuapd · 8月7日 12:19

**「背景」** 3D NAND 闪存通过垂直堆叠存储单元层数来提升容量和密度，层数越多通常代表技术越先进。SK 海力士此前已量产 321 层的 V9“4D NAND”，此次 V10 将层数提升至 375 层，并首次在 NAND 产品中引入晶圆键合技术——该技术也在被三星用于其 400 层以上的 V10 BV-NAND。SK 海力士基于 V10 的企业级 SSD 预计在 2027 年初量产，而整个 FMS 2026 峰会上，多家厂商正围绕 AI 存储需求比拼更高层数、功耗和性能。

**「影响」** 对 AI 基础设施的存储规划者而言，V10 NAND 的高堆叠层数和晶圆键合工艺预示着未来大容量闪存可在能效与性能之间取得更优平衡，但具体量产时间和实际成本尚未披露。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ajupress.com/view/20260805101311102">Samsung, SK hynix wage next battle for AI memory leadership at FMS</a></li>
<li><a href="https://www.odaily.news/en/post/5212378">MSX US Stock Daily Watch: FMS 2026 Storage Summit: HBF... - Odaily</a></li>
<li><a href="https://www.blocksandfiles.com/flash/2026/08/04/fms-storage-ticker-4-aug-2026/5282932">FMS Storage Ticker - 4 Aug 2026</a></li>

</ul>
</details>

**标签**: `#NAND`, `#SK Hynix`, `#semiconductors`, `#AI hardware`, `#wafer bonding`

---

<a id="item-tech-news-15"></a>
### [sub2api 曝 OAuth 高危漏洞，仅凭邮箱即可接管账户](https://github.com/Wei-Shaw/sub2api/issues/5350) ⭐️ 7.0/10

sub2api v0.1.171 及之前版本存在一个 CVSS 8.8 的高危 OAuth 账户接管漏洞。攻击者仅需知道受害者注册邮箱，无需密码、验证码或用户交互，即可通过接口将攻击者的 OAuth 身份绑定到受害者账户，从而完全控制其 API 密钥、账单余额与订阅配额。该漏洞源于 pending session 流程中 existingUser 分支未校验密码和验证码，攻击者将目标用户 ID 设为受害者后即可完成 OAuth 身份绑定，之后每次 OAuth 登录都会解析为受害者账户。相关讨论已在 GitHub Issue 中公开，使用该项目的用户应尽快关注修复或升级。

telegram · zaihuapd · 8月7日 14:59

**「背景」** sub2api 是一个用于分发和管理 AI 产品订阅 API 配额的网关平台，用户通过平台生成的 API 密钥访问上游 AI 服务，平台负责认证、计费、负载均衡和请求转发。该项目的登录流程采用 OAuth，并在处理待定会话（pending session）的 existingUser 分支时缺乏对密码和验证码的校验，从而为账户接管漏洞埋下隐患。

**「影响」** 使用 sub2api v0.1.171 及之前版本的用户面临账户被完全接管的风险，包括 API 密钥、账单余额和订阅配额失控；项目维护者应立即发布修复版本并提醒受影响用户轮换密钥。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://uuithub.com/Wei-Shaw/sub2api">GitHub Wei-Shaw/ sub 2 api LLM Context</a></li>
<li><a href="https://github--com.proxy.hfzk.net.cn/Wei-Shaw/sub2api">GitHub - Wei-Shaw/ sub 2 api : Sub 2 API ...</a></li>

</ul>
</details>

**标签**: `#security`, `#vulnerability`, `#OAuth`, `#account-takeover`, `#sub2api`

---

<a id="item-tech-news-16"></a>
### [亚马逊 AWS 严查内部 CPU 浪费，智能体 AI 推高算力需求](https://www.tomshardware.com/pc-components/cpus/amazon-cracks-down-on-cpu-waste-among-engineers-as-agentic-ai-crunch-intensifies-cpu-demand-makes-low-utilization-ec2-instances-a-hot-commodity) ⭐️ 7.0/10

亚马逊 AWS 正在严格审查工程师对 EC2 实例的使用浪费。今年 5 月，公司要求工程师减少 CPU 浪费以确保客户容量，导致内部申请实例的等待时间从此前数小时延长至数天，有工程师表示工作多年从未等过这么久。这一压力源于智能体 AI 工作负载的崛起，与传统推理任务不同，智能体 AI 工作流涉及大量运行在 CPU 上的工具调用和更复杂的 GPU 编排，使数据中心 GPU 与 CPU 配比从过去的 8:1 或 4:1 逐步逼近 1:1。AMD 和英伟达均已加大数据中心 CPU 布局以争夺这一市场。

telegram · zaihuapd · 8月7日 16:31

**「背景」** 智能体 AI 是一种能够自主执行多步骤任务的 AI 系统，其工作流不仅依赖 GPU 进行模型推理，还涉及大量工具调用、逻辑判断和编排任务，这些任务主要运行在 CPU 上。传统 AI 推理的算力需求以 GPU 为主，数据中心通常采用较高的 GPU 与 CPU 配比，而智能体 AI 的普及正在改变这一配比，使得 CPU 需求显著上升。

**「影响」** AWS 内部工程师申请 EC2 实例的等待时间从数小时延长至数天，可能拖慢内部项目开发进度，而客户容量保障则优先于内部使用。随着智能体 AI 工作负载增长，云服务商可能需要在 CPU 资源分配上做出更多调整。

**标签**: `#AWS`, `#EC2`, `#agentic AI`, `#CPU`, `#data center infrastructure`

---

## 科技博客

<a id="item-tech-blog-1"></a>
### [SpaceX 2027 年 10GW 与微软最大承购展望](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) ⭐️ 1.0/10

rss · SemiAnalysis · 8月7日 20:08

**「背景」** 作者在一篇预告中提出一个大胆预测：SpaceX 将在 2027 年达到 10GW 供电能力，并带动自身年收入增至 3000 亿美元，而微软将成为最大承购方。原文内容非常简短，只有标题和要点，没有展开论证。

**「方案」** 作者给出的支撑点包括：按每 GW 每年千亿次推理计算，SpaceX 的部署节奏“惊人”；微软从 2026 年起有 10GW 需求“觉醒”，Azure 有望实现三位数增长，因此会成为最大买家。但这些只是断言，原文没有提供模型、合同、成本或卫星产能等细节，也无法验证数字口径。这里的价值更多是识别议题——AI 推理电力需求可能让卫星能源成为新赛道。

**「启示」** 作者认为 SpaceX 的卫星电力业务将因 AI 推理需求爆发而成为千亿美元级生意，微软是其关键客户；不过上述结论目前只是一则宣称，仍需完整研究支持。

**标签**: `#SpaceX`, `#Microsoft Azure`, `#AI inference`, `#data center power`, `#satellite`

---

<a id="item-tech-blog-2"></a>
### [Gemini 长期失利，GCP 短期受益](https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking) ⭐️ 1.0/10

rss · SemiAnalysis · 8月7日 02:32

**「背景」** 作者在标题中提出一个判断：Gemini 在长期上会失败，而 DeepMind 的这种长期失利反而是 Google Cloud（GCP）的短期收益；副标题把因果凝练为“长期失败”带来“短期收益”。

**「方案」** 原文目前只有标题和副标题，没有正文或数据支撑。因此，无法还原作者如何论证 Gemini 的长期问题、失败通过什么机制让 GCP 短期受益，也无法确认其中的时间线、市场条件或具体业务逻辑。现有信息只表明作者持有这一观点，且区分了“长期”与“短期”两种不同影响：DeepMind 的困境可能在短期内有利于 GCP，但这种推测并未展开。

**「启示」** 如果作者论述成立，那么 Gemini 与 GCP 的命运可能存在时间差：长期失利不排除短期收益。但源内容过于简略，读者需借助原始文章才能判断这一论断是否可靠。

**标签**: `#Gemini`, `#GCP`, `#AI`, `#DeepMind`, `#business strategy`

---

## 财经新闻

<a id="item-finance-news-1"></a>
### [纳斯达克 23 小时交易制获 SEC 批准，12 月 6 日上线](https://finance.sina.com.cn/stock/bxjj/2026-08-07/doc-inimnkup0012339.shtml) ⭐️ 9.0/10

美国证券交易委员会（SEC）已批准纳斯达克的 23 小时交易制度（23/5），将于 2026 年 12 月 6 日上线；届时美股每个交易日仅休市 1 小时（美东时间 20:00 至 21:00）用于系统清算和数据处理。

telegram · zaihuapd · 8月7日 10:03

**「背景」** 此前 NYSE Arca 已获 SEC 加速批准将交易延长至每日 22 小时，Cboe 也提交了近 24×5 的提案，目标均为 2026 年 12 月。在交易所正式延长时段前，散户已通过 Blue Ocean ATS 等另类交易系统进行隔夜交易，Robinhood、嘉信理财等平台也已提供延长时段服务。

**标签**: `#Nasdaq`, `#SEC`, `#trading hours`, `#US stock market`, `#regulation`

---

<a id="item-finance-news-2"></a>
### [7 月非农意外减少后，市场大幅下调美联储 9 月加息概率](https://www.cnbc.com/2026/08/07/odds-the-fed-hikes-in-september-tumble-following-big-july-jobs-miss.html) ⭐️ 8.0/10

7 月非农就业意外减少后，市场对美联储 9 月加息的预期大幅下降：预测平台 Kalshi 显示 9 月按兵不动概率升至 65%，CME FedWatch（根据联邦基金期货）也升至 60%；此前两项数据分别约为 50%和 45%。

rss · CNBC Finance · 8月7日 13:34

**「背景」** 美联储 7 月会议维持利率不变，但有三名政策委员反对，主张加息；此前 2026 年劳动力市场一直持续增长，如果就业转弱，进一步加息以压低经济会被视为风险更大。

**「影响」** 若 9 月维持利率，家庭和企业的借贷成本短期内不会因加息而上升；但 CME FedWatch 显示 10 月仍有约 55%的加息概率、12 月约 75%，年内政策走向尚不确定。

**标签**: `#Federal Reserve`, `#Jobs Report`, `#Interest Rates`, `#Monetary Policy`, `#Market Expectations`

---

<a id="item-finance-news-3"></a>
### [特朗普再签行政令限制美国出生公民权](https://www.bbc.co.uk/news/articles/cj63966j95yo) ⭐️ 8.0/10

美国总统特朗普 8 月 6 日签署两项行政令，再次尝试限制出生公民权：一项扩大父母双方均非美国公民时子女不自动获得公民身份的情形（涉及外国恐怖组织成员、外国政府雇员等），另一项禁止孕妇赴美“生育旅游”。法律专家称新令存在严重宪法问题，美国公民自由联盟预测其将在法庭败诉。

telegram · zaihuapd · 8月7日 07:01

**「背景」** 今年 6 月 30 日，美国最高法院以 6 比 3 裁定特朗普 2025 年上任首日签署的类似行政令违宪，确认出生公民权仍是法律；白宫则辩称新令通过重新解释出生公民权的历史例外，不在该裁决管辖范围内。

**标签**: `#birthright citizenship`, `#immigration policy`, `#executive order`, `#Supreme Court`, `#US politics`

---

<a id="item-finance-news-4"></a>
### [美国审查中国 AI 企业海外获取英伟达芯片渠道](https://www.bloomberg.com/news/articles/2026-08-07/us-reviews-china-s-offshore-access-to-nvidia-chips-after-ai-breakthroughs) ⭐️ 8.0/10

美国商务部工业与安全局（BIS）正系统审查中国 AI 企业如何通过海外云计算等方式获取和使用英伟达芯片，以回应近期中国模型性能突破引发的担忧。此次审查是在白宫官员指控月之暗面非法获取英伟达芯片并经泰国远程访问后启动的，美国众议院已通过两党法案拟明确授权 BIS 限制此类云计算协议，但预计将遭到英伟达等科技公司反对。

telegram · zaihuapd · 8月7日 11:18

**「背景」** 美国商务部工业与安全局（BIS）负责执行芯片出口管制，但现有规则主要限制芯片实体出口，是否涵盖中国公司租用海外云计算算力的“远程访问”方式存在法律空白；美国众议院已于今年 1 月通过《远程访问安全法案》（H.R. 2683），拟明确授权 BIS 监管这类远程访问，但法案仍在参议院等待审议。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.techtimes.com/articles/323532/20260807/bis-targets-legal-cloud-compute-china-ai-firms-bypass-export-controls.htm">BIS Targets Legal Cloud Compute as China AI Firms Bypass Export Controls</a></li>
<li><a href="https://thenextweb.com/news/us-bis-review-china-remote-offshore-nvidia-chip-access">US reviews China&#x27;s remote access to Nvidia chips</a></li>

</ul>
</details>

**标签**: `#export-controls`, `#US-China tech rivalry`, `#Nvidia`, `#AI policy`, `#cloud-computing`

---

<a id="item-finance-news-5"></a>
### [北京非京籍购房社保年限下调至 1 年，公积金贷款额度同步提高](https://www.peopleapp.com/column/30052875352-500007640471) ⭐️ 8.0/10

北京市住建委等部门宣布，非京籍居民家庭购买五环内商品住房的社保或个税缴纳年限，调整为购房之日前连续缴纳满 1 年及以上。同时，首套住房公积金贷款最高额度提高至 240 万元，符合城六区户籍在区外购房、绿色建筑、多子女家庭等条件的最高可再上浮 100 万元。

telegram · zaihuapd · 8月7日 13:57

**「背景」** 此前 2025 年 12 月，北京已将非京籍家庭购买五环内商品住房的社保或个税缴纳年限由 3 年下调至 2 年；本次进一步降至 1 年，意味着非京籍家庭在京购房门槛已降至历史最低水平。

**「影响」** 这一政策将降低非京籍居民家庭在北京五环内购房的社保门槛，并提高公积金贷款支持上限，可能带动符合条件的购房需求释放。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://emwap.eastmoney.com/a/202608073835569636.html">北京新政：非京籍五环内购房社保年限降至1年，公积金最高可贷340万元 _ 东方财富网</a></li>

</ul>
</details>

**标签**: `#北京房地产`, `#限购政策`, `#公积金贷款`, `#中国楼市`, `#政策宽松`

---