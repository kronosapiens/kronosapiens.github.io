---
layout: post
title: "Maintaining Octopress themes as git submodules"
date: 2014-05-01 13:04:35 -0400
comments: true
categories: 
- development process

---

I've spent much of this week converting my technical blog onto Octopress, away from Wordpress. It's been a very pleasant experience -- my technical chops are worlds beyond what they were when I first experimented with Octopress back in February, and I'm finding that developing and maintaining an Octopress blog is a great opportunity to test out my burgeoning developer chops.

One of the first challenges I tackled was integrating a third-party theme, using git submodules. Octopress themes are generally contained within their own repos, and generally have four top-level components:

```
sass/
source/
.editorconfig
README.md
```
The substance of the theme is stored in the first two directories, `sass` and `source`. `sass` contains all of the styling for the theme, including the base bootstrap styles, custom theme styles, and placeholders for user-added styles. `source` contains all of the html, page templates, and javascript files for the theme.

<!--more-->

## Aside: 'What is a submodule?'

A submodule is a git repository which has been *included as a subdirectory* in another repository. The submodule is maintained indepenently of the 'supermodule', or main repository -- pushing to its own 'origin', keeping its own commit history, and so on. You add a submodule to a project by cloning that submodule into your main project, and in the context of development, those files are as accessible to your text editor and server as any other. From git's perspective, however, the contents of the submodule are *not* tracked by git, nor included in any of the commits of the 'supermodule'. All the supermodule keeps track of is the commit id of the version of the submodule that it is currently using -- essentially a pointer to the repository where the submodule is actually being tracked and version controlled.

Mostly, submodules work the way you expect a repo-within-a-repo would work, and while you'll need to be a bit more careful around pushing and pulling, it's a powerful and intersting feature of git. You can [read more about submodules here](http://git-scm.com/book/en/Git-Tools-Submodules).

## Installing a theme

### Cloning

You install a theme by **cloning** the theme repository into the `.themes` folder at the top level of your Octopress directory *as a submodule*. In essence, you are cloning a self-contained repo *into* another repo (in this case, your Octopress blog). If you check your remotes, you'll notice that the remotes for the theme repository point back to the creator of the theme, while the remotes in the rest of the repository point back to your own Github account.

If you navigate to the theme files in your command line, you'll notice that the repo name changes as you navigate into the theme directory. Any git status checks, commits, and pushes will take place within the context of the repo you are currently in. Commits made to the theme repo will only affect the theme repo, while commits made elsewhere will affect the overall Octopress repo.

### Installing

To install, navigate to the top level of your Octopress directory and run `rake install['ThemeName']`. The `install` command will essentially *copy* all of the files in `.themes/ThemeName` into your `source` folder, overrwriting any previous themes.

Note that this is the point at which files are copied from the *theme* repo (the submodule) into the main Octopress repo (the 'super' module). When you commit your site now, the files which were copied from the theme directory into the `source` directory will be committed to the main Octopress repository.

## Maintaining a theme

Now that you've installed the theme, you might be wondering what the workflow is for updating and changing the theme. There are three ways you might go about this, with differing amounts of complexity and benefit. They are, in ascending order of difficulty:

* Editing the theme files in your `source` directory
* Updating the files in the `.themes/ThemeName` directory locally
* Forking the theme, updating the files in the theme directory, and making a pull request to the theme creator

### Editing files in your `source` folder

The easiest way to make changes to your theme is to edit the files in your `source` directory. When Octopress generates your site, it uses the templates and styles in `source`. By running `rake preview` and editing files in `source`, you can get near-instant feedback on site changes. Most sandbox editing should be done in this way -- it's the safest and easiest way to play around with your theme.

### Updating files in your theme directory

The downside of editing your theme in the `source` directory is that all of those changes will be lost if and when you decide to install a new theme. A more permanent way to change a theme is to make changes in the `.themes/ThemeName` directory. This way, your changes will be preserved in the case you want to change themes, because a future re-install of ThemeName will include your changes.

The workflow I recommend is to treat the `source` directory as your sandbox, and to copy your changes over to the theme directory when you're satisfied with the results.

*Now, if you're never planning on downloading any updated versions of the theme, and have no desire to try and have your changes incorporated into the theme so that others can use them, then this will probably be enough for you. However, if you plan on maintaining the theme and installing future updates, or have a desire to share your changes with the larger community, then you'll probably want to consider this last option:*

### Forking the theme, updating the files, and making a pull request

The limitation to updating the files in the theme directory *locally* is that you run into problems as the theme evolves. Recall, our third-party theme is *not* a part of our blog's repository. It is an independent repo that lives within our main repository. This means that as changes are made to the theme, you'll be able to pull in and integrating those new changes.

The problem is that any changes you've made to the theme directory will be *overwritten* when you pull down new changes (there are ways around this, though, such as saving all your changes to a new branch before you pull, and merging that temporary branch into the updated master).

The solution here is, instead of simply *cloning* the theme repo into your repository, to *fork* the theme and clone *your copy*, make and push the theme changes to your forked copy of the theme, and then make a pull request back to the theme's creator.

The biggest benefits of this workflow is that your changes will benefit the entire community using the theme, and that future updates to the theme will include your changes (so that you'll never have to worry about future updates overwriting your local edits).

The biggest challenge of this method is that you must keep your changes generic -- any changes to the theme which pertain to *only you* should not be transferred onto the main theme.

To emulate this workflow, you'll need to set up a second remote pointing to the theme's original creator, from which you'll pull new updates to the theme.

For example, here is my remote configuration for the MediumFox theme:

```console
[14:25:07] (master) MediumFox
ƒ: git remote -v
origin	git@github.com:kronosapiens/MediumFox.git (fetch)
origin	git@github.com:kronosapiens/MediumFox.git (push)
sevenadrian	git@github.com:sevenadrian/MediumFox.git (fetch)
sevenadrian	git@github.com:sevenadrian/MediumFox.git (push)
```

In this example, I push all my edits to `origin`, and pull theme updates from `sevenadrian`.

## The flow

The overall flow for this last system is as follows:

1. Find a third-party theme you like and fork the repository
2. Clone your version of the repository into the `.themes/` folder of your Octopress directory.
3. Install the theme (follow the instructions on the theme, they'll be some variation of `rake install['ThemeName']`).
4. Play with the files in your `source` directory, experiment with new features and fixes, hack away and make it better. Remember, commits to your Octopress repo *won't affect* the theme repo (if you go to Github.com and explore the repo's files, you'll see that there *aren't even any files* where the theme is -- just a pointer to a specific commit in another repository).
5. When you're satisfied with your changes, edit the files in your theme's folders.
6. Push the changes to your forked copy of the theme's repository.
7. Open a pull request to the original theme and ask that your changes be merged into the main repo.
8. Smile the satisfied smile of someone who knows that they've just made a positive impact in the lives of Octopress users around the world.
9. Periodically, check for updates to the theme and pull those changes from the original theme repo.
10. Reinstall the theme to get all the new changes.
11. World peace.
12. Repeat steps 3-11 forever, as necessary.

And that's basically it. Through the power of submodules, Octopress users can enjoy and contribute to a number of third-party, open source themes, as well as get great experience managing files and collaborating with git.
