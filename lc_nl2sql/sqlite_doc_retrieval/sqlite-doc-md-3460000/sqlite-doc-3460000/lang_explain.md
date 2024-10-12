




EXPLAIN




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










EXPLAIN


# 1\. Syntax


**[sql\-stmt:](syntax/sql-stmt.html)**







EXPLAIN



QUERY



PLAN









alter\-table\-stmt






analyze\-stmt






attach\-stmt






begin\-stmt






commit\-stmt






create\-index\-stmt






create\-table\-stmt






create\-trigger\-stmt






create\-view\-stmt






create\-virtual\-table\-stmt






delete\-stmt






delete\-stmt\-limited






detach\-stmt






drop\-index\-stmt






drop\-table\-stmt






drop\-trigger\-stmt






drop\-view\-stmt






insert\-stmt






pragma\-stmt






reindex\-stmt






release\-stmt






rollback\-stmt






savepoint\-stmt






select\-stmt






update\-stmt






update\-stmt\-limited






vacuum\-stmt








# 2\. Description


An SQL statement can be preceded by the keyword "EXPLAIN" or
by the phrase "EXPLAIN QUERY PLAN". Either modification causes the
SQL statement to behave as a query and to return information about
how the SQL statement would have operated if the EXPLAIN keyword or
phrase had been omitted.


The output from EXPLAIN and EXPLAIN QUERY PLAN is intended for
interactive analysis and troubleshooting only. The details of the 
output format are subject to change from one release of SQLite to the next.
Applications should not use EXPLAIN or EXPLAIN QUERY PLAN since
their exact behavior is variable and only partially documented.


When the EXPLAIN keyword appears by itself it causes the statement
to behave as a query that returns the sequence of 
[virtual machine instructions](opcode.html) it would have used to execute the command had
the EXPLAIN keyword not been present. When the EXPLAIN QUERY PLAN phrase
appears, the statement returns high\-level information regarding the query
plan that would have been used.



The EXPLAIN QUERY PLAN command is described in 
[more detail here](eqp.html).



## 2\.1\. EXPLAIN operates at run\-time, not at prepare\-time


The EXPLAIN and EXPLAIN QUERY PLAN prefixes affect the behavior of
running a [prepared statement](c3ref/stmt.html) using [sqlite3\_step()](c3ref/step.html). The process of
generating a new prepared statement using [sqlite3\_prepare()](c3ref/prepare.html) or similar
is (mostly) unaffected by EXPLAIN. (The exception to the previous sentence
is that some special opcodes used by EXPLAIN QUERY PLAN are omitted when
building an EXPLAIN QUERY PLAN prepared statement, as a performance
optimization.)



This means that actions that occur during sqlite3\_prepare() are
unaffected by EXPLAIN.



* Some [PRAGMA](pragma.html#syntax) statements do their work during sqlite3\_prepare() rather
than during sqlite3\_step(). Those PRAGMA statements are unaffected
by EXPLAIN. They operate the same with or without the EXPLAIN prefix.
The set of PRAGMA statements that are unaffected by EXPLAIN can vary
from one release to the next. Some PRAGMA statements operate during
sqlite3\_prepare() depending on their arguments. For consistent
results, avoid using EXPLAIN on PRAGMA statements.
* The [authorizer callback](c3ref/set_authorizer.html) is invoked regardless of the presence of
EXPLAIN or EXPLAIN QUERY PLAN.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


