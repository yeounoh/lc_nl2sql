




Recovering Data From A Corrupt SQLite Database




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Recovering Data From A Corrupt SQLite Database


►
Table Of Contents
[1\. Recovering (Some) Data From A Corrupt SQLite Database](#recovering_some_data_from_a_corrupt_sqlite_database)
[1\.1\. Limitations](#limitations)
[2\. Recovery Using The ".recover" Command In The CLI](#recovery_using_the_recover_command_in_the_cli)
[3\. Building The Recovery API Into An Application](#building_the_recovery_api_into_an_application)
[3\.1\. Source Code Files](#source_code_files)
[3\.2\. How To Implement Recovery](#how_to_implement_recovery)
[3\.3\. Example Implementations](#example_implementations)




# 1\. Recovering (Some) Data From A Corrupt SQLite Database



SQLite databases are remarkably rebust. Application faults and
power failures typically leave the content of the database intact.
However, it is possible to [corrupt an SQLite database](howtocorrupt.html).
For example, hardware malfunctions can damage the database file, or a
rogue process can open the database and overwrite parts of it.




Given a corrupt database file, it is sometimes desirable to try to
salvage as much data from the file as possible. The recovery API
is designed to facilitate this.



## 1\.1\. Limitations



It is sometimes possible to perfectly restore a database that has
gone corrupt, but that is the exception. Usually
the recovered database will be defective in a number of ways:



* Some content might be permanently deleted and unrecoverable.
This can happen, for example, if a rogue process overwrites part
of the database file.
* Previously deleted content might reappear. Normally when SQLite
does a DELETE operation, it does not actually overwrite the old content
but instead remembers that space is available for reuse during the next
INSERT. If such deleted content is still in the file when a recovery
is attempted, it might be extracted and "resurrected".
* Recovered content might be altered.
For example, the value stored in a particular row
might change from 48 to 49\. Or it might change from an integer into
a string or blob. A value that was NULL might become an integer.
A string value might become a BLOB. And so forth.
* Constraints may not be valid after recovery. CHECK constraints, 
FOREIGN KEY constraints, UNIQUE constraints, type constraints on
[STRICT tables](stricttables.html) \- any of these might be violated in the recovered
database.
* Content might be moved from one table into another.



The recovery API does as good of a job as it can at restoring a database,
but the results will always be suspect. Sometimes (for example if the
corruption is restricted to indexes) the recovery will perfectly restore
the database content. However in other cases, the recovery will be imperfect.
The impact of this imperfection depends on the application. A database that
holds a list of bookmarks is still a list of bookmarks after recovery.
A few bookmarks might be missing or added or altered after recovery, but
the list is "fuzzy" and imperfect to begin with so adding a bit more
uncertainty will not be fatal to the application. But if an accounting
database goes corrupt and is subsequently recovered, the books might be
out of balance.




It is best to think of the recovery API as a salvage undertaking.
Recovery will extract as much usable data as it can from the wreck
of the old database, but some parts may be damaged beyond repair and
some rework and testing should be performed prior to returning the
recovered database to service.



# 2\. Recovery Using The ".recover" Command In The CLI



The easiest way to manually recover a corrupt database is using
the [Command Line Interface](cli.html) or "CLI" for SQLite. The CLI is a program
named "sqlite3". Use it to recover a corrupt database file using
a command similar to the following:




```
sqlite3 corrupt.db .recover >data.sql

```


This will generate SQL text in the file named "data.sql" that can be used
to reconstruct the original database:




```
sqlite3 recovered.db <data.sql

```


The ".recover" option is actually a command that is issued to the
CLI. That command can accept arguments. For example, by running:




```
sqlite3 corruptdb ".recover --ignore-freelist" >data.sql

```


Notice that the ".recover" command and its arguments must be contained
in quotes. The following options are supported:







> \-\-ignore\-freelist
> 
> Ignore pages of the database that appear to be part of the
> freelist. Normally the freelist is scanned, and if it contains
> pages that look like they have content, that content is output.
> But if the page really is on the freelist, that can mean that
> previously deleted information is reintroduced into the database.
> 
> 
> 
> \-\-lost\-and\-found *TABLE*
> 
> If content is found during recovery that cannot be associated
> with a particular table, it is put into the "lost\_and\_found"
> table. Use this option to change the name of the
> "lost\_and\_found" table to "TABLE".
> 
> 
> 
> \-\-no\-rowids
> 
> If this option is provided, then rowid values that are not also
> INTEGER PRIMARY KEY values are not extracted from the
> corrupt database.


# 3\. Building The Recovery API Into An Application


## 3\.1\. Source Code Files


If you want to build the recovery API into your application, you will
need to add some source files to your build, above and beyond the usual
"sqlite3\.c" and "sqlite3\.h" source files. You will need:







> | [sqlite3recover.c](https://sqlite.org/src/file/ext/recover/sqlite3recover.c) | This is the main source file that implements the recovery API. |
> | --- | --- |
> | [sqlite3recover.h](https://sqlite.org/src/file/ext/recover/sqlite3recover.h) | This is the header file that goes with sqlite3recover.h. |
> | [dbdata.c](https://sqlite.org/src/file/ext/recover/dbdata.c) | This file implements two virtual tables name "sqlite\_dbdata" and "sqlite\_dbptr" that required by sqlite3recover.c. |



The two C source file above need to be linked into your application in the
same way as "sqlite3\.c" is linked in. And the header file needs to be
accessible to the compiler when the C files are being compiled.




Additionally, the application, or more specifically the sqlite3\.c linked
into the application, must be compiled with the following option:



```

        -DSQLITE_ENABLE_DBPAGE_VTAB

```

## 3\.2\. How To Implement Recovery


These are the basic steps needed to recover content from a corrupt
Database:



1. Creates an sqlite3\_recover handle by calling either
sqlite3\_recover\_init() or sqlite3\_recover\_init\_sql().
Use sqlite3\_recover\_init() to store the recovered content
in a separate database and use sqlite3\_recover\_init\_sql()
to generate SQL text that will reconstruct the database.
2. Make zero or more calls to sqlite3\_recover\_config() to set
options on the new sqlite3\_recovery handle.
3. Invoke sqlite3\_recover\_step() repeatedly
until it returns something other than SQLITE\_OK. If it
returns SQLITE\_DONE, then the recovery operation completed without 
error. If it returns some other non\-SQLITE\_OK value, then an error 
has occurred. The sqlite3\_recover\_run() interface is also
available as a convenience wrapper that simply invokes
sqlite3\_recover\_step() repeatedly until it returns something other
than SQLITE\_DONE.
4. Retrieves any error code and English language error message using the
sqlite3\_recover\_errcode() and sqlite3\_recover\_errmsg() interfaces,
respectively.
5. Invoke sqlite3\_recover\_finish() to destroy the sqlite3\_recover object.



Details of the interface are described in comments in the
[sqlite3\_recover.h header file](https://sqlite.org/src/file/ext/recover/sqlite3recover.h).



## 3\.3\. Example Implementations



Examples of how the recovery extension is used by SQLite itself
can be seen at the following links:



* [https://sqlite.org/src/info/30475c820dc5ab8a8?ln\=999,1026](https://sqlite.org/src/info/30475c820dc5ab8a8?ln=999,1026)



An example of the recovery extension found in the 
"fuzzcheck" testing utility in the SQLite tree.
* [https://sqlite.org/src/info/84bb08d8762920285f08f1c0?ln\=7299,7361](https://sqlite.org/src/info/84bb08d8762920285f08f1c0?ln=7299,7361)



The code that implements the ".recover" command in the [CLI](cli.html).


*This page last modified on [2023\-02\-28 11:22:37](https://sqlite.org/docsrc/honeypot) UTC* 


