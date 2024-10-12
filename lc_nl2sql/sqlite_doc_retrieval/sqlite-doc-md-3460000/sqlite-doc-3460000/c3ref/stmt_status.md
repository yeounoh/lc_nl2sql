




Prepared Statement Status




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Prepared Statement Status




> ```
> 
> int sqlite3_stmt_status(sqlite3_stmt*, int op,int resetFlg);
> 
> ```



Each prepared statement maintains various
[SQLITE\_STMTSTATUS counters](../c3ref/c_stmtstatus_counter.html) that measure the number
of times it has performed specific operations. These counters can
be used to monitor the performance characteristics of the prepared
statements. For example, if the number of table steps greatly exceeds
the number of table searches or result rows, that would tend to indicate
that the prepared statement is using a full table scan rather than
an index.


This interface is used to retrieve and reset counter values from
a [prepared statement](../c3ref/stmt.html). The first argument is the prepared statement
object to be interrogated. The second argument
is an integer code for a specific [SQLITE\_STMTSTATUS counter](../c3ref/c_stmtstatus_counter.html)
to be interrogated.
The current value of the requested counter is returned.
If the resetFlg is true, then the counter is reset to zero after this
interface call returns.


See also: [sqlite3\_status()](../c3ref/status.html) and [sqlite3\_db\_status()](../c3ref/db_status.html).


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


