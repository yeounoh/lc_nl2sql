




The SQLITE\_STMT Virtual Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The SQLITE\_STMT Virtual Table


# 1\. Overview



The SQLITE\_STMT extension implements an [eponymous\-only virtual table](vtab.html#epoonlyvtab) that
provides information about all [prepared statements](c3ref/stmt.html) associated with
the [database connection](c3ref/sqlite3.html).




The SQLITE\_STMT extension is included in the [amalgamation](amalgamation.html) though 
it is disabled
by default. Use the [SQLITE\_ENABLE\_STMTVTAB](compile.html#enable_stmtvtab) compile\-time option to enable
the SQLITE\_STMT extension. The SQLITE\_STMT extension can also be 
loaded at run\-time
by compiling the extension into a shared library or DLL using the source
code at <https://sqlite.org/src/file/ext/misc/stmt.c> and following the
instructions for how to [compile loadable extensions](loadext.html#build).




The SQLITE\_STMT extension is enabled in default builds
of the [command\-line shell](cli.html).



# 2\. Usage



The SQLITE\_STMT virtual table is a read\-only table that can be directly
queried to access information about all prepared statements on the 
current database connection. For example:




```
SELECT * FROM sqlite_stmt;

```


A statement such as the above can be run immediately prior to invoking
[sqlite3\_close()](c3ref/close.html) to confirm that all prepared statements have been 
[finalized](c3ref/finalize.html) and to help identify and track down prepared
statements that have "leaked" and missed finalization.




The SQLITE\_STMT virtual table can also be used to access performance
information about prepared statements, to aid in optimization an application.
For example,
to find out how much memory is being used by [prepared statements](c3ref/stmt.html) that have
never been used, one could run:




```
SELECT sum(mem) FROM sqlite_stmt WHERE run=0;

```

## 2\.1\. Columns



The columns are provided by the SQLITE\_STMT virtual table are summarized by
the hypothetical CREATE TABLE statement show here:




```
CREATE TABLE sqlite_stmt(
  sql    TEXT,    -- Original SQL text
  ncol   INT,     -- Number of output columns
  ro     BOOLEAN, -- True for "read only" statements
  busy   BOOLEAN, -- True if the statement is current running
  nscan  INT,     -- Number of full-scan steps
  nsort  INT,     -- Number of sort operations
  naidx  INT,     -- Number of automatic index inserts
  nstep  INT,     -- Number of byte-code engine steps
  reprep INT,     -- Number of reprepare operations
  run    INT,     -- Number of times this statement has been run
  mem    INT      -- Heap memory used by this statement
);

```

Future releases may add new output columns and may change the order
of legacy columns.
Further detail about the meaning of each column in the SQLITE\_STMT virtual
table is provided below:



* **sql**:
The original SQL text of the prepared statement. If the prepared
statement is compiled using the [sqlite3\_prepare()](c3ref/prepare.html) interface, then
the SQL text might not have been saved, in which case this column
will be NULL.
* **ncol**:
The number of columns in the result set of a query.
For DML statements, this column has a value of 0\.
* **ro**:
The "read only" column. This column is true (non\-zero) if the
SQL statement is a query and false (zero) if it is a DML statement.
* **busy**:
This field is true if the prepared statement is currently running.
In other words, this field is true if [sqlite3\_step()](c3ref/step.html) has been called
on the [prepared statement](c3ref/stmt.html) at least once but [sqlite3\_reset()](c3ref/reset.html) has
not yet been called to reset it.
* **nscan**:
This field is the number of times that the [bytecode engine](opcode.html) has stepped
through a table as part of a full\-table scan. A large number if this
field may indicate an opportunity to improve performance by adding an
index. This field is equivalent to the [SQLITE\_STMTSTATUS\_FULLSCAN\_STEP](c3ref/c_stmtstatus_counter.html#sqlitestmtstatusfullscanstep)
value.
* **nsort**:
This field is the number of times that the [bytecode engine](opcode.html) had to sort.
A positive value in this field may indicate an opportunity to improve
performance by adding an index that will cause the query results to
appear naturally in the desired order. 
This field is equivalent to the [SQLITE\_STMTSTATUS\_SORT](c3ref/c_stmtstatus_counter.html#sqlitestmtstatussort) value.
* **naidx**:
This field is the number of rows that have been inserted into
[automatic indexes](optoverview.html#autoindex). A positive value in this field may indicate 
an opportunity to improve performance by adding a named index that
take the place of the automatic index.
This field is equivalent to the [SQLITE\_STMTSTATUS\_AUTOINDEX](c3ref/c_stmtstatus_counter.html#sqlitestmtstatusautoindex) value.
* **nstep**:
This field is the number of [bytecode engine](opcode.html) operations that have
been performed for the prepared statement. This field can be used
as a proxy for how much CPU time a statement has used.
This field is equivalent to the [SQLITE\_STMTSTATUS\_VM\_STEP](c3ref/c_stmtstatus_counter.html#sqlitestmtstatusvmstep) value.
* **reprep**:
This field is the number of times that the statement has had to be
reprepared due to schema changes or changes to parameter bindings.
This field is equivalent to the [SQLITE\_STMTSTATUS\_REPREPARE](c3ref/c_stmtstatus_counter.html#sqlitestmtstatusreprepare) value.
* **run**:
This field is the number of times that the statement has been run.
This field is equivalent to the [SQLITE\_STMTSTATUS\_RUN](c3ref/c_stmtstatus_counter.html#sqlitestmtstatusrun) value.
* **mem**:
This field is the number of bytes of heap storage used by the
prepared statement.
This field is equivalent to the [SQLITE\_STMTSTATUS\_MEMUSED](c3ref/c_stmtstatus_counter.html#sqlitestmtstatusmemused) value.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


