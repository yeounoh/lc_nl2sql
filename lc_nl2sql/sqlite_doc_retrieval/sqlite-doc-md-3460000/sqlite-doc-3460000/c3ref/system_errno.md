




Low\-level system error code




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Low\-level system error code




> ```
> 
> int sqlite3_system_errno(sqlite3*);
> 
> ```



Attempt to return the underlying operating system error code or error
number that caused the most recent I/O error or failure to open a file.
The return value is OS\-dependent. For example, on unix systems, after
[sqlite3\_open\_v2()](../c3ref/open.html) returns [SQLITE\_CANTOPEN](../rescode.html#cantopen), this interface could be
called to get back the underlying "errno" that caused the problem, such
as ENOSPC, EAUTH, EISDIR, and so forth.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


