




Imposter Tables




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Imposter Tables


# 1\. Introduction



An imposter table is a table that is attached to the same [b\-tree](fileformat2.html#btree)
as an index.
An imposter table allows the content of an index to be queried or
modified as if the index were an ordinary table.




Imposter tables are intended for analysis and debugging only.
This is not a feature that most application developers should understand
or even know about.
Imposter tables are for experts only.




Improper use of imposter tables can cause index corruption, though
any corruption created this way can be fixed by running [REINDEX](lang_reindex.html).



# 2\. Details



Each table and each index in SQLite is stored in a separate b\-tree
in the database file. Each b\-tree is identified by its root page
number. The root page number for any index or table can be found
by querying the "rootpage" column of the [sqlite\_schema table](schematab.html).
See the [indexing tutorial](queryplanner.html) and the [file format](fileformat2.html) documentation
for further background on this design.




Usually the b\-trees for tables and indexes are slightly different.
A table b\-tree contains a 64\-bit integer key and arbitrary data.
The 64\-bit integer key is the [ROWID](lang_createtable.html#rowid). Index b\-trees contain
an arbitrary binary key and no data. So table b\-trees and index
b\-trees are not directly compatible.




However, the b\-tree for a [WITHOUT ROWID](withoutrowid.html) table is in the same format
as an index b\-tree. Thus, an index b\-tree can be accessed as if it
were a WITHOUT ROWID table.



## 2\.1\. Manually Created Imposter Tables



One way to create an imposter table is to directly edit the sqlite\_schema
table to insert a new row that describes the table.
For example, suppose the schema is like this:




```
CREATE TABLE t1(a INTEGER PRIMARY KEY,b TEXT,c INT, d INT);
CREATE INDEX t1bc ON t1(b,c);

```


The WITHOUT ROWID table that has the same structure as the t1bc index
would look like this:




```
CREATE TABLE t2(b TEXT,c INT,a INT, PRIMARY KEY(b,c,a)) WITHOUT ROWID;

```


To create a permanent imposter table "t2" against index "t1bc" one
should first enable editing of the sqlite\_schema table by running
"[PRAGMA writable\_schema\=ON](pragma.html#pragma_writable_schema)".
(Be careful to observe the warnings that accompany this PRAGMA.
A mistake can cause severe database corruption.)
Then insert a new entry into the sqlite\_schema table like this:




```
INSERT INTO sqlite_schema(type,name,tbl_name,rootpage,sql)
 SELECT 'table','t2','t2',rootpage,
   'CREATE TABLE t2(b,c,a,PRIMARY KEY(b,c,a))WITHOUT ROWID'
   FROM sqlite_schema
  WHERE name='t1bc';

```


The INSERT statement above adds a new row to the sqlite\_schema table that
defines a table "t2" having the same on\-disk format as index "t1bc" and 
pointing to the same b\-tree.
After adding this sqlite\_schema table entry, it is necessary to close and
reopen the database in order to get SQLite to reread the schema.
Then the "t2" table can be queried to see the content of the "t1bc" index.



### 2\.1\.1\. Corrupted Database



A serious problem with the manual imposter table approach described above
is that after adding the new "t2" entry to the "sqlite\_schema" table, the
database file will technically be corrupt. Both the "t1bc" index and the
"t2" table will point to the same b\-tree. This will not cause
any immediate problems, though one should avoid running [VACUUM](lang_vacuum.html).




It is possible to write into the "t2" table, thus changing the content
of the index.
But doing so will get the "t1bc" index out of synchronization with its
parent table "t1". An out\-of\-sync index can result in incorrect query
results.




Since the "t2" imposter table is a form of database corruption, the
manual approach to creating imposter tables is not recommended.
Actually, any use of imposter tables is discouraged for all but
expert developers, but manually created imposter tables are
especially discouraged because they are permanent.



## 2\.2\. Transient Imposter Tables



Another (safer) approach to creating an imposter table is to add an
entry for the imposter table to SQLite's internal symbol table without
updating the "sqlite\_schema" table on disk.
That way, the imposter table exists in only a single database connection
and is automatically removed whenever the schema is reloaded.




Creation of a transient imposter table involves a special
[sqlite3\_test\_control()](c3ref/test_control.html) call. Unlike all other SQLite APIs,
[sqlite3\_test\_control()](c3ref/test_control.html) interface is subject to incompatible changes
from one release to the next, and so the mechanism described below
is not guaranteed to work in future releases of SQLite. The
SQLite developers do not consider this a problem because imposter
tables should not be used in applications. Imposter tables are for
analysis and testing use only.




To create a transient imposter table, first call sqlite3\_test\_control()
as follows:




```
sqlite3_test_control(SQLITE_TESTCTRL_IMPOSTER, db, "main", 1, tnum);

```


The "db" parameter is a pointer to the [database connection](c3ref/sqlite3.html).
The "main" argument is the name of the schema in which the imposter
table is to be created. The "1" argument enables the imposter table
mechanism. "tnum" is the root page of the index that the imposter
table should mirror.




After the sqlite3\_test\_control() call above, then run a [CREATE TABLE](lang_createtable.html)
statement the defines the imposter table.
With the imposter mechanism enabled, this CREATE TABLE statement does
not create a real table but instead merely adds an entry in SQLite's
internal symbol table. Note that the CREATE TABLE statement must
be in the correct format for the index. If the imposter table has the
wrong number of columns or is not a [WITHOUT ROWID](withoutrowid.html) table or is otherwise
incompatible with the index b\-tree, then [SQLITE\_CORRUPT](rescode.html#corrupt) errors will result
when the imposter table is used.




After running the CREATE TABLE statement, disable the imposter mechanism
as follows:




```
sqlite3_test_control(SQLITE_TESTCTRL_IMPOSTER, db, "main", 0, 0);

```


In other words, make the same sqlite3\_test\_control() call except change
the last two parameters to zero.




After the imposter table is loaded into SQLite's internal schema as
described above, the imposter table can be used as any other table.
But the imposter table will only be visible to the one database
connection that created it. No changes are made to the database file
on disk. And the imposter table will disappear the next time the schema 
is loaded.




## 2\.3\. The .imposter Shell Command



As of SQLite 3\.16\.0 (2017\-01\-02\), the [command\-line shell](cli.html) contains
a dot\-command ".imposter" that does all of the work of setting up a
transient imposter table.
Instead of making multiple calls to sqlite3\_test\_control() and figuring
out and invoking a compatible CREATE TABLE statement, a transient
imposter table can be constructed as follows:




```
.imposter t1bc t2

```


Of course, substitute the desired index and imposter table names in
place of the "t1bc" and "t2" shown in the example.
The ".imposter" command reads the schema of the "t1bc" index, uses
that information to construct a compatible CREATE TABLE statement for
the imposter table, then makes all the necessary calls to create the
transient imposter table automatically.



# 3\. Summary And Final Warning



The imposter table mechanism is a power analysis and debugging tool
for SQLite. But as with all sharp tools, it can also be dangerous and
can result in corrupt database files if misused. Do not attempt to
use imposter tables in an application. Imposter tables are intended
for use in the laboratory by experts.



*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


