---
date: 2026-10-01
event_id: EVT-20261001-000434
type: event_unit
status: completed
source_count: 66
language: zh
timezone: Asia/Shanghai
---

# Separate Unrelated Global Events

> Event ID：EVT-20261001-000434
>
> 原始新闻数量：66

## 第一层 Global Merge 事件判断

Each Cluster represents a distinct specific event or a set of unrelated events that should not be merged. Cluster 5 and 19 describe the same Tel Aviv Flight Stabbing Incident but are already grouped together in the input as Cluster 5. Cluster 26 contains two distinct UK security incidents (RAF Fairford and University Espionage) which are different events by location and nature, so they remain separate within their cluster. Cluster 27 contains distinct sports news items. Cluster 28 contains distinct international news. Cluster 29 contains distinct global news items. All other clusters (1-4, 6-25, 30) represent single distinct events. No additional merges across these clusters are warranted as they do not share the same specific real-world event, policy, product, or accident.

## 第二层 AI 多来源综合

# Event Name

关于以色列飞往特拉维夫航班中途发生袭击事件的报道综合

## Event Overview

本次事件涉及一航班在飞往以色列期间遭遇袭击。根据多份报道标题，事件包含“飞机中途袭击”、“乘客讲述恐怖时刻”、“水管工协助制服袭击者”以及“飞行员被刺伤”等关键要素。报道来源主要为 Google News 聚合及少数主流媒体（AP）。需要注意的是，多篇报道仅提供了标题及元数据，缺乏完整正文内容，因此当前分析基于标题信息及有限的元数据线索。

## Core Facts

基于所提供的 Article #137、#153、#163、#164 的标题及描述信息：

1.  **事件性质**：一起发生在空中、飞往以色列（特拉维夫）的航班上的袭击事件。
2.  **受害者身份**：一名飞行员被刺伤。以色列总理（Israeli PM）称该飞行员为“英雄”（'Hero' pilot）。
3.  **袭击者行为**：袭击者疑似为另一名飞行员（"by other pilot"）。袭击导致飞机进入俯冲状态（"pull plane out of dive"）。
4.  **干预人员**：
    *   有乘客协助制服袭击者，其中包括一名水管工（Plumber）。
    *   另一名乘客（或相关人员）向以色列总理讲述了自己如何帮助停止袭击者的经过，并提到“我拉动了控制装置”（"I pulled the controls"）。
5.  **时间/背景**：事件被报道为近期发生（基于文章标题语境），具体日期在提供的文本中未明确给出。

## Cross-Source Verification

*   **袭击地点与目的地**：Article #137 ("Tel Aviv flight... mid-air attack") 和 Article #163 ("stabbing on Israel-bound plane") 相互印证了事件发生在飞往以色列/特拉维夫的航班上。
*   **袭击者与受害者**：Article #153 明确指出袭击者是“其他飞行员”（other pilot），受害者是“飞行员”（pilot）。Article #163 提到“刺伤”（stabbing），与 Article #153 的语境相符。
*   **干预行动**：Article #138 提到“水管工协助制服袭击者，将飞机拉出俯冲”；Article #164 提到乘客告诉以色列总理“我拉动了控制装置”。这两者描述了同一干预事件的不同侧面：一人制服袭击者，一人控制飞机。
*   **信息来源重叠**：Article #137、#153、#163、#164 均指向 Google News 聚合平台，且标题高度互补，极可能来源于同一新闻事件的多角度报道，而非独立证实的多个独立源。Article #153 和 #138 来源标记为 "Unknown"，内容状态为 "horizon_summary_only"，表明其完整正文未获取，仅依据标题进行推断。

## Unique Information by Source

*   **Article #137 (news.google.com)**：提供了事件的基本概况——“特拉维夫航班乘客讲述空中袭击期间的恐怖时刻”。来源状态为 fetched，但内容为 Google News 聚合页，非原文正文。
*   **Article #138 (Unknown)**：提供了具体干预细节——“水管工协助制服袭击者，将飞机拉出俯冲”。来源状态 unresolved，无原文。
*   **Article #153 (Unknown)**：提供了袭击者与受害者的身份关系——“‘英雄’飞行员被另一飞行员在飞往以色列的飞机上刺伤，以色列总理称”。来源状态 unresolved，无原文。
*   **Article #163 (Unknown)**：标题为“关于以色列航班刺伤事件我们了解的情况”，暗示这是一篇综述性报道。来源状态 unresolved，无原文。
*   **Article #164 (Unknown)**：提供了乘客视角的具体行动——“乘客告诉以色列总理他是如何帮助阻止袭击者的”，并引用“我拉动了控制装置”的表述。来源状态 unresolved，无原文。

## Different Country / Regional Perspectives

*   **以色列视角**：Article #153 和 #164 提及“以色列总理”（Israeli PM）的表态，称飞行员为“英雄”，并听取了乘客关于阻止袭击者的叙述。这表明事件在以色列方面受到高度重视，且官方已介入或发声。
*   **美国/英国视角**：Article #137 通过 Google News (US/UK) 传播，使用了“harrowing moments”（恐怖时刻）等情感化词汇。Article #138 提到“水管工”（Plumber），这一职业细节具有西方媒体报道中常见的突出平民英雄的色彩。

## Information Differences and Conflicts

*   **袭击者身份细节冲突/不明确**：Article #153 标题称袭击者是“另一飞行员”（other pilot），这是一个非常具体的指控。然而，其他文章（如 #137, #138, #163, #164）在标题中并未明确提及袭击者的职业身份，仅称其为“袭击者”（attacker）。鉴于目前无法获取这些文章的完整正文，**无法确认袭击者是否确为飞行员**，这可能是 Article #153 独有的未证实信息，或是与其他报道来源一致但标题未重复的信息。
*   **干预者身份**：Article #138 明确提到“水管工”，而 Article #164 提到“乘客”告诉总理。两者可能指同一人，也可能是不同的人。由于缺乏正文，**无法确定水管工是否即为向以色列总理陈述的乘客**。

## Known Current Impact

*   **人员伤亡**：一名飞行员被刺伤（Article #153, #163）。袭击被制止，飞机安全（隐含于“pull plane out of dive”和“stop attacker”）。
*   **官方回应**：以色列总理已对受伤飞行员给予“英雄”评价，并听取乘客陈述（Article #153, #164）。
*   **媒体关注**：事件已被多家媒体（通过 Google News）报道，引发公众关注。

## What Cannot Currently Be Determined

1.  **事件确切日期**：提供的文章中均未明确给出事件发生的具体日期。
2.  **航空公司及航班号**：所有文章均未提及事发航班的航空公司名称或航班编号。
3.  **起飞地点**：虽然目的地是特拉维夫，但起飞地点未知。
4.  **袭击者确切身份**：Article #153 称袭击者为“另一飞行员”，但其他来源标题未佐证，且无正文验证。袭击者的国籍、动机、是否受伤或被控制，均无法从现有材料中确定。
5.  **受伤飞行员的最终状况**：仅知被刺伤，不知伤势轻重及后续治疗情况。
6.  **水管工与“拉动控制装置”的乘客是否为同一人**：无法确定。
7.  **完整事件经过**：由于大部分文章处于 "source_status: unresolved" 或 "content_status: partial/horizon_summary_only" 状态，无法还原完整的事件时间线。

## Sources

*   Article #137: [Tel Aviv flight passengers recount harrowing moments during mid-air attack](https://news.google.com/rss/articles/...) (news.google.com, fetched, partial content)
*   Article #138: [Plumber helped subdue flight attacker, pull plane out of dive](Unknown, unresolved)
*   Article #153: ['Hero' pilot stabbed by other pilot on Israel-bound plane, Israeli PM says](Unknown, unresolved)
*   Article #163: [What we know about stabbing on Israel-bound plane](Unknown, unresolved)
*   Article #164: ["I pulled the controls": Passenger tells Israeli PM how he helped stop attacker](Unknown, unresolved)

## Event Conclusion

综上所述，近期发生一起飞往以色列特拉维夫的航班中途遇袭事件。据以色列总理确认，一名飞行员被刺伤，并被其称为“英雄”。袭击疑似由另一名飞行员实施，但此点尚需完整原文验证。事件中，包括一名水管工在内的乘客协助制服了袭击者，并有人拉动了飞机控制装置以阻止飞机俯冲。以色列总理已听取相关乘客的陈述。由于多数报道来源状态为“未解决”或“仅摘要”，缺乏完整正文，事件的详细经过、袭击者确切身份、受伤情况及航班具体信息目前无法完全确定。建议后续获取完整原文以进一步核实 Article #153 中关于袭击者身份的特定说法。

## 原始来源映射

- ARTICLE 133 | Unknown | [Mamdani&\\\\#x27;s taxpayer-funded influencer army accused of plotting pressure campaign against NYC CEOs](#item-tech-news-133) ⭐️ ?/10 | 
- ARTICLE 134 | Unknown | [John Cusack sets the record straight on whether he was once considered for ‘The Breakfast Club’ role](#item-tech-news-134) ⭐️ ?/10 | 
- ARTICLE 135 | Unknown | [Phil Mickelson entered treatment facility for &\\\\#x27;family trauma and addiction,&\\\\#x27; representative says](#item-tech-news-135) ⭐️ ?/10 | 
- ARTICLE 136 | Unknown | [Cornell agrees to outside review of how it handled alleged sexual assault: Governor](#item-tech-news-136) ⭐️ ?/10 | 
- ARTICLE 137 | news.google.com | [Tel Aviv flight passengers recount harrowing moments during mid-air attack](#item-tech-news-137) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMirgFBVV95cUxOa0xLY3hxODU0ZzdtZmNjZ3lHMEFIZmFtNEt0R2pBNnhxRzI0SFR2ZTVfZ1R6eUhqT09CUGhKVXdjVzJ1YlhwU0hHek8wZkc3cUdxTUUxMmlveUpaZFRobzdSRG92RHhKbXZiU1c4QUcxVVhaTEVCMEVWZEVfLW5SWWQxTk8tMDl2ZDJlSXhHT1FzSDB2YnAzbzFUckpTeWF6OGFZVzl1cTdlUVc2VHfSAbMBQVVfeXFMUGNnTDFuak1VV3FUc1NLd2xDN28teHBFeU5JRjR1cW84dE1pblE3amlTVF8yWDI4ZjZ4T0RDZ005OEJwRnZpRmxYWGJJQ1F1cThGZE5nQmU4M1N3MUxxQThvbGZKblN0eXFlMER4TkJYM0JsMkZtTXVqTGhhUHBGdDJRR0g3OFFXYXdYMXloZ29EMzY0REdaUm5yT3VNZFR2aE5CUEdDMnNmSGJCbWhrd2FkdXM?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 138 | Unknown | [Plumber helped subdue flight attacker, pull plane out of dive](#item-tech-news-138) ⭐️ ?/10 | 
- ARTICLE 140 | Unknown | [WATCH: Snow leopard baby reveal](#item-tech-news-140) ⭐️ ?/10 | 
- ARTICLE 142 | Unknown | [WATCH: Will Reeve shares message of hope after cancer battle](#item-tech-news-142) ⭐️ ?/10 | 
- ARTICLE 143 | Unknown | [WATCH: Annual orange car parade grows in popularity](#item-tech-news-143) ⭐️ ?/10 | 
- ARTICLE 144 | Unknown | [Ken Paxton heard saying Trump&\\\\#x27;s GOP midterm convention hurt him: Report](#item-tech-news-144) ⭐️ ?/10 | 
- ARTICLE 145 | Unknown | [GOP doubts grow over Senate wins in Georgia and North Carolina](#item-tech-news-145) ⭐️ ?/10 | 
- ARTICLE 146 | news.google.com | [Hegseth says 20% of senior military officers will be cut, unveils new AI command](#item-tech-news-146) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMikApBVV95cUxOVHRyMVFPRnI4WXVUa28zNmRCdGlZd05wRjVtWWU3MGhBS19DNVBTdUluV3VuTFJwd0ZZUGJ4eVpES2lUNTBOTXV5bWtoeFh6ZFRIamo5eHlSdnpUdFZsTHVuT3liY1psaTl1Ti1xaTZwYVY0bUg5UnhQQW1oTzRvdmhvWDJrUVZ2dHdvNG0zWURYM191ZVZUNDJjVWFMWnJ1QTZzRVYxZGc1bjBGNlVJZG4xaWkwNjRDdVdwY2lpa1JsZmdZSWxGY1pBN2lkb2E2VEJnWi1iQW9rYUhjNjlFVGlSNnR5MzhxT1kzNXMwbWxpdVdtOW9iRGFBTFpuVnJEUnRIa2JQOEI4WU5HX3VFdmNXRzlLbzZCQ0hhalFRaGJoSlBIdFBWSWEwR1F2aWpBeUtIRFFxVG5xWXgwNGpkUlZPemx4dXBoS3l1SFRTZFU1X3hLT1IwbXotX19uQVdpdUlSMVk0RGpDNlVJY2tZb0hvVkdiYjJWRW1GcEJLQUc1eWJYNlhyejRGSjRkNmpSUUZkdWxMNUdPMW96SDdlQUlUbkpnRmJzUXZZYnJzYmJLSlF3eThyWkprLXdFSjFXcEJ2RjlpSEJHQU02WkpzaUVfb3QzNW9lS1Uwc0NpMFBMSDBvS1QwNFpOZEl1Q0hZd216d19JWVZFN0lBcXBCUUR0bjNpRzNHa1NZSWF2OWlSSGJIdy1WOXQ0TG16dFhrZGVwN0pSTnBPWHpXcWRWZDFQd2NKa2l3WnZpWjFnWlJMTloyX3pDa09lZmxmZG5fc2hpczBXQ2NNOTBMVjc2RUVRVm1pYWZiQUZKRDdFMGkxSjV0d0QzcDkyMVctc1ZTRU9ZWDRCd2lXeng1S1ZXUVhJUUd0VVVvMXpXR1cwaXQxTGFIR2wtN3ZESlozR0lTYzdJbDljdnROY196c0gyaHhFZXROeFowN0N2TElpZzZhQm1iNEMyV2hiWjFmWUxjMDl0Rkpxb0psSmJOeGZqNHR2cWRlNFRIempWeEZVVzNsZ1FsWlFGTVVzMENYbmJLN0tMaFVLdHBlbElJdHF5azlJVzVKYzE4Q2plZXd0OFBkWFRvMlJyVDlxSXFyRTU4cC1mX20xMkNRY0k2YkdoLVJPdjEyU1A0WTBkU24wMjFIVWdMZHlIT196VENPT3JCcnBuVktob3pPUjBDTnU2bl93alMzTExfTVVybEdydXc3LVktcWJlMmR1YmhsNTIzdEVTbTF3S01oUXYtQUZMZXNVMkgzRXBtX0JKUHpvRWRCa25ydkhQdnhyV1loODVNeE9CbDZrVk91TVY2VWRnam1BUE1uSXFaWHlHQlNYSno5S2VjYVU5b21RWUlrVjRBTEpESmhBLTYzUW9FYU55RVZzMW1rZGlIR1FNVVBDMnRMUmNFNGU0a1hVY1EyQTRJV2hUa04zNTRtTm1XV3lIXzVwRzY2RWl0ZlZycTZOeXZKWTRyZERIS3ZmNVBXZzVXRVU2N2M3ZTRvYVhuUXVVZFVpSG16OHA5YlpiNmw4dHBkZDAwTkNDUFZZQ3ZZTFVRNUNKb3BYQ0x1QlFVdWE5OUpzZkREUEZrSWRERVUwajZqenJtcDAyT3FrSjk1T1BfTEttR01xek5TUlhCM0ljbEJzRlZrdzVJNmw2eHRNNWZXZnpwQk9IY2hmc0U0b2Fab0ZlTVFORXhwb2ZPSXZ2M1FKMlN5UWxYdGw1T0NYcHg?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 147 | news.google.com | [California Gov. Gavin Newsom signs laws to protect workers from AI risks](#item-tech-news-147) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiugFBVV95cUxPVUM3X1c0NER4WmZtM2lyT2pxZmhnTWluWmdEWHpqWmNSWXFWaTQ1ZFhQTFFpSkFrb0h6QU9xWm96S2ZHclRHblUwRklvSGJIdEJOY0t4T3U0MWx6OHplTW1WdWJ0RnM5aWpiVVJQTXB2dkpYcG1TbEQ3UU5iMUNLTjJkZGtrZHBwZnp0ZWxrUGRZUHNfX2tFdkgzbm1VbEJtN2h4SmhDLUo3TjFQY1RGNGNQa01VRlQzNmc?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 148 | Unknown | [Former DHS Secretary Kristi Noem files for divorce](#item-tech-news-148) ⭐️ ?/10 | 
- ARTICLE 149 | AP | [Gov. Hochul calls for &\\\\#x27;independent review&\\\\#x27; of Cornell response to alleged group rape](#item-tech-news-149) ⭐️ ?/10 | 
- ARTICLE 150 | Unknown | [Trump’s shift from &\\\\#x27;Housing First&\\\\#x27; causing upheaval for homelessness programs](#item-tech-news-150) ⭐️ ?/10 | 
- ARTICLE 151 | news.google.com | [Veteran broadcaster Dame Esther Rantzen dies aged 86](#item-tech-news-151) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiXEFVX3lxTE1sWF85Q1NxVGRneHpBSWlNUXowWTZ3bkNkSy1ZSUdzWHRFRUNPMlh2S1M2NkRGV2FKZnFnZjExaTNBLUtpbXZmMmhKdmFJR1F6YXdmR2FBd0I0eW9T?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 152 | Unknown | [How That&\\\\#x27;s Life\\\\! gave Esther Rantzen a career-defining moment](#item-tech-news-152) ⭐️ ?/10 | 
- ARTICLE 153 | Unknown | [&\\\\#x27;Hero&\\\\#x27; pilot stabbed by other pilot on Israel-bound plane, Israeli PM says](#item-tech-news-153) ⭐️ ?/10 | 
- ARTICLE 154 | Unknown | [US Supreme Court allows execution of Christa Pike to go ahead](#item-tech-news-154) ⭐️ ?/10 | 
- ARTICLE 155 | news.google.com | [Employers should teach primary-age children about work, says Milburn](#item-tech-news-155) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMimAFBVV95cUxNbVl1VlBWb1VFUlBUbzc3WDEtUGRpa1RWWFZzNWhHel9pQU9nc3VYbi03WkFRRHc0TTRwUW1qX3JQZTdESjNZUkhDdFNjSkozaUNoLXZHV3Q3c0xOQTQ3cF94dXJGN2xYS0FEWVN1Mk53M2Nua25xMFNEUDJDcEIzMTBSS0FsRW1ZdG5HY0w5OXgwXy1XM2JpSQ?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 156 | news.google.com | [China has cracked down on AI relationships. Is it ahead of the game?](#item-tech-news-156) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiXkFVX3lxTFBPTVU4RTl1LUhfX0JxTWJtM1lsVDgxMXF4MTItSGVUTWQ4VmdHSHRyX1dqbUtvb05ZVjV4Nmk5eTRYajJraDRGSWx2eWxCdHU4blZid2ktVFZMakR4Y2c?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 157 | Unknown | [Celebrity Traitors is back - here&\\\\#x27;s what you need to know ahead of the first show](#item-tech-news-157) ⭐️ ?/10 | 
- ARTICLE 158 | news.google.com | [We fear for our lives after being told our abusive exes will be freed from jail early](#item-tech-news-158) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiXkFVX3lxTE5NdjhsMDhqTGFmOEFjcUUxeElFVmZJTFBvOS1uZVpLTS1ZY3pEUUFwLTJ2YXo1XzJCc2xQbThUdVo4dnV4RXhEVzV3MERvTkdrQUhJSGJPYzg0UzdUWGc?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 159 | news.google.com | [Tiny image sparks big backlash in Nikon photo contest](#item-tech-news-159) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiXkFVX3lxTE1NMEU2Tjgxc2djdFlMVXFSd1hnMnpZdkRjUlZYNVhiRm82SVFNbDBrckJMRFVpamZnNUY1MkNYbzM0S0RVUDJyQ0pvbXNCMVdjYl9PSjh6elBOZ3hJcGc?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 160 | Unknown | [Swiss glaciers suffer &\\\\#x27;disastrous&\\\\#x27; year of ice loss, threatening water supplies](#item-tech-news-160) ⭐️ ?/10 | 
- ARTICLE 161 | BBC | [BBC should not overspend on shows such as Suits and Schitt&\\\\#x27;s Creek, MPs say](#item-tech-news-161) ⭐️ ?/10 | 
- ARTICLE 162 | Unknown | [Conservatives pledge &\\\\#x27;tough love&\\\\#x27; benefit rules for under-25s](#item-tech-news-162) ⭐️ ?/10 | 
- ARTICLE 163 | Unknown | [What we know about stabbing on Israel-bound plane](#item-tech-news-163) ⭐️ ?/10 | 
- ARTICLE 164 | Unknown | [&\\\\#x27;I pulled the controls&\\\\#x27;: Passenger tells Israeli PM how he helped stop attacker](#item-tech-news-164) ⭐️ ?/10 | 
- ARTICLE 165 | news.google.com | [Flydubai passenger describes putting attacker in chokehold after cockpit stabbing](#item-tech-news-165) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiXkFVX3lxTE5fbTBRYnA1dGN6VHJ2R0pKQzZLaFNVaXlZbFR4TVY1b1lQVnFORXNEVkdGNWlzeFU3SmtSakMyMjRLOW9LZFNmZE9iRjNMOGY3bFlTN2xmU2lCY1EzaHc?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 166 | Unknown | [&\\\\#x27;Shaken and emotional&\\\\#x27; travellers arrive at Israeli airport](#item-tech-news-166) ⭐️ ?/10 | 
- ARTICLE 167 | Unknown | [Energy bills are going up - here&\\\\#x27;s what you can do about it](#item-tech-news-167) ⭐️ ?/10 | 
- ARTICLE 168 | Unknown | [Trekkers helicoptered off mountains as more deadly landslides hit Nepal](#item-tech-news-168) ⭐️ ?/10 | 
- ARTICLE 169 | Unknown | [UK believes Iran involved in RAF Fairford incident, PM says](#item-tech-news-169) ⭐️ ?/10 | 
- ARTICLE 170 | Unknown | [Punish Man City this season, say other club chiefs](#item-tech-news-170) ⭐️ ?/10 | 
- ARTICLE 171 | Unknown | [Burnham &\\\\#x27;really concerned&\\\\#x27; if Man City owners sell up after rule breaches](#item-tech-news-171) ⭐️ ?/10 | 
- ARTICLE 172 | Unknown | [Ronaldo leaves Portugal camp after coach denies rift](#item-tech-news-172) ⭐️ ?/10 | 
- ARTICLE 173 | Unknown | [Respect and laughs as Fury and Joshua face off](#item-tech-news-173) ⭐️ ?/10 | 
- ARTICLE 174 | Unknown | [Arsenal let two-goal lead slip to draw with Paris FC](#item-tech-news-174) ⭐️ ?/10 | 
- ARTICLE 175 | Unknown | [Infantino should have no place in future of football - Pinto](#item-tech-news-175) ⭐️ ?/10 | 
- ARTICLE 176 | Unknown | [Saracens boss Venter skips more media duties](#item-tech-news-176) ⭐️ ?/10 | 
- ARTICLE 177 | news.google.com | [Trump administration diverts human rights funds to push far-right agenda abroad](#item-tech-news-177) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMikgFBVV95cUxNVllFcEFycUNYQTVsbG43Z3pYbV9Sakx0a0J5aVVsVHNHRDN6Y1doYThLWVdfZWRMZDgyT2JuRWs0MnFYeTV0elRSbUVYVnVHVy05cHNFaFdpUi1PUlZZWXdEMm1VdU5DRnYxOVl2d0szSFNqYXdxeFpNSDBBYjJleUkyRU9mZFl0aTFjS3NISk13dw?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 178 | news.google.com | [South African leader urges men to speak up on gender-based violence after series of killings](#item-tech-news-178) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMimwFBVV95cUxOcnVPVlBzNnptRl9TSG10NTl5cHNGZ0JqM2U0R1hEdU9aclJuMDdmU09DaEZOX3dOTGc0TTRnU3BxY0VRdlZwMXdxd1JsdkhfSnU2dWpQcHE2UGVxUTRnOGxoc0NHQ1FiMldINGNwRlhKTjdFNl9kZHJjQjI1U0FIajlJNVVCVFU0ZjBnSUtlN1lfcFQ4VDhXc3RNSQ?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 179 | news.google.com | [Burundi agrees to receive ‘third-country’ migrant deportees from US](#item-tech-news-179) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiogFBVV95cUxOZndOOXZCM3BGQlBXR1JYV0VKYzJ1ZFp4QnIxRGV3dGVvcGFmMnI4S3lJZGRoRWwtOVJvQU9leUYtRTZ4NFhlQnN5bFRKSkh4Zlg0SzZEZWw5RWtQcnlKS3NQa2VFbkhwVm5SUkd6X3ZzNU9Fb3NtdHVWR1dhMGd1LWtidDVid2RDQjRwTXBySXgyMnNRUG1UaVk4cmM0dS1Yanc?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 180 | news.google.com | [Daredevil Jaan Roose prepares to walk slackline high above central Seoul](#item-tech-news-180) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMikwFBVV95cUxNdXFFeUQzRGZ3c1h4MG9oSGlPdEVNZlcyZXk5NG5hSERCT2hHbkxfdjdoTUNPUGticU5Va3lpUkRtMGpaZWItc1RyWkdiTGtOTTRVWVcydXhLSjQ4NmstX2c0cUNIYmJadTVabXE4eEJyc0ltdVM3dnpFUmRKLTBaaFJMMTlud0w1MHc1WWZHLUVwaE0?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 181 | news.google.com | [MI5 China alert will send chill through UK’s cash-strapped universities](#item-tech-news-181) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMioAFBVV95cUxQN05nWmttTE9TZkhKem9Na1V1eVhOcTRlRDc4Q01ZWGM1YTZqeUtrRGlXTjlVRUZRV295S1hkbmR5N2pYN2FRWk1YSkVwZ0xHSjBpcWFIVEZHVlpQV2lVTGhQRkZDVFN4d0NqS0JzY3pXZXpfYTh0dDRJVHRpdHBadkRqS0c4ZERNQkYycDJNc0xOMUtyd1V2ZUJPVlB2eVpz?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 182 | news.google.com | [MI5 warns UK universities over ‘theft of tech secrets by Chinese front company’](#item-tech-news-182) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMi1gFBVV95cUxPQTBmYnFoZWdKX1g0bFhhZm5ITWQ3bnlUTmtnd2dZQ25jYWtjNUM0UDJpdWFfUlpYR3ZKV3h2VFNKNUpzZENzc3JwS2xFN1hFSjZvdF8wLXcxZjJvU3AyclAtVU15Tkp4czdJS1JTeHJFdGVONmFwN0ZVVHNXS2NWTzZfTFowcE5TLWFLTGxWS1p2UmV5MlJ1eUoyeWJNMDBMalhTOUdYdEoxTWJRUUxPSkRNc2ttWnUzbDliM1cyN19FMGt6SXJHbV83cVZTWnpHQXpWbWd3?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 183 | news.google.com | [AI tool that copied actor’s ‘lustrous’ voice violated his rights, Tokyo court rules](#item-tech-news-183) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMingFBVV95cUxOVF93OS1qYzhDOHZlcURzdExLUlJyNjNEeEdmaHZkZDNPZGNndjhOQjVyUlBtbnlkcXhQbU1fd0E3YnN5SF9CTnNtTXYzNUFKT0dEWk1ELVJ5dGFKZmlSb21CM3JHZmJNalNCd2FmTVVuQTQzVm9oX1dKNllsWmM3Zkc1M2QxMUJSLVhwQmJiNFkwSFZXc0RHTFQtSm9rdw?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 184 | news.google.com | [South Korea calls for apology from North Korea after mine injures three soldiers](#item-tech-news-184) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMioAFBVV95cUxNbGp5LVFPNGhLTjZRZkxIalI2RUQ3bkNKSXpZNDVMaTQyby1hMlhhOXY4ZWFrVDdkVG8xUTR4ZkxCRGF0M1hyZGtXN1hJRXBybmNFZmxZQklLVl9KVjRWdkNFSzRrWVRiUjBMWFdJZzFhcmtKUURzT0pGRTV1TGVJc2tXT0haLWRvdGpNOEdydHBsaFZ2UWtpSHkzZFMwN2s5?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 185 | Unknown | [Australia news live: Albanese says Shoebridge’s goal to ‘replace Labor’ is ‘somewhat concerning’; recruitment for Antarctic jobs open](#item-tech-news-185) ⭐️ ?/10 | 
- ARTICLE 186 | news.google.com | [Brisbane and Sydney hit hardest by falling house prices as 5.2% shaved from property values nationwide](#item-tech-news-186) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiqgFBVV95cUxOY1R6MURvNU4tWmdERzFrMUtrUjRhTjgyWnlYTW41dXpBZVBEZHVaeTNiNjd2ZkFWZC1pYW1FczlLZVlwU1JCR2RJdktOT2w3bTNJYzlXQm8tWGpHMDl4MGF6RjM4dm9DZ2pGS2NaSERiQUFoN0R1bFllVlVaeGlRZDVGaTdaS0dUYXVnUVlzZzJTUjE4cDZveDNCYlk3TkpYbnZXZVJIamFGZw?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 187 | news.google.com | [Australia’s cheapest mayonnaise is also the best tasting, Choice test finds](#item-tech-news-187) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMioAFBVV95cUxQdmQ4VkNLU3dxZFBuNDRHcGVyVGg2QVduQ3p5czMyeWZSdk1mNHRPRWxrTDBNVDZtM284SGJOd2J0ZTVkYWpUeWEyZVFtTkp2dmwwZWNBelJoS1Q3cnZTN0Z2SndRNlpCaTdJMzkxdHh2UjYtR2xtcjFXQmlaNnJmS1V2QlE3clB3QlFEekZ4UUVxVC1nelB4U0QtY1NqZmFN?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 188 | news.google.com | [Australian colleges warned ‘do not try to game’ student visas after last-minute enrolments for cancelled diploma soar](#item-tech-news-188) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMi1gFBVV95cUxOZlpQM2NVTjhncWVGOHZycmYzRDN6bXdkSmY3VngwOUVVc2Vyblh0QS1HTE1SRjF0S2xOeDMzaXhGc05RZkJXX25KNHZIM0ZQNkNjaG11bjd6UU5BQWtwaWk4WHE4alpqeXUtbUZscklPMjBVZnlHRjZZYUZjR3BjNHhRbC16dHZ0enNNbkNDdGNfTWQtODRtTXpoSkczYmk2c3E0MFR5ZThkSUNQLUZkbjIxYWpnQWdoXzZ5R1BNdTFYZHZtRmgwU2lET0t6SVhXTmdBTml3?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 189 | AP | [Peugeot recalls hundreds of cars in Australia over issue that could increase ‘risk of serious injury or death’ – as it happened](#item-tech-news-189) ⭐️ ?/10 | 
- ARTICLE 190 | news.google.com | [Stella McCartney makes waves with ‘sea life, not sea food’ theme in zero-wool Paris show](#item-tech-news-190) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiqgFBVV95cUxNc0preF9ENDk0NURuNmFaejZqVjI3Vjl5b0Y1NFRTZ205S25Xd2tlZjZlN3JKMTdvYmJhNE5hcmpfcXViTnlWdjBYYXBHTHNnQXZ2cmhuNWp4dkJfNWZRMEFOeDNFWHZPZDhTWWZKSy1WRFIxZXNjQUlWckFzWlRQd1JEZDZmRXhlY0taMlZLNkZOYjJQdnpKMUlwcWRlVzBWMTNwejNxQTBNZw?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 191 | news.google.com | [No 10 gathering evidence on public support for UK rejoining EU](#item-tech-news-191) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMiugFBVV95cUxNOGR0NkxuWEJGVmh6YmVXM2xxWFVDa08tRGhSTHU0eVNXQWlGQVpMbzRHMHBSb2h2eHprZXYyNHhRWmljN3BGcGp6YTM2MXMyTjd6YkljY3hfR3Y1U0pWSG93QjhVeVVCMF9jWDlsR3B0UlVEMFFHeVBDdmlSZFNEU0lidGFrN3g2OUZ5azQ4Y09ET2JGWkNvbVhaZU5WLWdPNjFrRkV3TTlNLU14cWR4YUkwaXlkMGtNS1E?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 192 | news.google.com | [Macron says ‘welcome back’ to Burnham suggestion UK could rejoin EU](#item-tech-news-192) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMipgFBVV95cUxNam95YkxtZjdhQ3ZadHVCLUp5bWZiRW45UzBoUTNjU0dKMDFQLWVWS0tXQmZzMFdDay1mV3BXYXBPd2tLTEJpSDVJRlBEaG96UW5VNDloa1ByX3NoMnp2UFlJc3RMR2JZU1Z5V1BsQWdyQ2FXM0ZqWUpBZFVMdFZFUk9mM1hlcUFTODcwREVENGZaeTVRTExUTWJoeUZxc1VObFVIZW5n?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 193 | news.google.com | [French court jails six men for manslaughter over mass drowning in Channel](#item-tech-news-193) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMipgFBVV95cUxQazhENjk4OVNMaUo4Y2p1WjZ1VEpFZ2owT0lFSXlPMk10U2JwM1QxTHlHMEFxdGwtd2RZVzEtS1JzSWp3WDRuN0c4UGRwbDE1Z0ZPUjdtOGRmekhkZUtEYkdiNGRqSnJPQ21rclpiVlhXUTN2RmNYMEpjRmt0cXpCdlJHZzFaZm9MdS01VDkyVFdEdG9VMnlrNTZJWXlVSEtFcWpFcGN3?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 194 | news.google.com | [Sweden must apologise for harm done to Sami people, says state-backed report](#item-tech-news-194) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMigwFBVV95cUxQUzg2SFVRQ3RhVG10QlNHc1NWSnFqSnVmZFRLWEVmMWJNV21FaU4ybVAtcWdVRHN5dHl0VkwyTVA5eDFpMmhUTkJmN0tNTGFwMWNLQWpid0Z6N3JkUmVUeklrVDd2UnFLelhWbUp0S2xxX2hmVjdSSWhMVmhIbmIwZG9qYw?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 196 | news.google.com | [Israeli forces overwhelmed by violent settlers in ‘terrorist attack’ on Palestinian family](#item-tech-news-196) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMisAFBVV95cUxQck1UYS1hTWNab0xHZEFSYzV1U0RUQXMxMXZuakpsTFl6TVI3MmxjYXB4ZDRWVGNKWVBLek9rQll3MHRGV2pESmEwOFhvVkZuUG5IazJBWG5sak05SzdEYUhiUVBOVjA0c2syUUNXeF9RM2tEUGlSeFpoZlM4OHdITk9jNXdjQjFKaUZOOW81TjQ0YkJ0bXRhT21BZ2lPNmVJcWJiaXRyTi1BMWh6MnFPRA?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 197 | news.google.com | [Pentagon says it has formally completed withdrawal of US troops from Iraq](#item-tech-news-197) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMijwFBVV95cUxPMnVnUlREdFdEd2ctcFdoa2FxRHNGOUF5N2VzZDVHZkVhN2VYeVozdmNlaHAxVEE3dXlubUdNM01xbVhXandGTTdpRVdMbWJrSXgyN2twLWR0QXNHU3U5cWdPWE10WFJ4NThYdHVqSk9qVWpfNktGYllPS1RrMVN4ZWtZOTQ0cDZvR0hUSWdKcw?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 198 | news.google.com | [‘Whoever is hearing me, we need help’: how flight 1073 survived its 17,000ft plunge](#item-tech-news-198) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMixgFBVV95cUxNTXRhSDR2MVlQZGtwdWJsRGU2QVp5ZF9RNkp1OVdqaVF0bDlRYzNlckZMQl8zNy1kanZHZzYxWTJ5TWJwdzA0c1ZOdVAtZ010U1RocExVcmVtUENDVGRuM3hGaDB0MUZRWk9CVjl0OGZ1VmlUVGhJLXFXelpvMDhvdjFoaWVna2xtOVJXYmRSWnYyUDFsdzhuZTE3MllDUkpVdHNBbWFlMm5rSXlpSG41NzRVek8xOXZkbnMwcWp1RnZvZGdmVVE?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 200 | news.google.com | [‘We want justice’: series of rapes trigger mass protests at Indian universities](#item-tech-news-200) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMimgFBVV95cUxNU2JGeENOcUJteDNUN2dWMU5PcFhtMnZGMHBRZGN5ZzA5eEZSUEhNWExFbWdTajR4MjlKSUZKd2hzZTRsT3lyeHh3Z2VvTlJoZ0VsN2tBMnhjLV92X3dPT3pZR2dzNjB3Q21pUGt1RktEZzNBb2hEcUhPMFQ0WlZ5OFNTN0F0WWVVai1fdGxpLS1fUWsxaUo2Ymd3?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 201 | news.google.com | [Oasis take legal action to stop sale of unheard recordings valued at more than £1m](#item-tech-news-201) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMilgFBVV95cUxNandNMUhTeG9yTHl2MDBDQmt0Njk1S2U1eEpGeDZoRW9MS0V2WGt5ejI4cHBNVWZSV1FPRFFSbmVJNFFwa0thdmRYTldmWENrc3lQUDZLdDhRSUlRVzQ2SWlNMmxoSmdOTkdJTl9CSDJURThMSHFxN1hMbFR5U2NBTkNrNU9mSDZhc3Z2SDdwZGNIVFQwV1E?oc=5&hl=en-US&gl=US&ceid=US:en
- ARTICLE 202 | news.google.com | [Floating scarecrows: how Cornish fishers are stopping seabirds drowning in their nets](#item-tech-news-202) ⭐️ ?/10 | https://news.google.com/rss/articles/CBMirgFBVV95cUxOYndNdWs2Nm5ITEoydVJaZWVpbHZYWlh0UHdtcmQ5YXFya3hlWDlobXZ3aGlXWnV4eklZOTQzVE41MzFXNENDUVREMGhFcWJKUGVEdUxDS3RuWEUtRmVUck1KOVNmemU4NFlfUHFsSC1oTHI2dFp5bjRFanZaNWtGNTVpZl9ZZmVuanI5OENMTHc3QmljeFRKb3B1N0NrVXJtR0tDYjZnVW80QkhFSEE?oc=5&hl=en-US&gl=US&ceid=US:en
