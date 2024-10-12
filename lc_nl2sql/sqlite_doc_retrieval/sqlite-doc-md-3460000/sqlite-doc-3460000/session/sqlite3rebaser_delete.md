




Delete a changeset rebaser object.




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Delete a changeset rebaser object.


> ```
> void sqlite3rebaser_delete(sqlite3_rebaser *p); 
> 
> ```

**Important:** This interface is [experimental](../c3ref/experimental.html) and is subject to change without notice.


Delete the changeset rebaser object and all associated resources. There
should be one call to this function for each successful invocation
of sqlite3rebaser\_create().


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


