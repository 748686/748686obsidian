---
layout: default
title: "Horizon Summary: 2026-04-29 (EN)"
date: 2026-04-29
lang: en
---

> From 55 items, 31 important content pieces were selected

---

1. [Critical GitHub RCE Vulnerability CVE-2026-3854 Disclosed](#item-1) ⭐️ 9.0/10
2. [Talkie: 13B Vintage Language Model Trained on Pre-1931 Text](#item-2) ⭐️ 9.0/10
3. [Ghostty Leaves GitHub Due to Platform Decline](#item-3) ⭐️ 8.0/10
4. [Reflecting on GitHub's Transformation of Open Source](#item-4) ⭐️ 8.0/10
5. [OpenAI Models to Launch on Amazon Bedrock](#item-5) ⭐️ 8.0/10
6. [Google's Silent Update Threatens Android Openness](#item-6) ⭐️ 8.0/10
7. [Who owns code written by Claude Code?](#item-7) ⭐️ 8.0/10
8. [UAE announces departure from OPEC](#item-8) ⭐️ 8.0/10
9. [GitHub Actions Supply Chain Risk Exposed](#item-9) ⭐️ 8.0/10
10. [AISLE Discovers 38 CVEs in OpenEMR Healthcare Software](#item-10) ⭐️ 8.0/10
11. [Pip 26.1 introduces lockfiles and dependency cooldowns](#item-11) ⭐️ 8.0/10
12. [Fedora Linux 44 Released with GNOME 50 and Apple Silicon Support](#item-12) ⭐️ 8.0/10
13. [NVIDIA Releases Nemotron-3-Nano-Omni-30B-A3B-Reasoning](#item-13) ⭐️ 8.0/10
14. [User Abandons Local LLMs for Coding, Cites Poor Decision-Making](#item-14) ⭐️ 8.0/10
15. [EU Launches Two DMA Proceedings Against Google](#item-15) ⭐️ 8.0/10
16. [China Blocks Foreign Acquisition of Manus AI Project](#item-16) ⭐️ 8.0/10
17. [Google Signs Classified AI Deal with Pentagon](#item-17) ⭐️ 8.0/10
18. [Qwen Open-Sources FlashQLA: 2-3x Faster Linear Attention Kernels](#item-18) ⭐️ 8.0/10
19. [LiteLLM SQL Injection Leaks API Keys Without Auth](#item-19) ⭐️ 8.0/10
20. [LocalSend: Open-source cross-platform AirDrop alternative](#item-20) ⭐️ 7.0/10
21. [Waymo Launches Autonomous Ride-Hailing in Portland](#item-21) ⭐️ 7.0/10
22. [Claude.ai and API suffer major outage, sparking reliability debate](#item-22) ⭐️ 7.0/10
23. [GitHub Pledges Availability Focus After Poor Uptime](#item-23) ⭐️ 7.0/10
24. [Live Sun and Moon Dashboard Using NASA Footage](#item-24) ⭐️ 7.0/10
25. [Interactive Tool Visualizes Neural Network Loss Landscapes](#item-25) ⭐️ 7.0/10
26. [Qwen 3.6 27B Quantization Benchmark: Q4_K_M Best Tradeoff](#item-26) ⭐️ 7.0/10
27. [DeepSeek Vision Development Sparks Community Excitement](#item-27) ⭐️ 7.0/10
28. [Anthropic's Project Deal: AI Agents Trade in Real Marketplace](#item-28) ⭐️ 7.0/10
29. [China Adds 38 New Undergraduate Majors Including Embodied Intelligence](#item-29) ⭐️ 7.0/10
30. [China penalizes Jianying, Jimeng AI for improper AI content labeling](#item-30) ⭐️ 7.0/10
31. [Warp Open-Sources Client Codebase with GPT-Powered Agent Workflows](#item-31) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Critical GitHub RCE Vulnerability CVE-2026-3854 Disclosed](https://www.wiz.io/blog/github-rce-vulnerability-cve-2026-3854) ⭐️ 9.0/10

Wiz Research disclosed a critical remote code execution (RCE) vulnerability, CVE-2026-3854 (CVSS 8.7), affecting GitHub.com and GitHub Enterprise Server, which allows an authenticated attacker to achieve RCE with a single git push command. This vulnerability is critical because 88% of on-premises GitHub Enterprise Server instances remain unpatched seven weeks after a fix was released, leaving a vast number of organizations at risk of full compromise. The flaw resides in GitHub's internal git infrastructure and can be triggered by an authenticated user pushing a specially crafted repository. The fix is available in GHES version 3.19.3 and later.

hackernews · bo0tzz · Apr 28, 16:15

**Background**: GitHub Enterprise Server (GHES) is the self-hosted version of GitHub used by organizations that require on-premises code hosting. Remote code execution (RCE) vulnerabilities allow attackers to run arbitrary commands on a server, potentially leading to full system compromise. The Wiz research team used AI-augmented reverse engineering to discover this flaw.

<details><summary>References</summary>
<ul>
<li><a href="https://www.wiz.io/blog/github-rce-vulnerability-cve-2026-3854">GitHub RCE Vulnerability: CVE-2026-3854 Breakdown | Wiz Blog</a></li>
<li><a href="https://thehackernews.com/2026/04/researchers-discover-critical-github.html">Researchers Discover Critical GitHub CVE-2026-3854 RCE Flaw ...</a></li>
<li><a href="https://thecodersblog.com/unpacking-cve-2026-3854-a-critical-rce-vulnerabili">CVE-2026-3854 Breakdown: A Critical RCE Vulnerability Strikes ...</a></li>

</ul>
</details>

**Discussion**: The community praised Wiz's work and highlighted the effectiveness of AI-augmented reverse engineering in vulnerability research. Commenters expressed concern over the high percentage of unpatched instances and debated the challenges of replacing GitHub with alternative platforms.

**Tags**: `#security`, `#vulnerability`, `#github`, `#RCE`, `#AI-assisted reversing`

---

<a id="item-2"></a>
## [Talkie: 13B Vintage Language Model Trained on Pre-1931 Text](https://simonwillison.net/2026/Apr/28/talkie/#atom-everything) ⭐️ 9.0/10

Researchers Nick Levine, David Duvenaud, and Alec Radford released talkie-1930-13b, a 13-billion-parameter language model trained exclusively on 260B tokens of pre-1931 English text, along with an instruction-tuned chat version, both under Apache 2.0 license. This model introduces a novel 'vintage language model' concept with a hard historical knowledge cutoff, enabling research into how well LLMs can predict future events, invent post-cutoff discoveries, or learn programming without modern data. The involvement of Alec Radford and the open-source license amplify its impact on AI research and historical NLP. The base model was trained on 260B tokens of pre-1931 English text, and the instruction-tuned model used a novel dataset of instruction-response pairs extracted from pre-1931 reference works, with further refinement using Claude Sonnet 4.6 as a judge and synthetic multi-turn chats from Claude Opus 4.6. The project also addresses contamination challenges from post-1931 text and modern LLM assistance.

rss · Simon Willison · Apr 28, 02:47

**Background**: Large language models (LLMs) are typically trained on vast internet data with no fixed historical cutoff, making it hard to study their generalization abilities. A 'vintage language model' like talkie has a hard knowledge cutoff at a specific historical date (1931), allowing researchers to probe how well the model can reason about events after its training data. The Apache 2.0 license permits free use, modification, and distribution.

<details><summary>References</summary>
<ul>
<li><a href="https://simonwillison.net/2026/Apr/28/talkie/">Introducing talkie: a 13B vintage language model from 1930</a></li>
<li><a href="https://huggingface.co/collections/talkie-lm/talkie-13b">talkie-13b - a talkie-lm Collection - Hugging Face</a></li>
<li><a href="https://github.com/talkie-lm/talkie">talkie - a 13B vintage language model from 1930 - GitHub</a></li>

</ul>
</details>

**Discussion**: Simon Willison praised the release, highlighting its potential for 'vegan models' trained on out-of-copyright data, but noted that the chat model's fine-tuning relied on non-vegan LLMs (Claude) for synthetic data, which may introduce anachronistic knowledge. He also expressed hope that the training data would be released.

**Tags**: `#language model`, `#historical NLP`, `#open source`, `#AI research`, `#NLP`

---

<a id="item-3"></a>
## [Ghostty Leaves GitHub Due to Platform Decline](https://mitchellh.com/writing/ghostty-leaving-github) ⭐️ 8.0/10

Mitchell Hashimoto announced that his terminal emulator project Ghostty is leaving GitHub, citing emotional attachment and disappointment with GitHub's decline under Microsoft. This move highlights growing developer dissatisfaction with GitHub's platform degradation and Microsoft's influence, potentially triggering more project migrations and discussions about open-source platform ethics. Hashimoto described crying while writing the blog post, emphasizing his deep emotional connection to GitHub. The decision follows months of discussion and reflects broader community concerns about GitHub's reliability and direction.

hackernews · WadeGrimridge · Apr 28, 19:44

**Background**: GitHub, acquired by Microsoft in 2018, is the dominant platform for open-source code hosting. Mitchell Hashimoto is the co-founder of HashiCorp and creator of Ghostty, a GPU-accelerated terminal emulator. His departure from GitHub signals a notable shift in developer trust.

<details><summary>References</summary>
<ul>
<li><a href="https://ghostty.org/">Ghostty</a></li>
<li><a href="https://en.wikipedia.org/wiki/HashiCorp">HashiCorp - Wikipedia</a></li>

</ul>
</details>

**Discussion**: Community comments express empathy with Hashimoto's emotional struggle and share observations of GitHub's decline, with some suggesting that non-free software is inherently suspect. Others propose that GitHub should hire Hashimoto as CEO to turn things around.

**Tags**: `#GitHub`, `#open-source`, `#platform migration`, `#developer experience`, `#Microsoft`

---

<a id="item-4"></a>
## [Reflecting on GitHub's Transformation of Open Source](https://lucumr.pocoo.org/2026/4/28/before-github/) ⭐️ 8.0/10

A retrospective blog post by Armin Ronacher examines how GitHub shifted open source focus from projects to individuals, while also critiquing centralization and archival practices. This reflection highlights GitHub's profound cultural impact on open source, sparking ongoing debates about centralization versus decentralization and the preservation of software heritage. The post notes that GitHub made it easy to create repositories tied to individuals rather than formal projects, and argues that its role as a central archive may atrophy collective archival skills.

hackernews · mlex · Apr 28, 21:17

**Background**: GitHub, launched in 2008, became the dominant platform for hosting Git repositories, introducing social features like profiles and forks that emphasized individual contributors. Before GitHub, platforms like SourceForge required more formal project setup. The post reflects on how this shift changed open source culture.

**Discussion**: Comments debate the merits of Git versus Fossil, with one user lamenting Git's dominance despite Fossil's integrated tools. Another commenter argues that GitHub's centralization is harmful because it atrophies collective archival skills, advocating for decentralized forges with federation.

**Tags**: `#GitHub`, `#open source`, `#version control`, `#community`, `#archival`

---

<a id="item-5"></a>
## [OpenAI Models to Launch on Amazon Bedrock](https://stratechery.com/2026/an-interview-with-openai-ceo-sam-altman-and-aws-ceo-matt-garman-about-bedrock-managed-agents/) ⭐️ 8.0/10

OpenAI has announced a partnership with AWS to make its models, including GPT-4o and Codex, available through Amazon Bedrock, a fully managed service for building generative AI applications. The collaboration also introduces Amazon Bedrock Managed Agents powered by OpenAI. This move significantly expands OpenAI's enterprise reach by leveraging AWS's vast customer base and trusted infrastructure, especially in regulated industries. It also intensifies competition with Anthropic, whose models are already available on Bedrock, and challenges Microsoft's exclusive position as OpenAI's primary cloud partner. OpenAI models on Bedrock will be accessible via a unified API, with options for customization and security controls. The partnership includes both OpenAI's proprietary models and open-weight models, though exact pricing and availability dates have not been disclosed.

hackernews · translocator · Apr 28, 19:24

**Background**: Amazon Bedrock is a fully managed service launched in 2023 that provides access to foundation models from multiple AI companies via a single API. It competes with Microsoft Azure AI Foundry and Google Cloud's Vertex AI. Previously, OpenAI models were primarily available through Microsoft Azure, limiting enterprise adoption for organizations with existing AWS commitments.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Amazon_Bedrock">Amazon Bedrock</a></li>
<li><a href="https://openai.com/index/openai-on-aws/">OpenAI models , Codex, and Managed Agents come to AWS | OpenAI</a></li>
<li><a href="https://www.aboutamazon.com/news/aws/openai-models-amazon-bedrock-sagemaker">OpenAI 's open weight models now available on AWS</a></li>

</ul>
</details>

**Discussion**: Community comments highlight that OpenAI's absence from Bedrock previously drove enterprises toward Anthropic's Claude due to trust and privacy concerns. Some users note that inference results may vary across platforms due to optimizations, adding non-determinism. Others speculate this move is a direct response to losing enterprise ground to Anthropic and Microsoft's evolving relationship.

**Tags**: `#OpenAI`, `#AWS`, `#Bedrock`, `#Enterprise AI`, `#Cloud Computing`

---

<a id="item-6"></a>
## [Google's Silent Update Threatens Android Openness](https://keepandroidopen.org/en/) ⭐️ 8.0/10

Starting September 2026, Google will require all Android apps to be registered by verified developers, blocking unapproved apps from being installed on certified devices, with a mandatory 24-hour waiting period for sideloading. This change undermines Android's core promise of openness, potentially turning it into a walled garden like iOS, and could harm users who rely on sideloading for freedom, privacy, or regional app access. The policy applies to all certified Android devices globally with no opt-out, though an 'advanced flow' exists for developers. Users who disable Developer Options must re-enable them to turn off the new sideloading restrictions.

hackernews · doener · Apr 28, 15:21

**Background**: Android has long been distinguished from iOS by allowing users to install apps from outside the official Google Play Store, a practice known as sideloading. This openness has been a key reason many users chose Android over iPhone. Google's new restrictions aim to combat scams and coercion but are seen by critics as a step toward vendor lock-in.

<details><summary>References</summary>
<ul>
<li><a href="https://www.androidauthority.com/google-android-sideloading-unverified-apps-new-rules-3650343/">Android's new sideloading rules are here, and they come with a 24-hour lock!</a></li>
<li><a href="https://lwn.net/Articles/1034989/">New restrictions on Android app sideloading [LWN.net]</a></li>
<li><a href="https://android.gadgethacks.com/news/android-sideloading-restrictions-explained-why-even-supporters-object/">Android Sideloading Restrictions Explained: Why Even Supporters Object << Android :: Gadget Hacks</a></li>

</ul>
</details>

**Discussion**: Community comments are sharply divided: some users feel betrayed, arguing that Android's openness was its only advantage over iOS, while others point out that the restrictions are not as absolute as claimed, with opt-out flows available. A common concern is that this sets a precedent for further lock-down, reducing user choice.

**Tags**: `#Android`, `#Google`, `#open source`, `#vendor lock-in`, `#mobile ecosystem`

---

<a id="item-7"></a>
## [Who owns code written by Claude Code?](https://legallayer.substack.com/p/who-owns-the-claude-code-wrote) ⭐️ 8.0/10

A Substack article explores the unresolved copyright and ownership questions surrounding code generated by Anthropic's AI coding agent, Claude Code, highlighting legal ambiguities and implications for open source software. This issue matters because AI-generated code is increasingly used in software development, and the lack of clear copyright ownership could affect open source licensing, developer rights, and legal liability for both individuals and companies. The US Copyright Office has stated that works predominantly generated by AI without meaningful human authorship are not eligible for copyright protection, but this rule is not yet settled nationwide. The EU AI Act also requires disclosure of AI-generated content, adding another layer of complexity.

hackernews · senaevren · Apr 28, 11:24

**Background**: Claude Code is an AI coding agent developed by Anthropic that can explore codebases, answer questions, and make changes. Copyright law traditionally protects original works of human authorship, but AI-generated content challenges this framework, leading to ongoing legal debates about ownership and infringement.

<details><summary>References</summary>
<ul>
<li><a href="https://www.geeky-gadgets.com/ai-generated-content-copyright-guidelines/">Understanding Copyright Rules for AI-Generated Content - Geeky</a></li>
<li><a href="https://thebarristergroup.co.uk/blog/ai-generated-content-and-copyright-evolving-legal-boundaries-in-english-law">AI-Generated Content and Copyright: Evolving Legal Boundaries</a></li>

</ul>
</details>

**Discussion**: Community comments on Hacker News reveal diverse viewpoints: some argue that the human directing the agent should own the copyright, while others worry about copyright 'washing' of stolen IP. There is also skepticism that courts will ultimately favor corporate interests over developers.

**Tags**: `#AI`, `#copyright`, `#open source`, `#legal`, `#software engineering`

---

<a id="item-8"></a>
## [UAE announces departure from OPEC](https://www.ft.com/content/8c354f2d-3e66-47f1-aad4-9b4aa30e386d) ⭐️ 8.0/10

The United Arab Emirates has announced its decision to leave OPEC, effective immediately, marking a historic split from the oil cartel after decades of membership. This move could significantly weaken OPEC's influence over global oil prices and reshape Middle Eastern geopolitical alliances, particularly as the UAE aligns more closely with Israel and the US. The departure comes amid strained Saudi-Emirati relations and follows the UAE's request for Pakistan to repay a $3.5 billion loan early, highlighting a broader realignment in the region.

hackernews · bazzmt · Apr 28, 13:02

**Background**: OPEC, the Organization of the Petroleum Exporting Countries, is a cartel of oil-producing nations that coordinates production levels to influence prices. The UAE has been a member since 1967 and is one of its largest producers. Internal disagreements over production quotas and strategic direction have been growing, particularly between the UAE and Saudi Arabia.

**Discussion**: Commenters noted the geopolitical context, including an emerging Emirati-Israeli axis to counter Saudi and Iranian influence, and the historical tendency of OPEC members to cheat on quotas. Some saw this as a major crack in OPEC's power, potentially leading to a shift in global oil market dynamics.

**Tags**: `#OPEC`, `#geopolitics`, `#oil`, `#UAE`, `#energy`

---

<a id="item-9"></a>
## [GitHub Actions Supply Chain Risk Exposed](https://nesbitt.io/2026/04/28/github-actions-is-the-weakest-link.html) ⭐️ 8.0/10

A blog post by nesbitt.io highlights that GitHub Actions' reliance on mutable tags for third-party actions introduces significant supply-chain security risks, advocating for using commit hashes instead or switching to more secure CI platforms. This matters because GitHub Actions is widely used in CI/CD pipelines, and a compromised third-party action could inject malicious code into thousands of projects, affecting the entire software supply chain. Tags in Git can be moved to point to different commits, allowing an attacker to replace a legitimate action with a malicious version without changing the tag reference. Using commit hashes (SHA) ensures immutability and precise version control.

hackernews · dochtman · Apr 28, 11:58

**Background**: GitHub Actions allows workflows to reference third-party actions via tags (e.g., v1) or commit hashes. Tags are mutable and can be updated, while commit hashes are immutable and uniquely identify a specific version. Recent supply-chain attacks on GitHub Actions have demonstrated the real-world risk of mutable tag references.

<details><summary>References</summary>
<ul>
<li><a href="https://www.techtarget.com/searchitoperations/news/366621078/GitHub-Actions-supply-chain-attack-spotlights-CI-CD-risks">GitHub Actions supply chain attack spotlights CI/CD risks |</a></li>
<li><a href="https://socket.dev/blog/github-actions-supply-chain-attack-puts-thousands-of-projects-at-risk">GitHub Actions Supply Chain Attack Puts Thousands of Project...</a></li>

</ul>
</details>

**Discussion**: Commenters largely agree with the article's premise, with some noting they have always used commit hashes for third-party actions. Others discuss alternative CI platforms like Dagger and Blacksmith, and tools like ratchet for pinning actions to hashes.

**Tags**: `#security`, `#CI/CD`, `#GitHub Actions`, `#supply chain`, `#DevOps`

---

<a id="item-10"></a>
## [AISLE Discovers 38 CVEs in OpenEMR Healthcare Software](https://aisle.com/blog/aisle-discovers-38-critical-security-vulnerabilities-in-healthcare-software-used-by-100000-providers) ⭐️ 8.0/10

AISLE, a security vendor, disclosed 38 Common Vulnerabilities and Exposures (CVEs) in OpenEMR, a widely-used open-source electronic health records system, including SQL injection and cross-site scripting (XSS) flaws. These vulnerabilities could compromise sensitive patient data for over 100,000 healthcare providers, highlighting systemic security weaknesses in healthcare software and the potential role of AI-driven security scanners. All 38 vulnerabilities are common types such as SQL injection, XSS, path traversal, and insecure direct object references, suggesting basic security oversights. The discovery was made using an AI-powered security scanner.

hackernews · mmsc · Apr 28, 16:06

**Background**: OpenEMR is a free, open-source electronic health records (EHR) and medical practice management software written in PHP, used by over 100,000 healthcare providers worldwide. SQL injection and XSS are well-known web security vulnerabilities that can allow attackers to access or manipulate sensitive data. The discovery by AISLE underscores ongoing challenges in securing legacy open-source healthcare applications.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/OpenEMR">OpenEMR</a></li>
<li><a href="https://en.wikipedia.org/wiki/SQL_injection">SQL injection</a></li>
<li><a href="https://en.wikipedia.org/wiki/XSS">XSS</a></li>

</ul>
</details>

**Discussion**: Community comments note that these are low-hanging fruit vulnerabilities, with one commenter having found similar issues 16 years ago. Some see this as a marketing-driven disclosure but acknowledge the value of AI scanners, while others argue that proper prioritization could have fixed these issues without AI.

**Tags**: `#security`, `#vulnerabilities`, `#healthcare`, `#open source`, `#AI`

---

<a id="item-11"></a>
## [Pip 26.1 introduces lockfiles and dependency cooldowns](https://simonwillison.net/2026/Apr/28/pip-261/#atom-everything) ⭐️ 8.0/10

Pip 26.1 adds support for lockfiles via the new `pip lock` command, which generates a `pylock.toml` file, and introduces dependency cooldowns through the `--uploaded-prior-to` option using ISO 8601 duration format. It also drops support for Python 3.9. Lockfiles improve reproducibility by pinning exact dependency versions, which is crucial for production deployments and collaborative projects. Dependency cooldowns help mitigate supply-chain attacks by preventing installations of very recently uploaded packages. The `pip lock` command writes all resolved dependencies to a `pylock.toml` file, which can be used with `pip install --lock` for reproducible installs. The `--uploaded-prior-to` option accepts values like `P4D` to require packages uploaded at least 4 days ago.

rss · Simon Willison · Apr 28, 05:23

**Background**: Pip is the default package installer for Python. Lockfiles have long been available in other tools like Pipenv and Poetry, but pip itself lacked native support until now. Dependency cooldowns are a security measure that reduces the window for malicious packages to be installed immediately after upload.

<details><summary>References</summary>
<ul>
<li><a href="https://ichard26.github.io/blog/2026/04/whats-new-in-pip-26.1/">What's new in pip 26.1 - lockfiles and dependency cooldowns! | Richard Si</a></li>
<li><a href="https://pip.pypa.io/en/stable/cli/pip_lock/">pip lock - pip documentation v26.0.1</a></li>
<li><a href="https://simonwillison.net/2026/Apr/28/pip-261/">What's new in pip 26.1 - lockfiles and dependency cooldowns!</a></li>

</ul>
</details>

**Tags**: `#pip`, `#Python`, `#dependency management`, `#lockfiles`

---

<a id="item-12"></a>
## [Fedora Linux 44 Released with GNOME 50 and Apple Silicon Support](https://lwn.net/Articles/1070198/) ⭐️ 8.0/10

Fedora Linux 44 has been released, featuring GNOME 50 for Workstation, KDE Plasma 6.6 for the KDE spin, and the Fedora Asahi Remix for Apple Silicon Macs. The release also includes updated Atomic Desktops and various desktop refinements. This release marks a significant milestone for Fedora, bringing the latest GNOME and KDE desktop environments to users, and extending official support to Apple Silicon Macs through the Asahi Remix. It demonstrates Fedora's commitment to cutting-edge software and broad hardware compatibility. Fedora Workstation 44 ships with GNOME 50, which includes accessibility improvements, color management, and remote desktop enhancements. The KDE Plasma Desktop 44 is based on Plasma 6.6, featuring a new Plasma Login Manager and simplified setup. Fedora Asahi Remix 44 retires vendored Mesa and virglrenderer packages.

rss · LWN.net · Apr 28, 14:33

**Background**: Fedora is a popular Linux distribution known for its rapid adoption of new technologies. GNOME and KDE are two major desktop environments for Linux. The Fedora Asahi Remix is a collaboration with the Asahi Linux project to bring Fedora to Apple Silicon Macs. Atomic Desktops are immutable variants of Fedora, such as Silverblue and Kinoite.

<details><summary>References</summary>
<ul>
<li><a href="https://fedoramagazine.org/fedora-asahi-remix-44-is-now-available/">Fedora Asahi Remix 44 is now available - Fedora Magazine</a></li>

</ul>
</details>

**Tags**: `#Fedora`, `#Linux`, `#GNOME`, `#KDE`, `#Apple Silicon`

---

<a id="item-13"></a>
## [NVIDIA Releases Nemotron-3-Nano-Omni-30B-A3B-Reasoning](https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning) ⭐️ 8.0/10

NVIDIA has released Nemotron-3-Nano-Omni-30B-A3B-Reasoning, an open multimodal model that accepts video, audio, image, and text inputs and produces text output, with 30 billion total parameters and 3 billion active parameters per token. This model brings enterprise-grade multimodal reasoning to local deployment, enabling agents to perceive and reason across modalities in a single inference loop, which is significant for building complex AI agent systems. The model uses a hybrid MoE architecture combining Mamba layers and Transformer layers, supports a 100K token context window, and is available in BF16, FP8, and GGUF formats for flexible deployment.

reddit · r/LocalLLaMA · Altruistic_Heat_9531 · Apr 28, 16:12

**Background**: Nemotron-3-Nano-Omni is part of NVIDIA's Nemotron family of open models designed for multimodal agentic workloads. The A3B designation indicates a 30B total parameter model with 3B active parameters per token, using a sparse mixture-of-experts approach to balance performance and efficiency.

<details><summary>References</summary>
<ul>
<li><a href="https://build.nvidia.com/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning/modelcard">nemotron-3-nano-omni-30b-a3b-reasoning Model by NVIDIA ...</a></li>
<li><a href="https://unsloth.ai/docs/models/nemotron-3-nano-omni">NVIDIA Nemotron 3 Nano Omni - How To Run Locally | Unsloth ...</a></li>
<li><a href="https://openrouter.ai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning/api">NVIDIA: Nemotron 3 Nano Omni – API Quickstart | OpenRouter</a></li>

</ul>
</details>

**Discussion**: The community is excited about the release, with comments expressing enthusiasm and humor. Some users are asking about local inference support for video input beyond the first frame, and others are comparing it to models like Qwen 35B for coding tasks.

**Tags**: `#multimodal`, `#NVIDIA`, `#Nemotron`, `#reasoning`, `#local-LLM`

---

<a id="item-14"></a>
## [User Abandons Local LLMs for Coding, Cites Poor Decision-Making](https://www.reddit.com/r/LocalLLaMA/comments/1sxqa2c/im_done_with_using_local_llms_for_coding/) ⭐️ 8.0/10

A Reddit user reported that after weeks of testing local LLMs like Qwen 27B and Gemma 31B for coding tasks, they concluded these models are not yet competitive with Claude Code in productivity, citing poor decision-making and tool-calling issues. This post provides a realistic counterpoint to the hype around local LLMs for coding, highlighting that even the best local models under 100B parameters still lag behind cloud-based models like Claude in complex, multi-step tasks. The user specifically mentioned issues with Dockerization tasks, where the local model would incorrectly assume failure due to timeouts or hallucinate error causes instead of checking actual process status.

reddit · r/LocalLLaMA · dtdisapointingresult · Apr 28, 03:50

**Background**: Local LLMs are language models that run on the user's own hardware, offering privacy and offline use but limited by available compute. Qwen 27B and Gemma 31B are among the most capable local models under 100B parameters, while Claude Code is Anthropic's agentic coding tool that runs on cloud infrastructure.

<details><summary>References</summary>
<ul>
<li><a href="https://qwenlm.github.io/blog/qwen2.5-llm/">Qwen2.5-LLM: Extending the boundary of LLMs | Qwen</a></li>
<li><a href="https://lmstudio.ai/models/google/gemma-4-31b">google/gemma-4-31b • LM Studio</a></li>
<li><a href="https://claude.com/product/claude-code">Claude Code by Anthropic | AI Coding Agent, Terminal, IDE</a></li>

</ul>
</details>

**Discussion**: The community largely agreed with the user's assessment, with many sharing similar experiences. Some commenters noted that harness configuration can significantly impact performance, while others pointed out that a single consumer GPU cannot match cloud models like Claude.

**Tags**: `#local LLMs`, `#coding`, `#productivity`, `#Claude`, `#LLM comparison`

---

<a id="item-15"></a>
## [EU Launches Two DMA Proceedings Against Google](https://t.me/zaihuapd/41099) ⭐️ 8.0/10

On January 27, the European Commission initiated two formal proceedings under the Digital Markets Act (DMA) against Google, requiring it to open its Gemini AI interface and share search data with third parties. This marks a major enforcement action under the DMA, potentially reshaping competition in AI and search markets by forcing Google to provide equal access to its core platform capabilities. The first proceeding targets interoperability, requiring Google to let third-party AI services access Android's hardware and software features on par with Gemini. The second focuses on search data sharing under FRAND (fair, reasonable, and non-discriminatory) terms, covering anonymized ranking, query, click, and display data.

telegram · zaihuapd · Apr 28, 01:31

**Background**: The Digital Markets Act (DMA) is an EU regulation that designates large online platforms as 'gatekeepers' and imposes obligations to ensure fair competition, including interoperability and data access. FRAND principles, originally from standard-essential patent licensing, are now being applied to data access under the DMA to prevent anti-competitive behavior.

<details><summary>References</summary>
<ul>
<li><a href="https://zh.wikipedia.org/zh-hans/數位市場法案">数位市场法案 - 维基百科，自由的百科全书</a></li>
<li><a href="https://baike.baidu.com/item/FRAND/4496552">FRAND - 百度百科</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/676302896">DMA解读：守门人的定位与职责 - 知乎</a></li>

</ul>
</details>

**Tags**: `#EU regulation`, `#Google`, `#DMA`, `#AI`, `#search data`

---

<a id="item-16"></a>
## [China Blocks Foreign Acquisition of Manus AI Project](https://t.me/zaihuapd/41102) ⭐️ 8.0/10

China's National Development and Reform Commission (NDRC) has prohibited a foreign acquisition of the Manus project, requiring the parties to withdraw the deal. The decision was made by the Foreign Investment Security Review Office under the NDRC. This marks a significant government intervention in a high-profile AI acquisition, reflecting China's tightening national security scrutiny over foreign investments in advanced technology. The decision could impact cross-border tech M&A and signal stricter regulatory controls. The Manus project is reportedly the world's first fully autonomous AI agent, developed by Chinese startup Monica. The acquisition was reportedly valued at $2 billion and involved Meta Platforms, though the NDRC statement did not name the acquirer.

telegram · zaihuapd · Apr 28, 03:43

**Background**: China's Foreign Investment Security Review mechanism allows the government to block foreign acquisitions that threaten national security. The Manus project is an advanced AI agent capable of autonomous task execution, which falls under sensitive technology categories. This review process has been increasingly used to protect domestic tech assets.

<details><summary>References</summary>
<ul>
<li><a href="https://www.theguardian.com/world/2026/apr/27/china-blocks-meta-takeover-manus-ai-agent-developer">China blocks $2bn Meta takeover of AI agent developer Manus | China</a></li>
<li><a href="https://www.yicai.com/brief/103154622.html">外商投资安全审查工作机制办公室（国家发展改革委） 对外资收购Manus项目作出安全审查决定</a></li>
<li><a href="https://www.nbd.com.cn/articles/2026-04-27/4363048.html">外商投资安全审查工作机制办公室（国家发展改革委）对外资收购Manus项目作出安全审查决定 | 每经网</a></li>

</ul>
</details>

**Tags**: `#national security`, `#foreign investment`, `#regulation`, `#tech policy`, `#China`

---

<a id="item-17"></a>
## [Google Signs Classified AI Deal with Pentagon](https://www.theinformation.com/articles/google-signs-classified-ai-deal-pentagon-amid-employee-opposition) ⭐️ 8.0/10

Google has signed a classified agreement with the U.S. Department of Defense to provide its AI models for sensitive military applications, including mission planning and weapons targeting, under contracts worth up to $200 million each. This marks a significant shift from Google's 2018 decision to withdraw from Project Maven after employee protests, and it sets a precedent for how major AI companies engage with military clients amid ongoing ethical debates. The agreement prohibits use for mass domestic surveillance or autonomous weapons without human oversight, but Google does not have veto power over lawful government operational decisions. Anthropic was previously labeled a supply chain risk for refusing similar restrictions.

telegram · zaihuapd · Apr 28, 11:47

**Background**: Project Maven was a 2017 Pentagon initiative to accelerate AI adoption in military intelligence, which sparked massive employee protests at Google in 2018, leading Google to not renew the contract. Since then, the Pentagon has pursued AI contracts with multiple companies, including OpenAI and Anthropic, while facing ethical pushback from some firms.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Project_Maven">Project Maven - Wikipedia</a></li>
<li><a href="https://www.wired.com/story/3-years-maven-uproar-google-warms-pentagon/">3 Years After the Project Maven Uproar, Google Cozies to the ...</a></li>
<li><a href="https://www.vice.com/en/article/google-project-maven-protest-letter-killer-ai/">Over 3,000 Google Employees Signed a Letter Demanding Google ...</a></li>

</ul>
</details>

**Tags**: `#AI ethics`, `#military AI`, `#Google`, `#US Department of Defense`, `#technology policy`

---

<a id="item-18"></a>
## [Qwen Open-Sources FlashQLA: 2-3x Faster Linear Attention Kernels](https://qwen.ai/blog?id=flashqla) ⭐️ 8.0/10

Qwen team open-sourced FlashQLA, a high-performance linear attention kernel library built on TileLang for Gated Delta Networks, achieving 2-3x speedup on forward pass and 2x on backward pass on NVIDIA Hopper GPUs. This release significantly accelerates linear attention models, making them more practical for long-sequence pretraining and on-device agent inference, potentially reducing costs and latency in AI applications. FlashQLA leverages operator fusion and algebraic optimization, and introduces automatic intra-card context parallelism using gated decay properties, along with warpgroup-specialized kernels to overlap computation and data movement.

telegram · zaihuapd · Apr 28, 14:11

**Background**: Linear attention mechanisms like Gated Delta Networks (GDN) aim to reduce the quadratic complexity of standard attention, enabling efficient processing of long sequences. FlashQLA is built on TileLang, a tiled programming model that decouples dataflow and scheduling for efficient AI kernel programming.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/QwenLM/FlashQLA">QwenLM/ FlashQLA : high-performance linear attention kernel library...</a></li>
<li><a href="https://tilelang.com/">TileLang 0.1.9 documentation</a></li>
<li><a href="https://arxiv.org/abs/2412.06464">[2412.06464] Gated Delta Networks: Improving Mamba2 with Delta</a></li>

</ul>
</details>

**Tags**: `#AI/ML`, `#open-source`, `#attention mechanism`, `#GPU optimization`, `#Qwen`

---

<a id="item-19"></a>
## [LiteLLM SQL Injection Leaks API Keys Without Auth](https://mp.weixin.qq.com/s/ytNWdqGECo0fmWwPQGqy8A) ⭐️ 8.0/10

A critical SQL injection vulnerability (CVE-2026-42208) was discovered in LiteLLM Proxy, allowing unauthenticated attackers to extract API keys from the database by injecting malicious payloads via the Bearer token field. The flaw is actively exploited in the wild and has been fixed in version 1.83.7-stable. LiteLLM is widely used as a unified gateway for multiple LLM providers, and exposed instances are at high risk of credential theft. This vulnerability could lead to unauthorized use of expensive LLM APIs, data breaches, and financial loss for organizations. The attack exploits error logs generated during authentication failure; no valid credentials are required. Users are advised to upgrade immediately and rotate all stored API keys, or set disable_error_logs: true to mitigate the risk.

telegram · zaihuapd · Apr 28, 14:44

**Background**: LiteLLM is an open-source Python SDK and proxy server that provides an OpenAI-compatible interface to interact with over 100 LLM providers. The proxy component handles authentication and routing, storing API keys in a database. SQL injection occurs when user input is improperly sanitized, allowing an attacker to execute arbitrary SQL commands.

<details><summary>References</summary>
<ul>
<li><a href="https://securityonline.info/litellm-sql-injection-exploited-in-the-wild-cve-2026-42208/">Critical LiteLLM SQL Injection (CVE-2026-42208) Exploited in</a></li>
<li><a href="https://docs.litellm.ai/docs/providers/litellm_proxy">LiteLLM Proxy ( LLM Gateway) | liteLLM</a></li>
<li><a href="https://github.com/BerriAI/litellm">GitHub - BerriAI/ litellm : Python SDK, Proxy Server (AI Gateway) to...</a></li>

</ul>
</details>

**Discussion**: The security community has expressed concern over the active exploitation of this vulnerability, with many urging immediate patching. Some users noted that disabling error logs is a temporary workaround but not a complete fix.

**Tags**: `#security`, `#vulnerability`, `#SQL injection`, `#LiteLLM`, `#API keys`

---

<a id="item-20"></a>
## [LocalSend: Open-source cross-platform AirDrop alternative](https://github.com/localsend/localsend) ⭐️ 7.0/10

LocalSend is a free, open-source, cross-platform file-sharing application that enables local file transfer without an internet connection, supporting Windows, macOS, Linux, Android, and iOS. It addresses the long-standing gap in cross-platform local file sharing, offering a privacy-focused, decentralized alternative to proprietary solutions like Apple's AirDrop, which is limited to Apple devices. LocalSend uses the local network (LAN) for transfers, meaning devices must be on the same network; it does not create its own ad-hoc network like AirDrop. The app is built with Flutter, which leads to larger installer sizes compared to Tauri-based alternatives.

hackernews · bilsbie · Apr 28, 11:54

**Background**: AirDrop is Apple's proprietary wireless file-sharing feature that uses Bluetooth and Wi-Fi to create a direct peer-to-peer connection between Apple devices. It is widely praised for its ease of use but is limited to the Apple ecosystem. Open-source alternatives like LocalSend aim to provide similar functionality across different operating systems, but often require devices to be on the same local network, which can be a limitation in scenarios without existing network infrastructure.

<details><summary>References</summary>
<ul>
<li><a href="https://localsend.org/">LocalSend: Share files to nearby devices</a></li>
<li><a href="https://grokipedia.com/page/localsend">LocalSend</a></li>
<li><a href="https://www.makeuseof.com/airdrop-alternatives-better-than-localsend/">3 open-source AirDrop alternatives that are better than ... - MUO</a></li>

</ul>
</details>

**Discussion**: Community comments highlight that LocalSend is reliable and works well, but note the limitation of requiring same-network connectivity, unlike AirDrop which creates its own network. Some users suggest alternatives like Sendme and AltSendme that use Iroh for peer-to-peer relay without network restrictions. A developer also points out that Tauri-based apps have significantly smaller installer sizes compared to Flutter-based LocalSend.

**Tags**: `#file-sharing`, `#open-source`, `#cross-platform`, `#networking`, `#flutter`

---

<a id="item-21"></a>
## [Waymo Launches Autonomous Ride-Hailing in Portland](https://waymo.com/blog/shorts/waymo-in-portland/) ⭐️ 7.0/10

Waymo has launched its fully autonomous ride-hailing service in Portland, Oregon, expanding its operations to a new city amid local transit budget cuts. This expansion highlights the growing tension between autonomous vehicle deployment and public transit funding, sparking debate on how AVs should complement or compete with public transportation. The launch coincides with TriMet, Portland's transit agency, facing a $300 million budget shortfall and cutting services. Waymo's geofenced approach uses LIDAR and detailed mapping, contrasting with Tesla's vision-only strategy.

hackernews · xnx · Apr 28, 18:08

**Background**: Waymo is the world's first autonomous ride-hailing service, operating in multiple U.S. cities. Autonomous vehicles use sensors and AI to navigate without human drivers, but their impact on public transit and urban mobility remains debated.

<details><summary>References</summary>
<ul>
<li><a href="https://waymo.com/">Waymo - Self-Driving Cars - Autonomous Vehicles - Ride-Hail</a></li>
<li><a href="https://waymo.com/rides/">Ride-Hailing App - Make the Most of Your Drive - Waymo</a></li>
<li><a href="https://www.nature.com/articles/s41599-025-05600-6">The public perception and adaptability of laws and ... - Nature</a></li>

</ul>
</details>

**Discussion**: Commenters note the irony of Waymo launching as TriMet cuts services, with some praising Waymo's LIDAR-first approach over Tesla's vision-only method. Others express concerns about AVs getting stuck on tram tracks in Portland's downtown.

**Tags**: `#autonomous vehicles`, `#Waymo`, `#public transit`, `#urban mobility`, `#self-driving cars`

---

<a id="item-22"></a>
## [Claude.ai and API suffer major outage, sparking reliability debate](https://status.claude.com/incidents/9l93x2ht4s5w) ⭐️ 7.0/10

Claude.ai and the Anthropic API experienced a significant outage, leaving users unable to access the platform or make API calls. This outage highlights the fragility of relying on a single LLM provider for critical workflows, especially as enterprises invest heavily in AI infrastructure. The outage affected both the web interface and API, with users reporting errors for several hours. Anthropic's status page indicated elevated error rates and degraded performance.

hackernews · shorsher · Apr 28, 18:01

**Background**: Anthropic is a leading AI company known for its Claude model series. Claude.ai is the consumer-facing chat interface, while the API serves developers and enterprises. Reliability is critical for production systems that depend on these services.

**Discussion**: Commenters expressed frustration over frequent outages, with one enterprise user reporting over $200k monthly spend and poor support. Others noted the importance of multi-model strategies to mitigate such risks.

**Tags**: `#AI`, `#outage`, `#reliability`, `#Anthropic`, `#infrastructure`

---

<a id="item-23"></a>
## [GitHub Pledges Availability Focus After Poor Uptime](https://github.blog/news-insights/company-news/an-update-on-github-availability/) ⭐️ 7.0/10

GitHub published an official update on availability, declaring that availability is now the top priority over capacity and new features, and that they are pursuing a multi-cloud strategy to improve reliability. This matters because GitHub is a critical platform for millions of developers, and its recent poor uptime has eroded trust. The shift to multi-cloud signals that even Microsoft-owned GitHub may not rely solely on Azure for reliability. The announcement includes an unlabeled graph showing large numbers but lacks detailed uptime metrics. GitHub also notes that agent-driven activity has put sudden pressure on the platform, contributing to stability issues.

hackernews · salkahfi · Apr 28, 10:05

**Background**: GitHub has experienced significant downtime and performance issues over the past year, leading to developer frustration. In 2023, GitHub prioritized migrating to Azure over feature development, but the new post suggests a multi-cloud approach to avoid single points of failure.

**Discussion**: The community is highly skeptical, with comments mocking the unlabeled graph and questioning the sincerity of the priorities. Some users report ongoing issues like incomplete pull request lists, and others interpret the multi-cloud move as an implicit admission of Azure's unreliability.

**Tags**: `#GitHub`, `#availability`, `#cloud`, `#reliability`, `#infrastructure`

---

<a id="item-24"></a>
## [Live Sun and Moon Dashboard Using NASA Footage](https://www.lumara-space.app/) ⭐️ 7.0/10

A developer launched Lumara Space, a live dashboard that displays real-time sun and moon imagery sourced from NASA's Scientific Visualization Studio, featuring a polished UI and cross-platform availability via web and iOS App Store. This dashboard makes high-quality NASA space imagery accessible to the public in an engaging, real-time format, potentially inspiring interest in space science and demonstrating creative use of public data. The app currently hotlinks large 2K resolution videos (up to 30MB each) directly from NASA servers, which may lead to performance issues and bandwidth concerns. Community feedback suggests optimizing content delivery and adding UI improvements like a close button.

hackernews · beeswaxpat · Apr 28, 13:25

**Background**: NASA's Scientific Visualization Studio (SVS) provides free, high-resolution imagery and videos of space phenomena. Hotlinking refers to directly embedding content from another server, which can consume the host's bandwidth without permission. The dashboard combines these assets into a unified, real-time display.

**Discussion**: The community praised the app's visual polish and novelty, with comments like 'super cool' and 'beautiful app.' However, several users raised technical concerns about hotlinking large NASA videos and suggested optimizations, such as caching or using lower-resolution streams. Feature requests included CME tracking and better navigation controls.

**Tags**: `#space`, `#dashboard`, `#NASA`, `#UI/UX`, `#web app`

---

<a id="item-25"></a>
## [Interactive Tool Visualizes Neural Network Loss Landscapes](https://www.reddit.com/gallery/1sy7f5r) ⭐️ 7.0/10

A new interactive browser tool visualizes neural network loss landscapes using filter-wise normalization from Li et al. (NeurIPS 2018), allowing users to explore how optimizers navigate the terrain. This tool helps researchers and practitioners build better intuition about loss landscape geometry and optimizer behavior, potentially improving model debugging and generalization analysis. The tool runs entirely client-side, supports architectures from simple MLPs to ResNet-8 and LeNet-5, and uses synthetic or real image datasets. A known limitation is that 2D/3D projections may create geometric surfaces not present in the true high-dimensional space.

reddit · r/MachineLearning · Hackerstreak · Apr 28, 17:04

**Background**: Loss landscapes of neural networks are high-dimensional and hard to visualize. Filter-wise normalization, proposed by Li et al. (NeurIPS 2018), removes scale effects to reveal true geometry. This tool applies that method to create interactive 3D plots.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/pdf/1712.09913">Visualizing the Loss Landscape of Neural Nets</a></li>
<li><a href="https://sh-tsang.medium.com/brief-review-visualizing-the-loss-landscape-of-neural-nets-dd93cb261afc">Brief Review — Visualizing the Loss Landscape of Neural... | Medium</a></li>
<li><a href="https://weary-travelers.gitlab.io/posts/outlines/Li_et_al_NeurIPS_2018/outline.html">Visualizing the Loss Landscape of Neural Nets</a></li>

</ul>
</details>

**Discussion**: A commenter with research experience suggests starting with ResNet vs feedforward at initialization, then batchnorm feedforward during training, to build understanding. The author provides a TL;DR covering dimensionality, scale invariance trap, and the interactive tool.

**Tags**: `#loss landscape`, `#neural networks`, `#visualization`, `#optimization`, `#deep learning`

---

<a id="item-26"></a>
## [Qwen 3.6 27B Quantization Benchmark: Q4_K_M Best Tradeoff](https://i.redd.it/ncwdmp21bxxg1.jpeg) ⭐️ 7.0/10

A benchmark evaluated Qwen 3.6 27B across BF16, Q4_K_M, and Q8_0 GGUF quantizations using llama-cpp-python on HumanEval, HellaSwag, and BFCL, finding Q4_K_M offers the best practical tradeoff with minimal accuracy loss and significant memory/throughput gains. This comparison helps practitioners choose the right quantization for local deployment, balancing accuracy, memory, and speed, which is critical for running large models on consumer hardware. Q4_K_M achieved 66.54% average accuracy (vs 69.78% BF16), 22.5 tok/s throughput (1.45x faster), and 28 GB peak RAM (48% less), while Q8_0 surprisingly underperformed Q4_K_M on HellaSwag (83% vs 86%).

reddit · r/LocalLLaMA · gvij · Apr 28, 12:18

**Background**: GGUF is a file format for storing quantized LLMs, enabling efficient inference on CPUs and low-resource devices. Quantization reduces model precision (e.g., from 16-bit to 4-bit) to shrink size and speed up inference, often with minor accuracy loss. Q4_K_M and Q8_0 are common quantization levels in llama.cpp, with Q4_K_M being a 4-bit method that uses a combination of quantization techniques for better quality.

<details><summary>References</summary>
<ul>
<li><a href="https://medium.com/@vimalkansal/understanding-the-gguf-format-a-comprehensive-guide-67de48848256">Understanding the GGUF Format : A Comprehensive Guide | Medium</a></li>
<li><a href="https://github.com/ggml-org/llama.cpp/discussions/2094">Difference in different quantization methods · ggml-org llama.cpp...</a></li>
<li><a href="https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks">The Complete Guide to LLM Quantization with vLLM... | Jarvis Labs</a></li>

</ul>
</details>

**Discussion**: Commenters appreciated the comparison but raised concerns about missing error bars, potential sampling error, and the surprising Q8_0 underperformance. Some questioned the validity of the results, noting that Qwen 3.6 27B should score higher on HumanEval based on other leaderboards, and suggested KV cache quantization might have affected Q8_0.

**Tags**: `#LLM`, `#quantization`, `#benchmarking`, `#Qwen`, `#GGUF`

---

<a id="item-27"></a>
## [DeepSeek Vision Development Sparks Community Excitement](https://www.reddit.com/gallery/1sxy0o7) ⭐️ 7.0/10

DeepSeek is reportedly developing vision capabilities, as hinted by a post from Xiaokang Chen on X, leading to speculation about native multimodality in future models like DeepSeek V4. If DeepSeek integrates native vision capabilities, it could compete with frontier multimodal models like Llama 4, offering a powerful local AI solution for tasks requiring both text and image understanding. DeepSeek already has separate vision-language models like DeepSeek-VL2, but the community hopes for native multimodality (early fusion) in a single model rather than separate vision-specific releases.

reddit · r/LocalLLaMA · Nunki08 · Apr 28, 10:58

**Background**: Multimodal LLMs process multiple data types (text, images, etc.) within one model. Native multimodality, as seen in Llama 4, uses early fusion to jointly train on text and visual data, enabling seamless understanding across modalities. DeepSeek's existing VL2 model uses a separate vision encoder, which is less integrated.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/deepseek-vl2">deepseek-ai/deepseek-vl2 - Hugging Face</a></li>
<li><a href="https://github.com/deepseek-ai/DeepSeek-VL">DeepSeek-VL: Towards Real-World Vision-Language Understanding</a></li>
<li><a href="https://arxiv.org/abs/2412.10302">DeepSeek-VL2: Mixture-of-Experts Vision-Language Models for ... - arXiv</a></li>

</ul>
</details>

**Discussion**: The community is excited but divided: some hope for native multimodality in V4 rather than separate vision models, while others question the practical use of vision features. A few users express frustration over missing GGUF support for certain DeepSeek versions.

**Tags**: `#DeepSeek`, `#vision`, `#multimodal`, `#LLM`, `#AI`

---

<a id="item-28"></a>
## [Anthropic's Project Deal: AI Agents Trade in Real Marketplace](https://futurism.com/artificial-intelligence/claude-give-ai-agents-money-project-deal) ⭐️ 7.0/10

Anthropic conducted Project Deal, an experiment where Claude AI agents acted as digital proxies for 69 employees, each given $100 and used items, to negotiate and complete real second-hand transactions. The agents successfully closed 186 deals with a total value of over $4,000. This experiment demonstrates that AI agents can autonomously conduct real-world commercial transactions, hinting at a future where AI handles everyday bargaining and even financial management. However, the lack of legal and regulatory frameworks for such autonomous commerce poses significant risks. Notably, some AI agents made bizarre mistakes, such as buying back the seller's own item or purchasing 19 used ping-pong balls as a gift for itself. The experiment highlights both the potential and the current limitations of AI in negotiation and decision-making.

telegram · zaihuapd · Apr 28, 07:31

**Background**: AI agents are software programs that can autonomously perform tasks on behalf of users, such as negotiating prices or executing transactions. Anthropic, an AI safety company, designed Project Deal to explore how AI models could impact commercial transactions. Similar systems, like Pactum, are already used by large companies for automated contract negotiations, but Project Deal focuses on peer-to-peer marketplace interactions.

<details><summary>References</summary>
<ul>
<li><a href="https://www.anthropic.com/features/project-deal">Project Deal : our Claude-run marketplace... | Anthropic \ Anthropic</a></li>
<li><a href="https://gigazine.net/gsc_news/en/20260427-project-deal-anthropic/">Anthropic conducted Project Deal , a simulation of an AI... - GIGAZINE</a></li>
<li><a href="https://spectrum.ieee.org/ai-contracts">AI Agents Are Taking Over Contract Negotiations - IEEE Spectrum Top Stories Advancing AI Negotiations: A Large-Scale Autonomous ... From Agent to Advisor: How AI Is Transforming Negotiation AI Agents in Negotiation: From Game Theory to Diplomacy ... Anthropic Tests AI Agent Commerce Marketplace AI Agents Are Taking Over Contract Negotiations - IEEE Spectrum Advancing AI Negotiations : A Large-Scale Autonomous Negotiation Co… AI Agents Are Taking Over Contract Negotiations - IEEE Spectrum From Agent to Advisor: How AI Is Transforming Negotiation A2A Protocol Explained: How AI Agents Negotiate and ... ServiceNow® AI Agents - Breakthrough AI Innovation AI Assistant Capabilities - What Is An AI Assistant</a></li>

</ul>
</details>

**Tags**: `#AI agents`, `#autonomous negotiation`, `#Anthropic`, `#market experiment`, `#AI safety`

---

<a id="item-29"></a>
## [China Adds 38 New Undergraduate Majors Including Embodied Intelligence](https://mp.weixin.qq.com/s/T5yv1EVEL1mDSb1_58TO2g) ⭐️ 7.0/10

China's Ministry of Education has added 38 new undergraduate majors for 2026, including embodied intelligence, brain-computer science, and digital cultural tourism, with interdisciplinary fields listed for the first time. This move aligns higher education with emerging AI and tech needs, fostering a workforce skilled in embodied intelligence and other interdisciplinary areas critical for AI-实体经济 integration. The new majors cover fields like energy science, agricultural robotics, biomanufacturing, and digital trade; nine universities including HIT are approved to offer embodied intelligence programs. The undergraduate catalog now includes 883 majors across 92 categories.

telegram · zaihuapd · Apr 28, 08:52

**Background**: Embodied intelligence refers to AI systems that interact with the physical world through sensors and actuators, such as robots. China's '14th Five-Year Plan' emphasizes AI and interdisciplinary education, with major adjustments exceeding 30% during the period.

<details><summary>References</summary>
<ul>
<li><a href="http://scis.scichina.com/cn/2025/SSI-2025-0177.pdf">SCIENTIA SINICA</a></li>
<li><a href="https://www.cns.org.cn/upload/file/20210913/161424_30952.pdf">QYKX20210919B</a></li>

</ul>
</details>

**Tags**: `#education policy`, `#embodied intelligence`, `#AI`, `#interdisciplinary`, `#China`

---

<a id="item-30"></a>
## [China penalizes Jianying, Jimeng AI for improper AI content labeling](https://www.cac.gov.cn/2026-04/28/c_1779119736411711.htm) ⭐️ 7.0/10

On April 28, 2026, China's Cyberspace Administration announced that popular apps Jianying (CapCut) and Maoxiang, as well as the Jimeng AI website, were penalized for failing to properly label AI-generated content as required by law. This enforcement signals that China is actively enforcing its AI content labeling regulations, which took effect in September 2025, and that major platforms must comply or face consequences. It sets a precedent for how AI-generated content must be transparently identified across the industry. The platforms were found to violate the Cybersecurity Law, the Interim Measures for the Management of Generative AI Services, and the Measures for the Identification of AI-Generated Synthetic Content. Penalties included interviews, orders for rectification, warnings, and strict handling of responsible personnel.

telegram · zaihuapd · Apr 28, 09:29

**Background**: China's AI content labeling regulation, jointly issued by four government departments, took effect on September 1, 2025. It requires all AI-generated or synthetic content to be clearly marked with visible or metadata labels to help users distinguish AI-produced material. Jianying (CapCut) is a popular video editing app owned by ByteDance, and Jimeng AI is an AI image and video generation platform.

<details><summary>References</summary>
<ul>
<li><a href="https://news.cctv.com/2026/04/28/ARTIxoB8rJbUZOlu2zt7AG3J260428.shtml">网信部门依法查处“剪映”App等生成合成内容标识违法问题网站平台_新闻...</a></li>
<li><a href="https://www.36kr.com/p/3786399364455686">工信部约谈剪映、猫箱、即梦AI网站等平台，违反AI生成内容标识办法-36...</a></li>

</ul>
</details>

**Tags**: `#AI regulation`, `#content moderation`, `#China`, `#AI ethics`, `#compliance`

---

<a id="item-31"></a>
## [Warp Open-Sources Client Codebase with GPT-Powered Agent Workflows](https://github.com/warpdotdev/warp) ⭐️ 7.0/10

Warp, a terminal-based smart development environment, has open-sourced its client codebase under a dual license (MIT for UI framework, AGPL v3 for the rest) and introduced GPT-powered agent workflows for coding tasks. This move makes a popular AI-enhanced terminal accessible to the open-source community, potentially accelerating innovation in developer tooling and enabling custom integrations with AI agents like Claude Code and Gemini CLI. The codebase is hosted on GitHub under the Warpdotdev organization; OpenAI is a founding sponsor. The built-in coding agent is powered by GPT models, and users can also connect third-party CLI agents such as Claude Code, Codex, and Gemini CLI.

telegram · zaihuapd · Apr 28, 17:04

**Background**: Warp is a modern terminal emulator that integrates AI features to improve command-line productivity. The AGPL v3 license requires that modified versions of the software be made available to users who interact with it over a network, ensuring that improvements remain open.

<details><summary>References</summary>
<ul>
<li><a href="https://www.xda-developers.com/warp-isnt-terminal-tried-new-agentic-coding-mode/">Warp isn't really a terminal anymore, and I tried its new</a></li>
<li><a href="https://en.wikipedia.org/wiki/AGPL_license">AGPL license</a></li>
<li><a href="https://openai.com/index/introducing-workspace-agents-in-chatgpt/">Introducing workspace agents in ChatGPT - OpenAI</a></li>

</ul>
</details>

**Tags**: `#open source`, `#terminal`, `#AI`, `#developer tools`, `#Warp`

---