---
layout: post
title: "Trails &amp; Ways: A Look at Rails Routing"
date: 2014-03-25 17:58:16 -0400
comments: true
categories: blog
tags:
- routing

---

> Touch things with consideration and they will be yours.

> Infinite Jest

 
Our routes are the neuronal connections of our applications. They are the bridges between our users and our data, and define the interactions that our applications are capable of. Yet, beginners often describe routing to be frustrating; an uncertain process that often goes awry . Some, in frustration, swear off generated routes entirely, choosing to draw their routes by hand. Having read through the Rails Routing guide last week, I wanted to highlight a few particularly striking features of Rails routing, and suggest that the proper application of these tools will allow you to draw your routes with greater finesse, control, and accuracy.

<h3><a href="http://guides.rubyonrails.org/routing.html#nested-resources">Nested Resources</a></h3>
Most of us are aware of the
<pre>resources :posts</pre>
method in Rails, which, if added in the config/routes.rb file, will cause Rails to draw the "seven RESTful routes" of index, new, create, show, edit, update, and destroy. This works well for independent resources, but what if your domain model is more complex, and needs to support nested resources? Nested Resources to the rescue. Rails supports the nesting of resources via the following syntax:
<pre>resources :posts do
 resources :comments
end</pre>
<!--more-->
Including this in your routes.rb file will tell Rails to draw 14 routes, seven for each resource, with the nested resource coming after the first-level resource in the URI. Ex: <em>http://www.example.com/posts/1/comments/3/edit</em> You can theoretically nest resources to infinite depth, but the Rails guide explicitly discourages nesting more than three resources deep -- suggesting that perhaps, if such nesting seems necessary, that you should reconsider your site's design.
<h3><a href="http://guides.rubyonrails.org/routing.html#controller-namespaces-and-routing">Controller Namespaces and Routing</a></h3>
Now, say you'd like the benefit of nested URIs, but without all the headache of actually creating new resources? Or, you'd like to separate a resource into two sort of "virtual" resources, which use the same model but are accessed via different URIs? Namespaces to the rescue! This feature behaves quite similarly to nested resources, and accepts the following syntax:
<pre>namespace :admin do
 resources :posts
end</pre>
This will draw routes like <em>http://www.example.com/admin/posts/new</em> These routes can coexist with those at <em> <em>http://www.example.com/posts</em></em> which<em><em> </em></em>creates the possibility of two separate controllers, with different methods, both writing and reading from the same Post model.
<h3><a href="http://guides.rubyonrails.org/routing.html#restricting-the-routes-created">Restricting the Routes Created</a></h3>
Much hullaballoo has been made at Flatiron on the relative pros and cons of the über-powerful "<em>rails generate scaffold"</em><em> </em>command<em>. </em>In one corner, there are those who enjoy the ability to being a project with a fully-stocked pantry of routes and controllers. In the other, there are those of more sober caution, who worry about their projects being strangled in a jungle of superfluity. Rails, of course, allows for compromise. Using the "<em>only</em>" and "<em>except</em>" macros, it becomes possible to exert a finer degree of control over the almighty Rails generators, making drawing routes downright relaxing. Ex:
<pre> resources :posts only: [:new, :show, :destroy]</pre>
or
<pre>resources :posts except: [:index]</pre>
These macros will restrict the routes drawn, allowing us the benefits of the Rails generators, without the excess. (You will have to delete the actions from the controllers manually, I believe). As an aside, having some neuroscience background, the parallels between this sort of "pruning" and the process of neurogenesis are striking -- the idea that you first draw many more routes than you could possibly need, and prune downwards, as opposed to only building what you need as you need it. Perhaps I'm reading more into the metaphor than the substance justifies, but it's an exciting idea. More on this concept <a href="http://kronosapiens.com/2012/09/22/an-observation-of-some-patterns-of-nature/">here</a>.
<h3><span style="line-height:1.5em;"><a href="http://guides.rubyonrails.org/routing.html#segment-constraints">Segment Constraints</a></span></h3>
Perhaps my favorite routing feature. Segment constraints allow you to define regular expressions which filter through URIs when matching your routes. Ex:
<pre>get '/:id', to: 'posts#show', constraints: { id: /\d.+/ }
get '/:username', to: 'users#show'</pre>
What's cool about this is that, since routes are evaluated in the order they are defined, segment constraints allow you to create a "cascade" of possible routes within a single namespace. In the above example, any value which satisfied the constraint of being numeric would've been caught by the first route and been directed to <em>posts#show</em>, while any alphabetical values would've passed the first route and been captured by the second, going to <em>users#show</em>. In clever hands, this technique could be quite powerful. There are many other special features of Rails routing, but these were the most striking and seemed to have the most non-contrived potential. Good luck!