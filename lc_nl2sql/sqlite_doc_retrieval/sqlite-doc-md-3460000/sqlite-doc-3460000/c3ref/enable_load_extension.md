




Enable Or Disable Extension Loading




[![SQLite](../images/sqlite370_banner.gif)](../index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](../index.html)* [Menu](javascript:void(0))* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [License](../copyright.html)* [Support](../support.html)* [Purchase](../prosupport.html)* [Search](javascript:void(0))




* [About](../about.html)* [Documentation](../docs.html)* [Download](../download.html)* [Support](../support.html)* [Purchase](../prosupport.html)






Search Documentation
Search Changelog









[## SQLite C Interface](../c3ref/intro.html)
## Enable Or Disable Extension Loading




> ```
> 
> int sqlite3_enable_load_extension(sqlite3 *db, int onoff);
> 
> ```



So as not to open security holes in older applications that are
unprepared to deal with [extension loading](../loadext.html), and as a means of disabling
[extension loading](../loadext.html) while evaluating user\-entered SQL, the following API
is provided to turn the [sqlite3\_load\_extension()](../c3ref/load_extension.html) mechanism on and off.


Extension loading is off by default.
Call the sqlite3\_enable\_load\_extension() routine with onoff\=\=1
to turn extension loading on and call it with onoff\=\=0 to turn
it back off again.


This interface enables or disables both the C\-API
[sqlite3\_load\_extension()](../c3ref/load_extension.html) and the SQL function [load\_extension()](../lang_corefunc.html#load_extension).
Use [sqlite3\_db\_config](../c3ref/db_config.html)(db,[SQLITE\_DBCONFIG\_ENABLE\_LOAD\_EXTENSION](../c3ref/c_dbconfig_defensive.html#sqlitedbconfigenableloadextension),..)
to enable or disable only the C\-API.


**Security warning:** It is recommended that extension loading
be enabled using the [SQLITE\_DBCONFIG\_ENABLE\_LOAD\_EXTENSION](../c3ref/c_dbconfig_defensive.html#sqlitedbconfigenableloadextension) method
rather than this interface, so the [load\_extension()](../lang_corefunc.html#load_extension) SQL function
remains disabled. This will prevent SQL injections from giving attackers
access to extension loading capabilities.


See also lists of
 [Objects](../c3ref/objlist.html),
 [Constants](../c3ref/constlist.html), and
 [Functions](../c3ref/funclist.html).


