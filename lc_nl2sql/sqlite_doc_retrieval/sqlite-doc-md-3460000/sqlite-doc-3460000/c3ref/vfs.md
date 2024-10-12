




OS Interface Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## OS Interface Object




> ```
> 
> typedef struct sqlite3_vfs sqlite3_vfs;
> typedef void (*sqlite3_syscall_ptr)(void);
> struct sqlite3_vfs {
>   int iVersion;            /* Structure version number (currently 3) */
>   int szOsFile;            /* Size of subclassed sqlite3_file */
>   int mxPathname;          /* Maximum file pathname length */
>   sqlite3_vfs *pNext;      /* Next registered VFS */
>   const char *zName;       /* Name of this virtual file system */
>   void *pAppData;          /* Pointer to application-specific data */
>   int (*xOpen)(sqlite3_vfs*, sqlite3_filename zName, sqlite3_file*,
>                int flags, int *pOutFlags);
>   int (*xDelete)(sqlite3_vfs*, const char *zName, int syncDir);
>   int (*xAccess)(sqlite3_vfs*, const char *zName, int flags, int *pResOut);
>   int (*xFullPathname)(sqlite3_vfs*, const char *zName, int nOut, char *zOut);
>   void *(*xDlOpen)(sqlite3_vfs*, const char *zFilename);
>   void (*xDlError)(sqlite3_vfs*, int nByte, char *zErrMsg);
>   void (*(*xDlSym)(sqlite3_vfs*,void*, const char *zSymbol))(void);
>   void (*xDlClose)(sqlite3_vfs*, void*);
>   int (*xRandomness)(sqlite3_vfs*, int nByte, char *zOut);
>   int (*xSleep)(sqlite3_vfs*, int microseconds);
>   int (*xCurrentTime)(sqlite3_vfs*, double*);
>   int (*xGetLastError)(sqlite3_vfs*, int, char *);
>   /*
>   ** The methods above are in version 1 of the sqlite_vfs object
>   ** definition.  Those that follow are added in version 2 or later
>   */
>   int (*xCurrentTimeInt64)(sqlite3_vfs*, sqlite3_int64*);
>   /*
>   ** The methods above are in versions 1 and 2 of the sqlite_vfs object.
>   ** Those below are for version 3 and greater.
>   */
>   int (*xSetSystemCall)(sqlite3_vfs*, const char *zName, sqlite3_syscall_ptr);
>   sqlite3_syscall_ptr (*xGetSystemCall)(sqlite3_vfs*, const char *zName);
>   const char *(*xNextSystemCall)(sqlite3_vfs*, const char *zName);
>   /*
>   ** The methods above are in versions 1 through 3 of the sqlite_vfs object.
>   ** New fields may be appended in future versions.  The iVersion
>   ** value will increment whenever this happens.
>   */
> };
> 
> ```



An instance of the sqlite3\_vfs object defines the interface between
the SQLite core and the underlying operating system. The "vfs"
in the name of the object stands for "virtual file system". See
the [VFS documentation](../vfs.html) for further information.


The VFS interface is sometimes extended by adding new methods onto
the end. Each time such an extension occurs, the iVersion field
is incremented. The iVersion value started out as 1 in
SQLite [version 3\.5\.0](../releaselog/3_5_0.html) on 2007\-09\-04, then increased to 2
with SQLite [version 3\.7\.0](../releaselog/3_7_0.html) on 2010\-07\-21, and then increased
to 3 with SQLite [version 3\.7\.6](../releaselog/3_7_6.html) on 2011\-04\-12\. Additional fields
may be appended to the sqlite3\_vfs object and the iVersion value
may increase again in future versions of SQLite.
Note that due to an oversight, the structure
of the sqlite3\_vfs object changed in the transition from
SQLite [version 3\.5\.9](../releaselog/3_5_9.html) to [version 3\.6\.0](../releaselog/3_6_0.html) on 2008\-07\-16
and yet the iVersion field was not increased.


The szOsFile field is the size of the subclassed [sqlite3\_file](../c3ref/file.html)
structure used by this VFS. mxPathname is the maximum length of
a pathname in this VFS.


Registered sqlite3\_vfs objects are kept on a linked list formed by
the pNext pointer. The [sqlite3\_vfs\_register()](../c3ref/vfs_find.html)
and [sqlite3\_vfs\_unregister()](../c3ref/vfs_find.html) interfaces manage this list
in a thread\-safe way. The [sqlite3\_vfs\_find()](../c3ref/vfs_find.html) interface
searches the list. Neither the application code nor the VFS
implementation should use the pNext pointer.


The pNext field is the only field in the sqlite3\_vfs
structure that SQLite will ever modify. SQLite will only access
or modify this field while holding a particular static mutex.
The application should never modify anything within the sqlite3\_vfs
object once the object has been registered.


The zName field holds the name of the VFS module. The name must
be unique across all VFS modules.




SQLite guarantees that the zFilename parameter to xOpen
is either a NULL pointer or string obtained
from xFullPathname() with an optional suffix added.
If a suffix is added to the zFilename parameter, it will
consist of a single "\-" character followed by no more than
11 alphanumeric and/or "\-" characters.
SQLite further guarantees that
the string will be valid and unchanged until xClose() is
called. Because of the previous sentence,
the [sqlite3\_file](../c3ref/file.html) can safely store a pointer to the
filename if it needs to remember the filename for some reason.
If the zFilename parameter to xOpen is a NULL pointer then xOpen
must invent its own temporary name for the file. Whenever the
xFilename parameter is NULL it will also be the case that the
flags parameter will include [SQLITE\_OPEN\_DELETEONCLOSE](../c3ref/c_open_autoproxy.html).


The flags argument to xOpen() includes all bits set in
the flags argument to [sqlite3\_open\_v2()](../c3ref/open.html). Or if [sqlite3\_open()](../c3ref/open.html)
or [sqlite3\_open16()](../c3ref/open.html) is used, then flags includes at least
[SQLITE\_OPEN\_READWRITE](../c3ref/c_open_autoproxy.html) \| [SQLITE\_OPEN\_CREATE](../c3ref/c_open_autoproxy.html).
If xOpen() opens a file read\-only then it sets \*pOutFlags to
include [SQLITE\_OPEN\_READONLY](../c3ref/c_open_autoproxy.html). Other bits in \*pOutFlags may be set.


SQLite will also add one of the following flags to the xOpen()
call, depending on the object being opened:


* [SQLITE\_OPEN\_MAIN\_DB](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_MAIN\_JOURNAL](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_TEMP\_DB](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_TEMP\_JOURNAL](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_TRANSIENT\_DB](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_SUBJOURNAL](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_SUPER\_JOURNAL](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_WAL](../c3ref/c_open_autoproxy.html)



The file I/O implementation can use the object type flags to
change the way it deals with files. For example, an application
that does not care about crash recovery or rollback might make
the open of a journal file a no\-op. Writes to this journal would
also be no\-ops, and any attempt to read the journal would return
SQLITE\_IOERR. Or the implementation might recognize that a database
file will be doing page\-aligned sector reads and writes in a random
order and set up its I/O subsystem accordingly.


SQLite might also add one of the following flags to the xOpen method:


* [SQLITE\_OPEN\_DELETEONCLOSE](../c3ref/c_open_autoproxy.html)* [SQLITE\_OPEN\_EXCLUSIVE](../c3ref/c_open_autoproxy.html)



The [SQLITE\_OPEN\_DELETEONCLOSE](../c3ref/c_open_autoproxy.html) flag means the file should be
deleted when it is closed. The [SQLITE\_OPEN\_DELETEONCLOSE](../c3ref/c_open_autoproxy.html)
will be set for TEMP databases and their journals, transient
databases, and subjournals.


The [SQLITE\_OPEN\_EXCLUSIVE](../c3ref/c_open_autoproxy.html) flag is always used in conjunction
with the [SQLITE\_OPEN\_CREATE](../c3ref/c_open_autoproxy.html) flag, which are both directly
analogous to the O\_EXCL and O\_CREAT flags of the POSIX open()
API. The SQLITE\_OPEN\_EXCLUSIVE flag, when paired with the
SQLITE\_OPEN\_CREATE, is used to indicate that file should always
be created, and that it is an error if it already exists.
It is *not* used to indicate the file should be opened
for exclusive access.


At least szOsFile bytes of memory are allocated by SQLite
to hold the [sqlite3\_file](../c3ref/file.html) structure passed as the third
argument to xOpen. The xOpen method does not have to
allocate the structure; it should just fill it in. Note that
the xOpen method must set the sqlite3\_file.pMethods to either
a valid [sqlite3\_io\_methods](../c3ref/io_methods.html) object or to NULL. xOpen must do
this even if the open fails. SQLite expects that the sqlite3\_file.pMethods
element will be valid after xOpen returns regardless of the success
or failure of the xOpen call.




The flags argument to xAccess() may be [SQLITE\_ACCESS\_EXISTS](../c3ref/c_access_exists.html)
to test for the existence of a file, or [SQLITE\_ACCESS\_READWRITE](../c3ref/c_access_exists.html) to
test whether a file is readable and writable, or [SQLITE\_ACCESS\_READ](../c3ref/c_access_exists.html)
to test whether a file is at least readable. The SQLITE\_ACCESS\_READ
flag is never actually used and is not implemented in the built\-in
VFSes of SQLite. The file is named by the second argument and can be a
directory. The xAccess method returns [SQLITE\_OK](../rescode.html#ok) on success or some
non\-zero error code if there is an I/O error or if the name of
the file given in the second argument is illegal. If SQLITE\_OK
is returned, then non\-zero or zero is written into \*pResOut to indicate
whether or not the file is accessible.


SQLite will always allocate at least mxPathname\+1 bytes for the
output buffer xFullPathname. The exact size of the output buffer
is also passed as a parameter to both methods. If the output buffer
is not large enough, [SQLITE\_CANTOPEN](../rescode.html#cantopen) should be returned. Since this is
handled as a fatal error by SQLite, vfs implementations should endeavor
to prevent this by setting mxPathname to a sufficiently large value.


The xRandomness(), xSleep(), xCurrentTime(), and xCurrentTimeInt64()
interfaces are not strictly a part of the filesystem, but they are
included in the VFS structure for completeness.
The xRandomness() function attempts to return nBytes bytes
of good\-quality randomness into zOut. The return value is
the actual number of bytes of randomness obtained.
The xSleep() method causes the calling thread to sleep for at
least the number of microseconds given. The xCurrentTime()
method returns a Julian Day Number for the current date and time as
a floating point value.
The xCurrentTimeInt64() method returns, as an integer, the Julian
Day Number multiplied by 86400000 (the number of milliseconds in
a 24\-hour day).
SQLite will use the xCurrentTimeInt64() method to get the current
date and time if that method is available (if iVersion is 2 or
greater and the function pointer is not NULL) and will fall back
to xCurrentTime() if xCurrentTimeInt64() is unavailable.


The xSetSystemCall(), xGetSystemCall(), and xNestSystemCall() interfaces
are not used by the SQLite core. These optional interfaces are provided
by some VFSes to facilitate testing of the VFS code. By overriding
system calls with functions under its control, a test program can
simulate faults and error conditions that would otherwise be difficult
or impossible to induce. The set of system calls that can be overridden
varies from one VFS to another, and from one version of the same VFS to the
next. Applications that use these interfaces must be prepared for any
or all of these interfaces to be NULL or for their behavior to change
from one release to the next. Applications must not attempt to access
any of these methods if the iVersion of the VFS is less than 3\.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


