




Configure a changeset rebaser object.




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Configure a changeset rebaser object.


> ```
> int sqlite3rebaser_configure(
>   sqlite3_rebaser*, 
>   int nRebase, const void *pRebase
> ); 
> 
> ```

**Important:** This interface is [experimental](../c3ref/experimental.html) and is subject to change without notice.


Configure the changeset rebaser object to rebase changesets according
to the conflict resolutions described by buffer pRebase (size nRebase
bytes), which must have been obtained from a previous call to
sqlite3changeset\_apply\_v2().


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


