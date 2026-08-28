---
layout: default
title: "Horizon Summary: 2026-06-23 (ZH)"
date: 2026-06-23
lang: zh
---

> 从 25 条内容中筛选出 13 条重要资讯。

---

1. [Valve 的 Steam Machine 今日正式推出](#item-1) ⭐️ 9.0/10
2. [无锁 Python：过去、现在与未来](#item-2) ⭐️ 9.0/10
3. [Moebius：0.2B 参数图像修复模型达到 10B 级性能](#item-3) ⭐️ 8.0/10
4. [警察局长利用 Flock 车牌读取器跟踪女性凸显 warrant 需求](#item-4) ⭐️ 8.0/10
5. [Mitchell 承诺向 Zig 基金会捐赠 40 万美元](#item-5) ⭐️ 8.0/10
6. [Deno Desktop 推出多后端 Webview 框架](#item-6) ⭐️ 8.0/10
7. [Claude Code '扩展思维'输出仅为有损摘要](#item-7) ⭐️ 8.0/10
8. [近半数 LG 智能电视应用含住宅代理 SDK](#item-8) ⭐️ 8.0/10
9. [使用 Claude Code 将 Moebius 图像修复模型移植到浏览器](#item-9) ⭐️ 8.0/10
10. [Xfce 的 Wayland 合成器 xfwl4 首个预览版发布](#item-10) ⭐️ 8.0/10
11. [OSPM 2026 第一天：空闲状态、sched_ext 和锁持有者抢占](#item-11) ⭐️ 8.0/10
12. [美光计划投入 2000 亿美元扩产应对 AI 存储芯片短缺](#item-12) ⭐️ 8.0/10
13. [48 位中国开发者举报苹果垄断](#item-13) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Valve 的 Steam Machine 今日正式推出](https://store.steampowered.com/news/group/45479024/view/685257114654870245) ⭐️ 9.0/10

Valve 推出了 Steam Machine，这是一款搭载定制 AMD 芯片的新型客厅游戏主机，采用公平的预订系统，随机分配订单顺序，而不是奖励最快注册者。 此次发布标志着 Valve 首次大举进军主机市场，在客厅领域与索尼和微软展开竞争，同时倡导开放硬件和 Linux 游戏生态。 Steam Machine 的性能是 Steam Deck 的六倍以上，支持 4K 游戏。它运行 SteamOS，但允许用户安装其他操作系统或应用程序。

hackernews · theschwa · 6月22日 17:09 · [社区讨论](https://news.ycombinator.com/item?id=48632884)

**背景**: Steam Machine 是 Valve 对传统游戏主机如 PlayStation 和 Xbox 的回应。与封闭的主机不同，它是一个开放的类 PC 设备，可以运行任何软件。Valve 曾在 2015 年尝试过类似概念，但那条产品线后来被停产。新款机型利用了 Steam Deck 的技术进步。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Steam_Machine">Steam Machine - Wikipedia</a></li>
<li><a href="https://www.the-independent.com/extras/indybest/gadgets-tech/video-games-consoles/valve-steam-machine-release-date-b3000219.html">Valve’s Steam Machine launch could be just hours away | The Independent</a></li>
<li><a href="https://store.steampowered.com/hardware/steammachine">Steam Machine</a></li>

</ul>
</details>

**社区讨论**: 社区评论称赞了公平的预订系统、开放的特性以及真实的营销画面。有用户表达了对 Linux 游戏的支持，其他人则赞赏安装自定义软件的自由。

**标签**: `#steam-machine`, `#valve`, `#gaming-hardware`, `#pc-gaming`, `#launch`

---

<a id="item-2"></a>
## [无锁 Python：过去、现在与未来](https://lwn.net/Articles/1078367/) ⭐️ 9.0/10

CPython 核心开发者兼指导委员会成员 Thomas Wouters 在 PyCon US 2026 上发表了演讲，介绍了无锁 Python（即移除全局解释器锁 GIL）的动机、历史、现状和未来。 移除 GIL 是一项突破性变革，使 Python 中的线程能够真正并行执行，显著提升多核系统上的性能，并扩展了 Python 对 CPU 密集型和并发工作负载的适用性。 Wouters 指出，GIL 是在多 CPU 系统普及之前引入的，移除它一直是长期目标；他还强调，无锁模式已在近期的 Python 版本中可用，并持续演进。

rss · LWN.net · 6月22日 15:26

**背景**: 全局解释器锁（GIL）是 CPython 中的一个互斥锁，用于保护对 Python 对象的访问，防止多个线程同时执行 Python 字节码。虽然它简化了内存管理，但也限制了多核系统上的并行性。无锁 Python 移除了 GIL，允许多线程并发运行，这对现代硬件上的性能提升至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.python.org/3/howto/free-threading-python.html">Python support for free threading — Python 3.14.4</a></li>
<li><a href="https://github.com/python/steering-council">GitHub - python/steering-council: Communications from the ...</a></li>

</ul>
</details>

**标签**: `#Python`, `#GIL`, `#free-threading`, `#concurrency`, `#CPython`

---

<a id="item-3"></a>
## [Moebius：0.2B 参数图像修复模型达到 10B 级性能](https://hustvl.github.io/Moebius/) ⭐️ 8.0/10

研究人员发布了 Moebius，这是一个 0.2B 参数的图像修复模型，性能可与 10B 参数的模型相媲美。社区成员通过 ONNX 导出演示了模型完全在浏览器中运行。 这一突破显著降低了高质量图像修复的计算需求，使其能在边缘设备和浏览器中部署。它挑战了大型模型是顶级性能必需品的假设，可能降低成本并普及高级图像编辑技术。 Moebius 输出 512x512 分辨率的图像，社区测试显示其修复区域相比大型模型有明显平滑，且对新颖物体表现较弱。该模型已成功转换为 ONNX，可在浏览器中运行，下载量约 1.3GB。

hackernews · DSemba · 6月22日 13:53 · [社区讨论](https://news.ycombinator.com/item?id=48630171)

**背景**: 图像修复是指填补图像中缺失或损坏部分的任务。拥有数十亿参数的大型工业模型质量高，但计算成本高昂。Moebius 通过极端的结构压缩克服表示瓶颈，旨在用少得多的参数达到专家级质量。ONNX Runtime 支持跨平台推理，包括通过 WebAssembly 和 WebGPU 在网页浏览器中运行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://hustvl.github.io/Moebius/">Moebius: 0.2B Lightweight Image Inpainting Framework with 10B ...</a></li>
<li><a href="https://arxiv.org/abs/2606.19195">[2606.19195] Moebius: 0.2B Lightweight Image Inpainting ...</a></li>
<li><a href="https://huggingface.co/papers/2606.19195">Paper page - Moebius: 0.2B Lightweight Image Inpainting ...</a></li>

</ul>
</details>

**社区讨论**: 社区对该模型的小尺寸和浏览器演示印象深刻，有用户成功在本地运行。但对声称的 10B 级性能存在质疑，测试显示可见平滑和分辨率限制（512x512）。用户还对用于漫画翻译等领域的专用版本表现出兴趣。

**标签**: `#image inpainting`, `#efficient ML`, `#model compression`, `#ONNX`, `#browser inference`

---

<a id="item-4"></a>
## [警察局长利用 Flock 车牌读取器跟踪女性凸显 warrant 需求](https://ipvm.com/reports/police-chiefs-track) ⭐️ 8.0/10

一份报告记录了警察局长滥用 Flock Safety 的自动车牌读取器来跟踪女性的情况，突显了在此类监控工具用于个人追踪之前需要获得搜查令的紧迫性。 执法领导人自身的滥用行为显示了不受限制的 ALPR 访问的固有风险，可能侵蚀公众信任，并需要更强的隐私保护措施。 尽管 Flock 将此类滥用描述为罕见，但报告指出，跟踪警官认识的人是最常见的滥用形式，揭示了其立场中的矛盾。

hackernews · jhonovich · 6月22日 19:13 · [社区讨论](https://news.ycombinator.com/item?id=48634694)

**背景**: Flock Safety 等自动车牌读取器（ALPR）使用人工智能捕捉车牌、车辆品牌/型号和位置数据，从而能够追踪车辆的行驶轨迹。警察部门广泛部署这些摄像头，但由于没有搜查令要求，警官可以出于任何原因查询数据，从而导致隐私侵犯。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.jalopnik.com/1982690/police-flock-cameras-sued-for-tracking-man-526-times/">Police Used Flock Cameras To Track One Driver Over 500 Times.</a></li>
<li><a href="https://www.infosecinstitute.com/resources/general-security/privacy-implications-automatic-license-plate-recognition-technology/">Privacy Implications of Automatic License Plate Recognition...</a></li>
<li><a href="https://www.govtech.com/em/safety/despite-successes-alpr-tech-still-raises-privacy-concerns?_amp=true">Despite Successes, ALPR Tech Still Raises Privacy Concerns</a></li>

</ul>
</details>

**社区讨论**: 评论者就滥用行为罕见的主张与警官跟踪熟人的普遍性之间的紧张关系展开了辩论。一些人将其与更广泛的监控担忧相类比，而另一些人则认为，如果没有搜查令，这类系统会招致滥用。

**标签**: `#privacy`, `#surveillance`, `#police accountability`, `#civil liberties`, `#license plate readers`

---

<a id="item-5"></a>
## [Mitchell 承诺向 Zig 基金会捐赠 40 万美元](https://mitchellh.com/writing/zig-donation-2026) ⭐️ 8.0/10

Mitchell Hashimoto 宣布再次向 Zig 软件基金会承诺捐赠 40 万美元，使他的总支持额达到 80 万美元，用于资助 Zig 编程语言的持续开发。 这笔巨额捐赠为 Zig 软件基金会提供了关键的财务稳定性，使该语言（旨在成为系统编程中 C 语言的现代替代品）能够更快地发展。 该承诺针对 2026 年，此前他在 2023 年已捐赠 40 万美元；Mitchell Hashimoto 是用 Zig 编写的 Ghostty 终端模拟器的创建者。

hackernews · tosh · 6月22日 13:43 · [社区讨论](https://news.ycombinator.com/item?id=48630020)

**背景**: Zig 是一种通用系统编程语言，旨在改进 C 语言，注重安全性、性能和简洁性。它由非营利组织 Zig 软件基金会（ZSF）维护。Mitchell Hashimoto 是 HashiCorp 的联合创始人，是一位著名的开源开发者，一直是 Zig 的主要财务支持者。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Zig_(programming_language)">Zig (programming language)</a></li>
<li><a href="https://ziglang.org/">Home ⚡ Zig Programming Language</a></li>

</ul>
</details>

**社区讨论**: 社区反应积极，许多人赞扬 Hashimoto 的慷慨及其对 Zig 开发的影响。一些评论者指出 Ghostty 的质量是 Zig 的展示，而其他人则讨论了该语言反对 LLM 生成贡献的立场。

**标签**: `#zig`, `#programming-languages`, `#open-source`, `#funding`, `#donation`

---

<a id="item-6"></a>
## [Deno Desktop 推出多后端 Webview 框架](https://docs.deno.com/runtime/desktop/) ⭐️ 8.0/10

Deno 推出了名为 Deno Desktop 的桌面应用框架，支持多种 webview 后端（包括 CEF、Webview 和 Raw），通过共享运行时减少二进制文件大小，并通过权限系统增强安全性。 Deno Desktop 为 Electron 提供了一种有吸引力的替代方案，通过将应用二进制大小降至几兆字节，并利用其细粒度的权限系统提升安全性，降低了使用 Web 技术构建跨平台桌面应用的门槛。 该框架支持 CEF、系统 Webview（macOS/Linux 上的 WebKit，Windows 上的 Edge WebView2）以及 Raw 后端。共享运行时已列入路线图，预计可将每个应用的二进制大小降至几兆字节。

hackernews · GeneralMaximus · 6月22日 05:38 · [社区讨论](https://news.ycombinator.com/item?id=48626137)

**背景**: 像 Electron 这样的桌面应用框架会为每个应用捆绑完整的 Chromium 浏览器引擎，导致二进制文件体积庞大（通常超过 100 MB）。Webview 后端使用系统自带的浏览器引擎，从而减小体积。CEF 允许嵌入 Chromium，但仍然较大。Deno Desktop 的共享运行时方法旨在让多个应用共享一份 CEF 副本，进一步减少磁盘占用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/webview/webview">GitHub - webview/webview: Tiny cross-platform webview library for C/C++. Uses WebKit (GTK/Cocoa) and Edge WebView2 (Windows). · GitHub</a></li>
<li><a href="https://en.wikipedia.org/wiki/Chromium_Embedded_Framework">Chromium Embedded Framework</a></li>

</ul>
</details>

**社区讨论**: 评论者对共享 CEF 运行时和权限系统集成表现出兴趣。一位用户质疑跨不同应用共享 CEF 时的版本管理问题。另一位建议添加类似 WebUI 的“在浏览器中启动”选项，以获得更好的权衡。总体情绪积极，许多人称赞 Deno 生态系统的成熟。

**标签**: `#deno`, `#desktop-apps`, `#webview`, `#cef`, `#electron`

---

<a id="item-7"></a>
## [Claude Code '扩展思维'输出仅为有损摘要](https://patrickmccanna.net/the-text-in-claude-codes-extended-thinking-output-is-not-authentic/) ⭐️ 8.0/10

文章指出，Claude Code 的“扩展思维”功能生成的输出并非模型的真实推理过程，而是有损摘要，这引发了关于透明度和安全性的担忧。 此事意义重大，因为隐藏推理过程削弱了 AI 透明度，使得审核模型的安全性和可信度更加困难。同时，它也为潜在的提示注入攻击提供了可能，恶意指令可能被隐藏在推理链中。 文章使用了 JPEG 与 BMP 的类比来说明数据丢失：压缩后的摘要无法还原为原始推理过程。社区评论指出，OpenAI 和 Google 等公司也为了保持竞争优势而隐藏推理过程。

hackernews · 0o_MrPatrick_o0 · 6月22日 14:22 · [社区讨论](https://news.ycombinator.com/item?id=48630535)

**背景**: “扩展思维”是一项功能，让 Claude 在回答前通过“草稿板”进行推理，提供逐步的思维过程。然而，用户看到的输出可能是摘要而非完整推理，这可能会丢失细节和上下文。有损摘要为了效率而有意丢弃部分细节，但存在削弱准确性的风险。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://platform.claude.com/docs/en/build-with-claude/extended-thinking">Extended thinking - Claude API Docs</a></li>
<li><a href="https://zeromathai.com/en/lossy-lossless-summary-en/">Lossy Summary vs Lossless Summary — A Summarization ...</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍认为隐藏推理是已知做法，理由包括竞争保密性和安全性考虑。一些人警告这会增加提示注入攻击的风险，而另一些人则指出，根据关于“不可读推理”的研究，推理块甚至可能与人类推理完全不同。

**标签**: `#AI transparency`, `#reasoning`, `#safety`, `#Claude`, `#LLM`

---

<a id="item-8"></a>
## [近半数 LG 智能电视应用含住宅代理 SDK](https://spur.us/blog/smart-tv-apps-residential-proxy-sdks) ⭐️ 8.0/10

Spur.us 调查发现，近半数 LG Content Store 中的智能电视应用包含住宅代理 SDK，这些 SDK 在未经用户同意的情况下将电视变成代理节点。 这严重侵犯隐私，因为用户的家庭网络在不知情的情况下被用于代理流量，可能助长网页抓取或绕过地理封锁等恶意行为。 受影响的应用是第三方应用，而非 LG 的原生应用。这些 SDK 由第三方代理服务商提供，嵌入在流媒体和工具类等流行应用中。

hackernews · microcode · 6月22日 20:48 · [社区讨论](https://news.ycombinator.com/item?id=48635954)

**背景**: 住宅代理使用由互联网服务提供商分配给真实家庭的 IP 地址，使流量看起来来自合法的家庭用户而非数据中心。它常用于网页抓取、广告验证或绕过地理限制。当未经披露地嵌入智能电视应用时，它会将电视变成代理网络中的一个节点，消耗用户带宽并可能使他们的网络遭受滥用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://techreviewadvisor.com/what-is-a-residential-proxy/">What Is a Residential Proxy? How It Works - Tech Review Advisor</a></li>
<li><a href="https://www.fbi.gov/investigate/cyber/alerts/2026/evading-residential-proxy-networks-protecting-your-devices-from-becoming-a-tool-for-criminals">Evading Residential Proxy Networks: Protecting Your Devices ...</a></li>

</ul>
</details>

**社区讨论**: 评论表达了对智能电视的强烈担忧和不信任。用户建议永远不要将智能电视连接到网络，或者将其隔离在设有防火墙的 VLAN 中。有人指出受影响的是第三方应用而非内置应用，并讨论了来自住宅 IP 的抓取行为日益增多。

**标签**: `#privacy`, `#smart TV`, `#residential proxy`, `#security`, `#IoT`

---

<a id="item-9"></a>
## [使用 Claude Code 将 Moebius 图像修复模型移植到浏览器](https://simonwillison.net/2026/Jun/22/porting-moebius/#atom-everything) ⭐️ 8.0/10

Simon Willison 成功将 Moebius 0.2B 轻量级图像修复模型移植到网页浏览器中运行，利用 WebGPU 加速，并在 AI 编程代理 Claude Code 的协助下完成。演示地址为 simonw.github.io/moebius-web/。 此次移植证明，最先进的机器学习模型可以在浏览器中高效运行，减少对服务器端推理的依赖，并支持隐私保护和离线应用。它降低了开发人员将高级图像编辑功能集成到 Web 应用中的门槛。 移植使用了 ONNX Runtime Web 的 WebGPU 后端，绕过了原有的 PyTorch 和 CUDA 依赖。模型权重被转换为 ONNX 格式，Claude Code 在过程中协助了研究探索和代码生成。

rss · Simon Willison · 6月22日 23:43

**背景**: Moebius 是一个 0.2B 参数的图像修复模型，在轻量级的同时实现了与 10B 级别模型相当的性能。WebGPU 是一种现代浏览器 API，允许 Web 应用利用设备 GPU 进行高性能计算。Claude Code 是 Anthropic 推出的 AI 编程代理，能够自主编写、编辑和调试项目代码。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://hustvl.github.io/Moebius/">Moebius: 0.2B Lightweight Image Inpainting Framework with 10B ...</a></li>
<li><a href="https://github.com/mlc-ai/web-llm">GitHub - mlc-ai/web-llm: High-performance In-browser LLM Inference Engine · GitHub</a></li>
<li><a href="https://code.claude.com/docs/en/how-claude-code-works">How Claude Code works - Claude Code Docs</a></li>

</ul>
</details>

**标签**: `#image inpainting`, `#WebGPU`, `#machine learning`, `#browser inference`, `#Claude Code`

---

<a id="item-10"></a>
## [Xfce 的 Wayland 合成器 xfwl4 首个预览版发布](https://lwn.net/Articles/1078942/) ⭐️ 8.0/10

Brian Tarricone 宣布了 xfwl4 的首个预览版（Alpha 版本），这是为 Xfce 桌面环境开发的 Wayland 合成器，经过近六个月的开发。 这标志着 Xfce 从 X11 向 Wayland 过渡的重要里程碑，为轻量级桌面环境带来了现代显示服务器功能，并扩大了 Wayland 在 Linux 生态系统中的采用。 该合成器使用 Rust 语言编写，旨在与 Xfwm4 功能对等，但目前仍缺少许多行为和设置，用户应预期存在错误。

rss · LWN.net · 6月22日 13:44

**背景**: Wayland 是 Linux 上的显示服务器协议，旨在以更安全、更简单的方式取代旧的 X Window 系统。Xfce 是一个轻量级桌面环境，传统上在 X11 上使用 Xfwm4 窗口管理器。xfwl4 项目于 2026 年初宣布，代表 Xfce 对 Wayland 支持的投入，是作为独立的合成器开发，而非修改 Xfwm4。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wayland_compositor">Wayland compositor</a></li>
<li><a href="https://github.com/hanthor/xfwl4">GitHub - hanthor/xfwl4: xfwl4 Wayland compositor for XFCE</a></li>
<li><a href="https://www.phoronix.com/news/Xfce-Xfwl4-Wayland">Xfwl4 Being Developed As New Wayland Compositor For Xfce</a></li>

</ul>
</details>

**标签**: `#Xfce`, `#Wayland`, `#Linux desktop`, `#compositor`

---

<a id="item-11"></a>
## [OSPM 2026 第一天：空闲状态、sched_ext 和锁持有者抢占](https://lwn.net/Articles/1077759/) ⭐️ 8.0/10

OSPM 2026 Linux 内核电源管理与调度峰会第一天的报告涵盖了 CPU 空闲状态选择标准、sched_ext 可扩展调度器类以及虚拟化中锁持有者抢占问题的讨论。 这些话题对于提高 Linux 内核在电源管理和调度方面的效率至关重要，影响电池供电设备和数据中心的性能。这些讨论可能推动未来的内核补丁，以优化能耗并减少延迟。 cpuidle 维护者 Rafael Wysocki 讨论了空闲状态调控器的成功标准。会议还讨论了 sched_ext（允许基于 BPF 的调度器）以及锁持有者抢占问题（即持有自旋锁的虚拟 CPU 被抢占，导致性能问题）。

rss · LWN.net · 6月22日 13:26

**背景**: OSPM（操作系统导向的电源管理）峰会是 Linux 内核开发者年度聚会，专注于电源管理和调度。cpuidle 子系统负责将空闲 CPU 置于低功耗状态，调控器根据预测的空闲时长选择合适的空闲状态。sched_ext 是一项内核特性，允许将调度器实现为 BPF 程序，从而实现快速实验。锁持有者抢占是虚拟化中的经典问题：管理程序抢占持有自旋锁的 vCPU，导致其他 vCPU 空转浪费。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/sched-ext/scx">GitHub - sched-ext/scx: sched_ext schedulers and tools Overview - sched_ext linux/tools/sched_ext/README.md at master · torvalds/linux sched-ext Tutorial | CachyOS sched_ext Linux 7.2 sched_ext Continues Working Toward Sub-Scheduler ...</a></li>
<li><a href="https://sched-ext.com/docs/OVERVIEW">Overview - sched_ext</a></li>
<li><a href="https://stackoverflow.com/questions/30780311/lock-holder-preemption">multithreading - Lock Holder Preemption - Stack Overflow</a></li>

</ul>
</details>

**标签**: `#Linux kernel`, `#power management`, `#scheduling`, `#OSPM 2026`

---

<a id="item-12"></a>
## [美光计划投入 2000 亿美元扩产应对 AI 存储芯片短缺](https://t.me/zaihuapd/42101) ⭐️ 8.0/10

美光科技宣布计划投入 2000 亿美元在美国及全球范围内扩建晶圆厂，以缓解 AI 热潮引发的存储芯片供应瓶颈。其中在爱达荷州总部投资 500 亿美元新建两座工厂，首座工厂预计 2027 年中投产，生产高带宽内存（HBM）所需的 DRAM 芯片。 这一巨额投资凸显了高带宽内存（HBM）在 AI 硬件中的关键作用——过去一年 DRAM 价格涨幅超过 170%，美光的 HBM3e 和 HBM4 产能已售罄至 2026 年底。扩产将有助于保障 AI 加速器的供应，并可能影响全球半导体供应链格局。 美光 2000 亿美元总投资分散在全球多个地点，仅爱达荷州首座工厂就耗资 500 亿美元。受 AI 需求推动，公司毛利率已升至 56%；HBM 的生产涉及复杂的 DRAM 芯片 3D 堆叠技术，以实现高带宽和低功耗。

telegram · zaihuapd · 6月22日 05:30

**背景**: 高带宽内存（HBM）是一种 3D 堆叠 DRAM 技术，可提供超高带宽和能效，是 GPU 等 AI 加速器的关键组件。AI 热潮大幅推升了 HBM 需求，传统内存产能难以满足，导致供应紧张。美光、三星和 SK 海力士是少数几家能生产 HBM 的制造商。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/High_Bandwidth_Memory">High Bandwidth Memory - Wikipedia</a></li>
<li><a href="https://www.techtarget.com/whatis/definition/high-bandwidth-memory">What is high-bandwidth memory (HBM)? - TechTarget High Bandwidth Memory (HBM): Everything You Need To Know High-Bandwidth Memory (HBM) - Semiconductor Engineering High Bandwidth Memory (HBM): Everything You Need to Know HBM (High Bandwidth Memory): Concept, Architecture, and ... High Bandwidth Memory (HBM) Explained</a></li>
<li><a href="https://semiengineering.com/high-bandwidth-memory-hbm-everything-you-need-to-know/">High Bandwidth Memory (HBM): Everything You Need To Know</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#HBM`, `#AI hardware`, `#memory chips`, `#investment`

---

<a id="item-13"></a>
## [48 位中国开发者举报苹果垄断](https://m.nbd.com.cn/articles/2026-06-22/4433380.html) ⭐️ 8.0/10

2026 年 6 月 22 日，48 位中国 iOS 开发者向国家市场监督管理总局提交举报信，指控苹果滥用中国市场垄断地位，未兑现中国区 App Store 费率不高于其他市场整体水平的承诺，要求苹果开放第三方应用分发和支付渠道。 此次举报可能加剧苹果在中国（其第二大 iOS 市场）面临的监管压力，并可能迫使其调整 App Store 的佣金政策和第三方支付渠道开放策略，对全球反垄断讨论产生影响。 开发者还建议建立‘全球政策自动对齐监督机制’，以确保费率一致和市场开放。虽然苹果在 2026 年 3 月下调了中国区佣金，但开发者认为由于缺乏第三方分发和支付渠道，实际议价空间并未改善。

telegram · zaihuapd · 6月22日 14:57

**背景**: ‘苹果税’是指苹果对应用内购买和付费下载收取的 15%至 30%的佣金。在中国，随着监管机构推动公平竞争，苹果面临越来越大的反垄断压力。欧盟、韩国等其他司法管辖区也出现了类似行动，迫使苹果允许第三方支付系统等改变。

**标签**: `#Apple`, `#antitrust`, `#App Store`, `#China`, `#monopoly`

---