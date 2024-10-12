




Prepared Statement Scan Status Opcodes




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Prepared Statement Scan Status Opcodes




> ```
> 
> #define SQLITE_SCANSTAT_NLOOP    0
> #define SQLITE_SCANSTAT_NVISIT   1
> #define SQLITE_SCANSTAT_EST      2
> #define SQLITE_SCANSTAT_NAME     3
> #define SQLITE_SCANSTAT_EXPLAIN  4
> #define SQLITE_SCANSTAT_SELECTID 5
> #define SQLITE_SCANSTAT_PARENTID 6
> #define SQLITE_SCANSTAT_NCYCLE   7
> 
> ```



The following constants can be used for the T parameter to the
[sqlite3\_stmt\_scanstatus(S,X,T,V)](../c3ref/stmt_scanstatus.html) interface. Each constant designates a
different metric for sqlite3\_stmt\_scanstatus() to return.


When the value returned to V is a string, space to hold that string is
managed by the prepared statement S and will be automatically freed when
S is finalized.


Not all values are available for all query elements. When a value is
not available, the output variable is set to \-1 if the value is numeric,
or to NULL if it is a string (SQLITE\_SCANSTAT\_NAME).




SQLITE\_SCANSTAT\_NLOOP
The [sqlite3\_int64](../c3ref/int64.html) variable pointed to by the V parameter will be
set to the total number of times that the X\-th loop has run.



SQLITE\_SCANSTAT\_NVISIT
The [sqlite3\_int64](../c3ref/int64.html) variable pointed to by the V parameter will be set
to the total number of rows examined by all iterations of the X\-th loop.



SQLITE\_SCANSTAT\_EST
The "double" variable pointed to by the V parameter will be set to the
query planner's estimate for the average number of rows output from each
iteration of the X\-th loop. If the query planner's estimates was accurate,
then this value will approximate the quotient NVISIT/NLOOP and the
product of this value for all prior loops with the same SELECTID will
be the NLOOP value for the current loop.



SQLITE\_SCANSTAT\_NAME
The "const char \*" variable pointed to by the V parameter will be set
to a zero\-terminated UTF\-8 string containing the name of the index or table
used for the X\-th loop.



SQLITE\_SCANSTAT\_EXPLAIN
The "const char \*" variable pointed to by the V parameter will be set
to a zero\-terminated UTF\-8 string containing the [EXPLAIN QUERY PLAN](../eqp.html)
description for the X\-th loop.



SQLITE\_SCANSTAT\_SELECTID
The "int" variable pointed to by the V parameter will be set to the
id for the X\-th query plan element. The id value is unique within the
statement. The select\-id is the same value as is output in the first
column of an [EXPLAIN QUERY PLAN](../eqp.html) query.



SQLITE\_SCANSTAT\_PARENTID
The "int" variable pointed to by the V parameter will be set to the
the id of the parent of the current query element, if applicable, or
to zero if the query element has no parent. This is the same value as
returned in the second column of an [EXPLAIN QUERY PLAN](../eqp.html) query.



SQLITE\_SCANSTAT\_NCYCLE
The sqlite3\_int64 output value is set to the number of cycles,
according to the processor time\-stamp counter, that elapsed while the
query element was being processed. This value is not available for
all query elements \- if it is unavailable the output variable is
set to \-1\.



See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


