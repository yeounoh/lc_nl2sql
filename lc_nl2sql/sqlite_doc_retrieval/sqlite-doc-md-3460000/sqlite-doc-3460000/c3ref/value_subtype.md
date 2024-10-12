




Finding The Subtype Of SQL Values




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Finding The Subtype Of SQL Values




> ```
> 
> unsigned int sqlite3_value_subtype(sqlite3_value*);
> 
> ```



The sqlite3\_value\_subtype(V) function returns the subtype for
an [application\-defined SQL function](../appfunc.html) argument V. The subtype
information can be used to pass a limited amount of context from
one SQL function to another. Use the [sqlite3\_result\_subtype()](../c3ref/result_subtype.html)
routine to set the subtype for the return value of an SQL function.


Every [application\-defined SQL function](../appfunc.html) that invoke this interface
should include the [SQLITE\_SUBTYPE](../c3ref/c_deterministic.html#sqlitesubtype) property in the text
encoding argument when the function is [registered](../c3ref/create_function.html).
If the [SQLITE\_SUBTYPE](../c3ref/c_deterministic.html#sqlitesubtype) property is omitted, then sqlite3\_value\_subtype()
might return zero instead of the upstream subtype in some corner cases.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


