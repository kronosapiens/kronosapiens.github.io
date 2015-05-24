---
layout: post
published: false
title: "Setting up an IPython development environment"
date: 2014-06-16 08:03:47 -0400
comments: true
categories: blog
tags:
- python
- development-environment

---

The biggest challenge I had in moving from Ruby to Python was developing a good development workflow. Things like organizing projects, debugging code, and writing tests took a *long* time and were pretty annoying for the first few weeks, as I hunted around for models and best practices to guide my own work.

For those of you new to programming, having a good workflow is important because it determines the speed and ease with which you can develop software. It will shape how often you end up writing tests; how rigorous you are in hunting for edge cases; how meticulous you are in keeping things organized. Without a good workflow, developing software is a slow and frustrating process.

In the interest of helping other junior Python developers, I'll describe the three main aspects of my Python workflow, including the tools and processes that I've adopted to aid my work.

*Full disclosure: I use the IPython interpreter for my work, and so I'll only guarantee the techniques I'm going to describe to work for that interpreter. The vanilla Python interpreter has some different behaviors and less functionality, and not all of the setup can be ported directly over.*

<!--more-->


## 1. File Organization

An early challenge in setting up a project of more than a single file is figuring out how to organize your files and how to make sure your files know about each other.

### a. Structure

The first issue, that of organizing files, is a stylistic one. Different people will recommend different best practices (the Ruby on Rails framework is known for being very opinionated in this regard). Wherever you can, I would recommend you try and stick with convention. Odds are high that other developers will try and onboard themselves to your project some day, and the easier you make it for them to figure out where things are (by using file structures similar to what they've seen before), the happier they'll be.

For my project, I've chosen to go with three top-level folders containing a mix of python files (also known as 'modules') and data storage directories. This is what I'm working with:

{% highlight java %}
backend/
	modules/
		__init__.py
		subject.py
		...
	data/
		devices/
		raw/
		subjects/
	notes/
	tests/
		subject.py
		...
	.gitignore
	README.md
	scripts.py
{% endhighlight %}

In this structure, the majority of the codebase lives in the `modules/` directory. My test files live, unsurprisingly, in `tests/`, while my non-python data files (project-related CSV files, pickled pandas objects, etc) live in the `data/` directory. My notes and other non-code bits of text go in the `notes/` directory. `.gitignore` and `README.md` are git-related, and, finally, `scripts.py` is where I put any development scripts that I write to speed up the development process (but which won't make it into production).

### b. Relative Imports



https://docs.python.org/2/tutorial/modules.html#packages
http://legacy.python.org/dev/peps/pep-0366/

## 2. Testing

### a. Unittest

Python comes bundled with a unit testing framework called Unittest. The syntax for a Unittest test file is as follows:

`# test_file.py`

{% highlight python %}
from some_module import thing
import unittest


class TestThing(unittest.TestCase):

    def setUp(self):
        setup_variables = thing.do_something()

    def test_can_do_something(self):
        answer = thing.method_one(setup_variables, other_argument)
        self.assertEqual(answer, expected)

    def test_can_do_some_other_thing(self):
        something = thing.method_two(arg_a, arg_b)
        answer = thing.method_three(something, setup_variables)
        self.assertTrue(answer)

if __name__ == '__main__':
    unittest.main()
{% endhighlight %}

There are multiple ways to run this test:

`python -m tests.subject`

`%run tests.subject`

### b. Running the Tests & Module Autoreloading

Now that your tests are written, you have a few options for running them. The simplest is to type `python -m test_file` into the terminal. This will run the file with the `__name__` variable set to `__main__` (which is what you want). The tests will run, Unittest will print out a report (with details on the results and information about any errors), and you'll be dropped back off in the terminal.

This is a fine method, but

## 3. Debugging

### a. `pdb.set_trace()`

Python comes standard with a debugging library called pdb (short for, I'm assuming, 'Python DeBugger'). You use it by adding `import pdb` to the top of a module, and use it by copy/pasting `pdb.set_trace()` into your file. Whenever `pdb.set_trace()` is reached when your file is run, your interpreter will pause execution and drop you into that exact moment in the program, giving you a command line and access to all the current variables.

For those of you familiar with `pry` and `binding.pry` from Ruby, this is essentially the same exact thing.

My preferred debugging workflow (assuming you've enabled module autoreloading in IPython) is to throw `pdb.set_trace()` into whatever part of the program I'm currently investigating, running my test file, and letting the test file take me to the line in question. It's a 6-keystroke loop (click on line / newline /paste `pdb.set_trace()` / switch to terminal / up arrow (to recover command to run test file) / enter), and it's the fastest one I've found.

### b. `%run -d some_file`

An alternative debugging

