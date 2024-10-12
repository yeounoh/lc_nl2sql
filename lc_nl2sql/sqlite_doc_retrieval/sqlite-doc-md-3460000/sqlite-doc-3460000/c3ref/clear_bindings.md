




Reset All Bindings On A Prepared Statement




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Reset All Bindings On A Prepared Statement




> ```
> 
> int sqlite3_clear_bindings(sqlite3_stmt*);
> 
> ```



Contrary to the intuition of many, [sqlite3\_reset()](../c3ref/reset.html) does not reset
the [bindings](../c3ref/bind_blob.html) on a [prepared statement](../c3ref/stmt.html).
Use this routine to reset all host parameters to NULL.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


