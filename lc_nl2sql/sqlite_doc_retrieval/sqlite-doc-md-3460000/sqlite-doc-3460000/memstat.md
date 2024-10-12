




The SQLITE\_MEMSTAT Virtual Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The SQLITE\_MEMSTAT Virtual Table


# 1\. Overview



The SQLITE\_MEMSTAT extension implements an [eponymous\-only virtual table](vtab.html#epoonlyvtab) that
provides SQL access to the [sqlite3\_status64()](c3ref/status.html) and
[sqlite3\_db\_status()](c3ref/db_status.html) interfaces.




The SQLITE\_STMT extension can also be loaded at run\-time
by compiling the extension into a shared library or DLL using the source
code at <https://sqlite.org/src/file/ext/misc/memstat.c> and following the
instructions for how to [compile loadable extensions](loadext.html#build).



# 2\. Usage



The SQLITE\_MEMSTAT virtual table is a read\-only table that can be
queried to determine performance characteristics (primarily the
amount of memory being used) of the current instance of SQLite.
The SQLITE\_MEMSTATE table is essentially a wrapper around the
C\-language APIs [sqlite3\_status64()](c3ref/status.html) and [sqlite3\_db\_status()](c3ref/db_status.html).
If the 
[memstat.c](https://sqlite.org/src/file/ext/misc/memstat.c) source
file is compiled with the \-DSQLITE\_ENABLE\_ZIPVFS option, then SQLITE\_MEMSTAT
will also do some [file\-control](c3ref/file_control.html) calls to extract
memory usage information about the 
[ZIPVFS](https://www.hwaci.com/sw/sqlite/zipvfs.html) subsystem, 
if that subsystem as been licensed, installed, and is in use.




The SQLITE\_MEMSTAT table appears to have the following schema:




```
CREATE TABLE sqlite_memstat(
  name TEXT,
  schema TEXT,
  value INT,
  hiwtr INT
);

```


Each row of the SQLITE\_MEMSTAT table corresponds to a single call to
one of the [sqlite3\_status64()](c3ref/status.html) or [sqlite3\_db\_status()](c3ref/db_status.html) interfaces.
The NAME column of the row identifies which "verb" was passed to those
interfaces. For example, if [sqlite3\_status64()](c3ref/status.html) is invoked with
[SQLITE\_STATUS\_MEMORY\_USED](c3ref/c_status_malloc_count.html#sqlitestatusmemoryused), then the NAME column is 'MEMORY\_USED'.
Or if [sqlite3\_db\_status()](c3ref/db_status.html) is invoked with [SQLITE\_DBSTATUS\_CACHE\_USED](c3ref/c_dbstatus_options.html#sqlitedbstatuscacheused),
then the NAME column is "DB\_CACHE\_USED".




The SCHEMA column is NULL, except for cases when the [sqlite3\_file\_control()](c3ref/file_control.html)
interface is used to interrogate the ZIPVFS backend. As this only happens
when the memstat.c module is compiled with \-DSQLITE\_ENABLE\_ZIPVFS and when
[ZIPVFS](https://www.hwaci.com/sw/sqlite/zipvfs.html) is in use, 
SCHEMA is usually NULL.




The VALUE and HIWTR columns report the current value of the measure and
its "high\-water mark". The high\-water mark is the highest value ever seen
for the measurement, at least since the last reset. The SQLITE\_MEMSTAT
virtual table does not provide a mechanism for resetting the high\-water mark.




Depending on which parameter is being interrogated, one of the VALUE
or HIWTR mark measurements might be undefined. For example, only the
high\-water mark is meaningful for [SQLITE\_STATUS\_MALLOC\_SIZE](c3ref/c_status_malloc_count.html#sqlitestatusmallocsize), and
only the current value is meaningful for [SQLITE\_DBSTATUS\_CACHE\_USED](c3ref/c_dbstatus_options.html#sqlitedbstatuscacheused).
For rows where one or the other of VALUE or HIWTR is not meaningful,
that value is returned as NULL.
the 

interfaces, with the initial


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


