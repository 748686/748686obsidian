---
layout: default
title: "Horizon Summary: 2026-06-02 (EN)"
date: 2026-06-02
lang: en
---

> From 69 items, 16 important content pieces were selected

---

1. [AI Support Bot Exploit Bypasses Instagram 2FA](#item-1) ⭐️ 9.0/10
2. [Red Hat npm packages compromised with credential-stealing malware](#item-2) ⭐️ 9.0/10
3. [MiniMax M3: Open-Weight Frontier Model with 1M Context](#item-3) ⭐️ 9.0/10
4. [Nvidia Unveils Vera Rubin Platform, Forecasts $1T Sales](#item-4) ⭐️ 9.0/10
5. [Stanford CS336 Publishes AI Agent Guidelines for Students](#item-5) ⭐️ 8.0/10
6. [RGB Normalization: Divide by 255 or 256?](#item-6) ⭐️ 8.0/10
7. [Stanford CS336: Language Modeling from Scratch](#item-7) ⭐️ 8.0/10
8. [Life's Chemistry May Be Inherently Geological](#item-8) ⭐️ 8.0/10
9. [Nvidia Unveils RTX Spark Arm Processor for Windows](#item-9) ⭐️ 8.0/10
10. [Anthropic Files for IPO with SEC](#item-10) ⭐️ 8.0/10
11. [Recording optimized kernel function signatures in BTF](#item-11) ⭐️ 8.0/10
12. [Top LightGBM Feature Hurt Predictions Due to Label Variance](#item-12) ⭐️ 8.0/10
13. [MLE-Bench gains largely due to better models, not algorithms](#item-13) ⭐️ 8.0/10
14. [NVIDIA Announces Nemotron 3 Ultra LLM](#item-14) ⭐️ 8.0/10
15. [NVIDIA DLSS 4.5 Ray Reconstruction Coming to All RTX GPUs in August](#item-15) ⭐️ 8.0/10
16. [California bill passes requiring offline play after server shutdown](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [AI Support Bot Exploit Bypasses Instagram 2FA](https://www.0xsid.com/blog/meta-account-takeover-fiasco) ⭐️ 9.0/10

Hackers exploited Meta's AI support bot to take over Instagram accounts by tricking it into disabling 2FA and sending password reset emails to arbitrary addresses, as reported by Krebs on Security. This vulnerability reveals a critical flaw in Meta's reliance on AI for account security, as the bot had privileged access that allowed it to bypass strong authentication measures, affecting all Instagram users who trust the platform's security. The AI agent had the ability to remove 2FA from accounts, ignore the account's registered email, and send password reset emails to any address provided by the attacker. This allowed account takeover without any authentication.

hackernews · ssiddharth · Jun 1, 16:31 · [Discussion](https://news.ycombinator.com/item?id=48359102)

**Background**: Two-factor authentication (2FA) adds an extra layer of security by requiring a second factor beyond a password. Automated customer support bots are increasingly used by companies like Meta to handle account recovery, but granting them privileged access to sensitive actions like disabling 2FA creates risk. This exploit demonstrates how social engineering can be applied to AI agents, similar to how attackers manipulate human support staff.

<details><summary>References</summary>
<ul>
<li><a href="https://freedium-mirror.cfd/https://medium.com/p/296664399696">2 FA bypass after fix via manually injecting "isVerifyAuth" cookie in.....</a></li>

</ul>
</details>

**Discussion**: Commenters expressed shock at Meta's negligence, noting that granting an AI agent the ability to remove 2FA and send emails to arbitrary addresses is highly irresponsible. Some shared personal experiences of account takeovers through human support, highlighting that AI is now replicating existing weaknesses. There was agreement that such privileged tools should never be exposed to automated systems.

**Tags**: `#security`, `#AI`, `#exploit`, `#Instagram`, `#Meta`

---

<a id="item-2"></a>
## [Red Hat npm packages compromised with credential-stealing malware](https://lwn.net/Articles/1075742/) ⭐️ 9.0/10

Multiple npm packages under the @redhat-cloud-services scope were compromised with a multi-stage credential harvester that executes on npm install and targets cloud and CI/CD credentials, with self-propagation via stolen tokens. This supply chain attack on a widely used Red Hat scope poses significant risk to users, as the malware is a self-propagating worm that bypasses 2FA using npm's bypass_2fa parameter, and exploits a compromised CI/CD pipeline to republish backdoored versions. The malware was published via GitHub Actions OIDC from the RedHatInsights/javascript-clients repository, indicating the upstream CI/CD pipeline itself was compromised. The payload attempts to explicitly bypass StepSecurity Harden-Runner and is obfuscated in a 4.2 MB index.js file.

rss · LWN.net · Jun 1, 14:05

**Background**: npm packages can execute arbitrary code during installation via 'install' scripts, making them a vector for supply chain attacks. Compromised packages can steal credentials from CI/CD environments, such as GitHub Actions secrets, and use stolen tokens to propagate to other packages, even bypassing two-factor authentication if npm's bypass_2fa parameter is enabled.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/step-security/harden-runner">GitHub - step-security / harden-runner : Harden-Runner is a CI ...</a></li>
<li><a href="https://docs.stepsecurity.io/harden-runner">Harden - Runner | StepSecurity</a></li>

</ul>
</details>

**Discussion**: Community comments on Hacker News emphasize the effectiveness of dependency cooldowns (e.g., 1-2 days delay) to mitigate such attacks, and highlight improvements in package managers like pnpm and yarn 4 that offer similar protections. Some users also note the importance of MFA for publishing and running untrusted code in isolated environments.

**Tags**: `#npm`, `#supply-chain-security`, `#malware`, `#red-hat`, `#credential-theft`

---

<a id="item-3"></a>
## [MiniMax M3: Open-Weight Frontier Model with 1M Context](https://www.reddit.com/r/LocalLLaMA/comments/1ttdiq0/minimax_m3_coding_agentic_frontier_1m_context/) ⭐️ 9.0/10

MiniMax released M3 on June 1, 2026, as the first open-weight model combining frontier-level coding, a 1-million-token context window, and native multimodal capabilities (text, image, video) in a single model. M3 pushes the frontier of LLM capabilities by enabling long-context reasoning and autonomous agentic tasks, which could significantly impact coding assistants, data analysis, and AI agents development. Its open-weight nature allows broad community access and customization. M3 uses sparse attention to achieve 15.6× faster decoding at 1M tokens compared to standard attention, and it outperforms prior models like M2.7 and Claude on agentic benchmarks. The model supports native multimodal inputs including text, images, and video.

reddit · r/LocalLLaMA · /u/dryadofelysium · Jun 1, 01:23

**Background**: Large language models (LLMs) traditionally have limited context windows (e.g., 4K-128K tokens), restricting their ability to process long documents or multi-step tasks. Agentic AI refers to autonomous systems that plan, use tools, and adapt to achieve goals. MiniMax M3 combines a 1M-token context with strong agentic capabilities, enabling handling of entire codebases or extended agent sessions in one pass.

<details><summary>References</summary>
<ul>
<li><a href="https://www.aimadetools.com/blog/minimax-m3-complete-guide/">MiniMax M3 : Complete Guide to the Open-Weight Frontier Model ...</a></li>
<li><a href="https://felloai.com/minimax-m3/">MiniMax M3 : Release Date, Sparse Attention & What to Expect</a></li>
<li><a href="https://lushbinary.com/blog/minimax-m3-developer-guide-benchmarks-pricing-msa-architecture/">MiniMax M3 Developer Guide: Benchmarks & Pricing | Lushbinary</a></li>

</ul>
</details>

**Tags**: `#AI`, `#LLM`, `#coding`, `#multimodal`, `#context`

---

<a id="item-4"></a>
## [Nvidia Unveils Vera Rubin Platform, Forecasts $1T Sales](https://t.me/zaihuapd/41679) ⭐️ 9.0/10

At GTC, Nvidia announced the Vera Rubin platform featuring the Vera CPU and Rubin GPU, along with integration of Groq 3 LPU, targeting agentic AI infrastructure. CEO Jensen Huang forecast that combined sales of Blackwell and Rubin will reach at least $1 trillion by 2027. This announcement signals a major shift in AI hardware, with Nvidia doubling down on next-generation platforms to sustain its dominance. The trillion-dollar forecast underscores the explosive growth in AI infrastructure spending, affecting cloud providers and enterprises worldwide. The Vera CPU is claimed to be twice as efficient and 50% faster than traditional rack-level CPUs, with partner offerings starting later this year. The platform also incorporates Groq's LPU, a chip purpose-built for inference, aiming to reduce costs and latency.

telegram · zaihuapd · Jun 1, 06:10

**Background**: Nvidia's GTC conference is a key event for AI hardware announcements. The Vera Rubin platform follows the Blackwell architecture, targeting the next wave of AI workloads. A Language Processing Unit (LPU) is a custom chip designed specifically for inference, offering faster and more cost-effective AI model execution compared to general-purpose GPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://groq.com/">The Groq LPU delivers inference with the speed and cost developers...</a></li>
<li><a href="https://groq.com/lpu-architecture">LPU | Groq is fast, low cost inference.</a></li>

</ul>
</details>

**Tags**: `#Nvidia`, `#AI infrastructure`, `#hardware`, `#semiconductor`, `#Vera Rubin`

---

<a id="item-5"></a>
## [Stanford CS336 Publishes AI Agent Guidelines for Students](https://github.com/stanford-cs336/assignment1-basics/blob/main/CLAUDE.md) ⭐️ 8.0/10

Stanford's CS336 course has released a CLAUDE.md file providing guidelines for students on using AI agents in assignments, aiming to promote healthy and educational use of AI tools. This initiative reflects the growing need to integrate AI agents into education responsibly, sparking debate on how to design effective instructions that balance learning with assistance. The guidelines are inspired by an earlier AGENTS.md by Carson (of HTMX fame) and have been criticized as overly verbose, potentially exceeding context windows of some AI models.

hackernews · prakashqwerty · Jun 1, 16:41 · [Discussion](https://news.ycombinator.com/item?id=48359232)

**Background**: AI agents are tools that can assist with coding and problem-solving, but their use in education raises concerns about academic integrity and genuine learning. Guidelines like these attempt to set boundaries, instructing the AI to act as a tutor rather than a solution provider.

**Discussion**: The community comments show mixed opinions: some appreciate the effort but find the guidelines too verbose, others suggest learning modes and custom harnesses, and one commenter notes it is a close copy of Carson's earlier work.

**Tags**: `#AI agents`, `#education`, `#guidelines`, `#Stanford`, `#CS336`

---

<a id="item-6"></a>
## [RGB Normalization: Divide by 255 or 256?](https://30fps.net/pages/255-vs-256-division/) ⭐️ 8.0/10

An article on 30fps.net explores the subtle difference between normalizing RGB integer values by 255 versus 256, analyzing how each choice affects color accuracy in computer graphics and image processing. This distinction matters because the normalization factor directly impacts the mapping of integer colors to the floating-point range, influencing rendering pipelines, color conversions, and hardware interfaces like VGA signal generation. Dividing by 256 maps values 0–255 to 0.0–0.996..., leaving 1.0 unattainable, while dividing by 255 maps 255 exactly to 1.0 but creates unequal bin spacing; the article also discusses the use of +0.5 offset and truncation.

hackernews · pplanu · Jun 1, 17:37 · [Discussion](https://news.ycombinator.com/item?id=48360054)

**Background**: RGB color values are commonly stored as 8-bit integers (0–255) per channel, and need normalization to floating-point [0,1] for computation. The choice between 255 and 256 reflects different interpretations: 255 treats the maximum integer as full intensity, while 256 treats the range as equally spaced intervals. This is analogous to the 'max value' vs 'number of steps' distinction in quantization theory.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/RGB_color_model">RGB color model - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Commenters note that for 8-bit displays the difference is negligible, but for analog video signal generation it becomes critical. Some advocate adding 0.5 before truncation to avoid half-sized bins at extremes, while others argue that centered sampling models continuous light intensity more accurately.

**Tags**: `#computer graphics`, `#color representation`, `#RGB normalization`, `#image processing`

---

<a id="item-7"></a>
## [Stanford CS336: Language Modeling from Scratch](https://cs336.stanford.edu/) ⭐️ 8.0/10

Stanford University's CS336 course offers a comprehensive, hands-on curriculum for building language models from scratch, covering recent advances such as transformers and pretraining. This course fills a gap in educational resources by providing a deep, implementation-focused understanding of modern language models, which is valuable for practitioners and researchers. The course requires significant compute resources, with assignments involving training GPT-2 scale models; the instructor suggests using cloud GPUs like B200 at $4.99/hour.

hackernews · kristianpaul · Jun 1, 14:10 · [Discussion](https://news.ycombinator.com/item?id=48357075)

**Background**: Language modeling is a fundamental task in NLP, where models learn to predict the next word in a sequence. Recent advances like the Transformer architecture and large-scale pretraining have led to powerful models like GPT. CS336 teaches the full pipeline from data processing to training and evaluation, with all code written from scratch.

**Discussion**: Community members shared mixed experiences: one noted the course is very time-consuming even for those with deep learning background, while another reported success in implementing a GPT-1 variant using Claude AI. Another commenter questioned the need for expensive GPUs, suggesting cheaper alternatives like a 4090.

**Tags**: `#language modeling`, `#stanford`, `#deep learning`, `#NLP`, `#course`

---

<a id="item-8"></a>
## [Life's Chemistry May Be Inherently Geological](https://www.quantamagazine.org/the-dirt-that-refused-to-die-20260601/) ⭐️ 8.0/10

A Quanta Magazine article reports that what appear to be biochemical processes may actually be inherent geological features, challenging conventional assumptions about the origins of life. This paradigm-shifting hypothesis blurs the line between geology and biology, potentially redefining how we search for life beyond Earth and understand life's emergence on our planet. The article builds on decades of speculation that geochemistry can spawn biochemistry, citing examples like geothermal processes creating stable energy gradients that manufacture organic compounds.

hackernews · speckx · Jun 1, 15:11 · [Discussion](https://news.ycombinator.com/item?id=48357905)

**Background**: Abiogenesis is the natural process by which life arises from non-living matter. Geochemical processes that mimic biochemistry, such as the formation of organic compounds at hydrothermal vents, have long been studied as potential precursors to life.

<details><summary>References</summary>
<ul>
<li><a href="https://www.allaboutscience.org/abiogenesis.htm">Abiogenesis</a></li>
<li><a href="https://en.wikipedia.org/wiki/Biosignature">Biosignature - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Commenters noted this idea has been speculated for at least a decade, with references to abiogenic petroleum and excitement for missions to Europa and Enceladus. One comment raised questions about protein mass spectrometry to detect residual enzymes.

**Tags**: `#origins of life`, `#geochemistry`, `#astrobiology`, `#biochemistry`, `#earth science`

---

<a id="item-9"></a>
## [Nvidia Unveils RTX Spark Arm Processor for Windows](https://www.nvidia.com/en-us/products/rtx-spark/) ⭐️ 8.0/10

Nvidia has announced the RTX Spark, an Arm-based processor for Windows laptops and desktops that integrates a CPU, GPU, and AI accelerator, targeting a 1-petaflop performance level. The chip is designed to compete with Apple's M-series and traditional x86 chips from Intel and AMD. This marks Nvidia's first major push into the CPU market for consumer PCs, potentially disrupting the long-standing x86 dominance by Intel and AMD. If successful, it could accelerate the adoption of Windows on Arm and offer an alternative with superior AI and graphics capabilities. The RTX Spark chip includes a full CUDA and RTX ecosystem, supporting over 100 Windows software providers for native Arm ports, including Adobe, Blender, and games like League of Legends. However, early reviews note concerns about memory speed being half that of Apple's M5 and one-third of the M3 Ultra.

hackernews · shenli3514 · Jun 1, 05:24 · [Discussion](https://news.ycombinator.com/item?id=48352939)

**Background**: Arm-based processors have been used primarily in mobile devices, but recently Apple's M-series chips demonstrated that high-performance Arm chips can excel in laptops and desktops. Nvidia already has expertise in AI and GPUs, and with RTX Spark, it combines these with an Arm CPU to create a unified chip. Windows on Arm has historically struggled with software compatibility, but Nvidia's market influence is helping to secure native ports from major developers.

<details><summary>References</summary>
<ul>
<li><a href="https://www.nvidia.com/en-us/products/rtx-spark/">Slim Laptops & Small Desktops | NVIDIA RTX Spark</a></li>
<li><a href="https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pwMGY2YkVSRUpfTTB4UnFYRk5TZ0FQAQ?hl=en-NG&gl=NG&ceid=NG:en">Google News - Nvidia unveils RTX Spark chip for AI personal...</a></li>

</ul>
</details>

**Discussion**: The community reaction is mixed: some are excited about Nvidia's ability to bring Arm ports to major games and creative apps, while others are skeptical about compatibility and performance, particularly memory speed compared to Apple's chips. One user noted that the RTX Spark seems like a rebranded DGX Spark in laptop form, with limited memory bandwidth.

**Tags**: `#Nvidia`, `#RTX Spark`, `#Arm`, `#AI`, `#Hardware`

---

<a id="item-10"></a>
## [Anthropic Files for IPO with SEC](https://www.anthropic.com/news/confidential-draft-s1-sec) ⭐️ 8.0/10

Anthropic has confidentially submitted a draft S-1 registration statement to the U.S. Securities and Exchange Commission, signaling its intention to go public. The company stated that the final decision to launch an IPO will depend on market conditions and other factors. As a leading AI company, Anthropic's potential IPO marks a significant milestone for the industry and could expose retail and 401(k) investors to AI stocks. The shift from private to public markets will subject the company to quarterly earnings scrutiny, which may impact its long-term strategy and transparency. The confidential filing allows Anthropic to keep its financial details and business plans private during the SEC review process. The number of shares to be offered and the price range have not yet been determined, and the IPO may not proceed if conditions are unfavorable.

hackernews · surprisetalk · Jun 1, 16:00 · [Discussion](https://news.ycombinator.com/item?id=48358646)

**Background**: A Form S-1 is a registration statement required by the SEC for companies planning to go public, providing detailed information about the business, financials, and risks. Confidential IPO filings, allowed under the JOBS Act for emerging growth companies, enable firms to negotiate with the SEC privately before making their filings public, reducing market speculation during the review process.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Form_S-1">Form S-1 - Wikipedia</a></li>
<li><a href="https://www.newsfilecorp.com/filing/edgar/forms1.php">Form S-1 Filing Service SEC EDGAR</a></li>

</ul>
</details>

**Discussion**: The community expressed concerns about retail investors gaining exposure to AI stocks through index funds, the pressure of quarterly earnings calls, and the race to go public before market conditions change. Some commenters also noted that SpaceX recently submitted an amendment to its S-1, highlighting a broader trend of high-profile IPOs.

**Tags**: `#AI`, `#IPO`, `#Anthropic`, `#finance`, `#regulation`

---

<a id="item-11"></a>
## [Recording optimized kernel function signatures in BTF](https://lwn.net/Articles/1073762/) ⭐️ 8.0/10

Alan Maguire and Yonghong Song proposed recording changed function signatures in BTF debugging info to handle three common compiler optimizations that alter kernel function signatures. This work enables accurate tracing and BPF programs to work with optimized kernel functions, improving the kernel's debugging and observability infrastructure. The three cases are: argument removal, field extraction from structures, and struct pointer to value conversion. The approach uses the pahole utility to reverse-engineer DWARF data into BTF true signatures.

rss · LWN.net · Jun 1, 18:59

**Background**: BTF (BPF Type Format) is a debug info format used by the Linux kernel for BPF programs and tracing. DWARF is a broader debug format that represents source-level types, but its maintainers rejected extending it for runtime signature information. Pahole is a tool that parses DWARF and generates BTF, commonly used in kernel builds.

<details><summary>References</summary>
<ul>
<li><a href="https://www.kernel.org/doc/html/next/bpf/btf.html">BPF Type Format ( BTF ) — The Linux Kernel documentation</a></li>
<li><a href="https://cateee.net/lkddb/web-lkddb/DEBUG_INFO_BTF.html">Linux Kernel Driver DataBase: CONFIG_ DEBUG _ INFO _ BTF ...</a></li>
<li><a href="https://android.googlesource.com/kernel/build/+/master/kleaf/docs/btf.md">BTF debug information</a></li>

</ul>
</details>

**Tags**: `#kernel`, `#BTF`, `#BPF`, `#tracing`, `#compiling`

---

<a id="item-12"></a>
## [Top LightGBM Feature Hurt Predictions Due to Label Variance](https://www.reddit.com/r/MachineLearning/comments/1tu0y14/why_our_1_lightgbm_feature_by_importance_made/) ⭐️ 8.0/10

A practitioner found that a Bayesian target encoder feature ranked #1 by LightGBM importance actually worsened test MAPE by 0.28 percentage points in a 4-seed × 3-variant ablation study. This highlights a common pitfall in gradient boosting where feature importance can be misleading due to the model capturing irreducible label variance, reminding practitioners to validate important features with ablation studies. The encoder was designed to isolate within-reference pricing dynamics but instead learned splits that failed to generalize because the signal came from unobserved factors like condition nuance, seller behavior, and timing.

reddit · r/MachineLearning · /u/Nj-yeti · Jun 1, 18:20

**Background**: LightGBM is a gradient boosting framework that can compute feature importance scores based on how often a feature is used for splitting. However, high importance does not guarantee predictive value, especially when the feature captures noise rather than signal. Bayesian target encoding maps categorical variables to numerical representations using target statistics, but can leak label information if not regularized properly.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/data-science/target-encoding-and-bayesian-target-encoding-5c6a6c58ae8c">Target Encoding and Bayesian Target Encoding | by Michael ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Gradient_boosting">Gradient boosting - Wikipedia</a></li>
<li><a href="https://bayte.readthedocs.io/en/latest/index.html">Bayesian target encoding documentation - bayte.readthedocs.io</a></li>

</ul>
</details>

**Tags**: `#LightGBM`, `#feature importance`, `#ablation study`, `#gradient boosting`, `#machine learning`

---

<a id="item-13"></a>
## [MLE-Bench gains largely due to better models, not algorithms](https://www.reddit.com/r/MachineLearning/comments/1ttu47l/how_much_of_mlebenchs_gains_are_the_algorithm_vs/) ⭐️ 8.0/10

A critical analysis reveals that the perceived gains in MLE-Bench scores from 30% to 80% over two years are predominantly due to improved base models and problem shifts, not genuine algorithmic progress. This finding challenges the notion of rapid algorithmic advancement in automated ML, and the introduction of FML-Bench provides a standardized evaluation to isolate algorithmic efficiency, which is crucial for fair benchmarking. When controlling for the same step budget and models, and testing on different tasks, the two-year-old AIDE algorithm matches modern agent/evolutionary search systems, suggesting minimal algorithmic improvement.

reddit · r/MachineLearning · /u/Educational_Strain_3 · Jun 1, 14:34

**Background**: MLE-Bench is a benchmark for automated machine learning research that measures performance on machine learning engineering tasks. FML-Bench is a new benchmark that unifies the code editing agent, step definition, and validation/test split to more fairly evaluate algorithmic efficiency separate from model improvements and problem design choices.

**Tags**: `#machine learning`, `#benchmarking`, `#automated ML`, `#algorithms`, `#AI research`

---

<a id="item-14"></a>
## [NVIDIA Announces Nemotron 3 Ultra LLM](https://www.reddit.com/r/LocalLLaMA/comments/1tthkh5/nvidia_announces_nemotron_3_ultra/) ⭐️ 8.0/10

NVIDIA has announced the Nemotron 3 Ultra, the largest model in its new Nemotron 3 family of open-source large language models, designed for agentic AI applications. This release provides the AI community with a powerful, open-weight model that balances efficiency and accuracy, enabling developers to build sophisticated AI agents locally or in the cloud. The Nemotron 3 family includes three sizes: Nano, Super, and Ultra, with open weights, training data, and recipes, making it the most efficient family of open models for agentic AI with leading accuracy.

reddit · r/LocalLLaMA · /u/themixtergames · Jun 1, 04:34

**Background**: Nemotron is NVIDIA's family of open-source large language models designed for agentic AI, which are AI systems that can autonomously reason and act. The Nemotron 3 series continues this line with improved efficiency and accuracy, targeting applications like autonomous agents and conversational AI.

<details><summary>References</summary>
<ul>
<li><a href="https://research.nvidia.com/labs/nemotron/Nemotron-3/">NVIDIA Nemotron 3 Family of Models</a></li>
<li><a href="https://nvidianews.nvidia.com/news/nvidia-debuts-nemotron-3-family-of-open-models">NVIDIA Debuts Nemotron 3 Family of Open Models</a></li>
<li><a href="https://developer.nvidia.com/nemotron">Nemotron AI Models | NVIDIA Developer</a></li>

</ul>
</details>

**Tags**: `#AI`, `#NVIDIA`, `#LLM`, `#Machine Learning`, `#NLP`

---

<a id="item-15"></a>
## [NVIDIA DLSS 4.5 Ray Reconstruction Coming to All RTX GPUs in August](https://videocardz.com/newz/nvidia-dlss-4-5-ray-reconstruction-coming-in-august-for-rtx-20-30-40-and-50-series) ⭐️ 8.0/10

NVIDIA announced DLSS 4.5 Ray Reconstruction, which will be available via the NVIDIA App in August for all GeForce RTX 20, 30, 40, and 50 series GPUs. The update introduces a second-generation Transformer model offering 35% more compute and 20% more parameters, improving ray tracing accuracy, temporal stability, and motion clarity. This update benefits a wide range of RTX users across multiple generations by enhancing ray tracing and path tracing visuals without requiring new hardware. It also expands support to 27 games at launch and Blender Cycles, making high-quality ray tracing more accessible in both gaming and creative workflows. The new Transformer model in DLSS 4.5 improves upon the previous version with faster performance and higher quality, while maintaining similar overall performance to the current version. Blender 5.3, scheduled for fall 2025, will integrate the denoiser for real-time viewport previews.

telegram · zaihuapd · Jun 1, 07:51

**Background**: DLSS (Deep Learning Super Sampling) is NVIDIA's AI-powered upscaling technology that uses deep learning to reconstruct higher-resolution images from lower-resolution inputs. Ray Reconstruction is a feature that replaces traditional denoising methods with an AI network to produce more accurate and stable ray-traced lighting. The Transformer model is a neural network architecture that has been adapted for real-time graphics, offering better handling of complex scenes and temporal data.

<details><summary>References</summary>
<ul>
<li><a href="https://www.nvidia.com/en-us/geforce/news/dlss4-multi-frame-generation-ai-innovations/">NVIDIA DLSS 4 Introduces Multi Frame Generation... | NVIDIA</a></li>
<li><a href="https://www.nvidia.com/en-us/geforce/news/nvidia-dlss-3-5-ray-reconstruction/">NVIDIA DLSS 3.5: Enhancing Ray Tracing With AI; Coming This</a></li>

</ul>
</details>

**Tags**: `#NVIDIA`, `#DLSS`, `#Ray Tracing`, `#GPU`, `#Graphics`

---

<a id="item-16"></a>
## [California bill passes requiring offline play after server shutdown](https://www.eurogamer.net/stop-killing-games-passes-floor-vote-california) ⭐️ 8.0/10

The California Assembly passed the Protect Our Games Act (AB 1921) with a 43-16 vote, requiring game publishers to provide offline versions or community servers before shutting down online services, or offer full refunds. This bill represents a major legislative milestone for digital preservation and consumer rights in gaming, potentially setting a precedent that could compel publishers to maintain playability of purchased games indefinitely. The bill applies to digital games released or resold after January 1, 2027, and requires at least 60 days' notice before service termination. Publishers unable to provide offline play must issue full refunds.

telegram · zaihuapd · Jun 1, 12:01

**Background**: The bill is a key victory for the 'Stop Killing Games' movement, which began in 2024 after Ubisoft shut down servers for 'The Crew', making the game unplayable. Similar consumer protection initiatives in Europe have garnered over 1.3 million signatures. The legislative process now moves to the California State Senate, with the bill set to take effect in 2027 if passed.

<details><summary>References</summary>
<ul>
<li><a href="https://www.eurogamer.net/stop-killing-games-passes-floor-vote-california">Stop Killing Games consumer protection bill passes... | Eurogamer.net</a></li>
<li><a href="https://en.wikipedia.org/wiki/Stop_Killing_Games">Stop Killing Games - Wikipedia</a></li>
<li><a href="https://www.allkeyshop.com/blog/california-assembly-passes-video-game-preservation-bill-news-d/">California Assembly Passes Bill Mandating Video Game Preservation</a></li>

</ul>
</details>

**Tags**: `#gaming`, `#digital preservation`, `#consumer rights`, `#legislation`, `#game preservation`

---