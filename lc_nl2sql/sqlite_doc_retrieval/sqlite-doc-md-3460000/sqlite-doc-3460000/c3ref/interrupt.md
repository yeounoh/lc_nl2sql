




Interrupt A Long\-Running Query




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Interrupt A Long\-Running Query




> ```
> 
> void sqlite3_interrupt(sqlite3*);
> int sqlite3_is_interrupted(sqlite3*);
> 
> ```



This function causes any pending database operation to abort and
return at its earliest opportunity. This routine is typically
called in response to a user action such as pressing "Cancel"
or Ctrl\-C where the user wants a long query operation to halt
immediately.


It is safe to call this routine from a thread different from the
thread that is currently running the database operation. But it
is not safe to call this routine with a [database connection](../c3ref/sqlite3.html) that
is closed or might close before sqlite3\_interrupt() returns.


If an SQL operation is very nearly finished at the time when
sqlite3\_interrupt() is called, then it might not have an opportunity
to be interrupted and might continue to completion.


An SQL operation that is interrupted will return [SQLITE\_INTERRUPT](../rescode.html#interrupt).
If the interrupted SQL operation is an INSERT, UPDATE, or DELETE
that is inside an explicit transaction, then the entire transaction
will be rolled back automatically.


The sqlite3\_interrupt(D) call is in effect until all currently running
SQL statements on [database connection](../c3ref/sqlite3.html) D complete. Any new SQL statements
that are started after the sqlite3\_interrupt() call and before the
running statement count reaches zero are interrupted as if they had been
running prior to the sqlite3\_interrupt() call. New SQL statements
that are started after the running statement count reaches zero are
not effected by the sqlite3\_interrupt().
A call to sqlite3\_interrupt(D) that occurs when there are no running
SQL statements is a no\-op and has no effect on SQL statements
that are started after the sqlite3\_interrupt() call returns.


The [sqlite3\_is\_interrupted(D)](../c3ref/interrupt.html) interface can be used to determine whether
or not an interrupt is currently in effect for [database connection](../c3ref/sqlite3.html) D.
It returns 1 if an interrupt is currently in effect, or 0 otherwise.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


