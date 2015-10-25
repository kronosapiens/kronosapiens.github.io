---
layout: post
title: "Permissions and Chef, part I"
comments: true
categories: blog
tags:
- infrastructure
- aws
- unix
- chef

---

Enough.

{% highlight bash %}
~$ chmod 777 <some_file> # Until it works
{% endhighlight %}

It has gone too far.

{% highlight bash %}
~$ sudo !! # Fingers crossed
{% endhighlight %}

This ends **today.**

### 1. Motivation

In the past, when setting up infrastructure or working with systems, I generally neglected the management of users and groups on the system I was administering. If I ran into a permissions error when trying to access a file (usually a log file), I would `chmod` away, like a Viking en route to Valhalla, until the file would yield. If I ran into a permissions error while running a command, a hearty `sudo !!` has generally done the trick. These are the hacks of someone overextended and in a hurry, not someone calm and in control. Solutions like these are withdrawals against the account of technical debt, and are not appropriate for the serious and precise builders of things of consequence.

I've spent the past few weeks piecing together a little side project, [thena.io](http://thena.io). It's a system which combines a conventional Flask app with a Chrome extension, to (in theory) learns your interests by finding patterns in your Wikipedia browsing. Version 0.1 of the project was building an MVP [extension](https://chrome.google.com/webstore/detail/thena/edkbcffelaeaoedocffeocbhoncfjcgl?hl=en-US&gl=US) and [app](http://thena.io), and deploying it on AWS OpsWorks. The purpose of the 0.1 exercise was to erect a system with the fewest possible files and dependencies, to know the location of every project file, to understand the purpose of every line.

Version 0.1 went up, and it was time to begin 0.2. If 0.1 was about understanding the minimum, 0.2 was about doing infrastructure properly. OpsWorks provides (easy) integration with [Chef](https://www.chef.io/), the popular infrastructure management tool. I had worked with Chef at a past company, but having at one point been explicitly discouraged from "spending too much time reading documentation" and instead advised to keep hacking things together until they worked, my exposure had been mostly glueing together new recipes by mimicking the structure of what already existed.

I believe very strongly in building methodically on solid foundations. Now that Thena 0.1 was out the door, it was time to stop, breathe, and learn how to properly configure a system.

By this point, I had a working knowledge of users and permissions in [Unix-like systems](https://en.wikipedia.org/wiki/File_system_permissions), having developed applications on machines running both OSX and Ubuntu. I knew about root users and general users, file ownership and permissions, and process control. What I lacked was a general theory on how to structure ownership and control in the deployment of a web application. Given that I was going to be using Chef to manage Thena moving forward, I wanted to create a cookbook (a set of files defining a server setup) that would set things up properly, and which would work in a variety of as-yet-unknown environments.

### 2. Goals and Questions

For Thena 0.2, I wanted:

- To be able to deploy new code with a single button.
- To be able to spin up a new, fully-functional EC2 instance with a single button.
- To configure the deployment in the most secure way possible (the minimum permissions possible).
- The deployment to be as provider-agnostic as possible.

Some questions that would need to be answered:

- Which user should install the app-specific packages?
- Which user should own the webserver configuration and log files?
- What should the permissions be for the webserver configuration and log files?
- Which user should execute the actual webserver processes?

Throughout this process, I intend to experiment and develop what is essentially the Thena DevOps cookbook on two platforms. First, Chef's excellent [Test Kitchen](http://kitchen.ci/) for local development. Then, Amazon's OpsWorks for final testing and production. This means that the cookbook will need to run correctly in both environments, taking into account subtle differences in the defaults on both platforms.

### 3. Learning

# File Details

The `ls` command will list the contents of a directory. Running `ls` with the `-l` flag will show you the contents of the directory in great detail. It this detailed view that tells gives us the ownership and permission information that we want.

Here is an the example of this detail:

{% highlight bash %}
ls -l /path/to/dir
-rwxrwxrwx 1 root root 128 Aug 10 05:13 yourfile.txt
{% endhighlight %}

Of these details, the portion which appears `-rwxrwxrwx`, also known as the "mode" of the file, tells us the permissions associated with the file. The portion which appears `root root` tells us who owns the file. Together, these two pieces of information tell us what we want to know.

# Ownership

Although mode is displayed first, it will be more helpful to first look at owner and group settings. Looking at `root root`, we see that the file is owned by the `root` **user**, and is placed in the `root` **group**. In this case the user and group happen to have the same name -- they won't always. In the example below, the mysteriously-named `shadow` file is owned by the `root` user and in the `shadow` group:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ ls -l /etc
...
-rw-r----- 1 root shadow   765 Oct 21  2014 shadow
...
{% endhighlight %}

From this, we learn an important fact about files in Unix-like systems: they are owned by a `user` and placed in a `group`. This means that by adding users to various pre-defined groups, those users (who may not themselves own any files) will have special access to files they do not personally own. From this we can infer some design principles in these systems:

- A individual user account has principal responsibility for a file, and will enjoy the greatest control over the file.
- Generic users will have equal or less access to the file than the owner. In cases of critical, sensitive files, they may not be able to access them at all.
- Some restricted files may need to be accessed by a special group of users who are not themselves the owner of the file -- these users are assigned to the group which contains the file.

These principles themselves are attempts to handle the "freedom vs. control" problem that plagues any system in which multiple agents interact in an environment of incomplete trust. Given that this is the system we have inherited today, we can further infer that it either works well enough in most cases, or that it would be very inconvenient to try and change it.

Moving on.

# Mode

Looking at the mode, we see that it consists of ten characters: a leading hyphen, followed by three triads ([codons](https://en.wikipedia.org/wiki/DNA_codon_table)??).

In Unix, "[everything is a file](https://en.wikipedia.org/wiki/Everything_is_a_file)". As such, the leading hyphen (`-`) tells us the [file type](https://en.wikipedia.org/wiki/Unix_file_types) of the file. In the case of `yourfile.txt`, the type is simply a file, known as a "normal" file. Other kinds of files, known as "special" files, include directories (`d`), links (`l`), named pipes (`p`), sockets (`s`), device files (`c` or `b`), and doors (`D`). Most of the files we'll be working with will be normal files, but it's good to know that other kinds of files can be manipulated the same way.

The next nine characters (the three triads) represent the kinds of ways that different people can use the file. Each triad represents a different role in the system:

- The first triad represents the permissions granted to the **owner** of the file.
- The first triad represents the permissions granted to members of the **group** containing the file.
- The first triad represents the permissions granted to **everyone else**.

A single triad consists of three characters, present or absent, always in the same order: `rwx`. These represent the following:

- `r`: the read permission
- `w`: the write permission
- `x`: the execute permission

Quoting directly [from Digital Ocean](https://www.digitalocean.com/community/tutorials/an-introduction-to-linux-permissions
) [emphasis mine]:

> **Read**
> For a normal file, read permission allows a user to view the contents of the file.
> For a directory, read permission allows a user to view the **names** of the file in the directory.

> **Write**
> For a normal file, write permission allows a user to modify and delete the file.
> For a directory, write permission allows a user to delete the directory, modify its contents (create, delete, and rename files in it), and modify the contents of files that the user can read.

> **Execute**
> For a normal file, execute permission allows a user to execute a file (the user must also have read permission). As such, execute permissions must be set for executable programs and shell scripts before a user can run them.
> For a directory, execute permission allows a user to access, or traverse, into (i.e. `cd`) and **access metadata** about files in the directory (the information that is listed in an `ls -l`).

Groovy. From this we note that the execute permission must be accompanied by the read permission, or else execution is impossible. The write permission *should* be also accompanied by read (or else you're writing to a file you can't see), but doesn't have to be.

As an exercise, let's interpret the following triads:

- `rwx`: Total control
- `rw-`: Can read and write, but not execute
- `r-x`: Can read and execute, but not write
- `r--`: Can read, but nothing else
- `---`: Can't do anything

From this we can note that although there's 2^3 = 8 possible triads, there are only 5 which make sense. And given that we expect group permissions to be equal or lesser than owner permissions, and general user permissions to be equal or lesser than group permissions (owner >= group >= user), there is a sort of [lower-triangular](https://en.wikipedia.org/wiki/Triangular_matrix) nature to the space of possible permissions. This means that of the 5^3 = 125 possible combinations of reasonable triads, only about half of them are consistent with the principle of descending permissions. This means that there are about ~60 different modes of a file that we could concievably expect to encounter. My suspicion is that a far fewer number of modes represent majority of use cases. Let's briefly consider two examples:

- `-rw-rw-r--`: A file which the owner and group can write to, but which other users can only read. A `README.md` could be an example of this.
- `-rwxr-xr-x`: A file which the owner can write to, but which all others can execute. A complex but useful  `bash` script could be an example of this.

Let's continue.

# File Permissions in Practice

Let's log into the Test Kitchen virtual server and mess around a little:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ ls -l /etc/lvm
total 44
drwx------ 2 root root  4096 Oct 21  2014 archive
drwx------ 2 root root  4096 Oct 21  2014 backup
-rw-r--r-- 1 root root 36436 Dec 13  2013 lvm.conf

vagrant@default-ubuntu-1404:~$ ls -l /etc/lvm/archive/
ls: cannot open directory /etc/lvm/archive/: Permission denied
{% endhighlight %}

What happened? Here we see that I'm logged in as the user `vagrant`, which we can tell by looking at the `vagrant@default-ubuntu-1404` portion of the command prompt. This user is able to `ls` the `/etc/lvm` directory, where we see the directory `archive` is owned by `root root` and has mode `drwx------`. If our understanding of permissions is correct, this means that I, as user `vagrant`, should not have any access to this directory. This is correct, as I receive an error when I try to `ls` the contents of `/etc/lvm/archive/` (since I don't have read permission). Let's keep going:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ sudo chmod 704 /etc/lvm/archive

vagrant@default-ubuntu-1404:~$ ls -l /etc/lvm/
total 44
drwx---r-- 2 root root  4096 Oct 21  2014 archive # Permissions have changed!
drwx------ 2 root root  4096 Oct 21  2014 backup
-rw-r--r-- 1 root root 36436 Dec 13  2013 lvm.conf

vagrant@default-ubuntu-1404:~$ ls -l /etc/lvm/archive/
ls: cannot access /etc/lvm/archive/vagrant-vg_00000-929473501.vg: Permission denied
total 0
-????????? ? ? ? ?            ? vagrant-vg_00000-929473501.vg

vagrant@default-ubuntu-1404:~$ sudo chmod 705 /etc/lvm/archive

vagrant@default-ubuntu-1404:~$ ls -l /etc/lvm/
total 44
drwx---r-x 2 root root  4096 Oct 21  2014 archive # Permissions changed again!
drwx------ 2 root root  4096 Oct 21  2014 backup
-rw-r--r-- 1 root root 36436 Dec 13  2013 lvm.conf

vagrant@default-ubuntu-1404:~$ ls -l /etc/lvm/archive/
total 4
-rwx------ 1 root root 1679 Oct 21  2014 vagrant-vg_00000-929473501.vg
{% endhighlight %}

What happened this time? I used the `chmod` command with `sudo` to modify the permissions of the `/etc/lvm/archive/` directory. First, I gave myself `read` permission, which allowed me to see just the **name** of the one file in the directory. Then, I added the `execute` permission, which allowed me to see additional details about the file.

`sudo` is an important command that we haven't seen yet, but is about to become important. Last note: unliked some other systems, permissions in Unix-like systems **are not inherited**. It is possible for a file in a directory to be more or less restricted than the directory itself.

Finally, you'll note that I passed a number (`704`, `705`) to `chmod`, rather than a mode like `-rwxrwxrwx`. These numbers, known as "numeric notation" or "octal notation" for mode, represent the same information. The three numbers map to the three triads, and each number represents permissions as follows:

- `0`: `---`
- `1`: `--x`
- `2`: `-w-`
- `3`: `-wx`
- `4`: `r--`
- `5`: `r-x`
- `6`: `rw-`
- `7`: `rwx`

So we see how `704` maps to `-rwx---r--` and `705` maps to `-rwx---r-x`, which is what we needed. Let's keep tinkering.

# Managing Users and Groups

There are a number of commands we'll rely on to manage the users and groups on our system. Let's take a brief inventory here:

- `users`: list all the users
- `adduser`: add a new user (`useradd` provides similar functionality)
- `deluser`: delete a user (add the `--remove-home` option to delete the user's home directory)
- `usermod`: modify a user
- `groups`: list all the groups
- `groupadd`: add a new group
- `groupdel`: delete a group
- `groupmod`: modify a group
- `gpasswd`: add/remove users from groups
- `chmod`: change the permissions of a file
- `chown`: change the owner of a file
- `chgrp`: change the group the file is in
- `su`: switch to another user (may have to provide a password)
- `sudo`: short for "super user do", this allows the current user to act as `root`
- `visudo`: a shortcut to edit the `/etc/sudoers` file, which keeps track of who can use `sudo`
- `umask`: change the *default* permissions given to a new file

A few notes:

When you create a user with `adduser`, you automatically create a group with the same name, and place the user in that group (as the sole member). This group becomes the new user's default group (the group that all files created by that user are placed in). This is generally seen as sensible and desirable default behavior.

The all important `sudo` command is controlled in two ways: by editing the file located at `/etc/sudoers`, and by updating the `sudo` group. For a non-`root` user to be able to use the `sudo` command, they must either be included in `/etc/sudoers`, or be a member of the `sudo` group.

To add a user to the `sudo` group, execute either of the following:

{% highlight bash %}
$ gpasswd -a <username> sudo # From the group perspective

# or

$ usermod -a -G sudo <username> # From the user perspective
{% endhighlight %}

To see the **full** list of users (beyond what is printed by running `users`), run `cat /etc/passwd`. This will print detailed information about every user account (even those created specifically for certain services or applications). An analogous operation can be performed for groups using `cat /etc/group`.

Finally, it is important to note that the base permissions given to a newly-created file are `666`, representing read and write access for everyone. For a newly-created directory, they are `777`, representing the additional need to "execute" a directory to see its contents.

The `umask` command is used to adjust these defaults to something more secure. The way `umask` works is by decreasing the scope of permissions, by "masking" the default value of `666` or `777`. Consider a umask setting of `002` (the default). A umask setting of `002` will turn the default `666` into a `664`, and the default `777` into a `775`. Changing umask to `077` will turn the default `666` into `600`, and `777` into `700`, which is much more restrictive. `umask` defaults to `002`, and can be modified on a per-session basis, or permanently by adding the desired value to the user's `.bash_profile`. This is not something that we will be using here, but it good to know about regardless.

# Process Permissions

The last topic of our general learning will be process permissions. We now understand how permissions are assigned to **files**. What we have yet to discuss is how permissions are assigned to **processes**.

A process is created when a user executes a file. This obviously requires that user to have execute permission, which has been discussed at length above. When the process is created, it itself acquires certain permissions, which allow the process to interact with other files in the system.

By default, the process inherits permissions from the user which began ("spawned") the process. As such, running a command as `root` or with `sudo` gives the resulting process greater power to change the system than if it was run as a regular user. Certain commands require additional privileges, while others do not. As an exercise, let's use the `ps -aux` command to view some of our currently-running processes:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ ps -aux | head
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.6  33504  2480 ?        Ss   15:26   0:01 /sbin/init
root         2  0.0  0.0      0     0 ?        S    15:26   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    15:26   0:00 [ksoftirqd/0]
root         4  0.0  0.0      0     0 ?        S    15:26   0:00 [kworker/0:0]
root         5  0.0  0.0      0     0 ?        S<   15:26   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    15:26   0:00 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    15:26   0:00 [rcuos/0]
root         9  0.0  0.0      0     0 ?        S    15:26   0:00 [rcu_bh]
root        10  0.0  0.0      0     0 ?        S    15:26   0:00 [rcuob/0]

vagrant@default-ubuntu-1404:~$ ps -aux | tail
root     11146  0.0  0.3  85872  1368 ?        Ss   15:29   0:00 nginx: master process /usr/sbin/nginx
www-data 11147  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
www-data 11148  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
www-data 11149  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
www-data 11150  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
root     11151  0.0  1.1 103560  4144 ?        Ss   15:54   0:00 sshd: vagrant [priv]
vagrant  11169  0.0  0.5 103560  1876 ?        S    15:54   0:00 sshd: vagrant@pts/0
vagrant  11170  0.0  1.0  22448  3760 pts/0    Ss   15:54   0:00 -bash
vagrant  11238  0.0  0.3  18448  1292 pts/0    R+   17:31   0:00 ps -aux
vagrant  11239  0.0  0.1   7236   680 pts/0    S+   17:31   0:00 tail
{% endhighlight %}

Here we see the ten oldest and the ten newest processes currently running. Note how the older processes (with `PID`, or process ID, 1-10) are all being run as `root`. These are critical system processes, and require freedom to modify the system at any level. The newer processes are application processes -- `nginx`, the front-end reverse proxy webserver, and the processes I initiated by running my own commands. These newer processes do not need (and in fact, should not have) power to edit the system beyond what they need for their specific application tasks. Being run by users `www-data` and `vagrant`, these processes have the permissions of those users.

In general, processes inherit the permissions of the users who began them. It is possible, in some cases, to configure a file to run with permissions **independent** of the user which executed the file. This is accomplished with the `setuid` and `setgid` flags. These flags, set using `chmod`, can configure a file to execute using the identity of its *owner* or *group*, and **not** the identity of the user who executed the file.

For example, let's consider the file at `/usr/bin/passwd`:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 47032 Feb 17  2014 /usr/bin/passwd
{% endhighlight %}

Here we see that the first triad appears `rws`, instead of the usual `rwx`. This means that the `setuid` bit has been set for this file, meaning that it will always be executed as `root`, regardless of the user which executes the file. Note that the real user still needs permission to execute the file -- the difference is that, once executed, it will be run as `root`. Let's temporarily remove execute permission for other users:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ sudo chmod 4754 /usr/bin/passwd # The leading 4 corresponds to turning setuid on.

vagrant@default-ubuntu-1404:~$ ls -l /usr/bin/passwd
-rwsr-xr-- 1 root root 47032 Feb 17  2014 /usr/bin/passwd # Note how the last x was dropped

vagrant@default-ubuntu-1404:~$ /usr/bin/passwd
-bash: /usr/bin/passwd: Permission denied
{% endhighlight %}

Note how the numerical argument to `chmod` was four digits instead of the usual three. The first character represents the new setting -- 4 represents `setuid`, while 2 would represent `setgid`. As with the other digits, a 6 would have activated both `setuid` and `setgid`. As an aside, you can always provide a four-digit argument to `chmod` -- if you don't, the first digit is taken as 0.

Let's restore execute permission and try executing the file [output edited for clarity]:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ sudo chmod 4755 /usr/bin/passwd # Restore execute permission for user vagrant

vagrant@default-ubuntu-1404:~$ /usr/bin/passwd & ps -aux | tail
root     11284  0.0  1.1 103560  4148 ?        Ss   17:51   0:00 sshd: vagrant [priv]
vagrant  11302  0.0  0.5 103560  1880 ?        S    17:51   0:00 sshd: vagrant@pts/0
vagrant  11303  0.0  0.9  22436  3616 pts/0    Ss   17:51   0:00 -bash
root     11324  0.0  0.4  58352  1556 pts/0    T    17:57   0:00 /usr/bin/passwd # Note how this process is running as root
vagrant  11325  0.0  0.3  18448  1292 pts/0    R+   17:57   0:00 ps -aux # But this one is not
vagrant  11326  0.0  0.1   7236   676 pts/0    S+   17:57   0:00 tail

[1]+  Stopped                 /usr/bin/passwd
{% endhighlight %}

Here we see how the `setuid` and `setgid` flags can be used to provide even greater control over how processes are created.

For much of the above, thanks are owed to the following:

<https://www.digitalocean.com/community/tutorials/linux-permissions-basics-and-how-to-use-umask-on-a-vps>
<https://www.digitalocean.com/community/tutorials/an-introduction-to-linux-permissions>
<https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-14-04>
<https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file-on-ubuntu-and-centos>
<https://wiki.archlinux.org/index.php/Users_and_groups>
<https://en.wikipedia.org/wiki/File_system_permissions>
<https://en.wikipedia.org/wiki/Setuid>

### 4. Deploying the Server

Now that we've learned something about how to structure permissions on a server, let's turn to the question of the deployment. What processes will need to be running, and as which users? What permissions will those users need to have?

In general, we will need two processes to be running for the app to be live and accessible from the internet:

- `nginx`, the front-end reverse proxy webserver which will listen on the HTTP/HTTPS ports and receive requests from the internet
- `uwsgi`, the webserver which will encapsulate the Flask code and process all requests

**NGINX**
Let's see what happens when we install `nginx`, without changing any settings:

{% highlight bash %}
vagrant@default-ubuntu-1404:~$ ps -aux | grep nginx
root     11146  0.0  0.3  85872  1368 ?        Ss   15:29   0:00 nginx: master process /usr/sbin/nginx
www-data 11147  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
www-data 11148  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
www-data 11149  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
www-data 11150  0.0  0.4  86240  1792 ?        S    15:29   0:00 nginx: worker process
{% endhighlight %}

Observe how there are five `nginx` processes running. The first one is the master process, run as `root`. This process [spawned](https://en.wikipedia.org/wiki/Fork_%28system_call%29) four worker processes, being run as the restricted user `www-data`. Generally, only `root` processes can listen on ports below 1024. Given that HTTP uses port 80 and HTTPS uses port 443, it is necessary that `nginx` have some root access. The child processes are then run with reduced access for security. [Some people on the internet](http://unix.stackexchange.com/questions/134301/why-does-nginx-starts-process-as-root) are of the opinion that this is not a problem, because `nginx` itself does not actually handle the requests, merely passes them to other processes (in our case, `uwsgi`), which makes sense to me.

**UWSGI**
The [uWSGI docs](http://uwsgi-docs.readthedocs.org/en/latest/ThingsToKnow.html) explicitly warn us:

> Common sense: do not run uWSGI instances as root. You can start your uWSGIs as root, but be sure to drop privileges with the uid and gid options.

Why is this? uWSGI (the main webserver process) is receiving requests from the internet. This makes the uWSGI process a potential vulnerability and source of attack: if a malicious agent were able to gain control of the uWSGI process via a malformed request, that agent could then act against your system, limited only by the permissions given to the uWSGI process, which are the permissions held by the user which began the process.

So how do we run `uwsgi`? The question to ask ourselves, then, is what permissions does that process (and its children) need? Given that `uwsgi` is the process which is executing the source code of our Flask app, then at a minimum it needs to be able to read (and execute) the source code. From here we can make a case that `uwsgi` should be run as the same user who owns the app's source code.

That's not all, though. We are going to configure `uwsgi` to read and write to an [internal socket](https://en.wikipedia.org/wiki/Unix_domain_socket), which will be created and owned by the process (and thus by the user which began the process). `nginx` is going to need access to this socket in order to communicate with `uwsgi`. We enable this by setting `uwsgi` to run in the `www-data` **group**. Remember, the `www-data` user is (probably) the only member of the `www-data` group. Placing `uwsgi` into that group is then tantamount to saying that the `www-data` user has access to that process and the files it creates; in this case, allowing the `www-data` user (and thus the `nginx` processes) to read and write to the shared socket file owned by `uwsgi`'s owner.

The underlying principle here is that while perfect security may be impossible (or maybe it is?), it is always wise to present "the smallest possible surface" to an attacker. Rather than have five processes at risk of being compromised, let's have just one. If a permission isn't strictly necessary, take it away.

### 5. Conclusion

We've covered a lot of ground so far, and there's a lot left to do. In this post, we did a deep dive into Unix-style user and file management, and are feeling pretty comfortable with how users, files, and permissions work on a server.

In part II of this series, we'll take a look at Chef and how to incorporate users, files, and permissions into a rock-solid piece of automated infrastructure.