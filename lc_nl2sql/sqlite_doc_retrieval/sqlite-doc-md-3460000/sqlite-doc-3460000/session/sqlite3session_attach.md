




Attach A Table To A Session Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Attach A Table To A Session Object


> ```
> int sqlite3session_attach(
>   sqlite3_session *pSession,      /* Session object */
>   const char *zTab                /* Table name */
> );
> 
> ```


If argument zTab is not NULL, then it is the name of a table to attach
to the session object passed as the first argument. All subsequent changes 
made to the table while the session object is enabled will be recorded. See 
documentation for [sqlite3session\_changeset()](../session/sqlite3session_changeset.html) for further details.


Or, if argument zTab is NULL, then changes are recorded for all tables
in the database. If additional tables are added to the database (by 
executing "CREATE TABLE" statements) after this call is made, changes for 
the new tables are also recorded.


Changes can only be recorded for tables that have a PRIMARY KEY explicitly
defined as part of their CREATE TABLE statement. It does not matter if the 
PRIMARY KEY is an "INTEGER PRIMARY KEY" (rowid alias) or not. The PRIMARY
KEY may consist of a single column, or may be a composite key.


It is not an error if the named table does not exist in the database. Nor
is it an error if the named table does not have a PRIMARY KEY. However,
no changes will be recorded in either of these scenarios.


Changes are not recorded for individual rows that have NULL values stored
in one or more of their PRIMARY KEY columns.


SQLITE\_OK is returned if the call completes without error. Or, if an error 
occurs, an SQLite error code (e.g. SQLITE\_NOMEM) is returned.


### Special sqlite\_stat1 Handling




As of SQLite version 3\.22\.0, the "sqlite\_stat1" table is an exception to 
some of the rules above. In SQLite, the schema of sqlite\_stat1 is:
 
```

       CREATE TABLE sqlite_stat1(tbl,idx,stat)  
 
```



Even though sqlite\_stat1 does not have a PRIMARY KEY, changes are 
recorded for it as if the PRIMARY KEY is (tbl,idx). Additionally, changes 
are recorded for rows for which (idx IS NULL) is true. However, for such
rows a zero\-length blob (SQL value X'') is stored in the changeset or
patchset instead of a NULL value. This allows such changesets to be
manipulated by legacy implementations of sqlite3changeset\_invert(),
concat() and similar.


The sqlite3changeset\_apply() function automatically converts the 
zero\-length blob back to a NULL value when updating the sqlite\_stat1
table. However, if the application calls sqlite3changeset\_new(),
sqlite3changeset\_old() or sqlite3changeset\_conflict on a changeset 
iterator directly (including on a changeset iterator passed to a
conflict\-handler callback) then the X'' value is returned. The application
must translate X'' to NULL itself if required.


Legacy (older than 3\.22\.0\) versions of the sessions module cannot capture
changes made to the sqlite\_stat1 table. Legacy versions of the
sqlite3changeset\_apply() function silently ignore any modifications to the
sqlite\_stat1 table that are part of a changeset or patchset.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


