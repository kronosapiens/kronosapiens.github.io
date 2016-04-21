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

The Data Processing Inequality is one of the first results in information theory.

It can be stated as follows:

*No transformation of measurements of the world can increase the amount of information available about that world.*

In formal language, it goes like this:

Given a first-order Markov chain

$$
X \rightarrow Y \rightarrow \hat{X}
$$

such that $$\hat{X}$$ depends only on $$Y$$, which depends only on $$X$$, then

$$
I(\hat{X};X) \leq I(Y;X)
$$

The measure $$I(A,B)$$ is known as the [mutual information](https://en.wikipedia.org/wiki/Mutual_information), a measure of how much information one variable gives us about another.

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

In other words, analysis doesn't tell you anything new. What it **does** do, though, is make the information you already have more easily digestible. It puts it in forms you can work with. Think averages and odds. Think dashboards. Less information, but more actionable.

#### 3

Let's take this a bit further. Think of your analysis as a function, $$G$$, of your data. This gives us:

$$
X \rightarrow Y \rightarrow G(Y)
$$

We can then formulate the learning problem as a search over the space of possible functions $$G$$. In order to assess the quality of one $$G$$ over another, we must use some sort of measure of "expressiveness". Call this $$E$$, such that $$E[G(Y)]$$ is some measurement of the expressiveness of the analysis $$G(Y)$$.

Our goal becomes finding an optimal function $$G^*$$ such that:

$$
E[G^*(Y)] \geq E[G(Y)], \forall G
$$

In other words, that $$G^*$$ maximizes the expressive power of the data $$Y$$. Our choice of $$E$$ drives the exploration of the space of possible $$G$$.

This is the general formulation. To see how this general formulation maps to practice, let's take $$G$$ to be some sort of classification or regression model and $$E$$ to be the log likelihood or squared error. Note how we have described the typical machine learning setting. To see how this formulation helps frame different problems, let's take $$G$$ to be a causal graph -- what then should $$E$$ be? How could one select an $$E$$ to drive exploration of the space of causal graphs?

#### 4

If our goal is to understand the world, then it would seem as though we have two opportunities for growth.

First, in our measurements. The world is of infinite dimension, and any measurement is a finite reflection. Measurements are choices, and the dimensions along which we choose to measure will place the upper bound on our usable knowledge.

Second, in our analysis. Given a finite set of measurements, $$Y$$, our goal is to transform this into a different representation that expresses the information necessary to a given task, with "expressiveness" itself given by some measure. If that task is prediction or classification (core learning problems), then expressiveness will almost certainly be measured either via the likelihood of the analysis or the smallness of the error. But there can be other tasks and other measures of expression.

Which, at this time, is our limiting factor? Are we limited by our analysis, unable to make sense of what we know? Or are we limited by our measurements, trying to navigate with skewed vision?

Do you know?

#### 5

**Proof:**

$$
I(\hat{X};X)
$$

Definition of mutual information:

$$
= H(X) - H(X|\hat{X})
$$

Conditioning reduces entropy:

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

**Note:** $$H(A)$$ denotes the **[entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory))** of the random variable $$A$$, a measure of uncertainty in $$A$$. Given that more information can't hurt, the following is always true:

$$
H(A|B) \leq H(A)
$$