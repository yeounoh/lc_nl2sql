




Pseudo\-Random Number Generator




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Pseudo\-Random Number Generator




> ```
> 
> void sqlite3_randomness(int N, void *P);
> 
> ```



SQLite contains a high\-quality pseudo\-random number generator (PRNG) used to
select random [ROWIDs](../lang_createtable.html#rowid) when inserting new records into a table that
already uses the largest possible [ROWID](../lang_createtable.html#rowid). The PRNG is also used for
the built\-in random() and randomblob() SQL functions. This interface allows
applications to access the same PRNG for other purposes.


A call to this routine stores N bytes of randomness into buffer P.
The P parameter can be a NULL pointer.


If this routine has not been previously called or if the previous
call had N less than one or a NULL pointer for P, then the PRNG is
seeded using randomness obtained from the xRandomness method of
the default [sqlite3\_vfs](../c3ref/vfs.html) object.
If the previous call to this routine had an N of 1 or more and a
non\-NULL P then the pseudo\-randomness is generated
internally and without recourse to the [sqlite3\_vfs](../c3ref/vfs.html) xRandomness
method.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


