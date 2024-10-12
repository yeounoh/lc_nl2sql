




Changegroup Handle




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Changegroup Handle


> ```
> typedef struct sqlite3_changegroup sqlite3_changegroup;
> 
> ```


A changegroup is an object used to combine two or more 
[changesets](../sessionintro.html#changeset) or [patchsets](../sessionintro.html#changeset)


Constructor: [sqlite3changegroup\_new()](../session/sqlite3changegroup_new.html)


Destructor: [sqlite3changegroup\_delete()](../session/sqlite3changegroup_delete.html)


Methods:
 [sqlite3changegroup\_add()](../session/sqlite3changegroup_add.html),
[sqlite3changegroup\_add\_change()](../session/sqlite3changegroup_add_change.html),
[sqlite3changegroup\_output()](../session/sqlite3changegroup_output.html)


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


