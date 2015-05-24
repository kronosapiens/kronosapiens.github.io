---
layout: post
title: "A Dynamic and Generally Efficient Front-End Filtering Algorithm"
date: 2014-03-31 17:55:46 -0400
comments: true
categories: 
- filtering

---

For the last week or so, Sam and I have been working on "<a href="https://github.com/kronosapiens/xp">xp</a>", a skillshare platform for the Flatiron community. The concept: a site where people interested in teaching and people interested in learning can connect with each other by posting either requests for lessons or by offering lessons themselves. Users can then browse and sort available lessons via various filters, select and participate in those that interest them, and grow as people. Everyone wins!<em> Except plutocracy.</em>

One of the first hurdles of this digital steeplechase was the technical challenge of implementing an effective front-end filtering algorithm. We wanted users to be able to filter through the available lessons by selecting various combinations of tags -- and only those lessons which satisfied <em>all</em> of the conditions should be displayed. Further, we wanted the entire implementation to be able adapt dynamically to the addition of new tags, without requiring additional programming or modification. Finally, and needless to say, we wanted our algorithm to be efficient, with as little an O as possible.

<!--more-->

Sam found <a href="http://jsfiddle.net/6wYzw/41/">an interesting JSFiddle</a> solving a related problem, in which the user is able to select multiple checkboxes and see options which meet <em>any</em> of the criteria. This was the opposite of what we needed, however -- we needed a solution that would only allow options which met <em>all </em>the criteria. It was good inspiration, in any case.

Alright, enough exposition: <a href="http://jsfiddle.net/kronosapiens/4EqGw/10/">our Solution in a JSFiddle</a>

On the front end, our solution hinges on the identification of each tag by its unique id number. By representing each tag as an integer, we were able to use some jQuery syntax to dynamically construct an array of "active" tags every time a filter was selected or deselected. Further, we learned that, if we set the value of a "data" attribute to an array of integers, we could use the jQuery "data" selector to access that attribute directly as an array, as opposed to as a string. Finally, using a specialized adaptation of the "intersect" function, we were able to compare the dynamically constructed filter array to every lesson's own set of filters, only allowing those lessons whose filter set completely encompassed the current set of active filters. The fact that we were able to conduct the comparison through numbers, rather than string comparisons, represents the key achievement of efficiency. I assert that by avoiding an entire level of high-level iteration, we realized a five-fold speed increase over an alternative string-matching implementation.

On the back end, our solution took advantage of the fact that every tag would automatically be assigned a unique id. This meant that, via a number of lightweight model methods, we could generate our views such that every object on the page would contain a data tag containing a numeric representation of the filter information. As new tags were added, these methods would generate views that reflected the new information. In this way, our front-end JavaScript is relying directly on information from the database, and derives its functionality from an <em>automatic and central feature of the SQL database</em>. This passing and processing of the primary key all the way through the application, from the depths of the database to the pinnacle of the user interface, is one of the cooler things about this implementation, IMO.

A major consideration and minor complication was the implementation of multiple <em>categories </em>of tags. Given that the unique primary key was central to this implementation, constructing multiple tables for different categories of tags was unfeasible (as that would've created tags with identical primary keys). We chose to add a new "category" column to our "tags" table, and write a few methods to help select methods by category, as needed. This proved an effective solution, given that, from the perspective of the filter, all tags are equal.

The front-end code is all in the <a href="http://jsfiddle.net/kronosapiens/4EqGw/10/">JSFiddle</a>. Some back-end code is duplicated below for context and edification.

The "tags" table schema:
<pre>create_table "tags", force: true do |t|
  t.string   "name"
  t.datetime "created_at"
  t.datetime "updated_at"
  t.string   "category"
end
</pre>
Some helper methods for selecting from the database. Note that the Lesson and Tag models are connected via a "lesson_tags" join table. Lesson model (instance methods):
<pre>def all_tags
  lesson_tags.map(&amp;:tag)
end

def tag_ids_to_array
  all_tags.inject([]){|tag_array, tag| tag_array &lt;&lt; tag.id}
end
</pre>
Tag model (class methods):
<pre>def self.all_topics
  where(:category =&gt; "topic")
end

def self.all_times
  where(:category =&gt; "time")
end

def self.all_locations
  where(:category =&gt; "location")
end
</pre>
From the controller:
<pre>private
def get_tags
  @topic_tags = Tag.all_topics
  @location_tags = Tag.all_locations
  @time_tags = Tag.all_times
end
</pre>
Code from the view which generates the HTML. Generating the tags:
<pre>&lt;% @topic_tags.each do |tag| %&gt;
&lt;option id="&lt;%= tag.id %&gt;"&gt;&lt;%= tag.name %&gt;&lt;/option%&gt;
&lt;% end %&gt;
</pre>
Generating the lessons' data tags:
<pre>data-tags="&lt;%= lesson.tag_ids_to_array %&gt;"
</pre>
An early ruby "sketch" of our intersection comparator:
<pre>filters = [1, 4]
lessons = [[1, 2, 4], [2, 3], [1, 3, 4]]

def select_lessons_by_filters(lessons, filters)
  lessons.select do |lesson|
    lesson &amp; filters == filters
  end
end
</pre>
And good times were had by all.