---
title: "[🗺 The United States as a Civilization map, from real data](#item-tech-news-268) ⭐️ ?/10"
date: 2026-11-28
type: "news"
source: "www.lesswrong.com"
source_url: "https://www.lesswrong.com/posts/uTrkTFk4wFjb7Xoqq/capturing-my-favorite-electric-piano"
language: "en"
horizon_score: 6.0
source_status: "fetched"
content_status: "full"
search_method: "direct_url"
match_score: 1.0
ai_status: "pending"
original_title: "Capturing My Favorite Electric Piano — LessWrong"
author: ""
---

# [🗺 The United States as a Civilization map, from real data](#item-tech-news-268) ⭐️ ?/10

## Horizon 摘要

# [🗺 The United States as a Civilization map, from real data](#item-tech-news-268) ⭐️ ?/10

## Horizon Summary

---

## Technology Blog

### [Capturing My Favorite Electric Piano](https://www.lesswrong.com/posts/uTrkTFk4wFjb7Xoqq/capturing-my-favorite-electric-piano) ⭐️

A practical account of using a laptop to electronically capture a Yamaha P-85 electric piano sound via MIDI, converting it to a soundfont for live performance, while documenting the specific MIDI bank and program numbers required.

rss · LessWrong AI风险社区 · Nov 28, 03:10

**Tags**: `#MIDI programming`, `#Audio synthesis`, `#Instrument sampling`, `#FluidSynth`, `#Yamaha P-85`

---

### [Good domestic politics vs bad state realpolitik](https://www.lesswrong.com/posts/sQWvX3irLhuoSxpXu/good-domestic-politics-vs-bad-state-realpolitik) ⭐️

An analysis of why the British BIST committee&\#x27;s demand for the unredacted METR report serves domestic accountability while potentially harming British geopolitical interests in AI governance.

rss · LessWrong AI风险社区 · Nov 28, 01:53

**Tags**: `#AI Governance`, `#Geopolitics`, `#Parliamentary Committees`, `#Policy Analysis`

---

### [Who/What/Where/How of Compute Verification](https://www.lesswrong.com/posts/isY2zw4fQSRLooMfL/who-what-where-how-of-compute-verification) ⭐️

An overview of compute verification challenges in the context of AI regulation, categorizing devices and outlining the difficulty of tracking decentralized and edge computing.

rss · LessWrong AI风险社区 · Nov 27, 23:42

**Tags**: `#AI Governance`, `#Edge Computing`, `#Regulatory Compliance`, `#Hardware`, `#Security`

---

### [What Book to Read Next?](https://www.lesswrong.com/posts/ECRc2Hzi7iFYXsiqo/what-book-to-read-next) ⭐️

A personal reflection on strategies for prioritizing which books to read based on emotional impact and practical constraints.

rss · LessWrong AI风险社区 · Nov 27, 23:01

**Tags**: `#personal essay`, `#reading habits`, `#non-technical`, `#self-reflection`

---

## Financial News

### [03版 - 城尾乡头，搬不走的好产业](http://paper.people.com.cn/rmrb/pc/content/202611/28/content_30193547.html) ⭐️

An article from People&\#x27;s Daily details how the development of a local eel farming industry in Xiantao, Hubei, has spurred rural infrastructure improvements and boosted county-level economic growth.

rss · 人民日报\(People&\#x27;s Daily\) · Nov 28, 00:26

**Tags**: `#Rural Economy`, `#Agriculture`, `#Regional Development`, `#Hubei`, `#Industry`

---

### [03版 - 几十秒发射，如何让游客多留一晚（创业创富的年轻人）](http://paper.people.com.cn/rmrb/pc/content/202611/28/content_30193548.html) ⭐️ ?/10

## 原文信息

- Source: AP
- Original URL: https://www.lesswrong.com/posts/uTrkTFk4wFjb7Xoqq/capturing-my-favorite-electric-piano

## AI处理状态

等待后续 AI 二次处理及 27 Skills 分析。

## 原文信息

- Source: www.lesswrong.com
- Original URL: https://www.lesswrong.com/posts/uTrkTFk4wFjb7Xoqq/capturing-my-favorite-electric-piano
- Original Title: Capturing My Favorite Electric Piano — LessWrong
- Description: Since refelting the Yamaha P-85 I used to gig with, I've been playing it more. This has made me realize just how much I miss its epiano2 sound. It's…

## 原文正文

Capturing My Favorite Electric Piano — LessWrong

x

LESSWRONG

LW

Login

World Modeling

Personal Blog

10

Capturing My Favorite Electric

Piano

by

jefftk

28th Nov 2026

jefftk

3

min read

0

10

Since

refelting

the

Yamaha

P-85

I used to gig with, I've been playing it more. This has made

me realize just how much I miss its epiano2 sound. It's an imitation

of a

Fender

Rhodes

electric piano, which uses amplified metal tines instead of

strings. When a hammer hits the tine softly you get a relatively pure

and clear tone, and the harder you hit the more "bark" or "growl" you

get. The P-85 has a simplified imitation of this sound, and when I

got my

P-121

I was sad to learn that they'd removed almost all the bark.

The world

traditionally

dismisses keyboard sounds when they're new ("this sounds nothing like

a piano/organ/flute!") and then gets nostalgic when they're vintage

("I want a Hammond+Leslie sound exactly like on

A Whiter Shade of

Pale

!"). The P-85 is not quite vintage, but it's getting there,

and when I go back to it I realize how much I missed the specific way

key velocity translates into bark.

Before my keyboard gets so vintage that it stops working, I decided to

capture its characteristic sound. Unlike a real piano where I'd need

a very quiet room, thoughtfully positioned microphones, and a robotic

finger, I can do all of this electronically and silently. The

keyboard takes MIDI input and sends audio to the headphone jack, so my

laptop can ask it to play specific notes and record how it responds.

I set this up yesterday morning before leaving to do Thanksgiving at

my dad's, with the idea that I'd poke at Claude over remote control to

guide it through any parts of the process it couldn't handle.

Unfortunately it managed to wedge the system by rapidly opening and

closing the audio device, and needed a

sudo killall

coreaudiod

to get going again. Since I couldn't do that

remotely I needed to pick it up when I got home that evening.

It was a bit awkward, because I'd been planning to do this remotely,

so the keyboard was partly where my chair would usually go. But I

shifted my laptop and monitor to the side and persevered.

Unfortunately, when it had finished and I gave it a try, I realized

I'd painstakingly captured its Grand Piano 1 sound. Which isn't

even the piano sound I like: I always use Grand Piano 2.

If I'd done any listening at all I would have noticed it wasn't

capturing the right voice, so I do feel pretty silly.

This morning I set it up again, keeping it out of the way of my chair,

and started debugging. The issue turned out to be that the voice

selection buttons don't affect what the keyboard does over MIDI.

Instead, it responds to the MIDI "bank select" and "program change"

commands. The ten voices are, zero-indexed:

Voice

Bank (LSB)

Program

Demo

Grand Piano 1

122

0

mp3

Grand Piano 2

112

0

mp3

E. Piano 1

122

5

mp3

E. Piano 2

122

4

mp3

C. Organ 1

123

19

mp3

C. Organ 2

122

19

mp3

Strings

122

48

mp3

Harpsichord 1

122

6

mp3

Harpsichord 2

123

6

mp3

Vibraphone

122

11

mp3

I was initially surprised that they'd put epiano1 and epiano2 on "5"

and "4" respectively, but actually this is not so weird: "4" is

normally a Rhodes-style electric piano, while "5" is normally an FM

piano. The actual surprising thing is that the keyboard puts the FM

piano sound first; normally they'd be the other way around. Perhaps

Yamaha wanted to feature the more complex FM synth sound their DX7 was

famous for?

I also got this set up as a voice in my

updated rhythm

stage setup

. Claude prepared it as a soundfont, and loaded it

into FluidSynth alongside my

other voices

. It's been fun to play

around with!

Possible future directions:

Switch my standard rhythm stage setup to use the computer for

the piano sound so I sound the same when I fly to gigs, with whatever

keyboard I'm playing.

Figure out whether I want to switch over to an 8-channel

interface when gigging so that I can give sound people more things

they can independently adjust.

Make a switchable "bark" overlay so that I can get this

keyboard velocity effect on anything.

Claude

estimates

it contributed 5% of words and 15% of ideas; it also wrote and ran the capture software, worked out the MIDI voice map, and built the soundfont, while I set up the keyboard, identified the voices by ear, and wrote the post.

Comment via:

facebook

,

mastodon

,

bluesky

0

Comments

0

World Modeling

Personal Blog

10

New Comment

Submit

Moderation Log

More from

jefftk

View more

Curated and popular this week

## AI 处理状态

等待 27 Skills 进行后续处理。
