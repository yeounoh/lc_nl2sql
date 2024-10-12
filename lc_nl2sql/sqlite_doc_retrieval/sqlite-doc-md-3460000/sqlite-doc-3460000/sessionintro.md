




The Session Extension




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










The Session Extension


►
Table Of Contents
[1\. Introduction](#introduction)
[1\.1\. Typical Use Case](#typical_use_case)
[1\.2\. Obtaining the Session Extension](#obtaining_the_session_extension)
[1\.3\. Limitations](#limitations)
[2\. Concepts](#concepts)
[2\.1\. Changesets and Patchsets](#changesets_and_patchsets)
[2\.2\. Conflicts](#conflicts)
[2\.3\. Changeset Construction](#changeset_construction)
[3\. Using The Session Extension](#using_the_session_extension)
[3\.1\. Capturing a Changeset](#capturing_a_changeset)
[3\.2\. Applying a Changeset to a Database](#applying_a_changeset_to_a_database)
[3\.3\. Inspecting the Contents of a Changeset](#inspecting_the_contents_of_a_changeset)
[4\. Extended Functionality](#extended_functionality)




# 1\. Introduction


The session extension provide a mechanism for conviently recording
changes to some or all of certain tables in an SQLite database, and
packaging those changes into a "changeset" or "patchset" file that can
later be used to apply the same set of changes to another database with
the same schema and compatible starting data. A "changeset" may
also be inverted and used to "undo" a session.



This document is an introduction to the session extension.
The details of the interface are in the separate
[Session Extension C\-language Interface](session/intro.html) document.



## 1\.1\. Typical Use Case


Suppose SQLite is used as the [application file format](appfileformat.html) for a
particular design application. Two users, Alice and Bob, each start
with a baseline design that is about a gigabyte in size. They work
all day, in parallel, each making their own customizations and tweaks
to the design. At the end of the day, they would like to merge their
changes together into a single unified design.



The session extension facilitates this by recording all changes to
both Alice's and Bob's databases and writing those changes into
changeset or patchset files. At the end of the day, Alice can send her
changeset to Bob and Bob can "apply" it to his database. The result (assuming
there are no conflicts) is that Bob's database then contains both his
changes and Alice's changes. Likewise, Bob can send a changeset of
his work over to Alice and she can apply his changes to her database.



In other words, the session extension provides a facility for
SQLite database files that is similar to the unix
[patch](https://en.wikipedia.org/wiki/Patch_(Unix)) utility program,
or to the "merge" capabilities of version control systems such
as [Fossil](https://www.fossil-scm.org/), [Git](https://git-scm.com),
or [Mercurial](http://www.mercurial-scm.org/).



## 1\.2\. Obtaining the Session Extension


 Since [version 3\.13\.0](releaselog/3_13_0.html) (2016\-05\-18\),
the session extension has been included in the SQLite
[amalgamation](amalgamation.html) source distribution. By default, the session extension is
disabled. To enable it, build with the following compiler switches:




```
-DSQLITE_ENABLE_SESSION -DSQLITE_ENABLE_PREUPDATE_HOOK

```

 Or, if using the autoconf build system,
pass the \-\-enable\-session option to the configure script.



## 1\.3\. Limitations


* Prior to SQLite version 3\.17\.0, the session extension only worked with
 [rowid tables](rowidtable.html), not [WITHOUT ROWID](withoutrowid.html) tables. As of 3\.17\.0, both
 rowid and WITHOUT ROWID tables are supported. However, extra steps are
 needed to record primary keys for WITHOUT ROWID table changes.
* There is no support for [virtual tables](vtab.html). Changes to virtual tables are
 not captured.
* The session extension only works with tables that have a declared
 PRIMARY KEY. The PRIMARY KEY of a table may be an INTEGER PRIMARY KEY
 (rowid alias) or an external PRIMARY KEY.
* SQLite allows [NULL values](nulls.html) to be stored in
 PRIMARY KEY columns. However, the session extension ignores all
 such rows. No changes affecting rows with one or more NULL values
 in PRIMARY KEY columns are recorded by the sessions module.


# 2\. Concepts



## 2\.1\. Changesets and Patchsets


 The sessions module revolves around creating and manipulating
changesets. A changeset is a blob of data that encodes a series of
changes to a database. Each change in a changeset is one of the
following:



* An **INSERT**. An INSERT change contains a single row to add to
 a database table. The payload of the INSERT change consists of the
 values for each field of the new row.
* A **DELETE**. A DELETE change represents a row, identified by
 its primary key values, to remove from a database table. The payload
 of a DELETE change consists of the values for all fields of the
 deleted row.
* An **UPDATE**. An UPDATE change represents the modification of
 one or more non\-PRIMARY KEY fields of a single row within a database
 table, identified by its PRIMARY KEY fields. The payload for an UPDATE
 change consists of:
 


	+ The PRIMARY KEY values identifying the modified row,
	+ The new values for each modified field of the row, and
	+ The original values for each modified field of the row. An UPDATE change does not contain any information regarding
 non\-PRIMARY KEY fields that are not modified by the change. It is not
 possible for an UPDATE change to specify modifications to PRIMARY
 KEY fields.


 A single changeset may contain changes that apply to more than one
database table. For each table that the changeset includes at least one change
for, it also encodes the following data:



* The name of the database table,
* The number of columns the table has, and
* Which of those columns are PRIMARY KEY columns.


 Changesets may only be applied to databases that contain tables
matching the above three criteria as stored in the changeset.



 A patchset is similar to a changeset. It is slightly more compact than
a changeset, but provides more limited conflict detection and resolution
options (see the next section for details). The differences between a
patchset and a changeset are that:



* For a **DELETE** change, the payload consists of the PRIMARY KEY
 fields only. The original values of other fields are not stored as
 part of a patchset.
* For an **UPDATE** change, the payload consists of the PRIMARY KEY
 fields and the new values of modified fields only. The original
 values of modified fields are not stored as part of a patchset.


## 2\.2\. Conflicts


 When a changeset or patchset is applied to a database, an attempt is
made to insert a new row for each INSERT change, remove a row for each
DELETE change and modify a row for each UPDATE change. If the target
database is in the same state as the original database that the changeset
was recorded on, this is a simple matter. However, if the contents of the
target database is not in exactly this state, conflicts can occur when
applying the changeset or patchset.



When processing an **INSERT** change, the following conflicts can
occur:



* The target database may already contain a row with the same PRIMARY
 KEY values as specified by the INSERT change.
* Some other database constraint, for example a UNIQUE or CHECK
 constraint, may be violated when the new row is inserted.


When processing a **DELETE** change, the following conflicts may be
detected:



* The target database may contain no row with the specified PRIMARY
 KEY values to delete.
* The target database may contain a row with the specified PRIMARY
 KEY values, but the other fields may contain values that do not
 match those stored as part of the changeset. This type of conflict
 is not detected when using a patchset.


When processing an **UPDATE** change, the following conflicts may be
detected:



* The target database may contain no row with the specified PRIMARY
 KEY values to modify.
* The target database may contain a row with the specified PRIMARY
 KEY values, but the current values of the fields that will be modified
 by the change may not match the original values stored within the
 changeset. This type of conflict is not detected when using a patchset.
* Some other database constraint, for example a UNIQUE or CHECK
 constraint, may be violated when the row is updated.


 Depending on the type of conflict, a sessions application has a variety
of configurable options for dealing with conflicts, ranging from omitting the
conflicting change, aborting the entire changeset application or applying
the change despite the conflict. For details, refer to the documentation for
the [sqlite3changeset\_apply()](session/sqlite3changeset_apply.html) API.



## 2\.3\. Changeset Construction


 After a session object has been configured, it begins monitoring for
changes to its configured tables. However, it does not record an entire
change each time a row within the database is modified. Instead, it records
just the PRIMARY KEY fields for each inserted row, and just the PRIMARY KEY
and all original row values for any updated or deleted rows. If a row is
modified more than once by a single session, no new information is recorded.



 The other information required to create a changeset or patchset is
read from the database file when [sqlite3session\_changeset()](session/sqlite3session_changeset.html) or
[sqlite3session\_patchset()](session/sqlite3session_patchset.html) is called. Specifically,



* For each primary key recorded as a result of an INSERT operation,
 the sessions module checks if there is a row with a matching primary
 key still in the table. If so, an INSERT change is added to the
 changeset.
* For each primary key recorded as a result of an UPDATE or DELETE
 operation, the sessions module also checks for a row with a matching
 primary key within the table. If one can be found, but one or more
 of the non\-PRIMARY KEY fields does not match the original recorded
 value, an UPDATE is added to the changeset. Or, if there is no row
 at all with the specified primary key, a DELETE is added to the
 changeset. If the row does exist but none of the non\-PRIMARY KEY
 fields have been modified, no change is added to the changeset.


 One implication of the above is that if a change is made and then
unmade within a single session (for example if a row is inserted and then
deleted again), the sessions module does not report any change at all. Or
if a row is updated multiple times within the same session, all updates
are coalesced into a single update within any changeset or patchset blob.



# 3\. Using The Session Extension


 This section provides examples that demonstrate how to use the sessions
 extension.



## 3\.1\. Capturing a Changeset


 The example code below demonstrates the steps involved in capturing a
changeset while executing SQL commands. In summary:



1. A session object (type sqlite3\_session\*) is created by making a
 call to the [sqlite3session\_create()](session/sqlite3session_create.html) API function.

 

A single session object monitors changes made to a single database
 (i.e. "main", "temp" or an attached database) via a single
 sqlite3\* database handle.
2. The session object is configured with a set of tables to monitor
 changes on.

 

 By default a session object does not monitor changes on any
 database table. Before it does so it must be configured. There
 are three ways to configure the set of tables to monitor changes
 on:
 


	* By explicitly specifying tables using one call to
	 [sqlite3session\_attach()](session/sqlite3session_attach.html) for each table, or
	* By specifying that all tables in the database should be monitored
	 for changes using a call to [sqlite3session\_attach()](session/sqlite3session_attach.html) with a
	 NULL argument, or
	* By configuring a callback to be invoked the first time each table
	 is written to that indicates to the session module whether or
	 not changes on the table should be monitored. The example code below uses the second of the methods enumerated
 above \- it monitors for changes on all database tables.
3. Changes are made to the database by executing SQL statements. The
 session object records these changes.
4. A changeset blob is extracted from the session object using a call
 to [sqlite3session\_changeset()](session/sqlite3session_changeset.html) (or, if using patchsets, a call to
 the [sqlite3session\_patchset()](session/sqlite3session_patchset.html) function).
5. The session object is deleted using a call to the
 [sqlite3session\_delete()](session/sqlite3session_delete.html) API function.

 

 It is not necessary to delete a session object after extracting
 a changeset or patchset from it. It can be left attached to the
 database handle and will continue monitoring for changes on the
 configured tables as before. However, if
 [sqlite3session\_changeset()](session/sqlite3session_changeset.html) or [sqlite3session\_patchset()](session/sqlite3session_patchset.html) is
 called a second time on a session object, the changeset or patchset
 will contain *all* changes that have taken place on the connection
 since the session was created. In other words,
 a session object is not reset or
 zeroed by a call to sqlite3session\_changeset() or
 sqlite3session\_patchset().



```
/*
** Argument zSql points to a buffer containing an SQL script to execute
** against the database handle passed as the first argument. As well as
** executing the SQL script, this function collects a changeset recording
** all changes made to the "main" database file. Assuming no error occurs,
** output variables (*ppChangeset) and (*pnChangeset) are set to point
** to a buffer containing the changeset and the size of the changeset in
** bytes before returning SQLITE_OK. In this case it is the responsibility
** of the caller to eventually free the changeset blob by passing it to
** the sqlite3_free function.
**
** Or, if an error does occur, return an SQLite error code. The final
** value of (*pChangeset) and (*pnChangeset) are undefined in this case.
*/
int sql_exec_changeset(
  sqlite3 *db,                  /* Database handle */
  const char *zSql,             /* SQL script to execute */
  int *pnChangeset,             /* OUT: Size of changeset blob in bytes */
  void **ppChangeset            /* OUT: Pointer to changeset blob */
){
  sqlite3_session *pSession = 0;
  int rc;

  /* Create a new session object */
  rc = sqlite3session_create(db, "main", &pSession);

  /* Configure the session object to record changes to all tables */
  if( rc==SQLITE_OK ) rc = sqlite3session_attach(pSession, NULL);

  /* Execute the SQL script */
  if( rc==SQLITE_OK ) rc = sqlite3_exec(db, zSql, 0, 0, 0);

  /* Collect the changeset */
  if( rc==SQLITE_OK ){
    rc = sqlite3session_changeset(pSession, pnChangeset, ppChangeset);
  }

  /* Delete the session object */
  sqlite3session_delete(pSession);

  return rc;
}

```

## 3\.2\. Applying a Changeset to a Database


 Applying a changeset to a database is simpler than capturing a changeset.
Usually, a single call to [sqlite3changeset\_apply()](session/sqlite3changeset_apply.html), as depicted in the
example code below, suffices.



 In cases where it is complicated, the complications in applying a
changeset lie in conflict resolution. Refer to the API documentation linked
above for details.

 


```
/*
** Conflict handler callback used by apply_changeset(). See below.
*/
static int xConflict(void *pCtx, int eConflict, sqlite3_changset_iter *pIter){
  int ret = (int)pCtx;
  return ret;
}

/*
** Apply the changeset contained in blob pChangeset, size nChangeset bytes,
** to the main database of the database handle passed as the first argument.
** Return SQLITE_OK if successful, or an SQLite error code if an error
** occurs.
**
** If parameter bIgnoreConflicts is true, then any conflicting changes
** within the changeset are simply ignored. Or, if bIgnoreConflicts is
** false, then this call fails with an SQLITE_ABORT error if a changeset
** conflict is encountered.
*/
int apply_changeset(
  sqlite3 *db,                  /* Database handle */
  int bIgnoreConflicts,         /* True to ignore conflicting changes */
  int nChangeset,               /* Size of changeset in bytes */
  void *pChangeset              /* Pointer to changeset blob */
){
  return sqlite3changeset_apply(
      db,
      nChangeset, pChangeset,
      0, xConflict,
      (void*)bIgnoreConflicts
  );
}

```

## 3\.3\. Inspecting the Contents of a Changeset


 The example code below demonstrates the techniques used to iterate
through and extract the data related to all changes in a changeset. To
summarize:



1. The [sqlite3changeset\_start()](session/sqlite3changeset_start.html) API is called to create and
 initialize an iterator to iterate through the contents of a
 changeset. Initially, the iterator points to no element at all.
2. The first call to [sqlite3changeset\_next()](session/sqlite3changeset_next.html) on the iterator moves
 it to point to the first change in the changeset (or to EOF, if
 the changeset is completely empty). sqlite3changeset\_next() returns
 SQLITE\_ROW if it moves the iterator to point to a valid entry,
 SQLITE\_DONE if it moves the iterator to EOF, or an SQLite error
 code if an error occurs.
3. If the iterator points to a valid entry, the [sqlite3changeset\_op()](session/sqlite3changeset_op.html)
 API may be used to determine the type of change (INSERT, UPDATE or
 DELETE) that the iterator points to. Additionally, the same API
 can be used to obtain the name of the table the change applies to
 and its expected number of columns and primary key columns.
4. If the iterator points to a valid INSERT or UPDATE entry, the
 [sqlite3changeset\_new()](session/sqlite3changeset_new.html) API may be used to obtain the new.\* values
 within the change payload.
5. If the iterator points to a valid DELETE or UPDATE entry, the
 [sqlite3changeset\_old()](session/sqlite3changeset_old.html) API may be used to obtain the old.\* values
 within the change payload.
6. An iterator is deleted using a call to the
 [sqlite3changeset\_finalize()](session/sqlite3changeset_finalize.html) API. If an error occured while
 iterating, an SQLite error code is returned (even if the same error
 code has already been returned by sqlite3changeset\_next()). Or,
 if no error has occurred, SQLITE\_OK is returned.



```
/*
** Print the contents of the changeset to stdout.
*/
static int print_changeset(void *pChangeset, int nChangeset){
  int rc;
  sqlite3_changeset_iter *pIter = 0;

  /* Create an iterator to iterate through the changeset */
  rc = sqlite3changeset_start(&pIter, nChangeset, pChangeset);
  if( rc!=SQLITE_OK ) return rc;

  /* This loop runs once for each change in the changeset */
  while( SQLITE_ROW==sqlite3changeset_next(pIter) ){
    const char *zTab;           /* Table change applies to */
    int nCol;                   /* Number of columns in table zTab */
    int op;                     /* SQLITE_INSERT, UPDATE or DELETE */
    sqlite3_value *pVal;

    /* Print the type of operation and the table it is on */
    rc = sqlite3changeset_op(pIter, &zTab, &nCol, &op, 0);
    if( rc!=SQLITE_OK ) goto exit_print_changeset;
    printf("%s on table %s\n",
      op==SQLITE_INSERT?"INSERT" : op==SQLITE_UPDATE?"UPDATE" : "DELETE",
      zTab
    );

    /* If this is an UPDATE or DELETE, print the old.* values */
    if( op==SQLITE_UPDATE || op==SQLITE_DELETE ){
      printf("Old values:");
      for(i=0; i<nCol; i++){
        rc = sqlite3changeset_old(pIter, i, &pVal);
        if( rc!=SQLITE_OK ) goto exit_print_changeset;
        printf(" %s", pVal ? sqlite3_value_text(pVal) : "-");
      }
      printf("\n");
    }

    /* If this is an UPDATE or INSERT, print the new.* values */
    if( op==SQLITE_UPDATE || op==SQLITE_INSERT ){
      printf("New values:");
      for(i=0; i<nCol; i++){
        rc = sqlite3changeset_new(pIter, i, &pVal);
        if( rc!=SQLITE_OK ) goto exit_print_changeset;
        printf(" %s", pVal ? sqlite3_value_text(pVal) : "-");
      }
      printf("\n");
    }
  }

  /* Clean up the changeset and return an error code (or SQLITE_OK) */
 exit_print_changeset:
  rc2 = sqlite3changeset_finalize(pIter);
  if( rc==SQLITE_OK ) rc = rc2;
  return rc;
}

```

# 4\. Extended Functionality


 Most applications will only use the session module functionality described
in the previous section. However, the following additional functionality is
available for the use and manipulation of changeset and patchset blobs:



* Two or more changeset/patchsets may be combined using the
 [sqlite3changeset\_concat()](session/sqlite3changeset_concat.html) or [sqlite3\_changegroup](session/changegroup.html) interfaces.
* A changeset may be "inverted" using the [sqlite3changeset\_invert()](session/sqlite3changeset_invert.html)
 API function. An inverted changeset undoes the changes made by the
 original. If changeset C\+ is the inverse of changeset C, then
 applying C and then C\+ to a database should leave
 the database unchanged.


