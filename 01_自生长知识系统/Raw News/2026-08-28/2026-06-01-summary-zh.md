---
layout: default
title: "Horizon Summary: 2026-06-01 (ZH)"
date: 2026-06-01
lang: zh
---

> 从 44 条内容中筛选出 9 条重要资讯。

---

1. [Cloudflare Turnstile 利用 WebGL 指纹识别破坏隐私](#item-1) ⭐️ 8.0/10
2. [1 比特 Bonsai Image 4B：高效本地图像生成](#item-2) ⭐️ 8.0/10
3. [VideoLAN 发布开源 AV2 解码器 Dav2d](#item-3) ⭐️ 8.0/10
4. [Linux 重启序列详解](#item-4) ⭐️ 8.0/10
5. [Deflock 在美国绘制了 10 万个车牌读取器](#item-5) ⭐️ 8.0/10
6. [NVIDIA Parakeet 移植到 ggml：更快、量化、无需 Python](#item-6) ⭐️ 8.0/10
7. [去除安全对齐的 Gemma 4 E2B 变体基准测试](#item-7) ⭐️ 8.0/10
8. [FROST 攻击利用 SSD 定时窥探用户活动](#item-8) ⭐️ 8.0/10
9. [AV2 参考编码器发布首个 1.0.0 版本](#item-9) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Cloudflare Turnstile 利用 WebGL 指纹识别破坏隐私](https://hacktivis.me/articles/cloudflare-turnstile-webgl-fingerprinting) ⭐️ 8.0/10

Cloudflare Turnstile 现在要求使用 WebGL 进行指纹识别，这实际上绕过了 Firefox 等浏览器的隐私保护措施，并导致不支持 WebGL 的小众浏览器无法访问。 这种做法通过未经同意的持久追踪侵犯用户隐私，并且对小众或注重隐私的浏览器用户造成不成比例的影响，导致网络碎片化。 该问题由一位小众浏览器维护者报告，他注意到几周前用户开始遇到 Cloudflare 的挑战。WebGL 指纹识别利用硬件和驱动程序细节生成唯一标识符。

hackernews · HypnoticOcelot · 5月31日 14:13 · [社区讨论](https://news.ycombinator.com/item?id=48345840)

**背景**: 浏览器指纹识别通过收集设备信息（操作系统、浏览器类型、屏幕分辨率等）生成唯一标识符，常用于无 Cookie 追踪。WebGL 指纹识别专门利用显卡的差异性，即使相同的设备也可能不同。Cloudflare Turnstile 是一种 CAPTCHA 替代方案，旨在无需手动拼图即可验证人类用户，但它对 WebGL 的依赖损害了非标准浏览器的隐私。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Cloudflare_Turnstile">Cloudflare Turnstile</a></li>
<li><a href="https://browserleaks.com/webgl">WebGL Browser Report - WebGL Fingerprinting - BrowserLeaks</a></li>
<li><a href="https://en.wikipedia.org/wiki/Browser_fingerprinting">Browser fingerprinting</a></li>

</ul>
</details>

**社区讨论**: 评论者表达了对机器人检测与规避之间军备竞赛的担忧，有人指出指纹识别很常见，尽管生态代价高昂。还有人批评 Mozilla 未默认启用 resistFingerprinting，而小众浏览器维护者报告了真实用户影响。

**标签**: `#privacy`, `#fingerprinting`, `#Cloudflare`, `#WebGL`, `#browser`

---

<a id="item-2"></a>
## [1 比特 Bonsai Image 4B：高效本地图像生成](https://prismml.com/news/bonsai-image-4b) ⭐️ 8.0/10

PrismML 发布了 Bonsai Image 4B，这是一个使用 1 比特权重量化的 40 亿参数扩散 Transformer，内存占用减少高达 8.3 倍，可在 iPhone 上本地生成图像。 这标志着向高质量图像生成民主化迈出的重要一步，使其无需昂贵云订阅即可在消费设备上运行。用户现在可以本地运行复杂模型，保护隐私并支持离线使用。 Bonsai Image 4B 基于 FLUX.2 Klein 4B，并提供 1 比特和三进制变体。虽然它保持了较强的视觉质量，但一些社区成员指出其速度略慢于原始小型 FLUX.2 模型。

hackernews · modinfo · 5月31日 15:04 · [社区讨论](https://news.ycombinator.com/item?id=48346257)

**背景**: 1 比特量化是一种将每个模型权重仅用单个比特（或少量比特）表示的技术，大幅降低内存和计算需求。扩散模型是一类通过迭代去噪随机噪声生成图像的生成模型，通常需要大量 GPU 内存。通过应用极端量化，像 Bonsai Image 4B 这样的模型可以在资源有限的设备（如智能手机）上运行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://prismml.com/news/bonsai-image-4b">PrismML — Introducing 1-bit and Ternary Bonsai Image 4B: Image Generation for Local Devices</a></li>
<li><a href="https://www.prnewswire.com/news-releases/prismml-releases-bonsai-image-4b-302782354.html">PrismML Releases Bonsai Image 4B</a></li>
<li><a href="https://gigazine.net/gsc_news/en/20260527-bonsai-image-4b-image-generation-ai/">I tried out 'Bonsai Image 4B,' an image generation AI that runs locally on iPhones, and modified FLUX.2 Klein 4B into a 1-bit version, reducing memory usage to 1/8.3 of the original. - GIGAZINE</a></li>

</ul>
</details>

**社区讨论**: 社区评论褒贬不一：部分用户对本地硬件升级作为订阅替代方案表示兴奋，而另一些用户质疑内存是否是真正瓶颈，因为生成时间仍然较慢。有用户指出，Bonsai Image 4B 并非第一个在 iPhone 上运行的模型，因为 FLUX.2 本身已通过应用程序以 8 位或 6 位量化运行。

**标签**: `#1-bit`, `#image generation`, `#model compression`, `#local AI`, `#diffusion models`

---

<a id="item-3"></a>
## [VideoLAN 发布开源 AV2 解码器 Dav2d](https://jbkempf.com/blog/2026/dav2d/) ⭐️ 8.0/10

VideoLAN 发布了 dav2d，这是 AV2 视频编码标准的开源解码器，标志着该标准的首个主要独立实现。 AV2 承诺比 AV1 减少 25-30% 的码率，但解码复杂度提高了约五倍，因此高效的软件解码器对普及至关重要。Dav2d 提供了一个生产就绪的跨平台解码器，有助于硬件和软件生态系统为 AV2 做好准备。 Dav2d 解码器由 libavcodec 背后的同一团队开发，注重速度与正确性。它是跨平台的，并旨在为未来的硬件实现提供参考。

hackernews · captain_bender · 5月31日 11:44 · [社区讨论](https://news.ycombinator.com/item?id=48344961)

**背景**: AV2 是开放媒体联盟（AOMedia）推出的下一代开放、免版税视频编码格式，是 AV1 的继任者。它于 2026 年 5 月正式发布，压缩效率比 AV1 提高约 30%，但计算复杂度显著增加。VideoLAN 以开发 VLC 媒体播放器而闻名，并曾为 AV1 创建了高效的 dav1d 解码器。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.phoronix.com/news/Dav2d-Open-Source-AV2-Decode">VideoLAN Publishes Dav2d For Open-Source AV2 Decoder - Phoronix</a></li>
<li><a href="https://en.wikipedia.org/wiki/AV2_(video_coding_format)">AV2 (video coding format)</a></li>

</ul>
</details>

**社区讨论**: 社区评论担心 AV2 的解码复杂度约为 AV1 的五倍，可能使现有的 AV1 硬件解码器过时。一些人质疑 25% 的大小减少是否值得更换硬件，但也有人指出，经过优化后，软件解码可能足以满足许多用例。

**标签**: `#video codec`, `#AV2`, `#decoder`, `#performance`, `#open source`

---

<a id="item-4"></a>
## [Linux 重启序列详解](https://justine.lol/rseq/) ⭐️ 8.0/10

一篇文章深入技术性地解释了 Linux 重启序列（rseq），这是一个内核特性，允许在没有互斥锁或原子操作的情况下实现无锁数据结构。 该特性可以通过消除传统同步机制的开销，显著提升多线程应用的性能，有利于处理高并发代码的系统程序员。 重启序列的工作方式是让程序标记临界区；如果内核在该区域内抢占线程，则从开头重新启动该序列。librseq 库为常见用例提供了辅助函数，因此用户通常不需要编写汇编代码。

hackernews · grappler · 5月31日 14:38 · [社区讨论](https://news.ycombinator.com/item?id=48346019)

**背景**: 重启序列（rseq）是一种 Linux 内核机制，允许用户空间代码在不进行系统调用的情况下原子地执行每 CPU 操作。它们于 Linux 内核 4.18 中加入，用于高效实现引用计数、每 CPU 计数器和其他无锁数据结构。内核检测临界区内的抢占或迁移，并重新启动序列，从而无需传统锁即可确保正确性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://lwn.net/Articles/1033957/">The rseq() manual page [LWN.net]</a></li>
<li><a href="https://lwn.net/Articles/697539/">Kernel development [LWN.net]</a></li>

</ul>
</details>

**社区讨论**: 社区情绪总体积极，用户对在项目中使用 rseq 表示兴奋。然而，一些评论者批评了文章的语气以及缺少对 librseq 库的引用，指出该库提供了更易用的辅助函数，避免了汇编代码。

**标签**: `#linux`, `#kernel`, `#concurrency`, `#systems-programming`

---

<a id="item-5"></a>
## [Deflock 在美国绘制了 10 万个车牌读取器](https://deflock.org/) ⭐️ 8.0/10

开源项目 Deflock 宣布已在美国绘制了超过 10 万个自动车牌识别摄像头（ALPR）的位置。 这一里程碑凸显了监控基础设施的规模，并赋予社区挑战隐私侵犯的能力。它还引发了关于如何在安全摄像头的益处与个人隐私权之间取得平衡的辩论。 然而，一些社区成员指出，由于 OpenStreetMap 中的数据重复，实际数字可能被高估了几个百分点。此外，新地图界面需要 WebGL，给部分用户带来了可访问性问题。

hackernews · pilingual · 5月31日 17:04 · [社区讨论](https://news.ycombinator.com/item?id=48347370)

**背景**: 自动车牌识别摄像头（ALPR）是一种高速摄像头，可捕获车牌数据，常用于执法和私人公司。Deflock 是一个社区驱动的开源项目，通过绘制这些设备的位置来提高透明度和问责制。该项目使用 OpenStreetMap 数据并鼓励公众贡献。随着监控问题的日益增长，像 Deflock 这样的倡议帮助个人了解他们正在被监视的位置。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.forbes.com/sites/larsdaniel/2024/11/26/think-youre-not-being-watched-deflock-says-think-again/">Think You’re Not Being Watched? DeFlock Says Think Again</a></li>
<li><a href="https://www.404media.co/the-open-source-project-deflock-is-mapping-license-plate-surveillance-cameras-all-over-the-world/">The Open Source Project DeFlock Is Mapping License Plate ...</a></li>
<li><a href="https://sls.eff.org/technologies/automated-license-plate-readers-alprs">Automated License Plate Readers</a></li>

</ul>
</details>

**社区讨论**: 评论者表达了复杂的情绪：一些人支持对隐私侵犯的反击，而另一些人则对数据准确性（例如约 2500 个重复条目）和技术限制（如 WebGL 要求）提出担忧。少数人建议，像 Flock 这样的公司可以通过将摄像头放置在私人财产上来规避地图绘制，主张转而加强立法。

**标签**: `#privacy`, `#surveillance`, `#ALPR`, `#openstreetmap`, `#mapping`

---

<a id="item-6"></a>
## [NVIDIA Parakeet 移植到 ggml：更快、量化、无需 Python](https://www.reddit.com/r/LocalLLaMA/comments/1tt6oja/i_ported_nvidia_parakeet_speechtotext_to_ggml/) ⭐️ 8.0/10

一位开发者将 NVIDIA 的 Parakeet 语音识别模型移植到纯 C++/ggml 引擎，实现了与 NeMo 字节一致的输出，GPU 速度提升至 5 倍，量化后 CPU 速度提升 1.86 倍，并发布了 GGUF 量化版本用于高效的 CPU/GPU 推理。 这一成果使得高质量 NVIDIA 语音识别模型无需 Python 或 PyTorch 即可部署，推理更快、内存更少，且易于嵌入应用程序，有利于构建本地和边缘 ASR 系统的开发者。 移植版支持 FastConformer TDT/CTC/RNNT/混合模型，可在 CPU 和 GPU（CUDA、HIP、Vulkan、Metal）上运行，并包含带词级时间戳和置信度的缓存感知流式处理。GGUF 模型文件自包含，分词器已内嵌。

reddit · r/LocalLLaMA · /u/mudler_it · 5月31日 20:35

**背景**: ggml 是一个机器学习张量库，能在普通硬件上运行大模型，被 llama.cpp 和 whisper.cpp 使用。NVIDIA Parakeet 是基于 FastConformer 架构的一系列最先进 ASR 模型。GGUF 是一种量化格式，可减小模型大小并加速消费级硬件上的推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://ggml.ai/">ggml .ai</a></li>
<li><a href="https://developer.nvidia.com/blog/pushing-the-boundaries-of-speech-recognition-with-nemo-parakeet-asr-models/">Pushing the Boundaries of Speech Recognition with NVIDIA NeMo</a></li>
<li><a href="https://medium.com/@bnjmn_marie/gguf-quantization-for-fast-and-memory-efficient-inference-on-your-cpu-d10fbe58fbca">GGUF Quantization for Fast and Memory-Efficient Inference... | Medium</a></li>

</ul>
</details>

**标签**: `#speech-to-text`, `#ggml`, `#NVIDIA Parakeet`, `#model optimization`, `#open source`

---

<a id="item-7"></a>
## [去除安全对齐的 Gemma 4 E2B 变体基准测试](https://www.reddit.com/r/LocalLLaMA/comments/1tsvs3j/13_abliterated_gemma_4_e2b_variants_44_gpu_hours/) ⭐️ 8.0/10

一位 Reddit 用户发布了对 13 个去除安全对齐的 Google Gemma 4 E2B 模型变体的全面比较，使用 44 GPU 小时评估安全移除效果（HarmBench ASR）和 8 项基准性能，揭示了哪些方法保留了能力。 这项工作通过识别能够在不降低性能的情况下实现高攻击成功率的去除安全对齐技术，为 AI 安全社区提供了可操作的见解，并揭示了声称与实际的性能保留之间的差异，这对开源模型对齐至关重要。 最佳变体（coder3101）实现了 96% 的攻击成功率，甚至在 GSM8K 数学基准上超过了基础模型，而激进的方法会导致困惑度显著增加（高达 7.35 倍）和 token 浪费；此外，13 个模型中有 5 个因共享 KV 投影而丢失了 safetensor 键。

reddit · r/LocalLLaMA · /u/nathandreamfast · 5月31日 13:44

**背景**: 去除安全对齐是一种从大型语言模型中移除安全对齐的技术，通常通过消融或修改拒绝方向来实现。像 Heretic 这样的工具可以自动化这一过程。HarmBench 是一个标准化基准，用于评估针对有害提示的攻击成功率（ASR），衡量模型拒绝或遵从的频率。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/blog/mlabonne/abliteration">Uncensor any LLM with abliteration</a></li>
<li><a href="https://github.com/p-e-w/heretic">GitHub - p-e-w/heretic: Fully automatic censorship removal for</a></li>
<li><a href="https://arxiv.org/abs/2402.04249">[2402.04249] HarmBench: A Standardized Evaluation Framework for</a></li>

</ul>
</details>

**标签**: `#abliteration`, `#Gemma 4`, `#model safety`, `#benchmark`, `#alignment`

---

<a id="item-8"></a>
## [FROST 攻击利用 SSD 定时窥探用户活动](https://futurism.com/future-society/websites-spying-solid-state-drive) ⭐️ 8.0/10

研究人员披露了 FROST（基于 OPFS 的 SSD 定时远程指纹识别）攻击，恶意网站可通过浏览器的 Origin Private File System (OPFS) API 测量 SSD 读写时序，从而推断用户活动，无需任何用户交互。 这种侧信道攻击构成了重大隐私威胁，因为它仅使用标准浏览器 API，就能以高精度远程、被动地监视用户的浏览和应用使用情况。这揭示了现代 Web 平台功能中的一类新漏洞。 在实验中，FROST 攻击预测访问网站的准确率达 88.95%，预测打开应用的准确率达 95.83%。该攻击已在 macOS 和 Linux 上测试，但研究人员称 Windows 也可能受影响；用完网页后关闭标签页可降低风险。

telegram · zaihuapd · 5月31日 01:55

**背景**: SSD 定时侧信道攻击利用 SSD 内部资源争用导致的可测量的读写延迟差异。Origin Private File System (OPFS) 是一种浏览器 API，为 Web 应用提供私有的沙盒文件系统用于本地存储文件。FROST 利用 OPFS 发起受控的读写操作，并测量其完成时间，从而检测系统上的其他活动，推断正在使用的网站或应用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cyberpress.org/sites-ssd-timing-side-channel-attacks/">Malicious Sites Track Users Through SSD Timing Side-Channel Attacks</a></li>
<li><a href="https://cybersecuritynews.com/malicious-websites-track-ssd-timing/">Malicious Websites Track Visitors by Analyzing their SSD ...</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system">Origin private file system - Web APIs | MDN</a></li>

</ul>
</details>

**标签**: `#security`, `#side-channel attack`, `#SSD`, `#browser`, `#privacy`

---

<a id="item-9"></a>
## [AV2 参考编码器发布首个 1.0.0 版本](https://videocardz.com/newz/aomedias-av2-encoder-gets-first-1-0-0-release) ⭐️ 8.0/10

AOMedia 在 AVM GitHub 仓库中标记了 AV2 参考编码器的首个 1.0.0 版本，标志着下一代免版税视频编码格式迈出了第一步。 此次发布标志着 AV2 编解码器向实用化迈进，其目标是在相同视觉质量下比特率比 AV1 降低约 30%，有望以更高效率重塑视频流媒体、广播和实时通信等领域。 当前 AVM 软件是用于定义和测试格式的参考实现，而非优化的生产级编码器；其编码速度仍然很慢，细节保留问题尚未解决，且 AV2 规范仍为草案。

telegram · zaihuapd · 5月31日 14:08

**背景**: AV2 是开放媒体联盟（AOMedia）开发的一种开放、免版税的视频编码格式，是广泛使用的 AV1 的后续版本。工作始于 2020 年，原型实现显示在相同质量下比特率比 AV1 降低约 30%。AV2 预计将与基于版税的 VVC（H.266）格式在市场上展开竞争。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AV2_(video_coding_format)">AV2 (video coding format)</a></li>
<li><a href="https://www.phoronix.com/news/AV2-1.0-Specification-Released">AV 2 v1.0 Specification Released For Next-Gen Video Coding - Phoronix</a></li>
<li><a href="https://aomedia.org/press+releases/AOMedia-Announces-Year-End-Launch-of-Next-Generation-Video-Codec-AV2-on-10th-Anniversary/">AOMedia Announces Year-End Launch of Next Generation Video</a></li>

</ul>
</details>

**标签**: `#AV2`, `#video codec`, `#AOMedia`, `#reference encoder`

---