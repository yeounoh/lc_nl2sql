




Determine if a database is read\-only




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Determine if a database is read\-only




> ```
> 
> int sqlite3_db_readonly(sqlite3 *db, const char *zDbName);
> 
> ```



The sqlite3\_db\_readonly(D,N) interface returns 1 if the database N
of connection D is read\-only, 0 if it is read/write, or \-1 if N is not
the name of a database on connection D.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


