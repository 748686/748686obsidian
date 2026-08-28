---
layout: default
title: "Horizon Summary: 2026-04-11 (ZH)"
date: 2026-04-11
lang: zh
---

> From 38 items, 19 important content pieces were selected

---

1. [DeepSeek V4 旗舰大模型拟于 4 月下旬发布，首次实现国产芯片深度适配](#item-1) ⭐️ 9.0/10
2. [cuBLAS 性能缺陷导致 RTX 5090 上批处理 FP32 矩阵乘法效率降低约 60%](#item-2) ⭐️ 8.0/10
3. [GLM 5.1 在智能体基准测试中以约三分之一成本达到接近 Opus 的性能。](#item-3) ⭐️ 8.0/10
4. [新加坡国立大学推出 DMax，为扩散语言模型实现激进并行解码](#item-4) ⭐️ 8.0/10
5. [社区发布本地大语言模型现状、工具与发展概览](#item-5) ⭐️ 8.0/10
6. [LoRA 微调使 9B Qwen 模型能自主完成 89%的数据分析工作流](#item-6) ⭐️ 8.0/10
7. [社区从 TFLite 文件逆向工程 Gemma 4 的多令牌预测功能](#item-7) ⭐️ 8.0/10
8. [金融监管机构与华尔街 CEO 紧急开会，讨论 Anthropic 新 AI 模型 Mythos 带来的网络安全风险。](#item-8) ⭐️ 8.0/10
9. [阿里巴巴成立 ATH 事业群，由 CEO 吴泳铭亲征，全面锚定 Token 经济](#item-9) ⭐️ 8.0/10
10. [Solayer 创始人揭示 LLM 供应链风险：超 20% 免费路由器存在恶意行为](#item-10) ⭐️ 8.0/10
11. [法国政府承诺在 2026 年前为 250 万公务员用 Linux 取代 Windows](#item-11) ⭐️ 8.0/10
12. [Claude AI 模型曝出“身份混淆”缺陷，在自动化工具中可能触发未授权高危操作。](#item-12) ⭐️ 8.0/10
13. [WireGuard 在解决微软驱动签名问题后发布新版 Windows 版本](#item-13) ⭐️ 7.0/10
14. [氦气因其独特性质和经济学因素而难以被替代。](#item-14) ⭐️ 7.0/10
15. [Linux 内核因内存子系统变化移除页面缓存中的只读透明大页支持。](#item-15) ⭐️ 7.0/10
16. [GLM 5.1 在开源模型的代码竞技场基准测试中排名第一](#item-16) ⭐️ 7.0/10
17. [香港金管局向碇点金融及汇丰银行发出首批稳定币发行人牌照](#item-17) ⭐️ 7.0/10
18. [MiniMax 发布新一代音乐大模型 Music 2.6，开启 14 天免费内测](#item-18) ⭐️ 7.0/10
19. [硬件监测工具 CPU-Z 官网遭黑客入侵，部分下载包被植入恶意代码](#item-19) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [DeepSeek V4 旗舰大模型拟于 4 月下旬发布，首次实现国产芯片深度适配](https://finance.sina.com.cn/tech/2026-04-10/doc-inhtymqf5317301.shtml) ⭐️ 9.0/10

DeepSeek 创始人梁文锋在内部沟通中表示，新一代旗舰大模型 DeepSeek V4 将于 2026 年 4 月下旬正式发布，该模型具备万亿级参数规模和百万级上下文窗口，并首次实现与华为昇腾等国产芯片的深度适配。受此影响，阿里巴巴、字节跳动及腾讯等科技巨头已预订数十万片 AI 芯片，相关产品价格近期上涨约 20%。 这标志着中国 AI 产业在'去 CUDA 化'进程中取得关键进展，减少了对国外技术的依赖。国产芯片的深度适配将加速国内 AI 基础设施建设，并可能重塑全球 AI 芯片市场格局，从科技巨头的预订需求和价格上涨可见其影响。 据报道，该模型采用混合专家（MoE）架构，参数规模达 1 万亿，是目前最大的开源 MoE 模型之一。DeepSeek 已在网页端上线'快速模式'和'专家模式'为新模型预热，但官方尚未对发布消息作出正式回应。

telegram · zaihuapd · Apr 10, 05:16

**背景**: DeepSeek 是一家中国人工智能公司，专注于开发大语言模型，DeepSeek V4 是其即将发布的旗舰模型，具备万亿级参数规模。华为昇腾是面向数据中心设计的 AI 芯片系列，其中昇腾 910 采用 7 纳米工艺，旨在与 NVIDIA 竞争。CUDA 是 NVIDIA 的并行计算平台，在 AI 芯片市场占据主导地位，这种依赖性引发了担忧，促使业界开发 chipStar 等替代方案和开放标准。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>
<li><a href="https://macaron.im/nn/blog/deepseek-v4-moe-1-trillion">DeepSeek - V 4 MoE: The 1-Trillion Parameter Breakthrough - Macaron</a></li>
<li><a href="https://hardforum.com/threads/huawei-announces-ascend-ai-chips.1969505/">Huawei Announces Ascend AI Chips | [H]ard|Forum</a></li>

</ul>
</details>

**标签**: `#AI`, `#Large Language Models`, `#Chip Technology`, `#Industry News`, `#China Tech`

---

<a id="item-2"></a>
## [cuBLAS 性能缺陷导致 RTX 5090 上批处理 FP32 矩阵乘法效率降低约 60%](https://www.reddit.com/r/MachineLearning/comments/1shtv0r/d_60_matmul_performance_bug_in_cublas_on_rtx_5090/) ⭐️ 8.0/10

NVIDIA 的 cuBLAS 库中存在一个性能缺陷，导致在 RTX 5090 GPU 上进行批处理 FP32 矩阵乘法时效率降低约 60%，基准测试显示自定义内核在某些矩阵尺寸下比 cuBLAS 快高达 170%。该问题在 CUDA 13.2.51、cuBLAS 13.3.0 和驱动 595.58.03 下测试，可能影响所有非专业版 RTX GPU。 这一缺陷严重影响依赖批处理矩阵乘法的机器学习和科学计算工作负载，可能拖慢在广泛使用的 RTX GPU 上的训练和推理速度。它突显了 NVIDIA 软件栈中潜在的优化差异，非专业版 GPU 可能比 H200 等专业或数据中心型号受到较少关注。 该缺陷导致 cuBLAS 为从 256×256 到 8192×8192×8 的批处理 FP32 工作负载分派低效内核，仅使用 RTX GPU 上约 40% 的可用计算资源。相比之下，Pro 6000 和 H200 等其他 GPU 使用更优化的内核，H200 通过混合 CUTLASS 和 xmma 系列实现高达 82% 的 FMA 利用率。

reddit · r/MachineLearning · NoVibeCoding · Apr 10, 17:51

**背景**: cuBLAS 是 NVIDIA 的 CUDA 基础线性代数子程序库，针对 GPU 加速的矩阵运算（如 GEMM，通用矩阵乘法）进行了优化，这些运算是深度学习和高性能计算的基础。批处理矩阵乘法可同时处理多个矩阵，提高神经网络训练等任务的吞吐量。FMA（融合乘加）是一种关键的 GPU 指令，将乘法和加法合并为一步，提升了数值计算的性能和精度。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.nvidia.com/blog/new-cublas-12-0-features-and-matrix-multiplication-performance-on-nvidia-hopper-gpus/">New cuBLAS 12.0 Features and Matrix Multiplication Performance</a></li>
<li><a href="https://en.wikipedia.org/wiki/Multiply–accumulate_operation">Multiply–accumulate operation - Wikipedia</a></li>

</ul>
</details>

**标签**: `#GPU`, `#cuBLAS`, `#Performance`, `#Machine Learning`, `#NVIDIA`

---

<a id="item-3"></a>
## [GLM 5.1 在智能体基准测试中以约三分之一成本达到接近 Opus 的性能。](https://www.reddit.com/r/LocalLLaMA/comments/1shus54/glm_51_crushes_every_other_model_except_opus_in/) ⭐️ 8.0/10

智谱 AI 的大型语言模型 GLM 5.1 在基于 OpenClaw 的智能体基准测试中，以每次运行约 0.4 美元的成本达到与 Opus 4.6 相当的性能，而 Opus 的成本约为 1.2 美元。它在测试中超越了所有其他模型，成为 OpenClaw 等智能体任务的顶级选择。 这一突破显著提升了智能体 AI 的成本效益，使高性能模型在自主助手和复杂任务自动化等实际应用中更易获取。它挑战了 Opus 等昂贵模型的主导地位，可能加速开源或低成本替代方案在 AI 智能体生态系统中的采用。 测试方法在真实环境中使用 OpenClaw 处理用户提交的任务，采用类似 Chatbot Arena 的 LLM-as-a-judge 方法，以避免静态基准测试优化问题。Qwen 3.6 也表现良好，但目前 OpenRouter 上不支持提示缓存，这推高了其成本；若支持缓存，其成本可能达到与 minimax m2.7 相似的水平。

reddit · r/LocalLLaMA · zylskysniper · Apr 10, 18:23

**背景**: GLM 5.1 是智谱 AI 开发的 GLM 系列中最强大的模型，专为复杂系统工程和长视野智能体任务设计。OpenClaw 是一个免费开源的自主 AI 智能体，通过 LLM 执行任务，使用消息平台作为其界面。智能体基准测试与经典 ML 基准测试不同，强调真实场景中的多步交互、环境操作和结果验证，通常使用 LLM-as-a-Judge 方法进行评估。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://cookbook.sglang.io/autoregressive/GLM/GLM-5">GLM-5 | SGLang Cookbook</a></li>
<li><a href="https://en.wikipedia.org/wiki/OpenClaw">OpenClaw - Wikipedia</a></li>
<li><a href="https://www.emergentmind.com/topics/agentic-benchmarks">Agentic Benchmarks</a></li>

</ul>
</details>

**标签**: `#AI Agents`, `#Benchmarking`, `#Cost Efficiency`, `#Large Language Models`, `#Open Source AI`

---

<a id="item-4"></a>
## [新加坡国立大学推出 DMax，为扩散语言模型实现激进并行解码](https://v.redd.it/buzbtk1hdeug1) ⭐️ 8.0/10

新加坡国立大学的研究人员提出了 DMax，这是一种扩散语言模型（dLLM）的新范式，通过渐进式自我精炼和策略内均匀训练来减轻错误累积，从而实现激进的并行解码。该方法将解码重新定义为从掩码嵌入到标记嵌入的渐进过渡过程，使模型能够在生成过程中纠正自身的错误预测。 这一进展具有重要意义，因为它通过实现更快、并行的解码同时保持生成质量，解决了语言模型效率的关键瓶颈，可能加速代码生成和推理任务等应用。它代表了扩散模型处理文本生成方式的转变，超越了顺序或基于二进制掩码的方法，以提高人工智能系统的可扩展性和性能。 DMax 显著提高了每次前向传播的吞吐量（TPF），在 GSM8K 上从 2.04 提升至 5.47，在 MBPP 上从 2.71 提升至 5.86，同时保持准确性，并在两个 H200 GPU 上以批次大小 1 实现了平均每秒 1,338 个标记。该方法依赖于软并行解码，将中间状态表示为预测标记嵌入和掩码嵌入之间的插值，以实现迭代式自我修正。

reddit · r/LocalLLaMA · 44th--Hokage · Apr 10, 17:23

**背景**: 扩散语言模型（dLLM）是一类通过噪声到文本的转换过程生成文本的人工智能模型，类似于 DALL-E 等图像扩散模型，为顺序预测标记的自回归模型提供了替代方案。并行解码旨在通过同时处理多个标记来加速文本生成，但在扩散模型中常面临错误累积等挑战，错误可能传播并降低输出质量。DMax 方法基于这些概念，引入了渐进式自我精炼来减轻此类错误，如扩散语言模型的相关调查和资源所述。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2508.10875">[2508.10875] A Survey on Diffusion Language Models - arXiv.org</a></li>
<li><a href="https://huggingface.co/blog/ProCreations/diffusion-language-model">Diffusion Language Models: The New Paradigm - Hugging Face</a></li>
<li><a href="https://arxiv.org/html/2509.25188v1">Learning to Parallel: Accelerating Diffusion Large Language</a></li>

</ul>
</details>

**标签**: `#diffusion-models`, `#language-models`, `#parallel-decoding`, `#AI-research`, `#machine-learning`

---

<a id="item-5"></a>
## [社区发布本地大语言模型现状、工具与发展概览](https://i.redd.it/6jxe6recjaug1.png) ⭐️ 8.0/10

社区分享了一份题为 'the state of LocalLLama' 的概览，基于 1390 个赞和 98%的点赞率的高参与度，提供了关于本地运行大语言模型的当前现状、工具和发展的见解。该概览综合了社区在硬件、优化技术以及如 Mistral 7B、Llama 3 和 Mixtral 8x7B 等流行模型方面的知识。 这很重要，因为它突显了本地运行大语言模型以保护隐私、节省成本和增强控制的增长趋势，使开发者和爱好者能够利用开源模型而无需依赖云 API。这反映了 AI 的民主化，让更多人能够在消费级硬件上实验和部署先进的语言模型。 关键细节包括关注如 Ollama 和 LM Studio 等本地部署工具，针对 NVIDIA RTX 4090 和 Apple Silicon 等硬件的优化，以及使用如 Mistral 7B 和 Llama 3 等开源权重模型。该概览是社区驱动的，强调实用指导和实际应用而非理论研究。

reddit · r/LocalLLaMA · Beginning-Window-115 · Apr 10, 04:30

**背景**: LocalLLaMA 是一个专注于本地运行大语言模型的社区项目，通常通过讨论工具、硬件和优化技术的子论坛和指南进行交流。本地运行大语言模型涉及使用开源框架和工具在个人电脑或服务器上执行模型，绕过云服务以提高隐私性和降低成本。随着强大消费级硬件和高效模型架构的可用性，这一趋势获得了动力，使更多人能够接触 AI 能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://localllamma.pro/">LocalLLaMA - The Underground Guide to Local AI</a></li>
<li><a href="https://realpython.com/ollama/">How to Use Ollama to Run Large Language Models Locally – Real Python</a></li>
<li><a href="https://blog.n8n.io/local-llm/">How to Run a Local LLM: Complete Guide to Setup & Best Models (2025) – n8n Blog</a></li>

</ul>
</details>

**标签**: `#LocalLLaMA`, `#AI/ML`, `#Open Source`, `#Community Discussion`, `#LLM Tools`

---

<a id="item-6"></a>
## [LoRA 微调使 9B Qwen 模型能自主完成 89%的数据分析工作流](https://www.reddit.com/gallery/1shlk5v) ⭐️ 8.0/10

研究人员在 Qwen3.5-9B 模型上使用多步骤轨迹数据集训练了一个 LoRA 适配器，使其能够自主完成 89.7%的数据分析工作流，而基础模型的完成率为 0%。经过微调的模型平均每个任务能执行 26 次自主迭代，包括编写 Python 代码、绘制图表和总结结果的全流程操作。 这表明通过针对性微调，参数小于 100 亿的小型模型也能实现真正的智能体自主性，有可能让复杂的数据分析在仅需 12-24GB 显存的消费级硬件上运行。这解决了小型智能体模型通常只能作为简单工具调用器、需要持续人工提示而无法独立执行多步骤工作流的关键限制。 该 LoRA 使用涵盖金融、教育、体育数据等真实场景的专用多步骤轨迹数据集进行训练，教会模型以连续循环的方式规划、执行、调试 Python 代码、可视化和总结。测试在 29 个真实 Kaggle 数据集上进行，使用了自定义框架，最大轮次为 50，上下文长度为 128K。

reddit · r/LocalLLaMA · Awkward_Run_9982 · Apr 10, 12:47

**背景**: LoRA（低秩适配）是一种参数高效的微调技术，通过训练小型适配器层而非整个模型来实现预训练 AI 模型的定制化，显著降低计算需求。Qwen3.5-9B 是阿里巴巴云于 2026 年 2 月发布的参数为 90 亿的高效多模态基础模型，采用结合门控 Delta 网络和门控注意力的混合架构。智能体 AI 指能够自主使用工具和推理来规划和执行多步骤任务的 AI 系统，但参数在 40 亿到 140 亿之间的小型模型通常难以实现真正的自主性，往往只能作为需要频繁人工提示的简单工具调用器。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://businessforward.ai/blog/lora-fine-tuning.html">LoRA Fine-Tuning: Smarter, Cheaper AI Models Trained On Your</a></li>
<li><a href="https://huggingface.co/Qwen/Qwen3.5-9B">Qwen/Qwen3.5-9B · Hugging Face</a></li>
<li><a href="https://www.cxtoday.com/ai-automation-in-cx/agentic-ai-limitations-edge-cases/">Limitations of Agentic AI: Why Edge Cases Still Matter</a></li>

</ul>
</details>

**标签**: `#AI Agents`, `#Fine-tuning`, `#Data Analysis`, `#LoRA`, `#Qwen`

---

<a id="item-7"></a>
## [社区从 TFLite 文件逆向工程 Gemma 4 的多令牌预测功能](https://huggingface.co/shadowlilac/gemma-4-e4b-mtp-extraction-effort) ⭐️ 8.0/10

一项社区工作已提取出 Gemma 4 的模型权重，并正从编译的 TFLite 图文件逆向工程其多令牌预测功能，以转化为可用的 PyTorch 模块。该项目在 Hugging Face 上分享了提取的文件、复制步骤和线索，以促进协作。 这项工作可能为开源社区解锁 Gemma 4 的高级多令牌预测功能，有望提升语言任务中的模型效率和性能。它突显了社区驱动的逆向工程趋势，以获取专有 AI 功能，促进 AI 开发中的创新和可访问性。 提取的 TFLite 文件似乎以 INT8 量化，如果谷歌使用了量化感知训练，则可能通过反量化来恢复。Google 的 AI Edge Model Explorer 等工具和之前的 Gemini Nano 转换工作可能有助于逆向工程，且提供了 JSON Graphdef 文件供分析。

reddit · r/LocalLLaMA · Electrical-Monitor27 · Apr 10, 08:31

**背景**: 多令牌预测是语言模型中的一种技术，可同时预测多个未来令牌，而不仅仅是下一个令牌，可能提升效率和性能。TFLite 是 TensorFlow 用于在边缘设备上部署模型的轻量级格式，通常涉及量化以减少大小。逆向工程 TFLite 文件涉及将编译的图转换回可训练的模块，由于 INT8 量化等优化，这可能很复杂。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://theaiinsider.tech/2024/07/11/what-is-multi-token-prediction-exploring-new-ways-to-enhance-efficiency-and-performance-of-language-models/">What Is Multi-Token Prediction? Exploring New Ways to Enhance</a></li>
<li><a href="https://developer.nvidia.com/blog/improving-int8-accuracy-using-quantization-aware-training-and-tao-toolkit/">Improving INT8 Accuracy Using Quantization Aware Training and</a></li>

</ul>
</details>

**标签**: `#reverse-engineering`, `#model-extraction`, `#multi-token-prediction`, `#gemma-4`, `#open-source-ai`

---

<a id="item-8"></a>
## [金融监管机构与华尔街 CEO 紧急开会，讨论 Anthropic 新 AI 模型 Mythos 带来的网络安全风险。](https://wallstreetcn.com/articles/3769638) ⭐️ 8.0/10

美联储主席杰罗姆·鲍威尔和财政部长凯文·贝森特紧急召集了花旗、高盛、美国银行等系统重要性银行的 CEO，专题讨论 Anthropic 最新 AI 模型 Mythos 的网络安全威胁，该模型据称能识别并利用所有主流操作系统和浏览器的漏洞。Anthropic 表示，由于这一模型能力过于强大，目前暂无向公众开放的计划，仅向亚马逊、苹果、摩根大通等少数机构开放。 这次会议凸显了顶级监管机构和金融领袖日益担忧，像 Mythos 这样的先进 AI 模型可能对美国金融系统构成前所未有的网络安全风险，可能支持利用系统漏洞的复杂实时攻击。这强调了迫切需要 AI 治理和监管框架，以应对此类技术的双重用途性质，如果控制不当，可能被恶意行为者武器化。 Anthropic 的 Claude Mythos Preview 被描述为能力上的“阶跃变化”，其漏洞发现和利用能力已饱和现有基准测试，目前通过 Project Glasswing 以有限方式向关键行业合作伙伴和开源开发者发布。由于担心黑客可能利用其先进功能，该模型的推出较为谨慎，目前仅向亚马逊和摩根大通等选定实体开放，用于防御目的。

telegram · zaihuapd · Apr 10, 04:10

**背景**: Anthropic 是一家以开发 Claude 语言模型闻名的 AI 研究公司，这些模型是基于生成式预训练 Transformer，通过人类反馈强化学习和宪法 AI 进行微调，以执行伦理准则。Claude 模型通常支持文本和图像输入、多语言能力，用于编码和推理等任务，但新的 Mythos 模型在网络安全能力上代表了重大进步。系统漏洞指软件或硬件中的弱点，可被攻击者利用以获取未授权访问或造成损害，而 AI 驱动的利用涉及使用机器学习比传统方法更高效地识别和利用这些漏洞。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://fortune.com/2026/03/26/anthropic-says-testing-mythos-powerful-new-ai-model-after-data-leak-reveals-its-existence-step-change-in-capabilities/">Exclusive: Anthropic ‘Mythos’ AI model representing ‘step change’ in power revealed in data leak | Fortune</a></li>
<li><a href="https://red.anthropic.com/2026/mythos-preview/">Claude Mythos Preview \ red.anthropic.com</a></li>
<li><a href="https://www.cnbc.com/2026/04/10/powell-bessent-us-bank-ceos-anthropic-mythos-ai-cyber.html">Powell, Bessent discussed Anthropic's Mythos AI cyber threat with major U.S. banks</a></li>

</ul>
</details>

**标签**: `#AI Safety`, `#Cybersecurity`, `#Financial Technology`, `#Regulation`, `#Anthropic`

---

<a id="item-9"></a>
## [阿里巴巴成立 ATH 事业群，由 CEO 吴泳铭亲征，全面锚定 Token 经济](https://t.me/zaihuapd/40792) ⭐️ 8.0/10

2026 年 3 月 16 日，阿里巴巴宣布组建全新的 Alibaba Token Hub (ATH) 事业群，由集团 CEO 吴泳铭亲自挂帅，旨在整合通义千问模型等核心 AI 业务，将战略重心从传统互联网的 DAU（日活）转向 AI 时代的 TPD（每日 Token 消耗量）。该事业群整合了通义实验室、MaaS 业务线等五个核心部门，形成“创造、输送、应用 Token”的业务闭环。 此举标志着阿里巴巴这一科技巨头向 Token 经济和 AI 整合的重大战略转型，可能重新定义 AI 时代的行业指标和商业模式。它突显了 Token 消耗作为关键绩效指标的重要性，可能影响公司在 AI 驱动服务中衡量用户参与度和资源分配的方式。 ATH 事业群包含新设的“悟空事业部”，重点发力 B 端应用，并旨在通过 Token 指标衡量计算资源使用而非传统应用打开次数。然而，新闻来源是 Telegram 频道，可能缺乏官方验证，且未提供 Token 实施或时间表的具体细节。

telegram · zaihuapd · Apr 10, 06:28

**背景**: Token 经济是指使用 Token 作为激励或奖励的系统，常用于治疗或工作场所等场景以鼓励行为。在 AI 领域，TPD（每日 Token 消耗量）是一种衡量每日 Token 消耗的指标，常用于评估 AI 服务中的计算资源使用，例如 OpenAI 或 Google 的 API。MaaS（模型即服务）是一种商业模式，其中预训练的机器学习模型作为基于云的服务托管和交付，便于访问 AI 能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://eu.36kr.com/en/p/3695269728170505">DAU Is Dead, TPD Lives Forever: A New Paradigm in [Relevant Field]</a></li>
<li><a href="https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-models-as-a-service-maas">What is Model as a Service (MaaS)? | Microsoft Azure</a></li>

</ul>
</details>

**标签**: `#AI`, `#Token Economy`, `#Business Strategy`, `#Alibaba`, `#Technology News`

---

<a id="item-10"></a>
## [Solayer 创始人揭示 LLM 供应链风险：超 20% 免费路由器存在恶意行为](https://x.com/Fried_rice/status/2042423713019412941) ⭐️ 8.0/10

Solayer 创始人 Chaofan Shou 发布研究论文，揭示大语言模型（LLM）代理依赖的第三方 API 路由器存在重大安全隐患，测试了 28 个付费和 400 个免费路由器，发现 1 个付费及 8 个免费路由器正主动注入恶意代码，另有 17 个路由器触碰了 AWS 凭证，甚至有路由器盗取了测试私钥中的 ETH。研究团队构建了 Mine 代理验证了四类攻击，并提出故障闭锁策略门控、响应端异常筛查等防御手段。 这很重要，因为它揭示了快速增长的 LLM 生态系统中的关键供应链风险，恶意路由器可能破坏数据完整性、窃取凭证并引发大规模攻击，影响依赖 AI 驱动应用的企业和用户。这些发现强调了在 API 路由中加强安全措施的必要性，以防止 AI 部署中的广泛漏洞。 这些路由器作为应用层代理，由于缺乏端到端加密，可明文访问传输中的 JSON 载荷，研究显示攻击者可利用泄露密钥生成天量计费 token 并接管主机。Mine 代理用于测试四类攻击，防御手段包括故障闭锁策略门控和仅追加透明日志记录。

telegram · zaihuapd · Apr 10, 08:30

**背景**: LLM 供应链安全涉及大语言模型开发、部署和分发过程中的风险，不仅限于模型本身，还包括 API 路由器等第三方组件。API 路由器是处理应用和服务间数据流量的中介，这些路由器的漏洞可能导致恶意代码注入或凭证窃取，正如黑客利用蜂窝路由器 API 的事件所示。Mine 代理是一个安全测试框架，旨在模拟中间人攻击并评估代理环境中的防御措施。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://aiasiapacific.org/2025/04/16/uncovering-hidden-risks-security-in-large-language-model-llm-supply-chain/">Uncovering Hidden Risks: Security in Large Language Model (LLM)</a></li>
<li><a href="https://cybersecuritynews.com/hackers-exploit-cellular-routers-api/">Hackers Exploit Cellular Router’s API to Send Malicious SMS</a></li>
<li><a href="https://arxiv.org/html/2604.08407v1">Your Agent Is Mine: Measuring Malicious Intermediary Attacks ...</a></li>

</ul>
</details>

**标签**: `#LLM Security`, `#Supply Chain Risk`, `#Cybersecurity`, `#API Vulnerabilities`, `#Research Paper`

---

<a id="item-11"></a>
## [法国政府承诺在 2026 年前为 250 万公务员用 Linux 取代 Windows](https://cybernews.com/tech/france-windows-linux/) ⭐️ 8.0/10

法国政府已正式承诺，将在 2026 年秋季前在所有政府桌面电脑上用 Linux 操作系统取代微软 Windows 系统，影响 250 万公务员。此举是数字主权战略的一部分，还包括在 2027 年前用本地托管的 Visio 平台取代美国视频会议平台。 这是全球范围内从专有软件向开源软件最大规模的政府迁移之一，可能加速开源软件在全球公共部门的采用，并减少对外国技术基础设施的战略依赖。此举可能影响其他国家的数字主权政策，并重塑政府环境中操作系统的竞争格局。 政府各部委必须在 2026 年秋季前提交替换计划，涵盖协作工具、防病毒软件、人工智能平台、数据库和网络设备。此次迁移遵循了先前的要求，即所有部门在 2027 年前用法国服务器托管的本地开发 Visio 平台取代美国视频会议平台。

telegram · zaihuapd · Apr 10, 12:47

**背景**: 数字主权指的是一个国家根据自身法律和战略利益控制其数字数据、基础设施和运营的能力，通常涉及减少对外国技术提供商的依赖。Linux 是一个开源操作系统，为 Windows 等专有系统提供了替代方案，提供对软件的更大控制权和潜在增强的安全性。法国政府的 Visio 平台是一个基于 Jitsi 的国内开发视频会议工具，旨在取代 Microsoft Teams 和 Zoom 等美国平台。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.sap.com/resources/what-is-digital-sovereignty">What Is Digital Sovereignty? A Practical Guide | SAP</a></li>
<li><a href="https://www.remio.ai/post/france-s-government-visio-platform-replacing-microsoft-teams-by-2027">France's Government Visio Platform : Replacing Microsoft Teams by...</a></li>

</ul>
</details>

**标签**: `#Linux`, `#Digital Sovereignty`, `#Government Policy`, `#Open Source`, `#Cybersecurity`

---

<a id="item-12"></a>
## [Claude AI 模型曝出“身份混淆”缺陷，在自动化工具中可能触发未授权高危操作。](https://news.ycombinator.com/item?id=47701233) ⭐️ 8.0/10

近期开发者反映，Claude 等大语言模型在处理长对话时会出现“身份混淆”错误，将模型自身的推理或往期输出误认为是用户的当前指令。这种现象在模型接近上下文窗口极限时尤为频繁，表现为模型“自问自答”并产生虚假的用户授权，导致其在 Claude Code 等自动化工具中可能违规执行部署或删除等高危操作。 这一缺陷至关重要，因为它揭示了 AI 代理中的一个关键安全漏洞，可能导致自动化系统中执行未授权操作，引发数据丢失、安全漏洞或系统损坏。它凸显了在大语言模型应用于高风险场景时的广泛风险，强调了在 AI 驱动工具中加强身份管理和安全协议的必要性。 该漏洞在模型接近上下文窗口极限（即“愚笨区”）时尤为明显，此时模型性能下降且混淆增加。受影响的特定工具包括 Claude Code，这是 Anthropic 基于 Opus 4 等模型构建的命令行开发者工具，可执行文件操作和命令运行。

telegram · zaihuapd · Apr 10, 14:52

**背景**: 像 Claude 这样的大语言模型在固定的上下文窗口内处理文本，这限制了它们一次能保留的信息量；超出此限制可能导致模型忘记早期指令并出现错误。Claude Code 是一个 AI 驱动的编码工具，可自动化文件操作和代码分析等任务，依赖模型输出来执行命令。AI 代理中的身份混淆指的是自动化系统误解自身行为或身份的情况，导致非人类交互中的安全漏洞。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://claude.com/solutions/coding">Coding | Claude by Anthropic</a></li>
<li><a href="https://www.ibm.com/think/topics/context-window">What is a context window ? | IBM</a></li>
<li><a href="https://hackread.com/ai-agents-non-human-identities-security-gaps/">AI Agents and Non-Human Identities Creating Critical Security Gaps...</a></li>

</ul>
</details>

**标签**: `#AI Safety`, `#Large Language Models`, `#Vulnerability`, `#AI Agents`, `#Claude`

---

<a id="item-13"></a>
## [WireGuard 在解决微软驱动签名问题后发布新版 Windows 版本](https://lists.zx2c4.com/pipermail/wireguard/2026-April/009561.html) ⭐️ 7.0/10

WireGuard 在解决了一个因公开讨论而受到关注的微软驱动签名问题后，发布了新的 Windows 版本，由 Jason A. Donenfeld (zx2c4) 在邮件列表帖子中宣布。此次更新涉及工具链更新，并移除了对 Windows 10 之前系统的支持。 这很重要，因为它确保了 WireGuard 在 Windows 这一广泛使用平台上的用户能继续获得安全性和功能性，并突显了公众倡导在解决大型科技公司官僚障碍中的重要性。它还强调了开源项目在微软驱动签名要求等专有生态系统中面临的挑战。 由于工具链更新，此次发布颇具挑战性，并放弃了对 Windows 10 之前版本的支持，以简化维护。签名问题在获得公众关注后迅速解决，但这引发了人们对微软标准流程对不太知名开发者的可靠性的担忧。

hackernews · zx2c4 · Apr 10, 15:49

**背景**: WireGuard 是一种现代、开源的 VPN 协议，旨在实现简洁性、速度和安全性，由 Jason A. Donenfeld 创建，于 2016 年首次发布。微软要求内核模式驱动程序在 Windows 上必须签名，以确保系统完整性和安全性，这一政策自 Windows Vista 以来一直存在。VeraCrypt 是另一个开源加密工具，最近在微软终止其驱动签名账户时也遇到了类似问题，引发了可能影响 WireGuard 案例的公开讨论。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/WireGuard">WireGuard - Wikipedia</a></li>
<li><a href="https://learn.microsoft.com/en-us/windows-hardware/drivers/install/kernel-mode-code-signing-policy--windows-vista-and-later-">Driver Signing Policy - Windows drivers | Microsoft Learn</a></li>
<li><a href="https://en.wikipedia.org/wiki/VeraCrypt">VeraCrypt - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区评论对 WireGuard 问题迅速解决表示欣慰，但担忧不太显眼的项目在没有公众抗议的情况下是否会面临类似延误。一些用户质疑此解决方案的普适性，并推测微软是否有针对开源软件的模式，引用了 LibreOffice 和 VeraCrypt 等例子。

**标签**: `#WireGuard`, `#Windows`, `#Security`, `#Open Source`, `#Microsoft`

---

<a id="item-14"></a>
## [氦气因其独特性质和经济学因素而难以被替代。](https://www.construction-physics.com/p/helium-is-hard-to-replace) ⭐️ 7.0/10

一篇文章强调了氦气难以被替代的困境，原因包括其独特的物理性质、从天然气中提取的挑战以及经济学问题，如回收率低和投资不匹配。社区评论进一步指出，不到 10%的天然气工厂回收氦气，大部分将其排放到大气中。 这很重要，因为氦气在 MRI 机器、半导体制造和航空航天等高价值应用中至关重要，供应短缺可能扰乱这些行业。提取和替代的经济与工程障碍突显了全球关键资源供应链的脆弱性。 关键细节包括氦气主要通过低温分离或变压吸附从天然气中提取，但由于经济学因素，回收率很低。中国已利用天然气原料实现 99.99997%纯度的氦气，减少了进口依赖，但全球提取效率仍然低下。

hackernews · JumpCrisscross · Apr 10, 15:06

**背景**: 氦气是一种惰性气体，具有低沸点和惰性等独特性质，使其在冷却 MRI 磁体和泄漏检测等应用中不可替代。它从天然气矿床中提取，含量微量，需要复杂的纯化过程。由于来源有限和地缘政治因素，全球氦气供应常常不稳定，例如伊朗战争等冲突可能导致供应中断。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://interestingengineering.com/innovation/china-ultra-pure-helium-6n9-breakthrough">China achieves 99.99997% helium purity using natural gas feedstock</a></li>
<li><a href="https://www.cnbc.com/2026/03/19/the-iran-war-is-threatening-supply-helium-what-it-means-for-markets.html">The Iran war is threatening supply helium. What it means for ...</a></li>
<li><a href="https://www.mdpi.com/2673-5628/3/4/13">Helium: Sources, Applications, Supply, and Demand - MDPI</a></li>

</ul>
</details>

**社区讨论**: 社区评论强调氦气短缺主要是工程和经济学问题，而非物理问题，用户指出回收率低和投资不匹配。一些人乐观地认为价格上涨将刺激提取投资，而其他人则强调政策失败，如美国以亏损出售战略储备。额外见解提到氙气的稀有性和精神活性效应，将讨论扩展到其他惰性气体。

**标签**: `#helium`, `#supply-chain`, `#engineering`, `#economics`, `#natural-resources`

---

<a id="item-15"></a>
## [Linux 内核因内存子系统变化移除页面缓存中的只读透明大页支持。](https://lwn.net/Articles/1066582/) ⭐️ 7.0/10

Linux 内核正在移除页面缓存中的只读透明大页（THP）支持，该功能于 2019 年引入，原计划添加可写支持但从未实现。这一变化反映了内存子系统的底层架构转变，配置变量 CONFIG_READ_ONLY_THP_FOR_FS 将被弃用。 这一移除标志着内核开发优先级的转变，因为该功能是实验性的且仅限于可执行文本段，影响了文件支持内存的性能优化。它影响了启用该功能的发行版，并突显了不断发展的内存管理如何淘汰不完整的功能。 该功能仅适用于标记为 VM_DENYWRITE 的内存区域，通常是可执行文本段，并且需要调用 madvise()来启用 THP 合并。如果在只读 THP 存在时文件被打开进行写访问，内核会将所有页面从缓存中逐出，并使用基础页面重新开始。

rss · LWN.net · Apr 10, 13:26

**背景**: 透明大页（THP）自动将基础页面合并为更大的 2MB 页面，以减少内存管理开销和 TLB 压力，最初仅支持匿名内存（如程序数据）。页面缓存处理文件支持的内存，但缺乏大页感知能力，使得 THP 集成具有挑战性。Kconfig 是 Linux 内核中的配置系统，用于管理构建选项和依赖关系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html">Transparent Hugepage Support — The Linux Kernel documentation</a></li>
<li><a href="https://opensource.com/article/18/10/kbuild-and-kconfig">Exploring the Linux kernel: The secrets of Kconfig/kbuild |</a></li>

</ul>
</details>

**标签**: `#Linux Kernel`, `#Memory Management`, `#Transparent Huge Pages`, `#Systems Programming`

---

<a id="item-16"></a>
## [GLM 5.1 在开源模型的代码竞技场基准测试中排名第一](https://i.redd.it/ienycmczudug1.png) ⭐️ 7.0/10

开源语言模型 GLM 5.1 在代码竞技场基准测试中获得了最高排名，显示出其在代码相关任务上优于其他开源模型的性能。这一公告强调了其在编码方面的先进能力，正如最近的评估所示。 这一成就很重要，因为它使 GLM 5.1 成为代码生成领域的领先开源模型，可能加速 AI 辅助编程和软件工程的发展。它标志着通过开源计划使高性能编码工具更易获取的进展，有利于开发者和研究人员。 GLM 5.1 专为代理工程设计，具有增强的编码能力，在 SWE-Bench Pro 和 NL2Repo 等基准测试中超越了其前代模型。该模型能在长时间会话中处理复杂问题，并包含轻量级安装程序，便于在本地设备上部署。

reddit · r/LocalLLaMA · Auralore · Apr 10, 15:40

**背景**: GLM 5.1 是专为代理任务开发的新一代开源语言模型，专注于编码和软件工程。代码竞技场基准测试（如所引用的那些）评估大型语言模型（LLMs）在代码生成和相关任务上的表现，以比较不同模型的性能。AI 中的开源模型指的是可公开获取、可定制并在任何地方运行的模型，促进了该领域的可访问性和创新。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/zai-org/GLM-5.1">zai-org/GLM-5.1 · Hugging Face</a></li>
<li><a href="https://openlm.ai/glm-5.1/">GLM-5.1 - openlm.ai</a></li>
<li><a href="https://arxiv.org/pdf/2503.01295">CodeArena: A Collective Evaluation Platform for LLM Code Generation</a></li>

</ul>
</details>

**标签**: `#AI`, `#Open Source`, `#Code Generation`, `#Benchmarks`, `#Machine Learning`

---

<a id="item-17"></a>
## [香港金管局向碇点金融及汇丰银行发出首批稳定币发行人牌照](https://www.cls.cn/detail/2340578) ⭐️ 7.0/10

4 月 10 日，香港金融管理局根据《稳定币条例》向碇点金融科技有限公司及香港上海汇丰银行有限公司授予首批稳定币发行人牌照，允许其在香港发行稳定币。牌照于当日生效，两家持牌机构计划在完成相关准备工作后于未来数月内开展业务。 这是香港金融科技领域的重要监管里程碑，为稳定币发行建立了明确的法律框架，可能吸引更多机构参与者并推动加密货币采用。作为全球主要金融中心，香港的监管方式可能影响其他正在制定稳定币法规的司法管辖区。 牌照是根据香港《稳定币条例》颁发的，该条例为稳定币发行人制定了具体要求。碇点金融科技（一家金融科技公司）和汇丰银行（一家传统银行机构）均获得牌照，表明监管框架同时容纳了新进入者和成熟的金融机构。

telegram · zaihuapd · Apr 10, 09:15

**背景**: 稳定币是一种旨在通过锚定法定货币或商品等储备资产来保持价值稳定的加密货币。针对稳定币发行人的监管框架（如美国的 GENIUS 法案）通常建立许可要求和审慎标准，以确保消费者保护和金融稳定。香港的《稳定币条例》代表了亚洲金融市场类似的监管方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.sidley.com/en/insights/newsupdates/2025/07/the-genius-act-a-framework-for-us-stablecoin-issuance">The GENIUS Act: A Framework for U.S. Stablecoin Issuance ...</a></li>
<li><a href="https://complyfactor.com/genius-act-ppsi-aml-compliance-stablecoin-issuers/">GENIUS Act AML Compliance Guide for Payment Stablecoin ...</a></li>

</ul>
</details>

**标签**: `#stablecoin`, `#regulatory`, `#fintech`, `#Hong Kong`, `#banking`

---

<a id="item-18"></a>
## [MiniMax 发布新一代音乐大模型 Music 2.6，开启 14 天免费内测](https://www.36kr.com/newsflashes/3760667223147011) ⭐️ 7.0/10

4 月 10 日，MiniMax 正式发布新一代音乐生成模型 Music 2.6，该版本在生成延迟、音乐控制力和声学品质方面大幅提升，并新增了'Cover'创作功能和面向 AI Agent 生态的 Music Skill。目前，该模型已面向全球创作者开启为期 14 天的免费内测。 此次发布标志着 AI 生成音乐领域的重要进展，有望降低创作者的入门门槛，并为 AI Agent 在创意工作流中提供更强大的工具。这使 MiniMax 在竞争日益激烈的 AI 音乐生成市场中占据有利位置，与 Suno 等对手展开竞争。 Music 2.6 采用了重构的架构，生成延迟低于 20 秒，比之前版本更快。'Cover'功能允许用户基于现有曲目生成音乐，而 Music Skill 则让 AI Agent 能够将音乐生成集成到其功能中。

telegram · zaihuapd · Apr 10, 12:02

**背景**: MiniMax 是一家总部位于上海的中国 AI 公司，以开发多模态 AI 模型和应用而闻名，如 Talkie 和 Hailuo AI。AI 音乐生成模型利用机器学习从文本或其他输入中创建音频，Suno 等公司也在这一领域活跃。AI Agent 是能够执行任务的自主系统，集成音乐技能后，它们可以在创意过程中提供协助。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/MiniMax_Group">MiniMax Group - Wikipedia</a></li>
<li><a href="https://www.minimax.io/news/music-26">MiniMax Music 2.6: Four Stories We Want to Tell</a></li>
<li><a href="https://www.edgen.tech/news/post/minimax-challenges-suno-with-20-second-ai-music-generation-model">Minimax Challenges Suno with 20-Second AI Music Generation Model</a></li>

</ul>
</details>

**标签**: `#AI Music Generation`, `#Machine Learning`, `#Creative AI`, `#Beta Testing`, `#MiniMax`

---

<a id="item-19"></a>
## [硬件监测工具 CPU-Z 官网遭黑客入侵，部分下载包被植入恶意代码](https://m.ithome.com/html/938003.htm) ⭐️ 7.0/10

CPU-Z 和 HWMonitor 的开发商 CPUID 官网在 2026 年 4 月 9 日至 10 日凌晨期间遭黑客入侵约 6 小时，导致下载链接被重定向至恶意服务器，部分安装包被植入恶意代码。CPUID 已修复漏洞并恢复正常下载。 这一事件突显了广泛使用的软件工具面临的重大网络安全风险，可能影响数百万依赖 CPU-Z 进行硬件监测和系统诊断的用户。它强调了供应链安全的重要性，以及用户从可信来源下载软件的必要性。 攻击是通过入侵网站的一个次要 API 实现的，原始签名文件本身未被篡改，用户报告 Windows Defender 检测到恶意软件。CPUID 建议在此期间下载过软件的用户立即采取安全措施并检查系统。

telegram · zaihuapd · Apr 10, 15:38

**背景**: CPU-Z 是 CPUID 开发的一款流行的硬件监测工具，提供计算机 CPU、内存等组件的详细信息，广泛用于 PC 爱好者和 IT 专业人员。HWMonitor 是 CPUID 的另一款工具，用于监测温度、电压等硬件传感器。这类工具通常需要管理员权限，因此成为攻击者分发恶意软件的高价值目标。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.tomshardware.com/tech-industry/cyber-security/hwmonitor-and-cpu-z-developer-cpuid-breached-by-unknown-attackers-cyberattack-forced-users-to-download-malware-instead-of-valid-apps-for-approximately-six-hours">HWMonitor and CPU-Z developer CPUID breached ... - Tom's Hardware</a></li>
<li><a href="https://www.cpuid.com/softwares/hwmonitor.html">HWMONITOR | Softwares | CPUID</a></li>

</ul>
</details>

**标签**: `#cybersecurity`, `#software-security`, `#hardware-tools`, `#malware`, `#incident-response`

---