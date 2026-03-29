---
layout: post
title: "Implementing Active Select"
comments: true
categories: blog
tags:
- algorithms
- mechanism-design
- social-choice
---

<!-- For the raw commit log and research notes, run the following command -->
<!-- gh api repos/dojoengine/daimyo/commits --paginate -q '.[] | "\(.sha[0:8]) \(.commit.author.date[0:10]) \(.commit.message)"' -->

Social choice is often about allocating fixed resources among a set of items: a funding pool across projects, a budget across priorities, prize money across submissions.
The core problem is producing *weights* -- percentages out of 100 which say how valuable each item is relative to the others.

A common approach -- asking people to score items on a scale -- is fast but unreliable.
Scores are subjective and uncalibrated: one person's 7 is another person's 4.
Pairwise comparison sidesteps this by asking a simpler question: "Which of these two do you prefer, and (optionally) by how much?"
The cognitive load per judgment is lower, the signal is cleaner, and the results can be converted into weights that reflect genuine collective preference -- from which rankings, allocations, and funding decisions all follow.

The problem is cost.
Pairwise comparison scales quadratically: $$k$$ items means $$k(k-1)/2$$ possible pairs which need deciding.
*Active ranking* -- choosing which pairs to show based on what the system has already learned, thus significantly reducing the number of pairs you most observe -- is key to making pairwise methods practical.

This essay will explore how active ranking worked in practice -- over three weeks in February and March 2026, during a live game jam -- for PowerRanker, a spectral ranking engine that turns pairwise preferences into distributions of weights over items.

> The project was done in collaboration with Claude, and this essay drafted from the [git commit logs](https://github.com/dojoengine/daimyo/commits/main/) and edited for flow.

## I. Background

For the last year, I've been working with the Cartridge Gaming Company, and one of my responsibilities is running their hackathons.
When it came time to judge submissions, I saw an opportunity to put the ideas from [The Pairwise Paradigm]({% post_url 2025-12-14-pairwise-paradigm %}) into practice -- not just active ranking, but the full end-to-end pipeline: interface design, data encoding, and algorithmic pair selection.

The result was a judging tool built into [Daimyo](https://daimyo.cartridge.gg/), Cartridge's homespun game jam platform.
Judges would see two submissions side by side -- each with an AI-generated summary, playable links, and structured metrics -- and were asked a single question: "Which is the stronger game jam entry?"

![Daimyo Judging Interface](/img/daimyo-judging.jpg)

Responses used a five-point Likert scale (Much / Slightly / Even / Slightly / Much), which we encoded as values from 0 to 1 in increments of 0.25.
Each judgment was intended to take about 30 seconds, and judges were asked for 10 comparisons per session, keeping the total time commitment under five minutes.
PowerRanker then aggregates these comparisons into a collective weighting, used for deciding winners and giving out prizes.

The initiative was successful -- judges enjoyed encountering the projects in this way, the process made the game jam more visible to the larger ecosystem, and we were able to produce good results with a relatively small voter lift.

Of the ideas from the Pairwise Paradigm, active ranking was the one that required the most development during this process.
The original proposal was straightforward: for every pair $$(a, b)$$, construct a [Beta distribution](https://en.wikipedia.org/wiki/Beta_distribution) from the vote counts and sample pairs proportional to $$\text{Var}(p_{ab})$$.
An optional extension would weight by $$\text{Var}(p_{ab}) \cdot w_a \cdot w_b$$, upsampling uncertain pairs between high-value items.
In theory, this would reduce the data requirement from $$O(k^2)$$ to some multiple of $$k$$, a fundamental change in complexity.

This was the plan.
Then we tried to use it.

## II. Variance-Based Selection

The initial implementation followed the original proposal: Beta-variance-weighted sampling without replacement, with an optional impact flag that multiplied variance by the product of both items' current weights.

It worked, in the sense that it produced pairs and rankings converged.
But watching it run against real data, two problems became clear.

Variance sampling did explore -- unobserved pairs have the highest variance under a Beta prior, so the system naturally surfaced unseen comparisons.
But it explored indiscriminately, without regard to relative ordering.
The system would spend votes resolving the bear-vs-rabbit comparison with the same urgency as bear-vs-lion, even though these comparisons are not equally important for discovering the final ordering.
Variance told us what we hadn't *seen*, but not what we *needed to see*.

The weight-scaling extension -- multiplying variance by $$w_a \cdot w_b$$ -- introduced a different problem: path dependence.
With sparse early data, the ranking engine produces extreme weights -- an item that wins its first two comparisons can briefly appear to dominate the entire set.
Scaling by these volatile early weights meant that early winners were shown far more often, which produced more data about them, which reinforced their high weights.

Together, these issues suggested that variance alone wasn't enough.
The question was whether it could be rescued with additional terms, or whether it needed to go entirely.

## III. Composable Transforms

Before abandoning variance, we tried to save it.
The first iteration added a **coverage** term alongside variance.
Coverage tracked how many times each item had been observed in any comparison, and penalized well-observed items: $$1/(1 + n/N)$$ initially, then $$1/\sqrt{1 + n}$$ for stronger early exploration.

The idea was to balance exploitation (compare uncertain pairs) with exploration (compare unseen items).
We also reintroduced a **weight** term using the geometric mean of PageRank weights, compressed via sqrt to keep it in range with the other factors.
The goal was to observe all pairs a few times, and then concentrate observations both on similarly-ranked items, as well as the top-weighted items, directing attention to where it had the highest impact.

This was better.
Items that had been ignored got surfaced, and high-value items got more attention.
But the variance component still created path dependence, and the interaction between three multiplicative terms (variance, coverage, weight) was hard to reason about.
We spent a week tuning coverage: $$1/(1+n/N)$$, then $$1/\sqrt{1+n}$$, then back to $$1/(1+n)$$.

The tuning was producing results, but the deeper problem remained.
Variance is a backward-looking signal: it tells you what you don't know about past comparisons.
What we actually wanted was a forward-looking signal: which comparison would be most informative *given what we already know about the ranking*?

Variance was the wrong signal entirely.

## IV. The Pivot

On March 13, we abandoned it after reaching a pair of insights.
First: variance is indifferent to where items sit in the ranking.
A high-variance pair at the top of the distribution and a high-variance pair at the bottom look identical, but only one of those comparisons helps resolve the final ordering.
Variance-based selection would happily spend votes confirming that the bear beats the rabbit -- exactly the comparison we didn't need.
If the goal is to reduce ranking to $$O(n)$$ comparisons, the selection signal has to be order-aware.

Second: sleection based on weights is potentially misleading, since people don't vote on weights -- they vote on pairs.
Voters decide on _items_, and so we needed to surface close pairs, regardless of whether their underlying weights were 0.1 or 0.001.

These two observations pointed toward a design built entirely on position, ignoring weight and variance completely.
The replacement was `activeSelect()`, built on three multiplicative terms, which could be toggled on and off individually.

- **Coverage**: $$\frac{1}{\sqrt{1 + n_a}} \cdot \frac{1}{\sqrt{1 + n_b}}$$ -- favors items with fewer observations
- **Proximity**: $$\frac{1}{1 + \lvert pos_a - pos_b \rvert}$$ -- favors items close together in the current ranking
- **Position**: $$\frac{1}{\sqrt{pos_a \cdot pos_b}}$$ -- favors items near the top

The justification for proximity is structural.
A weighting of $$n$$ items has $$n-1$$ degrees of freedom -- the ratios between consecutive items.
This means the goal of the pairwise process should be to achieve high confidence on the relationship between each item and its neighbors.
With a budget of ten to twelve comparisons per item, this clustering should produce the tight local ratios needed for quality final
weights.

> "Neighbor" should be understood probabilistically -- ideally, observations cluster around each item's local neighborhood, two or three comparisons with items one or two positions away, one or two comparisons with items three or four positions away, etc.

The intuitive model is an amorphous graph gradually tightening into a clean ordering as votes come in.

Early on, the graph is sparse and the ranking is fuzzy, so coverage dominates: every item needs a few comparisons to anchor its position before proximity can meaningfully guide selection.
As data accumulates and the ranking stabilizes, proximity dominates, concentrating attention on the boundaries where more precision is useful.
Position adds a constant bias toward the top of the ranking, where getting the ordering right matters most for downstream allocation -- though for our use case, this term proved to be overkill.

## V. Tuning

The new design required its own round of tuning, but the iterations were faster and more principled because the terms were independently interpretable.
Claude could perform fast simulations, letting us explore the behavior of different parameterizations interactively.

**Range matching.** A subtlety of multiplicative composition is that all terms need to operate on similar scales.
If one term ranges from 0.00001 to 0.99999 while the others range from 0.2 to 0.6, the wide-range term effectively determines the outcome alone.
Getting the terms into comparable ranges -- so that their interactions were meaningful and intuitive -- was a recurring concern throughout tuning.
Thinking about the scales of terms -- and how they might be multiplied, squared, or rooted -- became a constant practice.

**Regularization.** The first version had no way to soften the weighting.
In production, under-observed entries were getting starved while already-ranked items dominated.
We added a regularization parameter `r` (0 = uniform, 1 = full weighting), which let us sample randomly and minimize unintended path-dependence.

The initial implementation was a linear blend: $$r \cdot w + (1 - r)$$.
This didn't work: the blend collapsed signal, producing useless values like 0.500001.
We replaced the linear blend with a **power transform**: $$w^r$$, producing a range between uniform and fully-weighted while preserving signal.

**Coverage formula.** The coverage term oscillated between $$1/(1+n)$$ and $$1/\sqrt{1+n}$$ across the project as we ran simulations and explored alternative paramaterizations.
The sqrt form was ultimatley gentler, allowing items with 3-4 observations to continue to appear while still favoring items with zero observations.

**Term composition.** Initially, we chose pairs using all three terms, but decided mid-jam to drop the position term and use coverage and proximity with `r=0.9`.
This made it easier to distribute voter attention across the entire set of items, which increased legitimacy.
This decision reveals an important subtlety in social choice: perceived legitimacy of a process just is as important as how close the final weights may come to an abstract ideal.

## VI. Validation

After the design stabilized, we ran simulations to validate the approach quantitatively.
We generated items with known power-law weights, simulated judges making noisy Bradley-Terry comparisons, and measured how well the ranking engine recovered the true ordering.

The simulation also clarified [a foundational question]({% post_url 2026-02-07-reinventing-the-wheel %}) about the ranking engine itself: whether preferences should be unidirectional (A is better than B) or bidirectional (A is better than B *and* B is worse than A).
With Likert-binned utilities (votes were encoded as 0, 0.25, .5, .75, 1), unidirectional preferences produce unbounded weight ratios as data accumulates -- the top item's weight grows without limit relative to the bottom, as preference "mass" accumulated unevenly.
Bidirectional preferences, by contrast, cause weights to converge, because every comparison contributes balanced information.
This distinction, while not directly about active selection, was essential for understanding what "convergence" means in the system we were trying to optimize -- and is a jumping off point for future research.

Our independent variable was **votes per item (vpi)**: the average number of comparisons each item participates in.
We wanted to know _how many votes_ we needed to get before we could publicize the results.
Results showed that with active selection, Spearman rank correlation reaches 0.95+ at around 12 vpi for most distributions.
Random pair selection requires significantly more data to reach the same accuracy.

The simulation served two purposes.
It helped balance the relative weighting of the three terms, confirming that the range-matching intuition from manual tuning was correct.
And it gave us confidence in the votes-per-item target, by showing that an accurate ordering can be reliably recoverred within our vote budget.

For a set of 50 items, 12 vpi means about 300 total votes, or 30 judges each making 10 comparisons.
At 30 seconds per comparison, that's 5 minutes per judge.
This is close to the Pairwise Paradigm's $$O(k \cdot 10)$$ estimate, achieved through a different mechanism than originally proposed.

## VII. Reflections

**Theory vs practice.**

The variance-based approach made sense on paper.
It was information-theoretically motivated, computationally efficient, and had a clear connection to the existing literature.
But it failed in practice because it treated pairs as isolated statistical objects rather than as part of a ranking structure.
The position-aware model succeeded because it grounded the selection process in the ranking it was trying to refine.

**Composability matters.**

The ability to drop or add terms based on context proved valuable in production.
A single monolithic scoring function would have been harder to adapt.

**The weights weren't ready for prime time.**

We had initially hoped to distribute prize money directly using the output weights -- the highest-impact use of PowerRanker.
But in the end, we didn't feel confident enough in the weight precision to tie dollars to them, especially as the selection process itself evolved over the course of vote-gathering.
To maintain legitimacy, we gave out funding based on rank order, with amounts decided externally.
The _ranking_ was reliable, but the _weights_ need more data and validation before they can be financially load-bearing.

**Open questions remain.**

The first iteration of Daimyo validated many of the ideas put forward in The Pairwise Paradigm, specifically around the design of the UI and the value of active ranking as a way to reduce the voting requirement.
Future research should push the simulations further, showing specifically under what circumstances different paramaterizations can achieve desired outcomes -- while remembering that real data are never so simple.

This research, like the [earlier work on pseudocounts]({% post_url 2026-02-07-reinventing-the-wheel %}), was conducted in collaboration with Claude -- both the R&D itself and the writing of this essay.
The pattern was similar: rapid iteration through a search space, punctuated by moments where stepping back and questioning the frame proved more valuable than another round of tuning.
The variance-to-position pivot was the frame-questioning moment here, analogous to the damp-before-normalize insight in the earlier project.
In both cases, the right answer was not a better parameter for the existing approach, but a different approach entirely.
