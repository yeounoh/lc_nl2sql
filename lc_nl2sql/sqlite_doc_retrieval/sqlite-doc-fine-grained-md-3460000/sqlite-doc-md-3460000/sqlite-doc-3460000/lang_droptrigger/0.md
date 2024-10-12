




DROP TRIGGER




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







**[drop\-trigger\-stmt:](syntax/drop-trigger-stmt.html)**
hide








DROP



TRIGGER



IF



EXISTS



schema\-name



.



trigger\-name












The DROP TRIGGER statement removes a trigger created by the 
[CREATE TRIGGER](lang_createtrigger.html) statement. Once removed, the trigger definition is no
longer present in the [sqlite\_schema](schematab.html) (or sqlite\_temp\_schema) table and is
not fired by any subsequent INSERT, UPDATE or DELETE statements.

Note that triggers are automatically dropped when the associated table is
dropped.
*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 






