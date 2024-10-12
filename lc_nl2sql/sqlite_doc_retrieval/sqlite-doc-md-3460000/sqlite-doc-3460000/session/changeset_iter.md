




Changeset Iterator Handle




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Changeset Iterator Handle


> ```
> typedef struct sqlite3_changeset_iter sqlite3_changeset_iter;
> 
> ```


An instance of this object acts as a cursor for iterating
over the elements of a [changeset](../sessionintro.html#changeset) or [patchset](../sessionintro.html#changeset).


Constructors:
 [sqlite3changeset\_start()](../session/sqlite3changeset_start.html),
[sqlite3changeset\_start\_v2()](../session/sqlite3changeset_start.html)



* [sqlite3changeset\_conflict](../session/sqlite3changeset_conflict.html)
* [sqlite3changeset\_finalize](../session/sqlite3changeset_finalize.html)
* [sqlite3changeset\_fk\_conflicts](../session/sqlite3changeset_fk_conflicts.html)
* [sqlite3changeset\_new](../session/sqlite3changeset_new.html)
* [sqlite3changeset\_next](../session/sqlite3changeset_next.html)
* [sqlite3changeset\_old](../session/sqlite3changeset_old.html)
* [sqlite3changeset\_op](../session/sqlite3changeset_op.html)
* [sqlite3changeset\_pk](../session/sqlite3changeset_pk.html)




See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


