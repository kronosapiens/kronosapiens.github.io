---
layout: post
title: "OpsWorks, Flask, and Chef"
comments: true
categories: blog
tags:
- opsworks
- flask
- chef
- infrastructure

---

Today we conquered the kitchen.

We have used AWS OpsWorks and Chef to successfully configure and deploy a Flask app, and to redeploy the app after every GitHub commit. Now [Thena](http://thena.io) can develop at significantly higher speeds.

## Setup

Let us consider the pieces in play:

1. Thena, a [Flask](http://flask.pocoo.org/)-based web application.
2. [AWS OpsWorks](https://aws.amazon.com/opsworks/), an "application management service".
3. [Chef](https://www.chef.io/), a configuration mangement tool.
4. The correct environment and infrastructure for Thena, call it $$ \theta $$.
5. A micro EC2 instance backed by a small Postgres database.

Our goal is to configure the EC2 instance to be able to serve the app, and to automate all infrastructure such that new features can be deployed in real-time.

The first challenge is to successfully automate setup and deploy. This requires the interaction of five components: the EC2 instance, GitHub, the Chef process, the nginx process, and the uWSGI process.

We will need to do the following:

1. Install all necessary ubuntu packages on the EC2 instance
2. Create (and update) all directories for application, configuration, and log files.
3. Create (and update) all necessary configuration files.
4. Set all necessary file and directory permissions.
5. Enable and start the nginx process.
6. Connect to GitHub and download most recent application code.
7. Update any Python packages.
8. Restart the uWSGI process.
9. Restart nginx.

Steps 1-5 are known as the "Configure" phase. Steps 6-9 are known as the "Deploy phase". The Configure commands are meant to be run once, when an EC2 instance is first brought online -- this configuration is not expected to change much over the life of the application. The Deploy commands are meant to be run arbitrarily often -- in this case, every time code is committed to GitHub.

## Enter the Kitchen

We use the Chef process to execute steps 1-9, both the Configure and the Deploy phases. Chef is a tool which uses "cookbooks" to learn how to bring nodes (in this case, EC2 instances) into proper alignment (formally, to create state-of-affairs $$ \theta $$). In order to configure Chef, we first have to write a cookbook.

Our cookbook, `thena-infra` is structured as follows:

```
thena-infra/
    attributes/
        default.rb
    recipes/
        configure.rb
        default.rb
        deploy.rb
    templates/
        default/
            thena-nginx.erb
            thena-uwsgi.conf.erb
            thena-uwsgi.ini.erb
    metadata.rb
    Berksfile
    .kitchen.yml
```

These files and directories play various roles, as follows:

- The `attributes` directory hold attributes files. These files define the constants which will be used in the cookbook. Things like application paths, logfiles, ports, and the like are defined here.

- The `recipes` directory contains the substance of the cookbook. This is where you specify the actual configuration that you want. With Chef, you define configuration using things called "resources". To Chef, everything is a resource -- files, processes, commands, packages, etc.

- The `templates` directory contains templates for all of the specific files you want Chef to write to the node (our EC2 instance). All templates have the `.erb` extension, short for "Embedded Ruby" -- allowing Chef to insert context-relevant data into the template before writing it to the node. You can think of these similarly to templates for web applications.

- The `metadata.rb` file provides, unsurprisingly, metadata about the cookbook. This includes the name, author, and version of the cookbook, as well as defining any **dependencies**.

- The `Berksfile` is the file used by Berkshelf, Chef's dependency manager. Berkshelf is responsible for downloading any dependency cookbooks, and Berksfile is where we define those dependencies and where Berkshelf should look for the cookbooks (in our case, we simply tell Berkshelf to check `metadata.rb` to see what cookbooks are needed).

- The `.kitchen.yml` file is used to configure Test Kitchen, Chef's test harness.

There will likely be other files in a cookbook, but we will concern ourselves with these for now.

Developing a cookbook is similar to developing any piece of software -- it requires a tight feedback loop. To get this feedback, we used [Test Kitchen](https://learn.chef.io/local-development/rhel/get-started-with-test-kitchen/).

Test Kitchen is a tool that lets you start virtual machines locally, execute your Chef recipes on that VM, and then check the VM to confirm that everything is in order. It's an easy-to-use tool that was very helpful when developing the `thena-infra` cookbook.

With Test Kitchen, I was able to develop the cookbook up to the point of launching a correctly-configured webserver serving a generic "Hello World" message. As the nginx process was listening on port 80, I was able to test the cookbook as follows:

```bash
ƒ: kitchen converge
<output logs suppressed>

ƒ: kitchen login
Welcome to Ubuntu 14.04.1 LTS (GNU/Linux 3.13.0-24-generic x86_64)

 * Documentation:  https://help.ubuntu.com/
Last login: Tue Nov 10 16:51:41 2015 from 10.0.2.2
vagrant@default-ubuntu-1404:~$ curl http://0.0.0.0:80/
Hello Thena
```

The cookbook works!

## To the Cloud

We've developed a cookbook which runs great locally. Now we need to get that cookbook onto AWS OpsWorks, and to update the cookbook to pull the application code from GitHub and serve that (instead of serving the generic message).

The first step will be to learn how to upload cookbooks to AWS OpsWorks. This ended up being a bit tricky, since the repository structure [that AWS expects](http://docs.aws.amazon.com/opsworks/latest/userguide/workingcookbook-installingcustom-repo.html) is different from the one [Chef uses](https://docs.chef.io/chef_repo.html) for its enterprise server product. Specifically, AWS expects:

```
chef-repo/
    cookbook_a/
    cookbook_b/
    ...
    Berksfile
```

While Chef enterprise uses:

```
chef-repo/
    cookbooks/
        cookbook_a/
            Berksfile
        cookbook_b/
            Berksfile
        ...
    ...
```

With differences being the location of the cookbooks and the Berksfile(s). Having developed the `thena-infra` cookbook using the Chef-recommended structure, I ran into a few errors when trying to upload the cookbook to AWS. I eventually got the [cookbook working](https://github.com/kronosapiens/chef-repo) as follows:

1. Placed the cookbook at the top of `chef-repo/`, rather than nested inside `cookbooks/`.
2. Moved the Berkshelf file to the top of `chef-repo/` and hard-coded the dependencies (because it was no longer possible to reference `metadata.rb`).

I wasn't thrilled about change 2, since it violates single-source-of-truth and will require me to update dependencies in two places. As I add more cookbooks, I will have to record all of their dependencies in the shared Berksfile, which is also not ideal. It is sufficient for now, but in the future it may be worth returning to this.

With this, AWS OpsWorks now has the cookbook.

Now comes time to test OpsWorks' ability to pull code from GitHub. OpsWorks provides some code you can use in your recipes to pull code from GitHub, using configuration from OpsWorks itself (which you set via the AWS Console). This isn't something that can easily be tested using Test Kitchen, so from here on out we're testing directly in OpsWorks, on our actual EC2 instance. OpsWorks makes it pretty easy to execute specific recipes via the console interface, which is what we'll be doing.

For reference, here's the boilerplate from AWS:

{% highlight python %}
include_recipe 'deploy'

node[:deploy].each do |application, deploy|
  opsworks_deploy_dir do
    user deploy[:user]
    group deploy[:group]
    path deploy[:deploy_to]
  end

  opsworks_deploy do
    deploy_data deploy
    app application
  end
end
{% endhighlight %}

And here is [AWS's guide](http://docs.aws.amazon.com/opsworks/latest/userguide/workingcookbook-json.html#workingcookbook-json-deploy) to deployment attributes.

Before going further, let's take a moment to discuss how OpsWorks uses Chef. Chef is run as root, but can be configured to take specific actions as a specific user. When OpsWorks is executing deploy recipes, for example, commands are by default run as the `deploy` user. Chef allows you to specify, for any given resource, what user should be associated with that resource. If you want to start the uWSGI process as the `ubuntu` user, for example, you will specify this in the recipe.

Executing the cookbook for the first time yields an error in accessing GitHub. I look online and see that someone has managed to circumvent the error by telling OpsWorks to download the repo using HTTPS instead of SSH. I make the change and the code downloads without a problem. I'm planning on circling back around to this later -- I anticipate the problem was that OpsWorks was trying to SSH to github as the `deploy` user, which hasn't set up a public key on GitHub.

I run the cookbook again. Another error -- uWSGI isn't being restarted. I look at the logs and realize that Chef is trying to start uWSGI with `init`. I'm planning on using [Upstart](http://upstart.ubuntu.com/) to manage the uWSGI process, so I add [a line to the resource](https://docs.chef.io/resource_service.html) specifying Upstart as the provider.

I run the cookbook again. No errors!

## Debugging

Once the `deploy` recipe is run for the first time, I SSH into the instance and poke around. The most recent code is in `/srv/www/thena/current/thena/`, exactly where it should be. I check for webserver processes:

```
ubuntu@aether:~$ ps -aux | grep nginx
root     30369  0.0  0.1  85880  1388 ?        Ss   Nov11   0:00 nginx: master process /usr/sbin/nginx
www-data 30370  0.0  0.1  86264  1816 ?        S    Nov11   0:00 nginx: worker process
www-data 30371  0.0  0.1  86264  1816 ?        S    Nov11   0:00 nginx: worker process
www-data 30372  0.0  0.2  86264  2308 ?        S    Nov11   0:00 nginx: worker process
www-data 30373  0.0  0.1  86264  1816 ?        S    Nov11   0:00 nginx: worker process
ubuntu   30809  0.0  0.0  10460   916 pts/0    S+   00:15   0:00 grep nginx

ubuntu@aether:~$ ps -aux | grep uwsgi
ubuntu   30336  0.0  0.7  47772  7352 ?        Ss   Nov11   0:00 uwsgi --ini thena-uwsgi.ini
ubuntu   30351  0.0  2.9 156764 30368 ?        S    Nov11   0:00 uwsgi --ini thena-uwsgi.ini
ubuntu   30352  0.0  2.9 156276 29820 ?        S    Nov11   0:00 uwsgi --ini thena-uwsgi.ini
ubuntu   30353  0.0  3.0 156632 30500 ?        S    Nov11   0:00 uwsgi --ini thena-uwsgi.ini
ubuntu   30786  0.0  0.0  10460   912 pts/0    S+   00:14   0:00 grep uwsgi
```

Excellent, the webserver is running. As a test, I kill the uWSGI processes and run the `deploy` command from the OpsWorks console. uWSGI is brought back up. More excellence. I hop onto Chrome to test the site.

Nothing. 502 errors every time. Frustrating. I check the uWSGI logs:

```
Traceback (most recent call last):
...
  File "./app/models.py", line 44, in load_user
    return User.query.get(int(user_id))
  File "/usr/local/lib/python2.7/dist-packages/flask_sqlalchemy/__init__.py", line 454, in __get__
    return type.query_class(mapper, session=self.sa.session())
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/orm/scoping.py", line 71, in __call__
    return self.registry()
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/util/_collections.py", line 988, in __call__
    return self.registry.setdefault(key, self.createfunc())
  File "/usr/local/lib/python2.7/dist-packages/flask_sqlalchemy/__init__.py", line 704, in create_session
    return SignallingSession(self, **options)
  File "/usr/local/lib/python2.7/dist-packages/flask_sqlalchemy/__init__.py", line 157, in __init__
    bind = options.pop('bind', None) or db.engine
  File "/usr/local/lib/python2.7/dist-packages/flask_sqlalchemy/__init__.py", line 816, in engine
    return self.get_engine(self.get_app())
  File "/usr/local/lib/python2.7/dist-packages/flask_sqlalchemy/__init__.py", line 833, in get_engine
    return connector.get_engine()
  File "/usr/local/lib/python2.7/dist-packages/flask_sqlalchemy/__init__.py", line 496, in get_engine
    self._sa.apply_driver_hacks(self._app, info, options)
  File "/usr/local/lib/python2.7/dist-packages/flask_sqlalchemy/__init__.py", line 775, in apply_driver_hacks
    if info.drivername.startswith('mysql'):
AttributeError: 'NoneType' object has no attribute 'drivername'
[pid: 21370|app: 0|req: 1/1] 129.236.232.24 () {44 vars in 955 bytes} [Mon Nov  9 20:52:44 2015] GET / => generated 0 bytes in 11 msecs (HTTP/1.1 500) 0 headers in 0 bytes (0 switches on core 0)
```

Wat. None of these words look familiar. Seems something databasey. I plug the error into Google, the results suggest a configuration error. Everything had been running fine before! (I had previously set up the server manually, it had been running successfully for a few months without any problems). I know things **had** been working. What's changed?

First, I replace `wsgi.py` (the module which wraps the whole Flask app in a callable that is passed to the uWSGI process) with the same hard-coded "Hello World!" I had used for local development. I restart the webserver and load http://thena.io. I see the "Hello World!" message, confirming that the issue is not with nginx or uWSGI, but rather with Flask. This is progress.

This smells like a user/permissions issue. I SSH into the instance to see if I can connect to the database manually. I can -- so I know the database is up and accessible. It must be that the database isn't getting configured correctly when starting uWSGI.

I check the Flask config file, where I see this line:

{% highlight python %}
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
{% endhighlight %}

So, the database is coming from the environment. I check the environmental variables, and see that DATABASE_ENV is defined just fine. Hmm. [I decide to learn about envronmental variables](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps). I learn that environmental variables are pretty temporary. They do not persist between shell sessions (unless saved in `.bash_profile`, `/etc/environment`, or similar location so they can be initialized at the start of every shell session). They are not passed from parents to children (so if you define a variable in a child process, the parent process will not have access to it). Running commands as sudo resets the environment (in the context of that one command), so commands run as sudo cannot access variables defined for the logged-in user.

I do some experiments, and realize that `DATABASE_URL` is defined for the `ubuntu` user, but **not** for `root`. I suspect that when Chef restarts the uWSGI process, it is running the command as `root` and therefore `DATABASE_URL` is not defined in that environment. I check this by hard-coding the database url in `config.py` and restarting uWSGI.

The site works! I am relieved. Now the challenge is to figure out an elegant way to pass the database info to uWSGI. Hardcoding it is not an option. It must come from the environment in some way. There should be as small a gap as possible between introducing the variable and starting the uWSGI process, to minimize the chance of the bug returning due to some minor unrelated change. I do a search on "environment variables uwsgi" and learn that you can specify environmental variables in a `.ini` file. I read the OpsWorks documentation and realize that environmental variables defined inside the OpsWorks console are available as attributes for Chef. My solution is to add the following line to my template `thena-uwsgi.ini.erb`:

{% highlight ruby %}
env DATABASE_URL="<%= node['deploy']['thena']['environment_variables']['DATABASE_URL'] %>"
{% endhighlight %}

Seems like a good solution. Since we are always going to be starting uWSGI through Upstart, adding the variable to the Upstart script seems like the perfect location. It will be hardcoded in the file, meaning the variable will be available to uWSGI *regardless* of what user is actually starting uWSGI.

I update the cookbook and re-deploy. It works! Hooray.

I click a few links on the site; everything seems to be working nicely. I go to the homepage and immediately get another 502! I refresh and the site loads fine. WHAT IS THIS? I check the uWSGI logs again and see this:

```
Traceback (most recent call last):
...
  File "./app/main/views.py", line 22, in index
    num_arcs = Arc.query.count()
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/orm/query.py", line 2735, in count
    return self.from_self(col).scalar()
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/orm/query.py", line 2504, in scalar
    ret = self.one()
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/orm/query.py", line 2473, in one
    ret = list(self)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/orm/query.py", line 2516, in __iter__
    return self._execute_and_instances(context)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/orm/query.py", line 2531, in _execute_and_instances
    result = conn.execute(querycontext.statement, self._params)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/base.py", line 914, in execute
    return meth(self, multiparams, params)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/sql/elements.py", line 323, in _execute_on_connection
    return connection._execute_clauseelement(self, multiparams, params)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/base.py", line 1010, in _execute_clauseelement
    compiled_sql, distilled_params
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/base.py", line 1146, in _execute_context
    context)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/base.py", line 1341, in _handle_dbapi_exception
    exc_info
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/util/compat.py", line 199, in raise_from_cause
    reraise(type(exception), exception, tb=exc_tb)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/base.py", line 1139, in _execute_context
    context)
  File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/default.py", line 450, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) SSL SYSCALL error: EOF detected
 [SQL: 'SELECT count(*) AS count_1 \nFROM (SELECT arcs.id AS arcs_id, arcs.created_at AS arcs_created_at, arcs.updated_at AS arcs_updated_at, arcs.user_id AS arcs_user_id, arcs.tail AS arcs_tail, arcs.head AS arcs_head, arcs.tail_url AS arcs_tail_url, arcs.head_url AS arcs_head_url \nFROM arcs) AS anon_1']
 [pid: 29957|app: 0|req: 33/225] 184.152.70.185 () {44 vars in 955 bytes} [Wed Nov 11 23:55:21 2015] GET / => generated 0 bytes in 9 msecs (HTTP/1.1 500) 0 headers in 0 bytes (0 switches on core 0)

```

I google the error and learn that this is a well-known bug when using uWSGI, Flask, and psycopg2 (the Postgres python driver), involving a feature called ["Copy on Write"](https://en.wikipedia.org/wiki/Copy-on-write).

When uWSGI starts, it begins as a master process, and then forks off into some number of child processes (in my case, 5). As a memory-saving optimization, uWSGI will write the application to memory once, and then spin off child processes which all read from one shared version of the app. Only when the child process needs to actually *write* some information (as opposed to read) does it take its own space in memory. This feature saves memory by ensuring that parts of the application which are static and read-only are not duplicated unecessarily.

The bug was due to the fact that the database threadpool (a fixed number of connections to the database, which are requested and relinquished as needed) was being created once and then shared by all of the child uWSGI processes. I am uncertain as to the specific failure, but this sharing is unintentional and was causing these requests to trip on each other. The answer was to update the `thena-uwsgi.ini` to add `lazy-apps = true`. This setting causes each child process to load the entire app from scratch, ensuring each process as a dedicated threadpool. Slightly less memory-efficient, but more stable.

From the uWSGI docs themselves:

> uWSGI tries to (ab)use the Copy On Write semantics of the fork() call whenever possible. By default it will fork after having loaded your applications to share as much of their memory as possible. If this behavior is undesirable for some reason, use the lazy-apps option. This will instruct uWSGI to load the applications after each worker’s fork().

I update the cookbook and re-deploy. Everything works great again!

## Final Touches

We can now configure and deploy an EC2 instance to serve Thena at the touch of a button. But to touch that button, we still have to log in to OpsWorks. What if we could deploy the app every time we made a commit? Well, we can!

GitHub has an [integrations](https://github.com/integrations) feature which makes this easy. We go to the [Thena repository](https://github.com/kronosapiens/thena), and under settings, we set up an integration with OpsWorks. It's pretty simple: you plug in the OpsWorks "stack" and "app" IDs, which you can find in the descriptions of the stack and app, respectively. Then you pass in an AWS access code and secret access code (which you can generate via [AWS identity management](https://console.aws.amazon.com/iam/home?#security_credential). That's it! Every time you push to the repository, GitHub will ping OpsWorks and start a deploy.

And with that, we have built **a full automatic deployment pipeline**, using a minimal Chef cookbook that we wrote ourselves, in which we understand the purpose of every setting. This is the level of control and reliability that can serve as a solid and extensible foundation for whatever comes next. We are able to focus 100% of our attention now to the development of Thena, confident in our knowledge that the site keep itself up and running.

What an adventure this has been!

Open questions:

1. Why was OpsWorks unable to fetch the repo from GitHub using SSH? The HTTPS workaround will be sufficient as long as we are fetching public repositories. If we ever have to serve a private repo, we'll need SSH access.

2. Why was nginx returning a 502 error when uWSGI was returning a 500? Seems peculiar.

**You can see the full cookbook in all its glory [here](https://github.com/kronosapiens/chef-repo/tree/master/thena-infra).**