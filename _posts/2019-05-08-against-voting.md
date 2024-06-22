---
layout: post
title: "Against Voting"
comments: true
categories: blog
tags:

- technology
- governance

---

*An essay about how the way we make choices shapes the choices we make.*

We open by introducing a visual metaphor for describing the behavior of complex systems, and then modify the metaphor to instead describe "coordinating processes" -- the mechanisms by which we manage our collective social life. We focus on the legislative process as a central coordinating process, and attempt to understand this process using concepts from mathematics and computer science. Through this lens, we can understand some of the limitations of current processes, and also orient ourselves towards new processes which promise to overcome these limitations. We conclude with a ten-thousand-foot view of coordinating processes in general and a framework for thinking about them going forward.

# Introduction: Pace Layering

In counter-cultural icon Stewart Brand's 1999 book *The Clock Of The Long Now*, we find a useful image innocuously titled "Pace Layering":

<p align="center">
  <img src="https://s3.amazonaws.com/kronosapiens.github.io/images/pace-layering.png">
</p>

This image's thesis is that complex systems can be seen as a "layering" of multiple sub-systems, with "lower" systems (the more foundational) simultaneously enabling an environment and setting the boundaries within which the "higher" systems (the more discretionary) can operate. Lower systems are more critical, in that disruptions in lower systems require recalibrations of all higher systems, and are thus ideally slower to change than the more discretionary systems built on top of them.

Brand's conceputualization of these systemic layers developed out of [his theorizing](http://everwas.com/2015/01/stewart-brand-and-the-pace-layer-model/) on the lives of buildings: he noticed that different "layers" of a building had different rates of change: the building's floor plan; the arrangement of furniture; the location of people and things. This recursive or fractal pattern is found also in nature:

> Consider, for example, a coniferous forest. The hierarchy in scale of pine needle, tree crown, patch, stand, whole forest, and biome is also a time hierarchy. The needle changes within a year, the tree crown over several years, the patch over many decades, the stand over a couple of centuries, the forest over a thousand years, and the biome over ten thousand years. The range of what the needle may do is constrained by the tree crown, which is constrained by the patch and stand, which are controlled by the forest, which is controlled by the biome. Nevertheless, innovation percolates throughout the system via evolutionary competition among lineages of individual trees dealing with the stresses of crowding, parasites, predation, and weather.
> - Stewart Brand, *The Clock Of The Long Now*

As physical beings, visual and spatial metaphors are invaluable aids when reasoning about abstract concepts, and the notion of "pace layering" is a useful and flexible metaphor for organizing our thinking about complex systems.

# I. Coordinating Processes I

Let us take Brand's metaphor and adapt it to questions of social coordination:

<p align="center">
  <img src="https://s3.amazonaws.com/kronosapiens.github.io/images/coordinating_processes_1.jpg">
</p>

This (highly schematic) setup is found, in varying degrees, in states and organizations across the world. The layers can be summarized as follows: some foundational documents bootstrap the entity into being; a specialized body is entrusted with the interpretation of those documents. On top of that, we have more flexible and popular mechanisms via which some some subset of the community is periodically entrusted with special decision-making powers; these individuals then engage in a legislative/allocative process which invariably culminates in a series of pass/fail votes on some series of things, strings of text which take many forms but can be frequently bucketed into **policies** and **expenditures**. Finally, some other subset of the community is given operational discretion to use the expenditures to enact the policies.

From a theory perspective, innovations which change these systems without changing the arrangement of layers can be thought of as *marginal* or *incremental* changes, while innovations which change the number or relationship between the layers can be thought of as *paradigmatic* changes. This distinction is not meant to diminish the importance of incremental improvements: measures to reduce the impact of gerrymandering, voter suppression, and the influence of moneyed special interests will make the outcomes more representative and thus more legitimate. Such efforts are valuable and needed, as are efforts to improve the efficiency of the pass/fail decision-making process (including but not limited to "just putting it on the blockchain").

#### Parliamentary Procedure

> The trouble with socialism is that it takes up too many evenings.
> - Oscar Wilde

The set of rules by which these representatives reach their pass/fail decisions are collectively known as ["parliamentary procedure"](https://en.wikipedia.org/wiki/Parliamentary_procedure), the most protyptical of which is ["Robert's Rules of Order"](https://en.wikipedia.org/wiki/Robert%27s_Rules_of_Order). Parliamentary procedure can be thought of as a type of *string-processing algorithm* which composes long strings of text via a sequence of branching decision points (although more commonly we speak in terms of motions, seconds, amendments, and so on).

Robert's Rules (and systems like it) are general and secure, in that they allow groups to make nearly arbitrary decisions (encoded as plain text) while remaining robust to manipulation via strict branching rules, but are consequently (and as we will argue, necessarily) remarkably tedious and inefficient. The tedium of parliamentary procedure is a large part of the reason why our coordinating processes *assume the necessity of* special representatives, motivated by some mixture of duty, money, and power, to provide the cognitive power needed to run the algorithm.

This setup emerged slowly out of an even older one-layer process in which single individuals held virtually unchecked power for unlimited periods of time, and represented a paradigmatic change in coordinating processes. However, this setup seems to have remained largely uninterrogated in the last two hundred years or so; it seems to be received wisdom that we cannot do better than tedious voting on proposals, and that all we can do is make marginal improvements in the composition of the representatives and the particulars of the parliamentary procedure. But we *can* do better.

Unfortunately, naive efforts to "broaden the franchise" and invite large groups to participate in parliamentary process often fail due to [low participation](https://medium.com/wave-financial/blockchain-voter-apathy-69a1570e2af3
). This effect can be partially explained via the notion of ["rational ignorance"](https://en.wikipedia.org/wiki/Rational_ignorance) -- the idea that if the work required to acquire information is greater than the benefit of that information, it makes no sense to gather that information. In situations where large groups are invited to participate in pass/fail decisions on complex proposals, rational ignorance clearly applies, and further we can speculate that, in cases where many votes are cast, a large fraction may be cast somewhat randomly, intuitively, or emotionally, introducing noise into a critical signal.

So, we select and incentivize representatives because parliamentary procedure is *unavoidably tedious*. Parliamentary procedure is unavoidably tedious because it is *completely general*. Were the procedure to be specialized, it could be made more efficient and less burdensome, making broad-based, meaningful participation possible. To develop this argument further, let us consider the relationship between specificity and efficiency in more detail.

# II. Representation & Computation

Behold a taxonomy of *types of numbers*:

<p align="center">
  <img src="https://docs.google.com/drawings/d/e/2PACX-1vSafRXMCUGKBg3p_zHBtJ2GCQJJtWa_qEM5q5FHSOrIiM-DPA16R-qKq4dEWC873mSXfduEJG-pT9Lw/pub?w=975&h=812">
</p>

The most *general* type of number (as far as this discussion is concerned) is the **real multivariate**, consisting of, unsurprisingly, one or more real numbers. A list of baseball batting averages would fall into this category. The most *specific* type of number is a **binary univariate** (more commonly known as a bit), taking on only the values of 0 or 1. In between we have a variety of other types of numbers: discrete (the integers), univariate (just one number), and so on. Note that a binary bit is still technically a multivariate real, but where the "multi" happens to be one and the "real" happens to be limited to the values 0 and 1.

The key point is that pass/fail voting makes use only of the most *specific* number -- the binary bit, yes or no. The bit is the most specific type of number, but therefore the most *general* in terms of possible applications: any decision can be made by a pass/fail vote on a *description of the decision* (how that description is created, however, is another matter).

We can demonstrate this generality via an example from computer science. Imagine we would like to know an integer $$k$$. We have two oracles: one which returns $$k$$ itself (a discrete output), and another, which, when given an integer $$q$$, tells you if that integer is either *greater* or *less than or equal* to $$k$$ (a binary output). While the first oracle would clearly get us to $$k$$ faster, note that you could use the second as well: you would simply have to query this second oracle many times (up to $$log(n)$$ times for a $$k$$ between $$0$$ and $$n$$), as you iteratively hone in on $$k$$ via a binary search. The binary output lets us approximate the discrete output, but slowly. As an aside, this technique (the reformulation of arbitrary algorithms as binary ["decision problems"](https://en.wikipedia.org/wiki/Decision_problem)) is used in computer science as part of the analysis of algorithms, useful in settings where you want to "compare" algorithms with different types of outputs.

More specific numbers (bits) are less *efficient* carriers of information, but are consequently more *general* with regard to the purposes to which they can be put. A string of bits can be a number, an image on a screen, or the outcome of a vote. Likewise, a mechanism of pass/fail voting can be used to decide on virtually anything (assuming the existence of a secondary process which can compose the string of text representing the decision).

However, this street runs two ways: a more *specific* number can be used to implement a more *general*, while a more *general* number can always be treated as if it were are more *specific*. Consider: a single bit (`0`) used to implement a uint8 (`10101010`) used to implement a single bit: (`00000001`). In fact, we can think of the second oracle in our earlier example as "constructing" the number $$k$$, bit-by-bit. Clearly, a process which returns one byte of information at a time (*assuming a sufficiently low signal-to-noise ratio*) is more efficient than one which returns only one bit.

Further, a byte contains more information than eight *independent* bits (the bits in the oracle example are *not* independent), for the reason that the number of meaningful states is much larger: `8` possible states for eight independent bits in which the order does not matter (since only the counts are unique), compared to `2 ** 8 == 256` for eight interdependent bits in which order does matter and therefore every permutation is unique. Of course, in the real world nothing is every *truly* independent, inasmuch as history is in fact a single non-repeating event, but the point is made.

It is a perhaps counterintuitive but nonetheless essential result that if a problem can be made more *specific* (for example, by connecting the items so that the *order* becomes a vehicle for encoding information), it may be possible to develop more *efficient* solutions which are able to process more information per unit-of-computation, encoding this information using more *general* or *expressive* types of numbers.

#### A Case Study

Let us make this disucssion concrete via a brief case study of Quadratic Voting, an alternative voting mechanism. With QV, participants are allocated some number of "voice credits", which they can exchange for actual votes on pass/fail proposals at a quadratic exchange rate (`n` votes costs `n * n` voice credits). This mechanic has [been shown](https://www.wired.com/story/colorado-quadratic-voting-experiment/) to [significantly increase](http://egap.org/file/1604/download?token=T_jeJe1f) the clarity of signal coming from voters by allowing them to allocate more voice credits to issues that they feel strongly about, in exchange for less influence on issues they care less about.

In our telling, we can understand Quadratic Voting as a mechanism which extends regular voting in a way which makes the outcomes of various proposals *interdependent* on each other -- since placing multiple votes on a single issue entails withholding many more votes on other issues, the output of this procedure changes from univariate binary (each proposal is independent, with a one-bit outcome) to multivariate binary (we can only meaningfully talk about proposals as a set, since voters need knowledge of the multiple proposals to be able to place their votes). Put another way, the output of a QV process is more *relative* than *absolute* in character.

So we see that by making a mechanism more *specific* (for proposals to be meaningfully compared, they must be of similar "kind" and grouped together), we are able to deploy a more *general* type of output (multivariate binary), and exploit this structure (the ordering of bits) to convey additional information, achieving significant *efficiencies* in terms of translating subjective preference into objective decisions.

# III. Against Voting

This essay is provocatively titled "Against Voting", but here we show our hand: we are "against voting" only when "voting" refers to pass/fail decisions on long strings of natural language text. In common use, "voting" is also used to describe the act of selecting representatives, and "voting" can even be used to describe the process by which we determine expenditures. For a modicum of clarity, let's talk about "voting", "electing", and "budgeting" to refer to these separate activites. We "vote" on policies, "elect" our representatives, and "budget" for expenditures.

Here is a table which summarizes a number of popular "input mechanisms", as well as their applications, their most general number types, and where the "processing" occurs (i.e. cognitive or computational, or "does the computer add any non-trivial value to the inputs"). Recall that anything used for voting can be inefficiently used for electing, and anything used for electing can be inefficiently used for budgeting. Likewise, anything used for budgeting can be re-purposed for electing (rank the items by the value they receive), and anything used for electing can be re-purposed for voting (an election with two candidates: "pass" and "fail).

<table align="center">
  <tr><th>Mechanism</th><th>Applications</th><th>Input</th><th>Output</th><th>Processing</th></tr>
  <tr><td><a href="https://en.wikipedia.org/wiki/Majority_rule">Majority</a></td><td>Voting</td><td>Univariate Binary</td><td>Univariate Discrete</td><td>Cognitive</td></tr>
  <tr><td><a href="https://en.wikipedia.org/wiki/Quadratic_voting">QV</a></td><td>Voting</td><td>Multivariate Discrete</td><td>Multivariate Discrete</td><td>Cognitive</td></tr>
  <tr><td><a href="https://en.wikipedia.org/wiki/First-past-the-post_voting">Plurality</a></td><td>Electing</td><td>Multivariate Binary</td><td>Multivariate Discrete</td><td>Cognitive</td></tr>
  <tr><td><a href="https://en.wikipedia.org/wiki/Score_voting">Score</a></td><td>Electing</td><td>Multivariate Discrete</td><td>Multivariate Discrete</td><td>Cognitive</td></tr>
  <tr><td><a href="https://en.wikipedia.org/wiki/Instant-runoff_voting">IRV</a></td><td>Electing</td><td>Multivariate Discrete</td><td>Multivariate Discrete</td><td>Computational</td></tr>
  <tr><td><a href="https://en.wikipedia.org/wiki/Dot-voting">Dot</a></td><td>Budgeting</td><td>Multivariate Real</td><td>Multivariate Real</td><td>Cognitive</td></tr>
  <tr><td><a href="https://en.wikipedia.org/wiki/Power_iteration">Power</a></td><td>Budgeting</td><td>Multivariate Binary</td><td>Multivariate Real</td><td>Computational</td></tr>
</table>

<br />
The first thing to notice is how the problem of voting differs from that of electing and budgeting. With pass/fail voting on strings of text, the only question we can meaningfully ask is "is *this thing* better or worse than the status quo?", and the only way to answer that question is by performing extensive cognitive labor, in large part because strings of natural language text have little formal structure and are thus difficult to analyze computationally (not for [lack of trying](https://en.wikipedia.org/wiki/Characteristica_universalis)). Calculemus!

The difference with electing and budgeting is that their questions are phrased not in terms of absolutes, but in terms of relationships ("is this thing better or worse than that thing", and "how much should this thing get compared to that thing"). This distinction is important because, as I am going to suggest, mental concepts (and so our understanding of the world) are *relational* in character. We understand things not in terms of their absolute nature, but rather by their relationships to the things around them.

This is true for elections, and doubly true for budgeting, a delightfully constrained setting in which the *only* question we ask is "is this thing more important than that thing". Very few people will dispute the absolute value of public education, public safety, public health, public infrastructure, and low deficits; the interesting things happen only when you ask people to choose between them. Budgeting is a crucial exercise in relativity.

We return to our theme. Consider for a moment that part of the reason which budgeting is *seen as difficult* is because we are making absolute decisions about relative questions. "Should we fund the police" is a meaningless question; "should we fund police before we fund education" is a meaningful one. By posing the question in terms of absolutes rather than relative degrees, we create an inefficient process (recall the binary oracle), and by framing budgeting questions as binary decisions about strings of text, we push the majority of the information processing "outside of the decision process", which in addition to increasing the cognitive burden on participants, increases the risk of error, capture, and manipulation.

#### A Category Error

We have inherited a categorical error in our collective handling of finances. Our familiar coordinating processes were developed in an age where information traveled at the speed of horse and computations ran on ink and parchment. Cognition and computation were one and the same. The methodological questions discussed here were on exactly nobody's radar (had there even been a radar to be on). But new tools bring into view new solutions, and new solutions shine light on present shortcomings, and it is time to move on. By teasing apart decisions about expenditures from decisions about policies, we can approach the question of allocation with a more precise and powerful set of tools than that of legislation writ large. We can deploy specialized mechanisms with information-rich outputs, and leverage computational techniques to perform the heavy lifting, generating these outputs from cognitively simpler but useful inputs.

Phrased differently, we can move from "simple inputs on complex objects" (cognitive complexity) to "complex inputs on simple objects" (computational complexity). A national budget is a complex object, but a relative choice between "infrastructure" and "education" is a simple one. By providing more complex inputs, such as a multivariate real describing percentage allocations, or a series of pairwise decisions bits (the simplest unit of relative information), we can shift the processing burden from cognition to computation, and by extension, change the *experience* of budgeting entirely.

Specifically, both Dot Voting and Power Budgeting represent alternatives to conventional proposal-based budgeting processes. The former asks participants to allocate percentages among various items, with the constraints that the sum of percentages must not exceed one. The latter asks participants to submit a sequence of explicitly pairwise preferences between items ("is A more important than B"), and then converts them into budgets using well-established mathematical techniques. In both cases, inputs are submitted under *relative constraint* (as with the Quadratic Voting example), which renders them more information-rich than when inputs are made without contraints, as in the case of score voting or Likert scales.

As an aside, it's not clear how it ever became acceptable to have people provide input using unconstrained numeric scales. It would be as informative and more honest to ask people to compose haikus describing their affect towards the item in question.

# IV. Coordinating Processes II

Our inherited miscategorization of questions of expenditure as questions of policy has limited the possible solutions available for solving those problems; recategorizing questions of expenditure will firstly allow us to incrementally apply a more powerful set of tools to answering these questions, and secondly and more importantly allow us to contemplate paradigmatic changes to *where* questions of expenditure are answered:

<p align="center">
  <img src="https://s3.amazonaws.com/kronosapiens.github.io/images/coordinating_processes_2.jpg">
</p>

The relocation of complexity in the computer, rather than the person, means that the computer can act as the chair and facilitator of the process, enabling a large group of participants to asynchronously collaborate in the allocative process. Thus, in addition to the incremental improvements we would see from improving existing budgeting processes while holding the set of participants fixed (i.e. maintaining the practice of electing representatives), the adoption of new budgeting processes would allow us to "extend the budgeting franchise" to the entire population: a *paradigmatic* change in which allocation becomes a coordinating process *more fundamental* than the election of representatives: whereas currently we provide oversight of finances via our choices of representatives, in the future we can provide oversight over representatives via our choices about allocation.

Further, while univariate binary outcomes are by definition all-or-nothing, and so many voices ultimately do not matter, multivariate real outcomes are capable of "shades of gray", of incorporating minority voices in incremental degrees: as a single participant, my input really does matter. This eliminates much of the challenges of collective action, and changes the emotional relationship the participants have to the system: active participants instead of passive validators.

# V. Surely You're Joking

Let us consider and rebut some possible objections to this thesis:

> Partial funding will lead to failed projects. Things must be funded fully or not at all.

We believe that this type of thinking is fundamentally flawed.

The future is a big place. To say that something is "fully funded" implicitly implies knowledge of the future (`fullyFunded => knowledgeOfFuture`). The converse of this is that if there is no knowledge of the future, nothing can ever be said to be fully funded (`!knowledgeOfFuture => !fullyFunded`). Since no one has knowledge of the future (`!knowledgeOfFuture`), it is not meaningful to think of something as "fully funded" (`!fullyFunded`). Things change all the time. Organizations grow and shrink into the money they have.

There may certaintly be edge cases where some item is uncomfortably underesourced for a period of time, but in general this should be considered a straw man argument until experience proves otherwise. More important than pursuing fictitious goals like "fully funded" is to pursue flexible allocation mechanisms which can respond effectively to new information as it becomes available.

> The vision of broad-based input is unrealistic. We know from experience that voter turnout is low.

It is true that voter turnout for referrenda is often low, but recall that referrenda are synchronous decisions overwhelming framed in terms of pass/fail. Historical experience of low turnout for largely synchronous, tedious decisions in which most participant input does not matter does not imply low turnout for asynchronous, intuitive decisions in which each participant has an incremental impact on the outcome. It is easier to decentralize allocative decisions than legislative ones; consider our historical experience with markets.

> The general population lacks the expertise to make allocative decisions.

Do they? Let us remove our rose-colored glasses and acknowledge that elected representatives rarely budget in our best interest -- control over allocations is an invaluable bargaining chip and a vector for opaque political processes leading to suboptimal outcomes. Any risk of suboptimal allocations by the population should be weighed against current allocation failures caused by giving control to a small group of representatives.

Further, no one knows the future and so the ability to flexibly adjust budgets is more important than "correctness" at any fixed moment in time. The mechanisms suggested here allow for constant, asynchronous updating of budgets, making it possible to course-correct should it become clear that errors have been made. We can also allow for liquid democracy-style delegation of influence, so that individuals with specific expertise can accumulate more influence over decisions in their purview.

Finally, we must remember that our memory and experience of budgeting is inextricable from the manner in which budgeting has historically occurred: as tedious, cognitively burdensome processes culminating in single contentious pass/fail vote. Changing the mechanism changes and relocates the cognitive burden, meaning that something that once required "expertise" (read: tedium) can become widely acessible.

> Direct democracy is dangerous! There is too much of a risk of rash mob behavior, and defunding of critical works.

This is a fair and important critique. Republican government developed out of democratic in large part due to a recognition of the temperamentality of direct democracy. Majority rule can easily tend to mob rule, with threat of violence. But there are ways to construct the system to blunt the effects of emotion and temperamentality. One possibility is to limit the extent to which allocations may change over any period of time, which would slow the effect of mood swings until the population has regained its composure. The ability to incorporate this type of ["regularization"](https://en.wikipedia.org/wiki/Regularization_(mathematics)) directly into the process (versus being limited to binary approval of the output of a separate, unspecified process) is a significant advantage of these more specialized techniques.

> Your computational methods seem overly complicated and hard to use.

Not necessarily; it is not true that a complicated *process* must have a complicated *interface*. Quite the opposite: by performing more information processing with a computer, you are able to create *simpler* experiences for the participants. The nature of the processing can be taught in school, much like we teach civics and government to teenagers today. These are all just differences of quality, not of kind. Further, the techniques proposed here are proven and reliable, intuitive, and interpretable by laypersons.

# Epilogue: Zeno and the Archery of Artifice

Zeno of Elea was a pre-Socratic Greek philosopher who lived in the fifth century BCE, known for his paradoxes involving objects in motion and his early explorations of infinity. His most famous paradox is that of an arrow in flight: as the arrow moves towards its target, it takes some non-zero amount of time to traverse *halfway* to the destination. As one can make infinite half-motions towards a destination (each half-motion is half the distance of the one before), and each motion takes non-zero time, paradoxically it seems that it will take the arrow an infinite amount of time to hit the target. Of course, Zeno didn't know about calculus.

They key image is that of the sequence of half-motions, each traversing half of the remaining distance: the first half-motion is the largest; the second half-motion a quarter of the total distance, and so on. As we add more half-motions, each becomes absolutely smaller until the motions diminish to zero in the infinite limit and the distance is traversed.

Return to Brand's Pace Layering. For sake of argument, let's say that each layer explains *half* of the problem of understanding the world, a type of "half motion" of responsibility. Each additional layer explains *half of the remaining half*. If we assume that each layer encompasses a constant amount of *work* (`size * complexity`), then we can think of an infinite sequence of increasingly complex layers with progressively smaller amounts of "discretion".

This provides a framework for thinking coordinating processes more broadly: we take the *easier half* of the problem, and develop the *simplest and most efficient mechanism* which addresses that half. We then take the easier half of the remaining half, which by definition is *more complex* than the first half which we've already solved, and do the same thing again. The more complex mechanisms have higher risk of failure, but simultaneously are responsible for smaller fractions of the "total discretion", and so the overall risk remains tolerably low at every layer. The entirety of the system, then, is the *integration* of this long tail of subsystems, with a total risk no higher than the risk represented at every layer. More specialized processes creates a less risky system, then, than fewer general processes, for the same amount of functinality.

Consider how our current paradigm is over-reliant on a single system (parliamentary procedure) and is therefore at a higher risk for failure. Contrast this with the *previous* paradigm, which was over-reliant on a single ur-system (hereditary autocracy) which was at an even *higher* risk for failure. As we have seen once, and as we will see again, by separating a coordinating process into parts, specializing the parts, and re-integretating them together will allow us to reduce the risk of failure while maintaining or even improving functionality.
