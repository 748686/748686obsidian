---
layout: default
title: "Horizon Summary: 2026-08-01 (ZH)"
date: 2026-08-01
lang: zh
---

> 从 46 条内容中筛选出 17 条重要资讯。

---

**科技新闻**
1. [Tailscale 复盘 Hugging Face 入侵：密钥重用是教训](#item-tech-news-1) ⭐️ 8.0/10
2. [DeepSeek 发布 V4-Flash-0731：304B 参数、低价高性能 AI 模型](#item-tech-news-2) ⭐️ 8.0/10
3. [MCP 2.0 无状态规范发布，Willison 推出 mcp-explorer 与 datasette-mcp](#item-tech-news-3) ⭐️ 8.0/10
4. [德国法院裁定 Suno 侵犯版权](#item-tech-news-4) ⭐️ 8.0/10
5. [电梯调度算法：从 SCAN 到目的地派梯的深度解析](#item-tech-news-5) ⭐️ 7.0/10
6. [qm：面向工作的多智能体协作开源框架](#item-tech-news-6) ⭐️ 7.0/10
7. [Arch Linux 因恶意接管关闭 AUR 孤儿包领养](#item-tech-news-7) ⭐️ 7.0/10
8. [联邦法官质疑证据，Anthropic 禁令或永久撤销](#item-tech-news-8) ⭐️ 7.0/10
9. [MiniMax H3 多模态视频模型将于 2026 年 8 月 3 日开源](#item-tech-news-9) ⭐️ 7.0/10

**科技博客**
1. [面向快速长上下文推理的注意力协同设计指南](#item-tech-blog-1) ⭐️ 8.0/10

**财经新闻**
1. [AI 对冲基金 Situational Awareness 在动量崩溃中爆仓，资产从 450 亿美元缩水至约 100 亿美元](#item-finance-news-1) ⭐️ 8.0/10
2. [纽约州起诉预测平台 Kalshi，称其非法赌博并索赔最高 360 亿美元](#item-finance-news-2) ⭐️ 8.0/10
3. [盘前主要个股波动：亚马逊涨 11%、苹果跌 7%、Replimune 涨 130%、诺和诺德跌 10%](#item-finance-news-3) ⭐️ 8.0/10
4. [Clear Street 推出 Pre-IPO 平台，向合格投资者开放 Databricks 等私营公司投资](#item-finance-news-4) ⭐️ 7.0/10
5. [美股午盘异动：亚马逊大涨、苹果下跌](#item-finance-news-5) ⭐️ 7.0/10
6. [三位美联储官员反对维持利率不变，呼吁立即加息遏制通胀](#item-finance-news-6) ⭐️ 7.0/10
7. [特朗普政府拟向留学生收 10 万美元毕业后工作费](#item-finance-news-7) ⭐️ 7.0/10

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [Tailscale 复盘 Hugging Face 入侵：密钥重用是教训](https://tailscale.com/blog/hugging-face-intrusion) ⭐️ 8.0/10

Tailscale 公布了对 Hugging Face 安全入侵事件的复盘：事件中没有 Tailscale 漏洞被利用，但 Hugging Face 环境变量文件中的可重用认证密钥被攻击者复制到外部沙箱，随后在数天内注册了大量 CI 节点进入其 tailnet。这些节点获得 CI 身份标签，因此拥有自动化测试节点所需的访问权限。Tailscale 表示，作为安全工具，这次入侵也是自身的责任，甚至比发现自身漏洞更令人不安。该事件凸显 mesh VPN 场景下长期有效的 auth key、环境变量中的凭据存储以及 CI 节点接入权限都可能是关键风险点。

hackernews · bluehatbrit · 7月31日 19:03 · [社区讨论](https://news.ycombinator.com/item?id=49127306)

**「背景」** Tailscale 是一种基于 WireGuard 的 mesh VPN，组织内的设备通过 tailnet 互联；认证密钥（auth key）可让新设备无需人工批准自动加入，其中可重用密钥尤其方便也尤其危险。CI 节点通常动态创建，若密钥写入环境变量并进入外部沙箱，攻击者就可能借其注册任意节点并获得相应身份标签。

**「影响」** 使用 Tailscale 或其他 mesh VPN 的组织应将所有 auth key 视为高价值机密，优先使用短期、可撤销且绑定来源/目标节点的密钥，并为新节点入网配置告警，避免重蹈因环境变量泄露而被批量注册节点的覆辙。

**「社区讨论」** 评论者中有人赞赏 Tailscale 主动公开复盘，认为这是可信的安全态度；也有人认为文章是展示高级功能的巧妙营销，同时指出把可重用 auth key 写入环境变量如同把钥匙留在门口。还有用户建议加入安全体检功能，并提议让长周期凭据绑定 CI 编排来源和节点身份，同时为新节点注册增加告警机会。

**标签**: `#security`, `#Tailscale`, `#Hugging Face`, `#CI-CD`, `#credentials`

---

<a id="item-tech-news-2"></a>
### [DeepSeek 发布 V4-Flash-0731：304B 参数、低价高性能 AI 模型](https://simonwillison.net/2026/Jul/31/deepseek-v4-flash-0731/#atom-everything) ⭐️ 8.0/10

DeepSeek 发布了其 V4 系列新模型 DeepSeek-V4-Flash-0731，参数规模为 3040 亿，Hugging Face 上权重约 167GB，官方称其“智能体能力大幅增强”。该模型在 Artificial Analysis 的智能指数上超越了 428B 参数的 MiniMax M3，每百万输入 token 收费 0.14 美元、每百万输出 token 收费 0.27 美元，被认为是当前“单位智能性价比”最高的模型。Simon Willison 通过 OpenRouter 实测发现，默认推理级别生成的“骑自行车鹈鹕”图像质量较差，但将 reasoning\_effort 设为 high 后得到了明显更好的结果。

rss · Simon Willison · 7月31日 23:59

**「背景」** DeepSeek-V4-Flash-0731 是 DeepSeek V4 系列的最新发布版本，属于稀疏混合专家（MoE）模型；OpenRouter 的资料显示其总参数量为 284B、激活参数约 13B，是一个面向编程、推理和智能体工作流的“重新训练后”修订版（来源：tool-1-2）。Hugging Face 模型页提供了该模型的直接加载方式，DeepInfra 的说明则称其在多项基准上优于 DeepSeek-V4-Pro \(Preview\)，尽管激活参数更少，并与最强的闭源模型大致相当（来源：tool-1-1, tool-1-3）。原报道把模型规模记为 304B 参数、Hugging Face 下载约 167GB，并引用 Artificial Analysis 的评测称其性价比突出。

**「影响」** 对于通过 OpenRouter 使用该模型的开发者，V4-Flash-0731 以约 0.028 美元/任务的成本提供了约 50 分的智能指数，使其在实际任务中成为性价比极具竞争力的选择，但默认推理级别下的输出质量可能不稳定，需要根据任务手动调高推理强度。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731">deepseek -ai/ DeepSeek - V 4 - Flash - 0731 · Hugging Face</a></li>
<li><a href="https://openrouter.ai/deepseek/deepseek-v4-flash-0731">DeepSeek V 4 Flash 0731 - API Pricing &amp; Providers | OpenRouter</a></li>
<li><a href="https://deepinfra.com/deepseek-ai/DeepSeek-V4-Flash-0731">deepseek -ai/ DeepSeek - V 4 - Flash - 0731 - Demo - DeepInfra</a></li>

</ul>
</details>

**标签**: `#AI models`, `#DeepSeek`, `#LLM`, `#Agentic AI`, `#Machine Learning`

---

<a id="item-tech-news-3"></a>
### [MCP 2.0 无状态规范发布，Willison 推出 mcp-explorer 与 datasette-mcp](https://simonwillison.net/2026/Jul/31/stateless-mcp/#atom-everything) ⭐️ 8.0/10

2026 年 7 月 28 日发布的 Model Context Protocol 2.0（又称 stateless MCP）是 MCP 自发布以来最重要的规范更新，将原来的两次 HTTP 请求（先初始化会话获取 Mcp-Session-Id，再调用工具）简化为一次携带 MCP-Protocol-Version、Mcp-Method 和 Mcp-Name 头的请求。Simon Willison 认为这大幅降低客户端和服务端实现复杂度，也更适合无状态可扩展的 Web 应用。基于新规范，他发布了 mcp-explorer（可用 uvx 直接运行，用于列出、检查和调用 MCP 服务器的 CLI）和 datasette-mcp（给 Datasette 实例增加 /-/mcp 端点，提供 list\_databases、get\_database\_schema 和只读 execute\_sql 三个工具）。目前 datasette-mcp 已运行在 datasette.simonwillison.net/-/mcp，并接入了 ChatGPT 与 Claude。MCP 由 Anthropic 于 2024 年 11 月提出，此前曾因 Skills 等方案而热度下降，但 stateless 版本重新吸引了作者的兴趣。

rss · Simon Willison · 7月31日 23:13

**「背景」** Model Context Protocol（MCP）是 Anthropic 在 2024 年 11 月提出的开放协议，用于统一描述 LLM 智能体如何调用外部工具。旧版 MCP 采用有状态会话，客户端需要先 POST initialize 获取服务端分配的会话 ID，再在后续调用中携带该 ID；新版无状态 MCP 通过请求头直接标识协议版本、方法和工具名，单次请求即可完成调用。

**「影响」** 开发者现在可以用 \`uvx mcp-explorer\` 快速探测和调用任何兼容 stateless MCP 的服务器，并可为 Datasette 实例启用 \`/-/mcp\` 端点，让 ChatGPT、Claude 等代理直接对托管数据库执行（当前只读的）SQL 查询。

**标签**: `#MCP`, `#AI`, `#developer tools`, `#protocols`

---

<a id="item-tech-news-4"></a>
### [德国法院裁定 Suno 侵犯版权](https://www.dw.com/en/german-court-rules-that-ai-music-firm-suno-violated-copyrights/a-78152227) ⭐️ 8.0/10

德国慕尼黑地区法院裁定美国 AI 音乐公司 Suno 侵犯版权，须披露非法所得并支付数额待定的赔偿。Suno 表示不认同判决，将评估包括上诉在内的所有选项。该诉讼由德国音乐版权集体管理组织 GEMA 于 2025 年 1 月提起，指控 Suno 未经许可和补偿，使用受版权保护的音乐训练 AI 模型。庭审中 GEMA 演示了 Suno 生成的歌曲与原作品高度相似；这是全球首批检验版权法如何适用于 AI 音乐训练的重大案件之一，GEMA 代表德国逾 9.5 万名音乐人及全球超 200 万名权利持有人。

telegram · zaihuapd · 7月31日 13:11

**「背景」** GEMA 是德国的音乐作品著作权集体管理组织，负责为音乐作品发放使用许可并收取版税，再分配给权利人。AI 音乐公司训练模型时若使用受版权保护的录音或乐谱，通常需要获得权利人的授权或付费许可，否则可能构成侵权。Suno 等新兴 AI 音乐生成公司此前主张训练属于合理使用或无须额外许可。

**「影响」** 该裁决可能推动 AI 音乐公司改变训练数据来源，主动取得音乐版权许可或选择已授权数据，同时为其他国家的 AI 版权诉讼提供了参考。

**标签**: `#AI版权`, `#法律裁决`, `#音乐生成`, `#知识产权`, `#产业影响`

---

<a id="item-tech-news-5"></a>
### [电梯调度算法：从 SCAN 到目的地派梯的深度解析](https://john.fun/elevators) ⭐️ 7.0/10

文章《Elevators》在 john.fun 上发表，深入解析电梯调度算法，结合模拟和现实观察，将电梯系统类比为绕轴旋转的“长电梯”，并指出 SCAN 本是磁盘调度算法。文章还讨论了目的地派梯（Destination Dispatch），称其在随机目的地模拟中通常表现更差，而现实中乘客常同时按上下按钮反而成为更大问题。该内容在 Hacker News 引发工程师广泛讨论，有人分享 Elevator Saga 模拟游戏和相关手游设计经验。这不是突发新闻，而是从工程视角对常见系统的技术深潜，适合对调度算法感兴趣的开发者阅读。

hackernews · Jrh0203 · 7月31日 15:17 · [社区讨论](https://news.ycombinator.com/item?id=49124218)

**「背景」** 电梯算法（又称 SCAN）最初是磁盘调度算法，用于决定磁盘臂和磁头在服务读写请求时的运动方式：它沿一个方向移动并处理途中请求，到达一端后再反向，类似电梯在楼层间往返。这个背景有助于理解文章将电梯调度与磁盘调度（SCAN/LOOK）联系起来的讨论，也解释了评论中提到的现实建筑里目的地调度系统（Destination Dispatch）为何会与随机目的地模拟结果不同。

**「影响」** 主要影响是让工程师群体重新审视电梯调度与磁盘调度之间的算法联系，并在社区中引导出大量关于目的地派梯实际效果和模拟工具（如 Elevator Saga）的实践讨论。

**「社区讨论」** 评论者整体认同电梯调度与磁盘调度（SCAN/LOOK）的类比，但有人质疑“目的地派梯在随机场景下更差”的结论可能源于模拟假设；多位开发者分享了用 Elevator Saga 做实验、在游戏中实现 LOOK 算法并优先等待时间更长楼层的经验，也有评论指出乘客误按上下按钮才是实际使用中的最大痛点。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Elevator_algorithm">Elevator algorithm - Wikipedia</a></li>

</ul>
</details>

**标签**: `#elevator-algorithms`, `#disk-scheduling`, `#SCAN`, `#destination-dispatch`, `#simulation`

---

<a id="item-tech-news-6"></a>
### [qm：面向工作的多智能体协作开源框架](https://github.com/yc-software/qm) ⭐️ 7.0/10

qm 是一个新发布的开源多智能体 harness，代码位于 yc-software/qm，目标是面向工作场景的多智能体协作。该项目在 Hacker News 上引发讨论，核心亮点是将重点放在作用域（scoping）上，通过 per-person scopes 与 shared rooms 来管理多智能体的协作边界。项目由 YC 生态相关人员发布，被视为对公司级助手作用域问题的一种合理回答。它面临 Claude Cowork 等现有工具的竞争，社区中也出现了直接对比的需求。

hackernews · tosh · 7月31日 18:04 · [社区讨论](https://news.ycombinator.com/item?id=49126604)

**「背景」** QM（仓库 yc-software/qm）是 YC Software 发布的一个开源“多人智能体工作框架”，定位为让多个 AI 代理在公司内协作，支持 Slack 和 Web 端。传统多数代理按“个人助理”设计，很难直接扩展为全公司使用；QM 面向初创公司，尝试通过按人员划分作用域和共享房间来简化这种扩展。该仓库还包含 CLAUDE.md 说明文件与 Issues 讨论区，项目本身仍在早期阶段。

**「影响」** 对构建多智能体工作助手的开发者而言，qm 提供了一种按用户作用域加共享房间的组织方式，可能降低将多个 agent 引入团队协作时的混乱；但它还需要证明自己相对于 Claude Cowork 等已有方案的优势。

**「社区讨论」** 一些评论者肯定 qm 对作用域问题的处理，认为 per-person scopes 与 shared rooms 是对公司级助手难题的合理方案；同时也有质疑认为现有工具如 Claude Cowork 可能更成熟、功能更丰富，并希望能看到 qm 与 Cowork 的对比。另有评论分享了 agent 自主安排会议的趣事，以及 Garry Tan 的 gstack 等类似方向的项目。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/yc-software/qm">GitHub - yc-software/qm: Multiplayer agent harness for work · GitHub</a></li>

</ul>
</details>

**标签**: `#ai-agents`, `#open-source`, `#multi-agent`, `#agent-harness`, `#yc`

---

<a id="item-tech-news-7"></a>
### [Arch Linux 因恶意接管关闭 AUR 孤儿包领养](https://lwn.net/Articles/1086489/) ⭐️ 7.0/10

Arch Linux DevOps 团队宣布，由于“当前一波通过 AUR 进行的恶意包领养和后续提交”，已禁用对 Arch 用户仓库（AUR）中孤儿包的领养功能。Michael Taggart 的简要分析显示，本轮攻击添加的载荷疑似为远程访问木马（RAT），通过 Tor 网络接收命令，并试图上传大量用户数据。此前项目已因类似攻击于 6 月暂停新账户注册，7 月 13 日重新开放，但新增的限制措施显然未能生效。此举旨在阻断攻击者领养孤儿包后推送恶意更新的供应链攻击路径。

rss · LWN.net · 7月31日 13:38

**「背景」** AUR 是 Arch 社区维护的软件包仓库，包含用户提交的 PKGBUILD 等构建脚本；当维护者弃用某个包时，它成为孤儿包，其他用户可申请领养并继续更新。攻击者利用这一机制领养知名孤儿包，再向其中加入恶意代码，用户通过 AUR 助手或手动安装时就会在系统上执行恶意内容。

**「影响」** Arch 用户在攻击期间安装或更新被恶意接管的 AUR 孤儿包，可能会执行 RAT 并被窃取数据；禁用领养可阻止新的恶意接管，但已下发的恶意包仍可能影响用户系统。

**标签**: `#security`, `#Arch Linux`, `#AUR`, `#malware`, `#open-source`

---

<a id="item-tech-news-8"></a>
### [联邦法官质疑证据，Anthropic 禁令或永久撤销](https://techcrunch.com/2026/07/30/judge-says-trump-admin-still-lacks-evidence-for-anthropic-supply-chain-risk-label/) ⭐️ 7.0/10

美国联邦地区法官 Rita Lin 在周四听证会上表示，特朗普政府仍未提供足够证据，证明将 Anthropic 列为「供应链风险」并禁止联邦政府使用其 AI 技术的决定合理。政府以 Anthropic 公开批评国防部为由实施封禁，Lin 称这一逻辑「非常令人不安」，可能开创对与政府意见不合的联邦承包商进行报复的先例，并指出案卷记录「在某些方面对政府而言变得更糟了」。争端源于 Anthropic 与国防部合同谈判破裂：Anthropic 要求其 AI 不被用于大规模监控或致命武器决策，而国防部认为私营企业不应规定军方如何使用技术。Anthropic 已于 3 月提起两起诉讼，Lin 此前临时叫停封禁，目前正考虑是否永久撤销，政府律师则称计划在 9 月 30 日前完成停用 Anthropic 产品。

telegram · zaihuapd · 7月31日 08:00

**「背景」** Anthropic 是一家美国人工智能公司，其与国防部就合同条款谈判破裂，原因是 Anthropic 要求其 AI 不得用于大规模监控或致命武器决策，而国防部认为企业不应限制军方技术使用。2026 年 3 月，Anthropic 就国防部的封禁提起诉讼；此前法官 Rita Lin 已临时叫停该封禁，政府则称将在 9 月 30 日前完成停用 Anthropic 产品。政府将 Anthropic 列为“供应链风险”的理由包括其公开批评国防部，以及担忧所谓“AI 模型投毒”，但法官称未看到具体依据。

**「影响」** 若法院作出永久禁令，将直接阻止政府在 9 月 30 日前停用 Anthropic 产品的计划，并可能限制政府以承包商批评政策为由实施供应链封禁的做法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://techcrunch.com/2026/07/30/judge-says-trump-admin-still-lacks-evidence-for-anthropic-supply-chain-risk-label/">Judge says Trump admin still lacks evidence for Anthropic ‘supply-chain risk’ label | TechCrunch</a></li>
<li><a href="https://www.axios.com/2026/07/30/judge-pentagon-case-worse-anthropic">Judge says government&#x27;s case got &quot;worse&quot; in Anthropic fight</a></li>
<li><a href="https://www.politico.com/news/2026/07/30/anthropic-supply-chain-risk-lawsuit-hearing">Trump admin has not justified labeling Anthropic a national security risk, judge says - POLITICO</a></li>

</ul>
</details>

**标签**: `#AI policy`, `#Anthropic`, `#legal`, `#US government`, `#supply-chain risk`

---

<a id="item-tech-news-9"></a>
### [MiniMax H3 多模态视频模型将于 2026 年 8 月 3 日开源](https://modelscope.cn/models/MiniMax/MiniMax-H3) ⭐️ 7.0/10

MiniMax 宣布其新一代通用多模态视频模型 H3 将于 2026 年 8 月 3 日在魔搭社区（ModelScope）开源发布。该模型原生支持文本、图像、音频和视频的理解与生成，可综合解析人物、动作、声音、情感、镜头语言及创作意图，并融合多种参考素材进行连贯创作。它还具备多维度精准编辑控制能力，面向影视、广告、品牌、电商与游戏等商业场景，可生成包含字幕、品牌信息、特效、产品展示及 UI 动态演示在内的多样化内容。此次开源意味着开发者可在魔搭社区获得该模型，但具体使用条件和技术细节尚未公布。

telegram · zaihuapd · 7月31日 12:37

**「背景」** 多模态视频模型是一种能够同时理解并生成文本、图像、音频和视频的 AI 模型，适用于视频创作、编辑和内容生成等任务。MiniMax H3 是 MiniMax 公司推出的新一代通用多模态视频模型；此次将模型开源到魔搭社区，标志着该模型进入公开可用阶段。

**「影响」** 开源后，影视、广告、品牌、电商与游戏等领域的开发者可直接使用 H3 生成字幕、品牌信息、特效、产品展示及 UI 动态演示等内容，从而加速多模态内容的制作流程。不过，由于模型尚未正式发布，其实际效果和性能仍需以开源后的测试为准。

**标签**: `#multimodal`, `#video generation`, `#open source`, `#MiniMax`, `#AI model`

---

## 科技博客

<a id="item-tech-blog-1"></a>
### [面向快速长上下文推理的注意力协同设计指南](https://developer.nvidia.com/blog/co-designing-ai-model-attention-for-fast-interactive-long-context-inference/) ⭐️ 8.0/10

rss · NVIDIA Inference Performance Blog · 7月31日 22:16

**「背景」** 在智能体与长上下文推理中，上下文长度不断增长，注意力计算逐渐主导推理开销；仅优化内核实现已不够，模型架构本身需要围绕 GPU 的执行方式来设计。作者以 GEMM 形状分析和实测数据为基础，比较了预填充与解码两个阶段的不同瓶颈。

**「方案」** 作者指出，预填充阶段 GEMM-M 很大、受计算限制，而解码阶段每次只生成一个 token、受 KV 缓存带宽限制。基于 FlashAttention 的两个矩阵乘法形状，他们系统分析了组大小、头维度和序列长度的影响：增加组大小几乎不改变预填充运行时，却能让解码算术强度约等于 2 倍组大小，因此应尽量选择较大的组大小；头维度不改变算术强度，但 128 或 256 才能对齐 GPU tile 与 128 字节访存，且较大的头还能在预填充中摊销 softmax 开销；序列长度使预填充按二次方增长、解码按线性增长，所以应通过 KV 缓存压缩、稀疏或滑动窗口注意力等方式减少有效 KV 状态。最后，张量并行受 KV 头数量限制，应保持 TP 不超过 KV 头数，否则会复制 KV 状态；对于 KV 头很少的模型，可用注意力数据并行或 KV 并行配合专家并行扩展。文章给出了四条可直接用于模型设计的协同设计清单。

**「启示」** 作者的核心结论是：在长上下文推理中，注意力架构选择应当以 GPU 的 GEMM 形状和内存带宽特性为依据，而不仅是关注精度或实现优化。通过协调组大小、头维度、序列长度和并行策略，可以在不牺牲准确率的前提下显著提升吞吐与交互性。

**标签**: `#attention mechanism`, `#GPU inference`, `#long context`, `#model co-design`, `#tensor parallelism`

---

## 财经新闻

<a id="item-finance-news-1"></a>
### [AI 对冲基金 Situational Awareness 在动量崩溃中爆仓，资产从 450 亿美元缩水至约 100 亿美元](https://www.cnbc.com/2026/07/31/why-leopold-aschenbrenner-situational-awareness-hedge-fund-imploded.html) ⭐️ 8.0/10

利奥波德·阿申布伦纳（Leopold Aschenbrenner）的人工智能主题对冲基金 Situational Awareness 遭遇创纪录的动量崩溃后爆仓，被迫以折价将所有杠杆股票头寸卖给 Citadel，管理规模从约 450 亿美元缩水至约 100 亿美元。据知情人士称，该基金同时做多 AI 基础设施股、做空软件股，结果多头和空头双双亏损。

rss · CNBC Finance · 7月31日 16:14

**「背景」** 阿申布伦纳曾在 OpenAI 工作，2024 年 7 月创立该基金，并因一篇关于超级人工智能的 165 页文章而成名；截至爆仓前，基金自成立以来曾上涨超过 1000%。此次波动中，标普 500 指数看似平稳，但 BTIG 的分析师称这是现代史上最大、最快的动量崩溃，即此前领涨的股票被集中抛售。

**「影响」** 强制平仓加剧了 AI 基础设施股近几周的下跌；随后投资者将其视为技术性错位，相关股票出现反弹。

**标签**: `#hedge fund`, `#AI`, `#momentum crash`, `#market disruption`, `#deleveraging`

---

<a id="item-finance-news-2"></a>
### [纽约州起诉预测平台 Kalshi，称其非法赌博并索赔最高 360 亿美元](https://www.cnbc.com/2026/07/31/new-york-sues-kalshi-claims-it-is-illegal-gambling-operation.html) ⭐️ 8.0/10

纽约州在州法院起诉预测市场平台 Kalshi，指控其未经州博彩监管机构注册、以“非法赌博”方式运营，要求法院发布永久禁令，并寻求最高约 360 亿美元的罚款和赔偿。

rss · CNBC Finance · 7月31日 15:31

**「背景」** Kalshi 总部位于纽约，自称受联邦商品期货交易委员会（CFTC）监管；此前 Kalshi 和 CFTC 已分别起诉纽约州，纽约州则主张体育赛事合约属于州级体育博彩监管范围。

**「影响」** 若诉讼推进，Kalshi 在纽约州乃至全美的运营将面临不确定性，而这场联邦与州监管权之争也会影响其他预测市场平台及其用户。

**标签**: `#prediction-markets`, `#regulation`, `#lawsuit`, `#New York`, `#CFTC`

---

<a id="item-finance-news-3"></a>
### [盘前主要个股波动：亚马逊涨 11%、苹果跌 7%、Replimune 涨 130%、诺和诺德跌 10%](https://www.cnbc.com/2026/07/31/stocks-making-the-biggest-moves-premarket-repl-cvx-aapl-amzn-mrna.html) ⭐️ 8.0/10

盘前最大波动的个股中，亚马逊因第二季度云业务收入同比增长 37%、超出市场预期的 31%，股价大涨逾 11%；苹果虽然 iPhone 销量增长 22%带动财季收入超预期，股价仍下跌逾 7%。Replimune 因美国 FDA 咨询委员会支持其 RP1 皮肤癌试验结果而飙升逾 130%，诺和诺德则因 ziltivekimab 三期试验未能减少主要心血管事件而下跌逾 10%。

rss · CNBC Finance · 7月31日 12:30

**「背景」** 这些波动多来自最新季度财报或药品监管/临床试验消息；FDA 咨询委员会的支持票是审批流程中的参考性步骤，临床试验失败则意味着相关药物难以按原计划推进。

**标签**: `#earnings`, `#FDA advisory`, `#big tech`, `#pharmaceuticals`, `#premarket movers`

---

<a id="item-finance-news-4"></a>
### [Clear Street 推出 Pre-IPO 平台，向合格投资者开放 Databricks 等私营公司投资](https://www.cnbc.com/2026/07/31/clear-street-pre-ipo-platform-databricks.html) ⭐️ 7.0/10

金融科技券商 Clear Street 即将推出平台，允许合格投资者在 IPO 前投资晚期私营公司，首个标的是本月估值 1880 亿美元的 AI 公司 Databricks。Clear Street 表示，到年底平台将上最多 30 家初创公司。

rss · CNBC Finance · 7月31日 21:49

**「背景」** Clear Street 是一家曾搁置自身 IPO 计划的主经纪商初创公司。该平台并非直接购买 Databricks 股票，而是通过特殊目的载体（SPV）持有第三方基金权益；Databricks 表示与 Clear Street 没有关系。

**「影响」** 该平台让合格投资者有机会在 IPO 前接触高成长科技公司，但投资者获得的是 SPV 间接权益，且需自行承担相关风险。

**标签**: `#Fintech`, `#Private Markets`, `#Pre-IPO`, `#Databricks`, `#SPV`

---

<a id="item-finance-news-5"></a>
### [美股午盘异动：亚马逊大涨、苹果下跌](https://www.cnbc.com/2026/07/31/stocks-making-the-biggest-moves-midday-aapl-amzn-rddt-gddy-iesc.html) ⭐️ 7.0/10

美股午盘多只个股因最新财报出现剧烈波动：亚马逊大涨 15%，其云业务收入同比增长 37%，超过市场预期的 31%；苹果下跌逾 9%，尽管季度营收超预期且 iPhone 销售增长 22%。其他显著异动包括 Reddit 跌 22%、GoDaddy 跌 20%、IES Holdings 涨 30%。

rss · CNBC Finance · 7月31日 17:42

**「背景」** 这些波动是在多家公司发布最新季度业绩后出现的，投资者根据实际业绩与市场预期的差距迅速调整仓位。

**标签**: `#earnings`, `#stock movers`, `#Amazon`, `#Apple`, `#market reaction`

---

<a id="item-finance-news-6"></a>
### [三位美联储官员反对维持利率不变，呼吁立即加息遏制通胀](https://www.cnbc.com/2026/07/31/fed-officials-who-voted-to-hike-rates-say-action-is-needed-now-against-inflation.html) ⭐️ 7.0/10

克利夫兰联储的哈马克、明尼阿波利斯的卡什卡里和达拉斯的洛根三位官员反对维持利率不变，主张立即加息以应对通胀。目前美联储政策利率保持在 3.5%-3.75%，通胀高于 2%目标已超过五年。

rss · CNBC Finance · 7月31日 14:35

**「背景」** 美联储其余九位投票委员支持按兵不动；此前在 2025 年下半年曾连续三次降息，近期通胀因能源价格、中东局势和关税等因素再度走高。

**标签**: `#Federal Reserve`, `#monetary policy`, `#inflation`, `#interest rates`, `#FOMC`

---

<a id="item-finance-news-7"></a>
### [特朗普政府拟向留学生收 10 万美元毕业后工作费](https://www.bloomberg.com/news/articles/2026-07-30/trump-weighs-100-000-fee-for-foreign-students-to-work-post-grad) ⭐️ 7.0/10

特朗普政府正考虑向国际学生收取 10 万美元费用，以获准通过选择性实践培训（OPT）项目毕业后留美工作；白宫官员称暂无即将出台的政策变化，但未否认正在讨论。据知情人士，去年秋季近 30 万国际学生持 OPT 留美，该政策仍在酝酿中。

telegram · zaihuapd · 7月31日 09:00

**「背景」** 这是政府收紧国际学生政策的最新动作：本月初国土安全部已将学生签证居留期限缩短为四年；政府还拟对 H-1B 签证收取同等费用，但 6 月被联邦法官裁定违法，白宫正在上诉。

**「影响」** 若实施，依赖国际学生学费的高校以及聘用国际毕业生的硅谷和华尔街企业将受到直接冲击。

**标签**: `#immigration policy`, `#international students`, `#OPT`, `#higher education`, `#labor market`

---