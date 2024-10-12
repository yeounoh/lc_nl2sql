




Upgrade the Schema of a Changeset/Patchset




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Upgrade the Schema of a Changeset/Patchset


> ```
> int sqlite3changeset_upgrade(
>   sqlite3 *db,
>   const char *zDb,
>   int nIn, const void *pIn,       /* Input changeset */
>   int *pnOut, void **ppOut        /* OUT: Inverse of input */
> );
> 
> ```

See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


