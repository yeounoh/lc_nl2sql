




Why SQLite Does Not Use Git




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Why SQLite Does Not Use Git


►
Table Of Contents
[1\. Introduction](#introduction)
[1\.1\. Edits](#edits)
[2\. A Few Reasons Why SQLite Does Not Use Git](#a_few_reasons_why_sqlite_does_not_use_git)
[2\.1\. Git does not provide good situational awareness](#git_does_not_provide_good_situational_awareness)
[2\.2\. Git makes it difficult to find successors (descendants)
of a check\-in](#git_makes_it_difficult_to_find_successors_descendants_of_a_check_in)
[2\.3\. The mental model for Git is needlessly complex](#the_mental_model_for_git_is_needlessly_complex)
[2\.4\. Git does not track historical branch names](#git_does_not_track_historical_branch_names)
[2\.5\. Git requires more administrative support](#git_requires_more_administrative_support)
[2\.6\. Git provides a poor user experience](#git_provides_a_poor_user_experience)
[3\. A Git\-User's Guide To Accessing SQLite Source Code](#a_git_user_s_guide_to_accessing_sqlite_source_code)
[3\.1\. The Official GitHub Mirror](#the_official_github_mirror)
[3\.2\. Web Access](#web_access)
[3\.3\. Fossil Access](#fossil_access)
[3\.4\. Verifying Source Code Integrity](#verifying_source_code_integrity)
[4\. See Also](#see_also)




# 1\. Introduction



SQLite does not use the
[Git](https://git-scm.org) version control system.
SQLite uses
[Fossil](https://fossil-scm.org/) instead, which is a
version control system that was specifically designed
and written to support SQLite.




People often wonder why SQLite does not use the
[Git](https://git-scm.org) version control system like everybody
else.
This article attempts to answer that question. Also,
in [section 3](#getthecode),
this article provides hints to Git users
about how they can easily access the SQLite source code.




This article is not a comparison between Fossil
and Git. See
[https://fossil\-scm.org/fossil/doc/trunk/www/fossil\-v\-git.wiki](https://fossil-scm.org/fossil/doc/trunk/www/fossil-v-git.wiki)
for one comparison of the two systems. Other third\-party
comparisons are available as well \- use a search engine to find them.




This article is not advocating that you switch your projects
away from Git. You can use whatever version control system you want.
If you are perfectly happy with Git, then by all means keep using
Git. But, if Git is not working well for you or you are wondering
if it can be improved or if there is something better,
then maybe try to understand the perspectives presented below.
Use the insights thus obtained to find or write a different and
better version control system, or to just make
improvements to Git itself.



## 1\.1\. Edits



This article has been revised multiple times in an attempt
to improve clarity, address concerns and misgivings,
and to fix errors.
The complete edit history for this document can be seen at
<https://sqlite.org/docsrc/finfo/pages/whynotgit.in>.
(Usage hint: Click on any two nodes of the graph for a diff.
BTW, are there any Git web interfaces that offers a similar
capability?)



# 2\. A Few Reasons Why SQLite Does Not Use Git


## 2\.1\. Git does not provide good situational awareness



When I want to see what has been happening on SQLite, I visit the
[timeline](https://sqlite.org/src/timeline) and in a single
screen I see a summary of the latest changes, on all branches.
In a few clicks, I can drill down as much detail as I
want. I can even do this from a phone.




GitHub and GitLab offer nothing comparable. The closest I have
found is the [network](https://github.com/sqlite/sqlite/network),
which is slow to render (unless it is already cached), does not
offer nearly as much details, and scarcely works at all on mobile.
The [commits](https://github.com/sqlite/sqlite/commits/master) view
of GitHub provides more detail, renders quickly,
and works on mobile, but only shows a single branch at a time,
so I cannot easily know if I've seen all of the recent changes.
And even if GitHub/GitLab did offer better interfaces, both are
third\-party services. They are not a core part of Git. Hence,
using them introduces yet another dependency into the project.




I am told that Git users commonly install third\-party graphical
viewers for Git, many of which do a better job of showing recent
activity on the project. That is great, but these are still
more third\-party applications that must be installed and
managed separately. Many are platform\-specific. (One of the
better ones, [GitUp](https://gitup.co/), only works on Mac, for
example.) All require that you first sync your local repository
then bring up their graphical interface on your desktop. And
even with all that, I still cannot see what I typically want to
see without multiple clicks. Checking on project status from
a phone while away from the office is not an option.



## 2\.2\. Git makes it difficult to find successors (descendants)
of a check\-in



Git lets you look backwards in time, but not forwards.
Given some historical check\-in, you can see what came before,
but it is challenging see what came next.




In contrast, Fossil offers helpful displays such as
[https://sqlite.org/src/timeline?df\=major\-release](https://sqlite.org/src/timeline?df=major-release)
to show all check\-ins that are derived from the most
recent major release.






* [All SQLite check\-ins derived from the most recent major release](https://sqlite.org/src/timeline?df=major-release)


It is not impossible to find the descendants of a check\-in
in Git. It is merely difficult. For example,
there is a
[stackoverflow page](https://stackoverflow.com/questions/27960605/find-all-the-direct-descendants-of-a-given-commit#27962018)
showing the command sequence for finding the descendants of a check\-in
in unix:




```
git rev-list --all --parents | grep ".\{40\}.*.*" | awk '{print $1}'


```


But this is not the same thing. The command above gives
a list of descendants without showing the branching structure, which
is important for understanding what happened. And the command only works
if you have a local clone of the repository; finding the descendants of
a check\-in is not something you can do with web interfaces such
as GitHub or GitLab.




This is not really about just finding the descendants of a check\-in
from time to time. The fact that descendants are readily available in
Fossil means that the information pervades the web pages provided by
Fossil. One example: Every Fossil check\-in information page
([example](https://www.sqlite.org/src/info/ec7addc87f97bcff)) shows
a small "Context" graph of the immediate predecessor and successors
to that check\-in. This helps the user maintain better situational
awareness, and it provides useful capabilities, such as the ability
to click forward to the next check\-in within a sequence. Another example:
Fossil easily shows the context around a specific check\-in
([example](https://www.sqlite.org/src/timeline?c=2018-03-16&n=10))
which again helps to promote situational awareness and a deeper
understanding of what is happening in the code. There is a
[whole page of additional examples](https://fossil-scm.org/fossil/doc/trunk/www/webpage-ex.md)
in the [Fossil documentation](https://fossil-scm.org/fossil).




All of the above is theoretically possible with Git, given the right extensions
and tools and using the right commands. But it is not easy to do,
and so it rarely gets done. Consequently, developers have less awareness
of what is happening in the code.



## 2\.3\. The mental model for Git is needlessly complex



The complexity of Git
distracts attention from the software under development. A user of Git
needs to keep all of the following in mind:


1. The working directory
2. The "index" or staging area
3. The local head
4. The local copy of the remote head
5. The actual remote head



Git has commands (and/or options on commands) for moving and
comparing content between all of these locations.



In contrast,
Fossil users only need to think about their working directory and
the check\-in they are working on. That is 60% less distraction.
Every developer has a finite number of brain\-cycles. Fossil
requires fewer brain\-cycles to operate, thus freeing up
intellectual resources to focus on the software under development.



One user of both Git and Fossil
[writes in HN](https://news.ycombinator.com/item?id=16806955):




> *Fossil gives me peace of mind that I have everything ... synced to
> the server with a single command....
> I never get this peace of mind with git.*


## 2\.4\. Git does not track historical branch names



Git keeps the complete DAG of the check\-in sequence. But branch
tags are local information that is not synced and not retained
once a branch closes.
This makes review of historical
branches tedious.




As an example, suppose a customer asks you:
"What ever became of that 'prefer\-coroutine\-sort\-subquery' branch
from two years ago?"
You might try to answer by consulting the history in
your version control system, thusly:



* **GitHub:** [https://github.com/sqlite/sqlite/commits/prefer\-coroutine\-sort\-subquery](https://github.com/sqlite/sqlite/commits/prefer-coroutine-sort-subquery)
* **Fossil:** [https://sqlite.org/src/timeline?r\=prefer\-coroutine\-sort\-subquery](https://sqlite.org/src/timeline?r=prefer-coroutine-sort-subquery)



The Fossil view clearly shows that the branch was eventually merged back into
trunk. It shows where the branch started, and it shows two occasions where changes
on trunk were merged into the branch. GitHub shows none of this. In fact, the
GitHub display is mostly useless in trying to figure out what happened.




Many readers have recommended various third\-party GUIs for Git that
might do a better job of showing historical development activity. Maybe
some of them do work better than native Git and/or GitHub, though they
will all be hampered by the fact that Git does not preserve historical
branch names across syncs. And even if those other tools are better,
the fact that it is necessary to go to a third\-party tool to get the information
desired does not speak well of the core system.



## 2\.5\. Git requires more administrative support



Git is complex software.
One needs an installer of some kind to put Git on a developer
workstation, or to upgrade to a newer version of Git.
Standing up a Git server is non\-trivial, and so most developers
use a third\-party service such as GitHub or GitLab,
and thus introduce additional dependencies.




In contrast, Fossil is a single standalone binary which is
installed by putting it on $PATH. That one binary contains all
the functionality of core Git and also GitHub and/or GitLab. It
manages a community server with wiki, bug tracking, and forums,
provides packaged downloads for consumers, login managements,
and so forth, with no extra software required. Standing up a
community server for Fossil takes minutes. And Fossil is efficient.
A Fossil server will run fine on a $5/month VPS or a Raspberry Pi,
whereas GitLab and similar require beefier hardware.




Less administration means that programmers spend more time working
on the software (SQLite in this case) and less time fussing with
the version control system.



## 2\.6\. Git provides a poor user experience


The following <https://xkcd.com/1597/> cartoon is an
exaggeration, yet hits close to home:




![](https://www.fossil-scm.org/fossil/doc/trunk/www/xkcd-git.gif)


Let's be real. Few people dispute that Git provides
a suboptimal user experience. A lot of
the underlying implementation shows through into the user
interface. The interface is so bad that there is even a
parody site that generates
[fake git man pages](https://git-man-page-generator.lokaltog.net/).



Designing software is hard. It takes a lot of focus.
A good version control system should provide the developer with
assistance, not frustration. Git has gotten better in this
regard over the past decade, but it still has a long way to go.




# 3\. A Git\-User's Guide To Accessing SQLite Source Code



If you are a devoted Git user, you can still easily access SQLite.
This section gives some hints on how to do so.



## 3\.1\. The Official GitHub Mirror



As of 2019\-03\-20, there is now an
[official Git mirror](https://github.com/sqlite/sqlite) of the
SQLite sources on GitHub.



The mirror is an incremental export of the
[canonical Fossil repository](https://sqlite.org/src/timeline) for
SQLite. A cron\-job updates the GitHub repository once an hour.
This is a one\-way, read\-only code mirror. No pull requests or
changes are accepted via GitHub. The GitHub repository merely copies
the content from the Fossil repository. All changes are input via
Fossil.




The hashes that identify check\-ins and files on the Git mirror are
different from the hashes in Fossil. There are many reasons for
this, chief among them that Fossil uses a SHA3\-256 hash whereas
Git uses a SHA1 hash. During export, the original Fossil hash for
each check\-in is added as a footer to check\-in comments. To avoid
confusion, always use the original Fossil hash, not the Git hash,
when referring to SQLite check\-ins.



## 3\.2\. Web Access



The [SQLite Fossil Repository](https://sqlite.org/src/timeline) contains links
for downloading a Tarball, ZIP Archive, or [SQLite Archive](sqlar.html) for any
historical version of SQLite. The URLs for these downloads are
simple and can be incorporated easily into automated tools. The format is:




> https://sqlite.org/src/tarball/*VERSION*/sqlite.tar.gz



Simply replace *VERSION* with some description of the version to be
downloaded. The *VERSION* can be a prefix of the cryptographic hash
name of a specific check\-in, or the name of a branch (in which case the
most recent version of the branch is fetched) or a tag for a specific
check\-in like "version\-3\.23\.1":




> https://sqlite.org/src/tarball/version\-3\.23\.1/sqlite.tar.gz


To get the latest release, use "release"
for *VERSION*, like this:




> https://sqlite.org/src/tarball/release/sqlite.tar.gz



To get the latest trunk check\-in, us "trunk" for *VERSION*:




> https://sqlite.org/src/tarball/trunk/sqlite.tar.gz



And so forth.
For ZIP archives and SQLite Archives, simply change the "/tarball/" element
into either "/zip/" or "/sqlar/", and maybe also change the name of the
download file to have a ".zip" or ".sqlar" suffix.



## 3\.3\. Fossil Access



Fossil is easy to install and use. Here are the steps for unix.
(Windows is similar.)



1. Download the self\-contained Fossil executable from
[https://fossil\-scm.org/fossil/uv/download.html](https://fossil-scm.org/fossil/uv/download.html) and put the executable
somewhere on your $PATH.
2. mkdir \~/fossils
3. fossil clone https://sqlite.org/src \~/fossils/sqlite.fossil
4. mkdir \~/sqlite; cd \~/sqlite
5. fossil open \~/fossils/sqlite.fossil



At this point you are ready to type "./configure; make"
(or on Windows with MSVC, "nmake /f Makefile.msc").




To change your checkout to a different version of Fossil use
the "update" command:




> fossil update *VERSION*



Use "trunk" for *VERSION* to get the latest trunk version of SQLite.
Or use a prefix of a cryptographic hash name, or the name of some branch
or tag. See
[https://fossil\-scm.org/fossil/doc/trunk/www/checkin\_names.wiki](https://fossil-scm.org/fossil/doc/trunk/www/checkin_names.wiki) for more
suggestions on what names can be used for *VERSION*.




Use the "fossil ui" command from within the \~/sqlite checkout to
bring up a local copy of the website.




Additional documentation on Fossil can be found at
[https://fossil\-scm.org/fossil/doc/trunk/www/permutedindex.html](https://fossil-scm.org/fossil/doc/trunk/www/permutedindex.html)



Do not be afraid to explore and experiment.
Without a log\-in you won't be able to
push back any changes you make, so you cannot damage the project.



## 3\.4\. Verifying Source Code Integrity



If you need to verify that the SQLite source code that you have is
authentic and has not been modified in any way (perhaps by an adversary)
that can be done using a few simple command\-line tools. At the root
of the SQLite source tree is a file named "manifest". The manifest
file contains the name of every other file in the source tree together
with either a SHA1 or SHA3\-256 hash for that file. (SHA1 is used for
older files and SHA3\-256 for newer files.) You can write a
script to extract these hashes and verify them against the source code
files. The hash name for the check\-in is just the SHA3\-256 hash of the
"manifest" file itself, possibly with the last line omitted if the
last line begins with "\# Remove this line..."



# 4\. See Also


Other pages that talk about Fossil and Git include:


* [Fossil vs. Git](https://fossil-scm.org/fossil/doc/trunk/www/fossil-v-git.wiki)
* [What others say about Fossil and Git](https://www.fossil-scm.org/fossil/doc/trunk/www/quotes.wiki)


*This page last modified on [2023\-02\-27 02:07:35](https://sqlite.org/docsrc/honeypot) UTC* 


