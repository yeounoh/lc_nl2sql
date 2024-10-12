




Finalize A Changeset Iterator




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Finalize A Changeset Iterator


> ```
> int sqlite3changeset_finalize(sqlite3_changeset_iter *pIter);
> 
> ```


This function is used to finalize an iterator allocated with
[sqlite3changeset\_start()](../session/sqlite3changeset_start.html).


This function should only be called on iterators created using the
[sqlite3changeset\_start()](../session/sqlite3changeset_start.html) function. If an application calls this
function with an iterator passed to a conflict\-handler by
[sqlite3changeset\_apply()](../session/sqlite3changeset_apply.html), [SQLITE\_MISUSE](../rescode.html#misuse) is immediately returned and the
call has no effect.


If an error was encountered within a call to an sqlite3changeset\_xxx()
function (for example an [SQLITE\_CORRUPT](../rescode.html#corrupt) in [sqlite3changeset\_next()](../session/sqlite3changeset_next.html) or an 
[SQLITE\_NOMEM](../rescode.html#nomem) in [sqlite3changeset\_new()](../session/sqlite3changeset_new.html)) then an error code corresponding
to that error is returned by this function. Otherwise, SQLITE\_OK is
returned. This is to allow the following pattern (pseudo\-code):



```

  sqlite3changeset_start();
  while( SQLITE_ROW==sqlite3changeset_next() ){
    // Do something with change.
  }
  rc = sqlite3changeset_finalize();
  if( rc!=SQLITE_OK ){
    // An error has occurred 
  }

```



See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


