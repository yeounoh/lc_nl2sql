




DROP VIEW




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










DROP VIEW


**[drop\-view\-stmt:](syntax/drop-view-stmt.html)**
hide








DROP



VIEW



IF



EXISTS



schema\-name



.



view\-name












The DROP VIEW statement removes a view created by the [CREATE VIEW](lang_createview.html) 
 statement. The view definition is removed from the database schema, but 
 no actual data in the underlying base tables is modified.



The view to drop is identified by the view\-name and optional 
 schema\-name specified as part of the DROP VIEW statement. This 
 reference is resolved using the standard procedure for [object resolution](lang_naming.html).




 If the specified view cannot be found and the IF EXISTS clause is not 
 present, it is an error. If the specified view cannot be found and an IF
 EXISTS clause is present in the DROP VIEW statement, then the statement
 is a no\-op.




*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


