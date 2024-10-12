




WAL\-mode File Format




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










WAL\-mode File Format


►
Table Of Contents
[1\. Files On Disk](#files_on_disk)
[1\.1\. The Main Database File](#the_main_database_file)
[1\.2\. The Write\-Ahead\-Log or "\-wal" File](#the_write_ahead_log_or_wal_file)
[1\.3\. The Wal\-Index or "\-shm" file](#the_wal_index_or_shm_file)
[1\.4\. File Lifecycles](#file_lifecycles)
[1\.5\. Variations](#variations)
[2\. The WAL\-Index File Format](#the_wal_index_file_format)
[2\.1\. The WAL\-Index Header](#the_wal_index_header)
[2\.1\.1\. The mxFrame field](#the_mxframe_field)
[2\.1\.2\. The nBackfill field](#the_nbackfill_field)
[2\.1\.3\. WAL Locks](#wal_locks)
[2\.2\. WAL\-Index Hash Tables](#wal_index_hash_tables)
[2\.3\. Locking Matrix](#locking_matrix)
[2\.3\.1\. How the various locks are used](#how_the_various_locks_are_used)
[2\.3\.2\. Operations that require locks and which locks those operations use](#operations_that_require_locks_and_which_locks_those_operations_use)
[3\. Recovery](#recovery)




This document describes low\-level details on how [WAL mode](wal.html) is
implemented on unix and windows.



The separate [file format](fileformat2.html) description provides details on the
structure of a database file and of the write\-head log file used in
[WAL mode](wal.html). But details of the locking protocol and of the format
of the WAL\-index are deliberately omitted since those details
are left to discretion of individual [VFS](vfs.html) implementations. This
document fills in those missing details for the unix and windows [VFSes](vfs.html).



For completeness, some of the higher level formatting information
contains in the [file format](fileformat2.html) document and elsewhere is replicated here,
when it pertains to WAL mode processing.



# 1\. Files On Disk


When in active use, the state of a WAL mode database is described
by three separate files:



1. The main database file with an arbitrary name "X".
2. The write\-ahead log file, usually named "X\-wal".
3. The wal\-index file, usually named "X\-shm".


## 1\.1\. The Main Database File


The format of the main database file is as described in the
[file format](fileformat2.html) document. The [file format version numbers](fileformat2.html#vnums) at offsets
18 and 19 into the main database must both be 2 to indicate that the
database is in WAL mode. The main database may have an arbitrary
name allowed by the underlying filesystem. No special file suffixes
are required, though ".db", ".sqlite", and ".sqlite3" seem to be
popular choices.



## 1\.2\. The Write\-Ahead\-Log or "\-wal" File


The write\-ahead log or "wal" file is a roll\-forward journal
that records transactions that have been committed but not yet applied
to the main database. Details on the format of the wal file are
describe in the [WAL format](fileformat2.html#walformat) subsection of the main [file format](fileformat2.html)
document. The wal file is named by appending the four characters
"\-wal" to the end of the name of the main database file. Except
on 8\+3 filesystems, such names are not allowed, and in that case
the file suffix is changed to ".WAL". But as 8\+3 filesystems are
increasingly rare, that exceptional case can usually be ignored.




## 1\.3\. The Wal\-Index or "\-shm" file


The wal\-index file or "shm" file is not actually used as a file.
Rather, individual database clients mmap the shm file and use it
as shared memory for coordinating access to the database and as a cache
for quickly locating frame within the wal file. The name
of the shm file is the main database file name with the four characters
"\-shm" appended. Or, for 8\+3 filesystems, the shm file is the main
database file with the suffix changed to ".SHM".



The shm does not contain any database content and is not required
to recover the database following a crash. For that reason, the first
client to connect to a quiescent database will normally truncate the
shm file if it exists. Since the content of the shm file does not need
to be preserved across a crash, the shm file is never fsync()\-ed to disk.
In fact, if there were a mechanism by which SQLite could tell the 
operating system to never persist the shm file to disk but always hold
it in cache memory, SQLite would use that mechanism to avoid any
unnecessary disk I/O associated with the shm file. However, no such
mechanism exists in standard posix.



Because the shm is only used to coordinate access between concurrent
clients, the shm file is omitted if [exclusive locking mode](pragma.html#pragma_locking_mode)
is set, as an optimization. When [exclusive locking mode](pragma.html#pragma_locking_mode) is set,
SQLite uses heap memory in place of the memory\-mapped shm file.



## 1\.4\. File Lifecycles


When a WAL mode database is in active use, all three of the above
files usually exist. Except, the Wal\-Index file is omitted if
[exclusive locking mode](pragma.html#pragma_locking_mode) is set.



If the last client using the database shuts down cleanly by
calling [sqlite3\_close()](c3ref/close.html), then a [checkpoint](wal.html#ckpt) is run automatically
in order to transfer all information from the wal file
over into the main database, and both the shm file
and the wal file are unlinked. Thus, when the database is not in
use by any client, it is usually the case that only the main
database file exists on disk.
However, if the last client did not call [sqlite3\_close()](c3ref/close.html) before it
shut down, or if the last client to disconnect was a read\-only client,
then the final cleanup operation does not occur and the
shm and wal files may still exist on disk even when the database is
not in use.



## 1\.5\. Variations


When [PRAGMA locking\_mode\=EXCLUSIVE](pragma.html#pragma_locking_mode) (exclusive locking mode) is set,
only a single client is allowed to have the database open at one time. Since
only a single client can use the database, the shm file is omitted.
The single client uses a buffer in heap memory as a substitute for the
memory\-mapped shm file.



If a read/write client invokes
[sqlite3\_file\_control](c3ref/file_control.html)([SQLITE\_FCNTL\_PERSIST\_WAL](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlpersistwal)) prior to shutdown,
then at shutdown a checkpoint is still run, but the shm file and wal
file are not deleted.
This allows subsequent read\-only clients to connect to and read the
database.




# 2\. The WAL\-Index File Format



The WAL\-index or "shm" file is used to coordinate access to the database
by multiple clients, and as a cache to help clients quickly locate frames
within the wal file.




Because the shm file is not involved in recovery, the shm file does not
need to be machine byte\-order independent. Hence, numeric values in
the shm file are written in the native byte order of the host computer,
rather than being converted into a specific cross\-platform byte order as
is done with the main database file and the wal file.




The shm file consists of one or more hash tables, where each hash table
is 32768 bytes in size. Except, a 136\-byte header is carved out of the
front of the very first hash table, so the first hash table is only
32632 bytes in size. The total size of the shm file is always a multiple
of 32768\. In most cases, the total size of the shm file is exactly 32768
bytes. The shm file only needs to grow beyond a single hash table if
when the wal file grows very large (more than 4079 frames). Since the
default [automatic checkpoint threshold](c3ref/wal_autocheckpoint.html) is
1000, WAL files rare reach the 4079 threshold needed to make the shm file
grow.



## 2\.1\. The WAL\-Index Header


The first 136 bytes of the shm file are a header. The shm header has
three main divisions as follows:




*WAL\-Index Header Divisions*  



| Bytes | Description |
| --- | --- |
| 0\..47 | First copy of the WAL Index Information |
| 48\..95 | Second copy of the WAL Index Information |
| 96\..135 | Checkpoint Information and Locks |



Individual fields of the shm header, except for the
salt values copied from the WAL header, are unsigned integers
in the native byte\-order of the host machine. The salt values
are exact copies from the WAL header and are in whatever byte
order is used by the WAL file.
The size of integers may be 8, 16, 32, or 64 bits.
A detailed breakout of the individual fields of the shm header
follows:




*WAL\-Index Header Details*  



| Bytes | Name | Meaning |
| --- | --- | --- |
| 0\..3 | iVersion | The WAL\-index format version number. Always 3007000\. |
| 4\..7 |  | Unused padding space. Must be zero. |
| 8\..11 | iChange | Unsigned integer counter, incremented with each transaction |
| 12 | isInit | The "isInit" flag. 1 when the shm file has been initialized. |
| 13 | bigEndCksum | True if the WAL file uses big\-ending checksums. 0 if the WAL  uses little\-endian checksums. |
| 14\..15 | szPage | The database page size in bytes, or 1 if the page size is 65536\. |
| 16\..19 | mxFrame | Number of valid and committed frames in the WAL file. |
| 20\..23 | nPage | Size of the database file in pages. |
| 24\..31 | aFrameCksum | Checksum of the last frame in the WAL file. |
| 32\..39 | aSalt | The two salt value copied from the WAL file header. These values are in the byte\-order of the WAL file, which might be different from the native byte\-order of the machine. |
| 40\..47 | aCksum | A checksum over bytes 0 through 39 of this header. |
| 48\..95 |  | A copy of bytes 0 through 47 of this header. |
| 96\..99 | nBackfill | Number of WAL frames that have already been backfilled into the database  by prior checkpoints |
| 100\..119 | read\-mark\[0\..4] | Five "read marks". Each read mark is a 32\-bit unsigned integer (4 bytes). |
| 120\..127 |  | Unused space set aside for 8 file locks. |
| 128\..132 | nBackfillAttempted | Number of WAL frames that have attempted to be backfilled but which might  not have been backfilled successfully. |
| 132\..136 |  | Unused space reserved for further expansion. |




### 2\.1\.1\. The mxFrame field


The 32\-bit unsigned integer at offset 16 (and repeated at offset 64\)
is the number of valid frames in the WAL. Because WAL frame are numbered
starting with 1, mxFrame is also the index of the last valid commit frame
in the WAL. A commit frame is a frame that has a non\-zero "size of database"
value in bytes 4 through 7 of the frame header, and that indicates the end
of a transaction.



When mxFrame field is zero, it indicates that the WAL is empty and that
all content should be obtained directly from the database file.



When mxFrame is equal to [nBackfill](walformat.html#nbackfill), that indicates that all content
in the WAL has been written back into the database.
In that case, all content can be read directly from the database.
Furthermore, the next writer is free to [reset the WAL](fileformat2.html#walreset) if no other
connections hold locks on WAL\_READ\_LOCK(N) for N\>0\.



The mxFrame value is always greater than or equal to both
[nBackfill](walformat.html#nbackfill) and nBackfillAttempted.





### 2\.1\.2\. The nBackfill field


The 32\-bit unsigned integer at offset 128 in the WAL\-index header
is called the "nBackfill".
this field holds the number of frames in the WAL file which
have been copied back into the main database.



The nBackfill number is never greater than [mxFrame](walformat.html#mxframe).
When nBackfill equals [mxFrame](walformat.html#mxframe), that means that the WAL content
has been completely written back into the database and it is
ok to [reset the WAL](fileformat2.html#walreset) if there are no locks held on any of WAL\_READ\_LOCK(N)
for N\>0\.



The nBackfill can only be increased while holding the
WAL\_CKPT\_LOCK. However, nBackfill is changed to zero
during a [WAL reset](fileformat2.html#walreset), and this happens while holding
the WAL\_WRITE\_LOCK.




### 2\.1\.3\. WAL Locks


Eight bytes of space are set aside in the header to support
file locking using the xShmLock() method in the [sqlite3\_io\_methods](c3ref/io_methods.html)
object. These eight bytes are never read nor written by SQLite since
some VFSes (ex: Windows) might implement locks using mandatory file locks.



These are the eight locks supported:




*WAL\-Index Locks Controlled By xShmLock()*  



| Name | Offset | |
| --- | --- | --- |
| xShmLock | File |
| WAL\_WRITE\_LOCK | 0 | 120 |
| WAL\_CKPT\_LOCK | 1 | 121 |
| WAL\_RECOVER\_LOCK | 2 | 122 |
| WAL\_READ\_LOCK(0\) | 3 | 123 |
| WAL\_READ\_LOCK(1\) | 4 | 124 |
| WAL\_READ\_LOCK(2\) | 5 | 125 |
| WAL\_READ\_LOCK(3\) | 6 | 126 |
| WAL\_READ\_LOCK(4\) | 7 | 127 |



*TBD: More information about the header*


## 2\.2\. WAL\-Index Hash Tables


The hash tables in the shm file are designed to answer the
following question quickly:




> *FindFrame(P,M):
> Given a page number P and a maximum WAL frame index M,
> return the largest WAL frame index for page P that does not exceed M, 
> or return NULL if there are no frames for page P that do not exceed M.*



Let the datatypes "u8", "u16", and "u32" mean unsigned integers of
length 8, 16, and 32 bits, respectively. Then, the first 32768\-byte unit
of the shm file is organized as follows:




> ```
> 
> u8 aWalIndexHeader[136];
> u32 aPgno[4062];
> u16 aHash[8192];
> 
> ```


The second and all subsequent 32768\-byte units of the shm file are
like this:




> ```
> 
> u32 aPgno[4096];
> u16 aHash[8192];
> 
> ```


Collectively, the aPgno entries record the database page number stored
in all frames of the WAL file. The aPgno\[0] entry on the first hash table
records the database page number stored in the very first frame in the WAL 
file. The aPgno\[i] entry from the first hash table is the database page number
for the i\-th frame in the WAL file. The aPgno\[k] entry for the second
hash table is the database page number for the (k\+4062\)\-th frame in the
WAL file. The aPgno\[k] entry for the n\-th 32768\-byte hash table in the
shm file (for n\>1\) holds the database page number stored in the
(k\+4062\+4096\*(n\-2\))\-th frame of the WAL file.



Here is a slightly different way to describe the aPgno values:
If you think of all aPgno values as a contiguous array, then
the database page number stored in the i\-th frame of the WAL file
is stored in aPgno\[i]. Of course, aPgno is not a contiguous array.
The first 4062 entries are on the first 32768\-byte unit of the shm
file and subsequent values are in 4096 entry chunks in later units
of the shm file.



One way to compute FindFrame(P,M) would be to scan the aPgno
array starting with the M\-th entry and working backwards towards
the beginning and return J where aPgno\[J]\=\=P. Such an algorithm would
work, and it would be faster than searching the whole WAL file for
the latest frame with page number P. But the search can be made
much faster still by using the aHash structure.



A database page number P is mapped into a hash value
using the following hash function:




> h \= (P \* 383\)%8192


This function maps every page number into an integer between 0
and 8191 inclusive. The aHash field of each 32768\-byte shm file unit
maps P values into indexes of the aPgno field of the same unit as
follows:



1. Compute the hash value: h \= P \* 383
2. Let X be the largest set of consecutive integers {h, h\+1, h\+2, ..., h\+N}
 such that for every j in X, aPgno\[j%8192]!\=0\. The X set will be empty
 if aPgno\[h%8192]\=\=0\. The X set is easily computed by starting with
 the value h%8192, and adding h%8192 to X and incrementing h until
 encountering the first aPgno\[h%8192] entry that is zero.
3. The set X contains the index in aPgno of every entry in the current
 32768\-byte unit of the shm file that might possible be a solution
 to the FindFrame(P,M) function. Each of these entries must be
 checked separately to ensure that the aPgno value is P and that the
 frame number does not exceed M. The largest frame number that passes
 those two tests is the answer.


Each entry in the aPgno array has a single corresponding entry
in the aHash array. There are more available slots in aHash than
there are in aPgno. The unused slots in aHash are filled with zero.
And since there are guaranteed to be unused slots in aHash, that means
the loop that computes X is guaranteed to terminate. The expected size
of X is less than 2\. The worst case is that X will be the same as the
number of entries in aPgno, in which case the algorithm runs at about
the same speed as a linear scan of aPgno. But that worst case performance
is exceedingly rare. Usually, the size of X will be small and the use
of the aHash array allows one to compute FindFrame(P,M) much faster.



Here is an alternative way of describing the hash look\-up algorithm:
Start with h \= (P \* 383\)%8192 and look at aHash\[h] and subsequent entries,
wrapping around to zero when h reaches 8192, until finding an entry with
aHash\[h]\=\=0\. All aPgno entries having a page number of P will have an
index that is one of the aHash\[h] values thusly computed.
But not all the computed aHash\[h] values will
meet the matching criteria, so you must check them independently. The
speed advantage comes about because normally this set of h values is
very small.



Note that each 32768\-byte unit of the shm file has its own aHash and
aPgno arrays. The aHash array for a single unit is only helpful in finding
aPgno entries in that same unit. The overall FindFrame(P,M) function
needs to do hash lookups beginning with the latest unit and working
backwards to the oldest unit until it finds an answer.



## 2\.3\. Locking Matrix


Access is coordinated in WAL mode using both the legacy DELETE\-mode
locks controlled by the xLock and xUnlock methods of the [sqlite3\_io\_methods](c3ref/io_methods.html)
object and the WAL locks controlled by the xShmLock method of the
[sqlite3\_io\_methods](c3ref/io_methods.html) object.



Conceptually, there is just a single DELETE\-mode lock. The DELETE\-mode
lock for a single database connection can be in exactly one of the
following states:


1. SQLITE\_LOCK\_NONE (unlocked)
2. SQLITE\_LOCK\_SHARED (reading)
3. SQLITE\_LOCK\_RESERVED (reading, waiting to write)
4. SQLITE\_LOCK\_PENDING (new readers blocked, waiting to write)
5. SQLITE\_LOCK\_EXCLUSIVE (writing)


The DELETE\-mode locks are stored on the [lock\-byte page](fileformat2.html#lockbyte) of the
main database file.
Only SQLITE\_LOCK\_SHARED and SQLITE\_LOCK\_EXCLUSIVE are factors for WAL\-mode
databases.
The other locking states are used in rollback\-mode, but not in WAL\-mode.



The [WAL\-mode locks](walformat.html#locks) are described above.



### 2\.3\.1\. How the various locks are used


The following rules show how each of the locks is used.



* **SQLITE\_LOCK\_SHARED**



All connections hold SQLITE\_LOCK\_SHARED continuously while attached
to a WAL\-mode database. This is true for both read/write connections
and read\-only connections.
The SQLITE\_LOCK\_SHARED lock is held even by connections that are
not within transaction.
This is different from rollback mode, where the SQLITE\_LOCK\_SHARED is
released at the end of each transaction.
* **SQLITE\_LOCK\_EXCLUSIVE**



Connections hold an exclusive lock when change in between WAL mode
and any of the various rollback\-modes. Connections might also attempt to
obtain an EXCLUSIVE lock when they disconnect from WAL mode. If
a connection is able to obtain an EXCLUSIVE lock, that means it is the
only connection to the database and so it may attempt to checkpoint
and then delete the WAL\-index and WAL files.



When a connection is holding a SHARED lock on the main database,
that will prevent any other connection from acquiring the EXCLUSIVE
lock, which in turn prevents the WAL\-index and WAL files from being
deleted out from under other users, and prevents a transition out of
WAL\-mode while other users are accessing the database in WAL\-mode.
* **WAL\_WRITE\_LOCK**



The WAL\_WRITE\_LOCK is only locked exclusively. There is never a shared
lock taken on WAL\_WRITE\_LOCK.



An EXCLUSIVE WAL\_WRITE\_LOCK is held by any connection that is appending
content to the end of the WAL. Hence, only a single process at a time
can append content to the WAL. If a [WAL reset](fileformat2.html#walreset) occurs as a consequence of
a write, then the [nBackfill](walformat.html#nbackfill) field of the WAL\-index header is reset to
zero while holding this lock.


An EXCLUSIVE is also held WAL\_WRITE\_LOCK, and on several other locking
bytes, when a connection is running [recovery](walformat.html#recovery) on the shared WAL\-index.
* **WAL\_CKPT\_LOCK**



The WAL\_CKPT\_LOCK is only locked exclusively. There is never a shared
lock taken on WAL\_CKPT\_LOCK.



An EXCLUSIVE WAL\_CKPT\_LOCK is held by any connection that is running
a [checkpoint](wal.html#ckpt). The [nBackfill](walformat.html#nbackfill) field of the WAL\-index header may be
increased while holding this exclusive lock, but it may not be decreased.


An EXCLUSIVE is also held WAL\_CKPT\_LOCK, and on several other locking
bytes, when a connection is running [recovery](walformat.html#recovery) on the shared WAL\-index.
* **WAL\_RECOVER\_LOCK**



The WAL\_RECOVER\_LOCK is only locked exclusively. There is never a shared
lock taken on WAL\_RECOVER\_LOCK.



An EXCLUSIVE WAL\_RECOVER\_LOCK is held by any connection that is running
[recovery](walformat.html#recovery) to reconstruct the shared WAL\-index.



A read\-only connection that is rebuilding its private heap\-memory WAL\-index
does not hold this lock. (It cannot, since read\-only connections are not
allowed to hold any exclusive locks.) This lock is only held when rebuilding
the global shared WAL\-index contained in the memory\-mapped SHM file.



In addition to locking this byte, a connection running [recovery](walformat.html#recovery) also
gets an exclusive lock on all other WAL locks except for WAL\_READ\_LOCK(0\).
* **WAL\_READ\_LOCK(N)**



There are five separate read locks, numbers 0 through 4\.
Read locks may be either SHARED or EXCLUSIVE.
Connections obtain a shared lock on one of the read locks bytes while
they are within a transaction.
Connections also obtain an exclusive lock on read locks, one at a time,
for the brief moment while they are updating the values of the corresponding
read\-marks.
Read locks 1 through 4 are held exclusively when running [recovery](walformat.html#recovery).



Each read lock byte corresponds to one of the five 32\-bit read\-mark
integers located in bytes 100 through 119 of the WAL\-index header, as
follows:





| Lock Name | Lock offset | Read\-mark name | Read\-mark offset |
| --- | --- | --- | --- |
| WAL\_READ\_LOCK(0\) | 123 | read\-mark\[0] | 100\..103 |
| WAL\_READ\_LOCK(1\) | 124 | read\-mark\[1] | 104\..107 |
| WAL\_READ\_LOCK(2\) | 125 | read\-mark\[2] | 108\..111 |
| WAL\_READ\_LOCK(3\) | 126 | read\-mark\[3] | 112\..115 |
| WAL\_READ\_LOCK(4\) | 127 | read\-mark\[4] | 116\..119 |




When a connection holds a shared lock on WAL\_READ\_LOCK(N), that is a
promise by the connection that it will use the WAL and not the database
file for any database pages that are modified by the first
read\-mark\[N] entries in the WAL.
The read\-mark\[0] is always zero. If a connection holds a shared lock
on WAL\_READ\_LOCK(0\), that means the connection expects to be able to ignore
the WAL and read any content it wants from the main database.
If N\>0 then the connection is free to use more of the WAL file beyond
read\-mark\[N] if it wants to, up to the first mxFrame frames.
But when a connection holds a shared lock on WAL\_READ\_LOCK(0\), that is a
promise that it will never read content from the WAL
and will acquire all content directly from the main database.



When a checkpoint runs, if it sees a lock on WAL\_READ\_LOCK(N), then it
must not move WAL content into the main database for more than the first
read\-mark\[N] frames. Were it to do so, it would overwrite content that
the process holding the lock was expecting to be able to read out of the
main database file. A consequence of if this is that f the WAL file
contains more than read\-mark\[N] frames (if mxFrame\>read\-mark\[N]
for any read\-mark for which WAL\_READ\_LOCK(N) is held by another process),
then the checkpoint cannot run to completion.



When a writer wants to [reset the WAL](fileformat2.html#walreset), it must ensure that there are
no locks on WAL\_READ\_LOCK(N) for N\>0 because such locks indicate
that some other connection is still using the current WAL file and 
a [WAL reset](fileformat2.html#walreset) would delete content out from those other connections. It is
ok for a [WAL reset](fileformat2.html#walreset) to occur if other connections are holding WAL\_READ\_LOCK(0\)
because by holding WAL\_READ\_LOCK(0\), those other connections are promising
not to use any content from the WAL.


### 2\.3\.2\. Operations that require locks and which locks those operations use


* **Transition into and out of WAL\-mode**


The SQLITE\_LOCK\_EXCLUSIVE lock must be held by a connection that wants
to transition into our out of WAL mode.
Transitioning into WAL mode is, therefore, just like any other write
transaction, since every write transaction in rollback mode requires
the SQLITE\_LOCK\_EXCLUSIVE lock.
If the database file is already in WAL mode (hence if the desire it to change
it back into rollback mode) and if there are two
or more connections to the database, then each of these connections will
be holding an SQLITE\_LOCK\_SHARED lock. That means that the
SQLITE\_LOCK\_EXCLUSIVE cannot be obtained, and the transition out of
WAL mode will not be allowed. This prevents one connection from deleting
WAL mode out from under another. It also means that the only way to move
a database from WAL mode into rollback mode is to close all but one
connection to the database.
* **Close a connection to a WAL mode database**


When a database connection closes (via [sqlite3\_close()](c3ref/close.html) or
[sqlite3\_close\_v2()](c3ref/close.html)), an attempt is made to acquire
SQLITE\_LOCK\_EXCLUSIVE. If this attempt is successful, that means
the connection that is closing is the last connection to the database.
In that case, it is desirable to clean up the WAL and WAL\-index files,
so the closing connection runs a [checkpoint](wal.html#ckpt) (while holding
SQLITE\_LOCK\_EXCLUSIVE) and the deletes both the WAL and WAL\-index files.
The SQLITE\_LOCK\_EXCLUSIVE is not released until after both the
WAL and WAL\-index files have been deleted.



If the application invokes
[sqlite3\_file\_control](c3ref/file_control.html)([SQLITE\_FCNTL\_PERSIST\_WAL](c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlpersistwal)) on the database
connection prior to closing, then the final checkpoint is still
run but the WAL and WAL\-index files are
not deleted as they normally would be.
This leaves the database in a state that allows other processes
without write permission on the database, WAL, or WAL\-index files
to open the database read\-only.
If the WAL and WAL\-index files are missing, then a process that
lacks permission to create and initialize those files will not be
able to open the database, unless the database is designated
as immutable using the [immutable query parameter](uri.html#uriimmutable).
* **Reconstruct the global shared WAL\-index during [recovery](walformat.html#recovery)**


All of the WAL\-index locks, except for WAL\_READ\_LOCK(0\),
are held exclusively while reconstructing the global shared WAL\-index
during [recovery](walformat.html#recovery).
* **Append a new transaction to the end of the WAL**


An exclusive lock is held on WAL\_WRITE\_LOCK while adding new
frame onto the end of a WAL file.
* **Read content from the database and WAL as part of a transaction**
* **Run a checkpoint**
* **Reset the WAL file**


A [WAL reset](fileformat2.html#walreset) means to rewind the WAL and start adding new frames
at the beginning. This occurs while appending new frames to a WAL
that has [mxFrame](walformat.html#mxframe) equal to [nBackfill](walformat.html#nbackfill) and which has no locks on
WAL\_READ\_LOCK(1\) through WAL\_READ\_LOCK(4\). The WAL\_WRITE\_LOCK is
held.



# 3\. Recovery



Recovery is the process of rebuilding the WAL\-index so that it is
synchronized with the WAL.




Recovery is run by the first thread to connect to a WAL\-mode database.
Recovery restores the WAL\-index so that it accurately describes the
WAL file. If there is no WAL file present when the first thread connects
to the database, there is nothing to recover, but the recovery process
still runs to initialize the WAL\-index.




If the WAL\-index is implemented as a memory\-mapped file and that file is
read\-only to the first thread to connect, then that thread creates an
private heap\-memory ersazt WAL\-index and runs the recovery routine to
populate that private WAL\-index. The same data results, but it is held
privately rather that being written into the public shared memory area.




Recovery works by doing a single pass over the WAL, from beginning to end.
The checksums are verified on each frame of the WAL as it is read. The
scan stops at the end of the file or at the first invalid checksum.
The [mxFrame](walformat.html#mxframe) field is set to the index of the last valid commit frame
in WAL. Since WAL frame numbers are indexed starting with 1, mxFrame is
also the number of valid frames in the WAL. A "commit frame" is a frame
that has a non\-zero value in bytes 4 through 7 of the frame header.
Since the recovery procedure has no way of knowing how many frames of the
WAL might have previously been copied back into the database, it initializes
the [nBackfill](walformat.html#nbackfill) value to zero.




During recovery of the global shared\-memory WAL\-index, exclusive locks are
held on WAL\_WRITE\_LOCK, WAL\_CKPT\_LOCK, WAL\_RECOVER\_LOCK, and WAL\_READ\_LOCK(1\) through WAL\_READ\_LOCK(4\). In other words, all locks associated with the
WAL\-index except for WAL\_READ\_LOCK(0\) are held exclusively. This prevents
any other thread from writing the database and from reading any transactions
that are held in the WAL, until the recovery is complete.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


