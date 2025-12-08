---
layout: post
title: "The Pairwise Paradigm"
comments: true
categories: blog
tags:

- public goods funding
- impact evaluation
- mechanism design
- pairwise preferences

---

# I. Motivations

[There is no perfect voting system.]({% post_url 2020-04-04-gaming-the-vote %})
The truth and tragedy of this statement has been understood by scholars for decades, epitomized by Kenneth Arrow's "impossibility theorem" demonstrating the fundamental limits of ranked-choice voting systems.

Ultimately, the problem stems from attempting to measure complex social reality under conditions of high stakes.
In attempting to distill subjective reality into objective votes, information is inevitably lost; the measurement process itself becomes an arena for power contestation.
In the end, the best we can do is design _task-specific_ voting systems in which the gap between subjective experience and objective input is as small as possible, minimizing the scope of conflict and increasing the utility and legitimacy of these systems.

Several years ago [I speculated that]({% post_url 2019-05-08-against-voting %}), at least among the web3 governance community, the limitations of pass-fail voting would shift interest away from proposal-based decision-making and towards distributed capital allocation.
Over the last five years, that prediction has been born out: instead of _voting on policy_, governance innovation has increasingly come to revolve around _giving out money_.
The shift from _discrete policy outcomes_ (you win, I lose) to _continuous financial outcomes_ ($10 to you, $5 to me) opens up a rich design space of contemporary social choice.

Within the domain of decentralized capital allocation, several classes of techniques have been explored:

- **Quadratic Funding**, in which direct donations double as "votes" dividing a matching pool, subject to square-root constraints.
- **Pairwise Methods**, in which inputs are framed as "A vs B" and converted into numeric allocations via an algorithm.
- **Metrics-Based**, in which votes are made on high-level metrics, and allocations are made indirectly based on these metrics.
- **AI-Augmented**, in which AI agents analyze grantees and recommend allocations.

Each of these approaches, on some level, seeks to convert _scarce attention_ into _useful signal_.
Each has its own strengths and weaknesses:

- **Quadratic Funding** struggles to efficiently allocate attention across projects, creating "beauty contests" and rewarding hype.
- **Pairwise Methods** struggles to get sufficient coverage and voter engagement to produce reliable results.
- **Metrics-Based** struggles with "Goodhart's Law" failures and incentivizes grantees to fabricate data.
- **AI-Augmented** struggles with issues of alignment, legitimacy, and decision quality.

[I have been researching and working with capital-allocation systems since 2016](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3359677), with a focus on pairwise methods, and believe that we should continue exploring _all_ of these techniques, and to develop a culture of practice able to select from among them based on the characteristics of the problem -- and audience -- at hand.

The rest of this essay will focus on **pairwise preferences** and lay out a roadmap of how they might develop over the next few years.
We will argue that pairwise methods should not be understood as isolated mechanisms, but as part of a larger _paradigm_ of decision-making involving various interrelated techniques.
By approaching pairwise methods in this way, it becomes easier to see how the pieces fit together and offer a compelling approach for allocating shared resources.

# II. Why Pairwise

A **pairwise preference** is simply a relative choice between two options: A or B.
Pairwise preferences can be seen as "atoms" of human subjectivity: the simplest possible distinction, running on the "phenomenological bare metal" of human perception.
This simplicity makes them robust (they mean what they say they mean), accessible (anybody can make a relative distinction), general (many decisions can be framed in relative terms), and flexible (pairwise preferences can be aggregated in many different ways).

In addition, the atomic nature of pairwise decisions makes these methods well adapted to environments of scarce attention, as participants are able to provide quality inputs in small amounts of time.

Pairwise preferences have been studied for decades, beginning with the work of [American psychometrician L. L. Thurstone](https://en.wikipedia.org/wiki/Louis_Leon_Thurstone) in 1927 and his research into subjective responses to stimuli.
Pairwise preferences would go on to find many applications in the ranking and ordering of items: from ranking chess players through Elo to weighting web pages through Google's PageRank.
This dual heritage, as both a technique for subjective measurement _and_ for allocating weights among items, suggests that these techniques have much to offer the practice of distributed capital allocation, which solves exactly these problems.

Despite these favorable qualities, pairwise methods have remained niche among distributed capital allocators.
They have seen some use, as a part of Optimism's RetroPGF program (helping to allocate $20mm in funding) as well in this year's [Deep Funding](http://deepfunding.org/) initiative, but have yet to capture the enthusiasm as the other techniques discussed.

I believe that this is due at least in part to there being several key gaps in pairwise practice, and the lack of an overarching vision.
These gaps, which will be discussed below, make the technique difficult to use and difficult to communicate.
By more clearly articulating pairwise as a _paradigm_ of interrelated techniques and practices, we can more clearly communicate the value of these methods, build more momentum around their use, and ultimately help advance the practice of public goods funding.

# III. The Pairwise Paradigm

The word "paradigm" comes from the Greek word for _pattern_, and in scientific contexts refers to "[a distinct set of concepts or thought patterns, including theories, research methods, postulates, and standards for what constitute legitimate contributions to a field.](https://en.wikipedia.org/wiki/Paradigm)"
By referring to pairwise as a "paradigm" instead of a single tool or mechanism, we emphasize that it is not any single technique, but rather the _synergies between multiple related techniques_, that produces desirable outcomes.

These techniques fall into multiple buckets: audience and problem selection, UI design and data collection, and data analysis.
As an end-to-end pipeline, audience selection feeds into a voting UI, which feeds data to algorithms which guide both ongoing data collection and final analysis:

![The Pairwise Paradigm](/img/pairwise-flow.png)

Individual techniques can be added, altered, or removed _within_ this pairwise paradigm, allowing for ongoing concurrent exploration within a coherent design space.
We will now discuss these various topics in turn:

## Algorithm Selection

Pairwise preferences themselves do not determine rankings or weights.
Rather, they must be processed by an algorithm and _converted_ into weights using some process.
The choice of algorithm has major implications for what kind of output gets created, and how it is interpreted.

This section will discuss several algorithmic options and their properties, with a focus on the _ontology_ and _computational complexity_ of each algorithm -- how each algorithm models reality, and how effectively it processes information relative to that model.

In all cases, we begin with a sequence of pairwise observations $[(a, b, obv), ...]$, and want to produce a set of weights $w = [w_a, w_b, ...]$ telling us how to divide a fixed pool of capital among the items.

> Note: Throughout this section, we will use standard mathematical notation to describe properties of these algorithms, specifically the ["Big-O" notation](https://en.wikipedia.org/wiki/Big_O_notation) for describing computational complexity.
> In this notation, will use $k$ to refer to the _number of items or projects being evaluated_ and $n$ to refer to the _number of votes or matchups being observed_.
> Other notation will be introduced as-needed and defined in context.

### Elo

The Elo rating system, developed by [Hungarian chess master and physicist Arpad Elo](https://en.wikipedia.org/wiki/Arpad_Elo), is most well known as the basis for professional chess rankings, but has found use in determining rankings across a variety of domains.

In the Elo system, every participant has a rating $R$ determined from their prior matchups, which can be used to predict the score of an upcoming match:

$
E[S_{ab}] = \frac{f(R_a)}{f(R_a) + f(R_b)}
$

After a match, the player's Elo ratings are updated as a function of the _actual outcome_ vs the _expected outcome_ against an opponent:

$
R^{'}_a \leftarrow R_a + g(S_{ab} - E[S_{ab}])
$

Unlike the other algorithms discussed, which generate weights using _all_ of the observed preference data, Elo is an _online_ algorithm, meaning that the rankings are updated after every match -- and thus that rankings are dependent on the sequence of the matches.
In addition, with Elo, the data are understood as the result of a matchup _between_ two items -- _not_ as a vote on a pair of items by an independent observer.

**Ontology**, Elo models interactions as ocurring _in a specific sequence, between the entities themselves_, with the entities themselves being changed as a result of these encounters.

**Computationally**, Elo is $O(n)$ in the _number of matchups_ $n$ , with every matchup resulting in one constant-time ($O(1)$) update, with no minimum number of observations.

While often proposed as a potential algorithm for capital allocation, Elo ontology of _a sequence of matchups between interacting items_ makes it a *bad fit* for this use-case, in which data takes the form of _a set of votes made by third-party observers_.

### Bradley-Terry

The Bradley-Terry model is a popular model for generating weights based on pairwise preferences.
Bradley-Terry models the probability of item $a$ being preferred to item $b$ as follows:

$
P(a > b) = \frac{p_a}{p_a + p_b}
$

Note the similarity to Elo, which also predicts the result as a ratio of latent scores.
However, unlike Elo, Bradley-Terry generates weights based on a _set of unordered preferences,_ making it a better fit in the setting where we want to gather many inputs before making a decision.
In terms of computational complexity, Bradley-Terry models are typically fit using a statistical technique called Maximum-Likelihood Estimation, in which the underlying probabilities are iteratively updated to improve their fit to the observed data.

**Ontologically**, Bradley-Terry is essentially _Platonic_: pairwise observations are understood as flickering shadows revealing a hidden truth.

**Computationally**, fitting a Bradley-Terry model is $O(nm)$ in the _number of matchups_ $n$ and _number of iterations_ $m$ needed to converge, requiring observations $O(k^2)$ in the number of items $k$.
Unlike Elo, all the computation occurs at once.

Bradley-Terry methods are popular in the psychological literature, as they lend themselves well to evaluation and simulation -- one can begin with fictional "ground truth" weights, run a simulated voting process, and then evalute how well the recovered weights align with the initial ground truth.

### Spectral Methods

Spectral methods, the most famous of which is Google's PageRank, aggregate pairwise inputs into a "graph" of interactions, and then takes the weights from the graph's _principal eigenvector_.

In linear algebra, the _eigenvector_ ("self-vector") of a graph or matrix is the vector $v$ such that:

$
Xv = \lambda v
$

We can interpret this as the "direction" to which the _whole graph points_, and can be seen as a type of summary or "center" of the data.

To find this center, we can imagine having energy "flow" through of the connections of the graph, until it reaches a "steady state" in which the energy stops moveing ([see visualization](https://en.wikipedia.org/wiki/PageRank#/media/File:Page_rank_animation.gif)).
Techniques for decomposing a graph into these components are known as "spectral methods" after the "spectrum" of latent values they reveal (as when white light is divided into components of the color).
Spectral methods for ranking and scoring have a history dating at least back to [Keener (1993)](https://www2.math.upenn.edu/~kazdan/312S14/Notes/Perron-Frobenius-football-SIAM1993.pdf), but were theoretically underdeveloped relative to Bradley-Terry until the [2015 Rank Centrality paper](https://arxiv.org/pdf/1209.1688) demonstrated both their statistical equivalence and computational advantages.

**Ontologically**, spectral methods invert the Bradley-Terry model by taking _interactions_ as the only knowable reality; weights are understood as _summary statistics_, not latent truth.

**Computationally**, spectral methods are $O(k^3 + n)$ in the _number of items_ $k$ and the _number of matchups_ $n$, requiring $O(k^2)$ observations.
That the computation grows with the number of items, not with the number of votes, makes this technique shine in settings where many votes are cast on a small number of items, i.e. $k << n$.

Ultiamtely, Bradley-Terry and spectral methods are more similar than they are different: they answer similar questions and produce similar results on similar data -- but there are subtle differences in how they operate.
Perhaps the most important is that spectral methods model relationships _globally_, enabling them to infer transitive relationships not explicitly observed -- if A beats B, and B beats C, then the spectral method can infer that A would likely beat C.
This propagation of signal creates more complex interactions, but also allows these methods to produce better results with less data.
Spectral methods are also robust against cycles and other intransitive relationships, for which they produce ties, not contradictions.
For these reasons, we believe spectral methods are the _best choice_ for capital allocation, where we care about modelling relationships across an entire ecosystem.

Historically, spectral methods were most commonly used for judging tournaments and competitions, in which the "votes" emerge _endogenously_ from interactions among the items themselves (i.e. two teams competing _with each other_, two websites linking _to each other_).
In 2018, my colleagues at Colony and I [extended these techniques to the domain of social choice](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3317445), modeling votes as emerging _exogenously_ as the judgments of external voters (a voter votes on two items; the items themselves do not interact).

This work would inspire the development of [Pairwise.vote](https://www.pairwise.vote/), helping guide the distribution of over $20mm through Optimism's RetroPGF as well as gather jury data in this year's Deep Funding initiative.

### Deep Funding

Both Bradley-Terry and spectral methods have a major drawback: they are data-hungry, requiring votes on the order of $O(k^2)$, the square of the number of items $k$.
This heavy data requirements makes pairwise methods difficult to use in practice, as it complicates data-gathering.

Deep Funding is a more recent technique proposed by Vitalik Buterin in late 2024, in which pairwise judgments are not used to generate weights directly, but rather to score competing weight _proposals_, which are produced externally.
Under the slogan of "[AI as the engine, humans as the steering wheel](https://vitalik.eth.limo/general/2025/02/28/aihumans.html)," Buterin introduces a model of social choice in which the weight proposals are produced _at scale_ by machines, with a small amount of human input being used to score proposals.
This reframing of the problem -- and of the role of human inputs -- aims to produce better results with less human input.

**Ontologically**, Deep Funding treats weights as _untrusted proposals_ and treats juror inputs as _samples of reality_ used to score and select the best proposals.

**Computationally**, Deep Funding is $O(nw)$ in the _number of votes_ $n$ and the _number of proposals_ $w$, requiring data on the order of $O(k)$.

Unlike the $O(k^2)$ vote requirement of the other methods, Deep Funding aims to produce results with on the order of one vote for every ten items, i.e. $O(k)/10$.
Note that this lower data requirement _does not_ take into account the computation needed to create the weight proposals themselves.
This reduction in complexity from quadratic to sub-linear means that Deep Funding methods can be applied to problems for which it is not feasible to gather large numbers of votes.

On the other hand, Deep Funding's central limitation is that the $O(k)$ votes are only enough to score proposals, not to produce them.
As a result, the method can only produce results as good as the proposals it receives as input, introducing a new vector of complexity and potential disruption.

## Pair Selection

As mentioned earlier, a challenge of using Bradley-Terry and spectral methods for weight-finding is that they require a quadratic number of votes for a given number of items -- $k$ items produce $k(k-1)/2$ pairs.
As a result of this explosion of interactions, producing weights for even 50 items might call for 2,000 votes -- a large ask given how many communities struggle with voter apathy.

Developing techniques for managing this scale will be key to bringing pairwise methods into the mainstream.
Fortunately, two practical approaches already exist: star grouping, and active ranking.

### Star Grouping

This approach, taken by the team at Pairwise, introduces a "pre-filtering" step in which voters score each project on a scale of 1 to 5 stars.
This scoring process "buckets" projects into one of five tiers, with pairwise contests being held only among projects of the same tier.
The result is that the number of votes required shrinks to $O(k^2)/5$ -- an 80% reduction -- by ensuring that the quadratic creation of pairs occurs in smaller sets.

Star grouping can also be adapted to settings where the categorization is not of _quality_, but of _type_.
In cases where the items being considered are not all of the same type, star grouping can help cluster like items together, simplifying downstream voting.

### Active Ranking

Another approach for reducing the number of votes would is through a technique called "active ranking," an extension of the machine learning concept of "[dueling bandits](https://www.cs.cornell.edu/people/tj/publications/yue_etal_09a.pdf)."
Active ranking works by surfacing pairs not at random, but based on the _uncertainty_ of that pair.
The intuition is that among the entire set of items, some pairwise judgments are more "obvious" than others, and so don't need to be voted on -- bear vs rabbit.
Active ranking direct valuable voter attention to the pairs which are the most ambiguous, and thus provide the most information -- bear vs lion.

Done well, we can imagine needing as few as $O(k)$ votes -- a different complexity class entirely compared to $O(k^2)$.

To understand why this is possible, observe that any weighting of $k$ items can be expressed as a set of $k-1$ scalars, representing the pairwise _ratio_ of two adjacent items:

$$
[a = .1, b = .2, c = .3, d = .4] <=> [b = 2a, c = 1.5b, d = 1.33c]
$$

This generalizes to an arbitrary number of weights and tells us that we can _in theory_ construct $k$ weights with only $k-1$ human inputs.
While this limit is not achievable in practice, we can attempt to approach it, reducing the data requirement to some multiple of the number of items, i.e. $10*O(k)$, by directing attention towards the subset pairs which are most competitive with each other.

Implementing active ranking is surprisingly straightforward.
For every pair of items $a, b$ we create a Beta distribution $p_{i,j} \sim Beta(votes[a,b], votes[b,a])$, and then sample pairs based on $Var(p_{i,j})$.
This variance will be high for pairs with few observations or mixed observations, and low for pairs in which one item is repeatedly preferred.

Calculating these distributions can be done iteratively, with the relevant distribution being updated in constant-time after each vote.

> Note that active ranking is an _online_ process -- the order of votes _does matter_ for determining which pairs are more likely to be shown.

Compared to star grouping, active ranking has several advantages.
First, active ranking permits $O(n)$ comparisons in total, while star grouping requires $O(n^2)$ votes per sub-group.
Second, active ranking can be run passively, while star grouping requires an explicit voting step.
Third, active ranking allows for all projects to be compared, whereas star grouping precludes comparison between groups.
Overall, active ranking lets the process capture and express _more information_ than does star grouping.

## UI Development

Another key consideration is _the design of the voting interface_.
A data analysis pipeline is only as good as the quality of the data is analyzes.
And more so than with other methods, the UI of a pairwise process has major implications for the quality of the data being collected.

To illustrate this, imagine a hypothetical "bad" interface -- one which only shows the name of the items being compared, and no other information.
In this case, participants will decide based purely on their per-existing associations with that item, resulting in noisy and unreliable data.
In an even more extreme example, imagine a user deciding between two random strings -- a process which produces _only_ noise.
As we see, there is nothing _inherently_ robust about pairwise data-gathering -- data quality is downstream of the interface.

### Voting and Session Times

Before getting into the specifics of UI design, we should ask ourselves a more basic question: _how long_ do we expect voters to spend evaluating a given pair?
With a target time in mind, we will be able to make better decisions about visual design.

In casual conversation, practitioners have proposed target times of as little as 5 seconds to as long as 5 minutes.
[Analysis of deep funding voting data]({% post_url 2025-08-03-deepfunding-jury-analysis %}) suggests that the "sweet spot" is about 30 seconds.
More time does not result in meaningfully better judgments, and reduces the total number of pairs submitted
Less time, however, increases the likelihood of a random choice, and thus of measurement error.

Working backwards from this 30-second target, we can design a UI to provide as much information as can be processed in that time frame.

We can also extrapolate out from individual votes to the concept of a voting "session."
If we see voting on a single pair as the "atom" of a pairwise decision process, a 30-second decision time lets us talk about 5-minute voting sessions, in which participants are able to submit 10 votes.
This five-minute session becomes the basic unit of engagement -- short enough to be completed on the train or over coffee, and data-rich enough to move the process forward.

### UI Elements

When it comes to visual design, the Pairwise team has arguably gone the furthest.
Consider the UI they developed for the Deep Funding pilot:

![Pairwise Screenshot](/img/pairwise-ui.png)

Here we see a number of key design elements:

- Each item clearly indicated by name and logo
- A set of curated and domain-specific metrics
- An AI-based textual summary of the project
- The ability to choose either item, or to skip
- The ability to revisit a previous vote

These elements form the foundation of an effective decision process.
The metrics enable immediate, quantitative contrast between thewo items, while the text summary gives the voter deeper context on individual items.
Letting the voter skip pairs reduces the incidence of bad data, in cases where a voter genuinely cannot differentiate between two items.

Further, this approach lets funding bodies incorporate both _metrics_ and _AI judgment_ in their process, leaving the final decision in the hands of human voters.
The advantage here is that while the metrics and summaries may be the same for every project, each individual voter _qualitatively_ integrates the information differently, yielding richer results would be possible by allocating funds by metric or AI judgment _directly_.
This makes pairwise methods more robust to [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law)-style failures common among metric and AI-based approaches, in which projects learn to "game the system" by optimizing their self-representation towards more narrow and mechanical decision criteria.

### Input Format

Another important question is whether voters are asked to make _ordinal_ judgments (A is better than B) or _cardinal_ judgments (A is 3x better than B).
While cardinal judgments may seem appealing at first glance -- offering the promise of _more signal_ -- in often turns out to be a distraction.
It is frequently the case that in _untrained audiences_, measurements of _psychic intensity_ are more likely to be measurements of _individual mood or personality_ than measurements of the _quality of the items themselves_ -- and so cardinal judgments will contain more noise than signal.

[An analysis of Deep Funding's juror data]({% post_url 2025-08-03-deepfunding-jury-analysis %}) showed that while the perceived ratio of two projects' impact varied widely, the perceived _valence_ of the impact (whether A or B overall was more important) was remarkably consistent -- between 63% and 89% agreement, depending on the set of items being evaluated.
This implies that while voters struggled to provide consistent evaluations of the relative impact of pairs of projects, they could consistently determine which of two projects was more impactful _overall_.

It is, of course, not so simple, and the question of cardinality vs ordinality continues to be explored by the academic community.
[One recent paper](https://arxiv.org/pdf/2504.14716) on LLM evaluation found that models which presented results alongside "distractions" like excess enthusiasm were more likely to be chosen in ordinal (pairwise) matchups, while both neutral and distracted responses received similar cardinal (numeric) scores, suggesting that in some cases, cardinal methods can be gamed in ways ordinal methods cannot.
[Another recent study](https://pmc.ncbi.nlm.nih.gov/articles/PMC9586273/pdf/pnas.202210412.pdf) found that over long periods of time, cardinal measures of personal wellbeing were correlated with objective outcomes (such as moving to a new neighborhood if unhappy where you live), suggesting that cardinal judgments are not always noisy or idiosyncratic.

The question of cardinal vs ordinal judgments is far from settled, and much depends on the specifics of the problem and the audience.
However, it does seems that in the setting of decentralized capital allocation by a large and heterogenous group of voters, that cardinal judgments should be -- at the very least -- the default.

## Audience Selection

An important consideration in running a pairwise voting process is audience selection.
Pairwise methods are very well adapted to the setting of _distributed capital allocation by a heterogenous audience_.
It thrives here primarily due to the way that it can direct participant attention efficiently over a wide range of items, without requiring participants to have deep prior knowledge of the items in question.

In contrast, pairwise methods are less effective when used by a _small audience of experts_, who are more likely to have _strong prior knowledge_ of the items in question.
To give a concrete example, during the Deep Funding pilot a senior Ethereum community member criticized the process, on the grounds that they had already formed clear opinions about the correct weights for individual projects, and felt that the pairwise process was impeding their ability to provide those weights directly.
In this example, we see how for participants who have _already performed_ the cognitive labor of developing opinions, a pairwise input format creates an unnecessary layer of indirection.

It is also possible to have an audience which lacks a minimum baseline of context, such that even with an efficient UI they are unable to make meaningful distinctions between items.

The ideal audience, then, is a _large and diverse group of people with at least some domain knowledge_, able to make a distinction on a never-before-seen pair after about 30 seconds of absorbing new information.
This group will be able to provide the most information, in terms of both _quantity_ and _quality_ of inputs.

Relatedly, it is important that participant _expectations_ be set appropriately.
Pairwise methods don't ask participants for weights directly, but infer them _indirectly_ using an algorithmic process.
For audiences unfamiliar with this process, "giving up control" of the final weights can be jarring, especially to an unfamiliar new algorithm.
Communicating the behavior of the system, and making the end-to-end process legible for participants, will be important to earning widespread acceptance of these methods.

## Item Discovery and Strategic Resistance

USV's Albert Wenger [recently argued](https://open.spotify.com/episode/6XJOXe3whWTCm3TkuvAWQq?si=e51a8b5f558e43be) that "capital allocation is often downstream from attention allocation."
As society increasingly recognizes that attention is now its scarcest resource, attentional analysis of social choice becomes increasingly important.

Compared to voting methods in which items are evaluated individually, pairwise methods more naturally spread attention across items by presenting them in (pseudorandom) pairs.
This pairwise approach builds in item discovery as a first-class construct, as even voters with strong preferences for individual projects will be asked to evaluate items for which they are unfamiliar.
By spreading voter attention more uniformly, it becomes more difficult to vote strategically and more difficult for projects to gain advantage through hype or marketing.
For this reason, pairwise methods are more robust than QF-style approaches, which often reduce to "beauty contests" among projects better able to build hype and draw limited voter attention.

## Continuous Funding

To-date, most public goods funding takes place via "rounds."
Every round is a distinct event, featuring a slightly different set of projects and, crucially, requiring an entirely new set of votes.
This reproduction of voter labor in every round is highly inefficient, as most voters will maintain similar opinions from round to round.
Unfortunately, porting vote information between rounds is theoretically challenging, as individual judgments are implicitly a function of the entire item set.
If we assume roughly that 90% of voter preferences are the same between rounds, then the epoch-based approach is converting attention to information at a rate of only 10%.

In contrast, pairwise methods naturally lend themselves to _continuous processes_ in which an always-on voting interface can be used to continuously monitor and update ongoing funding flows in response to new information -- converting attention to information at 100% efficiency.
Rather than replicate work in every round, individual preferences can be continuously aggregated into a single "source of truth" trivially capable of incorporating new items or removing those no longer relevant.

Taken together, we can imagine a single always-on funding process, continuously allocating funding in response to new information, with a minimum of operational overhead or wasted attention.

Continuous funding systems introduce new considerations.
We'll discuss a few of them here:

### Stale Data

While in theory a vote between two pairs is valid in perpetuity, in practice we should be wary of relying too much on stale data.
A practical design seek to leverage all available data, while preferring recent data over older and potentially out-of-date information.
This can be implemented through a decay process in which votes lose their impact over time -- for example, decaying to zero over a two-year period.

### Permissionless Entry

The ideal continuous-funding system would be largely permissionless.
Projects would be able to add themselves to the pool and would over time "reach their level" as incoming votes position the project at the correct weighting.
Under an active ranking process, a new project would be frequently surfaced (with few prior votes giving it a high variance).
A fraudulent project would quickly find itself downranked to zero, and effectively disappear from the pool.

A potential extension would be to require a stake for submitted projects, slashed in case the project weight falls below some threshold.

### Process Tempo

The funding process can be made truly continuous, in which votes update the weights as soon as they come in, and funding is distributed among the items at a per-second interval.
In practice, a practitioner might want to establish more well-defined tempos to meet the preferences of the community.

One could imagine running "campaigns" to encourage people to vote, where leaderboards and other activations spur a wave of data-collection and keeps the data fresh.
This would be qualitatively similar to a conventional round-based process, but running on a continuous substrate.

One could also imagine making payouts on a monthly or quarterly basis, or even conditioning payouts on milestones determined by a separate governance process.
Again, this would allow for a "product" qualitatively similar to other grant programs, running on a continuous substrate.

# IV: Conclusion

## Challenges and Limitations

Pairwise methods have limits.
In settings where participants expect a high degree of control over the output, these methods will be frustrating to use.

Pairwise methods also provide no innate sybil protection, requiring similar solutions to those used by other methods.
<!-- TODO: Expand sybil discussion. This is too dismissive of an important issue. What solutions work? (identity verification, staking, reputation systems?) Are there unique considerations for pairwise vs other methods? Does the pairwise structure make sybil attacks easier or harder? -->

There are other challenges specific to pairwise methods that are worth mentioning:

### Independence of Irrelevant Alternatives

The "independence of irrelevant alternatives" (IIA) is a foundational concept in social choice.
The principle of IIA says that the relative ranking of two options must never depend on a third (the "irrelevant alternative").

Some pairwise algorithms, such as spectral ranking, _intentionally_ draw in that third option to enable richer comparisons with less data.
This produces results which reflect a more global perspective, incorporating more data, but also increases the likelihood of unexpected interactions.
Violating the IIA principle does not make these algorithms _wrong_, but does require clarifying the advantages and disadvantages of the decision.

Relaxing IIA is acceptable in the setting of capital allocation, where the goal is to distribute resources across an entire ecosystem.
In single-winner settings like elections, relaxing IIA risks potential loss of legitimacy due to unexpected interactions among the candidates.
For these higher stakes, one-off settings, a Condorcet methods with strong guarantees is likely preferrable.

NOTE: IIA in votes vs in results. With QF, items are not independnet. With pairs, they are.

### Intransitivity

Closely related to IIA is the idea of _intransitivity_ of preferences.


### Dealing with Heterogeneity

One of the few prerequisites to using pairwise techniques is ensuring that the items being compared are meaningfully comparable.
One can meaningfully ask whether someone would prefer an apple or an orange; one cannot meaningfully ask whether freedom is more important than the color red.

Part of the practitioner's skill of problem selection is ensuring that the items being considered are part of a meaningful set.
This meaning can come from both grouping like items together, or by framing the comparison in a way which makes sense for the given set.

Techniques like star grouping can be used to help subdivide a heterogenous set, shifting some of the labor from those deploying the process to those participating in it.

## Putting it Together

As mentioned in the introduction, pairwise should be understood not as a single technique or mechanism, but as a complete _paradigm_ of social choice.
This is because pairwise methods go beyond a single technique, but rather encompass a suite of mechanisms, interfaces, and practices which work together to generate pro-social outcomes.

Having introduced the pieces of this paradigm, we can begin to put them all together to produce estimates of the attentional requirements for public goods funding
Assuming _30 seconds per vote_ and _10 votes per item_, pairwise methods can produce an allocation over a set of items at a fixed cost of _5 minutes_ per item.
For 600 items, this means _50 total hours_ of voter attention.
If we assume each voter commits 20 minutes to the process, then we need only 150 voters to produce a good result -- a fairly easy lift.

Things become even better when we think about a continuous process.
If we assume that only ~10% of the items undergo meaningful change in a given 3-month period, then we can sustain a continuous funding distribution _indefinitely_ with an ongoing attention cost of _2 minutes per item per year_ ((5 min / 10) * 4).

## Final Thoughts

There is no perfect voting system.
The most we can hope for in this life is to be able to choose from many tools the one which best fits our circumstances.

Arrow's theorem showed specifically the limits of ranked-choice systems for producing discrete, ordered results.
Shifting to the capital-allocation setting of _continuous outcomes_ opens up significant space for algorithmic exploration -- in which the complex perturbations of weights is not a bug, but a feature.

We have tried to show that pairwise methods, seen not as one-off techniques but as the foundation of a _paradigm_ for social choice, offers a compelling toolkit for solving one of the most challenging, and urgent, problems of our day.

Many of the basic tools already exist.
[Pairwise.vote](https://www.pairwise.vote/) offers a full-featured client for running pairwise voting processes.
As an open-source project, it would be straightforward to extend it with support for techniques like active ranking.

There is a growing record of practice, but it is still emerging.
More organizations should experiment with pairwise methods for resource allocation -- from awarding prizes to hackathon winners, to supporting critical infrastructure, to guiding corporate budgets.
If you believe your organization would benefit from a more robust process for allocating resources, reach out.

Relative to other techniques and to their underlying potential, pairwise methods remain underexplored.
By articulating this "pairwise paradigm" we hope to reveal a little bit more of the road ahead.

## Appendix: Comparison of Public Goods Funding Approaches

The table below compares four major approaches to public goods funding across key dimensions.
Pairwise methods show particular strength in strategic resistance, attention distribution, and Goodhart vulnerability, while requiring moderate voter engagement and computational resources.

<!-- TODO: Consider highlighting cells where pairwise methods have clear advantages, or adding a summary row at the bottom. -->

| Dimension | Quadratic Funding | Pairwise Methods | Metrics-Based | AI-Augmented |
| --- | --- | --- | --- | --- |
| Attention efficiency | High-visibility projects soak up attention, leaving long tails thinly reviewed. | Pseudorandom pairings concentrate attention exactly where comparisons are needed. | Depends on curators defining metrics; voters focus on abstractions instead of projects. | Automation triages attention but depends on prompt and model quality. |
| Strategic resistance | Sybil-resistant funding curves blunt collusion but can be gamed with coordinated donations. | Harder to game because preferences are relative and pair selection can be randomized. | Metric gaming is endemic once KPIs become targets. | Vulnerable to prompt attacks, model poisoning, and opaque biases. |
| Data requirements | Needs donation history. | Requires many pairwise ballots; can use active ranking to reduce load. | Requires trusted, frequently refreshed quantitative metrics. | Needs large labeled corpora and governance-ready evaluation datasets. |
| Scalability | Matching pool computation is cheap but human attention scales poorly. | Computationally tractable yet human voting grows near-quadratically without optimizations. | Scales if metrics pipeline is automated; bottlenecks arise in data verification. | Scales compute-wise but oversight cost grows with model sophistication. |
| Goodhart vulnerability | Moderate: quadratic matching discourages lopsided signals but still rewards hype. | Low: binary comparisons make it harder to optimize toward a single metric. | High: once a metric is known it becomes the target. | High: models optimize whatever objective they are given, often misaligned. |
| Voter engagement | Needs broad participation to unlock matching, favoring grassroots campaigns. | Needs fewer voters but they must stay engaged through many comparisons. | Limited voter role; engagement shifts to metric designers and auditors. | Minimal direct voters; trust shifts to jurors who audit AI outputs. |
