---
layout: post
title: "Understanding Package Imports in Python"
date: 2014-07-28 15:46:23 -0400
comments: true
categories: blog
tags:
- python
- development

---

I have been having an embarassingly hard time getting a handle on package imports in Python. I'll get something working, only to have it break inexplicably when I make what seems to be an incidental change. Tests will run in one directory but not another, but then inadvertently start working, only to stop a few days or minutes later. I've tried to be methodical in investigating what changes lead to what behavior, but it's been difficult. To hopefully put this to rest, I'm going to investigate and methodically record all the behavior I can isolate regarding package imports, to hopefully make some sense of what's going on.

## PYTHONPATH

First, let's start with a project I'm calling 'backend'. Here's the file structure:

{% highlight java %}
backend/
	backend/
		__init__.py
		analyzer.py
		tests/
		__init__.py
			test_analyzer.py
{% endhighlight %}

And my `PYTHONPATH`:

{% highlight bash %}
ƒ: echo $PYTHONPATH
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/:
{% endhighlight %}

<!--more-->

So, my `PYTHONPATH` is pointing to the directory *containing* the backend package, but *not* to the backend package itself (which contains `__init__.py`).

Let's open up a terminal and play around:

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from 'backend/__init__.pyc'>
{% endhighlight %}

Very cool. Now let's `cd` into the `backend` package and see if anything changes:

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from '/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/backend/__init__.pyc'>
{% endhighlight %}

That's curious.

Let's see what happens when we remove the path to the project from our `PYTHONPATH`.

{% highlight bash %}
ƒ: echo $PYTHONPATH
{% endhighlight %}

And into Python, from `backend/`:

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from 'backend/__init__.pyc'>
{% endhighlight %}

And, from `backend/backend`:

{% highlight python %}
>>> import backend
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named backend
{% endhighlight %}

Ah. Now we're getting somewhere. So you can import a package that is within your current working directory without having that package in your `PYTHONPATH`, as a local import. From anywhere else, you'll need your `PYTHONPATH` to point to it.

To double-check, let's `cd` all the way to `/` and try to import:

{% highlight python %}
>>> import backend
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named backend
{% endhighlight %}

So, a package must be *contained* in a directory on your `PYTHONPATH` to be able to import it from anywhere other than the directory immediately above it.

To verify, let's try changing our `PYTHONPATH`:

{% highlight bash %}
ƒ: echo $PYTHONPATH
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/backend:
{% endhighlight %}
Here, we've pointed it to the package itself, not to the containing directory. Let's try importing it from `backend/`:

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from 'backend/__init__.pyc'>
{% endhighlight %}

and from `backend/backend/`:

{% highlight python %}
>>> import backend
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named backend
{% endhighlight %}

and from `/`:

{% highlight python %}
>>> import backend
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named backend
{% endhighlight %}
Makes sense. But what happens if we `cd` up one directory above `backend/`?

{% highlight bash %}
ƒ: pwd
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon
{% endhighlight %}

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from 'backend/__init__.pyc'>
{% endhighlight %}

Strange. I would have expected this import to have failed, but it imported `backend` as though it were local. Let's go up one more directory:

{% highlight bash %}
ƒ: pwd
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs
{% endhighlight %}

{% highlight python %}
>>> import backend
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named backend
{% endhighlight %}
And now it fails, as it should. My suspicion is that, since the `paragon` directory contained the `backend` directory which contained the `backend` package, python was able to look into the similarly-named directories. Let's try renaming the outer `backend` directory to `backend1`and see what happens.

{% highlight python %}
>>> import backend
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named backend
{% endhighlight %}

Ok, so that makes sense (note that renaming `backend` to `backend1` meant that the `PYTHONPATH` was no longer valid. Hence the failure meant that the local import wasn't working.)

We can verify this by playing a bit more with the `PYTHONPATH`:

From `paragon/`

{% highlight bash %}
ƒ: echo $PYTHONPATH
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend1/:
{% endhighlight %}

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from '/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend1/backend/__init__.pyc'>
{% endhighlight %}
Note that we're doing an absolute import, not a relative import, because the name of the directory and the package are no longer the same. And now changing the directory name back to `backend`:

{% highlight bash %}
ƒ: echo $PYTHONPATH
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/:
{% endhighlight %}

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from 'backend/__init__.pyc'>
{% endhighlight %}
It goes back to importing locally. **Now I understand the convention of naming directories after the packages they contain.**

## Submodules

Now, let's look at importing modules from within a package.

For a long time, I assumed that if you imported a package, you could automatically access all of the modules within the package. It took an uncomfortably large amount of time debugging testing errors that I finally realized that this wasn't the case.

Let's play around and try importing the `analyzer` module inside the `backend` package.

{% highlight python %}
>>> import backend
>>> backend
<module 'backend' from 'backend/__init__.pyc'>
>>> backend.analyzer
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute 'analyzer'
# Uh oh. But wait:
>>> import backend.analyzer
>>> backend.analyzer
<module 'backend.analyzer' from 'backend/analyzer.pyc'>
>>> import backend.analyzer as analyzer
>>> analyzer
<module 'backend.analyzer' from 'backend/analyzer.pyc'>
>>> analyzer.clean
<function clean at 0x10ffe5b90>
{% endhighlight %}
Alright. So it seems that we have to explicitly import submodules inside a package. Once a module is imported, though, we can use all of the functions that module defines.

What if we don't want to import things one-by-one? Can we use the `from module import *` on a package?

{% highlight python %}
>>> from backend import *
>>> analyzer
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'analyzer' is not defined
{% endhighlight %}

Doesn't seem like it. But what about this?

{% highlight python %}
>>> from backend.analyzer import *
>>> backend
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'backend' is not defined
>>> backend.analyzer
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'backend' is not defined
>>> clean
<function clean at 0x109ad5c08>
{% endhighlight %}

Ah! Since `analyzer` is a module, we could import all of the functions from the module, *without* importing any of their wrapper files into the namespace. *Good to know.*

## Running Tests

Now that that's a bit clear, let's take a look at running tests.

For reference, this are the import statements in the test file:

{% highlight python %}
import math
import pdb # pdb.set_trace()
import unittest
import matplotlib.pyplot as plt
import numpy as np
from backend.analyzer import *
from scripts import *
from synth import *
{% endhighlight %}

`scripts.py` and `synth.py` contain tools for generating synthetic data and mocks, feel free to ignore those for now.

First, running the test file as a simple Python script:

{% highlight bash %}
ƒ: python backend/tests/test_analyzer.py
...........................
----------------------------------------------------------------------
Ran 27 tests in 14.084s

OK
{% endhighlight %}

Ok, that worked out. Now, though, we'll try running the test using the [pytest](http://pytest.org/latest/contents.html) framework:

{% highlight bash %}
ƒ: py.test backend/tests/test_analyzer.py
============= test session starts ==============
platform darwin -- Python 2.7.6 -- py-1.4.20 -- pytest-2.5.2
collected 0 items / 1 errors

==================== ERRORS ====================
______ERROR collecting backend/tests/test_analyzer.py ____________
/Users/kronosapiens/Library/Enthought/Canopy_64bit/User/lib/python2.7/site-packages/py-1.4.20-py2.7.egg/py/_path/local.py:620: in pyimport
>           __import__(modname)
/Users/kronosapiens/Library/Enthought/Canopy_64bit/User/lib/python2.7/site-packages/pytest-2.5.2-py2.7.egg/_pytest/assertion/rewrite.py:159: in load_module
>           py.builtin.exec_(co, mod.__dict__)
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/tests/test_analyzer.py:6: in <module>
>   ???
E   ImportError: No module named analyzer
=========== 1 error in 1.66 seconds ============
{% endhighlight %}

What is this? This is the bug that has been haunting me. Usually I just delete files and change paths at random until something starts to work. This time, I decided to delete the `__init__.py` from the `tests/` directory. Why? I have no idea. YOLO. I ran the tests again and got this:

{% highlight bash %}
ƒ: py.test backend/tests/test_analyzer.py
============= test session starts ==============
platform darwin -- Python 2.7.6 -- py-1.4.20 -- pytest-2.5.2
collected 0 items / 1 errors

==================== ERRORS ====================
__________ERROR collecting backend/tests/test_analyzer.py __________
import file mismatch:
imported module 'test_analyzer' has this __file__ attribute:
  /Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/tests/test_analyzer.py
which is not the same as the test file we want to collect:
  /Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/backend/tests/test_analyzer.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
=========== 1 error in 3.16 seconds ============
{% endhighlight %}

Well... something changed at least. Investigating the error, I notice that it suggests I delete the `__pycache__` folders that have been popping up in my projects. I've set my iPython interpreter not to generate these kinds of files, but I've been dropping into vanilla Python from time to time, so I guess that's where these came from. I go ahead and delete all of these files from the project, and try running the test again:

{% highlight bash %}
ƒ: py.test backend/tests/test_analyzer.py
============= test session starts ==============
platform darwin -- Python 2.7.6 -- py-1.4.20 -- pytest-2.5.2
collected 28 items

backend/tests/test_analyzer.py ............................

========== 28 passed in 12.81 seconds ==========
{% endhighlight %}

OH COME ON. Really? This isn't the first time that `.pyc` and `__pycache__` have caused me some pain. But this is good, this is progress. Let's run the whole shebang:

{% highlight bash %}
ƒ: py.test
============= test session starts ==============
platform darwin -- Python 2.7.6 -- py-1.4.20 -- pytest-2.5.2
collected 76 items

backend/tests/test_analyzer.py ............................
backend/tests/test_device.py ....
backend/tests/test_parser.py ....
backend/tests/test_session_parser.py .............
backend/tests/test_subject.py .......................
backend/tests/test_visualizer.py ..

========== 74 passed in 25.44 seconds ==========
{% endhighlight %}

Alright! Let's try an experiment: moving the `tests/` directory one level up, so it's a *sibling* directory to the `backend` package, rather than a child. Typing this command: `mv backend/tests .` gives us this:

{% highlight java %}
backend/
	backend/
		__init__.py
		analyzer.py
	tests/
		test_analyzer.py
{% endhighlight %}

Fingers crossed. `py.test`

Error! But the same as before. Delete `tests/__pycache__` and try again. SUCCESS!! Let's commit.

Sigh. As with most thing programming, *#itsalwaysusererror*. Mind your PYTHONPATH, attend to naming conventions, ***clear out your cached files***, and you'll have a long and happy life.

## BONUS: Testing a Non-Package

Let's say you're working on a project but don't want to add it to your PYTHONPATH. It's a work-in-progress, no one else should be able to import it, what have you. Can you still import those modules to test them?

*It seems like it.*

Let's consider another project, a webapp, with the following structure:

{% highlight java %}
webapp/
	webapp/
		__init__.py
		views.py
	tests/
		test_integration.py
{% endhighlight %}

Note that this directory is *not* in my PYTHONPATH:*

{% highlight bash %}
ƒ: pwd
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/webapp
ƒ: echo $PYTHONPATH
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend/:
{% endhighlight %}

**While writing this post, I read some articles advocating for keeping trailing slashes in your PATH variables. I thought it was a good idea, so I've changed my PYTHONPATH accordingly.*

Let's try running `py.test` from `webapp/`:

{% highlight bash %}
ƒ: py.test
=============== test session starts ===============
platform darwin -- Python 2.7.5 -- py-1.4.22 -- pytest-2.6.0
collected 5 items

tests/test_integration.py ..

=============== 2 passed in 1.89 seconds ===============
{% endhighlight %}
Very cool. But what happens if we change directories?

From `webapp/tests/`:

{% highlight bash %}
ƒ: pwd
/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/webapp/tests
(pm)[18:28:44] (master) tests
ƒ: py.test
=============== test session starts ===============
platform darwin -- Python 2.7.5 -- py-1.4.22 -- pytest-2.6.0
collected 0 items / 2 errors

=============== ERRORS ===============
_________ ERROR collecting test_integration.py _________
test_integration.py:6: in <module>
    import webapp
E   ImportError: No module named webapp

=============== 1 error in 0.05 seconds ===============
{% endhighlight %}

Hmm. Can't find the package. Here are the import statements at the top of the test:

{% highlight python %}
import os
import pdb # pdb.set_trace()
import unittest
import tempfile

import webapp
{% endhighlight %}

It seems like running `py.test` from the top of the project means that the test can look for local packages from that location. Running the tests from inside the test directory means that the package has to be imported via `PYTHONPATH`.

Well... that makes sense! In the end, it all makes sense.

Further reading: [another pretty good article on imports](http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html).