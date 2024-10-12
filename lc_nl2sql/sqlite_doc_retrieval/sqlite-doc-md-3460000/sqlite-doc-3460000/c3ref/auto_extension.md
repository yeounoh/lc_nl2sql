




Automatically Load Statically Linked Extensions




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Automatically Load Statically Linked Extensions




> ```
> 
> int sqlite3_auto_extension(void(*xEntryPoint)(void));
> 
> ```



This interface causes the xEntryPoint() function to be invoked for
each new [database connection](../c3ref/sqlite3.html) that is created. The idea here is that
xEntryPoint() is the entry point for a statically linked [SQLite extension](../loadext.html)
that is to be automatically loaded into all new database connections.


Even though the function prototype shows that xEntryPoint() takes
no arguments and returns void, SQLite invokes xEntryPoint() with three
arguments and expects an integer result as if the signature of the
entry point where as follows:



> ```
> 
>    int xEntryPoint(
>      sqlite3 *db,
>      const char **pzErrMsg,
>      const struct sqlite3_api_routines *pThunk
>    );
> 
> ```




If the xEntryPoint routine encounters an error, it should make \*pzErrMsg
point to an appropriate error message (obtained from [sqlite3\_mprintf()](../c3ref/mprintf.html))
and return an appropriate [error code](../rescode.html). SQLite ensures that \*pzErrMsg
is NULL before calling the xEntryPoint(). SQLite will invoke
[sqlite3\_free()](../c3ref/free.html) on \*pzErrMsg after xEntryPoint() returns. If any
xEntryPoint() returns an error, the [sqlite3\_open()](../c3ref/open.html), [sqlite3\_open16()](../c3ref/open.html),
or [sqlite3\_open\_v2()](../c3ref/open.html) call that provoked the xEntryPoint() will fail.


Calling sqlite3\_auto\_extension(X) with an entry point X that is already
on the list of automatic extensions is a harmless no\-op. No entry point
will be called more than once for each database connection that is opened.


See also: [sqlite3\_reset\_auto\_extension()](../c3ref/reset_auto_extension.html)
and [sqlite3\_cancel\_auto\_extension()](../c3ref/cancel_auto_extension.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


