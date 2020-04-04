---
layout: post
title: "A Review of 'Gaming the Vote'"
comments: true
categories: blog
tags:

- voting
- mathematics
- economics
- social-choice

---

## I. Introduction

Some months ago I read William Poundstone's _[Gaming the Vote](https://www.amazon.com/Gaming-Vote-Elections-Arent-About/dp/0809048922)_, a comprehensive survey of the history and attributes of various alternative voting systems -- a topic of longstanding [personal interest]({{site.baseurl}}/blog/2017/02/06/thesis.html).

The villain of Poundstone's story is the _plurality vote_, a fair-seeming but perniciously flawed way of choosing leaders, and Poundstone devotes fully the first third of the book to a survey of the method's myriad historical vailures. The remaining two thirds are a survey of the alternatives, and a discussion of their own (inevitable) achille's heels. Poundstone considers, in turn, the classic methods of Borda and Condorcet, the more recent innovations of Instant Runoff Voting and Approval Voting, and concludes with a bullish assessment of Score Voting as the "least worst" option. Along the way, we meet (among others) the idealistic Marquise de Condorcet, the obsessive-creative Charles Dodgson (Lewis Carroll!), and of course, Kenneth Arrow, our _axis mundi_.

Let's now review the various electoral sytems (as we will see, each has a fatal flaw), and then hone in on a number of points where I think Poundstone's argument can be extended or corrected.

## II. The Voting Systems

### Plurality Voting

- **What:** Voters submit single votes; the candidate with the most votes is the winner.

- **But:** Susceptible to vote-splitting, leading to the election of minority candidates (the "spoiler effect").

Plurality voting (also known as "first-past-the-post") is an electorical system in which voters cast a single vote for their preferred candidate, out of an arbitrary pool of candidates. The votes are summed up, and the candidate with the most votes is elected.

While simple and fair on its face, the critical flaw of the plurality vote is that when there are more than two candidates, often the larger group (the "majority bloc") will find themselves choosing between two candidates, while the smaller group (the "minority bloc") will have only one. In this case, the majority bloc, which should be the one to choose the candidate, will end up losing to the minority bloc. In concrete terms, if the majority bloc is 60% of the vote with two equally-popular candidates (Alice and Bob), then the minority candidate (Charlie) will win with 40% of the vote, while the two majority candidates will each take 30% of the vote and lose the election. Note that no candidate won a majority of the votes, a reasonable standard for legitimacy.

In real-world elections, a more common occurrence is that the majority and minority blocs are more closely matched (say 52% vs 48%), and a fringe candidate comes in to pull \~5% of the vote from the majority candidate, handing the victory to the minority bloc -- the "spoiler effect" phenomenon which famously sent George Bush to the White House in the 2000 United States presidential election. In addition, Poundstone discusses the recent practice (as of the last few decades) in which minority blocs explictly encourage this phenomena by descreetly funding fringe candidates to challenge their majority opponent.

From a theoretical perspective, the key limitation of the plurality vote is that a voter is unable to provide sufficient _information_ about their preferences. In many cases, voters who vote for a fringe candidate would still prefer the majority candidate to beat the minority candidate, but this type of "second choice" information is unavailable to the election algorithm. As we will see, the common theme of every other system Poundstone describes is their attempt to incorporate this additional information (with variously mixed results).

### The Borda Count

- **What:** Voters submit ranked lists, with candidates receiving more or less votes depending on their position. The candidate with the most votes is the winner.

- **But:** Susceptible to tactical voting ("burying"), which can lead to the election of unintended candidates.

The Borda count is a method which attempts to avoid the flaw of plurality voting by allowing voters to convey their preferences not only for their first choice, but for all the candidates, by submitting a ranked list. Known appropriately as a "ranked choice" method, the Borda count assigns a numeric score to every candidate based on their position in the list (i.e. for the list "Alice > Bob > Charlie", Alice gets two points, Bob one, and Charlie zero).

The Borda count thus avoids the spoiler effect by allowing multiple candidates to "share" the support of their bloc, in such a way that one of the majority candidates should prevail over the minority. To return to our earlier example, say that Alice and Bob are equally-popular candidates for the 60% majority bloc, while Charlie is the sole candidate for the 40% minority bloc. With the Borda count, each of Alice and Bob will receive a score of 30 * 2 + 30 * 1 = 90, while Charlie will recieve a score of 40 * 2 = 80. If we assume some small amount of randomness such that an exact tie is avoided, one of either Alice or Bob will win.

However, the Borda count's flaw is that by assigning scores to individual candidates _as a function of the number of total candidates_, it makes it possible to create "artificial distance" between candidates (i.e. to create a distance of "two" between Alice and Bob, simply by the presence of Charlie). This ability to create distance between candidates leads to the phenomenon of "burying", a type of strategic vote where strong candidates are ranked "artificially" low.

In extreme cases this can lead to unexpected candidates being elected. Consider an example of Alice, Bob, and Charlie, where Alice is the majority bloc candidate (60%), Bob is the minority bloc candidate (40%), and Charlie is a moderate. With plurality voting, Alice would easily win. But under the Borda count, the minority bloc can vote strategically to put Charlie in office: if the majority bloc ranks Alice, Charlie, and Bob, then the minority bloc can vote tactically, falsely putting Charlie as their top candidate (and Alice last). This would lead to a Charlie victory with a score of 40 * 2 + 60 * 1 = 140 vs. Alice's score of 60 * 2 = 120.

Theoretically, the problem is rooted in the ability to create absolute (numeric) distance between a pair of candidates, compared to simply relative distance, as a function of something _other than the pair of candidates themselves_ (in this case, the number of candidates total). The number of candidates in the election should not be able to affect the relative preferences of pairs of candidates (where the majority prefers Alice to Charlie), but in the Borda count it does. Another way to frame this limitation is that the Borda count provides no way to express non-uniform "distances" between the candidates -- the psychic "space" between Alice and Bob is assumed to be just as large as that between Bob and Charlie. This can be understood as a type of information-theoretic noise caused by the measurement not quite fitting the thing being measured (this will be a recurring theme).

### The Condorect Winner

- **What:** Voters submit ranked lists, which are translated into pairwise contests. The candidate which defeats every other candidate, pairwise, is the winner.

- **But:** No guarantee of transitivity, i.e. a winner might not exist.

The Condorcet winner is the candidate who would beat every other in a two-way contest. This method attempts to both avoid the spoiler effect and the problems of the Borda count by allowing voters to submit multiple preferences _without_ creating artificial distances.

To return to our opening example, in an election where Alice and Bob are majority candidates and Charlie is the minority candidate, both Alice and Bob will beat Charlie (60/40), and then Alice and Bob will themselves face off in what will amount to a 50/50 split (with some small randomness breaking the tie). This method solves the problems of plurality voting by allowing for the incorporation of the information that 60% of the people would prefer Alice and Bob to beat Charlie, while _avoiding_ the problems of the Borda count by never _casting relative preference to absolute_ (i.e. if I prefer Alice to Bob, ranking Bob _last_ doesn't make Alice beat him by "more" as long as he is ranked after Alice).

The problem with this method, however, is that the Condorcet winner _may not exist_. Consider a scenario with three equal-sized blocs (and three candidates), we may find ourselves in a situation where Alice beats Bob by 2:1 (i.e. bloc A and C both prefer Alice to Bob), but Bob beats Charlie 2:1 (i.e. bloc A and B both prefer Bob to Charlie), but Charlie beats Alice by 2:1 (because bloc B and C both prefer Charlie to Alice). This can be written as:

- Bloc A: Alice > Bob > Charlie
- Bloc B: Bob > Charlie > Alice
- Bloc C: Charlie > Alice > Bob

This creates a rock-paper-scissors situation known as a "cycle" (draw it as a graph -- or scroll down -- to see why), and there is no winner. Obviously it is problematic if there is "no winner" in an election, and so this is seen as a flaw in the method. Defenders of Condorcet methods say that cycles are rare in practice (it requires a particular "arrangement" of candidates and voters), and so the concern is over-blown (compared to the type of failures which can occur in the Borda count and plurality votes, which are much more common).

From a theoretical perspective, the problem here not the lack of information, but rather that the algorithm cannot "see" all the information that is there. As we will learn later, there are other techniques which can see this information and break cycles in a fair way.

### Instant Runoff Voting

- **What:** Voters submit ranked lists. An iterative algorithm re-allocates votes until a clear (majority) winner emerges.

- **But:** The algorithm is "non-monotonic": giving a candidates more votes can cause them to lose. Also, popular second-choice candidates may be eliminated too early.

Instant Runoff Voting (IRV) is an interesting beast. Unlike the other methods, which run in constant time, IRV is iterative: it runs in a `while` loop, rearranging votes until one candidate has a majority of first-place votes. Like the Borda count and Condorcet winner, IRV attempts to make second-choice votes meaningful by successively eliminating last-place candidates, reallocating votes to second (or third or fourth!) choices in the event that an eliminated candidate was a voter's first choice. Returning to our opening example, consider the case where Alice and Bob split the 60% majority bloc's vote down the middle (alternating as first and second choice on the ballots), while Charlie takes all of the 40% minority bloc's votes. In the first round of the IRV algorithm, either Alice or Bob will be eliminated (having the fewest votes, \~30%, versus Charlie's 40). Let's say that Bob is eliminated. Now, since every voter who ranked Bob first ranked Alice second, all of Bob's votes will now be transferred to Alice, giving her 60% of the vote and a majority victory.

IRV has proven to be popular in practice, gaining traction in governments and municipalities around the world, in part due to the intuitive nature of the algorithm making the process easy to understand. Among contemporary advocates for voting reform, IRV has become one of the most popular options (rivaling Score Voting). However, IRV is not without flaws. The essential problem with IRV is that it is, in mathematical speak, "non-monotonic". A "monotonically increasing" function is one which is always either staying the same or increasing, but never decreasing: for IRV, the "non-monotonicity" means that giving _more_ votes to a candidate can actually cause them to lose, a troubling phenomenon which does not appear in any of the other systems considered. Also, the nature of the IRV algorithm means that the most broadly popular candidate may still lose. To see why, consider the case where the population is split 50/50 for Alice and Bob, with Charlie being a universally-popular second choice. Charlie seems like the natural best choice, but because he receives no first-place votes, the IRV algorithm eliminates him in the first round, resulting in a deadlock between Alice and Bob -- exactly the situation we would hope IRV would avoid.

### Approval Voting

- **What:** Voters submit a binary approve/reject _per candidate_. Votes are tallied according to plurality rules.

- **But:** The ambiguous semantics of "approval" means that winner of the election can be hard to predict.

The Borda count, Condorcet winner, and Instant Runoff Voting all fall under the category of "ranked-choice voting" systems: they are all different algorithms which operate on the same _measurement_, that of a relative ranking of candidates. Approval voting (and its cousin, score voting) are fundamentally different animals, in that their primary representations are not relative, but absolute. As we will see, this approach will spare these methods from many of the flaws of their relative brethren, but introduces pernicious problems of its own.

Approval voting can be thought of as a generalization of plurality voting, but where instead of voting for one candidate, you can vote for _as many as you like_. This prevents the spoiler effect by allowing second-choice candidates to receive votes alongside the first-choice candidates. This also removes the benefits of voting strategically, since the sincere vote is the optimal vote. Recall Alice, Bob, and Charlie. With approval voting, both Alice _and_ Bob will receive \~60% of the vote, compared to Charlie's meager 40%. Some small randomness will ensure that one of Alice and Bob is elected, to the satisfaction of the majority bloc.

Unfortunately, the ambiguous semantics of "approval" (what is the standard by which someone is "approved"?) means that, contrary to expectations, mediocre candidates can prevail over strong candidates. Consider a situation where Alice is beloved by 60% of the population, Bob beloved by the other 40%, and Charlie seen as a bumbling but endearing candidate whom no-one takes seriously, but no one dispises. With approval voting, it is possible that more than 60% (potentially up to 100%) of the population will "approve" of Charlie, on the grounds that, from the perspective of each half of the population, Charlie isn't a _bad_ candidate. As a result, Charlie wins the election -- an unintended outcome. More fundamentally, depending on how voters interpret "approval", the same ranked-ordering of candidates can lead to different election outcomes -- a phenomenon known as "indeterminacy".

Observe that, under a Borda count, Alice would win the election, since a first-place vote from 60% of the population is worth more than a second-place vote from 100% of the population (2 * 60 > 1 * 100). With approval voting, the inability to represent the _underlying_ relative distinctions leads to the measurement error manifesting as indeterminacy. Said another way, by treating the candidates as unrelated in the model, the base concept of "approval" decoheres and loses definition as relativity inevitably re-inserts itself.

### Score Voting

- **What:** Voters submit a numeric score _per candidate_. Votes are tallied according to plurality rules.

- **But:** The ambiguous semantics of "scoring" means that winner of the election can be hard to predict.

On the surface, score voting arrives on the scene as the funnier and more handsome cousin of approval voting. Rather than precluding any expression of relative preference, score voting permits the assignment of real-valued scores to each candidate, allowing for _implicit_ relative preference. Further, the ability to use a fuller range allows voters to avoid the false "uniformity of differences" which hounds the Borda count.

Unfortunately, this merely kicks the can down the road -- it turns out that numerical scores vary as a function of the candidates just as much as binary "approvals". Consider a beloved Alice, a well-meaning Bob, and a chicanerous Charlie. A voter might give Alice a 1, Bob a .6 (indicating their positive sentiment), and Charlie a 0. Say Charlie is indicted for fraud and drops out of the race -- what happens to Bob's score? The voter wants Alice to win, and giving Bob a 0 maximizes those chances. So we see how Bob's score, real-valued as it is, decoheres just as much as "approval" does with binary votes. Fundamentally, the voter has no "score" for Bob, only a relative sentiment vis-a-vis Alice and Charlie. In line with our theme, we conclude that the use of real-valued scores is a mirage, providing an _illusion_ of information.

Apart from this, score voting is subject to the same quirks as approval voting, and so there is no need to recount them here. And of course, as with all systems described here, the existence of these types of failure conditions _in principle_ says little about the frequency with which they will be encountered _in practice_. All of these systems work well most of the time, which is good enough, _most of the time._


## III. Generalized Relativity

### The Confounding of Condorcet

Let us now take the ceremonial potshot at our bugbear, the Independence of Irrelevant Alternatives (IIA) -- the most frustrating of Arrow's criteria. Consider the example on page 225 of _Gaming the Vote_:

Three candidates (here, Clinton, Bush, and Perot) run in a ranked-choice election with a Condorcet winner. The first ballots arrive:

- Clinton > Bush > Perot (30 million)
- Bush > Perot > Clinton (30 million)
- Perot > Clinton > Bush (30 million)

This leads to the following graph:

![Condorcet 1](https://s3.amazonaws.com/kronosapiens.github.io/images/condorcet-1.jpg)

As we can see, we have a nightmarish cycle in which each candidate wins and loses by a landslide, and there is intuitively no winner. With this voting data, no system could declare a winner, as the information simply does not exist. Now, additional ballots arrive:

- Bush > Clinton > Perot (20 million)
- Clinton > Bush > Perot (15 million)

This leads to the following graph:

![Condorcet 2](https://s3.amazonaws.com/kronosapiens.github.io/images/condorcet-2.jpg)

Now we have sufficient information to declare a winner -- but who?

As Poundstone points out, the new votes favor Bush, and yet -- despite a folk moral arithmetic implying that a tie plus a victory equals a victory -- Clinton is the Condorcet winner. Yet Clinton's Condorcet victory hides the landslide victory that Bush holds over Perot -- much more decisive than Clinton's meager margin over either. It _feels_ to us that this one landslide means more than Clinton's two narrow victories. We spectators, with our "artist's eye" (to borrow a term from Paglia) can "see" the relevance of this background victory to the larger picture, but the simple "machine mind" of the Condorcet algorithm cannot.

Of course, not all is lost -- the information is there, clearly -- _we_ can see it. Condorcet cannot, but it turns out that Borda can. In this setting the Borda count would "see" Bush's victory -- with a count of 145 million compared to Clinton's 140. Of course, that the Borda count is "right" _in this case_ does not mean that it is better -- as we have discussed earlier, each algorithm can "see" only certain facets of the world -- and in this case, the Borda count is the machine that sees the right things.

There are more recent techniques, such as Power Ranking (the method famously underlying Google's PageRank), which mix the numerical aspect of the Borda count with the graphical approach of of the Condorcet winner to produce compelling results, and remains on the cutting edge of applied social choice with [numerous](https://blog.colony.io/introducing-budgetbox/) applications [under](https://sourcecred.io/) active [development](https://relevant.community/). As promised earlier, Power Ranking is a technique capable of breaking Condorcet cycles, "spinning the wheel" to leverage more of the available information.

There is no algorithm which can fully attain the "artist's eye", for the same reason that there is no way to fully express a feeling. However we can get closer, and insisting on representations which as closely as possible reflect their underlying world is the start. If all mental concepts are fundamentally relative, we should stop pretending that they are not, and include relativity explicitly (and thoughtfully) in our models -- before it sneaks in unnanounced. _All alternatives are relevant._ The two words are nearly anagrams, clearly there is a cosmic joke being played here.

### Signal and Noise

Continuing our theme, let's turn to another example in _Gaming the Vote_, the discussion of the infamous "Hot or Not" (chapter 14). Hot or Not, as Poundstone remembers, was (is?) a website in which people can upload photos of themselves, and have the good people of the internet submit judments as to the photo's attractiveness, which ultimately Poundstone holds up as an example of the efficacy of score voting. Quoting directly (Poundstone, 247):

> [The creators, Hong and Young] considered having visitors pick their favorite of two on-screen photos. A photo would win points for each time it was preferred over another, random photo. This would loosely simulate a Borda count. (In a true Borda count, a candidate wins a point every time a voter ranks her above a rival. No Hot or Not voter could rank all the millions of pictures on the site, of course. The aggregate effect of random visitors ranking random pairs would be similar.) However, when shown two photos that hapen to be of roughly equal attractiveness, "people will look at the pictures and not know," Hong said. "They have a harder time deciding."

> Hong and Young also considered a simple "hot" or "not" vote on a single picture. This would be an approval vote. There it was "average" Joes and Janes which slowed things down. People would have to ponder whether to click "hot" or "not". Range voting was faster. It seemed to require _less_ thought. "Sometimes people can't even express the number," Hong explained, "they just have a feeling and like having that bar: 'ah, it's kinda like here.'" They position the cursor where it feels right and click.

This is a valuable history which deserves closer scrutiny, through the analytical eye of information theory.

First, some definitions: note that a single pairwise preference ("A vs B") can be represented in one bit (`0` for A, `1` for B). So too can a binary "hot or not" (`0` for "not", `1` for "hot"). A real-value, on the other hand, requires more bits -- for argument's sake, let's say 3 bits for an 8-point scale (`000` gives a 0, `111` a 7, and the rest in-between). The axioms of information theory tell us that a digital "bit" can contain _up to one_ "bit" of information (the relationship between the digital bit and the information bit being governed by the mathematics of entropy -- in the classic example, the outcome of a fair coin is exactly one bit of information, while the outcome of a loaded coin is always a little bit less).

Here, we see that score voting yields 3 bits of data, while a binary "hot or not" vote yields 1. Yet, bizarrely, it is easier for users to provide more data rather than less -- suspicious. While we cannot prove which measure yields more information (as this requires access to the ineffable truth, which we lack), this juxtaposition should make us wonder how many bits of information we're really getting in those 3 bits of real-valued scores -- likely, it is less than the (up to) 1 bit we get from the binary "hot or not".

Historical experience supports my argument. Poundstone mentions at the beginning of the chapter that, among others, YouTube uses 5-point scores for their videos. However, as discussed (in some of my work) [here](https://colony.io/budgetbox.pdf), YouTube (along with Netflix) have since dropped the 5-point system in favor of a binary like/dislike, on the grounds that the 5-point scale ultimately provided very little _signal_ above and beyond what was gleaned from a like/dislike, and thus introduced mostly noise.

That it is "easier" for users to provide 3 bits tells us little about the quality of the measurement -- it is the easiest thing of all to submit a random number, containing no information at all. Is not the amount of data, but the ratio of data to information, that we should care about. It is difficult decision processes that produce information-rich results.

<!-- And what of the case of the pairwise vote? Like the binary "hot or not", a pairwise vote is 1 bit, but note that now that bit is put up against not 3 bits, but 6, since we can generate the pairwise bit indirectly by comparing two real-valued 3-bit scores (if A's score is greater than B's, A is hotter). Yet the situation is not quite comparable, because the same score can be used multiple times to generate pairwise outcomes, and the number of pairs grows quadratically with the number of candidates -- for example, 10 people gives us 45 pairs. In the pairwise setting, you may need _more_ data, not less, to get results (45 bits of 1-bit pairwise preferences, vs 30 bits of 3-bit real-valued scores). Yet, from those 30 bits of real-valued scores, we can "infer" 45 bits of pairwise preference. What does this tell us about the information content of these various measures and techniques? Are the "inferred" 45 bits noisier than the "authentic" 45, if users are asked directly? Intuitively, it seems that if someone cannot tell you which of two individuals is hotter, then asking them to submit separate ("easy") scores and then using those scores to infer a relative preference could hardly give an information-rich result. I will suggest (but again, cannot prove) that real-valued scores are noisier measures which provide a false sense of confidence when compared to their more data-frugal counterparts. -->

## IV. Conclusion

The foundation of science is the assumed validity of independent repetition -- the idea that things which occur in the future are like things which occurred in the past, and that the things that we observe occur somewhat independently of one-another. This allows us to, for instance, re-run experiments, test theories, and to develop re-usable mathematical models of the world. Unfortunately, this assumption is, at base, incorrect. Historians know that, while we conceptualize history as a series of interconnected-but-separate episodes, in which the past contains clues about the future, the deeper truth is that history is one, single event, in which every moment is intimately and inextricably wound up with every other, and no differentiation can occur. This reality is more felt in some cases than others. The natural sciences, for one, can often get away with strong assumptions of independence (protons behave largely the same in 21st century California is they did in 10th century China). In art history, this is less true -- it is virtually impossible to understand the behavior of English painters in the 19th century without understanding the Italian sculptors of the 15th. The social sciences (and by extension, voting systems) sit, somewhat frustratingly, in the middle.

In many cases, assumptions of independence are necessary to make problems tractable. Fortunately, this is not the case here. There is room in the field of electoral systems and social choice to incorporate notions of relativity alongside notions of psychic intensity, and to develop algorithms which leverage the information encoded in both. Doing so will allow our mechanisms to sit closer to the "reality" of our experience and thus yield more consistently legitimate outputs -- a worthy aim in the quixotic quest for better tools of freedom.
