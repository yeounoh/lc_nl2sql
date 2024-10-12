




The Carray() Table\-Valued Function




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Carray() Table\-Valued Function


# 1\. Overview


Carray() is a [table\-valued function](vtab.html#tabfunc2) with a single column (named
"value") and zero or more rows.
The "value" of each row in the carray() is taken from a C\-language array
supplied by the application via [parameter binding](c3ref/bind_blob.html).
In this way, the carray() function provides a convenient mechanism to
bind C\-language arrays to SQL queries.



# 2\. Availability


The carray() function is not compiled into SQLite by default.
It is available as a [loadable extension](loadext.html) in the
[ext/misc/carray.c](https://www.sqlite.org/src/file/ext/misc/carray.c)
source file.



The carray() function was first added to SQLite in version 3\.14
(2016\-08\-08\). The sqlite3\_carray\_bind() interface and the
single\-argument variant of carray() was added in SQLite version 3\.34\.0
(2020\-12\-01\). The ability to bind an array of struct iovec
objects that are interpreted as BLOBs was added in SQLite version 3\.41\.0
(2023\-02\-21\).



# 3\. Details


The carray() function takes one, two, or three arguments.



For the two\- and three\-argument versions of carray(),
the first argument is a pointer to an array. Since pointer values cannot
be specified directly in SQL, the first argument must be a [parameter](lang_expr.html#varparam) that
is bound to a pointer value using the [sqlite3\_bind\_pointer()](c3ref/bind_blob.html) interface
using a pointer\-type of "carray".
The second argument is the number of elements in the array. The optional
third argument is a string that determines the datatype of the elements
in the C\-language array. Allowed values for the third argument are:



1. 'int32'
2. 'int64'
3. 'double'
4. 'char\*'
5. 'struct iovec'


The default datatype is 'int32'.



The 'struct iovec' type used for BLOB data is a standard Posix data
structure, normally declared using "\#include \<sys/uio.h\>".
The format is:




> ```
> 
> struct iovec {
>   void  *iov_base; /* Starting address */
>   size_t iov_len;  /* Number of bytes to transfer */
> };
> 
> ```



## 3\.1\. Single\-Argument CARRAY


The single\-argument form of carray() requires a special C\-language
interface named "sqlite3\_carray\_bind()" in order to attach values:




> ```
> 
>   int sqlite3_carray_bind(
>     sqlite3_stmt *pStmt,         /* Statement containing the CARRAY */
>     int idx,                     /* Parameter number for CARRAY argument */
>     void *aData,                 /* Data array */
>     int nData,                   /* Number of entries in the array */
>     int mFlags,                  /* Datatype flag */
>     void (*xDestroy)(void*)      /* Destructor for aData */
>   );
> 
> ```


The mFlags parameter to sqlite3\_carray\_bind() must be one of:




> ```
> 
>   #define CARRAY_INT32   0
>   #define CARRAY_INT64   1
>   #define CARRAY_DOUBLE  2
>   #define CARRAY_TEXT    3
>   #define CARRAY_BLOB    4
> 
> ```


Higher order bits of the mFlags parameter must all be zero for now,
though they may be used in future enhancements. The definitions for the
constants that specify the datatype and a prototype for the
sqlite3\_carray\_bind() function are both available in the auxiliary
header file
[ext/misc/carray.h](https://www.sqlite.org/src/file/ext/misc/carray.h).



The xDestroy argument to sqlite3\_carray\_bind() routine is a pointer
to a function that frees the input array. SQLite will invoke this
function after it has finished with the data. The xDestroy argument
may optionally be one of the following constants defined in
"sqlite3\.h":



* [SQLITE\_STATIC](c3ref/c_static.html) → This means that the application that invokes
 sqlite3\_carray\_bind() maintains ownership of the data array and that
 the application promises SQLite that it will not change or deallocate
 the data until after the prepared statement is finialized.
* [SQLITE\_TRANSIENT](c3ref/c_static.html) → This special value instructs SQLite to make
 its own private copy of the data before the 
 sqlite3\_carray\_bind() interface returns.


# 4\. Usage


The carray() function can be used in the FROM clause of a query.
For example, to query two entries from the OBJ table using rowids
taken from a C\-language array at address $PTR.




```
SELECT obj.* FROM obj, carray($PTR, 10) AS x
 WHERE obj.rowid=x.value;

```

This query gives the same result:




```
SELECT * FROM obj WHERE rowid IN carray($PTR, 10);

```

*This page last modified on [2023\-02\-17 13:24:09](https://sqlite.org/docsrc/honeypot) UTC* 


