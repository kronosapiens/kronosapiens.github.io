---
layout: post
title: "Getting Cozy with rspec_helper"
date: 2014-03-12 18:03:36 -0400
comments: true
categories: 
- testing
- rspec

---

ZOMG THIS IS A LOT OF CODE ALL OF A SUDDEN WTF

Relax. This is rspec_helper, or 'Specky' for short. You've met. In fact, you two have already spent quite a bit of time together. Quality time. It's not always an easy relationship, of course. You have your differences, but you're on the same team. You want Specky to help you run your test suites, to give you the tools to run effective and efficient tests. Specky wants you to clearly communicate your desires and expectations. Problems arise when you don't know what Specky is trying to tell you, and when Specky doesn't know what you want. As with all relationships, it comes down to communication.

<!--more-->

```ruby
ENV["SINATRA_ENV"] = "test"
 
require_relative '../config/environment'
require 'rack/test'
require 'capybara/rspec'
require 'capybara/dsl'
 
if defined?(ActiveRecord::Migrator) && ActiveRecord::Migrator.needs_migration?
  raise 'Migrations are pending run `rake db:migrate SINATRA_ENV=test` to resolve the issue.'
end
 
RSpec.configure do |config|
  config.treat_symbols_as_metadata_keys_with_true_values = true
  config.run_all_when_everything_filtered = true
  config.filter_run :focus
  config.include Rack::Test::Methods
  config.include Capybara::DSL
 
  config.before(:suite) do
    DatabaseCleaner.strategy = :transaction
    DatabaseCleaner.clean_with(:truncation)
  end
 
  config.around(:each) do |example|
    DatabaseCleaner.cleaning do
      example.run
    end
  end
 
  config.order = 'default'
end
 
def app
  Rack::Builder.parse_file('config.ru').first
end
 
Capybara.app = app
```

In interests of peace and harmony, I thought it was high time to sit the two of you down for a little coeur-a-coeur. What, exactly, is Specky all about? Let's find out.
<pre>ENV["SINATRA_ENV"] = "test"</pre>
What's going on here? As you probably noticed, most of your projects have two databases going on -- one for development, and one for testing. The way that your program knows what database to write and read from is by checking the "SINATRA_ENV" variable. Because Specky is run before every rspec file, this line will make sure that all your tests are writing and reading from your test database -- just the way you want them to.
<pre>require_relative '../config/environment'
require 'rack/test'
require 'capybara/rspec'
require 'capybara/dsl'</pre>
Here, Specky is doing some housekeeping and loading all the other files you'll need to run your tests. The first line is the big one -- this loads all your models, your controllers, your views -- in short, everything in your program's environment. The next lines load the files needed for testing -- the rack/test and the capybara methods, so you can enjoy the oh-so-convenient testing syntax you've come to enjoy (all those "describes" and "expects" need to come from somewhere, after all).
<pre>if defined?(ActiveRecord::Migrator) &amp;&amp; ActiveRecord::Migrator.needs_migration?
  raise 'Migrations are pending run `rake db:migrate SINATRA_ENV=test` to resolve the issue.'
end</pre>
Here, Specky is double-checking your work and making sure that you've set up your testing database the way you're supposed to. Specky gets around, and they know that developers have a bad habit of creating migrations, running downstairs for some diet coke, and forgetting to actually run the migrations to set up their databases. It stresses Specky out when tests explode because the databases aren't right, and so they do a quick check before they start running your tests. A stitch in time saves nine, as they say.
<pre>RSpec.configure do |config|
  config.treat_symbols_as_metadata_keys_with_true_values = true
  config.run_all_when_everything_filtered = true
  config.filter_run :focus</pre>
Specky just opened the big configuration method, and is about to start flipping some switches. These next three settings are a bit obscure, and unless you're a pretty sophisticated rspec user,  most likely won't affect the outcomes of your tests. They relate to a feature of rspec that we don't really use, in which you set "tags" on specific tests, so that you can run only certain blocs of tests in your suite. If you're interested in learning more about these functionalities, the relevant documentation can be found <a href="https://www.relishapp.com/rspec/rspec-core/v/2-13/docs/filtering/run-all-when-everything-filtered">here</a> and <a href="https://www.relishapp.com/rspec/rspec-core/v/2-6/docs/filtering/inclusion-filters">here</a>.
<pre>  config.include Rack::Test::Methods
  config.include Capybara::DSL</pre>
These next two lines aren't particularly groundbreaking. They're the corollaries of the earlier rack and capybara requirements; this time around, we're including particular modules into our rspec configuration (as opposed to incorporating full libraries into our environment, which we did before, and which was a necessary precursor to these lines of code).
<pre>  config.before(:suite) do
    DatabaseCleaner.strategy = :transaction
    DatabaseCleaner.clean_with(:truncation)
  end</pre>
Ah. Now things start to get dicey. Here we move past global rspec configuration settings and start talking about specific procedure that Specky will execute <em>during the process</em> of running your test suite. This particular quartet requires a little <em>linguistic precision</em>. We generally use the term "suite" to describe our entire set of tests, as in "running your test suite". Specky, however, is possessed with a shade more nuance. They use the term "suite" to refer to a block of tests contained within a <em>describe</em> block (at least, according to <a href="https://stackoverflow.com/questions/6773675/how-to-define-suites-in-rspec2">this corner of StackOverflow</a>). Describe blocks occupy the second tier in rspec land, being used often as the envelope for a number of "it-do" blocks.

What this code is doing essentially is clearing out your databases in between "suites" (in this case, "transaction" seems to indicate a "rolling back" of data-writing, while "truncation" seems to be more of a "delete everything" sort of deal -- see <a href="https://stackoverflow.com/questions/7419498/transaction-vs-truncation-database-cleaner">StackOverflow</a> for more on this). For your purposes, though, this means that any data you create within one test suite will cease to exist by the time you reach your next test suite. This requires a bit of attention to precisely <i>where</i> and <em>how</em> you create the data you wish to test; inattention here will result in quite a bit of frustration as you try to debug your objects -- only to realize that you are in fact debugging your test suite.

Moving on.
<pre>  config.around(:each) do |example|
    DatabaseCleaner.cleaning do
      example.run
    end
  end</pre>
This code was tricky. Specky was being quite coy (<a href="http://animalpictures.us/wp-content/uploads/2013/12/Koi-Fish11.jpg">koi</a>?), here. To be honest, I'm really not 100% on this -- <a href="https://www.google.com/search?q=config.around(%3Aeach)+do+%7Cexample%7C+DatabaseCleaner.cleaning+do+example.run+end+end&amp;oq=config.around(%3Aeach)+do+%7Cexample%7C+DatabaseCleaner.cleaning+do+example.run+end+end&amp;aqs=chrome..69i57.560j0j1&amp;sourceid=chrome&amp;espv=210&amp;es_sm=119&amp;ie=UTF-8">the internet</a> was as ambiguous as Specky was. It's not entirely clear to me what "example" is, although previous lines would suggest that it is a "suite", following our precise definition. Then it seems like additional cleaning is done, although given that our previous chunk of code seemed to basically obliterate any extant database-type data-oids, I'm not quite sure what this is meant to be doing. Let's say it's doing some deep cleaning?

Levity aside, the aggressive data-clearing on the part of rspec_helper is very important for our tests. In production, you'll have little control over the data coming into your database. If you were to run your tests with a database containing old data, data that you had created yourself, data from past tests, etc, you run the risk of passing tests not because of the quality of your program, but by virtue of some fluke of your database. Specky's idea here is that your databases should contain the minimum amount of information necessary to make your tests pass, and so works hard to make sure that every test suite is run against a figurative <a href="https://en.wikipedia.org/wiki/John_Locke"><em>tabula rasa</em></a><em>.</em>
<pre>  config.order = 'default'
end</pre>
Ah yes, the end of our epic "config" call. And finally -- some stability! This line sets the order of tests to something nice and sane, like 'default', in which everything runs in the awfully-comfortable order in which it was defined. Compare this to the frustrating-but-admittedly-rather-useful "config.order = 'random'", which randomizes tests to add another layer of rigor to the overall suite.
<pre>def app
  Rack::Builder.parse_file('config.ru').first
end</pre>
In this little trio, Specky will parse your config.ru file using the Rack::Builder.parse_file method, nab the first entry* in the ensuing hash (which is, in fact, the thing that you want) and set that puppy equal to "app", for use very shortly.
<pre>Capybara.app = app</pre>
Finally! The last line. Here, Specky takes the variable "app" which you defined not three picoseconds prior and sets it as the value of the Capybara.app variable -- thereby teaching Capybara how to mimic your application.

And, voila. The thoughts, dreams, and aspirations of your rspec_helper file have been laid bare before you. Hopefully now, in your new and more intimate understanding, the two of you can move bravely forward into a bold new dawn of pleasant, test-driven development.

*For the curious, here is what 'app' is set equal to:

https://gist.github.com/kronosapiens/9505813