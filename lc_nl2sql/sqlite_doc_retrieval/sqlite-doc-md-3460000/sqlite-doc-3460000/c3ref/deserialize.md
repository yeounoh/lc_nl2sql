




Deserialize a database




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Deserialize a database




> ```
> 
> int sqlite3_deserialize(
>   sqlite3 *db,            /* The database connection */
>   const char *zSchema,    /* Which DB to reopen with the deserialization */
>   unsigned char *pData,   /* The serialized database content */
>   sqlite3_int64 szDb,     /* Number bytes in the deserialization */
>   sqlite3_int64 szBuf,    /* Total size of buffer pData[] */
>   unsigned mFlags         /* Zero or more SQLITE_DESERIALIZE_* flags */
> );
> 
> ```



The sqlite3\_deserialize(D,S,P,N,M,F) interface causes the
[database connection](../c3ref/sqlite3.html) D to disconnect from database S and then
reopen S as an in\-memory database based on the serialization contained
in P. The serialized database P is N bytes in size. M is the size of
the buffer P, which might be larger than N. If M is larger than N, and
the SQLITE\_DESERIALIZE\_READONLY bit is not set in F, then SQLite is
permitted to add content to the in\-memory database as long as the total
size does not exceed M bytes.


If the SQLITE\_DESERIALIZE\_FREEONCLOSE bit is set in F, then SQLite will
invoke sqlite3\_free() on the serialization buffer when the database
connection closes. If the SQLITE\_DESERIALIZE\_RESIZEABLE bit is set, then
SQLite will try to increase the buffer size using sqlite3\_realloc64()
if writes on the database cause it to grow larger than M bytes.


Applications must not modify the buffer P or invalidate it before
the database connection D is closed.


The sqlite3\_deserialize() interface will fail with SQLITE\_BUSY if the
database is currently in a read transaction or is involved in a backup
operation.


It is not possible to deserialized into the TEMP database. If the
S argument to sqlite3\_deserialize(D,S,P,N,M,F) is "temp" then the
function returns SQLITE\_ERROR.


The deserialized database should not be in [WAL mode](../wal.html). If the database
is in WAL mode, then any attempt to use the database file will result
in an [SQLITE\_CANTOPEN](../rescode.html#cantopen) error. The application can set the
[file format version numbers](../fileformat2.html#vnums) (bytes 18 and 19\) of the input database P
to 0x01 prior to invoking sqlite3\_deserialize(D,S,P,N,M,F) to force the
database file into rollback mode and work around this limitation.


If sqlite3\_deserialize(D,S,P,N,M,F) fails for any reason and if the
SQLITE\_DESERIALIZE\_FREEONCLOSE bit is set in argument F, then
[sqlite3\_free()](../c3ref/free.html) is invoked on argument P prior to returning.


This interface is omitted if SQLite is compiled with the
[SQLITE\_OMIT\_DESERIALIZE](../compile.html#omit_deserialize) option.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


