




Dynamically Typed Value Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Dynamically Typed Value Object




> ```
> 
> typedef struct sqlite3_value sqlite3_value;
> 
> ```



SQLite uses the sqlite3\_value object to represent all values
that can be stored in a database table. SQLite uses dynamic typing
for the values it stores. Values stored in sqlite3\_value objects
can be integers, floating point values, strings, BLOBs, or NULL.


An sqlite3\_value object may be either "protected" or "unprotected".
Some interfaces require a protected sqlite3\_value. Other interfaces
will accept either a protected or an unprotected sqlite3\_value.
Every interface that accepts sqlite3\_value arguments specifies
whether or not it requires a protected sqlite3\_value. The
[sqlite3\_value\_dup()](../c3ref/value_dup.html) interface can be used to construct a new
protected sqlite3\_value from an unprotected sqlite3\_value.


The terms "protected" and "unprotected" refer to whether or not
a mutex is held. An internal mutex is held for a protected
sqlite3\_value object but no mutex is held for an unprotected
sqlite3\_value object. If SQLite is compiled to be single\-threaded
(with [SQLITE\_THREADSAFE\=0](../compile.html#threadsafe) and with [sqlite3\_threadsafe()](../c3ref/threadsafe.html) returning 0\)
or if SQLite is run in one of reduced mutex modes
[SQLITE\_CONFIG\_SINGLETHREAD](../c3ref/c_config_covering_index_scan.html#sqliteconfigsinglethread) or [SQLITE\_CONFIG\_MULTITHREAD](../c3ref/c_config_covering_index_scan.html#sqliteconfigmultithread)
then there is no distinction between protected and unprotected
sqlite3\_value objects and they can be used interchangeably. However,
for maximum code portability it is recommended that applications
still make the distinction between protected and unprotected
sqlite3\_value objects even when not strictly required.


The sqlite3\_value objects that are passed as parameters into the
implementation of [application\-defined SQL functions](../appfunc.html) are protected.
The sqlite3\_value objects returned by [sqlite3\_vtab\_rhs\_value()](../c3ref/vtab_rhs_value.html)
are protected.
The sqlite3\_value object returned by
[sqlite3\_column\_value()](../c3ref/column_blob.html) is unprotected.
Unprotected sqlite3\_value objects may only be used as arguments
to [sqlite3\_result\_value()](../c3ref/result_blob.html), [sqlite3\_bind\_value()](../c3ref/bind_blob.html), and
[sqlite3\_value\_dup()](../c3ref/value_dup.html).
The [sqlite3\_value\_type()](../c3ref/value_blob.html) family of
interfaces require protected sqlite3\_value objects.


19 Methods using this object:

* [sqlite3\_value\_blob](../c3ref/value_blob.html)
* [sqlite3\_value\_bytes](../c3ref/value_blob.html)
* [sqlite3\_value\_bytes16](../c3ref/value_blob.html)
* [sqlite3\_value\_double](../c3ref/value_blob.html)
* [sqlite3\_value\_dup](../c3ref/value_dup.html)
* [sqlite3\_value\_encoding](../c3ref/value_encoding.html)
* [sqlite3\_value\_free](../c3ref/value_dup.html)
* [sqlite3\_value\_frombind](../c3ref/value_blob.html)
* [sqlite3\_value\_int](../c3ref/value_blob.html)
* [sqlite3\_value\_int64](../c3ref/value_blob.html)
* [sqlite3\_value\_nochange](../c3ref/value_blob.html)
* [sqlite3\_value\_numeric\_type](../c3ref/value_blob.html)
* [sqlite3\_value\_pointer](../c3ref/value_blob.html)
* [sqlite3\_value\_subtype](../c3ref/value_subtype.html)
* [sqlite3\_value\_text](../c3ref/value_blob.html)
* [sqlite3\_value\_text16](../c3ref/value_blob.html)
* [sqlite3\_value\_text16be](../c3ref/value_blob.html)
* [sqlite3\_value\_text16le](../c3ref/value_blob.html)
* [sqlite3\_value\_type](../c3ref/value_blob.html)






See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


