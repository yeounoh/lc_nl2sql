




Status Parameters for prepared statements




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Status Parameters for prepared statements




> ```
> 
> #define SQLITE_STMTSTATUS_FULLSCAN_STEP     1
> #define SQLITE_STMTSTATUS_SORT              2
> #define SQLITE_STMTSTATUS_AUTOINDEX         3
> #define SQLITE_STMTSTATUS_VM_STEP           4
> #define SQLITE_STMTSTATUS_REPREPARE         5
> #define SQLITE_STMTSTATUS_RUN               6
> #define SQLITE_STMTSTATUS_FILTER_MISS       7
> #define SQLITE_STMTSTATUS_FILTER_HIT        8
> #define SQLITE_STMTSTATUS_MEMUSED           99
> 
> ```



These preprocessor macros define integer codes that name counter
values associated with the [sqlite3\_stmt\_status()](../c3ref/stmt_status.html) interface.
The meanings of the various counters are as follows:




SQLITE\_STMTSTATUS\_FULLSCAN\_STEP
This is the number of times that SQLite has stepped forward in
a table as part of a full table scan. Large numbers for this counter
may indicate opportunities for performance improvement through
careful use of indices.



SQLITE\_STMTSTATUS\_SORT
This is the number of sort operations that have occurred.
A non\-zero value in this counter may indicate an opportunity to
improvement performance through careful use of indices.



SQLITE\_STMTSTATUS\_AUTOINDEX
This is the number of rows inserted into transient indices that
were created automatically in order to help joins run faster.
A non\-zero value in this counter may indicate an opportunity to
improvement performance by adding permanent indices that do not
need to be reinitialized each time the statement is run.



SQLITE\_STMTSTATUS\_VM\_STEP
This is the number of virtual machine operations executed
by the prepared statement if that number is less than or equal
to 2147483647\. The number of virtual machine operations can be
used as a proxy for the total work done by the prepared statement.
If the number of virtual machine operations exceeds 2147483647
then the value returned by this statement status code is undefined.



SQLITE\_STMTSTATUS\_REPREPARE
This is the number of times that the prepare statement has been
automatically regenerated due to schema changes or changes to
[bound parameters](../lang_expr.html#varparam) that might affect the query plan.



SQLITE\_STMTSTATUS\_RUN
This is the number of times that the prepared statement has
been run. A single "run" for the purposes of this counter is one
or more calls to [sqlite3\_step()](../c3ref/step.html) followed by a call to [sqlite3\_reset()](../c3ref/reset.html).
The counter is incremented on the first [sqlite3\_step()](../c3ref/step.html) call of each
cycle.




SQLITE\_STMTSTATUS\_FILTER\_HIT  

SQLITE\_STMTSTATUS\_FILTER\_MISS
SQLITE\_STMTSTATUS\_FILTER\_HIT is the number of times that a join
step was bypassed because a Bloom filter returned not\-found. The
corresponding SQLITE\_STMTSTATUS\_FILTER\_MISS value is the number of
times that the Bloom filter returned a find, and thus the join step
had to be processed as normal.



SQLITE\_STMTSTATUS\_MEMUSED
This is the approximate number of bytes of heap memory
used to store the prepared statement. This value is not actually
a counter, and so the resetFlg parameter to sqlite3\_stmt\_status()
is ignored when the opcode is SQLITE\_STMTSTATUS\_MEMUSED.




See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


