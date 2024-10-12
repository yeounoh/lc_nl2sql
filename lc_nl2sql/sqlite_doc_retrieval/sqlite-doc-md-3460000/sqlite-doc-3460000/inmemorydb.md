




In\-Memory Databases




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# In\-Memory Databases


An SQLite database is normally stored in a single ordinary disk
file. However, in certain circumstances, the database might be stored in
memory.


The most common way to force an SQLite database to exist purely 
in memory is to open the database using the special filename
"**:memory:**". In other words, instead of passing the name of
a real disk file into one of the [sqlite3\_open()](c3ref/open.html), [sqlite3\_open16()](c3ref/open.html), or
[sqlite3\_open\_v2()](c3ref/open.html) functions, pass in the string ":memory:". For
example:



> ```
> 
> rc = sqlite3_open(":memory:", &db);
> 
> ```


When this is done, no disk file is opened. 
Instead, a new database is created
purely in memory. The database ceases to exist as soon as the database
connection is closed. Every :memory: database is distinct from every
other. So, opening two database connections each with the filename
":memory:" will create two independent in\-memory databases.


The special filename ":memory:" can be used anywhere that a database
filename is permitted. For example, it can be used as the
*filename* in an [ATTACH](lang_attach.html) command:



> ```
> 
> ATTACH DATABASE ':memory:' AS aux1;
> 
> ```


Note that in order for the special ":memory:" name to apply and to
create a pure in\-memory database, there must be no additional text in the
filename. Thus, a disk\-based database can be created in a file by prepending
a pathname, like this: "./:memory:".


The special ":memory:" filename also works when using [URI filenames](uri.html).
For example:


> ```
> 
> rc = sqlite3_open("file::memory:", &db);
> 
> ```



Or,


> ```
> 
> ATTACH DATABASE 'file::memory:' AS aux1;
> 
> ```



## In\-memory Databases And Shared Cache


In\-memory databases are allowed to use [shared cache](sharedcache.html) if they are
opened using a [URI filename](uri.html). If the unadorned ":memory:" name is used
to specify the in\-memory database, then that database always has a private
cache and is only visible to the database connection that originally
opened it. However, the same in\-memory database can be opened by two or
more database connections as follows:


> ```
> 
> rc = sqlite3_open("file::memory:?cache=shared", &db);
> 
> ```



Or,


> ```
> 
> ATTACH DATABASE 'file::memory:?cache=shared' AS aux1;
> 
> ```


This allows separate database connections to share the same
in\-memory database. Of course, all database connections sharing the
in\-memory database need to be in the same process. The database is
automatically deleted and memory is reclaimed when the last connection
to the database closes.

If two or more distinct but shareable in\-memory databases are needed
in a single process, then the [mode\=memory](uri.html#coreqp) query parameter can
be used with a [URI filename](uri.html) to create a named in\-memory database:


> ```
> 
> rc = sqlite3_open("file:memdb1?mode=memory&cache=shared", &db);
> 
> ```



Or,


> ```
> 
> ATTACH DATABASE 'file:memdb1?mode=memory&cache=shared' AS aux1;
> 
> ```


When an in\-memory database is named in this way, it will only share its
cache with another connection that uses exactly the same name.




## Temporary Databases


When the name of the database file handed to [sqlite3\_open()](c3ref/open.html) or to
[ATTACH](lang_attach.html) is an empty string, then a new temporary file is created to hold
the database.



> ```
> 
> rc = sqlite3_open("", &db);
> 
> ```



> ```
> 
> ATTACH DATABASE '' AS aux2;
> 
> ```


A different temporary file is created each time so that, just as
with the special ":memory:" string, two database connections to temporary
databases each have their own private database. Temporary databases are
automatically deleted when the connection that created them closes.


Even though a disk file is allocated for each temporary database, in
practice the temporary database usually resides in the in\-memory pager cache
and hence there is very little difference between a pure in\-memory database
created by ":memory:" and a temporary database created by an empty filename.
The sole difference is that a ":memory:" database must remain in memory
at all times whereas parts of a temporary database might be flushed to disk
if the database becomes large or if SQLite comes under memory pressure.


The previous paragraphs describe the behavior of temporary databases
under the default SQLite configuration. An application can use the
[temp\_store pragma](pragma.html#pragma_temp_store) and the [SQLITE\_TEMP\_STORE](compile.html#temp_store) compile\-time parameter to
force temporary databases to behave as pure in\-memory databases, if desired.



*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 












