---
layout: post
title: "To Unit Test or not to Unit Test"
date: 2014-04-24 17:52:44 -0400
comments: true
categories: blog
tags:
- testing

---

It seems like some dust has been <a href="http://david.heinemeierhansson.com/2014/tdd-is-dead-long-live-testing.html">stirred up</a> around the issue of unit testing and the role that unit tests should play in a developer's overall TDD strategy. After reading through some <a href="http://www.rbcs-us.com/documents/Why-Most-Unit-Testing-is-Waste.pdf">writings</a> on 'con' side, I'm finding the issue very thought-provoking, specifically in regards to the relationship of unit tests and code design.

Before moving on though, let's draw a distinction between the general concept of TDD (writing tests to help you define your needs and design your program) and unit testing (testing specifically of models and model methods). These are often lumped together, and many people think of TDD only as unit testing. This is not necessarily the case, and, as I'll try to feel out, this conflation may be the cause of the current debate.

<!--more-->

When I was taught TDD, the emphasis was on using unit tests to help you design your methods -- by specifying the method's environment, inputs, and outputs beforehand, you create a sketch of the method, which you then fill in by actually writing the code. Reading through Sandi Metz's <a href="http://www.poodr.com/">book</a> helped drive this point home. She wrote about how well-designed code should be easy to test -- if you find yourself struggling to write tests for some class or method, then you need to re-think that method.

What I took from all this is that writing tests first helps you write concise, efficient code, and that hard-to-test methods are a mark against the method, not the testing framework.

This anti-TDD movement (if we can call it a 'movement'... perhaps it's more of a gesture, or a thought -- and again, referring to the unit-testing-style of TDD) seems to be coming down on this philosophy, at least to the extent that it has become ideology. The crux of their concern seems to be that the emphasis on unit testing has created incentives for people to <em>artificially</em> <em>break down</em> their code into simple methods <em>purely to aid in testing</em>. Implied here is that a larger, more complex method is what the application truly needed, and that the 'ideal' code is being sacrificed and turned into too many too-small helpers. <a href="http://www.rbcs-us.com/documents/Why-Most-Unit-Testing-is-Waste.pdf">James O Coplien</a> makes the point that a single algorithm, if written as many small methods, will actually be more confusing to understand than a single, larger method, due to the difficulty of following the trace and understanding the contexts in which every helper method is called.

James goes on to talk about how company policies around testing coverage has been incentivizing people to break up code into easily-testable chunks, which pushes up testing coverage but reduced overall comprehensibility. He drives the point home with the following thoughtful exhortation:

<blockquote>If you find your testers splitting up functions to support the testing process, you’re destroying your system architecture and code comprehension along with it. Test at a coarser level of granularity.</blockquote>

This makes sense, and is in line with <a href="http://david.heinemeierhansson.com/2014/tdd-is-dead-long-live-testing.html">DHH's critique</a>. DHH comes down against unit testing as being over-emphasized in relation to things like feature and integration tests, the 'coarser levels of granularity' that James talks about. DHH seems to take the position that tests should be oriented around the user's experience, not so much the verification of details of implementation.

This is starting to make sense, but there's something unsettling still. What about the core purpose of unit testing -- that is, to make it easier to find bugs in the code? With a full suite of unit tests, it seems as though it would be much easier to pinpoint and fix bugs. With a coarser set of tests, we would expect that developers would have to work harder to fix failing tests, since the failures would be occurring at a lower level than the tests. It would seem that by foregoing unit tests, we are setting ourselves up for a longer and painful debugging process, if and when (but mostly when) bugs arise.

The response to that, I would expect, is that developers should <em>prepare</em><em> </em>for that debugging process. The idea seems to be that developers should plan on debugging their methods in the absence of tests, and that methods <em>don't necessarily need</em> to be defined by a test suite. Methods can change as necessary to implement the <em>features</em> being built. Beyond features, they have no substance. In a sense, then, all methods can be seen as private methods. Further, a strong developer would not <em>need</em> unit tests to debug methods -- they would have a sufficiently strong grasp of their language to <em>think things through. </em>As a young developer, I've found unit tests very helpful in building my models, but I can imagine how a senior developer might find unit tests more tedious than helpful.

But won't that blow up in our faces? Wont unit tests save us hours of hunting down bugs?  Isn't the whole point of testing to save time (and money?).  Not necessarily. James goes on to make a number of points against unit tests. First, he points out that tests that never fail (or at least, once a method has been written to pass them) become deadweight in your test suite. Those methods aren't failing, and will never fail (unless they are re-written) -- and as such, those tests tell you nothing. He advises developers to delete any test that hasn't failed in over a year. Then, he explains how, given the complexity of on object-oriented application, "test coverage" becomes a meaningless metric  because it is impossible to test for every <em>possible combination </em>of events, even if you "test" every line. Following that line of reasoning, unit tests can become distractions, diverting attention away from problems in higher-level design.

That said, I'm still not entirely convinced. Something I admire about designing code is how well-written basic functions can be reused in new contexts. Designing around features instead of around units seems as though it would lead to more sloppiness at the unit level, reducing the overall quality of the codebase and making future change difficult.

That said, if I were to take the opposite position, I could say that leaving flexibility at the unit level is a good thing, because it allows a great deal of room to experiment with new methods and algorithms <em>without having to edit any existing tests</em>.

James eventually comes around and acknowledges the importance of unit-level specificity, and advocates for making <em>assertions</em> about methods, in lieu of actually testing them. Assertions are not something I have experience with, so I can't comment more on that.

All this makes sense. But there seems to be some lingering contradictions. On one hand, TDD on the unit level helps keep methods small, simple, and ostensibly more reusable. On the other, TDD on the unit level creates an incentive to artificially chop up logical units into confusing (albeit easily testable) atoms. The confusion is these are two sides of the same coin -- and the challenge becomes discerning when chopping up a complex method into simpler helper functions is a step <em>towards </em>clarity, or a step away. It seems like the answer is to stop seeing test coverage and the simplicity of a test suite as a perfect metric for code quality, but rather as one among many measurements and signals that must be taken into account. Every project will differ, and unit tests should play an accordingly different role.

As with all worthwhile ideas, unit-level TDD seems to contain within itself a contradiction -- unit testing can both help you organize your ideas and design quality code at the lowest levels of your application, and incentivize you to break up your code into confusing atoms to conform to out-of-touch expectations around test coverage. This contradiction should be acknowledged -- it is the sign of a good idea. Within the contradiction is wisdom, and rather than argue for one 'correct' interpretation or another, we should engage with that contradiction, hold the tension, and learn from it.