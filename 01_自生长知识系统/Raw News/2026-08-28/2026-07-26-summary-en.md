---
layout: default
title: "Horizon Summary: 2026-07-26 (EN)"
date: 2026-07-26
lang: en
---

> From 33 items, 10 important content pieces were selected

---

1. [Decker: A Modern Platform Inspired by HyperCard](#item-1) ⭐️ 8.0/10
2. [GrapheneOS Foils Locked Device Data Extraction](#item-2) ⭐️ 8.0/10
3. [EU Proposes Browser Privacy Preference to Replace Cookie Banners](#item-3) ⭐️ 8.0/10
4. [Strongest El Niño to Drive Record 2027 Temperatures](#item-4) ⭐️ 8.0/10
5. [LLM Token Relay Market Fuels Fraud and Abuse](#item-5) ⭐️ 8.0/10
6. [YOLO26n Inference Implemented from Scratch in ARM64 Assembly](#item-6) ⭐️ 8.0/10
7. [Open-weight 4B models near o3-level on Swedish medical QA](#item-7) ⭐️ 8.0/10
8. [DeepSeek Pauses Funding Round After Leak](#item-8) ⭐️ 8.0/10
9. [Claude Shared Links Indexed by Search Engines, Leaking Private Data](#item-9) ⭐️ 8.0/10
10. [SpaceX Halts Falcon 9 Orders Beyond 2028, Bets on Starship](#item-10) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Decker: A Modern Platform Inspired by HyperCard](https://beyondloom.com/decker/) ⭐️ 8.0/10

Decker is a newly developed platform that revives the interactive document authoring experience of HyperCard and classic macOS, allowing users to create interactive documents with a simple interface. Decker matters because it brings back the ease of use and rapid development capabilities of HyperCard to modern systems, potentially enabling a new generation of non-programmers to build interactive applications and documents. Decker builds on the legacy of HyperCard, but it does not require Apple&\#x27;s Classic Environment; it runs on modern operating systems. The platform emphasizes 1-bit graphics and a minimalist design aesthetic.

hackernews · tosh · Jul 26, 18:23 · [Discussion](https://news.ycombinator.com/item?id=49060856)

**Background**: HyperCard was a revolutionary hypermedia system released by Apple in 1987, combining a database with a graphical user interface and a scripting language called HyperTalk. It allowed users to create interactive &\#x27;stacks&\#x27; of cards for a wide range of applications, from games to databases. HyperCard was discontinued in 2004 but remains influential. Decker aims to recreate that experience for contemporary users.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/HyperCard">HyperCard</a></li>
<li><a href="https://hypercard.org/">HyperCard | The software erector set.</a></li>

</ul>
</details>

**Discussion**: Commenters expressed nostalgia for HyperCard and admiration for Decker&\#x27;s concept, but some questioned its practical utility in 2026, noting that while it&\#x27;s a fun nostalgia project, it may not be useful for real-world applications. Others discussed the broader ecosystem of similar tools like FileMaker and Access.

**Tags**: `#HyperCard`, `#Decker`, `#retro computing`, `#low-code`, `#interactive documents`

---

<a id="item-2"></a>
## [GrapheneOS Foils Locked Device Data Extraction](https://discuss.grapheneos.org/d/40700-grapheneos-protections-against-data-extraction-from-locked-devices) ⭐️ 8.0/10

A community discussion highlights how GrapheneOS protects against data extraction from locked devices using features like auto-reboot and duress PIN, which trigger a factory reset or return the device to Before First Unlock \(BFU\) mode. These protections are critical for high-risk users like journalists and activists, as they prevent forensic data extraction even under coercion. This sets a new standard for mobile security and privacy. The auto-reboot feature returns the device to BFU mode after 18 hours of inactivity, while the duress PIN silently wipes the device and triggers a factory reset. Both features prevent decryption key extraction from memory.

hackernews · Cider9986 · Jul 26, 05:57 · [Discussion](https://news.ycombinator.com/item?id=49055169)

**Background**: GrapheneOS is a hardened version of Android focused on security and privacy. When a device is locked, data encryption keys are held in memory; if an attacker can access the device while it&\#x27;s unlocked, they can extract these keys. Auto-reboot and duress PIN ensure the device is locked and keys are inaccessible, even if an adversary forces the user to unlock it.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GrapheneOS">GrapheneOS</a></li>
<li><a href="https://grapheneos.org/features">Features overview | GrapheneOS</a></li>
<li><a href="https://www.androidauthority.com/grapheneos-duress-pin-3584795/">I use a duress PIN to protect my data — here’s how it works and why everyone needs one</a></li>

</ul>
</details>

**Discussion**: The community praised GrapheneOS&\#x27;s protections, with one user noting it helped a journalist protect sources. Others discussed the need for a complete backup solution before wiping, and compared pattern lock entropy to PINs. Some users highlighted that similar protections exist on Apple devices, countering claims that only &\#x27;criminals&\#x27; need such security.

**Tags**: `#security`, `#grapheneos`, `#mobile`, `#privacy`, `#encryption`

---

<a id="item-3"></a>
## [EU Proposes Browser Privacy Preference to Replace Cookie Banners](https://killthecookiebanner.eu/) ⭐️ 8.0/10

The European Commission has proposed a new solution to eliminate cookie banners by allowing users to set their privacy preferences once in the browser, which would then automatically inform websites. This could drastically improve user experience by removing the constant nuisance of cookie consents, and if adopted, would shift the burden of consent management from websites to browsers, making privacy control more user-friendly. The proposal builds on existing technologies like the Global Privacy Control \(GPC\) signal, which already has legal force under some privacy laws, and aims to standardize such signals across all websites.

hackernews · rapnie · Jul 26, 11:53 · [Discussion](https://news.ycombinator.com/item?id=49057175)

**Background**: Cookie banners became widespread after the EU&\#x27;s ePrivacy Directive and GDPR required websites to obtain consent for non-essential cookies. However, many banners are designed to nudge users into accepting, leading to criticism that they fail to provide genuine informed consent. Previous attempts like the Do Not Track \(DNT\) header failed because it was widely ignored by advertisers. The Global Privacy Control \(GPC\) is a newer signal that has legal backing in some jurisdictions.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Global_Privacy_Control">Global Privacy Control</a></li>
<li><a href="https://globalprivacycontrol.org/">Global Privacy Control — Take Control Of Your Privacy</a></li>

</ul>
</details>

**Discussion**: Commenters generally support the idea but express frustration that it took so long. Some argue that click-based consent cannot constitute informed consent, while others point to California&\#x27;s GPC law as a model. There is also criticism that ad industry influence blocked earlier solutions like DNT.

**Tags**: `#privacy`, `#cookie banners`, `#EU regulation`, `#browser settings`, `#web standards`

---

<a id="item-4"></a>
## [Strongest El Niño to Drive Record 2027 Temperatures](https://www.theclimatebrink.com/p/the-strongest-el-nino-ever) ⭐️ 8.0/10

A new analysis warns that the strongest El Niño event on record is developing, which is expected to push global temperatures to unprecedented levels in 2027, with most climate models having underestimated the rate of ocean warming. This event could lead to extreme weather worldwide, intensifying heatwaves, droughts, and floods, and underscores a critical gap between climate model predictions and actual observations, affecting policy and preparedness decisions globally. Global temperature lags El Niño by three to five months, so most of the warming will manifest in 2027, which could become the warmest year on record by a significant margin. The models&\#x27; underestimation of ocean temperatures raises concerns about accelerating climate feedbacks.

hackernews · ndsipa\_pomu · Jul 26, 18:35 · [Discussion](https://news.ycombinator.com/item?id=49060978)

**Background**: El Niño is a climate pattern characterized by unusually warm ocean temperatures in the equatorial Pacific, which affects global weather. It alternates with La Niña \(cooler waters\) and can cause extreme events like heavy rain or drought in different regions. The strength of an El Niño event is measured by sea surface temperature anomalies, and a &\#x27;super El Niño&\#x27; can have outsized impacts.

**Discussion**: Commenters expressed deep concern about model inaccuracies and personal preparedness, with some questioning whether to prepare for deadly heatwaves or heavy rains in Europe. Others highlighted recent multiyear La Niña events and rainfall deficits, and one noted the difficulty of shrinking pollution given the pyramid of wealth.

**Tags**: `#climate change`, `#El Niño`, `#global warming`, `#environmental science`

---

<a id="item-5"></a>
## [LLM Token Relay Market Fuels Fraud and Abuse](https://simonwillison.net/2026/Jul/26/relay-market/#atom-everything) ⭐️ 8.0/10

Matt Lenhard&\#x27;s investigation uncovers a black market for discounted LLM tokens, where resellers use open-source proxy tools like one-api and its fork new-api to pool keys obtained from free trial abuse, stolen credentials, and chargeback attacks. This ecosystem exposes systemic API security weaknesses, threatens LLM provider revenue, and risks causing large bills for developers whose endpoints are exploited. It underscores the urgent need for strict API key caps and spending controls. The proxy services are primarily operated in China, and buyers seek cheap tokens, bypass geo-restrictions, or perform model distillation. The legitimate open-source gateways one-api and new-api are repurposed to load-balance across a pool of illicitly obtained credentials.

rss · Simon Willison · Jul 26, 19:30

**Background**: Large Language Model \(LLM\) providers charge per token for API access, making cost a barrier for heavy users. Resellers exploit this by pooling API keys obtained through free trial abuse, stolen credit cards, or unprotected internal endpoints, offering discounted rates. Open-source proxy software like one-api and its enhanced fork new-api allows managing these key pools and routing requests, making the fraud technically straightforward. This practice is particularly prevalent in China, where many such proxy services are hosted.

<details><summary>References</summary>
<ul>
<li><a href="https://aibit.im/blog/post/new-api-the-next-gen-llm-gateway-ai-asset-manager">New API : The Next-Gen LLM Gateway &amp; AI Asset Manager | AIBit</a></li>
<li><a href="https://www.claudehome.cn/en/articles/comparing-the-top-ai-api-providers-for-coding-and-development-in-2026">Comparing the Top AI API Providers for Coding and Development in...</a></li>

</ul>
</details>

**Tags**: `#security`, `#LLM`, `#API`, `#fraud`, `#proxy`

---

<a id="item-6"></a>
## [YOLO26n Inference Implemented from Scratch in ARM64 Assembly](https://www.reddit.com/r/MachineLearning/comments/1v6w394/i_implemented_the_yolo26n_model_inference_from/) ⭐️ 8.0/10

A Bachelor&\#x27;s project has implemented the full inference pipeline of the YOLO26n object detection model from scratch using ARM64 assembly language and C, without relying on any existing deep learning frameworks. The implementation runs on a Raspberry Pi 4 and incorporates advanced low-level optimizations such as ARM NEON SIMD, Winograd convolution, and cache-aware tiling. This project demonstrates deep understanding of how neural network inference engines work at the hardware level, offering insights into extreme optimization for edge AI devices with limited resources. It pushes the boundaries of what is possible on commodity single-board computers like the Raspberry Pi, potentially enabling real-time object detection without specialized accelerators. The implementation includes operator fusion, custom ARM64 micro-kernels, and attention mechanisms \(PSA module\). The model parameters were extracted and stored in a custom binary format optimized for the inference pipeline, and while detection results are correct, performance gains were lower than expected.

reddit · r/MachineLearning · /u/Forward\_Confusion902 · Jul 26, 06:43

**Background**: YOLO \(You Only Look Once\) is a popular family of real-time object detection models. Running such models on edge devices like the Raspberry Pi typically requires optimized inference frameworks such as TensorFlow Lite or ONNX Runtime. This project instead writes the entire inference code in ARM64 assembly, using techniques like Winograd convolution \(which reduces multiplication count\) and cache-aware tiling \(which improves data locality\) to accelerate computation.

<details><summary>References</summary>
<ul>
<li><a href="https://www.emergentmind.com/topics/winograd-convolution">Winograd Convolution in CNNs</a></li>
<li><a href="https://github.com/pranshutripathi21/memory-bound-kernel-optimizer">pranshutripathi21/memory-bound-kernel-optimizer: Cache - aware tiling ...</a></li>
<li><a href="https://medium.com/data-science/how-pytorch-2-0-accelerates-deep-learning-with-operator-fusion-and-cpu-gpu-code-generation-35132a85bd26">How Pytorch 2.0 Accelerates Deep Learning with Operator Fusion ...</a></li>

</ul>
</details>

**Tags**: `#YOLO`, `#ARM64 Assembly`, `#Edge AI`, `#Inference Optimization`, `#Computer Vision`

---

<a id="item-7"></a>
## [Open-weight 4B models near o3-level on Swedish medical QA](https://www.reddit.com/r/MachineLearning/comments/1v71wds/openweight_4b_models_approach_o3level_medical/) ⭐️ 8.0/10

Small open-weight 4B parameter LLMs \(Gemma4-E4B and Qwen3.5-4B\) achieved 77% accuracy on Swedish medical licensing exam questions without post-training, and Qwen3.5-4B with reasoning reached 87%, approaching the 88% score of o3. This demonstrates that small open-weight models can match closed-source state-of-the-art performance on domain-specific tasks, making advanced medical QA accessible without massive compute or proprietary APIs. It also highlights the rapid pace of improvement in open-source LLMs. The Qwen3.5-4B model performed reasoning entirely in English despite the Swedish prompts, and an early exit intervention from the S-GRPO paper was used to prevent reasoning loops. A reinforcement learning method to shorten reasoning traces yielded only minor gains.

reddit · r/MachineLearning · /u/AccomplishedCat4770 · Jul 26, 11:58

**Background**: The MedQA-SWE dataset is a Swedish multiple-choice question set from medical licensing exams. The o3 model refers to OpenAI&\#x27;s high-performing reasoning model that scored 88% on a subset of these questions. Open-weight models have their weights publicly available for fine-tuning and inference, unlike closed APIs.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2505.07686">S - GRPO : Early Exit via Reinforcement Learning in Reasoning Models</a></li>
<li><a href="https://huggingface.co/datasets/nicher92/medqa-swe">nicher92/ medqa - swe · Datasets at Hugging Face</a></li>
<li><a href="https://aclanthology.org/2024.lrec-main.975.pdf">MedQA - SWE - a Clinical Question &amp; Answer Dataset for Swedish</a></li>

</ul>
</details>

**Tags**: `#LLM`, `#medical-QA`, `#small-models`, `#reasoning`, `#Swedish`

---

<a id="item-8"></a>
## [DeepSeek Pauses Funding Round After Leak](https://www.bloomberg.com/news/articles/2026-07-25/deepseek-said-to-tell-backers-of-funding-pause-after-viral-posts) ⭐️ 8.0/10

DeepSeek has verbally informed some second-round investors to pause signing investment agreements, partly due to founder Liang Wenfeng&\#x27;s displeasure over leaked internal discussions online. This pause signals potential governance challenges at a leading Chinese AI startup and could affect investor confidence and the pace of AI funding in China. DeepSeek completed a $7 billion first round in June 2026 and was planning a second round of at least 10 billion yuan with a pre-money valuation of no less than 480 billion yuan.

telegram · zaihuapd · Jul 26, 01:17

**Background**: DeepSeek, founded in July 2023 by Liang Wenfeng, is a Chinese AI company known for developing cost-effective large language models like DeepSeek-R1. It is backed by High-Flyer and has attracted investors including Tencent, CATL, and the National AI Industry Investment Fund. The company&\#x27;s success has been described as &\#x27;upending AI&\#x27; due to its open-weight models and low training costs.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></li>
<li><a href="https://www.deepseek.com/en/">DeepSeek</a></li>

</ul>
</details>

**Tags**: `#deepseek`, `#ai-funding`, `#china-ai`, `#business-news`

---

<a id="item-9"></a>
## [Claude Shared Links Indexed by Search Engines, Leaking Private Data](https://search.brave.com/search?q=site%3Aclaude.ai%2Fshare&amp;amp;source=android) ⭐️ 8.0/10

Claude&\#x27;s shared conversation links, generated via the &\#x27;share&\#x27; feature, lack a &\#x27;noindex&\#x27; meta tag that would prevent search engine indexing. As a result, Google, Brave, and Bing have indexed these links, exposing private conversations containing sensitive information such as API keys, cryptocurrency wallet details, personal resumes, and social security numbers. This vulnerability exposes highly sensitive user data in a widely adopted AI platform, similar to a past ChatGPT issue that was quickly fixed. Anthropic&\#x27;s failure to address it puts millions of users at risk of identity theft, financial loss, and privacy breaches, undermining trust in AI assistant services. Google has already blocked indexing of these links, but Brave and Bing continue to display them in search results. Anthropic has not yet released a fix; users are advised to manually delete sensitive conversations from the &\#x27;Shared Conversations&\#x27; settings page.

telegram · zaihuapd · Jul 26, 11:16

**Background**: Claude is a conversational AI assistant built by Anthropic. Its &\#x27;share&\#x27; feature creates publicly accessible URLs for conversations, intended for easy sharing between users. Without a &\#x27;noindex&\#x27; meta tag instructing search engines not to index the page, these URLs can be crawled and appear in search results, inadvertently exposing private information to anyone who searches.

<details><summary>References</summary>
<ul>
<li><a href="https://claude.com/">Claude</a></li>
<li><a href="https://en.wikipedia.org/wiki/Noindex">noindex - Wikipedia</a></li>
<li><a href="https://moz.com/learn/seo/robots-meta-directives">What Are Robot Meta Tags ? And How to Implement them - Moz</a></li>

</ul>
</details>

**Tags**: `#privacy`, `#security`, `#Claude`, `#Anthropic`, `#data leak`

---

<a id="item-10"></a>
## [SpaceX Halts Falcon 9 Orders Beyond 2028, Bets on Starship](https://www.bloomberg.com/news/articles/2026-07-23/spacex-is-turning-away-falcon-customers-in-major-bet-on-starship) ⭐️ 8.0/10

SpaceX has stopped accepting new Falcon 9 launch orders for missions after 2028 and discontinued future reservations on its rideshare program, focusing resources on the Starship rocket. This strategic shift could create a launch capacity gap for commercial satellite operators if Starship fails to achieve operational readiness by late 2028, impacting the global space industry&\#x27;s access to orbit. SpaceX is also reducing production of non-reusable Falcon 9 parts. The company may still fly Falcon 9 for U.S. defense and NASA missions, but commercial customers with launch plans beyond 2028 must now wait for Starship.

telegram · zaihuapd · Jul 26, 12:42

**Background**: Falcon 9 is a reusable rocket that has dominated the commercial launch market since 2010, offering reliable and cost-effective access to space. Starship is SpaceX&\#x27;s next-generation fully reusable rocket, designed for heavy payloads and deep space missions, but it is still in development and has not yet completed a successful orbital flight.

<details><summary>References</summary>
<ul>
<li><a href="https://www.ithome.com/0/981/123.htm">星 舰 商 业 化 倒计 时 ， SpaceX 停止接收 2028...</a></li>
<li><a href="https://www.nstc.gov.tw/la/ch/detail/d72d4189-91d4-4bf8-b8d1-785af9a55cb5">國家科學及技術委員會-科技短訊-SpaceX將開闢 Starship ...</a></li>
<li><a href="https://www.spacex.com/launches">SpaceX - Launches</a></li>

</ul>
</details>

**Tags**: `#SpaceX`, `#Starship`, `#Falcon 9`, `#Space Industry`, `#Launch Vehicles`

---