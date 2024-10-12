




Reset A Prepared Statement Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Reset A Prepared Statement Object




> ```
> 
> int sqlite3_reset(sqlite3_stmt *pStmt);
> 
> ```



The sqlite3\_reset() function is called to reset a [prepared statement](../c3ref/stmt.html)
object back to its initial state, ready to be re\-executed.
Any SQL statement variables that had values bound to them using
the [sqlite3\_bind\_\*() API](../c3ref/bind_blob.html) retain their values.
Use [sqlite3\_clear\_bindings()](../c3ref/clear_bindings.html) to reset the bindings.


The [sqlite3\_reset(S)](../c3ref/reset.html) interface resets the [prepared statement](../c3ref/stmt.html) S
back to the beginning of its program.


The return code from [sqlite3\_reset(S)](../c3ref/reset.html) indicates whether or not
the previous evaluation of prepared statement S completed successfully.
If [sqlite3\_step(S)](../c3ref/step.html) has never before been called on S or if
[sqlite3\_step(S)](../c3ref/step.html) has not been called since the previous call
to [sqlite3\_reset(S)](../c3ref/reset.html), then [sqlite3\_reset(S)](../c3ref/reset.html) will return
[SQLITE\_OK](../rescode.html#ok).


If the most recent call to [sqlite3\_step(S)](../c3ref/step.html) for the
[prepared statement](../c3ref/stmt.html) S indicated an error, then
[sqlite3\_reset(S)](../c3ref/reset.html) returns an appropriate [error code](../rescode.html).
The [sqlite3\_reset(S)](../c3ref/reset.html) interface might also return an [error code](../rescode.html)
if there were no prior errors but the process of resetting
the prepared statement caused a new error. For example, if an
[INSERT](../lang_insert.html) statement with a [RETURNING](../lang_returning.html) clause is only stepped one time,
that one call to [sqlite3\_step(S)](../c3ref/step.html) might return SQLITE\_ROW but
the overall statement might still fail and the [sqlite3\_reset(S)](../c3ref/reset.html) call
might return SQLITE\_BUSY if locking constraints prevent the
database change from committing. Therefore, it is important that
applications check the return code from [sqlite3\_reset(S)](../c3ref/reset.html) even if
no prior call to [sqlite3\_step(S)](../c3ref/step.html) indicated a problem.


The [sqlite3\_reset(S)](../c3ref/reset.html) interface does not change the values
of any [bindings](../c3ref/bind_blob.html) on the [prepared statement](../c3ref/stmt.html) S.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


