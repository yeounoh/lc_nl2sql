




Application\-Defined SQL Functions




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Application\-Defined SQL Functions


►
Table Of Contents
[1\. Executive Summary](#executive_summary)
[2\. Defining New SQL Functions](#defining_new_sql_functions)
[2\.1\. Common Parameters](#common_parameters)
[2\.2\. Multiple Calls To sqlite3\_create\_function() For The Same Function](#multiple_calls_to_sqlite3_create_function_for_the_same_function)
[2\.3\. Callbacks](#callbacks)
[2\.3\.1\. The Scalar Function Callback](#the_scalar_function_callback)
[2\.3\.2\. The Aggregate Function Callbacks](#the_aggregate_function_callbacks)
[2\.3\.3\. The Window Function Callbacks](#the_window_function_callbacks)
[2\.3\.4\. Examples](#examples)
[3\. Security Implications](#security_implications)




# 1\. Executive Summary


Applications that use SQLite can define custom SQL functions that call
back into application code to compute their results. The custom SQL
function implementations can be embedded in the application code itself,
or can be [loadable extensions](loadext.html).



Application\-defined or custom SQL functions are created using the
[sqlite3\_create\_function()](c3ref/create_function.html) family of interfaces.
Custom SQL functions can be scalar functions, aggregate functions,
or [window functions](windowfunctions.html).
Custom SQL functions can have any number of arguments from 0 up to
[SQLITE\_MAX\_FUNCTION\_ARG](limits.html#max_function_arg).
The [sqlite3\_create\_function()](c3ref/create_function.html) interface specifies callbacks that are
invoked to carry out the processing for the new SQL function.



SQLite also supports custom [table\-valued functions](vtab.html#tabfunc2), but they are
implemented by a different mechanism that is not covered in this document.



# 2\. Defining New SQL Functions



The [sqlite3\_create\_function()](c3ref/create_function.html) family of interfaces is used to create
new custom SQL functions. Each member of this family is a wrapper around
a common core. All family members accomplish the same thing; they merely
have different calling signatures.



* **[sqlite3\_create\_function()](c3ref/create_function.html)** →
The original version of sqlite3\_create\_function() allows the application
to create a single new SQL function that can be either a scalar or an
aggregate. The name of the function is specified using UTF8\.
* **[sqlite3\_create\_function16()](c3ref/create_function.html)** →
This variant works exactly like the sqlite3\_create\_function() original
except that the name of the function itself is specified as a UTF16
string rather than as a UTF8 string.
* **[sqlite3\_create\_function\_v2()](c3ref/create_function.html)** →
This variant works like the original sqlite3\_create\_function() except
that it includes an additional parameter that is a pointer to a
destructor for the [sqlite3\_user\_data()](c3ref/user_data.html) pointer that is passed in
as the 5th argument to all of the sqlite3\_create\_function() variants.
That destructor function (if it is non\-NULL) is called when the
custom function is deleted \- usually when the database connection is
closing.
* **[sqlite3\_create\_window\_function()](c3ref/create_function.html)** →
This variant works like the original sqlite3\_create\_function() except
that it accepts a different set of callback pointers \- the callback
pointers used by [window function](windowfunctions.html) definitions.


## 2\.1\. Common Parameters


Many of the parameters passed to the [sqlite3\_create\_function()](c3ref/create_function.html)
family of interfaces are common across the entire family.



1. **db** →
The 1st parameter is always a pointer to the [database connection](c3ref/sqlite3.html)
on which the custom SQL function will work. Custom SQL functions are
created separately for each database connection. There is no short\-hand
mechanism for creating SQL functions that work across all database
connections.
2. **zFunctionName** →
The 2nd parameter is the name of the SQL function that is being
created. The name is usually in UTF8, except that the name should
be in UTF16 in the native byte order for [sqlite3\_create\_function16()](c3ref/create_function.html).



The maximum length of a SQL function name is 255 bytes of UTF8\.
Any attempt to create a function with a longer name will result in
an [SQLITE\_MISUSE](rescode.html#misuse) error.



The SQL function creation interfaces may be called multiple
times with the same function name.
If two calls have the same function number but a different number of
arguments, for example, then two variants of the SQL function will
be registered, each taking a different number of arguments.
3. **nArg** →
The 3rd parameter is always the number of arguments that the function
accepts. The value must be an integer between \-1 and 
[SQLITE\_MAX\_FUNCTION\_ARG](limits.html#max_function_arg) (default value: 127\). A value of \-1 means
that the SQL function is a variadic function that can take any number
of arguments between 0 and [SQLITE\_MAX\_FUNCTION\_ARG](limits.html#max_function_arg).
4. **eTextRep** →
The 4th parameter is a 32\-bit integer flag whose bits convey various
properties about the new function. The original purpose of this
parameter was to specify the preferred text encoding for the function,
using one of the following constants:



	* [SQLITE\_UTF8](c3ref/c_any.html)
	* [SQLITE\_UTF16BE](c3ref/c_any.html)
	* [SQLITE\_UTF16LE](c3ref/c_any.html)
All custom SQL functions will accept text in any encoding. Encoding
conversions will happen automatically. The preferred encoding merely
specifies the encoding for which the function implementation is optimized.
It is possible to specify multiple functions with the same name and the
same number of arguments, but different preferred encodings and different
callbacks used to implement the function, and SQLite will chose the
set of callbacks for which the input encodings most closely match the
preferred encoding.

The 4th parameter as more recently be extended with additional flag bits
to convey additional information about the function. The additional
bits include:



	* [SQLITE\_DETERMINISTIC](c3ref/c_deterministic.html#sqlitedeterministic)
	* [SQLITE\_DIRECTONLY](c3ref/c_deterministic.html#sqlitedirectonly)
	* [SQLITE\_INNOCUOUS](c3ref/c_deterministic.html#sqliteinnocuous)
	* [SQLITE\_SUBTYPE](c3ref/c_deterministic.html#sqlitesubtype)
Additional bits may be added in future versions of SQLite.
5. **pApp** →
The 5th parameter is an arbitrary pointer that is passed through
into the callback routines. SQLite itself does nothing with this
pointer, except to make it available to the callbacks, and to pass
it into the destructor when the function is unregistered.


## 2\.2\. Multiple Calls To sqlite3\_create\_function() For The Same Function



It is common for an application to invoke sqlite3\_create\_function() multiple
times for the same SQL function. For example, if an SQL function can take
either 2 or 3 arguments, then sqlite3\_create\_function() would be invoked
once for the 2\-argument version and a second time for the 3\-argument version.
The underlying implementation (the callbacks) can be different for both
variants.




An application can also register multiple SQL functions with the same name
and same number of arguments, but a different preferred text encoding.
In that case, SQLite will invoke the function using the callbacks for
the version whose preferred text encoding most closely matches the database
text encoding. In this way, multiple implementations of the same function
can be provided that are optimized for UTF8 or UTF16\.




If multiple calls to sqlite3\_create\_function() specify the same function name,
and the same number of arguments, and the same preferred text encoding, then
the callbacks and other parameters of the second call overwrite the first,
and the destructor callback from the first call (if it exists) is invoked.




## 2\.3\. Callbacks



SQLite evaluates an SQL function by invoking callback routines.



### 2\.3\.1\. The Scalar Function Callback


Scalar SQL functions are implemented by a single callback in the
**xFunc** parameter to sqlite3\_create\_function().
The following code demonstrations the implementation of a "noop(X)"
scalar SQL function that merely returns its argument:




```
static void noopfunc(
  sqlite3_context *context,
  int argc,
  sqlite3_value **argv
){
  assert( argc==1 );
  sqlite3_result_value(context, argv[0]);
}

```


The 1st parameter, **context**, is a pointer to an opaque object
that describes the content from which the SQL function was invoked. This
context point becomes the first parameter to many other routines that
the function implement might to invoke, including:


* [sqlite3\_aggregate\_context](c3ref/aggregate_context.html)
* [sqlite3\_context\_db\_handle](c3ref/context_db_handle.html)
* [sqlite3\_get\_auxdata](c3ref/get_auxdata.html)
* [sqlite3\_result\_blob](c3ref/result_blob.html)
* [sqlite3\_result\_blob64](c3ref/result_blob.html)
* [sqlite3\_result\_double](c3ref/result_blob.html)
* [sqlite3\_result\_error](c3ref/result_blob.html)
* [sqlite3\_result\_error16](c3ref/result_blob.html)
* [sqlite3\_result\_error\_code](c3ref/result_blob.html)
* [sqlite3\_result\_error\_nomem](c3ref/result_blob.html)
* [sqlite3\_result\_error\_toobig](c3ref/result_blob.html)
* [sqlite3\_result\_int](c3ref/result_blob.html)
* [sqlite3\_result\_int64](c3ref/result_blob.html)
* [sqlite3\_result\_null](c3ref/result_blob.html)
* [sqlite3\_result\_pointer](c3ref/result_blob.html)
* [sqlite3\_result\_subtype](c3ref/result_subtype.html)
* [sqlite3\_result\_text](c3ref/result_blob.html)
* [sqlite3\_result\_text16](c3ref/result_blob.html)
* [sqlite3\_result\_text16be](c3ref/result_blob.html)
* [sqlite3\_result\_text16le](c3ref/result_blob.html)
* [sqlite3\_result\_text64](c3ref/result_blob.html)
* [sqlite3\_result\_value](c3ref/result_blob.html)
* [sqlite3\_result\_zeroblob](c3ref/result_blob.html)
* [sqlite3\_result\_zeroblob64](c3ref/result_blob.html)
* [sqlite3\_set\_auxdata](c3ref/get_auxdata.html)
* [sqlite3\_user\_data](c3ref/user_data.html)





The [sqlite3\_result() family of functions](c3ref/result_blob.html) are
used to specify the result of the scalar SQL function. One or more of
these should be invoked by the callback to set the function return value.
If none of these routines are invoked for a specific callback, then the
return value will be NULL.



The [sqlite3\_user\_data()](c3ref/user_data.html) routine returns a copy of the **pArg**
pointer that was given to [sqlite3\_create\_function()](c3ref/create_function.html) when the SQL
function was created.



The [sqlite3\_context\_db\_handle()](c3ref/context_db_handle.html) routine returns a pointer to the
[database connection](c3ref/sqlite3.html) object.



The [sqlite3\_aggregate\_context()](c3ref/aggregate_context.html) routine is used only in the
implementations of aggregate and window functions. Scalar functions
may not use [sqlite3\_aggregate\_context()](c3ref/aggregate_context.html). The [sqlite3\_aggregate\_context()](c3ref/aggregate_context.html)
function is included in the interface list only for completeness.




The 2nd and 3rd arguments to the scalar SQL function implemenetation,
**argc** and **argv**, are
the number of arguments to the SQL function itself and the values for
each argument of the SQL function.
Argument values can be of any datatype and are thus stored in
instances of the [sqlite3\_value](c3ref/value.html) object.
Specific C\-language values can be extracted from this object using
the [sqlite3\_value() family of interfaces](c3ref/value_blob.html).



### 2\.3\.2\. The Aggregate Function Callbacks


Aggregate SQL functions are implemented by using two callback
functions, **xStep** and **xFinal**. The xStep() function 
is called for each row of the aggregate and the xFinal() function
is invoked to compute the final answer at the end.
The following (slightly simplified) version of the built\-in
count() function illustrates:




```
typedef struct CountCtx CountCtx;
struct CountCtx {
  i64 n;
};
static void countStep(sqlite3_context *context, int argc, sqlite3_value **argv){
  CountCtx *p;
  p = sqlite3_aggregate_context(context, sizeof(*p));
  if( (argc==0 || SQLITE_NULL!=sqlite3_value_type(argv[0])) && p ){
    p->n++;
  }
}   
static void countFinalize(sqlite3_context *context){
  CountCtx *p;
  p = sqlite3_aggregate_context(context, 0);
  sqlite3_result_int64(context, p ? p->n : 0);
}

```

Recall that there are two versions of the count() aggregate.
With zero arguments, count() returns a count of the number of rows.
With one argument, count() returns the number of times that the
argument was non\-NULL.



The countStep() callback is invoked once for each row in the aggregate.
As you can see, the count is incremented if either there are no arguments,
or if the one argument is not NULL.



The step function for an aggregate should always begin with a call
to the [sqlite3\_aggregate\_context()](c3ref/aggregate_context.html) routine to fetch the persistent
state of the aggregate function. On the first invocation of the step()
function, the aggregate context is initialized to a block of memory
that is N bytes in size, where N is the second parameter to
sqlite3\_aggregate\_context() and that memory is zeroed. On all subsequent
calls to the step() function, the same block of memory is returned.
Except, sqlite3\_aggregate\_context() might return NULL in the case of
an out\-of\-memory error, so aggregate functions should be prepared to
deal with that case.



After all rows are processed the countFinalize() routine is called
exactly once. This routine computes the final result and invokes
one of the [sqlite3\_result()](c3ref/result_blob.html) family of functions
to set the final result. The aggregate context will be freed automatically
by SQLite, though the xFinalize() routine must clean up any substructure
associated with the aggregate context before it returns. If the xStep()
method is called one or more times, then SQLite guarantees thta the
xFinal() method will be called at once, even if the query aborts.



### 2\.3\.3\. The Window Function Callbacks


[Window functions](windowfunctions.html) use the same xStep() and xFinal() callbacks that
aggregate functions use, plus two others: **xValue** and **xInverse**.
See the documentation on
[application\-defined window functions](windowfunctions.html#udfwinfunc) for further details.



### 2\.3\.4\. Examples


There are dozens and dozens of SQL function implementations scattered
throughout the SQLite source code that can be used as example applications.
The built\-in SQL functions use the same interface as application\-defined
SQL functions, so built\-in functions can be used as examples too.
Search for "sqlite3\_context" in the SQLite source code to find examples.




# 3\. Security Implications



Application\-defined SQL functions can become security vulnerabilities if
not carefully managed. Suppose, for example, an application defines
a new "system(X)" SQL function that runs its argument X as a command and
returns the integer result code. Perhaps the implementation is like this:




```
static void systemFunc(
  sqlite3_context *context,
  int argc,
  sqlite3_value **argv
){
  const char *zCmd = (const char*)sqlite3_value_text(argv[0]);
  if( zCmd!=0 ){
    int rc = system(zCmd);
    sqlite3_result_int(context, rc);
  }
}

```


This is a function with powerful side\-effects. Most programmers would
be naturally cautious about using it, but probably would not see the
harm in merely having it available. But there is great risk in merely
defining such a function, even if the application itself never invokes
it!




Suppose the application normally does a query against table TAB1
when it starts up. If an attacker can gain access to the database
file and modify the schema like this:




```
ALTER TABLE tab1 RENAME TO tab1_real;
CREATE VIEW tab1 AS SELECT * FROM tab1 WHERE system('rm -rf *') IS NOT NULL;

```


Then, when the application attempts to open the database, register the
system() function, then run an innocent query against the "tab1" table,
it instead deletes all the files in its working directory. Yikes!




To prevent this kind of mischief, applications that create their own
custom SQL functions should take one or more of the following safety
precautions. The more precautions taken the better:



1. Invoke [sqlite3\_db\_config](c3ref/db_config.html)(db,[SQLITE\_DBCONFIG\_TRUSTED\_SCHEMA](c3ref/c_dbconfig_defensive.html#sqlitedbconfigtrustedschema),0,0\)
on each [database connection](c3ref/sqlite3.html) as soon as it is opened.
This prevents application\-defined functions from being used in places
where an attacker might be able to surreptiously invoke them by modifying
a database schema:



	* In VIEWs.
	* In TRIGGERs.
	* In CHECK constraints of a table definition.
	* In DEFAULT constraints of a table definition.
	* In the definitions of generated columns.
	* In the expression part of an index on an expression.
	* In the WHERE clause of a partial index.
To put it another way, this setting requires that application\-defined
functions only be run directly by top\-level SQL invoked from the application
itself, not as a consequence of doing some other innocent\-looking query.
2. Use the [PRAGMA trusted\_schema\=OFF](pragma.html#pragma_trusted_schema) SQL statement to disable trusted
schema. This has the same effect as the previous bullet, but does not
require the use of C\-code and hence can be performed in programs written
in another programming language and that do not have access SQLite
C\-language APIs.
3. Compile SQLite using the [\-DSQLITE\_TRUSTED\_SCHEMA\=0](compile.html#trusted_schema) compile\-time option.
This make SQLite distrust application\-defined functions inside of
the schema by default.
4. If any application\-defined SQL functions have potentially dangerous
side\-effects, or if they could potentially leak sensitive information
to an attacker if misused, then tag those functions using the
[SQLITE\_DIRECTONLY](c3ref/c_deterministic.html#sqlitedirectonly) option on the "enc" parameter. This means
that the function can never be run from schema\-code even if the
trusted\-schema option is on.
5. Never tag an application\-defined SQL function with [SQLITE\_INNOCUOUS](c3ref/c_deterministic.html#sqliteinnocuous)
unless you really need to and you have checked the implementation closely
and are certain that it can do no harm even if it falls under the
control of an attacker.


*This page last modified on [2024\-04\-16 17:22:18](https://sqlite.org/docsrc/honeypot) UTC* 


