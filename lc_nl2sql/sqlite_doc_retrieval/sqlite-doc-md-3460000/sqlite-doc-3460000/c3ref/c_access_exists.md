




Flags for the xAccess VFS method




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Flags for the xAccess VFS method




> ```
> 
> #define SQLITE_ACCESS_EXISTS    0
> #define SQLITE_ACCESS_READWRITE 1   /* Used by PRAGMA temp_store_directory */
> #define SQLITE_ACCESS_READ      2   /* Unused */
> 
> ```



These integer constants can be used as the third parameter to
the xAccess method of an [sqlite3\_vfs](../c3ref/vfs.html) object. They determine
what kind of permissions the xAccess method is looking for.
With SQLITE\_ACCESS\_EXISTS, the xAccess method
simply checks whether the file exists.
With SQLITE\_ACCESS\_READWRITE, the xAccess method
checks whether the named directory is both readable and writable
(in other words, if files can be added, removed, and renamed within
the directory).
The SQLITE\_ACCESS\_READWRITE constant is currently used only by the
[temp\_store\_directory pragma](../pragma.html#pragma_temp_store_directory), though this could change in a future
release of SQLite.
With SQLITE\_ACCESS\_READ, the xAccess method
checks whether the file is readable. The SQLITE\_ACCESS\_READ constant is
currently unused, though it might be used in a future release of
SQLite.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


