




The C language interface to SQLite Version 2




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










| **Editorial Note:** This document describes SQLite version 2, which was deprecated and replaced by SQLite3 in 2004\. This document is retained as part of the historical record of SQLite. Modern programmers should refer to more up\-to\-date documentation on SQLite is available elsewhere on this website. |
| --- |


## The C language interface to SQLite Version 2


The SQLite library is designed to be very easy to use from
a C or C\+\+ program. This document gives an overview of the C/C\+\+
programming interface.


### 1\.0 The Core API


The interface to the SQLite library consists of three core functions,
one opaque data structure, and some constants used as return values.
The core interface is as follows:



> ```
> 
> typedef struct sqlite sqlite;
> #define SQLITE_OK           0   /* Successful result */
> 
> sqlite *sqlite_open(const char *dbname, int mode, char **errmsg);
> 
> void sqlite_close(sqlite *db);
> 
> int sqlite_exec(
>   sqlite *db,
>   char *sql,
>   int (*xCallback)(void*,int,char**,char**),
>   void *pArg,
>   char **errmsg
> );
> 
> ```



The above is all you really need to know in order to use SQLite
in your C or C\+\+ programs. There are other interface functions
available (and described below) but we will begin by describing
the core functions shown above.




#### 1\.1 Opening a database


Use the **sqlite\_open** function to open an existing SQLite
database or to create a new SQLite database. The first argument
is the database name. The second argument is intended to signal
whether the database is going to be used for reading and writing
or just for reading. But in the current implementation, the
second argument to **sqlite\_open** is ignored.
The third argument is a pointer to a string pointer.
If the third argument is not NULL and an error occurs
while trying to open the database, then an error message will be
written to memory obtained from malloc() and \*errmsg will be made
to point to this error message. The calling function is responsible
for freeing the memory when it has finished with it.


The name of an SQLite database is the name of a file that will
contain the database. If the file does not exist, SQLite attempts
to create and initialize it. If the file is read\-only (due to
permission bits or because it is located on read\-only media like
a CD\-ROM) then SQLite opens the database for reading only. The
entire SQL database is stored in a single file on the disk. But
additional temporary files may be created during the execution of
an SQL command in order to store the database rollback journal or
temporary and intermediate results of a query.


The return value of the **sqlite\_open** function is a
pointer to an opaque **sqlite** structure. This pointer will
be the first argument to all subsequent SQLite function calls that
deal with the same database. NULL is returned if the open fails
for any reason.



#### 1\.2 Closing the database


To close an SQLite database, call the **sqlite\_close**
function passing it the sqlite structure pointer that was obtained
from a prior call to **sqlite\_open**.
If a transaction is active when the database is closed, the transaction
is rolled back.



#### 1\.3 Executing SQL statements


The **sqlite\_exec** function is used to process SQL statements
and queries. This function requires 5 parameters as follows:


1. A pointer to the sqlite structure obtained from a prior call
 to **sqlite\_open**.
2. A zero\-terminated string containing the text of one or more
 SQL statements and/or queries to be processed.
3. A pointer to a callback function which is invoked once for each
 row in the result of a query. This argument may be NULL, in which
 case no callbacks will ever be invoked.
4. A pointer that is forwarded to become the first argument
 to the callback function.
5. A pointer to an error string. Error messages are written to space
 obtained from malloc() and the error string is made to point to
 the malloced space. The calling function is responsible for freeing
 this space when it has finished with it.
 This argument may be NULL, in which case error messages are not
 reported back to the calling function.



The callback function is used to receive the results of a query. A
prototype for the callback function is as follows:



> ```
> 
> int Callback(void *pArg, int argc, char **argv, char **columnNames){
>   return 0;
> }
> 
> ```



The first argument to the callback is just a copy of the fourth argument
to **sqlite\_exec** This parameter can be used to pass arbitrary
information through to the callback function from client code.
The second argument is the number of columns in the query result.
The third argument is an array of pointers to strings where each string
is a single column of the result for that record. Note that the
callback function reports a NULL value in the database as a NULL pointer,
which is very different from an empty string. If the i\-th parameter
is an empty string, we will get:



> ```
> 
> argv[i][0] == 0
> 
> ```


But if the i\-th parameter is NULL we will get:



> ```
> 
> argv[i] == 0
> 
> ```


The names of the columns are contained in first *argc*
entries of the fourth argument.
If the [SHOW\_DATATYPES](pragma.html) pragma
is on (it is off by default) then
the second *argc* entries in the 4th argument are the datatypes
for the corresponding columns.



If the [EMPTY\_RESULT\_CALLBACKS](pragma.html#pragma_empty_result_callbacks) pragma is set to ON and the result of
a query is an empty set, then the callback is invoked once with the
third parameter (argv) set to 0\. In other words

> ```
> 
> argv == 0
> 
> ```


The second parameter (argc)
and the fourth parameter (columnNames) are still valid
and can be used to determine the number and names of the result
columns if there had been a result.
The default behavior is not to invoke the callback at all if the
result set is empty.



The callback function should normally return 0\. If the callback
function returns non\-zero, the query is immediately aborted and 
**sqlite\_exec** will return SQLITE\_ABORT.


#### 1\.4 Error Codes



The **sqlite\_exec** function normally returns SQLITE\_OK. But
if something goes wrong it can return a different value to indicate
the type of error. Here is a complete list of the return codes:




> ```
> 
> #define SQLITE_OK           0   /* Successful result */
> #define SQLITE_ERROR        1   /* SQL error or missing database */
> #define SQLITE_INTERNAL     2   /* An internal logic error in SQLite */
> #define SQLITE_PERM         3   /* Access permission denied */
> #define SQLITE_ABORT        4   /* Callback routine requested an abort */
> #define SQLITE_BUSY         5   /* The database file is locked */
> #define SQLITE_LOCKED       6   /* A table in the database is locked */
> #define SQLITE_NOMEM        7   /* A malloc() failed */
> #define SQLITE_READONLY     8   /* Attempt to write a readonly database */
> #define SQLITE_INTERRUPT    9   /* Operation terminated by sqlite_interrupt() */
> #define SQLITE_IOERR       10   /* Some kind of disk I/O error occurred */
> #define SQLITE_CORRUPT     11   /* The database disk image is malformed */
> #define SQLITE_NOTFOUND    12   /* (Internal Only) Table or record not found */
> #define SQLITE_FULL        13   /* Insertion failed because database is full */
> #define SQLITE_CANTOPEN    14   /* Unable to open the database file */
> #define SQLITE_PROTOCOL    15   /* Database lock protocol error */
> #define SQLITE_EMPTY       16   /* (Internal Only) Database table is empty */
> #define SQLITE_SCHEMA      17   /* The database schema changed */
> #define SQLITE_TOOBIG      18   /* Too much data for one row of a table */
> #define SQLITE_CONSTRAINT  19   /* Abort due to constraint violation */
> #define SQLITE_MISMATCH    20   /* Data type mismatch */
> #define SQLITE_MISUSE      21   /* Library used incorrectly */
> #define SQLITE_NOLFS       22   /* Uses OS features not supported on host */
> #define SQLITE_AUTH        23   /* Authorization denied */
> #define SQLITE_ROW         100  /* sqlite_step() has another row ready */
> #define SQLITE_DONE        101  /* sqlite_step() has finished executing */
> 
> ```



The meanings of these various return values are as follows:




> SQLITE\_OK
> This value is returned if everything worked and there were no errors.
> 
> 
> 
> SQLITE\_INTERNAL
> This value indicates that an internal consistency check within
> the SQLite library failed. This can only happen if there is a bug in
> the SQLite library. If you ever get an SQLITE\_INTERNAL reply from
> an **sqlite\_exec** call, please report the problem on the SQLite
> mailing list.
> 
> 
> 
> SQLITE\_ERROR
> This return value indicates that there was an error in the SQL
> that was passed into the **sqlite\_exec**.
> 
> 
> 
> SQLITE\_PERM
> This return value says that the access permissions on the database
> file are such that the file cannot be opened.
> 
> 
> 
> SQLITE\_ABORT
> This value is returned if the callback function returns non\-zero.
> 
> 
> 
> SQLITE\_BUSY
> This return code indicates that another program or thread has
> the database locked. SQLite allows two or more threads to read the
> database at the same time, but only one thread can have the database
> open for writing at the same time. Locking in SQLite is on the
> entire database.




SQLITE\_LOCKED
This return code is similar to SQLITE\_BUSY in that it indicates
that the database is locked. But the source of the lock is a recursive
call to **sqlite\_exec**. This return can only occur if you attempt
to invoke sqlite\_exec from within a callback routine of a query
from a prior invocation of sqlite\_exec. Recursive calls to
sqlite\_exec are allowed as long as they do
not attempt to write the same table.



SQLITE\_NOMEM
This value is returned if a call to **malloc** fails.



SQLITE\_READONLY
This return code indicates that an attempt was made to write to
a database file that is opened for reading only.



SQLITE\_INTERRUPT
This value is returned if a call to **sqlite\_interrupt**
interrupts a database operation in progress.



SQLITE\_IOERR
This value is returned if the operating system informs SQLite
that it is unable to perform some disk I/O operation. This could mean
that there is no more space left on the disk.



SQLITE\_CORRUPT
This value is returned if SQLite detects that the database it is
working on has become corrupted. Corruption might occur due to a rogue
process writing to the database file or it might happen due to a
previously undetected logic error in of SQLite. This value is also
returned if a disk I/O error occurs in such a way that SQLite is forced
to leave the database file in a corrupted state. The latter should only
happen due to a hardware or operating system malfunction.



SQLITE\_FULL
This value is returned if an insertion failed because there is
no space left on the disk, or the database is too big to hold any
more information. The latter case should only occur for databases
that are larger than 2GB in size.



SQLITE\_CANTOPEN
This value is returned if the database file could not be opened
for some reason.



SQLITE\_PROTOCOL
This value is returned if some other process is messing with
file locks and has violated the file locking protocol that SQLite uses
on its rollback journal files.



SQLITE\_SCHEMA
When the database first opened, SQLite reads the database schema
into memory and uses that schema to parse new SQL statements. If another
process changes the schema, the command currently being processed will
abort because the virtual machine code generated assumed the old
schema. This is the return code for such cases. Retrying the
command usually will clear the problem.



SQLITE\_TOOBIG
SQLite will not store more than about 1 megabyte of data in a single
row of a single table. If you attempt to store more than 1 megabyte
in a single row, this is the return code you get.



SQLITE\_CONSTRAINT
This constant is returned if the SQL statement would have violated
a database constraint.



SQLITE\_MISMATCH
This error occurs when there is an attempt to insert non\-integer
data into a column labeled INTEGER PRIMARY KEY. For most columns, SQLite
ignores the data type and allows any kind of data to be stored. But
an INTEGER PRIMARY KEY column is only allowed to store integer data.



SQLITE\_MISUSE
This error might occur if one or more of the SQLite API routines
is used incorrectly. Examples of incorrect usage include calling
**sqlite\_exec** after the database has been closed using
**sqlite\_close** or 
calling **sqlite\_exec** with the same
database pointer simultaneously from two separate threads.



SQLITE\_NOLFS
This error means that you have attempts to create or access a file
database file that is larger that 2GB on a legacy Unix machine that
lacks large file support.



SQLITE\_AUTH
This error indicates that the authorizer callback
has disallowed the SQL you are attempting to execute.



SQLITE\_ROW
This is one of the return codes from the
**sqlite\_step** routine which is part of the non\-callback API.
It indicates that another row of result data is available.



SQLITE\_DONE
This is one of the return codes from the
**sqlite\_step** routine which is part of the non\-callback API.
It indicates that the SQL statement has been completely executed and
the **sqlite\_finalize** routine is ready to be called.





### 2\.0 Accessing Data Without Using A Callback Function



The **sqlite\_exec** routine described above used to be the only
way to retrieve data from an SQLite database. But many programmers found
it inconvenient to use a callback function to obtain results. So beginning
with SQLite version 2\.7\.7, a second access interface is available that
does not use callbacks.




The new interface uses three separate functions to replace the single
**sqlite\_exec** function.




> ```
> 
> typedef struct sqlite_vm sqlite_vm;
> 
> int sqlite_compile(
>   sqlite *db,              /* The open database */
>   const char *zSql,        /* SQL statement to be compiled */
>   const char **pzTail,     /* OUT: uncompiled tail of zSql */
>   sqlite_vm **ppVm,        /* OUT: the virtual machine to execute zSql */
>   char **pzErrmsg          /* OUT: Error message. */
> );
> 
> int sqlite_step(
>   sqlite_vm *pVm,          /* The virtual machine to execute */
>   int *pN,                 /* OUT: Number of columns in result */
>   const char ***pazValue,  /* OUT: Column data */
>   const char ***pazColName /* OUT: Column names and datatypes */
> );
> 
> int sqlite_finalize(
>   sqlite_vm *pVm,          /* The virtual machine to be finalized */
>   char **pzErrMsg          /* OUT: Error message */
> );
> 
> ```



The strategy is to compile a single SQL statement using
**sqlite\_compile** then invoke **sqlite\_step** multiple times,
once for each row of output, and finally call **sqlite\_finalize**
to clean up after the SQL has finished execution.



#### 2\.1 Compiling An SQL Statement Into A Virtual Machine



The **sqlite\_compile** "compiles" a single SQL statement (specified
by the second parameter) and generates a virtual machine that is able
to execute that statement. 
As with must interface routines, the first parameter must be a pointer
to an sqlite structure that was obtained from a prior call to
**sqlite\_open**.


A pointer to the virtual machine is stored in a pointer which is passed
in as the 4th parameter.
Space to hold the virtual machine is dynamically allocated. To avoid
a memory leak, the calling function must invoke
**sqlite\_finalize** on the virtual machine after it has finished
with it.
The 4th parameter may be set to NULL if an error is encountered during
compilation.




If any errors are encountered during compilation, an error message is
written into memory obtained from **malloc** and the 5th parameter
is made to point to that memory. If the 5th parameter is NULL, then
no error message is generated. If the 5th parameter is not NULL, then
the calling function should dispose of the memory containing the error
message by calling **sqlite\_freemem**.




If the 2nd parameter actually contains two or more statements of SQL,
only the first statement is compiled. (This is different from the
behavior of **sqlite\_exec** which executes all SQL statements
in its input string.) The 3rd parameter to **sqlite\_compile**
is made to point to the first character beyond the end of the first
statement of SQL in the input. If the 2nd parameter contains only
a single SQL statement, then the 3rd parameter will be made to point
to the '\\000' terminator at the end of the 2nd parameter.




On success, **sqlite\_compile** returns SQLITE\_OK.
Otherwise and error code is returned.



#### 2\.2 Step\-By\-Step Execution Of An SQL Statement



After a virtual machine has been generated using **sqlite\_compile**
it is executed by one or more calls to **sqlite\_step**. Each
invocation of **sqlite\_step**, except the last one,
returns a single row of the result.
The number of columns in the result is stored in the integer that
the 2nd parameter points to.
The pointer specified by the 3rd parameter is made to point
to an array of pointers to column values.
The pointer in the 4th parameter is made to point to an array
of pointers to column names and datatypes.
The 2nd through 4th parameters to **sqlite\_step** convey the
same information as the 2nd through 4th parameters of the
**callback** routine when using
the **sqlite\_exec** interface. Except, with **sqlite\_step**
the column datatype information is always included in the in the
4th parameter regardless of whether or not the
[SHOW\_DATATYPES](pragma.html) pragma
is on or off.




Each invocation of **sqlite\_step** returns an integer code that
indicates what happened during that step. This code may be
SQLITE\_BUSY, SQLITE\_ROW, SQLITE\_DONE, SQLITE\_ERROR, or
SQLITE\_MISUSE.




If the virtual machine is unable to open the database file because
it is locked by another thread or process, **sqlite\_step**
will return SQLITE\_BUSY. The calling function should do some other
activity, or sleep, for a short amount of time to give the lock a
chance to clear, then invoke **sqlite\_step** again. This can
be repeated as many times as desired.




Whenever another row of result data is available,
**sqlite\_step** will return SQLITE\_ROW. The row data is
stored in an array of pointers to strings and the 2nd parameter
is made to point to this array.




When all processing is complete, **sqlite\_step** will return
either SQLITE\_DONE or SQLITE\_ERROR. SQLITE\_DONE indicates that the
statement completed successfully and SQLITE\_ERROR indicates that there
was a run\-time error. (The details of the error are obtained from
**sqlite\_finalize**.) It is a misuse of the library to attempt
to call **sqlite\_step** again after it has returned SQLITE\_DONE
or SQLITE\_ERROR.




When **sqlite\_step** returns SQLITE\_DONE or SQLITE\_ERROR,
the \*pN and \*pazColName values are set to the number of columns
in the result set and to the names of the columns, just as they
are for an SQLITE\_ROW return. This allows the calling code to
find the number of result columns and the column names and datatypes
even if the result set is empty. The \*pazValue parameter is always
set to NULL when the return codes is SQLITE\_DONE or SQLITE\_ERROR.
If the SQL being executed is a statement that does not
return a result (such as an INSERT or an UPDATE) then \*pN will
be set to zero and \*pazColName will be set to NULL.




If you abuse the library by trying to call **sqlite\_step**
inappropriately it will attempt return SQLITE\_MISUSE.
This can happen if you call sqlite\_step() on the same virtual machine
at the same
time from two or more threads or if you call sqlite\_step()
again after it returned SQLITE\_DONE or SQLITE\_ERROR or if you
pass in an invalid virtual machine pointer to sqlite\_step().
You should not depend on the SQLITE\_MISUSE return code to indicate
an error. It is possible that a misuse of the interface will go
undetected and result in a program crash. The SQLITE\_MISUSE is
intended as a debugging aid only \- to help you detect incorrect
usage prior to a mishap. The misuse detection logic is not guaranteed
to work in every case.



#### 2\.3 Deleting A Virtual Machine



Every virtual machine that **sqlite\_compile** creates should
eventually be handed to **sqlite\_finalize**. The sqlite\_finalize()
procedure deallocates the memory and other resources that the virtual
machine uses. Failure to call sqlite\_finalize() will result in 
resource leaks in your program.




The **sqlite\_finalize** routine also returns the result code
that indicates success or failure of the SQL operation that the
virtual machine carried out.
The value returned by sqlite\_finalize() will be the same as would
have been returned had the same SQL been executed by **sqlite\_exec**.
The error message returned will also be the same.




It is acceptable to call **sqlite\_finalize** on a virtual machine
before **sqlite\_step** has returned SQLITE\_DONE. Doing so has
the effect of interrupting the operation in progress. Partially completed
changes will be rolled back and the database will be restored to its
original state (unless an alternative recovery algorithm is selected using
an ON CONFLICT clause in the SQL being executed.) The effect is the
same as if a callback function of **sqlite\_exec** had returned
non\-zero.




It is also acceptable to call **sqlite\_finalize** on a virtual machine
that has never been passed to **sqlite\_step** even once.



### 3\.0 The Extended API


Only the three core routines described in section 1\.0 are required to use
SQLite. But there are many other functions that provide 
useful interfaces. These extended routines are as follows:




> ```
> 
> int sqlite_last_insert_rowid(sqlite*);
> 
> int sqlite_changes(sqlite*);
> 
> int sqlite_get_table(
>   sqlite*,
>   char *sql,
>   char ***result,
>   int *nrow,
>   int *ncolumn,
>   char **errmsg
> );
> 
> void sqlite_free_table(char**);
> 
> void sqlite_interrupt(sqlite*);
> 
> int sqlite_complete(const char *sql);
> 
> void sqlite_busy_handler(sqlite*, int (*)(void*,const char*,int), void*);
> 
> void sqlite_busy_timeout(sqlite*, int ms);
> 
> const char sqlite_version[];
> 
> const char sqlite_encoding[];
> 
> int sqlite_exec_printf(
>   sqlite*,
>   char *sql,
>   int (*)(void*,int,char**,char**),
>   void*,
>   char **errmsg,
>   ...
> );
> 
> int sqlite_exec_vprintf(
>   sqlite*,
>   char *sql,
>   int (*)(void*,int,char**,char**),
>   void*,
>   char **errmsg,
>   va_list
> );
> 
> int sqlite_get_table_printf(
>   sqlite*,
>   char *sql,
>   char ***result,
>   int *nrow,
>   int *ncolumn,
>   char **errmsg,
>   ...
> );
> 
> int sqlite_get_table_vprintf(
>   sqlite*,
>   char *sql,
>   char ***result,
>   int *nrow,
>   int *ncolumn,
>   char **errmsg,
>   va_list
> );
> 
> char *sqlite_mprintf(const char *zFormat, ...);
> 
> char *sqlite_vmprintf(const char *zFormat, va_list);
> 
> void sqlite_freemem(char*);
> 
> void sqlite_progress_handler(sqlite*, int, int (*)(void*), void*);
> 
> 
> ```


All of the above definitions are included in the "sqlite.h"
header file that comes in the source tree.


#### 3\.1 The ROWID of the most recent insert


Every row of an SQLite table has a unique integer key. If the
table has a column labeled INTEGER PRIMARY KEY, then that column
serves as the key. If there is no INTEGER PRIMARY KEY column then
the key is a unique integer. The key for a row can be accessed in
a SELECT statement or used in a WHERE or ORDER BY clause using any
of the names "ROWID", "OID", or "\_ROWID\_".


When you do an insert into a table that does not have an INTEGER PRIMARY
KEY column, or if the table does have an INTEGER PRIMARY KEY but the value
for that column is not specified in the VALUES clause of the insert, then
the key is automatically generated. You can find the value of the key
for the most recent INSERT statement using the
**sqlite\_last\_insert\_rowid** API function.


#### 3\.2 The number of rows that changed


The **sqlite\_changes** API function returns the number of rows
that have been inserted, deleted, or modified since the database was
last quiescent. A "quiescent" database is one in which there are
no outstanding calls to **sqlite\_exec** and no VMs created by
**sqlite\_compile** that have not been finalized by **sqlite\_finalize**.
In common usage, **sqlite\_changes** returns the number
of rows inserted, deleted, or modified by the most recent **sqlite\_exec**
call or since the most recent **sqlite\_compile**. But if you have
nested calls to **sqlite\_exec** (that is, if the callback routine
of one **sqlite\_exec** invokes another **sqlite\_exec**) or if
you invoke **sqlite\_compile** to create a new VM while there is
still another VM in existence, then
the meaning of the number returned by **sqlite\_changes** is more
complex.
The number reported includes any changes
that were later undone by a ROLLBACK or ABORT. But rows that are
deleted because of a DROP TABLE are *not* counted.


SQLite implements the command "**DELETE FROM table**" (without
a WHERE clause) by dropping the table then recreating it. 
This is much faster than deleting the elements of the table individually.
But it also means that the value returned from **sqlite\_changes**
will be zero regardless of the number of elements that were originally
in the table. If an accurate count of the number of elements deleted
is necessary, use "**DELETE FROM table WHERE 1**" instead.


#### 3\.3 Querying into memory obtained from malloc()


The **sqlite\_get\_table** function is a wrapper around
**sqlite\_exec** that collects all the information from successive
callbacks and writes it into memory obtained from malloc(). This
is a convenience function that allows the application to get the
entire result of a database query with a single function call.


The main result from **sqlite\_get\_table** is an array of pointers
to strings. There is one element in this array for each column of
each row in the result. NULL results are represented by a NULL
pointer. In addition to the regular data, there is an added row at the 
beginning of the array that contains the name of each column of the
result.


As an example, consider the following query:



> SELECT employee\_name, login, host FROM users WHERE login LIKE 'd%';


This query will return the name, login and host computer name
for every employee whose login begins with the letter "d". If this
query is submitted to **sqlite\_get\_table** the result might
look like this:



> nrow \= 2  
> 
> ncolumn \= 3  
> 
> result\[0] \= "employee\_name"  
> 
> result\[1] \= "login"  
> 
> result\[2] \= "host"  
> 
> result\[3] \= "dummy"  
> 
> result\[4] \= "No such user"  
> 
> result\[5] \= 0  
> 
> result\[6] \= "D. Richard Hipp"  
> 
> result\[7] \= "drh"  
> 
> result\[8] \= "zadok"


Notice that the "host" value for the "dummy" record is NULL so
the result\[] array contains a NULL pointer at that slot.


If the result set of a query is empty, then by default
**sqlite\_get\_table** will set nrow to 0 and leave its
result parameter is set to NULL. But if the EMPTY\_RESULT\_CALLBACKS
pragma is ON then the result parameter is initialized to the names
of the columns only. For example, consider this query which has
an empty result set:



> SELECT employee\_name, login, host FROM users WHERE employee\_name IS NULL;



The default behavior gives this results:




> nrow \= 0  
> 
> ncolumn \= 0  
> 
> result \= 0



But if the EMPTY\_RESULT\_CALLBACKS pragma is ON, then the following
is returned:




> nrow \= 0  
> 
> ncolumn \= 3  
> 
> result\[0] \= "employee\_name"  
> 
> result\[1] \= "login"  
> 
> result\[2] \= "host"


Memory to hold the information returned by **sqlite\_get\_table**
is obtained from malloc(). But the calling function should not try
to free this information directly. Instead, pass the complete table
to **sqlite\_free\_table** when the table is no longer needed.
It is safe to call **sqlite\_free\_table** with a NULL pointer such
as would be returned if the result set is empty.


The **sqlite\_get\_table** routine returns the same integer
result code as **sqlite\_exec**.


#### 3\.4 Interrupting an SQLite operation


The **sqlite\_interrupt** function can be called from a
different thread or from a signal handler to cause the current database
operation to exit at its first opportunity. When this happens,
the **sqlite\_exec** routine (or the equivalent) that started
the database operation will return SQLITE\_INTERRUPT.


#### 3\.5 Testing for a complete SQL statement


The next interface routine to SQLite is a convenience function used
to test whether or not a string forms a complete SQL statement.
If the **sqlite\_complete** function returns true when its input
is a string, then the argument forms a complete SQL statement.
There are no guarantees that the syntax of that statement is correct,
but we at least know the statement is complete. If **sqlite\_complete**
returns false, then more text is required to complete the SQL statement.


For the purpose of the **sqlite\_complete** function, an SQL
statement is complete if it ends in a semicolon.


The **sqlite** command\-line utility uses the **sqlite\_complete**
function to know when it needs to call **sqlite\_exec**. After each
line of input is received, **sqlite** calls **sqlite\_complete**
on all input in its buffer. If **sqlite\_complete** returns true, 
then **sqlite\_exec** is called and the input buffer is reset. If
**sqlite\_complete** returns false, then the prompt is changed to
the continuation prompt and another line of text is read and added to
the input buffer.


#### 3\.6 Library version string


The SQLite library exports the string constant named
**sqlite\_version** which contains the version number of the
library. The header file contains a macro SQLITE\_VERSION
with the same information. If desired, a program can compare
the SQLITE\_VERSION macro against the **sqlite\_version**
string constant to verify that the version number of the
header file and the library match.


#### 3\.7 Library character encoding


By default, SQLite assumes that all data uses a fixed\-size
8\-bit character (iso8859\). But if you give the \-\-enable\-utf8 option
to the configure script, then the library assumes UTF\-8 variable
sized characters. This makes a difference for the LIKE and GLOB
operators and the LENGTH() and SUBSTR() functions. The static
string **sqlite\_encoding** will be set to either "UTF\-8" or
"iso8859" to indicate how the library was compiled. In addition,
the **sqlite.h** header file will define one of the
macros **SQLITE\_UTF8** or **SQLITE\_ISO8859**, as appropriate.


Note that the character encoding mechanism used by SQLite cannot
be changed at run\-time. This is a compile\-time option only. The
**sqlite\_encoding** character string just tells you how the library
was compiled.


#### 3\.8 Changing the library's response to locked files


The **sqlite\_busy\_handler** procedure can be used to register
a busy callback with an open SQLite database. The busy callback will
be invoked whenever SQLite tries to access a database that is locked.
The callback will typically do some other useful work, or perhaps sleep,
in order to give the lock a chance to clear. If the callback returns
non\-zero, then SQLite tries again to access the database and the cycle
repeats. If the callback returns zero, then SQLite aborts the current
operation and returns SQLITE\_BUSY.


The arguments to **sqlite\_busy\_handler** are the opaque
structure returned from **sqlite\_open**, a pointer to the busy
callback function, and a generic pointer that will be passed as
the first argument to the busy callback. When SQLite invokes the
busy callback, it sends it three arguments: the generic pointer
that was passed in as the third argument to **sqlite\_busy\_handler**,
the name of the database table or index that the library is trying
to access, and the number of times that the library has attempted to
access the database table or index.


For the common case where we want the busy callback to sleep,
the SQLite library provides a convenience routine **sqlite\_busy\_timeout**.
The first argument to **sqlite\_busy\_timeout** is a pointer to
an open SQLite database and the second argument is a number of milliseconds.
After **sqlite\_busy\_timeout** has been executed, the SQLite library
will wait for the lock to clear for at least the number of milliseconds 
specified before it returns SQLITE\_BUSY. Specifying zero milliseconds for
the timeout restores the default behavior.


#### 3\.9 Using the \_printf() wrapper functions


The four utility functions



* **sqlite\_exec\_printf()**
* **sqlite\_exec\_vprintf()**
* **sqlite\_get\_table\_printf()**
* **sqlite\_get\_table\_vprintf()**





implement the same query functionality as **sqlite\_exec**
and **sqlite\_get\_table**. But instead of taking a complete
SQL statement as their second argument, the four **\_printf**
routines take a printf\-style format string. The SQL statement to
be executed is generated from this format string and from whatever
additional arguments are attached to the end of the function call.


There are two advantages to using the SQLite printf
functions instead of **sprintf**. First of all, with the
SQLite printf routines, there is never a danger of overflowing a
static buffer as there is with **sprintf**. The SQLite
printf routines automatically allocate (and later frees)
as much memory as is 
necessary to hold the SQL statements generated.


The second advantage the SQLite printf routines have over
**sprintf** are two new formatting options specifically designed
to support string literals in SQL. Within the format string,
the %q formatting option works very much like %s in that it
reads a null\-terminated string from the argument list and inserts
it into the result. But %q translates the inserted string by
making two copies of every single\-quote (') character in the
substituted string. This has the effect of escaping the end\-of\-string
meaning of single\-quote within a string literal. The %Q formatting
option works similar; it translates the single\-quotes like %q and
additionally encloses the resulting string in single\-quotes.
If the argument for the %Q formatting options is a NULL pointer,
the resulting string is NULL without single quotes.



Consider an example. Suppose you are trying to insert a string
value into a database table where the string value was obtained from
user input. Suppose the string to be inserted is stored in a variable
named zString. The code to do the insertion might look like this:



> ```
> 
> sqlite_exec_printf(db,
>   "INSERT INTO table1 VALUES('%s')",
>   0, 0, 0, zString);
> 
> ```


If the zString variable holds text like "Hello", then this statement
will work just fine. But suppose the user enters a string like 
"Hi y'all!". The SQL statement generated reads as follows:


> ```
> 
> INSERT INTO table1 VALUES('Hi y'all')
> 
> ```


This is not valid SQL because of the apostrophe in the word "y'all".
But if the %q formatting option is used instead of %s, like this:



> ```
> 
> sqlite_exec_printf(db,
>   "INSERT INTO table1 VALUES('%q')",
>   0, 0, 0, zString);
> 
> ```


Then the generated SQL will look like the following:



> ```
> 
> INSERT INTO table1 VALUES('Hi y''all')
> 
> ```


Here the apostrophe has been escaped and the SQL statement is well\-formed.
When generating SQL on\-the\-fly from data that might contain a
single\-quote character ('), it is always a good idea to use the
SQLite printf routines and the %q formatting option instead of **sprintf**.



If the %Q formatting option is used instead of %q, like this:



> ```
> 
> sqlite_exec_printf(db,
>   "INSERT INTO table1 VALUES(%Q)",
>   0, 0, 0, zString);
> 
> ```


Then the generated SQL will look like the following:



> ```
> 
> INSERT INTO table1 VALUES('Hi y''all')
> 
> ```


If the value of the zString variable is NULL, the generated SQL
will look like the following:



> ```
> 
> INSERT INTO table1 VALUES(NULL)
> 
> ```


All of the \_printf() routines above are built around the following
two functions:



> ```
> 
> char *sqlite_mprintf(const char *zFormat, ...);
> char *sqlite_vmprintf(const char *zFormat, va_list);
> 
> ```


The **sqlite\_mprintf()** routine works like the standard library
**sprintf()** except that it writes its results into memory obtained
from malloc() and returns a pointer to the malloced buffer. 
**sqlite\_mprintf()** also understands the %q and %Q extensions described
above. The **sqlite\_vmprintf()** is a varargs version of the same
routine. The string pointer that these routines return should be freed
by passing it to **sqlite\_freemem()**.



#### 3\.10 Performing background jobs during large queries
The **sqlite\_progress\_handler()** routine can be used to register a
callback routine with an SQLite database to be invoked periodically during long
running calls to **sqlite\_exec()**, **sqlite\_step()** and the various
wrapper functions.

The callback is invoked every N virtual machine operations, where N is
supplied as the second argument to **sqlite\_progress\_handler()**. The third
and fourth arguments to **sqlite\_progress\_handler()** are a pointer to the
routine to be invoked and a void pointer to be passed as the first argument to
it.

The time taken to execute each virtual machine operation can vary based on
many factors. A typical value for a 1 GHz PC is between half and three million
per second but may be much higher or lower, depending on the query. As such it
is difficult to schedule background operations based on virtual machine
operations. Instead, it is recommended that a callback be scheduled relatively
frequently (say every 1000 instructions) and external timer routines used to
determine whether or not background jobs need to be run. 


4\.0 Adding New SQL Functions
Beginning with version 2\.4\.0, SQLite allows the SQL language to be
extended with new functions implemented as C code. The following interface
is used:


```

typedef struct sqlite_func sqlite_func;

int sqlite_create_function(
  sqlite *db,
  const char *zName,
  int nArg,
  void (*xFunc)(sqlite_func*,int,const char**),
  void *pUserData
);
int sqlite_create_aggregate(
  sqlite *db,
  const char *zName,
  int nArg,
  void (*xStep)(sqlite_func*,int,const char**),
  void (*xFinalize)(sqlite_func*),
  void *pUserData
);

char *sqlite_set_result_string(sqlite_func*,const char*,int);
void sqlite_set_result_int(sqlite_func*,int);
void sqlite_set_result_double(sqlite_func*,double);
void sqlite_set_result_error(sqlite_func*,const char*,int);

void *sqlite_user_data(sqlite_func*);
void *sqlite_aggregate_context(sqlite_func*, int nBytes);
int sqlite_aggregate_count(sqlite_func*);

```


The **sqlite\_create\_function()** interface is used to create 
regular functions and **sqlite\_create\_aggregate()** is used to
create new aggregate functions. In both cases, the **db**
parameter is an open SQLite database on which the functions should
be registered, **zName** is the name of the new function,
**nArg** is the number of arguments, and **pUserData** is
a pointer which is passed through unchanged to the C implementation
of the function. Both routines return 0 on success and non\-zero
if there are any errors.


The length of a function name may not exceed 255 characters.
Any attempt to create a function whose name exceeds 255 characters
in length will result in an error.


For regular functions, the **xFunc** callback is invoked once
for each function call. The implementation of xFunc should call
one of the **sqlite\_set\_result\_...** interfaces to return its
result. The **sqlite\_user\_data()** routine can be used to
retrieve the **pUserData** pointer that was passed in when the
function was registered.


For aggregate functions, the **xStep** callback is invoked once
for each row in the result and then **xFinalize** is invoked at the
end to compute a final answer. The xStep routine can use the
**sqlite\_aggregate\_context()** interface to allocate memory that
will be unique to that particular instance of the SQL function.
This memory will be automatically deleted after xFinalize is called.
The **sqlite\_aggregate\_count()** routine can be used to find out
how many rows of data were passed to the aggregate. The xFinalize
callback should invoke one of the **sqlite\_set\_result\_...**
interfaces to set the final result of the aggregate.


SQLite now implements all of its built\-in functions using this
interface. For additional information and examples on how to create
new SQL functions, review the SQLite source code in the file
**func.c**.

5\.0 Multi\-Threading And SQLite

If SQLite is compiled with the THREADSAFE preprocessor macro set to 1,
then it is safe to use SQLite from two or more threads of the same process
at the same time. But each thread should have its own **sqlite\***
pointer returned from **sqlite\_open**. It is never safe for two
or more threads to access the same **sqlite\*** pointer at the same time.


In precompiled SQLite libraries available on the website, the Unix
versions are compiled with THREADSAFE turned off but the Windows
versions are compiled with THREADSAFE turned on. If you need something
different that this you will have to recompile.


Under Unix, an **sqlite\*** pointer should not be carried across a
**fork()** system call into the child process. The child process
should open its own copy of the database after the **fork()**.

6\.0 Usage Examples
For examples of how the SQLite C/C\+\+ interface can be used,
refer to the source code for the **sqlite** program in the
file [src/shell.c](https://sqlite.org/src/file/src/shell.c.in)
of the source tree.
Additional information about sqlite is available at
<cli.html>.
See also the sources to the Tcl interface for SQLite in
the source file 
[src/tclsqlite.c](https://sqlite.org/src/file/src/tclsqlite.c).
*This page last modified on [2023\-01\-06 00:45:39](https://sqlite.org/docsrc/honeypot) UTC*





