




Low\-Level Control Of Database Files




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Low\-Level Control Of Database Files




> ```
> 
> int sqlite3_file_control(sqlite3*, const char *zDbName, int op, void*);
> 
> ```



The [sqlite3\_file\_control()](../c3ref/file_control.html) interface makes a direct call to the
xFileControl method for the [sqlite3\_io\_methods](../c3ref/io_methods.html) object associated
with a particular database identified by the second argument. The
name of the database is "main" for the main database or "temp" for the
TEMP database, or the name that appears after the AS keyword for
databases that are added using the [ATTACH](../lang_attach.html) SQL command.
A NULL pointer can be used in place of "main" to refer to the
main database file.
The third and fourth parameters to this routine
are passed directly through to the second and third parameters of
the xFileControl method. The return value of the xFileControl
method becomes the return value of this routine.


A few opcodes for [sqlite3\_file\_control()](../c3ref/file_control.html) are handled directly
by the SQLite core and never invoke the
sqlite3\_io\_methods.xFileControl method.
The [SQLITE\_FCNTL\_FILE\_POINTER](../c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlfilepointer) value for the op parameter causes
a pointer to the underlying [sqlite3\_file](../c3ref/file.html) object to be written into
the space pointed to by the 4th parameter. The
[SQLITE\_FCNTL\_JOURNAL\_POINTER](../c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntljournalpointer) works similarly except that it returns
the [sqlite3\_file](../c3ref/file.html) object associated with the journal file instead of
the main database. The [SQLITE\_FCNTL\_VFS\_POINTER](../c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntlvfspointer) opcode returns
a pointer to the underlying [sqlite3\_vfs](../c3ref/vfs.html) object for the file.
The [SQLITE\_FCNTL\_DATA\_VERSION](../c3ref/c_fcntl_begin_atomic_write.html#sqlitefcntldataversion) returns the data version counter
from the pager.


If the second parameter (zDbName) does not match the name of any
open database file, then SQLITE\_ERROR is returned. This error
code is not remembered and will not be recalled by [sqlite3\_errcode()](../c3ref/errcode.html)
or [sqlite3\_errmsg()](../c3ref/errcode.html). The underlying xFileControl method might
also return SQLITE\_ERROR. There is no way to distinguish between
an incorrect zDbName and an SQLITE\_ERROR return from the underlying
xFileControl method.


See also: [file control opcodes](../c3ref/c_fcntl_begin_atomic_write.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


