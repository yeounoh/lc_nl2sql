




Advance A Changeset Iterator




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Advance A Changeset Iterator


> ```
> int sqlite3changeset_next(sqlite3_changeset_iter *pIter);
> 
> ```


This function may only be used with iterators created by the function
[sqlite3changeset\_start()](../session/sqlite3changeset_start.html). If it is called on an iterator passed to
a conflict\-handler callback by [sqlite3changeset\_apply()](../session/sqlite3changeset_apply.html), SQLITE\_MISUSE
is returned and the call has no effect.


Immediately after an iterator is created by sqlite3changeset\_start(), it
does not point to any change in the changeset. Assuming the changeset
is not empty, the first call to this function advances the iterator to
point to the first change in the changeset. Each subsequent call advances
the iterator to point to the next change in the changeset (if any). If
no error occurs and the iterator points to a valid change after a call
to sqlite3changeset\_next() has advanced it, SQLITE\_ROW is returned. 
Otherwise, if all changes in the changeset have already been visited,
SQLITE\_DONE is returned.


If an error occurs, an SQLite error code is returned. Possible error 
codes include SQLITE\_CORRUPT (if the changeset buffer is corrupt) or 
SQLITE\_NOMEM.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


