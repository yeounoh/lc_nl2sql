




Declared Datatype Of A Query Result




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Declared Datatype Of A Query Result




> ```
> 
> const char *sqlite3_column_decltype(sqlite3_stmt*,int);
> const void *sqlite3_column_decltype16(sqlite3_stmt*,int);
> 
> ```



The first parameter is a [prepared statement](../c3ref/stmt.html).
If this statement is a [SELECT](../lang_select.html) statement and the Nth column of the
returned result set of that [SELECT](../lang_select.html) is a table column (not an
expression or subquery) then the declared type of the table
column is returned. If the Nth column of the result set is an
expression or subquery, then a NULL pointer is returned.
The returned string is always UTF\-8 encoded.


For example, given the database schema:


CREATE TABLE t1(c1 VARIANT);


and the following statement to be compiled:


SELECT c1 \+ 1, c1 FROM t1;


this routine would return the string "VARIANT" for the second result
column (i\=\=1\), and a NULL pointer for the first result column (i\=\=0\).


SQLite uses dynamic run\-time typing. So just because a column
is declared to contain a particular type does not mean that the
data stored in that column is of the declared type. SQLite is
strongly typed, but the typing is dynamic not static. Type
is associated with individual values, not with the containers
used to hold those values.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


