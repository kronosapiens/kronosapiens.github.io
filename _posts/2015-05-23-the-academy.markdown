---
layout: post
title:  "The Academy: A Machine Learning Framework"
date:   2015-05-23 15:15:59
categories: software machine-learning
---

*One of my last projects at my previous company was to implement a framework for developing and testing various predictive models.  Thinking about the users, designing the simplest and most useful interface, adding splashes of color and personality -- it was a really enjoyable project.*

*I'm including a modified version of README for the project, to give you all a flavor of how it was put together:*

## The Academy

#### A Trait Prediction Framework

Welcome to The Academy, a trait prediction framework. You're minutes away from hours of fun developing experimental models for understanding and predicting people's inner selves.

Before you start pounding those ivories, here's a bit about how the system works:

### Overview
First, all the goodness is located in the following directories:

{% highlight bash %}
prediction/
    models/
        hofstadter.py
        pirsig.py
        yourmodel.py <= This is where your model will go
    preprocessor.py
    predict_traits.py
{% endhighlight %}

<!--more-->

`predict_traits.py` is the command which makes the actual predictions for our production users. You update this file to change the model we use in production. We'll come back to this soon.

The `models/` directory is where our different models live. To create a model, create a new `.py` file in this directory. To make it easier to talk about different models, we're going to name them according to a theme. That theme is philosophers. The first two models are Pirsig and Hofstadter.

### Creating a model
You have a lot of freedom in creating your model, provided that you conform to the following interface:

1. Your model must inherit from the `BasePredictor` class, which can be imported from `question.prediction.models`
2. On initialization, your model must accept a `pandas.DataFrame` object as the first argument. It can accept an arbitrary number of keyword arguments, which can serve as the parameters to your model. The parameters are model-dependent -- you can make them anything you want, or have none at all.
3. Your model must implement a `predict()` method, which will return a `pandas.DataFrame`, with scores for all of the member's traits. pandas is a very powerful and popular library for doing data analysis. You can read more about it [here](http://pandas.pydata.org/)

That's it! As long as your model exposes the interface described, you can implement it in any way you like, from support vector machine to `randint()`.

There is a PreProcessor class which will help you prepare the data. Here's how the model should work:

{% highlight python %}
>>> from question.prediction.models import hofstadter
>>> from question.prediction import PreProcessor

>>> pp = PreProcessor()
>>> M = pp.get_scores() # M is the DataFrame of personality scores.
>>> model = hofstadter.Predictor(M, param1=value1, param2=value2)
>>> predictions = model.predict()

>>> predictions.ix[2515, 180]
.89 # The prediction for trait 180 (innovative) for user 2515.
{% endhighlight %}


### Testing a model
After developing a model, it is important that you test it. Only by testing model accuracy and tracking this metric over time will we be able to make continual movement towards greater effectiveness.

To test a model, use the `PredictionTest` class:

{% highlight python %}
>>> from question.models import PredictionTest
>>> from question.prediction.models import pirsig

>>> PredictionTest.objects.prep_data()
>>> PredictionTest.objects.run_test(pirsig.Predictor, params={'alpha': 0.5, 'kind': 'ridge', 'numq': 12, 'st': 2})
{% endhighlight %}


Your model will be tested against the data using a technique called "[K-Fold Cross Validation](http://en.wikipedia.org/wiki/Cross-validation_%28statistics%29)", and the results will be stored in the `question_predictiontest` table:

{% highlight sql %}
+----+---------------------+----------- -------------------------------------------+------------------------------------------------------+------+-------------------+---------+-------+
| id | timestamp           | model                                                 | parameters                                           | n    | error             | runtime | notes |
+----+---------------------+----------- -------------------------------------------+------------------------------------------------------+------+-------------------+---------+-------+
|  1 | 2015-04-13 22:24:30 | <class 'question.prediction.models.pirsig.Predictor'> | {'alpha': 0.5, 'kind': 'ridge', 'numq': 12, 'st': 2} | 1000 | 0.272384680982066 |   83550 | NULL  |
+----+---------------------+----------- -------------------------------------------+------------------------------------------------------+------+-------------------+---------+-------+
{% endhighlight %}

The test will store information about the model and parameters that were used in the test, as well as the accuracy and the runtime of your algorithm. Accuracy is calculated using a technique called "[Root Mean Square Error](https://www.kaggle.com/wiki/RootMeanSquaredError)".

You can test your model with different sets of parameters, to find the best values. You can also save some notes with the test, if you like:

{% highlight python %}
>>> PredictionTest.objects.run_test(mymodel.MyModel, params={param1:value3, param2:value4})
>>> PredictionTest.objects.run_test(mymodel.MyModel, params={param1:value5, param2:value6})
>>> PredictionTest.objects.run_test(mymodel.MyModel, params={param1:value5, param2:value6}, notes='Trying a large value for param2')
{% endhighlight %}

You have some options in regards to the data your model runs on. By default, the model runs on the entire dataset, and uses the `score` for any question (`agrees`/`enumeration`). You can change this as follows:

{% highlight python %}
>>> PredictionTest.objects.prep_data(n=5000) # Use only the top 5000 members (by total # of enumerations)
>>> PredictionTest.objects.prep_data(using='final_scores') # Use final_score (percentile ranking)
{% endhighlight %}

