




Copy And Free SQL Values




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Copy And Free SQL Values




> ```
> 
> sqlite3_value *sqlite3_value_dup(const sqlite3_value*);
> void sqlite3_value_free(sqlite3_value*);
> 
> ```



The sqlite3\_value\_dup(V) interface makes a copy of the [sqlite3\_value](../c3ref/value.html)
object D and returns a pointer to that copy. The [sqlite3\_value](../c3ref/value.html) returned
is a [protected sqlite3\_value](../c3ref/value.html) object even if the input is not.
The sqlite3\_value\_dup(V) interface returns NULL if V is NULL or if a
memory allocation fails. If V is a [pointer value](../bindptr.html), then the result
of sqlite3\_value\_dup(V) is a NULL value.


The sqlite3\_value\_free(V) interface frees an [sqlite3\_value](../c3ref/value.html) object
previously obtained from [sqlite3\_value\_dup()](../c3ref/value_dup.html). If V is a NULL pointer
then sqlite3\_value\_free(V) is a harmless no\-op.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


