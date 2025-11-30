---
layout: post
title: "The Pairwise Paradigm"
comments: true
categories: blog
tags:

- public goods funding
- impact evaluation
- mechanism design

---

# I. Motivations

[There is no perfect voting system.]({% post_url 2020-04-04-gaming-the-vote %})
The truth and tragedy of this statement has been understood by scholars for decades, epitomized by Kenneth Arrow's famous "impossibility theorem" demonstrating the fundamental limits of ranked-choice voting systems.

On a fundamental level, the problem stems from attempting to measure complex social reality under conditions of high stakes.
In attempting to distill subjective reality into objective votes, information is inevitably lost; the measurement process itself becomes an arena for power contestation.
The best we can do, ultimately, is to design _task-specific_ voting systems in which the gap between subjective experience and objective input is as small as possible, minimizing the scope of conflict and increasing the utility and legitimacy of these systems.

Several years ago, [I predicted]({% post_url 2019-05-08-against-voting %}) that challenges with pass-fail voting would shift governance interest away from proposal-driven governance and towards distributed capital allocation.
Over the last five years, that prediction has largely been born out: instead of electing representatives to develop budgets, we increasingly try to allocate resources _collectively_.
The shift from discrete outcomes (you win, I lose) to _continous outcomes_ ($10 to you, $5 to me) opens up a rich design space which, critically, sidesteps some of the fundamental limits implied by Arrow's Theorem.

Within the domain of decentralized capital allocation, several classes of techniques have been explored:

- **Quadratic Funding**, in which direct donations double as "votes" dividing a matching pool, subject to square-root constraints.
- **Pairwise Preferences**, in which inputs are framed as "A vs B" and converted into numeric allocations via an algorithm.
- **Metrics-Based**, in which votes are made on high-level metrics, and allocations are made indirectly based on these metrics.
- **AI-Augmented**, in which AI agents analyze grantees and recommend allocations.

Each of these approaches has strengths and weaknesses:

- **Quadratic Funding** struggles to efficiently allocate attention across projects, creating "beauty contests" and rewarding hype.
- **Pairwise Preferences** struggles to get sufficient coverage and voter engagement to produce reliable results.
- **Metrics-Based** struggles with "Goodhart's Law" failures and incentivizes grantees to fabricate data.
- **AI-Augmented** struggles with issues of alignment, legitimacy, and decision quality.

[I have been researching and working with capital-allocation systems since 2016](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3359677), and believe that the best path forward is to continue advancing the theory of _all_ of these techniques, and to develop a culture of practice which is able to select from among them based on the specifics of the problem, and audience, at hand.

The rest of this essay will focus specifically on pairwise preferences and lay out a roadmap of how they might develop over the next few years.
We will argue that pairwise methods should not be understood as isolated mechanisms, but as part of a larger _paradigm_ of decision-making involving various interacting techniques.
By approaching pairwise methods in this way, it becomes easier to see how the pieces fit together and offer a compelling approach for allocating shared resources.

# II. Why Pairwise

A pairwise preference is simply a choice between two options.
As such, pairwise preferences can be seen as the "atom" of human subjectivity: the simplest possible distinction, running on the "phenomenological bare metal" of human perception.
This simplicity makes them both very robust (they mean what they say they mean), accessible (anybody can make a relative distinction), general (many decisions can be framed in relative terms), and flexible (pairwise preferences can be aggregated in many different ways).

Pairwise preferences have been studied for decades, beginning with the work of psychometrician L. L. Thurstone in 1927 and his research into subjective responses to stimuli.
Pairwise preferences would go on to find many applications in the ranking and ordering of items: from ranking chess players through ELO to weighting web pages through Google's PageRank.
This dual heritage, as both a technique for subjective measurement (["high quality bits"](https://vitalik.eth.limo/general/2025/02/28/aihumans.html)) _and_ for allocating weights among items, suggests that these techniques have much to offer the practice of distributed capital allocation -- which must solve exactly these problems.

Despite these appealing qualities, pairwise methods have remained relatively niche among distributed capital allocators.
Pairwise methods have seen some use, as a part of Optimism's RetroPGF program (helping to allocate $20mm in funding) as well in this year's [Deep Funding](http://deepfunding.org/) initiative.
However, they have yet to capture the same level of enthusiasm as other techniques discussed.

I believe that this is due at least in part to there being several major gaps in pairwise practice, and the lack of an overarching vision.
These gaps, which will be discussed below, make the technique difficult to use and difficult to communicate.
By more clearly articulating pairwise as a _paradigm_ of interellated techniques and practices, we can build more momentum around the techniques and help push the public goods funding ecosystem forward.

# III. The Pairwise Paradigm

## Algorithm Selection

Pairwise preferences by themselves do not determine rankings or weights.
Rather, they must be processed by an algorithm and _converted_ into weights using some process.
The choice of algorithm has major implications for what kind of output gets created.

This section will discuss several algorthmic options and their properties, with a focus on the _ontology_ and _computational complexity_  of each algorithm -- how each algorithm models reality, and how effectively it can processes information relative to that model.

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

As a result of this, I would say that Elo is the *wrong choice* of algorithm for capital allocation, in which we want to take large body of _interchangable_ votes and convert them into a single set of _a posteriori_ weights.

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
\lambda v = Xv
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
Importantly, these extra interactions violate a principle of social choice -- the irrelevence of irrelevent alternatives -- but also invites us to critically re-examine whether that principle is as meaningful in practice as it appears in theory.

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

Unlike the Bradley-Terry and Spectral methods, which requires $O(k^2)$ votes, Deep Funding aims to produce similar results with $O(k)$ votes or less, perhaps as few as one vote for every ten items.
This reduction in complexity from quadratic to sub-linear means that Deep Funding methods can be applied to problems not computationally tractable for the other techniques.

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

## Active Ranking

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
For every pair of items $a, b$ we create a Beta distribution $p_{i,j} ~ Beta(votes[a,b], votes[b,a])$ and choose pairs based on $Var(p_{i,j})$.
This variance will high for pairs with few observations or mixed observations, and low for pairs in which one item is repeatedly preferred.

Calculating these distributions can be done online, with the relevant distribution being updated after each vote.
Note that active ranking is an _online_ process -- the order of votes _does matter_ for determining which pairs are more likely to be shown.

## UI Development

Another important consideration is _the design of the voting interface_.
A poorly designed interface (as an extreme example, consider the choice of two random strings) will yield data close to random, while a well-designed interface will enable participants to provide quality feedback quickly and effectively.

### Voting Times

[Earlier analysis has shown]({% post_url 2025-08-03-deepfunding-jury-analysis %}) that the "sweet spot" for deciding on a pair is about ~30 seconds.
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
This makes pairwise methods more robust against Goodhart's Law-style failures, in which projects falsely represent themselves based on narrow decision criteria.

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

The ideal audience, then, is a _large group of people with some domain knowledge_, able to form a specific opinion on a newly-presented pair after about ~30 seconds of digesting new information.
This group is able to provide the most information, in terms of both _quantity_ and _quality_ of inputs.

## Leveraging Attention

USV's Albert Wenger [recently argued](https://open.spotify.com/episode/6XJOXe3whWTCm3TkuvAWQq?si=e51a8b5f558e43be) that "capital allocation is often downstream from attention allocation."
As society increasingly recognizes that attention is now its scarcest resource, attentional analysis of social choice becomes increasingly important.

### Item Discovery and Strategic Resistance

Compared to voting methods in which items are evaluated individually, pairwise methods more naturally spread attention across items by presenting them in(pseudorandom) pairs.
This pairwise approach builds in item discovery as a first-class construct, as even voters with strong preferences for individual projects will be asked to evaluate items for which they are unfamiliar.
By spreading voter attention more uniformly across items, it becomes more difficult to vote strategically and more difficult for projects to gain advantage through hype or marketing.

## Continuous Funding

To-date, most public goods funding takes place via "rounds."
Every round is a distinct event, featuring a slightly different set of projects and, crucially, requiring an entirely new set of votes.
This reproduction of voter labor in every round is highly inefficient, as most voters will maintain similar opinions from round to round.
Unfortunately, porting vote information between rounds is theoretically challenging, as individual judgments are implicitly a function of the entire item set.
If we assume roughly that 90% of voter preferences are the same between rounds, then the epoch-based approach is converting attention to information at a rate of only 10%.

In contrast, pairwise methods naturally lend themselves to _continuous processes_ in which an always-on voting interface can be used to continuously monitor and update ongoing funding flows in response to new information -- converting attention to information at 100% efficiency.
Rather than replicate work in every round, individual preferences can be continuously aggregated into a single "source of truth" trivially capable of incorporating new items or removing those no longer relevant.
Concerns about stale data can be handled through a notion of "decay" -- a voter's judgment on a given pair may become less consequential over time, fading from a strength of 100% down to 0% over some time frame.

Taken together, we can imagine a single always-on funding process, continuously allocating funding in response to new information, with a minimum of operational overhead or wasted attention.
If we imagine the round-based approach as a type of extractive mining, inefficiently converting attention to information, then the continuous-funding approach is more like solar power, continuously and efficiently converting ambient attention into information.

# IV: Conclusion

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

We have tried to show that pairwise methods, seen not as one-off techniques but as the foundation of a _paradigm_ for social choice, offers a compelling toolkit for solving one of the most challenging, and urgent, problems of our day.
