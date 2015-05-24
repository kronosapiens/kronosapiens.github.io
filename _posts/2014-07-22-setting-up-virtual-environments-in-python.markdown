---
layout: post
title: "Setting up Virtual Environments in Python"
date: 2014-07-22 15:38:01 -0400
comments: true
categories: blog
tags:
- python
- devops

---

There comes a time in every young developer's life when they realize that they need to start programming like a grown-up. This is when they learn how to use virtual environments.

A virtual environment is basically like a small clubhouse in your computer that's a little bit isolated from everything else. Files in that clubhouse only really know about other files in that clubhouse; they couldn't care less about what's outside, what's outside doesn't really know much about them. It's a kind of isolation that is frowned upon when it occurs on University campuses, but is quite essential when it comes to writing production software.

Why? Because the world of code is a fickle, perpetually shifting place, with updates and changes happening constantly. You update things all the time; you're never quite sure what's going to change, and when. Version 1.2 might work a little bit differently from 1.2.2, and you can never be quite sure if something you've written for one will work for the other. Further, you're using 1.2, but maybe your colleague is still stuck on 1.0 (sad, I know). If she pulls your code and tries to run it, it'll throw approximately eight thousand bugs.

*Does that sound relaxing to you?*

<!--more-->

Enter virtual environments. With a virtual environment, you pick exactly what version of what packages go inside, and it's easy for someone else to re-create that environment on their own machine.

I'm in the process of moving the ParagonMeasure backend into a virtual environment, in preparation for building out the Django application which will bring it to life. The rest of this post will follow the process of setting up the environment.

## Installation & Creation

First, install virtualenv, the virtual environment library:

`sudo pip install virtualenv`

Easy enough. Now, create a directory for all your environments to go. This can be separate from the files meant to be run in the environment.

I created a top-level directory in my `code` directory called `environments`, where I plan on keeping all of the virtual environments I create for any of my projects.

{% highlight java %}
code/
	personal/
	projects/
	work/
	environments/
{% endhighlight %}

Now, let's actually create an environment.

`virtualenv -p python --no-site-packages env_one`

You should see some output that looks like this:

{% highlight bash %}
Running virtualenv with interpreter /usr/bin/python
New python executable in env_one/bin/python
Installing setuptools, pip...done.
{% endhighlight %}

You may be wondering about those options I passed. The `-p` flag specifies which version of Python to use to create the environment. Odds are you'll be fine without it -- I did a somewhat wonky install of the Enthought IPython Distribution and made some sort of default, so virtualenv kept crashing until I explicitly said to use regular old `python`.

By default, virtualenv will look in the active virtual environment for a package, but will fall back on any global installs if it isn't found. The `--no-site-packages` option tells virtualenv to only use the packages you install in that environment, and not to look in the global folders for it if it isn't found. I like this option because it means that I have to be explicit about every package that I'm using; I want to avoid a deployment where I realize that I've actually been relying on some obscure package I installed two years ago and completely forgot about.

Alright! We now have our very own virtual environment! Let's take a look at what we've made:

{% highlight java %}
code/
	environments/
		env_one/
			bin/
			include/
			lib/
			.Python

{% endhighlight %}

The `/bin` directory contains the binaries, like `pip` and `python`, which you'll actually be running when you use this environment. It also contains an executable python filed called `activate`, which we'll talk about in a second.

The `/include` directory contains a directory called `python2.7/`, which contains a bunch of header files (`.h`) which I don't understand.

`lib/` contains `/python2.7`, which is where all the goodies live. When you install new packages into this virtual environment, they'll end up in `/lib/python2.7/site-packages`. That'll be where your applications running in this environment will look first.

Here's what's inside `site-packages` to start:

{% highlight java %}
site-packages/
	_markerlib/
	pip/
	pip-1.5.6.dist-info/
	setuptools/
	setuptools-2.6.dist-info/
	easy_install.py
	pkg_resources.py
{% endhighlight %}

Pretty bare-bones, huh?

# Use

Now that we have our environment, how do we use it?

In general, we use our virtual environment by calling the binaries installed inside of it -- these binaries know to look in the virtual environment before the global environment, and so anything called with those binaries will be called *inside* of the virtual environment.

There are two ways of doing this. One is the boring way, the other is the cool way.

The boring way is to explicitly state the path to the virtual env binary. Say you had `somescript.py` in the `environments/` directory, and you wanted to run it inside of your new virtual environment. You could run it by typing the following:

`env_one/bin/python somescript.py`

This tells the shell to look in `env_one/bin` for a python executable and use it to run somescript.py, instead of whatever executable would've been found if you had typed `python somescript.py` and the shell had gone romping around the `$PATH` looking for it.

So that's the boring way.

The AWESOME way is to use the built-in `activate` method, as follows:

`source env_one/bin/activate`

This will do some magic and change your `$PATH` variable to point to the virtual environment *before anything else.* Further, you can `cd` around your hardrive and call files from anywhere without "leaving" the virtual environment. You also get a cool prompt, which I think is the best part:

{% highlight bash %}
(env_one)[16:25:01] environments
ƒ:
{% endhighlight %}
(the ƒ is my own flavor)

You can "leave" the environment by entering the `deactivate` command, which will restore the `$PATH` variable and put you back in your global environment.

## Installing Packages

Now, let's figure out how to install new packages. Out of the box, a virtual environment is pretty bare-bones:

{% highlight bash %}
[16:46:59] environments
ƒ: source pm_app/bin/activate
(pm_app)[16:47:07] environments
ƒ: python
Python 2.7.5 (default, Mar  9 2014, 22:15:05)
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named pandas
>>> import numpy
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named numpy
>>> import matplotlib
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named matplotlib
>>>
{% endhighlight %}

Heartbreaking.

We're going to talk about installing packages in a second, but first let's zoom out for a sec and look at how the `$PATH` is specifically changing when we change environments.

Here's python's `sys.path` in my global environment:

{% highlight python %}
Python 2.7.5 (default, Mar  9 2014, 22:15:05)
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> import pprint
>>> pprint.pprint(sys.path)
['',
 '/Library/Python/2.7/site-packages/pip-1.5.6-py2.7.egg',
 '/Library/Python/2.7/site-packages/xlrd-0.9.3-py2.7.egg',
 '/Library/Python/2.7/site-packages/openpyxl-2.0.2-py2.7.egg',
 '/Library/Python/2.7/site-packages/jdcal-1.0-py2.7.egg',
 '/Library/Python/2.7/site-packages/nose-1.3.3-py2.7.egg',
 '/Library/Python/2.7/site-packages/pandas-0.14.0-py2.7-macosx-10.9-intel.egg',
 '/Library/Python/2.7/site-packages/ipdb-0.8-py2.7.egg',
 '/Library/Python/2.7/site-packages/ipython-2.1.0-py2.7.egg',
 '/Library/Python/2.7/site-packages/gnureadline-6.3.3-py2.7-macosx-10.9-intel.egg',
 '/Library/Python/2.7/site-packages/pyzmq-14.3.1-py2.7-macosx-10.6-intel.egg',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/$PYTHONPATH',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python27.zip',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-old',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC',
 '/Library/Python/2.7/site-packages']
>>>
{% endhighlight %}

Here's the same thing, inside of my virtual environment:

{% highlight python %}
Python 2.7.5 (default, Mar  9 2014, 22:15:05)
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> import pprint
>>> pprint.pprint(sys.path)
['',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/jobs/paragon/backend',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/$PYTHONPATH',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python27.zip',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python2.7',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python2.7/plat-darwin',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python2.7/plat-mac',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python2.7/plat-mac/lib-scriptpackages',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/Extras/lib/python',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python2.7/lib-tk',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python2.7/lib-old',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/env_one/lib/python2.7/lib-dynload',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac',
 '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages',
 '/Users/kronosapiens/Dropbox/Documents/Development/code/environments/pm_app/lib/python2.7/site-packages']
{% endhighlight %}

Notice how the all the entries pointing to `/Library/` are totally gone, and the first entries are all pointing towards the directory containing my virtual env? That's how the magic happens.

Ok, back to installing packages.

We're using pandas and numpy pretty heavily at ParagonMeasure, so we need to get those bad boys installed ASAP.

Let's try the obvious:

{% highlight bash %}
(env_one)[16:57:33] environments
ƒ: pip install numpy
Downloading/unpacking numpy
  Downloading numpy-1.8.1-cp27-none-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.whl (12.0MB): 12.0MB downloaded
Installing collected packages: numpy
Successfully installed numpy
Cleaning up...
(env_one)[16:58:14] environments
ƒ:
{% endhighlight %}

Well, gosh.

{% highlight python %}
Python 2.7.5 (default, Mar  9 2014, 22:15:05)
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>>
{% endhighlight %}

Let's take a look in our `env_one/lib/site-packages` folder and see if anything looks different.

{% highlight bash %}
site-packages/
	_markerlib/
	numpy/
	numpy-1.8.1.dist-info/
	pip/
	pip-1.5.6.dist-info/
	setuptools/
	setuptools-2.6.dist-info/
	easy_install.py
	pkg_resources.py
{% endhighlight %}

WELL HOW ABOUT THAT.

Another way of looking at your packages is through the `pip list` command:

{% highlight bash %}
(env_one)[17:22:45] environments
ƒ: pip list
numpy (1.8.1)
pip (1.5.6)
setuptools (3.6)
wsgiref (0.1.2)
{% endhighlight %}

## Duplicating your environment

So, you've gotten your virtual environment set up just the way you like it. All the versions are right, your tests are passing, the birds are chirping. How do you create this environment somewhere else?

Via a requirements file. You can create one by entering the following:

{% highlight bash %}
(env_one)[17:22:45] environments
ƒ: pip freeze > requirements.txt`
{% endhighlight %}

This will write a text file containing all of the packages and versions installed in that environment, in a special format that pip can re-interpret later. It'll look something like this:

{% highlight bash %}
(env_one)[17:29:17] environments
ƒ: pip freeze
numpy==1.8.1
wsgiref==0.1.2
{% endhighlight %}

You can recreate that environment elsewhere by entering the following (assuming you've activated that other environment):

{% highlight bash %}
(env_two)[17:22:45] environments
ƒ: pip install -r requirements.txt
{% endhighlight %}

You should see pip go ahead and start installing any missing packages. You can edit requirements.txt directly to add packages or change version numbers. Just know that If you delete a package from requirements.txt, virtualenv *won't* uninstall it when you run `pip install -r requirements.txt`.

There you basically have it. Virtual environments are kind of like the magical adulthood of programming, where you can exert basically total control over your world (and make other people's lives easier to boot).

See the full documentation over at the [official site](https://virtualenv.pypa.io/en/latest/virtualenv.html).

Shout out to Jamie Matthews' [excellent post](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/) covering much of the same ground (which helped me quite a bit).

## Postscript

The ultimate test. I've created an environment called `pm_app` and have installed only the packages that the ParagonMeasure backend should require. I'm about to `cd` back into the main repository and run the test suite...

{% highlight bash %}
(pm_app)[18:06:23] (master*) backend
ƒ: pip list
backports.ssl-match-hostname (3.4.0.2)
certifi (14.05.14)
matplotlib (1.3.1)
nose (1.3.3)
numpy (1.8.1)
pandas (0.14.1)
pip (1.5.6)
pyparsing (2.0.2)
python-dateutil (2.2)
pytz (2014.4)
setuptools (3.6)
six (1.7.3)
tornado (4.0)
wsgiref (0.1.2)
(pm_app)[18:07:27] (master*) backend
ƒ: py.test
============test session starts ============
platform darwin -- Python 2.7.6 -- py-1.4.20 -- pytest-2.5.2
collected 77 items

logs/test id_outliers.txt .
logs/test_outliers.txt .
logs/test_subject_outliers.txt .
tests/test_analyzer.py ............................
tests/test_device.py ....
tests/test_parser.py ....
tests/test_session_parser.py .............
tests/test_subject.py .......................
tests/test_visualizer.py ..

============ 77 passed in 45.14 seconds ============
{% endhighlight %}

YES!