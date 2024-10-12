




Query The EXPLAIN Setting For A Prepared Statement




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Query The EXPLAIN Setting For A Prepared Statement




> ```
> 
> int sqlite3_stmt_isexplain(sqlite3_stmt *pStmt);
> 
> ```



The sqlite3\_stmt\_isexplain(S) interface returns 1 if the
prepared statement S is an EXPLAIN statement, or 2 if the
statement S is an EXPLAIN QUERY PLAN.
The sqlite3\_stmt\_isexplain(S) interface returns 0 if S is
an ordinary statement or a NULL pointer.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


