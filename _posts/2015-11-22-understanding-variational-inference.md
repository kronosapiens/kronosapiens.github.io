---
layout: post
title: "Understanding Variational Inference"
comments: true
categories: blog
tags:
- bayes
- statistics
- machine-learning
- data-science

---

In one of my courses this semester, [Bayesian Models for Machine Learning](http://www.columbia.edu/~jwp2128/Teaching/E6892/E6892Fall2015.html), we've been spending quite a bit of time on a technique called "[Variational Inference](https://en.wikipedia.org/wiki/Variational_Bayesian_methods)". I've spent the last few days working on an assigment using this technique, so I thought this would be a good occasion to test knowledge by attempting to describe the method. Much credit to [John Paisley](http://www.columbia.edu/~jwp2128/) for teaching me all this in the first place. The Columbia faculty are really top-notch.

## High-level Overview

First, a brief overview of Bayesian statistics. We begin with a distribution on our data $$x$$, paramaterized by $$\theta$$:

$$
p(x | \theta)p(\theta)
$$


Using basic rules of joint and conditional probability, we derive the theorem:

$$
p(\theta, x) = p(x, \theta)
$$

$$
p(\theta | x)p(x) = p(x | \theta)p(\theta)
$$

$$
\underbrace{
p(\theta | x) = \frac{p(x, \theta)p(\theta)}{p(x)}
}_{\text{Bayes Theorem}}
$$

For those unfamiliar with Bayes Theorem, our goal is to use the data $$x$$ to learn a *better* distribution on $$ \theta $$. In other words, Bayes Theorem gives us a formal way to update our predictions, given our experience of the world. In particular,

$$
p(\theta | x)
$$

is known as the *posterior* distribution of $$\theta$$. This distribution is our goal.

Now, the formulas given above are in terms of probability distributions. If we actually look under the hood at what these probabilities actually look like... well, it looks like a lot of calculus. Using Bayes Theorem involves working with those integrals. Fortunately, over the years statisticians have developed a pretty sophisticated body of knowledge around manipulating these probability distributions, so that (if you make smart choices about which distributions you pick) you can skip basically all of the calculus. This is convenient.

However, for more complicated models, things aren't always guaranteed to work out so nicely. Sometimes, when we try to model something, we find that calculating the posteriors directly is impossible. What can we do?

Fortunately, statisticians have developed techniques for handling this. Variational Inference is one of those techniques.

Now, we will derive the VI master equation.

Recall some basic rules of probability:

$$
p(\theta | x)p(x) = p(x, \theta)
$$

$$
p(x) = \frac{p(x, \theta)}{p(\theta | x)}
$$

$$
lnp(x) = lnp(x, \theta) - lnp(\theta | x)
$$

Now, we introduce an entirely new distribution, $$q(\theta)$$, and take the expectation with regards to this distribution:

$$
E_{q(\theta)}[lnp(x)] = E_{q(\theta)}[lnp(x, \theta)] - E_{q(\theta)}[lnp(\theta | x)]
$$

$$
\int q(\theta) lnp(x) d\theta = \int q(\theta) lnp(x, \theta) d\theta - \int q(\theta) lnp(\theta | x) d\theta
$$

Observing that the left-hand term is constant with respect to $$\theta$$:

$$
lnp(x) \int q(\theta) d\theta = \int q(\theta) lnp(x, \theta) d\theta - \int q(\theta) lnp(\theta | x) d\theta
$$

$$
lnp(x) = \int q(\theta) lnp(x, \theta) d\theta - \int q(\theta) lnp(\theta | x) d\theta
$$

We then add and subtract the [entropy](https://en.wikipedia.org/wiki/Maximum_entropy_probability_distribution) of $$q(\theta)$$:

$$
lnp(x) = \int q(\theta) lnp(x, \theta) d\theta - \int q(\theta) lnp(\theta | x) d\theta
+ \int q(\theta) lnq(\theta) d\theta - \int q(\theta) lnq(\theta) d\theta
$$

And reorganize:

$$
lnp(x) = \int q(\theta) (lnp(x, \theta) - q(\theta))d\theta - \int q(\theta) (lnp(\theta | x) - lnq(\theta)) d\theta
$$

$$
lnp(x) =
\underbrace{
\int q(\theta) ln\frac{p(x, \theta)}{q(\theta)} d\theta
}_{L}
+ \underbrace{
\int q(\theta) ln\frac{q(\theta)}{p(\theta | x)} d\theta
}_{KL(q||p)}
$$

Let's take a moment to understand what was just derived. We have shown that the log probability of the random variable $$x$$ is equal to the involved-looking equation on the right-hand side. This right-hand term is the sum of two terms. The first, which we call $$L$$, we will refer to as the "Variational Objective Function". The second is the equation of something known as the [Kullback–Leibler](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) divergence, or KL divergence for short.

Recall that our goal is to learn $$p(\theta \| x)$$.

*Note: The LaTeX engine I'm using doesn't doesn't support the single pipe \| for some reason when rendering inline math (probably due to a conflict with the Markdown parsing. I'll use the double pipe when I'm writing inline to represent conditional distributions. Apologies.*

We see that this term appears in the KL divergence, next to this new distribution we are calling $$q(\theta)$$. Conveniently, the KL divergence is a measure of the difference between two distributions. When the distributions are equal, the KL divergence equals 0. The more the distributions differ, the larger the term becomes. We're not sure what this $$q$$ distribution is, but let's assume that we can control it. The closer it comes to approximating the posterior, the smaller the KL divergence will become.

We see also that the left-hand term, $$lnp(x)$$, is a constant (just the probability of the data). So we have a constant equal to an equation plus a term we want to minimize. Therefore, if we can find a way to **maximize** the $$L$$ term, we will necessarily **minimize** the KL divergence. Therefore, the problem becomes one of finding a $$q(\theta)$$ distribution which maximizes $$L$$!

## In Context

Let's consider the model in the context of a very interesting problem. Say we have a non-linear function (such as $$sin(x), sinc(x)$$ or similar) and we would like to approximate this function via Bayesian Linear Regression. Approximating a non-linear function via a naive linear regression is not really feasible. However, if we expand the data into higher dimensions, it may be possible to learn a linear regression in the higher-dimensional space that corresponds to a non-linear function in the original dimension. This is what we will attempt in this problem.

We will project $$x_i, ... x_n \in R^{2}$$ into $$R^{n}$$, by projecting each $$x_i$$ into a vector of distances defined by the Gaussian kernel. In other words, every $$x_i$$ will become a vector representing that point's distance from every other point in the set -- and $$X$$, the data, becomes a $$n \times n$$ matrix of distances, with $$X_{ii} = 1$$ and $$X_{ij} \leq 1$$ for all $$j \neq 1$$. Adding a column of ones to represent any intercept term, we can now interpret the problem as a regression. Our goal is then to find a coefficient vector $$w$$ which, given the vector of difference, map the point to its correct location in the original space, $$R^{2}$$.

This transformation is quite a profound. We have many tools for working with linear functions (i.e. linear algebra), but fewer for working with non-linear functions. We found ourselves facing a problem, and rather than attempt to solve the problem using a limited toolset, we simply transformed the problem into one that we can approach skillfully. For any Ender's Game fans out there, this is an "enemy's gate is down" kind of moment. Anyway.

Complicating the problem further, we would like to encourage sparsity in $$w$$ -- in other words, we would like to identify a small subset of $$X$$ which are sufficiently discriminative to allow us to correctly place the other points. We can think of these points as "vantage points", and they are especially good at creating distance between points and illuminating their differences.

With that setup, we turn to the actual model, which looks like this:

$$
y_i \sim N(x_i^Tw, \lambda^{-1})
$$

$$
w_i \sim N(0, diag(\alpha_1, ..., \alpha_d)^{-1})
$$

$$
\lambda \sim Gamma(e_0, f_0)
$$

$$
\alpha_k \sim Gamma(a_0, b_0)
$$


The joint probability distribution is as follows:

$$
p(x,y,w, \lambda, \alpha)
= \prod_{i=1}^n p(y_i | x_i, w, \lambda)p(\lambda | e_0, f_0)p(w | \alpha)\prod_{k=1}^dp(\alpha_k| a_0, b_0)
$$

And the log joint probability is as follows:

$$
lnp(x,y,w, \lambda, \alpha)
= \sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(\lambda | e_0, f_0) + p(w | \alpha) + \sum_{k=1}^dp(\alpha_k| a_0, b_0)
$$

We model the $$q$$ distribution as a joint probability of independent distributions, one per variable:

$$
q(w, \lambda, \alpha) = q(w)q(\lambda)q(\alpha)
$$

Now, with the model defined, we plug these values in to the VI maste requation we derived earlier:

$$
lnp(y, x) =
\int q(w)q(\lambda)q(\alpha) ln \frac{p(x,y,w, \lambda, \alpha)}{q(w)q(\lambda)q(\alpha)} dw d\lambda d\alpha
+ \int q(w)q(\lambda)q(\alpha) ln \frac{q(w)q(\lambda)q(\alpha)}{p(w, \lambda, \alpha | x, y)} dw d\lambda d\alpha
$$

## Learning q

Recall, our goal is to maximize:

$$
L = \int q(w)q(\lambda)q(\alpha) ln \frac{p(x,y,w, \lambda, \alpha)}{q(w)q(\lambda)q(\alpha)} dw d\lambda d\alpha
$$

We will do this by finding better values for $$q(w)q(\lambda)q(\alpha)$$. To show how this is done, let's first consider $$q(w)$$ in isolation (the process will be the same for each variable). First, we reorganize the equation to remove all terms which are constant with respect to $$w$$ (in other words, which won't change regardless of $$w$$, so aren't important when it comes to maximizing the equation with regards to $$w$$):

$$
L = \int q(w) q(\lambda)q(\alpha) ln p(x,y,w, \lambda, \alpha) d\lambda d\alpha dw
- \int q(w) ln q(w) dw
- \text{const w.r.t } w
$$

Observe next that we can interpret the first integral as an expectation, where $$-q(w) = q(\lambda)q(\alpha)$$.

$$
L = \int q(w) E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)] dw
- \int q(w) ln q(w) dw
- \text{const w.r.t } w
$$


We will now pull off some slick math. First, observe that $$ln e^x = x$$. Now:

$$
L = \int q(w) ln \frac{e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]}}{q(w)} dw
- \text{const w.r.t } w
$$

This is looking an awful lot like our friend the KL divergence. If only the numerator were a probability distribution! Fortunately we can make it one, by introducing a new term $$Z$$:

$$
Z = \int e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]} dw
$$

Here, Z can be interpreted as the normalizing constant for the distribution $$e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]}$$. By adding and subtracting $$lnZ$$, we witness some more slick math:

$$
L = \int q(w) ln \frac{e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]}}{q(w)} dw
- \text{const w.r.t } w + lnZ - lnZ
$$

$$
L = \int q(w) ln \frac{\frac{1}{Z}e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]}}{q(w)} dw
- \text{const w.r.t } w
$$

Where are we now? We have succesfully transformed the integral into a KL divergence between $$q(w)$$, our distribution of interest, and $$\frac{1}{Z}e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]}$$, which is an expression involving terms we know. Specifically, we have:

$$
-KL(q(w)\|\frac{1}{Z}e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]})
$$

We want to maximize this expression, which is equivalent to *minimizing* -KL. We minimize -KL when the two distributions are equal. Therefore, we know that:

$$
q(w) = \frac{1}{Z}e^{E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]}
$$

Sweet! Now we just need to solve for the left hand term. It's worth pausing and noting how much fancy math it took to get us here. We relied on properties of logarithms, expectations, KL divergence, and the mechanics of probability distributions to derive this expression.

To actually evaluate this expression and figure out what $$q(w)$$  should be, we'll rewrite things to remove terms not involving $$w$$, by absorbing them in the normalizing constant. To see why this is the case, let's first rewrite the expectation:

$$
E_{-q(w)}[ln p(x,y,w, \lambda, \alpha)]
$$

Recalling the log joint probability we derived earlier:

$$
E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda)
+ p(\lambda | e_0, f_0)
+ p(w | \alpha)
+ \sum_{k=1}^dp(\alpha_k| a_0, b_0)]
$$

$$
p(\lambda | e_0, f_0) + \sum_{k=1}^dp(\alpha_k| a_0, b_0)
+ E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]
$$

Putting this back into context, we can rewrite the distribution:

$$
\frac{
e^{p(\lambda | e_0, f_0) + \sum_{k=1}^dp(\alpha_k| a_0, b_0)}
e^{E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]}
}{
\int e^{p(\lambda | e_0, f_0) + \sum_{k=1}^dp(\alpha_k| a_0, b_0)}
e^{E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]} dw
}
$$

Bringing outside of the integral all terms constant with respect to $$w$$:

$$
\frac{
e^{p(\lambda | e_0, f_0) + \sum_{k=1}^dp(\alpha_k| a_0, b_0)}
e^{E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]}
}{
e^{p(\lambda | e_0, f_0) + \sum_{k=1}^dp(\alpha_k| a_0, b_0)}
\int e^{E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]} dw
}
$$

And then cancelling:

$$
\frac{
e^{E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]}
}{
\int e^{E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]} dw
}
$$

All that is left to do is to evaluate the expression

$$
e^{E_{-q(w)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(w | \alpha)]}
$$

to learn the distribution. We will not go through the specific derivation here, which involves evaluating the expectation of the log of the distributions on $$y_i$$ and $$w$$; instead we will skip to the final result and claim that:

$$
q(w) \sim N(\mu, \Sigma)
$$

With:

$$
\Sigma = (E_{q(\alpha)}[diag(\alpha)] + E_{q(\lambda)}[\lambda] \sum_{i=1}^n x_i x_i^T)^{-1}
$$

$$
\mu = \Sigma(E_{q(\lambda)}[\lambda] \sum_{i=1}^n y_i x_i)
$$

The **key** observation to make here is that $$q(w)$$ involves the expected values of the *other* model variables. This will be true for the other variables as well. To show this, here are $$q(\lambda)$$ and $$q(\alpha)$$:

$$
q(\lambda) \sim Gamma(e, f)
$$

$$
e = e_0 + \frac{n}{2}
$$

$$
f = f_0 + \frac{1}{2} \sum_{i=1}^n [(y_i - E_{q(w)}[w]^T x_i)^2 + x_i^T Var_{q(w)}[w] x_i]
$$

$$
q(\alpha_k) \sim Gamma(a, b_k)
$$

$$
a = a_0 + \frac{1}{2}
$$

$$
b_k = b_0 + \frac{1}{2} E_{q(w)}[ww^T]_{kk}
$$

Finally, we give the expectations:

$$
E_{q(w)}[w] = \mu
$$

$$
Var_{q(w)}[w] = \Sigma
$$

$$
E_{q(w)}[ww^T] = \Sigma + \mu\mu^T
$$

$$
E_{q(\lambda)}[\lambda] = \frac{e}{f}
$$

$$
E_{q(\alpha_k)}[\alpha_k] = \frac{a}{b_k}
$$

Now we are prepared to discuss the value of this technique. Note how each $$q()$$ distribution is a function of the expectations of the other random variables, *with respect to their $$q()$$ distributions. This means that as one distribution changes, the others change... causing the first to change, causing the others to change, over and over again in a loop. The insight is that each change* brings the $$q()$$ closer to the true posterior that we are trying to approximate. In other words, each iteration through this update loop gives us a better set of $$q()$$, as improved values for one give improved values for the others. Also note that since we have solved for the various $$q()$$ distributions solely in terms of the data $$y_i, x_i$$ and the expecatations $$E[w], E[\lambda], E[\alpha]$$, we can implement the algorithm efficiently using only basic arithmetic operations, without having to do any calculus or derive anything!

## Assessing Convergence

The last thing we will need to do is discuss the process for assessing convergence -- calculating how much and how quickly our $$q$$ distributions are closing in on the true posteriors. To do this, we will have to evaluate the entire $$L$$ equation using the new $$q$$ distributions. Recall the equation:

$$
L = \int q(w)q(\lambda)q(\alpha) ln \frac{p(x,y,w, \lambda, \alpha)}{q(w)q(\lambda)q(\alpha)} dw d\lambda d\alpha
$$

Which can be written as follows:

$$
L = \int q(w)q(\lambda)q(\alpha) ln p(x,y,w, \lambda, \alpha) dw d\lambda d\alpha
- \int q(w) ln q(w) dw
- \int q(\lambda) ln q(\lambda) d\lambda
- \int q(\alpha) ln q(\alpha) d\alpha
$$

And interpreted as a sum of expectations:

$$
L = E_{q(w, \lambda, \alpha)}[ln p(x,y,w, \lambda, \alpha)]
- E_{q(w)}[ln q(w)]
- E_{q(\lambda)}[ln q(\lambda)]
- E_{q(\alpha)}[ln q(\alpha)]
$$

$$
L = E_{q(w, \lambda, \alpha)}[ln p(x,y,w, \lambda, \alpha)]
- E_{q(w)}[ln q(w)]
- E_{q(\lambda)}[ln q(\lambda)]
- E_{q(\alpha)}[ln q(\alpha)]
$$

$$
L = E_{q(w, \lambda, \alpha)}[\sum_{i=1}^n p(y_i | x_i, w, \lambda) + p(\lambda | e_0, f_0) + p(w | \alpha) + \sum_{k=1}^dp(\alpha_k| a_0, b_0)]
- E_{q(w)}[ln q(w)]
- E_{q(\lambda)}[ln q(\lambda)]
- E_{q(\alpha)}[ln q(\alpha)]
$$

Which breaks down as follows:

$$
L =
\sum_{i=1}^n E_{q(w, \lambda)}[p(y_i | x_i, w, \lambda)]
+ E_{q(\lambda)}[p(\lambda | e_0, f_0)]
+ E_{q(w, \alpha)}[p(w | \alpha)]
+ \sum_{k=1}^d E_{q(\alpha)}[p(\alpha_k| a_0, b_0)]
$$

$$
- E_{q(w)}[ln q(w)]
- E_{q(\lambda)}[ln q(\lambda)]
- E_{q(\alpha)}[ln q(\alpha)]
$$

There is an important subtlety in evaluating these expectations. To understand this subtlety, let's look at two of the terms:

$$
E_{q(\lambda)}[p(\lambda | e_0, f_0)] - E_{q(\lambda)}[ln q(\lambda)]
$$

Observe how both are expectations over $$q(\lambda)$$. However the probability distributions are not the same. To see how this works out, let's write out the actual log probabilities (both distributions are Gamma).

$$
E_{q(\lambda)}[p(\lambda | e_0, f_0)]
= E_{q(\lambda)}[(e_0lnf_0 - ln\Gamma(e_0)) + (e_0 - 1)ln\lambda - f_0\lambda]
$$

$$
E_{q(\lambda)}[ln q(\lambda)]
= E_{q(\lambda)}[(e lnf - ln\Gamma(e)) + (e - 1)ln\lambda - f\lambda]
$$

Now, passing the expectations through:

$$
(e_0lnf_0 - ln\Gamma(e_0)) + (e_0 - 1)E_{q(\lambda)}[ln\lambda] - f_0E_{q(\lambda)}[\lambda]
$$

$$
(e lnf - ln\Gamma(e))+ (e - 1)E_{q(\lambda)}[ln\lambda] - fE_{q(\lambda)}[\lambda]
$$

Writing in terms of the difference (note that the sign changes in the second expectation):

$$
(e_0lnf_0 - ln\Gamma(e_0)) + (e_0 - 1)E_{q(\lambda)}[ln\lambda] - f_0E_{q(\lambda)}[\lambda]
- (e lnf - ln\Gamma(e)) - (e - 1)E_{q(\lambda)}[ln\lambda] + fE_{q(\lambda)}[\lambda]
$$

And combining terms:

$$
(e_0lnf_0 - ln\Gamma(e_0)) - (e lnf - ln\Gamma(e))
+ (e_0 - e)E_{q(\lambda)}[ln\lambda] - (f_0 - f)E_{q(\lambda)}[\lambda]
$$

Notice how for both distributions, $$E_{q(\lambda)}[\lambda]$$ is identical. This is because $$E_{q(\lambda)}[\lambda]$$ is a function of the distribution with which we are taking the expectation, $$q(\lambda)$$. Therefore, even though the paramaters for $$p(\lambda)$$ don't change (they remain $$e_0, f_0$$ always), $$p(\lambda)$$ evaluates to a different result as $$q(\lambda)$$ changes. For $$q(\lambda)$$, on the other hand, we always use the latest values of $$f, e$$.

At first I found it counterintuitive that $$e_0, f_0$$ should be constant through every iteration -- the Bayesian insight is that priors are constantly being updated as information comes in. The reason why, in this case, $$e_0, f_0$$ are constant (and this is true for the priors on the other distributions as well) is that the entire Variational Inference algorithm is meant to approximate a **single** Bayesian update. Thus, it is wrong to interpret the $$q()$$ distribution learned from iteration $$t$$ as the new prior on the model variables for iteration $$t+1$$. In the context of the single update (regardless of current iteration), $$p()$$ is always the initial prior, and $$q()$$ is the best posterior-so-far. The VI concept is that we can iteratively improve the posteriors $$q()$$, but always in the context of a *single* Bayesian update.

## Final Thoughts

We have presented Variational Inference, in a hopefully accessible manner. It is a very slick technique that I am excited to continue to gain skill in applying. VI is the inference technique which underlies [Latent Dirichlet Allocation](http://www.columbia.edu/~jwp2128/Teaching/E6892/papers/LDA.pdf), a very popular learning algorithm developed by David Blei (now at Columbia!), Andrew Ng, and Michael Jordan, all Machine Learning heavyweights, while the former was at Cal (Go Bears)!

Earlier, we mentioned that we wanted to encourage sparsity in $$w$$. This can be accomplished (so I am told), by setting the priors on $$\alpha_k$$ to $$a_0, b_{0k} = 10^{-16}$$. Tiny priors here will limit the dimensions of $$w$$ which are signicantly non-zero. I'm not entirely sure why (something I still need to look into), but I can assure you that my model was super sparse :).

Variational Inference is a fairly sophisticated technique (the most complex algorithm I have encountered, but that might not count for much), and allows for the formal definition and learning of complex posteriors otherwise intractable using normal Bayesian methods.

If you're curious, you can see [my implementation](https://github.com/kronosapiens/bayesian-models/blob/master/models.py#L184) of the algorithm described above on GitHub. The [full derivations](https://github.com/kronosapiens/bayesian-models/blob/master/HW03/hw3.pdf) are here, along with measurements of the performance of my model.