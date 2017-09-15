---
layout: post
title: "Time and Authority"
comments: true
categories: blog
tags:
- voting
- consensus
- blockchain

---

I.

Some ideas have staying power. For whatever reason, ideas about good and evil,
right conduct, and so on have been around for millenia. Other ideas are newer.
Notions of individual freedom, equal rights, have been around for centuries,
or merely decades. Ideas come in and out of fashion; some last longer than
others.

On the other hand, we have people who are constantly changing their mind.
Especially in politics, where we are often frustrated by individuals
flip-flopping on issues to suit their immediate needs.

Is there something to be said for an idea that lasts?

II.

Since the end of World War II and the ushering in of the postmodern age,
it has become the norm to challenge and disassemble the authorities of
yesteryear. An idea which has been passed on for hundreds of years is
of the same value as one freshly conceived that morning; it is our
intellect, and nothing else, that arbitrates between them.

The discovery of deconstruction was a cultural breakthrough, but has
left us both highly sensitive to dialectical tensions and ill-equipped
to resolve them. As an example, consider the recent headlines
concerning trigger warnings on college campuses.

It is our position that the postmodern paradigm has been a gift and a curse,
and that we ultimately must find a way to balance both flexiblity of thought
and the value of tradition. The ideal balance is one which allows someone
to change their mind, while at the same time giving preference to those
who hang on to their beliefs.

Further, we would like put this balance into practice, specifically as
an exension of the theory of preference graphs developed in
[this thesis](http://nbviewer.jupyter.org/github/kronosapiens/thesis/blob/master/tex/thesis.pdf).

We will describe this mechanic, and identify a number of unanticipated benefits.

III.

To review the language of preference graphs, we have individuals $$e$$ with
preferences, expressed as $$(b,a)$$ when $$e$$ prefers $$a$$ over $$b$$. We can
imagine $$(b,a)$$ as an arrow, or edge, pointing from $$b$$ to $$a$$.

Thusfar when aggregating preferences, all preferences are given a weight of 1.
Now we introduce a new dimension to preferences: the *authority* of a
preference, defined as some function of the time since $$e$$ first expressed the
preference $$(b,a)$$. If $$p$$ is an arbitrary preference and $$t$$ is the time
(in seconds) since that preference was expressed, then the authority of
$$p$$ can be defined as:

$$
auth(p) \triangleq f(t)
$$

The authority function is intentionally general; any function will do, and
the choice of function will determine the way that the authority of a
preference increases (or potentially decreases) over time. That said, we
feel that the logarithm, $$log(t)$$, is a reasonable place to start.

When performing aggregations and analyses of group preferences, the units
will become units of authority, rather than simple counts.

As we will see, incorporating the time dimension will have some interesting
consequences.

IV.

What happens when we incorporate time? Assuming a monotonically-increasing
authority function, we can predict the following:

1. Individuals are incentivized to register their preferences as early as
possible. Assume that individuals would like their views to have the
maximum impact on the group. In the context of an online application or
service, this creates an valuable incentive to adopt the product as
early as possible.

2. Individuals will change their preferences less frequently. If an individual
changes their preference, the authority of that preference resets. If an
individual then decided that their original preference was the right one,
the preference resets again, and the accumulated authority of thier initial
preference is lost. There is an incentive to get it right the first time.

3. Individuals will change their preference when their views truly change.
There is no benefit to holding on to views one no longer agrees with:
if an individual truly feels differently about an issue, then updating
their preference will achieve the desired directional affect.

In summary, the addition of a time dimension to a preference-aggregation
platform creates powerful incentives to both adopt the platform and to
behave responsibly once on the platform. It is especially worth noting that
the additional computational complexity associated with incorporating the
time dimension is small: $O(n)$.

