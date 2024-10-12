




Database Connection Client Data




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Database Connection Client Data




> ```
> 
> void *sqlite3_get_clientdata(sqlite3*,const char*);
> int sqlite3_set_clientdata(sqlite3*, const char*, void*, void(*)(void*));
> 
> ```



These functions are used to associate one or more named pointers
with a [database connection](../c3ref/sqlite3.html).
A call to sqlite3\_set\_clientdata(D,N,P,X) causes the pointer P
to be attached to [database connection](../c3ref/sqlite3.html) D using name N. Subsequent
calls to sqlite3\_get\_clientdata(D,N) will return a copy of pointer P
or a NULL pointer if there were no prior calls to
sqlite3\_set\_clientdata() with the same values of D and N.
Names are compared using strcmp() and are thus case sensitive.


If P and X are both non\-NULL, then the destructor X is invoked with
argument P on the first of the following occurrences:
* An out\-of\-memory error occurs during the call to
sqlite3\_set\_clientdata() which attempts to register pointer P.
* A subsequent call to sqlite3\_set\_clientdata(D,N,P,X) is made
with the same D and N parameters.
* The database connection closes. SQLite does not make any guarantees
about the order in which destructors are called, only that all
destructors will be called exactly once at some point during the
database connection closing process.



SQLite does not do anything with client data other than invoke
destructors on the client data at the appropriate time. The intended
use for client data is to provide a mechanism for wrapper libraries
to store additional information about an SQLite database connection.


There is no limit (other than available memory) on the number of different
client data pointers (with different names) that can be attached to a
single database connection. However, the implementation is optimized
for the case of having only one or two different client data names.
Applications and wrapper libraries are discouraged from using more than
one client data name each.


There is no way to enumerate the client data pointers
associated with a database connection. The N parameter can be thought
of as a secret key such that only code that knows the secret key is able
to access the associated data.


Security Warning: These interfaces should not be exposed in scripting
languages or in other circumstances where it might be possible for an
an attacker to invoke them. Any agent that can invoke these interfaces
can probably also take control of the process.


Database connection client data is only available for SQLite
version 3\.44\.0 (2023\-11\-01\) and later.


See also: [sqlite3\_set\_auxdata()](../c3ref/get_auxdata.html) and [sqlite3\_get\_auxdata()](../c3ref/get_auxdata.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


