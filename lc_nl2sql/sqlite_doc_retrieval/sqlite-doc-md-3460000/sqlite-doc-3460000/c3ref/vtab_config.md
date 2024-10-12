




Virtual Table Interface Configuration




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Virtual Table Interface Configuration




> ```
> 
> int sqlite3_vtab_config(sqlite3*, int op, ...);
> 
> ```



This function may be called by either the [xConnect](../vtab.html#xconnect) or [xCreate](../vtab.html#xcreate) method
of a [virtual table](../vtab.html) implementation to configure
various facets of the virtual table interface.


If this interface is invoked outside the context of an xConnect or
xCreate virtual table method then the behavior is undefined.


In the call sqlite3\_vtab\_config(D,C,...) the D parameter is the
[database connection](../c3ref/sqlite3.html) in which the virtual table is being created and
which is passed in as the first argument to the [xConnect](../vtab.html#xconnect) or [xCreate](../vtab.html#xcreate)
method that is invoking sqlite3\_vtab\_config(). The C parameter is one
of the [virtual table configuration options](../c3ref/c_vtab_constraint_support.html). The presence and meaning
of parameters after C depend on which [virtual table configuration option](../c3ref/c_vtab_constraint_support.html)
is used.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


