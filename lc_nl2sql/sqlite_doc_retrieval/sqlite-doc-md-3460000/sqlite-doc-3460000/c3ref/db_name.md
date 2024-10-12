




Return The Schema Name For A Database Connection




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Return The Schema Name For A Database Connection




> ```
> 
> const char *sqlite3_db_name(sqlite3 *db, int N);
> 
> ```



The sqlite3\_db\_name(D,N) interface returns a pointer to the schema name
for the N\-th database on database connection D, or a NULL pointer of N is
out of range. An N value of 0 means the main database file. An N of 1 is
the "temp" schema. Larger values of N correspond to various ATTACH\-ed
databases.


Space to hold the string that is returned by sqlite3\_db\_name() is managed
by SQLite itself. The string might be deallocated by any operation that
changes the schema, including [ATTACH](../lang_attach.html) or [DETACH](../lang_detach.html) or calls to
[sqlite3\_serialize()](../c3ref/serialize.html) or [sqlite3\_deserialize()](../c3ref/deserialize.html), even operations that
occur on a different thread. Applications that need to
remember the string long\-term should make their own copy. Applications that
are accessing the same database connection simultaneously on multiple
threads should mutex\-protect calls to this API and should make their own
private copy of the result prior to releasing the mutex.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


