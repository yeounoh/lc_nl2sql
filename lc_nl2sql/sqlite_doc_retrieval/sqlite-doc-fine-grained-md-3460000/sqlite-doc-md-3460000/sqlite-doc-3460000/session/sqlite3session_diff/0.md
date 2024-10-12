




Load The Difference Between Tables Into A Session




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Load The Difference Between Tables Into A Session


> ```
> int sqlite3session_diff(
>   sqlite3_session *pSession,
>   const char *zFromDb,
>   const char *zTbl,
>   char **pzErrMsg
> );
> 
> ```


If it is not already attached to the session object passed as the first
argument, this function attaches table zTbl in the same manner as the
[sqlite3session\_attach()](../session/sqlite3session_attach.html) function. If zTbl does not exist, or if it
does not have a primary key, this function is a no\-op (but does not return
an error).


Argument zFromDb must be the name of a database ("main", "temp" etc.)
attached to the same database handle as the session object that contains 
a table compatible with the table attached to the session by this function.
A table is considered compatible if it:


* Has the same name,
 * Has the same set of columns declared in the same order, and
 * Has the same PRIMARY KEY definition.



If the tables are not compatible, SQLITE\_SCHEMA is returned. If the tables
are compatible but do not have any PRIMARY KEY columns, it is not an error
but no changes are added to the session object. As with other session
APIs, tables without PRIMARY KEYs are simply ignored.


This function adds a set of changes to the session object that could be
used to update the table in database zFrom (call this the "from\-table") 
so that its content is the same as the table attached to the session 
object (call this the "to\-table"). Specifically:


* For each row (primary key) that exists in the to\-table but not in 
 the from\-table, an INSERT record is added to the session object.



 - For each row (primary key) that exists in the to\-table but not in 
 the from\-table, a DELETE record is added to the session object.



 - For each row (primary key) that exists in both tables, but features 
 different non\-PK values in each, an UPDATE record is added to the
 session.



To clarify, if this function is called and then a changeset constructed
using [sqlite3session\_changeset()](../session/sqlite3session_changeset.html), then after applying that changeset to 
database zFrom the contents of the two compatible tables would be 
identical.


It an error if database zFrom does not exist or does not contain the
required compatible table.


If the operation is successful, SQLITE\_OK is returned. Otherwise, an SQLite
error code. In this case, if argument pzErrMsg is not NULL, \*pzErrMsg
may be set to point to a buffer containing an English language error 
message. It is the responsibility of the caller to free this buffer using
sqlite3\_free().


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


