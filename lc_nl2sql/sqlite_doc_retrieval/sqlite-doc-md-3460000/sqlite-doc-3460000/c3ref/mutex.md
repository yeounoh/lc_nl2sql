




Mutex Handle




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Mutex Handle




> ```
> 
> typedef struct sqlite3_mutex sqlite3_mutex;
> 
> ```



The mutex module within SQLite defines [sqlite3\_mutex](../c3ref/mutex.html) to be an
abstract type for a mutex object. The SQLite core never looks
at the internal representation of an [sqlite3\_mutex](../c3ref/mutex.html). It only
deals with pointers to the [sqlite3\_mutex](../c3ref/mutex.html) object.


Mutexes are created using [sqlite3\_mutex\_alloc()](../c3ref/mutex_alloc.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


