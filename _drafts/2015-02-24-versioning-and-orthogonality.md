---
layout: post
title: "Versioning and Orthogonality in an API"
comments: true
categories: blog
tags:
- versioning
- architecture
- orthogonality

---

#### So.
It's five months into working at <company>, and things are going pretty well.

The product is continually improving. Our user base and overall app activity is increasing day-over-day at a very satisfying rate (official numbers cannot be made public, unfortunately).

We have released three versions of the iPhone app since December (2.0, 2.1, and 2.2), and are over halfway finished with 2.3.

The company is small -- there is the founder/CEO, our VP of design, and five (soon to be four) engineers. Three on iOS, and two on the backend.

I'm one of the two backend engineers. Being such a small company, my job is a mix of feature development, operations, data and analytics, infrastructure improvements, and forensics. In any given week, I may be developing new features, optimizing database access or business logic, provisioning or updating our servers, or running statistical analysis on our data.

It's exciting.

#### But.
Such rapid development introduces new challenges. Specifically, rapid iOS development has necessitated a versioning system to enable the API to continue to serve old versions of the app, while simultaneously supporting the new features being developed by the iOS team.

This has introduced an entirely new layer of complexity that needs to be managed. Previously, the backend challenges were those of creating a platform to effectively support a *single* product. Now, that same platform is being called on to provide the same level of support to *multiple, overlapping* products **simultaneously**.

Of course, the problem of backwards compatibility is not a new one. Yet, it was new for us. The rest of this post will cover our early thinking around versioning, the more complex challenges our early approaches failed to address, and our next directions.

#### First ideas.

The first discussion we had as an engineering team was about methods of communicating version information between the client and the API. We considered two options:

**Option one: Versioning via URI**

The API endpoints currently look like this:

    https://<company>/api/v1/round/loadgames/
    # The request to get the current member's games.

Astute readers will notice the `/v1/` in the URI. The API is a Django project, with [TastyPie](https://django-tastypie.readthedocs.org/en/latest/) for the REST interface, and view functions are mapped to URIs in the following way:

{% highlight python %}
# <company>/urls.py

from tastypie.api import Api
from contest import rest as ContestAPI

v1_api = Api(api_name="v1")
v1_api.register(ContestAPI.RoundResource())
{% endhighlight %}

Here, `RoundResource` is a TastyPie object which wraps a number of resource-related endpoints (in this case, the `Round` resource, which represents a game in <company>.)

Currently, every resource has a single `rest.py` file which defines the endpoints for that resource. URI versioning would involve the creation of additional `rest.py` files, each representing a different version of the API.

That would look something like this:

{% highlight python %}
# <company>/urls.py

from tastypie.api import Api
from contest.rest_old import restv1 as V1ContestAPI
from contest.rest_old import restv2 as V2ContestAPI
from contest import rest as ContestAPI

v1_api = Api(api_name="v1")
v1_api.register(V1ContestAPI.RoundResource())

v2_api = Api(api_name="v2")
v2_api.register(V2ContestAPI.RoundResource())

v3_api = Api(api_name="v3")
v3_api.register(ContestAPI.RoundResource())
{% endhighlight %}

Notice here that we've moved the old `rest.py` files into a new directory, `rest_old`, and prefixed the file names with the version number.

The current, "working" `rest.py` is left in the original location, and is imported without prefix.

Now, when the iOS team is working on a new version of the app, they can update the URIs on their end to point to the relevant version of the API.

The advantages to this approach are that it allows for the maintenance of entirely separate `rest` modules for each version of the app. This helps keep the code clean (each `rest` file is responsible for one version of the app), at the cost of duplication (each `rest` file contains similar endpoints to the others, with small differences).

The biggest advantage is that changes can be made to the API for future version of the app *without* having to worry about backwards compatibility, because you know that the old `rest` files will be there, unchanged. This means that obsolete endpoints can be deleted with abandon and naming conventions can be improved without having to worry about breaking the old app.

The downside is that this introduces complexity in that there are now more files to keep track of, and while ostensibly the old `rest` files should never need to change, the reality is that they *will* need to be maintained in some form.

**Option Two: Versioning via HTTP headers.**

The second option was to keep one `rest` file per endpoint and to use *conditionals* in the view functions to direct behavior. The API can learn the version of the app making the request like so:


{% highlight python %}
# here, request is a Django HttpRequest object.

    def get_app_version(self, request):
        if settings.TESTING:
            return const.APP_DEV_VERSION

        user_agent = request.META.get('HTTP_USER_AGENT')
        # Looks like '<company>/2.1 (iPhone; iOS 8.1.2; Scale/2.00)'
        try:
            app = user_agent.split(' ')[0]
            version = app.split('/')[1]
            return float(version)
        except:
            return const.APP_STORE_VERSION
{% endhighlight %}

We then set the version number as a property of the request object (as `request.app_version`), and voilá! Every view function can now easily change logic based on app version. This approach results in code that looks like this:


{% highlight python %}
        is_new_search = request.app_version >= 2.2
        members = Member.objects.search(
            member, key, query_type, is_new_search=is_new_search)
{% endhighlight %}

and this:

{% highlight python %}
        if request.app_version >= 2.3:
            data = {'profile': profile}
        else:
            data = profile
        ret = self.generate_ok(data=data)
{% endhighlight %}

The big advantage of this approach is that it can be implemented *quickly* and with little *overhead*. It's a much more lightweight solution than the URI versioning discussed above, especially if the versioned changes are minor.

This solution can become unweildy, though, as the number of versions and the amount of logical branching needed to support all of the versions increased.

#### What we did, and what we found.

We ultimately decided to start with option 2, versioning via HTTP header.

We are three versions deep now, and we've found that while this system is effective for handling small changes in JSON structure (returning a list versus a dict, for example), as well as for passing simple `True`/`False` flags to the model functions, the system begins to struggle once it is asked to support more than two or three logical paths for a single piece of functionality.

What we began to realize is that both of these options are insufficient in that they both assume that the versioning logic can be encapsulated within the `rest` modules. In reality, our versioning changes require controlling behavior three or four function calls deep beyond the view function; changes at the level of the view (be it through separate `rest` files or version-based conditionals) are not enough.

#### The deeper challenge of versioning.

The first big change which we had to version was the implementation of major optimiziation to eliminate redundant calls to the database. This was a major, deep, and non-trivial change which reached deep into our model logic. Most of the rest of this post will focus on our challenges in versioning this change, and what this has taught us about versioning (and change) in general.

Onwards.

Prior to this change, our games were being sent to the client in the following way:

{% highlight python %}
'games': [{
    'round_number': '3',
    'opponent': {
        'userid': '256',
        'firstname': 'Sarah'
        'photopath': <url to photo>,
        # etc...
    },
    'cards': [
        {
            'question': 'Who is more likely to be in a rock band?'
            'top_member': {
                'userid': '1024',
                'firstname': 'Lao'
                'photopath': <url to photo>,
                # etc...
            }
            'bottom_member': {
                'userid': '64',
                'firstname': 'Gabriel'
                'photopath': <url to photo>,
                # etc...
            }
        },
        {
            'question': 'Who is more assertive?'
            'top_member': {
                'userid': '1024',
                'firstname': 'Lao'
                'photopath': <url to photo>,
                # etc...
            }
            'bottom_member': {
                'userid': '256',
                'firstname': 'Sarah'
                'photopath': <url to photo>,
                # etc...
            }
        },
        # etc...
    ]
}]
{% endhighlight %}

This approach was chosen for flexibility -- by implementing a `to_json()` method on every model, we could easily construct large JSON objects for the client. A `round` object, which implements `to_json()`, would call the `to_json()` method of every card it contains, which would then call the `to_json()` method of all of the member objects associated with it.

This allowed us to create a consistent, simple mechanism for generating data to be consumed by the client. It worked very well, but carried some significant costs in terms of speed:

1. It created redundancy in database access. If a single member appears in multiple cards in a round, that member will be generated separately for each card. Since no card has knowledge of any other card, there is no way for one card to "know" that the member was already generated.

2. It generates a great deal of redundant data to be sent to the client. This imposes a cost both in terms of network resources (sending 200,000 characters, containing only 50,000 characters of unique information), as well as in terms of processing time in the client (having to process four times more data than necessary).

As the product matured and concerns about speed became more pressing, the engineering team began to look for ways to eliminate this redundancy.

One of the iOS engineers (also the head of engineering) suggested a minification system in which the member data is kept separate from the games and cards, with the games and cards making reference to the member data via the `userid`.

The data would look something like this:

{% highlight python %}
'games': [{
    'round_number': '3',
    'opponent': '256',
    'cards': [
        {
            'question': 'Who is more likely to be in a rock band?'
            'top_member': '1024'
            'bottom_member': '64'
        }
        {
            'question': 'Who is more assertive?'
            'top_member': '1024'
            'bottom_member': '256'
        }
        # etc...
    ]
}]
'reduc': {
    'data': {
        '64': {
            'userid': '64',
            'firstname': 'Gabriel'
            'photopath': <url to photo>,
            # etc...
        }
        '256': {
            'userid': '256',
            'firstname': 'Sarah'
            'photopath': <url to photo>,
            # etc...
        },
        '1024': {
            'userid': '1024',
            'firstname': 'Lao'
            'photopath': <url to photo>,
            # etc...
        }
    },
    'keys': [
        'opponent',
        'top_member',
        'bottom_member'
    ]
}
{% endhighlight %}

Under this paradigm, the client will parse the `games` list, and look up the appropriate member data by matching the `userid` to the corresponding dictionary with the `reduc` dictionary. The `keys` list provides a means for the client to determine when a value has been reduced, as opposed to when the value is in fact an id.

This also solves the database problem, since in theory we should be able to keep track of which members have been added to the `reduc` dictionary, to avoid having to re-create them when generating future cards.

The challenge was implementing this in a way that could be versioned, without creating too much additional complexity or technical debt, or doing violence to the layers of abstraction which keep the API flexible and easy to develop. We saw two paths to achieve this:

**One:** Create the ability for the view functions to pass knowledge of the app version deep into the model layer. This seemed like a good solution from the point of database optimization, since the `to_json()` functions could then themselves be modified with conditionals to do different things, something like:

{% highlight python %}
    # Card model
    def to_json(self, member, do_reduc=False):
        if do_reduc:
            top_member = str(self.top_member_id)
            bottom_member = str(self.bottom_member_id)
        else:
            top_member = self.top_member.to_json(member)
            bottom_member = self.bottom_member.to_json(member)
{% endhighlight %}

In this example, passing `do_reduc=True` will cause the function to skip database access entirely, and return only the userid of the members.

The advantage of this path is that is *fundamentally* achieves both optimization goals -- database efficiency on the backend, and data efficiency for the client. The primary (and significant) downside is that it **couples** the model (abstract/domain) logic to the specific version of the client (concrete business logic). This violates MVC principles, and is undesirable for several reasons. It devastates the code from a composability perspective, as now the reduction functionality depends on all of the associated functions being called in a *specific* way, so that version status can be passed through.

**Two:** Continue to generate the JSON as before, and to recursively minimize the JSON at some point prior to sending. This approach satisfies the requirement of data efficiency for the client, but does not *fundamentally, by itself* satisfy the requirement of database efficiency.

However, this solution *does* preserve the boundary between the business logic of the view functions and the domain logic of the models. Preserving this boundary is important for reasons of code quality,[^1] as disregarding this boundary is to reject the key insight of the Model-View-Controllor paradigm, and take us back to the wild, anarchic lands.

Still, this solution seems lacking -- how can we achieve efficiency of database access if we cannot communicate version status directly to our models? If we were building *de novo* we could build the new database-access paradigm into the model code in some elegant way, but given that we have to *add* reduce functionality in a way that is backwards-compatible, it seems we need to find some way to allow for *conditional* database efficiency.

If only there was some way to avoid duplicate database access, in a general way that did not depend on specific function calls...

**Caching to the rescue.**

Fortunately, this is a problem that has been solved. The engineering team has been experimenting with different caching strategies for the past few months, trying to find the balance between overall speed and avoiding stale data.

Too much caching, as we have found, introduces difficult-to-diagnose bugs as out-of-date data from the cache is inevitably sent to the client. Too little caching results in a slower app (relative to *more* caching).

What we discovered was that we needed a general way to cache the output of an arbitrary function (conditional on its arguments), and to arbitrarily *delete* that value from the cache when the underlying data has changed.

None of the caching libraries I had looked at provided a suitable level of generality, so I ended up writing one myself (which I hope to make open source someday soon). It works like this:

{% highlight python %}
    MEMBER_JSON_KEY = 'mjson_{}_for_{}' # Filled by self.id and friend.id

    @cache.auto_set(MEMBER_JSON_KEY, [(0,'id'), (1,'id')], 60 * 5) # 5 minutes
    def to_json(self, friend):
        '''Must pass member, even if self'''
        json = {
            "userid": str(self.id),
            "firstname": self.first_name,
            "middlename": self.middle_name,
            "lastname": self.last_name,
            "gender": self.gender,
            "photopath": self.thumbnail_url,
            "originphoto": self.photo_url,
            "ts": self.last_updated,
            }
       # More stuff
{% endhighlight %}

It's working pretty well for us, and we've gotten better at knowing when and how to cache[^2].

With caching, it seems as though we can move confidently forward with option two (generic pre-send minimization). By caching the `to_json()` functions (and with some skillful use of the Django ORM's [`select_related`](https://docs.djangoproject.com/en/1.7/ref/models/querysets/#select-related)), we should be able to achieve the same gains in optimizing database access which we would if we had built a new database-access paradigm directly into the `to_json()` functions, but without needing to give these model-level functions knowledge of the HTTP request to which they are responding.

In addition, we can now write a general recursive function to reduce the *entire* response JSON just before sending it to the client. Given that the reduction now occurs at the very end of the request cycle (by a view function decorator, as it happens), this means that any versioning logic can be encapsulated *only by that decorator*, in just one location:

{% highlight python %}
            ret = func(inst, request, **kwargs) # Calling the view function
            if request.app_version >= 2.3:
                ret = self.reduc_return(ret)
{% endhighlight %}

A single control point. The day, it seems, is saved.

##### But... versioning.

Alas. The brilliant, elegant solution described above did not spring fully-formed from the head of Zeus, but was rather the outcome of several weeks of experimentation and thinking hard. During this process, we released another version of the app (v2.2), which used only a partial implemention of the reduce functionality.

The implemention of reduce which was in place when v2.2 was released was a much rougher cut, in which reduction was not yet a general feature, but rather a feature which worked for only a handful of endpoints (the `/loadgames/` endpoint, as well as the login endpoints). Other endpoints which returned games, or member data in general, were not reduced.

The consequence of this is that when we began preparing to deploy the *new* reduce implementation, we had to version not only for the pre-reduce app (v2.1), but the *earlier version of reduce*. This meant that instead of a `True`/`False` switch at the level of the view function, we had to communicate even more information to the model, and teach the model to take different paths based on which version of the app it was serving.

This increased the complexity of the problem significantly (think `n^3` vs `n^2`), and led to us doing things like this:

{% highlight python %}
    def get_reduc_version(self, request):
        app_version = self.get_app_version(request)
        if app_version >= 2.3:
            return 2
        elif app_version >= 2.2:
            return 1
        else:
            return 0
{% endhighlight %}

and

{% highlight python %}
    def load_games(self, member, do_reduc=0):
        games = []

        actives = self.load_actives(member, do_reduc=do_reduc)
        games.extend(actives)

        pendings = self.load_pendings(member, do_reduc=do_reduc)
        games.extend(pendings)

        # stuff...

        if do_reduc:
            kind = do_reduc
            reduc = self.create_reduc(member, games, kind)
            return games, reduc
        else:
            return games

    def create_reduc(self, member, games, kind=1):
        # stuff...
        if kind == 1:
            keys = ['player', 'top_member', 'bottom_member']
            return {'data': members, 'keys': keys}
        elif kind == 2:
            keys = {k: 'members' for k in ['player', 'top_member', 'bottom_member']}
            return {'members': members, 'keys': keys}
{% endhighlight %}

Our harmless-seeming `True`/`False` flag has turned into an integer. Also, look at how much of this method is devoted to handling version! We are passing version flags four levels deep into our code. And this is after only *three* versions of the app.  Consider the same code, if we had implemented reduction elsewhere:

{% highlight python %}
    def load_games(self, member):
        games = []

        actives = self.load_actives(member)
        games.extend(actives)

        pendings = self.load_pendings(member)
        games.extend(pendings)

        # stuff...

        return games
{% endhighlight %}

Simple. Concise. MVC boundaries are there for good reason, we've discovered.

When preparing the API for deployment, we realized that since *several* view functions relied on this code, we would need to update all of them with the new versioning system, while making sure that the *existing* versioning code (for v2.1) was left in place. Even more challenging, our regression tests, while great for catching bugs *internal* to the API, are less good at catching versioning problems. Ultimately, a versioning bug made it through the process -- an endpoint was configured to use reduce v2.2 style, instead of v2.1 style -- and was live in production for about 45 minutes before we caught it. Not the best moment.

Putting version-based logic in the models is dangerous, because each change is locked in place for the entire length of time you will need to support that version. This increased the complexity, and reduces the flexibility and composability of your code, as your model methods will become coupled to each other in their need to provide a coordinated, version-related response. Further, the code becomes increasingly more brittle, in that the versioning information is stored only in the conditionals themselves, so a single unintended change can break backwards compatibility.

#### The value of orthogonality
[Orthogonality](http://en.wikipedia.org/wiki/Orthogonality_%28programming%29) is a design principle which states that components of a software project should be independent from each other (orthogonal is a synonym for perpendicular, or two lines which intersect at right angles). Two components are orthogonal if one can be changed, removed, reimplemented without requiring a corresponding change to the second.

Orthogonality among software components is desirable because two components which are orthogonal result in more possible combinations of settings than those which are not. As Andrew Hunt and Dave Thomas discuss in their book, *[The Pragmatic Programmer](https://pragprog.com/the-pragmatic-programmer)*, two orthogonal components with three possible configurations each result in nine possible configurations overall. Those same two components, if not orthogonal, would result in fewer possible configurations overall. If component B, for example, could only work if component A was set to option X or Y (but not Z), then the combination of both components can result in at most six possible combinations.

In our case, the first attempt at reduction was implemented without thought to orthogonality -- the attempt to fundamentally improve database access by requiring coordination among multiple model-level functions meant that each function was now restricted and could be applied to fewer contexts. Rather than achieve flexiblity by composition of functions, we attempted to achieve flexiblity by the creation of additonal flags and switches, a solution which proved detrimental to the codebase.

Our second attempt at reduction was implemented in an orthogonal way: by keeping the model-level functions focused on collecting and preparing data, and relying on the separate *caching* and *view function decorator* components to accomplish our twin goals of efficiency in database access and data preparation for the client, we were able to achieve the same goals in a far more flexible and composable way.


#### Lessons learned
So, what have we learned? A few things.

1. Versioning can be accomplished through version-related conditionals in your view functions, or by creating multiple copies of your view functions and route them to different URIs. Each has a place (conditonals are easier for small changes, multiple copies are better for large, general changes).

2. Keep version information out of your models. The deeper you pass version information into your app, the more tightly coupled your code will become. The MVC paradigm did not become popular because it was random and arbitrary, and Rails and Django are not standard frameworks because they encourage frivolous structure. These levels of abstraction are powerful, and should be respected unless you're *very* confident in what you're doing. In this case, failing to respect these boundaries earned us a lot of technical debt.

3. In our case, attempting *fundamentally* improve database access (as opposed to relying on the caching layer) was a case of premature optimization. This is not to say that efforts to fundamentally improve database access are not appropriate (I was able, for example, to reduce database access by 50-75% for multiple functions through some careful refactoring and more complete use of the Django ORM). But attempting to reduce database access by *coupling* models and methods together ultimately proved harmful. It is true that our reduce functionality now relies on the caching layer to function correctly. If the cache ever goes down, then we will lose most of the database access optimizations (as they rely on the cache, not fundamental database access). But this seemed like an appropriate tradeoff: the likelihood of cache failure is much less than the likelihood that we will need to flexibly recombine and repurpose our model methods.

4. Orthogonality in software components is highly desirable. It is highly likely that a software project will be forced to adapt to new requirements, and so designing components to be able to function separately and independently from each other will preserve a great deal of flexibility in your project.

5. If something seems like a bad idea, it most likely is. Be willing to resist making a change in order to achieve some short-term objective if it means reducing the stability and quality of the codebase. Your obligation is to the life of the product, not only to the next release.

And that's where we are. With a much better handle of versioning, a few more scars, and a lot more character :)

---
[^1]: As well as reasons of truth, beauty, etc.

[^2]: I advocated against caching the `member.to_json()` function for a while, being concerned that caching a relatively light-weight function that had responsibility for providing basic member information would lead to many frustrating problems. As we added more substance to this function, however, and it itself became responsible for making subsequent database calls, I realized that setting a short (5 minute) cache for this function was appropriate.