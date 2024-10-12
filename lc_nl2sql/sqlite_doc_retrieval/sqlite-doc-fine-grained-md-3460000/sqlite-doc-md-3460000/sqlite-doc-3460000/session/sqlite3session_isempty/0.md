




Test if a changeset has recorded any changes.




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Test if a changeset has recorded any changes.


> ```
> int sqlite3session_isempty(sqlite3_session *pSession);
> 
> ```


Return non\-zero if no changes to attached tables have been recorded by 
the session object passed as the first argument. Otherwise, if one or 
more changes have been recorded, return zero.


Even if this function returns zero, it is possible that calling
[sqlite3session\_changeset()](../session/sqlite3session_changeset.html) on the session handle may still return a
changeset that contains no changes. This can happen when a row in 
an attached table is modified and then later on the original values 
are restored. However, if this function returns non\-zero, then it is
guaranteed that a call to sqlite3session\_changeset() will return a 
changeset containing zero changes.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


