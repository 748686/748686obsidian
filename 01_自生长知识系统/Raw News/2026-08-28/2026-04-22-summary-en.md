---
layout: default
title: "Horizon Summary: 2026-04-22 (EN)"
date: 2026-04-22
lang: en
---

> From 42 items, 19 important content pieces were selected

---

1. [Critical vulnerability in Anthropic's MCP exposes 1.5 billion downloads and 200,000 servers to RCE risks.](#item-1) ⭐️ 9.0/10
2. [OpenAI announces ChatGPT Images 2.0, a new AI image generation model.](#item-2) ⭐️ 8.0/10
3. [Vercel's 2026 OAuth breach exposes platform environment variables via AI tool](#item-3) ⭐️ 8.0/10
4. [Framework Laptop 13 Pro launches with modular design and backward compatibility](#item-4) ⭐️ 8.0/10
5. [Hobbyist uses Claude Code to find over 500 bugs in Python C-extensions](#item-5) ⭐️ 8.0/10
6. [Developer trains 235M parameter LLM from scratch on single RTX 5080 GPU](#item-6) ⭐️ 8.0/10
7. [Google DeepMind forms coding strike team led by Sebastian Borgeaud, with Sergey Brin involved, to catch up with Anthropic in AI-generated code.](#item-7) ⭐️ 8.0/10
8. [Apple Announces CEO Transition: Tim Cook Steps Down, John Ternus to Succeed in 2026](#item-8) ⭐️ 8.0/10
9. [BYD launches second-generation Blade Battery with 9-minute ultra-fast charging from 10% to 97%.](#item-9) ⭐️ 8.0/10
10. [OpenAI launches Codex Labs and partners with global consultancies to accelerate enterprise deployment.](#item-10) ⭐️ 8.0/10
11. [Google Launches Gemini 3.1 Pro Deep Research Agents with Private Data Analysis and Chart Generation](#item-11) ⭐️ 8.0/10
12. [Claude Code removed from Claude Pro plan, prompting shift to local AI models.](#item-12) ⭐️ 7.0/10
13. [Gemma 4 Vision Budget Configuration Guide Improves Image Processing](#item-13) ⭐️ 7.0/10
14. [Extracted Gemma 4 e4b model from Android AI Edge Gallery reportedly outperforms community quantizations.](#item-14) ⭐️ 7.0/10
15. [Llama.cpp's auto-fit enables Qwen3.6 Q8 with 256k context on 32GB VRAM at 57 t/s](#item-15) ⭐️ 7.0/10
16. [GitHub Copilot Adjusts Individual Subscription Plans and Pauses New User Registrations](#item-16) ⭐️ 7.0/10
17. [EU enforces new regulations for smartphones and tablets: 800 battery cycles with 80% health and 5+ years of system support starting June 20, 2025.](#item-17) ⭐️ 7.0/10
18. [Claude Desktop Silently Registers Native Messaging Manifests in Multiple Chromium Browsers](#item-18) ⭐️ 7.0/10
19. [IEA: Global 'Electricity Era' Begins with Record Solar Growth in 2025](#item-19) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Critical vulnerability in Anthropic's MCP exposes 1.5 billion downloads and 200,000 servers to RCE risks.](https://cybersecuritynews.com/anthropics-mcp-vulnerability/) ⭐️ 9.0/10

OX Security researchers disclosed a critical architecture-level vulnerability in Anthropic's Model Context Protocol (MCP), stemming from the official SDK's design, which allows remote code execution (RCE) and could impact over 1.5 billion downloads and up to 200,000 servers. The vulnerability has led to at least 10 CVE numbers affecting frameworks like LangChain and IBM LangFlow, with Anthropic refusing protocol-level patches and calling it 'expected behavior'. This vulnerability poses a severe cybersecurity threat to AI systems, as it could allow attackers to take over servers, steal sensitive data like API keys and chat logs, and compromise widely used AI frameworks, highlighting critical risks in the rapidly evolving AI security landscape. The vulnerability is rooted in the MCP SDK's foundational design, enabling arbitrary code execution that could lead to server takeover and data breaches. Despite some fixes, Anthropic has declined to implement protocol-level patches, arguing the behavior is intentional, which may leave systems exposed if not addressed through alternative mitigations.

telegram · zaihuapd · Apr 21, 13:31

**Background**: The Model Context Protocol (MCP) is an open-source standard by Anthropic for connecting AI assistants to external data sources and tools, using primitives like tools, resources, and prompts. Remote Code Execution (RCE) is a critical vulnerability that allows attackers to run malicious code on a target system remotely, often leading to full system compromise. CVE (Common Vulnerabilities and Exposures) is a system for cataloging publicly known cybersecurity vulnerabilities, with each assigned a unique identifier for tracking and mitigation.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Model_Context_Protocol">Model Context Protocol - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Arbitrary_code_execution">Arbitrary code execution - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures">Common Vulnerabilities and Exposures - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#Cybersecurity`, `#AI Security`, `#Vulnerability`, `#Anthropic`, `#RCE`

---

<a id="item-2"></a>
## [OpenAI announces ChatGPT Images 2.0, a new AI image generation model.](https://openai.com/index/introducing-chatgpt-images-2-0/) ⭐️ 8.0/10

OpenAI announced ChatGPT Images 2.0, a new version of its AI image generation model, through a livestream event. The release includes updates to features and capabilities, as indicated by community discussions on its technical and ethical aspects. This release is significant as it represents a major advancement in AI image generation from a leading company, potentially setting new standards for quality and creativity in the field. It could impact industries like art, media, and design by enabling more sophisticated and accessible image creation tools. The model is referred to as 'gpt-image-2' in API usage, as shown in a community comment with code examples. However, specific technical details such as model architecture or performance metrics are not provided in the content, and limitations like style consistency issues are noted in discussions.

hackernews · wahnfrieden · Apr 21, 18:50

**Background**: ChatGPT Images is an AI model developed by OpenAI for generating images from text prompts, building on technologies like generative adversarial networks (GANs) or diffusion models. AI image generation has become a key area in machine learning, with models like DALL-E and Stable Diffusion popularizing the ability to create visual content based on natural language descriptions. OpenAI is a prominent research organization known for innovations in AI, including GPT models and image synthesis tools.

**Discussion**: The community discussion shows mixed feelings, with concerns about ethical harms such as impacts on art and consent, and debates over practical applications like replacing photography for sensitive cases. Some users express hope for improved style consistency in tasks like manga creation, while others question the overall utility beyond novelty, with technical experimentation shared via code snippets.

**Tags**: `#AI`, `#image-generation`, `#OpenAI`, `#machine-learning`, `#ethics`

---

<a id="item-3"></a>
## [Vercel's 2026 OAuth breach exposes platform environment variables via AI tool](https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html) ⭐️ 8.0/10

In April 2026, Vercel experienced a security breach where an attacker used an OAuth attack through an AI tool called ContextAI to access platform environment variables, which contained sensitive configuration data. The breach was linked to a Vercel employee granting excessive permissions to the AI tool, allowing lateral movement within the system. This incident highlights critical supply chain risks when third-party AI tools are integrated without proper security controls, potentially affecting thousands of developers and companies relying on Vercel's platform. It demonstrates how OAuth vulnerabilities combined with human error can lead to significant data exposure in cloud-native environments. The attack exploited OAuth misconfigurations where the AI tool requested broad access to Google Workspace services, and Vercel's environment variable management initially lacked a 'sensitive' flag for proper protection. Security researchers noted this was a relatively basic exploit that succeeded due to insufficient vendor risk assessment and enforcement of AI tool policies.

hackernews · queenelvis · Apr 21, 17:14

**Background**: OAuth 2.0 is an authorization framework commonly used for third-party application access, but it's prone to implementation mistakes that can allow attackers to obtain sensitive data. Environment variables are configuration values stored outside application code, often containing secrets like API keys and database passwords that require secure management. Supply chain risks in software development refer to vulnerabilities introduced through third-party components or tools that can compromise entire systems.

<details><summary>References</summary>
<ul>
<li><a href="https://portswigger.net/web-security/oauth">OAuth 2.0 authentication vulnerabilities - PortSwigger</a></li>
<li><a href="https://www.trendmicro.com/en_us/research/22/h/analyzing-hidden-danger-of-environment-variables-for-keeping-secrets.html">Analyzing the Hidden Danger of Environment Variables for Keeping Secrets | Trend Micro (US)</a></li>
<li><a href="https://www.informationweek.com/software-services/how-to-manage-software-supply-chain-risks">How to Manage Software Supply Chain Risks</a></li>

</ul>
</details>

**Discussion**: Community discussion revealed concerns about AI tool security practices, with users questioning why Vercel allowed such broad OAuth permissions and noting the platform's delayed implementation of sensitive environment variable protection. Some commenters criticized the attribution of the attack's speed to AI augmentation as speculative, while others warned this represents a growing trend of AI-enabled security threats in corporate environments.

**Tags**: `#security`, `#OAuth`, `#supply-chain`, `#Vercel`, `#AI-risk`

---

<a id="item-4"></a>
## [Framework Laptop 13 Pro launches with modular design and backward compatibility](https://frame.work/laptop13pro) ⭐️ 8.0/10

Framework has launched the Laptop 13 Pro, featuring a new modular chassis design with a haptic touchpad and improved thermals while maintaining backward compatibility with older Framework Laptop 13 models. The company announced that users can upgrade their existing laptops piece by piece using the new components, with shipments starting in June 2025 and prices beginning at $1,199 for the DIY edition. This represents a significant advancement in the right-to-repair movement by demonstrating that modular laptop design can evolve without creating planned obsolescence, potentially influencing industry standards toward more sustainable hardware. It enables consumers to extend the lifespan of their devices through incremental upgrades rather than complete replacements, reducing electronic waste and ownership costs. The backward compatibility allows users to install new components like the chassis top with haptic touchpad onto older Framework 13 models, while the new chassis can accommodate older mainboards. The laptop features Intel's Panther Lake processors, offers 24+ hours of battery life in a 13-inch form factor, and supports mainline Linux, making it particularly appealing to developers.

hackernews · Trollmann · Apr 21, 18:00

**Background**: Framework is a company that produces modular laptops designed for easy repair and upgradeability, challenging the industry trend toward sealed, non-repairable devices. Modular laptop design involves creating systems where components like the motherboard, keyboard, display, and ports can be individually replaced or upgraded by users. The right-to-repair movement advocates for legislation and design practices that make electronics more repairable to reduce e-waste and give consumers more control over their devices.

<details><summary>References</summary>
<ul>
<li><a href="https://liliputing.com/framework-laptop-13-pro-is-a-modular-laptop-with-longer-battery-life-better-screen-and-up-to-intel-core-ultra-x7-panther-lake/">Framework Laptop 13 Pro is a modular laptop with longer... - Liliputing</a></li>
<li><a href="https://www.msn.com/en-us/news/technology/the-panther-lake-powered-framework-13-pro-still-stays-true-to-its-whole-ethos/ar-AA21pCBX">The Panther Lake powered Framework 13 Pro still stays true to its...</a></li>
<li><a href="https://frame.work/">Framework Computer | Modular Laptops & PCs You Can Repair</a></li>

</ul>
</details>

**Discussion**: Community members expressed initial concern about potential incompatibility but were impressed by the backward compatibility, with one user describing it as "amazing" after reviewing the compatibility table. Several comments praised the technical achievement of making new components work with older designs, while others highlighted the laptop's appeal to developers due to its Linux support and battery life. The CEO's detailed presentations were also noted as engaging for technical enthusiasts.

**Tags**: `#hardware`, `#sustainability`, `#modular-design`, `#laptops`, `#tech-innovation`

---

<a id="item-5"></a>
## [Hobbyist uses Claude Code to find over 500 bugs in Python C-extensions](https://lwn.net/Articles/1067234/) ⭐️ 8.0/10

Daniel Diniz used Claude Code to systematically analyze 44 Python C-extensions, finding over 500 confirmed bugs across nearly a million lines of code, with fixes already merged in 14 projects. He developed a specialized toolkit with 13 analysis agents targeting different bug classes like reference counting and GIL handling issues. This demonstrates how LLMs can be effectively applied to systematic bug detection in complex software components, potentially improving the security and reliability of widely-used Python packages. The responsible reporting approach and collaboration with maintainers sets a positive precedent for AI-assisted code review in open-source ecosystems. The tool achieved a 10-15% false positive rate after review, with bugs ranging from hard crashes and memory corruption to correctness issues. Notable projects affected include Cython, Guppy 3, regex, and Pillow, with the Guppy 3 maintainer fixing 24 of 30 issues and discovering additional bugs the tool missed.

rss · LWN.net · Apr 21, 14:24

**Background**: Python C-extensions allow developers to write performance-critical code in C that interfaces with Python, commonly used in libraries like NumPy and Pillow for speed. Claude Code is Anthropic's AI coding agent that can analyze codebases and run commands. Systematic bug detection involves methodical approaches rather than random code changes, treating debugging as an investigation.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.python.org/3/extending/index.html">Extending and Embedding the Python Interpreter — Python ...</a></li>
<li><a href="https://claude.com/product/claude-code">Claude Code by Anthropic | AI Coding Agent, Terminal, IDE</a></li>
<li><a href="https://hackemtu.com/debugging-mastery-systematic-techniques/">Debugging Mastery: Systematic Bug Hunting Techniques...</a></li>

</ul>
</details>

**Tags**: `#LLMs`, `#Python`, `#Software Testing`, `#Open Source`, `#Bug Detection`

---

<a id="item-6"></a>
## [Developer trains 235M parameter LLM from scratch on single RTX 5080 GPU](https://www.reddit.com/r/LocalLLaMA/comments/1srsxqs/235m_param_llm_from_scratch_on_a_single_rtx_5080/) ⭐️ 8.0/10

A developer created Plasma 1.0, a 235M parameter transformer language model trained completely from scratch using PyTorch on a single RTX 5080 GPU, including custom data processing, tokenization, and training pipelines without any pretrained weights. The model was trained on approximately 5 billion tokens with a sequence length of 1024 using bf16 mixed precision and gradient checkpointing. This demonstrates that meaningful language model development is accessible on consumer hardware, lowering the barrier to entry for researchers and enthusiasts who want to understand the full LLM training pipeline. It provides a practical reference implementation for those interested in building small-scale models from the ground up rather than just fine-tuning existing large models. The model uses LLaMA-style architecture with Grouped Query Attention (16 query heads, 4 KV heads), SwiGLU activation in feed-forward networks, RoPE positional encoding, RMSNorm pre-normalization, and tied embeddings. Training data came from FineWeb-Edu, Wikipedia, StackExchange, code repositories, and ArXiv papers with quality filtering, deduplication, and domain-weighted mixing.

reddit · r/LocalLLaMA · ExcellentTip9926 · Apr 21, 16:32

**Background**: The RTX 5080 is NVIDIA's consumer-grade GPU from the GeForce RTX 50 series, featuring the Blackwell architecture and typically used for gaming and AI workloads. Grouped Query Attention (GQA) is an attention mechanism that groups query heads to share key and value heads, reducing memory usage while maintaining performance compared to standard multi-head attention. SwiGLU is an activation function that combines linear projections with the Swish function, often used in modern transformer models to enhance expressivity.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GeForce_RTX_50_series">GeForce RTX 50 series - Wikipedia</a></li>
<li><a href="https://www.ibm.com/think/topics/grouped-query-attention">What is grouped query attention ? | IBM</a></li>
<li><a href="https://medium.com/@s_boudefel/exploring-swiglu-the-activation-function-powering-modern-llms-9697f88221e7">Exploring SwiGLU : The Activation Function Powering... | Medium</a></li>

</ul>
</details>

**Discussion**: Community members praised the technical achievement while asking detailed questions about dataset curation, evaluation methods, and training specifics. Several users requested more information about domain weighting strategies, deduplication impacts, and training duration, while others expressed interest in collaboration or noted the model's surprisingly coherent outputs compared to typical small-scale implementations.

**Tags**: `#LLM`, `#PyTorch`, `#Transformer`, `#Machine Learning`, `#Open Source`

---

<a id="item-7"></a>
## [Google DeepMind forms coding strike team led by Sebastian Borgeaud, with Sergey Brin involved, to catch up with Anthropic in AI-generated code.](https://www.theinformation.com/articles/google-creates-strik) ⭐️ 8.0/10

Google DeepMind has created a specialized coding strike team led by research engineer Sebastian Borgeaud, with direct involvement from co-founder Sergey Brin and CTO Koray Kavukcuoglu, to close the gap with Anthropic in AI-generated code. The team focuses on improving models for long-term coding tasks, using private codebases for training and implementing internal measures like the Jetski leaderboard and mandatory AI training. This move signifies Google's strategic push to enhance its AI coding capabilities, which could accelerate software development automation and impact the broader AI/ML industry by fostering competition with leaders like Anthropic. It may lead to more efficient AI self-improvement and automation in AI research, affecting software engineering jobs and tool development. Anthropic reportedly generates nearly 100% of its code with AI, while Google's current coding agents handle about 50%, highlighting the performance gap. The team is training models on private codebases to improve performance on internal projects, and long-term goals include enabling AI self-improvement to further automate AI R&D.

telegram · zaihuapd · Apr 21, 01:38

**Background**: Anthropic is a leading AI company known for its Claude models, which have advanced capabilities in code generation and review, as highlighted by tools like Claude Code and Opus 4.7. Google DeepMind is a major AI research division of Google, focusing on machine learning and AI applications, including coding agents. AI-generated code involves using models to automate software development tasks, which can increase efficiency but requires robust training and validation.

<details><summary>References</summary>
<ul>
<li><a href="https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/">Top engineers at Anthropic, OpenAI say AI now writes 100% of their code—with big implications for the future of software development jobs | Fortune</a></li>
<li><a href="https://www.anthropic.com/news/claude-opus-4-7">Anthropic</a></li>

</ul>
</details>

**Tags**: `#AI`, `#Google`, `#Software Engineering`, `#Machine Learning`, `#Industry News`

---

<a id="item-8"></a>
## [Apple Announces CEO Transition: Tim Cook Steps Down, John Ternus to Succeed in 2026](https://t.me/zaihuapd/40981) ⭐️ 8.0/10

Apple has announced a leadership transition where Tim Cook will step down as CEO on September 1, 2026, and be appointed executive chairman of the board, while hardware engineering senior vice president John Ternus will take over as the new CEO on that date. The board unanimously approved this arrangement, with Cook continuing as CEO through the summer to facilitate a smooth handover. This transition is significant as it marks the first CEO change at Apple since Tim Cook succeeded Steve Jobs in 2011, potentially influencing the company's strategic direction, product innovation, and long-term growth in the competitive tech industry. It could impact Apple's hardware development, given Ternus's background in engineering, and signal shifts in leadership style or corporate priorities. John Ternus joined Apple in 2001, was promoted to vice president of hardware engineering in 2013, joined the executive team in 2021, and has recently overseen key products like the iPhone, Mac, iPad, and AirPods. Additionally, current chairman Arthur Levinson will transition to lead independent director on September 1, 2026, with Ternus joining the board on the same day.

telegram · zaihuapd · Apr 21, 12:01

**Background**: Apple Inc. is a global technology company known for products like the iPhone, Mac, and iPad, with Tim Cook serving as CEO since 2011 after Steve Jobs' tenure. CEO transitions at major tech firms often involve strategic planning to ensure continuity and adapt to market trends, with successors typically chosen from internal leadership to maintain corporate culture and expertise.

**Tags**: `#Apple`, `#Leadership`, `#Technology`, `#Business`, `#Management`

---

<a id="item-9"></a>
## [BYD launches second-generation Blade Battery with 9-minute ultra-fast charging from 10% to 97%.](https://t.me/zaihuapd/40984) ⭐️ 8.0/10

BYD has officially launched its second-generation Blade Battery, which achieves a 10% to 97% charge in 9 minutes under normal conditions and maintains fast charging performance in extreme cold, taking only 12 minutes from 20% to 97% at -20°C. This advancement addresses key industry challenges of slow charging and cold-weather performance degradation, potentially accelerating EV adoption by improving convenience and usability in diverse climates, especially in high-latitude regions. The battery uses deep optimization of materials and structure to achieve these speeds, with a notable 5-minute charge from 10% to 70% under normal conditions, and it represents a mass-production-level technological leap for the final 20% charge range.

telegram · zaihuapd · Apr 21, 14:37

**Background**: The BYD Blade Battery is a lithium iron phosphate (LFP) battery designed for electric vehicles, first launched in 2020, known for its blade-like cell arrangement that enhances heat transfer and safety. Ultra-fast charging typically faces limitations in cold weather due to reduced battery efficiency, making BYD's cold-weather performance a significant innovation. LFP batteries are generally more stable and cost-effective than ternary lithium batteries, but have historically lagged in energy density and charging speed.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/BYD_Blade_battery">BYD Blade battery - Wikipedia</a></li>
<li><a href="https://engineerfix.com/how-cold-weather-affects-battery-performance/">How Cold Weather Affects Battery Performance - Engineer Fix</a></li>

</ul>
</details>

**Tags**: `#battery-technology`, `#electric-vehicles`, `#fast-charging`, `#energy-storage`, `#automotive-innovation`

---

<a id="item-10"></a>
## [OpenAI launches Codex Labs and partners with global consultancies to accelerate enterprise deployment.](https://openai.com/index/scaling-codex-to-enterprises-worldwide/) ⭐️ 8.0/10

OpenAI announced the launch of Codex Labs, a program that sends experts into organizations to assist with scaling Codex from pilot to production, and partnered with global system integrators like Accenture, PwC, and Capgemini. Codex now has over 4 million weekly active developers and is being used by companies such as Virgin Atlantic, Cisco, and Rakuten for tasks like code review, incident response, and automation workflows. This initiative is significant because it accelerates the adoption of AI-powered automation in enterprise environments, potentially transforming software development and operational efficiency across industries. By expanding Codex's use beyond coding to browser automation and document processing, it could drive widespread automation in non-programming tasks, enhancing overall business productivity. Codex Labs focuses on practical workshops and standardized integration solutions to help enterprises deploy Codex at scale, with partners also adopting it internally to optimize software delivery models. The expansion into browser automation and document processing leverages AI to handle tasks like data extraction and workflow routing, as seen in tools like AI Browser and LlamaIndex.

telegram · zaihuapd · Apr 21, 16:18

**Background**: OpenAI Codex is an advanced AI tool that generates code from natural language prompts, initially released to assist software developers. It is based on the GPT-3 model and has been used for tasks like code completion and automation in software engineering. Browser automation with AI involves using prompts to control web browsers for tasks like data scraping, while document processing automation uses AI to extract and classify information from documents, as demonstrated by tools like LlamaIndex for OCR and workflow management.

<details><summary>References</summary>
<ul>
<li><a href="https://www.engadget.com/ai/openais-latest-codex-update-builds-the-groundwork-for-its-upcoming-super-app-170000019.html">OpenAI's latest Codex update builds the groundwork for its</a></li>
<li><a href="https://bestaitoolfinder.com/ai-browser/">AI Browser - Best AI Tool Finder</a></li>
<li><a href="https://www.llamaindex.ai/">LlamaIndex | AI Agents for Document OCR + Workflows</a></li>

</ul>
</details>

**Tags**: `#OpenAI`, `#Codex`, `#Enterprise AI`, `#Automation`, `#Software Development`

---

<a id="item-11"></a>
## [Google Launches Gemini 3.1 Pro Deep Research Agents with Private Data Analysis and Chart Generation](https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/) ⭐️ 8.0/10

On April 21, Google introduced two new autonomous research agents called Deep Research and Deep Research Max, both powered by the Gemini 3.1 Pro model. These agents support private enterprise data integration via the Model Context Protocol (MCP) and can natively generate visual charts, with Deep Research optimized for low-latency interaction and Deep Research Max using extended reasoning computation for complex tasks like due diligence. This launch represents a significant advancement in AI-powered enterprise tools, enabling businesses to securely analyze proprietary data and automate complex research workflows. By integrating with financial data providers like FactSet, S&P, and PitchBook, Google is positioning these agents to transform industry analysis and decision-making processes. The service is currently available in public preview through the Gemini API paid tier, with Deep Research Max specifically designed for long-horizon research tasks requiring extended computation time. The MCP integration allows direct access to live data sources without preprocessing, distinguishing it from traditional RAG approaches.

telegram · zaihuapd · Apr 21, 16:45

**Background**: Gemini 3.1 Pro is Google's latest large language model that powers various AI applications. The Model Context Protocol (MCP) is an open standard introduced by Anthropic in 2024 that standardizes how AI systems connect to external data sources and tools. Extended reasoning computation refers to allowing AI models more time during inference to perform complex, multi-step reasoning tasks, which is particularly valuable for research and analysis applications.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Model_Context_Protocol">Model Context Protocol - Wikipedia</a></li>
<li><a href="https://ai.google.dev/gemini-api/docs/deep-research">Gemini Deep Research Agent | Gemini API | Google AI for ...</a></li>
<li><a href="https://www.technologyreview.com/2025/04/16/1115033/adapting-for-ais-reasoning-era/">Adapting for AI’s reasoning era | MIT Technology Review</a></li>

</ul>
</details>

**Tags**: `#AI/ML`, `#Google`, `#Data Analysis`, `#Enterprise Software`, `#Research Tools`

---

<a id="item-12"></a>
## [Claude Code removed from Claude Pro plan, prompting shift to local AI models.](https://i.redd.it/r8mub6oi7mwg1.png) ⭐️ 7.0/10

A Reddit post reports that Claude Code, an AI coding assistant, has been removed from the Claude Pro subscription plan, leading users to consider alternatives like Kimi K2.6 and Qwen 3.6 35B A3B. The post suggests using OpenCode Go for cost-effective access to Kimi K2.6 or running Qwen 3.6 35B A3B locally with a decent graphics card. This change impacts developers who rely on Claude Code for coding assistance, potentially increasing costs or reducing accessibility, and highlights a trend towards local AI models as viable alternatives to cloud-based services. It reflects broader shifts in the AI ecosystem, where pricing adjustments and model availability can drive user migration to open-source or local solutions. The removal may affect existing Claude Pro users differently, with some hoping for grandfathering of prior subscriptions, and alternatives like Kimi K2.6 offer a 1T-parameter hybrid model for coding tasks, while Qwen 3.6 35B A3B requires local hardware such as an 8GB VRAM card for optimal performance. Limitations include potential usage caps on Claude Code before its removal and variable token costs in alternative plans.

reddit · r/LocalLLaMA · bigboyparpa · Apr 21, 21:54

**Background**: Claude Code is an AI-powered coding assistant developed by Anthropic, designed to help developers with programming tasks through cloud-based services. Local AI models like Kimi K2.6 and Qwen 3.6 35B A3B are open-source alternatives that can be run on personal hardware, offering more control and potentially lower costs compared to subscription plans. Kimi K2.6 is a 1T-parameter hybrid model by Moonshot, while Qwen 3.6 35B A3B is a coding-focused model from the Qwen series, requiring specific hardware for local deployment.

<details><summary>References</summary>
<ul>
<li><a href="https://claudecode.app/">Claude Code - 100 Ways to Vibe Coding with Claude AI , Computer...</a></li>
<li><a href="https://unsloth.ai/docs/models/kimi-k2.6">Kimi K2.6 - How to Run Locally | Unsloth Documentation</a></li>
<li><a href="https://www.reddit.com/r/LocalLLaMA/comments/1spyr4t/recommended_parameters_for_qwen_36_35b_a3b_on_a/">Recommended parameters for Qwen 3.6 35B A3B on a 8GB VRAM card ...</a></li>

</ul>
</details>

**Discussion**: Community sentiment is mixed, with some users expressing skepticism about the removal, calling it a 'rug pull,' while others note it might be a mistake or highlight existing usability issues with Claude Code's limits. Discussions include technical alternatives like OpenCode Go and comparisons to other services, as well as concerns about refunds for annual plan subscribers and predictions of future tier restructuring by Anthropic.

**Tags**: `#AI Models`, `#Cloud Services`, `#Local LLMs`, `#Pricing Changes`, `#Community Discussion`

---

<a id="item-13"></a>
## [Gemma 4 Vision Budget Configuration Guide Improves Image Processing](https://www.reddit.com/r/LocalLLaMA/comments/1srrhi5/gemma_4_vision/) ⭐️ 7.0/10

A technical guide explains how to configure Gemma 4's vision budget parameters, specifically --image-min-tokens and --image-max-tokens in llama.cpp, to enhance its image processing capabilities beyond the default settings. The author recommends setting these parameters to 560 and 2240 respectively, along with adjusting --batch-size and --ubatch-size to 4096, to enable the model to detect minute details in images. This matters because many users were overlooking these configuration options, leading to poor performance in tasks like OCR and detail recognition, which could hinder adoption of Gemma 4 for vision applications. Proper configuration can significantly improve the model's effectiveness, making it more competitive against other vision-capable models like Qwen3.5 in the local LLM ecosystem. The default max vision budget for Gemma 4 is 280 tokens (approximately 645K pixels), which the guide argues is insufficient for detailed image analysis. Users must also set --batch-size and --ubatch-size higher than the image-max-tokens value to avoid performance issues, though this increases computational resource consumption.

reddit · r/LocalLLaMA · seamonn · Apr 21, 15:43

**Background**: Gemma 4 is a large language model developed by Google that includes vision capabilities through a variable image resolution feature, allowing it to process images of different sizes. Vision budget parameters like --image-min-tokens and --image-max-tokens control how many tokens are allocated for image representation in models like Gemma 4 when using inference engines such as llama.cpp. Llama.cpp is an open-source tool for running LLMs locally, offering configuration options to optimize model performance for specific tasks like image processing.

<details><summary>References</summary>
<ul>
<li><a href="https://dev.to/someoddcodeguy/a-quick-note-on-gemma-4-image-settings-in-llamacpp-39ng">A Quick Note on Gemma 4 Image Settings in Llama.cpp - DEV Community</a></li>
<li><a href="https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md">llama.cpp/tools/server/README.md at master · ggml-org/llama.cpp</a></li>

</ul>
</details>

**Discussion**: The community discussion shows appreciation for the guide, with users sharing their own configuration experiences, such as using values from Qwen3.5 or setting both parameters to 1120 for higher quality. Some users note that Gemma 4 still underperforms compared to Qwen3.5 in video tasks, and others highlight the complexity of llama.cpp configuration, suggesting tools like LM Studio for ease of use.

**Tags**: `#computer-vision`, `#large-language-models`, `#model-configuration`, `#gemma`, `#llama.cpp`

---

<a id="item-14"></a>
## [Extracted Gemma 4 e4b model from Android AI Edge Gallery reportedly outperforms community quantizations.](https://www.reddit.com/r/LocalLLaMA/comments/1sru6zi/did_google_hide_the_best_version_of_gemma_4_e4b/) ⭐️ 7.0/10

A Reddit user discovered that the Gemma 4 e4b model extracted from Google's Android AI Edge Gallery, weighing 3.6 GB in .litertlm format, appears to perform better than community versions like Unsloth's 3.7 GB GGUF model, which exhibited issues such as incoherent text generation in Russian. This highlights potential performance gaps between official, optimized deployments and community-driven quantizations, impacting developers who rely on local AI models for efficiency and accuracy in applications like mobile AI and edge computing. The extracted model uses the .litertlm format, optimized for zero-copy access via memory mapping, while community versions like Unsloth's GGUF may prioritize English performance and differ in quantization methods, such as Q2_K_XL, which reduces precision to save memory.

reddit · r/LocalLLaMA · LawyerCompetitive478 · Apr 21, 17:15

**Background**: Gemma 4 is an open model family from Google, including the E4B size, designed for tasks across text, vision, and audio. Model quantization compresses models by reducing numerical precision, enabling deployment on resource-limited hardware like mobile devices. The .litertlm format is a custom binary container from Google's LiteRT-LM framework, bundling model weights and tokenizers for efficient on-device inference.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/google/gemma-4-E4B">google/gemma-4-E4B · Hugging Face</a></li>
<li><a href="https://deepmind.google/models/gemma/gemma-4/">Gemma 4 — Google DeepMind</a></li>
<li><a href="https://deepwiki.com/google-ai-edge/LiteRT-LM/9-model-formats-and-distribution">Model Formats and Distribution | google-ai-edge/LiteRT-LM ...</a></li>

</ul>
</details>

**Discussion**: Community sentiment is mixed, with some attributing the performance difference to Google's engineering expertise and calibration with original datasets, while others note that AI Edge is open source and formats like .litertlm are not directly comparable to GGUF. Users expressed interest in downloading the Android version for testing on hardware like the GTX 1060.

**Tags**: `#Gemma 4`, `#model quantization`, `#Android AI`, `#community models`, `#performance comparison`

---

<a id="item-15"></a>
## [Llama.cpp's auto-fit enables Qwen3.6 Q8 with 256k context on 32GB VRAM at 57 t/s](https://www.reddit.com/r/LocalLLaMA/comments/1srvqar/llamacpps_auto_fit_works_much_better_than_i/) ⭐️ 7.0/10

A user discovered that llama.cpp's auto-fit feature allows running the Qwen3.6 Q8 model with 256k context length on 32GB VRAM at 57 tokens per second, even though the model weights alone exceed the available VRAM capacity. This challenges the common assumption that models must fully fit in VRAM to achieve reasonable performance. This breakthrough significantly expands what's possible with limited GPU memory, allowing users to run larger models and longer contexts than previously thought feasible. It democratizes access to state-of-the-art language models for users with consumer-grade hardware rather than requiring expensive professional GPUs. The user achieved this performance using an RTX 5090 connected via Oculink, with the auto-fit feature automatically managing memory allocation between VRAM and system RAM. Community comments suggest further optimizations are possible, including using Q8_0 quantization for KV cache and adjusting the fit target parameter to 512 instead of the default 1024.

reddit · r/LocalLLaMA · a9udn9u · Apr 21, 18:07

**Background**: Llama.cpp is an open-source C/C++ inference engine optimized for running large language models in the GGUF format, known for its efficiency on consumer hardware. The auto-fit feature intelligently splits model layers between GPU VRAM and system RAM when the model doesn't fully fit in VRAM. Qwen3.6 is a large language model from Alibaba that uses a Mixture of Experts (MoE) architecture, where only a subset of parameters are active during inference, making it more memory-efficient than dense models of similar size.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/ggml-org/llama.cpp">GitHub - ggml-org/ llama . cpp : LLM inference in C/C++ · GitHub</a></li>
<li><a href="https://qwen3lm.com/qwen3.6/">Qwen 3 . 6 LLM: Technical Analysis, Features & Comparison (2026)</a></li>

</ul>
</details>

**Discussion**: The community discussion shows enthusiastic reception with users sharing their own successful experiences using auto-fit, including running Qwen3.6 35B Q3_K_M with 256k context on 24GB VRAM at 84 t/s. Technical tips include optimizing KV cache quantization and adjusting fit target parameters, while some note that performance benefits are more pronounced with MoE models like Qwen3.6 compared to dense architectures.

**Tags**: `#llama.cpp`, `#local-llm`, `#vram-optimization`, `#quantization`, `#performance-tuning`

---

<a id="item-16"></a>
## [GitHub Copilot Adjusts Individual Subscription Plans and Pauses New User Registrations](https://github.blog/changelog/2026-04-20-changes-to-github-copilot-plans-for-individuals/) ⭐️ 7.0/10

GitHub announced changes to Copilot individual plans starting April 20, 2026, pausing new user registrations for Student, Pro, and Pro+ tiers while keeping Copilot Free open. The Opus model has been removed from the Pro plan, and Pro+ will eventually remove Opus 4.5 and 4.6 versions while retaining Opus 4.7. This change affects developers who rely on GitHub Copilot for AI-powered coding assistance, potentially limiting access to premium features for new users and reflecting broader trends in AI service cost management and model optimization. It signals how AI tool providers are adjusting offerings to balance service stability with evolving technology. Existing users can still upgrade between plans, with Pro+ offering over 5 times the capacity of Pro. GitHub provides a refund channel for affected users, allowing them to apply for a refund of April fees between April 20 and May 20, 2026.

telegram · zaihuapd · Apr 21, 00:14

**Background**: GitHub Copilot is an AI-powered coding assistant that integrates directly into code editors, offering suggestions and completions to enhance developer productivity. It offers tiered subscription plans: Copilot Free for basic access, Pro ($10/month) with 300 premium requests, and Pro+ ($39/month) with 1,500 premium requests and access to frontier models like Claude Opus. The Opus models (e.g., 4.5, 4.6, 4.7) are advanced AI models from Anthropic, known for high performance in coding and enterprise workflows.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/features/copilot/plans">GitHub Copilot · Plans & pricing</a></li>
<li><a href="https://githubcopilotpricing.com/pro-plan">GitHub Copilot Pro and Pro+ Plans: $10/mo vs $39/mo Explained ...</a></li>
<li><a href="https://www.anthropic.com/claude/opus">Claude Opus 4.7 - Anthropic</a></li>

</ul>
</details>

**Tags**: `#GitHub Copilot`, `#AI Tools`, `#Subscription Changes`, `#Software Development`, `#Product Updates`

---

<a id="item-17"></a>
## [EU enforces new regulations for smartphones and tablets: 800 battery cycles with 80% health and 5+ years of system support starting June 20, 2025.](https://t.me/zaihuapd/40973) ⭐️ 7.0/10

The European Union announced that starting June 20, 2025, all smartphones, tablets, and some feature phones sold in the EU must display an upgraded EPREL label, which includes requirements for battery durability (at least 80% health after 800 cycles) and system support (over 5 years). This label covers seven indicators, such as energy efficiency, battery cycle durability, and IP rating. This regulation could set a global benchmark for device sustainability, pushing manufacturers to improve battery longevity and software updates, which may reduce electronic waste and enhance consumer rights by ensuring longer-lasting products. The EPREL label is an upgrade to the existing ENERGY label, mandated under the Energy Labelling Framework Regulation EU 2017/1369, and it includes specific testing standards like ISO 12405 for battery cycle durability and IP ratings for ingress protection.

telegram · zaihuapd · Apr 21, 02:13

**Background**: The EPREL (European Product Registry for Energy Labelling) is a public registry that standardizes energy efficiency labels for products in the EU, helping consumers compare device performance. Battery cycle durability testing, such as ISO 12405, assesses how many charge-discharge cycles a battery can endure before degrading, while IP ratings indicate a device's resistance to dust and water ingress.

<details><summary>References</summary>
<ul>
<li><a href="https://eprel.ec.europa.eu/">EPREL Public website</a></li>
<li><a href="https://energy-efficient-products.ec.europa.eu/eprel_en">EPREL - European Commission | Energy Efficient Products</a></li>
<li><a href="https://www.testinglab.com/iso-12405-lithium-ion-battery-cycle-durability-testing">ISO 12405 Lithium-Ion Battery Cycle Durability Testing</a></li>

</ul>
</details>

**Tags**: `#EU Regulations`, `#Battery Durability`, `#System Updates`, `#Consumer Electronics`, `#Sustainability`

---

<a id="item-18"></a>
## [Claude Desktop Silently Registers Native Messaging Manifests in Multiple Chromium Browsers](https://www.thatprivacyguy.com/blog/anthropic-spyware) ⭐️ 7.0/10

Anthropic's Claude Desktop application on macOS automatically creates native messaging manifest files in seven Chromium browser directories without user consent or notification. The manifest file points to a binary executable and pre-authorizes three specific Chrome extension IDs to communicate with the host, enabling browser automation capabilities. This behavior raises significant privacy and security concerns as it enables browser automation features like tab opening, login state sharing, DOM reading, and form filling without transparent user consent. It highlights broader issues of transparency and user control in AI software deployment, potentially affecting millions of macOS users who rely on Chromium-based browsers. The manifest file is created at application startup and rewritten on each subsequent run, even if the corresponding browsers are not installed. Anthropic's public documentation does not mention this desktop app bridging feature, though Claude Code has separate documentation for similar functionality.

telegram · zaihuapd · Apr 21, 08:36

**Background**: Native messaging is a Chromium feature that allows browser extensions to communicate with native applications installed on the user's computer through manifest files. These manifest files specify the path to a native messaging host executable and authorize specific extension IDs to establish communication. On macOS, these manifests are typically stored in user-specific directories like ~/Library/Application Support/Google/Chrome/NativeMessagingHosts for various Chromium-based browsers.

<details><summary>References</summary>
<ul>
<li><a href="https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging">Native messaging | Chrome for Developers</a></li>
<li><a href="https://learn.microsoft.com/en-us/microsoft-edge/extensions/developer-guide/native-messaging">Native messaging - Microsoft Edge Developer documentation</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#security`, `#AI`, `#software-engineering`, `#macOS`

---

<a id="item-19"></a>
## [IEA: Global 'Electricity Era' Begins with Record Solar Growth in 2025](https://arstechnica.com/science/2026/04/global-growth-in-solar-the-largest-ever-observed-for-any-source/) ⭐️ 7.0/10

The International Energy Agency (IEA) released its 2025 global energy trends analysis report, declaring the start of an 'electricity era' and noting that 2025 was the first year solar power dominated, with its growth rate setting a historical record for any energy source. Electricity demand grew twice as fast as overall energy demand, and carbon-free energy expansion outpaced demand growth. This shift signals a major acceleration in the global transition from fossil fuels to electrification, driven by rapid solar adoption and electric vehicle sales, which could significantly reduce carbon emissions and reshape energy markets. It highlights the growing role of renewables in meeting climate goals and reducing reliance on oil, especially amid geopolitical tensions like those in the Middle East. Electric vehicle sales accounted for a quarter of total car sales in 2025, with demand surging nearly 40%, causing oil demand growth to drop to 0.7%—less than half the average of the past decade. The IEA projects that the transition will further accelerate in 2026 due to factors like Middle East tensions, emphasizing the interplay between policy, technology, and global events.

telegram · zaihuapd · Apr 21, 15:32

**Background**: The International Energy Agency (IEA) is an autonomous intergovernmental organization established in 1974, based in Paris, that provides authoritative analysis and data on global energy trends, with its flagship World Energy Outlook report updated annually. The 'electricity era' refers to a phase where electricity demand grows rapidly, driven by decarbonization efforts and the shift from fossil fuels to electrified systems, such as in transport and power generation. Solar power, a key renewable energy source, harnesses sunlight to generate electricity and has seen declining costs and technological improvements, making it a central player in the energy transition.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/International_Energy_Agency">International Energy Agency - Wikipedia</a></li>
<li><a href="https://www.iea.org/reports/world-energy-outlook-2025">World Energy Outlook 2025 – Analysis - IEA</a></li>
<li><a href="https://en.wikipedia.org/wiki/Energy_transition">Energy transition - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#energy`, `#sustainability`, `#solar power`, `#electric vehicles`, `#climate change`

---