




Column Names In A Result Set




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Column Names In A Result Set




> ```
> 
> const char *sqlite3_column_name(sqlite3_stmt*, int N);
> const void *sqlite3_column_name16(sqlite3_stmt*, int N);
> 
> ```



These routines return the name assigned to a particular column
in the result set of a [SELECT](../lang_select.html) statement. The sqlite3\_column\_name()
interface returns a pointer to a zero\-terminated UTF\-8 string
and sqlite3\_column\_name16() returns a pointer to a zero\-terminated
UTF\-16 string. The first parameter is the [prepared statement](../c3ref/stmt.html)
that implements the [SELECT](../lang_select.html) statement. The second parameter is the
column number. The leftmost column is number 0\.


The returned string pointer is valid until either the [prepared statement](../c3ref/stmt.html)
is destroyed by [sqlite3\_finalize()](../c3ref/finalize.html) or until the statement is automatically
reprepared by the first call to [sqlite3\_step()](../c3ref/step.html) for a particular run
or until the next call to
sqlite3\_column\_name() or sqlite3\_column\_name16() on the same column.


If sqlite3\_malloc() fails during the processing of either routine
(for example during a conversion from UTF\-8 to UTF\-16\) then a
NULL pointer is returned.


The name of a result column is the value of the "AS" clause for
that column, if there is an AS clause. If there is no AS clause
then the name of the column is unspecified and may change from
one release of SQLite to the next.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


