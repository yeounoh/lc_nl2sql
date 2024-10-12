




Error Logging Interface




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Error Logging Interface




> ```
> 
> void sqlite3_log(int iErrCode, const char *zFormat, ...);
> 
> ```



The [sqlite3\_log()](../c3ref/log.html) interface writes a message into the [error log](../errlog.html)
established by the [SQLITE\_CONFIG\_LOG](../c3ref/c_config_covering_index_scan.html#sqliteconfiglog) option to [sqlite3\_config()](../c3ref/config.html).
If logging is enabled, the zFormat string and subsequent arguments are
used with [sqlite3\_snprintf()](../c3ref/mprintf.html) to generate the final output string.


The sqlite3\_log() interface is intended for use by extensions such as
virtual tables, collating functions, and SQL functions. While there is
nothing to prevent an application from calling sqlite3\_log(), doing so
is considered bad form.


The zFormat string must not be NULL.


To avoid deadlocks and other threading problems, the sqlite3\_log() routine
will not use dynamically allocated memory. The log message is stored in
a fixed\-length buffer on the stack. If the log message is longer than
a few hundred characters, it will be truncated to the length of the
buffer.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


