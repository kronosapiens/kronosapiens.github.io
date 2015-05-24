---
layout: post
title: "The Ruby 'Tap' Method for Objects"
date: 2014-02-16 07:30:27 -0400
comments: true
categories:
- ruby
- methods

---

I've come across the "tap" method a number of times in the last few days, and I never quite understood what the purpose was.

Reading the <a href="http://ruby-doc.org/core-2.1.0/Object.html#method-i-tap">documentation</a>, it seems as though "tap" enables you to perform some intermediary within a method chain without actually changing the value passing through the chain. In other words, the value passed to tap is the same value that tap passes to the next method -- tap is unable to return anything other than what it is given.

This might make tap seem somewhat useless -- what is the point of a method that simply returns the value it is given? Quite the opposite -- tap enables you to access the value being passed through a method chain and use that method to power other actions, without disturbing or interrupting the other methods. Hence the name: tap enables you to "tap into" a method chain and perform some tangential function.

<!--more-->

Consider this function:
<pre>(1..10).map {|x| x*x }.tap {|x| puts "array: #{x.length} items long"}.join

array: 10 items long
 =&gt; "149162536496481100"</pre>
Here, we have the range of 1 - 10 being passed to map, which yields to the block which squares each number in the range, returning an array of squares. Then, that array of squares is passed to tap, which prints the statement "array: 10 items long" before passing the same array of squares (unchanged) to join, which collects the numbers into a single integer, returned as a string.

So we see how the presence or absence of the tap method has no effect on the ultimate output. It simply allows us to access the value at some intermediate point within the function chain (as opposed to accessing only the final return value), and performing some operation with it (but not upon it).

Considering this functionality, two possible uses for this method comes to mind. First, for debugging or general inspections. Tap should allow us to evaluate and print information concerning the state of the program at the time the method was called. Compare this to a tool like pry, which can only give us access to our program in between the evaluations of lines.

The second is to modify the environment in which the method chain is being executed, without modifying the method chain itself. Using tap to initialize or modify variables as part of a larger method chain seems like an interesting technique -- potentially saving a few lines of code by not having to define or modify variables elsewhere. Consider the following:

<pre>genre = Genre.new.tap { |g| g.name = 'rap' }</pre>

Compared to:

<pre>genre = Genre.new
genre.name = 'rap'</pre>

These two implementations have the exact same effect -- of creating a new Genre object and setting that object's name equal to 'rap'. The first implementation is able to fit on one line, however, by taking advantage of the 'tap' method.

At the very least, tap allows us access to a part of the program (the execution of a method chain) that we would otherwise have difficulty accessing. I wonder what other uses we might find for this tool.