---
layout: default
title: "Horizon Summary: 2026-05-04 (EN)"
date: 2026-05-04
lang: en
---

> From 33 items, 6 important content pieces were selected

---

1. [Desktop for One: Surge of AI-Built Personal Software](#item-1) ⭐️ 8.0/10
2. [Covert Surveillance Actors Exploit Global Telecom Networks](#item-2) ⭐️ 8.0/10
3. [Why Modern Text User Interfaces Are an Accessibility Nightmare](#item-3) ⭐️ 8.0/10
4. [Why Terminal User Interfaces (TUIs) Are Making a Comeback](#item-4) ⭐️ 8.0/10
5. [Security through obscurity is not bad](#item-5) ⭐️ 8.0/10
6. [Local LLM Speed Soars from 1 to 100 tk/s in 2 Years](#item-6) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Desktop for One: Surge of AI-Built Personal Software](https://isene.org/2026/05/Audience-of-One.html) ⭐️ 8.0/10

Developers are increasingly building highly personalized software environments, like custom desktop setups, using AI coding tools such as Claude. The linked article exemplifies a desktop made entirely for one person's needs, a practice that is becoming more common. This shift could democratize software creation, allowing individuals to craft tools perfectly tailored to their workflows without waiting for mass-market solutions. It may reshape how software is developed and valued, emphasizing personal efficiency over broad appeal. Examples from the discussion include custom window managers, shells, editors, and file managers written in Ruby, now enhanced by AI. However, AI coding assistants like Claude Code can be expensive, and the resulting software often contains bugs and idiosyncrasies acceptable only to the creator.

hackernews · xngbuilds · May 3, 15:32

**Background**: For decades, tech enthusiasts have customized their workflows with scripts and config files, but building entire applications from scratch was labor-intensive. AI coding tools now drastically lower the barrier, enabling creation of 'extremely personal software'—programs designed for a single user's unique needs, often by that user themselves.

**Discussion**: Commenters largely embrace the trend, with some coining terms like 'Extremely Personal Software' and predicting rapid growth. Cost and practical limitations are noted, but the overall sentiment is excitement about AI enabling greater personalization in software.

**Tags**: `#personal software`, `#ai-assisted development`, `#desktop environment`, `#hacker news discussion`, `#software customization`

---

<a id="item-2"></a>
## [Covert Surveillance Actors Exploit Global Telecom Networks](https://citizenlab.ca/research/uncovering-global-telecom-exploitation-by-covert-surveillance-actors/) ⭐️ 8.0/10

Citizen Lab released a report revealing that covert surveillance actors exploited SS7 vulnerabilities in Israeli telecom networks to track individuals globally. This shows systemic weaknesses in telecom infrastructure, enabling mass surveillance without consent and threatening the privacy of billions of mobile subscribers worldwide. The report links Israeli telecoms to surveillance via SS7 and Diameter traffic analysis, though some evidence is circumstantial; SIM card attacks were not addressed.

hackernews · miohtama · May 3, 16:15

**Background**: SS7 is a 1970s telephony signaling protocol lacking authentication, allowing location tracking, call interception, and SMS redirection if network access is gained. Diameter for 4G adds some security but remains vulnerable. These weaknesses have been long known but widely unaddressed.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Signalling_System_No._7">Signalling System No. 7 - Wikipedia</a></li>
<li><a href="https://learn.rbbn.com/hubfs/Corporate+Marketing+(TOP+LEVEL)/Solution+Brief/SB+SS7+Vulnerabilities.pdf">SS 7 Vulnerabilities</a></li>

</ul>
</details>

**Discussion**: Comments include a telecom expert finding some attribution claims circumstantial, another noting SS7's inherent insecurity makes it hardly an 'exploit', and a reminder to read the original Citizen Lab report.

**Tags**: `#security`, `#surveillance`, `#telecom`, `#SS7`, `#privacy`

---

<a id="item-3"></a>
## [Why Modern Text User Interfaces Are an Accessibility Nightmare](https://xogium.me/the-text-mode-lie-why-modern-tuis-are-a-nightmare-for-accessibility) ⭐️ 8.0/10

A new article reveals that modern Text User Interfaces (TUIs) like Claude Code's Ink-based renderer often use complex terminal escape codes and layered rendering, which can break screen readers and accessibility tools. Developers often assume terminal applications are inherently accessible, but this misconception may exclude users with disabilities from critical developer tools and workflows, counteracting ongoing efforts toward inclusive software. Issues include ANSI escape sequences for complex layouts, overlapping curse repositioning that confuses screen readers, and settings like CLAUDE_CODE_NO_FLICKER=1 to reduce visual noise, all of which hinder sequential text parsing.

hackernews · SpyCoder77 · May 3, 23:59

**Background**: Text User Interfaces (TUIs) are full-screen applications inside terminal emulators, using character grid, box-drawing, and colors to create interactive forms and panes. Unlike streaming command-line output, they actively manage the entire screen, often redrawing portions. This conflicts with traditional screen readers designed for linear text streams. Modern frameworks like Ink render components into escape codes, which can produce flickering and inaccessible layering.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Text_user_interface">Text user interface</a></li>

</ul>
</details>

**Discussion**: Community reaction is largely critical of modern TUI design, calling it bloated and misguided. Some users prefer the original terminal streaming model, while others doubt that developers actually believe TUIs are universally accessible. A few speculate about sprite-based or alternative TUI paradigms.

**Tags**: `#TUI`, `#accessibility`, `#terminal`, `#UI design`, `#software engineering`

---

<a id="item-4"></a>
## [Why Terminal User Interfaces (TUIs) Are Making a Comeback](https://wiki.alcidesfonseca.com/blog/why-tuis-are-back/) ⭐️ 8.0/10

The resurgence of terminal user interfaces (TUIs) is being driven by modern developer tools like Claude Code, the ability to deliver apps over SSH without local installs, and growing dissatisfaction with current graphical and web-based UI options. This trend reflects a shift toward lightweight, efficient, and cross-platform interfaces that bypass the bloat and fragmentation of OS-native and web UIs, directly impacting developer workflows and remote application access. Tools like Claude Code, Anthropic's AI coding assistant, operate natively in the terminal, while projects like pico.sh deploy TUIs accessible via SSH without any client-side installation, showcasing the practical advantages of this approach.

hackernews · rickcarlino · May 3, 18:42

**Background**: Terminal user interfaces (TUIs), also known as text-based user interfaces, use character-cell displays and often support mouse input and colors, running inside terminal emulators. They predate graphical user interfaces (GUIs) and are known for their speed, low resource usage, and keyboard-driven operation. Recent advances in terminal technology and the rise of developer-centric tools have sparked renewed interest. SSH (Secure Shell) allows secure remote access to command-line interfaces, enabling server-hosted applications to be used from any terminal without local installation.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Terminal_user_interface">Terminal user interface</a></li>
<li><a href="https://en.wikipedia.org/wiki/Claude_Code">Claude Code</a></li>

</ul>
</details>

**Discussion**: Community reactions are mixed: some point to Claude Code and SSH-based delivery as primary drivers, while others lament TUIs' lack of modern UI conveniences like standard keyboard shortcuts and password manager integration. However, many agree that the fragmentation of OS-native and web UIs has left a gap that TUIs are well-suited to fill.

**Tags**: `#TUI`, `#terminal`, `#developer-tools`, `#SSH`, `#Claude-Code`

---

<a id="item-5"></a>
## [Security through obscurity is not bad](https://mobeigi.com/blog/security/security-through-obscurity-is-not-bad/) ⭐️ 8.0/10

A blog post challenges the conventional wisdom by arguing that security through obscurity has its place and is not inherently bad, sparking a large Hacker News discussion. This perspective challenges a widely accepted security tenet, prompting a reevaluation of defense-in-depth strategies and highlighting the importance of nuanced, context-dependent approaches to security. The article distinguishes 'security only through obscurity' from using obscurity as an additional layer, and the community discusses its limited value against determined attackers and the impact of LLMs.

hackernews · mobeigi · May 3, 14:49

**Background**: Security through obscurity is a strategy that relies on keeping system details secret, contrary to Kerckhoffs's principle, which holds that security should depend only on the secrecy of keys. The principle is often paraphrased as 'the enemy knows the system,' emphasizing that obscurity should not be a primary defense. However, in practice, obscurity can add an extra layer of protection when used alongside strong security measures.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Kerckhoffs's_principle">Kerckhoffs's principle</a></li>

</ul>
</details>

**Discussion**: The community largely agrees that obscurity can be a useful layer but warns against relying on it solely. Some point out that Kerckhoffs's principle is often misapplied, while others emphasize that minimizing data collection is more effective. Concerns are raised about LLMs making obscurity less effective.

**Tags**: `#security`, `#obscurity`, `#best-practices`, `#debate`, `#kerckhoffs-principle`

---

<a id="item-6"></a>
## [Local LLM Speed Soars from 1 to 100 tk/s in 2 Years](https://www.reddit.com/r/LocalLLaMA/comments/1t2s7ik/what_a_time_to_be_alive_from_1tksec_to_20100tksec/) ⭐️ 8.0/10

Two years ago, running a quantized dense model like Llama 405B at ~1.2 tokens/second was impressive; now, Mixture of Experts (MoE) architectures enable huge state-of-the-art models like Qwen 3.5 397B to achieve 30–100 tokens/second on the same hardware. This leap democratizes access to cutting-edge AI, allowing individuals to run AGI-class models locally at practical speeds without costly infrastructure. The gains stem primarily from MoE's sparse activation rather than dense computation; improvements in attention (e.g., hybrid Mamba, DSA) also boost context length handling. Dense LLaMA 405B sees only modest speed gains via tensor parallelism and RAM offloading, and quantization (q4_k_m) remains essential for fitting models into consumer GPUs.

reddit · r/LocalLLaMA · segmond · May 3, 17:46

**Background**: Mixture of Experts (MoE) uses multiple specialized sub-models, activating only a few per token to cut computation. Quantization compresses model weights to lower precision (e.g., 4-bit) to reduce memory with minimal accuracy loss, enabling huge models on limited hardware. Dense models process all parameters for every token, making them slower. The local LLM community runs large models on personal devices via techniques like GPU offloading and tensor parallelism.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/@paul.ilvez/demystifying-llm-quantization-suffixes-what-q4-k-m-q8-0-and-q6-k-really-mean-0ec2770f17d3">Demystifying LLM Quantization Suffixes: What... | Medium</a></li>
<li><a href="https://arxiv.org/abs/2507.11181">[2507.11181] Mixture of Experts in Large Language Models</a></li>

</ul>
</details>

**Discussion**: Commenters note the speedup mainly comes from the dense-to-MoE shift, not hardware gains; dense LLaMA 405B remains just as slow. Some question the 'super AGI' claim, while others discuss hardware specifics (e.g., a used RTX 3090 for $900+ to run qwen3.6-36b at 50 tk/s). Overall, excitement is tempered by realism about architectural differences.

**Tags**: `#local LLM`, `#Mixture of Experts`, `#inference performance`, `#hardware acceleration`, `#model optimization`

---