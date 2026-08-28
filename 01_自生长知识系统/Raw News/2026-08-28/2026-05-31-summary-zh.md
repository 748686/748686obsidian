---
layout: default
title: "Horizon Summary: 2026-05-31 (ZH)"
date: 2026-05-31
lang: zh
---

> 从 48 条内容中筛选出 14 条重要资讯。

---

1. [在浏览器中用 Pyodide 和服务工作进程运行 Python ASGI 应用](#item-1) ⭐️ 9.0/10
2. [SpaceX 获 41.6 亿美元美军卫星导弹追踪合同](#item-2) ⭐️ 9.0/10
3. [埃森哲以 12 亿美元收购 Ookla](#item-3) ⭐️ 8.0/10
4. [Zig ELF 链接器改进日志详解](#item-4) ⭐️ 8.0/10
5. [Voxel Space 教程重现 1992 年《Comanche》图形技术](#item-5) ⭐️ 8.0/10
6. [OpenRouter 获 1.13 亿美元 B 轮融资](#item-6) ⭐️ 8.0/10
7. [Openrsync：OpenBSD 对 rsync 的重实现，已被 macOS 采用](#item-7) ⭐️ 8.0/10
8. [教皇利奥首篇通谕抨击技术弥赛亚主义](#item-8) ⭐️ 8.0/10
9. [Anthropic 详解 Claude 产品沙箱技术](#item-9) ⭐️ 8.0/10
10. [调试器揭示训练失败局部化到特定层和步骤](#item-10) ⭐️ 8.0/10
11. [英伟达发布 Qwen3.6-35B-A3B 的 NVFP4 量化版本](#item-11) ⭐️ 8.0/10
12. [本地 LLM 推理的 GPU 规格对比挑战 Mac 推荐](#item-12) ⭐️ 8.0/10
13. [Parallax：用于大语言模型的参数化局部线性注意力机制](#item-13) ⭐️ 8.0/10
14. [华为提出“韬定律”：用时间缩微替代几何缩微](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [在浏览器中用 Pyodide 和服务工作进程运行 Python ASGI 应用](https://simonwillison.net/2026/May/30/pyodide-asgi-browser/#atom-everything) ⭐️ 9.0/10

Simon Willison 展示了一种使用 Pyodide 和服务工作进程在浏览器中运行 Python ASGI 应用的方法，使得之前基于 Web Worker 的方法中无法执行的 JavaScript 脚本标签得以正常运行。这是通过 Claude Code 实验实现的，并在 Datasette Lite 和一个基本的 ASGI FastCGI 演示中进行了测试。 这一突破克服了在浏览器中运行 Python 应用的关键限制，使得依赖 JavaScript 的插件和动态内容能够正常执行。它显著增强了 Datasette Lite 等浏览器内 Python 工具的能力，并扩展了无服务器 Python 应用的潜力。 该演示使用服务工作进程替代 Web Worker 来拦截网络请求并在 Pyodide 中运行 Python ASGI 应用，从而保留了脚本标签的执行。Simon 计划在完全理解实现后，将 Datasette Lite 升级为采用这种方法。

rss · Simon Willison · 5月30日 21:02

**背景**: Pyodide 是一个基于 WebAssembly 的浏览器 Python 发行版，允许 Python 完全在客户端运行。ASGI（异步服务器网关接口）是异步 Python Web 服务器和应用的规范，支持 FastAPI 和 Starlette 等现代 Web 框架。服务工作进程是在 Web 浏览器后台运行的脚本，能够拦截网络请求并实现离线体验。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://pyodide.org/">Pyodide — Version 0.29.4</a></li>
<li><a href="https://github.com/pyodide/pyodide">GitHub - pyodide / pyodide : Pyodide is a Python distribution for...</a></li>

</ul>
</details>

**标签**: `#Pyodide`, `#ASGI`, `#WebAssembly`, `#Datasette`, `#Service Workers`

---

<a id="item-2"></a>
## [SpaceX 获 41.6 亿美元美军卫星导弹追踪合同](https://www.bloomberg.com/news/articles/2026-05-29/spacex-wins-4-billion-contract-for-us-golden-dome-satellites) ⭐️ 9.0/10

SpaceX 获得美国太空军 41.6 亿美元合同，开发天基导弹追踪卫星星座，作为 Golden Dome 防御系统的一部分。 这份合同标志着 SpaceX 在国家安全太空领域角色的重大扩展，该网络旨在减少现有地面雷达和空中监视的盲区。它将 SpaceX 置于下一代分层导弹防御架构的核心位置。 该星座将整合天基传感器、通信系统和地面处理能力，从轨道上跟踪外国飞机、导弹和其他空中威胁。SpaceX 此前已参与 Golden Dome 的天基拦截器原型开发，并加入了该计划底层软件系统的多公司联盟。

telegram · zaihuapd · 5月30日 01:53

**背景**: Golden Dome 防御计划由特朗普总统于 2025 年 5 月宣布，是 1980 年代战略防御倡议（SDI，常被称为“星球大战”）的现代版本。它旨在利用天基传感器和拦截器创建一个分层本土导弹防御系统，以应对弹道导弹和高超音速导弹等不断演变的威胁。类似概念于 2019 年在太空发展局的国防太空架构下重新出现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nytimes.com/2025/05/20/us/politics/trump-golden-dome.html">Trump Unveils Plans for ‘Golden Dome’ Missile Defense</a></li>
<li><a href="https://en.wikipedia.org/wiki/Space-Based_Interceptor">Space-Based Interceptor</a></li>

</ul>
</details>

**标签**: `#SpaceX`, `#defense`, `#satellite`, `#military`, `#space`

---

<a id="item-3"></a>
## [埃森哲以 12 亿美元收购 Ookla](https://newsroom.accenture.com/news/2026/accenture-to-acquire-ookla-to-strengthen-network-intelligence-and-experience-with-data-and-ai-for-enterprises) ⭐️ 8.0/10

埃森哲宣布以 12 亿美元收购 Ookla，后者旗下拥有 Speedtest 和 Downdetector，旨在通过数据和 AI 增强企业网络智能。 此次收购使埃森哲能够获取来自数百万消费者测试的大量网络性能数据，从而为电信和企业提供更深入的洞察。同时，这也引发了数据信任和潜在利益冲突的担忧，因为埃森哲现在拥有了监控其咨询客户中断情况的工具。 交易包括 Ookla 的数据产品，如 Speedtest、Downdetector、Ekahau 和 RootMetrics，每月有超过 2.5 亿次消费者发起的测试。埃森哲计划利用这些数据帮助通信服务提供商优化 Wi-Fi 和 5G 网络。

hackernews · Garbage · 5月30日 16:28 · [社区讨论](https://news.ycombinator.com/item?id=48337987)

**背景**: Ookla 最著名的产品是 Speedtest.net，这是一个广泛使用的互联网速度测试平台。其数据对电信运营商的网络规划和优化具有很高价值。埃森哲是一家全球专业服务公司，专注于 IT 服务和咨询。此次收购符合埃森哲将数据和 AI 整合到企业网络解决方案中的战略。

**社区讨论**: 社区评论指出，交易的实际价值在于数据而非消费者工具，电信运营商每年支付六位数费用获取洞察。一些人表达了不信任，担心埃森哲可能操纵中断数据以保护其咨询客户。一位前员工证实数据业务利润丰厚，且埃森哲此前已通过收购 Umlaut 成为竞争对手。

**标签**: `#acquisition`, `#network intelligence`, `#data`, `#AI`, `#enterprise`

---

<a id="item-4"></a>
## [Zig ELF 链接器改进日志详解](https://ziglang.org/devlog/2026/#2026-05-30) ⭐️ 8.0/10

Zig 团队发布的新开发日志详细介绍了其 ELF 链接器的改进，重点在于更快的增量编译和链接，以加速开发迭代。 这些改进可能大幅缩短编译-链接-迭代的时间，使 Zig 成为更实用的 C 语言替代品，特别是在系统编程领域。同时，它还能提升工具链的互操作性，并可能促使 Raku 等其他语言考虑将 Zig 作为后端目标。 该链接器支持增量链接，有利于开发阶段，但由于可能与链接时优化不兼容，可能不适合发布构建。开发日志中包含了社区期待已久的具体技术进展。

hackernews · kristoff_it · 5月30日 17:29 · [社区讨论](https://news.ycombinator.com/item?id=48338673)

**背景**: Zig 是一种现代系统编程语言，旨在改进 C 语言，具有编译时泛型、手动内存管理、无隐藏控制流等特点。ELF（可执行与可链接格式）是 Linux 及类 Unix 系统上的标准二进制格式，而链接器是将目标文件组合成可执行文件的工具。Zig 链接器是自托管的组件，负责处理 Zig 及其他语言的链接，其性能对开发者效率至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Zig_(programming_language)">Zig (programming language)</a></li>
<li><a href="https://en.wikipedia.org/wiki/ELF_file_format">ELF file format</a></li>
<li><a href="https://ziglang.org/">Home Zig Programming Language</a></li>

</ul>
</details>

**社区讨论**: 评论中对链接器的进展表示兴奋，用户认为它可能使 Zig 成为真正的 C 语言替代品，并实现类似动态语言的快速迭代。一些人讨论了将 Raku 的虚拟机移植到 Zig 等潜在应用，而另一些人则对增量链接与发布模式优化的兼容性提出疑问。

**标签**: `#Zig`, `#linker`, `#systems programming`, `#compilers`, `#performance`

---

<a id="item-5"></a>
## [Voxel Space 教程重现 1992 年《Comanche》图形技术](https://s-macke.github.io/VoxelSpace/) ⭐️ 8.0/10

一个交互式教程发布了，详细解释了 1992 年游戏《Comanche》中使用的 Voxel Space 算法，通过逐步可视化演示了基于高度图的地形渲染。 本教程罕见地深入剖析了一项开创性的复古图形技术，让现代开发者和爱好者易于理解，并保存了实时 3D 渲染的历史。 该算法本质上是一种高度图渲染器，而非真正的体素渲染，因为它使用二维高度数组来创建三维地形。教程包含交互式演示，并提供了 C++ 和 AGS 移植版的链接。

hackernews · davikr · 5月30日 14:25 · [社区讨论](https://news.ycombinator.com/item?id=48336564)

**背景**: Voxel Space 算法由 NovaLogic 为 1992 年的直升机战斗游戏《Comanche》开发，在早期 PC 上实现了流畅的地形渲染。与在三维网格中存储数据的真正体素方法不同，它使用高度图——一种灰度图像，每个像素的亮度代表海拔——通过将棱柱列投影到屏幕上来高效渲染景观。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.colinhoad.com/voxel-space-demo-bits-and-bytes-ep-4">Voxel Space Demo - Bits and Bytes (Ep. 4) | Colin Hoad</a></li>
<li><a href="https://en.wikipedia.org/wiki/Heightmap">Heightmap - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论者指出了高度图与真正体素之间的技术区别，一位用户分享了在代码测试中使用“油罐假期”测试的个人轶事。多位用户贡献了他们在 C++、AGS 等平台上的实现链接，凸显了该算法的持久影响力。

**标签**: `#voxel-space`, `#terrain-rendering`, `#retro-graphics`, `#algorithm`, `#comanche`

---

<a id="item-6"></a>
## [OpenRouter 获 1.13 亿美元 B 轮融资](https://openrouter.ai/announcements/series-b) ⭐️ 8.0/10

统一的大语言模型 API 代理平台 OpenRouter 获得了 1.13 亿美元的 B 轮融资，将用于扩大其基础设施和用户基础。 这一大额融资轮表明投资者对 AI 基础设施中介的强烈信心，OpenRouter 通过在单一 API 后聚合超过 300 个模型，降低了开发者的使用门槛，可能加速多样化大语言模型的采用。 OpenRouter 对 API 使用收取 5% 的附加费，并声称全球有超过 25 万款应用和 420 万用户。融资后公司仍由创始人领导并控制。

hackernews · freeCandy · 5月30日 17:27 · [社区讨论](https://news.ycombinator.com/item?id=48338660)

**背景**: OpenRouter 是一个 API 代理，提供统一接口以访问数百种大语言模型，包括来自 OpenAI、Anthropic 和开源社区的模型。开发者可以用最少的代码更改切换模型，该平台还提供自动路由和计费上限等功能，而许多提供商缺少这些。该服务与 OpenAI SDK 兼容，使许多现有应用的集成变得简单。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://apify.com/apify/openrouter">OpenRouter · Apify</a></li>
<li><a href="https://openrouter.ai/">OpenRouter</a></li>
<li><a href="https://www.morphllm.com/openrouter-alternative">OpenRouter Alternative: Intelligent Model Routing vs API Proxies</a></li>

</ul>
</details>

**社区讨论**: Hacker News 上的社区评论反映了不同观点：许多人称赞 OpenRouter 的低门槛模型试验和计费上限，但也有一些人质疑其长期价值，考虑到 5% 的附加费和 LLM 市场可能的整合。联合创始人回应称公司仍由创始人控制，旨在为开发者构建强大产品。

**标签**: `#AI`, `#funding`, `#OpenRouter`, `#LLM`, `#API`

---

<a id="item-7"></a>
## [Openrsync：OpenBSD 对 rsync 的重实现，已被 macOS 采用](https://github.com/kristapsdz/openrsync) ⭐️ 8.0/10

OpenBSD 团队发布了 Openrsync，这是 rsync 文件同步工具的一个新实现，并已被 macOS 15.0 采用为默认 rsync。 这一重实现为广泛使用的 rsync 协议提供了更安全、更易维护的代码库，减少了对原 Samba 维护版本的依赖，并改善了在 BSD 和 macOS 生态系统中的集成。 Openrsync 最初是作为 RPKI 验证器项目的一部分开发的，尽管它在功能上基本与 Samba rsync 匹配，但部分用户报告了使用 --rsync-path 选项同步目录时的问题。

hackernews · sph · 5月30日 10:51 · [社区讨论](https://news.ycombinator.com/item?id=48334854)

**背景**: rsync 是一款流行的开源工具，用于跨系统高效传输和同步文件，常用于备份和镜像。原始实现由 Samba 团队维护，但由于代码复杂性和安全问题，出现了像 Openrsync 这样的替代实现。

**社区讨论**: 社区评论总体积极，注意到持续改进并期待独占使用。但一位用户指出了在同步到远程目录时 --rsync-path 标志的特定兼容性问题。另一条评论提到了 Gokrazy 团队开发的基于 Go 的独立 rsync 实现，还有用户提到原始 rsync 代码库中突然出现的“氛围编码”提交使得 Openrsync 成为受欢迎的替代。

**标签**: `#rsync`, `#openbsd`, `#implementation`, `#macos`, `#file-sync`

---

<a id="item-8"></a>
## [教皇利奥首篇通谕抨击技术弥赛亚主义](https://www.economist.com/europe/2026/05/28/leos-first-encyclical-attacks-technological-messianism) ⭐️ 8.0/10

教皇利奥发布了其首篇通谕，强烈批评技术弥赛亚主义（即认为技术能解决一切人类问题的信念），并警告不要用人工智能取代人类。 这篇通谕标志着一位重要宗教领袖在人工智能伦理和社会技术控制辩论中的重大干预，可能影响公众讨论和政策方向。 据报道，该通谕一方面谴责对人工智能的盲目信仰，另一方面也承认教皇本人使用技术，凸显了拥抱技术与警惕技术之间的张力。

hackernews · 1vuio0pswjnm7 · 5月30日 10:30 · [社区讨论](https://news.ycombinator.com/item?id=48334710)

**背景**: 技术弥赛亚主义是一种信念，认为技术将不可避免地带来积极结果并解决所有问题。教皇通谕是教皇就重大问题阐明天主教会官方立场的正式信函，对信徒具有重要的道德权威。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.economist.com/europe/2026/05/28/leos-first-encyclical-attacks-technological-messianism">Leo’s first encyclical attacks technological messianism</a></li>
<li><a href="https://en.wikipedia.org/wiki/Papal_encyclical">Papal encyclical</a></li>

</ul>
</details>

**社区讨论**: 评论者就谁应控制技术——技术专家、用户、政府还是宗教机构——展开辩论，一些人表达了对人工智能炒作的怀疑。另一些人则引用彼得·蒂尔关于敌基督的观点，并质疑人工智能 CEO 是否患有“人工智能精神病”。

**标签**: `#AI`, `#ethics`, `#technology`, `#religion`, `#society`

---

<a id="item-9"></a>
## [Anthropic 详解 Claude 产品沙箱技术](https://simonwillison.net/2026/May/30/how-we-contain-claude/#atom-everything) ⭐️ 8.0/10

Anthropic 发布了一篇详细博文，解释了如何通过 gVisor、Seatbelt 和 Bubblewrap 等技术在 Claude.ai、Claude Code 和 Cowork 中对 Claude 进行沙箱隔离。 这份文档通过提供详细的沙箱策略信息，弥补了 AI 沙箱中常见的信任缺失，帮助用户和开发者评估安全风险，增强部署智能代理的信心。 Claude.ai 使用 gVisor；macOS 上的 Claude Code 使用 Apple 的 Seatbelt 框架，Linux 上使用 Bubblewrap；Claude Cowork 运行在完整虚拟机中（macOS 上使用 Apple Virtualization，Windows 上使用 HCS）。文章还描述了过去的风险，如 api.anthropic.com/v1/files 的泄露途径。

rss · Simon Willison · 5月30日 21:36

**背景**: 沙箱是一种安全技术，通过隔离应用程序防止其影响主机系统或访问未授权数据。gVisor 是谷歌开发的开源应用内核，在用户空间实现多个 Linux 系统调用，提供比传统容器更强的隔离。Seatbelt 是 macOS 上的 Apple 沙箱框架，Bubblewrap 是用于 Flatpak 等工具的轻量级 Linux 沙箱。理解这些方法有助于读者体会 Anthropic 采用的分层安全策略。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GVisor">gVisor - Wikipedia</a></li>
<li><a href="https://wiki.archlinux.org/title/Bubblewrap">Bubblewrap - ArchWiki</a></li>
<li><a href="https://nono.sh/docs/cli/internals/seatbelt">macOS Seatbelt - Nono Docs</a></li>

</ul>
</details>

**标签**: `#AI safety`, `#Claude`, `#sandboxing`, `#security`, `#Anthropic`

---

<a id="item-10"></a>
## [调试器揭示训练失败局部化到特定层和步骤](https://www.reddit.com/r/MachineLearning/comments/1trui0b/what_i_learned_building_a_debugger_for_pytorch/) ⭐️ 8.0/10

一个名为 NeuralDBG 的 PyTorch 调试器已开源，它通过钩入训练循环，监控每层梯度范数转换，自动检测并定位梯度消失、梯度爆炸和数据异常等失败。 这将故障诊断从依赖全局损失曲线转变为聚焦特定层和步骤，使 ML 工程师能够更快更精确地调试，可能节省数小时的训练时间。 该工具提取语义事件如“梯度范数转换”和“首次出现追踪”，而非原始张量，使输出紧凑且可操作；还提供了一个简单的逐层梯度范数监控代码片段作为实用建议。

reddit · r/MachineLearning · /u/ProgrammerNo8287 · 5月30日 08:48

**背景**: 训练深度学习模型时常遇到梯度消失或爆炸等失败，通常通过监控损失曲线来诊断。但损失是全局聚合值，掩盖了根本原因。逐层梯度范数提供了更局部的信号，但原始范数噪声大；检测从正常到异常值的转换是关键。

**标签**: `#PyTorch`, `#debugging`, `#training failures`, `#deep learning`, `#gradient analysis`

---

<a id="item-11"></a>
## [英伟达发布 Qwen3.6-35B-A3B 的 NVFP4 量化版本](https://www.reddit.com/r/LocalLLaMA/comments/1ts6j6j/nvidiaqwen3635ba3bnvfp4_hugging_face/) ⭐️ 8.0/10

英伟达发布了使用 NVFP4 数据类型量化的 Qwen3.6-35B-A3B 模型版本，实现了约 3.06 倍的内存需求缩减，同时在多个基准测试中保持了几乎相同的准确率。 这使得在有限硬件上高效部署大型混合专家模型成为可能，大大降低了本地运行先进大语言模型的门槛。极小的准确率损失（例如 MMLU Pro 从 85.6 降至 85.0）使 NVFP4 成为生产环境的实用选择。 仅量化了 MoE 中 Transformer 块的线性算子权重和激活值，每参数比特数从 16 降至 4。该模型使用英伟达的 Model Optimizer 进行量化，并可直接用于 vLLM 引擎的推理。

reddit · r/LocalLLaMA · /u/pmttyji · 5月30日 17:49

**背景**: 量化通过降低模型权重的数值精度来减少内存使用并加速推理。NVFP4 是一种具有共享指数和紧凑尾数的浮点格式，相比均匀 INT4 提供更高的动态范围。Qwen3.6-35B-A3B 是一个 350 亿参数的混合专家（MoE）模型，每个 token 仅激活部分专家，高效但内存密集。vLLM 是一个支持多种量化格式的高吞吐量推理引擎。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://build.nvidia.com/spark/nvfp4-quantization">NVFP4 Quantization | DGX Spark</a></li>
<li><a href="https://github.com/vllm-project/vllm">GitHub - vllm -project/ vllm : A high-throughput and memory ...</a></li>
<li><a href="https://arxiv.org/abs/2507.11181">[2507.11181] Mixture of Experts in Large Language Models</a></li>

</ul>
</details>

**标签**: `#quantization`, `#nvidia`, `#qwen`, `#efficient inference`, `#model optimization`

---

<a id="item-12"></a>
## [本地 LLM 推理的 GPU 规格对比挑战 Mac 推荐](https://www.reddit.com/r/LocalLLaMA/comments/1trkze4/i_compared_all_specs_of_the_major_gpusmachines/) ⭐️ 8.0/10

一位 Reddit 用户发布了对主要 GPU（包括 RTX PRO 6000、Intel Arc Pro B70、Radeon MI50、RTX 5070 Ti 等）进行本地 LLM 推理的全面对比，分析了价格、FP16 TFLOPS、显存、带宽以及$/TFLOP 和$/GB 等派生指标，认为 Mac 在此用途上性价比偏低。 这种基于数据的对比帮助本地 LLM 社区超越品牌偏见做出更明智的硬件购买决策，尤其适合那些看重预填充速度和总拥有成本的用户。 作者强调显存带宽通常是 LLM 推理的瓶颈，而预填充性能被常见的文本生成基准测试所忽视；表格包含了 Max-Q 版本的功耗效率，并指出某些 GPU 通过张量核心支持 2–4 倍更快的 FP16/BF16。

reddit · r/LocalLLaMA · /u/Ok_Top9254 · 5月30日 00:44

**背景**: 对于本地 LLM 推理，关键 GPU 规格包括 FP16 TFLOPS（半精度计算吞吐量）、显存容量（可容纳模型大小）和显存带宽（数据传输速度，通常是首令牌后的主要瓶颈）。Max-Q 是 NVIDIA 在专业 GPU 中优化功耗和性能的技术。作者使用$/TFLOP 和$/GB 等派生指标来评估成本效率。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ozyphus.github.io/gpu-maths.html">GPU Mathematics for Machine Learning - Interactive Guide</a></li>
<li><a href="https://www.adaline.ai/blog/understanding-gpu-for-inference-in-llms">Understanding GPU for Inference in LLMs | Adaline</a></li>
<li><a href="https://www.nvidia.com/en-sg/geforce/gaming-laptops/max-q-technologies/">Max-Q Technologies for Laptops | NVIDIA</a></li>

</ul>
</details>

**标签**: `#GPU`, `#LLM`, `#hardware comparison`, `#local inference`, `#performance`

---

<a id="item-13"></a>
## [Parallax：用于大语言模型的参数化局部线性注意力机制](https://www.reddit.com/r/LocalLLaMA/comments/1ts79rg/parallax_parameterized_local_linear_attention_for/) ⭐️ 8.0/10

研究人员提出了 Parallax，这是一种参数化的局部线性注意力机制，通过移除数值求解器并添加一个可学习的类似查询的投影器来探测 KV 协方差，从而能够在大语言模型预训练中扩展。 这项工作在理论上比标准 softmax 注意力有更优的偏差-方差权衡，并在 0.6B 和 1.7B 参数规模上展示了持续的困惑度改进，标志着注意力机制中首次实现了架构与优化器的协同设计。 Parallax 采用了一种硬件感知算法，提高了相对于 FlashAttention 的算术强度，其原型解码内核在多种批大小和上下文长度下匹配或超越 FlashAttention 2/3。其优势在参数匹配和计算匹配控制下均持续存在，并且发现 Muon 优化器能够释放 Parallax 的能力。

reddit · r/LocalLLaMA · /u/Thrumpwart · 5月30日 18:18

**背景**: 标准 Transformer 注意力使用 softmax，这属于测试时回归框架中的局部常数估计。局部线性注意力 (LLA) 将其升级为局部线性估计，改善了偏差-方差权衡，但由于数值求解器面临可扩展性问题。Parallax 引入了一个参数化版本，移除了这些求解器并学习到 KV 协方差的投影器，从而实现了高效的预训练。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2605.29157">[2605.29157] Parallax: Parameterized Local Linear Attention for...</a></li>
<li><a href="https://openreview.net/pdf?id=WGpzi489XY">L ATTENTION : AN OPTIMAL INTERPO L SOFTMAX ATTENTION FOR EST-T R</a></li>

</ul>
</details>

**标签**: `#attention mechanism`, `#LLM`, `#efficient attention`, `#language modeling`, `#machine learning research`

---

<a id="item-14"></a>
## [华为提出“韬定律”：用时间缩微替代几何缩微](https://t.me/zaihuapd/41648) ⭐️ 8.0/10

华为在 2026 年国际电路与系统研讨会上正式提出“韬定律”，主张用“时间缩微”替代传统的“几何缩微”推动半导体发展。该公司已依据该定律设计并量产了 381 款芯片，并计划于 2026 年秋季推出采用逻辑折叠技术的新麒麟芯片。 “韬定律”为后摩尔时代的半导体发展提供了新路径，有望突破物理缩放极限，重塑全球芯片产业格局。这是中国首次提出指导全球半导体演进的原则，具有重要的战略意义。 韬定律通过降低时间常数τ，实现器件、电路、芯片到系统的多层级协同优化，目标是到 2031 年达到 1.4 纳米制程等效的晶体管密度。逻辑折叠技术是一种真正的 3D 芯片设计方法，通过在逻辑门层面优化互连，超越了传统 2D 和伪 3D 设计。

telegram · zaihuapd · 5月30日 02:18

**背景**: 摩尔定律指出芯片晶体管密度大约每两年翻一番，但随着晶体管尺寸缩小到原子尺度，该定律正逼近物理极限。华为的“韬定律”引入了“时间缩微”——缩短信号传播延迟——作为缩小尺寸的替代方案，通过系统级协同优化而非单纯依赖工艺节点进步来维持性能提升。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://baike.baidu.com/item/时间缩微/67842555">时间缩微 _百度百科</a></li>
<li><a href="https://zhichai.net/topic/177620770">华为"韬定律"深度解读：从几何 缩微 到 时间缩微 的范式跃迁</a></li>
<li><a href="https://k.sina.com.cn/article_5953189932_162d6782c06704cr5a.html?cre=tianyi&mod=pcpager_tech&loc=12&r=0&rfunc=24&tj=cxvertical_pc_pager_spt&tr=12">k.sina.com.cn/article_5953189932_162d6782c06704cr5a.html?cre...</a></li>

</ul>
</details>

**标签**: `#semiconductor`, `#Huawei`, `#chip design`, `#Moore's Law`, `#innovation`

---