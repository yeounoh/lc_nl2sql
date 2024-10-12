




Rebasing changesets




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Rebasing changesets


> ```
> typedef struct sqlite3_rebaser sqlite3_rebaser;
> 
> ```

**Important:** This interface is [experimental](../c3ref/experimental.html) and is subject to change without notice.


Suppose there is a site hosting a database in state S0\. And that
modifications are made that move that database to state S1 and a
changeset recorded (the "local" changeset). Then, a changeset based
on S0 is received from another site (the "remote" changeset) and 
applied to the database. The database is then in state 
(S1\+"remote"), where the exact state depends on any conflict
resolution decisions (OMIT or REPLACE) made while applying "remote".
Rebasing a changeset is to update it to take those conflict 
resolution decisions into account, so that the same conflicts
do not have to be resolved elsewhere in the network. 


For example, if both the local and remote changesets contain an
INSERT of the same key on "CREATE TABLE t1(a PRIMARY KEY, b)":


 local: INSERT INTO t1 VALUES(1, 'v1');
 remote: INSERT INTO t1 VALUES(1, 'v2');


and the conflict resolution is REPLACE, then the INSERT change is
removed from the local changeset (it was overridden). Or, if the
conflict resolution was "OMIT", then the local changeset is modified
to instead contain:


 UPDATE t1 SET b \= 'v2' WHERE a\=1;


Changes within the local changeset are rebased as follows:



Local INSERT
 This may only conflict with a remote INSERT. If the conflict 
 resolution was OMIT, then add an UPDATE change to the rebased
 changeset. Or, if the conflict resolution was REPLACE, add
 nothing to the rebased changeset.


Local DELETE
 This may conflict with a remote UPDATE or DELETE. In both cases the
 only possible resolution is OMIT. If the remote operation was a
 DELETE, then add no change to the rebased changeset. If the remote
 operation was an UPDATE, then the old.\* fields of change are updated
 to reflect the new.\* values in the UPDATE.


Local UPDATE
 This may conflict with a remote UPDATE or DELETE. If it conflicts
 with a DELETE, and the conflict resolution was OMIT, then the update
 is changed into an INSERT. Any undefined values in the new.\* record
 from the update change are filled in using the old.\* values from
 the conflicting DELETE. Or, if the conflict resolution was REPLACE,
 the UPDATE change is simply omitted from the rebased changeset.


 If conflict is with a remote UPDATE and the resolution is OMIT, then
 the old.\* values are rebased using the new.\* values in the remote
 change. Or, if the resolution is REPLACE, then the change is copied
 into the rebased changeset with updates to columns also updated by
 the conflicting remote UPDATE removed. If this means no columns would 
 be updated, the change is omitted.



A local change may be rebased against multiple remote changes 
simultaneously. If a single key is modified by multiple remote 
changesets, they are combined as follows before the local changeset
is rebased:


* If there has been one or more REPLACE resolutions on a
 key, it is rebased according to a REPLACE.



 - If there have been no REPLACE resolutions on a key, then
 the local changeset is rebased according to the most recent
 of the OMIT resolutions.



Note that conflict resolutions from multiple remote changesets are 
combined on a per\-field basis, not per\-row. This means that in the 
case of multiple remote UPDATE operations, some fields of a single 
local change may be rebased for REPLACE while others are rebased for 
OMIT.


In order to rebase a local changeset, the remote changeset must first
be applied to the local database using sqlite3changeset\_apply\_v2() and
the buffer of rebase information captured. Then:


1. An sqlite3\_rebaser object is created by calling 
 sqlite3rebaser\_create().
 - The new object is configured with the rebase buffer obtained from
 sqlite3changeset\_apply\_v2() by calling sqlite3rebaser\_configure().
 If the local changeset is to be rebased against multiple remote
 changesets, then sqlite3rebaser\_configure() should be called
 multiple times, in the same order that the multiple
 sqlite3changeset\_apply\_v2() calls were made.
 - Each local changeset is rebased by calling sqlite3rebaser\_rebase().
 - The sqlite3\_rebaser object is deleted by calling
 sqlite3rebaser\_delete().




See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


