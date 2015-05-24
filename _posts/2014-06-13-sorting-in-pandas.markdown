---
layout: post
title: "Sorting in pandas"
date: 2014-06-13 09:20:25 -0400
comments: true
categories:
- pandas
- data structures
- python

---

For nearly a month now, I've been working as a lead software engineer at ParagonMeasure, a health technology startup developing passive telemonitoring applications. It's pretty exciting stuff; not at all what I expected to be doing right out of Flatiron, but in many ways more in line with what I'd like to be doing in the long run (extracting insights from large and novel datasets).

I've spent most of the last few weeks writing the library which will power the backend of our software -- parsing raw user data and performing various kinds of analysis on the resulting data structures. The library is built on [pandas](http://pandas.pydata.org/), the popular data analysis library written by Wes McKinney. I've become quite intimate with pandas over the last few weeks -- designing a library from scratch means that I have to make a number of design decisions about data structure and flow, and since I've been pushing myself to avoid technical debt and design as modularly and forward-thinkingly as possible, I've been hitting the [books](http://shop.oreilly.com/product/0636920023784.do) pretty hard.

A particular challenge has come from the question of how to index and sort user data. User data comes to us with several attributes, including various time stamps and category tags. One of the strengths of pandas is the flexibility with which it lets you set and modify indices -- including allowing for hierarchichal indexing to mimic higher-dimensional datasets -- leaving me with a lot of choice as to what the structure should be.

<!--more-->

This freedom of choice presents problems. Given that I don't entirely know how the data will need to be filtered and analyzed as the project moves forward, I want to avoid committing to a complicated indexing system which may result in less flexibility down the road. On the other hand, I want to index the data in a way that represents their deep structure, so that there is a close mapping between pandas data selection methods and actual units of meaning in the data. Finally, in any case, I want the library to run efficiently. We will be working with medium-size datasets (a hundred thousand rows or so for the testing data), but some of the analysis will involve calculating the relationships between multiple arbitrary combinations of these rows -- so controlling computational complexity is important (keeping to O(n) vs O(n^2), for example). Further, I want to make sure that I'm choosing efficient pandas operations and avoiding expensive operations wherever possible (things like changing the index, for example, can be very expensive -- doing it once is fine, but doing it as part of a loop would be unfeasible)

As an experiment, today I'm going to checkout a new branch and attempt to change the way I've been indexing the data at a low level. I'm curious to see see three things: first, if a simpler indexing system (a single time series index, as opposed to a more complicated multi-leveled index) allows me more flexiblity in building new methods of analysis; second, if a simpler index (and corresponding decrease in indexing *resolution*) will make the data *harder* to work with; and third, whether or not I have been sufficiently modular, decoupled, and forward-thinking in my design (if this re-design proves to be impossible, then I will consider myself as having failed in designing a changeable library).

Part of this experiment will have me attempting to sort the data using various of pandas sorting methods (some of which operate on indices, and others on columns) with various indexings of the data. They each have their pros and cons, and it's important to me that I use them efficiently and effectively. To get a handle on these various methods, I'll try and describe them below.

# Sorting Methods

##[DataFrame.sort()](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.sort.html)

**Returns:** a *new* dataframe, leaving the original dataframe unchanged. If you pass the `inplace=True` flag, it will instead mutate the original dataframe (and return `None`).

Passing no arguments will cause .sort() to sort by the current index. In the case of a MultiIndex, it will sort by level 0, then further by level 1, and so on (I will refer to this behavior henceforth as a 'cascading sort').

Optional parameters:

- `columns`: accepts either a column name or a list/tuple of column names (as strings). Will perform a cascading sort based on the order of names. (Note: the function seems to also accept `column`, with no apparent change in behavior. [*Edit: `column` is deprecated syntax.*]) If no argument is passed, the function will default to sorting by the index of the specified axis.
- `ascending`: accepts either True or False. If False, will place the largest values at the top. If a list is passed to `columns`, `ascending` can recieve an equal-lengthed list to match to the columns.
- `axis`: Like many pandas functions, .slide() can operate on either rows or columns. 0 corresponds to a sort on the rows (leaving the column order intact), while 1 corresponds to a sort along the columns (leaving row order intact).

##[DataFrame.sortlevel()](http://pandas.pydata.org/pandas-docs/version/0.13.1/generated/pandas.DataFrame.sortlevel.html)

**Returns:** a *new* dataframe, with the same `inplace=True` behavior as .sort().

Optional parameters:

- `level`: accepts an integer corresponding to a level of the MultiIndex. Will perform a cascading sort *beginning with* the indicated level. The documention  states that sorting will be 'followed by the other levels (in order))', which suggests that a three-tiered index sorted by the second level (level 1) would be cascade sorted by levels 1, 0, and 2 in order.
- `axis`: same behavior as .sort()
- `ascending`: same behavior as .sort()

##[DataFrame.sort_index()](http://pandas.pydata.org/pandas-docs/version/0.13.1/generated/pandas.DataFrame.sort_index.html)

**Returns:** a *new* dataframe, with the same `inplace=True` behavior as .sort().

Optional parameters:

- `by`: accepts a column name or list of column names (seemingly analogous to the `column` parameter of .sort()).
- `axis`: same behavior as .sort()
- `ascending`: same behavior as .sort()
- `kind`: accepts the name of a sorting algorithm as a string. Options are mergesort, quicksort, and heapsort. Quicksort is default, while mergesort is the only [stable sort](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability).

It seems that .sort_index() performs an almost identical function to the vanilla .sort() function, with the additional ability to specifying a sorting algorithm.

##[Series.sort()](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.Series.sort.html)

**Returns:** `None`. Sorts the series in-place, according to the series' values (*not* the index).

Optional parameters:

- `ascending`: Same behavior as other sort functions.
- `kind`: same behavior as .sort_index()

##[Series.sortlevel()](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.Series.sortlevel.html)

**Returns:** a *new* sorted series.

Optional parameters:

- `level`: same behavior as DataFrame.sortlevel()
- `ascending`: Same behavior as other sort functions.

## Summary

I'm surprised to see such similar functionality between the `.sort()` and `.sort_index()` methods. Aside from the more advanced `kind` parameter in `.sort_index()` (which I may actually need to make use of*), and some strange quirks of naming convention, they seem to be identical.

Closing out the day's experimentation, I've successfully re-tooled my project to use a single time series index (to take advantage of pandas built-in time series selecting features), and rely on a column-based cascade sort for ordering data within single days. These changes have made it much easier to select subsets of our data, as well as to group related clusters of rows using pandas' thoroughly useful [`.groupby()`](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.groupby.html) functionality.

**since I'm not indexing down to the individual row, but rather at the level of clusters of rows, stable sorting is crucial to preserving the data.*
