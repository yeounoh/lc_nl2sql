




DETACH




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










DETACH


**[detach\-stmt:](syntax/detach-stmt.html)**
hide








DETACH



DATABASE



schema\-name









This statement detaches an additional database connection previously 
attached using the [ATTACH](lang_attach.html) statement. 
When not in [shared cache mode](sharedcache.html), 
it is possible to have the same database file attached multiple times using 
different names, and detaching one connection to a file will leave the 
others intact.



In [shared cache mode](sharedcache.html), attempting to attach the same database file more
than once results in an error.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


