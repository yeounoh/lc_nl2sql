




Overload A Function For A Virtual Table




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Overload A Function For A Virtual Table




> ```
> 
> int sqlite3_overload_function(sqlite3*, const char *zFuncName, int nArg);
> 
> ```



Virtual tables can provide alternative implementations of functions
using the [xFindFunction](../vtab.html#xfindfunction) method of the [virtual table module](../c3ref/module.html).
But global versions of those functions
must exist in order to be overloaded.


This API makes sure a global version of a function with a particular
name and number of parameters exists. If no such function exists
before this API is called, a new function is created. The implementation
of the new function always causes an exception to be thrown. So
the new function is not good for anything by itself. Its only
purpose is to be a placeholder function that can be overloaded
by a [virtual table](../vtab.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


