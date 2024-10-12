




Create A New Session Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Create A New Session Object


> ```
> int sqlite3session_create(
>   sqlite3 *db,                    /* Database handle */
>   const char *zDb,                /* Name of db (e.g. "main") */
>   sqlite3_session **ppSession     /* OUT: New session object */
> );
> 
> ```


Create a new session object attached to database handle db. If successful,
a pointer to the new object is written to \*ppSession and SQLITE\_OK is
returned. If an error occurs, \*ppSession is set to NULL and an SQLite
error code (e.g. SQLITE\_NOMEM) is returned.


It is possible to create multiple session objects attached to a single
database handle.


Session objects created using this function should be deleted using the
[sqlite3session\_delete()](../session/sqlite3session_delete.html) function before the database handle that they
are attached to is itself closed. If the database handle is closed before
the session object is deleted, then the results of calling any session
module function, including [sqlite3session\_delete()](../session/sqlite3session_delete.html) on the session object
are undefined.


Because the session module uses the [sqlite3\_preupdate\_hook()](../c3ref/preupdate_blobwrite.html) API, it
is not possible for an application to register a pre\-update hook on a
database handle that has one or more session objects attached. Nor is
it possible to create a session object attached to a database handle for
which a pre\-update hook is already defined. The results of attempting 
either of these things are undefined.


The session object will be used to create changesets for tables in
database zDb, where zDb is either "main", or "temp", or the name of an
attached database. It is not an error if database zDb is not attached
to the database when the session object is created.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


