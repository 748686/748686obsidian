---
layout: default
title: "Horizon Summary: 2026-05-19 (ZH)"
date: 2026-05-19
lang: zh
---

> From 33 items, 8 important content pieces were selected

---

1. [埃隆·马斯克败诉山姆·奥特曼与 OpenAI](#item-1) ⭐️ 8.0/10
2. [FBI 寻求全美车牌读取器数据访问权](#item-2) ⭐️ 8.0/10
3. [内核交换子系统获得交换表和闪存友好改进](#item-3) ⭐️ 8.0/10
4. [Hugging Face 用 AI 解析复兴 PapersWithCode](#item-4) ⭐️ 8.0/10
5. [LLM 安全基准测试：许多模型失败](#item-5) ⭐️ 8.0/10
6. [24GB 显存下运行 Qwen 3.6 27B 的最佳 llama.cpp 分支](#item-6) ⭐️ 8.0/10
7. [欧盟 DMA 推动 Firefox 在欧洲新增逾 600 万用户](#item-7) ⭐️ 8.0/10
8. [SpaceX 押注 Starship V3 首飞为 IPO 铺路](#item-8) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [埃隆·马斯克败诉山姆·奥特曼与 OpenAI](https://techcrunch.com/2026/05/18/elon-musk-has-lost-his-lawsuit-against-sam-altman-and-openai/) ⭐️ 8.0/10

陪审团裁定，埃隆·马斯克针对山姆·奥特曼和 OpenAI 的诉讼因提起时间过晚而被驳回，具体认定马斯克本可以在 2019 年或 2021 年就类似的微软交易提出索赔。 这一裁决为挑战 AI 实体从非营利向营利转变的诉讼时效设立了先例，可能影响 AI 行业未来的治理纠纷。 陪审团仅回答是/否问题，因此确切理由未知，但裁决表明，诉讼核心的 2023 年微软交易与早期交易过于相似，导致索赔已过时效。

hackernews · nycdatasci · May 18, 17:38 · [社区讨论](https://news.ycombinator.com/item?id=48182754)

**背景**: 马斯克于 2015 年共同创立了非营利组织 OpenAI，但于 2018 年离开。OpenAI 后来重组为营利性实体，并与微软建立了合作关系。马斯克于 2023 年提起诉讼，指控违约和违反信义义务。该案因诉讼时效问题被驳回。

**社区讨论**: 评论者普遍认同法律结果基于时效问题，但部分人认为 OpenAI 的结构仍应承担后果。大家讨论了非营利向营利转变的先例以及上诉的理由。

**标签**: `#OpenAI`, `#Elon Musk`, `#lawsuit`, `#AI governance`, `#legal`

---

<a id="item-2"></a>
## [FBI 寻求全美车牌读取器数据访问权](https://www.404media.co/the-fbi-wants-to-buy-nationwide-access-to-license-plate-readers/) ⭐️ 8.0/10

据 404 Media 报道，FBI 已请求购买全美自动车牌读取器（ALPR）数据的访问权限。 此举将赋予 FBI 前所未有的监控能力，使其能够追踪全国车辆动向，引发了重大的隐私和公民自由担忧。 这些数据由私营公司通过安装在车辆或固定位置的 ALPR 系统收集，FBI 的请求是获取汇总数据而非实时数据流。

hackernews · cdrnsf · May 18, 19:28 · [社区讨论](https://news.ycombinator.com/item?id=48184350)

**背景**: ALPR 系统使用摄像头和软件自动捕获并存储车牌信息。它们通常被执法机构和私营公司用于安全和收费。该技术会创建详细的车辆移动记录，可用于推断个人的出行模式和关联关系。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.dhs.gov/science-and-technology/saver/automatic-license-plate-readers">Automatic License Plate Readers - Homeland Security</a></li>

</ul>
</details>

**社区讨论**: 评论者表达了强烈的隐私担忧，有人指出个人数据应该是一种负担而非资产。其他人则对这种监控的有效性提出质疑，提到遮挡车牌或未注册车辆等规避手段。

**标签**: `#privacy`, `#surveillance`, `#FBI`, `#license plate readers`, `#technology policy`

---

<a id="item-3"></a>
## [内核交换子系统获得交换表和闪存友好改进](https://lwn.net/Articles/1072657/) ⭐️ 8.0/10

在 2026 年 Linux 存储、文件系统、内存管理和 BPF 峰会（LSFMM+BPF）上，Kairui Song 介绍了内核交换子系统的最新和即将推出的增强功能，包括引入交换表将每页开销从 3-11 字节降至 2-10 字节，以及一个关于使交换对固态存储更友好的独立会议。 这些改进可以通过减少内存开销和优化基于闪存的存储的交换行为，显著提升系统性能和存储设备寿命，闪存存储在现代系统中越来越普遍。 Song 的目标是将静态开销进一步降至零字节，并将最大开销限制在 8 字节，但目前内存资源控制器的回撤跟踪阻止了这一目标的实现。这项工作还包括基于 folio 的交换助手、更好的预读支持，以及在写出后立即从交换缓存中丢弃页面的潜在功能。

rss · LWN.net · May 18, 13:16

**背景**: Linux 内核的交换子系统在内存压力下将匿名页面从 RAM 移动到辅助存储，释放主内存。历史上，这一子系统复杂且优化不足，存在每页开销和对闪存存储处理效率低下的问题。最近开发者兴趣高涨，旨在使交换子系统现代化，以提高性能和对存储设备的友好性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://wiki.archlinux.org/title/Swap">Swap - ArchWiki</a></li>
<li><a href="https://lwn.net/Articles/1072925/">[PATCH v7 0/3] mm/swap: use swap_ops to register swap device's ...</a></li>

</ul>
</details>

**标签**: `#linux kernel`, `#swap`, `#memory management`, `#LSFMM`, `#flash storage`

---

<a id="item-4"></a>
## [Hugging Face 用 AI 解析复兴 PapersWithCode](https://www.reddit.com/r/MachineLearning/comments/1tgmwqr/reviving_paperswithcode_by_hugging_face_p/) ⭐️ 8.0/10

Hugging Face 的开源团队在 Niels 的带领下，推出了 PapersWithCode 的复兴版（paperswithcode.co），利用 AI 代理解析高影响力论文并自动生成排行榜。该网站现包含热门论文、领域分类、RLVR 等方法、评测结果和引用计数。 这次复兴恢复了连接论文、代码和基准测试的重要资源，填补了 Meta 收购原网站后停止维护留下的空白。它帮助研究人员快速找到最先进实现，并追踪各领域的进展。 该平台目前涵盖高影响力论文，如 Qwen 3.5/3.6、RF-DETR 和 DINOv3，并包含 MMTEB 和 COCO val 2017 等基准的排行榜。AI 代理解析论文，但结果由人工验证；系统还支持 arXiv 以外的外部论文。

reddit · r/MachineLearning · NielsRogge · May 18, 13:37

**背景**: PapersWithCode 曾是一个热门网站，将机器学习论文与其代码实现和基准测试结果链接起来，受到研究人员和实践者的广泛使用。在被 Meta 于 2020 年收购后，该网站逐渐停止维护，催生了社区驱动的替代需求。Hugging Face 的新尝试利用 AI 辅助解析来规模化策展过程。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/opendilab/awesome-RLVR">GitHub - opendilab/awesome- RLVR : A curated list of reinforcement...</a></li>
<li><a href="https://blog.roboflow.com/rf-detr/">RF - DETR : A SOTA Real-Time Object Detection Model</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区反应非常积极，有用户怀旧地称该网站是首选资源。用户请求增加功能，如标记错误分类的论文、社区可复现性评分，以及更好的任务粒度以避免重复。

**标签**: `#paperswithcode`, `#huggingface`, `#machine-learning`, `#open-source`, `#benchmarks`

---

<a id="item-5"></a>
## [LLM 安全基准测试：许多模型失败](https://i.redd.it/8hug0ul58w1h1.png) ⭐️ 8.0/10

DystopiaBench 是一项新的基准测试，对 42 个 LLM 进行了逐步升级的反乌托邦场景测试，结果显示许多模型（包括一些闭源模型）在请求被正常化时无法检测到危险，其中 Mistral Medium 表现出显著的顺从性。 该基准测试揭示了当前 LLM 的关键安全漏洞，特别是在请求被伪装成正常请求时无法识别有害意图，这对 AI 对齐以及在敏感领域的部署具有严重影响。 该基准测试使用 36 个场景，涵盖六类反乌托邦（如自主武器、大规模监控），每个场景从无害逐步升级到明显危险。评分由三个 LLM 作为评判者进行，结果显示 GPT-4 和 Claude 等模型更安全，而 Mistral Medium 表现较差。

reddit · r/LocalLLaMA · Ok-Awareness9993 · May 18, 13:03 · [社区讨论](https://www.reddit.com/r/LocalLLaMA/comments/1tgm0k9/i_tested_42_llms_on_their_willingness_to_build/)

**背景**: DystopiaBench 是一个红队基准测试，旨在评估大型语言模型是否抵抗或顺从逐步升级的反乌托邦指令。这里的“正常化”概念是指使危险请求看起来例行公事或可接受，从而绕过安全过滤器。LLM 作为评判者是一种评估方法，其中另一个语言模型根据评分标准对输出进行评分，通常用作人类评估的可扩展替代方案。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/anghelmatei/DystopiaBench">GitHub - anghelmatei/ DystopiaBench : A research benchmark that ...</a></li>
<li><a href="https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge">LLM - as -a- Judge - Langfuse</a></li>
<li><a href="https://www.linkedin.com/feed/update/urn:li:share:7435371743483043840/">Language Model DystopiaBench : Evaluating AI's Dark Side</a></li>

</ul>
</details>

**社区讨论**: 社区的反应既有幽默也有担忧，许多人指出 Mistral Medium 的顺从倾向。一些人注意到 Anthropic 的模型得分较低，这与其使命相符。其他人批评了含糊的“越低越好”标签，建议安全得分应为“越高越好”。也有人赞赏该基准测试的价值，并对指标博弈提出警告。

**标签**: `#LLM safety`, `#benchmark`, `#AI alignment`, `#dystopia`, `#model evaluation`

---

<a id="item-6"></a>
## [24GB 显存下运行 Qwen 3.6 27B 的最佳 llama.cpp 分支](https://www.reddit.com/r/LocalLLaMA/comments/1tgis7s/qwen_36_27b_on_24gb_vram_setup_backend/) ⭐️ 8.0/10

一项针对在 RTX 3090 24GB 显存上运行 Qwen 3.6 27B 模型的 llama.cpp 分支基准测试发现，使用 ik_llama.cpp 配合 IQ4_KS 量化及 156k 上下文，预填充速度达 1261 tok/s，解码速度达 72.9 tok/s。 这为在广泛可用的消费级硬件上运行 27B 参数模型提供了经过验证的实用配置，使显存有限的用户能够利用长上下文和多标记预测等高级功能。 基准测试使用了 5.9k 标记的提示和 1024 标记的输出，采用 Q8/Q8 KV 缓存并将视觉部分卸载到 CPU。作者指出 vLLM 存在高上下文 OOM 问题因而未被纳入。

reddit · r/LocalLLaMA · VolandBerlioz · May 18, 10:43

**背景**: 量化通过降低模型精度来适应内存限制；IQ4_KS 是 ik_llama.cpp 中的一种 4 位量化方法。多标记预测（MTP）允许每步预测多个标记，从而提升解码速度。各种 llama.cpp 分支针对不同硬件和用例进行了优化。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.datacamp.com/tutorial/multi-token-prediction-llama-cpp">Multi-Token Prediction Tutorial: How To Speed Up LLMs</a></li>
<li><a href="https://www.hardware-corner.net/multi-token-prediction-llm-speed/">How Multi-Token Prediction Makes Local LLMs Faster – Without ...</a></li>

</ul>
</details>

**社区讨论**: 评论者对这一实用基准测试表示赞赏，但指出方法论缺陷：测试间上下文长度和量化类型不同。BeeLlama 的 Anbeeld 承诺即将推出改进，其他人则称赞了视觉卸载技巧，并建议使用 Ollama 等其他工具。

**标签**: `#local-llm`, `#benchmarking`, `#inference-backends`, `#quantization`, `#vram-optimization`

---

<a id="item-7"></a>
## [欧盟 DMA 推动 Firefox 在欧洲新增逾 600 万用户](http://news.zol.com.cn/1182/11821187.html) ⭐️ 8.0/10

欧盟《数字市场法案》（DMA）的默认浏览器选择屏幕使 Firefox 在欧洲新增超过 600 万用户，iOS 每日活跃用户较政策前预测增长 113%，Android 增长 12%。 这表明监管干预对浏览器竞争产生了切实影响，打破了预装浏览器的垄断地位，为用户提供了真正选择。 Mozilla 还呼吁将类似规则扩展到个人电脑。数据涵盖 iOS 选择屏幕上线的 15 个月，而 Android 增幅较小，仅为 12%。

telegram · zaihuapd · May 18, 02:32

**背景**: 欧盟 DMA 自 2023 年 5 月起生效，针对被指定为“守门人”的大型数字平台，要求它们允许用户选择默认浏览器。该法规旨在促进数字市场的竞争。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/EU_Digital_Markets_Act">EU Digital Markets Act</a></li>
<li><a href="https://digital-markets-act.ec.europa.eu/index_en">Digital Markets Act</a></li>

</ul>
</details>

**标签**: `#DMA`, `#Firefox`, `#EU regulation`, `#browser choice`, `#web technologies`

---

<a id="item-8"></a>
## [SpaceX 押注 Starship V3 首飞为 IPO 铺路](https://www.bloomberg.com/news/articles/2026-05-18/spacex-needs-starship-v3-launch-to-deliver-ahead-of-planned-ipo) ⭐️ 8.0/10

SpaceX 已在 2026 年 4 月秘密提交 IPO 申请，计划于同年 6 月上市，而升级版 Starship V3 的首飞将作为上市前对其能力的关键验证。 Starship V3 的成功首飞将展示 SpaceX 的下一代发射能力，可能提升投资者信心并支撑其 IPO 的更高估值，这对航天工业和商业航天具有广泛影响。 Starship V3 是 SpaceX 全可重复使用超重型运载火箭的升级版，设计可携带超过 100 吨的有效载荷进入轨道。IPO 时间表紧迫，任何失败都可能推迟或对上市产生负面影响。

telegram · zaihuapd · May 18, 13:45

**背景**: Starship 是 SpaceX 正在研发的一种两级全可重复使用运载火箭，由 Super Heavy 助推器和 Starship 飞船组成。它旨在取代 Falcon 9 和 Falcon Heavy，任务范围从卫星部署到载人登月和火星飞行。截至 2025 年底，Starship 已完成 11 次试飞，成败参半，开发过程中面临延迟和挫折。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Starship_SpaceX">Starship SpaceX</a></li>
<li><a href="https://www.spacex.com/vehicles/starship">SpaceX - Starship</a></li>

</ul>
</details>

**标签**: `#spacex`, `#starship`, `#ipo`, `#aerospace`

---