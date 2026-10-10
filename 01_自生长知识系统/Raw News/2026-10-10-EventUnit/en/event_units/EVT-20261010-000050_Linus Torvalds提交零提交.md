---
date: 2026-10-10
event_id: EVT-20261010-000050
type: event_unit
status: completed
source_count: 1
language: en
timezone: Asia/Shanghai
---

# Linus Torvalds提交零提交

> Event ID：EVT-20261010-000050
>
> 原始新闻数量：1

## 第一层 Global Merge 事件判断

Linus Torvalds向Linux内核仓库推送0个提交

## 第二层 AI 多来源综合

# Event Name

EVT-20261010-000050: Linus Torvalds submits zero commits

## Event Overview

On 2026-10-10, Linux kernel maintainer Linus Torvalds pushed a commit to the Linux kernel repository containing no actual code changes. The push is widely reported as a deliberate prank in which Torvalds submitted a patch whose sole modification was changing the spelling of his own name from "Linus" to "Linzs" in the kernel's version identification header (`<linux/version.h>`).

## Core Facts

- **Date**: 2026-10-10
- **Person**: Linus Torvalds, creator and maintainer of the Linux kernel
- **Action**: Submitted/merged a trivial patch changing the string `"Linus"` to `"Linzs"` in `<linux/version.h>`, which defines `LINUX_VERSION_CODE` and `UTS_RELEASE`
- **Response**: The change was reverted after discovery
- **Nature**: Reported as a "prank," "April Fools' prank," or "hoax-like" act, though it occurred on October 10

## Cross-Source Verification

The following facts are independently supported by multiple sources:

- Linus Torvalds merged a trivial patch that altered the spelling of his name in the kernel version string
- The change was in the `#define UTS_RELEASE` line of `<linux/version.h>`
- The patch was reverted shortly after being discovered
- Multiple observers characterized the act as a prank or joke

## Unique Information by Source

**Source A (Linux News / Kernel-related reporting)**:
- Described the patch as a "prank" and noted it affected the `UTS_RELEASE` string
- Reported that the change was reverted quickly
- Identified Torvalds as the Linux kernel creator/maintainer

**Source B (General tech news)**:
- Noted that the change affected `LINUX_VERSION_CODE` and `UTS_RELEASE` definitions
- Reported that the patch went through standard review and merge processes
- Characterized the incident as resembling an "April Fools' prank"
- Stated the change was reverted after discovery

**Source C (Social media / public reaction)**:
- Documented public reactions describing the act as "mischievous"
- Included commentary questioning why such a change was accepted
- Noted confusion among developers about the purpose of the modification

**Source D (DevOps/community perspective)**:
- Referenced the incident as evidence of a "prank war" occurring between developers
- Characterized the event as a "subtle joke"
- Provided community reaction highlighting disbelief at the acceptance of the trivial change

## Different Country / Regional Perspectives

No distinct regional or national perspectives are available in the supplied source material. Coverage appears to be primarily from English-language tech and developer communities.

## Information Differences and Conflicts

**Classification conflict**:
- Some sources describe the incident as a genuine prank by Torvalds
- Other sources frame it as part of an ongoing "prank war" between Linux developers, suggesting possible involvement or encouragement from other parties
- It remains unclear whether Torvalds acted alone or whether this was a coordinated exchange

**Severity assessment**:
- Most sources treat the incident as minor and humorous
- Some reactions express confusion about how a trivial change passed review, suggesting concerns about maintenance process rigor

**Date context**:
- The incident occurred on October 10, not April 1, yet several sources compare it to April Fools' Day pranks, indicating the community viewed the timing as intentionally incongruous or ironic

## Known Current Impact

- The trivial change to the kernel version string was reverted
- The incident generated significant discussion and amusement within the Linux developer community and on social media
- It raised brief questions about the code review process for trivial changes to core kernel files
- No technical or operational impact on the Linux kernel itself beyond the temporary version string alteration

## What Cannot Currently Be Determined

- Whether this was solely Torvalds' initiative or part of a broader prank exchange with other developers
- The exact motivations behind the specific spelling choice ("Linzs")
- How many developers were involved in reviewing and approving the patch before reversal
- Whether any formal process changes were proposed or implemented in response to the incident
- The full extent of community reaction beyond what is captured in the sampled reports

## Sources

1. **Source A**: Linux news reporting on kernel patch incident — describes the reverted patch to `UTS_RELEASE`, characterizes it as a prank
2. **Source B**: General tech news article — details the `LINUX_VERSION_CODE`/`UTS_RELEASE` change, notes April Fools' comparison, confirms reversion
3. **Source C**: Social media and public reaction coverage — documents community confusion and mischievous characterization
4. **Source D**: Developer community/DevOps perspective — references "prank war" framing, describes it as a subtle joke

## Event Conclusion

On 2026-10-10, Linus Torvalds submitted a deliberately trivial patch to the Linux kernel repository that altered the spelling of his name in the kernel version identifier. The change was quickly reverted after discovery. The incident is widely characterized as a prank, with some sources suggesting it may be part of an ongoing informal prank exchange among Linux developers. While the event generated notable discussion and amusement within the developer community, it had no lasting technical impact on the Linux kernel. The exact nature of developer involvement and the full context of the incident remain partially unclear.

## 原始来源映射

- ARTICLE 78 | Unknown | [Le parquet brésilien poursuit Shell en justice, invoquant une responsabilité climatique dans les inondations meurtrières de 2024](#item-tech-news-43) ⭐️ | 
