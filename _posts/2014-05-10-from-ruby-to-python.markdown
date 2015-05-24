---
layout: post
title: "From Ruby to Python"
date: 2014-05-10 14:35:04 -0400
comments: true
categories: blog
tags:
- python
- ruby

---

Coming out of the [Flatiron School](http://www.flatironschool.com), my core expertise was very much in Ruby. For twelve weeks, nearly every day, from 7am to midnight, I was writing Ruby. Towards the end, I even started to [dream in it](https://twitter.com/kronosapiens/status/444809790242713600).

But Ruby is just one among languages spoken on Planet Software -- and, just as in real life, multilingualism is highly desirable. I'm in the early stages of interviewing at an *extremely cool company* which works in some of those other languages, and so I figured it would be wise to track down some figurative dictionaries and grammar guides and start learning them. First up: **[Python](https://www.python.org/)**.

Python and Ruby are very similar. They're both high-level languages designed for readability, supporting multiple programming paradigms (object-oriented, functional, procedural, imperative). From my experience and through talking with other developers, Ruby seems to be a bigger player in the web space (in large part due to the influence of Ruby on Rails), while Python is a heavyweight in the academic and research world. Alternatively, you might want to think of Ruby as leaning to the side of ease-of-use, while Python leaning to the side of speed.

<!--more-->

Below, I've noted* some of the more immediate differences between the two, which might serve as an aid to someone trying to make the hop from one language to the other.

**Everything that follows is based on my understanding of the differences between these languages. I've done my best to find sources to support my interpretation and verify my claims, but I am still quite junior as a developer, and so should not be seen as an authority on the limits or capacities of either language.*

## Terms

Ruby and Python make use of similar datatypes, but occasionally call them by different names.

A **hash** in Ruby is a **dictionary** in Python.

An **array** in Ruby is a **list** in Python.

A **class variable** in Ruby is a **member variable** in Python (and they behave differently)

## Syntax

There are some interesting different between the languages in this regard.

Ruby doesn't care about whitespace, with indentation being primarily an aid to programmers. Functions, loops, and other definitions are closed with the `end` keyword. Additionally, blocks are demarcated by either the `do` keyword, or via the use of `{ }`.

Python, on the other hand, relies on whitespace to interpret its syntax. Right indenting a line four spaces in from the line above indicates that the line is a block to be passed to the preceding function. *Left* indenting four spaces indicates the end of the function definition or block (and corresponding conditional). Additionally, Python uses the `:` to indicate the beginning of a block.

## Interpretation & Execution

Division between two integers in Ruby will output an integer, with any remainder being truncated (`11 / 3` will return `3`, for example, even though the value of 11 / 3 is 3.667). To get the more accurate answer, you must either change one of the numbers to a float (by entering it as `11.0` or `3.0`, or by calling `.to_f` on either number). In Python, division defaults to floats where appropriate. The `//` operator will give you the floor (mimicking Ruby's default division behavior).

If a function takes no arguments, then Python is similar to JavaScript in that you distinguish between desiring a function's *value* and a function's *execution* by including a `()` at the end of the function's name. So, if we have a function `eight` which simply prints the number 8, then `eight` would return the function's value (some internal Python business), while `eight()` would actually return `8`.

## Iteration

#### Mapping

In Ruby, we would iterate over some array using the following syntax:

```ruby
array_of_things.each {|element| do_stuff_to(element) }
```

or

```ruby
array_of_things.each do |element|
	do_stuff_to(element)
end
```

Which is fine. Python, however, lets us do things like this:

```python
for element in array_of_things:
		do_stuff_to(element)
```

or this

```python
do_stuff_to(element) for element in array_of_things
```

Wow!

#### Selecting & Rejecting

One of the ways that Ruby lets us filter arrays is through the `select` and `reject` methods, which requires us to pass a block which evaluates some element(s) of the array and returns either `True` or `False`. Example:

```ruby
evens = [1, 2, 3, 4, 5, 6].select { |num| num % 2 == 0 }
```

Python lets us do this via its 'list comprehension' syntax, as follows:

```python
evens = [num for num in range(1,7) if num % 2 == 0]
```

One interesting feature of the list comprehension syntax is that it allows us to modify the variable after the conditional check but before inserting it into the array. For example:

```python
evens_squared = [num**2 for num in range(1,7) if num % 2 == 0]
```

To accomplish the same in Ruby (I believe) would require us to call `map` on the results of `select` or `reject`, while Python allows us to perform both operations at once.

Of course, Python also comes with a vanilla `filter` function, which accepts a function and an object to filter:

```python
evens = filter(lambda num: num % 2 == 0, range(1,7))
```

Note the support for lambda (λ)!

## Objects

#### Inheritance

Ruby handles inheritance via the `<` operator, like so: `class Dog < Mammal`, while Python has the parent class passed on as an argument, like so: `class Dog(mammal):`

In Ruby, we access overridden methods of the parent class by simply calling `super` within the overriding method. In Python, the syntax is slightly more complicated:

```
```python
super(ChildClass, self).overriden_method(all_arguments_except_self)
```

#### Initialization

Ruby handles object initialization by calling an `initialize` method, which can take optional arguments. Python, on the other hand, expects an `__init__` method which takes `(self)` as a required argument (with other parameters  optional). Like so: `__init__(self):`. When actually instantiating an instance of the class, however, you do not pass in a value for `self` -- it seems to be passed implicitly.

*As an aside, it seems as though Python requires that `self` be passed to all class methods -- unlike Ruby, which can use `self` at any point to access the object representing the immediate environment*


#### Instance Variables

In Ruby, instance variables are created with the `@` symbol preceding the variable name (as in `@instance_var`). Ruby allows us to create getter and setter functions via the `attr_accessor`, `attr_reader`, and `attr_writer` macros. These getter and setter methods, however, simply *wrap* changes to a corresponding variable `@attribute_name`.

In Python, on the other hand, seems to *only* use getters and setters. In other words, you *define* an instance variable by setting `self.var_name = value`. You can access the variable later by calling `self.var_name`.

#### Member Variables

Ruby and Python differ in that in Ruby, class variables are *shared* between individual instances of a class (in this respect, they behave similar to constants). In Python, on the other hand, member variables's scope is limited to an individual instance. It seems as though, in practice, member variables and instance variables behave very similarly. According to [some folks](https://stackoverflow.com/questions/2714573/instance-variables-vs-class-variables-in-python), member variables are not often used, with most programmers finding instance variables to be perfectly suitable and slightly faster (further down the lookup chain).

## String Interpolation

In Ruby, we can interpolate the results of method calls into strings using the following syntax:

```ruby
"The class of this object is #{self.class}, and 5 + 8 is #{5+8}"
```

Python doesn't support this kind of in-string interpolation, however. One option is to concatenate strings and values (similar to how we construct strings in JavaScript). Another option, however, is to use the following syntax:

```python
"The class of this object is %s, and 5 + 8 is %s" % (self.class, 5 + 8)
```

Here, Python will interpret the commands being passed after the `%` operator and insert them in the place of the `%s` placeholders.

Yet another option:

```python
"The class of this object is {0}, and 5 + 8 is {1}".format(self.class, 5+8)
```

It seems as though Python will interpret the commands that are passed as arguments to `format`, and then insert them into the string based on the index numbers provided within the curly braces.

Relatedly, the equivalent of Ruby's `value.to_s` method in Python is `str(value)`.

## Testing

Writing simple tests in Python is fairly straightforward. Python comes with a built-in testing framework called unittest. Here is a [sample testing file](http://www.openp2p.com/pub/a/python/2004/12/02/tdd_pyunit.html), to give you a sense of the structure of the tests.


File: `test_file.py`

```python
import unittest

#Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

#Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.assertEqual(IsOdd(2), False)

def main():
    unittest.main(module='test_file')

if __name__ == 'test_file':
    main()
```

To set up a test file, you need to:

1. `import unittest`
2. `import` the files you want to test (in this example case, we've defined the method we want to test explicitly in the file)
3. Create the testing class (which can be called anything, but must inherit from `unittest.TestCase`)
4. Write tests. Each test name must begin with the letters `test`, or else unittest will not recognize them as tests. Writing tests in Python is similar to writing them in Rspec in Ruby. Every test can perform whatever procedures necessary for that test, ultimately ending with some sort of assertion about the value of some variable or output. Unittest provides a number of methods for this, with `self.assertEqual(arg_a, arg_b)` being the most similar to Rspec's `expect(arg_a).to eq(arg_b)`.
5. Run the test file. The test file is run with the following command: `unittest.main(module='test_file_name')`. The syntax around `if __name__ == 'test_file'` I find a little strange, but I saw it on many examples so I assume it serve some purpose I am not yet aware of.
6. To run the tests, enter `import test_file` into the Python interpreter.

And that's it! Pretty similar to Ruby, huh?


## Minutiae

#### Conditionals

Ruby uses `if`, `elsif`, and `else` for its conditional. Python uses `if`, `elif`, and `else`.

Ruby allows for both `&&` and `and`, as well as `||` or `or` (with the symbols being higher in the order of operations than the words, and thus [preferred](http://devblog.avdi.org/2010/08/02/using-and-and-or-in-ruby/) for general use). Python uses `&` and `|`, as well as the words `and` and `or`.

Ruby supports `unless` in lieu of `if not`, while Python only supports `if not`.

#### List Slicing

To access subarrays, Ruby provides the [`.slice()`](http://www.ruby-doc.org/core-2.1.1/Array.html#method-i-slice). Python has this built in to the list object, via the following syntax:

```python
list[starting_index:ending_index:stride]
```

With `starting_index` representing where in the list you'd like to begin the slice, `ending_index` being where you'd like to end the slice, and `stride` being the distance between elements you would like to select (providing a negative value for `stride` will give you the values in reverse!)

#### Printing

Ruby provides `put` and `puts` to print to the screen. `puts` automatically adds a newline (`"\n"`), while `put` does not. This means that multiple `put`s will print all to one line, unless you insert `"\n"` manually.

Python provides only the `print` command, but allows us to include a comma `,` after the argument to be printed, which will cause Python to not insert a newline. Thus,

```python
print 1, 2,
print 3, 4
```

Will output to `1 2 3 4`

## Conclusion

There are many tiny differences between the languages, but the concepts being implemented are by large part the same. If you're a Rubyist looking to transition to Python (or vice versa), then simply [staring at some code](https://wiki.python.org/moin/SimplePrograms) and tracing through the logic might be the fastest way to get you up to speed. You'll find the other language legible, and it'll be easy for you to see the differences in implementation.

Good luck! Python has been a pleasure to use so far.

For more information on moving to Python from another language, you might want to check out [this guide](https://wiki.python.org/moin/MovingToPythonFromOtherLanguages)