




Collation Needed Callbacks




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Collation Needed Callbacks




> ```
> 
> int sqlite3_collation_needed(
>   sqlite3*,
>   void*,
>   void(*)(void*,sqlite3*,int eTextRep,const char*)
> );
> int sqlite3_collation_needed16(
>   sqlite3*,
>   void*,
>   void(*)(void*,sqlite3*,int eTextRep,const void*)
> );
> 
> ```



To avoid having to register all collation sequences before a database
can be used, a single callback function may be registered with the
[database connection](../c3ref/sqlite3.html) to be invoked whenever an undefined collation
sequence is required.


If the function is registered using the sqlite3\_collation\_needed() API,
then it is passed the names of undefined collation sequences as strings
encoded in UTF\-8\. If sqlite3\_collation\_needed16() is used,
the names are passed as UTF\-16 in machine native byte order.
A call to either function replaces the existing collation\-needed callback.


When the callback is invoked, the first argument passed is a copy
of the second argument to sqlite3\_collation\_needed() or
sqlite3\_collation\_needed16(). The second argument is the database
connection. The third argument is one of [SQLITE\_UTF8](../c3ref/c_any.html), [SQLITE\_UTF16BE](../c3ref/c_any.html),
or [SQLITE\_UTF16LE](../c3ref/c_any.html), indicating the most desirable form of the collation
sequence function required. The fourth parameter is the name of the
required collation sequence.


The callback function should register the desired collation using
[sqlite3\_create\_collation()](../c3ref/create_collation.html), [sqlite3\_create\_collation16()](../c3ref/create_collation.html), or
[sqlite3\_create\_collation\_v2()](../c3ref/create_collation.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


