




Setting The Subtype Of An SQL Function




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Setting The Subtype Of An SQL Function




> ```
> 
> void sqlite3_result_subtype(sqlite3_context*,unsigned int);
> 
> ```



The sqlite3\_result\_subtype(C,T) function causes the subtype of
the result from the [application\-defined SQL function](../appfunc.html) with
[sqlite3\_context](../c3ref/context.html) C to be the value T. Only the lower 8 bits
of the subtype T are preserved in current versions of SQLite;
higher order bits are discarded.
The number of subtype bytes preserved by SQLite might increase
in future releases of SQLite.


Every [application\-defined SQL function](../appfunc.html) that invokes this interface
should include the [SQLITE\_RESULT\_SUBTYPE](../c3ref/c_deterministic.html#sqliteresultsubtype) property in its
text encoding argument when the SQL function is
[registered](../c3ref/create_function.html). If the [SQLITE\_RESULT\_SUBTYPE](../c3ref/c_deterministic.html#sqliteresultsubtype)
property is omitted from the function that invokes sqlite3\_result\_subtype(),
then in some cases the sqlite3\_result\_subtype() might fail to set
the result subtype.


If SQLite is compiled with \-DSQLITE\_STRICT\_SUBTYPE\=1, then any
SQL function that invokes the sqlite3\_result\_subtype() interface
and that does not have the SQLITE\_RESULT\_SUBTYPE property will raise
an error. Future versions of SQLite might enable \-DSQLITE\_STRICT\_SUBTYPE\=1
by default.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


