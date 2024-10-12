




Prepared Statement Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Prepared Statement Object




> ```
> 
> typedef struct sqlite3_stmt sqlite3_stmt;
> 
> ```



An instance of this object represents a single SQL statement that
has been compiled into binary form and is ready to be evaluated.


Think of each SQL statement as a separate computer program. The
original SQL text is source code. A prepared statement object
is the compiled object code. All SQL must be converted into a
prepared statement before it can be run.


The life\-cycle of a prepared statement object usually goes like this:


1. Create the prepared statement object using [sqlite3\_prepare\_v2()](../c3ref/prepare.html).
- Bind values to [parameters](../lang_expr.html#varparam) using the sqlite3\_bind\_\*()
interfaces.
- Run the SQL by calling [sqlite3\_step()](../c3ref/step.html) one or more times.
- Reset the prepared statement using [sqlite3\_reset()](../c3ref/reset.html) then go back
to step 2\. Do this zero or more times.
- Destroy the object using [sqlite3\_finalize()](../c3ref/finalize.html).




6 Constructors using this object:

* [sqlite3\_prepare](../c3ref/prepare.html)
* [sqlite3\_prepare16](../c3ref/prepare.html)
* [sqlite3\_prepare16\_v2](../c3ref/prepare.html)
* [sqlite3\_prepare16\_v3](../c3ref/prepare.html)
* [sqlite3\_prepare\_v2](../c3ref/prepare.html)
* [sqlite3\_prepare\_v3](../c3ref/prepare.html)






1 Destructor using this object: [sqlite3\_finalize()](../c3ref/finalize.html)


53 Methods using this object:

* [sqlite3\_bind\_blob](../c3ref/bind_blob.html)
* [sqlite3\_bind\_blob64](../c3ref/bind_blob.html)
* [sqlite3\_bind\_double](../c3ref/bind_blob.html)
* [sqlite3\_bind\_int](../c3ref/bind_blob.html)
* [sqlite3\_bind\_int64](../c3ref/bind_blob.html)
* [sqlite3\_bind\_null](../c3ref/bind_blob.html)
* [sqlite3\_bind\_parameter\_count](../c3ref/bind_parameter_count.html)
* [sqlite3\_bind\_parameter\_index](../c3ref/bind_parameter_index.html)
* [sqlite3\_bind\_parameter\_name](../c3ref/bind_parameter_name.html)
* [sqlite3\_bind\_pointer](../c3ref/bind_blob.html)
* [sqlite3\_bind\_text](../c3ref/bind_blob.html)
* [sqlite3\_bind\_text16](../c3ref/bind_blob.html)
* [sqlite3\_bind\_text64](../c3ref/bind_blob.html)
* [sqlite3\_bind\_value](../c3ref/bind_blob.html)
* [sqlite3\_bind\_zeroblob](../c3ref/bind_blob.html)
* [sqlite3\_bind\_zeroblob64](../c3ref/bind_blob.html)
* [sqlite3\_clear\_bindings](../c3ref/clear_bindings.html)
* [sqlite3\_column\_blob](../c3ref/column_blob.html)
* [sqlite3\_column\_bytes](../c3ref/column_blob.html)
* [sqlite3\_column\_bytes16](../c3ref/column_blob.html)
* [sqlite3\_column\_count](../c3ref/column_count.html)
* [sqlite3\_column\_database\_name](../c3ref/column_database_name.html)
* [sqlite3\_column\_database\_name16](../c3ref/column_database_name.html)
* [sqlite3\_column\_decltype](../c3ref/column_decltype.html)
* [sqlite3\_column\_decltype16](../c3ref/column_decltype.html)
* [sqlite3\_column\_double](../c3ref/column_blob.html)
* [sqlite3\_column\_int](../c3ref/column_blob.html)
* [sqlite3\_column\_int64](../c3ref/column_blob.html)
* [sqlite3\_column\_name](../c3ref/column_name.html)
* [sqlite3\_column\_name16](../c3ref/column_name.html)
* [sqlite3\_column\_origin\_name](../c3ref/column_database_name.html)
* [sqlite3\_column\_origin\_name16](../c3ref/column_database_name.html)
* [sqlite3\_column\_table\_name](../c3ref/column_database_name.html)
* [sqlite3\_column\_table\_name16](../c3ref/column_database_name.html)
* [sqlite3\_column\_text](../c3ref/column_blob.html)
* [sqlite3\_column\_text16](../c3ref/column_blob.html)
* [sqlite3\_column\_type](../c3ref/column_blob.html)
* [sqlite3\_column\_value](../c3ref/column_blob.html)
* [sqlite3\_data\_count](../c3ref/data_count.html)
* [sqlite3\_db\_handle](../c3ref/db_handle.html)
* [sqlite3\_expanded\_sql](../c3ref/expanded_sql.html)
* [sqlite3\_normalized\_sql](../c3ref/expanded_sql.html)
* [sqlite3\_reset](../c3ref/reset.html)
* [sqlite3\_sql](../c3ref/expanded_sql.html)
* [sqlite3\_step](../c3ref/step.html)
* [sqlite3\_stmt\_busy](../c3ref/stmt_busy.html)
* [sqlite3\_stmt\_explain](../c3ref/stmt_explain.html)
* [sqlite3\_stmt\_isexplain](../c3ref/stmt_isexplain.html)
* [sqlite3\_stmt\_readonly](../c3ref/stmt_readonly.html)
* [sqlite3\_stmt\_scanstatus](../c3ref/stmt_scanstatus.html)
* [sqlite3\_stmt\_scanstatus\_reset](../c3ref/stmt_scanstatus_reset.html)
* [sqlite3\_stmt\_scanstatus\_v2](../c3ref/stmt_scanstatus.html)
* [sqlite3\_stmt\_status](../c3ref/stmt_status.html)






See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


