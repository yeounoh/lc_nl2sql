




Prepare Flags




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Prepare Flags




> ```
> 
> #define SQLITE_PREPARE_PERSISTENT              0x01
> #define SQLITE_PREPARE_NORMALIZE               0x02
> #define SQLITE_PREPARE_NO_VTAB                 0x04
> 
> ```



These constants define various flags that can be passed into
"prepFlags" parameter of the [sqlite3\_prepare\_v3()](../c3ref/prepare.html) and
[sqlite3\_prepare16\_v3()](../c3ref/prepare.html) interfaces.


New flags may be added in future releases of SQLite.




SQLITE\_PREPARE\_PERSISTENT
The SQLITE\_PREPARE\_PERSISTENT flag is a hint to the query planner
that the prepared statement will be retained for a long time and
probably reused many times. Without this flag, [sqlite3\_prepare\_v3()](../c3ref/prepare.html)
and [sqlite3\_prepare16\_v3()](../c3ref/prepare.html) assume that the prepared statement will
be used just once or at most a few times and then destroyed using
[sqlite3\_finalize()](../c3ref/finalize.html) relatively soon. The current implementation acts
on this hint by avoiding the use of [lookaside memory](../malloc.html#lookaside) so as not to
deplete the limited store of lookaside memory. Future versions of
SQLite may act on this hint differently.



SQLITE\_PREPARE\_NORMALIZE
The SQLITE\_PREPARE\_NORMALIZE flag is a no\-op. This flag used
to be required for any prepared statement that wanted to use the
[sqlite3\_normalized\_sql()](../c3ref/expanded_sql.html) interface. However, the
[sqlite3\_normalized\_sql()](../c3ref/expanded_sql.html) interface is now available to all
prepared statements, regardless of whether or not they use this
flag.



SQLITE\_PREPARE\_NO\_VTAB
The SQLITE\_PREPARE\_NO\_VTAB flag causes the SQL compiler
to return an error (error code SQLITE\_ERROR) if the statement uses
any virtual tables.



See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


