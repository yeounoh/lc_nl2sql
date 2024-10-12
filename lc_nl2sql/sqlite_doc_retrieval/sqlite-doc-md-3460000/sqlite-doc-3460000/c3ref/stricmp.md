




String Comparison




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## String Comparison




> ```
> 
> int sqlite3_stricmp(const char *, const char *);
> int sqlite3_strnicmp(const char *, const char *, int);
> 
> ```



The [sqlite3\_stricmp()](../c3ref/stricmp.html) and [sqlite3\_strnicmp()](../c3ref/stricmp.html) APIs allow applications
and extensions to compare the contents of two buffers containing UTF\-8
strings in a case\-independent fashion, using the same definition of "case
independence" that SQLite uses internally when comparing identifiers.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


