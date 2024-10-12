




Implementation Limits For SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







## Limits In SQLite



"Limits" in the context of this article means sizes or
quantities that can not be exceeded. We are concerned
with things like the maximum number of bytes in a
BLOB or the maximum number of columns in a table.




SQLite was originally designed with a policy of avoiding
arbitrary limits.
Of course, every program that runs on a machine with finite
memory and disk space has limits of some kind. But in SQLite, 
those limits
were not well defined. The policy was that if it would fit
in memory and you could count it with a 32\-bit integer, then
it should work.




Unfortunately, the no\-limits policy has been shown to create
problems. Because the upper bounds were not well
defined, they were not tested, and bugs were often found
when pushing SQLite to extremes. For this reason, versions
of SQLite since about release 3\.5\.8 (2008\-04\-16\)
have well\-defined limits, and those limits are tested as part of
the [test suite](testing.html).




This article defines what the limits of SQLite are and how they
can be customized for specific applications. The default settings
for limits are normally quite large and adequate for almost every
application. Some applications may want to increase a limit here
or there, but we expect such needs to be rare. More commonly,
an application might want to recompile SQLite with much lower
limits to avoid excess resource utilization in the event of
bug in higher\-level SQL statement generators or to help thwart 
attackers who inject malicious SQL statements.




Some limits can be changed at run\-time on a per\-connection basis
using the [sqlite3\_limit()](c3ref/limit.html) interface with one of the
[limit categories](c3ref/c_limit_attached.html#sqlitelimitlength) defined for that interface.
Run\-time limits are designed for applications that have multiple
databases, some of which are for internal use only and others which
can be influenced or controlled by potentially hostile external agents.
For example, a web browser application might use an internal database
to track historical page views but have one or more separate databases
that are created and controlled by javascript applications that are
downloaded from the internet.
The [sqlite3\_limit()](c3ref/limit.html) interface allows internal databases managed by
trusted code to be unconstrained while simultaneously placing tight
limitations on databases created or controlled by untrusted external
code in order to help prevent a denial of service attack.



2. **Maximum length of a string or BLOB**



The maximum number of bytes in a string or BLOB in SQLite is defined
by the preprocessor macro SQLITE\_MAX\_LENGTH. The default value
of this macro is 1 billion (1 thousand million or 1,000,000,000\).
You can raise or lower this value at compile\-time using a command\-line 
option like this:




> \-DSQLITE\_MAX\_LENGTH\=123456789



The current implementation will only support a string or BLOB
length up to 231\-1 or 2147483647\. And
some built\-in functions such as hex() might fail well before that
point. In security\-sensitive applications it is best not to
try to increase the maximum string and blob length. In fact,
you might do well to lower the maximum string and blob length
to something more in the range of a few million if that is
possible.




During part of SQLite's INSERT and SELECT processing, the complete
content of each row in the database is encoded as a single BLOB.
So the SQLITE\_MAX\_LENGTH parameter also determines the maximum
number of bytes in a row.




The maximum string or BLOB length can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_LENGTH](c3ref/c_limit_attached.html#sqlitelimitlength),size) interface.
4. **Maximum Number Of Columns**



The SQLITE\_MAX\_COLUMN compile\-time parameter is used to set an upper
bound on:



	* The number of columns in a table
	* The number of columns in an index
	* The number of columns in a view
	* The number of terms in the SET clause of an UPDATE statement
	* The number of columns in the result set of a SELECT statement
	* The number of terms in a GROUP BY or ORDER BY clause
	* The number of values in an INSERT statement
The default setting for SQLITE\_MAX\_COLUMN is 2000\. You can change it
at compile time to values as large as 32767\. On the other hand, many
experienced database designers will argue that a well\-normalized database
will never need more than 100 columns in a table.




In most applications, the number of columns is small \- a few dozen.
There are places in the SQLite code generator that use algorithms
that are O(N²) where N is the number of columns. 
So if you redefine SQLITE\_MAX\_COLUMN to be a
really huge number and you generate SQL that uses a large number of
columns, you may find that [sqlite3\_prepare\_v2()](c3ref/prepare.html)
runs slowly.



The maximum number of columns can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_COLUMN](c3ref/c_limit_attached.html#sqlitelimitcolumn),size) interface.
6. **Maximum Length Of An SQL Statement**



The maximum number of bytes in the text of an SQL statement is 
limited to SQLITE\_MAX\_SQL\_LENGTH which defaults to 1,000,000,000\.




If an SQL statement is limited to be a million bytes in length, then
obviously you will not be able to insert multi\-million byte strings
by embedding them as literals inside of INSERT statements. But
you should not do that anyway. Use host [parameters](lang_expr.html#varparam) 
for your data. Prepare short SQL statements like this:




> INSERT INTO tab1 VALUES(?,?,?);



Then use the [sqlite3\_bind\_XXXX()](c3ref/bind_blob.html) functions
to bind your large string values to the SQL statement. The use of binding
obviates the need to escape quote characters in the string, reducing the
risk of SQL injection attacks. It also runs faster since the large
string does not need to be parsed or copied as much.




The maximum length of an SQL statement can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_SQL\_LENGTH](c3ref/c_limit_attached.html#sqlitelimitsqllength),size) interface.
7. **Maximum Number Of Tables In A Join**



SQLite does not support joins containing more than 64 tables.
This limit arises from the fact that the SQLite code generator
uses bitmaps with one bit per join\-table in the query optimizer.




SQLite uses an efficient [query planner algorithm](queryplanner-ng.html)
and so even a large join can be [prepared](c3ref/prepare.html) quickly.
Hence, there is no mechanism to raise or lower the limit on the
number of tables in a join.
9. **Maximum Depth Of An Expression Tree**



SQLite parses expressions into a tree for processing. During
code generation, SQLite walks this tree recursively. The depth
of expression trees is therefore limited in order to avoid
using too much stack space.




The SQLITE\_MAX\_EXPR\_DEPTH parameter determines the maximum expression
tree depth. If the value is 0, then no limit is enforced. The
current implementation has a default value of 1000\.




The maximum depth of an expression tree can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_EXPR\_DEPTH](c3ref/c_limit_attached.html#sqlitelimitexprdepth),size) interface if the
SQLITE\_MAX\_EXPR\_DEPTH is initially positive. In other words, the maximum
expression depth can be lowered at run\-time if there is already a 
compile\-time limit on the expression depth. If SQLITE\_MAX\_EXPR\_DEPTH is
set to 0 at compile time (if the depth of expressions is unlimited) then
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_EXPR\_DEPTH](c3ref/c_limit_attached.html#sqlitelimitexprdepth),size) is a no\-op.
11. **Maximum Number Of Arguments On A Function**



The SQLITE\_MAX\_FUNCTION\_ARG parameter determines the maximum number
of parameters that can be passed to an SQL function. The default value
of this limit is 100\. SQLite should work with functions that have 
thousands of parameters. However, we suspect that anybody who tries
to invoke a function with more than a few parameters is really
trying to find security exploits in systems that use SQLite, 
not do useful work, 
and so for that reason we have set this parameter relatively low.


The number of arguments to a function is sometimes stored in a signed
character. So there is a hard upper bound on SQLITE\_MAX\_FUNCTION\_ARG
of 127\.



The maximum number of arguments in a function can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_FUNCTION\_ARG](c3ref/c_limit_attached.html#sqlitelimitfunctionarg),size) interface.
13. **Maximum Number Of Terms In A Compound SELECT Statement**



A compound [SELECT](lang_select.html) statement is two or more SELECT statements connected
by operators UNION, UNION ALL, EXCEPT, or INTERSECT. We call each
individual SELECT statement within a compound SELECT a "term".




The code generator in SQLite processes compound SELECT statements using
a recursive algorithm. In order to limit the size of the stack, we
therefore limit the number of terms in a compound SELECT. The maximum
number of terms is SQLITE\_MAX\_COMPOUND\_SELECT which defaults to 500\.
We think this is a generous allotment since in practice we almost
never see the number of terms in a compound select exceed single digits.




The maximum number of compound SELECT terms can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_COMPOUND\_SELECT](c3ref/c_limit_attached.html#sqlitelimitcompoundselect),size) interface.
15. **Maximum Length Of A LIKE Or GLOB Pattern**



The pattern matching algorithm used in the default [LIKE](lang_expr.html#like) and [GLOB](lang_expr.html#glob)
implementation of SQLite can exhibit O(N²) performance (where
N is the number of characters in the pattern) for certain pathological
cases. To avoid denial\-of\-service attacks from miscreants who are able
to specify their own LIKE or GLOB patterns, the length of the LIKE
or GLOB pattern is limited to SQLITE\_MAX\_LIKE\_PATTERN\_LENGTH bytes.
The default value of this limit is 50000\. A modern workstation can
evaluate even a pathological LIKE or GLOB pattern of 50000 bytes
relatively quickly. The denial of service problem only comes into
play when the pattern length gets into millions of bytes. Nevertheless,
since most useful LIKE or GLOB patterns are at most a few dozen bytes
in length, paranoid application developers may want to reduce this
parameter to something in the range of a few hundred if they know that
external users are able to generate arbitrary patterns.




The maximum length of a LIKE or GLOB pattern can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_LIKE\_PATTERN\_LENGTH](c3ref/c_limit_attached.html#sqlitelimitlikepatternlength),size) interface.
17. **Maximum Number Of Host Parameters In A Single SQL Statement**



A host [parameter](lang_expr.html#varparam) is a place\-holder in an SQL statement that is filled
in using one of the
[sqlite3\_bind\_XXXX()](c3ref/bind_blob.html) interfaces.
Many SQL programmers are familiar with using a question mark ("?") as a
host parameter. SQLite also supports named host parameters prefaced
by ":", "$", or "@" and numbered host parameters of the form "?123".




Each host parameter in an SQLite statement is assigned a number. The
numbers normally begin with 1 and increase by one with each new
parameter. However, when the "?123" form is used, the host parameter
number is the number that follows the question mark.




SQLite allocates space to hold all host parameters between 1 and the
largest host parameter number used. Hence, an SQL statement that contains
a host parameter like ?1000000000 would require gigabytes of storage.
This could easily overwhelm the resources of the host machine.
To prevent excessive memory allocations, 
the maximum value of a host parameter number is SQLITE\_MAX\_VARIABLE\_NUMBER,
which defaults to 999 for SQLite versions prior to 3\.32\.0 (2020\-05\-22\)
or 32766 for SQLite versions after 3\.32\.0\.




The maximum host parameter number can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_VARIABLE\_NUMBER](c3ref/c_limit_attached.html#sqlitelimitvariablenumber),size) interface.
19. **Maximum Depth Of Trigger Recursion**



SQLite limits the depth of recursion of triggers in order to prevent
a statement involving recursive triggers from using an unbounded amount
of memory. 



Prior to SQLite [version 3\.6\.18](releaselog/3_6_18.html) (2009\-09\-11\), 
triggers were not recursive and so
this limit was meaningless. Beginning with version 3\.6\.18, recursive triggers
were supported but had to be explicitly enabled using the
[PRAGMA recursive\_triggers](pragma.html#pragma_recursive_triggers) statement. 
Beginning with [version 3\.7\.0](releaselog/3_7_0.html) (2009\-09\-11\), 
recursive triggers are enabled by default but can be manually disabled
using [PRAGMA recursive\_triggers](pragma.html#pragma_recursive_triggers). The SQLITE\_MAX\_TRIGGER\_DEPTH is
only meaningful if recursive triggers are enabled.


The default maximum trigger recursion depth is 1000\.
21. **Maximum Number Of Attached Databases**



The [ATTACH](lang_attach.html) statement is an SQLite extension
that allows two or more databases to be associated to the same database
connection and to operate as if they were a single database. The number
of simultaneously attached databases is limited to SQLITE\_MAX\_ATTACHED
which is set to 10 by default.
The maximum number of attached databases cannot be increased above 125\.



The maximum number of attached databases can be lowered at run\-time using
the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_ATTACHED](c3ref/c_limit_attached.html#sqlitelimitattached),size) interface.
23. **Maximum Number Of Pages In A Database File**



SQLite is able to limit the size of a database file to prevent
the database file from growing too large and consuming too much
disk space.
The SQLITE\_MAX\_PAGE\_COUNT parameter
is the maximum number of pages allowed in a single
database file. An attempt to insert new data that would cause
the database file to grow larger than this will return
SQLITE\_FULL.




The largest possible setting for SQLITE\_MAX\_PAGE\_COUNT is 4294967294
(232\-2\).
Since version 3\.45\.0 (2024\-01\-15\), 4294967294 is
also the default value for SQLITE\_MAX\_PAGE\_COUNT.
When used with the default page size of 4096 bytes, this gives a
maximum database size of about 17\.5 terabytes.
If the page size is increased to the maximum of 65536 bytes, then the
database file can grow to be as large as about 281 terabytes.



The [max\_page\_count PRAGMA](pragma.html#pragma_max_page_count) can be used to raise or lower this
limit at run\-time.
24. **Maximum Number Of Rows In A Table**



The theoretical maximum number of rows in a table is
264 (18446744073709551616 or about 1\.8e\+19\).
This limit is unreachable since the maximum database size of 281 terabytes
will be reached first. A 281 terabytes database can hold no more than
approximately 2e\+13 rows, and then only if there are no indices and if
each row contains very little data.
25. **Maximum Database Size**



Every database consists of one or more "pages". Within a single database,
every page is the same size, but different databases can have page sizes
that are powers of two between 512 and 65536, inclusive. The maximum
size of a database file is 4294967294 pages. At the maximum page size
of 65536 bytes, this translates into a maximum database size of 
approximately 1\.4e\+14 bytes (281 terabytes, or 256 tebibytes, or
281474 gigabytes or 256,000 gibibytes).

This particular upper bound is untested since the developers do not 
have access to hardware capable of reaching this limit. However, tests
do verify that SQLite behaves correctly and sanely when a database 
reaches the maximum file size of the underlying filesystem (which is
usually much less than the maximum theoretical database size) and when
a database is unable to grow due to disk space exhaustion.
26. **Maximum Number Of Tables In A Schema**



Each table and index requires at least one page in the database file.
An "index" in the previous sentence means an index created explicitly
using a [CREATE INDEX](lang_createindex.html) statement or implicit indices created by UNIQUE
and PRIMARY KEY constraints. Since the maximum number of pages in a
database file is 2147483646 (a little over 2 billion) this is also then
an upper bound on the number of tables and indices in a schema.

Whenever a database is opened, the entire schema is scanned and parsed
and a parse tree for the schema is held in memory. That means that
database connection startup time and initial memory usage
is proportional to the size of the schema.


*This page last modified on [2024\-01\-03 11:05:13](https://sqlite.org/docsrc/honeypot) UTC* 


