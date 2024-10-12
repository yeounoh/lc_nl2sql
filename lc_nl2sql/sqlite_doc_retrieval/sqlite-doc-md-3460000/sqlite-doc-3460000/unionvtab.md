




The UNION Virtual Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The UNION Virtual Table


1. The UNION virtual table (hereafter: "union\-vtab")
is a [virtual table](vtab.html) that makes multiple independent
[rowid tables](rowidtable.html) tables look like a single large table.
2. The tables that participate in a union\-vtab can be in the same 
database file, or they can be in separate databases files that
are [ATTACH](lang_attach.html)\-ed to the same database connection.
3. The union\-vtab is not built into SQLite.
Union\-vtab is a [loadable extension](loadext.html).
The source code for union\-vtab is contained in a single file located at
[ext/misc/unionvtab.c](https://sqlite.org/src/file/ext/misc/unionvtab.c)
in the SQLite source tree.
4. A new union\-vtab instance is created as follows:




> **CREATE VIRTUAL TABLE temp.***tabname* **USING unionvtab(***query***);**
5. Every union\-vtab must be in the TEMP namespace. Hence, the "**temp.**"
prior to *tabname* is required. Only the union\-vtab itself is required
to be in the TEMP namespace \- the individual tables that are being unioned
can be any [ATTACH](lang_attach.html)\-ed database.
6. The *query* in the CREATE VIRTUAL TABLE statement for a union\-vtab 
must be a well\-formed SQL query that returns four columns and an 
arbitrary number of rows. Each row in the result of the *query*
represents a single table that is to participate in the union.



	1. The first column is the schema name for the database that contains
	the tables. Examples: "main", "zone512".
	2. The second column is the name of the table.
	3. The third column is the minimum value for any rowid in the table.
	4. The fourth column is the maximum value of any rowid in the table.
7. The *query* for the CREATE VIRTUAL TABLE statement of a union\-vtab
can be either a [SELECT](lang_select.html) statement or a [VALUES clause](lang_select.html#values).
8. The *query* is run once when the CREATE VIRTUAL TABLE statement is
first encountered and the results of that one run are used for all subsequent
access to the union\-vtab. If the results of *query* change, then
the union\-vtab should be [DROP](lang_droptable.html)\-ed and recreated in order
to cause the *query* to be run again.
9. There must be no overlap in the bands of rowids for the various tables
in a union\-vtab.
10. All tables that participate in a union\-vtab must have identical
CREATE TABLE definitions, except that the names of the tables can be different.
11. All tables that participate in a union\-vtab must be [rowid tables](rowidtable.html).
12. The column names and definitions for *tabname* will be the same as
the underlying tables. An application can access *tabname* just like
it was one of the real underlying tables.
13. No table in a union\-vtab may contain entries that are outside of the
rowid bounds established by the *query* in the CREATE VIRTUAL TABLE
statement.
14. The union\-vtab shall optimize access to the underlying real tables
when the constraints on the query are among forms shown below.
Other kinds of constraints may be optimized in the future, but only
these constraints are optimized in the initial implementation.



	* **rowid\=$id**
	* **rowid IN** *query\-or\-list*
	* **rowid BETWEEN $lwr AND $upr**
Other kinds of constraints may be used and will work, but other
constraints will be checked individually for each row and will not
be optimized (at least not initially). 
All constraint checking is completely automatic regardless of whether
or not optimization occurs. The optimization referred to in this bullet point
is a performance consideration only. The same result is obtained
regardless of whether or not the query is optimized.
15. The union\-vtab is read\-only. Support for writing may be added at a later
time, but writing is not a part of the initial implementation.
16. *Nota bene:*
The [sqlite3\_blob\_open()](c3ref/blob_open.html) interface does not work for a union\-vtab.
BLOB content must be read from the union\-vtab using ordinary SQL statements.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


