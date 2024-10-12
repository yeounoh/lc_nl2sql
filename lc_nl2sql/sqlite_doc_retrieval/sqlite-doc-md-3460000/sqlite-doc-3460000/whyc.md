




Why Is SQLite Coded In C




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Why Is SQLite Coded In C


►
Table Of Contents
[1\. C Is Best](#c_is_best)
[1\.1\. Performance](#performance)
[1\.2\. Compatibility](#compatibility)
[1\.3\. Low\-Dependency](#low_dependency)
[1\.4\. Stability](#stability)
[2\. Why Isn't SQLite Coded In An Object\-Oriented Language?](#why_isn_t_sqlite_coded_in_an_object_oriented_language_)
[3\. Why Isn't SQLite Coded In A "Safe" Language?](#why_isn_t_sqlite_coded_in_a_safe_language_)




# 1\. C Is Best



> | Note: Sections 2\.0 and 3\.0 of this article were added in response to comments on  [Hacker News](https://news.ycombinator.com/item?id=16585120) and [Reddit](https://www.reddit.com/r/programming/comments/84fzoc/why_is_sqlite_coded_in_c/). |
> | --- |



Since its inception on 2000\-05\-29, SQLite has been implemented in generic C.
C was and continues to be the best language for implementing a software
library like SQLite. There are no plans to recode SQLite in any other
programming language at this time.




The reasons why C is the best language to implement SQLite include:




* Performance
* Compatibility
* Low\-dependency
* Stability


## 1\.1\. Performance


An intensively used low\-level library like SQLite needs to be fast.
(And SQLite is fast, see [Internal Versus External BLOBs](intern-v-extern-blob.html) and
[35% Faster Than The Filesystem](fasterthanfs.html) for example.)



C is a great language for writing fast code. C is sometimes
described as "portable assembly language". It enables to developers
to code as close to the underlying hardware as possible while still
remaining portable across platforms.



Other programming languages sometimes claim to be "as fast as C".
But no other language claims to be faster than C for general\-purpose
programming, because none are.



## 1\.2\. Compatibility


Nearly all systems have the ability to call libraries
written in C. This is not true of other implementation languages.



So, for example, Android applications written in Java are able to
invoke SQLite (through an adaptor). Maybe it would have been more
convenient for Android if SQLite had been coded in Java as that would
make the interface simpler. However, on iPhone applications are coded
in Objective\-C or Swift, neither of which have the ability to call
libraries written in Java. Thus, SQLite would be unusable on iPhones
had it been written in Java.



## 1\.3\. Low\-Dependency


Libraries written in C do not have a huge run\-time dependency.
In its minimum configuration, SQLite requires only the following
routines from the standard C library:






| * memcmp() * memcpy() * memmove() * memset() |  | * strcmp() * strlen() * strncmp() |
| --- | --- | --- |




In a more complete build, SQLite also uses library routines like
malloc() and free() and operating system interfaces for opening, reading,
writing, and closing files. But even then, the number of dependencies
is very small. Other "modern" language, in contrast, often require
multi\-megabyte runtimes loaded with thousands and thousands of interfaces.



## 1\.4\. Stability



The C language is old and boring.
It is a well\-known and well\-understood language.
This is exactly what one wants when developing a module like SQLite.
Writing a small, fast, and reliable database engine is hard enough as it
is without the implementation language changing out from under you with
each update to the implementation language specification.



# 2\. Why Isn't SQLite Coded In An Object\-Oriented Language?



Some programmers cannot imagine developing a complex system like
SQLite in a language that is not "object oriented". So why is
SQLite not coded in C\+\+ or Java?



1. Libraries written in C\+\+ or Java can generally only be used by
applications written in the same language. It is difficult to
get an application written in Haskell or Java to invoke a library
written in C\+\+. On the other hand, libraries written in C are
callable from any programming language.
2. Object\-Oriented is a design pattern, not a programming language.
You can do object\-oriented programming in any language you want,
including assembly language. Some languages (ex: C\+\+ or Java) make
object\-oriented easier. But you can still do object\-oriented programming
in languages like C.
3. Object\-oriented is not the only valid design pattern.
Many programmers have been taught to think purely in terms of
objects. And, to be fair, objects are often a good way to
decompose a problem. But objects are not the only way, and are
not always the best way to decompose a problem. Sometimes good old
procedural code is easier to write, easier to maintain and understand,
and faster than object\-oriented code.
4. When SQLite was first being developed, Java was a young and immature
language. C\+\+ was older, but was undergoing such growing pains that
it was difficult to find any two C\+\+ compilers that worked the same
way. So C was definitely a better choice back when SQLite was first
being developed. The situation is less stark now, but there is little
to no benefit in recoding SQLite at this point.


# 3\. Why Isn't SQLite Coded In A "Safe" Language?



There has lately been a lot of interest in "safe" programming languages
like Rust or Go in which it is impossible, or is at least difficult, to make
common programming errors like memory leaks or array overruns. So the
question often arises as to why SQLite is not coded in a "safe" language.



1. None of the safe programming languages existed for the first 10 years
of SQLite's existence. SQLite could be recoded in Go or Rust, but doing
so would probably introduce far more bugs than would be fixed, and it
seems also likely to result in slower code.
2. Safe languages insert additional machine branches to do things like
verify that array accesses are in\-bounds. In correct code, those
branches are never taken. That means that the machine code cannot
be 100% branch tested, which is an important component of SQLite's
quality strategy.
3. Safe languages usually want to abort if they encounter an out\-of\-memory
(OOM) situation. SQLite is designed to recover gracefully from an OOM.
It is unclear how this could be accomplished in the current crop of
safe languages.
4. All of the existing safe languages are new. The developers of SQLite
applaud the efforts of computer language researchers in trying to
develop languages that are easier to program safely. We encourage these
efforts to continue. But we ourselves are more interested in old and
boring languages when it comes to implementing SQLite.



All that said, it is possible that SQLite might
one day be recoded in Rust. Recoding SQLite in Go is unlikely
since Go hates assert(). But Rust is a possibility. Some
preconditions that must occur before SQLite is recoded in Rust
include:






1. Rust needs to mature a little more, stop changing so fast, and
 move further toward being old and boring.
2. Rust needs to demonstrate that it can be used to create general\-purpose
 libraries that are callable from all other programming languages.
3. Rust needs to demonstrate that it can produce object code that
 works on obscure embedded devices, including devices that lack
 an operating system.
4. Rust needs to pick up the necessary tooling that enables one to
 do 100% branch coverage testing of the compiled binaries.
5. Rust needs a mechanism to recover gracefully from OOM errors.
6. Rust needs to demonstrate that it can do the kinds of work that
 C does in SQLite without a significant speed penalty.



If you are a "rustacean" and feel that Rust already meets the
preconditions listed above, and that SQLite should be recoded in
Rust, then you are welcomed and encouraged
to contact the SQLite developers privately
and argue your case.


*This page last modified on [2022\-07\-29 00:41:26](https://sqlite.org/docsrc/honeypot) UTC* 


