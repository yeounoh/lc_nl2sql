




Generated Columns




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Generated Columns


►
Table Of Contents
[1\. Introduction](#introduction)
[2\. Syntax](#syntax)
[2\.1\. VIRTUAL versus STORED columns](#virtual_versus_stored_columns)
[2\.2\. Capabilities](#capabilities)
[2\.3\. Limitations](#limitations)
[3\. Compatibility](#compatibility)




# 1\. Introduction


Generated columns (also sometimes called "computed columns")
are columns of a table whose values are a function of other columns
in the same row.
Generated columns can be read, but their values can not be directly
written. The only way to change the value of a generated column is to
modify the values of the other columns used to calculate
the generated column.



# 2\. Syntax


Syntactically, generated columns are designated using a
"GENERATED ALWAYS" [column\-constraint](syntax/column-constraint.html). For example:




```
CREATE TABLE t1(
   a INTEGER PRIMARY KEY,
   b INT,
   c TEXT,
   d INT GENERATED ALWAYS AS (a*abs(b)) VIRTUAL,
   e TEXT GENERATED ALWAYS AS (substr(c,b,b+1)) STORED
);

```

The statement above has three ordinary columns, "a" (the PRIMARY KEY),
"b", and "c", and two generated columns "d" and "e".



The "GENERATED ALWAYS" keywords at the beginning of the constraint
and the "VIRTUAL" or "STORED" keyword at the end are all optional.
Only the "AS" keyword and the parenthesized expression are required.
If the trailing "VIRTUAL" or "STORED" keyword is omitted, then
VIRTUAL is the default. Hence, the example statement above could
be simplified to just:




```
CREATE TABLE t1(
   a INTEGER PRIMARY KEY,
   b INT,
   c TEXT,
   d INT AS (a*abs(b)),
   e TEXT AS (substr(c,b,b+1)) STORED
);

```

## 2\.1\. VIRTUAL versus STORED columns


Generated columns can be either VIRTUAL or STORED. The value of
a VIRTUAL column is computed when read, whereas the value of a STORED
column is computed when the row is written. STORED columns take up space
in the database file, whereas VIRTUAL columns use more CPU cycles when
being read.



From the point of view of SQL, STORED and VIRTUAL columns are almost
exactly the same. Queries against either class of generated column
produce the same results. The only functional difference is that
one cannot add new STORED columns using the
[ALTER TABLE ADD COLUMN](lang_altertable.html#altertabaddcol) command. Only VIRTUAL columns can be added
using ALTER TABLE.



## 2\.2\. Capabilities


1. Generated columns can have a datatype. SQLite attempts to transform
the result of the generating expression into that datatype using the
same [affinity](datatype3.html#affinity) rules as for ordinary columns.
2. Generated columns may have NOT NULL, CHECK, and UNIQUE constraints,
and foreign key constraints, just like ordinary columns.
3. Generated columns can participate in indexes, just like ordinary
columns.
4. The expression of a generated column can refer to any of the
other declared columns in the table, including other generated columns,
as long as the expression does not directly or indirectly refer back
to itself.
5. Generated columns can occur anywhere in the table definition. Generated
columns can be interspersed among ordinary columns. It is not necessary
to put generated columns at the end of the list of columns in the
table definition, as is shown in the examples above.


## 2\.3\. Limitations


1. Generated columns may not have a [default value](lang_createtable.html#dfltval) (they may not use the
"DEFAULT" clause). The value of a generated column is always the value
specified by the expression that follows the "AS" keyword.
2. Generated columns may not be used as part of the [PRIMARY KEY](lang_createtable.html#primkeyconst).
(Future versions of SQLite might relax this constraint for STORED columns.)
3. The expression of a generated column may only reference
constant literals and columns within the same row, and may only use
scalar [deterministic functions](deterministic.html). The expression may not use subqueries,
aggregate functions, window functions, or table\-valued functions.
4. The expression of a generated column may refer to other generated columns
in the same row, but no generated column can depend upon itself, either
directly or indirectly.
5. The expression of a generated column may not directly reference
the [ROWID](lang_createtable.html#rowid), though it can reference the [INTEGER PRIMARY KEY](lang_createtable.html#rowid) column,
which is often the same thing.
6. Every table must have at least one non\-generated column.
7. It is not possible to [ALTER TABLE ADD COLUMN](lang_altertable.html#altertabaddcol) a STORED column.
One can add a VIRTUAL column, however.
8. The datatype and [collating sequence](datatype3.html#collation) of the generated column are determined
only by the datatype and [COLLATE clause](lang_createtable.html#collateclause) on the column definition.
The datatype and collating sequence of the GENERATED ALWAYS AS expression
have no affect on the datatype and collating sequence of the column itself.
9. Generated columns are not included in the list of columns provided by
the [PRAGMA table\_info](pragma.html#pragma_table_info) statement. But they are included in the output of
the newer [PRAGMA table\_xinfo](pragma.html#pragma_table_xinfo) statement.


# 3\. Compatibility


Generated column support was added with SQLite version 3\.31\.0
(2020\-01\-22\). If an earlier version of SQLite attempts to read
a database file that contains a generated column in its schema, then
that earlier version will perceive the generated column syntax as an
error and will report that the database schema is corrupt.



To clarify: SQLite version 3\.31\.0 can read and write any database
created by any prior version of SQLite going back to 
SQLite 3\.0\.0 (2004\-06\-18\). And, earlier versions of SQLite,
prior to 3\.31\.0, can read and write databases created by SQLite
version 3\.31\.0 and later as long
as the database schema does not contain features, such as
generated columns, that are not understood by the earlier version.
Problems only arise if you create a new database that contains
generated columns, using SQLite version 3\.31\.0 or later, and then
try to read or write that database file using an earlier version of
SQLite that does not understand generated columns.


*This page last modified on [2022\-11\-09 20:11:26](https://sqlite.org/docsrc/honeypot) UTC* 


