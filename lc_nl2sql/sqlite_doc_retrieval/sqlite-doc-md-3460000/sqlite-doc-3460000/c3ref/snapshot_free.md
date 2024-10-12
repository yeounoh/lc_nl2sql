




Destroy a snapshot




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Destroy a snapshot




> ```
> 
> void sqlite3_snapshot_free(sqlite3_snapshot*);
> 
> ```



The [sqlite3\_snapshot\_free(P)](../c3ref/snapshot_free.html) interface destroys [sqlite3\_snapshot](../c3ref/snapshot.html) P.
The application must eventually free every [sqlite3\_snapshot](../c3ref/snapshot.html) object
using this routine to avoid a memory leak.


The [sqlite3\_snapshot\_free()](../c3ref/snapshot_free.html) interface is only available when the
[SQLITE\_ENABLE\_SNAPSHOT](../compile.html#enable_snapshot) compile\-time option is used.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


