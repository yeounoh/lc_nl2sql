




The Error And Warning Log




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Error And Warning Log


►
Table Of Contents
[1\. Setting Up The Error Logging Callback](#setting_up_the_error_logging_callback)
[2\. Interface Details](#interface_details)
[3\. Variety of Error Messages](#variety_of_error_messages)
[4\. Summary](#summary)




## Overview


SQLite can be configured to invoke a callback function containing
an error code and a terse error message whenever anomalies occur.
This mechanism is very helpful in tracking obscure problems that
occur rarely and in the field. Application developers are encouraged
to take advantage of the error logging facility of SQLite in their
products, as it is very low CPU and memory cost but can be a
huge aid for debugging.


# 1\. Setting Up The Error Logging Callback


There can only be a single error logging callback per process.
The error logging callback is registered at start\-time using C\-code
similar to the following:




> ```
> 
> [sqlite3_config](c3ref/config.html)([SQLITE_CONFIG_LOG](c3ref/c_config_covering_index_scan.html#sqliteconfiglog), errorLogCallback, pData);
> 
> ```


The error logger callback function might look something like this:



> ```
> 
> void errorLogCallback(void *pArg, int iErrCode, const char *zMsg){
>   fprintf(stderr, "(%d) %s\n", iErrCode, zMsg);
> }
> 
> ```


The example above illustrates the signature of the error logger callback.
However, in an embedded application, one usually does not print
messages on stderr. Instead, one might store the messages in a
preallocated circular buffer where they can be accessed when diagnostic
information is needed during debugging. Or perhaps the messages can be
sent to [Syslog](http://en.wikipedia.org/wiki/Syslog). Somehow, the
messages need to be stored where they are accessible to developers,
not displayed to end users.


Do not misunderstand: There is nothing technically wrong with displaying 
the error logger messages to end users. The messages do not contain
sensitive or private information that must be protected from unauthorized
viewing. Rather the messages are technical in nature and are not useful
or meaningful to the typical end user. The messages coming from the
error logger are intended for database geeks. Display them accordingly.


# 2\. Interface Details


The third argument to the [sqlite3\_config](c3ref/config.html)([SQLITE\_CONFIG\_LOG](c3ref/c_config_covering_index_scan.html#sqliteconfiglog),...) 
interface (the "pData" argument in the example above) is a pointer to arbitrary
data. SQLite passes this pointer through to the first argument of the
error logger callback. The pointer can be used to pass application\-specific 
setup or state information, if desired. Or it can simply be a NULL 
pointer which is ignored by the callback.


The second argument to the error logger callback is an integer
[extended error code](rescode.html#extrc). The third argument to the error logger is the
text of the error message. The error message text is stored in a fixed\-length
stack buffer in the calling function and so will only be valid for the
duration of the error logger callback function. The error logger should
make a copy of this message into persistent storage if retention of the
message is needed.


The error logger callback should be treated like a signal handler.
The application should save off or otherwise process the error, then return
as soon as possible. No other SQLite APIs should be invoked, directly or
indirectly, from the error logger. SQLite is not reentrant through
the error logger callback. In particular, the error logger callback
is invoked when a memory allocation fails, so it is generally a bad idea
to try to allocate memory inside the error logger. Do not even think
about trying to store the error message in another SQLite database.


Applications can use the [sqlite3\_log(E,F,..)](c3ref/log.html) API to send new messages
to the log, if desired, but this is discouraged. The [sqlite3\_log()](c3ref/log.html)
interface is intended for use by extensions only, not by applications.


# 3\. Variety of Error Messages


The error messages that might be sent to the error logger and their
exact format is subject to changes from one release to the next. So
applications should not depend on any particular error message text formats or
error codes. Things do not change capriciously, but they do sometimes
changes.


The following is a partial list of the kinds of messages that might
appear in the error logger callback.


* Any time there is an error either compiling an SQL statement 
(using [sqlite3\_prepare\_v2()](c3ref/prepare.html) or its siblings) or running an SQL
statement (using [sqlite3\_step()](c3ref/step.html)) that error is logged.
* When a schema change occurs that requires a prepared statement to be reparsed
and reprepared, that event is logged with the error code SQLITE\_SCHEMA.
The reparse and reprepare is normally automatic (assuming that
[sqlite3\_prepare\_v2()](c3ref/prepare.html) has been used to prepare the statements originally,
which is recommended) and so these logging events are normally the only
way to know that reprepares are taking place.
* SQLITE\_NOTICE messages are logged whenever a database has to be recovered
because the previous writer crashed without completing its transaction.
The error code is SQLITE\_NOTICE\_RECOVER\_ROLLBACK when recovering a
[rollback journal](lockingv3.html#rollback) and SQLITE\_NOTICE\_RECOVER\_WAL when recovering a 
[write\-ahead log](wal.html).
* SQLITE\_WARNING messages are logged when database files are renamed or
aliased in ways that can lead to database corruption.
(See [1](howtocorrupt.html#unlink) and [2](howtocorrupt.html#alias) for
additional information.)
* Out of memory (OOM) error conditions generate error logging events
with the SQLITE\_NOMEM error code and a message that says how many bytes
of memory were requested by the failed allocation.
* I/O errors in the OS\-interface generate error logging events.
The message to these events gives the line number in the source code where
the error originated and the filename associated with the event when
there is a corresponding file.
* When database corruption is detected, an SQLITE\_CORRUPT error
logger callback is invoked. As with I/O errors, the error message text
contains the line number in the original source code where the error
was first detected.
* An error logger callback is invoked on SQLITE\_MISUSE errors.
This is useful in detecting application design issues when return codes
are not consistently checked in the application code.


SQLite strives to keep error logger traffic low and only send messages
to the error logger when there really is something wrong. Applications
might further cull the error message traffic 
by deliberately ignoring certain classes of error
messages that they do not care about. For example, an application that
makes frequent database schema changes might want to ignore all
SQLITE\_SCHEMA errors.


# 4\. Summary


The use of the error logger callback is highly recommended.
The debugging information that the error logger provides has proven
very useful in tracking down obscure problems that occur with applications
after they get into the field. The error logger callback has also 
proven useful in catching occasional errors that the application
misses because of inconsistent checking of API return codes.
Developers are encouraged to implement an error logger callback early
in the development cycle in order to spot unexpected behavior quickly,
and to leave the error logger callback turned on through deployment.
If the error logger never finds a problem, then no harm is done. 
But failure to set up an appropriate error logger might compromise
diagnostic capabilities later on.


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


