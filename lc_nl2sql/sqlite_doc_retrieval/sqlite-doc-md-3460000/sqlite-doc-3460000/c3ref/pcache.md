




Custom Page Cache Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Custom Page Cache Object




> ```
> 
> typedef struct sqlite3_pcache sqlite3_pcache;
> 
> ```



The sqlite3\_pcache type is opaque. It is implemented by
the pluggable module. The SQLite core has no knowledge of
its size or internal structure and never deals with the
sqlite3\_pcache object except by holding and passing pointers
to the object.


See [sqlite3\_pcache\_methods2](../c3ref/pcache_methods2.html) for additional information.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


