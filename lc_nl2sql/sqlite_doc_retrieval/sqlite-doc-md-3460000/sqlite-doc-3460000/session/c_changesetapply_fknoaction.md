




Flags for sqlite3changeset\_apply\_v2




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Flags for sqlite3changeset\_apply\_v2


> ```
> #define SQLITE_CHANGESETAPPLY_NOSAVEPOINT   0x0001
> #define SQLITE_CHANGESETAPPLY_INVERT        0x0002
> #define SQLITE_CHANGESETAPPLY_IGNORENOOP    0x0004
> #define SQLITE_CHANGESETAPPLY_FKNOACTION    0x0008
> 
> ```


The following flags may passed via the 9th parameter to
[sqlite3changeset\_apply\_v2](../session/sqlite3changeset_apply.html) and [sqlite3changeset\_apply\_v2\_strm](../session/sqlite3changegroup_add_strm.html):



SQLITE\_CHANGESETAPPLY\_NOSAVEPOINT 
 Usually, the sessions module encloses all operations performed by
 a single call to apply\_v2() or apply\_v2\_strm() in a [SAVEPOINT](../lang_savepoint.html). The
 SAVEPOINT is committed if the changeset or patchset is successfully
 applied, or rolled back if an error occurs. Specifying this flag
 causes the sessions module to omit this savepoint. In this case, if the
 caller has an open transaction or savepoint when apply\_v2() is called, 
 it may revert the partially applied changeset by rolling it back.


SQLITE\_CHANGESETAPPLY\_INVERT 
 Invert the changeset before applying it. This is equivalent to inverting
 a changeset using sqlite3changeset\_invert() before applying it. It is
 an error to specify this flag with a patchset.


SQLITE\_CHANGESETAPPLY\_IGNORENOOP 
 Do not invoke the conflict handler callback for any changes that
 would not actually modify the database even if they were applied.
 Specifically, this means that the conflict handler is not invoked
 for:
 * a delete change if the row being deleted cannot be found, 
 * an update change if the modified fields are already set to 
 their new values in the conflicting row, or
 * an insert change if all fields of the conflicting row match
 the row being inserted.



SQLITE\_CHANGESETAPPLY\_FKNOACTION 
 If this flag it set, then all foreign key constraints in the target
 database behave as if they were declared with "ON UPDATE NO ACTION ON
 DELETE NO ACTION", even if they are actually CASCADE, RESTRICT, SET NULL
 or SET DEFAULT.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


