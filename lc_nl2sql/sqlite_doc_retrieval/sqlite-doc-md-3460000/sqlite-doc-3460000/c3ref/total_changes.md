




Total Number Of Rows Modified




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Total Number Of Rows Modified




> ```
> 
> int sqlite3_total_changes(sqlite3*);
> sqlite3_int64 sqlite3_total_changes64(sqlite3*);
> 
> ```



These functions return the total number of rows inserted, modified or
deleted by all [INSERT](../lang_insert.html), [UPDATE](../lang_update.html) or [DELETE](../lang_delete.html) statements completed
since the database connection was opened, including those executed as
part of trigger programs. The two functions are identical except for the
type of the return value and that if the number of rows modified by the
connection exceeds the maximum value supported by type "int", then
the return value of sqlite3\_total\_changes() is undefined. Executing
any other type of SQL statement does not affect the value returned by
sqlite3\_total\_changes().


Changes made as part of [foreign key actions](../foreignkeys.html#fk_actions) are included in the
count, but those made as part of REPLACE constraint resolution are
not. Changes to a view that are intercepted by INSTEAD OF triggers
are not counted.


The [sqlite3\_total\_changes(D)](../c3ref/total_changes.html) interface only reports the number
of rows that changed due to SQL statement run against database
connection D. Any changes by other database connections are ignored.
To detect changes against a database file from other database
connections use the [PRAGMA data\_version](../pragma.html#pragma_data_version) command or the
[SQLITE\_FCNTL\_DATA\_VERSION](../c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntldataversion) [file control](../c3ref/file_control.html).


If a separate thread makes changes on the same database connection
while [sqlite3\_total\_changes()](../c3ref/total_changes.html) is running then the value
returned is unpredictable and not meaningful.


See also:
* the [sqlite3\_changes()](../c3ref/changes.html) interface
* the [count\_changes pragma](../pragma.html#pragma_count_changes)* the [changes() SQL function](../lang_corefunc.html#changes)* the [data\_version pragma](../pragma.html#pragma_data_version)* the [SQLITE\_FCNTL\_DATA\_VERSION](../c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntldataversion) [file control](../c3ref/file_control.html)




See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


