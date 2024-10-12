




Constants Defining Special Destructor Behavior




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Constants Defining Special Destructor Behavior




> ```
> 
> typedef void (*sqlite3_destructor_type)(void*);
> #define SQLITE_STATIC      ((sqlite3_destructor_type)0)
> #define SQLITE_TRANSIENT   ((sqlite3_destructor_type)-1)
> 
> ```



These are special values for the destructor that is passed in as the
final argument to routines like [sqlite3\_result\_blob()](../c3ref/result_blob.html). If the destructor
argument is SQLITE\_STATIC, it means that the content pointer is constant
and will never change. It does not need to be destroyed. The
SQLITE\_TRANSIENT value means that the content will likely change in
the near future and that SQLite should make its own private copy of
the content before returning.


The typedef is necessary to work around problems in certain
C\+\+ compilers.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


