---
layout: default
title: "Horizon Summary: 2026-06-07 (ZH)"
date: 2026-06-07
lang: zh
---

> 从 45 条内容中筛选出 15 条重要资讯。

---

1. [全国首例侵入式脑机接口让失明 20 年患者重见光明](#item-1) ⭐️ 9.0/10
2. [Meta 确认 AI 聊天机器人漏洞导致 Instagram 账户被黑](#item-2) ⭐️ 8.0/10
3. [超越 fork()+exec()：Unix 进程创建模型的再思考](#item-3) ⭐️ 8.0/10
4. [Zeroserve：基于 eBPF 脚本的零配置 Web 服务器](#item-4) ⭐️ 8.0/10
5. [英伟达为 Windows PC 提出高性能 CPU 方案](#item-5) ⭐️ 8.0/10
6. [HN 用户质疑社区的反 AI 情绪](#item-6) ⭐️ 8.0/10
7. [MicroPython 编译为 WebAssembly 实现 Python 沙箱](#item-7) ⭐️ 8.0/10
8. [Cohere 提供未发布编码模型早期访问，采用高效架构](#item-8) ⭐️ 8.0/10
9. [PewDiePie 的 Odysseus AI 工具发现一键管理员接管漏洞](#item-9) ⭐️ 8.0/10
10. [在 12GB 显存上用 Gemma 4 12B QAT MTP 达到 120 tok/s](#item-10) ⭐️ 8.0/10
11. [KVarN KV 缓存量化以更低内存实现更高比特精度](#item-11) ⭐️ 8.0/10
12. [为 NVIDIA DVLT 3D Transformer 定制的 CUDA/C++推理引擎](#item-12) ⭐️ 8.0/10
13. [llama.cpp 的 WIP PR 支持 DeepSeek V4 Flash，前景可期](#item-13) ⭐️ 8.0/10
14. [MoQ 与 GSQ：提升低比特 GGUF 量化效果](#item-14) ⭐️ 8.0/10
15. [Gemma 4 QAT 在 Strix Halo APU 上的基准测试](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [全国首例侵入式脑机接口让失明 20 年患者重见光明](https://www.ithome.com/0/960/883.htm) ⭐️ 9.0/10

中南大学湘雅医院成功为一名因视网膜色素变性失明 20 年的 61 岁患者植入 IMIE 智能视网膜系统，使其恢复至 0.03 视力，能够辨物和穿行房门。 这标志着中国在侵入式脑机接口视觉重建领域的首次临床突破，采用 256 通道柔性电极阵列，通道数是国外同类产品的四倍以上，展示了神经工程和医疗科技的重大进展。 IMIE 系统通过外部摄像头捕捉画面，经算法处理转换成电信号，直接刺激视神经，绕过坏死的感光细胞。患者目前仍需持续接受康复训练以提升视觉感知能力。

telegram · zaihuapd · 6月6日 07:30

**背景**: 侵入式脑机接口（BCI）通过手术将电极植入大脑或神经系统，直接与神经回路交互。IMIE（智能视网膜植入器）系统是一种视网膜假体，通过电刺激视神经重建视觉。本次试验使用的 256 通道柔性电极阵列更薄、生物相容性更高，可实现更高分辨率的刺激。清华大学等机构也在开发厚度仅 9 微米的全有机超柔性电极阵列，推动该领域发展。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ithome.com/0/960/883.htm">全国首例：侵入式脑机接口让失明 20 年患者重见光明 - IT之家</a></li>
<li><a href="https://sputniknews.cn/20260606/1071733984.html">中国首例！ 盲人凭脑机接口复明成功 - 2026年6月6日, 俄罗斯卫星通讯社</a></li>
<li><a href="https://www.tsinghua.edu.cn/info/1182/126137.htm">厚度仅9微米！清华打造脑机接口超柔性“神经纽带”-清华大学</a></li>

</ul>
</details>

**标签**: `#脑机接口`, `#医疗科技`, `#神经工程`, `#生物医学工程`, `#侵入式BCI`

---

<a id="item-2"></a>
## [Meta 确认 AI 聊天机器人漏洞导致 Instagram 账户被黑](https://this.weekinsecurity.com/meta-confirms-thousands-of-instagram-accounts-were-hacked-by-abusing-its-ai-chatbot/) ⭐️ 8.0/10

Meta 证实，攻击者利用其 AI 聊天机器人在账户恢复流程中的一个漏洞，绕过了电子邮件验证，劫持了数千个 Instagram 账户，该攻击从 4 月 17 日左右开始，持续了数周。 此事件凸显了 AI 驱动的客户支持和账户恢复系统中的关键安全风险，影响了超过 2 万名用户，并可能削弱用户对 Meta 平台安全的信任。 黑客获得了被劫持账户的完全控制权，包括访问私信、帖子和关联账户。Meta 通知了至少 20,225 名受影响的用户，该漏洞从 4 月 17 日一直存在直到被修复。

hackernews · speckx · 6月6日 18:35 · [社区讨论](https://news.ycombinator.com/item?id=48427643)

**背景**: 像 Meta 这样的公司越来越多地使用 AI 聊天机器人来自动化账户恢复，以简化用户支持。然而，此事件表明，当身份验证机制存在缺陷时，这些 AI 系统可能被操纵以绕过安全检查，从而实现未经授权的账户劫持。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cybersecuritynews.com/instagram-meta-ai-vulnerability/">Instagram Meta AI Vulnerability Allegedly Enables Password ...</a></li>
<li><a href="https://blog.checkpoint.com/ai-security/the-meta-ai-account-recovery-incident-wasnt-just-a-chatbot-problem/">The Meta AI Account Recovery Incident Wasn’t Just a Chatbot ...</a></li>

</ul>
</details>

**社区讨论**: 评论者批评 Meta 称该工具“正常工作”的说法，认为该漏洞代表了严重的安全失败。一些人对 Meta 的自动化系统表示沮丧，而另一些人则希望这一事件加速 Meta 平台的衰落。

**标签**: `#security`, `#Instagram`, `#AI chatbot`, `#account hijacking`, `#Meta`

---

<a id="item-3"></a>
## [超越 fork()+exec()：Unix 进程创建模型的再思考](https://lwn.net/SubscriberLink/1076018/16f01bbbb8e0d1f0/) ⭐️ 8.0/10

这篇文章讨论了 Unix 的 fork()+exec()进程创建模型的历史原因，并指出该模型如今已过时，提出了如 posix_spawn 和 vfork 等替代方案。 这很重要，因为 fork()+exec()是操作系统的基本原语；重新思考它可能会简化系统编程并提高性能，影响许多应用和开发者。 关键细节包括 fork()即使有写时复制也存在开销，而 posix_spawn 提供了组合的进程创建和执行调用，避免了不必要的复制。

hackernews · jwilk · 6月6日 14:34 · [社区讨论](https://news.ycombinator.com/item?id=48425528)

**背景**: 在 Unix 中，fork()创建一个几乎是父进程精确副本的子进程，而 exec()则用新程序替换子进程的内存。这种两步过程在当时很优雅，但会产生开销。诸如 vfork()（暂停父进程）和 posix_spawn()（组合调用）等替代方案存在但较少使用。争论在于这种优雅是否值得性能成本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.man7.org/linux/man-pages/man3/posix_spawn.3.html">posix_spawn(3) - Linux manual page</a></li>
<li><a href="https://en.wikipedia.org/wiki/Fork_(system_call)">Fork (system call) - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 评论展示了两种观点：一些人认为 fork()+exec()优雅且可扩展，而另一些人则对其复杂性和性能问题表示遗憾，并引用个人遇到的 bug。有评论提到微软研究院的论文《A fork() in the road》，对 fork 提出了批评。

**标签**: `#systems programming`, `#unix`, `#process creation`, `#fork`, `#exec`

---

<a id="item-4"></a>
## [Zeroserve：基于 eBPF 脚本的零配置 Web 服务器](https://su3.io/posts/introducing-zeroserve) ⭐️ 8.0/10

Zeroserve 被介绍为一款零配置 Web 服务器，它使用 eBPF 进行脚本编写，为 nginx 和 Caddy 等传统服务器提供了一种替代方案。该服务器用 Rust 构建，允许用户用 C 语言编写 eBPF 程序来处理 HTTP 请求。 这种方法将 Web 服务器配置从声明式语言转变为可编程的 eBPF，实现了高性能、灵活的请求处理。它可能简化部署，并为低延迟 Web 服务开辟新的可能性，尽管学习曲线可能更陡峭。 Zeroserve 是单线程的，专注于静态文件服务，社区建议探索通过 SO_REUSEPORT 实现多线程，以及与 XDP 等其他 eBPF 程序类型的集成。该项目的设计重点在于配置范式，而非仅仅性能。

hackernews · losfair · 6月6日 14:59 · [社区讨论](https://news.ycombinator.com/item?id=48425723)

**背景**: eBPF（扩展的伯克利包过滤器）是一种 Linux 内核技术，允许在内核空间运行沙箱程序，传统上用于网络、可观测性和安全。像 nginx 和 Caddy 这样的 Web 服务器使用声明式配置文件，而 Zeroserve 使用 eBPF 程序（用 C 编写）来定义请求处理逻辑，可能允许直接的内核交互以提升性能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/EBPF">eBPF - Wikipedia</a></li>
<li><a href="https://ebpf.io/what-is-ebpf/">What is eBPF? An Introduction and Deep Dive into the eBPF ...</a></li>

</ul>
</details>

**社区讨论**: 评论者对这一概念表示兴趣，部分人指出未能提供基于 Rust 的 eBPF 脚本接口是个遗憾。其他人则强调了 nginx 的出色性能，并质疑在当今趋势下专注于静态文件的做法。还有关于使用 eBPF 实现内核加速 Web 服务的潜在讨论，尽管当前实现是用户态的。

**标签**: `#eBPF`, `#web server`, `#zero-config`, `#Rust`, `#networking`

---

<a id="item-5"></a>
## [英伟达为 Windows PC 提出高性能 CPU 方案](https://twitter.com/lemire/status/2062880075117113739) ⭐️ 8.0/10

英伟达为 Windows PC 提出了一种强大的 CPU 系统，采用统一内存架构，可能将高性能 Arm 核心与其 GPU 技术集成，用于本地 AI 工作负载。 该提案可能重新定义 PC 架构，将统一内存引入 Windows，类似于 Apple Silicon，实现更高效的本地 AI 处理，并可能挑战英特尔和 AMD 在 CPU 市场的地位。 该系统据称在 CPU 和 GPU 之间共享统一内存池，类似于英伟达用于数据中心的 Grace CPU，但针对消费级 Windows PC 进行了优化，专注于本地 AI 推理。

hackernews · tosh · 6月6日 12:52 · [社区讨论](https://news.ycombinator.com/item?id=48424605)

**背景**: 统一内存架构允许 CPU 和 GPU 访问同一内存池，无需复制数据，从而降低延迟并简化编程。英伟达此前为服务器开发了基于 Arm 的 Grace CPU，该提案将类似技术应用于消费级 PC，以实现无缝的本地 AI 执行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Unified_memory_architecture">Unified memory architecture</a></li>
<li><a href="https://grokipedia.com/page/Nvidia_Grace">Nvidia Grace</a></li>
<li><a href="https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/unified-memory.html">4.1. Unified Memory — CUDA Programming Guide</a></li>

</ul>
</details>

**社区讨论**: 评论者讨论了统一内存在游戏和 AI 方面的优势，有人质疑性能声明，并与现有解决方案如 AMD Ryzen AI Max 和高通骁龙 X2 进行比较。其他人则对普通消费者本地 AI 的有限吸引力表示怀疑。

**标签**: `#Nvidia`, `#CPU`, `#Windows`, `#AI`, `#Unified Memory`

---

<a id="item-6"></a>
## [HN 用户质疑社区的反 AI 情绪](https://news.ycombinator.com/item?id=48420827) ⭐️ 8.0/10

一位 Hacker News 用户质疑该平台上明显的反 AI 情绪，引发了超过 600 条评论的讨论，包括版主 dang 指出社区对 AI 存在分歧。 这场讨论凸显了软件开发行业中 AI 辅助与传统编码之间的持续紧张关系，影响着工具采纳以及影响力科技论坛的社区动态。 原帖作者认为代码只是达成目的的手段，AI 辅助版本可以更快交付；评论从对失业的恐惧到对专有非确定性数据库的担忧。

hackernews · Ekami · 6月6日 02:31

**背景**: 像 Claude Code 和 GitHub Copilot 这样的 AI 编程助手使用大型语言模型从自然语言提示生成代码。它们引发了关于代码质量、开发者生产力以及软件工程未来的辩论。Hacker News 作为一个以技术为中心的社会新闻网站，经常就此类话题展开两极分化的讨论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>

</ul>
</details>

**社区讨论**: 评论揭示了一个分裂的社区：一些人支持 AI 加速开发，而另一些人则重视编程技艺并担心 AI 威胁其生计。反对者还提出对专有锁定和非确定性输出的担忧。版主 dang 指出 HN 并非一致反 AI，而是双方都感知到偏见。

**标签**: `#AI`, `#software engineering`, `#Hacker News`, `#meta`, `#community`

---

<a id="item-7"></a>
## [MicroPython 编译为 WebAssembly 实现 Python 沙箱](https://simonwillison.net/2026/Jun/6/micropython-in-a-sandbox/#atom-everything) ⭐️ 8.0/10

Simon Willison 发布了名为 micropython-wasm 的 alpha 软件包，它将 MicroPython 编译为 WebAssembly，从而能够在 Datasette 等 Python 应用内安全地运行 Python 代码。他还为 Datasette Agent 创建了一个插件 datasette-agent-micropython 来利用此沙箱。 这为安全执行不受信任的 Python 代码提供了实用的解决方案，解决了插件系统和应用程序长期面临的挑战。通过利用 WebAssembly 的沙箱特性，它可以强制执行内存和 CPU 限制，适用于 AI 代理等场景。 该软件包使用 Emscripten 编译 MicroPython，生成在隔离环境中运行的 WebAssembly 模块，阻止访问主机文件系统、网络或其他资源。目前为 alpha 软件，不建议用于生产环境。

rss · Simon Willison · 6月6日 03:53

**背景**: MicroPython 是 Python 3 的精简实现，针对微控制器进行了优化，但也能在其他平台上运行。WebAssembly (WASM) 是一种二进制指令格式，在具有内置沙箱功能的虚拟机中执行。将两者结合可以在有资源限制的隔离环境中运行 Python。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/MicroPython">MicroPython</a></li>
<li><a href="https://micropython.org/">MicroPython - Python for microcontrollers</a></li>
<li><a href="https://agent.datasette.io/">Datasette Agent: an AI assistant for Datasette to help ...</a></li>

</ul>
</details>

**标签**: `#sandbox`, `#micropython`, `#webassembly`, `#python`, `#security`

---

<a id="item-8"></a>
## [Cohere 提供未发布编码模型早期访问，采用高效架构](https://www.reddit.com/r/LocalLLaMA/comments/1tylzy2/coheres_unreleased_coding_model_early_access_for/) ⭐️ 8.0/10

Cohere 发布了其首个编码模型的早期访问版本，该模型拥有 300 亿参数但仅 30 亿活跃参数，在官方发布前于 Hugging Face 上供社区测试。 这标志着 Cohere 进入编码模型领域，并通过稀疏激活技术展示了对本地部署效率的关注，可能为开发者友好的 AI 工具树立新标准。 该模型总参数 300 亿但仅 30 亿活跃，暗示采用混合专家（MoE）架构，可在消费级硬件上实现快速推理。Cohere 正在寻求社区反馈以在公开发布前改进模型。

reddit · r/LocalLLaMA · /u/nick_frosst · 6月6日 16:36

**背景**: 在 AI 模型中，参数是训练过程中学习的内部权重，决定输出。混合专家（MoE）架构使用多个专门的子网络（专家）和一个门控机制，仅对每个输入激活部分专家，从而大幅降低计算成本。例如，一个 300 亿参数的 MoE 模型只有 30 亿活跃参数，可在单 GPU 上运行，使本地部署成为可能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained - Hugging Face</a></li>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>

</ul>
</details>

**标签**: `#Cohere`, `#coding model`, `#local LLM`, `#early access`, `#AI`

---

<a id="item-9"></a>
## [PewDiePie 的 Odysseus AI 工具发现一键管理员接管漏洞](https://www.reddit.com/r/LocalLLaMA/comments/1tys1wj/another_1click_admin_account_takeover_in/) ⭐️ 8.0/10

一名安全研究人员披露了 PewDiePie 自托管 AI 工具 Odysseus 中存在的一键管理员账户接管漏洞，攻击者可凭一次点击获得完全管理员权限。 该漏洞至关重要，因为 Odysseus 被宣传为私密的自托管 AI 工作区，而完全的管理员接管会损害用户信任和数据安全。此类漏洞反复出现表明，流行 AI 工具需要更严格的安全审计。 该漏洞允许无需用户交互的一键管理员接管，类似于近期 ZITADEL 和 Microsoft 365 Android 应用中的一键账户接管问题。披露时尚未确认有补丁。

reddit · r/LocalLLaMA · /u/theonejvo · 6月6日 20:32

**背景**: PewDiePie 发布了 Odysseus，一个用于本地运行开源模型的自托管 AI 工作区，强调隐私和用户控制。该工具基于现有的 Web UI（如 Claude 和 ChatGPT 的界面）构建，但可自托管。一键管理员接管漏洞是一个严重的安全问题，可能暴露所有用户数据并允许完全系统控制。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.tomshardware.com/tech-industry/artificial-intelligence/pewdiepie-goes-all-in-on-self-hosting-ai-using-modded-gpus-with-plans-to-build-own-model-soon-youtuber-pits-multiple-sentient-chatbots-against-each-other-to-find-the-best-answers">PewDiePie goes all-in on self-hosting AI using... | Tom's Hardware</a></li>
<li><a href="https://80.lv/articles/pewdiepie-releases-his-own-self-hosted-ai-workspace-available-for-free">PewDiePie Releases His Own Self-Hosted AI Workspace for Free</a></li>

</ul>
</details>

**标签**: `#security`, `#vulnerability`, `#AI`, `#LLM`, `#PewDiePie`

---

<a id="item-10"></a>
## [在 12GB 显存上用 Gemma 4 12B QAT MTP 达到 120 tok/s](https://www.reddit.com/r/LocalLLaMA/comments/1typjmc/120_toks_on_12gb_vram_with_gemma_4_12b_qat_mtp/) ⭐️ 8.0/10

一位用户通过使用经过修补的 llama.cpp，在配备 12GB 显存的 NVIDIA RTX 4070 Super GPU 上，利用 Gemma 4 12B QAT（量化感知训练）模型结合多令牌预测（MTP）推测解码，实现了每秒 120 个 token 的推理速度。 这展示了在消费级硬件上运行大型语言模型的显著突破，使得在中端 GPU（12GB 显存）上实现高速推理成为可能，且不牺牲质量，这可能会加速本地 LLM 的普及。 该方案使用了 Unsloth 的 Gemma 4 12B QAT 的 4 位量化 GGUF 模型和一个单独的 Q8_0 量化草稿模型进行 MTP，相比非 MTP 推理（约 60 tok/s）实现了约 2 倍加速（达到约 120 tok/s）。但需要将 GPU 设置为副显卡以释放显存，Windows 用户可能因驱动开销损失约 500MB 以上显存。

reddit · r/LocalLLaMA · /u/janvitos · 6月6日 18:53

**背景**: 量化感知训练（QAT）将量化过程整合到训练中，使模型能够适应低精度推理，从而在激进的量化后仍保持准确性。多令牌预测（MTP）是一种推测解码技术，其中轻量级草稿头并行预测多个后续令牌，主模型验证它们，从而增加吞吐量。Gemma 4 是谷歌最新的开源模型系列，QAT 变体专门为高效推理而设计。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ibm.com/think/topics/quantization-aware-training">What is Quantization Aware Training ? | IBM</a></li>
<li><a href="https://docs.llamatik.com/guides/multi-token-prediction/">Multi - Token Prediction ( MTP ) • Llamatik Documentation</a></li>

</ul>
</details>

**标签**: `#LLM`, `#quantization`, `#inference speed`, `#Gemma 4`, `#speculative decoding`

---

<a id="item-11"></a>
## [KVarN KV 缓存量化以更低内存实现更高比特精度](https://www.reddit.com/r/LocalLLaMA/comments/1tyockn/kv_cache_quant_benchmarks_kvarn_6bit_matches_q8_0/) ⭐️ 8.0/10

KVarN 量化基准测试表明，6 位 KVarN 的精度与 q8_0 相当，4 位 KVarN 的精度与 q5_0 相当，从而在 LLM 推理中实现显著的内存节省而不损失质量。 这一突破使得 VRAM 受限的用户能够运行更大的上下文或模型，因为 KVarN 在相同内存成本下提供高一个比特的精度，有望在消费级硬件上普及长上下文 LLM 推理。 基准测试在 Qwen 3.6 27B 模型上使用 64k 上下文，基于 llama.cpp 的一个分支（BeeLlama）进行。目前提示处理速度较慢，但预计该方法可进一步优化。

reddit · r/LocalLLaMA · /u/Anbeeld · 6月6日 18:06

**背景**: KV 缓存量化通过以较低精度存储键和值来减少内存使用。标准格式如 q8_0 使用 8 位，而 KVarN 利用方差归一化和 Hadamard 旋转在较低位宽下保持高质量。该研究来自华为，并已在 vLLM 中实现。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/huawei-csl/KVarN">GitHub - huawei-csl/KVarN: KVarN is a native vLLM KV-cache ...</a></li>
<li><a href="https://arxiv.org/pdf/2606.03458">KVarN: Variance-Normalized KV-Cache Quantization Mitigates ...</a></li>
<li><a href="https://insiderllm.com/guides/llm-quantization-explained/">Quantization Explained: What It Means for Local AI | InsiderLLM</a></li>

</ul>
</details>

**标签**: `#KV cache`, `#quantization`, `#LLM inference`, `#KVarN`, `#llama.cpp`

---

<a id="item-12"></a>
## [为 NVIDIA DVLT 3D Transformer 定制的 CUDA/C++推理引擎](https://www.reddit.com/r/LocalLLaMA/comments/1tyu79c/dvltcu_inference_engine_written_from_scratch_in/) ⭐️ 8.0/10

一位开发者发布了 dvlt.cu，这是一个针对 NVIDIA Déjà View（DVLT）3D Transformer 模型的轻量级推理引擎，完全用 CUDA/C++实现，单个 5MB 二进制文件，仅依赖 cuBLASLt 和 CUTLASS 中的 CuTe 头文件库。 这表明一个大型复杂的 Transformer 模型可以用一个微小无依赖的二进制文件提供服务，可能实现在边缘设备或资源受限环境中高效进行 3D 重建，无需 Python 或深度学习框架的开销。 该引擎使用 mmap 的 bf16 权重、批量 GPU 上传、静态维度以及一次性 arena 进行确定性内存分配；权重（1.17 亿参数）是 NVIDIA 的非商业发布版，需单独下载。

reddit · r/LocalLLaMA · /u/yassa9 · 6月6日 22:04

**背景**: Déjà View (DVLT)是一种用于多视图 3D 重建的循环 Transformer，它循环共享注意力块并带有离散深度索引，能从无序图像输出逐像素射线、深度、置信度和相机位姿。仅 1.17 亿参数，却能媲美更大模型。cuTLASS（CUTLASS）是 NVIDIA 的 CUDA 模板库，用于高性能矩阵运算，其 CuTe 组件提供了张量抽象。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/nv-tlabs/dvlt">GitHub - nv-tlabs/dvlt: Official implementation of Déjà View ...</a></li>
<li><a href="https://github.com/NVIDIA/cutlass">GitHub - NVIDIA/cutlass: CUDA Templates and Python DSLs for ...</a></li>

</ul>
</details>

**标签**: `#CUDA`, `#inference engine`, `#3D reconstruction`, `#transformer`, `#HPC`

---

<a id="item-13"></a>
## [llama.cpp 的 WIP PR 支持 DeepSeek V4 Flash，前景可期](https://www.reddit.com/r/LocalLLaMA/comments/1tyb3np/deepseek_v4_flash_is_amazing_wip_llamacpp_pr_24162/) ⭐️ 8.0/10

一个尚在开发中的拉取请求（#24162）为 llama.cpp 增加了对 DeepSeek V4 Flash 的支持，允许通过自定义量化进行本地推理。 DeepSeek V4 Flash 是一个拥有 284B 参数的 MoE 模型，在本地规模下提供前沿水平的智能，而此 PR 将其引入开源 llama.cpp 生态系统，可能主导 80-140GB 模型空间。 该 PR 处于早期阶段，推理速度慢（5-6 tps），GPU 和 Flash Attention 支持不完整，但模型原生的 FP4-FP8 混合量化使其比竞品更能容忍激进的量化，且 MoE 架构每个 token 仅激活 13B 参数。

reddit · r/LocalLLaMA · /u/Lowkey_LokiSN · 6月6日 07:56

**背景**: DeepSeek V4 Flash 是一个混合专家（MoE）模型，总参数 284B，但每个输入仅激活 13B 参数，支持 1M token 的上下文窗口。它采用 FP4-FP8 混合量化方案，在减少内存占用的同时保持质量。llama.cpp 是一个流行的开源库，用于在消费级硬件上本地运行 LLM。量化，如帖子中提到的自定义 3 位版本，可压缩模型以适配可用显存。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash">deepseek -ai/ DeepSeek - V 4 - Flash · Hugging Face</a></li>
<li><a href="https://build.nvidia.com/deepseek-ai/deepseek-v4-flash">deepseek - v 4 - flash Model by Deepseek -ai | NVIDIA NIM</a></li>
<li><a href="https://openrouter.ai/deepseek/deepseek-v4-flash:free">DeepSeek V 4 Flash - API Pricing & Benchmarks | OpenRouter</a></li>

</ul>
</details>

**标签**: `#deepseek`, `#llama.cpp`, `#local-llm`, `#quantization`, `#open-source`

---

<a id="item-14"></a>
## [MoQ 与 GSQ：提升低比特 GGUF 量化效果](https://www.reddit.com/r/LocalLLaMA/comments/1tyjkfh/moq_ggufs_and_gsq_lowbit_ggufs_are_about_to_get/) ⭐️ 8.0/10

两种新的量化方法 MoQ（混合量化）和 GSQ（Gumbel-Softmax 量化）将显著提升低比特 GGUF 模型的性能，从而实现更高效的本地大语言模型部署。 这一进展可以在不牺牲精度的前提下降低对内存和计算资源的需求，使高质量大语言模型在消费级硬件上更易用，惠及本地 LLM 社区和边缘部署场景。 MoQ 在量化感知训练中安排多种数据精度，而 GSQ 是一种标量训练后量化方法，能在 2 比特下对万亿参数模型实现接近无损的压缩。两者均设计为与现有推理框架兼容。

reddit · r/LocalLLaMA · /u/beneath_steel_sky · 6月6日 15:01

**背景**: GGUF 是一种用于存储机器学习模型的二进制文件格式，针对 GGML 快速加载和推理进行了优化。量化通过降低模型精度（例如从 16 比特降至 4 比特或 2 比特）来减少内存使用并加速计算，这对在资源有限的设备上部署大语言模型至关重要。MoQ 和 GSQ 代表了在此压缩过程中最小化精度损失的最先进技术。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GGUF">GGUF - Wikipedia</a></li>
<li><a href="https://www.deepspeed.ai/tutorials/MoQ-tutorial/">DeepSpeed Mixture-of- Quantization ( MoQ ) - DeepSpeed</a></li>
<li><a href="https://arxiv.org/html/2604.18556">GSQ : Highly-Accurate Low-Precision Scalar Quantization for LLMs via...</a></li>

</ul>
</details>

**标签**: `#quantization`, `#GGUF`, `#LLM`, `#inference optimization`, `#local deployment`

---

<a id="item-15"></a>
## [Gemma 4 QAT 在 Strix Halo APU 上的基准测试](https://www.reddit.com/r/LocalLLaMA/comments/1tyilv7/gemma_4_qat_q4_0_bench_on_strix_halo/) ⭐️ 8.0/10

一位用户在 AMD Strix Halo APU（Ryzen AI Max+ 395）上，使用 llama.cpp 的 Vulkan 后端对 Google 官方的 Gemma 4 QAT Q4_0 GGUF 模型进行了基准测试，包括多令牌预测（MTP）辅助头。26B-A4B QAT 模型实现了高达 71.4 tokens/s 的解码速度，草案接受率为 91.8%。 这一基准测试展示了量化感知训练（QAT）在尖端消费级 APU 上对大型语言模型的实际性能，表明使用 Gemma 4 等模型进行高质量本地推理是可行的。结果有助于用户了解本地 LLM 部署中模型大小、量化和推理速度之间的权衡。 测试系统使用 128 GB 统一 LPDDR5X 内存、Linux Mint（内核 6.17）和 Mesa 25.2.8。26B-A4B QAT 模型配合 QAT 匹配的 MTP 和 Q8 KV 缓存实现了 71.4 tok/s 的解码速度，而未使用 MTP 的普通 Vulkan 达到 59 tok/s。12B 和 31B 模型性能较低，31B 仅约 19 tok/s。

reddit · r/LocalLLaMA · /u/westsunset · 6月6日 14:22

**背景**: GGUF 是一种用于高效存储和推理大型语言模型的文件格式，由 llama.cpp 项目创建。Strix Halo 是 AMD 的高性能 APU，结合了 Zen 5 核心和大型 RDNA 3.5 集成显卡。量化感知训练（QAT）在训练过程中模拟低精度运算，以减少相比训练后量化的精度损失。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ggufloader.github.io/what-is-gguf.html">What is GGUF? Complete Guide to GGUF Format & Quantization</a></li>
<li><a href="https://d33gy59ovltp76.cloudfront.net/news/amd-s-game-changing-strix-halo-apu-formally-known-as-the-ryzen-ai-max-poses-for-new-die-shots-and-gets-annotated">AMD's game-changing Strix Halo APU , formally known as</a></li>
<li><a href="https://www.ibm.com/think/topics/quantization-aware-training">What is quantization aware training? - IBM</a></li>

</ul>
</details>

**标签**: `#Gemma 4`, `#QAT`, `#Quantization`, `#Local LLM`, `#Strix Halo`

---