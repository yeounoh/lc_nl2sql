




Authorizer Return Codes




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Authorizer Return Codes




> ```
> 
> #define SQLITE_DENY   1   /* Abort the SQL statement with an error */
> #define SQLITE_IGNORE 2   /* Don't allow access, but don't generate an error */
> 
> ```



The [authorizer callback function](../c3ref/set_authorizer.html) must
return either [SQLITE\_OK](../rescode.html#ok) or one of these two constants in order
to signal SQLite whether or not the action is permitted. See the
[authorizer documentation](../c3ref/set_authorizer.html) for additional
information.


Note that SQLITE\_IGNORE is also used as a [conflict resolution mode](../c3ref/c_fail.html)
returned from the [sqlite3\_vtab\_on\_conflict()](../c3ref/vtab_on_conflict.html) interface.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


