---
layout: post
title: "To Bounty or Not To Bounty"
comments: true
categories: blog
tags:

- software
- business
- open-source

---

That, truly, is the question.

On the surface, bounties seem like they should be a good way to leverage the world's distributed software talent. Projects carve out bits of work which need to be done, put up cash for their completion, and wait for a member of the global engineering cloud to submit some code.

Especially in the world of Ethereum, the idea of bounties has captured the imagination. Two bounties platforms, [Gitcoin](https://gitcoin.co/) and [Bounties Network](https://bounties.network/), are among the most mature in the ecosystem. And yet, despite all the infrastructure, bountied freelancers have largely not replaced the full-time engineers as the primary source of software labor. Curiously, however, bounties _have_ found application as a way to incentivize bug reporting. Why might this be?

My hypothesis is that the reason why bounties work for security but not for general development is that the security skillset is much more fungible from codebase to codebase. Someone who is experienced in security can approach a new codebase and look for bugs _without_ needing to understand the codebase as a whole. The time invested in building a security skillset is amortized over many bug bounties, and so coasting from bug bounty to bug bounty can be a reasoanble way to make money.

For general software development, however, the economics are different. When an engineer first joins a project, there is a fair amount of onboarding needed before that engineer can become an effective contributor. They must read through and understand the codebase, the conventions, the roadmap. This is difficult and non-fungible work but generates little to no value for the project, while also generating mostly _specific knowledge_ which cannot be transferred to other projects. That engineer's first contribution, which might be small from the project's perspective, may actually represent a significant amount of work by the engineer. The longer an engineer works on a particular codebase, the more they are able to amortize the cost of their onboarding: their tenth contribution might be significantly more impactful than their first, while actually taking only a fraction of the time. For this reason, bounties are a poor means of incentivizing this type of work as bounties do not allow the engineer (or the company) to amortize the cost of the onboarding (this is part of the reason why there is a norm to stay at a job for at least one year). For an engineer to sustain themselves via bounties, it will be more efficient for them to contribute exclusively to a single (or perhaps few) projects to allow them to better exploit their project-specific context. If this is the case, then this person is functionally a full-time employee.

If it is true that the incentives for bounties for general software development converge naturally to project-specificity, it may be better for projects to recruit a core of salaried engineers than to attempt to solicit labor exclusively via bounties.
