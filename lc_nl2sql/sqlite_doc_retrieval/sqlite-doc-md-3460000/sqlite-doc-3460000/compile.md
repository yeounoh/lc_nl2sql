




Compile\-time Options




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Compile\-time Options


►
Table Of Contents
[1\. Overview](#overview)
[2\. Recommended Compile\-time Options](#recommended_compile_time_options)
[3\. Platform Configuration](#_platform_configuration)
[4\. Options To Set Default Parameter Values](#_options_to_set_default_parameter_values)
[5\. Options To Set Size Limits](#_options_to_set_size_limits)
[6\. Options To Control Operating Characteristics](#_options_to_control_operating_characteristics)
[7\. Options To Enable Features Normally Turned Off](#_options_to_enable_features_normally_turned_off)
[8\. Options To Disable Features Normally Turned On](#_options_to_disable_features_normally_turned_on)
[9\. Options To Omit Features](#_options_to_omit_features)
[10\. Analysis and Debugging Options](#_analysis_and_debugging_options)
[11\. Windows\-Specific Options](#_windows_specific_options)
[12\. Compiler Linkage and Calling Convention Control](#compiler_linkage_and_calling_convention_control)




# 1\. Overview



For most purposes, SQLite can be built just fine using the default
compilation options. However, if required, the compile\-time options
documented below can be used to
[omit SQLite features](#omitfeatures) (resulting in
a [smaller compiled library size](footprint.html)) or to change the
[default values](#defaults) of some parameters.




Every effort has been made to ensure that the various combinations
of compilation options work harmoniously and produce a working library.
Nevertheless, it is strongly recommended that the SQLite test\-suite
be executed to check for errors before using an SQLite library built
with non\-standard compilation options.




# 2\. Recommended Compile\-time Options


The following compile\-time options are recommended for applications that
are able to use them, in order to minimized the number of CPU cycles and
the bytes of memory used by SQLite.
Not all of these compile\-time options are usable by every application.
For example, the SQLITE\_THREADSAFE\=0 option is only usable by applications
that never access SQLite from more than one thread at a time. And the
SQLITE\_OMIT\_PROGRESS\_CALLBACK option is only usable by applications that
do not use the [sqlite3\_progress\_handler()](c3ref/progress_handler.html) interface. And so forth.



It is impossible to test every possible combination of compile\-time
options for SQLite. But the following set of compile\-time options is
one configuration that is always fully tested.



1. **[SQLITE\_DQS\=0](compile.html#dqs)**.
This setting disables the [double\-quoted string literal](quirks.html#dblquote) misfeature.
2. **[SQLITE\_THREADSAFE\=0](compile.html#threadsafe)**.
Setting \-DSQLITE\_THREADSAFE\=0 causes all of the mutex and thread\-safety logic
in SQLite to be omitted. This is the single compile\-time option causes SQLite
to run about 2% faster and also reduces the size of the library by about 2%.
But the downside is that using the compile\-time option means that SQLite can never
be used by more than a single thread at a time, even if each thread has its own
database connection.
3. **[SQLITE\_DEFAULT\_MEMSTATUS\=0](compile.html#default_memstatus)**.
This setting causes the [sqlite3\_status()](c3ref/status.html) interfaces that track memory usage
to be disabled. This helps the [sqlite3\_malloc()](c3ref/free.html) routines run much faster,
and since SQLite uses [sqlite3\_malloc()](c3ref/free.html) internally, this helps to make the
entire library faster.
4. **[SQLITE\_DEFAULT\_WAL\_SYNCHRONOUS\=1](compile.html#default_wal_synchronous)**.
For maximum database safety following a power loss, the setting of
[PRAGMA synchronous\=FULL](pragma.html#pragma_synchronous) is recommended. However, in [WAL mode](wal.html), complete
database integrity is guaranteed with [PRAGMA synchronous\=NORMAL](pragma.html#pragma_synchronous). With
[PRAGMA synchronous\=NORMAL](pragma.html#pragma_synchronous) in [WAL mode](wal.html), recent changes to the database might
be rolled back by a power loss, but the database will not be corrupted.
Furthermore, transaction commit is much faster in WAL mode using
synchronous\=NORMAL than with the default synchronous\=FULL. For these
reasons, it is recommended that the synchronous setting be changed from
FULL to NORMAL when switching to WAL mode. This compile\-time option will
accomplish that.
5. **[SQLITE\_LIKE\_DOESNT\_MATCH\_BLOBS](compile.html#like_doesnt_match_blobs)**.
Historically, SQLite has allowed BLOB operands to the [LIKE](lang_expr.html#like) and [GLOB](lang_expr.html#glob)
operators. But having a BLOB as an operand of [LIKE](lang_expr.html#like) or [GLOB](lang_expr.html#glob) complicates
and slows the [LIKE optimization](optoverview.html#like_opt). When this option is set, it means that
the LIKE and GLOB operators always return FALSE if either operand is a BLOB.
That simplifies the implementation of the [LIKE optimization](optoverview.html#like_opt) and allows
queries that use the [LIKE optimization](optoverview.html#like_opt) to run faster.
6. **[SQLITE\_MAX\_EXPR\_DEPTH\=0](limits.html#max_expr_depth)**.
Setting the maximum expression parse\-tree depth to zero disables all checking
of the expression parse\-tree depth, which simplifies the code resulting in
faster execution, and helps the parse tree to use less memory.
7. **[SQLITE\_OMIT\_DECLTYPE](compile.html#omit_decltype)**.
By omitting the (seldom\-needed) ability to return the declared type of
columns from the result set of query, [prepared statements](c3ref/stmt.html) can be made
to consume less memory.
8. **[SQLITE\_OMIT\_DEPRECATED](compile.html#omit_deprecated)**.
Omitting deprecated interfaces and features will not help SQLite to
run any faster. It will reduce the library footprint, however. And
it is the right thing to do.
9. **[SQLITE\_OMIT\_PROGRESS\_CALLBACK](compile.html#omit_progress_callback)**.
The progress handler callback counter must be checked in the inner loop
of the [bytecode engine](opcode.html). By omitting this interface, a single conditional
is removed from the inner loop of the [bytecode engine](opcode.html), helping SQL statements
to run slightly faster.
10. **[SQLITE\_OMIT\_SHARED\_CACHE](compile.html#omit_shared_cache)**.
Omitting the possibility of using [shared cache](sharedcache.html) allows many conditionals
in performance\-critical sections of the code to be eliminated. This can
give a noticeable improvement in performance.
11. **[SQLITE\_USE\_ALLOCA](compile.html#use_alloca)**.
Make use of alloca() for dynamically allocating temporary stack space for
use within a single function, on systems that support alloca(). Without
this option, temporary space is allocated from the heap.
12. **[SQLITE\_OMIT\_AUTOINIT](compile.html#omit_autoinit)**.
The SQLite library needs to be initialized using a call to
[sqlite3\_initialize()](c3ref/initialize.html) before certain interfaces are used.
This initialization normally happens automatically the first time
it is needed. However, with the SQLITE\_OMIT\_AUTOINIT option, the automatic
initialization is omitted. This helps many API calls to run a little faster
(since they do not have to check to see if initialization has already occurred
and then run initialization if it has not previously been invoked) but it
also means that the application must call [sqlite3\_initialize()](c3ref/initialize.html) manually.
If SQLite is compiled with \-DSQLITE\_OMIT\_AUTOINIT and a routine like
[sqlite3\_malloc()](c3ref/free.html) or [sqlite3\_vfs\_find()](c3ref/vfs_find.html) or [sqlite3\_open()](c3ref/open.html) is invoked
without first calling [sqlite3\_initialize()](c3ref/initialize.html), the likely result will be
a segfault.
13. **[SQLITE\_STRICT\_SUBTYPE\=1](compile.html#strict_subtype)**.
This option causes an error to be raised if an application defined
function that does not have the [SQLITE\_RESULT\_SUBTYPE](c3ref/c_deterministic.html#sqliteresultsubtype) property
invokes the [sqlite3\_result\_subtype()](c3ref/result_subtype.html) interface. The sqlite3\_result\_subtype()
interface does not work reliably unless the function is registered
with the SQLITE\_RESULT\_SUBTYPE property. This compile\-time option
is designed to bring this problem to the attention of developers
early.


When all of the recommended compile\-time options above are used,
the SQLite library will be approximately 3% smaller and use about 5% fewer
CPU cycles. So these options do not make a huge difference. But in
some design situations, every little bit helps.



Library\-level configuration options, such as those listed above,
may optionally be defined in a client\-side header file. Defining
SQLITE\_CUSTOM\_INCLUDE\=myconfig.h (with no quotes) will cause sqlite3\.c
to include myconfig.h early on in the compilation process, enabling
the client to customize the flags without having to explicitly pass
all of them to the compiler.




# 3\.  Platform Configuration



**\_HAVE\_SQLITE\_CONFIG\_H**


> If the \_HAVE\_SQLITE\_CONFIG\_H macro is defined
>  then the SQLite source code will attempt to \#include a file named "sqlite\_cfg.h".
>  The "sqlite\_cfg.h" file usually contains other configuration options, especially
>  "HAVE\_*INTERFACE*" type options generated by autoconf scripts. Note that this
>  header is intended only for use for platform\-level configuration, not library\-level
>  configuration. To set SQLite\-level configuration flags in a custom header, define
>  SQLITE\_CUSTOM\_INCLUDE\=myconfig.h, as described in the previous section.


**HAVE\_FDATASYNC**


> If the HAVE\_FDATASYNC compile\-time option is true, then the default [VFS](vfs.html)
>  for unix systems will attempt to use fdatasync() instead of fsync() where
>  appropriate. If this flag is missing or false, then fsync() is always used.


**HAVE\_GMTIME\_R**


> If the HAVE\_GMTIME\_R option is true and if [SQLITE\_OMIT\_DATETIME\_FUNCS](compile.html#omit_datetime_funcs) is true,
>  then the CURRENT\_TIME, CURRENT\_DATE, and CURRENT\_TIMESTAMP keywords will use
>  the threadsafe "gmtime\_r()" interface rather than "gmtime()". In the usual case
>  where [SQLITE\_OMIT\_DATETIME\_FUNCS](compile.html#omit_datetime_funcs) is not defined or is false, then the
>  built\-in [date and time functions](lang_datefunc.html) are used to implement the CURRENT\_TIME,
>  CURRENT\_DATE, and CURRENT\_TIMESTAMP keywords and neither gmtime\_r() nor
>  gmtime() is ever called.


**HAVE\_ISNAN**


> If the HAVE\_ISNAN option is true, then SQLite invokes the system library isnan()
>  function to determine if a double\-precision floating point value is a NaN.
>  If HAVE\_ISNAN is undefined or false, then SQLite substitutes its own home\-grown
>  implementation of isnan().


**HAVE\_LOCALTIME\_R**


> If the HAVE\_LOCALTIME\_R option is true, then SQLite uses the threadsafe
>  localtime\_r() library routine instead of localtime()
>  to help implement the [localtime modifier](lang_datefunc.html#localtime)
>  to the built\-in [date and time functions](lang_datefunc.html).


**HAVE\_LOCALTIME\_S**


> If the HAVE\_LOCALTIME\_S option is true, then SQLite uses the threadsafe
>  localtime\_s() library routine instead of localtime()
>  to help implement the [localtime modifier](lang_datefunc.html#localtime)
>  to the built\-in [date and time functions](lang_datefunc.html).


**HAVE\_MALLOC\_USABLE\_SIZE**


> If the HAVE\_MALLOC\_USABLE\_SIZE option is true, then SQLite tries uses the
>  malloc\_usable\_size() interface to find the size of a memory allocation obtained
>  from the standard\-library malloc() or realloc() routines. This option is only
>  applicable if the standard\-library malloc() is used. On Apple systems,
>  "zone malloc" is used instead, and so this option is not applicable. And, of
>  course, if the application supplies its own malloc implementation using
>  [SQLITE\_CONFIG\_MALLOC](c3ref/c_config_covering_index_scan.html#sqliteconfigmalloc) then this option has no effect.
>  
>  If the HAVE\_MALLOC\_USABLE\_SIZE option is omitted or is false, then SQLite
>  uses a wrapper around system malloc() and realloc() that enlarges each allocation
>  by 8 bytes and writes the size of the allocation in the initial 8 bytes, and
>  then SQLite also implements its own home\-grown version of malloc\_usable\_size()
>  that consults that 8\-byte prefix to find the allocation size. This approach
>  works but it is suboptimal. Applications are encouraged to use
>  HAVE\_MALLOC\_USABLE\_SIZE whenever possible.


**HAVE\_STRCHRNUL**


> If the HAVE\_STRCHRNUL option is true, then SQLite uses the strchrnul() library
>  function. If this option is missing or false, then SQLite substitutes its own
>  home\-grown implementation of strchrnul().


**HAVE\_UTIME**


> If the HAVE\_UTIME option is true, then the built\-in but non\-standard
>  "unix\-dotfile" VFS will use the utime() system call, instead of utimes(),
>  to set the last access time on the lock file.


**SQLITE\_BYTEORDER\=*(0\|1234\|4321\)***


> SQLite needs to know if the native byte order of the target CPU is
>  big\-endian or little\-ending. The SQLITE\_BYTEORDER preprocessor is set
>  to 4321 for big\-endian machines and 1234 for little\-endian machines, or
>  it can be 0 to mean that the byte order must be determined at run\-time.
>  There are \#ifdefs in the code that set SQLITE\_BYTEORDER automatically
>  for all common platforms and compilers. However, it may be advantageous
>  to set SQLITE\_BYTEORDER appropriately when compiling SQLite for obscure
>  targets. If the target byte order cannot be determined at compile\-time,
>  then SQLite falls back to doing run\-time checks, which always work, though
>  with a small performance penalty.



# 4\.  Options To Set Default Parameter Values



**SQLITE\_DEFAULT\_AUTOMATIC\_INDEX\=*\<0 or 1\>***


> This macro determines the initial setting for [PRAGMA automatic\_index](pragma.html#pragma_automatic_index)
>  for newly opened [database connections](c3ref/sqlite3.html).
>  For all versions of SQLite through 3\.7\.17,
>  automatic indices are normally enabled for new database connections if
>  this compile\-time option is omitted.
>  However, that might change in future releases of SQLite.
>  See also: [SQLITE\_OMIT\_AUTOMATIC\_INDEX](compile.html#omit_automatic_index)


**SQLITE\_DEFAULT\_AUTOVACUUM\=*\<0 or 1 or 2\>***


> This macro determines if SQLite creates databases with the
>  [auto\_vacuum](pragma.html#pragma_auto_vacuum) flag set by default to OFF (0\), FULL (1\), or
>  INCREMENTAL (2\). The default value is 0 meaning that databases
>  are created with auto\-vacuum turned off.
>  In any case the compile\-time default may be overridden by the
>  [PRAGMA auto\_vacuum](pragma.html#pragma_auto_vacuum) command.


**SQLITE\_DEFAULT\_CACHE\_SIZE\=*\<N\>***


> This macro sets the default maximum size of the page\-cache for each attached
>  database. A positive value means that the limit is N page. If N is negative
>  that means to limit the cache size to \-N\*1024 bytes.
>  The suggested maximum cache size can be overridden by the
>  [PRAGMA cache\_size](pragma.html#pragma_cache_size) command. The default value is \-2000, which translates
>  into a maximum of 2048000 bytes per cache.


**SQLITE\_DEFAULT\_FILE\_FORMAT\=*\<1 or 4\>***


> The default [schema format number](fileformat2.html#schemaformat) used by SQLite when creating
>  new database files is set by this macro. The schema formats are all
>  very similar. The difference between formats 1 and 4 is that format
>  4 understands [descending indices](lang_createindex.html#descidx) and has a tighter encoding for
>  boolean values.
> 
> 
>  All versions of SQLite since 3\.3\.0 (2006\-01\-10\)
>  can read and write any schema format
>  between 1 and 4\. But older versions of SQLite might not be able to
>  read formats greater than 1\. So that older versions of SQLite will
>  be able to read and write database files created by newer versions
>  of SQLite, the default schema format was set to 1 for SQLite versions
>  through 3\.7\.9 (2011\-11\-01\). Beginning with
>  [version 3\.7\.10](releaselog/3_7_10.html) (2012\-01\-16\), the default
>  schema format is 4\.
> 
> 
>  The schema format number for a new database can be set at runtime using
>  the [PRAGMA legacy\_file\_format](pragma.html#pragma_legacy_file_format) command.


**SQLITE\_DEFAULT\_FILE\_PERMISSIONS\=*N***


> The default numeric file permissions for newly created database files
>  under unix. If not specified, the default is 0644 which means that
>  the files is globally readable but only writable by the creator.


**SQLITE\_DEFAULT\_FOREIGN\_KEYS\=*\<0 or 1\>***


> This macro determines whether enforcement of
>  [foreign key constraints](foreignkeys.html) is enabled or disabled by default for
>  new database connections. Each database connection can always turn
>  enforcement of foreign key constraints on and off and run\-time using
>  the [foreign\_keys pragma](pragma.html#pragma_foreign_keys). Enforcement of foreign key constraints
>  is normally off by default, but if this compile\-time parameter is
>  set to 1, enforcement of foreign key constraints will be on by default.


**SQLITE\_DEFAULT\_MMAP\_SIZE\=*N***


> This macro sets the default limit on the amount of memory that
>  will be used for memory\-mapped I/O
>  for each open database file. If the *N*
>  is zero, then memory mapped I/O is disabled by default. This
>  compile\-time limit and the [SQLITE\_MAX\_MMAP\_SIZE](compile.html#max_mmap_size) can be modified
>  at start\-time using the
>  [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_MMAP\_SIZE](c3ref/c_config_covering_index_scan.html#sqliteconfigmmapsize)) call, or at run\-time
>  using the [mmap\_size pragma](pragma.html#pragma_mmap_size).


**SQLITE\_DEFAULT\_JOURNAL\_SIZE\_LIMIT\=*\<bytes\>***


> This option sets the size limit on [rollback journal](lockingv3.html#rollback) files in
>  [persistent journal mode](pragma.html#pragma_journal_mode) and
>  [exclusive locking mode](pragma.html#pragma_locking_mode) and on the size of the
>  write\-ahead log file in [WAL mode](wal.html). When this
>  compile\-time option is omitted there is no upper bound on the
>  size of the rollback journals or write\-ahead logs.
>  The journal file size limit
>  can be changed at run\-time using the [journal\_size\_limit pragma](pragma.html#pragma_journal_size_limit).


**SQLITE\_DEFAULT\_LOCKING\_MODE\=*\<1 or 0\>***


> If set to 1, then the default [locking\_mode](pragma.html#pragma_locking_mode) is set to EXCLUSIVE.
>  If omitted or set to 0 then the default [locking\_mode](pragma.html#pragma_locking_mode) is NORMAL.


**SQLITE\_DEFAULT\_LOOKASIDE\=*SZ,N***


> Sets the default size of the [lookaside memory allocator](malloc.html#lookaside) memory pool
>  to N entries of SZ bytes each. This setting can be modified at
>  start\-time using [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_LOOKASIDE](c3ref/c_config_covering_index_scan.html#sqliteconfiglookaside)) and/or
>  as each [database connection](c3ref/sqlite3.html) is opened using
>  [sqlite3\_db\_config](c3ref/db_config.html)(db, [SQLITE\_DBCONFIG\_LOOKASIDE](c3ref/c_dbconfig_defensive.html#sqlitedbconfiglookaside)).


**SQLITE\_DEFAULT\_MEMSTATUS\=*\<1 or 0\>***


> This macro is used to determine whether or not the features enabled and
>  disabled using the SQLITE\_CONFIG\_MEMSTATUS argument to [sqlite3\_config()](c3ref/config.html)
>  are available by default. The default value is 1 ([SQLITE\_CONFIG\_MEMSTATUS](c3ref/c_config_covering_index_scan.html#sqliteconfigmemstatus)
>  related features enabled).
>  
>  The [sqlite3\_memory\_used()](c3ref/memory_highwater.html) and [sqlite3\_memory\_highwater()](c3ref/memory_highwater.html) interfaces,
>  the [sqlite3\_status64](c3ref/status.html)([SQLITE\_STATUS\_MEMORY\_USED](c3ref/c_status_malloc_count.html#sqlitestatusmemoryused)) interface,
>  and the [SQLITE\_MAX\_MEMORY](compile.html#max_memory) compile\-time option are all non\-functional
>  when memory usage tracking is disabled.


**SQLITE\_DEFAULT\_PCACHE\_INITSZ\=*N***


> This macro determines the number of pages initially allocated by the
>  page cache module when [SQLITE\_CONFIG\_PAGECACHE](c3ref/c_config_covering_index_scan.html#sqliteconfigpagecache) configuration option is
>  not use and memory for the page cache is obtained from [sqlite3\_malloc()](c3ref/free.html)
>  instead. The number of pages set by this macro are allocated in a single
>  allocation, which reduces the load on the memory allocator.


**SQLITE\_DEFAULT\_PAGE\_SIZE\=*\<bytes\>***


> This macro is used to set the default page\-size used when a
>  database is created. The value assigned must be a power of 2\. The
>  default value is 4096\. The compile\-time default may be overridden at
>  runtime by the [PRAGMA page\_size](pragma.html#pragma_page_size) command.


**SQLITE\_DEFAULT\_SYNCHRONOUS\=*\<0\-3\>***


> This macro determines the default value of the
>  [PRAGMA synchronous](pragma.html#pragma_synchronous) setting. If not overridden at compile\-time,
>  the default setting is 2 (FULL).


**SQLITE\_DEFAULT\_WAL\_SYNCHRONOUS\=*\<0\-3\>***


> This macro determines the default value of the
>  [PRAGMA synchronous](pragma.html#pragma_synchronous) setting for database files that open in
>  [WAL mode](wal.html). If not overridden at compile\-time, this value is the
>  same as [SQLITE\_DEFAULT\_SYNCHRONOUS](compile.html#default_synchronous).
>  
>  If SQLITE\_DEFAULT\_WAL\_SYNCHRONOUS differs from SQLITE\_DEFAULT\_SYNCHRONOUS,
>  and if the application has not modified the synchronous setting for
>  the database file using the [PRAGMA synchronous](pragma.html#pragma_synchronous) statement, then
>  the synchronous setting is changed to value defined by
>  SQLITE\_DEFAULT\_WAL\_SYNCHRONOUS when the database connection switches
>  into WAL mode for the first time.
>  If the SQLITE\_DEFAULT\_WAL\_SYNCHRONOUS value is not overridden at
>  compile\-time, then it will always be the same as
>  [SQLITE\_DEFAULT\_SYNCHRONOUS](compile.html#default_synchronous) and so no automatic synchronous setting
>  changes will ever occur.


**SQLITE\_DEFAULT\_WAL\_AUTOCHECKPOINT\=*\<pages\>***


> This macro sets the default page count for the [WAL](wal.html)
> [automatic checkpointing](wal.html#ckpt) feature. If unspecified,
>  the default page count is 1000\.


**SQLITE\_DEFAULT\_WORKER\_THREADS\=*N***


> This macro sets the default value for
>  the [SQLITE\_LIMIT\_WORKER\_THREADS](c3ref/c_limit_attached.html#sqlitelimitworkerthreads) parameter. The [SQLITE\_LIMIT\_WORKER\_THREADS](c3ref/c_limit_attached.html#sqlitelimitworkerthreads)
>  parameter sets the maximum number of auxiliary threads that a single
>  [prepared statement](c3ref/stmt.html) will launch to assist it with a query. If not specified,
>  the default maximum is 0\.
>  The value set here cannot be more than [SQLITE\_MAX\_WORKER\_THREADS](compile.html#max_worker_threads).


**SQLITE\_DQS\=*N***


> This macro determines the default values for
>  [SQLITE\_DBCONFIG\_DQS\_DDL](c3ref/c_dbconfig_defensive.html#sqlitedbconfigdqsddl) and [SQLITE\_DBCONFIG\_DQS\_DML](c3ref/c_dbconfig_defensive.html#sqlitedbconfigdqsdml), which
>  in turn determine how SQLite handles each [double\-quoted string literal](quirks.html#dblquote).
>  The "DQS" name stands for
>  "Double\-Quoted String".
>  The *N* argument should be an integer 0, 1, 2, or 3\.
>  
> > | SQLITE\_DQS Double\-Quoted Strings Allowed   Remarks  | In DDL In DML  | 3 yes yes default  | 2 yes no | 1 no yes | 0 no no recommended | | | | | --- | --- | --- | --- | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | | | | | | | | | | | | | | |
> > | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
> 
> 
> The recommended setting is 0, meaning that double\-quoted
>  strings are disallowed in all contexts. However, the default
>  setting is 3 for maximum compatibility with legacy applications.


**SQLITE\_EXTRA\_DURABLE**


> The SQLITE\_EXTRA\_DURABLE compile\-time option that used to cause the default
>  [PRAGMA synchronous](pragma.html#pragma_synchronous) setting to be EXTRA, rather than FULL. This option
>  is no longer supported. Use
>  [SQLITE\_DEFAULT\_SYNCHRONOUS\=3](compile.html#default_synchronous) instead.


**SQLITE\_FTS3\_MAX\_EXPR\_DEPTH\=*N***


> This macro sets the maximum depth of the search tree that corresponds to
>  the right\-hand side of the MATCH operator in an [FTS3](fts3.html) or [FTS4](fts3.html#fts4) full\-text
>  index. The full\-text search uses a recursive algorithm, so the depth of
>  the tree is limited to prevent using too much stack space. The default
>  limit is 12\. This limit is sufficient for up to 4095 search terms on the
>  right\-hand side of the MATCH operator and it holds stack space usage to
>  less than 2000 bytes.
>  
>  For ordinary FTS3/FTS4 queries, the search tree depth is approximately
>  the base\-2 logarithm of the number of terms in the right\-hand side of the
>  MATCH operator. However, for [phrase queries](fts3.html#phrase) and [NEAR queries](fts3.html#near) the
>  search tree depth is linear in the number of right\-hand side terms.
>  So the default depth limit of 12 is sufficient for up to 4095 ordinary
>  terms on a MATCH, it is only sufficient for 11 or 12 phrase or NEAR
>  terms. Even so, the default is more than enough for most application.


**SQLITE\_JSON\_MAX\_DEPTH\=*N***


> This macro sets the maximum nesting depth for JSON objects and arrays.
>  The default value is 1000\.
>  
>  The [JSON SQL functions](json1.html) use a
>  [recursive decent parser](https://en.wikipedia.org/wiki/Recursive_descent_parser).
>  This means that deeply nested JSON might require a lot of stack space to
>  parse. On systems with limited stack space, SQLite can be compiled with
>  a greatly reduced maximum JSON nesting depth to avoid the possibility of
>  a stack overflow, even from hostile inputs. A value of 10 or 20 is normally
>  sufficient even for the most complex real\-world JSON.


**SQLITE\_LIKE\_DOESNT\_MATCH\_BLOBS**


> This compile\-time option causes the [LIKE](lang_expr.html#like) operator to always return
>  False if either operand is a BLOB. The default behavior of [LIKE](lang_expr.html#like)
>  is that BLOB operands are cast to TEXT before the comparison is done.
>  
>  This compile\-time option makes SQLite run more efficiently when processing
>  queries that use the [LIKE](lang_expr.html#like) operator, at the expense of breaking backwards
>  compatibility. However, the backwards compatibility break may be only
>  a technicality. There was a long\-standing bug in the [LIKE](lang_expr.html#like) processing logic
>  (see <https://www.sqlite.org/src/info/05f43be8fdda9f>) that caused it to
>  misbehavior for BLOB operands and nobody observed that bug in nearly
>  10 years of active use. So for more users, it is probably safe to
>  enable this compile\-time option and thereby save a little CPU time
>  on LIKE queries.
>  
>  This compile\-time option affects the SQL [LIKE](lang_expr.html#like) operator only and has
>  no impact on the [sqlite3\_strlike()](c3ref/strlike.html) C\-language interface.


**SQLITE\_MAX\_MEMORY\=*N***


> This option limits the total amount of memory that SQLite will request
>  from malloc() to *N* bytes. Any attempt by SQLite to allocate
>  new memory that would cause the sum of all allocations held by SQLite to exceed
>  *N* bytes will result in an out\-of\-memory error.
>  This is a hard upper limit. See also the [sqlite3\_soft\_heap\_limit()](c3ref/soft_heap_limit.html)
>  interface.
>  
>  This option is a limit on the *total* amount of memory allocated.
>  See the [SQLITE\_MAX\_ALLOCATION\_SIZE](compile.html#max_allocation_size) option for a limitation on the amount
>  of memory allowed in any single memory allocation.
>  
>  This limit is only functional if memory usage statistics are available via
>  the [sqlite3\_memory\_used()](c3ref/memory_highwater.html) and [sqlite3\_status64](c3ref/status.html)([SQLITE\_STATUS\_MEMORY\_USED](c3ref/c_status_malloc_count.html#sqlitestatusmemoryused))
>  interfaces. Without that memory usage information, SQLite has no way of
>  knowing when it is about to go over the limit, and thus is unable to prevent
>  the excess memory allocation. Memory usage tracking is turned on by default,
>  but can be disabled at compile\-time using the [SQLITE\_DEFAULT\_MEMSTATUS](compile.html#default_memstatus) option,
>  or at start\-time using [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_MEMSTATUS](c3ref/c_config_covering_index_scan.html#sqliteconfigmemstatus)).


**SQLITE\_MAX\_MMAP\_SIZE\=*N***


> This macro sets a hard upper bound on the amount of address space that
>  can be used by any single database for memory\-mapped I/O.
>  Setting this value to 0 completely disables memory\-mapped I/O and
>  causes logic associated with memory\-mapped I/O to be omitted from the
>  build. This option does change the default memory\-mapped I/O address
>  space size (set by [SQLITE\_DEFAULT\_MMAP\_SIZE](compile.html#default_mmap_size) or
>  sqlite3\_config([SQLITE\_CONFIG\_MMAP\_SIZE](c3ref/c_config_covering_index_scan.html#sqliteconfigmmapsize)) or the
>  run\-time memory\-mapped I/O address space size (set by
>  sqlite3\_file\_control([SQLITE\_FCNTL\_MMAP\_SIZE](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlmmapsize)) or
>  [PRAGMA mmap\_size](pragma.html#pragma_mmap_size)) as long as those other settings are less than the
>  maximum value defined here.


**SQLITE\_MAX\_SCHEMA\_RETRY\=*N***


> Whenever the database schema changes, prepared statements are automatically
>  reprepared to accommodate the new schema. There is a race condition here
>  in that if one thread is constantly changing the schema, another thread
>  might spin on reparses and repreparations of a prepared statement and
>  never get any real work done. This parameter prevents an infinite loop
>  by forcing the spinning thread to give up after a fixed number of attempts
>  at recompiling the prepared statement. The default setting is 50 which is
>  more than adequate for most applications.


**SQLITE\_MAX\_WORKER\_THREADS\=*N***


> Set an upper bound on the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_WORKER\_THREADS](c3ref/c_limit_attached.html#sqlitelimitworkerthreads),N)
>  setting that determines the maximum number of auxiliary threads that a single
>  [prepared statement](c3ref/stmt.html) will use to aid with CPU\-intensive computations
>  (mostly sorting). See also the [SQLITE\_DEFAULT\_WORKER\_THREADS](compile.html#default_worker_threads) options.


**SQLITE\_MEMDB\_DEFAULT\_MAXSIZE\=*N***


> Set the default size limit (in bytes) for in\-memory databases created using
>  [sqlite3\_deserialize()](c3ref/deserialize.html). This is just the default. The limit can be
>  changed at start\-time using
>  [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_MEMDB\_MAXSIZE](c3ref/c_config_covering_index_scan.html#sqliteconfigmemdbmaxsize),N)
>  or at run\-time for individual databases using the
>  [SQLITE\_FCNTL\_SIZE\_LIMIT](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlsizelimit) [file\-control](c3ref/file_control.html).
>  If no default is specified, 1073741824 is used.


**SQLITE\_MINIMUM\_FILE\_DESCRIPTOR\=*N***


> The unix [VFS](vfs.html) will never use a file descriptor less than *N*. The
>  default value of *N* is 3\.
>  
>  Avoiding the use of low\-numbered file descriptors is a defense against
>  accidental database corruption. If a database file was opened using
>  file descriptor 2, for example, and then an assert() failed and invoked
>  write(2,...), that would likely cause database corruption by overwriting
>  part of the database file with the assertion error message. Using only
>  higher\-valued file descriptors avoids this potential problem. The
>  protection against
>  using low\-numbered file descriptors can be disabled by setting this
>  compile\-time option to 0\.


**SQLITE\_POWERSAFE\_OVERWRITE\=*\<0 or 1\>***


> This option changes the default assumption about [powersafe overwrite](psow.html)
>  for the underlying filesystems for the unix and windows [VFSes](vfs.html).
>  Setting SQLITE\_POWERSAFE\_OVERWRITE to 1 causes SQLite to assume that
>  application\-level writes cannot changes bytes outside the range of
>  bytes written even if the write occurs just before a power loss.
>  With SQLITE\_POWERSAFE\_OVERWRITE set to 0, SQLite assumes that other
>  bytes in the same sector with a written byte might be changed or
>  damaged by a power loss.


**SQLITE\_PRINTF\_PRECISION\_LIMIT\=*N***


> This option limits the maximum width and precision of substitutions
>  for the [printf() SQL function](lang_corefunc.html#printf) and the other C\-language string
>  formatting functions such as [sqlite3\_mprintf()](c3ref/mprintf.html) and
>  [sqlite3\_str\_appendf()](c3ref/str_append.html). This is turn can prevent a hostile or
>  malfunctioning script from using excessive memory by invoking
>  a format such as: "printf('%\*s',2147483647,'hi')".
>  A value for *N* of around 100000 is normally sufficient.
>  
>  The [printf() SQL function](lang_corefunc.html#printf) is subject to the [SQLITE\_LIMIT\_LENGTH](c3ref/c_limit_attached.html#sqlitelimitlength)
>  limit of [sqlite3\_limit()](c3ref/limit.html). Hence any printf() result with a
>  width or precision more than the SQLITE\_LIMIT\_LENGTH will cause
>  an [SQLITE\_TOOBIG](rescode.html#toobig) error. However, the low\-level formatting
>  for the printf() function is done by a subroutine that does not
>  have access to SQLITE\_LIMIT\_LENGTH. So the low\-level formatting
>  is done into a memory allocation that might be considerably larger
>  than SQLITE\_LIMIT\_LENGTH and the SQLITE\_LIMIT\_LENGTH check is only
>  performed after all formatting is complete. Thus there might be a
>  transient buffer that exceeds SQLITE\_LIMIT\_LENGTH. The
>  SQLITE\_PRINTF\_PRECISION\_LIMIT option is an additional check
>  that prevents excess sizes for the transient buffer used inside
>  the low\-level formatting subroutine, prior to the
>  SQLITE\_LIMIT\_LENGTH check.
>  
>  Be careful not to set SQLITE\_PRINTF\_PRECISION\_LIMIT too low.
>  SQLite uses its [built\-in printf()](printf.html) functionality to format the text
>  of CREATE statements stored in the [sqlite\_schema table](schematab.html). So
>  SQLITE\_PRINTF\_PRECISION\_LIMIT should be at least as big as the largest
>  table, index, view, or trigger definition that you are likely to
>  encounter.
>  
>  No error is raised if a width or precision exceeds
>  SQLITE\_PRINTF\_PRECISION\_LIMIT. Instead, the large width or
>  precision is silently truncated.
>  
>  The default value for SQLITE\_PRINTF\_PRECISION\_LIMIT is 2147483647
>  (0x7fffffff).


**SQLITE\_QUERY\_PLANNER\_LIMIT\=*N***


> As part of the query planning process, SQLite enumerates all usable
>  combinations of indexes and WHERE\-clause constraints. For certain
>  pathological queries, the number of these index\-and\-constraint combinations
>  can be very large, resulting in slow performance by the query planner.
>  The SQLITE\_QUERY\_PLANNER\_LIMIT value (in conjunction with the
>  related [SQLITE\_QUERY\_PLANNER\_LIMIT\_INCR](compile.html#query_planner_limit_incr) setting) limits the number
>  of index\-and\-constraint combinations that the query planner will
>  consider, in order to prevent the query planner from using excess
>  CPU time. The default value for SQLITE\_QUERY\_PLANNER\_LIMIT is set
>  high enough so that is never reached for real\-world queries. The
>  query planner search limit only applies to queries that are deliberately
>  crafted to use excess planning time.


**SQLITE\_QUERY\_PLANNER\_LIMIT\_INCR\=*N***


> The [SQLITE\_QUERY\_PLANNER\_LIMIT](compile.html#query_planner_limit) option sets an initial baseline value
>  for the maximum number of index\-and\-constraint combinations that the
>  query planner consider. The baseline query planner limit is increased
>  by SQLITE\_QUERY\_PLANNER\_LIMIT\_INCR prior to processing each table of a
>  join so that each table is guaranteed to be able to propose at least
>  some index\-and\-constraint combinations to the optimizer even if prior
>  tables of the join have exhausted the baseline limit. The default
>  value for both this compile\-time option and the
>  [SQLITE\_QUERY\_PLANNER\_LIMIT](compile.html#query_planner_limit) option are set high enough so that they should
>  never be reached for real\-world queries.


**SQLITE\_REVERSE\_UNORDERED\_SELECTS**


> This option causes the [PRAGMA reverse\_unordered\_selects](pragma.html#pragma_reverse_unordered_selects) setting to be
>  enabled by default. When enabled, [SELECT](lang_select.html) statements that lack an
>  ORDER BY clause will run in reverse order.
>  This option is useful for detecting when applications (incorrectly)
>  assume that the order of rows in a SELECT without an ORDER BY clause
>  will always be the same.


**SQLITE\_SORTER\_PMASZ\=*N***


> If multi\-threaded processing is enabled via the
>  [PRAGMA threads](pragma.html#pragma_threads) setting, then sort operations will
>  attempt to start helper threads when the amount of content
>  to be sorted exceeds the minimum of the [cache\_size](pragma.html#pragma_cache_size) and PMA Size
>  determined by the [SQLITE\_CONFIG\_PMASZ](c3ref/c_config_covering_index_scan.html#sqliteconfigpmasz) start\-time option.
>  This compile\-time option sets the default value for the
>  [SQLITE\_CONFIG\_PMASZ](c3ref/c_config_covering_index_scan.html#sqliteconfigpmasz) start\-time option.
>  The default value is 250\.


**SQLITE\_STMTJRNL\_SPILL\=*N***


> The SQLITE\_STMTJRNL\_SPILL compile\-time option determines the
>  default setting of the [SQLITE\_CONFIG\_STMTJRNL\_SPILL](c3ref/c_config_covering_index_scan.html#sqliteconfigstmtjrnlspill) start\-time
>  setting. That setting determines the size threshold above which
>  [statement journals](tempfiles.html#stmtjrnl) are moved from memory to disk.


**SQLITE\_WIN32\_MALLOC**


> This option enables the use of the Windows Heap API functions for memory
>  allocation instead of the standard library malloc() and free() routines.


**YYSTACKDEPTH\=*\<max\_depth\>***


> This macro sets the maximum depth of the LALR(1\) stack used by
>  the SQL parser within SQLite. The default value is 100\. A typical
>  application will use less than about 20 levels of the stack.
>  Developers whose applications contain SQL statements that
>  need more than 100 LALR(1\) stack entries should seriously
>  consider refactoring their SQL as it is likely to be well beyond
>  the ability of any human to comprehend.


# 5\.  Options To Set Size Limits


There are compile\-time options that will set upper bounds
on the sizes of various structures in SQLite. The compile\-time
options normally set a hard upper bound that can be changed
at run\-time on individual [database connections](c3ref/sqlite3.html) using the
[sqlite3\_limit()](c3ref/limit.html) interface.


The compile\-time options for setting upper bounds are
[documented separately](limits.html). The following is a list of
the available settings:


* [SQLITE\_MAX\_ATTACHED](limits.html#max_attached)
* [SQLITE\_MAX\_COLUMN](limits.html#max_column)
* [SQLITE\_MAX\_COMPOUND\_SELECT](limits.html#max_compound_select)
* [SQLITE\_MAX\_EXPR\_DEPTH](limits.html#max_expr_depth)
* [SQLITE\_MAX\_FUNCTION\_ARG](limits.html#max_function_arg)
* [SQLITE\_MAX\_LENGTH](limits.html#max_length)
* [SQLITE\_MAX\_LIKE\_PATTERN\_LENGTH](limits.html#max_like_pattern_length)
* [SQLITE\_MAX\_PAGE\_COUNT](limits.html#max_page_count)
* [SQLITE\_MAX\_SQL\_LENGTH](limits.html#max_sql_length)
* [SQLITE\_MAX\_VARIABLE\_NUMBER](limits.html#max_variable_number)


There are also some size limits that cannot be modified using
[sqlite3\_limit()](c3ref/limit.html). See, for example:



* [SQLITE\_FTS3\_MAX\_EXPR\_DEPTH](compile.html#fts3_max_expr_depth)
* [SQLITE\_JSON\_MAX\_DEPTH](compile.html#json_max_depth)
* [SQLITE\_MAX\_ALLOCATION\_SIZE](compile.html#max_allocation_size)
* [SQLITE\_MAX\_MEMORY](compile.html#max_memory)
* [SQLITE\_MAX\_MMAP\_SIZE](compile.html#max_mmap_size)
* [SQLITE\_PRINTF\_PRECISION\_LIMIT](compile.html#printf_precision_limit)
* [SQLITE\_TRACE\_SIZE\_LIMIT](compile.html#trace_size_limit)
* [YYSTACKDEPTH](compile.html#yystackdepth)



# 6\.  Options To Control Operating Characteristics



**SQLITE\_4\_BYTE\_ALIGNED\_MALLOC**


> On most systems, the malloc() system call returns a buffer that is
>  aligned to an 8\-byte boundary. But on some systems (ex: windows) malloc()
>  returns 4\-byte aligned pointer. This compile\-time option must be used
>  on systems that return 4\-byte aligned pointers from malloc().


**SQLITE\_CASE\_SENSITIVE\_LIKE**


> If this option is present, then the built\-in [LIKE](lang_expr.html#like) operator will be
>  case sensitive. This same effect can be achieved at run\-time using
>  the [case\_sensitive\_like pragma](pragma.html#pragma_case_sensitive_like).


**SQLITE\_DIRECT\_OVERFLOW\_READ**


> When this option is present, content contained in
>  [overflow pages](fileformat2.html#ovflpgs) of the database file is read directly from disk,
>  bypassing the [page cache](c3ref/pcache_methods2.html), during read transactions. In applications
>  that do a lot of reads of large BLOBs or strings, this option improves
>  read performance.
>  
>  As of version 3\.45\.0 (2024\-01\-15\), this option is enabled by
>  default. To disable it, using \-DSQLITE\_DIRECT\_OVERFLOW\_READ\=0\.


**SQLITE\_HAVE\_ISNAN**


> If this option is present, then SQLite will use the isnan() function from
>  the system math library. This is an alias for the [HAVE\_ISNAN](compile.html#isnan) configuration
>  option.


**SQLITE\_MAX\_ALLOCATION\_SIZE\=*N***


> This compile\-time option sets an upper bound on the size of memory
>  allocations that can be requested using [sqlite3\_malloc64()](c3ref/free.html),
>  [sqlite3\_realloc64()](c3ref/free.html), and similar. The default value is
>  2,147,483,391 (0x7ffffeff) and this should be considered an
>  upper bound. Most applications can get by with a maximum allocation
>  size of a few million bytes.
>  
>  This is a limit on the maximum size of any single memory allocation.
>  It is *not* a limit on the total amount of memory allocated.
>  See [SQLITE\_MAX\_MEMORY](compile.html#max_memory) for a limitation on the total amount of memory
>  allocated.
>  
>  Reducing the maximum size of individual memory allocations provides
>  extra defense against denial\-of\-service attacks that attempt to exhaust
>  system memory by doing many large allocations. It is also an extra layer
>  of defense against application bugs where the size of a memory allocation
>  is computed using a signed 32\-bit integer that could overflow →
>  with a small maximum allocation size, such buggy memory allocation size
>  computations are likely to be spotted sooner due to out\-of\-memory errors
>  and before the integer actually overflows.


**SQLITE\_OS\_OTHER\=*\<0 or 1\>***


> The option causes SQLite to omit its built\-in operating system interfaces
>  for Unix, Windows, and OS/2\. The resulting library will have no default
>  [operating system interface](c3ref/vfs.html). Applications must use
>  [sqlite3\_vfs\_register()](c3ref/vfs_find.html) to register an appropriate interface before
>  using SQLite. Applications must also supply implementations for the
>  [sqlite3\_os\_init()](c3ref/initialize.html) and [sqlite3\_os\_end()](c3ref/initialize.html) interfaces. The usual practice
>  is for the supplied [sqlite3\_os\_init()](c3ref/initialize.html) to invoke [sqlite3\_vfs\_register()](c3ref/vfs_find.html).
>  SQLite will automatically invoke [sqlite3\_os\_init()](c3ref/initialize.html) when it initializes.
> 
> 
>  This option is typically used when building SQLite for an embedded
>  platform with a custom operating system.


**SQLITE\_SECURE\_DELETE**


> This compile\-time option changes the default setting of the
>  [secure\_delete pragma](pragma.html#pragma_secure_delete). When this option is not used, secure\_delete defaults
>  to off. When this option is present, secure\_delete defaults to on.
> 
> 
>  The secure\_delete setting causes deleted content to be overwritten with
>  zeros. There is a small performance penalty since additional I/O
>  must occur. On the other hand, secure\_delete can prevent fragments of
>  sensitive information from lingering in unused parts of the database file
>  after it has been deleted. See the documentation on the
>  [secure\_delete pragma](pragma.html#pragma_secure_delete) for additional information.


**SQLITE\_THREADSAFE\=*\<0 or 1 or 2\>***


> This option controls whether or not code is included in SQLite to
>  enable it to operate safely in a multithreaded environment. The
>  default is SQLITE\_THREADSAFE\=1 which is safe for use in a multithreaded
>  environment. When compiled with SQLITE\_THREADSAFE\=0 all mutexing code
>  is omitted and it is unsafe to use SQLite in a multithreaded program.
>  When compiled with SQLITE\_THREADSAFE\=2, SQLite can be used in a multithreaded
>  program so long as no two threads attempt to use the same
>  [database connection](c3ref/sqlite3.html) (or any [prepared statements](c3ref/stmt.html) derived from
>  that database connection) at the same time.
> 
> 
>  To put it another way, SQLITE\_THREADSAFE\=1 sets the default
>  [threading mode](threadsafe.html) to Serialized. SQLITE\_THREADSAFE\=2 sets the default
>  [threading mode](threadsafe.html) to Multi\-threaded. And SQLITE\_THREADSAFE\=0 sets the
>  [threading mode](threadsafe.html) to Single\-threaded.
> 
> 
>  The value of SQLITE\_THREADSAFE can be determined at run\-time
>  using the [sqlite3\_threadsafe()](c3ref/threadsafe.html) interface.
> 
> 
>  When SQLite has been compiled with SQLITE\_THREADSAFE\=1 or
>  SQLITE\_THREADSAFE\=2 then the [threading mode](threadsafe.html)
>  can be altered at run\-time using the [sqlite3\_config()](c3ref/config.html) interface together
>  with one of these verbs:
> 
> 
>  * [SQLITE\_CONFIG\_SINGLETHREAD](c3ref/c_config_covering_index_scan.html#sqliteconfigsinglethread)* [SQLITE\_CONFIG\_MULTITHREAD](c3ref/c_config_covering_index_scan.html#sqliteconfigmultithread)* [SQLITE\_CONFIG\_SERIALIZED](c3ref/c_config_covering_index_scan.html#sqliteconfigserialized)
> 
> 
> 
>  The [SQLITE\_OPEN\_NOMUTEX](c3ref/c_open_autoproxy.html) and
>  [SQLITE\_OPEN\_FULLMUTEX](c3ref/c_open_autoproxy.html) flags to [sqlite3\_open\_v2()](c3ref/open.html) can also be used
>  to adjust the [threading mode](threadsafe.html) of individual [database connections](c3ref/sqlite3.html)
>  at run\-time.
> 
> 
>  Note that when SQLite is compiled with SQLITE\_THREADSAFE\=0, the code
>  to make SQLite threadsafe is omitted from the build. When this occurs,
>  it is impossible to change the [threading mode](threadsafe.html) at start\-time or run\-time.
> 
> 
>  See the [threading mode](threadsafe.html) documentation for additional information
>  on aspects of using SQLite in a multithreaded environment.


**SQLITE\_TEMP\_STORE\=*\<0 through 3\>***


> This option controls whether temporary files are stored on disk or
>  in memory. The meanings for various settings of this compile\-time
>  option are as follows:
> 
> 
>  
> 
> | SQLITE\_TEMP\_STORE | Meaning |
> | --- | --- |
> | 0 | Always use temporary files |
> | 1 | Use files by default but allow the  [PRAGMA temp\_store](pragma.html#pragma_temp_store) command to override |
> | 2 | Use memory by default but allow the  [PRAGMA temp\_store](pragma.html#pragma_temp_store) command to override |
> | 3 | Always use memory |
> 
> 
> 
> 
>  The default setting is 1\.
>  Additional information can be found in [tempfiles.html](tempfiles.html#tempstore).


**SQLITE\_TRACE\_SIZE\_LIMIT\=*N***


> If this macro is defined to a positive integer *N*, then the length of
>  strings and BLOB that are expanded into parameters in the output of
>  [sqlite3\_trace()](c3ref/profile.html) is limited to *N* bytes.


**SQLITE\_TRUSTED\_SCHEMA\=*\<0 or 1\>***


> This macro determines the default value for the
>  [SQLITE\_DBCONFIG\_TRUSTED\_SCHEMA](c3ref/c_dbconfig_defensive.html#sqlitedbconfigtrustedschema) and [PRAGMA trusted\_schema](pragma.html#pragma_trusted_schema) setting.
>  If no alternative is specified, the trusted\-schema setting defaults
>  to ON (a value of 1\) for legacy compatibility. However, for best
>  security, systems that implement
>  [application\-defined SQL functions](appfunc.html) and/or [virtual tables](vtab.html) should
>  consider changing the default to OFF.


**SQLITE\_USE\_URI**


> This option causes the [URI filename](uri.html) process logic to be enabled by
>  default.



# 7\.  Options To Enable Features Normally Turned Off



**SQLITE\_ALLOW\_URI\_AUTHORITY**


> [URI filenames](uri.html) normally throws an error if the authority section is
>  not either empty or "localhost". However, if SQLite is compiled with
>  the SQLITE\_ALLOW\_URI\_AUTHORITY compile\-time option, then the URI is
>  converted into a Uniform Naming Convention (UNC) filename and passed
>  down to the underlying operating system that way.
>  
>  Some future versions of SQLite may change to enable this feature
>  by default.


**SQLITE\_ALLOW\_COVERING\_INDEX\_SCAN\=*\<0 or 1\>***


> This C\-preprocess macro determines the default setting of the
>  [SQLITE\_CONFIG\_COVERING\_INDEX\_SCAN](c3ref/c_config_covering_index_scan.html#sqliteconfigcoveringindexscan) configuration setting. It defaults
>  to 1 (on) which means that covering indices are used for full table
>  scans where possible, in order to reduce I/O and improve performance.
>  However, the use of a covering index for a full scan will cause results
>  to appear in a different order from legacy, which could cause some
>  (incorrectly\-coded) legacy applications to break. Hence, the covering
>  index scan option can be disabled at compile\-time on systems that what
>  to minimize their risk of exposing errors in legacy applications.


**SQLITE\_ENABLE\_8\_3\_NAMES\=*\<1 or 2\>***


> If this C\-preprocessor macro is defined, then extra code is
>  included that allows SQLite to function on a filesystem that
>  only support 8\+3 filenames. If the value of this macro is 1,
>  then the default behavior is to continue to use long filenames and
>  to only use 8\+3 filenames if the
>  database connection is opened using [URI filenames](uri.html) with
>  the "8\_3\_names\=1" query parameter. If the value of
>  this macro is 2, then the use of 8\+3 filenames becomes the default
>  but may be disabled on using the 8\_3\_names\=0 query parameter.


**SQLITE\_ENABLE\_API\_ARMOR**


> When defined, this C\-preprocessor macro activates extra code that
>  attempts to detect misuse of the SQLite API, such as passing in NULL
>  pointers to required parameters or using objects after they have been
>  destroyed. When this option is enabled and an illegal API usage
>  is detected, the interface will typically return SQLITE\_MISUSE.
>  
>  The SQLITE\_ENABLE\_API\_ARMOR option does not guarantee that all
>  illegal API usages will be detected. Even when
>  SQLITE\_ENABLE\_API\_ARMOR is enabled, passing incorrect values
>  into the C\-language APIs can cause a process crash due to segmentation
>  fault or null\-pointer deference or other reasons. The
>  SQLITE\_ENABLE\_API\_ARMOR compile\-time option is intended as an aid
>  for application testing and debugging option. Applications
>  should not depend SQLITE\_ENABLE\_API\_ARMOR for safety.
>  SQLITE\_ENABLE\_API\_ARMOR is appropriate as a second line of
>  defense against application bugs, but it should not be the only
>  defense. If any SQLite interface returns SQLITE\_MISUSE, that
>  indicates that the application is using SQLite contrary to
>  the spec and that the application contains a bug. The SQLITE\_MISUSE
>  return provides the application with the opportunity to respond
>  gracefully to that bug, rather than simply crashing the process or
>  invoking undefined behavior, but nothing more. Applications should
>  neither make use of nor depend upon SQLITE\_MISUSE for routine processing.


**SQLITE\_ENABLE\_ATOMIC\_WRITE**


> If this C\-preprocessor macro is defined and if the
>  xDeviceCharacteristics method of [sqlite3\_io\_methods](c3ref/io_methods.html) object for
>  a database file reports (via one of the [SQLITE\_IOCAP\_ATOMIC](c3ref/c_iocap_atomic.html) bits)
>  that the filesystem supports atomic writes and if a transaction
>  involves a change to only a single page of the database file,
>  then the transaction commits with just a single write request of
>  a single page of the database and no rollback journal is created
>  or written. On filesystems that support atomic writes, this
>  optimization can result in significant speed improvements for
>  small updates. However, few filesystems support this capability
>  and the code paths that check for this capability slow down write
>  performance on systems that lack atomic write capability, so this
>  feature is disabled by default.


**SQLITE\_ENABLE\_BATCH\_ATOMIC\_WRITE**


> This compile\-time option enables SQLite to take advantage batch
>  atomic write capabilities in the underlying filesystem. As of
>  SQLite version 3\.21\.0 (2017\-10\-24\) this is only supported on
>  [F2FS](https://en.wikipedia.org/wiki/F2FS). However, the interface
>  is implemented generically, using [sqlite3\_file\_control()](c3ref/file_control.html) with
>  [SQLITE\_FCNTL\_BEGIN\_ATOMIC\_WRITE](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlbeginatomicwrite) and [SQLITE\_FCNTL\_COMMIT\_ATOMIC\_WRITE](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlcommitatomicwrite)
>  so the capability can be added to other filesystem times in the
>  future. When this option is enabled, SQLite automatically detects
>  that the underlying filesystem supports batch atomic writes, and
>  when it does so it avoids writing the [rollback journal](lockingv3.html#rollback) for transaction
>  control. This can make transactions over twice as fast, while
>  simultaneously reducing wear on SSD storage devices.
> 
>  Future versions of SQLite might enable the batch\-atomic\-write
>  capability by default, at which point this compile\-time option
>  will become superfluous.


**SQLITE\_ENABLE\_BYTECODE\_VTAB**


> This option enables the [bytecode and tables\_used virtual tables](bytecodevtab.html).


**SQLITE\_ENABLE\_COLUMN\_METADATA**


> When this C\-preprocessor macro is defined, SQLite includes some
>  additional APIs that provide convenient access to meta\-data about
>  tables and queries. The APIs that are enabled by this option are:
> 
> 
>  * [sqlite3\_column\_database\_name()](c3ref/column_database_name.html)
> * [sqlite3\_column\_database\_name16()](c3ref/column_database_name.html)
> * [sqlite3\_column\_table\_name()](c3ref/column_database_name.html)
> * [sqlite3\_column\_table\_name16()](c3ref/column_database_name.html)
> * [sqlite3\_column\_origin\_name()](c3ref/column_database_name.html)
> * [sqlite3\_column\_origin\_name16()](c3ref/column_database_name.html)


**SQLITE\_ENABLE\_DBPAGE\_VTAB**


> This option enables the [SQLITE\_DBPAGE virtual table](dbpage.html).


**SQLITE\_ENABLE\_DBSTAT\_VTAB**


> This option enables the [dbstat virtual table](dbstat.html).


**SQLITE\_ENABLE\_DESERIALIZE**


> This option was formerly used to enable
>  the [sqlite3\_serialize()](c3ref/serialize.html) and [sqlite3\_deserialize()](c3ref/deserialize.html)
>  interfaces. However, as of SQLite 3\.36\.0 (2021\-06\-18\)
>  those interfaces are enabled by default and a new
>  compile\-time option [SQLITE\_OMIT\_DESERIALIZE](compile.html#omit_deserialize) is added
>  to omit them.


**SQLITE\_ENABLE\_EXPLAIN\_COMMENTS**


> This option adds extra logic to SQLite that inserts comment text into the
>  output of [EXPLAIN](lang_explain.html). These extra comments use extra memory, thus
>  making [prepared statements](c3ref/stmt.html) larger and very slightly slower, and so they are
>  turned off by default and in most application. But some applications, such
>  as the [command\-line shell](cli.html) for SQLite, value clarity of EXPLAIN output
>  over raw performance and so this compile\-time option is available to them.
>  The SQLITE\_ENABLE\_EXPLAIN\_COMMENTS compile\-time option is also enabled
>  automatically if [SQLITE\_DEBUG](compile.html#debug) is enabled.


**SQLITE\_ENABLE\_FTS3**


> When this option is defined in the [amalgamation](amalgamation.html), versions 3 and 4
>  of the full\-text search engine are added to the build automatically.


**SQLITE\_ENABLE\_FTS3\_PARENTHESIS**


> This option modifies the query pattern parser in FTS3 such that it
>  supports operators AND and NOT (in addition to the usual OR and NEAR)
>  and also allows query expressions to contain nested parenthesis.


**SQLITE\_ENABLE\_FTS3\_TOKENIZER**


> This option enables the two\-argument version of the [fts3\_tokenizer()](fts3.html#f3tknzr)
>  interface. The second argument to fts3\_tokenizer() is suppose to be a
>  pointer to a function (encoded as a BLOB) that implements an
>  application defined tokenizer. If hostile actors are able to run
>  the two\-argument version of fts3\_tokenizer() with an arbitrary second
>  argument, they could use crash or take control of the process.
>  
>  Because of security concerns, the two\-argument fts3\_tokenizer() feature
>  was disabled beginning with [Version 3\.11\.0](releaselog/3_11_0.html) (2016\-02\-15\)
>  unless this compile\-time option is used.
>  [Version 3\.12\.0](releaselog/3_12_0.html) (2016\-03\-29\) added the
>  [sqlite3\_db\_config](c3ref/db_config.html)(db,[SQLITE\_DBCONFIG\_ENABLE\_FTS3\_TOKENIZER](c3ref/c_dbconfig_defensive.html#sqlitedbconfigenablefts3tokenizer),1,0\) interface
>  that activates the two\-argument version of [fts3\_tokenizer()](fts3.html#f3tknzr)
>  for a specific [database connection](c3ref/sqlite3.html) at run\-time.


**SQLITE\_ENABLE\_FTS4**


> When this option is defined in the [amalgamation](amalgamation.html), versions 3 and 4
>  of the full\-text search engine are added to the build automatically.


**SQLITE\_ENABLE\_FTS5**


> When this option is defined in the [amalgamation](amalgamation.html), versions 5
>  of the full\-text search engine ([fts5](fts5.html)) is added to the build automatically.


**SQLITE\_ENABLE\_GEOPOLY**


> When this option is defined in the [amalgamation](amalgamation.html), the [Geopoly extension](geopoly.html)
>  is included in the build.


**SQLITE\_ENABLE\_HIDDEN\_COLUMNS**


> When this option is defined in the [amalgamation](amalgamation.html),
>  The [hidden columns](vtab.html#hiddencol) feature is enabled for virtual tables.


**SQLITE\_ENABLE\_ICU**


> This option causes the
>  [International Components for Unicode](https://icu.unicode.org)
>  or "ICU" extension to SQLite to be added to the build.


**SQLITE\_ENABLE\_IOTRACE**


> When both the SQLite core and the [Command Line Interface](cli.html) (CLI) are both
>  compiled with this option, then the CLI provides an extra command
>  named ".iotrace" that provides a low\-level log of I/O activity.
>  This option is experimental and may be discontinued in a future release.


**SQLITE\_ENABLE\_MATH\_FUNCTIONS**


> This macro enables the [built\-in SQL math functions](lang_mathfunc.html). This option
>  is automatically added to the Makefile by the configure script on unix platforms,
>  unless the \-\-disable\-math option is used.
>  This option is also included on Windows builds using the
>  "Makefile.msc" makefile for nmake.


**SQLITE\_ENABLE\_JSON1**


> This compile\-time option is a no\-op. Prior to SQLite version 3\.38\.0
>  (2022\-02\-22\), it was necessary to compile with this option in order
>  to include the [JSON SQL functions](json1.html) in the build. However, beginning
>  with SQLite version 3\.38\.0, those functions are included by default.
>  Use the [\-DSQLITE\_OMIT\_JSON](compile.html#omit_json) option to omit them.


**SQLITE\_ENABLE\_LOCKING\_STYLE**


> This option enables additional logic in the OS interface layer for
>  Mac OS X. The additional logic attempts to determine the type of the
>  underlying filesystem and choose and alternative locking strategy
>  that works correctly for that filesystem type. Five locking strategies
>  are available:
> 
> 
>  * POSIX locking style. This is the default locking style and the
>  style used by other (non Mac OS X) Unixes. Locks are obtained and
>  released using the fcntl() system call.
> 
> 
> 
>  - AFP locking style. This locking style is used for network file
>  systems that use the AFP (Apple Filing Protocol) protocol. Locks
>  are obtained by calling the library function \_AFPFSSetLock().
> 
> 
> 
>  - Flock locking style. This is used for file\-systems that do not
>  support POSIX locking style. Locks are obtained and released using
>  the flock() system call.
> 
> 
> 
>  - Dot\-file locking style. This locking style is used when neither
>  flock nor POSIX locking styles are supported by the file system.
>  Database locks are obtained by creating and entry in the file\-system
>  at a well\-known location relative to the database file (a "dot\-file")
>  and relinquished by deleting the same file.
> 
> 
> 
>  - No locking style. If none of the above can be supported, this
>  locking style is used. No database locking mechanism is used. When
>  this system is used it is not safe for a single database to be
>  accessed by multiple clients.
> 
> 
> 
>  Additionally, five extra [VFS](vfs.html) implementations are provided as well as the
>  default. By specifying one of the extra VFS implementations
>  when calling [sqlite3\_open\_v2()](c3ref/open.html), an application may bypass the file\-system
>  detection logic and explicitly select one of the above locking styles. The
>  five extra [VFS](vfs.html) implementations are called "unix\-posix", "unix\-afp",
>  "unix\-flock", "unix\-dotfile" and "unix\-none".


**SQLITE\_ENABLE\_MEMORY\_MANAGEMENT**


> This option adds extra logic to SQLite that allows it to release unused
>  memory upon request. This option must be enabled in order for the
>  [sqlite3\_release\_memory()](c3ref/release_memory.html) interface to work. If this compile\-time
>  option is not used, the [sqlite3\_release\_memory()](c3ref/release_memory.html) interface is a
>  no\-op.


**SQLITE\_ENABLE\_MEMSYS3**


> This option includes code in SQLite that implements an alternative
>  memory allocator. This alternative memory allocator is only engaged
>  when the [SQLITE\_CONFIG\_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap) option to [sqlite3\_config()](c3ref/config.html) is used to
>  supply a large chunk of memory from which all memory allocations are
>  taken.
>  The MEMSYS3 memory allocator uses a hybrid allocation algorithm
>  patterned after dlmalloc(). Only one of SQLITE\_ENABLE\_MEMSYS3 and
>  SQLITE\_ENABLE\_MEMSYS5 may be enabled at once.


**SQLITE\_ENABLE\_MEMSYS5**


> This option includes code in SQLite that implements an alternative
>  memory allocator. This alternative memory allocator is only engaged
>  when the [SQLITE\_CONFIG\_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap) option to [sqlite3\_config()](c3ref/config.html) is used to
>  supply a large chunk of memory from which all memory allocations are
>  taken.
>  The MEMSYS5 module rounds all allocations up to the next power
>  of two and uses a first\-fit, buddy\-allocator algorithm
>  that provides strong guarantees against fragmentation and breakdown
>  subject to certain operating constraints.


**SQLITE\_ENABLE\_NORMALIZE**


> This option includes the [sqlite3\_normalized\_sql()](c3ref/expanded_sql.html) API.


**SQLITE\_ENABLE\_NULL\_TRIM**


> This option enables an optimization that omits NULL columns at
>  the ends of rows, for a space savings on disk.
>  
>  Databases generated with this option enabled are not readable
>  by SQLite version 3\.1\.6 (2005\-03\-17\) and earlier. Also,
>  databases generated with this option enabled are prone to
>  triggering the
>  [e6e962d6b0f06f46](https://www.sqlite.org/src/info/e6e962d6b0f06f46e)
>  bug in the [sqlite3\_blob\_reopen()](c3ref/blob_reopen.html) interface. For those reasons,
>  this optimization is disabled by default. However, this optimization
>  may be enabled by default in a future release of SQLite.


**SQLITE\_ENABLE\_OFFSET\_SQL\_FUNC**


> This option enables support for the [sqlite\_offset(X)](lang_corefunc.html#sqlite_offset) SQL function.
>  
>  The [sqlite\_offset(X)](lang_corefunc.html#sqlite_offset) SQL function requires a new interface on the
>  B\-tree storage engine, a new opcode in the [virtual machine](opcode.html) that
>  runs SQL statements, and a new conditional in a critical path of the
>  code generator. To avoid that overhead in applications that do not
>  need the utility of sqlite\_offset(X), the function is disabled by
>  default.


**SQLITE\_ENABLE\_PREUPDATE\_HOOK**


> This option enables
>  [several new APIs](c3ref/preupdate_blobwrite.html) that provide callbacks
>  prior to any change to a [rowid table](rowidtable.html). The callbacks can be used
>  to record the state of the row before the change occurs.
>  The action of the preupdate hook is similar to the
>  [update hook](c3ref/update_hook.html) except that the callback is
>  invoked before the change, not afterwards, and the preupdate
>  hook interfaces are omitted unless this compile\-time option is
>  used.
>  The preupdate hook interfaces were originally added to
>  support the [session](sessionintro.html) extension.


**SQLITE\_ENABLE\_QPSG**


> This option causes the [query planner stability guarantee](queryplanner-ng.html#qpstab) (QPSG) to
>  be on by default. Normally the QPSG is off and must be activated
>  at run\-time using the [SQLITE\_DBCONFIG\_ENABLE\_QPSG](c3ref/c_dbconfig_defensive.html#sqlitedbconfigenableqpsg) option to the
>  [sqlite3\_db\_config()](c3ref/db_config.html) interface.


**SQLITE\_ENABLE\_RBU**


> Enable the code the implements the [RBU extension](rbu.html).


**SQLITE\_ENABLE\_RTREE**


> This option causes SQLite to include support for the
>  [R\*Tree index extension](rtree.html).


**SQLITE\_ENABLE\_SESSION**


> This option enables the [session extension](sessionintro.html).


**SQLITE\_ENABLE\_SNAPSHOT**


> This option enables the code to support the [sqlite3\_snapshot](c3ref/snapshot.html) object
>  and its related interfaces:
>  * [sqlite3\_snapshot\_get()](c3ref/snapshot_get.html) (constructor)
>  * [sqlite3\_snapshot\_free()](c3ref/snapshot_free.html) (destructor)
>  * [sqlite3\_snapshot\_open()](c3ref/snapshot_open.html)* [sqlite3\_snapshot\_cmp()](c3ref/snapshot_cmp.html)* [sqlite3\_snapshot\_recover()](c3ref/snapshot_recover.html)


**SQLITE\_ENABLE\_SORTER\_REFERENCES**


> This option activates an optimization that reduces the memory required
>  by the sorter at the cost of doing additional B\-tree lookups after
>  the sort has occurred.
>  
>  The default sorting procedure is to gather all information that will
>  ultimately be output into a "record" and pass that complete record
>  to the sorter. But in some cases, for example if some of the output
>  columns consists of large BLOB values, the size of the each record
>  can be large, which means that the sorter has to either use more memory,
>  and/or write more content to temporary storage.
>  
>  When SQLITE\_ENABLE\_SORTER\_REFERENCES is enabled, the records passed to
>  the sorter often contain only a [ROWID](lang_createtable.html#rowid) value. Such records are much
>  smaller. This means the sorter has much less "payload" to deal with and
>  can run faster. After sorting has occurred, the ROWID is used to look up
>  the output column values in the original table. That requires another
>  search into the table, and could potentially result in a slowdown. Or,
>  it might be a performance win, depending on how large the values are.
>  
>  Even when the SQLITE\_ENABLE\_SORTER\_REFERENCES compile\-time option is on,
>  sorter references are still disabled by default. To use sorter references,
>  the application must set a sorter reference size threshold using the
>  [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_SORTERREF\_SIZE](c3ref/c_config_covering_index_scan.html#sqliteconfigsorterrefsize)) interface at start\-time.
>  
>  Because the SQLite developers do not know whether the
>  SQLITE\_ENABLE\_SORTER\_REFERENCES option will help or hurt performance,
>  it is disabled by default at this time (2018\-05\-04\). It might be enabled
>  by default in some future release, depending on what is learned about its
>  impact on performance.


**SQLITE\_ENABLE\_STMT\_SCANSTATUS**


> This option enables the [sqlite3\_stmt\_scanstatus()](c3ref/stmt_scanstatus.html) and
>  [sqlite3\_stmt\_scanstatus\_v2()](c3ref/stmt_scanstatus.html) interfaces. Those
>  interfaces are normally omitted from the build
>  because they imposes a performance penalty, even on statements that
>  do not use the feature.


**SQLITE\_ENABLE\_STMTVTAB**


> This compile\-time option enables the [SQLITE\_STMT virtual table](stmt.html) logic.


**SQLITE\_RTREE\_INT\_ONLY**


> This compile\-time option is deprecated and untested.


**SQLITE\_ENABLE\_SQLLOG**


> This option enables extra code (especially the [SQLITE\_CONFIG\_SQLLOG](c3ref/c_config_covering_index_scan.html#sqliteconfigsqllog)
>  option to [sqlite3\_config()](c3ref/config.html)) that can be used to create logs of all
>  SQLite processing performed by an application. These logs can be useful
>  in doing off\-line analysis of the behavior of an application, and especially
>  for performance analysis. In order for the SQLITE\_ENABLE\_SQLLOG option to
>  be useful, some extra code is required. The
>  ["test\_sqllog.c"](https://www.sqlite.org/src/doc/trunk/src/test_sqllog.c)
>  source code
>  file in the SQLite source tree is a working example of the required extra
>  code. On unix and windows systems, a developer can append the text of the
>  "test\_sqllog.c" source code file to the end of an "sqlite3\.c" amalgamation,
>  recompile the application using the \-DSQLITE\_ENABLE\_SQLLOG option, then
>  control logging using environment variables. See the header comment on
>  the "test\_sqllog.c" source file for additional detail.


**SQLITE\_ENABLE\_STAT2**


> This option used to cause the [ANALYZE](lang_analyze.html) command to collect
>  index histogram data in the **sqlite\_stat2** table. But that
>  functionality was superseded by [SQLITE\_ENABLE\_STAT3](compile.html#enable_stat3) as of
>  SQLite [version 3\.7\.9](releaselog/3_7_9.html) (2011\-11\-01\).
>  The SQLITE\_ENABLE\_STAT2 compile\-time option
>  is now a no\-op.


**SQLITE\_ENABLE\_STAT3**


> This option used to cause the [ANALYZE](lang_analyze.html) command to collect
>  index histogram data in the **sqlite\_stat3** table. But that
>  functionality was superseded by [SQLITE\_ENABLE\_STAT4](compile.html#enable_stat4) as of
>  SQLite [version 3\.8\.1](releaselog/3_8_1.html) (2013\-10\-17\).
>  The SQLITE\_ENABLE\_STAT3 compile\-time option
>  continued to be supported through [version 3\.29\.0](releaselog/3_29_0.html) (2019\-07\-10\)
>  but has now become a no\-op.


**SQLITE\_ENABLE\_STAT4**


> This option adds additional logic to the [ANALYZE](lang_analyze.html) command and to
>  the [query planner](optoverview.html) that can help SQLite to chose a better query plan
>  under certain situations. The [ANALYZE](lang_analyze.html) command is enhanced to collect
>  histogram data from all columns of every index and store that data
>  in the [sqlite\_stat4](fileformat2.html#stat4tab) table. The query planner will then use the
>  histogram data to help it make better index choices. The downside of
>  this compile\-time option is that it violates the
>  [query planner stability guarantee](queryplanner-ng.html#qpstab) making it more difficult to ensure
>  consistent performance in mass\-produced applications.
>  
>  SQLITE\_ENABLE\_STAT4 is an enhancement of [SQLITE\_ENABLE\_STAT3](compile.html#enable_stat3). STAT3
>  only recorded histogram data for the left\-most column of each index
>  whereas the STAT4 enhancement records histogram data from all columns
>  of each index.
>  The [SQLITE\_ENABLE\_STAT3](compile.html#enable_stat3) compile\-time option has become a no\-op.


**SQLITE\_ENABLE\_TREE\_EXPLAIN**


> This compile\-time option is no longer used.


**SQLITE\_ENABLE\_UPDATE\_DELETE\_LIMIT**


> This option enables an optional ORDER BY and LIMIT clause on
>  [UPDATE](lang_update.html) and [DELETE](lang_delete.html) statements.
> 
> 
>  If this option is defined, then it must also be
>  defined when using the [Lemon parser generator](lemon.html) tool to generate a parse.c
>  file. Because of this, this option may only be used when the library is built
>  from source, not from the [amalgamation](amalgamation.html) or from the collection of
>  pre\-packaged C files provided for non\-Unix like platforms on the website.


**SQLITE\_ENABLE\_UNKNOWN\_SQL\_FUNCTION**


> When the SQLITE\_ENABLE\_UNKNOWN\_SQL\_FUNCTION compile\-time option is
>  activated, SQLite will suppress "unknown function" errors when running
>  an [EXPLAIN](lang_explain.html) or [EXPLAIN QUERY PLAN](eqp.html). Instead of throwing an error,
>  SQLite will insert a substitute no\-op function named "unknown()".
>  The substitution of "unknown()" in place of unrecognized functions
>  only occurs on [EXPLAIN](lang_explain.html) and [EXPLAIN QUERY PLAN](eqp.html), not on ordinary
>  statements.
>  
>  When used in the [command\-line shell](cli.html), the
>  SQLITE\_ENABLE\_UNKNOWN\_SQL\_FUNCTION feature allows SQL text that contains
>  application\-defined functions to be pasted into the shell for
>  analysis and debugging without having to create and load an
>  extension that implements the application\-defined functions.


**SQLITE\_ENABLE\_UNLOCK\_NOTIFY**


> This option enables the [sqlite3\_unlock\_notify()](c3ref/unlock_notify.html) interface and
>  its associated functionality. See the documentation titled
>  [Using the SQLite Unlock Notification Feature](unlock_notify.html) for additional
>  information.


**SQLITE\_INTROSPECTION\_PRAGMAS**


> This option is obsolete. It used to enable some extra
>  some extra PRAGMA statements such as
>  [PRAGMA function\_list](pragma.html#pragma_function_list), [PRAGMA module\_list](pragma.html#pragma_module_list), and
>  [PRAGMA pragma\_list](pragma.html#pragma_pragma_list), but those pragmas are now all
>  enabled by default. See [SQLITE\_OMIT\_INTROSPECTION\_PRAGMAS](compile.html#omit_introspection_pragmas).


**SQLITE\_SOUNDEX**


> This option enables the [soundex() SQL function](lang_corefunc.html#soundex).


**SQLITE\_STRICT\_SUBTYPE\=1**


> This option causes [application\-defined SQL functions](appfunc.html) to raise an SQL
>  error if they invoke the [sqlite3\_result\_subtype()](c3ref/result_subtype.html) interface but
>  where not registered with the [SQLITE\_RESULT\_SUBTYPE](c3ref/c_deterministic.html#sqliteresultsubtype) property.
>  This recommended option helps to identify problems in the
>  implementation of application\-defined SQL functions early in the
>  development cycle.


**SQLITE\_USE\_ALLOCA**


> If this option is enabled, then the alloca() memory allocator will be
>  used in a few situations where it is appropriate. This results in a slightly
>  smaller and faster binary. The SQLITE\_USE\_ALLOCA compile\-time only
>  works, of course, on systems that support alloca().


**SQLITE\_USE\_FCNTL\_TRACE**


> This option causes SQLite to issue extra [SQLITE\_FCNTL\_TRACE](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntltrace) file controls
>  to provide supplementary information to the VFS. The "vfslog.c" extension
>  makes use of this to provide enhanced logs of VFS activity.


**SQLITE\_USE\_SEH**


> This option enabled Structured Exception Handling (SEH) on Windows builds.
>  SEH is a Windows\-specific technique for catching exceptions raised while
>  accessing a memory\-mapped file. SEH is used to intercept errors that might
>  occur while accessing the memory\-mapped [shm file](walformat.html#shm) that are part of
>  [WAL mode](wal.html) processing. If the operating system raised errors while SQLite
>  is trying to access the shm file, this option causes those errors to be
>  caught and dealt with by SQLite, rather than aborting the whole process.
>  
>  This option only works when compiling on Windows using MSVC.


**SQLITE\_HAVE\_ZLIB**


> This option causes some extensions to link against the
>  [zlib compression library](https://zlib.net).
>  
>  This option has no effect on the SQLite core. It is only used by extensions.
>  This is option is necessary for the compression and decompression
>  functions that are part of [SQL Archive](sqlar.html) support in the
>  [command\-line shell](cli.html).
>  
>  When compiling with this option, it will normally
>  be necessary to add a linker option to include the zlib library in the
>  build. Normal this option is "\-lz" but might be different on different
>  systems.
>  
>  When building with MSVC on Windows systems, one can put the zlib source
>  code in the compat/zlib subdirectory of the source tree and then add
>  the USE\_ZLIB\=1 option to the nmake command to cause the Makefile.msc
>  to automatically build and use an appropriate zlib library implementation.


**YYTRACKMAXSTACKDEPTH**


> This option causes the LALR(1\) parser stack depth to be tracked
>  and reported using the [sqlite3\_status](c3ref/status.html)([SQLITE\_STATUS\_PARSER\_STACK](c3ref/c_status_malloc_count.html#sqlitestatusparserstack),...)
>  interface. SQLite's LALR(1\) parser has a fixed stack depth
>  (determined at compile\-time using the [YYSTACKDEPTH](compile.html#yystackdepth) options).
>  This option can be used to help determine if an application is
>  getting close to exceeding the maximum LALR(1\) stack depth.



# 8\.  Options To Disable Features Normally Turned On



**SQLITE\_DISABLE\_LFS**


> If this C\-preprocessor macro is defined, large file support
>  is disabled.


**SQLITE\_DISABLE\_DIRSYNC**


> If this C\-preprocessor macro is defined, directory syncs
>  are disabled. SQLite typically attempts to sync the parent
>  directory when a file is deleted to ensure the directory
>  entries are updated immediately on disk.


**SQLITE\_DISABLE\_FTS3\_UNICODE**


> If this C\-preprocessor macro is defined, the [unicode61](fts3.html#unicode61) tokenizer
>  in [FTS3](fts3.html) is omitted from the build and is unavailable to
>  applications.


**SQLITE\_DISABLE\_FTS4\_DEFERRED**


> If this C\-preprocessor macro disables the "deferred token" optimization
>  in [FTS4](fts3.html#fts4). The "deferred token" optimization avoids loading massive
>  posting lists for terms that are in most documents of the collection
>  and instead simply scans for those tokens in the document source. [FTS4](fts3.html#fts4)
>  should get exactly the same answer both with and without this optimization.


**SQLITE\_DISABLE\_INTRINSIC**


> This option disables the use of compiler\-specific built\-in functions
>  such as \_\_builtin\_bswap32() and \_\_builtin\_add\_overflow() in GCC and Clang,
>  or \_byteswap\_ulong() and \_ReadWriteBarrier() with MSVC.


**SQLITE\_DISABLE\_PAGECACHE\_OVERFLOW\_STATS**


> This option disables the collection of the [sqlite3\_status()](c3ref/status.html)
> [SQLITE\_STATUS\_PAGECACHE\_OVERFLOW](c3ref/c_status_malloc_count.html#sqlitestatuspagecacheoverflow) and [SQLITE\_STATUS\_PAGECACHE\_SIZE](c3ref/c_status_malloc_count.html#sqlitestatuspagecachesize)
>  statistics. Setting this option has been shown to increase performance in
>  high concurrency multi\-threaded applications.



# 9\.  Options To Omit Features


The following options can be used to
[reduce the size of the compiled library](footprint.html)
by omitting unused features. This is probably only useful
in embedded systems where space is especially tight, as even with all
features included the SQLite library is relatively small. Don't forget
to tell your compiler to optimize for binary size! (the \-Os option if
using GCC). Telling your compiler to optimize for size usually has
a much larger impact on library footprint than employing any of these
compile\-time options. You should also verify that
[debugging options](#debugoptions) are disabled.


The macros in this section do not require values. The following
compilation switches all have the same effect:  

\-DSQLITE\_OMIT\_ALTERTABLE  

\-DSQLITE\_OMIT\_ALTERTABLE\=1  

\-DSQLITE\_OMIT\_ALTERTABLE\=0



If any of these options are defined, then the same set of SQLITE\_OMIT\_\*
options must also be defined when using the [Lemon parser generator](lemon.html)
tool to generate the
parse.c file and when compiling the 'mkkeywordhash' tool which generates
the keywordhash.h file.
Because of this, these options may only be used when the library is built
from canonical source, not from the [amalgamation](amalgamation.html).
Some SQLITE\_OMIT\_\* options might work, or appear to work, when used with
the [amalgamation](amalgamation.html). But this is not guaranteed. In general, always compile
from canonical sources in order to take advantage of SQLITE\_OMIT\_\* options.




> ***Important Note:** The SQLITE\_OMIT\_\* options may not work with the
> [amalgamation](amalgamation.html). SQLITE\_OMIT\_\* compile\-time
> options usually work correctly only when SQLite is built from canonical
> source files.*


Special versions of the SQLite amalgamation that do work with a
predetermined set of SQLITE\_OMIT\_\* options can be generated. To do so,
make a copy of the Makefile.linux\-gcc makefile template in the canonical
source code distribution. Change the name of your copy to simply "Makefile".
Then edit "Makefile" to set up appropriate compile\-time options. Then
type:



```
make clean; make sqlite3.c

```

The resulting "sqlite3\.c" amalgamation code file (and its associated
header file "sqlite3\.h") can then be moved to a non\-unix platform
for final compilation using a native compiler.


The SQLITE\_OMIT\_\* options are unsupported. By this we mean that
an SQLITE\_OMIT\_\* option that omits code from the build in the current
release might become a no\-op in the next release. Or the other way around:
an SQLITE\_OMIT\_\* that is a no\-op in the current release might cause code
to be excluded in the next release. Also, not all SQLITE\_OMIT\_\* options
are tested. Some SQLITE\_OMIT\_\* options might cause SQLite to malfunction
and/or provide incorrect answers.




> ***Important Note:**
> The SQLITE\_OMIT\_\* compile\-time options are mostly unsupported.*


The following are the available OMIT options:


**SQLITE\_OMIT\_ALTERTABLE**


> When this option is defined, the
>  [ALTER TABLE](lang_altertable.html) command is not included in the
>  library. Executing an [ALTER TABLE](lang_altertable.html) statement causes a parse error.


**SQLITE\_OMIT\_ANALYZE**


> When this option is defined, the [ANALYZE](lang_analyze.html) command is omitted from
>  the build.


**SQLITE\_OMIT\_ATTACH**


> When this option is defined, the [ATTACH](lang_attach.html) and [DETACH](lang_detach.html) commands are
>  omitted from the build.


**SQLITE\_OMIT\_AUTHORIZATION**


> Defining this option omits the authorization callback feature from the
>  library. The [sqlite3\_set\_authorizer()](c3ref/set_authorizer.html) API function is not present
>  in the library.


**SQLITE\_OMIT\_AUTOINCREMENT**


> This option is omits the [AUTOINCREMENT](autoinc.html) feature.
>  When this is macro is defined, columns declared as
>  "[INTEGER PRIMARY KEY](lang_createtable.html#rowid) AUTOINCREMENT"
>  behave in the same way as columns declared as "[INTEGER PRIMARY KEY](lang_createtable.html#rowid)" when a
>  NULL is inserted. The sqlite\_sequence system table is neither created, nor
>  respected if it already exists.


**SQLITE\_OMIT\_AUTOINIT**


> For backwards compatibility with older versions of SQLite that lack
>  the [sqlite3\_initialize()](c3ref/initialize.html) interface, the [sqlite3\_initialize()](c3ref/initialize.html) interface
>  is called automatically upon entry to certain key interfaces such as
>  [sqlite3\_open()](c3ref/open.html), [sqlite3\_vfs\_register()](c3ref/vfs_find.html), and [sqlite3\_mprintf()](c3ref/mprintf.html).
>  The overhead of invoking [sqlite3\_initialize()](c3ref/initialize.html) automatically in this
>  way may be omitted by building SQLite with the SQLITE\_OMIT\_AUTOINIT
>  C\-preprocessor macro. When built using SQLITE\_OMIT\_AUTOINIT, SQLite
>  will not automatically initialize itself and the application is required
>  to invoke [sqlite3\_initialize()](c3ref/initialize.html) directly prior to beginning use of the
>  SQLite library.


**SQLITE\_OMIT\_AUTOMATIC\_INDEX**


> This option is used to omit the
>  [automatic indexing](optoverview.html#autoindex) functionality.
>  See also: [SQLITE\_DEFAULT\_AUTOMATIC\_INDEX](compile.html#default_automatic_index).


**SQLITE\_OMIT\_AUTORESET**


> By default, the [sqlite3\_step()](c3ref/step.html) interface will automatically invoke
>  [sqlite3\_reset()](c3ref/reset.html) to reset the [prepared statement](c3ref/stmt.html) if necessary. This
>  compile\-time option changes that behavior so that [sqlite3\_step()](c3ref/step.html) will
>  return [SQLITE\_MISUSE](rescode.html#misuse) if it called again after returning anything other
>  than [SQLITE\_ROW](rescode.html#row), [SQLITE\_BUSY](rescode.html#busy), or [SQLITE\_LOCKED](rescode.html#locked) unless there was an
>  intervening call to [sqlite3\_reset()](c3ref/reset.html).
> 
> 
>  In SQLite [version 3\.6\.23\.1](releaselog/3_6_23_1.html) (2010\-03\-26\)
>  and earlier, [sqlite3\_step()](c3ref/step.html) used to always
>  return [SQLITE\_MISUSE](rescode.html#misuse) if it was invoked again after returning anything
>  other than [SQLITE\_ROW](rescode.html#row) without an intervening call to [sqlite3\_reset()](c3ref/reset.html).
>  This caused problems on some poorly written smartphone applications which
>  did not correctly handle the [SQLITE\_LOCKED](rescode.html#locked) and [SQLITE\_BUSY](rescode.html#busy) error
>  returns. Rather than fix the many defective smartphone applications,
>  the behavior of SQLite was changed in 3\.6\.23\.2 to automatically reset
>  the prepared statement. But that changed caused issues in other
>  improperly implemented applications that were actually looking
>  for an [SQLITE\_MISUSE](rescode.html#misuse) return to terminate their query loops. (Anytime
>  an application gets an SQLITE\_MISUSE error code from SQLite, that means the
>  application is misusing the SQLite interface and is thus incorrectly
>  implemented.) The SQLITE\_OMIT\_AUTORESET interface was added to SQLite
>  [version 3\.7\.5](releaselog/3_7_5.html) (2011\-02\-01\) in an effort to get all of the (broken)
>  applications to work again without having to actually fix the applications.


**SQLITE\_OMIT\_AUTOVACUUM**


> If this option is defined, the library cannot create or write to
>  databases that support [auto\_vacuum](pragma.html#pragma_auto_vacuum).
>  Executing a [PRAGMA auto\_vacuum](pragma.html#pragma_auto_vacuum) statement is not an error
>  (since unknown PRAGMAs are silently ignored), but does not return a value
>  or modify the auto\-vacuum flag in the database file. If a database that
>  supports auto\-vacuum is opened by a library compiled with this option, it
>  is automatically opened in read\-only mode.


**SQLITE\_OMIT\_BETWEEN\_OPTIMIZATION**


> This option disables the use of indices with WHERE clause terms
>  that employ the BETWEEN operator.


**SQLITE\_OMIT\_BLOB\_LITERAL**


> When this option is defined, it is not possible to specify a blob in
>  an SQL statement using the X'ABCD' syntax.


**SQLITE\_OMIT\_BTREECOUNT**


> This option is no longer used for anything. It is a no\-op.


**SQLITE\_OMIT\_BUILTIN\_TEST**


> This compile\-time option has been renamed to [SQLITE\_UNTESTABLE](compile.html#untestable).


**SQLITE\_OMIT\_CASE\_SENSITIVE\_LIKE\_PRAGMA**


> This compile\-time option disables the [PRAGMA case\_sensitive\_like](pragma.html#pragma_case_sensitive_like)
>  command.


**SQLITE\_OMIT\_CAST**


> This option causes SQLite to omit support for the CAST operator.


**SQLITE\_OMIT\_CHECK**


> This option causes SQLite to omit support for CHECK constraints.
>  The parser will still accept CHECK constraints in SQL statements,
>  they will just not be enforced.


**SQLITE\_OMIT\_COMPILEOPTION\_DIAGS**


> This option is used to omit the compile\-time option diagnostics available
>  in SQLite, including the [sqlite3\_compileoption\_used()](c3ref/compileoption_get.html) and
>  [sqlite3\_compileoption\_get()](c3ref/compileoption_get.html) C/C\+\+ functions, the
>  [sqlite\_compileoption\_used()](lang_corefunc.html#sqlite_compileoption_used) and [sqlite\_compileoption\_get()](lang_corefunc.html#sqlite_compileoption_get) SQL functions,
>  and the [compile\_options pragma](pragma.html#pragma_compile_options).


**SQLITE\_OMIT\_COMPLETE**


> This option causes the [sqlite3\_complete()](c3ref/complete.html) and [sqlite3\_complete16()](c3ref/complete.html)
>  interfaces to be omitted.


**SQLITE\_OMIT\_COMPOUND\_SELECT**


> This option is used to omit the compound [SELECT](lang_select.html) functionality.
>  [SELECT](lang_select.html) statements that use the
>  UNION, UNION ALL, INTERSECT or EXCEPT compound SELECT operators will
>  cause a parse error.
> 
> 
>  An [INSERT](lang_insert.html) statement with multiple values in the VALUES clause is
>  implemented internally as a compound SELECT. Hence, this option also
>  disables the ability to insert more than a single row using an
>  INSERT INTO ... VALUES ... statement.


**SQLITE\_OMIT\_CTE**


> This option causes support for [common table expressions](lang_with.html) to be omitted.


**SQLITE\_OMIT\_DATETIME\_FUNCS**


> If this option is defined, SQLite's built\-in date and time manipulation
>  functions are omitted. Specifically, the SQL functions julianday(), date(),
>  time(), datetime() and strftime() are not available. The default column
>  values CURRENT\_TIME, CURRENT\_DATE and CURRENT\_TIMESTAMP are still available.


**SQLITE\_OMIT\_DECLTYPE**


> This option causes SQLite to omit support for the
>  [sqlite3\_column\_decltype()](c3ref/column_decltype.html) and [sqlite3\_column\_decltype16()](c3ref/column_decltype.html)
>  interfaces.


**SQLITE\_OMIT\_DEPRECATED**


> This option causes SQLite to omit support for interfaces
>  marked as deprecated. This includes
>  [sqlite3\_aggregate\_count()](c3ref/aggregate_count.html),
>  [sqlite3\_expired()](c3ref/aggregate_count.html),
>  [sqlite3\_transfer\_bindings()](c3ref/aggregate_count.html),
>  [sqlite3\_global\_recover()](c3ref/aggregate_count.html),
>  [sqlite3\_thread\_cleanup()](c3ref/aggregate_count.html) and
>  [sqlite3\_memory\_alarm()](c3ref/aggregate_count.html) interfaces and
>  [PRAGMA](pragma.html#syntax) statements [PRAGMA count\_changes](pragma.html#pragma_count_changes),
>  [PRAGMA data\_store\_directory](pragma.html#pragma_data_store_directory),
>  [PRAGMA default\_cache\_size](pragma.html#pragma_default_cache_size),
>  [PRAGMA empty\_result\_callbacks](pragma.html#pragma_empty_result_callbacks),
>  [PRAGMA full\_column\_names](pragma.html#pragma_full_column_names),
>  [PRAGMA short\_column\_names](pragma.html#pragma_short_column_names), and
>  [PRAGMA temp\_store\_directory](pragma.html#pragma_temp_store_directory).


**SQLITE\_OMIT\_DESERIALIZE**


> This option causes the
>  [sqlite3\_serialize()](c3ref/serialize.html) and [sqlite3\_deserialize()](c3ref/deserialize.html)
>  interfaces to be omitted from the build.


**SQLITE\_OMIT\_DISKIO**


> This option omits all support for writing to the disk and forces
>  databases to exist in memory only. This option has not been
>  maintained and probably does not work with newer versions of SQLite.


**SQLITE\_OMIT\_EXPLAIN**


> Defining this option causes the [EXPLAIN](lang_explain.html) command to be omitted from the
>  library. Attempting to execute an [EXPLAIN](lang_explain.html) statement will cause a parse
>  error.


**SQLITE\_OMIT\_FLAG\_PRAGMAS**


> This option omits support for a subset of [PRAGMA](pragma.html#syntax) commands that
>  query and set boolean properties.


**SQLITE\_OMIT\_FLOATING\_POINT**


> This option is used to omit floating\-point number support from the SQLite
>  library. When specified, specifying a floating point number as a literal
>  (i.e. "1\.01") results in a parse error.
> 
> 
>  In the future, this option may also disable other floating point
>  functionality, for example the [sqlite3\_result\_double()](c3ref/result_blob.html),
>  [sqlite3\_bind\_double()](c3ref/bind_blob.html), [sqlite3\_value\_double()](c3ref/value_blob.html) and
>  [sqlite3\_column\_double()](c3ref/column_blob.html) API functions.


**SQLITE\_OMIT\_FOREIGN\_KEY**


> If this option is defined, then [foreign key constraint](foreignkeys.html) syntax is
>  not recognized.


**SQLITE\_OMIT\_GENERATED\_COLUMNS**


> If this option is defined, then [generated column](gencol.html) syntax is
>  not recognized.


**SQLITE\_OMIT\_GET\_TABLE**


> This option causes support for [sqlite3\_get\_table()](c3ref/free_table.html) and
>  [sqlite3\_free\_table()](c3ref/free_table.html) to be omitted.


**SQLITE\_OMIT\_HEX\_INTEGER**


> This option omits support for [hexadecimal integer literals](lang_expr.html#hexint).


**SQLITE\_OMIT\_INCRBLOB**


> This option causes support for [incremental BLOB I/O](c3ref/blob.html)
>  to be omitted.


**SQLITE\_OMIT\_INTEGRITY\_CHECK**


> This option omits support for the [integrity\_check pragma](pragma.html#pragma_integrity_check).


**SQLITE\_OMIT\_INTROSPECTION\_PRAGMAS**


> This option omits support for
>  [PRAGMA function\_list](pragma.html#pragma_function_list), [PRAGMA module\_list](pragma.html#pragma_module_list), and
>  [PRAGMA pragma\_list](pragma.html#pragma_pragma_list).


**SQLITE\_OMIT\_JSON**


> This option omits the [JSON SQL functions](json1.html) from the build.


**SQLITE\_OMIT\_LIKE\_OPTIMIZATION**


> This option disables the ability of SQLite to use indices to help
>  resolve [LIKE](lang_expr.html#like) and [GLOB](lang_expr.html#glob) operators in a WHERE clause.


**SQLITE\_OMIT\_LOAD\_EXTENSION**


> This option omits the entire extension loading mechanism from
>  SQLite, including [sqlite3\_enable\_load\_extension()](c3ref/enable_load_extension.html) and
>  [sqlite3\_load\_extension()](c3ref/load_extension.html) interfaces.


**SQLITE\_OMIT\_LOCALTIME**


> This option omits the "localtime" modifier from the date and time
>  functions. This option is sometimes useful when trying to compile
>  the date and time functions on a platform that does not support the
>  concept of local time.


**SQLITE\_OMIT\_LOOKASIDE**


> This option omits the [lookaside memory allocator](malloc.html#lookaside).


**SQLITE\_OMIT\_MEMORYDB**


> When this is defined, the library does not respect the special database
>  name ":memory:" (normally used to create an [in\-memory database](inmemorydb.html)). If
>  ":memory:" is passed to [sqlite3\_open()](c3ref/open.html), [sqlite3\_open16()](c3ref/open.html), or
>  [sqlite3\_open\_v2()](c3ref/open.html), a file with this name will be
>  opened or created.


**SQLITE\_OMIT\_OR\_OPTIMIZATION**


> This option disables the ability of SQLite to use an index together
>  with terms of a WHERE clause connected by the OR operator.


**SQLITE\_OMIT\_PAGER\_PRAGMAS**


> Defining this option omits pragmas related to the pager subsystem from
>  the build.


**SQLITE\_OMIT\_PRAGMA**


> This option is used to omit the [PRAGMA](pragma.html#syntax) command
>  from the library. Note that it is useful to define the macros that omit
>  specific pragmas in addition to this, as they may also remove supporting code
>  in other sub\-systems. This macro removes the [PRAGMA](pragma.html#syntax) command only.


**SQLITE\_OMIT\_PROGRESS\_CALLBACK**


> This option may be defined to omit the capability to issue "progress"
>  callbacks during long\-running SQL statements. The
>  [sqlite3\_progress\_handler()](c3ref/progress_handler.html)
>  API function is not present in the library.


**SQLITE\_OMIT\_QUICKBALANCE**


> This option omits an alternative, faster B\-Tree balancing routine.
>  Using this option makes SQLite slightly smaller at the expense of
>  making it run slightly slower.


**SQLITE\_OMIT\_REINDEX**


> When this option is defined, the [REINDEX](lang_reindex.html)
>  command is not included in the library.
>  Executing a [REINDEX](lang_reindex.html) statement causes
>  a parse error.


**SQLITE\_OMIT\_SCHEMA\_PRAGMAS**


> Defining this option omits pragmas for querying the database schema from
>  the build.


**SQLITE\_OMIT\_SCHEMA\_VERSION\_PRAGMAS**


> Defining this option omits pragmas for querying and modifying the
>  database schema version and user version from the build. Specifically, the
>  [schema\_version](pragma.html#pragma_schema_version) and [user\_version](pragma.html#pragma_user_version) PRAGMAs are omitted.


**SQLITE\_OMIT\_SHARED\_CACHE**


> This option builds SQLite without support for [shared cache mode](sharedcache.html).
>  The [sqlite3\_enable\_shared\_cache()](c3ref/enable_shared_cache.html) is omitted along with a fair
>  amount of logic within the B\-Tree subsystem associated with shared
>  cache management.
> 
> 
>  This compile\-time option is recommended most applications as it
>  results in improved performance and reduced library footprint.


**SQLITE\_OMIT\_SUBQUERY**


> If defined, support for sub\-selects and the IN() operator are omitted.


**SQLITE\_OMIT\_TCL\_VARIABLE**


> If this macro is defined, then the special "$" syntax
>  used to automatically bind SQL variables to TCL variables is omitted.


**SQLITE\_OMIT\_TEMPDB**


> This option omits support for TEMP or TEMPORARY tables.


**SQLITE\_OMIT\_TRACE**


> This option omits support for the [sqlite3\_profile()](c3ref/profile.html) and
>  [sqlite3\_trace()](c3ref/profile.html) interfaces and their associated logic.


**SQLITE\_OMIT\_TRIGGER**


> Defining this option omits support for TRIGGER objects. Neither the
>  [CREATE TRIGGER](lang_createtrigger.html) or [DROP TRIGGER](lang_droptrigger.html)
>  commands are available in this case, and attempting to execute
>  either will result in a parse error.
>  This option also disables enforcement of [foreign key constraints](foreignkeys.html),
>  since the code that implements triggers and which is omitted by this
>  option is also used to implement [foreign key actions](foreignkeys.html#fk_actions).


**SQLITE\_OMIT\_TRUNCATE\_OPTIMIZATION**


> A default build of SQLite, if a [DELETE](lang_delete.html) statement has no WHERE clause
>  and operates on a table with no triggers, an optimization occurs that
>  causes the DELETE to occur by dropping and recreating the table.
>  Dropping and recreating a table is usually much faster than deleting
>  the table content row by row. This is the "truncate optimization".


**SQLITE\_OMIT\_UTF16**


> This macro is used to omit support for UTF16 text encoding. When this is
>  defined all API functions that return or accept UTF16 encoded text are
>  unavailable. These functions can be identified by the fact that they end
>  with '16', for example [sqlite3\_prepare16()](c3ref/prepare.html), [sqlite3\_column\_text16()](c3ref/column_blob.html) and
>  [sqlite3\_bind\_text16()](c3ref/bind_blob.html).


**SQLITE\_OMIT\_VACUUM**


> When this option is defined, the [VACUUM](lang_vacuum.html)
>  command is not included in the library.
>  Executing a [VACUUM](lang_vacuum.html) statement causes
>  a parse error.


**SQLITE\_OMIT\_VIEW**


> Defining this option omits support for VIEW objects. Neither the
>  [CREATE VIEW](lang_createview.html) nor the [DROP VIEW](lang_dropview.html)
>  commands are available in this case, and
>  attempting to execute either will result in a parse error.
> 
> 
>  WARNING: If this macro is defined, it will not be possible to open a database
>  for which the schema contains VIEW objects.


**SQLITE\_OMIT\_VIRTUALTABLE**


> This option omits support for the [Virtual Table](c3ref/vtab.html)
>  mechanism in SQLite.


**SQLITE\_OMIT\_WAL**


> This option omits the "[write\-ahead log](wal.html)" (a.k.a. "[WAL](wal.html)") capability.


**SQLITE\_OMIT\_WINDOWFUNC**


> This option omits [window functions](windowfunctions.html) from the build.


**SQLITE\_OMIT\_WSD**


> This option builds a version of the SQLite library that contains no
>  Writable Static Data (WSD). WSD is global variables and/or static
>  variables. Some platforms do not support WSD, and this option is necessary
>  in order for SQLite to work those platforms.
> 
> 
>  Unlike other OMIT options which make the SQLite library smaller,
>  this option actually increases the size of SQLite and makes it run
>  a little slower. Only use this option if SQLite is being built for an
>  embedded target that does not support WSD.


**SQLITE\_OMIT\_XFER\_OPT**


> This option omits support for optimizations that help statements
>  of the form "INSERT INTO ... SELECT ..." run faster.


**SQLITE\_UNTESTABLE**


> A standard SQLite build includes a small amount of logic associated
>  with [sqlite3\_test\_control()](c3ref/test_control.html) to exercise
>  parts of the SQLite core that are otherwise difficult to validate.
>  This compile\-time option omits that extra testing logic. This
>  compile\-time option was called "SQLITE\_OMIT\_BUILTIN\_TEST" prior
>  to SQLite version 3\.16\.0 (2017\-01\-02\). The name was changed
>  to better describe the implications of using it.
>  
>  Setting this compile\-time option prevents SQLite from being fully
>  testable. Branch test coverage drops from 100% down to about 95%.
>  
>  SQLite developers follow the NASA principle of
>  "fly what you test and test what you fly". This principle is violated
>  if this option is enabled for delivery but disabled for testing.
>  But if this option is enabled during testing, not all branches are
>  reachable. Therefore, the use of this compile\-time option is discouraged.


**SQLITE\_ZERO\_MALLOC**


> This option omits both the [default memory allocator](malloc.html#defaultalloc) and the
>  [debugging memory allocator](malloc.html#memdebug) from the build and substitutes a stub
>  memory allocator that always fails. SQLite will not run with this
>  stub memory allocator since it will be unable to allocate memory. But
>  this stub can be replaced at start\-time using
>  [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_MALLOC](c3ref/c_config_covering_index_scan.html#sqliteconfigmalloc),...) or
>  [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_HEAP](c3ref/c_config_covering_index_scan.html#sqliteconfigheap),...).
>  So the net effect of this compile\-time option is that it allows SQLite
>  to be compiled and linked against a system library that does not support
>  malloc(), free(), and/or realloc().





# 10\.  Analysis and Debugging Options



**SQLITE\_DEBUG**


> The SQLite source code contains literally thousands of assert() statements
>  used to verify internal assumptions and subroutine preconditions and
>  postconditions. These assert() statements are normally turned off
>  (they generate no code) since turning them on makes SQLite run approximately
>  three times slower. But for testing and analysis, it is useful to turn
>  the assert() statements on. The SQLITE\_DEBUG compile\-time option does this.
>  SQLITE\_DEBUG also enables some other debugging features, such as
>  special [PRAGMA](pragma.html#syntax) statements that turn on tracing and listing features
>  used for troubleshooting and analysis of the [VDBE](opcode.html) and code generator.


**SQLITE\_MEMDEBUG**


> The SQLITE\_MEMDEBUG option causes an instrumented
>  [debugging memory allocator](malloc.html#memdebug)
>  to be used as the default memory allocator within SQLite. The
>  instrumented memory allocator checks for misuse of dynamically allocated
>  memory. Examples of misuse include using memory after it is freed,
>  writing off the ends of a memory allocation, freeing memory not previously
>  obtained from the memory allocator, or failing to initialize newly
>  allocated memory.



# 11\.  Windows\-Specific Options



**SQLITE\_WIN32\_HEAP\_CREATE**


> This option forces the Win32 native memory allocator, when enabled, to
>  create a private heap to hold all memory allocations.


**SQLITE\_WIN32\_MALLOC\_VALIDATE**


> This option forces the Win32 native memory allocator, when enabled, to
>  make strategic calls into the HeapValidate() function if assert() is also
>  enabled.



# 12\. Compiler Linkage and Calling Convention Control


The following macros specify interface details
for certain kinds of SQLite builds. The Makefiles will normally
handle setting these macros automatically. Application developers should
not need to worry with these macros. The following documentation about these
macros is included for completeness.



**SQLITE\_API**


> This macro identifies an externally visible interface for SQLite.
>  This macro is sometimes set to "extern". But the definition is
>  compiler\-specific.


**SQLITE\_APICALL**


> This macro identifies the calling convention used by public interface
>  routines in SQLite which accept a fixed number of arguments.
>  This macro is normally defined to be nothing,
>  though on Windows builds it can sometimes be set to "\_\_cdecl" or "\_\_stdcall".
>  The "\_\_cdecl" setting is the default, but "\_\_stdcall" is used when SQLite
>  is intended to be compiled as a Windows system library.
>  
>  A single function declaration should contain no more than one of
>  the following: [SQLITE\_APICALL](compile.html#apicall), [SQLITE\_CDECL](compile.html#cdecl), or [SQLITE\_SYSAPI](compile.html#sysapi).


**SQLITE\_CALLBACK**


> This macro specifies the calling convention used with callback pointers
>  in SQLite. This macro is normally defined to be nothing, though on Windows
>  builds it can sometimes be set to "\_\_cdecl" or "\_\_stdcall". The
>  "\_\_cdecl" setting is the default, but "\_\_stdcall" is used when SQLite
>  is intended to be compiled as a Windows system library.


**SQLITE\_CDECL**


> This macro specifies the calling convention used by varargs interface
>  routines in SQLite. This macro is normally defined to be nothing,
>  though on Windows builds it can sometimes be set to "\_\_cdecl". This
>  macro is used on varargs routines and so cannot be set to "\_\_stdcall"
>  since the \_\_stdcall calling convention does not support varargs functions.
>  
>  A single function declaration should contain no more than one of
>  the following: [SQLITE\_APICALL](compile.html#apicall), [SQLITE\_CDECL](compile.html#cdecl), or [SQLITE\_SYSAPI](compile.html#sysapi).


**SQLITE\_EXTERN**


> This macro specifies linkage for public interface variables in SQLite.
>  It should normally be allowed to default to "extern".


**SQLITE\_STDCALL**


> This macro is no longer used and is now deprecated.


**SQLITE\_SYSAPI**


> This macro identifies the calling convention used by operating system
>  interfaces for the target platform for an SQLite build.
>  This macro is normally defined to be nothing,
>  though on Windows builds it can sometimes be set to "\_\_stdcall".
>  
>  A single function declaration should contain no more than one of
>  the following: [SQLITE\_APICALL](compile.html#apicall), [SQLITE\_CDECL](compile.html#cdecl), or [SQLITE\_SYSAPI](compile.html#sysapi).


**SQLITE\_TCLAPI**


> This macro specifies the calling convention used by the
>  [TCL](http://www.tcl.tk) library interface routines.
>  This macro is not used by the SQLite core, but only by the [TCL Interface](tclsqlite.html)
>  and [TCL test suite](testing.html#tcl).
>  This macro is normally defined to be nothing,
>  though on Windows builds it can sometimes be set to "\_\_cdecl". This
>  macro is used on TCL library interface routines which are always compiled
>  as \_\_cdecl, even on platforms that prefer to use \_\_stdcall, so this
>  macro should not be set to \_\_stdcall unless the platform has a custom
>  TCL library build that supports \_\_stdcall.
>  
>  This macro may not be used in combination with any of [SQLITE\_APICALL](compile.html#apicall),
>  [SQLITE\_CALLBACK](compile.html#callback), [SQLITE\_CDECL](compile.html#cdecl) or [SQLITE\_SYSAPI](compile.html#sysapi).


*This page last modified on [2024\-05\-09 08:10:19](https://sqlite.org/docsrc/honeypot) UTC* 


