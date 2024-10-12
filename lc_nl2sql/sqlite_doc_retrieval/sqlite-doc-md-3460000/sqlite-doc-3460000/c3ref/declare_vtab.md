




Declare The Schema Of A Virtual Table




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Declare The Schema Of A Virtual Table




> ```
> 
> int sqlite3_declare_vtab(sqlite3*, const char *zSQL);
> 
> ```



The [xCreate](../vtab.html#xcreate) and [xConnect](../vtab.html#xconnect) methods of a
[virtual table module](../c3ref/module.html) call this interface
to declare the format (the names and datatypes of the columns) of
the virtual tables they implement.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


