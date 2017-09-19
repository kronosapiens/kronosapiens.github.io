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

Living together, humans exchange ideas.

Some of those ideas have staying power. Views concerning
good and evil and right conduct have been around for millenia.
Notions of individual freedom and equal rights have been around for centuries.
Concepts of gender and racial equality, decades.

Ideas come in and out of fashion; some last longer than
others. Not all of them are good, and sometimes we have to let them go.

Still, we expect people to stick to their beliefs: especially our leaders and
people we depend on. It is destructive when leaders renege on
important issues to suit their immediate needs.

At the same time, we don't want people to feel like they must perform
their beliefs under external pressure. As we change, our attitudes change,
and our expression of those attitudes should be free to change with them.

We want freedom. We want stability. How do we balance self and society?
If something is good, will it last? If something lasts, is it good?

II.

Since the end of World War II and the ushering in of the postmodern age,
it has become the norm to challenge and disassemble the authorities of
yesteryear. An idea which has been passed on for hundreds of years is
of the same value as one freshly conceived that morning; it is our
intellect, and nothing else, that arbitrates between them.

The deconstruction was a cultural breakthrough, but has
left us more sensitive to dialectical tensions yet [poorly-equipped](https://www.theatlantic.com/politics/archive/2016/05/the-peril-of-writing-a-provocative-email-at-yale/484418/)
to resolve them.

Ultimately, the postmodern vision has been a gift and a curse. We cannot hold
ourselves right *a priori* and we must ultimately find a way to balance
flexiblity of thought with a valuing of tradition. The ideal balance is one
that allows an individual to change their mind, while at the same time
creating some incentive to stick to one's beliefs. We must find a way to
embrace change without fearing destruction.

It is easy to speak in generalities; it is hard to put things into action.
In an attempt at the latter, we will bring this balance into practice,
as a demonstration and extension of [this theory](http://nbviewer.jupyter.org/github/kronosapiens/thesis/blob/master/tex/thesis.pdf) of preference graphs.

III.

To review the language of preference graphs, we an individual $$e$$, who has
preferences written as $$(b,a)$$ when $$e$$ prefers $$a$$ over $$b$$. We can
imagine $$(b,a)$$ as a preference, or arrow, from from $$b$$ to $$a$$.

Thusfar when aggregating preferences, all preferences are given a weight of 1.
Now we introduce a new dimension to preferences: the *authority* of a
preference, a variable weight defined as some function of the time $$t$$ since
$$e$$ first expressed the preference $$p = (b,a)$$.If $$p$$ is an arbitrary
preference and $$t_p$$ is the time since that preference was first expressed,
then the authority of $$p$$ can be defined as:

$$
auth(p) \triangleq f(t_p)
$$

The authority function is intentionally general; any function will do, and
the choice of function will shape our intereptation of the "authority."
Using a monotonically-increasing function, like the logarithm, creates an
authority curve which is intuitive and useful.

IV.

What happens when we incorporate time into applications of preference graphs?
Assuming a monotonically-increasing authority function and rational,
self-interested participants, we might expect the following.

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
time dimension is small: $$O(n)$$. That so many positive effects emerge
from a simple computation is highly suggestive.

