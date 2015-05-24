---
layout: post
title: "Setting up Auto-Indent in Sublime Text 2"
date: 2014-02-09 23:48:25 -0500
comments: true
categories:
- Sublime Text 2
- Workflow
- Keyboard Shortcuts

---

When I was in undergrad and programming in Scheme, I used the well-known editor Emacs. Emacs was a curious program -- oriented towards power-users, with byzantine keyboard commands. It had strengths, though -- the least of which was its very satisfying auto-indent feature. By selecting a line and punching in some shortcut, Emacs would automatically indent an entire section to fit style and convention. It was a great way to polish off some code that had gotten a bit rough over many rounds of editing. There's something very satisfying about seeing your code get perfectly indented in one virtuosic stroke.

Switching to Sublime Text 2, I worried that the days of blissful auto-indent were over, and that I would have to consign myself to the mines of manual indentation. Imagine my relieved surprise when I learned that Sublime, thoughtful editor that it is, can auto-indent as well. It's a bit of an obscure feature (strangely), but fairly easy to set up:

<!--more-->

Navigate to "Sublime Text 2" -> "Preferences" -> "Key Bindings - User", which will bring up a preferences file.
 
Copy this code between the square brackets:
 
`{ "keys": ["command+option+i"], "command": "reindent"}`

(feel free to change the shortcut to whatever you like)

If you'd rather access the feature through the menu interface, you can find it under Edit -> Line -> Reindent.
 
And there was much rejoicing among the people.

More info: https://stackoverflow.com/questions/9495007/indenting-code-in-sublime-text-2