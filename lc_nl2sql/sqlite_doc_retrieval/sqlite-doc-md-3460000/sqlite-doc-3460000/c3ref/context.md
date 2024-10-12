




SQL Function Context Object




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## SQL Function Context Object




> ```
> 
> typedef struct sqlite3_context sqlite3_context;
> 
> ```



The context in which an SQL function executes is stored in an
sqlite3\_context object. A pointer to an sqlite3\_context object
is always first parameter to [application\-defined SQL functions](../appfunc.html).
The application\-defined SQL function implementation will pass this
pointer through into calls to [sqlite3\_result()](../c3ref/result_blob.html),
[sqlite3\_aggregate\_context()](../c3ref/aggregate_context.html), [sqlite3\_user\_data()](../c3ref/user_data.html),
[sqlite3\_context\_db\_handle()](../c3ref/context_db_handle.html), [sqlite3\_get\_auxdata()](../c3ref/get_auxdata.html),
and/or [sqlite3\_set\_auxdata()](../c3ref/get_auxdata.html).


26 Methods using this object:

* [sqlite3\_aggregate\_context](../c3ref/aggregate_context.html)
* [sqlite3\_context\_db\_handle](../c3ref/context_db_handle.html)
* [sqlite3\_get\_auxdata](../c3ref/get_auxdata.html)
* [sqlite3\_result\_blob](../c3ref/result_blob.html)
* [sqlite3\_result\_blob64](../c3ref/result_blob.html)
* [sqlite3\_result\_double](../c3ref/result_blob.html)
* [sqlite3\_result\_error](../c3ref/result_blob.html)
* [sqlite3\_result\_error16](../c3ref/result_blob.html)
* [sqlite3\_result\_error\_code](../c3ref/result_blob.html)
* [sqlite3\_result\_error\_nomem](../c3ref/result_blob.html)
* [sqlite3\_result\_error\_toobig](../c3ref/result_blob.html)
* [sqlite3\_result\_int](../c3ref/result_blob.html)
* [sqlite3\_result\_int64](../c3ref/result_blob.html)
* [sqlite3\_result\_null](../c3ref/result_blob.html)
* [sqlite3\_result\_pointer](../c3ref/result_blob.html)
* [sqlite3\_result\_subtype](../c3ref/result_subtype.html)
* [sqlite3\_result\_text](../c3ref/result_blob.html)
* [sqlite3\_result\_text16](../c3ref/result_blob.html)
* [sqlite3\_result\_text16be](../c3ref/result_blob.html)
* [sqlite3\_result\_text16le](../c3ref/result_blob.html)
* [sqlite3\_result\_text64](../c3ref/result_blob.html)
* [sqlite3\_result\_value](../c3ref/result_blob.html)
* [sqlite3\_result\_zeroblob](../c3ref/result_blob.html)
* [sqlite3\_result\_zeroblob64](../c3ref/result_blob.html)
* [sqlite3\_set\_auxdata](../c3ref/get_auxdata.html)
* [sqlite3\_user\_data](../c3ref/user_data.html)






See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


