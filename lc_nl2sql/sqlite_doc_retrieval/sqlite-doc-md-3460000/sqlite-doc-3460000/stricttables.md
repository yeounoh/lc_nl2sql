




STRICT Tables




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










STRICT Tables


# 1\. Introduction


SQLite strives to be flexible regarding the datatype of
the content that it stores. For example, if a table column has a type of
"INTEGER", then SQLite tries to convert anything inserted into that column
into an integer. So an attempt to insert the string '123' results
in an integer 123 being inserted. But if the content cannot be losslessly
converted into an integer, for example if the input is 'xyz', then
the original string is inserted instead.
See the [Datatypes In SQLite](datatype3.html) document for additional information.



Some developers [appreciate the freedom](flextypegood.html) that SQLite's flexible typing
rules provide and use that freedom to advantage.
But other developers are aghast at SQLite's
flagrant rule\-breaking and prefer the traditional rigid type
system found in all other SQL database engines and in the
SQL standard. For this latter group, SQLite supports a strict typing
mode, as of version 3\.37\.0 (2021\-11\-27\), that is enabled
separately for each table.



# 2\. STRICT Tables


In a [CREATE TABLE](lang_createtable.html) statement, if the "STRICT" table\-option keyword is
added to the end, after the closing ")", then strict typing rules apply
to that table. 
The STRICT keyword causes the following differences:



1. Every column definition must specify a datatype for that column.
The freedom to specify a column without a datatype is removed.
2. The datatype must be one of following:



	* INT
	* INTEGER
	* REAL
	* TEXT
	* BLOB
	* ANYNo other datatype names are allowed, though new types might be added in
future releases of SQLite.
3. Content inserted into the column with a datatype other than ANY
must be either a NULL (assuming there
is no NOT NULL constraint on the column) or the type specified.
SQLite attempts to coerce the data into the appropriate type using the usual
affinity rules, as PostgreSQL, MySQL, SQL Server,
and Oracle all do. If the value cannot be
losslessly converted in the specified datatype, then an
SQLITE\_CONSTRAINT\_DATATYPE error is raised.
4. Columns with datatype ANY can accept any kind of data (except they will
reject NULL values if they have a NOT NULL constraint, of course). No
type coercion occurs for a column of type ANY in a STRICT table.
5. Columns that are part of the PRIMARY KEY are implicitly NOT NULL.
However, even though the PRIMARY KEY has an implicit NOT NULL constraint,
when a NULL value is inserted into an [INTEGER PRIMARY KEY](lang_createtable.html#rowid) column, the
NULL is automatically converted into a unique integer, using the same
rules for [INTEGER PRIMARY KEY](lang_createtable.html#rowid) on ordinary, non\-strict tables.
6. The [PRAGMA integrity\_check](pragma.html#pragma_integrity_check) and [PRAGMA quick\_check](pragma.html#pragma_quick_check) commands check the
type of the content of all columns in STRICT tables and show errors if
anything is amiss.



Everything else about a STRICT table works the same as it does in an
ordinary non\-strict table:



* [CHECK constraints](lang_createtable.html#ckconst) work the same.
* [NOT NULL constraints](lang_createtable.html#notnullconst) work the same.
* [FOREIGN KEY constraints](foreignkeys.html) work the same.
* [UNIQUE constraints](lang_createtable.html#uniqueconst) work the same.
* [DEFAULT clauses](lang_createtable.html#dfltval) work the same.
* [COLLATE clauses](lang_createtable.html#collateclause) work the same.
* [Generated columns](gencol.html) work the same.
* [ON CONFLICT clauses](lang_conflict.html) work the same.
* [Indexes](lang_createindex.html) work the same.
* [AUTOINCREMENT](autoinc.html) works the same.
* An [INTEGER PRIMARY KEY](lang_createtable.html#rowid) column is an alias for the [rowid](lang_createtable.html#rowid), but an
INT PRIMARY KEY column is not.
* The [on\-disk format](fileformat2.html) for the [table data](fileformat2.html##sqltab) is the same.


# 3\. The ANY datatype


The ability to host any type of data in a single column has proven to
be remarkably useful over the years. In order to continue supporting this
ability, even in STRICT tables, the new ANY datatype name is introduced.
When the datatype of a column is "ANY", that means that any kind of data \- 
integers, floating point values, strings, or binary blobs, can be inserted
into that table and its value and datatype will be preserved exactly as
it is inserted. As far as we know, SQLite is the only SQL database engine
that supports this advanced capability.



The behavior of ANY is slightly different in a
STRICT table versus an ordinary non\-strict table. In a STRICT table,
a column of type ANY always preserves the data exactly as it is received.
For an ordinary non\-strict table, a column of type ANY will attempt to
convert strings that look like numbers into a numeric value, and if
successful will store the numeric value rather than the original string.
For example:






| STRICT | ordinary non\-strict |
| --- | --- |
| ``` CREATE TABLE t1(a ANY) STRICT; INSERT INTO t1 VALUES('000123'); SELECT typeof(a), quote(a) FROM t1; -- result: text '000123' ``` | ```  CREATE TABLE t1(a ANY); INSERT INTO t1 VALUES('000123'); SELECT typeof(a), quote(a) FROM t1; -- result: integer 123 ``` |



# 4\. Backwards Compatibility


The STRICT keyword at the end of a CREATE TABLE statement is only
recognized by SQLite version 3\.37\.0 (2021\-11\-27\) and later. If
you try to open a database containing the STRICT keyword in an earlier
version of SQLite, it will not recognize the keyword and will report
an error (except as noted below). But apart from the extra STRICT keyword,
the underlying [file format](fileformat2.html) of the database is identical.



Thus, in general, a database file that contains one or more STRICT
tables can only be read and written by SQLite version 3\.37\.0 or later.
However, a database created by SQLite 3\.37\.0 or later can still be
read and written by earlier versions of SQLite, going all the way back
to version 3\.0\.0 (2004\-06\-18\) as long as the database does not contain
any STRICT tables or other features that were introduced after the older
version of SQLite.



The STRICT keyword may still be used as an identifier.
(It is only treated as a keyword in a certain part of the syntax,
and sqlite3\_keyword\_check(..) does not recognize it as a regular keyword.)



## 4\.1\. Accessing STRICT tables in earlier versions of SQLite


Because of a quirk in the SQL language parser, versions of SQLite prior
to 3\.37\.0 can still read and write STRICT tables if they set
"[PRAGMA writable\_schema\=ON](pragma.html#pragma_writable_schema)" immediately after opening the database
file, prior to doing anything else that requires knowing the schema.
One of the features of PRAGMA writable\_schema\=ON is that it disables
errors in the schema parser. This is intentional, because a big reason for
having PRAGMA writable\_schema\=ON is to facilitate recovery of database files
with corrupt schemas. So with writable\_schema\=ON, when the schema
parser reaches the STRICT keyword, it says to itself "I don't know what
to do with this, but everything up to this point seems like a valid
table definition so I'll just use what I have." Hence, the STRICT
keyword is effectively ignored. Because nothing else about the file
format changes for STRICT tables, everything else will work normally.
Of course, rigid type enforcement will not occur because the earlier
versions of SQLite do not know how to do that.



The [.dump](cli.html#dump) command in the [CLI](cli.html) sets [PRAGMA writable\_schema\=ON](pragma.html#pragma_writable_schema), because
.dump is designed to extract as much content as it can even from a corrupt
database file. Hence, if you are using an older version of SQLite and
you open a database with STRICT tables in the CLI and issue the ".dump"
command before doing anything else, you will be able to read and write
to the STRICT tables without rigid type enforcement. This could, potentially,
corrupt the database, by allowing incorrect types into STRICT tables.
Reopening the database with a newer version of SQLite and running
"[PRAGMA quick\_check](pragma.html#pragma_quick_check)" will detect and report all such corruption.



# 5\. Other Table Options


The SQLite parser accepts a comma\-separated list of table options after
the final close parenthesis in a CREATE TABLE statement. As of this
writing (2021\-08\-23\) only two options are recognized:



* STRICT
* [WITHOUT ROWID](withoutrowid.html)


If there are multiple options, they can be specified in any order.
To keep things simple, the current parser accepts duplicate options without
complaining, but that might change in future releases, so applications
should not rely on it.


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


