




Maximum xShmLock index




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Maximum xShmLock index




> ```
> 
> #define SQLITE_SHM_NLOCK        8
> 
> ```



The xShmLock method on [sqlite3\_io\_methods](../c3ref/io_methods.html) may use values
between 0 and this upper bound as its "offset" argument.
The SQLite core will never attempt to acquire or release a
lock outside of this range


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


