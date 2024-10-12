




Destroy A Prepared Statement Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Destroy A Prepared Statement Object




> ```
> 
> int sqlite3_finalize(sqlite3_stmt *pStmt);
> 
> ```



The sqlite3\_finalize() function is called to delete a [prepared statement](../c3ref/stmt.html).
If the most recent evaluation of the statement encountered no errors
or if the statement is never been evaluated, then sqlite3\_finalize() returns
SQLITE\_OK. If the most recent evaluation of statement S failed, then
sqlite3\_finalize(S) returns the appropriate [error code](../rescode.html) or
[extended error code](../rescode.html#extrc).


The sqlite3\_finalize(S) routine can be called at any point during
the life cycle of [prepared statement](../c3ref/stmt.html) S:
before statement S is ever evaluated, after
one or more calls to [sqlite3\_reset()](../c3ref/reset.html), or after any call
to [sqlite3\_step()](../c3ref/step.html) regardless of whether or not the statement has
completed execution.


Invoking sqlite3\_finalize() on a NULL pointer is a harmless no\-op.


The application must finalize every [prepared statement](../c3ref/stmt.html) in order to avoid
resource leaks. It is a grievous error for the application to try to use
a prepared statement after it has been finalized. Any use of a prepared
statement after it has been finalized can result in undefined and
undesirable behavior such as segfaults and heap corruption.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


