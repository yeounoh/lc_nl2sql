




Create An Iterator To Traverse A Changeset 




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Create An Iterator To Traverse A Changeset


> ```
> int sqlite3changeset_start(
>   sqlite3_changeset_iter **pp,    /* OUT: New changeset iterator handle */
>   int nChangeset,                 /* Size of changeset blob in bytes */
>   void *pChangeset                /* Pointer to blob containing changeset */
> );
> int sqlite3changeset_start_v2(
>   sqlite3_changeset_iter **pp,    /* OUT: New changeset iterator handle */
>   int nChangeset,                 /* Size of changeset blob in bytes */
>   void *pChangeset,               /* Pointer to blob containing changeset */
>   int flags                       /* SESSION_CHANGESETSTART_* flags */
> );
> 
> ```


Create an iterator used to iterate through the contents of a changeset.
If successful, \*pp is set to point to the iterator handle and SQLITE\_OK
is returned. Otherwise, if an error occurs, \*pp is set to zero and an
SQLite error code is returned.


The following functions can be used to advance and query a changeset 
iterator created by this function:


* [sqlite3changeset\_next()](../session/sqlite3changeset_next.html)* [sqlite3changeset\_op()](../session/sqlite3changeset_op.html)* [sqlite3changeset\_new()](../session/sqlite3changeset_new.html)* [sqlite3changeset\_old()](../session/sqlite3changeset_old.html)



It is the responsibility of the caller to eventually destroy the iterator
by passing it to [sqlite3changeset\_finalize()](../session/sqlite3changeset_finalize.html). The buffer containing the
changeset (pChangeset) must remain valid until after the iterator is
destroyed.


Assuming the changeset blob was created by one of the
[sqlite3session\_changeset()](../session/sqlite3session_changeset.html), [sqlite3changeset\_concat()](../session/sqlite3changeset_concat.html) or
[sqlite3changeset\_invert()](../session/sqlite3changeset_invert.html) functions, all changes within the changeset 
that apply to a single table are grouped together. This means that when 
an application iterates through a changeset using an iterator created by 
this function, all changes that relate to a single table are visited 
consecutively. There is no chance that the iterator will visit a change 
the applies to table X, then one for table Y, and then later on visit 
another change for table X.


The behavior of sqlite3changeset\_start\_v2() and its streaming equivalent
may be modified by passing a combination of
[supported flags](../session/c_changesetstart_invert.html) as the 4th parameter.


Note that the sqlite3changeset\_start\_v2() API is still **experimental**
and therefore subject to change.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


