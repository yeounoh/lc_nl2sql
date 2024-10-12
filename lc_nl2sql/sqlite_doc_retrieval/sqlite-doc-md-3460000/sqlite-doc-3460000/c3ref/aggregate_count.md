




Deprecated Functions




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Deprecated Functions




> ```
> 
> #ifndef SQLITE_OMIT_DEPRECATED
> int sqlite3_aggregate_count(sqlite3_context*);
> int sqlite3_expired(sqlite3_stmt*);
> int sqlite3_transfer_bindings(sqlite3_stmt*, sqlite3_stmt*);
> int sqlite3_global_recover(void);
> void sqlite3_thread_cleanup(void);
> int sqlite3_memory_alarm(void(*)(void*,sqlite3_int64,int),
>                       void*,sqlite3_int64);
> #endif
> 
> ```



These functions are [deprecated](../c3ref/experimental.html). In order to maintain
backwards compatibility with older code, these functions continue
to be supported. However, new applications should avoid
the use of these functions. To encourage programmers to avoid
these functions, we will not explain what they do.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


