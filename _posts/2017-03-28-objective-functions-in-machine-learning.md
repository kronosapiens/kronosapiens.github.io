---
layout: post
title: "Objective Functions in Machine Learning"
comments: true
categories: blog
tags:
- machine learning
- optimization
- math

---

Machine learning can be described in many ways. Perhaps the most useful is as type of optimization. Optimization problems, as the name implies, deal with finding the best, or "optimal" (hence the name) solution to some type of problem, generally mathematical.

In order to find the optimal solution, we need some way of measuring the quality of any solution. This is done via what is known as an **objective function**, with "objective" used in the sense of a goal. This function, taking data and model parameters as arguments, can be evaluated to return a number. Any given problem contains some parameters which can be changed; our goal is to find values for these parameters which either maximize or minimize this number.

The objective function is one of the most fundamental components of a machine learning problem, in that it provides the basic, formal specification of the problem. For some objectives, the optimal parameters can be found exactly (known as the analytic solution). For others, the optimal parameters cannot be found exactly, but can be approximated using a variety of iterative algorithms.

Put metaphorically, we can think of the model parameters as a ship in the sea. The goal of the algorithm designer is to navigate the space of possible values as efficiently as possible to guide the model to the optimal location.

For some models, the navigation is very precise. We can imagine this as a boat on a clear night, navigating by stars. For others yet, the ship is stuck in a fog, able to make small jumps without reference to a greater plan.

Let us consider a concrete example: finding an average. Our goal is to find a value, $$\mu$$, which is the best representation of the "center" of some set of n numbers. To find this value, we define an objective: the sum of the squared differences, between this value and our data:

$$
\mu = argmin_{\mu} \sum_{i=1}^n (x_i - \mu)^2
$$

This is our objective function, and it provides the formal definition of the problem: to **minimize an error**. We can analyze and solve the problem using calculus. In this case, we rely on the foundational result that the minimum of a function is reliably located at the point where the derivative of the function takes on a zero value. To solve the function, we take the derivative, set it to 0, and solve for $$\mu$$:

$$
\frac{d}{d\mu} \sum_{i=1}^n (x_i - \mu)^2 = \sum_{i=1}^n -2(x_i - \mu) = 0
$$

$$
\sum_{i=1}^n (x_i - \mu) = 0
$$

$$
\sum_{i=1}^n x_i = n\mu
$$

$$
\frac{\sum x_i}{n} = \mu
$$

And so. We see that the value which minimizes the squared error is, in fact, the mean. This elementary example may seem trite, but it is important to see how something as simple as an average can be interpreted as a problem of optimization. Note how the value of the average changes with the objective function: the mean is the value which minimizes the sum of squared error, but it is the median which minimizes the sum of *absolute error*.

In this example, the problem could be solved analytically: we were able to find the exact answer, and calculate it in linear time. For other problems, the objective function does not permit an analytic or linear-time solution. Consider the logistic regression, a classification algorithm whose simplicity, flexibility, and robustness has made it a workhorse of data teams. This algorithm iterates over many possible classification boundaries, each iteration yielding a more discriminant classifier. Yet, the true optimum is never found: the algorithm simply terminates once the solution has reached relative stability.

There are other types of objective functions that we might consider. In particular, we can conceive of the *maximizing of a probability*.

Part of the power of probability theory is the way in which it allows one to reason formally (with mathematics) about that which is fundamentally uncertain (the world). The rules of probability are simple: events are assigned a probability, and the probabilties must all add to one, because *something* has to happen. The way we represent these probabilities, however, is somewhat arbitrary -- a list of real numbers summing to 1 will do. In many cases, we use functions.

Consider flipping a coin. There are two possible outcomes: heads and tails. The odds of heads and the odds of tails must add to 1, because one of them must come up. We can represent this situation with the following equation:

$$
p^x(1-p)^{1-x}
$$

Here $$x$$ is the coin and $$x = 1$$ means heads and $$x = 0$$ if tails, and $$p$$ is the odds of coming up heads. We see that if the coin is heads, the value is $$p$$, the chance of heads. If the coin is tails, the value is $$1-p$$, which by necessity is the chance of tails. We call this equation $$P(x)$$, and it is a probability distribution, telling us the probability of various outcomes.

Now, not all coins are fair (meaning that $$p = 1-p = 0.5$$). Some may be unfair -- with heads, perhaps, coming up more often. Say we flipped a coin a few times, and we were curious as to whether the coin was biased. How might we discover this? Via the likelihood equation. Intuitively, we seek a value of p which gives the *maximum likelihood* to the coin flips we saw.

The word maximum should evoke our earlier discussion: we are again in the realm of optimization. We have a function and are looking for an optimal value: except now instead of minimizing an error, we want to **maximize a likelihood**. Calculus helped us one before -- perhaps it may again?

Here is the *joint likelihood distribution* of our series $$x$$ of n coin flips (now $$x$$ represents many flips, each individual flip subscripted $$x_1$$, etc):

$$
P(x) = \prod_{i=1}^n p^{x_i}(1-p)^{1-x_i}
$$

The thing to note here is that the probability of two what we call *independent* events (i.e. one does not give us knowledge about the other) is the product of the probability of the events separately. In this case, the coin flips are *conditionally independent* given heads probability p.

The *logarithm* is a remarkable function. When introduced in high school, the logarithm is often presented as "the function which tells you the power you would need to raise a number to to get back the original argument", or put more succintly, the degree to which you would need to exponentiate a base. This exposition obscures the key applications of the logarithm:

1. It makes small numbers big, and big numbers small.
2. It turns multiplication into addition.
3. It increases monotonically (if $$x$$ gets bigger, $$log(x)$$ gets bigger).

The first point helps motivate the use of "log scales" when presenting data of many types. Humans (and computers) are comfortable reasoining about magnitudes along certain types of scales; others, such as exponential scales, are less intuitive. The logarithm allows us to interpret events happening on incredible magnitude in a more familiar way. This property, conveniently, also comes in handy when working with very small numbers -- such as those involved in join probability calculations, in which the probability of any particular complex event is nearly 0. The logarithm takes very small positive numbers and converts them to more comfortable, albeit negative, numbers -- much easier to think about (and, perhaps more importantly, compute with).

The second point comes in handy when we attempt the actual calculus. By turning multiplication into addition, the function is more easily differentiated, without resorting to cumbersome applications of the product rule.

The third point provides the essential guarantee that the optimal solution for the log function will be identical with the optimal solution for the original function. This means that we can optimize the log function and get the right answer for the original.

Taking the logarithm of the joint likelihood function, we get the **log likelihood**:

$$
log(P(x)) = \sum_{i=1}^n x_ilog(p) + (1-x_i)log(1-p)
$$

What can we do with this? In this problem, we can use it to find the optimal value for p. Taking the derivative of this function with respect to p (recall that the derivative of $$log(x)$$ is $$1/x$$), and setting to 0, we have:

$$
\frac{d}{dp}log(P(x)) = \sum_{i=1}^n \frac{x_i}{p} - \frac{1-x_i}{1-p} = 0
$$

We can solve for p:

$$
\sum_{i=1}^n \frac{x_i(1-p)}{p} - (1-x_i) = 0
$$


$$
\sum_{i=1}^n (\frac{x_i}{p}-x_i) - (1-x_i) = 0
$$

$$
\sum_{i=1}^n \frac{x_i}{p} - 1 = 0
$$

$$
\frac{\sum_{i=1}^n x_i}{p} = n
$$

$$
\frac{\sum_{i=1}^n x_i}{n} = p
$$

And so again, the optimal value for the probability p of heads is the ratio of observed heads to total observations. We see how our intuition ("the average!") is made rigorous by the formalism.

This example is a model of a simple object. More advanced objects (such as a graph of interdependent events) require more advanced models (such as a Hidden Markov Model), for which the optimal solution involves many variables and as a consequence more elaborate calculations. In some cases, as with the logistic regression, the exact answer cannot ever be known, only iteratively approached.

In all of these cases, however, the log of the likelihood function remains an essential tool for the analysis. We can use it to calculate a measure of quality for an arbitrary combination of parameters, as well as use it (in a variety of ways) to attempt to find optimal parameters in a computationally efficient way. Further, while the examples given above are possibly the two simplest non-trivial examples of these concepts, they capture patterns of derivation which recur in more complex models.


