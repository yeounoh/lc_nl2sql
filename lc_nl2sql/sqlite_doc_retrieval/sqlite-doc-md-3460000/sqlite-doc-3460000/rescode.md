




Result and Error Codes




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Result and Error Codes


►
Table Of Contents
[1\. Result Codes versus Error Codes](#result_codes_versus_error_codes)
[2\. Primary Result Codes versus Extended Result Codes](#primary_result_codes_versus_extended_result_codes)
[3\. Definitions](#definitions)
[4\. Primary Result Code List](#primary_result_code_list)
[5\. Extended Result Code List](#extended_result_code_list)
[6\. Result Code Meanings](#result_code_meanings)




## Overview



Many of the routines in the SQLite [C\-language Interface](c3ref/intro.html) return
numeric result codes indicating either success or failure, and 
in the event of a failure, providing some idea of the cause of
the failure. This document strives to explain what each
of those numeric result codes means.



# 1\. Result Codes versus Error Codes



"Error codes" are a subset of "result codes" that indicate that
something has gone wrong. There are only a few non\-error result
codes: [SQLITE\_OK](rescode.html#ok), [SQLITE\_ROW](rescode.html#row), and [SQLITE\_DONE](rescode.html#done). The term
"error code" means any result code other than these three.




# 2\. Primary Result Codes versus Extended Result Codes



Result codes are signed 32\-bit integers.
The least significant 8 bits of the result code define a broad category
and are called the "primary result code". More significant bits provide
more detailed information about the error and are called the
"extended result code"




Note that the primary result code is always a part of the extended
result code. Given a full 32\-bit extended result code, the application
can always find the corresponding primary result code merely by extracting
the least significant 8 bits of the extended result code.




All extended result codes are also error codes. Hence the terms
"extended result code" and "extended error code" are interchangeable.




For historic compatibility, the C\-language interfaces return
primary result codes by default. 
The extended result code for the most recent error can be
retrieved using the [sqlite3\_extended\_errcode()](c3ref/errcode.html) interface.
The [sqlite3\_extended\_result\_codes()](c3ref/extended_result_codes.html) interface can be used to put
a [database connection](c3ref/sqlite3.html) into a mode where it returns the
extended result codes instead of the primary result codes.



# 3\. Definitions



All result codes are integers.
Symbolic names for all result codes are created using
"\#define" macros in the sqlite3\.h header file.
There are separate sections in the sqlite3\.h header file for
the [result code definitions](c3ref/c_abort.html) and the [extended result code definitions](c3ref/c_abort_rollback.html).




Primary result code symbolic names are of the form "SQLITE\_XXXXXX" where
XXXXXX is a sequence of uppercase alphabetic characters. Extended
result code names are of the form "SQLITE\_XXXXXX\_YYYYYYY" where
the XXXXXX part is the corresponding primary result code and the
YYYYYYY is an extension that further classifies the result code.




The names and numeric values for existing result codes are fixed
and unchanging. However, new result codes, and especially new extended
result codes, might appear in future releases of SQLite.




# 4\. Primary Result Code List


The 31 result codes are
 [defined in sqlite3\.h](c3ref/c_abort.html) and are listed in
 alphabetical order below:

* [SQLITE\_ABORT (4\)](rescode.html#abort)
* [SQLITE\_AUTH (23\)](rescode.html#auth)
* [SQLITE\_BUSY (5\)](rescode.html#busy)
* [SQLITE\_CANTOPEN (14\)](rescode.html#cantopen)
* [SQLITE\_CONSTRAINT (19\)](rescode.html#constraint)
* [SQLITE\_CORRUPT (11\)](rescode.html#corrupt)
* [SQLITE\_DONE (101\)](rescode.html#done)
* [SQLITE\_EMPTY (16\)](rescode.html#empty)
* [SQLITE\_ERROR (1\)](rescode.html#error)
* [SQLITE\_FORMAT (24\)](rescode.html#format)
* [SQLITE\_FULL (13\)](rescode.html#full)
* [SQLITE\_INTERNAL (2\)](rescode.html#internal)
* [SQLITE\_INTERRUPT (9\)](rescode.html#interrupt)
* [SQLITE\_IOERR (10\)](rescode.html#ioerr)
* [SQLITE\_LOCKED (6\)](rescode.html#locked)
* [SQLITE\_MISMATCH (20\)](rescode.html#mismatch)
* [SQLITE\_MISUSE (21\)](rescode.html#misuse)
* [SQLITE\_NOLFS (22\)](rescode.html#nolfs)
* [SQLITE\_NOMEM (7\)](rescode.html#nomem)
* [SQLITE\_NOTADB (26\)](rescode.html#notadb)
* [SQLITE\_NOTFOUND (12\)](rescode.html#notfound)
* [SQLITE\_NOTICE (27\)](rescode.html#notice)
* [SQLITE\_OK (0\)](rescode.html#ok)
* [SQLITE\_PERM (3\)](rescode.html#perm)
* [SQLITE\_PROTOCOL (15\)](rescode.html#protocol)
* [SQLITE\_RANGE (25\)](rescode.html#range)
* [SQLITE\_READONLY (8\)](rescode.html#readonly)
* [SQLITE\_ROW (100\)](rescode.html#row)
* [SQLITE\_SCHEMA (17\)](rescode.html#schema)
* [SQLITE\_TOOBIG (18\)](rescode.html#toobig)
* [SQLITE\_WARNING (28\)](rescode.html#warning)






# 5\. Extended Result Code List


The 74 extended result codes
 are [defined in sqlite3\.h](c3ref/c_abort_rollback.html) and are
 listed in alphabetical order below:

* [SQLITE\_ABORT\_ROLLBACK (516\)](rescode.html#abort_rollback)
* [SQLITE\_AUTH\_USER (279\)](rescode.html#auth_user)
* [SQLITE\_BUSY\_RECOVERY (261\)](rescode.html#busy_recovery)
* [SQLITE\_BUSY\_SNAPSHOT (517\)](rescode.html#busy_snapshot)
* [SQLITE\_BUSY\_TIMEOUT (773\)](rescode.html#busy_timeout)
* [SQLITE\_CANTOPEN\_CONVPATH (1038\)](rescode.html#cantopen_convpath)
* [SQLITE\_CANTOPEN\_DIRTYWAL (1294\)](rescode.html#cantopen_dirtywal)
* [SQLITE\_CANTOPEN\_FULLPATH (782\)](rescode.html#cantopen_fullpath)
* [SQLITE\_CANTOPEN\_ISDIR (526\)](rescode.html#cantopen_isdir)
* [SQLITE\_CANTOPEN\_NOTEMPDIR (270\)](rescode.html#cantopen_notempdir)
* [SQLITE\_CANTOPEN\_SYMLINK (1550\)](rescode.html#cantopen_symlink)
* [SQLITE\_CONSTRAINT\_CHECK (275\)](rescode.html#constraint_check)
* [SQLITE\_CONSTRAINT\_COMMITHOOK (531\)](rescode.html#constraint_commithook)
* [SQLITE\_CONSTRAINT\_DATATYPE (3091\)](rescode.html#constraint_datatype)
* [SQLITE\_CONSTRAINT\_FOREIGNKEY (787\)](rescode.html#constraint_foreignkey)
* [SQLITE\_CONSTRAINT\_FUNCTION (1043\)](rescode.html#constraint_function)
* [SQLITE\_CONSTRAINT\_NOTNULL (1299\)](rescode.html#constraint_notnull)
* [SQLITE\_CONSTRAINT\_PINNED (2835\)](rescode.html#constraint_pinned)
* [SQLITE\_CONSTRAINT\_PRIMARYKEY (1555\)](rescode.html#constraint_primarykey)
* [SQLITE\_CONSTRAINT\_ROWID (2579\)](rescode.html#constraint_rowid)
* [SQLITE\_CONSTRAINT\_TRIGGER (1811\)](rescode.html#constraint_trigger)
* [SQLITE\_CONSTRAINT\_UNIQUE (2067\)](rescode.html#constraint_unique)
* [SQLITE\_CONSTRAINT\_VTAB (2323\)](rescode.html#constraint_vtab)
* [SQLITE\_CORRUPT\_INDEX (779\)](rescode.html#corrupt_index)
* [SQLITE\_CORRUPT\_SEQUENCE (523\)](rescode.html#corrupt_sequence)
* [SQLITE\_CORRUPT\_VTAB (267\)](rescode.html#corrupt_vtab)
* [SQLITE\_ERROR\_MISSING\_COLLSEQ (257\)](rescode.html#error_missing_collseq)
* [SQLITE\_ERROR\_RETRY (513\)](rescode.html#error_retry)
* [SQLITE\_ERROR\_SNAPSHOT (769\)](rescode.html#error_snapshot)
* [SQLITE\_IOERR\_ACCESS (3338\)](rescode.html#ioerr_access)
* [SQLITE\_IOERR\_AUTH (7178\)](rescode.html#ioerr_auth)
* [SQLITE\_IOERR\_BEGIN\_ATOMIC (7434\)](rescode.html#ioerr_begin_atomic)
* [SQLITE\_IOERR\_BLOCKED (2826\)](rescode.html#ioerr_blocked)
* [SQLITE\_IOERR\_CHECKRESERVEDLOCK (3594\)](rescode.html#ioerr_checkreservedlock)
* [SQLITE\_IOERR\_CLOSE (4106\)](rescode.html#ioerr_close)
* [SQLITE\_IOERR\_COMMIT\_ATOMIC (7690\)](rescode.html#ioerr_commit_atomic)
* [SQLITE\_IOERR\_CONVPATH (6666\)](rescode.html#ioerr_convpath)
* [SQLITE\_IOERR\_CORRUPTFS (8458\)](rescode.html#ioerr_corruptfs)
* [SQLITE\_IOERR\_DATA (8202\)](rescode.html#ioerr_data)
* [SQLITE\_IOERR\_DELETE (2570\)](rescode.html#ioerr_delete)
* [SQLITE\_IOERR\_DELETE\_NOENT (5898\)](rescode.html#ioerr_delete_noent)
* [SQLITE\_IOERR\_DIR\_CLOSE (4362\)](rescode.html#ioerr_dir_close)
* [SQLITE\_IOERR\_DIR\_FSYNC (1290\)](rescode.html#ioerr_dir_fsync)
* [SQLITE\_IOERR\_FSTAT (1802\)](rescode.html#ioerr_fstat)
* [SQLITE\_IOERR\_FSYNC (1034\)](rescode.html#ioerr_fsync)
* [SQLITE\_IOERR\_GETTEMPPATH (6410\)](rescode.html#ioerr_gettemppath)
* [SQLITE\_IOERR\_LOCK (3850\)](rescode.html#ioerr_lock)
* [SQLITE\_IOERR\_MMAP (6154\)](rescode.html#ioerr_mmap)
* [SQLITE\_IOERR\_NOMEM (3082\)](rescode.html#ioerr_nomem)
* [SQLITE\_IOERR\_RDLOCK (2314\)](rescode.html#ioerr_rdlock)
* [SQLITE\_IOERR\_READ (266\)](rescode.html#ioerr_read)
* [SQLITE\_IOERR\_ROLLBACK\_ATOMIC (7946\)](rescode.html#ioerr_rollback_atomic)
* [SQLITE\_IOERR\_SEEK (5642\)](rescode.html#ioerr_seek)
* [SQLITE\_IOERR\_SHMLOCK (5130\)](rescode.html#ioerr_shmlock)
* [SQLITE\_IOERR\_SHMMAP (5386\)](rescode.html#ioerr_shmmap)
* [SQLITE\_IOERR\_SHMOPEN (4618\)](rescode.html#ioerr_shmopen)
* [SQLITE\_IOERR\_SHMSIZE (4874\)](rescode.html#ioerr_shmsize)
* [SQLITE\_IOERR\_SHORT\_READ (522\)](rescode.html#ioerr_short_read)
* [SQLITE\_IOERR\_TRUNCATE (1546\)](rescode.html#ioerr_truncate)
* [SQLITE\_IOERR\_UNLOCK (2058\)](rescode.html#ioerr_unlock)
* [SQLITE\_IOERR\_VNODE (6922\)](rescode.html#ioerr_vnode)
* [SQLITE\_IOERR\_WRITE (778\)](rescode.html#ioerr_write)
* [SQLITE\_LOCKED\_SHAREDCACHE (262\)](rescode.html#locked_sharedcache)
* [SQLITE\_LOCKED\_VTAB (518\)](rescode.html#locked_vtab)
* [SQLITE\_NOTICE\_RECOVER\_ROLLBACK (539\)](rescode.html#notice_recover_rollback)
* [SQLITE\_NOTICE\_RECOVER\_WAL (283\)](rescode.html#notice_recover_wal)
* [SQLITE\_OK\_LOAD\_PERMANENTLY (256\)](rescode.html#ok_load_permanently)
* [SQLITE\_READONLY\_CANTINIT (1288\)](rescode.html#readonly_cantinit)
* [SQLITE\_READONLY\_CANTLOCK (520\)](rescode.html#readonly_cantlock)
* [SQLITE\_READONLY\_DBMOVED (1032\)](rescode.html#readonly_dbmoved)
* [SQLITE\_READONLY\_DIRECTORY (1544\)](rescode.html#readonly_directory)
* [SQLITE\_READONLY\_RECOVERY (264\)](rescode.html#readonly_recovery)
* [SQLITE\_READONLY\_ROLLBACK (776\)](rescode.html#readonly_rollback)
* [SQLITE\_WARNING\_AUTOINDEX (284\)](rescode.html#warning_autoindex)





# 6\. Result Code Meanings



The meanings for all 105
result code values are shown below,
in numeric order.



### (0\) SQLITE\_OK



 The SQLITE\_OK result code means that the operation was successful and
 that there were no errors. Most other result codes indicate an error.




### (1\) SQLITE\_ERROR



 The SQLITE\_ERROR result code is a generic error code that is used when
 no other more specific error code is available.




### (2\) SQLITE\_INTERNAL



 The SQLITE\_INTERNAL result code indicates an internal malfunction.
 In a working version of SQLite, an application should never see this
 result code. If application does encounter this result code, it shows
 that there is a bug in the database engine.
 
 SQLite does not currently generate this result code.
 However, [application\-defined SQL functions](appfunc.html) or
 [virtual tables](vtab.html), or [VFSes](vfs.html), or other extensions might cause this 
 result code to be returned.




### (3\) SQLITE\_PERM



 The SQLITE\_PERM result code indicates that the requested access mode
 for a newly created database could not be provided.




### (4\) SQLITE\_ABORT



 The SQLITE\_ABORT result code indicates that an operation was aborted
 prior to completion, usually be application request.
 See also: [SQLITE\_INTERRUPT](rescode.html#interrupt).
 
 If the callback function to [sqlite3\_exec()](c3ref/exec.html) returns non\-zero, then
 sqlite3\_exec() will return SQLITE\_ABORT.
 
 If a [ROLLBACK](lang_transaction.html) operation occurs on the same [database connection](c3ref/sqlite3.html) as
 a pending read or write, then the pending read or write may fail with
 an SQLITE\_ABORT or [SQLITE\_ABORT\_ROLLBACK](rescode.html#abort_rollback) error.
 
 In addition to being a result code,
 the SQLITE\_ABORT value is also used as a [conflict resolution mode](c3ref/c_fail.html)
 returned from the [sqlite3\_vtab\_on\_conflict()](c3ref/vtab_on_conflict.html) interface.




### (5\) SQLITE\_BUSY



 The SQLITE\_BUSY result code indicates that the database file could not
 be written (or in some cases read) because of concurrent activity by 
 some other [database connection](c3ref/sqlite3.html), usually a database connection in a
 separate process.
 
 For example, if process A is in the middle of a large write transaction
 and at the same time process B attempts to start a new write transaction,
 process B will get back an SQLITE\_BUSY result because SQLite only supports
 one writer at a time. Process B will need to wait for process A to finish
 its transaction before starting a new transaction. The
 [sqlite3\_busy\_timeout()](c3ref/busy_timeout.html) and [sqlite3\_busy\_handler()](c3ref/busy_handler.html) interfaces and
 the [busy\_timeout pragma](pragma.html#pragma_busy_timeout) are available to process B to help it deal
 with SQLITE\_BUSY errors.
 
 An SQLITE\_BUSY error can occur at any point in a transaction: when the
 transaction is first started, during any write or update operations, or
 when the transaction commits.
 To avoid encountering SQLITE\_BUSY errors in the middle of a transaction,
 the application can use [BEGIN IMMEDIATE](lang_transaction.html#immediate) instead of just [BEGIN](lang_transaction.html) to
 start a transaction. The [BEGIN IMMEDIATE](lang_transaction.html#immediate) command might itself return
 SQLITE\_BUSY, but if it succeeds, then SQLite guarantees that no 
 subsequent operations on the same database through the next [COMMIT](lang_transaction.html) 
 will return SQLITE\_BUSY.
 
 See also: [SQLITE\_BUSY\_RECOVERY](rescode.html#busy_recovery) and [SQLITE\_BUSY\_SNAPSHOT](rescode.html#busy_snapshot).
 
 The SQLITE\_BUSY result code differs from [SQLITE\_LOCKED](rescode.html#locked) in that
 SQLITE\_BUSY indicates a conflict with a
 separate [database connection](c3ref/sqlite3.html), probably in a separate process,
 whereas [SQLITE\_LOCKED](rescode.html#locked) 
 indicates a conflict within the same [database connection](c3ref/sqlite3.html) (or sometimes
 a database connection with a [shared cache](sharedcache.html)).




### (6\) SQLITE\_LOCKED



 The SQLITE\_LOCKED result code indicates that a write operation could not
 continue because of a conflict within the same [database connection](c3ref/sqlite3.html) or
 a conflict with a different database connection that uses a [shared cache](sharedcache.html).
 
 For example, a [DROP TABLE](lang_droptable.html) statement cannot be run while another thread
 is reading from that table on the same [database connection](c3ref/sqlite3.html) because 
 dropping the table would delete the table out from under the concurrent
 reader.
 
 The SQLITE\_LOCKED result code differs from [SQLITE\_BUSY](rescode.html#busy) in that
 SQLITE\_LOCKED indicates a conflict on the same [database connection](c3ref/sqlite3.html)
 (or on a connection with a [shared cache](sharedcache.html)) whereas [SQLITE\_BUSY](rescode.html#busy) indicates
 a conflict with a different database connection, probably in a different
 process.




### (7\) SQLITE\_NOMEM



 The SQLITE\_NOMEM result code indicates that SQLite was unable to allocate
 all the memory it needed to complete the operation. In other words, an
 internal call to [sqlite3\_malloc()](c3ref/free.html) or [sqlite3\_realloc()](c3ref/free.html) has failed in
 a case where the memory being allocated was required in order to continue
 the operation.




### (8\) SQLITE\_READONLY



 The SQLITE\_READONLY result code is returned when an attempt is made to 
 alter some data for which the current database connection does not have
 write permission.




### (9\) SQLITE\_INTERRUPT



 The SQLITE\_INTERRUPT result code indicates that an operation was
 interrupted by the [sqlite3\_interrupt()](c3ref/interrupt.html) interface.
 See also: [SQLITE\_ABORT](rescode.html#abort)


### (10\) SQLITE\_IOERR



 The SQLITE\_IOERR result code says that the operation could not finish
 because the operating system reported an I/O error.
 
 A full disk drive will normally give an [SQLITE\_FULL](rescode.html#full) error rather than
 an SQLITE\_IOERR error.
 
 There are many different extended result codes for I/O errors that
 identify the specific I/O operation that failed.




### (11\) SQLITE\_CORRUPT



 The SQLITE\_CORRUPT result code indicates that the database file has
 been corrupted. See the [How To Corrupt Your Database Files](lockingv3.html#how_to_corrupt) for
 further discussion on how corruption can occur.




### (12\) SQLITE\_NOTFOUND



 The SQLITE\_NOTFOUND result code is exposed in three ways:
 1. SQLITE\_NOTFOUND can be returned by the [sqlite3\_file\_control()](c3ref/file_control.html) interface
 to indicate that the [file control opcode](c3ref/c_fcntl_begin_atomic_write.html) passed as the third argument
 was not recognized by the underlying [VFS](vfs.html).
 - SQLITE\_NOTFOUND can also be returned by the xSetSystemCall() method of
 an [sqlite3\_vfs](c3ref/vfs.html) object.
 - SQLITE\_NOTFOUND can be returned by [sqlite3\_vtab\_rhs\_value()](c3ref/vtab_rhs_value.html) to indicate
 that the right\-hand operand of a constraint is not available to the
 [xBestIndex method](vtab.html#xbestindex) that made the call.



 The SQLITE\_NOTFOUND result code is also used
 internally by the SQLite implementation, but those internal uses are
 not exposed to the application.




### (13\) SQLITE\_FULL



 The SQLITE\_FULL result code indicates that a write could not complete
 because the disk is full. Note that this error can occur when trying
 to write information into the main database file, or it can also
 occur when writing into [temporary disk files](tempfiles.html).
 
 Sometimes applications encounter this error even though there is an
 abundance of primary disk space because the error occurs when writing
 into [temporary disk files](tempfiles.html) on a system where temporary files are stored
 on a separate partition with much less space that the primary disk.




### (14\) SQLITE\_CANTOPEN



 The SQLITE\_CANTOPEN result code indicates that SQLite was unable to
 open a file. The file in question might be a primary database file
 or one of several [temporary disk files](tempfiles.html).




### (15\) SQLITE\_PROTOCOL



 The SQLITE\_PROTOCOL result code indicates a problem with the file locking
 protocol used by SQLite. The SQLITE\_PROTOCOL error is currently only
 returned when using [WAL mode](wal.html) and attempting to start a new transaction.
 There is a race condition that can occur when two separate 
 [database connections](c3ref/sqlite3.html) both try to start a transaction at the same time
 in [WAL mode](wal.html). The loser of the race backs off and tries again, after
 a brief delay. If the same connection loses the locking race dozens
 of times over a span of multiple seconds, it will eventually give up and
 return SQLITE\_PROTOCOL. The SQLITE\_PROTOCOL error should appear in practice
 very, very rarely, and only when there are many separate processes all
 competing intensely to write to the same database.




### (16\) SQLITE\_EMPTY



 The SQLITE\_EMPTY result code is not currently used.




### (17\) SQLITE\_SCHEMA



 The SQLITE\_SCHEMA result code indicates that the database schema
 has changed. This result code can be returned from [sqlite3\_step()](c3ref/step.html) for
 a [prepared statement](c3ref/stmt.html) that was generated using [sqlite3\_prepare()](c3ref/prepare.html) or
 [sqlite3\_prepare16()](c3ref/prepare.html). If the database schema was changed by some other
 process in between the time that the statement was prepared and the time
 the statement was run, this error can result.
 
 If a [prepared statement](c3ref/stmt.html) is generated from [sqlite3\_prepare\_v2()](c3ref/prepare.html) then
 the statement is automatically re\-prepared if the schema changes, up to
 [SQLITE\_MAX\_SCHEMA\_RETRY](compile.html#max_schema_retry) times (default: 50\). The [sqlite3\_step()](c3ref/step.html)
 interface will only return SQLITE\_SCHEMA back to the application if 
 the failure persists after these many retries.




### (18\) SQLITE\_TOOBIG



 The SQLITE\_TOOBIG error code indicates that a string or BLOB was
 too large. The default maximum length of a string or BLOB in SQLite is
 1,000,000,000 bytes. This maximum length can be changed at compile\-time
 using the [SQLITE\_MAX\_LENGTH](limits.html#max_length) compile\-time option, or at run\-time using
 the [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_LENGTH](c3ref/c_limit_attached.html#sqlitelimitlength),...) interface. The
 SQLITE\_TOOBIG error results when SQLite encounters a string or BLOB
 that exceeds the compile\-time or run\-time limit.
 
 The SQLITE\_TOOBIG error code can also result when an oversized SQL
 statement is passed into one of the [sqlite3\_prepare\_v2()](c3ref/prepare.html) interfaces.
 The maximum length of an SQL statement defaults to a much smaller
 value of 1,000,000,000 bytes. The maximum SQL statement length can be
 set at compile\-time using [SQLITE\_MAX\_SQL\_LENGTH](limits.html#max_sql_length) or at run\-time
 using [sqlite3\_limit](c3ref/limit.html)(db,[SQLITE\_LIMIT\_SQL\_LENGTH](c3ref/c_limit_attached.html#sqlitelimitsqllength),...).




### (19\) SQLITE\_CONSTRAINT



 The SQLITE\_CONSTRAINT error code means that an SQL constraint violation
 occurred while trying to process an SQL statement. Additional information
 about the failed constraint can be found by consulting the
 accompanying error message (returned via [sqlite3\_errmsg()](c3ref/errcode.html) or
 [sqlite3\_errmsg16()](c3ref/errcode.html)) or by looking at the [extended error code](rescode.html#extrc).
 
 The SQLITE\_CONSTRAINT code can also be used as the return value from
 the [xBestIndex()](vtab.html#xbestindex) method of a [virtual table](vtab.html) implementation. When
 xBestIndex() returns SQLITE\_CONSTRAINT, that indicates that the particular
 combination of inputs submitted to xBestIndex() cannot result in a
 usable query plan and should not be given further consideration.




### (20\) SQLITE\_MISMATCH



 The SQLITE\_MISMATCH error code indicates a datatype mismatch.
 
 SQLite is normally very forgiving about mismatches between the type of
 a value and the declared type of the container in which that value is
 to be stored. For example, SQLite allows the application to store
 a large BLOB in a column with a declared type of BOOLEAN. But in a few
 cases, SQLite is strict about types. The SQLITE\_MISMATCH error is
 returned in those few cases when the types do not match.
 
 The [rowid](lang_createtable.html#rowid) of a table must be an integer. Attempt to set the [rowid](lang_createtable.html#rowid)
 to anything other than an integer (or a NULL which will be automatically
 converted into the next available integer rowid) results in an
 SQLITE\_MISMATCH error.




### (21\) SQLITE\_MISUSE



 The SQLITE\_MISUSE return code might be returned if the application uses
 any SQLite interface in a way that is undefined or unsupported. For
 example, using a [prepared statement](c3ref/stmt.html) after that prepared statement has
 been [finalized](c3ref/finalize.html) might result in an SQLITE\_MISUSE error.
 
 SQLite tries to detect misuse and report the misuse using this result code.
 However, there is no guarantee that the detection of misuse will be
 successful. Misuse detection is probabilistic. Applications should
 never depend on an SQLITE\_MISUSE return value.
 
 If SQLite ever returns SQLITE\_MISUSE from any interface, that means that
 the application is incorrectly coded and needs to be fixed. Do not ship
 an application that sometimes returns SQLITE\_MISUSE from a standard
 SQLite interface because that application contains potentially serious bugs.




### (22\) SQLITE\_NOLFS



 The SQLITE\_NOLFS error can be returned on systems that do not support
 large files when the database grows to be larger than what the filesystem
 can handle. "NOLFS" stands for "NO Large File Support".




### (23\) SQLITE\_AUTH



 The SQLITE\_AUTH error is returned when the
 [authorizer callback](c3ref/set_authorizer.html) indicates that an
 SQL statement being prepared is not authorized.




### (24\) SQLITE\_FORMAT



 The SQLITE\_FORMAT error code is not currently used by SQLite.




### (25\) SQLITE\_RANGE



 The SQLITE\_RANGE error indices that the parameter number argument
 to one of the [sqlite3\_bind](c3ref/bind_blob.html) routines or the
 column number in one of the [sqlite3\_column](c3ref/column_blob.html)
 routines is out of range.




### (26\) SQLITE\_NOTADB



 When attempting to open a file, the SQLITE\_NOTADB error indicates that
 the file being opened does not appear to be an SQLite database file.




### (27\) SQLITE\_NOTICE



 The SQLITE\_NOTICE result code is not returned by any C/C\+\+ interface.
 However, SQLITE\_NOTICE (or rather one of its [extended error codes](rescode.html#extrc))
 is sometimes used as the first argument in an [sqlite3\_log()](c3ref/log.html) callback
 to indicate that an unusual operation is taking place.




### (28\) SQLITE\_WARNING



 The SQLITE\_WARNING result code is not returned by any C/C\+\+ interface.
 However, SQLITE\_WARNING (or rather one of its [extended error codes](rescode.html#extrc))
 is sometimes used as the first argument in an [sqlite3\_log()](c3ref/log.html) callback
 to indicate that an unusual and possibly ill\-advised operation is
 taking place.




### (100\) SQLITE\_ROW



 The SQLITE\_ROW result code returned by
 [sqlite3\_step()](c3ref/step.html) indicates that another row of output is available.




### (101\) SQLITE\_DONE



 The SQLITE\_DONE result code indicates that an operation has completed.
 The SQLITE\_DONE result code is most commonly seen as a return value
 from [sqlite3\_step()](c3ref/step.html) indicating that the SQL statement has run to
 completion. But SQLITE\_DONE can also be returned by other multi\-step
 interfaces such as [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep).




### (256\) SQLITE\_OK\_LOAD\_PERMANENTLY



 The [sqlite3\_load\_extension()](c3ref/load_extension.html) interface loads an
 [extension](loadext.html) into a single
 database connection. The default behavior is for that extension to be
 automatically unloaded when the database connection closes. However,
 if the extension entry point returns SQLITE\_OK\_LOAD\_PERMANENTLY instead
 of SQLITE\_OK, then the extension remains loaded into the process address
 space after the database connection closes. In other words, the
 xDlClose methods of the [sqlite3\_vfs](c3ref/vfs.html) object is not called for the
 extension when the database connection closes.
 
 The SQLITE\_OK\_LOAD\_PERMANENTLY return code is useful to
 [loadable extensions](loadext.html) that register new [VFSes](vfs.html), for example.




### (257\) SQLITE\_ERROR\_MISSING\_COLLSEQ



 The SQLITE\_ERROR\_MISSING\_COLLSEQ result code means that an SQL
 statement could not be prepared because a collating sequence named
 in that SQL statement could not be located.
 
 Sometimes when this error code is encountered, the
 [sqlite3\_prepare\_v2()](c3ref/prepare.html) routine will convert the error into
 [SQLITE\_ERROR\_RETRY](rescode.html#error_retry) and try again to prepare the SQL statement
 using a different query plan that does not require the use of
 the unknown collating sequence.




### (261\) SQLITE\_BUSY\_RECOVERY



 The SQLITE\_BUSY\_RECOVERY error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_BUSY](rescode.html#busy) that indicates that an operation could not continue
 because another process is busy recovering a [WAL mode](wal.html) database file
 following a crash. The SQLITE\_BUSY\_RECOVERY error code only occurs
 on [WAL mode](wal.html) databases.




### (262\) SQLITE\_LOCKED\_SHAREDCACHE



 The SQLITE\_LOCKED\_SHAREDCACHE result code indicates that access to
 an SQLite data record is blocked by another database connection that
 is using the same record in [shared cache mode](sharedcache.html). When two or more
 database connections share the same cache and one of the connections is
 in the middle of modifying a record in that cache, then other connections
 are blocked from accessing that data while the modifications are on\-going
 in order to prevent the readers from seeing a corrupt or partially
 completed change.




### (264\) SQLITE\_READONLY\_RECOVERY



 The SQLITE\_READONLY\_RECOVERY error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_READONLY](rescode.html#readonly). The SQLITE\_READONLY\_RECOVERY error code indicates
 that a [WAL mode](wal.html) database cannot be opened because the database file
 needs to be recovered and recovery requires write access but only
 read access is available.




### (266\) SQLITE\_IOERR\_READ



 The SQLITE\_IOERR\_READ error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error in the [VFS](vfs.html) layer
 while trying to read from a file on disk. This error might result
 from a hardware malfunction or because a filesystem came unmounted
 while the file was open.




### (267\) SQLITE\_CORRUPT\_VTAB



 The SQLITE\_CORRUPT\_VTAB error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_CORRUPT](rescode.html#corrupt) used by [virtual tables](vtab.html). A [virtual table](vtab.html) might
 return SQLITE\_CORRUPT\_VTAB to indicate that content in the virtual table
 is corrupt.




### (270\) SQLITE\_CANTOPEN\_NOTEMPDIR



 The SQLITE\_CANTOPEN\_NOTEMPDIR error code is no longer used.




### (275\) SQLITE\_CONSTRAINT\_CHECK



 The SQLITE\_CONSTRAINT\_CHECK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a [CHECK constraint](lang_createtable.html#ckconst) failed.




### (279\) SQLITE\_AUTH\_USER



 The SQLITE\_AUTH\_USER error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_AUTH](rescode.html#auth) indicating that an operation was attempted on a
 database for which the logged in user lacks sufficient authorization.




### (283\) SQLITE\_NOTICE\_RECOVER\_WAL



 The SQLITE\_NOTICE\_RECOVER\_WAL result code is
 passed to the callback of
 [sqlite3\_log()](c3ref/log.html) when a [WAL mode](wal.html) database file is recovered.




### (284\) SQLITE\_WARNING\_AUTOINDEX



 The SQLITE\_WARNING\_AUTOINDEX result code is
 passed to the callback of
 [sqlite3\_log()](c3ref/log.html) whenever [automatic indexing](optoverview.html#autoindex) is used.
 This can serve as a warning to application designers that the
 database might benefit from additional indexes.




### (513\) SQLITE\_ERROR\_RETRY



 The SQLITE\_ERROR\_RETRY is used internally to provoke [sqlite3\_prepare\_v2()](c3ref/prepare.html)
 (or one of its sibling routines for creating prepared statements) to
 try again to prepare a statement that failed with an error on the
 previous attempt.




### (516\) SQLITE\_ABORT\_ROLLBACK



 The SQLITE\_ABORT\_ROLLBACK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_ABORT](rescode.html#abort) indicating that an SQL statement aborted because
 the transaction that was active when the SQL statement first started
 was rolled back. Pending write operations always fail with this error
 when a rollback occurs. A [ROLLBACK](lang_transaction.html) will cause a pending read operation
 to fail only if the schema was changed within the transaction being rolled
 back.




### (517\) SQLITE\_BUSY\_SNAPSHOT



 The SQLITE\_BUSY\_SNAPSHOT error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_BUSY](rescode.html#busy) that occurs on [WAL mode](wal.html) databases when a database
 connection tries to promote a read transaction into a write transaction
 but finds that another [database connection](c3ref/sqlite3.html) has already written to the
 database and thus invalidated prior reads.
 
 The following scenario illustrates how an SQLITE\_BUSY\_SNAPSHOT error
 might arise:
 1. Process A starts a read transaction on the database and does one
 or more SELECT statement. Process A keeps the transaction open.
 - Process B updates the database, changing values previous read by
 process A.
 - Process A now tries to write to the database. But process A's view
 of the database content is now obsolete because process B has
 modified the database file after process A read from it. Hence
 process A gets an SQLITE\_BUSY\_SNAPSHOT error.




### (518\) SQLITE\_LOCKED\_VTAB



 The SQLITE\_LOCKED\_VTAB result code is not used by the SQLite core, but
 it is available for use by extensions. Virtual table implementations
 can return this result code to indicate that they cannot complete the
 current operation because of locks held by other threads or processes.
 
 The [R\-Tree extension](rtree.html) returns this result code when an attempt is made
 to update the R\-Tree while another prepared statement is actively reading
 the R\-Tree. The update cannot proceed because any change to an R\-Tree
 might involve reshuffling and rebalancing of nodes, which would disrupt
 read cursors, causing some rows to be repeated and other rows to be
 omitted.




### (520\) SQLITE\_READONLY\_CANTLOCK



 The SQLITE\_READONLY\_CANTLOCK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_READONLY](rescode.html#readonly). The SQLITE\_READONLY\_CANTLOCK error code indicates
 that SQLite is unable to obtain a read lock on a [WAL mode](wal.html) database
 because the shared\-memory file associated with that database is read\-only.




### (522\) SQLITE\_IOERR\_SHORT\_READ



 The SQLITE\_IOERR\_SHORT\_READ error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating that a read attempt in the [VFS](vfs.html) layer
 was unable to obtain as many bytes as was requested. This might be
 due to a truncated file.




### (523\) SQLITE\_CORRUPT\_SEQUENCE



 The SQLITE\_CORRUPT\_SEQUENCE result code means that the schema of
 the sqlite\_sequence table is corrupt. The sqlite\_sequence table
 is used to help implement the [AUTOINCREMENT](autoinc.html) feature. The
 sqlite\_sequence table should have the following format:
 
> ```
> 
>   CREATE TABLE sqlite_sequence(name,seq);
>   
> ```


If SQLite discovers that the sqlite\_sequence table has any other
 format, it returns the SQLITE\_CORRUPT\_SEQUENCE error.




### (526\) SQLITE\_CANTOPEN\_ISDIR



 The SQLITE\_CANTOPEN\_ISDIR error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_CANTOPEN](rescode.html#cantopen) indicating that a file open operation failed because
 the file is really a directory.




### (531\) SQLITE\_CONSTRAINT\_COMMITHOOK



 The SQLITE\_CONSTRAINT\_COMMITHOOK error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a
 [commit hook callback](c3ref/commit_hook.html) returned non\-zero that thus
 caused the SQL statement to be rolled back.




### (539\) SQLITE\_NOTICE\_RECOVER\_ROLLBACK



 The SQLITE\_NOTICE\_RECOVER\_ROLLBACK result code is
 passed to the callback of
 [sqlite3\_log()](c3ref/log.html) when a [hot journal](fileformat2.html#hotjrnl) is rolled back.




### (769\) SQLITE\_ERROR\_SNAPSHOT



 The SQLITE\_ERROR\_SNAPSHOT result code might be returned when attempting
 to start a read transaction on an historical version of the database
 by using the [sqlite3\_snapshot\_open()](c3ref/snapshot_open.html) interface. If the historical
 snapshot is no longer available, then the read transaction will fail
 with the SQLITE\_ERROR\_SNAPSHOT. This error code is only possible if
 SQLite is compiled with [\-DSQLITE\_ENABLE\_SNAPSHOT](compile.html#enable_snapshot).




### (773\) SQLITE\_BUSY\_TIMEOUT



 The SQLITE\_BUSY\_TIMEOUT error code indicates that a blocking Posix
 advisory file lock request in the VFS layer failed due to a timeout.
 Blocking Posix advisory locks are only
 available as a proprietary SQLite extension and even then are only
 supported if SQLite is compiled with the SQLITE\_EANBLE\_SETLK\_TIMEOUT
 compile\-time option.




### (776\) SQLITE\_READONLY\_ROLLBACK



 The SQLITE\_READONLY\_ROLLBACK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_READONLY](rescode.html#readonly). The SQLITE\_READONLY\_ROLLBACK error code indicates
 that a database cannot be opened because it has a [hot journal](fileformat2.html#hotjrnl) that
 needs to be rolled back but cannot because the database is readonly.




### (778\) SQLITE\_IOERR\_WRITE



 The SQLITE\_IOERR\_WRITE error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error in the [VFS](vfs.html) layer
 while trying to write into a file on disk. This error might result
 from a hardware malfunction or because a filesystem came unmounted
 while the file was open. This error should not occur if the filesystem
 is full as there is a separate error code (SQLITE\_FULL) for that purpose.




### (779\) SQLITE\_CORRUPT\_INDEX



 The SQLITE\_CORRUPT\_INDEX result code means that SQLite detected
 an entry is or was missing from an index. This is a special case of
 the [SQLITE\_CORRUPT](rescode.html#corrupt) error code that suggests that the problem might
 be resolved by running the [REINDEX](lang_reindex.html) command, assuming no other
 problems exist elsewhere in the database file.




### (782\) SQLITE\_CANTOPEN\_FULLPATH



 The SQLITE\_CANTOPEN\_FULLPATH error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_CANTOPEN](rescode.html#cantopen) indicating that a file open operation failed because
 the operating system was unable to convert the filename into a full pathname.




### (787\) SQLITE\_CONSTRAINT\_FOREIGNKEY



 The SQLITE\_CONSTRAINT\_FOREIGNKEY error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a [foreign key constraint](foreignkeys.html) failed.




### (1032\) SQLITE\_READONLY\_DBMOVED



 The SQLITE\_READONLY\_DBMOVED error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_READONLY](rescode.html#readonly). The SQLITE\_READONLY\_DBMOVED error code indicates
 that a database cannot be modified because the database file has been
 moved since it was opened, and so any attempt to modify the database
 might result in database corruption if the processes crashes because the
 [rollback journal](lockingv3.html#rollback) would not be correctly named.




### (1034\) SQLITE\_IOERR\_FSYNC



 The SQLITE\_IOERR\_FSYNC error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error in the [VFS](vfs.html) layer
 while trying to flush previously written content out of OS and/or
 disk\-control buffers and into persistent storage. In other words,
 this code indicates a problem with the fsync() system call in unix
 or the FlushFileBuffers() system call in windows.




### (1038\) SQLITE\_CANTOPEN\_CONVPATH



 The SQLITE\_CANTOPEN\_CONVPATH error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_CANTOPEN](rescode.html#cantopen) used only by Cygwin [VFS](vfs.html) and indicating that
 the cygwin\_conv\_path() system call failed while trying to open a file.
 See also: [SQLITE\_IOERR\_CONVPATH](rescode.html#ioerr_convpath)


### (1043\) SQLITE\_CONSTRAINT\_FUNCTION



 The SQLITE\_CONSTRAINT\_FUNCTION error code is not currently used
 by the SQLite core. However, this error code is available for use
 by extension functions.




### (1288\) SQLITE\_READONLY\_CANTINIT



 The SQLITE\_READONLY\_CANTINIT result code originates in the xShmMap method
 of a [VFS](vfs.html) to indicate that the shared memory region used by [WAL mode](wal.html)
 exists buts its content is unreliable and unusable by the current process
 since the current process does not have write permission on the shared
 memory region. (The shared memory region for WAL mode is normally a
 file with a "\-wal" suffix that is mmapped into the process space. If
 the current process does not have write permission on that file, then it
 cannot write into shared memory.)
 
 Higher level logic within SQLite will normally intercept the error code
 and create a temporary in\-memory shared memory region so that the current
 process can at least read the content of the database. This result code
 should not reach the application interface layer.




### (1290\) SQLITE\_IOERR\_DIR\_FSYNC



 The SQLITE\_IOERR\_DIR\_FSYNC error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error in the [VFS](vfs.html) layer
 while trying to invoke fsync() on a directory. The unix [VFS](vfs.html) attempts
 to fsync() directories after creating or deleting certain files to
 ensure that those files will still appear in the filesystem following
 a power loss or system crash. This error code indicates a problem
 attempting to perform that fsync().




### (1294\) SQLITE\_CANTOPEN\_DIRTYWAL



 The SQLITE\_CANTOPEN\_DIRTYWAL result code is not used at this time.




### (1299\) SQLITE\_CONSTRAINT\_NOTNULL



 The SQLITE\_CONSTRAINT\_NOTNULL error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a [NOT NULL constraint](lang_createtable.html#notnullconst) failed.




### (1544\) SQLITE\_READONLY\_DIRECTORY



 The SQLITE\_READONLY\_DIRECTORY result code indicates that the database
 is read\-only because process does not have permission to create
 a journal file in the same directory as the database and the creation of
 a journal file is a prerequisite for writing.




### (1546\) SQLITE\_IOERR\_TRUNCATE



 The SQLITE\_IOERR\_TRUNCATE error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error in the [VFS](vfs.html) layer
 while trying to truncate a file to a smaller size.




### (1550\) SQLITE\_CANTOPEN\_SYMLINK



 The SQLITE\_CANTOPEN\_SYMLINK result code is returned by the
 [sqlite3\_open()](c3ref/open.html) interface and its siblings when the
 [SQLITE\_OPEN\_NOFOLLOW](c3ref/c_open_autoproxy.html) flag is used and the database file is
 a symbolic link.




### (1555\) SQLITE\_CONSTRAINT\_PRIMARYKEY



 The SQLITE\_CONSTRAINT\_PRIMARYKEY error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a [PRIMARY KEY constraint](lang_createtable.html#primkeyconst) failed.




### (1802\) SQLITE\_IOERR\_FSTAT



 The SQLITE\_IOERR\_FSTAT error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error in the [VFS](vfs.html) layer
 while trying to invoke fstat() (or the equivalent) on a file in order
 to determine information such as the file size or access permissions.




### (1811\) SQLITE\_CONSTRAINT\_TRIGGER



 The SQLITE\_CONSTRAINT\_TRIGGER error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a [RAISE function](lang_createtrigger.html#raise) within
 a [trigger](lang_createtrigger.html) fired, causing the SQL statement to abort.




### (2058\) SQLITE\_IOERR\_UNLOCK



 The SQLITE\_IOERR\_UNLOCK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within xUnlock method on the [sqlite3\_io\_methods](c3ref/io_methods.html) object.




### (2067\) SQLITE\_CONSTRAINT\_UNIQUE



 The SQLITE\_CONSTRAINT\_UNIQUE error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a [UNIQUE constraint](lang_createtable.html#uniqueconst) failed.




### (2314\) SQLITE\_IOERR\_RDLOCK



 The SQLITE\_IOERR\_RDLOCK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within xLock method on the [sqlite3\_io\_methods](c3ref/io_methods.html) object while trying
 to obtain a read lock.




### (2323\) SQLITE\_CONSTRAINT\_VTAB



 The SQLITE\_CONSTRAINT\_VTAB error code is not currently used
 by the SQLite core. However, this error code is available for use
 by application\-defined [virtual tables](vtab.html).




### (2570\) SQLITE\_IOERR\_DELETE



 The SQLITE\_IOERR\_DELETE error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within xDelete method on the [sqlite3\_vfs](c3ref/vfs.html) object.




### (2579\) SQLITE\_CONSTRAINT\_ROWID



 The SQLITE\_CONSTRAINT\_ROWID error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that a [rowid](lang_createtable.html#rowid) is not unique.




### (2826\) SQLITE\_IOERR\_BLOCKED



 The SQLITE\_IOERR\_BLOCKED error code is no longer used.




### (2835\) SQLITE\_CONSTRAINT\_PINNED



 The SQLITE\_CONSTRAINT\_PINNED error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that an [UPDATE trigger](lang_createtrigger.html) attempted
 do delete the row that was being updated in the middle of the update.




### (3082\) SQLITE\_IOERR\_NOMEM



 The SQLITE\_IOERR\_NOMEM error code is sometimes returned by the [VFS](vfs.html)
 layer to indicate that an operation could not be completed due to the
 inability to allocate sufficient memory. This error code is normally
 converted into [SQLITE\_NOMEM](rescode.html#nomem) by the higher layers of SQLite before
 being returned to the application.




### (3091\) SQLITE\_CONSTRAINT\_DATATYPE



 The SQLITE\_CONSTRAINT\_DATATYPE error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_CONSTRAINT](rescode.html#constraint) indicating that an insert or update attempted
 to store a value inconsistent with the column's declared type
 in a table defined as STRICT.




### (3338\) SQLITE\_IOERR\_ACCESS



 The SQLITE\_IOERR\_ACCESS error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xAccess method on the [sqlite3\_vfs](c3ref/vfs.html) object.




### (3594\) SQLITE\_IOERR\_CHECKRESERVEDLOCK



 The SQLITE\_IOERR\_CHECKRESERVEDLOCK error code is
 an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xCheckReservedLock method on the [sqlite3\_io\_methods](c3ref/io_methods.html) object.




### (3850\) SQLITE\_IOERR\_LOCK



 The SQLITE\_IOERR\_LOCK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error in the
 advisory file locking logic.
 Usually an SQLITE\_IOERR\_LOCK error indicates a problem obtaining
 a [PENDING lock](lockingv3.html#pending_lock). However it can also indicate miscellaneous
 locking errors on some of the specialized [VFSes](vfs.html) used on Macs.




### (4106\) SQLITE\_IOERR\_CLOSE



 The SQLITE\_IOERR\_CLOSE error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xClose method on the [sqlite3\_io\_methods](c3ref/io_methods.html) object.




### (4362\) SQLITE\_IOERR\_DIR\_CLOSE



 The SQLITE\_IOERR\_DIR\_CLOSE error code is no longer used.




### (4618\) SQLITE\_IOERR\_SHMOPEN



 The SQLITE\_IOERR\_SHMOPEN error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xShmMap method on the [sqlite3\_io\_methods](c3ref/io_methods.html) object
 while trying to open a new shared memory segment.




### (4874\) SQLITE\_IOERR\_SHMSIZE



 The SQLITE\_IOERR\_SHMSIZE error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xShmMap method on the [sqlite3\_io\_methods](c3ref/io_methods.html) object
 while trying to enlarge a ["shm" file](walformat.html#shm) as part of
 [WAL mode](wal.html) transaction processing. This error may indicate that
 the underlying filesystem volume is out of space.




### (5130\) SQLITE\_IOERR\_SHMLOCK



 The SQLITE\_IOERR\_SHMLOCK error code is no longer used.




### (5386\) SQLITE\_IOERR\_SHMMAP



 The SQLITE\_IOERR\_SHMMAP error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xShmMap method on the [sqlite3\_io\_methods](c3ref/io_methods.html) object
 while trying to map a shared memory segment into the process address space.




### (5642\) SQLITE\_IOERR\_SEEK



 The SQLITE\_IOERR\_SEEK error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xRead or xWrite methods on the [sqlite3\_io\_methods](c3ref/io_methods.html) object
 while trying to seek a file descriptor to the beginning point of the
 file where the read or write is to occur.




### (5898\) SQLITE\_IOERR\_DELETE\_NOENT



 The SQLITE\_IOERR\_DELETE\_NOENT error code
 is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating that the
 xDelete method on the [sqlite3\_vfs](c3ref/vfs.html) object failed because the
 file being deleted does not exist.




### (6154\) SQLITE\_IOERR\_MMAP



 The SQLITE\_IOERR\_MMAP error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating an I/O error
 within the xFetch or xUnfetch methods on the [sqlite3\_io\_methods](c3ref/io_methods.html) object
 while trying to map or unmap part of the database file into the
 process address space.




### (6410\) SQLITE\_IOERR\_GETTEMPPATH



 The SQLITE\_IOERR\_GETTEMPPATH error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) indicating that the [VFS](vfs.html) is unable to determine
 a suitable directory in which to place temporary files.




### (6666\) SQLITE\_IOERR\_CONVPATH



 The SQLITE\_IOERR\_CONVPATH error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) used only by Cygwin [VFS](vfs.html) and indicating that
 the cygwin\_conv\_path() system call failed.
 See also: [SQLITE\_CANTOPEN\_CONVPATH](rescode.html#cantopen_convpath)


### (6922\) SQLITE\_IOERR\_VNODE



 The SQLITE\_IOERR\_VNODE error code is a code reserved for use
 by extensions. It is not used by the SQLite core.




### (7178\) SQLITE\_IOERR\_AUTH



 The SQLITE\_IOERR\_AUTH error code is a code reserved for use
 by extensions. It is not used by the SQLite core.




### (7434\) SQLITE\_IOERR\_BEGIN\_ATOMIC



 The SQLITE\_IOERR\_BEGIN\_ATOMIC error code indicates that the
 underlying operating system reported and error on the
 [SQLITE\_FCNTL\_BEGIN\_ATOMIC\_WRITE](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlbeginatomicwrite) file\-control. This only comes
 up when [SQLITE\_ENABLE\_ATOMIC\_WRITE](compile.html#enable_atomic_write) is enabled and the database
 is hosted on a filesystem that supports atomic writes.




### (7690\) SQLITE\_IOERR\_COMMIT\_ATOMIC



 The SQLITE\_IOERR\_COMMIT\_ATOMIC error code indicates that the
 underlying operating system reported and error on the
 [SQLITE\_FCNTL\_COMMIT\_ATOMIC\_WRITE](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlcommitatomicwrite) file\-control. This only comes
 up when [SQLITE\_ENABLE\_ATOMIC\_WRITE](compile.html#enable_atomic_write) is enabled and the database
 is hosted on a filesystem that supports atomic writes.




### (7946\) SQLITE\_IOERR\_ROLLBACK\_ATOMIC



 The SQLITE\_IOERR\_ROLLBACK\_ATOMIC error code indicates that the
 underlying operating system reported and error on the
 [SQLITE\_FCNTL\_ROLLBACK\_ATOMIC\_WRITE](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlrollbackatomicwrite) file\-control. This only comes
 up when [SQLITE\_ENABLE\_ATOMIC\_WRITE](compile.html#enable_atomic_write) is enabled and the database
 is hosted on a filesystem that supports atomic writes.




### (8202\) SQLITE\_IOERR\_DATA



 The SQLITE\_IOERR\_DATA error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) used only by [checksum VFS shim](cksumvfs.html) to indicate that
 the checksum on a page of the database file is incorrect.




### (8458\) SQLITE\_IOERR\_CORRUPTFS



 The SQLITE\_IOERR\_CORRUPTFS error code is an [extended error code](rescode.html#pve)
 for [SQLITE\_IOERR](rescode.html#ioerr) used only by a VFS to indicate that a seek or read
 failure was due to the request not falling within the file's boundary
 rather than an ordinary device failure. This often indicates a
 corrupt filesystem.





*This page last modified on [2023\-09\-14 14:42:56](https://sqlite.org/docsrc/honeypot) UTC* 










































































































































































































































































