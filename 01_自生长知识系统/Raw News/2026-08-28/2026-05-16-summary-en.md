---
layout: default
title: "Horizon Summary: 2026-05-16 (EN)"
date: 2026-05-16
lang: en
---

> From 44 items, 18 important content pieces were selected

---

1. [vLLM v0.21.0 Released with Breaking Changes and New Features](#item-1) ⭐️ 9.0/10
2. [Pixel 10 0-click exploit chain detailed by Project Zero](#item-2) ⭐️ 9.0/10
3. [arXiv bans papers with unchecked LLM errors for 1 year](#item-3) ⭐️ 9.0/10
4. [Offline Suitcase Robot Built with Jetson Orin NX and Gemma 4 LLM](#item-4) ⭐️ 9.0/10
5. [Orthrus accelerates Qwen3-8B up to 7.8x with diffusion attention](#item-5) ⭐️ 9.0/10
6. [Intern-S2-Preview: 35B Model Matches Trillion-Scale Performance](#item-6) ⭐️ 9.0/10
7. [Calif and Mythos Preview crack Apple M5 kernel in 5 days](#item-7) ⭐️ 9.0/10
8. [Mitchell Hashimoto warns of 'AI psychosis' in companies](#item-8) ⭐️ 8.0/10
9. [Zulip Announces Nonprofit Foundation for Long-Term Independence](#item-9) ⭐️ 8.0/10
10. [DOJ demands Apple and Google unmask 100k app users](#item-10) ⭐️ 8.0/10
11. [ABC News Takes Down All FiveThirtyEight Articles](#item-11) ⭐️ 8.0/10
12. [OxCaml Brings GC Improvements to Space Satellites](#item-12) ⭐️ 8.0/10
13. [Radicle: Peer-to-Peer Code Forge Built on Git](#item-13) ⭐️ 8.0/10
14. [BPF integration into Linux memory management faces obstacles](#item-14) ⭐️ 8.0/10
15. [Seven stable kernels patch CVE-2026-46333 with exploit available](#item-15) ⭐️ 8.0/10
16. [California Class Action Alleges OpenAI Shared User Data Without Consent](#item-16) ⭐️ 8.0/10
17. [Apple-OpenAI Partnership Frays, Legal Action Possible](#item-17) ⭐️ 8.0/10
18. [Trump Discusses AI Guardrails, Nvidia H200 Chip with Xi](#item-18) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [vLLM v0.21.0 Released with Breaking Changes and New Features](https://github.com/vllm-project/vllm/releases/tag/v0.21.0) ⭐️ 9.0/10

vLLM v0.21.0 introduces breaking build changes (C++20 requirement), deprecates transformers v4 in favor of v5, adds KV offload with Hybrid Memory Allocator (HMA), enables speculative decoding with thinking budget for reasoning models, and introduces a new TOKENSPEED_MLA attention backend for Blackwell GPUs. This release requires users to migrate to newer build environments (C++20) and transformers v5, potentially breaking existing workflows, while also bringing performance improvements like KV offload and speculative decoding that enhance inference efficiency for large reasoning models. The KV offload now integrates with HMA, which groups layers by type and pools memory across groups. Speculative decoding now respects reasoning/thinking budgets, enabling correct speculation for reasoning models. The MLA backend is specifically for DeepSeek-R1/Kimi-K25 on Blackwell GPUs.

github · khluu · May 15, 08:44

**Background**: vLLM is a high-throughput LLM inference engine that uses continuous batching and attention backends. The Hybrid Memory Allocator (HMA) is a new memory management approach that groups layers by type to improve memory efficiency. Speculative decoding is a technique where a smaller draft model generates proposals that a larger target model verifies to speed up inference. The thinking budget allows the model to allocate compute for reasoning steps.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/vllm-project/vllm/issues/11382">[RFC]: Hybrid Memory Allocator · Issue #11382 · vllm-project/vllm</a></li>
<li><a href="https://docs.vllm.ai/en/latest/design/attention_backends/">Attention Backend Feature Support - vLLM</a></li>
<li><a href="https://deepwiki.com/vllm-project/vllm/6.2-cuda-platform">CUDA Platform | vllm-project/vllm | DeepWiki</a></li>

</ul>
</details>

**Tags**: `#vLLM`, `#LLM inference`, `#breaking changes`, `#release`, `#GPU`

---

<a id="item-2"></a>
## [Pixel 10 0-click exploit chain detailed by Project Zero](https://projectzero.google/2026/05/pixel-10-exploit.html) ⭐️ 9.0/10

Google Project Zero published a detailed analysis of a 0-click exploit chain targeting the Pixel 10, highlighting how AI-powered features increase the attack surface by pre-processing messages and media before user interaction. This research underscores that zero-click exploits remain a critical threat despite fast patching, and the expansion of AI features in mobile devices adds new attack vectors that affect all platforms adopting similar capabilities. The exploit chain leverages multiple vulnerabilities, including a driver bug that was patched within 90 days—notably fast by Android standards. The analysis specifically calls out the risk of decoding media before user action as a side effect of AI features like Magic Cue and Voice Translate.

hackernews · happyhardcore · May 15, 13:39 · [Discussion](https://news.ycombinator.com/item?id=48148460)

**Background**: A 0-click exploit requires no user interaction, making it extremely stealthy. An exploit chain combines multiple vulnerabilities to achieve full device compromise. Google Project Zero is a security team that discovers and publicly discloses zero-day vulnerabilities to improve security across the industry.

<details><summary>References</summary>
<ul>
<li><a href="https://www.schneier.com/blog/archives/2023/09/zero-click-exploit-in-iphones.html">Zero-Click Exploit in iPhones - Schneier on Security</a></li>
<li><a href="https://www.csoonline.com/article/571799/exploit-chains-explained-how-and-why-attackers-target-multiple-vulnerabilities.html">Exploit chains explained: How and why attackers target ...</a></li>
<li><a href="https://blog.google/products-and-platforms/devices/pixel/google-pixel-10-ai-features-updates/">Google Pixel 10: 9 new AI features and updates - The Keyword</a></li>

</ul>
</details>

**Discussion**: Commenters expressed concern that AI features increase the 0-click attack surface, with one noting that Google's 90-day patch window was fast but raising questions about other Android vendors. Others debated the frequency of exploits and compared Apple's response times.

**Tags**: `#security`, `#mobile`, `#exploit`, `#Android`, `#Project Zero`

---

<a id="item-3"></a>
## [arXiv bans papers with unchecked LLM errors for 1 year](https://www.reddit.com/r/MachineLearning/comments/1tdje2d/arxiv_implements_1year_ban_for_papers_containing/) ⭐️ 9.0/10

arXiv announced a 1-year ban for submissions containing incontrovertible evidence that authors did not check LLM-generated output, such as hallucinated references or meta-comments from the AI. This policy directly addresses the epidemic of LLM-generated errors in scientific papers, holding authors fully responsible and deterring sloppy use of AI in research. Incontrovertible evidence includes hallucinated references and meta-comments like 'here is a 200 word summary; would you like me to make any changes?'; the ban is 1 year plus a requirement that future submissions be accepted at a reputable peer-reviewed venue first.

reddit · r/MachineLearning · Nunki08 · May 15, 02:44

**Background**: arXiv is an open-access preprint repository that hosts papers before peer review, moderated but not peer-reviewed. Recent studies have found a sharp rise in hallucinated citations due to widespread LLM use, polluting the scientific literature. This policy aims to maintain research integrity by enforcing author responsibility for content regardless of origin.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/ArXiv">arXiv - Wikipedia</a></li>
<li><a href="https://www.nature.com/articles/d41586-026-00969-z">Hallucinated citations are polluting the scientific ... - Nature</a></li>
<li><a href="https://arxiv.org/abs/2605.07723">[2605.07723] LLM hallucinations in the wild: Large-scale ...</a></li>

</ul>
</details>

**Discussion**: The Reddit community overwhelmingly supports the policy, with many calling for even longer bans (3–5 years or permanent). Some commenters note that the 'incontrovertible evidence' threshold only catches the most blatant cases, while more subtle LLM errors remain hard to detect.

**Tags**: `#arXiv`, `#LLM`, `#research integrity`, `#policy`, `#academic publishing`

---

<a id="item-4"></a>
## [Offline Suitcase Robot Built with Jetson Orin NX and Gemma 4 LLM](https://v.redd.it/9v5pmv1rgb1h1) ⭐️ 9.0/10

A developer created a fully offline suitcase robot named Sparky, running Gemma 4 E4B on a Jetson Orin NX, achieving approximately 200ms cached time-to-first-token through optimized prompt caching and integrating over 30 sensors for rich context. This demonstrates cutting-edge integration of a state-of-the-art local LLM with real-time robotics, proving that complex AI can run entirely offline on edge hardware. It pushes the boundaries of privacy, latency, and autonomy for interactive robots. The system uses llama.cpp with q8_0 KV cache and flash attention, running Gemma 4 E4B at Q4_K_M quantization. The prompt structure places persona and tools at the top, history in the middle, and volatile sensor data at the end to maintain cache stability, reducing TTFT from multiple seconds to about 200ms.

reddit · r/LocalLLaMA · CreativelyBankrupt · May 15, 15:09 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1tdz5gr/built_a_fully_offline_suitcase_robot_around_a/)

**Background**: Running large language models on embedded devices is challenging due to compute and memory constraints. The Jetson Orin NX is a powerful edge AI platform, and Gemma 4 is Google's latest open model family with native system prompt support and speculative decoding. By optimizing prompt caching and using quantization, the developer achieved low latency entirely offline, without any network connectivity.

<details><summary>References</summary>
<ul>
<li><a href="https://huggingface.co/google/gemma-4-E4B">google/gemma-4-E4B · Hugging Face</a></li>
<li><a href="https://ai.google.dev/gemma/docs/core">Gemma 4 model overview - Google AI for Developers</a></li>
<li><a href="https://ollama.com/library/gemma4:e4b">gemma4:e4b</a></li>

</ul>
</details>

**Discussion**: The community was highly positive, praising the hardware design and calling it one of the best projects seen. Some humorous comments about airport security and references to sci-fi computers. Suggestions included adding memory systems to allow the robot to evolve over time.

**Tags**: `#edge AI`, `#robotics`, `#Jetson Orin`, `#Gemma 4`, `#offline LLM`

---

<a id="item-5"></a>
## [Orthrus accelerates Qwen3-8B up to 7.8x with diffusion attention](https://i.redd.it/kmqh40q2nc1h1.gif) ⭐️ 9.0/10

Orthrus introduces a dual-architecture framework that augments a frozen Qwen3-8B with a lightweight diffusion attention module, achieving up to 7.8x token-per-forward speedup while provably preserving the original output distribution. This breakthrough significantly reduces LLM inference latency without any loss in accuracy, making large models more practical for real-time applications. It also challenges existing acceleration methods like speculative decoding by eliminating external drafters and cache overhead. The method trains only 16% of the model's parameters on fewer than 1 billion tokens for 24 hours on 8×H200 GPUs. It uses a shared KV cache between the diffusion and autoregressive heads, resulting in a flat KV overhead of about 4.5 MiB.

reddit · r/LocalLLaMA · Franck_Dernoncourt · May 15, 19:07 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1te5xpu/orthrusqwen38b_up_to_78tokensforward_on_qwen38b/)

**Background**: Autoregressive LLMs generate tokens sequentially, which limits speed. Diffusion models can generate multiple tokens in parallel. Orthrus combines both by adding a trainable diffusion module to a frozen autoregressive model, enabling parallel token generation while ensuring the output distribution matches the original model exactly.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/chiennv2000/orthrus">GitHub - chiennv2000/orthrus: Fast, lossless LLM inference ...</a></li>
<li><a href="https://huggingface.co/chiennv/Orthrus-Qwen3-8B">chiennv/Orthrus-Qwen3-8B · Hugging Face</a></li>

</ul>
</details>

**Discussion**: The community shows strong interest with questions about applicability to MoE models, larger contexts, RAM usage, and scaling to larger models. Some commenters praise the approach as a paradigm shift and inquire about integration with frameworks like llama.cpp.

**Tags**: `#efficient inference`, `#diffusion attention`, `#Qwen`, `#transformer optimization`, `#LLM speedup`

---

<a id="item-6"></a>
## [Intern-S2-Preview: 35B Model Matches Trillion-Scale Performance](https://huggingface.co/internlm/Intern-S2-Preview) ⭐️ 9.0/10

Shanghai AI Laboratory released Intern-S2-Preview, a 35B parameter scientific multimodal foundation model that achieves performance comparable to its trillion-scale predecessor Intern-S1-Pro on core scientific tasks. This demonstrates that task scaling—increasing difficulty and diversity of tasks—can rival conventional parameter scaling, making state-of-the-art scientific AI more accessible to researchers with limited computational resources. It is continued pre-trained from Qwen3.5, features full-chain training from pre-training to RL, and introduces crystal structure generation and real-valued prediction modules.

reddit · r/LocalLLaMA · pmttyji · May 15, 10:09 · [Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1tdrw0s/internlminterns2preview_hugging_face/)

**Background**: Conventional AI scaling has focused on increasing model parameters and training data. Task scaling, in contrast, enhances model capabilities by systematically expanding the range, difficulty, and coverage of tasks during training. Intern-S2-Preview applies this approach to scientific domains, achieving efficiency without massive parameter counts.

<details><summary>References</summary>
<ul>
<li><a href="https://docs.sglang.io/cookbook/autoregressive/InternLM/Intern-S2-Preview">Intern-S2-Preview - SGLang Documentation</a></li>
<li><a href="https://recipes.vllm.ai/internlm/Intern-S2-Preview">internlm/Intern-S2-Preview | vLLM Recipes</a></li>

</ul>
</details>

**Discussion**: The Reddit community is generally positive, with users praising the model's efficiency and unique features like crystal generation. Some users are looking forward to GGUF quantizations and hope for a larger 122B version. The discussion highlights interest in task scaling as a promising research direction.

**Tags**: `#AI`, `#Machine Learning`, `#Scientific Models`, `#Task Scaling`, `#Multimodal`

---

<a id="item-7"></a>
## [Calif and Mythos Preview crack Apple M5 kernel in 5 days](https://blog.calif.io/p/first-public-kernel-memory-corruption) ⭐️ 9.0/10

Calif, in collaboration with Anthropic's AI system Mythos Preview, constructed a working kernel memory corruption exploit for Apple M5 hardware running macOS 26.4.1 in just five days, from April 25 to May 1. The exploit chain bypasses Apple's Memory Integrity Enforcement (MIE) hardware protection, allowing an unprivileged user to gain root shell access using only normal system calls. This is the first public demonstration of a kernel memory corruption exploit on Apple M5, bypassing MIE which Apple spent five years and significant resources to develop. It shows that AI-assisted security research can rapidly defeat cutting-edge hardware defenses, potentially shifting the balance in vulnerability exploitation. The exploit chain involves two vulnerabilities and multiple techniques discovered with Mythos Preview's assistance. A full 55-page technical report will be released after Apple issues a fix for the vulnerabilities.

telegram · zaihuapd · May 15, 02:15

**Background**: Apple M5 is the latest generation of Apple's custom silicon, succeeding the M4, and features unified memory architecture for AI performance. Memory Integrity Enforcement (MIE) is a hardware security mechanism designed to prevent memory corruption attacks on the kernel, representing a five-year engineering investment. Mythos Preview is an advanced AI model from Anthropic, used for cybersecurity research and vulnerability discovery, and has already found thousands of high-severity vulnerabilities in major operating systems and browsers.

<details><summary>References</summary>
<ul>
<li><a href="https://blog.calif.io/p/first-public-kernel-memory-corruption">First public macOS kernel memory corruption exploit on Apple M5</a></li>
<li><a href="https://insiderllm.com/guides/mythos-cracked-apple-m5-5-days/">Mythos AI Cracked Apple 's Best Defense in 5 Days | InsiderLLM</a></li>
<li><a href="https://9to5mac.com/2026/04/07/anthropic-unveils-powerful-mythos-ai-model-working-with-apple-in-cybersecurity-initiative/">Anthropic unveils powerful Mythos AI model, working with... - 9to5Mac</a></li>

</ul>
</details>

**Tags**: `#security`, `#macOS`, `#kernel exploit`, `#AI-assisted`, `#Apple M5`

---

<a id="item-8"></a>
## [Mitchell Hashimoto warns of 'AI psychosis' in companies](https://twitter.com/mitchellh/status/2055380239711457578) ⭐️ 8.0/10

Mitchell Hashimoto, co-founder of HashiCorp, posted a warning on social media that many companies are suffering from 'AI psychosis,' blindly trusting AI outputs without proper oversight, leading to risky decisions. This highlights a critical risk in the current AI hype cycle, where companies may deploy unreliable AI-generated code or decisions without human verification, potentially causing system failures or security breaches. Hashimoto's post references a Mastodon thread where he elaborates on the concept. The tweet has garnered over 600 points and 283 comments, indicating high community engagement.

hackernews · reasonableklout · May 15, 20:26 · [Discussion](https://news.ycombinator.com/item?id=48153379)

**Background**: AI psychosis refers to the uncritical acceptance of AI-generated outputs without proper scrutiny. As large language models become more capable, there is a growing tendency to rely on them for coding, decision-making, and even infrastructure management, often without understanding the limitations.

**Discussion**: Comments discuss the potential rise of 'AI rescue consulting' similar to security breach response, and the risk of AI-generated systems becoming too complex for humans to understand. Some argue that using AI is fine if treated as a tool, not as an oracle.

**Tags**: `#AI`, `#software engineering`, `#technology criticism`, `#risk management`, `#decision-making`

---

<a id="item-9"></a>
## [Zulip Announces Nonprofit Foundation for Long-Term Independence](https://blog.zulip.com/2026/05/15/announcing-zulip-foundation/) ⭐️ 8.0/10

Zulip announced the creation of the Zulip Foundation, a nonprofit organization, with the company donated to it by its founders who are stepping back to join Anthropic. This move secures Zulip's independence and addresses user trust concerns about data privacy and commercial pressures, setting an example for open-source messaging platforms. The announcement was made on a Friday afternoon, which some view as a low-attention timing, and involves key team members leaving to join Anthropic while donating the company to the foundation.

hackernews · boramalper · May 15, 18:37 · [Discussion](https://news.ycombinator.com/item?id=48152168)

**Background**: Zulip is an open-source team chat platform known for its topic-based threading, competing with Slack and Discord. Many open-source projects establish foundations to ensure neutrality and long-term sustainability, as seen with Blender or Kubernetes.

<details><summary>References</summary>
<ul>
<li><a href="https://alternativeto.net/news/2026/4/zulip-12-0-adds-end-to-end-encrypted-mobile-push-notifications-and-easier-docker-deployment/">Zulip 12.0 adds end-to-end encrypted mobile push notifications</a></li>
<li><a href="https://alternativeto.net/news/2024/12/zulip-unveils-new-mobile-app-in-beta-with-multi-account-support-and-enhanced-performance/">Zulip unveils new mobile app in beta with multi-account support</a></li>

</ul>
</details>

**Discussion**: Community reactions are mixed: some praise the transparency and trust-building, while others express cynicism about the Friday timing and the loss of core developers to Anthropic. One commenter notes this could help Anthropic challenge Slack in the enterprise.

**Tags**: `#open-source`, `#Zulip`, `#nonprofit`, `#messaging`, `#foundation`

---

<a id="item-10"></a>
## [DOJ demands Apple and Google unmask 100k app users](https://macdailynews.com/2026/05/15/u-s-doj-demands-apple-and-google-unmask-over-100000-users-of-popular-car-tinkering-app-in-emissions-crackdown/) ⭐️ 8.0/10

The U.S. Department of Justice has issued demands to Apple and Google to reveal the identities of over 100,000 users who downloaded a car-tinkering app used to modify vehicle emissions controls. This case raises significant privacy concerns about government overreach and the power of centralized app stores to hand over user data, potentially setting a precedent for future surveillance. The app is reportedly used to defeat emissions controls, similar to 'rolling coal' modifications, and the DOJ wants to interview users as witnesses, not necessarily prosecute them.

hackernews · tencentshill · May 15, 17:28 · [Discussion](https://news.ycombinator.com/item?id=48151383)

**Background**: Engine Control Unit (ECU) remapping allows car owners to modify software parameters to increase performance or disable emissions controls. However, using defeat devices to bypass emissions regulations is illegal in many jurisdictions, including the U.S. under the Clean Air Act.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Defeat_device">Defeat device - Wikipedia</a></li>
<li><a href="https://www.epa.gov/sites/default/files/2020-12/documents/tamperinganddefeatdevices-enfalert.pdf">Aftermarket Defeat Devices and Tampering are Illegal and Undermine...</a></li>

</ul>
</details>

**Discussion**: Commenters express mixed views; some criticize the app for enabling pollution, while others worry about privacy and government overreach, noting that this could set a precedent for broader surveillance. One commenter suggests using anonymous app stores like F-Droid.

**Tags**: `#privacy`, `#legal`, `#app store`, `#government surveillance`, `#emissions`

---

<a id="item-11"></a>
## [ABC News Takes Down All FiveThirtyEight Articles](https://twitter.com/baseballot/status/2055309076209492208) ⭐️ 8.0/10

ABC News has removed all articles from the FiveThirtyEight website, effectively shutting down the data journalism platform. This action follows months of decline and layoffs at the property, which was acquired by Disney in 2018. The removal erases years of high-quality data journalism, including interactive visualizations and election forecasts that were widely referenced. It also highlights corporate mismanagement of a valuable brand and raises concerns about the preservation of digital journalism archives. Nate Silver, founder of FiveThirtyEight, approached ABC News about buying back the brand's intellectual property but was refused. Users have called for backing up FiveThirtyEight's public GitHub repository before it is also removed.

hackernews · cmsparks · May 15, 19:07 · [Discussion](https://news.ycombinator.com/item?id=48152553)

**Background**: FiveThirtyEight was founded by Nate Silver in 2008, known for its statistical analysis of politics, sports, and other topics. It was acquired by Disney-owned ABC News in 2018 but faced layoffs and reduced investment, especially after the 2020 election cycle. Data journalism sites like FiveThirtyEight rely on complex visualizations and datasets that are costly to maintain, making them vulnerable to corporate budget cuts.

**Discussion**: Commenters widely criticized ABC News for poor brand management, noting its refusal to sell the intellectual property back to Nate Silver out of apparent pettiness. Many expressed sadness over losing valuable visualizations, such as gun deaths and microbiome explorations, and urged the community to back up the GitHub repository.

**Tags**: `#journalism`, `#data visualization`, `#fivethirtyeight`, `#abc news`, `#brand management`

---

<a id="item-12"></a>
## [OxCaml Brings GC Improvements to Space Satellites](https://gazagnaire.org/blog/2026-05-14-borealis.html) ⭐️ 8.0/10

OCaml has been deployed in space satellites, and its variant OxCaml achieves dramatic latency and garbage collection improvements via stack annotations. Specifically, OxCaml reduces p99.9 latency from 29 ns to 9 ns per packet and eliminates minor GCs entirely over 25 million packets. This demonstrates that a garbage-collected language like OCaml can be effectively used in performance-critical, embedded space systems by minimizing GC overhead. It opens the door for safer, higher-level programming in environments traditionally dominated by C and assembly. The stack annotations in OxCaml allow programmers to explicitly place data on the stack instead of the heap, reducing GC pressure and improving cache efficiency. Throughput remains comparable to the original OCaml while latency is drastically reduced.

hackernews · yminsky · May 15, 10:55 · [Discussion](https://news.ycombinator.com/item?id=48147058)

**Background**: Garbage collection (GC) automatically reclaims memory, but it introduces pauses that are problematic for real-time systems. In contrast, stack allocation is deterministic and freed when a function returns, avoiding GC overhead. OxCaml is a set of extensions to OCaml developed by Jane Street, focusing on performance-oriented programming with finer control over memory allocation.

<details><summary>References</summary>
<ul>
<li><a href="https://oxcaml.org/">OxCaml | About</a></li>
<li><a href="https://blog.janestreet.com/introducing-oxcaml/">Jane Street Blog - Introducing OxCaml</a></li>

</ul>
</details>

**Discussion**: Community comments include a firsthand account of deploying OCaml in space in 2016, and praise for OxCaml's GC improvements. There is also discussion about similar techniques in Java for high-frequency trading, and skepticism about the security of custom CCSDS protocols versus using battle-tested TLS.

**Tags**: `#OCaml`, `#space`, `#garbage collection`, `#systems programming`, `#performance`

---

<a id="item-13"></a>
## [Radicle: Peer-to-Peer Code Forge Built on Git](https://radicle.dev/) ⭐️ 8.0/10

Radicle is a peer-to-peer code forge that provides a decentralized alternative to centralized platforms like GitHub, using Git for version control and a P2P network for collaboration. It matters because it offers a censorship-resistant and decentralized code hosting solution, giving developers control over their infrastructure and data, which is significant for open-source communities concerned about centralization. Radicle supports private repos where history remains public but new updates are not publicized, and uses cryptographic identities and signed artifacts by default. The project recently moved to the radicle.dev domain.

hackernews · KolmogorovComp · May 15, 12:07 · [Discussion](https://news.ycombinator.com/item?id=48147603)

**Background**: A code forge is a platform for hosting and collaborating on code repositories. Centralized forges like GitHub dominate, but they rely on a single company's infrastructure. Radicle leverages Git's distributed nature and peer-to-peer networking to create a decentralized forge where users host their own data.

**Discussion**: The community raised concerns about Radicle's license not being AGPL, potentially allowing SaaS companies to extract value. Others appreciated the local-first design, private repo support, and use in agentic workflows. The recent domain move was also noted.

**Tags**: `#git`, `#distributed-vcs`, `#forge`, `#open-source`, `#p2p`

---

<a id="item-14"></a>
## [BPF integration into Linux memory management faces obstacles](https://lwn.net/Articles/1072538/) ⭐️ 8.0/10

At the 2026 LSFMM+BPF summit, Roman Gushchin and Shakeel Butt led sessions identifying obstacles and requirements for using BPF (Berkeley Packet Filter) to control memory management heuristics, such as out-of-memory handling and NUMA balancing. If successful, BPF-based memory management could allow flexible, user-defined policies without kernel changes, potentially improving performance and adaptability for diverse workloads. Key obstacles include out-of-tree BPF programs, inability to attach struct ops programs to control groups, and safety/fallback concerns where a broken BPF program could crash the system.

rss · LWN.net · May 15, 14:54

**Background**: The Linux Storage, Filesystem, Memory Management & BPF Summit (LSFMM+BPF) is an annual invitation-only event where kernel developers discuss improvements. BPF allows running sandboxed programs in the kernel, but its use in memory management is still experimental. Previous proposals for BPF-controlled memory heuristics have not been merged into the mainline kernel.

<details><summary>References</summary>
<ul>
<li><a href="https://events.linuxfoundation.org/lsfmmbpf/">Linux Storage, Filesystem, MM & BPF Summit | LF Events</a></li>

</ul>
</details>

**Tags**: `#Linux`, `#BPF`, `#memory management`, `#kernel development`

---

<a id="item-15"></a>
## [Seven stable kernels patch CVE-2026-46333 with exploit available](https://lwn.net/Articles/1073060/) ⭐️ 8.0/10

Greg Kroah-Hartman announced seven new stable Linux kernel versions (7.0.8, 6.18.31, 6.12.89, 6.6.139, 6.1.173, 5.15.207, and 5.10.256) that include a patch for CVE-2026-46333, a security vulnerability reported by Qualys with a published proof-of-concept exploit. This vulnerability has a published exploit and was initially reported in 2020, indicating a long-standing issue that could affect many systems; users are urged to upgrade immediately to prevent potential compromise. The vulnerability was originally discovered by Jann Horn in 2020, who proposed a patch, but it took until 2026 for the fix to be rolled out across stable kernels; some kernels include additional bug fixes.

rss · LWN.net · May 15, 13:34

**Background**: Linux stable kernels are long-term supported versions that receive ongoing security and bug fixes. CVE-2026-46333 is a security vulnerability that could allow attackers to exploit the system, and with a proof-of-concept exploit publicly available, the risk of active attacks is heightened.

<details><summary>References</summary>
<ul>
<li><a href="https://linuxsecurity.com/advisories/suse/suse-2020-0806-1-important-tomcat-14-19-09">SUSE: 2020:0806-1 Important: Tomcat File Disclosure Fix</a></li>

</ul>
</details>

**Tags**: `#Linux kernel`, `#security`, `#CVE`, `#stable kernels`, `#vulnerability`

---

<a id="item-16"></a>
## [California Class Action Alleges OpenAI Shared User Data Without Consent](https://futurism.com/artificial-intelligence/openai-personal-information-meta-google) ⭐️ 8.0/10

A class action lawsuit filed in California accuses OpenAI of sharing users' chat queries and personal information, including email addresses and user IDs, with Meta and Google without proper consent, using Meta Pixel and Google Analytics. This lawsuit highlights serious privacy concerns in the AI industry, where user interactions with AI systems may be tracked by third-party analytics tools without explicit consent. If successful, it could set a precedent for how AI companies handle user data and the use of tracking technologies. The lawsuit alleges violations of California's Invasion of Privacy Act and Electronic Communications Privacy Act, and notes that OpenAI has not yet responded to requests for comment. The data sharing allegedly occurred via Meta Pixel and Google Analytics tracking codes embedded in the ChatGPT interface.

telegram · zaihuapd · May 15, 03:45

**Background**: Meta Pixel (formerly Facebook Pixel) is a JavaScript tracking code that monitors user actions on websites for advertising and analytics; Google Analytics is a web analytics service that tracks and reports traffic. Both tools are widely used but have faced scrutiny over privacy compliance, including GDPR violations. Class action lawsuits in California often seek damages and injunctions for alleged violations of state privacy laws.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Meta_Pixel">Meta Pixel</a></li>
<li><a href="https://en.wikipedia.org/wiki/Google_Analytics">Google Analytics</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#OpenAI`, `#lawsuit`, `#data-sharing`, `#regulation`

---

<a id="item-17"></a>
## [Apple-OpenAI Partnership Frays, Legal Action Possible](https://www.bloomberg.com/news/articles/2026-05-14/openai-apple-partnership-frays-setting-up-possible-legal-fight) ⭐️ 8.0/10

OpenAI is considering legal action against Apple, alleging insufficient promotion of ChatGPT integration on Apple devices, leading to far lower subscription conversions than expected. This dispute threatens a high-profile partnership between two tech giants, potentially reshaping how AI models are integrated into consumer devices and influencing future collaboration in the AI industry. ChatGPT is currently buried deep in Apple's system with limited functionality, and most users still use the standalone app; Apple plans to open Siri to third-party models like Claude and Gemini at WWDC in iOS 27, further diluting OpenAI's exclusivity.

telegram · zaihuapd · May 15, 12:59

**Background**: Apple and OpenAI announced a partnership in 2024 to integrate ChatGPT into Apple Intelligence features, with hopes of generating billions in subscription revenue. However, disagreements over promotion, privacy, and talent poaching have escalated tensions.

<details><summary>References</summary>
<ul>
<li><a href="https://support.apple.com/zh-cn/guide/mac-help-cn/mchlfc5cf131/mac">在 Mac 上配合 Apple 智能使用 ChatGPT - 官方 Apple 支持 (中国)</a></li>
<li><a href="https://www.36kr.com/p/3740759301046274">开放 Siri，苹果决定打开万亿「AI 生态」-36氪</a></li>
<li><a href="https://m.ithome.com/html/933107.htm">古尔曼：苹果 iOS 27 将 开 放 Siri 第 三 方 AI 接口，谷歌 Gemini...</a></li>

</ul>
</details>

**Tags**: `#Apple`, `#OpenAI`, `#ChatGPT`, `#partnership`, `#legal`

---

<a id="item-18"></a>
## [Trump Discusses AI Guardrails, Nvidia H200 Chip with Xi](https://www.bloomberg.com/news/articles/2026-05-15/trump-says-he-discussed-ai-guardrails-nvidia-s-chips-with-xi) ⭐️ 8.0/10

During his visit to China, President Trump discussed AI guardrails and Nvidia H200 chip exports with President Xi, noting that China has chosen not to buy the H200 chips. This highlights ongoing geopolitical tensions over advanced AI chips and could impact global AI hardware supply chains and US-China tech decoupling. The US granted export licenses for Nvidia H200 to China, but China has not approved purchases; previously, China also rejected lower-tier H20 chips.

telegram · zaihuapd · May 15, 15:13

**Background**: The H200 is Nvidia's high-end AI accelerator, and the US has imposed export controls to limit China's access to advanced chips. The Anthropic Mythos model, a frontier AI model, was mentioned as a reason for establishing AI communication channels due to global cybersecurity concerns.

<details><summary>References</summary>
<ul>
<li><a href="https://alltechmagazine.com/anthropic-mythos-ai-model-explained/">Anthropic Mythos AI Model Explained: What It Can Do — And Why</a></li>
<li><a href="https://mediumpulse.com/claude-mythos-a-guide-on-the-much-talked-about-anthropic-model/">Claude Mythos: A Guide on the Much-Talked About Anthropic Model</a></li>

</ul>
</details>

**Tags**: `#AI chips`, `#US-China relations`, `#Nvidia`, `#H200`, `#export controls`

---