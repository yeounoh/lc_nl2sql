




Determine The Virtual Table Conflict Policy




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Determine The Virtual Table Conflict Policy




> ```
> 
> int sqlite3_vtab_on_conflict(sqlite3 *);
> 
> ```



This function may only be called from within a call to the [xUpdate](../vtab.html#xupdate) method
of a [virtual table](../vtab.html) implementation for an INSERT or UPDATE operation. The
value returned is one of [SQLITE\_ROLLBACK](../c3ref/c_fail.html), [SQLITE\_IGNORE](../c3ref/c_deny.html), [SQLITE\_FAIL](../c3ref/c_fail.html),
[SQLITE\_ABORT](../rescode.html#abort), or [SQLITE\_REPLACE](../c3ref/c_fail.html), according to the [ON CONFLICT](../lang_conflict.html) mode
of the SQL statement that triggered the call to the [xUpdate](../vtab.html#xupdate) method of the
[virtual table](../vtab.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


