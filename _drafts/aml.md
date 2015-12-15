---
layout: post
title: "AML"
date: 2015-12-01 23:48:25 -0500
comments: false
categories: blog

---

General:

\[
x \sim Bern(G_{ij} = z)
\]

\[
\sigma^2 = var(x) = z(1-z)
\]

\[
0 \leq \sigma^2 \leq .25
\]

\[
0 \leq \sigma \leq .5
\]

For the proofs, we set $\sigma$ as the largest deviation of an entry in $\hat{M}$.

Theorem 12 proof:

We show that:

\[
|P_{\hat{A}}(B_u) - B_u| \leq 8\sigma\sqrt{nk/s_u}
\]

And that with probability at least $1 - \delta$,

\[
|P_{\hat{A}}(B_u - \hat{B_u})| \leq \sqrt{2klog(n/\delta)}
\]

...

First, we rewrite the following expression:

\[
(I - P_{\hat{A}})B
\]

\[
(I - P_{\hat{A}})(\hat{A} - \hat{A} + B)
\]

\[
(I - P_{\hat{A}})\hat{A} - (I - P_{\hat{A}})(\hat{A} - B)
\]

And then, relying on the assumed equivalence between $A, B$:

\[
(I - P_{\hat{A}})\hat{A} - (I - P_{\hat{A}})(\hat{A} - A)
\]

Note -- not sure how he's taking the norms here. When I expand I get this:

\[
(I - P_{\hat{A}})\hat{A} - (I - P_{\hat{A}})\hat{A} + (I - P_{\hat{A}})A
\]

\[
(I - P_{\hat{A}})A
\]

Or this:

\[
(\hat{A} - P_{\hat{A}}\hat{A}) - (\hat{A} - A) + (P_{\hat{A}}\hat{A} - P_{\hat{A}}A)
\]

When it seems like what we want is:

\[
(\hat{A} - P_{\hat{A}}\hat{A}) + (\hat{A} - A) + \epsilon
\]

Weyl's Inequality is a result regarding the change in eigenvalues for a random perturbation of a Hermitian matrix. In our case, since our matrices are all real-valued, this means only that the matrices are symmetric (which in this case they are). They are actually positive semi definite, meaning that all eigenvalues are $\geq 0$.

https://en.wikipedia.org/wiki/Weyl%27s_inequality#Weyl.27s_inequality_in_matrix_theory

https://terrytao.wordpress.com/2010/01/12/254a-notes-3a-eigenvalues-and-sums-of-hermitian-matrices/

We wish to show the following:

\[
|\lambda_i(A) - \lambda_i(B)| \leq ||A - B||
\]

We begin by placing the values in quadratic form, where $u_i, v_i$ are the respective eigenvectors of $\lambda_i(A), \lambda_i(B)$.

\[
|\lambda_i(A) - \lambda_i(B)|
\]

\[
= |u_i^TAu_i - v_i^TBv_i|
\]

\[
\leq |u_i^TAu_i - u_i^TBu_i|
\]

The inequality is due to the fact that $u^TBu \leq v_i^TBv_i$ for any $u \in S^{d-1}$, and that $B$ has positive eigenvalues.

\[
= |u_i^T(A - B)u_i|
\]

\[
\leq max_{w}|w^T(A - B)w|
\]

\[
= ||A - B||
\]

With this result, we see how we can bound

\[
|\hat{A} - P_{\hat{A}}\hat{A}| \leq |\hat{A} - A|
\]

Since $P_{\hat{A}}\hat{A}$ is the projection onto the first $k$ eigenvectors of $\hat{A}$,

\[
|\hat{A} - P_{\hat{A}}\hat{A}| = \lambda_{k+1}(\hat{A})
\]

Further, since $rank(A) = k$, $\lambda_{k+1}(A) = 0$. Using Weyl's Inequality, we show that:

\[
\lambda_{k+1}(\hat{A}) = \lambda_{k+1}(\hat{A}) + \lambda_{k+1}(A) \leq |\hat{A} - A|
\]

Thus bounding:

\[
||(I - P_{\hat{A}})B||_2 \leq 2||\hat{A} - A||_2
\]

Recall an earlier claim:

\[
|\{i: |M_i|^2 > |M|^2_F/c\}| \leq c
\]

\[
|\{i: |M_i| > |M|_F/\sqrt{c}\}| \leq {\sqrt{c}}
\]

Here, we observe that the number of columns in a vector with a norm larger than some fraction of the Frobenius norm is bounded by the size of that fraction. For a simple example, consider how no more than two vectors can have length greater than half the Frobenius norm. If they did, the Frobenius norm would necessarily be larger (as it is the sum of the norms of the vectors).

We use this claim to show that, as there are $s_u$ nodes of type $u$ (recall our earlier claim that the classes are evenly split into $A, B$), no column $(I - P_{\hat{A}})B_u$ can have length greater than:

\[
||(I - P_{\hat{A}})B_u|| \leq 2||\hat{A} - A||_F/\sqrt{s_u}
\]

Recalling the following relation for $M, rank(M) = k$:

\[
||M||_F^2 \leq k||M||_2^2
\]

We rewrite:

\[
||(I - P_{\hat{A}})B_u|| \leq 2||\hat{A} - A||\sqrt{k/s_u}
\]

Recall the result from Theorem 10, which stated that:

\[
Pr[|\hat{M} - M| \leq 4\sigma\sqrt{n}] \geq 1 - 2e^{-\sigma^2n/8}
\]

Which, for $\sigma >> log^6(n)/n$, is:

\[
Pr[|\hat{M} - M| \leq 4\sigma\sqrt{n}] \geq 1 - O(e^{-log^6(n)})
\]

With that in mind, we say that:

\[
||\hat{A} - A||_2 \leq 4\sigma\sqrt{n}
\]

With probability $1 - \delta$ for $\delta \geq 2e^{-\sigma^2n/8}$. This yields the first inequality of the proof:

\begin{equation}
||P_{\hat{A}}(B_u) - B_u|| \leq 8\sigma\sqrt{nk/s_u}
\end{equation}

\[
***
\]

Turning to the second inequality, writing $P_{\hat{A}}$ as $QQ^T$, with $Q$ being the first $k$ left singular unit vectors of $\hat{A}$, we show that:

\[
||QQ^T(B_u - \hat{B}_u)||_2^2
\]

\[
= (QQ^T(B_u - \hat{B}_u))^T(QQ^T(B_u - \hat{B}_u))
\]

\[
= (B_u - \hat{B}_u)^TQQ^TQQ^T(B_u - \hat{B}_u)
\]

\[
= (B_u - \hat{B}_u)^TQQ^T(B_u - \hat{B}_u)
\]

\[
= \sum_{i=1}^k ((B_u - \hat{B}_u)^TQ_i)^2
\]

We then see that for any $Q_i$,

\[
\dotp{(B_u - \hat{B}_u), Q_i} = \sum_{j=i}^n (B_{uj} - \hat{B}_{uj})Q_{ij}
\]

Next, note that $(B_{uj} - \hat{B}_{uj})Q_{ij}$ is a zero-mean random variable, as $\hat{B}_{uj} \sim Bern(B_{uj})$. This variable is upper-bounded as $1$ (in which $Q_{i} = e_i, B_{uj} = 1$, and $\hat{B}_{uj} = 0$.), and lower bounded by $-1$.

Next, observe that:

\[
\sum_{j=1}^n ((B_{uj} - \hat{B}_{uj})Q_{ij})^2
\]

\[
= \sum_{j=1}^n (B_{uj} - \hat{B}_{uj})^2 Q_{ij}^2
\]

Because $0 \geq (B_{uj} - \hat{B}_{uj}) \geq 1$, and

\[
\sum_{j=1}^n Q_{ij}^2 = ||Q_j||_2^2 = 1
\]

we can bound:

\[
\sum_{j=1}^n (B_{uj} - \hat{B}_{uj})^2 Q_{ij}^2 \leq 1
\]

These results let us use **Azuma's Inequality** to bound the likelihood. The statement of the theorem is as follows:

Let ${X_i}$ be independent zero-mean random variables such that $-c_i \leq X_i \leq c_i$ and also that $\sum_{i=1}^n c_i^2 \leq 1$. Then for any $\lambda > 0$:

\[
Pr[|\sum_{i=1}^n X_i| \geq \lambda] \leq 2e^{-\frac{\lambda^2}{2}}
\]

We have shown that $(B_{uj} - \hat{B}_{uj})Q_{ij}$ is a zero-mean random variable and that the sum of these variables squared is $\leq 1$. Therefore, we can show that:

\[
Pr[|\sum_{j=i}^n (B_{uj} - \hat{B}_{uj})Q_{ij}| \geq \lambda] \leq 2e^{-\frac{\lambda^2}{2}}
\]

\[
Pr[|\dotp{(B_u - \hat{B}_u), Q_i}| \geq \lambda] \leq 2e^{-\frac{\lambda^2}{2}}
\]

Now, recall:

\[
||P_{\hat{A}}(B_u - \hat{B}_u)||_2^2 = \sum_{i=1}^k \dotp{(B_u - \hat{B}_u), Q_i}^2
\]

Applying a union bound over the $k$ left singular vectors:

\[
Pr[\dotp{(B_u - \hat{B}_u), Q_i}^2 \geq \lambda^2] \leq 2e^{-\frac{\lambda^2}{2}}
\]

\[
U_i[Pr[\dotp{(B_u - \hat{B}_u), Q_i}^2 \geq \lambda^2]] \leq k2e^{-\frac{\lambda^2}{2}}
\]

\[
Pr[||P_{\hat{A}}(B_u - \hat{B}_u)||_2^2 \geq \lambda^2] \leq k2e^{-\frac{\lambda^2}{2}}
\]

\[
Pr[||P_{\hat{A}}(B_u - \hat{B}_u)||_2 \geq \lambda] \leq k2e^{-\frac{\lambda^2}{2}}
\]

Recall that our goal is to show that:

\[
Pr[|P_{\hat{A}}(B_u - \hat{B_u})| \leq \sqrt{2klog(n/\delta)}] \geq 1 - \delta
\]

Equivalent to:

\[
Pr[|P_{\hat{A}}(B_u - \hat{B_u})| \geq \sqrt{2klog(n/\delta)}] \leq \delta
\]

A formulation which permits an easy application of Azuma. We wish to put the bound in terms of $\delta$ and then solve for $\lambda$.

\[
k2e^{-\frac{\lambda^2}{2}} = \delta
\]

\[
e^{-\frac{\lambda^2}{2}} = \frac{\delta}{2k}
\]

\[
e^{\frac{\lambda^2}{2}} = \frac{2k}{\delta}
\]

\[
\frac{\lambda^2}{2} = log(\frac{2k}{\delta})
\]

\[
\lambda^2 = 2log(\frac{2k}{\delta})
\]

\[
\lambda = \sqrt{2log(\frac{2k}{\delta})}
\]

Note -- this isn't what we want. We want:

\[
\frac{n}{2}2(e^{-\frac{\lambda^2}{2}})^{1/k} = \delta
\]

Union bound over n/2 nodes in A? Take kth root of e? How can we justify this?
