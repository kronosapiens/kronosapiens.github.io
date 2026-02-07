---
layout: post
title: "Reinventing the Wheel"
comments: true
categories: blog
tags:
- algorithms
- mechanism-design
- cooperative-housing
---

> This essay describes a research process culminating in a significant overhaul of Chore Wheel's Chores system.
The research itself -- [analysis, dead ends](https://github.com/zaratanDotWorld/choreWheel/issues/296), and [eventual solution](https://github.com/zaratanDotWorld/choreWheel/pull/302) -- was a collaboration between myself and Anthropic's Claude taking place over the course of about a week.
Afterwards, I had Claude help me write up this research report based on our notes.

- [I. Introduction](#i-introduction)
- [II. Background](#ii-background)
- [III. Explorations](#iii-explorations)
- [IV. Breakthrough](#iv-breakthrough)
- [V. Reflections](#v-reflections)

# I. Introduction

[Chore Wheel](https://www.zaratan.world/chorewheel) is a cooperative household management system, deployed as a suite of Slack apps since September 2022.
Its origins trace back to my research on pairwise preference voting as a [master's student at Columbia in 2016](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3359677), [further developed at Colony in 2018](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3317445), and [culminating in Chore Wheel in 2020](https://blog.zaratan.world/p/the-story-of-chore-wheel).

The core concept is straightforward: residents express priorities as pairwise comparisons ("dishes are more important than sweeping"), and a [PageRank-style algorithm]({% post_url 2025-12-14-pairwise-paradigm %}) aggregates these into a collective prioritization that determines how many points each chore accumulates.
Points are fixed at 100 per resident per month and distributed continuously over time.
A chore prioritized twice as highly accumulates twice as many points, so the collective preferences directly shape how chores are incentivized and performed.
The emphasis on _emergent, intuitive, and asynchronous decision-making_ -- in lieu of long meetings or top-down manager control -- was meant to ensure communal resilience in the face of turnover and fluctuating resident capacity.

After 3+ years of continuous production use at Sage House -- with over 2,500 claimed chores and multiple generations of residents -- the system had proven the concept.
The prioritization mechanism, the system's most innovative component, worked.
But consistent patterns of user frustration pointed to problems beneath the surface.
This essay traces the research process that led to a key redesign of the ranking engine -- not as a straight line, but as the winding path it actually was.

# II. Background

### The Problem

Chore Wheel's goal is to make cooperative governance simple, intuitive, and effective.
Two persistent complaints suggested the goal was not yet fully achieved.

The first was **compressed distributions**.
Residents struggled to get the most important chores to high enough values.
No one ever complained that the top chores were worth "too much" -- but people regularly felt unable to push them high enough, no matter how many preferences they submitted.
Deep-cleaning a bathroom and watering the plants would sit closer together in the rankings than anyone felt they should, and no amount of voting seemed to fix it.
The result was that the most important chores still felt undervalued, and that people who did them still felt as though they were "sacrificing" on behalf of the group.

The second was **opaque causality**.
Priority changes often felt somewhat "random."
A resident would submit a clear preference -- "kitchen deep clean matters more than yard cleanup" -- and see unrelated chores shift in unexpected directions.
The effect wasn't enormous, but it was noticeable.
When inputs don't produce legible outputs, governance stops feeling democratic and starts feeling arbitrary -- and residents disengage.
For a system built on the premise that people should feel agency over their shared environment, this was not a minor complaint.

### The Ranking Engine

To understand the source of these problems -- and why they resisted easy fixes -- requires some background on how the ranking engine works and the design decisions it inherited.

PowerRanker takes in pairwise preferences from residents ("I prefer dishes to sweeping with a strength of 0.7"), aggregates them into a matrix of relationships, and turns this matrix into a set of weights ("priorities") which we use to assign points to chores.
The underlying math is well-established and is often used to calculate rankings based on tournaments and competitions; our innovation was applying it to problems of social choice.

One of the challenges of the social choice setting is achieving the twin -- and often contradictory -- goals of enabling groups to reach good outcomes in the face of low engagement, while also preventing minority factions from unfairly dominating the results.
Achieving these goals requires balancing trade-offs -- requiring coalition-building for extreme outcomes, while allowing individuals to make meaningful contributions.

This balancing, which can be seen as a type of "regularization," was previously done in two ways.
First, through an "implicit preference" of 0.5 assigned to every chore, which was removed proportionally (0.5/numResidents) as real preferences came in.
Second, through a "damping factor" -- taken directly from PageRank -- in which the observed preferences are scaled down and combined with a uniform prior (PageRank's "random surfer"), which compresses results and ensures that even low-priority chores receive at least _some_ value.

> Note: The original PageRank paper counterintuitively dampens _less_ when $$d$$ is large.
In this discussion, we will refer to "high damping" as creating more uniform outcomes, and "low damping" enabling more extreme outcomes.

### Prior Investigations

This project occurred in the context of a larger sweep of improvements brought about by the addition of a new house (see [here](https://github.com/zaratanDotWorld/choreWheel/pull/289), [here](https://github.com/zaratanDotWorld/choreWheel/pull/292), and [here](https://github.com/zaratanDotWorld/choreWheel/pull/294)).
This 5-person house, Solegria, had a different set of needs than Sage, and attempting to accommodate their needs _within_ the existing framework spurred a series of investigations which led to significant improvements in the system.

Before this project, we undertook an investigation into some confusing behavior which surfaced in the course of implementing a "bulk import" feature in which CSVs of chores could be uploaded instead of created and prioritized individually.
During the development of the import functionality, [we noticed that equal preferences lead to highly skewed outputs](https://github.com/zaratanDotWorld/choreWheel/issues/295), which itself turned out to be an unintended consequence of [an earlier investigation](https://github.com/zaratanDotWorld/choreWheel/issues/224) into why de-prioritizing a chore could in some cases _increase_ its priority.

That earlier fix had moved from bidirectional preferences -- in which a preference of (A, B, 0.7) was encoded as (A, B, 0.7), (B, A, 0.3) -- to unidirectional preferences, which encode only (A, B, 0.7).
Bidirectional preferences were appealing in that they made changes continuous, symmetric, and proportional.
The downside, however, was that in the context of the PageRank algorithm, the addition of (B, A, 0.3) would in fact _increase_ the ranking of B -- a clear semantics violation.
The unidirectional solution, on the other hand, avoided unintended interactions at the cost of more volatile rankings due to the loss of the natural "damping" of the counter-preference.
We attempted to mitigate this volatility by "scaling" the unidirectional preferences so that they rotated more cleanly around 0.5 (i.e. 0.7 would scale to 0.4).

Things had begun to feel like a game of whack-a-mole, with every solution introducing another problem.
A new approach to regularization was needed, one that was cleaner and more well-defined.
It was clunky, we thought, to have a general-purpose ranking tool be hard-coded to depend on a domain-specific value like $$\text{numResidents}$$.
Exploring alternative approaches to damping and regularization set us down a road which led to a significant breakthrough.

# III. Explorations

### Bidirectional Preferences with Dynamic Damping

At the highest level, our goal was to capture the "semantics" of prioritization as much as possible -- proportionally higher preference should lead to proportionally higher priority, always and under all circumstances.

The first attempt was, in retrospect, the most obvious one: remove implicit preferences, instead regularize by making explicit preferences bidirectional again, and replace the fixed damping factor with a data-driven one that increases as a function of explicit preference data.

By making the damping factor data-driven instead of a fixed parameter, it can replace the regularizing function of implicit preferences by ensuring that a small number of preferences could not dominate the results.

The initial damping formula was a hyperbolic curve, where $$P$$ is the number of preferences submitted and $$\text{maxPairs}$$ is the total number of possible chore pairs:

$$
d = \frac{P}{P + \alpha \cdot \text{maxPairs}}
$$

With few preferences, damping stays high and rankings hew close to uniform -- conservative, appropriate for thin data.
As preferences accumulate, damping decreases and the rankings increasingly reflect people's stated preferences.

We tested this against anonymized Sage House preferences and found that the empirically fitted $$\alpha$$ came to 0.48 -- nearly identical to the theoretically predicted value of 0.5.
The old and new rankings were nearly identical, essentially the same output through a cleaner mechanism.

The theoretical justification for $$\alpha = 0.5$$ was satisfying.
Not all preference weight creates ranking differentiation.
Each bidirectional preference adds a total weight of 1.0, but only the asymmetric component -- the amount by which the preferred chore exceeds the other -- creates signal.
For Sage's data, where the vast majority of preferences were maximal, the effective signal was roughly half the total weight.
Hence $$\alpha \approx 0.5$$.

This was promising.
It removed implicit preferences, replaced the fixed damping factor with something principled, and produced nearly identical rankings on real data.
The next step was to validate on a second dataset.

### Cross-Dataset Validation

The second dataset, from Solegria, told a different story.
Where Sage residents had submitted preferences organically -- mostly maximal values, spread across several active participants -- Solegria had a very different participation structure.
One person had submitted the vast majority of all preferences through the bulk-upload feature, and those preferences were derived from intended point values, producing a more moderate distribution of preference strengths.

The fixed $$\alpha = 0.5$$ still produced reasonable rankings, but an adaptive $$\alpha$$ based on preference intensity improved accuracy noticeably.
The formula measures how far the average preference deviates from neutral -- for Sage's near-maximal preferences, this gives $$\alpha \approx 0.49$$; for Solegria's more moderate preferences, $$\alpha \approx 0.31$$:

$$
\alpha = \frac{\text{mean}(|2(p - 0.5)|)}{2}
$$

However, regularizing based on explicit preferences would have introduced a new reflexivity: if strong preferences regularize themselves, preference-setting becomes less about expressing true beliefs and more an exercise in anticipating how the algorithm will react.
This was a complexity we were unwilling to introduce.

More wrinkles emerged when we tested round-trip fidelity: since Solegria's preferences were generated from known target scores, we could check whether the ranking algorithm recovered the intended distribution.
It didn't.
The $$\alpha = 0.5$$ formula, which worked well for Sage, significantly compressed rankings relative to Solegria's intended values.

Our takeaway was that for hyperbolic damping, the model's core parameter was sensitive not just to the _amount_ of data, but to its _distribution_.
There was not a universal constant we could apply without significantly distorting either group's current, in-production priorities -- something we were not willing to do as part of an internal research project.
Our goal was to make fundamental improvements either _transparently_ or not at all.

> It is worth noting that these data are slightly reflexive -- Sage residents produced extreme values in part _because_ the overly-strong compression was not responsive enough to moderate values.

### The Coalition Problem

Before abandoning the hyperbolic approach entirely, a different concern surfaced.
The damping formula counted total preferences without regard to _who_ submitted them.
One determined person submitting hundreds of preferences achieved nearly the same damping as several people submitting partial sets of preferences.
This defeated the coalition-building property that $$\text{numResidents}$$ had -- however crudely -- provided originally.

A fix was inspired by [Quadratic Voting]({% post_url 2020-04-19-sharing-the-wealth %}): compute an *effective* participation score as the sum of square roots of each resident's preference count:

$$
\text{effectiveP} = \sum_i \sqrt{\text{prefs}_i}
$$

This gives diminishing returns per person -- one person submitting 100 preferences contributes $$\sqrt{100} = 10$$, while four people submitting 25 each contribute $$4\sqrt{25} = 20$$.
More participants means higher effective participation, mathematically enforcing the normative value of coalition-building.

The idea was architecturally clean.
PowerRanker would become a generic library that accepts damping as a parameter, knowing nothing about residents or participation.
The application layer would compute $$\text{effectiveP}$$ from its knowledge of who submitted what, derive the damping factor, and pass it in.
Separation of concerns.

But this penalized Solegria's _legitimate_ use case -- a single person doing a bulk import on behalf of the group -- and more generally, any house where one or two engaged members did most of the administrative work.
The instinct about coalition-building was right; the implementation was simply too aggressive -- and too normative -- for the messy reality of shared living, where participation is never evenly distributed.

### The Search for a Universal Curve

At this point we stepped back and asked a different question: is there another curve that works consistently across different houses and coverage levels?
We were converging on the following input for the damping curve: $$P/maxPairs$$.

This value, the ratio of the number of observed preferences across _all residents_ and the number of possible preferences _per resident_, could range from 0 up to the number of residents.
What was the curve that could cleanly map this number to the range (0, 1)?
The answer was the sigmoid:

$$
d = \frac{1}{1 + e^{-a \cdot P / \text{maxPairs}}}
$$

Both formulas normalize by problem size, but they differ in _shape_.
The hyperbolic starts at $$d=0$$ with no data, meaning cold-start houses get near-total damping, while the sigmoid starts at $$d=0.5$$ -- an intuitive "50/50 blend with uniform" -- and its steeper S-curve transition meant a single parameter could work across both datasets.

We swept the steepness parameter $$a$$ across both datasets, looking for a value that most closely matched current production.
The result was encouraging: a single parameter value worked well for both houses.
Rankings shifted modestly, with slightly increased spread in both cases and minimal rank-order disruption.
This seemed like the answer.

But looking back at the full trajectory of the research, something nagged.
Four different damping formulas had now been explored -- hyperbolic, QV-weighted hyperbolic, sigmoid, and adaptive variants of each -- always asking "what's the right damping curve?" without questioning whether functional damping was the right tool at all.
The concept had been inherited from PageRank and never seriously challenged.
Every iteration refined the curve; none questioned the frame.

# IV. Breakthrough

### Damp-Before-Normalize

The frame did crack, though not in the way we expected.

Standard PageRank normalizes each row of the transition matrix (so rows sum to 1), _then_ applies damping (blending with the uniform distribution).
But normalization erases the *magnitude* of the raw preference data: an item with 10 strong preferences and an item with 1 weak preference look identical after normalization, because both rows sum to 1.
In PageRank this doesn't matter -- the link matrix is binary, so pre-normalization row sums just count outgoing links, which carry no information about page authority.
In a continuous preference matrix, the pre-normalization row sums encode something meaningful: how much total evidence the system has about each item.
We were throwing away information that the original PageRank never had to think about.

With bidirectional preferences and implicit preferences, this effect was obfuscated, as the normalizing effect was constrained by these additional values.
With unidirectional preferences and no implicit preferences, the problem with normalize-before-damp became plain as day:

![Damp Before Normalize](/img/damp-before-normalize.jpg)

*Fancy models and AI agents are no match for a good notebook at your side.*

This was the conceptual breakthrough of the research -- the first moment where the PageRank formalism itself, not just its parameters, was questioned.
By reversing the order -- damping first, then normalizing -- we can regularize outputs _without_ washing out valuable preference information.
The principle is simple: **regularize before you normalize**, so that cells with more real data are proportionally less affected by the prior.

Key mathematical properties were preserved: the final matrix is still row-stochastic, irreducible, and aperiodic, guaranteeing a unique stationary distribution via Perron-Frobenius.
Only the clean markov-plus-uniform decomposition of the classic Google matrix was lost -- but that decomposition, and its "random surfer" interpretation, was arguably never the right model for social choice anyway.

The damp-before-normalize approach still relied on a functional damping curve, though, which meant it still inherited the parameterization problems from the earlier sections.
**What we needed was a way to regularize _before_ normalization without relying on a curve at all.**

### Bayesian Pseudocounts

The implementation of this insight turned out to be embarrassingly simple.
Preferences remained unidirectional -- the bidirectional approach explored earlier had been purely analytical, never shipped -- and the new regularization required only one change: add a small constant to every off-diagonal cell in the matrix before loading the data.

$$
k = c \times \text{numResidents}
$$

That's it.
Each chore pair starts with $$k$$ units of "virtual preference" in both directions, representing a uniform prior belief before any data arrives.
As real preferences accumulate, they dominate the pseudocounts naturally -- no deleting implicit preferences, no coverage-dependent formula, no steepness parameter, no damping factor at all.

There is an irony here.
Pseudocounts do what implicit preferences were trying to do all along: provide a uniform baseline that washes out as real data arrives.
But where implicit preferences were a hack -- entangled with damping, lacking a clean mathematical interpretation, creating indirect effects through bidirectional subtraction -- pseudocounts have a principled statistical identity.
They are a [Dirichlet prior](https://en.wikipedia.org/wiki/Dirichlet_distribution), the standard Bayesian approach to regularizing categorical distributions.
The original system had the right instinct; it just expressed it through the wrong formalism.

The pseudocount approach has several properties that none of the damping-based models achieved:

- It **scales with house size**: more residents means a stronger prior, which means more preference data is needed to move rankings -- exactly the right behavior, since a single vote should matter more in a 3-person house than in a 20-person house.
- It provides **per-cell regularization**: cells with more real data are less affected by the prior, unlike global damping which applies a single blend ratio to every cell.
- It exhibits **cross-dataset stability**: the spread ratio stays consistent across both test datasets without parameter tuning.
- And it requires a **single parameter** $$c$$ with clear semantics, chosen analytically (or through governance).

Most strikingly, **the implementation was a net deletion of code.**
The old matrix initialization populated every off-diagonal cell with implicit preferences scaled by the number of participants:

{% highlight javascript %}
// Before: implicit preferences
_prepareMatrix () {
  let matrix = linAlg.Matrix.zero(n, n);
  if (this.options.numParticipants) {
    matrix = matrix
      .plusEach(1).minus(linAlg.Matrix.identity(n))
      .mulEach(numParticipants).mulEach(implicitPref);
  }
  return matrix;
}
{% endhighlight %}

The new version initializes with pseudocounts -- a uniform prior that knows nothing about participants:

{% highlight javascript %}
// After: pseudocounts
_prepareMatrix () {
  let matrix = linAlg.Matrix.zero(n, n);
  if (this.options.k) {
    matrix = matrix
      .plusEach(1).minus(linAlg.Matrix.identity(n))
      .mulEach(this.options.k);
  }
  return matrix;
}
{% endhighlight %}

Adding preferences went from a multi-step dance -- subtract implicit preferences, then add the scaled explicit preference in the dominant direction -- to simple addition:

{% highlight javascript %}
// Before: subtract implicit, then add explicit
preferences.forEach((p) => {
  const scaled = (p.value - 0.5) * 2;
  if (scaled !== 0) {
    matrix.data[sourceIx][targetIx] -= implicitPref;
    matrix.data[targetIx][sourceIx] -= implicitPref;
    if (scaled > 0) {
      matrix.data[sourceIx][targetIx] += scaled;
    } else {
      matrix.data[targetIx][sourceIx] += -scaled;
    }
  }
});
{% endhighlight %}

{% highlight javascript %}
// After: just add
preferences.forEach((p) => {
  const scaled = (p.value - 0.5) * 2;
  if (scaled > 0) {
    matrix.data[sourceIx][targetIx] += scaled;
  } else {
    matrix.data[targetIx][sourceIx] += -scaled;
  }
});
{% endhighlight %}

And the power method dropped its damping step entirely -- regularization now lives in the data, before normalization, not after:

{% highlight javascript %}
// Before: normalize, then damp
_powerMethod (matrix, d, epsilon, nIter) {
  matrix.data = matrix.data.map((row) => {
    const rowSum = this.#sum(row);
    return row.map(x => x / rowSum);
  });
  matrix.mulEach_(d);
  matrix.plusEach_((1 - d) / n);
  // ... power iteration
}
{% endhighlight %}

{% highlight javascript %}
// After: just normalize
_powerMethod (matrix, epsilon, nIter) {
  matrix.data = matrix.data.map((row) => {
    const rowSum = this.#sum(row);
    return row.map(x => x / rowSum);
  });
  // ... power iteration
}
{% endhighlight %}

The application layer computes $$k = c \times \text{numResidents}$$ and passes it in -- separation of concerns between the generic library and the domain-specific application.

We tested pseudocounts against both production datasets, and the results told two different stories -- both encouraging.
At Sage (9 residents), individual chore values shifted by an average of 0.08% -- nearly invisible.
At Solegria (5 residents), values shifted an average of 0.55%, with the spread between highest- and lowest-priority chores nearly doubling.

The difference is explained by the prior.
The old model initialized every off-diagonal cell with a fixed 0.5 units of implicit preference, regardless of house size.
The pseudocount model scales the prior with residents: $$k = 0.05 \times 9 = 0.45$$ for Sage -- almost identical to the old value -- but $$k = 0.05 \times 5 = 0.25$$ for Solegria, cutting the prior in half, and allowing an individual set of moderate preferences to be better expressed.

This is exactly the behavior you'd want from a major internal refactor: minimal disruption where things were established, meaningful improvement where they weren't.
Best of all, the original modeling goal -- group preferences that emerge cleanly and continuously out of a uniform baseline -- was better achieved.

# V. Reflections

The research began with user complaints -- compressed distributions and opaque causality -- and every candidate model was evaluated against those experiences.
"Spread" was never an abstract metric; it was a proxy for whether residents felt their preferences actually mattered.
The final model increased spread where it was over-compressed while preserving rank-order stability where preferences had matured -- translating to the user experience the system was always trying to provide: submit a preference, see a legible change, trust the output.

**The winding path was necessary.**

Each intermediate model revealed a dimension of the problem that had been previously overlooked.
The hyperbolic approach revealed that the damping parameter wasn't universal.
The cross-dataset validation revealed sensitivity to preference generation method.
The QV model revealed the tension between coalition-building norms and real-world participation patterns.
The sigmoid revealed that even the best curve couldn't work across all regimes.
The damp-before-normalize investigation revealed that regularization must happen before normalization -- the key conceptual insight.
Each failure narrowed the space of possible solutions, until what remained was simple.

**Every idea was tested against real data.**

The research used two production datasets with different participation structures and preference distributions.
Theoretical elegance was never sufficient; the datasets always had the final word.
This also reveals the importance of persistence -- it took several years to get enough data for this research.

**Separation of concerns clarified everything.**

The original PowerRanker knew about $$\text{numResidents}$$ and $$\text{implicitPref}$$ -- application-layer concepts that don't belong in a generic ranking library.
In the final design, PowerRanker accepts a pseudocount $$k$$ as a constructor option and knows nothing about residents, participation, or houses.
The application layer computes $$k = c \times \text{numResidents}$$ from its domain knowledge and passes it in.
The library became more general while the application remained domain-aware -- and beginning with this separation as a design constraint shaped the research process throughout.

**AI as a research partner accelerated exploration -- but speed has its own risks.**

This research was conducted in collaboration with Claude, which made it possible to move through the problem at a rapid pace.
Formulating hypotheses, writing scripts, running them against data, and interpreting results could happen in a single sitting rather than over days or weeks.
But the speed of the process created its own challenge: it became easy to explore faster than we could think.
The damp-before-normalize breakthrough -- the most important insight of the entire project -- came not from another round of analysis, but from stepping away from the screen and working through matrix algebra with pen and paper.
The AI was indispensable for traversing the search space; the human judgment about when to stop searching and start questioning was equally essential.

**Question inherited assumptions.**

PageRank's normalize-then-damp pipeline was cargo-culted in without questioning whether its order of operations made sense in a different domain.
We spent six iterations optimizing the damping curve before questioning where regularization belonged in the pipeline at all.
Adapting an algorithm means inheriting its structure -- and inherited structure can be the hardest kind to see, precisely because it came with the territory.
The same lesson applied to implicit preferences: a pragmatic hack that worked well enough to obscure its own conceptual problems for years.
