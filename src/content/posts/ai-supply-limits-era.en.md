---
lang: en
title: "Two Big Events in One Week: AI Is Entering the Era of Limited Supply"
date: 2026-07-21T10:00:00+08:00
categories: ["AI", "News"]
description: "Kimi suspends new user subscriptions + Fable 5 requires identity verification—two seemingly unrelated events point to the same trend: the most advanced AI is no longer enough."
---

Two seemingly unrelated events in the AI industry this week actually point in the same direction:

**July 20**: Moonshot AI's Kimi announced that due to severe compute shortages following the K3 release, it would immediately suspend new consumer subscriptions. At the same time, Kimi has notified investors of a corporate restructuring in preparation for a Hong Kong IPO.

**Starting July 8**: Fable 5 switched to a Usage Credits model, requiring Persona identity verification to purchase credits.

## The Supply Side Can't Keep Up

The surface reason for Kimi suspending new users is "K3 is too popular," but the deeper reason is: **the inference compute for top-tier AI models is finite**.

For a model with 2.8 trillion parameters, the computational cost of each inference is astronomical. Even with ample GPU reserves, Moonshot AI can't withstand the surge in users after release. Within 48 hours of K3's announcement, registered users reportedly grew by tens of times—no company can handle that kind of growth curve.

This reminds me of the situation after DeepSeek V3's release earlier this year: frequent API rate limiting, soaring response latency. It wasn't that the model was inadequate—it was that compute was insufficient.

Fable 5's situation is similar but for a different reason—it's not a compute shortage but scarcity *manufactured* by policy. Identity verification plus the Usage Credits model artificially limits the user base.

## What Does Scarcity Mean?

A bottle of water costs a dollar at the supermarket and a hundred dollars in the desert. AI capabilities work the same way.

If the most advanced AI (Fable 5, Kimi K3) becomes a scarce resource:

- **Only enterprise users with the strongest willingness to pay get stable access.** Individual developers, students, and small teams will be squeezed out.
- **API prices will rise.** Even if list prices stay the same, actual usage costs will increase due to rate limiting and queuing.
- **Local deployment of open-source models will accelerate.** If cloud APIs are both expensive and slow, downloading models to run on your own GPUs becomes a sensible choice—but that requires you to have GPUs.

Essentially, AI is regressing from a "public service available to everyone" to a "premium service requiring credentials."

## What Does This Mean for Developers?

A few practical suggestions:

**First, don't put all your eggs in one API basket.** Your application should be able to quickly switch between different model providers. Today Kimi suspends new users, tomorrow OpenAI raises prices, the day after Anthropic changes its policies. An abstraction layer isn't over-engineering—it's insurance.

**Second, local models are worth investing in.** You don't need to run K3 (nobody can run a 2.8T-parameter model), but smaller open-source models like DeepSeek V4, Llama 4 7B/13B, and Qwen 3 can run on your own hardware. That's sufficient for 80% of use cases.

**Third, cherish your API quota.** Fable 5's Usage Credits pricing won't be cheap, and even if Kimi K3 is "freely accessible," it will have rate limits. Use the most powerful models where they matter most—complex reasoning, long-horizon agents—and use cheaper, faster models for routine tasks.

## Reflection

A year ago we were discussing "when will AI become too powerful." Now we're discussing "AI is so powerful that there isn't enough of it." No one anticipated how quickly the conversation shifted.

The supply bottleneck for AI capabilities—whether technical (compute shortages) or policy-driven (export controls)—will be the most important industry issue over the next few years.

The good news: competition is accelerating. K2 was followed by K3 just a week later. The arms race in model capabilities shows no signs of slowing. Scarcity is temporary; capability is growing.

But during this transition, developers' strategy needs to shift from "use freely" to "use wisely." What's in limited supply isn't AI—it's the **best** AI.

---

**References:**

- [Zhihu — How to view Moonshot AI's Kimi announcement of compute shortage and suspension of new users (2026-07-19)](https://www.zhihu.com/question/2062310754481656074)
- [Anthropic — Redeploying Claude Fable 5](https://www.anthropic.com/news/redeploying-fable-5)