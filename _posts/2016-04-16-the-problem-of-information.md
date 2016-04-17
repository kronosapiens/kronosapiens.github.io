---
layout: post
title: "The Problem of Information"
comments: true
categories: blog
tags:
- information-theory
- machine-learning

---

#### 1

The Data Processing Inequality is one of the first results in information theory. It goes as follows: No transformation of measurements of the world can increase the amount of information available about that world. In formal language, it goes like this:

Given a first-order Markov chain

$$
X \rightarrow Y \rightarrow \hat{X}
$$

such that $$\hat{X}$$ depends only on $$Y$$, which depends only on $$X$$, then

$$
I(\hat{X};X) \leq I(Y;X)
$$

The measure $$I(a,b)$$ is known as the [mutual information](https://en.wikipedia.org/wiki/Mutual_information), a measure of how much information one variable gives us about another.

What this says is that the information $$\hat{X}$$ tells us about $$X$$ cannot be more than the information we already had from $$Y$$. In other words, that **processing** data adds no new information.

#### 2

Let's consider the problem of learning from data. Let's put it in the framework:

$$
\text{the world} \rightarrow \text{some measurements} \rightarrow \hat{\text{your analysis}}
$$

which implies

$$
I(\hat{\text{your analysis}};\text{the world}) \leq I(\text{some measurements};\text{the world})
$$

In other words, analysis doesn't tell you anything new. What it **does** do, though, is make the information you already have more easily digestible. It puts it in forms you can work with. Think averages and odds.

#### 3

If our goal is to understand the world, then it would seem as though we have two opportunities for growth.

First, in our measurements. The world is of infinite dimension, and any measurement is a finite reflection. Measurements are choices, and the dimensions along which we choose to measure will place the upper bound on our usable knowledge.

Second, in our analysis. Given a finite set of measurements, $$Y$$, our goal is to transform this into a different representation that expresses the information necessary to a given task, with "expressiveness" itself given by some measure. If that task is prediction or classification (fundamental and profound endeavors), then the measure will almost certainly be either likelihood of the analysis or the smallness of the error. But there can be other tasks and other measures of expression.

Which, at this time, is our limiting factor? Are we limited by our analysis, unable to make sense of what we know? Or are we limited by our measurements, trying to navigate with skewed vision?

Do you know?

#### 4

**Proof:**

$$
I(\hat{X};X)
$$

Definition of mutual information:

$$
= H(X) - H(X|\hat{X})
$$

Conditining reduces entropy:

$$
\leq H(X) - H(X|\hat{X}, Y)
$$

By Markov property:

$$
= H(X) - H(X|Y)
$$

Voila:

$$
= I(X,Y)
$$