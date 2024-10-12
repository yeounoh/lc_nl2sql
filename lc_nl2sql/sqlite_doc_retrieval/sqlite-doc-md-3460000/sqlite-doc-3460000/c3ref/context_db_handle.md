




Database Connection For Functions




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Database Connection For Functions




> ```
> 
> sqlite3 *sqlite3_context_db_handle(sqlite3_context*);
> 
> ```



The sqlite3\_context\_db\_handle() interface returns a copy of
the pointer to the [database connection](../c3ref/sqlite3.html) (the 1st parameter)
of the [sqlite3\_create\_function()](../c3ref/create_function.html)
and [sqlite3\_create\_function16()](../c3ref/create_function.html) routines that originally
registered the application defined function.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


