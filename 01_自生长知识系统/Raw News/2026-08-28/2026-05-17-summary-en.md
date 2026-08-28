---
layout: default
title: "Horizon Summary: 2026-05-17 (EN)"
date: 2026-05-17
lang: en
---

> From 32 items, 12 important content pieces were selected

---

1. [sglang v0.5.12 Adds Full DeepSeek V4 Inference Support](#item-1) ⭐️ 9.0/10
2. [MTP PR Merged into llama.cpp for Speculative Decoding](#item-2) ⭐️ 9.0/10
3. [NVIDIA's SANA-WM: 2.6B Parameter World Model for 1-Minute 720p Video](#item-3) ⭐️ 8.0/10
4. [Moving Away from Tailwind to Semantic CSS](#item-4) ⭐️ 8.0/10
5. [Accelerando: Prophetic Sci-Fi on Singularity](#item-5) ⭐️ 8.0/10
6. [Frontier AI disrupts open CTF competitions](#item-6) ⭐️ 8.0/10
7. [DeepSeek-V4-Flash Revives LLM Steering for Refusal Removal](#item-7) ⭐️ 8.0/10
8. [ArXiv's 1-year ban on LLM-hallucinated references sparks debate](#item-8) ⭐️ 8.0/10
9. [Qwen3.6-35B-A3B Surpasses Larger Models on Terminal-Bench 2.0](#item-9) ⭐️ 8.0/10
10. [SpaceX, OpenAI, Anthropic Plan Landmark IPOs by 2026](#item-10) ⭐️ 8.0/10
11. [Google Bans Manipulation of AI Search Results as Spam](#item-11) ⭐️ 8.0/10
12. [GitHub Copilot Desktop App Enters Technical Preview](#item-12) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [sglang v0.5.12 Adds Full DeepSeek V4 Inference Support](https://github.com/sgl-project/sglang/releases/tag/v0.5.12) ⭐️ 9.0/10

SGLang released v0.5.12, which provides comprehensive inference support for DeepSeek V4, including tensor/expert parallelism, DeepGemm kernels, and disaggregated prefill-decode. This release marks a significant engineering milestone for LLM serving, enabling efficient deployment of the large-scale DeepSeek V4 model with cutting-edge optimizations. DeepSeek V4 support includes MegaMoE kernels, HiSparse for offloading inactive KV cache to CPU, and HiCache with UnifiedRadixTree, alongside support for new hardware like Nvidia B300 and AMD MI35X.

github · Fridge003 · May 16, 18:23

**Background**: SGLang is an open-source inference engine for large language models, designed for high performance and flexibility. DeepSeek V4 is a large-scale MoE model requiring advanced parallelism and kernel optimizations for efficient serving. This release integrates these optimizations into SGLang.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/deepseek-ai/DeepGEMM">GitHub - deepseek-ai/ DeepGEMM : DeepGEMM : clean and efficient...</a></li>
<li><a href="https://www.lmsys.org/blog/2026-04-10-sglang-hisparse/">HiSparse : Turbocharging Sparse Attention with... | LMSYS Org</a></li>
<li><a href="https://www.kad8.com/ai/megamoe-megakernel-architecture-optimizing-deepseek-v4-llm-performance/">MegaMoE MegaKernel Architecture: Optimizing DeepSeek-V4 LLM Performance</a></li>

</ul>
</details>

**Tags**: `#LLM inference`, `#DeepSeek V4`, `#GPU kernels`, `#parallelism`, `#performance`

---

<a id="item-2"></a>
## [MTP PR Merged into llama.cpp for Speculative Decoding](https://i.redd.it/1mwo5r3wqh1h1.jpeg) ⭐️ 9.0/10

A pull request adding Multi-Token Prediction (MTP) support to llama.cpp has been merged, enabling speculative decoding that promises a 1.5x to 1.8x speedup in token generation. This merge brings one of the most significant speed improvements to token generation in llama.cpp, greatly enhancing the user experience for local LLM inference. The high community enthusiasm reflects the practical impact on everyday AI workflows. The speedup applies only to token generation, not prompt processing; early implementations slowed prompt processing, but subsequent fixes likely addressed that. Users need MTP-enabled GGUF models to benefit, and performance may vary across backends (e.g., only 30% increase on AMD APU with Vulkan).

reddit · r/LocalLLaMA · Valuable_Touch5670 · May 16, 12:13 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1terzq4/mtp_pr_merged/)

**Background**: Multi-Token Prediction (MTP) is a training technique where models learn to predict multiple future tokens simultaneously, using a shared trunk and multiple output heads. Speculative decoding accelerates inference by using a fast draft model to generate multiple token candidates, which are then verified by the target model, preserving output quality. The MTP layers in a model can serve as the draft mechanism, enabling significant speedups without additional model overhead.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2404.19737">[2404.19737] Better & Faster Large Language Models via Multi-token Prediction</a></li>
<li><a href="https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/">An Introduction to Speculative Decoding for Reducing Latency in AI Inference | NVIDIA Technical Blog</a></li>

</ul>
</details>

**Discussion**: The community responded with extraordinary enthusiasm, praising the llama.cpp team and likening the impact to that of AI CEOs. Users shared specific speedup numbers (1.5x-1.8x) and backend comparisons, while asking about vision capabilities, the need for special GGUF models, and whether slow prompt processing had been fixed. Some expressed curiosity about combining MTP with ngram-based speculative decoding on different hardware.

**Tags**: `#llama.cpp`, `#MTP`, `#speculative decoding`, `#LLM inference`, `#token generation`

---

<a id="item-3"></a>
## [NVIDIA's SANA-WM: 2.6B Parameter World Model for 1-Minute 720p Video](https://nvlabs.github.io/Sana/WM/) ⭐️ 8.0/10

NVIDIA has released SANA-WM, a 2.6 billion parameter world model that can generate one-minute-long 720p videos with 6-degree-of-freedom camera control. The model is available on Hugging Face but its weights are marked as 'coming soon', leading to debate about its open-source status. SANA-WM pushes the boundary of video generation by achieving world model capabilities at minute-scale with high resolution, which could significantly impact game development, simulation, and autonomous systems. However, the delayed release of model weights tempers enthusiasm, as true open-source validation remains pending. The model uses a hybrid linear diffusion transformer architecture and is trained on synthetic data, likely from Unreal Engine. Despite claims of open-source release under NVIDIA's Open Model License, only code and a subset of assets are currently available, with weights promised 'soon'.

hackernews · mjgil · May 16, 12:06 · [Discussion](https://news.ycombinator.com/item?id=48159445)

**Background**: A world model in AI is a neural network that learns an internal representation of an environment, enabling it to predict future states and simulate dynamics like physics and object interactions. Unlike traditional video generation models, world models are designed to support planning and reasoning, making them valuable for robotics, autonomous driving, and interactive media. SANA-WM builds on prior works like SANA-Video but extends to longer durations with camera control.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/World_model_(artificial_intelligence)">World model (artificial intelligence)</a></li>
<li><a href="https://arxiv.org/html/2605.15178v1">SANA-WM: Efficient Minute-Scale World Modeling with Hybrid</a></li>

</ul>
</details>

**Discussion**: Community comments express skepticism about the open-source claim, with one commenter stating 'weights coming soon == currently vaporware'. Another notes that while code license is Apache 2.0, the model license allows commercial use, but until weights are released, reproducibility is impossible. Some commenters are impressed by the technical achievement while others worry about synthetic data bias and lack of intentionality in game contexts.

**Tags**: `#world model`, `#video generation`, `#NVIDIA`, `#AI research`, `#open-source`

---

<a id="item-4"></a>
## [Moving Away from Tailwind to Semantic CSS](https://jvns.ca/blog/2026/05/15/moving-away-from-tailwind--and-learning-to-structure-my-css-/) ⭐️ 8.0/10

Julia Evans describes her decision to move away from Tailwind CSS and adopt a more semantic, structured approach to CSS, sharing the principles she learned along the way. This post fuels the ongoing debate between utility-first and semantic CSS, offering practical insights for developers reconsidering their CSS methodology for better maintainability and accessibility. Evans emphasizes starting with semantic HTML markup before styling, and notes that utility-first frameworks like Tailwind invert this order, potentially harming accessibility.

hackernews · mpweiher · May 16, 09:14 · [Discussion](https://news.ycombinator.com/item?id=48158400)

**Background**: Utility-first CSS, exemplified by Tailwind, relies on many small, single-purpose classes for rapid styling. In contrast, semantic CSS methodologies like BEM use descriptive class names tied to content meaning. The choice between them often involves tradeoffs in development speed, readability, and long-term maintainability.

<details><summary>References</summary>
<ul>
<li><a href="https://heydonworks.com/article/what-is-utility-first-css/">What is Utility-First CSS?: HeydonWorks</a></li>
<li><a href="https://andreipfeiffer.dev/blog/2022/scalable-css-evolution/part4-methologies-and-semantics">The evolution of scalable CSS, Part 4: Methodologies and ...</a></li>
<li><a href="https://github.com/HonzaMikula/Semantic-CSS">GitHub - HonzaMikula/Semantic-CSS: Semantic CSS methodology</a></li>

</ul>
</details>

**Discussion**: Commenters are divided: some praise Tailwind for eliminating ad-hoc class naming, while others argue it inverts proper HTML structure. Many value Evans's honest, exploratory writing style, and some suggest alternatives like CSS Modules.

**Tags**: `#CSS`, `#Tailwind CSS`, `#frontend`, `#web development`, `#semantic HTML`

---

<a id="item-5"></a>
## [Accelerando: Prophetic Sci-Fi on Singularity](https://www.antipope.org/charlie/blog-static/fiction/accelerando/accelerando.html) ⭐️ 8.0/10

The 2005 sci-fi novel Accelerando by Charles Stross remains highly influential, noted for its prophetic insights into AI agents and technological singularity. Accelerando offers a prescient vision of AI agents, posthumanism, and the singularity, influencing both science fiction and real-world tech discussions. The novel follows the Macx family through generations as humanity undergoes a technological singularity, featuring AI agents called 'OpenCLaw,' brain-computer interfaces, and digital uploads.

hackernews · eamag · May 16, 11:36 · [Discussion](https://news.ycombinator.com/item?id=48159241)

**Background**: The technological singularity is a hypothetical event where AI surpasses human intelligence, leading to explosive technological growth. Posthumanism explores the blurring boundaries between human and machine. Accelerando dramatizes these ideas through a narrative of rapid technological evolution and its impact on society.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Technological_singularity">Technological singularity</a></li>
<li><a href="https://en.wikipedia.org/wiki/Posthumanism">Posthumanism - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Commenters praise the novel's prescience, with some finding its depiction of AI agents eerily accurate, while others view the story as a tragedy about losing humanity to technology. The discussion also compares Accelerando to other sci-fi works like The Quantum Thief.

**Tags**: `#science fiction`, `#artificial intelligence`, `#futurism`, `#singularity`, `#technology prediction`

---

<a id="item-6"></a>
## [Frontier AI disrupts open CTF competitions](https://kabir.au/blog/the-ctf-scene-is-dead) ⭐️ 8.0/10

Frontier AI models can now automatically solve many challenges in open Capture The Flag (CTF) competitions, undermining the traditional manual problem-solving process and raising questions about fairness and educational value. This shift threatens the integrity and learning experience of CTF contests, which are critical for cybersecurity training and talent recruitment; it may also set a precedent for AI's impact on skill-based competitions and education. The article highlights that AI can solve challenges in minutes that previously took hours, and introduces a mentality of 'here is the flag' without understanding; however, some argue that automating early challenges is part of CTF culture and not necessarily cheating.

hackernews · frays · May 16, 07:01 · [Discussion](https://news.ycombinator.com/item?id=48157559)

**Background**: Capture The Flag (CTF) is a cybersecurity competition where participants solve security-related challenges to find hidden flags. Frontier AI refers to the most advanced AI models, such as GPT-4 and Claude, which can perform complex reasoning and code generation. These models are now capable of handling tasks that previously required human expertise, including some CTF challenges.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Frontier_AI">Frontier AI</a></li>
<li><a href="https://grokipedia.com/page/Frontier_model">Frontier model</a></li>

</ul>
</details>

**Discussion**: Comments are mixed: some lament that AI ruins both playing and building CTF challenges, reducing the rewarding collaborative learning process; others like tptacek note that automating challenges is part of CTF culture, and the games will adapt. There is also discussion about the broader collapse of education in the face of AI.

**Tags**: `#AI`, `#CTF`, `#security`, `#competition`, `#education`

---

<a id="item-7"></a>
## [DeepSeek-V4-Flash Revives LLM Steering for Refusal Removal](https://www.seangoedecke.com/steering-vectors/) ⭐️ 8.0/10

DeepSeek-V4-Flash has made LLM steering practical again, enabling effective removal of refusal behaviors and uncensoring via steering vectors, as demonstrated by antirez's DwarfStar project. This breakthrough reopens the door to fine-grained control over LLM behavior without retraining, impacting AI safety research, uncensored model deployment, and developer tooling. It empowers users to customize model outputs while raising important safety considerations. Steering vectors are directions in the model's latent space that can be added or subtracted to influence outputs; refusal removal in particular has been found to be mediated by a single direction. antirez's DwarfStar is a standalone project that integrates steering for DeepSeek-V4-Flash, not merely a stripped-down llama.cpp version.

hackernews · Brajeshwar · May 16, 14:58 · [Discussion](https://news.ycombinator.com/item?id=48160807)

**Background**: LLM steering, or activation vector steering, allows modifying a model's behavior by adjusting its internal representations. Earlier models had limited steering capabilities, but DeepSeek-V4-Flash provides well-documented steering features. The concept of 'abliteration'—identifying and removing a refusal direction—has been explored in previous research, showing that refusals often lie on a single vector. Steering vectors are computed directions in latent space that guide model outputs, offering a lightweight alternative to fine-tuning.

<details><summary>References</summary>
<ul>
<li><a href="https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction">Refusal in LLMs is mediated by a single direction — LessWrong</a></li>
<li><a href="https://bobrupakroy.medium.com/steering-large-language-models-with-activation-vectors-a-practical-guide-45866b3697ac">Steering Large Language Models with Activation Vectors ... | Medium</a></li>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash">deepseek-ai/DeepSeek-V4-Flash · Hugging Face</a></li>

</ul>
</details>

**Discussion**: The community discussion featured antirez clarifying that DwarfStar enables full refusal removal, not just a toy dataset, and NitpickLawyer highlighting the potential for uncensoring via steering vectors. Another commenter noted that DwarfStar is a standalone project, not a stripped-down llama.cpp. Overall sentiment is positive, with excitement about practical steering applications and concerns about misuse.

**Tags**: `#LLM`, `#steering vectors`, `#AI safety`, `#uncensoring`, `#deepseek`

---

<a id="item-8"></a>
## [ArXiv's 1-year ban on LLM-hallucinated references sparks debate](https://www.reddit.com/r/MachineLearning/comments/1tens5n/backlash_against_arxivs_proposed_1_year_ban_is/) ⭐️ 8.0/10

ArXiv proposed a 1-year ban on authors and coauthors who submit papers containing hallucinated references or other obvious LLM artifacts, and the community response has been largely supportive despite some backlash. This policy directly addresses the growing problem of AI-generated errors in scientific literature, which a Nature analysis found tens of thousands of papers in 2025 may contain invalid references, threatening academic integrity and trust in research. The ban applies to all coauthors, not just the original submitter, and the backlash includes arguments that PIs cannot read every reference and that LLMs will soon stop hallucinating references anyway.

reddit · r/MachineLearning · NeighborhoodFatCat · May 16, 08:30

**Background**: ArXiv is a widely used preprint server in machine learning and other sciences. Large language models (LLMs) sometimes generate plausible-sounding but fake references, a phenomenon known as hallucination. To maintain credibility, ArXiv proposed punitive measures against authors who fail to verify references.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2605.07723">[2605.07723] LLM hallucinations in the wild: Large-scale ...</a></li>
<li><a href="https://www.nature.com/articles/d41586-026-00969-z">Hallucinated citations are polluting the scientific ... - Nature</a></li>

</ul>
</details>

**Discussion**: Most commenters strongly support the ban, expressing disbelief that anyone would oppose it. Some note that this reveals how little some academics read their own papers, while others raise potential abuse, such as adding adversaries' names to force a ban.

**Tags**: `#arxiv`, `#llm`, `#academic-integrity`, `#peer-review`, `#machine-learning`

---

<a id="item-9"></a>
## [Qwen3.6-35B-A3B Surpasses Larger Models on Terminal-Bench 2.0](https://www.reddit.com/r/LocalLLaMA/comments/1temio0/qwen3635ba3b_and_9b_are_officially_on_the_public/) ⭐️ 8.0/10

Qwen3.6-35B-A3B achieved a score of 24.6% on the Terminal-Bench 2.0 leaderboard, surpassing Gemini 2.5 Pro (19.6%) and Qwen3-Coder-480B (23.9%). The smaller Qwen3.6-9B also scored 9.2%, showing sub-10B models are now competitive on hard agentic benchmarks. This demonstrates that open-source, locally-runable small models can outperform much larger proprietary models, making advanced AI capabilities more accessible. It signals a shift toward efficient, privacy-preserving local AI that reduces compute requirements. The results were achieved using the little-coder scaffold, which is specifically designed for small local models. The scaffold-model gap observed in earlier benchmarks persisted on Terminal-Bench 2.0, highlighting the importance of the scaffolding framework.

reddit · r/LocalLLaMA · Creative-Regular6799 · May 16, 07:19

**Background**: Terminal-Bench 2.0 is an open-source benchmark that tests an AI model's ability to navigate and complete tasks in a sandboxed terminal environment. Little-coder is a coding agent optimized for small local models, built on top of pi. The scaffold-model gap refers to the performance difference attributable to the scaffolding system rather than the model itself.

<details><summary>References</summary>
<ul>
<li><a href="https://www.vals.ai/benchmarks/terminal-bench-2">Terminal-Bench 2.0</a></li>
<li><a href="https://github.com/itayinbarr/little-coder">GitHub - itayinbarr/ little - coder : A coding agent optimized to smaller...</a></li>

</ul>
</details>

**Discussion**: The community is excited by the results, with users reporting strong real-world performance of Qwen3.6-35B-A3B and 9B models. Some users express surprise at the scaffold-model gap persisting on this benchmark, while others note ongoing improvements needed in prompt understanding and tool use. Overall sentiment is positive and supportive of the open-source push.

**Tags**: `#Qwen`, `#Terminal-Bench`, `#local LLMs`, `#open source`, `#benchmarking`

---

<a id="item-10"></a>
## [SpaceX, OpenAI, Anthropic Plan Landmark IPOs by 2026](https://t.me/zaihuapd/41409) ⭐️ 8.0/10

SpaceX, OpenAI, and Anthropic, three of the most valuable private tech companies in the US, are preparing for initial public offerings (IPOs) as early as 2026, aiming to raise hundreds of billions of dollars collectively. These IPOs could reshape the tech landscape, providing public market access to cutting-edge AI and space companies, and potentially surpassing the total IPO proceeds in the US for 2025. SpaceX is expected to go public within the next 12 months barring major market fluctuations, while Anthropic has already hired legal counsel to start preparations. OpenAI's timeline remains unspecified but is part of the 2026 target.

telegram · zaihuapd · May 16, 03:10

**Background**: An IPO is the process by which a private company offers shares to the public for the first time, allowing it to raise capital from a wide range of investors. SpaceX is a leader in space exploration and satellite internet, OpenAI is a pioneer in generative AI (e.g., ChatGPT), and Anthropic is a competitor focused on AI safety. Currently, all three are privately held, with valuations in the tens or hundreds of billions of dollars.

**Tags**: `#IPO`, `#SpaceX`, `#OpenAI`, `#Anthropic`, `#tech industry`

---

<a id="item-11"></a>
## [Google Bans Manipulation of AI Search Results as Spam](https://www.theverge.com/tech/931416/google-ai-search-spam-policy) ⭐️ 8.0/10

Google updated its spam policy to explicitly classify manipulation of generative AI search responses as a violation, covering AI Overview and AI Mode results. This directly targets Generative Engine Optimization (GEO) practices that aim to artificially boost brand visibility in AI answers. This policy change signals Google's commitment to maintaining trust in AI-powered search features, forcing SEO professionals and content creators to adapt their strategies. It could reduce spammy content in AI summaries and protect users from biased or manipulated information. Specific violations include mass-generating biased 'best recommendation' content or embedding prompt-like language in web pages to trick AI models into treating a site as authoritative. Offending sites may be demoted or completely removed from search results.

telegram · zaihuapd · May 16, 06:31

**Background**: AI Overviews are Google's generative AI summaries that appear at the top of search results, providing quick answers with links. AI Mode is a more advanced experimental feature offering deeper reasoning and multimodal capabilities. Generative Engine Optimization (GEO) is a new technical framework that optimizes content specifically for AI search engines, often involving tactics like injecting content into AI training data or manipulating model outputs.

<details><summary>References</summary>
<ul>
<li><a href="https://geoz.com.cn/article/geo是什么2026年生成式ai品牌优化新范式深度解析">GEO 是什么？ 2026年 生 成 式 AI品牌 优 化 新范 式 深度解析</a></li>
<li><a href="https://search.google/ways-to-search/ai-overviews/">Google AI Overviews - Search anything, effortlessly</a></li>
<li><a href="https://blog.google/products-and-platforms/products/search/ai-mode-search/">Expanding AI Overviews and introducing AI Mode</a></li>

</ul>
</details>

**Tags**: `#Google`, `#AI Search`, `#Spam Policy`, `#SEO`, `#GEO`

---

<a id="item-12"></a>
## [GitHub Copilot Desktop App Enters Technical Preview](https://github.blog/changelog/2026-05-14-github-copilot-app-is-now-available-in-technical-preview/) ⭐️ 8.0/10

GitHub Copilot desktop app is now available in technical preview, allowing developers to launch isolated development sessions directly from issues, pull requests, prompts, or history, and to view diffs, run tests, create PRs, and use Agent Merge for automated review handling. This release significantly enhances developer workflow by providing a self-contained environment for task-focused development and automated merge conflict resolution, potentially reducing context switching and manual overhead. The technical preview is available immediately for Copilot Pro and Pro+ subscribers, while Business and Enterprise users gain access within the week, pending organizational admin policy enabling CLI and preview permissions.

telegram · zaihuapd · May 16, 15:07

**Background**: GitHub Copilot is an AI-powered code completion tool that suggests code snippets and entire functions. A technical preview is an early release for testing feedback before general availability. Isolated development sessions allow developers to work on a specific task in a sandboxed environment without affecting their main codebase, improving focus and safety.

<details><summary>References</summary>
<ul>
<li><a href="https://github.blog/changelog/2026-04-13-fix-merge-conflicts-in-three-clicks-with-copilot-cloud-agent/">Fix merge conflicts in three clicks with Copilot cloud agent</a></li>

</ul>
</details>

**Tags**: `#GitHub`, `#Copilot`, `#AI`, `#developer tools`, `#technical preview`

---