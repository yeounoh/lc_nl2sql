




Obtain old.\* Values From A Changeset Iterator




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Obtain old.\* Values From A Changeset Iterator


> ```
> int sqlite3changeset_old(
>   sqlite3_changeset_iter *pIter,  /* Changeset iterator */
>   int iVal,                       /* Column number */
>   sqlite3_value **ppValue         /* OUT: Old value (or NULL pointer) */
> );
> 
> ```


The pIter argument passed to this function may either be an iterator
passed to a conflict\-handler by [sqlite3changeset\_apply()](../session/sqlite3changeset_apply.html), or an iterator
created by [sqlite3changeset\_start()](../session/sqlite3changeset_start.html). In the latter case, the most recent
call to [sqlite3changeset\_next()](../session/sqlite3changeset_next.html) must have returned SQLITE\_ROW. 
Furthermore, it may only be called if the type of change that the iterator
currently points to is either [SQLITE\_DELETE](../c3ref/c_alter_table.html) or [SQLITE\_UPDATE](../c3ref/c_alter_table.html). Otherwise,
this function returns [SQLITE\_MISUSE](../rescode.html#misuse) and sets \*ppValue to NULL.


Argument iVal must be greater than or equal to 0, and less than the number
of columns in the table affected by the current change. Otherwise,
[SQLITE\_RANGE](../rescode.html#range) is returned and \*ppValue is set to NULL.


If successful, this function sets \*ppValue to point to a protected
sqlite3\_value object containing the iVal'th value from the vector of 
original row values stored as part of the UPDATE or DELETE change and
returns SQLITE\_OK. The name of the function comes from the fact that this 
is similar to the "old.\*" columns available to update or delete triggers.


If some other error occurs (e.g. an OOM condition), an SQLite error code
is returned and \*ppValue is set to NULL.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


