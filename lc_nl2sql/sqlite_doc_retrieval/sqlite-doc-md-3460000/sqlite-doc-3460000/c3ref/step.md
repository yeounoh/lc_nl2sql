




Evaluate An SQL Statement




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Evaluate An SQL Statement




> ```
> 
> int sqlite3_step(sqlite3_stmt*);
> 
> ```



After a [prepared statement](../c3ref/stmt.html) has been prepared using any of
[sqlite3\_prepare\_v2()](../c3ref/prepare.html), [sqlite3\_prepare\_v3()](../c3ref/prepare.html), [sqlite3\_prepare16\_v2()](../c3ref/prepare.html),
or [sqlite3\_prepare16\_v3()](../c3ref/prepare.html) or one of the legacy
interfaces [sqlite3\_prepare()](../c3ref/prepare.html) or [sqlite3\_prepare16()](../c3ref/prepare.html), this function
must be called one or more times to evaluate the statement.


The details of the behavior of the sqlite3\_step() interface depend
on whether the statement was prepared using the newer "vX" interfaces
[sqlite3\_prepare\_v3()](../c3ref/prepare.html), [sqlite3\_prepare\_v2()](../c3ref/prepare.html), [sqlite3\_prepare16\_v3()](../c3ref/prepare.html),
[sqlite3\_prepare16\_v2()](../c3ref/prepare.html) or the older legacy
interfaces [sqlite3\_prepare()](../c3ref/prepare.html) and [sqlite3\_prepare16()](../c3ref/prepare.html). The use of the
new "vX" interface is recommended for new applications but the legacy
interface will continue to be supported.


In the legacy interface, the return value will be either [SQLITE\_BUSY](../rescode.html#busy),
[SQLITE\_DONE](../rescode.html#done), [SQLITE\_ROW](../rescode.html#row), [SQLITE\_ERROR](../rescode.html#error), or [SQLITE\_MISUSE](../rescode.html#misuse).
With the "v2" interface, any of the other [result codes](../rescode.html) or
[extended result codes](../rescode.html#extrc) might be returned as well.


[SQLITE\_BUSY](../rescode.html#busy) means that the database engine was unable to acquire the
database locks it needs to do its job. If the statement is a [COMMIT](../lang_transaction.html)
or occurs outside of an explicit transaction, then you can retry the
statement. If the statement is not a [COMMIT](../lang_transaction.html) and occurs within an
explicit transaction then you should rollback the transaction before
continuing.


[SQLITE\_DONE](../rescode.html#done) means that the statement has finished executing
successfully. sqlite3\_step() should not be called again on this virtual
machine without first calling [sqlite3\_reset()](../c3ref/reset.html) to reset the virtual
machine back to its initial state.


If the SQL statement being executed returns any data, then [SQLITE\_ROW](../rescode.html#row)
is returned each time a new row of data is ready for processing by the
caller. The values may be accessed using the [column access functions](../c3ref/column_blob.html).
sqlite3\_step() is called again to retrieve the next row of data.


[SQLITE\_ERROR](../rescode.html#error) means that a run\-time error (such as a constraint
violation) has occurred. sqlite3\_step() should not be called again on
the VM. More information may be found by calling [sqlite3\_errmsg()](../c3ref/errcode.html).
With the legacy interface, a more specific error code (for example,
[SQLITE\_INTERRUPT](../rescode.html#interrupt), [SQLITE\_SCHEMA](../rescode.html#schema), [SQLITE\_CORRUPT](../rescode.html#corrupt), and so forth)
can be obtained by calling [sqlite3\_reset()](../c3ref/reset.html) on the
[prepared statement](../c3ref/stmt.html). In the "v2" interface,
the more specific error code is returned directly by sqlite3\_step().


[SQLITE\_MISUSE](../rescode.html#misuse) means that the this routine was called inappropriately.
Perhaps it was called on a [prepared statement](../c3ref/stmt.html) that has
already been [finalized](../c3ref/finalize.html) or on one that had
previously returned [SQLITE\_ERROR](../rescode.html#error) or [SQLITE\_DONE](../rescode.html#done). Or it could
be the case that the same database connection is being used by two or
more threads at the same moment in time.


For all versions of SQLite up to and including 3\.6\.23\.1, a call to
[sqlite3\_reset()](../c3ref/reset.html) was required after sqlite3\_step() returned anything
other than [SQLITE\_ROW](../rescode.html#row) before any subsequent invocation of
sqlite3\_step(). Failure to reset the prepared statement using
[sqlite3\_reset()](../c3ref/reset.html) would result in an [SQLITE\_MISUSE](../rescode.html#misuse) return from
sqlite3\_step(). But after [version 3\.6\.23\.1](../releaselog/3_6_23_1.html) (2010\-03\-26,
sqlite3\_step() began
calling [sqlite3\_reset()](../c3ref/reset.html) automatically in this circumstance rather
than returning [SQLITE\_MISUSE](../rescode.html#misuse). This is not considered a compatibility
break because any application that ever receives an SQLITE\_MISUSE error
is broken by definition. The [SQLITE\_OMIT\_AUTORESET](../compile.html#omit_autoreset) compile\-time option
can be used to restore the legacy behavior.


**Goofy Interface Alert:** In the legacy interface, the sqlite3\_step()
API always returns a generic error code, [SQLITE\_ERROR](../rescode.html#error), following any
error other than [SQLITE\_BUSY](../rescode.html#busy) and [SQLITE\_MISUSE](../rescode.html#misuse). You must call
[sqlite3\_reset()](../c3ref/reset.html) or [sqlite3\_finalize()](../c3ref/finalize.html) in order to find one of the
specific [error codes](../rescode.html) that better describes the error.
We admit that this is a goofy design. The problem has been fixed
with the "v2" interface. If you prepare all of your SQL statements
using [sqlite3\_prepare\_v3()](../c3ref/prepare.html) or [sqlite3\_prepare\_v2()](../c3ref/prepare.html)
or [sqlite3\_prepare16\_v2()](../c3ref/prepare.html) or [sqlite3\_prepare16\_v3()](../c3ref/prepare.html) instead
of the legacy [sqlite3\_prepare()](../c3ref/prepare.html) and [sqlite3\_prepare16()](../c3ref/prepare.html) interfaces,
then the more specific [error codes](../rescode.html) are returned directly
by sqlite3\_step(). The use of the "vX" interfaces is recommended.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


