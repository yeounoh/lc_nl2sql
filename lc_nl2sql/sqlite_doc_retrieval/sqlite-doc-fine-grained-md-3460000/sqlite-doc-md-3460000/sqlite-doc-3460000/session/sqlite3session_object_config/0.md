




Configure a Session Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Configure a Session Object


> ```
> int sqlite3session_object_config(sqlite3_session*, int op, void *pArg);
> 
> ```


This method is used to configure a session object after it has been
created. At present the only valid values for the second parameter are
[SQLITE\_SESSION\_OBJCONFIG\_SIZE](../session/c_session_objconfig_rowid.html) and [SQLITE\_SESSION\_OBJCONFIG\_ROWID](../session/c_session_objconfig_rowid.html).


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


