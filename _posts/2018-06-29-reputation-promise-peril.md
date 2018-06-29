---
layout: post
title: "Reputation Systems: Promise and Peril"
comments: true
categories: blog
tags:

- reputation
- blockchain
- economics
- governance

---

## I. Introduction

When dealing with unfamiliar people, places, and companies, reputation can be powerful. Having a good reputation oneself will lead others to treat us more favorably, and we are more willing to deal with people and business which are themselves well-reputed. The role and importance of reputation in markets has been known by economists since at least the 1970's, with George Akerlof famously defining the ["Market for Lemons"](https://en.wikipedia.org/wiki/The_Market_for_Lemons), describing how a market can fail when participants cannot properly gauge the quality of the offerings.

Historically, much of reputation has been implicit, qualitative, and socially embedded: we retain other's reputations in our memories and learn them through our own experiences or by discussing with others. Companies embark on public relations campaigns to build goodwill with their customers.

Sometimes, reputation can been made explicit and quantitative: a notable example being the ubiquitous credit score, which condenses our financial reputation to a single number, bringing benefits to the financially stable and consequences to the rest. Other examples are the credit rating systems such as those offered by Moody's and S&P, which evaluate and rate securities (with some success and a number of [high-profile failures](https://en.wikipedia.org/wiki/Subprime_mortgage_crisis)).

In the last two decades, firms have emerged which seek to leverage new technologies and data to more accurately rate and evaluate the business and people of the world. Companies like Foursquare and Yelp seek to establish reputations for businesses based on the wisdom of the crowd, while OnDeck, Lemonade, and the like aim to determine accurate credit worthiness by ingesting myriad traces of our digital identities. Sharing economy services like Uber and AirBnB encourage us to rate our interactions, helping us to find the best (and avoid the worst) cars to ride in and homes to stay in.

None of these methods are perfect and a quick internet search will [surface](https://www.inc.com/magazine/20100201/youve-been-yelped_pagen_3.html) [much](https://qz.com/1244155/good-luck-leaving-your-uber-driver-less-than-five-stars/) digital ink spilt in their critique. Yet this project seems likely to continue, and on an increasingly large scale: in the past year, China has begun to roll out a ["social credit system"](https://foreignpolicy.com/2018/04/03/life-inside-chinas-social-credit-laboratory/) which extends the idea of a credit score to encompass more and more facets of life: our behavior in traffic, volunteer hours, and the like.

Many see dark clouds on the horizon. This mood is most famously captured by the now-classic Black Mirror episode ["Nosedive"](https://en.wikipedia.org/wiki/Nosedive). This episode, set in a futuristic society in which every personal interaction is rated from one to five, tells the story of a woman who experiences personal ruin while engaging in an ill-fated attempt to boost her rating.

The remainder of this essay will take up the question of reputation systems, their characteristics, and the problems they seek to solve in an attempt to understand the promise and peril of such systems, and to discern what kinds of reputation, in what contexts, may help us to better navigate and thrive in the world of the future.

## II. Peril

Before turning to the promise of reputation systems, it is prudent to consider where other systems have failed. Understanding the failure of past systems will help us to discern design principles for the future.

Here, we will compare the fictitious world of "Nosedive" with the reality of Uber ratings, discuss the early experiments of China's social credit system, and briefly mention the rating products of Foursquare and Yelp.

**Both "Nosedive" and Uber make prominent use of 5-star ratings.** The key difference between them, however, is that Nosedive's fictional app combines ratings for *every* interaction into a single score, while Uber's ratings are highly specific, concerning the limited interaction between a rider and a driver. Human beings are deep and complex creatures, with different relationships to different people. To distill our value and worth into a single number is to both deny the complexity of the individual and guarantee shallow and invidious comparisons. In the case of Uber, however, such a score can be defended on the grounds that it is highly *specific*: someone can meaningfully be said to be a better or worse driver or passenger of a car.

The first thing, then, is to distinguish between some sort of *global* or *general* reputation and a task-specific one, with the latter being more meaningfully captured by a single number. Note that there are always shades of nuance and complexity: even the act of driving a car has many dimensions (reaction to traffic conditions, car maintenance, and so on), but a single number can get us most of the way there. Put another way, the *benefit* of the rating can be argued to outweigh the *cost* (there is always some cost to measuring anything).

**Now, what of China's social credit system?** It is an ambitious, country-wide effort being implemented jointly by many local governments and agencies. There is no "single" system: rather, different towns and cities are experimenting with slightly different systems. To hear the reports of citizens in these different locales is to receive valuable insights.

Listening to these citizens, we hear that social credit systems which seek to simply enforce the law (traffic violations, etc) are well received. This is in large part due to the lack of trust Chinese citizens have in the government courts. In a country with weak rule of law, a social credit system which steps in for the judiciary is welcome. In other cases, where officials have ambitions for social credit to encompass all facets of human character, the system is less welcome. Jurisdictions which attempt to track volunteering hours, charitable donations, and the like place distorted expectations on their citizens. A case study in [Goodhart's law](https://en.wikipedia.org/wiki/Goodhart%27s_law), this type of system creates perverse incentives, replacing human relationships with rigid and quickly-counterproductive policy.

What can we take from the experiment in China? First is that people will welcome a reputation system which limits itself to objective, agreeable standards of conduct. To forego any reputation system out of fear of a dystopian outcome is to run into the arms of another darkness: fraud and corruption. The second is that while some simple behaviors can be measured numerically, higher level understandings of goodness and value need to be treated with more care, lest we create more problems than we solve. Complex phenomena require more complex representations and measurements: it may be that some things are best left unmeasured, rather than measured poorly.

**Finally, let's consider the local search services provided by Foursquare and Yelp.** These products allow people to submit numeric and text reviews of bars, restaurants, and the like, and determine ratings for these venues using various proprietary algorithms (full disclosure: I was previously a machine learning engineer at Foursquare). While these companies provide useful services, they are not without their drawbacks. First, the subjectivity of the reviews invites skew and bias: Yelp in particular is known for inviting quite hostile reviews. Second, and more subtly, in reality there is no "bar", there is only "me at the bar". [Happyfun Hideaway](https://foursquare.com/v/happyfun-hideaway/518fed68498e67e8b8c705b0) is my favorite bar in New York, but the hipster-chic aesthetic isn't for everyone. I don't particularly like [Employee's Only](https://foursquare.com/v/employees-only/41e46880f964a520d41e1fe3), but it's "better", ratings-wise. Assigning every venue a single number paints only a partial picture.

## III. Promise

What then to do? The first thing to recognize is that different problems will call for different types of reputation systems.

For **concrete, specific skills**, a single numerical reputation could work well. [Colony](https://colony.io/), a blockchain startup, is taking this approach, developing a reputation system in which participants earn reputation within a taxonomy of skills and specialties. If I write a well-received blog post, I can receive reputation as a "writer". If I write some code to speed up our testing, I earn reputation as an "engineer". The incorporation of a skills taxonomy allows for striking a balance between specificity and generality and allowing for earned reputation to be put to use, for example to weight votes (full disclosure: I am currently employed by Colony as an engineer).

For **higher-level aspects of our personality and character**, however, numerical representations will fail. Numbers beg to be gamed, and so here we should prefer systems in which there is no way to "win". To understand how we might approach this type of reputation, it will pay to take a leaf out of the psychologist's book. Since the 1980's, the ["Big Five"](https://en.wikipedia.org/wiki/Big_Five_personality_traits) model of personality traits has been a common (if imperfect) tool to assess individual personality. In this system, each person's personality is seen as a basket of five trait dimensions (specifically, "openness", "neuroticism", "conscientiousness", "agreeableness", and "extraversion"). As each trait is a dimension, or dialectic, there is nothing inherently "better" or "worse" about being highly agreeable, extroverted, and so on compared with the opposite. Conscientious individuals are more diligent and hardworking, but also stubborn: in contrast, people low in conscientiousness are more flexible and spontaneous, but can be unreliable. In one setting, one might be preferable, in another setting, the other. The essential difference, compared to a single 1-5 scale, is that no position on the scale is better or worse, only different.

Personality and character are tricky issues, and the question is far from solved even today. To develop our sense of possibility, it is worth taking a quick tour of some "artistic" approaches to personality: specifically, the classic Dungeons & Dragons [alignment system](https://en.wikipedia.org/wiki/Alignment_(Dungeons_%26_Dragons)) and the [Enneagram](https://en.wikipedia.org/wiki/Enneagram_of_Personality).

Dungeon & Dragons is a classic game in which players take the role of adventure heroes and explore various fantasy worlds. A major aspect of each character is their "alignment", defined as a position on two axes: the "Lawful/Chaotic" axis and the "Good/Evil" axis. A character can be Lawful Good (a soldier, for example), Chaotic Good (a revolutionary leader), Chaotic Evil (a common criminal), Lawful Evil (a rapacious business leader), and so on. As alignment exists along two axes, or dialectics, no one position can be better or worse than another: only different. We have the freedom to decide, based on the situation (and ourselves), what type of alignment is most suitable.

The Enneagram is a popular personality system which divides people into nine "types", each type being associated with a set of fears, desires, strengths, and weaknesses. As with the other personality systems described, the essential feature is that no type is "better" or "worse" than another, only different.

For **inter-personal and inter-item compatibility**, a third approach is called for. The challenge here is that different people like different things. Someone I find amusing you might find annoying. A restaurant you hate I could love. While you could argue that the flexible personality types described earlier could be used here ("put two extroverts together", etc), it is worth thinking what other options exist. There is much research in the social science (and more recently, machine learning) literature on predicting the compatibility of a single person-item or person-person matching. A common theme in these approaches is to take a large dataset of interactions (for example, individual movie reviews, or whether two roommates like each other) and to extract a set of high-level traits which can be used to predict the success of new interactions (such as new movies or new roommates). While the specifics of these approaches is beyond the scope of this essay (you can learn more [here](https://datajobs.com/data-science-repo/Recommender-Systems-[Netflix].pdf) and [here](http://jmlr.csail.mit.edu/papers/volume9/airoldi08a/airoldi08a.pdf)), the essential takeaway is that no potential movie or roommates is inherently good or bad, just good or bad *for you*.

One could imagine building a roommate-matching system which asks participants to give a simple thumbs-up or thumbs-down as to whether they would live with a given roommate again, and use this to infer implicit community memberships ("partier", "neat freak", "chiller", and the like), and match people based on whether they would likely be compatible. One advantage of this approach (as opposed to one where people self-evaluate on these categories) is that it provides a stronger signal (based on actual experience) and arguably avoids some self-perception biases.

## IV. Conclusions

The aim of this essay was to review the idea of reputation and rating systems, and to argue that while such systems *can* be immensely useful, they must be developed with care. In particular:

- Numerical scores are appropriate only when they point to **specific** skills and competencies.
- Personality is multifaceted and dialectic: there should not be "better" or "worse", only "different".
- What one person likes someone else might dislike: the viability of a pairing should be a function of what is being paired.

For those of us living in dense urban centers, it is common to hear people describe feeling "alone in a crowd". While we are surrounded by people, they are strangers to us. Many of us lack the support infrastructure to navigate relationships in a transient world; this leads to loneliness. We must exercise caution in our personal and professional dealings to avoid being scammed, while people with quiet integrity run the risk of being overlooked in favor of the loud. All of this leads to friction, cost, and pain. Appropriate reputation and rating systems can help us navigate and thrive in our ever-expanding world, while poorly-designed systems can cause problems bigger than they sought to solve.

The continued development of such systems is inevitable; the task of building them well falls to us.
