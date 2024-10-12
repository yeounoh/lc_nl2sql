




File Locking Levels




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## File Locking Levels




> ```
> 
> #define SQLITE_LOCK_NONE          0       /* xUnlock() only */
> #define SQLITE_LOCK_SHARED        1       /* xLock() or xUnlock() */
> #define SQLITE_LOCK_RESERVED      2       /* xLock() only */
> #define SQLITE_LOCK_PENDING       3       /* xLock() only */
> #define SQLITE_LOCK_EXCLUSIVE     4       /* xLock() only */
> 
> ```



SQLite uses one of these integer values as the second
argument to calls it makes to the xLock() and xUnlock() methods
of an [sqlite3\_io\_methods](../c3ref/io_methods.html) object. These values are ordered from
lest restrictive to most restrictive.


The argument to xLock() is always SHARED or higher. The argument to
xUnlock is either SHARED or NONE.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


