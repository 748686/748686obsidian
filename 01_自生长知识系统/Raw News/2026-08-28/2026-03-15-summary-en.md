---
layout: default
title: "Horizon Summary: 2026-03-15 (EN)"
date: 2026-03-15
lang: en
---

> From 27 items, 8 important content pieces were selected

---

1. [Jazzband open-source organization is sunsetting due to AI-generated spam PRs](#item-1) ⭐️ 8.0/10
2. [Nvidia's Nemotron 3 Super offers permissive open-source AI with state-of-the-art training infrastructure](#item-2) ⭐️ 8.0/10
3. [Custom CUTLASS kernel fixes SM120 MoE GEMM tiles, boosting Qwen3.5-397B inference from 55 to 282 tok/s on 4x RTX PRO 6000 Blackwell](#item-3) ⭐️ 8.0/10
4. [Anthropic releases Claude Opus 4.6 with 200K context window and adaptive thinking modes](#item-4) ⭐️ 8.0/10
5. [StepFun releases SFT dataset for Step 3.5 Flash model](#item-5) ⭐️ 7.0/10
6. [Open-source Rust app automates manga translation using AI models with zero setup](#item-6) ⭐️ 7.0/10
7. [Elon Musk admits xAI architectural mistakes, plans complete rebuild as 9 of 12 co-founders depart](#item-7) ⭐️ 7.0/10
8. [Instagram to discontinue end-to-end encryption for direct messages after May 2026](#item-8) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Jazzband open-source organization is sunsetting due to AI-generated spam PRs](https://simonwillison.net/2026/Mar/14/jannis-leidel/#atom-everything) ⭐️ 8.0/10

The Jazzband open-source organization announced it is sunsetting because GitHub's 'slopocalypse' of AI-generated spam pull requests has made its open membership model untenable. The organization cited examples including curl shutting down its bug bounty program and GitHub introducing a kill switch for pull requests as evidence of the severity of the problem. This highlights a critical threat to the sustainability of open-source projects, particularly those with open contribution models, as AI-generated low-quality submissions overwhelm maintainers and degrade project quality. It signals a broader industry challenge where automated content generation tools are undermining the collaborative foundations of open-source development. Jazzband specifically mentioned that only 1 in 10 AI-generated PRs meets project standards, and curl's bug bounty confirmation rates dropped below 5% before being shut down. The organization was designed for a world where the worst-case scenario was accidental merges, not systematic low-quality submissions at scale.

rss · Simon Willison · Mar 14, 18:41

**Background**: Jazzband is an open-source organization that allows members to transfer repositories and provides shared push access, operating on an open membership model where anyone can join. The term 'slopocalypse' refers to the flood of low-quality, AI-generated content (often called 'AI slop') that lacks effort, logic, or purpose, which has become a form of spam in software development. AI-generated spam PRs are automated pull requests created by AI tools that typically don't meet project standards and overwhelm maintainers with low-quality submissions.

<details><summary>References</summary>
<ul>
<li><a href="https://jazzband.co/">Jazzband - We are all part of this</a></li>
<li><a href="https://en.wikipedia.org/wiki/AI_slop">AI slop - Wikipedia</a></li>
<li><a href="https://www.theregister.com/2026/01/21/curl_ends_bug_bounty/">Curl shutters bug bounty program to stop AI slop • The Register</a></li>

</ul>
</details>

**Tags**: `#open-source`, `#AI-ethics`, `#software-maintenance`, `#GitHub`, `#developer-tools`

---

<a id="item-2"></a>
## [Nvidia's Nemotron 3 Super offers permissive open-source AI with state-of-the-art training infrastructure](https://www.signalbloom.ai/posts/nvidia-nemotron-3-super-is-a-bigger-deal-than-you-think/) ⭐️ 8.0/10

Nvidia released Nemotron 3 Super, a 120-billion-parameter open-source AI model with a more permissive license than previous versions, removing objectionable terms from the Open Model license. The model is part of the Nemotron 3 family that includes Nano, Super, and Ultra sizes, and it provides optimized 4-bit quantization for efficient deployment. This release democratizes access to state-of-the-art AI training infrastructure by lowering barriers to entry, potentially fracturing the software moats of traditional model builders. The permissive licensing enables broader adoption by developers, researchers, and organizations who want to train their own models without restrictive terms. The model uses 4-bit quantization (NVFP4) for optimized performance, though some community members noted its absence from certain benchmarks like SWE-bench. The license change specifically removes terms that were considered objectionable in the previous Open Model license, making it more permissive for commercial and research use.

reddit · r/LocalLLaMA · Comfortable-Rock-498 · Mar 14, 17:15

**Background**: Nemotron 3 is a family of open-source AI models from Nvidia that includes Nano (30B), Super (120B), and Ultra (500B) parameter sizes. Permissive licenses like Apache 2.0, MIT, and BSD allow broad usage with minimal restrictions, unlike more restrictive licenses that limit commercial applications. State-of-the-art training infrastructure refers to optimized hardware and software systems, such as Nvidia's DGX platforms, that enable efficient training of large AI models.

<details><summary>References</summary>
<ul>
<li><a href="https://wccftech.com/nvidia-nemotron-3-open-ai-models-nano-super-ultra-sizes-4x-faster/">NVIDIA Nemotron 3 Models Announced: Open AI Models In Nano,</a></li>
<li><a href="https://medium.com/@mne/understanding-permissive-licenses-for-large-language-models-llms-843d40909ce0">Understanding Permissive Licenses for Large Language Models (LLMs) - Medium</a></li>
<li><a href="https://www.nvidia.com/en-us/data-center/dgx-gb200/">DGX GB200: AI Infrastructure for State-of-the-Art AI Models ...</a></li>

</ul>
</details>

**Discussion**: Community sentiment is generally positive, with users highlighting the strategic implications of Nvidia commoditizing training infrastructure to create demand for their GPUs. Key discussions focus on the license change being more permissive, the model enabling countries and companies to train their own models, and some dismissive remarks about blog spam. There's debate about whether Nvidia's motivation is altruistic or strategic.

**Tags**: `#AI`, `#Open Source`, `#Nvidia`, `#Machine Learning`, `#Licensing`

---

<a id="item-3"></a>
## [Custom CUTLASS kernel fixes SM120 MoE GEMM tiles, boosting Qwen3.5-397B inference from 55 to 282 tok/s on 4x RTX PRO 6000 Blackwell](https://www.reddit.com/r/LocalLLaMA/comments/1rtrdsv/55_282_toks_how_i_got_qwen35397b_running_at_speed/) ⭐️ 8.0/10

A developer built a custom CUTLASS kernel to fix a bug in SM120 Blackwell GPUs' MoE GEMM tiles, which were incorrectly designed for datacenter B200 GPUs with 228KB shared memory instead of workstation GPUs' 99KB. This patch enabled K=64 tile shapes to compile and run correctly, increasing Qwen3.5-397B inference speed from 55 to 282 tokens per second on 4x RTX PRO 6000 Blackwell GPUs. This optimization significantly improves the practical usability of large Mixture-of-Experts models like Qwen3.5-397B on consumer and workstation Blackwell GPUs, potentially making high-performance local inference more accessible. It addresses a critical bottleneck where SM120 GPUs were stuck using slow fallback kernels, leaving over 50% of throughput unused. The fix specifically patches the `sm120_blockscaled_mma_builder.inl` file in CUTLASS to compute `EffBlk_SF = min(K/SFVectorSize, Blk_SF)` for handling K<128 cases and fold scale factors into the basic block when they exceed MMA requirements. The developer has submitted a pull request to FlashInfer and made a pre-built Docker image available for others to use.

reddit · r/LocalLLaMA · lawdawgattorney · Mar 14, 18:46

**Background**: CUTLASS is NVIDIA's CUDA Templates for Linear Algebra Subroutines, providing high-performance GEMM (General Matrix Multiply) kernel implementations for GPU acceleration. Mixture-of-Experts models like Qwen3.5-397B use specialized MoE GEMM tiles that optimize computation by routing inputs to different expert networks. SM120 refers to the compute capability of Blackwell architecture GPUs like the RTX PRO 6000, which have 99KB of shared memory compared to 228KB in datacenter B200 GPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/NVIDIA/cutlass">GitHub - NVIDIA/cutlass: CUDA Templates and Python DSLs for High-Performance Linear Algebra · GitHub</a></li>
<li><a href="https://pytorch.org/blog/accelerating-moes-with-a-triton-persistent-cache-aware-grouped-gemm-kernel/">Accelerating MoE’s with a Triton Persistent Cache-Aware Grouped GEMM Kernel – PyTorch</a></li>
<li><a href="https://github.com/orgs/flashinfer-ai/discussions/1464">Blackwell Architecture support? · flashinfer-ai · Discussion #1464</a></li>

</ul>
</details>

**Discussion**: Community comments praise the technical depth of the K=64 tile fix, with users noting that most people would blame frameworks like vLLM rather than tracing the issue to CUTLASS assumptions. Discussions include questions about scalability for more modest setups with multiple 5060/5070 Ti GPUs, hardware compatibility concerns regarding AMD Threadripper systems requiring `iommu=pt` kernel parameters, and excitement about potential verification on DGX Spark systems.

**Tags**: `#GPU Optimization`, `#CUTLASS`, `#MoE Models`, `#Inference Speed`, `#Blackwell Architecture`

---

<a id="item-4"></a>
## [Anthropic releases Claude Opus 4.6 with 200K context window and adaptive thinking modes](https://t.me/zaihuapd/40251) ⭐️ 8.0/10

Anthropic has released Claude Opus 4.6, which doubles the context window to 200K tokens (with a beta offering of 1 million tokens) and increases maximum output tokens to 128K from the previous 64K limit. The model introduces adaptive thinking modes that dynamically adjust reasoning depth based on problem complexity, adds a max effort parameter, and features context compression that automatically summarizes early conversation content when approaching window limits. These improvements significantly enhance Claude's ability to handle complex, long-form reasoning tasks and maintain coherent conversations over extended interactions, making it more suitable for professional workflows and agentic autonomy applications. The adaptive thinking modes represent an advancement in making AI reasoning more efficient and context-aware, while context compression addresses a fundamental limitation in current LLM architectures. The 200K context window is available in beta with 1 million tokens, though the standard version supports 200K tokens. The context compression feature works by automatically summarizing earlier parts of conversations when they approach the window limit, enabling effectively infinite-length conversations while maintaining semantic density. Claude Opus 4.6 is positioned as Anthropic's top-tier model for the most complex tasks, particularly excelling in coding and reasoning.

telegram · zaihuapd · Mar 14, 01:19

**Background**: Large language models (LLMs) like Claude process text using a context window that determines how much previous text they can consider when generating responses. Context windows have been expanding from early models with just a few thousand tokens to current models with hundreds of thousands of tokens. Adaptive thinking refers to techniques that allow models to adjust their reasoning depth and approach based on problem complexity, while context compression involves summarizing or condensing conversation history to stay within model limits without losing important information.

<details><summary>References</summary>
<ul>
<li><a href="https://apxml.com/models/claude-opus-46">Claude Opus 4.6: Model Specifications and Details - apxml.com</a></li>
<li><a href="https://platform.claude.com/docs/en/about-claude/models/overview">Models overview - Claude API Docs</a></li>
<li><a href="https://crompt.ai/blog/what-is-context-compression-in-ai-and-why-it-improves-long-conversations">Context Compression in AI. How Long Conversations Stay ...</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Large Language Models`, `#Anthropic`, `#Claude`, `#Natural Language Processing`

---

<a id="item-5"></a>
## [StepFun releases SFT dataset for Step 3.5 Flash model](https://huggingface.co/datasets/stepfun-ai/Step-3.5-Flash-SFT) ⭐️ 7.0/10

StepFun has publicly released the supervised fine-tuning (SFT) dataset used to train their Step 3.5 Flash model, making it available on Hugging Face under a non-commercial license. This release represents a significant contribution to the open-source AI community by enabling reproducibility, further research, and model comparisons, while also building StepFun's reputation for transparency. The dataset is released under a non-commercial license on Hugging Face, which restricts commercial use but allows research and experimentation. Step 3.5 Flash is noted for its strong performance in coding, agentic capabilities, and tool use, though some users note it can be slower in thinking processes.

reddit · r/LocalLLaMA · tarruda · Mar 14, 18:56

**Background**: Supervised fine-tuning (SFT) is a technique used to adapt pre-trained large language models (LLMs) to specific tasks using labeled data, where the model learns to replicate the style of provided examples. Step 3.5 Flash is StepFun's open-source foundation model engineered for reasoning and agentic capabilities, and it is available in formats like INT4/GGUF for efficient deployment. Hugging Face is a platform where AI models and datasets are shared, often with licenses that specify usage permissions.

<details><summary>References</summary>
<ul>
<li><a href="https://cameronrwolfe.substack.com/p/understanding-and-using-supervised">Understanding and Using Supervised Fine-Tuning (SFT) for Language Models</a></li>
<li><a href="https://forums.developer.nvidia.com/t/running-step-3-5-flash-on-single-spark/359457">Running Step-3.5-Flash on Single Spark - DGX Spark / GB10</a></li>
<li><a href="https://huggingface.co/docs/hub/repositories-licenses">Licenses · Hugging Face</a></li>

</ul>
</details>

**Discussion**: The community response is overwhelmingly positive, with users expressing appreciation for StepFun's transparency and the dataset's potential for fine-tuning. Comments highlight respect for the release, excitement for future models like Step-3.6 or StepFun 4, and praise for Step 3.5 Flash's performance in coding and tool use, though some note its non-commercial license as a limitation.

**Tags**: `#AI`, `#Machine Learning`, `#Open Source`, `#Fine-tuning`, `#Datasets`

---

<a id="item-6"></a>
## [Open-source Rust app automates manga translation using AI models with zero setup](https://www.reddit.com/r/LocalLLaMA/comments/1rtf4v8/local_manga_translator_with_llms_built_in/) ⭐️ 7.0/10

A developer has released Koharu, an open-source Rust application that automatically translates manga pages by combining YOLO for text detection, custom OCR, LaMa for inpainting, LLMs for translation, and a custom text rendering engine. The application comes with CUDA bundled and requires zero setup for immediate use. This tool democratizes manga translation by making it accessible to non-experts without requiring technical setup, potentially accelerating fan translations and content localization. It represents a practical integration of multiple AI technologies (computer vision and language models) into a single, user-friendly application for a specific real-world use case. The application is written in Rust and includes bundled CUDA support for GPU acceleration, but users report translation quirks such as proper noun errors (e.g., 'Zoro' translated as 'Sword Jesus') and challenges with culturally specific terms like 'nakama'. It currently focuses on Japanese-to-English translation but questions about other language support remain open.

reddit · r/LocalLLaMA · mayocream39 · Mar 14, 09:36

**Background**: YOLO (You Only Look Once) is a real-time object detection model that can be fine-tuned for text detection, identifying bounding boxes around text regions in images. LaMa (Large Mask Inpainting) is an AI model designed to remove or replace objects in images by filling in missing areas with plausible content, useful here for erasing original text before rendering translations. CUDA (Compute Unified Device Architecture) is a parallel computing platform that enables applications to leverage NVIDIA GPUs for accelerated processing, which is bundled with this application to simplify setup.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/RoyRud1902/yolo11n-text">RoyRud1902/ yolo 11n- text · Hugging Face</a></li>
<li><a href="https://medium.com/@martin-thissen/remove-any-object-from-an-image-using-ai-stable-diffusion-lama-cleaner-d52d5f3542f1">Remove Any Object From An Image Using AI | LaMa -Cleaner</a></li>
<li><a href="https://superuser.com/questions/219702/is-there-a-way-to-run-cuda-applications-with-the-cuda-device-being-a-secondary-a">nvidia geforce - Is there a way to run CUDA applications with</a></li>

</ul>
</details>

**Discussion**: Community comments show high engagement with users testing the tool on real manga, noting humorous translation errors and requesting features like multi-language support, browser integration, and font customization. Discussions also compare it to alternative tools like comic-translate and explore technical aspects such as model nuances for Japanese slang and whether it runs LLMs locally or via external requests.

**Tags**: `#manga-translation`, `#local-llm`, `#rust`, `#computer-vision`, `#open-source`

---

<a id="item-7"></a>
## [Elon Musk admits xAI architectural mistakes, plans complete rebuild as 9 of 12 co-founders depart](https://futurism.com/artificial-intelligence/elon-musk-screwed-up-xai-rebuilding) ⭐️ 7.0/10

On March 13, Elon Musk announced that his AI startup xAI is undergoing a complete architectural rebuild from the ground up, admitting the company was initially built incorrectly. Nine of xAI's twelve co-founders have now departed, leaving only three remaining, including image generation product lead Guodong Zhang who recently announced his departure. This significant restructuring at one of Elon Musk's core AI ventures signals potential strategic challenges and could impact xAI's competitive position in the rapidly evolving AI landscape. The high-profile departures and architectural overhaul may affect investor confidence and the company's ability to execute its AI development roadmap. To address talent loss, Musk is reconnecting with previously rejected candidates through talent head Baris Akis and has hired two senior employees from AI programming startup Cursor. Additionally, Tesla has received approval to convert its investment in xAI into a small equity stake in SpaceX, which is expected to go public later this year with a $1.25 trillion valuation.

telegram · zaihuapd · Mar 14, 02:21

**Background**: xAI is Elon Musk's artificial intelligence startup founded in 2023, positioned as a competitor to companies like OpenAI. The company has been developing AI models and tools, including image generation products. Cursor is an AI coding assistant startup that has gained significant traction in the developer community, recently raising $2.3 billion at a $29.3 billion valuation according to reports. SpaceX is Musk's aerospace company that is preparing for an initial public offering (IPO) expected later this year.

<details><summary>References</summary>
<ul>
<li><a href="https://cursor.com/">Cursor : The best way to code with AI</a></li>
<li><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lSNFBmLUR4R2h3d2UybkxHOU95Z0FQAQ?hl=en-IN&gl=IN&ceid=IN:en">Google News - Cursor , an AI company, raises $2.3 billion in funding...</a></li>
<li><a href="https://www.gurufocus.com/news/8704136/tesla-converts-xai-investment-to-spacex-shares-before-ipo">Tesla Converts xAI Investment to SpaceX Shares Before IPO</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Startups`, `#Leadership`, `#Restructuring`, `#Elon Musk`

---

<a id="item-8"></a>
## [Instagram to discontinue end-to-end encryption for direct messages after May 2026](https://www.theverge.com/tech/894752/instagram-end-to-end-encryption) ⭐️ 7.0/10

Instagram has updated its support page to confirm that end-to-end encryption for direct messages will be discontinued after May 8, 2026. Meta stated this change is due to "very low" actual usage of the feature on Instagram and recommends WhatsApp as an alternative for encrypted communication. This decision significantly reduces privacy protections for Instagram users, potentially exposing their private messages to Meta's access and increasing vulnerability to data breaches or surveillance. It reflects Meta's strategic consolidation of encrypted messaging services toward WhatsApp, which could influence user migration patterns and industry debates about balancing security with platform functionality. The change will take effect after May 8, 2026, giving users over two years to transition. While Instagram will lose end-to-end encryption for DMs, WhatsApp—which uses the Signal Protocol for encryption—remains fully end-to-end encrypted and is positioned as Meta's preferred platform for secure messaging.

telegram · zaihuapd · Mar 14, 04:47

**Background**: End-to-end encryption (E2EE) is a security method where only the sender and intended recipient can read messages, preventing third parties including service providers from accessing the content. It is widely used in messaging apps like WhatsApp, Signal, and iMessage to protect against data breaches and surveillance. Meta owns both Instagram and WhatsApp, with WhatsApp being the world's most widely used E2EE service with over 3 billion users as of 2025.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/End-to-end_encryption">End-to-end encryption</a></li>
<li><a href="https://signal.org/blog/whatsapp-complete/">Signal >> Blog >> WhatsApp's Signal Protocol</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#social-media`, `#encryption`, `#Meta`

---