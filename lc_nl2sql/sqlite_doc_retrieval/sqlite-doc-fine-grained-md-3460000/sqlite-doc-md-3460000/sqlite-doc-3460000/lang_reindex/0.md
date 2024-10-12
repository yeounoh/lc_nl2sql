




REINDEX




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










REINDEX


**[reindex\-stmt:](syntax/reindex-stmt.html)**
hide








REINDEX



schema\-name



.





index\-name








table\-name









collation\-name









The REINDEX command is used to delete and recreate indices from scratch.
This is useful when the definition of a collation sequence has changed, or
when there are [indexes on expressions](expridx.html) involving a function whose definition
has changed.



If the REINDEX keyword is not followed by a collation\-sequence or database 
object identifier, then all indices in all attached databases are rebuilt.



If the REINDEX keyword is followed by a collation\-sequence name, then
all indices in all attached databases that use the named collation sequences
are recreated. 



Or, if the argument attached to the REINDEX identifies a specific 
database table, then all indices attached to the database table are rebuilt. 
If it identifies a specific database index, then just that index is recreated.



For a command of the form "REINDEX *name*", a match
against collation\-name takes precedence over a match
against index\-name or table\-name.
This ambiguity in the syntax may be avoided by always specifying a
schema\-name when reindexing a specific table or index.


*This page last modified on [2022\-01\-08 05:02:57](https://sqlite.org/docsrc/honeypot) UTC* 


