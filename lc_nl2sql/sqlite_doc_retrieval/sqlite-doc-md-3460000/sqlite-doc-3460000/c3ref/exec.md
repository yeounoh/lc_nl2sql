




One\-Step Query Execution Interface




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## One\-Step Query Execution Interface




> ```
> 
> int sqlite3_exec(
>   sqlite3*,                                  /* An open database */
>   const char *sql,                           /* SQL to be evaluated */
>   int (*callback)(void*,int,char**,char**),  /* Callback function */
>   void *,                                    /* 1st argument to callback */
>   char **errmsg                              /* Error msg written here */
> );
> 
> ```



The sqlite3\_exec() interface is a convenience wrapper around
[sqlite3\_prepare\_v2()](../c3ref/prepare.html), [sqlite3\_step()](../c3ref/step.html), and [sqlite3\_finalize()](../c3ref/finalize.html),
that allows an application to run multiple statements of SQL
without having to use a lot of C code.


The sqlite3\_exec() interface runs zero or more UTF\-8 encoded,
semicolon\-separate SQL statements passed into its 2nd argument,
in the context of the [database connection](../c3ref/sqlite3.html) passed in as its 1st
argument. If the callback function of the 3rd argument to
sqlite3\_exec() is not NULL, then it is invoked for each result row
coming out of the evaluated SQL statements. The 4th argument to
sqlite3\_exec() is relayed through to the 1st argument of each
callback invocation. If the callback pointer to sqlite3\_exec()
is NULL, then no callback is ever invoked and result rows are
ignored.


If an error occurs while evaluating the SQL statements passed into
sqlite3\_exec(), then execution of the current statement stops and
subsequent statements are skipped. If the 5th parameter to sqlite3\_exec()
is not NULL then any error message is written into memory obtained
from [sqlite3\_malloc()](../c3ref/free.html) and passed back through the 5th parameter.
To avoid memory leaks, the application should invoke [sqlite3\_free()](../c3ref/free.html)
on error message strings returned through the 5th parameter of
sqlite3\_exec() after the error message string is no longer needed.
If the 5th parameter to sqlite3\_exec() is not NULL and no errors
occur, then sqlite3\_exec() sets the pointer in its 5th parameter to
NULL before returning.


If an sqlite3\_exec() callback returns non\-zero, the sqlite3\_exec()
routine returns SQLITE\_ABORT without invoking the callback again and
without running any subsequent SQL statements.


The 2nd argument to the sqlite3\_exec() callback function is the
number of columns in the result. The 3rd argument to the sqlite3\_exec()
callback is an array of pointers to strings obtained as if from
[sqlite3\_column\_text()](../c3ref/column_blob.html), one for each column. If an element of a
result row is NULL then the corresponding string pointer for the
sqlite3\_exec() callback is a NULL pointer. The 4th argument to the
sqlite3\_exec() callback is an array of pointers to strings where each
entry represents the name of corresponding result column as obtained
from [sqlite3\_column\_name()](../c3ref/column_name.html).


If the 2nd parameter to sqlite3\_exec() is a NULL pointer, a pointer
to an empty string, or a pointer that contains only whitespace and/or
SQL comments, then no SQL statements are evaluated and the database
is not changed.


Restrictions:


* The application must ensure that the 1st parameter to sqlite3\_exec()
is a valid and open [database connection](../c3ref/sqlite3.html).
* The application must not close the [database connection](../c3ref/sqlite3.html) specified by
the 1st parameter to sqlite3\_exec() while sqlite3\_exec() is running.
* The application must not modify the SQL statement text passed into
the 2nd parameter of sqlite3\_exec() while sqlite3\_exec() is running.
* The application must not dereference the arrays or string pointers
passed as the 3rd and 4th callback parameters after it returns.




See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


