




Translate filenames




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Translate filenames




> ```
> 
> const char *sqlite3_filename_database(sqlite3_filename);
> const char *sqlite3_filename_journal(sqlite3_filename);
> const char *sqlite3_filename_wal(sqlite3_filename);
> 
> ```



These routines are available to [custom VFS implementations](../vfs.html) for
translating filenames between the main database file, the journal file,
and the WAL file.


If F is the name of an sqlite database file, journal file, or WAL file
passed by the SQLite core into the VFS, then sqlite3\_filename\_database(F)
returns the name of the corresponding database file.


If F is the name of an sqlite database file, journal file, or WAL file
passed by the SQLite core into the VFS, or if F is a database filename
obtained from [sqlite3\_db\_filename()](../c3ref/db_filename.html), then sqlite3\_filename\_journal(F)
returns the name of the corresponding rollback journal file.


If F is the name of an sqlite database file, journal file, or WAL file
that was passed by the SQLite core into the VFS, or if F is a database
filename obtained from [sqlite3\_db\_filename()](../c3ref/db_filename.html), then
sqlite3\_filename\_wal(F) returns the name of the corresponding
WAL file.


In all of the above, if F is not the name of a database, journal or WAL
filename passed into the VFS from the SQLite core and F is not the
return value from [sqlite3\_db\_filename()](../c3ref/db_filename.html), then the result is
undefined and is likely a memory access violation.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


