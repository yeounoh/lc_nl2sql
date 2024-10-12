




Create A New Changegroup Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Create A New Changegroup Object


> ```
> int sqlite3changegroup_new(sqlite3_changegroup **pp);
> 
> ```


An sqlite3\_changegroup object is used to combine two or more changesets
(or patchsets) into a single changeset (or patchset). A single changegroup
object may combine changesets or patchsets, but not both. The output is
always in the same format as the input.


If successful, this function returns SQLITE\_OK and populates (\*pp) with
a pointer to a new sqlite3\_changegroup object before returning. The caller
should eventually free the returned object using a call to 
sqlite3changegroup\_delete(). If an error occurs, an SQLite error code
(i.e. SQLITE\_NOMEM) is returned and \*pp is set to NULL.


The usual usage pattern for an sqlite3\_changegroup object is as follows:


* It is created using a call to sqlite3changegroup\_new().



 - Zero or more changesets (or patchsets) are added to the object
 by calling sqlite3changegroup\_add().



 - The result of combining all input changesets together is obtained 
 by the application via a call to sqlite3changegroup\_output().



 - The object is deleted using a call to sqlite3changegroup\_delete().



Any number of calls to add() and output() may be made between the calls to
new() and delete(), and in any order.


As well as the regular sqlite3changegroup\_add() and 
sqlite3changegroup\_output() functions, also available are the streaming
versions sqlite3changegroup\_add\_strm() and sqlite3changegroup\_output\_strm().


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


