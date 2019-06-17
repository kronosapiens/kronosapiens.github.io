---
layout: post
title: "Aragon, DAOstack, Colony, Moloch"
comments: true
categories: blog
tags:

- governance
- blockchain

---

*In which we compare and contrast the essential approaches of four significant Ethereum DAO projects.*

## Prelude

What is a DAO? Here, we take as an ([imperfect](https://blog.ethereum.org/2014/05/06/daos-dacs-das-and-more-an-incomplete-terminology-guide/)) definition something simple: "a censorship-resistant means to coordinate the deployment of shared resources towards a shared objective". The simplest DAO, by this definition, would be a multi-sig wallet, in which individual members can withdraw paltry sums and many members together can withdraw significant sums.

While a multi-sig may be sufficient for a group of friends on a backpacking trip, it quickly becomes apparent that for more ambitious objectives requiring the coordination of more resources, additional mechanisms are necessary. How permeable should the boundaries of the organization be? How much influence should any individual have? How can individuals be protected from the bad behavior of others? How easy or difficult is it to participate?

For a certain type of person, these questions are irresistible, and it no surprise that many significant projects have emerged in recent years seeking to answer these questions. People frequently ask about the ways in which these projects are similar and different from each other; this essay is a step towards an answer.

*This commentary is based on my familiarity with these projects and their technical documentation, much of which I have read, as well as conversations with teammates from the various projects.*

## Aragon

> "Freedom to organize"

[Twitter](https://twitter.com/aragonproject) (71.2k followers) -- [Solidity repo](https://github.com/aragon/aragon) (created 3/2017)

Arguably the most high-profile DAO project, Aragon has achieved mindshare an order of magnitude larger (in terms of Twitter traction) than the other projects discussed here. Named after Aragon, one of Spain's 17 *comunidad autónoma*, or autonomous communities, Aragon's rhetoric and positioning is couched in the language of boundaryless freedom and unstoppability.

In the view of the Aragon team, the problem with organizations in their current form is their subjugation to the capriciousness of their real-world jurisdictions: kleptocratic governments, biased judicial systems, and the like. If organizations could be freed from these jurisdictions, then they would be able to reach their full potential.

Technically, Aragon's most noteworthy achievements are arguably their [permissioning](https://hack.aragon.org/docs/acl-intro.html) and [transaction forwarding](https://hack.aragon.org/docs/forwarding-intro) systems, designed to allow a very wide range of modules to be safely connected together. These tools are impressive: the permissioning system can, [for example](https://hack.aragon.org/docs/aragonos-ref.html#parameter-interpretation), grant access only up to a particular block number or condition access on the response of some oracle; their forwarding system is based on [a bespoke scripting language](https://hack.aragon.org/docs/aragonos-ref.html#evmscripts-1), `evmScript`.

Rather than build a product around a specific decision-making mechanism, as the other projects discussed do, Aragon has instead focused on developing a secure and general *backbone* for building organizations *in general*. One one hand, this is very appealing: by leveraging the foundation built by the Aragon team, end users are able to compose organizations to meet their specifications, with a fraction of the effort. On the other hand, one can ask whether "just putting it on the blockchain" is really the way to go. What is perhaps surprising about Aragon is, for such a visionary project, they remain pointedly agnostic with regards to organizational form and decision-making mechanisms. While many associate the term "DAO" with some flavor of non-hierarchichal, decentralized decision-making, some Aragon teammates have stated explicitly that it doesn't matter what the organizations built with Aragon look like -- for all they are concerned, one could build an autocratic Apple or Microsoft using Aragon and be in line with the project's goals.

An open question is whether the de-emphasis on mechanism in favor of a generalized modularity will benefit or hurt Aragon in the long run. As they say, "if nothing changes, nothing changes". As mentioned above, the Aragon's team focus is on bringing organizations into uncensorable cyberspace. However, it is possible that in truth it is not capture by jurisdiction, but rather our antiquated decision-making mechanisms (such as pass/fail voting on arbitrary strings of text) which are keeping organizations from rising to meet the challenges ahead. That said, Aragon's emphasis on modularity will likely make it easier for them to build out a developer ecosystem and add support for novel decision-making mechanisms down the road (once they are proven elsewhere), and there are already three separate teams (Autark Labs, Aragon Black, Aragon One) working on exactly this.

## DAOstack

> "An operating system for collective intelligence"

[Twitter](https://twitter.com/daostack) (5.3k followers) -- [Solidity repo](https://github.com/daostack/arc) (created 9/2016)

While slightly lower profile than Aragon, DAOstack has been steadily racking up wins, most recently as the platform of choice for the (assuredly non-derivative) [dxDAO](https://dxdao.daostack.io/). Unlike Aragon, DAOstack's messaging explicitly values *decentralized decision-making*, and so the project places greater emphasis on solving [the problems inherent](https://medium.com/daostack/decentralized-governance-first-principles-1fc6eaa492ed) with decentralized decision-making at scale. As one would expect from two PhDs in theoretical physics, their theory is strong.

In the view of the DAOstack team, organizations with decentralized and broad-based decision-making processes are more *resilient* (an inherent good), but making decisions on an unbounded sequence of pass/fail proposals is too cognitively burdonsome to *scale* to large numbers of participants and proposals. With large numbers of proposals, it will be difficult for participants to know which proposals are most deserving of attention. With large numbers of voters, it is difficult to motivate participants to take the time to consider proposals which may not be personally relevant. For DAOstack, "just putting it on the blockchain" without engaging with these more fundamental *human* questions will get us exactly nowhere.

Technically (and unsurprisingly), DAOstack's most noteworthy achievement and crown jewel is the "holographic consensus" cryptoeconomic mechanism for efficiently and reliably approximating group decisions using small numbers of participants (a hologram, after all, is an image in which every part contains all of the information of the whole). The mechanism functions by incentivizing a network of "predictors" to place bets on whether a proposal will pass or fail; the predictions are then used (along with a number of other rules) to emphasize or de-emphasize proposals and modify the quorum requirements necessary for the proposal to pass (for example, it may take fewer total voters to approve a highly boosted proposal). Functioning well, an organization using holographic consensus can scale to arbitrary numbers of proposals and arbitrary numbers of participants without sacrificing either decision-making speed or quality.

The DAOstack team has rightly identified the problem of attention as one of the most fundamental challenges confronting humanity in the 21st century, and while others write thinkpieces and wring their hands, this team has put forward at least part of a solution. For the DAOstack team, the holographic consensus mechanism is the missing piece for unlocking performant, decentralized organizations. However, we will need to see how well the ambitious mechanism works in practice. In particular, the mechanism assumes the independence of the predictors and the voters (["you cannot buy a decision, but you can buy it into consideration"](https://medium.com/daostack/holographic-consensus-part-1-116a73ba1e1c)), yet we can imagine situations in which voters may be "swayed" by the predictions, especially if the predictors present themselves as authoritative experts. If this line proves too fine, the approximations may cease to be reliable, threatening the central promise of the project.

## Colony

> "A platform for open organizations"

[Twitter](https://twitter.com/joincolony) (8.2k followers) -- [Solidity repo](https://github.com/JoinColony/colonyNetwork) (created 4/2017)

Unlike Aragon and DAOstack, which make their focus the enabling of vote-driven management of an organization, Colony (my employer, forgive my bias) has chosen to focus on the quotidian. With "permissionless by default" as their rallying cry, Colony focuses heavily on mechanisms which, to the extent possible, eliminate the need for voting in daily operations, and let people just "get shit done", with an eye towards enabling the global digital workforces of the future.

While both Colony and DAOstack take as axiomatic the value of enabling decentralized organizations, their approach to creating them is somewhat orthogonal. In the DAOstack case, scale is achieved by using holographic consensus to accelerate a *synchronous* process of *discrete* pass/fail decision making. In the Colony case, on the other hand, scale is achieved via an *asynchronous* process of *continuous* financial decision-making (using an org-chart-like domain tree), allowing different domains of the organization to conduct their business relatively autonomously.

Technically, Colony's biggest achievement is the constellation of mechanisms which leverage *time* to enable the permissionless allocation of resources (note: for the full experience, you are encouraged to narrate every sentence mentioning "time" in an Alan Watts voice). Time plays a role in Colony in two critical ways: reputation earned decays over time (implemented via an off-chain reputation mining process), and funds are allocated continuously as a function of time (as opposed to discrete pass/fail methods). The more reputation which backs a proposal, the faster it is funded, but even someone with little reputation can slowly claim resources. The acquisition of reputation is driven by work (as opposed to pass/fail proposals to allocate reputation), which makes reputation a carrier of market information (much in the same way prices are).

More subtly, the incorporation of time mechanics in the operation of a Colony *animates* the organization and makes it an entity with which individuals interact. Rather than being a static object which requires synchronous effort to overcome inertia (via a voting process), in a Colony *resources are always moving*, and the key interaction then becomes one of asynchronously influencing the flow of resources over time.

Scholars of organizational design [in particular](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3356774) seem excited about Colony: the use of work-driven, time-decaying reputation in funding decisions promises to mix the best of top-down hierarchy (experienced leaders have outsized influence), with the best of independent decision-making at the periphery (leveraging local knowledge). However, it remains to be seen whether the lack of a central coordinating point will lead to organizations which are nonetheless able to work effectively towards collective goals, and further, for what types of organizations this model represents a competitive advantage. Colony takes as its patron saint the image of the ant colony, in which independent ants, unbeknowenst to any of them individually, are engaged in staggering collective enterprise. Colony hopes that its mechanisms can emulate for humans the same stigmergetic processes which evolution has bequeathed to ants; yet, as certain [dilletantish cultural commentators](https://kronosapiens.com/2013/07/25/unlocking-the-magic-of-studio-ghibli/) have observed, the capacity to appreciate novelty is incremental at best. Of the projects discussed here, Colony is the only one yet to have a mainnet launch (although one is imminent), and so much of Colony's promise has yet to be proven.

## Moloch

> "Moloch whose mind is pure machinery"

[Twitter](https://twitter.com/molochDAO) (2.6k followers) -- [Solidity repo](https://github.com/MolochVentures/moloch) (created 7/2018)

By far the youngest project described here, Moloch, brainchild of Ethereum's [Romantic hero](https://en.wikipedia.org/wiki/Romantic_hero) Ameen Soleimani, has burst onto the scene and acquired significant traction in recent months. Unlike Aragon, which has moral roots in the struggle against bad government, and DAOstack and Colony, which set themselves against the dysfunction of human organization, Moloch's foundations are solidily rationalist and cryptoeconomic, rooted in, among other things, the trauma of TheDAO.

Moloch can be described succinctly as an experiment in coordination mechanism, seeking to create the "minimum viable process" which allows people to allocate shared resources towards a shared goal, while *aggressively* minimizing the vectors for attack and abuse, both technical and social.

Technically, Moloch achieves this in two ways, both of which cleverly mix the computer and social layers. The first is by leveraging time (remember the Alan Watts voice) to create "rails" which focus the attention of participants on exactly one collective decision. Proposals are considered in sequence, on a timer, and malicious participants are unable to overwhelm the participants with many decisions. Further, the decisions themselves are similarly constrained: each proposal includes a credit of some amount of tokens (the "tribute") and a debit of some amount of influence ("voting rights"). An unknown candidate may offer a large tribute for small influence, while a known and respected candidate may offer small tribute for large influence. By creating a mechanism with a single-minded focus, Moloch has make it likely that at least *something* will get done well.

The second technical achievement was the innovation around "rage quitting", in which participants are able to exit (with their portion of the resources) if they are unhappy with the decisions of their colleagues. This innovation creates a disincentive for malice and implicitly places social pressure on participants to remain aligned on the organization's goals.

The ease of participation and the guarantees of security and safety, along with the clever memeing on the part of the Moloch team has made Moloch the *dao du jour*, with Ethereum heavies Vitalik and Joe Lubin among the members. An open question for Moloch is whether the highly specific and limited interface will prove sufficient for coordinating around the ambitious goals they have set for themselves. At present, Moloch seems to see itself more as an improvement over existing grants committees, and less as a new foundation for an operating organization -- it remains to be seen how far the Moloch mechanism can go.

In an important sense, Moloch can be seen as fundamentally a self-determining, plutocracy-resistent reputation system, in which members with influence choose to allocate influence to new members, and reputation just happens to be convertible into money. Inasmuch as reputation systems are important building blocks for other, more complex systems, it may well be that Moloch finds application as an important piece of other puzzles.

## Conclusion

Here we present a succient and high-level overview of four Ethereum DAO projects, and attempt to get at their *essential* points-of-view and notable technical innovations which form the basis for their value. Each project has substantial achievements under its belt, and it will be exciting to see which hypotheses are proven out in the years head.
