---
layout: default
title: "Horizon Summary: 2026-08-17 (ZH)"
date: 2026-08-17
lang: zh
---

> 从 26 条内容中筛选出 8 条重要资讯。

---

**科技新闻**
1. [Anthropic 发布 Claude 系统提示词，开发者追踪版本差异](#item-tech-news-1) ⭐️ 8.0/10
2. [Qwen 3.8 27B 能力出色，但默认过度思考需调低推理档位](#item-tech-news-2) ⭐️ 8.0/10
3. [Linux 内核 7.2 发布：引入 BPF、调度器及文件系统多项改进](#item-tech-news-3) ⭐️ 8.0/10
4. [模型正被有意变笨：转向外部知识与工具调用](#item-tech-news-4) ⭐️ 7.0/10
5. [Cloudflare 切换域名服务器后静默注入分析脚本](#item-tech-news-5) ⭐️ 7.0/10
6. [AI 追踪 Telegram 盗版：61 天关闭 524 个频道](#item-tech-news-6) ⭐️ 7.0/10

**科技博客**
1. [PJM 建模错误致 120 亿美元浪费](#item-tech-blog-1) ⭐️ 2.0/10

**财经新闻**
1. [Anthropic 第二季初步营收超 115 亿美元，同比增逾 14 倍](#item-finance-news-1) ⭐️ 8.0/10

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [Anthropic 发布 Claude 系统提示词，开发者追踪版本差异](https://platform.claude.com/docs/en/release-notes/system-prompts) ⭐️ 8.0/10

Anthropic 在官方文档的发布说明中公开了 Claude 的系统提示词，让外界能够看到指导这一前沿模型行为的隐藏指令。这些说明复盖 Opus 4.8、Opus 5 等版本，开发者 Simon Willison 还将其整理成 git 提交历史以便追踪变化，并指出 Opus 4.8 到 Opus 5 的差异中最值得注意的新增内容提到了 Claude Fable 5 与 Claude Mythos 5 的首次发布。这被视作主要 AI 厂商在透明度方面的罕见举动，为开发者提供了了解模型被如何约束的窗口。不过，这仍是一次文档发布而非新模型或技术突破，社区中也出现了关于系统提示词是否过长、是否反而影响模型表现的讨论。

hackernews · tosh · 8月16日 12:48 · [社区讨论](https://news.ycombinator.com/item?id=49319556)

**「背景」** Anthropic 在其 Claude 平台文档中发布了官方系统提示词（system prompts），这些提示词通常是大模型隐藏的运行指令，用于设定模型行为、边界和输出偏好。此前这类内容很少被厂商主动公开，因此这次发布被视为提高模型透明度的重要举措，也让开发者能研究 Claude 在不同版本间的指令变化。

**「影响」** 开发者和研究人员现在可以直接查看官方发布的 Claude 系统提示词及其版本差异，更准确地理解模型行为约束，并借助社区维护的 git 历史高效追踪变更。

**「社区讨论」** 社区反应积极但存在分歧：Simon Willison 制作了 git 历史以方便追踪提示词变化，但一些开发者认为这些系统提示词过长且包含大量未必适用的内容，可能分散模型注意力；还有人质疑提示词中加入“图片是否存在”这类常识性规定。另有用户借此表达了对 HN 删除负面 AI 报道的担忧。

**标签**: `#AI`, `#Claude`, `#system prompts`, `#transparency`, `#LLM`

---

<a id="item-tech-news-2"></a>
### [Qwen 3.8 27B 能力出色，但默认过度思考需调低推理档位](https://simonwillison.net/2026/Aug/16/qwen-38-27b/) ⭐️ 8.0/10

阿里巴巴 Qwen 实验室发布 Apache 2 许可的 27B 参数视觉语言模型 Qwen 3.8 27B，官方自报基准测试同时超越了前代 Qwen 3.6 27B 和闭源 Qwen 3.7-Plus。Simon Willison 在 128GB M5 Max MacBook Pro 和 NVIDIA DGX Spark 上通过 LM Studio 的 17GB Q4\_K\_M 量化版进行实测，发现模型默认的 xhigh 推理档位会导致严重过度思考：为生成“鹈鹕骑自行车”SVG 消耗 22,276 个推理 token 并耗时 21 分钟，而关闭推理后仅需约 137 秒。将 LM Studio 默认 8,192 token 上下文改为 262,144 才能避免上下文被思考过程占满。作者强烈建议先使用 low 或关闭推理档位运行该模型，并称其边界框等视觉能力表现良好，但独立基准测试仍有待观察。

rss · Simon Willison · 8月16日 22:00

**「背景」** Qwen 3.8 27B 是阿里巴巴 Qwen 实验室的开源视觉语言模型，27B 参数规模适合在配置较好的笔记本电脑本地运行，前代 Qwen 3.6 27B 已获得不错评价。该系列通过 reasoning\_effort 参数（xhigh/medium/low）控制推理深度，但官方默认值为最高的 xhigh，这会显著增加 token 消耗和延迟。

**「影响」** 对本地部署该模型的开发者和爱好者，最直接的教训是应先手动把 reasoning\_effort 设为 low 或关闭，否则简单任务也可能等待数分钟并耗尽上下文；是否值得升级仍待独立测试确认。

**标签**: `#Qwen`, `#LLM`, `#open-source`, `#AI benchmarks`, `#model deployment`

---

<a id="item-tech-news-3"></a>
### [Linux 内核 7.2 发布：引入 BPF、调度器及文件系统多项改进](https://lwn.net/Articles/1088991/) ⭐️ 8.0/10

Linux 内核 7.2 已正式发布。Linus Torvalds 表示最后一周补丁比预期多，但按“新常态”仍按时发布。主要特性包括 bpf\(\) 系统调用的通用属性支持、CPU 调度器的缓存感知负载均衡、Btrfs 大 folio、swap 子系统改进、Landlock 安全模块增强，以及通过 dm-inlinecrypt 目标支持内联加密硬件。更完整的变更可见 LWN 合并窗口摘要和 KernelNewbies 7.2 页面。

rss · LWN.net · 8月16日 23:11

**「背景」** Linux 内核是操作系统底层核心，版本号采用主版本.次版本.补丁形式，7.2 是 7.x 系列的更新版本。新内核通常集成来自开发者的改进，并需要发行版或用户自行编译后使用。

**「影响」** 对于依赖 BPF、Btrfs 和存储加密的用户与开发者，这些功能只有升级到 7.2 或包含该内核的发行版才能使用。

**标签**: `#linux-kernel`, `#bpf`, `#scheduler`, `#btrfs`, `#kernel-release`

---

<a id="item-tech-news-4"></a>
### [模型正被有意变笨：转向外部知识与工具调用](https://w4g1.dev/blog/models-are-getting-dumber-on-purpose) ⭐️ 7.0/10

一篇技术评论文章指出，AI 模型正在被有意设计得更小、更约束记忆，用可插拔知识库和工具调用替代把事实直接编码进权重。作者认为这种转变会影响幻觉的产生方式和模型生命周期，并可能导致模型卡不再列出知识截止日期，因为留在权重里的知识会以年而不是周为单位过时。文章引用 SimpleQA 上最佳纯事实召回模型约 53% 的表现作为支撑，强调当事实不在权重中时，错误可能转移到工具或检索链路。该观点引起了开发者关注，但也有评论认为文中引用的事实已经过时。

hackernews · hruvhwe · 8月16日 19:04 · [社区讨论](https://news.ycombinator.com/item?id=49322695)

**「背景」** 传统上，大语言模型把事实知识直接编码在权重中，因此存在知识截止日期和幻觉问题。这篇文章讨论的方向是有意缩小或约束模型内部记忆，转而通过可插拔知识库和外接工具调用获取事实信息。这种设计把“推理能力”与“事实知识”分离，可能影响模型卡中知识截止日期的意义，并改变模型生命周期。

**「影响」** 对正在选择模型架构的开发者而言，这篇文章把注意力从扩大参数规模转向外接知识库、工具调用和评估检索失败；但这更多是该文所主张的方向而非已确立的行业结果。

**「社区讨论」** 评论中，有开发者期待可插拔知识库按领域组合模型，另有评论认可方向但批评文章引用的 SimpleQA 和 Gemini 2.5 Pro 已过时；还有人质疑把推理与事实完全分离是否可行，因为要推理人类集体行为就离不开具体事实。

**标签**: `#AI`, `#LLM`, `#tool-augmented models`, `#knowledge bases`, `#model design`

---

<a id="item-tech-news-5"></a>
### [Cloudflare 切换域名服务器后静默注入分析脚本](https://news.ycombinator.com/item?id=49322107) ⭐️ 7.0/10

一名用户将域名服务器切换到 Cloudflare 以启用 R2 存储桶的独立子域服务后，发现 Cloudflare 在其纯 HTML、无 JavaScript 的网站 textlog.cc 中静默注入了 Web Analytics 的 JavaScript 片段。用户只有在进入 Analytics 仪表盘、添加站点后才能手动禁用该片段，他认为此类功能应当默认关闭而非需要用户退出。社区评论确认了这一行为，并展示了具体的 beacon.min.js 注入代码（如版本 2024.11.0 和 static.cloudflareinsights.com 地址），同时指出仅将 Cloudflare 用于 DNS 而不使用其代理时不会出现注入。这意味着可能受影响的站点所有者应检查自己的 Cloudflare Analytics 设置。

hackernews · stagas · 8月16日 17:49

**「背景」** Cloudflare 是一家提供 DNS、CDN 和 R2 对象存储等服务的公司。当用户将域名服务器切换到 Cloudflare 并通过其代理服务访问站点时，Cloudflare 可以在响应 HTML 中插入脚本；Web Analytics 是 Cloudflare 提供的流量分析产品，通过注入名为 beacon 的 JavaScript 来收集访问数据。该用户的问题正是在启用了 R2 子域服务并切换域名服务器后出现的。

**「影响」** 使用 Cloudflare 代理的站点所有者需要在 Analytics 仪表盘中手动停用 Web Analytics，否则其页面会默认加载 Cloudflare 的 beacon 脚本，这可能影响注重隐私或无脚本站点的预期行为。

**「社区讨论」** 评论中，有用户建议通过 Content-Security-Policy 的 script-src 指令限制脚本来源以阻止注入，另有用户展示了实际出现的 beacon.min.js 注入片段并给出 Cloudflare 官方博客链接；其他用户则表示在仅 DNS 模式下未观察到注入，因此认为该行为与启用 Cloudflare 代理有关。

**标签**: `#Cloudflare`, `#web analytics`, `#privacy`, `#JavaScript injection`, `#DNS`

---

<a id="item-tech-news-6"></a>
### [AI 追踪 Telegram 盗版：61 天关闭 524 个频道](https://torrentfreak.com/researchers-hunt-telegram-pirates-with-ai-tool-flag-hundreds-of-channels/) ⭐️ 7.0/10

研究人员分析了 1057 个 Telegram 频道中的约 20.9 万条帖子，发现 983 个频道涉及盗版内容，相关帖子累计浏览达 48.5 亿次，共涉及 19033 部影视作品。团队开发了名为 Anti-RIP 的 AI 工具，扫描约 24.9 万个新频道并标记 802 个疑似盗版频道，测试准确率达 98%。研究结果提交给 Telegram 及版权方后，61 天内有 524 个此前未知的盗版频道被关闭，但工具仍存在误报。该研究展示了 AI 在内容审核和版权执法中的实际应用，同时凸显了误报等技术局限性。

telegram · zaihuapd · 8月16日 09:13

**「背景」** Telegram 是一个即时通讯平台，其公开频道可以触达大量用户，部分频道会传播盗版影视内容。版权方和平台运营者长期以来很难靠人工在如此大的规模下发现并删除侵权内容。该研究尝试用机器学习工具自动标记可疑频道，依据的是帖子元数据和内容模式，而非单纯的逐条人工审核。

**「影响」** 对 Telegram 上的盗版频道运营者构成了直接打击，帮助版权方在两个月内关停 524 个频道；同时，误报问题意味着合法频道也可能面临被错误标记和关停的风险。

**标签**: `#AI`, `#content moderation`, `#copyright`, `#telegram`, `#machine learning`

---

## 科技博客

<a id="item-tech-blog-1"></a>
### [PJM 建模错误致 120 亿美元浪费](https://newsletter.semianalysis.com/p/12b-of-us-ratepayers-money-wasted) ⭐️ 2.0/10

rss · SemiAnalysis · 8月16日 22:27

**「背景」** 作者指出，美国最大电网运营商 PJM 因建模错误浪费了 120 亿美元电费，并正让费率支付者承担风险。这一论断强调电网容量市场的模型选择具有重大财务后果。

**「方案」** 文章将浪费归因于使用了错误的模型，并警告 PJM 仍打算再次采用同样的做法，使风险持续存在。作者认为这正是需要警惕的问题。

**「启示」** 核心结论是，电网建模失误可能造成数十亿美元的损失，若不纠正，代价将继续由费率支付者承担。

**标签**: `#PJM`, `#electricity modeling`, `#ratepayers`

---

## 财经新闻

<a id="item-finance-news-1"></a>
### [Anthropic 第二季初步营收超 115 亿美元，同比增逾 14 倍](https://www.cnbc.com/2026/08/15/anthropic-revenue-jumps-to-over-11point5-billion-in-q2-report.html) ⭐️ 8.0/10

据彭博社引述的文件，Anthropic 2026 年第二季初步营收超过 115 亿美元，同比增长逾 14 倍，高于去年同期的 7.87 亿美元与首季的 47.3 亿美元；当季调整后营业利润转正。公司正筹备可能在今秋启动的大型 IPO，数字为初步数据，仍可能调整。

telegram · zaihuapd · 8月16日 07:26

**「背景」** Anthropic 是开发 Claude 聊天机器人的 AI 初创公司，已经开始 IPO 流程，可能成为大型公开上市。本次公布的 Q2 数据为初步数字，仍可能调整；作为对比，2025 年 Q2 营收为 7.87 亿美元，2026 年 Q1 为 47.3 亿美元。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://nairametrics.com/2026/08/15/anthropics-revenue-surges-1360-to-11-5-billion-as-ipo-looms/">Anthropic’s revenue surges 1,360% to $11.5 billion as IPO ...</a></li>
<li><a href="https://www.zacks.com/featured-articles/761/anthropic-ipo">Anthropic IPO 2026 Guide: Price Predictions, Dates, and ...</a></li>

</ul>
</details>

**标签**: `#Anthropic`, `#revenue`, `#IPO`, `#AI`, `#earnings`

---