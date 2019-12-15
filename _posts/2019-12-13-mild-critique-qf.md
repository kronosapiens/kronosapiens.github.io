---
layout: post
title: "A Mild Critique of Quadratic Funding"
comments: true
categories: blog
tags:

- voting
- mathematics
- economics
- social-choice

---

This essay is meant as a mild and constructive engagement with one part of the constellation of ideas being advanced under the aegis of [RadicalxChange](https://radicalxchange.org/) (pronounced "radical exchange"), specifically the concept of quadratic funding, and it's claim to "optimality". Let's review the argument and then assess the strength of that claim. This will involve a few equations but I'll narrate the whole thing so it shouldn't be too hard to follow (or just skip to the critique).

## A Review

From the "Liberal Radicalism" [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3243656), we have the following notion of **social welfare:**

$$
\sum_p (\sum_i V_i^p(F^p)) - F^p
$$

Here, $$i$$ is a citizen in a society while $$p$$ is a public good in that society. $$c_i^p$$ (which shows up later) is the amount of money that citizen $$i$$ gives to good $$p$$, whle $$F^p$$ is the *total amount* of funding that good $$p$$ receives. $$V_i^p(F^p)$$ is the "currency-equivalent utility" that citizen $$i$$ receives if good $$p$$ is funded at level $$F^p$$. Pay extra special attention to the term **currency-equivalent utility** because it is the hinge of the critique. With these definitions, the equation is straightforward: *social welfare is the sum of all individual utilities across all public goods, less the total cost of those goods.* Pretty reasonable.

Now, the authors (Buterin, Hitzig, and Weyl) use this equation to show why two existing systems, namely capitalism and one-person-one-vote democracy, lead to suboptimal allocations, while their quadratic methods lead to optimal allocations. An important concept in their argument is the *first derivative of the individual utility function*, $$V_i^{p\prime}$$. This tells us how much value citizen $$i$$ gets from the *next dollar* which funds the good $$p$$, i.e. the slope of the curve.

For an optimal allocation, we would expect that the first derivative of the *total utility* for a given good (summed across all citizens) would be equal to 1, meaning that *society as a whole* has reached the point where giving more funding to the good would create less value than the funding itself, i.e. $$V^{p\prime}(F^p) = 1$$. At that point, funding should be placed elsewhere.

Now, under **capitalism** (the system where all contributions to public goods are made by citizens *in isolation*), otherwise known as $$F^p = \sum_i c_i^p$$, citizen $$i$$ will contribute to a good up until the point where their *individual increase in utility is worth what they contribute*, i.e. where $$V_i^{p\prime}(F^p) = 1$$. The problem here is that there is a lot of utility that ends up being "left on the table" -- even if an extra $1 of funding can create $.5 of utility for three people (i.e. $1.5 of utility for society), no one will provide that funding since from the perspective of the individual, they are giving $1 and getting only $.5 back in value. Formally, this looks like $$V^{p\prime}(F^p) > 1$$, i.e. putting in more money will create more utility *for society*, but no one does it. Sad.

Under **one-person-one-vote (1p1v)** (the system where citizens vote on alloctions), otherwise known as $$F^p = N \cdot \text{Median}_i V_i^{p\prime}(F^p)$$, the problem is different. Here, the issue is that since the utility is determined by a majority vote (i.e. by the "median voter"), the allocation will be suboptimal to the degree to which the median voter differs from the *average* or *mean* voter. Note the appearance of the term *mean* here, because it sets the stage for (drumroll please) the quadratic methods.

Recall that the median is a measure of centrality which *ignores* degree of intensity, while the mean is exactly the measure of centrality which incorporates it, i.e. the mean minimizes the *square error* of itself to all the data points (while the median minimizes the *absolute error*).

Enter **quadratic funding** (the system in which the total contribution is the *sum of the roots* of the individual contributions), otherwise known as $$F^p = (\sum_i \sqrt{c_i^p})^2$$. Unlike capitalism, in which individuals contribute up until *their utility* matches their contribution, quadratic funding allows people to  contribute until the *total utility* matches their contribution. We'll look at the derivation because it'll be instructive. Starting with the individual's utility function, $$V_i^p(F^p) - c_i^p$$, we maximize by taking the derivative and setting to zero (involving several applications of the chain rule), which gives us:

$$
V_i^{p\prime}(F^p) = \frac{\sqrt{c_i^p}}{\sum_j \sqrt{c_j^p}} \leq 1
$$

This is an odd looking fraction, but note that it is less than (or equal to) 1, *and equals one when you sum across all citizens*. That is the voilà moment for quadratic funding:

$$
V^{p\prime}(F^p) = \sum_i(\frac{\sqrt{c_i^p}}{\sum_j \sqrt{c_j^p}}) = 1
$$

While capitalism provides funding up until *individual utility* matches the increased funding, quadratic funding provides funding up until the *collective utility* matches the increased  funding, which is *optimal*. This is a great result and a source of legitimate excitement.

## The Critique

But (and finally, we reach the critique), let us recall the key assumption of the model: individual (subjective) utility, $$V_i^p$$, is assumed to be both *known* and *dollar-valued*, being inferred per-citizen from the amounts contributed. This is a problematic assumption, as it equates something which is fundamentally *subjective* (a private feeling) with something which is fundamentally *objective* (a real number). The collective (subjective) utility is inferred from *summing up* these numbers, equating them with feelings. This seems... peculiar.

Economists have [long wrestled](https://en.wikipedia.org/wiki/Social_choice_theory#Interpersonal_utility_comparison) with this problem. In his *Social Choice and Individual Values*, economist icon Ken Arrow famously argued that since choices are defined by relative preferences ("apple vs orange"), that "there is no quantitative meaning of utility for an individual", and thus "interpersonal comparison [and thus summation] of utilities [have] no meaning", since something which is not a number can be difficult to compare (i.e. it is easy to see that 6 is less than 7, but not easy to see that red is less than blue).

One might turn around and say that quadratic funding sidesteps the issue by asking citizens to make *absolute* decisions ("give $25 to the parks department"), rather than *relative* decisions ("plant apple trees, not orange trees, in the park"). In this case, citizens are *telling* us their currency-valued utility -- $25, problem solved (known as "revealed preference"). But all that *really* tells us is that the citizen prefers giving the parks department $25 dollars to keeping it for themselves -- and tells us nothing about the fuzzy questions of psychic insensities. Further, if we assume that everyone has the same capacity for inner experience (a question with deep ties to identity, our other bugbear), but not everyone has the same amount of money to give, then we paint ourselves into another corner: do those with more wealth, who give more, experience greater utility than those who give less? If I make $100 a day while you make $10, is my experience of satisfaction ten times yours? [Probably not](https://www.nature.com/articles/s41562-017-0277-0).

You might retort that this is excessive pedantism. Our lived experience is full of assessments of the subjective experiences of others, and -- although they are based on evolved heuristics, not mathematical proofs -- it seems to work well. In his *[Gaming the Vote](https://www.amazon.com/Gaming-Vote-Elections-Arent-About/dp/0809048922)* (chapter 15), William Poundstone considers this debate and makes the point that "these intellectual positions... entailed a pose of fashionable agnosticism over matters previously held to be common sense." Many economists agree, with Amartya Sen giving the famous example of Nero's sacking of Rome: it is almost universally seen as self-evident that the negative utility of all the Romans who suffered in that blaze outweigh the positive utility that Nero experienced in the sacking, and so the sacking was "bad". Clearly, utilitarian arguments have a place. To conclude that "we cannot model or compare subjective experience" seems like the easy way out, and evokes the behaviorist posture which constrained psychologists up until the "cognitive revolution" of the mid-20th century. Even if it's not perfect, putting numbers to feelings seems "good enough" and gives us something to work with -- so what's the problem?

The problem is ultimately one of signal and noise, of [signifier and signified](/blog/2016/04/16/the-problem-of-information.html), and of the [risks of optimizing for proxies](https://www.lesswrong.com/posts/uL74oQv5PsnotGzt7). Briefly, since we are unable to accurately represent (and thus measure) the thing we really care about (subjective utility), we instead measure a *proxy* (funding amounts). Unfortunately, there is a **fundamentally unknowable** gap between these two measurements, and so *we cannot know* how good our mechanisms really are with regard to our true goal of maximizing welfare -- not only is there some error, but we cannot know what that error is.

In casual settings this is a non-issue, since this "proxy gap" will be too small to be consequential. However, the more *pressure* that is placed on the system (i.e. the more resources are at stake, the more people whose interests are affected), the greater the incentive to exploit the system (a phenomena known as [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law)), and a key vector of exploitation is the gap between the desired measurement and the true measurement (for a well-known example, consider the test-prep industry which coaches students taking high-stakes standardized tests). The more resources which are deployed using quadratic funding, the more pressure is placed on the system, and so the more the gap between "true utility" and "funding amounts" (the proxy) will be exploited -- leading to unexpected failures because the gap *cannot be modeled by the system*. Unlike other kinds of error, which can be modeled and thus handled by the system, this kind of error necessarily lies *outside the system* and is thus quite pernicious, as the consequences invariably come suddenly and by surprise.

All of this is not to say that quadratic funding is a bad idea -- quite the opposite, in fact, as *in general* it will probably work well (see [this experiment](https://vitalik.ca/general/2019/10/24/gitcoin.html)) and represents an important step forward. Further, these basic measurement problems do not affect quadratic funding alone -- any mechanism which must represent and measure a subjective quality falls into this trap -- which includes basically all voting, rating, and reputation systems.

The point is more that one of the banner claims -- optimality -- is overstated. Ultimately, quadratic funding is "optimal" in the same way that blue is the "optimal" color for the Blue Man Group -- it follows from the definition, rather than from some essential truth. Quadratic funding does not *really* maximize utility -- it maximizes some other amorphous "utility-like" thing. Which, again, is fine... until it's not.

*Thanks to Auryn Macmillan for feedback and for making sure I'm not an idiot.*
