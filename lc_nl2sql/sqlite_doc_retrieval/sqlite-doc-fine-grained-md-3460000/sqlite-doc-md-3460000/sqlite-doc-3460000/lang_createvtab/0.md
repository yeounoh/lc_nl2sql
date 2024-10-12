




CREATE VIRTUAL TABLE




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










CREATE VIRTUAL TABLE


**[create\-virtual\-table\-stmt:](syntax/create-virtual-table-stmt.html)**
hide








CREATE



VIRTUAL



TABLE



IF



NOT



EXISTS

schema\-name



.



table\-name

USING



module\-name



(



module\-argument



)




,























A [virtual table](vtab.html) is an interface to an external storage or computation
engine that appears to be a table but does not actually store information
in the database file.


In general, you can do anything with a [virtual table](vtab.html) that can be done
with an ordinary table, except that you cannot create indices or triggers on a
virtual table. Some virtual table implementations might impose additional
restrictions. For example, many virtual tables are read\-only.


The module\-name is the name of an object that implements
the virtual table. The module\-name must be registered with
the SQLite database connection using
[sqlite3\_create\_module()](c3ref/create_module.html) or [sqlite3\_create\_module\_v2()](c3ref/create_module.html)
prior to issuing the CREATE VIRTUAL TABLE statement.
The module takes zero or more comma\-separated arguments.
The arguments can be just about any text as long as it has balanced
parentheses. The argument syntax is sufficiently general that the
arguments can be made to appear as [column definitions](lang_createtable.html#tablecoldef) in a traditional
[CREATE TABLE](lang_createtable.html) statement. 
SQLite passes the module arguments directly
to the [xCreate](vtab.html#xcreate) and [xConnect](vtab.html#xconnect) methods of the module implementation
without any interpretation. It is the responsibility
of the module implementation to parse and interpret its own arguments.


A virtual table is destroyed using the ordinary
[DROP TABLE](lang_droptable.html) statement. There is no
DROP VIRTUAL TABLE statement.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


