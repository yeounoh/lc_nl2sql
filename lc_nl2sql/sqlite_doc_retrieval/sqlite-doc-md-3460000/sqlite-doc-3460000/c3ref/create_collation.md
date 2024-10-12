




Define New Collating Sequences




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Define New Collating Sequences




> ```
> 
> int sqlite3_create_collation(
>   sqlite3*,
>   const char *zName,
>   int eTextRep,
>   void *pArg,
>   int(*xCompare)(void*,int,const void*,int,const void*)
> );
> int sqlite3_create_collation_v2(
>   sqlite3*,
>   const char *zName,
>   int eTextRep,
>   void *pArg,
>   int(*xCompare)(void*,int,const void*,int,const void*),
>   void(*xDestroy)(void*)
> );
> int sqlite3_create_collation16(
>   sqlite3*,
>   const void *zName,
>   int eTextRep,
>   void *pArg,
>   int(*xCompare)(void*,int,const void*,int,const void*)
> );
> 
> ```



These functions add, remove, or modify a [collation](../datatype3.html#collation) associated
with the [database connection](../c3ref/sqlite3.html) specified as the first argument.


The name of the collation is a UTF\-8 string
for sqlite3\_create\_collation() and sqlite3\_create\_collation\_v2()
and a UTF\-16 string in native byte order for sqlite3\_create\_collation16().
Collation names that compare equal according to [sqlite3\_strnicmp()](../c3ref/stricmp.html) are
considered to be the same name.


The third argument (eTextRep) must be one of the constants:
* [SQLITE\_UTF8](../c3ref/c_any.html),
* [SQLITE\_UTF16LE](../c3ref/c_any.html),
* [SQLITE\_UTF16BE](../c3ref/c_any.html),
* [SQLITE\_UTF16](../c3ref/c_any.html), or
* [SQLITE\_UTF16\_ALIGNED](../c3ref/c_any.html).


The eTextRep argument determines the encoding of strings passed
to the collating function callback, xCompare.
The [SQLITE\_UTF16](../c3ref/c_any.html) and [SQLITE\_UTF16\_ALIGNED](../c3ref/c_any.html) values for eTextRep
force strings to be UTF16 with native byte order.
The [SQLITE\_UTF16\_ALIGNED](../c3ref/c_any.html) value for eTextRep forces strings to begin
on an even byte address.


The fourth argument, pArg, is an application data pointer that is passed
through as the first argument to the collating function callback.


The fifth argument, xCompare, is a pointer to the collating function.
Multiple collating functions can be registered using the same name but
with different eTextRep parameters and SQLite will use whichever
function requires the least amount of data transformation.
If the xCompare argument is NULL then the collating function is
deleted. When all collating functions having the same name are deleted,
that collation is no longer usable.


The collating function callback is invoked with a copy of the pArg
application data pointer and with two strings in the encoding specified
by the eTextRep argument. The two integer parameters to the collating
function callback are the length of the two strings, in bytes. The collating
function must return an integer that is negative, zero, or positive
if the first string is less than, equal to, or greater than the second,
respectively. A collating function must always return the same answer
given the same inputs. If two or more collating functions are registered
to the same collation name (using different eTextRep values) then all
must give an equivalent answer when invoked with equivalent strings.
The collating function must obey the following properties for all
strings A, B, and C:


1. If A\=\=B then B\=\=A.
- If A\=\=B and B\=\=C then A\=\=C.
- If A\<B THEN B\>A.
- If A\<B and B\<C then A\<C.



If a collating function fails any of the above constraints and that
collating function is registered and used, then the behavior of SQLite
is undefined.


The sqlite3\_create\_collation\_v2() works like sqlite3\_create\_collation()
with the addition that the xDestroy callback is invoked on pArg when
the collating function is deleted.
Collating functions are deleted when they are overridden by later
calls to the collation creation functions or when the
[database connection](../c3ref/sqlite3.html) is closed using [sqlite3\_close()](../c3ref/close.html).


The xDestroy callback is not called if the
sqlite3\_create\_collation\_v2() function fails. Applications that invoke
sqlite3\_create\_collation\_v2() with a non\-NULL xDestroy argument should
check the return code and dispose of the application data pointer
themselves rather than expecting SQLite to deal with it for them.
This is different from every other SQLite interface. The inconsistency
is unfortunate but cannot be changed without breaking backwards
compatibility.


See also: [sqlite3\_collation\_needed()](../c3ref/collation_needed.html) and [sqlite3\_collation\_needed16()](../c3ref/collation_needed.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


