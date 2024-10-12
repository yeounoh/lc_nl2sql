




OS Interface Open File Handle




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## OS Interface Open File Handle




> ```
> 
> typedef struct sqlite3_file sqlite3_file;
> struct sqlite3_file {
>   const struct sqlite3_io_methods *pMethods;  /* Methods for an open file */
> };
> 
> ```



An [sqlite3\_file](../c3ref/file.html) object represents an open file in the
[OS interface layer](../c3ref/vfs.html). Individual OS interface
implementations will
want to subclass this object by appending additional fields
for their own use. The pMethods entry is a pointer to an
[sqlite3\_io\_methods](../c3ref/io_methods.html) object that defines methods for performing
I/O operations on the open file.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


