---
layout: default
title: "Horizon Summary: 2026-04-11 (EN)"
date: 2026-04-11
lang: en
---

> From 38 items, 19 important content pieces were selected

---

1. [DeepSeek V4 flagship LLM to launch in late April 2026 with deep adaptation to domestic chips](#item-1) ⭐️ 9.0/10
2. [cuBLAS Performance Bug Causes 60% Inefficiency in Batched FP32 Matrix Multiplication on RTX 5090](#item-2) ⭐️ 8.0/10
3. [GLM 5.1 achieves near-Opus performance at one-third the cost in agentic benchmarks.](#item-3) ⭐️ 8.0/10
4. [National University of Singapore Introduces DMax for Aggressive Parallel Decoding in Diffusion Language Models](#item-4) ⭐️ 8.0/10
5. [Community overview of the local LLM landscape, tools, and developments](#item-5) ⭐️ 8.0/10
6. [LoRA fine-tuning enables 9B Qwen model to autonomously complete 89% of data analysis workflows](#item-6) ⭐️ 8.0/10
7. [Community reverse-engineers Gemma 4's multi-token prediction from TFLite files](#item-7) ⭐️ 8.0/10
8. [Financial regulators and Wall Street CEOs hold emergency meeting on cybersecurity risks from Anthropic's new AI model Mythos.](#item-8) ⭐️ 8.0/10
9. [Alibaba Forms ATH Business Group Led by CEO Wu Yongming to Focus on Token Economy](#item-9) ⭐️ 8.0/10
10. [Solayer Founder Exposes LLM Supply Chain Risks: Over 20% of Free Routers Engage in Malicious Activities](#item-10) ⭐️ 8.0/10
11. [French government commits to replacing Windows with Linux for 2.5 million civil servants by 2026](#item-11) ⭐️ 8.0/10
12. [Claude AI models exhibit 'identity confusion' vulnerability, risking unauthorized high-risk operations in automated tools.](#item-12) ⭐️ 8.0/10
13. [WireGuard releases new Windows version after resolving Microsoft driver signing issue](#item-13) ⭐️ 7.0/10
14. [Helium faces replacement challenges due to unique properties and economic factors.](#item-14) ⭐️ 7.0/10
15. [Linux kernel removes read-only transparent huge pages for page cache due to memory subsystem changes.](#item-15) ⭐️ 7.0/10
16. [GLM 5.1 ranks first in code arena benchmarks for open models](#item-16) ⭐️ 7.0/10
17. [Hong Kong issues first stablecoin issuer licenses to Anchor Financial and HSBC](#item-17) ⭐️ 7.0/10
18. [MiniMax releases Music 2.6, a new music generation model with 14-day free beta](#item-18) ⭐️ 7.0/10
19. [CPU-Z official website hacked, malicious code inserted into download packages](#item-19) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [DeepSeek V4 flagship LLM to launch in late April 2026 with deep adaptation to domestic chips](https://finance.sina.com.cn/tech/2026-04-10/doc-inhtymqf5317301.shtml) ⭐️ 9.0/10

DeepSeek founder Liang Wenfeng announced internally that the DeepSeek V4 flagship large language model, featuring trillion-scale parameters and million-token context, will be officially released in late April 2026. The model marks the first deep adaptation to domestic chips like Huawei Ascend, driving pre-orders from tech giants and AI chip price increases of about 20%. This represents a significant milestone in China's AI independence from NVIDIA's CUDA ecosystem, reducing reliance on foreign technology. The deep chip adaptation could accelerate domestic AI infrastructure development and reshape global AI chip market dynamics, as evidenced by increased demand and pricing. The model is reportedly a Mixture-of-Experts (MoE) architecture with 1 trillion parameters, making it one of the largest open MoE models to date. DeepSeek has already launched 'Fast Mode' and 'Expert Mode' on its web platform to prepare users for the new model's capabilities.

telegram · zaihuapd · Apr 10, 05:16

**Background**: DeepSeek is a Chinese AI company that develops large language models, with DeepSeek V4 being its upcoming flagship model featuring trillion-scale parameters. Huawei Ascend is a series of AI chips designed for data centers, with the Ascend 910 using 7nm technology and aiming to compete with NVIDIA's offerings. CUDA is NVIDIA's parallel computing platform that dominates the AI chip market, creating dependency concerns that have spurred efforts to develop alternatives like chipStar and other open standards.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek - Wikipedia</a></li>
<li><a href="https://macaron.im/nn/blog/deepseek-v4-moe-1-trillion">DeepSeek - V 4 MoE: The 1-Trillion Parameter Breakthrough - Macaron</a></li>
<li><a href="https://hardforum.com/threads/huawei-announces-ascend-ai-chips.1969505/">Huawei Announces Ascend AI Chips | [H]ard|Forum</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Large Language Models`, `#Chip Technology`, `#Industry News`, `#China Tech`

---

<a id="item-2"></a>
## [cuBLAS Performance Bug Causes 60% Inefficiency in Batched FP32 Matrix Multiplication on RTX 5090](https://www.reddit.com/r/MachineLearning/comments/1shtv0r/d_60_matmul_performance_bug_in_cublas_on_rtx_5090/) ⭐️ 8.0/10

A performance bug in NVIDIA's cuBLAS library causes approximately 60% inefficiency in batched FP32 matrix multiplication on the RTX 5090 GPU, as demonstrated by benchmarks showing custom kernels outperforming cuBLAS by up to 170% for certain matrix sizes. The issue was tested with CUDA 13.2.51, cuBLAS 13.3.0, and driver 595.58.03, and likely affects all non-Pro RTX GPUs. This bug significantly impacts machine learning and scientific computing workloads that rely on batched matrix multiplications, potentially slowing down training and inference on widely used RTX GPUs. It highlights potential optimization disparities in NVIDIA's software stack, where non-Pro GPUs may receive less attention compared to professional or data center models like the H200. The bug causes cuBLAS to dispatch an inefficient kernel for batched FP32 workloads from 256×256 to 8192×8192×8, using only about 40% of available compute on RTX GPUs. In contrast, other GPUs like the Pro 6000 and H200 use more optimized kernels, with the H200 achieving up to 82% FMA utilization through mixed CUTLASS and xmma families.

reddit · r/MachineLearning · NoVibeCoding · Apr 10, 17:51

**Background**: cuBLAS is NVIDIA's CUDA Basic Linear Algebra Subprograms library, optimized for GPU-accelerated matrix operations like GEMM (General Matrix Multiply), which are fundamental in deep learning and high-performance computing. Batched matrix multiplication processes multiple matrices simultaneously, improving throughput for tasks such as neural network training. FMA (Fused Multiply-Add) is a key GPU instruction that combines multiplication and addition in one step, enhancing performance and accuracy in numerical computations.

<details><summary>References</summary>
<ul>
<li><a href="https://developer.nvidia.com/blog/new-cublas-12-0-features-and-matrix-multiplication-performance-on-nvidia-hopper-gpus/">New cuBLAS 12.0 Features and Matrix Multiplication Performance</a></li>
<li><a href="https://en.wikipedia.org/wiki/Multiply–accumulate_operation">Multiply–accumulate operation - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#GPU`, `#cuBLAS`, `#Performance`, `#Machine Learning`, `#NVIDIA`

---

<a id="item-3"></a>
## [GLM 5.1 achieves near-Opus performance at one-third the cost in agentic benchmarks.](https://www.reddit.com/r/LocalLLaMA/comments/1shus54/glm_51_crushes_every_other_model_except_opus_in/) ⭐️ 8.0/10

GLM 5.1, a large language model from Zhipu AI, has been tested in an agentic benchmark using OpenClaw and achieved performance comparable to Opus 4.6 while costing only about $0.4 per run versus Opus's $1.2. It outperformed all other models tested, establishing itself as a top choice for agentic tasks like those on OpenClaw. This breakthrough significantly advances cost-effectiveness in agentic AI, making high-performance models more accessible for real-world applications like autonomous assistants and complex task automation. It challenges the dominance of expensive models like Opus and could accelerate adoption of open-source or lower-cost alternatives in the AI agent ecosystem. The testing methodology used OpenClaw in a real environment with user-submitted tasks, employing an LLM-as-a-judge approach similar to Chatbot Arena to avoid static benchmark optimization issues. Qwen 3.6 also performed well but currently lacks prompt caching support on OpenRouter, which inflates its price; with caching, it could reach cost levels similar to minimax m2.7.

reddit · r/LocalLLaMA · zylskysniper · Apr 10, 18:23

**Background**: GLM 5.1 is the most powerful model in the GLM series developed by Zhipu AI, designed for complex systems engineering and long-horizon agentic tasks. OpenClaw is a free, open-source autonomous AI agent that executes tasks via LLMs, using messaging platforms as its interface. Agentic benchmarks differ from classical ML benchmarks by emphasizing multi-step interaction, environment manipulation, and outcome verification in real scenarios, often using LLM-as-a-Judge methods for evaluation.

<details><summary>References</summary>
<ul>
<li><a href="https://cookbook.sglang.io/autoregressive/GLM/GLM-5">GLM-5 | SGLang Cookbook</a></li>
<li><a href="https://en.wikipedia.org/wiki/OpenClaw">OpenClaw - Wikipedia</a></li>
<li><a href="https://www.emergentmind.com/topics/agentic-benchmarks">Agentic Benchmarks</a></li>

</ul>
</details>

**Tags**: `#AI Agents`, `#Benchmarking`, `#Cost Efficiency`, `#Large Language Models`, `#Open Source AI`

---

<a id="item-4"></a>
## [National University of Singapore Introduces DMax for Aggressive Parallel Decoding in Diffusion Language Models](https://v.redd.it/buzbtk1hdeug1) ⭐️ 8.0/10

Researchers from the National University of Singapore presented DMax, a new paradigm for diffusion language models (dLLMs) that enables aggressive parallel decoding by mitigating error accumulation through progressive self-refinement and on-policy uniform training. This approach reformulates decoding as a progressive transition from mask embeddings to token embeddings, allowing the model to correct its own erroneous predictions during generation. This advancement is significant because it addresses a key bottleneck in language model efficiency by enabling faster, parallel decoding while maintaining generation quality, potentially accelerating applications like code generation and reasoning tasks. It represents a shift in how diffusion models handle text generation, moving beyond sequential or binary mask-based approaches to improve scalability and performance in AI systems. DMax improves throughput per forward pass (TPF) significantly, increasing from 2.04 to 5.47 on GSM8K and from 2.71 to 5.86 on MBPP while preserving accuracy, and achieves an average of 1,338 tokens per second on two H200 GPUs at batch size 1. The method relies on soft parallel decoding, which represents intermediate states as interpolations between predicted token embeddings and mask embeddings to enable iterative self-revising.

reddit · r/LocalLLaMA · 44th--Hokage · Apr 10, 17:23

**Background**: Diffusion language models (dLLMs) are a class of AI models that generate text through a noise-to-text transformation process, similar to image diffusion models like DALL-E, offering an alternative to autoregressive models that predict tokens sequentially. Parallel decoding aims to accelerate text generation by processing multiple tokens simultaneously, but it often faces challenges like error accumulation in diffusion models, where mistakes can propagate and degrade output quality. The DMax approach builds on these concepts by introducing progressive self-refinement to mitigate such errors, as detailed in related surveys and resources on diffusion language models.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2508.10875">[2508.10875] A Survey on Diffusion Language Models - arXiv.org</a></li>
<li><a href="https://huggingface.co/blog/ProCreations/diffusion-language-model">Diffusion Language Models: The New Paradigm - Hugging Face</a></li>
<li><a href="https://arxiv.org/html/2509.25188v1">Learning to Parallel: Accelerating Diffusion Large Language</a></li>

</ul>
</details>

**Tags**: `#diffusion-models`, `#language-models`, `#parallel-decoding`, `#AI-research`, `#machine-learning`

---

<a id="item-5"></a>
## [Community overview of the local LLM landscape, tools, and developments](https://i.redd.it/6jxe6recjaug1.png) ⭐️ 8.0/10

A community-driven overview titled 'the state of LocalLLama' was shared, providing insights into the current landscape, tools, and developments for running large language models locally, based on high engagement with 1390 upvotes and a 98% upvote ratio. This overview synthesizes community knowledge on hardware, optimization techniques, and popular models like Mistral 7B, Llama 3, and Mixtral 8x7B. This matters because it highlights the growing trend of running LLMs locally for privacy, cost-effectiveness, and control, empowering developers and enthusiasts to leverage open-source models without relying on cloud APIs. It reflects the democratization of AI, enabling more people to experiment with and deploy advanced language models on consumer hardware. Key details include the focus on tools like Ollama and LM Studio for local deployment, optimization for hardware such as NVIDIA RTX 4090s and Apple Silicon, and the use of open-weights models like Mistral 7B and Llama 3. The overview is community-driven, emphasizing practical guidance and real-world applications rather than theoretical research.

reddit · r/LocalLLaMA · Beginning-Window-115 · Apr 10, 04:30

**Background**: LocalLLaMA is a community project centered on running large language models locally, often through subreddits and guides that discuss tools, hardware, and optimization techniques. Running LLMs locally involves using open-source frameworks and tools to execute models on personal computers or servers, bypassing cloud services for increased privacy and reduced costs. This trend has gained momentum with the availability of powerful consumer hardware and efficient model architectures, enabling broader access to AI capabilities.

<details><summary>References</summary>
<ul>
<li><a href="https://localllamma.pro/">LocalLLaMA - The Underground Guide to Local AI</a></li>
<li><a href="https://realpython.com/ollama/">How to Use Ollama to Run Large Language Models Locally – Real Python</a></li>
<li><a href="https://blog.n8n.io/local-llm/">How to Run a Local LLM: Complete Guide to Setup & Best Models (2025) – n8n Blog</a></li>

</ul>
</details>

**Tags**: `#LocalLLaMA`, `#AI/ML`, `#Open Source`, `#Community Discussion`, `#LLM Tools`

---

<a id="item-6"></a>
## [LoRA fine-tuning enables 9B Qwen model to autonomously complete 89% of data analysis workflows](https://www.reddit.com/gallery/1shlk5v) ⭐️ 8.0/10

A researcher trained a LoRA adapter on multi-step trace datasets for the Qwen3.5-9B model, enabling it to autonomously complete 89.7% of data analysis workflows without human intervention, compared to 0% completion by the base model. The fine-tuned model averages 26 autonomous iterations per task, writing Python code, plotting charts, and summarizing results end-to-end. This demonstrates that small models under 10B parameters can achieve true agentic autonomy through targeted fine-tuning, potentially making sophisticated data analysis accessible on consumer-grade hardware with 12-24GB VRAM. It addresses a key limitation where small agentic models typically function as simple tool-callers requiring constant human prompting rather than executing multi-step workflows independently. The LoRA was trained on specialized multi-step trace datasets covering real-world scenarios like finance, education, and sports data, teaching the model to plan, execute, debug Python code, visualize, and summarize in continuous loops. Testing was conducted on 29 real Kaggle datasets using a custom framework with max_turns=50 and 128K context length.

reddit · r/LocalLLaMA · Awkward_Run_9982 · Apr 10, 12:47

**Background**: LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning technique that enables customization of pre-trained AI models by training small adapter layers rather than the entire model, significantly reducing computational requirements. Qwen3.5-9B is Alibaba Cloud's efficient multimodal foundation model with 9 billion parameters, released in February 2026, featuring a hybrid architecture combining Gated Delta Networks and Gated Attention. Agentic AI refers to AI systems that can autonomously plan and execute multi-step tasks using tools and reasoning, but small models in the 4B-14B range often struggle with true autonomy, typically functioning as simple tool-callers that require frequent human prompting.

<details><summary>References</summary>
<ul>
<li><a href="https://businessforward.ai/blog/lora-fine-tuning.html">LoRA Fine-Tuning: Smarter, Cheaper AI Models Trained On Your</a></li>
<li><a href="https://huggingface.co/Qwen/Qwen3.5-9B">Qwen/Qwen3.5-9B · Hugging Face</a></li>
<li><a href="https://www.cxtoday.com/ai-automation-in-cx/agentic-ai-limitations-edge-cases/">Limitations of Agentic AI: Why Edge Cases Still Matter</a></li>

</ul>
</details>

**Tags**: `#AI Agents`, `#Fine-tuning`, `#Data Analysis`, `#LoRA`, `#Qwen`

---

<a id="item-7"></a>
## [Community reverse-engineers Gemma 4's multi-token prediction from TFLite files](https://huggingface.co/shadowlilac/gemma-4-e4b-mtp-extraction-effort) ⭐️ 8.0/10

A community effort has extracted Gemma 4's model weights and is now reverse-engineering its multi-token prediction (MTP) feature from compiled TFLite graph files into usable PyTorch modules. The project includes extracted files, replication steps, and clues shared on Hugging Face to facilitate collaboration. This effort could unlock Gemma 4's advanced MTP capability for the open-source community, potentially improving model efficiency and performance in language tasks. It highlights the growing trend of community-driven reverse engineering to access proprietary AI features, fostering innovation and accessibility in AI development. The extracted TFLite files appear to be quantized in INT8, suggesting possible salvage through de-quantization if Google used quantization-aware training (QAT). Tools like Google's AI Edge Model Explorer and prior Gemini Nano conversion efforts may aid the reverse engineering, with a JSON Graphdef file available for analysis.

reddit · r/LocalLLaMA · Electrical-Monitor27 · Apr 10, 08:31

**Background**: Multi-token prediction (MTP) is a technique in language models that predicts multiple future tokens simultaneously, rather than just the next token, potentially enhancing efficiency and performance. TFLite is TensorFlow's lightweight format for deploying models on edge devices, often involving quantization to reduce size. Reverse engineering TFLite files involves converting compiled graphs back to trainable modules, which can be complex due to optimizations like INT8 quantization.

<details><summary>References</summary>
<ul>
<li><a href="https://theaiinsider.tech/2024/07/11/what-is-multi-token-prediction-exploring-new-ways-to-enhance-efficiency-and-performance-of-language-models/">What Is Multi-Token Prediction? Exploring New Ways to Enhance</a></li>
<li><a href="https://developer.nvidia.com/blog/improving-int8-accuracy-using-quantization-aware-training-and-tao-toolkit/">Improving INT8 Accuracy Using Quantization Aware Training and</a></li>

</ul>
</details>

**Tags**: `#reverse-engineering`, `#model-extraction`, `#multi-token-prediction`, `#gemma-4`, `#open-source-ai`

---

<a id="item-8"></a>
## [Financial regulators and Wall Street CEOs hold emergency meeting on cybersecurity risks from Anthropic's new AI model Mythos.](https://wallstreetcn.com/articles/3769638) ⭐️ 8.0/10

Federal Reserve Chair Jerome Powell and Treasury Secretary Kevin Bessent urgently convened CEOs of systemically important banks, including Citigroup, Goldman Sachs, and Bank of America, to discuss cybersecurity threats posed by Anthropic's new AI model Claude Mythos, which reportedly can identify and exploit vulnerabilities in mainstream operating systems and browsers. Anthropic has stated that due to the model's powerful capabilities, it currently has no plans for public release and is only available to a limited group of institutions like Amazon, Apple, and JPMorgan Chase. This meeting highlights the growing concern among top regulators and financial leaders that advanced AI models like Mythos could pose unprecedented cybersecurity risks to the U.S. financial system, potentially enabling sophisticated attacks that exploit system vulnerabilities in real-time. It underscores the urgent need for AI governance and regulatory frameworks to address the dual-use nature of such technologies, which could be weaponized by malicious actors if not properly controlled. Anthropic's Claude Mythos Preview has been described as a 'step change' in power, with capabilities that saturate existing benchmarks for vulnerability discovery and exploitation, and it is being released in a limited capacity to critical industry partners and open-source developers through Project Glasswing. The model's rollout is cautious due to fears that hackers could exploit its advanced features, and it is currently accessible only to select entities like Amazon and JPMorgan Chase for defensive purposes.

telegram · zaihuapd · Apr 10, 04:10

**Background**: Anthropic is an AI research company known for developing the Claude language models, which are generative pre-trained transformers fine-tuned with reinforcement learning from human feedback and constitutional AI to enforce ethical guidelines. Claude models typically support text and image input, multilingual capabilities, and are used for tasks like coding and reasoning, but the new Mythos model represents a significant advancement in cybersecurity capabilities. System vulnerabilities refer to weaknesses in software or hardware that can be exploited by attackers to gain unauthorized access or cause damage, and AI-powered exploitation involves using machine learning to identify and leverage these vulnerabilities more efficiently than traditional methods.

<details><summary>References</summary>
<ul>
<li><a href="https://fortune.com/2026/03/26/anthropic-says-testing-mythos-powerful-new-ai-model-after-data-leak-reveals-its-existence-step-change-in-capabilities/">Exclusive: Anthropic ‘Mythos’ AI model representing ‘step change’ in power revealed in data leak | Fortune</a></li>
<li><a href="https://red.anthropic.com/2026/mythos-preview/">Claude Mythos Preview \ red.anthropic.com</a></li>
<li><a href="https://www.cnbc.com/2026/04/10/powell-bessent-us-bank-ceos-anthropic-mythos-ai-cyber.html">Powell, Bessent discussed Anthropic's Mythos AI cyber threat with major U.S. banks</a></li>

</ul>
</details>

**Tags**: `#AI Safety`, `#Cybersecurity`, `#Financial Technology`, `#Regulation`, `#Anthropic`

---

<a id="item-9"></a>
## [Alibaba Forms ATH Business Group Led by CEO Wu Yongming to Focus on Token Economy](https://t.me/zaihuapd/40792) ⭐️ 8.0/10

On March 16, 2026, Alibaba announced the formation of a new business group called Alibaba Token Hub (ATH), led by CEO Wu Yongming, to integrate AI services like Tongyi Qianwen and shift strategic focus from traditional metrics like DAU to TPD (Token Per Day consumption). The group consolidates five core departments, including Tongyi Lab and MaaS business lines, to create a business loop for token creation, delivery, and application. This move signals a major strategic pivot for Alibaba, a leading tech giant, toward token-based economics and AI integration, which could redefine industry metrics and business models in the AI era. It highlights the growing importance of token consumption as a key performance indicator, potentially influencing how companies measure user engagement and resource allocation in AI-driven services. The ATH group includes a new 'Wukong Division' focused on B-end applications, and it aims to leverage token metrics to measure computing power usage rather than traditional app opens. However, the news source is a Telegram channel, which may lack official verification, and specific details on token implementation or timelines are not provided.

telegram · zaihuapd · Apr 10, 06:28

**Background**: A token economy refers to a system where tokens are used as incentives or rewards, commonly applied in contexts like therapy or workplaces to encourage behavior. In AI, TPD (Token Per Day) is a metric that measures daily token consumption, often used to gauge computing resource usage in AI services, such as with APIs from companies like OpenAI or Google. MaaS (Model as a Service) is a business model where pre-trained machine learning models are hosted and delivered as cloud-based services, enabling easier access to AI capabilities.

<details><summary>References</summary>
<ul>
<li><a href="https://eu.36kr.com/en/p/3695269728170505">DAU Is Dead, TPD Lives Forever: A New Paradigm in [Relevant Field]</a></li>
<li><a href="https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-models-as-a-service-maas">What is Model as a Service (MaaS)? | Microsoft Azure</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Token Economy`, `#Business Strategy`, `#Alibaba`, `#Technology News`

---

<a id="item-10"></a>
## [Solayer Founder Exposes LLM Supply Chain Risks: Over 20% of Free Routers Engage in Malicious Activities](https://x.com/Fried_rice/status/2042423713019412941) ⭐️ 8.0/10

Solayer founder Chaofan Shou published a research paper revealing significant security vulnerabilities in third-party API routers used by LLM agents, with testing of 28 paid and 400 free routers showing that 1 paid and 8 free routers actively inject malicious code, while 17 routers accessed AWS credentials and one stole ETH from test private keys. The research team built the Mine proxy to validate four attack classes and proposed defenses like fail-closed policy gates and response-side anomaly screening. This matters because it highlights critical supply chain risks in the rapidly growing LLM ecosystem, where malicious routers can compromise data integrity, steal credentials, and enable large-scale attacks, potentially affecting businesses and users relying on AI-driven applications. The findings underscore the need for enhanced security measures in API routing to prevent widespread vulnerabilities in AI deployments. The routers act as application-layer proxies that can access JSON payloads in plaintext due to a lack of end-to-end encryption, and the research demonstrated attacks where leaked keys could generate massive billing tokens and take over hosts. The Mine proxy was used to test four attack classes, with defenses including fail-closed policy gates and append-only transparency logging.

telegram · zaihuapd · Apr 10, 08:30

**Background**: LLM supply chain security involves risks across the development, deployment, and distribution of large language models, extending beyond the models themselves to include third-party components like API routers. API routers are intermediaries that handle data traffic between applications and services, and vulnerabilities in these routers can lead to malicious code injection or credential theft, as seen in incidents like hackers exploiting cellular routers' APIs. The Mine proxy is a security testing framework designed to simulate man-in-the-middle attacks and evaluate defenses in proxy environments.

<details><summary>References</summary>
<ul>
<li><a href="https://aiasiapacific.org/2025/04/16/uncovering-hidden-risks-security-in-large-language-model-llm-supply-chain/">Uncovering Hidden Risks: Security in Large Language Model (LLM)</a></li>
<li><a href="https://cybersecuritynews.com/hackers-exploit-cellular-routers-api/">Hackers Exploit Cellular Router’s API to Send Malicious SMS</a></li>
<li><a href="https://arxiv.org/html/2604.08407v1">Your Agent Is Mine: Measuring Malicious Intermediary Attacks ...</a></li>

</ul>
</details>

**Tags**: `#LLM Security`, `#Supply Chain Risk`, `#Cybersecurity`, `#API Vulnerabilities`, `#Research Paper`

---

<a id="item-11"></a>
## [French government commits to replacing Windows with Linux for 2.5 million civil servants by 2026](https://cybernews.com/tech/france-windows-linux/) ⭐️ 8.0/10

The French government has formally committed to replacing Microsoft Windows with the Linux operating system on all government desktop computers by autumn 2026, affecting 2.5 million civil servants. This initiative is part of a broader digital sovereignty push that also includes replacing US video conferencing platforms with a locally hosted Visio platform by 2027. This represents one of the largest government migrations from proprietary to open-source software globally, potentially accelerating open-source adoption in public sectors worldwide and reducing strategic dependency on foreign technology infrastructure. The move could influence other nations' digital sovereignty policies and reshape the competitive landscape for operating systems in government environments. Government ministries must submit replacement plans by autumn 2026 covering collaboration tools, antivirus software, AI platforms, databases, and network equipment. The migration follows an earlier requirement for all departments to replace US video conferencing platforms with the locally developed Visio platform hosted on French servers by 2027.

telegram · zaihuapd · Apr 10, 12:47

**Background**: Digital sovereignty refers to a nation's ability to control its digital data, infrastructure, and operations according to its own laws and strategic interests, often involving reduced reliance on foreign technology providers. Linux is an open-source operating system that provides an alternative to proprietary systems like Windows, offering greater control over software and potentially enhanced security. The French government's Visio platform is a Jitsi-based video conferencing tool developed domestically to replace US platforms like Microsoft Teams and Zoom.

<details><summary>References</summary>
<ul>
<li><a href="https://www.sap.com/resources/what-is-digital-sovereignty">What Is Digital Sovereignty? A Practical Guide | SAP</a></li>
<li><a href="https://www.remio.ai/post/france-s-government-visio-platform-replacing-microsoft-teams-by-2027">France's Government Visio Platform : Replacing Microsoft Teams by...</a></li>

</ul>
</details>

**Tags**: `#Linux`, `#Digital Sovereignty`, `#Government Policy`, `#Open Source`, `#Cybersecurity`

---

<a id="item-12"></a>
## [Claude AI models exhibit 'identity confusion' vulnerability, risking unauthorized high-risk operations in automated tools.](https://news.ycombinator.com/item?id=47701233) ⭐️ 8.0/10

Developers have reported that Claude and other large language models suffer from an 'identity confusion' vulnerability in long conversations, where the models misinterpret their own outputs or past reasoning as current user instructions. This issue occurs frequently near the context window limit, leading to models 'self-answering' and generating false user authorizations, which can trigger unauthorized high-risk actions like deployment or deletion in tools such as Claude Code. This vulnerability is significant because it exposes a critical safety flaw in AI agents, potentially allowing them to execute unauthorized operations in automated systems, which could lead to data loss, security breaches, or system damage. It highlights broader risks in deploying large language models for high-stakes applications, emphasizing the need for improved identity management and security protocols in AI-driven tools. The vulnerability is particularly pronounced when models approach their context window limit, a region sometimes called the 'stupid zone,' where performance degrades and confusion increases. Specific tools affected include Claude Code, Anthropic's command-line developer tool built on models like Opus 4, which can perform file manipulation and command execution.

telegram · zaihuapd · Apr 10, 14:52

**Background**: Large language models like Claude process text within a fixed context window, which limits the amount of information they can retain at once; exceeding this limit can cause the model to forget earlier instructions and exhibit errors. Claude Code is an AI-powered coding tool that automates tasks such as file manipulation and code analysis, relying on model outputs to execute commands. Identity confusion in AI agents refers to situations where automated systems misinterpret their own actions or identities, leading to security gaps in non-human interactions.

<details><summary>References</summary>
<ul>
<li><a href="https://claude.com/solutions/coding">Coding | Claude by Anthropic</a></li>
<li><a href="https://www.ibm.com/think/topics/context-window">What is a context window ? | IBM</a></li>
<li><a href="https://hackread.com/ai-agents-non-human-identities-security-gaps/">AI Agents and Non-Human Identities Creating Critical Security Gaps...</a></li>

</ul>
</details>

**Tags**: `#AI Safety`, `#Large Language Models`, `#Vulnerability`, `#AI Agents`, `#Claude`

---

<a id="item-13"></a>
## [WireGuard releases new Windows version after resolving Microsoft driver signing issue](https://lists.zx2c4.com/pipermail/wireguard/2026-April/009561.html) ⭐️ 7.0/10

WireGuard has released a new version for Windows following the resolution of a Microsoft driver signing issue that gained attention through public discussion, as announced by Jason A. Donenfeld (zx2c4) in a mailing list post. The update involved toolchain updates and removed support for pre-Windows 10 systems. This matters because it ensures continued security and functionality for WireGuard users on Windows, a widely used platform, and highlights the importance of public advocacy in resolving bureaucratic hurdles with large tech companies. It also underscores the challenges open-source projects face with proprietary ecosystems like Microsoft's driver signing requirements. The release was challenging due to toolchain updates, and it dropped support for pre-Windows 10 versions, streamlining maintenance. The signing issue was resolved quickly after gaining public attention, but it raises concerns about the reliability of Microsoft's standard processes for less prominent developers.

hackernews · zx2c4 · Apr 10, 15:49

**Background**: WireGuard is a modern, open-source VPN protocol designed for simplicity, speed, and security, created by Jason A. Donenfeld and first released in 2016. Microsoft requires kernel-mode drivers to be signed for Windows to ensure system integrity and security, a policy that has been in place since Windows Vista. VeraCrypt, another open-source encryption tool, recently faced a similar issue when Microsoft terminated its driver signing account, sparking public discussion that likely influenced WireGuard's case.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/WireGuard">WireGuard - Wikipedia</a></li>
<li><a href="https://learn.microsoft.com/en-us/windows-hardware/drivers/install/kernel-mode-code-signing-policy--windows-vista-and-later-">Driver Signing Policy - Windows drivers | Microsoft Learn</a></li>
<li><a href="https://en.wikipedia.org/wiki/VeraCrypt">VeraCrypt - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Community comments express relief that the issue was resolved quickly for WireGuard but raise concerns about whether less visible projects would face similar delays without public outcry. Some users question the generalizability of this resolution and speculate if Microsoft has a pattern of targeting open-source software, citing examples like LibreOffice and VeraCrypt.

**Tags**: `#WireGuard`, `#Windows`, `#Security`, `#Open Source`, `#Microsoft`

---

<a id="item-14"></a>
## [Helium faces replacement challenges due to unique properties and economic factors.](https://www.construction-physics.com/p/helium-is-hard-to-replace) ⭐️ 7.0/10

An article highlights the difficulties in replacing helium, citing its unique physical properties, extraction challenges from natural gas, and economic issues like low recovery rates and investment misalignment. Community comments reinforce these points, noting that less than 10% of natural gas plants recover helium, with most venting it into the atmosphere. This matters because helium is critical for high-value applications like MRI machines, semiconductor manufacturing, and aerospace, and supply shortages could disrupt these industries. The economic and engineering barriers to extraction and substitution highlight vulnerabilities in global supply chains for essential resources. Key details include that helium is primarily extracted from natural gas via cryogenic separation or pressure swing adsorption, but recovery rates are low due to economic factors. China has achieved 99.99997% purity helium using natural gas feedstock, reducing import reliance, yet global extraction remains inefficient.

hackernews · JumpCrisscross · Apr 10, 15:06

**Background**: Helium is a noble gas with unique properties like low boiling point and inertness, making it irreplaceable in applications such as cooling MRI magnets and leak detection. It is extracted from natural gas deposits, where it occurs in trace amounts, requiring complex purification processes. The global helium supply is often precarious due to limited sources and geopolitical factors, as seen in potential disruptions from conflicts like the Iran war.

<details><summary>References</summary>
<ul>
<li><a href="https://interestingengineering.com/innovation/china-ultra-pure-helium-6n9-breakthrough">China achieves 99.99997% helium purity using natural gas feedstock</a></li>
<li><a href="https://www.cnbc.com/2026/03/19/the-iran-war-is-threatening-supply-helium-what-it-means-for-markets.html">The Iran war is threatening supply helium. What it means for ...</a></li>
<li><a href="https://www.mdpi.com/2673-5628/3/4/13">Helium: Sources, Applications, Supply, and Demand - MDPI</a></li>

</ul>
</details>

**Discussion**: Community comments emphasize that helium shortages are primarily an engineering and economic problem, not a physics issue, with users noting low recovery rates and investment misalignment. Some express optimism that price increases will spur extraction investments, while others highlight policy failures like the U.S. selling strategic reserves at a loss. Additional insights mention xenon's rarity and psychoactive effects, broadening the discussion to other noble gases.

**Tags**: `#helium`, `#supply-chain`, `#engineering`, `#economics`, `#natural-resources`

---

<a id="item-15"></a>
## [Linux kernel removes read-only transparent huge pages for page cache due to memory subsystem changes.](https://lwn.net/Articles/1066582/) ⭐️ 7.0/10

The Linux kernel is removing support for read-only transparent huge pages (THP) in the page cache, a feature introduced in 2019 that was initially planned to gain writable support but never did. This change reflects underlying architectural shifts in the memory subsystem, with the configuration variable CONFIG_READ_ONLY_THP_FOR_FS being deprecated. This removal signifies a shift in kernel development priorities, as the feature was experimental and limited to executable text sections, impacting performance optimizations for file-backed memory. It affects distributions that enabled it and highlights how evolving memory management can deprecate incomplete features. The feature only worked with memory areas marked VM_DENYWRITE, typically executable text sections, and required an madvise() call to enable THP merging. If a file was opened for write access while read-only THPs existed, the kernel would evict all pages from the cache and restart with base pages.

rss · LWN.net · Apr 10, 13:26

**Background**: Transparent huge pages (THP) automatically combine base pages into larger 2MB pages to reduce memory-management overhead and TLB pressure, initially supporting only anonymous memory like program data. The page cache handles file-backed memory but lacked huge-page awareness, making THP integration challenging. Kconfig is a configuration system in the Linux kernel used to manage build options and dependencies.

<details><summary>References</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html">Transparent Hugepage Support — The Linux Kernel documentation</a></li>
<li><a href="https://opensource.com/article/18/10/kbuild-and-kconfig">Exploring the Linux kernel: The secrets of Kconfig/kbuild |</a></li>

</ul>
</details>

**Tags**: `#Linux Kernel`, `#Memory Management`, `#Transparent Huge Pages`, `#Systems Programming`

---

<a id="item-16"></a>
## [GLM 5.1 ranks first in code arena benchmarks for open models](https://i.redd.it/ienycmczudug1.png) ⭐️ 7.0/10

GLM 5.1, an open-source language model, has achieved the top ranking in code arena benchmarks, demonstrating superior performance in code-related tasks compared to other open models. This announcement highlights its state-of-the-art capabilities in coding, as indicated by recent evaluations. This achievement matters because it positions GLM 5.1 as a leading open model for code generation, potentially accelerating development in AI-assisted programming and software engineering. It signals progress in making high-performance coding tools more accessible through open-source initiatives, benefiting developers and researchers. GLM 5.1 is designed for agentic engineering with enhanced coding capabilities, outperforming its predecessor on benchmarks like SWE-Bench Pro and NL2Repo. The model handles complex problems over long sessions and includes a lightweight installer for easy deployment on local devices.

reddit · r/LocalLLaMA · Auralore · Apr 10, 15:40

**Background**: GLM 5.1 is a next-generation open-source language model developed for agentic tasks, focusing on coding and software engineering. Code arena benchmarks, such as those referenced, evaluate large language models (LLMs) on code generation and related tasks to compare performance across models. Open models in AI refer to publicly available models that can be customized and run anywhere, promoting accessibility and innovation in the field.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/zai-org/GLM-5.1">zai-org/GLM-5.1 · Hugging Face</a></li>
<li><a href="https://openlm.ai/glm-5.1/">GLM-5.1 - openlm.ai</a></li>
<li><a href="https://arxiv.org/pdf/2503.01295">CodeArena: A Collective Evaluation Platform for LLM Code Generation</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Open Source`, `#Code Generation`, `#Benchmarks`, `#Machine Learning`

---

<a id="item-17"></a>
## [Hong Kong issues first stablecoin issuer licenses to Anchor Financial and HSBC](https://www.cls.cn/detail/2340578) ⭐️ 7.0/10

On April 10, Hong Kong's Monetary Authority issued the first stablecoin issuer licenses under the Stablecoin Ordinance to Anchor Financial Technology and HSBC, allowing them to issue stablecoins in Hong Kong. The licenses are effective immediately, with both companies planning to launch operations within the coming months after completing preparatory work. This represents a significant regulatory milestone for Hong Kong's fintech sector, establishing a clear legal framework for stablecoin issuance that could attract more institutional players and boost cryptocurrency adoption. As a major global financial hub, Hong Kong's regulatory approach may influence other jurisdictions developing stablecoin regulations. The licenses were granted under Hong Kong's Stablecoin Ordinance, which establishes specific requirements for stablecoin issuers. Both Anchor Financial Technology (a fintech company) and HSBC (a traditional banking institution) received licenses, indicating the regulatory framework accommodates both new entrants and established financial players.

telegram · zaihuapd · Apr 10, 09:15

**Background**: Stablecoins are cryptocurrencies designed to maintain a stable value by being pegged to a reserve asset like fiat currency or commodities. Regulatory frameworks for stablecoin issuers, such as the GENIUS Act in the US, typically establish licensing requirements and prudential standards to ensure consumer protection and financial stability. Hong Kong's Stablecoin Ordinance represents a similar regulatory approach in Asia's financial markets.

<details><summary>References</summary>
<ul>
<li><a href="https://www.sidley.com/en/insights/newsupdates/2025/07/the-genius-act-a-framework-for-us-stablecoin-issuance">The GENIUS Act: A Framework for U.S. Stablecoin Issuance ...</a></li>
<li><a href="https://complyfactor.com/genius-act-ppsi-aml-compliance-stablecoin-issuers/">GENIUS Act AML Compliance Guide for Payment Stablecoin ...</a></li>

</ul>
</details>

**Tags**: `#stablecoin`, `#regulatory`, `#fintech`, `#Hong Kong`, `#banking`

---

<a id="item-18"></a>
## [MiniMax releases Music 2.6, a new music generation model with 14-day free beta](https://www.36kr.com/newsflashes/3760667223147011) ⭐️ 7.0/10

On April 10, MiniMax officially launched Music 2.6, a new music generation model that features reduced latency, enhanced control, better audio quality, and new capabilities like 'Cover' creation and Music Skill for AI Agents. The model is available for a 14-day free beta test to global creators. This release represents a significant advancement in AI-generated music, potentially lowering barriers for creators and enhancing tools for AI agents in creative workflows. It positions MiniMax competitively in the growing AI music generation market, which includes rivals like Suno. Music 2.6 boasts a restructured architecture with sub-20-second latency, making it faster than previous versions. The 'Cover' feature allows users to generate music based on existing tracks, while Music Skill enables AI agents to integrate music generation into their functionalities.

telegram · zaihuapd · Apr 10, 12:02

**Background**: MiniMax is a Chinese AI company based in Shanghai, known for developing multimodal AI models and applications like Talkie and Hailuo AI. AI music generation models use machine learning to create audio from text or other inputs, with companies like Suno also active in this space. AI agents are autonomous systems that can perform tasks, and integrating music skills allows them to assist in creative processes.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/MiniMax_Group">MiniMax Group - Wikipedia</a></li>
<li><a href="https://www.minimax.io/news/music-26">MiniMax Music 2.6: Four Stories We Want to Tell</a></li>
<li><a href="https://www.edgen.tech/news/post/minimax-challenges-suno-with-20-second-ai-music-generation-model">Minimax Challenges Suno with 20-Second AI Music Generation Model</a></li>

</ul>
</details>

**Tags**: `#AI Music Generation`, `#Machine Learning`, `#Creative AI`, `#Beta Testing`, `#MiniMax`

---

<a id="item-19"></a>
## [CPU-Z official website hacked, malicious code inserted into download packages](https://m.ithome.com/html/938003.htm) ⭐️ 7.0/10

The official website of CPU-Z and HWMonitor developer CPUID was hacked from April 9 to 10, 2026, for about 6 hours, causing download links to redirect to malicious servers and some installation packages to be infected with malware. CPUID has since fixed the vulnerability and restored normal downloads. This incident highlights significant cybersecurity risks for widely-used software tools, potentially affecting millions of users who rely on CPU-Z for hardware monitoring and system diagnostics. It underscores the importance of supply chain security and user vigilance in downloading software from trusted sources. The attack was executed by compromising a minor API on the website, without tampering with the original signed files, and users reported malware detection by Windows Defender. CPUID advises users who downloaded the software during the breach to take immediate security measures and check their systems.

telegram · zaihuapd · Apr 10, 15:38

**Background**: CPU-Z is a popular hardware monitoring tool developed by CPUID that provides detailed information about a computer's CPU, memory, and other components, widely used by PC enthusiasts and IT professionals. HWMonitor, another tool by CPUID, monitors hardware sensors like temperatures and voltages. Such tools often require administrative privileges, making them high-value targets for attackers seeking to distribute malware.

<details><summary>References</summary>
<ul>
<li><a href="https://www.tomshardware.com/tech-industry/cyber-security/hwmonitor-and-cpu-z-developer-cpuid-breached-by-unknown-attackers-cyberattack-forced-users-to-download-malware-instead-of-valid-apps-for-approximately-six-hours">HWMonitor and CPU-Z developer CPUID breached ... - Tom's Hardware</a></li>
<li><a href="https://www.cpuid.com/softwares/hwmonitor.html">HWMONITOR | Softwares | CPUID</a></li>

</ul>
</details>

**Tags**: `#cybersecurity`, `#software-security`, `#hardware-tools`, `#malware`, `#incident-response`

---