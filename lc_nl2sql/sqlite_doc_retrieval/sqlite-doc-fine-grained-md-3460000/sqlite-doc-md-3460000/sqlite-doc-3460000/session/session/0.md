




Session Object Handle




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Session Object Handle


> ```
> typedef struct sqlite3_session sqlite3_session;
> 
> ```


An instance of this object is a [session](../sessionintro.html) that can be used to
record changes to a database.


Constructor: [sqlite3session\_create()](../session/sqlite3session_create.html)


Destructor: [sqlite3session\_delete()](../session/sqlite3session_delete.html)



* [sqlite3session\_attach](../session/sqlite3session_attach.html)
* [sqlite3session\_changeset](../session/sqlite3session_changeset.html)
* [sqlite3session\_changeset\_size](../session/sqlite3session_changeset_size.html)
* [sqlite3session\_diff](../session/sqlite3session_diff.html)
* [sqlite3session\_enable](../session/sqlite3session_enable.html)
* [sqlite3session\_indirect](../session/sqlite3session_indirect.html)
* [sqlite3session\_object\_config](../session/sqlite3session_object_config.html)
* [sqlite3session\_patchset](../session/sqlite3session_patchset.html)
* [sqlite3session\_table\_filter](../session/sqlite3session_table_filter.html)




See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


