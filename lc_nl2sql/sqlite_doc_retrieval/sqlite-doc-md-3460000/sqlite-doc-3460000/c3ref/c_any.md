




Text Encodings




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Text Encodings




> ```
> 
> #define SQLITE_UTF8           1    /* IMP: R-37514-35566 */
> #define SQLITE_UTF16LE        2    /* IMP: R-03371-37637 */
> #define SQLITE_UTF16BE        3    /* IMP: R-51971-34154 */
> #define SQLITE_UTF16          4    /* Use native byte order */
> #define SQLITE_ANY            5    /* Deprecated */
> #define SQLITE_UTF16_ALIGNED  8    /* sqlite3_create_collation only */
> 
> ```



These constant define integer codes that represent the various
text encodings supported by SQLite.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


