




Concatenate Two Changeset Objects




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Concatenate Two Changeset Objects


> ```
> int sqlite3changeset_concat(
>   int nA,                         /* Number of bytes in buffer pA */
>   void *pA,                       /* Pointer to buffer containing changeset A */
>   int nB,                         /* Number of bytes in buffer pB */
>   void *pB,                       /* Pointer to buffer containing changeset B */
>   int *pnOut,                     /* OUT: Number of bytes in output changeset */
>   void **ppOut                    /* OUT: Buffer containing output changeset */
> );
> 
> ```


This function is used to concatenate two changesets, A and B, into a 
single changeset. The result is a changeset equivalent to applying
changeset A followed by changeset B. 


This function combines the two input changesets using an 
sqlite3\_changegroup object. Calling it produces similar results as the
following code fragment:



```

  sqlite3_changegroup *pGrp;
  rc = sqlite3_changegroup_new(&pGrp);
  if( rc==SQLITE_OK ) rc = sqlite3changegroup_add(pGrp, nA, pA);
  if( rc==SQLITE_OK ) rc = sqlite3changegroup_add(pGrp, nB, pB);
  if( rc==SQLITE_OK ){
    rc = sqlite3changegroup_output(pGrp, pnOut, ppOut);
  }else{
    *ppOut = 0;
    *pnOut = 0;
  }

```



Refer to the sqlite3\_changegroup documentation below for details.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


