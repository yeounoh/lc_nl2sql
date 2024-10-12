




Determine The Number Of Foreign Key Constraint Violations




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Determine The Number Of Foreign Key Constraint Violations


> ```
> int sqlite3changeset_fk_conflicts(
>   sqlite3_changeset_iter *pIter,  /* Changeset iterator */
>   int *pnOut                      /* OUT: Number of FK violations */
> );
> 
> ```


This function may only be called with an iterator passed to an
SQLITE\_CHANGESET\_FOREIGN\_KEY conflict handler callback. In this case
it sets the output variable to the total number of known foreign key
violations in the destination database and returns SQLITE\_OK.


In all other cases this function returns SQLITE\_MISUSE.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


