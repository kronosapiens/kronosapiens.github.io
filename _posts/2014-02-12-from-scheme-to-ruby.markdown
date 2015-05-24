---
layout: post
title: "From Scheme to Ruby"
date: 2014-02-12 07:34:47 -0400
comments: true
categories: blog
tags:
- ruby
- scheme
- programming-languages

---

From the opening of [Structure and Interpretation of Computer Programs, Chapter 4: "Metalinguistic Abstraction"](https://mitpress.mit.edu/sicp/full-text/book/book-Z-H-25.html#%_chap_4):

> It's in words that the magic is -- Abracadabra, Open Sesame, and the rest -- but the magic words in one story aren't magical in the next. The real magic is to understand which words work, and when, and for what; the trick is to learn the trick.
And those words are made from the letters of our alphabet: a couple-dozen squiggles we can draw with the pen. This is the key! And the treasure, too, if we can only get our hands on it! It's as if -- as if the key to the treasure is the treasure!

> John Barth, Chimera

Most people, when they start to program, pick a language that people actually use. C. Java. Python. Ruby.

Me? My first language was Scheme. A dialect of LISP, Scheme is a functional programming language -- in which there are no objects, and every procedure begins with a function call and ends with a return value. There are no "for" or "while" loops, and all higher functionality is achieved through clever applications of recursion and base cases.

<!--more-->

Consider the fib function, which returns the nth Fibonacci number:
<pre>(define (fib n)
  (if (&lt;= n 2)
      1
      (+ (fib (- n 1)) (fib (- n 2)))))</pre>
Lines 2 and 3 represent the base case -- the first two digits of the fib sequence, which are both 1. Line 4 contains the recursive calls -- initiating two more instances of the same fibonacci function, being called on the two fibonacci numbers immediately preceding n. The function continues until each fib instance returns 1 (as they all must), and the 1s are all added together, creating the nth fibonacci number.

Scheme's syntax is spartan -- an open paren initiates a function  call, and the closing paren indicated the end of the arguments. <strong><em>Always</em></strong>. Functions were nested inside of functions, the return value of the latter becoming the argument to the former. Data structures? Bah. We had to build them ourselves, abstracting away from our basic tools to create new techniques of working with information.

Consider the Scheme implementation of "map" (a procedure so beautiful I <a href="http://archive.dailycal.org/article.php?id=106973">wrote a column</a> about it):
<pre><code>(define (tree-map f tree)
  (cond ((null? tree) null)
        ((pair? tree)
         (cons (tree-map f (car tree))
               (tree-map f (cdr tree))))
        (else (f tree))))</code></pre>
Scheme is the programming equivalent of whole wheat bran. Syntactic-sugar free.

Why would anyone learn this language? Where the hell was I?

Turns out, Scheme is the language of choice in  Abelson and Sussman's landmark computer science textbook <em><a href="https://mitpress.mit.edu/sicp/full-text/book/book.html">Structure and Interpretation of Computer Programs</a>. </em>In their opinion (and in the opinion of my CS61A professor, <a href="http://www.cs.berkeley.edu/~bh/">Brian Harvey</a>), Scheme is an optimal language for teaching programming  because it encourages (or, perhaps more accurately, forces) students to think with precision about the structure (and interpretation) of their computer programs.

Think with precision we did. Having to build everything from the simplest tools (arithmetic operators and some stone-hammer-caliber selectors), we developed an iron grasp of the Scheme language. We had to learn our data structures backwards and forwards, because exploiting the quirks in their underlying implementation was the only way we could get them to do anything interesting. Lists were implemented by daisy-chaining long links of pairs,  the second element consisting of nothing more than a pointer to the first element of the second pair. We had to learn exactly how variable assignments flowed through various environmental scopes, and exactly how every character would be interpreted.

People laugh at Scheme these days, calling it obsolete (which it may be) and irrelevant -- but it forced you to get really intimate with the interpreter, and to think hard about structure. Near the end of the semester, we built a Scheme interpreter from scratch... in Scheme. That was a trip.

In a sense, when you work in Scheme, the lines between programming and philosophy blur.

Moving to Ruby has been a mixed blessing. At first, I had reservations about the language's forgiving interpretation. Coming from a language where there was exactly one way to do something, the TMTOWTDI nature of Ruby seemed to invite carelessness and ambiguity. Closely duplicated functionality? "Most likely" interpretation? Something about it bugged me.

As I've worked with the language more, though, I've come to admire the openness of the language, and the speed and power that the flexibility allows. Programming in Scheme was slow, because we spent much of our time debugging syntax. Building so much from first principles meant that bigger projects involved substantially more complexity, and were ultimately more limited. In Ruby, you can just blaze forward, thinking less about the minutiae of interpretation, and focus more on the big ideas that you're trying to cast into substance. I may wax nostalgic about the precision and discipline of Scheme, but I would rather program in Ruby any day.

Do I feel that my training in Scheme is serving me well? Absolutely. Unlike most of the programmers in that Berkeley classroom, I came in with zero experience. Scheme was my first language -- my native language -- and my approach to program structure shows it, I think. I'm very attuned to the structure and behavior of data types, am  curious about lower-level interpretation and algorithmic efficiency, and think often about strategies for breaking open logical problems. At the same time, I'm comfortable abstracting away from primitive functions and thinking in terms of the interactions and relationships among larger constructs, and reflecting on things like the ontological distinction between "nil" and "undefined".

Whether these are traits cultivated by Scheme, though, or are simply the universal traits that distinguish programmers from the rest of society, is an open question.

Shifting to a higher-level, object-oriented language is exciting -- I recognize clearly the advantages of these tools, given the abundance of processing power at our fingertips. Entering the world of programming and web development, there's no where else I'd rather be. Part of me, though, will always have a soft spot for that high-minded, didactic, and elegant language: Scheme.