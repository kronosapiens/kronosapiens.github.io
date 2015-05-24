---
layout: post
title: "Understanding Contexts in Flask"
date: 2014-08-14 12:00:34 -0400
comments: true
categories: 
- flask
- web development
- testing

---

For those of you following along, you'll be happy to know that the **database** and **model** layers of the Paragon Measure web application are more-or-less built. We can fire up an interpreter and create, destroy, and interact with our data in much the same way we would when everything was done locally. This is good.

Now my work is starting to pivot over to the API side of things -- building a RESTful interface for the front-end developers who are going to be building the client-side interface.

Being a **T**est-**D**riven kind of **D**eveloper, I need to establish a good framework for testing the API as I move forwards. This means getting my head around Flask's conception of **contexts**.

<!--more-->

Before getting into the details, let's establish the purpose of contexts. From Miguel Grinberg's *Flask Web Development* (p12):

>When Flask receives a request from a client, it needs to make a few objects available to the view functions that will handle it. A good example of this is the *request object*, which encapsulates the HTTP request sent by the client.

>The obvious way in which Flask could give a view function access to the request object is by sending it as an argument, but that would require every single view function in the application to have an extra argument. ...

>To avoid cluttering view functions with lots of arguments that may or may not be neded, Flask uses *contexts* to temporarily make certain objects globally accessible.


Alright, so it seems that contexts are used to control the presence or absence of various *global variables*, so that you, the developer, can simply assume that the correct variables will be available when you need them. Given that an application can be running in multiple threads and serving multiple clients at once, I assume that this kind of context management will prove very helpful in keeping things organized.

First, let's take a look at the **application context**.

## The Application Context

An excerpt from the Flask [docs](http://flask.pocoo.org/docs/):

>One of the design ideas behind Flask is that there are two different “states” in which code is executed. The application setup state in which the application implicitly is on the module level. It starts when the Flask object is instantiated, and it implicitly ends when the first request comes in. While the application is in this state a few assumptions are true:

> - the programmer can modify the application object safely.
- no request handling happened so far
- you have to have a reference to the application object in order to modify it, there is no magic proxy that can give you a reference to the application object you’re currently creating or modifying.

>In contrast, during request handling, a couple of other rules exist:

>- while a request is active, the context local objects (flask.request and others) point to the current request.
- any code can get hold of these objects at any time.

>There is a third state which is sitting in between a little bit. Sometimes you are dealing with an application in a way that is similar to how you interact with applications during request handling just that there is no request active. Consider for instance that you’re sitting in an interactive Python shell and interacting with the application, or a command line application.

>The application context is what powers the **current_app** context local.

Ok, so looking at this, it seems that the **application context**, at least inasmuch as we'll be interacting with it, is the state of the application **after** the first request has been made (and when large configuration changes are no longer possible), but **before** a specific request has come in (at which point we should switch to the (more specific?) **request context**).

Continuing with the docs, there are **two** ways to create an application context:

1. Automatically, whenever a request context is pushed.
2. Manually, by using the `app_context()` method.

And within an application context, the function `flask.current_app` will return the current application object.* The `g` variable is also defined there.

*Not quite, apparently. `current_app` returns a proxy which *wraps* around the current app (for some reason which seem to involve words like "threads"). To get the real, bona-fide app, call `current_app._get_current_object`.

Regarding the use of an application context, the docs have this to say (emphasis mine):

>The context is typically used to cache resources on there that need to be created on a per-request or usage case. **For instance database connects are destined to go there.** When storing things on the application context unique names should be chosen as this is a place that is shared between Flask applications and extensions.

So it seems that the application context (specifically, the `g` variable) is the common resource repository for everything which needs to interact to create this application. This also implies that your views connect to your database through this `g` variable. No `g`, no db, as they say.

Now, let's move on and take a look at the **request context**.

## The Request Context

While the application context contains `g` and `current_app`, the request context contains the `request` and `session` variables -- the request-specific variables containing the information your view function will need to process it's request, while still relying on the more powerful tools made available by `g` and `current_app`.

As with the app context, a request context can be created:

1. Automatically when the application recieves a request.
2. Manually, by calling `app.test_request_context('/route?param=value)`

You'll note that, unlike the application context, the manual creation accepts an argument representing the request.

Also, important:

> Another thing of note is that the request context will automatically also create an application context when it’s pushed and there is no application context for that application so far.

This seems to make sense. Since application contexts aren't instantiated by themselves during the running of a normal application (you create them in the shell, in tests, etc), the request context would just bring a new application context along with it.

## Working with Contexts

This is the thing that's been giving me a bit of a struggle. Different examples will show the contexts being initialized and used in different ways, some with [`with`](http://effbot.org/zone/python-with-statement.htm) statements, some without.

I'll go over the examples one-by-one and try to unpack what's going on.

From the Flask [docs](http://flask.pocoo.org/docs/appcontext/#app-context):

```python
from flask import Flask, current_app

app = Flask(__name__)
with app.app_context():
    # within this block, current_app points to app.
    print current_app.name
```

From a testing example in *Flask Web Development*:

```python
import unittest
from app import create_app, db
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		Role.insert_roles()
		self.client = self.app.test_client(use_cookies=True)
	
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
		
	def test_home_page(self):
		response = self.client.get(url_for('main.index))
		self.assertTrue('Stranger' in response.get_data(as_text=True)
```

Finally, a third syntax:

```python
with app.test_client() as client:
    resp = client.get('/foo')
```
Here, we pass in `app.test_client()` in as `client`.

Poking around the [docs](http://flask.pocoo.org/docs/reqcontext/#request-context) some more, I found this clarifying nugget:

>This context can be used in two ways. Either with the with statement or by calling the **push()** and **pop()** methods.

Hallelujah! The warm light of wisdom shines upon my face.

Well, mostly. I'm not 100% confident that I understand how the Flask context stack works, but I'm getting there. There's probably some important functionality about embedding requests in each other that I'm just not quite ready for. Some day.

But in seriousness, this is a *very* helpful clarification. Some settings (such as within a function) might call for the `with` syntax. Others, such as in the shell or in the `setUp()` and `tearDown()` functions of a test suite, `.push()` and `.pop()` might be easier.

As a counterexample, let's look at some of my pre-enlightenment code. From my integration test file, `tests/test_integration.py`:

```python
from flask import request
import unittest

from webapp import app, db

class TestIntegration(unittest.TestCase):
    def setUp(self):
        app.config.from_object('webapp.config.Testing')
        db.init_app(app)
        self.app = app.test_client()

    def tearDown(self): 
        for collection in db.session.db.collection_names()[1:]: # Skip first
            db.session.db.drop_collection(collection)

    def test_root(self):
        rv = self.app.get('/')
        assert 'Hello world!' in rv.data

    def test_params(self):
        with app.test_request_context('/?name=Daniel'):
            assert request.path == '/'
            assert request.args['name'] == 'Daniel'
```

Amusingly, both of these tests passed, which made it hard for me to understand why the more elaborate setups discussed above are necessary. Here are the view functions that I was testing:

```python
@app.route('/')
def root():
    return 'Hello world! What a beautiful day for research!'

@app.route('/<name>')
def name(name):
    return 'Hello {0}! What a beautiful day for research!'.format(name)
```

Things became clear to me when I began trying to test more involved views. These two views are almost entirely self-contained -- they never access `g`, or the database, or anything. Further, in my utter ignorance, I didn't even realize that `test_params` *never actually made it to the views*. This became clear to me when I tried this:

```python
@app.route('/<name>')
def name(name):
	import ipdb; ipdb.set_trace()
    return 'Hello {0}! What a beautiful day for research!'.format(name)
```

*And I never even hit the binding.*

Truly, in the words of my favorite Roman Civ professor, the depths of my ignorance are vast and unplumbed.

Well, at least I'm figuring it out.

One thing I noticed is that I'm actually using the `request` variable in my `test_params` function -- note that I imported it at the top of the file, from `flask`. I didn't import anything else, though -- not `g`, or `session`, or `current_app`. So even though these might be in existence within the test request context I've created, I can't actually access them. This is an important point, at least for neophytes like me: these variables are flask magic, so you need to actually import them (and *also* be in the correct context) before you can access them. They don't *just appear*. This isn't Rails.

Ok, I think I may be getting close to being able to test my application like a real grown-up.

Ok, time to set a goal: to be able to retrieve a model from my database. Let's see if I can manage it.

Let's start off by defining a view function in `webapp/views.py` to display a single research trial:

```python
@app.route('trials/<name>')
def trial(name):
    trial = Trial.query.filter({'name': name}) # Mongo!
    if trial is None:
        return 'Trial not found!'
    return 'Trial found: {0}, {1}'.format(trial.name, trial.mongo_id)
```

And writing a test. For brevity, I'm truncating the two tests I included earlier, but keeping the `setUp()` and `tearDown()` methods.

```python
from flask import request
import unittest

from webapp import app, db
from webapp.models import Trial

class TestIntegration(unittest.TestCase):
    def setUp(self):
        app.config.from_object('webapp.config.Testing')
        db.init_app(app)
        self.app = app.test_client()

    def tearDown(self): 
        for collection in db.session.db.collection_names()[1:]: # Skip first
            db.session.db.drop_collection(collection)

    def test_trial(self):
        Trial('Parkinsons').save()
        rv = self.app.get('/trials/Parkinsons')
        assert 'Trial found: Parkinsons' in rv.data 
```

I run it... and it works. Well, that's great. Turns out my janky setup is actually... ok? This is strange. I'm not popping or pushing or withing or anything.

Well, might as well keep exploring. I've formally imported `g`, `current_app`, `request`, and `session` from `flask`, so let's see what those look like:

`g`:

```python
ipdb> g
<flask.g of 'webapp'>
ipdb> g.get
<bound method _AppCtxGlobals.get of <flask.g of 'webapp'>>
```
I tab-completed `g.` and got exactly *one* method, `get`. I'm not sure what values are currently set on `g`, because it doesn't respond to `.keys()`. What a mystery.

`current_app`:

```python
ipdb> current_app
<Flask 'webapp'>
ipdb> type(current_app)
<class 'werkzeug.local.LocalProxy'>
ipdb> myapp = current_app._get_current_object()
ipdb> myapp
<Flask 'webapp'>
ipdb> type(myapp)
<class 'flask.app.Flask'>
```
About what I expected.

`session`:

```python
ipdb> session
<SecureCookieSession {}>
ipdb> session.modified
False
ipdb> session.items()
[]
```
Not much going on here just yet.

`request`:

```python
ipdb> request
<Request 'http://localhost/trials/Parkinsons' [GET]>        
ipdb> request.view_args
{'name': u'Parkinsons'}
ipdb> request.path
u'/trials/Parkinsons'
ipdb> request.url
u'http://localhost/trials/Parkinsons'
ipdb> request.headers
EnvironHeaders([('Host', u'localhost'), ('Content-Length', u'0'), ('Content-Type', u'')])
```
About right. Groovy. Those work.

So why is my terrible test suite working? I'm distraught. Where have I entered the correct context? Miguel's example from above is the same as mine, except he creates and pushes an app context before creating his test client, while I don't. Yet I'm able to access the database just fine, and it seems like my contexts are being generated correctly.

The mysteries of life. In any case, I'm quite pleased with the work we've done today. I'll keep working on the app and I'll update this post once I finally figure out where I've gone wrong. So far, things seem to be working.

## Update #1

Ok, I figured out at least one way that my testing setup differs from Miguel's.

I threw a binding right after my `assert` statement and tried to see what variables I could find:

```python
ipdb> flask.g
<LocalProxy unbound>
ipdb> flask.current_app
<LocalProxy unbound>
```
As I thought. I'm using the Flask test client for my request, which means that while the *request* is made as it should be, and *within the request* (within the view functions, etc) all of the context variables exist, the minute the request finishes and the response is returned, those variables go away. I can make assertions only about the value of `response`.

In Miguel's version, on the other hand, since he pushes and pops the application context inside of `setUp()` and `tearDown()`, he has access to `g` and `current_app` from anywhere in his test, and can make assertions about them.

## Update #2

A bit more strangeness. Flask gives you a helper function, `url_for()`, which takes the name of a view function as a string and returns either the relative or the absolute URL for that function. Somewhat similar to the `_path` functions in Rails.

I tried to switch my test suite away from hard-coded URLs and towards `url_for()`, but got the following error:

```python
RuntimeError: Application was not able to create a URL adapter for request independent URL generation. You might be able to fix this by setting the SERVER_NAME config variable.
```
 
I pop on over to the Flask [config docs](http://flask.pocoo.org/docs/config/), and see this, under the description of the `SERVER_NAME` variable:

>Setting a SERVER_NAME also by default enables URL generation without a request context but with an application context.

I set `SERVER_NAME = 'http://localhost:5000/'` in my config file, and lo, `url_for()` started to work.

I'm still mulling over why this is the case -- if Flask defaults to `localhost` when you start a development server, why wouldn't `url_for()` do the same? Why does it need to be given the server explicitly, but nothing else does? I suppose it could be an issue with a single application interacting with multiple servers, so Flask can't really know what the URL should be for any given route prior to an actual request being fired.

Anyway, life's mysteries.

## Update #2.1

Getting back into the office today, I kept working on the test suite. I was still getting bugs with `url_for()`, so I threw in a binding and poked around:

```python
ipdb> url_for('trials')
'http://http://localhost:5000//trials'
```

Hmm. Definitely more `http://` and a little more `/` than there needs to be. It seems like `SERVER_NAME` should be set to something more like `localhost:5000`. Let's try.

Works. Go bears.