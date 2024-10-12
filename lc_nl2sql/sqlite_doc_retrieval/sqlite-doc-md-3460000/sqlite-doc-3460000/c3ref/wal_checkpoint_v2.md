




Checkpoint a database




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Checkpoint a database




> ```
> 
> int sqlite3_wal_checkpoint_v2(
>   sqlite3 *db,                    /* Database handle */
>   const char *zDb,                /* Name of attached database (or NULL) */
>   int eMode,                      /* SQLITE_CHECKPOINT_* value */
>   int *pnLog,                     /* OUT: Size of WAL log in frames */
>   int *pnCkpt                     /* OUT: Total number of frames checkpointed */
> );
> 
> ```



The sqlite3\_wal\_checkpoint\_v2(D,X,M,L,C) interface runs a checkpoint
operation on database X of [database connection](../c3ref/sqlite3.html) D in mode M. Status
information is written back into integers pointed to by L and C.
The M parameter must be a valid [checkpoint mode](../c3ref/c_checkpoint_full.html):



SQLITE\_CHECKPOINT\_PASSIVE
Checkpoint as many frames as possible without waiting for any database
readers or writers to finish, then sync the database file if all frames
in the log were checkpointed. The [busy\-handler callback](../c3ref/busy_handler.html)
is never invoked in the SQLITE\_CHECKPOINT\_PASSIVE mode.
On the other hand, passive mode might leave the checkpoint unfinished
if there are concurrent readers or writers.


SQLITE\_CHECKPOINT\_FULL
This mode blocks (it invokes the
[busy\-handler callback](../c3ref/busy_handler.html)) until there is no
database writer and all readers are reading from the most recent database
snapshot. It then checkpoints all frames in the log file and syncs the
database file. This mode blocks new database writers while it is pending,
but new database readers are allowed to continue unimpeded.


SQLITE\_CHECKPOINT\_RESTART
This mode works the same way as SQLITE\_CHECKPOINT\_FULL with the addition
that after checkpointing the log file it blocks (calls the
[busy\-handler callback](../c3ref/busy_handler.html))
until all readers are reading from the database file only. This ensures
that the next writer will restart the log file from the beginning.
Like SQLITE\_CHECKPOINT\_FULL, this mode blocks new
database writer attempts while it is pending, but does not impede readers.


SQLITE\_CHECKPOINT\_TRUNCATE
This mode works the same way as SQLITE\_CHECKPOINT\_RESTART with the
addition that it also truncates the log file to zero bytes just prior
to a successful return.



If pnLog is not NULL, then \*pnLog is set to the total number of frames in
the log file or to \-1 if the checkpoint could not run because
of an error or because the database is not in [WAL mode](../wal.html). If pnCkpt is not
NULL,then \*pnCkpt is set to the total number of checkpointed frames in the
log file (including any that were already checkpointed before the function
was called) or to \-1 if the checkpoint could not run due to an error or
because the database is not in WAL mode. Note that upon successful
completion of an SQLITE\_CHECKPOINT\_TRUNCATE, the log file will have been
truncated to zero bytes and so both \*pnLog and \*pnCkpt will be set to zero.


All calls obtain an exclusive "checkpoint" lock on the database file. If
any other process is running a checkpoint operation at the same time, the
lock cannot be obtained and SQLITE\_BUSY is returned. Even if there is a
busy\-handler configured, it will not be invoked in this case.


The SQLITE\_CHECKPOINT\_FULL, RESTART and TRUNCATE modes also obtain the
exclusive "writer" lock on the database file. If the writer lock cannot be
obtained immediately, and a busy\-handler is configured, it is invoked and
the writer lock retried until either the busy\-handler returns 0 or the lock
is successfully obtained. The busy\-handler is also invoked while waiting for
database readers as described above. If the busy\-handler returns 0 before
the writer lock is obtained or while waiting for database readers, the
checkpoint operation proceeds from that point in the same way as
SQLITE\_CHECKPOINT\_PASSIVE \- checkpointing as many frames as possible
without blocking any further. SQLITE\_BUSY is returned in this case.


If parameter zDb is NULL or points to a zero length string, then the
specified operation is attempted on all WAL databases [attached](../lang_attach.html) to
[database connection](../c3ref/sqlite3.html) db. In this case the
values written to output parameters \*pnLog and \*pnCkpt are undefined. If
an SQLITE\_BUSY error is encountered when processing one or more of the
attached WAL databases, the operation is still attempted on any remaining
attached databases and SQLITE\_BUSY is returned at the end. If any other
error occurs while processing an attached database, processing is abandoned
and the error code is returned to the caller immediately. If no error
(SQLITE\_BUSY or otherwise) is encountered while processing the attached
databases, SQLITE\_OK is returned.


If database zDb is the name of an attached database that is not in WAL
mode, SQLITE\_OK is returned and both \*pnLog and \*pnCkpt set to \-1\. If
zDb is not NULL (or a zero length string) and is not the name of any
attached database, SQLITE\_ERROR is returned to the caller.


Unless it returns SQLITE\_MISUSE,
the sqlite3\_wal\_checkpoint\_v2() interface
sets the error information that is queried by
[sqlite3\_errcode()](../c3ref/errcode.html) and [sqlite3\_errmsg()](../c3ref/errcode.html).


The [PRAGMA wal\_checkpoint](../pragma.html#pragma_wal_checkpoint) command can be used to invoke this interface
from SQL.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


