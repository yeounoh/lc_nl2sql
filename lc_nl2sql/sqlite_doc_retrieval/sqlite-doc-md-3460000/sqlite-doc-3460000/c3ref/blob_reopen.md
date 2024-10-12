




Move a BLOB Handle to a New Row




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Move a BLOB Handle to a New Row




> ```
> 
> int sqlite3_blob_reopen(sqlite3_blob *, sqlite3_int64);
> 
> ```



This function is used to move an existing [BLOB handle](../c3ref/blob.html) so that it points
to a different row of the same database table. The new row is identified
by the rowid value passed as the second argument. Only the row can be
changed. The database, table and column on which the blob handle is open
remain the same. Moving an existing [BLOB handle](../c3ref/blob.html) to a new row is
faster than closing the existing handle and opening a new one.


The new row must meet the same criteria as for [sqlite3\_blob\_open()](../c3ref/blob_open.html) \-
it must exist and there must be either a blob or text value stored in
the nominated column. If the new row is not present in the table, or if
it does not contain a blob or text value, or if another error occurs, an
SQLite error code is returned and the blob handle is considered aborted.
All subsequent calls to [sqlite3\_blob\_read()](../c3ref/blob_read.html), [sqlite3\_blob\_write()](../c3ref/blob_write.html) or
[sqlite3\_blob\_reopen()](../c3ref/blob_reopen.html) on an aborted blob handle immediately return
SQLITE\_ABORT. Calling [sqlite3\_blob\_bytes()](../c3ref/blob_bytes.html) on an aborted blob handle
always returns zero.


This function sets the database handle error code and message.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


