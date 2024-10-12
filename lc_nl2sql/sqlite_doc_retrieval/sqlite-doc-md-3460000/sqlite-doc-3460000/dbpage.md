




The SQLITE\_DBPAGE Virtual Table




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The SQLITE\_DBPAGE Virtual Table


# 1\. Overview



The SQLITE\_DBPAGE extension implements an [eponymous\-only virtual table](vtab.html#epoonlyvtab) that
provides direct access to the underlying database file by interacting
with the pager. SQLITE\_DBPAGE is capable of both reading and writing any
page of the database. Because interaction is through the pager layer, all
changes are transactional.




**Warning:** writing to the SQLITE\_DBPAGE virtual table can very easily
cause unrecoverably database corruption. Do not allow untrusted components
to access the SQLITE\_DBPAGE table. Use appropriate care while using the
SQLITE\_DBPAGE table. Back up important data prior to experimenting with the
SQLITE\_DBPAGE table. Writes to the SQLITE\_DBPAGE virtual table are
disabled when the [SQLITE\_DBCONFIG\_DEFENSIVE](c3ref/c_dbconfig_defensive.html#sqlitedbconfigdefensive) flag is set.




The SQLITE\_DBPAGE extension is included in the [amalgamation](amalgamation.html) though 
it is disabled
by default. Use the [SQLITE\_ENABLE\_DBPAGE\_VTAB](compile.html#enable_dbpage_vtab) compile\-time option to enable
the SQLITE\_DBPAGE extension. The SQLITE\_DBPAGE extension makes use of
unpublished internal interfaces and is not run\-time loadable. The only way
to add SQLITE\_DBPAGE to an application is to compile it in using the
[SQLITE\_ENABLE\_DBPAGE\_VTAB](compile.html#enable_dbpage_vtab) compile\-time option.




The SQLITE\_DBPAGE extension is enabled in default builds
of the [command\-line shell](cli.html).



# 2\. Usage



The SQLITE\_DBPAGE virtual table read/write table that provides direct
access to the underlying disk file on a page\-by\-page basis. The
virtual table appears to have a schema like this:




```
CREATE TABLE sqlite_dbpage(
  pgno INTEGER PRIMARY KEY,
  data BLOB
);

```


An SQLite database file is divided into pages.
The first page is 1, the second page is 2, and so forth.
There is no page 0\.
Every page is the same size.
The size of every page is a power of 2 between 512 and 65536\.
See the [file format](fileformat2.html) documentation for further details.




The SQLITE\_DBPAGE table allows an application to view or replace the
raw binary content of each page of the database file.
No attempt is made to interpret the content of the page.
Content is returned byte\-for\-byte as it appears on disk.




The SQLITE\_DBPAGE table has one row for each page in the database file.
SQLITE\_DBPAGE allows pages to be read or to be overwritten.
However the size of the database file cannot be changed. It is not
possible to change the number of rows in the SQLITE\_DBPAGE table by
running DELETE or INSERT operations against that table.



## 2\.1\. Using SQLITE\_DBPAGE On ATTACH\-ed Databases



The SQLITE\_DBPAGE table schema shown above is incomplete. There is
a third [hidden column](vtab.html#hiddencol) named "schema" that determines which
[ATTACH\-ed database](lang_attach.html) should be read or written. Because
the "schema" column is hidden, it can be used as a parameter when
SQLITE\_DBPAGE is invoked as a [table\-valued function](vtab.html#tabfunc2).




For example, suppose an additional database is attached to the 
database connection using a statement like this:




```
ATTACH 'auxdata1.db' AS aux1;

```


Then to read the first page of that database file, one merely runs:




```
SELECT data FROM sqlite_dbpage('aux1') WHERE pgno=1;

```


If the "schema" is omitted, it defaults to the primary database
(usually called 'main', unless renamed using [SQLITE\_DBCONFIG\_MAINDBNAME](c3ref/c_dbconfig_defensive.html#sqlitedbconfigmaindbname)).
Hence, the following two queries are normally equivalent:




```
SELECT data FROM sqlite_dbpage('main') WHERE pgno=1;
SELECT data FROM sqlite_dbpage WHERE pgno=1;

```


The SQLITE\_DBPAGE table can participate in a join just like any other
table. Hence, to see the content of the first page to all connected
database files, one might run a statement like this:




```
SELECT dbpage.data, dblist.name
  FROM pragma_database_list AS dblist
  JOIN sqlite_dbpage(dblist.name) AS dbpage
 WHERE dbpage.pgno=1;

```

*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


