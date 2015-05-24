---
layout: post
title: "Designing Software to Influence Behavior"
date: 2014-05-04 17:11:13 -0400
comments: true
categories: blog
tags:
- software
- behavioral-economics

---

> Putting the fruit at eye level counts as a nudge. Banning junk food does not.

> Sunstein & Thaler, Nudge


### Where I'm Coming From With This

As an eccentric and unusually curious freshman at Berkeley, I decided one day that I hated the idea of a major, and resolved to try and study everything. Nothing would be outside of my sphere of interest -- computer science, economics, sociology, neuroscience, linguistics, philosophy, history, biology, political science, psychology. I absorbed it all, with abandon.

Four and a half years later, I found myself graduating, PBK, with a double-major in Cognitive Science and Political Economy. People would stare at me quizzically when I told them what I studied, often asking me what those two disparate fields could possibly have in common.

As it turns out, quite a lot. Cognitive Science provided the micro view of human beings -- how they think, process information, and make decisions. Political Economy provided the macro -- the trends of markets and culture, the forces that shape governments and insitutions. These random disciplines somehow managed to coaelsce into a quite powerful perspective on individuals and society, and taught me to think constantly about how individual actions aggregate into group behavior, and wonder about possibilities of shaping individual behavior to bring about better collective outcomes.

<!--more-->

### Transition to Software

One of the reasons I'm so excited about making the transition to software (besides that it's an awesome field that's thrilling to work in) is that it provides the opportunity to design new ways for people to interact with information -- ways which can be designed for *good*, designed to help bring about better outcomes for individuals, and by extension for society.

That said, it's a long road from starry-eyed visions of a better world to actually creating tools capable of making a difference. Succeeding on that journey, I believe, demands a tremendous amount of study, self-awareness of your own biases, and deference to data over intution. We as humans are predisposed to assuming that other people's perceptions mirror our own -- designing software *that actually works* demands that you distance yourself from yourself and turn towards data -- the more the better, the more rigorously collected the better -- about how people respond to various kinds of stimuli, and design accordingly.

### Insights from Cognitive Psychology & Behavioral Economics

The Nobel Prize-winning cognitive psychologist [Daniel Kahneman](https://en.wikipedia.org/wiki/Daniel_Kahneman) was one of the idols of my CogSci cohort. He, along with the late [Amos Tversky](https://en.wikipedia.org/wiki/Amos_Tversky), led several breakthroughs in the field of Cognitive Psychology, rigorously and empirically demonstrating a number of human cognitive biases regarding judgment and decision-making.

One of their most well-known discoveries, "[Prospect Theory](https://en.wikipedia.org/wiki/Prospect_theory)", shows how human beings are irrational in regards to their relative evaluation of losses and gains -- they are more afraid of losing money than they are willing to take a risk to win the same amount.

![A Visualization of Prospect Theory](https://upload.wikimedia.org/wikipedia/commons/4/4e/Valuefun.jpg)

*A Visualization of Prospect Theory*

Another insight of theirs was the power of "[Framing Effects](http://goo.gl/FoMRYy)", in which a decision presented in terms of loss would be perceived and thought about differently from a decision presented in terms of gain. **In other words, a decision framed in terms of a potential loss will result in different, more conservative behavior than a decision framed in terms of a potential gain.** Thoughts about possible applications towards software design should be sparking in your head right about now.

These articulations of these ideas were groundbreaking not because they were completely novel, but that they placed existing psychological ideas on a solid empirical foundation, forcing the more quantitatively-minded economists to sit up and take notice. Prior to Kahneman and Tversky, these psychological ideas had failed to make much of an impact on rational-actor economic thinking, precisely because economists had been able to dismiss those ideas of as being insufficiently grounded in data.

Kahneman and Tversky made many more strides in the area of human heuristics (a type of thinking 'shortcut') and biases. Along the way, they were joined by an economist named [Richard Thaler](https://en.wikipedia.org/wiki/Richard_H._Thaler), **who helped develop the psychological ideas into economic ones, laying the groundwork for the field of "Behavioral Economics".** Thaler would eventually join forces with a law professor, [Cass Sunstein](https://en.wikipedia.org/wiki/Cass_R._Sunstein), to write a book called "[Nudge](http://goo.gl/VeJEOp)", in which they defend a new paradigm of policy-making, centered around the idea of using "choice architecture" to design systems and programs which help to 'nudge' people into making better choices for themselves.

In the book, they describe a number of heuristics and biases (expanding on the work of Kahneman and Tversky), with focus on applications to policy. Here are five:

- **Anchoring:** a bias where an individual uses a bit of known numeric information to estimate some unknown figure. Goes awry when the relationship between the known and unknown bits of information is unexpected, as the individual will make severely inaccurate estimations.
- **Availability Heuristic:** a bias where an individual will estimate the likelihood of some event happening based on how easily an example comes to mind, regardless of the actual odds of the event. Consider the relative odds of plane vs. car crashes -- plane crashes are much higher profile than car crashes, so many people incorrectly estimate the odds of being killed in a plane crash as being much higher than they actually are, and conversely underestimate the odds of their being killed in a car crash.
- **Representativeness Heuristic:** a bias where an individual will estimate the likelihood of some event based on recent events and immediately available data -- often causing individuals to perceive patterns where they are none. Often described facetiously as the "law of small numbers", a good example is believing that you are 'due' to win at roulette after having lost several spins.
- **Status Quo Bias:** a phenomenon where people prefer the continue whatever course of action they have begun, even when changing their behavior would be in their interest. Can be colloquially thought of as
"the power of habit", or "the persistence of defaults".
- **Herd Mentality:** the observation that people tend to do what they perceive people around them to be doing.

Acknowledging these biases, *and acknowledging that there is no such thing as truly neutral design,* Sunstein and Thaler go on to discuss a number of case studies and make a number of recommendations around designing interactions to encourage people to make better decisions. Some of their discussions include:

- **Changing the default option** for employee retirement plans to from "unenrolled" to "enrolled". In the sample case, this single change increased the rate of employees signing up for their IRA from 68% to 98% after 36 months of employment.
- **Providing a series of increasingly-complex options** for structuring investments. Employees can choose to go "fully default", "semi default", or "fully manual" in how their investments are allocated, depending on their knowledge and motivation.
- **Requiring lenders to provide an annual report** of their fee structure, in a standardized format, to enable consumers to evaluate and compare lenders. This would make it more difficult for lenders to confuse customers with byzantine fee structures.
- **Implementing "intelligent assignment" of individuals** to healthcare plans (in lieu of "random assignment"), to help ensure that people have sufficient coverage for their prescription drug needs.
- **Creating visual feedback mechanisms,** such as fuel efficiency stickers on cars and indicator lights which change based on energy usage, to encourage people to make energy-efficient choices.

As the [Ruby community](https://en.wikipedia.org/wiki/Ruby_on_rails) has long been aware, *convention over configuration* and *sensible defaults* can be powerful tools.

### Possible Applications to Software Design

Builders of software would seem to have tremendous advantages over writers of policy when it comes to taking advantage of these findings.

**First**, the feedback cycle for software is orders of magnitude faster than the feedback cycle for policy. With good [A/B testing](https://en.wikipedia.org/wiki/A/B_testing) and analytics, it is possible to measure the effects of different presentations with remarkable precision. These methods are already quite mature in the field of digital marketing -- it would make sense to apply that same knowledge to the rest of our application as well.

**Second**, software is capable of providing a much more engaging and rich experience, with multiple opportunities to offer facts and figures to help counteract the effects of the biases discussed above.

For example, if we fear that our users will shy away from placing a portion of their paycheck in a retirement account, then we can include some popup informing the user that the majority of people in their income bracket who have chosen to invest in retirement have done quite well for themselves. Including that popup (or whatever makes sense) at the moment of decision could help counteract the cognitive bias that would otherwise push the user into making a poor long-term decision.

**Third**, software can be made social, allowing us to communicate more convincingly what the user's peers are doing, helping create network effects around prosocial behavior. This has been implemented, with some success, in environmental and energy-efficiency campaigns, encouraging households to be energy-efficient by promoting the energy-efficient behavior of neighbors.

**Fourth**, software can be designed with *sensible defaults* to promote better outcomes for individuals who for whatever reason are unable to complete a signup or configuration process themselves. Incorporating user surveys and other forms of demographic analysis into the design would be critical here, to ensure that there is sufficient data to design the defaults to meet the needs of the target population.

**Fifth**, software (particularly mobile apps) can be minimally intrusive and thus powerful *habit (re)shaping* tools. One organization, [Significance Labs](http://significancelabs.org/), has already begun exploring possible applications in the context of financial applications for low-income communities, by creating tools which send automatic reminders to help reinforce good habits as people first begin using credit cards.

One example of this fifth concept in action is [MOTECH](http://www.grameenfoundation.org/what-we-do/health/motech-suite-and-platform), the Grameen initiative to create a technology platform to help impoverished countries manage their healthcare systems.

Among many features designed to help nurses and doctors collect and share patient information, MOTECH includes TAMA ("Treatment Advice by Mobile Alerts"), a feature which sends automatic alerts by SMS to patients to encourage them to take their medication and attend their clinic appointments, as well as alert nurses when patients miss their appointments. In addition, MOTECH developers have implemented checklists and other decision-support features to help ensure that workers are taking the correct steps for any given treatment.

### Looking Forward

Neuroscience research is moving quickly, and is continuously accelerating as our tools for measuring and understanding cognitive processes become more sophisticated -- and will continue to shake and influence the world of economic thinking. Our ability to collect and analyze huge amounts of data about population behavior is growing apace. Finally, our knowledge of successful implementations of socially-oriented behavior-influencing software will continue to grow as more organizations experiment with putting these concepts into practice and more data becomes available to drive further efforts.

It should be a very exciting couple of years.

