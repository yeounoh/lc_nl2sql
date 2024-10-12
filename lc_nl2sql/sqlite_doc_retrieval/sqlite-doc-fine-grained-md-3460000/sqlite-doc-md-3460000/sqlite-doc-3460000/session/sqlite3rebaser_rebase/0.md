




Rebase a changeset




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Rebase a changeset


> ```
> int sqlite3rebaser_rebase(
>   sqlite3_rebaser*,
>   int nIn, const void *pIn, 
>   int *pnOut, void **ppOut 
> );
> 
> ```

**Important:** This interface is [experimental](../c3ref/experimental.html) and is subject to change without notice.


Argument pIn must point to a buffer containing a changeset nIn bytes
in size. This function allocates and populates a buffer with a copy
of the changeset rebased according to the configuration of the
rebaser object passed as the first argument. If successful, (\*ppOut)
is set to point to the new buffer containing the rebased changeset and 
(\*pnOut) to its size in bytes and SQLITE\_OK returned. It is the
responsibility of the caller to eventually free the new buffer using
sqlite3\_free(). Otherwise, if an error occurs, (\*ppOut) and (\*pnOut)
are set to zero and an SQLite error code returned.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


