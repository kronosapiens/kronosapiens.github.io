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

# I. Motivation

[There is no perfect voting system.]({% post_url 2020-04-04-gaming-the-vote %})
The truth and tragedy of this statement has been understood by scholars for decades, epitomized by Kenneth Arrow's famous "impossibility theorem" demonstrating the fundamental limits of ranked-choice voting systems.

Fundamentally, the problem stems from attempting to measure complex social reality under conditions of high stakes.
In attempting to distill subjective reality into objective votes, information is inevitably lost; the measurement process itself becomes an arena for power contestation.
The best we can do, ultimately, is to design _task-specific_ voting systems in which the gap between subjective experience and objective input is as small as possible, minimizing the scope of conflict and increasing the utility and legitimacy of these systems.

Several years ago [I predicted]({% post_url 2019-05-08-against-voting %}), at least among the web3 governance community, that challenges with pass-fail voting would shift governance interest away from proposal-based governance and towards distributed capital allocation.
Over the last five years, that prediction has been born out: instead of _voting on policy_, governance innovation has increasingly come to revolve around _giving out money_.
The shift from discrete policy outcomes (you win, I lose) to _continous financial outcomes_ ($10 to you, $5 to me) opens up a rich design space which, critically, sidesteps some of the fundamental limits implied by Arrow's Theorem.

Within the domain of decentralized capital allocation, several classes of techniques have been explored:

- **Quadratic Funding**, in which direct donations double as "votes" dividing a matching pool, subject to square-root constraints.
- **Pairwise Methods**, in which inputs are framed as "A vs B" and converted into numeric allocations via an algorithm.
- **Metrics-Based**, in which votes are made on high-level metrics, and allocations are made indirectly based on these metrics.
- **AI-Augmented**, in which AI agents analyze grantees and recommend allocations.

Each of these approaches, on some level, seeks to convert scarce attention into legitimate signal.
Each has their own strengths and weaknesses:

- **Quadratic Funding** struggles to efficiently allocate attention across projects, creating "beauty contests" and rewarding hype.
- **Pairwise Methods** struggles to get sufficient coverage and voter engagement to produce reliable results.
- **Metrics-Based** struggles with "Goodhart's Law" failures and incentivizes grantees to fabricate data.
- **AI-Augmented** struggles with issues of alignment, legitimacy, and decision quality.

[I have been researching and working with capital-allocation systems since 2016](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3359677), and believe that the best path forward is to continue advancing the theory of _all_ of these techniques, and to develop a culture of practice which is able to select from among them based on the specifics of the problem, and audience, at hand.

The rest of this essay will focus specifically on pairwise preferences and lay out a roadmap of how they might develop over the next few years.
We will argue that pairwise methods should not be understood as isolated mechanisms, but as part of a larger _paradigm_ of decision-making involving various interrelated techniques.
By approaching pairwise methods in this way, it becomes easier to see how the pieces fit together and offer a compelling approach for allocating shared resources.

# II. Why Pairwise

A pairwise preference is simply a choice between two options.
As such, pairwise preferences can be seen as the "atom" of human subjectivity: the simplest possible distinction, running on the "phenomenological bare metal" of human perception.
This simplicity makes them both very robust (they mean what they say they mean), accessible (anybody can make a relative distinction), general (many decisions can be framed in relative terms), and flexible (pairwise preferences can be aggregated in many different ways).
In addition, the self-contained nature of the pairwise decision makes these methods well adapted to environments of scarce attention, as participants are able to provide quality inputs in small amounts of time.

Pairwise preferences have been studied for decades, beginning with the work of psychometrician L. L. Thurstone in 1927 and his research into subjective responses to stimuli.
Pairwise preferences would go on to find many applications in the ranking and ordering of items: from ranking chess players through ELO to weighting web pages through Google's PageRank.
This dual heritage, as both a technique for subjective measurement (["high quality bits"](https://vitalik.eth.limo/general/2025/02/28/aihumans.html)) _and_ for allocating weights among items, suggests that these techniques have much to offer the practice of distributed capital allocation -- which must solve exactly these problems.

Despite these appealing qualities, pairwise methods have remained relatively niche among distributed capital allocators.
Pairwise methods have seen some use, as a part of Optimism's RetroPGF program (helping to allocate $20mm in funding) as well in this year's [Deep Funding](http://deepfunding.org/) initiative.
However, they have yet to capture the same level of enthusiasm as other techniques discussed.

I believe that this is due at least in part to there being several major gaps in pairwise practice, and the lack of an overarching vision.
These gaps, which will be discussed below, make the technique difficult to use and difficult to communicate.
By more clearly articulating pairwise as a _paradigm_ of interrelated techniques and practices, we can build more momentum around the techniques and help push the public goods funding ecosystem forward.

# III. The Pairwise Paradigm

The word "paradigm" comes from the Greek word for _pattern_, and in scientific contexts refers to "[a distinct set of concepts or thought patterns, including theories, research methods, postulates, and standards for what constitute legitimate contributions to a field.](https://en.wikipedia.org/wiki/Paradigm)"
By referring to pairwise as a "paradigm" instead of a single tool or mechanism, we emphasize that it is not any single technique, but rather the _synergies between multiple related techniques_, that produces key outcomes.

In this case, audience selection feeds into a voting UI, which feeds data to multiple algorithms which guide both ongoing data collection and final weight outputs.
Individual techniques can be added, altered, or removed _within_ the pairwise paradigm, allowing for forwards progress within a coherent exploratary space.

![The Pairwise Paradigm](/img/pairwise-flow.png)

## Algorithm Selection

Pairwise preferences by themselves do not determine rankings or weights.
Rather, they must be processed by an algorithm and _converted_ into weights using some process.
The choice of algorithm has major implications for what kind of output gets created.

This section will discuss several algorithmic options and their properties, with a focus on the _ontology_ and _computational complexity_ of each algorithm -- how each algorithm models reality, and how effectively it can processes information relative to that model.

In all cases, we begin with a sequence of pairwise observations $[(a, b, x), ...]$, and want to produce a set of weights $w = [w_a, w_b, ...]$ telling us how to allocate fungible resources among the items.

### Elo

The Elo rating system, developed by Hungarian chess master and physicist Arpad Elo, is most well known as the basis for professional chess rankings, but has found use in determining rankings across a variety of domains.

In the Elo system, every participant has a rating $R$ determined from their prior matchups, which can be used to predict the score of an upcoming match:

$
E[S_{ab}] = \frac{f(R_a)}{f(R_a) + f(R_b)}
$

After a match, the player's Elo ratings are updated as a function of the _actual outcome_ vs the _expected outcome_ against an opponent:

$
R^{'}_a \leftarrow R_a + g(S_{ab} - E[S_{ab}])
$

Compared to the algorithms below, Elo has two unique characteristics.
Unlike the other algorithms, which generate weights using all of the observed preference data, Elo is an _online_ algorithm, meaning that the rankings are updated after every match -- and thus that rankings are determined in part by the ordering of the matches.

**Ontology**, Elo understands entities as _changing over time_, with interactions occurring in a specific sequence and entities adapting in response to encounters.

**Computationally**, Elo is $O(n)$ in the number of matches $n$ -- every matchup results in one constant-time update.

As a result of this, I would say that Elo is a *suboptimal choice* of algorithm for capital allocation, in which we want to take large body of _interchangeable_ votes and convert them into a single set of _a posteriori_ weights.

### Bradley-Terry

The Bradley-Terry model is another popular model for generating weights based on pairwise preferences.
Bradley-Terry models the probability of item $a$ being preferred to item $b$ as follows:

$
P(a > b) = \frac{p_a}{p_a + p_b}
$

Note the similarity to Elo!
However, unlike Elo, Bradley-Terry generates weights based on a _set of preferences,_ making it a better fit for capital allocation in which we want to gather many inputs before making a decision.
In terms of computational complexity, Bradley-Terry models are typically fit using a technique known as Maximum-Likelihood Estimation, in which the underlying probabilities are iteratively updated to maximize their fit to the observed data.

**Ontologically**, Bradley-Terry is deeply Platonic: pairwise observations are understood as flickering shadows revealing a latent, intrinsic truth.

**Computationally**, fitting a Bradley-Terry model is $O(nm)$ in the _number of matchups_ $n$ and _number of iterations_ $m$ needed to converge.
Unlike Elo, all the computation occurs at once.

Bradley-Terry methods are popular in the psychological literature in part due to them lending themselves well to evaluation and simulation.
In a simulation, one knows the underlying weights, and can thus rigorously show the degree to which some process re-creates those weights.

### Spectral Methods

Spectral methods, the most famous of which is Google's PageRank, aggregate pairwise inputs into a "graph" of interactions, and then interprets that graph's principal eigenvector as a _measure of centrality_.

For those new to linear algebra, the eigenvector ("self-vector") of a graph is the vector $v$ such that:

$
Xv = \lambda v
$

We can interpret this as the "direction" to which the _whole graph points_, and can be seen as a type of "center" of the data.

To find this center, we can use a technique in which energy "flows" through of the graph until it reaches a "steady state" where no more energy moves ([see visualization](https://en.wikipedia.org/wiki/PageRank#/media/File:Page_rank_animation.gif)).
These types of techniques are known as "spectral methods" after the "spectrum" of latent values they reveal.
Spectral methods for ranking and scoring have a history dating at least back to [Keener (1993)](https://www2.math.upenn.edu/~kazdan/312S14/Notes/Perron-Frobenius-football-SIAM1993.pdf), but were theoretically underdeveloped relative to Bradley-Terry until the [2015 Rank Centrality paper](https://arxiv.org/pdf/1209.1688) demonstrated both their statistical equivalence and computational advantages.

**Ontologically**, spectral methods take _interactions_ as the only knowable reality; weights are understood as _synthetic information products_.

**Computationally**, spectral methods are $O(k^3 + n)$ in the _number of items_ $k$ and the _number of matchups_ $n$ -- making the this technique shine in the setting where many votes are cast on a small number of items.

Bradley-Terry and Spectral methods answer similar questions and will generally produce similar results for similar data, but there are important differences in how they operate.
Perhaps the most important is that spectral methods integrate _all of the data_ when generating weights, enabling them to infer transitive relationships not explicitly observed.
This propagation of signal creates more complex interactions, making these methods robust against sparse data.

Historically, spectral methods were most commonly used for judging tournaments and competitions, in which the "votes" emerge _endogenously_ from interactions among the items themselves (i.e. two teams competing _with each other_, two websites linking _to each other_)
My colleagues at Colony and I extended these techniques to the domain of social choice with our [2018 Budgeting Box paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3317445), modeling votes as emerging _exogenously_ as the judgments of external voters (a voter votes on two items; the items themselves do not interact).

This work inspired the development of [Pairwise.vote](https://www.pairwise.vote/), which has been used to help guide the distribution of over $20mm through Optimism's RetroPGF and gather jury data in this year's Deep Funding initiative.

### Deep Funding

Both Bradley-Terry and Spectral methods have a major drawback: they are data-hungry.
To produce good results, both models require votes on the order of $O(k^2)$, growing as a square of the number of items $k$.

Deep Funding is a more recent technique proposed by Vitalik Buterin in late 2024, in which pairwise judgments are not used to generate weights directly, but rather to score competing weight _proposals_.
This reframing of the problem -- and of the role of human inputs -- aims to produce competitive results with far less human input.

Under the slogan of "[AI as the engine, humans as the steering wheel](https://vitalik.eth.limo/general/2025/02/28/aihumans.html)," Buterin introduces a model of social choice in which the weight proposals are produced _at scale_ by machines, with a small amount of human "juror" input being used to score proposals.
By leveraging human inputs, the approach promises to produce satisfactory outcomes with less human effort.

**Ontologically**, Deep Funding treats weights as untrusted proposals and treats juror pairwise inputs as samples of reality used to score and select the best proposals.

**Computationally**, Deep Funding is $O(wn)$ in the _number of proposals_ $w$ and the _number of votes_ $n$.

Unlike the Bradley-Terry and Spectral methods, which requires $O(k^2)$ votes, Deep Funding aims to produce similar results with $O(k)$ votes or less, perhaps as few as one vote for every ten items (note that this _does not_ take into account the computational effort needed to propose the proposals themselves)
This reduction in complexity from quadratic to sub-linear means that Deep Funding methods can be applied to problems not computationally tractable for the other techniques.
Deep Funding's central limitation is that it can only produce results as good as the proposals it takes as input.
The $O(k)$ votes are only enough to score existing proposals, not to produce them.

## Pair Selection

As mentioned in the previous section, a challenge of using Bradley-Terry and Spectral methods for weight-finding is that they require a quadratic number of votes for a given number of items.
This is because for any set of $k$ items, there are $k(k-1)/2 = O(k^2)$ possible pairs.
Getting good results means voting not only on every _item_, but on every _pair_, ideally multiple times.
Creating weights for even 50 items might call for 2,000 votes -- a tall order given how many communities _already_ struggle with voter apathy.

Developing techniques for managing this scale will be key to bringing pairwise methods more into the mainstream.

### Star Grouping

One approach, taken by the team at Pairwise, was to introduce a "pre-filter" step in which voters score each project on a scale of 1 - 5 stars.
This scoring process would then "bucket" projects into five tiers, with pairwise votes being made only between projects in the same tier.
This technique reduces the number of votes required to $O(k^2/5)$, a reduction of 80%, by ensuring that the quadratic creation of pairs occurs within smaller sets.

Star grouping can also be adapted to settings where the categorization is not of _quality_, but of _type_.
In cases where the items being considered are not all of the same type, star grouping can help cluster like items together, simplifying downstream voting.

### Active Ranking

Another approach for reducing the number of votes would be through a technique called "active ranking," an extension of the concept of "[dueling bandits](https://www.cs.cornell.edu/people/tj/publications/yue_etal_09a.pdf)."
Active ranking works by surfacing pairs not at random, but based on an assessment of the _uncertainty_ of that pair.
The intuition is that among the entire set of items, some pairwise judgments are more "obvious" than others -- imagine a bear fighting a rabbit.
Active ranking works to direct scarce voter attention to the pairs which provide the most meaningful signal -- in this analogy, to bear vs lion.

Done well, we can imagine needing as few as $k$ votes.
Observe that any weighting of $k$ items can be expressed as a set of $k-1$ scalars, representing the ratio of two adjacent items:

$$
[a = .1, b = .2, c = .3, d = .4] <=> [b = 2a, c = 1.5b, d = 1.33c]
$$

This generalizes to an arbitrary number of weights and tells us that we can _in theory_ recover a set of $k$ weights with only $k-1$ human inputs.
While achieving this limit is not realistic in practice, we can approach it and likely reduce the data requirement to some scalar multiple $c$ of the number of items, i.e. $O(ck)$.

Implementing active ranking is straightforward.
For every pair of items $a, b$ we create a Beta distribution $p_{i,j} \sim Beta(votes[a,b], votes[b,a])$ and choose pairs based on $Var(p_{i,j})$.
This variance will high for pairs with few observations or mixed observations, and low for pairs in which one item is repeatedly preferred.

Calculating these distributions can be done online, with the relevant distribution being updated in constant-time after each vote.
Note that active ranking is an _online_ process -- the order of votes _does matter_ for determining which pairs are more likely to be shown.

Compared to star grouping, active ranking has several advantages.
First, active ranking permits $O(n)$ comparisons in total, while star grouping still requires $O(n^2)$ votes per sub-group.
Second, active ranking can be run passively in the background, while star grouping requires an explicit voting step.
Third, active ranking allows for all projects to be compared, whereas star grouping disallows comparisons between groups.
Overall, active ranking lets the process capture and express _more information_ than would be possible with star grouping.

## UI Development

Another important consideration is _the design of the voting interface_.
A poorly designed interface (as an extreme example, consider the choice of two random strings) will yield data close to random, while a well-designed interface will enable participants to provide quality feedback quickly and effectively.

### Voting Times

[Earlier analysis has shown]({% post_url 2025-08-03-deepfunding-jury-analysis %}) that the "sweet spot" for deciding on a pair is about 30 seconds.
More time does not result in meaningfully better judgments (and reduces the total number of pairs submitted), while less time increases the likelihood of a random choice (and thus measurement error).

Working backwards from this 30-second target, we can purposefully design a UI to provide as much information as can be processed within that time frame.

### UI Elements

The Pairwise team has arguably gone the furthest here, offering this UI for the Deep Funding pilot:

![Pairwise Screenshot](/img/pairwise-ui.png)

Here we see a number of key design elements:

- Each item clearly indicated by name and logo
- A set of curated and domain-specific metrics
- An AI-based textual summary of the project
- The ability to choose either item, or to skip
- The ability to revisit a previous vote

These elements provide the basics for an effective decision-process.
The metrics enable simple and quantitative contrasting between the two items, while the text summary gives the voter more context on the indiviual items.
Letting the voter skip the pair limits the generation of bad data in cases where the voter genuinely cannot differentiate between the items.

This approach lets funding bodies leverage both _metrics_ and _AI judgment_ while still leaving the final decision in the hands of human voters.
The advantage here is that while the metrics and summaries may be the same for every project, each individual voter will _qualitatively_ integrate the information in a slightly different way, yielding richer results than allocating funds based on metrics or AI judgments _directly_.
This makes pairwise methods more robust against the Goodhart's Law-style failures more common among metric and AI-based approaches, in which projects are able to "game the system" by optimizing their self-representation for more narrow decision criteria.

### Input Format

An important question is whether voters should be asked to make _ordinal_ judgments (A vs B) or _cardinal_ judgments (A is 3x better than B).
While the idea of cardinal judgments may seem appealing at first glance -- offering the promise of _more signal_ -- it will in most cases be a distraction.
It is a timeless truth that in _untrained audiences_, measurements of _psychic intensity_ are more likely to be measurements of _individual mood or personality_ than measurements of the quality of the items themselves -- and attempts to collect cardinal judgments will result in more noise than signal.

[An analysis of Deep Funding's juror data]({% post_url 2025-08-03-deepfunding-jury-analysis %}) showed that while the perceived ratio of two projects' impact varied widely, the perceived _valence_ of the impact (whether A or B overall was more important) was remarkably consistent -- between 63% and 89% agreement, depending on the set of items being evaluated.

Ultimately, cardinal measurements _can_ be used, but require voters to receive special training for them to be meaningful.
For a general audience, ordinal measurements should be preferred whenever possible.

## Audience Selection

An important consideration in running a pairwise voting process is audience selection.
Pairwise methods are very well adapted to the setting of _distributed capital allocation by an audience of non-experts_.
It thrives in this setting primarily due to the way that it can direct participant attention efficiently over a wide range of items, without requiring participants to have deep prior knowledge of the items in question.

Pairwise methods are less effective when used by a _small audience of experts_, who are more likely to have _strong prior knowledge_ of the items in question.
For experts who have _already performed_ the cognitive labor of developing specific opinions, and will benefit less from algorithmic support, a pairwise input format creates an unnecessary layer of indirection.
This audience may prefer to express pre-meditated weights directly, rather than have them inferred through a computational discovery process.

Pairwise methods are also likely less effective when being used by a large audience with _no prior domain knowledge_, as they may be unable to make sufficient sense of the information presented.

The ideal audience, then, is a _large group of people with some domain knowledge_, able to form a specific opinion on a newly-presented pair after about 30 seconds of digesting new information.
This group is able to provide the most information, in terms of both _quantity_ and _quality_ of inputs.

It is also important that audience _expectations_ be set appropriately for the pairwise setting.
Unlike settings in which participants decide weights directly, pairwise methods ask participants for relative inputs, and then infers the weights indirectly.
For audiences unfamiliar with this process, "giving up control" of the final weights can be jarring.
To earn participant trust, the process for generating the final weights must be made legible.

## Leveraging Attention

USV's Albert Wenger [recently argued](https://open.spotify.com/episode/6XJOXe3whWTCm3TkuvAWQq?si=e51a8b5f558e43be) that "capital allocation is often downstream from attention allocation."
As society increasingly recognizes that attention is now its scarcest resource, attentional analysis of social choice becomes increasingly important.

### Item Discovery and Strategic Resistance

Compared to voting methods in which items are evaluated individually, pairwise methods more naturally spread attention across items by presenting them in(pseudorandom) pairs.
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

While in theory a vote between two pairs is valid in perpetuity, in practice should be wary of relying too much on stale data.
A practical design seek to leverage all available data, while preferring recent data over older and potentially out-of-date information.
This can be implemented through a decay process in which votes lose their impact over time -- for example, decaying to zero over a two-year period.

### Permissonless Entry

The ideal continuous-funding system would be largely permissionless.
Projects would be able to add themselves to the pool and would over time "reach their level" as incoming votes position the project at the correct weighting.
Under an active ranking process, a new project would be frequently surfaced (with few prior votes giving it a high variance).
A fraudulent project would quickly find itself donwranked to zero, and effectively disappear from the pool.

A potential extension would be to require a stake for submitted projects, slashed in case the project weight falls below some threshold.

### Process Tempo

The funding process can be made truly continuous, in which votes update the weights as soon as they come in, and funding is distributed among the items at a per-second interval.
In practice, a practitioner might want to establish more well-defined tempos to meet the preferences of the community.

One could imagine running "campaigns" to encourage people to vote, where leaderboards and other activations spur a wave of data-collection and keeps the data fresh.
This would be qualitatively similar to a conventional round-based process, but running on a continuous substrate.

One could also imagine making payouts on a monthly or quarterly basis, or even conditioning payouts on milestones determined by a separate governance process.
Again, this would allow for a "product" qualitatively similar to other grant programs, running on a continuous substrate.

### Governance Implications

Continuous funding models have significant governance implications.
By giving the resource management task to the community, you make possible a new style of democracy in which dynamic budgets are used to guide and hold accountable those in power.
Counterintuitively, it also means that less oversight is needed over those in power, as they can be more easily denied resources if they start behaving in self-serving ways.

# IV: Conclusion

## Challenges and Limitations

Pairwise methods have limits.
In settinsg where participants expect a high degree of control over the output, these methods will be frustrating to use.
Pairwise methods also provide no innate sibyl protection, requiring similar solutions to those used by other methods.

There are other challenges specific to pairwise methods that are worth mentioning:

### Independence of Irrelevant Alternatives

The "independence of irrelevant alternatives" (IIA) is a foundational concept on social choice.
The principle of IIA says that the relative ranking of two options must never  depend on a third (the "irrelevant alternative").

Some pairwise algorithms, such as spectral ranking, _intentionally_ draws in that third option to enable richer comparisons with less data.
Violating the IIA principle does not make these algorithms _wrong_, but does require clarifying the advantages and disadvantages of the decision.

Relaxing IIA is acceptable in the setting of capital allocation, where the goal is to distribute resources across an entire ecosystem.
In a single-winner settings like elections, relaxing IIA risks potential loss of legitimacy due to unexpected iteractions among the candidates.

### Dealing with Heterogeneity

One of the few prerequisites to using pairwise techniques is ensuring that the items being compared are meaningfully comparable.
One can meaningfully ask whether someone would prefer an apple are an orange; one cannot meaningfully ask whether freedom is more important than the color red.

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

Things become even better when we think about a continous process.
If we assume that only ~10% of the items undergo meaningful change in a given 3-month period, then we can sustain a continuous funding distribution _indefinitely_ with an ongoing attention cost of _2 minutes per item per year_ ((5 min / 10) * 4).

## Final Thoughts

There is no perfect voting system.
The most we can hope for this life to be able to choose from many tools the one which best fits our circumstances.

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

## Appendix A: Detailed Comparison of Public Goods Funding Techniques

| Dimension | Quadratic Funding | Pairwise Methods | Metrics-Based | AI-Augmented |
| --- | --- | --- | --- | --- |
| Attention efficiency | High-visibility projects soak up attention, leaving long tails thinly reviewed. | Pseudorandom pairings concentrate attention exactly where comparisons are needed. | Depends on curators defining metrics; voters focus on abstractions instead of projects. | Automation triages attention but depends on prompt and model quality. |
| Strategic resistance | Sybil-resistant funding curves blunt collusion but can be gamed with coordinated donations. | Harder to game because preferences are relative and pair selection can be randomized. | Metric gaming is endemic once KPIs become targets. | Vulnerable to prompt attacks, model poisoning, and opaque biases. |
| Data requirements | Needs donation history. | Requires many pairwise ballots; can use active ranking to reduce load. | Requires trusted, frequently refreshed quantitative metrics. | Needs large labeled corpora and governance-ready evaluation datasets. |
| Scalability | Matching pool computation is cheap but human attention scales poorly. | Computationally tractable yet human voting grows near-quadratically without optimizations. | Scales if metrics pipeline is automated; bottlenecks arise in data verification. | Scales compute-wise but oversight cost grows with model sophistication. |
| Goodhart vulnerability | Moderate: quadratic matching discourages lopsided signals but still rewards hype. | Low: binary comparisons make it harder to optimize toward a single metric. | High: once a metric is known it becomes the target. | High: models optimize whatever objective they are given, often misaligned. |
| Voter engagement | Needs broad participation to unlock matching, favoring grassroots campaigns. | Needs fewer voters but they must stay engaged through many comparisons. | Limited voter role; engagement shifts to metric designers and auditors. | Minimal direct voters; trust shifts to jurors who audit AI outputs. |
