




Defense Against The Dark Arts




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Defense Against The Dark Arts


# 1\. SQLite Always Validates Its Inputs



SQLite should never crash, overflow a buffer, leak memory,
or exhibit any other harmful behavior, even when presented with
maliciously malformed SQL inputs or database files. SQLite should
always detect erroneous inputs and raise an error, not crash or
corrupt memory.
Any malfunction caused by an SQL input or database file
is considered a serious bug and will be promptly addressed when
brought to the attention of the SQLite developers. SQLite is
extensively fuzz\-tested to help ensure that it is resistant
to these kinds of errors.




Nevertheless, bugs happen.
If you are writing an application that sends untrusted SQL inputs
or database files to SQLite, there are additional steps you can take
to help reduce the attack surface and
prevent zero\-day exploits caused by undetected bugs.



## 1\.1\. Untrusted SQL Inputs



Applications that accept untrusted SQL inputs should take the following
precautions:



1. Set the [SQLITE\_DBCONFIG\_DEFENSIVE](c3ref/c_dbconfig_defensive.html#sqlitedbconfigdefensive) flag.
This prevents ordinary SQL statements from deliberately corrupting the 
database file. SQLite should be proof against attacks that involve both
malicious SQL inputs and a maliciously corrupted database file at the
same time. Nevertheless, denying a script\-only attacker access to 
corrupt database inputs provides an extra layer of defense.
2. Reduce the [limits](limits.html) that SQLite imposes on inputs. This can help prevent
denial of service attacks and other kinds of mischief that can occur
as a result of unusually large inputs. You can do this either at compile\-time
using \-DSQLITE\_MAX\_... options, or at run\-time using the
[sqlite3\_limit()](c3ref/limit.html) interface. Most applications can reduce limits
dramatically without impacting functionality. The table below
provides some suggestions, though exact values will vary depending
on the application:





| Limit Setting | Default Value | High\-security Value |
| --- | --- | --- |
| LIMIT\_LENGTH | 1,000,000,000 | 1,000,000 |
| LIMIT\_SQL\_LENGTH | 1,000,000,000 | 100,000 |
| LIMIT\_COLUMN | 2,000 | 100 |
| LIMIT\_EXPR\_DEPTH | 1,000 | 10 |
| LIMIT\_COMPOUND\_SELECT | 500 | 3 |
| LIMIT\_VDBE\_OP | 250,000,000 | 25,000 |
| LIMIT\_FUNCTION\_ARG | 127 | 8 |
| LIMIT\_ATTACH | 10 | 0 |
| LIMIT\_LIKE\_PATTERN\_LENGTH | 50,000 | 50 |
| LIMIT\_VARIABLE\_NUMBER | 999 | 10 |
| LIMIT\_TRIGGER\_DEPTH | 1,000 | 10 |
3. Consider using the [sqlite3\_set\_authorizer()](c3ref/set_authorizer.html) interface to limit
the scope of SQL that will be processed. For example, an application
that does not need to change the database schema might add an
sqlite3\_set\_authorizer() callback that causes any CREATE or DROP
statement to fail.
4. The SQL language is very powerful, and so it is always possible for
malicious SQL inputs (or erroneous SQL inputs caused by an application
bug) to submit SQL that runs for a very long time. To prevent this
from becoming a denial\-of\-service attack, consider using the
[sqlite3\_progress\_handler()](c3ref/progress_handler.html) interface to invoke a callback periodically
as each SQL statement runs, and have that callback return non\-zero to
abort the statement if the statement runs for too long. Alternatively,
set a timer in a separate thread and invoke [sqlite3\_interrupt()](c3ref/interrupt.html) when
the timer goes off to prevent the SQL statement from running forever.
5. Limit the maximum amount of memory that SQLite will allocate using
the [sqlite3\_hard\_heap\_limit64()](c3ref/hard_heap_limit64.html) interface. This helps prevent
denial\-of\-service attacks. To find out how much heap space an
application actually needs, run the it against typical inputs and
then measure the maximum instantaneous memory usage with the 
[sqlite3\_memory\_highwater()](c3ref/memory_highwater.html) interface. Set the hard heap limit
to the maximum observed instantaneous memory usage plus some margin.
6. Consider setting the [SQLITE\_MAX\_ALLOCATION\_SIZE](compile.html#max_allocation_size) compile\-time option
to something smaller than its default value of 2147483391 (0x7ffffeff).
A value of 100000000 (100 million) or even smaller would not be unreasonable,
depending on the application.
7. For embedded systems, consider compiling SQLite with the
[\-DSQLITE\_ENABLE\_MEMSYS5](compile.html#enable_memsys5) option and then providing SQLite with
a fixed chunk of memory to use as its heap via the
[sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap)) interface. This will
prevent malicious SQL from executing a denial\-of\-service attack
by using an excessive amount of memory. If (say) 5 MB of memory
is provided for SQLite to use, once that much has been consumed,
SQLite will start returning SQLITE\_NOMEM errors rather than
soaking up memory needed by other parts of the application.
This also sandboxes SQLite's memory so that a write\-after\-free
error in some other part of the application will not cause
problems for SQLite, or vice versa.
8. To control memory usage in the [printf() SQL function](lang_corefunc.html#printf), compile
with "[\-DSQLITE\_PRINTF\_PRECISION\_LIMIT\=100000](compile.html#printf_precision_limit)" or some similarly
reasonable value.
This \#define limits the width and precision for %\-substitutions in the
printf() function, and thus prevents a hostile SQL statement from
consuming large amounts of RAM via constructs such as
"printf('%1000000000s','hi')".



Note that SQLite uses its built\-in printf() internally to help it
format the sql column in the [sqlite\_schema table](schematab.html). For that reason,
no table, index, view, or trigger definition can be much larger than the
precision limit. You can set a precision limit of less than 100000,
but be careful that whatever precision limit you use is at least as
long as the longest CREATE statement in your schema.



## 1\.2\. Untrusted SQLite Database Files


Applications that read or write SQLite database files of uncertain
provenance should take precautions enumerated below.



Even if the application does not deliberately accept database files 
from untrusted sources, beware of attacks in which a local 
database file is altered. For best security, any database file which 
might have ever been writable by an agent in a different security domain
should be treated as suspect.



1. If the application includes any [custom SQL functions](appfunc.html) or 
[custom virtual tables](vtab.html#customvtab) that have side effects or that might leak
privileged information, then the application should use one or more
of the techniques below to prevent a maliciously crafted database
schema from surreptitiously running those SQL functions and/or
virtual tables for nefarious purposes:



	1. Invoke [sqlite3\_db\_config](c3ref/db_config.html)(db,[SQLITE\_DBCONFIG\_TRUSTED\_SCHEMA](c3ref/c_dbconfig_defensive.html#sqlitedbconfigtrustedschema),0,0\)
	 on each [database connection](c3ref/sqlite3.html) as soon as it is opened.
	2. Run the [PRAGMA trusted\_schema\=OFF](pragma.html#pragma_trusted_schema) statement on each database connection
	 as soon as it is opened.
	3. Compile SQLite using the [\-DSQLITE\_TRUSTED\_SCHEMA\=0](compile.html#trusted_schema) compile\-time option.
	4. Disable the surreptitious use of custom SQL functions and virtual tables
	 by setting the [SQLITE\_DIRECTONLY](c3ref/c_deterministic.html#sqlitedirectonly) flag on all custom SQL functions and
	 the [SQLITE\_VTAB\_DIRECTONLY](c3ref/c_vtab_constraint_support.html#sqlitevtabdirectonly) flag on all custom virtual tables.
2. If the application does not use triggers or views, consider disabling the
unused capabilities with:



> ```
> 
> [sqlite3_db_config](c3ref/db_config.html)(db,[SQLITE_DBCONFIG_ENABLE_TRIGGER](c3ref/c_dbconfig_defensive.html#sqlitedbconfigenabletrigger),0,0);
> [sqlite3_db_config](c3ref/db_config.html)(db,[SQLITE_DBCONFIG_ENABLE_VIEW](c3ref/c_dbconfig_defensive.html#sqlitedbconfigenableview),0,0);
> 
> ```



For reading database files that are unusually high\-risk, such as database
files that are received from remote machines, and possibly from anonymous
contributors, the following extra precautions
might be justified. These added defenses come with performance costs,
however, and so may not be appropriate in every situation:



1. Run [PRAGMA integrity\_check](pragma.html#pragma_integrity_check) or [PRAGMA quick\_check](pragma.html#pragma_quick_check) on the database
as the first SQL statement after opening the database files and
prior to running any other SQL statements. Reject and refuse to
process any database file containing errors.
2. Enable the [PRAGMA cell\_size\_check\=ON](pragma.html#pragma_cell_size_check) setting.
3. Do not enable memory\-mapped I/O.
In other words, make sure that [PRAGMA mmap\_size\=0](pragma.html#pragma_mmap_size).


# 2\. Summary



The precautions above are not required in order to use SQLite safely
with potentially hostile inputs.
However, they do provide an extra layer of defense against zero\-day
exploits and are encouraged for applications that pass data from
untrusted sources into SQLite.


*This page last modified on [2024\-01\-16 14:06:27](https://sqlite.org/docsrc/honeypot) UTC* 


