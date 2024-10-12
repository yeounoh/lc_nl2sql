




sqldiff.exe: Database Difference Utility




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










sqldiff.exe: Database Difference Utility


►
Table Of Contents
[1\. Usage](#usage)
[2\. How It Works](#how_it_works)
[3\. Limitations](#limitations)




# 1\. Usage



The sqldiff.exe binary is a command\-line utility program that
displays content differences between SQLite databases. Example
usage:




```
sqldiff [options] database1.sqlite database2.sqlite

```


The usual output is an SQL script that will transform
database1\.sqlite (the "source" database) into database2\.sqlite
(the "destination" database). This behavior can be
altered using command\-line switches:




**\-\-changeset FILE**
Do not write changes to standard output. Instead, write a (binary)
 changeset file into FILE. The changeset can be interpreted using
 the [session extension](sessionintro.html) to SQLite.


**\-\-lib LIBRARY**
**\-L LIBRARY**
Load the shared library or DLL file LIBRARY into SQLite prior to
 computing the differences. This can be used to add application\-defined
 [collating sequences](datatype3.html#collation) that are required by the schema.


**\-\-primarykey**
Use the schema\-defined [PRIMARY KEY](lang_createtable.html#primkeyconst) instead of the [rowid](lang_createtable.html#rowid) to
 pair rows in the source and destination database. (See additional
 explanation below.)


**\-\-schema**
Show only column name and table differences in the schema,
 not the table content


**\-\-summary**
Show how many rows have changed on each table, but do not show
 the actual changes


**\-\-table TABLE**
Show only the differences in content for TABLE, not for the
 entire database


**\-\-transaction**
Wrap SQL output in a single large transaction


**\-\-vtab**
Add support for handling [FTS3](fts3.html), [FTS5](fts5.html) and [rtree](rtree.html) virtual tables.
 [See below](#sqldiff_vtab) for details.




# 2\. How It Works


The sqldiff.exe utility works by finding rows in the source and
destination that are logical "pairs". The default behavior is to
treat two rows as pairs if they are in tables with the same name
and they have the same [rowid](lang_createtable.html#rowid), or in the case of a [WITHOUT ROWID](withoutrowid.html)
table if they have the same [PRIMARY KEY](lang_createtable.html#primkeyconst). Any differences in the
content of paired rows are output as UPDATEs. Rows in the source
database that could not be paired are output as DELETEs. Rows in
the destination database that could not be paired are output as
INSERTs.



The \-\-primarykey flag changes the pairing algorithm slightly so
that the schema\-declared [PRIMARY KEY](lang_createtable.html#primkeyconst) is always used for pairing,
even on tables that have a [rowid](lang_createtable.html#rowid). This is often a better choice
for finding differences, however it can lead to missed differences in
the case of rows that have one or more PRIMARY KEY columns set to
NULL.


# 3\. Limitations


1. The sqldiff.exe utility does not compute changesets for
either: rowid tables for which the rowid is inaccessible;
or tables which have no explicit primary key.
Given the \-\-changeset option, sqldiff omits them from the comparison.
Examples of such tables are:




```
CREATE TABLE NilChangeset (
   -- inaccessible rowid due to hiding its aliases
   "rowid" TEXT,
   "oid" TEXT,
   "_rowid_" TEXT
);

```


and


```
CREATE TABLE NilChangeset (
   -- no explicit primary key
   "authorId" TEXT,
   "bookId" TEXT
);

```



When sqldiff is made to compare only such tables, no error occurs.
However, the result may be unexpected.
For example, the effect of this invocation:


```
sqldiff --changeset CHANGESET_OUT --table NilChangeset db1.sdb db2.sdb

```


will be to produce an empty file named "CHANGESET\_OUT". See [session limitations](sessionintro.html#limitations) for details.
2. The sqldiff.exe utility does not (currently) display differences in
[TRIGGERs](lang_createtrigger.html) or [VIEWs](lang_createview.html).
3. The sqldiff utility is not designed to support schema migrations
and is forgiving with respect to differing column definitions.
Normally, only the column names and their order are compared
for like\-named tables before content comparison proceeds.



However, the single\-table comparison option, with "sqlite\_schema"
named, can be used to show or detect detailed schema differences
between a pair of databases.
When doing this, the output should not be used directly to modify a database.
4. By default, differences in the schema or content of virtual tables are
not reported on.



However, if a [virtual table](vtab.html) implementation creates real tables (sometimes
referred to as "shadow" tables) within the database to store its data in, then
sqldiff.exe does calculate the difference between these. This can have
surprising effects if the resulting SQL script is then run on a database that
is not *exactly* the same as the source database. For several of SQLite's
bundled virtual tables (FTS3, FTS5, rtree and others), the surprising effects
may include corruption of the virtual table content.



 If the \-\-vtab option is passed to sqldiff.exe, then it ignores all
underlying shadow tables belonging to an FTS3, FTS5 or rtree virtual table
and instead includes the virtual table differences directly.


*This page last modified on [2023\-01\-06 00:45:39](https://sqlite.org/docsrc/honeypot) UTC* 


