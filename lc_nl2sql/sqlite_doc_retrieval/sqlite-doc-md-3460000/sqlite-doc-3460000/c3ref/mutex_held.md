




Mutex Verification Routines




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Mutex Verification Routines




> ```
> 
> #ifndef NDEBUG
> int sqlite3_mutex_held(sqlite3_mutex*);
> int sqlite3_mutex_notheld(sqlite3_mutex*);
> #endif
> 
> ```



The sqlite3\_mutex\_held() and sqlite3\_mutex\_notheld() routines
are intended for use inside assert() statements. The SQLite core
never uses these routines except inside an assert() and applications
are advised to follow the lead of the core. The SQLite core only
provides implementations for these routines when it is compiled
with the SQLITE\_DEBUG flag. External mutex implementations
are only required to provide these routines if SQLITE\_DEBUG is
defined and if NDEBUG is not defined.


These routines should return true if the mutex in their argument
is held or not held, respectively, by the calling thread.


The implementation is not required to provide versions of these
routines that actually work. If the implementation does not provide working
versions of these routines, it should at least provide stubs that always
return true so that one does not get spurious assertion failures.


If the argument to sqlite3\_mutex\_held() is a NULL pointer then
the routine should return 1\. This seems counter\-intuitive since
clearly the mutex cannot be held if it does not exist. But
the reason the mutex does not exist is because the build is not
using mutexes. And we do not want the assert() containing the
call to sqlite3\_mutex\_held() to fail, so a non\-zero return is
the appropriate thing to do. The sqlite3\_mutex\_notheld()
interface should also return 1 when given a NULL pointer.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


