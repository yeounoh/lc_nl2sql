




Number of columns in a result set




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Number of columns in a result set




> ```
> 
> int sqlite3_data_count(sqlite3_stmt *pStmt);
> 
> ```



The sqlite3\_data\_count(P) interface returns the number of columns in the
current row of the result set of [prepared statement](../c3ref/stmt.html) P.
If prepared statement P does not have results ready to return
(via calls to the [sqlite3\_column()](../c3ref/column_blob.html) family of
interfaces) then sqlite3\_data\_count(P) returns 0\.
The sqlite3\_data\_count(P) routine also returns 0 if P is a NULL pointer.
The sqlite3\_data\_count(P) routine returns 0 if the previous call to
[sqlite3\_step](../c3ref/step.html)(P) returned [SQLITE\_DONE](../rescode.html#done). The sqlite3\_data\_count(P)
will return non\-zero if previous call to [sqlite3\_step](../c3ref/step.html)(P) returned
[SQLITE\_ROW](../rescode.html#row), except in the case of the [PRAGMA incremental\_vacuum](../pragma.html#pragma_incremental_vacuum)
where it always returns zero since each step of that multi\-step
pragma returns 0 columns of data.


See also: [sqlite3\_column\_count()](../c3ref/column_count.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


