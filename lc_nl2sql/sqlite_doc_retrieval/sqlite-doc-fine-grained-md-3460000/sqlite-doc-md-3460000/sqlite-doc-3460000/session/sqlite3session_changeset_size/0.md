




Return An Upper\-limit For The Size Of The Changeset




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Return An Upper\-limit For The Size Of The Changeset


> ```
> sqlite3_int64 sqlite3session_changeset_size(sqlite3_session *pSession);
> 
> ```


By default, this function always returns 0\. For it to return
a useful result, the sqlite3\_session object must have been configured
to enable this API using sqlite3session\_object\_config() with the
SQLITE\_SESSION\_OBJCONFIG\_SIZE verb.


When enabled, this function returns an upper limit, in bytes, for the size 
of the changeset that might be produced if sqlite3session\_changeset() were
called. The final changeset size might be equal to or smaller than the
size in bytes returned by this function.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


