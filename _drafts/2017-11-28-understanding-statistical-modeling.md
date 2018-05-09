---
layout: post
title: "Understanding Statistical Modeling"
comments: true
categories: blog
tags:

- statistics
- machine-learning

---

This post is about statistical modeling as a tool. Emphasis will be placed on the computational complexity associated with evaluating statistical models, as ultimately computational efficiency will be seen as a main driver of modeling decisions. Certain basic concepts in probability theory will be cast in a new light.

I.

We begin with the universe. We'll call it $$MU$$. $$MU$$ cannot be defined precisely nor measured. $$MU$$ consists of an very, very large number of particles, all interacting and passing through many states, on miniscule time scales. $$MU$$ contains the probabilities of everything, yet can never be useful as a tool.

So we take a step, and define $$mu$$, in which $$MU$$ is discretized into a ~large number of particles each in one of a ~large number of states, each with a corresponding probability. Unfortunately for $$mu$$, not only is it a mere approximation of $$MU$$, it is still far to large to ever be stored in memory, much less compute over: not useful. Yet, it is a well-formed discrete joint probability distribution:

$$
mu \triangleeq P({Z })
$$

Now, let's say that our interest wasn't in $$mu$$ as a whole, but instead was confined to a very small portion of it: the behavior of a certain coin $$X$$. We have methods for "excluding" superfluous variables from our models: we **marginalize** them away:

$$
P(X) = \sum_{Z \in mu/{X}} P(X, z)
$$