




Commit And Rollback Notification Callbacks




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Commit And Rollback Notification Callbacks




> ```
> 
> void *sqlite3_commit_hook(sqlite3*, int(*)(void*), void*);
> void *sqlite3_rollback_hook(sqlite3*, void(*)(void *), void*);
> 
> ```



The sqlite3\_commit\_hook() interface registers a callback
function to be invoked whenever a transaction is [committed](../lang_transaction.html).
Any callback set by a previous call to sqlite3\_commit\_hook()
for the same database connection is overridden.
The sqlite3\_rollback\_hook() interface registers a callback
function to be invoked whenever a transaction is [rolled back](../lang_transaction.html).
Any callback set by a previous call to sqlite3\_rollback\_hook()
for the same database connection is overridden.
The pArg argument is passed through to the callback.
If the callback on a commit hook function returns non\-zero,
then the commit is converted into a rollback.


The sqlite3\_commit\_hook(D,C,P) and sqlite3\_rollback\_hook(D,C,P) functions
return the P argument from the previous call of the same function
on the same [database connection](../c3ref/sqlite3.html) D, or NULL for
the first call for each function on D.


The commit and rollback hook callbacks are not reentrant.
The callback implementation must not do anything that will modify
the database connection that invoked the callback. Any actions
to modify the database connection must be deferred until after the
completion of the [sqlite3\_step()](../c3ref/step.html) call that triggered the commit
or rollback hook in the first place.
Note that running any other SQL statements, including SELECT statements,
or merely calling [sqlite3\_prepare\_v2()](../c3ref/prepare.html) and [sqlite3\_step()](../c3ref/step.html) will modify
the database connections for the meaning of "modify" in this paragraph.


Registering a NULL function disables the callback.


When the commit hook callback routine returns zero, the [COMMIT](../lang_transaction.html)
operation is allowed to continue normally. If the commit hook
returns non\-zero, then the [COMMIT](../lang_transaction.html) is converted into a [ROLLBACK](../lang_transaction.html).
The rollback hook is invoked on a rollback that results from a commit
hook returning non\-zero, just as it would be with any other rollback.


For the purposes of this API, a transaction is said to have been
rolled back if an explicit "ROLLBACK" statement is executed, or
an error or constraint causes an implicit rollback to occur.
The rollback callback is not invoked if a transaction is
automatically rolled back because the database connection is closed.


See also the [sqlite3\_update\_hook()](../c3ref/update_hook.html) interface.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


