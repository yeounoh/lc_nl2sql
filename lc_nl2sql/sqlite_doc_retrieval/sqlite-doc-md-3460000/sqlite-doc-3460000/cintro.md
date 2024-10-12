




An Introduction To The SQLite C/C\+\+ Interface




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










An Introduction To The SQLite C/C\+\+ Interface


►
Table Of Contents
[1\. Summary](#summary)
[2\. Introduction](#introduction)
[3\. Core Objects And Interfaces](#core_objects_and_interfaces)
[4\. Typical Usage Of Core Routines And Objects](#typical_usage_of_core_routines_and_objects)
[5\. Convenience Wrappers Around Core Routines](#convenience_wrappers_around_core_routines)
[6\. Binding Parameters and Reusing Prepared Statements](#binding_parameters_and_reusing_prepared_statements)
[7\. Configuring SQLite](#configuring_sqlite)
[8\. Extending SQLite](#extending_sqlite)
[9\. Other Interfaces](#other_interfaces)




# 1\. Summary


The following two objects and eight methods comprise the essential
elements of the SQLite interface:



* **[sqlite3](c3ref/sqlite3.html)** →
The database connection object. Created by
[sqlite3\_open()](c3ref/open.html) and destroyed by [sqlite3\_close()](c3ref/close.html).
* **[sqlite3\_stmt](c3ref/stmt.html)** →
The prepared statement object. Created by
[sqlite3\_prepare()](c3ref/prepare.html) and destroyed by [sqlite3\_finalize()](c3ref/finalize.html).
* **[sqlite3\_open()](c3ref/open.html)** →
Open a connection to a new or existing SQLite database.
The constructor for [sqlite3](c3ref/sqlite3.html).
* **[sqlite3\_prepare()](c3ref/prepare.html)** →
Compile SQL text into
byte\-code that will do the work of querying or updating the database.
The constructor for [sqlite3\_stmt](c3ref/stmt.html).
* **[sqlite3\_bind()](c3ref/bind_blob.html)** →
Store application data into
[parameters](lang_expr.html#varparam) of the original SQL.
* **[sqlite3\_step()](c3ref/step.html)** →
Advance an [sqlite3\_stmt](c3ref/stmt.html) to the next result row or to completion.
* **[sqlite3\_column()](c3ref/column_blob.html)** →
Column values in the current result row for an [sqlite3\_stmt](c3ref/stmt.html).
* **[sqlite3\_finalize()](c3ref/finalize.html)** →
Destructor for [sqlite3\_stmt](c3ref/stmt.html).
* **[sqlite3\_close()](c3ref/close.html)** →
Destructor for [sqlite3](c3ref/sqlite3.html).
* **[sqlite3\_exec()](c3ref/exec.html)** →
A wrapper function that does [sqlite3\_prepare()](c3ref/prepare.html), [sqlite3\_step()](c3ref/step.html),
[sqlite3\_column()](c3ref/column_blob.html), and [sqlite3\_finalize()](c3ref/finalize.html) for
a string of one or more SQL statements.


# 2\. Introduction



 SQLite has more than 225 APIs.
 However, most of the APIs are optional and very specialized
 and can be ignored by beginners.
 The core API is small, simple, and easy to learn.
 This article summarizes the core API.




 A separate document, [The SQLite C/C\+\+ Interface](c3ref/intro.html),
 provides detailed
 specifications for all C/C\+\+ APIs for SQLite. Once
 the reader
 understands the basic principles of operation for SQLite,
 [that document](c3ref/intro.html) should be used as a reference
 guide. This article is intended as introduction only and is neither a
 complete nor authoritative reference for the SQLite API.



# 3\. Core Objects And Interfaces



 The principal task of an SQL database engine is to evaluate SQL statements
 of SQL. To accomplish this, the developer needs two objects:



* The [database connection](c3ref/sqlite3.html) object: sqlite3
* The [prepared statement](c3ref/stmt.html) object: sqlite3\_stmt



 Strictly speaking, the [prepared statement](c3ref/stmt.html) object is not required since
 the convenience wrapper interfaces, [sqlite3\_exec](c3ref/exec.html) or
 [sqlite3\_get\_table](c3ref/free_table.html), can be used and these convenience wrappers
 encapsulate and hide the [prepared statement](c3ref/stmt.html) object.
 Nevertheless, an understanding of
 [prepared statements](c3ref/stmt.html) is needed to make full use of SQLite.




 The [database connection](c3ref/sqlite3.html) and [prepared statement](c3ref/stmt.html) objects are controlled
 by a small set of C/C\+\+ interface routine listed below.



* [sqlite3\_open()](c3ref/open.html)
* [sqlite3\_prepare()](c3ref/prepare.html)
* [sqlite3\_step()](c3ref/step.html)
* [sqlite3\_column()](c3ref/column_blob.html)
* [sqlite3\_finalize()](c3ref/finalize.html)
* [sqlite3\_close()](c3ref/close.html)



 Note that the list of routines above is conceptual rather than actual.
 Many of these routines come in multiple versions.
 For example, the list above shows a single routine
 named [sqlite3\_open()](c3ref/open.html) when in fact there are three separate routines
 that accomplish the same thing in slightly different ways:
 [sqlite3\_open()](c3ref/open.html), [sqlite3\_open16()](c3ref/open.html) and [sqlite3\_open\_v2()](c3ref/open.html).
 The list mentions [sqlite3\_column()](c3ref/column_blob.html)
 when in fact no such routine exists.
 The "sqlite3\_column()" shown in the list is a placeholder for
 an entire family of routines that extract column
 data in various datatypes.




 Here is a summary of what the core interfaces do:



* **[sqlite3\_open()](c3ref/open.html)**



 This routine
 opens a connection to an SQLite database file and returns a
 [database connection](c3ref/sqlite3.html) object. This is often the first SQLite API
 call that an application makes and is a prerequisite for most other
 SQLite APIs. Many SQLite interfaces require a pointer to
 the [database connection](c3ref/sqlite3.html) object as their first parameter and can
 be thought of as methods on the [database connection](c3ref/sqlite3.html) object.
 This routine is the constructor for the [database connection](c3ref/sqlite3.html) object.
* **[sqlite3\_prepare()](c3ref/prepare.html)**



 This routine
 converts SQL text into a [prepared statement](c3ref/stmt.html) object and returns a pointer
 to that object. This interface requires a [database connection](c3ref/sqlite3.html) pointer
 created by a prior call to [sqlite3\_open()](c3ref/open.html) and a text string containing
 the SQL statement to be prepared. This API does not actually evaluate
 the SQL statement. It merely prepares the SQL statement for evaluation.

 

Think of each SQL statement as a small computer program. The purpose
 of [sqlite3\_prepare()](c3ref/prepare.html) is to compile that program into object code.
 The [prepared statement](c3ref/stmt.html) is the object code. The [sqlite3\_step()](c3ref/step.html) interface
 then runs the object code to get a result.

 

New applications should always invoke [sqlite3\_prepare\_v2()](c3ref/prepare.html) instead
 of [sqlite3\_prepare()](c3ref/prepare.html). The older [sqlite3\_prepare()](c3ref/prepare.html) is retained for
 backwards compatibility. But [sqlite3\_prepare\_v2()](c3ref/prepare.html) provides a much
 better interface.
* **[sqlite3\_step()](c3ref/step.html)**



 This routine is used to evaluate a [prepared statement](c3ref/stmt.html) that has been
 previously created by the [sqlite3\_prepare()](c3ref/prepare.html) interface. The statement
 is evaluated up to the point where the first row of results are available.
 To advance to the second row of results, invoke [sqlite3\_step()](c3ref/step.html) again.
 Continue invoking [sqlite3\_step()](c3ref/step.html) until the statement is complete.
 Statements that do not return results (ex: INSERT, UPDATE, or DELETE
 statements) run to completion on a single call to [sqlite3\_step()](c3ref/step.html).
* **[sqlite3\_column()](c3ref/column_blob.html)**



 This routine returns a single column from the current row of a result
 set for a [prepared statement](c3ref/stmt.html) that is being evaluated by [sqlite3\_step()](c3ref/step.html).
 Each time [sqlite3\_step()](c3ref/step.html) stops with a new result set row, this routine
 can be called multiple times to find the values of all columns in that row.

 

As noted above, there really is no such thing as a "sqlite3\_column()"
 function in the SQLite API. Instead, what we here call "sqlite3\_column()"
 is a place\-holder for an entire family of functions that return
 a value from the result set in various data types. There are also routines
 in this family that return the size of the result (if it is a string or
 BLOB) and the number of columns in the result set.

 


	+ [sqlite3\_column\_blob()](c3ref/column_blob.html)
	+ [sqlite3\_column\_bytes()](c3ref/column_blob.html)
	+ [sqlite3\_column\_bytes16()](c3ref/column_blob.html)
	+ [sqlite3\_column\_count()](c3ref/column_count.html)
	+ [sqlite3\_column\_double()](c3ref/column_blob.html)
	+ [sqlite3\_column\_int()](c3ref/column_blob.html)
	+ [sqlite3\_column\_int64()](c3ref/column_blob.html)
	+ [sqlite3\_column\_text()](c3ref/column_blob.html)
	+ [sqlite3\_column\_text16()](c3ref/column_blob.html)
	+ [sqlite3\_column\_type()](c3ref/column_blob.html)
	+ [sqlite3\_column\_value()](c3ref/column_blob.html)
* **[sqlite3\_finalize()](c3ref/finalize.html)**



 This routine destroys a [prepared statement](c3ref/stmt.html) created by a prior call
 to [sqlite3\_prepare()](c3ref/prepare.html). Every prepared statement must be destroyed using
 a call to this routine in order to avoid memory leaks.
* **[sqlite3\_close()](c3ref/close.html)**



 This routine closes a [database connection](c3ref/sqlite3.html) previously opened by a call
 to [sqlite3\_open()](c3ref/open.html). All [prepared statements](c3ref/stmt.html) associated with the
 connection should be [finalized](c3ref/finalize.html) prior to closing the
 connection.


# 4\. Typical Usage Of Core Routines And Objects



 An application will typically use
 [sqlite3\_open()](c3ref/open.html) to create a single [database connection](c3ref/sqlite3.html)
 during initialization.
 Note that [sqlite3\_open()](c3ref/open.html) can be used to either open existing database
 files or to create and open new database files.
 While many applications use only a single [database connection](c3ref/sqlite3.html), there is
 no reason why an application cannot call [sqlite3\_open()](c3ref/open.html) multiple times
 in order to open multiple [database connections](c3ref/sqlite3.html) \- either to the same
 database or to different databases. Sometimes a multi\-threaded application
 will create separate [database connections](c3ref/sqlite3.html) for each thread.
 Note that a single [database connection](c3ref/sqlite3.html) can access two or more
 databases using the [ATTACH](lang_attach.html) SQL command, so it is not necessary to
 have a separate database connection for each database file.




 Many applications destroy their [database connections](c3ref/sqlite3.html) using calls to
 [sqlite3\_close()](c3ref/close.html) at shutdown. Or, for example, an application that
 uses SQLite as its [application file format](appfileformat.html) might
 open [database connections](c3ref/sqlite3.html) in response to a File/Open menu action
 and then destroy the corresponding [database connection](c3ref/sqlite3.html) in response
 to the File/Close menu.




 To run an SQL statement, the application follows these steps:



1. Create a [prepared statement](c3ref/stmt.html) using [sqlite3\_prepare()](c3ref/prepare.html).
2. Evaluate the [prepared statement](c3ref/stmt.html) by calling [sqlite3\_step()](c3ref/step.html) one
 or more times.
3. For queries, extract results by calling
 [sqlite3\_column()](c3ref/column_blob.html) in between
 two calls to [sqlite3\_step()](c3ref/step.html).
4. Destroy the [prepared statement](c3ref/stmt.html) using [sqlite3\_finalize()](c3ref/finalize.html).



 The foregoing is all one really needs to know in order to use SQLite
 effectively. All the rest is optimization and detail.



# 5\. Convenience Wrappers Around Core Routines



 The [sqlite3\_exec()](c3ref/exec.html) interface is a convenience wrapper that carries out
 all four of the above steps with a single function call. A callback
 function passed into [sqlite3\_exec()](c3ref/exec.html) is used to process each row of
 the result set. The [sqlite3\_get\_table()](c3ref/free_table.html) is another convenience wrapper
 that does all four of the above steps. The [sqlite3\_get\_table()](c3ref/free_table.html) interface
 differs from [sqlite3\_exec()](c3ref/exec.html) in that it stores the results of queries
 in heap memory rather than invoking a callback.




 It is important to realize that neither [sqlite3\_exec()](c3ref/exec.html) nor
 [sqlite3\_get\_table()](c3ref/free_table.html) do anything that cannot be accomplished using
 the core routines. In fact, these wrappers are implemented purely in
 terms of the core routines.



# 6\. Binding Parameters and Reusing Prepared Statements



 In prior discussion, it was assumed that each SQL statement is prepared
 once, evaluated, then destroyed. However, SQLite allows the same
 [prepared statement](c3ref/stmt.html) to be evaluated multiple times. This is accomplished
 using the following routines:



* [sqlite3\_reset()](c3ref/reset.html)
* [sqlite3\_bind()](c3ref/bind_blob.html)



 After a [prepared statement](c3ref/stmt.html) has been evaluated by one or more calls to
 [sqlite3\_step()](c3ref/step.html), it can be reset in order to be evaluated again by a
 call to [sqlite3\_reset()](c3ref/reset.html).
 Think of [sqlite3\_reset()](c3ref/reset.html) as rewinding the [prepared statement](c3ref/stmt.html) program
 back to the beginning.
 Using [sqlite3\_reset()](c3ref/reset.html) on an existing [prepared statement](c3ref/stmt.html) rather than
 creating a new [prepared statement](c3ref/stmt.html) avoids unnecessary calls to
 [sqlite3\_prepare()](c3ref/prepare.html).
 For many SQL statements, the time needed
 to run [sqlite3\_prepare()](c3ref/prepare.html) equals or exceeds the time needed by
 [sqlite3\_step()](c3ref/step.html). So avoiding calls to [sqlite3\_prepare()](c3ref/prepare.html) can give
 a significant performance improvement.




 It is not commonly useful to evaluate the *exact* same SQL
 statement more than once. More often, one wants to evaluate similar
 statements. For example, you might want to evaluate an INSERT statement
 multiple times with different values. Or you might want to evaluate
 the same query multiple times using a different key in the WHERE clause.
 To accommodate
 this, SQLite allows SQL statements to contain [parameters](lang_expr.html#varparam)
 which are "bound" to values prior to being evaluated. These values can
 later be changed and the same [prepared statement](c3ref/stmt.html) can be evaluated
 a second time using the new values.




 SQLite allows a [parameter](lang_expr.html#varparam) wherever a string literal,
 blob literal, numeric constant, or NULL is allowed
 in queries or data modification statements. (DQL or DML)
 (Parameters may not be used for column or table names,
 or as values for constraints or default values. (DDL))
 A [parameter](lang_expr.html#varparam) takes one of the following forms:



* **?**
* **?***NNN*
* **:***AAA*
* **$***AAA*
* **@***AAA*



 In the examples above, *NNN* is an integer value and
 *AAA* is an identifier.
 A parameter initially has a value of NULL.
 Prior to calling [sqlite3\_step()](c3ref/step.html) for the first time or immediately
 after [sqlite3\_reset()](c3ref/reset.html), the application can invoke the
 [sqlite3\_bind()](c3ref/bind_blob.html) interfaces to attach values
 to the parameters. Each call to [sqlite3\_bind()](c3ref/bind_blob.html)
 overrides prior bindings on the same parameter.




 An application is allowed to prepare multiple SQL statements in advance
 and evaluate them as needed.
 There is no arbitrary limit to the number of outstanding
 [prepared statements](c3ref/stmt.html).
 Some applications call [sqlite3\_prepare()](c3ref/prepare.html) multiple times at start\-up to
 create all of the [prepared statements](c3ref/stmt.html) they will ever need. Other
 applications keep a cache of the most recently used [prepared statements](c3ref/stmt.html)
 and then reuse [prepared statements](c3ref/stmt.html) out of the cache when available.
 Another approach is to only reuse [prepared statements](c3ref/stmt.html) when they are
 inside of a loop.



# 7\. Configuring SQLite



 The default configuration for SQLite works great for most applications.
 But sometimes developers want to tweak the setup to try to squeeze out
 a little more performance, or take advantage of some obscure feature.



 The [sqlite3\_config()](c3ref/config.html) interface is used to make global, process\-wide
 configuration changes for SQLite. The [sqlite3\_config()](c3ref/config.html) interface must
 be called before any [database connections](c3ref/sqlite3.html) are created. The
 [sqlite3\_config()](c3ref/config.html) interface allows the programmer to do things like:


* Adjust how SQLite does [memory allocation](malloc.html), including setting up
 alternative memory allocators appropriate for safety\-critical
 real\-time embedded systems and application\-defined memory allocators.
* Set up a process\-wide [error log](errlog.html).
* Specify an application\-defined page cache.
* Adjust the use of mutexes so that they are appropriate for various
 [threading models](threadsafe.html), or substitute an
 application\-defined mutex system.



 After process\-wide configuration is complete and [database connections](c3ref/sqlite3.html)
 have been created, individual database connections can be configured using
 calls to [sqlite3\_limit()](c3ref/limit.html) and [sqlite3\_db\_config()](c3ref/db_config.html).



# 8\. Extending SQLite



 SQLite includes interfaces that can be used to extend its functionality.
 Such routines include:



* [sqlite3\_create\_collation()](c3ref/create_collation.html)
* [sqlite3\_create\_function()](c3ref/create_function.html)
* [sqlite3\_create\_module()](c3ref/create_module.html)
* [sqlite3\_vfs\_register()](c3ref/vfs_find.html)



 The [sqlite3\_create\_collation()](c3ref/create_collation.html) interface is used to create new
 [collating sequences](datatype3.html#collation) for sorting text.
 The [sqlite3\_create\_module()](c3ref/create_module.html) interface is used to register new
 [virtual table](vtab.html) implementations.
 The [sqlite3\_vfs\_register()](c3ref/vfs_find.html) interface creates new [VFSes](vfs.html).




 The [sqlite3\_create\_function()](c3ref/create_function.html) interface creates new SQL functions \-
 either scalar or aggregate. The new function implementation typically
 makes use of the following additional interfaces:



* [sqlite3\_aggregate\_context()](c3ref/aggregate_context.html)
* [sqlite3\_result()](c3ref/result_blob.html)
* [sqlite3\_user\_data()](c3ref/user_data.html)
* [sqlite3\_value()](c3ref/value_blob.html)



 All of the built\-in SQL functions of SQLite are created using exactly
 these same interfaces. Refer to the SQLite source code, and in particular
 the
 [date.c](https://www.sqlite.org/src/doc/trunk/src/date.c) and
 [func.c](https://www.sqlite.org/src/doc/trunk/src/func.c) source files
 for examples.




 Shared libraries or DLLs can be used as [loadable extensions](loadext.html) to SQLite.



# 9\. Other Interfaces



 This article only mentions the most important and most commonly
 used SQLite interfaces.
 The SQLite library includes many other APIs implementing useful
 features that are not described here.
 A [complete list of functions](c3ref/funclist.html) that form the SQLite
 application programming interface is found at the
 [C/C\+\+ Interface Specification](c3ref/intro.html).
 Refer to that document for complete and authoritative information about
 all SQLite interfaces.



