




Register A Virtual Table Implementation




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Register A Virtual Table Implementation




> ```
> 
> int sqlite3_create_module(
>   sqlite3 *db,               /* SQLite connection to register module with */
>   const char *zName,         /* Name of the module */
>   const sqlite3_module *p,   /* Methods for the module */
>   void *pClientData          /* Client data for xCreate/xConnect */
> );
> int sqlite3_create_module_v2(
>   sqlite3 *db,               /* SQLite connection to register module with */
>   const char *zName,         /* Name of the module */
>   const sqlite3_module *p,   /* Methods for the module */
>   void *pClientData,         /* Client data for xCreate/xConnect */
>   void(*xDestroy)(void*)     /* Module destructor function */
> );
> 
> ```



These routines are used to register a new [virtual table module](../c3ref/module.html) name.
Module names must be registered before
creating a new [virtual table](../vtab.html) using the module and before using a
preexisting [virtual table](../vtab.html) for the module.


The module name is registered on the [database connection](../c3ref/sqlite3.html) specified
by the first parameter. The name of the module is given by the
second parameter. The third parameter is a pointer to
the implementation of the [virtual table module](../c3ref/module.html). The fourth
parameter is an arbitrary client data pointer that is passed through
into the [xCreate](../vtab.html#xcreate) and [xConnect](../vtab.html#xconnect) methods of the virtual table module
when a new virtual table is be being created or reinitialized.


The sqlite3\_create\_module\_v2() interface has a fifth parameter which
is a pointer to a destructor for the pClientData. SQLite will
invoke the destructor function (if it is not NULL) when SQLite
no longer needs the pClientData pointer. The destructor will also
be invoked if the call to sqlite3\_create\_module\_v2() fails.
The sqlite3\_create\_module()
interface is equivalent to sqlite3\_create\_module\_v2() with a NULL
destructor.


If the third parameter (the pointer to the sqlite3\_module object) is
NULL then no new module is created and any existing modules with the
same name are dropped.


See also: [sqlite3\_drop\_modules()](../c3ref/drop_modules.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


