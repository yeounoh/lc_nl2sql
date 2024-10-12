




Obtain The Current Operation From A Changeset Iterator




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Obtain The Current Operation From A Changeset Iterator


> ```
> int sqlite3changeset_op(
>   sqlite3_changeset_iter *pIter,  /* Iterator object */
>   const char **pzTab,             /* OUT: Pointer to table name */
>   int *pnCol,                     /* OUT: Number of columns in table */
>   int *pOp,                       /* OUT: SQLITE_INSERT, DELETE or UPDATE */
>   int *pbIndirect                 /* OUT: True for an 'indirect' change */
> );
> 
> ```


The pIter argument passed to this function may either be an iterator
passed to a conflict\-handler by [sqlite3changeset\_apply()](../session/sqlite3changeset_apply.html), or an iterator
created by [sqlite3changeset\_start()](../session/sqlite3changeset_start.html). In the latter case, the most recent
call to [sqlite3changeset\_next()](../session/sqlite3changeset_next.html) must have returned [SQLITE\_ROW](../rescode.html#row). If this
is not the case, this function returns [SQLITE\_MISUSE](../rescode.html#misuse).


Arguments pOp, pnCol and pzTab may not be NULL. Upon return, three
outputs are set through these pointers: 


\*pOp is set to one of [SQLITE\_INSERT](../c3ref/c_alter_table.html), [SQLITE\_DELETE](../c3ref/c_alter_table.html) or [SQLITE\_UPDATE](../c3ref/c_alter_table.html),
depending on the type of change that the iterator currently points to;


\*pnCol is set to the number of columns in the table affected by the change; and


\*pzTab is set to point to a nul\-terminated utf\-8 encoded string containing
the name of the table affected by the current change. The buffer remains
valid until either sqlite3changeset\_next() is called on the iterator
or until the conflict\-handler function returns.


If pbIndirect is not NULL, then \*pbIndirect is set to true (1\) if the change
is an indirect change, or false (0\) otherwise. See the documentation for
[sqlite3session\_indirect()](../session/sqlite3session_indirect.html) for a description of direct and indirect
changes.


If no error occurs, SQLITE\_OK is returned. If an error does occur, an
SQLite error code is returned. The values of the output variables may not
be trusted in this case.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


