




Return The Size Of An Open BLOB




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Return The Size Of An Open BLOB




> ```
> 
> int sqlite3_blob_bytes(sqlite3_blob *);
> 
> ```



Returns the size in bytes of the BLOB accessible via the
successfully opened [BLOB handle](../c3ref/blob.html) in its only argument. The
incremental blob I/O routines can only read or overwriting existing
blob content; they cannot change the size of a blob.


This routine only works on a [BLOB handle](../c3ref/blob.html) which has been created
by a prior successful call to [sqlite3\_blob\_open()](../c3ref/blob_open.html) and which has not
been closed by [sqlite3\_blob\_close()](../c3ref/blob_close.html). Passing any other pointer in
to this routine results in undefined and probably undesirable behavior.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


