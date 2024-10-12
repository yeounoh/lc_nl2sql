




Pointer Passing Interfaces




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Pointer Passing Interfaces


►
Table Of Contents
[1\. Overview](#overview)
[2\. A Brief History Of Pointer Passing In SQLite](#a_brief_history_of_pointer_passing_in_sqlite)
[2\.1\. Upping The Threat Level](#upping_the_threat_level)
[2\.2\. Preventing Forged Pointers](#preventing_forged_pointers)
[2\.3\. Pointer Leaks](#pointer_leaks)
[3\. The New Pointer\-Passing Interfaces](#the_new_pointer_passing_interfaces)
[3\.1\. Pointer Types](#pointer_types)
[3\.1\.1\. Pointer types are static strings](#pointer_types_are_static_strings)
[3\.2\. Destructor Functions](#destructor_functions)
[4\. Restrictions On The Use of Pointer Values](#restrictions_on_the_use_of_pointer_values)
[5\. Summary](#summary)




# 1\. Overview



Three new "\_pointer()" interfaces were added to SQLite 3\.20\.0 (2017\-08\-01\):


* [sqlite3\_bind\_pointer()](c3ref/bind_blob.html),
* [sqlite3\_result\_pointer()](c3ref/result_blob.html), and
* [sqlite3\_value\_pointer()](c3ref/value_blob.html).


Questions and confusion quickly arose
on the [mailing lists](support.html#mailinglists) about the purpose behind these new interfaces,
why they were introduced, and what problem they solve. This essay attempts
to answer those questions and clear up the confusion.



# 2\. A Brief History Of Pointer Passing In SQLite



It is sometimes convenient for SQLite extensions to
communicate non\-SQL values between subcomponents or between the extension
and the application. Some examples:



* In the [FTS3](fts3.html) extension, the 
[MATCH operator](fts3.html#full_text_index_queries) (which does the full\-text search)
needs to communicate details of matching entries 
to the [snippet()](fts3.html#snippet), [offsets()](fts3.html#offsets),
and [matchinfo()](fts3.html#matchinfo) functions so that those functions can convert the details
of the match into useful output.
* In order for an application to 
[add new extensions to FTS5](fts5.html#extending_fts5), such as new tokenizers, 
the application needs a pointer to the "fts5\_api" object.
* In the [CARRAY extension](carray.html), the application needs to tell the 
extension the
location of a C\-language array that contains the data for the table\-valued
function that the extension implements.



The traditional way of communicating this information was to transform a
C\-language pointer into a BLOB or a 64\-bit integer, then move that BLOB or
integer through SQLite using the usual interfaces like
[sqlite3\_bind\_blob()](c3ref/bind_blob.html), [sqlite3\_result\_blob()](c3ref/result_blob.html), [sqlite3\_value\_blob()](c3ref/value_blob.html) or
the integer equivalents.



## 2\.1\. Upping The Threat Level



Passing around pointers as if they were integers or BLOBs is easy,
effective, and works well in an environment where the application
components are all friendly toward one another. However, passing pointers
as integers and BLOBs allows hostile SQL text to forge invalid pointers that
can carry out mischief.




For example, the first argument to the [snippet()](fts3.html#snippet) function is supposed to
be a special column of the FTS3 table that contains a pointer to an fts3cursor
object that contains information about the current full text search match.
That pointer was formerly passed as a BLOB. 
For example, if the FTS3 table is named "t1" and has a column named "cx",
one might write:




```
SELECT snippet(t1) FROM t1 WHERE cx MATCH $pattern;

```


But if a hacker is able to run arbitrary SQL, he might run a slightly
different query, like this:




```
SELECT hex(t1) FROM t1 WHERE cx MATCH $pattern;

```


Because the pointer is passed in the t1 column of the t1
table as a BLOB (in older versions of SQLite), such a query would have 
shown the value of the
pointer in hex. The attacker could then modify that pointer to try to
get the snippet() function to modify memory in some other part of 
the application address space instead of the fts3cursor object it 
was supposed to be operating on:




```
SELECT snippet(x'6092310100000000') FROM t1 WHERE cx MATCH $pattern;

```


Historically, this was not considered a threat. The argument was that if
a hostile agent is able to inject arbitrary SQL text into the application,
then that agent is already in full control of the application, so
letting the hostile agent forge a pointer does not give the agent
any new capability.




For most cases, it is true that potential attackers have no way of injecting
arbitrary SQL, and so most uses of SQLite are immune to the attack above.
But there are some notable exceptions. To wit:



* The [WebSQL](https://en.wikipedia.org/wiki/Web_SQL_Database) interface
to webkit allowed any webpage to run arbitrary SQL in the browser
for Chrome and Safari. That arbitrary SQL was supposed to be run inside
a sandbox where it could do no harm even if exploited, but that sandbox
turned out to be less secure than people supposed. In the spring of 2017, 
one team of hackers was able to root an iMac using a long sequence of 
exploits, one of which involved corrupting the pointers passed as BLOB 
values to the snippet() FTS3 function of an SQLite database running via
the WebSQL interface inside of Safari.
* On Android, we are told, there are many services that will blindly 
run arbitrary SQL that is passed to them by untrustworthy apps
that have been downloaded from dodgy corners of the internet.
Android services are suppose to be more guarded about running SQL
from unvetted sources. This author does not have any specific examples
to the contrary, but he has heard rumors that they exist. Even if
all Android services are more careful and properly vet all the SQL
they run, it would be difficult to audit them
all in order to verify that they are safe. Hence, security\-minded people
are keen to ensure that no exploits are possible by passing arbitrary
SQL text.
* The [Fossil](https://www.fossil-scm.org/) version control system (designed
and written for the purpose of supporting SQLite development) allows
mildly trusted users to enter arbitrary SQL for generating trouble\-ticket
reports. That SQL is sanitized using the
[sqlite3\_set\_authorizer()](c3ref/set_authorizer.html) interface, and no exploits have ever been
found. But this is an example of potentially hostile agents being able to
inject arbitrary SQL into the system.


## 2\.2\. Preventing Forged Pointers



The first attempt at closing security gaps in pointer passing was to
prevent pointer values from being forged. This was accomplished by
having the sender attach a subtype to each pointer using
[sqlite3\_result\_subtype()](c3ref/result_subtype.html) and having the receiver verify that subtype
using [sqlite3\_value\_subtype()](c3ref/value_subtype.html) and reject pointers that had an incorrect
subtype. Since there is no way to attach a subtype to a result using
pure SQL, this prevents pointers from being forged using SQL. The only
way to send a pointer is to use C code. If an attacker can set a subtype,
then he is also able to forge a pointer without the help of SQLite.




Using subtypes to identify valid pointers prevented the WebSQL exploit.
But it turned out to be an incomplete solution.




## 2\.3\. Pointer Leaks



The use of subtypes on pointers prevented pointer forgery using
pure SQL. But subtypes do nothing to prevent an attacker from reading
the values of pointers. In other words, subtypes on pointer values
prevent attacks using SQL statements like this:




```
SELECT snippet(x'6092310100000000') FROM t1 WHERE cx MATCH $pattern;

```


The BLOB argument to snippet() does not have the correct subtype, so the
snippet function ignores it, makes no changes to any data structures,
and harmlessly returns NULL.




But the use of subtypes does nothing to prevent the value of a
pointer from being read using SQL code like this:




```
SELECT hex(t1) FROM t1 WHERE cx MATCH $pattern;

```


What harm could come of that, you ask? The SQLite developers (including
this author) wondered the same thing. But then security researchers
pointed out that knowledge of pointers can help attackers to circumvent
address\-space randomization defenses. This is called a "pointer leak".
A pointer leak is not itself a vulnerability, but it can aid an attacker
in effectively exploiting other vulnerabilities.



# 3\. The New Pointer\-Passing Interfaces



Allowing extension components to pass private information to one another
securely and without introducing pointer leaks requires new interfaces:



* **[sqlite3\_bind\_pointer](c3ref/bind_blob.html)(S,I,P,T,D)** →
Bind pointer P of type T to the I\-th parameter of prepared statement S.
D is an optional destructor function for P.
* **[sqlite3\_result\_pointer](c3ref/result_blob.html)(C,P,T,D)** →
Return pointer P of type T as the argument of function C.
D is an optional destructor function for P.
* **[sqlite3\_value\_pointer](c3ref/value_blob.html)(V,T)** →
Return the pointer of type T associated with value V, or if V has no
associated pointer, or if the pointer on V is of a type different from
T, then return NULL.



To SQL, the values created by [sqlite3\_bind\_pointer()](c3ref/bind_blob.html) and 
[sqlite3\_result\_pointer()](c3ref/result_blob.html) are indistinguishable from NULL. An
SQL statement that tries to use the [hex()](lang_corefunc.html#hex) function to read the
value of a pointer will get an SQL NULL answer. The only way to
discover whether or not a value has an associated pointer is to
use the [sqlite3\_value\_pointer()](c3ref/value_blob.html) interface with the appropriate
type string T. 




Pointer values read by [sqlite3\_value\_pointer()](c3ref/value_blob.html)
cannot be generated by pure SQL. Hence, it is not possible for SQL to
forge pointers.




Pointer values generated by [sqlite3\_bind\_pointer()](c3ref/bind_blob.html) and
[sqlite3\_result\_pointer()](c3ref/result_blob.html) cannot be read by pure SQL.
Hence, it is not possible for SQL to leak the value of pointers.




In this way the new pointer\-passing interface seems to solve all of the
security problems associated with passing pointer values from one
extension to another in SQLite.




## 3\.1\. Pointer Types



The "pointer type" in the last parameter to [sqlite3\_bind\_pointer()](c3ref/bind_blob.html),
[sqlite3\_result\_pointer()](c3ref/result_blob.html), and [sqlite3\_value\_pointer()](c3ref/value_blob.html) is used to prevent
pointers intended for one extension from being redirected to a different
extension. For example, without the use of pointer types, an attacker 
could still get access to pointer information in a system that included 
both the [FTS3](fts3.html) and the [CARRAY extension](carray.html) using SQL like this:




```
SELECT ca.value FROM t1, carray(t1,10) AS ca WHERE cx MATCH $pattern

```


In the statement above, the FTS3 cursor pointer generated by the
MATCH operator is send into the carray() table\-valued function instead
of its intended recipient snippet(). The carray() function treats the
pointer as a pointer to an array of integers and returns each integer
one by one, thus leaking the content of the FTS3 cursor object. Since
the FTS3 cursor object contains pointers to other objects, the statement
above would be a pointer leak.




Except, the statement above does not work, thanks to pointer types.
The pointer generated by the MATCH operator has a type of "fts3cursor"
but the carray() function expects to receives a pointer of type "carray".
Because the pointer type on the [sqlite3\_result\_pointer()](c3ref/result_blob.html) does not match
the pointer type on the [sqlite3\_value\_pointer()](c3ref/value_blob.html) call, 
[sqlite3\_value\_pointer()](c3ref/value_blob.html) returns NULL in carray() and thus signals
the CARRAY extension that it has been passed an invalid pointer.



### 3\.1\.1\. Pointer types are static strings



Pointer types are static strings, which ideally should be string literals
embedded directly in the SQLite API call, not parameters passed in from
other functions. Consideration was given to using integer values as
the pointer type, but static strings provides a much larger name space
which reduces the chance of accidental type\-name collisions between
unrelated extensions.




By "static string", we mean a zero\-terminated array of bytes that is
fixed and unchanging for the life of the program. In other words, the
pointer type string should be a string constant.
In contrast, a "dynamic string" is a zero\-terminated array of bytes
that is held in memory allocated
from the heap, and which must be freed to avoid a memory leak.
Do not use dynamic strings as the pointer type string.




Multiple commentators have expressed a desire to use dynamic strings
for the pointer type, and to have SQLite take ownership of the type strings
and to automatically free the type string
when it has finished using it. That design is rejected for the
following reasons:



1. The pointer type is not intended to be flexible and dynamic. The
pointer type is intended to be a design\-time constant. Applications
should not synthesize pointer type strings at run\-time. Providing
support for dynamic pointer type strings would lead developers
to misuse the pointer\-passing interfaces by creating run\-time
synthesized pointer type strings. Requiring the pointer type strings
to be static encourages developers to do the right thing by choosing
fixed pointer type names at design\-time and encoding those names
as constant strings.
2. All string values at the SQL level in SQLite are dynamic strings. 
Requiring type strings to be static makes it difficult to 
create an application\-defined SQL function that
can synthesize a pointer of an arbitrary type. We do not want users
to create such SQL functions, since such functions would compromise the
security of the system. Thus, the requirement to use static strings
helps to defend that the integrity of the pointer\-passing interfaces against
ill\-designed SQL functions. The static string requirement is not
a perfect defense, since a sophisticated programmer can code around
it, and a novice program can simply take the memory leak. But by
stating that the pointer type string must be static, we hope to encourage
developers who might otherwise use a dynamic string for the pointer type
to think more carefully about the problem and avoid introducing
security issues.
3. Having SQLite take ownership of the type strings would impose a performance
cost on all applications, even applications that do not use the 
pointer\-passing interfaces. SQLite passes values around as instances
of the [sqlite3\_value](c3ref/value.html) object. That object has a destructor, which because
of the fact that sqlite3\_value objects are used for nearly everything, is
invoked frequently. If the destructor needs to check to see if there is
a pointer type string that needs to be freed, that is a few extra CPU
cycles that need to be burned on each call to the destructor. Those
cycles add up. We would be willing to bear the cost of the extra CPU
cycles if pointer\-passing was a commonly used programming paradigm, but
pointer\-passing is rare, and so it seems unwise to impose a run\-time cost
on billions and billions of applications that do not use pointer passing
just for convenience of a few applications that do.



If you feel that you need dynamic pointer type strings in your application,
that is a strong indicator that you are misusing the pointer\-passing interface.
Your intended use may be unsafe.
Please rethink your design. Determine if you really need to be passing
pointers through SQL in the first place. Or perhaps find a different
mechanism other than the pointer\-passing interfaces described by this
article.



## 3\.2\. Destructor Functions



The last parameter to the [sqlite3\_bind\_pointer()](c3ref/bind_blob.html) and
[sqlite3\_result\_pointer()](c3ref/result_blob.html) routines is a pointer to a procedure
used to dispose of the P pointer once SQLite has finished with it.
This pointer can be NULL, in which case no destructor is called.




When the D parameter is not NULL, that means that ownership of the
pointer is being transferred to SQLite. SQLite will take responsibility
for freeing resources associated with the pointer when it has finished
using the pointer. If the D parameter is NULL, that means that ownership
of the pointer remains with the caller and the caller is responsible for
disposing of the pointer.




Note that the destructor function D is for the pointer value P, not for
the type string T. The type string T should be a static string with an
infinite lifetime.




If ownership of the pointer is passed into SQLite by providing a
non\-NULL D parameter to [sqlite3\_bind\_pointer()](c3ref/bind_blob.html) or [sqlite3\_result\_pointer()](c3ref/result_blob.html)
then the ownership remains with SQLite until the object is destroyed.
There is no way to transfer ownership out of SQLite and back into the
application again.



# 4\. Restrictions On The Use of Pointer Values



The pointers that piggy\-back on SQL NULL values using the
[sqlite3\_bind\_pointer()](c3ref/bind_blob.html), [sqlite3\_result\_pointer()](c3ref/result_blob.html), and
[sqlite3\_value\_pointer()](c3ref/value_blob.html) interface are transient and ephemeral.
The pointers are never written into the database. The pointers
will not survive sorting. The latter fact is why there is no
sqlite3\_column\_pointer() interface, since it is impossible to
predict whether or not the query planner will insert a sort operation
prior to returning a value from a query, so it would be impossible to
know if a pointer value inserted into a query by
[sqlite3\_bind\_pointer()](c3ref/bind_blob.html) or [sqlite3\_result\_pointer()](c3ref/result_blob.html) would survive
through to the result set.




Pointer values must flow directly from their producer into their
consumer, with no intermediate operators or functions. Any transformation
of a pointer value destroys the pointer and transforms the value into
an ordinary SQL NULL.



# 5\. Summary


Key take\-aways from this essay:



1. The internet is an increasingly hostile place. These day, developers
should assume that attackers will find a way to execute arbitrary SQL 
in an application.
Applications should be designed to prevent the execution of arbitrary
SQL from escalating into a more severe exploit.
2. A few SQLite extensions benefit from passing pointers:



	* The [FTS3](fts3.html) MATCH operator passes pointers into [snippet()](fts3.html#snippet),
	 [offsets()](fts3.html#offsets), and [matchinfo()](fts3.html#matchinfo).
	* The [carray table\-valued function](carray.html) needs to accept a pointer to
	 an array of C\-language values from the application.
	* The [remember() extension](https://sqlite.org/src/file/ext/misc/remember.c)
	 needs a pointer to a C\-language integer variable in which to remember
	 the value it passes.
	* Applications need to receive a pointer to the "fts5\_api" object in order
	 to add extensions, such as custom tokenizers, to the [FTS5](fts5.html) extension.
3. Pointers should never be exchanged by encoding them as some other
SQL datatype, such as integers or BLOBs. Instead, use the interfaces
designed to facilitate secure pointer passing:
[sqlite3\_bind\_pointer()](c3ref/bind_blob.html), [sqlite3\_result\_pointer()](c3ref/result_blob.html), and
[sqlite3\_value\_pointer()](c3ref/value_blob.html).
4. The use of pointer\-passing is an advanced technique that should be used
infrequently and cautiously. Pointer\-passing should not be
used haphazardly or carelessly. Pointer\-passing is a sharp tool 
that can leave deep scars if misused.
5. The "pointer type" string which is the last parameter to each of the
pointer\-passing interfaces should be a distinct, application\-specific
string literal that appears directly in the API call. The pointer type
should not be a parameter passed in from a higher\-level function.


*This page last modified on [2022\-10\-07 10:23:26](https://sqlite.org/docsrc/honeypot) UTC* 


