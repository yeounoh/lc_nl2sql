




Set Or Clear the Indirect Change Flag




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Set Or Clear the Indirect Change Flag


> ```
> int sqlite3session_indirect(sqlite3_session *pSession, int bIndirect);
> 
> ```


Each change recorded by a session object is marked as either direct or
indirect. A change is marked as indirect if either:


* The session object "indirect" flag is set when the change is
 made, or
 * The change is made by an SQL trigger or foreign key action 
 instead of directly as a result of a users SQL statement.



If a single row is affected by more than one operation within a session,
then the change is considered indirect if all operations meet the criteria
for an indirect change above, or direct otherwise.


This function is used to set, clear or query the session object indirect
flag. If the second argument passed to this function is zero, then the
indirect flag is cleared. If it is greater than zero, the indirect flag
is set. Passing a value less than zero does not modify the current value
of the indirect flag, and may be used to query the current state of the 
indirect flag for the specified session object.


The return value indicates the final state of the indirect flag: 0 if 
it is clear, or 1 if it is set.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


