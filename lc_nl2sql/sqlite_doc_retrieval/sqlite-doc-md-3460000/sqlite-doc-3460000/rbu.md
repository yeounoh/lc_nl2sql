




The RBU Extension




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The RBU Extension


►
Table Of Contents
[1\. The RBU Extension](#the_rbu_extension)
[2\. RBU Updates](#rbu_updates)
[2\.1\. RBU Update Limitations](#rbu_update_limitations)
[2\.2\. Preparing an RBU Update File](#preparing_an_rbu_update_file)
[2\.2\.1\. The RBU Database Schema](#the_rbu_database_schema)
[2\.2\.2\. RBU Database Contents](#rbu_database_contents)
[2\.2\.3\. Using RBU with FTS3/4 Tables](#using_rbu_with_fts3_4_tables)
[2\.2\.4\. Automatically Generating RBU Updates with sqldiff](#automatically_generating_rbu_updates_with_sqldiff)
[2\.3\. RBU Update C/C\+\+ Programming](#rbu_update_c_c_programming)
[3\. RBU Vacuum](#rbu_vacuum)
[3\.1\. RBU Vacuum Limitations](#rbu_vacuum_limitations)
[3\.2\. RBU Vacuum C/C\+\+ Programming](#rbu_vacuum_c_c_programming)




# 1\. The RBU Extension


The RBU extension is an add\-on for SQLite designed for use with large 
SQLite database files on low\-power devices at the edge of a network. RBU
may be used for two separate tasks:



* **RBU Update operations**. An [RBU Update](rbu.html#rbu_updates) is a bulk update of a
 database file that may include many insert, update and delete
 operations on one or more tables.
* **RBU Vacuum operations**. An [RBU Vacuum](rbu.html#rbu_vacuum) optimizes and rebuilds an
 entire database file, with results similar to SQLite's native VACUUM
 command.


The acronym RBU stands for "Resumable Bulk Update".



Both of the RBU functions may be accomplished using SQLite's built\-in 
SQL commands \- RBU update via a series of [INSERT](lang_insert.html), [DELETE](lang_delete.html) and 
[UPDATE](lang_update.html) commands within a single transaction, and RBU vacuum by a single
[VACUUM](lang_vacuum.html) command. The RBU module provides the following advantages over
these simpler approaches:




1. **RBU may be more efficient**
The most efficient way to apply changes to a B\-Tree (the data structure
that SQLite uses to store each table and index on disk) is to make the
changes in key order. But if an SQL table has one or more indexes, the key
order for each index may be different from the main table and the other
auxiliary indexes. As a result, when executing a series of [INSERT](lang_insert.html),
[UPDATE](lang_update.html) and [DELETE](lang_delete.html) statements it is not generally possible to order the
operations so that all b\-trees are updated in key order. The RBU update
process works around this by applying all changes to the main table in one 
pass, then applying changes to each index in separate passes, ensuring each
B\-Tree is updated optimally. For a large database file (one that does not
fit in the OS disk cache) this procedure can result in two orders of
magnitude faster updates.



An RBU Vacuum operation requires less temporary disk space and writes
less data to disk than an SQLite VACUUM. An SQLite VACUUM requires roughly
twice the size of the final database file in temporary disk space to run.
The total amount of data written is around three times the size of the
final database file. By contrast, an RBU Vacuum requires roughly the size
of the final database file in temporary disk space and writes a total of
twice that to disk.



On the other hand, an RBU Vacuum uses more CPU than a regular SQLite
VACUUM \- in one test as much as five times as much. For this reason, an RBU
Vacuum is often significantly slower than an SQLite VACUUM under the same
conditions.
2. **RBU runs in the background**
An ongoing RBU operation (either an update or a vacuum) does not
interfere with read access to the database file.
3. **RBU runs incrementally**
RBU operations may be suspended and then later resumed, perhaps with
intervening power outages and/or system resets. For an RBU update, the
original database content remains visible to all database readers until 
the entire update has been applied \- even if the update is suspended and
then later resumed.


The RBU extension is not enabled by default. To enable it, compile the
[amalgamation](amalgamation.html) with the [SQLITE\_ENABLE\_RBU](compile.html#enable_rbu) compile\-time option.




# 2\. RBU Updates


## 2\.1\. RBU Update Limitations


The following limitations apply to RBU updates:



* The changes must consist of [INSERT](lang_insert.html), [UPDATE](lang_update.html), and [DELETE](lang_delete.html)
 operations only. CREATE and DROP operations are not
 supported.
* [INSERT](lang_insert.html) statements may not use default values.
* [UPDATE](lang_update.html) and [DELETE](lang_delete.html) statements must identify the target rows
 by rowid or by non\-NULL PRIMARY KEY values.
* [UPDATE](lang_update.html) statements may not modify PRIMARY KEY or rowid values.
* RBU updates cannot be applied to any tables that contain a column
 named "rbu\_control".
* The RBU update will not fire any triggers.
* The RBU update will not detect or prevent foreign key or
 CHECK constraint violations.
* All RBU updates use the "OR ROLLBACK" constraint handling mechanism.
* The target database may not be in [WAL mode](wal.html).
* ~~The target database may not contain [indexes on expressions](expridx.html).~~
 Indexes on expressions are supported beginning with SQLite 3\.30\.0
 (2019\-10\-04\).
* No other writes may occur on the target database while the
 RBU update is being applied. A read\-lock is held on the target
 database to prevent this.


## 2\.2\. Preparing an RBU Update File


All changes to be applied by RBU are stored in a separate SQLite database
called the "RBU database". The database that is to be modified is called
the "target database".



For each table in the target database that will be modified by the update,
a corresponding table is created within the RBU database. The RBU database
table schema is not the same as that of the target database, but is derived
from it as [described below](rbu.html#database_tables).



The RBU database table contains a single row for each target database 
row inserted, updated or deleted by the update. Populating the RBU database
tables is described in [the following section](rbu.html#database_contents).




### 2\.2\.1\. The RBU Database Schema



For each table in the target database, the RBU database should contain a table
named "data\<*integer*\>\_\<*target\-table\-name*\>" where
\<*target\-table\-name*\> is the name of the table in the target
database and \<*integer*\> is any sequence of zero or more numeric
characters (0\-9\). Tables within the RBU database are processed in order by 
name (from smallest to largest according to the BINARY collation sequence),
so the order in which target tables are updated is influenced by the selection 
of the \<*integer*\> portion of the data\_% table name. While this can
be useful when using RBU to update 
[certain types of virtual tables](rbu.html#fts4_tables), there is normally no
reason to use anything other than an empty string in place of
\<*integer*\>.



The data\_% table must have all the same columns as the target table, plus
one additional column named "rbu\_control". The data\_% table should have no
PRIMARY KEY or UNIQUE constraints, but each column should have the same type as
the corresponding column in the target database. The rbu\_control column should
have no type at all. For example, if the target database contains:




```
CREATE TABLE t1(a INTEGER PRIMARY KEY, b TEXT, c UNIQUE);

```

Then the RBU database should contain:




```
CREATE TABLE data_t1(a INTEGER, b TEXT, c, rbu_control);

```

The order of the columns in the data\_% table does not matter.



If the target database table is a virtual table or a table that has no
PRIMARY KEY declaration, the data\_% table must also contain a column 
named "rbu\_rowid". The rbu\_rowid column is mapped to the tables [ROWID](lang_createtable.html#rowid).
For example, if the target database contains either of the following:




```
CREATE VIRTUAL TABLE x1 USING fts3(a, b);
CREATE TABLE x1(a, b);

```

then the RBU database should contain:




```
CREATE TABLE data_x1(a, b, rbu_rowid, rbu_control);

```

Virtual tables for which the "rowid" column does 
not function like a primary key value cannot be updated using RBU.




All non\-hidden columns (i.e. all columns matched by "SELECT \*") of the
target table must be present in the input table. For virtual tables,
hidden columns are optional \- they are updated by RBU if present in
the input table, or not otherwise. For example, to write to an fts4
table with a hidden languageid column such as:




```
CREATE VIRTUAL TABLE ft1 USING fts4(a, b, languageid='langid');

```

Either of the following input table schemas may be used:




```
CREATE TABLE data_ft1(a, b, langid, rbu_rowid, rbu_control);
CREATE TABLE data_ft1(a, b, rbu_rowid, rbu_control);

```


### 2\.2\.2\. RBU Database Contents


For each row to INSERT into the target database as part of the RBU 
update, the corresponding data\_% table should contain a single record
with the "rbu\_control" column set to contain integer value 0\. The
other columns should be set to the values that make up the new record 
to insert. 



The "rbu\_control" column may also be set to integer value 2 for 
an INSERT. In this case, the new row silently replaces any existing row that
has the same primary key values. This is equivalent to a DELETE followed by an
INSERT with the same primary key values. It is not the same as an SQL REPLACE
command, as in that case the new row may replace any conflicting rows (i.e.
those that conflict due to UNIQUE constraints or indexes), not just those with
conflicting primary keys.



If the target database table has an INTEGER PRIMARY KEY, it is not 
possible to insert a NULL value into the IPK column. Attempting to 
do so results in an SQLITE\_MISMATCH error.



For each row to DELETE from the target database as part of the RBU 
update, the corresponding data\_% table should contain a single record
with the "rbu\_control" column set to contain integer value 1\. The
real primary key values of the row to delete should be stored in the
corresponding columns of the data\_% table. The values stored in the
other columns are not used.



For each row to UPDATE from the target database as part of the RBU 
update, the corresponding data\_% table should contain a single record
with the "rbu\_control" column set to contain a value of type text.
The real primary key values identifying the row to update should be 
stored in the corresponding columns of the data\_% table row, as should
the new values of all columns being update. The text value in the 
"rbu\_control" column must contain the same number of characters as
there are columns in the target database table, and must consist entirely
of 'x' and '.' characters (or in some special cases 'd' \- see below). For 
each column that is being updated, the corresponding character is set to
'x'. For those that remain as they are, the corresponding character of the
rbu\_control value should be set to '.'. For example, given the tables 
above, the update statement:




```
UPDATE t1 SET c = 'usa' WHERE a = 4;

```

is represented by the data\_t1 row created by:




```
INSERT INTO data_t1(a, b, c, rbu_control) VALUES(4, NULL, 'usa', '..x');

```

If RBU is used to update a large BLOB value within a target database, it
may be more efficient to store a patch or delta that can be used to modify
the existing BLOB instead of an entirely new value within the RBU database. 
RBU allows deltas to be specified in two ways:



* In the "fossil delta" format \- the format used for blob deltas by the 
 [Fossil source\-code management system](http://fossil-scm.org), or
* In a custom format defined by the RBU application.


 The fossil delta format may only be used to update BLOB values. Instead
of storing the new BLOB within the data\_% table, the fossil delta is stored
instead. And instead of specifying an 'x' as part of the rbu\_control string
for the column to be updated, an 'f' character is stored. When processing
an 'f' update, RBU loads the original BLOB data from disk, applies the fossil
delta to it and stores the results back into the database file. The RBU
databases generated by [sqldiff \-\-rbu](rbu.html#sqldiff) make use of fossil deltas wherever
doing so would save space in the RBU database.



 To use a custom delta format, the RBU application must register a
user\-defined SQL function named "rbu\_delta" before beginning to process the
update. rbu\_delta() will be invoked with two arguments \- the original value
stored in the target table column and the delta value provided as part of
the RBU update. It should return the result of applying the delta to the
original value. To use the custom delta function, the character of the
rbu\_control value corresponding to the target column to update must be
set to 'd' instead of 'x'. Then, instead of updating the target table with the
value stored in the corresponding data\_% column, RBU invokes the user\-defined
SQL function "rbu\_delta()" and the store in the target table column.



For example, this row:




```
INSERT INTO data_t1(a, b, c, rbu_control) VALUES(4, NULL, 'usa', '..d');

```

causes RBU to update the target database table in a way similar to:




```
UPDATE t1 SET c = rbu_delta(c, 'usa') WHERE a = 4;

```

If the target database table is a virtual table or a table with no PRIMARY
KEY, the rbu\_control value should not include a character corresponding 
to the rbu\_rowid value. For example, this:




```
INSERT INTO data_ft1(a, b, rbu_rowid, rbu_control) 
  VALUES(NULL, 'usa', 12, '.x');

```

causes a result similar to:




```
UPDATE ft1 SET b = 'usa' WHERE rowid = 12;

```

The data\_% tables themselves should have no PRIMARY KEY declarations.
However, RBU is more efficient if reading the rows in from each data\_%
table in "rowid" order is roughly the same as reading them sorted by
the PRIMARY KEY of the corresponding target database table. In other 
words, rows should be sorted using the destination table PRIMARY KEY 
fields before they are inserted into the data\_% tables.




### 2\.2\.3\. Using RBU with FTS3/4 Tables


Usually, an [FTS3 or FTS4](fts3.html) table is an example of a virtual table 
with a rowid that works like a PRIMARY KEY. So, for the following FTS4 tables:




```
CREATE VIRTUAL TABLE ft1 USING fts4(addr, text);
CREATE VIRTUAL TABLE ft2 USING fts4;             -- implicit "content" column

```

The data\_% tables may be created as follows:




```
CREATE TABLE data_ft1 USING fts4(addr, text, rbu_rowid, rbu_control);
CREATE TABLE data_ft2 USING fts4(content, rbu_rowid, rbu_control);

```

And populated as if the target table were an ordinary SQLite table with no
explicit PRIMARY KEY columns.



[Contentless FTS4 tables](fts3.html#_contentless_fts4_tables_) are handled similarly,
except that any attempt to update or delete rows will cause an error when
applying the update.



[External content FTS4 tables](fts3.html#_external_content_fts4_tables_) may also be 
updated using RBU. In this case the user is required to configure the RBU
database so that the same set of UPDATE, DELETE and INSERT operations are
applied to the FTS4 index as to the underlying content table. As for all
updates of external content FTS4 tables, the user is also required to ensure
that any UPDATE or DELETE operations are applied to the FTS4 index before
they are applied to the underlying content table (refer to FTS4 documentation
for a detailed explanation). In RBU, this is done by ensuring that the name
of the data\_% table used to write to the FTS4 table sorts before the name
of the data\_% table used to update the underlying content table using the
[BINARY](datatype3.html#collation) collation sequence. In order to avoid duplicating data within the
RBU database, an SQL view may be used in place of one of the data\_% tables.
For example, for the target database schema:




```
CREATE TABLE ccc(addr, text);
CREATE VIRTUAL TABLE ccc_fts USING fts4(addr, text, content=ccc);

```


 The following RBU database schema may be used: 




```
CREATE TABLE data_ccc(addr, text, rbu_rowid, rbu_control);
CREATE VIEW data0_ccc_fts AS SELECT * FROM data_ccc;

```


 The data\_ccc table may then be populated as normal with the updates intended
 for target database table ccc. The same updates will be read by RBU from
 the data0\_ccc\_fts view and applied to FTS table ccc\_fts. Because
 "data0\_ccc\_fts" is smaller than "data\_ccc", the FTS table will be updated
 first, as required.




 Cases in which the underlying content table has an explicit INTEGER PRIMARY
 KEY column are slightly more difficult, as the text values stored in the
 rbu\_control column are slightly different for the FTS index and its
 underlying content table. For the underlying content table, a character
 must be included in any rbu\_control text values for the explicit IPK, but
 for the FTS table itself, which has an implicit rowid, it should not. This
 is inconvenient, but can be solved using a more complicated view, as follows:




```
-- Target database schema
CREATE TABLE ddd(i INTEGER PRIMARY KEY, k TEXT);
CREATE VIRTUAL TABLE ddd_fts USING fts4(k, content=ddd);

-- RBU database schema
CREATE TABLE data_ccc(i, k, rbu_control);
CREATE VIEW data0_ccc_fts AS SELECT i AS rbu_rowid, k, CASE 
  WHEN rbu_control IN (0,1) THEN rbu_control ELSE substr(rbu_control, 2) END
FROM data_ccc;

```


 The substr() function in the SQL view above returns the text of the
 rbu\_control argument with the first character (the one corresponding to
 column "i", which is not required by the FTS table) removed.




### 2\.2\.4\. Automatically Generating RBU Updates with sqldiff



 As of SQLite [version 3\.9\.0](releaselog/3_9_0.html) (2015\-10\-14\), 
 the [sqldiff](sqldiff.html) utility is able to generate
 RBU databases representing the difference between two databases with
 identical schemas. For example, the following command:




```
sqldiff --rbu t1.db t2.db

```


 Outputs an SQL script to create an RBU database which, if used to update
 database t1\.db, patches it so that its contents are identical to that of
 database t2\.db.




 By default, sqldiff attempts to process all non\-virtual tables within
 the two databases provided to it. If any table appears in one database
 but not the other, or if any table has a slightly different schema in
 one database it is an error. The "\-\-table" option may be useful if this
 causes a problem
 



 Virtual tables are ignored by default by sqldiff. However, it is possible 
 to explicitly create an RBU data\_% table for a virtual table that features
 a rowid that functions like a primary key using a command such as:




```
sqldiff --rbu --table <virtual-table-name> t1.db t2.db

```


 Unfortunately, even though virtual tables are ignored by default, any
 [underlying database tables](fts3.html#*shadowtab) that they create in order to
 store data within the database are not, and [sqldiff](sqldiff.html) will include add these
 to any RBU database. For this reason, users attempting to use sqldiff to
 create RBU updates to apply to target databases with one or more virtual
 tables will likely have to run sqldiff using the \-\-table option separately
 for each table to update in the target database.



## 2\.3\. RBU Update C/C\+\+ Programming


The RBU extension interface allows an application to apply an RBU update 
stored in an RBU database to an existing target database.
The procedure is as follows:



1. Open an RBU handle using the sqlite3rbu\_open(T,A,S) function.



The T argument is the name of the target database file.
The A argument is the name of the RBU database file.
The S argument is the name of a "state database" used to store
state information needed to resume the update after an interruption.
The S argument can be NULL in which case the state information
is stored in the RBU database in various tables whose names all
begin with "rbu\_".



The sqlite3rbu\_open(T,A,S) function returns a pointer to
an "sqlite3rbu" object, which is then passed into the subsequent
interfaces.
2. Register any required virtual table modules with the database
handle returned by sqlite3rbu\_db(X) (where argument X is the sqlite3rbu
pointer returned from sqlite3rbu\_open()). Also, if required, register
the rbu\_delta() SQL function using 
[sqlite3\_create\_function\_v2()](c3ref/create_function.html).
3. Invoke the sqlite3rbu\_step(X) function one or more times on
the sqlite3rbu object pointer X. Each call to sqlite3rbu\_step() 
performs a single b\-tree operation, so thousands of calls may be 
required to apply a complete update. The sqlite3rbu\_step() 
interface will return SQLITE\_DONE when the update has been
completely applied.
4. Call sqlite3rbu\_close(X) to destroy the sqlite3rbu object pointer.
If sqlite3rbu\_step(X) has been called enough times to completely
apply the update to the target database, then the RBU database
is marked as fully applied. Otherwise, the state of the RBU 
update application is saved in the state database (or in the RBU
database if the name of the state database file in sqlite3rbu\_open()
is NULL) for later resumption of the update.


If an update is only partially applied to the target database by the
time sqlite3rbu\_close() is called, state information is saved 
within the state database if it exists, or otherwise in the RBU database. 
This allows subsequent processes to automatically
resume the RBU update from where it left off.
If state information is stored in the RBU database, it can be removed
by dropping all tables whose names begin with "rbu\_".



For more details, refer to the comments in 
[header file
sqlite3rbu.h](http://sqlite.org/src/doc/trunk/ext/rbu/sqlite3rbu.h).




# 3\. RBU Vacuum


## 3\.1\. RBU Vacuum Limitations


When compared with SQLite's built\-in VACUUM command, RBU Vacuum has the
following limitations:



* It may not be used on a database that contains [indexes on expressions](expridx.html).
* The database being vacuumed may not be in [WAL mode](wal.html).


## 3\.2\. RBU Vacuum C/C\+\+ Programming


 This section provides an overview of and example code demonstrating the
 integration of RBU Vacuum into an application program. For full details,
 refer to the comments in 
 [header file
 sqlite3rbu.h](http://sqlite.org/src/doc/trunk/ext/rbu/sqlite3rbu.h).



 RBU Vacuum applications all implement some variation of the following
procedure:



1. An RBU handle is created by calling sqlite3rbu\_vacuum(T, S).

 

 Argument T is the name of the database file to vacuum. Argument S is
 the name of a database in which the RBU module will save its state if the
 vacuum operation is suspended.

 

 If state database S does not exist when sqlite3rbu\_vacuum() is
 invoked, it is automatically created and populated with the single table
 used to store the state of an RBU vacuum \- "rbu\_state". If an ongoing RBU
 vacuum is suspended, this table is populated with state data. The next
 time sqlite3rbu\_vacuum() is called with the same S parameter, it detects
 this data and attempts to resume the suspended vacuum operation. When
 an RBU vacuum operation is completed or encounters an error, RBU 
 automatically deletes the contents of the rbu\_state table. In this case,
 the next call to sqlite3rbu\_vacuum() starts an entirely new vacuum
 operation from scratch.

 

 It is a good idea to establish a convention for determining the RBU
 vacuum state database name based on the target database name. The
 example code below uses "\<target\>\-vacuum", where \<target\> is
 the name of the database being vacuumed.
2. Any custom collation sequences used by indexes within the database
 being vacuumed are registered with both of the database handles returned
 by the sqlite3rbu\_db() function.
3. Function sqlite3rbu\_step() is called on the RBU handle until either
 the RBU vacuum is finished, an error occurs or the application wishes to
 suspend the RBU vacuum.

 

 Each call to sqlite3rbu\_step() does a small amount of work towards
 completing the vacuum operation. Depending on the size of the database, a
 single vacuum may require thousands of calls to sqlite3rbu\_step().
 sqlite3rbu\_step() returns SQLITE\_DONE if the vacuum operation has
 finished, SQLITE\_OK if the vacuum operation has not finished but no error
 has occurred, and an SQLite error code if an error is encountered. If
 an error does occur, all subsequent calls to sqlite3rbu\_step() immediately
 return the same error code.
4. Finally, sqlite3rbu\_close() is called to close the RBU handle. If the
 application stopped calling sqlite3rbu\_step() before either the vacuum
 finished or an error occurred, the state of the vacuum is saved in the
 state database so that it may be resumed later on.

 

 Like sqlite3rbu\_step(), if the vacuum operation has finished,
 sqlite3rbu\_close() returns SQLITE\_DONE. If the vacuum has not finished
 but no error has occurred, SQLITE\_OK is returned. Or, if an error has
 occurred, an SQLite error code is returned. If an error occurred as part
 of a prior call to sqlite3rbu\_step(), sqlite3rbu\_close() returns the
 same error code.


The following example code illustrates the techniques described above. 




```
/*
** Either start a new RBU vacuum or resume a suspended RBU vacuum on 
** database zTarget. Return when either an error occurs, the RBU 
** vacuum is finished or when the application signals an interrupt
** (code not shown).
**
** If the RBU vacuum is completed successfully, return SQLITE_DONE.
** If an error occurs, return SQLite error code. Or, if the application
** signals an interrupt, suspend the RBU vacuum operation so that it
** may be resumed by a subsequent call to this function and return
** SQLITE_OK.
**
** This function uses the database named "<zTarget>-vacuum" for
** the state database, where <zTarget> is the name of the database 
** being vacuumed.
*/
int do_rbu_vacuum(const char *zTarget){
  int rc;
  char *zState;                   /* Name of state database */
  sqlite3rbu *pRbu;               /* RBU vacuum handle */

  zState = sqlite3_mprintf("%s-vacuum", zTarget);
  if( zState==0 ) return SQLITE_NOMEM;
  pRbu = sqlite3rbu_vacuum(zTarget, zState);
  sqlite3_free(zState);

  if( pRbu ){
    sqlite3 *dbTarget = sqlite3rbu_db(pRbu, 0);
    sqlite3 *dbState = sqlite3rbu_db(pRbu, 1);

    /* Any custom collation sequences used by the target database must
    ** be registered with both database handles here.  */

    while( sqlite3rbu_step(pRbu)==SQLITE_OK ){
      if( <application has signaled interrupt> ) break;
    }
  }
  rc = sqlite3rbu_close(pRbu);
  return rc;
}

```

*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


