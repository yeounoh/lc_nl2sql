




Delete A Session Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Delete A Session Object


> ```
> void sqlite3session_delete(sqlite3_session *pSession);
> 
> ```


Delete a session object previously allocated using 
[sqlite3session\_create()](../session/sqlite3session_create.html). Once a session object has been deleted, the
results of attempting to use pSession with any other session module
function are undefined.


Session objects must be deleted before the database handle to which they
are attached is closed. Refer to the documentation for 
[sqlite3session\_create()](../session/sqlite3session_create.html) for details.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


