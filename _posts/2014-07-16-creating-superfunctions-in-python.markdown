---
layout: post
title: "Creating superfunctions in Python"
date: 2014-07-16 16:14:16 -0700
comments: true
categories: 
- python
- architecture

---

Last week I ran into an interesting problem while building out the ParagonMeasure backend.

Much of the work of the past two months has involved the design and implementation of a data analysis library to parse, organize, and query subject typing data. The library is nearly mature, in the sense that we can now go from a raw CSV file to a feature matrix comparing multiple subjects over time.

The problem that I'm grappling with now is the problem of integrating the higher-level functionality into our more exploratory tools. While building the library, I wrote a number of functions to allow us to easily compare various data series, experimen with various parameters and filters, and get a sense of what our data looked like. Those functions, though, were written around whatever modules I had managed to complete *at the time*, with little thought to forwards-compatibility. Inevitably, as new and more complex functions were written and our means for representing our data evolved, the older exploratory functions stopped working with the new data representations. These functions were deprecated, new functions were written to work with the *new* modules, and the library kept growing.

<!--more-->

Eventually, we arrived at a structure in which we encapsulated all of the knowledge needed to calculate a specific *feature* out of a larger dataset into something called a "Feature Function", a function capable of taking in some intermediate data structure, filtering it, analyzing it, aggregating it, and packaging it for assembly into a feature matrix. Adding features to our analysis became a matter of writing a new Feature Function according to the spec, and adding that function to `feature_matrix()`.

I was pleased with this convention. There are a number of steps that need to occur, in order, to go from raw data to a full feature_matrix. One of the toughest things about writing this library was keeping track of where in the process each function was expected to live, in order to know how that function needed to receive input and package output to play nicely with the other functions. The Feature Function convention meant that every new feature could start from the same place, perform some unique analysis, and package the results into a standard format.

It worked, for a while. But a challenge emerged when I was asked to go back to some earlier exploratory functions and use them to generate some new graphs, using the new data. The Feature Functions were written to exist in a particular place in the analytical flow, and now I was being asked to generate plots of arbitrary feature functions with arbitrary parameters; in essence, to use an API which I hadn't built.

The easiest thing to do would have been to gut the feature functions and duplicate a lot of their behavior elsewhere, in a new environment where I could control the parameters that I needed to to generate the exploratory plots. But I desperately wanted to avoid this. I find duplicating code to be upsetting; it's a form of technical debt that I can almost never justify. The second-easiest thing to do would have been to write new exploratory functions which accepted an egregious number of essentially redundant arguments, in order for them to re-create the environment that the Feature Functions expect. That would have been suboptimal, as the exploratory functions (designed to facilitate speedy development) error-prone and unpleasant to use. The third option was to make the Feature Functions very general -- let them accept essentially arbitrary data, and give them the ability to refine the data themselves. This solution would have been terrible from an efficiency and optimization perspective, resulting in an unacceptable amount of duplicate work.

Whatever my solution was, it needed to make the Feature Functions more easily plugged into exploratory functions, without sacrificing the efficiency of their primary use. I wanted a DRY solution that was easy to use -- **I wanted to be able to pass my Feature Functions into arbitrary *new* functions, and have them just know what to do.**

I realized that I wanted these Feature Functions to have *knowledge* about their own requirements (beyond the behavior they define), so that functions to which they are passed can *recreate* the environment that the Feature Functions expect to be executed in.

Enter **function attributes**. Python allows you to assign arbitrary attributes to a function, in the same way that you can assign attributes to any object (which is unsurprising -- functions are first-class citizens, objects, in Python).

My preferred syntax looks something like this: 

```python

def PAOFFSET(unigrams, df=True, agg=True, metrics=['O0']):
    unigrams = clean(unigrams, metrics)
    analysis = unigrams['ND_Offset']
	...
    return analysis 
PAOFFSET.q = 1
PAOFFSET.trait = 'ND_Offset'

```

In this case, the `PAOFFSET` function has been given two attributes. The first, `q`, represents the size of the QGram that this function expects to recieves as an argument (in this case, one, creating unigrams). The second, `ND_Offset`, refers to the column in the data that this function is designed to analyze.

Regarding syntax, you'll note that the function attributes are defined *after* the close of the function definition. This is because the attributes are not *executed* in any way with the function, but are rather properties of the function *as an object*. So, they are assigned to the *function object* at the soonest possible point -- immediately after the function is defined.

Normally, this function would be called only after the subject's data had been processed to extract the desired rows. With these attributes, however, it is now possible to drop `PAOFFSET` into some arbitrary function and provide that function with the knowledge to recreate the environment that `PAOFFSET` expects. This is a good solution, to my mind, because it keeps `PAOFFSET` optimized for it's main use inside the feature_matrix() function, while allowing for unexpected and exploratory uses of that same feature.

An additional feature, much more mainstream, was the addition of a number of new keyword arguments (or kwargs**!!!!!!!, as the cool kids call them). These kwargs essentially activate or deactivate parts of the Feature Function to allow for more control over the output (allowing for different levels of indexing and aggregation for different circumstances).

So. Function attributes + keyword arguments =  superfunction. You might think for a moment that this sounds a lot like the concept of a Class. *Nope. Superfunction.*