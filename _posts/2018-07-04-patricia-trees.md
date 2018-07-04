---
layout: post
title: "Trie, Merkle, Patricia: A Blockchain Story"
comments: true
categories: blog
tags:

- blockchain
- data-structures
- algorithms
- trees

---

In which we tell the story of the Patricia Tree.

## I. Introduction

Spend a few days around blockchain engineers and certain words will start to sound familiar. "Merkle Tree" and "Patricia Tree" in particular will start to seem... important somehow. You'll eventually gather that these are quite essential parts of this whole blockchain thing... but why? What problems, exactly, do they solve?

You might do a quick search and stumble upon more than a few peices of #content which explain these things, but retreat upon seeing the complicated-looking diagrams. Fear not, dear reader. Here we will explain these things, not with graphs, but with story.

Where to begin? The beginning, I suppose.

## II. The Hash Table

In the beginning there was the **computer,** stretching infinitely in all directions. In fact, it's hard to say that there even *was* the computer, since existence implies absence, and there was nothing that wasn't the computer. So there was the computer, but the computer was inert. Nothing was *happening*. Boring. So the computer decided to create a **programmer.** Pop.

At first the programmer wasn't very good, but over time she got better. There wasn't much else going on at this time, so the programmer kept going, programming more and more things into the world. Animals and the like. After a while there were a lot of animals, which meant a lot of names to keep track of. This was a problem.

The programmer thought -- "how can I keep track of all of the names of these animals? I want to be able to easily look up the name I gave to each species of animal. I could write all the names down in a big list, but eventually looking up the names will get really slow. If only I had the right *data structure*".

And so the programmer created the **hash table.**

What is a hash table? For starters, its the basis of everything else that's going to happen, so we're going to talk about it for a minute. Essentially, a hash table is a type of "key-value store". This means that for a given "key" (i.e. an animal specie) you can save the "value" (i.e. the name of the animal). The main property of the hash table is that when you have a key, you can find the value *fast*, regardless of how many other items are in the hash table. In computer science terms, this is known as "constant-time lookup" and is very useful, which is why hashtables are ["arguably the single most important data structure known to mankind"](http://steve-yegge.blogspot.com/2008/03/get-that-job-at-google.html)). Here's an example:

```
>>> hashtable.set("dog", "fido")
>>> hashtable.get("dog")
"fido"
```

How do they work? To understand the hash table, we have to digress for a moment and talk the **hash function**. Hash functions are a magical secret sauce which make some amazing things possible. Hash functions are the "cryptography" people talk about when they talk about blockchains. Hash functions are legit.

What is a hash function? Fortunately, hash functions are simple to understand. They are essentially tiny machines which take in some value, shake it around for a while (imagine a bartender shaking a cocktail), and output some other crazy-looking value (a big number). Their essential properties are:

- For a given input (like "cat"), you will always get the same output (like "0x52763589")
- Two similar inputs (like "cat" and "car") should not have similar outputs. Put another way, given an output, you should not be able to guess the input.

This makes hash functions extremely useful because they let us handle sensitive information safely. Have you ever wondered how *responsible* websites keep your passwords safe? They don't store your password, they store a hash of your password. When you type in your password to log in, they take the hash of your password and compare that against what they have in their database. But if a hacker ever gets in, all they'll know is the gibberish hash of your password -- useless since they have no way of figuring out what your actual password was.

The other thing they're useful for is making hash tables. Why? Remember that the output of the hash function is a *number*. So when you hash the key, you essentially get a number telling you where to find the value. Imagine the hash table as a cabinet with 100 drawers. You `hash("dog")` and get `34` -- you go to cabinet 34 and get the name out. You `hash("cat")` and get 89 -- you go to cabinet 89. No need to look through a whole list -- you skip directly to the finish line.

Pretty cool right? Yes it is.

And so the programmer had the hash table, and for a while things were good. Great, even! But it couldn't last. Eventually, the **brogrammer** appeared.

At first things were good between them: they shared ideas, they shared code, they shared space. But eventually dark clouds appeared on the horizon. They wanted different things. The programmer was fine with a little randomness thrown into things, but the brogrammer wanted certainty, and he wasn't happy with hash tables anymore. They're "not deterministic", he said.

What did he mean? To understand this point, we'll have to talk a little more about hash functions and hash tables. The first thing to note is that the "range" of the hash function (the possible values the output can take) is very large -- depending on the computer, it can take as much as 2^256, but more typically 2^32 or 2^64 possible values. 2^32 is 4,294,967,296 -- and the others are much, much larger. Hash tables have to support this whole range, but we can't make cabinets with that many drawers -- there wouldn't be room for anything else! So behind the scenes, we do a little trick: we take the hash value *modulo* the size of the cabinet. The modulo operation (`%`) is essentially division's sidekick: it gives you the *remainder*. The nice thing about modulo is that the output (the remainder) is always between 0 and the base -- so no matter how big the input, the output can only be so big.

So behind the scenes, we make a cabinet with 100 drawers, and when deciding where to put the name of `"dog"`, we look in drawer `hash("dog") % 100`. Because the hash value is random, the remainder will still be random, just smaller. This works great, but there's a big downside: two animals might end up in the same drawer! Let's say that `hash("dog")` is `1,000,034` and `hash("shark")` is `200,034`. Different values, but both will be `34` after the modulo. So we put them in the same drawer, and we have to look through the drawer to find the dog's name. It's still fast, since there's usually only one or two names in the drawer.

So it's fine in practice, but the brogrammer's point is that the spot you put the name in is not 100% determined by the hash function you're using. Two more factors come in: the size of the cabinet, and the other animals! The size of the cabinet matters because a cabinet with 10 drawers will put both `72` and `182` in the same place (`2`), but a cabinet with 100 drawers will put them in different places (`72` and `82`). Also, you can't tell in advance if a name will be alone in a drawer, or if it will have to share with other names.

The brogrammer wasn't happy about this, but dealt with his feelings in a healthy way and went off into the mountains for a few weeks to think about alternatives. "A place for everything, and everything in its place," he kept repeating in his head. When he eventually came down, he had a new idea.

## III. The Trie

The problem, the brogrammer had realized, was that we were trying to put everything into a single huge cabinet, which could never be big enough. The solution, the brogrammer said, was to use a sequence of *smaller* cabinets. The first cabinet would give you the address of the second cabinet, the second cabinet the third, and eventually you would get to the cabinet which had the name you were looking for. You would need more cabinets (but not that many, as it turns out), and each cabinet could be quite small (maybe 16 drawers, or even 2!). Here's an example, using an 8-drawer, 3-cabinet system (which gives us 8^3 = 512 drawers total):

```
>>> hash3("dog")
0x237

>>> firstCabinet = trie.find(firstCabinetLocation)

>>> secondCabinetLocation = firstCabinet.drawer(7).contents
>>> secondCabinet = trie.find(secondCabinetLocation)

>>> thirdCabinetLocation = secondCabinet.drawer(3).contents
>>> thirdCabinet = trie.find(thirdCabinetLocation)

>>> thirdCabinet.drawer(2).contents
"fido"
```

Note that each number tells us which drawer to open, and each number means one more cabinet. The brogrammer called this system a "[Trie](https://en.wikipedia.org/wiki/Trie)" (as in re**trie**ve), and said that the beauty of it was that you didn't need to build all the cabinets at once -- you could start out with just one cabinet, and only build new cabinets the first time you needed them, wherever there was room. And while it means a little more work (opening more drawers), every name will have a dedicated drawer, always in the same place. And the brogrammer knew that no one would ever need *all* the drawers, and so most of the cabinets would never need to be built (although you can't rule it out).

The programmer looked at the Trie and agreed it was a clever idea (although it involved quite a bit more walking), and there was harmony between them.

Years passed, and a new **people** started to appear in the nearby valley. Curious, the programmer and the brogrammer journeyed over to see these people and learn about their culture. They found the people intriguing, with a curious religion revolving around the worship of a particular arrangement of carved granite blocks.

The people were quite friendly, and after meeting with some of their priests, the programmer and brogrammer learned that these people had once been warlike, but after years of conflict developed a new system of "trust" which allowed them to co-exist in remarkable peace and prosperity. The computer, they said, was only as good as the programmer, and that humans could not be trusted to program alone. These people knew of the hash table and the trie, but they had found that people would cheat: sometimes people would come in the night and change the names in the drawers; there was no way to prove that the names in the drawers were the right names. For a while these people had a warrior class who guarded the cabinets, but found that this only led to more conflict.

Eventually a number of their most skilled artisans developed the technique of carving blocks of granite; these blocks, they realized, were very difficult to carve, and so things carved into these blocks could be trusted in away that the names in the cabinets could not. It was unfeasible to carve every name into the block, however, and to carve new blocks when the names changed. What they needed, they said, was some way to carve a *signature* of the names onto the block, such that if any one name changes, the signature would change; but if the names were the same, the signature would always be the same. Eventually, one of their scientists, Ralph, developed a [solution](https://en.wikipedia.org/wiki/Merkle_tree): the Merkle tree.

## IV. The Merkle Tree

The Merkle tree behaves much like a Trie, but with a new rule: the drawers of each cabinet will not contain the location of the next cabinet, but rather the *hash* of all of the contents of the next cabinet. Separately, we keep track of the location of each cabinet (using, of all things, a simple hash table):

```
>>> hash3("dog")
0x237

>>> firstCabinetLocation = hashtable.get(firstCabinetHash)
>>> firstCabinet = trie.find(firstCabinetLocation)

>>> secondCabinetHash = firstCabinet.drawer(7).contents
>>> secondCabinetLocation = hashtable.get(secondCabinetHash)
>>> secondCabinet = trie.find(secondCabinetLocation)

>>> thirdCabinetHash = secondCabinet.drawer(3).contents
>>> thirdCabinetLocation = hashtable.get(thirdCabinetHash)
>>> thirdCabinet = trie.find(thirdCabinetLocation)

>>> thirdCabinet.drawer(2).contents
"fido"
```

Remember our hash function? Earlier we talked about hashing simple values like "dog" and "cat", but in truth you can hash anything, including other hashes or sets of hashes. What Ralph realized was that by keeping the hashes in the cabinets, you can create a "hash trail" which will change whenever any value changes (remember how websites store your passwords? Same idea). Here is how you update a value:

```
>>> hash3("dog")
0x237

### Find cabinet same as before

>>> thirdCabinet.drawer(2).contents = "rover"

### But then you start working backwards...

>>> thirdCabinetHash = hash3(thirdCabinet.drawers)
>>> hashtable.set(thirdCabinetHash, thirdCabinetLocation)

>>> secondCabinet.drawer(3).contents = thirdCabinetHash
>>> secondCabinetHash = hash3(secondCabinet.drawers)
>>> hashtable.set(secondCabinetHash, secondCabinetLocation)

>>> firstCabinet.drawer(7).contents = secondCabinetHash
>>> firstCabinetHash = hash3(firstCabinet.drawers)
>>> hashtable.set(firstCabinetHash, firstCabinetLocation)

>>> firstCabinetHash
0x375

```

Now the final value, `0x375`, is a "fingerprint" of the entire Merkle tree. You can save this fingerprint (or engrave it into a granite block), and know that if anyone changes any of the names in the drawers, the process of making the hashes will give a different result -- you'll know something has changed. Notice that this adds more steps compared to a simple Trie: you need to have a separate hashtable to keep track of locations. But what you get is *security*.

The programmer and the brogrammer walked up to get a closer look at the granite blocks, and to their surprise, on them they saw engraved a series of hashes! `0x736`, `0x264`, `0x123`, and so on, with `0x542` being the most recent. They were amazed! Nearby, they noticed some activity: one of this peculiar tribe wanted to prove that he had purchased a horse from another. He brought forward the name of the horse and his own name, set `trie.set(horse, name)` and through an elaborate ritual showed that his name, hashed with certain other names, with certain other names... voila! He arrived at `0x542`, and thus all agreed that the horse was his.

What a remarkable society, the programmer and brogrammer agreed. There was something nagging at the programmer, though. This was a small tribe -- only 512 members. As they grow, they will need a new hash function with a larger range -- thousands, millions, billions. And so updating and verifying the values in the Merkle tree will become more and more costly -- from three cabinets to five, to ten, to sixty and beyond! And for what? Most of these drawers will be empty. It seems like an expensive system, slow and costly. Surely there must be a better way? If only there was a Practical Algorithm To Retrieve Information Coded In Alphanumeric...

### V. The Patricia Tree

To gather their thoughts, the programmer and the brogrammer took a walk into the hills above the valley. "There must be some way to optimize this tree!" they thought to themselves. The brogrammer suggested they look at a few random hashes, to build some intuition:

```
>>> hash8("cat")
0x14350235

>>> hash8("dog")
0x14350762
```

Then the brogrammer got excited -- he noticed that both of these hashes happened to start with the same numbers: `14350`. With just these two entries, getting to the final drawer should only need two cabinets: one for `14350`, and one for whatever was left: `235` or `762`. This would be much faster than using eight cabinets. You could always add more cabinets later, but why make more than you need? On each drawer we tape a little slip of paper, where we write down the common prefix for that drawer. Finally, the first cabinet is actually just a single drawer.

Looking up values would go like this:

```
>>> hash8("dog")
0x14350762

>>> firstDrawerLocation = hashtable.get(firstDrawerHash)
>>> firstDrawer = trie.find(firstDrawerLocation)
>>> split(14350762, firstDrawer.commonPrefix)
(14350, 762)

>>> secondCabinetHash = firstDrawer.contents
>>> secondCabinetLocation = hashtable.get(secondCabinetHash)
>>> secondCabinet = trie.find(secondCabinetLocation)
>>> secondDrawer = secondCabinet.drawer(7)
>>> split(62, secondDrawer.commonPrefix)
(62,)

>>> secondDrawer.contents
"fido"
```

The programmer got excited -- she felt pretty good about this. It would make the algorithm a little trickier, to make sure that cabinets were created appropriately and that common prefixes are kept up-to-date, but nothing they couldn't figure out. A little more work at the beginning to set this all up would save the valley people a lot of time over the long run.

The pair sat down and worked out the details of this new system, which they called the ["Patricia Tree"](https://github.com/ethereum/wiki/wiki/Patricia-Tree). Satisfied, they descended to the valley and presented their work to the people there. They people were joyous; the slow Merkle tree had been a drag on their society. With the Patricia tree, they hoped, they would be able to advance their arts, sciences, and industry faster.

Satisfied, the programmer and the brogrammer left the valley. As they crested the ridge and began to make their way through the surrounding grassland, they heard a soft humming sound. Looking up, they saw a flying car sailing off into the horizon.

## VI. Summary

What did we learn from this completely stylistically original story?

**First**, that hash tables, tries, merkle trees, and patricia trees are all do essentially the same thing: they let you map *keys* to *values*. While there are differences between them, this is essentially what they do.

**Second**, in computer science, nothing is free (but some things are cheap). Everything has a trade-off. Hash tables are fast, but have some randomness. Tries are fully determinstic, but slower. Merkle trees have nice security properties, but use a more complicated algorithm and are slower to update. Finally, Patricia trees are faster than Tries and Merkle trees, but require an even *more* complicated algorithm.

**Third**, Patricia trees are useful for blockchains because they let you "prove" a potentially large amount of data is correct, without having to store all of that data. This is very convenient: you can have a big tree with a lot of data (such as all of the transactions in the last 24 hours), but you only have to store a few numbers (like 0x323757382) on the actual blockchain. You can keep the rest of the data on a regular database somewhere and know that no one will be able to tamper it and get away with it. Note that here the blockchain is only *part* of the system: it is co-dependent on other data stores to function.

**Fourth**, the hash function is the magical machine that makes all of this possible. The design and implementation of hash functions has been the ongoing work of computer scientists for decades, and they are very hard to get right. You should take a moment and appreciate the years of work that made this magical technology possible.
