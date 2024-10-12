




SQLite Runtime Status




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## SQLite Runtime Status




> ```
> 
> int sqlite3_status(int op, int *pCurrent, int *pHighwater, int resetFlag);
> int sqlite3_status64(
>   int op,
>   sqlite3_int64 *pCurrent,
>   sqlite3_int64 *pHighwater,
>   int resetFlag
> );
> 
> ```



These interfaces are used to retrieve runtime status information
about the performance of SQLite, and optionally to reset various
highwater marks. The first argument is an integer code for
the specific parameter to measure. Recognized integer codes
are of the form [SQLITE\_STATUS\_...](../c3ref/c_status_malloc_count.html).
The current value of the parameter is returned into \*pCurrent.
The highest recorded value is returned in \*pHighwater. If the
resetFlag is true, then the highest record value is reset after
\*pHighwater is written. Some parameters do not record the highest
value. For those parameters
nothing is written into \*pHighwater and the resetFlag is ignored.
Other parameters record only the highwater mark and not the current
value. For these latter parameters nothing is written into \*pCurrent.


The sqlite3\_status() and sqlite3\_status64() routines return
SQLITE\_OK on success and a non\-zero [error code](../rescode.html) on failure.


If either the current value or the highwater mark is too large to
be represented by a 32\-bit integer, then the values returned by
sqlite3\_status() are undefined.


See also: [sqlite3\_db\_status()](../c3ref/db_status.html)


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


