




VACUUM




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










VACUUM


# 1\. Syntax


**[vacuum\-stmt:](syntax/vacuum-stmt.html)**
hide








VACUUM



schema\-name





INTO



filename







# 2\. Description



 The VACUUM command rebuilds the database file, repacking it into a minimal
 amount of disk space. There are several
 reasons an application might do this:



* Unless SQLite is running in "auto\_vacuum\=FULL" mode, when a large
 amount of data is deleted from the database file it leaves behind empty
 space, or "free" database pages. This means the database file might
 be larger than strictly necessary. Running VACUUM to rebuild the
 database reclaims this space and reduces the size of the database file.
* Frequent inserts, updates, and deletes can cause the database file
 to become fragmented \- where data for a single table or index is scattered
 around the database file. Running VACUUM ensures that each table and
 index is largely stored contiguously within the database file. In some
 cases, VACUUM may also reduce the number of partially filled pages in
 the database, reducing the size of the database file further.
* When content is deleted from an SQLite database, the content is not
 usually erased but rather the space used to hold the content is marked as
 being available for reuse. This can allow deleted content to be recovered
 by a hacker or by forensic analysis. Running VACUUM will clean the database
 of all traces of deleted content, thus preventing an adversary from recovering
 deleted content. Using VACUUM in this way is an alternative to setting
 [PRAGMA secure\_delete\=ON](pragma.html#pragma_secure_delete).
* Normally, the database [page\_size](pragma.html#pragma_page_size) and whether or not the database
 supports [auto\_vacuum](pragma.html#pragma_auto_vacuum) must be configured before the database file is
 actually created. However, when not in [write\-ahead log](wal.html) mode, the
 [page\_size](pragma.html#pragma_page_size) and/or [auto\_vacuum](pragma.html#pragma_auto_vacuum) properties of an existing database may be
 changed by using the [page\_size](pragma.html#pragma_page_size) and/or
 [pragma auto\_vacuum](pragma.html#pragma_auto_vacuum) pragmas and then immediately VACUUMing
 the database. When in [write\-ahead log](wal.html) mode, only the [auto\_vacuum](pragma.html#pragma_auto_vacuum)
 support property can be changed using VACUUM.


By default, VACUUM operates on the main database.
[Attached databases](lang_attach.html) can be vacuumed by appending the appropriate
schema\-name to the VACUUM statement.



**Compatibility Warning:** The ability to vacuum attached databases was
added in [version 3\.15\.0](releaselog/3_15_0.html) (2016\-10\-14\). Prior to that, a
schema\-name added to the
VACUUM statement would be silently ignored and the "main" schema would be
vacuumed.



## 2\.1\. VACUUM with an INTO clause


If the INTO clause is included, then the original database file is
unchanged and a new database is created in a file named by the
argument to the INTO clause.
The argument is a scalar [expression](lang_expr.html), such as a text literal.
The new database will contain the same
logical content as the original database, fully vacuumed.




The VACUUM command with an INTO clause is an alternative to the
[backup API](backup.html) for generating backup copies of a live database.
The advantage of using VACUUM INTO is that the resulting backup
database is minimal in size and hence the amount of filesystem
I/O may be reduced. Also, all deleted content is purged from the
backup, leaving behind no forensic traces. On the other hand,
the [backup API](backup.html) uses fewer CPU cycles and can be executed
incrementally.




The filename in the INTO clause can be an arbitrary SQL expression
that evaluates to a string.
The file named by the INTO clause must not previously exist, or
else it must be an empty file, or the VACUUM INTO command will
fail with an error.




The argument to INTO can be a [URI filename](uri.html) if URI filenames
are enabled.
URL filenames are enabled if any of the following are true:


* The SQLite library was compiled with [\-DSQLITE\_USE\_URI\=1](compile.html#use_uri).
* The [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_URI](c3ref/c_config_covering_index_scan.html#sqliteconfiguri),1\) interfaces was
 invoked at start\-time.
* The [database connection](c3ref/sqlite3.html) that is running the VACUUM INTO
 statement was originally opened using the
 [SQLITE\_OPEN\_URI](c3ref/c_open_autoproxy.html) flag.



The VACUUM INTO command is transactional in the sense that
the generated output database is a consistent snapshot of the
original database. However, if the VACUUM INTO command is
interrupted by an unplanned shutdown or power loss, then
the generated output database might be incomplete and corrupt.
Also, SQLite does not invoke fsync() or FlushFileBuffers()
on the generated database to ensure that it has reached
non\-volatile storage before completing.





# 3\. How VACUUM works


The VACUUM command works by copying the contents of the database into
a temporary database file and then overwriting the original with the
contents of the temporary file. When overwriting the original, a rollback
journal or [write\-ahead log](wal.html) WAL file is used just as it would be for any
other database transaction. This means that when VACUUMing a database,
as much as twice the size of the original database file is required in free
disk space.



The VACUUM INTO command works the same way except that it uses the file
named on the INTO clause in place of the temporary database and omits the
step of copying the vacuumed database back over top of the original database.



The VACUUM command may change the [ROWIDs](lang_createtable.html#rowid) of entries in any
tables that do not have an explicit [INTEGER PRIMARY KEY](lang_createtable.html#rowid).



A VACUUM will fail if there is an open transaction on the database
connection that is attempting to run the VACUUM. Unfinalized SQL
statements typically hold a read transaction open, so the VACUUM
might fail if there are unfinalized SQL statements on the same connection.
VACUUM (but not VACUUM INTO) is a write operation and so if another
database connection is holding a lock that prevents writes, then
the VACUUM will fail.



An alternative to using the VACUUM command to
reclaim space after data has been deleted is auto\-vacuum mode, enabled using
the [auto\_vacuum](pragma.html#pragma_auto_vacuum) pragma. When [auto\_vacuum](pragma.html#pragma_auto_vacuum) is enabled for a database
free pages may be reclaimed after deleting data, causing the file to shrink,
without rebuilding the entire database using VACUUM. However, using
[auto\_vacuum](pragma.html#pragma_auto_vacuum) can lead to extra database file fragmentation. And [auto\_vacuum](pragma.html#pragma_auto_vacuum)
does not compact partially filled pages of the database as VACUUM does.




*This page last modified on [2023\-12\-05 14:43:20](https://sqlite.org/docsrc/honeypot) UTC* 


