---
layout: post
title: "Introducing Talmud"
comments: true
categories: blog
tags:

- economics
- governance
- measurement
- javascript
- machine-learning

---

It is with a mix of excitement and trepidation that I present [Talmud](http://talmud.ai), a recent undertaking self-styled as a "collaborative art project" exploring identity. Why "Talmud"? Because the name evokes the idea of a stream of learning, with every participant increasing the knowledge of the whole.

I.

The seed of Talmud was sown in the Winter of 2012, when I was living in Jerusalem during one of the Gaza conflicts. Rockets were literally flying overhead, and the dialogues playing out over the internet were tense. It seemed that much of the vitriol fell along the lines of identity. Amongst Jews, some felt their Zionist identity came first (in which Israel should take a hawkish defender militaristic stance towards Palestine); amongst others, their Humanist identity (in which Israel should take a more dovish diplomatic stance). For others their Jewish identities came first, and so they did not take a side, not wanting to undermine their communal relationships.

I remember thinking at that time that most of us are a little bit of all these things: part hawk, part dove, members of one or another community. We have many identities, but in different contexts some are more salient than others, leading to contextually-specific conflict when those identities differ. Wouldn't it be helpful if people could indicate that although in this setting one identity came first, there was more there? Some way to indicate that while there was a basis for disagreement and conflict, there was also a basis for coming-together and reconciliation? Some way to say **"I am an X first, and a Y second"?**

That was the idea; I envisioned people being able to generate badges and displaying them on their social media profiles. Of course, being a dilletantish twenty-three year old, nothing came of it. In the intervening years, more examples of these types of conflicts came to mind. Consider the American Civil War, pitting "brother against brother, father against son". Here, political identity trumped the ostensibly powerful familial identity. Consider the McCarthy Era, in which people were often forced to choose between their professional and their political identities: most chose the former. Consider another example from Jewish culture: the film "Fiddler on the Roof", in which the protaganist rejects his daughter after she marries outside the faith, placing religious identity above familial.

Ultimately, we are all multi-faceted and have many identities: child, friend, lover, colleague. In addition to the high-profile conflicts mentioned above, we make these choices **implicitly** every day as we try to balance our personal and professional lives: balancing friend and colleague, parent and professional. We make these choiced implicitly, beneath the surface and accessible to understanding via our actions. What if there was a way to make these choices explicit, to facilitate our understanding of ourselves and each other? What if we could answer, empirically, the old question of whether we are fundamentally the same and our seperateness an illusion, or whether our differences run deep and the road to coexistence needs be arduous?

II.

Addressing the question of identity empirically is challenging, in that our subject matter is highly subjective: "who am I?" Conveniently, I wrote my [master's thesis](http://kronosapiens.github.io/blog/2017/02/06/thesis.html) on the very topic of measuring subjectivities. As much as Talmud is the realization of an idea several years old, it is also an expression of theory and algorithms developed much more recently.

Talmud (and the thesis on which it draws) is based on the notion of "pairwise preference": given two options, you choose one (or potentially neither). The benefit of pairwise preferences are twofold. First, it is an efficient and robust way to measure something subjective: you either like A better than B, B better than A, or you can't decide. Second, pairwise preferences are amenable to many types of mathematical and computational analysis, allowing us to derive powerful and highly interpretable insights from simple data.

For instance, Talmud users can answer the following questions:

1. What are my most important identities (as percentages of a whole)?
2. How similar or different are my identities to those of another group?

Other questions we could potentially answer:

1. How strong or flexible are my preferences overall?
2. Are identities being presented at the right level of abstraction (such as "Musician" instead of "Pianist")?

One nice thing is that the theory behind Talmud is more general than the question of identities. For example, Talmud could be trivially adapted to the following use cases:

1. Participatory budgeting by **local government** ("Parks", "Police", "Roads", "Schools", etc.)
2. Interest group formation at a **co-working space** ("Hiking", "Crafting", "Music", "Board Games", etc.)
3. Roommate matching in a **housing cooperative** ("Clean", "Social", "Quiet", "Food", "Space", etc.)

The first and second example makes use of the ranking analysis, the second and third make use of the similarity analysis. I'll note that these ideas are not new: the use of pairwise interactions to derive rankings is a standard technique in machine learning (being the core idea behing Google's original PageRank algorithm), and the use of pairwise preferences as a survey tool was done a number of years ago by [AllOurIdeas](http://www.allourideas.com), a great project and direct inspiration behind this work. The use of pairwise preferences to determine *similarity*, however, is not something I have seen elsewhere (although it very well may have been done before).

All said, my hope is that Talmud will find application as a flexible, efficient, and reliable instrument for measuring and analyzing subjective preference. An ambitious hope to be sure, but not an impossible one.
