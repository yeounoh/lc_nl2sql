




The Use Of assert() In SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Use Of assert() In SQLite


►
Table Of Contents
[1\. Assert() And Similar Macros In SQLite](#assert_and_similar_macros_in_sqlite)
[1\.1\. Philosophy of assert()](#philosophy_of_assert_)
[1\.2\. Different Behaviors According To Build Type](#different_behaviors_according_to_build_type)
[2\. Examples](#examples)




# 1\. Assert() And Similar Macros In SQLite



The assert(X) macro is 
[part of standard C](https://en.wikipedia.org/wiki/Assert.h), in the
\<assert.h\> header file.
SQLite adds three other assert()\-like macros named NEVER(X), ALWAYS(X),
and testcase(X).



* **assert(X)** →
The assert(X) statement indicates that the condition X is always true.
In other words, X is an invariant. The assert(X) macro works like a
procedure in that it has no return value.
* **ALWAYS(X)** →
The ALWAYS(X) function indicates that condition X is always true as far
as the developers know, but there is no proof the X is true, or the
proof is complex and error\-prone, or the proof depends on implementation
details that are likely to change in the future. ALWAYS(X) behaves like
a function that returns the boolean value X, and is intended to be used
within the conditional of an "if" statement.
* **NEVER(X)** →
The NEVER(X) function indicates that condition X is never true. This
is the negative analog of the ALWAYS(X) function.
* **testcase(X)** →
The testcase(X) statement indicates that X is sometimes true and sometimes
false. In other words, testcase(X) indicates that X is definitely not an
invariant. Since SQLite uses 100% [MC/DC testing](testing.html#mcdc), the presence of a
testcase(X) macro indicates that not only is it possible for X to be either
true or false, but there are test cases to demonstrate this.



SQLite version 3\.22\.0 (2018\-01\-22\) contains 5290 assert() macros,
839 testcase() macros, 88 ALWAYS() macros, and 63 NEVER() macros.



## 1\.1\. Philosophy of assert()


In SQLite, the presence of assert(X) means that the developers have
a proof that X is always true. Readers can depend upon X being true to
help them reason about the code. An assert(X) is a strong statement
about the truth of X. There is no doubt.



The ALWAYS(X) and NEVER(X) macros are a weaker statement about the
truth of X. The presence of ALWAYS(X) or NEVER(X) means that the developers
believe X is always or never true, but there is no proof, or the proof
is complex and error\-prone, or the proof depends on other aspects 
of the system that seem likely to change.



Other systems sometimes use assert(X) in a way that is
similar to the use of ALWAYS(X) or NEVER(X) in SQLite.
Developers will add an assert(X) as a 
[tacit acknowledgement that they
do not fully believe that X is always true](https://blog.regehr.org/archives/1576).
We believe that this use of assert(X) is wrong and violates the intent
and purpose of having assert(X) available in C in the first place.
An assert(X) should not be seen as a safety\-net or top\-rope used to
guard against mistakes. Nor is assert(X) appropriate for defense\-in\-depth.
An ALWAYS(X) or NEVER(X) macro, or something similar, should be used in 
those cases because ALWAYS(X) or NEVER(X) will be followed by code to
actually deal with the problem when the programmers reasoning
turns out to be wrong. Since the code that follows ALWAYS(X) or NEVER(X)
is untested, it should be something very simple, like a "return" statement,
that is easily verified by inspection.




Because assert() can be and is commonly misused, some programming language
theorists and designers look upon it with disfavor.
For example, the designers of the [Go programming language](https://golang.org) 
intentionally [omit a built\-in assert()](https://golang.org/doc/faq#assertions).
They feel that the harm caused by misuse of assert()
outweighs the benefits of including it as a language built\-in.
The SQLite developers disagree. In fact, the original purpose of this
article is to push back against the common notion that assert() is harmful.
In our experience, SQLite would be much more difficult to develop, test,
and maintain without assert().



## 1\.2\. Different Behaviors According To Build Type


Three separate builds are used to validate the SQLite software.


1. A functionality testing build is used to validate the source code.
2. A coverage testing build is used to validate the test suite, to confirm
 that the test suite provides 100% MC/DC.
3. The release build is used to validate the generated machine code.


All tests must give the same answer in all three
builds. See the ["How SQLite Is Tested"](testing.html) document for more detail.



The various assert()\-like
macros behave differently according to how SQLite is built.





|  | Functionality Testing | Coverage Testing | Release |
| --- | --- | --- | --- |
| assert(X) | abort() if X is false | no\-op | no\-op |
| ALWAYS(X) | abort() if X is false | always true | pass through the value X |
| NEVER(X) | abort() if X is true | always false | pass through the value X |
| testcase(X) | no\-op | do some harmless work if X is true | no\-op |


The default behavior of assert(X) in standard C is that it is enabled
for release builds. This is a reasonable default. However, the
SQLite code base has many assert() statements in performance\-sensitive
areas of the code. Leaving assert(X) turned on causes SQLite to run about
three times slower. Also, SQLite strives to provide 100% MC/DC in an
as\-delivered configuration, which is obviously impossible if assert(X)
statements are enabled. For these reasons, assert(X) is a no\-op for
release builds in SQLite.



The ALWAYS(X) and NEVER(X) macros behave like assert(X) during
functionality testing, because the developers want to be immediately
alerted to the issue if the value of X is different from what is expected.
But for delivery, ALWAYS(X) and NEVER(X) are simple pass\-through macros,
which provide defense\-in\-depth. For coverage testing ALWAYS(X) and NEVER(X)
are hard\-coded boolean values so that they do not cause unreachable
machine code to be generated.



The testcase(X) macro is normally a no\-op, but for a coverage test
build it does generate a small amount of extra code that includes at least
one branch, in order to verify that test cases exist for which X is both
true and false.



# 2\. Examples


An assert() statement is often used to validate pre\-conditions on 
internal functions and methods.
Example: [https://sqlite.org/src/artifact/c1e97e4c6f?ln\=1048](https://sqlite.org/src/artifact/c1e97e4c6f?ln=1048).
This is deemed better than simply stating the pre\-condition in a header 
comment, since the assert() is actually executed. In a highly tested
program like SQLite, the reader knows that the pre\-condition is true
for all of the hundreds of millions of test cases run against SQLite,
since it has been verified by the assert().
In contrast, a text pre\-condition statement in a header comment
is untested. It might have been true when the code was written, 
but who is to say that it is still true now?




Sometimes SQLite uses compile\-time evaluatable assert() statements.
Consider the code at
[https://sqlite.org/src/artifact/c1e97e4c6f?ln\=2130\-2138](https://sqlite.org/src/artifact/c1e97e4c6f?ln=2130-2138).
Four assert() statements verify the values for compile\-time constants
so that the reader can quickly check the validity of the if\-statement
that follows, without having to look up the constant values in a separate
header file.




Sometimes compile\-time assert() statements are used to verify that
SQLite has been correctly compiled. For example, the code at
[https://sqlite.org/src/artifact/c1e97e4c6f?ln\=157](https://sqlite.org/src/artifact/c1e97e4c6f?ln=157)
verifies that the SQLITE\_PTRSIZE preprocessor macro is set correctly
for the target architecture.




The CORRUPT\_DB macro is used in many assert() statements.
In functional testing builds, CORRUPT\_DB references a global variable
that is true if the database file might contain corruption. This variable
is true by default, since we do not normally know whether or not a database
is corrupt, but during testing while working on databases that are known
to be well\-formed, that global variable can be set to false.
Then the CORRUPT\_DB macro
can be used in assert() statements such as seen at
[https://sqlite.org/src/artifact/18a53540aa3?ln\=1679\-1680](https://sqlite.org/src/artifact/18a53540aa3?ln=1679-1680).
Those assert()s specify pre\-conditions to the routine that are true for
consistent database files, but which might be false if the database file
is corrupt. Knowledge of these kinds of conditions is very helpful to
readers who are trying to understand a block of code in isolation.




ALWAYS(X) and NEVER(X) functions are used in places where we always
want the test to occur even though the developers believe the value of
X is always true or false. For example, the sqlite3BtreeCloseCursor()
routine shown must remove the closing cursor from a linked list of all
cursors. We know that the cursor is on the list, so that the loop
must terminate by the "break" statement, but it is convenient to
use the ALWAYS(X) test at
[https://sqlite.org/src/artifact/18a53540aa3?ln\=4371](https://sqlite.org/src/artifact/18a53540aa3?ln=4371) to prevent
running off the end of the linked list in case there is an error in some
other part of the code that has corrupted the linked list.




An ALWAYS(X) or NEVER(X) sometimes verifies pre\-conditions that are
subject to change if other parts of the code are modified in
subtle ways. At [https://sqlite.org/src/artifact/18a53540aa3?ln\=5512\-5516](https://sqlite.org/src/artifact/18a53540aa3?ln=5512-5516)
we have a test for two pre\-conditions that are true only because
of the limited scope of use of the sqlite3BtreeRowCountEst() function.
Future enhancements to SQLite might use sqlite3BtreeRowCountEst() in
new ways where those preconditions no longer hold, and the NEVER()
macros will quickly alert the developers to that fact when the
situation arises. But if, for some reason, the pre\-conditions are
not satisfied in a release build, the program will still behave sanely
and will not do an undefined memory access.




The testcase() macro is often used to verify that boundary
cases of an inequality comparison are checked. For example, at
[https://sqlite.org/src/artifact/18a53540aa3?ln\=5766](https://sqlite.org/src/artifact/18a53540aa3?ln=5766). These
kind of checks help to prevent off\-by\-one errors.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


