




Retrieve the mutex for a database connection




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Retrieve the mutex for a database connection




> ```
> 
> sqlite3_mutex *sqlite3_db_mutex(sqlite3*);
> 
> ```



This interface returns a pointer the [sqlite3\_mutex](../c3ref/mutex.html) object that
serializes access to the [database connection](../c3ref/sqlite3.html) given in the argument
when the [threading mode](../threadsafe.html) is Serialized.
If the [threading mode](../threadsafe.html) is Single\-thread or Multi\-thread then this
routine returns a NULL pointer.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


