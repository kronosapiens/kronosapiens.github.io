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

DRAFT

_Abstract: Pairwise methods are best thought of as a paradigm for turning scarce attention into robust allocation signals. With the right algorithms, UI, and audience, they can support continuous funding of ecosystems at surprisingly low attention cost._

Thanks to Carl Cervone and David Gasquez for feedback on earlier versions of this essay.

# I. Motivations

[There is no perfect voting system.]({% post_url 2020-04-04-gaming-the-vote %})
The truth and tragedy of this statement has been understood for decades, beginning with Kenneth Arrow's "impossibility theorem" showing the fundamental limits of ranked-choice voting systems.

Ultimately, the problem stems from attempting to measure complex social reality under conditions of high stakes.
In attempting to distill _subjective_ reality into _objective_ votes, information is lost, and the measurement process itself becomes an arena for power contestation.
In the end, the best we can do is design _task-specific_ systems in which the gap between subjective experience and objective input is as small as possible, decreasing the scope of conflict and increasing both the utility, and legitimacy, of these systems.

Several years ago [I speculated that]({% post_url 2019-05-08-against-voting %}), at least within the web3 governance community, the limitations of pass-fail voting would shift interest away from proposal-based decision-making and towards distributed capital allocation.
Over the last five years, that prediction has been borne out: instead of _voting on policy_, governance innovation has increasingly come to revolve around _giving out money_.
The shift from _discrete policy outcomes_ (you win, I lose) to _continuous financial outcomes_ ($10 to you, $5 to me) opens up a rich design space for contemporary social choice.

Within the domain of decentralized capital allocation, several classes of techniques have been explored:

- **Quadratic Funding**, in which direct donations double as "votes" dividing a matching pool, subject to square-root constraints.
- **Pairwise Methods**, in which inputs are framed as "A vs B" and converted into numeric allocations via an algorithm.
- **Metrics-Based**, in which votes are made on high-level metrics, and allocations are made indirectly based on these metrics.
- **AI-Augmented**, in which AI agents analyze projects and recommend allocations based on various internal processes.

Each of these approaches, on some level, seeks to convert _scarce attention_ into _useful signal_.
Each has its own strengths and weaknesses:

- **Quadratic Funding** struggles to efficiently allocate attention, creating "beauty contests" and rewarding hype.
- **Pairwise Methods** struggles to get sufficient coverage to produce reliable results.
- **Metrics-Based** struggles with "Goodhart's Law" failures and incentivizes misrepresentation.
- **AI-Augmented** struggles with issues of alignment, legitimacy, and interpretability.

[I have been researching and working with decision-making systems since 2016](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3359677), with a focus on pairwise methods.
I believe that we should continue exploring _all_ of these techniques, and develop a culture of practice able to select from among them based on the characteristics of the problem, and audience, at hand.

The rest of this essay will discuss **pairwise preferences** specifically, and describe the _design space_ in which they operate.
We will argue that pairwise methods should not be understood as isolated mechanisms, but as part of a larger _paradigm of decision-making_ incorporating multiple interacting techniques.
By approaching pairwise methods as a _paradigm_, it becomes easier to see how the various elements combine into a higher-performance system for allocating shared resources.

This essay will focus on the use-case of "public goods funding," in which communities come together to fund critical infrastructure, as this is the domain with the most activity and richest basis for analysis.
The scope of these methods, however, is broader.
Instead of funding public goods, we could apply these methods to problems as grand as the setting of federal budgets, or as mundane as judging hackathons or [prioritizing chores in a coliving house](https://www.zaratan.world/chorewheel).
Given the range of possible applications, getting pairwise right would be a major unlock in our ability to coordinate at scale.

## Why Pairwise

A **pairwise preference** is a relative choice between two options, A or B.
Pairwise preferences are the atoms of human subjectivity: the simplest distinction a person can make, running on the "phenomenological bare metal" of perception.
This simplicity makes them robust (they mean what they say they mean), accessible (anybody can make a relative distinction), general (many decisions can be framed in relative terms), and flexible (pairwise preferences can be aggregated in many different ways).

**Pairwise and Attention**

USV's Albert Wenger [recently argued](https://open.spotify.com/episode/6XJOXe3whWTCm3TkuvAWQq?si=e51a8b5f558e43be) that "capital allocation is often downstream from attention allocation."
As society increasingly comes to view attention as its scarcest resource, evaluating social choice schemes through the lens of attention becomes increasingly critical.
When compared to other voting systems, pairwise methods are arguably more "attention-native" -- stimulating, game-like, and inherently rewarding to engage with.
This dynamic alone makes pairwise preferences particularly well-suited our historical moment.

In contrast, a common critique of non-attention-native methods like Quadratic Funding is that they lead to "beauty contests" -- projects with marketing muscle attract most of the funding, at the expense of valuable, but more subtle, alternatives.

Pairwise methods, on the other hand, more naturally _distribute attention_ by presenting items in random pairs.
This approach elevates _item discovery_ into a first-class construct, as voters are frequently exposed to items with which they are unfamiliar.
This reduces the need (and benefit) for projects to market themselves, freeing resources for driving engagement with _the system as a whole_.

Further, distributing voter attention makes strategic voting more costly.
Unlike, for instance, a Borda Count, in which one can trivially "bury" a rival, voter evaluations will involve pairs of items in which they have no strategic interest.

Seen through this lens, pairwise methods appear as a natural basis for social choice in an environment of scarce attention.
Rather than take voting methods designed for ink and parchment and try to adapt them to fast-paced, interactive decision environments, we can take decision primitives _designed for attention_ and use them as the basis for entirely new regime.

**Pairwise History**

Pairwise preferences have been studied for decades, beginning with the work of [American psychometrician L. L. Thurstone](https://en.wikipedia.org/wiki/Louis_Leon_Thurstone) in 1927 and his research into subjective responses to stimuli.
Pairwise preferences would find many applications in the ranking and ordering of items: from ranking chess players with Elo, to weighting web pages with Google's PageRank, to allocating credit for open-source contributions with [SourceCred](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4570035).

This dual heritage, as a technique for subjective measurement _and_ allocating weights among items, suggests these techniques have much to offer to the practice of distributed capital allocation, which faces exactly these problems.

Despite these attractive qualities, pairwise methods have remained niche in practice.
They have seen some use in public goods funding, such as in [Optimism's RetroPGF](https://www.optimism.io/blog/announcing-retropgf-round-3-recipients) (helping to allocate $100mm in funding) as well in this year's [Deep Funding](http://deepfunding.org/) initiative, but have yet to capture the enthusiasm of the other techniques discussed.

This is in part due to gaps in pairwise practice, and the lack of an overarching vision.
These gaps, explored below, make the technique difficult to use and to communicate.
By more clearly articulating pairwise as a _paradigm_ of interrelated techniques, we can more clearly communicate the scope of these methods, build momentum around their use, and ultimately advance the art and practice of public goods funding overall.

# II. The Pairwise Paradigm

The word "paradigm" comes from the Greek word for "pattern," and in scientific contexts refers to "[a distinct set of concepts or thought patterns, including theories, research methods, postulates, and standards for what constitute legitimate contributions to a field](https://en.wikipedia.org/wiki/Paradigm)."
By framing pairwise as a "paradigm" instead of a single tool or mechanism, we emphasize that it is not any one technique, but rather the _synergies between multiple related techniques_, that produces desirable outcomes.

These techniques fall into multiple buckets: audience and problem selection, interface design and data collection, and algorithmic data analysis.
As an end-to-end pipeline, audience selection feeds into a voting interface, which feeds data to algorithms which guide both ongoing data collection and final analysis:

![The Pairwise Paradigm](/img/pairwise-flow.png)

Individual techniques can be added, altered, or removed _within_ this pairwise paradigm, allowing for parallel explorations within a coherent design space.

We will now explore these topics, from back to front.

## 1. Algorithm Selection

> Note: this section is more technically dense than the rest of the essay.
> Feel free to skim if the details are not relevant to you.

Pairwise preferences themselves do not determine rankings or weights.
Rather, they must be _converted_ into weights using an algorithmic process, a type of "machine for converting subjectivity into objectivity."
The choice of algorithm has far-reaching implications for what kind of output gets created, and how it should be interpreted.

This section will discuss several options and their properties, with a focus on the _ontology_ and  _complexity_ of each algorithm -- how each algorithm models reality, and how effectively it processes information relative to that model.

In all cases, we begin with a sequence of pairwise observations $[(a, b, x), ...]$ with $x$ presenting the pairwise vote, and want to produce a set of weights $w = [w_a, w_b, ...]$ telling us how to divide a fixed pool of capital among the items.

> Note: Throughout this section, we will use the standard ["Big-O" notation](https://en.wikipedia.org/wiki/Big_O_notation) for comparing the complexity, in terms of both computation and data, of these algorithms.

### Elo

The Elo rating system, developed by [Hungarian chess master Arpad Elo](https://en.wikipedia.org/wiki/Arpad_Elo), is most well known as the basis for professional chess rankings, but has found use in determining rankings across a variety of domains.

In the Elo system, every participant has a rating $R$ determined by their prior matchups, used to predict the score of an upcoming match:

$
E[S_{ab}] = \frac{f(R_a)}{f(R_a) + f(R_b)}
$

After a match, the player's Elo ratings are updated as a function of the _actual outcome_ vs the _predicted outcome_ against an opponent:

$
R^{'}_a \leftarrow R_a + g(S_{ab} - E[S_{ab}])
$

**Ontologically**, Elo models interactions as occurring _in a sequence, between the entities themselves_, with the entities changing as a result of these encounters.

**Computationally**, Elo is $O(n)$ in the _number of matchups_ $n$ , with every matchup resulting in one constant-time ($O(1)$) update, with no minimum number of observations.

Unlike the other algorithms discussed, which generate weights at once using _all_ of the observed preference data, Elo is an _online_ algorithm, meaning that the rankings are updated after every match -- and are thus dependent on the specific sequence of the matches.
In addition, data are understood as the result of a matchup _between_ two items, _not_ as a vote on a pair of items by an independent observer.

While often proposed as a candidate algorithm for capital allocation, Elo's ontology of _a sequence of matchups between items_ makes it a *bad fit* for the use-case, in which data takes the form of _a set of votes by third-party observers_.

### Bradley-Terry

[The Bradley-Terry model](https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model) is a popular model for generating weights based on pairwise preferences.

Bradley-Terry models every item as having a _latent strength_ $p$, and models the probability of item $a$ being preferred to item $b$ as follows:

$
P(a > b) = \frac{p_a}{p_a + p_b}
$

**Ontologically**, Bradley-Terry is fundamentally _Platonic_: pairwise observations are understood as random fluctuations revealing a hidden capital-T Truth.

**Computationally**, fitting a Bradley-Terry model is $O(nm)$ in the _number of matchups_ $n$ and _number of iterations_ $m$ needed to converge, requiring observations $O(k^2)$ in the number of items $k$.

Note the similarity to Elo, which also models results as a ratio of latent scores.
However, unlike Elo, Bradley-Terry produces weights in a batch based on a _set of unordered preferences,_ making it a better fit in the setting where we want to gather many inputs before making a decision.
In terms of computational complexity, Bradley-Terry models are typically fit using a statistical technique of Maximum-Likelihood Estimation, in which the underlying probabilities are iteratively updated to improve their fit to the observed data.

Bradley-Terry methods are popular in the academic literature, as they lend themselves well to evaluation and simulation -- one can begin with a fictional "ground truth," run a simulated voting process, and then evaluate how well the recovered weights align with the initial ground truth.
These types of simulations, while rigorous in the statistical sense, tell us less than we might like about how these models perform under real-world conditions.

### Spectral Methods

Spectral methods, the most famous of which is Google's PageRank, aggregate pairwise inputs into a "graph" of interactions, and then takes the weights from the graph's _principal eigenvector_.

In linear algebra, the _eigenvector_ ("self-vector") of a graph or matrix is the vector $v$ such that:

$
Xv = \lambda v
$

We can interpret this vector as the "direction" to which the _whole graph points_, which can be interpreted as a type of "center" or "steady state" of the data ([see visualization](https://en.wikipedia.org/wiki/PageRank#/media/File:Page_rank_animation.gif)).
Techniques for decomposing a graph into these components are known as "spectral methods" after the "spectrum" of latent values they reveal (just as white light is divided into a "spectrum" of constituent colors).

**Ontologically**, spectral methods invert the Bradley-Terry model by taking _interactions_ as the only knowable reality; weights are understood as _summary statistics_, not latent truth.

**Computationally**, spectral methods are $O(k^3 + n)$ in the _number of items_ $k$ and the _number of matchups_ $n$, requiring $O(k^2)$ observations.
That the computation grows with the number of items, not the number of votes, makes this technique shine in settings where many votes are cast on a small number of items.

> Note: spectral methods naively require $O(k^2)$ observations, but smart pair selection can reduce this to $O(k)$ (see "active ranking" below).

Spectral methods have a history dating at least back to [Keener (1993)](https://www2.math.upenn.edu/~kazdan/312S14/Notes/Perron-Frobenius-football-SIAM1993.pdf).
Historically, spectral methods were most commonly used for judging tournaments and competitions, in which the "votes" emerge _endogenously_ from interactions among the items themselves (i.e. two teams competing _with each other_, two websites linking _to each other_).
In 2018, my colleagues at Colony and I [extended these techniques to the domain of social choice](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3317445), modeling votes emerging _exogenously_ as voter judgments.
This work led to the development of [pairwise.vote](https://pairwise.vote/), the preferred pairwise UI for web3 public goods funding, used in both Optimism's RetroPGF and the first iteration of this year's Deep Funding initiative.

Pairwise methods were historically neglected relative to Bradley-Terry, until the [2015 Rank Centrality paper](https://arxiv.org/pdf/1209.1688) demonstrated both their statistical equivalence and computational advantages.
Perhaps the most important difference between the models is that spectral methods evaluate relationships _globally_ and leverage transitive relationships not explicitly observed: if A beats B, and B beats C, then a spectral method can infer that A likely beats C.
This propagation of signal creates more complex interactions, but also allows these methods to produce better results with less data.
Spectral methods are also robust against cycles and other intransitive relationships, for which they produce ties, not contradictions.

For these reasons, we believe spectral methods are a _strong choice_ for capital allocation, which cares about modelling relationships across an entire ecosystem.

### Deep Funding

Both Bradley-Terry and spectral methods have a major drawback: they are data-hungry, requiring votes on the order of $O(k^2)$, the square of the number of items $k$.
These large data requirements makes pairwise methods difficult to use in practice, as they make gathering sufficient data challenging.

Deep Funding is an alternative technique proposed by [Vitalik Buterin in late 2024](https://x.com/VitalikButerin/status/1867886974058520820), in which pairwise judgments are not used to generate weights directly, but rather to score competing weight _proposals_, which are produced externally.

> Note: this initiative is unrelated to [SingularityNET's Deep Funding](https://deepfunding.ai/) program.

Under the slogan of "[AI as the engine, humans as the steering wheel](https://vitalik.eth.limo/general/2025/02/28/aihumans.html)," Buterin introduces a model of social choice in which the weight proposals are produced _at scale_ by machines, with a relatively small amount of human input being used to score proposals.
This reframing of the problem -- and of the role of voters -- aims to produce better results with less human input, and can be seen as an alternative response to the attention problem we introduced earlier.

**Ontologically**, Deep Funding treats weights as _untrusted proposals_ and treats juror inputs as _samples of reality_ used to score and select the best proposals.

**Computationally**, Deep Funding is $O(nw)$ in the _number of votes_ $n$ and the _number of proposals_ $w$, requiring data on the order of $O(k)$ in the _number of items_.

> Given that weights are not derived from votes directly, Deep Funding may be better understood as a meta-algorithm than as a pairwise algorithm proper.

Unlike the $O(k^2)$ vote requirement of Bradley-Terry and the spectral methods, Deep Funding aims to produce results with only $O(k)$ votes and a small constant factor, on the order of _one vote for every ten items_.
This reduction in complexity from _quadratic_ to _linear_ means that Deep Funding methods can be applied to problems with many items, for which it would not be feasible to gather a large number of pairwise votes.

> Note that this smaller data requirement _does not_ take into account the computation needed to create the weight proposals themselves.

Deep Funding's central drawbacks is that the $O(k)$ votes are only enough to _score_ proposals, not to _produce_ them.
Ultimately, the method can only produce results as good as the proposals it receives, introducing new vectors of complexity, risk, and disruption.

## 2. Pair Selection

As mentioned earlier, a challenge of using Bradley-Terry and spectral methods is that they require a quadratic number of votes for a given number of items.
As a result of this explosion of interactions, producing weights for even 50 items might call for 2,000 votes -- a big ask, especially for communities _already struggling_ with voter apathy.

Developing techniques for managing this scale will be key to bringing pairwise methods into the mainstream.

Fortunately, two practical approaches already exist: star grouping and active ranking.

### Star Grouping

This approach, developed by the team at [General Magic](https://www.generalmagic.io/), introduces a pre-filtering step in which voters score each project on a scale of one to five stars.
These scores then bucket projects into one of five tiers, with pairwise comparisons being made only between projects of the same tier.
This reduces the number of votes required by 80%, by ensuring that the quadratic creation of pairs occurs in smaller sets.

Star grouping can also be adapted to settings where the categorization is not of _quality_, but of _type_.
In cases where the items being considered are not all of the same type, star grouping can cluster like items together, clarifying downstream voting.

### Active Ranking

Another approach for reducing the number of votes needed is through a technique called "active ranking," an adaptation of the "[dueling bandits](https://www.cs.cornell.edu/people/tj/publications/yue_etal_09a.pdf)" algorithm from machine learning.

Active ranking works by surfacing pairs not at random, but based on the _uncertainty_ of that pair.
The intuition is that among the entire set of items, some pairwise judgments are more "obvious" than others, and so don't need to be voted on (e.g. bear vs rabbit).
Active ranking directs scarce voter attention to the pairs which are the most ambiguous, and thus provide the most _information_ (e.g. bear vs lion).

In theory, we can imagine needing as few as $O(k)$ votes, albeit with a large constant factor -- an entirely different complexity class from $O(k^2)$.

To understand why this is possible, observe that any weighting of $k$ items can be expressed as a set of $k-1$ scalars (up to an overall scaling factor), representing the pairwise _ratio_ of two adjacent items:

$$
[a = .1, b = .2, c = .3, d = .4] <=> [b = 2a, c = 1.5b, d = 1.33c]
$$

This generalizes to an arbitrary number of weights and tells us that we can _in theory_ construct $k$ weights with only $k-1$ human inputs.
While this limit is not achievable in practice, we can attempt to approach it, reducing the data requirement to some multiple of the number of items, i.e. $10k$ by directing attention towards the subset pairs which are most competitive with each other.

> Note: the estimate of 10 votes per item is speculative and will need to be validated by future research.

Implementing active ranking is surprisingly straightforward.
For every pair of items $a, b$ we construct a Beta distribution $p_{i,j} \sim Beta(votes[a,b], votes[b,a])$ representing the ambiguity of the pair, and then sample based on $Var(p_{i,j})$.
This variance will be high for pairs with few or mixed observations, and low for pairs in which one item is repeatedly preferred -- directing voter attention to where it is most valuable.
Calculating these distributions can be done iteratively, with the relevant distribution being updated in constant-time after each vote.

Compared to star grouping, active ranking has several advantages.
First, active ranking permits $O(k)$ comparisons _total_, while star grouping implies $O(k^2)$ votes _per tier_.
Second, active ranking can be run transparently in the background, while star grouping requires an explicit voting step.
Third, active ranking allows for all projects to be compared, whereas star grouping precludes comparison between groups.

Note that active ranking is an _online_ process -- the order of votes _does matter_ for determining which pairs are more likely to be shown, although the final weight production remains a batch process using all available data.
This online nature of active ranking creates new attack vector, as prior votes now influence the likelihood of future items being shown.
Mitigating this risk will be an important part of bringing active ranking into production.

## 3. Interface Design

Another key consideration is _the design of the voting interface_.
A data analysis pipeline is only as good as the quality of the data it analyzes.
More so than with other methods, the interface of a pairwise process has significant impact on the quality of the data collected.

To illustrate this, imagine a hypothetical "bad" interface, showing only the names of the items being compared.
With this interface, participants must make decisions based only on their pre-existing associations, resulting in noisy and unreliable data.
In an even more extreme example, imagine a user deciding between two random strings -- a process which produces _pure noise_.

Taking it in the other direction, can you imagine an interface profoundly better than any you've seen before?
Why or why not?

Ultimately, the performance of a pairwise voting system is downstream of the interface.

### Voting and Session Times

Before getting into the specifics of UI elements, we should ask ourselves a basic "product" question: _how long_ should voters spend evaluating a given pair?
With a target time in mind, we can work backwards to make decisions about visual design.

In discussion, practitioners have proposed target decision times of as short as 5 seconds to as long as 5 minutes.
[Analysis of deep funding voting data]({% post_url 2025-08-03-deepfunding-jury-analysis %}) suggests that the "sweet spot" is about 30 seconds.
More time does not result in meaningfully better judgments, and reduces the total number of pairs submitted.
Less time, however, increases the likelihood of a random choice, and thus of measurement error.

Working backwards from this 30-second target, we can design an interface to provide as much information as can be processed in that time frame.

Beyond individual votes, we can also think about the voting "session" as another type of product.
If we see voting on a single pair as the atom of a pairwise process, a 30-second decision bundles naturally into the 5-minute voting sessions, yielding 10 new votes.
The 5-minute session becomes the unit of engagement -- light enough to be completed on the train or over coffee, yet substantial enough to move the process forward.

### Input Format

Another key question is whether voters will b e asked to make _ordinal_ judgments (A better than B) or _cardinal_ judgments (A 3x better than B).
While cardinal judgments are appealing at first glance, offering the promise of _more signal_, that promise is often unfulfilled.
It is typically the case that in _untrained audiences_, measurements of _psychic intensity_ are more likely than not to be measurements of _individual mood or personality_, yeilding mostly noise and little signal.

[An analysis of Deep Funding's initial juror data]({% post_url 2025-08-03-deepfunding-jury-analysis %}) showed that while the perceived numeric ratio of two projects' impact varied widely, the perceived _direction_ of the impact (whether A or B overall was more important) was remarkably consistent -- between 63% and 89% agreement, depending on the set of items being evaluated.
This implies that while voters struggled to provide consistent numeric evaluations of the relative impact between pairs of projects, they could more consistently determine which of two projects was more impactful _overall_.

It is, of course, not so simple, and questions of cardinality and ordinality continue to be explored by the academic community.
[One recent paper](https://arxiv.org/pdf/2504.14716) on LLM evaluation found that models which presented results with "distractions" like excess enthusiasm were more likely to be chosen in ordinal matchups, while both neutral and "distracting" responses received similar cardinal ratings, suggesting that, at least in the case of LLM judgment, cardinal methods may be robust in ways that ordinal methods are not.
[Another recent study](https://pmc.ncbi.nlm.nih.gov/articles/PMC9586273/pdf/pnas.202210412.pdf) found that over long periods of time, cardinal measures of personal wellbeing were correlated with objective outcomes (such as moving to a new neighborhood if unhappy where you live), suggesting that cardinal judgments are not always noisy or idiosyncratic, but consistent captures sentiment at scale.

The question of cardinal vs ordinal judgments is far from settled, and much depends on the specifics of the problem and the audience.
However, it does seem that in our setting of decentralized capital allocation by large heterogeneous groups of voters, that ordinal judgments should be, at the very least, the default.

### Visual Elements

When it comes to visual design, the Pairwise team has arguably gone the furthest.
Consider the interface they developed for the Deep Funding pilot:

**Pairwise.vote**

![Pairwise Sample Interface](/img/pairwise-ui.png)

Here we see a number of design elements:

- Each item clearly indicated by name and logo
- A set of curated and domain-specific metrics
- An AI-based textual summary of the project
- The ability to choose either item, or to skip

These elements form the foundation of an effective decision process.
The metrics enable immediate, quantitative contrast between the two items, while the text summary gives the voter deeper context on individual items.
Letting the voter skip pairs reduces the incidence of bad data, in cases where a voter genuinely cannot differentiate between two items.

Further, this approach leverages both _metrics_ and _AI judgment_, while leaving the final decision in the hands of human voters.
The key insight is that while the metrics and summaries may be the same for every project, individual voters _qualitatively_ integrate the information differently, yielding richer results than would be possible by allocating funds by metric or AI judgment _directly_.
Pairwise methods are more robust to [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law)-style failures, common among metric and AI-based approaches, in which projects learn to "game the system" by tailoring their self-representation to more narrow and mechanical decision criteria.

**Verdict**

Here is another interface example, [Verdict](https://deepfundingjury.com/evaluation), recently developed by the Deep Funding team:

![Deep Funding Jury](/img/deepfundingjury-ui.png)

This interface is organized around the idea of "high quality bits," reflects the team's priors around data quality and their desire for fewer, highly selected votes.
This interface asks voters to make cardinal assessments of relative value, and asks for written explanations for their decisions.
In addition, the interface states that all votes will be reviewed by "meta-jurors" and potentially rejected if deemed unjustified.

This interface was developed following the initial pilot, which used the Pairwise.vote interface presented previously.
When analyzing the data from that pilot, the Deep Funding team found that their cardinal rankings varied significantly in scale and range per-voter.
Rather than adopt ordinal inputs, which are more robust to voter idiosyncracies, they chose to increase gatekeeping as a way of maintaining data quality.
It retains the use of AI summaries, but omits the metrics featured in the earlier iteration, pushing voters to rely more heavily on textual summaries.

**Hypothetical Mockup**

Finally, here is a mockup of a UI which I would consider closer to ideal, focusing on simplicity and comprehensibility:

![Pairwise Mock UI](/img/pairwise-mock.png)

This interface leans into ordinal inputs and prioritizes speed and access over gatekeeping, while leveraging AI summarization and metrics to standardize decision framing.

> It would be interesting for the Deep Funding team to A/B test these two designs, and empirically evaluate the differences in data quality and quantity produced by the two methods.

## 4. Audience Selection

The next key consideration when running a pairwise voting process is audience selection and development.

**Audience Selection**

Pairwise methods are well-suited to the setting of _distributed capital allocation by a heterogeneous audience_, with many different people coming together to distribute shared resources.
They succeed by directing participant attention efficiently over a range of items, without requiring deep prior knowledge of the items in question.

Pairwise methods are less effective when used by a _small group of experts_, who are more likely to have _strong prior knowledge_ of the items in question.
For this audience, who has _already performed_ the cognitive labor of developing opinion, assigning weights directly might be more efficient and more natural.

> To give a concrete example, during the Deep Funding pilot a senior Ethereum community member criticized the process, on the grounds that they had already formed clear opinions about the right weights for individual projects, and felt the pairwise process impeded their ability to communicate those opinions.

It is also possible to have an audience which lacks a _minimum baseline_ of context, such that even with a quality interface are unable to meaningfully distinguish between items.

The ideal audience, then, is a _large and diverse group of people with at least some domain knowledge_, able to make judgments on never-before-seen pairs after about 30 seconds of absorbing information
This group will be able to provide the most information, in terms of both _quantity_ and _quality_ of inputs.

**Audience Expectations**

Relatedly, it is important that participant _expectations_ be set appropriately.

Pairwise methods don't ask participants for weights directly, but infer them _indirectly_ using an algorithmic process.
For audiences used to assigning values directly, "giving up control" of the weights can be disorienting.
After Optimism's RetroPGF 3, General Magic [interviewed participants](https://gov.optimism.io/t/pairwise-retrospective-and-proposed-spec-for-retropgf-4/7479) and found that while participants found the system engaging and an aid to discovery, they also struggled with expectations shift of not setting weights directly.

Communicating the behavior of the system, and making the end-to-end process legible for participants, is key to building trust in these methods.

**Audience Segmentation**

Every voting process needs some way of segmenting and evaluating its participants to prevent vote manipulation.
At minimum, this means some form of [sibyl resistance](https://en.wikipedia.org/wiki/Sybil_attack), whether tokens, identity "passports," or webs-of-trust built off of pairwise attestation.
Choosing the right solution will again be a function of problem and audience.

The dual of sibyl resistance is making better use of expert attention through reputation systems.
Just as much as we discard fraudulent votes, we can give leverage to experts by assigning their inputs a higher weight.

One might imagine a continuous funding process in which the majority of the community engages early, making a "first pass" over the items, to be followed by expert assessment of only the most ambiguous pairs.

# III. Continuous Funding

Possibly the most significant application of the pairwise paradigm is towards the idea of "continuous funding."

Historically, most public goods funding takes place via "rounds."
Every round is a discrete event, featuring a slightly different set of projects and requiring an entirely new set of votes.

This reproduction of voter labor in every round is inefficient, both because most projects will not change much between rounds, and because voters will maintain similar opinions from round to round.
[Looking at data](/data/gg-rankings.csv) from Gitcoin Grant rounds 20 and 22, which took place six months apart in April and November 2024 (disclosure: I participated in both rounds), we see that 52% of the top 25 projects in their "dApps and Apps" category stayed consistent between rounds.
If the ecosystem is evolving only 50% between rounds, then the round-based approach is wasting half of its voter attention.

One might propose transferring votes from round to round, so that a voter does not need to submit potentially redundant new votes.
This transferring of vote information between rounds is theoretically challenging, however, as individual item judgments are _implicitly_ a function of the entire item set -- perhaps I give a project A $10, but if B had been an option, I might have only given $5.

On the other hand, the self-contained, "atomic" nature of pairwise judgments lend themselves more naturally to _continuous processes_ in which always-on voting interfaces can be used to _continuously_ monitor and update _ongoing_ funding flows in response to new information.
Rather than repeating redundant work each round, preferences can be continuously aggregated into a single "source of truth" that incorporates new items and retires old ones.
By gathering new inputs only as-needed, voter attention is converted into useful information at high efficiency.

Continuous funding systems introduce new considerations, which we explore in the following sections:

### Cybernetic Allocation

With most prize and grant programs, there is an expectation that the organizers will "get it right" the first time.
These are labor-intensive, high-stakes processes on which much depends.

Continuous funding processes allow for a more relaxed attitude towards "correctness," as the opportunity to course-correct is built right in.
It becomes more acceptable to "throw something out there" with the confidence that allocations will be updated in response to new information, and that over time the resources will be directed to where they are highest leverage.

This "cybernetic" approach to capital allocation -- focusing less on specific "point" solutions and more on dynamic _processes_ -- promises to be more robust and resilient compared to intensive, round-based approaches.

### Stale Voting Data

As previously mentioned, one of the advantages of pairwise judgments is that they can be meaningfully re-used between rounds.
However, while in theory a vote between two pairs is perpetually valid, _in practice_ we should be wary of relying on stale data.
In reality, projects are always evolving, and a preference for A over B may become increasingly inaccurate if A stagnates while B thrives.

One approach to balancing this trade-off is through a decay process in which votes lose their impact slowly over time, perhaps decaying to zero over a two-year period.
Many types of decay curves are possible, all reflecting different assessments of how fast this particular reality changes.

By incorporating a "vote decay" we extend the life of voting data while minimizing the potential impact of stale data.

### Permissionless Entry

Most public goods funding rounds have high overheads, with staff needed to screen projects, run communication, and ensure performance.
A continuous funding system could be made fully permissionless, enabling efficient capital allocation at lower cost.

A fully permissionless system would let projects add themselves to the pool, potentially requiring them to put up a stake.
Once entered, the active ranking process would quickly surface the high-variance new project, allowing it to quickly "find its level" of funding.
Projects that perform poorly -- say, more than three standard deviations below the mean -- would be evicted from the pool, forfeiting their stake.

Pairwise methods are uniquely suited to enabling this type of permissionless, self-correcting process.
Octant [has recently experimented](https://streamvote.octant.build/) with continuous funding, with quadratic voting being used to distribute a flow of funds.
However, as QV lacks the attentional properties of pairwise methods, this initiative required heavy curation on the part of the organizers, consuming resources which could have otherwise been directed towards the projects themselves.

### Process Tempo

Even a truly continuous process might benefit from a periodic tempo of participation.
By organizing participation in "sprints," it becomes easier to command a community's attention, who might otherwise forget about a process which is "always on."

One could imagine running "campaigns" to encourage people to vote, where leaderboards and other activations spur a wave of data-collection and keep the data fresh.
One could also imagine making payouts on a monthly or quarterly basis, or conditioning payouts on milestones determined by a separate governance process.

The user experience could be made _qualitatively_ similar to a conventional round-based process, but running on a continuous substrate in which allocations both update and distribute in real-time.

It is worth noting that even an ideal audience will not show up for free; participation must have incentives -- either relational (status), financial, or both.

### Funding Rates

In a continuous process, one must answer the question of "how fast should I distribute the money?"

One approach would be to give it out at a _constant_ rate over some period of time, let's say four years.
This approach would give out 50% of the funds after two years, and 100% after four years, at which point the process would end (assuming no new funds).

Another approach, proposed by the Colony team [in their 2018 whitepaper](https://uploads-ssl.webflow.com/61840fafb9a4c433c1470856/639b50406de5d97564644805_whitepaper.pdf), would be to distribute funds at an _exponentially decaying_ rate, such that funds are distributed according to a "half life" of, say, one year.
This approach would give out half the funds in the first year, and then half of the remaining half in the second year, and so on.
The benefit of this approach is that the funding process never truly ends, but rather continues indefinitely at decreasing levels.

In both cases, more funds should continue to be raised, extending the funding process indefinitely.
The topic of fundraising, however, is beyond the scope of this argument.

## Putting it Together

As argued in the introduction, pairwise methods should be understood not as a single technique or mechanism, but as a _paradigm_ of social choice.
Having introduced the various pieces of this paradigm, we can begin putting them together, and begin to estimate the actual attention requirements for public goods funding processes.

Assuming **30 seconds per vote** and **10 votes per item**, pairwise methods can produce allocations at an attentional cost of  **5 minutes** per item.
For a set of 600 items, this means **50 hours** of total voter attention.
If we assume each voter contributes four five-minute sessions (20 minutes), then we need only 150 voters to produce legitimate results -- a relatively easy lift.

As a continuous process, things get even better.
If we assume that only ~20% of the items undergo meaningful change in a given quarter, we can sustain a continuous funding process _indefinitely_ with an attention cost of **4 minutes per item per year** (5 min * 20% * 4 quarters).

The idea of sustaining a complex public goods funding ecosystem with such little effort might seem implausible.
The continued development of these techniques will almost certainly surface new challenges and limitations.
And yet, the arguments have been laid out, and these are the conclusions we've drawn.

# IV: Conclusion

## Challenges and Limitations

While compelling in many ways, pairwise methods have limits.


### The Independence of Irrelevant Alternatives

The "independence of irrelevant alternatives" (IIA) is a key concept in social choice.
The principle of IIA says that the relative ranking of two options must never depend on a third (the "irrelevant alternative").
In practice, almost every voting system violates this ideal in some way; the question becomes why and to what degree.

Some pairwise algorithms, such as spectral ranking, _intentionally_ draw in that third option to enable richer comparisons with less data.
This produces results which reflect a global perspective, incorporating more data, but increases the likelihood of unexpected interactions.
This unapologetic rejection of IIA is acceptable in the setting of capital allocation, where the goal is to distribute resources across an entire ecosystem.

In high-stakes, single-winner settings like elections, however, these complex and non-linear interactions might undermine the perceived legitimacy of the process.
In those settings, a Condorcet method with stronger guarantees would almost certainly be preferable.

> Note: Individual pairwise judgments _are_ in fact independent of alternatives; it is the final result which is not.

### Intransitivity of Preferences

Related to IIA in the social choice literature is the idea of cycles and of the _transitivity of preference_ -- the idea that if you prefer A to B, and B to C, then it is logically consistent that you would prefer A to C.
To prefer otherwise creates what is known as a "cycle" of _intransitive preferences_.
For some voting methods, including Condorcet methods, cycles represent _contradictions_ and are seen as inherent flaws.

Spectral methods, on the other hand, handle intransitive preferences naturally -- they are not contradictions, but information.
Cycles are interpreted simply as ties, which pose problems for single-winner settings like elections, but not for capital allocation in which funds are simply given out equally.

Further, pairwise spectral methods allow for a different interpretation of intransitivity.
Unlike Bradley-Terry, which models every item as having a latent value, and thus interprets intransitivity as measurement error, spectral methods model intransitivity as a normal part of reality.

To give an example, imagine items A and B, each having qualities X and Y.
If we conceptualize voters as making pairwise decisions based on _subjective integrations_ of the presented data, one voter might integrate X and Y and choose A, while another, filtering through the lens of their own personal beliefs and live experience, might choose B.
Over hundreds or thousands of voters, the pairwise graph becomes a rich field of relationships with substantial cyclical and intransitive behaviors.
Taking this graph as the only knowable ground truth, we then produce weights as an _actionable synthesis_ of that rich data.

One might imagine going even further, devising new metrics for community dynamism based on the degree of intransitivity in a given preference graph.
This view of pairwise data -- not as messy and needing of discipline -- but as rich and nuanced truth, invites bold new visions.

### Dealing with Heterogeneity

One of the few prerequisites to using pairwise techniques is making sure that the items being compared are meaningfully comparable.
This may sound tautological -- but it is by no means guaranteed.
To give an example, one can meaningfully prefer an apple or an orange; one cannot meaningfully prefer an apple to the _color_ orange.

Part of the practitioner's skill is ensuring that the items being considered are part of a semantically coherent set.
This meaning can come from both grouping like items together, or by framing the comparison in a way which makes sense for the given set.

To give a concrete example, this year's Deep Funding initiative framed the decision in terms of the relative impact of two _software dependencies_ on a given _software project_.
In that setting, the same dependency might be assessed very differently depending on which project's context was being considered.

Also, as mentioned earlier, techniques like star grouping can be used to subdivide heterogeneous sets in cases where meaningful groupings may be difficult to define in advance and must be constructed on-the-fly.

### Evaluation

At the start of this essay, we argued that the limitations of pass/fail voting led to a shift in interest towards capital allocation.
Capital allocation, however, has its own challenges: in particular, evaluation.
As has been well-documented by Metagov's [Grant Innovation Lab](https://grant.metagov.org/), difficulties in evaluating the effectiveness of any grant program or allocation is leading to an erosion of trust in public goods funding overall, and a slow reduction in funding for such programs.

In recent months, the public goods funding community has increasingly begun prioritizing _evaluation_ over _experimentation_.

On some level, evaluation is an impossible and fundamentally speculative task.
If someone who wanted to support public goods was able to evaluate the future impact of a present investment with certainty, they would be better off making billions on Wall Street and starting a foundation in their name.

Given that nobody does that, it's fair to ask what evaluation actually achieves.
Ultimately, _evaluation produces legitimacy_, which translates concretely into higher future funding inflows.
By instituting robust evaluations, a funding process earns legitimacy and is able to attract a greater share of the available funding.

What are some possible evaluation techniques?

One possibility, adapting [techniques used to evaluate large-language models](https://arxiv.org/pdf/2403.04132), is to subject allocations _themselves_ to pairwise judgments.
In addition to pairwise judgments _between projects_, the community (or experts within that community) can make pairwise judgments _between allocations_.
By comparing the outputs of different allocation processes, a community can essentially vote on the "policies" governing how resources are distributed: this algorithm vs that, this paramaterization vs that.

Another possibility, often advocated by Ethereum's leadership, is to lean into "info-finance" as a tool for producing high-quality predictions about the future.
Unlike votes, which reflect subjective opinions, financially incentivized predictions can _in theory_ be treated as objectively reliable sources of information.
Info-finance is not my area, so I cannot comment deeply on the strengths and weaknesses of this design, but these approaches have always struck me as a touch reflexive, with predictions and allocations influencing other in complex and hard-to-model ways.

> This is not idle speculation. [The proliferation of sports betting apps has begun affecting player behavior](https://www.espn.com/espn/betting/story/_/id/47337056/scandals-prediction-markets-2025-turning-point-sports-betting), who exploit their position to resolve markets in their favor.

Yet another possibility would be to develop new metrics for evalauting the "health" of a funding process.
By tracking metrics such as the degree to which a funding distribution follows a power-law, or the churn of top projects over time, one can assess how a funding process is performing relative to an abstract baseline.

Whatever approach is used, it is virtually certain that evaluation will become table-stakes for those looking to implement capital-allocation schemes.

## Final Thoughts

The task of helping large groups of people effectively manage shared resources is one of the critical problems of our day.
We have tried to show that pairwise methods, seen not as isolated techniques but as part of a _paradigm_ of social choice, offers a compelling toolkit for solving exactly this problem.

Relative to other techniques and to their underlying potential, however, pairwise methods remain underexplored.
By articulating a "pairwise paradigm," we hope to help chart the way.
