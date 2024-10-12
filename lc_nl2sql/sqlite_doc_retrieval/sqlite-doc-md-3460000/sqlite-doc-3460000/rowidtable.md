




Rowid Tables




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# Rowid Tables


## 1\.0 Definition


A "rowid table" is any table in an SQLite schema that
* is *not* a [virtual table](vtab.html), and
* is *not* a [WITHOUT ROWID](withoutrowid.html) table.


Most tables in a typical SQLite database schema are rowid tables.

Rowid tables are distinguished by the fact that they all have
a unique, non\-NULL, signed 64\-bit integer [rowid](lang_createtable.html#rowid) that is used as
the access key for the data in the underlying [B\-tree](fileformat2.html#btree) storage engine.

## 2\.0 Quirks


* The [PRIMARY KEY](lang_createtable.html#primkeyconst) of a rowid table (if there is one) is usually not the
true primary key for the table, in the sense that it is not the unique
key used by the underlying [B\-tree](fileformat2.html#btree) storage engine. The exception to
this rule is when the rowid table declares an [INTEGER PRIMARY KEY](lang_createtable.html#rowid).
In the exception, the INTEGER PRIMARY KEY becomes an alias for the 
[rowid](lang_createtable.html#rowid).

* The true primary key for a rowid table (the value that is used as the
key to look up rows in the underlying [B\-tree](fileformat2.html#btree) storage engine)
is the [rowid](lang_createtable.html#rowid).

* The PRIMARY KEY constraint for a rowid table (as long as it is not
the true primary key or INTEGER PRIMARY KEY) is really the same thing
as a [UNIQUE constraint](lang_createtable.html#uniqueconst). Because it is not a true primary key,
columns of the PRIMARY KEY are allowed to be NULL, in violation of
all SQL standards.

* The [rowid](lang_createtable.html#rowid) of a rowid table can be accessed (or changed) by reading or
writing to any of the "rowid" or "oid" or "\_rowid\_" columns. Except,
if there is a declared columns in the table that use those
special names, then those names refer to the declared columns, not to
the underlying [rowid](lang_createtable.html#rowid).

* Access to records via [rowid](lang_createtable.html#rowid) is highly optimized and very fast.

* If the [rowid](lang_createtable.html#rowid) is not aliased by [INTEGER PRIMARY KEY](lang_createtable.html#rowid) then it is not
persistent and might change. In particular the [VACUUM](lang_vacuum.html) command will
change rowids for tables that do not declare an INTEGER PRIMARY KEY.
Therefore, applications should not normally access the rowid directly,
but instead use an INTEGER PRIMARY KEY.

* In the underlying [file format](fileformat2.html), each rowid is stored as a
[variable\-length integer](fileformat2.html#varint). That means that small non\-negative
rowid values take up less disk space than large or negative
rowid values.

* All of the complications above (and others not mentioned here)
arise from the need to preserve backwards
compatibility for the hundreds of billions of SQLite database files in
circulation. In a perfect world, there would be no such thing as a "rowid"
and all tables would following the standard semantics implemented as
[WITHOUT ROWID](withoutrowid.html) tables, only without the extra "WITHOUT ROWID" keywords.
Unfortunately, life is messy. The designer of SQLite offers his
sincere apology for the current mess.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 






