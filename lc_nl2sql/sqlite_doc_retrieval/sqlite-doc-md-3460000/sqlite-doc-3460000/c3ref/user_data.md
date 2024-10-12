




User Data For Functions




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## User Data For Functions




> ```
> 
> void *sqlite3_user_data(sqlite3_context*);
> 
> ```



The sqlite3\_user\_data() interface returns a copy of
the pointer that was the pUserData parameter (the 5th parameter)
of the [sqlite3\_create\_function()](../c3ref/create_function.html)
and [sqlite3\_create\_function16()](../c3ref/create_function.html) routines that originally
registered the application defined function.


This routine must be called from the same thread in which
the application\-defined function is running.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


