




Attempt To Free Heap Memory




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Attempt To Free Heap Memory




> ```
> 
> int sqlite3_release_memory(int);
> 
> ```



The sqlite3\_release\_memory() interface attempts to free N bytes
of heap memory by deallocating non\-essential memory allocations
held by the database library. Memory used to cache database
pages to improve performance is an example of non\-essential memory.
sqlite3\_release\_memory() returns the number of bytes actually freed,
which might be more or less than the amount requested.
The sqlite3\_release\_memory() routine is a no\-op returning zero
if SQLite is not compiled with [SQLITE\_ENABLE\_MEMORY\_MANAGEMENT](../compile.html#enable_memory_management).


See also: [sqlite3\_db\_release\_memory()](../c3ref/db_release_memory.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


