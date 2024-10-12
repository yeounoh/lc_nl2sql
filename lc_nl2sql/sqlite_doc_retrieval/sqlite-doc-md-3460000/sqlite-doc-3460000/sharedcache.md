




SQLite Shared\-Cache Mode




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










SQLite Shared\-Cache Mode


►
Table Of Contents
[1\. SQLite Shared\-Cache Mode](#sqlite_shared_cache_mode)
[1\.1\. Use of shared\-cache is discouraged](#use_of_shared_cache_is_discouraged)
[2\. Shared\-Cache Locking Model](#shared_cache_locking_model)
[2\.1\. Transaction Level Locking](#transaction_level_locking)
[2\.2\. Table Level Locking](#table_level_locking)
[2\.2\.1\. Read\-Uncommitted Isolation Mode](#read_uncommitted_isolation_mode)
[2\.3\. Schema (sqlite\_schema) Level Locking](#schema_sqlite_schema_level_locking)
[3\. Thread Related Issues](#thread_related_issues)
[4\. Shared Cache And Virtual Tables](#shared_cache_and_virtual_tables)
[5\. Enabling Shared\-Cache Mode](#enabling_shared_cache_mode)
[6\. Shared Cache And In\-Memory Databases](#shared_cache_and_in_memory_databases)





# 1\. SQLite Shared\-Cache Mode


Starting with [version 3\.3\.0](releaselog/3_3_0.html) (2006\-01\-11\),
SQLite includes a special "shared\-cache"
mode (disabled by default) intended for use in embedded servers. If
shared\-cache mode is enabled and a thread establishes multiple connections
to the same database, the connections share a single data and schema cache.
This can significantly reduce the quantity of memory and IO required by
the system.


In [version 3\.5\.0](releaselog/3_5_0.html) (2007\-09\-04\),
shared\-cache mode was modified so that the same
cache can be shared across an entire process rather than just within
a single thread. Prior to this change, there were restrictions on
passing database connections between threads. Those restrictions were
dropped in 3\.5\.0 update. This document describes shared\-cache mode
as of version 3\.5\.0\.


Shared\-cache mode changes the semantics
of the locking model in some cases. The details are described by
this document. A basic understanding of the normal SQLite locking model (see
[File Locking And Concurrency In SQLite Version 3](lockingv3.html)
for details) is assumed.



## 1\.1\. Use of shared\-cache is discouraged


Shared\-cache mode is an obsolete feature. The use of shared\-cache mode
is discouraged. Most use cases for shared\-cache are better served by
[WAL mode](wal.html).



Shared\-cache mode was invented in 2006 at the request of developers
of [Symbian](https://en.wikipedia.org/wiki/Symbian). Their problem was that
if the contacts database on the phone was being synced, that would lock the
database file. Then if a call came in, the database lock would prevent them
from querying the contacts database in order to find the appropriate
ring\-tone for the incoming call, or a photo of the caller to show on screen,
and so forth.
[WAL mode](wal.html) (circa 2010\) is a better solution to this problem as it permits
simultaneous access without breaking transaction isolation.



Applications that build their own copy of SQLite from source code
are encouraged to use the [\-DSQLITE\_OMIT\_SHARED\_CACHE](compile.html#omit_shared_cache) compile\-time option,
as the resulting binary will be both smaller and faster.



The shared\-cache interfaces described here will continue to be supported
in SQLite, to insure full backwards compatibility. However, the use of
shared\-cache is discouraged.



# 2\. Shared\-Cache Locking Model


Externally, from the point of view of another process or thread, two
or more [database connections](c3ref/sqlite3.html) using a shared\-cache appear as a single
connection. The locking protocol used to arbitrate between multiple
shared\-caches or regular database users is described elsewhere.





|  |
| --- |


Figure 1


Figure 1 depicts an example runtime configuration where three
database connections have been established. Connection 1 is a normal
SQLite database connection. Connections 2 and 3 share a cache
The normal locking
protocol is used to serialize database access between connection 1 and
the shared cache. The internal protocol used to serialize (or not, see
"Read\-Uncommitted Isolation Mode" below) access to the shared\-cache by
connections 2 and 3 is described in the remainder of this section.



There are three levels to the shared\-cache locking model,
transaction level locking, table level locking and schema level locking.
They are described in the following three sub\-sections.


## 2\.1\. Transaction Level Locking


SQLite connections can open two kinds of transactions, read and write
transactions. This is not done explicitly, a transaction is implicitly a
read\-transaction until it first writes to a database table, at which point
it becomes a write\-transaction.



At most one connection to a single shared cache may open a
write transaction at any one time. This may co\-exist with any number of read
transactions.



## 2\.2\. Table Level Locking


When two or more connections use a shared\-cache, locks are used to
serialize concurrent access attempts on a per\-table basis. Tables support
two types of locks, "read\-locks" and "write\-locks". Locks are granted to
connections \- at any one time, each database connection has either a
read\-lock, write\-lock or no lock on each database table.



At any one time, a single table may have any number of active read\-locks
or a single active write lock. To read data from a table, a connection must
first obtain a read\-lock. To write to a table, a connection must obtain a
write\-lock on that table. If a required table lock cannot be obtained,
the query fails and SQLITE\_LOCKED is returned to the caller.



Once a connection obtains a table lock, it is not released until the
current transaction (read or write) is concluded.



### 2\.2\.1\. Read\-Uncommitted Isolation Mode


The behaviour described above may be modified slightly by using the
[read\_uncommitted](pragma.html#pragma_read_uncommitted) pragma to change the isolation level from serialized
(the default), to read\-uncommitted.


 A database connection in read\-uncommitted mode does not attempt
to obtain read\-locks before reading from database tables as described
above. This can lead to inconsistent query results if another database
connection modifies a table while it is being read, but it also means that
a read\-transaction opened by a connection in read\-uncommitted mode can
neither block nor be blocked by any other connection.


Read\-uncommitted mode has no effect on the locks required to write to
database tables (i.e. read\-uncommitted connections must still obtain
write\-locks and hence database writes may still block or be blocked).
Also, read\-uncommitted mode has no effect on the [sqlite\_schema](schematab.html)
locks required by the rules enumerated below (see section
"Schema (sqlite\_schema) Level Locking").




> ```
> 
>   /* Set the value of the read-uncommitted flag:
>   **
>   **   True  -> Set the connection to read-uncommitted mode.
>   **   False -> Set the connection to serialized (the default) mode.
>   */
>   PRAGMA read_uncommitted = <boolean>;
> 
>   /* Retrieve the current value of the read-uncommitted flag */
>   PRAGMA read_uncommitted;
> 
> ```


## 2\.3\. Schema (sqlite\_schema) Level Locking


The [sqlite\_schema table](schematab.html) supports shared\-cache read and write
locks in the same way as all other database tables (see description
above). The following special rules also apply:



* A connection must obtain a read\-lock on *sqlite\_schema* before
accessing any database tables or obtaining any other read or write locks.
* Before executing a statement that modifies the database schema (i.e.
a CREATE or DROP TABLE statement), a connection must obtain a write\-lock on
*sqlite\_schema*.
* A connection may not compile an SQL statement if any other connection
is holding a write\-lock on the *sqlite\_schema* table of any attached
database (including the default database, "main").


# 3\. Thread Related Issues


In SQLite versions 3\.3\.0 through 3\.4\.2 when shared\-cache mode is enabled,
a database connection may only be
used by the thread that called [sqlite3\_open()](c3ref/open.html) to create it.
And a connection could only share cache with another connection in the
same thread.
These restrictions were dropped beginning with SQLite
[version 3\.5\.0](releaselog/3_5_0.html) (2007\-09\-04\).



# 4\. Shared Cache And Virtual Tables



In older versions of SQLite,
shared cache mode could not be used together with virtual tables.
This restriction was removed in SQLite [version 3\.6\.17](releaselog/3_6_17.html) (2009\-08\-10\).



# 5\. Enabling Shared\-Cache Mode


Shared\-cache mode is enabled on a per\-process basis. Using the C
interface, the following API can be used to globally enable or disable
shared\-cache mode:




> ```
> 
> int sqlite3_enable_shared_cache(int);
> 
> ```


Each call to [sqlite3\_enable\_shared\_cache()](c3ref/enable_shared_cache.html) affects subsequent database
connections created using [sqlite3\_open()](c3ref/open.html), [sqlite3\_open16()](c3ref/open.html), or
[sqlite3\_open\_v2()](c3ref/open.html). Database connections that already exist are
unaffected. Each call to [sqlite3\_enable\_shared\_cache()](c3ref/enable_shared_cache.html) overrides
all previous calls within the same process.



Individual database connections created using [sqlite3\_open\_v2()](c3ref/open.html) can
choose to participate or not participate in shared cache mode by using
the [SQLITE\_OPEN\_SHAREDCACHE](c3ref/c_open_autoproxy.html) or [SQLITE\_OPEN\_PRIVATECACHE](c3ref/c_open_autoproxy.html) flags the
third parameter. The use of either of these flags overrides the
global shared cache mode setting established by [sqlite3\_enable\_shared\_cache()](c3ref/enable_shared_cache.html).
No more than one of the flags should be used; if both SQLITE\_OPEN\_SHAREDCACHE
and SQLITE\_OPEN\_PRIVATECACHE flags are used in the third argument to
[sqlite3\_open\_v2()](c3ref/open.html) then the behavior is undefined.


When [URI filenames](uri.html) are used, the "cache" query parameter can be used
to specify whether or not the database will use shared cache. Use
"cache\=shared" to enable shared cache and "cache\=private" to disable
shared cache. The ability to use URI query parameters to specify the
cache sharing behavior of a database connection allows cache sharing to
be controlled in [ATTACH](lang_attach.html) statements. For example:



> ```
> 
> ATTACH 'file:aux.db?cache=shared' AS aux;
> 
> ```



# 6\. Shared Cache And In\-Memory Databases



Beginning with SQLite [version 3\.7\.13](releaselog/3_7_13.html) (2012\-06\-11\),
shared cache can be used on
[in\-memory databases](inmemorydb.html), provided that the database is created using
a [URI filename](uri.html). For backwards compatibility, shared cache is always
disabled for in\-memory
databases if the unadorned name ":memory:" is used to open the database.
Prior to version 3\.7\.13, shared cache was always
disabled for in\-memory databases regardless of the database name used,
current system shared cache setting, or query parameters or flags.




Enabling shared\-cache for an in\-memory database allows two or more
database connections in the same process to have access to the same
in\-memory database. An in\-memory database in shared cache is automatically
deleted and memory is reclaimed when the last connection to that database
closes.



*This page last modified on [2023\-01\-02 14:22:42](https://sqlite.org/docsrc/honeypot) UTC* 


