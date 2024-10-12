




DROP TABLE




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










DROP TABLE


**[drop\-table\-stmt:](syntax/drop-table-stmt.html)**
hide








DROP



TABLE



IF



EXISTS



schema\-name



.



table\-name












The DROP TABLE statement removes a table added with the
[CREATE TABLE](lang_createtable.html) statement. The name specified is the
table name. The dropped table is completely removed from the database 
schema and the disk file. The table can not be recovered. 
All indices and triggers
associated with the table are also deleted.


The optional IF EXISTS clause suppresses the error that would normally
result if the table does not exist.


If [foreign key constraints](foreignkeys.html) are enabled, a DROP TABLE command performs an
implicit [DELETE FROM](lang_delete.html) command before removing the
table from the database schema. Any triggers attached to the table are
dropped from the database schema before the implicit DELETE FROM
is executed, so this cannot cause any triggers to fire. By contrast, an
implicit DELETE FROM does cause any configured
[foreign key actions](foreignkeys.html#fk_actions) to take place. 
If the implicit DELETE FROM executed
as part of a DROP TABLE command violates any immediate foreign key constraints,
an error is returned and the table is not dropped. If 
the implicit DELETE FROM causes any 
deferred foreign key constraints to be violated, and the violations still
exist when the transaction is committed, an error is returned at the time
of commit.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


