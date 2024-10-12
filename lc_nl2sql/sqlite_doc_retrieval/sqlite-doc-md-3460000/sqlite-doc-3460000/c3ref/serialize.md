




Serialize a database




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Serialize a database




> ```
> 
> unsigned char *sqlite3_serialize(
>   sqlite3 *db,           /* The database connection */
>   const char *zSchema,   /* Which DB to serialize. ex: "main", "temp", ... */
>   sqlite3_int64 *piSize, /* Write size of the DB here, if not NULL */
>   unsigned int mFlags    /* Zero or more SQLITE_SERIALIZE_* flags */
> );
> 
> ```



The sqlite3\_serialize(D,S,P,F) interface returns a pointer to memory
that is a serialization of the S database on [database connection](../c3ref/sqlite3.html) D.
If P is not a NULL pointer, then the size of the database in bytes
is written into \*P.


For an ordinary on\-disk database file, the serialization is just a
copy of the disk file. For an in\-memory database or a "TEMP" database,
the serialization is the same sequence of bytes which would be written
to disk if that database where backed up to disk.


The usual case is that sqlite3\_serialize() copies the serialization of
the database into memory obtained from [sqlite3\_malloc64()](../c3ref/free.html) and returns
a pointer to that memory. The caller is responsible for freeing the
returned value to avoid a memory leak. However, if the F argument
contains the SQLITE\_SERIALIZE\_NOCOPY bit, then no memory allocations
are made, and the sqlite3\_serialize() function will return a pointer
to the contiguous memory representation of the database that SQLite
is currently using for that database, or NULL if the no such contiguous
memory representation of the database exists. A contiguous memory
representation of the database will usually only exist if there has
been a prior call to [sqlite3\_deserialize(D,S,...)](../c3ref/deserialize.html) with the same
values of D and S.
The size of the database is written into \*P even if the
SQLITE\_SERIALIZE\_NOCOPY bit is set but no contiguous copy
of the database exists.


After the call, if the SQLITE\_SERIALIZE\_NOCOPY bit had been set,
the returned buffer content will remain accessible and unchanged
until either the next write operation on the connection or when
the connection is closed, and applications must not modify the
buffer. If the bit had been clear, the returned buffer will not
be accessed by SQLite after the call.


A call to sqlite3\_serialize(D,S,P,F) might return NULL even if the
SQLITE\_SERIALIZE\_NOCOPY bit is omitted from argument F if a memory
allocation error occurs.


This interface is omitted if SQLite is compiled with the
[SQLITE\_OMIT\_DESERIALIZE](../compile.html#omit_deserialize) option.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


