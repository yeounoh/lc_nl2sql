




Dynamic String Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Dynamic String Object




> ```
> 
> typedef struct sqlite3_str sqlite3_str;
> 
> ```



An instance of the sqlite3\_str object contains a dynamically\-sized
string under construction.


The lifecycle of an sqlite3\_str object is as follows:
1. The sqlite3\_str object is created using [sqlite3\_str\_new()](../c3ref/str_new.html).
- Text is appended to the sqlite3\_str object using various
methods, such as [sqlite3\_str\_appendf()](../c3ref/str_append.html).
- The sqlite3\_str object is destroyed and the string it created
is returned using the [sqlite3\_str\_finish()](../c3ref/str_finish.html) interface.




1 Constructor using this object: [sqlite3\_str\_new()](../c3ref/str_new.html)


1 Destructor using this object: [sqlite3\_str\_finish()](../c3ref/str_finish.html)


9 Methods using this object:

* [sqlite3\_str\_append](../c3ref/str_append.html)
* [sqlite3\_str\_appendall](../c3ref/str_append.html)
* [sqlite3\_str\_appendchar](../c3ref/str_append.html)
* [sqlite3\_str\_appendf](../c3ref/str_append.html)
* [sqlite3\_str\_errcode](../c3ref/str_errcode.html)
* [sqlite3\_str\_length](../c3ref/str_errcode.html)
* [sqlite3\_str\_reset](../c3ref/str_append.html)
* [sqlite3\_str\_value](../c3ref/str_errcode.html)
* [sqlite3\_str\_vappendf](../c3ref/str_append.html)






See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


