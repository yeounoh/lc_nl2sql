




The pre\-update hook.




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## The pre\-update hook.




> ```
> 
> #if defined(SQLITE_ENABLE_PREUPDATE_HOOK)
> void *sqlite3_preupdate_hook(
>   sqlite3 *db,
>   void(*xPreUpdate)(
>     void *pCtx,                   /* Copy of third arg to preupdate_hook() */
>     sqlite3 *db,                  /* Database handle */
>     int op,                       /* SQLITE_UPDATE, DELETE or INSERT */
>     char const *zDb,              /* Database name */
>     char const *zName,            /* Table name */
>     sqlite3_int64 iKey1,          /* Rowid of row about to be deleted/updated */
>     sqlite3_int64 iKey2           /* New rowid value (for a rowid UPDATE) */
>   ),
>   void*
> );
> int sqlite3_preupdate_old(sqlite3 *, int, sqlite3_value **);
> int sqlite3_preupdate_count(sqlite3 *);
> int sqlite3_preupdate_depth(sqlite3 *);
> int sqlite3_preupdate_new(sqlite3 *, int, sqlite3_value **);
> int sqlite3_preupdate_blobwrite(sqlite3 *);
> #endif
> 
> ```



These interfaces are only available if SQLite is compiled using the
[SQLITE\_ENABLE\_PREUPDATE\_HOOK](../compile.html#enable_preupdate_hook) compile\-time option.


The [sqlite3\_preupdate\_hook()](../c3ref/preupdate_blobwrite.html) interface registers a callback function
that is invoked prior to each [INSERT](../lang_insert.html), [UPDATE](../lang_update.html), and [DELETE](../lang_delete.html) operation
on a database table.
At most one preupdate hook may be registered at a time on a single
[database connection](../c3ref/sqlite3.html); each call to [sqlite3\_preupdate\_hook()](../c3ref/preupdate_blobwrite.html) overrides
the previous setting.
The preupdate hook is disabled by invoking [sqlite3\_preupdate\_hook()](../c3ref/preupdate_blobwrite.html)
with a NULL pointer as the second parameter.
The third parameter to [sqlite3\_preupdate\_hook()](../c3ref/preupdate_blobwrite.html) is passed through as
the first parameter to callbacks.


The preupdate hook only fires for changes to real database tables; the
preupdate hook is not invoked for changes to [virtual tables](../vtab.html) or to
system tables like sqlite\_sequence or sqlite\_stat1\.


The second parameter to the preupdate callback is a pointer to
the [database connection](../c3ref/sqlite3.html) that registered the preupdate hook.
The third parameter to the preupdate callback is one of the constants
[SQLITE\_INSERT](../c3ref/c_alter_table.html), [SQLITE\_DELETE](../c3ref/c_alter_table.html), or [SQLITE\_UPDATE](../c3ref/c_alter_table.html) to identify the
kind of update operation that is about to occur.
The fourth parameter to the preupdate callback is the name of the
database within the database connection that is being modified. This
will be "main" for the main database or "temp" for TEMP tables or
the name given after the AS keyword in the [ATTACH](../lang_attach.html) statement for attached
databases.
The fifth parameter to the preupdate callback is the name of the
table that is being modified.


For an UPDATE or DELETE operation on a [rowid table](../rowidtable.html), the sixth
parameter passed to the preupdate callback is the initial [rowid](../lang_createtable.html#rowid) of the
row being modified or deleted. For an INSERT operation on a rowid table,
or any operation on a WITHOUT ROWID table, the value of the sixth
parameter is undefined. For an INSERT or UPDATE on a rowid table the
seventh parameter is the final rowid value of the row being inserted
or updated. The value of the seventh parameter passed to the callback
function is not defined for operations on WITHOUT ROWID tables, or for
DELETE operations on rowid tables.


The sqlite3\_preupdate\_hook(D,C,P) function returns the P argument from
the previous call on the same [database connection](../c3ref/sqlite3.html) D, or NULL for
the first call on D.


The [sqlite3\_preupdate\_old()](../c3ref/preupdate_blobwrite.html), [sqlite3\_preupdate\_new()](../c3ref/preupdate_blobwrite.html),
[sqlite3\_preupdate\_count()](../c3ref/preupdate_blobwrite.html), and [sqlite3\_preupdate\_depth()](../c3ref/preupdate_blobwrite.html) interfaces
provide additional information about a preupdate event. These routines
may only be called from within a preupdate callback. Invoking any of
these routines from outside of a preupdate callback or with a
[database connection](../c3ref/sqlite3.html) pointer that is different from the one supplied
to the preupdate callback results in undefined and probably undesirable
behavior.


The [sqlite3\_preupdate\_count(D)](../c3ref/preupdate_blobwrite.html) interface returns the number of columns
in the row that is being inserted, updated, or deleted.


The [sqlite3\_preupdate\_old(D,N,P)](../c3ref/preupdate_blobwrite.html) interface writes into P a pointer to
a [protected sqlite3\_value](../c3ref/value.html) that contains the value of the Nth column of
the table row before it is updated. The N parameter must be between 0
and one less than the number of columns or the behavior will be
undefined. This must only be used within SQLITE\_UPDATE and SQLITE\_DELETE
preupdate callbacks; if it is used by an SQLITE\_INSERT callback then the
behavior is undefined. The [sqlite3\_value](../c3ref/value.html) that P points to
will be destroyed when the preupdate callback returns.


The [sqlite3\_preupdate\_new(D,N,P)](../c3ref/preupdate_blobwrite.html) interface writes into P a pointer to
a [protected sqlite3\_value](../c3ref/value.html) that contains the value of the Nth column of
the table row after it is updated. The N parameter must be between 0
and one less than the number of columns or the behavior will be
undefined. This must only be used within SQLITE\_INSERT and SQLITE\_UPDATE
preupdate callbacks; if it is used by an SQLITE\_DELETE callback then the
behavior is undefined. The [sqlite3\_value](../c3ref/value.html) that P points to
will be destroyed when the preupdate callback returns.


The [sqlite3\_preupdate\_depth(D)](../c3ref/preupdate_blobwrite.html) interface returns 0 if the preupdate
callback was invoked as a result of a direct insert, update, or delete
operation; or 1 for inserts, updates, or deletes invoked by top\-level
triggers; or 2 for changes resulting from triggers called by top\-level
triggers; and so forth.


When the [sqlite3\_blob\_write()](../c3ref/blob_write.html) API is used to update a blob column,
the pre\-update hook is invoked with SQLITE\_DELETE. This is because the
in this case the new values are not available. In this case, when a
callback made with op\=\=SQLITE\_DELETE is actually a write using the
sqlite3\_blob\_write() API, the [sqlite3\_preupdate\_blobwrite()](../c3ref/preupdate_blobwrite.html) returns
the index of the column being written. In other cases, where the
pre\-update hook is being invoked for some other reason, including a
regular DELETE, sqlite3\_preupdate\_blobwrite() returns \-1\.


See also: [sqlite3\_update\_hook()](../c3ref/update_hook.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


