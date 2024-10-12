




Write Data Into A BLOB Incrementally




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Write Data Into A BLOB Incrementally




> ```
> 
> int sqlite3_blob_write(sqlite3_blob *, const void *z, int n, int iOffset);
> 
> ```



This function is used to write data into an open [BLOB handle](../c3ref/blob.html) from a
caller\-supplied buffer. N bytes of data are copied from the buffer Z
into the open BLOB, starting at offset iOffset.


On success, sqlite3\_blob\_write() returns SQLITE\_OK.
Otherwise, an [error code](../rescode.html) or an [extended error code](../rescode.html#extrc) is returned.
Unless SQLITE\_MISUSE is returned, this function sets the
[database connection](../c3ref/sqlite3.html) error code and message accessible via
[sqlite3\_errcode()](../c3ref/errcode.html) and [sqlite3\_errmsg()](../c3ref/errcode.html) and related functions.


If the [BLOB handle](../c3ref/blob.html) passed as the first argument was not opened for
writing (the flags parameter to [sqlite3\_blob\_open()](../c3ref/blob_open.html) was zero),
this function returns [SQLITE\_READONLY](../rescode.html#readonly).


This function may only modify the contents of the BLOB; it is
not possible to increase the size of a BLOB using this API.
If offset iOffset is less than N bytes from the end of the BLOB,
[SQLITE\_ERROR](../rescode.html#error) is returned and no data is written. The size of the
BLOB (and hence the maximum value of N\+iOffset) can be determined
using the [sqlite3\_blob\_bytes()](../c3ref/blob_bytes.html) interface. If N or iOffset are less
than zero [SQLITE\_ERROR](../rescode.html#error) is returned and no data is written.


An attempt to write to an expired [BLOB handle](../c3ref/blob.html) fails with an
error code of [SQLITE\_ABORT](../rescode.html#abort). Writes to the BLOB that occurred
before the [BLOB handle](../c3ref/blob.html) expired are not rolled back by the
expiration of the handle, though of course those changes might
have been overwritten by the statement that expired the BLOB handle
or by other independent statements.


This routine only works on a [BLOB handle](../c3ref/blob.html) which has been created
by a prior successful call to [sqlite3\_blob\_open()](../c3ref/blob_open.html) and which has not
been closed by [sqlite3\_blob\_close()](../c3ref/blob_close.html). Passing any other pointer in
to this routine results in undefined and probably undesirable behavior.


See also: [sqlite3\_blob\_read()](../c3ref/blob_read.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


