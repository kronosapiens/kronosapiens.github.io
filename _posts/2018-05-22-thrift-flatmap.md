---
layout: post
title: "Scala's Thrift-Flatmap Pattern"
comments: true
categories: blog
tags:

- programming
- scala
- thrift

---

## I. Introduction

Working with Foursquare's machine learning stack was a great opportunity to see how a mature organization handles data at scale. While not a Google or a Facebook in terms of data size, Foursquare nonetheless ingests millions of data points per day, and runs these data through myriad data pipelines to power their various products, further increasing the amount of derivative data to work with.

Foursquare has a permissive engineering culture, in which individual contributors (in coordination with their teammates) are given liberty to add or extend existing datatypes in order to solve their problems at hand. On its face, this might seem like a big risk: a loose swarm of engineers continually modifying shared data definitions could only lead to disaster. But it is not so. Through some clever infrastructure and design decisions, the engineering team was able to achieve robustness and resiliency in their systems, while at the same time giving individual engineers significant latitude in solving their particular technical problems.

This essay will discuss one noteworthy piece of this solution, dubbed the "Thrift-Flatmap" pattern.

## II. Thrift

[Thrift](https://thrift.apache.org/static/files/thrift-20070401.pdf) is an open-source project (originally developed at Facebook, now governed by Apache) which allows for the language-agnostic definition of data types. In essence, Thrift provides two things:

1. A DSL (domain-specific language) for defining arbitrary data types (or "structs").
2. A set of code generation tools for working with these structs (serializing and deserializing) in your language of choice.

The goal of Thrift is to allow a company to define data types separately from the code in which they are used, allowing Python code and Scala code (for example) to work with the same data. Using Thrift, a company could write an API server in Scala, for example, to handle requests coming from their users, savaing the results in the results to some shared data store (such as HDFS, the Hadoop Distributed File System) as a Thrift struct. Later, someone could read these Thrift structs into a Python notebook to perform some analysis.

Here is an example Thrift struct, defined in `my_struct.thrift`:

```
struct MyThriftStruct {
	1: optional string requestId,
	2: optional i32 value
}
```

The `optional` denotes that the field does not need to be set for the serialization/deserialization to occur (this will become relevant later).

Here is a brief pseudocode illustration of the desired language interoperability:

```
# Bash

thrift gen --python --scala my_struct

... later ...

// Scala

import company.Api
import thrift.Thrift
import thrift.gen.my_struct.MyThriftStruct

val typedDataSequence: Seq[MyThriftStruct] = Api.handleRequests()

Thrift.write(typedDataSequence, 'data.dat')

... later ...

# Python

import pandas as pd
from thrift import Thrift
from thrift.gen.my_struct import MyThriftStruct

dataList = Thrift.read('data.dat', MyThriftStruct)

pd.DataFrame(dataList).value.mean()

```

We see here how the Scala process generated some typed data, which it wrote out using Thrift's Scala-specific writer. Later, we read that same data into a Python process using equivalent Python-specific reader. This is made possible by Thrift's language-agnostic binary storage format, which all languages can read and write.

## III. Scala, Options, Flatmap

So that's Thrift in a nutshell. Now, how does Thrift enable the relatively smooth coordination of multiple teams, particularly in a strongly typed Scala environment? The answer is through the strict us of `optional` fields, and Scala's `flatMap` operation.

In the context of a large, fast-moving company, the use of `optional` fields is essential. First, incoming data itself is subject to tremendous variation (data comes in from a variety of sources, under a variety of conditions -- different devices, different versions of software, etc), making it difficult to guarantee the presence of any particular field. Second, data are always changing: if a new version of iOS allows for the gathering of gyroscopic information, we might want to add a new `gyroscope` field to our struct.

Now, different teams are responsible for different services, each of which operate on overlapping sets of data but are deployed at different times. If team A adds a new field to a shared Thrift struct, we don't want team B's service to break. Each service needs to keep running in a shifting environment: achieving this means that services need to be able to:

1. Ignore fields which are present in the data but they aren't yet aware of (if the struct was updated before the service), and
2. Skip over fields which are absent in the data but the service is aware of (if the data is incomplete)

Thrift's `optional` fields allow services to handle ever-changing structs without choking. It's worth asking, though, what `optional` means in a Scala context. To understand this, we need to briefly discuss Scala's idea of an `Option`.

Scala is a strongly-typed language, meaning every value has a specific type, and every function needs to return a value of a certain type. This enables very helpful compiler debugging and optimization, and makes code easier to read and maintain. There are cases, however, where we can't guarantee that a function will return a value of a certain type (for instance, if a function depends on some external data I/O which may fail). In these cases, Scala provides the idea of an `Option`. An `Option` is a "wrapper-type" which wraps around another of Scala's types. So we have `Option[Int]`, `Option[String]`, and so on. An `Option[Int]` is essentially a type which can be any `Int`, or `None`. This allows for Scala programmers to account for uncertainty in their code: any function which returns an `Option` is communicating a measure of uncertainty about what will happen.

Under the hood, an `Option` can be thought of as a sequence of zero or one elements (zero elements means `None`, one element means whatever the type is). Now, When reading a Thrift struct into a Scala environment, the Thrift reader will interpret every `optional` field as an `Option` (sensibly). This can be cumbersome, however, as in order to work with any of these data, a consumer of these data will need to check every field to see if the value is set or not. Enter `flatMap`.

Flatmap is a standard Scala operation on sequences, in which a `map` operation is followed, sensibly, by a `flatten` operation, resulting in a single-level sequence of elements. Notably, if the `map` operation results in a `None` value, the `flatten` operation will simply omit it.

```
Seq[Option[Int]](Some(1), Some(2), None, Some(4)).flatMap(x => x)
>>> Seq(1, 2, 4)
```

In order to read in Thrift structs with optional fields, we simply `flatMap` over them, extracting the value of each field using a for-comprehension. Each line of the for-comprehension extracts the value of the option. If any field is empty, then the for-comprehension will yield `None`. If all are present, then it will yeild a tuple of (non-`Option`) values:


```
val dataSeq: Seq[(String, Int]) = Thrift.read('data.dat', MyThriftStruct)
	.flatMap(struct =>
		for {
			requestId <- struct.requestIdOption
			value <- struct.valueOption
		} yield {
			(requestId, value)
		}
	)
```

It is useful to think of this in terms of functions and guarantees. Prior to the flatmap, we have essentially a struct of optional values, which may or many not be present. This type of data is very hard to analyze, as we know nothing about the information these data contain. After the flatmap, we have guarantees about the data we are working with. In the context of a fast-moving company, the `flatMap` can be seen as providing a kind of semi-permeable filtering membrane: everything before the `flatMap` is a somewhat vague unknown, subject to all of the shifting forces of the world outside (software and hardware changes, internal service changes, and so on). After the `flatMap`, we have guarantees about the data we are working with, allowing that specific team to define and solve the problem at hand. Afterwards, they output their own data, which will be consumed by another team in the same fashion.

It is worth highlighting that this "semi-permeable membrane" is achieved via a coordination of two ostensibly unrelated components. The first is a flexible data representation, and the second is a language-specific mechanism for mapping over data. What is remarkable is the way that the two combine to provide an essential functionality, enabling teams to work with a great deal of autonomy without needing to worry about remaining in constant synchronization around shared data types.

## IV: Conclusion

Allowing for individual- and team-level autonomy while ensuring system-wide stability is difficult, but important to achieve in order to create a flexible and responsive engineering organization. Foursquare was able to achieve this by leveraging a specific interaction of open-source tools (the Thrift project) and language-specific features (Scala's flatmap), which combine to create an effective mediation layer in between individuals and teams and the engineering organization at large.
