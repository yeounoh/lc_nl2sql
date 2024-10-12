




The Bytecode() And Tables\_Used() Table\-Valued Functions




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Bytecode() And Tables\_Used() Table\-Valued Functions


# 1\. Overview



Bytecode and tables\_used are [virtual tables](vtab.html) built into SQLite that
access information about [prepared statements](c3ref/stmt.html).
Both bytecode and tables\_used operate as [table\-valued functions](vtab.html#tabfunc2).
They take a single required argument which is either the text of
an SQL statement, or a pointer to an existing prepared statement.
The bytecode function returns one row of result for each [bytecode](opcode.html)
operation in the prepared statement. The tables\_used function returns
one row for each persistent btree (either a table or an index) accessed
by the prepared statement.



# 2\. Usage



The bytecode and tables\_used tables are only available if SQLite has
been compiled with the [\-DSQLITE\_ENABLE\_BYTECODE\_VTAB](compile.html#enable_bytecode_vtab) compile\-time option.
The [CLI](cli.html) has been compiled that way, and so you can use the standard
[CLI](cli.html) as a test platform to experiement.




Both virtual tables are read\-only [eponymous\-only virtual tables](vtab.html#epoonlyvtab). You use them
by mentioning them directly in the FROM clause of a SELECT statement.
They both require a single argument which is the SQL statement to be
analyzed. For example:




```
SELECT * FROM bytecode('SELECT * FROM bytecode(?1)');

```


The argument can be either the text of an SQL statement, in which case
the bytecode (or tables\_used) for that statement is returned, or the
argument can be a parameter such as ?1 or $stmt that is later bound
to a [prepared statement](c3ref/stmt.html) object using the
[sqlite3\_bind\_pointer()](c3ref/bind_blob.html) interface. Use a pointer type of
"stmt\-pointer" for the [sqlite3\_bind\_pointer()](c3ref/bind_blob.html) interface.



## 2\.1\. Schema



The schema of the bytecode table is:




```
CREATE TABLE bytecode(
  addr INT,
  opcode TEXT,
  p1 INT,
  p2 INT,
  p3 INT,
  p4 TEXT,
  p5 INT,
  comment TEXT,
  subprog TEXT,
  stmt HIDDEN
);

```


The first eight columns are the address, opcode, and operands for a
single [bytecode](opcode.html) in the virtual machine that implements the statement.
These columns are the same columns output when using EXPLAIN. The
bytecode virtual tables shows all operations in the prepared statement,
both the main body of the prepared statement and in subprograms used
to implement triggers or foreign key actions. The "subprog" field
is NULL for the main body of the prepared statement, or is the trigger
name or the string "(FK)" for triggers and foreign key actions.




The schema for the tables\_used table is:




```
CREATE TABLE tables_used(
  type TEXT,
  schema TEXT,
  name TEXT,
  wr INT,
  subprog TEXT,
  stmt HIDDEN
);

```


The tables\_used table is intended to show which btrees of the database file
are read or written by a prepared statement, both by the main statement
itself but also by related triggers and foreign key actions. The columns
are as follows:



* **type** → Either "table" or "index", depending on what role
the btree is serving.
* **schema** → Which database file the btree is located in.
This will be "main" for the main database (the usual case), or "temp" for
TEMP tables and indexes, or the name assigned to [attached](lang_attach.html) databases by
the [ATTACH](lang_attach.html) statement.
* **name** → The name of the table or index
* **wr** → 0 if the object is read, 1 if the object is written
* **subprog** → The sub\-program in which the object is
accessed. NULL means the main body of the prepared statement. Otherwise
this field is the name of a trigger or "(FK)" for a foreign key action.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


