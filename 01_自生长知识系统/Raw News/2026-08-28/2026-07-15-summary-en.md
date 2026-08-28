---
layout: default
title: "Horizon Summary: 2026-07-15 (EN)"
date: 2026-07-15
lang: en
---

> From 38 items, 11 important content pieces were selected

---

1. [Stripe and Advent Offer $53B to Acquire PayPal](#item-1) ⭐️ 9.0/10
2. [Many old shim versions still accepted by Secure Boot](#item-2) ⭐️ 9.0/10
3. [DeepSeek’s annualized revenue nears $500M, V4 API margins top 50%](#item-3) ⭐️ 9.0/10
4. [Inkling: A New Open-Weights Multimodal Model with Audio Support](#item-4) ⭐️ 8.0/10
5. [Claude web\_fetch exploit leaks user memories](#item-5) ⭐️ 8.0/10
6. [Lockless MPSC FIFO queues for io\_uring in Linux 7.2](#item-6) ⭐️ 8.0/10
7. [Disentangling Convolutional Neurons via Hadamard Product Analysis](#item-7) ⭐️ 8.0/10
8. [7 Major Smartphone On-Device AI Models Registered in China](#item-8) ⭐️ 8.0/10
9. [Chinese retail vertical segmentation ends as players converge](#item-9) ⭐️ 8.0/10
10. [Google and Epic Drop Motion, Third-Party App Stores Coming to Google Play](#item-10) ⭐️ 8.0/10
11. [Telegram Launches Serverless Platform for Bots and Mini Apps](#item-11) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Stripe and Advent Offer $53B to Acquire PayPal](https://www.reuters.com/business/finance/stripe-advent-offer-buy-paypal-more-than-53-billion-sources-say-2026-07-15/) ⭐️ 9.0/10

Stripe and private equity firm Advent International made a joint offer to acquire PayPal for over $53 billion, according to sources. This acquisition would combine two major payment platforms, potentially reducing competition and raising antitrust concerns in the fintech industry. The offer is over $53 billion, and if completed, would bring together Stripe, PayPal, Venmo, Braintree, and Xoom under one umbrella.

hackernews · rvz · Jul 15, 03:32 · [Discussion](https://news.ycombinator.com/item?id=48915953)

**Background**: Stripe is a major online payment processor, while PayPal is a leading digital wallet. Both companies compete in the online checkout space. Antitrust regulators may scrutinize the deal due to potential market concentration.

**Discussion**: Commenters expressed strong opposition, citing concerns about fee increases, reduced competition, and Stripe&\#x27;s restrictive policies on certain merchants. Some noted potential antitrust issues due to high market share.

**Tags**: `#fintech`, `#acquisition`, `#payments`, `#antitrust`, `#Stripe`

---

<a id="item-2"></a>
## [Many old shim versions still accepted by Secure Boot](https://lwn.net/Articles/1082940/) ⭐️ 9.0/10

CMU CERT Coordination Center has disclosed that many exploitable versions of the shim bootloader were never added to the Secure Boot revocation list, allowing attackers to bypass Secure Boot protections and execute arbitrary code during early boot. This oversight undermines a fundamental security mechanism in Linux systems, potentially allowing persistent compromise that survives reboots and OS reinstalls. The advisory includes a list of vulnerable shims, but many were missed from the revocation list \(DBX\), which is used to block untrusted UEFI modules from loading.

rss · LWN.net · Jul 15, 12:49

**Background**: Secure Boot is a UEFI security feature that ensures only signed and trusted bootloaders can run. The shim bootloader acts as a bridge between UEFI firmware and the Linux bootloader, and a revocation list \(DBX\) is used to blacklist known vulnerable versions. Failure to add compromised shim versions to this list leaves systems exposed.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/rhboot/shim">GitHub - rhboot/shim: UEFI shim loader · GitHub</a></li>
<li><a href="https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_monitoring_and_updating_the_kernel/updating-the-secure-boot-revocation-list">Chapter 24. Updating the Secure Boot Revocation List | Managing...</a></li>

</ul>
</details>

**Tags**: `#security`, `#secure boot`, `#linux`, `#bootloader`, `#vulnerability`

---

<a id="item-3"></a>
## [DeepSeek’s annualized revenue nears $500M, V4 API margins top 50%](https://www.theinformation.com/articles/deepseeks-annualized-revenue-nears-500-million-boosting-fundraise-ipo-plans) ⭐️ 9.0/10

DeepSeek has achieved an annualized revenue of $400-500 million, primarily from enterprise and developer API calls, and its V4 API gross margin exceeds 50%. The company also plans to raise $7.4 billion at a $74 billion valuation. This milestone demonstrates strong commercial adoption and profitability for DeepSeek, validating the viability of its API business model against competitors like OpenAI and Anthropic. The massive valuation and fundraising indicate high investor confidence and potential for further growth in the competitive AI landscape. The annualized revenue is based on recent monthly run rates, not actual full-year realized revenue. DeepSeek achieved high margins despite charging significantly less than OpenAI and Anthropic, by optimizing infrastructure to reduce the number of chips needed to run its models.

telegram · zaihuapd · Jul 15, 07:04

**Background**: DeepSeek is a Chinese AI company known for developing large language models. The DeepSeek V4 API, launched in April 2026, is compatible with OpenAI and Anthropic API formats and is designed to offer cost-effective frontier AI capabilities. The company has also attracted investment from Tencent, CATL, and other major firms in its first funding round.

<details><summary>References</summary>
<ul>
<li><a href="https://api-docs.deepseek.com/">Your First API Call | DeepSeek API Docs</a></li>
<li><a href="https://deepseek.ai/deepseek-v4">DeepSeek AI: R1 Reasoning, API &amp; Local Deployment 2026</a></li>

</ul>
</details>

**Tags**: `#DeepSeek`, `#AI`, `#Revenue`, `#API`, `#Fundraising`

---

<a id="item-4"></a>
## [Inkling: A New Open-Weights Multimodal Model with Audio Support](https://thinkingmachines.ai/news/introducing-inkling/) ⭐️ 8.0/10

Thinking Machines AI released Inkling, a large open-weights multimodal model that supports audio input and enables fine-tuning on the Tinker platform. As one of the largest open-weights models supporting audio, Inkling provides enterprises and developers a customizable, locally deployable alternative to closed-source models, potentially reducing costs and fostering innovation in multimodal AI applications. Inkling is not the strongest overall model but combines multimodal capabilities, efficient thinking, and availability on Tinker for fine-tuning, making it a practical base for customization. Community resources for local deployment include llama.cpp branch, Unsloth, and Hugging Face GGUF/NVFP4 versions.

hackernews · vimarsh6739 · Jul 15, 18:12 · [Discussion](https://news.ycombinator.com/item?id=48924912)

**Background**: Open-weights models are AI models whose trained parameters \(weights\) are publicly released, allowing anyone to download and modify them. This contrasts with closed models like GPT-4, where only API access is given. Inkling supports audio as well as text and images, making it multimodal, though it does not support video. The Tinker platform allows users to fine-tune the model for specific tasks without deep expertise.

<details><summary>References</summary>
<ul>
<li><a href="https://hai.stanford.edu/ai-definitions/what-is-an-open-weight-model">What is an Open-Weight Model? - Stanford HAI</a></li>
<li><a href="https://www.tinker.com/">Tinker — Play with AI , bring your ideas to life</a></li>

</ul>
</details>

**Discussion**: Community comments express enthusiasm for Inkling&\#x27;s audio capabilities and local deployment potential, with one user noting it might be a leading open-weight model from US-based Thinking Machines. Another comment praises the business model of offering open base models for fine-tuning on Tinker, enabling enterprises to own customized models at lower cost. Overall sentiment is positive, focusing on practical applications.

**Tags**: `#AI`, `#open-weights`, `#multimodal`, `#fine-tuning`, `#HN`

---

<a id="item-5"></a>
## [Claude web\_fetch exploit leaks user memories](https://simonwillison.net/2026/Jul/15/claude-web-fetch-exfiltration/#atom-everything) ⭐️ 8.0/10

Security researcher Ayush Paul discovered a prompt injection attack that bypasses Claude&\#x27;s web\_fetch tool protections, allowing attackers to extract private user memories such as name, location, and employer by tricking the AI into following malicious links embedded in fetched pages. This attack demonstrates a practical bypass of Anthropic&\#x27;s carefully designed defenses, underscoring that even sophisticated protections against the &\#x27;lethal trifecta&\#x27; can be circumvented by creative exploits. It affects all Claude users who have enabled memories and web\_fetch, and highlights the ongoing challenge of securing AI agents against data exfiltration. The attack relied on a honeypot webpage that presented a fake authentication system requiring the agent to navigate alphabetically through user profile URLs. Anthropic declined a bug bounty claim, stating they had already internally identified the vulnerability, and subsequently fixed the issue by preventing web\_fetch from following additional links retrieved within fetched content.

rss · Simon Willison · Jul 15, 14:21

**Background**: Prompt injection attacks exploit the ability of large language models to follow instructions embedded in untrusted content. When an AI agent has the &\#x27;lethal trifecta&\#x27;—access to private data, ability to process untrusted input, and a tool that can communicate externally—attackers can trick it into revealing sensitive information. Claude&\#x27;s web\_fetch tool was designed with restrictions that only allow fetching URLs that were either directly entered by the user or returned from its web\_search tool, to prevent this. However, the loophole allowed following links within fetched pages, enabling the data exfiltration attack.

<details><summary>References</summary>
<ul>
<li><a href="https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/">The lethal trifecta for AI agents: private data, untrusted content, and external communication</a></li>
<li><a href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool">Web fetch tool - Claude Platform Docs</a></li>
<li><a href="https://simonwillison.net/2025/Sep/10/claude-web-fetch-tool/">Claude API: Web fetch tool</a></li>

</ul>
</details>

**Tags**: `#AI safety`, `#prompt injection`, `#security vulnerability`, `#Claude`, `#exfiltration`

---

<a id="item-6"></a>
## [Lockless MPSC FIFO queues for io\_uring in Linux 7.2](https://lwn.net/Articles/1081871/) ⭐️ 8.0/10

Linux kernel 7.2&\#x27;s io\_uring subsystem will replace its current lockless linked-list \(llist\) task tracking with a lockless multi-producer, single-consumer \(MPSC\) FIFO queue, resulting in notable performance gains. This change improves fairness and reduces cache contention for high-performance I/O workloads, directly benefiting applications using io\_uring for asynchronous I/O. The new queue uses a tail pointer and a stub sentinel node to maintain FIFO order without the need for list reversal, and avoids the retry loop and cache-line bouncing inherent in the old head-based llist approach.

rss · LWN.net · Jul 15, 13:35

**Background**: io\_uring is a Linux kernel interface for asynchronous I/O, using shared ring buffers between userspace and kernel. It currently tracks work items using a lockless singly linked list \(llist\), which acts as a stack and requires reordering before processing, leading to inefficiencies.

<details><summary>References</summary>
<ul>
<li><a href="https://www.linux.org/threads/lwn-net-lockless-mpsc-fifo-queues-for-io_uring.68933/">News - [LWN.net] [$] Lockless MPSC FIFO queues for io_uring</a></li>

</ul>
</details>

**Tags**: `#linux kernel`, `#io\_uring`, `#lockless data structures`, `#performance`, `#MPSC queue`

---

<a id="item-7"></a>
## [Disentangling Convolutional Neurons via Hadamard Product Analysis](https://www.reddit.com/r/MachineLearning/comments/1uwya70/mechanistic_interpretability_a_first_paper_on/) ⭐️ 8.0/10

The author proposes a novel technique to interpret neurons in Inceptionv1 by computing the Hadamard product of the receptive field and weights, then clustering to reveal monosemantic feature clusters like cars, cats, and dogs. This work is an important contribution to mechanistic interpretability, providing a new method to analyze convolutional neurons at a fine-grained level. It could help researchers better understand and verify the internal representations of vision models, advancing AI safety. The analysis revealed that low-valued clusters \(e.g., letters\) had all their dependent neurons firing on the same concept, with positive and negative weights evenly distributed to reduce the sum, suggesting deliberate gradient descent behavior. The method was applied to the mixed4e layer of Inceptionv1.

reddit · r/MachineLearning · /u/narang\_27 · Jul 15, 06:59

**Background**: Mechanistic interpretability aims to reverse-engineer neural networks by understanding their internal algorithms and circuits. Inceptionv1 is a convolutional neural network architecture that uses 1x1 convolutions to reduce dimensionality. The Hadamard product is an element-wise multiplication operation used here to combine receptive field and weight information.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mechanistic_interpretability">Mechanistic interpretability</a></li>
<li><a href="https://en.wikipedia.org/wiki/Hadamard_product_%28matrices%29">Hadamard product (matrices) - Wikipedia</a></li>
<li><a href="https://medium.com/@karuneshu21/implement-inception-v1-in-pytorch-66bdbb3d0005">Implement Inception - v 1 in PyTorch | by Karunesh Upadhyay | Medium</a></li>

</ul>
</details>

**Tags**: `#mechanistic interpretability`, `#convolutional neural networks`, `#interpretability`, `#AI safety`, `#deep learning`

---

<a id="item-8"></a>
## [7 Major Smartphone On-Device AI Models Registered in China](https://mp.weixin.qq.com/s/5MTWh4pWVAlL71RQbU-Udg) ⭐️ 8.0/10

Seven on-device language models from Apple, Huawei, OPPO, vivo, Xiaomi, Samsung, and ZTE were officially registered with China&\#x27;s Cyberspace Administration on July 8, 2024, covering their respective AI assistants. This regulatory milestone signals that major smartphone AI features can be deployed compliantly in China, accelerating on-device AI adoption and potentially setting a precedent for AI governance. The registered models include Apple Intelligence, Huawei Xiaoyi AI Large Model, OPPO AndesGPT, vivo BlueMind Intelligent Large Model, Xiaomi Hyper AI, and Samsung Galaxy AI, all designed for on-device use.

telegram · zaihuapd · Jul 15, 08:06

**Background**: On-device AI models run directly on smartphones rather than in the cloud, offering faster response and better privacy. Chinese regulators require registration for AI products to ensure safety and compliance with laws.

<details><summary>References</summary>
<ul>
<li><a href="https://juejin.cn/post/7413629689255182390">juejin.cn/post/7413629689255182390</a></li>
<li><a href="https://www.53ai.com/news/zhinengyingjian/2024070758924.html">【不看后悔】一文梳理 端 侧 模 型 和小 模 型 - 53AI-AI...</a></li>
<li><a href="https://www.aibase.com/tool/22425">AndesGPT -Personalized and exclusive intelligent experience</a></li>

</ul>
</details>

**Tags**: `#AI regulation`, `#on-device AI`, `#mobile AI`, `#China`

---

<a id="item-9"></a>
## [Chinese retail vertical segmentation ends as players converge](https://mp.weixin.qq.com/s/dAHAVxglD-F1RovjcvqCRw) ⭐️ 8.0/10

A research report based on 257 interviews and 5,224 surveys reveals that vertical segmentation in Chinese retail has ended, with Sam&\#x27;s Club, snack discount stores, instant retail platforms, and Pinduoduo now directly competing for the same household spending. Sam&\#x27;s Club&\#x27;s annual revenue in China is estimated at 180–200 billion yuan, snack store chains have nearly 40,000 outlets, and Pinduoduo&\#x27;s Duoduo Maicai has around 300 billion yuan in sales, potentially reaching 400 billion yuan this year. This convergence signals a fundamental shift in China&\#x27;s retail landscape, where traditional format boundaries dissolve and trust and physical proximity become decisive factors. For consumers and businesses alike, understanding this new competitive dynamic is essential for strategic decision-making. The research found that 48% of respondents plan to control spending, and when shopping offline, distance is more important than price—for food and other ingestible products, excessively low prices actually trigger safety concerns, making trust the primary competitive factor.

telegram · zaihuapd · Jul 15, 09:01

**Background**: Chinese retail has historically been segmented by format and price range, with different players serving distinct consumer segments. However, with economic slowdown and shifting consumer behavior, boundaries have blurred: premium warehouse clubs like Sam&\#x27;s Club, ultra-low-cost e-commerce platforms like Pinduoduo, convenience-focused instant retail, and price-aggressive snack discount stores now all target the same household budget. Instant retail enables delivery within 30–60 minutes, and Duoduo Maicai \(Pinduoduo&\#x27;s community group-buying arm\) has expanded rapidly across hundreds of cities.

<details><summary>References</summary>
<ul>
<li><a href="https://www.linkedin.com/posts/koppitz_instant-retail-in-china-how-are-aldi-china-activity-7423848168498397184-Wg4g">Multinational brands adopt instant retail in China with local... | LinkedIn</a></li>
<li><a href="https://en.jiemian.com/article/5833006.html">Home to the farm: Pinduoduo founder moves upstream-Jiemian Global</a></li>
<li><a href="https://asia.nikkei.com/spotlight/comment/china-discount-snack-chain-draws-crowds-of-frugal-shoppers">China discount snack chain draws crowds of frugal... - Nikkei Asia</a></li>

</ul>
</details>

**Tags**: `#retail`, `#China`, `#e-commerce`, `#consumer behavior`, `#market research`

---

<a id="item-10"></a>
## [Google and Epic Drop Motion, Third-Party App Stores Coming to Google Play](https://www.theverge.com/policy/965792/google-epic-withdraw-injunction-third-party-app-stores-coming-google-play) ⭐️ 8.0/10

Google and Epic Games have jointly withdrawn a motion to modify a permanent U.S. court injunction, forcing Google to allow third-party app stores on Google Play starting July 22, 2025. This marks a major shift in Android&\#x27;s app distribution landscape, potentially increasing competition and lowering barriers for alternative app stores, which could impact Google&\#x27;s dominant position and revenue from the Play Store. Third-party stores must pay an annual $5,000 security and policy review fee, cannot distribute outside the U.S., and must be open to developers with clear trust and safety policies. Outside the U.S., Google plans to use its upcoming &\#x27;Registered App Store&\#x27; sideloading program later this year.

telegram · zaihuapd · Jul 15, 11:15

**Background**: Sideloading on Android refers to installing apps without using the Google Play Store, typically via APK files. In the ongoing antitrust battle, Epic Games sued Google over its app store policies. The new &\#x27;Registered App Store&\#x27; program by Google will offer a simplified installation UI for certified stores outside the U.S., with no transaction fees.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Sideloading">Sideloading - Wikipedia</a></li>
<li><a href="https://www.androidauthority.com/google-epic-changes-registered-app-stores-3646743/">Registered App Stores coming to Android this year - Android Authority</a></li>

</ul>
</details>

**Tags**: `#Android`, `#Google Play`, `#Epic Games`, `#反垄断`, `#应用商店`

---

<a id="item-11"></a>
## [Telegram Launches Serverless Platform for Bots and Mini Apps](https://core.telegram.org/bots/serverless) ⭐️ 8.0/10

Telegram has officially launched a serverless platform that allows developers to run backend code for bots and Mini Apps directly on Telegram&\#x27;s infrastructure, eliminating the need to manage servers. Deployments are done via a single command: npx tgcloud push. This significantly lowers the barrier for bot development, as developers no longer need to set up and scale their own servers. It also integrates tightly with Telegram&\#x27;s Bot API, potentially improving performance and reliability for millions of bots. The code runs in an isolated V8 sandbox close to the Bot API and includes a built-in SQLite database. Developers write standard JavaScript modules and deploy with a single command.

telegram · zaihuapd · Jul 15, 16:00

**Background**: Serverless computing allows developers to run code without provisioning or managing servers. Telegram&\#x27;s platform specifically uses V8 sandbox isolation to securely execute untrusted JavaScript code, similar to how Cloudflare Workers or AWS Lambda operate. This launch extends Telegram&\#x27;s bot ecosystem by offering a managed runtime environment.

<details><summary>References</summary>
<ul>
<li><a href="https://www.generative.inc/ai-agent-sandboxes-the-infrastructure-layer-every-builder-needs-to-understand">AI Agent Sandboxes : Infrastructure Guide 2026 | Generative, Inc.</a></li>
<li><a href="https://www.aimadetools.com/blog/cloudflare-sandbox-ai-agents/">Cloudflare Sandbox for AI Agents: Secure Code Execution at the Edge</a></li>

</ul>
</details>

**Tags**: `#serverless`, `#telegram`, `#bots`, `#platform`, `#deployment`

---