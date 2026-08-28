---
layout: default
title: "Horizon Summary: 2026-05-12 (EN)"
date: 2026-05-12
lang: en
---

> From 40 items, 16 important content pieces were selected

---

1. [UCLA discovers first stroke rehab drug to repair brain damage](#item-1) ⭐️ 10.0/10
2. [TanStack NPM Packages Hit by Supply Chain Attack with Dead Man's Switch](#item-2) ⭐️ 9.0/10
3. [GitLab Announces Layoffs and Ends CREDIT Values](#item-3) ⭐️ 8.0/10
4. [Ratty: Terminal Emulator with Inline 3D Graphics](#item-4) ⭐️ 8.0/10
5. [Gmail Registration Now Requires QR Code Scan and SMS Sending](#item-5) ⭐️ 8.0/10
6. [CUDA-oxide: Nvidia's Official Rust-to-CUDA Compiler](#item-6) ⭐️ 8.0/10
7. [Software engineering may no longer be a lifetime career due to AI](#item-7) ⭐️ 8.0/10
8. [Shore: AI Coding Agents Must Cut Maintenance Costs](#item-8) ⭐️ 8.0/10
9. [Shopify's River Agent Turns Slack into a Public Teaching Workshop](#item-9) ⭐️ 8.0/10
10. [Linux kernel 7.0.6 and 6.18.29 fix Dirty Frag vulnerability](#item-10) ⭐️ 8.0/10
11. [Debian enforces reproducible builds in testing](#item-11) ⭐️ 8.0/10
12. [Intel Optane build runs 1T parameter model locally at 4 tok/s](#item-12) ⭐️ 8.0/10
13. [Unsloth Releases GGUF Models with MTP Support](#item-13) ⭐️ 8.0/10
14. [MiniCPM 4.6 Released with Improved Document Understanding](#item-14) ⭐️ 8.0/10
15. [Qwen 3.6 35B A3B Shows Dramatic Improvement in Niche Code Understanding](#item-15) ⭐️ 8.0/10
16. [Fake OpenAI Privacy Filter Repo Tops Hugging Face Trends](#item-16) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [UCLA discovers first stroke rehab drug to repair brain damage](https://stemcell.ucla.edu/news/ucla-discovers-first-stroke-rehabilitation-drug-repair-brain-damage) ⭐️ 10.0/10

UCLA researchers have identified the first drug, DDL-920, that can repair brain damage caused by stroke by restoring gamma oscillations in surviving neurons. This discovery was published in 2025 and represents a breakthrough over conventional physical rehabilitation. This is significant because it is the first pharmacological intervention to reverse stroke-induced brain damage, potentially offering a treatment for patients who cannot undergo intensive physical rehabilitation. It could also open avenues for treating other neurodegenerative diseases linked to gamma oscillation deficits. The drug DDL-920 targets parvalbumin neurons to restore gamma oscillations, which are critical for coordinated brain activity and motor recovery. The compound was identified after successful physical rehabilitation in mice and humans showed that restoring gamma oscillations repaired neural connections.

hackernews · bookofjoe · May 11, 17:53 · [Discussion](https://news.ycombinator.com/item?id=48098261)

**Background**: Stroke often causes brain cell death at the infarct core, but surrounding 'bruised' neurons can recover. Gamma oscillations are brain rhythms (30-100 Hz) that link neurons into coordinated networks essential for movement and cognition. After stroke, these oscillations are lost, and physical rehab can restore them over time. UCLA's drug aims to chemically replicate that restoration without intense therapy.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Gamma_oscillations">Gamma oscillations</a></li>
<li><a href="https://medicalxpress.com/news/2025-03-drug-reestablishes-brain-mouse.html">First stroke rehabilitation drug that reestablishes brain connections...</a></li>
<li><a href="https://www.medindia.net/news/healthwatch/first-ever-drug-to-repair-brain-damage-caused-by-stroke-219297-1.htm">First-Ever Drug to Repair Brain Damage Caused by Stroke</a></li>

</ul>
</details>

**Discussion**: Community comments highlight that while the drug targets surviving neurons, it cannot reverse cell death in the infarct core. Some users noted the compound DDL-920 (linked via PubMed) and speculated about its potential for other neurodegenerative diseases. One comment referenced Ted Chiang's story 'Understand,' reflecting awe at the implications.

**Tags**: `#stroke`, `#neuroscience`, `#drug discovery`, `#brain repair`, `#rehabilitation`

---

<a id="item-2"></a>
## [TanStack NPM Packages Hit by Supply Chain Attack with Dead Man's Switch](https://github.com/TanStack/router/issues/7383) ⭐️ 9.0/10

TanStack and other npm packages were compromised in a supply chain attack that deployed malicious postinstall scripts to steal tokens and included a dead man's switch that erases systems if tokens are revoked. This is critical because TanStack is widely used in React and web development; the attack could lead to widespread token theft and data loss among developers and organizations, highlighting the vulnerabilities in npm supply chains. The malicious payload installs a dead man's switch as a systemd user service on Linux or LaunchAgent on macOS, polling api.github.com/user with the stolen token every 60 seconds, and if the token is revoked, it executes rm -rf ~/.

hackernews · varunsharma07 · May 11, 21:08 · [Discussion](https://news.ycombinator.com/item?id=48100706)

**Background**: A supply chain attack occurs when attackers compromise a trusted software package to distribute malware to its users. npm is a popular package manager for JavaScript, and postinstall scripts run automatically after package installation, making them a common vector for malware. TanStack is a suite of open-source libraries for building web applications, including React Router and Query.

<details><summary>References</summary>
<ul>
<li><a href="https://cyberpress.org/dead-mans-switch-widespread-npm-supply-chain-attack-driving-malware-attacks/">Dead Man’s Switch: Widespread npm Supply Chain Attack Driving ...</a></li>
<li><a href="https://docs.npmjs.com/cli/v8/using-npm/scripts/?v=true">scripts | npm Docs</a></li>

</ul>
</details>

**Discussion**: Community members noted the sophistication of the attack, including the dead man's switch, and advised caution when revoking tokens. Some pointed out that this class of attack is possible even with Trusted Publishing if CI is compromised, and criticized GitHub's shared object storage for making malicious fork commits indistinguishable from legitimate ones.

**Tags**: `#security`, `#npm`, `#supply-chain-attack`, `#TanStack`, `#open-source`

---

<a id="item-3"></a>
## [GitLab Announces Layoffs and Ends CREDIT Values](https://about.gitlab.com/blog/gitlab-act-2/) ⭐️ 8.0/10

GitLab has announced a workforce reduction and is replacing its long-standing CREDIT core values with three new AI-focused values: Speed with Quality, Ownership Mindset, and Customer Outcomes. This shift comes as the company pivots its strategy toward the 'agentic era' of AI. This move signals a significant cultural and strategic shift at GitLab, potentially affecting employee morale and company direction. The removal of Diversity, Inclusion & Belonging from core values has drawn criticism, and the heavy focus on AI may impact GitLab's product development and community trust. According to GitLab's blog post, the company believes the 'agentic era' offers its largest opportunity yet, and it is restructuring to meet it. Critics note that despite touting AI, GitLab's existing AI features have been criticized for poor UX, and the layoffs contradict the narrative of needing more resources for growth.

hackernews · AnonGitLabEmpl · May 11, 20:51 · [Discussion](https://news.ycombinator.com/item?id=48100500)

**Background**: GitLab is a DevOps platform that provides a single application for the software development lifecycle. Its CREDIT values (Collaboration, Results, Efficiency, Diversity, Inclusion & Belonging, Iteration, Transparency) were a defining aspect of its company culture, emphasizing collaboration, transparency, and diversity. The company has now decided to abandon these values in favor of a more product- and AI-centric approach, likely in response to market pressures and investor demands.

<details><summary>References</summary>
<ul>
<li><a href="https://handbook.gitlab.com/handbook/values/">GitLab Values</a></li>
<li><a href="https://news.ycombinator.com/item?id=48100500">GitLab Announces Workforce Reduction and End of Their CREDIT ...</a></li>

</ul>
</details>

**Discussion**: The Hacker News community is largely critical of GitLab's announcement. Commenters express disappointment over the removal of DEI values and view the pivot as a buzzword-laden attempt to appease investors. Some question the logic of reducing headcount while claiming the largest opportunity in company history, and others point to ongoing UX issues with GitLab's AI features.

**Tags**: `#gitlab`, `#layoffs`, `#company-culture`, `#ai-strategy`, `#dei`

---

<a id="item-4"></a>
## [Ratty: Terminal Emulator with Inline 3D Graphics](https://ratty-term.org/) ⭐️ 8.0/10

Ratty is a newly released GPU-accelerated terminal emulator that can render 3D models inline alongside traditional text output, using a custom Ratty Graphics Protocol. This innovation blurs the line between terminal and graphical interfaces, opening up new possibilities for data visualization, debugging, and immersive development workflows directly in the command line. Ratty is written in Rust, uses Ratatui for UI, and leverages Bevy for 3D rendering. It supports .obj and .glb models and offers multiple viewing modes including a 3D perspective mode.

hackernews · orhunp_ · May 11, 10:13 · [Discussion](https://news.ycombinator.com/item?id=48093100)

**Background**: Terminal emulators traditionally only display text, but protocols like Sixel and Kitty have enabled inline images. Ratty extends this to 3D, inspired by TempleOS's graphical terminal but designed for modern systems and usability.

<details><summary>References</summary>
<ul>
<li><a href="https://ratty-term.org/">Ratty — A GPU- rendered terminal emulator with inline 3 D graphics</a></li>
<li><a href="https://github.com/orhun/ratty">GitHub - orhun/ratty: A GPU-rendered terminal emulator with ...</a></li>
<li><a href="https://blog.orhun.dev/introducing-ratty/">Ratty: A terminal emulator with inline 3 D graphics - Orhun's Blog</a></li>

</ul>
</details>

**Discussion**: Comments on Hacker News compare Ratty to historical systems like Xerox workstations and Lisp machines, with some highlighting its potential for VR or shallow-3D UIs. Others question performance over SSH and whether it could handle 2D better than existing solutions.

**Tags**: `#terminal emulator`, `#3D graphics`, `#developer tools`, `#open source`, `#Hacker News`

---

<a id="item-5"></a>
## [Gmail Registration Now Requires QR Code Scan and SMS Sending](https://discuss.privacyguides.net/t/google-account-registration-now-requires-sending-an-sms-via-phone-instead-of-receiving-an-sms/36082) ⭐️ 8.0/10

Google has updated Gmail registration to require scanning a QR code and sending an SMS from the user's phone, instead of simply receiving an SMS for verification. This change adds friction and raises privacy concerns for new users, as it forces phone number verification tied to sending a message, potentially deterring sign-ups and impacting accessibility. The QR code opens an SMS URI that pre-fills a text message to Google for verification; it does not automatically send anything. This is essentially the previous phone verification method with added convenience via QR code.

hackernews · negura · May 11, 07:26 · [Discussion](https://news.ycombinator.com/item?id=48092028)

**Background**: Gmail is a widely used email service with billions of users. Phone number verification has long been part of Google's account registration to prevent abuse, but previously often only required receiving an SMS. This change now requires users to send an SMS, which may incur charges or require a capable phone.

**Discussion**: Community comments show mixed reactions; some understand Google’s need to combat spam and abuse, while others criticize the privacy implications and see it as an anti-competitive move. One user clarifies that the QR code simply pre-fills an SMS, not automatically sending it.

**Tags**: `#gmail`, `#privacy`, `#registration`, `#sms`, `#google`

---

<a id="item-6"></a>
## [CUDA-oxide: Nvidia's Official Rust-to-CUDA Compiler](https://nvlabs.github.io/cuda-oxide/index.html) ⭐️ 8.0/10

Nvidia has released CUDA-oxide, an official compiler that compiles Rust code directly to CUDA PTX, allowing Rust programmers to write GPU kernels without using C/C++. This bridge between Rust's memory safety and CUDA's performance could significantly lower the barrier for GPU programming in Rust, expanding the ecosystem for high-performance computing and machine learning. CUDA-oxide targets PTX (Parallel Thread Execution) directly, bypassing higher-level IRs like MLIR or Tile IR; it is an official NVIDIA Labs project, hosted on GitHub under the NVIDIA organization.

hackernews · adamnemecek · May 11, 15:55 · [Discussion](https://news.ycombinator.com/item?id=48096692)

**Background**: CUDA is NVIDIA's proprietary parallel computing platform that allows GPUs to be used for general-purpose processing. PTX is a low-level virtual machine and instruction set architecture that serves as an intermediate representation for CUDA kernels. Rust is a modern systems programming language emphasizing safety and concurrency. CUDA-oxide enables Rust to compile to PTX, thereby allowing Rust code to run on NVIDIA GPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Cuda_platform">Cuda platform</a></li>
<li><a href="https://en.wikipedia.org/wiki/Parallel_Thread_Execution">Parallel Thread Execution - Wikipedia</a></li>
<li><a href="https://docs.nvidia.com/cuda/parallel-thread-execution/index.html">1. Introduction — PTX ISA 9.2 documentation</a></li>

</ul>
</details>

**Discussion**: Commenters expressed excitement about the potential drop-in replacement for existing Rust CUDA crates, raising questions about build times and safety semantics. Some questioned the choice of targeting PTX over higher-level IRs, while others discussed implications for languages like Slang. The overall sentiment is positive and curious about technical details.

**Tags**: `#Rust`, `#CUDA`, `#GPU`, `#compiler`, `#NVIDIA`

---

<a id="item-7"></a>
## [Software engineering may no longer be a lifetime career due to AI](https://www.seangoedecke.com/software-engineering-may-no-longer-be-a-lifetime-career/) ⭐️ 8.0/10

An essay argues that reliance on AI tools like large language models (LLMs) for code generation could lead to skill atrophy among software engineers, potentially shortening their career longevity. This discussion highlights a growing concern in the tech industry about the long-term impact of AI on software engineering roles, affecting career planning, hiring practices, and the nature of the profession itself. The article distinguishes between engineers who augment their reasoning with AI and those who replace it, warning that the latter group may experience technical skill atrophy over time.

hackernews · movis · May 11, 14:34 · [Discussion](https://news.ycombinator.com/item?id=48095550)

**Background**: Large language models (LLMs) are deep learning models trained on vast amounts of text data, capable of generating code and natural language. Their increasing use in software development has sparked debate about whether they supplement or supplant human expertise, with some seeing them as tools that boost productivity and others as a risk to fundamental skill development.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Large_language_model">Large language model - Wikipedia</a></li>
<li><a href="https://www.ibm.com/think/topics/large-language-models">What Are Large Language Models ( LLMs )? | IBM</a></li>

</ul>
</details>

**Discussion**: Community comments are mixed: some developers argue that AI tools only handle a small fraction of their work (2-5% coding), while others note that experienced engineers using AI effectively become more productive. A teacher analogizes that students who replace reasoning with AI may suffer, echoing concerns about skill atrophy. Some also observe a shift in hiring market sentiment, with businesses adopting a 'wait and see' approach.

**Tags**: `#software engineering`, `#AI`, `#career`, `#LLMs`, `#skill atrophy`

---

<a id="item-8"></a>
## [Shore: AI Coding Agents Must Cut Maintenance Costs](https://simonwillison.net/2026/May/11/james-shore/#atom-everything) ⭐️ 8.0/10

James Shore argues that AI coding agents must reduce maintenance costs in inverse proportion to their productivity gains, otherwise they create an unsustainable maintenance burden that grows quadratically. This challenges the dominant narrative that AI coding tools purely boost productivity, revealing a hidden cost that could lead to long-term software debt and undermine tool adoption. Shore's mathematical argument: if an AI doubles code output without halving maintenance costs, total maintenance costs increase by a factor of four (2×2). Only if maintenance costs decrease by the same multiplier can the system remain sustainable.

rss · Simon Willison · May 11, 19:48

**Background**: Software maintenance (fixing bugs, refactoring, adding features) is a major long-term cost in software engineering. AI coding agents can generate code rapidly but may introduce code that is harder to maintain. Shore's argument highlights that productivity gains from AI can be misleading if the resulting code increases long-term maintenance burden.

**Tags**: `#AI coding`, `#software maintenance`, `#productivity`, `#LLMs`

---

<a id="item-9"></a>
## [Shopify's River Agent Turns Slack into a Public Teaching Workshop](https://simonwillison.net/2026/May/11/learning-on-the-shop-floor/#atom-everything) ⭐️ 8.0/10

Shopify CEO Tobias Lütke revealed that their internal AI coding agent, River, operates exclusively in public Slack channels rather than via direct messages, turning every interaction into a transparent learning opportunity for all employees. This approach creates a 'Lehrwerkstatt' (teaching workshop) culture, enabling osmotic learning where employees improve by observing each other's work with the AI agent, potentially serving as a model for collaborative AI integration in organizations. In the last 30 days, 5,938 employees used River across 4,450 channels, and River authored one in eight merged pull requests at Shopify. The agent handles tasks from code review to pull-request creation, but refuses direct messages and directs users to public channels.

rss · Simon Willison · May 11, 15:46

**Background**: Shopify developed River as an internal AI coding agent integrated into Slack. The constraint of public-only operation was designed to foster a transparent environment where employees learn from observing each other's interactions, similar to how Midjourney's early public Discord channels helped users learn prompt engineering through shared experimentation.

<details><summary>References</summary>
<ul>
<li><a href="https://www.zenml.io/llmops-database/building-a-public-ai-agent-workspace-for-organizational-learning">Building a Public AI Agent Workspace for Organizational Learning</a></li>
<li><a href="https://x.com/simonw/status/2053529689122328947">Shopify's River agent system lives in Slack and can only be ...</a></li>

</ul>
</details>

**Tags**: `#AI coding assistant`, `#collaborative learning`, `#transparency`, `#software engineering`, `#internal tool`

---

<a id="item-10"></a>
## [Linux kernel 7.0.6 and 6.18.29 fix Dirty Frag vulnerability](https://lwn.net/Articles/1072311/) ⭐️ 8.0/10

Greg Kroah-Hartman released Linux kernel versions 7.0.6 and 6.18.29 containing a patch from Hyunwoo Kim that fixes CVE-2026-43500, part of the Dirty Frag vulnerability set. All users are strongly advised to upgrade immediately. This is a critical security fix for a local privilege escalation vulnerability that allows any unprivileged user or container process to gain full root access on the host system. Given the widespread use of Linux in servers, cloud, and embedded devices, patching is urgent to prevent potential exploitation. The patch addresses the second Dirty Frag vulnerability (CVE-2026-43500), building on prior fixes for CVE-2026-43284, and also references the related Copy Fail 2 issue. System administrators should upgrade to these stable kernels as soon as possible to mitigate the risk.

rss · LWN.net · May 11, 13:35

**Background**: Dirty Frag is a set of Linux kernel local privilege escalation vulnerabilities disclosed in May 2026, affecting multiple kernel modules. They allow an unprivileged user or a process inside a container to escalate privileges to root. Copy Fail (CVE-2026-31431) is a separate but similar vulnerability that also enables local privilege escalation through a logic bug in the authencesn cryptographic template.

<details><summary>References</summary>
<ul>
<li><a href="https://ubuntu.com/blog/dirty-frag-linux-vulnerability-fixes-available">Dirty Frag Linux kernel local privilege escalation vulnerability ...</a></li>
<li><a href="https://fornex.com/help/linux-cve-2026-43500/">Dirty Frag Vulnerability (CVE-2026-43284, CVE-2026-43500) | Fornex</a></li>
<li><a href="https://arstechnica.com/security/2026/05/linux-bitten-by-second-severe-vulnerability-in-as-many-weeks/">Linux bitten by second severe vulnerability in as many... - Ars Technica</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#security`, `#vulnerability`, `#CVE`, `#fix`

---

<a id="item-11"></a>
## [Debian enforces reproducible builds in testing](https://lwn.net/Articles/1072314/) ⭐️ 8.0/10

Debian's release team, led by Paul Gevers, has enabled migration software to block packages that cannot be reproduced or show reproducibility regressions from entering the testing distribution. This policy change significantly enhances software supply chain security for one of the largest Linux distributions, ensuring that binaries can be verified to match source code. Gioele Barabucci noted that 'reproducible' in this context is limited to building within Debian's own build environment, which is a stricter requirement than usual.

rss · LWN.net · May 11, 13:21

**Background**: Reproducible builds (or deterministic compilation) ensure that building the same source code with the same build environment produces identical binary outputs. This allows independent verification that no malicious modifications were introduced during the build process. Debian has been working with the Reproducible Builds project for years, and this enforcement is a major milestone.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Reproducible_builds">Reproducible builds - Wikipedia</a></li>
<li><a href="https://reproducible-builds.org/">Reproducible Builds — a set of software development practices ...</a></li>

</ul>
</details>

**Discussion**: The community reaction was generally positive, with Gioele Barabucci providing technical nuance about the scope of reproducibility. Some may debate the strictness of the requirement.

**Tags**: `#Debian`, `#reproducible builds`, `#software supply chain`, `#open source`, `#security`

---

<a id="item-12"></a>
## [Intel Optane build runs 1T parameter model locally at 4 tok/s](https://i.redd.it/na7zo7lmck0h1.jpeg) ⭐️ 8.0/10

A builder has demonstrated a local inference setup using Intel Optane Persistent Memory (768GB) to run Moonshot AI's Kimi K2.5, a 1 trillion parameter Mixture-of-Experts model, at approximately 4 tokens per second using llama.cpp with hybrid GPU/CPU inference. This build showcases a cost-effective alternative to expensive high-capacity DRAM for running massive LLMs locally, potentially enabling more hobbyists and researchers to experiment with trillion-parameter models without cloud dependency. The system uses a TYAN S5630GMRE-CGN motherboard, Intel Xeon Gold 6246 CPU, 192GB DDR4 DRAM (as cache), and an RTX 3060 12GB GPU. The Optane PMem in Memory Mode acts as RAM with DRAM caching; the sparse expert weights are hosted on the PMem, while attention and dense layers fit on the GPU.

reddit · r/LocalLLaMA · APFrisco · May 11, 19:54 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1taeg8h/computer_build_using_intel_optane_persistent/)

**Background**: Intel Optane Persistent Memory is a discontinued technology that sits between DRAM and SSD in latency and persistence. It can operate in Memory Mode, where it acts as volatile memory with DRAM as a cache, or App Direct Mode for persistent storage. Kimi K2.5 is an open-source multimodal agentic model from Moonshot AI, using a Mixture-of-Experts architecture with about 1 trillion total parameters but only a fraction activated per token.

<details><summary>References</summary>
<ul>
<li><a href="https://www.storagereview.com/review/intel-optane-persistent-memory-200-series-review-memverge">Intel Optane Persistent Memory 200 Series... - StorageReview.com</a></li>
<li><a href="https://medium.com/intel-analytics-software/accelerate-your-big-data-cluster-13ca362507d4">Accelerate Your Big Data Cluster. Intel Optane Persistent Memory for...</a></li>
<li><a href="https://huggingface.co/moonshotai/Kimi-K2.5">moonshotai/ Kimi - K 2 . 5 · Hugging Face</a></li>

</ul>
</details>

**Discussion**: Community comments reflect both excitement and practicality concerns. Some users praise the clever use of cheap Optane memory to achieve token rates that are 'honestly better than I expected,' while others question the usability of 4 tok/s for interactive tasks. There are also suggestions for optimization, such as using more CPU cores or trying different Optane modes.

**Tags**: `#Intel Optane PMem`, `#LLM Inference`, `#Local LLM`, `#Hardware Build`, `#Large Language Models`

---

<a id="item-13"></a>
## [Unsloth Releases GGUF Models with MTP Support](https://i.redd.it/7qopol51pi0h1.png) ⭐️ 8.0/10

Unsloth has released GGUF versions of Qwen3.6-27B and Qwen3.6-35B-A3B that preserve Multi-Token Prediction (MTP) layers, but users must build and use a specific llama.cpp PR to leverage MTP for faster local inference. MTP support in GGUF format allows local LLM inference to predict multiple tokens per forward pass, significantly boosting speed without needing external draft models. This is a major advancement for efficient local deployment on consumer hardware. The models require llama.cpp PR #15225 or a compatible fork (e.g., ik_llama.cpp) and setting nextn_predict_layers > 0. Some users report that the ik_llama.cpp fork currently offers faster MTP than the official PR.

reddit · r/LocalLLaMA · Altruistic_Heat_9531 · May 11, 14:21 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1ta4rvs/mtp_on_unsloth/)

**Background**: Multi-Token Prediction (MTP) is a training strategy where LLMs learn to predict multiple future tokens simultaneously, reducing sequential decoding steps. This technique is especially beneficial for low-concurrency local inference, as it can double or triple throughput. GGUF is a quantized model format used by llama.cpp for efficient CPU and GPU inference.

<details><summary>References</summary>
<ul>
<li><a href="https://www.ravchat.com/llm-inference-multi-token">Local LLM Inference & Multi - Token Prediction : ik_llama.cpp | RavChat</a></li>
<li><a href="https://blog.gopenai.com/how-multi-token-prediction-mtp-works-in-deepseek-v3-94bb9301989c">How Multi - Token Prediction ( MTP ) works in... | GoPenAI</a></li>
<li><a href="https://github.com/Linus467/llama.cpp-MTP">GitHub - Linus467/llama.cpp-MTP: LLM inference in C/C++</a></li>

</ul>
</details>

**Discussion**: The community is highly excited, with many calling MTP a 'game changer' for local inference. Some users report compilation errors and note that the ik_llama.cpp fork may be faster than the official PR. Others are eagerly awaiting full integration into llama.cpp master.

**Tags**: `#MTP`, `#Unsloth`, `#llama.cpp`, `#GGUF`, `#LLM inference`

---

<a id="item-14"></a>
## [MiniCPM 4.6 Released with Improved Document Understanding](https://huggingface.co/openbmb/MiniCPM-V-4.6) ⭐️ 8.0/10

OpenBMB released MiniCPM-V 4.6, a multimodal small language model with enhanced document understanding, featuring a Qwen3.5-style hybrid LLM backbone and NaViT-packed vision encoder. This release shows that small models can match or exceed larger models in multimodal tasks, enabling efficient local deployment on resource-constrained devices. The model supports text, image, and video inputs, and is available in Q8_0 (812 MB) and F16 (1.52 GB) quantized formats. Community discussion highlights trade-offs between quantization precision and model size.

reddit · r/LocalLLaMA · themrzmaster · May 11, 17:08 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1ta9k8o/minicpm_46/)

**Background**: MiniCPM is a series of small language models developed by OpenBMB, a joint lab from Tsinghua University and ModelBest. Small language models (SLMs) offer a resource-efficient alternative to large models. Quantization reduces model size and memory footprint, enabling faster inference on local hardware.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/openbmb/MiniCPM-V-4.6">openbmb/MiniCPM-V-4.6 · Hugging Face</a></li>
<li><a href="https://github.com/OpenBMB/MiniCPM">GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra ...</a></li>
<li><a href="https://arxiv.org/abs/2404.06395">MiniCPM: Unveiling the Potential of Small Language Models ... openbmb/MiniCPM-V-4.6 · Hugging Face OpenBMB launches MiniCPM-V 4.6 1.3B Instruct MiniCPM: Unveiling the Potential of End-side Large Language ... MiniCPM-V 4.6 - SGLang Documentation MiniCPM-V Series | OpenBMB/MiniCPM-o | DeepWiki</a></li>

</ul>
</details>

**Discussion**: Users debated whether to use Q8_0 or F16 quantization, with some favoring smaller sizes for RAM efficiency. Others noted the model's notable 'PRC bias with deflection behavior' and suggested that adding a blank image tile can bypass behavioral restrictions.

**Tags**: `#MiniCPM`, `#multimodal`, `#small language model`, `#local LLM`, `#quantization`

---

<a id="item-15"></a>
## [Qwen 3.6 35B A3B Shows Dramatic Improvement in Niche Code Understanding](https://www.reddit.com/r/LocalLLaMA/comments/1t9whrt/the_qwen_36_35b_a3b_hype_is_real/) ⭐️ 8.0/10

A Reddit user reports that the new Qwen 3.6 35B A3B model, along with other recent small models, demonstrates significantly improved ability to understand niche academic code, thanks to advanced long-context mechanisms such as Gated DeltaNet and hybrid Mamba2. This breakthrough makes small local models viable for complex code understanding tasks, enabling researchers to feed entire academic papers and codebases into a model running on consumer hardware. The user tested four models: Qwen 3.6 35B A3B, Qwen 3.6 27B, Gemma 4 26B A4B, and Nemotron 3 Nano. All showed marked improvement over previous small models, but fitting long contexts into 32GB RAM remains challenging for some models like Devstral Small 2.

reddit · r/LocalLLaMA · The_Paradoxy · May 11, 07:51

**Background**: Recent open-weight models incorporate linear attention mechanisms like Gated DeltaNet and hybrid Mamba2 to efficiently handle long contexts beyond 64K tokens. Qwen 3.6 35B A3B uses a hybrid architecture with three Gated DeltaNet layers for every Gated Attention layer, and a sparse MoE with 3B active parameters per token, enabling fast inference on consumer GPUs.

<details><summary>References</summary>
<ul>
<li><a href="https://dev.to/czmilo/qwen36-35b-a3b-complete-review-alibabas-open-source-coding-model-that-beats-frontier-giants-4382">Qwen3.6-35B-A3B Complete Review: Alibaba's ... - DEV Community</a></li>
<li><a href="https://apxml.com/models/qwen36-35b-a3b">Qwen3.6 35B A3B: Specifications and GPU VRAM Requirements</a></li>
<li><a href="https://insiderllm.com/guides/qwen-3-6-local-ai-guide/">Qwen 3.6 Complete Guide: 27B Dense, 35B-A3B MoE, and Which to ...</a></li>

</ul>
</details>

**Discussion**: Users share practical experiences: one recommends using Qwen 35B A3B in thinking mode for long context tasks, while another notes the 27B model performs similarly to DeepSeek V4. Some discuss the need for proper sampling settings and quantization levels. A user with a 12GB GPU seeks advice on pairing with a second card.

**Tags**: `#Qwen`, `#LLM`, `#local AI`, `#model benchmark`, `#long context`

---

<a id="item-16"></a>
## [Fake OpenAI Privacy Filter Repo Tops Hugging Face Trends](https://thehackernews.com/2026/05/fake-openai-privacy-filter-repo-hits-1.html) ⭐️ 8.0/10

A malicious repository named Open-OSS/privacy-filter impersonated OpenAI's privacy filter on Hugging Face, distributing a Rust-based infostealer via a loader script. It reached the platform's trending top, amassed 244k downloads and 667 likes, and was subsequently taken down. This incident highlights critical supply chain vulnerabilities in the open-source AI ecosystem, as attackers impersonated a trusted brand to spread malware. It underscores the urgent need for stronger security measures on model hubs like Hugging Face to protect developers and users from data theft. Security firm HiddenLayer discovered six additional similar repositories, and the same infrastructure was used to distribute ValleyRAT, a remote access trojan. The attack infrastructure overlaps with the Silver Fox hacker group, known for tax-themed phishing campaigns.

telegram · zaihuapd · May 11, 12:51

**Background**: Hugging Face is a popular platform for hosting and sharing machine learning models and datasets, often used by developers in AI pipelines. Supply chain attacks target these platforms by injecting malicious code into seemingly legitimate packages, compromising downstream users. ValleyRAT is a remote access trojan that grants attackers unauthorized control over infected systems, and Silver Fox is a threat actor group known for deploying malware via decoy tax-related documents.

<details><summary>References</summary>
<ul>
<li><a href="https://www.zscaler.com/blogs/security-research/technical-analysis-latest-variant-valleyrat">New Updates to ValleyRAT | ThreatLabz - Zscaler</a></li>
<li><a href="https://research.checkpoint.com/2025/cracking-valleyrat-from-builder-secrets-to-kernel-rootkits/">Cracking ValleyRAT: From Builder Secrets to Kernel Rootkits</a></li>
<li><a href="https://mybroadband.co.za/news/security/646153-hacker-group-targeted-companies-in-south-africa-using-fake-sars-notifications.html">Hacker group targeted companies in South Africa using fake SARS...</a></li>

</ul>
</details>

**Tags**: `#security`, `#supply-chain-attack`, `#hugging-face`, `#malware`, `#open-source`

---