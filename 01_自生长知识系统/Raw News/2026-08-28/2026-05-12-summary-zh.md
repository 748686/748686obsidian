---
layout: default
title: "Horizon Summary: 2026-05-12 (ZH)"
date: 2026-05-12
lang: zh
---

> From 40 items, 16 important content pieces were selected

---

1. [UCLA 发现首个修复脑损伤的中风康复药物](#item-1) ⭐️ 10.0/10
2. [TanStack NPM 包遭供应链攻击含死亡开关](#item-2) ⭐️ 9.0/10
3. [GitLab 宣布裁员并终止 CREDIT 价值观](#item-3) ⭐️ 8.0/10
4. [Ratty：支持内联 3D 图形的终端模拟器](#item-4) ⭐️ 8.0/10
5. [Gmail 注册现在需要扫描二维码并发送短信](#item-5) ⭐️ 8.0/10
6. [CUDA-oxide：英伟达官方 Rust 转 CUDA 编译器](#item-6) ⭐️ 8.0/10
7. [AI 或使软件工程不再成为终身职业](#item-7) ⭐️ 8.0/10
8. [Shore：AI 编码代理必须降低维护成本](#item-8) ⭐️ 8.0/10
9. [Shopify 的 River 代理将 Slack 转变为公开教学工坊](#item-9) ⭐️ 8.0/10
10. [Linux 内核 7.0.6 和 6.18.29 修复 Dirty Frag 漏洞](#item-10) ⭐️ 8.0/10
11. [Debian 在测试版中强制可重现构建](#item-11) ⭐️ 8.0/10
12. [英特尔 Optane 构建本地运行 1 万亿参数模型，速度 4 tok/s](#item-12) ⭐️ 8.0/10
13. [Unsloth 发布支持 MTP 的 GGUF 模型](#item-13) ⭐️ 8.0/10
14. [MiniCPM 4.6 发布，文档理解能力提升](#item-14) ⭐️ 8.0/10
15. [Qwen 3.6 35B A3B 在小众代码理解上大幅提升](#item-15) ⭐️ 8.0/10
16. [冒充 OpenAI 隐私过滤器的恶意仓库登上 Hugging Face 趋势榜首](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [UCLA 发现首个修复脑损伤的中风康复药物](https://stemcell.ucla.edu/news/ucla-discovers-first-stroke-rehabilitation-drug-repair-brain-damage) ⭐️ 10.0/10

加州大学洛杉矶分校的研究人员发现了第一种药物 DDL-920，它通过恢复幸存神经元中的伽马振荡来修复中风引起的脑损伤。这一发现于 2025 年公布，代表了超越传统物理康复的突破。 这意义重大，因为它是首个逆转中风引起的脑损伤的药物干预，为无法进行高强度物理康复的患者提供了治疗可能。它还可能为治疗与伽马振荡缺陷相关的其他神经退行性疾病开辟途径。 药物 DDL-920 靶向小白蛋白神经元以恢复伽马振荡，这对协调的脑活动和运动恢复至关重要。该化合物是在小鼠和人类的成功物理康复显示恢复伽马振荡可修复神经连接后被确定的。

hackernews · bookofjoe · May 11, 17:53 · [社区讨论](https://news.ycombinator.com/item?id=48098261)

**背景**: 中风通常会导致梗死核心部位的脑细胞死亡，但周围“挫伤”的神经元可以恢复。伽马振荡是大脑节律（30-100 Hz），它将神经元连接成协调的网络，对运动和认知至关重要。中风后，这些振荡消失，物理康复可以随着时间的推移恢复它们。UCLA 的药物旨在无需高强度治疗的情况下化学模拟这种恢复。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Gamma_oscillations">Gamma oscillations</a></li>
<li><a href="https://medicalxpress.com/news/2025-03-drug-reestablishes-brain-mouse.html">First stroke rehabilitation drug that reestablishes brain connections...</a></li>
<li><a href="https://www.medindia.net/news/healthwatch/first-ever-drug-to-repair-brain-damage-caused-by-stroke-219297-1.htm">First-Ever Drug to Repair Brain Damage Caused by Stroke</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调，虽然该药物针对幸存神经元，但不能逆转梗死核心的细胞死亡。一些用户指出了化合物 DDL-920（通过 PubMed 链接），并推测其对其他神经退行性疾病的潜力。一条评论引用 Ted Chiang 的故事《Understand》，反映了对其影响的敬畏。

**标签**: `#stroke`, `#neuroscience`, `#drug discovery`, `#brain repair`, `#rehabilitation`

---

<a id="item-2"></a>
## [TanStack NPM 包遭供应链攻击含死亡开关](https://github.com/TanStack/router/issues/7383) ⭐️ 9.0/10

TanStack 及其他 npm 包在供应链攻击中被攻陷，攻击者部署了恶意 postinstall 脚本窃取令牌，并包含一个死亡开关，在令牌被撤销时擦除系统。 此事至关重要，因为 TanStack 被广泛用于 React 和 Web 开发；该攻击可能导致开发者及组织大规模令牌泄露和数据丢失，凸显了 npm 供应链的脆弱性。 恶意载荷在 Linux 上安装为 systemd 用户服务，在 macOS 上安装为 LaunchAgent，每 60 秒用窃取的令牌轮询 api.github.com/user，若令牌被撤销，则执行 rm -rf ~/ 擦除用户目录。

hackernews · varunsharma07 · May 11, 21:08 · [社区讨论](https://news.ycombinator.com/item?id=48100706)

**背景**: 供应链攻击是指攻击者攻陷受信任的软件包，以向用户分发恶意软件。npm 是 JavaScript 的流行包管理器，postinstall 脚本在包安装后自动运行，因此常被用作恶意软件传播的媒介。TanStack 是一套用于构建 Web 应用的开源库，包括 React Router 和 Query 等。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cyberpress.org/dead-mans-switch-widespread-npm-supply-chain-attack-driving-malware-attacks/">Dead Man’s Switch: Widespread npm Supply Chain Attack Driving ...</a></li>
<li><a href="https://docs.npmjs.com/cli/v8/using-npm/scripts/?v=true">scripts | npm Docs</a></li>

</ul>
</details>

**社区讨论**: 社区成员指出攻击的复杂性，包括死亡开关，并建议撤销令牌时谨慎。有人指出即使使用 Trusted Publishing，若 CI 被攻陷此类攻击仍可能发生，并批评 GitHub 的共享对象存储使恶意分支的提交与合法提交无法区分。

**标签**: `#security`, `#npm`, `#supply-chain-attack`, `#TanStack`, `#open-source`

---

<a id="item-3"></a>
## [GitLab 宣布裁员并终止 CREDIT 价值观](https://about.gitlab.com/blog/gitlab-act-2/) ⭐️ 8.0/10

GitLab 宣布了裁员计划，并用三个以人工智能为核心的新价值观（Speed with Quality、Ownership Mindset、Customer Outcomes）取代了其长期秉持的 CREDIT 核心价值观。这一转变是该公司将战略重心转向人工智能“代理时代”的一部分。 此举标志着 GitLab 公司文化和发展方向的重大转变，可能会影响员工士气和公司未来走向。将多元、包容与归属感从核心价值观中移除已招致批评，而过度聚焦人工智能也可能影响 GitLab 的产品开发和社区信任。 根据 GitLab 的博文，该公司认为“代理时代”提供了其历史上最大的机遇，并正在进行重组以迎接这一机遇。批评者指出，尽管大力宣传人工智能，但 GitLab 现有的人工智能功能因用户体验差而受到批评，且裁员与需要更多资源以增长的说法相矛盾。

hackernews · AnonGitLabEmpl · May 11, 20:51 · [社区讨论](https://news.ycombinator.com/item?id=48100500)

**背景**: GitLab 是一个 DevOps 平台，为软件开发生命周期提供单一应用程序。其 CREDIT 价值观（协作、客户成果、效率、多元化与包容性、迭代、透明）曾是公司文化的核心特征，强调协作、透明和多元。该公司现已决定放弃这些价值观，转而采用更以产品和 AI 为中心的方法，这很可能是为了应对市场压力和投资者需求。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://handbook.gitlab.com/handbook/values/">GitLab Values</a></li>
<li><a href="https://news.ycombinator.com/item?id=48100500">GitLab Announces Workforce Reduction and End of Their CREDIT ...</a></li>

</ul>
</details>

**社区讨论**: Hacker News 社区对 GitLab 的这一宣布普遍持批评态度。评论者对 DEI 价值观的移除表示失望，并认为这一转型是充满术语的迎合投资者的尝试。一些人质疑在声称公司历史上最大机遇的同时裁员的逻辑，另一些人则指出 GitLab 的 AI 功能长期存在用户体验问题。

**标签**: `#gitlab`, `#layoffs`, `#company-culture`, `#ai-strategy`, `#dei`

---

<a id="item-4"></a>
## [Ratty：支持内联 3D 图形的终端模拟器](https://ratty-term.org/) ⭐️ 8.0/10

Ratty 是一款新发布的 GPU 加速终端模拟器，能够通过自定义的 Ratty 图形协议，在传统文本输出中内联渲染 3D 模型。 这一创新模糊了终端与图形界面之间的界限，为命令行环境中的数据可视化、调试和沉浸式开发工作流开辟了新的可能性。 Ratty 使用 Rust 编写，采用 Ratatui 处理 UI，并利用 Bevy 进行 3D 渲染。它支持.obj 和.glb 模型，并提供包括 3D 透视模式在内的多种查看方式。

hackernews · orhunp_ · May 11, 10:13 · [社区讨论](https://news.ycombinator.com/item?id=48093100)

**背景**: 传统终端模拟器仅能显示文本，但 Sixel 和 Kitty 等协议已实现了内联图像。Ratty 将其扩展到 3D 领域，受 TempleOS 图形终端的启发，但针对现代系统和可用性进行了优化设计。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ratty-term.org/">Ratty — A GPU- rendered terminal emulator with inline 3 D graphics</a></li>
<li><a href="https://github.com/orhun/ratty">GitHub - orhun/ratty: A GPU-rendered terminal emulator with ...</a></li>
<li><a href="https://blog.orhun.dev/introducing-ratty/">Ratty: A terminal emulator with inline 3 D graphics - Orhun's Blog</a></li>

</ul>
</details>

**社区讨论**: Hacker News 上的评论将 Ratty 与历史上的 Xerox 工作站和 Lisp 机器进行比较，一些人强调其在 VR 或浅层 3D 界面方面的潜力。其他人则质疑通过 SSH 的性能表现，以及它是否能比现有方案更好地处理 2D 内容。

**标签**: `#terminal emulator`, `#3D graphics`, `#developer tools`, `#open source`, `#Hacker News`

---

<a id="item-5"></a>
## [Gmail 注册现在需要扫描二维码并发送短信](https://discuss.privacyguides.net/t/google-account-registration-now-requires-sending-an-sms-via-phone-instead-of-receiving-an-sms/36082) ⭐️ 8.0/10

Google 更新了 Gmail 注册流程，要求用户扫描二维码并从手机发送短信，而不是简单地接收验证短信。 这一变化增加了新用户注册的麻烦并引发隐私担忧，因为它强制要求发送短信来验证手机号码，可能会阻止用户注册并影响可访问性。 二维码会打开一个 SMS URI，预填好发送给 Google 的验证短信；并不会自动发送。这本质上还是之前的手机验证方式，只是通过二维码增加了便利性。

hackernews · negura · May 11, 07:26 · [社区讨论](https://news.ycombinator.com/item?id=48092028)

**背景**: Gmail 是拥有数十亿用户的广泛使用的电子邮件服务。电话号码验证长期以来一直是 Google 账户注册的一部分，以防止滥用，但过去通常只需要接收短信。这一改变现在要求用户发送短信，可能会产生费用或需要具备相应功能的手机。

**社区讨论**: 社区评论反应不一；有人理解 Google 打击垃圾邮件和滥用的需要，而其他人批评隐私影响，认为这是反竞争行为。有用户澄清二维码只是预填短信，并非自动发送。

**标签**: `#gmail`, `#privacy`, `#registration`, `#sms`, `#google`

---

<a id="item-6"></a>
## [CUDA-oxide：英伟达官方 Rust 转 CUDA 编译器](https://nvlabs.github.io/cuda-oxide/index.html) ⭐️ 8.0/10

英伟达发布了 CUDA-oxide，这是一个官方编译器，可以将 Rust 代码直接编译为 CUDA PTX，使得 Rust 程序员能够编写 GPU 内核而无需使用 C/C++。 这一桥梁将 Rust 的内存安全性与 CUDA 的高性能连接起来，有望显著降低 Rust 中 GPU 编程的门槛，扩展高性能计算和机器学习领域的生态系统。 CUDA-oxide 直接以 PTX（并行线程执行）为目标，绕过了 MLIR 或 Tile IR 等更高级的 IR；它是 NVIDIA Labs 的官方项目，托管在 GitHub 的 NVIDIA 组织下。

hackernews · adamnemecek · May 11, 15:55 · [社区讨论](https://news.ycombinator.com/item?id=48096692)

**背景**: CUDA 是 NVIDIA 专有的并行计算平台，允许 GPU 用于通用处理。PTX 是一种低级虚拟机和指令集架构，作为 CUDA 内核的中间表示。Rust 是一种现代系统编程语言，强调安全性和并发性。CUDA-oxide 使 Rust 能够编译为 PTX，从而允许 Rust 代码在 NVIDIA GPU 上运行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Cuda_platform">Cuda platform</a></li>
<li><a href="https://en.wikipedia.org/wiki/Parallel_Thread_Execution">Parallel Thread Execution - Wikipedia</a></li>
<li><a href="https://docs.nvidia.com/cuda/parallel-thread-execution/index.html">1. Introduction — PTX ISA 9.2 documentation</a></li>

</ul>
</details>

**社区讨论**: 评论者对于该项目可能成为现有 Rust CUDA crate 的即插即用替代品表示兴奋，并提出了关于构建时间和安全语义的问题。一些人质疑为何选择直接以 PTX 为目标而不是更高级的 IR，其他人则讨论了这对 Slang 等语言的影响。总体情绪是积极且好奇的，期待更多技术细节。

**标签**: `#Rust`, `#CUDA`, `#GPU`, `#compiler`, `#NVIDIA`

---

<a id="item-7"></a>
## [AI 或使软件工程不再成为终身职业](https://www.seangoedecke.com/software-engineering-may-no-longer-be-a-lifetime-career/) ⭐️ 8.0/10

一篇评论文章指出，依赖大型语言模型（LLM）等 AI 工具进行代码生成可能导致软件工程师技能退化，从而缩短其职业寿命。 这场讨论突显了科技行业对 AI 长期影响软件工程角色的日益关注，影响职业规划、招聘实践以及职业本身的性质。 文章区分了利用 AI 增强推理的工程师和用 AI 替代推理的工程师，警告后者可能随时间推移出现技术技能退化。

hackernews · movis · May 11, 14:34 · [社区讨论](https://news.ycombinator.com/item?id=48095550)

**背景**: 大型语言模型（LLM）是在海量文本数据上训练的深度学习模型，能够生成代码和自然语言。它们在软件开发中日益广泛的使用引发了争论：究竟是辅助还是取代人类专业知识？一些人视其为提升生产力的工具，另一些人则担忧它损害了基础技能的培养。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>
<li><a href="https://www.ibm.com/think/topics/large-language-models">What Are Large Language Models ( LLMs )? | IBM</a></li>

</ul>
</details>

**社区讨论**: 社区评论观点不一：一些开发者认为 AI 工具仅处理其工作的一小部分（2-5%的编码），而另一些人指出，有效使用 AI 的经验丰富的工程师效率更高。一位教师类比，那些用 AI 替代推理的学生可能会受影响，呼应了技能退化的担忧。也有人注意到招聘市场情绪转变，企业采取观望态度。

**标签**: `#software engineering`, `#AI`, `#career`, `#LLMs`, `#skill atrophy`

---

<a id="item-8"></a>
## [Shore：AI 编码代理必须降低维护成本](https://simonwillison.net/2026/May/11/james-shore/#atom-everything) ⭐️ 8.0/10

James Shore 认为，AI 编码代理必须按与其生产力提升相反的比例降低维护成本，否则会产生呈二次方增长的不可持续的维护负担。 这挑战了 AI 编码工具纯粹提升生产力的主流叙事，揭示了可能导致长期软件债务并阻碍工具采用的隐性成本。 Shore 的数学论证指出：如果 AI 将代码输出翻倍却不将维护成本减半，总维护成本将增加四倍（2×2）。只有当维护成本按相同倍数下降时，系统才能维持可持续性。

rss · Simon Willison · May 11, 19:48

**背景**: 软件维护（修复 bug、重构、添加功能）是软件工程中的主要长期成本。AI 编码代理可以快速生成代码，但可能引入更难维护的代码。Shore 的论证强调，如果 AI 生成的代码增加了长期维护负担，那么其生产力提升可能具有误导性。

**标签**: `#AI coding`, `#software maintenance`, `#productivity`, `#LLMs`

---

<a id="item-9"></a>
## [Shopify 的 River 代理将 Slack 转变为公开教学工坊](https://simonwillison.net/2026/May/11/learning-on-the-shop-floor/#atom-everything) ⭐️ 8.0/10

Shopify 首席执行官 Tobias Lütke 透露，其内部 AI 编码代理 River 只能在公共 Slack 频道中使用，而非通过私信，从而将每次交互转变为所有员工透明学习的机会。 这种方法创建了一种'Lehrwerkstatt'（教学工坊）文化，使员工通过观察彼此与 AI 代理的协作实现渗透式学习，可能成为组织内协作式 AI 集成的典范。 在过去 30 天内，5,938 名员工在 4,450 个频道中使用了 River，且 River 创作了 Shopify 八分之一的合并拉取请求。该代理处理从代码审查到拉取请求创建的任务，但拒绝私信，并引导用户使用公共频道。

rss · Simon Willison · May 11, 15:46

**背景**: Shopify 开发了 River 作为集成在 Slack 中的内部 AI 编码代理。仅限公共操作的约束旨在创造一个透明环境，让员工通过观察彼此的交互来学习，类似于 Midjourney 早期的公共 Discord 频道帮助用户通过共享实验学习提示工程的方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.zenml.io/llmops-database/building-a-public-ai-agent-workspace-for-organizational-learning">Building a Public AI Agent Workspace for Organizational Learning</a></li>
<li><a href="https://x.com/simonw/status/2053529689122328947">Shopify's River agent system lives in Slack and can only be ...</a></li>

</ul>
</details>

**标签**: `#AI coding assistant`, `#collaborative learning`, `#transparency`, `#software engineering`, `#internal tool`

---

<a id="item-10"></a>
## [Linux 内核 7.0.6 和 6.18.29 修复 Dirty Frag 漏洞](https://lwn.net/Articles/1072311/) ⭐️ 8.0/10

Greg Kroah-Hartman 发布了 Linux 内核版本 7.0.6 和 6.18.29，其中包含了 Hyunwoo Kim 提供的补丁，用于修复 Dirty Frag 漏洞组中的 CVE-2026-43500。所有用户被强烈建议立即升级。 这是一个关键的权限提升漏洞修复，允许任何非特权用户或容器进程在宿主机系统上获得完全 root 权限。鉴于 Linux 在服务器、云和嵌入式设备中的广泛使用，修补漏洞以防止潜在利用至关重要。 该补丁解决了第二个 Dirty Frag 漏洞（CVE-2026-43500），建立在先前对 CVE-2026-43284 的修复基础上，并涉及相关的 Copy Fail 2 问题。系统管理员应尽快升级到这些稳定内核以降低风险。

rss · LWN.net · May 11, 13:35

**背景**: Dirty Frag 是 2026 年 5 月披露的一组 Linux 内核本地权限提升漏洞，影响多个内核模块。它们允许非特权用户或容器内的进程提升权限至 root。Copy Fail（CVE-2026-31431）是一个独立但类似的漏洞，通过 authencesn 加密模板中的逻辑错误实现本地权限提升。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ubuntu.com/blog/dirty-frag-linux-vulnerability-fixes-available">Dirty Frag Linux kernel local privilege escalation vulnerability ...</a></li>
<li><a href="https://fornex.com/help/linux-cve-2026-43500/">Dirty Frag Vulnerability (CVE-2026-43284, CVE-2026-43500) | Fornex</a></li>
<li><a href="https://arstechnica.com/security/2026/05/linux-bitten-by-second-severe-vulnerability-in-as-many-weeks/">Linux bitten by second severe vulnerability in as many... - Ars Technica</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#security`, `#vulnerability`, `#CVE`, `#fix`

---

<a id="item-11"></a>
## [Debian 在测试版中强制可重现构建](https://lwn.net/Articles/1072314/) ⭐️ 8.0/10

Debian 发布团队在 Paul Gevers 的领导下，已启用迁移软件，阻止无法重现或出现可重现性退化的软件包进入测试版分发。 这一政策变化极大地增强了最大 Linux 发行版之一的软件供应链安全性，确保二进制文件可以与源代码匹配验证。 Gioele Barabucci 指出，此上下文中的“可重现”仅限于在 Debian 的构建环境内构建，这比通常的要求更严格。

rss · LWN.net · May 11, 13:21

**背景**: 可重现构建（或确定性编译）确保使用相同构建环境编译相同源代码会产生相同的二进制输出。这允许独立验证在构建过程中没有引入恶意修改。Debian 多年来一直与可重现构建项目合作，这一强制执行是一个重要的里程碑。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Reproducible_builds">Reproducible builds - Wikipedia</a></li>
<li><a href="https://reproducible-builds.org/">Reproducible Builds — a set of software development practices ...</a></li>

</ul>
</details>

**社区讨论**: 社区反应普遍积极，Gioele Barabucci 提供了关于可重现性范围的技术细节。有些人可能会争论这一要求的严格性。

**标签**: `#Debian`, `#reproducible builds`, `#software supply chain`, `#open source`, `#security`

---

<a id="item-12"></a>
## [英特尔 Optane 构建本地运行 1 万亿参数模型，速度 4 tok/s](https://i.redd.it/na7zo7lmck0h1.jpeg) ⭐️ 8.0/10

一位构建者展示了使用英特尔 Optane 持久内存（768GB）本地运行 Moonshot AI 的 Kimi K2.5（一个 1 万亿参数的混合专家模型），通过 llama.cpp 进行混合 GPU/CPU 推理，速度约为每秒 4 个 token。 该构建展示了一种经济高效的替代方案，用昂贵的大容量 DRAM 本地运行大规模 LLM，可能使更多爱好者和研究人员无需依赖云服务就能实验万亿参数模型。 该系统使用 TYAN S5630GMRE-CGN 主板、英特尔 Xeon Gold 6246 CPU、192GB DDR4 DRAM（作为缓存）和 RTX 3060 12GB GPU。Optane PMem 以内存模式作为 RAM 运行，DRAM 作为缓存；稀疏专家权重存放在 PMem 上，而注意力和密集层则放在 GPU 上。

reddit · r/LocalLLaMA · APFrisco · May 11, 19:54 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1taeg8h/computer_build_using_intel_optane_persistent/)

**背景**: 英特尔 Optane 持久内存是一种已停产的技术，其延迟和持久性介于 DRAM 和 SSD 之间。它可以在内存模式下运行（作为易失性内存，DRAM 作为缓存）或 App Direct 模式（作为持久存储）。Kimi K2.5 是 Moonshot AI 开源的多模态智能体模型，采用混合专家架构，总参数量约 1 万亿，但每个 token 只激活一小部分。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.storagereview.com/review/intel-optane-persistent-memory-200-series-review-memverge">Intel Optane Persistent Memory 200 Series... - StorageReview.com</a></li>
<li><a href="https://medium.com/intel-analytics-software/accelerate-your-big-data-cluster-13ca362507d4">Accelerate Your Big Data Cluster. Intel Optane Persistent Memory for...</a></li>
<li><a href="https://huggingface.co/moonshotai/Kimi-K2.5">moonshotai/ Kimi - K 2 . 5 · Hugging Face</a></li>

</ul>
</details>

**社区讨论**: 社区评论反映出兴奋和实用性担忧。一些用户称赞巧妙使用廉价 Optane 内存实现了'比我预期的好'的 token 速率，而另一些人质疑 4 tok/s 对交互任务的可用性。还有优化建议，如使用更多 CPU 核心或尝试不同的 Optane 模式。

**标签**: `#Intel Optane PMem`, `#LLM Inference`, `#Local LLM`, `#Hardware Build`, `#Large Language Models`

---

<a id="item-13"></a>
## [Unsloth 发布支持 MTP 的 GGUF 模型](https://i.redd.it/7qopol51pi0h1.png) ⭐️ 8.0/10

Unsloth 发布了保留多令牌预测（MTP）层的 Qwen3.6-27B 和 Qwen3.6-35B-A3B 的 GGUF 版本，但用户需构建并使用特定的 llama.cpp PR 才能利用 MTP 实现更快的本地推理。 GGUF 格式中的 MTP 支持允许本地 LLM 推理每次前向传递预测多个令牌，无需外部草稿模型即可显著提升速度。这对在消费级硬件上的高效本地部署是一项重大进步。 这些模型需要 llama.cpp 的 PR #15225 或兼容的分支（如 ik_llama.cpp），并设置 nextn_predict_layers > 0。部分用户报告 ik_llama.cpp 分支目前比官方 PR 提供更快的 MTP。

reddit · r/LocalLLaMA · Altruistic_Heat_9531 · May 11, 14:21 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1ta4rvs/mtp_on_unsloth/)

**背景**: 多令牌预测（MTP）是一种训练策略，让 LLM 同时预测多个未来令牌，减少顺序解码步骤。该技术对低并发的本地推理尤其有利，可将吞吐量提升两到三倍。GGUF 是 llama.cpp 使用的量化模型格式，用于高效的 CPU 和 GPU 推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ravchat.com/llm-inference-multi-token">Local LLM Inference & Multi - Token Prediction : ik_llama.cpp | RavChat</a></li>
<li><a href="https://blog.gopenai.com/how-multi-token-prediction-mtp-works-in-deepseek-v3-94bb9301989c">How Multi - Token Prediction ( MTP ) works in... | GoPenAI</a></li>
<li><a href="https://github.com/Linus467/llama.cpp-MTP">GitHub - Linus467/llama.cpp-MTP: LLM inference in C/C++</a></li>

</ul>
</details>

**社区讨论**: 社区非常兴奋，许多用户称 MTP 是本地推理的“游戏规则改变者”。一些用户报告编译错误，并指出 ik_llama.cpp 分支可能比官方 PR 更快。其他人则热切期待其完全整合到 llama.cpp 主线中。

**标签**: `#MTP`, `#Unsloth`, `#llama.cpp`, `#GGUF`, `#LLM inference`

---

<a id="item-14"></a>
## [MiniCPM 4.6 发布，文档理解能力提升](https://huggingface.co/openbmb/MiniCPM-V-4.6) ⭐️ 8.0/10

OpenBMB 发布了 MiniCPM-V 4.6，一款多模态小语言模型，具有增强的文档理解能力，采用 Qwen3.5 风格的混合 LLM 骨干和 NaViT 视觉编码器。 此次发布表明小模型在多模态任务中可以媲美甚至超越大模型，从而能够在资源受限的设备上高效本地部署。 该模型支持文本、图像和视频输入，并提供 Q8_0（812MB）和 F16（1.52GB）量化格式。社区讨论突显了量化精度与模型大小之间的权衡。

reddit · r/LocalLLaMA · themrzmaster · May 11, 17:08 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1ta9k8o/minicpm_46/)

**背景**: MiniCPM 是由清华大学与 ModelBest 联合实验室 OpenBMB 开发的一系列小语言模型。小语言模型（SLM）提供了一种资源高效的大型模型替代方案。量化技术可减小模型体积并降低内存占用，从而在本地硬件上实现更快的推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/openbmb/MiniCPM-V-4.6">openbmb/MiniCPM-V-4.6 · Hugging Face</a></li>
<li><a href="https://github.com/OpenBMB/MiniCPM">GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra ...</a></li>
<li><a href="https://arxiv.org/abs/2404.06395">MiniCPM: Unveiling the Potential of Small Language Models ... openbmb/MiniCPM-V-4.6 · Hugging Face OpenBMB launches MiniCPM-V 4.6 1.3B Instruct MiniCPM: Unveiling the Potential of End-side Large Language ... MiniCPM-V 4.6 - SGLang Documentation MiniCPM-V Series | OpenBMB/MiniCPM-o | DeepWiki</a></li>

</ul>
</details>

**社区讨论**: 用户就在 Q8_0 与 F16 量化间的选择展开讨论，部分人偏向更小尺寸以节省 RAM。另有用户指出该模型存在明显的“PRC 偏见及回避行为”，并建议添加空白图像块可绕过行为限制。

**标签**: `#MiniCPM`, `#multimodal`, `#small language model`, `#local LLM`, `#quantization`

---

<a id="item-15"></a>
## [Qwen 3.6 35B A3B 在小众代码理解上大幅提升](https://www.reddit.com/r/LocalLLaMA/comments/1t9whrt/the_qwen_36_35b_a3b_hype_is_real/) ⭐️ 8.0/10

一位 Reddit 用户报告称，新型 Qwen 3.6 35B A3B 模型以及其他近期小模型，借助 Gated DeltaNet 和 hybrid Mamba2 等先进长上下文机制，理解小众学术代码的能力显著提升。 这一突破使得小型本地模型能够胜任复杂的代码理解任务，让研究者可以将整篇学术论文和代码库输入到消费级硬件上运行的模型中。 用户测试了四个模型：Qwen 3.6 35B A3B、Qwen 3.6 27B、Gemma 4 26B A4B 和 Nemotron 3 Nano。所有模型相较于之前的小模型都有明显提升，但将长上下文装入 32GB 内存对某些模型（如 Devstral Small 2）仍具挑战。

reddit · r/LocalLLaMA · The_Paradoxy · May 11, 07:51

**背景**: 近期的开源权重模型引入了 Gated DeltaNet 和 hybrid Mamba2 等线性注意力机制，以高效处理超过 64K token 的长上下文。Qwen 3.6 35B A3B 采用混合架构，每三个 Gated DeltaNet 层搭配一个 Gated Attention 层，并采用稀疏 MoE，每个 token 仅激活 3B 参数，从而在消费级 GPU 上实现快速推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://dev.to/czmilo/qwen36-35b-a3b-complete-review-alibabas-open-source-coding-model-that-beats-frontier-giants-4382">Qwen3.6-35B-A3B Complete Review: Alibaba's ... - DEV Community</a></li>
<li><a href="https://apxml.com/models/qwen36-35b-a3b">Qwen3.6 35B A3B: Specifications and GPU VRAM Requirements</a></li>
<li><a href="https://insiderllm.com/guides/qwen-3-6-local-ai-guide/">Qwen 3.6 Complete Guide: 27B Dense, 35B-A3B MoE, and Which to ...</a></li>

</ul>
</details>

**社区讨论**: 用户分享了实际经验：有人推荐在长上下文任务中使用 Qwen 35B A3B 的思考模式，另一位用户指出 27B 模型与 DeepSeek V4 表现相似。部分用户讨论了合适的采样设置和量化级别。一位拥有 12GB GPU 的用户询问如何搭配第二张显卡。

**标签**: `#Qwen`, `#LLM`, `#local AI`, `#model benchmark`, `#long context`

---

<a id="item-16"></a>
## [冒充 OpenAI 隐私过滤器的恶意仓库登上 Hugging Face 趋势榜首](https://thehackernews.com/2026/05/fake-openai-privacy-filter-repo-hits-1.html) ⭐️ 8.0/10

一个名为 Open-OSS/privacy-filter 的恶意仓库在 Hugging Face 上冒充 OpenAI 的隐私过滤器，通过加载器脚本分发用 Rust 编写的信息窃取程序。该仓库一度登上平台趋势榜第一，累计获得约 24.4 万次下载和 667 次点赞，随后被平台禁用。 此次事件凸显了开源 AI 生态系统中严重的供应链漏洞，攻击者通过冒充可信品牌传播恶意软件。这亟需在 Hugging Face 等模型中心加强安全措施，以保护开发者和用户免受数据窃取。 安全公司 HiddenLayer 还发现了另外 6 个类似的仓库，同一基础设施曾被用于分发远程访问木马 ValleyRAT。该攻击基础设施与银狐黑客组织存在重叠，后者以税务主题钓鱼活动闻名。

telegram · zaihuapd · May 11, 12:51

**背景**: Hugging Face 是一个用于托管和共享机器学习模型与数据集的流行平台，常被开发者在 AI 流程中使用。供应链攻击通过将恶意代码注入看似合法的包中，从而危害下游用户。ValleyRAT 是一种远程访问木马，可让攻击者非法控制受感染系统；银狐是一个威胁行为者组织，以通过伪装成税务相关文档传播恶意软件而闻名。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.zscaler.com/blogs/security-research/technical-analysis-latest-variant-valleyrat">New Updates to ValleyRAT | ThreatLabz - Zscaler</a></li>
<li><a href="https://research.checkpoint.com/2025/cracking-valleyrat-from-builder-secrets-to-kernel-rootkits/">Cracking ValleyRAT: From Builder Secrets to Kernel Rootkits</a></li>
<li><a href="https://mybroadband.co.za/news/security/646153-hacker-group-targeted-companies-in-south-africa-using-fake-sars-notifications.html">Hacker group targeted companies in South Africa using fake SARS...</a></li>

</ul>
</details>

**标签**: `#security`, `#supply-chain-attack`, `#hugging-face`, `#malware`, `#open-source`

---