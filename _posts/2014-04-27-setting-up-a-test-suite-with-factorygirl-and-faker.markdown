---
layout: post
title: "Setting up a test suite with FactoryGirl and Faker"
date: 2014-04-27 17:47:18 -0400
comments: true
categories:
- testing
- gems

---

*Note: this is my first post written using markdown. I've decided to migrate my technical blog back to Octopress from Wordpress after realizing that Wordpress's support for `code snippets` is just not up to snuff. Markdown is fun!*

## Intro

Since Flatiron School ended last week, I've been taking some time to work on xp, a skillshare-like platform I created (along with @sts10) for the Flatiron science fair.

I realized early on how important it would be to become *good* at testing, and I've made tests a top priority in every project I've done. The test suite for xp is the best I've ever written, and while that isn't saying all that much (it's far from perfect), there are some good things going on. We made use of thoughtbot's **FactoryGirl**, a gem which lets you create 'factories' to easily create objects to test. xp uses a lot of associations and validations, which meant that getting FactoryGirl to do what we wanted took a little bit of configuration. The TAs at Flatiron were a big help in getting everything going.

Factory girl works by letting you define 'factories', which contain all the information and settings you need in order to create ActiveRecord objects for your test suite. Complex objects require some special settings and configuration -- as we go through the factory settings, I'll explain what aspects of our program required the additional factory configuration.

<!--more-->

Here's one of our factories (I'll explain what's going on below):

```ruby
FactoryGirl.define do 

  sequence :title do |n|
    Faker::Name.name + n.to_s
  end

  factory :lesson do 
    title
    description { Faker::Lorem.sentence }
    references { Faker::Internet.url }
    specific_time { DateTime.now }
    specific_location { Faker::Address.street_address }

    trait :completed do
      status 'completed'
    end

    trait :closed do
      status 'closed'
    end

    before(:create) do |lesson|
      lesson.tags << create(:tag)
    end
  
  end
end
```
Let's take it bit by bit.

## Creating the factory

```ruby
FactoryGirl.define do
	# code
end
```
This may be self-explanatory, but this code is where you tell FactoryGirl to define a new factory. All of the blocks that follow are organized by the 'define' function into a single factory. In this case, the factory is `:lesson`.

## Defining a sequence

```ruby
  sequence :title do |n|
    Faker::Name.name + n.to_s
  end
```

Many ActiveRecord objects require that their name or title (or similar) attributes be unique. FactoryGirl supports this by providing a syntax for defining 'sequences', where an attribute (in this case, `:title`) will be automatically incremented every time FactoryGirl creates an object out of that factory. In this case, `n` will increase by one every time we ask for a new object, so that no two objects have the same name.

You may be wondering what's going on with `Faker::Name.name`. [Faker](https://github.com/stympy/faker) is a gem which lets you create real-looking fake data for attributes. It makes testing a lot more fun (and makes your tests more realistic), because you're dealing with values that look like real data, versus every name and description being some variation of 'test test' ;).

[More on using Faker with FactoryGirl](http://objectliteral.blogspot.com/2009/07/make-faker-work-with-factory-girl.html)

## Defining values for the objects attributes

```ruby
factory :lesson do 
    title
    description { Faker::Lorem.sentence }
    references { Faker::Internet.url }
    specific_time { DateTime.now }
    specific_location { Faker::Address.street_address }
```

Here, we get down to business and define the values for all the attributes of the lesson object. Note that we don't *need* to define a value for every attribute. At minimum, you'll need to satisfy every validation requirement you've written for your object. Everything above that is optional, and you'll want to define attributes as necessary so you can test what you need to test.

You'll note that `title` doesn't have any value after it. That's because we've defined title earlier, when we defined the sequence. Calling `title` on the second line pulls a value out of the sequence generator above, while all the other attributes take their values from the block being passed to that attribute.

## Specifying specific traits

```ruby
    trait :completed do
      status 'completed'
    end

    trait :closed do
      status 'closed'
    end
```
Here, we define special "options" for when we create our objects. Some of our tests test for behavior based on specific values for an attribute (in this case, the `status` attribute). We specify the trait when we create the object in our actual test file (which you'll see later). This `trait` feature is very powerful, and allows you to tap into the power of FactoryGirl without sacrificing the flexibility of creating objects explicitly in your tests.

## Advanced actions
```ruby
    before(:create) do |lesson|
      lesson.tags << create(:tag)
    end
```

Sometimes you need to take actions on your object before you can save it -- in our case, we wrote a custom validator which required a lesson to have at least one associated tag before it could be saved. We addressed this by defining a `before(:create)` action, which is called after an object is instantiated but before it is first saved to the database.

## FactoryGirl in action
Now that you've seen all the powers of FactoryGirl in defining a factory, let's see it in action. Here's an exerpt from our `lesson_spec.rb` file:

```ruby
describe "Lesson" do
  let(:lesson1){ create(:lesson) }
  let(:lesson2){ create(:lesson) }
  let(:lesson3){ create(:lesson, :closed) }
  let(:lesson4){ create(:lesson, :completed) }
```
As an aside, notice that we're using rspec's `let` syntax, which is powerful because it lets you *define* variables in your test file, but not actually *create* the objects until your actual test needs it. What that means is that `lesson1` is not actually created until much later, when we call it for the first time below:

```ruby
lesson1.registrations.create(:user => user1, :role => "student")
```
The advantage here is that we can define the variables all in one place, but not use system resources creating and storing them until the point at which they are required in the test. Contrast this to the following:

```ruby
before(:each) do
	@lesson1 = create(:lesson)
	@lesson2 = create(:lesson)
	@lesson3 = create(:lesson, :closed)
	@lesson4 = create(:lesson, :completed)
end
```
This block would create all four lessons before the first test is run, and regardless of whether or not the variable is called, resulting in a *much* slower test suite. A third option, which is defining every variable at the top of every test, would be faster at runtime, but lead to a bloated and redundant test file.

The `let` syntax gives us speed while keeping us DRY. Use it!

Going back to FactoryGirl, we see how easily we can create new lessons and configure them as necessary for out tests. One of our tests checks a method which returns all lessons by status. FactoryGirl's `trait` feature gave us the ability to control just enough of the lesson's information to pass that test, while keeping most of the data out of our hands (making our test suite more valuable, by making the data as close to possible as real life).

Finally, let's take a peek at what `lesson1` looks like: 

```ruby
 #<Lesson id: 1, title: "Mr. Madyson Mayert4", description: "Quidem eligendi non laboriosam ratione ipsam labor...", references: "http://bernhard.net/izaiah", created_at: "2014-04-27 22:54:56", updated_at: "2014-04-27 22:54:56", specific_time: "2014-04-27 22:54:56", specific_location: "60691 Milan Trail", status: "open", slug: "mr.-madyson-mayert4">
```

Happy testing!