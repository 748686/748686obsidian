---
layout: default
title: "Horizon Summary: 2026-07-30 (EN)"
date: 2026-07-30
lang: en
---

> From 41 items, 15 important content pieces were selected

---

1. [GitHub Stacked PRs Now in Public Preview](#item-1) ⭐️ 9.0/10
2. [OpenAI GPT-5.6 Luna price cut 80%](#item-2) ⭐️ 9.0/10
3. [Kimi K3 Open-Weight Model Reaches Frontier with Novel Architecture](#item-3) ⭐️ 9.0/10
4. [Claude AI Weakens NIST Post-Quantum Candidate HAWK in 60 Hours](#item-4) ⭐️ 9.0/10
5. [Google DeepMind Disbands AlphaFold Team, Core Members Move to Anthropic](#item-5) ⭐️ 9.0/10
6. [Gemini Robotics 2 Enables Whole-Body Robot Intelligence](#item-6) ⭐️ 8.0/10
7. [UEFA and 55 associations boycott FIFA competitions](#item-7) ⭐️ 8.0/10
8. [Muon Mystery Solved, Old Results Now Inconsistent](#item-8) ⭐️ 8.0/10
9. [Economic Benefit of Refactoring Analyzed](#item-9) ⭐️ 8.0/10
10. [GCC Steering Committee Announces AI Policy](#item-10) ⭐️ 8.0/10
11. [Professor loses three PhD candidates over review process frustrations](#item-11) ⭐️ 8.0/10
12. [ByteDance Merges Feishu into Doubao and Volcano Engine in Major To B Restructuring](#item-12) ⭐️ 8.0/10
13. [USCC Delegation Denied Meetings with Huawei, DeepSeek in China](#item-13) ⭐️ 8.0/10
14. [Australia sues Telegram over extremist content, faces $54.6M fine](#item-14) ⭐️ 8.0/10
15. [EU launches AI gigafactory tender to mobilize 300B euros](#item-15) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [GitHub Stacked PRs Now in Public Preview](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/) ⭐️ 9.0/10

GitHub has launched Stacked PRs in public preview, allowing developers to break large changes into small, reviewable pull requests organized in a stack. This is a major workflow change for GitHub, enabling incremental development and reviews, which can improve code quality and developer productivity. It exposes a wider audience to stacked workflows, potentially transforming how large features are shipped. Stacked PRs are an ordered series of pull requests each representing a focused layer of a change, with CLI \(gh-stack\) and UI support. However, users have reported issues with merging entire stacks and re-approval requirements when using squash-and-merge with required reviews.

hackernews · tomzorz · Jul 30, 16:26 · [Discussion](https://news.ycombinator.com/item?id=49112232)

**Background**: Traditionally, pull requests are monolithic, making large changes hard to review. Stacked PRs allow splitting a large feature into smaller, dependent PRs that can be reviewed and merged incrementally. This workflow has been popular in some open-source communities but lacked native GitHub support until now.

<details><summary>References</summary>
<ul>
<li><a href="https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/">Stacked pull requests are now in public preview - GitHub Changelog</a></li>
<li><a href="https://github.github.com/gh-stack/">GitHub Stacked PRs | GitHub Stacked PRs</a></li>
<li><a href="https://www.reddit.com/r/programming/comments/1sl4erj/github_stacked_prs/">r/programming on Reddit: GitHub Stacked PRs</a></li>

</ul>
</details>

**Discussion**: The community response is mixed: notable developer steveklabnik praised it as one of the biggest changes to GitHub, while user matharmin reported bugs like broken stack merging. The GitHub team acknowledged issues and invited feedback, aiming to fix them soon.

**Tags**: `#github`, `#pull-requests`, `#developer-tools`, `#workflow`, `#version-control`

---

<a id="item-2"></a>
## [OpenAI GPT-5.6 Luna price cut 80%](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) ⭐️ 9.0/10

OpenAI announced an 80% price reduction for GPT-5.6 Luna, its fastest and most affordable model, alongside 15% efficiency gains from kernel optimizations and experiments. This drastic cost reduction reshapes AI model economics, making high-quality inference accessible at a fraction of previous cost, and signals a new era of falling prices after a year of increases. The 80% cut means Luna is now 5x cheaper, achieved through kernel work reducing serving cost by 20% and token-generation efficiency gains over 15%. This applies to both API and consumer usage.

hackernews · tedsanders · Jul 30, 17:15 · [Discussion](https://news.ycombinator.com/item?id=49112867)

**Background**: GPT-5.6 is a family of models from OpenAI released in July 2026, with three variants: Luna \(cheapest\), Terra \(balanced\), and Sol \(flagship\). Luna was already very capable and affordable; this update further slashes costs dramatically.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/GPT-5.6">GPT-5.6 - Wikipedia</a></li>
<li><a href="https://openai.com/index/gpt-5-6/">GPT‑5.6: Frontier intelligence that scales with ... - OpenAI</a></li>
<li><a href="https://developers.openai.com/api/docs/models/gpt-5.6-luna">GPT-5.6 Luna Model | OpenAI API</a></li>

</ul>
</details>

**Discussion**: The community expressed shock and excitement, with comments noting the transition feels like dial-up to broadband and speculation about billions in monthly savings for inference providers. Some highlighted the difficulty of choosing models optimally.

**Tags**: `#GPT-5.6`, `#OpenAI`, `#AI cost reduction`, `#language models`, `#price-performance`

---

<a id="item-3"></a>
## [Kimi K3 Open-Weight Model Reaches Frontier with Novel Architecture](https://www.reddit.com/r/MachineLearning/comments/1vaysjf/how_kimi_k3_engineered_its_way_to_the_frontier_r/) ⭐️ 9.0/10

Moonshot AI released Kimi K3, an open-weight large language model that ranks fourth among 580 models, behind only Claude Opus 5, Fable 5, and GPT-5.6 Sol. It introduces three key innovations: Kimi Delta Attention replacing KV cache with a 128×128 matrix per head, Quantile Balancing for load balancing 896 experts per layer, and AgentENV, a Firecracker microVM runtime for reinforcement learning training. Kimi K3 demonstrates that open-weight models can compete with the best proprietary frontier models, potentially accelerating AI research and deployment. Its architectural innovations—especially the memory-efficient attention and hyperparameter-free load balancing—could influence future model designs across the industry. Kimi K3 uses Kimi Delta Attention in 69 of 93 layers, reducing the memory footprint for a 1M-token context from 104.6 GiB to 27.2 GiB. Quantile Balancing computes biases directly from router score margins in a single batch, avoiding the fixed-step bias nudging used by DeepSeek-V3. AgentENV created 51 million sandboxes with 133 ms checkpoints and 49 ms resumes during RL training.

reddit · r/MachineLearning · /u/noninertialframe96 · Jul 30, 16:37

**Background**: Large language models often use KV cache to store attention key-value pairs, which grows linearly with context length, limiting long-context performance. Mixture-of-Experts \(MoE\) models use multiple specialized sub-networks \(experts\) activated per token, requiring load balancing to ensure all experts are utilized evenly. Reinforcement learning from human feedback \(RLHF\) or agentic RL trains models by interacting with environments, which traditionally requires dedicated infrastructure that is expensive and slow.

<details><summary>References</summary>
<ul>
<li><a href="https://jianyuh.github.io/attention/2025/12/13/KDA.html">Linear Attention : Kimi Delta Attention | Jianyu Huang’s Blog</a></li>
<li><a href="https://openathena.ai/blog/quantile-balancing/">Mixture of Experts Quantile Balancing: Validated at 32B-A5B (1e22 FLOPs) Scale | Open Athena</a></li>
<li><a href="https://github.com/kvcache-ai/AgentENV">GitHub - kvcache-ai/AgentENV: AgentENV (AENV) is a ...</a></li>

</ul>
</details>

**Tags**: `#attention mechanisms`, `#mixture of experts`, `#large language models`, `#model efficiency`, `#open-source`

---

<a id="item-4"></a>
## [Claude AI Weakens NIST Post-Quantum Candidate HAWK in 60 Hours](https://startupfortune.com/claude-mythos-broke-hawk-and-the-nist-post-quantum-timeline-may-not-survive-it/) ⭐️ 9.0/10

Anthropic&\#x27;s Claude Mythos Preview model discovered a critical weakness in the NIST post-quantum digital signature algorithm HAWK, reducing its effective key strength by half. The attack took approximately 60 hours and cost $100,000 in API fees, whereas human experts had missed it for two years. This demonstrates that AI can outperform human cryptanalysts in finding vulnerabilities in post-quantum cryptographic candidates, potentially reshaping the NIST standardization timeline. It underscores the need for cryptographic agility and reliance on proven standards rather than waiting for perfect algorithms. The attack targets HAWK-256, reducing its security from 2^64 to 2^38 operations, but it does not run in polynomial time, so larger key sizes remain secure. Additionally, the model improved the best known attack on a 7-round version of AES-128, though full AES-128 \(10 rounds\) is unaffected.

telegram · zaihuapd · Jul 30, 05:47

**Background**: HAWK is a lattice-based digital signature scheme and the only such candidate in NIST&\#x27;s Round 3 of the &\#x27;Additional Digital Signatures&\#x27; phase for post-quantum cryptography. NIST is standardizing algorithms resistant to quantum computer attacks, following a 2026 executive order requiring federal agencies to migrate to quantum-resistant cryptography by 2030-2031.

<details><summary>References</summary>
<ul>
<li><a href="https://www.techtimes.com/articles/321876/20260728/ai-cracks-post-quantum-cipher-60-hours-after-two-years-human-review-failed.htm">AI Cracks Post-Quantum Cipher in 60 Hours After Two Years of Human Review Failed</a></li>
<li><a href="https://www.csoonline.com/article/4202920/mythos-takes-its-first-shot-at-post-quantum-cryptography.html">Anthropic finds weakness in Hawk post-quantum digital signature algorithm | CSO Online</a></li>
<li><a href="https://en.wikipedia.org/wiki/NIST_Post-Quantum_Cryptography_Standardization">NIST Post-Quantum Cryptography Standardization</a></li>

</ul>
</details>

**Tags**: `#AI`, `#密码学`, `#后量子密码学`, `#NIST`, `#HAWK`

---

<a id="item-5"></a>
## [Google DeepMind Disbands AlphaFold Team, Core Members Move to Anthropic](https://www.ft.com/content/61b2953d-ee0d-45de-af6e-a9c1cf524b33?syn-25a6b1a6=1) ⭐️ 9.0/10

Google DeepMind has disbanded its Nobel Prize-winning AlphaFold research team as part of a strategic shift, with core members John Jumper, Jonas Adler, and Alexander Pritzel moving to rival AI company Anthropic. This move signals an intensifying talent war in AI research, as DeepMind reallocates resources toward large language models and other projects while Anthropic gains top-tier structural biology expertise. Nearly a quarter of AlphaFold&\#x27;s original paper authors have left the company entirely, with others reassigned to projects like Gemini, enzyme design, nuclear fusion, and Isomorphic Labs.

telegram · zaihuapd · Jul 30, 07:45

**Background**: AlphaFold is an AI system developed by Google DeepMind that predicts protein structures with high accuracy, winning the Nobel Prize in Chemistry in 2024. It was a breakthrough in computational biology, enabling rapid understanding of protein folding. DeepMind&\#x27;s new research strategy focuses on large language models and other frontier AI applications, while Isomorphic Labs is an Alphabet subsidiary focused on AI-driven drug discovery.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/AlphaFold">AlphaFold - Wikipedia</a></li>
<li><a href="https://deepmind.google/science/alphafold/">AlphaFold — Google DeepMind</a></li>
<li><a href="https://en.wikipedia.org/wiki/Isomorphic_Labs">Isomorphic Labs - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#AlphaFold`, `#DeepMind`, `#Anthropic`, `#AI Research`, `#Talent Movement`

---

<a id="item-6"></a>
## [Gemini Robotics 2 Enables Whole-Body Robot Intelligence](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) ⭐️ 8.0/10

Google DeepMind released Gemini Robotics 2 on July 30, 2026, a set of three vision-language-action models that enable whole-body control, fine dexterity, and multi-robot collaboration for humanoid robots. This release moves robotics beyond table-top manipulation to full-body coordination, representing a significant step toward versatile humanoid robots that can operate in real-world environments. It showcases the integration of large multimodal AI with physical action, potentially accelerating the deployment of robots in homes and workplaces. Gemini Robotics 2 is based on Gemini 2.0 and ships as three separate models with different access levels, currently restricted to trusted testers like Boston Dynamics. The models convert vision and language input into motor commands, enabling whole-body tasks like walking, manipulation, and teamwork.

hackernews · ai2027 · Jul 30, 15:15 · [Discussion](https://news.ycombinator.com/item?id=49111237)

**Background**: Vision-Language-Action \(VLA\) models are AI systems that process visual and textual inputs to directly output robotic actions. Previous robotics models often focused on isolated skills like grasping or navigation. Gemini Robotics 2 extends this to whole-body control, meaning the robot uses its entire body—legs, torso, arms, hands—to perform coordinated tasks. The previous version, Gemini Robotics, was launched in March 2025 and focused on table-top manipulation.

<details><summary>References</summary>
<ul>
<li><a href="https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/">Gemini Robotics 2 brings whole body intelligence to robots</a></li>
<li><a href="https://en.wikipedia.org/wiki/Gemini_Robotics">Gemini Robotics</a></li>
<li><a href="https://www.marktechpost.com/2026/07/30/google-deepmind-gemini-robotics-2-whole-body-control-dexterity-multi-robot-collaboration/">Google DeepMind Ships Three Physical AI Models For Whole Body ...</a></li>

</ul>
</details>

**Discussion**: Community comments express excitement about Google DeepMind&\#x27;s broad AI portfolio and the potential for rapid progress, but also skepticism about current robot speed and actuator quality. Some users request honest assessments of real-world capabilities, while others compare the slow but promising start to early LLMs.

**Tags**: `#AI`, `#Robotics`, `#DeepMind`, `#Multimodal AI`, `#Gemini`

---

<a id="item-7"></a>
## [UEFA and 55 associations boycott FIFA competitions](https://www.uefa.com/news-media/news/02a7-213a92896eb0-54dfbf454e3b-1000--statement-on-behalf-of-uefa-and-its-55-national-associations/) ⭐️ 8.0/10

UEFA and its 55 national associations have announced they will not participate in FIFA competitions, citing governance concerns and investor influence. This represents a major rift in international football governance, potentially leading to competing tournaments and reshaping the sport&\#x27;s global structure. The boycott stems from FIFA&\#x27;s plans to expand the World Cup to 48 or even 64 teams and allow external investors ownership in competitions.

hackernews · dickfickling · Jul 30, 18:40 · [Discussion](https://news.ycombinator.com/item?id=49113929)

**Background**: FIFA is the global governing body for football, while UEFA governs European football. Historically, UEFA has been a powerful bloc within FIFA. Recent FIFA proposals have raised concerns about corruption and commercial overreach.

**Discussion**: The Hacker News community expresses strong support for UEFA&\#x27;s stance, with many calling for the removal of FIFA President Infantino. Commenters worry that external investment will turn football into a pure business.

**Tags**: `#sports`, `#governance`, `#FIFA`, `#UEFA`, `#corruption`

---

<a id="item-8"></a>
## [Muon Mystery Solved, Old Results Now Inconsistent](https://www.quantamagazine.org/physicists-solve-a-muon-mystery-now-old-results-dont-add-up-20260729/) ⭐️ 8.0/10

Physicists have resolved the decades-old muon g-2 anomaly by showing that lattice QCD calculations align the theoretical prediction with the Fermilab experimental measurement. This resolution, however, invalidates older results from the Brookhaven experiment, which now show a significant discrepancy. The resolution strengthens the Standard Model of particle physics, which had been challenged by the apparent anomaly. It also forces a re-evaluation of previous experimental results, potentially altering our understanding of fundamental particle properties. The key breakthrough came from improved lattice QCD calculations that reduced theoretical uncertainties, making the predicted value of the muon&\#x27;s anomalous magnetic moment \(g-2\) consistent with the Fermilab result. The Brookhaven measurement, once considered the harbinger of new physics, now lies 4.2 standard deviations away from the combined theoretical and experimental consensus.

hackernews · ibobev · Jul 30, 15:22 · [Discussion](https://news.ycombinator.com/item?id=49111305)

**Background**: The muon is a particle similar to an electron but about 200 times heavier. Its magnetic moment can be measured extremely precisely, and any deviation from the Standard Model prediction could indicate new particles. The Muon g-2 experiment at Fermilab measured the muon&\#x27;s anomalous magnetic moment to an unprecedented precision of 0.14 parts per million. For years, the experimental value disagreed with theoretical calculations, sparking hope for new physics. Recent lattice QCD computations have revised the theoretical value, eliminating the discrepancy.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Muon_g-2">Muon g-2 - Wikipedia</a></li>
<li><a href="https://muon-g-2.fnal.gov/">Fermilab | Muon g-2</a></li>
<li><a href="https://news.fnal.gov/2025/06/muon-g-2-most-precise-measurement-of-muon-magnetic-anomaly/">Muon g-2 announces most precise measurement of the magnetic ...</a></li>

</ul>
</details>

**Discussion**: Comments ranged from philosophical reflections on scientific paradigms to skepticism about unknown systematic errors. Some found relief in not having dedicated years to the problem, while a humorous comment suggested parallel universes might reconcile the old results.

**Tags**: `#physics`, `#muon`, `#particle physics`, `#quantum mechanics`

---

<a id="item-9"></a>
## [Economic Benefit of Refactoring Analyzed](https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html) ⭐️ 8.0/10

Martin Fowler&\#x27;s article provides a quantitative analysis of the economic benefits of refactoring, especially when assisted by AI tools, using real measurements to demonstrate cost savings and quality improvements. This analysis grounds AI-assisted software engineering in concrete data, moving beyond vague commentary to offer actionable insights for developers and organizations considering AI adoption. The article likely compares token consumption and other metrics before and after refactoring, showing that AI-assisted refactoring can reduce costs and improve code quality.

hackernews · javaeeeee · Jul 30, 15:10 · [Discussion](https://news.ycombinator.com/item?id=49111176)

**Background**: Refactoring is restructuring existing code without changing external behavior to improve internal structure. With AI coding assistants like GitHub Copilot, understanding the economic impact of refactoring is crucial for teams adopting these tools.

**Discussion**: Commenters appreciate the grounded, quantitative approach, contrasting it with vague AI commentary. Some note best practices for human developers are being rediscovered for AI, and others highlight the need for human oversight in agentic refactoring.

**Tags**: `#refactoring`, `#software engineering`, `#economics`, `#AI-assisted development`, `#best practices`

---

<a id="item-10"></a>
## [GCC Steering Committee Announces AI Policy](https://lwn.net/Articles/1086041/) ⭐️ 8.0/10

The GCC steering committee has announced a policy restricting AI-generated contributions, citing copyright and open-source ethics concerns. This policy sets a precedent for how major open-source projects handle AI contributions, potentially influencing the broader free software ecosystem. The policy explicitly addresses contributions from large language models, noting that such output may not be copyrightable, which conflicts with the GPL&\#x27;s reliance on copyright.

hackernews · arto · Jul 30, 11:45 · [Discussion](https://news.ycombinator.com/item?id=49108685)

**Background**: GCC \(GNU Compiler Collection\) is a core component of the GNU project and is licensed under the GPL, which uses copyright to enforce copyleft principles. If AI-generated code is not copyrightable, it cannot be licensed under the GPL, potentially undermining the legal basis of free software.

**Discussion**: Community comments express a mix of support and concern. Some appreciate the policy&\#x27;s guidance for contributors, while others debate the copyright implications for free software, with one comment quoting &\#x27;the true purpose of AI is to allow wealth to access skill without allowing skill to access wealth.&\#x27;

**Tags**: `#GCC`, `#AI Policy`, `#Open Source`, `#GNU`, `#Contributions`

---

<a id="item-11"></a>
## [Professor loses three PhD candidates over review process frustrations](https://www.reddit.com/r/MachineLearning/comments/1vawwb8/i_have_lost_three_and_a_half_potential_phd/) ⭐️ 8.0/10

An early-career assistant professor reported losing three and a half potential PhD students because the conference review process discouraged them from pursuing research careers. The students were talented undergraduates who contributed to strong papers that received positive reviews but were still rejected and trapped in resubmission cycles. This highlights a systemic problem in ML academic publishing where the review process can deter talented newcomers from entering the field. It underscores the need for reform in peer review to reduce randomness and bias, as the current system may be harming the future of research. The professor has over 10 years of experience at top-tier conferences and considers the papers well above the bar. One paper received four unanimous weak accepts but was rejected, leading to endless resubmissions where addressing previous concerns only invited more random criticisms.

reddit · r/MachineLearning · /u/AffectionateLife5693 · Jul 30, 15:30

**Background**: The &quot;big three&quot; machine learning conferences typically refer to NeurIPS, ICML, and ICLR, which are highly competitive and have significant influence on academic careers in ML. The peer review process for these conferences is known to be noisy and sometimes arbitrary, with papers often requiring multiple resubmissions.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/khairulislam/ML-conferences">GitHub - khairulislam/ML-conferences: List of ML conferences ...</a></li>
<li><a href="https://conferencedatabase.com/blog/machine-learning-conferences">Top 7 Machine Learning Conferences for 2025-2026</a></li>
<li><a href="https://www.datacamp.com/blog/top-machine-learning-conferences">Top 11 Machine Learning Conferences for 2026 - DataCamp</a></li>

</ul>
</details>

**Tags**: `#peer review`, `#academic publishing`, `#machine learning`, `#PhD students`

---

<a id="item-12"></a>
## [ByteDance Merges Feishu into Doubao and Volcano Engine in Major To B Restructuring](https://news.qq.com/rain/a/20260730A03CAP00) ⭐️ 8.0/10

ByteDance has restructured its enterprise business by merging Feishu&\#x27;s product team with Doubao&\#x27;s product team into a new &\#x27;Doubao Product Team&\#x27; led by Zhao Qi, and integrating Feishu&\#x27;s market, sales, and customer service teams with Volcano Engine to form a &\#x27;Creativity Service Platform&\#x27; led by Tan Dai. This marks ByteDance&\#x27;s largest To B restructuring since its founding, signaling a strategic push to monetize its consumer AI lead \(Doubao has 330 million users\) in enterprise productivity scenarios. It could reshape China&\#x27;s enterprise software and AI market by tightly coupling collaboration tools with AI assistants and cloud services. Existing Feishu products and services remain unchanged, and the Doubao Enterprise Edition, jointly developed by both teams, is already being internally tested among some Feishu customers. The restructuring places Feishu head Xie Xin under Zhao Qi&\#x27;s leadership for product, and integrates go-to-market functions under Tan De&\#x27;s creativity service platform.

telegram · zaihuapd · Jul 30, 02:55

**Background**: Feishu is ByteDance&\#x27;s enterprise collaboration platform \(known as Lark internationally\), Doubao is its flagship AI chatbot launched in August 2023, which became China&\#x27;s most popular AI assistant with 60 million monthly active users by November 2024, growing to 330 million by May 2026. Volcano Engine is ByteDance&\#x27;s cloud and AI services platform, providing infrastructure for AI model training and deployment. This restructuring aims to better integrate these assets to compete in the enterprise AI market.

<details><summary>References</summary>
<ul>
<li><a href="https://www.eastisread.com/p/bytedance-folds-feishu-teams-into">ByteDance folds Feishu teams into Doubao, Volcano Engine in enterprise AI push</a></li>
<li><a href="https://technode.com/2026/07/30/bytedance-restructures-ai-business-merging-doubao-and-feishu-product-teams/">ByteDance restructures AI business, merging Doubao and Feishu ...</a></li>
<li><a href="https://en.wikipedia.org/wiki/Doubao">Doubao - Wikipedia</a></li>

</ul>
</details>

**Tags**: `#ByteDance`, `#AI Business`, `#Enterprise Software`, `#Organizational Change`, `#Feishu`

---

<a id="item-13"></a>
## [USCC Delegation Denied Meetings with Huawei, DeepSeek in China](https://tech.ifeng.com/c/8v7fL2j6ajG) ⭐️ 8.0/10

In late July 2026, a delegation from the US-China Economic and Security Review Commission \(USCC\) visited Beijing, Hangzhou, and Shanghai, but was collectively denied meetings or site visits by major Chinese tech firms including Huawei, Tencent, Alibaba, Baidu, and DeepSeek. This refusal highlights escalating tensions and distrust between the US and China in the tech sector, potentially impacting future policy recommendations and export controls on AI and semiconductors. It underscores the growing challenge of bilateral engagement on critical technologies. The USCC, an independent legislative branch commission established in 2000, has historically advocated for chip sanctions, expanded entity lists, and AI technology export restrictions against China. This was its first official visit to China since 2019.

telegram · zaihuapd · Jul 30, 03:40

**Background**: The USCC monitors and reports to Congress on national security implications of the US-China economic relationship. DeepSeek is a Chinese AI company founded in 2023 that developed cost-effective, open-weight large language models, disrupting the AI industry and facing export restrictions. Huawei is a leading Chinese telecom and tech firm long targeted by US sanctions.

<details><summary>References</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/US-China_Economic_and_Security_Review_Commission">US-China Economic and Security Review Commission</a></li>
<li><a href="https://en.wikipedia.org/wiki/DeepSeek">DeepSeek</a></li>
<li><a href="https://www.uscc.gov/">Homepage | U.S.- CHINA | ECONOMIC and SECURITY REVIEW COMMISSION</a></li>

</ul>
</details>

**Tags**: `#US-China relations`, `#tech policy`, `#Huawei`, `#DeepSeek`, `#security review`

---

<a id="item-14"></a>
## [Australia sues Telegram over extremist content, faces $54.6M fine](https://www.reuters.com/world/asia-pacific/australia-begins-legal-action-against-telegram-over-alleged-pro-terror-material-2026-07-30/) ⭐️ 8.0/10

Australia&\#x27;s eSafety commissioner has filed a lawsuit against Telegram for failing to remove terrorist-related content, including videos of the Christchurch and Buffalo attacks, potentially resulting in a civil penalty of up to 54.6 million AUD. This case underscores the growing regulatory pressure on encrypted messaging platforms to enforce content moderation, potentially setting a precedent for how governments hold tech companies accountable for user-generated extremist material. According to court documents, between July and October 2025, Australian users reported 12 posts containing terrorist material, but Telegram failed to remove 10 of them and did not ban related accounts.

telegram · zaihuapd · Jul 30, 03:45

**Background**: Telegram is a popular messaging app known for its strong encryption and minimal content moderation. The eSafety Commissioner is Australia&\#x27;s online safety regulator empowered to issue notices requiring removal of illegal content. If found guilty, Telegram&\#x27;s fine would be one of the largest under Australia&\#x27;s 2021 Online Safety Act.

**Tags**: `#platform regulation`, `#content moderation`, `#Telegram`, `#Australia`, `#terrorism`

---

<a id="item-15"></a>
## [EU launches AI gigafactory tender to mobilize 300B euros](https://www.wsj.com/world/europe/eu-opens-call-for-creation-of-local-ai-gigafactories-c286213d) ⭐️ 8.0/10

The European Commission has officially opened a tender for up to seven AI gigafactories, aiming to mobilize around 300 billion euros in investment, with 100 billion euros coming from EU-level funds and participating member states. This initiative signals a strategic push by the EU to build sovereign AI infrastructure and compete with global leaders like the United States and China, potentially reshaping the European tech ecosystem and attracting significant private capital. The tender supports up to seven AI facilities in two phases: site selection and expansion. Bids are due by November 12, 2024, winners announced by July 2027, and facilities must be operational within 18 months of signing.

telegram · zaihuapd · Jul 30, 11:50

**Background**: AI gigafactories are large-scale computing facilities designed to train and run advanced AI models. The EU aims to reduce dependence on non-European cloud and compute providers, and to foster a competitive local AI ecosystem, similar to efforts by the US CHIPS Act and China&\#x27;s AI infrastructure investments.

**Tags**: `#AI`, `#Europe`, `#supercomputing`, `#investment`, `#policy`

---