---
layout: default
title: "Horizon Summary: 2026-02-25 (EN)"
date: 2026-02-25
lang: en
---

> From 43 items, 12 important content pieces were selected

---

1. [AMD and Meta sign $600 billion AI chip supply deal with 10% equity option](#item-1) ⭐️ 9.0/10
2. [Linux kernel developer proposes AUTOREAP and PIDFS flags for clone3() system call](#item-2) ⭐️ 8.0/10
3. [Critique of ML conference papers lacking code and reproducibility](#item-3) ⭐️ 8.0/10
4. [Qwen3.5-122B-A10B, a major open-source 122B parameter model, is released on Hugging Face.](#item-4) ⭐️ 8.0/10
5. [Qwen3.5-122B-A10B outperforms GPT-5-mini and GPT-OSS-120B in comprehensive benchmark tests.](#item-5) ⭐️ 8.0/10
6. [Anthropic's blog on detecting distillation attacks sparks censorship and reliability concerns](#item-6) ⭐️ 8.0/10
7. [U.S. Department of Defense Considers Ending Partnership with Anthropic Over AI Military Use Restrictions](#item-7) ⭐️ 8.0/10
8. [Dog's random keyboard inputs generate playable games through AI scaffolding](#item-8) ⭐️ 7.0/10
9. [Qwen3.5-35B-A3B demonstrates breakthrough performance for agentic coding on consumer-grade hardware.](#item-9) ⭐️ 7.0/10
10. [New Qwen3.5 Model Variants Discovered: 27B Dense and 122B MoE](#item-10) ⭐️ 7.0/10
11. [Liquid AI releases LFM2-24B-A2B, a 24B parameter sparse MoE model for efficient edge inference.](#item-11) ⭐️ 7.0/10
12. [Unitree Robotics Releases Unitree As2 Quadruped Robot for Industrial Applications](#item-12) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [AMD and Meta sign $600 billion AI chip supply deal with 10% equity option](https://www.reuters.com/business/amd-clinches-second-mega-chip-supply-deal-this-time-with-meta-2026-02-24/) ⭐️ 9.0/10

On February 24, AMD announced a 5-year AI chip supply agreement with Meta valued at up to $600 billion, which includes an option for Meta to acquire up to 10% of AMD's stock. The deal involves AMD supplying 6 gigawatts of computing capacity, including its upcoming MI450 flagship hardware and custom CPUs, starting in the second half of this year. This massive deal represents a significant strategic shift in the AI hardware market, directly challenging Nvidia's dominance by securing a major hyperscaler as a long-term customer. The unprecedented scale and equity participation terms could reshape competitive dynamics and supply chain relationships across the semiconductor industry for years to come. AMD will issue 160 million warrants to Meta with an exercise price of $0.01, with vesting contingent on AMD's stock price reaching $600 and other performance milestones. The agreement covers 6GW of AI compute capacity, with the first 1GW deployment scheduled for the second half of 2026 according to industry reports.

telegram · zaihuapd · Feb 24, 14:47

**Background**: AMD's MI series accelerators are designed to compete with Nvidia's dominant H100 and upcoming Blackwell GPUs in the data center AI market. AI chip supply agreements between semiconductor manufacturers and large cloud providers like Meta, Amazon, and Google have become increasingly strategic, often involving custom silicon and long-term capacity commitments. The "6GW" metric refers to the total power capacity allocated for AI computing infrastructure, which correlates with the number of accelerators that can be deployed.

**Tags**: `#AI Hardware`, `#Semiconductors`, `#Corporate Strategy`, `#Meta`, `#AMD`

---

<a id="item-2"></a>
## [Linux kernel developer proposes AUTOREAP and PIDFS flags for clone3() system call](https://lwn.net/Articles/1059673/) ⭐️ 8.0/10

Christian Brauner has proposed two new flags for the clone3() system call: CLONE_AUTOREAP, which automatically cleans up child processes when they exit, and CLONE_PIDFD_AUTOKILL, which ties a child process's life to its pidfd file descriptor and kills it if the pidfd is closed. These proposals extend the pidfd API and represent a significant change to Linux's process management security model. This matters because it fundamentally changes how processes are managed on Linux systems, moving toward safer and more deterministic process handles via pidfds. The CLONE_PIDFD_AUTOKILL flag in particular introduces a new security model where process lifetime is tied to a file descriptor, which could prevent orphaned processes but also raises concerns about unexpected terminations. The CLONE_AUTOREAP flag provides a 'fire-and-forget' pattern where exit status is unavailable unless CLONE_PIDFD is also used. CLONE_PIDFD_AUTOKILL requires both CLONE_PIDFD and CLONE_AUTOREAP, and kills the child with SIGKILL if its pidfd is closed, which some developers find controversial due to its abrupt termination behavior.

rss · LWN.net · Feb 24, 15:26

**Background**: The pidfd API provides file descriptors that refer to processes, offering safer and more deterministic process handles than traditional process IDs. The clone3() system call creates new processes or threads, and the existing CLONE_PIDFD flag returns a pidfd for the new process. In traditional Unix, parents must call wait() to 'reap' zombie processes after children exit, or set SIGCHLD to SIG_IGN for automatic cleanup of all children.

**Tags**: `#linux-kernel`, `#systems-programming`, `#process-management`, `#kernel-api`, `#pidfd`

---

<a id="item-3"></a>
## [Critique of ML conference papers lacking code and reproducibility](https://www.reddit.com/r/MachineLearning/comments/1rdca7x/d_papers_with_no_code/) ⭐️ 8.0/10

A Reddit post criticizes the acceptance of machine learning papers at major conferences without accompanying code or reproducible evidence, citing a specific example where a paper promising fast protein MSA generation via RAG linked to an empty GitHub repository. The post highlights this as a systemic issue enabling potentially fabricated results or methodological errors to go unchecked. This matters because it exacerbates the reproducibility crisis in machine learning, undermining scientific integrity and slowing genuine progress. When papers claiming state-of-the-art (SOTA) performance on expensive-to-train models cannot be verified, it wastes community resources, erodes trust in published research, and hinders the practical application of potentially groundbreaking methods. The critique specifically mentions papers that claim to train huge models and present SOTA results but provide no code, making independent verification impossible due to the high computational cost. A noted example is a paper on protein MSA generation using RAG, which provided a link to a completely empty GitHub repository with no author response regarding code release.

reddit · r/MachineLearning · osamabinpwnn · Feb 24, 10:05

**Background**: In machine learning, 'SOTA' (State-Of-The-Art) refers to the best currently known performance on a specific benchmark task. Major conferences often use platforms like OpenReview for submission and peer review. Reproducibility—the ability for other researchers to obtain the same results using the provided code and data—is a cornerstone of scientific research but is a recognized challenge in computational fields like ML.

**Discussion**: Community sentiment is strongly critical, viewing the lack of code as symptomatic of a deeper reproducibility crisis and misaligned career incentives in academia. Key viewpoints include: even provided code is often non-functional or obfuscated; unavailable code prevents detection of results within statistical noise; and some argue the field prioritizes career advancement over rigorous science. Several commenters note that code quality is often poor because academics are not professional software developers.

**Tags**: `#reproducibility`, `#machine-learning`, `#academic-research`, `#open-science`, `#peer-review`

---

<a id="item-4"></a>
## [Qwen3.5-122B-A10B, a major open-source 122B parameter model, is released on Hugging Face.](https://huggingface.co/Qwen/Qwen3.5-122B-A10B) ⭐️ 8.0/10

Alibaba's Qwen team has released Qwen3.5-122B-A10B, a 122-billion-parameter dense language model, on Hugging Face. The model achieves strong benchmark performance, scoring 25.3 on the HELM (HLE) benchmark, which was state-of-the-art approximately six months ago. This release provides the open-source community with a powerful, large-scale model that directly competes with other leading open-source models like GPT-OSS-120B. It advances the accessibility of high-performance AI, enabling researchers and developers to experiment with and deploy a model of this scale without proprietary restrictions. The model is a 'dense' architecture (not a Mixture-of-Experts) and currently lacks natively provided 4-bit quantized weights, which is a point of discussion for practical deployment. Community members have already created quantized versions, such as GGUF formats from Unsloth, with one quantized variant reportedly achieving 94 tokens per second on an RTX 6000 Blackwell GPU.

reddit · r/LocalLLaMA · coder543 · Feb 24, 16:44

**Background**: Qwen3.5 is the latest generation of the Qwen series of large language models from Alibaba, which includes both dense and Mixture-of-Experts (MoE) architectures in various sizes. Quantization is a crucial technique for deploying large models, as it reduces the model's memory footprint and computational requirements by using lower-precision numbers (like 4-bit integers) to represent weights, enabling faster inference on consumer hardware.

**Discussion**: The community is actively discussing quantization and practical deployment. Sentiment is positive, with users testing the model and comparing it favorably to GPT-OSS-120B. Key topics include the immediate creation of GGUF quantized versions by groups like Unsloth, the desire for natively quantized models, performance testing on high-end hardware like the RTX 6000 Blackwell, and appreciation for Qwen's release of models in 'local-friendly' sizes.

**Tags**: `#large-language-models`, `#open-source-ai`, `#model-quantization`, `#ai-benchmarks`, `#huggingface`

---

<a id="item-5"></a>
## [Qwen3.5-122B-A10B outperforms GPT-5-mini and GPT-OSS-120B in comprehensive benchmark tests.](https://www.reddit.com/r/LocalLLaMA/comments/1rdmbhv/qwen35_the_middle_childs_122ba10b_benchmarks/) ⭐️ 8.0/10

The Qwen3.5-122B-A10B model has demonstrated superior performance against OpenAI's GPT-5-mini and the open-source GPT-OSS-120B across a range of key benchmarks. It achieved higher scores in knowledge (MMLU-Pro), STEM reasoning (GPQA Diamond), agentic tasks (BFCL-V4), and vision tasks (MathVision), establishing itself as the strongest overall performer among the three models. This result is significant as it shows a leading open-source model can match or exceed the performance of a proprietary model from a major AI lab like OpenAI in specific, demanding tasks. It provides a powerful, high-performing alternative for developers and researchers, potentially accelerating open-source AI development and offering more choice in model deployment. While Qwen3.5 leads in most areas, GPT-5-mini remains competitive in some coding benchmarks and translation tasks. A key caveat noted in the community is the difference in native quantization, as GPT-OSS-120B is natively 4-bit while Qwen3.5 is trained at a higher precision, which could affect performance comparisons under resource constraints like limited VRAM.

reddit · r/LocalLLaMA · carteakey · Feb 24, 17:18

**Background**: Qwen3.5 is the latest generation of the Qwen series of large language models, which includes both dense and Mixture-of-Experts (MoE) architectures. Benchmarks like MMLU-Pro and GPQA Diamond are standard tools for evaluating LLM capabilities; MMLU-Pro tests broad knowledge across multiple subjects, while GPQA Diamond is a highly challenging subset of questions designed to test deep, expert-level reasoning, particularly in STEM fields.

**Discussion**: Community sentiment is excited but measured, with discussions focusing on practical deployment and benchmark validity. Key points include concerns about chart readability, the importance of real-world testing beyond benchmarks, and questions about how the model's performance holds up under quantization for users with hardware constraints like 64GB of VRAM. Some users also expressed curiosity about its performance compared to the larger Qwen3-235B-A22B model.

**Tags**: `#large-language-models`, `#benchmarks`, `#open-source-ai`, `#model-comparison`, `#qwen`

---

<a id="item-6"></a>
## [Anthropic's blog on detecting distillation attacks sparks censorship and reliability concerns](https://www.reddit.com/gallery/1rd8cfw) ⭐️ 8.0/10

Anthropic published a blog post detailing how it detected and actively countered what it calls 'industrial-scale distillation attacks' by Chinese AI firms DeepSeek, Moonshot AI, and MiniMax. The company revealed it used output poisoning as a countermeasure against these attempts to extract knowledge from its proprietary models. This matters because it reveals how major AI companies may actively manipulate model outputs to sabotage competitors, raising serious questions about the reliability and integrity of responses from commercial AI services. It also intensifies the debate over corporate control versus open-source alternatives, potentially pushing users toward local, open-weight models they can trust. Anthropic's countermeasures involved poisoning outputs for specific requests, which could inadvertently affect legitimate users. The company frames these actions as necessary security measures but provides limited public evidence, such as a comprehensive data dump, to support its claims about the scale and nature of the attacks.

reddit · r/LocalLLaMA · obvithrowaway34434 · Feb 24, 06:07

**Background**: Model distillation is a technique where a smaller, student model is trained to mimic the outputs of a larger, teacher model, effectively transferring knowledge. In this context, a 'distillation attack' refers to unauthorized attempts to extract proprietary model capabilities, often via API queries. Open-weight models are AI models whose parameters (weights) are publicly released, allowing for local deployment and inspection, unlike closed-source models where both weights and internal workings are kept secret.

**Discussion**: The community reaction is highly critical, focusing on three main points: skepticism about the term 'attack' and the evidence presented, deep concern over the ethics of output poisoning and its impact on response reliability for all users, and strong criticism of Anthropic's corporate tone and perceived motives, including linking the issue to arguments for export controls on chips.

**Tags**: `#AI Ethics`, `#Model Security`, `#Corporate Censorship`, `#Open Source AI`, `#AI Policy`

---

<a id="item-7"></a>
## [U.S. Department of Defense Considers Ending Partnership with Anthropic Over AI Military Use Restrictions](https://t.me/zaihuapd/39845) ⭐️ 8.0/10

The U.S. Department of Defense is considering terminating its partnership with AI company Anthropic due to a fundamental disagreement over usage restrictions for the Claude AI models. The core conflict is that Anthropic insists on prohibiting the use of Claude for mass surveillance and fully autonomous weapons systems, while the DoD demands authorization for 'all lawful uses,' including weapons development and battlefield operations. This potential split highlights a critical tension between the ethical guardrails established by leading AI developers and the strategic demands of national defense, potentially setting a precedent for how governments procure and deploy advanced AI. It could impact the U.S. military's access to cutting-edge AI capabilities while reinforcing the growing industry debate on responsible AI development and the limits of commercial technology in warfare. The disagreement was reportedly exacerbated after Claude was used in a military operation targeting Venezuelan leader Nicolás Maduro, raising Anthropic's concerns about its technology being involved in live combat. Notably, competitors like OpenAI and Google have reportedly agreed to relax similar restrictions for the Defense Department, placing Anthropic in a more isolated ethical stance.

telegram · zaihuapd · Feb 25, 01:21

**Background**: Anthropic is an AI safety and research company known for developing the Claude family of large language models. A core tenet of Anthropic's approach is 'Constitutional AI,' a training method where the AI uses a set of written principles (a constitution) to critique and revise its own responses, aiming to build reliable and steerable systems. The Claude models, such as Claude 3 Opus, are advanced multimodal AI capable of complex reasoning, coding, and understanding text and images, and are available via APIs and cloud platforms.

**Tags**: `#AI Ethics`, `#Military Technology`, `#Government Policy`, `#Anthropic`, `#AI Governance`

---

<a id="item-8"></a>
## [Dog's random keyboard inputs generate playable games through AI scaffolding](https://www.calebleak.com/posts/dog-game/) ⭐️ 7.0/10

A developer conducted a humorous experiment where his dog's random keyboard presses were fed into an AI system that generated functional, playable games from the nonsensical input. The experiment demonstrates that modern development systems can produce working applications even from completely random or low-quality input. This experiment serves as powerful social commentary on how AI-assisted development has shifted the focus from precise human input to sophisticated system scaffolding. It raises questions about the diminishing importance of input quality in programming and whether we're approaching a point where the engineering work happens in the system architecture rather than the prompts. The experiment specifically highlights how LLM-based scaffolding systems can interpret and build upon even random keystrokes to create functional applications. The author notes that "the magic isn't in the input, it's in the system around it," suggesting that the real engineering work has shifted to creating robust development frameworks.

hackernews · cleak · Feb 24, 17:15

**Background**: AI code generation uses machine learning models to write code based on input that describes what the code should do. LLM scaffolding refers to structured frameworks that guide large language models to perform specific tasks, similar to how scaffolding in construction provides temporary support. Vibe coding is an informal development approach that emphasizes intuitive, rapid prototyping over meticulous planning.

**Discussion**: Commenters praised the experiment as brilliant social commentary, with one noting that "AI doesn't know or care if you're a dog" as long as you can provide input. Several users highlighted the key insight that "random keystrokes producing playable games means the input barely matters anymore," suggesting we've reached a point where engineering focus has shifted to system scaffolding rather than input quality.

**Tags**: `#AI`, `#Programming`, `#Social Commentary`, `#LLM`, `#Experiments`

---

<a id="item-9"></a>
## [Qwen3.5-35B-A3B demonstrates breakthrough performance for agentic coding on consumer-grade hardware.](https://www.reddit.com/r/LocalLLaMA/comments/1rdxfdu/qwen3535ba3b_is_a_gamechanger_for_agentic_coding/) ⭐️ 7.0/10

A user successfully ran the Qwen3.5-35B-A3B model, quantized to the MXFP4_MOE format, on a single RTX 3090 GPU using Llama.cpp. The model achieved over 100 tokens per second, utilized a 131k context window, and successfully completed complex, time-limited coding challenges that previously required more powerful AI systems. This demonstrates that high-performance agentic coding—where AI autonomously plans and executes complex software tasks—is now feasible on affordable, consumer-grade hardware. It significantly lowers the barrier to entry for developers and researchers wanting to experiment with or deploy advanced AI coding assistants locally, challenging the dominance of cloud-based, proprietary models. The model uses a Mixture-of-Experts (MoE) architecture with only 3 billion active parameters (A3B), enabling high efficiency. It was run using a specific MXFP4 quantization (approximately 4.25 bits per weight) which reduces memory footprint, allowing the 35B-parameter model to fit within the 24GB VRAM of an RTX 3090 while maintaining performance.

reddit · r/LocalLLaMA · jslominski · Feb 25, 00:04

**Background**: Agentic coding refers to AI systems that autonomously take a high-level instruction, break it into steps, and execute them using tools (like reading/writing files) to complete a software task, unlike traditional AI coding assistants that primarily suggest code snippets. The Qwen3.5 series is a family of open-weight large language models developed by Alibaba. Mixture-of-Experts (MoE) is an architecture where only a small subset of the model's total parameters (the 'experts') are activated for a given input, making large models more efficient to run.

**Discussion**: The community reaction is overwhelmingly positive, with multiple users replicating the high speed and successful task completion, expressing excitement about the model's performance on consumer hardware. A notable counterpoint mentions that an earlier 8-bit quantized version struggled with basic tool use, highlighting the importance of the specific MXFP4 quantization for optimal performance. There is also discussion about the model resolving persistent issues like 'readfile loops' present in earlier versions.

**Tags**: `#llm`, `#agentic-coding`, `#local-llm`, `#qwen`, `#hardware-performance`

---

<a id="item-10"></a>
## [New Qwen3.5 Model Variants Discovered: 27B Dense and 122B MoE](https://i.redd.it/h1c3uk0iwflg1.png) ⭐️ 7.0/10

New variants of the Qwen3.5 large language model series, including a 27-billion-parameter dense model and a 122-billion-parameter Mixture-of-Experts (MoE) model, have been discovered on the Qwen chat platform. This discovery indicates upcoming releases beyond the previously known model sizes. This matters because it shows Alibaba's Qwen team is actively innovating across the model size spectrum, offering both efficient dense models for constrained hardware and powerful MoE models for high-performance tasks. It provides more options for developers and researchers, filling gaps in the mid-to-large model range and intensifying competition in the open-source AI landscape. The 122B MoE model's parameter count suggests it is designed for systems with substantial memory, with community members noting it would be suitable for setups with 128GB of RAM. The 27B dense model represents a continuation of the 'medium-sized' model category, which is prized for offering a good balance of performance and resource requirements.

reddit · r/LocalLLaMA · AaronFeng47 · Feb 24, 12:55

**Background**: Qwen is a series of open-source large language models developed by Alibaba Cloud. 'Dense' models, like GPT-3, activate all parameters for every input, leading to a direct relationship between parameter count and computational cost. In contrast, 'Mixture-of-Experts' models are 'sparse'; they contain a large total parameter pool (e.g., hundreds of billions) but for each input, only a small subset of specialized 'expert' sub-networks are activated, making them computationally more efficient at scale. The Qwen3.5 series is known for its hybrid architecture integrating linear attention and sparse MoE.

**Discussion**: The community reaction is overwhelmingly positive and excited, with users expressing surprise at the 27B dense model and high anticipation for the 122B MoE model. Key discussion points include appreciation for the continued development of medium-sized dense models, speculation about hardware requirements (with users calculating VRAM/RAM needs), and hopes for future releases in the 3B-12B range. There is also a sentiment that these models fill a gap left by other projects.

**Tags**: `#llm`, `#qwen`, `#model-release`, `#moe`, `#open-source-ai`

---

<a id="item-11"></a>
## [Liquid AI releases LFM2-24B-A2B, a 24B parameter sparse MoE model for efficient edge inference.](https://i.redd.it/28drgi3ufglg1.png) ⭐️ 7.0/10

Liquid AI has released LFM2-24B-A2B, a 24-billion-parameter sparse Mixture-of-Experts (MoE) model with only 2.3 billion active parameters per token, making it their largest LFM2 model to date. The model is designed to run within 32GB of RAM and is available as an open-weight instruct model on Hugging Face. This release demonstrates the effective scaling of Liquid AI's hybrid architecture to a much larger size while maintaining efficient inference, a key requirement for deploying powerful AI models on consumer hardware at the edge. It represents a significant step towards making high-capacity, energy-efficient AI accessible for local and on-device applications, potentially expanding the reach of advanced AI beyond data centers. The model features a 40-layer MoE architecture with 64 experts per block and top-4 routing, and it shows log-linear quality improvements across benchmarks like MMLU-Pro and GSM8K as model size scales. It is important to note that this is a preview release, as pre-training on 17 trillion tokens is still ongoing, with a more complete LFM2.5 version expected later.

reddit · r/LocalLLaMA · PauLabartaBajo · Feb 24, 14:43

**Background**: A sparse Mixture-of-Experts (MoE) architecture is a technique where a model consists of many specialized sub-networks ('experts'), but for each input token, only a small, selected subset (e.g., top-4) is activated. This allows the total parameter count to grow very large (encompassing vast knowledge) while keeping the computational cost per token relatively low, as only a fraction of parameters are used. The GGUF format mentioned is a quantization file format designed for efficient execution, particularly on CPUs and Apple Silicon, by reducing model size and memory requirements.

**Discussion**: The community shows excitement about the model's potential for fast, efficient edge inference and its scaling from smaller versions, but there is a strong call for more detailed and independent benchmarks to compare its performance against models like Mixtral or GPT-OSS 20B. Several users clarified that this is a preview release, with pre-training still ongoing, and some noted humorous typos in the announcement while others reported mixed initial test results.

**Tags**: `#Mixture-of-Experts`, `#Efficient-Inference`, `#Model-Release`, `#Sparse-Models`, `#Edge-AI`

---

<a id="item-12"></a>
## [Unitree Robotics Releases Unitree As2 Quadruped Robot for Industrial Applications](https://weibo.com/1818617132/QtjToeQFh) ⭐️ 7.0/10

Unitree Robotics has officially launched the Unitree As2, a compact quadruped robot featuring a high peak torque of 90 N·m, a battery life exceeding 4 hours when unloaded, an IP54 rating for dust and water resistance, and a payload capacity of 15 kg with a range of over 13 km. The company also emphasizes its open development ecosystem to enable secondary development for industry-specific applications. This release represents a significant step in making advanced, high-performance quadruped robotics more accessible for industrial automation, inspection, and logistics tasks. The combination of high torque, long endurance, and an open ecosystem could accelerate the adoption of legged robots in real-world scenarios beyond research labs. Key technical specifications include the 90 N·m torque for powerful movement, an IP54 rating which protects against limited dust ingress and water splashes from any direction, and a notable trade-off where the 15 kg payload significantly reduces the operational range to 13 km compared to the 4+ hour unloaded runtime. The 'open development ecosystem' suggests the platform provides APIs or SDKs for custom application development.

telegram · zaihuapd · Feb 24, 10:09

**Background**: Quadruped robots, inspired by animals like dogs, use legs for locomotion, offering advantages over wheeled robots in traversing rough, uneven, or cluttered terrain common in industrial and outdoor environments. Locomotion control is a core challenge, often involving methods like virtual model control or impedance control to achieve stable and adaptive walking. An IP (Ingress Protection) rating is an international standard that classifies the level of sealing effectiveness of electrical enclosures against dust and water.

**Tags**: `#robotics`, `#quadruped-robot`, `#hardware`, `#industrial-automation`, `#unitree`

---