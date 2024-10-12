




Obtain The Primary Key Definition Of A Table




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Obtain The Primary Key Definition Of A Table


> ```
> int sqlite3changeset_pk(
>   sqlite3_changeset_iter *pIter,  /* Iterator object */
>   unsigned char **pabPK,          /* OUT: Array of boolean - true for PK cols */
>   int *pnCol                      /* OUT: Number of entries in output array */
> );
> 
> ```


For each modified table, a changeset includes the following:


* The number of columns in the table, and
 * Which of those columns make up the tables PRIMARY KEY.



This function is used to find which columns comprise the PRIMARY KEY of
the table modified by the change that iterator pIter currently points to.
If successful, \*pabPK is set to point to an array of nCol entries, where
nCol is the number of columns in the table. Elements of \*pabPK are set to
0x01 if the corresponding column is part of the tables primary key, or
0x00 if it is not.


If argument pnCol is not NULL, then \*pnCol is set to the number of columns
in the table.


If this function is called when the iterator does not point to a valid
entry, SQLITE\_MISUSE is returned and the output variables zeroed. Otherwise,
SQLITE\_OK is returned and the output variables populated as described
above.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


