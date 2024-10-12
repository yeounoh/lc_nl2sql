




Extended Result Codes




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Extended Result Codes




> ```
> 
> #define SQLITE_ERROR_MISSING_COLLSEQ   (SQLITE_ERROR | (1<<8))
> #define SQLITE_ERROR_RETRY             (SQLITE_ERROR | (2<<8))
> #define SQLITE_ERROR_SNAPSHOT          (SQLITE_ERROR | (3<<8))
> #define SQLITE_IOERR_READ              (SQLITE_IOERR | (1<<8))
> #define SQLITE_IOERR_SHORT_READ        (SQLITE_IOERR | (2<<8))
> #define SQLITE_IOERR_WRITE             (SQLITE_IOERR | (3<<8))
> #define SQLITE_IOERR_FSYNC             (SQLITE_IOERR | (4<<8))
> #define SQLITE_IOERR_DIR_FSYNC         (SQLITE_IOERR | (5<<8))
> #define SQLITE_IOERR_TRUNCATE          (SQLITE_IOERR | (6<<8))
> #define SQLITE_IOERR_FSTAT             (SQLITE_IOERR | (7<<8))
> #define SQLITE_IOERR_UNLOCK            (SQLITE_IOERR | (8<<8))
> #define SQLITE_IOERR_RDLOCK            (SQLITE_IOERR | (9<<8))
> #define SQLITE_IOERR_DELETE            (SQLITE_IOERR | (10<<8))
> #define SQLITE_IOERR_BLOCKED           (SQLITE_IOERR | (11<<8))
> #define SQLITE_IOERR_NOMEM             (SQLITE_IOERR | (12<<8))
> #define SQLITE_IOERR_ACCESS            (SQLITE_IOERR | (13<<8))
> #define SQLITE_IOERR_CHECKRESERVEDLOCK (SQLITE_IOERR | (14<<8))
> #define SQLITE_IOERR_LOCK              (SQLITE_IOERR | (15<<8))
> #define SQLITE_IOERR_CLOSE             (SQLITE_IOERR | (16<<8))
> #define SQLITE_IOERR_DIR_CLOSE         (SQLITE_IOERR | (17<<8))
> #define SQLITE_IOERR_SHMOPEN           (SQLITE_IOERR | (18<<8))
> #define SQLITE_IOERR_SHMSIZE           (SQLITE_IOERR | (19<<8))
> #define SQLITE_IOERR_SHMLOCK           (SQLITE_IOERR | (20<<8))
> #define SQLITE_IOERR_SHMMAP            (SQLITE_IOERR | (21<<8))
> #define SQLITE_IOERR_SEEK              (SQLITE_IOERR | (22<<8))
> #define SQLITE_IOERR_DELETE_NOENT      (SQLITE_IOERR | (23<<8))
> #define SQLITE_IOERR_MMAP              (SQLITE_IOERR | (24<<8))
> #define SQLITE_IOERR_GETTEMPPATH       (SQLITE_IOERR | (25<<8))
> #define SQLITE_IOERR_CONVPATH          (SQLITE_IOERR | (26<<8))
> #define SQLITE_IOERR_VNODE             (SQLITE_IOERR | (27<<8))
> #define SQLITE_IOERR_AUTH              (SQLITE_IOERR | (28<<8))
> #define SQLITE_IOERR_BEGIN_ATOMIC      (SQLITE_IOERR | (29<<8))
> #define SQLITE_IOERR_COMMIT_ATOMIC     (SQLITE_IOERR | (30<<8))
> #define SQLITE_IOERR_ROLLBACK_ATOMIC   (SQLITE_IOERR | (31<<8))
> #define SQLITE_IOERR_DATA              (SQLITE_IOERR | (32<<8))
> #define SQLITE_IOERR_CORRUPTFS         (SQLITE_IOERR | (33<<8))
> #define SQLITE_IOERR_IN_PAGE           (SQLITE_IOERR | (34<<8))
> #define SQLITE_LOCKED_SHAREDCACHE      (SQLITE_LOCKED |  (1<<8))
> #define SQLITE_LOCKED_VTAB             (SQLITE_LOCKED |  (2<<8))
> #define SQLITE_BUSY_RECOVERY           (SQLITE_BUSY   |  (1<<8))
> #define SQLITE_BUSY_SNAPSHOT           (SQLITE_BUSY   |  (2<<8))
> #define SQLITE_BUSY_TIMEOUT            (SQLITE_BUSY   |  (3<<8))
> #define SQLITE_CANTOPEN_NOTEMPDIR      (SQLITE_CANTOPEN | (1<<8))
> #define SQLITE_CANTOPEN_ISDIR          (SQLITE_CANTOPEN | (2<<8))
> #define SQLITE_CANTOPEN_FULLPATH       (SQLITE_CANTOPEN | (3<<8))
> #define SQLITE_CANTOPEN_CONVPATH       (SQLITE_CANTOPEN | (4<<8))
> #define SQLITE_CANTOPEN_DIRTYWAL       (SQLITE_CANTOPEN | (5<<8)) /* Not Used */
> #define SQLITE_CANTOPEN_SYMLINK        (SQLITE_CANTOPEN | (6<<8))
> #define SQLITE_CORRUPT_VTAB            (SQLITE_CORRUPT | (1<<8))
> #define SQLITE_CORRUPT_SEQUENCE        (SQLITE_CORRUPT | (2<<8))
> #define SQLITE_CORRUPT_INDEX           (SQLITE_CORRUPT | (3<<8))
> #define SQLITE_READONLY_RECOVERY       (SQLITE_READONLY | (1<<8))
> #define SQLITE_READONLY_CANTLOCK       (SQLITE_READONLY | (2<<8))
> #define SQLITE_READONLY_ROLLBACK       (SQLITE_READONLY | (3<<8))
> #define SQLITE_READONLY_DBMOVED        (SQLITE_READONLY | (4<<8))
> #define SQLITE_READONLY_CANTINIT       (SQLITE_READONLY | (5<<8))
> #define SQLITE_READONLY_DIRECTORY      (SQLITE_READONLY | (6<<8))
> #define SQLITE_ABORT_ROLLBACK          (SQLITE_ABORT | (2<<8))
> #define SQLITE_CONSTRAINT_CHECK        (SQLITE_CONSTRAINT | (1<<8))
> #define SQLITE_CONSTRAINT_COMMITHOOK   (SQLITE_CONSTRAINT | (2<<8))
> #define SQLITE_CONSTRAINT_FOREIGNKEY   (SQLITE_CONSTRAINT | (3<<8))
> #define SQLITE_CONSTRAINT_FUNCTION     (SQLITE_CONSTRAINT | (4<<8))
> #define SQLITE_CONSTRAINT_NOTNULL      (SQLITE_CONSTRAINT | (5<<8))
> #define SQLITE_CONSTRAINT_PRIMARYKEY   (SQLITE_CONSTRAINT | (6<<8))
> #define SQLITE_CONSTRAINT_TRIGGER      (SQLITE_CONSTRAINT | (7<<8))
> #define SQLITE_CONSTRAINT_UNIQUE       (SQLITE_CONSTRAINT | (8<<8))
> #define SQLITE_CONSTRAINT_VTAB         (SQLITE_CONSTRAINT | (9<<8))
> #define SQLITE_CONSTRAINT_ROWID        (SQLITE_CONSTRAINT |(10<<8))
> #define SQLITE_CONSTRAINT_PINNED       (SQLITE_CONSTRAINT |(11<<8))
> #define SQLITE_CONSTRAINT_DATATYPE     (SQLITE_CONSTRAINT |(12<<8))
> #define SQLITE_NOTICE_RECOVER_WAL      (SQLITE_NOTICE | (1<<8))
> #define SQLITE_NOTICE_RECOVER_ROLLBACK (SQLITE_NOTICE | (2<<8))
> #define SQLITE_NOTICE_RBU              (SQLITE_NOTICE | (3<<8))
> #define SQLITE_WARNING_AUTOINDEX       (SQLITE_WARNING | (1<<8))
> #define SQLITE_AUTH_USER               (SQLITE_AUTH | (1<<8))
> #define SQLITE_OK_LOAD_PERMANENTLY     (SQLITE_OK | (1<<8))
> #define SQLITE_OK_SYMLINK              (SQLITE_OK | (2<<8)) /* internal use only */
> 
> ```



In its default configuration, SQLite API routines return one of 30 integer
[result codes](../rescode.html). However, experience has shown that many of
these result codes are too coarse\-grained. They do not provide as
much information about problems as programmers might like. In an effort to
address this, newer versions of SQLite (version 3\.3\.8 2006\-10\-09
and later) include
support for additional result codes that provide more detailed information
about errors. These [extended result codes](../rescode.html#extrc) are enabled or disabled
on a per database connection basis using the
[sqlite3\_extended\_result\_codes()](../c3ref/extended_result_codes.html) API. Or, the extended code for
the most recent error can be obtained using
[sqlite3\_extended\_errcode()](../c3ref/errcode.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


