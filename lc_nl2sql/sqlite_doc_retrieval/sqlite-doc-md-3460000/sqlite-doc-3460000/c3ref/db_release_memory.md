




Free Memory Used By A Database Connection




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Free Memory Used By A Database Connection




> ```
> 
> int sqlite3_db_release_memory(sqlite3*);
> 
> ```



The sqlite3\_db\_release\_memory(D) interface attempts to free as much heap
memory as possible from database connection D. Unlike the
[sqlite3\_release\_memory()](../c3ref/release_memory.html) interface, this interface is in effect even
when the [SQLITE\_ENABLE\_MEMORY\_MANAGEMENT](../compile.html#enable_memory_management) compile\-time option is
omitted.


See also: [sqlite3\_release\_memory()](../c3ref/release_memory.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


