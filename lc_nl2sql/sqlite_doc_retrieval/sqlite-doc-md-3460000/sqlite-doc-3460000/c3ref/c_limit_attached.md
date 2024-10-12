




Run\-Time Limit Categories




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Run\-Time Limit Categories




> ```
> 
> #define SQLITE_LIMIT_LENGTH                    0
> #define SQLITE_LIMIT_SQL_LENGTH                1
> #define SQLITE_LIMIT_COLUMN                    2
> #define SQLITE_LIMIT_EXPR_DEPTH                3
> #define SQLITE_LIMIT_COMPOUND_SELECT           4
> #define SQLITE_LIMIT_VDBE_OP                   5
> #define SQLITE_LIMIT_FUNCTION_ARG              6
> #define SQLITE_LIMIT_ATTACHED                  7
> #define SQLITE_LIMIT_LIKE_PATTERN_LENGTH       8
> #define SQLITE_LIMIT_VARIABLE_NUMBER           9
> #define SQLITE_LIMIT_TRIGGER_DEPTH            10
> #define SQLITE_LIMIT_WORKER_THREADS           11
> 
> ```



These constants define various performance limits
that can be lowered at run\-time using [sqlite3\_limit()](../c3ref/limit.html).
The synopsis of the meanings of the various limits is shown below.
Additional information is available at [Limits in SQLite](../limits.html).




SQLITE\_LIMIT\_LENGTH
The maximum size of any string or BLOB or table row, in bytes.



SQLITE\_LIMIT\_SQL\_LENGTH
The maximum length of an SQL statement, in bytes.



SQLITE\_LIMIT\_COLUMN
The maximum number of columns in a table definition or in the
result set of a [SELECT](../lang_select.html) or the maximum number of columns in an index
or in an ORDER BY or GROUP BY clause.



SQLITE\_LIMIT\_EXPR\_DEPTH
The maximum depth of the parse tree on any expression.



SQLITE\_LIMIT\_COMPOUND\_SELECT
The maximum number of terms in a compound SELECT statement.



SQLITE\_LIMIT\_VDBE\_OP
The maximum number of instructions in a virtual machine program
used to implement an SQL statement. If [sqlite3\_prepare\_v2()](../c3ref/prepare.html) or
the equivalent tries to allocate space for more than this many opcodes
in a single prepared statement, an SQLITE\_NOMEM error is returned.



SQLITE\_LIMIT\_FUNCTION\_ARG
The maximum number of arguments on a function.



SQLITE\_LIMIT\_ATTACHED
The maximum number of [attached databases](../lang_attach.html).



SQLITE\_LIMIT\_LIKE\_PATTERN\_LENGTH
The maximum length of the pattern argument to the [LIKE](../lang_expr.html#like) or
[GLOB](../lang_expr.html#glob) operators.



SQLITE\_LIMIT\_VARIABLE\_NUMBER
The maximum index number of any [parameter](../lang_expr.html#varparam) in an SQL statement.



SQLITE\_LIMIT\_TRIGGER\_DEPTH
The maximum depth of recursion for triggers.



SQLITE\_LIMIT\_WORKER\_THREADS
The maximum number of auxiliary worker threads that a single
[prepared statement](../c3ref/stmt.html) may start.



See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


