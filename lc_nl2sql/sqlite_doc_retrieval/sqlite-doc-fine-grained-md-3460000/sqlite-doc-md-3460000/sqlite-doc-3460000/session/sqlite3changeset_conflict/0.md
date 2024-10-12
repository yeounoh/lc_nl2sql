




Obtain Conflicting Row Values From A Changeset Iterator




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Obtain Conflicting Row Values From A Changeset Iterator


> ```
> int sqlite3changeset_conflict(
>   sqlite3_changeset_iter *pIter,  /* Changeset iterator */
>   int iVal,                       /* Column number */
>   sqlite3_value **ppValue         /* OUT: Value from conflicting row */
> );
> 
> ```


This function should only be used with iterator objects passed to a
conflict\-handler callback by [sqlite3changeset\_apply()](../session/sqlite3changeset_apply.html) with either
[SQLITE\_CHANGESET\_DATA](../session/c_changeset_conflict.html) or [SQLITE\_CHANGESET\_CONFLICT](../session/c_changeset_conflict.html). If this function
is called on any other iterator, [SQLITE\_MISUSE](../rescode.html#misuse) is returned and \*ppValue
is set to NULL.


Argument iVal must be greater than or equal to 0, and less than the number
of columns in the table affected by the current change. Otherwise,
[SQLITE\_RANGE](../rescode.html#range) is returned and \*ppValue is set to NULL.


If successful, this function sets \*ppValue to point to a protected
sqlite3\_value object containing the iVal'th value from the 
"conflicting row" associated with the current conflict\-handler callback
and returns SQLITE\_OK.


If some other error occurs (e.g. an OOM condition), an SQLite error code
is returned and \*ppValue is set to NULL.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


