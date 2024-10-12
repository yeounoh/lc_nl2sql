




Temporary Files Used By SQLite




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Temporary Files Used By SQLite


►
Table Of Contents
[1\. Introduction](#introduction)
[2\. Nine Kinds Of Temporary Files](#nine_kinds_of_temporary_files)
[2\.1\. Rollback Journals](#rollback_journals)
[2\.2\. Write\-Ahead Log (WAL) Files](#write_ahead_log_wal_files)
[2\.3\. Shared\-Memory Files](#shared_memory_files)
[2\.4\. Super\-Journal Files](#super_journal_files)
[2\.5\. Statement Journal Files](#statement_journal_files)
[2\.6\. TEMP Databases](#temp_databases)
[2\.7\. Materializations Of Views And Subqueries](#materializations_of_views_and_subqueries)
[2\.8\. Transient Indices](#transient_indices)
[2\.9\. Transient Database Used By [VACUUM](lang_vacuum.html)](#transient_database_used_by_vacuum_)
[3\. The SQLITE\_TEMP\_STORE Compile\-Time Parameter and Pragma](#the_sqlite_temp_store_compile_time_parameter_and_pragma)
[4\. Other Temporary File Optimizations](#other_temporary_file_optimizations)
[5\. Temporary File Storage Locations](#temporary_file_storage_locations)




# 1\. Introduction



One of the [distinctive features](different.html) of
SQLite is that a database consists of a single disk file.
This simplifies the use of SQLite since moving or backing up a
database is a simple as copying a single file. It also makes
SQLite appropriate for use as an
[application file format](whentouse.html#appfileformat).
But while a complete database is held in a single disk file,
SQLite does make use of many temporary files during the
course of processing a database.




This article describes the various temporary files that SQLite
creates and uses. It describes when the files are created, when
they are deleted, what they are used for, why they are important,
and how to avoid them on systems where creating temporary files is
expensive.




The manner in which SQLite uses temporary files is not considered
part of the contract that SQLite makes with applications. The
information in this document is a correct description of how
SQLite operates at the time that this document was written or last
updated. But there is no guarantee that future versions of SQLite
will use temporary files in the same way. New kinds of temporary
files might be employed and some of
the current temporary file uses might be discontinued
in future releases of SQLite.




# 2\. Nine Kinds Of Temporary Files



SQLite currently uses nine distinct types of temporary files:



1. Rollback journals
2. Super\-journals
3. Write\-ahead Log (WAL) files
4. Shared\-memory files
5. Statement journals
6. TEMP databases
7. Materializations of views and subqueries
8. Transient indices
9. Transient databases used by VACUUM



Additional information about each of these temporary file types
is in the sequel.




## 2\.1\. Rollback Journals



A rollback journal is a temporary file used to implement
atomic commit and rollback capabilities in SQLite.
(For a detailed discussion of how this works, see
the separate document titled
[Atomic Commit In SQLite](atomiccommit.html).)
The rollback journal is always located in the same directory
as the database file and has the same name as the database
file except with the 8 characters "**\-journal**" appended.
The rollback journal is usually created when a transaction
is first started and is usually deleted when a transaction
commits or rolls back.
The rollback journal file is essential for implementing the
atomic commit and rollback capabilities of SQLite. Without
a rollback journal, SQLite would be unable to rollback an
incomplete transaction, and if a crash or power loss occurred
in the middle of a transaction the entire database would likely
go corrupt without a rollback journal.




The rollback journal is *usually* created and destroyed at the
start and end of a transaction, respectively. But there are exceptions
to this rule.




If a crash or power loss occurs in the middle of a transaction,
then the rollback journal file is left on disk. The next time
another application attempts to open the database file, it notices
the presence of the abandoned rollback journal (we call it a "hot
journal" in this circumstance) and uses the information in the
journal to restore the database to its state prior to the start
of the incomplete transaction. This is how SQLite implements
atomic commit.




If an application puts SQLite in 
[exclusive locking mode](pragma.html#pragma_locking_mode) using
the pragma:




> ```
> 
> PRAGMA locking_mode=EXCLUSIVE;
> 
> ```



SQLite creates a new rollback journal at the start of the first
transaction within an exclusive locking mode session. But at the
conclusion of the transaction, it does not delete the rollback
journal. The rollback journal might be truncated, or its header
might be zeroed (depending on what version of SQLite you are using)
but the rollback journal is not deleted. The rollback journal is
not deleted until exclusive access mode is exited.



Rollback journal creation and deletion is also changed by the
[journal\_mode pragma](pragma.html#pragma_journal_mode).
The default journaling mode is DELETE, which is the default behavior
of deleting the rollback journal file at the end of each transaction,
as described above. The PERSIST journal mode foregoes the deletion of
the journal file and instead overwrites the rollback journal header
with zeros, which prevents other processes from rolling back the
journal and thus has the same effect as deleting the journal file, though
without the expense of actually removing the file from disk. In other
words, journal mode PERSIST exhibits the same behavior as is seen
in EXCLUSIVE locking mode. The
OFF journal mode causes SQLite to omit the rollback journal, completely.
In other words, no rollback journal is ever written if journal mode is
set to OFF.
The OFF journal mode disables the atomic
commit and rollback capabilities of SQLite. The ROLLBACK command
is not available when OFF journal mode is set. And if a crash or power
loss occurs in the middle of a transaction that uses the OFF journal
mode, no recovery is possible and the database file will likely
go corrupt.
The MEMORY journal mode causes the rollback journal to be stored in
memory rather than on disk. The ROLLBACK command still works when
the journal mode is MEMORY, but because no file exists on disks for
recovery, a crash or power loss in the middle of a transaction that uses
the MEMORY journal mode will likely result in a corrupt database.




## 2\.2\. Write\-Ahead Log (WAL) Files



A write\-ahead log or WAL file is used in place of a rollback journal
when SQLite is operating in [WAL mode](wal.html). As with the rollback journal,
the purpose of the WAL file is to implement atomic commit and rollback.
The WAL file is always located in the same directory
as the database file and has the same name as the database
file except with the 4 characters "**\-wal**" appended.
The WAL file is created when the first connection to the
database is opened and is normally removed when the last
connection to the database closes. However, if the last connection
does not shutdown cleanly, the WAL file will remain in the filesystem
and will be automatically cleaned up the next time the database is
opened.




## 2\.3\. Shared\-Memory Files



When operating in [WAL mode](wal.html), all SQLite database connections associated
with the same database file need to share some memory that is used as an
index for the WAL file. In most implementations, this shared memory is
implemented by calling mmap() on a file created for this sole purpose:
the shared\-memory file. The shared\-memory file, if it exists, is located
in the same directory as the database file and has the same name as the
database file except with the 4 characters "**\-shm**" appended.
Shared memory files only exist while running in WAL mode.




The shared\-memory file contains no persistent content. The only purpose
of the shared\-memory file is to provide a block of shared memory for use
by multiple processes all accessing the same database in WAL mode.
If the [VFS](vfs.html) is able to provide an alternative method for accessing shared
memory, then that alternative method might be used rather than the
shared\-memory file. For example, if [PRAGMA locking\_mode](pragma.html#pragma_locking_mode) is set to
EXCLUSIVE (meaning that only one process is able to access the database
file) then the shared memory will be allocated from heap rather than out
of the shared\-memory file, and the shared\-memory file will never be
created.




The shared\-memory file has the same lifetime as its associated WAL file.
The shared\-memory file is created when the WAL file is created and is
deleted when the WAL file is deleted. During WAL file recovery, the
shared memory file is recreated from scratch based on the contents of
the WAL file being recovered.




## 2\.4\. Super\-Journal Files



The super\-journal file is used as part of the atomic commit
process when a single transaction makes changes to multiple
databases that have been added to a single [database connection](c3ref/sqlite3.html)
using the [ATTACH](lang_attach.html) statement. The super\-journal file is always
located in the same directory as the main database file
(the main database file is the database that is identified
in the original [sqlite3\_open()](c3ref/open.html), [sqlite3\_open16()](c3ref/open.html), or
[sqlite3\_open\_v2()](c3ref/open.html) call that created the [database connection](c3ref/sqlite3.html))
with a randomized suffix. The super\-journal file contains
the names of all of the various attached auxiliary databases
that were changed during the transaction. The multi\-database
transaction commits when the super\-journal file is deleted.
See the documentation titled
[Atomic Commit In SQLite](atomiccommit.html) for
additional detail.




Without the super\-journal, the transaction commit on a multi\-database
transaction would be atomic for each database individually, but it
would not be atomic across all databases. In other words, if the
commit were interrupted in the middle by a crash or power loss, then
the changes to one of the databases might complete while the changes
to another database might roll back. The super\-journal causes all
changes in all databases to either rollback or commit together.




The super\-journal file is only created for [COMMIT](lang_transaction.html) operations that
involve multiple database files where at least two of the databases 
meet all of the following requirements:



1. The database is modified by the transaction
2. The [PRAGMA synchronous](pragma.html#pragma_synchronous) setting is not OFF
3. The [PRAGMA journal\_mode](pragma.html#pragma_journal_mode) is not OFF, MEMORY, or WAL



This means that SQLite transactions are not atomic
across multiple database files on a power\-loss when the database 
files have synchronous turned off or when they are using journal 
modes of OFF, MEMORY, or WAL. For synchronous OFF and for
journal\_modes OFF and MEMORY, database will usually corrupt if
a transaction commit is interrupted by a power loss. For 
[WAL mode](wal.html), individual database files are updated atomically
across a power\-loss, but in the case of a multi\-file transactions,
some files might rollback while others roll forward after
power is restored.




## 2\.5\. Statement Journal Files



A statement journal file is used to rollback partial results of
a single statement within a larger transaction. For example, suppose
an UPDATE statement will attempt to modify 100 rows in the database.
But after modifying the first 50 rows, the UPDATE hits
a constraint violation which should block the entire statement.
The statement journal is used to undo the first 50 row changes
so that the database is restored to the state it was in at the start
of the statement.




A statement journal is only created for an UPDATE or INSERT statement
that might change multiple rows of a database and which might hit a
constraint or a RAISE exception within a trigger and thus need to
undo partial results.
If the UPDATE or INSERT is not contained within BEGIN...COMMIT and if
there are no other active statements on the same database connection then
no statement journal is created since the ordinary
rollback journal can be used instead.
The statement journal is also omitted if an alternative
[conflict resolution algorithm](lang_conflict.html) is
used. For example:




> ```
> 
> UPDATE OR FAIL ...
> UPDATE OR IGNORE ...
> UPDATE OR REPLACE ...
> UPDATE OR ROLLBACK ...
> INSERT OR FAIL ...
> INSERT OR IGNORE ...
> INSERT OR REPLACE ...
> INSERT OR ROLLBACK ...
> REPLACE INTO ....
> 
> ```



The statement journal is given a randomized name, not necessarily
in the same directory as the main database, and is automatically
deleted at the conclusion of the transaction. The size of the
statement journal is proportional to the size of the change implemented
by the UPDATE or INSERT statement that caused the statement journal
to be created.




## 2\.6\. TEMP Databases


Tables created using the "CREATE TEMP TABLE" syntax are only
visible to the [database connection](c3ref/sqlite3.html) in which the "CREATE TEMP TABLE"
statement is originally evaluated. These TEMP tables, together
with any associated indices, triggers, and views, are collectively
stored in a separate temporary database file that is created as
soon as the first "CREATE TEMP TABLE" statement is seen.
This separate temporary database file also has an associated
rollback journal.
The temporary database file used to store TEMP tables is deleted
automatically when the [database connection](c3ref/sqlite3.html) is closed
using [sqlite3\_close()](c3ref/close.html).




The TEMP database file is very similar to auxiliary database
files added using the [ATTACH](lang_attach.html) statement, though with a few
special properties.
The TEMP database is always automatically deleted when the
[database connection](c3ref/sqlite3.html) is closed.
The TEMP database always uses the
[synchronous\=OFF](pragma.html#pragma_synchronous) and [journal\_mode\=PERSIST](pragma.html#pragma_journal_mode)
PRAGMA settings.
And, the TEMP database cannot be used with [DETACH](lang_detach.html) nor can
another process [ATTACH](lang_attach.html) the TEMP database.




The temporary files associated with the TEMP database and its
rollback journal are only created if the application makes use
of the "CREATE TEMP TABLE" statement.




## 2\.7\. Materializations Of Views And Subqueries


Queries that contain subqueries must sometime evaluate
the subqueries separately and store the results in a temporary
table, then use the content of the temporary table to evaluate
the outer query.
We call this "materializing" the subquery.
The query optimizer in SQLite attempts to avoid materializing,
but sometimes it is not easily avoidable.
The temporary tables created by materialization are each stored
in their own separate temporary file, which is automatically
deleted at the conclusion of the query.
The size of these temporary tables depends on the amount of
data in the materialization of the subquery, of course.




A subquery on the right\-hand side of IN operator must often
be materialized. For example:




> ```
> 
> SELECT * FROM ex1 WHERE ex1.a IN (SELECT b FROM ex2);
> 
> ```



In the query above, the subquery "SELECT b FROM ex2" is evaluated
and its results are stored in a temporary table (actually a temporary
index) that allows one to determine whether or not a value ex2\.b
exists using a simple binary search. Once this table is constructed,
the outer query is run and for each prospective result row a check
is made to see if ex1\.a is contained within the temporary table.
The row is output only if the check is true.




To avoid creating the temporary table, the query might be rewritten
as follows:




> ```
> 
> SELECT * FROM ex1 WHERE EXISTS(SELECT 1 FROM ex2 WHERE ex2.b=ex1.a);
> 
> ```



Recent versions of SQLite ([version 3\.5\.4](releaselog/3_5_4.html) 2007\-12\-14\) and later)
will do this rewrite automatically
if an index exists on the column ex2\.b.




If the right\-hand side of an IN operator can be list of values
as in the following:




> ```
> 
> SELECT * FROM ex1 WHERE a IN (1,2,3);
> 
> ```



List values on the right\-hand side of IN are treated as a 
subquery that must be materialized. In other words, the
previous statement acts as if it were:




> ```
> 
> SELECT * FROM ex1 WHERE a IN (SELECT 1 UNION ALL
>                               SELECT 2 UNION ALL
>                               SELECT 3);
> 
> ```



A temporary index is always used to hold the values of the
right\-hand side of an IN operator when that right\-hand side
is a list of values.




Subqueries might also need to be materialized when they appear
in the FROM clause of a SELECT statement. For example:




> ```
> 
> SELECT * FROM ex1 JOIN (SELECT b FROM ex2) AS t ON t.b=ex1.a;
> 
> ```



Depending on the query, SQLite might need to materialize the 
"(SELECT b FROM ex2\)" subquery into a temporary table, then
perform the join between ex1 and the temporary table. The
query optimizer tries to avoid this by "flattening" the
query. In the previous example the query can be flattened,
and SQLite will automatically transform the query into




> ```
> 
> SELECT ex1.*, ex2.b FROM ex1 JOIN ex2 ON ex2.b=ex1.a;
> 
> ```



More complex queries may or may not be able to employ query
flattening to avoid the temporary table. Whether or not
the query can be flattened depends on such factors as whether
or not the subquery or outer query contain aggregate functions,
ORDER BY or GROUP BY clauses, LIMIT clauses, and so forth.
The rules for when a query can and cannot be flattened are
very complex and are beyond the scope of this document.




## 2\.8\. Transient Indices



SQLite may make use of transient indices to
implement SQL language features such as:



* An ORDER BY or GROUP BY clause
* The DISTINCT keyword in an aggregate query
* Compound SELECT statements joined by UNION, EXCEPT, or INTERSECT



Each transient index is stored in its own temporary file.
The temporary file for a transient index is automatically deleted
at the end of the statement that uses it.




SQLite strives to implement ORDER BY clauses using a preexisting
index. If an appropriate index already exists, SQLite will walk
the index, rather than the underlying table, to extract the 
requested information, and thus cause the rows to come out in
the desired order. But if SQLite cannot find an appropriate index
it will evaluate the query and store each row in a transient index
whose data is the row data and whose key is the ORDER BY terms.
After the query is evaluated, SQLite goes back and walks the
transient index from beginning to end in order to output the
rows in the desired order.




SQLite implements GROUP BY by ordering the output rows in the
order suggested by the GROUP BY terms. Each output row is
compared to the previous to see if it starts a new "group".
The ordering by GROUP BY terms is done in exactly the same way
as the ordering by ORDER BY terms. A preexisting index is used
if possible, but if no suitable index is available, a transient
index is created.




The DISTINCT keyword on an aggregate query is implemented by
creating a transient index in a temporary file and storing
each result row in that index. As new result rows are computed
a check is made to see if they already exist in the transient
index and if they do the new result row is discarded.




The UNION operator for compound queries is implemented by creating
a transient index in a temporary file and storing the results
of the left and right subquery in the transient index, discarding
duplicates. After both subqueries have been evaluated, the
transient index is walked from beginning to end to generate the final output.




The EXCEPT operator for compound queries is implemented by creating
a transient index in a temporary file, storing the results of the
left subquery in this transient index, then removing the result 
from right subquery from the transient index, and finally walking
the index from beginning to end to obtain the final output.




The INTERSECT operator for compound queries is implemented by
creating two separate transient indices, each in a separate
temporary file. The left and right subqueries are evaluated
each into a separate transient index. Then the two indices
are walked together and entries that appear in both indices
are output.




Note that the UNION ALL operator for compound queries does not
use transient indices by itself (though of course the right
and left subqueries of the UNION ALL might use transient indices
depending on how they are composed.)




## 2\.9\. Transient Database Used By [VACUUM](lang_vacuum.html)



The [VACUUM](lang_vacuum.html) command works by creating a temporary file
and then rebuilding the entire database into that temporary
file. Then the content of the temporary file is copied back
into the original database file and the temporary file is
deleted.




The temporary file created by the [VACUUM](lang_vacuum.html) command exists only
for the duration of the command itself. The size of the temporary
file will be no larger than the original database.




# 3\. The SQLITE\_TEMP\_STORE Compile\-Time Parameter and Pragma



The temporary files associated with transaction control, namely
the rollback journal, super\-journal, write\-ahead log (WAL) files,
and shared\-memory files, are always written to disk.
But the other kinds of temporary files might be stored in memory
only and never written to disk.
Whether or not temporary files other than the rollback,
super, and statement journals are written to disk or stored only in memory
depends on the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter, the
[temp\_store pragma](pragma.html#pragma_temp_store),
and on the size of the temporary file.




The [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter is a \#define whose value is
an integer between 0 and 3, inclusive. The meaning of the
[SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter is as follows:



1. Temporary files are always stored on disk regardless of the setting
of the [temp\_store pragma](pragma.html#pragma_temp_store).
2. Temporary files are stored on disk by default but this can be
overridden by the [temp\_store pragma](pragma.html#pragma_temp_store).
3. Temporary files are stored in memory by default but this can be
overridden by the [temp\_store pragma](pragma.html#pragma_temp_store).
4. Temporary files are always stored in memory regardless of the setting
of the [temp\_store pragma](pragma.html#pragma_temp_store).



The default value of the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter is 1,
which means to store temporary files on disk but provide the option
of overriding the behavior using the [temp\_store pragma](pragma.html#pragma_temp_store).




The [temp\_store pragma](pragma.html#pragma_temp_store) has
an integer value which also influences the decision of where to store
temporary files. The values of the temp\_store pragma have the
following meanings:



1. Use either disk or memory storage for temporary files as determined
by the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter.
2. If the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter specifies memory storage for
temporary files, then override that decision and use disk storage instead.
Otherwise follow the recommendation of the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time
parameter.
3. If the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter specifies disk storage for
temporary files, then override that decision and use memory storage instead.
Otherwise follow the recommendation of the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time
parameter.



The default setting for the [temp\_store pragma](pragma.html#pragma_temp_store) is 0,
which means to following the recommendation of [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time
parameter.




To reiterate, the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter and the 
[temp\_store pragma](pragma.html#pragma_temp_store) only
influence the temporary files other than the rollback journal
and the super\-journal. The rollback journal and the
super\-journal are always written to disk regardless of the settings of
the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter and the
[temp\_store pragma](pragma.html#pragma_temp_store).




# 4\. Other Temporary File Optimizations



SQLite uses a page cache of recently read and written database
pages. This page cache is used not just for the main database
file but also for transient indices and tables stored in temporary
files. If SQLite needs to use a temporary index or table and
the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter and the
[temp\_store pragma](pragma.html#pragma_temp_store) are
set to store temporary tables and index on disk, the information
is still initially stored in memory in the page cache. The 
temporary file is not opened and the information is not truly
written to disk until the page cache is full.




This means that for many common cases where the temporary tables
and indices are small (small enough to fit into the page cache)
no temporary files are created and no disk I/O occurs. Only
when the temporary data becomes too large to fit in RAM does
the information spill to disk.




Each temporary table and index is given its own page cache
which can store a maximum number of database pages determined
by the SQLITE\_DEFAULT\_TEMP\_CACHE\_SIZE compile\-time parameter.
(The default value is 500 pages.)
The maximum number of database pages in the page cache is the
same for every temporary table and index. The value cannot
be changed at run\-time or on a per\-table or per\-index basis.
Each temporary file gets its own private page cache with its
own SQLITE\_DEFAULT\_TEMP\_CACHE\_SIZE page limit.




# 5\. Temporary File Storage Locations



The directory or folder in which temporary files are created is
determined by the OS\-specific [VFS](vfs.html).




On unix\-like systems, directories are searched in the following order:


1. The directory set by [PRAGMA temp\_store\_directory](pragma.html#pragma_temp_store_directory) or by the
 [sqlite3\_temp\_directory](c3ref/temp_directory.html) global variable
2. The SQLITE\_TMPDIR environment variable
3. The TMPDIR environment variable
4. /var/tmp
5. /usr/tmp
6. /tmp
7. The current working directory (".")


The first of the above that is found to exist and have the write and
execute bits set is used. The final "." fallback is important for some
applications that use SQLite inside of chroot jails that do not have
the standard temporary file locations available.


On Windows systems, folders are searched in the following order:


1. The folder set by [PRAGMA temp\_store\_directory](pragma.html#pragma_temp_store_directory) or by the
 [sqlite3\_temp\_directory](c3ref/temp_directory.html) global variable
2. The folder returned by the GetTempPath() system interface.


SQLite itself does not pay any attention to environment variables
in this case, though presumably the GetTempPath() system call does.
The search algorithm is different for CYGWIN builds. Check the 
source code for details.
*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


