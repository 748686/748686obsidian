---
layout: default
title: "Horizon Summary: 2026-07-29 (EN)"
date: 2026-07-29
lang: en
---

> From 47 items, 11 important content pieces were selected

---

1. [Document-borne AI worm self-propagates through Copilot for Word](#item-1) ⭐️ 9.0/10
2. [TurboFieldfare: Run Gemma 4 26B on M-series Mac with 2GB RAM](#item-2) ⭐️ 8.0/10
3. [Mitchell Hashimoto Announces Superlogical](#item-3) ⭐️ 8.0/10
4. [Kimi K3-256k Model: Half Price, Same Quality](#item-4) ⭐️ 8.0/10
5. [Handbook.md Benchmark Reveals LLM Agents Fail on Long Policies](#item-5) ⭐️ 8.0/10
6. [Cryptographer Green: AI&\#x27;s moment in post-quantum transition](#item-6) ⭐️ 8.0/10
7. [GCC Steering Committee Adopts AI Contributions Policy](#item-7) ⭐️ 8.0/10
8. [Vendor-agnostic ML inference on edge devices via ncnn Vulkan](#item-8) ⭐️ 8.0/10
9. [Russia&\#x27;s FSB Charges Telegram Founder with Aiding Terrorism](#item-9) ⭐️ 8.0/10
10. [Hugging Face Widely Used for Deepfake Nudes: Report](#item-10) ⭐️ 8.0/10
11. [Moonshot AI Raises $3.5B at $35B Valuation After Kimi K3 Model](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Document-borne AI worm self-propagates through Copilot for Word](https://enklypesalt.com/posts/context-collapse-part3-ai-worming-through-word/) ⭐️ 9.0/10

Researcher Håkon Måløy demonstrated a novel prompt injection technique that turns Microsoft Copilot for Word into a self-replicating AI worm, capable of spreading malicious instructions across documents without user intervention. This discovery reveals a critical security gap in AI-integrated productivity tools, showing that AI agents can be weaponized to autonomously propagate attacks, potentially affecting enterprises and individuals relying on Copilot for daily work. The worm operates by hiding adversarial instructions in document content—such as white text or Unicode tricks—which Copilot interprets as user commands, leading to payload execution and propagation to new documents via email or sharing. No robust mitigation exists as of publication.

hackernews · Canopy9560 · Jul 29, 11:44 · [Discussion](https://news.ycombinator.com/item?id=49096188)

**Background**: Prompt injection attacks exploit the inability of large language models \(LLMs\) to distinguish between user instructions and untrusted data. AI worms are a new class of malware that use LLMs to autonomously spread across systems. Microsoft Copilot for Word can process text in documents as part of its context, making it vulnerable to such injections.

<details><summary>References</summary>
<ul>
<li><a href="https://enklypesalt.com/posts/context-collapse-part3-ai-worming-through-word/">Context Collapse, Part 3 - AI Worming through Word | En Klype Salt</a></li>
<li><a href="https://thehackernews.com/2026/06/researchers-build-self-replicating-ai.html">Researchers Build Self-Replicating AI Worm That Operates Entirely on Local, Open-Weight Models</a></li>
<li><a href="https://www.infosecurity-magazine.com/news/worm-created-generative-ai-systems/">Self-Propagating Worm Created to Target Generative AI Systems - Infosecurity Magazine</a></li>

</ul>
</details>

**Discussion**: Commenters expressed strong concern, noting that mixing instructions with data is an inherent design flaw that cannot be easily fixed. Some predicted the situation will worsen as users grant excessive access to AI agents. Others shared practical tricks like white text injection that already bypass defenses.

**Tags**: `#AI security`, `#LLM attacks`, `#Copilot`, `#adversarial attacks`, `#software vulnerabilities`

---

<a id="item-2"></a>
## [TurboFieldfare: Run Gemma 4 26B on M-series Mac with 2GB RAM](https://github.com/drumih/turbo-fieldfare) ⭐️ 8.0/10

TurboFieldfare is an open-source inference engine written in Swift and Metal that runs a 4-bit quantized Gemma 4 26B-A4B-IT model on M-series Macs using only about 2GB of RAM, by streaming Mixture-of-Experts weights from SSD. It achieves 5–6 tok/s on an 8GB M2 MacBook Air and 31–35 tok/s on an M5 MacBook Pro. This innovation makes powerful large language models accessible on consumer hardware without expensive memory upgrades, potentially democratizing on-device AI for Mac users. It also demonstrates a practical approach to SSD offloading for MoE models, which could influence future inference engine design. The model&\#x27;s 4-bit quantized weights occupy roughly 14GB, but TurboFieldfare keeps only shared layers and KV cache in RAM while streaming routed experts from SSD using bounded parallel pread and a small expert cache. The engine includes an experimental OpenAI-compatible local server with streaming and tool call support.

hackernews · gitpusher42 · Jul 29, 15:05 · [Discussion](https://news.ycombinator.com/item?id=49098510)

**Background**: Gemma 4 26B is a Mixture-of-Experts \(MoE\) model where only a subset of parameters \(experts\) are activated per token, making it more efficient than dense models. 4-bit quantization compresses model weights to reduce memory footprint, while SSD offloading stores rarely used weights on disk and loads them on demand. These techniques together allow running models that would otherwise require far more RAM.

<details><summary>References</summary>
<ul>
<li><a href="https://www.datacamp.com/blog/mixture-of-experts-moe">What Is Mixture of Experts ( MoE )? How It Works, Use... | DataCamp</a></li>
<li><a href="https://huggingface.co/blog/moe">Mixture of Experts Explained</a></li>
<li><a href="https://arxiv.org/pdf/2508.06978">SSD Offloading for LLM Mixture-of-Experts Weights Considered...</a></li>

</ul>
</details>

**Discussion**: Community members noted similarities to llama.cpp&\#x27;s mmap approach but praised TurboFieldfare&\#x27;s expert-specific SSD streaming optimization. One user reported successful compilation on M1 MBA with a minor code tweak, achieving similar speed. Another developer expressed interest in collaborating on a DiffusionGemma project, suggesting potential synergy.

**Tags**: `#inference engine`, `#on-device AI`, `#Gemma`, `#model optimization`, `#open source`

---

<a id="item-3"></a>
## [Mitchell Hashimoto Announces Superlogical](https://www.superlogical.com/) ⭐️ 8.0/10

Mitchell Hashimoto, creator of Ghostty, has announced Superlogical, a new company that will build on the open source libghostty library, after transferring ownership of Ghostty to a non-profit organization. This move sets an exemplary model for open source sustainability, where the core project is owned by a non-profit while a commercial entity builds proprietary products on top of the same open source foundation, ensuring community benefit and commercial viability. Superlogical will consume the same MIT-licensed libghostty components available to everyone else and plans to upstream shared terminal improvements. The company aims to build terminal applications using libghostty as a public building block.

hackernews · yan · Jul 29, 15:41 · [Discussion](https://news.ycombinator.com/item?id=49098965)

**Background**: Ghostty is a fast, feature-rich, cross-platform terminal emulator using platform-native UI and GPU acceleration. libghostty is an embeddable C-compatible library that allows any application to integrate a full Ghostty terminal emulator. By transferring Ghostty to a non-profit, Hashimoto ensures the core remains community-governed.

<details><summary>References</summary>
<ul>
<li><a href="https://ghostty.org/">Ghostty</a></li>
<li><a href="https://github.com/ghostty-org/ghostty">GitHub - ghostty-org/ghostty: 👻 Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration.</a></li>
<li><a href="https://mitchellh.com/writing/libghostty-is-coming">Libghostty Is Coming - Mitchell Hashimoto</a></li>

</ul>
</details>

**Discussion**: The community largely praised the open source licensing and architecture, with user simonw highlighting the model of building a company on an open source dependency owned by a non-profit. Some commenters, like rixed, criticized the enigmatic title, while others drew parallels to OLE/COM or shared related projects.

**Tags**: `#open source`, `#terminal`, `#software engineering`, `#ghostty`, `#mitchell hashimoto`

---

<a id="item-4"></a>
## [Kimi K3-256k Model: Half Price, Same Quality](https://www.kimi.com/code/docs/en/kimi-code/models) ⭐️ 8.0/10

Moonshot AI released the K3-256k model, a 256K context version of its K3 model, at half the quota cost of the original 1M context version. This price cut makes advanced coding assistance more accessible, fueling the commoditization of large language models and pressuring competitors like OpenAI. The K3-256k delivers identical results to the full K3 within 256K context; previously, 1M context was limited to higher-tier plans, while 256K is available on the Moderato plan.

hackernews · monneyboi · Jul 29, 19:25 · [Discussion](https://news.ycombinator.com/item?id=49101852)

**Background**: Kimi K3 is a 2.8 trillion parameter open-weight multimodal reasoning model with a 1M token context window, capable of frontier performance in coding and reasoning. Many coding tasks rarely exceed 200K context, making a cheaper 256K variant practical for most users.

<details><summary>References</summary>
<ul>
<li><a href="https://www.kimi.com/code/docs/en/kimi-code/models">Model Configuration | Kimi Code Docs</a></li>
<li><a href="https://openrouter.ai/moonshotai/kimi-k3">Kimi K3 - API Pricing &amp; Benchmarks | OpenRouter</a></li>

</ul>
</details>

**Discussion**: Users welcomed the lower price, with comments noting that 1M context is often unnecessary and describing LLMs as rapidly becoming commodities. Some appreciated staying under 200K context personally.

**Tags**: `#AI`, `#LLM`, `#cost-efficiency`, `#coding assistant`, `#context window`

---

<a id="item-5"></a>
## [Handbook.md Benchmark Reveals LLM Agents Fail on Long Policies](https://arxiv.org/abs/2607.25398) ⭐️ 8.0/10

A new paper, &\#x27;HANDBOOK.md,&\#x27; introduces a benchmark of 65 tasks derived from real employee handbooks and finds that LLM agents fail to reliably follow long policy documents, with performance declining as context length increases. This finding underscores a critical reliability gap for LLM agents deployed in real-world scenarios like customer service and coding assistants, where adhering to lengthy policy instructions is essential; it challenges the practical utility of long-context models for agentic tasks. The benchmark uses real employee handbooks to create 65 tasks, and agents consistently ignore or misinterpret policies, with accuracy dropping sharply as documents grow longer; the paper corroborates known long-context limitations, such as the KV cache bottleneck and poor sampling.

hackernews · spIrr · Jul 29, 13:01 · [Discussion](https://news.ycombinator.com/item?id=49096969)

**Background**: Long-context LLMs claim to support millions of tokens, but research shows they effectively use only 10-20% of the context, especially in complex tasks. The &\#x27;needle in a haystack&\#x27; problem persists: models struggle to locate and apply relevant information from long texts. This paper tests a practical agentic scenario where agents must follow a handbook&\#x27;s rules while performing tasks, revealing that even state-of-the-art models cannot reliably do so.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2607.25398">[2607.25398] HANDBOOK . md : A Benchmark for Long-Context Agentic...</a></li>
<li><a href="https://neurips.cc/virtual/2024/poster/97462">Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack</a></li>
<li><a href="https://ai-tldr.dev/releases/surge-ai-handbook-benchmark/">HANDBOOK . md — Surge AI benchmark keeps frontier... | AI/TLDR</a></li>

</ul>
</details>

**Discussion**: Commenters largely agree with the findings. One user notes that even with explicit instructions in CLAUDE.md, Claude ignores them after sustained interaction, suggesting a practical &\#x27;forgetting&\#x27; effect. Another argues that agentic AI requires extensive RL post-training on domain-specific data, and without it, long-context adherence fails. The discussion reflects a consensus that long-context reliability remains a major unsolved problem.

**Tags**: `#LLM`, `#long-context`, `#AI agents`, `#policy`, `#benchmark`

---

<a id="item-6"></a>
## [Cryptographer Green: AI&\#x27;s moment in post-quantum transition](https://simonwillison.net/2026/Jul/29/matthew-green/#atom-everything) ⭐️ 8.0/10

Matthew Green highlights that the ongoing migration from traditional public-key algorithms to post-quantum algorithms creates a perfect window for AI to advance cryptanalysis, potentially strengthening confidence in new cryptographic problems. This intersection of a historic cryptographic transition and emerging AI capabilities could reshape security standards and validation of post-quantum algorithms, affecting future encryption practices globally. Green references the HAWK signature scheme as an example of new standards, and notes the possibility of AI undermining hard problems or living in Impagliazzo&\#x27;s Minicrypt world.

rss · Simon Willison · Jul 29, 18:18

**Background**: Post-quantum cryptography \(PQC\) refers to algorithms resistant to quantum computer attacks. The transition is driven by the need to replace RSA and elliptic-curve cryptosystems. Impagliazzo&\#x27;s Five Worlds classify cryptographic possibilities; Minicrypt implies one-way functions exist but no public-key cryptography. AI&\#x27;s role in cryptanalysis could help verify the security of new PQC schemes.

<details><summary>References</summary>
<ul>
<li><a href="https://blog.computationalcomplexity.org/2004/06/impagliazzos-five-worlds.html">Computational Complexity: Impagliazzo&#x27;s Five Worlds</a></li>
<li><a href="https://ieeexplore.ieee.org/document/11433250">Post - Quantum HAWK Signature Acceleration with... | IEEE Xplore</a></li>
<li><a href="https://theunum.io/en/news/read/claude-has-identified-theoretical-vulnerabilities-in-post-quantum-encryption-algorithms">Claude has identified theoretical vulnerabilities in post - quantum ...</a></li>

</ul>
</details>

**Tags**: `#cryptography`, `#post-quantum`, `#AI`, `#cryptanalysis`

---

<a id="item-7"></a>
## [GCC Steering Committee Adopts AI Contributions Policy](https://lwn.net/Articles/1086041/) ⭐️ 8.0/10

The GCC steering committee has adopted a policy that rejects legally significant contributions containing LLM-generated content, defining &\#x27;legally significant&\#x27; as around 15 lines of code or text. This policy was recommended by the GCC AI policy working group. This policy sets a precedent for other open-source projects grappling with AI-generated code, addressing copyright and legal concerns. It impacts GCC contributors and maintainers, potentially altering how LLMs are used in compiler development. The policy does not prohibit LLM use for research, analysis, bug discovery, and patch review, as long as the output is not included in contributions. However, maintainers may accept legally significant test cases generated by an LLM at their discretion.

rss · LWN.net · Jul 29, 14:38

**Background**: GCC \(GNU Compiler Collection\) is a major open-source compiler project supporting multiple programming languages. Like many open-source projects, GCC relies on clear contribution policies to ensure legal clarity and software quality. The rise of AI-assisted coding has prompted new policies to address copyright and originality concerns, especially for legally significant contributions where copyrightability is a factor.

<details><summary>References</summary>
<ul>
<li><a href="https://www.phoronix.com/news/GCC-Working-Group-AI-Policy">GCC Establishes Working Group To Decide On AI/LLM Policy - Phoronix</a></li>

</ul>
</details>

**Tags**: `#GCC`, `#AI policy`, `#open source`, `#compiler`, `#LLM`

---

<a id="item-8"></a>
## [Vendor-agnostic ML inference on edge devices via ncnn Vulkan](https://www.reddit.com/r/MachineLearning/comments/1v9s4mz/vendoragnostic_ml_inference_on_production_edge/) ⭐️ 8.0/10

The author demonstrates vendor-agnostic ML inference on production edge devices using ncnn&\#x27;s Vulkan backend, achieving a 10x speedup over ONNX CPU inference on an NVIDIA 4070 for face embedding and detection models. This approach eliminates vendor lock-in and the need for users to install proprietary runtimes, making GPU-accelerated ML inference practical across diverse hardware \(NVIDIA, AMD, Intel, Apple Silicon\) on edge devices. On an RTX 4070, ArcFace R50 drops from 30 ms \(ONNX CPU\) to 3 ms \(ncnn Vulkan\), and SCRFD face detection from 25 ms to 2.5 ms. Model size also halves from 174 MB \(ONNX fp32\) to 87 MB \(ncnn fp16 weight storage\).

reddit · r/MachineLearning · /u/ppchaos · Jul 29, 10:22

**Background**: ncnn is a high-performance neural network inference framework optimized for mobile, embedded, and desktop platforms with no third-party runtime dependencies. Vulkan is a cross-platform GPU API that provides a unified compute interface across vendors, enabling GPU acceleration without vendor-specific code. The combination allows developers to run ML models on any GPU without forcing users to install extra runtimes.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/Tencent/ncnn">GitHub - Tencent/ncnn: ncnn is a high-performance neural network inference framework optimized for the mobile platform · GitHub</a></li>
<li><a href="https://sourceforge.net/projects/ncnn.mirror/">ncnn download | SourceForge.net</a></li>
<li><a href="https://pypi.org/project/ncnn/">ncnn · PyPI</a></li>

</ul>
</details>

**Tags**: `#machine-learning`, `#inference`, `#vulkan`, `#edge-devices`, `#cross-platform`

---

<a id="item-9"></a>
## [Russia&\#x27;s FSB Charges Telegram Founder with Aiding Terrorism](https://www.interfax.ru/russia/1106228) ⭐️ 8.0/10

Russia&\#x27;s Federal Security Service \(FSB\) has filed criminal charges against Telegram founder Pavel Durov under Article 205.1.1.1 of the Criminal Code \(aiding terrorism\) and placed him on an international wanted list. This escalates state-level action against a major tech platform founder, setting a precedent for holding platform leaders personally responsible for user-generated content and raising concerns about censorship and international law enforcement. The FSB alleges that Telegram&\#x27;s management failed to remove channels, groups, and bots used by Ukrainian intelligence and terrorist organizations to plan and coordinate attacks, causing numerous casualties and billions of rubles in damages.

telegram · zaihuapd · Jul 29, 05:56

**Background**: Telegram is a widely used messaging platform known for its strong encryption and privacy features. Pavel Durov, its founder, has been a vocal advocate for free speech and has resisted government censorship demands. This charge stems from his refusal to comply with Russian authorities&\#x27; requests to remove content deemed related to terrorism.

**Tags**: `#Telegram`, `#Pavel Durov`, `#Russia`, `#cybersecurity`, `#legal`

---

<a id="item-10"></a>
## [Hugging Face Widely Used for Deepfake Nudes: Report](https://www.theverge.com/ai-artificial-intelligence/971723/hugging-face-nudify-deepfake-undress-women-children) ⭐️ 8.0/10

A report by European nonprofit AI Forensics, released on July 28, finds that Hugging Face, a major open-source model hosting platform, is extensively used to generate non-consensual deepfake nude images, with minimal safeguards in place. This highlights serious ethical and security flaws in AI model hosting platforms, potentially affecting millions of users and prompting stricter regulations on deepfake content moderation. The report set up honeypots that received over 1,000 requests in seven days, with 73% involving sexual content and nearly 7% targeting children. Among the top nine image-editing models, seven could easily undress women with simple prompts.

telegram · zaihuapd · Jul 29, 08:20

**Background**: Hugging Face is a popular platform for hosting and sharing machine learning models, including image generation models. Deepfake technology uses AI to create realistic but fake images or videos. Honeypots are decoy systems set up to attract and monitor malicious activity. Prompt filtering and output scanning are common safety measures to block harmful content generation.

<details><summary>References</summary>
<ul>
<li><a href="https://developer.aliyun.com/article/214627">《网络 空 间 欺骗：构筑欺骗防御的科学基石》一2.2.1 基于Honey...</a></li>
<li><a href="https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/cue-word-attack-protection">防护规则模板-Web应用防火墙(WAF) - 阿里云帮助文档</a></li>
<li><a href="https://i-newcar.com/index.php?m=home&amp;c=View&amp;a=index&amp;aid=4575">【突破性研究】通过提示词重写越狱文本到视频系统：语义保留攻击揭示模型安全过滤器脆弱性_牛喀网-具身智能开发者生态</a></li>

</ul>
</details>

**Tags**: `#AI ethics`, `#deepfake`, `#platform safety`, `#content moderation`, `#Hugging Face`

---

<a id="item-11"></a>
## [Moonshot AI Raises $3.5B at $35B Valuation After Kimi K3 Model](https://www.bloomberg.com/news/articles/2026-07-29/china-s-moonshot-ai-passes-funding-goal-to-hit-35-billion-value) ⭐️ 8.0/10

Moonshot AI, a Chinese AI startup, raised $3.5 billion in a funding round that values the company at $35 billion, far exceeding its initial target. The round was driven by the success of its Kimi K3 model, which approaches frontier AI performance and caused a market selloff upon release. This funding signals China&\#x27;s growing ability to produce frontier AI models, with Kimi K3 being one of the largest open-source models at 2.8 trillion parameters. It also marks a &\#x27;DeepSeek moment&\#x27; for the industry, indicating that Chinese AI companies can now compete with top US labs. Moonshot AI has already started a new funding round with a pre-money valuation of $50 billion and plans an IPO in Hong Kong this year. The company&\#x27;s annualized recurring revenue reached $300 million in June, and daily sales grew at least 6x after the K3 launch.

telegram · zaihuapd · Jul 29, 10:12

**Background**: Moonshot AI is a Chinese artificial intelligence startup known for developing the Kimi series of large language models. The Kimi K3 model, with 2.8 trillion parameters and a 1-million-token context window, uses a hybrid linear attention mechanism called Kimi Delta Attention. A &\#x27;DeepSeek moment&\#x27; refers to a market selloff triggered by the release of a high-performance open-source AI model from China, following the precedent set by DeepSeek in early 2025.

<details><summary>References</summary>
<ul>
<li><a href="https://www.kimi.com/blog/kimi-k3">Kimi K 3 Tech Blog: Open Frontier Intelligence</a></li>
<li><a href="https://www.siliconflow.com/models/kimi-k3">SiliconFlow – AI Infrastructure for LLMs &amp; Multimodal Models</a></li>
<li><a href="https://www.linkedin.com/pulse/why-we-wont-see-another-deepseek-moment-anytime-soon-breitenother-lzvwe">Why we won’t see another DeepSeek moment anytime soon</a></li>

</ul>
</details>

**Tags**: `#AI`, `#funding`, `#Moonshot AI`, `#Kimi K3`, `#China AI`

---