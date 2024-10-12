




Set the Last Insert Rowid value.




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Set the Last Insert Rowid value.




> ```
> 
> void sqlite3_set_last_insert_rowid(sqlite3*,sqlite3_int64);
> 
> ```



The sqlite3\_set\_last\_insert\_rowid(D, R) method allows the application to
set the value returned by calling sqlite3\_last\_insert\_rowid(D) to R
without inserting a row into the database.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


