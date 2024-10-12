




Clustered Indexes and the WITHOUT ROWID Optimization




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Clustered Indexes and the WITHOUT ROWID Optimization


►
Table Of Contents
[1\. Introduction](#introduction)
[1\.1\. Syntax](#syntax)
[1\.2\. Compatibility](#compatibility)
[1\.3\. Quirks](#quirks)
[2\. Differences From Ordinary Rowid Tables](#differences_from_ordinary_rowid_tables)
[3\. Benefits Of WITHOUT ROWID Tables](#benefits_of_without_rowid_tables)
[4\. When To Use WITHOUT ROWID](#when_to_use_without_rowid)
[5\. Determining If An Existing Table Is WITHOUT ROWID](#determining_if_an_existing_table_is_without_rowid)




# 1\. Introduction


By default, every row in SQLite has a special column, usually called the
"[rowid](lang_createtable.html#rowid)", that uniquely identifies that row within the table. However
if the phrase "WITHOUT ROWID" is added to the end of a [CREATE TABLE](lang_createtable.html) statement,
then the special "rowid" column is omitted. There are sometimes
space and performance advantages to omitting the rowid.


A WITHOUT ROWID table is a table that uses a
[Clustered Index](https://en.wikipedia.org/wiki/Database_index#Clustered)
as the primary key.


## 1\.1\. Syntax


To create a WITHOUT ROWID table, simply add the keywords "WITHOUT ROWID"
to the end of the [CREATE TABLE](lang_createtable.html) statement. For example:



> ```
> 
> CREATE TABLE IF NOT EXISTS wordcount(
>   word TEXT PRIMARY KEY,
>   cnt INTEGER
> ) WITHOUT ROWID;
> 
> ```


As with all SQL syntax, the case of the keywords does not matter.
One can write "WITHOUT rowid" or "without rowid" or "WiThOuT rOwId" and
it will mean the same thing.


Every WITHOUT ROWID table must have a [PRIMARY KEY](lang_createtable.html#primkeyconst). An error is raised
if a CREATE TABLE statement with the WITHOUT ROWID clause lacks a PRIMARY KEY.



In most contexts, the special "rowid" column of normal tables can
also be called "oid" or "\_rowid\_". However, only "rowid" works as
the keyword in the CREATE TABLE statement.


## 1\.2\. Compatibility


SQLite [version 3\.8\.2](releaselog/3_8_2.html) (2013\-12\-06\) or later
is necessary in order to use a WITHOUT
ROWID table. An attempt to open a database that contains one or more WITHOUT
ROWID tables using an earlier version of SQLite will result in a
"malformed database schema" error.


## 1\.3\. Quirks


WITHOUT ROWID is found only in SQLite and is not compatible
with any other SQL database engine, as far as we know.
In an elegant system, all tables would behave as WITHOUT ROWID
tables even without the WITHOUT ROWID keyword. However, when SQLite was
first designed, it used only integer [rowids](lang_createtable.html#rowid) for row keys
to simplify the implementation.
This approach worked well for many years. But as the demands on
SQLite grew, the need for tables in which the PRIMARY KEY really did
correspond to the underlying row key grew more acute. The WITHOUT ROWID
concept was added
in order to meet that need without breaking backwards
compatibility with the billions of SQLite databases already in use at
the time (circa 2013\).



# 2\. Differences From Ordinary Rowid Tables


The WITHOUT ROWID syntax is an optimization. It provides no new
capabilities. Anything that can be done using a WITHOUT ROWID table
can also be done in exactly the same way, and exactly the same syntax,
using an ordinary rowid table. The only advantage of a WITHOUT ROWID
table is that it can sometimes use less disk space and/or perform a little
faster than an ordinary rowid table.


For the most part, ordinary rowid tables and WITHOUT ROWID tables
are interchangeable. But there are some additional restrictions on
WITHOUT ROWID tables that do not apply to ordinary rowid tables:


1. **Every WITHOUT ROWID table must have a PRIMARY KEY.**
An attempt to create a WITHOUT ROWID table without a PRIMARY KEY results
in an error.
2. **The special behaviors associated "[INTEGER PRIMARY KEY](lang_createtable.html#rowid)" do not apply
on WITHOUT ROWID tables.**
In an ordinary table, "INTEGER PRIMARY KEY" means that the column is an
alias for the rowid. But since there is no rowid in a WITHOUT ROWID
table, that special meaning no longer applies. An "INTEGER PRIMARY KEY"
column in a WITHOUT ROWID table works
like an "INT PRIMARY KEY" column in an ordinary table: It is a PRIMARY KEY
that has integer [affinity](datatype3.html#affinity).
3. **[AUTOINCREMENT](autoinc.html) does not work on WITHOUT ROWID tables.**
The [AUTOINCREMENT](autoinc.html) mechanism assumes the presence of a rowid and so it
does not work on a WITHOUT ROWID table. An error is raised if the
 "AUTOINCREMENT" keyword is used in the CREATE TABLE statement for
a WITHOUT ROWID table.
4. **NOT NULL is enforced on every column of the PRIMARY KEY in a WITHOUT
ROWID table.**
This is in accordance with the SQL standard. Each column of a PRIMARY KEY
is supposed to be individually NOT NULL. However, NOT NULL was not enforced
on PRIMARY KEY columns by early versions of SQLite due to a bug. By the
time that this bug was discovered, so many SQLite databases were already
in circulation that the decision was made not to fix this bug for fear of
breaking compatibility. So, ordinary rowid tables in SQLite violate the
SQL standard and allow NULL values in PRIMARY KEY fields. But WITHOUT ROWID
tables do follow the standard and will throw an error on any attempt to
insert a NULL into a PRIMARY KEY column.
5. **The [sqlite3\_last\_insert\_rowid()](c3ref/last_insert_rowid.html) function
does not work for WITHOUT ROWID tables.**
Inserts into a WITHOUT ROWID do not change the value returned by the
[sqlite3\_last\_insert\_rowid()](c3ref/last_insert_rowid.html) function. The [last\_insert\_rowid()](lang_corefunc.html#last_insert_rowid) SQL
function is also unaffected since it is just a wrapper around
[sqlite3\_last\_insert\_rowid()](c3ref/last_insert_rowid.html).
6. **The [incremental blob I/O](c3ref/blob_open.html) mechanism does not work
for WITHOUT ROWID tables.**
Incremental BLOB I/O uses the rowid to create an [sqlite3\_blob](c3ref/blob.html) object for
doing the direct I/O. However, WITHOUT ROWID tables do not have a rowid,
and so there is no way to create an [sqlite3\_blob](c3ref/blob.html) object for a WITHOUT
ROWID table.
7. **The [sqlite3\_update\_hook()](c3ref/update_hook.html) interface does not fire callbacks for changes
to a WITHOUT ROWID table.**
Part of the callback from [sqlite3\_update\_hook()](c3ref/update_hook.html) is the rowid of the table
row that has changed. However, WITHOUT ROWID tables do not have a rowid.
Hence, the update hook is not invoked when a WITHOUT ROWID table changes.



# 3\. Benefits Of WITHOUT ROWID Tables


A WITHOUT ROWID table is an optimization that can reduce storage and
processing requirements.



In an ordinary SQLite table, the PRIMARY KEY is really just a
[UNIQUE](lang_createtable.html#uniqueconst) index. The key used to look up records on disk
is the [rowid](lang_createtable.html#rowid).
The special "[INTEGER PRIMARY KEY](lang_createtable.html#rowid)" column type in ordinary SQLite tables
causes the column to be an alias for the rowid, and so an INTEGER PRIMARY
KEY is a true PRIMARY KEY. But any other kind of PRIMARY KEYs, including
"INT PRIMARY KEY" are just unique indexes in an ordinary rowid table.


Consider a table (shown below) intended to store a
vocabulary of words together with a count of the number of occurrences of
each word in some text corpus:




> ```
> 
> CREATE TABLE IF NOT EXISTS wordcount(
>   word TEXT PRIMARY KEY,
>   cnt INTEGER
> );
> 
> ```


As an ordinary SQLite table, "wordcount" is implemented as two
separate B\-Trees. The main table uses the hidden rowid value as the key
and stores the "word" and "cnt" columns as data. The "TEXT PRIMARY KEY"
phrase of the CREATE TABLE statement
causes the creation of an [unique index](lang_createindex.html#uniqueidx) on the "word" column. This index is a
separate B\-Tree that uses "word" and the "rowid" as the key and stores no
data at all. Note that the complete text of every "word" is stored twice:
once in the main table and again in the index.



Consider querying this table to find the number of occurrences of the
word "xsync".:




> ```
> 
> SELECT cnt FROM wordcount WHERE word='xsync';
> 
> ```


This query first has to search the index B\-Tree looking for any entry
that contains the matching value for "word". When an entry is found in
the index, the rowid is extracted and used to search the main table.
Then the "cnt" value is read out of the main table and returned. Hence, two
separate binary searches are required to fulfill the request.



A WITHOUT ROWID table uses a different data design for the equivalent
table.




> ```
> 
> CREATE TABLE IF NOT EXISTS wordcount(
>   word TEXT PRIMARY KEY,
>   cnt INTEGER
> ) WITHOUT ROWID;
> 
> ```


In this latter table, there is only a single B\-Tree which uses the "word"
column as its key and the "cnt" column as its data. (Technicality: the
low\-level implementation actually stores both "word" and "cnt" in the "key"
area of the B\-Tree. But unless you are looking at the low\-level byte encoding
of the database file, that fact is unimportant.) Because there is only
a single B\-Tree, the text of the "word" column is only stored once in the
database. Furthermore, querying the "cnt" value for a specific "word"
only involves a single binary search into the main B\-Tree, since the "cnt"
value can be retrieved directly from the record found by that first search
and without the need to do a second binary search on the rowid.



Thus, in some cases, a WITHOUT ROWID table can use about half the amount
of disk space and can operate nearly twice as fast. Of course, in a
real\-world schema, there will typically be secondary indices and/or
UNIQUE constraints, and the situation is more complicated. But even then,
there can often be space and performance advantages to using WITHOUT ROWID
on tables that have non\-integer or composite PRIMARY KEYs.




# 4\. When To Use WITHOUT ROWID


The WITHOUT ROWID optimization is likely to be helpful for tables
that have non\-integer or composite (multi\-column) PRIMARY KEYs and that do
not store large strings or BLOBs.


WITHOUT ROWID tables will work correctly (that is to say, they
provide the correct answer) for tables with a single INTEGER PRIMARY KEY.
However, ordinary rowid tables will run faster in that case.
Hence, it is good design
to avoid creating WITHOUT ROWID tables with single\-column PRIMARY KEYs
of type INTEGER.



WITHOUT ROWID tables work best when individual rows are not too large.
A good rule\-of\-thumb is that the average size of a single row in a
WITHOUT ROWID table should be less than about 1/20th the size of
a database page. That means that rows should not contain more than about
50 bytes each for a 1KiB page size or about 200 bytes each for 4KiB
page size. WITHOUT ROWID tables will work (in the sense that
they get the correct answer) for arbitrarily large rows \- up to 2GB in size \-
but traditional rowid tables tend to work faster for large row sizes.
This is because rowid tables are implemented as [B\*\-Trees](fileformat2.html#btree) where
all content is stored in the leaves of the tree, whereas WITHOUT ROWID
tables are implemented using ordinary B\-Trees with content stored on both
leaves and intermediate nodes. Storing content in
intermediate nodes causes each intermediate node entry to take up more
space on the page and thus reduces the fan\-out, increasing the search cost.



The "sqlite3\_analyzer.exe" utility program, available as source code
in the SQLite source tree or as a precompiled binary on the
[SQLite Download page](https://www.sqlite.org/download.html), can be
used to measure the average sizes of table rows in an existing SQLite
database.


Note that except for a few corner\-case differences detailed above,
WITHOUT ROWID tables and rowid tables work the same. They both generate
the same answers given the same SQL statements. So it is a simple matter
to run experiments on an application, late in the development cycle,
to test whether or not the use of WITHOUT ROWID tables will be helpful.
A good strategy is to simply not worry about WITHOUT ROWID until near
the end of product development, then go back and run tests to see
if adding WITHOUT ROWID to tables with non\-integer PRIMARY KEYs helps
or hurts performance, and retaining the WITHOUT ROWID only in those cases
where it helps.



# 5\. Determining If An Existing Table Is WITHOUT ROWID


A WITHOUT ROWID table returns the same content for
[PRAGMA table\_info](pragma.html#pragma_table_info) and [PRAGMA table\_xinfo](pragma.html#pragma_table_xinfo) as does an ordinary
table. But unlike an ordinary table, a WITHOUT ROWID also
responds to the [PRAGMA index\_info](pragma.html#pragma_index_info) command. The [PRAGMA index\_info](pragma.html#pragma_index_info)
on a WITHOUT ROWID table returns information about the PRIMARY KEY
for the table. In this way, the [PRAGMA index\_info](pragma.html#pragma_index_info) command can be
used to unambiguously determine whether a particular table is a
WITHOUT ROWID table or an ordinary table \- an ordinary table will
always return no rows but a WITHOUT ROWID table will always return
one or more rows.



