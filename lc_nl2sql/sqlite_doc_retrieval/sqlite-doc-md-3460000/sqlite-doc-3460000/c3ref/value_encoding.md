




Report the internal text encoding state of an sqlite3\_value object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Report the internal text encoding state of an sqlite3\_value object




> ```
> 
> int sqlite3_value_encoding(sqlite3_value*);
> 
> ```



The sqlite3\_value\_encoding(X) interface returns one of [SQLITE\_UTF8](../c3ref/c_any.html),
[SQLITE\_UTF16BE](../c3ref/c_any.html), or [SQLITE\_UTF16LE](../c3ref/c_any.html) according to the current text encoding
of the value X, assuming that X has type TEXT. If sqlite3\_value\_type(X)
returns something other than SQLITE\_TEXT, then the return value from
sqlite3\_value\_encoding(X) is meaningless. Calls to
[sqlite3\_value\_text(X)](../c3ref/value_blob.html), [sqlite3\_value\_text16(X)](../c3ref/value_blob.html), [sqlite3\_value\_text16be(X)](../c3ref/value_blob.html),
[sqlite3\_value\_text16le(X)](../c3ref/value_blob.html), [sqlite3\_value\_bytes(X)](../c3ref/value_blob.html), or
[sqlite3\_value\_bytes16(X)](../c3ref/value_blob.html) might change the encoding of the value X and
thus change the return from subsequent calls to sqlite3\_value\_encoding(X).


This routine is intended for used by applications that test and validate
the SQLite implementation. This routine is inquiring about the opaque
internal state of an [sqlite3\_value](../c3ref/value.html) object. Ordinary applications should
not need to know what the internal state of an sqlite3\_value object is and
hence should not need to use this interface.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


