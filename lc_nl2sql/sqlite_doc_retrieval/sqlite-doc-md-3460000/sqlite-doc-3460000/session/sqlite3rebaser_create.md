




Create a changeset rebaser object.




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Create a changeset rebaser object.


> ```
> int sqlite3rebaser_create(sqlite3_rebaser **ppNew);
> 
> ```

**Important:** This interface is [experimental](../c3ref/experimental.html) and is subject to change without notice.


Allocate a new changeset rebaser object. If successful, set (\*ppNew) to
point to the new object and return SQLITE\_OK. Otherwise, if an error
occurs, return an SQLite error code (e.g. SQLITE\_NOMEM) and set (\*ppNew) 
to NULL. 


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


