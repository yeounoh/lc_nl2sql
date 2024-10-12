




C/C\+\+ Interface For SQLite Version 3 (old)




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog








**Note:**
This document was written in 2004 as a guide to helping programmers
move from using SQLite version 2 to SQLite version 3\. The information
in this document is still essentially correct, however there have been
many changes and enhancements over the years. We recommend that the
following documents be used instead:
* [An Introduction To The SQLite C/C\+\+ Interface](cintro.html)
* [SQLite C/C\+\+ Reference Guide](c3ref/intro.html)






## C/C\+\+ Interface For SQLite Version 3


### 1\.0 Overview



SQLite version 3\.0 is a new version of SQLite, derived from
the SQLite 2\.8\.13 code base, but with an incompatible file format
and API.
SQLite version 3\.0 was created to answer demand for the following features:



* Support for UTF\-16\.
* User\-definable text collating sequences.
* The ability to store BLOBs in indexed columns.



It was necessary to move to version 3\.0 to implement these features because
each requires incompatible changes to the database file format. Other
incompatible changes, such as a cleanup of the API, were introduced at the
same time under the theory that it is best to get your incompatible changes
out of the way all at once. 




The API for version 3\.0 is similar to the version 2\.X API,
but with some important changes. Most noticeably, the "sqlite\_"
prefix that occurs on the beginning of all API functions and data
structures are changed to "sqlite3\_". 
This avoids confusion between the two APIs and allows linking against both
SQLite 2\.X and SQLite 3\.0 at the same time.




There is no agreement on what the C datatype for a UTF\-16
string should be. Therefore, SQLite uses a generic type of void\*
to refer to UTF\-16 strings. Client software can cast the void\* 
to whatever datatype is appropriate for their system.



### 2\.0 C/C\+\+ Interface



The API for SQLite 3\.0 includes 83 separate functions in addition
to several data structures and \#defines. (A complete
[API reference](c3ref/intro.html) is provided as a separate 
document.)
Fortunately, the interface is not nearly as complex as its size implies.
Simple programs can still make do with only 3 functions:
[sqlite3\_open()](c3ref/open.html), [sqlite3\_exec()](c3ref/exec.html), and [sqlite3\_close()](c3ref/close.html).
More control over the execution of the database engine is provided
using [sqlite3\_prepare\_v2()](c3ref/prepare.html)
to compile an SQLite statement into byte code and
[sqlite3\_step()](c3ref/step.html) to execute that bytecode.
A family of routines with names beginning with 
[sqlite3\_column\_](c3ref/column_blob.html)
is used to extract information about the result set of a query.
Many interface functions come in pairs, with both a UTF\-8 and
UTF\-16 version. And there is a collection of routines
used to implement user\-defined SQL functions and user\-defined
text collating sequences.



#### 2\.1 Opening and closing a database



> ```
> 
>    typedef struct sqlite3 sqlite3;
>    int sqlite3_open(const char*, sqlite3**);
>    int sqlite3_open16(const void*, sqlite3**);
>    int sqlite3_close(sqlite3*);
>    const char *sqlite3_errmsg(sqlite3*);
>    const void *sqlite3_errmsg16(sqlite3*);
>    int sqlite3_errcode(sqlite3*);
> 
> ```



The sqlite3\_open() routine returns an integer error code rather than
a pointer to the sqlite3 structure as the version 2 interface did.
The difference between sqlite3\_open()
and sqlite3\_open16() is that sqlite3\_open16() takes UTF\-16 (in host native
byte order) for the name of the database file. If a new database file
needs to be created, then sqlite3\_open16() sets the internal text
representation to UTF\-16 whereas sqlite3\_open() sets the text
representation to UTF\-8\.




The opening and/or creating of the database file is deferred until the
file is actually needed. This allows options and parameters, such
as the native text representation and default page size, to be
set using PRAGMA statements.




The sqlite3\_errcode() routine returns a result code for the most
recent major API call. sqlite3\_errmsg() returns an English\-language
text error message for the most recent error. The error message is
represented in UTF\-8 and will be ephemeral \- it could disappear on
the next call to any SQLite API function. sqlite3\_errmsg16() works like
sqlite3\_errmsg() except that it returns the error message represented
as UTF\-16 in host native byte order.




The error codes for SQLite version 3 are unchanged from version 2\.
They are as follows:




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
> #define SQLITE_CONSTRAINT  19   /* Abort due to contraint violation */
> #define SQLITE_MISMATCH    20   /* Data type mismatch */
> #define SQLITE_MISUSE      21   /* Library used incorrectly */
> #define SQLITE_NOLFS       22   /* Uses OS features not supported on host */
> #define SQLITE_AUTH        23   /* Authorization denied */
> #define SQLITE_ROW         100  /* sqlite_step() has another row ready */
> #define SQLITE_DONE        101  /* sqlite_step() has finished executing */
> 
> ```


#### 2\.2 Executing SQL statements



> ```
> 
>    typedef int (*sqlite_callback)(void*,int,char**, char**);
>    int sqlite3_exec(sqlite3*, const char *sql, sqlite_callback, void*, char**);
> 
> ```



The [sqlite3\_exec()](c3ref/exec.html) function works much as it did in SQLite version 2\.
Zero or more SQL statements specified in the second parameter are compiled
and executed. Query results are returned to a callback routine.




In SQLite version 3, the sqlite3\_exec routine is just a wrapper around
calls to the prepared statement interface.




> ```
> 
>    typedef struct sqlite3_stmt sqlite3_stmt;
>    int sqlite3_prepare(sqlite3*, const char*, int, sqlite3_stmt**, const char**);
>    int sqlite3_prepare16(sqlite3*, const void*, int, sqlite3_stmt**, const void**);
>    int sqlite3_finalize(sqlite3_stmt*);
>    int sqlite3_reset(sqlite3_stmt*);
> 
> ```



The sqlite3\_prepare interface compiles a single SQL statement into byte code
for later execution. This interface is now the preferred way of accessing
the database.




The SQL statement is a UTF\-8 string for sqlite3\_prepare().
The sqlite3\_prepare16() works the same way except
that it expects a UTF\-16 string as SQL input.
Only the first SQL statement in the input string is compiled.
The fifth parameter is filled in with a pointer to the next (uncompiled)
SQLite statement in the input string, if any.
The sqlite3\_finalize() routine deallocates a prepared SQL statement.
All prepared statements must be finalized before the database can be
closed.
The sqlite3\_reset() routine resets a prepared SQL statement so that it
can be executed again.




The SQL statement may contain tokens of the form "?" or "?nnn" or ":aaa"
where "nnn" is an integer and "aaa" is an identifier.
Such tokens represent unspecified literal values (or "wildcards")
to be filled in later by the 
[sqlite3\_bind](c3ref/bind_blob.html) interface.
Each wildcard has an associated number which is its sequence in the
statement or the "nnn" in the case of a "?nnn" form. 
It is allowed for the same wildcard
to occur more than once in the same SQL statement, in which case
all instance of that wildcard will be filled in with the same value.
Unbound wildcards have a value of NULL.




> ```
> 
>    int sqlite3_bind_blob(sqlite3_stmt*, int, const void*, int n, void(*)(void*));
>    int sqlite3_bind_double(sqlite3_stmt*, int, double);
>    int sqlite3_bind_int(sqlite3_stmt*, int, int);
>    int sqlite3_bind_int64(sqlite3_stmt*, int, long long int);
>    int sqlite3_bind_null(sqlite3_stmt*, int);
>    int sqlite3_bind_text(sqlite3_stmt*, int, const char*, int n, void(*)(void*));
>    int sqlite3_bind_text16(sqlite3_stmt*, int, const void*, int n, void(*)(void*));
>    int sqlite3_bind_value(sqlite3_stmt*, int, const sqlite3_value*);
> 
> ```



There is an assortment of sqlite3\_bind routines used to assign values
to wildcards in a prepared SQL statement. Unbound wildcards
are interpreted as NULLs. Bindings are not reset by sqlite3\_reset().
But wildcards can be rebound to new values after an sqlite3\_reset().




After an SQL statement has been prepared (and optionally bound), it
is executed using:




> ```
> 
>    int sqlite3_step(sqlite3_stmt*);
> 
> ```



The sqlite3\_step() routine return SQLITE\_ROW if it is returning a single
row of the result set, or SQLITE\_DONE if execution has completed, either
normally or due to an error. It might also return SQLITE\_BUSY if it is
unable to open the database file. If the return value is SQLITE\_ROW, then
the following routines can be used to extract information about that row
of the result set:




> ```
> 
>    const void *sqlite3_column_blob(sqlite3_stmt*, int iCol);
>    int sqlite3_column_bytes(sqlite3_stmt*, int iCol);
>    int sqlite3_column_bytes16(sqlite3_stmt*, int iCol);
>    int sqlite3_column_count(sqlite3_stmt*);
>    const char *sqlite3_column_decltype(sqlite3_stmt *, int iCol);
>    const void *sqlite3_column_decltype16(sqlite3_stmt *, int iCol);
>    double sqlite3_column_double(sqlite3_stmt*, int iCol);
>    int sqlite3_column_int(sqlite3_stmt*, int iCol);
>    long long int sqlite3_column_int64(sqlite3_stmt*, int iCol);
>    const char *sqlite3_column_name(sqlite3_stmt*, int iCol);
>    const void *sqlite3_column_name16(sqlite3_stmt*, int iCol);
>    const unsigned char *sqlite3_column_text(sqlite3_stmt*, int iCol);
>    const void *sqlite3_column_text16(sqlite3_stmt*, int iCol);
>    int sqlite3_column_type(sqlite3_stmt*, int iCol);
> 
> ```



The [sqlite3\_column\_count()](c3ref/column_count.html)
function returns the number of columns in
the results set. sqlite3\_column\_count() can be called at any time after
[sqlite3\_prepare\_v2()](c3ref/prepare.html). [sqlite3\_data\_count()](c3ref/data_count.html) works similarly to
[sqlite3\_column\_count()](c3ref/column_count.html) except that it only works following [sqlite3\_step()](c3ref/step.html).
If the previous call to [sqlite3\_step()](c3ref/step.html) returned SQLITE\_DONE or an error code,
then [sqlite3\_data\_count()](c3ref/data_count.html) will return 0 whereas [sqlite3\_column\_count()](c3ref/column_count.html) will
continue to return the number of columns in the result set.



Returned data is examined using the other 
[sqlite3\_column\_\*\*\*()](c3ref/column_blob.html) functions, 
all of which take a column number as their second parameter. Columns are
zero\-indexed from left to right. Note that this is different to parameters,
which are indexed starting at one.




The [sqlite3\_column\_type()](c3ref/column_blob.html) function returns the
datatype for the value in the Nth column. The return value is one
of these:




> ```
> 
>    #define SQLITE_INTEGER  1
>    #define SQLITE_FLOAT    2
>    #define SQLITE_TEXT     3
>    #define SQLITE_BLOB     4
>    #define SQLITE_NULL     5
> 
> ```



The sqlite3\_column\_decltype() routine returns text which is the
declared type of the column in the CREATE TABLE statement. For an
expression, the return type is an empty string. sqlite3\_column\_name()
returns the name of the Nth column. sqlite3\_column\_bytes() returns
the number of bytes in a column that has type BLOB or the number of bytes
in a TEXT string with UTF\-8 encoding. sqlite3\_column\_bytes16() returns
the same value for BLOBs but for TEXT strings returns the number of bytes
in a UTF\-16 encoding.
sqlite3\_column\_blob() return BLOB data. 
sqlite3\_column\_text() return TEXT data as UTF\-8\.
sqlite3\_column\_text16() return TEXT data as UTF\-16\.
sqlite3\_column\_int() return INTEGER data in the host machines native
integer format.
sqlite3\_column\_int64() returns 64\-bit INTEGER data.
Finally, sqlite3\_column\_double() return floating point data.




It is not necessary to retrieve data in the format specify by
sqlite3\_column\_type(). If a different format is requested, the data
is converted automatically.




Data format conversions can invalidate the pointer returned by
prior calls to sqlite3\_column\_blob(), sqlite3\_column\_text(), and/or
sqlite3\_column\_text16(). Pointers might be invalided in the following
cases:



* The initial content is a BLOB and sqlite3\_column\_text() 
or sqlite3\_column\_text16()
is called. A zero\-terminator might need to be added to the string.
* The initial content is UTF\-8 text and sqlite3\_column\_bytes16() or
sqlite3\_column\_text16() is called. The content must be converted to UTF\-16\.
* The initial content is UTF\-16 text and sqlite3\_column\_bytes() or
sqlite3\_column\_text() is called. The content must be converted to UTF\-8\.



Note that conversions between UTF\-16be and UTF\-16le 
are always done in place and do
not invalidate a prior pointer, though of course the content of the buffer
that the prior pointer points to will have been modified. Other kinds
of conversion are done in place when it is possible, but sometime it is
not possible and in those cases prior pointers are invalidated. 




The safest and easiest to remember policy is this: assume that any
result from
* sqlite3\_column\_blob(),
* sqlite3\_column\_text(), or
* sqlite3\_column\_text16()


is invalided by subsequent calls to 
* sqlite3\_column\_bytes(),
* sqlite3\_column\_bytes16(),
* sqlite3\_column\_text(), or
* sqlite3\_column\_text16().


This means that you should always call sqlite3\_column\_bytes() or
sqlite3\_column\_bytes16() before calling sqlite3\_column\_blob(),
sqlite3\_column\_text(), or sqlite3\_column\_text16().



#### 2\.3 User\-defined functions



User defined functions can be created using the following routine:




> ```
> 
>    typedef struct sqlite3_value sqlite3_value;
>    int sqlite3_create_function(
>      sqlite3 *,
>      const char *zFunctionName,
>      int nArg,
>      int eTextRep,
>      void*,
>      void (*xFunc)(sqlite3_context*,int,sqlite3_value**),
>      void (*xStep)(sqlite3_context*,int,sqlite3_value**),
>      void (*xFinal)(sqlite3_context*)
>    );
>    int sqlite3_create_function16(
>      sqlite3*,
>      const void *zFunctionName,
>      int nArg,
>      int eTextRep,
>      void*,
>      void (*xFunc)(sqlite3_context*,int,sqlite3_value**),
>      void (*xStep)(sqlite3_context*,int,sqlite3_value**),
>      void (*xFinal)(sqlite3_context*)
>    );
>    #define SQLITE_UTF8     1
>    #define SQLITE_UTF16    2
>    #define SQLITE_UTF16BE  3
>    #define SQLITE_UTF16LE  4
>    #define SQLITE_ANY      5
> 
> ```



The nArg parameter specifies the number of arguments to the function.
A value of 0 indicates that any number of arguments is allowed. The
eTextRep parameter specifies what representation text values are expected
to be in for arguments to this function. The value of this parameter should
be one of the parameters defined above. SQLite version 3 allows multiple
implementations of the same function using different text representations.
The database engine chooses the function that minimization the number
of text conversions required.




Normal functions specify only xFunc and leave xStep and xFinal set to NULL.
Aggregate functions specify xStep and xFinal and leave xFunc set to NULL.
There is no separate sqlite3\_create\_aggregate() API.




The function name is specified in UTF\-8\. A separate sqlite3\_create\_function16()
API works the same as sqlite\_create\_function()
except that the function name is specified in UTF\-16 host byte order.




Notice that the parameters to functions are now pointers to sqlite3\_value
structures instead of pointers to strings as in SQLite version 2\.X.
The following routines are used to extract useful information from these
"values":




> ```
> 
>    const void *sqlite3_value_blob(sqlite3_value*);
>    int sqlite3_value_bytes(sqlite3_value*);
>    int sqlite3_value_bytes16(sqlite3_value*);
>    double sqlite3_value_double(sqlite3_value*);
>    int sqlite3_value_int(sqlite3_value*);
>    long long int sqlite3_value_int64(sqlite3_value*);
>    const unsigned char *sqlite3_value_text(sqlite3_value*);
>    const void *sqlite3_value_text16(sqlite3_value*);
>    int sqlite3_value_type(sqlite3_value*);
> 
> ```



Function implementations use the following APIs to acquire context and
to report results:




> ```
> 
>    void *sqlite3_aggregate_context(sqlite3_context*, int nbyte);
>    void *sqlite3_user_data(sqlite3_context*);
>    void sqlite3_result_blob(sqlite3_context*, const void*, int n, void(*)(void*));
>    void sqlite3_result_double(sqlite3_context*, double);
>    void sqlite3_result_error(sqlite3_context*, const char*, int);
>    void sqlite3_result_error16(sqlite3_context*, const void*, int);
>    void sqlite3_result_int(sqlite3_context*, int);
>    void sqlite3_result_int64(sqlite3_context*, long long int);
>    void sqlite3_result_null(sqlite3_context*);
>    void sqlite3_result_text(sqlite3_context*, const char*, int n, void(*)(void*));
>    void sqlite3_result_text16(sqlite3_context*, const void*, int n, void(*)(void*));
>    void sqlite3_result_value(sqlite3_context*, sqlite3_value*);
>    void *sqlite3_get_auxdata(sqlite3_context*, int);
>    void sqlite3_set_auxdata(sqlite3_context*, int, void*, void (*)(void*));
> 
> ```


#### 2\.4 User\-defined collating sequences



The following routines are used to implement user\-defined
collating sequences:




> ```
> 
>    sqlite3_create_collation(sqlite3*, const char *zName, int eTextRep, void*,
>       int(*xCompare)(void*,int,const void*,int,const void*));
>    sqlite3_create_collation16(sqlite3*, const void *zName, int eTextRep, void*,
>       int(*xCompare)(void*,int,const void*,int,const void*));
>    sqlite3_collation_needed(sqlite3*, void*, 
>       void(*)(void*,sqlite3*,int eTextRep,const char*));
>    sqlite3_collation_needed16(sqlite3*, void*,
>       void(*)(void*,sqlite3*,int eTextRep,const void*));
> 
> ```



The sqlite3\_create\_collation() function specifies a collating sequence name
and a comparison function to implement that collating sequence. The
comparison function is only used for comparing text values. The eTextRep
parameter is one of SQLITE\_UTF8, SQLITE\_UTF16LE, SQLITE\_UTF16BE, or
SQLITE\_ANY to specify which text representation the comparison function works
with. Separate comparison functions can exist for the same collating
sequence for each of the UTF\-8, UTF\-16LE and UTF\-16BE text representations.
The sqlite3\_create\_collation16() works like sqlite3\_create\_collation() except
that the collation name is specified in UTF\-16 host byte order instead of
in UTF\-8\.




The sqlite3\_collation\_needed() routine registers a callback which the
database engine will invoke if it encounters an unknown collating sequence.
The callback can lookup an appropriate comparison function and invoke
sqlite\_3\_create\_collation() as needed. The fourth parameter to the callback
is the name of the collating sequence in UTF\-8\. For sqlite3\_collation\_need16()
the callback sends the collating sequence name in UTF\-16 host byte order.



*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


