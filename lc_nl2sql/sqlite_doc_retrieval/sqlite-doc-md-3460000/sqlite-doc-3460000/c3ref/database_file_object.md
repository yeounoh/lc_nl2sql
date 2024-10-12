




Database File Corresponding To A Journal




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Database File Corresponding To A Journal




> ```
> 
> sqlite3_file *sqlite3_database_file_object(const char*);
> 
> ```



If X is the name of a rollback or WAL\-mode journal file that is
passed into the xOpen method of [sqlite3\_vfs](../c3ref/vfs.html), then
sqlite3\_database\_file\_object(X) returns a pointer to the [sqlite3\_file](../c3ref/file.html)
object that represents the main database file.


This routine is intended for use in custom [VFS](../vfs.html) implementations
only. It is not a general\-purpose interface.
The argument sqlite3\_file\_object(X) must be a filename pointer that
has been passed into [sqlite3\_vfs](../c3ref/vfs.html).xOpen method where the
flags parameter to xOpen contains one of the bits
[SQLITE\_OPEN\_MAIN\_JOURNAL](../c3ref/c_open_autoproxy.html) or [SQLITE\_OPEN\_WAL](../c3ref/c_open_autoproxy.html). Any other use
of this routine results in undefined and probably undesirable
behavior.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


