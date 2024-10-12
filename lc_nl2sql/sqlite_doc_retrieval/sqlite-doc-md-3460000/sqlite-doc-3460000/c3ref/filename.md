




File Name




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## File Name




> ```
> 
> typedef const char *sqlite3_filename;
> 
> ```



Type [sqlite3\_filename](../c3ref/filename.html) is used by SQLite to pass filenames to the
xOpen method of a [VFS](../vfs.html). It may be cast to (const char\*) and treated
as a normal, nul\-terminated, UTF\-8 buffer containing the filename, but
may also be passed to special APIs such as:


* sqlite3\_filename\_database()
* sqlite3\_filename\_journal()
* sqlite3\_filename\_wal()
* sqlite3\_uri\_parameter()
* sqlite3\_uri\_boolean()
* sqlite3\_uri\_int64()
* sqlite3\_uri\_key()




See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


