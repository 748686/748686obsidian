---
layout: default
title: "Horizon Summary: 2026-08-21 (ZH)"
date: 2026-08-21
lang: zh
---

> 从 41 条内容中筛选出 14 条重要资讯。

---

**科技新闻**
1. [AliExpress 无声 WebAudio 指纹识别干扰蓝牙多设备](#item-tech-news-1) ⭐️ 8.0/10
2. [恶意 Rust 包 Arrayref 在构建期执行载荷](#item-tech-news-2) ⭐️ 8.0/10
3. [端侧 MIDI 钢琴自动补全：125M 参数 Transformer 实时续奏](#item-tech-news-3) ⭐️ 8.0/10
4. [Linux 7.2 内核发布：聚焦硬件支持更新](#item-tech-news-4) ⭐️ 8.0/10
5. [GitHub 8 月 17 日宕机复盘：级联故障、重试放大与迁移进展](#item-tech-news-5) ⭐️ 7.0/10
6. [Meta 大规模抓取数据无后果，Aaron Swartz 却遭起诉引争议](#item-tech-news-6) ⭐️ 7.0/10
7. [Bun 1.4 发布，WebView 带来浏览器自动化 JSON API 原型](#item-tech-news-7) ⭐️ 7.0/10
8. [Linux 7.3 合并窗口开始：组调度重构与架构弃用更新](#item-tech-news-8) ⭐️ 7.0/10
9. [OpenAI 预览前沿模型零数据留存与私密安全处理](#item-tech-news-9) ⭐️ 7.0/10
10. [陶哲轩：AI 或致数学证明过剩与基础危机](#item-tech-news-10) ⭐️ 7.0/10
11. [反向查询服务泄露数百万张面部照片](#item-tech-news-11) ⭐️ 7.0/10

**科技博客**
1. [生成式推荐重塑大规模推荐](#item-tech-blog-1) ⭐️ 8.0/10
2. [模式演化：小改动为何引发生产故障](#item-tech-blog-2) ⭐️ 2.0/10

**财经新闻**
1. [深圳中院一审宣判恒大及许家印案：许家印获无期徒刑并处没收个人全部财产](#item-finance-news-1) ⭐️ 9.0/10

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [AliExpress 无声 WebAudio 指纹识别干扰蓝牙多设备](https://blog.laserphile.com/2026/08/aliexpress-webpage-keeping-multipoint.html) ⭐️ 8.0/10

一项调查发现，AliExpress 网页会在后台以无声方式运行 WebAudio 指纹识别，该行为会干扰蓝牙多设备（multipoint）连接。这种隐蔽的指纹识别技术不仅具有隐私侵入性，还可能带来实际的用户体验副作用，例如用户反映手机电池耗电加快、音频输出异常等。调查还指出，多数浏览器没有显示正在播放音频的提示，使用户难以察觉此类静默操作。社区讨论也提到，Firefox 等浏览器已对 WebAudio 指纹识别进行了部分缓解，但其他浏览器仍存在风险。

hackernews · emctech · 8月20日 10:08 · [社区讨论](https://news.ycombinator.com/item?id=49372583)

**「背景」** WebAudio 指纹识别是一种利用网页音频处理时的微小硬件或软件差异来识别用户的隐私追踪技术。蓝牙多点连接（Bluetooth multipoint）允许一副耳机同时连接多个设备，通常会在存在音频流时保持相应链路。AliExpress 网页被发现会在后台播放无声音频流，这不仅触发了 WebAudio 指纹识别，还会让耳机保持与电脑的连接，从而阻断手机音频。

**「影响」** 访问 AliExpress 时，网站的防滥用脚本会创建隐藏的 WebAudio 图并连接到音频输出端，保持系统音频路径占用，从而阻止多点蓝牙耳机自动切换到其他已配对设备。这会导致用户在同时连接 PC 和手机时无法听到手机音频。

**「社区讨论」** 社区评论中，多名用户报告了与此相关的实际问题，包括后台打开网站导致手机快速耗电、助听器对外界噪音的放大变化，以及 AliExpress 应用后台运行时车载音频误响应。同时，也有评论指出 Firefox 等浏览器已对 WebAudio 指纹识别采取缓解措施。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://upstract.com/x/56150fe846bd9a27">AliExpress runs silent WebAudio fingerprinting that breaks...</a></li>
<li><a href="https://www.elseif.net/stories/aliexpress-runs-silent-webaudio-fingerprinting-that-breaks-bluetooth-m-4d2c69f">AliExpress silent WebAudio fingerprinting keeps Bluetooth audio...</a></li>
<li><a href="https://news.ycombinator.com/item?id=49372583">AliExpress runs silent WebAudio fingerprinting that... | Hacker News</a></li>
<li><a href="https://www.elseif.net/stories/aliexpress-runs-silent-webaudio-fingerprinting-that-breaks-bluetooth-m-4d2c69f">AliExpress silent WebAudio fingerprinting keeps Bluetooth ... — elseif</a></li>
<li><a href="https://news.ycombinator.com/item?id=49372583">AliExpress runs silent WebAudio fingerprinting that... | Hacker News</a></li>

</ul>
</details>

**标签**: `#web-audio`, `#fingerprinting`, `#privacy`, `#bluetooth`, `#browsers`

---

<a id="item-tech-news-2"></a>
### [恶意 Rust 包 Arrayref 在构建期执行载荷](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/) ⭐️ 8.0/10

SafeDep 报道称，Rust 生态中广泛使用的 arrayref crate 的一个恶意版本被发现会在构建期执行载荷。Rust 官方博客于 2026 年 8 月 20 日发布供应链攻击通报，RustSec 咨询库也创建了 issue 进行跟踪。该恶意版本已从 crates.io 消失，但社区指出没有明显的 yank 标记，也暂无安全公告，引发对包管理器应对能力的质疑。事件凸显了构建脚本和第三方依赖的供应链风险，StepSecurity 和 JFrog 等厂商也发布了相关分析。

hackernews · abhisek · 8月20日 13:23 · [社区讨论](https://news.ycombinator.com/item?id=49374269)

**「背景」** Rust 的包管理器 Cargo 在构建某些 crate 时会执行其自带的构建脚本（build.rs），这为恶意代码在开发者机器上运行提供了机会。arrayref 是一个广泛使用的 Rust crate，用于安全地创建数组引用；攻击者通过发布名称相似的恶意 crate（如 proc-macro1）并使其成为受影响 crate 的构建时依赖，从而在 cargo build 过程中下载并运行远程恶意负载。官方 Rust 安全响应团队已确认这一攻击，并删除了相关恶意 crate 及其同伙（proc-macro-en、aovine、arone、aronenao、tinymember）。

**「影响」** 受影响版本 arrayref 0.3.10、internment 0.8.7 和 append-only-vec 0.1.9 在 cargo build 时通过 build.rs 拉取并执行远程载荷，可能导致开发者凭据被盗；Rust 安全响应团队已移除这些版本并锁定作者帐户。

**「社区讨论」** 评论者批评 crates.io 在事件中管理不善：恶意版本消失却没有 yank 标记，也没有安全公告，GitHub 对仓库的处理过于粗暴。同时有声音呼吁 Cargo 对 build.rs 脚本进行沙箱化，并反思标准库过薄导致依赖膨胀的问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/">Supply chain attack on arrayref | Rust Blog</a></li>
<li><a href="https://www.stepsecurity.io/blog/arrayref-rust-crate-supply-chain-attack">Rust Supply-Chain Attack: arrayref, internment, and append-only-vec Poisoned by the proc-macro1 Build-Time Dropper - StepSecurity</a></li>
<li><a href="https://research.jfrog.com/post/arrayref-proc-macro1-crates-io/">Compromised Rust crates on crates . io silently execute malware at...</a></li>
<li><a href="https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/">Supply chain attack on arrayref | Rust Blog</a></li>
<li><a href="https://runtimewire.com/article/arrayref-rust-crates-supply-chain-attack-build-malware">Attackers poisoned three Rust crates to steal developer credentials...</a></li>

</ul>
</details>

**标签**: `#security`, `#rust`, `#supply-chain`, `#open-source`, `#malware`

---

<a id="item-tech-news-3"></a>
### [端侧 MIDI 钢琴自动补全：125M 参数 Transformer 实时续奏](https://simedw.com/2026/08/20/midi-autocomplete/) ⭐️ 8.0/10

开发者 simedw 训练了一个 125M 参数的 Transformer 模型，用于 MIDI 钢琴演奏的实时自动补全，在 iPhone 15 上可达约 108 音符/秒，并且完全在设备端运行。其思路类似 GitHub Copilot 或 Tabnine，只不过用户不是用代码提示模型，而是先弹几个音符，模型便基于这些音符继续演奏。该应用免费开放，作者表示乐意回答关于模型、训练、Core ML 以及各种失败尝试的问题。这一项目展示了小型生成模型在端侧音乐创作场景中的实际可行性，尤其是低延迟和隐私优势。

hackernews · simedw · 8月20日 12:04 · [社区讨论](https://news.ycombinator.com/item?id=49373456)

**「背景」** 自动补全模型通常用于代码或文本，根据已有输入预测接下来的内容。这个项目把同样的思路迁移到音乐领域：通过 MIDI 钢琴输入若干音符，Transformer 模型预测并续奏后续乐句，并利用 Core ML 部署到 iPhone 上实现实时推理。类似的“音乐自动补全”概念在古典音乐教育中也有渊源，例如作曲家训练中使用的模式识别与生成练习。

**「影响」** 使用 iPhone 15 的 MIDI 钢琴用户可以免费体验完全本地运行的实时钢琴续奏，约 108 音符/秒的推理速度使交互接近即时；这为音乐创作工具和端侧生成式 AI 应用提供了一个可借鉴的实例。

**「社区讨论」** 评论区普遍肯定项目的原创性和技术价值，有人提议将其做成 VST 或 Max for Live 设备，也有人将其与古典作曲家的训练方法及 AI 设计工具中的“品味探索”联系起来。多位用户还关心训练数据规模和预训练/后训练样本数量等细节，作者尚未在评论中公开回应。

**标签**: `#transformer`, `#MIDI`, `#on-device ML`, `#music generation`, `#Core ML`

---

<a id="item-tech-news-4"></a>
### [Linux 7.2 内核发布：聚焦硬件支持更新](https://www.igalia.com/2026/08/19/Linux-72-Released.html) ⭐️ 8.0/10

Linux 7.2 内核已正式发布，此次发布被描述为一次重要的增量版本更新。该版本在硬件支持方面有显著更新，例如 HDMI 2.1 支持，同时对开源生态系统具有广泛影响。虽然并非颠覆性改变，但涉及显示、图形等桌面相关功能，适合 Linux 桌面、嵌入式及服务器用户关注。相关公告与报道由 Igalia 发布，发行版将陆续提供内核更新。

hackernews · mariuz · 8月20日 15:46 · [社区讨论](https://news.ycombinator.com/item?id=49376265)

**「背景」** Linux 7.2 是继 7.1 之后的新内核版本，预计于 2026 年 8 月中旬发布，主要带来缓存感知调度、AMD Zen 6 支持以及 AMDGPU 驱动对 HDMI 2.1 固定速率链路（FRL）的正式补丁。HDMI 2.1 FRL 支持此前因 HDMI 论坛的授权限制而受阻，现在 AMD 已将相关补丁提交到 Linux 7.2，使开源驱动能够使用更高的 HDMI 2.1 带宽，这对需要高刷新率或高分辨率显示的用户尤其重要。

**「社区讨论」** 评论中，有用户询问 HDMI 2.1 支持在 AMD 开源驱动中如何突破早前的限制，也有用户探索该版本的主要受众和与 LWN 报道的差异。有人对 Raspberry Pi 4 的内核更新表示期待，还有人比较 HDMI 与 DisplayPort 的适用场景。整体讨论展现了技术兴趣，但存在不少开放问题。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://media.patentllm.org/news/hardware/amd-gpu-benchmarks-hdmi-2-1-frl-driver-and-multi-device-ai-w-20260604">AMD GPU Benchmarks, HDMI 2 . 1 FRL Driver , and... - PatentLLM Blog</a></li>
<li><a href="https://t.me/linuxgram/19972">Linuxgram– Telegram</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#open source`, `#hardware support`, `#release`, `#operating systems`

---

<a id="item-tech-news-5"></a>
### [GitHub 8 月 17 日宕机复盘：级联故障、重试放大与迁移进展](https://github.blog/news-insights/company-news/the-august-17-outage-and-the-work-ahead/) ⭐️ 7.0/10

GitHub 官方发布了 8 月 17 日重大宕机的事后分析报告，指出故障由级联失败、共享依赖问题以及客户端重试循环放大共同导致。具体而言，一个内部端点的延迟响应触发了 VS Code 中一个潜在的重试 bug，使流量放大约 10 倍，并延迟了 Copilot Token Service 的恢复。报告还显示，自 4 月以来每月提交数从 14 亿增长到 29 亿，同时 GitHub 向 Azure 的迁移仅完成 58%。这次事件突出表明，在大规模服务中，客户端重试逻辑和共享依赖可能成为加剧事故的关键因素，也为依赖 GitHub 与 Copilot 的工程团队提供了可靠性方面的实际借鉴。

hackernews · 0xedb · 8月20日 19:22 · [社区讨论](https://news.ycombinator.com/item?id=49378957)

**「背景」** GitHub 在 8 月 17 日发生了一次持续约 7 小时 47 分钟的大规模故障，影响了 Issues、Pull Requests、Actions 和 Copilot 等核心功能，原因包括级联故障、网络饱和以及客户端重试风暴。官方事后分析指出，一个内部端点延迟响应触发了 VS Code 中潜在的重试缺陷，导致流量被放大约 10 倍，进而延迟了 Copilot Token Service 的恢复。这一事件也发生在 GitHub 向 Microsoft Azure 的迁移尚未完成、以及月提交量从 14 亿增长到 29 亿的背景下。

**「影响」** 对于依赖 GitHub 和 Copilot 的开发者及工程团队，这次故障说明客户端重试风暴和内部依赖单点问题可能在恢复期间造成流量放大和恢复延迟，提醒他们在设计客户端容错与服务依赖时需考虑级联效应。

**「社区讨论」** 评论中有人批评这类故障背后是“不惜一切代价避免向用户显示错误”的趋势，导致用户长时间面对加载动画；也有人对每月提交量短期内翻倍表示惊讶，并质疑 Azure 迁移进度缓慢。还有观点认为，微软有激励让开发者继续使用 AI 工具，因此不会通过向提交收费来抑制 AI 相关流量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://sitem.co/public/summary/3071/github-com-incident-report-august-17-2026">GitHub .com Incident Report - August 17 , 2026 - SiteM</a></li>

</ul>
</details>

**标签**: `#outage`, `#post-mortem`, `#GitHub`, `#reliability`, `#devops`

---

<a id="item-tech-news-6"></a>
### [Meta 大规模抓取数据无后果，Aaron Swartz 却遭起诉引争议](https://blog.curiousquail.com/im-upset-again-about-a-co-creator-of-rss-being-prosecuted-for-something-meta-is-doing-with-little-consequence/) ⭐️ 7.0/10

这篇观点文章将作家兼 RSS 共同创造者 Aaron Swartz 因抓取 JSTOR 论文而遭美国政府起诉的经历，与 Meta 大规模抓取数据用于 AI 训练却几乎没有法律后果的情况进行对比，提出了法律双重标准的质疑。作者认为，大型上市公司因其广泛的经济影响而受到保护，而个人则可能面临严厉惩罚。文章指出 AI 数据来源、法律伦理和行业权力动态是当前技术政策的核心问题。社区评论则对 Swartz 案的具体事实和这种类比的恰当性提出了不同看法。

hackernews · speckx · 8月20日 20:07 · [社区讨论](https://news.ycombinator.com/item?id=49379550)

**「背景」** 亚伦·斯沃茨（Aaron Swartz）是美国程序员和互联网活动家，2011 年因通过 MIT 计算机网络从 JSTOR 下载大量学术期刊文章，被联邦政府依据《计算机欺诈与滥用法》（CFAA）起诉多项联邦罪名。起诉书中包括非法获取受保护计算机信息、鲁莽损坏受保护计算机等指控；据报道，他最终面临最多 13 项重罪，理论上最高可判 50 年监禁和 100 万美元罚款。这与从开放互联网抓取公开网页的行为在法律上有很大区别。

**「影响」** 现实后果是，企业级 AI 抓取即使未获授权，目前也主要面临民事诉讼而非刑事起诉（例如针对 Meta 和 Anthropic 的诉讼），这使得 Swartz 案所凸显的法律双重标准在 AI 训练数据领域仍未得到解决。

**「社区讨论」** 评论者之间存在明显分歧：一些人强调 Swartz 并非单纯抓取公开网页，而是侵入路由器并规避封禁，与 Meta 抓取公开网络数据有本质区别；另一些人则指出 Swartz 案中 JSTOR 并未提起民事诉讼，是美国政府主动追诉，并纠正关于其可能刑期的误解。讨论总体聚焦于事实准确性和两种行为是否真正可比。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/United_States_v._Swartz">United States v. Swartz - Wikipedia</a></li>
<li><a href="https://www.nacdl.org/Content/CFAACases">NACDL - CFAA Cases</a></li>
<li><a href="https://www.investopedia.com/terms/a/aarons-law.asp">Aaron&#x27;s Law and the Computer Fraud and Abuse Act Explained</a></li>
<li><a href="https://petapixel.com/2025/02/24/meta-disussed-using-copyrighted-content-for-ai-training-purposes-lawsuit-reveals/">Meta Discussed Using Copyrighted Content for AI Training ... | PetaPixel</a></li>
<li><a href="https://www.anybodycanprompt.com/p/another-ai-training-data-theft-but">Another AI Training Data Theft? BUT This Time It’s Anthropic, NOT...</a></li>
<li><a href="https://reclaimr.app/blog/ai-technology-lawsuits-privacy-settlements-2025-guide">AI Technology Lawsuits and Privacy Settlements 2025: Your...</a></li>

</ul>
</details>

**标签**: `#web-scraping`, `#AI-ethics`, `#legal`, `#Meta`, `#Aaron-Swartz`

---

<a id="item-tech-news-7"></a>
### [Bun 1.4 发布，WebView 带来浏览器自动化 JSON API 原型](https://simonwillison.net/2026/Aug/20/bun-webview-json-api/) ⭐️ 7.0/10

Bun 1.4 正式发布，这是自 Rust 重写以来第一个稳定版本。官方称其新增 1,517 项 Node.js 测试套件用例、修复超过 2,900 个问题，并让 Linux 上空闲 CPU 使用率降低 5 倍、内存使用最多降低 35%、启动速度提升 50%。该版本还加入了 Bun.Image、Bun.WebView、Bun.markdown、Bun.cron\(\)、Bun.Terminal 以及并行运行等多项功能。其中 Bun.WebView 首次为 Bun 核心提供浏览器自动化能力，可通过 macOS WebKit 或通过 Chrome DevTools 协议（CDP）控制本地 Chromium。Simon Willison 利用该 API 构建了一个 shot-scraper 风格的 JSON API 原型，可以加载网页并执行 JavaScript；实测运行完整 Chrome 处理复杂网页时，服务大约需要 192MB 到 256MB 的容器内存。

rss · Simon Willison · 8月20日 15:37

**「背景」** Bun 是一个 JavaScript 和 TypeScript 运行时及工具链，此前经历了一次从 Zig 到 Rust 的大型重写。shot-scraper 是 Simon Willison 维护的命令行工具，基于 Playwright 提供网页抓取、截图和执行 JavaScript 的能力。Bun.WebView 则是 Bun 1.4 新增的浏览器自动化接口，让开发者可以在 Bun 进程中直接控制 WebKit 或 Chromium。

**「影响」** 对于需要在 Bun 环境中提供网页 JavaScript 执行能力的开发者，Bun.WebView 可能减少对 Playwright 等外部浏览器驱动层的依赖；该原型的 192MB 到 256MB 内存测量值也为运行完整 Chromium 的容器容量规划提供了参考。

**标签**: `#Bun`, `#WebView`, `#JavaScript`, `#Open Source`, `#Performance`

---

<a id="item-tech-news-8"></a>
### [Linux 7.3 合并窗口开始：组调度重构与架构弃用更新](https://lwn.net/Articles/1089244/) ⭐️ 7.0/10

Linux 内核 7.3 开发周期的合并窗口已开始，截至报道时已有 2346 个非合并变更集进入主线。最值得注意的变化是对多处理器系统上组调度权重缩放的重构，新增 debugfs 中的 cgroup\_mode 旋钮，提供 smp、up、max、concur、tasks 等模式，默认值为 concur，取代旧行为；该系列最后还改为控制组使用单一运行队列，以降低调度器开销和延迟问题。架构方面，nolibc 已支持 Alpha，PowerPC 新增 Rust 支持，若干 32 位 Arm CPU 被标记弃用（7.3 是预期 LTS，之后可能移除），x86 的 SMP alternatives 代码被删除。内核还扩展了 binfmt\_misc，加入 BPF 钩子在运行时选择解释器，并新增 syscall\_user\_dispatch 的 sysctl 开关（默认启用）。文件系统方面，移除了 EFS 和 FreeVxFS 支持，新增 failfs 文件系统和 fchroot\(\) 系统调用以及 FD\_FAILFS\_ROOT 特殊描述符。

rss · LWN.net · 8月20日 13:11

**「背景」** Linux 内核每个开发周期都从合并窗口开始，在此期间维护者将各子系统的改动合入主分支，之后进入稳定期。组调度（group scheduling）用于在控制组之间公平分配 CPU 时间，此前权重的缩放会在大型多处理器系统上产生极小因子和整数溢出等问题，因此调度器维护者 Peter Zijlstra 重新设计了这一机制。

**「影响」** 运行 7.3 或使用 cgroup 调度策略的服务器管理员可能观察到 CPU 时间分配行为变化，因为新的默认 concur 模式使组调度的权重缩放与先前内核不同；不过该行为可通过 debugfs 中的 cgroup\_mode 调整回旧的 smp 模式以保持兼容。

**标签**: `#linux kernel`, `#merge window`, `#group scheduling`, `#open source`, `#computer systems`

---

<a id="item-tech-news-9"></a>
### [OpenAI 预览前沿模型零数据留存与私密安全处理](https://openai.com/index/offering-zero-data-retention-for-frontier-models/) ⭐️ 7.0/10

OpenAI 宣布面向符合条件的 API 客户重申“零数据留存”（ZDR）承诺，即在请求处理完毕后不保留提示词与回复；同时预览“私密安全处理”机制，可在不向 OpenAI 人员暴露原始内容的前提下，跨相关交互识别潜在滥用并仅回传有限安全信号。客户内容由客户控制的密钥加密存储，即使被标记，OpenAI 人员也无法获取原文。该功能目前正与早期客户测试，计划于 9 月逐步上线，并发布技术白皮书。此举旨在回应企业对采用前沿模型时的隐私、合规与安全顾虑。

telegram · zaihuapd · 8月20日 02:33

**「背景」** OpenAI 的企业隐私页面说明，除少数端点和功能外，API 的输入和输出可能被安全保留最多 30 天，用于提供服务及识别滥用；默认情况下，API 不会用客户数据训练模型。零数据留存（ZDR）是面向符合条件的 API 客户提供的一种数据控制承诺，在请求处理完毕后不保留提示词和回复，但 OpenAI 保留在必要时对特定客户取消该资格以调查或防范严重风险活动的权利。本次预览的“私密安全处理”正是这类数据控制功能的延伸，目标是在不向 OpenAI 人员暴露原始内容的前提下完成滥用监测。

**「影响」** 对于依赖 API 处理敏感数据的企业客户，这一预览若正式落地，将显著降低数据留存和人工审查带来的合规风险，有助于推动前沿模型在金融、医疗等受监管行业的采用。不过目前仍属预览，技术细节有限，最终效果取决于白皮书和实际部署。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developers.openai.com/api/docs/guides/your-data">Data controls in the OpenAI platform</a></li>
<li><a href="https://openai.com/enterprise-privacy/">Enterprise privacy at OpenAI | OpenAI</a></li>
<li><a href="https://meetily.ai/llm-privacy/openai">OpenAI Data Retention Policy 2026 - Does OpenAI Train on Your API Data? | Meetily</a></li>

</ul>
</details>

**标签**: `#OpenAI`, `#zero data retention`, `#privacy`, `#AI safety`, `#enterprise AI`

---

<a id="item-tech-news-10"></a>
### [陶哲轩：AI 或致数学证明过剩与基础危机](https://the-decoder.com/terence-tao-says-ai-could-trigger-maths-biggest-crisis-since-godel/) ⭐️ 7.0/10

陶哲轩在为 2026 年国际数学家大会撰写的文章中警告，人工智能可能引发数学界的重大基础危机，其严重程度堪比 1900 至 1930 年间由罗素悖论和哥德尔不完备定理引发的危机。他认为数学界应停止争论 AI 能做什么，转而直面被回避的研究目标问题。他援引 First-Proof 项目第二轮结果：10 道未发表研究题由 4 个 AI 系统测试，其中 7 道至少被一个系统判为合格，每题成本为数十至数百美元。陶哲轩警告数学可能从证明稀缺转向证明过剩，并指出即使通过形式验证，无人能清晰讲解的证明也应被视为不完整。

telegram · zaihuapd · 8月20日 13:19

**「背景」** 陶哲轩在 2026 年国际数学家大会的公开演讲及配套文章中，将当前 AI 对数学的影响比作 1900 至 1930 年间由罗素悖论和哥德尔不完备定理引发的基础危机。他认为数学界不应继续争论 AI 的能力边界，而应正视研究目标的重定义问题。他援引的 First-Proof 项目中，第二轮使用 4 个 AI 系统测试 10 道未发表研究题，其中 7 道至少被一个系统判定为合格，每题成本数十至数百美元。

**「影响」** 这一警告给依赖传统同行评审和可读证明的数学研究体系带来压力，可能促使学界重新定义验证标准与研究激励。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://teorth.github.io/tao-web/slides/age-of-ai-icm-2026.pdf">Mathematics in the age of AI - Public lecture, International ...</a></li>
<li><a href="https://www.i6eal.de/en/newsroom/terence-tao-ki-mathematik-grundlagenkrise/">Terence Tao Warns: AI Could Plunge Mathematics Into ...</a></li>
<li><a href="https://arxiv.org/abs/2608.16753">[2608.16753] Mathematics in the age of AI - arXiv.org</a></li>

</ul>
</details>

**标签**: `#AI`, `#mathematics`, `#proof verification`, `#Terence Tao`, `#research`

---

<a id="item-tech-news-11"></a>
### [反向查询服务泄露数百万张面部照片](https://arstechnica.com/gadgets/2026/08/reverse-lookup-service-exposed-millions-of-photos-of-peoples-faces/) ⭐️ 7.0/10

据报道，一家反向图像搜索服务发生数据泄露，约 450 GB 的数据库被暴露，包含超过 900 万张人物面部照片，部分记录还涉及邮箱、电话和 IP 地址等信息。由于人脸属于难以更换的生物识别信息，此次事件引发隐私与身份安全的严重担忧。专家警告，泄露数据可能被用于未经授权的身份识别、个人追踪或诈骗。截至目前，相关服务方已限制数据库访问，但事件影响范围及后续补救措施仍有待进一步确认。

telegram · zaihuapd · 8月20日 15:14

**「背景」** 反向图像搜索允许用户通过上传图片来查找相似图片或图片来源，这类服务通常需要建立并存储包含大量图像及其关联信息的索引。人脸图像被视为高敏感性的生物识别数据，因为一旦泄露，人们难以像更换密码一样更换自己的面部特征，因此此类数据泄露带来的长期风险尤为突出。

**「影响」** 受影响用户面临基于人脸图像的未授权身份识别、追踪和诈骗等直接风险，且由于生物识别信息无法重置，其隐私影响可能长期持续。

**标签**: `#data breach`, `#privacy`, `#biometrics`, `#security`, `#reverse image search`

---

## 科技博客

<a id="item-tech-blog-1"></a>
### [生成式推荐重塑大规模推荐](https://developer.nvidia.com/blog/how-generative-recommenders-are-redefining-recsys-at-scale/) ⭐️ 8.0/10

rss · NVIDIA CUDA Technical Blog · 8月20日 16:00

**「背景」** 传统推荐系统依赖嵌入相似度来建模用户与物品的偏好，但面对每日 TB/PB 级用户历史、长尾稀疏交互、冷启动和毫秒级在线延迟时难以扩展。作者提出，把推荐重构为生成式序列建模——给定用户历史序列预测下一个动作或物品——可以借鉴 LLM 的规模化优势。

**「方案」** 方案核心是两类架构：Meta 的 HSTU 把交互序列当作类似 token 的历史，去掉显式特征工程，并用 SiLU 加权、相对注意力偏置和逐元素门控替换 softmax，从而保留长序列的尺度信息、利于 kernel 融合；Google 的 Semantic IDs 则把物品嵌入做层次聚类成小词表，使模型自回归解码直接生成推荐并天然排序。NVIDIA 的 recsys-examples 用 DynamicEmb 按需分配嵌入行并跨 HBM 与主机内存扩展，结合 Megatron-Core 训练并行，把端到端 MFU 从 7.65% 提升到 31.40%；推理侧用 AOTInductor、FlexKV 和面向语义 ID 的 GR 路径，离线延迟相对 SGLang 束搜索约快 2.1–2.3 倍，在线吞吐约提升 1.85 倍。作者还介绍 nv-embedding-cache 以 HBM/DRAM/远程存储分层缓存，支持超过单卡容量的嵌入表，并在 DLRM v3 上达到 99,997 queries/s。

**「启示」** 作者的核心论点是，生成式推荐不仅是目标函数的改变，而是通过统一架构和专用推理基础设施，让推荐系统在工业规模下利用 LLM 生态、统一检索与排序，同时仍满足严格延迟要求。

**标签**: `#generative recommenders`, `#HSTU`, `#semantic IDs`, `#inference optimization`, `#recsys architecture`

---

<a id="item-tech-blog-2"></a>
### [模式演化：小改动为何引发生产故障](https://blog.bytebytego.com/p/schema-evolution-changing-the-contract) ⭐️ 2.0/10

rss · ByteByteGo · 8月20日 15:32

**「背景」** 作者指出，模式变更在代码评审中看起来很小，例如重命名列、给事件增加字段或移除未使用的响应字段，但部署到生产后常导致无关服务失败。原因是迁移本身没有错，而是新旧两个应用版本同时在同一个数据库上运行，只有其中一个引用了新模式。数据在旧模式版本下写入，却可能在另一个版本下被读取，这样的矛盾不限于部署窗口，也会出现在历史消息或旧版移动端调用中。

**「方案」** 这篇内容目前只搭建了问题框架，尚未展开具体技术方案。作者计划讨论为什么同一时刻总有多个模式版本在起作用，区分向后兼容和向前兼容，分析哪些改动会破坏消费者以及判断条件，介绍 expand-and-contract 迁移和模式注册表的使用，并比较数据库、API 与事件流中的差异，最后给出版本化策略和废弃时间线。不过当前可见的正文仅列出这些议题，没有提供具体机制、示例或证据，因此无法据此验证作者所提策略的有效性。

**「启示」** 从引言看，作者想强调模式演化真正的风险不是迁移过程本身，而是多版本并存时的读写不一致；这一论点需要后续更详细的技术内容来支撑和展开。

**标签**: `#schema evolution`, `#compatibility`, `#databases`, `#APIs`, `#event streams`

---

## 财经新闻

<a id="item-finance-news-1"></a>
### [深圳中院一审宣判恒大及许家印案：许家印获无期徒刑并处没收个人全部财产](https://www.news.cn/legal/20260820/737dfb54ab564fb8a549ba392af9fb0a/c.html) ⭐️ 9.0/10

8 月 20 日，深圳市中级人民法院一审宣判，恒大集团被处罚金 88.2 亿元，恒大地产被处罚金 70 亿元；许家印因非法吸收公众存款、集资诈骗、欺诈发行证券等罪数罪并罚，被判处无期徒刑、剥夺政治权利终身并处没收个人全部财产。法院认定相关犯罪发生于 2016 年至 2021 年间，另有 56 名涉案人员分别被判处十八年至一年十个月不等有期徒刑。

telegram · zaihuapd · 8月20日 04:06

**「背景」** 许家印曾是中国首富，恒大曾是头部房企；此前监管机构已因财务造假等问题对其处以罚款并终身禁入证券市场。

**「影响」** 许家印被判无期徒刑并没收个人全部财产，恒大集团和恒大地产合计被罚 158.2 亿元；据外媒报道，该判决在恒大五年前倒闭并冲击国内经济和金融市场后作出，对债权人、投资者和房地产行业而言，是监管强力追责的标志性案件。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.wral.com/archive/21336491/">Biggest fraud in Chinese history? Beijing accuses Evergrande of...</a></li>
<li><a href="https://www.washingtontimes.com/news/2026/aug/20/chinese-court-sentences-founder-property-developer-evergrande-life/">Chinese court sentences founder of troubled property developer...</a></li>
<li><a href="https://au.finance.yahoo.com/news/founder-chinas-evergrande-sentenced-life-044218098.html">Founder of collapsed Chinese property giant Evergrande sentenced ...</a></li>
<li><a href="https://www.france24.com/en/asia-pacific/20260820-china-reast-estate-giant-xu-jiayin-sentenced-to-life-in-prison">Founder of Chinese real estate giant Evergrande Xu Jiayin ...</a></li>

</ul>
</details>

**标签**: `#Evergrande`, `#China property market`, `#securities fraud`, `#regulatory enforcement`, `#court ruling`

---