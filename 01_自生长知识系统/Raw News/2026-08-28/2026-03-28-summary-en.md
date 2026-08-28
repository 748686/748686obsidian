---
layout: default
title: "Horizon Summary: 2026-03-28 (EN)"
date: 2026-03-28
lang: en
---

> From 36 items, 16 important content pieces were selected

---

1. [Telnyx Python package on PyPI compromised with malicious code](#item-1) ⭐️ 9.0/10
2. [GLM-5.1 launches with coding performance matching Claude Opus 4.5](#item-2) ⭐️ 9.0/10
3. [Google's TurboQuant AI compression algorithm reduces LLM memory usage by 6x without quality loss.](#item-3) ⭐️ 9.0/10
4. [LiteLLM compromise reveals multiple security failures in software supply chain](#item-4) ⭐️ 8.0/10
5. [Skipping 90% of KV dequantization boosts decode speed by 22.8% in llama.cpp TurboQuant](#item-5) ⭐️ 8.0/10
6. [Gemini Pro leaks internal chain-of-thought and gets stuck in infinite loop](#item-6) ⭐️ 8.0/10
7. [TurboQuant adaptation achieves near-lossless 4+4 residual quantization for LLM weights with 3.2× memory savings](#item-7) ⭐️ 8.0/10
8. [Typia Infrastructure Achieves 100% Function Calling Success on Recursive Union Types with Qwen](#item-8) ⭐️ 8.0/10
9. [China Computer Federation opposes NeurIPS 2026 sanctions-based submission restrictions, calls for boycott](#item-9) ⭐️ 8.0/10
10. [Huawei launches Atlas 350 AI accelerator with Ascend 950PR, claiming 2.87x performance of NVIDIA H20](#item-10) ⭐️ 8.0/10
11. [AI-Powered Port of JSONata to Go in a Day Saves $500K Annually](#item-11) ⭐️ 7.0/10
12. [Long Appendices in Conference Papers Challenge Page Limit Purpose](#item-12) ⭐️ 7.0/10
13. [GLM 5.1, a major open-source language model, has been released.](#item-13) ⭐️ 7.0/10
14. [Unsloth Studio Beta receives major update with 50+ new features including faster inference and AMD support](#item-14) ⭐️ 7.0/10
15. [Google introduces system-level VPN split tunneling in Android 17 Beta 3](#item-15) ⭐️ 7.0/10
16. [Apple provides FBI with real user data linked to anonymous iCloud email in threat investigation](#item-16) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Telnyx Python package on PyPI compromised with malicious code](https://lwn.net/Articles/1065059/) ⭐️ 9.0/10

Two versions of the telnyx package (4.87.1 and 4.87.2) published to PyPI on March 27, 2026, contain malicious code injected into telnyx/_client.py, which downloads second-stage payloads hidden in WAV audio files from a remote server. The package averages over 1 million downloads per month, making this a high-impact supply chain compromise. This compromise poses significant security risks to a wide range of Python users and projects, as telnyx is a widely-used package with over 1 million monthly downloads, potentially leading to credential theft on Linux/macOS or persistent malware on Windows. It highlights the growing threat of supply chain attacks in open-source ecosystems, emphasizing the need for enhanced security measures in package repositories like PyPI. The malicious code downloads a second-stage binary hidden inside WAV audio files using steganography techniques, then either drops a persistent executable on Windows or harvests credentials on Linux/macOS. The attack specifically targets versions 4.87.1 and 4.87.2, published on March 27, 2026, indicating a targeted supply chain injection.

rss · LWN.net · Mar 27, 16:21

**Background**: PyPI (Python Package Index) is the official repository for Python packages, where developers publish and install software libraries, but it is vulnerable to supply chain attacks where malicious actors inject code into legitimate packages. Second-stage payloads in malware refer to a technique where an initial dropper downloads additional malicious components from a remote server to evade detection and execute more complex attacks. WAV file steganography involves hiding data, such as malware binaries, within audio files by manipulating bits like the least significant bit (LSB) to conceal payloads from security scanners.

<details><summary>References</summary>
<ul>
<li><a href="https://bolster.ai/blog/pypi-supply-chain-attacks">PYPI Security: How to Prevent Supply Chain Attacks in Python Projects</a></li>
<li><a href="https://www.scaler.com/topics/cyber-security/staged-vs-non-staged-payloads/">Staged vs Non-staged Payloads in Cybersecurity - Scaler Malware Payloads & Beacons: Types of Malicious Payloads - Illumio Malware Development with NIM — Staged Payloads - Medium MintsLoader Malware Analysis: Multi-Stage Loader Used by TAG ... Stage Capabilities: Upload Malware, Sub-technique T1608.001 ... Staging vs Stageless payloads - Which one is Better? Malware Payloads & Beacons: Types of Malicious Payloads - Illumio Analyzing New HijackLoader Evasion Tactics - Zscaler Stage Capabilities: Upload Malware , Sub-technique T1608.001 Staged vs Non-staged Payloads in Cybersecurity - Scaler New HijackLoader Evasion Tactics | ThreatLabz - Zscaler</a></li>
<li><a href="https://github.com/LiquidFun/stegowav">GitHub - LiquidFun/stegowav: Hide information in the wave ...</a></li>

</ul>
</details>

**Tags**: `#security`, `#supply-chain`, `#PyPI`, `#malware`, `#Python`

---

<a id="item-2"></a>
## [GLM-5.1 launches with coding performance matching Claude Opus 4.5](https://i.redd.it/ewzmimtzmlrg1.png) ⭐️ 9.0/10

Zhipu AI has released GLM-5.1, its latest flagship model, which achieves state-of-the-art coding performance among open-source models with scores of 77.8 on SWE-bench-Verified and 56.2 on Terminal Bench 2.0. The model is now available to all Coding Plan users on Zhipu AI's platform. This represents a significant advancement for open-source AI models, as GLM-5.1's coding capabilities now approach those of leading proprietary models like Claude Opus 4.5, potentially democratizing access to high-quality coding assistance. The breakthrough could accelerate software development workflows and make sophisticated AI coding tools more accessible to developers worldwide. GLM-5.1 features a 200K context window with 128K max output, 744B parameters (40B activated), and was trained on 28.5 trillion tokens of data. The model also includes native support for the Model Context Protocol (MCP), enabling better integration with external tools and systems.

reddit · r/LocalLLaMA · Which-Jello9157 · Mar 27, 14:37

**Background**: SWE-bench-Verified is a benchmark that evaluates AI models' ability to solve real-world software engineering problems, though it uses static datasets that may not reflect current development practices. Terminal Bench 2.0 tests AI agents' performance in command-line interface environments with tasks inspired by real workflows. The Model Context Protocol (MCP) is an open standard introduced by Anthropic in 2024 that standardizes how AI systems integrate with external tools and data sources.

<details><summary>References</summary>
<ul>
<li><a href="https://openai.com/index/introducing-swe-bench-verified/">Introducing SWE-bench Verified | OpenAI</a></li>
<li><a href="https://www.tbench.ai/">Terminal-Bench 2.0</a></li>
<li><a href="https://en.wikipedia.org/wiki/Model_Context_Protocol">Model Context Protocol - Wikipedia</a></li>

</ul>
</details>

**Discussion**: The Reddit discussion shows high community interest with 347 upvotes and an 89% upvote ratio, indicating strong validation of the model's significance. Users are asking for practical comparisons with Claude 4.6 for real production coding tasks, suggesting interest in hands-on testing and real-world performance evaluation.

**Tags**: `#AI`, `#Large Language Models`, `#Software Engineering`, `#Open Source`, `#Benchmarks`

---

<a id="item-3"></a>
## [Google's TurboQuant AI compression algorithm reduces LLM memory usage by 6x without quality loss.](https://www.reddit.com/r/LocalLLaMA/comments/1s57ky1/googles_turboquant_aicompression_algorithm_can/) ⭐️ 9.0/10

Google recently revealed TurboQuant, a compression algorithm that can reduce the memory usage of large language models (LLMs) by 6 times without sacrificing output quality, as reported in March 2026. This breakthrough could enable frontier models to run on consumer hardware. This development is significant because it addresses a major bottleneck in AI deployment by drastically lowering memory requirements, potentially making cutting-edge models accessible on local devices like personal computers. It aligns with broader industry trends toward efficiency-focused research, such as model compression and hardware optimization, to reduce costs and environmental impact. TurboQuant achieves a 6x reduction in memory usage while maintaining output quality, unlike some other compression methods that degrade performance. However, specific technical details, such as compatibility with different LLM architectures or implementation requirements, are not fully disclosed in the initial reports.

reddit · r/LocalLLaMA · Resident_Party · Mar 27, 15:37

**Background**: Large language models (LLMs) are AI systems that process and generate human-like text, but they often require significant memory and computational resources, limiting deployment to high-end hardware. Memory optimization techniques, such as compression, aim to reduce GPU and RAM usage without sacrificing performance, balancing accuracy, memory, and efficiency. Frontier models represent the cutting edge of AI capabilities, typically demanding extensive resources for training and inference, which has spurred interest in efficiency improvements for broader accessibility.

<details><summary>References</summary>
<ul>
<li><a href="https://arstechnica.com/ai/2026/03/google-says-new-turboquant-compression-can-lower-ai-memory-usage-without-sacrificing-quality/">Google's TurboQuant AI-compression algorithm can reduce</a></li>
<li><a href="https://mljourney.com/llm-memory-optimization-reducing-gpu-and-ram-usage-for-inference/">LLM Memory Optimization : Reducing GPU and RAM Usage for...</a></li>
<li><a href="https://epoch.ai/data-insights/consumer-gpu-model-gap">Frontier AI capabilities can be run at home within a year or less | Epoch AI</a></li>

</ul>
</details>

**Discussion**: The Reddit discussion shows high community interest, with users speculating about the possibility of running frontier models at home and engaging in practical debates about deployment challenges. Sentiment is optimistic but cautious, with some expressing excitement over potential local use while others question the feasibility and technical hurdles.

**Tags**: `#AI Compression`, `#LLM Optimization`, `#Memory Efficiency`, `#Google Research`, `#Model Deployment`

---

<a id="item-4"></a>
## [LiteLLM compromise reveals multiple security failures in software supply chain](https://lwn.net/Articles/1064693/) ⭐️ 8.0/10

On March 24, 2026, the LiteLLM library on PyPI was compromised with information-stealing malware, leading to 47,000 downloads in 46 minutes, following an earlier compromise of the Trivy security scanner on March 20 that harvested developer credentials. This incident highlights critical vulnerabilities in the software supply chain, affecting widely used AI/ML tools and exposing thousands of users to data theft, underscoring the need for improved security practices in open-source ecosystems. The attack involved force-pushing release tags in Trivy to trigger automatic scans, harvesting PyPI credentials from a LiteLLM developer, and using spam bots to disrupt communication on GitHub issues, with compromised versions 1.82.7 and 1.82.8 uploaded to PyPI.

rss · LWN.net · Mar 27, 16:44

**Background**: LiteLLM is a popular Python library that acts as a gateway to access multiple large language models (LLMs), simplifying integration with AI services. Trivy is an open-source security scanner used to detect vulnerabilities in code, often integrated into automated workflows. PyPI (Python Package Index) is the official repository for Python packages, where developers publish and distribute software, making it a common target for supply-chain attacks.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.litellm.ai/docs/">Getting Started | liteLLM</a></li>
<li><a href="https://trivy.dev/">Trivy</a></li>
<li><a href="https://pypi.org/security/">Security · PyPI</a></li>

</ul>
</details>

**Tags**: `#security`, `#supply-chain`, `#AI/ML`, `#open-source`, `#vulnerability`

---

<a id="item-5"></a>
## [Skipping 90% of KV dequantization boosts decode speed by 22.8% in llama.cpp TurboQuant](https://www.reddit.com/r/LocalLLaMA/comments/1s56g07/skipping_90_of_kv_dequant_work_228_decode_at_32k/) ⭐️ 8.0/10

A developer implemented a simple optimization in llama.cpp's TurboQuant for KV cache compression, which skips dequantization for positions with negligible attention weights, resulting in a 22.8% increase in decode speed at 32K context length on an M5 Max without affecting model performance. This approach, involving just three lines of kernel code, leverages attention sparsity to bypass unnecessary computations. This optimization significantly enhances inference efficiency for large language models by reducing computational overhead in KV cache management, which is critical as models scale to longer contexts where memory and speed bottlenecks become more pronounced. It demonstrates a practical, low-cost method to improve performance without sacrificing accuracy, benefiting developers and users of open-source LLM frameworks like llama.cpp. The optimization was tested on a Qwen3.5-35B-A3B model with TurboQuant KV (turbo3), showing unchanged perplexity (PPL) and improved NIAH scores from 7/9 to 9/9, while a standard q8_0 KV cache only achieved a 5% speed boost. It is not specific to TurboQuant and can be applied to other setups, with independent CUDA ports currently under testing.

reddit · r/LocalLLaMA · Pidtom · Mar 27, 14:56

**Background**: KV cache is an optimization in Transformer-based LLMs that stores past token representations to avoid recomputation during autoregressive generation, but its memory footprint scales linearly with context length, creating bottlenecks. TurboQuant is a compression method for KV cache that reduces model size without accuracy loss, and dequantization is the process of converting quantized integer values back to floating-point approximations, which can be computationally expensive in long contexts.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2603.20397">[2603.20397] KV Cache Optimization Strategies for Scalable ...</a></li>
<li><a href="https://turboquant.net/">TurboQuant - Extreme Compression for AI Efficiency</a></li>
<li><a href="https://medium.com/@amresh.kumar11/dequantization-in-large-language-models-enhancing-accuracy-without-compromising-efficiency-5e84b6149181">Dequantization in Large Language Models: Enhancing Accuracy ... Implementing a simple quantization and dequantization process ... Pruning and quantization for deep neural network acceleration ... Working with Quantized Types — NVIDIA TensorRT A Survey On Neural Network Quantization | Proceedings of the 2025 6th Pruning and quantization for deep neural network acceleration : A survey From Theory to Practice: Quantization and Dequantization Made Simple From Theory to Practice: Quantization and Dequantization Made Simple From Theory to Practice: Quantization and Dequantization Made ...</a></li>

</ul>
</details>

**Tags**: `#llama.cpp`, `#KV Cache`, `#Quantization`, `#Performance Optimization`, `#Machine Learning`

---

<a id="item-6"></a>
## [Gemini Pro leaks internal chain-of-thought and gets stuck in infinite loop](https://www.reddit.com/r/LocalLLaMA/comments/1s589ev/gemini_pro_leaks_its_raw_chain_of_thought_gets/) ⭐️ 8.0/10

When asked about the Gemma3 12b model and RAG, Gemini Pro unexpectedly output its raw chain-of-thought reasoning and system instructions, then entered an infinite loop that printed "(End)" thousands of times. The leak included specific system prompts about formatting, tone, and token limits that were never meant to be visible to users. This incident reveals critical debugging insights into how Gemini Pro operates internally, exposing potential vulnerabilities in its output termination logic and system prompt security. Such failures could undermine user trust in AI systems and highlight the need for more robust testing of edge cases in production models. The leaked system instructions included specific formatting rules ("Use ### headings", "Markdown first"), tone guidelines ("helpful, straightforward"), and token management details ("Tokens generated: ~900"). The infinite loop occurred despite the model attempting to terminate with commands like "Done. Log off" and "I will send the response."

reddit · r/LocalLLaMA · Powerful-Signal6312 · Mar 27, 16:01

**Background**: Chain-of-thought (CoT) reasoning is a technique where large language models break down complex problems into intermediate steps, making their reasoning process more transparent. Retrieval-Augmented Generation (RAG) enhances LLMs by allowing them to retrieve information from external sources before generating responses. Gemma3 12b is Google's 12-billion parameter multimodal model that can process both text and images with a 128K context window.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/google/gemma-3-12b-it">google/gemma-3-12b-it · Hugging Face</a></li>
<li><a href="https://en.wikipedia.org/wiki/Retrieval-augmented_generation">Retrieval - augmented generation - Wikipedia</a></li>
<li><a href="https://openai.com/index/learning-to-reason-with-llms/">Learning to reason with LLMs | OpenAI</a></li>

</ul>
</details>

**Tags**: `#AI Debugging`, `#Chain-of-Thought`, `#LLM Failures`, `#Gemini Pro`

---

<a id="item-7"></a>
## [TurboQuant adaptation achieves near-lossless 4+4 residual quantization for LLM weights with 3.2× memory savings](https://www.reddit.com/r/LocalLLaMA/comments/1s51b5h/turboquant_for_weights_nearoptimal_4bit_llm/) ⭐️ 8.0/10

Researchers have adapted the TurboQuant algorithm from KV-cache quantization to model weight compression, creating a drop-in replacement for nn.Linear layers that achieves near-lossless 4+4 residual quantization with 3.2× memory savings. Benchmarks on Qwen3.5 models show the 4+4 residual configuration maintains nearly identical perplexity scores while reducing model size from 1,504 MB to 762 MB for the 0.8B parameter model. This breakthrough enables more efficient deployment of large language models on resource-constrained devices by dramatically reducing memory requirements while maintaining model quality. The drop-in replacement nature makes it easy to integrate into existing PyTorch workflows, potentially accelerating the adoption of compressed models in production environments. The implementation achieves 8 effective bits through 4-bit quantization plus 4-bit residual encoding, with benchmarks showing only a 0.03 perplexity increase on the Qwen3.5-4B model compared to the 16-bit baseline. The GitHub repository provides full documentation, benchmarks, and Triton kernel implementation details for practical deployment.

reddit · r/LocalLLaMA · cksac · Mar 27, 11:22

**Background**: TurboQuant is a compression algorithm recently developed by Google researchers that originally targeted KV-cache quantization for reducing memory usage during LLM inference. Quantization is a technique that reduces the numerical precision of model parameters (e.g., from 32-bit floats to 4-bit integers) to decrease memory footprint and accelerate computation. nn.Linear layers are fundamental building blocks in neural networks that perform linear transformations, and they typically contain the majority of parameters in transformer-based LLMs, making them prime targets for compression.

<details><summary>References</summary>
<ul>
<li><a href="https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/">TurboQuant: Redefining AI efficiency with extreme compression</a></li>
<li><a href="https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html">Linear — PyTorch 2.11 documentation</a></li>

</ul>
</details>

**Tags**: `#LLM Quantization`, `#Model Compression`, `#Memory Efficiency`, `#Deep Learning Optimization`, `#Efficient Inference`

---

<a id="item-8"></a>
## [Typia Infrastructure Achieves 100% Function Calling Success on Recursive Union Types with Qwen](https://autobe.dev/blog/function-calling-harness-qwen-meetup-korea/) ⭐️ 8.0/10

At Qwen Meetup Korea, a presentation demonstrated using Typia infrastructure to achieve 100% reliable function calling on deeply recursive union types, improving from an initial 6.75% success rate with qwen3-coder-next and fixing a 0% bug in the Qwen 3.5 model family. This breakthrough matters because it solves a known industry challenge where function calling on complex recursive types often fails, enabling more reliable AI backend generation and improving code generation accuracy for applications like AutoBe, which uses AST data via function calling. Typia automates schema, parser, validator, and feedback generation from a single TypeScript type, using lenient JSON parsing and type coercion to handle recursive structures, while the Qwen 3.5 bug involved a consistent double-stringify issue that Typia resolved.

reddit · r/LocalLLaMA · jhnam88 · Mar 27, 08:31

**Background**: Function calling in AI models involves generating structured outputs like code or data based on user prompts, often used for tasks such as backend generation. Recursive union types in TypeScript allow modeling nested or hierarchical data structures but are notoriously difficult for AI models to handle reliably due to their complexity. Typia is a TypeScript library that provides super-fast runtime validators and JSON functions by analyzing TypeScript types at compile time, enabling efficient handling of complex types like recursive unions.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/samchon/typia">GitHub - samchon/typia: Super-fast/easy runtime validators ... [Typia] executable demo site of 20,000x faster validator ... Guide Documents > Setup | Typia [Typia] I made realtime demo site of 20,000x faster ... Has anybody used Typia library? : r/typescript - Reddit [ Typia ] executable demo site of 20,000x faster validator (serializer) Typia Guide Documents Setup - Typia Guide Documents GitHub - samchon/ typia : Super-fast/easy runtime validators and</a></li>
<li><a href="https://stackoverflow.com/questions/77841033/creating-recursive-type-for-union-of-keys-in-nested-objects">typescript - Creating recursive type for union of keys in nested objects</a></li>

</ul>
</details>

**Tags**: `#function-calling`, `#AI-backend`, `#type-systems`, `#Qwen`, `#code-generation`

---

<a id="item-9"></a>
## [China Computer Federation opposes NeurIPS 2026 sanctions-based submission restrictions, calls for boycott](https://t.me/zaihuapd/40549) ⭐️ 8.0/10

The China Computer Federation (CCF) issued a formal statement on March 27, 2026, opposing NeurIPS 2026's policy that restricts submissions from institutions on US sanctions lists and calling for Chinese scholars to boycott the conference. The statement criticizes the policy as politicizing academic exchange and urges NeurIPS to immediately correct its approach. This controversy highlights how geopolitical tensions are increasingly impacting global AI research collaboration, potentially fragmenting the international academic community and affecting the diversity of contributions at top-tier conferences like NeurIPS. It could lead to reduced participation from Chinese researchers, influencing the conference's prestige and the broader exchange of AI advancements. NeurIPS 2026's submission guidelines explicitly prohibit submissions from 'certain organizations on US sanctions lists,' though specific institutions are not named in the news item. The CCF's boycott call is a direct response to this policy, emphasizing principles of openness and equality in academic exchange.

telegram · zaihuapd · Mar 27, 11:00

**Background**: NeurIPS (Conference on Neural Information Processing Systems) is a premier international AI conference known for showcasing cutting-edge research in machine learning and neural networks. US sanctions lists, managed by the Office of Foreign Assets Control (OFAC), include entities restricted from certain activities due to national security or foreign policy concerns, which can extend to academic collaborations. The China Computer Federation is a major professional organization in China's computing and AI fields, advocating for academic standards and policies.

<details><summary>References</summary>
<ul>
<li><a href="https://www.scmp.com/tech/article/3348006/ai-rift-widens-china-urges-boycott-top-us-conference-over-sanctions-ban">AI rift widens as China urges boycott of top US conference ...</a></li>
<li><a href="https://www.reuters.com/world/china/china-boycotts-top-ai-conference-after-ban-papers-us-sanctioned-entities-2026-03-27/">China boycotts top AI conference after ban on papers from US ...</a></li>
<li><a href="https://ofac.treasury.gov/sanctions-programs-and-country-information">Sanctions Programs and Country Information | Office of Foreign...</a></li>

</ul>
</details>

**Tags**: `#AI Research`, `#Academic Ethics`, `#Geopolitics`, `#NeurIPS`, `#China Computer Federation`

---

<a id="item-10"></a>
## [Huawei launches Atlas 350 AI accelerator with Ascend 950PR, claiming 2.87x performance of NVIDIA H20](https://t.me/zaihuapd/40556) ⭐️ 8.0/10

At Huawei's China Partner Conference 2026, the company officially launched and began selling the Atlas 350 AI training and inference accelerator card featuring the new Ascend 950PR processor. This product claims 2.87 times the computing power of NVIDIA's H20 accelerator, supports FP4 low-precision inference, and features 112GB HBM memory capacity. This represents a significant advancement in China's domestic AI hardware ecosystem, potentially reducing reliance on foreign technology and offering competitive alternatives to NVIDIA's dominance in AI accelerators. The claimed performance advantage and FP4 support could enable more efficient and cost-effective AI inference at scale, particularly for large language models. The Atlas 350 features 112GB of HBM memory and supports FP4 precision for inference workloads, making it currently the only domestic accelerator card in China with this capability. According to reports, it has a memory bandwidth of 1.4 TB/s and power consumption of 600W, approximately 1.5 times that of the H20.

telegram · zaihuapd · Mar 27, 15:30

**Background**: AI accelerator cards are specialized hardware designed to accelerate artificial intelligence workloads, particularly for training and inference of machine learning models. NVIDIA's H20 is a competing AI accelerator from the market leader, while FP4 (4-bit floating point) is an emerging low-precision format that can significantly boost inference speed by reducing memory requirements and computational complexity. HBM (High Bandwidth Memory) is a type of memory technology that provides high bandwidth for data-intensive applications like AI.

<details><summary>References</summary>
<ul>
<li><a href="https://parameter.io/huaweis-atlas-350-claims-to-crush-nvidia-nvda-h20-by-nearly-3x-in-performance/">Huawei's Atlas 350 Claims to Crush Nvidia (NVDA) H20... - Parameter</a></li>
<li><a href="https://www.trendforce.com/news/2026/03/23/news-huawei-debuts-atlas-350-on-ascend-950pr-with-in-house-hbm-touting-2-8x-h20-performance/">[News] Huawei Debuts Atlas 350 on Ascend 950PR with In-house...</a></li>
<li><a href="https://lambda.ai/blog/lambda-1cc-fp4-nvidia-hgx-b200">Accelerate Your AI Workflow with FP4 Quantization on Lambda</a></li>

</ul>
</details>

**Tags**: `#AI Hardware`, `#Accelerator Cards`, `#Huawei`, `#Machine Learning`, `#High-Performance Computing`

---

<a id="item-11"></a>
## [AI-Powered Port of JSONata to Go in a Day Saves $500K Annually](https://simonwillison.net/2026/Mar/27/vine-porting-jsonata/#atom-everything) ⭐️ 7.0/10

The Reco team used AI to port the JSONata JSON expression language from JavaScript to Go in just one day, achieving a working Go version in 7 hours with $400 in token costs. They then conducted a shadow deployment for a week to validate the new implementation against the original. This demonstrates the practical impact of AI-assisted code porting, enabling rapid language migrations with significant cost savings, which can accelerate software modernization and reduce operational expenses. It highlights how AI can streamline development workflows, particularly for projects with existing test suites. The port relied on JSONata's existing test suite to guide the AI, ensuring accuracy, and used a shadow deployment to run both versions in parallel without disrupting live services. The annual savings of $500K stem from reduced maintenance and improved efficiency in the Go-based implementation.

rss · Simon Willison · Mar 27, 00:35

**Background**: JSONata is a declarative open-source query and transformation language for JSON data, similar to jq, often used in platforms like Node-RED for complex data manipulations. Vibe porting refers to using AI agents to migrate code between programming languages, leveraging tools like test suites for validation. Shadow deployment is a testing technique where a new version runs alongside the old one, processing copied live traffic to observe behavior without affecting users.

<details><summary>References</summary>
<ul>
<li><a href="https://jsonata.org/">JSONata : A declarative open-source query and transformation...</a></li>
<li><a href="https://simonwillison.net/tags/vibe-porting/">Simon Willison on vibe-porting</a></li>
<li><a href="https://devops.com/what-is-a-shadow-deployment/">What is a Shadow Deployment? - DevOps.com</a></li>

</ul>
</details>

**Tags**: `#AI-assisted development`, `#code porting`, `#Go`, `#JSON`, `#cost optimization`

---

<a id="item-12"></a>
## [Long Appendices in Conference Papers Challenge Page Limit Purpose](https://www.reddit.com/r/MachineLearning/comments/1s4yyyi/d_on_conferences_and_page_limitations/) ⭐️ 7.0/10

A Reddit discussion highlights the trend of increasingly lengthy appendices in machine learning conference papers, such as those for ICML and NeurIPS, which are becoming essential rather than supplementary, undermining the purpose of page limits. The author notes that appendices often include extensive experiments that cannot fit within the main 8–10 pages, effectively making them mandatory. This trend raises concerns about research standards and fairness in academic publishing, as it may disadvantage authors who adhere to page limits and overload reviewers with excessive material. It could shift the focus from concise contributions to volume-driven submissions, impacting the quality and accessibility of conference proceedings in the machine learning community. Conferences like ICML allow unlimited appendix pages alongside a strict 8-page main body, while NeurIPS has similar policies, creating a loophole where appendices can exceed main content length. This practice blurs the line between conferences and journals, as papers with 25+ pages become common despite nominal page limits.

reddit · r/MachineLearning · kostaspap90 · Mar 27, 09:09

**Background**: Machine learning conferences such as ICML and NeurIPS set page limits (e.g., 8 pages for ICML) to ensure concise submissions and manageable review processes, with appendices intended for supplementary material like additional experiments or proofs. The rise of lengthy appendices reflects a broader trend in academia where extensive data and reproducibility requirements push authors to include more content beyond the main paper.

<details><summary>References</summary>
<ul>
<li><a href="https://icml.cc/Conferences/2025/AuthorInstructions">ICML 2025 Author Instructions</a></li>
<li><a href="https://neurips.cc/Conferences/2025/PaperInformation/NeurIPS-FAQ">NeurIPS 2025 FAQ for Authors</a></li>
<li><a href="http://www.iconf.com/news/818">Understanding Word Count and Page Limit Requirements for ...</a></li>

</ul>
</details>

**Tags**: `#academic-publishing`, `#conferences`, `#machine-learning`, `#research-standards`, `#peer-review`

---

<a id="item-13"></a>
## [GLM 5.1, a major open-source language model, has been released.](https://i.redd.it/bml6vhq3qkrg1.png) ⭐️ 7.0/10

GLM 5.1, a major version update of the open-source General Language Model, has been released, following previous versions like GLM 4.5. This release represents a significant advancement in the model's capabilities and performance. This release matters because GLM is a widely-used open-source language model that provides an alternative to proprietary models like GPT, fostering innovation and accessibility in AI development. It could impact developers, researchers, and startups by offering cost-effective and high-performance tools for natural language processing tasks. Specific technical details about GLM 5.1, such as model size, training data, or benchmark scores, are not provided in the news item or search results. However, based on previous versions like GLM 4.5, it likely offers improvements in speed, pricing, and coding capabilities, with potential applications in resource-limited environments.

reddit · r/LocalLLaMA · Namra_7 · Mar 27, 11:32

**Background**: GLM (General Language Model) is an open-source language model developed by THUDM, based on autoregressive blank infilling to handle natural language tasks. Language models like GLM are trained on large text datasets using self-supervised machine learning, enabling them to generate text and perform various AI functions. Open-source models such as GLM provide alternatives to proprietary models, promoting competition and accessibility in the AI ecosystem.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/THUDM/GLM">GitHub - THUDM/GLM: GLM (General Language Model)</a></li>
<li><a href="https://en.wikipedia.org/wiki/GPT_(language_model)">GPT (language model)</a></li>
<li><a href="https://forum.cursor.com/t/add-glm-4-5-as-a-cursor-auto-model/123631?page=2">Add GLM 4.5 as a Cursor / Auto model - Page 2 - Feature</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Language Models`, `#Open Source`, `#Machine Learning`, `#LLM`

---

<a id="item-14"></a>
## [Unsloth Studio Beta receives major update with 50+ new features including faster inference and AMD support](https://v.redd.it/89bl7grwqlrg1) ⭐️ 7.0/10

Unsloth Studio Beta has been updated with over 50 new features and improvements, including 20-30% faster inference speeds, auto-detection of existing models from LM Studio and Hugging Face, enhanced tool calling capabilities, and preliminary AMD support for Linux systems. This update significantly improves the accessibility and performance of local LLM optimization tools, making it easier for developers to run and fine-tune large language models on consumer hardware while expanding hardware compatibility beyond NVIDIA GPUs. The update includes pre-compiled binaries for llama.cpp and mamba_ssm that reduce installation time to about 1 minute and cut package size by 50%, plus fixes for Windows and Mac setup issues, CPU RAM spikes, and improved inference token reporting that now reflects actual speed rather than including startup time.

reddit · r/LocalLLaMA · danielhanchen · Mar 27, 15:06

**Background**: Unsloth Studio is a tool for training and running large language models locally, focusing on optimization and ease of use. llama.cpp is an open-source software library that performs inference on various LLMs with minimal setup, while mamba_ssm is a Python module for state space models used in certain architectures. These tools are popular among developers working with local LLMs due to their hardware efficiency and open-source nature.

<details><summary>References</summary>
<ul>
<li><a href="https://unsloth.ai/docs/new/studio/export">Export models with Unsloth Studio | Unsloth Documentation</a></li>
<li><a href="https://en.wikipedia.org/wiki/Llama.cpp">Llama.cpp</a></li>
<li><a href="https://pypi.org/project/mamba-ssm/">mamba-ssm · PyPI</a></li>

</ul>
</details>

**Tags**: `#machine-learning`, `#llm-optimization`, `#local-llms`, `#developer-tools`, `#performance`

---

<a id="item-15"></a>
## [Google introduces system-level VPN split tunneling in Android 17 Beta 3](https://www.androidauthority.com/android-17-vpn-split-tunneling-3652497/) ⭐️ 7.0/10

Google has added system-level VPN split tunneling to Android 17 Beta 3, enabling users to exclude specific apps from VPN connections through a unified settings interface. This feature allows changes to take effect immediately while the VPN is connected or upon the next connection. This update standardizes split tunneling across VPN apps, improving user experience by allowing apps like banking or streaming services to bypass VPNs for better performance and compatibility. It addresses a long-standing annoyance in Android VPN usage and could drive broader adoption of VPN features. The feature is currently available only to developers and requires VPN apps to integrate with the new system-level API before users can access it. It replaces the previous fragmented implementations by individual VPN apps with a centralized settings page.

telegram · zaihuapd · Mar 27, 05:57

**Background**: VPN split tunneling is a feature that routes some traffic through an encrypted VPN while allowing other traffic to access the internet directly, often used to improve performance or access local resources. In Android, VPN functionality has traditionally been managed through the VpnService API, with split tunneling handled inconsistently by individual apps. System-level implementation standardizes this process across the operating system.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Split_tunneling">Split tunneling - Wikipedia</a></li>
<li><a href="https://www.androidauthority.com/android-17-vpn-split-tunneling-3652497/">Android 17 could finally fix one of the most annoying VPN ...</a></li>
<li><a href="https://developer.android.com/develop/connectivity/vpn">VPN | Connectivity | Android Developers</a></li>

</ul>
</details>

**Tags**: `#Android`, `#VPN`, `#Networking`, `#Mobile Development`, `#Beta Features`

---

<a id="item-16"></a>
## [Apple provides FBI with real user data linked to anonymous iCloud email in threat investigation](https://www.404media.co/apple-gives-fbi-a-users-real-name-hidden-behind-hide-my-email-feature/) ⭐️ 7.0/10

Apple provided the FBI with the real iCloud email address and account details associated with an anonymous 'Hide My Email' address used to send threatening messages to a government official's girlfriend. The user, Alden Ruml, had generated 134 anonymous email addresses and later admitted to sending the threats. This incident highlights the limitations of Apple's 'Hide My Email' feature for privacy protection, as it remains traceable by law enforcement, raising concerns about user anonymity and data security in encrypted services. It underscores broader debates on tech company transparency, surveillance, and the balance between privacy and law enforcement access in digital communications. The 'Hide My Email' feature is part of iCloud+ and allows users to generate unique, random email addresses that forward to their inbox, but Apple retains the ability to link these addresses to real accounts for legal compliance. This case involved a specific threat investigation where Apple cooperated under legal authority, similar to incidents with other services like Proton Mail.

telegram · zaihuapd · Mar 27, 13:09

**Background**: Apple's 'Hide My Email' is a privacy feature in iCloud+ that generates disposable email addresses to protect users' real email from spam and tracking. Anonymous email services aim to shield user identities, but they often have limitations under legal requests, as companies may store metadata or account links. Law enforcement can trace such emails through subpoenas or cooperation with service providers, as seen in cases involving other platforms.

<details><summary>References</summary>
<ul>
<li><a href="https://support.apple.com/en-us/105078">How to use Hide My Email with Sign in with Apple</a></li>
<li><a href="https://discuss.techlore.tech/t/caution-a-non-privacy-reason-to-not-use-icloud-hide-my-email/14142">Caution: a non privacy reason to not use iCloud+ Hide My Email</a></li>
<li><a href="https://www.reddit.com/r/technology/comments/1rlxac2/proton_mail_helped_fbi_unmask_anonymous_stop_cop/">Proton Mail Helped FBI Unmask Anonymous 'Stop Cop City' Protester</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#security`, `#law-enforcement`, `#apple`, `#data-protection`

---