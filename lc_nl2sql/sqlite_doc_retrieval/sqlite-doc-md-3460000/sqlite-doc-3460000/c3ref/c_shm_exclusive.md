




Flags for the xShmLock VFS method




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Flags for the xShmLock VFS method




> ```
> 
> #define SQLITE_SHM_UNLOCK       1
> #define SQLITE_SHM_LOCK         2
> #define SQLITE_SHM_SHARED       4
> #define SQLITE_SHM_EXCLUSIVE    8
> 
> ```



These integer constants define the various locking operations
allowed by the xShmLock method of [sqlite3\_io\_methods](../c3ref/io_methods.html). The
following are the only legal combinations of flags to the
xShmLock method:


* SQLITE\_SHM\_LOCK \| SQLITE\_SHM\_SHARED
* SQLITE\_SHM\_LOCK \| SQLITE\_SHM\_EXCLUSIVE
* SQLITE\_SHM\_UNLOCK \| SQLITE\_SHM\_SHARED
* SQLITE\_SHM\_UNLOCK \| SQLITE\_SHM\_EXCLUSIVE



When unlocking, the same SHARED or EXCLUSIVE flag must be supplied as
was given on the corresponding lock.


The xShmLock method can transition between unlocked and SHARED or
between unlocked and EXCLUSIVE. It cannot transition between SHARED
and EXCLUSIVE.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


