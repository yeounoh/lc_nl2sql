




SQLite Backup API




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog









# Using the SQLite Online Backup API



 Historically, backups (copies) of SQLite databases have been created
 using the following method:

1. Establish a shared lock on the database file using the SQLite API (i.e.
 the shell tool).
 - Copy the database file using an external tool (for example the unix 'cp'
 utility or the DOS 'copy' command).
 - Relinquish the shared lock on the database file obtained in step 1\.



 This procedure works well in many scenarios and is usually very
 fast. However, this technique has the following shortcomings:

* Any database clients wishing to write to the database file while a
 backup is being created must wait until the shared lock is
 relinquished.

 * It cannot be used to copy data to or from in\-memory databases.

 * If a power failure or operating system failure occurs while copying
 the database file the backup database may be corrupted following
 system recovery.



 The [Online Backup API](c3ref/backup_finish.html#sqlite3backupinit) was created to 
 address these concerns. The online backup API allows the contents of
 one database to be copied into another database file, replacing any 
 original contents of the target database. The copy operation may be 
 done incrementally, in which case the source database does not need
 to be locked for the duration of the copy, only for the brief periods
 of time when it is actually being read from. This allows other database
 users to continue without excessive delays while a backup of an online
 database is made.

 The effect of completing the backup call sequence is to make the
 destination a bit\-wise identical copy of the source database as it
 was when the copying commenced. (The destination becomes a "snapshot.")


 The online backup API is [documented here](c3ref/backup_finish.html#sqlite3backupinit).
 The remainder of this page contains two C language examples illustrating 
 common uses of the API and discussions thereof. Reading these examples
 is no substitute for reading the API documentation!


 Update: The [VACUUM INTO](lang_vacuum.html#vacuuminto) command introduced in 
 SQLite version 3\.27\.0 (2019\-02\-07\) can serve as an
 alternative to the backup API.

## Example 1: Loading and Saving In\-Memory Databases



```

/*
** This function is used to load the contents of a database file on disk 
** into the "main" database of open database connection pInMemory, or
** to save the current contents of the database opened by pInMemory into
** a database file on disk. pInMemory is probably an in-memory database, 
** but this function will also work fine if it is not.
**
** Parameter zFilename points to a nul-terminated string containing the
** name of the database file on disk to load from or save to. If parameter
** isSave is non-zero, then the contents of the file zFilename are 
** overwritten with the contents of the database opened by pInMemory. If
** parameter isSave is zero, then the contents of the database opened by
** pInMemory are replaced by data loaded from the file zFilename.
**
** If the operation is successful, SQLITE_OK is returned. Otherwise, if
** an error occurs, an SQLite error code is returned.
*/
int loadOrSaveDb([sqlite3](c3ref/sqlite3.html) *pInMemory, const char *zFilename, int isSave){
  int rc;                   /* Function return code */
  [sqlite3](c3ref/sqlite3.html) *pFile;           /* Database connection opened on zFilename */
  [sqlite3_backup](c3ref/backup.html) *pBackup;  /* Backup object used to copy data */
  [sqlite3](c3ref/sqlite3.html) *pTo;             /* Database to copy to (pFile or pInMemory) */
  [sqlite3](c3ref/sqlite3.html) *pFrom;           /* Database to copy from (pFile or pInMemory) */

  /* Open the database file identified by zFilename. Exit early if this fails
  ** for any reason. */
  rc = [sqlite3_open](c3ref/open.html)(zFilename, &pFile);
  if( rc==SQLITE_OK ){

    /* If this is a 'load' operation (isSave==0), then data is copied
    ** from the database file just opened to database pInMemory. 
    ** Otherwise, if this is a 'save' operation (isSave==1), then data
    ** is copied from pInMemory to pFile.  Set the variables pFrom and
    ** pTo accordingly. */
    pFrom = (isSave ? pInMemory : pFile);
    pTo   = (isSave ? pFile     : pInMemory);

    /* Set up the backup procedure to copy from the "main" database of 
    ** connection pFile to the main database of connection pInMemory.
    ** If something goes wrong, pBackup will be set to NULL and an error
    ** code and message left in connection pTo.
    **
    ** If the backup object is successfully created, call backup_step()
    ** to copy data from pFile to pInMemory. Then call backup_finish()
    ** to release resources associated with the pBackup object.  If an
    ** error occurred, then an error code and message will be left in
    ** connection pTo. If no error occurred, then the error code belonging
    ** to pTo is set to SQLITE_OK.
    */
    pBackup = [sqlite3_backup_init](c3ref/backup_finish.html#sqlite3backupinit)(pTo, "main", pFrom, "main");
    if( pBackup ){
      (void)[sqlite3_backup_step](c3ref/backup_finish.html#sqlite3backupstep)(pBackup, -1);
      (void)[sqlite3_backup_finish](c3ref/backup_finish.html#sqlite3backupfinish)(pBackup);
    }
    rc = [sqlite3_errcode](c3ref/errcode.html)(pTo);
  }

  /* Close the database connection opened on database file zFilename
  ** and return the result of this function. */
  (void)[sqlite3_close](c3ref/close.html)(pFile);
  return rc;
}

```


 The C function to the right demonstrates one of the simplest,
 and most common, uses of the backup API: loading and saving the contents
 of an in\-memory database to a file on disk. The backup API is used as
 follows in this example:

 1. Function [sqlite3\_backup\_init()](c3ref/backup_finish.html#sqlite3backupinit) is called to create an [sqlite3\_backup](c3ref/backup.html)
 object to copy data between the two databases (either from a file and
 into the in\-memory database, or vice\-versa).
 - Function [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep) is called with a parameter of 
 \-1 to copy the entire source database to the destination.
 - Function [sqlite3\_backup\_finish()](c3ref/backup_finish.html#sqlite3backupfinish) is called to clean up resources
 allocated by [sqlite3\_backup\_init()](c3ref/backup_finish.html#sqlite3backupinit).


**Error handling**

 If an error occurs in any of the three main backup API routines
 then the [error code](rescode.html) and [message](c3ref/errcode.html) are attached to
 the destination [database connection](c3ref/sqlite3.html).
 Additionally, if
 [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep) encounters an error, then the [error code](rescode.html) is returned
 by both the [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep) call itself, and by the subsequent call
 to [sqlite3\_backup\_finish()](c3ref/backup_finish.html#sqlite3backupfinish). So a call to [sqlite3\_backup\_finish()](c3ref/backup_finish.html#sqlite3backupfinish)
 does not overwrite an [error code](rescode.html) stored in the destination
 [database connection](c3ref/sqlite3.html) by [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep). This feature
 is used in the example code to reduce amount of error handling required.
 The return values of the [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep) and [sqlite3\_backup\_finish()](c3ref/backup_finish.html#sqlite3backupfinish)
 calls are ignored and the error code indicating the success or failure of
 the copy operation collected from the destination [database connection](c3ref/sqlite3.html)
 afterward.

**Possible Enhancements**

 The implementation of this function could be enhanced in at least two ways:

 1. Failing to obtain the lock on database file zFilename (an [SQLITE\_BUSY](rescode.html#busy)
 error) could be handled, and
 - Cases where the page\-sizes of database pInMemory and zFilename are
 different could be handled better.



 Since database zFilename is a file on disk, then it may be accessed 
 externally by another process. This means that when the call to
 sqlite3\_backup\_step() attempts to read from or write data to it, it may
 fail to obtain the required file lock. If this happens, this implementation
 will fail, returning SQLITE\_BUSY immediately. The solution would be to
 register a busy\-handler callback or 
 timeout with [database connection](c3ref/sqlite3.html) pFile 
 using [sqlite3\_busy\_handler()](c3ref/busy_handler.html) or [sqlite3\_busy\_timeout()](c3ref/busy_timeout.html)
 as soon as it is opened. If it fails to obtain a required lock immediately,
 [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep) uses any registered busy\-handler callback or timeout
 in the same way as [sqlite3\_step()](c3ref/step.html) or [sqlite3\_exec()](c3ref/exec.html) does.


 Usually, it does not matter if the page\-sizes of the source database and the
 destination database are different before the contents of the destination
 are overwritten. The page\-size of the destination database is simply changed
 as part of the backup operation. The exception is if the destination database
 happens to be an in\-memory database. In this case, if the page sizes
 are not the same at the start of the backup operation, then the operation
 fails with an SQLITE\_READONLY error. Unfortunately, this could occur when
 loading a database image from a file into an in\-memory database using
 function loadOrSaveDb().


 However, if in\-memory database pInMemory has just been opened (and is 
 therefore completely empty) before being passed to function loadOrSaveDb(), 
 then it is still possible to change its page size using an SQLite "PRAGMA
 page\_size" command. Function loadOrSaveDb() could detect this case, and
 attempt to set the page\-size of the in\-memory database to the page\-size
 of database zFilename before invoking the online backup API functions.
 
## Example 2: Online Backup of a Running Database



```

/*
** Perform an online backup of database pDb to the database file named
** by zFilename. This function copies 5 database pages from pDb to
** zFilename, then unlocks pDb and sleeps for 250 ms, then repeats the
** process until the entire database is backed up.
** 
** The third argument passed to this function must be a pointer to a progress
** function. After each set of 5 pages is backed up, the progress function
** is invoked with two integer parameters: the number of pages left to
** copy, and the total number of pages in the source file. This information
** may be used, for example, to update a GUI progress bar.
**
** While this function is running, another thread may use the database pDb, or
** another process may access the underlying database file via a separate 
** connection.
**
** If the backup process is successfully completed, SQLITE_OK is returned.
** Otherwise, if an error occurs, an SQLite error code is returned.
*/
int backupDb(
  [sqlite3](c3ref/sqlite3.html) *pDb,               /* Database to back up */
  const char *zFilename,      /* Name of file to back up to */
  void(*xProgress)(int, int)  /* Progress function to invoke */     
){
  int rc;                     /* Function return code */
  [sqlite3](c3ref/sqlite3.html) *pFile;             /* Database connection opened on zFilename */
  [sqlite3_backup](c3ref/backup.html) *pBackup;    /* Backup handle used to copy data */

  /* Open the database file identified by zFilename. */
  rc = [sqlite3_open](c3ref/open.html)(zFilename, &pFile);
  if( rc==SQLITE_OK ){

    /* Open the [sqlite3_backup](c3ref/backup.html) object used to accomplish the transfer */
    pBackup = [sqlite3_backup_init](c3ref/backup_finish.html#sqlite3backupinit)(pFile, "main", pDb, "main");
    if( pBackup ){

      /* Each iteration of this loop copies 5 database pages from database
      ** pDb to the backup database. If the return value of backup_step()
      ** indicates that there are still further pages to copy, sleep for
      ** 250 ms before repeating. */
      do {
        rc = [sqlite3_backup_step](c3ref/backup_finish.html#sqlite3backupstep)(pBackup, 5);
        xProgress(
            [sqlite3_backup_remaining](c3ref/backup_finish.html#sqlite3backupremaining)(pBackup),
            [sqlite3_backup_pagecount](c3ref/backup_finish.html#sqlite3backuppagecount)(pBackup)
        );
        if( rc==SQLITE_OK || rc==SQLITE_BUSY || rc==SQLITE_LOCKED ){
          [sqlite3_sleep](c3ref/sleep.html)(250);
        }
      } while( rc==SQLITE_OK || rc==SQLITE_BUSY || rc==SQLITE_LOCKED );

      /* Release resources allocated by backup_init(). */
      (void)[sqlite3_backup_finish](c3ref/backup_finish.html#sqlite3backupfinish)(pBackup);
    }
    rc = [sqlite3_errcode](c3ref/errcode.html)(pFile);
  }
  
  /* Close the database connection opened on database file zFilename
  ** and return the result of this function. */
  (void)[sqlite3_close](c3ref/close.html)(pFile);
  return rc;
}

```


 The function presented in the previous example copies the entire source
 database in one call to [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep). This requires holding a 
 read\-lock on the source database file for the duration of the operation,
 preventing any other database user from writing to the database. It also
 holds the mutex associated with database pInMemory throughout the copy,
 preventing any other thread from using it. The C function in this section,
 designed to be called by a background thread or process for creating a 
 backup of an online database, avoids these problems using the following 
 approach:

 1. Function [sqlite3\_backup\_init()](c3ref/backup_finish.html#sqlite3backupinit) is called to create an [sqlite3\_backup](c3ref/backup.html)
 object to copy data from database pDb to the backup database file 
 identified by zFilename.
 - Function [sqlite3\_backup\_step()](c3ref/backup_finish.html#sqlite3backupstep) is called with a parameter of 5 to
 copy 5 pages of database pDb to the backup database (file zFilename).
 - If there are still more pages to copy from database pDb, then the
 function sleeps for 250 milliseconds (using the [sqlite3\_sleep()](c3ref/sleep.html)
 utility) and then returns to step 2\.
 - Function [sqlite3\_backup\_finish()](c3ref/backup_finish.html#sqlite3backupfinish) is called to clean up resources
 allocated by [sqlite3\_backup\_init()](c3ref/backup_finish.html#sqlite3backupinit).


**File and Database Connection Locking**

 During the 250 ms sleep in step 3 above, no read\-lock is held on the database
 file and the mutex associated with pDb is not held. This allows other threads
 to use [database connection](c3ref/sqlite3.html) pDb and other connections to write to the
 underlying database file. 


 If another thread or process writes to the source database while this 
 function is sleeping, then SQLite detects this and usually restarts the 
 backup process when sqlite3\_backup\_step() is next called. There is one 
 exception to this rule: If the source database is not an in\-memory database,
 and the write is performed from within the same process as the backup
 operation and uses the same database handle (pDb), then the destination
 database (the one opened using connection pFile) is automatically updated
 along with the source. The backup process may then be continued after the 
 sqlite3\_sleep() call returns as if nothing had happened. 


 Whether or not the backup process is restarted as a result of writes to
 the source database mid\-backup, the user can be sure that when the backup
 operation is completed the backup database contains a consistent and 
 up\-to\-date snapshot of the original. However:

 * Writes to an in\-memory source database, or writes to a file\-based 
 source database by an external process or thread using a 
 database connection other than pDb are significantly more expensive 
 than writes made to a file\-based source database using pDb (as the
 entire backup operation must be restarted in the former two cases).

 * If the backup process is restarted frequently enough it may never
 run to completion and the backupDb() function may never return.


**backup\_remaining() and backup\_pagecount()**

 The backupDb() function uses the sqlite3\_backup\_remaining() and
 sqlite3\_backup\_pagecount() functions to report its progress via the
 user\-supplied xProgress() callback. Function sqlite3\_backup\_remaining()
 returns the number of pages left to copy and sqlite3\_backup\_pagecount()
 returns the total number of pages in the source database (in this case 
 the database opened by pDb). So the percentage completion of the process
 may be calculated as:


 Completion \= 100% \* (pagecount() \- remaining()) / pagecount()


 The sqlite3\_backup\_remaining() and sqlite3\_backup\_pagecount() APIs report
 values stored by the previous call to sqlite3\_backup\_step(), they do not
 actually inspect the source database file. This means that if the source
 database is written to by another thread or process after the call to
 sqlite3\_backup\_step() returns but before the values returned by
 sqlite3\_backup\_remaining() and sqlite3\_backup\_pagecount() are used, the 
 values may be technically incorrect. This is not usually a problem.



*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 
















































