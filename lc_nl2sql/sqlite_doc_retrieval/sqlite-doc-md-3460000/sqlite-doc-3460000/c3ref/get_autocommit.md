




Test For Auto\-Commit Mode




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Test For Auto\-Commit Mode




> ```
> 
> int sqlite3_get_autocommit(sqlite3*);
> 
> ```



The sqlite3\_get\_autocommit() interface returns non\-zero or
zero if the given database connection is or is not in autocommit mode,
respectively. Autocommit mode is on by default.
Autocommit mode is disabled by a [BEGIN](../lang_transaction.html) statement.
Autocommit mode is re\-enabled by a [COMMIT](../lang_transaction.html) or [ROLLBACK](../lang_transaction.html).


If certain kinds of errors occur on a statement within a multi\-statement
transaction (errors including [SQLITE\_FULL](../rescode.html#full), [SQLITE\_IOERR](../rescode.html#ioerr),
[SQLITE\_NOMEM](../rescode.html#nomem), [SQLITE\_BUSY](../rescode.html#busy), and [SQLITE\_INTERRUPT](../rescode.html#interrupt)) then the
transaction might be rolled back automatically. The only way to
find out whether SQLite automatically rolled back the transaction after
an error is to use this function.


If another thread changes the autocommit status of the database
connection while this routine is running, then the return value
is undefined.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


