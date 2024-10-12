




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
> typedef struct sqlite3_pcache_page sqlite3_pcache_page;
> struct sqlite3_pcache_page {
>   void *pBuf;        /* The content of the page */
>   void *pExtra;      /* Extra information associated with the page */
> };
> 
> ```



The sqlite3\_pcache\_page object represents a single page in the
page cache. The page cache will allocate instances of this
object. Various methods of the page cache use pointers to instances
of this object as parameters or as their return value.


See [sqlite3\_pcache\_methods2](../c3ref/pcache_methods2.html) for additional information.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


