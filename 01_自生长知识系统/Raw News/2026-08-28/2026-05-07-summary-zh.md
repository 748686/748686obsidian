---
layout: default
title: "Horizon Summary: 2026-05-07 (ZH)"
date: 2026-05-07
lang: zh
---

> From 41 items, 14 important content pieces were selected

---

1. [Qwen 3.6 27B 通过 llama.cpp 的 MTP 实现 2.5 倍推理加速](#item-1) ⭐️ 9.0/10
2. [苹果计划在 iOS 27 中开放第三方 AI 模型](#item-2) ⭐️ 9.0/10
3. [英伟达、OpenAI、微软联合发布开源 MRC 协议](#item-3) ⭐️ 9.0/10
4. [对现代职场表演式生产力的批判](#item-4) ⭐️ 8.0/10
5. [氛围编码与代理工程在实践中界限模糊](#item-5) ⭐️ 8.0/10
6. [Incus 7.0 LTS 发布，新增备份 API 和 S3 支持](#item-6) ⭐️ 8.0/10
7. [ZAYA1-8B：基于 AMD 硬件训练的 8B 高效模型](#item-7) ⭐️ 8.0/10
8. [通过国际象棋 SVG 生成对比 Qwen 3.6 27B 量化质量](#item-8) ⭐️ 8.0/10
9. [Qwen3-27B 通过 MTP 嫁接实现 2.5 倍速度提升](#item-9) ⭐️ 8.0/10
10. [在 RTX 5090 上以 200k 上下文运行 Qwen3.6 27B NVFP4 和 MTP](#item-10) ⭐️ 8.0/10
11. [Anthropic 承诺五年内为谷歌云投入 2000 亿美元](#item-11) ⭐️ 8.0/10
12. [DeepSeek 据称正洽谈 450 亿美元估值融资](#item-12) ⭐️ 8.0/10
13. [谷歌 Chrome 静默下载 4GB AI 模型未获用户同意](#item-13) ⭐️ 8.0/10
14. [欧盟拟强制移除电信网络中华为和中兴设备](#item-14) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Qwen 3.6 27B 通过 llama.cpp 的 MTP 实现 2.5 倍推理加速](https://www.reddit.com/r/LocalLLaMA/comments/1t57xuu/25x_faster_inference_with_qwen_36_27b_using_mtp/) ⭐️ 9.0/10

最近的一个拉取请求为 llama.cpp 添加了 Qwen 3.6 27B 的多令牌预测（MTP）支持，在 M2 Max 和 RTX 3090 等消费级硬件上实现了高达 2.5 倍的令牌生成加速。 这使得本地代理编程在 48GB 设备上可行，上下文长度可达 262k，为实际应用拉近了云端与本地 LLM 推理之间的差距。 MTP 功能利用模型内置的张量层进行推测解码，需要从开放的 PR 自定义编译 llama.cpp。已转换的带有修正 Jinja 聊天模板的 GGUF 量化模型可在 Hugging Face 上获取。

reddit · r/LocalLLaMA · ex-arman68 · May 6, 09:35

**背景**: 推测解码通过使用较小的草稿模型预测多个令牌，然后由主模型并行验证，从而加速 LLM 推理。GGUF 格式使得模型能够在消费级硬件上高效量化和部署。llama.cpp 是一个流行的 C/C++推理引擎，支持多种模型和优化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/ggml-org/llama.cpp/pull/22673">llama + spec: MTP Support by am17an · Pull Request #22673 · ggml-org/llama.cpp</a></li>
<li><a href="https://research.google/blog/looking-back-at-speculative-decoding/">Looking back at speculative decoding</a></li>
<li><a href="https://dasroot.net/posts/2026/05/llama-cpp-performance-surge-beta-mtp-support/">Llama.cpp Performance Surge: Bridging the Gap with Beta MTP Support · Technical news about AI, coding and all</a></li>

</ul>
</details>

**社区讨论**: 社区非常热情，用户在各种硬件上报告了 2-3 倍的速度提升。一位 RTX 3090 用户在 IQ4_XS 量化下以 256k 上下文达到了 100 tok/s。一些用户指出进展速度之快令人应接不暇，但对实际改进表示赞赏。

**标签**: `#inference-speedup`, `#local-llm`, `#llama.cpp`, `#speculative-decoding`, `#Qwen`

---

<a id="item-2"></a>
## [苹果计划在 iOS 27 中开放第三方 AI 模型](https://www.bloomberg.com/news/articles/2026-05-05/ios-27-features-apple-plans-to-let-users-swap-models-across-apple-intelligence) ⭐️ 9.0/10

苹果计划在 iOS 27、iPadOS 27 和 macOS 27 中允许用户为 Siri、写作工具和图像乐园等系统功能选择第三方 AI 模型，打破 ChatGPT 目前的独家地位。 这标志着苹果 AI 策略的重大转变，将 Apple Intelligence 转变为一个开放平台，通过促进谷歌和 Anthropic 等提供商之间的竞争，可能重塑 AI 助手市场。 该功能内部称为 Extensions，可在设置中使用，允许用户切换用于文本生成、图像生成和编辑的模型，同时苹果继续提供自研模型。

telegram · zaihuapd · May 6, 05:38

**背景**: Apple Intelligence 是苹果的生成式 AI 系统，于 2024 年 WWDC 首次发布，结合了设备端和服务器处理。最初它整合了 ChatGPT 作为 Siri 和图像乐园等功能的独家第三方模型。新计划大幅扩展了第三方选择。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Apple_Intelligence">Apple Intelligence</a></li>
<li><a href="https://www.apple.com/apple-intelligence/">Apple Intelligence - Apple</a></li>

</ul>
</details>

**标签**: `#Apple`, `#AI`, `#iOS`, `#ChatGPT`, `#third-party models`

---

<a id="item-3"></a>
## [英伟达、OpenAI、微软联合发布开源 MRC 协议](https://blogs.nvidia.com/blog/spectrum-x-ethernet-mrc/) ⭐️ 9.0/10

英伟达、OpenAI 和微软等合作伙伴联合发布并开源了多路径可靠连接（MRC）协议，这是一种采用数据包喷射技术实现多路径并发传输并具备微秒级故障重路由能力的 RDMA 传输协议。 此次多家 AI 巨头合作旨在解决大规模 AI 训练中的网络瓶颈，提升千兆级集群的吞吐量和稳定性。作为贡献给 OCP 的开放标准，MRC 旨在减少行业碎片化，加速 Stargate 等未来 AI 基础设施的建设。 MRC 已部署在 NVIDIA Spectrum-X 平台和 Blackwell 架构上，支撑微软 Fairwater 和 OCI Abilene 等系统，并用于 GPT-5.5 等模型训练。该协议是开放计算项目（OCP）下的开放规范。

telegram · zaihuapd · May 6, 14:39

**背景**: RDMA（远程直接内存访问）可在无需操作系统介入的情况下实现计算机间的直接数据传输，达到高吞吐量和低延迟。传统网络在大规模 AI 集群中面临拥塞和单路径故障问题。MRC 结合了数据包喷射（跨多条路径发送数据）和快速故障切换，确保持续为 GPU 提供数据，减少空闲时间。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://blogs.nvidia.com/blog/spectrum-x-ethernet-mrc/">NVIDIA Spectrum-X — the Open, AI-Native Ethernet Fabric ...</a></li>
<li><a href="https://www.firecat-web.com/daily-news/7869">OpenAI联合多家厂商推出MRC协议，破解大规模AI训练网络瓶颈</a></li>
<li><a href="https://news.qq.com/rain/a/20260507A00RCF00">OpenAI携手五巨头开源革命性超算协议：一举解决超大集群LLM训练不稳定...</a></li>

</ul>
</details>

**标签**: `#AI基础设施`, `#网络协议`, `#NVIDIA`, `#MRC协议`, `#高算力集群`

---

<a id="item-4"></a>
## [对现代职场表演式生产力的批判](https://nooneshappy.com/article/appearing-productive-in-the-workplace/) ⭐️ 8.0/10

一篇在 No One's Happy 发表的评论文章分析了现代职场（尤其是科技行业）如何通过冗长文档、AI 生成的过度工程化和表演性产物，优先展现表面生产力而非实际产出。 这篇文章与那些亲身经历表演式生产力低效的工程师和管理者产生强烈共鸣，揭示了 AI 工具可能加剧而非解决职场冗余问题。 作者指出需求文档从一页增至十二页，状态更新变成了摘要的摘要，而 AI 生成的过度工程化受到非技术管理者的赞扬，却掩盖了低效。

hackernews · diebillionaires · May 6, 16:18 · [社区讨论](https://news.ycombinator.com/item?id=48038001)

**背景**: 表演式生产力指那些营造高效假象却未带来实际价值的行为，例如过度文档和过度工程化解决方案。在软件工程中，生成式 AI 工具（如大语言模型）加剧了这一问题，它们能生成大量看似出色但缺乏实质的代码和文本。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://medium.com/@olabodeoyeneye/documentation-bloat-at-workplace-perspectives-on-its-avoidance-c0f32b82a277">Documentation Bloat at Workplace: Perspectives on its Avoidance | by 'Bode Oyeneye | Medium</a></li>
<li><a href="https://www.forbes.com/sites/timkeary/2026/04/27/is-software-engineering-cooked-the-future-of-development-post-ai/">Is Software Engineering ‘Cooked’? The Future Of Development ...</a></li>
<li><a href="https://www.acm.org/media-center/2026/april/techbrief-vibe-coding">AI “Vibe Coding” Could Reshape Software Development but Lacks ...</a></li>

</ul>
</details>

**社区讨论**: 评论者普遍认同这一批评，分享了关于 AI 过度工程化和文档膨胀的个人经历。有人认为软件工程因其非技术管理文化和工具滥用而特别容易滋生此类问题。

**标签**: `#workplace culture`, `#software engineering`, `#productivity`, `#management`, `#AI`

---

<a id="item-5"></a>
## [氛围编码与代理工程在实践中界限模糊](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/#atom-everything) ⭐️ 8.0/10

西蒙·威利森在播客中透露，他原本认为截然不同的“氛围编码”和“代理工程”在自己的工作中正日益重叠，这让他对代码质量和责任感到不安。 这种融合挑战了 AI 在软件开发中的负责任使用，因为即使经验丰富的工程师在 AI 代理变得可靠时也可能跳过代码审查，可能损害生产软件的质量和安全性。 威利森指出，对于生成 JSON API 端点等常规任务，他信任 Claude Code 能产出正确代码而不审查每一行，但他质疑这对于生产系统是否负责任。

rss · Simon Willison · May 6, 14:24 · [社区讨论](https://news.ycombinator.com/item?id=48037128)

**背景**: “氛围编码”由安德烈·卡帕西于 2025 年提出，是一种 AI 辅助编程方式，程序员接受生成的代码而不进行深入审查。“代理工程”也由卡帕西提出，指在专业工程工作流程中将 AI 代理作为工具使用，强调监督和质量。威利森此前认为氛围编码适用于个人工具，但对生产软件不负责任，而代理工程则保持高标准。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Vibe_coding">Vibe coding</a></li>
<li><a href="https://www.ibm.com/think/topics/agentic-engineering">What is agentic engineering? - IBM</a></li>

</ul>
</details>

**社区讨论**: 评论者对 AI 的可靠性表示怀疑，指出错误变得更加微妙且难以发现，有人指出使用代码行数作为指标是有问题的。另有人强调，在 AI 出现之前就已经存在不规范的工程实践，现在只是被加速了。

**标签**: `#vibe coding`, `#agentic engineering`, `#AI coding tools`, `#software engineering`, `#LLMs`

---

<a id="item-6"></a>
## [Incus 7.0 LTS 发布，新增备份 API 和 S3 支持](https://lwn.net/Articles/1071469/) ⭐️ 8.0/10

Incus 7.0 LTS 已发布，引入了底层备份 API、内置 S3 操作（取代 MinIO），并移除了对 cgroups v1 和 xtables 的支持。 此长期支持版本确保了容器和虚拟机管理稳定至 2031 年，移除 cgroups v1 和 xtables 等过时依赖使平台现代化。 前两年通过小版本提供错误修复和改进，随后五年仅进行安全维护。共有 204 人参与此版本的贡献。

rss · LWN.net · May 6, 13:53

**背景**: Incus 是一个容器和虚拟机管理器，源自 LXC/LXD。cgroups v1 是旧版内核资源控制机制，已被 cgroups v2 取代。xtables（iptables、ip6tables、ebtables）是传统防火墙框架，现已由 nftables 替代。此版本使 Incus 与现代 Linux 内核功能保持一致。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://diveinto.com/blog/cgroups-v1-to-v2">Understanding cgroups: From v1 to v2 and Why It Matters for ...</a></li>
<li><a href="https://dashdash.io/8/xtables-nft">xtables-nft(8): iptables using nftables | Linux Man Page</a></li>

</ul>
</details>

**标签**: `#Incus`, `#containers`, `#virtual-machines`, `#LTS`, `#open-source`

---

<a id="item-7"></a>
## [ZAYA1-8B：基于 AMD 硬件训练的 8B 高效模型](https://www.zyphra.com/post/zaya1-8b) ⭐️ 8.0/10

Zyphra 发布了 ZAYA1-8B，这是一个 80 亿参数的语言模型，完全在由 1024 个 AMD MI300x 节点和 Pensando Pollara 互连组成的集群上预训练，采用新颖的 Markovian RSA 架构，性能可与超过 1000 亿参数的模型相媲美。 这表明前沿质量的小型语言模型可以在非 NVIDIA 硬件上训练，减少对单一供应商的依赖，并可能降低 AI 研究和本地部署的成本。 该模型采用 MoE++架构、推理优先预训练、推理强化学习级联以及一种称为 Markovian RSA 的测试时计算方法。它设计用于在 24-32GB 显存的 GPU 上本地部署，并提供 vLLM 分支支持。

reddit · r/LocalLLaMA · carbocation · May 6, 19:43 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1t5nll0/zaya18b_frontier_intelligence_density_trained_on/)

**背景**: 由于 CUDA 生态的主导地位，训练大型语言模型通常需要昂贵的 NVIDIA 硬件。AMD 一直在开发其 ROCm 软件栈以支持 AI 工作负载，但在 AMD 基础设施上进行大规模预训练仍然很少见。Markovian RSA 是一种新颖的测试时计算技术，可以迭代改进推理轨迹，在不增加模型大小的情况下提高推理质量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://x.com/ZyphraAI/status/2052103623904309618">Zyphra on X: "Maximum intelligence per parameter was the target. ZAYA1-8B's performance reflects innovations across the full stack: Zyphra’s MoE++ architecture, reasoning-first pretraining, a reasoning RL cascade methodology, and a novel test-time compute method called Markovian RSA. https://t.co/LjNnbkniwj" / X</a></li>
<li><a href="https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/pretrain/setup_tutorial.html">Pretraining with Megatron-LM — Tutorials for AI developers 12.0</a></li>
<li><a href="https://medium.com/@RaajasSode/training-large-language-models-with-an-amd-gpu-85e53616b20c">Training Large Language Models with an AMD GPU - Medium</a></li>

</ul>
</details>

**社区讨论**: 社区对基于 AMD 的训练感到兴奋，但对基准比较持怀疑态度。一些用户质疑“前沿”模型的对比，而另一些用户则欢迎这一创新并希望获得本地部署支持。也有人担心与 llama.cpp 等推理引擎的兼容性有限。

**标签**: `#AMD`, `#small language models`, `#model training`, `#novel architecture`, `#local deployment`

---

<a id="item-8"></a>
## [通过国际象棋 SVG 生成对比 Qwen 3.6 27B 量化质量](https://www.reddit.com/r/LocalLLaMA/comments/1t53dhp/quality_comparison_between_qwen_36_27b/) ⭐️ 8.0/10

一位 Reddit 用户通过随机走棋的国际象棋棋盘 SVG 生成任务，实证比较了 Qwen 3.6 27B 多种量化版本（BF16、Q8_0、Q6_K、Q5_K_XL、Q4_K_XL、IQ4_XS、IQ3_XXS）之间的质量退化程度。 该对比为在有限显存（16GB）上部署本地大语言模型的量化选择提供了实用指导，揭示了模型大小、速度与输出正确性之间的权衡。 任务要求跟踪 7 步随机走棋（半回合）后的棋盘状态，并生成包含棋子位置和最后一步高亮显示的正确 SVG，考验推理与代码生成能力。

reddit · r/LocalLLaMA · bobaburger · May 6, 05:10

**背景**: 量化降低模型权重精度以将更大模型适配到更少显存中，但会损失输出质量。常见方法包括 Q8_0（8 位）、Q6_K（6 位）以及 IQ（改进量化）变体如 IQ4_XS 和 IQ3_XXS，位宽越低压缩越大但退化也越严重。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/localmodels/Llama-2-7B-ggml">localmodels/Llama-2-7B-ggml · Hugging Face</a></li>
<li><a href="https://gist.github.com/Artefact2/b5f810600771265fc1e39442288e8ec9">GGUF quantizations overview · GitHub</a></li>
<li><a href="https://tonisagrista.com/blog/2026/quantization/">GGUF quantization guide - Langur Monkey</a></li>

</ul>
</details>

**社区讨论**: 评论者称赞测试的全面性和视觉清晰度，但也提出单次运行结果可能受统计噪声影响。建议包括多次测试、尝试 AWQ 量化以及使用 llama.cpp 的分支版本来更好地处理上下文。

**标签**: `#quantization`, `#Qwen3.6`, `#local LLM`, `#benchmark`, `#SVG generation`

---

<a id="item-9"></a>
## [Qwen3-27B 通过 MTP 嫁接实现 2.5 倍速度提升](https://www.reddit.com/r/LocalLLaMA/comments/1t5ageq/qwen3627b_with_mtp_grafted_on_unsloth_ud_xl_25x/) ⭐️ 8.0/10

一位用户将多标记预测（MTP）草案头嫁接到使用 Unsloth UD XL 量化的 Qwen3-27B GGUF 模型上，并使用了包含未合并 PR #22673 的自定义 llama.cpp 构建，实现了 2-2.5 倍的令牌吞吐量提升。 这一优化显著加快了 270 亿参数模型的本地推理速度，使其对使用部分 CPU 卸载等受限硬件的用户更加实用，并展示了在 llama.cpp 官方支持之前，在量化模型上启用 MTP 的可行方法。 基础模型使用 Unsloth 的 UD XL 量化（例如 Q4_K_XL），而三个 MTP 层保持在 Q8_0 以保持推测准确性；所有 GGUF 文件和一个转换脚本已在 Hugging Face 上共享以供复现。

reddit · r/LocalLLaMA · havenoammo · May 6, 11:45

**背景**: 多标记预测（MTP）是一种训练技术，模型同时预测多个未来标记，通过推测解码提高推理效率。GGUF 是一种二进制格式，优化用于通过 llama.cpp 等执行器在本地运行量化模型。Unsloth 的 UD XL 量化在保持质量的同时减小模型大小。llama.cpp 中的 PR #22673 添加了 MTP 支持，但尚未合并到主分支。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2404.19737">[2404.19737] Better & Faster Large Language Models via Multi-token Prediction</a></li>
<li><a href="https://huggingface.co/docs/hub/gguf">GGUF · Hugging Face</a></li>
<li><a href="https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs">Unsloth Dynamic 2.0 GGUFs | Unsloth Documentation</a></li>

</ul>
</details>

**社区讨论**: 评论普遍非常积极，用户在包括 RTX Pro 6000 和 AMD ROCm（RDNA 3.5）在内的各种硬件上报告了 2-2.5 倍的加速。一些用户指出了对部分 CPU 卸载场景的益处，并感谢共享的转换脚本，可用于将 MTP 嫁接到其他模型。

**标签**: `#LLM inference`, `#Multi-Token Prediction`, `#GGUF quantization`, `#llama.cpp`, `#optimization`

---

<a id="item-10"></a>
## [在 RTX 5090 上以 200k 上下文运行 Qwen3.6 27B NVFP4 和 MTP](https://www.reddit.com/r/LocalLLaMA/comments/1t5dya8/qwen36_27b_nvfp4_mtp_on_a_single_rtx_5090_200k/) ⭐️ 8.0/10

一名用户在单张 RTX 5090 GPU 上成功运行了 Qwen3.6-27B-NVFP4 模型，并启用了多令牌预测（MTP）推测解码，使用 vLLM 和 flashinfer 注意力后端实现了 200k 的上下文长度。 这一演示表明，具有 27B 参数的大语言模型可以在消费级硬件上以高上下文长度和不错的性能运行，使先进 AI 更易访问且更适用于本地部署。 配置使用了 NVFP4 量化（compressed-tensors）、KV 缓存数据类型 fp8_e4m3、3 个推测令牌的 MTP，以及 max-model-len 设为 230400。用户仅验证了 200k 上下文，而非完整的 262k。

reddit · r/LocalLLaMA · Maheidem · May 6, 14:05

**背景**: NVFP4 是 NVIDIA 提出的一种 4 位浮点量化格式，相比整数量化保留了更高的动态范围。多令牌预测（MTP）是一种推测解码方法，目标模型自身预测多个未来令牌，无需单独的草稿模型，可潜在使推理吞吐量翻倍或提升三倍。FlashInfer 是一个用于注意力操作的高性能 CUDA 内核库，在 vLLM 中用于加速预填充和解码阶段。vLLM 是一个开源 LLM 服务框架，支持多种量化和解码优化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://build.nvidia.com/spark/nvfp4-quantization">NVFP4 Quantization | DGX Spark</a></li>
<li><a href="https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp/">MTP (Multi-Token Prediction) - vLLM</a></li>
<li><a href="https://github.com/flashinfer-ai/flashinfer">GitHub - flashinfer-ai/flashinfer: FlashInfer: Kernel Library ... Attention Backend Feature Support - vLLM FlashAttention and FlashInfer | vllm-project/vllm | DeepWiki FlashInfer on ROCm: High‑Throughput Prefill Attention via ... FlashInfer: Efficient and Customizable Attention Engine for ... FlashInfer Attention Backend | NVIDIA/TensorRT-LLM | DeepWiki</a></li>

</ul>
</details>

**社区讨论**: 评论者对此性能表示赞赏，一位用户指出在消费级硬件上以 Q4 运行约 30B 密集模型并支持 128k+上下文是一场革命。另一位用户报告在 5090 上使用类似设置，启用思考功能后达到 75-130 t/s。同时也有关于禁用思考功能以及该配置是否属于“AI 垃圾”的讨论。

**标签**: `#LLM`, `#vLLM`, `#quantization`, `#RTX5090`, `#MTP`

---

<a id="item-11"></a>
## [Anthropic 承诺五年内为谷歌云投入 2000 亿美元](https://www.theinformation.com/articles/anthropic-commits-spending-200-billion-googles-cloud-chips?utm_source=chatgpt.com) ⭐️ 8.0/10

Anthropic 承诺未来五年内向谷歌云支付 2000 亿美元，这一金额占谷歌云已披露积压订单的 40%以上。《The Information》报道后，Alphabet 盘后股价上涨约 2%。 这一巨额承诺表明 Anthropic 与谷歌之间形成了深度的战略联盟，巩固了谷歌云在人工智能基础设施领域的地位，并加剧了与 AWS 和微软 Azure 等云提供商的竞争。同时，它也凸显了训练和部署先进 AI 模型所需的巨额资本投入。 今年 4 月，双方还与博通签署协议，锁定数吉瓦的 TPU 算力，预计从 2027 年起陆续上线。此外，Alphabet 计划以 3500 亿美元的估值向 Anthropic 投资最多 400 亿美元，进一步加深双方合作。

telegram · zaihuapd · May 6, 03:53

**背景**: Anthropic 是一家专注于人工智能研究与安全的企业，以其 Claude 系列大语言模型闻名。谷歌云的 TPU（张量处理单元）是专为 AI 工作负载设计的定制芯片，能够优化训练和推理性能。云提供商的积压订单指客户已承诺但尚未确认为收入的支出，而这项承诺占谷歌云未来收入的很大一部分。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cloud.google.com/tpu">Tensor Processing Units (TPUs) | Google Cloud</a></li>

</ul>
</details>

**标签**: `#Anthropic`, `#Google Cloud`, `#AI Infrastructure`, `#Cloud Computing`, `#Business Strategy`

---

<a id="item-12"></a>
## [DeepSeek 据称正洽谈 450 亿美元估值融资](https://www.bloomberg.com/news/articles/2026-05-06/china-chip-fund-in-talks-to-lead-mega-deepseek-funding-ft-says) ⭐️ 8.0/10

据称，DeepSeek 正洽谈首轮大规模外部融资，由中国国家集成电路产业投资基金领投，估值约 450 亿美元。 这笔融资将是国资背景资金对中国 AI 领域的重要投入，表明政府正更深介入核心 AI 公司，可能在美国芯片出口限制下加速 DeepSeek 的发展。 本轮融资由中国国家集成电路产业投资基金（又称“大基金”）领投，是 DeepSeek 首次大规模外部融资。450 亿美元的估值反映了 DeepSeek 自 2023 年成立以来的快速崛起。

telegram · zaihuapd · May 6, 06:28

**背景**: DeepSeek 是一家中国 AI 公司，于 2023 年由梁文锋创立，最初由对冲基金 High-Flyer 资助。2025 年初，其 R1 模型以极低的训练成本达到与 GPT-4 相当的性能，引起全球关注。国家集成电路产业投资基金是一个国资基金，旨在推动中国半导体自给自足。此次潜在投资表明中国在技术限制下仍战略性地加强 AI 能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></li>
<li><a href="https://en.wikipedia.org/wiki/National_Integrated_Circuit_Industry_Investment_Fund">National Integrated Circuit Industry Investment Fund</a></li>

</ul>
</details>

**标签**: `#DeepSeek`, `#AI funding`, `#China`, `#semiconductor`, `#venture capital`

---

<a id="item-13"></a>
## [谷歌 Chrome 静默下载 4GB AI 模型未获用户同意](https://www.tomshardware.com/tech-industry/cyber-security/google-chrome-silently-downloads-4gb-ai-model-to-your-device-without-permission-report-claims-researcher-says-practice-may-violate-eu-law-waste-thousands-of-kilowatts-of-energy) ⭐️ 8.0/10

安全研究员 Alexander Hanff 报告称，Google Chrome 在未获用户许可的情况下，向符合硬件条件的设备静默下载约 4GB 的 Gemini Nano AI 模型文件（weights.bin），即便手动删除也会自动重新下载。 这种行为可能违反欧盟 GDPR 等隐私法律，并浪费大量能源和带宽，潜在影响数十亿用户。这凸显了科技公司未经用户同意强制部署 AI 功能的更广泛趋势。 模型文件大小约 4GB，研究人员估计，向 10 亿用户分发该文件可能产生高达 6 万吨碳排放。据报道，Anthropic 的 Claude 应用也存在类似行为。

telegram · zaihuapd · May 6, 11:15

**背景**: Gemini Nano 是谷歌 DeepMind 开发的轻量级 AI 模型，旨在设备端运行，用于摘要和智能回复等任务。Chrome 一直在整合 AI 功能，但此次静默下载引发了对用户控制和数据隐私的担忧。文件'weights.bin'包含训练好的神经网络参数。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Gemini_(language_model)">Gemini (language model) - Wikipedia</a></li>

</ul>
</details>

**标签**: `#privacy`, `#google-chrome`, `#AI`, `#GDPR`, `#security`

---

<a id="item-14"></a>
## [欧盟拟强制移除电信网络中华为和中兴设备](https://t.me/zaihuapd/41247) ⭐️ 8.0/10

欧盟委员会正考虑制定新规，强制所有成员国在其电信和宽带基础设施中逐步淘汰华为和中兴的设备，将之前不具约束力的建议升级为具有法律效力的强制性规定。 这标志着欧盟网络安全政策的重大升级，可能重塑欧洲电信供应链并影响全球地缘政治。若实施，将迫使运营商更换现有基础设施，影响成本与网络运营，同时也会影响其他地区对高风险供应商的处理方式。 新规还将收紧对外基础设施资金池，停止向使用华为设备的非欧盟国家提供贷款。未能按期移除指定设备的成员国可能面临违规调查和经济处罚。

telegram · zaihuapd · May 6, 14:00

**背景**: 2020 年，欧盟通过了 5G 网络安全工具箱，这是一套不具约束力的措施，旨在应对来自华为和中兴等高风险供应商的风险。该工具箱包括限制或排除此类供应商参与 5G 网络的建议，但各成员国的实施情况各不相同。拟议的法规旨在在全欧盟范围内建立统一、具有约束力的方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://digital-strategy.ec.europa.eu/en/library/eu-toolbox-5g-security">The EU toolbox for 5G security - Shaping Europe’s digital ...</a></li>
<li><a href="https://www.telecomrevieweurope.com/articles/reports-and-coverage/how-the-eus-5g-toolbox-shapes-secure-connectivity/">How the EU’s 5G Toolbox Shapes Secure Connectivity</a></li>
<li><a href="https://eutechloop.com/eus-plans-to-reduce/">EU’s plans to reduce dependency on high-risk vendors</a></li>

</ul>
</details>

**标签**: `#Huawei`, `#EU`, `#telecom regulation`, `#cybersecurity`, `#geopolitics`

---