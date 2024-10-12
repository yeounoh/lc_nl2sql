




Autovacuum Compaction Amount Callback




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Autovacuum Compaction Amount Callback




> ```
> 
> int sqlite3_autovacuum_pages(
>   sqlite3 *db,
>   unsigned int(*)(void*,const char*,unsigned int,unsigned int,unsigned int),
>   void*,
>   void(*)(void*)
> );
> 
> ```



The sqlite3\_autovacuum\_pages(D,C,P,X) interface registers a callback
function C that is invoked prior to each autovacuum of the database
file. The callback is passed a copy of the generic data pointer (P),
the schema\-name of the attached database that is being autovacuumed,
the size of the database file in pages, the number of free pages,
and the number of bytes per page, respectively. The callback should
return the number of free pages that should be removed by the
autovacuum. If the callback returns zero, then no autovacuum happens.
If the value returned is greater than or equal to the number of
free pages, then a complete autovacuum happens.


If there are multiple ATTACH\-ed database files that are being
modified as part of a transaction commit, then the autovacuum pages
callback is invoked separately for each file.


**The callback is not reentrant.** The callback function should
not attempt to invoke any other SQLite interface. If it does, bad
things may happen, including segmentation faults and corrupt database
files. The callback function should be a simple function that
does some arithmetic on its input parameters and returns a result.


The X parameter to sqlite3\_autovacuum\_pages(D,C,P,X) is an optional
destructor for the P parameter. If X is not NULL, then X(P) is
invoked whenever the database connection closes or when the callback
is overwritten by another invocation of sqlite3\_autovacuum\_pages().


There is only one autovacuum pages callback per database connection.
Each call to the sqlite3\_autovacuum\_pages() interface overrides all
previous invocations for that database connection. If the callback
argument (C) to sqlite3\_autovacuum\_pages(D,C,P,X) is a NULL pointer,
then the autovacuum steps callback is canceled. The return value
from sqlite3\_autovacuum\_pages() is normally SQLITE\_OK, but might
be some other error code if something goes wrong. The current
implementation will only return SQLITE\_OK or SQLITE\_MISUSE, but other
return codes might be added in future releases.


If no autovacuum pages callback is specified (the usual case) or
a NULL pointer is provided for the callback,
then the default behavior is to vacuum all free pages. So, in other
words, the default behavior is the same as if the callback function
were something like this:



> ```
> 
>     unsigned int demonstration_autovac_pages_callback(
>       void *pClientData,
>       const char *zSchema,
>       unsigned int nDbPage,
>       unsigned int nFreePage,
>       unsigned int nBytePerPage
>     ){
>       return nFreePage;
>     }
> 
> ```




See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).










