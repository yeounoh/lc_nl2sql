




Configure global parameters




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog







[## Session Module C Interface](../session/intro.html)## Configure global parameters


> ```
> int sqlite3session_config(int op, void *pArg);
> 
> ```


The sqlite3session\_config() interface is used to make global configuration
changes to the sessions module in order to tune it to the specific needs 
of the application.


The sqlite3session\_config() interface is not threadsafe. If it is invoked
while any other thread is inside any other sessions method then the
results are undefined. Furthermore, if it is invoked after any sessions
related objects have been created, the results are also undefined. 


The first argument to the sqlite3session\_config() function must be one
of the SQLITE\_SESSION\_CONFIG\_XXX constants defined below. The 
interpretation of the (void\*) value passed as the second parameter and
the effect of calling this function depends on the value of the first
parameter.



SQLITE\_SESSION\_CONFIG\_STRMSIZE
 By default, the sessions module streaming interfaces attempt to input
 and output data in approximately 1 KiB chunks. This operand may be used
 to set and query the value of this configuration setting. The pointer
 passed as the second argument must point to a value of type (int).
 If this value is greater than 0, it is used as the new streaming data
 chunk size for both input and output. Before returning, the (int) value
 pointed to by pArg is set to the final value of the streaming interface
 chunk size.



This function returns SQLITE\_OK if successful, or an SQLite error code
otherwise.


See also lists of
 [Objects](../session/objlist.html),
 [Constants](../session/constlist.html), and
 [Functions](../session/funclist.html).


