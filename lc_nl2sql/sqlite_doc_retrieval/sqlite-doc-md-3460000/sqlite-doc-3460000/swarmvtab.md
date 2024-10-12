




Swarmvtab Virtual Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Swarmvtab Virtual Table


►
Table Of Contents
[1\. Overview](#overview)
[2\. Compiling and Using Swarmvtab](#compiling_and_using_swarmvtab)
[3\. Advanced Usage](#advanced_usage)
[3\.1\. SQL Parameters](#sql_parameters)
[3\.2\. The "maxopen" Parameter](#the_maxopen_parameter)
[3\.3\. The "openclose" Callback](#the_openclose_callback)
[3\.4\. The "missing" Callback](#the_missing_callback)
[3\.5\. Component table "context" values](#component_table_context_values)





# 1\. Overview


The "swarmvtab" virtual table allows the user to query a large number 
of tables (hereafter "component" tables) with similar schemas but distinct
ranges of rowid values as if they were a single database table. The tables may
be (and usually are) located in different databases. Swarmvtab tables are
read\-only.



Component tables must not be declared WITHOUT ROWID, and must all have
the same schema, but may have different names within their databases. In
this context, "the same schema" means that:



* All component tables must have the same set of columns, in the same 
 order.
* The types and default collation sequences attached to each column
 must be the same for all component tables.
* All component tables must have the same PRIMARY KEY declaration (if any).


A swarmvtab table has the same schema as each of its component tables.



A swarmvtab virtual table is created as follows:




```
CREATE VIRTUAL TABLE temp.<name> USING swarmvtab(<sql-statement>);

```

Swarmvtab virtual tables must be created in the temp schema. Attempting
to create a swarmvtab in the main or an attached database is an error.



The SQL statement supplied as the argument to the CREATE VIRTUAL TABLE
statement is executed when the table is created. It must return either four
or five columns. Each row returned describes one of the component tables. The
first four columns are interpreted, from first to last, as:



* **Database URI**. A filename or URI that can be used to open the
 database containing the component table.
* **Table name**. The name of the component table within its database.
* **Minimum rowid**. The smallest rowid value that the component
 table may contain.
* **Maximum rowid**. The smallest rowid value that the component
 table may contain.


The interpretation of the final column, if it is present, is 
[described here](swarmvtab.html#component_table_context_values).



For example, say the SQL statement returns the following data when 
executed:





| Database URI | Table name | Minimum rowid | Maximum rowid |
| --- | --- | --- | --- |
| test.db1 | t1 | 0 | 10 |
| test.db2 | t2 | 11 | 20 |
| test.db3 | t1 | 21 | 30 |
| test.db4 | t1 | 31 | 40 |


and the user queries the swarmvtab table for the row with rowid value
25\. The swarmvtab table will open database file "test.db3" and read the
data to return from table "t1" (as 25 falls within the range of rowids
assigned to table "t1" in "test.db3").



Swarmvtab efficiently handles range and equality constraints on the
rowid (or other INTEGER PRIMARY KEY) field only. If a query does not 
contain such a constraint, then swarmvtab finds the results by opening
each database in turn and linearly scanning the component table. Which 
generates a correct result, but is often slow.



There must be no overlapping rowid ranges in the rows returned by
the SQL statement. It is an error if there are.



The swarmvtab implementation may open or close databases at any 
point. By default, it attempts to limit the maximum number of 
simultaneously open database files to nine. This is not a hard limit \-
it is possible to construct a scenario that will cause swarmvtab to 
exceed it.




# 2\. Compiling and Using Swarmvtab


The code for the swarmvtab virtual table is found in the
ext/misc/unionvtab.c file of the main SQLite source tree. It may be compiled
into an SQLite [loadable extension](loadext.html) using a command like:




```
gcc -g -fPIC -shared unionvtab.c -o unionvtab.so

```

Alternatively, the unionvtab.c file may be compiled into the application. 
In this case, the following function should be invoked to register the
extension with each new database connection:




```
int sqlite3_unionvtab_init(sqlite3 *db, void*, void*);

```

 The first argument passed should be the database handle to register the
extension with. The second and third arguments should both be passed 0\.



 The source file and entry point are named for "unionvtab" instead of
"swarmvtab". Unionvtab is a [separately documented](unionvtab.html) virtual table 
that is bundled with swarmvtab.




# 3\. Advanced Usage


Most users of swarmvtab will only use the features described above. 
This section describes features designed for more esoteric use cases. These
features all involve specifying extra optional parameters following the SQL
statement as part of the CREATE VIRTUAL TABLE command. An optional parameter 
is specified using its name, followed by an "\=" character, followed by an
optionally quoted value. Whitespace may separate the name, "\=" character 
and value. For example:




```
CREATE VIRTUAL TABLE temp.sv USING swarmvtab (
  'SELECT ...',                -- the SELECT statement
  maxopen = 20,                -- An optional parameter
  missing='missing_udf'        -- Another optional parameter
);

```

The following sections describe the supported parameters. Specifying
an unrecognized parameter name is an error.




## 3\.1\. SQL Parameters


If a parameter name begins with a ":", then it is assumed to be a
value to bind to the SQL statement before executing it. The value is always
bound as text. It is an error if the specified SQL parameter does not
exist. For example:




```
CREATE VIRTUAL TABLE temp.x1 USING swarmvtab (
  "SELECT :dir || local_filename, tbl, min, max FROM components",
  :dir = '/home/user/app/databases/'
);

```

When the above CREATE VIRTUAL TABLE statement is executed, swarmvtab binds
the text value "/home/user/app/databases/" to the :dir parameter of the
SQL statement before executing it.



A single CREATE VIRTUAL TABLE statement may contain any number of SQL
parameters.




## 3\.2\. The "maxopen" Parameter


By default, swarmvtab attempts to limit the number of simultaneously
open databases to nine. This parameter allows that limit to be changed.
For example, to create a swarmvtab table that may hold up to 30 databases
open simultaneously:




```
CREATE VIRTUAL TABLE temp.x1 USING swarmvtab (
  "SELECT ...",
  maxopen=30
);

```

Raising the number of open databases may improve performance in some
scenarios.




## 3\.3\. The "openclose" Callback


The "openclose" parameter allows the user to specify the name of a
[application\-defined SQL function](appfunc.html) that will be invoked just before
swarmvtab opens a database, and again just after it closes one. The first
argument passed to the open close function is the filename or URI
identifying the database to be opened or just recently closed (the same
value returned in the leftmost column of the SQL statement provided to
the CREATE VIRTUAL TABLE command). The second argument is integer value
0 when the function is invoked before opening a database, and 1 when it
is invoked after one is closed. For example, if:




```
CREATE VIRTUAL TABLE temp.x1 USING swarmvtab (
  "SELECT ...",
  openclose = 'openclose_udf'
);

```

then before each database containing a component table is opened, 
swarmvtab effectively executes:




```
SELECT openclose_udf(<database-name>, 0);

```

After a database is closed, swarmvtab runs the equivalent of:




```
SELECT openclose_udf(<database-name>, 1);

```

Any value returned by the openclose function is ignored. If an invocation
made before opening a database returns an error, then the database file is
not opened and the error returned to the user. This is the only scenario
in which swarmvtab will issue an "open" invocation without also eventually
issuing a corresponding "close" call. If there are still databases open,
"close" calls may be issued from within the eventual sqlite3\_close() call
on the applications database that deletes the temp schema in which the
swarmvtab table resides.



Errors returned by "close" invocations are always ignored.




## 3\.4\. The "missing" Callback


The "missing" parameter allows the user to specify the name of a
[application\-defined SQL function](appfunc.html) that will be invoked just before
swarmvtab opens a database if it finds that the required database file
is not present on disk. This provides the application with an opportunity
to retrieve the required database from a remote source before swarmvtab
attempts to open it. The only argument passed to the "missing" function
is the name or URI that identifies the database being opened. Assuming:




```
CREATE VIRTUAL TABLE temp.x1 USING swarmvtab (
  "SELECT ...",
  openclose = 'openclose_udf',
  missing='missing_udf'
);

```

then the missing function is invoked as follows:




```
SELECT missing_udf(<database-name>);

```

If the missing function returns an error, then the database is not 
opened and the error returned to the user. If an openclose function is
configured, then a "close" invocation is issued at this point to match
the earlier "open". The following pseudo\-code illustrates the procedure used
by a swarmvtab instance with both missing and openclose functions configured
when a component database is opened.




```
SELECT openclose_udf(<database-name>, 0);
if( error ) return error;
if( db does not exist ){
  SELECT missing_udf(<database-name>);
  if( error ){
    SELECT openclose_udf(<database-name>, 1);
    return error;
  }
}
sqlite3_open_v2(<database-name>);
if( error ){
  SELECT openclose_udf(<database-name>, 1);
  return error;
}
// db successfully opened!

```


## 3\.5\. Component table "context" values


 If the SELECT statement specified as part of the CREATE VIRTUAL 
TABLE command returns five columns, then the final column is used
for application context only. Swarmvtab does not use this value at
all, except that it is passed after \<database\-name\> to both
the openclose and missing functions, if specified. In other words,
instead of invoking the functions as described above, if the "context"
column is present swarmvtab instead invokes:




```
SELECT missing_udf(<database-name>, <context>);
SELECT openclose_udf(<database-name>, <context>, 0);
SELECT openclose_udf(<database-name>, <context>, 1);

```

as required.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


